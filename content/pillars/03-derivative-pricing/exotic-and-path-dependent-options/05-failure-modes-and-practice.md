---
title: "05 — Failure Modes & Real-World Practice for Exotics"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - failure-modes
  - monte-carlo
  - discrete-monitoring
  - greeks
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange|04 · Compound/Chooser/Quanto/Exchange]].

---

### 1. Intuition & Practical Objective

The closed forms in this folder are beautiful, and *three of their assumptions break in real markets*. This page names the failures precisely and shows each in money terms, so a practitioner knows *which* knob to distrust:

1. **Monitoring is discrete, not continuous.** The barrier closed forms assume the barrier is watched continuously. Real contracts (and MC) check at discrete dates, so the discrete price is systematically **above** the continuous one for knock-outs (the grid "misses" touches).
2. **Pathwise MC Greeks fail for the step payoffs.** Digit/digital and barrier deltas come from a *density*, not a step — pathwise differentiation gives exactly zero (Glasserman Ch 7). Only the likelihood-ratio (score) method recovers the true Greek.
3. **Correlation is a wobbly input.** Quanto/exchange/spread prices depend on $\rho$; it is the least-stable market parameter, and a small error propagates through the closed forms ([[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Implied Volatility Surfaces]]).

---

### 2. Mathematical Ground Truth & Derivations

**Discrete vs continuous monitoring.** The continuously-monitored down-and-out value $v_c$ uses the first-hitting-time density of the Brownian bridge. A discretely-monitored contract (grid $\Delta t$) only sees the path at grid points, so the knock-out probability is smaller and the value $v_d>v_c$. Broadie–Glasserman–Kou (1995) restore agreement to $O(\Delta t)$ by pricing the **continuous** formula at the *shifted* barrier

$$H_D = H\,e^{\pm\beta\sigma\sqrt{\Delta t}},\qquad \beta=\frac{\zeta(1/2)}{\sqrt{2\pi}}\approx 0.5826,$$

`+` when the barrier is above spot, `−` when below (Haug §5.6). This is the single most-used "dirty fix" in the exotic-options playbook.

**Pathwise vs likelihood-ratio Greeks (Glasserman Ch 7).** For a digital $Y=e^{-rT}K\mathbf 1\{S_T>X\}$, the pathwise derivative $dY/dS_0$ exists a.s. but equals **zero** — the indicator is flat almost everywhere, and the genuine delta comes from the strike-crossing that pathwise differentiation misses. The likelihood-ratio method differentiates the *density* instead: for lognormal $S_T$, the score is $Z/(S_0\sigma\sqrt T)$, and the LR delta estimator is

$$\widehat{\Delta}_{LR}=e^{-rT}K\,\mathbf 1\{S_T>X\}\cdot\frac{Z}{S_0\sigma\sqrt T},\qquad\text{with }\mathbb{E}[\widehat{\Delta}_{LR}]=K e^{-rT}\frac{\varphi(d_2)}{S_0\sigma\sqrt T}.$$

The rule of thumb (Glasserman §7.2.2): pathwise applies when the payoff is **continuous (Lipschitz)** in the parameter — which *excludes* digitals, barriers, and 2nd derivatives.

---

### 3. Computational Implementation — the failures in numbers

**Experiment 1 — discrete monitoring overprices a knock-out, BGK fixes it.** Stdlib only.

```python
import math, random
from math import log, exp, sqrt

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def barrier(S,X,H,K,T,r,b,sig,phi_f,eta):
    sT=sig*sqrt(T); mu=(b-0.5*sig**2)/sig**2; la=math.sqrt(mu*mu+2*r/(sig*sig)); hs=H/S
    x1=log(S/X)/sT+(1+mu)*sT; x2=log(S/H)/sT+(1+mu)*sT
    y1=log(H*H/(S*X))/sT+(1+mu)*sT; y2=log(H/S)/sT+(1+mu)*sT; z=log(H/S)/sT+la*sT
    A=phi_f*S*exp((b-r)*T)*N(phi_f*x1)-phi_f*X*exp(-r*T)*N(phi_f*x1-phi_f*sT)
    B=phi_f*S*exp((b-r)*T)*N(phi_f*x2)-phi_f*X*exp(-r*T)*N(phi_f*x2-phi_f*sT)
    C=phi_f*S*exp((b-r)*T)*hs**(2*(mu+1))*N(eta*y1)-phi_f*X*exp(-r*T)*hs**(2*mu)*N(eta*y1-eta*sT)
    D=phi_f*S*exp((b-r)*T)*hs**(2*(mu+1))*N(eta*y2)-phi_f*X*exp(-r*T)*hs**(2*mu)*N(eta*y2-eta*sT)
    E=K*exp(-r*T)*(N(eta*x2-eta*sT)-hs**(2*mu)*N(eta*y2-eta*sT))
    F=K*(hs**(mu+la)*N(eta*z)+hs**(mu-la)*N(eta*z-2*eta*la*sT))
    return A,B,C,D,E,F
def c_do(S,X,H,K,T,r,b,sig):
    A,B,C,D,E,F=barrier(S,X,H,K,T,r,b,sig,1,1); return A-C+F if S>H else B-D+F

def mc_doc(S,X,H,T,r,sig,nsteps,npath,seed):   # discretely-monitored down-and-out
    rnd=random.Random(seed); tot=0.0; dt=T/nsteps
    for _ in range(npath):
        St=S; alive=True
        for _ in range(nsteps):
            St*=exp((r-0.5*sig**2)*dt+sig*sqrt(dt)*rnd.gauss(0,1))
            if St<H: alive=False; break
        if alive: tot+=max(St-X,0)
    return exp(-r*T)*tot/npath

r,b,sig=0.08,0.08,0.25
closed=c_do(100,100,95,0,.5,r,b,sig)              # continuous closed form (no rebate)
print(f"continuous closed-form down-and-out = {closed:.4f}")
for ns in (25,100,400):
    print(f"  discrete MC, nsteps={ns:3d}       = {mc_doc(100,100,95,.5,r,sig,ns,40000,11):.4f}  (over-priced: grid misses hits)")
beta=0.5826
for ns in (25,100):
    dt=.5/ns; Hd=95*exp(-beta*sig*sqrt(dt))
    print(f"  BGK, nsteps={ns:3d}: H_D={Hd:.3f} -> continuous-form price = "
          f"{c_do(100,100,Hd,0,.5,r,b,sig):.4f}  vs  discrete MC {mc_doc(100,100,95,.5,r,sig,ns,40000,11):.4f}")
```
```
continuous closed-form down-and-out = 5.2998
  discrete MC, nsteps= 25       = 6.5904  (over-priced: grid misses hits)
  discrete MC, nsteps=100       = 6.0473  (over-priced: grid misses hits)
  discrete MC, nsteps=400       = 5.7857  (over-priced: grid misses hits)
  BGK, nsteps= 25: H_D=93.063 -> continuous-form price = 6.5635  vs  discrete MC 6.5904
  BGK, nsteps=100: H_D=94.027 -> continuous-form price = 5.9831  vs  discrete MC 6.0473
```
Discrete MC overprices the knock-out by up to ~24% at coarse grids; the BGK-shifted continuous formula lands within MC error of the discrete MC.

