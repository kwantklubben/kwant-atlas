---
title: "04 — Random-Matrix-Theory Denoising: Cleaning the Eigenvalue Spectrum"
tags:
  - pillar-portfolio-optimization
  - covariance-shrinkage
  - random-matrix-theory
  - marchenko-pastur
  - eigenvalue-clipping
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/02-the-sample-covariance-problem|02 · The Sample-Covariance Problem]] (the Marchenko–Pastur law and its edges).

---

### 1. Intuition & Practical Objective

Linear shrinkage (page 03) throws a *single* scalar at the whole matrix. RMT denoising is **surgical**: it uses the Marchenko–Pastur law to decide, eigenvalue by eigenvalue, which directions are signal and which are noise, then rebuilds the matrix with the noise directions collapsed. The practical objective: given a correlation matrix with $N\approx T$, produce a cleaned matrix that (a) keeps the genuine systematic factors, (b) removes the spurious eigenvalue spread that the optimizer would otherwise exploit, and (c) is well-conditioned by construction.

The idea is due to Laloux, Cizeau, Bouchaud & Potters (1999): **"noise dressing."** If the true correlation were the identity, the sample would still show an eigenvalue band $[\lambda_-,\lambda_+]$ (page 02). Therefore the *signal* is exactly the set of eigenvalues pushed **above $\lambda_+$** — the market mode and the strongest sectors — and everything inside the band should be replaced by the flat, structureless value that pure noise would produce.

> **One-line essence.** "Eigenvalues above the Marchenko–Pastur edge $\lambda_+=(1+\sqrt{N/T})^2$ carry information; replace all eigenvalues inside the noise band by their common average and rebuild."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The noise edge as a signal/noise threshold

For a $N\times N$ correlation matrix estimated from $T$ observations ($q=N/T$), the MP edge is

$$
\lambda_+=\Bigl(1+\sqrt{q}\Bigr)^2 .
$$

The RMT hypothesis test is:

$$
H_0:\ \lambda_i\le\lambda_+\ \Rightarrow\ \text{eigen-direction }i\text{ is consistent with pure noise};\qquad \lambda_i>\lambda_+\ \Rightarrow\ \text{genuine cross-sectional structure}.
$$

The number of signal eigenvalues is $K=\#\{i:\lambda_i>\lambda_+\}$. In equity data $K$ is small and interpretable — typically 1 (market mode) plus a handful of sectors; Plerou et al. (2002) confirm this bulk-plus-spikes structure on real returns.

#### 2.2 The constant-residual ("clipping") estimator

Given the spectral decomposition $C=\sum_{i=1}^N\lambda_i q_iq_i^\top$ of the sample correlation matrix $C$, and $K$ signal eigenvalues,

$$
\boxed{\ \lambda_i^{\text{den}}= \begin{cases} \lambda_i, & i\le K\\[4pt] \bar\lambda_{\text{noise}}, & i>K\end{cases}\ }\qquad \bar\lambda_{\text{noise}}=\frac{1}{N-K}\sum_{i=K+1}^{N}\lambda_i ,
$$

then $\displaystyle C^{\text{den}}=\sum_i\lambda_i^{\text{den}}q_iq_i^\top$, followed by a **diagonal rescaling** $c_{ij}^{\text{den}}\leftarrow c_{ij}^{\text{den}}/\sqrt{c_{ii}^{\text{den}}c_{jj}^{\text{den}}}$ so the diagonal returns to exactly $1$.

Why the average and not just delete? Because deleting the entire noise bulk would make $C^{\text{den}}$ singular of rank $K$; replacing the bulk by its mean keeps full rank, keeps the trace, and removes the *dispersion* — the spurious spread the optimizer would otherwise chase. In terms of the spectrum, $\bar\lambda_{\text{noise}}\approx1$ (the bulk average of a correlation matrix is $(N-\sum\lambda_i^{\text{signal}})/(N-K)\approx1$). This is the **Laloux et al. (1999) "constant residual" method**, the simplest and most used RMT cleaner. A refinement (Guhr & Kälbermann; Marchenko–Pastur "rotation" methods) replaces the bulk by an MP-distributed profile rather than a flat line.

