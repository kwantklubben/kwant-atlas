---
title: "1.2.4 The Deflated Sharpe Ratio"
tags:
  - pillar-quant-research
  - backtesting-hygiene
  - deflated-sharpe
  - probabilistic-sharpe
  - selection-bias
  - non-normality
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/backtesting-hygiene/03-the-multiple-testing-problem|03 · The Multiple-Testing Problem]] (expected maximum Sharpe) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

A raw Sharpe ratio conflates two very different claims: *(i)* "this strategy made money relative to its risk" and *(ii)* "this strategy is statistically distinguishable from luck". The **Probabilistic Sharpe Ratio (PSR)** answers (ii) for a *single* trial. The **Deflated Sharpe Ratio (DSR)** answers it after admitting that the strategy was selected as the best of $N$ trials - and that its returns are not normal.

The practical objective: turn a strategy's reported Sharpe, sample length, skew/kurtosis, and the number of trials into **one number in $[0,1]$** - the probability that the true Sharpe exceeds the selection-bias-adjusted threshold $\widehat{SR}_0$. Pass/fail conventions: **$\text{DSR}\ge0.95$ = significant at 95%**, i.e. the strategy is *not* explainable as the best of $N$ null flukes.

> **The one-line essence.** "DSR is a PSR whose rejection threshold is *raised* to the height expected of the maximum of $N$ zero-skill trials: $\widehat{SR}_0=\sqrt{V[\{\widehat{SR}_n\}]}\,\mathbb{E}[\max_n Z_n]$, and whose standard error is *widened* by skewness and kurtosis."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Probabilistic Sharpe Ratio (single trial)

