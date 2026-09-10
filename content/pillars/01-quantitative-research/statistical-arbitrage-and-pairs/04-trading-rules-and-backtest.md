---
title: "04 — Trading Rules, the z-score & a Full Pairs Backtest"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - trading-rules
  - s-score
  - backtest
  - sharpe
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/03-pairs-selection-and-hedge|03 · Pairs Selection & Hedge]] and [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/02-cointegration-and-the-spread|02 · Cointegration & the Spread]].

---

### 1. Intuition & Practical Objective

Once a pair and its hedge ratio are fixed, the strategy is a **rule on the spread**: open when the spread is far from equilibrium, close when it returns. The whole art is in two numbers — the *entry threshold* and the *exit threshold* — expressed in **standard deviations of the spread** so that the same constants work across every pair. This page gives the rule, the exact P&L identity of a dollar-neutral pair, and a **closed-form backtest** you can run and audit.

The standard deviation is the natural unit because the OU spread is Gaussian in equilibrium: a \$2\sigma$ excursion is expected to recur with a known frequency, and the *time* it takes to revert is governed by the half-life. Entry, exit and stop must all be consistent with $\tau_{1/2}$: entering a $2\sigma$ move in a spread with a 250-day half-life is not a trade, it is a position.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The z-score signal

Rolling on the formation window (or an expanding window), estimate $\mu_z,\sigma_z$ of the spread $z_t=y_t-\hat\beta x_t$, and define

$$Z_t=\frac{z_t-\mu_z}{\sigma_z}.$$

**Canonical rule** (the flat-file convention, made precise):

| Condition | Action |
|---|---|
| $Z_t>+2$ | **Short the spread**: short $y$, long $\hat\beta x$ |
| $Z_t<-2$ | **Long the spread**: long $y$, short $\hat\beta x$ |
| $\lvert Z_t\rvert<0.5$ | **Flat** (converged) |
| $\lvert Z_t\rvert\ge3.5$ | **Stop out** (possible cointegration break) |

The stop is not arbitrary: under a correct model, $\lvert Z\rvert\ge3.5$ should occur with probability $\approx0.05\%$ per observation, so its *repeated* occurrence is evidence the model has broken, not a bargain.

#### 2.2 The Avellaneda–Lee s-score (a drift-adjusted z-score)

Avellaneda & Lee define the dimensionless **s-score** from the OU parameters over a 60-day window,

$$s_i=\frac{X_i(t)-m_i}{\sigma_{\text{eq},i}},\qquad \sigma_{\text{eq},i}=\sqrt{\frac{\operatorname{Var}(\zeta)}{1-b^2}},$$

and trade: **open short if $s>+1.25$**, **open long if $s<-1.25$**, **close short at $s<+0.75$**, **close long at $s>-0.50$.** Including the drift $\alpha_i$ gives the "modified s-score" $s_{\text{mod},i}=s_i-\alpha_i\tau_i/\sigma_{\text{eq},i}$, which just shifts the thresholds by $\approx0.3$ in practice — the built-in momentum term.

#### 2.3 The P&L identity (why pairs trading is "free" of the market)

Long \$1 of $y$, short \$\hat\beta of $x$. In log-price space the one-period portfolio return is

$$r_{p,t+1}=\Delta\ln y_{t+1}-\hat\beta\,\Delta\ln x_{t+1}=\Delta z_{t+1}.$$

So the cumulative P&L is the change in the spread between entry and exit, and the market factor cancels to first order. Over the holding period from entry at level $z_{\text{in}}$ to exit at $z_{\text{out}}$ the gross P&L is $z_{\text{in}}-z_{\text{out}}$ (for a short-spread position), i.e. $\propto$ the number of standard deviations captured.

#### 2.4 Sharpe and the cost drag

With per-period returns $r_{p,t}$, the annualised Sharpe is

$$\text{SR}=\frac{\bar r_p}{\hat\sigma(r_p)}\sqrt{252}.$$

Transaction costs enter as $c\cdot\lvert\Delta\text{position}\rvert$ per change with $c\approx5$ bp **per leg** (10 bp round-trip for the two-leg book), and borrow cost on the short leg accrues daily. A pairs strategy's gross Sharpe is high; the net Sharpe is a *cost-and-turnover* phenomenon, which is exactly why the half-life matters (fast reversion → shorter holding → more turnover).

