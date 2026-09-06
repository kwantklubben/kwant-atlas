---
title: "Signal Processing & Kalman Filtering"
tags:
  - pillar-quant-research
  - kalman-filter
  - signal-processing
  - state-space
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices|Linear Algebra]] and [[foundations/probability-and-measure-theory|Probability Theory]] (Bayesian Updating).

---

### 1. Intuition & Practical Objective

Asset prices in financial markets are corrupted by high-frequency noise, bid-ask bounce, and microstructure friction. Static regression models (like rolling OLS) suffer from a crippling trade-off: short windows are too noisy, while long windows react too slowly to genuine structural shifts.

The Kalman filter solves this recursively. By modeling the underlying parameter (such as a hedge ratio or latent macro factor) as a hidden state vector that evolves dynamically, the Kalman filter optimally updates its state estimate upon receiving each new noisy price observation, balancing prediction uncertainty against measurement noise.

---

### 2. Mathematical Ground Truth & Derivations

#### Linear State-Space Representation
1. **State Transition Equation (Latent State Evolution):**
$$x_t = F_t x_{t-1} + B_t u_t + w_t, \quad w_t \sim \mathcal{N}(0, Q_t)$$
2. **Measurement Equation (Noisy Price Observation):**
$$y_t = H_t x_t + v_t, \quad v_t \sim \mathcal{N}(0, R_t)$$
where $Q_t$ is process noise covariance and $R_t$ is measurement noise covariance.

#### Dynamic Hedge Ratio Estimation
In pairs trading, let $y_t = P_t^A$ (price of asset A) and observation matrix $H_t = [P_t^B, \; 1]$. The state vector $x_t = [\beta_t, \; \alpha_t]^T$ contains the dynamic hedge ratio and spread intercept.

#### Recursive Kalman Filter Update Equations
For each incoming bar $t$:
1. **Predict (A Priori Step):**
$$\hat{x}_{t|t-1} = F_t \hat{x}_{t-1|t-1}$$
$$P_{t|t-1} = F_t P_{t-1|t-1} F_t^T + Q_t$$
2. **Compute Innovation & Gain:**
$$\tilde{y}_t = y_t - H_t \hat{x}_{t|t-1} \quad \text{(Measurement Innovation)}$$
$$S_t = H_t P_{t|t-1} H_t^T + R_t \quad \text{(Innovation Covariance)}$$
$$K_t = P_{t|t-1} H_t^T S_t^{-1} \quad \text{(Optimal Kalman Gain)}$$
3. **Update (A Posteriori Step):**
$$\hat{x}_{t|t} = \hat{x}_{t|t-1} + K_t \tilde{y}_t$$
$$P_{t|t} = (I - K_t H_t) P_{t|t-1}$$

---

### 3. Computational Implementation

```python
import numpy as np

class DynamicBetaKalman:
    def __init__(self, delta: float = 1e-4, R: float = 1e-3):
        """
        delta: Controls process noise Q = (delta / (1 - delta)) * I
        R: Measurement noise variance
        """
        self.delta = delta
        self.R = R
        self.x = np.zeros((2, 1))           # [beta, alpha]^T
        self.P = np.eye(2)                  # State covariance
        self.Q = (delta / (1 - delta)) * np.eye(2)
        
    def update(self, price_a: float, price_b: float) -> tuple[float, float, float]:
        H = np.array([[price_b, 1.0]])
        y = price_a
        
        # 1. Predict
        x_pred = self.x
        P_pred = self.P + self.Q
        
        # 2. Innovation & Gain
        y_hat = float(H @ x_pred)
        error = y - y_hat
        S = float(H @ P_pred @ H.T) + self.R
        K = (P_pred @ H.T) / S
        
        # 3. Update
        self.x = x_pred + K * error
        self.P = (np.eye(2) - K @ H) @ P_pred
        
        beta, alpha = float(self.x[0, 0]), float(self.x[1, 0])
        return beta, alpha, error
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Filter Lagging Behind Sudden Regimes:**
   - *Failure:* If process noise $Q$ is parameterized too small, the filter assumes the state is nearly static and reacts with severe lag when a genuine structural break occurs.
   - *Remedy:* Implement an adaptive $Q$-matrix scaled by recent innovation variance $S_t$.

2. **Divergence Due to Numerical Asymmetry:**
   - *Failure:* Repeated floating-point matrix multiplications can cause error covariance $P$ to lose symmetry or positive definiteness.
   - *Remedy:* Force Joseph form update: $P = (I - KH)P(I - KH)^T + KRK^T$.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series*, Chapter 11 (State-Space Models and the Kalman Filter).
- **Chan, Ernest P.**: *Algorithmic Trading: Winning Strategies and Their Rationale*, Wiley, Chapter 3 (Pairs Trading and Kalman Filtering).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/linear-algebra-and-matrices|Linear Algebra]]
- Bridges to: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading|Statistical Arbitrage]]
- Bridges to: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm|Regime Classification]]
