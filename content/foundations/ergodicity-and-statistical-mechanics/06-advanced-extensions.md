---
title: "M.9.6 Advanced Extensions"
tags:
  - foundations
  - kelly-criterion
  - portfolio-growth
  - estimation-error
  - ergodicity-economics
---

**Basic Prerequisites:** [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]] and [[foundations/ergodicity-and-statistical-mechanics/05-ruin-and-drawdown|05 · Ruin & Drawdown]].

---

### 1. Intuition & Practical Objective

Pages 04–05 sized a single bet. Real investing is a **vector** decision across correlated assets with **estimated** parameters, in a world that does not hold still. This page is the launchpad to the three extensions that turn Kelly from a casino rule into a portfolio discipline:

1. **Multi-asset (vector) Kelly.** The optimal fractions solve $\boldsymbol f^*=\Sigma^{-1}(\boldsymbol\mu-r\mathbf 1)$ - the growth-optimal analogue of mean-variance, with the same matrix inverse but a *log* objective. It naturally produces leverage and short positions.
2. **Estimation error → fractional Kelly.** Because $f^*$ is computed from noisy estimates and the growth function is asymmetric (overbetting is punished harder than underbetting), the *practical* optimum is systematically *below* the plug-in Kelly fraction. This is the single most important robustness lesson in the folder.
3. **Ergodicity economics.** The deeper theoretical extension: abandon expected-utility maximisation entirely and instead maximise the **time-average growth rate of the actual dynamic** - which, for multiplicative wealth, *derives* log utility rather than assuming it.

> **Takeaway.** Three out of four real-world blow-ups in leveraged growth strategies come from estimation error, not from the model being wrong. Multi-asset Kelly is elegant, but the fraction you should actually trade is smaller than the formula, by a factor you choose for survival.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Multi-asset (vector) Kelly

Let $\boldsymbol f$ be the vector of wealth fractions in $n$ risky assets, $\boldsymbol\mu$ the drift vector, $\Sigma$ the covariance matrix, $r$ the riskless rate. The continuous growth rate generalises $g_\infty(f)=r+f(m-r)-\tfrac12s^2f^2$ to

$$
g_\infty(\boldsymbol f)=r+\boldsymbol f^\top(\boldsymbol\mu-r\mathbf 1)-\tfrac12\boldsymbol f^\top\Sigma\boldsymbol f .
$$

Maximising (the function is concave in $\boldsymbol f$) gives the first-order condition $\Sigma\boldsymbol f=\boldsymbol\mu-r\mathbf 1$, hence

$$
\boxed{\;\boldsymbol f^*=\Sigma^{-1}(\boldsymbol\mu-r\mathbf 1)\;}\qquad
g_\infty(\boldsymbol f^*)=r+\tfrac12(\boldsymbol\mu-r\mathbf 1)^\top\Sigma^{-1}(\boldsymbol\mu-r\mathbf 1).
$$

This is the log-utility cousin of the Markowitz tangency portfolio: same $\Sigma^{-1}$, but the objective is growth, not mean-variance utility. Note the fractions can exceed $1$ (leverage) and go negative (shorts) - the constraints $\mathbf 1^\top\boldsymbol f = c$ and $\boldsymbol f\ge0$ must be added for real portfolios (Thorp §7).

#### 2.2 Estimation error and the case for fractional Kelly

In practice $(\boldsymbol\mu,\Sigma)$ are estimated, so $f^*$ is itself random. Two structural problems make the plug-in Kelly fraction an **overbet**:

- **Mean reversion / data mining:** estimated expected returns are biased *upward* ($\mathbb{E}[\hat m]>m$), so $f^*=(m-r)/s^2$ is too large.
- **Asymmetry of $g$:** the growth function is flat at its maximum and steep at the edges, so overbetting by $\delta$ costs more growth than underbetting by $\delta$ gains. The *optimal response to uncertainty* is to shrink the fraction.

Thorp's recommendation (§7.3): choose $f$ so that even if the true edge is, say, $m_t=\tfrac12\hat m$, you stay in the growth region - i.e. **cap $f$ well below $\hat f^*$**; practice uses $\boldsymbol f=0.25\hat{\boldsymbol f}^*$ to $0.5\hat{\boldsymbol f}^*$.

#### 2.3 Ergodicity economics (the theoretical extension)

