---
title: "06 — Advanced Extensions: Jumps, Forward-Variance Models, LSV & Rough Volatility"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - jumps
  - forward-variance
  - local-stochastic-volatility
  - rough-volatility
  - vix
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]] and [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

Heston and SABR are the entry points, not the destination. Each of their failures points at a specific extension, and this page maps the ladder:

| failure of Heston/SABR | extension | what it buys |
|---|---|---|
| cannot fit the short-dated skew (which rises faster than any time-homogeneous SV allows) | **jumps** (SVJ / SVJJ / Lévy) | the $-2\mu_J$ additive skew term at $\tau\to0$ |
| cannot fit a general variance-swap term structure and a power-law vol-of-vol term structure | **forward-variance (multi-factor OU) models** | exact VS calibration by construction; term-structure control |
| calibrated vanillas do not pin the dynamics | **Bergomi–Guyon** ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04]]) | an inventory of which functionals matter |
| local vol fits statics but kills forward skew; Heston fits statics but not the short end | **local-stochastic vol (LSV)** | both — *if* the model is "usable" |
| the short-dated skew behaves as $T^{H-\frac12}$ with $H\approx0.1$, not $T^{1/2}$ | **rough volatility** | the empirical short-end scaling |

The practical objective: know what each extension actually fixes, what it costs (parameters, simulation complexity, identifiability), and which are desk-standard versus frontier. The one thing to internalise: **extensions are bought to fix *dynamics*, and the price is paid in identifiability.**

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Jumps: SVJ and SVJJ (Gatheral ch 5)

Add a compound Poisson jump to the spot (Merton), keeping Heston variance — the **SVJ** model:

$$dS=\mu S\,dt+\sqrt v\,S\,dZ_1+(e^{\alpha+\delta Z}-1)S\,dq,\quad Z\sim N(0,1),\qquad dv=-\lambda(v-\bar v)dt+\eta\sqrt v\,dZ_2,$$

with log-jump size $\sim\mathcal N(\alpha,\delta^2)$. The characteristic function **factorises** (Gatheral ch 5):

$$\varphi_T(u)=e^{C(u,T)\bar v+D(u,T)v_0}\,e^{\psi(u)T},\qquad \psi(u)=-\lambda_Jiu\big(e^{\alpha+\delta^2/2}-1\big)+\lambda_J\big(e^{iu\alpha-u^2\delta^2/2}-1\big),$$

so the Heston $C,D$ are untouched and the jump part is a separate, cheap term. Two facts decide how to fit it:

- **The short-dated variance skew is exactly additive:** $\partial_k\sigma_{BS}^2|_0\to\rho\eta/2-2\mu_J$ with compensator $\mu_J=\lambda_J\mathbb E[J]$ (Gatheral 7.8). Fit Heston on the long end (which it handles well) and the jump parameters on the short end (which it does not).
- **Jumps *in volatility* (SVJJ, Matytsin) do not help the short-dated skew at all.** Because the short skew depends only on the jump *compensator*, identical in SVJ and SVJJ (after the jump an ATM option is out-of-the-money with zero time value whatever the vol does). Vol-jumps do reduce the vol-of-vol needed for *longer*-dated skew — at the cost of three more parameters and a harder fit. Gatheral's verdict: **SVJ beats SVJJ** on real SPX data (Table 5.5: $v_0=0.0158,\bar v=0.0439,\eta=0.3038,\rho=-0.6974,\lambda=0.5394,\lambda_J=0.1308,\delta=0.0967,\alpha=-0.1151$ reproduces the surface where Heston cannot).
- **Drawback:** after a price jump, volatility stays fixed (jumps and vol are uncorrelated), inconsistent with the observation that implied vols jump when spot jumps. And jumps destroy the static-hedging/completeness arguments that make diffusive models tractable: with uncertain jump size there is **no replicating hedge** — options stop being redundant (Gatheral §5.1).
- **Reading (Bergomi ch 10):** a Lévy/jump component is best understood not as a dynamics but as an embedded **stress-test reserve policy** — extra theta, a cost-of-capital levy ($\lambda=\beta\mu$), or a minimum return on stress-limit usage. "Using a diffusive process for pricing does not mean we assume securities behave as diffusions."

