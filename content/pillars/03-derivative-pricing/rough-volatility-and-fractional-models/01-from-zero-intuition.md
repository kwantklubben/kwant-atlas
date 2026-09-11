---
title: "01 — Rough Volatility from Zero: Why Log-Vol Is Rougher Than Brownian Motion"
tags:
  - pillar-derivative-pricing
  - rough-volatility-and-fractional-models
  - intuition
  - fractional-brownian-motion
  - hurst-exponent
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (or none — this page is written to stand alone).

---

### 1. Intuition & Practical Objective

Stochastic-volatility models made volatility random but kept it *smooth*: a diffusion's increments scale like $\sqrt{\Delta t}$. The market disagrees. Measure daily log-volatility $\ln\sigma_t$ and look at how its *increments* scale with the lag $\Delta$:

$$\mathbb E\big[(\ln\sigma_{t+\Delta}-\ln\sigma_t)^2\big]=\nu^2\Delta^{2H}.$$

If $\ln\sigma$ were a diffusion, $H=\tfrac12$. The data say **$H\approx0.1$** (Gatheral–Jaisson–Rosenbaum 2018). A process with $H<\tfrac12$ is **rougher** than Brownian motion: its increments are *anti-correlated* (a step up is more likely followed by a step down), and its paths have fractal dimension $2-H>1.5$ — visibly wiggly, not smooth.

Three "aha"s:

1. **Rough ≠ jumpy, rough = anti-persistent.** A fractional Brownian motion with $H=0.14$ is a continuous Gaussian process (no jumps) whose increments have *negative* autocorrelation. This is the opposite of "long memory" (which is $H>\tfrac12$). Rough vol is *anti-persistent* noise with a power-law covariance kernel $(t-s)^{H-1/2}$.
2. **H is a single knob that sets every short-dated property.** The same exponent controls the increment variance ($\Delta^{2H}$), the autocorrelation sign, the fractal dimension ($2-H$), *and* the ATMF skew term structure $\psi(T)\propto T^{H-\frac12}$. One number, and the whole short end follows.
3. **The skew is the forensic evidence.** Markovian SV models (Heston, SABR, $n$-factor Bergomi) generate an ATMF skew that *caps* as $T\to0$. The market's SPX skew grows like $T^{-0.44}$. The only way to get a *blowing-up* short skew is a power-law kernel with $H<1/2$.

The practical objective: internalise that "rough" is a precise, measurable statement about the *scaling exponent of log-vol increments* — not a vague notion of turbulence — and that the single number $H\approx0.1$ is both an empirical fact and the design parameter that fixes the short-dated skew.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Fractional Brownian motion in one line

fBm $W^H_t$ is the Gaussian process with autocovariance (Mandelbrot–Van Ness 1968)

$$\boxed{\;\mathbb E[W^H_tW^H_s]=\frac12\big(|t|^{2H}+|s|^{2H}-|t-s|^{2H}\big)\;}$$

For $H=\tfrac12$ this collapses to $\mathbb E[W_tW_s]=\min(t,s)$ — ordinary Brownian motion. For $H\neq\tfrac12$ it is neither a martingale nor a Markov process, but it has **stationary increments**: $W^H_{t+\Delta}-W^H_t$ has the same law as $W^H_\Delta$, and

$$\mathbb E\big[(W^H_{t+\Delta}-W^H_t)^2\big]=\Delta^{2H}$$

(stationary increments give this exactly, as verified in §3). It is this exact $\Delta^{2H}$ law that GJR estimate as $\nu^2\Delta^{2H}$ on log-volatility.

#### 2.2 Why H<1/2 means anti-persistence

The lag-1 autocorrelation of fBm increments $X_i=W^H_{i+1}-W^H_i$ is

$$\rho_1=\frac{\mathbb E[X_iX_{i+1}]}{\mathbb E[X_i^2]}=\frac12\big(2^{2H}-2\big),$$

