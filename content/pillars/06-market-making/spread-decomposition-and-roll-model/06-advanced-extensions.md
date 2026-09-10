---
title: "06 — Advanced Extensions: Generalized Roll, Random-Walk Decomposition & Price Impact"
tags:
  - pillar-market-making
  - spread-decomposition-and-roll-model
  - generalized-roll
  - random-walk-decomposition
  - beveridge-nelson
  - price-impact
  - var
---

**Basic Prerequisites:** [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]], [[pillars/06-market-making/spread-decomposition-and-roll-model/05-failure-modes-and-practice|05 · Failure Modes]], and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (MA/VAR, cointegration).

---

### 1. Intuition & Practical Objective

The plain Roll model is univariate: prices only. This page is the **launchpad** to the modern toolkit that fixes its limits — (1) the **generalized Roll model** (Hasbrouck Ch 8) that splits the spread into $c$ (transitory) and $\lambda$ (permanent/price-impact), (2) the **random-walk / permanent-transitory decomposition** (Beveridge–Nelson 1981; Watson 1986) that separates the efficient price from the pricing error, and (3) the **multivariate VAR / price-impact** machinery (Hasbrouck Ch 9) that measures $\lambda$ directly from the trade-innovation response.

> **Why these first?** They are the *measurement completion* of Roll: Roll gives the total spread; these give its *components* and its *permanent vs transitory* split. Everything farther — Hasbrouck information shares across venues, PIN/VPIN, structural adverse-selection models — links from here.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The generalized Roll model (Hasbrouck Ch 8)

Let the efficient price be driven by both public information $u_t$ and the information content of the trade itself, $\lambda q_t$:

$$p_t = m_t + c\,q_t, \qquad m_t = m_{t-1} + \lambda q_t + u_t.$$

Here $c$ = non-informational (order-processing/inventory) cost, $\lambda$ = adverse-selection / price-impact cost. The bid/ask straddles $m_{t-1}+u_t$, and the **spread is $2(c+\lambda)$**. Differencing:

$$\Delta p_t = c\,(q_t-q_{t-1}) + \lambda q_t + u_t,$$
$$\gamma_0 = c^2 + (c+\lambda)^2 + \sigma_u^2, \qquad \gamma_1 = -c\,(c+\lambda).$$

**The central identification result:** only two autocovariances are observable, but there are three structural parameters $\{c,\lambda,\sigma_u^2\}$ — so the components are **under-identified from prices alone**. However, the random-walk innovation variance

$$\boxed{\;\sigma_w^2 \equiv \lambda^2+\sigma_u^2 = \gamma_0+2\gamma_1\;}$$

**is identified**, because it is the permanent component and does not depend on the bounce. This is the economic reason the permanent/transitory split is recoverable while the spread components are not.

#### 2.2 Random-walk (Beveridge–Nelson / Watson) decomposition

Any covariance-stationary $\Delta p_t$ is an MA(1) (Wold): $\Delta p_t=\varepsilon_t+\theta\varepsilon_{t-1}$. The Beveridge–Nelson decomposition writes $p_t=m_t+s_t$ where $m_t$ is the random-walk (permanent) component and $s_t$ is the stationary pricing error:

$$\sigma_w^2 = (1+\theta)^2\,\sigma_\varepsilon^2 \qquad\text{(permanent innovation variance)},$$
$$\sigma_s^2 = \theta^2\,\sigma_\varepsilon^2 \qquad\text{(lower bound on the pricing-error variance)}.$$

In the pure Roll case, $\sigma_w^2=\sigma_u^2$ and the *actual* pricing-error variance is $\mathrm{Var}(p_t-m_t)=c^2$, attained by the bound $\theta^2\sigma_\varepsilon^2$ only when $\sigma_u^2=0$ (in Roll, $c^2=\theta\sigma_\varepsilon^2>\theta^2\sigma_\varepsilon^2$). The decomposition is **invariant to the identification** of the MA parameters — a strong robustness property.

#### 2.3 Variance ratio

The variance ratio compares variances over different horizons:

$$V_{M,N}=\frac{\mathrm{Var}(p_t-p_{t-M})/M}{\mathrm{Var}(p_t-p_{t-N})/N}.$$

With microstructure (bid-ask bounce) inflating the *short* horizon variance, for $M>N$ (longer horizon in numerator) one gets $V_{M,N}<1$, declining toward $1$ as the horizon grows and the transitory component washes out. A ratio below 1 is the signature of a transitory (pricing-error) component in the price.

#### 2.4 Multivariate price impact (Hasbrouck Ch 9) — the empirical route to $\lambda$

