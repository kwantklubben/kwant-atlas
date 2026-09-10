---
title: "04 — Evaluating Signal: IC, ICIR, Decay & the Research Protocol"
tags:
  - pillar-machine-learning
  - alternative-data-pipelines-and-evaluation
  - information-coefficient
  - signal-decay
  - evaluation
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/03-the-pipeline|03 · The Pipeline]] (you need a point-in-time feature first) and [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]].

---

### 1. Intuition & Practical Objective

You have a clean, point-in-time feature. Now the only question that matters: **does it actually predict returns, or am I fooling myself?** This page is the **research protocol** — the sequence of statistics a serious desk computes before capital is committed — and the math behind each. The objective is to answer "is there signal here?" with numbers that *cannot* be manufactured by leakage, and to translate a signal into the portfolio language of breadth and IR.

The protocol, in order (each step can veto the dataset):

1. **Information Coefficient (IC)** — the cross-sectional correlation between the signal and the next-period return. Use **rank IC** (Spearman) to be robust to outliers.
2. **ICIR and $t$-statistic** — the *consistency* of that IC across periods. A $0.05$ IC that varies wildy is worthless; a $0.03$ IC that is stable is a business.
3. **Decay curve** — IC as a function of forecast horizon, fit to $\text{IC}(h)\approx\text{IC}_0 e^{-\lambda h}$ to get the **half-life** and decide the rebalance frequency.
4. **Residual (orthogonalized) IC** — IC *after* removing existing factors; the part you don't already trade.
5. **Out-of-sample** — repeat 1–4 under purged/embargoed CV ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]]), and deflate for the number of datasets you tried.

> **The one-sentence essence.** "A dataset has signal iff its cross-sectional correlation with forward returns is *mean-positive, consistent across periods, and survives orthogonalization and honest out-of-sample testing* — and the quantity you trade is not the IC but $\text{ICIR}\sqrt{\text{breadth}}$."

---

### 2. Mathematical Ground Truth & Derivations

**The Information Coefficient.** For each period $p$ with $N$ names,

$$\text{IC}_p=\operatorname{corr}\big(x_i^{(p)},\,y_i^{(p)}\big),\qquad
\text{rank-IC}_p=\operatorname{Pearson}\big(\operatorname{rank}(x^{(p)}),\operatorname{rank}(y^{(p)})\big)\ \ (\text{Spearman}).$$

**Consistency: ICIR and $t$-stat.** Over $P$ periods, with $\overline{\text{IC}}$ the mean and $\sigma_{\text{IC}}$ the standard deviation,

$$\text{ICIR}=\frac{\overline{\text{IC}}}{\sigma_{\text{IC}}},\qquad
t=\text{ICIR}\sqrt{P}=\frac{\overline{\text{IC}}}{\sigma_{\text{IC}}}\sqrt{P}.$$

Under iid periods, $\text{IC}_p$ has standard error $\approx1/\sqrt{N}$ *within* a period and $\sigma_{\text{IC}}/\sqrt P$ *across* periods; with overlapping forward returns you need a **Newey–West** correction to $t$ (López de Prado, AFML Ch. 8, on the deflated Sharpe / multiple testing).

**Decay estimation by log-linear regression.** If $\text{IC}(h)=\text{IC}_0 e^{-\lambda h}$ then

$$\ln \text{IC}(h)=\ln\text{IC}_0-\lambda h,$$

so an OLS of $\ln\text{IC}(h)$ on $h$ gives $\hat\lambda$ (slope) and $\widehat{\text{IC}_0}=e^{\text{intercept}}$; the half-life is $t_{1/2}=\ln 2/\hat\lambda$. **Estimate $\lambda$ on *smoothed, positive* ICs and report the fit quality** — the exponential is a first-order model.

**From IC to IR.** $\;\text{IR}=\text{ICIR}\cdot\sqrt{B_{\text{eff}}}\;$ where $B_{\text{eff}}$ is the effective number of independent bets; equivalently the Fundamental Law $\text{IR}=\text{IC}\sqrt{B}\text{TC}$ ([[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/02-alt-data-landscape|02 · Alt-Data Landscape]]).

**Why "just look at the IC" lies.** With $N$ names, the *sampling* std of a single-period IC is $\approx1/\sqrt N$: at $N{=}60$ that is $0.13$ — an order of magnitude larger than a typical signal. You must average over many periods and names, and the only honest average is out of sample.

---

### 3. Computational Implementation — the protocol on a synthetic dataset

numpy only. Part 1 runs the IC/ICIR/t-stat battery on a signal with a *known* true IC of $0.05$; Part 2 generates ICs across horizons and recovers the decay rate by log-linear fit. Both are the exact statistics you would compute on a real vendor feed.

