---
name: dam-invest
description: damostack investor lens: implied ERP and market reading, value-to-decision framework, investment philosophy fit, the sleep test. Not personalized advice. Triggers: "is the market overvalued", "should I buy X", "my investment philosophy".
---

# /dam-invest — from valuation to an investing decision

There is no single best investment philosophy, only the one that fits you
*(2026/03/finding-your-investing-lodestar-in)*. And whatever you do, it should pass the sleep test
*(2026/10/stock-prices-earnings-and-cashflows-ai)*.

**Scope:** this skill gives frameworks and analysis. It is not personalized financial advice,
so say that when someone asks whether *they* should buy or sell, and leave the decision with them.

## 0. Load

Read `~/.claude/skills/damostack/knowledge/core.md` (short; replaces reading voice.md and principles.md in full), then run
`~/.claude/skills/damostack/bin/kb frameworks V8 V9` and `~/.claude/skills/damostack/bin/kb market-data`.
Refresh: `adsearch.py --recent 3`.

## Mode A — Reading the market

- Report the latest **implied ERP**, the **riskfree rate**, and the **expected return on stocks**,
  each with its date. Compare with history (`addata.py histimpl`).
- His framing: a lower implied ERP means the market is pricing risk cheaply, and a higher one means
  dearly. It's a barometer, not a timing signal. He calls himself not a market timer
  *(2014/06/bubble-bubble-toil-and-trouble-costs)*.
- Put the current narrative in context (AI capex, rates, earnings vs cash returns) from his latest
  posts, paraphrased and cited.

## Mode B — A specific stock

1. Get or build the valuation (`/dam-value`). What matters is **value vs price** and **where the
   price falls in the distribution**.
2. **What the price implies** (`--solve`), and whether that's plausible.
3. **Catalyst**: what makes price and value converge, and over what horizon?
4. **The good company / bad investment check** *(2017/03/explaining-paradox-why-good-bad)*.
5. **Conviction check**: what's the strongest counter-story? What would make you sell? Is leverage
   involved? (Over-conviction plus leverage is how plausible theses ruin people
   *(2026/08/the-situational-awareness-blow-up)*.)

## Mode C — Finding your philosophy

Ask one at a time: How do you think markets make mistakes (slow to react, over-react, systematic
biases)? What's your time horizon? How do you react to losses? What edge do you have (information,
analysis, patience)? How much time will you spend? Then map their answers to a philosophy (passive,
value, growth, momentum or trading, information-driven) and say which one fits, its known failure
modes, and how to stay consistent with it.

## Mode D — Themes (e.g. AI)

Lay out his four stances (all-in, market consensus, skeptic, crash-out), what each implies, and the
evidence to watch (AI revenues vs capex, returns on AI capex vs the cost of capital, write-offs). Remind
them to count **human capital**: if AI threatens your job, your portfolio is already more exposed
than it looks *(2026/10/stock-prices-earnings-and-cashflows-ai)*.

## Always

- Distinguish **investing** (value, convergence) from **trading** (price, momentum).
- Be clear about uncertainty, and show distributions rather than point estimates.
- End with the questions the investor should answer for themselves, plus the sleep test.
