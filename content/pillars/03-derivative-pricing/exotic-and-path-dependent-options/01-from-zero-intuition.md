---
title: "3.7.1 Exotic & Path-Dependent Options from Zero"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - path-dependent-options
  - intuition
  - monte-carlo
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

A vanilla European option is priced from **one number**: the terminal stock price $S_T$. Everything - the whole distribution - collapses into a single draw at expiry. An **exotic option** is anything whose payoff needs *more* than $S_T$. The moment it references the path's running **maximum or minimum** (lookback), its **average** (Asian), whether it **touched a level** (barrier), or a **second asset** (exchange/quanto), the pricing problem changes character, because *the payoff is now a functional of the whole path, not a function of its endpoint.*

The practical objective of this page: build the intuition for *why* this change matters, with no formula beyond one idea - **the risk-neutral expectation extends from "$S_T$" to "any functional of the path."** Three "aha"s:

1. **Path-dependence = the payoff ignores nothing.** Two different paths can end at the *same* $S_T$ yet pay *different* amounts (one touched the barrier, one didn't; one set a lower minimum, one didn't). So the terminal distribution alone is useless - you need the joint law of the path statistics and $S_T$.
2. **The pricing measure is unchanged.** You still compute $V(0)=e^{-rT}\,\mathbb{E}^{\mathbb{Q}}[\text{payoff}]$ (Glasserman 1.39; Shreve Ch 7). The *only* difference is that the payoff is now a function of more of the trajectory, so the expectation is over the full path - which is precisely what **Monte Carlo simulates**.
3. **The underlying's drift under $\mathbb{Q}$ is the cost-of-carry $b$.** For path-dependent products the distribution of the running max/min/average depends on the drift of $\log S$, which under $\mathbb{Q}$ is $b-\tfrac12\sigma^2$ (not $r$ in general). Simulating with the wrong drift misprices every path statistic.

---

### 2. Mathematical Ground Truth & Derivations

**The shared object: a path-functional.** Under the risk-neutral measure the stock is

$$
dS = b\,S\,dt + \sigma S\,dW^{\mathbb{Q}},
$$

and every exotic here is $V(0)=e^{-rT}\,\mathbb{E}^{\mathbb{Q}}\big[f(\text{path})\big]$ for a different functional $f$:

| Exotic | Path functional $f$ |
|---|---|
| Barrier (down-and-out call) | $(S_T-X)^+\cdot\mathbf 1\{\min_{0\le t\le T}S_t>H\}$ |
| Cash-or-nothing digital | $K\cdot\mathbf 1\{S_T>X\}$ |
| Lookback (floating call) | $S_T-\min_{0\le t\le T}S_t$ |
| Asian (average-rate put) | $\big(X-\frac{1}{T}\int_0^T S_t\,dt\big)^+$ |
| Quanto | payoff in *domestic* currency of a *foreign* equity |

**The reflection principle - the workhorse for barrier & lookback closed forms.** For driftless Brownian motion, the probability that the maximum exceeds a level $m$ by time $T$ equals twice the probability that the *terminal* value exceeds $m$: $\mathbb{P}(\bar W_T>m)=2\mathbb{P}(W_T>m)$. This "reflects" every path that touched $m$ into a path ending above $m$ (Shreve II Thm 7.2.1 gives the exact joint density of $(\bar W_T, W_T)$). It is the seed of every barrier/lookback closed form: price the vanilla, subtract (or add) the reflected "image" terms.

**Shreve's unifying structure (Ch 7).** Knock-out barriers solve the BSM PDE on a *shrunk domain* $0\le x\le B$ with $v(t,B)=0$; lookbacks add a running-max state $Y(t)$ and a smooth-pasting condition $v_y(t,y,y)=0$; Asians add an integral state $Y(t)=\int_0^t S\,du$ and the degenerate PDE $v_t+rxv_x+xv_y+\tfrac12\sigma^2x^2v_{xx}=rv$. In every case the state vector grows - and that is exactly the dimensionality that forces Monte Carlo.

---

### 3. Computational Implementation - path-dependence made visible

The single most convincing way to *feel* the divide: simulate one batch of paths, record both the terminal values and the running minima, and price a **lookback** (path-dependent) against a **vanilla** (terminal-only) that share the exact same terminal draws. The lookback price cannot be recovered from $S_T$ alone. Stdlib only.



The vanilla MC lands on the BSM closed form (terminal-only: the closed form *is* the answer), while the lookback put on the *same* paths is more than twice as valuable - it pays off on every path whose **running minimum** (not just endpoint) dipped below $X$. Same terminal draws, radically different prices: that is path-dependence.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "terminal distribution is enough" trap.** For an exotic you cannot compress the path to $S_T$; you need the joint law of $(\text{path statistic}, S_T)$. This is the single biggest conceptual error.
2. **Wrong drift under $\mathbb{Q}$.** Simulate with the cost-of-carry $b$ (e.g. $r-q$ for an index) in $d\log S=(b-\tfrac12\sigma^2)dt+\sigma dW$, and discount at $r$. Using $r$ as the drift when $b\neq r$ (dividend-paying underlying) biases every running-min/max statistic.
3. **Monitoring specification is part of the contract.** Continuous vs discrete monitoring changes the price (see [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06 · Advanced Extensions]]); for a **knock-in** a barrier checked daily is cheaper than one checked continuously; for a **knock-out** the daily check is *more* expensive, because the grid misses touches the continuous monitor would catch. Ignoring this is a first-principles mis-specification.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 7 (exotic options; the reflection-principle joint density, Thm 7.2.1; running-max state; the "not a dt-term" subtlety that forces lookback boundary conditions).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 3 (exact GBM path simulation §3.2; path-dependent payoffs as the natural MC targets).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, Ch 4 (the closed-form catalog that the intuition in §2 organizes).

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]]
- Continue: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/02-barriers-and-digitals|02 · Barriers & Digitals]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Theory: [[foundations/calculus-and-optimization/index|Multivariable Calculus]]
