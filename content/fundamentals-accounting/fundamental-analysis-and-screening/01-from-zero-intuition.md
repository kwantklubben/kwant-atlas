---
title: "01 — Fundamental Analysis & Screening from Zero: Intuition & the Why"
tags:
  - fundamentals-accounting
  - fundamental-analysis-and-screening
  - intuition
  - value-investing
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (a P/E and a current ratio, nothing more). No prior screening knowledge needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of fundamental investing with **no prior knowledge needed**. The objective is a single chain of reasoning: **a stock is a piece of a business; a business has an intrinsic value; the market price is not that value; and the gap between price and value is where money is made or lost.**

Start with the dumbest question: *what does owning a stock actually mean?* It means you own a fraction of a real company — its factories, its customers, its earnings. If the company earns money, you eventually get some of it. So a stock is not a lottery ticket; it is a claim on a business. That sounds trivially obvious and it is *the entire discipline*. Everything else is method.

Three steps, three "aha"s:

1. **Price and value are two different things.** The market quotes a **price** every second; that price moves on fear, fashion, and flows. The **value** of the business moves on earnings, assets, and prospects. Benjamin Graham personified the price as "Mr. Market," a manic-depressive business partner who offers to buy or sell at a different price every day — and whom you are free to ignore. When Mr. Market's price is *below* your estimate of value, you buy; when it is *above*, you sell or wait. His mood is an opportunity, not an instruction.

2. **The margin of safety is the whole game.** You will be wrong sometimes. Graham's answer is not to be right more often — it is to **buy cheap enough that being wrong doesn't ruin you**. If a business is worth roughly \$40 a share and you buy at \$60, you need everything to go right; buy at \$27 and you can be substantially wrong and still not lose money. The gap is the **margin of safety**, and it is the single most important idea in this entire folder. The Graham Number you will compute below is one concrete expression of it.

3. **Screening is how you make the search possible.** There are thousands of listed companies. You cannot read every annual report. So you **screen**: apply a few mechanical filters (cheap enough, safe enough, stable enough) to shrink the universe to a handful of names, *then* do the human work of reading their filings. The screen is not the analysis — it is the *triage* that tells you where to spend your reading time. (This is the workflow that [[fundamentals-accounting/fundamental-analysis-and-screening/04-the-research-workflow|04 · The Research Workflow]] makes concrete.)

---

### 2. Mathematical Ground Truth & Derivations

**Value from a price and an earnings stream — the two ratios that started it all.** The two cheapest definitions of "am I paying too much?" are:

$$\text{P/E} = \frac{P}{EPS}, \qquad \text{P/B} = \frac{P}{BVPS},$$

where $P$ is the price, $EPS$ earnings per share, and $BVPS$ book value (net assets) per share. A P/E of 10 means you pay \$10 for every \$1 of annual earnings — a rough "payback period" of ten years. A P/B of 1 means you pay \$1 for every \$1 of accounting net worth.

**Graham's two price ceilings, combined.** Graham's defensive rule caps the multiple of earnings at 15 and the multiple of book at 1.5. Multiply the two inequalities and a single price ceiling falls out:

$$\frac{P}{EPS} \le 15 \quad\text{and}\quad \frac{P}{BVPS} \le 1.5 \quad\Longrightarrow\quad P^2 \le 22.5 \cdot EPS \cdot BVPS,$$

so the highest price consistent with *both* caps — the **Graham Number** — is

$$\boxed{\,P_{\max} = \sqrt{22.5 \cdot EPS \cdot BVPS}\,}.$$

This is the mathematical heart of the page: a price ceiling derived from *two independent* fundamental anchors, so that a stock is not "cheap on earnings but expensive on assets" — it must satisfy both.

**Margin of safety.** If $\hat{V}$ is your estimate of value (here, the Graham Number), require buying only at a discount:

$$\text{buy if } P \le (1 - m)\,\hat{V}, \qquad m \in [20\%, 40\%].$$

Graham's aggressive version is buying at two-thirds of value — sometimes stated as requiring value $\ge 1.5 \times$ price.

