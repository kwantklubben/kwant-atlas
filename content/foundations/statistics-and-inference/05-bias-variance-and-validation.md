---
title: "05 — Bias–Variance, Cross-Validation & Model Selection"
tags:
  - foundations
  - statistics-and-inference
  - bias-variance
  - cross-validation
  - model-selection
  - overfitting
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/02-point-estimation|02 · Point Estimation]] (MSE) and [[foundations/statistics-and-inference/03-the-clt-and-sampling|03 · The CLT & Sampling]] (sampling distributions).

---

### 1. Intuition & Practical Objective

Why does a model that fits the training data *perfectly* often predict *terribly*? Because the error of a model has two sources that trade off against each other, and fitting harder improves one while worsening the other.

- **Bias:** systematic error — the model family is not rich enough to represent the truth (a straight line cannot bend).
- **Variance:** sensitivity to the particular training sample — a rich model moves wildly when the data changes (a degree-12 polynomial chases noise).

**Total expected prediction error = bias² + variance + irreducible noise.** The first two sum to a U-shape in model complexity; the minimum is the sweet spot. This is the same decomposition you met in [[foundations/statistics-and-inference/02-point-estimation|02]] (MSE = Var + Bias²), now applied to *predictions* rather than parameters. Validation — cross-validation and penalised criteria (AIC, BIC) — is how you find the minimum without cheating by looking at the test set.

> **Why the grader cares.** Every hyper-parameter in a quant pipeline (lookback window, model order, regularisation strength, number of factors) is chosen by this tradeoff. And the canonical way to get it *wrong* — screening features on the whole dataset before cross-validating — is the most common silent bug in quantitative research.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The bias–variance decomposition (ESL eq 2.25 two-term; eq 2.46 / 7.9 three-term)
For a target \(Y=f(X)+\varepsilon\) with \(\mathbb E[\varepsilon]=0\), \(\mathrm{Var}\,\varepsilon=\sigma^2_\varepsilon\), and an estimator \(\hat f\) fit on a random training set \(T\):
$$\underbrace{\mathbb E_{T,Y}\big[(Y-\hat f(x_0))^2\big]}_{\text{expected test MSE}}=\underbrace{\sigma^2_\varepsilon}_{\text{irreducible}}+\underbrace{\big(\mathbb E_T[\hat f(x_0)]-f(x_0)\big)^2}_{\text{Bias}^2}+\underbrace{\mathbb E_T\big[(\hat f(x_0)-\mathbb E_T[\hat f(x_0)])^2\big]}_{\text{Variance}}.$$
(The noise-free two-term form ESL eq 2.25 drops \(\sigma^2_\varepsilon\); the full three-term form with irreducible error is ESL eq 2.46 / 7.9.) Increasing complexity typically **lowers bias\(^2\) and raises variance**; the sum is U-shaped.

#### 2.2 In-sample optimism (ESL §7.2–7.4)
Training error *always* decreases with complexity and is therefore a **biased-down** estimate of test error. For a linear model with \(d\) parameters,
$$\mathbb E[\text{err}_{\text{in}}]\approx\text{err}_{\text{out}}-\frac{2d}{n}\sigma^2_\varepsilon,\qquad \text{(optimism }\approx\tfrac{2d}{n}\sigma^2_\varepsilon\text{)}.$$
The **effective degrees of freedom** of a linear smoother \(\hat y=Sy\) is \(\mathrm{df}=\operatorname{tr}(S)\) (ESL eq 7.32) — not the raw parameter count.

#### 2.3 Cross-validation (ESL §7.10, eq 7.48)
**\(K\)-fold CV** splits the data into \(K\) folds; for each fold \(k\) fit on the other \(K-1\) folds and score on fold \(k\):
$$\mathrm{CV}_{(K)}=\frac1K\sum_{k=1}^K\frac{1}{|C_k|}\sum_{i\in C_k}\mathcal L\!\left(y_i,\ \hat f^{(-k)}(x_i)\right).$$
- \(K=n\) is **leave-one-out**: low bias, high variance, expensive.
- \(K=5\) or \(10\) is the recommended compromise.
- **One-standard-error rule:** among models within one SE of the minimum CV error, pick the simplest.

#### 2.4 Penalised criteria (ESL eqs 7.29/7.35; Tsay eq 2.16)
Trade fit against complexity without a validation set:
$$\text{AIC}=-2\log L+2k\qquad(\text{ESL }-\tfrac2N\log L+\tfrac{2d}N),\qquad \text{BIC}=-2\log L+k\log n\qquad(\text{ESL }-\tfrac2N\log L+\tfrac{\log N\,d}{N}).$$
BIC penalises complexity harder (\(\log n\) vs \(2\)) and is asymptotically consistent, so it selects simpler models than AIC at finite \(n\).

