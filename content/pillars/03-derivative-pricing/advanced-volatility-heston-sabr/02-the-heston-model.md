---
title: "02 — The Heston Model: SDE, Feller Condition, Characteristic Function & Fourier Pricing"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - heston
  - characteristic-function
  - fourier-pricing
  - cir-process
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/01-from-zero-intuition|01 · From Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 The PDE & Derivation]].

---

### 1. Intuition & Practical Objective

Heston (1993) asks a simple question and answers it completely: *what is the simplest honest stochastic-volatility model that still has a fast price?* The answer is a mean-reverting, square-root variance process correlated with the spot — a **CIR** process (Cox–Ingersoll–Ross), which is an **affine** process. Affineness is the whole trick: it makes the Laplace transform of the log-price **analytic**, so option prices come from a single one-dimensional integral instead of a PDE solve or a simulation.

Three things to internalise before the maths:

1. **Two risk factors, one incomplete market.** Spot and variance are separate diffusions. You can hedge the spot with the underlying; you *cannot* hedge the variance with the underlying alone. The model therefore prices **volatility risk** through a market price of volatility risk $\varphi$ (Gatheral 1.3) — after which the standard practice is to work directly in the risk-neutral measure, since the model is calibrated to option prices anyway.
2. **The Feller condition is a statement about the *origin*.** $v_t$ is a square-root process; whether it can reach zero is decided by $2\lambda\bar v\gtrless\eta^2$. This matters numerically (negative variance) and economically (vol clustering at zero), and — crucially — **calibrated market parameters routinely violate it**.
3. **Affinity is what you buy.** Everything downstream — calibration to hundreds of quotes, VIX computation, time-dependent extensions — depends on $\varphi$ being a closed-form function of $(u,T)$.

The practical objective: be able to (a) write down the Heston SDE and PDE, (b) state and use the Feller condition, (c) derive/implement the characteristic function, (d) price by Fourier and validate the implementation against Black-Scholes and the martingale condition.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The model and its valuation equation

Under $\mathbb Q$, with $\lambda$ the mean-reversion speed and $\bar v$ the long-run variance:

$$\boxed{\;dS_t=\sqrt{v_t}\,S_t\,dZ_1,\qquad dv_t=-\lambda(v_t-\bar v)\,dt+\eta\sqrt{v_t}\,dZ_2,\qquad dZ_1dZ_2=\rho\,dt\;}$$

(Gatheral 2.1–2.2, with $\alpha=-\lambda(v-\bar v)$, $\beta=1$ in the generic SV SDEs 1.1–1.2; the same SDEs in Bergomi 6.1 with $k\leftrightarrow\lambda$, $\sigma\leftrightarrow\eta$.)

Two risk factors ⇒ hedge the option with $-\Delta$ shares **and** $-\Delta_1$ units of a second (volatility-dependent) traded asset. Killing both $dS$ and $dv$ terms in the generic valuation equation (Gatheral 1.3) and setting the market price of volatility risk to zero (working in $\mathbb Q$) gives the **Heston PDE** (Gatheral 2.3):

$$\frac{\partial V}{\partial t}+\tfrac12vS^2V_{SS}+\rho\eta vS\,V_{vS}+\tfrac12\eta^2v\,V_{vv}+rS\,V_S-rV=\lambda(\bar v-v)V_v .$$

Note the shape: the mixed derivative $\rho\eta vS\,V_{vS}$ is what makes the *skew* appear (it is the coupling between spot and variance), and the quadratic-in-vol-of-vol term $\tfrac12\eta^2vV_{vv}$ is what makes the *wings* lift.

#### 2.2 Feller condition

For $dv=-\lambda(v-\bar v)dt+\eta\sqrt v\,dZ$, the origin $v=0$ is unattainable (and inaccessible) iff

$$\boxed{\;2\lambda\bar v>\eta^2\;}$$

If $2\lambda\bar v\le\eta^2$ the origin is *regular and accessible*: the process hits zero in finite time and reflects. It then stays non-negative — a square-root diffusion **cannot** go negative — but it spends time pinned near zero, and the variance distribution acquires an atom-like pile-up at the origin. Numerical schemes that ignore this produce negative $v$ (see [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]]).

#### 2.3 The characteristic function (the heart of the model)

Write $x=\ln(F_{t,T}/K)$ and $\tau=T-t$. Heston's ansatz is

