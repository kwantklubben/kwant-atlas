---
title: "Liquidity Risk & Margin Spirals"
tags:
  - pillar-quant-risk
  - liquidity-risk
  - margin-spirals
  - fire-sales
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & CVaR]].

---

### 1. Intuition & Practical Objective

A financial firm can be deeply solvent on paper (assets exceed liabilities) and yet die within 48 hours from a **liquidity crisis**.

Liquidity risk manifests in two interconnected forms:
1. **Asset / Market Liquidity:** The ability to sell an asset immediately without crushing its price.
2. **Funding Liquidity:** The ease with which a firm can obtain cash or roll over repo borrowing against collateral.

When asset prices decline, clearing houses and prime brokers raise margin requirements (**haircuts**). To post more cash margin, funds are forced to liquidate assets, depressing market prices further in a catastrophic feedback loop: **the margin spiral**.

---

### 2. Mathematical Ground Truth & Derivations

#### Liquidity-Adjusted VaR (L-VaR)
Standard VaR assumes positions can be liquidated instantaneously at the mid-market price. Incorporating bid-ask spread liquidation costs:
$$L-\text{VaR}_\alpha = \text{VaR}_\alpha + \frac{1}{2} \sum_{i=1}^N P_i Q_i \left( S_i + z_\alpha \sigma_{S_i} \right)$$
where $S_i$ is the relative bid-ask spread $\frac{p_a - p_b}{M}$ and $\sigma_{S_i}$ is spread volatility.

#### The Brunnermeier & Pedersen (2009) Margin Spiral Model
Consider a leveraged speculator financing a position of size $x_t$ via margin borrowing:
- Haircut / Margin Requirement $m_t \in (0, 1)$ set by prime broker.
- Equity Capital: $W_t$.
- Maximum position size:
$$x_t \le \frac{W_t}{m_t}$$

Prime brokers set margin haircuts dynamically based on asset volatility $\sigma_t$:
$$m_t = \Phi^{-1}(1 - \epsilon) \cdot \sigma_t$$
When a negative market shock hits:
1. Wealth decreases: $\Delta W_t < 0$.
2. Realized volatility surges: $\sigma_t \uparrow \implies m_t \uparrow$.
3. Max allowed position $\frac{W_t}{m_t}$ collapses from both the numerator and denominator!
$$\Delta x_{\text{forced}} = x_{t-1} - \frac{W_t}{m_t} \gg 0$$
4. Forced liquidation dumps $x_{\text{forced}}$ onto the market, depressing asset price $P$ further through market impact, reigniting step 1.

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_margin_spiral(initial_capital: float = 10_000_000, 
                           leverage: float = 5.0, 
                           initial_haircut: float = 0.10, 
                           market_impact_param: float = 1e-6) -> dict:
    """
    Simulates a dynamic feedback margin spiral triggered by an initial asset shock.
    """
    capital = initial_capital
    position = capital * leverage # $50M initial asset position
    haircut = initial_haircut
    
    # Exogenous -3% market shock
    asset_price = 1.0 * (1.0 - 0.03)
    loss = position * 0.03
    capital -= loss
    
    history = [{"round": 0, "capital": capital, "position": position, "haircut": haircut}]
    
    # Spiral iterations
    for round_num in range(1, 6):
        # Volatility shock causes prime broker to hike haircut
        haircut = min(0.35, haircut + 0.04)
        max_allowed_position = capital / haircut
        
        if position > max_allowed_position:
            forced_liquidation = position - max_allowed_position
            # Market impact of liquidation pushes price down further
            price_impact = forced_liquidation * market_impact_param
            liquidation_loss = forced_liquidation * price_impact
            capital -= liquidation_loss
            position = max_allowed_position
        else:
            forced_liquidation = 0
            
        history.append({
            "round": round_num,
            "capital": capital,
            "position": position,
            "forced_liquidation": forced_liquidation,
            "haircut": haircut
        })
        if capital <= 0:
            break
            
    return history

# Run spiral
spiral = simulate_margin_spiral()
for step in spiral:
    print(f"Round {step['round']}: Capital=${step['capital']/1e6:5.2f}M | Position=${step['position']/1e6:5.2f}M | Haircut={step['haircut']*100:.1f}%")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming Linear Collateral Haircuts:**
   - *Failure:* Assuming prime brokers will keep margin rules static during extreme macro volatility.
   - *Reality:* Prime brokers unilaterally hike haircuts on illiquid or exotic collateral from $15\%$ to $50\%$ overnight to protect their own balance sheets.

2. **Crowded Unwind Contagion:**
   - *Failure:* Even if your fund did not change its risk profile, competing funds holding the same assets are forced to liquidate, crushing your mark-to-market prices.

---

### 5. Canonical Literature & Study References

- **Brunnermeier, Markus K. & Pedersen, Lasse Heje**: *Market Liquidity and Funding Liquidity*, Review of Financial Studies 22(6), 2201-2238 (2009).
- **Foucault, Thierry, Pagano, Marco, & Röell, Ailsa**: *Market Liquidity*, Chapter 10 (Liquidity and Financial Stability).

---

### 6. Connected Graph Bridges

- Foundational Base: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]]
- Bridges to: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]
- Bridges to: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs]]
