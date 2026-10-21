#!/usr/bin/env python3
"""adcalc — the building blocks of a Damodaran-style valuation.

  coc       cost of capital from riskfree, beta, ERP, country risk, cost of debt, weights
  lever     relever an unlevered (industry) beta: bL = bU * (1 + (1 - t) * D/E)
  rating    synthetic rating and default spread from an interest coverage ratio
  crp       country risk premium = default spread x (equity vol / bond vol)
  vc        venture capital method vs. intrinsic value; pre/post-money and dilution
  reinvest  sustainable growth = reinvestment rate x return on capital

Rates are decimals. Defaults reflect the market as of 1 Oct 2026 (see knowledge/market-data.md);
override them with current numbers.
"""
import argparse

# Large non-financial firms (market cap > $5bn) — interest coverage -> rating -> spread.
# Spreads from Damodaran's ratings.html, data as of January 2026.
LARGE = [(-1e9, 0.2, "D2/D", .19), (0.2, 0.65, "C2/C", .16), (0.65, 0.8, "Ca2/CC", .1261),
         (0.8, 1.25, "Caa/CCC", .0885), (1.25, 1.5, "B3/B-", .0509), (1.5, 1.75, "B2/B", .0321),
         (1.75, 2.0, "B1/B+", .0275), (2.0, 2.25, "Ba2/BB", .0184), (2.25, 2.5, "Ba1/BB+", .0138),
         (2.5, 3.0, "Baa2/BBB", .0111), (3.0, 4.25, "A3/A-", .0089), (4.25, 5.5, "A2/A", .0078),
         (5.5, 6.5, "A1/A+", .0070), (6.5, 8.5, "Aa2/AA", .0055), (8.5, 1e9, "Aaa/AAA", .0040)]
# Smaller / riskier firms (market cap < $5bn) use stricter coverage cut-offs (approximation of
# the smaller-firm table in his cost-of-capital spreadsheet; same rating -> spread map). Verify.
SMALL = [(-1e9, 0.5, "D2/D"), (0.5, 0.8, "C2/C"), (0.8, 1.25, "Ca2/CC"), (1.25, 1.5, "Caa/CCC"),
         (1.5, 2.0, "B3/B-"), (2.0, 2.5, "B2/B"), (2.5, 3.0, "B1/B+"), (3.0, 3.5, "Ba2/BB"),
         (3.5, 4.0, "Ba1/BB+"), (4.0, 4.5, "Baa2/BBB"), (4.5, 6.0, "A3/A-"), (6.0, 7.5, "A2/A"),
         (7.5, 9.5, "A1/A+"), (9.5, 12.5, "Aa2/AA"), (12.5, 1e9, "Aaa/AAA")]
SPREAD = {r: s for _, _, r, s in LARGE}


def rating(cov, size="large"):
    table = LARGE if size == "large" else [(lo, hi, r, SPREAD[r]) for lo, hi, r in SMALL]
    for lo, hi, r, s in table:
        if lo <= cov < hi:
            return r, s
    return table[-1][2], table[-1][3]


def cmd_coc(a):
    beta = a.beta
    if a.unlevered_beta is not None:
        beta = a.unlevered_beta * (1 + (1 - a.tax) * a.de)
    crp = a.crp * a.lam
    coe = a.riskfree + beta * a.erp + crp
    if a.coverage is not None:
        r, s = rating(a.coverage, a.size)
        spread = s + (a.country_spread or 0)
        how = f"synthetic rating {r} (coverage {a.coverage:.2f}, {a.size} firm) -> spread {s:.2%}"
    else:
        spread = a.spread
        how = f"stated default spread {spread:.2%}"
    cod_pre = a.riskfree + spread
    cod = cod_pre * (1 - a.tax)
    wd = a.de / (1 + a.de)
    wacc = coe * (1 - wd) + cod * wd
    print(f"Cost of equity = {a.riskfree:.2%} + {beta:.2f} x {a.erp:.2%}"
          + (f" + {a.lam:.2f} x {a.crp:.2%}" if a.crp else "") + f" = {coe:.2%}")
    print(f"Cost of debt   = ({a.riskfree:.2%} + {spread:.2%}) x (1 - {a.tax:.0%}) = {cod:.2%}   [{how}]")
    print(f"Weights        = equity {1-wd:.1%}, debt {wd:.1%}  (D/E {a.de:.2f}, use market values)")
    print(f"Cost of capital = {wacc:.2%}")
    print("\nPlausibility (Damodaran, Jan 2026): 80% of US firms fall between 5.26% and 9.88% in USD; "
          "global 6.28%–11.66%. Outside that range, check your inputs before trusting it.")
    print("To convert to another currency: (1 + coc_usd) x (1 + inflation_local) / (1 + inflation_usd) - 1.")


def cmd_lever(a):
    bl = a.unlevered_beta * (1 + (1 - a.tax) * a.de)
    print(f"Levered beta = {a.unlevered_beta:.2f} x (1 + (1 - {a.tax:.0%}) x {a.de:.2f}) = {bl:.2f}")


def cmd_rating(a):
    r, s = rating(a.coverage, a.size)
    print(f"Interest coverage {a.coverage:.2f} ({a.size} firm) -> {r}, default spread {s:.2%} "
          "(spreads as of Jan 2026; check addata.py ratings for the latest)")


def cmd_crp(a):
    crp = a.default_spread * a.rel_vol
    print(f"Country risk premium = {a.default_spread:.2%} x {a.rel_vol:.2f} = {crp:.2%}")
    print(f"Total ERP for the country = mature ERP {a.mature_erp:.2%} + {crp:.2%} = {a.mature_erp + crp:.2%}")
    print("Better: look up the country directly with `addata.py ctryprem <country>`.")


