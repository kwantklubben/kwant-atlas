# Code Audit — runnable-Python blocks across `content/`

Automated harness over `content/` (excluding `content/_legacy/`). Every fenced ```python block was executed with `python3 -c` (timeout 60s, scratch cwd) and its stdout compared to the documented output block. Failures were re-run as a temp **file** (timeout 240s) to separate *runs-as-file* cases (multiprocessing / `__main__` guards) from real errors. Where a page emits **one combined output block for several consecutive python snippets**, the snippets' stdout is concatenated before comparison.

Environment: Python 3.14.7; numpy/scipy/pandas/numba present; **statsmodels, sklearn, matplotlib not installed**.

---

## 1. Summary

| Metric | Count |
|---|---|
| Total ```python blocks | 767 |
| Block groups (a group = 1+ blocks sharing one output block) | 764 |
| Blocks with a documented output block | 746 |
| Blocks with no adjacent output block | 21 |
| **Ran OK under `python3 -c` (exit 0)** | **756** (groups) |
| Runs as FILE only (multiprocessing / `__main__`) | 2 (groups) |
| **Failed in both modes** | **6** (groups) |

| Output diff class | Groups |
|---|---|
| Exact stdout match | 707 |
| Whitespace-only (column alignment) | 4 |
| Blank-line-only | 4 |
| Numeric within 1e-6 (last-digit float) | 2 |
| Reordered lines (same content, different order) | 1 |
| **Genuine content mismatch** | **22** |
| Comparable groups | 740 |

---

## 2. Non-running blocks

- **`content/pillars/01-quantitative-research/fundamental-multi-factor-models.md:48`** — `ModuleNotFoundError: No module named 'statsmodels'`
- **`content/pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading.md:55`** — `ModuleNotFoundError: No module named 'statsmodels'`
- **`content/pillars/04-quantitative-risk/systemic-risk-and-aggregation/index.md:52`** — `NameError: name 'Phinv' is not defined`
- **`content/pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr.md:53`** — `ModuleNotFoundError: No module named 'sklearn'`
- **`content/pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice.md:94`** — `NameError: name 'em_gmm' is not defined`
- **`content/pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice.md:112`** — `NameError: name 'r' is not defined`

### Runs as a FILE only (expected — not a defect)

- `content/pillars/04-quantitative-risk/credit-risk-and-the-merton-model/06-advanced-extensions.md:60` — fails under `-c` (TIMEOUT after 60s); exits 0 as a file. Documented-output comparison as file: **exact**.
- `content/pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice.md:47` — fails under `-c` (concurrent.futures.process.BrokenProcessPool: A process in the process pool was ); exits 0 as a file. Documented-output comparison as file: **genuine**.

---

## 3. Output mismatches (documented vs actual)

`stable=True` = 3 independent re-runs produced byte-identical stdout (deterministic block → the documented output is stale/incorrect). `stable=False` = the block's own stdout varies run-to-run (timing / threading / unseeded RNG) → exact comparison is not meaningful.

### 3.1 `genuine` (22)

#### `content/foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion.md:105` — stable: True, nondet-hint: True, group size: 1
> Code prints one extra line (`c=1.5 f=0.090 sim=0.001362 ...`) absent from the documented block (seeded RNG, deterministic).
```diff
+  c=1.5 f=0.090  sim=0.001362  theory=0.001348  ruined=0.019
```

#### `content/foundations/linear-algebra-and-matrices/06-advanced-extensions.md:46` — stable: True, nondet-hint: True, group size: 1
> Float precision on an ill-conditioned matrix (same kappa, different last digits) — platform/BLAS-dependent, benign.
```diff
-  n=3: kappa=5.241e+02   max|x-1| = 9.992e-15
+  n=3: kappa=5.241e+02   max|x-1| = 1.033e-14
-  n=8: kappa=1.304e+07   max|x-1| = 4.188e-07
+  n=8: kappa=1.306e+07   max|x-1| = 1.372e-07
```

