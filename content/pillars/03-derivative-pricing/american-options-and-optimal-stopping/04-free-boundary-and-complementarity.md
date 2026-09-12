---
title: "3.6.4 The Free Boundary & the Linear-Complementarity Problem"
tags:
  - pillar-derivative-pricing
  - american-options
  - free-boundary
  - variational-inequality
  - linear-complementarity
  - smooth-pasting
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/02-optimal-stopping-theory|02 · Optimal-Stopping Theory]] and [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · The PDE]].

---

### 1. Intuition & Practical Objective

The practical objective: write the American option as a **well-posed boundary-value problem** whose unknown is a *function* (the value) and a *curve* (the exercise boundary), and see why the two clean formulations - variational inequality and linear complementarity - are what a numerical solver actually implements.

The awkwardness is the free boundary $S^*(t)$. On the "continue" region the value solves the BSM PDE; on the "exercise" region it equals intrinsic. The two regions are separated by a curve *we do not know*. Three ways to tame it:

1. **Guess the boundary, solve, enforce tangency.** Solve the PDE on $[S^*, \infty)$ with $v(S^*)=K-S^*$; then impose **smooth pasting** $v_S(S^*)=-1$ to pin $S^*$. This is exactly the perpetual case, where it is closed-form. *(This is how we solve the perpetual put in [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/03-analytic-approximations|03 · Analytic Approximations]].)*
2. **Variational inequality (VI).** State a single inequality that encodes "value ≥ payoff" **and** "waiting is not profitable" simultaneously - no explicit boundary.
3. **Linear complementarity (LCP).** The pointwise algebraic form of the VI: at every $(t,S)$, either the value is above the payoff (and the PDE holds), or the value *equals* the payoff (and the PDE inequality is slack). This is the form PSOR and penalty methods solve.

> **One sentence.** "American pricing = solve the BSM operator subject to $V\ge$ payoff and making the residual complementary to the constraint - the boundary is whatever curve that complementarity implies."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The free-boundary formulation (Shreve II §8.4; Björk Prop 21.27)

Let $\mathcal L$ be the BSM operator, $\mathcal L V = \tfrac{\partial V}{\partial t}+rS\tfrac{\partial V}{\partial S}+\tfrac12\sigma^2S^2\tfrac{\partial^2 V}{\partial S^2}-rV$. On the continuation region $\mathcal C=\{(t,S):V(t,S)>$ intrinsic$\}$:

$$
\mathcal L V=0\quad\text{in }\mathcal C,\qquad V(t,S)=\text{intrinsic on }\partial\mathcal C,\qquad V(T,S)=\text{intrinsic}.
$$

The boundary $\partial\mathcal C$ is the free boundary $S^*(t)$ (a curve rising to $K$ at $t=T$ for the put). Two conditions hold **across** it:

$$
\underbrace{V(t,S^*)=K-S^*}_{\text{value matching}},\qquad \underbrace{\frac{\partial V}{\partial S}(t,S^*)=-1}_{\text{smooth pasting}}.
$$

$V$ and $V_S$ are continuous across $\partial\mathcal C$; $V_{SS}$ **jumps**. Only $C^1$ regularity is required - smooth pasting is a *choice* (the "smooth fit" heuristic) that the correct solution satisfies, not an assumption.

#### 2.2 The variational inequality (Björk Prop 21.25/21.26; Shreve II 8.3.18–8.3.20)

In the perpetual put the three conditions combine into a single statement with $\mathcal LV := rV-rSV_S-\tfrac12\sigma^2S^2V_{SS}$ (the **negative** of the BSM operator):

$$
\text{(i) }V(x)\ge (K-x)^+\ \forall x;\qquad \text{(ii) }\mathcal LV(x)\ge0\ \forall x;\qquad \text{(iii) at each }x\text{, equality holds in (i) or (ii)}.
$$

The unique bounded $C^1$ function satisfying all three is the value $v_{L^*}$ of [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/03-analytic-approximations|03]]. In the continuation region $\mathcal LV=0$; in the exercise region $V'=V''=0$, $V=K-x$ so $\mathcal LV=rK>0$. The probabilistic twin (Shreve II Thm 8.3.5, Cor 8.3.6): $e^{-rt}v_{L^*}(S_t)$ is a **supermartingale**, and is a **martingale** when stopped at the first hitting time $T_{L^*}$.

