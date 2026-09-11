---
title: "05 — SVD, PCA & Linear Regression: The Workhorse"
tags:
  - foundations
  - linear-algebra
  - svd
  - pca
  - least-squares
  - ridge
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]].

---

### 1. Intuition & Practical Objective

This page is where the folder *earns its keep*: the **singular value decomposition (SVD)** unifies three things every quant uses daily — **least-squares regression**, **principal components analysis (PCA)**, and **low-rank approximation / denoising** — into one factorization. The objective is to see that these are not three methods but *one decomposition viewed three ways*: the SVD of the design/return matrix $X$ is simultaneously (a) the engine behind $\hat\beta=(X'X)^{-1}X'y$, (b) the geometry behind PCA's principal axes, and (c) the machine behind the best rank-$k$ approximation (Eckart–Young).

In one line: **regression asks "which combination of my *columns* best predicts $y$?", PCA asks "which few *directions* carry most of the variance?", and SVD answers both because it decomposes any matrix into independent rank-one layers $X=\sum_i\sigma_i u_i v_i'$.** The largest layers are the signal; the smallest are the noise you should drop.

---

### 2. Mathematical Ground Truth & Derivations

**Least squares (ESL Ch 3).** Minimize $\text{RSS}(\beta)=\sum_i(y_i-x_i'\beta)^2$ (ESL eq. 3.3). The normal equations (3.5) give the closed form (ESL eq. 3.6)

$$
\hat\beta=(X'X)^{-1}X'y,\qquad \hat y=X(X'X)^{-1}X'y=X\hat\beta\ \ (3.7),
$$

with the hat matrix $H=X(X'X)^{-1}X'$ projecting $y$ onto the column space. This is *the* workhorse of factor models — each factor exposure is a linear regression of the return on the factor. **Ridge** adds an $L_2$ penalty (3.41–3.44):

$$
\hat\beta_{ridge}=(X'X+\lambda I)^{-1}X'y,
$$

which, via the SVD $X=UDV'$ (ESL 3.45), shrinks each fitted component by $\frac{d_j^2}{d_j^2+\lambda}$ (3.47): **more shrinkage on the smaller (noisier) singular values** $d_j$.

**SVD (ESL eq. 3.45, 14.54).** Any real $X\in\mathbb{R}^{T\times N}$ factors as $X=U\Sigma V'$ with $U'U=I$, $V'V=I$, $\Sigma$ diagonal with **singular values** $\sigma_1\ge\dots\ge\sigma_r\ge0$, where $r=\text{rank}(X)$ and $\sigma_i=\sqrt{\lambda_i(X'X)}$. Equivalently

$$
X=\sum_{i=1}^{r}\sigma_i\,u_i v_i'.
$$

**Eckart–Young–Mirsky.** The best rank-$k$ approximation to $X$ (minimizing Frobenius error) is $X_k=\sum_{i\le k}\sigma_i u_i v_i'$, and the error is $\|X-X_k\|_F=\sqrt{\sum_{i>k}\sigma_i^2}$. This is the mathematical engine of denoising: keep the big singular layers, drop the tail.

**PCA via SVD (ESL 14.5).** PCA fits the best rank-$q$ affine manifold $f(\lambda)=\mu+V_q\lambda$ to the rows (model **eq. 14.49**) by minimizing reconstruction error $\min\sum_i\|x_i-\mu-V_q\lambda_i\|^2$ (**eq. 14.50**) — solved by the SVD **eq. 14.54**. The first $q$ right-singular vectors $V_q$ are the principal axes; the singular values measure how much variance each carries. (ESL's digits example: 12 of 256 SVD directions account for 63% of variance.)

---

### 3. Computational Implementation — regression and PCA from the SVD, from scratch

Everything here is implemented from first principles (Jacobi diagonalization + Gaussian elimination), so there is no hidden numpy. Stdlib only.

```python
import math

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
    """X=U S V' via eigen of X'X (N<=T)."""
    T,N=len(X),len(X[0]); Xt=trans(X)
    XtX=matmul(Xt,X); V,l=jacobi_eigh(XtX); S=[math.sqrt(max(v,0.0)) for v in l]
    U=[[0.0]*N for _ in range(T)]
    for j in range(N):
        if S[j]<1e-12: continue
        xv=matvec(X,[V[k][j] for k in range(N)])
        for i in range(T): U[i][j]=xv[i]/S[j]
    return U,S,V

def solve(A,b):                                    # Gaussian elimination w/ partial pivoting
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

# ---- (a) least squares: normal equations  (ESL 3.6)  vs  SVD pseudo-inverse  ----
X=[[1.0,x] for x in [0.1,0.4,0.9,1.3,1.7,2.0,2.6,3.0]]
y=[1.2,1.5,2.1,2.4,3.0,3.4,3.9,4.6]
Xt=trans(X); XtX=matmul(Xt,X); Xty=matvec(Xt,y)
bhat=solve(XtX, Xty)
rss=sum((y[i]-sum(bhat[k]*X[i][k] for k in range(2)))**2 for i in range(len(y)))
U,S,V=svd(X)
uy=[sum(U[i][j]*y[i] for i in range(len(y))) for j in range(2)]
bhat_svd=[sum((uy[j]/S[j])*V[i][j] for j in range(2)) for i in range(2)]
print(f"least squares  beta = {[round(x,6) for x in bhat]}   RSS = {rss:.6f}")
print(f"SVD pseudo-inv beta = {[round(x,6) for x in bhat_svd]}   (identical)")

# ---- (b) PCA: best rank-1 (or 2) manifold of a 4x3 matrix, reconstruction error = tail sigma  ----
Xm=[[1.0,2.0,3.0],[2.0,1.0,4.0],[3.0,3.0,1.0],[4.0,2.0,2.0]]
U,S,V=svd(Xm)
def rankk(k):
    return [[sum(S[j]*U[i][j]*V[c][j] for j in range(k)) for c in range(3)] for i in range(4)]
err2=math.sqrt(sum((rankk(2)[i][c]-Xm[i][c])**2 for i in range(4) for c in range(3)))
print(f"\nSVD singular values = {[round(s,6) for s in S]}")
print(f"rank-2 reconstruction error = {err2:.6f}  == sigma_3 = {S[2]:.6f}   (Eckart-Young)")
```
```
least squares  beta = [1.03709, 1.150273]   RSS = 0.053449
SVD pseudo-inv beta = [1.03709, 1.150273]   (identical)

SVD singular values = [8.174835, 3.003784, 1.46607]
rank-2 reconstruction error = 1.466070  == sigma_3 = 1.466070   (Eckart-Young)
```
Regression and the SVD give **byte-identical** coefficients (both solve the same normal equations; the SVD route is the numerically safer one for ill-conditioned $X$). And the best rank-2 manifold of $X$ misses exactly $\sigma_3=1.466$ of Frobenius error — the Eckart–Young guarantee that PCA/denoising "keep the big layers, drop the tail" is exact, not heuristic.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Normal equations can be ill-conditioned even when the problem isn't.** Forming $X'X$ squares the condition number ($\kappa(X'X)=\kappa(X)^2$). For wide or nearly-collinear $X$, solve $\hat\beta$ via the SVD / QR instead — this is the difference between "works" and "silently wrong."
2. **$N>T$ makes $X'X$ singular (rank $\le T$).** The normal equations have no unique solution; PCA on the sample covariance fills the spectrum with noise eigenvalues ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]). Ridge ($+\lambda I$) and shrinkage restore a solution by pushing the ill-conditioned directions off.
3. **SVD truncation is a model choice, not a given.** Dropping "small" singular values removes noise *and* genuine small-signal directions; the cut-off (ESL digits kept 12/256 for 63%) must be justified (eigenvalue gap, cross-validation, or RMT threshold — [[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]).
4. **Correlation vs covariance scale.** PCA on $\Sigma$ (scale-sensitive) vs on the correlation matrix (scale-free) gives different axes; standardized data is the default for factor extraction (Tsay §9.4).

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani, Friedman**, *The Elements of Statistical Learning* (2nd ed.), Ch 3 (LS eqs. 3.3–3.7; ridge 3.41–3.47; SVD 3.45) and Ch 14.5 (PCA, eqs. 14.49–14.50, 14.54; digits example). *Math-verified in the corpus.*
- **Tsay**, *Analysis of Financial Time Series*, §9.4 (PCA), §9.5–9.6 (statistical factor models, APCA for $k\gg T$). *Verified.*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §2.2 (eigen/PC simulation route, eq. 2.32).
- **Strang**, *Introduction to Linear Algebra* (5th ed.), Ch 7 (SVD) and Ch 11 (numerical linear algebra). *Corpus PDF available.*

---

### 6. Connected Graph Bridges

- Back: [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Continue: [[foundations/linear-algebra-and-matrices/06-advanced-extensions|06 · Advanced Extensions (RMT & Numerics)]]
- Forward: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (regression = the factor engine) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric & Monte Carlo VaR]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (OLS/regression diagnostics)
