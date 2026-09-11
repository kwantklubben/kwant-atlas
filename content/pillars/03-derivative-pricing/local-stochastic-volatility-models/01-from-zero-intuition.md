---
title: "01 — Local-Stochastic Volatility from Zero: One Scale Factor Fits the Smile, and It Costs You Nothing in Dynamics"
tags:
  - pillar-derivative-pricing
  - local-stochastic-volatility-models
  - intuition
  - local-volatility
  - stochastic-volatility
  - leverage-function
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (or none — this page is written to stand alone).

---

### 1. Intuition & Practical Objective

Two models, two opposite failures, one fix.

- **Local volatility** (Dupire, [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|VS · 02 Implied vs Local Vol]]) has a *deterministic* volatility function $\sigma_{loc}(t,S)$ and it fits **every** vanilla price in the market, exactly, by construction. Its failure is dynamical: volatility is a deterministic function of the spot, so there is nothing left to be random. It gets forward-starting options, cliquets and the smile's own motion wrong — famously, it produces a *flatter* forward smile than the market.
- **Stochastic volatility** ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr|Heston & SABR]]) has a *random* variance $v_t$ and gets the dynamics right — vol-of-vol, skew stickiness, forward skew. Its failure is static: four parameters cannot bend to an arbitrary market smile, and its ATM level, skew scaling and vol-of-vol term structure are all hard-wired.

**Local-stochastic volatility** is the observation that these two failures are complementary and can be fixed simultaneously with one object:

$$
dS_t=(r-q)S_t\,dt+\underbrace{\sigma(t,S_t)}_{\text{leverage function}}\sqrt{v_t}\,S_t\,dW^S_t,\qquad dv_t=\text{(your favourite SV driver)}.
$$

The stochastic factor $\sqrt{v_t}$ supplies the **dynamics**. The deterministic multiplier $\sigma(t,S)$ supplies the **level and shape**. You choose $\sigma$ so the model reproduces the market's implied surface; you choose the SV driver so the *unobserved* dynamics — forward skew, skew stickiness, vol-of-vol term structure — look like the market's.

Three "aha"s:

1. **One added function, not added randomness.** The leverage $\sigma(t,S)$ is deterministic. It adds **no** new source of randomness, **no** new state variable, and **no** new hedging instrument — the model still has the same two Brownian motions as the SV driver. What it adds is a *free rescaling of volatility at every point in the $(t,S)$ plane*.
2. **The rescaling has a unique correct value.** You cannot fit $\sigma$ however you like: the model must match the market's one-dimensional marginals at every date, and the local variance that generates a given marginal is Dupire's. So $\sigma(t,S)^2$ times the model's *conditional* expected variance must equal the Dupire local variance:
$$
\sigma^2(t,S)\,\mathbb E[v_t\,|\,S_t=S]=\sigma^2_{loc}(t,S).
$$
   Vanillas pin only the **product**. The split between the leverage and the conditional variance is decided by the SV driver — which is exactly the point: the driver, not the smile, controls the dynamics.
3. **What you get for free is scale, not shape.** Because $\sigma$ is a single *scalar field*, it can shift the level at each point and re-tilt the smile through its spot-dependence; it cannot add a second vol-of-vol or a second time scale. That is why after LSV is in place, the frontier moves on to *which driver* (forward-variance, rough, jumps) — the leverage is settled mathematics.

The practical objective: know what LSV is *for* (vanilla-exact statics with chosen dynamics), know the one equation that defines it, and know that "calibrating the leverage" means solving a fixed point — not running a least-squares fit.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The two failures, in one formula each

Let $\sigma_{loc}(t,S)$ be Dupire's local volatility and $\xi_0^t=\mathbb E[v_t]$ the forward-variance curve of a stochastic-volatility model.

| model | static fit | its dynamics |
|---|---|---|
| local vol | exact, by construction | deterministic: $\mathrm{Var}[\sigma_{loc}(t,S_t)]=0$; forward skew decays too fast |
| stochastic vol | only within a rigid 4-parameter family | non-trivial: forward skew, SSR, vol-of-vol term structure |
| **LSV** | **exact, by construction** | **inherited from the SV driver** |

