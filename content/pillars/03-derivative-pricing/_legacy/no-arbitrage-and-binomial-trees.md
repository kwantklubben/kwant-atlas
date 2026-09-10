---
title: "No-Arbitrage Foundations & Binomial Trees"
tags:
  - pillar-derivative-pricing
  - binomial-trees
  - no-arbitrage
  - put-call-parity
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory|Probability Theory]] and high-school algebra.

---

### 1. Intuition & Practical Objective

How do you price an option when nobody knows whether the stock will go up or down?

The breakthrough of modern finance is that you do not need to know the true physical drift $\mu$ of the stock. By constructing a synthetic portfolio combining the stock and risk-free cash that perfectly replicates the option's payoff in every possible future state of the world, the option *must* trade at the exact cost of that replicating portfolio. If it doesn't, a risk-free arbitrage exists.

---

### 2. Mathematical Ground Truth & Derivations

#### Put-Call Parity
For European call $C$ and put $P$ with strike $K$ and maturity $T$, investing in a call and lending discounted cash $K e^{-rT}$ yields the exact same payoff at maturity as holding the stock $S_0$ and a put:
$$C_0 + K e^{-rT} = P_0 + S_0$$
- If $C_0 + K e^{-rT} > P_0 + S_0$: Sell Call, Borrow $K e^{-rT}$, Buy Put, Buy Stock (Arb profit $> 0$).
- If $C_0 + K e^{-rT} < P_0 + S_0$: Buy Call, Lend $K e^{-rT}$, Sell Put, Short Stock (Arb profit $> 0$).

#### The Cox-Ross-Rubinstein (CRR) One-Period Model
Over time step $\Delta t$, stock price $S_0$ can move to:
- Up state: $S_u = u S_0$ with payoff $C_u$
- Down state: $S_d = d S_0$ with payoff $C_d$
where $d < e^{r \Delta t} < u$.

Construct a portfolio of $\Delta$ shares of stock and $B$ dollars of bonds:
$$\Pi_u = \Delta u S_0 + B e^{r \Delta t} = C_u$$
$$\Pi_d = \Delta d S_0 + B e^{r \Delta t} = C_d$$
Solving this linear 2x2 system yields the exact replicating delta:
$$\Delta = \frac{C_u - C_d}{S_0(u - d)}$$
$$B = e^{-r \Delta t} \left( \frac{u C_d - d C_u}{u - d} \right)$$

The cost of the portfolio today $\Pi_0 = \Delta S_0 + B$ simplifies to:
$$C_0 = e^{-r \Delta t} \left[ q C_u + (1 - q) C_d \right]$$
where the **risk-neutral probability** $q$ is:
$$q = \frac{e^{r \Delta t} - d}{u - d}, \quad 0 < q < 1$$
Notice that the real-world probability $p$ has completely vanished from the pricing equation!

#### Multi-Step CRR Parameters
Matching drift and variance of continuous Geometric Brownian Motion over step $\Delta t$:
$$u = e^{\sigma \sqrt{\Delta t}}, \quad d = e^{-\sigma \sqrt{\Delta t}} = \frac{1}{u}$$

#### American Option Backward Induction
For American options with early exercise payoff $\Psi(S)$:
$$V_{i, j} = \max\left( \Psi(S_{i, j}), \; e^{-r \Delta t} [q V_{i+1, j+1} + (1 - q) V_{i+1, j}] \right)$$

---

### 3. Computational Implementation

```python
import numpy as np

def price_american_option_tree(S0: float, K: float, T: float, r: float, 
                               sigma: float, steps: int, option_type: str = "put") -> float:
    """
    Prices American options using CRR binomial tree backward induction.
    """
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    q = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)
    
    # Asset prices at maturity (step N)
    prices = S0 * (u ** np.arange(steps, -1, -1)) * (d ** np.arange(0, steps + 1, 1))
    
    # Terminal payoffs
    if option_type.lower() == "call":
        values = np.maximum(0.0, prices - K)
    else:
        values = np.maximum(0.0, K - prices)
        
    # Backward induction
    for i in range(steps - 1, -1, -1):
        prices = S0 * (u ** np.arange(i, -1, -1)) * (d ** np.arange(0, i + 1, 1))
        continuation_value = discount * (q * values[:-1] + (1.0 - q) * values[1:])
        exercise_value = np.maximum(0.0, prices - K) if option_type.lower() == "call" else np.maximum(0.0, K - prices)
        values = np.maximum(exercise_value, continuation_value)
        
    return float(values[0])

# Price American Put: S=100, K=100, T=1yr, r=5%, vol=20%
am_put = price_american_option_tree(100, 100, 1.0, 0.05, 0.20, steps=500, option_type="put")
print(f"American Put Price (CRR 500 steps): ${am_put:.4f}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Dividend Early-Exercise Trap:**
   - *Failure:* Using European Black-Scholes formulas on American options with impending ex-dividend dates.
   - *Reality:* American call options should often be exercised immediately prior to the ex-dividend date if the dividend payment exceeds the remaining time value of the option.

2. **Negative Risk-Neutral Probability:**
   - *Failure:* If step size $\Delta t$ is too large such that $e^{r \Delta t} > u$ or $e^{r \Delta t} < d$, $q$ falls outside $[0, 1]$, violating probability axioms.

---

### 5. Canonical Literature & Study References

- **Shreve, Steven E.**: *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model*, Springer, Chapters 1-4.
- **Hull, John C.**: *Options, Futures, and Other Derivatives*, Chapter 13 (Binomial Trees).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/probability-and-measure-theory|Probability & Measure Theory]]
- Bridges to: [[pillars/03-derivative-pricing/black-scholes-merton-and-feynman-kac|Black-Scholes PDE]]
- Bridges to: [[pillars/03-derivative-pricing/the-greeks-and-dynamic-hedging|The Greeks & Dynamic Hedging]]
