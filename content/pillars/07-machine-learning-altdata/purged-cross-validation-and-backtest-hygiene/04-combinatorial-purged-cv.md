---
title: "04 — Combinatorial Purged Cross-Validation (CPCV)"
tags:
  - pillar-machine-learning
  - purged-cross-validation
  - cpcv
  - backtest-paths
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/03-purging-and-embargo|03 · Purging & Embargo]].

---

### 1. Intuition & Practical Objective

Purging and embargo make a *single* train/test split honest — but a walk-forward backtest or a plain CV still reports **one** number: one Sharpe ratio from one historical path. A single path is one draw from a high-variance distribution, so selecting a strategy on that number is selecting on noise. The objective of **Combinatorial Purged Cross-Validation (CPCV)** is to replace that single path with a **distribution of $\varphi$ backtest paths**, each the honest, purged, out-of-sample result of a different train/test combination.

The idea in one sentence: split the data into $N$ contiguous groups, hold out every possible combination of $k$ of them as the test set (with purging/embargo against each), and recombine the forecasts so that every observation is tested in $\varphi$ different paths. You end up with a Sharpe *distribution* for the strategy — mean, variance, tails — instead of a single fragile point estimate. This is what lets you report "the strategy's Sharpe is $1.5\pm0.3$" and what makes the Deflated Sharpe Ratio meaningful (see page 06 and [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).

---

### 2. Mathematical Ground Truth & Derivations

**Partition.** Split the $T$ observations, without shuffling, into $N$ contiguous groups: groups $n=1,\dots,N-1$ of size $\lfloor T/N\rfloor$ and the $N$th of size $T-\lfloor T/N\rfloor(N-1)$ (AFML §12.4.1).

**Number of splits.** A test set of $k$ groups out of $N$ gives

$$
\binom{N}{k}=\prod_{i=0}^{k-1}\frac{N-i}{k!}
$$

possible train/test splits, each training on the $N-k$ remaining groups (a fraction $\theta=1-k/N$ of the data) and testing on $k$ groups.

**Number of backtest paths.** Because all $\binom{N}{k}$ combinations are enumerated, the tested groups are **uniformly distributed** across the $N$ groups. Each group therefore belongs to exactly $\varphi[N,k]$ test sets, where

$$
\varphi[N,k]=\frac{k}{N}\binom{N}{k}=\prod_{i=1}^{k-1}\frac{N-i}{(k-1)!}.
$$

$\varphi$ is the number of backtest paths: each path stitches together, observation by observation, the out-of-sample forecasts for which that observation's group was in the test set (AFML §12.4.1, Figs. 12.1–12.2).

**Key facts (AFML §12.4.3):**
- $k=1\Rightarrow\varphi[N,1]=1$ — CPCV degenerates to plain CV. CPCV is a *generalisation* of CV to $k>1$.
- $k=2\Rightarrow\varphi[N,2]=N-1$ paths. Rule of thumb: pick $N=\varphi+1$ groups, $k=2$, training each combination on $\theta=1-2/N$ of the data.
- Maximum paths at $N=T,\;k=N/2$: $\varphi_{\max}=\tfrac12\binom{T}{T/2}$, at the cost of training every model on only half the sample ($\theta=\tfrac12$).

**Why it beats a single path (AFML §12.5).** The variance of the sample-mean Sharpe across $\varphi$ CPCV paths is

$$
\sigma^2[\mu_i]=\varphi^{-1}\,\sigma_i^2\big[1+(\varphi-1)\bar\rho_i\big],
$$

where $\sigma_i^2$ is the variance of the Sharpe across paths and $\bar\rho_i$ the average off-diagonal correlation among the $\varphi$ paths. Since $\bar\rho_i<1$,

$$
\varphi^{-1}\sigma_i^2\;\le\;\sigma^2[\mu_i]\;<\;\sigma_i^2,
$$

and $\sigma^2[\mu_i]\to\bar\rho_i\,\sigma_i^2$ as $\varphi\to\infty$ (subject to the upper bound $\varphi\le\varphi[T,T/2]$) — it falls to zero only when the paths are independent ($\bar\rho_i=0$), otherwise a positive floor $\bar\rho_i\sigma_i^2$ survives (page 06's $\bar\rho=0.8$ case: little reduction). More, less-correlated paths $\Rightarrow$ less volatile (hence less overfit-prone) backtest.

---

### 3. Computational Implementation — counting splits and paths

Stdlib only. This reproduces the book's headline numbers: $\varphi[6,2]=5$ from $15$ splits, the general counters, and verifies that every group is tested in exactly $\varphi$ paths.

```python
import math
from itertools import combinations
from math import comb

def cpcv_paths(N, k):                 # phi[N,k] = (k/N)*C(N,k), exact integer
    p = 1
    for i in range(1, k): p *= (N - i)
    return p // math.factorial(k - 1)

print("CPCV book check, N=6, k=2:")
print(f"  splits C(6,2) = {comb(6,2)}  (book: 15)   paths phi[6,2] = {cpcv_paths(6,2)}  (book: 5)")
print(f"  phi[6,3] = {cpcv_paths(6,3)}   C(6,3) = {comb(6,3)}")

print("\nGeneral counters:")
for N, k in ((10,2),(101,2),(10,5),(20,10)):
    print(f"  phi[{N},{k}] = {cpcv_paths(N,k)}   (train fraction theta=1-{k}/{N} = {1-k/N:.2f})")

print("\nEach group is tested in exactly phi[N,k] paths:")
N, k = 6, 2
seen = {g: 0 for g in range(N)}
for c in combinations(range(N), k):
    for g in c: seen[g] += 1
print(f"  N=6,k=2 group memberships: {dict(seen)}  -> all equal {cpcv_paths(6,2)} = phi")

print("\nMax paths at N=T, k=N/2:")
for T in (10, 20, 30):
    print(f"  N=T={T}, k={T//2}: phi = {cpcv_paths(T, T//2)}")
```
```
CPCV book check, N=6, k=2:
  splits C(6,2) = 15  (book: 15)   paths phi[6,2] = 5  (book: 5)
  phi[6,3] = 10   C(6,3) = 20

General counters:
  phi[10,2] = 9   (train fraction theta=1-2/10 = 0.80)
  phi[101,2] = 100   (train fraction theta=1-2/101 = 0.98)
  phi[10,5] = 126   (train fraction theta=1-5/10 = 0.50)
  phi[20,10] = 92378   (train fraction theta=1-10/20 = 0.50)

Each group is tested in exactly phi[N,k] paths:
  N=6,k=2 group memberships: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5}  -> all equal 5 = phi

Max paths at N=T, k=N/2:
  N=T=10, k=5: phi = 126
  N=T=20, k=10: phi = 92378
  N=T=30, k=15: phi = 77558760
```

Read the tension in the "General counters" block. With $k=2$ you get $N-1$ paths while training on $80\text{–}98\%$ of the data — the practical regime. Doubling the test fraction to $k=N/2$ explodes the path count (92378, 77 million) but forces every model to train on only half the sample. **More paths and more training data are in direct competition** — choose the trade-off deliberately.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **CPCV is not historically accurate.** It answers "how might the strategy perform out-of-sample under $k$-of-$N$ stress scenarios," *not* "what would it have earned in real time." Treat it as an inferential tool, not a historical replay (AFML §12.3 disadvantage 2).
2. **Leakage still possible without purge/embargo.** CPCV *reuses* the test set across many combinations; if any combination lets training data touch test data, the leak is amplified over all paths. Purging and embargo are mandatory inside CPCV (AFML §12.4.2 step 3).
3. **Path correlation $\bar\rho_i$ is the hidden tax.** If the $\varphi$ paths are highly correlated, $\sigma^2[\mu_i]\approx\sigma_i^2$ and CPCV buys little variance reduction. Truly independent paths are what deflate the noise — which is why $k=2,N=\varphi+1$ (minimal overlap) is the recommended operating point.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, **Ch. 12** (§12.4 "The Combinatorial Purged Cross-Validation Method": §12.4.1 splits & $\varphi[N,k]$, §12.4.2 the algorithm, §12.4.3 examples and the $k=2$ rule of thumb; §12.5 the variance formula $\sigma^2[\mu_i]=\varphi^{-1}\sigma_i^2[1+(\varphi-1)\bar\rho_i]$). *Primary source; every formula on this page is transcribed from it and numerically reproduced.*
- **Bailey, Borwein, López de Prado & Zhu**, *The Probability of Backtest Overfitting*, J. Comp. Finance 20(4) (2017) — the CSCV/PBO machinery CPCV complements.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/03-purging-and-embargo|03 · Purging & Embargo]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/06-advanced-extensions|06 · Advanced Extensions]]
- Why a distribution matters (single-path Sharpe is a lottery): [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
- CPCV hyperparameter tuning in practice: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
