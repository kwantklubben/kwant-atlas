---
title: "Value at Risk & Expected Shortfall (CVaR)"
tags:
  - pillar-quant-risk
  - var
  - expected-shortfall
  - coherent-risk
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability Theory]] (Cumulative Distribution Functions, Quantiles).

---

### 1. Intuition & Practical Objective

If a risk manager tells an executive: "Our 1-day 99% Value at Risk is $\$5,000,000$," this means: *On 99 out of 100 trading days, our daily loss will not exceed $\$5,000,000$.*

However, VaR tells you absolutely nothing about what happens on that 1 remaining day: do you lose $\$5,000,001$, or do you lose $\$100,000,000$ and go bankrupt?

**Expected Shortfall (Conditional VaR)** answers this existential question by calculating the mathematical expectation of losses given that the loss has exceeded the VaR threshold.

---

### 2. Mathematical Ground Truth & Derivations

#### Value at Risk (VaR)
Let $L = -\Delta V$ be the portfolio loss over horizon $\Delta t$. For confidence level $\alpha \in (0, 1)$ (typically $0.95$ or $0.99$):
$$\text{VaR}_\alpha(L) = \inf \{ l \in \mathbb{R} \mid \mathbb{P}(L > l) \le 1 - \alpha \} = F_L^{-1}(\alpha)$$

#### Artzner et al. (1999) Coherent Risk Measure Axioms
A risk measure $\rho: \mathcal{L} \to \mathbb{R}$ is **coherent** if and only if it satisfies:
1. **Translation Invariance:** $\rho(L + c) = \rho(L) + c$ for constant cash $c$.
2. **Subadditivity:** $\rho(L_1 + L_2) \le \rho(L_1) + \rho(L_2)$ (Diversification must never increase risk).
3. **Positive Homogeneity:** $\rho(\lambda L) = \lambda \rho(L)$ for all $\lambda \ge 0$.
4. **Monotonicity:** If $L_1 \le L_2$ almost surely, then $\rho(L_1) \le \rho(L_2)$.

#### The Fatal Flaw of VaR: Violation of Subadditivity
VaR is **NOT** a coherent risk measure because it violates subadditivity.
- *Counter-Example:* Consider two independent bonds $A$ and $B$, each having a $4\%$ probability of defaulting and losing $\$100$, and a $96\%$ probability of losing $\$0$.
  - At $\alpha = 0.95$: $\text{VaR}_{0.95}(A) = 0$ and $\text{VaR}_{0.95}(B) = 0$.
  - Combined portfolio $A + B$: Probability that at least one defaults is $1 - (0.96)^2 = 7.84\% > 5\%$.
  - Therefore, $\text{VaR}_{0.95}(A + B) = \$100 > \text{VaR}_{0.95}(A) + \text{VaR}_{0.95}(B) = 0$.
  - Merging the two assets created massive measured risk out of nothing!

#### Expected Shortfall (CVaR)
Expected Shortfall is strictly **coherent**:
$$\text{ES}_\alpha(L) = \mathbb{E}[L \mid L \ge \text{VaR}_\alpha(L)] = \frac{1}{1 - \alpha} \int_\alpha^1 \text{VaR}_u(L) \, du$$
For a standard normal loss distribution $L \sim \mathcal{N}(\mu, \sigma^2)$:
$$\text{VaR}_\alpha = \mu + \sigma \Phi^{-1}(\alpha)$$
$$\text{ES}_\alpha = \mu + \sigma \frac{\phi(\Phi^{-1}(\alpha))}{1 - \alpha}$$

#### Cornish-Fisher Expansion for Non-Gaussian Losses
When returns exhibit skewness $\gamma_1$ and excess kurtosis $\gamma_2$:
$$z_\alpha^{\text{CF}} = z_\alpha + \frac{1}{6}(z_\alpha^2 - 1)\gamma_1 + \frac{1}{24}(z_\alpha^3 - 3z_\alpha)\gamma_2 - \frac{1}{36}(2z_\alpha^3 - 5z_\alpha)\gamma_1^2$$
where $z_\alpha = \Phi^{-1}(\alpha)$.
$$\text{VaR}_\alpha^{\text{CF}} = -(\mu + z_\alpha^{\text{CF}} \sigma)$$

---

### 3. Computational Implementation

```python
import numpy as np
import scipy.stats as stats

def calculate_var_cvar(returns: np.ndarray, alpha: float = 0.99) -> dict[str, float]:
    """
    Computes Historical and Gaussian VaR & Expected Shortfall (CVaR).
    """
    losses = -returns
    
    # 1. Historical VaR & CVaR
    var_hist = np.percentile(losses, alpha * 100)
    cvar_hist = np.mean(losses[losses >= var_hist])
    
    # 2. Parametric Gaussian
    mu = np.mean(losses)
    sigma = np.std(losses)
    z = stats.norm.ppf(alpha)
    var_param = mu + sigma * z
    cvar_param = mu + sigma * (stats.norm.pdf(z) / (1.0 - alpha))
    
    return {
        "Historical_VaR": var_hist,
        "Historical_CVaR": cvar_hist,
        "Parametric_VaR": var_param,
        "Parametric_CVaR": cvar_param
    }

# Synthetic fat-tailed Student-t returns
np.random.seed(42)
t_returns = stats.t.rvs(df=3, loc=0.0005, scale=0.01, size=10000)
metrics = calculate_var_cvar(t_returns, alpha=0.99)
print(f"99% Historical VaR:  {metrics['Historical_VaR']*100:.2f}% | CVaR: {metrics['Historical_CVaR']*100:.2f}%")
print(f"99% Parametric VaR:  {metrics['Parametric_VaR']*100:.2f}% | CVaR: {metrics['Parametric_CVaR']*100:.2f}%")
print("Notice how Gaussian Parametric CVaR drastically underestimates fat-tailed loss!")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tail Blindness of VaR:**
   - *Failure:* Optimizing portfolios directly against VaR constraints.
   - *Symptom:* The optimizer loads up on strategies with small positive gains and massive hidden disaster tails (e.g., selling deep out-of-the-money puts), maximizing the probability of total ruin beyond the 99% percentile.

2. **Window Truncation in Historical Simulation:**
   - *Failure:* Using a 1-year historical window during a quiet bull market.
   - *Symptom:* The model assigns 0% probability to any volatility shock larger than the tranquil observations of the past 250 days.

---

### 5. Canonical Literature & Study References

- **Artzner, Philippe, Delbaen, Freddy, Eber, Jean-Marc, & Heath, David**: *Coherent Measures of Risk*, Mathematical Finance 9(3), 203-228 (1999).
- **Hull, John C.**: *Risk Management and Financial Institutions*, Wiley, Chapters 11-13 (Value at Risk and Expected Shortfall).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Bridges to: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|Extreme Value Theory]]
- Bridges to: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Portfolio Risk Constraints]]
