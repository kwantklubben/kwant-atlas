---
title: "F.6.2 Stationarity & ARMA Models"
tags:
  - foundations
  - econometrics-timeseries
  - stationarity
  - arma
  - acf-pacf
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/01-from-zero-intuition|01 · From Zero]] (returns, stationarity, ACF).

---

### 1. Intuition & Practical Objective

Once a series is stationary, the *linear* part of its dependence — how the current value relates to its own past — can be summarized by two families: **AR** (autoregressive: the value depends on its own past *values*) and **MA** (moving-average: the value depends on its own past *shocks*). Almost every "explainable" mean-level behavior in a stationary series is a mixture of the two, the **ARMA** model. This page's objective is the discipline of **identification**: given data, how do you decide the model *orders* $(p,q)$, estimate them, and check the residuals?

The intuition: **the ACF is the "signature" of dependence, and the PACF is the "degree" of direct dependence.**

- An **AR(p)** process has an ACF that decays (exponentially, or as a damped sine if the roots are complex) but never cleanly cuts off; its **PACF cuts off after lag $p$**.
- An **MA(q)** process has an **ACF that cuts off after lag $q$**; its PACF decays.
- An **ARMA(p,q)** process has *both* decaying — it cuts off at no finite lag.

That asymmetry (ACF cuts for MA, PACF cuts for AR) is the entire identification game. But the ACF/PACF story alone is *not* enough for ARMA — Tsay's key correction is that you also need the **EACF** (extended autocorrelation function, Tsay–Tiao 1984) to pin down joint $(p,q)$ order, because an ARMA's ACF/PACF look like high-order AR/MA.

---

### 2. Mathematical Ground Truth & Derivations

**The Wold decomposition** (Tsay §2.3): any purely-nondeterministic stationary process can be written as a linear combination of current and past white noise:
$$
r_t=\mu+\sum_{i=0}^\infty\psi_i\,a_{t-i},\qquad \psi_0=1,\quad \sum\psi_i^2<\infty,
$$
with the ACF $\rho_\ell=\dfrac{\sum_i\psi_i\psi_{i+\ell}}{\sum_i\psi_i^2}$ and total variance $\sigma_a^2\sum\psi_i^2$.

**AR(1)** $x_t=\phi_0+\phi_1x_{t-1}+a_t$: stationary iff $\lvert\phi_1\rvert<1$; mean $\phi_0/(1-\phi_1)$; variance $\sigma_a^2/(1-\phi_1^2)$; **ACF $\rho_\ell=\phi_1^\ell$** (exponential decay; alternating signs if $\phi_1<0$).

**AR(p)** $x_t=\phi_0+\sum_{i=1}^p\phi_i x_{t-i}+a_t$: stationary iff all characteristic roots of $1-\phi_1B-\dots-\phi_pB^p=0$ lie outside the unit circle; $\rho_\ell=\phi_1\rho_{\ell-1}+\dots+\phi_p\rho_{\ell-p}$ for $\ell\ge1$. Complex roots $\Rightarrow$ damped sine, cycle length $k=2\pi/\cos^{-1}[\phi_1/(2\sqrt{-\phi_2})]$ (Tsay Example 2.1: GNP $\approx10.6$ qtrs).

**PACF.** The partial autocorrelation at lag $k$ is the last coefficient of the best AR($k$) fit — equivalently the Durbin–Levinson recursion's final coefficient at each order. For an AR(p), the PACF is exactly **0 for lags $>p$** (asymptotic variance $1/T$).

**MA(q)** $x_t=a_t+\sum_{i=1}^q\theta_i a_{t-i}$: always stationary; invertible iff zeros of $\theta(B)=0$ are outside the unit circle ($\lvert\theta_1\rvert<1$ for MA(1)); ACF cuts off after $q$. MA(1): $\rho_1=+\theta_1/(1+\theta_1^2)$ under this $+\theta$ convention ($\rho_\ell=0$ for $\ell>1$).

**ARMA(p,q)** $x_t=\phi_0+\sum_{i=1}^p\phi_ix_{t-i}+a_t+\sum_{j=1}^q\theta_ja_{t-j}$: stationary iff AR roots outside unit circle, invertible iff MA roots outside. **ARMA(1,1)** variance $\dfrac{(1+2\phi\theta+\theta^2)}{1-\phi^2}\sigma_a^2$ and
$$
\rho_1=\frac{(1+\theta\phi)(\phi+\theta)}{1+2\theta\phi+\theta^2},\qquad \rho_\ell=\phi\,\rho_{\ell-1}\ \ (\ell\ge2).
$$
The ACF decays *exponentially from lag 2 on* — it does **not** cut off at any finite lag (Tsay §2.3). This "decay starting at lag 2" is the ARMA(1,1) fingerprint.

**Model selection.** AIC $=\ln\tilde\sigma_\ell^2+\dfrac{2\ell}{T}$, BIC $=\ln\tilde\sigma_\ell^2+\dfrac{\ell\ln T}{T}$ (Tsay eq. 2.16). BIC penalizes complexity more ($\ln T>2$ for $T>7$) and is asymptotically consistent; AIC is better for forecasting in finite samples. The residual check is **Ljung–Box** $Q(m)=T(T+2)\sum_{\ell=1}^m\frac{\hat\rho_\ell^2}{T-\ell}\sim\chi^2_{m-g}$ ($g$ fitted ARMA coefficients).

