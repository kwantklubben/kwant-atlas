---
title: "03 — Pairs Selection & Hedging: Distance Method vs Cointegration"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - pairs-selection
  - hedge-ratio
  - distance-method
  - market-neutral
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/02-cointegration-and-the-spread|02 · Cointegration & the Spread]].

---

### 1. Intuition & Practical Objective

A trading rule is only as good as the pair it is applied to. This page answers the two questions that come *before* any signal: **which two assets?** and **in what ratio?** There are two schools:

- **Distance method (Gatev, Goetzmann & Rouwenhorst, 2006)** — a nonparametric screen. Normalise each price to a cumulative-return index, compute the sum of squared deviations between every pair, and trade the closest pairs. It assumes $y$ and $x$ move together *in levels* (implicitly $\beta=1$ on the normalised index). Cheap, robust, but it ignores the statistical structure of the spread.
- **Cointegration method (Vidyamurthy 2004; Avellaneda & Lee 2010)** — estimate the equilibrium relationship formally, test the residual for stationarity, and trade the *residual* of a regression (or of a factor decomposition). More sound econometrically, but more parameters to over-fit.

The *hedge ratio* is the bridge: the distance method's "buy one, sell one" is the special case $\beta=1$ of the regression hedge. Getting $\beta$ right is what makes the book **market-neutral** — zero exposure to the systematic factors.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The distance method (GGR 2006, §2.1)

Let $P^i_t$ be the normalised cumulative total-return index of stock $i$ over the formation window (start $=1$). For every candidate pair $(i,j)$,

$$D_{ij}=\sum_{t=1}^{M}\big(P^i_t-P^j_t\big)^2 .$$

Rank all pairs by $D_{ij}$ and trade the top $n$ (GGR study the top 5 and top 20, plus pairs 101–120 as a control). Matching in normalised price space is equivalent to assuming a cointegrating vector with two nonzero coordinates and unit scale — "the sum or difference of scaled prices will be reverting to zero" (GGR §1.4). The **danger flagged by GGR itself**: normalisation is not a test, and spuriously correlated prices will pass.

#### 2.2 The regression hedge ratio

If we accept the cointegrating model $y_t=\mu+\beta x_t+z_t$, the OLS estimate is

$$\hat\beta=\frac{\widehat{\operatorname{Cov}}(y,x)}{\widehat{\operatorname{Var}}(x)},\qquad \hat\mu=\bar y-\hat\beta\bar x .$$

The **market-neutral portfolio** (long \$1 of $y$, short \$\hat\beta of $x$) has return equal to the idio residual:

$$r_{p,t+1}=r^{y}_{t+1}-\hat\beta\,r^{x}_{t+1}\approx \Delta z_{t+1},$$

so its exposure to any factor $F$ loading $\beta^y_F,\beta^x_F$ cancels when $\hat\beta=\beta^y_F/\beta^x_F$. In log-price space, $\Delta z_{t+1}=\Delta\ln y_{t+1}-\hat\beta\,\Delta\ln x_{t+1}$ is the portfolio return of the dollar-neutral book.

#### 2.3 Factor-neutral generalisation (Avellaneda–Lee 2010)

Pairs trading is the two-asset case of a broader **statistical arbitrage**: decompose each stock's return against systematic factors,

$$R_i=\sum_{j=1}^{m}\beta_{ij}F_j+\tilde R_i,$$

