---
title: "02 — Sklar's Theorem & the Copula Machinery"
tags:
  - pillar-quantitative-risk
  - copulas-and-dependence
  - sklars-theorem
  - copula
  - rank-correlation
  - kendall-tau
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/copulas-and-dependence/01-from-zero-intuition|01 · Copulas from Zero]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (CDFs, generalized inverses).

---

### 1. Intuition & Practical Objective

Page 01 showed that the marginals do not determine the joint distribution. This page supplies the *structure theorem* that says exactly what the missing piece is, and gives you the machinery to build and measure it.

**Sklar's theorem (1959)** is the decomposition theorem of multivariate risk:

> **Every joint distribution factors into its margins and a copula, and conversely any copula joined to any margins is a valid joint distribution.** For continuous margins the copula is unique.

The "conversely" is the practically explosive part. It says you can build a multivariate model **bottom-up**: model each risk factor's marginal distribution separately (where you often have lots of data), choose a dependence structure separately (where you usually have little), and glue them. A credit-risk book can have heavy-tailed loss marginals *and* a Gaussian dependence structure; an equity book can have normal marginals and a $t$ dependence structure. These are different models, and Sklar's theorem guarantees both are legitimate.

The two concrete tools this page delivers:

1. **The copula as a rank object** — $C(u_1,\dots,u_d)=\Pr[U_1\le u_1,\dots,U_d\le u_d]$ where $U_i=F_i(X_i)$; dependence on the quantile scale, invariant under monotone rescaling.
2. **Rank correlations as copula functionals** — Kendall's $\tau$ and Spearman's $\rho_S$ depend *only* on the copula, so they are the correct inputs for calibrating one. For the Gaussian copula they are closed forms in $\varrho$: $\rho_\tau=\frac{2}{\pi}\arcsin\varrho$ and $\rho_S=\frac{6}{\pi}\arcsin(\varrho/2)$.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The definition and Sklar's theorem

**Definition (copula).** A $d$-dimensional copula is a distribution function on $[0,1]^d$ with standard-uniform margins: $C:[0,1]^d\to[0,1]$, $C(u)=0$ if some $u_i=0$, $C(1,\dots,u_i,\dots,1)=u_i$, and $C$ is $d$-increasing (the rectangle inequality).

**Theorem (Sklar 1959).** Let $F$ be a joint CDF with margins $F_1,\dots,F_d$. Then there is a copula $C$ with

$$F(x_1,\dots,x_d)=C\big(F_1(x_1),\dots,F_d(x_d)\big),\qquad\text{and}\qquad
C(u_1,\dots,u_d)=F\big(F_1^{\leftarrow}(u_1),\dots,F_d^{\leftarrow}(u_d)\big),$$

where $F_i^{\leftarrow}(u)=\inf\{x:F_i(x)\ge u\}$. If the margins are continuous, $C$ is unique; otherwise it is unique only on $\mathrm{Ran}\,F_1\times\cdots\times\mathrm{Ran}\,F_d$.

**Proof sketch (continuous case).** Set $U_i=F_i(X_i)$. The probability transform gives $U_i\sim U(0,1)$, and $F_i^{\leftarrow}(U_i)=X_i$ a.s. Then

$$F(x)=\Pr[X_1\le x_1,\dots,X_d\le x_d]=\Pr[U_1\le F_1(x_1),\dots,U_d\le F_d(x_d)]=C\big(F_1(x_1),\dots,F_d(x_d)\big).$$

The converse: given any copula $C$ and margins $F_i$, the function $C(F_1(x_1),\dots,F_d(x_d))$ is a valid joint CDF with those margins — take $\mathbf U\sim C$ and set $X_i:=F_i^{\leftarrow}(U_i)$.

**Invariance.** If $T_1,\dots,T_d$ are strictly increasing, then $(T_1(X_1),\dots,T_d(X_d))$ has the **same copula**. Dependence is a property of ranks, not levels.

**Fréchet bounds.** $\max\!\big(\sum_i u_i+1-d,0\big)\le C(u)\le\min(u_1,\dots,u_d)$, with $W$ (countermonotone) and $M$ (comonotone) attained.

#### 2.2 The fundamental and implicit copulas

