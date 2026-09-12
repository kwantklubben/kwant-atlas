---
title: "3.6.3 Analytic Approximations"
tags:
  - pillar-derivative-pricing
  - american-options
  - barone-adesi-whaley
  - bjerksund-stensland
  - perpetual-options
  - closed-form
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/02-optimal-stopping-theory|02 · Optimal-Stopping Theory]] and [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · Pricing Formulas]].

---

### 1. Intuition & Practical Objective

American options have no exact closed form - but they have an **exact closed form in one limit and good closed-form approximations everywhere else**. This page is the **analytic-approximation lookup**: the base case (perpetual options, which *do* solve exactly), the two industry approximations (Barone–Adesi–Whaley, Bjerksund–Stensland), and the transformation that turns every American *put* into an American *call*.

The idea behind every approximation is the same as the structure of the problem. The American value is the European value plus a **premium** for the early-exercise right;

$$
V^{\text{Am}}(S)=v^{\text{Eu}}(S)+\text{early-exercise premium}(S).
$$

The premium is zero deep out-of-the-money, grows as $S$ moves toward the boundary, and is exactly $(S-X)-v^{\text{Eu}}$ at the boundary. Approximations differ only in *how they guess the shape of the premium*. Barone–Adesi–Whaley guesses a single power $A_2(S/S^*)^{q_2}$ and solves a one-dimensional root-find for the boundary $S^*$; Bjerksund–Stensland instead approximates the *exercise boundary itself* as flat (1993) or two-piece (2002), and integrates the resulting payoff analytically.

> **Why perpetual matters.** With infinite maturity the value is time-homogeneous, the PDE becomes an ODE, and the problem *solves exactly* - boundary and all. It is both the only true closed form and the $\tau\to\infty$ limit that every finite-maturity boundary tends toward.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Perpetual American put - the canonical solved case (Shreve II §8.3; Björk Prop 21.30)

Infinite horizon, $dS=rS\,dt+\sigma S\,dW$ under $\mathbb Q$, payoff $g(x)=(K-x)^+$. The continuation-region ODE $\tfrac12\sigma^2x^2v''+rxv'-rv=0$ has independent solutions $x$ and $x^{-\gamma}$ with

$$
\gamma=\frac{2r}{\sigma^2}\qquad(\text{Shreve Eq. 8.3.14; Björk Eq. 21.71}).
$$

Boundedness as $x\to\infty$ kills the $x$ solution, leaving $v(x)=Bx^{-\gamma}$. **Value matching** $v(L^*)=K-L^*$ and **smooth pasting** $v'(L^*)=-1$ give the boundary and the value:

$$
L^*=\frac{\gamma K}{1+\gamma}=\frac{2rK}{2r+\sigma^2}\qquad(\text{Eq. 8.3.12}),\qquad
v(x)=\begin{cases}K-x, & 0\le x\le L^*,\\[2pt] (K-L^*)\left(\dfrac{x}{L^*}\right)^{-\gamma}, & x\ge L^*.\end{cases}\tag{8.3.13}
$$

Checking smooth pasting directly: the right derivative at $L^*$ is $-\gamma(K-L^*)/L^*=-1$ - reproducing $L^*=2rK/(2r+\sigma^2)$ (Shreve Eq. 8.3.14). Note the second derivative *jumps* at $L^*$ ($0$ on the left, positive on the right); only $C^1$ smoothness is required.

#### 2.2 Perpetual options with cost-of-carry $b$ (Haug §3.5)

$$
c=\frac{(\gamma_1-1)^{\gamma_1-1}}{\gamma_1^{\gamma_1}}\left(\frac{S}{X}\right)^{\gamma_1}X,\quad
\gamma_1=\left(\tfrac12-\tfrac{b}{\sigma^2}\right)+\sqrt{\left(\tfrac{b}{\sigma^2}-\tfrac12\right)^2+\tfrac{2r}{\sigma^2}}\qquad(\text{call, }b<r),
$$
$$
p=\frac{X}{1-\gamma_2}\left(\frac{\gamma_2-1}{\gamma_2}\cdot\frac{S}{X}\right)^{\gamma_2},\quad
\gamma_2=\left(\tfrac12-\tfrac{b}{\sigma^2}\right)-\sqrt{\left(\tfrac{b}{\sigma^2}-\tfrac12\right)^2+\tfrac{2r}{\sigma^2}}\qquad(\text{put}).
$$

#### 2.3 Barone–Adesi–Whaley (1987) (Haug §3.1)

**Call** ($b<r$; else $C=c_{BSM}$):
$$
C(S)=\begin{cases} c_{BSM}(S)+A_2\left(\dfrac{S}{S^*}\right)^{q_2}, & S<S^*,\\[4pt] S-X, & S\ge S^*,\end{cases}
\quad A_2=\frac{S^*}{q_2}\Big[1-e^{(b-r)T}N\big(d_1(S^*)\big)\Big],
$$
$$
q_2=\frac{-(N-1)+\sqrt{(N-1)^2+4M/K}}{2},\quad M=\frac{2r}{\sigma^2},\ N=\frac{2b}{\sigma^2},\ K=1-e^{-rT}.
$$