#### `content/foundations/statistics-and-inference/index.md:78` — stable: True, nondet-hint: True, group size: 1
> Deterministic but the Monte-Carlo figures differ in the last 2-3 digits — documented block was captured on a different platform/BLAS; seed reproduces a stable but slightly different stream.
```diff
-MSE(sigma2_MLE)=3.0553  theory (2n-1)/n^2*sig^4=3.0400
-MSE(S^2)       =3.5790  theory 2*sig^4/(n-1)     =3.5556
-Exp rate MLE: mean=2.5141 (true 2.5)  Var=0.031716 vs CRLB lam^2/n=0.031250
-n=  10: sd(mean)=0.31672  sigma/sqrt(n)=0.31623
-n=  40: sd(mean)=0.15831  sigma/sqrt(n)=0.15811
-n= 160: sd(mean)=0.07901  sigma/sqrt(n)=0.07906
+MSE(sigma2_MLE)=3.0366  theory (2n-1)/n^2*sig^4=3.0400
+MSE(S^2)       =3.5459  theory 2*sig^4/(n-1)     =3.5556
+Exp rate MLE: mean=2.5145 (true 2.5)  Var=0.031743 vs CRLB lam^2/n=0.031250
+n=  10: sd(mean)=0.31681  sigma/sqrt(n)=0.31623
+n=  40: sd(mean)=0.15793  sigma/sqrt(n)=0.15811
+n= 160: sd(mean)=0.07893  sigma/sqrt(n)=0.07906
```

#### `content/pillars/03-derivative-pricing/interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates.md:63` — stable: True, nondet-hint: False, group size: 1
> Column spacing changed and `T=1`→`T=1.0` label formatting; all numbers identical.
```diff
-  0.0  1.000000  3.00   3.00      3.10
-  0.5  0.984743  3.08   3.15      3.25
-  1.0  0.968991  3.15   3.30      3.40
-  2.0  0.936131  3.30   3.60      3.71
-  5.0  0.829029  3.75   4.50      4.63
- 10.0  0.637628  4.50   6.00      6.17
-reconstruct T=1: P=0.968991 vs exp(-∫f)=0.968991  err=4.9e-14
-reconstruct T=5: P=0.829029 vs exp(-∫f)=0.829029  err=1.4e-11
-reconstruct T=10: P=0.637628 vs exp(-∫f)=0.637628  err=3.0e-11
+  0.0  1.000000   3.00    3.00      3.10
+  0.5  0.984743   3.08    3.15      3.25
+  1.0  0.968991   3.15    3.30      3.40
+  2.0  0.936131   3.30    3.60      3.71
+  5.0  0.829029   3.75    4.50      4.63
+ 10.0  0.637628   4.50    6.00      6.17
+reconstruct T=1.0: P=0.968991 vs exp(-∫f)=0.968991  err=4.9e-14
+reconstruct T=5.0: P=0.829029 vs exp(-∫f)=0.829029  err=1.3e-11
+reconstruct T=10.0: P=0.637628 vs exp(-∫f)=0.637628  err=3.0e-11
+
```

#### `content/pillars/03-derivative-pricing/interest-rate-and-term-structure/06-advanced-extensions.md:73` — stable: True, nondet-hint: False, group size: 1
> Code prints an extra `(rho=-0.3 -> ...)` annotation line absent from the documented block.
```diff
+
+  (rho=-0.3 -> downward ATM skew; nu=0.5 -> curvature -> smile)
```

#### `content/pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation.md:59` — stable: True, nondet-hint: True, group size: 1
> Code prints two extra lines (EWMA next-day vol) absent from the documented block.
```diff
+
+EWMA factor-1 next-day vol after the spike = 0.0136
+  (above the plain sample vol 0.0120 -> FHS would scale recent shocks up)
```

#### `content/pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/06-advanced-extensions.md:57` — stable: True, nondet-hint: False, group size: 1
> Code prints an extra `growth g(w*) = 0.133478` line absent from the documented block.
```diff
+growth g(w*)          = 0.133478
```

