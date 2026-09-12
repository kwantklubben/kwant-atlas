---
title: "4.1 Value at Risk & Expected Shortfall"
tags:
  - pillar-quantitative-risk
  - var-and-expected-shortfall
  - risk-measures
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (CDFs, quantiles, expectation) and [[pillars/04-quantitative-risk/var-and-expected-shortfall/01-from-zero-intuition|01 · From Zero (this folder)]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

This folder answers one question with two competing instruments: **how much can we lose, and how bad is the part we did not plan for?** *Value at Risk* (VaR) is a **quantile** - the loss level that is exceeded only $(1-\alpha)$ of the time. *Expected Shortfall* (ES, a.k.a. Conditional VaR / CVaR / Tail-VaR) is the **average of the losses beyond that quantile** - the answer to "and then what?"

This folder is a *hub*: it (a) gives the **fast formula lookup and the coherence scorecard** below (job #1 of this pillar), and (b) routes to six sub-pages that walk from raw intuition through the definition and its flaws, the coherence axioms, ES, the failure modes, and the spectral/regulatory extensions.

> **The one-sentence essence.** "VaR tells you the *door* to the tail but not what is behind it; ES prices what is behind the door, and unlike VaR it is *coherent* - a merger of independent bets never looks riskier than the sum of its parts."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $L=-\Delta V$ is the portfolio **loss** over horizon $\Delta t$; $\alpha\in(0,1)$ the confidence level; $F_L$ the loss CDF; $\Phi,\varphi$ the standard-normal CDF/density; $z_\alpha=\Phi^{-1}(\alpha)$.

| Quantity | Formula | Verified check (§3) |
|---|---|---|
| **VaR** (quantile) | $\mathrm{VaR}_\alpha(L)=\inf\{l:\mathbb{P}(L>l)\le 1-\alpha\}=F_L^{-1}(\alpha)$ | - |
| Artzner (net-worth) form | $\mathrm{VaR}_\alpha(X)=-\inf\{x:\mathbb{P}(X\le xr)>\alpha\}$ | - |
| **ES** (tail mean) | $\mathrm{ES}_\alpha(L)=\mathbb{E}[L\mid L\ge \mathrm{VaR}_\alpha(L)]$ | - |
| **ES** (quantile integral) | $\mathrm{ES}_\alpha(L)=\dfrac{1}{1-\alpha}\displaystyle\int_\alpha^1 \mathrm{VaR}_u(L)\,du$ | - |
| **ES** (Rockafellar–Uryasev) | $\mathrm{ES}_\alpha(L)=\min_{\beta\in\mathbb{R}}\Big\{\beta+\tfrac{1}{1-\alpha}\mathbb{E}[(L-\beta)^+]\Big\}$ | - |
| Normal VaR | $\mathrm{VaR}_\alpha=\mu+\sigma z_\alpha$ | $\mu{=}0,\sigma{=}1,\alpha{=}.99\Rightarrow 2.326348$ |
| Normal ES | $\mathrm{ES}_\alpha=\mu+\sigma\dfrac{\varphi(z_\alpha)}{1-\alpha}$ | $2.665214$ |
| Normal ES / VaR ($99\%$) | $\dfrac{\varphi(z_\alpha)}{(1-\alpha)z_\alpha}$ | $1.145665$ |
| N-day scaling (i.i.d.) | $\mathrm{VaR}_N=\mathrm{VaR}_1\sqrt{N}$; $\mathrm{ES}_N=\mathrm{ES}_1\sqrt{N}$ | Hull 22.4 |

**The coherence scorecard (Artzner et al. 1999, Def. 2.4).** A risk measure $\rho$ is *coherent* iff it satisfies all four axioms. VaR satisfies three and **fails subadditivity**; ES satisfies all four.

| Axiom | Statement | VaR | ES |
|---|---|---|---|
| **T** Translation invariance | $\rho(L+c)=\rho(L)+c$ | ✅ | ✅ |
| **S** Subadditivity | $\rho(L_1+L_2)\le\rho(L_1)+\rho(L_2)$ | ❌ | ✅ |
| **PH** Positive homogeneity | $\rho(\lambda L)=\lambda\rho(L),\ \lambda\ge0$ | ✅ | ✅ |
| **M** Monotonicity | $L_1\le L_2\ \text{a.s.}\Rightarrow\rho(L_1)\le\rho(L_2)$ | ✅ | ✅ |
| *(bonus)* Convexity / optimizability | convex in positions | ❌ (may have local extrema) | ✅ (convex, LP-solvable) |

> **Subadditivity failure in one line (after Artzner §3.3, made discrete; §3 of this hub).** Two independent bonds each default with probability $4\%$ losing $ $\$100: $\mathrm{VaR}_{95\%}=0$ for each alone, but $1-0.96^2=7.84\%>5\%$, so the merged $\mathrm{VaR}_{95\%}=100$. *A merger created measured risk from nothing.*

**Regulatory switch (Basel FRTB).** The 1996 Amendment / Basel II.5 set market-risk capital on **10-day $99\%$ VaR**, $\text{capital}=k\cdot\mathrm{VaR}$ with multiplier $k\ge3$ (Hull BS 22.1). The **Fundamental Review of the Trading Book** (BCBS 2019, d457) replaces VaR with **$97.5\%$ Expected Shortfall** - chosen so that, in the normal benchmark, $\mathrm{ES}_{97.5\%}\approx\mathrm{VaR}_{99\%}$ while capturing the tail VaR ignores.

---

### 3. Computational Implementation - the formula engine

Standard library only ($\Phi$ from `math.erf`; a rational $\Phi^{-1}$). Reproduces every number above.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Tail blindness.** VaR is a single quantile: it is *silent* about the magnitude of losses beyond it (change the worst loss from $-3$ to $-15$ and a $99\%$ VaR does not move - §5/§3). Optimizing against a VaR constraint therefore rewards selling deep-OTM tails.
2. **Non-coherence / non-convexity.** VaR violates subadditivity and its acceptance set is non-convex; it can have multiple local extrema in portfolio weights (Rockafellar–Uryasev), making it hazardous to optimize and unsafe to decentralise.
3. **Estimation error.** Both measures must be *estimated*; $99\%$ VaR from a 250-day window has a sampling standard deviation of order $0.23\sigma$, and empirical ES is noisier still because it averages a handful of tail points.

---

### 5. References

- **Artzner, Delbaen, Eber & Heath** - *Coherent Measures of Risk*, *Mathematical Finance* **9**(3):203–228 (1999). Defines the four coherence axioms (Def. 2.4), proves VaR fails subadditivity (§3.3 with the digital-option and normal-distribution remarks), and proposes **tail conditional expectation** (§5.1)
- **Rockafellar & Uryasev** - *Optimization of Conditional Value-at-Risk*, *Journal of Risk* **2**(3):21–41 (2000). Introduces the convex function $F_\alpha(x,\zeta)=\zeta+\frac{1}{1-\alpha}\mathbb{E}[(L-\zeta)^+]$ whose minimum is CVaR and whose minimiser is VaR (Thms 1–2), reducing CVaR optimisation to linear programming. *Read in full from the corpus PDF.*
- **Acerbi & Tasche** - *On the Coherence of Expected Shortfall*, *J. Banking & Finance* **26**(7):1487–1503 (2002). ES is coherent under general (non-normal) distributions; the formal justification for Basel's shift to ES.
- **McNeil & Frey** - *Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach*, *J. Empirical Finance* **7**(3–4):271–300 (2000). Conditional/dynamic VaR-ES via GARCH + EVT
- **Hull** - *Options, Futures, and Other Derivatives*
- **McNeil, Frey & Embrechts** - *Quantitative Risk Management* (2015)

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/01-from-zero-intuition|01 · From Zero]]
- Sub-pages (in-folder): 01 From Zero · 02 VaR Definition & Flaws · 03 Coherent Risk Measures · 04 Expected Shortfall · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Risk Constraints & Mean–Variance]]

**Beginner:** start at [[pillars/04-quantitative-risk/var-and-expected-shortfall/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05]]