**Experiment 2 — pathwise delta of a digital fails; likelihood-ratio recovers it.**

```python
import math, random
from math import log, exp, sqrt, pi
def N(x):  return 0.5*(1+math.erf(x/math.sqrt(2)))
def phi(x):return exp(-0.5*x*x)/sqrt(2*pi)

S,X,K,T,r,b,sig=100,100,1,.5,.05,.05,.20
d2=(log(S/X)+(b-0.5*sig**2)*T)/(sig*sqrt(T))
anal=K*exp(-r*T)*phi(d2)/(S*sig*sqrt(T))           # analytic digital-call delta
print(f"analytic digital-call delta = {anal:.6f}")
rnd=random.Random(3); np=200000; lr=0.0
for _ in range(np):
    W=rnd.gauss(0,1); ST=S*exp((r-0.5*sig**2)*T+sig*sqrt(T)*W)
    ind=1.0 if ST>X else 0.0
    lr+=ind*(W/(S*sig*sqrt(T)))                    # LR score (pathwise dY/dS0 == 0 a.s.)
print(f"pathwise delta             = 0.000000  (fails: step payoff is flat a.s.)")
print(f"likelihood-ratio delta     = {exp(-r*T)*K*lr/np:.6f}")
```
```
analytic digital-call delta = 0.027359
pathwise delta             = 0.000000  (fails: step payoff is flat a.s.)
likelihood-ratio delta     = 0.027338
```
The pathwise derivative of the digital is identically zero — useless. The likelihood-ratio (score) estimator matches the analytic delta to 4 dp, because it differentiates the density, not the step.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Continuous-form assumption (monitoring).** Using the continuous closed form for a discretely-monitored barrier misprices by the whole missed-hit probability — Experiment 1 quantifies it, BGK fixes it.
2. **Pathwise Greeks on step payoffs.** Digit/binary and barrier deltas cannot come from pathwise differentiation (identically zero); use likelihood-ratio or finite differences with common random numbers (Glasserman Ch 7; the central+CRN estimator dominates with RMSE $O(n^{-2/5})$).
3. **Correlation instability.** Margrabe/quanto/spread depend on $\rho$; it drifts and smiles, and it is *less* observable than vol. Always re-run the exotic price across a $\rho$-band (sensitivity, not point estimate).
4. **Rebate & parity traps.** In–out parity holds only at $K=0$; mixing rebated and non-rebated forms (or using American barrier parity, which fails) misprices.
5. **MC dimension confusion.** MC error is $O(n^{-1/2})$ in *paths*, but the discrete-monitoring bias is $O(\Delta t)$ in *steps*. A "converged" MC on too-coarse a grid is confidently wrong — always push $n_{steps}$ and check it changes the answer.

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 7 (pathwise vs likelihood-ratio: the digital/barrier failure, score estimators, finite-difference bias/variance tradeoffs) and Ch 1 (the $O(n^{-1/2})$ rate, §1.1).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §5.6 (Broadie–Glasserman–Kou discrete-barrier correction).
- **Broadie, Glasserman & Kou (1995)**, "A Continuity Correction for Discrete Barrier Options," *Math. Finance* — the source of $H_D=He^{\pm\beta\sigma\sqrt{\Delta t}}$.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 26–27 (pricing notes and the numerical route for path-dependent products).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange|04 · Compound/Chooser/Quanto/Exchange]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-and-sabr|Heston & SABR]]
