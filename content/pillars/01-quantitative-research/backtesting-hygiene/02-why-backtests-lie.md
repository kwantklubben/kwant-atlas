---
title: "02 — Why Backtests Lie: Selection Bias, Optimism & the Is/OOS Gap"
tags:
  - pillar-quant-research
  - backtesting-hygiene
  - selection-bias
  - in-sample-optimism
  - performance-degradation
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/backtesting-hygiene/01-from-zero-intuition|01 · From Zero]] (a backtest is a search) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (expectation, bias–variance).

---

### 1. Intuition & Practical Objective

Every good-looking backtest lies through one of **three distinct doors**, and hygiene means closing all three:

1. **Selection bias** — you report the winner of a search and hide the losers. (Multiple testing; the subject of [[pillars/01-quantitative-research/backtesting-hygiene/03-the-multiple-testing-problem|03]] and [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04]].)
2. **In-sample optimism** — you measured performance *on the data you tuned to*. Even a single fitted model reports an optimistically biased error (Hastie et al., ESL Ch 7).
3. **Contamination of the sample itself** — look-ahead (using information not yet available), survivorship (today's constituents), and backfill/self-selection (only successful track records published).

The practical objective: recognise which door a given number came through, so you know exactly *how* it overstates and by roughly how much.

The cleanest field evidence is the **in-sample / out-of-sample gap**. A rule optimised on 500 days of a pure random walk wins an in-sample Sharpe of $\approx1.3$ and then delivers $\approx0$ out of sample — because on a random walk there is no rule; only the search exists.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 In-sample optimism (ESL Ch 7)

For a fitted model, training error is systematically *below* test error. ESL quantify the gap for linear models:

- **Bias–variance decomposition** (ESL eq. 7.9): $\mathbb{E}[(Y-\hat f)^2]=\sigma_\varepsilon^2+\mathrm{Bias}^2+\mathrm{Var}$ — the irreducible $\sigma_\varepsilon^2$ cannot be fitted away.
- **In-sample variance of the fit** (ESL eq. 7.12): $\mathrm{Var}$ in sample scales as $\dfrac{p}{N}\sigma_\varepsilon^2$ with $p$ effective parameters and $N$ observations.
- **Optimism of the training error** (ESL §7.4, eq. 7.24): for a model with $d$ inputs/$d$ degrees of freedom,
$$\mathbb{E}[\text{Err}_{\text{in}}]\approx \mathbb{E}[\text{Err}_{\text{out}}]-\frac{2d}{N}\sigma_\varepsilon^2,$$
- **Effective degrees of freedom** for a linear smoother $\hat y=Sy$ is $df=\mathrm{tr}(S)$ (ESL eq. 7.32) — this is the honest "$d$" to count, not the nominal parameter count.

**Translation to finance:** every free knob (lookback, threshold, stop, universe, weighting) raises $d$ and quietly *lowers* the reported in-sample error. A backtest Sharpe computed in sample is $\text{Err}_{\text{in}}$, i.e. it is biased optimistic by roughly $2d/N$ in variance units.

#### 2.2 The IS → OOS gap and performance degradation

Let $\widehat{SR}^{\text{IS}}$ be the selected strategy's in-sample Sharpe and $\widehat{SR}^{\text{OOS}}$ its Sharpe on unseen data. Define the **performance degradation** $\Delta=\widehat{SR}^{\text{OOS}}-\widehat{SR}^{\text{IS}}\le0$ typically. The magnitude of $\Delta$ is driven by how much freedom the search had relative to the sample length: $\Delta \downarrow$ as the trial-space grows and $T$ shrinks.

**Memory effects make it worse than "zero".** In an i.i.d. (memoryless) series a spurious pattern is merely *diluted* out of sample. In a series with **memory** (mean reversion, autocorrelation), a rule fitted to the extreme in-sample pattern must be *undone* when the process reverts — so the overfit rule does not earn zero, it earns **negative** returns systematically. Bailey, Borwein, López de Prado & Zhu (2014) prove that under memory effects backtest overfitting becomes **loss maximization**, not merely neutral. Most financial series are neither i.i.d. nor trendless, so the realistic sign of $\Delta$ is negative.

#### 2.3 The three-door taxonomy (what each looks like numerically)

| Door | Mechanism | In-sample symptom | Fix |
|---|---|---|---|
| Selection bias | Reported = max of $N$ trials | "Best" beats all others; $N$ undisclosed | DSR / haircut (pages 03–04) |
| In-sample optimism | Tuned on the scored data | $d$ free params raise apparent fit | Hold out + effective $df=\mathrm{tr}(S)$ |
| Look-ahead | Uses future info | Unrealistically smooth equity curve | Point-in-time data, lag by publish date |
| Survivorship | Only survivors measured | Universe biased to winners | Point-in-time universe, include delistings |
| Backfill / self-selection | Only winners disclosed | Too-good-to-be-true track records | Demand full trial history |

---

### 3. Computational Implementation — the IS/OOS collapse

A backtest on a **pure random walk** (zero drift, no memory, by construction *no signal*). We search a grid of 72 moving-average-crossover strategies (fast $\times$ slow $\times$ direction), pick the in-sample best, and score it out of sample. Stdlib only.

```python
import random, math

def sharpe(xs, ann=252.0):
    n=len(xs); m=sum(xs)/n; v=sum((x-m)**2 for x in xs)/(n-1)
    return (m/math.sqrt(v))*math.sqrt(ann) if v>0 else 0.0

def backtest(prices, fast, slow, flip):
    pnl=[]; ma_f=sum(prices[:fast])/fast; ma_s=sum(prices[:slow])/slow
    for t in range(slow, len(prices)):
        sig = 1.0 if ma_f>ma_s else -1.0
        if flip: sig=-sig
        pnl.append(sig*(prices[t]-prices[t-1])/prices[t-1])
        ma_f += (prices[t]-prices[t-fast])/fast
        ma_s += (prices[t]-prices[t-slow])/slow
    return sharpe(pnl)

def one_search(T=1000, reps=400):
    grid=[(f,s,fl) for f in (2,3,5,8,12,20) for s in (25,30,40,60,80,120) for fl in (False,True)]
    random.seed(5); is_best=[]; oos_best=[]
    for _ in range(reps):
        p=[100.0]
        for _ in range(T):
            p.append(p[-1]*(1.0+random.gauss(0,0.01)))     # pure random walk, zero drift
        half=T//2; isp=p[:half+1]; oosp=p[half:]
        scores=[backtest(isp,f,s,fl) for (f,s,fl) in grid]
        b=max(range(len(grid)),key=lambda i:scores[i])
        is_best.append(scores[b]); oos_best.append(backtest(oosp,*grid[b]))
    n=len(is_best)
    return sum(is_best)/n, sum(oos_best)/n

ib, ob = one_search()
print(f"grid = 72 MA-crossover strategies, IS=500d, OOS=500d, 400 searches")
print(f"mean IN-SAMPLE  Sharpe of chosen strategy = {ib:+.2f}")
print(f"mean OUT-OF-SAMPLE Sharpe of SAME strategy = {ob:+.2f}")
```
```
grid = 72 MA-crossover strategies, IS=500d, OOS=500d, 400 searches
mean IN-SAMPLE  Sharpe of chosen strategy = +1.33
mean OUT-OF-SAMPLE Sharpe of SAME strategy = -0.01
```
The searched rule looks like a **Sharpe 1.3 strategy in sample** and is worth **exactly nothing** out of sample. Nothing decayed and nothing broke: the data was a random walk, so the in-sample edge was the *height of the maximum of 72 noisy draws* (compare [[pillars/01-quantitative-research/backtesting-hygiene/03-the-multiple-testing-problem|03]]). This is the mechanism behind the "common practice of discounting reported Sharpe ratios by 50%" (Harvey & Liu 2015) — except the discount is **non-linear**, not a flat half.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tuning on the test set.** Any parameter chosen using the test window converts it into a training window. Repeated holdout use makes 5% false positives *expected* after ~20 applications (Bailey & López de Prado §"holdout").
2. **Ex-post universe construction.** "I backtested the S&P 500" using *today's* members imports survivorship: firms that were delisted or acquired are missing, and membership required success.
3. **Look-ahead leakage via stale vintages.** Using restated fundamentals, index membership known only later, or a data vendor's *current* adjusted prices, silently hands the strategy future information.
4. **Ignoring effective $df$.** Counting named parameters but not the implicit degrees of freedom of a search (a grid of 72 crossovers is 72 $d$'s) understates optimism.
5. **Assuming $\Delta\approx0$.** In mean-reverting markets the OOS Sharpe of an overfit rule is **negative**, so "past performance does not guarantee future results" is too lenient — adverse outcomes are likely (B&LdP §conclusion).
6. **Confusing selection bias with model error.** A low OOS Sharpe can mean (a) the strategy is a fluke, or (b) execution costs were mis-modelled. Hygiene analyses both; the fix differs.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed.), Ch 7 §7.1–7.4 (training vs test error, bias–variance eq. 7.9, in-sample variance eq. 7.12, optimism eq. 7.24, effective $df$ eq. 7.32) and §7.10.2–7.10.3 (the wrong-vs-right CV example: full-data screening yields CV error $3\%$ against a true $50\%$). *Math-verified in the corpus.*
- **Bailey, D. H. & López de Prado, M.**: *The Deflated Sharpe Ratio* (2014), §"Backtest overfitting under memory effects" and §"Backtest overfitting and the holdout method".
- **Bailey, Borwein, López de Prado & Zhu**: *Pseudo-Mathematics and Financial Charlatanism* (Notices of the AMS, 2014) — the formal "overfitting ⇒ loss maximization under memory" result.
- **Harvey, C. R. & Liu, Y.**: *Backtesting*, JPM (2015) — the origin of the "50% haircut" folklore and its critique.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/backtesting-hygiene/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/backtesting-hygiene/03-the-multiple-testing-problem|03 · Multiple Testing]] → [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04 · Deflated Sharpe]] → [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|05 · Failure Modes]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · Sibling: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]]
