---
title: "CAPM, APT & Multi-Factor Pricing"
tags: [asset-pricing, capm, fama-french, factor-models]
---

# CAPM, APT & Multi-Factor Pricing Models

How are financial assets priced in equilibrium? Asset pricing models determine the expected rate of return required by investors to bear systematic risk.

## 1. The Capital Asset Pricing Model (CAPM)
Developed by Sharpe (1964), Lintner (1965), and Mossin (1966):
$$\mathbb{E}[R_i] = R_f + \beta_i (\mathbb{E}[R_m] - R_f)$$
$$\beta_i = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}$$
- **The Core Axiom:** Idiosyncratic firm-specific risk can be fully diversified away in large portfolios. Therefore, the market offers **zero expected return** for bearing idiosyncratic risk. Investors are compensated only for bearing systematic market risk $\beta_i$.

---

## 2. Fama-French 5-Factor Model (2015)
Empirical data revealed that CAPM beta fails to explain cross-sectional stock returns. Fama & French expanded the model:
$$R_{it} - R_{ft} = \alpha_i + \beta_{i1}(R_{mt} - R_{ft}) + \beta_{i2}\text{SMB}_t + \beta_{i3}\text{HML}_t + \beta_{i4}\text{RMW}_t + \beta_{i5}\text{CMA}_t + \epsilon_{it}$$
Where:
- $\text{SMB}$ (Small Minus Big): Size anomaly.
- $\text{HML}$ (High Minus Low): Value anomaly (Book-to-Market).
- $\text{RMW}$ (Robust Minus Weak): Operating profitability.
- $\text{CMA}$ (Conservative Minus Aggressive): Capital investment intensity.