#### `content/pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers.md:53` — stable: True, nondet-hint: False, group size: 1
> Documented block is **abridged/stylized** (12 of 34 vocabulary rows plus an ellipsis; cosine rows listed in a different order and with different padding). The headline singular values (8.103, 7.584) and cosine values are correct.
```diff
+  a             [-0.405, +2.454]
+  again         [-0.927, +0.151]
+  and           [-3.080, -0.851]
+  badly         [-0.484, +1.217]
+  beat          [-0.437, +1.213]
+  charge        [-0.571, +3.146]
+  costs         [-1.975, -0.760]
+  cut           [-2.220, -0.976]
+  demand        [-1.224, -0.302]
+  disappointed  [-1.719, -0.374]
+  exceeded      [-1.125, +0.638]
+  expanded      [-1.687, -0.605]
+  expectations  [-0.869, +0.940]
+  faster        [-1.074, +0.613]
+  flat          [-1.382, -0.567]
+  grew          [-1.433, +0.331]
+  guidance      [-1.622, +0.194]
+  hit           [-0.538, +2.608]
+  margins       [-1.359, -0.460]
+  missed        [-0.457, +1.304]
+  our           [-1.137, +0.793]
+  outlook       [-1.589, -0.767]
+  quarter       [-0.553, +1.226]
-  guidance      [-1.622, +0.194]
-  outlook       [-1.589, -0.767]
-  missed        [-0.457, +1.304]
... (truncated)
```

#### `content/pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop.md:70` — stable: False, nondet-hint: True, group size: 1
```diff
-20,000 events: heap push+pop=43.1 ms  sorted-list=89.2 ms  ratio=2.07x
+20,000 events: heap push+pop=42.4 ms  sorted-list=93.0 ms  ratio=2.19x
```

#### `content/pillars/08-quantitative-development/event-driven-backtesting-engines/index.md:69` — stable: False, nondet-hint: True, group size: 1
```diff
-20,000 events: heap=45.9 ms  sorted-list=95.3 ms  ratio=2.07x
+20,000 events: heap=43.2 ms  sorted-list=90.1 ms  ratio=2.08x
```

#### `content/pillars/08-quantitative-development/high-performance-cpp-for-trading/04-zero-cost-abstraction.md:84` — stable: False, nondet-hint: True, group size: 1
```diff
-  fresh list [0.0]*8 :    90.4 ns/op  (checksum 0.0)
-  reused buffer      :    26.8 ns/op  (checksum 0.0)
-  per-op saving      :    63.6 ns  (3.37x)
+  fresh list [0.0]*8 :    82.1 ns/op  (checksum 0.0)
+  reused buffer      :    25.7 ns/op  (checksum 0.0)
+  per-op saving      :    56.4 ns  (3.20x)
-At 1e6 msgs/s, saving 64 ns/op removes ~0.06 us per message
-  = 6.4% of a 100 us alpha half-life window consumed by the allocator
+At 1e6 msgs/s, saving 56 ns/op removes ~0.06 us per message
+  = 5.6% of a 100 us alpha half-life window consumed by the allocator
```

#### `content/pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions.md:78` — stable: False, nondet-hint: True, group size: 1
```diff
-  single-shot : mean   171.3 ns   median   169.0 ns   p99   186.0 ns
-  batched     :   103.2 ns/op  (100,000 calls inside one timed region)
-  timer overhead inflates single-shot by 1.7x
+  single-shot : mean   168.6 ns   median   167.0 ns   p99   184.0 ns
+  batched     :    95.5 ns/op  (100,000 calls inside one timed region)
+  timer overhead inflates single-shot by 1.8x
-  spread of single-shot samples: min 160 ns, max 12678 ns  -> report min/percentiles, never a lone mean
+  spread of single-shot samples: min 156 ns, max 5026 ns  -> report min/percentiles, never a lone mean
```

#### `content/pillars/08-quantitative-development/low-latency-linux-and-networking/02-kernel-tuning-for-latency.md:57` — stable: True, nondet-hint: False, group size: 1
> Difference is formatting (`16ns`→`16 ns`) **plus an extra undocumented line** `NUMA: local DRAM ~80 ns, ...` that the code prints but the documented block omits.
```diff
-4 KB : 16,384 pages, TLB miss  99.6%, walk 16ns -> effective addr-latency  19.9 ns (vs 4.0ns base)
-2 MB : 32 pages, TLB miss   0.0%, walk 12ns -> effective addr-latency   4.0 ns (vs 4.0ns base)
+4 KB : 16,384 pages, TLB miss  99.6%, walk 16 ns -> effective addr-latency  19.9 ns (vs 4.0 ns base)
+2 MB : 32 pages, TLB miss   0.0%, walk 12 ns -> effective addr-latency   4.0 ns (vs 4.0 ns base)
+NUMA: local DRAM ~80 ns, remote socket +40-80 ns per access
```

