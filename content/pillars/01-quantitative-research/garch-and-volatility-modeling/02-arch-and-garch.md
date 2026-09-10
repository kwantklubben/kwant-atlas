---
title: "02 — ARCH & GARCH: The Recursion, Stationarity & Estimation"
tags:
  - pillar-quant-research
  - garch-and-volatility-modeling
  - arch
  - garch
  - maximum-likelihood
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (ARMA, stationarity, forecasting) and [[foundations/statistics-and-inference/index|Statistics & Inference]] (maximum likelihood).

---

### 1. Intuition & Practical Objective

ARCH and GARCH answer a single question: **how should yesterday's shock enter today's variance forecast?** The ARCH answer (Engle 1982) is "through yesterday's *squared shock*". The GARCH answer (Bollerslev 1986) adds "…and through yesterday's *variance forecast*", which is the crucial generalisation: it lets a long history of shocks feed today's risk through a short memory.

The economic reading of GARCH(1,1),

$$\sigma_t^2=\underbrace{\alpha_0}_{\text{floor}}+\underbrace{\alpha_1 a_{t-1}^2}_{\text{news from yesterday}}+\underbrace{\beta_1\sigma_{t-1}^2}_{\text{memory of the past}},$$

is a **weighted, exponentially-decaying average of past squared shocks with a floor**. It is *exactly* the same object as RiskMetrics' EWMA, but with two differences that make it a proper statistical model: an intercept $\alpha_0$ restoring mean reversion, and estimated (not fixed) coefficients. Because the recursion feeds back, a single large shock propagates forward for many days — the model *generates* clustering rather than being told about it.

The practical payoff: a **one-line, closed-form, one-step-ahead variance forecast** that a risk system can consume directly. Everything downstream — VaR, position sizing, option-hedging vol input — starts here.

---

### 2. Mathematical Ground Truth & Derivations

**ARCH($q$).** With $a_t=\sigma_t\varepsilon_t$, $\varepsilon_t\overset{iid}{\sim}N(0,1)$,
$$\sigma_t^2=\alpha_0+\sum_{i=1}^{q}\alpha_i a_{t-i}^2,\qquad \alpha_0>0,\quad \alpha_i\ge0.$$
Taking unconditional expectations, $\mathbb{E}[\sigma_t^2]=\alpha_0+\big(\sum\alpha_i\big)\mathbb{E}[a_{t}^2]$, and $\mathbb{E}[\sigma_t^2]=\operatorname{Var}(a_t)$, so
$$\operatorname{Var}(a_t)=\frac{\alpha_0}{1-\sum_{i=1}^q\alpha_i},\qquad\text{finite iff }\sum\alpha_i<1.$$
ARCH($1$) is already fat-tailed: its unconditional excess kurtosis is $3(1-\alpha_1^2)/(1-3\alpha_1^2)-3>0$ whenever $3\alpha_1^2<1$ (Tsay §3.4.1). Fat tails emerge **without** fat-tailed shocks — the clustering does it.

**GARCH($p,q$).**
$$\sigma_t^2=\alpha_0+\sum_{i=1}^{q}\alpha_i a_{t-i}^2+\sum_{j=1}^{p}\beta_j\sigma_{t-j}^2.$$
**Stationarity** requires $\sum_{i=1}^{\max(p,q)}(\alpha_i+\beta_i)<1$ (set $\alpha_i=0$ for $i>q$, $\beta_j=0$ for $j>p$). Then the **unconditional variance** is
$$\operatorname{Var}(a_t)=\frac{\alpha_0}{1-\sum_i\alpha_i-\sum_j\beta_j}.$$
*Derivation:* take unconditional expectations of the recursion: $\mathbb{E}[\sigma_t^2]=\alpha_0+\sum\alpha_i\mathbb{E}[a_{t-i}^2]+\sum\beta_j\mathbb{E}[\sigma_{t-j}^2]$; stationarity gives both $\mathbb{E}[a_t^2]$ and $\mathbb{E}[\sigma_t^2]$ equal to a common $\bar\sigma^2$, so $\bar\sigma^2=\alpha_0+(\sum\alpha_i+\sum\beta_j)\bar\sigma^2$.

**GARCH(1,1) — the workhorse.**
$$\boxed{\ \sigma_t^2=\alpha_0+\alpha_1 a_{t-1}^2+\beta_1\sigma_{t-1}^2\ },\qquad \pi\equiv\alpha_1+\beta_1<1,\qquad \operatorname{Var}(a_t)=\frac{\alpha_0}{1-\alpha_1-\beta_1}.$$

