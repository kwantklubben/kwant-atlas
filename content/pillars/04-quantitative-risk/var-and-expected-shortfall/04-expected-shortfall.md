---
title: "4.1.4 Expected Shortfall (CVaR)"
tags:
  - pillar-quantitative-risk
  - var-and-expected-shortfall
  - expected-shortfall
  - cvar
  - tail-risk
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|03 · Coherent Risk Measures]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Expected Shortfall (ES) - also called Conditional VaR, CVaR, Mean Shortfall, or Tail-VaR - is **the average loss on the days VaR is breached.** It is the direct answer to VaR's most damning silence: *"and then what?"*

This page gives the three equivalent definitions of ES (tail mean, quantile integral, Rockafellar–Uryasev minimum), proves the two non-obvious facts - that the quantile integral *equals* the tail mean, and that ES $\ge$ VaR always - and verifies all three numerically. The practical payoff: ES is **coherent** and **convex-optimisable**, which is why it, not VaR, is the modern default (and the Basel FRTB standard).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The three definitions

For a loss $L$ and confidence level $\alpha\in(0,1)$:

$$
\textbf{(Tail mean)}\quad \mathrm{ES}_\alpha(L)=\mathbb{E}\big[L\mid L\ge \mathrm{VaR}_\alpha(L)\big].
$$
$$
\textbf{(Quantile integral)}\quad \mathrm{ES}_\alpha(L)=\frac{1}{1-\alpha}\int_\alpha^1 \mathrm{VaR}_u(L)\,du.
$$
$$
\textbf{(Rockafellar–Uryasev)}\quad \mathrm{ES}_\alpha(L)=\min_{\beta\in\mathbb{R}}\Big\{\,\beta+\frac{1}{1-\alpha}\,\mathbb{E}\big[(L-\beta)^+\big]\Big\},\quad (t)^+=\max(t,0).
$$

The tail mean integrates the loss over the worst $(1-\alpha)$ fraction of outcomes - the region *beyond* VaR. The quantile integral averages VaR across confidence levels $u\in(\alpha,1]$; for continuous distributions these coincide. For **discrete** distributions the tail mean needs a correction, and the quantile integral is the clean definition:

$$
\mathrm{ES}_\alpha(L)=\frac{1}{1-\alpha}\Big(\mathbb{E}\big[L\,\mathbf{1}_{\{L\ge \mathrm{VaR}_\alpha\}}\big]-\mathrm{VaR}_\alpha\big(\mathbb{P}(L\ge \mathrm{VaR}_\alpha)-(1-\alpha)\big)\Big).
$$

#### 2.2 The Rockafellar–Uryasev characterization (2000, Thm. 1)

Define the convex function $F_\alpha(\beta)=\beta+\frac{1}{1-\alpha}\mathbb{E}[(L-\beta)^+]$. Its subgradient is $1-\frac{1}{1-\alpha}\mathbb{P}(L\ge\beta)$. Theorem 1: **$F_\alpha$ is convex, continuously differentiable, minimised at $\beta=\mathrm{VaR}_\alpha$, and its minimum equals $\mathrm{ES}_\alpha$**:

$$
\boxed{\ \mathrm{ES}_\alpha=\min_\beta F_\alpha(\beta),\qquad \mathrm{VaR}_\alpha=\text{left endpoint of }\arg\min_\beta F_\alpha(\beta)\ }
$$

Consequences: (i) you can compute ES **without first computing VaR**; (ii) minimising ES over a portfolio is a *convex program* (often a plain LP after sampling: $F_\alpha\approx\beta+\frac{1}{q(1-\alpha)}\sum_k (L_k-\beta)^+$ with auxiliary $u_k\ge0$), while VaR minimisation may have multiple local extrema ([[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|02 · §2.2]]).

#### 2.3 ES $\ge$ VaR, always

Since $F_\alpha(\beta)=\beta+(1-\alpha)^{-1}\mathbb{E}[(L-\beta)^+]$ and $\mathbb{E}[L\mid L\ge\mathrm{VaR}]\ge\mathrm{VaR}$ on the tail, the minimum $F_\alpha(\mathrm{VaR})=\mathrm{ES}_\alpha$ cannot fall below $\mathrm{VaR}_\alpha$. Rockafellar–Uryasev: "the $\alpha$-VaR is never more than the $\alpha$-CVaR" - portfolios with low CVaR necessarily have low VaR as well.

