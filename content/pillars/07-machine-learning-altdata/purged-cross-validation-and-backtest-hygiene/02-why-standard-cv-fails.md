---
title: "7.2.2 Why Standard k-Fold CV Fails in Finance"
tags:
  - pillar-machine-learning
  - purged-cross-validation
  - cross-validation
  - leakage
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Standard $k$-fold CV was built for **IID data**: each row is an independent draw, so no row in the training set can tell you anything about a row in the test set except what the model should *generalise*. Finance violates the premise twice, and the second violation is what this page makes visible:

1. **The data are not IID.** Features are serially correlated ($X_t\approx X_{t+1}$) and labels are formed on overlapping windows ($Y_t\approx Y_{t+1}$). Putting a training row next to a test row that is its near-duplicate leaks the answer.
2. **The test set is reused.** The same test data is consulted again and again while a researcher searches hyperparameters, features, and model families — selection bias, the *second* way CV overstates skill (AFML §7.3). That second cause is the domain of [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]].

The objective of this page is to demonstrate cause #1 so concretely that you never trust an un-purged financial CV score again: **on a pure-noise target, standard CV's accuracy rises toward the adjacent-label agreement simply because you make the folds thinner.** That is not signal. That is leakage.

---

### 2. Mathematical Ground Truth & Derivations

**The two ingredients of label leakage.** A classifier trained on $(X_t,Y_t)$ is asked to predict $Y_{t+1}$ from $X_{t+1}$. It scores correctly *even when $X$ is irrelevant* when both near-equalities hold:

$$
X_t \approx X_{t+1} \qquad\text{(serial correlation)}, \qquad Y_t \approx Y_{t+1} \qquad\text{(overlapping label windows)}.
$$

López de Prado (AFML §7.3) is explicit: leakage requires the *pair* $(X_i,Y_i)\approx(X_j,Y_j)$. $X_i\approx X_j$ alone, or $Y_i\approx Y_j$ alone, is not enough — the model must be able to map a near-duplicate feature to a near-duplicate label.

**Why thin folds leak more.** In contiguous $k$-fold CV, each fold is a block of bars. An observation $t$ inside a thick block has its temporal neighbours $t\pm1$ in the *same* test block, so no training row is a near-duplicate — leakage is confined to the two fold boundaries. As the blocks shrink (larger $k$, toward leave-one-out), a larger fraction of test rows sit next to a training row, so the leaked fraction grows. AFML §7.4.1 states the diagnostic directly: *"When leakage takes place, performance improves merely by increasing $k\to T$."* The purge-free CV then reports accuracy that is a function of **how many folds you chose**, not of any real skill.

---

### 3. Computational Implementation — manufacturing a false discovery

Stdlib only. Target $y_t=\operatorname{sgn}\sum_{s=t+1}^{t+10}r_s$ is **pure noise** (iid daily returns — there is no edge by construction). The "learner" copies the nearest *training* label **in time** — the minimal model that exploits serial structure. It must score $\approx0.5$ under honest evaluation; under standard CV it "learns" exactly as much as the folds leak.

```python
import random, math

def labels(T, h, seed=3):
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
        s = min(train_idx, key=lambda q: abs(q - t))   # nearest training label in time
        ok += (y[s] == y[t]); tot += 1
    return ok/tot if tot else float('nan')

T, h = 2400, 10
y = labels(T, h); N = T - h + 1
agree = sum(y[t]==y[t+1] for t in range(N-1) if y[t]>=0 and y[t+1]>=0) / \
        sum(1 for t in range(N-1) if y[t]>=0 and y[t+1]>=0)
print(f"P(Y_t==Y_t+1), overlapping h=10 labels = {agree:.3f}")
for block in (N//5, 40, 5, 1):                 # thick -> LOO-like folds
    k = math.ceil(N/block); al, ap = [], []
    for i in range(k):
        t0 = i*block; t1 = min((i+1)*block, N)
        test = list(range(t0, t1)); B = (t1-1) + h - 1
        trn_std = [s for s in range(N) if not (t0 <= s < t1)]
        trn_pur = [s for s in trn_std if not (s <= B and s + h - 1 >= t0)]  # purge overlap
        al.append(nn_time_acc(trn_std, test, y)); ap.append(nn_time_acc(trn_pur, test, y))
    print(f"  fold-block~{block:4d} (k~{k:5d}): STANDARD k-fold acc={sum(al)/k:.3f} | PURGED acc={sum(ap)/k:.3f}")
```
```
P(Y_t==Y_t+1), overlapping h=10 labels = 0.854
  fold-block~ 478 (k~    6): STANDARD k-fold acc=0.451 | PURGED acc=0.426
  fold-block~  40 (k~   60): STANDARD k-fold acc=0.594 | PURGED acc=0.535
  fold-block~   5 (k~  479): STANDARD k-fold acc=0.798 | PURGED acc=0.509
  fold-block~   1 (k~ 2391): STANDARD k-fold acc=0.854 | PURGED acc=0.519
```

Read the columns. Under **standard** contiguous $k$-fold the accuracy is not constant — it climbs from $0.45$ (thick folds) to $0.85$ (leave-one-out), converging exactly on the adjacent-label agreement $0.854$: **the classifier is "earning" nothing but leaked duplicates.** Under **purging**, every configuration sits at $\approx0.5$ regardless of fold count — the honest null, because the leaked training rows have been deleted. This is the textbook false discovery, manufactured end-to-end from noise, exactly as AFML §7.3 predicts.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Choosing folds to flatter yourself.** If un-purged CV accuracy rises with $k$, that *is* the leak diagnostic (AFML §7.4.1). Reporting "best-$k$" accuracy without purging is reporting your choice of folds.
2. **Shuffling hides the crime.** Shuffled CV interleaves near-duplicate pairs across *every* fold, so even thick folds leak — and the score goes *up* (AFML Ex. 7.2). Shuffling is not a cure; it is how the leak becomes total.
3. **Crossing into the second failure.** Even a correctly purged CV suffers selection bias if the test set is reused across many trials. Purged CV fixes label leakage, not the missing-$N$ problem — that is the separate domain of [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (DSR, PBO).

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, **Ch. 7** (§7.3 "Why k-fold CV fails in finance"; §7.4.1 the $k\to T$ diagnostic). *Primary source for this page.*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, **Ch. 7** (§7.10.2 wrong-vs-right CV; the full-data-screening example reports $\sim$3% CV error against a true $\sim$50%) — the classical analogue of the leak above.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/03-purging-and-embargo|03 · Purging & Embargo]]
- The second failure (selection bias): [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