---

### 3. Computational Implementation — the backtest

**Experiment A — full formation/trading backtest.** We simulate a cointegrated pair (common log-price factor + stationary log-spread with $\phi=0.93$, half-life $\approx9.5$ days), estimate the hedge ratio and spread moments on a 252-day formation window, then trade the next 252 days with the $2\sigma/0.5\sigma/3.5\sigma$ rule. Stdlib only.

```python
import math, random

def ols(y, X):
    T=len(y); K=len(X)
    XtX=[[sum(X[i][t]*X[j][t] for t in range(T)) for j in range(K)] for i in range(K)]
    Xty=[sum(X[i][t]*y[t] for t in range(T)) for i in range(K)]
    A=[row[:]+[Xty[i]] for i,row in enumerate(XtX)]
    for c in range(K):
        p=max(range(c,K),key=lambda r:abs(A[r][c])); A[c],A[p]=A[p],A[c]
        for r in range(K):
            if r!=c:
                f=A[r][c]/A[c][c]
                for k in range(c,K+1): A[r][k]-=f*A[c][k]
    return [A[i][K]/A[i][i] for i in range(K)]

nf,nt=252,252; rng=random.Random(101)
f=[0.0]*(nf+nt)
for t in range(1,nf+nt): f[t]=f[t-1]+rng.gauss(0,0.01)
z=[0.0]*(nf+nt)
for t in range(1,nf+nt): z[t]=0.93*z[t-1]+rng.gauss(0,0.005)
lny=[f[t]+z[t] for t in range(nf+nt)]; lnx=f[:]

b0,b1=ols(lny[:nf],[[1.0]*nf,lnx[:nf]])
w=[lny[t]-b1*lnx[t] for t in range(nf+nt)]
m=sum(w[:nf])/nf; sd=math.sqrt(sum((s-m)**2 for s in w[:nf])/nf)

pos=0; pnl=0.0; cost=0.0; rets=[]; changes=0; stops=0; bp=0.0005
for t in range(nf,nf+nt):
    zs=(w[t]-m)/sd; newpos=pos
    if pos==0:
        if zs>2.0: newpos=-1
        elif zs<-2.0: newpos=1
    else:
        if abs(zs)<0.5: newpos=0
        elif abs(zs)>=3.5: newpos=0; stops+=1
    if newpos!=pos: changes+=1; cost+=bp*abs(newpos-pos)
    r=pos*(w[t]-w[t-1])/(1+abs(b1)); pnl+=r; rets.append(r); pos=newpos
mu=sum(rets)/len(rets); sdr=math.sqrt(sum((r-mu)**2 for r in rets)/len(rets))
print(f"formation hedge ratio beta={b1:.3f}  spread mean={m:+.4f}  sd={sd:.4f}")
print(f"trading: {changes} position changes, {stops} stop-outs")
print(f"total return (no cost) = {pnl*100:+.2f}%")
print(f"total return (costs)   = {(pnl-cost)*100:+.2f}%")
print(f"annualized Sharpe      = {mu/sdr*math.sqrt(252):+.2f}")
```
```
formation hedge ratio beta=0.928  spread mean=+0.0061  sd=0.0102
trading: 27 position changes, 8 stop-outs
total return (no cost) = +5.21%
total return (costs)   = +3.86%
annualized Sharpe      = +1.91
```

The book earns $+5.21\%$ gross over the year ($+3.86\%$ net of 10 bp round-trips) at a gross-exposure Sharpe of $+1.91$ — a market-neutral profile. Note the cost drag: $27$ position changes (i.e. $54$ leg-trades) cost $1.35\%$, about a quarter of the gross P&L. **Turnover is the enemy**, which is why the half-life screen matters.

**Experiment B — the Avellaneda–Lee s-score.** Estimate the OU parameters from a 60-day window and read today's s-score and half-life.

