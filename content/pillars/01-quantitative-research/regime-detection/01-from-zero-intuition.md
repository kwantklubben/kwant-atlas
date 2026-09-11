---
title: "01 — Regime Detection from Zero: Intuition & the Why"
tags:
  - pillar-quant-research
  - regime-detection
  - intuition
  - latent-state
  - bayes
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayes' rule, conditional expectation) and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity).

---

### 1. Intuition & Practical Objective

This page builds the *why* of regime detection with **no prior knowledge of switching models needed**. The objective is one idea: **returns come from a process whose mean and volatility occasionally change, you never observe the change directly, and your whole job is to track, in probability, which state you are in — updating a belief with every new observation.**

Start with the dumbest version. You have a coin, but it is one of two coins: a fair coin (heads probability $0.5$) or a biased coin ($0.9$). You are not told which. Each round someone flips the coin *they happen to be holding* and shows you only the outcome (H/T). Over time, by watching the outcomes, you can estimate *which coin is currently in play* and, more powerfully, you can notice when the hand switches.

Now swap the metaphor into markets:

1. **"Coin" = market regime.** A bull regime is a coin biased toward positive, calm returns; a bear regime is one biased toward negative, violent returns. The bias is never directly labeled on the tape — you infer it from the outcomes (returns).
2. **The switch is a hidden, stochastic process.** Regimes do not switch on a schedule; the next regime depends probabilistically on the current one (a Markov chain: "if it's bull today, there's a 5% chance of bear tomorrow"). This is Hamilton's (1989) core modeling move.
3. **You maintain a probability, not a verdict.** At every step you carry $\mathbb{P}[\text{bull}\mid\text{all returns so far}]$. A filtered probability of $0.85$ says "probably bull," not "it's bull." The filter *recursively* updates this number with each new return via Bayes' rule — the same engine that runs a Kalman filter, but on a discrete hidden state.