which is **negative** for $H<\tfrac12$, zero at $H=\tfrac12$, **positive** for $H>\tfrac12$. So $H=0.14\Rightarrow\rho_1=\tfrac12(2^{0.28}-2)\approx-0.393$: after a volatility spike the next increment is more likely to reverse it — vol clusters *because* it reverts. This is the single cleanest number distinguishing rough ($H\ll\tfrac12$) from smooth ($H>\tfrac12$) from Brownian ($H=\tfrac12$).

#### 2.3 The RFSV model and the monofractal scaling

GJR model log-vol directly as fBm ("Rough Fractional Stochastic Volatility"):

$$\log\sigma_{t+\Delta}-\log\sigma_t=\nu\big(W^H_{t+\Delta}-W^H_t\big),$$

so $\mathbb E[(\ln\sigma_{t+\Delta}-\ln\sigma_t)^2]=\nu^2\Delta^{2H}$. They further check the **monofractal scaling** of the $q$-th sample moments $m(q,\Delta)=\langle|\ln\sigma_{t+\Delta}-\ln\sigma_t|^q\rangle\propto\Delta^{\zeta_q}$ and find $\zeta_q=qH$ with $H\approx0.13$ on SPX — the signature of a single Gaussian (fractional) driver rather than a multifractal cascade. The exponent $\alpha=H-\tfrac12\approx-0.36$ is what the skew will inherit (§03, §02).

---

### 3. Computational Implementation — H's sign decides persistence

We compute the fBm increment autocorrelation exactly from the covariance formula, for $H$ from anti-persistent ($0.14$) through Brownian ($0.5$) to persistent ($0.9$). Stdlib only — no simulation needed, the answer is a closed-form number.

```python
import math
def fbm_inc_cov(d, H):
    """Cov[ X_i, X_{i+d} ] for unit-lag fBm increments X_i = W^H_{i+1}-W^H_i, Var[X_i]=1."""
    if d == 0: return 1.0
    return 0.5*(abs(d+1)**(2*H) + abs(d-1)**(2*H) - 2*abs(d)**(2*H))
print("== fBm increment autocorrelation Cov[X_i, X_{i+d}] (unit-lag, Var[X_i]=1) ==")
print("   X_i = W^H_{i+1} - W^H_i ; H=1/2 -> white noise (all 0); H<1/2 -> negative (anti-persistent)")
for H in (0.14, 0.30, 0.50, 0.70, 0.90):
    row = "  ".join(f"lag{d}:{fbm_inc_cov(d,H):+.3f}" for d in (1,2,5,10))
    print(f"H={H:4.2f}  {row}")
print("\nLag-1 formula check: rho_1 = 0.5*(2^(2H)-2)")
for H in (0.14, 0.50, 0.90):
    print(f"  H={H:4.2f}  closed form 0.5*(2^{{2H}}-2) = {0.5*(2**(2*H)-2):+.4f}  (matches lag1 above)")
```
```
== fBm increment autocorrelation Cov[X_i, X_{i+d}] (unit-lag, Var[X_i]=1) ==
   X_i = W^H_{i+1} - W^H_i ; H=1/2 -> white noise (all 0); H<1/2 -> negative (anti-persistent)
H=0.14  lag1:-0.393  lag2:-0.034  lag5:-0.006  lag10:-0.002
H=0.30  lag1:-0.242  lag2:-0.049  lag5:-0.013  lag10:-0.005
H=0.50  lag1:+0.000  lag2:+0.000  lag5:+0.000  lag10:+0.000
H=0.70  lag1:+0.320  lag2:+0.189  lag5:+0.107  lag10:+0.070
H=0.90  lag1:+0.741  lag2:+0.630  lag5:+0.522  lag10:+0.454

Lag-1 formula check: rho_1 = 0.5*(2^(2H)-2)
  H=0.14  closed form 0.5*(2^{2H}-2) = -0.3929  (matches lag1 above)
  H=0.50  closed form 0.5*(2^{2H}-2) = +0.0000  (matches lag1 above)
  H=0.90  closed form 0.5*(2^{2H}-2) = +0.7411  (matches lag1 above)
```

