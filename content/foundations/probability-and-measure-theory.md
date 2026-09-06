---
title: "Probability & Measure Theory"
tags:
  - foundations
  - probability
  - measure-theory
  - martingales
---

**Basic Prerequisites:** Elementary set theory and calculus.

---

### 1. Intuition & Practical Objective

Why do we need measure theory instead of simple high-school probability in quantitative finance? Because financial markets operate on continuous information flows over continuous time.

Naive probability breaks down when computing probabilities of paths in continuous time or conditioning on zero-probability events (e.g., conditioning on the stock price hitting exactly $\$100.000$ at time $t$). Measure theory provides the rigorous framework—via $\sigma$-algebras (information sets), filtrations (time flow), and martingales (fair game equilibrium)—that guarantees derivative pricing models and risk estimators are mathematically consistent.

---

### 2. Mathematical Ground Truth & Derivations

#### The Probability Space $(\Omega, \mathcal{F}, \mathbb{P})$
1. **Sample Space $\Omega$:** The set of all possible market states or price paths $\omega$.
2. **$\sigma$-Algebra $\mathcal{F}$:** A collection of subsets of $\Omega$ containing $\emptyset$, closed under complementation and countable unions. An event $A \in \mathcal{F}$ is a question about the market to which an answer (Yes/No) can be assigned.
3. **Probability Measure $\mathbb{P}$:** A function $\mathbb{P}: \mathcal{F} \to [0, 1]$ such that $\mathbb{P}(\Omega) = 1$ and for mutually disjoint events $A_1, A_2, \dots$:
$$\mathbb{P}\left(\bigcup_{i=1}^\infty A_i\right) = \sum_{i=1}^\infty \mathbb{P}(A_i)$$

#### Filtrations & Information Flow
A **filtration** $\mathbb{F} = (\mathcal{F}_t)_{t \ge 0}$ is an increasing family of sub-$\sigma$-algebras:
$$\mathcal{F}_s \subseteq \mathcal{F}_t \subseteq \mathcal{F} \quad \forall 0 \le s \le t$$
$\mathcal{F}_t$ represents all market history and information revealed up to time $t$. A stochastic process $X_t$ is **adapted** to $\mathbb{F}$ if $X_t$ is $\mathcal{F}_t$-measurable for every $t$ (i.e., you cannot use future price information to evaluate current state).

#### Conditional Expectation
Given sub-$\sigma$-algebra $\mathcal{G} \subseteq \mathcal{F}$, the conditional expectation $\mathbb{E}[X | \mathcal{G}]$ is the unique $\mathcal{G}$-measurable random variable satisfying:
$$\int_A \mathbb{E}[X | \mathcal{G}] \, d\mathbb{P} = \int_A X \, d\mathbb{P} \quad \forall A \in \mathcal{G}$$
**Intuition:** $\mathbb{E}[X | \mathcal{G}]$ is the best $L^2$-projection of $X$ onto the information contained in $\mathcal{G}$.

#### Martingales: The Mathematical Definition of Fair Games
An adapted integrable stochastic process $M = (M_t)_{t \ge 0}$ is a **martingale** with respect to filtration $(\mathcal{F}_t)$ and measure $\mathbb{P}$ if:
$$\mathbb{E}[M_t \mid \mathcal{F}_s] = M_s \quad \forall 0 \le s \le t$$
- If $\mathbb{E}[M_t \mid \mathcal{F}_s] \ge M_s$, $M$ is a **submartingale** (expected upward drift, e.g., accumulated wealth).
- If $\mathbb{E}[M_t \mid \mathcal{F}_s] \le M_s$, $M$ is a **supermartingale** (expected downward drift, e.g., casino gambler's bankroll).

#### Radon-Nikodym Derivative & Change of Measure
Let $\mathbb{P}$ and $\mathbb{Q}$ be two probability measures on $(\Omega, \mathcal{F})$. $\mathbb{Q}$ is **absolutely continuous** with respect to $\mathbb{P}$ (written $\mathbb{Q} \ll \mathbb{P}$) if $\mathbb{P}(A) = 0 \implies \mathbb{Q}(A) = 0$.

By the Radon-Nikodym Theorem, there exists an almost surely non-negative random variable $Z \in L^1(\mathbb{P})$ such that:
$$\mathbb{Q}(A) = \int_A Z \, d\mathbb{P} \quad \forall A \in \mathcal{F}, \quad \text{denoted } Z = \frac{d\mathbb{Q}}{d\mathbb{P}}$$
This density $Z$ is the engine that converts physical real-world probabilities $\mathbb{P}$ into risk-neutral pricing probabilities $\mathbb{Q}$.

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_martingale_and_verify(n_paths: int = 10000, n_steps: int = 100):
    """
    Empirically verifies the martingale property E[M_T | M_t] = M_t
    using zero-mean random walk increments.
    """
    dt = 1.0 / n_steps
    # Increments with E[dX] = 0
    dx = np.random.normal(0, np.sqrt(dt), size=(n_paths, n_steps))
    paths = np.cumsum(dx, axis=1)
    
    t_inspect = 30
    T_end = 99
    
    # Group paths by state at time t_inspect
    states_at_t = paths[:, t_inspect]
    cond_mask = (states_at_t > 0.4) & (states_at_t < 0.6)
    
    actual_t_mean = np.mean(states_at_t[cond_mask])
    empirical_future_expectation = np.mean(paths[cond_mask, T_end])
    
    print(f"Conditioned state at t={t_inspect}: {actual_t_mean:.4f}")
    print(f"Empirical E[M_T | M_t]:               {empirical_future_expectation:.4f}")
    print(f"Martingale deviation:                 {abs(actual_t_mean - empirical_future_expectation):.4f}")

simulate_martingale_and_verify()
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Filtration Leakage (Lookahead Bias):**
   - *Failure:* In backtesting, computing a feature at bar $t$ using the bar's closing price $C_t$ before that close has actually occurred, or using summary statistics computed over the full sample.
   - *Root Cause:* The feature is not $\mathcal{F}_t$-measurable; it belongs to $\mathcal{F}_{t+\Delta t}$.

2. **Equivalent Measure Violation (Zero-Probability Blowup):**
   - *Failure:* If real-world measure $\mathbb{P}$ allows an asset to reach zero, but pricing measure $\mathbb{Q}$ assumes Geometric Brownian Motion ($S_t > 0$ almost surely), absolute continuity breaks down.
   - *Symptom:* Radon-Nikodym density $\frac{d\mathbb{Q}}{d\mathbb{P}}$ becomes undefined.

---

### 5. Canonical Literature & Study References

- **Shreve, Steven E.**: *Stochastic Calculus for Finance II: Continuous-Time Models*, Springer, Chapter 1 (General Probability Theory), Chapter 3 (State Prices and Measure Changes).
- **Williams, David**: *Probability with Martingales*, Cambridge University Press, Chapters 9-14 (Conditioning, Martingales).

---

### 6. Connected Graph Bridges

- Feeds into: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]]
- Feeds into: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial-trees|No-Arbitrage & Binomial Trees]]
- Feeds into: [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]]
