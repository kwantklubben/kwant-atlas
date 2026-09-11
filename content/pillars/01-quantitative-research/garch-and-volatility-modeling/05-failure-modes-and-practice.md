---
title: "1.9.5 Failure Modes & Practice"
tags:
  - pillar-quant-research
  - garch-and-volatility-modeling
  - failure-modes
  - structural-break
  - risk-management
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity, structural breaks) and [[foundations/statistics-and-inference/index|Statistics & Inference]] (estimation error, validation).

---

### 1. Intuition & Practical Objective

Every previous page was a *solution*: here is the model, here is the fix, here is the better estimator. This page is the honest audit. Volatility models fail in ways that are **systematic, first-principles, and exactly correlated with the moments you care about** — they break worst in crises. The job of a practitioner is to know *which* failure is currently binding and to guard against it.

There are four failure families, and each traces to a violated assumption in the GARCH declaration $a_t=\sigma_t\varepsilon_t$:
1. **The model is stationary; the world is not** — structural breaks inflate estimated persistence toward 1.
2. **The model is symmetric; the world is not** — leverage means symmetric GARCH understates downside risk.
3. **The model is finite-order; the truth is long-memory-ish** — high-order estimation is unstable, so you are always approximating.
4. **The model treats parameters as known; you estimate them from a handful of crises** — estimation error in the tails is *largest* exactly when it matters.

---

### 2. Mathematical Ground Truth & Derivations

**Failure 1 — Structural break vs. genuine persistence.** Suppose the true process is GARCH(1,1) with **constant** parameters but the *level* $\alpha_0$ jumps at some date $\tau$ (a regime shift in the volatility floor). Estimating a single GARCH on the pooled sample, the recursion accumulates variance across the break, and the fitted persistence $\hat\pi=\hat\alpha_1+\hat\beta_1$ is driven **toward the IGARCH boundary $\pi=1$**. The near-unit-root is an **artefact of the break**, not evidence of infinite memory (Lamoureux & Lastrapes 1990; Diebold 1986). Practical consequences: the unconditional variance $\alpha_0/(1-\pi)$ becomes numerically explosive (denominator $\to0$), and forecasts never mean-revert.

Diagnostics: (a) CUSUM / Chow tests on the variance equation; (b) fit on sub-samples and compare $\hat\pi$; (c) Markov-switching GARCH if the break is recurrent ([[pillars/01-quantitative-research/regime-detection/index|Regime Detection]]).

**Failure 2 — Symmetry / leverage.** Symmetric GARCH imposes $\partial\sigma_t^2/\partial a_{t-1}^2=\alpha_1$ regardless of the **sign** of $a_{t-1}$. Empirically the derivative is larger on the downside. Consequence: a symmetric model's **downside VaR is biased low** and its vol forecast *after a crash* is too small — the model systematically under-reacts to exactly the events that produce losses. Fix: GJR/EGARCH (03), or add the negative-return term directly to a HAR (04).

**Failure 3 — Estimation of high-order models.** The ARCH($q$)/GARCH($p,q$) likelihood is flat along the ridge where $\sum\alpha_i+\sum\beta_j$ is fixed; only the *sum* is well-identified, not its split. As $p,q$ grow, the positivity constraints multiply, the effective sample per parameter shrinks, and the estimates become unstable (variance blows up, occasionally landing on the constraint boundary). This is *why* GARCH(1,1) survives every forecast horse-race (Hansen & Lunde 2005). Practical rule: **prefer parsimony; test the residual ACF squared, do not add lags by default.**

**Failure 4 — Tail / estimation error.** VaR of a GARCH model at level $p$ is $\hat z_p\sqrt{\hat\sigma_{t+1}^2}$, where $\hat z_p$ uses a distributional assumption. Two errors compound: (i) $\varepsilon_t$ is not Gaussian — it is fat-tailed and skewed, so Gaussian $z_p$ understates tail risk; (ii) $\hat\sigma_{t+1}^2$ itself is estimated, and the parameters driving the *tail* (large-$\alpha_1$ behaviour) are pinned by the small number of historical crises. Backtests (Christoffersen 1998; Kupiec 1995) are the mandatory audit — see [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & ES]].

