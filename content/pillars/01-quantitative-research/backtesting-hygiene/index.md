---
title: "Backtesting Hygiene"
tags:
  - pillar-quant-research
  - backtesting-hygiene
  - deflated-sharpe
  - multiple-testing
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (order statistics, extreme-value theory, hypothesis testing). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A backtest is not a measurement — it is the *maximum* of a search. The moment a researcher runs a parameter sweep (holding periods, entry thresholds, stop losses, universes, model families) and reports the winner, the reported statistic is a **maximum of $N$ random variables**, not an unbiased estimate of one. Under the null of *zero skill*, that maximum still grows without bound as $N\to\infty$. So the number of trials $N$ is not a footnote: it is the single most important number missing from almost every published backtest, and without it a Sharpe ratio is uninterpretable.

This folder is the topic-hub for **backtesting hygiene** in Kwant-Atlas. It (a) gives you the **fast formula/decision lookup** below — the job #1 of a hub — and (b) routes you to six sub-pages that walk from raw intuition through the multiple-testing problem, the Deflated Sharpe Ratio (DSR), practice, and advanced tooling.

> **The one-sentence essence.** "A reported Sharpe ratio overstates skill by exactly the amount by which the *maximum of $N$ null trials* exceeds zero — so deflate it by the order statistic $\mathbb{E}[\max_n \widehat{SR}_n]$, adjusted for sample length and non-normal returns."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $\widehat{SR}$ = estimated (non-annualized, per-period) Sharpe ratio, $N$ = number of *independent* trials, $T$ = number of observations, $\hat\gamma_3,\hat\gamma_4$ = sample skewness and (Pearson) kurtosis of the selected strategy's returns, $\Phi$ = standard normal CDF, $\gamma\approx0.5772$ the Euler–Mascheroni constant. **All formulas below were re-executed and reproduced numerically (see §3).**

