---
title: "04 — Confidence Intervals & Hypothesis Testing: Pivots, Size, Power & Multiplicity"
tags:
  - foundations
  - statistics-and-inference
  - confidence-intervals
  - hypothesis-testing
  - p-values
  - multiple-testing
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/02-point-estimation|02 · Point Estimation]] and [[foundations/statistics-and-inference/03-the-clt-and-sampling|03 · The CLT & Sampling]].

---

### 1. Intuition & Practical Objective

A point estimate is half an answer. The other half is a *set* of plausible values (a confidence interval) or a *decision* with a stated error rate (a hypothesis test). These two are the same construction viewed from two sides: **a \(1-\alpha\) confidence interval is exactly the set of parameter values that a level-\(\alpha\) test would not reject** (C&B Thm 9.2.1). Inverting the test gives the interval; the interval's coverage gives the test's size.

For a quant this is not academic:

- "The strategy's mean return is positive" \(\Rightarrow\) a one-sided \(t\)-test, and the Sharpe ratio's \(t\)-statistic \(= \text{SR}\sqrt{T}\).
- "The fund's VaR is 2%" \(\Rightarrow\) an interval estimator of a tail quantile.
- A p-value is the probability, *under the null*, of seeing a test statistic at least as extreme as observed — **not** the probability the null is true (the single most abused number in finance).

> **Why the grader cares.** Backtest overfitting is a multiplicity problem: test \(N\) strategies and the best looks significant by construction; the expected best spurious \(t\)-statistic grows like \(\sqrt{2\log N}\). Testing theory, done right, is what separates a real signal from the best of \(N\) coin flips.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Intervals by inverting tests (C&B §9.2.1)
For each \(\theta_0\), let \(A(\theta_0)\) be the acceptance region of a level-\(\alpha\) test of \(H_0:\theta=\theta_0\). Then
$$C(x)=\{\theta_0: x\in A(\theta_0)\}$$
is a \(1-\alpha\) confidence set; its **coverage probability** satisfies \(P_\theta(\theta\in C(X))\ge1-\alpha\). The **confidence coefficient** is \(\inf_\theta P_\theta(\theta\in C(X))\) (C&B §9.3.1).

#### 2.2 Pivots (C&B §9.2.2)
A **pivot** is \(Q(X,\theta)\) whose distribution is independent of all parameters (Def 9.2.1). For normal data, \(T=(\bar X-\mu)/(S/\sqrt n)\sim t_{n-1}\) is a pivot, giving the exact \(t\)-interval
$$\bar X\pm t_{n-1,\alpha/2}\,\frac{S}{\sqrt n}.$$
When no pivot exists, the CLT gives an **approximate** interval (C&B §9.4.2): for a statistic \(W\) with \(\widehat{\mathrm{Var}}(W)\),
$$W\pm z_{\alpha/2}\sqrt{\widehat{\mathrm{Var}}(W)}.$$
For MLEs the likelihood-based interval inverts the (asymptotically normal) pivot \(Q(X,\theta)=\dfrac{\partial_\theta\log L(\theta\mid X)}{\sqrt{-I_n(\theta)}}\sim N(0,1)\) (eq 9.4.1).

#### 2.3 Hypothesis testing: size, power, p-value (C&B §8.3)
Reject if the test statistic falls in the **rejection region** \(R\). Two error types:
- **Type I** (\(H_0\) true, rejected), probability \(\alpha=P_{\theta\in\Theta_0}(X\in R)\) — the **size** \(\alpha=\sup_{\theta\in\Theta_0}P_\theta(X\in R)\).
- **Type II** (\(H_1\) true, not rejected); **power** \(\beta(\theta)=P_\theta(X\in R)\), \(\theta\in\Theta_1\). Ideal: power 0 on \(\Theta_0\), 1 on \(\Theta_1\).

The **p-value** is the smallest \(\alpha\) at which the observed data would be rejected; equivalently \(p=\sup_{\theta\in\Theta_0}P_\theta(T\ge T_{\text{obs}})\) — data-dependent, not a fixed error rate (C&B §8.3.3).

#### 2.4 Optimal tests (C&B §8.3.2, §8.2.1)
- **Neyman–Pearson Lemma** (Thm 8.3.1): for simple \(H_0:\theta=\theta_0\) vs \(H_1:\theta=\theta_1\), the most powerful level-\(\alpha\) test rejects \(H_0\) when the likelihood ratio \(L(\theta_1)/L(\theta_0)>k\), with \(k\) set by the size.
- **Karlin–Rubin** (Thm 8.3.2): for a monotone likelihood-ratio family, a threshold test on the sufficient statistic is UMP for one-sided hypotheses.
- **Generalised likelihood-ratio test** (Def 8.2.1): reject for small \(\Lambda(x)=\dfrac{\sup_{\theta\in\Theta_0}L(\theta\mid x)}{\sup_{\theta\in\Theta}L(\theta\mid x)}\). **Wilks' theorem** (Thm 8.4.1): under \(H_0\), \(-2\log\Lambda\Rightarrow\chi^2_\nu\), \(\nu=\dim\Theta-\dim\Theta_0\).

