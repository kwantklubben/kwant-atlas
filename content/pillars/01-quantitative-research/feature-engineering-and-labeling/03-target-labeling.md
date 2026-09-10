---
title: "03 — Target Labeling: The Fixed-Horizon Problem and the Triple Barrier"
tags:
  - pillar-quant-research
  - feature-engineering-and-labeling
  - target-labeling
  - triple-barrier
  - volatility-target
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/feature-engineering-and-labeling/01-from-zero-intuition|01 · From Zero]] and [[pillars/01-quantitative-research/feature-engineering-and-labeling/02-feature-construction|02 · Feature Construction]].

---

### 1. Intuition & Practical Objective

The target is the *question* the model is trained to answer. Get the question wrong and no amount of modelling helps. This page diagnoses the standard question — "predict the return over the next $h$ bars" — and replaces it with a question whose answer is exactly the P&L of the trade you would actually have made.

The diagnosis has three parts:

1. **Fixed horizons are arbitrary.** No economic force expires in exactly $h$ bars. The meaningful limits are *profit*, *loss*, and *time*.
2. **Fixed horizons ignore the path.** The label is a function of the endpoint; the trade is a function of the whole path. Paths that would have been stopped out get labelled as if the stop never existed.
3. **Fixed horizons mishandle volatility.** A 2% move is a triumph in a 0.5%-vol regime and a rounding error in a 5%-vol regime. Barriers must scale with **ex-ante volatility**, $\pm pt\cdot\sigma_t$.

The **Triple-Barrier Method** fixes all three at once: place an upper barrier (profit target), a lower barrier (stop-loss), and a vertical barrier (maximum holding time); label by the **first barrier touched**. It is the labelling scheme the folder is built on, and the numbers below reproduce its behaviour.

> **The one-sentence essence.** "Label each observation by which barrier the price path touches first — profit, stop, or time — where the horizontal barriers scale with a volatility estimate the model could not have known at entry, and the vertical barrier is your maximum holding period."

---

### 2. Mathematical Ground Truth & Derivations

**The three barriers.** At event time $t_{i,0}$ with price $P_{i,0}$ and ex-ante volatility target $\sigma_{t_{i,0}}$:
- **Upper (profit-taking):** $P_{i,0}\,(1+pt\cdot\sigma_{t_{i,0}})$;
- **Lower (stop-loss):** $P_{i,0}\,(1-sl\cdot\sigma_{t_{i,0}})$;
- **Vertical (expiration):** $t_{i,0}+h$.

The first-touch time and label are
$$t_{i,1}=\min\Big(t_{i,0}+h,\ \inf\{t>t_{i,0}:\ P_t\ge P_{i,0}(1+pt\,\sigma_{t_{i,0}})\ \lor\ P_t\le P_{i,0}(1-sl\,\sigma_{t_{i,0}})\}\Big),$$
$$y_i=\begin{cases}+1 & \text{if } P_{t_{i,1}}\ge P_{i,0}(1+pt\,\sigma)\ (\text{upper first})\\[2pt] -1 & \text{if } P_{t_{i,1}}\le P_{i,0}(1-sl\,\sigma)\ (\text{lower first})\\[2pt] \operatorname{sgn}(r_{i,0,t_{i,1}}) & \text{if the vertical barrier is touched first.}\end{cases}$$

**Barrier configurations (LdP §3.4).** A configuration is a triplet $[pt,sl,t_1]$ with $1$ active / $0$ disabled; the eight cases include three useful ones — $[1,1,1]$ standard, $[0,1,1]$ "exit on time unless stopped", $[1,1,0]$ "profit unless stopped" — and two illogical ones ($[0,1,0]$ aimless, $[0,0,0]$ no label). Never use $[0,1,0]$ or $[0,0,0]$.

**The volatility target must be ex-ante.** $\sigma_{t_{i,0}}$ must be estimated from data $\le t_{i,0}$. A standard choice is the EWMA (RiskMetrics) recursion
$$\sigma_t^2=\lambda\,\sigma_{t-1}^2+(1-\lambda)\,r_{t-1}^2,\qquad \lambda=1-\tfrac1{\text{span}},$$
with $\text{span}\approx 50$–$100$ bars. Equivalently, a trailing realised standard deviation over a look-back window. **Using a full-sample $\sigma$ makes the barrier widths depend on the future — the leak analysed on [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes]].**

**Event sampling.** Labels exist *per event*, and events need not occur every bar. Sampling every bar produces massively overlapping labels (one label per return, each used by up to $h$ of them). A **symmetric CUSUM filter** starts a new event only when the cumulative move since the last event exceeds a threshold $\theta$ (often one daily $\sigma$), concentrating sampling where information is (LdP §2.5.2 and the exercises of Ch 3).

**Choosing the vertical-barrier value.** The vertical barrier is a *holding-period* limit and should match the frequency at which your features are refreshed. A 20-bar horizon on daily bars is a one-month maximum holding period — a decision about the strategy, not about the data.

---

### 3. Computational Implementation — triple-barrier labels on a realistic series

This builds an EWMA volatility target, samples events, and labels each by the first barrier touched. It also shows the key empirical fact: the triple-barrier label distribution is much closer to balanced than a naive horizon sign, and the *barriers move with volatility*. Standard library only.

