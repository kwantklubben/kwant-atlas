---
title: "02 — The Sample-Covariance Problem: Curse of Dimensionality & the Marchenko–Pastur Law"
tags:
  - pillar-portfolio-optimization
  - covariance-shrinkage
  - marchenko-pastur
  - random-matrix-theory
  - curse-of-dimensionality
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/01-from-zero-intuition|01 · From Zero]] and [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (eigenvalues, Wishart matrices).

---

### 1. Intuition & Practical Objective

Page 01 showed *that* the sample covariance fools the optimizer. This page shows *why*, with the mathematics of how a sample covariance's eigenvalues are distributed. The practical objective: give you the **$q=N/T$ diagnostic** and the **Marchenko–Pastur law**, so that before you trust any covariance matrix you can ask "how much of this spectrum is even distinguishable from noise?" and get a quantitative answer.

The key insight, due to the random-matrix-theory (RMT) literature (Laloux et al. 1999; Plerou et al. 2002): **if the true covariance were pure noise (identity), the sample covariance would still have a *spread* of eigenvalues — a whole interval $[\lambda_-,\lambda_+]$ — simply because of finite sampling.** That spread is not information; it is the fingerprint of estimation error. Any *real* covariance structure must show up as eigenvalues pushed **outside** this noise band. Everything inside the band is, statistically, noise dressed up as correlation.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The curse of dimensionality: parameters vs data

A covariance matrix has $P=N(N+1)/2$ free parameters. The data supply $NT$ numbers. The information per parameter is $2T/(N+1)$. Three regimes:

| Regime | Condition | Consequence |
|---|---|---|
| Classical | $N$ fixed, $T\to\infty$ | $S\to\Sigma$, $\kappa$ bounded, shrinkage intensity $\to0$ |
| High-dimensional | $q=N/T\in(0,1)$ | $S$ invertible but **ill-conditioned**; eigenvalues biased; shrinkage intensity stays strictly positive |
| Singular | $N\ge T$ | $S$ has rank $\le T-1$; **not invertible**; $\kappa=\infty$ |

This is why Ledoit & Wolf work in *general asymptotics*: both $N,T\to\infty$ with $q=N/T\to$ constant. In that framework the optimal shrinkage intensity **does not vanish** — it tends to a positive limiting constant, which is exactly why shrinkage helps in real portfolios and not just in tiny samples.

#### 2.2 The Marchenko–Pastur law

Let $X\in\mathbb{R}^{T\times N}$ have i.i.d. zero-mean entries of variance $\sigma^2$. As $N,T\to\infty$ with $N/T\to q\in(0,1]$, the empirical eigenvalue distribution of $S=\tfrac1T X^\top X$ converges to the **Marchenko–Pastur density**

$$
f(\lambda)=\frac{1}{2\pi\sigma^2 q\,\lambda}\sqrt{(\lambda_+-\lambda)(\lambda-\lambda_-)}\;\mathbf 1_{[\lambda_-,\lambda_+]},\qquad \lambda_\pm=\sigma^2\bigl(1\pm\sqrt q\bigr)^2 .
$$

Three facts to internalize:

- **The support is a band, not a point.** Even for $\Sigma=I$, the sample eigenvalues are spread across $[\sigma^2(1-\sqrt q)^2,\ \sigma^2(1+\sqrt q)^2]$.
- **The band widens with $q$.** At $q=0.1$ the noise eigenvalues live in $[0.47,1.73]$; at $q=1$ they live in $[0,4]$. The *lower* edge collapses to zero as $q\to1$ — that is the singularity, foreshadowed spectrally.
- **Everything below $\lambda_+$ is indistinguishable from noise.** This gives the RMT denoising rule of page 04: keep eigenvalues above $\lambda_+$, replace the rest by their mean.

#### 2.3 Condition number blow-up

The condition number $\kappa(S)=\lambda_{\max}/\lambda_{\min}$ governs how much an inversion amplifies error. For pure noise at ratio $q$,

$$
\kappa(S)\;\approx\;\frac{(1+\sqrt q)^2}{(1-\sqrt q)^2}\ \xrightarrow[\ q\to1\ ]{}\ \infty .
$$

A single ill-conditioned direction makes the minimum-variance weights $w\propto S^{-1}\mathbf 1$ enormous along that eigenvector. The condition number is the *quantitative* measure of "how much will the optimizer be fooled" — and shrinking brings it down to a bounded, economically meaningful value (Ledoit & Wolf 2004, Thm 3.5: the shrinkage estimator's condition number is *bounded in probability*).

---

### 3. Computational Implementation — simulating the noise band

Pure-noise simulation: generate $T\times N$ i.i.d. Gaussian data, compute the sample covariance, and compare its extreme eigenvalues to the Marchenko–Pastur bounds $\lambda_\pm=(1\pm\sqrt q)^2$. Then show how the condition number explodes as $q\to1$ on a fixed history length.

```python
import numpy as np

rng = np.random.default_rng(1)

print("empirical eigenvalue edges vs Marchenko-Pastur theory (pure noise):")
for q in (0.1, 0.5, 1.0):
    T = 2000; N = int(T * q)
    X = rng.normal(size=(T, N))
    ev = np.linalg.eigvalsh(np.cov(X, rowvar=False, bias=True))
    lam_p, lam_m = (1 + np.sqrt(q))**2, (1 - np.sqrt(q))**2
    print(f"  q={q:4.2f}: lam_max={ev.max():.4f} (theory {lam_p:.4f})  "
          f"lam_min={ev.min():.4f} (theory {lam_m:.4f})  cond={ev.max()/max(ev.min(),1e-12):.2f}")

print("\ncondition number of the sample covariance, T=500 held fixed:")
for N in (50, 100, 250, 400, 490):
    X = rng.normal(size=(500, N))
    ev = np.linalg.eigvalsh(np.cov(X, rowvar=False, bias=True))
    print(f"  N={N:4d}  q={N/500:.3f}: cond = {ev.max()/ev.min():.2f}")
```
```
empirical eigenvalue edges vs Marchenko-Pastur theory (pure noise):
  q=0.10: lam_max=1.6970 (theory 1.7325)  lam_min=0.4811 (theory 0.4675)  cond=3.53
  q=0.50: lam_max=2.8809 (theory 2.9142)  lam_min=0.0875 (theory 0.0858)  cond=32.92
  q=1.00: lam_max=4.0024 (theory 4.0000)  lam_min=0.0000 (theory 0.0000)  cond=4002363567625.91

condition number of the sample covariance, T=500 held fixed:
  N=  50  q=0.100: cond = 3.64
  N= 100  q=0.200: cond = 6.36
  N= 250  q=0.500: cond = 32.28
  N= 400  q=0.800: cond = 305.86
  N= 490  q=0.980: cond = 20517.46
```

**What the numbers say.** (i) The empirical edges track the MP theory to ~1% — the noise band is real and predictable. (ii) *This is pure noise* (true $\Sigma=I$), yet at $q=0.5$ an analyst would see "eigenvalues ranging from $0.09$ to $2.88$" and could easily mistake the spread for a factor structure. (iii) At $q=1$ the smallest eigenvalue is numerically zero: the matrix is singular and its inverse undefined. (iv) Holding $T=500$ fixed and growing $N$, the condition number climbs from $3.6$ to $20{,}518$ — a $5{,}600\times$ degradation from adding assets, not from losing data.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading the noise band as signal.** At $q=0.5$, a pure-noise spectrum spans $[0.09,2.88]$. Interpreting its "top eigenvalue" as a market factor is a false positive; only eigenvalues above $\lambda_+$ carry information (page 04 formalizes the test).
2. **Ignoring the MLE vs unbiased divisor.** Using $1/(T-1)$ vs $1/T$ shifts the whole spectrum by a $T/(T-1)$ factor; harmless at large $T$, but a common source of "my eigenvalues don't match the formula" confusion. The MP result is stated for the ML version $S=\tfrac1T X^\top X$.
3. **Standard asymptotics mislead.** Classical statistics says shrinkage intensity $\to0$ as $T\to\infty$ (with $N$ fixed), implying "just get more data." In general asymptotics it does **not** vanish — because $N$ grows with $T$ in real portfolios. This is the single most important conceptual shift on this page.
4. **Condition number is not the whole story.** A matrix can be well-conditioned but still a poor estimate in Frobenius/portfolio terms; conversely $\kappa$ is the sharpest *single-number* diagnostic for inversion error. Use $\kappa$ and $q$ together, never alone.

---

### 5. Canonical Literature & Study References

- **Marchenko, V. A. & Pastur, L. A. (1967).** "Distribution of eigenvalues for some sets of random matrices." *Mat. Sb.* 72(4):507–536. *The original law.*
- **Silverstein, J. W. & Choi, S.-I. (1995).** "Analysis of the limiting spectral distribution of large-dimensional random matrices." *Journal of Multivariate Analysis* 54(2):295–309. *The rigorous support/edge determination used for RMT denoising.*
- **Ledoit, O. & Wolf, M. (2004).** "A well-conditioned estimator…" *J. Multivariate Anal.* 88(2):365–411. *General asymptotics, condition-number theory (Thm 3.5).*
- **Bai, Z. & Silverstein, J. W. (2010).** *Spectral Analysis of Large Dimensional Random Matrices* (2nd ed.), Springer. *Reference for the proofs.*
- **Potters, M. & Bouchaud, J.-P. (2020).** *A First Course in Random Matrix Theory*, Cambridge. *The readable modern textbook.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/01-from-zero-intuition|01 · From Zero]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/03-linear-shrinkage|03 · Linear Shrinkage]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/04-random-matrix-theory-denoising|04 · RMT Denoising]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Statistics]] (Wishart law)
