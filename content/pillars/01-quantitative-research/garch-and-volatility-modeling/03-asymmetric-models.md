---
title: "03 — Asymmetric Models: Leverage, EGARCH & GJR"
tags:
  - pillar-quant-research
  - garch-and-volatility-modeling
  - egarch
  - gjr
  - leverage-effect
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (conditional variance) and [[foundations/statistics-and-inference/index|Statistics & Inference]] (MLE).

---

### 1. Intuition & Practical Objective

Symmetric GARCH has one blind spot, and it is the costly one: it treats a $+3\%$ day and a $-3\%$ day as identical news. Empirically they are not. A large **negative** return raises future volatility substantially more than a large **positive** one — the **leverage effect** (Black 1976), also called the *sign bias* or *asymmetry*. In Tsay's IBM example a $-2\sigma$ shock lifts volatility about **37% more** than a $+2\sigma$ shock.

Why does this happen? Two reinforcing stories:
- **Financial leverage:** a falling equity price mechanically raises the firm's debt-to-equity ratio, making the stock riskier — so a price drop increases future volatility.
- **Volatility feedback / risk premium:** rising volatility raises the required return, which lowers the price today — so large moves and high vol reinforce each other, asymmetrically for downside moves.

Whatever the cause, a symmetric model **understates the volatility clustering after crashes** — precisely when it matters most. This page builds the two canonical fixes: **EGARCH** (Nelson 1991, models $\ln\sigma_t^2$ so no positivity constraints and the asymmetry is explicit) and **GJR/TGARCH** (Glosten–Jagannathan–Runkle 1993, keeps the GARCH form but adds a term that is switched on only by negative shocks).

---

### 2. Mathematical Ground Truth & Derivations

**EGARCH($p,q$) (Nelson 1991).** Model the **log**-variance, so it is positive by construction and negative dependence is allowed:
$$\ln\sigma_t^2=\omega+\sum_{i=1}^{q}\big[\theta_i z_{t-i}+\gamma_i\big(|z_{t-i}|-\mathbb{E}|z|\big)\big]+\sum_{j=1}^{p}\beta_j\ln\sigma_{t-j}^2,\qquad z_t=\frac{a_t}{\sigma_t}.$$
For Gaussian $z$, $\mathbb{E}|z|=\sqrt{2/\pi}=0.7979$. The **weighted innovation** $g(z)=\theta z+\gamma(|z|-\mathbb{E}|z|)$ is crucial: its slope is $\theta+\gamma$ for $z\ge0$ and $\theta-\gamma$ for $z<0$. **Expect $\theta<0$** — then a negative standardized shock has a *larger* effect on $\ln\sigma^2$ than a positive one of the same size. The asymmetry is carried by $\theta$; **this is a different parameterisation from the S-Plus/Tsay form** $\ln\sigma_t^2=\omega+\sum\alpha_i(|a_{t-i}|+\gamma_i a_{t-i})/\sigma_{t-i}+\sum\beta_j\ln\sigma_{t-j}^2$, where leverage is $\gamma_i<0$. Do not mix the two attributions.

**GJR / TGARCH (Glosten–Jagannathan–Runkle 1993; Zakoian 1994).** Keep the GARCH recursion but let negative shocks switch on an extra term:
$$\sigma_t^2=\alpha_0+\sum_{i=1}^{q}\big(\alpha_i+\gamma_i N_{t-i}\big)a_{t-i}^2+\sum_{j=1}^{p}\beta_j\sigma_{t-j}^2,\qquad N_{t-i}=\begin{cases}1,&a_{t-i}<0\\0,&a_{t-i}\ge0.\end{cases}$$
A negative shock gets coefficient $\alpha_i+\gamma_i$; a positive shock gets only $\alpha_i$. **Expect $\gamma_i>0$.** For GJR(1,1):
$$\sigma_t^2=\alpha_0+\big(\alpha_1+\gamma_1 N_{t-1}\big)a_{t-1}^2+\beta_1\sigma_{t-1}^2,\qquad \operatorname{Var}(a_t)=\frac{\alpha_0}{1-\alpha_1-\tfrac12\gamma_1-\beta_1},$$
(the $\tfrac12\gamma_1$ because $\mathbb{E}[N]=P(a<0)=\tfrac12$ under symmetry). The asymmetric response as a function of the shock is the **news-impact curve**: a kinked, piecewise-quadratic line, steeper on the left.

**Which to use.** EGARCH handles log-variance (no positivity constraints, multiplicative news impact); GJR keeps the familiar quadratic form and is often easier to interpret and to estimate. Both are one extra parameter. The *test* for whether you need either is the **Engle–Ng sign-bias test** (regress $\hat a_t^2$ on a constant, $\hat a_{t-1}^2$, and $\hat a_{t-1}^2\mathbf{1}\{\hat a_{t-1}<0\}$ and test the coefficient on the indicator) — a significant coefficient means symmetric GARCH is mis-specified.

**Asymmetric persistence.** Under GJR the effective persistence is $\alpha_1+\tfrac12\gamma_1+\beta_1$, so part of the long-run risk is carried by the asymmetry term; ignoring it understates memory.

---

### 3. Computational Implementation — the news-impact asymmetry, quantified

Standard library only. Feeds one $\pm3\sigma$ shock into a GJR(1,1) recursion and into an EGARCH(1,1), and reads off how much more future variance the negative shock produces.

