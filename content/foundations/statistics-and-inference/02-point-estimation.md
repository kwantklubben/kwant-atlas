---
title: "02 — Point Estimation: MLE, Method of Moments, Bias, Variance & Cramér–Rao"
tags:
  - foundations
  - statistics-and-inference
  - maximum-likelihood
  - method-of-moments
  - bias-variance
  - cramer-rao
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/01-from-zero-intuition|01 · From Zero]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] (maximisation).

---

### 1. Intuition & Practical Objective

Given data, how do you produce a single best guess of an unknown parameter? There are two workhorse recipes, and understanding them *and* how to judge them is the core of estimation theory.

- **Maximum likelihood (MLE):** choose the parameter that makes the data you actually saw *most probable*. It is the default estimator in all of quantitative finance: GARCH parameters, default intensities, factor loadings, and \(p\) in a logistic scorecard are all MLEs.
- **Method of moments (MoM):** set the theoretical moments equal to the sample moments and solve. Older, often cruder, but closed-form and a great starting point for the MLE's numerical search.

The practical objective is to know **which estimator to trust and why**. "Best" is not "unbiased": the right yardstick is **mean squared error**, \(\mathbb E(W-\theta)^2=\mathrm{Var}(W)+(\mathrm{Bias}\,W)^2\), and the theoretical floor is the **Cramér–Rao lower bound**, attained exactly (asymptotically) by the MLE. Two numbers — bias and variance — decide everything, and one bound tells you when to stop looking for something better.

> **Why it matters for the Atlas.** A GARCH(1,1) fit, a VaR quantile, an implied default probability, and a Sharpe ratio are all point estimates with sampling distributions. Mis-reading bias versus variance is how a model that is "unbiased on paper" still blows up out-of-sample.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Maximum likelihood (C&B §7.2.2)
Let \(X_1,\dots,X_n\) be i.i.d. with density/pmf \(f(x\mid\theta)\). The likelihood is \(L(\theta\mid x)=\prod_i f(x_i\mid\theta)\) and the MLE maximises \(\ell(\theta)=\log L(\theta\mid x)\). For a regular model the score is zero at the MLE:
$$
\ell'(\hat\theta\mid x)=\sum_{i=1}^n\frac{\partial}{\partial\theta}\log f(x_i\mid\hat\theta)=0,\qquad \hat\theta=\arg\max_\theta \ell(\theta).
$$
Properties: **invariance** — if \(\hat\theta\) is the MLE of \(\theta\), then \(g(\hat\theta)\) is the MLE of \(g(\theta)\); **consistency** (Thm 7.3.8); and **asymptotic normality/efficiency** (below).

#### 2.2 Method of moments (C&B §7.2.1)
Equate the first \(k\) population moments to the sample moments and solve for the \(k\) parameters:
$$
\mathbb E_\theta[X^j]=\frac1n\sum_{i=1}^n X_i^j,\quad j=1,\dots,k\;\Longrightarrow\;\hat\theta_{\text{MoM}}.
$$
For a two-parameter family this gives two equations in two unknowns; the MoM estimate is often used as the MLE's starting value.

#### 2.3 Bias, variance and mean squared error (C&B §7.3.1)
$$
\boxed{\;\mathbb E_\theta(W-\theta)^2=\mathrm{Var}_\theta\,W+(\mathrm{Bias}_\theta W)^2,\qquad \mathrm{Bias}_\theta W=\mathbb E_\theta W-\theta.\;}
$$
If \(W\) is unbiased, MSE \(=\) variance. The classic illustration: for normal data,
$$
\hat\sigma^2_{\text{MLE}}=\frac1n\sum(X_i-\bar X)^2\quad\text{(biased, }\mathbb E=\tfrac{n-1}{n}\sigma^2)\quad\text{vs}\quad S^2=\frac1{n-1}\sum(X_i-\bar X)^2\quad\text{(unbiased)},
$$
$$
\mathrm{MSE}(\hat\sigma^2_{\text{MLE}})=\frac{2n-1}{n^2}\sigma^4 \;<\; \frac{2}{n-1}\sigma^4=\mathrm{MSE}(S^2).
$$
Trading a little bias for less variance *lowers* MSE — the first sighting of the bias–variance tradeoff that [[foundations/statistics-and-inference/05-bias-variance-and-validation|05]] makes central.

#### 2.4 Cramér–Rao lower bound (C&B Thm 7.3.1)
For any estimator \(W\) with \(\mathbb E_\theta W=\tau(\theta)\),
$$
\mathrm{Var}_\theta W\ge\frac{[\tau'(\theta)]^2}{n\,\mathbb E_\theta\!\left[\left(\frac{\partial}{\partial\theta}\log f(X\mid\theta)\right)^2\right]}=\frac{[\tau'(\theta)]^2}{I_n(\theta)},
$$
where \(I_n(\theta)=n\,\mathbb E[(\partial_\theta\log f)^2]=n\,\mathrm{Var}(\partial_\theta\log f)\) is the **Fisher information**. Bigger information \(\Rightarrow\) tighter bound \(\Rightarrow\) less uncertainty. An unbiased estimator attaining the bound is **best unbiased (UMVUE)**. Caveat: the bound requires differentiating under the integral, which fails when the support depends on \(\theta\) (the uniform scale example, C&B Ex 7.3.5, beats the bound).

