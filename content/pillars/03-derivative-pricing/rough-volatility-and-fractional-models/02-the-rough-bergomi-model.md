---
title: "02 — The rBergomi Model: Forward Variance, the Volterra Driver & the Power-Law Skew"
tags:
  - pillar-derivative-pricing
  - rough-volatility-and-fractional-models
  - rough-bergomi
  - forward-variance
  - volterra-process
  - atm-skew
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/01-from-zero-intuition|01 · From Zero]] and [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|SV · 04 Stochastic-Vol Dynamics]].

---

### 1. Intuition & Practical Objective

Bayer, Friz & Gatheral (2016) ask: *what is the minimal pricing model that inherits the empirical roughness of log-vol without losing tractability?* The answer is **rBergomi**: a forward-variance model whose variance is lognormal and driven by a **Riemann–Liouville Volterra process** $W^\alpha$ with $\alpha=H-\tfrac12<0$ — the fractional driver with the right covariance.

Three things to internalise:

1. **It is a forward-variance model, like Bergomi's $n$-factor model — but with a power-law kernel.** The variance is $v_t=\xi_0(t)\exp(\eta W^\alpha_t-\frac{\eta^2}{2}t^{2H})$, which keeps $\mathbb E[v_t]=\xi_0(t)$ (the forward-variance curve stays a market input). What makes it *rough* is replacing the exponential OU kernel with $(t-u)^{H-\frac12}$.
2. **The exponent $\alpha=H-\tfrac12$ is the whole design.** Because $W^\alpha_t=\sqrt{2\alpha+1}\int_0^t(t-u)^\alpha dW_u$ has $\mathrm{Var}[W^\alpha_t]=t^{2\alpha+1}=t^{2H}$, the log-variance inherits the fBm increment law $\nu^2\Delta^{2H}$ — the exact GJR scaling. Roughness is *built in by the kernel exponent*, not added as an afterthought.
3. **The skew falls out of the Bergomi–Guyon machinery.** The ATMF skew of *any* forward-variance model is $S_T=\frac{\rho\eta\sqrt{2H}}{2(H+\frac12)(H+\frac32)}T^{H-\frac12}$ at order one (verified in §3) — a power law in $T$ with exponent $H-\tfrac12\approx-0.36$, precisely the SPX $\tau^{-0.44}$ regime, and blowing up as $T\to0$ in a way no Markovian model can.

The practical objective: be able to write the rBergomi SDE, understand why $E[v_t]=\xi_0(t)$ is the martingale check, know the three parameters $(H,\eta,\rho)$, and reproduce the power-law ATMF skew from the Bergomi–Guyon expansion.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The model

Under $\mathbb Q$, with $S_0$ scaled to 1 and the forward-variance curve $\xi_0(u)$ given by the market:

$$
S_t=\mathcal E\!\Big(\int_0^t\sqrt{v_u}\,d\big(\rho W^1_u+\sqrt{1-\rho^2}W^2_u\big)\Big)_t,\qquad
v_t=\xi_0(t)\exp\!\Big(\eta W^\alpha_t-\frac{\eta^2}{2}t^{2\alpha+1}\Big),
$$

$$
W^\alpha_t=\sqrt{2\alpha+1}\int_0^t(t-u)^\alpha\,dW^1_u,\qquad \alpha=H-\tfrac12\in(-\tfrac12,0),
$$

where $W^1,W^2$ are independent Brownian motions and $\mathcal E(\cdot)$ is the stochastic exponential. The Volterra process $W^\alpha$ is a centred, $(\alpha+\tfrac12-\varepsilon)$-Hölder, **non-semimartingale** Gaussian process with $\mathrm{Var}[W^\alpha_t]=t^{2\alpha+1}=t^{2H}$ — "rough" in the precise sense of having $H<\tfrac12$.

#### 2.2 Why $E[v_t]=\xi_0(t)$ (the martingale check)

Since $W^\alpha_t$ is Gaussian with variance $t^{2H}$,

$$
\mathbb E\Big[e^{\eta W^\alpha_t}\Big]=e^{\frac{\eta^2}{2}t^{2H}},
$$

