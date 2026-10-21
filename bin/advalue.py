#!/usr/bin/env python3
"""advalue — a story-driven FCFF valuation engine in the style of Damodaran's
"Ginzu" spreadsheet for growth companies (pages.stern.nyu.edu/~adamodar/pc/fcffsimpleginzu.xlsx).

  advalue.py run inputs.json                 base-case valuation, year-by-year table
  advalue.py run inputs.json --sens          + sensitivity grid (growth x target margin)
  advalue.py run inputs.json --solve target_margin   what the market price implies
  advalue.py run inputs.json --mc 10000      + Monte Carlo on the ranges in "mc"
  advalue.py run inputs.json --md out.md     also write a markdown report
  advalue.py template                        print a blank input file

The engine is deliberately simple and transparent: every number traces to a story input.
Rates are decimals (0.12 = 12%). Money in any single currency, consistently.

Mechanics (per Damodaran's growth-company structure):
  revenue:     year-1 growth, then a compounded rate for years 2-5, fading linearly
               to the terminal growth rate over years 6-10
  margin:      converges linearly from the year-1 margin to a target pre-tax operating
               margin by `years_to_converge`, then stays there
  taxes:       effective rate in years 1-5, moving to the marginal rate by year 10;
               NOLs shelter income until used up
  reinvestment = change in revenue / sales-to-capital ratio
  FCFF         = EBIT(1 - t) - reinvestment
  discount:    initial cost of capital for years 1-5, moving linearly to the mature
               cost of capital by year 10 (cumulated year by year)
  terminal:    growth <= riskfree rate; reinvestment rate = g / terminal ROIC
               (default terminal ROIC = mature cost of capital, i.e. no excess returns forever)
  failure:     value = (1 - p) x going-concern value + p x distress proceeds
  equity:      operating assets - debt - minority interests + cash + non-operating assets
               - value of employee options; then per share
"""
import argparse
import json
import math
import random
import sys

TEMPLATE = {
    "name": "Example Co",
    "currency": "USD",
    "as_of": "2026-10-01",
    "story": "One paragraph: what the business is, who it sells to, how big it can get, "
             "how profitable at scale, how much it must reinvest, and how risky it is.",
    "base": {
        "revenue": 1000.0, "ebit": -50.0, "invested_capital": 800.0,
        "cash": 300.0, "debt": 100.0, "minority_interests": 0.0,
        "non_operating_assets": 0.0, "options_value": 0.0,
        "shares": 100.0, "price": 25.0,
        "effective_tax": 0.05, "marginal_tax": 0.25, "nol": 400.0
    },
    "drivers": {
        "growth_y1": 0.30, "growth_y2_5": 0.25,
        "margin_y1": None, "target_margin": 0.20, "years_to_converge": 6,
        "sales_to_capital_1_5": 2.0, "sales_to_capital_6_10": 2.0,
        "riskfree": 0.0507, "coc_initial": 0.10, "coc_mature": 0.0865,
        "terminal_growth": None, "terminal_roic": None,
        "failure_prob": 0.05, "distress_proceeds_pct": 0.5,
        "tam_year10": None
    },
    "mc": {
        "growth_y2_5": [0.15, 0.25, 0.35],
        "target_margin": [0.12, 0.20, 0.26],
        "sales_to_capital_1_5": [1.5, 2.0, 3.0],
        "coc_initial": [0.09, 0.10, 0.115]
    }
}

DRIVER_DEFAULTS = {k: v for k, v in TEMPLATE["drivers"].items()}
BASE_DEFAULTS = {"invested_capital": None, "cash": 0.0, "debt": 0.0, "minority_interests": 0.0,
                 "non_operating_assets": 0.0, "options_value": 0.0, "price": None,
                 "effective_tax": 0.25, "marginal_tax": 0.25, "nol": 0.0}


def load(path):
    with open(path) as f:
        inp = json.load(f)
    base = {**BASE_DEFAULTS, **inp.get("base", {})}
    drv = {**DRIVER_DEFAULTS, **inp.get("drivers", {})}
    for k in ("revenue", "ebit", "shares"):
        if base.get(k) is None:
            sys.exit(f"base.{k} is required")
    return inp, base, drv


