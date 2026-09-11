---
title: "01 — Deep Learning for Sequences from Zero: Why Order Matters"
tags:
  - pillar-machine-learning
  - deep-learning-for-sequences
  - intuition
  - sequence-modeling
  - state
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]. Everything else is built from scratch on this page.

---

### 1. Intuition & Practical Objective

This page builds the *why* of sequence models with **no prior deep-learning knowledge needed**. The objective is one idea: **if the order of your data carries information, then any model that ignores the order — a regression, a tree, a plain feed-forward net — is provably throwing that information away.**

Start with the dumbest possible question. You have a stream $x_1,x_2,\dots,x_T$ and you want to predict $y_t$. What does a normal (IID) model do? It treats each row $(x_t,y_t)$ as an independent draw and learns a function $f(x_t)\to y_t$. It is *blind to the arrow of time*: shuffle your rows, retrain, and the IID model is unchanged. If shuffling changes nothing, the model has discarded everything the ordering could have told it.

Financial series are ordered in exactly the way that matters. Three "aha"s:

1. **There is state, and it is not in the current row.** Whether the market is in a trending or mean-reverting mood is not visible in today's return alone — it is visible in the *sequence* of recent returns. A model with no memory cannot represent "we have been drifting up for two weeks."
2. **Order is information, and shuffling destroys it.** Take a series with regime persistence, keep every value, and shuffle: the *marginal distribution is identical* but the predictability collapses. The information lived entirely in the ordering (§3 shows this: lag-1 autocorrelation $0.527\to0.003$).
3. **A recurrence is a learned sufficient statistic.** Instead of feeding the model a hand-built window of lags, a *recurrent* model maintains a hidden state $h_t$ that summarises everything seen so far, and updates it as each new input arrives: $h_t=g(h_{t-1},x_t)$. This is the whole idea of a sequence model, and everything else (LSTM, GRU, Transformer) is a better-designed $g$.

The practical objective of this folder is then: **choose $g$ (recurrence, attention, or convolution) and train it, while staying honest about a signal that is weak and a distribution that drifts.**

---

### 2. Mathematical Ground Truth & Derivations

**The IID assumption, written down.** Standard supervised learning assumes $(x_t,y_t)$ are i.i.d. draws from a joint $p(x,y)$, so the optimal predictor is the conditional mean/expectation $\mathbb{E}[y\mid x]$ and the joint likelihood factorises:

$$
p(x_1,y_1,\dots,x_T,y_T)=\prod_{t=1}^{T}p(x_t,y_t).
$$

The factorisation is the assumption. For a time series it is false in two ways — through the *inputs* and the *targets*:

$$
p(x_1,\dots,x_T)=\prod_{t}p(x_t\mid x_{t-1},x_{t-2},\dots),\qquad p(y_t\mid x_{1:t})\neq p(y_t\mid x_t).
$$

**The Markov chain (the simplest sequence model).** The cleanest tractable assumption is order-1 Markov:

$$
p(x_t\mid x_{1:t-1})=p(x_t\mid x_{t-1}).
$$

The state is just the previous value; the whole past is summarised by one number. This is already a sequence model, and it is the discrete cousin of the RNN: an RNN generalises "state $=$ previous value" to "state $=$ learned vector $h_{t-1}$", with a *continuous* transition

$$
h_t=g_\theta(h_{t-1},x_t),\qquad \hat y_t=f_\phi(h_t),
$$

and parameters $\theta,\phi$ fitted by maximising $\sum_t \log p(y_t\mid h_t)$. The Kalman filter is the special case where $g$ is linear-Gaussian and the state has a closed-form optimal update (see [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Kalman Filtering]]).

**The value of memory, quantified.** For a persistence process the autocovariance $\gamma_k=\operatorname{Cov}(x_t,x_{t+k})$ is positive and slowly decaying, so the lag-$k$ predictor's skill is $\rho_k=\gamma_k/\gamma_0$. A function of $x_t$ alone captures only $\rho_0=1$'s *instantaneous* structure; a function of the recent path captures $\rho_k>0$. The next pages make $g$ expressive enough to capture these dependencies in both directions (past→future) and at multiple scales.

---

### 3. Computational Implementation — order carries information

Stdlib only. We generate a regime-switching return series (the sign persists, as in bull/bear phases), then **keep every value but shuffle the order** and measure what is lost: lag-1 autocorrelation, mean run length, and the accuracy of a simple recurrent predictor ("the running sum of the last $k$ returns predicts the sign of the next").

