---
title: "Black-Scholes-Merton & Feynman-Kac Bridge"
tags:
  - pillar-derivative-pricing
  - black-scholes
  - feynman-kac
  - pde
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]] and [[foundations/multivariable-calculus-and-optimization|Calculus]].

---

### 1. Intuition & Practical Objective

The Black-Scholes-Merton (BSM) framework is the continuous-time limit of binomial replication. By continuously rebalancing a portfolio consisting of one derivative contract and $-\Delta$ shares of underlying stock, all Brownian motion randomness perfectly cancels out.

Because the hedged portfolio has zero variance over the next infinitesimal time interval $dt$, it must earn the risk-free interest rate to prevent instantaneous arbitrage. This yields a deterministic partial differential equation (PDE) that bridges continuous diffusion physics with mathematical option pricing.

---

### 2. Mathematical Ground Truth & Derivations

#### Derivation via Delta-Neutral Replicating Portfolio
Let underlying asset price $S_t$ follow Geometric Brownian Motion under physical measure $\mathbb{P}$:
$$d S_t = \mu S_t dt + \sigma S_t dW_t$$
Let $V(t, S_t)$ be the price of a derivative. By Itô's Lemma:
$$d V = \left( \frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S \frac{\partial V}{\partial S} dW_t$$

Construct a portfolio $\Pi = V - \Delta S$. Over interval $dt$:
$$d \Pi = d V - \Delta d S$$
Substitute $dV$ and $dS$:
$$d \Pi = \left( \frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - \Delta \mu S \right) dt + \sigma S \left( \frac{\partial V}{\partial S} - \Delta \right) dW_t$$

Choose $\Delta = \frac{\partial V}{\partial S}$ to eliminate the stochastic $dW_t$ term entirely:
$$d \Pi = \left( \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt$$
Since the portfolio is now riskless, by the No-Arbitrage Principle it must earn the risk-free rate: $d \Pi = r \Pi dt = r(V - \Delta S) dt$.
Equating the two expressions:
$$\frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} = r \left( V - S \frac{\partial V}{\partial S} \right)$$
Rearranging yields the **Black-Scholes-Merton Partial Differential Equation**:
$$\frac{\partial V}{\partial t} + r S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - r V = 0$$

#### The Feynman-Kac Stochastic Bridge
The Feynman-Kac Theorem establishes an exact equivalence between parabolic PDEs and conditional expectations of stochastic processes.
For the terminal condition $V(T, S) = h(S)$, the solution to the BSM PDE is:
$$V(t, S) = e^{-r(T - t)} \mathbb{E}^{\mathbb{Q}}\left[ h(S_T) \mid S_t = S \right]$$
where under the risk-neutral measure $\mathbb{Q}$, the asset drift is replaced by $r$:
$$d S_t = r S_t dt + \sigma S_t dW_t^{\mathbb{Q}}$$

#### Analytical European Call Formula
Solving the expectation for payoff $h(S_T) = \max(S_T - K, 0)$:
$$C(S, t) = S N(d_1) - K e^{-r(T - t)} N(d_2)$$
$$d_1 = \frac{\ln(S / K) + \left( r + \frac{1}{2} \sigma^2 \right)(T - t)}{\sigma \sqrt{T - t}}, \quad d_2 = d_1 - \sigma \sqrt{T - t}$$
where $N(x)$ is the cumulative standard normal distribution function.

---

### 3. Computational Implementation

```python
import numpy as np
import scipy.stats as stats

def black_scholes_call_put(S: float, K: float, T: float, r: float, 
                           sigma: float) -> tuple[float, float]:
    """
    Computes analytical European Call and Put prices under Black-Scholes-Merton.
    """
    if T <= 0:
        return max(0.0, S - K), max(0.0, K - S)
        
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    put_price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    
    return call_price, put_price

# Test European Option pricing
c, p = black_scholes_call_put(S=100, K=100, T=1.0, r=0.05, sigma=0.20)
print(f"BSM Call Price: ${c:.4f}")
print(f"BSM Put Price:  ${p:.4f}")
# Verify Put-Call Parity: C + K*exp(-rT) == P + S
lhs = c + 100 * np.exp(-0.05 * 1.0)
rhs = p + 100
print(f"Put-Call Parity Check: LHS={lhs:.4f} | RHS={rhs:.4f} (Diff: {abs(lhs-rhs):.2e})")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Constant Volatility Delusion:**
   - *Failure:* BSM assumes volatility $\sigma$ is constant across all strikes and maturities.
   - *Reality:* Post-1987 crash markets exhibit steep volatility skews and smiles; out-of-the-money puts trade at implied volatilities far higher than at-the-money options.

2. **Continuous Hedging Friction (Transaction Cost Bleed):**
   - *Failure:* BSM requires continuous rebalancing ($dt \to 0$). In live trading, rebalancing every second incurs bid-ask spread costs that outstrip the option's premium.

---

### 5. Canonical Literature & Study References

- **Shreve, Steven E.**: *Stochastic Calculus for Finance II*, Chapter 4 (Risk-Neutral Pricing), Chapter 5 (Connections with PDEs).
- **Hull, John C.**: *Options, Futures, and Other Derivatives*, Chapter 15 (The Black-Scholes-Merton Model).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]]
- Bridges to: [[pillars/03-derivative-pricing/the-greeks-and-dynamic-hedging|The Greeks]]
- Bridges to: [[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Volatility Surfaces]]
