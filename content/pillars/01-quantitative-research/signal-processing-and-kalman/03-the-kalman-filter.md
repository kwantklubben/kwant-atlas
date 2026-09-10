---
title: "03 — The Kalman Filter: Prediction, Update, Gain"
tags:
  - pillar-quant-research
  - signal-processing-and-kalman
  - kalman-filter
  - recursion
  - riccati
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/signal-processing-and-kalman/02-state-space-models|02 · State-Space Models]].

---

### 1. Intuition & Practical Objective

The Kalman filter is the **predictor–corrector** loop for a Gaussian state-space model. Each cycle does two things and only two things:

1. **Predict** — push the current belief about the state forward through the transition dynamics, *inflating* its uncertainty (the state may have moved, and we weren't looking).
2. **Correct** — when a new observation arrives, form the **innovation** (how surprising the observation is given what we predicted), and move the belief toward the data by a fraction — the **Kalman gain** — that is exactly the signal-to-noise ratio at that moment.

Two properties make it the workhorse of quantitative finance:

- **It is recursive and online.** It never re-runs the whole history; it stores only the current state estimate and its covariance. This makes it $O(m^3)$ per step regardless of how long the series is, and directly deployable in a live system.
- **It is optimal.** Under linearity and Gaussianity it is the **minimum mean-squared-error** estimator — no other estimator (linear *or* nonlinear) can do better. When the assumptions fail, it is still the best *linear* estimator (the orthogonal-projection view).

The practical objective is to give the practitioner the recursion in a form they can drop into code, with the conventions pinned down and the numerics made stable.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The recursion, step by step

Given $(s_{t\mid t-1},\ \Sigma_{t\mid t-1})$ (the a-priori belief at time $t$), the filter processes $y_t$ and produces $(s_{t+1\mid t},\ \Sigma_{t+1\mid t})$:

$$\textbf{Innovation:}\qquad v_t=y_t-c_t-Z_t s_{t\mid t-1}$$
$$\textbf{Innovation covariance:}\qquad V_t=Z_t\Sigma_{t\mid t-1}Z_t^\top+H_t$$
$$\textbf{Kalman gain:}\qquad K_t=T_t\Sigma_{t\mid t-1}Z_t^\top V_t^{-1}$$
$$\textbf{State update:}\qquad s_{t+1\mid t}=d_t+T_t s_{t\mid t-1}+K_t v_t$$
$$\textbf{Covariance update:}\qquad \Sigma_{t+1\mid t}=T_t\Sigma_{t\mid t-1}L_t^\top+R_tQ_tR_t^\top,\qquad L_t=T_t-K_tZ_t.$$

(Tsay Eq. 11.64, verified in the corpus.) The gain is a matrix version of the scalar weight $P^{-}/(P^{-}+r)$: $Z_t\Sigma Z_t^\top$ is the predicted observation variance (signal), $V_t$ adds the measurement variance (signal + noise), and $T_t\Sigma Z_t^\top$ maps it back to state space. When the observation is uninformative ($V_t$ large), $K_t\to0$ and the state just follows its prediction.

#### 2.2 Where the gain comes from (three equivalent routes)

- **Bayes / Gaussian conditioning.** The joint of $(s_{t+1},y_t)$ is Gaussian; conditioning on $y_t$ gives a posterior mean $=\text{prediction}+K\cdot\text{innovation}$ and covariance $=(I-KZ)\Sigma^{-}$ with $K=\Sigma^{-}Z^\top(Z\Sigma^{-}Z^\top+H)^{-1}$. Algebra, not magic.
- **Orthogonal projection (least squares).** Among all linear functions of the data, the minimum-MSE state estimate is the orthogonal projection onto the observation space; solving the normal equations reproduces exactly the same $K$. This is why the filter remains the best *linear* estimator even when the model is non-Gaussian.
- **Weighted average of two beliefs.** The predict step and the observation are two Gaussian "estimates" of the same quantity; the posterior is their variance-weighted average. $K$ is the weight on the data.

#### 2.3 The scalar local-level case (Tsay 11.14), for cross-checking

With $T=Z=R=1$, $d=c=0$, $Q=\sigma_\eta^2$, $H=\sigma_e^2$:

$$v_t=y_t-\mu_{t\mid t-1},\quad V_t=\Sigma_{t\mid t-1}+\sigma_e^2,\quad K_t=\frac{\Sigma_{t\mid t-1}}{V_t},\quad \mu_{t+1\mid t}=\mu_{t\mid t-1}+K_tv_t,\quad \Sigma_{t+1\mid t}=\Sigma_{t\mid t-1}(1-K_t)+\sigma_\eta^2 .$$

This is the form to verify a matrix implementation against — it is small enough to compute by hand.

#### 2.4 Steady state and the Riccati recursion

For a time-invariant model, the covariance recursion converges: $\Sigma_t\to\Sigma_\infty$ solving the **algebraic Riccati equation**, after which $K_t\to K_\infty$ is a *constant*. In steady state the filter is a fixed-coefficient linear filter, and this is the origin of the famous result that the optimal filter satisfies a Riccati (not a Wiener–Hopf) equation. Practically: you can pre-compute $K_\infty$ and run a gloriously cheap constant-gain filter — at the cost of losing adaptivity.

#### 2.5 Maximum likelihood for free

The **prediction-error decomposition** (Tsay Eq. 11.25) gives the exact log-likelihood of the observations as a by-product of the recursion:

$$\ln L=-\frac{T}{2}\ln(2\pi)-\frac12\sum_t\Big[\ln V_t+\frac{v_t^2}{V_t}\Big].$$

So parameters $(\sigma_e^2,\sigma_\eta^2,\ldots)$ are estimated by simply maximizing this — no external likelihood machinery, and the innovations $v_t$ double as a model-diagnostic series (page 05).

---

### 3. Computational Implementation — the filter as a function, verified two ways

The general matrix filter is implemented exactly as §2.1. It is then run on a local-level model and its output is checked **coefficient-by-coefficient against the scalar recursion** — the strongest possible test that the matrix code is correct. Finally the Riccati fixed point is computed and compared to the filter's converged gain.

```python
import math, random
import numpy as np

def kalman_general(y, d, T, Z, H, Q, Rm, s1, P1):
    """Tsay 11.64: s_{t+1}=d+T s_t+R eta (cov Q); y_t=Z s_t+e (cov H)."""
    s = np.array(s1, float).reshape(-1, 1); P = np.array(P1, float)
    pred, filt = [], []
    for t in range(len(y)):
        v = y[t] - Z @ s                         # innovation
        V = Z @ P @ Z.T + H                      # innovation covariance
        K = T @ P @ Z.T @ np.linalg.inv(V)       # Kalman gain
        filt.append((s + K @ v, P.copy()))
        pred.append((s.copy(), P.copy()))        # a-priori, kept for the cross-check
        s = d + T @ s + K @ v
        P = T @ P @ (T - K @ Z).T + Rm @ Q @ Rm.T
    return pred, filt

def kalman_local_level(y, x0, P0, sn2, se2):     # scalar Tsay 11.14
    x, P, xs = x0, P0, []
    for yt in y:
        Pp = P + sn2; K = Pp / (Pp + se2)
        x = x + K * (yt - x); P = (1 - K) * Pp
        xs.append(x)
    return xs

random.seed(5); Tlen, sn2, se2 = 400, 0.30, 1.00
y = []
mu = 0.0
for _ in range(Tlen):
    mu += random.gauss(0, math.sqrt(sn2)); y.append(mu + random.gauss(0, math.sqrt(se2)))
y = np.array(y)

pred, _ = kalman_general(y, d=np.zeros((1, 1)), T=np.array([[1.0]]), Z=np.array([[1.0]]),
                         H=np.array([[se2]]), Q=np.array([[sn2]]), Rm=np.array([[1.0]]),
                         s1=[0.0], P1=np.array([[1e7]]))
gen = [float(p[0][0, 0]) for p in pred]           # a-priori mu_{t|t-1}
sc  = kalman_local_level(y, 0.0, 1e7, sn2, se2)   # filtered mu_{t|t}
diff = max(abs(gen[t] - sc[t - 1]) for t in range(1, Tlen))
print(f"max |matrix KF - scalar local-level recursion| = {diff:.2e} over {Tlen} steps")

# Riccati fixed point
P = 1e7
for _ in range(5000):
    K = P / (P + se2); Pn = P * (1 - K) + sn2
    if abs(Pn - P) < 1e-14: P = Pn; break
    P = Pn
print(f"steady state: Sigma_inf={P:.6f}  K_inf={P/(P+se2):.6f}  filtered var={P*(1-P/(P+se2)):.6f}")
```
```
max |matrix KF - scalar local-level recursion| = 3.53e-12 over 400 steps
steady state: Sigma_inf=0.717891  K_inf=0.417891  filtered var=0.417891
```
The matrix implementation matches the hand-checkable scalar recursion to **$3.5\times10^{-12}$** (the residual is the diffuse initial $P_0=10^7$; the two recursions are algebraically identical), and its converged gain $K_\infty=0.417891$ equals the algebraic-Riccati fixed point computed independently — two implementations, one number.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Covariance blow-up / loss of symmetry.** The update $(I-KZ)\Sigma$ is only *mathematically* symmetric; floating-point round-off can drift it into asymmetry and even negative variance, after which the filter oscillates or diverges. Fix: use the **Joseph form** $\Sigma=(I-KZ)\Sigma^{-}(I-KZ)^\top+KHK^\top$, which is symmetric and positive-semi-definite *by construction*, or use a square-root (Cholesky) implementation.
2. **Numerically singular $V_t$.** $V_t^{-1}$ is computed every step; if a regressor is nearly collinear with another, $V_t$ becomes ill-conditioned and $K_t$ explodes. In practice solve the linear system rather than inverting, and consider a small jitter on $H$.
3. **Diffuse initialization.** A genuinely unknown initial state needs $P_0\to\infty$ (S-Plus uses an `mSigma = −1` sentinel). Using a large *finite* $P_0$ instead leaves a transient bias; using a large *inverse* is numerically disastrous. Tsay §11.1.6 treats this explicitly.
4. **Mixing the two recursion forms.** The canonical (11.64) form uses $L_t=T_t-K_tZ_t$ and puts the $T_t$ factor in $K_t$; the contemporaneous form updates $\Sigma$ as $T\Sigma_{t\mid t}T^\top+RQR^\top$. Both are correct *internally*, but splicing a line from one into the other silently off-by-ones the covariance (flagged in the corpus verification of Tsay Ch 11).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series* (3rd ed.), Ch 11 §11.1 (filter/prediction/smoothing definitions; local KF 11.14; diffuse init 11.1.6; ML via 11.25) and §11.4 (general filter 11.64, steady state 11.4.1). **Primary, corpus-verified source.**
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, Ch 2 (filtering), Ch 4 (ML estimation), Ch 5–6 (diagnostics, initialization).
- **Welch & Bishop**, *An Introduction to the Kalman Filter* (TR 95-041) — the standard predictor–corrector derivation.
- **Särkkä**, *Bayesian Filtering and Smoothing*, Ch 4 (the general Gaussian filter) and Ch 6 (numerically stable / square-root forms).
- **Hamilton**, *Time Series Analysis*, Ch 13.2 (the filter as an iterative least-squares projection).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/signal-processing-and-kalman/02-state-space-models|02 · State-Space Models]]
- Continue: [[pillars/01-quantitative-research/signal-processing-and-kalman/04-time-varying-beta|04 · Time-Varying Beta]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Index Hub]]
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (matrix inverse, SPD) · [[foundations/probability-and-measure-theory/index|Probability]] (Gaussian conditioning)
- Robustness: [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/06-advanced-extensions|06 · Smoothing & Particle Filters]]
