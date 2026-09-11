---
title: "6.8.5 Failure Modes & Real-World Practice"
tags:
  - pillar-market-making
  - liquidity-risk-and-asset-pricing
  - failure-modes
  - measurement-error
  - liquidity-spiral
---

**Basic Prerequisites:** [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]] and [[pillars/06-market-making/liquidity-risk-and-asset-pricing/04-liquidity-risk-and-crises|04 · Liquidity Risk & Crises]].

---

### 1. Intuition & Practical Objective

Liquidity work is measurement work, and the measurements are fragile. This page names the three ways the whole enterprise breaks down, so a practitioner knows *which number to distrust and why*:

1. **Measurement error** — every proxy is a noisy stand-in for true price impact; ILLIQ is undefined on zero-volume days and conflates volatility with illiquidity.
2. **The Roll-estimator collapse** — the autocovariance trick returns "infinite liquidity" (an estimate of zero) whenever price changes are positively autocorrelated, which is common in trending/momentum markets.
3. **Commonality, regime dependence & the spiral** — the *level* of measured risk is not the *risk of the level*; the covariances that matter only appear in crises, and they feed the funding spiral.

The objective is not cynicism: it is knowing *which* of your numbers can quietly be wrong, and the discipline of stress-testing a liquidity measurement before pricing it.

---

### 2. Mathematical Ground Truth & Derivations

**The Roll failure.** Roll (1984) recovers the half-spread as $c=\sqrt{-\operatorname{cov}(\Delta p_t,\Delta p_{t-1})}$. The estimator is only valid when the autocovariance is *negative* (the bid-ask bounce). If instead price changes are positively autocorrelated,

$$
\operatorname{cov}(\Delta p_t,\Delta p_{t-1})>0 \;\Longrightarrow\; \sqrt{-(\text{positive})}\;\text{is undefined},
$$

and implementations clamp to $0$ — reporting an asset as perfectly liquid when it is anything but. Positive autocovariance arises whenever the fundamental price trends (momentum) or when inventory effects are weak relative to news, i.e. precisely when the Roll assumptions fail.

**The ILLIQ instability.** Amihud ILLIQ is $|R_t|/\text{VOLD}_t$, averaged only over days with volume. On a zero-volume day the ratio is undefined; for thinly traded names most days are dropped, so the estimate rests on few observations and is dominated by whichever days did trade. It also scales with return *volatility*, not just price impact — a volatile, deep stock looks "illiquid."

**The spiral (why risk is not the level).** Measured illiquidity $\bar{c}$ is a calm-times average. The *priced* risk is the covariance of returns/illiquidity with market illiquidity in the tail, which is essentially invisible in the average. Because illiquidity is common and pro-cyclical, the true risk of a crisis far exceeds what a level measure or a calm-sample beta can see — and it feeds back through funding: forced sales raise realized illiquidity, which raises margin calls, which forces more sales ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|the funding spiral]]).

---

### 3. Computational Implementation — the failures in numbers

**Experiment 1 — Roll clamps to zero on positive autocovariance.** A trending (momentum) price path has *positive* price-change autocovariance, so Roll reports "infinite liquidity":

```python
import random, statistics, math
random.seed(5)
dp, p = [], 100.0
for _ in range(2000):                       # momentum: dp_t has +0.6*AR(1) term
    shock = random.gauss(0.0, 0.01) + 0.6*(dp[-1] if dp else 0.0)
    dp.append(shock); p += shock
m = statistics.mean(dp)
acov = sum((dp[i]-m)*(dp[i-1]-m) for i in range(1,len(dp)))/(len(dp)-1)
print(f"price-change autocovariance = {acov:+.5f}")
print(f"Roll estimate = {2*math.sqrt(max(-acov,0.0)):.5f}  (clamped -> 'infinitely liquid')")
```
```
price-change autocovariance = +0.00009
Roll estimate = 0.00000  (clamped -> 'infinitely liquid')
```
The positive autocovariance makes $\sqrt{-\text{cov}}$ undefined; a naive implementation returns **0** — a trending, actively-traded stock mislabeled as free to trade. **Roll is only valid where the bounce dominates the trend.**

**Experiment 2 — ILLIQ with zero-volume days.** Days with no volume are silently dropped, biasing the average:

```python
zero_vol = [0.0, 0.0, 2e6, 1e6, 0.0, 5e5]
zero_ret = [0.005, -0.004, 0.001, 0.002, 0.0, -0.001]
vals = [abs(r)/v for r, v in zip(zero_ret, zero_vol) if v > 0]
print(f"ILLIQ over usable days = {sum(vals)/len(vals):.3e}  ({len(vals)}/{len(zero_vol)} days used)")
```
```
ILLIQ over usable days = 1.500e-09  (3/6 days used)
```
Half the sample vanished. For an infrequently-traded stock this fraction is far worse, and the surviving days are exactly the *active* ones — so measured ILLIQ reflects the easy-to-measure days and silently drops the illiquidity of the quiet ones.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Measurement error / proxy risk.** Every proxy estimates *something* about the cost of trading, but none is true price impact. ILLIQ conflates volatility with illiquidity; spreads miss depth; Roll breaks under trends. Any single number can be wrong by construction.
2. **Roll's sign assumption fails.** Negative autocovariance is required; positive autocovariance (momentum, weak inventory) produces undefined or zero estimates — the asset looks *more* liquid than it is.
3. **Zero-volume bias.** ILLIQ silently drops non-trading days; thinly traded names are measured on their most active days only, biasing illiquidity *down*.
4. **Regime dependence / tail risk.** Betas and levels estimated in calm markets miss the crisis-state covariances that actually matter — the priced risk lives in the tail and the average hides it.
5. **The spiral is a feedback, not a number.** Falling prices → forced sales → wider spreads/impact → more margin → more sales. No static measure captures this; it is a *dynamics* failure that the level-vs-risk distinction and the [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|margin spiral]] page make concrete.

---

### 5. Canonical Literature & Study References

- **Roll (1984).** *A simple implicit measure of the effective bid-ask spread.* Journal of Finance 39 — the estimator and its identification condition (negative autocovariance).
- **Amihud (2002).** *Illiquidity and stock returns.* JFM 5 — ILLIQ's construction, robustness, and its known limits (volatility confounding, data availability).
- **Chordia, Roll & Subrahmanyam (2000).** *Commonality in liquidity.* JFE 56 — why the common factor defeats diversification and breaks level-based thinking.
- **Brunnermeier & Pedersen (2009).** *Market liquidity and funding liquidity.* RFS 22 — the spiral that makes tail liquidity risk self-amplifying.
- **Acharya & Pedersen (2005); Amihud, Mendelson & Pedersen (2013).** — the priced-risk view these failures warn you to stress-test.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/04-liquidity-risk-and-crises|04 · Liquidity Risk & Crises]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Index Hub]]
- Forward: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/06-advanced-extensions|06 · Advanced Extensions]]
- Funding spiral: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]