#### 2.5 The wrong way to cross-validate (ESL §7.10.2)
If a **screening** step (feature selection, variance filter) is applied to the *whole* dataset before splitting, information leaks from the test folds into training. ESL's worked example: full-data screening yields an average CV error of **3%** where the true error is **50%** — a 16× illusion of skill. **All data-dependent preprocessing must happen inside each training fold.**

---

### 3. Computational Implementation — the U-curve, CV, and AIC/BIC

Standard library only. We decompose the prediction error of polynomial fits into bias², variance and irreducible noise; watch in-sample error fall while CV error explodes; and confirm AIC/BIC pick the true (linear) model.

```python
import math, random
random.seed(29)
def mean(x): return sum(x)/len(x)

def truef(x): return 0.75*(x+1.0)                 # linear truth, x ~ U[-1,1]
def fit_poly(xs,ys,deg):                          # normal equations (|x|<=1: well conditioned)
    m=deg+1
    A=[[sum(x**(i+j) for x in xs) for j in range(m)] for i in range(m)]
    b=[sum(y*x**i for x,y in zip(xs,ys)) for i in range(m)]
    for c in range(m):
        p=max(range(c,m), key=lambda r: abs(A[r][c])); A[c],A[p]=A[p],A[c]; b[c],b[p]=b[p],b[c]
        for r in range(c+1,m):
            f=A[r][c]/A[c][c]
            for k in range(c,m): A[r][k]-=f*A[c][k]
            b[r]-=f*b[c]
    beta=[0.0]*m
    for r in range(m-1,-1,-1):
        beta[r]=(b[r]-sum(A[r][k]*beta[k] for k in range(r+1,m)))/A[r][r]
    return beta
def evalp(beta,x): return sum(c*x**i for i,c in enumerate(beta))

# (A) Bias^2 + variance + irreducible = expected test MSE  [ESL eq 2.46 / 7.9]
n=25; sig=0.7; x0=0.3; M=600
print("(A) x0=0.3, n=25, sigma^2=%.2f, irreducible=%.2f" % (sig**2, sig**2))
for deg in (1,2,3,5,8,12):
    preds=[]
    for _ in range(M):
        xs=[random.uniform(-1,1) for _ in range(n)]
        ys=[truef(x)+random.gauss(0,sig) for x in xs]
        preds.append(evalp(fit_poly(xs,ys,deg),x0))
    mp=mean(preds); bias2=(mp-truef(x0))**2; v=sum((p-mp)**2 for p in preds)/(M-1)
    print(f"  deg={deg:2d}  bias^2={bias2:.5f}  variance={v:.5f}  MSE={bias2+v:.5f}")

# (B) in-sample vs K-fold CV error  [ESL eq 7.48]
n=40; sig=0.5; N=200
def mse_poly(xs,ys,deg,xt,yt):
    b=fit_poly(xs,ys,deg); return sum((evalp(b,x)-y)**2 for x,y in zip(xt,yt))/len(xt)
tr={d:[] for d in range(1,11)}; cv={d:[] for d in range(1,11)}
for _ in range(N):
    xs=[random.uniform(-1,1) for _ in range(n)]
    ys=[truef(x)+random.gauss(0,sig) for x in xs]
    idx=list(range(n)); random.shuffle(idx); folds=[idx[i::5] for i in range(5)]
    for deg in range(1,11):
        tr[deg].append(mse_poly(xs,ys,deg,xs,ys))
        ce=0.0
        for f in folds:
            te=set(f); trn=[i for i in range(n) if i not in te]
            b=fit_poly([xs[i] for i in trn],[ys[i] for i in trn],deg)
            ce+=sum((evalp(b,xs[i])-ys[i])**2 for i in te)/len(f)
        cv[deg].append(ce/5)
best=min(range(1,11), key=lambda d: mean(cv[d]))
print(f"\n(B) in-sample MSE: deg=1 {mean(tr[1]):.4f} -> deg=10 {mean(tr[10]):.4f} (monotone down)")
print(f"    CV MSE       : deg=1 {mean(cv[1]):.4f} -> deg=10 {mean(cv[10]):.4f}")
print(f"    CV selects degree = {best}   (true model is degree 1)")

# (C) AIC vs BIC  [ESL 7.29/7.35 ; Tsay 2.16]
print("\n(C) AIC/BIC, true degree 1")
for deg in (1,2,3,6,10):
    aic=[];bic=[]
    for _ in range(400):
        xs=[random.uniform(-1,1) for _ in range(n)]
        ys=[truef(x)+random.gauss(0,sig) for x in xs]
        b=fit_poly(xs,ys,deg)
        rss=sum((evalp(b,x)-y)**2 for x,y in zip(xs,ys))
        ll=-n/2*math.log(rss/n); k=deg+2
        aic.append(-2*ll+2*k); bic.append(-2*ll+math.log(n)*k)
    print(f"    deg={deg:2d}  AIC={mean(aic):8.2f}  BIC={mean(bic):8.2f}")
```
```
(A) x0=0.3, n=25, sigma^2=0.49, irreducible=0.49
  deg= 1  bias^2=0.00004  variance=0.02637  MSE=0.02640
  deg= 2  bias^2=0.00011  variance=0.04316  MSE=0.04328
  deg= 3  bias^2=0.00004  variance=0.06966  MSE=0.06970
  deg= 5  bias^2=0.00003  variance=0.10601  MSE=0.10603
  deg= 8  bias^2=0.00001  variance=0.19307  MSE=0.19308
  deg=12  bias^2=0.00092  variance=0.73648  MSE=0.73740

(B) in-sample MSE: deg=1 0.2381 -> deg=10 0.1799 (monotone down)
    CV MSE       : deg=1 0.2675 -> deg=10 55.7672
    CV selects degree = 1   (true model is degree 1)

(C) AIC/BIC, true degree 1
    deg= 1  AIC=  -52.82  BIC=  -47.75
    deg= 2  AIC=  -52.09  BIC=  -45.33
    deg= 3  AIC=  -49.60  BIC=  -41.15
    deg= 6  AIC=  -49.33  BIC=  -35.82
    deg=10  AIC=  -46.89  BIC=  -26.62
```

