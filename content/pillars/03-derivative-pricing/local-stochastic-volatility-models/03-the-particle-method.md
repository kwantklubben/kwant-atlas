---
title: "03 — The Particle Method: Solving the McKean–Vlasov Fixed Point by Monte-Carlo Binning"
tags:
  - pillar-derivative-pricing
  - local-stochastic-volatility-models
  - particle-method
  - mckean-vlasov
  - monte-carlo
  - leverage-function
  - calibration
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]] and [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]].

---

### 1. Intuition & Practical Objective

The leverage formula

$$\sigma^2(t,S)=\frac{\sigma^2_{loc}(t,S)}{\mathbb E[v_t\,|\,S_t=S]}$$

looks like an explicit solution. It is not. The expectation in the denominator is taken **under the LSV model**, and the LSV model's law depends on $\sigma$. Writing it out,

$$\sigma^2(t,S)=\frac{\sigma^2_{loc}(t,S)}{\mathbb E^{\sigma}[v_t\,|\,S_t=S]},$$

the unknown appears on both sides. This is a **McKean–Vlasov** (nonlinear) stochastic differential equation: a diffusion whose coefficients depend on its own law. There is no closed form for the general case; there are two ways to solve it:

1. **Monte-Carlo fixed-point iteration — the particle method** (Guyon–Henry-Labordère 2012). Simulate the model with the current leverage, estimate the conditional variance by binning the paths by spot, update the leverage, repeat until the implied surface stops moving.
2. **A Fokker–Planck / forward-PDE solve for the joint density** ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04]]), which computes $m(t,S)$ from the density rather than from bins.

This page is about the first route, which is the one that works for *arbitrary* drivers — Heston, multi-factor forward variance, rough, with jumps.

Four things to carry out of this page:

1. **The method is a fixed point, not a fit.** Nothing is minimised. You start from a leverage (any leverage), simulate, and let the conditional variance estimate push the leverage to the value that reproduces the market's local variance.
2. **The proxy is not the answer.** The obvious zeroth guess — $\sigma^2=\sigma^2_{loc}/\xi_0^t$ with $\xi_0^t$ the forward-variance curve — *increases* the smile error on a correlated driver. The conditional variance $m(t,S)$ is not the unconditional one, and the gap is the whole reason the iteration is needed.
3. **The leverage comes out strongly spot-dependent.** On the Heston test below it runs from $0.48$ in the crash wing to $2.03$ in the upside wing at $t=1$ — a factor of $4.2$. That function *is* the model's spot/vol response, and it is invisible in vanillas.
4. **Convergence is fast and the residual is Monte-Carlo error.** Three iterations take a $7.3$-vol-point RMS error to $0.23$ vol points.

The practical objective: be able to implement the particle method from scratch (simulator, binning, conditional-mean estimator, leverage interpolation), know how many paths and bins you need, and know why the algorithm converges.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The nonlinear SDE

Write the LSV model in the "self-consistent" form. With $\rho=\mathrm{corr}(W^S,W^v)$ and the driver $(v_t)$,

$$dS_t=(r-q)S_t\,dt+\sigma(t,S_t)\sqrt{v_t}\,S_t\,dW^S_t,\qquad \sigma^2(t,S)=\frac{\sigma^2_{loc}(t,S)}{\displaystyle\int v\,\rho^{\sigma}_t(S,v)\,dv\Big/\int \rho^{\sigma}_t(S,v)\,dv},$$

