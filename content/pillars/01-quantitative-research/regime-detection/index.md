---
title: "Regime Detection"
tags:
  - pillar-quant-research
  - regime-detection
  - markov-switching
  - hmm
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity, ARMA, forecasting) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation, Markov chains, Bayes' rule). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Markets do not sit in one statistical state. Sometimes they grind upward with calm, low-volatility returns (bull); sometimes they fall hard with spiking volatility (bear); sometimes vol rises without direction (regime). If the data-generating process for returns **changes regime**, then a single unconditional mean/vol fit is wrong for *both* regimes, and — worse — a strategy tuned on calm data is fragile exactly when turbulence arrives. **Regime detection is the discipline of learning the regime from the data and knowing which regime you are in right now.**

This folder is the topic-hub for **regime detection** in Kwant-Atlas. It (a) gives the **fast formula lookup** below — job #1 of a hub — and (b) routes to six sub-pages that walk from raw intuition, through Markov-switching models (Hamilton), threshold models (SETAR/STAR), hidden Markov models (HMM), the failure modes (label switching, overfitting regimes, persistence), and regime-aware allocation.

> **The one-sentence essence.** "Regimes are *latent* — you never observe bull/bear directly, only noisy returns — so the entire machinery is a **recursive Bayes exercise**: maintain a probability distribution over the hidden regime, update it with each new return, and estimate the regime parameters (means, vols, transition probabilities) by maximum likelihood via the Hamilton filter (or EM for the HMM)."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Hamilton (1989), Tsay Ch 4 (Markov switching / SETAR / STAR) and Tsay Ch 11–12 (state-space / MCMC), and cross-checked against the verified corpus. Numbers in the check column were **re-executed and reproduced exactly** from the working Python in §3 and the sub-pages.

**Notation:** $s_t\in\{0,1\}$ latent regime; $P_{ij}=\mathbb{P}[s_t=j\mid s_{t-1}=i]$ transition probability (rows $i$, columns $j$); $\mu_j,\sigma_j$ regime-conditional mean/vol of returns $y_t$; $\hat{\xi}_{t\mid t}=\mathbb{P}[s_t\mid y_1,\dots,y_t]$ the filtered state distribution; $n(x)$ the standard-normal density.

| Quantity | Formula | Verified check |
|---|---|---|
| Transition matrix (2-state) | $P=\begin{pmatrix}P_{00} & P_{01}\\ P_{10} & P_{11}\end{pmatrix}$, rows sum to $1$ | — |
| Stationary distribution | $\pi_0=\dfrac{1-P_{11}}{2-P_{00}-P_{11}},\;\pi_1=1-\pi_0$ | Hamilton params $\Rightarrow\pi_{\text{exp}}=0.720$ |
| **Expected regime duration** | $\mathbb{E}[\text{stay in }i]=\dfrac{1}{1-P_{ii}}$ | expansion $10.52$ qtr, recession $4.08$ qtr (paper $10.5$, $4.1$) |
| Hamilton filter — **predict** | $\mathbb{P}[s_t=j\mid y_{1:t-1}]=\sum_i P_{ij}\,\hat\xi_{t-1\mid t-1,i}$ | — |
| Hamilton filter — **update** | $\hat\xi_{t\mid t,j}=\dfrac{f(y_t\mid s_t=j)\,\mathbb{P}[s_t=j\mid y_{1:t-1}]}{\sum_k f(y_t\mid s_t=k)\,\mathbb{P}[s_t=k\mid y_{1:t-1}]}$ | filtered probs sum to $1.0000$ |
| Conditional density (Gaussian) | $f(y_t\mid s_t=j)=\dfrac{1}{\sqrt{2\pi}\sigma_j}\exp\!\Big[-\tfrac{(y_t-\mu_j)^2}{2\sigma_j^2}\Big]$ | — |
| **Sample log-likelihood** (Hamilton §4.2) | $\ln L=\sum_{t=1}^{T}\ln\Big[\sum_j f(y_t\mid s_t=j)\,\mathbb{P}[s_t=j\mid y_{1:t-1}]\Big]$ | filter $889.5$; EM $\to891.195$ |
| HMM forward / backward | $\alpha_t(j)=f(y_{1:t},s_t{=}j)$, $\beta_t(j)=f(y_{t+1:T}\mid s_t{=}j)$; $\gamma_t(j)\propto\alpha_t(j)\beta_t(j)$ | smoothed agreement $88.6\%$ |
| Viterbi (MAP path) | $\delta_t(j)=\max_i\delta_{t-1}(i)P_{ij}f(y_t\mid j)$; backtrace | $77.8\%$ agreement |
| SETAR($2$;$d$) | $x_t=\phi_0^{(j)}+\sum_i\phi_i^{(j)}x_{t-i}+a_t^{(j)}$ if $\gamma_{j-1}\le x_{t-d}<\gamma_j$ | threshold recovered $0.000$ |
| STAR (logistic) | $x_t=c_0+\sum_i\phi_{0,i}x_{t-i}+F[(x_{t-d}-\ell)/s]\big(c_1+\sum_i\phi_{1,i}x_{t-i}\big)+a_t$ | midpoint $c=0.00\approx\gamma$ |

