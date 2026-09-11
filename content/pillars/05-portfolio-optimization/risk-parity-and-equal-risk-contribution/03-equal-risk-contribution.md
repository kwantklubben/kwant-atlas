---
title: "03 — Equal Risk Contribution (ERC): the Convex Problem & Its Closed Forms"
tags:
  - pillar-portfolio-optimization
  - risk-parity-and-equal-risk-contribution
  - erc
  - convex-optimization
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/02-risk-contributions|02 · Risk Contributions]] and [[foundations/calculus-and-optimization/index|Calculus & KKT Convex Optimization]].

---

### 1. Intuition & Practical Objective

Now we put a *target* on the decomposition of page 02: find the weights $w$ such that **every asset contributes the same amount of risk.**

$$
RC_1(w)=RC_2(w)=\cdots=RC_N(w)=\frac{\sigma(w)}{N}.
$$

This is the **Equal Risk Contribution (ERC)** portfolio. It is the disciplined, covariance-aware form of risk parity — and, under a constant-correlation $\Sigma$, it *is* the naive inverse-vol risk parity. The practical objective of this page is threefold: (1) state the ERC condition and *why it is well-posed* (existence & uniqueness), (2) give the closed forms that exist in special cases, and (3) present the **convex optimization / cyclical-coordinate-descent** solver that handles every other case.

Why ERC *and not* the minimum-variance (MV) or $1/N$ portfolios? Recall the "menu" (Maillard §3.4):

$$
x_i=x_j \ \ (1/N),\qquad \partial_{x_i}\sigma=\partial_{x_j}\sigma \ \ (\text{MV}),\qquad x_i\,\partial_{x_i}\sigma=x_j\,\partial_{x_j}\sigma\ \ (\text{ERC}).
$$

MV equalizes *marginal* contributions — it is the least-volatile point on the frontier but concentrates both weights and risk in a handful of assets. $1/N$ equalizes *weights* — diversified in capital but wildly unbalanced in risk (47% of risk in one of four assets on page 02). **ERC is the middle ground:** diversified in risk (which is what matters), not maximally cheap, and never zeroing any position because $w_i\to0$ would send its risk contribution to zero. The volatility ordering is strict:

$$
\sigma_{mv}\;\le\;\sigma_{erc}\;\le\;\sigma_{1/N}.
$$

(Maillard App. A.3 proves this by embedding all three in one family $\min\sqrt{w^\top\Sigma w}\ \text{s.t.}\ \sum_i\ln w_i\ge c$ with $c=-\infty$ → MV, $c$ = ERC level, $c=-N\ln N$ → $1/N$.)

> **The one-sentence essence.** "ERC is the portfolio that divides the risk pie, not the capital pie, into $N$ exactly equal slices — the unique, correlation-aware sweet spot between $1/N$ and minimum variance."

---

### 2. Mathematical Ground Truth & Derivations

**The condition.** From page 02, $RC_i=w_i(\Sigma w)_i/\sigma(w)$. ERC demands equal slices:

$$
w_i\,(\Sigma w)_i = w_j\,(\Sigma w)_j\quad \forall i,j \qquad\Longleftrightarrow\qquad w_i(\Sigma w)_i=\text{const}.
$$

Multiplying by the budget $\sum_i w_i=1$ normalizes. **Well-posedness:** Maillard et al. (2010) show the ERC portfolio exists and is *unique* as long as $\Sigma$ is positive-definite and the weights are long-only, by embedding it in a strictly convex program (below).

**Closed form — two assets.** Let $w_1=w$, $w_2=1-w$. The ERC condition $w_1^2\sigma_1^2=(1-w)^2\sigma_2^2$ gives the unique solution in $[0,1]$:

$$
\boxed{\;w_1=\frac{\sigma_1^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}}=\frac{\sigma_2}{\sigma_1+\sigma_2},\qquad w_2=\frac{\sigma_2^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}}=\frac{\sigma_1}{\sigma_1+\sigma_2}\;}
$$
*— and it does not depend on the correlation $\rho$ at all.*

**Closed form — constant correlation ($\rho_{ij}=\rho$).** With $\Sigma_{ij}=\rho\sigma_i\sigma_j$ ($i\ne j$) the ERC condition reduces to $w_i\sigma_i=w_j\sigma_j$, giving