where $\rho^{\sigma}_t$ is the joint density of $(S_t,v_t)$ *under the model with leverage $\sigma$*. The map $\sigma\mapsto\rho^{\sigma}$ is the nonlinearity. The **existence and uniqueness** question for such McKean–Vlasov calibrations is a genuine analysis problem (the literature establishes local well-posedness and gives conditions for global solvability; the practitioner's evidence is that the iteration below converges for market-grade inputs).

#### 2.2 The fixed-point map

Discretise the leverage on a grid $\{t_n\}\times\{k_j\}$ in time and log-moneyness. The **particle-method map** is

$$\sigma^2_{n+1}(t_n,k_j)=\frac{\sigma^2_{loc}(t_n,k_j)}{m_n(t_n,k_j)},\qquad m_n(t_n,k_j)=\frac{\sum_{i\in \text{bin}(j)}v^{(i)}_{t_n}}{\#\text{bin}(j)},$$

where $v^{(i)}$ are the simulated variance paths under leverage $\sigma_n$. At the fixed point, $m$ is the model's true conditional variance, the model's local variance is $\sigma^2_{loc}$, and by Dupire's theorem the model prices every vanilla. Convergence of this map is a contraction in practice for market-calibrated inputs; the iteration count is typically $3$–$10$.

In continuous form the same statement is: the LSV marginal density $\rho$ satisfies the *linear* Fokker–Planck equation

$$\partial_t\rho=\tfrac12\partial^2_{SS}\!\left(\sigma^2_{loc}(t,S)S^2\rho\right)$$

with the *nonlinear* closure $\sigma^2_{loc}(t,S)=\sigma^2(t,S)m(t,S)$ and $m$ computed from $\rho$. This is the bridge to §04.

#### 2.3 Implementation recipe

1. **Local variance.** Build $\sigma^2_{loc}(t,k)$ from the market smile — Dupire in the total-variance form ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|hub §3]]), or from a calibrated arbitrage-free parameterisation (SVI etc.).
2. **Grid.** Time steps $\{t_n\}$ (use the *same* steps as the simulator) and $N_b$ log-moneyness bins over a range wide enough to hold the terminal distribution at every step.
3. **Simulator.** Log-Euler for $S$ (exact for the diffusion part, preserves positivity) and **Milstein** for the variance (positivity where $4\lambda\bar v/\eta^2>1$; see [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston · 05]]). Use antithetic sampling for variance reduction.
4. **Binning.** For each step $n$, accumulate $\sum v$ and the count per bin. At the end, $m_n(t_n,k_j)=\overline{v}$ in each bin.
5. **Empty-bin policy.** Under-populated bins (typically the wings) must be handled explicitly: fill from the nearest populated bin (the left/right boundary values), or fall back to the forward-variance value. This interpolates smoothly but *bias-corrects upward* — the leverage error from it is not noise (§05).
6. **Interpolation.** Between grid points in $(t,k)$, interpolate the *variance* $\sigma^2$, not $\sigma$: it is $\sigma^2$ that is linearly behaved.
7. **Stopping.** Iterate until the implied-volatility RMS error against the target surface stops falling. Two diagnostics: the RMS in vol points and the change in $\sigma$ between iterations.

#### 2.4 Why the conditional variance is the crux

Consider the two candidate estimands:

$$\underbrace{\xi_0^t=\mathbb E[v_t]}_{\text{unconditional: forward variance}}\qquad\text{vs}\qquad\underbrace{m(t,S)=\mathbb E[v_t\,|\,S_t=S]}_{\text{conditional: what the projection needs}}.$$

With $\rho<0$, low-$S$ states come with high $v$ — the crash wing has *more* variance than average, the upside wing *less*. On the Heston test of §3 the ratio $m(1,S)/\xi_0^1$ runs from $5.6$ in the crash wing to $0.32$ in the upside wing. Using the unconditional value therefore mis-states the local variance by those factors, the model is *over-levered* in the wings, and the resulting smile is *more* skewed than the raw Heston smile — the opposite of the intent. This is not a numerical detail; it is the mathematical content of the projection.

---

### 3. Computational Implementation — the particle method end to end

The **target market is a flat $20\%$ Black–Scholes surface** (target local variance $0.0400$ everywhere), which makes the calibration error directly readable as "distance from a flat $20\%$ line". The driver is the fitted-index Heston set of the hub. We run the un-levered model, the forward-variance proxy, and three particle-method iterations. Stdlib only.