#### 2.2 Forward-variance models: the desk-grade fix (Bergomi ch 7)

Model the curve $\{\xi_t^T\}$ directly. The pricing equation (7.4) plus the cardinal rule $\sigma(t,S,\xi)^2=\xi_t^t$ gives a driftless, exactly-calibratable-to-VS system, with the $N$-factor Markov representation

$$d\xi_t^T=\omega\alpha_w\xi_t^T\sum_iw_ie^{-k_i(T-t)}dW_t^i,\qquad \xi_t^T=\xi_0^T\exp\Big(\omega\sum_iw_ie^{-k_i(T-t)}X_t^i-\frac{\omega^2}{2}\sum_{ij}w_iw_je^{-(k_i+k_j)(T-t)}\mathbb E[X_t^iX_t^j]\Big),$$

with $\omega=2\nu$, $\alpha_w=1/\sqrt{\sum_{ij}w_iw_j\rho_{ij}}$, and the **exact** OU transitions (7.15–7.18)

$$X^i_{\tau_{n+1}}=e^{-k_i\delta\tau}X^i_{\tau_n}+\delta X^i,\quad \mathbb E[\delta X^i\delta X^j]=\rho_{ij}\frac{1-e^{-(k_i+k_j)\delta\tau}}{k_i+k_j},\quad \mathbb E[\delta W^S\delta X^i]=\rho_{iS}\frac{1-e^{-k_i\delta\tau}}{k_i}.$$

Because the transition law is exact, **no time discretisation bias** enters for variance-only payoffs (realized variance, variance swaps, VIX) — a decisive practical advantage over Heston simulation. The stationary vol-of-vol and correlation structures are

$$\nu_T(t)=\nu\alpha_w\sqrt{\textstyle\sum_{ij}w_iw_j\rho_{ij}I(k_i(T-t))I(k_j(T-t))},\quad I(x)=\frac{1-e^{-x}}{x},$$

$$\omega(T-t)=2\nu\alpha_w\sqrt{\textstyle\sum_{ij}w_iw_j\rho_{ij}e^{-(k_i+k_j)(T-t)}},\qquad \rho_t(\xi^T,\xi^{T'})=\frac{\sum w_iw_j\rho_{ij}e^{-k_i(T-t)}e^{-k_j(T'-t)}}{\sqrt{\cdots}},$$

and the break-even covariances (7.27a,b) that close the pricing equation. **VIX** is (a scaling of) the variance-swap variance for $T=30$d; VIX futures are $\mathbb E_t[\sqrt{\cdot}\,]$ in this model, priced by two-dimensional quadrature over $(X^1,X^2)$. **Vega hedging caveat (Bergomi §7.3.3):** the $N$-factor structure does *not* justify hedging only $N$ variance swaps — deltas must immunise against **all** deformations $\delta\xi^T$; the factors only fix the *rank* of the break-even covariance matrix.

#### 2.3 Local-stochastic volatility (LSV) — and why "usable" is a real constraint

LSV multiplies the local-vol component onto the stochastic variance (Bergomi 12.1–12.2):

$$\sigma_t=\sqrt{\zeta_t^t}\,\sigma(t,S_t),\qquad dS_t=(r-q)S_tdt+\sigma(t,S_t)\sqrt{\zeta_t^t}S_tdW^S,\qquad d\zeta_t^T=2\nu\alpha_\theta\zeta_t^T\big[(1-\theta)e^{-k_1(T-t)}dW^1+\theta e^{-k_2(T-t)}dW^2\big]$$

