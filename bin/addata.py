#!/usr/bin/env python3
"""addata — pull Damodaran's public datasets (pages.stern.nyu.edu/~adamodar) and look up rows.

  addata.py --list                         show available datasets
  addata.py wacc "software"                industry cost of capital (US, latest update)
  addata.py margin "semiconductor"         operating, net, EBITDA margins by industry
  addata.py capex "software"               includes Sales / Invested Capital (for sales-to-capital)
  addata.py ctryprem "Brazil"              country risk premium, total ERP, default spread
  addata.py histimpl                       implied ERP by year (last rows)
  addata.py psdata "retail"                EV/Sales, Price/Sales
  addata.py ratings                        coverage ratio -> synthetic rating -> spread

Data is read live, so it is as current as his site (industry data is updated each January;
country risk mid-year; the monthly implied ERP is in the latest ERP<Mon><YY>.xlsx and his blog).
"""
import html
import re
import sys
import urllib.request

BASE = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/"
DATASETS = {
    "wacc": ("wacc.html", "Cost of equity, debt and capital by industry (US)"),
    "betas": ("Betas.html", "Levered/unlevered betas, D/E, cash by industry (US)"),
    "totalbeta": ("totalbeta.html", "Total betas (for private / undiversified owners) by industry"),
    "margin": ("margin.html", "Gross, operating, net, EBITDA margins by industry (US)"),
    "capex": ("capex.html", "Cap ex, depreciation, Sales/Invested Capital by industry (US)"),
    "eva": ("EVA.html", "ROE vs cost of equity, ROC vs cost of capital by industry (US)"),
    "roe": ("roe.html", "Return on equity by industry"),
    "psdata": ("psdata.html", "Price/Sales and EV/Sales by industry (US)"),
    "vebitda": ("vebitda.html", "EV/EBITDA, EV/EBIT multiples by industry (US)"),
    "pedata": ("pedata.html", "PE ratios and PEG by industry (US)"),
    "pbvdata": ("pbvdata.html", "Price to book by industry (US)"),
    "fundgr": ("fundgr.html", "Fundamental growth (ROE x retention) by industry"),
    "histgr": ("histgr.html", "Historical growth rates by industry"),
    "taxrate": ("taxrate.html", "Effective tax rates by industry (US)"),
    "countrytax": ("countrytaxrates.html", "Marginal corporate tax rates by country"),
    "ctryprem": ("ctryprem.html", "Country risk premiums, total ERP, default spreads by country"),
    "histimpl": ("histimpl.html", "Implied ERP for the S&P 500, annual since 1960"),
    "histret": ("histretSP.html", "Historical returns on stocks, bonds, bills"),
    "ratings": ("ratings.html", "Interest coverage -> synthetic rating -> default spread"),
    "wcdata": ("wcdata.html", "Working capital ratios by industry"),
    "rd": ("R&D.html", "R&D spending by industry"),
    "macro": ("macro.html", "Macro data: rates, inflation, GDP"),
    "optvar": ("optvar.html", "Standard deviations (equity & firm value) by industry"),
}


def fetch(name):
    path = DATASETS[name][0]
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "damostack/1.0"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("latin-1")
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    date = re.search(r"Date of Analysis\s*:\s*(?:Data used is as of\s*)?(.{0,40}?)(?:\s+Download|\s+If you|\.|$)", text)
    rows = []
    for r in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", raw):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip()
                 for c in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", r)]
        if any(cells):
            rows.append(cells)
    return rows, (date.group(1).strip() if date else "see page")


def header_of(rows):
    for r in rows:
        if r and r[0].lower().startswith(("industry", "country", "year", "if ")):
            return r
    return rows[0] if rows else []


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "--list"):
        print(__doc__)
        for k, (p, d) in DATASETS.items():
            print(f"  {k:<11} {d}")
        return
    name = args[0].lower()
    if name not in DATASETS:
        sys.exit(f"Unknown dataset '{name}'. Use --list.")
    q = " ".join(args[1:]).lower()
    rows, date = fetch(name)
    hdr = header_of(rows)
    print(f"{DATASETS[name][1]}  |  {BASE}{DATASETS[name][0]}  |  data as of: {date}\n")
    body = [r for r in rows if r is not hdr]
    if name == "histimpl" and not q:
        body = [r for r in body if r and re.match(r"^\d{4}$", r[0])][-12:]
    elif q:
        body = [r for r in body if r and q in r[0].lower()] or \
               [r for r in body if any(q in c.lower() for c in r)]
    else:
        body = body[:40]
    if hdr:
        print(" | ".join(hdr))
        print("-" * min(160, len(" | ".join(hdr))))
    for r in body[:60]:
        print(" | ".join(r))
    if not body:
        print("(no matching rows: try a shorter query, e.g. 'soft' for Software)")
    total = [r for r in rows if r and r[0].lower().startswith(("total market", "total"))]
    if q and total:
        print("\n" + " | ".join(total[-1]))


if __name__ == "__main__":
    main()