> **Critical caveat.** The regime label is *arbitrary*: the decision of which state to call "bull" vs "bear" is a normalization (Hamilton 1989 §4.2 fixes it by, e.g., $\mu_1>\mu_0$). Without that constraint the likelihood is exactly symmetric — which is the *label-switching* degeneracy exploited in [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation — the formula engine

Standard library only. Reproduces the two cleanest verified numbers from §2: **Hamilton's expected regime durations** and the **normalized two-state filter** (probabilities stay in $[0,1]$ and sum to $1$ by construction — Hamilton's §4.2 point vs the Liptser–Shiryayev continuous-time analog).

```python
import math

# Hamilton (1989) Table I, US real GNP: state 0 = recession, state 1 = expansion
# P[s_t=0|s_{t-1}=0]=q (recession persists), P[s_t=1|s_{t-1}=1]=p (expansion persists)
p, q = 0.9049, 0.7550
print(f"expected expansion duration = 1/(1-p) = {1/(1-p):.2f} qtr   (paper 10.5)")
print(f"expected recession duration = 1/(1-q) = {1/(1-q):.2f} qtr   (paper 4.1)")

# stationary distribution pi P = pi  (2-state closed form): pi_rec=(1-p)/(2-p-q)
pi_rec = (1-p)/(2-p-q); pi_exp = 1-pi_rec
print(f"stationary P(expansion)={pi_exp:.3f}  P(recession)={pi_rec:.3f}")

# Hamilton filter: forward recursion, probabilities sum to 1 by construction
def gauss(x,m,v): return math.exp(-0.5*((x-m)/v)**2)/(math.sqrt(2*math.pi)*v)
def hamilton_filter(y, mu, sig, P, pinit):
    n=2; xi=[list(pinit)]
    for t in range(len(y)):
        pred=[P[0][j]*xi[-1][0]+P[1][j]*xi[-1][1] for j in range(n)]  # predict
        f=[gauss(y[t],mu[j],sig[j]) for j in range(n)]                # density
        d=sum(pred[j]*f[j] for j in range(n))
        xi.append([pred[j]*f[j]/d for j in range(n)])                 # update (Bayes)
    return xi[1:]

mu=[-0.004,0.012]; sig=[0.769,0.769]          # Hamilton's growth states (0=recession, 1=expansion)
P=[[q,1-q],[1-p,p]]                           # rows=prev state
xi = hamilton_filter([-0.3,1.5,0.2], mu, sig, P, [pi_rec,pi_exp])
for t,pr in enumerate(xi):
    print(f"t={t+1}: P(expansion|data)={pr[1]:.4f}  P(recession|data)={pr[0]:.4f}  sum={sum(pr):.4f}")
```
```
expected expansion duration = 1/(1-p) = 10.52 qtr   (paper 10.5)
expected recession duration = 1/(1-q) = 4.08 qtr   (paper 4.1)
stationary P(expansion)=0.720  P(recession)=0.280
t=1: P(expansion|data)=0.7187  P(recession|data)=0.2813  sum=1.0000
t=2: P(expansion|data)=0.7274  P(recession|data)=0.2726  sum=1.0000
t=3: P(expansion|data)=0.7261  P(recession|data)=0.2739  sum=1.0000
```
Starting from the *correct* stationary prior ($P(\text{expansion})=0.72$), the filter stays expansion-leaning and firms up slightly as the two positive observations arrive — the qualitative essence of regime detection, reproduced on three data points. (Note how sensitive the path is to the prior: mislabel the states and the same data appear to "start in recession", which is exactly the identification problem the caveat below warns about.)

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's full failure-mode analysis lives in [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Label switching.** The likelihood is symmetric under a permutation of the states, so two identical models can be returned with swapped labels (verified: two EM runs, loglik both $1309.234$, means permuted). Fix by a parameter constraint ($\mu_1>\mu_0$).
2. **Overfitting regimes.** Adding a state always raises the likelihood; a 3-state HMM on genuine 2-state data splits one regime into two near-identical clones (verified: loglik $+0.925$ but **BIC prefers 2-state**, $-2580$ vs $-2543$).
3. **Regime persistence & late detection.** The filter is Bayesian and slow by design; on volatile-but-meaningless data it oscillates, and every "regime" call carries detection lag that a fast strategy pays for.