#### 2.5 Multiplicity (the finance-critical part)
Testing \(m\) hypotheses at level \(\alpha\) each inflates the **family-wise error rate** (FWER):
$$\text{FWER}=P(\ge1\text{ false rejection})\le1-(1-\alpha)^m\approx m\alpha\ \text{(independence, small }\alpha).$$
- **Bonferroni:** use \(\alpha/m\) per test \(\Rightarrow\) FWER \(\le\alpha\).
- **Benjamini–Hochberg FDR:** sort p-values \(p_{(1)}\le\dots\le p_{(m)}\), reject the largest \(k\) with \(p_{(k)}\le\frac{k}{m}q\); controls the *expected proportion* of false discoveries \(\mathbb E[V/\max(R,1)]\le q\).
- **Max-statistic correction:** the best of \(N\) independent zero-skill strategies has \(t\)-statistic with \(\mathbb E[\max]\approx\sqrt{2\log N}\) — the deflated Sharpe / White Reality Check threshold.

---

### 3. Computational Implementation — t-Intervals, LRT, and the Multiplicity Tax

Standard library only, with a self-contained regularised incomplete gamma (for \(\chi^2\)) and normal inverse. We check \(t\)-interval coverage, a Poisson likelihood-ratio test against \(\chi^2_1\), and the multiplicity problem.

```python
import math, random
random.seed(23)
def mean(x): return sum(x)/len(x)
def var(x):
    m=mean(x); return sum((v-m)**2 for v in x)/(len(x)-1)
def Phi(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def gammainc_reg(a,x):
    if x<=0: return 0.0
    if x<a+1:
        term=1.0/a; s=term; n=0
        while True:
            n+=1; term*=x/(a+n); s+=term
            if abs(term)<1e-14*abs(s) or n>1000: break
        return s*math.exp(-x+a*math.log(x)-math.lgamma(a))
    b=x+1-a; c=1e30; d=1.0/b; h=d
    for i in range(1,1000):
        an=-i*(i-a); b+=2.0; d=an*d+b
        if abs(d)<1e-30: d=1e-30
        c=b+an/c
        if abs(c)<1e-30: c=1e-30
        d=1.0/d; de=d*c; h*=de
        if abs(de-1.0)<1e-14: break
    return 1.0-math.exp(-x+a*math.log(x)-math.lgamma(a))*h
def chi2inv(p,k):
    lo,hi=0.0,max(100.0,10*k)
    for _ in range(200):
        mid=(lo+hi)/2
        if gammainc_reg(k/2.0,mid/2.0)<p: lo=mid
        else: hi=mid
    return (lo+hi)/2

# (A) t-interval coverage: use exact t cutoff (0.975, 14 df), not z=1.96
n=15; B=40000; tc=2.1448; covN=covE=0
for _ in range(B):
    xn=[random.gauss(0,1) for _ in range(n)]
    xe=[]
    for _ in range(n):
        u=random.random()
        while u==0.0: u=random.random()
        xe.append(-math.log(u))
    mn=mean(xn); seN=math.sqrt(var(xn)/n)
    if mn-tc*seN<=0<=mn+tc*seN: covN+=1
    me=mean(xe); seE=math.sqrt(var(xe)/n)
    if me-tc*seE<=1.0<=me+tc*seE: covE+=1
print(f"(A) 95% t-CI coverage: Normal={covN/B:.4f}   Exponential={covE/B:.4f}")

# (B) Likelihood-ratio test for a Poisson mean: -2logLambda ~ chi^2_1 (Wilks)
lam0=3.0; n=60; B=30000; lr=[]
for _ in range(B):
    x=[]
    for _ in range(n):
        L=math.exp(-lam0); k=0; pr=1.0
        while True:
            k+=1; pr*=random.random()
            if pr<=L: break
        x.append(k-1)
    xb=mean(x)
    lr.append(2*n*(xb*math.log(xb/lam0)-(xb-lam0)) if xb>0 else 2*n*lam0)
print(f"(B) mean(-2logLam)={mean(lr):.4f} (chi2_1=1)  95th pct={sorted(lr)[int(0.95*B)]:.4f} "
      f"(chi2_1 0.95={chi2inv(0.95,1):.4f})")

# (C) Multiplicity: 20 independent TRUE nulls, alpha=0.05
m=20; R=20000; fwe=0; bonf=0
def p_of_z(z): return 2*(1-Phi(abs(z)))
for _ in range(R):
    ps=[p_of_z(random.gauss(0,1)) for _ in range(m)]
    if min(ps)<0.05: fwe+=1
    if min(ps)<0.05/m: bonf+=1
print(f"(C) P(>=1 raw p<0.05)={fwe/R:.4f} (theory 1-0.95^20={1-0.95**20:.4f})  "
      f"Bonferroni FWER={bonf/R:.4f}")
```
```
(A) 95% t-CI coverage: Normal=0.9504   Exponential=0.9123
(B) mean(-2logLam)=0.9941 (chi2_1=1)  95th pct=3.8614 (chi2_1 0.95=3.8415)
(C) P(>=1 raw p<0.05)=0.6467 (theory 1-0.95^20=0.6415)  Bonferroni FWER=0.0483
```