The Sharpe estimator's variance under non-normal returns (Lo 2002; Bailey & López de Prado 2012) is
$$
\widehat{\mathrm{Var}}[\widehat{SR}]=\frac{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}{T-1},
$$
where $\hat\gamma_3$ is skewness and $\hat\gamma_4$ is **Pearson** kurtosis ($=3$ for normal). Hence, against a user-chosen benchmark $\widehat{SR}^{\ast}$,
$$
\text{PSR}(\widehat{SR}^{\ast})=\Phi\!\left(\frac{(\widehat{SR}-\widehat{SR}^{\ast})\sqrt{T-1}}{\sqrt{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right).
$$
Note the **non-normality penalty**: negative skew *inflates* the denominator (raises the bar); fat tails (kurtosis $>3$) do the same. Two strategies with identical Sharpe but different higher moments get different PSRs.

#### 2.2 The Deflated Sharpe Ratio

Replace the arbitrary benchmark by the **expected maximum under the null** of $N$ trials: $\widehat{SR}^{\ast}\to\widehat{SR}_0$ with
$$
\boxed{\ \widehat{SR}_0=\sqrt{V[\{\widehat{SR}_n\}]}\cdot\Big[(1-\gamma)\,\Phi^{-1}\!\Big(1-\tfrac1N\Big)+\gamma\,\Phi^{-1}\!\Big(1-\tfrac1{Ne}\Big)\Big]\ }
$$
and define
$$
\boxed{\ \text{DSR}=\Phi\!\left(\frac{(\widehat{SR}-\widehat{SR}_0)\sqrt{T-1}}{\sqrt{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right).\ }
$$
Everything is in **non-annualized (per-period) units** - DSR is scale-invariant only if $T$ matches the return frequency and $\widehat{SR}$, $\widehat{SR}_0$ share the period.

**What DSR adds over a raw Sharpe** - five extra inputs, each of which can only *lower* significance:
1. $N$ - the number of independent trials (raises $\widehat{SR}_0$),
2. $V[\{\widehat{SR}_n\}]$ - how dispersed the trials were (scales $\widehat{SR}_0$),
3. $T$ - sample length (longer = more certain),
4. $\hat\gamma_3,\hat\gamma_4$ - non-normality (widens the denominator).

#### 2.3 Minimum Track Record Length

Inverting DSR $=1-\alpha$ for the required sample length (PSR threshold) gives the **MinTRL**:
$$
\text{MinTRL}=1+\Big[1-\hat\gamma_3\widehat{SR}+\tfrac{\hat\gamma_4-1}{4}\widehat{SR}^2\Big]\left(\frac{\Phi^{-1}(1-\alpha)}{\widehat{SR}}\right)^2.
$$
It answers "how long must this track record be before it is significant?" - and it *grows* with negative skew and fat tails, the empirical signature of option-selling and carry strategies.

---

### 3. Computational Implementation - DSR end-to-end

Stdlib only. Reproduces the canonical Bailey & López de Prado worked example, sweeps $N$, contrasts normal vs non-normal returns, and computes MinTRL.



Read the story: a strategy with an annualized Sharpe of **2.5** over 5 years is only fundable if it survived **at most ~46 trials** ($\text{DSR}=0.950$). At the **100** trials it actually survived, **$\text{DSR}=0.900$** - below the 95% bar. The **normal-returns** column isolates the second source of inflation: holding $N$ fixed, non-normality (skew $-3$, kurt $10$) costs ~4 percentage points of DSR at $N{=}100$ (0.942 $\to$ 0.900). MinTRL shows the flip side: a Sharpe-2.5 record needs only ~110 days (~0.44 yr) *ignoring* non-normality, stretched to ~168 days (0.7 yr) once skew $-3$ / kurt $10$ are priced in - negative skew is expensive.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Unit mismatch.** DSR mixes $T$, $\widehat{SR}$, $\widehat{SR}_0$, and $V[\{\widehat{SR}_n\}]$; all must be in the **same (per-period) units**. Annualizing some but not others is the classic implementation bug (annualize the final threshold, not the inputs).
2. **Kurtosis convention.** The formula uses **Pearson** kurtosis ($3$ for normal). Passing excess kurtosis ($0$ for normal) silently biases DSR; `scipy.stats.kurtosis(..., fisher=False)` is the safe call.
3. **$V[\{\widehat{SR}_n\}]$ ignored or guessed.** $V$ is the *variance of the trial Sharpes*, not the strategy's own variance. Using the strategy's return variance is a category error; using a made-up $V$ is unverifiable.
4. **$N$ understated.** Every dependent/derived trial counts (page 03). Understating $N$ makes DSR *too* generous - the exact failure DSR exists to prevent.
5. **Threshold mis-read.** $\text{DSR}=0.90$ does **not** prove fraud; it says the result is not distinguishable from the best of $N$ flukes at 95%. Conversely $\text{DSR}\ge0.95$ is necessary, not sufficient - it says nothing about costs, capacity, or decay.
6. **Short samples + fat tails.** Both inflate the standard error; a 6-month record with kurtosis 12 can never reach DSR 0.95 regardless of Sharpe. MinTRL tells you this before you deploy.

---

### 5. Canonical Literature & Study References

- **Bailey, D. H. & López de Prado, M.**: *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality*, JPM 40(5), 94–107 (2014) - eqs. (1)–(2); §"A numerical example" (the example reproduced above: annualized $\widehat{SR}{=}2.5$, $T{=}1250$, $V[\{\widehat{SR}_n\}]$, skew $-3$, kurtosis $10$, $N{=}100$; the paper reports the $N{=}46$ crossing and the normal-returns $N{=}88$ crossing, both matched here). *The formula-authoritative source.*
- **Bailey, D. H. & López de Prado, M.**: *The Sharpe Ratio Efficient Frontier*, Journal of Risk 15(2) (2012) - the PSR and MinTRL.
- **Lo, A.**: *The Statistics of Sharpe Ratios*, Financial Analysts Journal 58(4) (2002) - the non-normal variance of the Sharpe estimator.
- **Ingersoll, Spiegel, Goetzmann & Welch**: *Portfolio Performance Manipulation and Manipulation-Proof Performance Measures*, RFS 20(5) (2007) - why higher moments matter for performance claims.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/backtesting-hygiene/03-the-multiple-testing-problem|03 · Multiple Testing]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|06 · Purged CV, PBO & Reality Check]]
- Siblings: [[pillars/01-quantitative-research/backtesting-hygiene/02-why-backtests-lie|02 · Why Backtests Lie]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (triple-barrier labels drive the skew that DSR penalizes)
