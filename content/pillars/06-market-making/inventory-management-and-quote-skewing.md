---
title: "Inventory Management & Quote Skewing"
tags:
  - pillar-market-making
  - inventory-management
  - quote-skewing
  - position-limits
---

**Basic Prerequisites:** [[pillars/06-market-making/the-avellaneda-stoikov-model|Avellaneda-Stoikov Model]].

---

### 1. Intuition & Practical Objective

Market makers operate with strict regulatory capital and prime broker position limits. If a desk has an inventory limit of $\pm 20{,}000$ shares and accumulates $+18{,}000$ shares, they face an immediate margin breach.

Quote skewing is the active mechanism used to maintain a target inventory profile. By widening quotes on the side you don't want and tightening (or improving) quotes on the side you want, market makers use the natural arrival of noise traders to bleed off excess inventory back to flat.

---

### 2. Mathematical Ground Truth & Derivations

#### Linear Skewing Formulation
Let $q_t$ be current inventory and $q_{\text{target}} = 0$ be the target inventory.
The mid-quote skew $\Delta s(q)$ is proportional to inventory displacement:
$$\Delta s(q) = -\alpha \cdot (q_t - q_{\text{target}})$$
where $\alpha > 0$ is the skew sensitivity factor.
- Skewed Bid: $p_t^{\text{bid}} = p_{\text{mid}} + \Delta s(q) - \frac{\text{Spread}}{2}$
- Skewed Ask: $p_t^{\text{ask}} = p_{\text{mid}} + \Delta s(q) + \frac{\text{Spread}}{2}$

#### Non-Linear Quadratic Inventory Penalty
When inventory approaches hard risk limit $Q_{\max}$:
$$\Delta s(q) = -\alpha \cdot \text{sign}(q) \left( \frac{|q|}{Q_{\max}} \right)^2$$
As $|q| \to Q_{\max}$, the quote on the accumulating side is pulled completely out of the market (infinite spread), while the unloading side is quoted aggressively inside the national best bid/offer (NBBO) to force an immediate fill.

---

### 3. Computational Implementation

```python
def compute_skewed_quotes(mid_price: float, current_inventory: int, 
                          max_inventory: int, base_spread: float, 
                          alpha: float = 0.001) -> tuple[float, float]:
    """
    Computes non-linear quote skewing to enforce inventory limits.
    """
    q_ratio = current_inventory / max_inventory
    # Non-linear quadratic skew
    skew = -alpha * np.sign(current_inventory) * (q_ratio ** 2) * mid_price
    
    bid = mid_price + skew - base_spread / 2.0
    ask = mid_price + skew + base_spread / 2.0
    
    # If hit max inventory, withdraw quoting on that side completely
    if current_inventory >= max_inventory:
        bid = -np.inf # Stop buying
    elif current_inventory <= -max_inventory:
        ask = np.inf  # Stop selling
        
    return bid, ask

# Demonstration: Normal vs Skewed
mid = 50.00
b_norm, a_norm = compute_skewed_quotes(mid, current_inventory=0, max_inventory=1000, base_spread=0.04)
b_skew, a_skew = compute_skewed_quotes(mid, current_inventory=800, max_inventory=1000, base_spread=0.04)

print(f"Neutral Quotes (q=0):   Bid=${b_norm:.2f} | Ask=${a_norm:.2f}")
print(f"Skewed Quotes (q=+800): Bid=${b_skew:.2f} | Ask=${a_skew:.2f} (Shaded down to attract sellers)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Adverse Selection during Aggressive Skewing:**
   - *Failure:* Shading your ask quote down so aggressively to dump long inventory that you sell to informed traders right before a massive upward breakout.

2. **Overnight Inventory Gapping Risk:**
   - *Failure:* Holding non-zero inventory into the market close. Overnight gaps bypass intraday stop-loss algorithms.

---

### 5. Canonical Literature & Study References

- **Guéant, Olivier, Tapia, Charles-Albert, & Manziadi, Zaki**: *Dealing with the inventory risk: a solution to the market making problem*, Mathematics and Financial Economics 6, 259-277 (2012).
- **Foucault, Thierry, Pagano, Marco, & Röell, Ailsa**: *Market Liquidity*, Chapter 5 (Inventory Risk).

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/06-market-making/the-avellaneda-stoikov-model|Avellaneda-Stoikov]]
- Bridges to: [[pillars/04-quantitative-risk/liquidity-risk-and-margin-spirals|Liquidity Risk]]
