---
title: "06 — Advanced Extensions: Heston & Fourier Pricing, Calibration, Rough Vol"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - heston
  - sabr
  - fourier-pricing
  - calibration
  - rough-volatility
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|04 · Advanced Dynamics]] and [[pillars/03-derivative-pricing/black-scholes-merton|Black-Scholes-Merton]] (familiarity with the characteristic-function method).

---

### 1. Intuition & Practical Objective

This page is the **launchpad** from surface empirics to the model toolkit. The four moves:

1. **Stochastic volatility with a closed-form-ish price — Heston.** A second Brownian driver on variance; prices via a **characteristic function** and a one-dimensional Fourier integral. Exactly the machinery that makes SV calibration (to hundreds of quotes) feasible.
2. **SABR** — an industry standard *smile* parametrization (not a full dynamics), exact in the short-expiration limit.
3. **Forward-variance / Bergomi models** — model the variance curve $\xi_t^T$ directly; exactly calibrated to a VS term structure by construction, with direct control of the vol-of-vol term structure (Bergomi ch 7).
4. **Rough volatility** — the empirical finding that realized volatility is rougher than a diffusion ($H\approx0.1$), motivating fractional/rough SV.

The practical objective: know how to compute an SV price fast (Fourier), how calibration is posed, and where the frontier (rough vol, joint calibration of SPX/VIX) sits.

> **One-line essence.** "Heston gives the tractable SV price via a characteristic function; SABR gives the tractable smile; Bergomi gives control of the term structure; rough vol explains why all of them still mis-calibrate the very short end."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Heston model (Gatheral ch 2; Bergomi ch 6)

$$dS_t=\sqrt{v_t}\,S_t\,dZ_1,\qquad dv_t=-\lambda(v_t-\bar v)\,dt+\eta\sqrt{v_t}\,dZ_2,\qquad dZ_1dZ_2=\rho\,dt.$$
The variance is a **CIR/square-root** process (a special affine jump-diffusion; Duffie–Pan–Singleton 2000). Its PDE is (1.3) with $\alpha=-\lambda(v-\bar v),\beta=1$; the European price is $C=K[e^xP_1-P_0]$ with $P_j$ the pseudo-probabilities (Gatheral eq 2.5–2.6).

**The characteristic function** (Gatheral eq 2.12–2.15): with $x=\ln(F_T/K)$, $\tau=T-t$,
$$D(u,\tau)=\frac{r_-\big(1-e^{-d\tau}\big)}{1-g\,e^{-d\tau}},\qquad C(u,\tau)=\lambda\!\left\{r_-\tau-\frac{2}{\eta^2}\log\frac{1-g\,e^{-d\tau}}{1-g}\right\},$$
$$r_\pm=\frac{\beta\pm d}{\eta^2},\quad d=\sqrt{\beta^2-4\alpha\gamma},\quad g=\frac{r_-}{r_+},\quad \alpha=-\tfrac{u^2}{2}-\tfrac{iu}{2}+iju,\ \ \beta=\lambda-\rho\eta j-\rho\eta iu,\ \ \gamma=\tfrac{\eta^2}{2},$$
$$\varphi_T(u)=\mathbb{E}\!\left[e^{iux}\right]=\exp\!\big(C(u,\tau)\,\bar v+D(u,\tau)\,v_0\big).$$
**Pricing by Fourier** (Lewis 2000; Gatheral eq 5.6, zero rates/dividends):
$$\boxed{\;C(S,K,T)=S-\frac{\sqrt{SK}}{\pi}\int_0^\infty\frac{du}{u^2+\tfrac14}\,\mathrm{Re}\!\left[e^{-iuk}\varphi_T\!\left(u-\tfrac i2\right)\right],\qquad k=\log\frac KS\;}$$
The integrand decays fast; a few thousand points suffice. The equivalent **Heston (1993) two-probability** form is $C=K[e^xP_1-P_0]$ with $P_j=\tfrac12+\tfrac1\pi\int_0^\infty\mathrm{Re}[e^{-iuk}\varphi(u-i\delta_j)/(iu)]du$. Both use the same $\varphi$ and must agree — the cross-check used below.

**Consistency checks on any $\varphi$:** $\varphi(0)=1$ (normalization) and $\varphi(-i)=\mathbb{E}[e^{x}]=1$ (the martingale condition $F_T=\mathbb{E}[S_T]$).

#### 2.2 SABR (Hagan et al. 2002; Gatheral §7.2)

$$dS_t=\sigma_tS_t^{\beta}dZ_1,\quad d\sigma_t=\chi\sigma_tdZ_2,\quad dZ_1dZ_2=\rho dt,$$
with the exact $\tau\to0$ implied-vol formula (Gatheral eq 7.7) and ATM skew $\partial_k\sigma_{BS}|_{k=0}=\rho/2$. No mean reversion ⇒ **short-expiration tool only**. The Medvedev–Scaillet expansion reproduces SABR for small $\tau$.