```python
import numpy as np

rng = np.random.default_rng(5)
# --- 1) Cross-sectional IC time series -> ICIR & t-stat ---
P, Nx = 252, 250          # 252 periods, 250 names
TRUE_IC = 0.05
ics = []
for _ in range(P):
    x = rng.normal(size=Nx)
    y = TRUE_IC * x + rng.normal(size=Nx)
    xc, yc = x - x.mean(), y - y.mean()
    ics.append(float((xc*yc).sum()/np.sqrt((xc**2).sum()*(yc**2).sum())))
ics = np.array(ics)
mean_ic, std_ic = ics.mean(), ics.std(ddof=1)
icir = mean_ic/std_ic
print("Cross-sectional IC evaluation (252 periods x 250 names)")
print(f"  mean IC   = {mean_ic:+.4f}   (true {TRUE_IC:.3f})")
print(f"  IC std    = {std_ic:.4f}     (theory 1/sqrt(N) = {1/np.sqrt(Nx):.4f})")
print(f"  ICIR      = {icir:.4f}")
print(f"  t-stat    = {icir*np.sqrt(P):.2f}   (needs |t|>2)")

# --- 2) Signal decay: IC(h) = IC0*exp(-lam h); fit log IC(h) vs h ---
TRUE_LAM, IC0 = 0.12, 0.06
horizons = np.arange(1, 16)
ic_h = np.array([IC0*np.exp(-TRUE_LAM*h) + rng.normal(0, 0.0015) for h in horizons])
m = ic_h > 0
slope, intercept = np.polyfit(horizons[m], np.log(ic_h[m]), 1)
lam_hat = -slope
print("\nDecay estimation (fit log IC(h) vs horizon h)")
print(f"  true lambda   = {TRUE_LAM:.4f}/period -> half-life {np.log(2)/TRUE_LAM:.2f}")
print(f"  fitted lambda = {lam_hat:.4f}/period -> half-life {np.log(2)/lam_hat:.2f}")
print(f"  fitted IC0    = {np.exp(intercept):.4f}  (true {IC0:.3f})")
print("  IC(h) at h=1,5,10,15: " + ", ".join(f"{ic_h[h-1]:.4f}" for h in (1,5,10,15)))
```
```
Cross-sectional IC evaluation (252 periods x 250 names)
  mean IC   = +0.0566   (true 0.050)
  IC std    = 0.0616     (theory 1/sqrt(N) = 0.0632)
  ICIR      = 0.9190
  t-stat    = 14.59   (needs |t|>2)

Decay estimation (fit log IC(h) vs horizon h)
  true lambda   = 0.1200/period -> half-life 5.78
  fitted lambda = 0.1175/period -> half-life 5.90
  fitted IC0    = 0.0600  (true 0.060)
  IC(h) at h=1,5,10,15: 0.0553, 0.0321, 0.0154, 0.0098
```

Read it. The measured mean IC ($+0.0566$) sits within sampling error of the true $0.05$, and the **actual per-period IC standard deviation ($0.0616$) matches the theoretical $1/\sqrt N=0.0632$** — a single period's IC is nearly all noise, which is why you need $P$ periods and a $t$-stat. Here $\text{ICIR}=0.919$ and $t=14.59$, decisively significant. The decay fit recovers $\hat\lambda=0.1175$ against the true $0.12$ (half-life $5.90$ vs $5.78$) and $\widehat{\text{IC}_0}=0.0600$ exactly — **the protocol reads the true signal parameters out of noisy data.** On a *real* dataset this is the moment you learn both whether there is signal and *how fast you must trade it*.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading a single-period IC.** One period's IC is noise-dominated ($\text{std}\approx1/\sqrt N$). Reporting "the IC was 0.12" from one month is reporting a draw, not a property. Always report $\overline{\text{IC}}$, ICIR, and $t$.
2. **Overlapping horizons inflate $t$.** ICs computed from overlapping forward returns are autocorrelated, so the naive $t=\text{ICIR}\sqrt P$ overstates significance. Use Newey–West / block bootstrap, and count *non-overlapping* effective periods.
3. **Raw IC hides redundancy.** A dataset with great raw IC that is 0.9-correlated with your existing model adds nothing; always compute the **residual** IC ([[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/06-advanced-extensions|06 · Advanced Extensions]]).
4. **Testing thousands of datasets and reporting the winner.** The evaluation is itself a search; the $t$-stat of the *best of $K$* trials is not the $t$-stat of one trial. Deflate for $K$ (multiple-testing / deflated Sharpe — [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).
5. **In-sample decay fits.** Fitting $\lambda$ on the same data you select the horizon on overfits the half-life; validate the chosen rebalance frequency out of sample.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning* — **Ch. 8** (feature importance, PSR/DSR and the multiple-testing correction to a Sharpe/IC $t$-stat), **Ch. 7** (purged CV so the IC is measured out of sample), **Ch. 11** (backtest errors). *Corpus PDF verified.*
- **Grinold, Richard C. & Kahn, Ronald N.**: *Active Portfolio Management* (2nd ed.) — IC, ICIR, breadth, and the translation of a signal into IR (Ch. 6).
- **Bailey, David H. & López de Prado, Marcos**: "The Deflated Sharpe Ratio" (*Journal of Portfolio Management*, 2014) and "The Probability of Backtest Overfitting" (*Journal of Computational Finance*, 2017) — the corrections for selection bias when many signals are tested.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch. 7 — the generalisation-error framework behind honest evaluation. *Corpus available.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/03-the-pipeline|03 · The Pipeline]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/06-advanced-extensions|06 · Advanced Extensions]]
- The leak-proof harness for step 5: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
- Noise floor of the target: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]]
