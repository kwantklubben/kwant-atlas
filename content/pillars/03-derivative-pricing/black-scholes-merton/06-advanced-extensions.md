---
title: "06 — Advanced Extensions: Local/Stochastic Vol, Jumps, Numerical Methods"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - stochastic-volatility
  - jump-diffusion
  - american-options
  - numerical-methods
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · Pricing Formulas]] and [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Every real-market defect of BSM (the smile, jumps, fat tails, early exercise) motivates an *extension*. This page is the **launchpad**: it shows the two immediate extensions that stay inside the BSM family — **American early exercise** (still lognormal, still one asset) and **Merton jump-diffusion** (keeps a closed form as a Poisson mixture of BS) — and then hands off to the dedicated topic-folder pages for stochastic/local volatility and numerical methods.

> **Why these first?** American options are the *same* PDE with a free boundary, so they are the closest extension. Jump-diffusion is the minimal *incomplete-market* extension and still prices in closed form — the perfect bridge to why one-factor models fail. Everything farther (Heston, SABR, FDM, MC) is linked from here.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 American options & the early-exercise boundary (Haug Ch 3; Björk §7.8)

An American option adds the right to exercise *before* $T$, giving the free-boundary (variational) problem
$$
V\ge\max(\text{intrinsic},0),\qquad \frac{\partial V}{\partial t}+rS\frac{\partial V}{\partial S}+\tfrac12\sigma^2S^2\frac{\partial^2 V}{\partial S^2}-rV\le0,
$$
with equality where it is optimal to *continue*. The optimal exercise boundary $S^*(t)$ solves a smooth-pasting condition. Key facts:
- **American call, no dividends:** never optimal to exercise early, so $C^{\text{Am}}=c^{\text{BSM}}$ (Haug §1.2).
- **American put / dividend-paying call:** early exercise *is* optimal; no closed form — solve numerically (binomial tree, finite-difference, or analytic approximations like Barone–Adesi–Whaley or Bjerksund–Stensland, all in Haug Ch 3).

#### 2.2 Merton (1976) jump-diffusion — the minimal incomplete-market extension

Under $\mathbb{Q}$,
$$
dS_t/S_t=(r-\lambda\kappa)\,dt+\sigma\,dW_t+(J-1)\,dN_t,
$$
where $N$ is a Poisson process with intensity $\lambda$, $J$ the multiplicative jump size ($\ln J\sim N(\mu_J,\sigma_J^2)$), and $\kappa=\mathbb{E}[J-1]=e^{\mu_J+\frac12\sigma_J^2}-1$ the compensator that keeps $e^{-rt}S_t$ a martingale. Because a Poisson-mixture of lognormals is lognormal, the call prices in **closed form** as a Poisson-weighted average of BSM calls at inflated vol:

$$
C_{\text{Merton}}=\sum_{n=0}^{\infty}\frac{e^{-\lambda' T}(\lambda' T)^n}{n!}\;c_{\text{BSM}}\!\left(S,X,T,r,\sigma_n\right),\qquad \sigma_n=\sqrt{\sigma^2+\frac{n\sigma_J^2}{T}},\qquad \lambda'=\lambda(1+\kappa).
$$

*(Glasserman Ch 3.5, eq. 3.79–3.81, gives the pathwise simulation form.)*

#### 2.3 Beyond: toward local & stochastic volatility (bridges)

- **Local volatility (Dupire):** replace constant $\sigma$ with a deterministic function $\sigma(S,t)$ *calibrated to the entire smile*; the model stays complete (one driver). → [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]].
- **Stochastic volatility (Heston/SABR):** add a second driver to variance, breaking completeness; characteristic-function/Fourier pricing. → [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]].
- **Numerical methods:** finite-difference schemes (Duffy) for the PDE, Monte Carlo (Glasserman) for path-dependent exotics.

---

### 3. Computational Implementation — two extensions, both stdlib

**A. American put via CRR tree** (Haug §4.2; Hull Ch 13) — the early-exercise premium is the gap vs the European value.

```python
import math

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bsm_put(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1 - sig*math.sqrt(T)
    return X*math.exp(-r*T)*N(-d2) - S*N(-d1)

def american_put_crr(S, X, T, r, sig, n):
    dt = T/n; u = math.exp(sig*math.sqrt(dt)); d = 1.0/u
    p  = (math.exp(r*dt) - d)/(u - d)
    val = [max(X - S*u**(n-i)*d**i, 0.0) for i in range(n+1)]
    for j in range(n-1, -1, -1):
        val = [max(math.exp(-r*dt)*(p*val[i]+(1-p)*val[i+1]), X - S*u**(j-i)*d**i)
               for i in range(j+1)]
    return val[0]

S, X, T, r, sig = 100.0, 95.0, 0.5, 0.08, 0.30
euro, amer = bsm_put(S,X,T,r,sig), american_put_crr(S,X,T,r,sig,1000)
print(f"European put={euro:.4f}   American (CRR n=1000)={amer:.4f}")
print(f"early-exercise premium = {amer-euro:.4f}")
```
```
European put=4.4494   American (CRR n=1000)=4.6921
early-exercise premium = 0.2427
```
*(Haug §4.2 verifies the CRR American put $4.692$ against the same inputs.)*