```python
import math

# ---------- GJR(1,1): s2_t = a0 + (a1 + gamma*N_{t-1}) a_{t-1}^2 + b1 s2_{t-1} ----------
a0, a1, b1, gamma = 2e-6, 0.02, 0.90, 0.06
base = a0/(1-a1-b1-0.5*gamma)          # E[N]=1/2 steady state
def gjr_path(a_prev):
    N = 1.0 if a_prev < 0 else 0.0
    s = a0 + (a1 + gamma*N)*a_prev**2 + b1*base
    out = []
    for _ in range(5):
        out.append(s); s = a0 + b1*s    # no further shocks
    return out
neg = gjr_path(-3*math.sqrt(base)); pos = gjr_path(+3*math.sqrt(base))
print("GJR(1,1) sigma^2 response to a single shock:")
print("  +3sigma: " + " ".join(f"{v:.3e}" for v in pos))
print("  -3sigma: " + " ".join(f"{v:.3e}" for v in neg))
print(f"  variance ratio (-3sigma)/(+3sigma) at t+1 = {neg[0]/pos[0]:.4f}")

# ---------- EGARCH(1,1): ln s2_t = w + b ln s2_{t-1} + theta z_{t-1} + gam(|z|-E|z|) ----------
w, b, theta, gam = -0.05, 0.95, -0.10, 0.20
Ez = math.sqrt(2.0/math.pi)
def egarch(z):
    ln = w/(1-b)                         # steady state, then one shock
    return w + b*ln + theta*z + gam*(abs(z)-Ez)
ln_neg = egarch(-3.0); ln_pos = egarch(3.0)
print(f"\nEGARCH E|z| = sqrt(2/pi) = {Ez:.4f}   theta={theta:.2f} (theta<0 => leverage)")
print(f"  ln sigma^2 after z=-3: {ln_neg:.4f}  sigma^2={math.exp(ln_neg):.4e}")
print(f"  ln sigma^2 after z=+3: {ln_pos:.4f}  sigma^2={math.exp(ln_pos):.4e}")
print(f"  -3sigma raises vol {100*(math.exp(ln_neg)/math.exp(ln_pos)-1):.1f}% more than +3sigma")
```
```
GJR(1,1) sigma^2 response to a single shock:
  +3sigma: 4.520e-05 4.268e-05 4.041e-05 3.837e-05 3.653e-05
  -3sigma: 6.680e-05 6.212e-05 5.791e-05 5.412e-05 5.071e-05
  variance ratio (-3sigma)/(+3sigma) at t+1 = 1.4779

EGARCH E|z| = sqrt(2/pi) = 0.7979   theta=-0.10 (theta<0 => leverage)
  ln sigma^2 after z=-3: -0.2596  sigma^2=7.7138e-01
  ln sigma^2 after z=+3: -0.8596  sigma^2=4.2334e-01
  -3sigma raises vol 82.2% more than +3sigma
```

The GJR model gives **1.48× the variance** after a negative 3σ shock versus a positive one; EGARCH with $\theta=-0.10$ gives **82% more**. Both encode the same qualitative fact — downside news is disproportionately risky — and both, being symmetric-in-$|z|$ for the magnitude part, still cluster. The size of the asymmetry is a free parameter estimated from data; our chosen values are illustrative, calibrated so the *direction and rough magnitude* match the empirical leverage effect Tsay reports for IBM (~37% at 2σ).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Sign-bias survival is a red flag.** If you fit symmetric GARCH and the Engle–Ng sign-bias test rejects, every downside VaR you produce is biased *low*. Skipping the asymmetry term is the most common under-modelling error in equity volatility.
2. **EGARCH stationarity is subtler.** Log-variance has no positivity constraint, but stationarity now requires $|\beta|<1$ on the log-AR root; a naive implementation that assumes $\alpha+\beta<1$ on the original parameters is wrong.
3. **Asymmetry vs. leverage direction is index-dependent.** Equity indices show strong leverage ($\theta<0$ / $\gamma>0$); some commodities and FX show the *opposite* or none. Do not hard-code the sign — estimate it.
4. **Parameter contamination by the mean equation.** If the mean $\mu_t$ is mis-specified (e.g. an ignored holiday effect), large residuals get mis-attributed to the variance equation and can masquerade as spurious asymmetry.
5. **The indicator ignores magnitude asymmetry.** GJR's $\gamma N$ captures *sign* asymmetry only. If the news-impact is asymmetric in *magnitude* as well (common in crisis data), you need a smooth transition model (e.g. ST-GARCH) — a foreshadow of [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]].

---

### 5. Canonical Literature & Study References

- **Nelson, Daniel B.** (1991): *Conditional Heteroskedasticity in Asset Returns: A New Approach*, Econometrica 59(2), 347–370 — EGARCH. *Verified corpus refs/pillar1.*
- **Glosten, Jagannathan & Runkle** (1993): *On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks*, J. Finance 48(5), 1779–1801 — GJR/TGARCH. *Verified corpus refs/pillar1.*
- **Black, Fischer** (1976): *Studies of Stock Price Volatility Changes* — the leverage effect's first documentation.
- **Engle, Robert F. & Ng, Victor K.** (1993): *Measuring and Testing the Impact of News on Volatility*, J. Finance 48(5) — the sign-bias test and the news-impact curve.
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — §3.7 (EGARCH, g-form and S-Plus form, IBM 37% example), §3.8 (TGARCH/GJR).

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Prior: [[pillars/01-quantitative-research/garch-and-volatility-modeling/02-arch-and-garch|02 · ARCH & GARCH]] · Hub: [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|Index]]
- Continue: [[pillars/01-quantitative-research/garch-and-volatility-modeling/04-realized-vol-and-har|04 · Realized Vol & HAR]] · [[pillars/01-quantitative-research/garch-and-volatility-modeling/05-failure-modes-and-practice|05 · Failure Modes]]
- Applied: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (the volatility smile *is* leverage in option prices) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & ES]]
