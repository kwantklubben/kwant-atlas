---
title: "03 — Tangency Portfolio, the Capital Market Line & CAPM"
tags:
  - pillar-portfolio-optimization
  - modern-portfolio-theory-and-mean-variance
  - tangency-portfolio
  - capm
  - sharpe-ratio
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · The Efficient Frontier]].

---

### 1. Intuition & Practical Objective

Once a riskless (or low-risk) asset exists, the investor's decision splits cleanly: **how much to put in cash vs. in one "best" risky portfolio** — and that best risky portfolio is the same for everyone, independent of risk aversion (Tobin's two-fund separation). That portfolio is the **tangency portfolio** $w_{\text{tan}}$: the point where the line from the riskless rate $r_f$ just touches (is tangent to) the risky frontier. It is *by construction* the portfolio with the **maximum Sharpe ratio**
$$\text{SR}(w)=\frac{w^T\mu-r_f}{\sqrt{w^T\Sigma w}}.$$
The practical objective: compute $w_{\text{tan}}$, its Sharpe ratio and the **Capital Market Line** $\mu=r_f+\text{SR}_{\max}\sigma$ on which every efficient risky-plus-cash portfolio lies — and then the **CAPM/Security Market Line**, the equilibrium statement that each asset's expected excess return is proportional to its *beta* against the tangency (market) portfolio. The entire CAPM is the frontier machinery read at the tangency point.

---

### 2. Mathematical Ground Truth & Derivations

**Tangency = maximum Sharpe (Merton 1972, §IV).** Maximizing SR over the budget line $w^T\mathbf{1}=1$ gives the first-order condition with
$$\boxed{\;w_{\text{tan}}=\frac{\Sigma^{-1}(\mu-r_f\mathbf{1})}{\mathbf{1}^T\Sigma^{-1}(\mu-r_f\mathbf{1})}\;}$$
(Merton eq. 44), valid whenever $r_f<\mu_{\text{mv}}=A/C$ (the tangency portfolio is then efficient; if $r_f\ge A/C$ the tangency lies on the *inefficient* branch and no finite tangency exists in the equilibrium sense — Merton §IV).

**Sharpe and the CML.** Let $\mu_t=w_{\text{tan}}^T\mu$ and $\sigma_t^2=w_{\text{tan}}^T\Sigma w_{\text{tan}}$. Two identities hold exactly:
$$\text{SR}_{\max}^2=\frac{(\mu_t-r_f)^2}{\sigma_t^2}=C r_f^2-2A r_f+B\qquad\text{and}\qquad \mu_t-r_f=\text{SR}_{\max}\,\sigma_t=\sqrt{C r_f^2-2A r_f+B}\;\sigma_t.$$
So the **Capital Market Line** is $\mu=r_f+\text{SR}_{\max}\,\sigma$, and *every* optimal portfolio is a blend of cash and $w_{\text{tan}}$: $w=\theta w_{\text{tan}}+(1-\theta)\mathbf{0}_{\text{cash}}$, with $\theta$ determined by risk aversion. This is Tobin's separation theorem: **all investors hold the same risky fund, only the cash/risky mix differs.**

**Security Market Line / CAPM (Sharpe 1964; Merton §V, eq. 45–47).** Under the equilibrium that the market portfolio is the tangency portfolio, each asset prices according to its covariance with the market:
$$\boxed{\;\mu_i-r_f=\beta_i\,(\mu_M-r_f),\qquad \beta_i=\frac{\sigma_{iM}}{\sigma_M^2}=\frac{\Sigma_i\cdot w_M}{\sigma_M^2}\;}$$
i.e. CAPM is a *security market line*: expected excess return is linear in $\beta$. Crucially, this holds **identically** for the tangency portfolio given *any* $\mu,\Sigma$ — it's a mathematical identity ($(\mu-r_f\mathbf{1})=D_t\,\Sigma w_t$ collapses to $\beta_i(\mu_M-r_f)$), not an empirical fit. The empirical content lives entirely in the assumption that *observed* prices reflect this equilibrium.

---

### 3. Computational Implementation — from covariance to tangency to CAPM

Stdlib only. Everything follows from $\Sigma^{-1}(\mu-r_f\mathbf{1})$. (All results cross-checked against `numpy`; they match to machine precision.)

