---
name: dam-startup
description: damostack startup/private-company valuation: intrinsic value vs VC pricing, pre/post-money, dilution, scale vs profitability. Triggers: "what's my startup worth", "is this term sheet fair", "should we scale".
---

# /dam-startup — what your company is worth, and what it's priced at

VC is a pricing game *(2016/10/venture-capital-it-is-pricing-not-value)*. Founders need to know
both the **price** they can get and the **value** of what they're building, and when to choose
scaling over profitability *(2026/09/the-scaling-and-profitability-trade-off)*.

## 0. Load

Read `~/.claude/skills/damostack/knowledge/core.md` (short; replaces reading voice.md and principles.md in full), then run
`~/.claude/skills/damostack/bin/kb frameworks V1 V2 V5 V7`.

## 1. Facts (ask together, as a short list)

Stage; trailing 12-month revenue and growth; gross margin and contribution margin per unit;
burn rate and cash (runway); capital raised and on what terms (post-money, preferences); cap table
(founder, investor, and option-pool percentages); the proposed round, if any (amount, pre-money,
terms); market and competitors; the founders' goals (control vs scale, exit vs long-lived).

## 2. Business-model diagnosis  *(V7)*

Score scalability and business building, name the archetype, and say plainly whether this business
**should** scale aggressively. Many shouldn't. Scaling a broken model makes small failures big
ones. Check:
- **Unit economics**: price − marginal cost per unit. Is it positive now? Will it be at scale?
- **Cash burn**: is it investment (building a model with good unit economics) or subsidy
  (paying users to use a broken model)? *(2016/08/the-bonfire-of-venture-capital-good-bad)*
- **Capital intensity**: how much capital per dollar of new revenue (sales-to-capital)?

## 3. Intrinsic value

Build inputs as in `/dam-value`, with startup adjustments:
- **Failure probability**, from runway, capital access, and stage. Distress proceeds are usually low
  (0–30% of value) for asset-light firms.
- **Cost of capital**: start high (the top decile for its industry and region), moving to the industry
  median. If the owners are **undiversified** (founders, angels), also show the cost of equity using
  **total beta** (`addata.py totalbeta <industry>`) to reflect the risk they actually bear.
- **Illiquidity**: for a private-to-private sale, discuss a discount; don't hide it in the discount rate.

```bash
python3 ~/.claude/skills/damostack/bin/advalue.py run ~/.damostack/valuations/<slug>/inputs.json --sens --mc 10000
```

## 4. The VC pricing, decoded

```bash
python3 ~/.claude/skills/damostack/bin/adcalc.py vc --exit-metric <yr-N revenue or earnings> \
  --exit-multiple <x> --years <N> --target <0.3–0.6> --investment <amount> --retention <0.6–0.8> \
  --failure <p> --coc <young-firm CoC>
```

Explain:
- What post-money the VC's math implies, and the failure probability hidden in their target rate.
- **Pre-money vs post-money vs "play money"**: if later preferred shares carry liquidation
  preferences, the headline post-money (price per share × all shares) overstates the value of
  common shares *(2015/02/blood-in-shark-tank-pre-money-post, 2015/06/billion-dollar-tech-babies-blessing-of)*.
- **Dilution path**: founder ownership after this round and two more hypothetical rounds, and
  founder value = equity value × eventual ownership.

## 5. Advice for the founder

Give concrete recommendations on:
1. **Raise or not, and how much**: enough to reach the next value-creating milestone, given the
   sales-to-capital ratio and burn.
2. **Price**: the range between intrinsic value and the VC pricing, and the terms that matter more
   than the headline number (preferences, control).
3. **Scale vs profitability**: the path that fits the archetype, and the control-vs-ambition trade-off
   (the founder's dilemma).
4. **What builds value fastest**: the driver with the biggest effect in the sensitivity grid
   (usually target margin or growth), and the milestone that would de-risk it (cut the failure
   probability).

For an **investor** in a private round, the same analysis tells you whether the price leaves room
for return given the failure risk, and which terms protect you.

Save to `~/.damostack/valuations/<slug>/` and log it.