**ARMA($1,1$) representation.** Substituting $\sigma_{t-1}^2=a_{t-1}^2-\eta_{t-1}$ (with $\eta_t\equiv a_t^2-\sigma_t^2$ a martingale difference) gives
$$a_t^2=\alpha_0+(\alpha_1+\beta_1)a_{t-1}^2+\eta_t-\beta_1\eta_{t-1}.$$
So $a_t^2$ is an **ARMA(1,1)**, and the persistence $\pi=\alpha_1+\beta_1$ is its autoregressive root. This is the bridge that lets ARMA theory (stationarity, ACF decay, forecasting) transfer to the variance world — and it is why GARCH(1,1), not high-order GARCH, is usually enough: a low-order ARMA captures most of the dynamics.

**Forecasting.** $\mathbb{E}_t[a_{t+1}^2]=\sigma_{t+1}^2$ is known, and for $\ell\ge2$,
$$\sigma_h^2(\ell)=\alpha_0+\pi\,\sigma_h^2(\ell-1)\ \longrightarrow\ \frac{\alpha_0}{1-\pi}\quad(\ell\to\infty).$$
The forecast decays geometrically from the current level to the unconditional variance — the "volatility term structure". The **half-life** of a shock is $\ln\tfrac12/\ln\pi$; for $\pi=0.98$, $\approx34$ days.

**Estimation.** With $\varepsilon_t\sim N(0,1)$, the Gaussian log-likelihood is
$$\ln L=-\tfrac12\sum_{t=1}^{T}\Big[\ln 2\pi+\ln\sigma_t^2+\frac{a_t^2}{\sigma_t^2}\Big],$$
maximised numerically (the recursion is not linear in the parameters). Method-of-moments / ARMA estimation of the $a_t^2$ series gives a starting point; MLE is the standard.

---

### 3. Computational Implementation — simulate, fit by MLE, forecast

Standard library only. Simulates a GARCH(1,1), estimates $(\alpha_0,\alpha_1,\beta_1)$ by **Gaussian MLE with a compact Nelder–Mead optimiser** (unconstrained reparametrisation: $\alpha_0=e^{q_0}$, persistence via a logistic so $\pi<0.999$, and a share so $\alpha_1,\beta_1\ge0$), then produces the term-structure forecast.

```python
import math, random
random.seed(7)

# --- simulate GARCH(1,1) ---
A0, A1, B1 = 2e-6, 0.10, 0.85
n = 1500
r = [0.0]*n; s2t = [0.0]*n; s2t[0] = A0/(1-A1-B1)
for t in range(1, n):
    z = random.gauss(0.0, 1.0)
    r[t] = math.sqrt(s2t[t-1])*z
    s2t[t] = A0 + A1*r[t]**2 + B1*s2t[t-1]
print(f"TRUE: alpha0={A0:.2e} alpha1={A1:.3f} beta1={B1:.3f} pers={A1+B1:.3f} uvar={A0/(1-A1-B1):.4e}")

# --- Gaussian negative log-likelihood (unconstrained reparametrisation) ---
def nll(q):
    a0 = math.exp(q[0]); pers = 0.999/(1.0+math.exp(-q[1])); share = 1.0/(1.0+math.exp(-q[2]))
    a1 = pers*share; b1 = pers*(1.0-share); s = a0/(1.0-pers); ll = 0.0
    for t in range(n):
        if t > 0: s = a0 + a1*r[t-1]**2 + b1*s
        if s <= 1e-12: return 1e12
        ll += -0.5*(math.log(2*math.pi) + math.log(s) + r[t]**2/s)
    return -ll

# --- compact Nelder-Mead ---
def nelder_mead(f, x0, step=0.4, tol=1e-7, maxit=800):
    d = len(x0); simp = [list(x0)]
    for i in range(d):
        p = list(x0); p[i] += step; simp.append(p)
    val = [f(p) for p in simp]
    for _ in range(maxit):
        idx = sorted(range(d+1), key=lambda i: val[i])
        simp = [simp[i] for i in idx]; val = [val[i] for i in idx]
        if abs(val[-1]-val[0]) < tol*(abs(val[0])+tol): break
        cen = [sum(simp[i][j] for i in range(d))/d for j in range(d)]
        xr = [cen[j] + (cen[j]-simp[-1][j]) for j in range(d)]; fr = f(xr)
        if fr < val[0]:
            xe = [cen[j] + 2.0*(cen[j]-simp[-1][j]) for j in range(d)]; fe = f(xe)
            if fe < fr: simp[-1], val[-1] = xe, fe
            else: simp[-1], val[-1] = xr, fr
        elif fr < val[-2]: simp[-1], val[-1] = xr, fr
        else:
            xc = [cen[j] + 0.5*(simp[-1][j]-cen[j]) for j in range(d)]; fc = f(xc)
            if fc < val[-1]: simp[-1], val[-1] = xc, fc
            else:
                for i in range(1, d+1):
                    simp[i] = [(simp[i][j]+simp[0][j])/2.0 for j in range(d)]; val[i] = f(simp[i])
    idx = sorted(range(d+1), key=lambda i: val[i]); return simp[idx[0]], val[idx[0]]

best, fv = nelder_mead(nll, [math.log(2e-6), 2.0, 0.0])
a0 = math.exp(best[0]); pers = 0.999/(1+math.exp(-best[1])); share = 1/(1+math.exp(-best[2]))
a1 = pers*share; b1 = pers*(1-share)
print(f"MLE : alpha0={a0:.2e} alpha1={a1:.3f} beta1={b1:.3f} pers={pers:.3f} uvar={a0/(1-pers):.4e}  -logL={fv:.1f}")

# --- term-structure forecast from the fitted state ---
s = a0/(1-pers)
for t in range(1, n): s = a0 + a1*r[t-1]**2 + b1*s
path = []
for h in range(1, 11): s = a0 + (a1+b1)*s; path.append(s)
print("h-step sigma^2: " + " ".join(f"{p:.2e}" for p in path))
print(f"converges to uncond var {a0/(1-pers):.4e}")
```
```
TRUE: alpha0=2.00e-06 alpha1=0.100 beta1=0.850 pers=0.950 uvar=4.0000e-05
MLE : alpha0=3.34e-06 alpha1=0.112 beta1=0.805 pers=0.917 uvar=4.0204e-05  -logL=-5506.6
h-step sigma^2: 4.86e-05 4.79e-05 4.72e-05 4.66e-05 4.61e-05 4.56e-05 4.52e-05 4.48e-05 4.44e-05 4.40e-05
converges to uncond var 4.0204e-05
```

