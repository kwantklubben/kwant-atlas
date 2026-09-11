---
title: "05 — Failure Modes & Practice: The Singular Kernel, Spurious Long Memory, Calibration & Model Risk"
tags:
  - pillar-derivative-pricing
  - rough-volatility-and-fractional-models
  - calibration
  - discretisation
  - long-memory
  - model-risk
  - monte-carlo
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/04-hurst-estimation-and-simulation|04 · Hurst Estimation & Simulation]] and [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/02-the-rough-bergomi-model|02 · The rBergomi Model]].

---

### 1. Intuition & Practical Objective

Everything up to here was mathematics; this page is about what actually goes wrong with rough-vol models on a desk, and why. Four symptom classes, each traceable to a first principle:

1. **The simulation breaks.** The Volterra kernel $(t-u)^{H-\frac12}$ is singular at $u\to t$; naive Euler diverges. The hybrid scheme exists to fix exactly this.
2. **The empirics are misread.** H<1/2 is *anti-persistence*, not long memory; classical long-memory estimators certify long memory on rough data that has none (GJR §4). This misdiagnosis has historically driven the wrong model choice.
3. **Calibration is ill-posed and non-Markovian.** Three parameters but no characteristic function and no PDE; pricing is Monte Carlo or a Markovian lift, and $H$ and $\eta$ enter the short-time skew only through $\eta\sqrt{2H}$.
4. **Model risk is concentrated at the short end.** The whole reason to adopt rough vol is the short-dated skew; but the short end is also where estimation error is largest and where the Markovian-vs-rough gap is biggest.

The practical objective: be able to state exactly *why* naive simulation fails and how the hybrid scheme fixes it; know that "rough" and "long memory" are opposites; size the Markovian-vs-rough skew gap; and know the checks (martingale, positivity) that police any implementation.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The singular kernel and the hybrid fix

The driver $W^\alpha_t=\sqrt{2\alpha+1}\int_0^t(t-u)^\alpha dW_u$ with $\alpha=H-\tfrac12\in(-\tfrac12,0)$ has a kernel that diverges as $u\to t^-$. A naive Euler discretisation $\sqrt{2\alpha+1}\sum_j(t_i-u_j)^\alpha\Delta W_j$ is **not** a consistent estimator of the Itô integral: the singular proximal cell contributes a term whose discretisation error does not vanish as the grid refines unless handled separately. The hybrid scheme (BLP 2017) splits off the proximal integral and treats it as a Gaussian of variance $\Delta^{2\alpha+1}/(2\alpha+1)$ — which is what makes $\mathrm{Var}[W^\alpha_t]\to t^{2H}$ (verified in [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/04-hurst-estimation-and-simulation|04 · Simulation]]).

#### 2.2 Rough is not long memory (GJR §4)

For $H<\tfrac12$, fBm increments are *anti-correlated* and the autocovariance is **negative at every nonzero lag** ($\rho_1=\tfrac12(2^{2H}-2)<0$). Classical long memory means $H>\tfrac12$ (positive, non-integrable autocovariance). GJR's §4 is the sharp empirical statement: run a long-memory test (R/S, fractional differencing with $d=0.4$) on a well-calibrated RFSV path and on real SPX vol — **both return "long memory"**, with matching statistics. The apparent long memory of volatility is **spurious**, an artefact of anti-persistence at short scales. Roughness and long memory are not only different — they are *opposite* regimes of H.

#### 2.3 Why Markovian models are structurally wrong at the short end

For a one-factor OU (Heston-like) vol-of-vol kernel $g(u-t)=e^{-\kappa(u-t)}$, the Bergomi–Guyon skew functional gives

$$
S_T^{OU}=\frac{1}{2\hat\sigma_T^3T^2}C^{x\xi},\qquad C^{x\xi}\propto\int_0^T\int_t^T e^{-\kappa(u-t)}dudt=\frac{\kappa T-1+e^{-\kappa T}}{\kappa^2},
$$

so $S_T^{OU}\to\frac12$ (bounded) as $T\to0$. For the rough kernel $(u-t)^{H-\frac12}$, $S_T\propto T^{H-\frac12}\to\infty$. **This is the structural failure**: no finite-factor Markovian model can produce an ATMF skew that blows up at short maturity, yet the SPX data demand $\psi(T)\propto T^{-0.44}$. The comparison is quantified in §3.

#### 2.4 The short-time skew and the H/η identification

From [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/02-the-rough-bergomi-model|02]]:

$$
\psi(T)=\frac{\rho\eta\sqrt{2H}}{2(H+\tfrac12)(H+\tfrac32)}T^{H-\frac12}.
$$