- **Independence** $\Pi(u)=\prod_i u_i$: $X$'s are independent iff their copula is $\Pi$.
- **Comonotonicity** $M(u)=\min(u_1,\dots,u_d)$: joint CDF of $(U,\dots,U)$; perfect positive dependence.
- **Countermonotonicity** $W(u_1,u_2)=\max(u_1+u_2-1,0)$: joint CDF of $(U,1-U)$; exists only in $d=2$.
- **Gaussian copula** (implicit, from $N_d(0,P)$):

$$C^{Ga}_P(u)=\Phi_P\!\big(\Phi^{-1}(u_1),\dots,\Phi^{-1}(u_d)\big),\qquad
C^{Ga}_\varrho(u,v)=\Phi_2\!\big(\Phi^{-1}(u),\Phi^{-1}(v);\varrho\big)=
\int_{-\infty}^{\Phi^{-1}(u)}\!\!\int_{-\infty}^{\Phi^{-1}(v)}\!\frac{1}{2\pi\sqrt{1-\varrho^2}}
\exp\!\Big(-\frac{s_1^2-2\varrho s_1s_2+s_2^2}{2(1-\varrho^2)}\Big)\,ds_1ds_2 .$$
- **$t$ copula** (implicit, from $t_d(\nu,0,P)$): $C^t_{\nu,P}(u)=t_{\nu,P}\big(t_\nu^{-1}(u_1),\dots,t_\nu^{-1}(u_d)\big)$.

**Simulation (Algorithm 7.11).** Generate $\mathbf Z\sim N_d(0,P)$; return $\mathbf U=(\Phi(Z_1),\dots,\Phi(Z_d))$. The $t$ copula adds a chi-square mixing: $\mathbf X=\mathbf Z\sqrt{\nu/W}$ with $W\sim\chi^2_\nu$, then $U_i=t_\nu(X_i)$.

**Meta distributions.** Given a copula and arbitrary margins, $F(x)=C(F_1(x_1),\dots,F_d(x_d))$ is a *meta-Gaussian* (or meta-$t$, meta-Clayton) distribution.

#### 2.3 Rank correlation as a copula functional

Neither Kendall's $\tau$ nor Spearman's $\rho_S$ sees anything but the copula:

$$\rho_\tau(X_1,X_2)=\mathbb{E}\big[\mathrm{sign}((X_1-\tilde X_1)(X_2-\tilde X_2))\big]=4\!\iint_{[0,1]^2}C\,dC-1,$$
$$\rho_S(X_1,X_2)=12\!\iint_{[0,1]^2}\big(C(u_1,u_2)-u_1u_2\big)\,du_1du_2=\rho\big(F_1(X_1),F_2(X_2)\big)\ \ (\text{linear corr.\ of the copula}).$$

Both are $0$ under independence, $\pm1$ under (counter)monotonicity, and invariant under strictly increasing transforms — exactly what Pearson correlation fails to be. For the **Gaussian copula** they have closed forms:

$$\boxed{\ \rho_\tau=\frac{2}{\pi}\arcsin\varrho\ },\qquad \boxed{\ \rho_S=\frac{6}{\pi}\arcsin\!\Big(\frac{\varrho}{2}\Big)\ },$$

so a Gaussian copula can be calibrated by inverting an empirical rank correlation: $\varrho=\sin(\pi\rho_\tau/2)$.

---

### 3. Computational Implementation — Sklar verified numerically

Stdlib only. Three checks: (a) the Gaussian copula computed as a bivariate-normal integral via Sklar's formula; (b) the probability transform of a simulated bivariate normal reproducing the copula's empirical joint CDF; (c) the rank-correlation closed forms.