and trade the idiosyncratic residual $\tilde R_i$. The factors $F_j$ can be **sector ETFs** (each stock regressed on its peers' ETF, $\beta_{ij}=\operatorname{Cov}(R_i,R_{I_j})/\operatorname{Var}(R_{I_j})$) or **PCA eigenportfolios** (eigenvectors of the return correlation matrix; weights $Q^{(j)}_i=v^{(j)}_i/\sigma_i$). A portfolio $\{Q_i\}$ is market-neutral iff $\sum_i\beta_{ij}Q_i=0$ for all $j$; the first eigenportfolio is the market, higher eigenportfolios are interpretable long–short sector bets ("coherence").

#### 2.4 Distance vs cointegration — when they agree

On normalised prices, the distance metric $D_{ij}$ is minimised by the pair whose *level* spread is tightest. If the true relationship is $y=\mu+\beta x+z$ with $\beta\approx1$ and small $\operatorname{Var}(z)$, distance and cointegration agree. When $\beta\neq1$ (different volatilities/leverage), distance systematically mis-hedges and the regression hedge is required.

---

### 3. Computational Implementation — the distance screen and the hedge ratio

Stdlib only. Build a small synthetic universe: four stocks on factor A (with stationary idio), three on factor B, and one unrelated loner. The distance screen should recover the *within-sector* pairs, and the top pair's OLS hedge ratio should be close to $1$ on the normalised index.

```python
import math, random

def rand_walk(n, rng):
    x=0.0; out=[]
    for _ in range(n): x+=rng.gauss(0,1); out.append(x)
    return out

n=252; rng=random.Random(3)
fA=rand_walk(n,rng); fB=rand_walk(n,rng); stocks={}
for k in range(4):
    e=[0.0]*n
    for t in range(1,n): e[t]=0.8*e[t-1]+rng.gauss(0,0.4)
    stocks[f"A{k}"]=[fA[t]+e[t] for t in range(n)]
for k in range(3):
    e=[0.0]*n
    for t in range(1,n): e[t]=0.8*e[t-1]+rng.gauss(0,0.4)
    stocks[f"B{k}"]=[fB[t]+e[t] for t in range(n)]
stocks["Z"]=rand_walk(n,rng)

def norm(p):                                  # Gatev normalised cumulative index
    out=[1.0]
    for t in range(1,n): out.append(out[-1]*(1+(p[t]-p[t-1])/100.0))
    return out
P={k:norm(v) for k,v in stocks.items()}; names=sorted(P)

pairs=[]
for i in range(len(names)):
    for j in range(i+1,len(names)):
        d=sum((P[names[i]][t]-P[names[j]][t])**2 for t in range(n))
        pairs.append((d,names[i],names[j]))
pairs.sort()
print("Gatev distance method — 5 closest pairs (sum of squared deviations):")
for d,a,b in pairs[:5]: print(f"  {a}-{b}: distance={d:.4f}")

d0,a0,b0=pairs[0]; pa,pb=P[a0],P[b0]
mpa=sum(pa)/n; mpb=sum(pb)/n
beta=sum((pa[t]-mpa)*(pb[t]-mpb) for t in range(n))/sum((pb[t]-mpb)**2 for t in range(n))
print(f"top pair {a0}-{b0}: OLS hedge ratio beta={beta:.4f} (distance method implicitly uses beta=1)")
```
```
Gatev distance method — 5 closest pairs (sum of squared deviations):
  A2-A3: distance=0.0116
  A1-A3: distance=0.0122
  A0-A3: distance=0.0129
  A0-A2: distance=0.0158
  A1-A2: distance=0.0175
top pair A2-A3: OLS hedge ratio beta=0.9985 (distance method implicitly uses beta=1)
```

Every top-5 pair is **within sector A** — the screen correctly identifies the comoving block and never touches the loner `Z`. The OLS hedge ratio on the normalised indices is $\hat\beta=0.9985\approx1$, confirming that for this pair the distance method's implicit unit hedge is essentially correct.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Selection is a multiple test.** Screening $N$ stocks gives $N(N-1)/2$ pairs; the "best" distance is an extreme order statistic and is biased toward spurious fits. GGR mitigate this by fixing the formation/trading split *ex ante*; modern practice uses the Deflated Sharpe Ratio ([[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene]]).
2. **Distance ignores $\beta$.** Normalised-price matching forces $\beta=1$; a pair with different volatilities is mis-hedged, leaving residual factor exposure that surfaces as a directional loss in a market move.
3. **Economic link ≠ statistical link.** Same-sector stocks can have different regulatory, leverage or commodity exposure. The distance screen finds *optical* comovement; a structural break in the link (Ch 5) is invisible to it.
4. **Factor model choice drives the residuals (Avellaneda–Lee).** PCA vs ETF factors give different residuals and hence different P&L; ETF weights are biased to large caps, PCA factors are not, and the number of significant eigenvalues is itself time-varying.
5. **Look-ahead in normalisation.** Using the *entire* sample to normalise prices leaks future information into the formation window. Normalise strictly on the formation period.

---

### 5. Canonical Literature & Study References

- **Gatev, Goetzmann & Rouwenhorst**, *RFS* 19(3), 2006 — §2.1 pairs formation (minimum distance in normalised cum-dividend price space), §1.4 cointegration interpretation.
- **Avellaneda, M. & Lee, J.-H.**, *Quantitative Finance* 10(7), 2010 — §2 (PCA vs ETF factor extraction, market-neutrality condition Eq. 6, eigenportfolios Eq. 9), §3 (residual model Eq. 10–11).
- **Vidyamurthy, G.**, *Pairs Trading: Quantitative Methods and Analysis*, Wiley, 2004 — the univariate cointegration approach to pair selection.
- **Krauss, C.**, *Journal of Economic Surveys* 31(2), 2017 — §2 distance approach, §3 cointegration approach, and the finding that the cointegration method "outperforms the distance method" after risk loadings and costs (Dunis & Ho).
- **Tsay**, *Analysis of Financial Time Series*, Ch 8 §8.5 — spurious-correlation caveat in pair matching.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/02-cointegration-and-the-spread|02 · Cointegration & the Spread]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/04-trading-rules-and-backtest|04 · Trading Rules & Backtest]]
- Sibling: [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]] (factor definitions that drive the residual) · [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman Filtering]] (time-varying $\beta$)
- Portfolio: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]
