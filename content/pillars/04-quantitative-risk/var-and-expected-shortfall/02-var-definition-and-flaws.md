---
title: "02 — Value at Risk: Definition, Geometry & the Subadditivity Flaw"
tags:
  - pillar-quantitative-risk
  - var-and-expected-shortfall
  - value-at-risk
  - subadditivity
  - quantile
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/01-from-zero-intuition|01 · From Zero]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Value at Risk is the most-used and most-misused risk number in finance. This page gives its **exact definition** (including the quantile subtleties Artzner is careful about), then isolates the precise defect that motivated two decades of reform: **VaR is not subadditive, and its acceptance set is not convex.** The practical objective is to know *exactly* when a VaR limit is safe to use and when it will be gamed by the portfolio it is supposed to police.

The fault is not estimation sloppiness — it is structural. VaR is a *quantile*, and quantiles of sums do not respect quantiles of parts. Everything downstream (capital allocation, desk limits, decentralised risk governance) inherits the flaw.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Definitions (Artzner §3.3; Hull §22.1)

For a loss $L=-\Delta V$ over a horizon and confidence $\alpha\in(0,1)$:

$$\mathrm{VaR}_\alpha(L)=\inf\{l\in\mathbb{R}:\mathbb{P}(L>l)\le 1-\alpha\}=F_L^{-1}(\alpha).$$

Artzner's net-worth form makes the *capital* interpretation explicit: for a future net worth $X$ and reference return $r$ (usually $r=1$ over a short horizon),

$$\mathrm{VaR}_\alpha(X)=-\inf\{x\in\mathbb{R}:\mathbb{P}(X\le x\,r)>\alpha\}.$$

**The quantile trap (Artzner Def. 3.2).** Define the left/right quantiles $q^-_\alpha=\inf\{x:\mathbb{P}(X\le x)\ge\alpha\}$ and $q^+_\alpha=\inf\{x:\mathbb{P}(X\le x)>\alpha\}$. These differ on at most countably many $\alpha$ (where the CDF has a flat spot or a jump). VaR is pinned to $q^+_\alpha$. With **discrete** loss distributions (defaults, options, integer positions) the flat spots are common, and the choice of $q^-$ vs $q^+$ changes the number — a real reconciliation headache between desks.

#### 2.2 The subadditivity counterexample (Artzner §3.3)

Artzner's own example: two digital options on a stock with the same expiry. $A$ pays $1000$ if $S_T>U$; $B$ pays $1000$ if $S_T<L$ (with $L<U$). Choose $L,U$ so $\mathbb{P}(S_T<L)=\mathbb{P}(S_T>U)=0.008$. A trader **writes** two $A$'s and two $B$'s.

- Writing $2A$ alone: the $1\%$ VaR of the net worth is $-2u$ (essentially the premium — the $1.6\%$ chance of a $2000$ payout sits *inside* the $1\%$ quantile only if it is the adverse tail; the point is the isolated positions look cheap).
- Writing $A+B$ together: now the union of the two tail events has probability $0.016$, and the $1\%$ VaR jumps to the positive number $1000-l-u$.

The consequence Artzner stresses: **the set of acceptable net worths is not convex** — "an even worse feature than the non-subadditivity of the measurement." A non-convex acceptance set means the risk measure can have **multiple local minima as a function of portfolio weights**, so a VaR-constrained optimiser can be trapped away from the true safe portfolio (Rockafellar–Uryasev make the same point: VaR "can exhibit multiple local extrema").

#### 2.3 When does VaR *look* subadditive? (Artzner §3.3, Remark 1)

If all prices are **jointly normal** and exceedance probabilities are below $0.5$, then
$$\mathrm{VaR}_\alpha(X)=-\big(\mathbb{E}_P[X]+\Phi^{-1}(\alpha)\sigma_P(X)\big),$$
and $\sigma_{X+Y}\le\sigma_X+\sigma_Y$ (standard deviation is subadditive) so VaR *is* subadditive. **This is a trap**: it makes VaR look fine in Gaussian textbooks, while the failure appears precisely in the fat-tailed, discrete, and option-heavy portfolios that dominate real books. (Rockafellar–Uryasev: "VaR is coherent only when it is based on the standard deviation of normal distributions.")

#### 2.4 Two more first-principles failures (Artzner §3.3)

