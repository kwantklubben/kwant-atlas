---
title: "1.2.3 The Multiple-Testing Problem"
tags:
  - pillar-quant-research
  - backtesting-hygiene
  - multiple-testing
  - extreme-value-theory
  - haircut-sharpe
  - data-snooping
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (order statistics, extreme-value distributions) and [[pillars/01-quantitative-research/backtesting-hygiene/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Test one hypothesis at the 5% level and you have a 5% chance of a false positive. Test **100** and the chance that *at least one* is a false positive — under the null of no skill anywhere — is **99.4%**. This is the **multiple-testing problem**, and it is not a subtle statistical caveat: it is the arithmetic reason a large theory-free parameter sweep is guaranteed to "find" something.

The practical objective of this page is to put a **number** on the bar a backtest must clear once you admit how many trials it survived. Two equivalent framings:

- **Extreme-value framing (Bailey & López de Prado):** the reported Sharpe is $\max_n\widehat{SR}_n$; its expected value under the null is a known **order statistic** of $N$ draws. (→ feeds the DSR, page 04.)
- **$p$-value framing (Harvey & Liu / White):** the single-test $p$-value $p_S$ must be inflated to a multiple-testing $p_M$ that reflects the search. (→ the **haircut Sharpe**.)

Both answer "how high does the bar go?", and they agree in spirit: the bar rises with $N$, slowly (logarithmically) but without limit.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Family-wise error rate (FWER)

With $N$ independent tests at level $\alpha$,
$$
\text{FWER}=1-(1-\alpha)^N\approx N\alpha\ \ (\alpha\ \text{small}).
$$
So $\alpha{=}0.05$: $N{=}10\Rightarrow0.401$, $N{=}100\Rightarrow0.994$, $N{=}1000\Rightarrow1.000$. **Bonferroni** controls FWER by inflating each $p$: $p^{\text{Bonf}}_{(i)}=\min\{Np_{(i)},1\}$; **Holm** applies the same idea sequentially, $p^{\text{Holm}}_{(i)}=\min\{1,\max_{j\le i}[(N-j+1)p_{(j)}]\}$, and is uniformly more powerful. For thousands of tests FWER is too conservative, and the **false-discovery-rate** (Benjamini–Hochberg) controls instead the *proportion* of false rejections among the rejected (Harvey & Liu §"multiple testing framework").

#### 2.2 Expected maximum Sharpe under $N$ null trials

Let $\{\widehat{SR}_n\}$ be $N$ i.i.d. trial Sharpe estimates with mean $\mu$ and variance $V[\{\widehat{SR}_n\}]=\sigma^2$ (in per-period units). Standardize: $Z_n=(\widehat{SR}_n-\mu)/\sigma$. The expected maximum of $N$ standard normals has two standard forms:

**EVT approximation** (loose, ubiquitous):
$$
\mathbb{E}\big[\max_n Z_n\big]\approx\sqrt{2\ln N}+\frac{\gamma}{\sqrt{2\ln N}},\qquad \gamma\approx0.5772.
$$

**Exact order-statistic form** (used by the DSR):
$$
\mathbb{E}\big[\max_n Z_n\big]=(1-\gamma)\,\Phi^{-1}\!\Big(1-\tfrac1N\Big)+\gamma\,\Phi^{-1}\!\Big(1-\tfrac1{Ne}\Big).
$$

The selection threshold in Sharpe units is then
$$
\widehat{SR}_0=\mu+\sigma\cdot\mathbb{E}\big[\max_n Z_n\big],\qquad \text{under } H_0:\ \mu=0\Rightarrow \widehat{SR}_0=\sqrt{V[\{\widehat{SR}_n\}]}\cdot\mathbb{E}\big[\max_n Z_n\big].
$$

**The approximation is not innocent.** The crude EVT form *overstates* the true expected maximum by ~28% at $N{=}100$ (3.225 vs 2.531) — using it makes you over-penalise a good strategy. Monte Carlo settles which is right (see §3). The order-statistic version is the one to use.

#### 2.3 The Harvey–Liu haircut

Transform Sharpe to a $t$-statistic, $t=\widehat{SR}\cdot\sqrt T$ (net of any factor adjustment, $SR$ non-annualized). Compute the single-test two-sided $p$-value $p_S=\Pr(|r_{T-1}|>t)$. Under $N$ independent tests the multiple-testing $p$-value is
$$
p_M=1-(1-p_S)^N.
$$
The **haircut Sharpe** $HSR$ is found by equating a *single* test's $p$-value to $p_M$: solve $\Pr(|r_{T-1}|>t^\ast)=p_M$ and set $HSR=t^\ast/\sqrt T$. Because $p_M\gg p_S$, $HSR\ll\widehat{SR}$. Harvey & Liu's rule: the haircut is **non-linear** — very high Sharpes are barely penalised, marginal ones are heavily penalised (a flat 50% is wrong in both directions).

#### 2.4 How many trials are *optimal*? The 1/e-law

Since each added trial raises the false-positive floor, there is an optimal stopping rule (the "secretary problem", Bruss 1984): **sample a random $\tfrac1e\approx37\%$ of the theory-justified configurations, measure them, then keep drawing one at a time until one beats all previous — take it.** Every further trial *after* that is pure overfitting. Theory, not compute, should choose the search.

#### 2.5 Independent vs effective $N$

$N$ is the count of **independent** trials. If you ran $M$ correlated trials with average off-diagonal correlation $\widehat\rho$, the implied independent count is
$$
\widehat N\approx\widehat\rho\,(M-1)+1.
$$
Using raw $M$ overstates the threshold; treating correlated trials as independent understates it. **Report the full sweep $M$ and an estimate of $\widehat\rho$** — a strategy found among 1,000 correlated variants is often really ~10 independent bets (Bailey & López de Prado §A.3).

---

### 3. Computational Implementation — the three numbers

Stdlib only. (1) The expected-maximum table with Monte Carlo verification, (2) the Harvey–Liu haircut, (3) FWER and Bonferroni.

```python
import math, random
from statistics import NormalDist
Z, Zi = NormalDist().cdf, NormalDist().inv_cdf
g = 0.5772156649

# --- 1. Expected max Sharpe under N independent null trials (in units of sigma) ---
def evt_max(N):
    if N <= 1: return 0.0
    L = 2*math.log(N); return math.sqrt(L) + g/math.sqrt(L)
def exact_max(N):
    if N <= 1: return 0.0
    return (1-g)*Zi(1-1.0/N) + g*Zi(1-1.0/(N*math.e))
print("N      EVT approx   exact order-stat   MC (20k reps)")
random.seed(7)
for N in (1,10,100,1000):
    if N == 1: mc = 0.0
    else:
        s = 0.0; R = 20000
        for _ in range(R): s += max(random.gauss(0,1) for _ in range(N))
        mc = s/R
    print(f"{N:5d}   {evt_max(N):8.4f}     {exact_max(N):8.4f}        {mc:8.4f}")

# --- 2. Harvey-Liu haircut: annual SR 0.75, T=240 months, N=200 ---
Tm, SRann, N = 240, 0.75, 200
SRm = SRann/math.sqrt(12); t = SRm*math.sqrt(Tm)
pS = 2*(1-Z(t)); pM = 1-(1-pS)**N
HSRann = (Zi(1-pM/2)/math.sqrt(Tm))*math.sqrt(12)
print(f"\nt={t:.4f}  pS={pS:.5f}  pM=1-(1-pS)^N={pM:.4f}")
print(f"haircut Sharpe (ann)={HSRann:.4f}  haircut={100*(1-HSRann/SRann):.1f}%")

# --- 3. FWER and Bonferroni ---
print("\nFWER(a=0.05):", ", ".join(f"N={N}:{1-(1-0.05)**N:.4f}" for N in (1,10,100,1000)))
pv=[0.005,0.009,0.0128,0.0135,0.045,0.06]; M=len(pv)
print("raw p     :", pv)
print("Bonferroni:", [round(min(M*p,1),4) for p in pv])
```
```
N      EVT approx   exact order-stat   MC (20k reps)
    1     0.0000       0.0000          0.0000
   10     2.4149       1.5746          1.5404
  100     3.2250       2.5306          2.5071
 1000     3.8722       3.2551          3.2433

t=3.3541  pS=0.00080  pM=1-(1-pS)^N=0.1473
haircut Sharpe (ann)=0.3241  haircut=56.8%

FWER(a=0.05): N=1:0.0500, N=10:0.4013, N=100:0.9941, N=1000:1.0000
raw p     : [0.005, 0.009, 0.0128, 0.0135, 0.045, 0.06]
Bonferroni: [0.03, 0.054, 0.0768, 0.081, 0.27, 0.36]
```
Three readings: **(1)** the exact order statistic tracks Monte Carlo (2.531 vs 2.507 at $N{=}100$) while the EVT approximation overshoots (3.225) — *use the exact form*. **(2)** An honest-looking annual Sharpe of **0.75** over 20 years is cut to **0.32** (a **57%** haircut) once $N{=}200$ trials are acknowledged — closely matching the "50% discount" folklore, but *derived* rather than assumed. **(3)** Bonferroni's adjusted $p$-values reproduce Harvey & Liu's textbook sequence exactly (only the first of six "discoveries" survives), and FWER at $N{=}100$ is 99.4%.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Counting trials you can remember.** The denominator $N$ must include *every* configuration evaluated, including the exploratory ones you "weren't really serious about". Pre-register the search to know $N$.
2. **Treating correlated trials as independent.** Position sizing, stops, and filters applied onto one base signal produce thousands of *dependent* trials. Use $\widehat N=\widehat\rho(M-1)+1$.
3. **Using the EVT approximation.** $\sqrt{2\ln N}+\gamma/\sqrt{2\ln N}$ over-penalizes by ~28% at $N{=}100$. For DSR the exact order statistic is the correct bar.
4. **FWER when you don't need it.** With thousands of tests, Bonferroni virtually never rejects; FDR (Benjamini–Hochberg) is the appropriate error rate and is what Harvey–Liu advocate for factor zoos.
5. **Treating $p_M$ as a final verdict.** A non-rejection is not proof of falsehood; it is the statement that the result is not distinguishable from the best of $N$ flukes. Combine with DSR, PBO, and economics.
6. **Endless testing.** Once the optimal-stopping point is passed, additional trials *guarantee* inflation — the secretary-problem $1/e$ rule is a hard discipline, not a suggestion.

---

### 5. Canonical Literature & Study References

- **Bailey, D. H. & López de Prado, M.**: *The Deflated Sharpe Ratio* (2014), §"Expected Sharpe ratios under multiple trials", eqs. (1)–(2), and Appendix 1 (the order-statistic derivation), Appendix 3 (implied independent trials $\widehat N$). *The expected-max formula and its MC verification.*
- **Harvey, C. R. & Liu, Y.**: *Backtesting*, JPM (2015), §"Method", §"Multiple testing framework" — eqs. (1)–(5): the t↔Sharpe link, $p_M=1-(1-p_S)^N$, the haircut Sharpe $HSR$, and the Bonferroni/Holm/FDR trio.
- **White, H.**: *A Reality Check for Data Snooping*, Econometrica 68(5) (2000) — the bootstrap test that the best model in a search has no edge (page 06).
- **Bruss, F. T.**: *A Unified Approach to a Class of Best Choice Problems*, Annals of Probability 12(3) (1984) — the $1/e$-law / secretary problem as the optimal trial count.
- **Bonferroni / Holm / Benjamini–Hochberg** — the classical multiple-testing procedures (see Harvey & Liu references).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/backtesting-hygiene/02-why-backtests-lie|02 · Why Backtests Lie]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04 · The Deflated Sharpe Ratio]] (the order statistic becomes the DSR threshold) → [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|06 · PBO & Reality Check]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · Cross-pillar: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]]
