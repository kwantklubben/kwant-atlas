---
title: "M.8.1 Numerical Methods from Zero"
tags:
  - foundations
  - numerical-methods
  - intuition
  - error-analysis
---

**Basic Prerequisites:** High-school calculus and a first course in linear algebra.

---

### 1. Intuition & Practical Objective

This page builds the *why* of numerical methods with **no prior numerical knowledge needed**. The objective is one idea: **a numerical answer is an approximation with a known budget, and the whole discipline is about controlling that budget.**

Start with the dumbest question: *why not just use the formula?* Because most of the time there is none. There is no closed form for $\int e^{-x^2}dx$, for the root of $x=\cos x$, for the eigenvalues of a $200\times200$ matrix, or for the solution of a free-boundary PDE. The formula book ends precisely where real problems begin. So instead of an exact answer we manufacture an **approximate one whose error we can bound**.

Three steps, three "aha"s:

1. **Approximation is unavoidable - so measure it.** A computer cannot store $\pi$; it stores $\pi$ to ~16 digits. Every operation inherits that limit. The goal is never zero error; it is an error *small enough for the decision at hand*, provably.

2. **There is always a trade-off knob.** Refine the mesh, add samples, take another iteration - each buys accuracy at a cost. The *quality* of a method is the **rate** at which the error falls (its **order** $p$), not any single number.

3. **Some problems are ill-posed for *any* algorithm.** If the answer changes wildly under a tiny change in the input, no cleverness helps - that is **conditioning**, a property of the *problem*, separate from the *algorithm*.

---

### 2. Mathematical Ground Truth & Derivations

**The four sources of numerical error.** Every wrong digit you will ever see comes from one of these:

| Source | Symbol | Origin | How it shrinks |
|---|---|---|---|
| Truncation (discretisation) | $\tau$ | replacing a limit/integral by a finite sum | $\to0$ as mesh $h\to0$, like $O(h^p)$ |
| Round-off | $\epsilon$ | finite floating-point precision ($\epsilon_{\text{mach}}\approx2.2\times10^{-16}$) | $\to$ **grows** as $h\to0$, like $O(\epsilon/h^m)$ |
| Statistical (sampling) | $s_f/\sqrt n$ | estimating an expectation by $n$ random draws | $O(n^{-1/2})$ |
| Model error | - | the equations are wrong | never - fix the model |

**Order of accuracy.** A method has order $p$ if its error $E(h)=O(h^p)$, i.e. $\lim_{h\to0}E(h)/h^p$ is finite and non-zero. Concretely: **halving $h$ divides the error by $2^p$.** So an $O(h)$ method gains one binary digit per halving, an $O(h^2)$ method gains two. The Taylor expansion is the engine:

$$
f(a+h)=f(a)+hf'(a)+\tfrac{h^2}{2!}f''(a)+\tfrac{h^3}{3!}f'''(a)+\cdots
$$

(Duffy eq. 6.6), so any difference formula is the exact derivative *plus* a remainder whose leading power is the order.

**The central limit/consistency/stability triangle.** For discretising a well-posed differential problem the governing theorem (Duffy Thm 8.1) is:

$$
\underbrace{\text{consistency}}_{\text{truncation error}\to0}\;+\;\underbrace{\text{stability}}_{\|Q^n\|\le K\text{, uniformly}}\;\Longleftrightarrow\;\underbrace{\text{convergence}}_{\|U^n-u\|\to0}.
$$

**Lax equivalence:** a *consistent* scheme converges **iff** it is *stable*. Consistency is usually easy (Taylor); **stability is the hard part**, and it depends on the mesh, not just the stencil.

**Conditioning vs stability - keep them apart.** Conditioning $\kappa$ is a property of the *problem*: for $Ax=b$,

$$
\frac{\|\delta x\|}{\|x\|}\;\le\;\kappa(A)\,\frac{\|\delta b\|}{\|b\|},\qquad \kappa(A)=\|A\|\,\|A^{-1}\|.
$$

