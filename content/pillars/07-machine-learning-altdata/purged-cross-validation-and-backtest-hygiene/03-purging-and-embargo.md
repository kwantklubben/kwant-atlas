---
title: "7.2.3 Purging & Embargo"
tags:
  - pillar-machine-learning
  - purged-cross-validation
  - purging
  - embargo
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/02-why-standard-cv-fails|02 · Why Standard CV Fails]].

---

### 1. Intuition & Practical Objective

Once you accept that overlapping labels leak, the fix is obvious and blunt: **delete from the training set anything that overlaps the test set in time.** That is *purging*. And because financial features are serially correlated (an ARMA-style feature is a function of its own recent history), observations *immediately after* the test block still carry its echo - delete those too. That is the *embargo*.

The two tools remove two different mechanisms:

- **Purging** kills the *label-overlap* leak: a training label $Y_i$ and a test label $Y_j$ that are contingent on at least one common random draw are near-duplicates, and one of them must go.
- **Embargo** kills the *serial-correlation* leak: even a training label that does *not* overlap the test window can still predict the test outcome if the underlying feature regresses on values the test block "saw" - so we drop a buffer of $h\approx0.01T$ bars right after the test block.

The objective is precise bookkeeping: for each fold, compute *exactly which* training rows to purge and *exactly which* to embargo, and - crucially - know that this costs you training data.

---

### 2. Mathematical Ground Truth & Derivations

**Purging - the overlap rule (AFML §7.4.1, Snippet 7.1).** Suppose the test observation's label is $Y_j=f\big[t_{j,0},\,t_{j,1}\big]$. A training observation's label $Y_i=f\big[t_{i,0},\,t_{i,1}\big]$ overlaps it - and is purged - if any one of three sufficient conditions holds:

$$
t_{j,0}\le t_{i,0}\le t_{j,1} \qquad(\text{train label starts inside test}),
$$
$$
t_{j,0}\le t_{i,1}\le t_{j,1} \qquad(\text{train label ends inside test}),
$$
$$
t_{i,0}\le t_{j,0}\le t_{j,1}\le t_{i,1} \qquad(\text{train label envelops the test label}).
$$

Equivalently, the two bar-intervals $[t_{i,0},t_{i,1}]$ and $[t_{j,0},t_{j,1}]$ overlap iff

$$
t_{i,0}\le t_{j,1} \;\wedge\; t_{j,0}\le t_{i,1}.
$$

For a *contiguous* test block spanning bars $[a,b]$, every test label reaches to $b+h_{label}-1$ (a label starting at bar $b$ uses bars up to $b+h_{label}-1$). So a training observation with label window $[s,\,s+h_{label}-1]$ is purged iff

$$
s \le b+h_{label}-1 \;\wedge\; s+h_{label}-1 \ge a .
$$

**Embargo - the post-test buffer (AFML §7.4.2, Snippet 7.2).** We only need to drop training observations that *follow* the test, i.e. those with $t_{j,1}\le t_{i,0}\le t_{j,1}+h$. López de Prado implements this by *extending the test label* to $Y_j=f\big[t_{j,0},\,t_{j,1}+h\big]$ *before* purging: extending the test interval by $h$ bars and then purging automatically removes any training observation starting within the next $h$ bars. A small $h\approx0.01\,T$ "often suffices to prevent all leakage," verified by the test that performance no longer improves as $k\to T$ (AFML §7.4.2).

**The cost - sample loss.** Every purged/embargoed row is a row the model never trains on. For a label horizon $h_{label}$ and embargo $h$, roughly a fraction $\approx (2h_{label}+h)/T$ of the sample is discarded per interior fold - real information gone, which is why purging is a **bias–variance tradeoff**, not a free lunch (see page 05).

---

### 3. Computational Implementation - exact fold bookkeeping

Stdlib only. For $T=1000$ observations, label horizon $h=20$, $k=5$ contiguous folds, and an embargo of $10$ bars, this prints exactly how many training rows each fold loses to purge and to embargo.




Notice the geometry. Folds 2–4 each purge $\approx38$ overlapping training labels and embargo $10$; the **first** fold purges only $19$ (its test block sits at the start of the sample, so nothing precedes it to overlap) and the **last** fold $20$ plus a $0$ embargo (no future training data to embargo). For the interior folds the purge is symmetric (labels before *and* after the test block overlap it), which is exactly the "two overlaps that must be purged" AFML draws in his Fig. 7.2. Total cost: **4.9% of the training sample**, the price of honesty.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Purging only the "obvious" overlap.** Dropping only training rows that are *simultaneous* with the test is not enough - the second and third overlap conditions (label *ends inside* the test, label *envelops* the test) are just as leaky. Use the interval-intersection rule, not a timestamp equality.
2. **Forgetting the embargo.** Purging removes label overlap but leaves the serial-correlation echo. On ARMA-like features the post-test rows still predict the test outcome; without the embargo, the leak returns (AFML §7.4.2).
3. **Purging the test set itself.** Purge logic that accidentally removes test rows, or symmetric implementation mistakes (purging *future* data when the fold is the last one), silently corrupts the split. The last fold's embargo must be a no-op.

---

### 5. References

- **López de Prado**, *Advances in Financial Machine Learning*, **Ch. 7** (§7.4 purging & embargo; Snippets 7.1–7.3 `getTrainTimes`, `getEmbargoTimes`, `PurgedKFold`; Fig. 7.2 the two overlaps;

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/02-why-standard-cv-fails|02 · Why Standard CV Fails]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/04-combinatorial-purged-cv|04 · Combinatorial Purged CV]]
- The labels being purged come from: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (triple-barrier, interval labels)
- Purged CV applied to trees: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
