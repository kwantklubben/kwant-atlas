---
title: "1.1.6 Advanced Extensions"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - johansen
  - vecm
  - optimal-stopping
  - kalman-filter
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/02-cointegration-and-the-spread|02 · Cointegration & the Spread]] and [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/04-trading-rules-and-backtest|04 · Trading Rules & Backtest]].

---

### 1. Intuition & Practical Objective

Three extensions take StatArb beyond the two-asset t-test:

1. **Johansen's multivariate test** - instead of a *pair*, allow a *basket* and ask "how many* independent equilibrium relationships exist?" (the cointegrating rank). This is the correct tool when several assets share the same factors and you do not want to pre-pick a pair.
2. **Optimal stopping / stochastic control of the OU spread** - instead of fixed $2\sigma$ thresholds, solve for the thresholds that maximise expected return per unit time net of costs.
3. **Dynamic hedging (Kalman filter)** - replace the static OLS $\beta$ with a time-varying $\beta_t$ estimated recursively, so the hedge adapts when the relationship drifts (the bridge to [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]]).

All three keep the OU spread at the centre; they differ in how many assets and how much structure they assume.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Johansen procedure (Tsay §8.6.2–8.6.3; Johansen 1988/1991)

Start from a VAR($p$) in levels and rewrite it in **error-correction** form for a $k$-dimensional $I(1)$ vector $x_t$:

$$
\Delta x_t=\Pi x_{t-1}+\sum_{i=1}^{p-1}\Gamma_i\Delta x_{t-i}+a_t,\qquad \Pi=\sum_{i=1}^{p}\Phi_i-I=-\Phi(1).
$$

The **rank of $\Pi$ is the cointegrating rank** $m$: $\Pi=\alpha\beta'$, with $\beta$ ($k\times m$) the cointegrating vectors and $\alpha$ the adjustment speeds.

**Estimation (the reduced-rank regression).** Run two auxiliary regressions and collect residuals:

$$
R_{0t}=\Delta x_t-\text{proj on }(\Delta x_{t-1},\dots),\qquad R_{1t}=x_{t-1}-\text{proj on }(\Delta x_{t-1},\dots).
$$

Form the moment matrices $S_{ij}=\tfrac1T\sum_t R_{it}R_{jt}'$, and solve the **generalised eigenvalue problem**

$$
\big|\lambda S_{11}-S_{10}S_{00}^{-1}S_{01}\big|=0\;\Longrightarrow\;\hat\lambda_1\ge\dots\ge\hat\lambda_k.
$$

The cointegrating vectors are the eigenvectors, normalised so $e'S_{11}e=I$.

**Tests (H0: rank $=m$).** Two standard statistics, with nonstandard (Brownian-motion) critical values:

$$
LR_{\text{tr}}(m)=-(T-p)\sum_{i=m+1}^{k}\ln(1-\hat\lambda_i)\quad\text{(rank}=m\text{ vs }>m),
$$

$$
LR_{\max}(m)=-(T-p)\ln(1-\hat\lambda_{m+1})\quad\text{(rank}=m\text{ vs }m+1).
$$

For $k=2$ with a restricted constant, the 95% critical values are $\approx15.41$ (rank $\le0$) and $\approx3.76$ (rank $\le1$): reject "no cointegration" if the first exceeds $15.41$, and fail to reject rank 1 if the second is below $3.76$.

#### 2.2 Multivariate StatArb (Avellaneda–Lee "generalized pairs trading")

Trade a stock against a *weighted portfolio* (basket) rather than a single peer. With factors $F_j$ and residuals $\tilde R_i=R_i-\sum_j\beta_{ij}F_j$, the "generalized" spread is the idiosyncratic residual $\tilde R_i$, and the same OU/z-score machinery applies per stock. Market-neutrality $\sum_i\beta_{ij}Q_i=0$ holds at the book level, so the net factor exposure cancels.

#### 2.3 Optimal stopping / thresholds (Elliott, van der Hoek & Malcolm 2005; Bertram 2010)

Model the spread as an OU process and the trade as a **first-passage problem**: enter at level $a$, exit at level $m$ ($a<m$ for a long-spread trade). The cycle time $T=T_1+T_2$ (entry→exit + exit→next entry) is random; the return per cycle is deterministic, $r(a,m,c)=m-a-c$ with cost $c$. By renewal theory the expected return and variance per unit time are