Two things to read off. First, **MLE recovers the true process closely**: the estimated unconditional variance $4.02\text{e-}05$ is within 0.5% of the truth $4.00\text{e-}05$, and persistence is $0.917$ vs $0.950$ — the small downward bias is expected at $n=1500$ for a persistent series (a symptom of the flat likelihood surface discussed in §4). Second, the **forecast path decays monotonically to the unconditional variance**, exactly as $\sigma_h^2(\ell)=\alpha_0+\pi\sigma_h^2(\ell-1)$ predicts.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Flat, non-quadratic likelihood $\Rightarrow$ unstable estimates.** $\alpha_1$ and $\beta_1$ are weakly identified separately (only $\pi$ is well-determined), so estimates trade off along a ridge. This is why "$\hat\beta_1$ moved 0.05 between samples" is usually noise, not news.
2. **High-order ARCH/GARCH over-parameterisation.** Adding lags multiplies the positivity constraints and widens the identification ridge; the likelihood barely improves. **GARCH(1,1) is empirically near-optimal** — extra order buys complexity, not accuracy (Hansen–Lunde 2005's forecast comparison reaches the same conclusion).
3. **Symmetry.** The model cannot tell $+3\sigma$ from $-3\sigma$; the single largest empirical mis-specification for equity risk. Fixed in 03.
4. **Persistence $\to1$ degeneracy.** When $\hat\pi\approx1$, the unconditional variance estimate $\alpha_0/(1-\pi)$ blows up (denominator near zero) and the model becomes IGARCH-in-practice — often a *structural-break artefact*, not true persistence (see 05).
5. **Non-negativity constraints.** $\alpha_i,\beta_j\ge0$ are needed only for the "all shocks raise variance" interpretation; if the optimiser wanders into a negative coefficient the recursion can go negative and the likelihood is undefined — a common coding failure.

---

### 5. Canonical Literature & Study References

- **Engle, Robert F.** (1982): *Autoregressive Conditional Heteroscedasticity…*, Econometrica 50(4), 987–1007 — ARCH. *Verified corpus refs/pillar1.*
- **Bollerslev, Tim** (1986): *Generalized Autoregressive Conditional Heteroskedasticity*, J. Econometrics 31(3), 307–327 — GARCH.
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — §3.4 (ARCH: definitions, uncond. variance, ARCH(1) kurtosis, weaknesses), §3.5 (GARCH: $a_t^2$ ARMA form, stationarity $\max(p,q)$ bound, forecasting).
- **Hansen, Peter R. & Lunde, Asger** (2005): *A Forecast Comparison of Volatility Models: Does Anything Beat a GARCH(1,1)?*, J. Applied Econometrics 20(7) — the empirical defence of the low-order model.

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (ARMA ↔ $a_t^2$ rep.) · [[foundations/statistics-and-inference/index|Statistics & Inference]] (MLE)
- Prior: [[pillars/01-quantitative-research/garch-and-volatility-modeling/01-from-zero-intuition|01 · From Zero]] · Hub: [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|Index]]
- Continue: [[pillars/01-quantitative-research/garch-and-volatility-modeling/03-asymmetric-models|03 · Asymmetric Models]] · [[pillars/01-quantitative-research/garch-and-volatility-modeling/05-failure-modes-and-practice|05 · Failure Modes]]
- Applied: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (consumes $\sigma_{t+1}^2$)