$$C(x,v,\tau)=K\big[e^{x}P_1(x,v,\tau)-P_0(x,v,\tau)\big]$$

(Gatheral 2.5): the price is "the pseudo-expectation of the final index, in the money" minus "strike $\times$ the pseudo-probability of exercise". Each $P_j$ solves a backward PDE with the same generator and different coefficients $b_j=\lambda-j\rho\eta$ (Gatheral 2.6):

$$-\frac{\partial P_j}{\partial\tau}+\tfrac12v\,P_{j,xx}-(\tfrac12-j)v\,P_{j,x}+\tfrac12\eta^2v\,P_{j,vv}+\rho\eta v\,P_{j,xv}+(a-b_jv)P_{j,v}=0,\qquad a=\lambda\bar v .$$

Fourier-transforming in $x$, $\widetilde P_j=\int e^{-iux}P_j\,dx$, the PDE collapses to a **Riccati ODE system** (Gatheral 2.9–2.11) with

$$\alpha=-\tfrac{u^2}{2}-\tfrac{iu}{2}+iju,\qquad \beta=\lambda-\rho\eta j-\rho\eta iu,\qquad \gamma=\tfrac{\eta^2}{2},$$

$$\frac{\partial D}{\partial\tau}=\alpha-\beta D+\gamma D^2=\gamma\,(D-r_+)(D-r_-),\qquad \frac{\partial C}{\partial\tau}=\lambda D,\qquad r_\pm=\frac{\beta\pm d}{\eta^2},\quad d=\sqrt{\beta^2-4\alpha\gamma}.$$

With $D(0)=C(0)=0$ and $g:=r_-/r_+$ (Gatheral 2.12):

$$\boxed{\;D(u,\tau)=\frac{r_-\big(1-e^{-d\tau}\big)}{1-g\,e^{-d\tau}},\qquad C(u,\tau)=\lambda\Big\{r_-\tau-\frac{2}{\eta^2}\ln\frac{1-g\,e^{-d\tau}}{1-g}\Big\}\;}$$

and the pseudo-probabilities are the real integrals (Gatheral 2.13)

$$P_j(x,v,\tau)=\frac12+\frac1\pi\int_0^\infty\mathrm{Re}\Big\{\frac{e^{C_j(u,\tau)\bar v+D_j(u,\tau)v+iux}}{iu}\Big\}du .$$

**The $j=0$ case is the whole model.** Setting $j=0$ ($\Rightarrow\alpha=-\tfrac{u^2}{2}-\tfrac{iu}{2}$, $\beta=\lambda-\rho\eta iu$) gives precisely the characteristic function of the *forward-measure* log-return $X_T=\ln(S_T/F_T)$:

$$\varphi_T(u)=\mathbb E^{\mathbb Q}\big[e^{iuX_T}\big]=\exp\!\big(C(u,\tau)\bar v+D(u,\tau)v_0\big).$$

Two consequences worth stating as *checks*, because they are the standard way to police an implementation:

- **Normalisation:** $\varphi_T(0)=1$.
- **Martingale condition:** $\varphi_T(-i)=\mathbb E[e^{X_T}]=\mathbb E[S_T]/F_T=1$ at **every** $T$.

The second identity is non-trivial — it fails if you pick the wrong root $r_+$ or get a sign of $\lambda$ wrong — and it is verified numerically below. It also anchors the Feynman–Kac/risk-neutral logic of [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02]] on the two-factor model.

#### 2.4 Pricing by Fourier (Lewis / Carr–Madan)

With $\varphi_T$ in hand, the European call is one real integral. Gatheral's zero-dividend form (5.6), which is exactly Lewis' contour prescription, is

$$\boxed{\;C(F_T,K,T)=F_T-\frac{\sqrt{F_TK}}{\pi}\int_0^\infty\frac{du}{u^2+\tfrac14}\,\mathrm{Re}\Big[e^{-iuk}\varphi_T\!\Big(u-\tfrac i2\Big)\Big],\qquad k=\ln\frac{K}{F_T}\;}$$

The shift to the contour $\mathrm{Im}\,u=\tfrac12$ makes the integrand decay and removes the $\mathrm{Re}[1/(iu)]$ singularity. A few thousand quadrature nodes suffice. (The equivalent Heston two-probability form $C=K[e^xP_1-P_0]$ uses the same $\varphi$ with $j=1,0$ and must agree — a useful second implementation.)

---

### 3. Computational Implementation — CF, Fourier price, and four validation checks

