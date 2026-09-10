---
title: "02 - Illiquidity Measures: Amihud ILLIQ, Bid-Ask Spread, Roll & Turnover"
tags:
  - pillar-market-making
  - liquidity-risk-and-asset-pricing
  - illiquidity-measures
  - amihud-illiq
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] and [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & Roll Model]].

---

### 1. Intuition & Practical Objective

Before you can price liquidity risk you have to *measure* illiquidity — and every choice of measure changes the answer. This page is the **measurement toolkit**: what each proxy actually captures, how to compute it from the data you realistically have, and what each one gets wrong.

The objective is a working command of four proxies, from the most data-hungry to the most robust:

1. **Bid–ask spread** — the *direct* cost of a round trip, but needs quotes/transaction data.
2. **Roll estimator** — the spread *inferred from the negative autocovariance* that bid-ask bounce induces in prices; needs only prices.
3. **Amihud ILLIQ** — *price impact per dollar of volume*, $|r|/\text{VOLD}$; needs only daily returns and volume, which is why it became the workhorse.
4. **Turnover / Amivest** — *how much volume passes through*; a capacity/activeness proxy.

The unifying idea: **illiquidity is the response of price to order flow** (Kyle's price-impact concept). Spreads and ILLIQ are two operationalizations of that same response — one in quote space, one in return/volume space.

---

### 2. Mathematical Ground Truth & Derivations

**Bid–ask spread.** Relative quoted spread is $S=(a-b)/m$ with mid $m=(a+b)/2$. The *effective* half-spread uses the trade price $p$ against the mid: $c=|p-m|$. Round-trip cost ≈ $2c$.

**Roll (1984) estimator.** If trades bounce between bid and ask, successive *transaction-price changes* carry negative autocovariance whose magnitude is the half-spread squared:

$$\operatorname{cov}(\Delta p_t,\Delta p_{t-1})=-c^2 \quad\Longrightarrow\quad S_R = 2\sqrt{-\operatorname{cov}(\Delta p_t,\Delta p_{t-1})}.$$

**Amihud (2002) ILLIQ.** The average absolute price change per dollar of volume:

$$\text{ILLIQ}_{iy}=\frac{1}{D_{iy}}\sum_{t=1}^{D_{iy}}\frac{|R_{iyt}|}{\text{VOLD}_{iyt}}.$$

It is a **Kyle-lambda-like price-impact** measure built from daily data — the slope of price response to order flow, averaged over days. More illiquid ⇒ larger ILLIQ.

**Amivest / turnover.** Liquidity ratio $=\dfrac{\sum_t \text{VOLD}_t}{\sum_t |R_t|}$ (the *inverse* of a volume-weighted ILLIQ); turnover $=\text{volume}/\text{shares outstanding}$ measures how much of the float actually trades.

**The economic content.** ILLIQ dominates empirical work because (Amihud 2002) it is computable for long histories in most markets, where spread data does not exist. Its cost: it mixes the *level* of price impact with idiosyncratic return volatility (a volatile stock has high ILLIQ even if deeply liquid).

---

### 3. Computational Implementation — the measures in numbers

**Experiment 1 — Amihud ILLIQ across market cap.** A small cap (big moves, tiny volume) vs a mega cap (small moves, huge volume):

```python
import math, random

def amihud_illiq(returns, dollar_vol):
    """Amihud ILLIQ = mean(|daily return| / daily dollar volume)."""
    vals = [abs(r)/v for r, v in zip(returns, dollar_vol) if v > 0]
    return sum(vals)/len(vals) if vals else float('nan')

random.seed(1)
small_ret = [random.gauss(0.0010, 0.030) for _ in range(252)]
small_vol = [random.uniform(1e6, 5e6)   for _ in range(252)]
mega_ret  = [random.gauss(0.0004, 0.010) for _ in range(252)]
mega_vol  = [random.uniform(5e8, 1e9)   for _ in range(252)]
i_small = amihud_illiq(small_ret, small_vol)
i_mega  = amihud_illiq(mega_ret,  mega_vol)
print(f"Amihud ILLIQ small-cap = {i_small:.4e}  (|% price change| per $ volume)")
print(f"Amihud ILLIQ mega-cap  = {i_mega:.4e}")
print(f"ratio small/mega = {i_small/i_mega:,.0f}x")
```
```
Amihud ILLIQ small-cap = 9.4050e-09  (|% price change| per $ volume)
Amihud ILLIQ mega-cap  = 1.0969e-11
ratio small/mega = 857x
```
The same absolute price response per *unit* of volume is ~**850×** steeper in the small cap — its price is far more sensitive to order flow, which is precisely the "illiquidity" the asset-pricing literature prices.

**Experiment 2 — Roll spread from a bid-ask bounce.** Build a price path that trades at bid/ask around a slowly-moving mid, then recover the spread from the autocovariance alone:

```python
import math, random

def roll_spread(prices):
    dp  = [prices[i]-prices[i-1] for i in range(1, len(prices))]
    m   = sum(dp)/len(dp)
    acov= sum((dp[i]-m)*(dp[i-1]-m) for i in range(1,len(dp)))/(len(dp)-1)
    return 2*math.sqrt(max(-acov, 0.0)), acov

def gen_bidask_path(T, c, mu, sig):   # half-spread c around a drifting mid
    mid = 100.0; path = []
    for _ in range(T):
        mid *= math.exp(random.gauss(mu, sig))
        path.append(mid + random.choice([-c, c]))
    return path

random.seed(3)
rA, aA = roll_spread(gen_bidask_path(20000, 0.02, 0.0, 0.001))
rB, aB = roll_spread(gen_bidask_path(20000, 0.20, 0.0, 0.001))
print(f"true full spread 0.04 -> Roll est={rA:.4f}  (autocov={aA:.5f})")
print(f"true full spread 0.40 -> Roll est={rB:.4f}  (autocov={aB:.5f})")
```
```
true full spread 0.04 -> Roll est=0.0350  (autocov=-0.00031)
true full spread 0.40 -> Roll est=0.3994  (autocov=-0.03988)
```
With fundamental moves small relative to the spread, Roll recovers the true spread (0.035 vs 0.04; 0.399 vs 0.40). The negative autocovariance is the fingerprint of the bounce — see [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & Roll]] for the full model and its breakdown when autocovariance is positive.

