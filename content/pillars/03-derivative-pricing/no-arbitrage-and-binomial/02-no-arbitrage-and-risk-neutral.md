---
title: "3.2.2 No-Arbitrage, the Risk-Neutral Measure & State Prices"
tags:
  - pillar-derivative-pricing
  - no-arbitrage-and-binomial
  - risk-neutral-measure
  - martingale
  - state-prices
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/01-from-zero|01 · From Zero]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Page 01 built the price by replication. This page names the *structure* underneath it, because that structure - not the algebra - is what generalizes to continuous time.

Three objects are equivalent, and knowing they are the same object is most of the subject:

1. **No arbitrage** - no self-financing portfolio starts at zero and ends non-negative with a positive chance of being positive.
2. **A risk-neutral measure** $\widetilde{\mathbb P}$ - a probability measure, equivalent to the real one, under which the **discounted** stock is a martingale.
3. **State prices** $\zeta(\omega)$ - Arrow–Debreu prices of a dollar in state $\omega$; every payoff is priced as $\sum_\omega\zeta(\omega)\,f(\omega)$, and they sum to $1/(1+r)$ because a dollar in every state *is* the bond.

The practical objective: be able to move freely between "expected payoff", "martingale", and "state price" language - because a desk quotes in the first, proves in the second, and calibrates in the third.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The risk-neutral measure and the martingale property

With $\tilde p,\tilde q$ from [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/01-from-zero|01]], the one-step recursion $V_k=\frac{1}{1+r}[\tilde pV_{k+1}(H)+\tilde qV_{k+1}(T)]$ rearranges to

$$
V_k=(1+r)^k\,\widetilde{\mathbb E}\!\left[\frac{V_m}{(1+r)^m}\,\Big|\,F_k\right]\qquad\text{(risk-neutral valuation, Shreve §3.4)}
$$

and in particular, applied to the stock itself,

$$
\widetilde{\mathbb E}\!\left[\frac{S_{k+1}}{(1+r)^{k+1}}\,\Big|\,F_k\right]=\frac{S_k}{(1+r)^k}\qquad\Longleftrightarrow\qquad \tilde pu+\tilde qd=1+r .
$$

**The discounted stock - not the stock - is the $\widetilde{\mathbb P}$-martingale.** (Under the *physical* measure, $S_k$ is a martingale only if $pu+qd=1$; here $pu+qd\ne1+r$ in general, which is exactly why the real measure cannot price.) This single fact is the discrete statement of "$dS=rS\,dt+\sigma S\,d\widetilde W$" in [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02]].

#### 2.2 Self-financing wealth

A portfolio process $\Delta=(\Delta_0,\dots,\Delta_{n-1})$ with each $\Delta_k$ $F_k$-measurable (no inside information) is **self-financing** if wealth evolves as (Shreve §3.3)

$$
X_{k+1}=\Delta_kS_{k+1}+(1+r)\big(X_k-\Delta_kS_k\big)=(1+r)X_k+\Delta_k\big(S_{k+1}-(1+r)S_k\big).
$$

The bracketed term is a $\widetilde{\mathbb P}$-martingale increment, so **$X_k/(1+r)^k$ is a $\widetilde{\mathbb P}$-martingale** for every self-financing, adapted strategy. Discounted prices are martingales; that is the whole content of the measure.

#### 2.3 State prices (Arrow–Debreu)

Define

$$
\boxed{\;\zeta(\omega)=\frac{\widetilde{\mathbb P}(\omega)}{1+r}\;}
$$

Then $\sum_\omega\zeta(\omega)=\frac{1}{1+r}$ (the bond) and $\sum_\omega\zeta(\omega)S_1(\omega)=S_0$ (the stock) - the two traded assets are *reproduced* by the state-price system. Any claim is priced by

$$
V_0=\sum_\omega\zeta(\omega)\,f(\omega).
$$

Equivalently, writing $Z(\omega)=d\widetilde{\mathbb P}/d\mathbb P$ (the Radon–Nikodym derivative) and $\zeta=\frac{Z}{1+r}$, the price is a *physical*-measure expectation

$$
V_0=\mathbb E^{\mathbb P}\!\left[\zeta\,f\right].
$$

$Z$ is the **stochastic discount factor / state-price density** (Björk Prop 3.18, $\Pi(0;X)=\mathbb E^{\mathbb P}[\Lambda X]$ with $\Lambda=\frac{1}{1+R}\frac{dQ}{dP}$; Shreve Vol I Ch 9, $\zeta_k=(1+r)^{-k}Z_k$). Crucially $\zeta$ *depends on the physical measure* while $V_0$ **does not** - the same price is recovered for every $\mathbb P$ consistent with the same $\widetilde{\mathbb P}$.

---

### 3. Computational Implementation - martingale, state prices, measure-invariance

All checks on Shreve's $S_0=4,u=2,d=\tfrac12,r=\tfrac14$, $K=5$ put. Stdlib only.




Two things are visible in that output. The state prices reproduce *both* traded assets, so they are the market's pricing kernel; and the price $1.200000$ is recovered under physical probabilities $p=0.5$, $0.6$, and $0.9$ - the state-price density $\zeta=Z/(1+r)$ absorbs the change of measure exactly. **The price is a property of the traded assets, not of anyone's beliefs.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Discounting under the wrong measure.** $\mathbb E^{\mathbb P}[f]/(1+r)$ is *not* the price unless $\mathbb P=\widetilde{\mathbb P}$. The state-price form $\mathbb E^{\mathbb P}[\zeta f]$ is correct for any $\mathbb P$ - provided $\zeta$ is right.
2. **Martingaling the wrong object.** $S_k$ itself is not the $\widetilde{\mathbb P}$-martingale; $S_k/(1+r)^k$ is. Confusing the two produces a spurious drift and mispricing of every path-dependent claim.
3. **Forgetting measurability.** $\Delta_k$ must be $F_k$-measurable - chosen from information available *before* the step. A "hedge" that uses $S_{k+1}$ is look-ahead and its apparent profit is fictitious.
4. **Reading $\zeta$ as a probability.** State prices sum to $1/(1+r)<1$, not to $1$. They are prices, and their discount factor is baked in; treating them as probabilities double-discounts.
5. **Assuming $\zeta$ is unique.** In an incomplete market the state-price vector is a *set*, so a claim has a price *interval*, not a price ([[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|04 · Fundamental Theorems]]).

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance I*, §2.4 (martingale/super-/submartingale conditions $pu+qd\gtrless1$; the discounted stock as the $\widetilde{\mathbb P}$-martingale), §3.3–3.4 (self-financing wealth, risk-neutral valuation, state prices/Radon–Nikodym in Ch 9). *Math-verified.*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 3 - equivalent measures (Def 3.5), martingale measure (Def 3.7), martingale pricing (Prop 3.15), stochastic discount factor $\Lambda$ and $\Pi(0;X)=\mathbb E^{\mathbb P}[\Lambda X]$ (Prop 3.18, the Arrow–Debreu system). *Math-verified.*
- **Shreve**, *Stochastic Calculus for Finance II*, §5.2 - the continuous version: Girsanov, market price of risk, $V(t)=\widetilde{\mathbb E}[e^{-\int_t^TR}V(T)\,|\,F(t)]$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/01-from-zero|01 · From Zero]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/03-binomial-trees-and-convergence|03 · Trees & Convergence]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|04 · Fundamental Theorems]]
- Theory: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 PDE & Derivation]]