```python
import math, random

def Phi(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)

def Phinv(p):
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,
        1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00]
    b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,
        6.680131188771972e+01,-1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,
       -2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00]
    d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00]
    pl=0.02425
    if p<pl:
        q=math.sqrt(-2*math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p<=1-pl:
        q=p-0.5; r=q*q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q=math.sqrt(-2*math.log(1-p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

def Phi2(h, k, rho, m=4000):
    """Bivariate standard-normal CDF: int_{-inf}^{h} phi(x) Phi((k-rho x)/s) dx (Simpson)."""
    s = math.sqrt(1.0-rho*rho); lo, hi = -10.0, h; n = m if m % 2 == 0 else m+1
    dx = (hi-lo)/n
    tot = phi(lo)*Phi((k-rho*lo)/s) + phi(hi)*Phi((k-rho*hi)/s)
    for i in range(1, n):
        x = lo+i*dx
        tot += (4.0 if i % 2 else 2.0)*phi(x)*Phi((k-rho*x)/s)
    return tot*dx/3.0

def gauss_copula(u, v, rho):
    """Sklar: C(u,v) = Phi_2(Phi^{-1}(u), Phi^{-1}(v); rho)."""
    return Phi2(Phinv(u), Phinv(v), rho)

rho = 0.7
print("Gaussian copula values C(u,v)=Phi2(Phi^-1(u),Phi^-1(v);rho), rho=0.7")
for (u,v) in [(0.5,0.5),(0.95,0.95),(0.05,0.05),(0.9,0.1)]:
    print(f"  C({u},{v}) = {gauss_copula(u,v,rho):.4f}   [independence {u*v:.4f}, comonotone {min(u,v):.4f}]")
print(f"  C(0.5,0.5) rho=0  -> {gauss_copula(0.5,0.5,0.0):.6f}  (= u*v = 0.250000, independence)")

# ---- Sklar numerical verification: empirical joint CDF of the probability transform ----
random.seed(7)
n = 400000
U = []; V = []
for _ in range(n):
    x = random.gauss(0,1); y = rho*x + math.sqrt(1-rho*rho)*random.gauss(0,1)
    U.append(Phi(x)); V.append(Phi(y))
uu, vv = 0.9, 0.3
emp = sum(1 for i in range(n) if U[i] <= uu and V[i] <= vv)/n
print(f"empirical P(U<={uu}, V<={vv}) = {emp:.4f}   vs  C(u,v) = {gauss_copula(uu,vv,rho):.4f}   (independence {uu*vv:.4f})")

# ---- rank correlations: Kendall tau = (2/pi) arcsin(rho), Spearman = (6/pi) arcsin(rho/2) ----
def kendall(a, b):
    m = len(a); c = 0
    for i in range(m):
        for j in range(i+1, m):
            c += 1 if (a[i]-a[j])*(b[i]-b[j]) > 0 else -1
    return c/(m*(m-1)/2)
def spearman(a, b):
    def rank(x):
        order = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0]*len(x)
        for pos, i in enumerate(order): r[i] = pos+1
        return r
    ra, rb = rank(a), rank(b); m = len(a)
    ma = sum(ra)/m; mb = sum(rb)/m
    cov = sum((ra[i]-ma)*(rb[i]-mb) for i in range(m))
    va = math.sqrt(sum((x-ma)**2 for x in ra)); vb = math.sqrt(sum((x-mb)**2 for x in rb))
    return cov/(va*vb)
s = 6000
ks, ss = kendall(U[:s], V[:s]), spearman(U[:s], V[:s])
print(f"Kendall tau: empirical {ks:.4f}  formula (2/pi)arcsin(rho) = {(2/math.pi)*math.asin(rho):.4f}")
print(f"Spearman rho: empirical {ss:.4f}  formula (6/pi)arcsin(rho/2) = {(6/math.pi)*math.asin(rho/2):.4f}")
```
```
Gaussian copula values C(u,v)=Phi2(Phi^-1(u),Phi^-1(v);rho), rho=0.7
  C(0.5,0.5) = 0.3734   [independence 0.2500, comonotone 0.5000]
  C(0.95,0.95) = 0.9196   [independence 0.9025, comonotone 0.9500]
  C(0.05,0.05) = 0.0196   [independence 0.0025, comonotone 0.0500]
  C(0.9,0.1) = 0.1000   [independence 0.0900, comonotone 0.1000]
  C(0.5,0.5) rho=0  -> 0.250000  (= u*v = 0.250000, independence)
empirical P(U<=0.9, V<=0.3) = 0.2992   vs  C(u,v) = 0.2990   (independence 0.2700)
Kendall tau: empirical 0.4893  formula (2/pi)arcsin(rho) = 0.4936
Spearman rho: empirical 0.6780  formula (6/pi)arcsin(rho/2) = 0.6829
```

