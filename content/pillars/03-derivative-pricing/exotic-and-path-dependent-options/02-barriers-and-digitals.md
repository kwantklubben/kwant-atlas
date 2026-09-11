---
title: "02 — Barriers & Digital (Binary) Options"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - barriers
  - binary-options
  - reflection-principle
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]].

---

### 1. Intuition & Practical Objective

A **barrier option** knocks in or out when the spot touches a level $H$; a **digital/binary** pays a lump sum (cash) or the asset (asset-or-nothing) conditional on a trigger. They are the two most liquid *single-asset* exotics, and their pricing is pure **reflection principle**: every closed form is "a vanilla option, plus reflected image terms at $x\mapsto H^2/S$" (Shreve II §7.3). The practical objective: master the barrier building blocks ($A\dots F$), the **in–out parity** identity that makes barrier pricing trivial once one side is known, and the digital one-liners — then see why **discrete monitoring** breaks the nice closed forms (the subject of [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06 · Advanced Extensions]]).

Barrier notation (Haug §4.17): **down** = barrier below spot ($S>H$), **up** = barrier above spot ($S<H$); **in/out** = knocked in/out when touched; $\eta=+1$ down / $-1$ up. Eight combinations: down/up $\times$ in/out $\times$ call/put.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Reiner–Rubinstein building blocks (Haug §4.17.2, eqs 4.51–4.52) — `[V-8]`, the highest-confidence block

With $\phi=+1$ call / $-1$ put, $\eta=+1$ down / $-1$ up, and the scaling exponents

$$
\mu=\frac{b-\tfrac12\sigma^2}{\sigma^2},\qquad \lambda=\sqrt{\mu^2+\frac{2r}{\sigma^2}},
$$

$$
x_1=\frac{\ln(S/X)}{\sigma\sqrt T}+(1+\mu)\sigma\sqrt T,\; x_2=\frac{\ln(S/H)}{\sigma\sqrt T}+(1+\mu)\sigma\sqrt T,
$$
$$
y_1=\frac{\ln(H^2/(SX))}{\sigma\sqrt T}+(1+\mu)\sigma\sqrt T,\; y_2=\frac{\ln(H/S)}{\sigma\sqrt T}+(1+\mu)\sigma\sqrt T,\; z=\frac{\ln(H/S)}{\sigma\sqrt T}+\lambda\sigma\sqrt T,
$$

the six blocks are

$$
A=\phi S e^{(b-r)T}N(\phi x_1)-\phi X e^{-rT}N(\phi x_1-\phi\sigma\sqrt T)
$$
$$
B=\phi S e^{(b-r)T}N(\phi x_2)-\phi X e^{-rT}N(\phi x_2-\phi\sigma\sqrt T)
$$
$$
C=\phi S e^{(b-r)T}\big(\tfrac HS\big)^{2(\mu+1)}N(\eta y_1)-\phi X e^{-rT}\big(\tfrac HS\big)^{2\mu}N(\eta y_1-\eta\sigma\sqrt T)
$$
$$
D=\phi S e^{(b-r)T}\big(\tfrac HS\big)^{2(\mu+1)}N(\eta y_2)-\phi X e^{-rT}\big(\tfrac HS\big)^{2\mu}N(\eta y_2-\eta\sigma\sqrt T)
$$
$$
E=K e^{-rT}\big[N(\eta x_2-\eta\sigma\sqrt T)-\big(\tfrac HS\big)^{2\mu}N(\eta y_2-\eta\sigma\sqrt T)\big]
$$
$$
F=K\big[\big(\tfrac HS\big)^{\mu+\lambda}N(\eta z)+\big(\tfrac HS\big)^{\mu-\lambda}N(\eta z-2\eta\lambda\sigma\sqrt T)\big]
$$

Combination table (call; puts analogous):

| Option | $S>H$ | $S<H$ |
|---|---|---|
| Down-and-in call | $C+E$ | $A-B+D+E$ |
| Up-and-in call | $A+E$ | $B-C+D+E$ |
| Down-and-out call | $A-C+F$ | $B-D+F$ |
| Up-and-out call | $F$ | $A-B+C-D+F$ |

**In–out parity** (no rebate, $K=0$): $c_{di}+c_{do}=c_{\text{vanilla}}$ — a down-and-in plus down-and-out reproduces the plain call, because exactly one of the two pays. With a rebate $K\neq0$ there is an extra discounted-rebate term. Verified here: $3.3368+4.5126=7.8494=c_{\text{vanilla}}$.

#### 2.2 Digitals (Haug §4.19)

Cash-or-nothing (pay $K$ if triggered): $c=K e^{-rT}N(d)$, $p=K e^{-rT}N(-d)$, with $d=[\ln(S/X)+(b-\tfrac12\sigma^2)T]/(\sigma\sqrt T)$.

Asset-or-nothing (deliver $S_T$ if triggered): $c=S e^{(b-r)T}N(d)$, $p=S e^{(b-r)T}N(-d)$, with $d=[\ln(S/X)+(b+\tfrac12\sigma^2)T]/(\sigma\sqrt T)$.