#### 2.3 Why this is a shrinkage of eigenvalues

Eigenvalue clipping and linear shrinkage are two ends of *the same* idea — a nonlinear map on the sample eigenvalues $\lambda_i\mapsto\lambda_i^{\text{den}}$:

- **Linear shrinkage** (page 03): $\lambda_i\mapsto\delta\mu+(1-\delta)\lambda_i$ — an *affine* pull of every eigenvalue toward the grand mean. Same map for all $i$.
- **RMT clipping**: $\lambda_i\mapsto\lambda_i$ for large $i$ (leave signal alone) and $\mapsto\bar\lambda\approx1$ for small $i$ (flatten noise). **Different** map depending on where the eigenvalue sits.

This is exactly the gateway to full **nonlinear shrinkage** (page 06), where the optimal per-eigenvalue map is derived rather than hard-thresholded.

---

### 3. Computational Implementation — denoising a simulated factor model

Simulate a 3-factor correlation matrix (three "sectors"), draw $N=200$ assets from $T=500$ observations, estimate the sample correlation, apply MP clipping, and measure what it buys: Frobenius distance to the true correlation, the true (out-of-sample) variance of the minimum-variance portfolio, and the condition number.

```python
import numpy as np

def minvar(C):
    one = np.ones(C.shape[0]); w = np.linalg.solve(C, one); return w / w.sum()

rng = np.random.default_rng(11)
N, T, K = 200, 500, 3
B  = rng.normal(0, 1, size=(N, K)) * 0.4                 # 3 real factors
Ce = B @ B.T + np.diag(np.full(N, 1.0))                  # true covariance
De = np.sqrt(np.diag(Ce)); Re = Ce / np.outer(De, De)    # true correlation
X  = rng.normal(size=(T, N)) @ np.linalg.cholesky(Ce).T  # T returns
Rs = np.corrcoef(X, rowvar=False)                        # sample correlation

q = N / T; lam_p = (1 + np.sqrt(q))**2                   # Marchenko-Pastur edge
ev, V = np.linalg.eigh(Rs)
idx = np.argsort(ev)[::-1]; ev, V = ev[idx], V[:, idx]
k = int((ev > lam_p).sum())                              # signal count
ev_den = ev.copy(); ev_den[k:] = ev[k:].mean()           # constant-residual clipping
Rd = V @ np.diag(ev_den) @ V.T
d  = np.sqrt(np.diag(Rd)); Rd = Rd / np.outer(d, d)      # rescale diagonal to 1

Cs = np.cov(X, rowvar=False)
Cd = Rd * np.outer(np.sqrt(np.diag(Cs)), np.sqrt(np.diag(Cs)))
print(f"q={q:.2f}  lambda_+ = {lam_p:.4f}  signal eigenvalues={k}  top-6={np.round(ev[:6],4)}")
print(f"||R_sample - R_true||_F = {np.linalg.norm(Rs - Re):.4f}")
print(f"||R_denoised-R_true||_F = {np.linalg.norm(Rd - Re):.4f}")
w_s, w_d, w_e = minvar(Cs), minvar(Cd), np.ones(N)/N
print(f"TRUE variance: w_sample={w_s@Ce@w_s:.6f}  w_denoised={w_d@Ce@w_d:.6f}  w_1/N={w_e@Ce@w_e:.6f}")
print(f"cond: C_sample={np.linalg.cond(Cs):.2f}  C_denoised={np.linalg.cond(Cd):.2f}  C_true={np.linalg.cond(Ce):.2f}")
```
```
q=0.40  lambda_+ = 2.6649  signal eigenvalues=3  top-6=[22.9279 22.0705 15.3671  1.9985  1.9113  1.8765]
||R_sample - R_true||_F = 8.7404
||R_denoised-R_true||_F = 6.5351
TRUE variance: w_sample=0.008875  w_denoised=0.005120  w_1/N=0.006337
cond: C_sample=277.20  C_denoised=43.63  C_true=35.57
```

