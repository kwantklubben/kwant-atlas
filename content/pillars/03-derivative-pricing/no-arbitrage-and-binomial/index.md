---
title: "3.2 No-Arbitrage & the Binomial Model"
tags:
  - pillar-derivative-pricing
  - no-arbitrage-and-binomial
  - binomial-trees
  - risk-neutral-measure
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and high-school algebra. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Two prices for the same payoff cannot coexist, because the difference is free money. That single sentence - the **law of one price** - is the whole engine of derivative pricing, and it is worth nothing unless you can *build* the alternative: a portfolio of traded assets that reproduces the payoff exactly. The **binomial model** is the smallest market in which that construction is possible, and it is the model where every concept of continuous-time finance (risk-neutral measure, martingale, state price, completeness, dynamic hedging) appears in a form you can compute by hand.

This folder is the *hub* of that topic. It gives (a) the **fast formula lookup** below - job #1 of this pillar - and (b) six sub-pages that walk from one-period replication through multiperiod trees, the Fundamental Theorems, the failure modes, and the road to continuous time.

> **The one-sentence essence.** "A derivative's price is the cost of the cheapest self-financing portfolio that replicates it; because that cost is independent of the real-world drift, the price can always be written as a discounted expectation under an artificial measure $\widetilde{\mathbb P}$ - and under that measure the discounted stock is a martingale."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Everything below is transcribed from the verified corpus (Shreve Vol I Ch 1–3, 5–8; Björk Ch 2–3; Hull Ch 13; Haug §4.1–4.2) and every number in the check column was **re-executed** from the scripts in §3 and the sub-pages.

**Notation:** $S_k$ stock at step $k$, $u>1$ up-factor, $d<1$ down-factor, $r$ one-period risk-free rate, $T$ maturity, $n$ number of steps, $\Delta t=T/n$, $f_u,f_d$ the claim's up/down payoffs, $b$ cost-of-carry, $\sigma$ volatility, $\zeta(\omega)$ the state price of state $\omega$.

| Quantity | Formula | Verified check |
|---|---|---|
| **One-period no-arbitrage bracket** (Shreve 1.2; Björk Prop 2.3) | $d<1+r<u$ | $S_0{=}4,u{=}2,d{=}\tfrac12,r{=}\tfrac14$: $0.5<1.25<2$ ✓ |
| **Risk-neutral probabilities** (Shreve 1.8) | $\tilde p=\dfrac{1+r-d}{u-d},\quad \tilde q=\dfrac{u-1-r}{u-d}$ | $\tilde p=\tilde q=0.5$, $\tilde p+\tilde q=1$ |
| **Replicating delta** (Shreve 1.6) | $\Delta_0=\dfrac{f_u-f_d}{S_0(u-d)}$ | put $K{=}5$: $\Delta_0=-0.5000$, bond $=3.2000$ |
| **One-period price** (Shreve 1.9) | $V_0=\dfrac{1}{1+r}\left[\tilde p f_u+\tilde q f_d\right]$ | $V_0=1.2000$; replication both states $=0.0000/3.0000$ ✓ |
| **Multiperiod RN valuation** (Shreve §3.4) | $V_k=(1+r)^k\,\widetilde{\mathbb E}\!\left[\dfrac{V_m}{(1+r)^m}\,\Big|\,F_k\right]$ | discounted stock: $\widetilde{\mathbb E}[S_1/(1{+}r)]=4.000000=S_0$ |
| **State price** (Arrow–Debreu) | $\zeta(\omega)=\dfrac{\widetilde{\mathbb P}(\omega)}{1+r}$ | $\zeta(H)=\zeta(T)=0.4$, $\sum\zeta=0.8=\frac{1}{1+r}$ |
| **State-price valuation** | $V_0=\sum_\omega \zeta(\omega)V_1(\omega)=\mathbb E^{\mathbb P}[\zeta\,V_1]$ | $1.2000$ for **any** physical $p$ (checked $p=0.5,0.6,0.9$) |
| **CRR up/down** (CRR 1979; Hull 13.15/13.16) | $u=e^{\sigma\sqrt{\Delta t}},\quad d=\dfrac1u=e^{-\sigma\sqrt{\Delta t}}$ | $n{=}100$, $T{=}0.5$: $u=1.021440$, $d=0.979010$ |
| **CRR risk-neutral prob** (Hull 13.17) | $p=\dfrac{e^{b\Delta t}-d}{u-d}$ ($b=r$ stock, $b=r-q$ index) | same: $p=0.504126$, $d<e^{r\Delta t}<u$ ✓ |
| **CRR European put** (Haug 7.1–7.6) | $e^{-rT}\displaystyle\sum_{i=0}^{n}\binom{n}{i}p^i(1-p)^{n-i}(X-Su^id^{\,n-i})^+$ | $n{=}1000\Rightarrow 4.4496$ vs BSM $4.4494$ (Haug-verified) |
| **CRR American put** (Haug 7.9–7.11) | $P_{j,i}=\max\!\big(X-Su^id^{\,j-i},\;e^{-r\Delta t}(pP_{j+1,i+1}+(1-p)P_{j+1,i})\big)$ | $n{=}1000\Rightarrow 4.6921$ (early-exercise premium $0.2427$) |
| **First Fundamental Theorem** (Shreve II 5.4.7; Björk Ch 3) | arbitrage-free $\iff$ an equivalent martingale measure exists | $1$-stock $3$-state market: EMM set is $1$-dimensional |
| **Second Fundamental Theorem** (Shreve II 5.4.9; Björk Prop 3.15) | complete $\iff$ the EMM is **unique** | same market: claim price range $[0.5952,0.6667]$; after adding a $3$rd asset: $0.628571$ |
| **Perpetual American put** (Shreve Ch 8.8) | $v(x)=\dfrac{6}{x}$ for $x\ge3$; $\;v(x)=5-x$ for $0<x\le3$ | $v(4)=1.5000$; $v(8)=0.7500$ |

