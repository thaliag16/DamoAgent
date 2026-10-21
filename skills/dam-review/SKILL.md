---
name: dam-review
description: damostack critique of a DCF, analyst or banker valuation, M&A case, or pitch deck against Damodaran's "dark side" checklist. Triggers: "review this DCF", "is this target reasonable", "critique this valuation".
---

# /dam-review — grade the valuation like he grades his students'

He reviews and grades many more valuations than he does himself, and he uses benchmarks to spot
the suspect ones *(2026/02/data-update-5-for-2026-risk-and-hurdle)*. This skill does the same.

## 0. Load

Read `~/.claude/skills/damostack/knowledge/core.md` (short; replaces reading voice.md and principles.md in full), then run
`~/.claude/skills/damostack/bin/kb pitfalls`. Get the material: a file path (Read it; for a
spreadsheet, extract the key inputs), a URL (WebFetch it), or pasted text.

## 1. Reconstruct it

Extract the valuation's **story** (stated or implied), its **key inputs** (growth, margins,
reinvestment, cost of capital, terminal growth, terminal ROIC, failure handling), and its **result**
(value, and how it compares with price). If inputs are missing, infer them and say so.

## 2. Run the checklist

Go through `pitfalls.md` silently, then report the **three to five issues that move the value most**,
ranked by impact. For each issue, give:

- **What's wrong** (quote the specific number or assumption)
- **Why it matters**, citing his principle or post
- **The fix**, and **the rough value impact**

Rerun the valuation with the corrected inputs where possible:
```bash
python3 ~/.claude/skills/damostack/bin/advalue.py run <rebuilt-inputs.json> --sens
```

## 3. Bias check

Ask who commissioned it and what outcome they wanted. Is the value suspiciously close to a deal
price or to the last round? Are all the errors in the same direction? *(2016/09/fairness-opinions-fix-them-or-get-rid,
2016/09/keystone-kop-valuations-lazard-evercore)*

## 4. Grade and summarize

```
Grade: A–F (with one-line reason)
Biggest issue: ...
Corrected value range: ... (vs their ...)
What I'd need to believe to accept their number: ...
What they did well: ...
```

For **pitch decks**, focus on TAM construction, ARR claims, unit economics, the scaling story, and
the gap between the asked-for valuation and any defensible intrinsic value. Hand off to
`/dam-startup` for a rebuild. For **M&A**, separate the standalone value, the value of control,
and the synergy (with timing and cost), and check whether the premium paid exceeds all three
*(2015/10/winning-at-losers-game-control-synergy, 2012/12/acquisition-accounting-i-accretive)*.