```python
import random, math
random.seed(1)

# Regime-switching returns: sign persists (bull/bear), magnitude ~ N(0,1)
def gen(T, p_stay=0.95):
    state = 1; r = []
    for _ in range(T):
        if random.random() > p_stay:
            state = -state
        r.append(state * abs(random.gauss(0.0, 1.0)) + random.gauss(0.0, 0.3))
    return r

def lag1ac(x):
    n = len(x); m = sum(x) / n
    num = sum((x[i]-m)*(x[i+1]-m) for i in range(n-1))
    den = sum((v-m)**2 for v in x)
    return num / den

def mean_run(x):
    runs = []; cur = 1
    for i in range(1, len(x)):
        if (x[i] > 0) == (x[i-1] > 0):
            cur += 1
        else:
            runs.append(cur); cur = 1
    runs.append(cur)
    return sum(runs) / len(runs)

T = 20000
r = gen(T)
sh = r[:]; random.shuffle(sh)
print("original sequence : lag-1 autocorr = %+.3f  mean run length = %.2f" % (lag1ac(r), mean_run(r)))
print("shuffled sequence : lag-1 autocorr = %+.3f  mean run length = %.2f" % (lag1ac(sh), mean_run(sh)))

# A recurrence turns the persistent sign into a usable state (running sum of last k)
k = 5
def acc_predict(x):
    ok = tot = 0
    for t in range(k, len(x)):
        s = sum(x[t-k:t])
        if s != 0:
            ok += (s > 0) == (x[t] > 0); tot += 1
    return ok / tot
print("sign(r_t) predicted from running sum of last %d returns:" % k)
print("  original : acc = %.3f" % acc_predict(r))
print("  shuffled : acc = %.3f" % acc_predict(sh))
```
```
original sequence : lag-1 autocorr = +0.527  mean run length = 5.00
shuffled sequence : lag-1 autocorr = +0.003  mean run length = 2.02
sign(r_t) predicted from running sum of last 5 returns:
  original : acc = 0.797
  shuffled : acc = 0.505
```

Read the punchline: the shuffled and original series have **identical values** (identical mean, variance, histogram) yet the shuffled one is nearly a fair coin ($0.505$ accuracy, run length $2.02\approx$ the geometric baseline), while the original is highly predictable from a simple *recurrent state* ($0.797$ accuracy, run length $5.00$). **The information is in the ordering, and a model with a state can read it.** More importantly for finance: the recurrent predictor was *two lines of arithmetic*, not a deep net — the value is in having a state at all, which is the point the more elaborate architectures on the next pages build on.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Order doesn't matter if I just use good features."** False in general. Hand-built lag features can *approximate* state, but they fix the window length in advance and cannot represent a state that is updated by new information. A recurrence learns the sufficient statistic instead of you guessing it.
2. **"Shuffling is harmless"** — the exact error that inflates CV scores in the sibling [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]] folder. For a sequence model, shuffling is not merely a validation bug; it *destroys the signal you are trying to learn* (autocorr $0.527\to0.003$ above).
3. **Stationarity is smuggled in.** The Markov/RNN view assumes the transition $g_\theta$ is *stationary* — the same rule at every $t$. Financial regimes violate this (page 05 quantifies it: a model fit on regime A has $R^2=+0.76$ in-sample but $-0.68$ out-of-regime). Order carries information; the *rule* generating that order does not stay fixed.
4. **State can memorise noise.** With enough hidden units, $h_t$ can encode idiosyncratic shocks that look predictive in-sample and mean nothing out-of-sample — the low-SNR failure developed in [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]].

---

### 5. Canonical Literature & Study References

- **Goodfellow, Bengio & Courville**, *Deep Learning*, **Ch. 10** (§10.1–10.3: why sequence modeling needs state; the unrolled computational graph; the RNN as a learned sufficient statistic) — the primary theory source for this page.
- **Tsay, Ruey S.**, *Analysis of Financial Time Series* (3rd ed.) — serial dependence, autocorrelation, and why the IID assumption fails for returns (the classical-econometrics side of the same idea). *Corpus available.*
- **López de Prado**, *Advances in Financial Machine Learning*, **Ch. 1** — why a *sequence* of financial data is not an IID sample, and why the ML-pipeline problems (labels, validation) dominate the architecture choice.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Index Hub]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
- Forward: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/02-rnns-and-lstms|02 · RNNs & LSTMs]]
- Classical state-space cousin: [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]]
- Features the state model replaces/consumes: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]]
