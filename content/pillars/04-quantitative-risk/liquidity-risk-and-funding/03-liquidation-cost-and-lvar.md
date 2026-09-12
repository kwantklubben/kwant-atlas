---
title: "4.6.3 Liquidation Cost & Liquidity-Adjusted VaR (L-VaR)"
tags:
  - pillar-quantitative-risk
  - liquidity-risk-and-funding
  - liquidity-adjusted-var
  - market-impact
  - liquidation-horizon
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] and [[pillars/04-quantitative-risk/liquidity-risk-and-funding/02-market-vs-funding-liquidity|02 · Market vs Funding Liquidity]].

---

### 1. Intuition & Practical Objective

Value at Risk is built on a lie of convenience: **it assumes you can liquidate the whole position in zero time at the mid price.** Neither clause is true. This page removes them, one at a time, and rebuilds VaR into a **liquidity-adjusted VaR (L-VaR)**:

$$
\text{L-VaR}\;=\;\underbrace{\text{VaR}_{\text{market}}}_{\text{price risk over the horizon}}\;+\;\underbrace{\text{LC}_{\text{exogenous}}}_{\text{spread you cross}}\;+\;\underbrace{\text{LC}_{\text{impact}}}_{\text{price you move by selling}}.
$$

The objective is the decomposition itself: know which component dominates, because the fix differs. If spread dominates, trade smaller/patiently; if impact dominates, the position is simply too large for the market and must be split over days.

Three ideas carry the page:
1. **Two liquidation costs, two mechanisms.** The *exogenous* cost is the spread and its variability - independent of your size. The *endogenous* cost is your own market impact - it grows with the **square** of your size, because both the number of shares *and* the price concession per share rise with $Q$.
2. **The liquidation horizon is a risk multiplier.** Liquidating over $T$ days means you are exposed for $T$ days, so market risk scales like $\sqrt T$ - but the *schedule* of forced execution adds cost that scales like $T$ in the worst (linear-impact) case. This is exactly why Basel's market-risk horizon is 10 days, and why the FRTB introduces liquidity horizons that can be far longer for illiquid risk factors.
3. **L-VaR is a coherent upgrade of VaR, not a different animal.** It keeps the quantile (so backtesting machinery survives) and adds a *deterministic* liquidation cost - the Bangia–Diebold–Schuermann–Stroughair (1999) construction.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Exogenous liquidation cost (spread).** Selling realises the half-spread plus a *worsening of the spread itself* in the tail. With relative spread $s$ and spread volatility $\sigma_s$, the $\alpha$-confidence liquidation cost on value $V$ is
$$
\text{LC}_{\text{exog}}=\tfrac12 V\left(S+z_\alpha\sigma_S\right).
$$
The first term is the mechanical cost of crossing a normal quarter-spread; the second prices the realistic possibility that **when you are forced to sell, the spread is wider than usual** - the cost and the tail are correlated. This is the pillar's established L-VaR form (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|the flat liquidity note]] for the same formula in $\sum_i P_iQ_i$ form).

**2.2 Endogenous liquidation cost (market impact).** With linear price impact $\Delta p=\lambda q$ (Foucault eq. 2.8) and depth $D=1/\lambda$ shares to move the price by one unit, liquidating $Q$ shares moves the price by $Q/D$. The **volume-weighted** execution price sits at the mid of the impact, so the shortfall per share is $\tfrac12 Q/D$ and
$$
\boxed{\ \text{LC}_{\text{impact}}=\frac{Q^2}{2D}=\frac{\lambda Q^2}{2}\ }
$$
The $Q^2$ is the whole story: doubling the position **quadruples** the impact cost. Equivalently, in return terms the impact drag is $\tfrac{\lambda Q}{2}$ per unit of value traded.

> **Reality check on the exponent.** Real impact is closer to **square-root** (Almgren–Chriss 2000 temporary impact; Bouchaud et al. 2009 "How Markets Slowly Digest Changes in Supply and Demand": impact $\propto \sigma\,(Q/V)^{1/2}$). The linear model is the *conservative-for-reasoning* baseline used in risk-adjusted measures because (i) it is closed-form and (ii) at the sizes at which L-VaR matters, the quadratic overstates less than the linear-per-share model understates. Square-root impact is treated in [[pillars/04-quantitative-risk/liquidity-risk-and-funding/06-advanced-extensions|06 · Advanced Extensions]] and in the Pillar 6 microstructure refs.

