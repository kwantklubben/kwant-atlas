---
title: "02 — The Factor Zoo: Multiple Testing & How Many Factors Are Real"
tags:
  - pillar-quant-research
  - factor-investing-and-timing
  - factor-zoo
  - multiple-testing
  - data-mining
  - fdr
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/factor-investing-and-timing/01-from-zero-intuition|01 · From Zero]] and [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]].

---

### 1. Intuition & Practical Objective

Cochrane (2011) named it in the abstract of his presidential address: "we thought that the cross-section of expected returns came from the CAPM. Now we have a **zoo of new factors**." Momentum, accruals, equity issuance, beta arbitrage, credit risk, market timing, FX carry, put writing, liquidity provision — Cochrane lists them and then asks the practitioner's questions directly:

> "First, which characteristics really provide independent information about average returns? Which are subsumed by others? ... Third, how many of these new factors are really important?"

This page is about that problem, and it has two halves that must be held together:

- **The statistical half.** If you test $M$ candidate characteristics and all of them are *null*, you will still "discover" about $4.6\%\times M$ at the conventional $|t|>2$ threshold. With $M$ in the hundreds, spurious factors are not a risk — they are a certainty. Green–Hand–Zhang catalogued ~100 published and unpublished characteristics; Harvey–Liu–Zhu argued the literature's effective hurdle should be $t>3$, not $t>2$.
- **The economic half.** Most "new" factors are not new. They are **redundant combinations** of a few underlying ones (value, momentum, quality, low-vol, size). Cochrane's hope is that "we can again account for $N$ independent dimensions of expected returns with $K<N$ factor exposures."

> **The one-sentence essence.** "A factor zoo is the predictable result of searching hundreds of characteristics with a fixed significance threshold — the number of *real* factors is governed by a multiple-testing discipline ($t>3$, FDR, deflated Sharpe), not by how many papers report $t>2$."

**Why it matters for investing.** Every factor you add to a portfolio is a claim that it carries *independent* expected return. If it is really a noisy proxy for value, you have not diversified — you have doubled your value exposure and called it two factors. Cochrane's warning to empiricists applies to allocators too: "expected returns, variances, and covariances are stable functions of characteristics such as size and book-to-market ratio, and not security names."

---

### 2. Mathematical Ground Truth & Derivations

