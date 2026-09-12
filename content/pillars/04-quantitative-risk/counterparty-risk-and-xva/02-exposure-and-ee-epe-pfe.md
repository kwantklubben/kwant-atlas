---
title: "4.7.2 Exposure Profiles"
tags:
  - pillar-quantitative-risk
  - counterparty-risk-and-xva
  - exposure
  - epe
  - pfe
  - monte-carlo
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/counterparty-risk-and-xva/01-from-zero-intuition|01 · From Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (lognormal simulation).

---

### 1. Intuition & Practical Objective

CVA needs one input more than any other: **the exposure profile** - the expected positive value of the portfolio at every future date, *conditional on the counterparty having survived so far*. This page builds that profile from scratch and separates the four statistics a desk actually quotes:

$$
\underbrace{\text{EE}(t)=\mathbb{E}[V(t)^+]}_{\text{expected exposure}},\quad \underbrace{\text{EPE}=\tfrac1T\!\int_0^T\!\text{EE}(t)\,dt}_{\text{expected positive exposure}},\quad \underbrace{\text{ENE}(t)=\mathbb{E}[V(t)^-]}_{\text{expected negative exposure}},\quad \underbrace{\text{PFE}_\alpha(t)}_{\text{quantile}}.
$$

The practical objective is the **shape**, because the shape *is* the answer. A forward's exposure **grows monotonically** (the further out you look, the more the spot can move away from the strike). A *swap's* exposure is **humped** - large in the middle, collapsing to zero at maturity, because near maturity there are few remaining payments to differ. Quantifying that shape is the job of a Monte Carlo over risk-factor paths.

> **Why simulation, not a formula?** The exposure at date $t$ is $\max(V(t),0)$ where $V$ depends on the whole future path of rates/FX/vol and on collateral terms. EPE is an *option-like* quantity - and for a swap it is exactly a strip of **co-terminal ("diagonal") swaptions** (Sorensen–Bollier 1994). That is the deep point: *exposure quantification is at least as hard as pricing the instrument.*

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Defining the profile and averaging it

For a grid $0=t_0<t_1<\dots<t_m=T$:
$$
\text{EE}(t_i)=\mathbb{E}\!\left[\max(V(t_i),0)\right],\qquad \text{EPE}=\frac{1}{m}\sum_{i=1}^{m}\text{EE}(t_i)\ \ (\text{time-weighted if uneven}),
$$
$$
\text{ENE}(t_i)=\mathbb{E}\!\left[\min(V(t_i),0)\right],\qquad \text{PFE}_\alpha(t_i)=\inf\{x:\mathbb{P}(V(t_i)^+\le x)\ge\alpha\}.
$$

For CVA the profile is taken **discounted to today**: replace $\text{EE}(t_i)$ by $D(0,t_i)\,\text{EE}(t_i)$ (Gregory §17.2.2, citing Jamshidian 1989 to avoid a convexity bias).

#### 2.2 A tractable example: the at-the-money forward

Take a forward to buy the asset at $K$ at time $T$, on a spot that follows geometric Brownian motion under $\mathbb{Q}$:
$$
dS_t=rS_t\,dt+\sigma S_t\,dW_t,\qquad S_t=S_0\exp\!\left[(r-\tfrac12\sigma^2)t+\sigma\sqrt t\,Z\right].
$$

Set $K=S_0 e^{rT}$ (the **no-arbitrage forward price**, so the forward is struck at-the-money and worth zero today). The value at $t$ is the discounted forward gap
$$
V(t)=S_t-K\,e^{-r(T-t)}=S_t-S_0e^{rt},
$$
so $\mathbb{E}[V(t)]=0$ and the forward has **symmetric** exposure. Because $S_t$ is lognormal, the expected positive exposure has a clean closed form:
$$
\boxed{\;\text{EE}(t)=S_0 e^{rt}\left[2\,\Phi\!\left(\tfrac{\sigma\sqrt t}{2}\right)-1\right]\;}
$$
*(derivation: for lognormal $X$ with mean $S_0e^{rt}$, $\mathbb{E}[(X-K)^+]=\mathbb{E}[X]\Phi(d_1)-K\Phi(d_2)$ with $d_1=\sigma\sqrt t/2,\ d_2=-\sigma\sqrt t/2$).*

Two immediate consequences, both visible in the numbers below:

- **EE(t) increases with $t$** - the profile of a forward is monotone, unlike a swap's hump.
- **EE(t) increases with $\sigma$** - exposure is manufactured by uncertainty. At $\sigma=40\%$ the 5-year EE is roughly *four times* the $\sigma=10\%$ value.

#### 2.3 Why a swap looks different

An interest-rate swap's exposure is *humped* because it is a **portfolio of co-terminal swaptions**: each future floating payment fixes against a forward that can move, so the value-to-be-replaced peaks in mid-life and goes to zero as the last payments wash out (Gregory §15.1.3). The forward above is the atom; a swap is a sum of such atoms with a decaying annuity weight.

---

### 3. Computational Implementation - an exposure profile by Monte Carlo

Simulate the ATM forward of §2.2, tabulate EE/ENE, compute the average EPE and the 95% PFE, and confirm the Monte Carlo against the closed form. Standard library only.



Three things to verify by eye: (i) the Monte Carlo EE tracks the closed form within sampling error (~0.5%); (ii) $\text{EPE}+\text{ENE}=0$ to within noise (symmetric ATM forward); (iii) the 95% PFE (**133.7**) is far above the average EPE (**16.4**) - a reminder that PFE answers a different question from EPE, and that *most* of the tail sits in a small fraction of paths.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Roll-off / grid misses.** Exposure jumps exist at cash-flow dates, exercise dates, break clauses and resets. A coarse time grid that skips them **understates** EPE (Gregory §15.3.1 "roll-off risk"). Put critical dates into the grid or use look-back points.
2. **Parameter misestimation propagates linearly.** EPE scales roughly with volatility; a volatility estimate that is 40% too low produces a CVA that is ~40% too low. Better to be conservative here than precise.
3. **Wrong measure.** CVA/FVA are **risk-neutral** computations (market-implied vols and drifts); PFE/IMM are often **physical**. Mixing them in one Monte Carlo silently biases both (Gregory §15.3.3).
4. **The ATM-forward intuition does not generalise.** A *swap's* profile is humped and can be much larger than a forward's; assuming monotone growth, or treating EPE as a constant, mis-states the mid-life peak that dominates CVA.
5. **Correlation = exposure too.** For multi-currency or multi-asset portfolios the EPE depends on **correlations**, which are far harder to estimate than volatilities. Under-modelling correlation is the quiet source of exposure surprise (see [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Gregory, Jon**: *The xVA Challenge* (5th ed., 2025) - Ch 11 (exposure definitions, EFV/EPE/ENE/PFE, the five-scenario and normal examples) and Ch 15 (Monte Carlo methodology, grids, roll-off risk, margin modelling). *Deep-read and numerically checked in the corpus.*
- **Sorensen & Bollier** (1994): the co-terminal-swaption representation of swap exposure (EPE = swaption payoff × risky duration).
- **Pykhtin & Zhu** (2007): *A Guide to Modeling Counterparty Credit Risk* - the practitioner standard for PFE and expected exposure.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 24 §24.7 (exposure, netting, collateral); **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 1/4 (simulation and variance reduction).

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
