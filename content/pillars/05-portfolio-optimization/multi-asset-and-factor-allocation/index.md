---
title: "5.9 Multi-Asset & Factor Allocation"
tags:
  - pillar-portfolio-optimization
  - multi-asset-and-factor-allocation
  - asset-allocation
  - factor-allocation
  - strategic-vs-tactical
  - index-hub
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization & the Efficient Frontier]] and [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Factor Timing]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

"Multi-asset & factor allocation" is the discipline of deciding **what to hold** at the top of the portfolio tree - not which 500 stocks, but how much *equity*, how much *bonds*, how much *commodities*, how much *credit*, and - the modern refinement - how much *value*, *momentum*, *carry*, and *defensive* exposure regardless of the label attached to the vehicle. It is the bridge between Pillar 1 (where the return sources are *identified*) and Pillar 5's optimizer (where they are *held*).

The practical objective of this folder is a **lookup hub** plus a walked path: the formulas you need to size an asset-class or factor allocation, the carry identities that price each building block, and the failure modes that make the whole exercise fragile in a crisis.

Two framings, one decision:

1. **Asset-class allocation** - the traditional split across equities / bonds / commodities / credit. The building blocks are *labels*, and the covariance matrix of the labels is the object of study. A 60/40 portfolio looks balanced in dollars and is **overwhelmingly equity risk** in reality (≈98% here - see §3).
2. **Factor-based allocation** - the modern view (Ang 2014). Asset classes are *bundles of factors*; two "different" assets can be the same bet, and two "same" assets can be different bets. Allocating to factor premia directly **decorrelates** the portfolio far more effectively than allocating to labels: the diversified factor portfolio here carries a diversification ratio of **1.98** against **1.46** for the asset-class portfolio.

> **The one-sentence essence.** "Allocate across *return sources*, not across *names* - a diversified asset-class portfolio is usually a concentrated factor bet, and a diversified factor portfolio is what you thought you owned."

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $w\in\mathbb{R}^N$ weights (fractions of capital, $\mathbf{1}^\top w=1$), $\Sigma$ the covariance matrix, $\sigma_i=\sqrt{\Sigma_{ii}}$, $\mu$ expected returns, $r_f$ the risk-free rate, $B$ the $N\times K$ factor-loading matrix, $f$ the $K$ factor returns, $\varepsilon$ idiosyncratic noise.