#### 2.3 Forward-variance / Bergomi models (Bergomi ch 7)

State variables $(S_t,\{\xi_t^T\})$ with $dS_t=\sqrt{\xi_t^t}S_tdW_t^S$, $d\xi_t^T=\lambda_t^TdW_t^T$, and an $N$-factor Markov-functional representation by OU processes:
$$\xi_t^T=\xi_0^T\exp\!\left(\omega\sum_iw_ie^{-k_i(T-t)}X_t^i-\frac{\omega^2}{2}\sum_{ij}w_iw_je^{-(k_i+k_j)(T-t)}\mathbb{E}[X_t^iX_t^j]\right),\quad dX_t^i=-k_iX_t^idt+dW_t^i,$$
exactly calibratable to a VS term structure and **exactly simulable** (Bergomi eq 7.10/7.13–7.18). Two factors capture the empirical **power-law vol-of-vol term structure** $\nu_T(t)=\sigma_0(\tau_0/(T-t))^\alpha$, $\alpha\approx0.4$ (Bergomi eq 7.40). This is the current desk-grade answer to LV's forward-skew failure.

#### 2.4 Rough volatility

Empirically the log-realized-volatility has Hurst $H\approx0.1$ (much rougher than a diffusion's $H=1/2$), motivating $\sigma_t=\exp(X_t)$ with $dX$ a fractional Brownian motion. Rough SV reproduces the short-dated skew $\propto T^{H-1/2}$ (steeper than any SV model allows), which is exactly the short-end failure flagged in §04/05. Beyond this folder's verified corpus — treated as a forward pointer.

---

### 3. Computational Implementation — Heston by Fourier, verified against BS

We implement the Heston characteristic function and a single Lewis integral pricer, then (i) validate the integrator by feeding it the **Black-Scholes** characteristic function and checking it reproduces the closed form, (ii) check the two Heston martingale identities $\varphi(0)=\varphi(-i)=1$, and (iii) produce a Heston smile. Stdlib only (`cmath`).

```python
import math, cmath
def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def n(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)
def bsm_call(S,K,T,r,sig):
    d1=(math.log(S/K)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*N(d1)-K*math.exp(-r*T)*N(d2), d1
def implied_vol(price,S,K,T,r):
    sig=0.20
    for _ in range(200):
        c,d1=bsm_call(S,K,T,r,sig); diff=c-price
        if abs(diff)<1e-13: break
        sig-=diff/(S*n(d1)*math.sqrt(T))
    return sig

def bs_cf(u,T,sig): return cmath.exp(-0.5*sig*sig*T*(u*u+1j*u))
def heston_cf(u,T,v0,vbar,lam,eta,rho):
    iu=1j*u
    d=cmath.sqrt((rho*eta*iu-lam)**2+eta*eta*(iu+u*u))
    g=(lam-rho*eta*iu-d)/(lam-rho*eta*iu+d); ed=cmath.exp(-d*T)
    D=((lam-rho*eta*iu-d)/eta**2)*(1-ed)/(1-g*ed)
    C=(lam*vbar/eta**2)*((lam-rho*eta*iu-d)*T-2*cmath.log((1-g*ed)/(1-g)))
    return cmath.exp(C+D*v0)
def lewis_call(cf,S,K,T):                      # Lewis (5.6), zero rates/dividends
    k=math.log(K/S);tot=0.0;n=6000;hi=200.0;du=hi/n
    for i in range(n):
        u=(i+0.5)*du
        tot+=(cf(u-0.5j)*cmath.exp(-1j*u*k)).real/(u*u+0.25)*du
    return S-math.sqrt(S*K)/math.pi*tot

for K in (80.0,100.0,120.0):                   # validate the integrator against BSM
    bc,_=bsm_call(100.0,K,1.0,0.0,0.20)
    lw=lewis_call(lambda u:bs_cf(u,1.0,0.20),100.0,K,1.0)
    print(f"BS K={K:5.0f}: closed={bc:.6f}  Lewis-integrator={lw:.6f}  diff={abs(bc-lw):.2e}")

v0,vbar,eta,rho,lam=0.0174,0.0354,0.3877,-0.7165,1.3253     # Gatheral Table 3.2
p0=heston_cf(0.0,1.0,v0,vbar,lam,eta,rho); pm=heston_cf(-1j,1.0,v0,vbar,lam,eta,rho)
print(f"Heston CF: phi(0)={p0.real:.10f}  phi(-i)={pm.real:.10f}  (both must be 1)")
for K in (80.0,90.0,100.0,110.0,120.0):
    hc=lewis_call(lambda u:heston_cf(u,1.0,v0,vbar,lam,eta,rho),100.0,K,1.0)
    print(f"Heston K={K:5.0f}: price={hc:.4f}  implied vol={implied_vol(hc,100.0,K,1.0,0.0)*100:.3f}%")
```
```
BS K=   80: closed=21.185930  Lewis-integrator=21.185930  diff=5.68e-14
BS K=  100: closed=7.965567  Lewis-integrator=7.965567  diff=1.56e-13
BS K=  120: closed=2.147299  Lewis-integrator=2.147299  diff=1.14e-13
Heston CF: phi(0)=1.0000000000  phi(-i)=1.0000000000  (both must be 1)
Heston K=   80: price=21.1056  implied vol=19.573%
Heston K=   90: price=12.5960  implied vol=16.895%
Heston K=  100: price=5.6736  implied vol=14.234%
Heston K=  110: price=1.5232  implied vol=11.989%
Heston K=  120: price=0.2433  implied vol=10.993%
```

The Fourier integrator reproduces the Black-Scholes closed form to $\sim10^{-13}$ — the numerical proof that the Lewis representation and the characteristic function are correctly implemented. The Heston CF satisfies both martingale identities exactly, and the resulting smile is **downward-sloping** ($19.57\%$ at $K{=}80$ down to $10.99\%$ at $K{=}120$) at the very parameters (Table 3.2) that were shown in §04 to be **too flat at the short end** — the calibration failure that motivates jumps, forward-variance models, and rough vol.

**Calibration, in one paragraph.** Calibration is a *nonlinear least-squares fit of model prices to the whole surface*, typically weighted by vega/bid-offer. Heston has 5 parameters $(v_0,\bar v,\lambda,\eta,\rho)$; two expirations fix $\lambda'$ and $\rho\eta$, the term structure gives $\bar v,v_0$, and the skew curvature separates $\rho$ from $\eta$ (Gatheral §3.4). But since the surface *shape* is model-generic, good fits are easy and **do not validate the model** — only the dynamics (SSR, forward skew) do.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Complex-logarithm branch cuts.** The alternate Heston CF form $C=\lambda\{r_+\tau-\frac{2}{\eta^2}\log[(e^{d\tau}-g)/(1-g)]\}$ suffers jumps when the log argument crosses the negative real axis (winding number; Kahl–Jäckel 2005). Use the form $C=\lambda\{r_-\tau-\frac{2}{\eta^2}\log[(1-ge^{-d\tau})/(1-g)]\}$, whose argument appears never to cut the axis (Gatheral §2.2).
2. **Negative variance in simulation.** Euler on the CIR variance step gives negative $v$; use the **Milstein/Andersen** scheme $v_{i+1}=[\sqrt{v_i}+\frac\eta2\sqrt{\Delta t}Z]^2-\lambda(v_i-\bar v)\Delta t-\frac{\eta^2}{4}\Delta t$, which stays positive when $4\lambda\bar v/\eta^2>1$ (Gatheral §2.2).
3. **Over-fitting the surface.** With enough parameters any model fits the vanillas; the real constraints (forward skew, vol-of-vol term structure, VIX options) are invisible in today's slice (Bergomi ch 5–8).
4. **Wrong tool for the horizon.** SABR for long expirations, Heston for forward-skew exotics, LV for cliquets — each is a documented mis-application (Gatheral ch 7, Bergomi ch 2–3).
5. **Calibration instability.** SV parameters trade off (e.g. $\rho$ vs $\eta$ through $\rho\eta$); the fit is ill-conditioned and unstable across days, especially when jumps are added. Regularize, fit jointly across expirations, and check parameter stability over time.

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 2 (Heston SDE/PDE, Riccati system 2.11, C/D 2.12, CF 2.15, Milstein 2.18), Ch 3 §3.4 (Heston implied variance, calibration), Ch 5 (SVJ/SVJJ, Lewis call formula 5.6, skew 5.8/5.10), Ch 7 §7.2 (SABR). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 4 (power payoffs, forward variances), Ch 5 (variance swaps), Ch 6 (Heston in forward-variance form), Ch 7 (forward-variance / multi-factor models, 7.10–7.40). *Math-verified.*
- **Hagan, Kumar, Lesniewski, Woodward** (2002) SABR; **Lewis** (2000) small-$\eta$ and Fourier pricing; **Medvedev–Scaillet** (2004); **Duffie–Pan–Singleton** (2000) affine models; **Kahl–Jäckel** (2005) branch cuts. **Rough volatility:** Gatheral–Jaisson–Rosenbaum (2018) — forward pointer (beyond the verified corpus).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-and-sabr|Heston & SABR]] · [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · Advanced Extensions]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure-models|Interest-Rate & Term-Structure Models]]
- Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory|Probability & Measure Theory]]
