---
title: "Stress Testing & Reverse Stress Testing"
tags:
  - pillar-quant-risk
  - stress-testing
  - scenario-analysis
  - crisis-replay
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & CVaR]] and [[foundations/linear-algebra-and-matrices|Linear Algebra]].

---

### 1. Intuition & Practical Objective

VaR and Expected Shortfall answer the question: *Given normal and historically frequent market behavior, what is our expected loss?*

**Stress Testing** answers the existential question: *What happens to our firm if the unforecastable happens?* What if the US Dollar crashes $15\%$, interest rates spike $300$ basis points overnight, and high-yield credit spreads widen by $600$ bps simultaneously?

Stress testing bypasses historical probability distributions entirely, subjecting the portfolio to deterministic macroeconomic shocks and historical crisis replays.

---

### 2. Mathematical Ground Truth & Derivations

#### Historical Crisis Replays
The portfolio is evaluated against historical asset return trajectories during famous crises:
1. **October 1987 Black Monday:** S&P 500 drops $-20.5\%$ in a single day.
2. **August 1998 Russian Default / LTCM:** Flight to quality, Treasury yields collapse, credit spreads blow out, swap spreads surge.
3. **September 2008 Lehman Bankruptcy:** Equity markets plunge $-40\%$, interbank lending freezes (TED spread $> 300$ bps), correlation across all risky assets jumps to $+1.0$.
4. **March 2020 COVID Liquidity Shock:** Simultaneous liquidation across equities, gold, and long Treasuries to raise cash; VIX hits 82.

#### Macroeconomic Factor Stress Shocks
Let portfolio return be represented by multi-factor sensitivity:
$$\Delta V = \sum_{k=1}^K \beta_k \Delta F_k + \epsilon$$
Apply deterministic shock vector $\Delta F^* = [\Delta \text{Equity} = -25\%, \; \Delta \text{10Y Yield} = +150\text{bps}, \; \Delta \text{VIX} = +35]$:
$$\text{Stress Loss } \Delta V^* = \beta^T \Delta F^*$$

#### Reverse Stress Testing
Standard stress testing takes a scenario and computes the resulting loss. **Reverse Stress Testing** starts with an intolerable outcome (e.g., bankruptcy, regulatory capital breach of $\$500\text{M}$) and solves an inverse optimization problem to find the smallest plausible market shock vector $\mathbf{z}$ that causes that failure:
$$\min_{\mathbf{z} \in \mathbb{R}^K} \mathbf{z}^T \Sigma_F^{-1} \mathbf{z} \quad \text{subject to} \quad \Delta V(\mathbf{z}) \le -L_{\text{fatal}}$$
This exposes the hidden vulnerability vectors and Achilles' heels of the fund.

---

### 3. Computational Implementation

```python
import numpy as np

def run_stress_scenarios(portfolio_betas: dict[str, float], portfolio_nav: float) -> dict[str, float]:
    """
    Evaluates portfolio P&L against canonical historical macro stress scenarios.
    """
    # Scenario shocks: [Equity, Rates_bps, CreditSpread_bps, Oil]
    scenarios = {
        "1987_Black_Monday": {"Equity": -0.22, "Rates_bps": -50, "CreditSpread_bps": +150, "Oil": -0.10},
        "2008_Lehman_Crisis": {"Equity": -0.35, "Rates_bps": -150, "CreditSpread_bps": +500, "Oil": -0.40},
        "2020_COVID_Liquidity": {"Equity": -0.28, "Rates_bps": -80, "CreditSpread_bps": +300, "Oil": -0.55},
        "Inflation_Rate_Shock": {"Equity": -0.15, "Rates_bps": +250, "CreditSpread_bps": +100, "Oil": +0.30},
    }
    
    results = {}
    for name, shocks in scenarios.items():
        # Compute portfolio return shock
        pnl_pct = (
            portfolio_betas.get("Equity", 0) * shocks["Equity"] +
            portfolio_betas.get("Rates", 0) * (shocks["Rates_bps"] / 10000.0) +
            portfolio_betas.get("Credit", 0) * (shocks["CreditSpread_bps"] / 10000.0) +
            portfolio_betas.get("Oil", 0) * shocks["Oil"]
        )
        results[name] = pnl_pct * portfolio_nav
        
    return results

# $100M Long/Short Multi-Asset Fund
fund_betas = {"Equity": 0.40, "Rates": -5.0, "Credit": -8.0, "Oil": 0.15}
stress_pnl = run_stress_scenarios(fund_betas, portfolio_nav=100_000_000)
for k, v in stress_pnl.items():
    print(f"Scenario {k:22s}: Loss = -${abs(v)/1e6:6.2f}M")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Correlation Breakdown in Severe Crises:**
   - *Failure:* Assuming historical diversification benefits hold during stress.
   - *Reality:* In severe liquidity panics, all correlations converge to 1: *"In a crisis, the only thing that goes up is correlation."* Assets assumed to be hedges fall in tandem.

2. **Plausibility Blindness:**
   - *Failure:* Fabricating arbitrary scenarios that violate basic economic laws (e.g., oil dropping 90% while inflation spikes 10%).

---

### 5. Canonical Literature & Study References

- **McNeil, Alexander J., Frey, Rüdiger, & Embrechts, Paul**: *Quantitative Risk Management*, Chapter 13 (Stress Testing).
- **Hull, John C.**: *Risk Management and Financial Institutions*, Chapter 22 (Scenario Analysis and Stress Testing).

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/04-quantitative-risk/liquidity-risk-and-margin-spirals|Liquidity Risk]]
- Bridges to: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model|Credit Risk]]