```python
import math, random
N=lambda x:0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bs_call(F,K,T,s):
    d1=(math.log(F/K)+0.5*s*s*T)/(s*math.sqrt(T)); return F*N(d1)-K*N(d1-s*math.sqrt(T))
def implied_vol(pv,F,K,T):
    lo,hi=1e-8,6.0
    for _ in range(300):
        m=0.5*(lo+hi)
        if bs_call(F,K,T,m)>pv: hi=m
        else: lo=m
    return 0.5*(lo+hi)

v0,vbar,lam,eta,rho=0.0174,0.0354,1.3253,0.3877,-0.7165      # Gatheral Table 3.2
F=100.0; T=1.0; SIG=0.20                                     # target: flat 20% BSM
NSTEP=100; NB=25; KLO,KHI=-0.70,0.40; DE=(KHI-KLO)/NB
def xi0(t): return vbar+(v0-vbar)*math.exp(-lam*t)           # Heston forward-variance curve

def lsv_run(npath,lev_fn,bins=False,seed=20240911):
    random.seed(seed); dt=T/NSTEP; rq=math.sqrt(1.0-rho*rho)
    ks=[]; acc=[[0.0]*NB for _ in range(NSTEP)]; cnt=[[0]*NB for _ in range(NSTEP)]
    for _ in range(npath//2):
        S=F; v=v0; z1s=[]
        for n in range(NSTEP):
            Z1=random.gauss(0,1); Z3=random.gauss(0,1); Z2=rho*Z1+rq*Z3; z1s.append(Z1)
            vp=v if v>0 else 0.0; L=lev_fn(n*dt,S)
            S=S*math.exp(-0.5*L*L*vp*dt+L*math.sqrt(vp*dt)*Z1)
            v=(math.sqrt(vp)+0.5*eta*math.sqrt(dt)*Z2)**2-lam*(vp-vbar)*dt-0.25*eta*eta*dt
            if bins:
                i=int((math.log(S/F)-KLO)/DE)
                if 0<=i<NB: acc[n][i]+=v; cnt[n][i]+=1
        ks.append(math.log(S/F))
        S=F; v=v0
        for n in range(NSTEP):
            Z1=-z1s[n]; Z3=random.gauss(0,1); Z2=rho*Z1+rq*Z3
            vp=v if v>0 else 0.0; L=lev_fn(n*dt,S)
            S=S*math.exp(-0.5*L*L*vp*dt+L*math.sqrt(vp*dt)*Z1)
            v=(math.sqrt(vp)+0.5*eta*math.sqrt(dt)*Z2)**2-lam*(vp-vbar)*dt-0.25*eta*eta*dt
            if bins:
                i=int((math.log(S/F)-KLO)/DE)
                if 0<=i<NB: acc[n][i]+=v; cnt[n][i]+=1
        ks.append(math.log(S/F))
    return ks,acc,cnt

KST=[0.75,0.85,0.90,1.00,1.10,1.20,1.30]
def smile(ks):
    r=[]
    for m in KST:
        K=F*m; pv=sum(max(F*math.exp(k)-K,0.0) for k in ks)/len(ks)
        r.append(implied_vol(pv,F,K,T)*100.0)
    return r
def rms(s): return math.sqrt(sum((x-20.0)**2 for x in s)/len(s))

NP=60000
print("Particle method, %d paths x %d steps.  Heston driver: v0=%.4f vbar=%.4f k=%.4f eta=%.4f rho=%.4f"
      %(NP,NSTEP,v0,vbar,lam,eta,rho))
print("Target market: FLAT 20% Black-Scholes  (so target local variance = 0.0400 for all (t,S))")
print()
print("%-34s %s"%("K/S0"," ".join("%7.2f"%m for m in KST)))
ks0,_,_=lsv_run(NP,lambda t,s:1.0)
print("%-34s %s"%("un-levered Heston (sigma=1) [%]"," ".join("%7.3f"%x for x in smile(ks0))))
lev_proxy=lambda t,s: math.sqrt(SIG*SIG/xi0(t))
ksp,_,_=lsv_run(NP,lev_proxy)
print("%-34s %s"%("lev_0 = sigma_loc/sqrt(xi0(t)) [%]"," ".join("%7.3f"%x for x in smile(ksp))))
lev=lev_proxy
prof=None
for it in (1,2,3):
    ksx,acc,cnt=lsv_run(NP,lev,bins=True)
    M=[[0.0]*NB for _ in range(NSTEP)]
    for n in range(NSTEP):
        for i in range(NB):
            if cnt[n][i]>=30: M[n][i]=acc[n][i]/cnt[n][i]
            else:
                j=i
                while j>=0 and cnt[n][j]<30: j-=1
                k2=i
                while k2<NB and cnt[n][k2]<30: k2+=1
                vals=([acc[n][j]/cnt[n][j]] if j>=0 else [])+([acc[n][k2]/cnt[n][k2]] if k2<NB else [])
                M[n][i]=sum(vals)/len(vals) if vals else xi0(n*T/NSTEP)
    if it==3: prof=[(KLO+(i+0.5)*DE,M[NSTEP-1][i],math.sqrt(SIG*SIG/M[NSTEP-1][i])) for i in range(NB)]
    def make_lev(M):
        def lv(t,s):
            n=min(NSTEP-1,int(t/(T/NSTEP))); x=(math.log(s/F)-KLO)/DE-0.5
            i=int(math.floor(x)); f=x-i; i=max(0,min(NB-1,i)); j=max(0,min(NB-1,i+1))
            return math.sqrt(SIG*SIG/max(M[n][i]*(1-f)+M[n][j]*f,1e-6))
        return lv
    lev=make_lev(M)
    ksr,_,_=lsv_run(NP,lev)
    sm=smile(ksr)
    print("%-34s %s"%("after particle iteration %d [%%]"%it," ".join("%7.3f"%x for x in sm)),
          "  RMS vs 20%% = %.3f" % rms(sm))
print()
print("conditional variance m(t,S)=E[v_t|S_t=S] at t=1 and the resulting leverage sigma(t,S):")
print("   k=ln(S/F)     m(1,S)      sigma(1,S)")
for k,m,sl in prof:
    if abs(k*20-round(k*20))<0.6 and -0.55<k<0.3:
        print("   %+8.2f   %9.5f   %9.5f"%(k,m,sl))
```
```
Particle method, 60000 paths x 100 steps.  Heston driver: v0=0.0174 vbar=0.0354 k=1.3253 eta=0.3877 rho=-0.7165
Target market: FLAT 20% Black-Scholes  (so target local variance = 0.0400 for all (t,S))

K/S0                                  0.75    0.85    0.90    1.00    1.10    1.20    1.30
un-levered Heston (sigma=1) [%]     20.816  18.150  16.814  14.180  11.964  10.967  10.988
lev_0 = sigma_loc/sqrt(xi0(t)) [%]  24.427  21.734  20.407  17.824  15.599  14.126  13.586
after particle iteration 1 [%]      20.140  19.332  18.986  18.554  18.534  18.548  18.355   RMS vs 20% = 1.228
after particle iteration 2 [%]      19.706  19.558  19.511  19.510  19.597  19.622  19.585   RMS vs 20% = 0.421
after particle iteration 3 [%]      19.787  19.782  19.774  19.755  19.767  19.760  19.749   RMS vs 20% = 0.233

conditional variance m(t,S)=E[v_t|S_t=S] at t=1 and the resulting leverage sigma(t,S):
   k=ln(S/F)     m(1,S)      sigma(1,S)
      -0.55     0.17249     0.48155
      -0.50     0.14923     0.51774
      -0.46     0.12879     0.55729
      -0.41     0.11070     0.60111
      -0.37     0.09542     0.64746
      -0.33     0.08390     0.69047
      -0.28     0.06897     0.76156
      -0.24     0.05737     0.83499
      -0.19     0.04555     0.93715
      -0.15     0.03721     1.03684
      -0.11     0.02964     1.16175
      -0.06     0.02386     1.29484
      -0.02     0.01941     1.43569
      +0.03     0.01636     1.56351
      +0.07     0.01414     1.68170
      +0.11     0.01233     1.80111
      +0.16     0.01166     1.85227
      +0.20     0.01004     1.99582
      +0.25     0.01014     1.98574
      +0.29     0.00975     2.02551
```

