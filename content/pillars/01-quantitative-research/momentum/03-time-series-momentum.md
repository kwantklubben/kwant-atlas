---
title: "03 — Time-Series Momentum: Trend-Following & CTA"
tags:
  - pillar-quant-research
  - momentum
  - time-series
  - cta
  - trend-following
  - volatility-targeting
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (forecasting, EWMA/GARCH-style vol) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (moments).

---

### 1. Intuition & Practical Objective

Time-series momentum (TSMOM) is the **Moskowitz–Ooi–Pedersen** strategy and the mathematical heart of **CTA / trend-following**: look at *each asset in isolation*; if its **own** trailing 12-month return is positive, go long; if negative, go short; and scale each position **inversely to its own ex-ante volatility** so every contract carries the same risk.

The bet is **absolute**, not relative: an asset is traded because *it* trended, regardless of its peers. This is what makes TSMOM behave differently from cross-sectional momentum — notably, TSMOM does *well* in crashes (it flips short as markets fall), while XSMOM crashes (see 05).

Verified facts (MOP 2012, 58 futures contracts across commodities, currencies, global equity indexes, and fixed income, 1985–2009):
- **All 58** contracts show positive TSMOM predictability; 52 significant at 5%.
- The diversified TSMOM portfolio runs at **~12% annualized volatility** (each position is sized to 40% ex-ante vol), delivering large alpha vs standard factors (1.58%/mo) and loading only on the *cross-sectional* momentum factor.
- TSMOM's worst month is nowhere near as bad as XSMOM's — it profits during the extreme 2008 episode.

Two engineering facts make TSMOM a *system*, not a slogan: **volatility scaling** (equalize risk across wildly different assets) and **sign-based signals** (robust to magnitudes, comparable across assets).

---

### 2. Mathematical Ground Truth & Derivations

**Signal.** For asset $s$ with daily/monthly excess returns, the sign of its own trailing 12-month excess return:
$$S^s_t = \operatorname{sign}\Big(r^s_{t-12,t}\Big), \qquad r^s_{t-12,t}=\prod_{k=1}^{12}\big(1+r^s_{t-k}\big)-1.$$

**Ex-ante volatility (MOP §2.4).** An exponentially weighted variance with a 60-day center of mass, annualized by 261:
$$\sigma^2_t = 261\sum_{i\ge0}(1-\delta)\,\delta^i\big(r_{t-1-i}-\bar r_t\big)^2, \qquad \frac{\delta}{1-\delta}=60\ \text{days}.$$
To avoid look-ahead, the volatility measured at $t-1$ is applied to the time-$t$ return.

**Position sizing and TSMOM return.** Size each position to an ex-ante annualized volatility $\sigma_{\text{tgt}}$ (MOP use 40%):
$$w^s_t = \frac{\sigma_{\text{tgt}}}{\sigma^s_{t-1}}\,\operatorname{sign}\big(r^s_{t-12,t}\big), \qquad r^{\text{TSMOM,s}}_{t,t+1}=w^s_t\, r^s_{t,t+1}.$$
The diversified factor (equal-weight across the $S_t$ available contracts) is
$$r^{\text{TSMOM}}_{t,t+1}=\frac{1}{S_t}\sum_{s=1}^{S_t}\operatorname{sign}\big(r^s_{t-12,t}\big)\,\frac{\sigma_{\text{tgt}}}{\sigma^s_{t-1}}\,r^s_{t,t+1}.$$
Because each position is scaled to the same ex-ante vol, the diversified portfolio has vol $\approx\sigma_{\text{tgt}}/\sqrt{S_t}$ (diversification) — in the corpus, ~12% annualized.

