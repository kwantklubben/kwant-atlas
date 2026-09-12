---
title: "3.9.4 Numeraire Change, the HJM Framework & Market Models (LFM/LMM, BGM)"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - numeraire
  - forward-measure
  - hjm
  - libor-market-model
  - bgm
  - black-76
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page is the mathematical *engine room* of interest-rate modelling: the two tools that make rate derivatives tractable. The practical objective: understand why forward-LIBOR products are priced by **Black's formula under the forward measure**, and why swaptions need the **annuity measure**, all via a single device - the **change of numeraire**.

Two structural ideas, both with no constant-$r$ analogue:

1. **A numeraire is just a unit of account you choose to make the payoff simple.** Under the risk-neutral measure $\mathbb{Q}$ (numeraire = bank account $B$), a $T$-payoff needs the messy $\mathbb{E}[e^{-\int_0^T r} \cdot]$ integral. Switch to the **$T$-forward measure** $\mathbb{Q}^T$ (numeraire = the $T$-bond $P(t,T)$) and the same claim prices as $P(t,T)\,\mathbb{E}^{\mathbb{Q}^T}[\text{payoff}]$ - no discount integral, and *any forward rate spanning to $T$ is a martingale* under $\mathbb{Q}^T$. That martingale property is what makes Black's lognormal formula exact.

2. **Model the object you price, not a hidden state.** Short-rate models specify $r$ and derive the curve. **HJM** instead specifies the *whole forward curve* $df(t,T)=\alpha(t,T)dt+\sigma(t,T)dW$ - which fits today's curve *by construction* - and the no-arbitrage **drift condition** then fixes $\alpha$ from $\sigma$ alone. But lognormal *instantaneous* forwards explode (see §2.3). The fix is the **LIBOR market model (LFM/LMM = BGM)**: model each *simple* forward LIBOR $F_k$ as lognormal under its own measure, giving exact Black caplets and avoiding the explosion.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Change of numeraire & the forward measure (BM Ch2; Björk Ch26; Shreve Ch33)

A numeraire is any strictly positive asset. **Fact One (BM Ch2):** price/numeraire is a martingale under that numeraire's measure; **Fact Two:** the risk-neutral price is invariant under change of numeraire. The Radon–Nikodym derivative between bank-account ($\mathbb{Q}$) and forward ($\mathbb{Q}^T$) measures is

$$
\frac{d\mathbb{Q}^T}{d\mathbb{Q}}=\frac{P(T,T)/B(T)}{P(0,T)/B(0)}=\frac{1}{B(T)P(0,T)}.
$$

Pricing a $T$-payoff $X$:

$$
\Pi_t(X)=B(t)\mathbb{E}^{\mathbb{Q}}\!\left[\frac{X}{B(T)}\right]=P(t,T)\,\mathbb{E}^{\mathbb{Q}^T}\left[X\right].
$$

The **Girsanov kernel between two numeraires is their volatility difference**: for numeraires $S_0,S_1$ the kernel is $\varphi^1_0(t)=\sigma_1(t)-\sigma_0(t)$ (Björk eq. 26.20). Crucially, the instantaneous forward $f(t,T)$ is a $\mathbb{Q}^T$-martingale, and the forward LIBOR $L(t;T,S)$ is a $\mathbb{Q}^S$-martingale (numeraire $P(t,S)$) - different maturity indices (Björk Lemma 26.10; BM Prop 2.5.1).

**Forward vs futures (Björk Ch29 correction):** forward price $f(t;T,Y)=\mathbb{E}^{\mathbb{Q}^T}[Y]$; futures price $F(t;T,Y)=\mathbb{E}^{\mathbb{Q}}[Y]$; they are equal *iff* the short rate is deterministic.

#### 2.2 HJM framework (BM Ch5; Björk Ch25; Shreve Ch28/34; Hull Ch33)

Model the forward curve directly:

$$
df(t,T)=\alpha(t,T)dt+\sigma(t,T)dW(t),\qquad f(0,T)=f^{M}(0,T).
$$

No-arbitrage forces the **drift condition** (Björk Prop 25.2):

$$
\alpha(t,T)=\sigma(t,T)\int_t^T\sigma(t,s)ds .
$$

