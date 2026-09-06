---
title: "Regime Classification: HMM & GMM"
tags:
  - pillar-ml-altdata
  - regime-classification
  - hmm
  - gmm
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory|Probability Theory]] and [[foundations/econometrics-and-time-series|Econometrics]].

---

### 1. Intuition & Practical Objective

Financial markets do not operate under a single stationary Gaussian distribution. Markets oscillate between distinctly different **macroeconomic regimes**:
- **Low-Volatility Bull Regime:** Steady upward trend, low volatility, mean-reversion works, credit spreads tight.
- **High-Volatility Crisis / Panic Regime:** Severe drawdowns, volatility spikes, correlations converge to 1, trend following thrives, mean-reversion blows up.

Applying a trading strategy calibrated for a calm regime during a high-volatility panic causes immediate capital destruction. **Hidden Markov Models (HMM)** and **Gaussian Mixture Models (GMM)** infer the unobservable underlying market state directly from data, dynamically switching portfolio risk limits.

---

### 2. Mathematical Ground Truth & Derivations

#### Hidden Markov Model (HMM) Formulation
Let $S_t \in \{1, 2, \dots, K\}$ be the unobservable discrete latent market regime at time $t$.
1. **Transition Probability Matrix $A$:**
$$A_{ij} = \mathbb{P}(S_t = j \mid S_{t-1} = i), \quad \sum_{j=1}^K A_{ij} = 1$$
2. **Emission Distribution $B$:**
Given state $S_t = k$, observed market returns $y_t$ are drawn from state-dependent Gaussian distributions:
$$y_t \mid (S_t = k) \sim \mathcal{N}(\mu_k, \sigma_k^2)$$

#### Training via Baum-Welch (Expectation-Maximization)
1. **E-Step (Forward-Backward Algorithm):**
   - Compute forward variable $\alpha_t(i) = \mathbb{P}(y_1, \dots, y_t, S_t = i)$
   - Compute backward variable $\beta_t(i) = \mathbb{P}(y_{t+1}, \dots, y_T \mid S_t = i)$
   - Posterior state probability:
$$\gamma_t(i) = \mathbb{P}(S_t = i \mid Y) = \frac{\alpha_t(i) \beta_t(i)}{\sum_{j=1}^K \alpha_t(j) \beta_t(j)}$$
2. **M-Step:**
   - Update transition probabilities and state emission parameters $(\mu_k, \sigma_k)$ by maximizing the expected log-likelihood.

#### Decoding the Optimal State Path: The Viterbi Algorithm
Finds the single most probable sequence of hidden states $S_{1:T}^*$:
$$S_{1:T}^* = \arg\max_{S_1, \dots, S_T} \mathbb{P}(S_1, \dots, S_T \mid y_1, \dots, y_T)$$

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_regime_switching_returns(T: int = 1000) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulates a 2-state market: State 0 (Bull Low-Vol) vs State 1 (Bear High-Vol).
    """
    np.random.seed(42)
    # Transition matrix: A[0,0]=0.98, A[1,1]=0.92
    A = np.array([[0.98, 0.02],
                  [0.08, 0.92]])
    # Regimes: Bull (mu=10% ann, vol=12%), Bear (mu=-20% ann, vol=35%)
    params = [
        {"mu": 0.10 / 252, "sig": 0.12 / np.sqrt(252)},
        {"mu": -0.20 / 252, "sig": 0.35 / np.sqrt(252)}
    ]
    
    states = np.zeros(T, dtype=int)
    returns = np.zeros(T)
    curr_state = 0
    
    for t in range(T):
        curr_state = 0 if np.random.uniform() < A[curr_state, 0] else 1
        states[t] = curr_state
        p = params[curr_state]
        returns[t] = np.random.normal(p["mu"], p["sig"])
        
    return states, returns

states, rets = simulate_regime_switching_returns(1000)
print(f"Sample generated: Bull days={np.sum(states==0)} | Bear days={np.sum(states==1)}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **State Label Switching & Inversion:**
   - *Failure:* HMM is unsupervised; after re-training, "State 0" and "State 1" can swap definitions.
   - *Symptom:* If an automated risk engine hardcodes "State 0 = Bull", an inverted model will max out leverage during a market crash.
   - *Remedy:* Explicitly enforce ordering constraints on variance ($\sigma_1 < \sigma_2 < \dots < \sigma_K$).

2. **Lag in Real-Time State Detection:**
   - *Failure:* HMM requires several consecutive negative return days to accumulate sufficient posterior probability that a regime shift has occurred.

---

### 5. Canonical Literature & Study References

- **Hamilton, James D.**: *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle*, Econometrica 57(2), 357-384 (1989).
- **Tsay, Ruey S.**: *Analysis of Financial Time Series*, Chapter 4 (Nonlinear Models).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/econometrics-and-time-series|Econometrics]]
- Bridges to: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing]]
- Bridges to: [[pillars/01-quantitative-research/cross-sectional-and-time-series-momentum|Momentum Strategies]]