The critical price $S^*$ solves $S^*-X=c_{BSM}(S^*)+\big(1-e^{(b-r)T}N(d_1(S^*))\big)S^*/q_2$ (Newton–Raphson, tolerance $|LHS-RHS|/X<10^{-5}$). The **put** is symmetric with $q_1=\frac{-(N-1)-\sqrt{(N-1)^2+4M/K}}{2}$, $A_1=-\frac{S^{**}}{q_1}[1-e^{(b-r)T}N(-d_1(S^{**}))]$ and boundary $S^{**}<X$.

#### 2.4 Bjerksund–Stensland 1993 (Haug §3.2)

Model the boundary as a **flat** trigger $I$ and integrate the payoff analytically:
$$
C=\alpha S^\beta-\alpha\,\phi(S,T,\beta,I,I)+\phi(S,T,1,I,I)-\phi(S,T,1,X,I)-X\phi(S,T,0,I,I)+X\phi(S,T,0,X,I),
$$
$$
\alpha=(I-X)I^{-\beta},\quad \beta=\left(\tfrac12-\tfrac{b}{\sigma^2}\right)+\sqrt{\left(\tfrac{b}{\sigma^2}-\tfrac12\right)^2+\tfrac{2r}{\sigma^2}},\quad
\phi(S,T,\gamma,H,I)=e^{\lambda}S^\gamma\left[N(d)-\left(\tfrac{I}{S}\right)^{\kappa}N\!\left(d-\tfrac{2\ln(I/S)}{\sigma\sqrt T}\right)\right],
$$
$$
\lambda=\big({-r}+\gamma b+\tfrac12\gamma(\gamma-1)\sigma^2\big)T,\quad d=-\frac{\ln(S/H)+(b+(\gamma-\tfrac12)\sigma^2)T}{\sigma\sqrt T},\quad\kappa=\frac{2b}{\sigma^2}+2\gamma-1.
$$

Trigger $I=B_0+(B_\infty-B_0)(1-e^{h(T)})$, $B_\infty=\frac{\beta}{\beta-1}X$, $B_0=\max(X,\frac{r}{r-b}X)$, $h(T)=-(bT+2\sigma\sqrt T)\frac{B_0}{B_\infty-B_0}$; if $S\ge I$, exercise ⇒ $S-X$. The **2002** refinement uses a two-piece boundary (needs the bivariate normal $M(\cdot,\cdot,\rho)$) and is more accurate for long maturities.

#### 2.5 The American put-call transformation (Haug §3.4)

$$
P(S,X,T,r,b,\sigma)=C(X,S,T,\;r-b,\;-b,\;\sigma).
$$

Every American-put result - perpetual, BAW, BS-1993 - is reused for calls and vice versa, which is why Haug only tabulates one side.

---

### 3. Computational Implementation - the approximations, benchmarked

Perpetual closed forms, BAW and BS-1993, each checked against its Haug cell and against a high-resolution CRR tree. Stdlib only.



*(The BAW call values differ from Haug's printed cells by $2\times10^{-4}$ - his Newton tolerance, not the formula. BS-1993 reproduces Haug's $5.2704$ exactly.)* BAW's error is tens of basis points against a 4000-step tree - good for desk use, too coarse for risk sensitivities near the boundary.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **BAW is not uniformly accurate.** Error grows with maturity - $+0.45\%$ at $T{=}0.5$ drifting to $+2\%$ at $T{=}3$ (see [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/05-failure-modes-and-practice|05 · Failure Modes]]). It is a *short-maturity* tool; long-dated Americans should use BS-2002 or a tree.
2. **The critical price must actually be found.** BAW's $S^*$ is a Newton root of a transcendental equation; bad seeds or loose tolerance move the answer by more than the approximation error. Use robust bracketing and a tight tolerance.
3. **Wrong branch when $b\ge r$.** For a call with $b\ge r$ (no dividend / futures/forward-type carry) BAW *is* the European formula - assembling the premium branch there double-counts value.
4. **Applying the put formula where the transformation belongs.** Haug tabulates calls; puts come via $P(S,X,T,r,b,\sigma)=C(X,S,T,r-b,-b,\sigma)$. Mixing signs ($r-b$ vs $b-r$) is the classic transcription error, and it silently shifts the boundary.
5. **Perpetual formulas misused for long-but-finite maturity.** The perpetual put ignores the approach to maturity, where the boundary collapses to $K$; it *overstates* the value of a $T{=}5$ option unless the extra early-exercise value is genuinely there.

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, Ch 3 - §3.1 BAW (Table 3-1, $1.8771$ / $15.5689$), §3.2 BS-1993, §3.3 BS-2002 (Table 3-2), §3.4 put-call transformation, §3.5 perpetual (Table 3-3, $20.7939$). *All numerically verified in the corpus.*
- **Shreve**, *Stochastic Calculus for Finance II*, §8.3 (perpetual put 8.3.12–8.3.14, linear-complementarity 8.3.18–8.3.20). *Math-verified.*
- **Björk**, *Arbitrage Theory in Continuous Time*, §21.6.3 (perpetual put Prop 21.30, $b=\gamma K/(1+\gamma)$). *Math-verified.*
- **Barone-Adesi, G. & Whaley, R.** (1987), *Efficient analytic approximation of American option values*, JF 42(2). **Bjerksund, P. & Stensland, G.** (1993, 2002), NHH working papers.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/02-optimal-stopping-theory|02 · Optimal-Stopping Theory]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/05-failure-modes-and-practice|05 · Failure Modes]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · Pricing Formulas]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