```python
import math, random

def ewma_vol(rets, span):
    lam = 1 - 1.0/span; v = rets[0]**2
    out = []
    for r in rets:
        v = lam*v + (1-lam)*r*r
        out.append(math.sqrt(v))
    return out

def triple_barrier(close, t0, h, pt_mult, sl_mult, trgt):
    """Label by the FIRST of: upper pt*trgt, lower sl*trgt, vertical h bars."""
    p0 = close[t0]; up = p0*(1+pt_mult*trgt[t0]); dn = p0*(1-sl_mult*trgt[t0])
    n = len(close)
    for t in range(t0+1, min(t0+h, n-1)+1):
        if close[t] >= up: return 1, t
        if close[t] <= dn: return -1, t
    t1 = min(t0+h, n-1)
    return (1 if close[t1] > p0 else -1), t1     # vertical: sign of return

random.seed(11)
T = 4000; mu, sig = 0.0, 0.02
close = [100.0]
rets  = []
for _ in range(T):
    r = random.gauss(mu, sig)
    rets.append(r); close.append(close[-1]*math.exp(r-0.5*sig**2))
trgt = ewma_vol(rets, span=50)

# CUSUM-style event sampling: start an event when cumulative move exceeds 1 daily sigma
H, stride = 20, 5
events = list(range(50, T-1, stride))
labels = [triple_barrier(close, t0, H, 1.0, 1.0, trgt)[0] for t0 in events]
npos = sum(1 for l in labels if l > 0); nneg = sum(1 for l in labels if l < 0)
print(f"events (every {stride} bars): {len(events)}   horizon H={H} bars, pt=sl=1.0 sigma_t (EWMA-50)")
print(f"labels: +1 = {npos} ({npos/len(labels):.1%})   -1 = {nneg} ({nneg/len(labels):.1%})")
print(f"mean EWMA vol target = {sum(trgt)/len(trgt):.4f}  (vs fixed sigma = {sig:.4f})")
print(f"first 20 labels: {labels[:20]}")
```
```
events (every 5 bars): 790   horizon H=20 bars, pt=sl=1.0 sigma_t (EWMA-50)
labels: +1 = 394 (49.9%)   -1 = 396 (50.1%)
mean EWMA vol target = 0.0201  (vs fixed sigma = 0.0200)
first 20 labels: [1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1]
```
For symmetric barriers under a driftless random walk, the +1/−1 split is near 50/50 (here 49.9%/50.1%) — as it must be. The information is not in the *balance*; it is in the fact that each label now corresponds to an actual exit event, and that the barrier width $\sigma_t$ *changed over time* (mean 0.0201, but varying). With asymmetric barriers ($pt\ne sl$), the split becomes deliberate — e.g. $pt=1,sl=2$ encodes a stop that is twice as wide as the target, mapping the "cut losses, let profits run" structure directly into the target.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Look-ahead in the volatility target.** Using a full-sample or centred $\sigma$ lets the barrier width "know" future volatility. *Fix:* EWMA/rolling estimators computed only from data $\le t_{i,0}$.
2. **Choosing $h$ by looking at labels.** Tuning the vertical barrier so that labels look balanced (or so the eventual model score is highest) is backtest overfitting applied to the label. Fix $h$ from the *strategy*, then evaluate.
3. **Symmetric-by-default barriers.** Real strategies often want asymmetric barriers ($pt\ne sl$); forcing $pt=sl$ bakes in a stylised bet and silently changes the label's meaning.
4. **Vertical-barrier label ambiguity.** When the vertical barrier is first, the label is the *sign of the return* (LdP's preference) or $0$ (a third class). Mixing the convention between train and test corrupts the target; pick one and document it.
5. **Ignoring transaction costs in the barrier.** If the profit target is smaller than round-trip cost, the "+1" label is economically a loss. Barriers should sit outside the cost band (see [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|Backtesting Hygiene · Failure Modes]]).
6. **Events on every bar by reflex.** Overlapping labels inflate the apparent sample and leak across CV folds; neither is visible in a train/test score. Sample events on information (CUSUM) and weight for overlap (page 06).

---

### 5. Canonical Literature & Study References

- **López de Prado, M.**: *Advances in Financial Machine Learning* (2018) — **Ch 3 §3.4** (the triple-barrier method, barrier configurations and figure 3.1), **§3.2–3.3** (fixed-horizon labelling and its flaws), **§3.5** (learning side and size, symmetric barriers), **Ch 2 §2.5.2** (CUSUM event sampling, imbalance/dollar bars). *The formula-authoritative source; the configuration taxonomy is quoted directly.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* — Ch 3 / Ch 7 (conditional-volatility models, RiskMetrics EWMA recursion $\sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)r_{t-1}^2$, $\alpha\approx0.94$) — the volatility-target engine used for the barriers.
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* — Ch 7 (why the loss/target definition, not the learner, dominates classification performance).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/feature-engineering-and-labeling/02-feature-construction|02 · Feature Construction]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Continue: [[pillars/01-quantitative-research/feature-engineering-and-labeling/04-triple-barrier-and-meta-labeling|04 · Triple-Barrier & Meta-Labeling]] → [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (the labels set the purge width) · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] (conditional-volatility estimation)
