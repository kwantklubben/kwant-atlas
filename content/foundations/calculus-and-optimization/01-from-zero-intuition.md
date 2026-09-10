---
title: "01 — Calculus & Optimization from Zero: What a Derivative Really Is"
tags:
  - foundations
  - calculus
  - intuition
  - derivative
---

**Basic Prerequisites:** none. This page assumes only arithmetic and the idea of a function.

---

### 1. Intuition & Practical Objective

This page builds the *why* of calculus with **no prior knowledge needed**, and it builds it around the one idea everything else extends: **a derivative is the best straight-line approximation of a curve at a point.** Not a formula, not a slope symbol — an *approximation device*. Once you see that, the rest of this folder (gradients, Taylor expansions, optimisation) is just the same idea applied to more variables and more terms.

The dumbest question first: *what is calculus for?* Three things, and finance needs all three.

1. **Sensitivity ("if I nudge the input, how much does the output move?").** If the stock moves \$1, how much does the option move? That ratio *is* a derivative, and it has a name on a trading desk: delta. Every Greek is a derivative.
2. **Optimisation ("where is the output best?").** At the top of a smooth hill the ground is flat: the derivative is zero. That statement — *interior optimum ⇒ derivative zero* (Fermat's principle) — is the seed of every portfolio optimisation, every model fit, every calibration.
3. **Accumulation ("what do the nudges add up to?").** Summing infinitely many tiny contributions is integration, and that is how a payoff times a probability density becomes an expected value.

Three "aha"s before the formal section:

- **The derivative is a *local* linear model, not a global one.** Saying "$f'(2)=12$" means: *near* $2$, $f(x)\approx f(2)+12(x-2)$. Far away the line is useless. This locality is exactly why hedging is a *small-move* activity and why a delta hedge breaks on a gap.
- **"Only the first derivative" is a choice, not a law.** A straight line (first derivative) is the simplest model; adding curvature (the second derivative, the Hessian) gives the delta–gamma expansion. Higher derivatives are *more accurate over a wider neighbourhood*.
- **Fermat's principle is the whole of static optimisation.** At an interior maximum or minimum a differentiable function has zero slope. Everything from "set the gradient to zero" to the KKT conditions is this one fact, constrained and generalised.

---

### 2. Mathematical Ground Truth & Derivations

**The derivative as a limit.**

$$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}.$$

The fraction on the right is the *slope of a secant line* through $(x,f(x))$ and $(x+h,f(x+h))$. As $h\to0$ the secant pivots toward the tangent; its limit $f'(x)$ is the tangent slope. Rearranged, this gives the **local linear approximation**

$$f(x+h)\ \approx\ f(x)+f'(x)\,h\quad\text{for small }h,\qquad f(x+h)-f(x)-f'(x)h=o(h).$$

Bernstein's *Calculus for Mathematicians* makes the local-linearity definition primary (the **Carathéodory** form): $f$ is differentiable at $c$ iff there is a function $f_1$, continuous at $c$, with

$$f(x)=f(c)+(x-c)\,f_1(x),\qquad\text{and then } f'(c)=f_1(c).$$

This is equivalent to the limit definition and is the cleanest parent of the multivariable total derivative on [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable Calculus]].

**The derivative is linear (the rules).** From the definition follow the sum, product, quotient and **chain rules**:

