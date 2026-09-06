---
title: "Fat Tails, Power Laws & Extreme Value Theory"
tags: [complexity, fat-tails, power-laws, evt, cvar]
---

# Fat Tails, Power Laws & Extreme Value Theory (EVT)

Gaussian distributions drastically underestimate the probability of extreme market dislocations.

## 1. The Power-Law Tail
A distribution has a fat tail if the survival function decays as a power law:
$$P(X > x) = L(x) x^{-\alpha}$$
Where $\alpha$ is the tail index.
- If $\alpha \le 2$: The distribution has **infinite variance**!
- If $\alpha \le 1$: The distribution has **infinite mean**!
- In equity markets, empirical studies (Gopikrishnan et al., Bouchaud) find **$\alpha \approx 3$ (the cubic law of returns)**.

---

## 2. Extreme Value Theory (EVT): Pickands-Balkema-de Haan Theorem
Instead of fitting the entire distribution, EVT models the excess over a high threshold $u$.
For large $u$, the distribution of excess $Y = X - u$ converges to the **Generalized Pareto Distribution (GPD)**:
$$G_{\xi, \beta}(y) = 1 - \left( 1 + \frac{\xi y}{\beta} \right)^{-1/\xi}$$
- $\xi > 0$: Heavy-tailed (Frechet-type, financial returns).
- $\xi = 0$: Exponential tail (Gaussian, normal).
- $\xi < 0$: Bounded tail (Weibull).
