---
title: "05 — Failure Modes & Real-World Practice: Tail Blindness, Estimation Error & Backtesting"
tags:
  - pillar-quantitative-risk
  - var-and-expected-shortfall
  - failure-modes
  - backtesting
  - estimation-error
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|04 · Expected Shortfall]].

---

### 1. Intuition & Practical Objective

VaR and ES are *mathematically* clean but *operationally* treacherous. This page names the three failure modes precisely, so a risk manager knows which assumption to distrust and how the failure shows up in money terms. The objective is not cynicism — it is the discipline of knowing exactly where each number is an approximation so the residual can be measured and managed.

The three failures, in one line each:
1. **Tail blindness** — a quantile is insensitive to the *magnitude* of the worst outcomes (VaR), and even ES only reports their *mean*.
2. **Non-coherence** — VaR breaks subadditivity and convexity, so it cannot be safely optimised or decentralised.
3. **Estimation error** — both measures are *estimated* from finite (and quiet-period) samples; the estimates carry standard errors large enough to flip decisions.

---

### 2. Mathematical Ground Truth & Derivations

**Tail blindness (exact).** VaR is the $\alpha$-quantile. Changing the loss in *any* outcome already beyond $\mathrm{VaR}_\alpha$ leaves VaR **exactly unchanged**, because the quantile depends only on the *ordering* up to rank $\alpha$, not on the values past it. Concretely, with a $300$-observation sample the $99\%$ VaR is the $298$th order statistic (index $297$ in a 0-based sort) sorted loss: the $298$th, $299$th, $300$th (the truly catastrophic days) do not enter. ES *does* enter them:
$$
\frac{\partial\,\mathrm{ES}_\alpha}{\partial(\text{worst loss})}=\frac{1}{k},\qquad k=\lceil (1-\alpha)\,n\rceil.
$$
So a single worst-day escalation from $-3$ to $-15$ moves a $99\%$ ES (over $3$ tail points) by $(15-3)/3=4$, and moves VaR by $0$. **That asymmetry is the definition of tail blindness.**

**Estimation error (organisation).** For a sample of size $n$, the density-quantile standard error of $\mathrm{VaR}_\alpha$ is
$$
\mathrm{se}(\widehat{\mathrm{VaR}}_\alpha)\approx\frac{1}{f_L(\mathrm{VaR}_\alpha)}\sqrt{\frac{\alpha(1-\alpha)}{n}}.
$$
It shrinks like $n^{-1/2}$ — *slowly*. In the normal case at $\alpha=0.99$ we measured $\approx0.23\sigma$ at $n=250$, $\approx0.12\sigma$ at $n=1000$, $\approx0.04\sigma$ at $n=10^4$. ES averages the tail and is **noisier still** in small samples, because $F_L(\mathrm{VaR}_\alpha)$ — and hence $1/f$ and the effective tail count — is exactly what is hard to estimate.

**Window truncation.** Historical-simulation VaR over a fixed window assigns **zero probability** to any loss larger than the window's maximum. A $250$-day window drawn from a calm period reports a VaR *lower* than the true tail admits, and there is no data point to correct it. This is the same pathology as [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT's threshold problem]] seen from the other side.

**Backtesting.** A risk model is a forecast and must be graded (Hull §22.7). Two standard tests:
- **Kupiec POF (1995)** — unconditional coverage: do exceptions occur at the promised $(1-\alpha)$ rate? A likelihood-ratio test on the count of breaches.
- **Christoffersen (1998)** — conditional coverage: exceptions must also be *independent* (no clustering). A model that blows through its VaR in bursts fails even if the average rate is right.
The 1996 Basel framework encodes this as the **traffic-light** backtest ($99\%$/$10$-day; green $\le4$, yellow $5$–$9$, red $\ge10$ exceptions), with the capital multiplier $k\ge3$ rising through the zones (BCBS 1996).

---

### 3. Computational Implementation — estimating the estimator

We (a) measure the sampling standard deviation of $99\%$ VaR and ES across resamples for increasing $n$, and (b) demonstrate tail blindness by changing *only* the single worst loss. Stdlib only.

