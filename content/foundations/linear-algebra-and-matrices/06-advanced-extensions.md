---
title: "06 — Advanced Extensions: Random Matrix Theory & Numerical Linear Algebra"
tags:
  - foundations
  - linear-algebra
  - random-matrix-theory
  - marchenko-pastur
  - condition-number
  - ill-conditioning
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05 · SVD, PCA & Regression]] and [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]].

---

### 1. Intuition & Practical Objective

This page is the *robustness layer*: it names the two ways real linear algebra fails and what to do about each. The first failure is **numerical** — an ill-conditioned matrix silently destroys accuracy no matter how careful the algebra is. The second failure is **statistical** — with more assets than observations ($N>T$), the sample covariance matrix is not just singular, it is *full of noise eigenvalues that look like signal*, and naive PCA will happily report factors that are pure sampling error. The unifying tool for the second failure is **random matrix theory (RMT)**: it tells you *exactly* how wide a spectrum pure noise produces, so you can separate signal eigenvalues from noise by a *principled threshold* (Marchenko–Pastur), not by eyeballing a scree plot.

The practical objective: (1) quantify ill-conditioning via the condition number and know when an inversion is untrustworthy; (2) compute the Marchenko–Pastur noise band and use it to threshold a covariance spectrum before PCA/factor extraction; and (3) understand the canonical remedies — nearest-PSD projection, shrinkage, and eigenvalue clipping.

---

### 2. Mathematical Ground Truth & Derivations

**Condition number & perturbation bound.** For solving $Ax=b$, the 2-norm condition number is $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$. A perturbation bound says

$$\frac{\|\delta x\|}{\|x\|}\;\le\;\kappa_2(A)\,\frac{\|\delta A\|}{\|A\|},$$

so relative error in the solution can be $\kappa_2$ times larger than relative error in the inputs. $\kappa_2=10^7$ means a "perfectly computed" answer can be wrong in the 7th significant digit from a *machine-precision* input perturbation. The Hilbert matrix $H_{ij}=1/(i+j+1)$ is the canonical ill-conditioned example: $\kappa_2(H_8)\approx1.3\times10^7$.

**Marchenko–Pastur (Bai 2010; Laloux–Cizeau–Bouchaud 1999).** Let $X$ be $T\times N$ with iid entries of variance $\sigma^2$, and let $\hat\Sigma=\frac1T X'X$ be the sample covariance. As $T,N\to\infty$ with ratio $c=N/T$ fixed, the empirical eigenvalue distribution of $\hat\Sigma$ converges to the **Marchenko–Pastur law**, supported on

$$\Big[\sigma^2\big(1-\sqrt{c}\big)^2,\ \ \sigma^2\big(1+\sqrt{c}\big)^2\Big],$$

with density $p(\lambda)=\frac{1}{2\pi c\lambda}\sqrt{\big((1+\sqrt c)^2-\lambda/\sigma^2\big)\big(\lambda/\sigma^2-(1-\sqrt c)^2\big)}$ and a point mass at $0$ if $c>1$ ($N>T$). **Consequences:** (a) even *pure* noise produces a spread of eigenvalues up to $\sigma^2(1+\sqrt c)^2$ — call anything above that *signal*; (b) when $N>T$, $c>1$ forces a fraction $1-1/c$ of eigenvalues to be exactly zero; (c) the top noise eigenvalue is bounded — so a *real* factor must clear the MP edge. This is the principled alternative to guessing the number of factors from a scree plot (Tsay §9.4.1; Connor–Korajczyk and Bai–Ng criteria).

**Nearest-PSD repair & shrinkage.** To restore PSD, project onto the cone by clipping negative eigenvalues (Higham 1988) or shrink toward a structured target (Ledoit–Wolf) — both are *eigenvalue* operations, which is why this folder's [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04]] spectrum is the object you repair.

---

### 3. Computational Implementation — condition numbers & the MP edge, stdlib only

This builds the Hilbert matrices, computes their condition numbers by a from-scratch SVD, and then (a) shows all eigenvalues of a noise-only sample covariance sit inside the Marchenko–Pastur band, and (b) shows a planted single-factor eigenvalue **clears** the band — the RMT signal test. Stdlib only.