The **delta of a cash-or-nothing** is the payoff density at the trigger — this is why pathwise MC Greeks fail for digitals (see [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 3. Computational Implementation — the barrier engine

Reproduces the Haug-verified values and the parity identity exactly. Stdlib only.

```python
import math
from math import log, exp, sqrt

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def barrier(S, X, H, K, T, r, b, sig, phi_f, eta):
    sT = sig*sqrt(T); mu = (b - 0.5*sig**2)/sig**2
    la = math.sqrt(mu*mu + 2*r/(sig*sig)); hs = H/S
    x1 = log(S/X)/sT+(1+mu)*sT; x2 = log(S/H)/sT+(1+mu)*sT
    y1 = log(H*H/(S*X))/sT+(1+mu)*sT; y2 = log(H/S)/sT+(1+mu)*sT; z = log(H/S)/sT+la*sT
    A = phi_f*S*exp((b-r)*T)*N(phi_f*x1) - phi_f*X*exp(-r*T)*N(phi_f*x1-phi_f*sT)
    B = phi_f*S*exp((b-r)*T)*N(phi_f*x2) - phi_f*X*exp(-r*T)*N(phi_f*x2-phi_f*sT)
    C = phi_f*S*exp((b-r)*T)*hs**(2*(mu+1))*N(eta*y1) - phi_f*X*exp(-r*T)*hs**(2*mu)*N(eta*y1-eta*sT)
    D = phi_f*S*exp((b-r)*T)*hs**(2*(mu+1))*N(eta*y2) - phi_f*X*exp(-r*T)*hs**(2*mu)*N(eta*y2-eta*sT)
    E = K*exp(-r*T)*(N(eta*x2-eta*sT) - hs**(2*mu)*N(eta*y2-eta*sT))
    F = K*(hs**(mu+la)*N(eta*z) + hs**(mu-la)*N(eta*z-2*eta*la*sT))
    return A, B, C, D, E, F

def c_di(S,X,H,K,T,r,b,sig):
    A,B,C,D,E,F = barrier(S,X,H,K,T,r,b,sig,1,1); return C+E if S>H else A-B+D+E
def c_do(S,X,H,K,T,r,b,sig):
    A,B,C,D,E,F = barrier(S,X,H,K,T,r,b,sig,1,1); return A-C+F if S>H else B-D+F
def c_ui(S,X,H,K,T,r,b,sig):
    A,B,C,D,E,F = barrier(S,X,H,K,T,r,b,sig,1,-1); return A+E if S>H else B-C+D+E
def bsm_call(S,X,T,r,b,sig):
    d1=(log(S/X)+(b+0.5*sig**2)*T)/(sig*sqrt(T)); d2=d1-sig*sqrt(T)
    return S*exp((b-r)*T)*N(d1)-X*exp(-r*T)*N(d2)

# Haug Table 4-13 anchor: S=X=100, T=.5, r=.08, b=.04, rebate=3
print(f"down-and-out call H=95 sig=.25 = {c_do(100,100,95,3,.5,.08,.04,.25):.5f}  (Haug 6.7924)")
print(f"down-and-out call H=95 sig=.30 = {c_do(100,100,95,3,.5,.08,.04,.30):.5f}  (Haug 7.0285)")
print(f"up-and-in   call H=105 sig=.25 = {c_ui(100,100,105,3,.5,.08,.04,.25):.5f}  (Haug 8.4482)")

# in-out parity, no rebate (K=0): c_di + c_do = vanilla
v = c_di(100,100,95,0,.5,.08,.04,.25) + c_do(100,100,95,0,.5,.08,.04,.25)
print(f"c_di + c_do = {v:.4f}  ==  vanilla {bsm_call(100,100,.5,.08,.04,.25):.4f}  (parity OK)")

# digitals (Haug 4.84-4.87)
d = (log(100/80)+(0-0.5*.35**2)*.75)/(.35*sqrt(.75))
print(f"cash-or-nothing put = {10*exp(-.06*.75)*N(-d):.4f}  (Haug 2.6710)")
d = (log(70/65)+(.02+0.5*.27**2)*.5)/(.27*sqrt(.5))
print(f"asset-or-nothing put= {70*exp((.02-.07)*.5)*N(-d):.4f}  (Haug 20.2069)")
```
```
down-and-out call H=95 sig=.25 = 6.79244  (Haug 6.7924)
down-and-out call H=95 sig=.30 = 7.02854  (Haug 7.0285)
up-and-in   call H=105 sig=.25 = 8.44821  (Haug 8.4482)
c_di + c_do = 7.8494  ==  vanilla 7.8494  (parity OK)
cash-or-nothing put = 2.6710  (Haug 2.6710)
asset-or-nothing put= 20.2069  (Haug 20.2069)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Continuous vs discrete monitoring.** The closed forms assume *continuous* monitoring. Real contracts (and the MC that prices them) check at *discrete* dates. A continuously-monitored down-and-out is **cheaper** than a discretely-monitored one, because the continuous form "sees" barrier touches the discrete grid misses. The Broadie–Glasserman–Kou correction ([[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06]]) restores agreement.
2. **Rebate misuse.** $E$ and $F$ carry the rebate $K$; in–out parity $c_{di}+c_{do}=c_{vanilla}$ holds **only** when $K=0$. Mixing rebated and non-rebated forms is a classic desk error.
3. **In–out parity is not a free lunch.** It holds for the *same* parameters; American barriers break it, and so does discrete monitoring. Don't infer the in-side from the out-side without checking the specification matches.
4. **Digital delta is a delta spike.** The digital price is $K e^{-rT}N(d)$; its delta is proportional to the *density* $n(d)$, concentrated near the trigger. Any hedge or pathwise Greek that ignores the density (a step payoff) is wrong — see [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05]].

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, §4.17 (barrier options, eqs 4.51–4.52, `[V-8]` verified block) and §4.19 (binary options, eqs 4.84–4.87). §5.6 (discrete-barrier correction, Broadie–Glasserman–Kou).
- **Shreve**, *Stochastic Calculus for Finance II*, §7.2 (joint density of max & terminal, the reflection principle) and §7.3 (knock-out barrier PDE; the hedge $\Delta=v_x$ "breaks down" near the barrier — why industry prices a barrier slightly above $B$).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 26 (barrier & binary catalog; $c=c_{di}+c_{do}$).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/03-lookbacks-and-asians|03 · Lookbacks & Asians]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