The \(t\)-interval is exact for normal data (0.9504) but *under-covers* on exponential data (0.9123) — the CLT's finite-sample error, visible. The LRT statistic matches its \(\chi^2_1\) limit. And 20 independent nulls produce at least one "significant" result 65% of the time — Bonferroni restores the 5% FWER (0.0483).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Interpreting \(p=0.04\) as "4% chance the null is true".** The p-value is \(P(\text{data this extreme}\mid H_0)\), not \(P(H_0\mid\text{data})\); the two differ by the prior odds (Bayes' rule). A 4% p-value on a coin that all prior evidence says is fair is weak evidence.
2. **Ignoring multiplicity.** Reporting the best of many tested strategies at a raw 5% level is a near-certain false positive; the expected best-of-\(N\) spurious \(t\approx\sqrt{2\log N}\). Correct with Bonferroni/FDR or a bootstrap Reality Check.
3. **Confusing statistical and economic significance.** A t-stat of 3 from a century of daily data with a 1-basis-point edge is statistically "real" and economically worthless; and a short high-Sharpe sample can be economically huge and statistically indistinguishable from noise.
4. **Under-covering intervals.** Using \(z\) instead of \(t\), or the CLT on short fat-tailed samples, produces intervals that cover less than advertised (0.912 not 0.950) — your "95%" is really 91%.
5. **One-sided vs two-sided silent switch.** Peeking at the data, then choosing the direction of a one-sided test, doubles the true Type-I rate. Pre-specify the test.
6. **The LRT's edge-of-support trap.** Wilks' theorem fails when the null is on the boundary of the parameter space or the support depends on \(\theta\); then \(-2\log\Lambda\) is *not* \(\chi^2_\nu\). Check the regularity conditions.

---

### 5. Canonical Literature & Study References

- **Casella & Berger**, *Statistical Inference*, Ch 8 (LRT §8.2.1, Neyman–Pearson Lemma Thm 8.3.1, Karlin–Rubin Thm 8.3.2, size/power §8.3.1, p-values §8.3.3, Wilks Thm 8.4.1, large-sample tests §8.4.2), Ch 9 (inverting tests Thm 9.2.1, pivots Def 9.2.1, coverage §9.3.1, approximate/ML intervals §9.4.1–§9.4.2). *Primary source, formulas cross-checked in the corpus.*
- **Hastie, Tibshirani & Friedman**, *ESL*, Ch 7 (§7.10.2 the wrong-vs-right CV: screening outside folds gives 3% vs a true 50%). The validation counterpart of multiplicity.
- **White, H. (2000)**, *A Reality Check for Data Snooping* — the canonical bootstrap test for the best of many strategies.
- **Harvey, Liu & Zhu (2016)**, "…and the Cross-Section of Expected Returns" — multiple-testing thresholds for factor discovery.

---

### 6. Connected Graph Bridges

- Back: [[foundations/statistics-and-inference/03-the-clt-and-sampling|03 · The CLT & Sampling]] · [[foundations/statistics-and-inference/02-point-estimation|02 · Point Estimation]] · [[foundations/statistics-and-inference/index|Index Hub]]
- Continue: [[foundations/statistics-and-inference/05-bias-variance-and-validation|05 · Bias–Variance & Validation]] · [[foundations/statistics-and-inference/06-advanced-extensions|06 · Advanced Extensions]]
- Applications: [[pillars/01-quantitative-research/index|Quantitative Research]] (backtesting, signal validation) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (tail interval estimation) · [[foundations/econometrics-and-timeseries/index|Econometrics]] (ACF/PACF and Ljung–Box are hypothesis tests)