#### `content/pillars/08-quantitative-development/low-latency-linux-and-networking/06-advanced-extensions.md:47` — stable: True, nondet-hint: True, group size: 1
```diff
+-> coarse bins bias the tail estimate more than the median; size bins to the percentile you actually quote.
```

#### `content/pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization.md:52` — stable: False, nondet-hint: True, group size: 1
```diff
-pure-Python loop:   620.43 ms
-numpy vectorized:     7.495 ms
-speedup:         82.8x
+pure-Python loop:   715.36 ms
+numpy vectorized:    9.447 ms
+speedup:     75.7x
```

#### `content/pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization.md:80` — stable: False, nondet-hint: True, group size: 1
```diff
-pure-Python double loop:    0.28 s
+pure-Python double loop:    0.35 s
-speedup:                  122x
+speedup:       156x
```

#### `content/pillars/08-quantitative-development/python-quant-stack/03-pandas-pitfalls.md:73` — stable: False, nondet-hint: True, group size: 1
```diff
-float64  s+1.0:   0.08 ms
-object   s+1.0:   3.93 ms
-object-vs-float slowdown: 47x
+float64  s+1.0:    0.10 ms
+object   s+1.0:    4.40 ms
+object-vs-float slowdown: 44x
```

#### `content/pillars/08-quantitative-development/python-quant-stack/03-pandas-pitfalls.md:96` — stable: False, nondet-hint: True, group size: 1
```diff
-groupby+apply (python call):    5.4 ms
-groupby+mean  (cython):         1.8 ms
-slowdown of apply:            3.0x
+groupby+apply (python call):    8.4 ms
+groupby+mean  (cython):         2.5 ms
+slowdown of apply:           3.4x
```

#### `content/pillars/08-quantitative-development/python-quant-stack/04-numba-and-jit.md:51` — stable: False, nondet-hint: True, group size: 1
```diff
-pure-Python loop:     324.2 ms
-numpy   np.dot:       0.687 ms
-numba   njit loop:    1.956 ms  (first-call compile excluded)
-numba vs Python:     165.7x   numba vs numpy: 0.35x
+pure-Python loop:     352.5 ms
+numpy   np.dot:       5.500 ms
+numba   njit loop:    2.028 ms  (first-call compile excluded)
+numba vs Python:     173.8x   numba vs numpy: 2.71x
```

#### `content/pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice.md:47` — stable: None, nondet-hint: True, group size: 1
```diff
-sequential 2x burn:   4.726 s
-two threads (GIL):    4.632 s  speedup 1.02x  (serialized)
-two processes (free): 2.493 s  speedup 1.90x
+sequential 2x burn:   5.090 s
+two threads (GIL):    5.952 s  speedup 0.86x  (serialized)
+two processes (free): 3.009 s  speedup 1.69x
```

#### `content/pillars/08-quantitative-development/python-quant-stack/06-advanced-extensions.md:45` — stable: False, nondet-hint: True, group size: 1
```diff
-pandas groupby-sum:   45.0 ms   result mean 21.100
-polars groupby-sum:    5.1 ms   result mean 21.100
-polars/pandas ratio: 0.11x  (identical numeric result)
+pandas groupby-sum:    46.7 ms   result mean 21.100
+polars groupby-sum:     5.8 ms   result mean 21.100
+polars/pandas ratio: 0.12x  (identical numeric result)
```

#### `content/pillars/08-quantitative-development/python-quant-stack/index.md:73` — stable: False, nondet-hint: True, group size: 1
```diff
-pure-Python loop:   620.43 ms
-numpy vectorized:     7.495 ms
-speedup:         82.8x
+pure-Python loop:   646.52 ms
+numpy vectorized:    7.518 ms
+speedup:     86.0x
```

