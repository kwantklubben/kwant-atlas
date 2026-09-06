---
title: "Volatility Clustering: ARCH & GARCH Models"
tags: [econometrics, garch, arch, volatility-clustering]
---

# Volatility Clustering: ARCH & GARCH Models

Financial asset returns exhibit zero linear autocorrelation (you cannot predict tomorrow's return from today's return linearly), but their squared returns $r_t^2$ show massive positive autocorrelation. Volatility clusters in regimes.

## 1. ARCH(q) Model (Engle, 1982)
$$r_t = \mu_t + a_t, \quad a_t = \sigma_t \epsilon_t, \quad \epsilon_t \sim \text{i.i.d. } \mathcal{N}(0, 1)$$
$$\sigma_t^2 = \alpha_0 + \sum_{i=1}^q \alpha_i a_{t-i}^2 \quad (\alpha_0 > 0, \alpha_i \ge 0)$$

---

## 2. GARCH(1,1) Model (Bollerslev, 1986)
The standard industry workhorse incorporates autoregressive variance terms:
$$\sigma_t^2 = \omega + \alpha a_{t-1}^2 + \beta \sigma_{t-1}^2$$
- **Stationarity Condition:** $\alpha + \beta < 1$.
- **Long-Run Unconditional Variance:** $\sigma^2 = \frac{\omega}{1 - \alpha - \beta}$.
- **Half-Life of Volatility Shocks:** $\tau = \frac{\ln(0.5)}{\ln(\alpha + \beta)}$. In daily equity data, $\alpha + \beta \approx 0.98\text{--}0.99$, meaning volatility shocks persist for months!

---

## 3. Asymmetric Volatility & The Leverage Effect (EGARCH)
Empirical fact: negative equity returns cause volatility to spike significantly more than positive returns of equal magnitude.
**Exponential GARCH (EGARCH, Nelson 1991):**
$$\ln(\sigma_t^2) = \omega + \beta \ln(\sigma_{t-1}^2) + \alpha \left( \left|\frac{a_{t-1}}{\sigma_{t-1}}\right| - \sqrt{\frac{2}{\pi}} \right) + \gamma \left( \frac{a_{t-1}}{\sigma_{t-1}} \right)$$
If $\gamma < 0$, negative return shocks ($a_{t-1} < 0$) generate higher future volatility than positive shocks.
