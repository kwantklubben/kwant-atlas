---
title: "Purged Cross-Validation & Backtest Hygiene: Topic Hub"
tags:
  - pillar-machine-learning
  - purged-cross-validation
  - backtest-hygiene
  - cpcv
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (the Deflated Sharpe Ratio, PBO (*probability of backtest overfitting*), multiple testing). Comfort with [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (interval labels) is what makes the purge meaningful. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Every ML evaluation in finance is an act of **leakage control**. A standard $k$-fold cross-validation (CV) splits an IID dataset into train and test and shuffles so that "no observation leaks into another set." But financial observations are **not IID**: features are serially correlated ($X_t \approx X_{t+1}$) and, because labels are formed over *overlapping* forward windows (e.g., "sign of the next $h$-bar return"), adjacent labels are near-duplicates ($Y_t \approx Y_{t+1}$). Put $t$ in the training set and $t+1$ in the test set and you have just told the model the answer.

This folder is the topic-hub for **purged cross-validation and backtest hygiene** in Kwant-Atlas, the companion to the *classical* backtesting-hygiene folder (multiple testing, DSR) but for the **ML pipeline**. It (a) gives the **fast formula/decision lookup** below — job #1 of a hub — and (b) routes you to six sub-pages that go from raw intuition through the two leak-removal tools (**purging**, **embargoing**), their combinatorial generalization (**CPCV**), and the failure modes and practice.

> **The one-sentence essence.** "Standard $k$-fold CV measures skill plus *leaked duplicate labels*; purging drops every training observation whose label window overlaps the test set, an embargo drops the serially-correlated stragglers right after it, and Combinatorial Purged CV (CPCV) repeats the honest split across *every* test-set combination to yield a *distribution* of backtest paths instead of one fragile number."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: label of observation $i$ spans the closed bar interval $[t_{i,0},\,t_{i,1}]$; test block spans $[t_{j,0},\,t_{j,1}]$; $T$ = number of observations, $N$ = number of contiguous groups, $k$ = number of groups in the test set, $h$ = embargo length in bars, $\varphi$ = number of backtest paths. **All checks below were re-executed and reproduced exactly (see §3).**

| Quantity | Formula | Verified check |
|---|---|---|
| **Purge condition** (drop train $i$ if label overlaps test $j$ — any of 3) | $t_{j,0}\!\le t_{i,0}\!\le t_{j,1}$ · $t_{j,0}\!\le t_{i,1}\!\le t_{j,1}$ · $t_{i,0}\!\le t_{j,0}\le t_{j,1}\le t_{i,1}$ | all three = overlap $\Rightarrow$ purge |
| **Embargo** (kill post-test serial memory) | re-label test as $Y_j=f\big[t_{j,0},\,t_{j,1}+h\big]$, then purge; $h\approx 0.01\,T$ suffices | $h{=}10,\,T{=}1000\Rightarrow 1\%$ |
| Number of train/test **splits** (test $=k$ of $N$ groups) | $\displaystyle\binom{N}{k}=\prod_{i=0}^{k-1}\frac{N-i}{k!}$ | $N{=}6,k{=}2\Rightarrow 15$ |
| **Number of backtest paths** | $\displaystyle\varphi[N,k]=\frac{k}{N}\binom{N}{k}=\prod_{i=1}^{k-1}\frac{N-i}{(k-1)!}$ | $\varphi[6,2]{=}5$; $\varphi[6,3]{=}10$; $\varphi[101,2]{=}100$ |
| Fraction of data used for training per combination | $\theta=1-k/N$ | $N{=}10,k{=}2\Rightarrow 0.80$ |
| Max paths (limit) | $N{=}T,\;k{=}N/2$ $\Rightarrow \varphi=\tfrac12\binom{T}{T/2}$ | $N{=}30\Rightarrow\varphi{=}77\,558\,760$ |
| **CPCV variance of sample-mean Sharpe** | $\sigma^2[\mu_i]=\varphi^{-1}\sigma_i^2\big[1+(\varphi-1)\bar\rho_i\big]$ | $\sigma^2_i{=}1,\bar\rho{=}0.3:\ \varphi{=}1\Rightarrow1.0$, $\varphi{=}100\Rightarrow0.3070$ |

> **Critical caveat (AFML §12.4.3).** There is a strict budget: more paths $\varphi$ requires either more groups $N$ (smaller group granularity) or a bigger test fraction $k/N$ — and the latter *shrinks the training data* ($\theta=1-k/N$). The practical sweet spot is $k=2$ with $N=\varphi+1$, which trains on $\theta=1-2/N$ of the data while still yielding $N-1$ paths. Pushing to $k=N/2$ maximizes $\varphi$ but trains each classifier on only half the sample.

---

### 3. Computational Implementation — the hygiene engine

Standard-library only. This reproduces the two headline numbers in §2: the **leakage signature** (accuracy inflates with the number of folds on a *pure-noise* feature) and the **CPCV path counter**.

```python
import random, math

# ---- (1) LEAKAGE from overlapping labels (AFML 7.3) ----
# Pure-noise target: y_t = sign of the next h-bar return (overlapping windows).
# A "learner" that copies the nearest training label in TIME will score high
# under standard k-fold because adjacent labels are near-duplicates.
def labels(T, h, seed=0):
    rnd = random.Random(seed)
    r = [rnd.gauss(0, 1) for _ in range(T + h + 1)]
    y = [-1]*T
    for t in range(T - h + 1):
        y[t] = 1 if sum(r[t+1:t+1+h]) > 0 else 0
    return y

def nn_time_acc(train_idx, test_idx, y):
    ok = tot = 0
    for t in test_idx:
        if y[t] < 0: continue
        s = min(train_idx, key=lambda q: abs(q - t))
        ok += (y[s] == y[t]); tot += 1
    return ok/tot if tot else float('nan')

T, h = 2400, 10
y = labels(T, h, seed=3); N = T - h + 1
agree = sum(y[t]==y[t+1] for t in range(N-1) if y[t]>=0 and y[t+1]>=0)
agree /= sum(1 for t in range(N-1) if y[t]>=0 and y[t+1]>=0)
print(f"P(Y_t==Y_t+1) for overlapping h=10 labels = {agree:.3f}")
for block in (N//5, 20, 1):                      # thick -> thin (LOO-like) folds
    k = math.ceil(N/block); al, ap = [], []
    for i in range(k):
        t0 = i*block; t1 = min((i+1)*block, N)
        test = list(range(t0, t1)); B = (t1-1) + h - 1
        trn_std = [s for s in range(N) if not (t0 <= s < t1)]
        trn_pur = [s for s in trn_std if not (s <= B and s + h - 1 >= t0)]
        al.append(nn_time_acc(trn_std, test, y)); ap.append(nn_time_acc(trn_pur, test, y))
    print(f"  fold-block~{block:4d}: STANDARD k-fold acc={sum(al)/k:.3f} | PURGED acc={sum(ap)/k:.3f}")

# ---- (2) CPCV path counter (AFML 12.4.1) ----
def cpcv_paths(N, k):
    p = 1
    for i in range(1, k): p *= (N - i)
    return p // math.factorial(k - 1)
print("\nCPCV paths:  phi[6,2]=", cpcv_paths(6,2), " phi[6,3]=", cpcv_paths(6,3),
      " phi[101,2]=", cpcv_paths(101,2))
```
```
P(Y_t==Y_t+1) for overlapping h=10 labels = 0.854
  fold-block~ 478: STANDARD k-fold acc=0.451 | PURGED acc=0.426
  fold-block~  20: STANDARD k-fold acc=0.658 | PURGED acc=0.509
  fold-block~   1: STANDARD k-fold acc=0.854 | PURGED acc=0.519

CPCV paths:  phi[6,2]= 5  phi[6,3]= 10  phi[101,2]= 100
```

Read it as the punchline of the whole folder: on **pure noise**, thinning the folds from block-$\sim\!478$ to leave-one-out drives standard CV accuracy from $0.45$ to $0.85$ — a textbook "false discovery" manufactured purely by leaked overlapping labels. Purging pins every configuration at $\approx0.5$. The same classifier sees *no* signal.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the practice checklist lives in [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Look-ahead (label) leakage** — overlapping label windows make adjacent train/test samples near-duplicates; standard CV reads the answer back ($\S$02).
2. **Purging is not free** — dropping overlapping training rows shrinks the sample, and the loss grows with the label horizon (up to $11\%$ at $h=50$); a real bias–variance tradeoff ($\S$05).
3. **One path = one lottery ticket** — walk-forward and CV each produce a *single* backtest, so their Sharpe is a high-variance draw; CPCV replaces it with a distribution ($\S$04).
4. **The missing $N$ again** — a purged CV that is run a thousand times still suffers selection bias; pair it with the Deflated Sharpe Ratio ([[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).

---

### 5. Canonical Literature & Study References

- **López de Prado, Marcos**: *Advances in Financial Machine Learning* (Wiley, 2018) — **Ch. 7 "Cross-Validation in Finance"** (purging, embargo, PurgedKFold, sklearn bugs) and **Ch. 12 "Backtesting Through Cross-Validation"** (§12.4 CPCV: splits, $\varphi[N,k]$; §12.5 the variance formula). *The formula-authoritative source; every formula in this folder is transcribed from it and numerically reproduced.*
- **Bailey, Borwein, López de Prado & Zhu**: *The Probability of Backtest Overfitting*, J. Computational Finance 20(4) (2017) — CSCV and the PBO measure (see sibling hub).
- **Bailey & López de Prado**: *The Deflated Sharpe Ratio*, J. Portfolio Management 40(5) (2014) — corrects reported Sharpe for trials $N$ and non-normality.
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009) — **Ch. 7** (model assessment: $k$-fold CV eq. 7.48, the *wrong-vs-right* CV §7.10.2 where full-data screening yields 3% vs true 50%). *Math-verified in the corpus.*
- **"Backtest Overfitting in the Machine Learning Era"** (Expert Systems with Applications, 2025) — controlled comparison of walk-forward vs. purged vs. adaptive CPCV on synthetic non-stationary data.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (classical: DSR, PBO, multiple testing)
- Sibling (same pillar): [[pillars/07-machine-learning-altdata/tree-based-factor-ranking-and-purged-cv|Tree-Based Factor Ranking & Purged CV]] (purging applied to LightGBM/XGBoost MDA) · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
- Labels that need purging: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (triple-barrier & interval labels)
- Sub-pages (in-folder): 01 From Zero · 02 Why Standard CV Fails · 03 Purging & Embargo · 04 Combinatorial Purged CV · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/01-from-zero-intuition|01 · From Zero]] — no prior stats needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/02-why-standard-cv-fails|02 · Why Standard CV Fails]] → [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/03-purging-and-embargo|03 · Purging & Embargo]] → [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/04-combinatorial-purged-cv|04 · Combinatorial Purged CV]].
- **Robustness (practitioner/graduate):** [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/07-machine-learning-altdata/tree-based-factor-ranking-and-purged-cv|Purged CV on Trees]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Deflated Sharpe & PBO]]