### 3.2 `reordered` (1)

#### `content/pillars/03-derivative-pricing/exotic-and-path-dependent-options/01-from-zero-intuition.md:53` — stable: True, nondet-hint: True, group size: 1
```diff
+lookback put (path-dependent)  = 8.7952
-lookback put (path-dependent)  = 8.7952
```

### 3.3 Cosmetic-only (`whitespace` / `blanklines` / `numeric_tolerance`)

These do not change the numbers presented — spacing, trailing blank lines, or a last-digit float.

- `content/foundations/probability-and-measure-theory/01-from-zero-intuition.md:52` — `whitespace`
- `content/pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin.md:55` — `whitespace`
- `content/pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/05-failure-modes-and-practice.md:53` — `whitespace`
- `content/pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact.md:75` — `whitespace`
- `content/pillars/02-algorithmic-hft/queue-position-and-fill-probability/02-the-order-queue.md:73` — `blanklines`
- `content/pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice.md:52` — `blanklines`
- `content/pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition.md:46` — `blanklines`
- `content/pillars/08-quantitative-development/low-latency-linux-and-networking/04-market-data-networking.md:51` — `blanklines`
- `content/foundations/econometrics-and-timeseries/04-volatility-modeling.md:58` — `numeric_tolerance`
- `content/pillars/05-portfolio-optimization/robust-optimization/01-from-zero-intuition.md:69` — `numeric_tolerance`

---

## 4. Nondeterministic-but-plausible list

Blocks whose stdout is not byte-reproducible (wall-clock timing, CPU scheduling, unseeded RNG). Exact match is not applicable; the documented block is a representative run and the quantities are of the same magnitude/behaviour.

- `content/pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop.md:70`
- `content/pillars/08-quantitative-development/event-driven-backtesting-engines/index.md:69`
- `content/pillars/08-quantitative-development/high-performance-cpp-for-trading/04-zero-cost-abstraction.md:84`
- `content/pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions.md:78`
- `content/pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization.md:52`
- `content/pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization.md:80`
- `content/pillars/08-quantitative-development/python-quant-stack/03-pandas-pitfalls.md:73`
- `content/pillars/08-quantitative-development/python-quant-stack/03-pandas-pitfalls.md:96`
- `content/pillars/08-quantitative-development/python-quant-stack/04-numba-and-jit.md:51`
- `content/pillars/08-quantitative-development/python-quant-stack/06-advanced-extensions.md:45`
- `content/pillars/08-quantitative-development/python-quant-stack/index.md:73`

Separately, **379 groups** contain seeded-RNG / numpy / timing constructs whose stdout **matches exactly** — determinism is confirmed there.

---

## 5. Library-promise consistency

**Stdlib-only prose contradicted by a third-party import:** 0

None — every block whose adjacent prose promises "stdlib only" imports only the standard library.

**Blocks importing libraries not installed in this environment:** 3

- `content/pillars/01-quantitative-research/fundamental-multi-factor-models.md:48` — imports ['statsmodels'] (block cannot run here; output unverifiable)
- `content/pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading.md:55` — imports ['statsmodels'] (block cannot run here; output unverifiable)
- `content/pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr.md:53` — imports ['sklearn'] (block cannot run here; output unverifiable)

---

## 6. Verdict

Of **767 embedded Python blocks (764 groups)**, **756 groups run cleanly under `python3 -c`**, **2 run only as a file** (multiprocessing / `__main__` — expected, not defects), and **6 groups fail outright**: 3 require libraries absent from this environment (statsmodels ×2, sklearn), and 3 call names defined in an earlier block (`Phinv`, `em_gmm`, `r`), so they are not self-contained. Of the 740 groups with a documented output block, **707 match stdout exactly**; 10 differ only cosmetically and 1 only in line order. **22 groups are genuine content mismatches**: 10 are deterministic (stale documented block to regenerate) and 12 are timing/nondeterminism by construction. No prose "stdlib-only" promise is violated. **Overall: the corpus is in strong shape — 95.5% of documented outputs are byte-exact.**
