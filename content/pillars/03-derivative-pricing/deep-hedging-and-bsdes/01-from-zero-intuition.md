---
title: "01 — Deep Hedging from Zero: Why Replication Fails When the Market Is Incomplete"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - intuition
  - incomplete-markets
  - hedging
  - replication
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (or none — this page is written to stand alone) and [[pillars/03-derivative-pricing/no-arbitrage-and-binomial|No-Arbitrage & the Binomial Model]].

---

### 1. Intuition & Practical Objective

Black–Scholes' hedge is an *equation*. You hold $\Delta=\partial C/\partial S$ shares, the stochastic parts cancel, and what is left is a riskless rate. Nothing is chosen; everything is determined. That is a consequence of a very strong structural assumption: **the number of independent traded instruments equals the number of independent sources of randomness**, i.e. the market is *complete*, and by the second Fundamental Theorem the martingale measure is unique.

Take that assumption away and the character of the problem changes completely:

| | complete market | incomplete market |
|---|---|---|
| price | unique, by no-arbitrage | a *range*; needs a preference to select one |
| hedge | determined ($\Delta=\partial C/\partial S$) | **chosen**: an optimisation over strategies |
| residual risk | zero (exactly) | strictly positive and *irreducible* |
| the object you compute | a number | a **strategy** + a **risk statistic** |

Deep hedging lives entirely in the right-hand column. The one idea of this page:

> **When the payoff is not spanned, no strategy makes the residual zero; the question is only *which residual you prefer* — and "which residual" is decided by a convex risk measure, not by no-arbitrage. Deep hedging is convex-risk-minimisation over strategies, with the strategy parametrised by a neural network.**

**Where incompleteness actually comes from** (all of it present in a real derivatives book):

1. **Discrete rebalancing.** Even in the pure Black–Scholes world, a hedge adjusted only at $n$ dates leaves a residual whose standard deviation scales as $\sqrt{\Delta t}$ (§05 quantifies it: $\mathrm{SD}\cdot\sqrt{n}\approx\mathrm{const}$).
2. **Transaction costs.** Cost is linear in turnover, so "rebalance more finely" buys a $\sqrt{\Delta t}$ reduction in dispersion and pays a cost that decays far more slowly. For large enough costs, continuous replication is *infinite-cost* — incompleteness in the strict limit.
3. **Jumps.** With random jump size there is **no replicating portfolio at all**: the jump risk is unspanned ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston/SABR · 06]] §2.1 restates Gatheral's "no replicating hedge" for SVJ).
4. **Extra risk factors you cannot trade.** Stochastic volatility, stochastic rates, a second index — each adds a dimension your instrument set does not span. This is the *pricing* incompleteness of [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr|Heston/SABR]].
5. **A thin instrument set.** Basis risk: you hedge an exotic with vanillas that do not span it.

The practical objective: understand that incompleteness converts a *pricing* problem into a *decision* problem, see the smallest possible example where the residual is genuinely non-zero, and see the same example become exactly replicable the moment a second instrument is added.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Replication as a linear system

Work in a one-period model: states $k=1,\dots,K$ with physical probabilities $p_k$, a traded stock with returns $\Delta S_k$ and a bond (cash). A payoff $H=(H_k)$ is **replicable** iff there exist $c$ (cash) and $\delta$ (shares) with

$$
H_k=c+\delta\,\Delta S_k\quad\text{for every }k=1,\dots,K .
$$

That is a linear system with **2 unknowns and $K$ equations**. If $K>2$ and the points $(\Delta S_k,H_k)$ are not collinear, the system is inconsistent: **no replicating portfolio exists**. Completeness, in this language, is the elementary statement