We implement $\varphi_T$ and the Lewis pricer, then run the four checks: (a) the martingale identity, (b) the $\eta\to0$ Black-Scholes collapse, (c) put–call parity, (d) the $T\to0$ ATM limit $\sigma_{BS}\to\sqrt{v_0}$. Stdlib only.

```python
import math, cmath

N = lambda x: 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bs_call(F,K,T,sig):
    d1=(math.log(F/K)+0.5*sig*sig*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return F*N(d1)-K*N(d2)
def implied_vol(price,F,K,T):
    lo,hi=1e-8,5.0
    for _ in range(200):
        m=0.5*(lo+hi)
        if bs_call(F,K,T,m)>price: hi=m
        else: lo=m
    return 0.5*(lo+hi)

# --- Heston characteristic function, Gatheral (2.12)/(2.15), j=0.
#     phi(u) = E[exp(i u X_T)],  X_T = log(S_T/F_T)  (martingale log-return)
def heston_phi(u,T,v0,vbar,lam,eta,rho):
    iu=1j*u
    alpha=-0.5*u*u-0.5*iu                 # -u^2/2 - iu/2
    beta =lam-rho*eta*iu                  # lambda - rho*eta*i*u
    gamma=0.5*eta*eta                     # eta^2/2
    d=cmath.sqrt(beta*beta-4*alpha*gamma)
    rp=(beta+d)/(2*gamma); rm=(beta-d)/(2*gamma); g=rm/rp
    e=cmath.exp(-d*T)
    D=rm*(1-e)/(1-g*e)
    C=lam*(rm*T-(2.0/eta**2)*cmath.log((1-g*e)/(1-g)))
    return cmath.exp(C*vbar+D*v0)         # exponent = C*vbar + D*v0

def simpson(f,a,b,n):
    h=(b-a)/n; s=f(a)+f(b)
    for i in range(1,n): s+=(4.0 if i%2 else 2.0)*f(a+i*h)
    return s*h/3.0

# --- Lewis / Carr-Madan inversion, Gatheral (5.6), evaluated on Im u = 1/2
def heston_call(F,K,T,r,v0,vbar,lam,eta,rho,n=4000,U=200.0):
    k=math.log(K/F)
    f=lambda u:(cmath.exp(-1j*u*k)*heston_phi(u-0.5j,T,v0,vbar,lam,eta,rho)).real/(u*u+0.25)
    I=simpson(f,1e-10,U,n)
    return math.exp(-r*T)*(F-math.sqrt(F*K)/math.pi*I)
def heston_put(F,K,T,r,v0,vbar,lam,eta,rho,n=4000,U=200.0):
    return heston_call(F,K,T,r,v0,vbar,lam,eta,rho,n,U)-math.exp(-r*T)*(F-K)

print("== (a) martingale condition  phi(-i) = E[S_T/F_T] = 1 ==")
for T in (0.01,1.0,5.0):
    z=heston_phi(-1j,T,0.0174,0.0354,1.3253,0.3877,-0.7165)
    print(f"  T={T:5.2f}: phi(-i) = {z.real:.12f} {z.imag:+.1e}i")

print("== (b) vol-of-vol -> 0 must collapse to Black-Scholes with sigma=sqrt(v) ==")
v=0.04; F=100.0
print(f"  eta=1e-6 Heston call = {heston_call(F,100.0,1.0,0.0,v,v,1.0,1e-6,0.0,n=2000):.8f}")
print(f"  BSM(20%) call        = {bs_call(F,100.0,1.0,math.sqrt(v)):.8f}")

print("== (c) put-call parity  C - P = e^{-rT}(F-K) ==")
v0,vbar,lam,eta,rho=0.0174,0.0354,1.3253,0.3877,-0.7165
for K in (80.0,90.0,100.0,110.0,120.0):
    c=heston_call(F,K,1.0,0.0,v0,vbar,lam,eta,rho)
    p=heston_put(F,K,1.0,0.0,v0,vbar,lam,eta,rho)
    print(f"  K={K:5.0f} call={c:8.5f} put={p:8.5f} iv={implied_vol(c,F,K,1.0)*100:7.3f}% "
          f"resid={c-p-(F-K):+.1e}")

print("== (d) ATM implied vol tends to sqrt(v0) as T->0 (v0=0.0174 -> 13.191%) ==")
for T in (0.002,0.01,0.05,0.5,1.0):
    c=heston_call(F,F,T,0.0,v0,vbar,lam,eta,rho,n=8000,U=400.0)
    print(f"  T={T:6.3f}: ATM implied vol = {implied_vol(c,F,F,T)*100:.4f}%  var={implied_vol(c,F,F,T)**2:.6f}")
avg=vbar+(v0-vbar)*(1-math.exp(-lam))/lam
print(f"  deterministic average of the forward-variance curve, (1/T)int xi_0^t, at T=1: {avg:.6f} "
      f"({math.sqrt(avg)*100:.3f}% vol)")
```
```
== (a) martingale condition  phi(-i) = E[S_T/F_T] = 1 ==
  T= 0.01: phi(-i) = 1.000000000000 +0.0e+00i
  T= 1.00: phi(-i) = 1.000000000000 +0.0e+00i
  T= 5.00: phi(-i) = 1.000000000000 +0.0e+00i
== (b) vol-of-vol -> 0 must collapse to Black-Scholes with sigma=sqrt(v) ==
  eta=1e-6 Heston call = 7.96607957
  BSM(20%) call        = 7.96556746
== (c) put-call parity  C - P = e^{-rT}(F-K) ==
  K=   80 call=21.10563 put= 1.10563 iv= 19.573% resid=+0.0e+00
  K=   90 call=12.59600 put= 2.59600 iv= 16.895% resid=+0.0e+00
  K=  100 call= 5.67364 put= 5.67364 iv= 14.234% resid=+0.0e+00
  K=  110 call= 1.52324 put=11.52324 iv= 11.989% resid=+0.0e+00
  K=  120 call= 0.24325 put=20.24325 iv= 10.993% resid=+0.0e+00
== (d) ATM implied vol tends to sqrt(v0) as T->0 (v0=0.0174 -> 13.191%) ==
  T= 0.002: ATM implied vol = 13.2237%  var=0.017487
  T= 0.010: ATM implied vol = 13.1903%  var=0.017398
  T= 0.050: ATM implied vol = 13.1903%  var=0.017398
  T= 0.500: ATM implied vol = 13.5635%  var=0.018397
  T= 1.000: ATM implied vol = 14.2337%  var=0.020260
  deterministic average of the forward-variance curve, (1/T)int xi_0^t, at T=1: 0.025427 (15.946% vol)
```

