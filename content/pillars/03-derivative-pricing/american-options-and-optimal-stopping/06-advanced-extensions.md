---
title: "3.6.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - american-options
  - monte-carlo
  - longstaff-schwartz
  - duality
  - stochastic-mesh
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]] and [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Numerical Methods · Monte Carlo]].

---

### 1. Intuition & Practical Objective

Everything so far assumes a *low-dimensional* American problem - one or two assets, where a tree or a finite-difference grid can carry the free boundary. For a **high-dimensional** American option (a Bermudan swaption on many rates, a max-of-$d$ option) grids are impossible: FDM memory is exponential in dimension, and trees are worse. **Monte Carlo is the only tool that scales** - but its natural backward induction is exactly what simulation cannot do.

The resolution is the theme of Glasserman Ch 8: approximate the **continuation value** by regression on simulated paths (Longstaff–Schwartz / LSM), which yields a **sub-optimal** stopping rule and hence a **low-biased** price; then obtain a **guaranteed upper bound** from the **duality** theorem (Rogers; Haugh–Kogan) to bracket the true value. The interval $[\text{LSM low},\ \text{dual high}]$ *contains* the truth.

> **The bias pair (Glasserman p. 421).** Using *future information* (backward induction over a finite path set, Jensen) biases **high**; using a *sub-optimal policy* biases **low**. LSM is a policy ⇒ low. The dual is a near-optimal martingale ⇒ high. Together they sandwich the price.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The dynamic program (Glasserman 8.6–8.13)

For Bermudan dates $t_1<\dots<t_m$ with payoff $h_i$, the value obeys

$$
V_m=h_m,\qquad V_i(x)=\max\big\{h_i(x),\ \underbrace{\mathbb E[V_{i+1}(X_{i+1})\mid X_i=x]}_{C_i(x)\ \text{(continuation)}}\big\},
$$

and the stopping rule induced by exact continuation values is $\hat\tau=\min\{i: h_i(X_i)\ge C_i(X_i)\}$.

#### 2.2 Longstaff–Schwartz LSM (Glasserman 8.52) - the low-biased estimator

Regress the (discounted) realised continuation cash-flow on basis functions $\psi$ of the current state:

$$
C_i(x)\approx \hat\beta_i^{\!\top}\psi(x),\qquad \hat\beta_i=\hat B_\psi^{-1}\hat B_{\psi V},
$$

then follow the rule "exercise if intrinsic $\ge$ fitted continuation" **along the realised path**, taking the value from the realised future cash-flow (not the fitted value):

$$
\hat V_{ij}=h_i(X_{ij})\ \text{if }h_i\ge\hat C_i(X_{ij}),\quad\text{else }\hat V_{i+1,j}.
$$

This is **low-biased** (Clément–Lamberton–Protter): a suboptimal policy can never beat the optimum. *(Contrast the Tsitsiklis–van Roy regression-DP $\hat V_{ij}=\max\{h_i,\hat C_i\}$, which uses the fitted value to both decide and value and is generally **high**-biased.)* Best practice: fit $\hat\beta$ on one sample, then run a **second independent pass** at the fixed rule - only then is the estimator guaranteed low.

#### 2.3 Duality - the upper bound (Glasserman 8.58–8.65; Rogers; Haugh–Kogan)

For any martingale $M$ with $M_0=0$, optional sampling gives $\mathbb E[h_\tau]\le\mathbb E[\max_k(h_k(X_k)-M_k)]$ for every $\tau$, hence

$$
\boxed{\ V_0(X_0)=\sup_\tau\mathbb E[h_\tau(X_\tau)]=\inf_{M}\ \mathbb E\!\left[\max_{k=1..m}\big(h_k(X_k)-M_k\big)\right],\qquad M_0=0.\ }
$$

Equality is attained by the martingale built from the value process: $\Delta_i=V_i(X_i)-\mathbb E[V_i(X_i)\mid X_{i-1}]$, $M_i=\sum_{s\le i}\Delta_s$. Any *approximate* value function $\hat V_i=\max\{h_i,\hat C_i\}$ yields a **valid** (if looser) upper bound

$$
V_0\le\mathbb E\!\left[\max_k\big(h_k(X_k)-\hat M_k\big)\right],
$$

with $\hat M$ from nested single-step estimates of the conditional expectation. The regression residual is (approximately) the optimal martingale difference - so a *good* basis tightens the dual; a *bad* basis loosens it (verified below: over-rich polynomial bases make the bound *worse*).

