---
title: "06 — Advanced Extensions: Meta-Labeling, Denoised Covariance, HERC & RL Allocation"
tags:
  - pillar-machine-learning
  - ml-for-portfolio
  - meta-labeling
  - hrp
  - reinforcement-learning
---

**Basic Prerequisites:** all of [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02]]–[[pillars/07-machine-learning-altdata/ml-for-portfolio/05-failure-modes-and-practice|05]]. This page is the "where the field goes next" survey plus one flagship worked example (meta-labeling).

---

### 1. Intuition & Practical Objective

The ML-for-portfolio frontier is a set of refinements that attack the seam from both sides: make the *position* smarter about reliability, make the *covariance* cleaner, and make the *allocation* more robust. Four extensions dominate the practitioner toolkit:

1. **Meta-labeling** — train a *secondary* classifier to predict whether the primary model's side call is correct, and use its probability to size the bet (AFML Ch 3 & 10). This decouples *which side* (primary) from *how big* (secondary), and it is the single highest-leverage trick in the book: it upgrades a mediocre signal into a properly sized book without touching the primary model.
2. **Denoised covariance (Marcenko–Pastur) & robust frontier estimators** — collapse noise eigenvalues before inversion, or use MCD/TS/DNN covariance estimators to feed the optimizer a covariance that survives inversion (AFML 2018 Ch 16; *ML for Asset Managers* Ch 5–6; "A Robust Estimator of the Efficient Frontier").
3. **HERC (Hierarchical Equal Risk Contribution) & HRP-family** — extend HRP from inverse-variance bisection to *equal-risk* splits, giving cluster-aware risk contributions that beat both HRP and standard risk parity out-of-sample (Raffinot 2018).
4. **RL allocation** — treat position sizing as a sequential decision problem (MDP) and optimize the *policy* directly against a risk-adjusted reward, sidestepping the explicit forecast→position decomposition. Powerful, but data-hungry and prone to the low-signal overfitting that plagues all of Pillar 7.

The practical objective: know *when* each extension earns its complexity — meta-labeling when reliability is predictable, denoising when $N\approx T$, HRP/HERC when the covariance is too fragile to invert, RL only when you have enough clean data and a stable reward.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Meta-labeling as a two-stage bet sizer

Let the primary model emit a side call $s_t\in\{-1,+1\}$. Define the meta-label $z_t=\mathbb{1}[s_t \text{ is correct}]$, and fit a *secondary* classifier $q(x_t)=P(z_t=1\mid x_t)$ on features (including the primary's confidence) that predict whether the side call will succeed. Size the bet by the probability-mapped position from [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02]]:

$$z_t = \frac{q_t-\tfrac12}{\sqrt{q_t(1-q_t)}},\qquad m_t = 2\Phi(z_t)-1\;\in[-1,1],$$

and hold $m_t\cdot s_t$. The insight: the secondary model is trained on a *much* cleaner target ($z$ is binary, nearly deterministic given good features) than the primary's return forecast, so it can extract reliability structure the primary never uses. Meta-labeling is therefore "predict the *quality* of the primary prediction, then size by that quality."

#### 2.2 Denoising before inversion

Given a sample covariance $\hat\Sigma$ with eigen-decomposition $\hat\Sigma=\sum_i \lambda_i v_iv_i^\top$, the Marcenko–Pastur law bounds the eigenvalues of a pure-noise covariance in $[\lambda_-,\lambda_+]$ (function of $N,T,\sigma^2$). Collapse the $\lambda_i<\lambda_+$ directions to their average and keep only the $>$ band:

$$\hat\Sigma_{\text{den}} = \sum_{\lambda_i>\lambda_+}\lambda_i v_iv_i^\top + \bar\lambda_{\text{noise}}\sum_{\lambda_i\le\lambda_+} v_iv_i^\top .$$

This raises the floor of the spectrum (so $1/\lambda_{\min}^2$ no longer explodes) with almost no loss of structure. It is the modern upgrade of the shrinkage seen in [[pillars/07-machine-learning-altdata/ml-for-portfolio/04-ml-for-covariance-factors|04]]. (Full treatment in [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]].)

#### 2.3 HERC: from inverse-variance to equal-risk bisection

HRP ([[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]]) splits each cluster by inverse-variance of sub-variances, $\alpha=1-\frac{\tilde V^{(1)}}{\tilde V^{(1)}+\tilde V^{(2)}}$. **HERC** replaces that with an *equal-risk* bisection: choose $\alpha$ so the two sub-clusters contribute equal *risk* to the portfolio,

$$\text{choose }\alpha :\quad \alpha\, v^{(1)} = (1-\alpha)\, v^{(2)},\qquad v^{(j)}=\sqrt{w^{(j)\top}\Sigma^{(j)}w^{(j)}},$$

where $w^{(j)}$ is a risk-based (e.g. inverse-variance or equal-risk) allocation inside each cluster. The result is a tree allocation that equalizes risk contributions *across* the hierarchy rather than inverse-variance-splitting — empirically flatter and more robust than HRP on correlated universes.

#### 2.4 RL allocation (orientation)

Formulate allocation as an MDP: state = features + current portfolio, action = position vector, reward = risk-adjusted return (e.g. log-return or Sharpe proxy). The policy is optimized directly by policy gradient/PPO. The appeal is end-to-end (forecast and position rule are one object); the danger is the same low-SNR overfitting and non-stationarity that makes every Pillar-7 method fragile (see [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial-ML Pitfalls & Low SNR]]). Use RL only when the data and reward are stable enough for the extra variance to pay.

---

