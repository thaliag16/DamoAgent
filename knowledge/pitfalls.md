# Pitfalls — the "dark side" checklist for reviewing any valuation, pitch, or deal

Use this when reviewing someone else's DCF, an analyst report, a banker's fairness opinion,
a startup pitch deck, or your own work. Each item has a **check** and a **fix**. Report the
three to five that matter most, not all of them.

## Consistency errors (the most common)

| Pitfall | Check | Fix |
|---|---|---|
| **Currency mismatch** | Cash flows in one currency, discount rate in another (e.g. local-currency cash flows with a USD cost of capital) | Convert the discount rate using the inflation differential |
| **Inflation mismatch** | Nominal cash flows with a real discount rate, or the reverse | Make both nominal or both real |
| **Cash flow / discount rate mismatch** | FCFF discounted at the cost of equity, or FCFE at the WACC | FCFF ↔ cost of capital; FCFE ↔ cost of equity |
| **Growth without reinvestment** | High growth but cap ex ≈ depreciation and no working capital | Reinvestment = Δrevenue / sales-to-capital; check the implied ROIC |
| **Terminal growth > riskfree** | g of 4–6% forever in a ~4–5% riskfree world | Cap at the riskfree rate |
| **Terminal value from a multiple** | Exit EV/EBITDA plugged in as the terminal value | That's a pricing inside a DCF; use stable-growth FCFF |
| **Terminal reinvestment missing** | Terminal FCFF = NOPAT (no reinvestment) with g > 0 | Reinvestment rate = g / ROIC |
| **Moat forever** | Terminal ROIC far above the cost of capital, with no story to back it | Fade excess returns, or justify the moat |
| **Equity bridge errors** | Cash or debt ignored; lease debt missing; minority interests or cross-holdings mishandled | Apply the full bridge |
| **Share-count tricks** | Basic share count; options, RSUs, or convertibles ignored | Use diluted shares, and value options separately |
| **SBC added back** | EBITDA or FCF "adjusted" by adding back stock-based compensation | SBC is a real expense; don't add it back |

## Risk and discount-rate errors

| Pitfall | Check | Fix |
|---|---|---|
| **Historical ERP / stale ERP** | ERP of 5.5–6% from historical averages, or one from a year ago | Use the current implied ERP |
| **Country of incorporation, not operation** | CRP based on HQ location | Weight CRP by revenue or operations |
| **Regression beta for one company** | Beta from 2 years of weekly returns | Bottom-up industry beta |
| **Padding the discount rate for failure** | 25–60% "VC" discount rates inside a DCF | Use a cost of capital plus a separate failure probability |
| **Book-value weights** | D/(D+E) from book values | Market values |
| **Effective vs marginal tax** | Effective tax used to compute the after-tax cost of debt | Marginal tax for debt; effective converging to marginal for operations |
| **Implausible cost of capital** | Below the 10th or above the 90th percentile with no reason | Check against the distribution |

## Story errors

| Pitfall | Check | Fix |
|---|---|---|
| **TAM hallucination** | Top-down TAM in the trillions, with no bottom-up build | Build the market from spending it replaces; implied share in year 10 |
| **Big market delusion** | Every competitor priced to win the same market | Sum the implied market shares across peers |
| **ARR as revenue** | Run-rate annualized from a peak week or month | Use trailing revenue; treat ARR as a claim |
| **Story-number disconnect** | The story says "niche luxury" but the numbers say mass-market growth (or the reverse) | Every input must trace to the story |
| **Runaway story** | No falsifiable milestones; pushback is dismissed | Define what evidence would break the story |
| **Ignoring competition** | Margins rise to best-in-class while ten rivals chase the same customers | Industry structure sets how many can win |
| **Synergy fairy tales** | Revenue synergies are the bulk of a deal's value; there's no integration plan | Value synergy explicitly, with timing and cost; haircut it |
| **Accretion = value** | "The deal is accretive to EPS" | EPS accretion says nothing about value |
| **Life-cycle mismatch** | Mature or declining firm valued with high growth; young firm valued on current earnings | Value the stage |

## Process and bias errors

| Pitfall | Check | Fix |
|---|---|---|
| **Backing into the price** | Inputs tweaked until value ≈ deal price (common in fairness opinions) | Value first, then compare with the price |
| **Precision theater** | Values to the cent, 50-tab models | Fewer inputs; show the distribution |
| **No sensitivity or distribution** | A single point estimate | Sensitivity grid and Monte Carlo |
| **Pricing called valuation** | "Valued at 15× forward revenue" | Call it a pricing, and ask what the multiple implies |
| **Market call disguised as stock call** | Every stock looks cheap (or rich) | Check whether the ERP is the market's |
| **Confirmation bias** | Only bullish (or bearish) evidence cited | List the strongest counter-story |