**2.3 The liquidation horizon.** If the order may not exceed a fraction $\alpha$ of average daily volume,
$$
T_{\text{liq}}=\frac{Q}{\text{ADV}\cdot\alpha}\quad(\text{days}).
$$
The **horizon-matched** market VaR is then $\mathrm{VaR}_T=z_\alpha\,\sigma_{\text{daily}}\sqrt{T_{\text{liq}}}\,V$ under i.i.d. scaling (Hull §22.4) - and the L-VaR must be evaluated at that horizon, not at 1 day. The FRTB makes this explicit: each risk factor gets a **liquidity horizon** (10/20/40/60/120 days) and the ES is computed on the scaled shock $\sigma\sqrt{LH/10}$.

**2.4 The combined measure.**
$$
\mathrm{LVaR}_\alpha=\mathrm{VaR}_{\text{market}}(\sigma,\,T_{\text{liq}})+\tfrac12 V\!\left(S+z_\alpha\sigma_S\right)+\frac{Q^2}{2D}.
$$

---

### 3. Computational Implementation - VaR, L-VaR, and the horizon

We decompose a \$10M position's 1-day 99% VaR into its three liquidity components, then show how each scales with the liquidation horizon. Stdlib only.




Interpretation: the impact cost (\$25,000, 25 bp) *exceeds* the exogenous spread cost (15.8 bp) even for this ~\$10M order - and total cost grows as $Q^2$, so a 5× larger order carries 5× the per-unit impact drag and ~25× the total impact cost. The horizon row shows the other multiplier: mis-specifying the horizon (1 day instead of 10) understates the market-risk term by $\sqrt{10}\approx3.16$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Ignoring the horizon, then compounding it.** Two separate errors live here: using a 1-day VaR for a position that takes 10 days to unwind (understates market risk by $\sqrt{10}$), *and* omitting the liquidation cost entirely. The two do not cancel; they add.
2. **Assuming the spread is constant.** $\text{LC}_{\text{exog}}=\tfrac12V(s+z_\alpha\sigma_s)$ prices the *correlation* between "I am forced to sell" and "the spread is wide." Setting $\sigma_s=0$ removes exactly the part that mattered in 2008.
3. **Linear impact at explosive sizes.** $\text{LC}_{\text{impact}}=\lambda Q^2/2$ understates for very large orders only if real impact is *super*-linear (it is not - it is sub-linear, square-root), so the quadratic model **overstates** for very large $Q$ and can be *conservative*; but the linear slope $\lambda$ is itself underestimated in calm periods, so the two errors run in opposite directions. Calibrate $\lambda$ from stress-period data, not calm data.
4. **Level, not path, thinking.** L-VaR prices the cost of *a* liquidation but treats the liquidation as one-shot. Patient execution (Almgren–Chriss optimal schedules) trades impact against timing risk; the realised cost can be above *or* below the static L-VaR depending on the path. See [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]].
5. **Non-coherence sneaks back in.** Adding a size-dependent cost $Q^2/2D$ (convex in $Q$) makes L-VaR *super*-additive in positions - the opposite of the subadditivity failure of plain VaR, and a reminder that "liquidity-adjusted" changes the aggregation properties that risk governance relies on.
6. **Currency of the horizon.** ADV and $D$ are themselves state-dependent; in a crisis ADV collapses and $D$ shrinks simultaneously, so $T_{\text{liq}}$ lengthens *and* $\text{LC}_{\text{impact}}$ rises - the two horizon terms move together (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Bangia, A., Diebold, F., Schuermann, T. & Stroughair, J.** - *Modeling Liquidity Risk, With Implications for Traditional Market Risk Measurement and Management* (1999/2000) - the canonical exogenous + endogenous L-VaR decomposition and its horizon scaling; the source of the $\tfrac12V(S+z_\alpha\sigma_S)$ form.
- **Almgren, R. & Chriss, N.** - *Optimal Execution of Portfolio Transactions*, *J. Risk* 3(2):5–39 (2000) - temporary vs permanent impact, the efficient frontier of impact vs timing risk. (Pillar 6 refs.)
- **Bouchaud, J.-P., Farmer, J.D. & Lillo, F.** - *How Markets Slowly Digest Changes in Supply and Demand* (2009) - square-root impact; the empirical shape behind §2.2's caveat. (Pillar 6 refs.)
- **Foucault, Pagano & Röell** - *Market Liquidity* (2013), Ch 2: effective/realized spread, price impact $\Delta m=\lambda q$, implementation shortfall (Perold 1988). *Verified in corpus.*
- **Hull** - *Risk Management and Financial Institutions*, liquidity-risk chapter (liquidity trading risk and L-VaR) and *Options, Futures and Other Derivatives* Ch 22.4 (the $\sqrt N$ scaling). *Corpus-verified for Ch 22.*
- **BCBS** - *FRTB: Minimum Capital Requirements for Market Risk* (2019, d457) - liquidity horizons and the ES scaling. (Pillar 4 refs.)

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/02-market-vs-funding-liquidity|02 · Market vs Funding Liquidity]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes]]
- Measure base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover Constraints]]