### 3. Computational Implementation — meta-labeling, end-to-end (verified)

numpy. A primary model emits a side call whose correctness is predictable from a reliability feature $r$, and whose moves are **big when reliability is low** — the exact regime where all-in sizing loses money. A secondary logistic classifier learns $P(\text{primary right}\mid r)$; its probability is mapped to a bet size $m=2\Phi(z)-1$. Numbers **re-executed and verified**.

```python
import numpy as np
from math import erf, sqrt
Phi = np.vectorize(lambda x: 0.5*(1+erf(x/sqrt(2))))

rng = np.random.default_rng(42)
T = 8000
d    = np.where(rng.random(T) < 0.52, 1.0, -1.0)   # latent favorable direction
r    = rng.normal(0, 1.0, T)                       # reliability feature
p_right = 1/(1+np.exp(-1.0*r))                     # P(primary call correct) ~ r
side = np.where(rng.random(T) < p_right, d, -d)    # primary model output
correct = np.where(side == d, 1.0, -1.0)           # is the primary call right?
move = np.clip(0.5 - 0.3*r, 0.02, None)            # moves BIG when r<0 (low reliability)
y    = correct*move + rng.normal(0, 1.0, T)        # realized return of holding the side
meta = (side == d).astype(float)                   # meta-label ground truth

def logistic_fit(rr, mm, steps=2000, lr=0.3):      # gradient-descent logistic
    a = b = 0.0
    for _ in range(steps):
        p = 1/(1+np.exp(-(a + b*rr)))
        a -= lr*(p-mm).mean(); b -= lr*((p-mm)*rr).mean()
    return a, b
cut = 5000
a, b = logistic_fit(r[:cut], meta[:cut])
p_meta = 1/(1+np.exp(-(a + b*r[cut:])))            # P(primary right) out-of-sample
z = (p_meta - 0.5)/np.sqrt(p_meta*(1-p_meta))      # AFML bet-size z-stat
m = 2*Phi(z) - 1                                   # bet size in [-1,1]

pos_naive = np.ones(len(m))                        # hold full size always
pos_meta  = m                                      # size by predicted reliability
def st(p):
    dd = p*y[cut:]
    return dd.mean()/dd.std()*np.sqrt(252), dd.std()*np.sqrt(252), np.abs(p).mean()
print("logistic (intercept, slope on r):", round(a,3), round(b,3))
for name, p in [("naive all-in", pos_naive), ("meta-label sized", pos_meta)]:
    shp, vol, avg = st(p)
    print(f"{name:18s} ann.Sharpe={shp:+.3f}  ann.vol={vol:5.1f}  avg|pos|={avg:.3f}")
```
```
logistic (intercept, slope on r): -0.068 0.97
naive all-in       ann.Sharpe=-1.599  ann.vol= 18.3  avg|pos|=1.000
meta-label sized   ann.Sharpe=+3.216  ann.vol=  7.3  avg|pos|=0.306
```

**What the numbers teach.** The primary model is not useless — it is right whenever reliability is high — but it is *wrong on the big days* (large moves coincide with low $r$). All-in sizing keeps a full position through those regimes and bleeds (Sharpe $-1.60$). The meta-label learns the reliability schedule out-of-sample ($P(\text{right}\mid r)$ via logistic on $r$), sizes down to an average position of $0.31$, and *both* raises the Sharpe to $+3.22$ *and* cuts vol from $18.3$ to $7.3$. That is the meta-labeling win: a better *position*, not a better forecast — exactly the seam this folder is about.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Meta-labeling inherits the primary's side errors.** The secondary model sizes the bet but cannot change the sign. If the primary is systematically wrong about *which side* (not just how reliable), meta-labeling only reduces how much you lose — it cannot make a bad side call good. Pair it with a trustworthy side model.
2. **Denoising mis-calibrates on short data.** Marcenko–Pastur needs $T$ large and correlations stable; on overlapping/short samples the noise band is wrong and denoising discards real structure or keeps noise. Validate on embargoed data.
3. **HERC adds parameters, not robustness, on small universes.** Equal-risk bisection needs reliable per-cluster risk estimates; with $N\approx T$ it inherits the same estimation error it tries to avoid. On thin data, plain HRP or $1/N$ is the honest choice.
4. **RL overfits the reward.** A policy gradient maximizing Sharpe on a short, non-stationary history memorizes that history. The low-signal, adaptive-market problem ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial-ML Pitfalls & Low SNR]]) makes RL the *least* robust of these four extensions unless data is long and reward is stable.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning* (2018), Ch 3 (meta-labeling) and Ch 10 (bet sizing from probabilities) — the meta-labeling machinery demonstrated in §3.
- **López de Prado**, *Machine Learning for Asset Managers* (2020), Ch 5–6 (Marcenko–Pastur denoising/detoning) and Ch 8 (clustering for allocation).
- **López de Prado**, "A Robust Estimator of the Efficient Frontier," SSRN 3469961, 2019 — MCD/SK/NaN/TS/DNN covariance estimators vs $1/N$.
- **Raffinot**, "The Hierarchical Equal Risk Contribution Portfolio," SSRN 3237540, 2018 — HERC.
- **Ang & Timmermann**, "Regime Changes and Financial Markets," *Annual Review of Financial Economics* 4:313–337, 2012 — regime structure behind allocation (bridges to [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm|Regime Classification]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/ml-for-portfolio/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Hub: [[pillars/07-machine-learning-altdata/ml-for-portfolio/index|Index Hub]]
- Extensions' homes: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity (HRP)]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm|Regime Classification]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]]
