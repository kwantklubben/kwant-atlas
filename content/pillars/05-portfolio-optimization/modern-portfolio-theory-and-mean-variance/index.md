---
title: "Modern Portfolio Theory & Mean–Variance"
tags:
  - pillar-portfolio-optimization
  - modern-portfolio-theory-and-mean-variance
  - markowitz
  - efficient-frontier
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] and [[foundations/calculus-and-optimization/index|Calculus & KKT Optimization]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Modern Portfolio Theory (Markowitz 1952) is the discipline that turned portfolio construction into **an explicit quadratic program with a closed-form answer**. Its core claim is that an asset's value to a portfolio is *not* its own return and risk but how it **covaries** with every other holding — so the portfolio's return $w^T\mu$ and variance $w^T\Sigma w$ are the entire decision surface. From that one quadratic object, everything in this folder follows: the **efficient frontier**, the **tangency (Sharpe-optimal) portfolio**, **two-fund separation**, the **capital market line / CAPM**, and the **minimum-variance portfolio**.

This page is the *hub*: it gives the **fast formula lookup** (job #1) and routes you to six sub-pages that walk from raw intuition through the derivation, the frontier, tangency/CAPM, constraints, failure modes, and extensions. Every formula below is transcribed from **Merton (1972)** ($A,B,C,D$ machinery, frontier parabola, min-variance, tangency, SML) and cross-checked against Markowitz (1952), Sharpe (1964), and Tobin (1958); the check-column numbers were **re-executed and reproduced exactly** from the verified corpus (§3).

> **The one-sentence essence.** "Minimize portfolio variance subject to a target expected return — the solution is linear in $\Sigma^{-1}$; add a riskless asset and the Sharpe-optimal portfolio is the tangency portfolio, and a linear combination of the riskless asset with *any* two frontier funds spans the whole efficient set."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Worked on the folder's worked universe — three assets with
$\mu=\begin{bmatrix}0.08\\0.12\\0.16\end{bmatrix}$, $\Sigma=\begin{bmatrix}0.100&0.040&0.016\\0.040&0.180&0.032\\0.016&0.032&0.250\end{bmatrix}$, $r_f=0.04$. ($\Sigma$ from annual volatilities 0.10/0.18/0.25 with correlations 0.30, 0.10, 0.15.) All numbers below were **re-run and reproduced exactly** (see §3).

**Merton scalars** ($\mathbf{1}$ the ones-vector, $\Sigma^{-1}$ the inverse covariance):
$$
A=\mathbf{1}^T\Sigma^{-1}\mu,\quad B=\mu^T\Sigma^{-1}\mu,\quad C=\mathbf{1}^T\Sigma^{-1}\mathbf{1},\quad D=BC-A^2>0.
$$
Worked values: $A=1.53150,\ B=0.18447,\ C=14.48325,\ D=0.32622$.

| Quantity | Formula | Verified numbers |
|---|---|---|
| Frontier variance (parabola) | $\sigma^2(\mu)=\dfrac{C\mu^2-2A\mu+B}{D}$ | at $\mu{=}0.14$: $\sigma^2{=}0.12115$, $\sigma{=}0.3481$ |
| Min-variance portfolio | $\mu_{\text{mv}}=\dfrac{A}{C},\quad \sigma^2_{\text{mv}}=\dfrac{1}{C},\quad w_{\text{mv}}=\dfrac{\Sigma^{-1}\mathbf{1}}{\mathbf{1}^T\Sigma^{-1}\mathbf{1}}$ | $w_{\text{mv}}{=}[0.569,0.219,0.212]$, $\mu{=}0.10574$, $\sigma{=}0.26276$ |
| Generic frontier portfolio | $w^{\text{f}}(\mu^*)=\Sigma^{-1}(\lambda\mathbf{1}+\gamma\mu)$, $\lambda,\gamma$ solve $\begin{bmatrix}C&A\\A&B\end{bmatrix}\begin{bmatrix}\lambda\\\gamma\end{bmatrix}=\begin{bmatrix}1\\\mu^*\end{bmatrix}$ | $\mu^*{=}0.12 \Rightarrow [0.354,0.292,0.354]$, $\sigma{=}0.2794$ |
| **Tangency portfolio** (max Sharpe) | $w_{\text{tan}}=\dfrac{\Sigma^{-1}(\mu-r_f\mathbf{1})}{\mathbf{1}^T\Sigma^{-1}(\mu-r_f\mathbf{1})}$ | $w_{\text{tan}}{=}[0.2124,0.3402,0.4474]$, $\sigma{=}0.30641$ |
| Max Sharpe ratio | $\text{SR}_{\max}^2=C r_f^2-2A r_f+B=\dfrac{(\mu_t-r_f)^2}{\sigma_t^2}$ | $\text{SR}{=}0.29176$, ${}^2{=}0.085121$ |
| Capital market line | $\mu = r_f + \text{SR}_{\max}\,\sigma$ | slope $0.29176$ through $(0.3064,0.1294)$ |
| Security market line (CAPM) | $\mu_i = r_f + \beta_i(\mu_M-r_f),\quad \beta_i=\dfrac{\sigma_{iM}}{\sigma_M^2}$ | betas $0.4474,\,0.8949,\,1.3423$; holds exactly at tangency |
| Two-fund separation | any efficient $w = w_{\text{mv}}+\lambda\,(w_{\text{tan}}-w_{\text{mv}})$ | $\lambda{=}0.603$ reproduces $\mu{=}0.12$ to $4\times10^{-16}$ |

> **The $\Sigma^{-1}$-linearity is the whole story.** Because the objective is quadratic, every optimizing weight is **linear in $\Sigma^{-1}$**. That makes it beautiful and simultaneously fragile: whatever estimation error lives in $\Sigma$ (and especially in $\mu$) is amplified by $\Sigma^{-1}$, whose small eigenvalues blow up — see [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation — the frontier engine

This runs on the **standard library only** (Gauss–Jordan matrix inversion + dot products). It reproduces every verified number above. (All results were cross-checked against `numpy.linalg.solve/inv` and match to machine precision.)

```python
import math
def matvec(A, v): return [sum(A[i][k]*v[k] for k in range(len(v))) for i in range(len(A))]
def dot(a, b):    return sum(x*y for x, y in zip(a, b))
def inv(A):
    n = len(A); A = [r[:] for r in A]
    I = [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for k in range(n):
        f = A[k][k]
        for j in range(n): A[k][j]/=f; I[k][j]/=f
        for i in range(n):
            if i==k: continue
            f = A[i][k]
            for j in range(n): A[i][j]-=f*A[k][j]; I[i][j]-=f*I[k][j]
    return I

mu = [0.08, 0.12, 0.16]; rf = 0.04
import math
S  = [[0.100, 0.30*math.sqrt(0.100*0.180), 0.10*math.sqrt(0.100*0.250)],
      [0.30*math.sqrt(0.100*0.180), 0.180, 0.15*math.sqrt(0.180*0.250)],
      [0.10*math.sqrt(0.100*0.250), 0.15*math.sqrt(0.180*0.250), 0.250]]
Si = inv(S); one = [1.0,1.0,1.0]
A = dot(one, matvec(Si, mu)); B = dot(mu, matvec(Si, mu))
C = dot(one, matvec(Si, one)); D = B*C - A*A
print(f"A={A:.5f} B={B:.5f} C={C:.5f} D={D:.5f}")

z = matvec(Si, one); wmv = [x/sum(z) for x in z]
print(f"min-var: w={['%.3f'%x for x in wmv]} mu={dot(wmv,mu):.5f} "
      f"sd={(dot(wmv,matvec(S,wmv)))**0.5:.5f}  (A/C={A/C:.5f}, 1/C={1/C:.5f})")

z = matvec(Si, [mu[i]-rf for i in range(3)])
wt = [x/sum(z) for x in z]; mt = dot(wt, mu)
sd_t = (dot(wt, matvec(S, wt)))**0.5
print(f"tangency: w={['%.4f'%x for x in wt]} mu={mt:.5f} sd={sd_t:.5f} "
      f"Sharpe={(mt-rf)/sd_t:.5f}  (SR^2={C*rf*rf-2*A*rf+B:.6f})")

def frontier(mustar):
    lam = (1.0*B - A*mustar)/D; gam = (C*mustar - A*1.0)/D
    v1 = matvec(Si, one); v2 = matvec(Si, mu)
    return [lam*v1[i] + gam*v2[i] for i in range(3)]
print("frontier  mu* ->  w                                  sd      analytic-var")
for mustar in (0.10, 0.12, 0.14):
    w = frontier(mustar); sd = dot(w, matvec(S, w))**0.5
    an = (C*mustar*mustar - 2*A*mustar + B)/D
    ws = str(['%+.3f'%x for x in w])
    print(f"  {mustar:.2f}  {ws:>30}  {sd:.4f}  {an:.5f}")
```
```
A=1.53150 B=0.18447 C=14.48325 D=0.32622
min-var: w=['0.569', '0.219', '0.212'] mu=0.10574 sd=0.26276  (A/C=0.10574, 1/C=0.06905)
tangency: w=['0.2124', '0.3402', '0.4474'] mu=0.12940 sd=0.30641 Sharpe=0.29176  (SR^2=0.085121)
frontier  mu* ->  w                                  sd      analytic-var
  0.10  ['+0.655', '+0.189', '+0.155']  0.2655  0.07051
  0.12  ['+0.354', '+0.292', '+0.354']  0.2794  0.07807
  0.14  ['+0.053', '+0.395', '+0.553']  0.3481  0.12115
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **MVO is an "estimation-error maximizer."** Because $w \propto \Sigma^{-1}(\mu-r_f\mathbf{1})$, small errors in $\mu$ (the hardest inputs to estimate) are amplified by $\Sigma^{-1}$; Best & Grauer (1991) show a **0.08%** mean change can drive the most-sensitive asset out of a 100-asset portfolio.
2. **Covariance inversion instability.** Near-collinear assets make $\Sigma$ ill-conditioned ($\kappa(\Sigma)=\lambda_{\max}/\lambda_{\min}$ large); $\Sigma^{-1}$ then explodes tiny eigenvalue noise into extreme long/short weights.
3. **Unconstrained solutions are not investable.** The frontier assumes shorting is free; real long-only and turnover constraints push optimal weights to corner solutions — the bridge into [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|04 · Constraints]] and [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs]].

---

### 5. Canonical Literature & Study References

- **Merton, Robert C.**: *An Analytic Derivation of the Efficient Portfolio Frontier*, JFQA 7(4):1851–1872 (1972) — the $A,B,C,D$ closed forms, min-variance portfolio, tangency, and SML derived here. **The math-authoritative source for this folder; all formulas numerically verified.**
- **Markowitz, Harry**: *Portfolio Selection*, Journal of Finance 7(1):77–91 (1952) — the founding E-V quadratic program and efficient set.
- **Tobin, James**: *Liquidity Preference as Behavior Toward Risk*, Review of Economic Studies 25(2):65–86 (1958) — the (two-fund) separation theorem: a riskless asset + one efficient risky portfolio.
- **Sharpe, William F.**: *Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk*, Journal of Finance 19(3):425–442 (1964) — equilibrium tangency = market portfolio + the SML/CAPM.
- **Best & Grauer**: *On the Sensitivity of Mean–Variance-Efficient Portfolios to Changes in Asset Means*, Review of Financial Studies 4(2):315–342 (1991) — the formal "estimation-error maximizer" result.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/calculus-and-optimization/index|Calculus & KKT Optimization]]
- Sub-pages (in-folder): 01 From Zero · 02 Efficient Frontier · 03 Tangency & CAPM · 04 Min-Variance & Constraints · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · Efficient Frontier]] → [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/03-tangency-and-capm|03 · Tangency & CAPM]] → [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|04 · Min-Variance & Constraints]].
- **Robustness (practitioner/graduate):** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Bayesian Allocation]]