$$(f+g)'=f'+g',\qquad (fg)'=f'g+fg',\qquad \left(\tfrac{f}{g}\right)'=\frac{f'g-fg'}{g^2},\qquad (f\circ g)'=(f'\circ g)\cdot g'.$$

The chain rule is the mathematical engine of finance: if the option value is $V(S)$ and the stock follows $S(t)$, then $\frac{dV}{dt}=V'(S(t))\,S'(t)$ — sensitivities compose. It is what makes "the derivative of the payoff with respect to spot" computable at all.

**Why a flat point is an optimum (Fermat).** If $f'(x^\*)>0$ then a small step left decreases $f$; if $f'(x^\*)<0$ a small step right decreases it. Hence at an interior minimum (or maximum) of a differentiable $f$:

$$\boxed{\,f'(x^\*)=0\,}\qquad\text{(first-order condition).}$$

This is **necessary, not sufficient**: $f(x)=x^3$ has $f'(0)=0$ at a point that is neither max nor min. Sufficiency needs the second derivative — $f''(x^\*)>0$ for a min, $f''(x^\*)<0$ for a max — which is the one-variable case of the Hessian test on page 03.

**The mean value theorem (the workhorse).** For $f$ continuous on $[b,c]$ and differentiable on $(b,c)$, there is an $x\in(b,c)$ with

$$f(c)-f(b)=f'(x)(c-b).$$

It converts a statement about a *change in values* into a statement about a *derivative*, and it is the reason finite-difference approximations of derivatives have a controlled error: the secant slope equals the tangent slope at *some* intermediate point.

**Integration and the FTC.** The definite integral $\int_b^c f$ is the limit of Riemann sums over finer and finer tagged divisions. Its centrepiece is the **Fundamental Theorem of Calculus**: for differentiable $f$,

$$\int_b^c f'(x)\,dx=f(c)-f(b).$$

Differentiation and integration are inverse operations. In finance this identity is why a *density* integrates to a *probability* and why discounted expected payoffs are well-defined integrals.

---

### 3. Computational Implementation — the derivative *is* the limit, and floating point has a floor

Two experiments, stdlib only. First, watch the difference quotient converge to the true derivative as $h$ shrinks — and then watch it *fall apart* as $h$ becomes too small.

```python
import math

def forward_diff(f, x, h):  return (f(x + h) - f(x)) / h
def central_diff(f, x, h):  return (f(x + h) - f(x - h)) / (2*h)

f, fp, x0 = (lambda x: x**3), (lambda x: 3*x*x), 2.0     # f'(2) = 12
print("forward difference  (f(2+h)-f(2))/h :")
for h in (1.0, 1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-12, 1e-16):
    d = forward_diff(f, x0, h)
    print(f"  h={h:8.0e}  approx={d:.10f}  error={abs(d-fp(x0)):.2e}")
print("centred difference  (f(2+h)-f(2-h))/(2h) :")
for h in (1e-1, 1e-3, 1e-5, 1e-6, 1e-8, 1e-10):
    d = central_diff(f, x0, h)
    print(f"  h={h:8.0e}  approx={d:.12f}  error={abs(d-fp(x0)):.2e}")
```
```
forward difference  (f(2+h)-f(2))/h :
  h=   1e+00  approx=19.0000000000  error=7.00e+00
  h=   1e-01  approx=12.6100000000  error=6.10e-01
  h=   1e-02  approx=12.0601000000  error=6.01e-02
  h=   1e-04  approx=12.0006000100  error=6.00e-04
  h=   1e-06  approx=12.0000060022  error=6.00e-06
  h=   1e-08  approx=11.9999999271  error=7.29e-08
  h=   1e-12  approx=12.0010668070  error=1.07e-03
  h=   1e-16  approx=0.0000000000  error=1.20e+01
centred difference  (f(2+h)-f(2-h))/(2h) :
  h=   1e-01  approx=12.010000000000  error=1.00e-02
  h=   1e-03  approx=12.000000999998  error=1.00e-06
  h=   1e-05  approx=12.000000000212  error=2.12e-10
  h=   1e-06  approx=12.000000000789  error=7.89e-10
  h=   1e-08  approx=11.999999882661  error=1.17e-07
  h=   1e-10  approx=12.000000992884  error=9.93e-07
```

**Read the table.** The forward difference's error falls linearly in $h$ (halving $h$ halves the error) until round-off takes over at $h\approx10^{-8}$; at $h=10^{-16}$ the subtraction $f(2+h)-f(2)$ cancels to nothing and the estimate is pure noise. The **centred** difference is second-order (error $\sim h^2$), reaching $\sim2\times10^{-10}$ at $h=10^{-5}$ — then *rising again* as round-off, $\sim\epsilon/h$, dominates. There is an optimal $h^\*$ where truncation meets round-off; shrinking past it makes the answer worse. That is a *first-principles* fact about floating point, not a coding bug, and it is why every practical Greek is computed with a *sensibly-sized* bump, not an infinitesimal one.

Second, the local linear model in action:

```python
f, fp = (lambda x: x**3), (lambda x: 3*x*x)
x0, h = 2.0, 0.1
print(f"f(2.1)          = {f(2.1):.6f}")
print(f"linear model    = {f(x0)+fp(x0)*h:.6f}   (f(2)+f'(2)*0.1)")
print(f"approximation error = {abs(f(2.1)-(f(x0)+fp(x0)*h)):.6f}")
```
```
f(2.1)          = 9.261000
linear model    = 9.200000   (f(2)+f'(2)*0.1)
approximation error = 0.061000
```

The straight line misses by $0.061$ over a step of $0.1$ — the miss is the *curvature*, the piece a second-order (Hessian/Taylor) model would capture (page 03).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The derivative is the slope everywhere" — no, it is local.** A delta of $0.5$ is exact only for infinitesimal moves. Over a finite move the *correct* change includes the second-order term $\tfrac12\Gamma(\Delta S)^2$; ignoring it is the delta–gamma hedging error (see [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · Failure Modes]]).
2. **Setting the derivative to zero finds *all* stationary points, including saddles.** Fermat's condition is necessary; without the sign of $f''$ you can hand back a point that is neither a max nor a min.
3. **The round-off floor is real.** As the first experiment shows, "just make $h$ tiny" is exactly backwards: below $h\approx10^{-5}$ the centred difference gets *worse*. Numerically, accuracy is a trade-off, never a limit you can take.
4. **Differentiability is an assumption, not a guarantee.** Payoff functions like $\max(S-K,0)$ have a *kink* at $S=K$; the derivative does not exist there (it jumps from $0$ to $1$). That single kink is why the gamma of an option spikes at the strike and why the second derivative is where the analytic trouble lives.
5. **The chain rule only composes *reasonable* functions.** $\frac{d}{dt}f(x(t))=\nabla f^\top x'(t)$ requires differentiability of *both*; a pathology in the inner path (a jump, a non-differentiable curve) breaks the composition — the seed of the Itô correction when the path is Brownian.

---

### 5. Canonical Literature & Study References

- **Bernstein, D. J.**: *Calculus for Mathematicians* (1997 draft), §§1–5 (continuity, Carathéodory derivatives, completeness, mean value theorem, Kurzweil–Henstock integration). *The internal foundation note; single-variable and proof-based.*
- **Spivak, Michael**: *Calculus* (4th ed.) — Part II–III (limits, derivatives, the mean value theorem, the Taylor polynomial and its remainder) and Part IV (the integral). *The rigorous single-variable treatment of exactly this page.*
- **Stewart, Clegg & Watson**: *Calculus: Early Transcendentals* (9th ed.) — Ch 2–4 (limits, derivatives, applications of differentiation). *The readable companion.*
- **Simon & Blume**: *Mathematics for Economists* — Ch 1–3 (one-variable calculus: derivative for graphing, convexity, second-order conditions, maxima and minima, chain rule). Ch 3.5 gives the one-variable FOC/SOC directly in the economics framing used throughout this folder.

---

### 6. Connected Graph Bridges

- Next: [[foundations/calculus-and-optimization/02-single-variable-calculus|02 · Single-Variable Calculus]] · [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable Calculus]] · [[foundations/calculus-and-optimization/index|Index Hub]]
- Applied: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] (why delta, gamma and theta are derivatives)
- Base: [[foundations/linear-algebra-and-matrices|Linear Algebra & Matrices]]