$$
\boxed{\;w_i=\frac{\sigma_i^{-1}}{\sum_{j=1}^N \sigma_j^{-1}}\;}
$$

i.e. **constant correlation ⇒ ERC = inverse-volatility (naive) risk parity.** This is the cleanest statement of when the simple rule is exactly right.

**Closed form — beta reading (any $\Sigma$).** Define $\beta_i=(\Sigma w)_i/\sigma(w)^2$ (the portfolio beta of asset $i$). Then $RC_i=w_i\beta_i\sigma(w)$, and ERC implies

$$
w_i\propto \beta_i^{-1},
$$

i.e. weight is **inversely proportional to portfolio beta** — high-beta, highly-correlated assets get a *small* capital weight. This is endogenous ($\beta_i$ depends on $w$), so it is interpretive, not a closed form.

**Convex formulation (the general solver).** Because $\sigma$ is homogeneous of degree 1, ERC = risk budgeting with equal budgets $b_i=1/N$. The standard convex embedding: minimize a quadratic subject to a log-barrier:

$$
\min_{w>0}\ \tfrac12\,w^\top\Sigma w \quad\text{s.t.}\quad \textstyle\sum_{i=1}^N b_i\ln w_i \ge c,
$$

whose KKT stationarity $(\Sigma w)_i=\lambda\,b_i/w_i$ forces $w_i(\Sigma w)_i\propto b_i$ — i.e. $RC_i\propto b_i$. Setting $b_i=1/N$ recovers ERC. Equivalently one may minimize $f(w)=\tfrac12 w^\top\Sigma w-\textstyle\sum_i b_i\ln w_i$ for *any* fixed barrier weight, then renormalize — the road the computational implementation takes.

---

### 3. Computational Implementation — ERC by cyclical coordinate descent, verified

The general case (non-constant $\Sigma$) has **no closed form**, so we solve it numerically. Below is a **cyclical coordinate descent (CCD)** on the convex barrier $f(w)=\tfrac12 w^\top\Sigma w-\sum_i b_i\ln w_i$: for each coordinate $i$ in turn, with the others held fixed, stationarity $\partial f/\partial w_i=0$ becomes a simple *quadratic* in $w_i$,

$$
S_{ii}w_i^2+\Big(\textstyle\sum_{j\ne i}S_{ij}w_j\Big)w_i-b_i=0,
$$

whose positive root is taken in closed form, then the vector is renormalized to $\sum w=1$. On Maillard's universe it reproduces the paper's ERC weights exactly — and we *verify* the equal contributions and the exact Euler sum.

```python
import math
def matvec(A, v): return [sum(A[i][k]*v[k] for k in range(len(v))) for i in range(len(A))]
def dot(a, b):     return sum(x*y for x, y in zip(a, b))

def erc_ccd(S, b, sweeps=3000):
    n = len(S); w = [1.0/n]*n
    for _ in range(sweeps):
        for i in range(n):
            c_i = sum(S[i][j]*w[j] for j in range(n) if j != i)
            w[i] = (-c_i + math.sqrt(c_i*c_i + 4.0*b[i]*S[i][i])) / (2.0*S[i][i])
    s = sum(w); return [x/s for x in w]

vols = [0.10, 0.20, 0.30, 0.40]
C = [[1.00, 0.80, 0.00, 0.00],
     [0.80, 1.00, 0.00, 0.00],
     [0.00, 0.00, 1.00, -0.50],
     [0.00, 0.00, -0.50, 1.00]]
S = [[C[i][j]*vols[i]*vols[j] for j in range(4)] for i in range(4)]

werc = erc_ccd(S, [0.25, 0.25, 0.25, 0.25])
Sw = matvec(S, werc); sig = math.sqrt(dot(werc, Sw))
RC = [werc[i]*Sw[i]/sig for i in range(4)]
print("ERC weights =", ['%.3f'%x for x in werc], " (paper: 0.384 0.192 0.243 0.182)")
print("sigma       =", '%.4f'%sig, " (paper: 10.3%)")
print("RC_i each   =", ['%.4f'%x for x in RC])
print("pct RC      =", ['%.1f%%'%(x/sig*100) for x in RC])
print(f"sum RC = {sum(RC):.4f} == sigma (Euler holds): {abs(sum(RC)-sig)<1e-9}")

# naive inverse-vol for comparison
iv = [1.0/vols[i]/sum(1.0/v for v in vols) for i in range(4)]
Si = matvec(S, iv); si = math.sqrt(dot(iv,Si)); RCi = [iv[i]*Si[i]/si for i in range(4)]
print("inverse-vol w =", ['%.3f'%x for x in iv], " RC shares =", ['%.1f%%'%(x/si*100) for x in RCi])
```
```
ERC weights = ['0.384', '0.192', '0.243', '0.182']  (paper: 0.384 0.192 0.243 0.182)
sigma       = 0.1029  (paper: 10.3%)
RC_i each   = ['0.0257', '0.0257', '0.0257', '0.0257']
pct RC      = ['25.0%', '25.0%', '25.0%', '25.0%']
sum RC = 0.1029 == sigma (Euler holds): True
inverse-vol w = ['0.480', '0.240', '0.160', '0.120']  RC shares = ['39.1%', '39.1%', '10.9%', '10.9%']
```

