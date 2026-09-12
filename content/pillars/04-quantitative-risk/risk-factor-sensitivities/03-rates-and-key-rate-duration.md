---
title: "4.11.3 Rates and Key-Rate Duration"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - interest-rate-risk
  - dv01
  - key-rate-duration
  - convexity
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/risk-factor-sensitivities/01-from-zero-intuition|01 · From Zero]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]].

---

### 1. Intuition & Practical Objective

Interest-rate risk is the largest sensitivity exposure in the financial system, and it is the one where the *choice of risk factor* matters most. A bond does not trade off "the interest rate" - there is no such thing. There is a **curve**: a rate for every maturity. The job here is to replace one useless scalar with a **ladder of exposures**, then show that the ladder is not optional.

Three levels of resolution, in increasing honesty:

1. **DV01 (dollar value of a basis point).** The money lost if *the whole curve* moves up by one basis point: $\text{DV01}=-\partial V/\partial y\times10^{-4}$. One number. Useful, and blind to shape.
2. **Modified duration and convexity.** DV01 restated as a relative measure ($D_{\text{mod}}=\text{DV01}/V\times10^4$) plus the second-order term that makes duration wrong for large moves.
3. **Key-rate durations (KRDs).** The sensitivity to *each curve node separately*: $KRD_i=-\partial V/\partial y_i\times10^{-4}$. This is the **risk-factor map** for rates, and it is what a swap desk actually hedges, node by node, with a portfolio of instruments chosen to reproduce the ladder.

> **The essential property.** A parallel shift of the curve is *one* scenario; the curve moving in every other way is *infinitely many*. Duration hedges the first and only the first. The KRD ladder is the minimal representation that lets you hedge the others.

---

### 2. Mathematical Ground Truth & Derivations

**Price, duration, convexity.** For a set of cash flows $C_i$ at times $t_i$ discounted at zero rates $y_i$,

$$
V=\sum_i C_i(1+y_i)^{-t_i},\qquad
D_{\text{mod}}=-\frac{1}{V}\frac{\partial V}{\partial y}=\frac{1}{V}\sum_i t_i\,C_i(1+y_i)^{-t_i-1},\qquad
\mathcal{C}=\frac{1}{V}\frac{\partial^2V}{\partial y^2}.
$$

For a **parallel shift** $\Delta y$, the second-order expansion is

$$
\Delta V\approx -\underbrace{D_{\text{mod}}V\,\Delta y}_{\text{DV01}\times\Delta y\text{ in basis points}}+\underbrace{\tfrac12\mathcal{C}V(\Delta y)^2}_{\text{convexity correction}} .
$$

Convexity is **always favourable to a long bond position**: the price rises more than duration predicts on a rally and falls less than duration predicts on a selloff. That asymmetry is a real, priced asset - and it is exactly the second-order sensitivity term this folder keeps returning to.

**Key-rate durations (the canonical definitions).** Let the curve be parameterised by node rates $y_1,\dots,y_n$ (zero rates, or par swap rates - the choice is a convention, but *fixed before* the ladder is computed). Then

$$
KRD_i=-\frac{\partial V}{\partial y_i}\times10^{-4}\approx-\frac{V(y_i+h)-V(y_i-h)}{2}\quad(\text{per }1\text{bp},\ h=10^{-4}),\qquad
\sum_i KRD_i=\text{DV01}_{\text{parallel}} .
$$

The **summation identity** is the fundamental consistency check of any rate-risk system: *the key-rate ladder must sum to the parallel DV01.* When it does not, the curve interpolation or the bump convention is inconsistent with the parallel-shift convention.

**Portfolio aggregation.** Because the ladder is a vector, books aggregate **node by node**:

$$
KRD^{\text{book}}_i=\sum_{\text{desks}} KRD_i^{\text{desk}} .
$$

