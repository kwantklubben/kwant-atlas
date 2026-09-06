---
title: "P vs Q Measures & Girsanov's Theorem"
tags: [stochastics, girsanov, risk-neutral, radon-nikodym]
---

# P vs Q Measures & Girsanov's Theorem

The single most fundamental concept in derivatives pricing is the difference between the **Physical Measure $\mathbb{P}$** (the real world) and the **Risk-Neutral Measure $\mathbb{Q}$** (the pricing world).

## 1. Equivalent Probability Measures
Two measures $\mathbb{P}$ and $\mathbb{Q}$ on $(\Omega, \mathcal{F})$ are **equivalent** ($\mathbb{P} \sim \mathbb{Q}$) if they agree on impossible events:
$$\mathbb{P}(A) = 0 \iff \mathbb{Q}(A) = 0 \quad \forall A \in \mathcal{F}$$
The **Radon-Nikodym Derivative** $Z = \frac{d\mathbb{Q}}{d\mathbb{P}}$ defines the density ratio:
$$\mathbb{Q}(A) = \int_A Z(\omega) \, d\mathbb{P}(\omega) = \mathbb{E}^\mathbb{P}[Z \cdot \mathbf{1}_A]$$

---

## 2. Girsanov's Theorem
Let $W_t^\mathbb{P}$ be a Brownian motion under physical measure $\mathbb{P}$. Let $\theta_t$ be an adapted process (the market price of risk). Define the Radon-Nikodym martingale:
$$Z_t = \exp\left( -\int_0^t \theta_s dW_s^\mathbb{P} - \frac{1}{2} \int_0^t \theta_s^2 ds \right)$$
Then under the measure $\mathbb{Q}$ defined by $\frac{d\mathbb{Q}}{d\mathbb{P}} = Z_T$, the process:
$$W_t^\mathbb{Q} = W_t^\mathbb{P} + \int_0^t \theta_s ds$$
is a **standard Brownian motion under $\mathbb{Q}$**!

### Financial Impact: Removing the Physical Drift
Under $\mathbb{P}$, a stock grows at its real-world expected return $\mu$:
$$dS_t = \mu S_t dt + \sigma S_t dW_t^\mathbb{P}$$
Choosing the market price of risk $\theta = \frac{\mu - r}{\sigma}$ and substituting $dW_t^\mathbb{P} = dW_t^\mathbb{Q} - \theta dt$:
$$dS_t = \mu S_t dt + \sigma S_t \left( dW_t^\mathbb{Q} - \frac{\mu - r}{\sigma} dt \right) = r S_t dt + \sigma S_t dW_t^\mathbb{Q}$$
Under $\mathbb{Q}$, the stock grows exactly at the risk-free rate $r$. The real-world drift $\mu$ completely vanishes from the pricing equations!