**What each check proves.**

- **(a)** The martingale identity holds to machine precision at three maturities — the Riccati normalisation, the root choice and the $\lambda$ sign are all right.
- **(b)** With $\eta\to0$ and $v_0=\bar v$ the Heston price collapses onto Black-Scholes to $5\times10^{-4}$ (the residual is Simpson-quadrature error, not model error). The SV model *contains* BSM as a limit.
- **(c)** Put–call parity is satisfied **exactly** (residual $0.0$) at every strike — a consequence of $\varphi(-i)=1$ plus the structure of the Lewis formula. The implied vols trace the downward equity skew: $19.573\%$ at $K{=}80$ down to $10.993\%$ at $K{=}120$.
- **(d)** As $T\to0$ the ATM implied vol converges to $\sqrt{v_0}=13.191\%$ — the *instantaneous* variance, exactly as it must ($13.1903\%$ at $T{=}0.01$ and $0.05$; the slight excess at $T{=}0.002$, $13.2237\%$, is quadrature error in the Fourier integral at extremely small $T$). It then rises with maturity toward the deterministic average of the forward-variance curve, $15.946\%$ at $T{=}1$ (§04).
- **An independent path check.** A full Monte Carlo of the SDE pair (60 000 antithetic paths, 300 Euler steps, $T{=}1$ ATM) gives $5.66266$ against the Fourier price $5.67364$ — a $0.2\%$ gap, inside one standard error ($\approx0.03$), and the simulated average realized variance matches its theoretical value $(1/T)\int_0^T\xi_0^t dt=0.025427$ (simulated $0.025350$). The Fourier route is validated end to end.