```python
import math, random

def matmul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def matvec(A,x): return [sum(A[i][k]*x[k] for k in range(len(x))) for i in range(len(A))]
def trans(A):   return [list(r) for r in zip(*A)]

def jacobi_eigh(A, tol=1e-12):
    n=len(A); A=[r[:] for r in A]; Q=[[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(200):
        p,q=0,1; mx=abs(A[0][1])
        for i in range(n):
            for j in range(i+1,n):
                if abs(A[i][j])>mx: mx,p,q=abs(A[i][j]),i,j
        if mx<tol: break
        app,aqq,apq=A[p][p],A[q][q],A[p][q]
        th=0.5*math.atan2(2*apq,aqq-app) if aqq!=app else math.pi/4
        c,s=math.cos(th),math.sin(th)
        for k in range(n):
            akp,akq=A[k][p],A[k][q]; A[k][p]=c*akp-s*akq; A[p][k]=A[k][p]; A[k][q]=s*akp+c*akq; A[q][k]=A[k][q]
            qkp,qkq=Q[k][p],Q[k][q]; Q[k][p]=c*qkp-s*qkq; Q[k][q]=s*qkp+c*qkq
        A[p][p]=c*c*app-2*s*c*apq+s*s*aqq; A[q][q]=s*s*app+2*s*c*apq+c*c*aqq; A[p][q]=A[q][p]=0.0
    l=[A[i][i] for i in range(n)]; idx=sorted(range(n),key=lambda i:-l[i])
    return [[Q[i][k] for k in idx] for i in range(n)], [l[i] for i in idx]

def svd(X):
    T,N=len(X),len(X[0]); Xt=trans(X); V,l=jacobi_eigh(matmul(Xt,X))
    S=[math.sqrt(max(v,0.0)) for v in l]; U=[[0.0]*N for _ in range(T)]
    for j in range(N):
        if S[j]<1e-12: continue
        xv=matvec(X,[V[k][j] for k in range(N)])
        for i in range(T): U[i][j]=xv[i]/S[j]
    return U,S,V

def solve(A,b):
    A=[r[:] for r in A]; b=b[:]; n=len(A)
    for col in range(n):
        piv=max(range(col,n),key=lambda r:abs(A[r][col]))
        if piv!=col: A[col],A[piv]=A[piv],A[col]; b[col],b[piv]=b[piv],b[col]
        for r in range(col+1,n):
            f=A[r][col]/A[col][col]; A[r][col]=0.0
            for c in range(col+1,n): A[r][c]-=f*A[col][c]
            b[r]-=f*b[col]
    x=[0.0]*n
    for i in range(n-1,-1,-1): x[i]=(b[i]-sum(A[i][c]*x[c] for c in range(i+1,n)))/A[i][i]
    return x

# ---- (a) ill-conditioning: Hilbert matrices ----
print("Hilbert matrix  kappa_2(H_n)  vs  max|computed - true|  (true solution = all 1s)")
for n in (3, 5, 8):
    H=[[1.0/(i+j+1) for j in range(n)] for i in range(n)]
    U,S,V=svd(H); kappa=S[0]/S[-1]
    b=[sum(H[i][j] for j in range(n)) for i in range(n)]      # H*1 = b
    x=solve(H,b); err=max(abs(x[i]-1.0) for i in range(n))
    print(f"  n={n}: kappa={kappa:.3e}   max|x-1| = {err:.3e}")

# ---- (b) Marchenko-Pastur: noise-only vs planted-factor spectra ----
random.seed(0); T,N=400,200; c=N/T
M=[[random.gauss(0,1) for _ in range(N)] for _ in range(T)]
Mt=trans(M); S2=[[sum(Mt[i][k]*M[k][j] for k in range(T)) for j in range(N)] for i in range(N)]
S2=[[S2[i][j]/T for j in range(N)] for i in range(N)]
_,e=jacobi_eigh(S2)
lmin=(1-math.sqrt(c))**2; lmax=(1+math.sqrt(c))**2
inside=sum(1 for x in e if lmin-1e-6<=x<=lmax+1e-6)
print(f"\nMarchenko-Pastur (N={N},T={T},c={c:.2f}): support [{lmin:.4f},{lmax:.4f}]")
print(f"  noise-only: max eig={e[0]:.4f}, min={e[-1]:.4f}, {inside}/{N} eigenvalues inside band")

random.seed(7)
f=[random.gauss(0,1) for _ in range(T)]; beta=[random.gauss(0,1)*0.8 for _ in range(N)]
R=[[f[i]*beta[j]+random.gauss(0,1)*0.5 for j in range(N)] for i in range(T)]
Rt=trans(R); S3=matmul(Rt,R); S3=[[S3[i][j]/T for j in range(N)] for i in range(N)]
_,e3=jacobi_eigh(S3)
print(f"  WITH 1 planted factor: max eig={e3[0]:.4f}  -> clears the MP edge {lmax:.4f} (signal);")
print(f"  eig1/total variance = {e3[0]/sum(e3):.3f}")
```
```
Hilbert matrix  kappa_2(H_n)  vs  max|computed - true|  (true solution = all 1s)
  n=3: kappa=5.241e+02   max|x-1| = 9.992e-15
  n=5: kappa=4.766e+05   max|x-1| = 6.168e-13
  n=8: kappa=1.304e+07   max|x-1| = 4.188e-07

Marchenko-Pastur (N=200,T=400,c=0.50): support [0.0858,2.9142]
  noise-only: max eig=2.2882, min=0.6470, 200/200 eigenvalues inside band
  WITH 1 planted factor: max eig=126.9064  -> clears the MP edge 2.9142 (signal);
  eig1/total variance = 0.719
```
Two clean verdicts. **Ill-conditioning is real and silent:** $H_8$ has $\kappa\approx1.3\times10^7$, and even with an *exact* right-hand side the solved vector is off by $\sim10^{-7}$ purely from arithmetic rounding — a direct, measured violation of the perturbation bound's prediction. **RMT works as a signal detector:** a pure-noise $200\times400$ covariance keeps all 200 eigenvalues inside the Marchenko–Pastur band, while a single planted factor pushes one eigenvalue to $127$ — orders of magnitude above the edge $\approx2.9$. Anything inside the band is indistinguishable from noise; anything above it is signal.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The $N>T$ singularity trap.** Sample covariance rank $\le T$; with $N=500$ assets and $T=250$ days at least 250 eigenvalues are exactly zero. Naive PCA/optimizers then load heavily on zero-variance "risk" that is pure in-sample noise. Remedy: MP thresholding, shrinkage (Ledoit–Wolf), or factor-structured estimation.
2. **Ill-conditioning is invisible without the condition number.** A huge $\kappa_2$ makes "solved" systems wrong at machine precision with no error message. Always report $\kappa_2$ (or solve via SVD/QR) before trusting an inversion of a near-collinear $X'X$.
3. **Pairwise-assembled correlations are non-PSD by construction.** Column-by-column correlation building violates transitivity and produces negative eigenvalues, breaking Cholesky and optimizers. Repair via nearest-PSD projection (Higham) or shrink the whole matrix.
4. **The MP edge is asymptotic.** In finite samples the bulk blurs and a *weak* factor can sit just above the edge while noise spikes poke through it. Use the edge as a first cut, then confirm with factor-number criteria (eigenvalue gap, Bai–Ng, Connor–Korajczyk).