The LSV trick is to keep the SV driver's *correlation structure* while replacing the *level* by the local-vol level. In one line: the LSV instantaneous variance is $\sigma^2(t,S_t)v_t$ instead of $v_t$.

#### 2.2 The defining equation, derived in two lines

Take the LSV spot process. Its Markovian projection ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]]) has diffusion coefficient equal to the conditional second moment of the instantaneous volatility,

$$
\bar\alpha^2(t,y)=\mathbb E\!\left[\alpha_t^2\,\middle|\,S_t=y\right]=\mathbb E\!\left[\sigma(t,S_t)^2v_t\,\middle|\,S_t=y\right]=\sigma(t,y)^2\,\mathbb E\!\left[v_t\,\middle|\,S_t=y\right].
$$

For the LSV model to reproduce the market's marginals, this projected diffusion must be the local-volatility model of the market, whose coefficient is $\sigma^2_{loc}(t,y)$ by Dupire's theorem. Hence:

$$
\boxed{\;\sigma^2(t,S)=\frac{\sigma^2_{loc}(t,S)}{m(t,S)},\qquad m(t,S):=\mathbb E[v_t\,|\,S_t=S]\;}
$$

This is the **leverage function**. Note what it does *not* contain: the leverage does not appear in the spot measure change, there is no free parameter, and it is not an optimisation output.

#### 2.3 Why the leverage is a *scale*, and what its spot-dependence does

Write the LSV instantaneous variance as

$$
\underbrace{\sigma^2(t,S)}_{\text{you choose}}\cdot\underbrace{m(t,S)}_{\text{from the driver}}=\sigma^2_{loc}(t,S).
$$

- **Flat in $S$ (as far as vanillas can see):** the *product* is the local variance. Changing how much of it comes from $\sigma$ and how much from $m$ changes nothing observable in vanillas.
- **Spot-dependent (as far as exotics can see):** everything. If $\sigma$ is large where $S$ is low, the model's volatility *responds* to spot moves — a spot/vol correlation that is on top of the driver's own $\rho$. The hedge ratios and the forward smile both move.

So the leverage is the dial that transfers volatility response from the (random, path-dependent) driver onto the (deterministic, spot-dependent) function. Getting that split right — by fixing the driver and solving the fixed point — is the whole calibration.

#### 2.4 The limits you should always sanity-check against

- **Vol-of-vol $\to0$ (deterministic driver).** Then $v_t$ is a deterministic function of time, $m(t,S)=\xi_0^t$ is *known*, and $\sigma(t)=\sigma_{loc}(t)/\sqrt{\xi_0^t}$: the model *is* local volatility. LSV contains LV.
- **Target $=$ the driver's own smile.** Then $m(t,S)=\sigma^2_{loc}(t,S)$ by definition and $\sigma\equiv1$: nothing to bend. LSV contains SV.
- **$\rho=0$ and a frozen driver.** $m(t,S)$ is a symmetric function of $\log(S/F)$; the leverage is symmetric; both wings of the smile lift with no tilt. To *tilt* a smile you need correlation, and the leverage does not supply it.

---

### 3. Computational Implementation — the leverage absorbs the driver, the vanillas do not see it

We take a **flat $20\%$ market** (so the target local variance is $0.0400$ at every $(t,S)$) and two different stochastic-volatility drivers with different conditional-variance shapes. We compute the leverage each one needs, and show the local variance — hence the vanillas — is identical while the leverage functions differ. Stdlib only.