A large $\kappa$ means the answer is *inherently* sensitive; no algorithm can beat it. Stability is a property of the *algorithm* - whether errors introduced during computation stay bounded. **An algorithm can be numerically stable on an ill-conditioned problem and still return few correct digits** (the digits were destroyed by the conditioning, page 05).

**Round-off vs truncation - the optimal step.** For a difference with truncation $C_1 h^p$ and round-off $C_2\epsilon/h^m$:

$$
E(h)\;\approx\;C_1h^p+\frac{C_2\epsilon}{h^m}\quad\Longrightarrow\quad h^*\sim \epsilon^{1/(p+m)},\qquad E(h^*)\sim\epsilon^{\,p/(p+m)}.
$$

For the centred difference ($p=2$ truncation, $m=1$ round-off) this gives $h^*\sim\epsilon^{1/3}\approx6\times10^{-6}$, matching the §3 experiment (floor near $h\approx10^{-5}$); a *one-sided* (first-order, $p=1$) difference would give the larger step $h^*\sim\sqrt{\epsilon}\sim10^{-8}$. For the second difference Conte & de Boor quote $h\approx0.0033$ - the empirical optimum.

---

### 3. Computational Implementation - the round-off/truncation valley

The single most instructive experiment in numerical analysis: differentiate $e^x$ at $x=0$ by a centred difference. Watch the error fall as $h$ shrinks - and then *rise again*.




Read the shape: from $h=10^{-2}$ to $h=10^{-5}$ the error falls like $h^2$ (as theory predicts - $1.67\times10^{-9}\to1.21\times10^{-11}$ is ~$100\times$ over a $10\times$ reduction, i.e. order 2), reaches its floor around $h\approx10^{-5}$, and then round-off takes over - by $h=10^{-16}$ the "derivative" is $1.00$ off. **The algorithm did not change; the regime did.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Smaller step is always better."** False. Below $h^*\sim\epsilon^{1/(p+m)}$ the subtraction $f(a+h)-f(a-h)$ catastrophic-cancels and round-off *amplifies* like $1/h$. This is the round-off valley of the experiment above (Conte & de Boor, Duffy §6.3).
2. **Confusing conditioning with stability.** Ill-conditioning ($\kappa\gg1$) is the *problem's* fault and is not fixable by algorithm choice; instability is the *algorithm's* fault and is fixable. Diagnosing the wrong one wastes the effort (page 05).
3. **Assuming order implies accuracy.** An $O(h^2)$ method with a huge constant can be *worse* at practical $h$ than an $O(h)$ method - big-$O$ is an asymptotic promise, not a guarantee at finite $h$.
4. **Forgetting the fourth error.** Choosing a beautiful discretisation of the *wrong* PDE is still wrong. Numerical error is the smallest of your worries if the model is misspecified.
5. **Trusting a single grid.** A number from one mesh has no error bar. Always refine *and check the order*: compute at $h$ and $h/2$ and verify the error ratio matches $2^p$ - the standard **grid-convergence check** (Richardson, Duffy §6.5).

---

### 5. Canonical Literature & Study References

- **Duffy**, *Finite Difference Methods in Financial Engineering*, Ch 6 (§6.3 round-off/truncation trade-off, optimal $h$; §6.5 Richardson extrapolation) and Ch 8 (consistency, stability, convergence, Lax).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 1 (§1.1 estimator and error; §1.1.3 the asymptotic MSE framework $O(s^{-\beta/(2\beta+\eta)})$).
- **Nocedal & Wright**, *Numerical Optimization*, Ch 1–2 (orders of convergence, floating-point arithmetic).
- **Golub & Van Loan**, *Matrix Computations*, Ch 2 (floating-point error, conditioning).

---

### 6. Connected Graph Bridges

- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]]
- Continue: [[foundations/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] · [[foundations/numerical-methods/index|Index Hub]]
- Cross-link: [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|Pricing · From Zero]]