| Quantity | Formula | Verified check (this folder's code) |
|---|---|---|
| Portfolio volatility | $\sigma(w)=\sqrt{w^\top\Sigma w}$ | $\sigma_{\text{eq}}=0.0789$ |
| Diversification ratio | $\mathrm{DR}(w)=\dfrac{\sum_i w_i\sigma_i}{\sqrt{w^\top\Sigma w}}$ | asset EW: $1.4568$; factor EW: $1.9782$ |
| Risk contribution (asset $i$) | $\mathrm{RC}_i=\dfrac{w_i(\Sigma w)_i}{\sigma(w)}$, $\sum_i\mathrm{RC}_i=\sigma(w)$ | equity share of 60/40 $=0.9775$ |
| Global min-variance | $w^\star=\dfrac{\Sigma^{-1}\mathbf1}{\mathbf1^\top\Sigma^{-1}\mathbf1}$ | $\{0.0170,0.6942,0.0395,0.2493\}$ |
| Mean-variance / tangency | $w^\star=\dfrac{\Sigma^{-1}(\mu-r_f\mathbf1)}{\mathbf1^\top\Sigma^{-1}(\mu-r_f\mathbf1)}$ | $\{0.1768,0.2317,0.0229,0.5686\}$, Sharpe $0.3841$ |
| Factor model of returns | $r=\alpha+Bf+\varepsilon$, $\;\Sigma_r=B\Sigma_fB^\top+D$ | asset EW $\sigma=0.0789$ vs factor EW $\sigma=0.0480$ |
| Factor-portfolio → asset map | $w_{\text{asset}}=B\,w_{\text{factor}}$ | factor EW $\Rightarrow (0.25,0.25,0.25,0.25)$ |
| Carry (generic) | $c=\mathbb{E}[r\mid\text{spot unchanged}]$ | credit $+5.5\%$, gold $-1.0\%$ (see 04) |
| Regime-conditional choice | $w^\star(\text{regime})=\arg\max_w\;\dfrac{w^\top\mu_{\text{reg}}-r_f}{\sqrt{w^\top\Sigma_{\text{reg}}w}}$ | min-var rotates: bonds $0.6942\to0.5991$ |

**The three decompositions that matter.**

- **Capital vs risk.** Euler's theorem on the degree-1 homogeneous $\sigma(w)$ splits total risk exactly: $\sigma(w)=\sum_i w_i\partial\sigma/\partial w_i$. This is why a "$60/40$" portfolio is a $97.75\%$-equity bet: dollars and risk are different units.
- **Asset vs factor.** $\Sigma_r=B\Sigma_fB^\top+D$ separates *systematic co-movement* (through $B,\Sigma_f$) from idiosyncratic noise $D$. A cross-asset correlation of $0.2$ can be entirely a single shared factor; once you allocate to the *factors*, the residual correlations vanish.
- **Strategic vs tactical.** Strategic allocation fixes a long-horizon policy weight $w_{\text{SAA}}$ from long-run $\mu,\Sigma$; tactical allocation overlays a *deviation* $\Delta w$ driven by short-horizon signals (valuation, carry, trend, regime), subject to a tracking-error budget $\Delta w^\top\Sigma\,\Delta w\le \text{TE}^2$.

---

### 3. Computational Implementation - the hub engine

One self-contained snippet (numpy) that computes every headline number in the table: portfolio volatility, the diversification ratio, risk shares, and the factor-vs-asset contrast.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's full failure-mode analysis lives in [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Diversification is regime-dependent.** Cross-asset correlations rise precisely when you need them low; the equal-weight portfolio's volatility jumps $1.19\times$ from calm to crisis and its effective number of bets collapses ($3.17\to2.20$).
2. **Factor crowding.** Factors are *traded* - a popular factor gets crowded, its Sharpe decays, and its correlation to everything else rises (the bridge to Pillar 1's crowding page).
3. **Estimation error is the dominant term.** A mean-variance optimizer fed 24 months of noisy history posts a *worse* out-of-sample Sharpe ($0.14$) than naive $1/N$ ($0.30$), at roughly $8\times$ the volatility - MVO is an estimation-error maximizer.
4. **Carry is not free.** The carry premium is compensation for crash risk; carry strategies have a famously negative skew (the "carry crash").

---

### 5. References

- **Ang, Andrew**: *Asset Management: A Systematic Approach to Factor Investing* (Oxford University Press, 2014)
- **Meucci, Attilio**: *Risk and Asset Allocation* (Springer Finance, 2005)
- **Ilmanen, Antti**: *Expected Returns: An Investor's Guide to Harvesting Market Rewards* (Wiley, 2011)
- **Qian, Hua & Sorensen**: *Quantitative Equity Portfolio Management* (Chapman & Hall/CRC, 2007)
- **Grinold & Kahn**: *Active Portfolio Management* (2nd ed., 2000)

---

### 6. Connected Graph Bridges

- **Sub-pages (in-folder):** [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/01-from-zero-intuition|01 · From Zero Intuition]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/02-asset-class-allocation|02 · Asset-Class Allocation]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/03-factor-based-allocation|03 · Factor-Based Allocation]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/04-carry-and-styles|04 · Carry & Styles]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/06-advanced-extensions|06 · Advanced Extensions]]
- **Sibling topics (Pillar 5):** [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Bayesian Allocation]] (turning views into strategic weights) · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] (the all-weather multi-asset idea) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & the Efficient Frontier]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]]
- **Cross-pillar:** [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Factor Timing]] (the factor zoo, crowding, timing) · [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] (the input to page 06)
- **Foundations:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/calculus-and-optimization/index|Calculus & Convex Optimization]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]

**Beginner:** start at [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/05-failure-modes-and-practice|05]]