> **Two caveats to carry into every calculation.** (1) The risk-neutral probabilities are *derived* from the replication equations - they are **not** the real coin-toss probabilities and carry no forecasting content (Shreve §1.1). (2) The bracket $d<1+r<u$ is a *condition*, not a convention: a tree that violates it has arbitrage and its "$p$" leaves $[0,1]$ (see [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 3. Computational Implementation - the tree engine

Stdlib only (`math`), one function for European and American puts/calls. It reproduces the Haug-verified CRR numbers used throughout this folder.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Violating the bracket.** Any tree with $e^{r\Delta t}\ge u$ (or $\le d$) has arbitrage and a "probability" $p\notin[0,1]$; the up/down factors must bracket the risk-free growth.
2. **$p\ne\tilde p$ confusion.** Discounting the *real-world* expected payoff - $\mathbb E^{\mathbb P}[\cdot]/(1+r)$ - gives the wrong number whenever $\tilde p\ne p$; only the $\widetilde{\mathbb P}$ expectation prices.
3. **Ignoring early exercise.** A European formula applied to an American put understates value by the early-exercise premium ($0.2427$ on the running example).
4. **Treating convergence as monotone.** CRR error is $O(1/n)$ but *oscillates*, badly so for at-the-money American puts - "more steps" is not uniformly better.

---

### 5. Canonical Literature & Study References

- **Shreve, Steven E.**: *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model* - §1.1 (no-arbitrage bracket, delta, $\tilde p/\tilde q$), Ch 2 (conditional expectation, martingales), Ch 3 (general APT, completeness, risk-neutral valuation), Ch 5–8 (American pricing, stopping times, Jensen, random walks, the perpetual put). *The primary source of this folder; math-verified in the corpus.*
- **Shreve, Steven E.**: *Stochastic Calculus for Finance II* - §5.4 (First/Second Fundamental Theorems, market price of risk), §5.2 (Girsanov, risk-neutral pricing). *Math-verified.*
- **Björk, Tomas**: *Arbitrage Theory in Continuous Time* - Ch 2 (binomial, replicating weights Prop 2.9–2.11), Ch 3 (general one-period model, Farkas' lemma, FTA, state-price/SDF Prop 3.18). *Math-verified.*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) - Ch 13 (one-step delta, risk-neutral valuation, CRR parameters, American backward induction, convergence). *Verification report in the corpus.*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* - §4.1 (CRR European, eq 7.1–7.6), §4.2 (CRR American + tree Greeks, eq 7.9–7.11). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Sibling topic: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (the continuous-time limit of exactly this model)
- Related flat notes: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage Foundations & Binomial Trees]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|BSM & Feynman–Kac]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]]
- Sub-pages (in-folder): 01 From Zero · 02 No-Arbitrage & Risk-Neutral · 03 Trees & Convergence · 04 Fundamental Theorems · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/01-from-zero|01]] · **Practitioner:** start at [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05]]