```python
import math
v0,vbar,lam,eta=0.0174,0.0354,1.3253,0.3877
xi0=lambda t: vbar+(v0-vbar)*math.exp(-lam*t)      # Heston forward-variance curve xi_0^t
SL2=0.04                                           # target local variance (a flat 20% market)
print("Target market: flat 20% -> target local variance sigma_loc^2 = 0.0400 at every (t,S).")
print("Leverage function  sigma(t,S)^2 = sigma_loc(t,S)^2 / m(t,S),  m(t,S)=E[v_t|S_t=S].")
print("Two different stochastic-volatility drivers, SAME vanillas:")
print("  driver A (independent vol):   m_A(t,S) = xi_0^t")
print("  driver B (leverage effect):   m_B(t,S) = xi_0^t * exp(-2S/S0 + 2), S0=100")
print()
mA=lambda t,S: xi0(t)
mB=lambda t,S: xi0(t)*math.exp(-2.0*S/100.0+2.0)
print("   t     S      m_A        sigma_A    m_B        sigma_B    sigma^2*m  (both)")
for t,S in ((0.0,100.0),(0.25,80.0),(0.25,100.0),(0.25,120.0),(1.0,80.0),(1.0,100.0),(1.0,120.0)):
    sA=math.sqrt(SL2/mA(t,S)); sB=math.sqrt(SL2/mB(t,S))
    print("  %.2f  %5.0f   %8.5f   %8.5f   %8.5f   %8.5f   %8.5f"%(t,S,mA(t,S),sA,mB(t,S),sB,sB*sB*mB(t,S)))
print()
print("Both columns reproduce the same local variance (last column = 0.040000), hence the same")
print("vanilla prices; the leverage functions differ, so the spot/vol dynamics differ.")
sA80=math.sqrt(SL2/mA(1.0,80.0)); sB80=math.sqrt(SL2/mB(1.0,80.0))
print("At t=1, S=80:  sigma_A=%.5f   sigma_B=%.5f   sigma_B/sigma_A=%.4f  (%.1f%% lower: driver B"
      %(sA80,sB80,sB80/sA80,100*(1-sB80/sA80)))
print("already carries more conditional variance in the crash wing, so its leverage needs to be smaller).")
```
```
Target market: flat 20% -> target local variance sigma_loc^2 = 0.0400 at every (t,S).
Leverage function  sigma(t,S)^2 = sigma_loc(t,S)^2 / m(t,S),  m(t,S)=E[v_t|S_t=S].
Two different stochastic-volatility drivers, SAME vanillas:
  driver A (independent vol):   m_A(t,S) = xi_0^t
  driver B (leverage effect):   m_B(t,S) = xi_0^t * exp(-2S/S0 + 2), S0=100

   t     S      m_A        sigma_A    m_B        sigma_B    sigma^2*m  (both)
  0.00    100    0.01740    1.51620    0.01740    1.51620    0.04000
  0.25     80    0.02248    1.33403    0.03353    1.09221    0.04000
  0.25    100    0.02248    1.33403    0.02248    1.33403    0.04000
  0.25    120    0.02248    1.33403    0.01507    1.62939    0.04000
  1.00     80    0.03062    1.14301    0.04568    0.93581    0.04000
  1.00    100    0.03062    1.14301    0.03062    1.14301    0.04000
  1.00    120    0.03062    1.14301    0.02052    1.39607    0.04000

Both columns reproduce the same local variance (last column = 0.040000), hence the same
vanilla prices; the leverage functions differ, so the spot/vol dynamics differ.
At t=1, S=80:  sigma_A=1.14301   sigma_B=0.93581   sigma_B/sigma_A=0.8187  (18.1% lower: driver B
already carries more conditional variance in the crash wing, so its leverage needs to be smaller).
```

Three facts to read off the table:

1. **The last column is $0.040000$ in every row.** Both driver/leverage pairs reproduce the identical local variance field, so they price every vanilla in the flat-$20\%$ market identically. Vanillas simply cannot tell them apart — this is the static-fit blindness that makes "we fit the smile" a non-test ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|SV Dynamics]]).
2. **The leverage functions are visibly different.** At $t{=}0$ both are $1.51620$ (because $\mathbb E[v_0|S_0]=v_0$ — the variance is *known* at time zero, so the conditional and unconditional expectations coincide there). Away from $t{=}0$ they diverge: at $t{=}1,\,S{=}80$, driver B needs a leverage $18.1\%$ *smaller* than driver A, because driver B already carries more conditional variance in the crash wing. The leverage is the accounting entry that makes the two drivers agree on statics.
3. **$m(t,S)$ is where the asymmetry lives.** Driver A has a flat $m$ in $S$ and can therefore never produce a spot-dependent volatility response on its own; driver B's $m$ rises as spot falls (the leverage effect), so its leverage has to *undo* that to keep the static fit. Putting the spot-dependence in the leverage rather than in $m$ is a modelling choice with exotic pricing consequences, and it is not visible in vanillas.