---

### 3. Computational Implementation — identification in action

Simulate an AR(2) with known $(\phi_1,\phi_2)=(1.2,-0.6)$, recover the parameters by Yule–Walker, and show the sample PACF cuts off at lag 2. Then simulate an ARMA(1,1) and verify the ACF matches its theory (decay from lag 2). Stdlib only.

```python
import math, random
random.seed(3)
def mean(x): return sum(x)/len(x)
def acf(x,k):
    m=mean(x); d=sum((v-m)**2 for v in x)
    return sum((x[i]-m)*(x[i+k]-m) for i in range(len(x)-k))/d
phi1,phi2=1.2,-0.6
T=6000; x=[0.0,0.0]
for t in range(2,T): x.append(phi1*x[-1]+phi2*x[-2]+random.gauss(0,1))
x=x[3000:]
r1,r2=acf(x,1),acf(x,2)
det=1-r1*r1
print("AR(2) true (phi1,phi2) :",(phi1,phi2))
print("AR(2) Yule-Walker est  :",(round((r1-r1*r2)/det,3),round((r2-r1*r1)/det,3)))
def durbin_levinson(rho,p):
    phi=[[0.0]*(p+1) for _ in range(p+1)]; phip=[0.0]*(p+1)
    phip[1]=rho[0]; phi[1][1]=rho[0]
    for k in range(2,p+1):
        num=rho[k-1]-sum(phi[k-1][j]*rho[k-1-j] for j in range(1,k))
        den=1.0-sum(phi[k-1][j]*rho[j-1] for j in range(1,k))
        phik=num/den; phi[k][k]=phik
        for j in range(1,k): phi[k][j]=phi[k-1][j]-phik*phi[k-1][k-j]
        phip[k]=phik
    return phip
rho=[acf(x,i) for i in range(1,5)]
pacf=durbin_levinson(rho,4)
print("AR(2) sample PACF 1-4 :",[round(v,3) for v in pacf[1:]])
ph,th=0.5,0.3; T2=8000; xa=[0.0]; al=0.0
for t in range(1,T2):
    e=random.gauss(0,1); xa.append(ph*xa[-1]+e+th*al); al=e
xa=xa[4000:]
rho_theory=(1+th*ph)*(ph+th)/(1+2*th*ph+th**2)
print("ARMA(1,1) rho1 theory :",round(rho_theory,4))
print("ARMA(1,1) rho1 sample :",round(acf(xa,1),4))
print("ARMA(1,1) rho3 sample :",round(acf(xa,3),4))
```
```
AR(2) true (phi1,phi2) : (1.2, -0.6)
AR(2) Yule-Walker est  : (1.213, -0.605)
AR(2) sample PACF 1-4 : [0.756, -0.605, 0.003, -0.027]
ARMA(1,1) rho1 theory : 0.6619
ARMA(1,1) rho1 sample : 0.6611
ARMA(1,1) rho3 sample : 0.1634
```
The Yule–Walker estimates recover $(\phi_1,\phi_2)$ almost exactly. The **PACF is $\approx0$ at lags 3 and 4** (0.003, −0.027) and equals $\phi_2=-0.6$ at lag 2 — the textbook AR(2) cut-off. The ARMA(1,1) sample $\rho_1=0.6611$ matches theory $0.6619$ and, as predicted, the ACF does **not** vanish at lag 3 (0.1634): it decays geometrically at rate $\phi=0.5$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **ACF/PACF alone cannot order an ARMA.** An ARMA's ACF/PACF look like a high-order AR/MA and cut off nowhere; you need the **EACF** (Tsay–Tiao 1984) triangle to locate $(p,q)$. Using only ACF/PACF is the classic beginner identification failure (Tsay §2.6.3).
2. **Near-unit-root distortion.** For $\phi_1\approx1$, the sample ACF decays extremely slowly and the PACF misbehaves — an AR(2) near the boundary looks like an AR(1)-with-roughly-unit-root. Stationarity must be settled *before* identification ([[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Unit Roots]]).
3. **Order overfitting via AIC.** AIC's lighter penalty tends to overfit order (it trades a little bias for less variance, good for forecasting, bad for parsimony). Use BIC when you want the "true" order and report residual Ljung–Box; the "one-standard-error" rule of ESL Ch 7 applies to order selection too.
4. **MA estimation near non-invertibility.** When $\theta_1\to1$ the conditional-likelihood (initial shocks = 0) estimator breaks down; use the *exact* likelihood (Tsay §2.5.3).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 2 (§2.2 ACF/PACF, §2.3 Wold/ARMA, §2.5 estimation, §2.6 identification incl. EACF). *Primary, verified.*
- **Box, Jenkins & Reinsel**, *Time Series Analysis: Forecasting and Control* — the classic Box–Jenkins identification/estimation/diagnostic loop.
- **Hastie, Tibshirani & Friedman**, *Elements of Statistical Learning*, Ch 7 — model-selection discipline (AIC/BIC/CV) that governs order choice.

---

### 6. Connected Graph Bridges

- Back: [[foundations/econometrics-and-timeseries/01-from-zero-intuition|01 · From Zero]] · [[foundations/econometrics-and-timeseries/index|Index Hub]]
- Forward: [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Forecasting & Unit Roots]] · [[foundations/econometrics-and-timeseries/04-volatility-modeling|04 · Volatility Modeling]]
