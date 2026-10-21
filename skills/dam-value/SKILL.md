---
name: dam-value
description: Flagship damostack skill. A full Damodaran-style intrinsic valuation of a public or private company - story, 3P test, inputs from filings and his live datasets, FCFF DCF (Ginzu-style engine), sensitivity, Monte Carlo, value vs price, what the price implies, and what to watch - saved as a report. Use for "value X", "what is X worth", "is X overvalued/undervalued", "build a DCF for X", "Damodaran valuation of X".
---

# /dam-value — story → numbers → value → price → decision

## 0. Load

Read `~/.claude/skills/damostack/knowledge/voice.md`; V1, V2, V3, and V8 in
`~/.claude/skills/damostack/knowledge/frameworks.md`; and `market-data.md` in the same folder.

```bash
python3 ~/.claude/skills/damostack/bin/adsearch.py "<company>" -n 5
ls ~/.damostack/valuations/ 2>/dev/null
```

If he has valued this company, WebFetch that post and note his story, key inputs, value, and
date. If a prior damostack valuation exists, load its `inputs.json` and `log.md` and treat this
run as an update.

## 1. Gather facts (do the work; don't make the user do it)

- **Financials**: the last 12 months of revenue, operating income (EBIT), R&D, lease commitments,
  stock-based comp, cash, debt (including leases), minority interests, cross-holdings, diluted
  shares, options/RSUs, effective tax rate, NOLs. Get them from 10-K/10-Q/annual report via WebFetch
  of SEC EDGAR or investor relations, or ask the user for private companies.
- **Price**: current share price and market cap, with the date. (For private firms, use the last
  round's post-money as the "price".)
- **Market inputs (refresh them)**: `adsearch.py --recent 3` for the latest ERP and riskfree rate;
  `addata.py ctryprem <country>` for where it operates.
- **Industry data**: `addata.py margin <industry>`, `addata.py capex <industry>` (sales-to-capital),
  `addata.py wacc <industry>`, `addata.py betas <industry>`.

Tell the user the facts table, with sources and dates, before valuing.

## 2. The story  *(V1; dam-story has the deep version)*

Write the business story in one paragraph: what it does, the market it's in (and how big),
how it wins, profitability at scale, capital needs, risk, and life-cycle stage *(V6)*.
Run the **3P test** in a few lines: what's possible, what's plausible, what's probable.
If the user has a view, use their story; otherwise state yours and invite pushback.

## 3. Story → inputs

Fill the input table, each with **the story reason** and **the data check**:

| Driver | Value | Story reason | Data check |
|---|---|---|---|
| Revenue growth yr 1 / yrs 2–5 | | | Year-10 revenue vs market → implied share |
| Target operating margin / years to converge | | | Industry percentile, best peers |
| Sales-to-capital (1–5 / 6–10) | | | Industry ratio, company's marginal ratio |
| Cost of capital initial → mature | | | `adcalc.py coc` and distribution check |
| Riskfree / terminal growth | | | ≤ riskfree |
| Terminal ROIC | | | = CoC unless there's a moat |
| Failure probability / proceeds | | | Stage, cash runway |

Write `~/.damostack/valuations/<slug>/inputs.json` using the `advalue.py template` schema,
including a `story` field and an `mc` block with low/mode/high ranges for the three or four
most uncertain drivers.

## 4. Run it

```bash
mkdir -p ~/.damostack/valuations/<slug>
python3 ~/.claude/skills/damostack/bin/advalue.py run ~/.damostack/valuations/<slug>/inputs.json \
  --sens --solve target_margin --mc 10000 --md ~/.damostack/valuations/<slug>/valuation.md
```

Also run `--solve growth_y2_5` if growth is the contested driver. Read the sanity flags and fix
real problems; don't just suppress them.

## 5. Pricing cross-check  *(V4)*

Compute the company's multiple on the most relevant metric (EV/Sales for young firms, EV/EBITDA
or PE for mature ones), and compare it with the industry distribution
(`addata.py psdata | vebitda | pedata <industry>`), controlled for its driver. In a sentence,
say whether the market is pricing it in line with peers, and how that compares with your value.

## 6. Present (lead with the answer)

```
## <Company> — value per share <V> vs price <P> (<date>)
Verdict: under this story, <undervalued / overvalued / fairly valued> by X%
(median of simulations <M>; price sits at the <k>th percentile of the value distribution)

The story (one paragraph)
Inputs (table, with story reasons)
Value bridge (from the engine)
What the price implies: "<the market is pricing in a target margin of Y%>"
Pricing cross-check (multiple vs industry)
What would change my mind: 2–3 specific variables/events (story break, change, or shift triggers)
If you hold it / are considering it: questions to ask yourself (philosophy fit, sleep test)
```

Cite his posts for the method and any prior valuation. Show uncertainty honestly. Avoid false
precision: round the value per share sensibly for a highly uncertain company.

Close with: *This is an analytical valuation under a stated story, not personalized investment
advice.*

## 7. Save and log

Append to `~/.damostack/valuations/<slug>/log.md`:
```
## <YYYY-MM-DD> — value <V> vs price <P> (<gap>)
story: <one line>
key inputs: growth <g>, target margin <m>, S/C <s>, CoC <c0>→<cm>, p(fail) <p>
watch: <triggers>
```
On later runs, compare with the previous entry and classify what changed: a **story break**,
**change**, or **shift** *(2025/01/deepseek-crashes-ai-party-story-break)*.