with the mixed covariance $\mu(t,u,\xi)=2\nu\xi^u\sqrt{\xi^t}\alpha_\theta[\rho_{SX^1}(1-\theta)e^{-k_1(u-t)}+\rho_{SX^2}\theta e^{-k_2(u-t)}]$ (12.4/8.50 — note the radical covers only $\xi^t$). The appeal is obvious: the local part fits the statics exactly, the stochastic part restores forward skew. **The warning is equally clear (Bergomi §12.2.2):** the LSV pricing equation is *not* derived from a replication argument — it is the forward-variance equation with the ansatz $\sqrt{\zeta_t^t}\to\sqrt{\zeta_t^t}\sigma(t,S_t)$. Whether its solution is a *price* (i.e. whether the hedge P&L has the usual gamma/theta form) must be verified *a posteriori*: **"most local-stochastic volatility models are not usable models."** The characterisation of usable LSV, the decomposition of the ATMF skew into its components, and the resulting SSR/vol-of-vol dynamics are Bergomi §12.3–12.4 — a *separate* deep-read from the corpus used here.

#### 2.4 Rough volatility

Empirically, log realized volatility has Hurst exponent $H\approx0.1$ (Gatheral–Jaisson–Rosenbaum 2018) — far rougher than a diffusion ($H=\tfrac12$), with a power-law autocorrelation of log-vol. Replacing the OU factors by a fractional Brownian motion, $\sigma_t=\exp(X_t)$ with $X$ fBm of Hurst $H$, gives a short-dated ATM skew that scales as

$$\frac{\partial\sigma_{BS}}{\partial k}\sim T^{H-\frac12},$$

i.e. much steeper than any Markovian SV model permits — precisely the short-end failure flagged in §04/§05, and the same power-law family as Bergomi's benchmark $\nu_T(t)=\sigma_0(\tau_0/(T-t))^{\alpha}$, $\alpha\approx0.4$ (note $\alpha\leftrightarrow\tfrac12-H$ in spirit). The cost is that the model is non-Markovian, harder to simulate, and harder to calibrate jointly to SPX and VIX. This is a **forward pointer** beyond the corpus files used for this folder.

---

### 3. Computational Implementation — the two-factor model, simulated exactly

We verify the two structural facts that make forward-variance models desk-usable: (i) the closed-form $\chi(t,T)$ used in the exponent equals the exact integral $\int_{T-t}^T\eta^2(u)du$ (so $\xi_t^T$ is a genuine martingale), (ii) the exact OU simulation reproduces $\mathbb E[\xi_t^T]=\xi_0^T$ and the instantaneous vol-of-vol $\omega^2\eta^2(T)$, and (iii) the model implies a **VIX-versus-variance-swap convexity gap** of the right sign. Stdlib only.