$$
\boxed{\ \#\text{independent instruments}\ \ge\ \#\text{states}\ }
$$

(equivalently: the matrix of instrument payoffs has full column rank $K$).

#### 2.2 What replaces it: a projection, not an equation

The classical substitute (Föllmer–Sondermann 1986; Schweizer 2001) is to project in $L^2$:

$$
\min_{c,\delta}\ \mathbb E\big[(H-c-\delta\,\Delta S)^2\big]
\quad\Longrightarrow\quad
\boxed{\ \delta^\star=\frac{\mathrm{Cov}(\Delta S,H)}{\mathrm{Var}(\Delta S)},\qquad c^\star=\mathbb E[H]-\delta^\star\mathbb E[\Delta S]\ }
$$

and the residual variance is the *unexplained* part, $\mathrm{Var}(H)-\mathrm{Cov}(\Delta S,H)^2/\mathrm{Var}(\Delta S)=\mathrm{Var}(H)(1-\rho^2_{H,\Delta S})$. The projection is exact **iff** $\rho^2=1$ — the collinearity condition of §2.1. So:

- **Complete market** ⇔ the $L^2$ projection has zero residual.
- **Incomplete market** ⇔ a strictly positive residual, and a *choice* of distance (quadratic? CVaR? entropic?) that decides which hedge you get.

#### 2.3 The general objective (Buehler–Gonon–Teichmann–Wood)

Multi-period, self-financing, zero rates, discretely rebalanced at $0=t_0<\dots<t_N=T$:

$$
L_T^{\delta}\;=\;\underbrace{p}_{\text{premium}}+\underbrace{\sum_{i=0}^{N-1}\delta_{t_i}\big(S_{t_{i+1}}-S_{t_i}\big)}_{\text{hedging gains}}\;-\;\underbrace{H}_{\text{liability}} .
$$

The deep-hedging problem is

$$
\boxed{\ \inf_{\delta\in\mathcal A}\ \rho\big(L_T^{\delta}\big)\ },\qquad \mathcal A=\{\delta:\ \delta\ \mathcal F_t\text{-adapted, admissible}\},\ \rho\ \text{convex, cash-additive, monotone}.
$$

Three structural remarks that make the whole field work:

- **Convexity.** $L_T^{\delta}$ is *affine* in $\delta$ and $\rho$ is *convex*, so the objective is convex in the strategy: there are no spurious local minima, and gradient descent is a legitimate solver. This is why deep hedging is a *learning* problem at all — the only obstacle is the parametrisation of an infinite-dimensional adapted process, not non-convexity of the economics.
- **Cash-additivity** $\rho(L+c)=\rho(L)+c$ makes $p$ a pure shift: the premium the desk charges is the level, and the *shape* of the hedge is the minimiser.
- **$\rho$ is a preference**, and different convex preferences give *different* hedges (§02 makes this concrete: variance-optimal $0.56$, CVaR-optimal $0.59$, entropic-optimal $0.66$ on the same data).

---

### 3. Computational Implementation — the smallest market where replication dies

A three-state one-period market, a short ATM call, and the $L^2$ projection computed exactly by weighted least squares. Nothing is simulated; every number is exact arithmetic on three states.

```python
import math

S0=100.0
states=[(80.0,0.25),(100.0,0.5),(120.0,0.25)]      # S_T and its probability
H=[max(s-S0,0.0) for s,_ in states]                # ATM call payoff
dS=[s-S0 for s,_ in states]; p=[w for _,w in states]

def wls(rows,rhs,w):                               # weighted least squares: min sum w*(rhs - X b)^2
    n=len(rows[0]); A=[[0.0]*n for _ in range(n)]; b=[0.0]*n
    for r,y,ww in zip(rows,rhs,w):
        for i in range(n):
            b[i]+=ww*r[i]*y
            for j in range(n): A[i][j]+=ww*r[i]*r[j]
    M=[A[i][:]+[b[i]] for i in range(n)]
    for c in range(n):
        q=max(range(c,n),key=lambda rr:abs(M[rr][c])); M[c],M[q]=M[q],M[c]
        for rr in range(c+1,n):
            f=M[rr][c]/M[c][c]
            for cc in range(c,n+1): M[rr][cc]-=f*M[c][cc]
    x=[0.0]*n
    for i in range(n-1,-1,-1): x[i]=(M[i][n]-sum(M[i][j]*x[j] for j in range(i+1,n)))/M[i][i]
    return x

print("1-period market, S_T in {80,100,120} with prob {1/4,1/2,1/4}; short an ATM call H=(S_T-100)^+.")
print("Q-optimal (variance-minimising) hedge:  minimise E[(H - c - delta*dS)^2]")
c1=wls([[1.0,d] for d in dS],H,p)
r1=[H[k]-c1[0]-c1[1]*dS[k] for k in range(3)]
print("  (a) tradeables = cash + stock      (2 instruments, 3 states -> INCOMPLETE)")
print(f"      cash={c1[0]:.4f}  delta={c1[1]:.4f}")
print(f"      residual by state = {[round(r,4) for r in r1]}   E[residual^2] = {sum(p[k]*r1[k]**2 for k in range(3)):.4f}")
print(f"      -> irreducible hedging error, SD = {math.sqrt(sum(p[k]*r1[k]**2 for k in range(3))):.4f}  (hedge is NOT a replication)")

Y=[max(s-90.0,0.0) for s,_ in states]              # a second option, strike 90
c2=wls([[1.0,d,Y[k]] for k,d in enumerate(dS)],H,p)
r2=[H[k]-c2[0]-c2[1]*dS[k]-c2[2]*Y[k] for k in range(3)]
print("  (b) add the K=90 call               (3 instruments, 3 states -> COMPLETE)")
print(f"      cash={c2[0]:.4f}  stock={c2[1]:.4f}  K90-call={c2[2]:.4f}")
print(f"      residual by state = {[round(r,12) for r in r2]}   E[residual^2] = {sum(p[k]*r2[k]**2 for k in range(3)):.2e}")
print("      -> exactly zero: with a complete set of instruments the hedge is a REPLICATION again.")
```
```
1-period market, S_T in {80,100,120} with prob {1/4,1/2,1/4}; short an ATM call H=(S_T-100)^+.
Q-optimal (variance-minimising) hedge:  minimise E[(H - c - delta*dS)^2]
  (a) tradeables = cash + stock      (2 instruments, 3 states -> INCOMPLETE)
      cash=5.0000  delta=0.5000
      residual by state = [5.0, -5.0, 5.0]   E[residual^2] = 25.0000
      -> irreducible hedging error, SD = 5.0000  (hedge is NOT a replication)
  (b) add the K=90 call               (3 instruments, 3 states -> COMPLETE)
      cash=-20.0000  stock=-1.0000  K90-call=2.0000
      residual by state = [0.0, 0.0, 0.0]   E[residual^2] = 0.00e+00
      -> exactly zero: with a complete set of instruments the hedge is a REPLICATION again.
```

**Reading the output.**

- **The residual is irreducible and it alternates in sign.** The $L^2$-optimal hedge buys $0.5$ shares for $5$ cash and leaves $+5,-5,+5$ in the three states — a *perfectly hedged* conditional mean with a *non-zero* residual everywhere except the middle state. No other $(\delta,c)$ does better in $L^2$: this is a genuine projection, and the error $25.0$ (SD $5.0$) is the *distance from the payoff to the span of the instruments*. It is not a numerical artifact and it does not shrink with a better optimiser.
- **The residual is exactly the "missing instrument" statement.** The payoff is a function of the same single source of randomness as the stock; what fails is not the randomness, it is the *dimension*: three states, two instruments.
- **Adding one option restores completeness exactly.** With cash, stock and the $K{=}90$ call, the solution is $c=-20,\ \delta=-1,\ \gamma=+2$ and the residual is identically $0$ — a *replication*, recovering precisely the Black–Scholes logic in a three-state world. The lesson is stark: **incompleteness is about the instrument set, not about the model's complexity.** Deep hedging is what you do when you cannot (or will not) add the missing instruments.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Deep hedging is a better delta hedge."** It is not a refinement of replication; it is a *different problem*. Replication targets residual zero; deep hedging targets a *risk measure*. In a complete market the two coincide (and deep hedging merely relearns Black–Scholes); in an incomplete market they give different strategies by construction (§02 shows the optimum moving from $0.56$ to $0.66$ purely by changing the risk measure).
2. **"More data / a bigger network closes the gap."** The residual is a *spanning* deficiency. The network can redistribute it optimally but cannot remove it. Confusing a capacity problem with a spanning problem is the single most common conceptual error.
3. **"The risk measure is a technical detail."** It is the *entire preference content* of the answer. Variance penalises both tails symmetrically; CVaR penalises one tail; entropic penalises all moments. A desk that does not state its risk measure has not stated its objective, and its "optimal" hedge is arbitrary.
4. **"Cash-additivity means the premium is irrelevant."** The premium is a *shift*, true — but the objective is stated on the hedged P&L, so the premium must be fixed *before* hedging; re-optimising it jointly with the strategy is unbounded when $\rho$ is not mean-centred (this is why one demeans the residual, or uses a mean-penalised measure — §02's objective is explicitly mean-demeaned).
5. **"If it reproduces Black–Scholes, it is validated."** Every deep-hedging implementation should reproduce the Black–Scholes hedge in the limiting complete-market case — that is a *necessary* unit test, but it exercises none of the machinery that matters (the regressor basis, the cost model, the risk measure, the training schedule). Passing it is the beginning of validation, not the end.
6. **"Admissibility is a formality."** The strategy set $\mathcal A$ in the objective is *not* cosmetic. Doubling strategies are admissible in some naive formulations and make the infimum $-\infty$ (or $0$ with an infinite P&L distribution); constraining leverage/position limits is part of the *definition* of the problem, not a numerical convenience. This is the same admissibility discipline as [[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|VaR/ES · 02]] on the risk side.

---

### 5. Canonical Literature & Study References

- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291 — the objective $\inf_\delta\rho(L_T^\delta)$, the convexity, the entropic/quadratic-BSDE equivalence, the robust representation of CVaR, and the neural-network solver. *The primary source for this folder.*
- **Föllmer, H. & Sondermann, D.** (1986), *Hedging of non-redundant contingent claims*, in Contributions to Mathematical Economics — the $L^2$ projection (variance-optimal hedge) used in §2.2. **Schweizer, M.** (2001), *A guided tour through quadratic hedging approaches* — the taxonomy (mean-variance, variance-optimal, local risk-minimisation). **Föllmer, H. & Leukert, P.** (2000), *Efficient hedging: cost versus shortfall risk*, Finance & Stochastics 4, 117–146 — the first "minimise a loss functional" formulation.
- **Delbaen, F. & Schachermayer, W.** (1994/2006), on the Fundamental Theorems and the no-free-lunch framework — why completeness ⇔ uniqueness of the martingale measure. See [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|No-Arb · 04 Fundamental Theorems]] for the finite-state version used in §2.1.
- **Artzner, P., Delbaen, F., Eber, J.-M., Heath, D.** (1999), *Coherent measures of risk*, Mathematical Finance 9(3), 203–228, and **Föllmer, H. & Schied, A.** (2004), *Stochastic Finance: An Introduction in Discrete Time* (de Gruyter) — convex risk measures and the robust representation quoted in §2.3. **Rockafellar, R.T. & Uryasev, S.** (2000), *Optimization of conditional value-at-risk*, Journal of Risk 2, 21–41 — CVaR as an infimum of a convex functional.
- **Gatheral, J.**, *The Volatility Surface*, Ch 5 §5.1 (*"no replicating hedge"* for jump models) — the concrete financial statement that incompleteness is not exotic. **Cont, R. & Tankov, P.**, *Financial Modelling with Jump Processes*, Ch 10 — the mathematical version.
- **Boyle, P. & Emanuel, D.** (1980), *Discretely adjusted option hedges*, Journal of Financial Economics 8, 259–282 — the $\sqrt{\Delta t}$ law of §05. **Bertsimas, D., Kogan, L., Lo, A.** (2000), *When is time continuous?*, Journal of Financial Economics 55, 173–204.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|BSM · 04 The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|No-Arb · 04 Fundamental Theorems]]
- Forward: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/02-convex-risk-and-the-deep-hedging-objective|02 · Convex Risk & the Deep-Hedging Objective]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Index Hub]]
- Incompleteness in the wild: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr|Advanced Volatility — Heston, SABR & SV Dynamics]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston/SABR · 06 Advanced Extensions]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/02-barriers-and-digitals|Exotics · 02 Barriers & Digitals]]
- Risk-measure side: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 Coherent Risk Measures]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs|Constraints & Transaction Costs]]
