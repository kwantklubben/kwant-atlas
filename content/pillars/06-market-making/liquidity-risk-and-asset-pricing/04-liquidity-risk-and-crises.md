---
title: "04 - Liquidity Risk & Crises: Acharya-Pedersen and Commonality"
tags:
  - pillar-market-making
  - liquidity-risk-and-asset-pricing
  - liquidity-risk
  - commonality
  - flight-to-quality
---

**Basic Prerequisites:** [[pillars/06-market-making/liquidity-risk-and-asset-pricing/03-liquidity-as-a-priced-factor|03 · Liquidity as a Priced Factor]] and [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (Pillar 4).

---

### 1. Intuition & Practical Objective

The single most dangerous fact about liquidity is that it is **common and pro-cyclical**: illiquidity rises across *all* assets in bad times, so you cannot diversify it away by holding many illiquid assets — they all become illiquid together. This page makes that precise in three ways:

1. **Commonality** — a large fraction of a stock's illiquidity moves with *market* illiquidity (Chordia, Roll & Subrahmanyam 2000).
2. **The liquidity-adjusted CAPM** — Acharya & Pedersen (2005) show that expected return depends not just on the asset's own illiquidity but on **three covariances**: with market illiquidity, of its return with market illiquidity, and of its illiquidity with the market return.
3. **Crises & flight to quality** — when these covariances spike (2007–08, 2020), the premium jumps and liquidity provision vanishes; investors flee to Treasuries and the spread between liquid and illiquid assets explodes.

The objective: understand *why* liquidity risk cannot be hedged by diversification, and be able to estimate the three betas that capture the risk.

---

### 2. Mathematical Ground Truth & Derivations

**Commonality in liquidity.** Regress stock $i$'s illiquidity innovation on the market's:

$$\Delta \text{ILLIQ}_{i,t}=\alpha_i+\beta_i\,\Delta \text{ILLIQ}_{M,t}+\varepsilon_{i,t}.$$

The $R^2$ (and average $\beta_i$) measures how much of each stock's liquidity variation is a *systematic* market-wide shock. Chordia et al. find a large common component; the practical consequence is that liquidity risk is largely undiversifiable.

**The Acharya–Pedersen liquidity-adjusted CAPM.** Define $r^i$ = return, $c^i$ = relative illiquidity cost, $r^M$ = market return, $c^M$ = market illiquidity. The required excess return is

$$E_t(r^i_{t+1})=r^f+E_t(c^i_{t+1})+\lambda_t\left[
\frac{\operatorname{cov}_t(r^i,r^M)}{\operatorname{var}(r^M-c^M)}
+\frac{\operatorname{cov}_t(c^i,c^M)}{\operatorname{var}(r^M-c^M)}
-\frac{\operatorname{cov}_t(r^i,c^M)}{\operatorname{var}(r^M-c^M)}
-\frac{\operatorname{cov}_t(c^i,r^M)}{\operatorname{var}(r^M-c^M)}\right],$$

where the four betas share the same denominator (the variance of the *net* market return $r^M-c^M$). The three liquidity-risk betas:

- **$\beta_1=\operatorname{cov}(c^i,c^M)/\operatorname{var}(r^M-c^M)$** — *commonality*: asset illiquid when the market is illiquid ⇒ **higher** required return (positive premium).
- **$\beta_2=\operatorname{cov}(r^i,c^M)/\operatorname{var}(r^M-c^M)$** — *return-vs-liquidity* (the PS channel): return high when market illiquid ⇒ **lower** required return (negative premium).
- **$\beta_3=\operatorname{cov}(c^i,r^M)/\operatorname{var}(r^M-c^M)$** — *down-market liquidity*: asset stays liquid when the market falls ⇒ **lower** required return (negative premium).

**Crises.** In a crisis, $c^M$ spikes and its covariation with both $r^M$ and asset illiquidities increases, so the *priced* covariances rise precisely when risk aversion is highest — the liquidity premium becomes large exactly when you need to be compensated most. This is the asset-pricing reflection of the [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|funding/margin spiral]].

---

### 3. Computational Implementation — the three liquidity-risk betas

Simulate a market where illiquidity rises in down markets, and a stock that shares market illiquidity (positive commonality) yet stays liquid when the market falls. Estimate all three betas and confirm the signs the theory predicts. Stdlib only.

