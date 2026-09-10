---
title: "06 — Advanced Extensions: Purged CV, PBO & the Reality Check"
tags:
  - pillar-quant-research
  - backtesting-hygiene
  - purged-cross-validation
  - leakage
  - probability-of-backtest-overfitting
  - reality-check
  - data-snooping
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/backtesting-hygiene/03-the-multiple-testing-problem|03 · Multiple Testing]] and [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

Three mature tools close the remaining gaps that a single DSR number cannot:

1. **Purged, embargoed $K$-fold cross-validation** — fixes the **leakage** that makes ordinary CV dishonest on financial data.
2. **Probability of Backtest Overfitting (PBO)** via **combinatorially symmetric cross-validation (CSCV)** — a *non-parametric*, statistic-agnostic estimate of how likely your *selection procedure* is to pick a strategy that underperforms out of sample.
3. **White's Reality Check / the bootstrap SPA test** — the founding frequentist test of **data snooping**, which asks whether the *best* model in a whole search beats a benchmark once you account for the search.

The objective: move from "DSR passed" to a *portfolio of independent checks* — parametric (DSR), non-parametric (PBO), and bootstrap-based (Reality Check) — because each fails in a different regime.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Leakage and why ordinary $K$-fold CV is wrong in finance

Standard $K$-fold CV shuffles observations and holds out a random test fold. On i.i.d. data this is unbiased. **Financial observations are neither i.i.d. nor exchangeable in time.** Two failure mechanisms:

- **Overlap / serial correlation.** If a feature or label at $t$ uses a window $[t-h,t+h']$, a randomly chosen test fold shares information with training folds — the model *peeks*. This is why the ESL wrong-vs-right CV demonstration (full-data screening gives CV error $3\%$ against a true $50\%$, §7.10.2) is not a curiosity but the *norm* in finance.
- **Regime/segment boundaries.** Purging by random folds lets the model learn adjacent, correlated observations directly.

**Purging:** remove from the *training* set every observation whose label/factor window overlaps the *test* fold's time span (by $\ge$ the label horizon). **Embargo:** after each test fold, additionally drop a short window (e.g. $1\%$ of $T$ or a fixed number of days) from training to kill residual autocorrelation memory (López de Prado, *Advances in Financial Machine Learning*, Ch 7).

#### 2.2 Probability of Backtest Overfitting (CSCV)

Build the $T\times N$ matrix $M$ of the $N$ trials' performance series (columns = trials, rows = synchronous observations). Partition rows into $S$ (even) equal blocks; take all $\binom{S}{S/2}$ combinations, each half used as IS *and* (its complement) as OOS.
- For each combination $c$: pick the IS-best strategy $n^*$, find its **OOS relative rank** $\bar\omega_c=\bar r_{n^*}/(N+1)\in(0,1)$, and form the logit
$$\lambda_c=\ln\!\frac{\bar\omega_c}{1-\bar\omega_c}.$$
- Collecting $\{\lambda_c\}$ gives an empirical distribution; the **PBO** is the probability the IS-best underperforms the OOS median:
$$\text{PBO}=\Pr[\lambda<0]=\int_{-\infty}^{0} f(\lambda)\,d\lambda.$$
**Interpretation:** $\text{PBO}\to0.5$ means the selection is *no better than random* (the IS winner is coin-flip-ranked OOS); $\text{PBO}\ll0.5$ means IS ranking carries genuine OOS information. PBO is non-parametric and works for any performance statistic (Sharpe, Sortino, drawdown ratio).

#### 2.3 White's Reality Check (bootstrap data-snooping test)

Given $l$ candidate models and a benchmark, let $f_k$ be model $k$'s performance differential vs the benchmark. The null is *no model beats the benchmark*:
$$H_0:\ \max_{k=1,\dots,l}\mathbb{E}[f_k^{\ast}]\le0.$$
The test statistic is $V=\max_k \sqrt{n}\,\bar f_k$. Its null distribution is unknown analytically, so it is bootstrapped (Politis–Romano **stationary bootstrap** — blocks of geometrically-distributed length preserve dependence). With resampled series,
$$V^{\ast}=\max_{k}\ \sqrt{n}\,(\bar f_k^{\ast}-\bar f_k),$$
and the **Reality Check $p$-value** is the fraction of bootstrap draws with $V^{\ast}\ge V$. A small $p$ means the best model's edge survives the search; a large $p$ means it is a data-snooping artifact. **SPA** (Hansen 2005) sharpens this by recentring the dominated models.

---

### 3. Computational Implementation — PBO via CSCV, and leakage intuition

Stdlib only. We build a $T\times N$ trial matrix, run CSCV ($S{=}10$), and report PBO for (a) *all-noise* strategies and (b) *one genuinely-skilled* strategy among noise. PBO should land near $0.5$ in (a) and well below it in (b).

```python
import math, random
from itertools import combinations

def sharpe(xs):
    n=len(xs); m=sum(xs)/n; v=sum((x-m)**2 for x in xs)/(n-1)
    return m/math.sqrt(v) if v>0 else 0.0

def pbo_cscv(M, S):
    T=len(M); N=len(M[0]); sub=T//S
    blocks=[[M[r] for r in range(s*sub,(s+1)*sub)] for s in range(S)]
    logits=[]; below=0
    for c in combinations(range(S), S//2):
        train=[blocks[s] for s in c]; test=[blocks[s] for s in range(S) if s not in c]
        def col_stats(part):
            rows=[row for block in part for row in block]
            return [sharpe([row[n] for row in rows]) for n in range(N)]
        rIS=col_stats(train); rOOS=col_stats(test)
        best=max(range(N), key=lambda n: rIS[n])                 # chosen in-sample
        rank=1+sum(1 for n in range(N) if rOOS[n] < rOOS[best])  # OOS rank
        w=rank/(N+1); lam=math.log(w/(1-w)); logits.append(lam)
        if lam < 0: below+=1
    return below/len(logits), len(logits)

random.seed(11); T=1200; N=50; S=10
noise=[[random.gauss(0,0.01) for _ in range(N)] for _ in range(T)]
pbo1, ncomb = pbo_cscv(noise, S)
print(f"all-noise strategies: PBO = {pbo1:.3f}  ({ncomb} combinations, S={S}, N={N})")

skilled=[[random.gauss(0,0.01) for _ in range(N)] for _ in range(T)]
for t in range(T): skilled[t][0] += 0.0009      # strategy #0 has genuine skill
pbo2,_ = pbo_cscv(skilled, S)
print(f"one real strategy among noise: PBO = {pbo2:.3f}")
```
```
all-noise strategies: PBO = 0.504  (252 combinations, S=10, N=50)
one real strategy among noise: PBO = 0.127
```
The reading: when **nothing** is real, the IS-best is OOS-median on average — PBO $\approx0.50$, the perfect signature of a search that is pure noise. When **one** strategy truly has edge, the IS-best tends to *be* that strategy and it ranks well OOS — PBO drops to $\approx0.13$, well below the $0.5$ threshold. **Decision rule: PBO $>0.5$ or near it condemns the selection process; PBO well below $0.5$ is positive evidence — but PBO and DSR can disagree, which is why you run both.**

*(Leakage note: the same matrix fed to standard $K$-fold CV — random folds — would leak via serial correlation and report a spuriously good "OOS" score; CSCV avoids this by keeping blocks contiguous and alternating IS/OOS in time, the CV analogue of purging/embargo.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Random-fold CV on time series.** Shuffling breaks the temporal structure; leakage makes CV error optimistic in finite samples (ESL §7.10.2–7.10.3: high-dimensional/irrelevant features make CV *underestimate* error unless the model is retrained per fold). Use **purged + embargoed** folds.
2. **Purge width guessed.** The purge must span the **label horizon** (how far forward a label looks). Too narrow → leakage; too wide → discard most data. Tie it to the triple-barrier/label construction.
3. **Embargo omitted.** Even after purging, residual serial correlation crosses the fold boundary; a short embargo window is cheap insurance (López de Prado Ch 7).
4. **PBO mis-read as a significance test.** PBO estimates the *selection procedure's* reliability, not a strategy's alpha. PBO $\approx0.5$ does **not** prove your best strategy is fake; it says your *ranking* is uninformative — a much more specific indictment.
5. **CSCV assumptions.** PBO requires a synchronous, rectangular matrix and a metric estimable on subsamples; unevenly-sampled or short series break it (aggregate to a common index).
6. **Reality Check on the wrong null.** The RC null is *no model beats the benchmark*; testing against a wrong benchmark, or bootstrapping without preserving dependence (plain i.i.d. bootstrap on serially-correlated data), invalidates the $p$-value. Use a stationary/block bootstrap.
7. **Correlated strategies over-count in PBO.** CSCV uses ranks among $N$ columns; if columns are near-duplicates the effective diversity is smaller and PBO is optimistic — pre-cluster near-identical trials.

---

### 5. Canonical Literature & Study References

- **Bailey, D., Borwein, J., López de Prado, M. & Zhu, J.**: *The Probability of Backtest Overfitting*, Journal of Computational Finance 20(4) (2017) — the PBO definition and Algorithm 2.3 (CSCV). *The source for §2.2 and §3.*
- **White, H.**: *A Reality Check for Data Snooping*, Econometrica 68(5), 1097–1126 (2000) — the null $\max_k\mathbb{E}[f_k^{\ast}]\le0$, the statistic $V_l$, and the stationary-bootstrap $p$-value. *The source for §2.3.*
- **Hansen, P. R.**: *A Test for Superior Predictive Ability*, Journal of Business & Economic Statistics (2005) — the SPA refinement of the Reality Check.
- **López de Prado, M.**: *Advances in Financial Machine Learning*, Ch 7 (purged $K$-fold CV, embargo, the interplay of overlapping labels with CV) — the leakage fix. *Companion to the Atlas's [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]].*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed.), §7.10.2–7.10.3 and eq. 7.48 — $K$-fold CV mechanics and its failure under feature screening/high dimension.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Index Hub]]
- Cross-cutting: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (label horizons define the purge) · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] (state-space models need the same CV discipline)
- Cross-pillar: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] (purged CV, meta-labeling, and the low signal-to-noise regime)