so $\mathbb E[v_t]=\xi_0(t)e^{-\frac{\eta^2}{2}t^{2H}}\cdot e^{\frac{\eta^2}{2}t^{2H}}=\xi_0(t)$. The drift term $-\frac{\eta^2}{2}t^{2H}$ is *exactly* the lognormal compensator — get its sign or the exponent $t^{2H}$ (i.e. the mapping $\alpha=H-\tfrac12$) wrong and the martingale fails. This is the first check on any implementation, verified in §3.

#### 2.3 The ATMF skew from Bergomi–Guyon

For a forward-variance model, the order-1 ATMF skew is (Bergomi ch 8, [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]])

$$
S_T:=\left.\frac{\partial\sigma_{BS}}{\partial k}\right|_{k=0}=\frac{C^{x\xi}(T)}{2\hat\sigma_T^3T^2},\qquad
C^{x\xi}(T)=\int_0^T\!dt\int_t^T\!du\ \frac{\mathbb E[dx_t\,d\xi_t(u)]}{dt}.
$$

For rBergomi the spot/forward-variance covariance is $\frac{\mathbb E[dx_t\,d\xi_t(u)]}{dt}=\rho\sqrt{\xi_t^t}\,\xi_t(u)\,\eta\sqrt{2H}(u-t)^{H-\frac12}$; on a flat forward-variance curve $\xi_0=\sigma_0^2$ this gives

$$
C^{x\xi}(T)=\rho\eta\sqrt{2H}\,\sigma_0^3\int_0^T\!dt\int_t^T\!du\ (u-t)^{H-\frac12}
=\rho\eta\sqrt{2H}\,\sigma_0^3\,\frac{T^{H+\frac32}}{(H+\frac12)(H+\frac32)},
$$

$$
\boxed{\;\psi(T)=|S_T|=\frac{\rho\eta\sqrt{2H}}{2(H+\tfrac12)(H+\tfrac32)}\,T^{H-\frac12}\;}
$$

The double integral is evaluated exactly (§3): $\int_0^T\int_t^T (u-t)^{H-\frac12}dudt=\frac{T^{H+3/2}}{(H+1/2)(H+3/2)}$. The result is the **power-law skew** $\psi(T)\propto T^{H-\frac12}$ with exponent $H-\tfrac12=-0.36$ for $H=0.14$ — the empirically observed $\tau^{-0.44}$ regime, and qualitatively different from the Markovian cap (§05).

---

### 3. Computational Implementation — the martingale check and the skew power law

We (i) verify the two defining identities of the hybrid-scheme rBergomi — $\mathrm{Var}[W^\alpha_t]=t^{2H}$ and $\mathbb E[v_t]=\xi_0(t)$ — and (ii) verify the Bergomi–Guyon skew functional: the double integral equals its closed form, and the resulting $\psi(T)$ scales as $T^{H-\frac12}$. Stdlib only.