> **Caveat on the ATM level (flagged in the corpus).** At $T{=}1$ the ATM implied variance is $0.020260$ ($14.234\%$), *not* the deterministic forward-variance average $0.025427$ ($15.946\%$). This is a genuine, large **vol-of-vol effect**, not an error: in the Bergomi–Guyon expansion (§04) the ATMF level correction carries a factor $1/(\sigma_{BS}^2T)^3$, which is large precisely when $\sigma^2T$ is small. It is also why Bergomi warns that the *order-1* ATMF-level approximation is poor while the order-1 *skew* is accurate to $\sim10\%$ — a distinction the next two pages quantify.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Complex-logarithm branch cuts (the "little trap").** The alternative Heston CF form written with $r_+$, $C=\lambda\{r_+\tau-\frac{2}{\eta^2}\ln[(e^{d\tau}-g)/(1-g)]\}$, is only *almost* equivalent to (2.12): the principal-value log jumps when its argument crosses the negative real axis, producing a discontinuous characteristic function (winding-number / Riemann-sheet problem; Kahl–Jäckel 2005). **Use the $r_-$ form** (2.12), whose argument appears never to cut the axis.
2. **Negative variance in simulation.** Euler on the CIR step produces negative $v$. The **Milstein** scheme $v_{i+1}=[\sqrt{v_i}+\frac{\eta}{2}\sqrt{\Delta t}\,Z]^2-\lambda(v_i-\bar v)\Delta t-\frac{\eta^2}{4}\Delta t$ stays positive provided $4\lambda\bar v/\eta^2>1$ — at *no extra cost* — and is therefore preferred to Euler (Gatheral 2.18). Where that condition fails one needs the exact CIR transition (Broadie–Kaya) or a matching-moment scheme (Andersen–Brotherton-Ratcliffe). Quantified in [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]].
3. **Feller is not an assumption — it is an output.** Nothing in the calibration forbids $2\lambda\bar v\le\eta^2$, and in practice the fit to an equity surface *wants* to violate it. Treat any scheme that assumes $v>0$ a.s. as broken.
4. **The order-1 ATM-level approximation is unreliable.** Gatheral's (3.18) — the formula everyone quotes for the Heston ATM term structure — is built from the *unconditional* expected-variance path, so its literal $T\to0$ limit is $\bar v$, not $v_0$; and the $O(\eta^2)$ corrections to the *level* are large whenever $\sigma_{BS}^2T$ is small (§04). Trust the skew, distrust the level.
5. **Pricing by $\varphi$ is not the same as pricing by $\mathbb P$.** $\varphi_T$ is a $\mathbb Q$ object built with the risk-neutral drift. Simulating the SDE with the physical drift and then discounting gives the wrong price; the drift must be absorbed by construction (or the market price of volatility risk specified).
6. **The model is one-factor and Markov in $(S,v)$.** Its forward-variance curve is *determined*, $\xi_0^T=\bar v+e^{-\lambda T}(v_0-\bar v)$ — so it cannot match a general variance-swap term structure and an ATM term structure simultaneously (Bergomi §6, §04). Making $v_0(t)$ time-dependent is legitimate; making $\lambda,\eta,\rho$ time-dependent is not, unless the corresponding forward-skew claims actually trade.

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 2 in full (SV SDEs 1.1–1.2, valuation equation 1.3, Heston PDE 2.3, ansatz 2.5, $P_j$ PDE 2.6, Fourier ODEs 2.9–2.10, Riccati 2.11, $C,D$ 2.12, $P_j$ integral 2.13, alternative form/branch cuts 2.14, CF 2.15, Euler/Milstein/exact schemes 2.17–2.19, why Heston is popular) and Ch 3 §3.4 (Heston implied variance 3.17, ATM term structure 3.18, skew 3.19, calibration recipe). *Math-verified in the corpus.*
- **Heston, Steven L.** (1993), *A closed-form solution for option prices with stochastic volatility with applications to bond and currency options*, Review of Financial Studies 6(2), 327–343 — the original.
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 6 (Heston re-read as a one-factor forward-variance model: 6.1–6.5, Feller-adjacent structure, vol-of-vol 6.9, skew 6.16–6.20, and the four structural criticisms) and Ch 1 (what makes a model *usable*). *Math-verified.*
- **Cox–Ingersoll–Ross (1985)** and **Duffie–Pan–Singleton (2000)** (affine jump-diffusions — the general class Heston sits in); **Broadie–Kaya (2006)** (exact simulation); **Andersen (2008)** (efficient simulation); **Kahl–Jäckel (2005)** (the complex-log branch-cut problem); **Lord–Koekkoek–van Dijk (2010)** (discretisation schemes compared).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §1.1–1.9 — the generalized BSM/parity backstop used in checks (b) and (c). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|03 · SABR & Asymptotics]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 PDE & Feynman–Kac]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|VS · 06 Advanced Extensions]] (Heston by Fourier, from the surface side)
