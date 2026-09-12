---
title: "3.7.5 Failure Modes & Real-World Practice for Exotics"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - failure-modes
  - monte-carlo
  - discrete-monitoring
  - greeks
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange|04 · Compound/Chooser/Quanto/Exchange]].

---

### 1. Intuition & Practical Objective

The closed forms in this folder are beautiful, and *three of their assumptions break in real markets*. This page names the failures precisely and shows each in money terms, so a practitioner knows *which* knob to distrust:

1. **Monitoring is discrete, not continuous.** The barrier closed forms assume the barrier is watched continuously. Real contracts (and MC) check at discrete dates, so the discrete price is systematically **above** the continuous one for knock-outs (the grid "misses" touches).
2. **Pathwise MC Greeks fail for the step payoffs.** Digit/digital and barrier deltas come from a *density*, not a step - pathwise differentiation gives exactly zero (Glasserman Ch 7). Only the likelihood-ratio (score) method recovers the true Greek.
3. **Correlation is a wobbly input.** Quanto/exchange/spread prices depend on $\rho$; it is the least-stable market parameter, and a small error propagates through the closed forms ([[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]).

---

### 2. Mathematical Ground Truth & Derivations

**Discrete vs continuous monitoring.** The continuously-monitored down-and-out value $v_c$ uses the first-hitting-time density of the Brownian bridge. A discretely-monitored contract (grid $\Delta t$) only sees the path at grid points, so the knock-out probability is smaller and the value $v_d>v_c$. Broadie–Glasserman–Kou (1995) restore agreement to $O(\Delta t)$ by pricing the **continuous** formula at the *shifted* barrier

$$
H_D = H\,e^{\pm\beta\sigma\sqrt{\Delta t}},\qquad \beta=\frac{\zeta(1/2)}{\sqrt{2\pi}}\approx 0.5826,
$$

`+` when the barrier is above spot, `−` when below (Haug §5.6). This is the single most-used "dirty fix" in the exotic-options playbook.

**Pathwise vs likelihood-ratio Greeks (Glasserman Ch 7).** For a digital $Y=e^{-rT}K\mathbf 1\{S_T>X\}$, the pathwise derivative $dY/dS_0$ exists a.s. but equals **zero** - the indicator is flat almost everywhere, and the genuine delta comes from the strike-crossing that pathwise differentiation misses. The likelihood-ratio method differentiates the *density* instead: for lognormal $S_T$, the score is $Z/(S_0\sigma\sqrt T)$, and the LR delta estimator is

$$
\widehat{\Delta}_{LR}=e^{-rT}K\,\mathbf 1\{S_T>X\}\cdot\frac{Z}{S_0\sigma\sqrt T},\qquad\text{with }\mathbb{E}[\widehat{\Delta}_{LR}]=K e^{-rT}\frac{\varphi(d_2)}{S_0\sigma\sqrt T}.
$$

The rule of thumb (Glasserman §7.2.2): pathwise applies when the payoff is **continuous (Lipschitz)** in the parameter - which *excludes* digitals, barriers, and 2nd derivatives.

---

### 3. Computational Implementation - the failures in numbers

**Experiment 1 - discrete monitoring overprices a knock-out, BGK fixes it.** Stdlib only.



Discrete MC overprices the knock-out by up to ~24% at coarse grids; the BGK-shifted continuous formula lands within MC error of the discrete MC.

**Experiment 2 - pathwise delta of a digital fails; likelihood-ratio recovers it.**



The pathwise derivative of the digital is identically zero - useless. The likelihood-ratio (score) estimator matches the analytic delta to 4 dp, because it differentiates the density, not the step.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Continuous-form assumption (monitoring).** Using the continuous closed form for a discretely-monitored barrier misprices by the whole missed-hit probability - Experiment 1 quantifies it, BGK fixes it.
2. **Pathwise Greeks on step payoffs.** Digit/binary and barrier deltas cannot come from pathwise differentiation (identically zero); use likelihood-ratio or finite differences with common random numbers (Glasserman Ch 7; the central+CRN estimator dominates with RMSE $O(n^{-2/5})$).
3. **Correlation instability.** Margrabe/quanto/spread depend on $\rho$; it drifts and smiles, and it is *less* observable than vol. Always re-run the exotic price across a $\rho$-band (sensitivity, not point estimate).
4. **Rebate & parity traps.** In–out parity holds only at $K=0$; mixing rebated and non-rebated forms (or using American barrier parity, which fails) misprices.
5. **MC dimension confusion.** MC error is $O(n^{-1/2})$ in *paths*, but the discrete-monitoring bias is $O(\Delta t)$ in *steps*. A "converged" MC on too-coarse a grid is confidently wrong - always push $n_{steps}$ and check it changes the answer.

---

### 5. References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*
- **Haug**, *The Complete Guide to Option Pricing Formulas*
- **Broadie, Glasserman & Kou (1995)**, "A Continuity Correction for Discrete Barrier Options," *Math. Finance*
- **Hull**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange|04 · Compound/Chooser/Quanto/Exchange]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