```python
import math, random
# (i) hybrid scheme (BLP 2017, kappa=1) -> Volterra process W^alpha
def hybrid_volterra(n, alpha, seed):
    random.seed(seed); sq=2.0*alpha+1.0
    b=[0.0]*(n+1)
    for k in range(1,n+1):
        b[k]=((k**(alpha+1)-(k-1)**(alpha+1))/(alpha+1))**(1.0/alpha)
    dW=[random.gauss(0,1)/math.sqrt(n) for _ in range(n)]
    W=[0.0]
    for i in range(n): W.append(W[-1]+dW[i])
    out=[0.0]*(n+1); prox_sd=(1.0/n)**(alpha+0.5)/math.sqrt(sq)
    for i in range(1,n+1):
        ff=sum((b[k]/n)**alpha*(W[i-(k-1)]-W[i-k]) for k in range(2,i+1))
        out[i]=math.sqrt(sq)*(prox_sd*random.gauss(0,1)+ff)
    return out
H=0.14; alpha=H-0.5; eta=0.30; xi0=0.04; n=150; N=8000
tvals=[0.2,0.5,0.8,1.0]; idx=[int(t*n) for t in tvals]
sumV=[0.0]*len(idx); varW=[0.0]*len(idx)
for s in range(N):
    w=hybrid_volterra(n,alpha,seed=s)
    for j,i in enumerate(idx):
        tt=i/n; V=xi0*math.exp(eta*w[i]-0.5*eta*eta*tt**(2*H))
        sumV[j]+=V; varW[j]+=w[i]*w[i]
print("(i) hybrid-scheme identities: Var[W^alpha_t] vs t^{2H};  E[v_t] vs xi_0(t)")
for j,i in enumerate(idx):
    tt=i/n; ev=sumV[j]/N
    print(f"    t={tt:4.2f}  Var[W]={varW[j]/N:.4f} vs t^{{2H}}={tt**(2*H):.4f}  |  "
          f"E[v_t]={ev:.4f} vs xi0={xi0:.4f}  rel.err={abs(ev-xi0)/xi0*100:.2f}%")
print("\n(ii) Bergomi-Guyon skew functional, power-law kernel (u-t)^{H-1/2}:")
def I_closed(H,T): return T**(H+1.5)/((H+0.5)*(H+1.5))
def I_numeric(H,T,n=120):
    h=T/n; tot=0.0
    for i in range(n):
        t=(i+0.5)*h; tot+=(T-t)**(H+0.5)/(H+0.5)*h
    return tot
for T in (0.1, 0.5, 1.0):
    print(f"    I(H,T) T={T:4.2f}: closed={I_closed(H,T):.5f}  numeric={I_numeric(H,T):.5f}")
eta2,rho2=1.9,-0.9
def S_T(T): return rho2*eta2*math.sqrt(2*H)*I_closed(H,T)/(2*T*T)
lx=[]; ly=[]
for T in (0.03,0.1,0.3,1.0,3.0):
    s=S_T(T); lx.append(math.log(T)); ly.append(math.log(abs(s)))
    print(f"    T={T:5.2f}  psi(T)=|S_T|={abs(s):+.4f}   T^(H-1/2)={T**(H-0.5):.4f}   ratio={abs(s)/T**(H-0.5):.3f}")
xb=sum(lx)/len(lx); yb=sum(ly)/len(ly)
slope=sum((lx[i]-xb)*(ly[i]-yb) for i in range(len(lx)))/sum((lx[i]-xb)**2 for i in range(len(lx)))
print(f"    OLS slope of log|S_T| vs log T = {slope:.3f}   (theory H-1/2 = {H-0.5:.3f})")
```
```
(i) hybrid-scheme identities: Var[W^alpha_t] vs t^{2H};  E[v_t] vs xi_0(t)
    t=0.20  Var[W]=0.6208 vs t^{2H}=0.6372  |  E[v_t]=0.0399 vs xi0=0.0400  rel.err=0.16%
    t=0.50  Var[W]=0.8122 vs t^{2H}=0.8236  |  E[v_t]=0.0399 vs xi0=0.0400  rel.err=0.25%
    t=0.80  Var[W]=0.9537 vs t^{2H}=0.9394  |  E[v_t]=0.0401 vs xi0=0.0400  rel.err=0.13%
    t=1.00  Var[W]=1.0338 vs t^{2H}=1.0000  |  E[v_t]=0.0402 vs xi0=0.0400  rel.err=0.55%

(ii) Bergomi-Guyon skew functional, power-law kernel (u-t)^{H-1/2}:
    I(H,T) T=0.10: closed=0.02183  numeric=0.02183
    I(H,T) T=0.50: closed=0.30569  numeric=0.30570
    I(H,T) T=1.00: closed=0.95274  numeric=0.95278
    T= 0.03  psi(T)=|S_T|=+1.5232   T^(H-1/2)=3.5338   ratio=0.431
    T= 0.10  psi(T)=|S_T|=+0.9875   T^(H-1/2)=2.2909   ratio=0.431
    T= 0.30  psi(T)=|S_T|=+0.6649   T^(H-1/2)=1.5425   ratio=0.431
    T= 1.00  psi(T)=|S_T|=+0.4310   T^(H-1/2)=1.0000   ratio=0.431
    T= 3.00  psi(T)=|S_T|=+0.2902   T^(H-1/2)=0.6733   ratio=0.431
    OLS slope of log|S_T| vs log T = -0.360   (theory H-1/2 = -0.360)
```

**What the output establishes.**

