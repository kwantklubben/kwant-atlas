---
title: "03 — Threshold Models: SETAR & STAR (Observed-State Regimes)"
tags:
  - pillar-quant-research
  - regime-detection
  - setar
  - star
  - threshold
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (AR models, stationarity, ergodicity) and [[pillars/01-quantitative-research/regime-detection/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Markov-switching ([[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · MS]]) treats the regime as *latent* — you never see it. **Threshold models flip this: the regime is *observable* (or nearly so), because it is decided by a lagged value of the observed series crossing a threshold.** If returns (or some state variable like a drawdown measure) are below a level $\gamma$, you are in the low regime; above it, in the high regime. No hidden coin — the data itself flips the switch.

Two families (Tsay Ch 4, verified):

1. **SETAR — Self-Exciting Threshold AR.** The AR coefficients switch discontinuously when the delay-$d$ lag $x_{t-d}$ crosses $\gamma$:
$$x_t=\phi_0^{(j)}+\sum_{i}\phi_i^{(j)}x_{t-i}+a_t^{(j)}\quad\text{if } \gamma_{j-1}\le x_{t-d}<\gamma_j.$$
The regime is *fully observed* once $x_{t-d}$ is known. This gives threshold models a forecasting advantage Hamilton flags: **when the threshold variable is observed, the next regime is known with certainty** (SETAR is a *single* model at horizon $\le d$); Markov-switching always produces a mixture.

2. **STAR — Smooth Transition AR.** Replaces the hard cut with a smooth transition function $0\le F\le1$ (logistic or exponential):
$$x_t=c_0+\sum_i\phi_{0,i}x_{t-i}+F\Big[\frac{x_{t-d}-\ell}{s}\Big]\Big(c_1+\sum_i\phi_{1,i}x_{t-i}\Big)+a_t,$$
so the conditional mean is a **weighted combination of two linear models** with weight $F$. The logistic transition $F(z)=1/(1+e^{-z})$ is $0$ for very negative $x$, $1$ for very positive, and $1/2$ at the location $\ell$ with slope controlled by $s$.

**Practical objective:** when you can name the switching variable (e.g., vol-level or drawdown state), threshold models estimate the threshold and the per-regime dynamics directly — cleaner than forcing a hidden Markov state. Tsay's threshold-cointegration application (S&P 500 futures basis, Ch 8 §8.7) finds thresholds $\hat\gamma_1=-0.0226,\hat\gamma_2=0.0377$: outside the no-arbitrage band the ECM binds, inside it does not — a classic "regime = active vs inactive" story.

---

### 2. Mathematical Ground Truth & Derivations

**SETAR($2;d$) ergodicity (Tsay Ch 4, verified).** For a TAR(1) with threshold variable $x_{t-1}$ (delay $d=1$), the two-regime process is ergodic if
$$\phi_1^{(1)}<1,\qquad \phi_1^{(2)}<1,\qquad \phi_1^{(1)}\cdot\phi_1^{(2)}<1 .$$
Note the *product* condition: one regime may have $\phi_1>1$ as long as the other compensates — a key difference from a single linear AR, where $|\phi_1|<1$ is required.

**Estimation (least squares).** For a fixed threshold $\gamma$, each regime is a linear regression on the observations whose $x_{t-d}$ falls on that side; total SSE is the sum over regimes. The threshold is then chosen by **grid search** over the observed values of $x_{t-d}$ (Tsay recommends candidate thresholds in the interior, e.g. the $8\%$–$92\%$ quantiles, to keep enough observations per regime):

$$\hat\gamma=\arg\min_{\gamma}\Big[\;\text{SSE}_1(\gamma)+\text{SSE}_2(\gamma)\Big],\qquad \text{SSE}_j=\sum_{t:\,x_{t-d}\in\text{regime }j}\big(x_t-\hat x_t\big)^2.$$

**SETAR vs Markov-switching — the forecasting contrast (Tsay, verified).** SETAR: if the horizon $\le d$ and $x_{t-d}$ is observed, the regime is known exactly, so the conditional mean is a *single* linear model. Only beyond horizon $d$ do you average over which regime might be entered. Markov-switching: the state is always latent, so the forecast is *always* a mixture. **Latent vs observed state is a modeling choice with real forecasting consequences.**

**STAR as a smooth generalization.** As the slope $s\to0$, the logistic $F\to$ a step function and STAR collapses to SETAR. The smooth version avoids the discontinuity (better for estimation and for regimes that transition gradually) at the cost of the weakly-identified parameters $(\ell,s)$.

---

### 3. Computational Implementation — SETAR threshold recovered exactly, STAR smooths it

**Part 1 — SETAR grid search.** Simulate a 2-regime AR(1) with a hard threshold at $\gamma=0$ (low regime $\phi=0.3$, high regime $\phi=0.9$), then recover the threshold and both regimes by grid search. Stdlib only.

```python
import math, random
random.seed(3)

gamma_true=0.0; a1,b1,a2,b2=0.05,0.30,-0.03,0.90; sig=0.10; T=600
x=[0.0]
for t in range(1,T):
    m=(a1+b1*x[-1]) if x[-1]<=gamma_true else (a2+b2*x[-1])
    x.append(m+random.gauss(0,sig))

def ols(X,yv):
    n=len(X); mx=sum(X)/n; my=sum(yv)/n
    b=sum((X[i]-mx)*(yv[i]-my) for i in range(n))/sum((X[i]-mx)**2 for i in range(n))
    a=my-b*mx; return a,b,sum((yv[i]-a-b*X[i])**2 for i in range(n))

Xt=[x[t-1] for t in range(1,T)]; yt=[x[t] for t in range(1,T)]
qs=sorted(set(round(float(v),3) for v in Xt))
qs=qs[int(0.08*len(qs)):int(0.92*len(qs))]          # interior candidate thresholds
best=None
for g in qs:
    X1=[Xt[i] for i in range(len(Xt)) if Xt[i]<=g]; y1=[yt[i] for i in range(len(Xt)) if Xt[i]<=g]
    X2=[Xt[i] for i in range(len(Xt)) if Xt[i]> g]; y2=[yt[i] for i in range(len(Xt)) if Xt[i]> g]
    s1=ols(X1,y1)[2]; s2=ols(X2,y2)[2]
    if best is None or s1+s2<best[0]: best=(s1+s2,g,ols(X1,y1),ols(X2,y2))
tot,g,(a1h,b1h,_),(a2h,b2h,_)=best
print(f"SETAR fit: threshold gamma={g:.3f}  (true {gamma_true})")
print(f"  regime1 (x<=g): a={a1h:+.4f} b={b1h:+.4f}   (true a={a1}, b={b1})")
print(f"  regime2 (x> g): a={a2h:+.4f} b={b2h:+.4f}   (true a={a2}, b={b2})")
print(f"  total SSE={tot:.3f}")
```
```
SETAR fit: threshold gamma=0.000  (true 0.0)
  regime1 (x<=g): a=+0.0581 b=+0.4012   (true a=0.05, b=0.3)
  regime2 (x> g): a=-0.0342 b=+0.8234   (true a=-0.03, b=0.9)
  total SSE=5.666
```
The grid search finds the threshold **exactly at $0.000$** and recovers both regimes' AR coefficients well — a sharp, unambiguous demonstration of how an *observed-state* regime model works.

**Part 2 — STAR smooths the hard threshold.** Fit a logistic-STAR to the *same* SETAR data and show it approximates the threshold with a smooth transition (midpoint $c\approx\gamma$) at nearly equal SSE.

```python
import math, random
random.seed(3)                       # same SETAR data as Part 1, regenerated here
gamma_true=0.0; a1,b1,a2,b2=0.05,0.30,-0.03,0.90; sig=0.10; T=600
x=[0.0]
for t in range(1,T):
    m=(a1+b1*x[-1]) if x[-1]<=gamma_true else (a2+b2*x[-1])
    x.append(m+random.gauss(0,sig))
Xt=[x[t-1] for t in range(1,T)]; yt=[x[t] for t in range(1,T)]

def fit_star(s,c,Xt,yt):
    F=[1/(1+math.exp(-(Xt[i]-c)/s)) for i in range(len(Xt))]
    Z=[[1.0,Xt[i],F[i],F[i]*Xt[i]] for i in range(len(Xt))]
    n=len(Z); k=4
    ZtZ=[[sum(Z[i][r]*Z[i][cc] for i in range(n)) for cc in range(k)] for r in range(k)]
    Zty=[sum(Z[i][r]*yt[i] for i in range(n)) for r in range(k)]
    A=[row[:]+[Zty[r]] for r,row in enumerate(ZtZ)]
    for col in range(k):
        piv=max(range(col,k),key=lambda r:abs(A[r][col])); A[col],A[piv]=A[piv],A[col]
        pv=A[col][col]; A[col]=[v/pv for v in A[col]]
        for r in range(k):
            if r!=col:
                f=A[r][col]; A[r]=[A[r][cc]-f*A[col][cc] for cc in range(k+1)]
    beta=[A[r][k] for r in range(k)]
    res=[yt[i]-(beta[0]+beta[1]*Xt[i]+beta[2]*F[i]+beta[3]*F[i]*Xt[i]) for i in range(n)]
    return sum(r*r for r in res), beta

best=None
for s in (0.05,0.10,0.20,0.30,0.50,0.80):
    for c in (-0.05,0.0,0.05,0.10):
        sse,beta=fit_star(s,c,Xt,yt)
        if best is None or sse<best[0]: best=(sse,s,c,beta)
sse,s,c,beta=best
print(f"STAR fit on the SAME SETAR data: best (c,s)=({c:+.2f},{s:.2f})  SSE={sse:.3f}")
print(f"  STAR SSE / SETAR SSE = {sse/5.666:.3f}  -> STAR smoothly approximates the hard break")
print(f"  transition midpoint c={c:+.2f} vs SETAR threshold gamma=0.0 (smooth generalizes the threshold)")
```
```
STAR fit on the SAME SETAR data: best (c,s)=(+0.00,0.05)  SSE=5.863
  STAR SSE / SETAR SSE = 1.035  -> STAR smoothly approximates the hard break
  transition midpoint c=+0.00 vs SETAR threshold gamma=0.0 (smooth generalizes the threshold)
```
The STAR midpoint lands at $0.00$ — right on the SETAR threshold — and reaches $1.035\times$ the SETAR SSE with a steep slope ($s=0.05$, nearly a step). **STAR is the smooth generalization of SETAR; the "regime" is a weighted blend, not a hard cut.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Threshold undefined under $H_0$.** Testing for a threshold is delicate: under the null of a *single* linear regime, the threshold $\gamma$ is not identified (the classic Davies problem), so a standard LR test statistic has no null distribution (Tsay Ch 4 notes this explicitly). Hypothesis tests must be simulated/bootstrap, not taken from $\chi^2$ tables.
2. **Ergodicity vs one-regime stability.** The two-regime process can be ergodic with one regime's AR coefficient above $1$ (the product condition). Practitioners who impose $|\phi|<1$ in *each* regime throw away valid nonlinear behavior; those who ignore it may simulate explosive paths. Understand which you are assuming.
3. **Weak identification of the smooth parameters $(c,s)$.** STAR's location and slope are only weakly identified (a broad, flat likelihood), so fitted $(c,s)$ bounce between runs even when in-sample SSE is nearly identical — unlike SETAR's sharply-identified threshold. Report the whole transition, not the point estimate.
4. **Threshold-variable choice.** The result depends on *which* lagged variable defines the regime and the delay $d$; misspecify the threshold variable and the "regimes" are artifacts. Cross-validate over candidate variables.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series*, 3rd ed. — Ch 4 §4.1 (SETAR Eq. 4.9, ergodicity condition, STAR Eq. 4.15, Markov-switching contrast §4.1.3) and Ch 8 §8.7 (threshold cointegration, S&P 500 basis thresholds). *Verified: tsay_ch4-6.md, tsay_ch7-9.md.*
- **Tong, Howell**: *Non-Linear Time Series* (1990) and *Threshold Models in Non-linear Time Series Analysis* (1983) — the origin of SETAR/threshold models (Tsay's Ch 4 frames Hamilton's Markov-switching as Tong's *stochastic* counterpart).
- **Teräsvirta, Timo**: *Specification, Estimation, and Evaluation of Smooth Transition Autoregressive Models*, JASA (1994) — STAR estimation and the logistic/exponential transition.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching]] · [[pillars/01-quantitative-research/regime-detection/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]] (the threshold-undefined-under-$H_0$ caveat)
- Contrast: [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching]] (latent state) and [[pillars/01-quantitative-research/regime-detection/04-hmm|04 · Hidden Markov Models]] (observed state vs hidden state modeling choice)
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (AR stationarity/ergodicity)
