---
title: "6.4.4 Spread Decomposition"
tags:
  - pillar-market-making
  - spread-decomposition
  - adverse-selection
  - order-processing
  - inventory-cost
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (regression, autocovariance) and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]].

---

### 1. Intuition & Practical Objective

The GM model says the *entire* spread is adverse selection. Reality is richer: a real observed spread bundles **three costs** with different price-dynamics signatures (Foucault Ch 3 §3.6; Hasbrouck Ch 8; Huang–Stoll 1997):

| Component | Source | Effect on transaction price |
|---|---|---|
| **Adverse selection** (information) | trading against informed | **permanent** - the efficient price moves and stays |
| **Order-processing** (fees, clearing, rents) | cost of providing immediacy | **instant reversal** - a temporary premium that snaps back |
| **Inventory** (holding risk) | undesired position | **slow/gradual reversal** |

The objective: **identify the permanent part.** The information component is the one that moves the *true* price; processing and inventory only jiggle it around temporarily. If you can measure the permanent component, you have measured the "toxicity" of the flow in dollar terms - and you know how much spread revenue genuinely compensates you for taking information risk versus how much is just cost-recovery.

---

### 2. Mathematical Ground Truth & Derivations

**Hasbrouck's generalized Roll model (Ch 8)** is the cleanest structural statement. Let $m_t$ be the efficient (information) price and the market maker a permanent-plus-transitory cost:

$$
p_t=m_t+c\,q_t,\qquad m_t=m_{t-1}+\lambda q_t+u_t,
$$

where $q_t\in\{-1,+1\}$ is signed order flow, $c$ the per-trade order-processing (transitory) cost, and $\lambda$ the **adverse-selection / price-impact cost** (the permanent informational component). The full spread is $2(c+\lambda)$ and the difference equation is

$$
\boxed{\;\Delta p_t=c\,(q_t-q_{t-1})+\lambda q_t+u_t\;}.
$$

Because $c$ multiplies the *change* in flow (it reverses next period) while $\lambda$ multiplies the *level* of flow (it persists), ordinary least squares on $\Delta p_t$ against $\{q_t,\,q_t-q_{t-1}\}$ separately recovers both - **the spread decomposition.** The moment structure (Hasbrouck eq. 8.3):

$$
\gamma_0\equiv Var(\Delta p_t)=c^2+(c+\lambda)^2+\sigma_u^2,\qquad
\gamma_1\equiv Cov(\Delta p_{t-1},\Delta p_t)=-c(c+\lambda).
$$

The permanent/variance measure $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ is **identified** even though the three structural parameters $\{\lambda,c,\sigma_u^2\}$ individually are not (only two autocovariances). Glosten–Harris (1988) make the same permanent-vs-transitory split and, cross-sectionally, find statistically significant adverse-selection (information) components in NYSE common-stock spreads for 1981–83.

**The signature test:** the transitory component reverses (negative return autocorrelation, bid–ask bounce), the permanent component does not - a trade that moves the *efficient* price leaves a lasting mark; a trade that only pays crossing costs leaves a bounce. In practice short-term impact = $\lambda+c$, long-term impact = $\lambda$ (Foucault eq. 3.34–3.37: $ST-LT=c$).

---

### 3. Computational Implementation - recover $\lambda$ and $c$ from trade prices (stdlib only)

Simulate the structural model with *known* $\lambda,c$, then run OLS and retrieve them. If the estimator recovers the true values, you can trust it on real price data to separate the information component of the spread.





The OLS recovers the adverse-selection ($\lambda$) and order-processing ($c$) components **exactly** across a range of true values - the mechanism that makes the spread decomposition practical. On real trade data, $\hat{c}$ is the "instant-reversal" premium and $\hat{\lambda}$ is the "permanent mark." (Copeland–Galai's option framing of the information piece and Huang–Stoll's three-way split are the extensions; the econometric instrument here is the same as Hasbrouck Ch 8.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Underidentification of the full tri-component spread.** $\{\lambda,c,\sigma_u^2\}$ cannot be recovered from $\{\gamma_0,\gamma_1\}$ alone - three parameters, two moments (Hasbrouck Ch 8). Only $\sigma_w^2=\lambda^2+\sigma_u^2$ is identified. Any claimed "exact" three-way split from pure price data needs extra structure or extra variables (e.g. quote data, order-size - Glosten–Harris, Huang–Stoll).
2. **Order-processing vs rents are inseparable from price data alone.** A dealer's "cost" $\gamma$ bundles operating cost and monopoly rent (Foucault Box 3.1); price dynamics cannot tell them apart. Don't assert a *cost* where you only measured a *markup*.
3. **Roll bias corrupts the transitory estimate.** Serial correlation in orders (buys follow buys), informed flow (corr($q_t,u_t$)>0), unbalanced flow, and time-varying expected returns all bias the simple autocovariance estimator - on informed-flow data the bounce is attenuated and the naive $c$ is biased upward/downward depending on the misspecification (Foucault Ch 2, eqs 2.19–2.25).

---

### 5. Canonical Literature & Study References

- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 8 (generalized Roll; eq 8.1–8.3; identification; random-walk decomposition) - **math-verified**.
- **Glosten & Harris (1988)**, *Estimating the components of the bid/ask spread*, JFE 21(1), 123–142 - the permanent/transitory empirical split.
- **Huang & Stoll (1997)**, *The components of the bid-ask spread: a general approach*, RFS 10(4), 995–1034 - the three-component (order-processing + inventory + adverse selection) framework.
- **Foucault, Pagano & Röell (2013)**, *Market Liquidity*, Ch 3 §3.4–3.6 (adverse-selection vs order-processing vs inventory signatures; $ST-LT=c$).
- **Copeland & Galai (1983)**, J. Finance 38 - the option-theoretic view of the information component.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Index Hub]]
- Forward: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model (topic)]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]]