**B. Merton jump-diffusion vs pure BSM** — a Poisson mixture of lognormals priced by Monte Carlo. Constant-vol BSM (no jumps) under-prices when jumps are present.

```python
import math, random

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bsm_call(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1 - sig*math.sqrt(T)
    return S*N(d1) - X*math.exp(-r*T)*N(d2)

def poisson(lam):
    # Knuth: multiply uniforms until their product falls below exp(-lam)
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        k += 1; p *= random.random()
        if p <= L: break
    return k - 1

def merton_jump_call(S, X, T, r, sig, lam, muJ, sigJ, npaths):
    kappa = math.exp(muJ + 0.5*sigJ**2) - 1
    tot = 0.0
    for _ in range(npaths):
        W  = random.gauss(0, 1)
        nJ = poisson(lam*T)                                     # N_jumps ~ Poisson(lam*T)
        J  = sum(random.gauss(muJ, sigJ) for _ in range(nJ))     # sum of the jumps
        ST = S*math.exp((r - 0.5*sig**2 - lam*kappa)*T + sig*math.sqrt(T)*W + J)
        tot += max(ST - X, 0.0)
    return math.exp(-r*T) * tot / npaths

def merton_jump_call_exact(S, X, T, r, sig, lam, muJ, sigJ, nterms=100):
    # Poisson mixture of lognormals -- closed form, no MC (discount at r, drift shifts)
    kappa = math.exp(muJ + 0.5*sigJ**2) - 1
    def payoff(m, v):                                            # E[(S e^Y - X)^+], Y~N(m,v)
        d1 = (m + v - math.log(X/S))/math.sqrt(v); d2 = (m - math.log(X/S))/math.sqrt(v)
        return S*math.exp(m + 0.5*v)*N(d1) - X*N(d2)
    tot = 0.0
    for n in range(nterms):
        w = math.exp(-lam*T) * (lam*T)**n / math.factorial(n)     # P(N_jumps = n)
        m = (r - 0.5*sig**2 - lam*kappa)*T + n*muJ
        v = sig**2*T + n*sigJ**2
        tot += w * payoff(m, v)
    return math.exp(-r*T) * tot

random.seed(42)
S, X, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.20
bs  = bsm_call(S, X, T, r, sig)
mj  = merton_jump_call(S, X, T, r, sig, 2.0, -0.10, 0.10, 200000)
mje = merton_jump_call_exact(S, X, T, r, sig, 2.0, -0.10, 0.10)
print(f"pure BSM call (sigma=20%)              = {bs:.4f}")
print(f"Merton jump-diffusion MC (lam=2)       = {mj:.4f}")
print(f"Merton jump-diffusion exact (mixture)  = {mje:.4f}")
```
```
pure BSM call (sigma=20%)              = 10.4506
Merton jump-diffusion MC (lam=2)       = 13.3015
Merton jump-diffusion exact (mixture)  = 13.3506
```
The jump model prices the call materially higher ($13.35$ vs $10.45$): the fat left tail makes the payoff right-skewed, and constant-vol BSM cannot represent that tail risk — exactly the structural failure of [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **American pricing is a free-boundary problem, not a closed form.** Applying the European formula to an American *put* understates value by the early-exercise premium ($0.24$ here). Use the tree/analytic approximations (Haug Ch 3).
2. **Jump-diffusion markets are incomplete.** One stock cannot hedge the jump source of randomness, so prices are *not* unique — the Merton price is one (risk-neutral) choice, not a no-arbitrage necessity. This is the theoretical cliff-edge beyond BSM.
3. **Numerical methods carry their own errors.** Trees have discretization (oscillating) error; MC has $O(n^{-1/2})$ error and needs variance reduction (Glasserman Ch 4); FDM has stability/consistency constraints (Duffy Ch 3). "More steps" is not automatically better — see the failure pages of the linked topics.
4. **Stochastic-vol parameters are hard to identify.** Heston/SABR free parameters trade off against each other and are notoriously hard to calibrate stably (see [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]).

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, Ch 3 (American: BAW, Bjerksund–Stensland 1993/2002, perpetual options) and Ch 7 (trees). *All numerically verified in the corpus.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 13 (binomial, American via backward induction), Ch 20/21 (smiles, numerical procedures).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 1 (MC principles), Ch 3 §3.5 (jump-diffusion simulation, eq. 3.79–3.81). *Math-verified.*
- **Duffy**, *Finite Difference Methods in Financial Engineering* (FDM for the BSM PDE). *Corpus available.*
- **Björk**, *Arbitrage Theory in Continuous Time*, §7.8 (American options introduction).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]]
- Forward topic-folder pages: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate Models]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
