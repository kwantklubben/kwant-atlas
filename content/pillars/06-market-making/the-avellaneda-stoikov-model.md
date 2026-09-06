---
title: "The Avellaneda-Stoikov Model"
tags:
  - pillar-market-making
  - avellaneda-stoikov
  - optimal-quoting
  - inventory-risk
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus]] and [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]].

---

### 1. Intuition & Practical Objective

If you place symmetric quotes at the bid and ask ($\pm \$0.02$ from the mid-price), a random barrage of market orders will cause your inventory to fluctuate. If several buyers hit your ask, you are suddenly short $-5{,}000$ shares. If the market starts trending upwards, your short position will bleed capital.

The **Avellaneda & Stoikov (2008)** model is the canonical mathematical framework that solves optimal high-frequency quoting. When inventory builds up, the market maker skews their quotes: shading their **reservation price** downwards to discourage further buys and aggressively incentivize sellers to take them back to flat inventory.

---

### 2. Mathematical Ground Truth & Derivations

#### Midpoint Asset Dynamics
Let the midpoint price $S_t$ follow Brownian motion:
$$d S_t = \sigma dW_t$$
The market maker holds inventory $q_t \in \mathbb{Z}$ and cash $X_t$. The value of the portfolio at horizon $T$ is:
$$X_T + q_T S_T$$

#### Agent Utility Function
The market maker maximizes expected exponential utility under absolute risk aversion $\gamma > 0$:
$$\max_{\delta^a, \delta^b} \mathbb{E}\left[ -\exp\left( -\gamma (X_T + q_T S_T) \right) \right]$$

#### Reservation Price (Indifference Price)
The reservation price $r(s, q, t)$ is the subjective price at which the market maker is completely indifferent between holding their current inventory $q$ vs trading 1 unit of stock:
$$r(s, q, t) = s - q \gamma \sigma^2 (T - t)$$
- If $q > 0$ (long inventory): The reservation price is *strictly lower* than the market mid-price $s$. The market maker wants to dump inventory!
- If $q < 0$ (short inventory): The reservation price is *strictly higher* than $s$. The market maker bids aggressively to buy back shares.

#### Order Fill Arrival Intensities
Passive limit orders placed at distances $\delta^a$ and $\delta^b$ from the mid-price fill according to Poisson processes with intensities:
$$\lambda^a(\delta^a) = A e^{-k \delta^a}, \quad \lambda^b(\delta^b) = A e^{-k \delta^b}$$
where $k$ is order book liquidity density.

#### The Optimal Quoting Formula
Solving the Hamilton-Jacobi-Bellman (HJB) partial differential equation yields the optimal half-spread quotes:
$$\delta^a(s, q, t) + \delta^b(s, q, t) = \frac{2}{\gamma} \ln\left(1 + \frac{\gamma}{k}\right) + \frac{1}{2} (2q + 1) \gamma \sigma^2 (T - t)$$
Optimal quotes around the reservation price $r$:
$$r_t = s_t - q_t \gamma \sigma^2 (T - t)$$
$$p_t^{\text{ask}} = r_t + \frac{1}{2} s^*, \quad p_t^{\text{bid}} = r_t - \frac{1}{2} s^*$$
where $s^* = \frac{2}{\gamma} \ln(1 + \frac{\gamma}{k})$ is the optimal stationary spread.

---

### 3. Computational Implementation

```python
import numpy as np

def compute_avellaneda_stoikov_quotes(s: float, q: int, gamma: float, 
                                      sigma: float, T_minus_t: float, 
                                      k: float) -> tuple[float, float, float]:
    """
    Computes Avellaneda-Stoikov optimal reservation price, bid, and ask quotes.
    s: Current mid-price
    q: Current inventory position (shares/contracts)
    gamma: Risk aversion parameter
    sigma: Volatility
    T_minus_t: Remaining trading horizon (fraction of day)
    k: Order book liquidity density
    """
    # Reservation (indifference) price
    r = s - q * gamma * (sigma ** 2) * T_minus_t
    
    # Optimal stationary spread
    optimal_spread = (2.0 / gamma) * np.log(1.0 + gamma / k)
    
    bid_quote = r - optimal_spread / 2.0
    ask_quote = r + optimal_spread / 2.0
    
    return r, bid_quote, ask_quote

# Compare quotes when Neutral (q=0) vs Long Inventory (q=+10)
mid = 100.00
r_0, bid_0, ask_0 = compute_avellaneda_stoikov_quotes(mid, q=0, gamma=0.1, sigma=0.20, T_minus_t=0.5, k=1.5)
r_10, bid_10, ask_10 = compute_avellaneda_stoikov_quotes(mid, q=10, gamma=0.1, sigma=0.20, T_minus_t=0.5, k=1.5)

print(f"Inventory q=0:  ResPrice={r_0:.3f} | Bid={bid_0:.3f} | Ask={ask_0:.3f}")
print(f"Inventory q=10: ResPrice={r_10:.3f} | Bid={bid_10:.3f} | Ask={ask_10:.3f} (Quotes shaded downward!)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Terminal Inventory Liquidation Shock ($t \to T$):**
   - *Failure:* As $T - t \to 0$, the reservation penalty term vanishes, leading to zero inventory protection right at market close when liquidity evaporates.
   - *Remedy:* Impose an explicit terminal liquidation penalty $\alpha q_T^2$.

2. **Constant Intensity Parameter $k$ Assumption:**
   - *Failure:* In live markets, fill intensity parameter $k$ collapses during news events, as liquidity takers sweep the book.

---

### 5. Canonical Literature & Study References

- **Avellaneda, Marco & Stoikov, Sasha**: *High-frequency trading in a limit order book*, Quantitative Finance 8(3), 217-224 (2008).
- **Guéant, Olivier**: *The Financial Mathematics of Market Liquidity: From Optimal Execution to Market Making*, CRC Press.

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]]
- Bridges to: [[pillars/06-market-making/inventory-management-and-quote-skewing|Quote Skewing]]
- Bridges to: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]]