**Read the result.** The MP test recovers exactly $K=3$ signal eigenvalues ($22.93, 22.07, 15.37$) — the three planted factors — and correctly relegates the next eigenvalues ($1.998, 1.911, 1.877,\dots$) to the noise band; note how close those bulk eigenvalues sit to $1$ and how far below $\lambda_+=2.66$. Denoising cuts the Frobenius distance to the true correlation by **25%** ($8.74\to6.54$), cuts the true portfolio variance by **42%** ($0.008875\to0.005120$) — now beating $1/N$ ($0.006337$) — and pulls the condition number down from $277$ to $44$, close to the true matrix's $36$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The known-$\lambda_+$ assumption.** $\lambda_+$ needs $\sigma^2$ and $q$; for *correlation* matrices $\sigma^2=1$ and $q=N/T$ are known, but if returns are heavy-tailed the empirical edge wanders above the Gaussian prediction, causing **over-clipping** (you delete real signal). Always plot the spectrum against $\lambda_+$ before trusting $K$.
2. **Over-clipping destroys genuine weak factors.** A true but weak sector with $1<\lambda< \lambda_+$ is statistically indistinguishable from noise and *will* be flattened. Denoising is conservative by design — it errs toward declaring things noise.
3. **Non-i.i.d. returns violate the MP derivation.** Autocorrelation, volatility clustering and non-stationarity inflate effective $q$; the MP band is narrower than reality, so fixed-edge clipping over-cleans. **Standardize/whiten or use a window that is actually stationary.**
4. **Denoising helps the *portfolio*, not always the *Frobenius norm*.** In our experiment both improved, but they can move in opposite directions: a cleaner matrix in $\|\cdot\|_F$ is not automatically a better min-variance input, because min-variance weights the *inverse*. Always evaluate the estimator with the *downstream* metric (out-of-sample portfolio variance), never Frobenius alone.
5. **Denoising is not free of estimation error either.** You now estimate $\lambda_+$ and $K$; with $N$ small this uncertainty can dominate, and simple shrinkage can match RMT. Prefer RMT cleaning when $N$ is large ($\gtrsim100$) and the factor structure is strong.

---

### 5. Canonical Literature & Study References

- **Laloux, L., Cizeau, P., Bouchaud, J.-P. & Potters, M. (1999).** "Noise dressing of financial correlation matrices." *Physical Review Letters* 83(7):1467–1470. ★ *The constant-residual method implemented here.*
- **Plerou, V., Gopikrishnan, P., Rosenow, B., Amaral, L., Guhr, T. & Stanley, H. (2002).** "Random matrix approach to cross correlations in financial data." *Physical Review E* 65:066126. *Empirical bulk-plus-spikes structure of equity correlation matrices.*
- **Bouchaud, J.-P. & Potters, M. (2003).** *Theory of Financial Risk and Derivative Pricing* (2nd ed.), Cambridge. *The physics view of correlation denoising.*
- **Guhr, T. & Kälbermann, G. (2003).** "Local eigenvalue density for generalized random matrix ensembles…" *J. Phys. A* 36:1349. *Refined (non-flat-residual) cleaning.*
- **Potters, M. & Bouchaud, J.-P. (2020).** *A First Course in Random Matrix Theory*, Cambridge. *Modern readable RMT reference.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/02-the-sample-covariance-problem|02 · The Sample-Covariance Problem]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/03-linear-shrinkage|03 · Linear Shrinkage]]
- Forward: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/06-advanced-extensions|06 · Nonlinear Shrinkage & Factor Covariance]]
- Hub: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Index Hub]]
- Related: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]] (uses correlation structure/denoising differently — clustering instead of eigen-clipping)