The parameters enter as **products**: $\rho\eta\sqrt{2H}$ (level) and $H-\tfrac12$ (exponent). From one short-time skew you can read the *exponent* $H$ (the slope) but only the *product* $\rho\eta\sqrt{2H}$ (the level) — you cannot separate $\eta$ from $\rho$ without the wings or additional maturities, and $\rho$ must come from the spot/vol correlation. Three parameters, but the short-time vanillas see them as ~2 independent directions.

---

### 3. Computational Implementation — MC pricing, the Markovian cap, and the exponent

We (i) run a full Monte Carlo of the rBergomi model and extract the ATMF skew at several maturities to confirm the power-law exponent empirically; (ii) compare the rough-kernel skew to the Markovian OU skew to size the short-end gap. Stdlib only.

```python
import math, random
def hybrid_rbergomi(n, T, alpha, seed):
    random.seed(seed); sq=2.0*alpha+1.0; dt=T/n
    b=[0.0]*(n+1)
    for k in range(1,n+1):
        b[k]=((k**(alpha+1)-(k-1)**(alpha+1))/(alpha+1))**(1.0/alpha)
    bk=[0.0]*(n+1)
    for k in range(1,n+1): bk[k]=(b[k]*dt)**alpha
    dW1=[random.gauss(0,1)*math.sqrt(dt) for _ in range(n)]
    W1=[0.0]
    for x in dW1: W1.append(W1[-1]+x)
    W2=[0.0]
    for _ in range(n): W2.append(W2[-1]+random.gauss(0,1)*math.sqrt(dt))
    Wa=[0.0]*(n+1); prox_sd=dt**(alpha+0.5)/math.sqrt(sq)
    for i in range(1,n+1):
        ff=sum(bk[k]*dW1[i-k] for k in range(2,i+1))
        Wa[i]=math.sqrt(sq)*(prox_sd*random.gauss(0,1)+ff)
    return W1, W2, Wa
def mc_atmf_skew(H, eta, rho, xi0, N=10000):
    alpha=H-0.5; out={}
    for T in (0.10, 0.50, 1.0):
        n=120; ks=[-0.15,-0.10,-0.05,0.0,0.05,0.10,0.15]
        acc={k:0.0 for k in ks}
        for p in range(N):
            W1,W2,Wa=hybrid_rbergomi(n,T,alpha,1000+p); S=1.0
            for i in range(n):
                V=xi0*math.exp(eta*Wa[i+1]-0.5*eta*eta*((i+1)*T/n)**(2*H))
                dZ=rho*(W1[i+1]-W1[i])+math.sqrt(1-rho*rho)*(W2[i+1]-W2[i])
                S*=(1.0+math.sqrt(V)*dZ)
            for k in ks: acc[k]+=max(S-math.exp(k),0.0)/N
        def bs_call(sig,k):
            sT=sig*math.sqrt(T); d1=-k/sT+0.5*sT; d2=-k/sT-0.5*sT
            def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
            return N(d1)-math.exp(k)*N(d2)
        iv=[]
        for k in ks:
            price=acc[k]; lo,hi=1e-4,3.0
            for _ in range(60):
                m=0.5*(lo+hi)
                if bs_call(m,k)>price: hi=m
                else: lo=m
            iv.append(0.5*(lo+hi))
        i0=ks.index(0.0); out[T]=(iv[i0+1]-iv[i0-1])/(ks[i0+1]-ks[i0-1])
    return out
print("(i) rBergomi MC ATMF skew S_T (H=0.14, eta=1.9, rho=-0.9, 10000 paths)")
sk=mc_atmf_skew(0.14,1.9,-0.9,0.04)
for T in sorted(sk): print(f"    T={T:5.2f}  S_T={sk[T]:+.4f}")
lx=[math.log(t) for t in sk]; ly=[math.log(abs(sk[t])) for t in sk]
xb=sum(lx)/len(lx); yb=sum(ly)/len(ly)
slope=sum((lx[i]-xb)*(ly[i]-yb) for i in range(len(lx)))/sum((lx[i]-xb)**2 for i in range(len(lx)))
print(f"    OLS slope of log|S_T| vs log T = {slope:.3f}   (theory H-1/2 = -0.360)")

print("\n(ii) why Markovian models fail: skew functional S_T as T->0")
def skew_rough(H,T): return T**(H+1.5)/((H+0.5)*(H+1.5))/(T*T)
def skew_ou(k,T): return (k*T-1.0+math.exp(-k*T))/(k*k)/(T*T)
print(f"    {'T':>7} {'rough S_T':>10} {'OU S_T':>10}")
for T in (1.0, 0.1, 0.01, 0.001):
    print(f"    {T:7.4f} {skew_rough(0.14,T):10.4f} {skew_ou(5.0,T):10.4f}")
```
```
(i) rBergomi MC ATMF skew S_T (H=0.14, eta=1.9, rho=-0.9, 10000 paths)
    T= 0.10  S_T=-0.8021
    T= 0.50  S_T=-0.4304
    T= 1.00  S_T=-0.3240
    OLS slope of log|S_T| vs log T = -0.392   (theory H-1/2 = -0.360)

(ii) why Markovian models fail: skew functional S_T as T->0
          T  rough S_T     OU S_T
     1.0000     0.9527     0.1603
     0.1000     2.1826     0.4261
     0.0100     5.0001     0.4918
     0.0010    11.4545     0.4992
```