$$
\mu(a,m,c)=\frac{r(a,m,c)}{\mathbb{E}[T]},\qquad \sigma^2(a,m,c)=\frac{r^2(a,m,c)\operatorname{Var}(T)}{\mathbb{E}^3[T]},
$$

and $\mathbb{E}[T],\operatorname{Var}(T)$ come from the **first-passage-time density of the OU process** (Itô-transformed to a dimensionless system). Maximising a Sharpe-type objective over $(a,m)$ yields the optimal thresholds - recovering the fixed $2\sigma$ rule as a special (suboptimal-in-general) case.

#### 2.4 Dynamic hedge ratio (Kalman filter)

Let $\beta_t$ follow a random walk $\beta_t=\beta_{t-1}+w_t$ with observation $y_t=\alpha+\beta_t x_t+v_t$. The Kalman filter gives the one-step-ahead estimate $\hat\beta_{t|t-1}$; use it as the hedge ratio so the spread is $z_t=y_t-\hat\beta_{t|t-1}x_t$. This turns the static cointegration regression into an adaptive one - essential when $\beta$ drifts slowly (see the sibling topic for the full state-space derivation).

---

### 3. Computational Implementation - the Johansen trace test

Stdlib only. We simulate a genuine cointegrated bivariate system (random walk $x_1$, and $x_2=0.9\,x_1+$ stationary) so the true rank is **1**, then run the full Johansen reduced-rank regression with a 2×2 analytic generalised-eigenvalue solve.




The procedure recovers the simulated rank exactly: the first trace statistic ($103.14$) is far above its critical value (reject "no cointegration"), while the second ($3.12$) sits below $3.76$ (a second vector is not supported). The estimated $\hat\lambda_1=0.0983$ is a measure of how strongly the equilibrium is restored by the error-correction term.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Johansen critical values depend on the deterministic spec.** The five cases (no constant, restricted constant, unrestricted constant, restricted/unrestricted trend; Tsay §8.6.1) have *different* tables. Resembling the wrong table invalidates the rank conclusion.
2. **Rank ≠ profitability.** A system can have rank 1 with an unfavourably *slow* adjustment ($\alpha$ small) or a spread whose $\sigma_{\text{eq}}$ is tiny relative to costs - econometrically cointegrated, economically untradeable.
3. **Basket legibility.** Trading a stock against a *basket* multiplies transaction costs and creates netting and borrow complexity; Avellaneda–Lee rely on the net ETF position being small, which need not hold in stress.
4. **Optimal-stopping thresholds assume stationarity.** The Elliott/Bertram solution is only optimal under a *fixed* OU; the moment the parameters drift or the equilibrium breaks, the "optimal" thresholds are worse than a plain stop.
5. **Kalman $\beta$ can chase noise.** If the state-noise variance is set too high, the hedge ratio over-fits recent co-movement and the spread becomes white noise by construction (a filter artefact, not cointegration).
6. **The nested risk.** These extensions add parameters to a problem whose *core* risk (structural break, Ch 5) they do not fix. More machinery is not robustness.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 8 §8.6.2 (Johansen MLE, auxiliary regressions Eq. 8.40–8.41, eigenvalues), §8.6.3 (trace Eq. and max-eigenvalue tests; TB3m/TB6m trace $83.27$ vs 95% CV $19.96$), §8.7 (3-regime threshold cointegration). *Math-verified in the corpus.*
- **Johansen, S.**, "Statistical Analysis of Cointegration Vectors", *Journal of Economic Dynamics and Control* 12(2–3), 1988; and *Econometrica* 59(6), 1991.
- **Avellaneda, M. & Lee, J.-H.**, *Quantitative Finance* 10(7), 2010 - §1 "generalized pairs-trading", §2 PCA/eigenportfolios.
- **Elliott, R. J., van der Hoek, J. & Malcolm, W. P.**, "Pairs Trading", *Quantitative Finance* 5(3), 2005 - OU optimal stopping.
- **Krauss, C.**, *J. Economic Surveys* 31(2), 2017 - §5 stochastic-control approach (Bertram renewal-theory thresholds, Eq. 23–25).
- **Harvey, A. C.**, *Forecasting, Structural Time Series Models and the Kalman Filter* - the state-space machinery for time-varying $\beta$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] (dynamic hedge ratio) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (factor choice for residuals)
- Foundations: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] (for the OU first-passage solution)
- Cross-pillar: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]
