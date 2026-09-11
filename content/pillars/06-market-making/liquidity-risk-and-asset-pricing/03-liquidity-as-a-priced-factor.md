---
title: "6.8.3 Liquidity as a Priced Risk Factor"
tags:
  - pillar-market-making
  - liquidity-risk-and-asset-pricing
  - liquidity-beta
  - priced-factor
  - pastor-stambaugh
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] and [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]].

---

### 1. Intuition & Practical Objective

The level of illiquidity being priced (page 01) is not the whole story. The deeper, harder-to-hedge risk is that **liquidity itself moves over time**, and that some stocks are more exposed to those moves than others. A stock that behaves like a normal, liquid stock most of the time but *becomes expensive to trade exactly when the whole market becomes expensive to trade* is riskier than its average illiquidity suggests. Investors demand compensation for bearing that exposure.

This page builds the standard machinery: an **aggregate liquidity factor**, its **innovations** (surprises), and each stock's **liquidity beta** — the sensitivity of its return to those innovations. The empirical punchline of Pástor & Stambaugh (2003): sorting stocks on liquidity beta produces a long-short spread of about **7.5% per year** in abnormal returns — high-liquidity-beta stocks earn more.

> **The two-premium recap.** Page 01 priced the *level* of illiquidity ($E[c^i]$). This page prices the *covariance of the return with aggregate liquidity* — the "PS channel" that Acharya–Pedersen formalize as their $\beta_3$ (the return-vs-market-illiquidity term; AP number the four betas $\beta_1..\beta_4$, so our $\beta_1,\beta_2,\beta_3$ are their $\beta_2,\beta_3,\beta_4$). They are different risks and both are compensated.

---

### 2. Mathematical Ground Truth & Derivations

**Step 1 — per-stock liquidity measure.** For each stock, each month, run a time-series regression of the stock's excess return on the signed dollar volume (a price-impact slope). The slope coefficient $\hat\gamma_{i,t}$ is the stock's liquidity: a large negative $\hat\gamma$ (returns fall sharply when volume is heavy) means *illiquid*.

**Step 2 — aggregate liquidity.** Equal-weight the per-stock measures into a market-wide series:

$$
\hat\gamma_t=\frac{1}{N_t}\sum_{i=1}^{N_t}\hat\gamma_{i,t}, \qquad \Delta\hat\gamma_t=\hat\gamma_t-\hat\gamma_{t-1} .
$$

**Step 3 — the innovation.** Because the *level* of liquidity may be forecastable (and expected changes would contaminate risk measures), Pástor–Stambaugh extract innovations by regressing the change on its own lag and the lagged deviation from trend:

$$
\Delta\hat\gamma_t = a+b\,\Delta\hat\gamma_{t-1}+c\left(\frac{m_{t-1}}{m_1}\right)\hat\gamma_{t-1}+u_t,
$$

then define the **liquidity innovation** $L_t=\tfrac{1}{100}\hat u_t$ (the $\tfrac1{100}$ is just scaling).

**Step 4 — the liquidity beta.** For stock $i$, regress its return on the innovation:

$$
r^i_t=\alpha^i+\beta^i_L\,L_t+\varepsilon^i_t, \qquad \beta^i_L=\frac{\operatorname{cov}(r^i_t,L_t)}{\operatorname{var}(L_t)}.
$$

A high (more positive) $\beta^i_L$ means the stock's return tends to rise when aggregate liquidity improves and fall when it dries up — it is *exposed to liquidity risk*.

**Step 5 — the price.** Cross-sectionally, expected return increases in $\beta^i_L$:

$$
E[r^i]=\alpha+\lambda\,\beta^i_L+\cdots
$$

with $\lambda>0$: bearing liquidity risk is compensated. Pástor–Stambaugh measure the spread between high- and low-liquidity-beta deciles at roughly 7.5% annually *after* controlling for market, size, value and momentum.

---

### 3. Computational Implementation — a liquidity factor and sorted portfolios

Simulate a market with a true aggregate liquidity-innovation factor $L_t$, give stocks different true liquidity betas, then recover those betas and show that a long-short portfolio sorted on *estimated* beta earns a positive spread. Stdlib only.