Three verifications land at once. (a) The copula value $C(0.5,0.5)=0.3734$ sits strictly between independence ($0.2500$) and comonotonicity ($0.5000$), and at $\varrho=0$ it collapses to exactly $u\,v$ — Sklar's converse with the independence copula. (b) The copula computed by the double integral matches the empirical joint CDF of the **probability transform** $U=\Phi(X),\,V=\Phi(Y)$ to three decimals ($0.2992$ vs $0.2990$) — the proof of Sklar's theorem, executed. (c) The empirical rank correlations reproduce the closed forms: $\tau=0.4893$ vs $\frac{2}{\pi}\arcsin(0.7)=0.4936$ and $\rho_S=0.6780$ vs $\frac{6}{\pi}\arcsin(0.35)=0.6829$ (the gap is finite-sample bias in the $O(n^2)$ Kendall estimator).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Discrete margins break uniqueness.** With non-continuous margins (default indicators! ratings!) the copula is *not* unique — Example 7.6 of McNeil gives a bivariate Bernoulli where infinitely many copulas fit the same joint and margins. Any inference about "the" copula from discrete credit data is under-identified.
2. **A copula carries no marginal information.** Fitting a beautiful $t$ copula to normal-independence data does not make a fat-tailed portfolio; you must model the margins separately, or the joint tail is wrong even with a "correct" copula. This is the meta-distribution point.
3. **Pearson $\rho$ is not a copula parameter.** Only under elliptical dependence does linear correlation determine the copula; in general two variables can have $\rho=0$ and depend strongly. Rank correlations are the invariant, copula-functional measures.
4. **Simulation error hides in the tail.** Copula Monte Carlo is easy in the centre and hard where you need it — a $99.99\%$ quantile may rest on a handful of paths. Variance reduction (importance sampling) or analytic shortcuts (Vasicek) are not optional at extreme quantiles.
5. **The integral $4\iint C\,dC-1$ is a *definition*, not a formula.** Kendall's $\tau$ for most copulas has no closed form; you estimate it from the pseudo-sample $(U_i,V_i)$ and *then* invert. Inverting can leave the positive-definite range (the "$t$-copula correlation matrix from $\tau$ may not be PD" problem, Algorithm 7.57), requiring an eigenvalue repair.

---

### 5. Canonical Literature & Study References

- **Sklar, A. (1959)**, *Fonctions de répartition à n dimensions et leurs marges* — the original decomposition theorem.
- **McNeil, Frey & Embrechts (2015)**, *Quantitative Risk Management* — Ch 7 §7.1 (Definition 7.1, Sklar Thm 7.3, invariance 7.7, Fréchet 7.8, fundamental/implicit/explicit copulas, Algorithms 7.10–7.12) and §7.2.3–7.2.4 (Kendall 7.28, Spearman 7.33, dependence measures). *Formula-verified in the corpus.*
- **Nelsen, R. B. (2006)**, *An Introduction to Copulas*, 2nd ed. — Ch 2–4: the definitive treatment of copula properties, the Fréchet bounds and Archimedean construction.
- **Joe, H. (1997)**, *Multivariate Models and Dependence Concepts* — the dependence-measure and tail-dependence definitions.
- **Schweizer, B. & Wolff, E. F. (1981)**, *On nonparametric measures of dependence for random variables* — the rank-correlation/copula equivalence.
- **Nelsen (2006)** and **Embrechts, McNeil & Straumann (2002)** — the correlation-fallacy literature.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/copulas-and-dependence/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/copulas-and-dependence/index|Index Hub]]
- Continue: [[pillars/04-quantitative-risk/copulas-and-dependence/03-the-gaussian-copula-and-2008|03 · The Gaussian Copula & 2008]] · [[pillars/04-quantitative-risk/copulas-and-dependence/04-tail-dependence-and-t-copula|04 · Tail Dependence & the $t$-Copula]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (correlation matrices, PD repair)
- Sibling: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]] (the one-factor copula in credit terms) · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]]
