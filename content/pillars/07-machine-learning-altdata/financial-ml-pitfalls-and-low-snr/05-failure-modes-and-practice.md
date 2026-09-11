---
title: "7.1.5 Failure Modes & Real-World Practice"
tags:
  - pillar-machine-learning
  - financial-ml-pitfalls-and-low-snr
  - failure-modes
  - data-leakage
  - selection-bias
  - survivorship-bias
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/04-non-stationarity-and-samples|04 · Non-Stationarity & Samples]].

---

### 1. Intuition & Practical Objective

The pillar's entire message compresses into one discipline: **most financial-ML "discoveries" are false positives.** This page names the failure modes precisely, ties each to a first principle, and — where possible — *measures* how big the fraud is. The objective is not cynicism; it is the muscle of knowing which numbers to trust.

The failure modes, in one line each:

1. **Overfitting with few effective samples** — flexible model + tiny $N_{\text{eff}}$ = memorizing noise ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/01-from-zero-intuition|01]], [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03]]).
2. **Random / leaky cross-validation** — IID CV on non-IID, overlapping-label data inflates the score ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/02-why-finance-is-different|02]]).
3. **Look-ahead (point-in-time) bias** — using information that was not available at the timestamp (reported earnings used at the open; today's constituents backtested into the past).
4. **Survivorship bias** — backtesting only today's S&P 500 constituents excludes the Enrons and Lehmans that died along the way.
5. **Selection bias / multiple testing** — the best of $N$ tried strategies looks great by pure chance (expected max Sharpe $\approx\sqrt{2\ln N}$).

> **The one-line takeaway.** "Ask yourself, *in what way am I overfitting?* — overfitting is not a tuning nuisance, it is the industry's default mode of operation and, when done knowingly, outright fraud (López de Prado)."

---

### 2. Mathematical Ground Truth & Derivations

**Wrong-vs-right CV (ESL §7.10.2).** If features are *screened on the full dataset* (e.g., pick the most correlated features using all rows, then cross-validate), the test fold's information has already leaked into the feature choice. ESL's canonical demo — 50 samples, 1000 irrelevant predictors, true $R^2=0$ — shows the leaky procedure reporting an average CV error of $3\%$ while the honest (screen-inside-each-fold) procedure reports the true $\sim50\%$. Screening must happen inside each training fold only.

**Selection bias / multiple testing (Bailey & López de Prado 2014).** If you try $N$ skill-less strategies and keep the best, its *in-sample* Sharpe ratio is not $0$; it is (asymptotically, for IID Normal returns) the expected maximum of $N$ standard Normals,

$$
\mathbb{E}\!\left[\max_{i=1..N}\mathrm{SR}_i\right]\approx\sqrt{2\ln N},
$$

in annualized units scaled by the track length. To prevent skill-less strategies from showing an in-sample Sharpe of $\mathrm{SR}_{\text{IS}}$, you need a **Minimum Backtest Length**

$$
y\ge\frac{2\ln N}{\mathrm{SR}_{\text{IS}}^2}\ \text{years}.
$$

The simple bound $y\ge2\ln N/\mathrm{SR}_{\text{IS}}^2$ is conservative: for $N=45$, $\mathrm{SR}_{\text{IS}}=1$ it demands $\approx7.6$ years. The *exact* Bailey Minimum-Backtest-Length $y=(E[\max_N Z])^2/\mathrm{SR}_{\text{IS}}^2$ with $E[\max_N Z]=(1-\gamma)\Phi^{-1}(1-1/N)+\gamma\Phi^{-1}(1-1/(Ne))$ is sharper — $N=45$ gives $E[\max]=2.235\Rightarrow y=5.0$ years (and $N=7\Rightarrow1.92$ yr, matching the paper's two-year example). So the same bookkeeping says: over a 5-year backtest, no more than $\approx45$ independent configurations should be tried (the corpus-verified Bailey figure: "if only five years of data are available, no more than forty-five independent model configurations should be tried").

---

### 3. Computational Implementation — two failure modes, measured

**Experiment A — wrong-vs-right CV (ESL 7.10.2).** On 50 samples × 1000 irrelevant features (true $R^2=0$), screening on the full data vs screening inside each fold.

**Experiment B — selection bias.** Try $N=200$ pure-noise strategies (each one year of random returns), keep the best, and see its in-sample Sharpe.

```python
import math, random
from numpy.random import default_rng

def fit_predict(Xtr, ytr, Xte):
    p = len(Xtr[0]); X = [[1.0]+list(r) for r in Xtr]
    G = [[0.0]*(p+1) for _ in range(p+1)]; b = [0.0]*(p+1)
    for r, t in zip(X, ytr):
        for i in range(p+1):
            for j in range(p+1): G[i][j] += r[i]*r[j]
            b[i] += r[i]*t
    A = [row[:] for row in G]; bb = b[:]
    for col in range(p+1):
        piv = max(range(col, p+1), key=lambda r: abs(A[r][col]))
        A[col], A[piv] = A[piv], A[col]; bb[col], bb[piv] = bb[piv], bb[col]
        for r in range(col+1, p+1):
            f = A[r][col]/A[col][col]
            for c in range(col, p+1): A[r][c] -= f*A[col][c]
            bb[r] -= f*bb[col]
    coef = [0.0]*(p+1)
    for r in range(p, -1, -1):
        coef[r] = (bb[r]-sum(A[r][c]*coef[c] for c in range(r+1, p+1)))/A[r][r]
    return [coef[0]+sum(c*x for c, x in zip(coef[1:], row)) for row in Xte]

def r2(y, yh):
    ym = sum(y)/len(y); ss = sum((t-ym)**2 for t in y)
    return 1.0 - sum((t-p)**2 for t, p in zip(y, yh))/ss

def cv_5fold(X, y, seed):
    idx = list(range(len(y))); random.Random(seed).shuffle(idx); sc = []
    for fi in range(5):
        te = idx[fi::5]; tr = [i for k in range(5) if k != fi for i in idx[k::5]]
        yh = fit_predict([X[i] for i in tr], [y[i] for i in tr], [X[i] for i in te])
        sc.append(r2([y[i] for i in te], yh))
    return sum(sc)/len(sc)

rng = default_rng(0)
Nn, P = 50, 1000
X = rng.standard_normal((Nn, P)); y = rng.standard_normal(Nn)   # true R^2 = 0
corr = [abs(float(sum((X[:,j]-X[:,j].mean())*(y-y.mean())))/   # |corr(feature,y)|
          ((sum((X[:,j]-X[:,j].mean())**2)**0.5)*(sum((y-y.mean())**2)**0.5))) for j in range(P)]
top = sorted(range(P), key=lambda j: corr[j], reverse=True)[:10]
wrong = cv_5fold(X[:, top].tolist(), list(y), 1)

right = []
idx = list(range(Nn)); random.Random(2).shuffle(idx)
for fi in range(5):
    te = idx[fi::5]; tr = [i for k in range(5) if k != fi for i in idx[k::5]]
    Xtr, ytr = X[tr], y[tr]
    c = [abs(float(sum((Xtr[:,j]-Xtr[:,j].mean())*(ytr-ytr.mean())))/
          ((sum((Xtr[:,j]-Xtr[:,j].mean())**2)**0.5)*(sum((ytr-ytr.mean())**2)**0.5))) for j in range(P)]
    top2 = sorted(range(P), key=lambda j: c[j], reverse=True)[:10]
    yh = fit_predict(Xtr[:, top2].tolist(), ytr.tolist(), X[te][:, top2].tolist())
    right.append(r2(y[te].tolist(), yh))
print("ESL 7.10.2 wrong-vs-right CV on 50 samples x 1000 irrelevant features (true R^2=0):")
print(f"  WRONG (screen on full data): CV R^2 = {wrong:.4f}   (spurious!)")
print(f"  RIGHT (screen inside folds): CV R^2 = {sum(right)/5:.4f}   (honest)")

random.seed(123)                              # fix the global generator for reproducibility
Ntr, T = 200, 252
sr = []
for s in range(Ntr):
    rets = [random.gauss(0, 1) for _ in range(T)]
    m = sum(rets)/T; sd = (sum((v-m)**2 for v in rets)/(T-1))**0.5
    sr.append(m/sd*math.sqrt(T))
best = max(sr); emax = math.sqrt(2*math.log(Ntr))
print("\nSelection bias: N=200 pure-noise strategies (true Sharpe=0), each from 1yr of returns:")
print(f"  best in-sample annualized Sharpe = {best:.3f}   (expected max ~ sqrt(2 ln N) = {emax:.3f})")
print(f"  of the 200, {sum(1 for s in sr if s>1.0)} had SR>1.0 by pure chance")
```
```
ESL 7.10.2 wrong-vs-right CV on 50 samples x 1000 irrelevant features (true R^2=0):
  WRONG (screen on full data): CV R^2 = 0.0474   (spurious!)
  RIGHT (screen inside folds): CV R^2 = -0.8851   (honest)

Selection bias: N=200 pure-noise strategies (true Sharpe=0), each from 1yr of returns:
  best in-sample annualized Sharpe = 2.727   (expected max ~ sqrt(2 ln N) = 3.255)
  of the 200, 40 had SR>1.0 by pure chance
```
Experiment A reproduces the ESL wrong-vs-right lesson in $R^2$ units: leaky screening reports a spurious $+0.047$ (looks predictive on pure noise) while honest screening shows the model is worthless ($-0.89$). Experiment B is the selection-bias killer: of **200 pure-noise strategies**, the best shows an in-sample annualized Sharpe of **2.73** — and **40** of the 200 look "good" (SR>1) by pure chance. **If you tried 200 strategies and are pitching the best one, its Sharpe is most likely this artifact, not skill.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Leaky cross-validation / screening.** Screening features or scaling on the full dataset before splitting leaks the test fold (ESL §7.10.2; AFML Ch. 7). Fix: preprocessing and feature selection *inside each training fold only*.
2. **Look-ahead (point-in-time) bias.** Using data at a timestamp before it was actually available (a 10-Q filed at 16:30 used at 09:30; today's index constituents backtested to 2005). The fix is strict point-in-time (PIT) datasets — see [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alt-Data Pipelines & Evaluation]].
3. **Survivorship bias.** A universe filtered to today's S&P 500 drops Enron, Lehman, WorldCom — the very names that reveal a model's flaws. Backtest on point-in-time constituent lists.
4. **Selection bias / multiple testing.** Tuning over $N$ configurations inflates the best in-sample Sharpe to $\approx\sqrt{2\ln N}$ (Experiment B). Report $N$ and use the Deflated Sharpe ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/06-advanced-extensions|06]]).
5. **The "Sisyphus paradigm" (AFML Ch. 1).** Demanding every quant independently produce a strategy in six months guarantees each settles for an overfit backtest or crowded factor investing. The cure is the team-based *meta-strategy paradigm*, not more solo searching.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, Ch 1 (the Sisyphus vs meta-strategy paradigms; "Overfitting is unethical"), Ch 7 (why K-fold CV fails; purged/embargoed CV), Ch 11 (dangers of backtesting), Ch 14 (probabilistic & deflated Sharpe).
- **Bailey, David H. & López de Prado, Marcos**, "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance," *Notices of the AMS* 61(5), 2014 — MinBTL and the expected-max-Sharpe formalization. *Corpus PDF read.*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 7 §7.10.2 (the wrong-vs-right CV warning). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/04-non-stationarity-and-samples|04 · Non-Stationarity & Samples]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling solutions: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Purged & Embargoed CV]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alt-Data Pipelines (point-in-time hygiene)]]