The drift is *completely determined by volatility* - no freedom remains. With this, the bond satisfies $dP=rP\,dt-\sigma^*(t,T)P\,dW$ with accumulated vol $\sigma^*(t,T)=\int_t^T\sigma(t,s)ds$. **Musiela parametrization** ($x=T-t$, $r(t,x)=f(t,t+x)$) turns this into an infinite-dimensional SDE (Björk §25.3). One-factor HJM with mean-reverting vol $\sigma e^{-a(T-t)}$ **is** the Hull–White model (BM Ch5 headline).

#### 2.3 Why lognormal *instantaneous* forwards explode (Shreve Ch34; Björk Ch27)

Take $\sigma(t,T)=\sigma f(t,T)$. Then $\sigma^*(t,T)=\sigma\int_t^T f(t,u)du$ and the HJM drift is $\alpha=\sigma^2 f\int f \sim f^2$. The deterministic toy $f'=f^2$, $f(0)=c$, solves $f(t)=c/(1-ct)$ and **blows up at $t=1/c$** - HJM show the stochastic analogue does the same. Hence: model lognormal *simple* (LIBOR) rates instead.

#### 2.4 LIBOR market model / BGM (BM Ch6; Björk Ch27; Shreve Ch34; Hull Ch33)

Forward LIBOR $F_k(t)=L(t;T_{k-1},T_k)$ is a **martingale under its own forward measure** $\mathbb{Q}^{T_k}$. The LFM postulates

$$
dF_k(t)=\sigma_k(t)F_k(t)\,dZ_k(t)\quad\text{under }\mathbb{Q}^{T_k}.
$$

The **caplet** is then priced *exactly* by Black's formula (BM Prop 6.4.1; Björk Def 27.2):

$$
Cpl_i(t)=P(t,T_i)\,\tau_i\Big[F_i(t)N(d_1)-K N(d_2)\Big],\quad d_1=\frac{\ln(F_i/K)+\tfrac12 v_i^2}{v_i},\quad v_i^2=\int_t^{T_{i-1}}\sigma_i^2(s)\,ds\ \text{(vol accumulated to the reset }T_{i-1}\text{)}.
$$

Under a *single* common measure (e.g. terminal/spot-LIBOR $\mathbb{Q}^d$), the rates carry **drift terms** summing over other rates (BM Prop 6.3.3):

$$
dF_k=\sigma_kF_k\Big[\sum_{j=\beta}^{k}\frac{\rho_{kj}\tau_j\sigma_jF_j}{1+\tau_jF_j}\Big]dt+\sigma_kF_k\,dZ^d_k .
$$

The forward **swap rate** $R_{\alpha,\beta}$ is a martingale under the **annuity (swap) measure** $\mathbb{Q}^{\alpha,\beta}$ (numeraire $C_{\alpha,\beta}(t)=\sum\tau_iP(t,T_i)$), giving the **Black swaption** formula (BM Prop 6.7.1):

$$
PS^{Black}(0)=C_{\alpha,\beta}(0)\Big[R(0)N(d_1)-K N(d_2)\Big].
$$

---

### 3. Computational Implementation - Black caplets, the martingale, and swaptions

Stdlib only: price a caplet by Black, verify forward-LIBOR is driftless (a martingale) under its own measure, and price a swaption under the annuity measure.



The forward LIBOR is driftless under its own measure (MC returns $F(0)$ to $10^{-4}$) - *that* is why the Black caplet is exact, not an approximation. The swaption uses the annuity numeraire, not the bank account.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Modelling lognormal instantaneous forwards** - the HJM explosion of §2.3. This is *the* structural reason market models exist; do not "fix" it by fiat.
2. **Wrong numeraire for the product.** Caplets need the $T$-forward measure; swaptions need the annuity measure; spot-LIBOR products need $\mathbb{Q}^d$. Pricing a caplet with a constant-discount shortcut, or a swaption with the bank account, is a first-principles error (BM Ch6 §6.2 rigorously avoids any "deterministic discount" approximation).
3. **LFM vs LSM distributional incompatibility.** A swap rate built from lognormal forwards is *not* exactly lognormal under the annuity measure (BM §6.8) - "mostly theoretical" in practice (Brace-Dun-Barton), but real when vols are high.
4. **Forward ≠ futures with stochastic rates.** The futures price is a $\mathbb{Q}$-martingale; the forward is $\mathbb{Q}^T$. Conflating them (Björk Ch29 corrected error) misses the convexity/marking-to-market adjustment.

---

### 5. References

- **Brigo–Mercurio**, *Interest Rate Models*
- **Björk**, *Arbitrage Theory in Continuous Time*
- **Shreve**, *Stochastic Calculus for Finance I*
- **Hull**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