Two desks can each have large DV01 and cancel exactly in the ladder - the classic "matched book" - while their *convexities* add rather than cancel. That mismatch is the origin of the "convexity book" and of the P&L that appears when the curve does not move in parallel (see also [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/03-scenario-construction|03 · Scenario Construction]] for twist/bowing scenarios).

**Other rate risk factors, for completeness:** *swap-spread* and *basis* sensitivities (spread of a curve to a benchmark), *inflation* sensitivities (real vs nominal nodes), and *FX* sensitivity for a foreign-currency curve. Each is another node in the exposure vector.

---

### 3. Computational Implementation - DV01, convexity, and the KRD ladder of a two-bond book

We price two coupon bonds off a flat $4\%$ zero curve, compute modified duration/DV01/convexity, build the full key-rate ladder, verify the summation identity, and then show how far duration alone gets you on a real parallel shift. Stdlib only.




**Three things to read off.**

1. **The ladder is the risk.** The book's DV01 is $0.130916$, but it is *not* spread evenly: the 5-year bond's final coupon/principal node carries $0.043467$ ($33\%$ of the total) and the 10-year's carries $0.068206$ ($52\%$). The **intermediate nodes carry almost nothing** ($\approx0.003$ each). A parallel-shift hedge is therefore a poor hedge against almost any actual curve move - the classic pain trade of a coupon-bond book.
2. **The summation identity holds to machine precision** ($\text{diff}=1.42\times10^{-14}$). This is the check that a risk system's curve parameterisation and its bump are mutually consistent.
3. **Convexity is a real correction, not trivia.** On a $+100$bp parallel move, duration alone predicts $-13.09$ against an actual $-12.56$ - a $ $\$0.53 error on a \212.56 book ($+4.2\%$ of the loss). At $+200$bp the error is $ $\$2.05 (8.5\%$). The sign is favourable (long convexity cushions a selloff) and it is *symmetric* - the same convexity term helps on a rally, which is exactly what makes convexity a priced asset.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Hedging the parallel shift is not hedging the curve.** With a $33\%/52\%$ concentration at the 5y and 10y nodes, a parallel hedge leaves the book massively exposed to a steepening or flattening. You must hedge the **ladder**, or accept a curve-shape position explicitly.
2. **Duration is a first-order number; the loss is not.** Duration alone overstates a $+100$bp loss by $4.2\%$ here and $8.5\%$ at $+200$bp, and the miss grows roughly quadratically in the shock. **A duration-only risk system systematically mis-states large rate moves** - and it is the large moves that matter.
3. **The choice of nodes is a modelling decision that changes the answer.** Zero-rate nodes, par-swap nodes, and cash-flow buckets give different ladders that all "sum to DV01". A ladder is only comparable to another ladder if both use the same curve and bump convention.
4. **DV01 is linear, the book is not.** Two desks with offsetting DV01 still have *additive* convexity - the matched book earns or loses on curve moves beyond parallel, and the risk of that lives in the second-order term, invisible to every DV01 report.
5. **Interpolation risk.** Key-rate ladders are built on an interpolated curve; linear interpolation of zero rates and log-linear interpolation of discount factors produce different node sensitivities and, in the limit of coarse nodes, materially different hedges.

---

### 5. References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.)
- **Hull, John C.**: *Risk Management and Financial Institutions*
- **Alexander, Carol**: *Market Risk Analysis, Vol. III* (2008)
- **J.P. Morgan / RiskMetrics**: *Technical Document*, 4th ed. (1996)
- **BCBS**: *Minimum Capital Requirements for Market Risk* (2019, FRTB, d457)

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/risk-factor-sensitivities/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma, Vega]]
- Continue: [[pillars/04-quantitative-risk/risk-factor-sensitivities/04-factor-exposures|04 · Factor Exposures]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/03-scenario-construction|Scenario Construction (twist & bowing shocks)]]
- Regulatory application: [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation - FRTB sensitivities-based method]]