Read the table:
1. **H=0.14 increments are anti-correlated** ($\rho_1=-0.393$), and the autocorrelation *decays* with lag ($-0.393\to-0.002$): rough vol is *not* long memory — it is short-range anti-persistence. This is exactly GJR's §4 point: the data are rough, not long-memory.
2. **H=1/2 is pure white noise** (all zeros) — ordinary Brownian increments. This is the smooth/diffusive benchmark that Heston and SABR assume.
3. **H=0.9 is persistent** ($\rho_1=+0.741$) — the "smooth, slowly-mean-reverting vol" of the pre-rough era, and the direction you must *not* go if the data say $H\approx0.1$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Rough means turbulent/jumpy."** No — a fractional Brownian motion with $H=0.14$ is continuous and Gaussian. Roughness is about the *scaling exponent of increments* (and hence fractal dimension $2-H>1.5$), not about discontinuities. Rough ≠ Lévy.
2. **"Rough = long memory."** The opposite. $H<1/2$ is anti-persistent; classical long-memory estimators (R/S, fractional differencing) are exactly the tools that *falsely* certify long memory on rough data (GJR §4). Get the sign of the exponent wrong and you build the wrong model.
3. **Estimating H from a too-short sample.** The variogram slope needs many lags; with a handful of days the estimator is badly biased (GJR use thousands of daily obs across 21 indices). H≈0.1 is a *population* claim.
4. **Reading H off a single skew slice.** The short-time skew gives $\eta\sqrt{2H}$ (product), not H alone. You need the *variogram of log-vol* or several maturities to separate the roughness from the vol-of-vol.
5. **Confusing the physical ($\mathbb P$) and risk-neutral ($\mathbb Q$) measures.** GJR's H is estimated from *realized* variance (physical measure). Pricing uses the $\mathbb Q$ forward-variance curve; the roughness parameter is assumed to pass through the change of measure (BFG), but the vol-of-vol $\eta$ need not.

---

### 5. Canonical Literature & Study References

- **Gatheral, Jaisson & Rosenbaum (2018)**, *Volatility is rough*, Quantitative Finance 18(6), 933–949 — the empirical finding: $\mathbb E[(\ln\sigma_{t+\Delta}-\ln\sigma_t)^2]=\nu^2\Delta^{2H}$ with $H\approx0.1$ on 21 indices (SPX $H{=}0.13,\nu{=}0.32$); monofractal scaling $\zeta_q=qH$; §4 on **spurious long memory**. *The empirical ground truth of this page.*
- **Mandelbrot & Van Ness (1968)**, *Fractional Brownian motions, fractional noises and applications*, SIAM Review 10(4), 422–437 — the fBm covariance and the Hurst-parameter framework.
- **Bennedsen, Lunde & Pakkanen (2017)**, *Hybrid scheme for Brownian semistationary processes*, Finance and Stochastics 21(4), 931–965 — how rough processes are actually simulated (and why naive schemes fail).
- **Fukasawa (2017)**, *Short-time at-the-money skew and rough fractional volatility* — the theory linking H to the short-time skew.
- **Hull**, *Options, Futures, and Other Derivatives*, ch 20 §20.3 (why smiles exist) and ch 23 (volatility term structure) — the classical baseline this folder extends.

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] (BM as the H=1/2 case) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Gaussian processes, self-similarity) · [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (the constant-σ zero point)
- Continue: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/03-fractional-brownian-motion-and-derivations|03 · fBm & Derivations]] · [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/01-from-zero-intuition|Heston · 01 From Zero]] (why variance must be a process — the Markovian step that rough vol then out-roughs) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/01-from-zero-intuition|VS · 01 From Zero]]