#### 2.4 Stochastic mesh, random trees, partitioning (Glasserman §8.3–8.5)

Alternatives to regression: **random trees** (Broadie-Glasserman, exponential in $m$), **state-space partitioning** (§8.4), and the **stochastic mesh** (§8.5) which keeps $b$ nodes per step and interconnects them with likelihood-ratio weights $W^i_{jk}=f_{i+1}(X_{ij},X_{i+1,k})/g(X_{i+1,k})$; the mesh recursion is high-biased, its low estimator follows the induced policy. All share the same high/low bias dichotomy.

#### 2.5 Where this sits relative to the rest of the folder

The **theory** (Snell envelope, VI, free boundary) is dimension-independent; the *tabular* solvers (trees, FDM) are not. LSM trades exactness for dimension-freedom, which is why it - not the closed forms - is what a rates desk runs for Bermudan swaptions. The implementation recipes for the regression basis, mesh weights, and variance reduction live in [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|Numerical Methods · Advanced Extensions]].

---

### 3. Computational Implementation - LSM low + dual high, bracketing the truth

Full stdlib LSM (fit on one path set, value on an independent second set) plus a duality upper bound from the fitted value function, benchmarked against a 4000-step CRR American put. Runs in $\approx18$ s.



The LSM rule lands $0.044$ **below** the tree value (the price of a slightly sub-optimal policy - exactly the guaranteed-low direction), and the dual martingale gives a valid **upper** bound. The true value lies inside the bracket. *(Trade-off observed while building this: enlarging the polynomial basis to degree 3/4 made the dual bound **worse** ($6.64\to10.3\to19.4$) because the fitted value function is used inside a max over paths - a direct instance of Glasserman's warning that the dual is only as tight as the value function is accurate.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reporting the in-sample LSM value as the price.** If the same paths both fit the rule and value it, the estimate is optimistically biased; the **second independent pass** is mandatory for a genuine lower bound (Glasserman §8.2, eqs. 8.14–8.15).
2. **Confusing LSM with regression-DP.** Tsitsiklis–van Roy’s $\max\{h,\hat C\}$ uses the *fitted* continuation to value, and is generally **high**-biased; LSM takes the value from the *realised* path and is **low**-biased. Which one you implemented changes the sign of your bias.
3. **Basis functions that do not span the value function.** LSM is exact only if $C_i$ is exactly linear in the basis (Clément–Lamberton–Protter); a poor basis makes the exercise boundary wrong and the lower bound loose. And an over-rich basis **loosens the dual** (demonstrated above) - more functions is not always better.
4. **A lower bound alone is not a price.** The dual bound is what certifies the estimate; without it a low-biased number can be arbitrarily far from the truth. Always report the interval.
5. **Dimension is not free in the *policy*.** MC scales the *pricing*, but the number of exercise dates $m$ and the regression cost grow; random-tree methods are exponential in $m$, and mesh cost is $O(mb^2)$.
6. **Nested-simulation noise inflates the dual.** $\hat M$ is a valid martingale, but a noisy conditional-expectation estimate widens the bound (it was $7.39\to6.85\to6.69$ as the nested sample $n_j$ rose $10\to40\to100$ here). Use enough nested draws.

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, **Ch 8** - §8.1–8.2 (problem, parametric low/high bias), §8.3 random trees, §8.4 partitioning, §8.5 stochastic mesh (weights 8.36–8.45), §8.6 regression DP vs LSM 8.52 and the regression/mesh-weight identity 8.54–8.56, §8.7 duality 8.58–8.69. *Math-verified in the corpus.*
- **Longstaff, F. & Schwartz, E.** (2001), *Valuing American options by simulation: a simple least-squares approach*, RFS 14(1).
- **Rogers, L.C.G.** (2002) and **Haugh, M. & Kogan, L.** (2004) - the duality upper bound.
- **Broadie, M. & Glasserman, P.** (1997, 2004) - random trees and stochastic mesh. **Andersen, L. & Broadie, M.** (2004) - primal-dual.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|Index Hub]]
- Numerical implementation (linked, not duplicated): [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Monte Carlo Pricing]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|Variance Reduction]] · [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|Numerical Methods · Advanced]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] (Bermudan swaptions are the archetypal high-dim American problem) · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Exotic & Path-Dependent Options]]