**Failure 5 — Aggregation and the $\sqrt{h}$ rule.** Multi-day VaR via $\sqrt{h}\,\sigma_1$ assumes iid returns. Under GARCH with $\pi<1$, the correct $h$-day variance is $\sigma_h^2(\ell)$ (geometric decay), which is *smaller* than $h\sigma_1^2$ when today is elevated — the $\sqrt h$ rule is **conservative after a shock and anticonservative in calm times**. Always use the model's own term structure (see 06).

---

### 3. Computational Implementation — the break inflates persistence

Standard library only. Builds a GARCH(1,1) series whose **volatility floor $\alpha_0$ jumps 4×** partway through (a structural break, parameters otherwise constant), then fits GARCH(1,1) by MLE on (a) the full sample and (b) the calm first half. The full-sample persistence is pulled toward 1 — the *signature* of the break-artefact failure.

```python
import math, random
random.seed(2024)

def nelder_mead(f, x0, step=0.4, tol=1e-7, maxit=600):
    d=len(x0); simp=[list(x0)]
    for i in range(d):
        p=list(x0); p[i]+=step; simp.append(p)
    val=[f(p) for p in simp]
    for _ in range(maxit):
        idx=sorted(range(d+1),key=lambda i:val[i]); simp=[simp[i] for i in idx]; val=[val[i] for i in idx]
        if abs(val[-1]-val[0])<tol*(abs(val[0])+tol): break
        cen=[sum(simp[i][j] for i in range(d))/d for j in range(d)]
        xr=[cen[j]+(cen[j]-simp[-1][j]) for j in range(d)]; fr=f(xr)
        if fr<val[0]:
            xe=[cen[j]+2*(cen[j]-simp[-1][j]) for j in range(d)]; fe=f(xe)
            if fe<fr: simp[-1],val[-1]=xe,fe
            else: simp[-1],val[-1]=xr,fr
        elif fr<val[-2]: simp[-1],val[-1]=xr,fr
        else:
            xc=[cen[j]+0.5*(simp[-1][j]-cen[j]) for j in range(d)]; fc=f(xc)
            if fc<val[-1]: simp[-1],val[-1]=xc,fc
            else:
                for i in range(1,d+1):
                    simp[i]=[(simp[i][j]+simp[0][j])/2 for j in range(d)]; val[i]=f(simp[i])
    idx=sorted(range(d+1),key=lambda i:val[i]); return simp[idx[0]]

def fit_garch(series):
    N=len(series)
    def nll(q):
        a0=math.exp(q[0]); pers=0.999/(1+math.exp(-q[1])); share=1/(1+math.exp(-q[2]))
        a1=pers*share; b1=pers*(1-share); s=a0/(1-pers); ll=0.0
        for t in range(N):
            if t>0: s=a0+a1*series[t-1]**2+b1*s
            if s<=1e-12: return 1e12
            ll+=-0.5*(math.log(2*math.pi)+math.log(s)+series[t]**2/s)
        return -ll
    best=nelder_mead(nll,[math.log(1e-6),2.0,0.0])
    a0=math.exp(best[0]); pers=0.999/(1+math.exp(-best[1])); share=1/(1+math.exp(-best[2]))
    return a0, pers*share, pers*(1-share), pers

# --- regime-shift series: omega jumps 4x at t=600 (persistence UNCHANGED) ---
m=1200; rs=[]; sc=[0.0]*m
for t in range(m):
    z=random.gauss(0,1); base=3e-7 if t<600 else 1.2e-6
    if t==0: v=base/(1-0.98)
    else: sc[t]=base+0.08*rs[t-1]**2+0.90*sc[t-1]; v=sc[t]
    rs.append(math.sqrt(v)*z)

full=fit_garch(rs); calm=fit_garch(rs[:600])
print("GARCH(1,1) MLE persistence (alpha1+beta1):")
print(f"  FULL sample (with break) pers={full[3]:.4f}  alpha1={full[1]:.3f} beta1={full[2]:.3f}")
print(f"  CALM subsample only      pers={calm[3]:.4f}  alpha1={calm[1]:.3f} beta1={calm[2]:.3f}")
print("  => the break inflates persistence toward the IGARCH boundary.")
```