**What the output establishes.**

- **(i) The full MC pricing confirms the power-law skew.** Running the actual rBergomi model (hybrid scheme for the vol driver + correlated spot) and inverting implied vol gives a **negative** ATMF skew ($\rho<0$) whose log-log slope is $-0.392$ vs the theory $-0.360$ — agreement within Monte Carlo error (10 000 paths). The power-law short-dated skew is not an artefact of the Bergomi–Guyon expansion; it is present in the raw simulated prices.
- **(ii) The Markovian gap is unbounded as T→0.** The rough-kernel skew $S_T$ grows without bound ($0.95\to11.45$ as $T:1\to0.001$) while the OU (Heston-like) skew **caps** at $0.4992$ (the $\frac12$ limit of §2.3). No finite-factor Markovian model can produce the SPX $\tau^{-0.44}$ short-end behaviour — this is the quantitative case for rough vol.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using naive Euler on the singular kernel.** Divergent, biased, no Brownian-limit consistency. Use the hybrid scheme (or the exact Hosking for fBm-increment tasks). Check $\mathrm{Var}[W^\alpha_t]=t^{2H}$ and $\mathbb E[v_t]=\xi_0(t)$ after any scheme change.
2. **Reading "rough" as "long memory".** They are opposite regimes of H. Long-memory estimators (R/S, fractional differencing) return long memory on *anti-persistent* rough data — GJR §4 shows the same "verdict" on real SPX and on a simulated RFSV path. Diagnose with the variogram exponent $2H$, not R/S.
3. **Estimating H from too short a sample.** The variogram slope is biased on short series (see §04's downward bias at 400×150); GJR use thousands of days across 21 indices. A weekly H is noise.
4. **Trying to separate H from η on a single skew slice.** The short-time skew sees $\eta\sqrt{2H}$ and the exponent $H-\tfrac12$; $\eta$ and $\rho$ are not individually pinned by vanillas. Use the variogram of log-vol (for H) + the wing/multi-maturity data (for η, ρ).
5. **Believing the Bergomi–Guyon expansion globally.** $\psi(T)\propto T^{H-\frac12}$ is the order-1 ATMF slope; the truncated density can misbehave at extreme strikes (Lee's moment formula governs the wings). Use it near the money and for its *coefficients*, like any SV expansion.
6. **Ignoring the non-Markovian pricing cost.** No characteristic function, no PDE — pricing is MC (slow, needs variance reduction; see McCrickerd–Pakkanen) or a Markovian lift (rough Heston, El Euch–Rosenbaum). The adoption decision must price in this computational tax.

---

### 5. Canonical Literature & Study References

- **Gatheral, Jaisson & Rosenbaum (2018)**, *Volatility is rough*, Quantitative Finance 18(6), 933–949 — §4 (**spurious long memory**: R/S, fractional differencing $d=0.4$, matching data-vs-model statistics), §3.4 (scale invariance). *The failure-mode ground truth.*
- **Bennedsen, Lunde & Pakkanen (2017)**, *Hybrid scheme for Brownian semistationary processes*, Finance and Stochastics 21(4), 931–965 — why naive discretisation of the singular kernel fails, and the convergent fix.
- **Bayer, Friz & Gatheral (2016)**, *Pricing under rough volatility*, Quantitative Finance 16(6), 887–904 — the rBergomi model and SPX calibration.
- **Bergomi (2016)**, *Stochastic Volatility Modeling*, ch 8 (Bergomi–Guyon expansion and its validity) — the framework behind §2.3–2.4; ch 3 §3.1.7 (vanillas do not pin forward skew — model risk).
- **McCrickerd & Pakkanen (2018)**, *Turbocharging Monte Carlo pricing for the rough Bergomi model* — variance-reduced MC for rBergomi calibration.
- **Fukasawa (2017)**, *Short-time at-the-money skew and rough fractional volatility* — the rigorous skew asymptotics behind §2.4.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/04-hurst-estimation-and-simulation|04 · Hurst Estimation & Simulation]] · [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/02-the-rough-bergomi-model|02 · The rBergomi Model]]
- Forward: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/index|Index Hub]]
- Cross-links: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston/SABR · 05 Failure Modes]] (Feller, discretisation, model risk — the Markovian analogue) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Quantitative Risk (VaR/ES)]] (fat tails) · [[foundations/numerical-methods/03-monte-carlo|Foundations · Monte Carlo]] (variance reduction for rBergomi pricing)