```python
import math, random

def ols(y, X):
    T=len(y); K=len(X)
    XtX=[[sum(X[i][t]*X[j][t] for t in range(T)) for j in range(K)] for i in range(K)]
    Xty=[sum(X[i][t]*y[t] for t in range(T)) for i in range(K)]
    A=[row[:]+[Xty[i]] for i,row in enumerate(XtX)]
    for c in range(K):
        p=max(range(c,K),key=lambda r:abs(A[r][c])); A[c],A[p]=A[p],A[c]
        for r in range(K):
            if r!=c:
                f=A[r][c]/A[c][c]
                for k in range(c,K+1): A[r][k]-=f*A[c][k]
    return [A[i][K]/A[i][i] for i in range(K)]

w=60; rng=random.Random(77)
rI=[rng.gauss(0,0.01) for _ in range(w)]
rS=[1.2*rI[t]+rng.gauss(0,0.006) for t in range(w)]
beta=ols(rS,[[1.0]*w,rI])
eps=[rS[t]-(beta[0]+beta[1]*rI[t]) for t in range(w)]
X=[]; acc=0.0
for e in eps: acc+=e; X.append(acc)
a,b=ols(X[1:],[[1.0]*(w-1),X[:-1]])
resi=[X[t+1]-(a+b*X[t]) for t in range(w-1)]
varz=sum(r*r for r in resi)/(w-2)
kappa=-math.log(b)*252; sigma_eq=math.sqrt(varz/(1-b*b)); s=(X[-1]-a/(1-b))/sigma_eq
print(f"OU 1-lag: a={a:+.3e}  b={b:.4f}")
print(f"kappa={kappa:.2f}/yr  half-life={math.log(2)/kappa*252:.2f} days")
print(f"s-score today = {s:+.3f}   (enter short spread if s > +1.25)")
```
```
OU 1-lag: a=+7.275e-04  b=0.8651
kappa=36.53/yr  half-life=4.78 days
s-score today = -0.462   (enter short spread if s > +1.25)
```

The estimated half-life is $4.78$ days (fast, well inside the $\kappa>252/30$ filter) and the s-score is $-0.462$ — inside the $\pm1.25$ entry band, so **no trade**: most of the time a well-behaved spread sits near equilibrium.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Thresholds fitted to the backtest.** Choosing $2\sigma/0.5\sigma/3.5\sigma$ because they maximise historical Sharpe is in-sample optimisation; the Deflated Sharpe Ratio corrects for exactly this ([[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene]]).
2. **The stop is a model-rejection test, not a loss cap.** Repeated $\lvert Z\rvert\ge3.5$ means the cointegration has broken; averaging down ("it must revert") is the classic way a market-neutral book dies.
3. **Costs scale with turnover, turnover scales with $1/\tau_{1/2}$.** A spread with a 5-day half-life can turn the book over every week; two legs of spread cost then dominate. Always report net-of-cost Sharpe.
4. **Non-synchronous legs.** If one leg trades thinly, the closing-price spread is stale and the backtest fills at prices you cannot get (GGR's bid-ask discussion). Use quotes or trade both legs simultaneously.
5. **Borrow and short availability.** The short leg may be unborrowable or expensive exactly when the signal is strongest (big divergence) — an unmodelled asymmetry.

---

### 5. Canonical Literature & Study References

- **Avellaneda, M. & Lee, J.-H.**, *Quantitative Finance* 10(7), 2010 — §4.1 pure mean-reversion signal (Eq. 15–16, cutoffs $1.25/0.75/0.50$), §4.2 drift-adjusted modified s-score; 10 bp round-trip cost assumption.
- **Gatev, Goetzmann & Rouwenhorst**, *RFS* 19(3), 2006 — §2.2 trading rule (open at two historical standard deviations, close at the next crossing), self-financing top-20 portfolio.
- **Tsay**, *Analysis of Financial Time Series*, Ch 8 §8.8 — pairs-trading rule (enter at $\mu_w-\delta$, unwind at $\mu_w+\delta$, net profit $2\delta-\eta$).
- **Krauss, C.**, *J. Economic Surveys* 31(2), 2017 — §4 time-series approach (optimal rules for mean-reverting spreads), transaction-cost sensitivity.
- **Gatev et al.** and **Do & Faff** for the empirical cost-adjusted Sharpe collapse.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/03-pairs-selection-and-hedge|03 · Pairs Selection & Hedge]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene & Deflated Sharpe]]
- Costs: [[pillars/05-portfolio-optimization/transaction-costs-and-turnover-constraints|Transaction Costs & Turnover Constraints]]