```python
import math, random

nu,th,k1,k2,r12=1.74,0.245,5.35,0.28,0.0     # Bergomi Set II (Table 7.1)
om=2.0*nu; aw=1.0/math.sqrt((1-th)**2+th**2+2*r12*th*(1-th)); xi0=0.04

def eta2(u):                                  # (7.31)^2
    return aw*aw*((1-th)**2*math.exp(-2*k1*u)+th**2*math.exp(-2*k2*u)+2*r12*th*(1-th)*math.exp(-(k1+k2)*u))
def Var_X(t):                                 # E[X^i X^j] (7.16)
    return ((1-math.exp(-2*k1*t))/(2*k1), (1-math.exp(-2*k2*t))/(2*k2),
            r12*(1-math.exp(-(k1+k2)*t))/(k1+k2))
def chi(t,T):
    v11,v22,v12=Var_X(t)
    return aw*aw*((1-th)**2*math.exp(-2*k1*(T-t))*v11 + th**2*math.exp(-2*k2*(T-t))*v22
                  + 2*r12*th*(1-th)*math.exp(-(k1+k2)*(T-t))*v12)
def chi_integral(t,T,n=200000):               # int_{T-t}^{T} eta^2(u) du
    a,b=T-t,T; h=(b-a)/n; s=eta2(a)+eta2(b)
    for i in range(1,n): s+=(4.0 if i%2 else 2.0)*eta2(a+i*h)
    return s*h/3.0

print("(1) consistency: Var[x_t^T] = chi(t,T) vs the exact integral of eta^2(u)")
for t,T in ((0.01,1.0),(1.0,1.0),(1.0,5.0),(3.0,5.0)):
    print(f"    t={t:5.2f} T={T:5.2f}: chi={chi(t,T):.8f}  integral={chi_integral(t,T):.8f}  diff={chi(t,T)-chi_integral(t,T):+.2e}")

def simulate(npath,dt,t,Ts,seed=7):
    random.seed(seed); n=int(round(t/dt))
    sd1=math.sqrt((1-math.exp(-2*k1*dt))/(2*k1)); sd2=math.sqrt((1-math.exp(-2*k2*dt))/(2*k2))
    acc={T:0.0 for T in Ts}; accsq={T:0.0 for T in Ts}
    for _ in range(npath):
        X1=X2=0.0
        for _ in range(n):
            X1=math.exp(-k1*dt)*X1+sd1*random.gauss(0,1)
            X2=math.exp(-k2*dt)*X2+sd2*random.gauss(0,1)
        for T in Ts:
            x=aw*((1-th)*math.exp(-k1*(T-t))*X1+th*math.exp(-k2*(T-t))*X2)
            lx=om*x-0.5*om*om*chi(t,T)            # log(xi_t^T/xi_0^T), (7.33)-(7.35)
            acc[T]+=xi0*math.exp(lx); accsq[T]+=lx*lx
    return {T:(acc[T]/npath, accsq[T]/npath) for T in Ts}

print("(2) martingale: E[xi_t^T] = xi_0^T = 0.04, and Var[log xi_t^T]/t -> omega^2*eta^2(T) as t->0")
for t,Ts in ((1.0,[1.0,2.0,5.0]),(0.01,[1.0])):
    for T,(m,v) in simulate(40000,0.005 if t>0.1 else 0.0005,t,Ts).items():
        print(f"    t={t:5.3f} T={T:5.2f}: mean(xi)={m:.6f} (target {xi0})   Var[log xi]/t={v/t:.6f}"
              f"   omega^2*eta^2(T)={om*om*eta2(T):.6f}")

tau=30.0/365.0
def sim_vix(npath,seed=11):
    random.seed(seed); dt=0.002; n=int(round(1.0/dt))
    sd1=math.sqrt((1-math.exp(-2*k1*dt))/(2*k1)); sd2=math.sqrt((1-math.exp(-2*k2*dt))/(2*k2))
    roots=0.0; means=0.0
    for _ in range(npath):
        X1=X2=0.0
        for _ in range(n):
            X1=math.exp(-k1*dt)*X1+sd1*random.gauss(0,1)
            X2=math.exp(-k2*dt)*X2+sd2*random.gauss(0,1)
        m=400; a,b=1.0,1.0+tau; h=(b-a)/m; s=0.0
        for i in range(m+1):
            T=a+i*h
            x=aw*((1-th)*math.exp(-k1*(T-1.0))*X1+th*math.exp(-k2*(T-1.0))*X2)
            val=xi0*math.exp(om*x-0.5*om*om*chi(1.0,T))
            s+=(1.0 if i in (0,m) else (4.0 if i%2 else 2.0))*val
        V=s*h/3.0/tau
        roots+=math.sqrt(V); means+=V
    return roots/npath, means/npath

r,m=sim_vix(4000)
print("(3) VIX-style convexity at t=1, 30-day horizon:")
print(f"    E[sqrt(V)]={r:.6f}   sqrt(E[V])={math.sqrt(m):.6f}   gap={r-math.sqrt(m):+.6f} (Jensen)")
```
```
(1) consistency: Var[x_t^T] = chi(t,T) vs the exact integral of eta^2(u)
    t= 0.01 T= 1.00: chi=0.00054593  integral=0.00054593  diff=+2.28e-18
    t= 1.00 T= 1.00: chi=0.15750050  integral=0.15750050  diff=-2.28e-15
    t= 1.00 T= 5.00: chi=0.00776596  integral=0.00776596  diff=-1.47e-16
    t= 3.00 T= 5.00: chi=0.04516314  integral=0.04516314  diff=+4.86e-16
(2) martingale: E[xi_t^T] = xi_0^T = 0.04, and Var[log xi_t^T]/t -> omega^2*eta^2(T) as t->0
    t=1.000 T= 1.00: mean(xi)=0.040078 (target 0.04)   Var[log xi]/t=2.832229   omega^2*eta^2(T)=0.659285
    t=1.000 T= 2.00: mean(xi)=0.039755 (target 0.04)   Var[log xi]/t=0.564695   omega^2*eta^2(T)=0.376449
    t=1.000 T= 5.00: mean(xi)=0.039902 (target 0.04)   Var[log xi]/t=0.095331   omega^2*eta^2(T)=0.070160
    t=0.010 T= 1.00: mean(xi)=0.040006 (target 0.04)   Var[log xi]/t=0.663842   omega^2*eta^2(T)=0.659285
(3) VIX-style convexity at t=1, 30-day horizon:
    E[sqrt(V)]=0.168534   sqrt(E[V])=0.205718   gap=-0.037184 (Jensen)
```

