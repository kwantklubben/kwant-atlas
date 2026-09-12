---
title: "3.8.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - american-options
  - adi
  - quasi-monte-carlo
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] and [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction]].

---

### 1. Intuition & Practical Objective

The two families of pages 02–04 solve *linear* problems on *one* state variable. Three things break that: **(i) early exercise** turns the PDE into a free-boundary (variational-inequality) problem and the MC into a *stopping-time* problem; **(ii) extra factors** make a full grid cost $O(N^d)$ and force operator splitting; **(iii) high effective dimension** is where Monte Carlo's $n^{-1/2}$ starts to be beaten by *deterministic* point sets. This page is the launchpad for all three, each with a runnable check against a benchmark.

> **Why these three?** They are the exact three axes on which production pricing systems are chosen: exercise style, dimension, and dimension-free error. Everything else (Heston, LMM, jump PIDEs) is these solvers applied to a wider operator.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 American options: three equivalent statements

**Free boundary / complementarity** (Duffy eqs. 26.5–26.11). For an American put with exercise boundary $B(t)$:

$$
\frac{\partial P}{\partial t}+\tfrac12\sigma^2S^2\frac{\partial^2P}{\partial S^2}+rS\frac{\partial P}{\partial S}-rP=0 \ \ \text{for }S>B(t),\qquad
P\ge\max(K-S,0)\ \ \text{everywhere},
$$

with **smooth pasting** at the boundary $P(B(t),t)=K-B(t)$ and $\partial P/\partial S(B(t),t)=-1$, and terminal boundary $B(T)=K$. Equivalently: $\mathcal LP\le0$ and $P\ge g$, with $(\mathcal LP)\,(P-g)=0$ - a linear complementarity problem.

**Penalty regularisation** (Duffy eqs. 28.15–28.17). Replace the constraint by a large nonlinear reaction term:

$$
f_\varepsilon(P_\varepsilon)=\frac1\varepsilon\,[g(S)-P_\varepsilon]^+ \qquad\text{or}\qquad f_\varepsilon(P_\varepsilon)=\frac{\varepsilon C}{P_\varepsilon+\varepsilon-q(S)},\quad q(S)=K-S,\ C\ge rK,
$$

then $P_\varepsilon\to P$ in $L^\infty_{\text{loc}}$ as $\varepsilon\to0$ (Thm 28.2). The semi-implicit scheme (implicit in the linear terms, explicit in $f_\varepsilon$) satisfies the discrete constraint $P^n_j\ge\max(q,0)$ **iff** $k\le\varepsilon/(rK)$ (Thm 28.3) - a cheap, monotone, no-Newton route.

**Projected SOR on the LCP** (Duffy eq. 29.11, Thm 29.1).

$$
z_j^{(k+1)}=b_j+\sum_{i<j}A_{ji}c_i^{(k+1)}-\sum_{i>j}A_{ji}c_i^{(k)},\qquad
c_j^{(k+1)}=\max\!\big(0,\ c_j^{(k)}+\omega\,z_j^{(k+1)}/A_{jj}\big),
$$

convergent for any start **iff** $0<\omega<2$ (positive-definiteness of $A$ is what matters). For a put the projection max is against intrinsic value.

**Monte Carlo: Longstaff–Schwartz (LSM)** (Glasserman eqs. 8.46–8.52). Regress the realised discounted continuation value on basis functions of the current state,

$$
\hat C_i(x)=\hat\beta_i'\psi(x),\qquad \hat\beta_i=\hat B_\psi^{-1}\hat B_{\psi V},\qquad
\hat V_{ij}=h_i(X_{ij})\ \text{if }h_i\ge\hat C_i(X_{ij}),\ \text{else}\ \hat V_{i+1,j}.
$$

Two distinct estimators must not be confused: the **Tsitsiklis–van Roy regression DP** ($\hat V=\max\{h_i,\hat C_i\}$, biased **high** through Jensen when the basis is imperfect) and **LSM** (value taken from the *realised* continuation path, biased **low**: any implementable stopping rule is suboptimal). Duality closes the bracket (Glasserman eqs. 8.58, 8.65):

$$
V_0=\sup_\tau\mathbb E[h_\tau]=\inf_M\mathbb E\!\left[\max_{k=1..m}\big(h_k(X_k)-M_k\big)\right]\ \Longrightarrow\ \text{low}\le V_0\le\text{dual upper}.
$$

#### 2.2 Multidimensional: ADI and operator splitting

**Peaceman–Rachford ADI** (Duffy eqs. 19.7a–b, growth factor 19.5/19.6): each half-step is only *conditionally* stable, but the two-leg step is **unconditionally** stable and second order in time and space:

$$
\frac{U^{n+\frac12}_{ij}-U^n_{ij}}{k/2}=\Delta^2_xU^{n+\frac12}_{ij}+\Delta^2_yU^{n}_{ij},\qquad
\frac{U^{n+1}_{ij}-U^{n+\frac12}_{ij}}{k/2}=\Delta^2_xU^{n+\frac12}_{ij}+\Delta^2_yU^{n+1}_{ij}.
$$

Two hard limits from Duffy: a naive three-leg ADI in 3-D is **not** unconditionally stable (eq. 19.34 → use Douglas–Rachford), and **ADI breaks down with mixed derivatives** (eq. 19.37) - exactly the correlated multi-asset case. The fix is **Yanenko splitting**, treating the cross term explicitly (eqs. 20.8/20.9), or a general $m$-way split $L=L_1+\dots+L_m$ converging when the discrete operators commute (eqs. 20.21–20.24).