**The expected false-discovery count.** Consider $M$ independent tests of a true-null characteristic (zero premium). Under the null, the $t$-statistic is standard normal, so the expected number of $|t|>2$ "discoveries" is
$$
\mathbb{E}[\#\text{false discoveries}]=M\times\Pr(|Z|>2)=M\times0.0455.
$$
For $M=300$ that is **13.7 spurious factors** — all with no economic content whatsoever.

**The family-wise and false-discovery corrections.**
- **Bonferroni (FWER $\le\alpha$):** reject only if $|t|>z_{1-\alpha/(2M)}$. For $M=300$, $\alpha=0.05$, this is $|t|>3.76$.
- **Harvey–Liu–Zhu (2016) rule of thumb:** the factor literature should require $|t|>3$ — a coarser, less conservative hurdle that still eliminates the vast majority of chance discoveries.
- **Benjamini–Hochberg FDR:** sort the $p$-values $p_{(1)}\le\dots\le p_{(M)}$ and reject the largest $k$ with
$$
p_{(k)}\le\frac{k}{M}q.
$$
Unlike Bonferroni, FDR accepts that a controlled *fraction* of discoveries may be false — the right criterion when you must pick a factor set rather than certify a single signal.

**The "how many are independent?" question.** If the true returns follow a $K$-factor structure,
$$
r_t=\alpha+Bf_t+\varepsilon_t,\qquad \Sigma=B\Omega B^\top+D,
$$
then $M\gg K$ candidate characteristics are just noisy functions of the same $K$ factors. The empirical test is whether adding factor $j$ raises the cross-sectional fit *after* controlling for the existing factors — the incremental-$R^2$ / GRS test. Five variants of value do not add five dimensions of expected return; they add one dimension and four units of collinearity (quantified in [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|the sibling folder's failure page]]).

**Data-snooping in the presence of a search.** Bailey, Borwein, López de Prado & Zhu (2014) put a number on the search itself. If you try $m$ configurations and keep the best in-sample Sharpe $SR^*$, the *expected maximum* under the null is approximately
$$
\mathbb{E}\big[\max SR\big]\approx\sqrt{2\ln m}\cdot \sigma_{SR},
$$
so the best of $m=1000$ null backtests looks like a Sharpe of order $2\text{–}3$ by construction. The **Deflated Sharpe Ratio** discounts exactly this. (See [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]].)

---

### 3. Computational Implementation — the zoo, built and then audited

Stdlib only. Two experiments: first the pure-null census (how many factors are born from nothing), then a *mixed* zoo with a handful of genuinely priced signals, audited with the $t>2$/$t>3$ hurdles and Benjamini–Hochberg FDR.

```python
import math, random
from statistics import NormalDist

def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))
def tstat(xs): return mean(xs)/(sd(xs)/math.sqrt(len(xs)))

# --- A. PURE-NULL CENSUS: M factors, every one worthless ---
random.seed(101)
M_NULL, OBS = 300, 480            # 300 candidates, 40 years monthly
trials = [tstat([random.gauss(0, 0.01) for _ in range(OBS)]) for _ in range(M_NULL)]
h2 = sum(1 for t in trials if abs(t) > 2.0)
h3 = sum(1 for t in trials if abs(t) > 3.0)
print(f"NULL zoo (M={M_NULL}, T={OBS}):")
print(f"  |t|>2.0 'discoveries' = {h2:3d} ({h2/M_NULL*100:.1f}%)   expected by chance = {M_NULL*0.0455:.1f}")
print(f"  |t|>3.0 'discoveries' = {h3:3d} ({h3/M_NULL*100:.1f}%)")
print(f"  Bonferroni 5% hurdle for M={M_NULL}: |t| > {NormalDist().inv_cdf(1-0.025/M_NULL):.2f}")
```
```
NULL zoo (M=300, T=480):
  |t|>2.0 'discoveries' =  13 (4.3%)   expected by chance = 13.7
  |t|>3.0 'discoveries' =   0 (0.0%)
  Bonferroni 5% hurdle for M=300: |t| > 3.76
```

The count lands on the theoretical value: 13 of 300 worthless characteristics clear the naive hurdle, and the Bonferroni threshold that would have kept the family-wise error at 5% is $|t|>3.76$. **Nothing here has any economic content, and yet a naive literature would publish 13 factors.**

```python
import math, random
from statistics import NormalDist

def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))
def tstat(xs): return mean(xs)/(sd(xs)/math.sqrt(len(xs)))

# --- B. MIXED ZOO: 100 candidates, 8 genuinely priced, 92 worthless ---
random.seed(707)
M, T, REAL = 100, 240, 8          # 8 real factors earning 0.4%/mo; 92 nulls
ts = []
for i in range(M):
    lam = 0.004 if i < REAL else 0.0
    ts.append(tstat([lam + random.gauss(0, 0.03) for _ in range(T)]))
d2 = [i for i in range(M) if abs(ts[i]) > 2.0]
d3 = [i for i in range(M) if abs(ts[i]) > 3.0]
print(f"MIXED zoo (M={M}, {REAL} truly priced, T={T}):")
print(f"  |t|>2.0 -> {len(d2):2d} discoveries, {sum(1 for i in d2 if i<REAL)} genuinely real  => false-discovery rate {(1-sum(1 for i in d2 if i<REAL)/len(d2))*100:3.0f}%")
print(f"  |t|>3.0 -> {len(d3):2d} discoveries, {sum(1 for i in d3 if i<REAL)} genuinely real")
# Benjamini-Hochberg FDR at q = 10%
pvals = sorted(2*(1-NormalDist().cdf(abs(t))) for t in ts)
rej = max([k for k, p in enumerate(pvals, 1) if p <= 0.10*k/M] or [0])
print(f"  BH-FDR at q=0.10 rejects {rej} of {M}  (the {REAL} true signals are not all detectable at T={T})")
```
```
MIXED zoo (M=100, 8 truly priced, T=240):
  |t|>2.0 -> 10 discoveries, 4 genuinely real  => false-discovery rate  60%
  |t|>3.0 ->  2 discoveries, 1 genuinely real
  BH-FDR at q=0.10 rejects 2 of 100  (the 8 true signals are not all detectable at T=240)
```

Two lessons the numbers force. **(i)** At the naive $|t|>2$ hurdle, **60% of the "discoveries" are fakes** — 6 spurious factors out of 10 published. **(ii)** Raising the hurdle to $t>3$ cuts the false positives to 1, but also discards several *real* factors: a weak genuine premium of 0.4%/month with 3% volatility gives $t\approx2.07$ over 20 years, so half the true signals simply are not distinguishable from noise at this sample length. **The zoo is not a collection of lies; it is a collection of underpowered truths and a comparable number of chance findings, and no single threshold separates them cleanly.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Publication bias and the file drawer.** The 300 nulls in experiment A were never written up; only the 13 "discoveries" were. A literature is a *censored* sample of the tests that were run, so its apparent $t$-distribution is a truncated one. This is why Harvey–Liu–Zhu's hurdle must be applied to the *number of tests attempted*, not the number published.
2. **Redundancy masquerading as breadth.** Five value factors are one factor plus four units of collinearity. Adding them to a portfolio raises gross exposure without raising independent expected return, and inflates the apparent Sharpe through correlation with the same bet (see [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03 · Crowding & Capacity]]).
3. **The `t>2` comfort blanket.** As experiment B shows, $|t|>2$ is simultaneously *too lax* (60% false discoveries) and, in a search, *meaningless* because the search itself was run at that threshold. The honest fixed point is: state how many configurations you tried, then apply the Deflated Sharpe / Bonferroni correction for that number.
4. **Nonstationarity defeats the backtest outright.** A characteristic validated in one era can be arbitraged away in the next. The statistical machinery here assumes the premium, if real, is *constant*; in practice it decays ([[pillars/01-quantitative-research/factor-investing-and-timing/04-post-publication-decay|04 · Post-Publication Decay]]), which is a further reason a high in-sample $t$ overstates the future.

---

### 5. Canonical Literature & Study References

- **Cochrane, John H.**, "Presidential Address: Discount Rates" (*JF*, 2011) §II.A–B — "a zoo of new factors"; the four questions; sorts vs regressions; the multidimensional challenge. *Verified against the corpus paper.*
- **Harvey, Campbell; Liu, Yan & Zhu, Heqing**, "... and the Cross-Section of Expected Returns" (*RFS*, 2016) — the multiple-testing critique; the $t>3$ hurdle. Corpus paper *28_harvey_2016_cross_section_expected_returns*.
- **Green, Jeremiah; Hand, John R. M. & Zhang, X. Frank**, "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns" (*RFS*, 2017) — the characteristic census (~100 candidates, ~24 independent). Corpus paper *49_Green_2017*.
- **Bailey, Borwein, López de Prado & Zhu**, "Pseudo-Mathematics and Financial Charlatanism" (*Notices of the AMS*, 2014) — the expected-maximum-Sharpe inflation $\sqrt{2\ln m}$; backtest overfitting. Corpus paper *42_bailey_2014*.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 18.7 — Bonferroni, Benjamini–Hochberg FDR, q-values; the machinery behind §2–§3. *Verified in the corpus.*
- **Tsay, Ruey S.**, *Analysis of Financial Time Series*, Ch 9 — factor-model families, factor-number selection. *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/factor-investing-and-timing/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/factor-investing-and-timing/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03 · Crowding & Capacity]] · [[pillars/01-quantitative-research/factor-investing-and-timing/04-post-publication-decay|04 · Post-Publication Decay]]
- Discipline: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (DSR, purged CV) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/06-advanced-extensions|The sibling folder's zoo page]] (q-factor, statistical consolidation)
- Statistical base: [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt Data]] (high-dimensional selection) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