---

### 4. Failure Modes & First-Principles Breakdowns

- **ILLIQ confounds volatility with illiquidity.** $|R|/\text{VOLD}$ is high for a volatile but deep stock; it is a *noisy* proxy for true price impact. Scale matters — values differ by orders of magnitude across cap sizes, so compare within, not across, groups.
- **Zero-volume days are undefined.** ILLIQ drops days with no volume; for infrequently traded names that discards most of the sample and biases the average.
- **Roll needs negative autocovariance.** When price changes are positively autocorrelated (trends, momentum), $\sqrt{-(\text{positive})}$ is undefined and the estimator clamps to zero — wrongly declaring "infinite liquidity." See [[pillars/06-market-making/liquidity-risk-and-asset-pricing/05-failure-modes-and-practice|05 · Failure Modes]].
- **Spreads miss depth.** A tight quoted spread is worthless if you cannot trade size at it; spread measures capture the *cost of a small trade*, ILLIQ/Kyle capture the *price impact of order flow*.

---

### 5. Canonical Literature & Study References

- **Amihud (2002).** *Illiquidity and stock returns.* JFM 5, 31–56 — the ILLIQ definition, eq. (1), and its robustness.
- **Roll (1984).** *A simple implicit measure of the effective bid-ask spread.* Journal of Finance 39, 1127–1139 — the autocovariance estimator.
- **Amihud, Mendelson & Pedersen (2013).** *Market Liquidity*, Ch 3 — the full catalogue of measures and their relative merits.
- **Hasbrouck.** *Market Microstructure: Foundations*, Ch 3 (Roll, effective spreads) and Ch 5 (price impact, ILLIQ).

---

### 6. Connected Graph Bridges

- Next: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/03-liquidity-as-a-priced-factor|03 · Liquidity as a Priced Factor]]
- Back: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Index Hub]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/01-from-zero-intuition|01 · From Zero]]
- Sibling: [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & Roll Model]] · [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth (Kyle)]]