#### 2.3 Quasi-Monte Carlo

**Koksma–Hlawka** (Glasserman eq. 5.10): for a deterministic low-discrepancy set with star discrepancy $D^*$,

$$
\left|\frac1n\sum_if(x_i)-\int f\right|\ \le\ V_{HK}(f)\,D^*,\qquad
D^*\le C(d,b)\,b^t\,\frac{(\log n)^d}{n}+O\!\Big(\frac{(\log n)^{d-1}}{n}\Big),
$$

so QMC's error is $O(n^{-1+\varepsilon})$ against Monte Carlo's $O(n^{-1/2})$ - **conditional on finite Hardy–Krause variation $V_{HK}(f)$**, which fails for non-axis-aligned indicator payoffs (barriers) and is the reason QMC is applied to *smooth* integrands. Randomisation (**random shift / digit scrambling**) restores unbiasedness and gives valid error bars, with scrambled-net variance $O(n^{-(3-\varepsilon)})$ for smooth $f$ - a rate Monte Carlo can never reach.

---

### 3. Computational Implementation - three checks

**A. American put by three methods.** PSOR on the implicit-Euler PDE, a CRR tree as the benchmark, and LSM for the path view. Note the *sign* of the deviation in each case - LSM must sit below the benchmark.




The PSOR values converge *upward* to the tree benchmark ($4.6818\to4.6854\to4.6890$ against $4.6921$) - implicit-Euler-in-time is $O(k)$ and the domain is truncated at $S_{\max}=400$, so the residual $0.003$ is exactly the discretisation error of pages 02/05. The LSM value $4.6765$ sits **below** the true price, as the low-bias theorem demands, with the early-exercise premium versus the European $4.4494$ equal to $4.6765-4.4494=0.2271$ (the benchmark's premium is $0.2427$).

**B. Multidimensional: ADI versus explicit on the 2-D heat equation.** ADI is unconditionally stable; the explicit scheme is not, and the *initial condition* decides whether the instability shows.




ADI matches the exact centre value $0.138911$ to three decimals at $40\times40$ nodes with only $40$ time steps, and at $\Delta t=0.1/60$ - where the explicit amplification factor is $\rho_{\max}=-4.33$ - ADI still returns a bounded $0.225107$ against the explicit scheme's $1.73\times10^{33}$. The smooth-IC explicit runs are *stable but inaccurate at coarse steps* (the same phenomenon as page 02), and the step IC is what exposes the instability: the discrete Laplacian annihilates a constant, so high-frequency content is required to see $\rho$ in action.

**C. Quasi-Monte Carlo: Halton versus pseudo-random in 8 dimensions.** The integrand is an 8-fixing geometric Asian, so an exact closed form exists to measure both estimators against; randomised (shifted) Halton supplies the error bar.




At 2,000 points in 8 dimensions, low-discrepancy points cut the RMSE from $0.1692$ to $0.0302$ - a $31.4\times$ variance reduction, roughly seven times the antithetic device of page 04 ($31.4/4.41$) and obtained at about a twentieth of the path count. Note also the honest counter-example in the same output: the *unrandomised* Halton value $6.0202$ is off by $-0.1174$, about four times the randomised RMSE. That is the **plateau / false-convergence** trap of Glasserman §5.5 - never use unrandomised QMC without skipping a burn-in and checking stability across $n$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **American pricing is a free-boundary problem, not a European formula.** Applying the closed form to an American put understates it by the early-exercise premium ($4.6921$ vs $4.4494$ - a $5.5\%$ error here). Every route must enforce $P\ge g$: projection (PSOR), penalty, front fixing, or an explicit exercise check (tree/LSM).
2. **The two Monte Carlo American estimators have opposite biases.** LSM is low-biased ($4.6765$ below $4.6921$) and the regression DP is high-biased; quoting one as "the price" without a duality upper bound hides which way the error points.
3. **ADI dies on cross derivatives.** The correlated multi-asset PDE contains $\rho\sigma_1\sigma_2S_1S_2\,\partial^2V/\partial S_1\partial S_2$; standard ADI is not unconditionally stable there (Duffy eq. 19.37) - use Yanenko splitting with the mixed term treated explicitly, or an iterative (Rothe + SOR/GS) solve.
4. **The three-leg ADI in 3-D is not stable.** Duffy eq. 19.34 is explicit: use Douglas–Rachford or simple splitting; a naive generalisation of the 2-D result is a silent blow-up.
5. **QMC requires finite variation and is not a black box.** Koksma–Hlawka's bound is useless when $V_{HK}(f)=\infty$ (barrier/indicator payoffs, non-axis-aligned regions), and unrandomised points can plateau at a wrong value (the $-0.1174$ above). Fix: smooth the integrand, use effective-dimension reduction (Brownian bridge / principal components for Gaussian vectors), and randomise for error bars.
6. **Grid methods do not scale in dimension.** FDM costs $O(N^d)$ memory; the practitioner's rule (Duffy Ch 24) is $1$–$3$ factors for FD/FEM, and Monte Carlo/meshless beyond. The boundary between the two families is therefore set by *dimension*, not by accuracy.

---

### 5. References

- **Duffy**, *Finite Difference Methods in Financial Engineering*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Haug**, *Complete Guide to Option Pricing Formulas*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward topics: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (whose 2-D PDE needs ADI/splitting) · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure Models]] (HJM/LMM simulation, Ch 3.6–3.7 of Glasserman)
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · Advanced Extensions]] (American early exercise and jump-diffusion MC)
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
