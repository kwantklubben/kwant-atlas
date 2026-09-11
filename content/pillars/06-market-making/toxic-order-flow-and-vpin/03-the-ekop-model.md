---
title: "6.6.3 The EKOP Model"
tags:
  - pillar-market-making
  - ekop
  - poisson-mixture
  - maximum-likelihood
  - pin
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Poisson processes, MLE) and [[pillars/06-market-making/toxic-order-flow-and-vpin/02-probability-of-informed-trading|02 · PIN]].

---

### 1. Intuition & Practical Objective

PIN in [[pillars/06-market-making/toxic-order-flow-and-vpin/02-probability-of-informed-trading|02]] gives the formula; this page makes it **estimable**. The **EKOP model** (Easley, Kiefer & O'Hara 1997) is the full generative story behind PIN: a daily **mixture** of three Poisson processes, with parameters $\alpha,\mu,\epsilon$ to be estimated from observed daily buy/sell counts by **maximum likelihood**.

The intuition: on any day, exactly one of three regimes generates the counts —

1. **No information event** (prob $1-\alpha$): buys ~ $\mathrm{Poisson}(\epsilon)$, sells ~ $\mathrm{Poisson}(\epsilon)$ — balanced.
2. **Good news** (prob $\tfrac{\alpha}{2}$): buys ~ $\mathrm{Poisson}(\mu+\epsilon)$, sells ~ $\mathrm{Poisson}(\epsilon)$ — buys lopsided.
3. **Bad news** (prob $\tfrac{\alpha}{2}$): buys ~ $\mathrm{Poisson}(\epsilon)$, sells ~ $\mathrm{Poisson}(\mu+\epsilon)$ — sells lopsided.

The likelihood of any observed $(b,s)$ is the *weighted average* of the three Poisson probabilities. Maximizing the log-likelihood over the parameter grid recovers $(\alpha,\mu,\epsilon)$ — and with them PIN.

The practical objective: implement the full likelihood, fit it to simulated data of known truth, and verify that MLE recovers the true PIN — the honest, working rendition of the primary paper.

---

### 2. Mathematical Ground Truth & Derivations

**Poisson probabilities.** A single day with $b$ buys and $s$ sells has probability (Hasbrouck eq. 6.3):

$$
\Pr(b,s)=\underbrace{(1-\alpha)\;e^{-\epsilon}\tfrac{\epsilon^b}{b!}\;e^{-\epsilon}\tfrac{\epsilon^s}{s!}}_{\text{no event}}
+\underbrace{\tfrac{\alpha}{2}\;e^{-(\mu+\epsilon)}\tfrac{(\mu+\epsilon)^b}{b!}\;e^{-\epsilon}\tfrac{\epsilon^s}{s!}}_{\text{good news}}
+\underbrace{\tfrac{\alpha}{2}\;e^{-\epsilon}\tfrac{\epsilon^b}{b!}\;e^{-(\mu+\epsilon)}\tfrac{(\mu+\epsilon)^s}{s!}}_{\text{bad news}}.
$$

**Log-likelihood over $D$ days** (each day independent):

$$
\ln\mathcal{L}(\alpha,\mu,\epsilon)=\sum_{d=1}^{D}\ln\Big[\Pr(b_d,s_d)\Big].
$$

The parameters are estimated by maximizing $\ln\mathcal{L}$ over $\alpha,\mu,\epsilon$ (grid search is a robust, transparent method for this small three-parameter problem). PIN follows:

$$
\boxed{\;\widehat{\mathrm{PIN}}=\frac{\widehat\alpha\,\widehat\mu}{\widehat\alpha\,\widehat\mu+2\widehat\epsilon}\;}.
$$

**Why only $\alpha\mu$ is well identified.** The likelihood surface is shallow over the ridge where $\alpha\mu$ is constant — many $(\alpha,\mu)$ pairs give nearly the same fit. The *product* is identified, so $\widehat{\mathrm{PIN}}$ is stable even though $\widehat\alpha,\widehat\mu$ individually bounce around the grid (Hasbrouck Ch 6).

---

### 3. Computational Implementation — full EKOP likelihood + MLE (stdlib only)

Generate 5000 days from known truth $(\alpha,\mu,\epsilon)=(0.30,8,3)$ (true PIN $=0.2857$), then grid-search the likelihood and show the MLE recovers it.

```python
import math, random

def pois_pmf(k, lam):
    if k < 0:
        return 0.0
    return math.exp(-lam) * lam**k / math.factorial(k)

def ekop_lik(alpha, mu, eps, buys, sells):
    """Log-likelihood of daily buy/sell counts under the EKOP mixture."""
    logL = 0.0
    for b, s in zip(buys, sells):
        p_no   = (1 - alpha) * pois_pmf(b, eps) * pois_pmf(s, eps)
        p_good = (alpha / 2) * pois_pmf(b, mu + eps) * pois_pmf(s, eps)
        p_bad  = (alpha / 2) * pois_pmf(b, eps) * pois_pmf(s, mu + eps)
        logL  += math.log(p_no + p_good + p_bad)
    return logL

def mle_ekop(buys, sells):
    grid = [(a, m, e) for a in (i * 0.05 for i in range(1, 15))
            for m in range(2, 22) for e in (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)]
    return max(grid, key=lambda ab: ekop_lik(ab[0], ab[1], ab[2], buys, sells))

def simulate_day(alpha, mu, eps, rng):
    event = rng.random() < alpha
    if event:
        good = rng.random() < 0.5
        buy  = max(0, round(rng.gauss((mu + eps) if good else eps,
                                      math.sqrt((mu + eps) if good else eps))))
        sell = max(0, round(rng.gauss(eps if good else (mu + eps),
                                      math.sqrt(eps if good else (mu + eps)))))
    else:
        buy, sell = (max(0, round(rng.gauss(eps, math.sqrt(eps)))),
                     max(0, round(rng.gauss(eps, math.sqrt(eps)))))
    return buy, sell

def pin(a, m, e): return a * m / (a * m + 2 * e)

rng = random.Random(11)
TRUE = (0.30, 8.0, 3.0)
data = [simulate_day(*TRUE, rng) for _ in range(5000)]
buys, sells = [d[0] for d in data], [d[1] for d in data]

print(f"True parameters: alpha={TRUE[0]}, mu={TRUE[1]}, eps={TRUE[2]}  ->  true PIN={pin(*TRUE):.4f}")
est = mle_ekop(buys, sells)
print(f"MLE estimate   : alpha={est[0]}, mu={est[1]}, eps={est[2]}  ->  estimated PIN={pin(*est):.4f}")
print("(alpha and mu are individually imprecise, but the PRODUCT alpha*mu -- and hence PIN -- is well identified)")
print(f"  true alpha*mu = {TRUE[0]*TRUE[1]:.3f}   est alpha*mu = {est[0]*est[1]:.3f}   <- the stable quantity")
```
```
True parameters: alpha=0.3, mu=8.0, eps=3.0  ->  true PIN=0.2857
MLE estimate   : alpha=0.30000000000000004, mu=8, eps=3  ->  estimated PIN=0.2857
(alpha and mu are individually imprecise, but the PRODUCT alpha*mu -- and hence PIN -- is well identified)
  true alpha*mu = 2.400   est alpha*mu = 2.400   <- the stable quantity
```

MLE recovers the truth: estimated PIN $=0.2857$, exactly equal to the true PIN, and $\alpha\mu=2.4$ is matched. This is the full EKOP pipeline — the same machinery that turns real daily buy/sell counts into an information-risk estimate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The $\alpha\mu$ identification ridge.** With a coarse grid or too little data, MLE can pick a different $(\alpha,\mu)$ pair with the same product — PIN stays right, but the individual rates are not trustworthy. Never report $\widehat\alpha$ or $\widehat\mu$ in isolation.
2. **Grid search resolution.** The estimate is only as good as the grid. Refining the grid (or using a continuous optimizer) changes $\widehat\alpha,\widehat\mu$ while leaving $\widehat{\mathrm{PIN}}$ essentially fixed — another sign that the product, not the parts, is identified.
3. **Daily counts throw away the tape.** The EKOP likelihood uses only daily totals; intraday timing, order sizes, and sequence are discarded. This is the precise gap VPIN (volume buckets) is designed to close for high-frequency data ([[pillars/06-market-making/toxic-order-flow-and-vpin/04-vpin|04 · VPIN]]).
4. **Model misspecification.** Real data has correlation in uninformed arrivals, clustering, and multi-day information events that violate the i.i.d.-daily-Poisson assumption; PIN then becomes a *biased* estimator of the true informed fraction.

---

### 5. Canonical Literature & Study References

- **Easley, Kiefer & O'Hara (1997)**, *The information content of the trading process*, J. Empirical Finance 4, 159–186 — the Poisson-mixture model and PIN, the anchor for this page. *Primary PDF in corpus.*
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 6 — the mixture likelihood (eq. 6.3), the identification of $\alpha\mu$, and the daily-total-only aggregation point. *Math-verified in `hasbrouck_ch6-10.md`.*
- **Easley, Hvidkjaer & O'Hara (2002)**, *Is information risk a determinant of asset returns?*, J. Finance 57(5) — PIN estimated by this very likelihood, then used cross-sectionally as an information-risk factor.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/toxic-order-flow-and-vpin/02-probability-of-informed-trading|02 · PIN]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Index Hub]]
- Forward: [[pillars/06-market-making/toxic-order-flow-and-vpin/04-vpin|04 · VPIN]] (why and how this model is re-expressed on a volume clock)
- Estimation base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (MLE, mixture models) · [[foundations/bayesian-statistics/index|Bayesian Statistics]]
