---
title: "3.6.2 Optimal-Stopping Theory"
tags:
  - pillar-derivative-pricing
  - american-options
  - optimal-stopping
  - snell-envelope
  - martingale
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/01-from-zero-intuition|01 · From Zero]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

The practical objective: replace the vague instruction "exercise at the best time" with a **mathematically precise object** - the smallest supermartingale that dominates the payoff - and read the optimal exercise region off it. This gives both the value *and* the exercise rule, and explains in one stroke why calls and puts behave so differently.

Why supermartingales? A discounted price process under $\mathbb Q$ is a martingale. Add the *right to stop* and the value must be a process you can never make money by stopping - i.e. a **supermartingale** - that stays above the payoff (you can always exercise). The **smallest** such process is the cheapest thing that dominates the payoff: that is the price. Björk calls this the **Snell envelope**; Shreve calls it Definition 6.1(b). They are the same theorem.

> **One picture.** Below the exercise boundary the value process *equals* the payoff (you are at the supermartingale's "floor"); above it, the value process is a pure martingale (waiting is fair, so keep waiting). The boundary is where the two regions meet.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Stopping times and optimal-stopping value

A random time $\tau\in\{0,\dots,n\}$ is a **stopping time** if $\{\tau=k\}\in\mathcal F_k$ for all $k$ - the decision uses no look-ahead (Shreve I §5.2). The American value is (Shreve II §8.1; Björk §21.2)

$$
V_k=(1+r)^k\operatorname*{max}_{\tau\in\mathcal T_k}\widetilde{\mathbb E}\!\left[(1+r)^{-\tau}G_\tau\,\Big|\,\mathcal F_k\right],
$$

where $\mathcal T_k$ is the set of stopping times with $\tau\ge k$. For a continuous-time diffusion with reward $\Phi$, the value is $V(t,x)=\sup_\tau \mathbb E_{t,x}[\Phi(\tau,X_\tau)]$.

#### 2.2 Three equivalent characterisations (Shreve I Def 6.1; Björk Thm 21.12/21.23)

1. **Optimal-stopping value** - the max over $\tau$ above.
2. **Smallest supermartingale.** $\{(1+r)^{-k}V_k\}$ is the *smallest* supermartingale dominating $\{G_k\}$ (the Snell envelope of the discounted payoff).
3. **Optimal exercise time.** $\tau^*=\min\{k:V_k=G_k\}$ is optimal; the stopped process $V^{\tau^*}$ is a **martingale** on $[k,n]$ (Björk Prop 21.15).

The **backward recursion** that computes all of this is exactly the tree step from [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/01-from-zero-intuition|01 · From Zero]]:

$$
V_n=G_n,\qquad V_k=\max\big\{G_k,\ \mathbb E[V_{k+1}\mid\mathcal F_k]\big\}\quad\text{(undiscounted form, Björk Prop 21.7)}.
$$

#### 2.3 The drift test and the convexity test (Björk Props 21.2–21.5)

- **Supermartingale payoff ⇒ stop now** ($\hat\tau=0$); **submartingale ⇒ stop late** ($\hat\tau=T$); **martingale ⇒ every $\tau$ is optimal**.
- Convex increasing $g$ of a submartingale is a submartingale ($\text{mart}\to\text{mart}$ for linear, $\text{sub}$ for convex, $\text{super}$ for concave).

#### 2.4 The call/put asymmetry - a two-line proof each

**Call, no dividend (Björk §21.6.1; Shreve I Cor 2.25).** Under $\mathbb Q$, $e^{-rt}S_t$ is a martingale; $g(x)=(x-K)^+$ is convex increasing with $g(0)=0$. Hence $e^{-rt}g(S_t)=\max(e^{-rt}S_t-e^{-rt}K,\,0)$ is a **submartingale** (a convex increasing function of a martingale, with the driftless discounted strike adding an upward push). Submartingale ⇒ stop late ⇒ $\hat\tau=T$ ⇒ **the American call equals the European call**.

**Put (Shreve II §8.3).** $g(x)=(K-x)^+$ is *decreasing* in $x$; $e^{-rt}(K-S_t)$ is a **supermartingale**, so the value lies strictly above the European value and exercise can be optimal. This is the structural reason puts - and dividend-paying calls - need the free-boundary machinery.

**Call with dividends.** Between dividend dates the American call satisfies the BSM equation; it is **only ever optimal to exercise immediately before a dividend date** $t_j$ (Shreve II §8.5), giving the backward recursion: the American call equals a European call expiring at $t_j$ until $S(t_j-) - K > c_j(t_j,(1-a_j)S(t_j-))$, else hold to $T$.

---

### 3. Computational Implementation - the theory, checked on a lattice

Two experiments. **(A)** Reproduce Shreve's two-step example and expose the early-exercise node. **(B)** Test the submartingale argument: a dividend-free call should have **zero** nodes where intrinsic beats continuation; adding a yield should create an exercise region. Stdlib only.



The no-dividend call has **exactly zero** nodes where intrinsic beats continuation - the submartingale property made visible. Add a 5% yield and $55\,769$ nodes flip to exercise. The asymmetry between calls and puts is not a convention; it is a theorem, and the lattice obeys it.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"No early exercise" applied to puts.** The submartingale argument is specific to *convex increasing* payoffs with $g(0)=0$ and *no dividends*. Puts are decreasing payoffs and violate every hypothesis - early exercise is the rule, not the exception.
2. **Using the physical measure.** The Snell envelope is a $\mathbb Q$-object (discounted prices are $\mathbb Q$-martingales). Computing $\mathbb E^{\mathbb P}[e^{-r\tau}g(S_\tau)]$ prices the wrong thing; the drift $\mu$ contaminates the exercise rule.
3. **Assuming the smallest-supermartingale characterisation is automatically the price.** It is - *because the market is complete* (single Brownian driver). In an incomplete market the supermartingale envelope gives only a range, not a unique price (Björk Ch 15) - the bridge to jump/vol models.
4. **Ignoring the freedom in $\tau^*$.** Multiple stopping times can be optimal; $\tau^*=\min\{k:V_k=G_k\}$ is *a* smallest optimal one, and different but equivalent rules give the same value. Comparing two *different* exercise rules can be a false test of a pricing bug.

---

### 5. References

- **Björk**, *Arbitrage Theory in Continuous Time*
- **Shreve**, *Stochastic Calculus for Finance I*
- **Shreve**, *Stochastic Calculus for Finance II*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/01-from-zero-intuition|01 · From Zero]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/03-analytic-approximations|03 · Analytic Approximations]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]]
- Theory base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|Fundamental Theorems of Asset Pricing]]
