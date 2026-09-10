---
title: "03 — Short-Rate Models: Vasicek, CIR, Hull-White & the Market Price of Risk"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - vasicek
  - cir
  - hull-white
  - affine-term-structure
  - market-price-of-risk
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates|02 · Bonds, Yield Curve & Forward Rates]] and [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

A **short-rate model** picks the dynamics of the instantaneous rate $r_t$ directly, and then *derives* the whole bond/forward structure as a consequence. The objective of this page: understand the three canonical models — **Vasicek** (Gaussian, mean-reverting, negative rates possible), **CIR** (square-root diffusion, non-negative rates), and **Hull-White** (time-dependent drift for exact fit to today's curve) — and the one idea that connects them to prices: the **market price of risk**.

The key structural idea that has no analogue in a constant-$r$ BSM world: **bond prices are not uniquely determined by the physical ($\mathbb{P}$) dynamics of $r$.** Because there is only one random source ($dW$) but the market of bonds has infinitely many maturities, one bond cannot hedge another unless you know how much risk the market prices. That missing quantity is the **market price of risk** $\lambda$ — the excess return per unit of volatility. Different $\lambda$ give different risk-neutral measures $\mathbb{Q}$ and hence different bond prices (Björk Prop 23.1–23.3).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The term-structure equation and the market price of risk (Björk Ch23)

Let $dr=\mu(t,r)dt+\sigma(t,r)d\bar W$ under $\mathbb{P}$. A portfolio of a $S$-bond and a $T$-bond kills the $dW$ term, which forces the market price of risk to be *the same for all maturities*:

$$\frac{\alpha_T(t)-r(t)}{\sigma_T(t)}=\lambda(t)\quad\forall T\qquad\text{(Björk Prop 23.1)}.$$

$F(t,r;T)=P(t,T)$ then satisfies the **term-structure equation** (Björk Prop 23.2):

$$F_t+(\mu-\lambda\sigma)F_r+\tfrac12\sigma^2F_{rr}-rF=0,\qquad F(T,r;T)=1.$$

Under the risk-neutral measure the $r$-dynamics become $dr=(\mu-\lambda\sigma)dt+\sigma dW$ and (Björk Prop 23.3)

$$P(t,T)=\mathbb{E}^{\mathbb{Q}}_{t,r}\!\left[e^{-\int_t^T r_s ds}\right].$$

**$\lambda$ is exogenous** — not pinned by the model, but calibrated to (or assumed for) the market. It is the single lever connecting real-world and risk-neutral drift.

#### 2.2 Vasicek (BM Ch3; Björk Prop 24.3; Hull Ch31)

$$dr=a(b-r)dt+\sigma dW .$$

Gaussian, mean-reverting to $b$ with speed $a$. The affine bond price $P(t,T)=A(t,T)e^{-B(t,T)r}$ has closed forms

$$B(t,T)=\frac{1-e^{-a(T-t)}}{a},\qquad A(t,T)=\exp\!\left\{\frac{(B-(T-t))(a^2b-\frac12\sigma^2)}{a^2}-\frac{\sigma^2B^2}{4a}\right\}.$$

**Flaw:** $r$ is Gaussian, so $\mathbb{P}(r<0)>0$ — nominal rates can go negative.

#### 2.3 Cox-Ingersoll-Ross (BM Ch3; Björk Prop 24.6; Shreve Ch31)

$$dr=a(b-r)dt+\sigma\sqrt r\,dW .$$

The square-root diffusion keeps $r\ge0$; the **Feller condition** $2ab\ge\sigma^2$ makes $r>0$ strictly and $r$ unattainable at 0. Closed-form bond (Björk Prop 24.6, $h=\sqrt{a^2+2\sigma^2}$):

$$B(t,T)=\frac{2(e^{h\tau}-1)}{(h+a)(e^{h\tau}-1)+2h},\qquad A(t,T)=\left[\frac{2he^{(a+h)\tau/2}}{(h+a)(e^{h\tau}-1)+2h}\right]^{\frac{2ab}{\sigma^2}},\quad \tau=T-t.$$

$r(t)$ has a **non-central chi-square** transition density; the stationary density is Gamma (Shreve Ch31).

#### 2.4 Hull-White extended Vasicek (BM Ch3 3.33–3.34; Björk Prop 24.8; Hull Ch32; Shreve Ch30)

$$dr=[\theta(t)-ar]dt+\sigma dW,\qquad \theta(t)=\frac{\partial}{\partial T}f^{M}(0,t)+a f^{M}(0,t)+\frac{\sigma^2}{2a}\left(1-e^{-2at}\right).$$

The time-dependent drift $\theta(t)$ is chosen so the model **reproduces today's market forward curve exactly** (no yield-curve inversion — this is why HW is the workhorse). With constant $a,\sigma$, $r$ is Gaussian (Shreve Ch30), $\int_0^T r\,dt$ is normal, and bond prices and bond-options have closed forms. Ho-Lee is the $a=0$ special case; a two-factor Hull-White adds a second process for the humped vol structure.

#### 2.5 Affine term structure (ATS) — the unifying machinery (Björk Prop 24.2; BM Ch3)

If $\mu(t,r)=\alpha(t)r+\beta(t)$ and $\sigma^2(t,r)=\gamma(t)r+\delta(t)$ (affine drift & variance), then $P=A(t,T)e^{-B(t,T)r}$ with $B,A$ solving Riccati ODEs:

$$B_t+\alpha B-\tfrac12\gamma B^2=-1,\quad B(T,T)=0;\qquad A_t=\beta B-\tfrac12\delta B^2,\quad A(T,T)=0.$$

All of Vasicek, CIR, Ho-Lee, Hull-White are affine; Dothan and Black-Derman-Toy are not.

---

### 3. Computational Implementation — closed forms vs MC, and the exact-fit HW

Verify the closed-form bonds against Monte-Carlo of $r$, and confirm Hull-White's exact fit. Stdlib only.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

def vasicek_bond(a,b,sig,r,t,T):
    B=(1.0-math.exp(-a*(T-t)))/a
    A=math.exp((B-(T-t))*(a*a*b-sig*sig/2.0)/(a*a)-sig*sig*B*B/(4.0*a))
    return A*math.exp(-B*r)

def cir_bond(a,b,sig,r,t,T):
    h=math.sqrt(a*a+2*sig*sig); tau=T-t; ex=math.exp(h*tau)-1.0
    B=2.0*ex/((h+a)*ex+2*h)
    A=math.pow(2*h*math.exp((a+h)*tau/2.0)/((h+a)*ex+2*h),2*a*b/(sig*sig))
    return A*math.exp(-B*r)

def mc_bond(drift, diff, r0, T, steps, n):
    dt=T/steps; tot=0.0
    for _ in range(n):
        r=r0; acc=0.0
        for _ in range(steps):
            r+=drift(r)*dt+diff(r)*math.sqrt(dt)*random.gauss(0,1)
            if r<0: r=0.0                     # CIR: keep non-negative
            acc+=r*dt
        tot+=math.exp(-acc)
    return tot/n

random.seed(1)
ev=vasicek_bond(0.15,0.05,0.01,0.04,0,5)
mv=mc_bond(lambda r:0.15*(0.05-r), lambda r:0.01, 0.04, 5.0, 200, 200000)
print(f"Vasicek P(0,5): closed={ev:.6f}  MC={mv:.6f}  err={abs(ev-mv):.1e}")

random.seed(2)
ec=cir_bond(0.20,0.05,0.05,0.04,0,5)
mc=mc_bond(lambda r:0.20*(0.05-r), lambda r:0.05*math.sqrt(max(r,0)), 0.04, 5.0, 200, 100000)
print(f"CIR     P(0,5): closed={ec:.6f}  MC={mc:.6f}  err={abs(ec-mc):.1e}")
print(f"CIR Feller 2ab={2*0.20*0.05:.4f} >= sig^2={0.05**2:.4f}  -> r stays >0")

# Hull-White theta for exact fit to flat market forward curve fM(t)=4%
def fM(t): return 0.04
def hw_theta(t,a,sig,h=1e-5):
    df=(fM(t+h)-fM(t-h))/(2*h)
    return df+a*fM(t)+(sig*sig/(2*a))*(1-math.exp(-2*a*t))

def mc_hw_bond(a,sig,T,steps,n,flat=0.04):
    dt=T/steps; tot=0.0
    for _ in range(n):
        r=flat; acc=0.0
        for k in range(steps):
            th=hw_theta(k*dt,a,sig)
            r+=(th-a*r)*dt+sig*math.sqrt(dt)*random.gauss(0,1)
            acc+=r*dt
        tot+=math.exp(-acc)
    return tot/n

random.seed(3)
mh=mc_hw_bond(0.10,0.015,5.0,200,50000)
print(f"HW exact-fit: theta(0)={hw_theta(0,0.10,0.015):.4f} theta(5)={hw_theta(5,0.10,0.015):.4f}")
print(f"  MC P(0,5)={mh:.6f} vs flat target e^-0.2={math.exp(-0.04*5):.6f}  (exact fit confirmed)")
```
```
Vasicek P(0,5): closed=0.807678  MC=0.807470  err=2.1e-04
CIR     P(0,5): closed=0.804696  MC=0.804421  err=2.8e-04
CIR Feller 2ab=0.0200 >= sig^2=0.0025  -> r stays >0
HW exact-fit: theta(0)=0.0040 theta(5)=0.0047
  MC P(0,5)=0.818932 vs flat target e^-0.2=0.818731  (exact fit confirmed)
```
Closed forms and MC agree to $O(10^{-4})$ (MC sampling error). The Hull-White $\theta(t)$ reconstruction reproduces the target curve — **the model fits today's forwards by construction**, which is its reason for being.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Vasicek negative rates.** Gaussian $r$ means $\mathbb{P}(r<0)>0$; for low-rate or negative-rate regimes this is more than a theoretical blemish. CIR fixes it (at a cost: heavier calibration); negative-rate regimes force shifted-lognormal/Bachelier handling anyway ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05]]).
2. **Market price of risk is not identified by the model.** Bond prices depend on $\lambda$ only through the $\mathbb{Q}$-drift $\mu-\lambda\sigma$. From market *bond prices* alone you cannot separate $\lambda$ from the real-world drift — this is a fundamental identification problem, not a numerical one.
3. **Equilibrium vs no-arbitrage models.** Vasicek/CIR are *equilibrium* models: their implied curve rarely matches today's market curve. Hull-White is a *no-arbitrage* model: $\theta(t)$ forces exact fit. Using Vasicek to price a swap against the live curve misprices the residual.
4. **HW calibration differentiation instability.** Recovering $\theta(t)$ needs numerical derivatives of the market forward curve (up to 3rd order in Shreve Ch30 Remark 30.1); noisy or coarsely sampled curves make the fit numerically unstable.

---

### 5. Canonical Literature & Study References

- **Brigo–Mercurio**, *Interest Rate Models*, Ch 3 (one-factor short-rate models: Vasicek 3.5–3.10, CIR 3.21–3.26, Hull-White 3.33–3.43, affine structure 3.1–3.29, deterministic-shift / CIR++), Ch 4 (two-factor G2++). *Primary verified source.*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 23 (market price of risk, term-structure equation Prop 23.2) and Ch 24 (martingale models, affine Prop 24.2, Vasicek 24.3, CIR 24.6, Hull-White 24.8, Ho-Lee 24.4–24.5).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 29–32 (Gaussian/HW affine bond, CIR construction & Feller, Duffie-Kan two-factor).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 31 (equilibrium models) and Ch 32 (no-arbitrage models, HW $\theta$ 32.4).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates|02 · Bonds, Yield Curve & Forward Rates]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]]
