---
title: "Statistical Arbitrage & Pairs Trading"
tags:
  - pillar-quant-research
  - stat-arb
  - cointegration
  - mean-reversion
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (Stationarity, Unit Roots, Engle–Granger Cointegration).

---

### 1. Intuition & Practical Objective

Pairs trading and statistical arbitrage (StatArb) do not seek to predict the absolute direction of the macro market. Instead, they exploit relative mispricings between economically linked assets.

If two assets share common fundamental drivers (e.g., Chevron and ExxonMobil, or Royal Dutch Shell Class A and Class B), their price ratio or linear spread should fluctuate around a stable long-term equilibrium. When idiosyncratic market flow pushes the spread temporarily apart, a StatArb strategy shorts the expensive asset and buys the cheap asset, capturing the spread's convergence back to equilibrium.

---

### 2. Mathematical Ground Truth & Derivations

#### Cointegration vs Correlation
Two asset prices $P_t^A$ and $P_t^B$ can have high correlation ($> 0.95$) over a single year yet diverge permanently if their trends drift apart. Cointegration is a property of the *spread*, not the returns:
$$P_t^A = \alpha + \beta P_t^B + z_t$$
where $P_t^A, P_t^B \sim I(1)$ (non-stationary random walks), but the residual spread $z_t \sim I(0)$ (strictly stationary with constant mean 0 and finite variance $\sigma_z^2$).

#### Ornstein–Uhlenbeck (OU) Mean-Reverting Spread Dynamics
The continuous-time spread $z_t$ is modeled as an Ornstein–Uhlenbeck process:
$$d z_t = \theta (\mu - z_t) dt + \sigma_z dW_t$$
- $\theta > 0$: Speed of mean reversion.
- $\mu$: Long-term equilibrium level (typically normalized to 0).
- $\sigma_z$: Diffusion volatility.

Discretizing via Euler–Maruyama over time step $\Delta t$:
$$z_{t} - z_{t-1} = \theta \mu \Delta t - \theta z_{t-1} \Delta t + \epsilon_t = a + b z_{t-1} + \epsilon_t$$
where $b = -\theta \Delta t$. From the OLS estimate $\hat{b}$:
$$\theta = -\frac{\ln(1 + \hat{b})}{\Delta t}$$
The **half-life of mean reversion** (time required for the spread to decay to half its displacement) is:
$$\tau_{1/2} = \frac{\ln(2)}{\theta}$$

#### Trading Signal Generation
We normalize the spread into a dimensionless $Z$-score:
$$Z_t = \frac{z_t - \text{EMA}(z_t)}{\text{StdDev}(z_t)}$$
- **Enter Short Spread (Short A, Long $\beta$ B):** $Z_t > +2.0$
- **Enter Long Spread (Long A, Short $\beta$ B):** $Z_t < -2.0$
- **Exit / Flatten Position:** $|Z_t| \le 0.5$
- **Stop-Loss Exit:** $|Z_t| \ge 3.5$ (indicates cointegration breakdown)

---

### 3. Computational Implementation


> **Requires `statsmodels`** (`pip install statsmodels`) — this block is not stdlib-only, unlike most of the Atlas. Left in place as a superseded *original note*; the topic-folder above is the maintained version.
```python
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

class StatArbPair:
    def __init__(self, p1: np.ndarray, p2: np.ndarray):
        self.p1 = p1
        self.p2 = p2
        self.beta = None
        self.half_life = None
        
    def fit_cointegration(self) -> dict:
        # Step 1: Check cointegration
        score, pvalue, _ = coint(self.p1, self.p2)
        
        # Step 2: Estimate hedge ratio beta via OLS
        X = sm.add_constant(self.p2)
        model = sm.OLS(self.p1, X).fit()
        self.beta = model.params[1]
        spread = self.p1 - self.beta * self.p2
        
        # Step 3: Estimate OU half-life
        delta_z = np.diff(spread)
        z_lag = spread[:-1]
        ou_model = sm.OLS(delta_z, sm.add_constant(z_lag)).fit()
        theta = -ou_model.params[1]
        self.half_life = np.log(2) / theta if theta > 0 else np.inf
        
        return {
            "p_value": pvalue,
            "hedge_ratio": self.beta,
            "half_life_bars": self.half_life,
            "cointegrated": pvalue < 0.05
        }

# Verification on synthetic mean-reverting spread
np.random.seed(42)
t = 1000
trend = np.cumsum(np.random.normal(0, 1, t))
asset_B = 100 + trend + np.random.normal(0, 0.5, t)
# Asset A has beta=1.2 to B plus stationary mean-reverting spread
spread_ou = np.zeros(t)
for i in range(1, t):
    spread_ou[i] = spread_ou[i-1] * 0.90 + np.random.normal(0, 1.0)
asset_A = 50 + 1.2 * asset_B + spread_ou

pair = StatArbPair(asset_A, asset_B)
metrics = pair.fit_cointegration()
print(f"Cointegrated: {metrics['cointegrated']} (p={metrics['p_value']:.4e})")
print(f"Hedge Ratio:  {metrics['hedge_ratio']:.3f} (True: 1.2)")
print(f"Half-Life:    {metrics['half_life_bars']:.1f} bars")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Cointegration Structural Break (The Divergence Trap):**
   - *Failure:* A merger, debt restructuring, dividend cut, or technological obsolescence permanently breaks the economic link between the two companies.
   - *Symptom:* The spread widens from $2\sigma \to 4\sigma \to 10\sigma$. Without a strict statistical stop-loss, the strategy suffers catastrophic losses.
   - *First-Principle Check:* Always run rolling Chow tests or CUSUM tests for structural breaks on the residuals.

2. **Execution Slippage & Bid-Ask Asymmetry:**
   - *Failure:* In backtests, orders fill instantaneously at midpoint prices. In live trading, crossing the spread on two simultaneous legs doubles transaction costs.
   - *Symptom:* Theoretical Sharpe ratio of $2.5$ collapses to $-0.4$ net of trading fees and short borrowing costs.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series*, Chapter 8 (Cointegration and Error-Correction Models).
- **Vidyamurthy, Ganapathy**: *Pairs Trading: Quantitative Methods and Analysis*, Wiley Finance.

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Bridges to: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection]]
- Bridges to: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs]]
