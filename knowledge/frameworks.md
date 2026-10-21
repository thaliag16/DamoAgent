# Frameworks — his process, step by step

Tools live in `~/.claude/skills/damostack/bin/`:
- `advalue.py` is the DCF engine
- `adcalc.py` handles cost of capital, ratings, CRP, the VC method, and growth
- `addata.py` fetches his datasets
- `adsearch.py` searches his blog

---

## V1. Narrative to numbers (the five steps)  *(2014/06/numbers-and-narrative-modeling-story, 2017/01/narrative-and-numbers-how-number)*

1. **Develop a story** for the business: what it does, for whom, how big it gets, how it makes
   money, how it beats competitors, and what could go wrong.
2. **Test the story** with the 3P test: is it **possible**, **plausible**, **probable**?
   Check it against the market (how big?), the competition (how many winners?), and the
   company's own resources.
3. **Convert the story into value drivers**:

   | Story element | Value driver |
   |---|---|
   | Market size, market share, pace | Revenue growth (yr 1, yrs 2–5, fade) and revenue in year 10 |
   | Unit economics, economies of scale, moat | Target operating margin and years to reach it |
   | Business model capital intensity | Sales-to-capital ratio (reinvestment) |
   | Business and country risk, life-cycle stage | Cost of capital (initial → mature) |
   | Survival odds | Failure probability and distress proceeds |
   | Lasting competitive advantage | Terminal ROIC vs cost of capital |

4. **Connect the drivers to value**: run `advalue.py`.
5. **Keep the feedback loop open**: show the valuation to people who disagree, update it when
   news arrives, and classify each change as a break, a change, or a shift.

---

## V2. Inputs checklist for `advalue.py`

| Input | Where to get it | Sanity range / his heuristics |
|---|---|---|
| Base revenue, EBIT | Last 12 months (10-K/10-Q), with R&D capitalized and leases adjusted where material | Use operating income before stock-based comp **only if** you value SBC separately; default is to treat SBC as an expense |
| Growth yr 1, yrs 2–5 | The story; compare with industry (`addata.py histgr`) and the year-10 revenue vs market size | Year-10 revenue ÷ year-10 market = implied market share. Is it plausible? |
| Target operating margin | Unit economics plus industry distribution (`addata.py margin`); best-in-class peers | Top-decile margins require a moat |
| Years to converge | How fast scale economies kick in | 3–10 years |
| Sales-to-capital | Industry (`addata.py capex`, the "Sales/Invested Capital" column), company's marginal ratio | Software ~1.5–3, capital-intensive ~0.5–1 |
| Riskfree | Currency-specific; USD = 10y T − US default spread | See market-data.md (5.07% on 1 Oct 2026) |
| Initial cost of capital | `adcalc.py coc` or industry (`addata.py wacc`), at a higher percentile for young or risky firms | US 10th–90th: 5.26–9.88% (Jan 2026) |
| Mature cost of capital | ≈ the median firm (riskfree + ~4–4.5%) | ~8–9% USD at current rates |
| Terminal growth | ≤ riskfree | Default = riskfree |
| Terminal ROIC | = cost of capital (no moat), higher only with a lasting moat | |
| Failure probability | Stage, cash runway, access to capital, business type | Agent heuristic, not his number: young unprofitable 10–40%, mature ~0. Justify it from runway and capital access |
| Debt, cash, minority interests, cross-holdings, options | Balance sheet; options by Black-Scholes or treasury method | Include lease debt |
| Shares | Diluted share count, including RSUs | |

---

## V3. Cost of capital build  *(2015/01/putting-d-in-dcf-cost-of-capital, 2026/02/data-update-5-for-2026-risk-and-hurdle)*

