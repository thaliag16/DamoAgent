---
name: dam-coc
description: damostack discount-rate builder: riskfree rate, implied ERP, country risk, bottom-up beta, synthetic rating, plausibility checks. Triggers: "WACC for X", "hurdle rate", "cost of equity", "country risk premium".
---

# /dam-coc — the discount rate, without the agonizing

Don't overthink it. 80% of US companies have costs of capital in a band about 4.5 points wide.
Get it reasonable and consistent, then spend your time on the cash flows
*(2026/02/data-update-5-for-2026-risk-and-hurdle)*.

## 0. Load

Read `~/.claude/skills/damostack/knowledge/core.md` (short; replaces reading voice.md and principles.md in full), then run
`~/.claude/skills/damostack/bin/kb frameworks V3` and `~/.claude/skills/damostack/bin/kb market-data`.
Refresh the market inputs: `adsearch.py --recent 3` (latest ERP and riskfree) and `addata.py ctryprem <country>`.

## 1. Ask (briefly)

The company or project, its **currency**, its **industry**, **where its revenues come from** (by
country or region), its **debt** (amount, interest expense, rating if any), its **market cap**,
and whether the owners are **diversified** (public investors) or not (founders, a family).

## 2. Build it, showing every step

1. **Riskfree rate in the currency**: the government bond rate minus the sovereign default spread.
   For USD, that's the 10y Treasury less the US Aa1 spread (5.07% on 1 Oct 2026). For other
   currencies, either use the local bond rate less its default spread, or (1 + USD rf) × (1 + local
   inflation) / (1 + US inflation) − 1.
2. **ERP**: the current implied mature-market ERP, plus country risk premiums weighted by revenue
   exposure (`addata.py ctryprem <country>` for each).
3. **Beta**: industry unlevered beta (`addata.py betas "<industry>"`), relevered:
   `adcalc.py lever --unlevered-beta <bu> --de <D/E> --tax <marginal>`. For multi-business firms,
   use a revenue- or value-weighted average of the businesses. For undiversified owners, use total
   beta (`addata.py totalbeta`).
4. **Cost of debt**: `adcalc.py rating --coverage <EBIT/interest> --size large|small`, then
   riskfree + spread (+ a country default spread if the borrowing is local), after tax at the
   marginal rate.
5. **Put it together**:
   `adcalc.py coc --riskfree <rf> --unlevered-beta <bu> --de <D/E> --erp <erp> --crp <weighted crp> --coverage <cov> --tax <t>`
6. **Check it**: compare with `addata.py wacc "<industry>"` (January data; adjust for rate changes
   since) and with the distribution (US 5.26–9.88%, global 6.28–11.66%, Jan 2026).
7. **Over time**: for a young firm, give an initial rate and a mature rate (≈ the median company),
   with the path between them.

## 3. Output

A table with each component, its source, and its as-of date, then the result, a plausibility note,
and the mature rate. For a **project**, use the project's risk (its industry and country), not the
company's. The cost of capital is an opportunity cost.

## 4. Common mistakes to flag

A historical ERP; a regression beta for one firm; country risk based on headquarters; book-value
weights; an effective tax rate applied to debt; failure risk padded into the discount rate; and
currency mismatches *(pitfalls.md)*.