Why this matters for a practitioner: a strategy fitted on calm data is systematically wrong in turbulence. **Knowing the regime lets you switch allocation, target volatility, and size risk to the state you are probably in** (see [[pillars/01-quantitative-research/regime-detection/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 2. Mathematical Ground Truth & Derivations

**The recursive Bayes core.** Let $s_t$ be the hidden regime and $y_t$ the observed return. You want the filtered belief

$$
\hat\xi_{t\mid t}\;\equiv\;\mathbb{P}[s_t\mid y_1,y_2,\dots,y_t].
$$

Because you cannot observe $s_t$, this is a *latent-state* inference problem. The two-step recursion (Hamilton 1989 §4.2) is:

**Predict** (roll the Markov chain one step forward):
$$
\mathbb{P}[s_t=j\mid y_{1:t-1}]=\sum_{i}P_{ij}\,\hat\xi_{t-1\mid t-1,i}, \qquad P_{ij}=\mathbb{P}[s_t=j\mid s_{t-1}=i].
$$

**Update** (incorporate the new observation via Bayes):
$$
\hat\xi_{t\mid t,j}=\frac{f(y_t\mid s_t=j)\;\mathbb{P}[s_t=j\mid y_{1:t-1}]}{\sum_k f(y_t\mid s_t=k)\;\mathbb{P}[s_t=k\mid y_{1:t-1}]},
$$

where $f(y_t\mid s_t=j)$ is the regime-conditional density of the return (e.g., a Gaussian with regime mean $\mu_j$ and vol $\sigma_j$). The denominator is the conditional likelihood of $y_t$ — so the **same filter that infers the regime also evaluates the sample likelihood**, which is why ML estimation and state inference are one loop (Hamilton §4.2, line "evaluation of the sample likelihood is a natural byproduct of the filter").

**Stationary distribution & expected durations.** A 2-state chain with transition probs $P_{00}=q$, $P_{11}=p$ has stationary probabilities $\pi_0=(1-q)/(2-p-q)$, and the expected duration of state $i$ is

$$
\mathbb{E}[\text{time in }i]=\frac{1}{1-P_{ii}}.
$$

With Hamilton's US GNP estimates ($p=0.9049$, $q=0.7550$): a recession lasts on average $1/(1-0.7550)=4.1$ quarters, an expansion $1/(1-0.9049)=10.5$ quarters — versus NBER postwar averages of roughly $4$ and $14$–$15$ quarters (NBER business-cycle peak/trough dates). **Persistence is a parameter, not an assumption.**

---

### 3. Computational Implementation — a filter you can read in one screen

The full recursion in ~15 lines. We generate a 2-regime series (bull mean $+1.0\%$, bear mean $-1.2\%$), then run the Hamilton filter *knowing the true parameters*, and measure how well it recovers the planted states. Stdlib only.

```python
import math, random
random.seed(42)

mu=[0.010,-0.012]; sig=[0.020,0.035]; P=[[0.95,0.05],[0.10,0.90]]  # bull, bear
T=400
p0=(1-P[1][1])/(2-P[0][0]-P[1][1]); s0=0 if random.random()<p0 else 1
s=[s0]; y=[random.gauss(mu[s0],sig[s0])]
for t in range(1,T):
    nxt = 0 if random.random()<P[s[-1]][0] else 1
    s.append(nxt); y.append(random.gauss(mu[nxt],sig[nxt]))

def gauss(x,m,v): return math.exp(-0.5*((x-m)/v)**2)/(math.sqrt(2*math.pi)*v)
def hamilton_filter(y,mu,sig,P,pinit):
    xi=[list(pinit)]
    for t in range(len(y)):
        pred=[P[0][j]*xi[-1][0]+P[1][j]*xi[-1][1] for j in range(2)]  # predict
        f=[gauss(y[t],mu[j],sig[j]) for j in range(2)]
        d=sum(pred[j]*f[j] for j in range(2))
        xi.append([pred[j]*f[j]/d for j in range(2)])                 # update
    return xi[1:]

xi=hamilton_filter(y,mu,sig,P,[p0,1-p0])
agree=sum(1 for t in range(T) if (xi[t][0]>0.5)==(s[t]==0))
print(f"regime shares: bull={s.count(0)}, bear={s.count(1)}")
print(f"filter state agreement: {agree}/{T} = {100*agree/T:.1f}%")
print("filtered P(bull|data), first 6:", " ".join(f"{xi[t][0]:.3f}" for t in range(6)))
```
```
regime shares: bull=312, bear=88
filter state agreement: 350/400 = 87.5%
filtered P(bull|data), first 6: 0.821 0.898 0.877 0.640 0.808 0.891
```
The filter tracks the planted regime **without ever seeing it** — 87.5% agreement on raw, overlapping return distributions. The residual 12.5% is irreducible: the regimes overlap (bull vol $0.02$ vs a $0.022$ mean gap), so some returns are simply ambiguous.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The filter tells me the regime."** It tells you the *posterior probability*. At $0.55$ you are essentially unsure, and a strategy that overreacts to weak signals will whipsaw (see [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]]).
2. **Confusing the filter with prediction.** The filter gives $\mathbb{P}[s_t\mid y_{1:t}]$ (today's state). Forecasting next period requires the *predict* step $\mathbb{P}[s_{t+1}\mid y_{1:t}]$; many beginners stop at the filter and misdate their exposures.
3. **The label is arbitrary.** Calling state $0$ "bull" and state $1$ "bear" is a normalization; swap the labels and the likelihood is unchanged. That is the *label-switching* degeneracy — see the failure-modes page.
4. **Garbage-in regime detection.** If regimes do not actually exist (a single Gaussian), the filter still produces *some* two-state story and will happily overfit noise. Regime detection is only meaningful if the data is genuinely nonlinear-in-regime (Tsay Ch 4's nonlinearity tests, BDS).

---

### 5. Canonical Literature & Study References

- **Hamilton (1989)**, *Econometrica* 57(2) — §§1–4.2: the intuition (the coin metaphor, state 1/0), the filter, and why the sample likelihood is a byproduct. *Verified corpus deep-read.*
- **Tsay**, *Analysis of Financial Time Series*, Ch 4 §4.1.3 — the Markov-switching model contrasted with SETAR (deterministic vs stochastic switching), forecasting implications. *Verified: tsay_ch4-6.md.*
- **Ang & Timmermann (2012)**, *Annual Review of Financial Economics* — the survey bridge from regime estimates to market behavior and portfolio choice.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayes) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (ARMA) · [[foundations/bayesian-statistics/index|Bayesian Statistics]] (posterior updating)
- Continue: [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching Models]] · [[pillars/01-quantitative-research/regime-detection/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & the Kalman Filter]] (same predict/update recursion, continuous state)