```python
import random, statistics

def ols_beta(x, y):
    mx = statistics.mean(x); my = statistics.mean(y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x)

random.seed(7)
N, T = 60, 180                       # 60 stocks x 180 months
true_beta = [random.uniform(-1.5, 2.5) for _ in range(N)]   # disperse liquidity betas
L   = [random.gauss(0.0, 0.01) for _ in range(T)]           # aggregate liquidity innovation
rM  = [random.gauss(0.008, 0.05) for _ in range(T)]         # market return
returns = []
for i in range(N):
    eps = [random.gauss(0.0, 0.04) for _ in range(T)]
    returns.append([0.006 + 1.0*rM[t] + true_beta[i]*L[t] + eps[t] for t in range(T)])

est_beta = [ols_beta(L, r) for r in returns]                # recovered liquidity betas
order = sorted(range(N), key=lambda i: est_beta[i])
third = N//3
low, high = order[:third], order[-third:]
ret_low  = statistics.mean(statistics.mean(returns[i]) for i in low)
ret_high = statistics.mean(statistics.mean(returns[i]) for i in high)
print(f"avg monthly return, LOW  liquidity-beta portfolio = {ret_low*100:.3f}%")
print(f"avg monthly return, HIGH liquidity-beta portfolio = {ret_high*100:.3f}%")
print(f"long-short (HIGH-LOW) = {(ret_high-ret_low)*100:.3f}%/mo = {(ret_high-ret_low)*1200:.1f}%/yr")
```
```
avg monthly return, LOW  liquidity-beta portfolio = 1.626%
avg monthly return, HIGH liquidity-beta portfolio = 1.876%
long-short (HIGH-LOW) = 0.250%/mo = 3.0%/yr
```
Even in this small synthetic sample, sorting on the *estimated* liquidity beta delivers a monotone spread: the high-beta portfolio earns more than the low-beta portfolio. **That spread is the liquidity-risk premium.** (Real-world estimates are noisier, and Pástor–Stambaugh reach 7.5%/yr by first *predicting* betas from firm characteristics rather than using raw historical betas — see §5.)

---

### 4. Failure Modes & First-Principles Breakdowns

- **Innovations, not levels.** Using the level of liquidity instead of its surprise contaminates the beta (expected liquidity changes predict returns). The residual-based innovation $L_t=\hat u_t/100$ exists precisely to purge this.
- **Beta estimation noise.** Historical liquidity betas are noisy, so decile sorts on *raw* betas understate the true spread; the Pástor–Stambaugh fix is to sort on *predicted* betas (from market cap, return, and other predictors).
- **Small-stock tilt.** Liquidity betas are highest for small, low-price, low-volume stocks — so a liquidity-factor strategy is easily confused with a size strategy unless you control for size (they do).
- **Factor measurability.** The aggregate liquidity series has occasional large *downward* spikes (Oct 1987, Sep 1998/LTCM, COVID) — the factor is fat-tailed, so OLS betas are sensitive to a few extreme months.

---

### 5. Canonical Literature & Study References

- **Pástor & Stambaugh (2003).** *Liquidity risk and expected stock returns.* JPE 111(3), 642–685. The construction (eqs. 6–8), the innovations, the predicted-beta sorts, and the 7.5%/yr spread.
- **Acharya & Pedersen (2005).** *Asset pricing with liquidity risk.* JFE 77(2) — embeds the PS channel as $\beta_3$ (our $\beta_2$) inside a full equilibrium CAPM.
- **Chordia, Roll & Subrahmanyam (2000).** *Commonality in liquidity.* Journal of Financial Economics 56 — why aggregate liquidity exists to begin with (the factor's foundation).
- **Hasbrouck.** *Market Microstructure: Foundations*, Ch 5, 11–15 — measuring the per-stock price-impact slopes the factor aggregates.

---

### 6. Connected Graph Bridges

- Next: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/04-liquidity-risk-and-crises|04 · Liquidity Risk & Crises]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/05-failure-modes-and-practice|05 · Failure Modes]]
- Back: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Index Hub]]
- Sibling: [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] (information risk as a second priced microstructure risk, Easley et al. 2002)
