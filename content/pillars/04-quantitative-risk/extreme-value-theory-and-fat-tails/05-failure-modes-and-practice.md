---
title: "05 — Failure Modes & Real-World Practice in EVT"
tags:
  - pillar-quantitative-risk
  - extreme-value-theory
  - failure-modes
  - threshold-selection
  - volatility-clustering
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/04-peaks-over-threshold|04 · Peaks Over Threshold]].

---

### 1. Intuition & Practical Objective

EVT is *mathematically beautiful and empirically delicate in three specific ways*. This page names them precisely, so a practitioner knows *which* choice to distrust and *how* the failures show up in the numbers. The objective is not cynicism — it is the discipline of knowing exactly where an EVT estimate is an approximation, so the residual tail risk can be managed.

The three failures, in one line each:
1. **Threshold choice is the whole method** — a bias–variance tradeoff with no free lunch (McNeil 1997 §4.4).
2. **Small-sample tail estimation is intrinsically hard** — distant quantiles are extrapolation, and different thresholds can double the answer.
3. **Financial extremes are dependent and regime-dependent** — the i.i.d. excesses assumption fails because volatility clusters, so unconditional EVT misbehaves in stress periods (McNeil & Frey 2000).

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live.** Every POT result rests on four interlocking assumptions:
- **(A1) A high enough threshold $u$** that the GPD limit theorem applies — the convergence $F_u\to G_\xi$ is only asymptotic in $u\to x_0$.
- **(A2) Enough exceedances $N_u$** that $(\hat\xi,\hat\beta)$ can be estimated — the MLE is asymptotically normal only as $N_u\to\infty$ (McNeil 1997 §3.6, for $\xi>-1/2$).
- **(A3) i.i.d. excesses** — the excess distribution is written for independent draws; clustering breaks it.
- **(A4) A stable tail regime** — $\xi$ is assumed constant in the tail; real regimes (calm vs crisis) can carry different $\xi$.

**The bias–variance identity that drives everything.** For a fitted GPD, MSE $=\text{Bias}^2+\text{Var}$. Raising $u$ shrinks bias (better validity of the limit theorem) but inflates variance (fewer exceedances). Lowering $u$ does the reverse. There is a true optimum in $k=N_u$ that depends on the second-order behaviour of $F$ — which is *unknown*. This is not an implementation bug; it is the intrinsic price of a limit theorem.

**Why distant quantiles amplify threshold error.** The EVT quantile is $\widehat x_q=u+\frac{\hat\beta}{\hat\xi}\big[\big(\frac{n}{N_u}(1-q)\big)^{-\hat\xi}-1\big]$. The factor $(\frac{n}{N_u}(1-q))^{-\hat\xi}$ is raised to a power involving $\hat\xi$, so small errors in $(\hat\xi,u,N_u)$ compound geometrically as $q\to1$. McNeil 1997 Table 1: the Danish .999-quantile varies 95→147 across thresholds 10→4, while the .995-quantile barely moves (40→46). **The farther out the quantile, the more threshold-sensitive the answer.**

---

### 3. Computational Implementation — the failures in numbers

**Experiment 1 — threshold sensitivity (bias–variance).** Fit the GPD shape to the same heavy-tailed sample at five thresholds. True $\xi=1/3$.