def value(base, d):
    """Return dict with year-by-year rows and the value bridge."""
    rf = d["riskfree"]
    g_T = d["terminal_growth"] if d.get("terminal_growth") is not None else rf
    coc_m = d["coc_mature"]
    roic_T = d["terminal_roic"] if d.get("terminal_roic") is not None else coc_m
    m1 = d["margin_y1"] if d.get("margin_y1") is not None else base["ebit"] / base["revenue"]
    tgt, conv = d["target_margin"], max(1, int(d["years_to_converge"]))
    t_eff, t_mar = base["effective_tax"], base["marginal_tax"]

    rows, rev_prev, nol = [], base["revenue"], base["nol"]
    ic = base["invested_capital"]
    df_cum, pv_sum = 1.0, 0.0
    for t in range(1, 11):
        if t == 1:
            g = d["growth_y1"]
        elif t <= 5:
            g = d["growth_y2_5"]
        else:
            g = d["growth_y2_5"] - (d["growth_y2_5"] - g_T) * (t - 5) / 5
        rev = rev_prev * (1 + g)
        margin = tgt if t >= conv else tgt - (tgt - m1) * (conv - t) / conv
        ebit = rev * margin
        tax_rate = t_eff if t <= 5 else t_eff + (t_mar - t_eff) * (t - 5) / 5
        taxable = ebit
        if ebit > 0 and nol > 0:
            used = min(nol, ebit)
            nol -= used
            taxable = ebit - used
        elif ebit < 0:
            nol += -ebit
        tax = max(0.0, taxable) * tax_rate
        nopat = ebit - tax
        s2c = d["sales_to_capital_1_5"] if t <= 5 else d["sales_to_capital_6_10"]
        reinv = (rev - rev_prev) / s2c
        fcff = nopat - reinv
        coc = d["coc_initial"] if t <= 5 else d["coc_initial"] + (coc_m - d["coc_initial"]) * (t - 5) / 5
        df_cum /= (1 + coc)
        pv = fcff * df_cum
        pv_sum += pv
        roic = None
        if ic is not None:
            roic = nopat / ic if ic else None
            ic += reinv
        rows.append(dict(t=t, g=g, rev=rev, margin=margin, ebit=ebit, tax_rate=tax_rate,
                         nopat=nopat, reinv=reinv, fcff=fcff, coc=coc, df=df_cum, pv=pv, roic=roic))
        rev_prev = rev

    # Terminal year
    rev_T = rev_prev * (1 + g_T)
    nopat_T = rev_T * tgt * (1 - t_mar)
    reinv_rate_T = g_T / roic_T if roic_T > 0 else 0
    fcff_T = nopat_T * (1 - reinv_rate_T)
    if coc_m <= g_T:
        sys.exit("Mature cost of capital must exceed terminal growth.")
    tv = fcff_T / (coc_m - g_T)
    pv_tv = tv * df_cum
    going = pv_sum + pv_tv
    p, proceeds = d["failure_prob"], d["distress_proceeds_pct"]
    op_assets = (1 - p) * going + p * proceeds * going
    equity = (op_assets - base["debt"] - base["minority_interests"]
              + base["cash"] + base["non_operating_assets"])
    common = equity - base["options_value"]
    per_share = common / base["shares"]
    return dict(rows=rows, g_T=g_T, roic_T=roic_T, rev_T=rev_T, nopat_T=nopat_T, fcff_T=fcff_T,
                reinv_rate_T=reinv_rate_T, tv=tv, pv_tv=pv_tv, pv_sum=pv_sum, going=going,
                op_assets=op_assets, equity=equity, common=common, per_share=per_share,
                tv_share=pv_tv / going if going else float("nan"), m1=m1)