**Expected return decomposition (MOP eq. 7).** With portfolio weights $w^{\text{TS}}_t=(1/N)r_{t-12,t}$,
$$\mathbb{E}\big[r^{\text{TS}}_{t,t+1}\big]=\frac{\operatorname{tr}(\Omega)}{N}+\frac{12\,\mu'\mu}{N},$$
so TSMOM profit is driven primarily by **own time-series autocovariance** $\operatorname{tr}(\Omega)$ — the cleanest statement that TSMOM is a bet on *each asset's own* return continuation.

**TSMOM vs XSMOM.** Regressing TSMOM on XSMOM (MOP §5) gives $\beta=0.66$ ($t=15.2$, $R^2=44\%$) with a **positive significant alpha of 76 bp/month** ($t=5.9$): related, but not the same strategy.

---

### 3. Computational Implementation — vol-targeted trend engine

Standard library only. Implements the MOP engine: EWMA ex-ante vol, sign-based 12-month signal, inverse-vol position sizing. Verifies (a) **vol-targeting** (a single scaled contract realizes ~the target vol) and (b) a **positive-Sharpe diversified TSMOM portfolio**.

```python
import random, math
random.seed(21)

# Time-series momentum (Moskowitz-Ooi-Pedersen): pos = sign(own 12m return)*(tgt/vol).
# Ex-ante vol = EWMA of squared daily returns, center of mass 60 days, annualized by 261,
# measured at t-1 (no look-ahead).
M, DAYS = 12, 1000                        # 12 futures contracts, ~4y of daily data
mu = [random.gauss(0.0004, 0.0006) for _ in range(M)]   # per-asset drift
ret = []
for i in range(M):
    prev, r = 0.0, []
    for t in range(DAYS):
        e = random.gauss(0.0, 0.012)
        prev = mu[i] + 0.06*(prev - mu[i]) + e          # weak AR(1) persistence
        r.append(prev)
    ret.append(r)

lam = 60.0/61.0                                          # center of mass 60 days
def exante_vol(r, t):
    v = 0.0
    for k in range(1, min(t, 500)+1):
        v = lam*v + (1.0-lam)*r[t-k]**2
    return math.sqrt(261.0 * v)                          # annualized

TARGET = 0.40                                            # 40% ex-ante vol per position (MOP)
strategies = [[] for _ in range(M)]
for i in range(M):
    for t in range(253, DAYS-1):
        past12 = math.prod(1.0+ret[i][j] for j in range(t-252, t)) - 1.0
        sig = 1.0 if past12 > 0 else -1.0
        pos = TARGET / exante_vol(ret[i], t)             # ex-ante vol at t-1
        strategies[i].append(sig * pos * ret[i][t])

def stats(s):
    m = sum(s)/len(s); sd = (sum((x-m)**2 for x in s)/len(s))**0.5
    return m*252, sd*math.sqrt(252), (m/sd)*math.sqrt(252), min(s)*100

mn, sd, sr, lo = stats(strategies[0])
print(f"single contract: realized ann.vol {sd*100:.1f}%  (target {TARGET*100:.0f}%)")
port = [sum(strategies[i][k] for i in range(M))/M for k in range(len(strategies[0]))]
mn, sd, sr, lo = stats(port)
print(f"diversified TSMOM: ann.return {mn*100:+.2f}%  ann.vol {sd*100:.1f}%  Sharpe {sr:+.2f}  worst day {lo:+.2f}%")
pos = sum(1 for i in range(M) if stats(strategies[i])[2] > 0)
print(f"contracts with positive TSMOM Sharpe: {pos}/{M}")
```
```
single contract: realized ann.vol 39.2%  (target 40%)
diversified TSMOM: ann.return +22.77%  ann.vol 11.7%  Sharpe +1.95  worst day -2.32%
contracts with positive TSMOM Sharpe: 9/12
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The turning-point whipsaw.** In range-bound, mean-reverting regimes the sign flips on every cross of the trailing mean, buying tops and shorting bottoms — a slow, persistent drawdown ("death by a thousand papercuts") over 12–18 months. Vol scaling doesn't fix a *wrong-sign* problem; it only fixes risk allocation.
2. **Volatility estimator quality drives returns.** The strategy is only as good as its ex-ante vol. A *noisy* vol estimator mis-sizes every position; better estimators (EWMA with sound half-life, or realized-vol extensions per Baltas & Kosowski) cut turnover and lift net Sharpe. Baltas & Kosowski (2013) show transaction costs can fall to ~105 bp without a significant Sharpe loss using more efficient estimators.
3. **Burst risk / momentum-in-a-crash cuts both ways.** TSMOM profits *in* the 2008 crash (it is short before the fall) but can be caught **short** when a long decline *reverses* sharply upward — the trend-flip whipsaw. It is not crash-proof, only crash-*timed* differently from XSMOM.
4. **Sign + magnitude ambiguity at the flip.** Near $S_t=0$ the sign is unstable; small measurement noise flips a large position. Practitioners use a dead-band / threshold rather than raw sign.
5. **Capacity & turnover.** Scaling by inverse vol concentrates turnover in low-vol, high-turnover instruments; costs and market impact erode the diversified factor (see Baltas & Kosowski turnover analysis).

---

### 5. Canonical Literature & Study References

- **Moskowitz, Ooi & Pedersen (2012)**, *Time Series Momentum*, J. Financial Economics 104(2) — the TSMOM engine, EWMA vol, 58 contracts, XSMOM relation. *Verified corpus refs/14.*
- **Baltas & Kosowski (2013)**, *Demystifying Time-Series Momentum Strategies* — the role of volatility estimators and trading rules. *Verified corpus refs/19.*
- **Daniel & Moskowitz (2016)**, *Momentum Crashes* — dynamic version of the TSMOM/XSMOM strategy. *Verified corpus refs/16.*
- **Fung & Hsieh (2001)** — trend-following CTA returns and their option-like payoff structure.

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Sibling: [[pillars/01-quantitative-research/momentum/02-cross-sectional-momentum|02 · Cross-Sectional Momentum]] (TSMOM's $\beta=0.66$ cousin) · [[pillars/01-quantitative-research/momentum/04-value-momentum-interaction|04 · Value–Momentum]]
- Practice: [[pillars/01-quantitative-research/momentum/06-advanced-extensions|06 · Advanced Extensions]] (vol scaling, dynamic weighting) · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity (vol targeting)]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]