Stack the price change and trade variables into $y_t=[\Delta p_t,\ x_t']'$ and fit a VAR; the impulse response of $\Delta p$ to a trade-innovation $v_t$ measures $\lambda$ directly. Structural form:

$$q_t = v_t+\beta v_{t-1}\ \ (\text{MA(1) order flow}), \qquad w_t = u_t+\lambda v_t,$$
$$\Delta p_t = u_t + \lambda v_t + c\,[(v_t+\beta v_{t-1})-(v_{t-1}+\beta v_{t-2})].$$

The permanent/trade-driven variance splits as $\sigma_w^2=\sigma_u^2+\lambda^2\sigma_v^2$, where $\lambda^2\sigma_v^2$ is the **absolute information content of trade flow** and $\lambda^2\sigma_v^2/\sigma_w^2$ the relative share (≈ $R^2$ of price changes on trades). This is the bridge to [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] and to price discovery across venues.

---

### 3. Computational Implementation — the decomposition in numbers

Recover the MA(1) parameters from the sample autocovariances, then split the price into permanent (random-walk) and transitory (pricing-error) components, and confirm the permanent variance equals $\gamma_0+2\gamma_1$. Stdlib only.

```python
import math, random, statistics as st
random.seed(8181)

def simulate_roll(n=50000, spread=0.05, sig_u=0.01):
    c = spread/2.0; m = 100.0; ps = []
    for _ in range(n):
        m += random.gauss(0, sig_u)
        ps.append(m + random.choice([-1, 1])*c)
    return ps

prices = simulate_roll()
dp = [prices[i]-prices[i-1] for i in range(1, len(prices))]
n = len(dp); mean = sum(dp)/n
g0 = sum((x-mean)**2 for x in dp)/n
g1 = sum((dp[i]-mean)*(dp[i-1]-mean) for i in range(1, n))/n

disc  = math.sqrt(g0*g0 - 4*g1*g1)                 # invertible MA(1)
theta = (g0 - disc)/(2*g1); se2 = (g0 + disc)/2
sw2   = (1+theta)**2*se2                            # permanent innovation variance (B-N)
perr  = theta**2*se2                                # pricing-error (bounce) variance
print(f"gamma0={g0:.7f}  gamma1={g1:.7f}")
print(f"MA(1): theta={theta:.4f}  sigma_e^2={se2:.7f}")
print(f"permanent variance sw2 = {sw2:.6f}   (check gamma0+2*gamma1 = {g0+2*g1:.6f})   true su2 = {0.01**2:.6f}")
print(f"pricing-error variance  = {perr:.6f}   (bounce ~ c^2 = {0.025**2:.6f})")

dp10 = [prices[i]-prices[i-10] for i in range(10, len(prices))]
vr   = (st.pvariance(dp10)/10)/g0                  # V(10,1): longer in numerator
print(f"variance ratio V(10,1) = {vr:.4f}   (< 1 => transitory bounce inflates 1-period variance)")
```
```
gamma0=0.0013522  gamma1=-0.0006322
MA(1): theta=-0.6902  sigma_e^2=0.0009159
permanent variance sw2 = 0.000088   (check gamma0+2*gamma1 = 0.000088)   true su2 = 0.000100
pricing-error variance  = 0.000436   (bounce ~ c^2 = 0.000625)
variance ratio V(10,1) = 0.1630   (< 1 => transitory bounce inflates 1-period variance)
```

The permanent (random-walk) innovation variance $0.000088$ matches $\gamma_0+2\gamma_1$ and recovers the true efficient $\sigma_u^2=0.0001$; the pricing-error variance $0.000436$ approximates the bounce $c^2$. The variance ratio below 1 is the empirical signature of the transitory component.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading components out of prices alone.** $\{c,\lambda,\sigma_u^2\}$ are under-identified from autocovariances; only $\sigma_w^2$ is. Any claim to have separated order-processing from adverse-selection using only a price tape is either an extra assumption or an error.
2. **Variance-ratio sign confusion.** The ratio is *less* than 1 when the *shorter* horizon is inflated (bounce); ">1 means microstructure noise" only when the short horizon is in the numerator. State $M,N$ explicitly.
3. **VAR identification is ordering-dependent.** The Cholesky decomposition that splits $\sigma_w^2$ into public vs trade information depends on the causal ordering; report bounds or justify the ordering (the same caveat that drives Hasbrouck information shares).
4. **Trade signing.** $\lambda$ estimation needs correct aggressor-side signing (Lee–Ready). Mis-signed flow attenuates or reverses the price-impact estimate (see [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]).

---

### 5. Canonical Literature & Study References

- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 8 (generalized Roll, $\sigma_w^2=\gamma_0+2\gamma_1$, variance ratio, B–N decomposition) and Ch 9 (multivariate VAR, price impact, $\lambda^2\sigma_v^2$ info measure) — *verified per-chapter in the corpus*.
- **Beveridge & Nelson (1981)**, *A new approach to decomposition of economic time series into permanent and transitory components*, Journal of Monetary Economics 7(2) — the permanent/transitory split.
- **Watson (1986)**, *Univariate detrending methods with stochastic trends*, Journal of Monetary Economics 18(1).
- **Huang & Stoll (1997)**, *The components of the bid-ask spread: a general approach*, RFS 10(4) — the structural three-component model underlying Ch 8's measurement.
- **Hasbrouck (1991)**, *Measuring the information content of stock trades*, Journal of Finance 46(1) — the trade-innovation VAR, the empirical route to $\lambda$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/05-failure-modes-and-practice|05 · Failure Modes]]
- Forward topic pages: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] (structural $\lambda$) · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] (signing, PIN) · [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics & L3 Data]] (trade/quote data)
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (MA/VAR, Wold, cointegration) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (martingales)
- Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]] (price impact in execution cost)
