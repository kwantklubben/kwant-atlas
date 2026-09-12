---
title: "A.6.1 Capital Structure from Zero"
tags:
  - fundamentals-accounting
  - capital-structure-and-corporate-finance
  - intuition
  - debt-vs-equity
  - residual-claim
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (the accounting equation). No prior corporate-finance knowledge needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of capital structure with **no prior knowledge needed**. The objective is one idea: **financing is a question of who gets to claim the firm's cash - and equity is the claim that is paid last, only after everyone else is whole.** Learn to see every financing instrument as a *ranked claim on the same pie of future cash flows*, and the whole theory of capital structure becomes one thought: *how you slice the pie changes who bears the risk, not how much pie there is* - until taxes, distress, information, and agency start to matter.

Start with the dumbest question: *why does a firm have a "capital structure" at all?* Because the accounting equation forces it: assets = liabilities + equity. To own a productive asset you must fund it - with **debt** (a promise to pay interest and principal, with legal priority) or **equity** (a residual ownership claim). The *mix* of those two funding sources is the capital structure. The whole question of corporate finance is: **does that mix itself change the value of the pie, or only how the risk is shared?**

Three steps:

1. **Debt is a priority claim, equity is a residual claim.** A lender gets paid *first* from operating cash flow - interest before anything else - and in liquidation is entitled to its principal ahead of everyone else. Equity gets whatever is *left* after every creditor (and every preference) is paid. "Residual" is not a metaphor: it is the strict legal and economic ordering. This single fact explains why equity is riskier than debt, why it must offer a higher expected return, and why [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03 · Seniority]] is a whole page.

2. **Leverage magnifies shareholder returns - up *and* down.** If debt costs a fixed $r \cdot D$ before shareholders see anything, then for a given operating profit $X$, equity receives $X - rD$. Borrowing a large $D$ leaves a smaller equity base $S$ to absorb the *whole* swing in $X$. So equity return $\frac{X - rD}{S}$ swings wildly with $X$ when $D/S$ is large. Leverage does not create return - it *amplifies* the risk of the underlying business into a bigger equity upside and a bigger equity downside.

3. **"Leverage is good" is only half the story.** The tax deductibility of interest (the *tax shield*, worth $\tau D$) genuinely makes debt add value - but only because it transfers money from the tax authority to the claimants. In the frictionless world of [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]], leverage adds *zero* value; it only moves risk around. The moment you learn that, "leverage amplifies, it does not create" becomes the discipline that stops over-borrowing.

---

### 2. Mathematical Ground Truth & Derivations

**The two claims on the same pie.** Let $X$ be operating profit (EBIT), $r$ the interest rate on debt $D$, $S$ the market value of equity. Cash available to shareholders each period:

$$
\text{Equity cash flow} = X - rD, \qquad \text{Debt cash flow} = rD.
$$

Total to all claimants: $X$. Debt gets $rD$ regardless of how $X$ moves (a *priority* claim, until the firm cannot pay); equity gets the residual $X - rD$ (which can be negative - equity bears all the operating risk).

**Leverage as amplification.** Define the equity ratio $e = S/(S+D)$ (fraction of capital that is equity) and debt $D = K - S$ where $K = S + D$ is total capital. Return on equity:

$$
ROE = \frac{X - rD}{S} = \frac{X - r(K-S)}{S}.
$$

As $S \to 0$ (equity thin), the *entire* swing in $X$ is concentrated on a shrinking base: $\text{ROE}$ spreads wider and its downside goes negative. This is the direct mechanism behind the "financial leverage" term in the Penman decomposition ([[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|ROCE = RNOA + FLEV×(RNOA − NBC)]]): leverage adds to shareholder return **only while** the operating return exceeds the after-tax cost of debt.

**Why the residual claim is the riskiest.** Because equity is paid *last*, it absorbs every loss that creditors' priority does not shield them from. In formal priority: debt principal and interest rank above common equity; common equity is subordinate to *all* other claims (see the full ladder in [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03 · Debt, Equity & Seniority]]). Risk and required return are priced to match: $r_E > r$ for any levered firm (MM Proposition II makes this precise - [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]]).

---

### 3. Computational Implementation - leverage magnification, stdlib only

Runs on the standard library. A $1{,}000$ capital project can be funded with different debt/equity mixes; we compute shareholder return on equity in a *good* operating state (EBIT 300) and a *bad* state (EBIT 60), and watch the return spread widen - and the downside go negative - as leverage rises.





Read the spread: all-equity ranges 6–30%; at 80% debt it ranges **−2% to +118%**. The *same* operating business produces far wider - and negative - shareholder outcomes the more debt it carries. Leverage magnifies; it does not create.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating "leverage is good" as a rule.** The tax shield makes debt valuable, but leverage's amplification is symmetric - it makes losses worse too. The correct discipline is the spread condition (operating return vs. after-tax debt cost) from the [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|ROCE decomposition]], never a blanket "borrow more."
2. **Confusing "residual" with "whatever is left over in a good year."** Residual means *legally subordinate to every other claim*, in every state - including bankruptcy, where equity is routinely worth zero. The §3 bad-state negative ROE is the milder cousin of equity being wiped out.
3. **Forgetting that equity bears all operating risk.** Because debt's $rD$ is fixed, *all* of the volatility of $X$ lands on equity. A high-D/S firm's equity is not "more of the same business" - it is a levered option on the business, much riskier than the business itself.
4. **Treating the pie as fixed.** The whole frictionless theorem says the *pie* (firm value) is fixed and leverage only re-slices it. The moment a beginner thinks leverage *adds* to the pie, they have missed that value only appears through the four real frictions (tax, distress, information, agency) of [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06 · Advanced Extensions]].

---

### 5. References

- **Modigliani & Miller**, "The Cost of Capital, Corporation Finance and the Theory of Investment" (*AER*, 1958)
- **Brealey, Myers & Allen**, *Principles of Corporate Finance*
- **Damodaran**, *Applied Corporate Finance*
- **Graham & Dodd**, *Security Analysis* (6th ed.)

---

### 6. Connected Graph Bridges

- Base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios - Liquidity & Leverage]]
- Continue: [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Index Hub]]
