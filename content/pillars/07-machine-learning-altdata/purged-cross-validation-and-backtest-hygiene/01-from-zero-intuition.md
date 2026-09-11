---
title: "7.2.1 Purged CV & Backtest Hygiene from Zero"
tags:
  - pillar-machine-learning
  - purged-cross-validation
  - intuition
  - leakage
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]. Everything else is built from scratch on this page.

---

### 1. Intuition & Practical Objective

This page builds the *why* of purged cross-validation with **no prior ML-evaluation knowledge needed**. The objective is one idea: **when your training data contains a copy of the answer, the model "scores well" without learning anything — and financial labels are built out of copies of each other.**

Start with the dumbest framing. You have data $(X_t, y_t)$, $t=1,\dots,T$. You want to know: *does my model generalise to data it has never seen?* The standard answer is cross-validation: split the data, train on one part, test on the other, and the test score measures generalisation — *provided the two parts are independent*. The word **independent** is doing all the work, and finance breaks it in a specific, measurable way.

Here is the mechanism, in three steps (López de Prado, AFML Ch. 7):

1. **The features are sticky.** A serially correlated feature satisfies $X_t \approx X_{t+1}$: today's momentum, volatility, or order-flow is a near-twin of yesterday's.
2. **The labels are made of shared data.** A label like "sign of the next $h$-bar return" at time $t$ uses bars $t{+}1\dots t{+}h$; the same label at $t{+}1$ uses bars $t{+}2\dots t{+}h{+}1$. They share $h-1$ bars, so $y_t \approx y_{t+1}$.
3. **The two near-duplicates land in different sets.** The moment observation $t$ goes to training and $t{+}1$ goes to testing, the model has effectively *seen the test answer in training*. Train on $(X_t, y_t)$, predict $y_{t+1}$ from $X_{t+1}$, and because $X_t\approx X_{t+1}$ and $y_t\approx y_{t+1}$, the prediction is right **even when $X$ is pure noise.**

The practical objective of this folder is to make step 3 *impossible*: **purging** deletes every training observation whose label overlaps a test label, **embargoing** deletes the serially-correlated observations right after the test block, and **CPCV** applies the honest split to every combination of test sets so you get a *distribution* of backtests instead of one fragile number.

---

### 2. Mathematical Ground Truth & Derivations

**Why labels become near-duplicates.** Let $r_t$ be the per-bar return and define the overlapping label at bar index $t$ by its *evaluation window* $[t+1,\,t+h]$:

$$
y_t = \operatorname{sgn}\Big(\sum_{s=t+1}^{t+h} r_s\Big), \qquad y_{t+1} = \operatorname{sgn}\Big(\sum_{s=t+2}^{t+h+1} r_s\Big).
$$

The two sums share $h-1$ of $h$ terms, so if $r_s$ are iid with $E[r_s]=0$, the correlation between the two *sums* is

$$
\rho = \frac{h-1}{h} \;\longrightarrow\; 1 \;\text{ as } h\to\infty.
$$

For jointly normal sums, the probability the two *signs* agree is (Sheppard's formula) $\operatorname{P}(y_t{=}y_{t+1}) = \tfrac12 + \tfrac{1}{\pi}\arcsin\rho$, which for $\rho=\tfrac{h-1}{h}$ grows monotonically toward $1$. **Long-horizon labels are the most redundant** — and therefore the most leakage-prone.

**Why standard $k$-fold CV misses it.** Standard CV's guarantee assumes each observation is drawn independently. When $y$ is built from overlapping windows, consecutive rows violate that: the "independent" test row is a function of nearly the same random draw as its training neighbour. Shuffling makes it *worse* — it interleaves the near-duplicate pairs across folds, so leakage is no longer confined to fold boundaries but is spread through every training set (AFML exercise 7.2: shuffled CV scores far higher than unshuffled on the same data).

**The formal overlap (preview of page 03).** Two interval labels $Y_i=f\big[t_{i,0},\,t_{i,1}\big]$ and $Y_j=f\big[t_{j,0},\,t_{j,1}\big]$ overlap — hence leak — if any of three sufficient conditions holds:

$$
t_{j,0}\le t_{i,0}\le t_{j,1}\qquad\text{or}\qquad t_{j,0}\le t_{i,1}\le t_{j,1}\qquad\text{or}\qquad t_{i,0}\le t_{j,0}\le t_{j,1}\le t_{i,1}.
$$

Purging removes from the training set every $i$ satisfying one of these against the test interval $j$ (AFML §7.4.1, Snippet 7.1).

---

### 3. Computational Implementation — seeing the redundancy with your own eyes

Stdlib only. This measures exactly how redundant overlapping labels are, as a function of the label horizon $h$ — the quantity that decides *how much* you must purge.

```python
import random, math

def label_agreement(h, T=40000, seed=0):
    """Fraction of adjacent overlapping labels that agree (pure-noise target)."""
    rnd = random.Random(seed)
    r = [rnd.gauss(0, 1) for _ in range(T + h + 1)]
    y = [1 if sum(r[t+1:t+1+h]) > 0 else 0 for t in range(T - h + 1)]
    agree = sum(y[t] == y[t+1] for t in range(len(y)-1)) / (len(y)-1)
    return agree

print("adjacent-label agreement P(Y_t == Y_{t+1}) vs label horizon h (pure noise):")
for h in (1, 2, 5, 10, 20, 40):
    print(f"  h={h:2d}: {label_agreement(h):.3f}")
```
```
adjacent-label agreement P(Y_t == Y_{t+1}) vs label horizon h (pure noise):
  h= 1: 0.501
  h= 2: 0.669
  h= 5: 0.795
  h=10: 0.858
  h=20: 0.900
  h=40: 0.933
```

With $h{=}1$ (non-overlapping) the labels are fair coin flips ($0.501$) — independent, as CV expects. At $h{=}10$ an adjacent pair agrees $86\%$ of the time; at $h{=}40$ it agrees $93\%$. **That 0.93 is the ceiling a leaked classifier "earns" for free.** If your CV reports higher accuracy than the agreement of adjacent labels on your noise floor, you are almost certainly reading leaked duplicates back.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Shuffling is a neutral, harmless step" — false.** Shuffling exists to break spurious ordering in IID data. In finance it *spreads* the near-duplicate train/test pairs through every fold, so it is not a fix — it is an amplifier of leakage (AFML Ex. 7.2).
2. **"I split once, so I'm clean" — insufficient.** A single chronological split avoids *this* mechanism only if labels don't overlap the split boundary. With an $h$-bar label, the $h-1$ bars before the split are contaminated even in a "clean" train/test split.
3. **Redundancy ≠ signal.** High adjacent-label agreement is a property of the *label construction*, not of your feature. Confusing the two is exactly how a noise model "beats" the market in a leaked backtest.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, **Ch. 7** (§7.2–7.3: why $k$-fold fails in finance; the $X_t\approx X_{t+1}$, $Y_t\approx Y_{t+1}$ mechanism) — the primary source for everything on this page.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, **Ch. 7** (§7.10.2: the wrong-vs-right CV example) — why screening inside folds matters.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Index Hub]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
- Forward: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/02-why-standard-cv-fails|02 · Why Standard CV Fails]]
- Labels that create the overlap: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]]