- **(i) The hybrid scheme reproduces both defining identities.** $\mathrm{Var}[W^\alpha_t]$ tracks $t^{2H}$ (within ~3%, the discretisation error of the singular kernel) and — with a small $\eta$ so the estimator is well-conditioned — $\mathbb E[v_t]=\xi_0(t)$ to within $0.55\%$. With $\eta=1.9$ the martingale still holds exactly in law; the naive MC estimate just becomes heavy-tailed ([[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/05-failure-modes-and-practice|05 · Failure Modes]]).
- **(ii) The closed-form double integral is right to 5 decimals**, and $\psi(T)=|S_T|\propto T^{H-\frac12}$ with OLS slope $-0.360$ exactly equal to $H-\tfrac12$. The constant of proportionality $\frac{\rho\eta\sqrt{2H}}{2(H+\frac12)(H+\frac32)}$ equals $0.4310$ — so $\psi(T)=0.431\,T^{-0.36}$ for these parameters. A Monte Carlo pricing of the actual skew in §05 confirms the exponent ($-0.392$ with MC noise).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Wrong sign on the compensator.** The $- \frac{\eta^2}{2}t^{2H}$ term is load-bearing: flip it and $\mathbb E[v_t]=\xi_0(t)e^{\eta^2t^{2H}}\neq\xi_0(t)$, silently mispricing everything. Always check the martingale (§3(i)).
2. **Confusing $\alpha$ and $H$.** The model is written with $\alpha=H-\tfrac12$; the variance exponent is $t^{2\alpha+1}=t^{2H}$. Papers use both — a factor of 2 in the exponent of $t$ is an easy, catastrophic slip.
3. **The singular kernel breaks naive Euler.** $(t-u)^\alpha$ diverges at $u\to t$; a plain Euler discretisation is biased and has no Brownian-limit consistency. The hybrid scheme's proximal-term handling is not cosmetic ([[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/04-hurst-estimation-and-simulation|04 · Simulation]]).
4. **$\rho,\eta$ sign and the skew orientation.** With equity $\rho<0$ the skew is negative; the formula is $\psi(T)=\frac{\rho\eta\sqrt{2H}}{\cdots}T^{H-\frac12}$, so a wrong $\rho$ sign flips the skew. Calibrate $\rho$ from the leverage effect / spot-vol covariance, not from H.
5. **The order-1 expansion is a near-the-money tool.** $\psi(T)\propto T^{H-\frac12}$ is the ATMF slope at order one; using it to extrapolate the whole smile (the wings) is outside its validity — Lee's moment formula still governs extreme strikes ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|03 · SABR & Asymptotics]]).

---

### 5. Canonical Literature & Study References

- **Bayer, Friz & Gatheral (2016)**, *Pricing under rough volatility*, Quantitative Finance 16(6), 887–904 — the rBergomi model, its forward-variance form, and the SPX calibration $\eta=1.9,\rho=-0.9$. *The primary source of this page.*
- **Gatheral, Jaisson & Rosenbaum (2018)**, *Volatility is rough*, Quantitative Finance 18(6), 933–949 — the RFSV scaling law that rBergomi is the pricing-compatible lift of.
- **Bennedsen, Lunde & Pakkanen (2017)**, *Hybrid scheme for Brownian semistationary processes*, Finance and Stochastics 21(4), 931–965 — the exact hybrid discretisation (first-order κ=1 form used here).
- **Bergomi (2016)**, *Stochastic Volatility Modeling*, ch 7–8 — forward-variance pricing equation and the **Bergomi–Guyon expansion** ($C^{x\xi}$ functional) that produces the skew formula of §2.3; ch 7's power-law vol-of-vol benchmark $\nu_T\propto T^{-0.4}$ is the same roughness.
- **Fukasawa (2017)**, *Short-time at-the-money skew and rough fractional volatility* — rigorous short-time skew asymptotics.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/01-from-zero-intuition|01 · From Zero]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|SV · 04 SV Dynamics]] (forward-variance framework + Bergomi–Guyon)
- Forward: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/04-hurst-estimation-and-simulation|04 · Hurst Estimation & Simulation]] · [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] (Volterra integrals, non-semimartingales) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|02 · The Heston Model]] (the affine/CF baseline rBergomi abandons) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|SV · 06 Advanced Extensions]] (the frontier flag pointing here)