```python
def inv(A):
    n=len(A); A=[r[:] for r in A]
    I=[[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for k in range(n):
        f=A[k][k]
        for j in range(n): A[k][j]/=f; I[k][j]/=f
        for i in range(n):
            if i==k: continue
            f=A[i][k]
            for j in range(n): A[i][j]-=f*A[k][j]; I[i][j]-=f*I[k][j]
    return I
def matvec(A,v): return [sum(A[i][k]*v[k] for k in range(len(v))) for i in range(len(A))]
def dot(a,b):    return sum(x*y for x,y in zip(a,b))

mu=[0.08,0.12,0.16]; rf=0.04
import math
S=[[0.100, 0.30*math.sqrt(0.100*0.180), 0.10*math.sqrt(0.100*0.250)],
   [0.30*math.sqrt(0.100*0.180), 0.180, 0.15*math.sqrt(0.180*0.250)],
   [0.10*math.sqrt(0.100*0.250), 0.15*math.sqrt(0.180*0.250), 0.250]]
Si=inv(S); one=[1.0,1.0,1.0]
A=dot(one,matvec(Si,mu)); B=dot(mu,matvec(Si,mu)); C=dot(one,matvec(Si,one))

z=matvec(Si,[mu[i]-rf for i in range(3)]); wt=[x/sum(z) for x in z]
mt=dot(wt,mu); st=(dot(wt,matvec(S,wt)))**0.5; SR=(mt-rf)/st
print(f"tangency w={['%.4f'%x for x in wt]}  mu_t={mt:.5f} sd_t={st:.5f} SR={SR:.5f}")
print(f"SR^2 computed={SR**2:.6f}   theory (C rf^2-2A rf+B)={C*rf*rf-2*A*rf+B:.6f}")

varM=dot(wt,matvec(S,wt))
print("\nCAPM / Security Market Line  (market == tangency):")
for i in range(3):
    beta=dot(S[i],wt)/varM
    sml=rf+beta*(mt-rf)
    print(f"  asset{i+1}: beta={beta:.4f}  mu_i-rf={mu[i]-rf:.5f}  "
          f"beta*(muM-rf)={beta*(mt-rf):.5f}   diff={abs(sml-(mu[i])):.2e}")

print("\nCML points (cash+risky blends of the tangency fund):")
for theta in (0.0,0.5,1.0):
    print(f"  theta={theta:.1f}: mu={rf+theta*(mt-rf):.4f} sigma={theta*st:.4f}")
```
```
tangency w=['0.2124', '0.3402', '0.4474']  mu_t=0.12940 sd_t=0.30641 SR=0.29176
SR^2 computed=0.085121   theory (C rf^2-2A rf+B)=0.085121

CAPM / Security Market Line  (market == tangency):
  asset1: beta=0.4474  mu_i-rf=0.04000  beta*(muM-rf)=0.04000   diff=1.39e-17
  asset2: beta=0.8949  mu_i-rf=0.08000  beta*(muM-rf)=0.08000   diff=0.00e+00
  asset3: beta=1.3423  mu_i-rf=0.12000  beta*(muM-rf)=0.12000   diff=0.00e+00

CML points (cash+risky blends of the tangency fund):
  theta=0.0: mu=0.0400 sigma=0.0000
  theta=0.5: mu=0.0847 sigma=0.1532
  theta=1.0: mu=0.1294 sigma=0.3064
```
Read the output: the theoretical Sharpe identity $(C r_f^2-2A r_f+B)=0.085121$ reproduces the *computed* $\text{SR}^2$ exactly, and the SML identity $\mu_i-r_f=\beta_i(\mu_M-r_f)$ holds to **all shown digits** (zero difference) for every asset — the tangency portfolio is self-consistent as a "market" by construction.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tangency requires $r_f<A/C$.** If the riskless rate is at or above the min-variance return, the tangency point vanishes (Merton §IV) — the "market" portfolio isn't a finite ray, and schools that draw a tangent regardless are drawing an impossible line.
2. **Sharpe maximization inherits every input error, doubled.** $w_{\text{tan}}\propto\Sigma^{-1}(\mu-r_f\mathbf{1})$ is the *most* fragile object in the folder — it needs both $\mu$ (hard) and $\Sigma^{-1}$ (amplifying), so the tiniest estimation error in the excess returns dominates the weights. This is the "estimation-error maximizer" alert of [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]].
3. **CAPM is an identity, not a discovery.** The SML holds by algebra for the tangency portfolio; the *empirical* claim is that real markets price expectations that way (and that the true market portfolio exists and is mean-variance-efficient). Testing CAPM is testing the market portfolio's measurability, not the algebra.
4. **The riskless asset is fictional.** Real borrowing is limited, taxed, and risky; proxy rates and short constraints break the clean cash/risky separation and the linear CML.

---

### 5. Canonical Literature & Study References

- **Merton, Robert C.**: *An Analytic Derivation of the Efficient Portfolio Frontier*, JFQA 7(4):1851–1872 (1972), §IV–V — the risky+riskless frontier, tangency (eq. 44), and the SML derivation (eq. 45–47).
- **Tobin, James**: *Liquidity Preference as Behavior Toward Risk*, RES 25(2):65–86 (1958) — two-fund separation; the cash/risky split this page operationalizes.
- **Sharpe, William F.**: *Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk*, Journal of Finance 19(3):425–442 (1964) — the CAPM/SML; follow with *Mutual Fund Performance* (1966), the Sharpe ratio paper.
- **Bodie, Kane & Marcus**, *Investments* — the CML/SML and beta interpretation.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · Efficient Frontier]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|04 · Min-Variance & Constraints]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]]
- Sibling: [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] (reverse-optimizes means so the tangency = market weights) · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]]