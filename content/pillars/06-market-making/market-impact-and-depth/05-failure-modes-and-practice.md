---
title: "6.7.5 Measuring Impact"
tags:
  - pillar-market-making
  - market-impact
  - measurement
  - ofi
  - amihud
  - failure-modes
---

**Basic Prerequisites:** [[pillars/06-market-making/market-impact-and-depth/04-the-square-root-law|04 · The Square-Root Law]] and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (regression, robustness).

---

### 1. Intuition & Practical Objective

Theory gives you $\lambda$, depth and a square-root cost function. **Practice asks: how do I measure these from data, and where does the measurement lie?** This page is the folder's bridge from model to desk: the canonical estimators of market impact, what each one is actually measuring, and the failure modes that make them disagree.

The practical objective is narrow and crucial: given a trade (or a strategy), produce an honest **estimate of its cost** - and know which of the following you are holding: an *impact coefficient* ($\lambda$, a price move per unit flow), an *impact cost* ($I,J$, dollars per share), or an *illiquidity proxy* (a scaled return per dollar volume). They are different objects, measured differently, and the most common estimating errors are category errors between them.

Three estimation families, in increasing order of data hunger:

1. **Regression on order flow** - regress price changes on signed order flow or its imbalance (Hasbrouck's trade VAR; Cont et al.'s OFI). Yields $\lambda$ directly.
2. **Metaorder cost studies** - observe real large orders, split the effect into pre-/post-trade and realized prices, fit power laws (Almgren et al. 2005). Yields $I,J$ and the exponents.
3. **Low-frequency illiquidity proxies** - Amihud, Amivest, Roll's covariance. Cheap to compute on daily data, but one step removed from the mechanism.

> **The one-sentence essence.** "Impact is measured either as a *flow coefficient* from high-frequency regressions, as a *cost function* from observed metaorders, or as a *proxy* from daily returns and volume - and confusing these three is the failure mode this page exists to prevent."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The high-frequency regression route

**Order flow imbalance (OFI)** - Cont, Kukanov & Stoikov (2014). Over a short interval, define the imbalance between supply and demand at the best quotes as the net change in the queue at the best bid minus the best ask (each event - a limit order, a cancel, or a market order - contributes to one side). The empirical finding:

$$
\Delta P \;=\; \lambda_{\mathrm{OFI}}\cdot \mathrm{OFI} + \varepsilon,\qquad \boxed{\ \lambda_{\mathrm{OFI}}\ \propto\ \frac{1}{\text{depth}}\ }
$$

- a **linear** relation, robust across stocks and time scales, with a slope that is **inversely proportional to market depth**. This is the practical face of Kyle's $\lambda$: the same concept, estimated from the book rather than assumed. Other things being equal, a market with twice the depth has half the impact coefficient.

**Hasbrouck's trade VAR** is the sibling route: regress the efficient-price innovation on signed trades to estimate the *permanent* impact $\lambda$, and use the price/quote relationship to recover the transitory $c$ (the generalized Roll decomposition, eq. 8.2). The two quantities map exactly onto the temporary/permanent split of page 03.

#### 2.2 The metaorder route (Almgren et al. 2005)

For each observed order, record three prices: the **pre-trade** price $S_0$ (before impact), the **post-trade** price $S_{\text{post}}$ (after temporary effects have dissipated), and the **average execution** price $\bar S$. Then

$$
\text{Permanent impact } I=\frac{S_{\text{post}}-S_0}{S_0},\qquad
\text{Realized impact } J=\frac{\bar S-S_0}{S_0},
$$