---

### 5. Canonical Literature & Study References

- **Bai & Silverstein**: *Spectral Analysis of Large Dimensional Random Matrices* (2010) — the rigorous RMT source for the Marchenko–Pastur law. *Corpus PDF available.*
- **Laloux, Cizeau, Bouchaud & Potters**: "Noise Dressing of Financial Correlation Matrices" (1999) — the finance-native statement: most empirical eigenvalue "structure" in correlation matrices is MP noise.
- **Hastie, Tibshirani, Friedman**, *The Elements of Statistical Learning*, Ch 18 (high-dimensional $p\gg N$ problems; supervised PCA; false-discovery discipline). *Verified in the corpus.*
- **Tsay**, *Analysis of Financial Time Series*, §9.6.1 (factor-number selection: Connor–Korajczyk, Bai–Ng criteria). *Verified.*
- **Horn & Johnson**, *Matrix Analysis*, Ch 5–6 (condition numbers, matrix norms).

---

### 6. Connected Graph Bridges

- Back: [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05 · SVD, PCA & Regression]] · [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] (RMT denoising, Ledoit–Wolf) · [[foundations/numerical-methods/index|Numerical Methods]] (05 · Numerical Linear Algebra, iterative solvers) · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var|Parametric & Monte Carlo VaR]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