**Reading the output.**

- **(1) The exponent's $\chi(t,T)$ is exactly $\int_{T-t}^T\eta^2(u)du$** — agreement to $10^{-15}$ across four $(t,T)$ pairs. This is *why* $\xi_t^T$ is a martingale: the driftless lognormal ansatz needs $\mathrm{Var}[\omega x_t^T]=\omega^2\chi$ to cancel in the expectation, and the identity provides exactly that.
- **(2) The martingale property holds in simulation.** $\mathbb E[\xi_1^T]$ is $0.040078$, $0.039755$, $0.039902$ for $T=1,2,5$ against the initial curve $0.04$ — all within Monte Carlo error at 40 000 paths. And the instantaneous vol-of-vol check is sharp: at $t=0.01$ the simulated $\mathrm{Var}[\log\xi_t^T]/t=0.6638$ against the analytic $\omega^2\eta^2(T)=0.6593$ ($0.7\%$, the MC error of a variance estimate on 40 000 paths). The $t{=}1$ rows are *not* this limit (the window $[T-t,T]$ is long), and are shown only to display the maturity profile: forward variance for far maturities is much better behaved than for near ones.
- **(3) VIX versus variance swap.** $\mathbb E[\sqrt V]=0.1685$ against $\sqrt{\mathbb E[V]}=0.2057$ — a $(16.85,20.57)$ vol-point pair, i.e. the model-implied **VIX-futures/VS-vol gap**, with the correct sign ($\mathbb E[\sqrt{\cdot}]<\sqrt{\mathbb E[\cdot]}$ by Jensen). The *magnitude* here is dictated by Set II's deliberately high $\nu=174\%$ (chosen to fit the power-law benchmark over 0.25–5y, §04); with realistic index $\nu$ the gap is on the order of one vol point. The mechanism — VIX is a concave (square-root) functional of the variance curve, so VIX futures trade *below* the variance-swap strike — is the reason the two are separate products with separate hedges.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Adding jumps to fix the long end.** Jumps contribute $-2\mu_J$ to the *short-dated* variance skew and nothing structural to the term structure. Using SVJ to repair the long end over-fits the short end and mis-attributes the risk (Gatheral ch 5).
2. **Buying vol-jumps (SVJJ) expecting a better short end.** They contribute nothing at $\tau\to0$ (the skew depends only on the jump compensator) while adding three parameters and a harder fit. SVJ fits the SPX surface with *fewer* parameters.
3. **Using an LSV model without the usability check.** LSV's pricing equation is an *ansatz*, not a replication result; the hedge P&L must be verified. "Most LSV models are not usable models" (Bergomi §12.2.2).
4. **Hedging a forward-variance model with only $N$ variance swaps.** The Markov structure fixes the *rank* of the break-even covariance matrix; deltas must immunise against *all* deformations $\delta\xi^T$ (Bergomi §7.3.3).
5. **Treating $\xi_0^T$ as a calibration output.** In forward-variance models the variance curve is a *market input* from the (more liquid) variance-swap market. Calibrating it to vanillas discards the best-quality information in the market.
6. **Ignoring the dividend/rate effect on variance swaps.** The log-contract replication needs a discrete-dividend correction (Bergomi 5.44–5.47), and index VS vols and ATMF vols differ through rate vol too: $\hat\sigma_{VS,T}=\hat\sigma_T-\frac{\rho}{2}\sigma_rT$ (5.54–5.55) — one vol point for 5y EUR rates at 5bp/day.
7. **Jumping to rough vol without the infrastructure.** Rough vol fixes the short-end scaling but is non-Markovian: pricing needs fractional-kernel simulation or the multifactor Markov approximation, and joint SPX/VIX calibration is materially harder. Adopt it for a *reason* (the $T^{H-1/2}$ skew), not for fashion.
8. **Extending a model because it fits better.** More parameters always fit better; the relevant test is whether the extension changes a *dynamic* quantity (SSR, $\nu_T$, forward skew) in the direction the market says. Otherwise it is a stress reserve (jumps) or unidentifiable noise (extra factors).

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 5 in full (jump-diffusion SDE 5.1, valuation equations 5.2–5.3, Lévy–Khintchine 5.4, Merton CF 5.5, **Lewis call formula 5.6**, implied vol from CF 5.7, ATM skew 5.8/5.10, SVJ factorisation, SVJJ 5.11 with $I(u,T)$ and $p_\pm$, empirical fits Table 5.4 and the SVJ SPX fit Table 5.5, "no replicating hedge" §5.1), Ch 6 (default risk as a skew driver: Merton jump-to-ruin, CreditGrades), Ch 10 (cliquet valuations; the LV/SV table). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 5 (variance swaps: replication 5.28–5.31, discrete strikes 5.3–5.4, dividends 5.44–5.47, rate vol 5.54–5.55, weighted VS 5.56–5.58, **timer options** 5.67–5.76, Gram–Charlier App. B), Ch 7 in full (pricing equation 7.4, break-even covariances 7.2/7.27, Markov representation 7.9–7.13, exact simulation 7.15–7.18, vol-of-vol/correlations 7.19–7.26, **two-factor model 7.28–7.39, benchmark 7.40, VS swaption approximation 7.41**, VIX/realized-variance §7.6–7.7, rank-of-covariance caveat §7.3.3), Ch 10 (**what causes equity smiles**: Student-$t$ one-day returns 10.1–10.7, the $1/T$ one-day-smile contribution 10.10, daily cliquets 10.2, jumps as a reserve policy App. A: P&L 10.12, reserve 10.14, jump pricing equation 10.18, Lévy–Khintchine 10.29), Ch 12 (**LSV**: 12.1–12.4 and the "not usable models" warning §12.2.2). *Math-verified.*
- **Gatheral, Jaisson & Rosenbaum** (2018), *Volatility is rough* — the $H\approx0.1$ empirical finding and the rough-vol programme. **Bayer, Friz & Gatheral** (2016) on pricing under rough vol; **El Euch & Rosenbaum** (2019) on the rough Heston Markovian lift. *Forward pointers beyond the verified corpus of this folder.*
- **Hagan et al.** (2002) for SABR ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|03]]); **Duffie–Pan–Singleton** (2000) for the affine class; **Matytsin** (1999) for SVJJ; **Andersen–Andreasen** (2000) and **Bakshi–Cao–Chen** (1997) for the empirical jump fits cited by Gatheral Table 5.4.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 20 §20.7–20.8 (model as interpolation tool; the single-large-jump "frown"), Ch 23 (volatility term structure). *Verification report in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Index Hub]]
- Sibling / back-references: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|VS · 06 Advanced Extensions]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR (flat note)]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|VS · 05 Failure Modes]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] (SABR / LMM) · [[pillars/04-quantitative-risk/var-and-expected-shortfall|Quantitative Risk]] (stress reserves and model risk)
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