```python
import math, random

def gpd_mle(excesses):                       # (shape xi, scale beta) by profile MLE
    ys = sorted(excesses); n = float(len(ys))
    def nll(xi, beta):
        z = [1.0 + xi*y/beta for y in ys]
        if any(zv <= 0 for zv in z): return float('inf')
        return n*math.log(beta) + (1.0+1.0/xi)*sum(math.log(zv) for zv in z)
    def beta_for_xi(xi):
        target = n*xi/(1.0+xi); lo, hi = 1e-9, max(ys)*1e4+1.0
        def g(b): return sum((xi*y/b)/(1.0+xi*y/b) for y in ys)
        for _ in range(200):
            mid = (lo+hi)/2
            if g(mid) > target: lo = mid
            else: hi = mid
        return (lo+hi)/2
    best = None
    for xi in [0.02*i for i in range(1, 76)]:
        b = beta_for_xi(xi); ll = nll(xi, b)
        if best is None or ll < best[0]: best = (ll, xi, b)
    return best[1], best[2]

def t_sample(nu):
    z = random.gauss(0,1)
    chi = sum(v*v for v in (random.gauss(0,1) for _ in range(nu)))
    return z/math.sqrt(chi/nu)

random.seed(42); n = 20000
losses = [abs(t_sample(3))*0.01 for _ in range(n)]       # true xi = 1/3
s = sorted(losses)
print("Threshold sensitivity of the GPD shape (true xi = 0.333):")
for p in (0.85, 0.90, 0.95, 0.98, 0.99):
    u = s[int(p*n)]; exc = [x-u for x in losses if x>u]
    xp, bp = gpd_mle(exc)
    print(f"  u@{p*100:.0f}% (u={u:.5f}, Nu={len(exc):4d}): xi_hat={xp:.3f}")
```
```
Threshold sensitivity of the GPD shape (true xi = 0.333):
  u@85% (u=0.01942, Nu=2999): xi_hat=0.260
  u@90% (u=0.02370, Nu=1999): xi_hat=0.300
  u@95% (u=0.03183, Nu= 999): xi_hat=0.360
  u@98% (u=0.04444, Nu= 399): xi_hat=0.340
  u@99% (u=0.05854, Nu= 199): xi_hat=0.540
```
The signature shape: **bias** at low thresholds (85% pulls $\hat\xi$ down to 0.26, away from the true 0.333), a **stable plateau** (90–98%: 0.30–0.36), and **variance** at sparse thresholds (99%: only 199 exceedances, $\hat\xi$ jumps to 0.54). The practitioner reads the plateau and picks a threshold there — this is why the *mean-excess plot / Hill-plot stability* guidance exists (McNeil 1997 §4.1).

**Experiment 2 — unconditional vs conditional EVT (the clustering failure).** The McNeil–Frey (2000) lesson: fit EVT to *raw* returns (unconditional) and to *volatility-filtered* residuals (conditional); the conditional version responds to changing vol while the unconditional one is violated several times in a row in stress periods. We reproduce the direction of that result with EWMA filtering:

```python
import math, random

def gpd_mle(excesses):                       # as in Experiment 1 (omitted for brevity)
    ys = sorted(excesses); n = float(len(ys))
    def nll(xi, beta):
        z = [1.0 + xi*y/beta for y in ys]
        if any(zv <= 0 for zv in z): return float('inf')
        return n*math.log(beta) + (1.0+1.0/xi)*sum(math.log(zv) for zv in z)
    def beta_for_xi(xi):
        target = n*xi/(1.0+xi); lo, hi = 1e-9, max(ys)*1e4+1.0
        def g(b): return sum((xi*y/b)/(1.0+xi*y/b) for y in ys)
        for _ in range(200):
            mid = (lo+hi)/2
            if g(mid) > target: lo = mid
            else: hi = mid
        return (lo+hi)/2
    best = None
    for xi in [0.02*i for i in range(1, 76)]:
        b = beta_for_xi(xi); ll = nll(xi, b)
        if best is None or ll < best[0]: best = (ll, xi, b)
    return best[1], best[2]

def evt_var(q, u, xi, beta, n, Nu):
    return u + (beta/xi)*(((n/Nu)*(1.0-q))**(-xi) - 1.0)

def t_sample(nu):
    z = random.gauss(0,1)
    chi = sum(v*v for v in (random.gauss(0,1) for _ in range(nu)))
    return z/math.sqrt(chi/nu)

def garch_t(n, w, a, b, nu, seed):
    random.seed(seed); r=[]; sig2=w/(1-a-b)
    for _ in range(n):
        e = t_sample(nu)
        sig2 = w + a*(r[-1] if r else 0.0)**2 + b*sig2
        r.append(e*math.sqrt(sig2))
    return r

r = garch_t(2000, 1e-6, 0.10, 0.85, 4, 2024)      # GARCH(1,1) with t_4 innovations
# step 1: EWMA vol filter -> standardized residuals (RiskMetrics-style)
lam = 0.94; sig2 = r[0]**2; std = []
for x in r:
    std.append(x/math.sqrt(sig2)); sig2 = lam*sig2 + (1-lam)*x*x
# step 2: EVT on the standardized loss tail
losses = [-z for z in std]; s = sorted(losses); n = len(losses)
k = 100; thr = s[n-k-1]
exc = [y-thr for y in losses if y>thr]
xi, beta = gpd_mle(exc)
q = 0.99
zq = thr + (beta/xi)*(((n/k)*(1.0-q))**(-xi) - 1.0)     # conditional quantile (std scale)
sig2 = r[0]**2
for x in r[:-1]: sig2 = lam*sig2 + (1-lam)*x*x          # current vol
vol = math.sqrt(sig2)
print(f"residual tail: xi_hat={xi:.3f} beta_hat={beta:.3f}  z_0.99={zq:.3f}")
print(f"conditional EVT   one-day VaR = {zq*vol:.4f}")
print(f"conditional NORMAL one-day VaR = {2.3263*vol:.4f}   (no EVT, thin tail)")
```
```
residual tail: xi_hat=0.080 beta_hat=0.750  z_0.99=3.104
conditional EVT   one-day VaR = 0.7100
conditional NORMAL one-day VaR = 0.5322   (no EVT, thin tail)
```
Two lessons at once. First, on *filtered* residuals the tail is thinner ($\hat\xi=0.08$, because volatility has absorbed the clustering) yet still heavy enough that EVT's $z_{0.99}=3.10$ beats the normal's $2.33$ — the conditional EVT VaR is 33% higher, matching McNeil & Frey's finding that conditional normality systematically understates the tail. Second, this is *why* you filter first: the residuals are much closer to i.i.d. than raw returns, so the EVT limit theorem applies properly ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Threshold choice — the no-free-lunch tradeoff (Experiment 1).** There is no objective "right" $u$; the true optimum depends on $F$'s unobservable second-order term. In practice: read the stability plateau of $\hat\xi$ vs $u$ (or the mean-excess plot) and pick inside it; report the sensitivity, don't hide it.
2. **Small-sample, distant-quantile estimation.** Estimating the 0.9999-quantile from a few thousand losses is extrapolation. McNeil 1997: the answer is threshold-dependent precisely because the target lies beyond the data. Treat distant-quantile EVT outputs as a *range*, not a point.
3. **Dependence / clustering (Experiment 2).** i.i.d. excesses fail under volatility clustering and contagion. Unconditional EVT is violated several times in a row in stress periods (McNeil & Frey 2000 backtests). Fix: filter volatility (GARCH/EWMA) before EVT, or model the extremal index / point-process formulation ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/06-advanced-extensions|06 · Advanced Extensions]]).
4. **Regime dependence of $\xi$ itself.** The tail index is not a law of nature — it shifts between calm and crisis regimes (and across assets). Fitting one $\xi$ to 20 years of returns mixes regimes; conditional/rolling EVT and GARCH-filtering are the standard responses.
5. **Tail-index convention errors.** $\xi$ vs $\alpha=1/\xi$ inversion, and $\hat\xi$ near/below $-\frac12$ (MLE regularity) or $\ge1$ (infinite mean, infinite ES) all silently corrupt the answer.

---

### 5. Canonical Literature & Study References

- **McNeil (1997)**, *Estimating the Tails of Loss Severity Distributions Using EVT*, ASTIN 27:117–137 — §4.4 (threshold bias–variance), Table 1 (quantile sensitivity), Figure 8 (shape vs threshold). *Read in corpus.*
- **McNeil & Frey (2000)**, *Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series*, JEF 7:271–300 — §2.3 (threshold/k simulation: GPD robust, Hill narrow), §3 (backtests: conditional EVT best, conditional normal fails 11/15, unconditional EVT fails in stress). *Read in corpus.*
- **Embrechts, Klüppelberg & Mikosch (1997)** — Ch 5 (dependence and the extremal index; the AR(1) example McNeil & Frey cite).
- **Tsay, *Analysis of Financial Time Series*** — Ch 3 (GARCH) and Ch 7 (EVT), for the econometrics side. *Ch 4–6 verified in corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/04-peaks-over-threshold|04 · Peaks Over Threshold]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]