1. Pick the **currency** and get its **riskfree rate** (government bond minus the default spread
   if the sovereign isn't Aaa; or the USD rate plus the inflation differential).
2. **Equity risk premium** = mature-market implied ERP + country risk premium, weighted by where
   the company *operates* (revenues), not where it's listed.
3. **Beta**: bottom-up. Industry unlevered beta (`addata.py betas`), corrected for cash, relevered
   at the firm's market debt-to-equity ratio (`adcalc.py lever`). For private firms owned by
   undiversified owners, use total beta (`addata.py totalbeta`).
4. **Cost of debt**: riskfree + default spread from an actual or synthetic rating
   (`adcalc.py rating --coverage <EBIT/interest>`), then after-tax at the **marginal** rate.
5. **Weights**: market values, with lease debt included.
6. **Plausibility check** against the distribution, then **move it over time** toward the
   mature level.

---

## V4. Pricing (relative valuation)  *(2013/07/market-multiples-global-comparison-and, 2015/06/debt-cash-and-pe-why-cash-is-upper-and)*

1. **Define**: match numerator and denominator (EV with operating metrics, market cap with equity
   metrics), and use the same timing for every firm.
2. **Describe**: get the industry distribution (`addata.py psdata | vebitda | pedata | pbvdata`),
   with median and spread.
3. **Analyze**: name the driver. EV/Sales ↔ operating margin, growth, and reinvestment. PE ↔ growth,
   payout, and risk. P/BV ↔ ROE − cost of equity.
4. **Apply**: compare against firms with similar drivers. Use the driver to adjust (a regression,
   or matrix: multiple vs. driver), not a raw median.
5. **Reconcile with intrinsic value**: if pricing and value disagree, explain why (market mood,
   peer mispricing, or a story difference).

---

## V5. Startups and private companies  *(2016/10/venture-capital-it-is-pricing-not-value, 2015/02/blood-in-shark-tank-pre-money-post, 2026/09/the-scaling-and-profitability-trade-off)*

- **Value it the same way as a public firm** (V1–V2), but with a **failure probability** and,
  for an undiversified owner, a **total-beta** cost of equity. Consider an illiquidity discount
  for private-to-private transactions.
- **Compare with the VC pricing** (`adcalc.py vc`): what exit metric × multiple × target rate gives
  the post-money? What failure rate is hidden in the target rate?
- **Pre-money vs post-money vs "play money"**: post-money = pre-money + new capital. A headline
  unicorn valuation that treats preferred shares as common overstates value.
- **Dilution**: founders should model ownership through future rounds. Value per founder share
  = equity value × founder's eventual share.
- **Scale/profit archetype**: place the business in one of the eight archetypes (lightning in a
  bottle, field of dreams, field of nightmares, niche star, big and broken, small winner,
  small loser, cut your losses) using its market size and growth, capital intensity, unit economics,
  economies of scale, and moats.
- **For entrepreneurs, the practical questions are:** Does scaling make economic sense for this
  business? What has to be true about unit economics? How much capital does it need (sales-to-capital),
  and how much control do you give up to get it?

---

## V6. Life-cycle diagnosis  *(2024/08/the-corporate-life-cycle-corporate)*

| Stage | Signs | Valuation focus | Management task |
|---|---|---|---|
| Start-up / idea | Little or no revenue | Story, market, failure probability | Build a product and business model |
| Young growth | Revenue growth, losses | Growth, target margin, reinvestment, survival | Prove unit economics |
| High growth | Fast growth, turning profitable | Scaling efficiency, margins | Scale |
| Mature growth | Growth slowing, good margins | Excess returns and moat | Defend |
| Mature stable | Low growth, high cash flow | Cash flows, payout, capital structure | Return cash, show restraint |
| Decline | Shrinking revenue, eroding margins | Negative or near-zero growth, liquidation value | Manage decline, divest |

Flag **acting out of stage** (a decliner buying growth, a young firm paying dividends).

---

## V7. Business-model scorecard (scale vs profitability)  *(2026/09/the-scaling-and-profitability-trade-off)*

Rate each one high, medium, or low, with evidence.

| Scalability | | Business building | |
|---|---|---|---|
| Market size | | Unit economics (price − marginal cost) | |
| Market growth | | Economies of scale (fixed-cost leverage) | |
| Industry structure (winner-take-all?) | | Competition and moats | |
| Capital intensity (low = easier) | | | |
| Customer inertia (low = easier) | | | |
| Key-person dependence (low = easier) | | | |

This gives the archetype and the recommended path: scale aggressively, scale carefully, stay
niche, fix the model first, or shut it down.

---

## V8. Investor decision frame  *(2026/03/finding-your-investing-lodestar-in, 2026/10/stock-prices-earnings-and-cashflows-ai)*

1. Value per share (intrinsic) and a **distribution** (Monte Carlo).
2. Price per share, and **what the price implies** (`advalue.py --solve target_margin` or `growth_y2_5`).
3. Gap = price / value, read against the distribution rather than the point estimate. Where
   does the price fall among the simulated values? The wider the distribution, the bigger the gap
   you should want before acting. (This is the agent's reading of his approach; he often places
   the price within his simulated distribution.)
4. **Catalyst**: what makes price converge to value, and when?
5. **Philosophy fit**: does this trade fit your philosophy (value, growth, momentum, passive)?
6. **Sleep test and portfolio context**: position size, diversification, and human-capital exposure.
7. **Re-valuation triggers**: the events that would cause a story break, change, or shift.

---

## V9. Disruptive-technology / AI business check  *(2026/08/ais-bar-mitzvah-moment-from-hype-hope)*

1. **Market size**: build it from the spending it replaces (for AI, employee compensation ≈ $13T
   in the US in 2025, about twice that globally), then cut it down: tool or replacement? Which
   wage tiers? Which industries? Which countries?
2. **Industry economics**: how many winners, and what margins at scale (unit economics: inference
   cost vs price)?
3. **Moats**: what keeps entrants out (data, distribution, switching costs, scale)?
4. **Where in the cycle**: hope and hype → build-up → business building → recalibration.
5. **Second-order effects**: the more optimistic the TAM, the bigger the damage to incumbents and
   the economy. Make sure the story is internally consistent.