- **Concentration blindness (credit).** With zero base rate, $2\%$ bond spreads, $1\%$ independent default probability, the $5\%$ VaR of a $\$1$m single-name position is $-\$20{,}000$ (apparently riskless). Spreading across $100$ names makes $\mathbb{P}(\ge2\text{ defaults})>0.18$, so the same money has a $>5\%$ chance of negative net worth: **diversification increased the VaR.** Meanwhile the pile-up in one name went undetected.
- **Bad risk allocation.** VaR can prefer a Pareto-dominated allocation of risks across two agents (Artzner's $3$-state example): a capital level "found sufficient" for $X$ is "more than sufficient" after a risk exchange that all risk-averse agents dislike — VaR does not encourage sensible risk sharing.

---

### 3. Computational Implementation — the counterexample, exactly and by Monte Carlo

Exact pmfs (no simulation noise), plus a Monte Carlo confirmation. Stdlib only.

```python
import math, random

def var_pmf(pmf, a):
    cum = 0.0
    for l in sorted(pmf):
        cum += pmf[l]
        if cum >= a - 1e-12: return l
    return max(pmf)
def es_pmf(pmf, a):
    cum = 0.0; tot = 0.0
    for l in sorted(pmf):
        hi = cum + pmf[l]; lo = max(cum, a)
        if hi > lo: tot += l*(hi-lo)
        cum = hi
    return tot/(1.0-a)
def conv(d1, d2):
    o = {}
    for x, px in d1.items():
        for y, py in d2.items(): o[x+y] = o.get(x+y, 0.0) + px*py
    return o

A = {0.0: 0.96, 100.0: 0.04}          # each bond: 4% chance to lose 100
AB = conv(A, A); a = 0.95
print(f"P(single loss>0)               = {0.04:.2f}   VaR_95(A)  = {var_pmf(A, a):.1f}")
print(f"P(at least one of two defaults)= {1-0.96**2:.4f}  VaR_95(A+B)= {var_pmf(AB, a):.1f}")
print(f"VaR: VaR(A)+VaR(B)={var_pmf(A,a)+var_pmf(A,a):.1f}  but VaR(A+B)={var_pmf(AB,a):.1f}  -> SUBADDITIVITY FAILS")
print(f"ES : ES(A)+ES(B) ={es_pmf(A,a)*2:.2f}  vs ES(A+B)={es_pmf(AB,a):.2f}  -> coherent")

random.seed(5); ns = 200000; L = []
for _ in range(ns):
    L.append(100.0*sum(1 for _ in range(2) if random.random() < 0.04))
L.sort(); v = L[min(ns-1, int(0.95*ns))]; k = max(1, int(0.05*ns))
print(f"MC n=2: VaR_95={v:.1f}  ES_95={sum(L[-k:])/k:.2f}")
```
```
P(single loss>0)               = 0.04   VaR_95(A)  = 0.0
P(at least one of two defaults)= 0.0784  VaR_95(A+B)= 100.0
VaR: VaR(A)+VaR(B)=0.0  but VaR(A+B)=100.0  -> SUBADDITIVITY FAILS
ES : ES(A)+ES(B) =160.00  vs ES(A+B)=103.20  -> coherent
MC n=2: VaR_95=100.0  ES_95=103.23
```

The exact and Monte Carlo numbers agree; the Monte Carlo path also shows the estimator noise that any production VaR carries (see [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Subadditivity violation → aggregation failure.** Risk cannot be *decentralised*: a supervisor cannot split one cash limit $m=m_1+m_2$ across two desks and trust that $\rho(X_1)+\rho(X_2)$ covers $\rho(X_1+X_2)$ (Artzner's Axiom S motivation). With VaR the split can under-reserve the firm.
2. **Non-convex acceptance set → non-convex optimisation.** VaR-constrained portfolio optimisation has multiple local minima; solvers return arbitrary local optima. Rockafellar–Uryasev's fix: optimise the *convex* $F_\alpha$ and read VaR off as a by-product ($\S 3.3$ of this hub, and [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|04 · ES]]).
3. **Gaussian complacency.** Because VaR *is* subadditive under normality, back-tests on normal data pass while the real (fat-tailed) book fails silently. Always stress VaR on discrete/jump/option payoffs.
4. **Quantile-edge ambiguity.** $q^-_\alpha\neq q^+_\alpha$ on discrete books; two desks reporting "the same" VaR can differ by a full position. Fix the convention ($q^+_\alpha$ per Artzner) in the risk policy.
5. **Tail blindness.** The single quantile is insensitive to the *size* of the worst outcomes — demonstrated numerically in [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Artzner, Delbaen, Eber & Heath**, *Coherent Measures of Risk* (1999) — Def. 2.4 (coherence), Def. 3.2–3.3 (quantiles, VaR), §3.3 (digital-option counterexample, normal-subadditivity remark, concentration and allocation failures). *Primary source, read from the corpus PDF.*
- **Rockafellar & Uryasev**, *Optimization of Conditional Value-at-Risk*, *J. Risk* 2(3):21–41 (2000) — VaR's lack of convexity and multiple local extrema (citing Mauser–Rosen, McKay–Keefer).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 (VaR mechanisms, backtesting) and *Risk Management and Financial Institutions*, Ch 11–13.
- **Jorion, P.**, *Value at Risk: The New Benchmark for Managing Financial Risk*, 3rd ed. (2006) — the practitioner standard for VaR implementation.
- **Kupiec, P.**, *Techniques for Verifying the Accuracy of Risk Measurement Models*, *J. Derivatives* 3(2) (1995) — the backtest that grades a VaR model.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/var-and-expected-shortfall/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|03 · Coherent Risk Measures]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|04 · Expected Shortfall]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model|Credit Risk & the Merton Model]]