#### 2.5 Asymptotic normality, efficiency and the delta method (C&B §7.4)
Under regularity conditions, the MLE is **asymptotically efficient**:
$$
\hat\theta\ \approx\ N\!\left(\theta,\ \frac{1}{I_n(\theta)}\right),\qquad \mathrm{Var}\big(h(\hat\theta)\big)\approx\frac{[h'(\theta)]^2}{I_n(\theta)}\approx\frac{[h'(\theta)]^2}{-\ell''(\hat\theta\mid x)}\ \text{(observed information, eq 7.4.1)}.
$$
For a smooth function of the sample mean, the **delta method** expands to first order (eq 7.4.5):
$$
\mathrm{Var}\,g(\bar X)\approx[g'(\mu)]^2\,\mathrm{Var}\,\bar X,\qquad \text{multivariate: }\ \sum_i g_i'^2\mathrm{Var}X_i+2\sum_{i<j}g_i'g_j'\mathrm{Cov}(X_i,X_j).
$$

---

### 3. Computational Implementation — MLE by Newton–Raphson, MoM, MSE and the delta method

Standard library only. The headline is an MLE with **no closed form** (the Gamma shape), solved by Newton's method on the score equation using digamma/trigamma functions.

```python
import math, random
random.seed(11)
def mean(x): return sum(x)/len(x)
def var(x):
    m=mean(x); return sum((v-m)**2 for v in x)/(len(x)-1)

# ---- (A) MLE with NO closed form: Gamma(alpha,beta) shape, solved by Newton-Raphson
def digamma(x):
    r=0.0
    while x<6: r-=1.0/x; x+=1.0
    f=1.0/(x*x)
    return r+math.log(x)-0.5/x + f*(-1/12 + f*(1/120 + f*(-1/252 + f*(1/240 + f*(-1/132)))) )
def trigamma(x):
    r=0.0
    while x<6: r+=1.0/(x*x); x+=1.0
    f=1.0/(x*x)
    return r+1.0/x+0.5*f + f*(1/6 - f*(1/30 - f*(1/42 - f*(1/30 - f*(5/66)))) )
def gamma_mle(x):
    logbar=mean([math.log(v) for v in x]); xbar=mean(x)
    a=xbar/max(var(x),1e-12)                 # MoM start
    for _ in range(100):                     # Newton on  log(a)-psi(a)+logbar-log(xbar)=0
        h=math.log(a)-digamma(a)+logbar-math.log(xbar); hp=1.0/a - trigamma(a)
        a-=h/hp
        if abs(h)<1e-13: break
    return a, a/xbar                         # beta_hat = alpha_hat / xbar

alpha, beta, n, B = 4.0, 2.0, 400, 120
est_a=[]; est_b=[]; mom_a=[]
for _ in range(B):
    x=[sum(-math.log(random.random()) for _ in range(int(alpha)))/beta for _ in range(n)]
    a,b=gamma_mle(x); est_a.append(a); est_b.append(b); mom_a.append(mean(x)**2/var(x))
print(f"(A) Gamma MLE (Newton-Raphson), true alpha={alpha}, beta={beta}, n={n}")
print(f"    mean(alpha_MLE)={mean(est_a):.4f} (sd {math.sqrt(var(est_a)):.4f})   mean(beta_MLE)={mean(est_b):.4f}")
print(f"    mean(alpha_MoM)={mean(mom_a):.4f}   Var(alpha_MLE)~{var(est_a):.5f}")

# ---- (B) MSE = Var + Bias^2 : biased sigma^2_MLE beats unbiased S^2
sig2, n, B = 4.0, 10, 40000
mle=[]; s2=[]
for _ in range(B):
    x=[random.gauss(0,math.sqrt(sig2)) for _ in range(n)]; m=mean(x)
    mle.append(sum((v-m)**2 for v in x)/n); s2.append(sum((v-m)**2 for v in x)/(n-1))
print(f"\n(B) n=10 Normal variance:")
print(f"    MSE(sigma2_MLE)={mean([(v-sig2)**2 for v in mle]):.4f}  theory (2n-1)/n^2*sig^4={(2*n-1)/n**2*sig2**2:.4f}")
print(f"    MSE(S^2)       ={mean([(v-sig2)**2 for v in s2]):.4f}  theory 2*sig^4/(n-1)     ={2*sig2**2/(n-1):.4f}")

# ---- (C) Delta method: Bernoulli(p) odds ratio
p, n, B = 0.3, 500, 40000
odds=[]
for _ in range(B):
    Y=sum(1 for _ in range(n) if random.random()<p); ph=Y/n
    odds.append(ph/(1-ph))
print(f"\n(C) Odds ratio p/(1-p), p=0.3 n=500:")
print(f"    Var(odds_hat)={var(odds):.5f}   delta-method p/(n(1-p)^3)={p/(n*(1-p)**3):.5f}")

# ---- (D) Cramer-Rao: exponential rate MLE is efficient
lam,n,B=2.5,200,20000
ests=[1.0/mean([-math.log(random.random())/lam for _ in range(n)]) for _ in range(B)]
print(f"\n(D) Exponential rate MLE: Var={var(ests):.6f}  CRLB lam^2/n={lam**2/n:.6f}")
```
```
(A) Gamma MLE (Newton-Raphson), true alpha=4.0, beta=2.0, n=400
    mean(alpha_MLE)=4.0297 (sd 0.2569)   mean(beta_MLE)=2.0165
    mean(alpha_MoM)=4.0188   Var(alpha_MLE)~0.06602

(B) n=10 Normal variance:
    MSE(sigma2_MLE)=3.0429  theory (2n-1)/n^2*sig^4=3.0400
    MSE(S^2)       =3.5526  theory 2*sig^4/(n-1)     =3.5556

(C) Odds ratio p/(1-p), p=0.3 n=500:
    Var(odds_hat)=0.00177   delta-method p/(n(1-p)^3)=0.00175

(D) Exponential rate MLE: Var=0.031922  CRLB lam^2/n=0.031250
```

Three takeaways visible in the numbers: the numerical MLE recovers \(\alpha=4.03\) without a closed form; the biased MLE of \(\sigma^2\) beats \(S^2\) on MSE (3.043 vs 3.553) exactly as the formula predicts; and the exponential MLE's variance sits on the Cramér–Rao bound (0.0319 vs 0.03125 — efficient).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Equating "unbiased" with "best".** MSE \(=\) Var \(+\) Bias\(^2\); the biased estimator wins whenever the variance saved exceeds the squared bias added. Choosing \(S^2\) "because it's unbiased" can be strictly worse.
2. **Trusting the delta method for non-monotone \(h\).** If \(h'(\theta)=0\) somewhere, the plug-in variance can be (near-)zero and badly wrong — the MLE of \(p(1-p)\) reports \(\mathrm{Var}=0\) at \(p=\tfrac12\) (C&B §7.4.1). Always check \(h'\).
3. **Applying Cramér–Rao when the support depends on \(\theta\).** For uniform data the bound is unattainable (Ex 7.3.5 beats it); the regularity condition is not decoration.
4. **Boundary/identifiability failures in MLE.** A GARCH persistence \(\hat\alpha+\hat\beta\to1\), or a Gaussian-mixture with a diverging component, makes the likelihood unbounded or flat — the Newton iteration diverges. Regularity is a promise the model must keep.
5. **Numerical MLE gone wrong.** Bad starting values, non-concave likelihoods, and over-parameterised models give local optima that look like findings. Always re-start from MoM and check convergence.

---

### 5. Canonical Literature & Study References

- **Casella & Berger**, *Statistical Inference*, Ch 7 §7.2 (MoM, MLE, invariance), §7.3 (MSE eq 7.3.1, Cramér–Rao Thm 7.3.1, Rao–Blackwell, sufficiency, consistency §7.3.4), §7.4 (asymptotic variance eq 7.4.1, Taylor/delta method eqs 7.4.4–7.4.5). *Primary source, formulas cross-checked in the corpus.*
- **Hastie, Tibshirani & Friedman**, *ESL*, Ch 8 §8.2 (MLE vs Bayesian estimation), Ch 7 (why in-sample error is optimistic).
- **Tsay**, *Analysis of Financial Time Series*, Ch 3 (MLE for GARCH/EGARCH — the production use of this machinery).

---

### 6. Connected Graph Bridges

- Back: [[foundations/statistics-and-inference/01-from-zero-intuition|01 · From Zero]] · [[foundations/statistics-and-inference/index|Index Hub]]
- Continue: [[foundations/statistics-and-inference/03-the-clt-and-sampling|03 · The CLT & Sampling]] · [[foundations/statistics-and-inference/04-confidence-intervals-and-testing|04 · Confidence Intervals & Testing]] · [[foundations/statistics-and-inference/05-bias-variance-and-validation|05 · Bias–Variance & Validation]]
- Application: [[foundations/econometrics-and-timeseries/04-volatility-modeling|Volatility Modeling]] (GARCH MLE) · [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt-Data]] (regularised likelihoods) · [[foundations/calculus-and-optimization/index|Optimization]] (the numerical search itself)