---

### 5. Canonical Literature & Study References

- **Hamilton, James D.**: *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle*, Econometrica 57(2), 357–384 (1989). *Verified corpus ref (pillar1 PDF, pdftotext deep-read). The foundational paper: the nonlinear filter, ML estimation, and the 1952–1984 US GNP application — the 3% permanent GNP drop, recession duration $4.1$ qtr, expansion $10.5$ qtr.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series*, 3rd ed. (2010) — Ch 4 (Markov switching, SETAR, STAR, BDS), Ch 11 (state-space, Kalman filter), Ch 12 (MCMC: Gibbs, Metropolis–Hastings, FFBS, Markov-switching GARCH). *Verified corpus: tsay_ch4-6.md, tsay_ch10-12.md — no factual errors.*
- **Ang, Andrew & Timmermann, Allan**: *Regime Changes and Financial Markets*, Annual Review of Financial Economics 4, 313–337 (2012). *The canonical survey linking estimated regimes to fat tails, heteroskedasticity, skewness, and portfolio choice — the bridge from statistics to allocation.*
- **Kritzman, Mark, Page, Sébastien & Turkington, David**: *Regime Shifts: Implications for Dynamic Strategies*, Financial Analysts Journal 68(3) (2012). *Practitioner application of regime detection (Markov-switching on macro data) to dynamic asset allocation.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/bayesian-statistics/index|Bayesian Statistics]]
- Sibling topics (this pillar): [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & the Kalman Filter]] (the continuous-state sibling of the discrete-state filter here) · [[pillars/01-quantitative-research/momentum/index|Momentum]] (trend = a persistence regime) · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] (mean-reversion = a *different* regime)
- ML cross-link: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]] (Baum–Welch, Viterbi, regime-aware ML)
- Risk & portfolio: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Tail Risk (VaR/ES)]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]]
- Sub-pages (in-folder): 01 From Zero · 02 Markov-Switching Models · 03 Threshold Models · 04 Hidden Markov Models · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/01-quantitative-research/regime-detection/01-from-zero-intuition|01 · From Zero]] — elementary probability; everything else is built from zero.
- **Models + code (undergrad/job-seeking):** [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching]] → [[pillars/01-quantitative-research/regime-detection/03-threshold-models|03 · Threshold Models]] → [[pillars/01-quantitative-research/regime-detection/04-hmm|04 · Hidden Markov Models]].
- **Robustness (practitioner/graduate):** [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/01-quantitative-research/regime-detection/06-advanced-extensions|06 · Advanced Extensions (Regime Allocation)]].
