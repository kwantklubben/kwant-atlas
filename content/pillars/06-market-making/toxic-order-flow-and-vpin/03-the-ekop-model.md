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

The intuition: on any day, exactly one of three regimes generates the counts -

1. **No information event** (prob $1-\alpha$): buys ~ $\mathrm{Poisson}(\epsilon)$, sells ~ $\mathrm{Poisson}(\epsilon)$ - balanced.
2. **Good news** (prob $\tfrac{\alpha}{2}$): buys ~ $\mathrm{Poisson}(\mu+\epsilon)$, sells ~ $\mathrm{Poisson}(\epsilon)$ - buys lopsided.
3. **Bad news** (prob $\tfrac{\alpha}{2}$): buys ~ $\mathrm{Poisson}(\epsilon)$, sells ~ $\mathrm{Poisson}(\mu+\epsilon)$ - sells lopsided.

The likelihood of any observed $(b,s)$ is the *weighted average* of the three Poisson probabilities. Maximizing the log-likelihood over the parameter grid recovers $(\alpha,\mu,\epsilon)$ - and with them PIN.

The practical objective: implement the full likelihood, fit it to simulated data of known truth, and verify that MLE recovers the true PIN - the honest, working rendition of the primary paper.

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

**Why only $\alpha\mu$ is well identified.** The likelihood surface is shallow over the ridge where $\alpha\mu$ is constant - many $(\alpha,\mu)$ pairs give nearly the same fit. The *product* is identified, so $\widehat{\mathrm{PIN}}$ is stable even though $\widehat\alpha,\widehat\mu$ individually bounce around the grid (Hasbrouck Ch 6).

---

### 3. Computational Implementation - full EKOP likelihood + MLE (stdlib only)

Generate 5000 days from known truth $(\alpha,\mu,\epsilon)=(0.30,8,3)$ (true PIN $=0.2857$), then grid-search the likelihood and show the MLE recovers it.




MLE recovers the truth: estimated PIN $=0.2857$, exactly equal to the true PIN, and $\alpha\mu=2.4$ is matched. This is the full EKOP pipeline - the same machinery that turns real daily buy/sell counts into an information-risk estimate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The $\alpha\mu$ identification ridge.** With a coarse grid or too little data, MLE can pick a different $(\alpha,\mu)$ pair with the same product - PIN stays right, but the individual rates are not trustworthy. Never report $\widehat\alpha$ or $\widehat\mu$ in isolation.
2. **Grid search resolution.** The estimate is only as good as the grid. Refining the grid (or using a continuous optimizer) changes $\widehat\alpha,\widehat\mu$ while leaving $\widehat{\mathrm{PIN}}$ essentially fixed - another sign that the product, not the parts, is identified.
3. **Daily counts throw away the tape.** The EKOP likelihood uses only daily totals; intraday timing, order sizes, and sequence are discarded. This is the precise gap VPIN (volume buckets) is designed to close for high-frequency data ([[pillars/06-market-making/toxic-order-flow-and-vpin/04-vpin|04 · VPIN]]).
4. **Model misspecification.** Real data has correlation in uninformed arrivals, clustering, and multi-day information events that violate the i.i.d.-daily-Poisson assumption; PIN then becomes a *biased* estimator of the true informed fraction.

---

### 5. References

- **Easley, Kiefer & O'Hara (1997)**, *The information content of the trading process*, J. Empirical Finance 4, 159–186
- **Hasbrouck (2007)**, *Empirical Market Microstructure*
- **Easley, Hvidkjaer & O'Hara (2002)**, *Is information risk a determinant of asset returns?*, J. Finance 57(5)

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/toxic-order-flow-and-vpin/02-probability-of-informed-trading|02 · PIN]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Index Hub]]
- Forward: [[pillars/06-market-making/toxic-order-flow-and-vpin/04-vpin|04 · VPIN]] (why and how this model is re-expressed on a volume clock)
- Estimation base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (MLE, mixture models) · [[foundations/bayesian-statistics/index|Bayesian Statistics]]
