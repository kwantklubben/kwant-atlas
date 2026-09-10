---
title: "03 — The Roll (1984) Model: Measuring the Effective Spread from Return Autocovariance"
tags:
  - pillar-market-making
  - spread-decomposition-and-roll-model
  - roll-model
  - autocovariance
  - ma1
  - efficient-market
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (autocovariance, MA(1), stationarity) and [[pillars/06-market-making/spread-decomposition-and-roll-model/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

The Roll (1984) model is the **zero point of spread measurement**: a paper that extracts the effective bid-ask spread from a *single* summary statistic of the price series — the first-order autocovariance of returns — under the minimal assumption that the efficient price is a random walk. No order book, no quotes, no trade-direction data. Just $p_t$, $p_{t-1}$, $p_{t-2}, \ldots$

The practical objective is sharp: **estimate the effective spread of an illiquid or opaque security from returns alone.** This is the classic tool for markets where quotes are unreliable or unavailable (dealer markets, options, corporate bonds), and it remains the benchmark every fancier estimator is compared against.

The trick, again: trades bounce between bid and ask, so consecutive price changes are *negatively* autocorrelated, and the size of that negative correlation is exactly $c^2$ where $c$ is the half-spread. Measure the covariance, take a square root, done.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The model (Hasbrouck 2007, Ch 3)

The efficient price follows a random walk with **no drift** (microstructure horizon; drift is negligible):

$$m_t = m_{t-1} + u_t, \qquad u_t \sim \text{i.i.d.}(0,\sigma_u^2).$$

Trade direction $q_t\in\{-1,+1\}$ is i.i.d. with $\mathbb{P}(q_t=+1)=\mathbb{P}(q_t=-1)=\tfrac12$, independent of $u_t$. The dealer charges a constant half-spread $c$ per trade; the trade price is

$$p_t = m_t + q_t\,c.$$

So a buy prints at $m_t+c$ (the ask), a sell at $m_t-c$ (the bid), and the **quoted/effective spread is $2c$**. The observed price change is

$$\Delta p_t = u_t + c\,(q_t-q_{t-1}).$$

#### 2.2 The moments and the estimator

Take variances and the first autocovariance (Hasbrouck eqs 3.4–3.5):

$$\gamma_0 \equiv \mathrm{Var}(\Delta p_t) = 2c^2+\sigma_u^2,$$
$$\gamma_1 \equiv \mathrm{Cov}(\Delta p_{t-1},\Delta p_t) = -c^2,$$
$$\gamma_k = 0 \quad \forall\, k\ge 2.$$

All higher autocovariances vanish because $q_t$ is i.i.d. and independent of $u_t$. Inverting:

$$\boxed{\;c = \sqrt{-\gamma_1}\;, \qquad S = 2\sqrt{-\gamma_1}\;, \qquad \sigma_u^2 = \gamma_0 + 2\gamma_1.}$$

**Interpretation.** The efficient-price innovation variance is $\gamma_0+2\gamma_1$ — because the two-covariance correction removes the bounce variance $2c^2$ from the total return variance, leaving only the true (random-walk) component. This is precisely the univariate random-walk decomposition: Roll splits observed return variance into a permanent part $\sigma_u^2$ and a transitory (bounce) part $2c^2$.

#### 2.3 Empirical calibration anchor (Hasbrouck Ch 3)

For Price Communications Oct 2003, the sample autocovariance was $\hat\gamma_1=-0.0000294$, giving $c=\$0.017$, spread $=\$0.034$ — close to the time-weighted NYSE average spread of $\$0.032$. A perfect worked example of the formula on real data.

#### 2.4 Connection to MA(1) (Hasbrouck Ch 4)

Because only $\gamma_0$ and $\gamma_1$ are nonzero, the differenced series is an **MA(1)**: $\Delta p_t=\varepsilon_t+\theta\varepsilon_{t-1}$ with

$$\gamma_0=(1+\theta^2)\sigma_\varepsilon^2,\qquad \gamma_1=\theta\,\sigma_\varepsilon^2,\qquad
\theta=\frac{\gamma_0-\sqrt{\gamma_0^2-4\gamma_1^2}}{2\gamma_1}\ \text{(invertible, }|\theta|<1).$$

The Wold theorem guarantees the MA(1) representation exists, and the Roll model is the structural story underneath that single moving-average parameter. This is the formal bridge to the time-series machinery of [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]].

---

### 3. Computational Implementation — recover the spread from a price series

Simulate a Roll process with a known spread, compute the autocovariance, and recover the spread. Also verify the variance decomposition $\sigma_u^2=\gamma_0+2\gamma_1$. Stdlib only.

```python
import math, random

random.seed(1234)
def simulate_roll(n=20000, spread=0.05, sig_u=0.01):
    c = spread/2.0; m = 100.0; ps = []
    for _ in range(n):
        m += random.gauss(0, sig_u)
        q = random.choice([-1, 1])
        ps.append(m + q*c)
    return ps

def roll_estimate(prices):
    dp = [prices[i]-prices[i-1] for i in range(1, len(prices))]
    n = len(dp); mean = sum(dp)/n
    g0 = sum((x-mean)**2 for x in dp)/n
    g1 = sum((dp[i]-mean)*(dp[i-1]-mean) for i in range(1, n))/n
    if g1 < 0:
        return 2.0*math.sqrt(-g1), g0, g1
    return None, g0, g1

for true in (0.05, 0.02):
    est, g0, g1 = roll_estimate(simulate_roll(spread=true))
    sig2 = g0 + 2*g1                      # efficient innovation variance (true sig_u^2 = 0.0001)
    print(f"true spread {true:.3f}: gamma0={g0:.7f}  gamma1={g1:.7f}  "
          f"Roll spread={est:.5f}  sigma_u^2={sig2:.5f}")
```
```
true spread 0.050: gamma0=0.0013456  gamma1=-0.0006227  Roll spread=0.04991  sigma_u^2=0.00010
true spread 0.020: gamma0=0.0002949  gamma1=-0.0000976  Roll spread=0.01976  sigma_u^2=0.00010
```

The estimator recovers spreads of $0.05$ and $0.02$ to within a few basis points of error, and recovers the true efficient innovation variance $\sigma_u^2=0.0001$ (i.e. $\sigma_u=0.01$) from $\gamma_0+2\gamma_1$ — exactly the random-walk decomposition.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Positive autocovariance kills the estimator.** Roll needs $\gamma_1<0$. If genuine persistence in $u_t$ (momentum, clustering) outweighs the $-c^2$ bounce, $\gamma_1$ goes positive and $\sqrt{-\gamma_1}$ is undefined. This is the most common real-data failure (Harris 1990: positive $\hat\gamma_1$ is common).
2. **Serial-correlated order flow biases it down.** Buys-follow-buys ($\mathrm{corr}(q_t,q_{t-1})=\rho>0$) changes the autocovariance to $-c^2(1-2\rho)$, so Roll **underestimates** the spread (Hasbrouck Ex 4.2).
3. **Information correlated with trade direction biases it up.** If $\mathrm{corr}(q_t,u_t)>0$ (informed traders), $\gamma_1=-c(c+\rho\sigma_u)$, so Roll **overestimates** (Hasbrouck Ex 4.3).
4. **Non-constant spread / non-stationarity.** Roll assumes a fixed spread; a time-varying spread (wider in volatility, narrower in calm) contaminates the single autocovariance. Overnight gaps must be excluded (drop overnight changes; insert missing values at day breaks).

Full dissections with numbers in [[pillars/06-market-making/spread-decomposition-and-roll-model/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 5. Canonical Literature & Study References

- **Roll (1984)**, *A simple implicit measure of the effective bid-ask spread in an efficient market*, Journal of Finance 39(4), 1127–1139 — the original.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 3 (model & formulas) and Ch 4 (MA(1), Wold, estimation, bias exercises) — *verified per-chapter in the corpus*.
- **Harris (1990)**, *Statistical properties of the Roll serial covariance bid/ask spread estimator*, Journal of Financial Economics 27(2), 305–329 — on the positive-autocovariance problem and estimation.
- **Niederhoffer & Osborne (1966)**, *Market making and reversal on the stock exchange* — the empirical precursor documenting bid-ask bounce.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/spread-decomposition-and-roll-model/01-from-zero-intuition|01 · From Zero]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/02-quoted-effective-realized|02 · Quoted / Effective / Realized]]
- Forward: [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/06-advanced-extensions|06 · Advanced Extensions]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (autocovariance, MA(1)) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (martingale)