```python
import random, statistics

def cov(x, y):
    mx=statistics.mean(x); my=statistics.mean(y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/(len(x)-1)

random.seed(11)
T = 240
rM = [random.gauss(0.01, 0.020) for _ in range(T)]
# market illiquidity rises when the market return falls (crisis channel)
cM = [max(0.0005, 0.008 - 0.05*rM[t] + random.gauss(0,0.001)) for t in range(T)]
# stock: strong commonality in illiquidity, beta-3 "liquid when market falls" profile
r_i = [0.9*rM[t] + random.gauss(0,0.01) for t in range(T)]
c_i = [1.0*cM[t] + random.gauss(0,0.0002) for t in range(T)]

net = [rM[t]-cM[t] for t in range(T)]
net_var = statistics.variance(net)               # var(r^M - c^M), common denominator
b1 = cov(c_i, cM)/net_var                        # commonality in liquidity
b2 = cov(r_i, cM)/net_var                        # return vs market liquidity (PS)
b3 = cov(c_i, rM)/net_var                        # illiquidity vs market return
print(f"var(net mkt r^M-c^M) = {net_var:.5f}")
print(f"beta1 = cov(c^i,c^M)/varnet = {b1:+.4f}  (POSITIVE premium -> riskier)")
print(f"beta2 = cov(r^i,c^M)/varnet = {b2:+.4f}  (NEGATIVE premium -> safer)")
print(f"beta3 = cov(c^i,r^M)/varnet = {b3:+.4f}  (NEGATIVE premium -> safer)")
```
```
var(net mkt r^M-c^M) = 0.00050
beta1 = cov(c^i,c^M)/varnet = +0.0043  (POSITIVE premium -> riskier)
beta2 = cov(r^i,c^M)/varnet = -0.0440  (NEGATIVE premium -> safer)
beta3 = cov(c^i,r^M)/varnet = -0.0468  (NEGATIVE premium -> safer)
```
The signs are exactly as theory requires: because the stock's illiquidity shares the market's commonality ($\beta_1>0$, the risk channel) but its *return* is high when the market is illiquid ($\beta_2<0$) and it stays *liquid* when the market falls ($\beta_3<0$, the two hedge channels), the three channels pull required return in opposite directions — and the sign of the net premium is an empirical question per asset.

---

### 4. Failure Modes & First-Principles Breakdowns

- **Commonality defeats diversification.** Holding many illiquid assets does not diversify liquidity risk because their illiquidities all load on the same market factor — you are long a single bet.
- **Betas estimated in calm times mislead.** If you estimate $\beta_2,\beta_3$ from a low-volatility sample, you miss the crisis-state covariances that are the whole point. This is a *regime-dependence* failure: the risk is in the tail, not the average.
- **Flight to quality is a correlated bet.** "Safe" assets (Treasuries) see their *liquidity* improve and their price rise exactly when everything else dries up — so the flight itself is what makes the illiquid side so costly.
- **The funding link.** The covariance spikes in a crisis are driven by the [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|margin spiral]] (leverage → forced sales → more illiquidity) — the asset-pricing betas here are the *shadow* of the funding constraint's failure.

---

### 5. Canonical Literature & Study References

- **Acharya & Pedersen (2005).** *Asset pricing with liquidity risk.* JFE 77(2), 375–410. The full model, Proposition 1, and the three betas; empirical premia for each channel.
- **Chordia, Roll & Subrahmanyam (2000).** *Commonality in liquidity.* JFE 56, 3–28. The empirical fact of a market-wide liquidity factor.
- **Pástor & Stambaugh (2003).** *Liquidity risk and expected stock returns.* JPE 111(3) — the $\beta_2$ channel's big empirical payoff (7.5%/yr).
- **Bao, Pan & Wang (2011).** *The illiquidity of corporate bonds.* Journal of Finance 66(3) — commonality and the crisis spike in the bond market (page 06).
- **Amihud, Mendelson & Pedersen (2013).** *Market Liquidity*, Ch 4 (liquidity risk) and Ch 6 (crises) — the crisis narrative in one volume.

---

### 6. Connected Graph Bridges

- Next: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/06-advanced-extensions|06 · Advanced Extensions]]
- Back: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/03-liquidity-as-a-priced-factor|03 · Liquidity as a Priced Factor]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Index Hub]]
- Funding spiral: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]]