#### 2.4 Closed form and the normal benchmark

For $L\sim\mathcal{N}(\mu,\sigma^2)$ (Hull eq. 22.1):
$$
\mathrm{VaR}_\alpha=\mu+\sigma z_\alpha,\qquad \mathrm{ES}_\alpha=\mu+\sigma\frac{\varphi(z_\alpha)}{1-\alpha},\qquad z_\alpha=\Phi^{-1}(\alpha).
$$
At $\alpha=0.975$: $\mathrm{ES}=2.337803$ vs $z_{0.99}=2.326348$ - the reason FRTB's $97.5\%$ ES matches the old $99\%$ VaR in the normal benchmark. Under fat tails (Student-$t$, EVT), the same quantile gives a *much* larger ES ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT §ES]]).

---

### 3. Computational Implementation - three representations, verified to agree

Monte Carlo normal sample; verify the empirical tail mean equals the quantile integral equals the analytic formula. Stdlib only.




All three agree to Monte Carlo precision (the small residual is $O(1/\sqrt{N})$ and the discrete-quantile granularity of the tail mean). ES exceeds VaR by the expected $14.6\%$ normal gap.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **ES is harder to *estimate*.** It averages a handful of tail points, so its sampling variance exceeds VaR's - a $99\%$ ES from a 250-day window is noisier than the VaR it sits above ([[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · §3]]). Coherence buys aggregation safety at the cost of estimation stability; use filtered/EVT methods (McNeil–Frey) for tail efficiency.
2. **Coherence does not mean elicitable.** Gneiting (2011) showed **ES is not elicitable** on its own (VaR is). This is the honest counter-argument to ES and the reason FRTB backtests ES *indirectly*, through its VaR component and joint VaR–ES scoring. Coherence and backtestability are *different* desiderata.
3. **Definition drift on discrete books.** For loss pmfs with atoms, "mean of losses $\ge$ VaR" over-counts the boundary atom; use the corrected quantile-integral form (§2.1) so ES equals $\lim_{\alpha'\downarrow\alpha}$ of the smooth tail mean. Two desks can otherwise disagree.
4. **Horizon scaling is only valid i.i.d.** $\mathrm{ES}_N=\mathrm{ES}_1\sqrt N$ (Hull) presumes i.i.d. returns; with autocorrelation or volatility clustering the true multi-day ES differs - McNeil–Frey show multi-day conditional ES beats naive $\sqrt N$ scaling.
5. **ES is still a single number.** It summarises the whole tail by its *mean*; a strategy can shape the distribution *beyond* ES (a very rare but catastrophic jump) to evade it - hence the parallel need for stress testing ([[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]).

---

### 5. Canonical Literature & Study References

- **Rockafellar, R.T. & Uryasev, S.**, *Optimization of Conditional Value-at-Risk*, *Journal of Risk* 2(3):21–41 (2000) - Defs. of VaR/CVaR, the function $F_\alpha$ and Thms. 1–2 (CVaR as a convex minimum), the linear-programming reduction. *Primary source; read in full from the corpus PDF.* (Extended: *Conditional Value-at-Risk for General Loss Distributions*, *JBF* 26(7), 2002.)
- **Artzner, Delbaen, Eber & Heath**, *Coherent Measures of Risk* (1999) - §5.1 (tail conditional expectation), Prop. 5.2 (VaR is the least coherent measure dominating it).
- **Acerbi, C. & Tasche, D.**, *On the Coherence of Expected Shortfall*, *J. Banking & Finance* 26(7):1487–1503 (2002) - ES coherence for general distributions; Euler allocation of ES.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 (ES definition, normal ES eq. 22.1, Basel ES@97.5%). *Numerically verified in the corpus.*
- **McNeil & Frey**, *Estimation of Tail-Related Risk Measures…*, *J. Empirical Finance* 7 (2000) - conditional ES via GARCH + EVT.
- **Gneiting, T.**, *Making and Evaluating Point Forecasts*, *JASA* 106(494) (2011) - the non-elicatability of ES (the backtesting caveat).

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|03 · Coherent Risk Measures]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|06 · Spectral/Euler & Basel ES]]
- Sibling: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Estimation Methods]]