```python
import math, random

def normals(n, seed):
    random.seed(seed); o=[]
    for _ in range(n//2):
        u1=random.random(); u2=random.random()
        r=math.sqrt(-2*math.log(u1)); th=2*math.pi*u2
        o.append(r*math.cos(th)); o.append(r*math.sin(th))
    return o
def var(sample, a):
    s=sorted(sample); return s[min(len(s)-1, int(a*len(s)))]
def es(sample, a):
    s=sorted(sample); k=max(1, int((1-a)*len(s))); return sum(s[-k:])/k

# (A) estimation standard error of 99% VaR & ES vs sample size
for n in (250, 1000, 10000):
    vs=[]; ess=[]
    for j in range(400):
        smp = normals(n, 1000+j)
        vs.append(var(smp, 0.99)); ess.append(es(smp, 0.99))
    def stat(x):
        m=sum(x)/len(x); return m, math.sqrt(sum((v-m)**2 for v in x)/len(x))
    mv,sv = stat(vs); me,se = stat(ess)
    print(f"n={n:6d}: VaR_99={mv:.4f} (sd {sv:.4f})   ES_99={me:.4f} (sd {se:.4f})")

# (B) tail blindness: change ONLY the single worst loss; VaR unchanged, ES moves
s = sorted(normals(300, 9))              # 300-day sample, treated as losses
mild   = list(s); mild[-1]   = 3.0       # worst day = 3
severe = list(s); severe[-1] = 15.0      # worst day = 15
print(f"worst loss  3: VaR_99={var(mild,0.99):.4f}  ES_99={es(mild,0.99):.4f}")
print(f"worst loss 15: VaR_99={var(severe,0.99):.4f}  ES_99={es(severe,0.99):.4f}")
print(f"VaR is identical ({var(mild,0.99)==var(severe,0.99)}); ES rises by {(15.0-3.0)/3:.4f}")
```
```
n=   250: VaR_99=2.3450 (sd 0.2314)   ES_99=2.6790 (sd 0.2910)
n=  1000: VaR_99=2.3530 (sd 0.1181)   ES_99=2.6577 (sd 0.1327)
n= 10000: VaR_99=2.3299 (sd 0.0388)   ES_99=2.6670 (sd 0.0460)
worst loss  3: VaR_99=2.6615  ES_99=2.8079
worst loss 15: VaR_99=2.6615  ES_99=6.8079
VaR is identical (True); ES rises by 4.0000
```

Panel (A): the standard error falls only as $1/\sqrt n$, and **ES's is larger than VaR's at every sample size** — the coherence/estimation trade-off made concrete. Panel (B): VaR literally cannot see the $5\times$ worse tail; ES records it.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tail blindness → "picking up nickels in front of a steamroller."** A portfolio optimised against a VaR constraint loads on strategies with small steady gains and hidden catastrophic tails (selling deep-OTM puts, short-vol carry) that sit *past* the quantile ([[pillars/04-quantitative-risk/var-and-expected-shortfall/01-from-zero-intuition|01 · §4]]). Fix: constrain ES, not VaR.
2. **Non-coherence → aggregation and governance failure.** Subadditivity failure means firm-level VaR is **not** bounded by the sum of desk VaRs; capital "saved" by netting can be illusory (Artzner Axiom-S motivation; [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|03 · §2]]). Fix: coherent (ES-based) aggregation.
3. **Estimation error → decision flips on noise.** At $n=250$ the $99\%$ VaR carries $\sim0.23\sigma$ of pure sampling error; two desks with identical risk can report VaRs a quarter-$\sigma$ apart. Backtest (Kupiec + Christoffersen) and average over longer/filtered samples.
4. **Window truncation → a calm window is a blindfold.** Zero probability assigned beyond the sample max; the longer and quieter the calm, the worse (Hull §22.2). Fix: volatility-filtered historical simulation (FHS; McNeil–Frey) and EVT tail extrapolation.
5. **Discrete/short-horizon artefacts.** With few tail points the discrete quantile convention ($q^-$ vs $q^+$, [[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|02 · §2.1]]) and the ES boundary correction dominate; pin the convention in the policy.
6. **Procyclicality.** Historical VaR/ES fall in calm markets (allowing more leverage) and spike after losses — a feedback loop supervisors counter with **stressed** VaR/ES (Basel II.5) and the FRTB liquidity-horizon scaling ([[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|06 · §Basel]]).

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 (§22.2 historical simulation and window length, §22.7 backtesting, Business Snapshot 22.1 on the Basel $99\%$/$10$-day/$k\ge3$ rule) and Ch 23 (EWMA/GARCH volatility updating). *Numerically verified in the corpus.*
- **Kupiec, P.**, *Techniques for Verifying the Accuracy of Risk Measurement Models*, *J. Derivatives* 3(2):73–84 (1995) — the POF/TUFF backtest.
- **Christoffersen, P.**, *Evaluating Interval Forecasts*, *International Economic Review* 39(4):841–862 (1998) — conditional-coverage (independence/clustering) test.
- **BCBS**, *Supervisory Framework for the Use of Backtesting…* (1996, BIS) — the traffic-light zones and the capital multiplier.
- **McNeil & Frey**, *Estimation of Tail-Related Risk Measures…* (2000) — GARCH-filtered, EVT-tailed VaR/ES for heteroscedastic series; shows multi-day ES beats $\sqrt N$ scaling.
- **Gneiting, T.**, *Making and Evaluating Point Forecasts*, *JASA* 106 (2011) — ES is not elicitable, the formal limit on direct ES backtesting.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|04 · Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|06 · Advanced Extensions (Spectral/Euler, Basel ES)]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]