def flags(inp, base, d, r):
    out = []
    rf = d["riskfree"]
    if r["g_T"] > rf + 1e-9:
        out.append(f"Terminal growth {r['g_T']:.2%} exceeds the riskfree rate {rf:.2%}. "
                   "No firm can grow faster than the economy forever; cap it at the riskfree rate.")
    if d["coc_mature"] - r["g_T"] < 0.02:
        out.append("Mature cost of capital is within 2 points of terminal growth: the terminal "
                   "value will be hypersensitive. Recheck both.")
    if r["tv_share"] > 0.85:
        out.append(f"Terminal value is {r['tv_share']:.0%} of operating value, which is normal for young "
                   "companies, but it means the steady-state story (margin, ROIC) carries the valuation.")
    if r["roic_T"] > d["coc_mature"] + 0.05:
        out.append(f"Terminal ROIC {r['roic_T']:.1%} implies a moat lasting forever. Defensible only with a "
                   "strong, specific competitive advantage.")
    if d["target_margin"] > 0.45:
        out.append(f"Target operating margin {d['target_margin']:.0%} is above what all but a handful of "
                   "businesses sustain. Compare with industry data (addata.py margin).")
    if d["coc_initial"] > 0.14:
        out.append(f"Initial cost of capital {d['coc_initial']:.1%} is above the 90th percentile for "
                   "US/global firms. Is failure risk being double-counted in the discount rate?")
    last = r["rows"][-1]
    if last["roic"] is not None and last["roic"] > 0.6:
        out.append(f"Year-10 ROIC of {last['roic']:.0%} suggests the sales-to-capital ratio is too generous "
                   "(growth is coming nearly free).")
    if d.get("tam_year10"):
        share = last["rev"] / d["tam_year10"]
        out.append(f"Year-10 revenue is {share:.1%} of the stated year-10 market. Is that market share plausible "
                   "given competition and industry structure?")
    if d["failure_prob"] == 0 and r["rows"][0]["ebit"] < 0:
        out.append("The company is losing money but failure probability is 0. Young firms fail; consider a "
                   "failure probability rather than a padded discount rate.")
    return out


def fmt(x, w=10, pct=False):
    if x is None:
        return " " * (w - 3) + "n/a"
    return f"{x:>{w}.1%}" if pct else f"{x:>{w},.1f}"