> **The first-principles warning.** It is tempting to read the table as "the leverage is free to fix the smile". It is not: the *product* is fixed by the market, and $m$ is fixed by the driver. The leverage is the only remaining degree of freedom in the split, and the split is exactly what the exotic book prices. That is the message the rest of this folder makes quantitative.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"LSV = LV plus a random factor."** Not additive: the leverage *multiplies* the stochastic driver, so the model's local variance is $\sigma^2m$, not $\sigma_{loc}^2+\text{something}$. Getting the arithmetic wrong changes the whole calibration.
2. **Treating the leverage as a fitting function.** Because vanillas see only $\sigma^2m$, a leverage "fitted" to vanillas jointly with a driver can absorb almost any driver — and then the dynamics are an artefact of the fit, not a hypothesis. Fix the driver first, then solve for the leverage ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]]).
3. **Assuming the leverage adds information.** It adds none about the *future*: it is deterministic in $(t,S)$, so it cannot produce a forward skew that the driver does not have. LSV inherits the driver's forward skew, vol-of-vol term structure and SSR ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]]).
4. **Forgetting that $\mathbb E[v_t|S_t=S]$ is a *conditional* expectation under the model.** It is not $\xi_0^t$, not the variance-swap curve, and not a historical average. Substituting any of those is the most common and most damaging implementation error.
5. **Believing "usable" is automatic.** Bergomi's admissibility condition — the pricing function must be insensitive to the SV state variables for fixed hedge instruments — is not satisfied by most LSV constructions ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06 · Advanced Extensions]]).
6. **Thinking one more parameter fixes the forward smile.** The leverage cannot; only the driver can. If the forward skew is wrong, change the driver (add a factor, add roughness, add jumps) — not the leverage.

---

### 5. Canonical Literature & Study References

- **Guyon, J. & Henry-Labordère, P.** (2012), *Being particular about calibration*, Risk **25**(1), 91–107 — the paper that made LSV a practical production object; the particle method and the "particular" (nonlinear) structure of the calibration. *Primary source.*
- **Bergomi, L.**, *Stochastic Volatility Modeling*, Ch 1 (the Black–Scholes equation as an "accounting" identity — the frame that makes the leverage's role obvious) and Ch 12 §12.1–12.2 (LSV defined, the pricing equation as an ansatz, and the "not usable models" warning). *Math-verified in the corpus.*
- **Dupire, B.** (1994), *Pricing with a smile*, Risk **7**(1), 18–20; **Gyöngy, I.** (1986), *Mimicking the one-dimensional marginal distributions of processes having an Itô differential*, PTRF **71**(4), 501–516 — the two theorems behind the defining equation. **Gatheral, J.**, *The Volatility Surface*, Ch 7 §7.8 (the shape of the smile is model-generic). *Verification backdrop.*
- **Hull, J. C.**, *Options, Futures, and Other Derivatives*, Ch 20 §20.3–20.8 (why smiles exist; the surface as an interpolation tool) and Ch 20 §20.5 (minimum-variance delta — the practitioner's face of a spot-dependent leverage). *Verification report in the corpus.*
- **Ren, Y., Madan, D. & Qian, M. Q.** (2007), *Calibrating and pricing with embedded local volatility models*, Risk **20**(9); **Hagan, P. S., Kumar, D., Lesniewski, A. & Woodward, D.** (2002), *Managing smile risk*, Wilmott 84–108 — the SABR-based LSV and the LSV-LMM formulation used on rates desks.

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|VS · 02 Implied vs Local Vol]]
- Continue: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/01-from-zero-intuition|Heston & SABR · 01 From Zero]] (why variance must be a process) · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06 · Advanced Extensions]] (jumps, rough vol, LSV-LMM)