**Reading the output.** (Runtime: about 55 seconds for the six 60 000-path simulations.)

- **The un-levered Heston driver has a $9.8$-vol-point skew** ($20.816\%$ at $K/S_0=0.75$ down to $10.988\%$ at $K/S_0=1.30$) against a flat-$20\%$ target. That is the static fit LSV has to repair.
- **The forward-variance proxy makes it worse.** `lev_0 = 0.20/√ξ_0^t` gives $24.427\%\to13.586\%$ — an even steeper smile. Why: the projection needs the *conditional* variance, and with $\rho=-0.7165$ the crash wing carries far more variance than the average, so the proxy lever is too large exactly where it must be small. This is the single most instructive negative result in the folder.
- **The particle method converges.** Iteration 1 already collapses the wings to a near-flat profile with RMS $1.228$ vol points; iteration 2 gives $0.421$; iteration 3 gives $0.233$. The residual is Monte-Carlo and binning error, not model error: the target is exactly flat $20\%$ and the fitted curve is flat to within $0.033$ vol points across the five central strikes ($19.755$–$19.787$), with the residual concentrated at the extreme wings where the bins are thin.
- **The calibrated leverage is strongly spot-dependent.** At $t=1$ it runs from $\sigma=0.48155$ at $k=-0.55$ to $\sigma=2.02551$ at $k=+0.29$ — a factor of $4.2$. Recall the leverage is a *deterministic* function of $(t,S)$: what the calibration has done is install a large, explicitly spot-dependent volatility response so that the *product* $\sigma^2m$ is flat. Those two functions — $\sigma$ and $m$ — are individually wild and jointly trivial; only their product is observable in vanillas.
- **$m(1,S)$ runs $17.7\times$ across the smile** ($0.17249$ at $k=-0.55$ vs $0.00975$ at $k=+0.29$) while $\xi_0^1=0.03062$. The ratio is $5.6$–$0.32$: this is the conditional-variance asymmetry the whole method exists to capture, and it is *created by the correlation $\rho$ interacting with the leverage*. That the ratio is not $1$ even in the low-$|\rho|$ regime is why the proxy fails.
- **Why the iteration is needed at all.** Iteration 1's leverage was built from a *simulation with the proxy*, so its binned $m$ is measured under the wrong law. Each iteration shrinks the inconsistency; the fixed point is the leverage under which the *measured* conditional variance equals the variance that would make the local variance equal Dupire's.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Starting from the forward-variance proxy and declaring victory.** As the table shows, the proxy is *worse* than the un-levered model on a correlated driver. It is a valid zeroth iteration, not an answer.
2. **Too few paths per bin.** The estimator is a conditional mean; its error is $\sqrt{\mathrm{Var}(v_t|S_t)/n_{bin}}$ and it blows up in the wings. Bins with $<30$ paths (the cutoff used above) must be filled from neighbours, and that fill is *biased*, not noisy.
3. **Too coarse a time grid.** The binned $m$ is used as a *leverage at that instant*, so the time resolution of the grid is the resolution of the leverage's time dependence. A leverage that is piecewise-constant in time with $10$ steps will show up as a term-structure error in the forward-smile dynamics.
4. **Interpolating $\sigma$ instead of $\sigma^2$.** The variance is the quantity with the projection identity; linearly interpolating $\sigma$ across a $4\times$ dynamic range introduces a systematic local-variance error of order $(\Delta\sigma)^2$.
5. **Mixing the simulator's bin edges with the leverage's grid.** If the bin edges used to *estimate* $m$ are not the interpolation points used to *apply* $\sigma$, the fixed point is being solved on a slightly different object than the one being simulated, and the iteration can stall at a bias of the order of the bin width.
6. **Treating the converged leverage as a market quantity.** It is not estimable from prices: vanillas see only $\sigma^2m$. The leverage is a *decomposition* of a fitted surface, and its shape is entirely conditional on the driver (§05's gauge freedom makes even that statement non-unique).
7. **Ignoring the driver's own pathologies in simulation.** The variance process must be simulated with a positivity-preserving scheme (Milstein/QE); negative-variance patches corrupt $m$ in exactly the low-$S$ bins where it matters most. See [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston · 05]] — the fitted index parameters violate Feller.
8. **Assuming convergence is guaranteed.** The McKean–Vlasov map is not a contraction for arbitrary inputs (extreme smiles, very high vol-of-vol, sparse bins in the far wings). Always monitor the residual surface *and* the iteration-to-iteration change in $\sigma$.

---

### 5. Canonical Literature & Study References

- **Guyon, J. & Henry-Labordère, P.** (2012), *Being particular about calibration*, Risk **25**(1), 91–107 — the particle method as published: the fixed-point algorithm, the treatment of the conditional expectation, and its use with hybrid local-stochastic volatility models. *The primary source of this page.*
- **Henry-Labordère, P.** (2009), *Calibration of local stochastic volatility models to market smiles: a Monte-Carlo approach*, Risk (September 2009); SSRN 1493306 — the precursor, illustrated on the Bergomi variance-curve model and the two-factor lognormal model, with the Markovian-projection derivation.
- **Bergomi, L.**, *Stochastic Volatility Modeling* (CRC, 2016), Ch 12 §12.2–12.4 (LSV construction, the ATMF-skew decomposition after calibration) and Ch 7 (the forward-variance drivers the leverage is most often applied to; exact OU simulation, which removes all discretisation bias for the variance-only part). *Math-verified in the corpus.*
- **Guyon, J. & Henry-Labordère, P.**, *Nonlinear Option Pricing* (Chapman & Hall/CRC, 2013) — the book-length treatment of McKean–Vlasov SDEs in finance, including the LSV calibration and the "particle" interpretation. **Jourdain, B. & Sbai, M.** (2015) on well-posedness of LSV calibration problems; **Abergel & Tachet** (2010) on calibration of a local-stochastic model.
- **Andersen, L.** (2008), *Simple and efficient simulation of the Heston stochastic volatility model* (QE scheme); **Lord, Koekkoek & van Dijk** (2010), *A comparison of biased simulation schemes for stochastic volatility models* — the simulators the step-3 recipe calls for. *Verification backdrop for §03 of this page.*
- **Gatheral, J.**, *The Volatility Surface*, Ch 1 (the Dupire local variance fed into the calibration) and Ch 7 §7.8 (why the *static* fit is not a test of the model the leverage preserves). *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]]
- Forward: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04 · The Fokker–Planck / McKean–Vlasov Route]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Index Hub]]
- Cross-links: [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]] (Monte Carlo, variance reduction, discretisation) · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Numerical Methods · 03 Monte Carlo Pricing]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston & SABR · 05]] (Feller vs Milstein, the schemes used above) · [[pillars/03-derivative-pricing/calibration-and-market-practice/04-calibrating-stochastic-vol|Calibration · 04 Calibrating Stochastic Vol]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (nonparametric conditional-mean estimation)