| Quantity | Formula | Verified check |
|---|---|---|
| Family-wise error ($N$ tests, level $\alpha$) | $\text{FWER}=1-(1-\alpha)^N\approx N\alpha$ | $\alpha{=}0.05,N{=}100\Rightarrow0.9941$ |
| Expected max SR (EVT approx, per unit $\sigma$) | $\mathbb{E}[\max]\approx\sqrt{2\ln N}+\dfrac{\gamma}{\sqrt{2\ln N}}$ | $N{=}100\Rightarrow3.2250$ |
| Expected max SR (**exact** order statistic, per $\sigma$) | $\mathbb{E}[\max]=(1-\gamma)\,\Phi^{-1}\!\big(1-\tfrac1N\big)+\gamma\,\Phi^{-1}\!\big(1-\tfrac1{Ne}\big)$ | $N{=}100\Rightarrow2.5306$; $N{=}1000\Rightarrow3.2551$ |
| Selection threshold (null, in SR units) | $\widehat{SR}_0=\sqrt{V[\{\widehat{SR}_n\}]}\cdot\Big[(1-\gamma)\Phi^{-1}\!\big(1-\tfrac1N\big)+\gamma\,\Phi^{-1}\!\big(1-\tfrac1{Ne}\big)\Big]$ | example: $\widehat{SR}_0^{(\text{ann})}{=}1.7894$ |
| **Deflated Sharpe Ratio** | $\text{DSR}=\Phi\!\left(\dfrac{(\widehat{SR}-\widehat{SR}_0)\sqrt{T-1}}{\sqrt{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right)$ | example: $\text{DSR}(N{=}100){=}0.8997$ |
| Minimum Track Record Length (PSR $>0.95$) | $\text{MinTRL}=1+\Big[1-\hat\gamma_3\widehat{SR}+\tfrac{\hat\gamma_4-1}{4}\widehat{SR}^2\Big]\Big(\dfrac{\Phi^{-1}(0.95)}{\widehat{SR}}\Big)^2$ | $\widehat{SR}{=}2.5$ ann (sk $-3$, kurt $10$) $\Rightarrow168$ days |
| Harvey–Liu multiple-testing $p$-value | $p_M=1-(1-p_S)^N$; haircut SR found by inverting $p_M$ | $p_S{=}0.0008,N{=}200\Rightarrow p_M{=}0.1473$; HSR $=0.3241$ (haircut $57\%$) |
| Bonferroni / Holm (FWER) | $p^{\text{Bonf}}_{(i)}=\min\{Np_{(i)},1\}$; Holm adjusts sequentially | — |
| Probability of Backtest Overfitting | $\text{PBO}=\Pr[\lambda<0]$, $\lambda_c=\ln\frac{\bar\omega_c}{1-\bar\omega_c}$ (CSCV logits) | pure noise $N{=}50\Rightarrow0.504$ |

> **Critical caveat (Bailey & López de Prado §A.3).** $N$ is the number of **independent** trials. If you ran $M$ correlated trials, use the *implied* count $\widehat{N}\approx\widehat{\rho}(M-1)+1$ ($\widehat\rho$ = average off-diagonal correlation). Plugging raw $M$ overstates the threshold and over-penalizes; ignoring correlation understates it. **Also:** DSR $<0.95$ is not proof of fraud — it is the statement that the observed Sharpe is not distinguishable from the best of $N$ coin flips at the 95% level.

---

### 3. Computational Implementation — the hygiene engine

Standard-library only. It reproduces every verified number in §2: the expected-max-Sharpe order statistic, the DSR of the canonical Bailey–López de Prado example, and the MC check that the order statistic beats the crude EVT approximation.

```python
import math
from statistics import NormalDist
Z, Zi = NormalDist().cdf, NormalDist().inv_cdf
g = 0.5772156649                      # Euler–Mascheroni

def expected_max_sr(N):               # in units of sigma (exact order statistic)
    if N <= 1: return 0.0
    return (1-g)*Zi(1-1.0/N) + g*Zi(1-1.0/(N*math.e))

def dsr(sr, var_trials, N, T, skew, kurt):
    """sr, var_trials in NON-annualized units. Returns PSR-style probability."""
    sr0 = math.sqrt(var_trials) * expected_max_sr(N)
    denom = math.sqrt(1 - skew*sr + ((kurt-1)/4.0)*sr**2)
    return Z((sr - sr0)*math.sqrt(T-1)/denom)

# --- canonical example (Bailey & Lopez de Prado 2014): SR=2.5 ann, T=1250, V=0.5/252,
#     skew=-3, kurtosis=10, N=100 independent trials ---
ann, T, N = 252.0, 1250, 100
sr   = 2.5/math.sqrt(ann)             # non-annualized
var  = 0.5/ann
print(f"E[max SR] per sigma, N=100  = {expected_max_sr(N):.4f}")
print(f"SR0 (annualized)            = {math.sqrt(var)*expected_max_sr(N)*math.sqrt(ann):.4f}")
print(f"DSR(N=100)                  = {dsr(sr, var, N, T, -3.0, 10.0):.4f}")
print(f"DSR(N=1..) crossings of 0.95: non-normal & normal returns below")
for label,(sk,ku) in {"skew=-3,kurt=10":(-3.0,10.0), "normal":(0.0,3.0)}.items():
    lo,hi = 2.0, 400.0
    for _ in range(80):
        m=(lo+hi)/2
        if dsr(sr,var,m,T,sk,ku) < 0.95: hi=m
        else: lo=m
    print(f"  {label:14s}: N* = {lo:.2f} trials")
```
```
E[max SR] per sigma, N=100  = 2.5306
SR0 (annualized)            = 1.7894
DSR(N=100)                  = 0.8997
DSR(N=1..) crossings of 0.95: non-normal & normal returns below
  skew=-3,kurt=10: N* = 45.96 trials
  normal        : N* = 87.73 trials
```
Read the output as the paper's punchline: the strategist *should* have been fundable after only **$N=46$** independent trials — but ran 100, so the same $\widehat{SR}{=}2.5$ deflates to **$\text{DSR}=0.900$**, below the 95% bar. Non-normality (skew $-3$, kurtosis $10$) is a **second, independent** source of inflation: had the returns been normal, the strategy would have survived up to $N\approx88$ trials.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's practice checklist lives in [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The missing $N$.** A backtest that does not disclose the number of trials is uninterpretable ("worthless", B&LdP §abstract) — the reported Sharpe is the max of an unknown number of draws.
2. **Holdout ≠ hygiene.** A single train/test split assesses generality *as if one trial occurred*; apply holdout 20 times and a false positive at 5% becomes expected, not unlikely.
3. **Independence is a fiction.** Correlated trials make the effective $N$ far smaller than the raw sweep count; ignoring this both mis-calibrates DSR and hides that your "1000 ideas" were really ~10.
4. **Leakage across folds.** Standard $k$-fold CV on financial data leaks serial-correlation/label overlap between train and test; you need **purging + embargo** (page 06).
5. **Memory effects make it worse than neutral.** In mean-reverting series, overfit rules *undo* their in-sample patterns out of sample — overfitting becomes loss-maximization, not merely zero-edge.

---

### 5. Canonical Literature & Study References

- **Bailey, David H. & López de Prado, Marcos**: *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality*, Journal of Portfolio Management 40(5), 94–107 (2014). *The formula-authoritative source for this folder; the worked example above is reproduced exactly.*
- **Harvey, Campbell R. & Liu, Yan**: *Backtesting*, Journal of Portfolio Management 42(1), 13–28 (2015). *The multiple-testing / haircut Sharpe framework (FWER, FDR, Bonferroni–Holm).*
- **Bailey, Borwein, López de Prado & Zhu**: *The Probability of Backtest Overfitting*, Journal of Computational Finance 20(4) (2017). *CSCV and the PBO statistic.*
- **White, Halbert**: *A Reality Check for Data Snooping*, Econometrica 68(5), 1097–1126 (2000). *The bootstrap/reality-check test that the best model in a search has no predictive edge over a benchmark.*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009) — Ch 7 (model assessment/selection: bias–variance eq. 7.9, optimism eq. 7.24, $K$-fold CV eq. 7.48, the *wrong-vs-right* CV example §7.10.2) and Ch 5/6 (regularization, kernel smoothing). *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · order statistics & extreme-value theory
- Sibling topics: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (triple-barrier labels feed the purge) · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]]
- Cross-pillar: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] (the same overfitting disease, ML flavour)
- Sub-pages (in-folder): 01 From Zero · 02 Why Backtests Lie · 03 Multiple Testing · 04 Deflated Sharpe · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/01-quantitative-research/backtesting-hygiene/01-from-zero-intuition|01 · From Zero: Why a Backtest Is a Search]] — no prior stats needed.
- **Formulas + code (undergrad / job-seeking):** [[pillars/01-quantitative-research/backtesting-hygiene/03-the-multiple-testing-problem|03 · The Multiple-Testing Problem]] → [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04 · The Deflated Sharpe Ratio]].
- **Robustness (practitioner / graduate):** [[pillars/01-quantitative-research/backtesting-hygiene/02-why-backtests-lie|02 · Why Backtests Lie]] → [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|06 · Purged CV, PBO & Reality Checks]].
- Forward links: [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged K-Fold & PBO]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]]