#### 2.3 The linear-complementarity problem (the solver's form)

For a finite-maturity American put on a grid, conditions (i)–(iii) become, at every node $(t_i,S_j)$:

$$
\boxed{\ \min\!\Big(V(t_i,S_j)-\text{intrinsic}(S_j),\ \ \mathcal LV(t_i,S_j)\Big)=0\ }
$$

or equivalently the complementarity system

$$
V\ge g,\qquad \mathcal LV\ge 0,\qquad (V-g)\cdot(\mathcal LV)=0.
$$

Discretise $\mathcal L$ (implicit Euler / Crank–Nicolson) and you get, at each time step, an algebraically messy linear system $AV\ge b$, $V\ge g$, with complementarity $(V-g)^{\!\top}(AV-b)=0$ - solved by **PSOR** (projected SOR) or by a **penalty method** (Duffy Ch 27–29). This is precisely the "1-factor American" row of the numerical-methods scheme table - the implementation detail lives in [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|Numerical Methods · FDM]]; this page owns the *formulation*.

#### 2.4 Why the boundary is where it is - the drift test (Björk Prop 21.28)

It is never optimal to stop where the *payoff alone* is a submartingale: if $\partial_t\Phi+\mu\Phi_x+\tfrac12\sigma^2\Phi_{xx}>0$ then $(t,x)\in\mathcal C$. Intuitively you never exercise while the immediate reward is expected to grow faster than the discounting can erode it - the boundary is pushed out to the point where the two balance.

---

### 3. Computational Implementation - smooth pasting, complementarity and the perpetual limit

Three checks. **(A)** The boundary $L^*$ is the maximiser over constant boundaries of the value - smooth pasting as a first-order condition. **(B)** Long-dated CRR converges to the perpetual closed form. **(C)** The complementarity residual $\min(V-\text{payoff},\mathcal LV)=0$ holds at every $x$, computed by finite differences with the **negative**-BSM convention. Stdlib only.



Read the residual table: on the exercise side ($x=60,75$) the value *equals* payoff (first bracket $=0$) and $\mathcal LV=rK=10>0$; on the continuation side ($x=80,100,130$) the value is *strictly above* payoff and $\mathcal LV=0$ (to finite-difference accuracy). The minimum is zero everywhere - the complementarity system, verified. And the finite-maturity American put climbs monotonically toward the perpetual $13.9719$ as $T\to\infty$, exactly the limit Björk Prop 21.30 predicts.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Sign confusion in the VI.** Shreve writes $\mathcal LV=rV-rSV_S-\tfrac12\sigma^2S^2V_{SS}$, the *negative* of the usual BSM operator; it is $\ge0$ (not $\le$) and equals $rK$ in the exercise region. Writing the wrong sign turns a correct solver into a subtly wrong one with no obvious symptom.
2. **Smooth pasting is a consequence, not an assumption.** Imposing $V_S(S^*)=-1$ *with an otherwise wrong ansatz* produces a boundary that satisfies the tangency but not the PDE - a plausible-looking wrong answer. The VI formulation (no explicit boundary) is the safe statement.
3. **$V_{SS}$ discontinuity breaks naive schemes.** The gamma jump at $S^*$ is precisely what makes Crank–Nicolson ring near the strike; Rannacher startup / extrapolated implicit Euler suppress it ([[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|Numerical Methods · Failure Modes]]).
4. **Freezing the boundary or the "exercise-if-deep-ITM" heuristic.** Both are sub-optimal policies; they return a value *below* the true one and, worse, an inconsistent delta. The boundary must be solved, not guessed.
5. **The free boundary is a full curve, not a point.** For a finite-maturity put $S^*(t)$ rises to $K$ at $t=T$; discretising only the current boundary (a perpetuity) misprices intermediate maturities.

---

### 5. References

- **Shreve**, *Stochastic Calculus for Finance II*
- **Björk**, *Arbitrage Theory in Continuous Time*
- **Duffy**, *Finite Difference Methods in Financial Engineering*
- **Wilmott, Howison & Dewynne**, *The Mathematics of Financial Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/03-analytic-approximations|03 · Analytic Approximations]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/06-advanced-extensions|06 · Advanced Extensions]]
- Implementation (linked, not duplicated): [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|FDM: penalty & PSOR]] · [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · PDE]]