The bottom two rows are the entire argument for "ERC over naive risk parity": the inverse-vol portfolio (the marketing-default of many risk-parity funds) puts **39.1% of risk in each of assets 1 and 2 and only 10.9% in each of 3 and 4** — it is risk parity only *by name*. Because assets 1 and 2 are highly correlated ($\rho=0.8$) and asset 3 is *negatively* correlated with asset 4 ($\rho=-0.5$), naive inverse-vol double-counts the redundant correlation among 1–2 and ignores the free diversification of 3–4. ERC's CCD solution fixes exactly that: **25.0% of risk, each, exactly.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Inverse volatility" is not always ERC.** It is ERC *iff* the correlation matrix is constant (all $\rho_{ij}$ equal). With real covariance structure, inverse-vol concentrates risk exactly where ERC would not — the worked example above proves it numerically.
2. **ERC is long-only by construction.** Relaxing the short constraint destroys uniqueness: multiple weight vectors can satisfy $w_i(\Sigma w)_i=\text{const}$ when shorting is allowed (Maillard §3.3). The solver above implicitly forces $w>0$; a short-allowed copy of the problem is a different animal.
3. **The solution is a function of $\Sigma$, full stop.** ERC takes no expected-return input — its robustness to return estimation is real, but it inherits *every* error in $\Sigma$. A covariance estimated on too-short a window, or un-denoised, quietly mismeasures "risk balance." (See [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes]] and [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]].)
4. **Convex ≠ cheap for huge $N$.** CCD is $O(N^2)$ per sweep and excellent for the $N\!\sim\!10$-100 asset-class case; at security-level $N\!>\!1000$ the same machinery is heavier, which is part of HRP's appeal ([[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]]).

---

### 5. Canonical Literature & Study References

- **Maillard, Roncalli & Teïletche** (2010), *JPM* 36(4) — definition (eq. 2), existence/uniqueness, the two-asset and constant-correlation closed forms (eq. 3), the beta form (eq. 5), the SQP/barrier programs (eqs. 6–8), and the volatility-ordering proof (App. A.3). **Math-authoritative for this page; all numbers re-verified.**
- **Qian, Edward** (2005): *Risk Parity Portfolios* — the practitioner statement that parity *means* equal risk contribution and is MV-optimal under equal Sharpe ratios + independence.
- **Griveau-Billion, T., Richard, J.-C. & Roncalli, T.**: *A Fast Algorithm for Computing High-Dimensional Risk Parity Portfolios* (2013) — the cyclical-coordinate-descent acceleration behind the implementation here.
- **Roncalli, Thierry**: *Introduction to Risk Parity and Budgeting*, CRC (2013) — Ch. on ERC algorithms and long-only constraints.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/02-risk-contributions|02 · Risk Contributions]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/04-risk-budgeting|04 · Risk Budgeting]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes]]
- Base: [[foundations/calculus-and-optimization/index|KKT Convex Optimization]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|Min-Variance & Constraints]]