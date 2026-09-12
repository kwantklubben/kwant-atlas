---
title: "3.7.2 Barriers & Digital (Binary) Options"
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

A **barrier option** knocks in or out when the spot touches a level $H$; a **digital/binary** pays a lump sum (cash) or the asset (asset-or-nothing) conditional on a trigger. They are the two most liquid *single-asset* exotics, and their pricing is pure **reflection principle**: every closed form is "a vanilla option, plus reflected image terms at $x\mapsto H^2/S$" (Shreve II §7.3). The practical objective: master the barrier building blocks ($A\dots F$), the **in–out parity** identity that makes barrier pricing trivial once one side is known, and the digital one-liners - then see why **discrete monitoring** breaks the nice closed forms (the subject of [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06 · Advanced Extensions]]).

Barrier notation (Haug §4.17): **down** = barrier below spot ($S>H$), **up** = barrier above spot ($S<H$); **in/out** = knocked in/out when touched; $\eta=+1$ down / $-1$ up. Eight combinations: down/up $\times$ in/out $\times$ call/put.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Reiner–Rubinstein building blocks (Haug §4.17.2, eqs 4.51–4.52) - `[V-8]`, the highest-confidence block

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

**In–out parity** (no rebate, $K=0$): $c_{di}+c_{do}=c_{\text{vanilla}}$ - a down-and-in plus down-and-out reproduces the plain call, because exactly one of the two pays. With a rebate $K\neq0$ there is an extra discounted-rebate term. Verified here: $3.3368+4.5126=7.8494=c_{\text{vanilla}}$.

#### 2.2 Digitals (Haug §4.19)

Cash-or-nothing (pay $K$ if triggered): $c=K e^{-rT}N(d)$, $p=K e^{-rT}N(-d)$, with $d=[\ln(S/X)+(b-\tfrac12\sigma^2)T]/(\sigma\sqrt T)$.

Asset-or-nothing (deliver $S_T$ if triggered): $c=S e^{(b-r)T}N(d)$, $p=S e^{(b-r)T}N(-d)$, with $d=[\ln(S/X)+(b+\tfrac12\sigma^2)T]/(\sigma\sqrt T)$.

The **delta of a cash-or-nothing** is the payoff density at the trigger - this is why pathwise MC Greeks fail for digitals (see [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 3. Computational Implementation - the barrier engine

Reproduces the Haug-verified values and the parity identity exactly. Stdlib only.




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Continuous vs discrete monitoring.** The closed forms assume *continuous* monitoring. Real contracts (and the MC that prices them) check at *discrete* dates. A continuously-monitored down-and-out is **cheaper** than a discretely-monitored one, because the continuous form "sees" barrier touches the discrete grid misses. The Broadie–Glasserman–Kou correction ([[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06]]) restores agreement.
2. **Rebate misuse.** $E$ and $F$ carry the rebate $K$; in–out parity $c_{di}+c_{do}=c_{vanilla}$ holds **only** when $K=0$. Mixing rebated and non-rebated forms is a classic desk error.
3. **In–out parity is not a free lunch.** It holds for the *same* parameters; American barriers break it, and so does discrete monitoring. Don't infer the in-side from the out-side without checking the specification matches.
4. **Digital delta is a delta spike.** The digital price is $K e^{-rT}N(d)$; its delta is proportional to the *density* $n(d)$, concentrated near the trigger. Any hedge or pathwise Greek that ignores the density (a step payoff) is wrong - see [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05]].

---

### 5. References

- **Haug**, *The Complete Guide to Option Pricing Formulas*
- **Shreve**, *Stochastic Calculus for Finance II*
- **Hull**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/03-lookbacks-and-asians|03 · Lookbacks & Asians]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