```text
GARCH(1,1) MLE persistence (alpha1+beta1):
  FULL sample (with break) pers=0.9913  alpha1=0.070 beta1=0.921
  CALM subsample only      pers=0.9384  alpha1=0.070 beta1=0.869
  => the break inflates persistence toward the IGARCH boundary.
```

The **true** persistence was $0.98$ in both regimes; the full-sample fit reports $0.9913$ — nearly IGARCH — while the clean subsample recovers only $0.9384$. Note that $\hat\alpha_1=0.070$ in *both* fits: what the break did was push the entire persistence premium into $\hat\beta_1$ ($0.921$ vs $0.869$), i.e. into pure *level memory*, which is exactly the spurious-unit-root channel. A risk system built on the full-sample $\hat\pi$ would never let volatility mean-revert.

---

### 4. Failure Modes & First-Principles Breakdowns (checklist)

1. **Test for breaks before trusting persistence.** Split the sample, run a CUSUM on the standardized residuals $z_t=a_t/\sigma_t$, and compare $\hat\pi$ across sub-samples. If they differ, model the break, not the memory.
2. **Always add an asymmetry term for equity risk.** Run the Engle–Ng sign-bias test; if it rejects, symmetric GARCH is wrong on the downside.
3. **Backtest the quantile, not the variance.** Volatility forecasts can be "accurate" while the VaR is systematically breached (wrong tail model). Use Kupiec/Christoffersen tests.
4. **Fat tails in the shock distribution.** Replace Gaussian $\varepsilon_t$ with a standardized Student-$t$ (or GED); the estimated $\nu$ is your fat-tail parameter and moves the tail $z_p$ substantially.
5. **Beware the $\sqrt h$ shortcut.** Use the GARCH/HAR term structure for multi-day horizons.
6. **Sub-sample estimation in crises.** Tail parameters are estimated from few events; report parameter uncertainty (bootstrap/profile likelihood), and prefer robust, low-order models.
7. **Model risk is real and quantitative.** Keep a model-risk buffer (Derman 1996) — the loss from *using* a mis-specified vol model can exceed the apparent precision gain.

---

### 5. Canonical Literature & Study References

- **Lamoureux, Christopher G. & Lastrapes, William D.** (1990): *Persistence in Variance, Structural Change, and the GARCH Model*, J. Business & Economic Statistics 8(2) — the break-inflates-persistence result.
- **Diebold, Francis X.** (1986): *Modeling the Persistence of Conditional Variances* — IGARCH and the persistence question.
- **Hansen, Peter R. & Lunde, Asger** (2005): *A Forecast Comparison of Volatility Models…*, J. Applied Econometrics 20(7) — parsimony wins.
- **Kupiec, Paul** (1995) and **Christoffersen, Peter** (1998): *Evaluating Interval Forecasts*, International Economic Review 39(4) — VaR backtesting. *Verified corpus refs/pillar4 — `14_Christoffersen_1998_evaluating_interval_forecasts.pdf`.*
- **Derman, Emanuel** (1996): *Model Risk*, Quantitative Strategies Research Notes, Goldman Sachs. *Verified corpus refs/pillar4.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — §3.4.2 (ARCH weaknesses), §3.16 (kurtosis conditions).

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (structural breaks) · [[foundations/statistics-and-inference/index|Statistics & Inference]] (estimation error)
- Prior: [[pillars/01-quantitative-research/garch-and-volatility-modeling/03-asymmetric-models|03 · Asymmetric Models]] · [[pillars/01-quantitative-research/garch-and-volatility-modeling/04-realized-vol-and-har|04 · Realized Vol & HAR]] · Hub: [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|Index]]
- Continue: [[pillars/01-quantitative-research/garch-and-volatility-modeling/06-advanced-extensions|06 · Advanced Extensions]]
- Applied: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