Peters & Gell-Mann propose replacing "maximise expected utility" with "maximise the time-average growth rate of the dynamic". For additive dynamics $dx=\mu\,dt+\sigma\,dW$, the time-average growth equals the ensemble drift $\mu$ - reproduce the standard answer. For **multiplicative** dynamics $dx=\mu x\,dt+\sigma x\,dW$, the time-average growth rate is $\mu-\tfrac12\sigma^2$ (page 03) - so maximising it **derives** logarithmic utility rather than assuming it. Ergodicity economics thus gives the axiomatic foundation under Kelly: log utility is not an arbitrary risk-aversion choice, it is *the* utility that makes the ensemble average equal the time average.

#### 2.4 Non-stationarity and path dependence

All the closed forms assume i.i.d. returns. Real markets are non-stationary: $m$ and $s$ drift, correlations change, and regimes switch. The practical consequences are (i) $f^*$ should be re-estimated and revised over time (Thorp §7.2), and (ii) drawdowns *path-depend* - leverage that looked safe is re-levered automatically as equity falls, exactly the mechanism of 1987 and 2008.

---

### 3. Computational Implementation - vector Kelly and the estimation-error penalty

Stdlib only. Block A solves the two-asset Kelly system and verifies the closed-form growth. Block B simulates a trader who estimates the edge with noise and evaluates full Kelly versus fractional Kelly.




The punchline is in block B: with a modest estimation error, **full Kelly has almost a 20% chance of a negative twenty-year growth rate and a *lower* median outcome ($+0.600$) than half Kelly ($+0.965$)**. Fractional Kelly is not merely safer - it is *better* once you admit you do not know $\mu$. A quarter Kelly nearly eliminates the ruin probability at a small growth cost. This is the empirical case for $\boldsymbol f\approx0.5\hat{\boldsymbol f}^*$ in production.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Plugging in $\hat{\boldsymbol f}^*$ from estimated moments.** The single most common way to lose money with Kelly. Overbetting is asymmetric; the estimate is biased high; shrink the fraction (block B).
2. **Ignoring the $1^\top\boldsymbol f = c$ and $\boldsymbol f\ge0$ constraints.** Unconstrained vector Kelly can demand huge leverage or violent shorts; the constrained problem needs KKT ([[foundations/calculus-and-optimization/04-constrained-optimization|page 04 of calculus]]) and its solution is *not* a simple rescaling.
3. **Treating $\Sigma$ as known.** A poor covariance estimate (noisy, ill-conditioned) inverts into explosive weights; shrinkage/denoising is mandatory ([[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Estimation]]).
4. **Assuming stationarity.** $f^*$ moves as $\mu,s$ move; a static full-Kelly lever is a bet on regime stability as much as on the edge.
5. **Confusing vector Kelly with mean-variance optimality.** They share $\Sigma^{-1}$ but maximise different objectives; a mean-variance "optimal" portfolio is generally *not* growth-optimal (it ignores the $\tfrac12\boldsymbol f^\top\Sigma\boldsymbol f$ curvature of log wealth).

---

### 5. Canonical Literature & Study References

- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006) - §7 (portfolio Kelly, the $n$-dimensional $g(\boldsymbol f)=\mathbb{E}\ln(1+\boldsymbol f^\top\mathbf X)$, constraints), §7.3 (fractional Kelly and estimation error), §7.2 (re-estimating and revising $f^*$). *Corpus-verified.*
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion* (World Scientific, 2011) - multi-asset Kelly and the "good/bad properties" treatment of estimation error.
- **Peters, Ole**: *The Ergodicity Problem in Economics*, Nature Physics 15 (2019), and **Peters & Gell-Mann**, *Evaluating Gambles Using Dynamics*, Chaos 26 (2016) - ergodicity economics: time-average growth as the objective, deriving log utility.
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering*, Ch 1 - the standard error $\sigma_f/\sqrt n$ that governs the precision of every estimation-error experiment here. *Verified in the corpus.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series*, Ch 1 - the non-normality/fat-tail facts that make the Gaussian growth formulas a leading-order approximation. *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[foundations/ergodicity-and-statistical-mechanics/05-ruin-and-drawdown|05 · Ruin & Drawdown]]
- Hub: [[foundations/ergodicity-and-statistical-mechanics/index|Index Hub]]
- Base: [[foundations/calculus-and-optimization/04-constrained-optimization|Constrained Optimization]] (constrained vector Kelly) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Applied destinations: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Estimation, Shrinkage & RMT]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/01-quantitative-research/index|Quantitative Research]] (overfitting & estimation error)
- Forward topic-folder (in Pillar 5): `kelly-criterion-and-bet-sizing` - the applied treatment of this material.
