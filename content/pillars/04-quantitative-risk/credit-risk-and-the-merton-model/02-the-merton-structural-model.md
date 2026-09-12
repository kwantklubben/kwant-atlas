---
title: "4.4.2 The Merton Structural Model"
tags:
  - pillar-quantitative-risk
  - credit-risk-and-the-merton-model
  - structural-model
  - merton-1974
  - equity-call
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/01-from-zero-intuition|01 · From Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]].

---

### 1. Intuition & Practical Objective

The structural model takes the payoff insight of page 01 and turns it into a *pricing machine*. Two assumptions do all the work:

1. The firm's assets follow a geometric Brownian motion, $dV=\mu V\,dt+\sigma_V V\,dW$.
2. The firm has issued a single zero-coupon bond of face $D$ maturing at $T$; default happens **only** at $T$, and only if $V_T<D$.

Under those assumptions the equity claim $E=V\,N(d_1)-D e^{-rT}N(d_2)$ is *not an approximation* - it is the exact no-arbitrage price of the shareholders' position. The practical objective is the **inverse problem**: real data gives us equity price $E_0$ and equity volatility $\sigma_E$, but the model runs on $(V_0,\sigma_V)$, which are unobservable. So we must solve the two-equation system

$$
E_0=V_0\,N(d_1)-D e^{-rT}N(d_2),\qquad \sigma_E E_0=N(d_1)\,\sigma_V V_0
$$

for the two unknowns $(V_0,\sigma_V)$. Everything downstream - distance to default, PD, credit spread - is then deterministic algebra.

> **Why two equations?** Equity fixes the *scale* of firm value (the call equation); equity volatility fixes the firm's *riskiness* (the vol identity, which is Itô applied to $E(V,t)$: $\sigma_E E=\partial E/\partial V\cdot\sigma_V V=N(d_1)\sigma_V V$).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The equity PDE (Merton 1974, eqs. 10–11)

Let $f(V,t)$ be equity value and $F(V,t)$ the debt value, $V=f+F$. The firm's asset dynamics give, for any claim on the firm's assets under the risk-free measure,
$$
\tfrac12\sigma_V^2V^2F_{VV}+rVF_V-rF-F_t=0 .
$$
Substituting $f=V-F$ and using $F_{VV}=-f_{VV}$, $F_V=1-f_V$ (Merton eq. 15), the equity value satisfies the **same BSM PDE**,
$$
\tfrac12\sigma_V^2V^2 f_{VV}+rVf_V-rf-f_t=0,
$$
with terminal condition $f(V,0)=\max(0,V-B)$ and boundary conditions $f(0,t)=0$, $f(V,t)\le V$. This is precisely the BSM PDE for a European call on $V$ struck at $B$ - so the solution is (Merton eq. 12)
$$
\boxed{\,E=f(V,t)=V\,N(d_1)-B e^{-rt}N(d_2)\,},\qquad
d_1=\frac{\ln(V/B)+(r+\tfrac12\sigma_V^2)t}{\sigma_V\sqrt t},\quad d_2=d_1-\sigma_V\sqrt t .
$$

#### 2.2 The debt value and the risk structure (Merton eqs. 13–14)

From $F=V-E$,
$$
F(V,t)=B e^{-rt}\Big\{\Phi\big[h_2(d,\sigma_V^2 t)\big]+\tfrac1d\,\Phi\big[h_1(d,\sigma_V^2 t)\big]\Big\},
$$
where the *quasi* debt-to-firm ratio is $d=B e^{-rt}/V$ and
$$
h_1(d,\sigma_V^2 t)=-\frac{\tfrac12\sigma_V^2 t-\ln d}{\sigma_V\sqrt t},\qquad
h_2(d,\sigma_V^2 t)=-\frac{\tfrac12\sigma_V^2 t+\ln d}{\sigma_V\sqrt t}.
$$
Because bond talk is in yields, define the risky yield by $e^{-R(t)t}=F(V,t)/B$, giving **Merton's risk structure of interest rates** (eq. 14):
$$
R(t)-r=-\frac1t\ln\Big\{\Phi\big[h_2(d,\sigma_V^2 t)\big]+\tfrac1d\Phi\big[h_1(d,\sigma_V^2 t)\big]\Big\}.
$$
The striking content: *for a given maturity, the credit spread depends on only two variables* - the business risk $\sigma_V^2$ and the quasi leverage $d=B e^{-rt}/V$.

#### 2.3 Comparative statics (Merton eq. 15)

With $F[V,t,B,\sigma_V^2,r]$ shown in full:
$$
F_V=1-f_V>0,\quad F_B=-f_B>0,\quad F_t=-f_t<0,\quad F_{\sigma_V^2}=-f_{\sigma_V^2}<0,\quad F_r=-t\,D e^{-rt}N(d_2)<0 .
$$
Translation: debt value rises with firm value and promised payment; **falls with time to maturity, firm volatility, and the riskless rate.** Since equity is a call and the call is homogeneous of degree one and convex in $(V,B)$, default-free debt-plus-equity is concave in $V$ - the origin of the equity skew.

#### 2.4 The two-equation inversion (Hull eqs. 24.3–24.4)

The *observable* system is Hull's §24.6:
$$
\boxed{\,E_0=V_0\,N(d_1)-D e^{-rT}N(d_2)\,},\qquad \boxed{\,\sigma_E E_0=N(d_1)\,\sigma_V V_0\,},
$$
with $\mathbb{Q}(\text{default})=N(-d_2)$. This is solved numerically (fixed point or Newton) - §3 below.

---

### 3. Computational Implementation - forward map, then inverse map

The acid test of any structural-model implementation: assume *true* firm parameters, generate the *equity observables*, then feed only the equity observables back in and check that the solver recovers the firm parameters. Stdlib only.



The solver recovers the firm parameters to machine precision - the forward/inverse maps are consistent. Note the last line is already a **failure-mode preview**: the model spread is $2.7$ bp for a firm whose equity vol is $48\%$ and whose book leverage ($D/V=0.6$) is high.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The inverse problem is ill-conditioned.** The two-equation system must be solved numerically, and near the interesting region (levered, high-vol firms) the Jacobian is nearly singular - small errors in $\sigma_E$ produce large errors in $\sigma_V$ and hence in PD. See [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/03-distance-to-default-and-pd|03]] and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05]].
2. **Single zero-coupon bond, default only at $T$.** Real capital structures are multi-layered and default can happen at *any* time. Merton's own §VI extends to coupon/callable bonds, but the vanilla formula's "$T$-only" default is the source of the credit-spread puzzle.
3. **Constant $\sigma_V$ and a lognormal firm.** The same constant-volatility delusion that afflicts BSM afflicts the firm: no jumps means no *jump-to-default*, so a firm can never default "suddenly".
4. **$\partial E/\partial V=N(d_1)<1$ breaks the naive hedge.** Equity is a *levered* claim: equity vol exceeds asset vol, and equity beta with the market exceeds 1 - a direct consequence of the convexity in §2.3 that practitioners must respect.

---

### 5. References

- **Merton (1974)**, *On the Pricing of Corporate Debt*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Bluhm, Overbeck & Wagner**, *Introduction to Credit Risk Modeling*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/03-distance-to-default-and-pd|03 · Distance-to-Default & PD]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Index Hub]]
- Theory: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/06-advanced-extensions|06 · Portfolio Credit & Vasicek]]
