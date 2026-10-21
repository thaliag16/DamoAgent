---
name: dam-price
description: damostack relative valuation (define, describe, analyze, apply) with his live industry multiples. Triggers: "is 20x revenue reasonable", "comps", "is X cheap vs peers".
---

# /dam-price — pricing, done honestly

Most valuations in practice are pricings. That's fine, as long as you know it and do it
properly *(2020/03/a-viral-market-meltdown-iii-pricing-or)*.

## 0. Load

Read `~/.claude/skills/damostack/knowledge/core.md` (short; replaces reading voice.md and principles.md in full), then run `~/.claude/skills/damostack/bin/kb frameworks V4`.

## 1. Define

Pick the multiple that fits the company's stage and business:
- Young, money-losing → **EV/Sales** (driver: target margin, growth, reinvestment)
- Profitable, capital-light → **EV/EBIT(1−t)**, **PE** (drivers: growth, payout, risk)
- Capital-intensive → **EV/EBITDA** (watch cap ex)
- Banks and insurers → **P/BV** (driver: ROE − cost of equity)

Make it consistent: EV with operating metrics, market cap with equity metrics, and the same
time period (trailing or forward) for every firm.

## 2. Describe

```bash
python3 ~/.claude/skills/damostack/bin/addata.py psdata "<industry>"
python3 ~/.claude/skills/damostack/bin/addata.py vebitda "<industry>"
python3 ~/.claude/skills/damostack/bin/addata.py pedata "<industry>"
python3 ~/.claude/skills/damostack/bin/addata.py margin "<industry>"
```

Report the industry level and the total market for context. If the user names specific peers,
gather their multiples (WebFetch filings or quote pages) and show the median, the spread, and the outliers.

## 3. Analyze

Name the fundamental that drives the multiple and show it next to the multiple for each peer
(EV/Sales with operating margin, PE with expected growth). Where you have enough peers, fit a simple
relationship (multiple vs driver) and read off the predicted multiple for the target. Point out
peers that look cheap only because their fundamentals are weak.

## 4. Apply

The target's predicted multiple × its metric gives the **relative value**. Compare it with the actual
price, and give a range rather than a point.

## 5. Reconcile

If an intrinsic valuation exists (`/dam-value`), compare the two. If the pricing says cheap and the
value says expensive (or the reverse), explain why: the sector may be mispriced, the target's story
may differ from its peers', or the market mood may be extreme.
Be explicit: *a pricing tells you whether it's cheap relative to peers, not whether the peers are right.*
