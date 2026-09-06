---
title: "Fixed Income & Interest Rate Models"
tags: [fixed-income, interest-rates, vasicek, cir, hull-white, hjm]
---

# Fixed Income & Interest Rate Models

Interest rates are not single numbers; they form continuous yield curves across maturities from overnight to 30+ years.

## 1. Zero-Coupon Bonds & Forward Rates
Let $P(t, T)$ be the price at time $t$ of a zero-coupon bond paying $1 at maturity $T$:
$$P(t, T) = \exp\left( -\int_t^T f(t, u) du \right) = \exp(-R(t, T)(T - t))$$
Where $R(t, T)$ is the continuously compounded spot rate, and $f(t, T) = -\frac{\partial \ln P(t, T)}{\partial T}$ is the instantaneous forward rate.

---

## 2. Short-Rate Models
1. **Vasicek (1977):** Mean-reverting Gaussian process:
   $$dr_t = \kappa(\theta - r_t)dt + \sigma dW_t$$
   *Limitation:* Rates can become negative.
2. **Cox-Ingersoll-Ross (CIR, 1985):** Square-root diffusion:
   $$dr_t = \kappa(\theta - r_t)dt + \sigma \sqrt{r_t} dW_t$$
   If $2\kappa\theta \ge \sigma^2$ (Feller condition), rates stay strictly positive.
3. **Hull-White (1990):** Time-dependent mean-reversion parameter $\theta(t)$ calibrated to fit the exact initial term structure of interest rates perfectly.