def report(inp, base, d, r, extra=""):
    cur = inp.get("currency", "")
    L = []
    L.append(f"# {inp.get('name', 'Valuation')} — intrinsic value ({cur}, as of {inp.get('as_of', 'n/a')})\n")
    if inp.get("story"):
        L.append(f"**Story:** {inp['story']}\n")
    L.append("| Year | Growth | Revenue | Op margin | EBIT | Tax | NOPAT | Reinvest | FCFF | CoC | PV |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    L.append(f"| Base | | {base['revenue']:,.1f} | {r['m1']:.1%} | {base['ebit']:,.1f} | | | | | | |")
    for x in r["rows"]:
        L.append(f"| {x['t']} | {x['g']:.1%} | {x['rev']:,.1f} | {x['margin']:.1%} | {x['ebit']:,.1f} | "
                 f"{x['tax_rate']:.0%} | {x['nopat']:,.1f} | {x['reinv']:,.1f} | {x['fcff']:,.1f} | "
                 f"{x['coc']:.2%} | {x['pv']:,.1f} |")
    L.append(f"| Terminal | {r['g_T']:.1%} | {r['rev_T']:,.1f} | {d['target_margin']:.1%} | | "
             f"{base['marginal_tax']:.0%} | {r['nopat_T']:,.1f} | {r['nopat_T']*r['reinv_rate_T']:,.1f} | "
             f"{r['fcff_T']:,.1f} | {d['coc_mature']:.2%} | |")
    L.append("")
    L.append("**Value bridge**\n")
    L.append(f"- PV of FCFF, years 1–10: {r['pv_sum']:,.1f}")
    L.append(f"- PV of terminal value: {r['pv_tv']:,.1f}  ({r['tv_share']:.0%} of going-concern value; "
             f"terminal ROIC {r['roic_T']:.1%}, reinvestment rate {r['reinv_rate_T']:.1%})")
    L.append(f"- Going-concern value of operating assets: {r['going']:,.1f}")
    L.append(f"- Adjusted for failure (p = {d['failure_prob']:.0%}, proceeds = {d['distress_proceeds_pct']:.0%}): "
             f"{r['op_assets']:,.1f}")
    L.append(f"- − Debt {base['debt']:,.1f}  − Minority interests {base['minority_interests']:,.1f}  "
             f"+ Cash {base['cash']:,.1f}  + Non-operating assets {base['non_operating_assets']:,.1f}")
    L.append(f"- = Value of equity: {r['equity']:,.1f};  − Options {base['options_value']:,.1f}  "
             f"= Common equity {r['common']:,.1f}")
    L.append(f"- **Value per share: {r['per_share']:,.2f}**")
    if base.get("price"):
        ratio = base["price"] / r["per_share"] if r["per_share"] > 0 else float("inf")
        L.append(f"- Price: {base['price']:,.2f}  →  price is {ratio:.0%} of value "
                 f"({'under' if ratio < 1 else 'over'}valued by {abs(1-ratio):.0%} under this story)")
    fl = flags(inp, base, d, r)
    if fl:
        L.append("\n**Sanity flags**\n")
        L += [f"- {f}" for f in fl]
    if extra:
        L.append(extra)
    return "\n".join(L)


def sens(base, d):
    gs = [d["growth_y2_5"] + k for k in (-0.10, -0.05, 0, 0.05, 0.10)]
    ms = [d["target_margin"] + k for k in (-0.06, -0.03, 0, 0.03, 0.06)]
    L = ["\n\n**Sensitivity: value per share (rows = growth yrs 2–5, cols = target margin)**\n",
         "| g \\ margin | " + " | ".join(f"{m:.0%}" for m in ms) + " |",
         "|---|" + "---|" * len(ms)]
    for g in gs:
        cells = []
        for m in ms:
            dd = {**d, "growth_y2_5": g, "target_margin": m}
            cells.append(f"{value(base, dd)['per_share']:,.2f}")
        L.append(f"| {g:.0%} | " + " | ".join(cells) + " |")
    return "\n".join(L)


def solve(base, d, field):
    price = base.get("price")
    if not price:
        return "\n(--solve needs base.price)"
    lo, hi = {"target_margin": (-0.2, 0.9), "growth_y2_5": (-0.3, 1.5),
              "sales_to_capital_1_5": (0.1, 20), "coc_initial": (0.03, 0.4)}[field]
    f = lambda x: value(base, {**d, field: x})["per_share"] - price
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return f"\n**What the price implies:** no value of {field} in [{lo}, {hi}] reproduces the price."
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    x = (lo + hi) / 2
    shown = f"{x:.1%}" if field != "sales_to_capital_1_5" else f"{x:.2f}"
    return (f"\n\n**What the price implies:** holding everything else fixed, the price of {price:,.2f} "
            f"requires {field} = {shown} (your story says "
            f"{d[field]:.1%}" + (")" if field != "sales_to_capital_1_5" else f" / {d[field]:.2f})") +
            ". Ask whether that is possible, plausible, and probable.")


def monte_carlo(base, d, ranges, n, seed=7):
    rnd = random.Random(seed)
    vals = []
    for _ in range(n):
        dd = dict(d)
        for k, (lo, mode, hi) in ranges.items():
            dd[k] = rnd.triangular(lo, hi, mode)
        try:
            vals.append(value(base, dd)["per_share"])
        except SystemExit:
            continue
    vals.sort()
    q = lambda p: vals[min(len(vals) - 1, int(p * len(vals)))]
    L = [f"\n\n**Monte Carlo ({len(vals):,} runs, triangular distributions on {', '.join(ranges)})**\n",
         f"- 10th / 25th / median / 75th / 90th percentile value per share: "
         f"{q(.10):,.2f} / {q(.25):,.2f} / {q(.5):,.2f} / {q(.75):,.2f} / {q(.90):,.2f}"]
    if base.get("price"):
        under = sum(v > base["price"] for v in vals) / len(vals)
        L.append(f"- Share of outcomes where value exceeds the price ({base['price']:,.2f}): {under:.0%} "
                 f"(the price sits at the {round((1 - under) * 100)}th percentile of the value distribution)")
    L.append("- Uncertainty is not a reason to avoid valuing; it is a reason to show the distribution.")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("template")
    r = s.add_parser("run")
    r.add_argument("inputs")
    r.add_argument("--sens", action="store_true")
    r.add_argument("--solve", choices=["target_margin", "growth_y2_5", "sales_to_capital_1_5", "coc_initial"])
    r.add_argument("--mc", type=int, default=0)
    r.add_argument("--md")
    a = p.parse_args()
    if a.cmd == "template":
        print(json.dumps(TEMPLATE, indent=2))
        return
    inp, base, d = load(a.inputs)
    res = value(base, d)
    extra = ""
    if a.sens:
        extra += sens(base, d)
    if a.solve:
        extra += solve(base, d, a.solve)
    if a.mc:
        ranges = {k: v for k, v in inp.get("mc", {}).items() if k in d}
        extra += monte_carlo(base, d, ranges, a.mc) if ranges else "\n(no 'mc' ranges in inputs)"
    out = report(inp, base, d, res, extra)
    print(out)
    if a.md:
        with open(a.md, "w") as f:
            f.write(out + "\n")


if __name__ == "__main__":
    main()
