---
name: dam-story
description: damostack narrative builder: a valuable business story, the 3P test, a bottom-up TAM, and the story mapped to value drivers. Triggers: "build my company's story", "is our TAM realistic", "story check".
---

# /dam-story — a story you can value

Valuation is a bridge between stories and numbers *(2014/06/numbers-and-narrative-modeling-story)*.
A founder's pitch is a story. This skill makes it a story with numbers attached that will hold up
in front of skeptics.

## 0. Load

Read `~/.claude/skills/damostack/knowledge/core.md` (short; replaces reading voice.md and principles.md in full), then run
`~/.claude/skills/damostack/bin/kb frameworks V1 V7 V9`.
For depth, WebFetch `https://aswathdamodaran.blogspot.com/2014/07/possible-plausible-and-probable-big.html`.

## 1. Draft the story (ask one question at a time; skip what's known)

1. *What does the business do, for whom, and how does it make money (the unit of sale and its price)?*
2. *What market are you in? Define it narrowly and broadly.* Market definition changes value.
   Uber as car service or as logistics roughly triples the market *(2014/06/a-disruptive-cab-ride-to-riches-uber)*.
3. *Why do you win? What's the edge, and will it last (a moat)?*
4. *What does one more unit cost you to deliver? What are your fixed costs?* (unit economics,
   economies of scale)
5. *How much capital does growth need?* (capital intensity → sales-to-capital)
6. *What could kill it?* (competition, regulation, key person, funding)

Then write it as a **one-paragraph story**, in plain language.

## 2. Market size, bottom-up  *(2026/08/ais-bar-mitzvah-moment-from-hype-hope, 2019/12/the-market-is-huge-revisiting-big)*

- Replace any top-down TAM with a **bottom-up build**: the number of buyers × spend per buyer, or
  the spending the product replaces. Make every filter explicit (who, where, what share of spend).
- Separate **today's market** from the **year-10 market** and say why it grows.
- **Big market delusion check**: who else is chasing this market, and does the sum of everyone's
  implied market share exceed 100%?

## 3. The 3P test

| Claim in the story | Possible? | Plausible? (evidence) | Probable? (goes in the numbers) |
|---|---|---|---|

Possible-only claims become optionality, not base-case inputs (expansion options, as with SpaceX's
"other businesses" line *(2026/04/to-trillion-dollars-and-beyond-spacex)*).

## 4. Scale vs profit archetype  *(V7; 2026/09/the-scaling-and-profitability-trade-off)*

Score the scalability factors and business-building factors, then name the archetype:
lightning in a bottle, field of dreams, field of nightmares, niche star, big and broken, small
winner, small loser, or cut your losses. Say what it implies for the strategy: scale fast, scale
carefully, stay niche, fix unit economics first, or stop.

## 5. Story → value drivers

Fill the V1 mapping table: growth, target margin, years to converge, sales-to-capital, cost of
capital, failure probability, and terminal ROIC. Each value gets a one-line reason from the story.
Offer to run `/dam-value` (or `/dam-startup` for private companies) on these drivers.

## 6. Make it robust

- **The strongest counter-story**: the most credible skeptic's version, and which driver it changes.
- **What evidence would move it**: milestones that would turn plausible into probable (or break it).
- **For a pitch**: lead with the story, show the drivers, and show you've thought about the
  counter-story. That beats TAM theater with sophisticated investors.

Save it to `~/.damostack/valuations/<slug>/story.md`.
