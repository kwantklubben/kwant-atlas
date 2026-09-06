---
title: "Measure-Theoretic Probability"
tags: [probability, measure-theory, sigma-algebra, filtrations]
---

# Measure-Theoretic Probability & Probability Spaces

In modern quantitative finance, probability is formalized through measure theory (Kolmogorov, 1933).

## 1. The Probability Triple $(\Omega, \mathcal{F}, \mathbb{P})$
1. **Sample Space $\Omega$:** The set of all possible outcomes of the world $\omega \in \Omega$.
2. **$\sigma$-Algebra $\mathcal{F}$:** A collection of subsets of $\Omega$ satisfying:
   - $\Omega \in \mathcal{F}$.
   - Closed under complementation: $A \in \mathcal{F} \implies A^c \in \mathcal{F}$.
   - Closed under countable unions: $A_1, A_2, \dots \in \mathcal{F} \implies \bigcup_{i=1}^\infty A_i \in \mathcal{F}$.
   *Interpretation:* $\mathcal{F}$ represents the set of all observable events to which probabilities can be assigned.
3. **Probability Measure $\mathbb{P}$:** A function $\mathbb{P}: \mathcal{F} \to [0, 1]$ satisfying:
   - Non-negativity: $\mathbb{P}(A) \ge 0 \quad \forall A \in \mathcal{F}$.
   - Unit measure: $\mathbb{P}(\Omega) = 1$.
   - Countable additivity: For disjoint sets $A_i$, $\mathbb{P}(\bigcup A_i) = \sum \mathbb{P}(A_i)$.

---

## 2. Filtrations: The Mathematical Flow of Time
A **filtration** $\mathbb{F} = \{\mathcal{F}_t\}_{t \ge 0}$ is an increasing family of sub-$\sigma$-algebras:
$$s \le t \implies \mathcal{F}_s \subseteq \mathcal{F}_t \subseteq \mathcal{F}$$
- **Financial Intuition:** $\mathcal{F}_t$ represents the accumulated market history and information available at time $t$. An investor at time $t$ knows whether events in $\mathcal{F}_t$ have occurred, but cannot see into $\mathcal{F}_u$ for $u > t$.
- **Adapted Process:** A stochastic process $X_t$ is adapted to $\mathcal{F}_t$ if $X_t$ is $\mathcal{F}_t$-measurable for all $t$ (no look-ahead bias!).