and the *temporary* impact is recovered as $J$ minus a fraction of $I$ (half, for a constant-rate program). Regress these on order size and duration in **volume time**, fit power laws, and you get the $I,J$ formulas and $\gamma,\eta$ of page 04. The critical design choice is **volume time** (fraction of an average day's volume elapsed), which removes the intraday U-shape in volume and volatility; a naive clock-time regression mixes the two.

#### 2.3 Daily illiquidity proxies

- **Amihud (2002):** $I=\mathbb E\!\left[\dfrac{|r_t|}{\text{Vol}_t}\right] - the absolute return per dollar traded. Better as a \lambda$ proxy than the inverse ratio (Hasbrouck §9.9).
- **Amivest / liquidity ratio:** $L=\dfrac{\text{Vol}_t}{|r_t|}$ - dollars of volume per unit return (the reciprocal idea).
- **Roll (1984):** effective spread $=2\sqrt{-\gamma_1}$ from the first autocovariance of price changes - a *spread* proxy, not an impact proxy, and biased by serial correlation in order flow.

All three are computable from daily data, which is exactly their danger: they mix impact with volatility, spread and discrete pricing, and they cannot distinguish temporary from permanent.

---

### 3. Computational Implementation - OFI regression and depth

Simulate an event stream where the mid-price change is linear in OFI with a slope set by depth, recover $\lambda_{\mathrm{OFI}}$ by OLS, and watch it fall as depth rises. Then compute an Amihud proxy. Stdlib only.





The OLS slope tracks $1/(2\,\text{depth})$ to five decimals at every depth - the empirical content of "price impact is inversely proportional to the depth of the order book." The Amihud proxy is on a completely different (per-dollar) scale, which is precisely why the three families must not be conflated.

**A practical measurement checklist.**
1. **Sign your trades** (Lee–Ready 1991) before any flow regression - an unsigned regression attenuates $\lambda$ toward zero.
2. **Use mid-quote changes**, not trade-price changes, as the dependent variable: trade prices carry the bid-ask bounce (temporary $c$), quote midpoints do not and have lower short-run transient volatility (Hasbrouck §9.7).
3. **Estimate in event time**, not wall-clock time, when flow is the regressor.
4. **Use volume time** for metaorder studies (Almgren et al.).
5. **Average over many metaorders** - single-order $R^2$ is under 1% because volatility dominates.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Bid-ask bounce contaminates the impact estimate.** Regressing *trade-price* changes on signed flow captures the transitory $c(q_t-q_{t-1})$ term as if it were impact, inflating $\lambda$. Fix: use quote midpoints, or use the generalized-Roll system that separates $c$ from $\lambda$ structurally.
2. **Endogeneity: prices cause flow as well as flow cause prices.** Momentum traders buy after price rises, so the OLS coefficient is not purely causal. Instrumental-variable or event-based designs are needed; a naive regression overstates persistent impact.
3. **Volume is a noisy, less robust regressor than OFI.** Cont et al. show traded volume explains price changes worse than OFI; volume is a convex transform of order flow and adds noise. Prefer OFI (or signed flow).
4. **Model misspecification by functional form.** Fitting linear impact to square-root data, or an exponential impact-decay kernel, is not a small error: the former biases large-order costs, the latter admits arbitrage (page 04, Gatheral).
5. **Category errors across the three families.** Equating an Amihud ratio (per dollar) with an OFI $\lambda$ (per share of flow) with a metaorder $J$ (per share of size) is dimensionally wrong and is the most common spreadsheet-level mistake. Always carry units.
6. **Ignoring intraday seasonality.** Depth, spread and OFI slope all follow a U-shape (wide/deep at open and close, thin at midday); a full-day average hides this and mis-prices trades scheduled at the wrong time.
7. **Non-stationarity.** $\lambda$ changes with volatility regimes, news, and structural breaks in the market's composition. A $\lambda$ estimated in a calm regime under-charges in a stressed one - and impact estimation is exactly when stressed regimes matter most.

---

### 5. References

- **Cont, R., Kukanov, A. & Stoikov, S. (2014)**, *The price impact of order book events*, J. Financial Econometrics 12(1), 47–88. *OFI definition, linear relation, slope $\propto1/$depth, robustness. Primary PDF in corpus (`04Cont2014_...`).*
- **Almgren, R., Thum, C., Hauptmann, H. & Li, H. (2005)**, *Direct estimation of equity market impact*, Risk 18(7), 57–62. *Pre-trade/post-trade/realized prices, volume time, power-law fitting, $\gamma,\eta$. Primary PDF in corpus.*
- **Hasbrouck, J. (2007)**, *Empirical Market Microstructure*
- **Amihud, Y. (2002)**, *Illiquidity and stock returns*, J. Financial Markets 5(1), 31–56. *The illiquidity ratio. Primary PDF in corpus.*
- **Lee, C. & Ready, M. (1991)**, *Inferring trade direction from intraday data*, J. Finance 46(2), 733–746. *The trade-signing prerequisite for any flow regression.*
- **Roll, R. (1984)**, *A simple implicit measure of the effective bid-ask spread*, J. Finance 39(4), 1127–1139. *The autocovariance spread proxy and its bias directions.*
- **Glosten, L. R. & Harris, L. E. (1988)**, *Estimating the components of the bid/ask spread*, JFE 21(1), 123–142. *Structural transitory/permanent estimation with size dependence.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-impact-and-depth/04-the-square-root-law|04 · The Square-Root Law]] · [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|03 · Temporary vs Permanent]]
- Forward: [[pillars/06-market-making/market-impact-and-depth/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/06-market-making/market-impact-and-depth/index|Index Hub]]
- Related: [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (OFI construction) · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] (the same signing machinery) · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]] (Amihud as a priced factor)