Since the truth is linear, bias² is ~0 for every degree; **all** the U-shape comes from variance, which climbs steeply with degree (0.026 → 0.736) — the shape of overfitting. In-sample error falls monotonically (0.238 → 0.180) while CV error explodes (0.268 → 55.8); CV and both penalised criteria correctly select degree 1. The lesson is blunt: **training error is a liar; only held-out error is honest.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Validating on training data.** In-sample error falls monotonically with complexity and says nothing about generalisation. Never report it as performance.
2. **Screening outside the folds (the #1 silent bug).** Feature selection or variance filtering on the full dataset before CV leaks the test set into training; ESL demonstrates a 3%-vs-50% illusion. Put *every* data-dependent step inside the fold loop.
3. **Reusing the test set for selection.** If you pick the best model by the test error, the test error is no longer an unbiased estimate — it becomes a training signal. Keep a final "vault" set, or use nested CV.
4. **Choosing complexity by AIC when you want consistency.** AIC targets predictive risk and over-selects; BIC is consistent and picks the true model asymptotically. Neither replaces a validation set for non-nested models.
5. **Treating \(\mathrm{df}=\text{number of coefficients}\).** For regularised/smoothed models the effective df is \(\operatorname{tr}(S)\le p\); using \(p\) over-penalises and mis-ranks models.
6. **Ignoring the irreducible floor.** No amount of modelling removes \(\sigma^2_\varepsilon\); chasing below it is fitting noise. Compare models against that floor, not against zero.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *Elements of Statistical Learning*, Ch 2 §2.5–2.6 (bias–variance eqs 2.25/2.46), Ch 7 (test vs training error, the \(2d/N\) optimism, Cp/AIC/BIC eqs 7.24–7.35, effective df §7.6, \(K\)-fold CV eq 7.48, one-standard-error rule, the wrong-vs-right CV §7.10.2, bootstrap §7.11). *Verification report in the corpus.*
- **Casella & Berger**, *Statistical Inference*, Ch 7 (MSE = Var + Bias² is the parameter-level twin of this decomposition).
- **Tsay**, *Analysis of Financial Time Series*, Ch 2 (AIC/BIC eq 2.16 used for ARMA/GARCH order selection).

---

### 6. Connected Graph Bridges

- Back: [[foundations/statistics-and-inference/04-confidence-intervals-and-testing|04 · Testing]] · [[foundations/statistics-and-inference/02-point-estimation|02 · Point Estimation]] · [[foundations/statistics-and-inference/index|Index Hub]]
- Continue: [[foundations/statistics-and-inference/06-advanced-extensions|06 · Advanced Extensions]] (bootstrap validation, .632)
- Applications: [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt-Data]] (regularisation, CV in production) · [[pillars/01-quantitative-research/index|Quantitative Research]] (backtest validation) · [[foundations/econometrics-and-timeseries/index|Econometrics]] (information criteria for model order)