---

### 3. Computational Implementation — price vs. value for one company, from zero

Runs on the **standard library only**. It takes one company (Alpha Machine Works: 3-yr average EPS \$2.60, book value per share \$22.00, price \$30.00) and computes the value ceiling, the margin of safety, and the buy/watch verdict — the whole discipline in eight lines.

```python
# The Graham Number and the margin of safety, from zero.
import math
eps, bvps, price = 2.60, 22.00, 30.00          # Alpha Machine Works
graham_number = math.sqrt(22.5 * eps * bvps)   # P^2 = 22.5*EPS*BVPS
mos = (graham_number - price) / graham_number  # discount to the value ceiling
print(f"Graham Number = sqrt(22.5*{eps}*{bvps}) = {graham_number:.2f}")
print(f"Price = {price:.2f}  ->  Margin of safety = {mos*100:.1f}%")
print(f"Buy rule (value >= 1.5x price): {'BUY' if graham_number >= 1.5*price else 'watch'}")
```
```
Graham Number = sqrt(22.5*2.6*22.0) = 35.87
Price = 30.00  ->  Margin of safety = 16.4%
Buy rule (value >= 1.5x price): watch
```

Read the output as a decision, not a calculation: at \$30 the stock trades at a **16.4% discount** to its Graham Number — a *positive* but *thin* margin of safety. Under Graham's aggressive "buy at two-thirds" rule the verdict is **watch**, not buy. That gap between "cheap-ish" and "cheap enough" is the discipline: the number does not tell you the stock is bad, it tells you the cushion is too small to protect you if you are wrong. (The same logic, extended across a universe, is the screen in the [[fundamentals-accounting/fundamental-analysis-and-screening/index|hub]] and the richer metrics in [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]].)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing cheap with good.** A low P/E can mean "the market hasn't noticed" *or* "the market has correctly noticed the business is dying." The Graham Number cannot tell you which — only the business reading can. This is the value trap, and it is the whole thesis of [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes]].
2. **Book value is an accounting number, not a floor.** On a modern firm whose assets are intangible (software, brands, people), $BVPS$ understates true net worth; on a declining manufacturer with obsolete plant, it *overstates* it. The Graham Number inherits every weakness of the book value that feeds it.
3. **A margin of safety on the wrong value estimate is no safety at all.** If your $\hat{V}$ is anchored to a growth assumption that is too optimistic, a "30% discount" is a discount to a fantasy. The margin of safety is only as real as the value estimate under it — which is why the estimate must be grounded in the actual filings.

---

### 5. Canonical Literature & Study References

- **Graham, Benjamin**: *The Intelligent Investor* (rev. 1973; HarperBusiness annotated 4th ed. 2003) — Ch 8 ("Mr. Market") and Ch 20 ("Margin of Safety") are the direct sources of this page. *Concepts and the \$15 / 1.5× caps verified against the corpus text.*
- **Graham, Benjamin & Dodd, David**: *Security Analysis* (McGraw-Hill, 6th ed. 2008) — the deeper origin of earnings power, asset-value floors, and the margin-of-safety principle.
- **Greenwald, Kahn, Sonkin & van Biema**: *Value Investing: From Graham to Buffett and Beyond* (Wiley, 2001) — the modern formalization of "value" as three distinct estimates (asset, earnings power, franchise) rather than one number.
- **Dorsey, Pat (Morningstar)**: *The Five Rules for Successful Stock Investing* (2004) — the plain-English on-ramp to how a professional turns "is it cheap?" into "is it a good business at a fair price?"

---

### 6. Connected Graph Bridges

- Base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]]
- Continue: [[fundamentals-accounting/fundamental-analysis-and-screening/02-graham-criteria-and-value-investing|02 · Graham Criteria & Value Investing]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Index Hub]]
- Value anchor: [[fundamentals-accounting/equity-valuation/index|Equity Valuation — DCF, Comps & Value Logic]] (where $\hat{V}$ becomes a full model)
