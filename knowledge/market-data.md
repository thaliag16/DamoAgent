# Market data snapshot — as of 1 October 2026

**These numbers go stale.** Before relying on them, refresh them:
- `adsearch.py --recent 5`: his latest post usually reports the start-of-month implied ERP.
- `addata.py histimpl`: the annual implied ERP. The monthly spreadsheet is at
  `https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERP<Mon><YY>.xlsx`, for example `ERPOct26.xlsx`.
- `addata.py ctryprem <country>`: country risk (updated each July).
- `addata.py wacc | betas | margin | capex | psdata ...`: industry data (updated each January).

Always state the as-of date of every market input you use.

## US dollar inputs (start of October 2026)  *(2026/10/stock-prices-earnings-and-cashflows-ai)*

| Input | Value | Notes |
|---|---|---|
| 10-year US Treasury | **5.29%** | Up from 4.18% at the start of 2026; +54 bp in September 2026 alone |
| US dollar riskfree rate | **5.07%** | Treasury less the US default spread (Aa1 rating, 0.22%) |
| Implied ERP (S&P 500) | **3.70%** over the T-bond; **3.92%** over the USD riskfree rate | Below 4% for the first time in 2026 |
| Expected return on stocks | **8.99%** | Up from 8.41% at the start of 2026 |

## Mature-market ERP for country risk (July 2026)  *(2026/07/country-risk-drivers-measures-and)*

- Implied ERP for the US at the start of July 2026: 4.42%. Less the 0.22% Aa1 default spread,
  that gives a **mature market premium of 4.20%**. This is the base he adds country risk premiums to.
- Equity-to-bond relative volatility multiplier: **1.55** (CRP = default spread × 1.55).
- Example: Brazil (Ba1). Adjusted default spread 2.13%, CRP 3.24%, total ERP 7.47%
  (`addata.py ctryprem brazil`).
- Earlier in 2026: ERP 4.37% at the start of March, rising to 4.51% by mid-March during the
  oil and Middle East shock. *(2026/03/the-price-of-risk-equity-risk-premium)*

**Which ERP to use.** For a US-dollar valuation of a company operating mostly in mature markets,
the current implied ERP over the USD riskfree rate is the market-neutral choice. On 1 Oct 2026
that's 3.92% on a 5.07% riskfree rate. For country-risk work, use his published mature-market
premium plus CRP. Say which convention you're following.

## Cost of capital distribution (January 2026 data)  *(2026/02/data-update-5-for-2026-risk-and-hurdle)*

- 80% of US companies had USD costs of capital between **5.26% and 9.88%**; global companies
  between **6.28% and 11.66%**.
- His worked example: a small, newly listed AI firm with global operations would start near
  **11.66%** and move toward **8.65%** as it matures.
- A US public company valuation using a 14% USD cost of capital goes on his "suspect" list.
- These were computed at January 2026 rates. Riskfree rates have risen since, so adjust the
  industry costs of capital roughly by the change in the riskfree rate and the ERP before using them.
- Expected inflation (IMF, used in his currency conversions): US 2.24%, India 4.00%.

## Default spreads by synthetic rating (January 2026, large non-financial firms)  *(ratings.html)*

AAA 0.40% · AA 0.55% · A+ 0.70% · A 0.78% · A- 0.89% · BBB 1.11% · BB+ 1.38% · BB 1.84% ·
B+ 2.75% · B 3.21% · B- 5.09% · CCC 8.85% · CC 12.61% · C 16.00% · D 19.00%

## Market context (2026)  *(2026/10/stock-prices-earnings-and-cashflows-ai, 2026/08/ais-bar-mitzvah-moment-from-hype-hope)*

- US aggregate net income was up 35% (Q1) and 57% (Q2) year on year, driven by AI capex flowing
  into supplier revenues. Cash returned has lagged: the S&P 500 returned 63% of earnings, the
  lowest since 2004.
- US public-company capex was up about 36% year on year in Q2 2026. The top hyperscalers account for more than $2T of AI capex.
- AI product revenue: generous estimates top out around $250B (Anthropic ARR ~$65B and OpenAI
  ~$40B in July 2026), set against trillions of capex.
- SpaceX IPO'd in June 2026 at about $1.8T. His pre-IPO valuation was $1.22T, using an 8% cost of
  capital *(2026/04/to-trillion-dollars-and-beyond-spacex)*, revisited after the prospectus
  *(2026/06/a-weeks-ago-i-assessed-value-of-spacex)*.
- His stated personal stance: holding the market-consensus AI exposure (five of the Mag Seven),
  with new money mostly in short-term Treasuries. He describes himself as not a market timer.