def cmd_vc(a):
    # VC method: exit value discounted at a target rate -> post-money.
    exit_value = a.exit_metric * a.exit_multiple
    post_vc = exit_value / (1 + a.target) ** a.years
    pre_vc = post_vc - a.investment
    own = a.investment / post_vc
    print("VENTURE CAPITAL METHOD (a pricing, not a valuation)")
    print(f"  Exit value = {a.exit_metric:,.0f} x {a.exit_multiple:.1f} = {exit_value:,.0f} in year {a.years}")
    print(f"  Post-money = exit / (1 + {a.target:.0%})^{a.years} = {post_vc:,.0f};  pre-money = {pre_vc:,.0f}")
    print(f"  Investor ownership for {a.investment:,.0f}: {own:.1%}")
    if a.retention < 1:
        own_r = own / a.retention
        print(f"  With {1-a.retention:.0%} expected dilution before exit, investor needs {own_r:.1%} today")
    # Same exit, expected-value framing: failure probability + cost of capital.
    ev_exit = exit_value * (1 - a.failure)
    intrinsic = ev_exit / (1 + a.coc) ** a.years
    print("\nEXPECTED-VALUE VIEW (separates failure risk from the discount rate)")
    print(f"  Survival-weighted exit = {exit_value:,.0f} x (1 - {a.failure:.0%}) = {ev_exit:,.0f}")
    print(f"  Discounted at a cost of capital of {a.coc:.1%}: {intrinsic:,.0f} (post-money equivalent)")
    implied = (exit_value / post_vc) ** (1 / a.years) - 1
    surv = (post_vc * (1 + a.coc) ** a.years) / exit_value
    print(f"\n  A {a.target:.0%} target rate is equivalent to a {a.coc:.1%} cost of capital plus a "
          f"cumulative failure probability of {1 - surv:.0%}.")
    print("  The VC target rate bundles failure risk, illiquidity and negotiation into one number. "
          "Ask whether the story actually supports the exit metric and multiple.")
    print(f"  (Check: implied annual return on post-money if the exit happens: {implied:.1%})")


def cmd_reinvest(a):
    g = a.reinvestment_rate * a.roic
    print(f"Sustainable growth = reinvestment rate {a.reinvestment_rate:.0%} x ROIC {a.roic:.1%} = {g:.2%}")
    if a.roic < a.coc:
        print(f"ROIC {a.roic:.1%} is below the cost of capital {a.coc:.1%}: this growth destroys value. "
              "Growth is not free; it is only valuable when ROIC exceeds the cost of capital.")
    elif a.coc:
        print(f"ROIC exceeds the cost of capital by {a.roic - a.coc:.1%}: growth creates value, for as long "
              "as the excess return (the moat) lasts.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    c = s.add_parser("coc", help="cost of capital")
    c.add_argument("--riskfree", type=float, default=0.0507, help="USD riskfree (10y T less US default spread)")
    c.add_argument("--beta", type=float, default=1.0, help="levered beta")
    c.add_argument("--unlevered-beta", type=float, help="industry unlevered beta (relevered with --de)")
    c.add_argument("--erp", type=float, default=0.042, help="mature market ERP")
    c.add_argument("--crp", type=float, default=0.0, help="country risk premium (operations-weighted)")
    c.add_argument("--lam", type=float, default=1.0, help="exposure to the country risk (lambda)")
    c.add_argument("--de", type=float, default=0.0, help="market D/E ratio")
    c.add_argument("--tax", type=float, default=0.25, help="marginal tax rate")
    c.add_argument("--spread", type=float, default=0.0111, help="default spread if no coverage given")
    c.add_argument("--coverage", type=float, help="EBIT / interest expense (gives synthetic rating)")
    c.add_argument("--size", choices=["large", "small"], default="large")
    c.add_argument("--country-spread", type=float, help="add sovereign default spread to cost of debt")
    c.set_defaults(f=cmd_coc)

    l = s.add_parser("lever", help="relever a beta")
    l.add_argument("--unlevered-beta", type=float, required=True)
    l.add_argument("--de", type=float, required=True)
    l.add_argument("--tax", type=float, default=0.25)
    l.set_defaults(f=cmd_lever)

    r = s.add_parser("rating", help="synthetic rating from coverage")
    r.add_argument("--coverage", type=float, required=True)
    r.add_argument("--size", choices=["large", "small"], default="large")
    r.set_defaults(f=cmd_rating)

    k = s.add_parser("crp", help="country risk premium")
    k.add_argument("--default-spread", type=float, required=True)
    k.add_argument("--rel-vol", type=float, default=1.55, help="equity/bond volatility ratio (1.55 in July 2026)")
    k.add_argument("--mature-erp", type=float, default=0.042)
    k.set_defaults(f=cmd_crp)

    v = s.add_parser("vc", help="VC method vs expected value")
    v.add_argument("--exit-metric", type=float, required=True, help="e.g. year-N revenue or earnings")
    v.add_argument("--exit-multiple", type=float, required=True)
    v.add_argument("--years", type=int, default=5)
    v.add_argument("--target", type=float, default=0.40, help="VC target rate of return")
    v.add_argument("--investment", type=float, required=True)
    v.add_argument("--retention", type=float, default=1.0, help="share of stake kept after future dilution")
    v.add_argument("--failure", type=float, default=0.5, help="probability the company fails before exit")
    v.add_argument("--coc", type=float, default=0.12, help="cost of capital for a young firm")
    v.set_defaults(f=cmd_vc)

    g = s.add_parser("reinvest", help="growth from reinvestment and ROIC")
    g.add_argument("--reinvestment-rate", type=float, required=True)
    g.add_argument("--roic", type=float, required=True)
    g.add_argument("--coc", type=float, default=0.0)
    g.set_defaults(f=cmd_reinvest)

    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
