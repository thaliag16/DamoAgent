# DamoAgent

**An Aswath Damodaran–style valuation agent for Claude Code.** (Internally the skill pack is called *damostack*.)

A set of Claude Code skills that act as a valuation advisor reasoning the way **Aswath
Damodaran** does: story first, then numbers; value kept separate from price; current market data;
and honest about uncertainty. It's built for **entrepreneurs** (what is my company worth, should I
scale, is this term sheet fair) and **investors** (what is this stock worth, what is the price
assuming, how do I decide).

> damostack is an AI advisor modeled on Professor Damodaran's published work (his blog *Musings
> on Markets*, his Substack, his NYU datasets and books). It is not Aswath Damodaran and isn't
> affiliated with him or NYU Stern. It paraphrases and cites his posts and links to the
> originals; read them. It provides analysis, not personalized investment advice.

## Skills

| Command | What it does |
|---|---|
| `/dam` | Entry point. Answers any valuation or investing question with citations, or routes to the right skill below. |
| **`/dam-value`** | **Flagship.** Full intrinsic valuation: facts from filings, the story and 3P test, story → inputs, FCFF DCF, sensitivity, Monte Carlo, what the price implies, a pricing cross-check, a verdict, and what to watch. Saves a report. |
| `/dam-story` | Builds and tests the business story: a bottom-up market size instead of a hallucinated TAM, the 3P test, the scale-vs-profit archetype, and the story mapped to value drivers. Good for pitches. |
| `/dam-startup` | Startups and private companies: intrinsic value with failure risk and total beta, VC pricing decoded, pre/post/"play" money, the dilution path, and whether to scale or build profitability. |
| `/dam-price` | Relative valuation done properly (define, describe, analyze, apply), using his live industry multiples. |
| `/dam-coc` | Discount rate: currency-consistent riskfree rate, implied ERP, operations-weighted country risk, bottom-up beta, synthetic rating, and plausibility checks. |
| `/dam-review` | Grades someone else's DCF, analyst target, fairness opinion, M&A case, or pitch deck against the "dark side" checklist, then rebuilds it. |
| `/dam-invest` | Investor lens: reading the market (implied ERP), the value-to-decision framework, investment philosophy fit, theme stances (AI), and the sleep test. |

Plus a **`damodaran` subagent** (`agents/damodaran.md`) that any Claude Code session can call for a
second opinion.

## Tools (`bin/`, Python standard library only)

```bash
python3 bin/advalue.py template > my.json        # input schema
python3 bin/advalue.py run my.json --sens --solve target_margin --mc 10000 --md report.md
python3 bin/addata.py wacc "software"             # his live industry data (cost of capital)
python3 bin/addata.py capex "software"            # sales-to-invested-capital
python3 bin/addata.py ctryprem india              # country risk premium
python3 bin/addata.py --list                      # all 23 datasets
python3 bin/adcalc.py coc --unlevered-beta 1.2 --de 0.1 --coverage 6 --erp 0.042
python3 bin/adcalc.py vc --exit-metric 100 --exit-multiple 8 --years 5 --target 0.5 --investment 10
python3 bin/adsearch.py nvidia                    # find his posts on a topic
```

`advalue.py` mirrors the structure of his growth-company ("Ginzu") spreadsheet:
- revenue growth, then a fade to the terminal rate
- margin converging to a target
- reinvestment from the sales-to-capital ratio
- tax moving from the effective to the marginal rate, with NOLs
- cost of capital moving from initial to mature
- terminal growth capped at the riskfree rate, with reinvestment = g / ROIC
- a failure probability
- the full equity bridge

It adds sanity flags, a sensitivity grid, a reverse solve ("what the price implies"), and Monte Carlo.

## Knowledge base (`knowledge/`)

| File | Contents |
|---|---|
| `principles.md` | 76 principles in his voice of reasoning, each cited to blog posts (all verified against the archive) |
| `frameworks.md` | V1 narrative → numbers, V2 inputs checklist, V3 cost of capital, V4 pricing, V5 startups/VC, V6 life cycle, V7 scale-vs-profit scorecard, V8 investor decision frame, V9 AI/disruption check |
| `pitfalls.md` | The review checklist: consistency, risk, story, and bias errors |
| `market-data.md` | **Dated** snapshot (1 Oct 2026): riskfree 5.07%, implied ERP 3.70–3.92%, cost-of-capital distributions, default spreads, 2026 context. Refresh before use. |
| `post-index.md` | All 2026 posts plus the essential older ones by theme, with URLs |
| `voice.md` | How the advisor thinks and talks, and its honesty rules |

Built from all **683 posts** on his blog (2008 – October 2026, ~1.5M words, searched in full), his
2026 posts read closely, and his public datasets at pages.stern.nyu.edu/~adamodar.

## Install

```bash
git clone https://github.com/thaliag16/DamoAgent.git ~/DamoAgent
cd ~/DamoAgent && ./setup.sh
```

Keep the clone where it is: the installed skills are symlinks into it, so `git pull` updates them.
Restart Claude Code. Valuations are saved to `~/.damostack/valuations/<company>/`
(`inputs.json`, `valuation.md`, and `log.md`, which tracks how the story and value change over time).

## Keeping it current

- Market inputs refresh live through `addata.py` and `adsearch.py`.
- When he publishes his annual January data updates or the July country risk update, update
  `knowledge/market-data.md`.
- When a new post changes a framework, update `principles.md` and add it to `post-index.md`.

## License

[MIT](LICENSE). The license covers this repo's code and its own text (the summaries, principles,
frameworks, and skills). Aswath Damodaran's posts, books, and datasets are his; the tools read his
public data live from pages.stern.nyu.edu/~adamodar and don't redistribute it.
