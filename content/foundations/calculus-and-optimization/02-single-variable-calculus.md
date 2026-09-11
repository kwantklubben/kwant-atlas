---
title: "F.2.2 Single-Variable Calculus"
tags:
  - foundations
  - calculus
  - taylor-series
  - single-variable
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/01-from-zero-intuition|01 · From Zero]] (what a derivative is).

---

### 1. Intuition & Practical Objective

Single-variable calculus is the *reference implementation* of everything that follows. It gives you four tools, and each one has a direct finance job:

1. **Limits** — make sense of "instantaneous" quantities: a continuously-compounded return is the limit of periodic compounding, and the price of a bond as maturity $\to0$ is a limit.
2. **Derivatives** — local sensitivity and the first-order optimality condition (Fermat): "flat $\Rightarrow$ optimum."
3. **Taylor polynomials** — replace a messy function by a polynomial you can compute with. This is *the* expansion behind delta–gamma–theta P&L, duration–convexity, and every "local model" on a desk.
4. **Integration** — turn a density into a probability and a payoff into a price, via the Fundamental Theorem of Calculus.

The one mental model: **Taylor's theorem says every smooth function is a polynomial plus a controlled error.** Stop at degree 1 and you get the tangent (delta). Go to degree 2 and you get curvature (gamma). The remainder term is the *honest* part — it tells you the size of the error you are eating by truncating, and it is exactly the term a trader is exposed to when the market moves more than "a little."

---

### 2. Mathematical Ground Truth & Derivations

**Limits and continuity.** $\lim_{x\to c}f(x)=L$ means $f(x)$ can be made arbitrarily close to $L$ by taking $x$ close enough to $c$. $f$ is **continuous** at $c$ if $\lim_{x\to c}f(x)=f(c)$. The algebra of limits (sums, products, compositions of continuous functions are continuous) lets one compute almost everything without $\epsilon$–$\delta$ arguments. **L'Hôpital's rule** handles the indeterminate $0/0$ form:

$$
\text{if } f(c)=g(c)=0 \text{ and } g'(c)\ne0,\qquad \lim_{x\to c}\frac{f(x)}{g(x)}=\frac{f'(c)}{g'(c)},\qquad\text{(iterated if the ratio is still }0/0\text{).}
$$

Bernstein's note deliberately defines limits *via* continuity (convergence at a point is "the redefined function is continuous there"), which makes L'Hôpital a corollary of the mean value theorem rather than a separate axiom.

**Derivative rules.** From the limit definition: $(f+g)'=f'+g'$, $(fg)'=f'g+fg'$, $(f/g)'=(f'g-fg')/g^2$, $(f\circ g)'=(f'\circ g)g'$, and $(x^n)'=nx^{n-1}$.

**The mean value theorem (MVT).** If $f$ is continuous on $[b,c]$ and differentiable on $(b,c)$, there is $x\in(b,c)$ with

$$
f(c)-f(b)=f'(x)(c-b).
$$

Its corollaries drive optimisation and numerics: $f'\equiv0$ on an interval $\Rightarrow f$ constant; and the secant slope of a finite-difference scheme equals the true derivative at *some* intermediate point, which is what makes truncation-error bounds possible.

**Fermat, Rolle and the second-order test.**

- **Fermat:** an interior extremum of a differentiable $f$ has $f'(x^*)=0$.
- **Rolle:** $f(b)=f(c)$ $\Rightarrow$ some interior point has $f'=0$.
- **Second-order sufficiency:** if $f'(x^*)=0$ and $f''(x^*)>0$, then $x^*$ is a strict local minimum ($f''<0$ $\Rightarrow$ maximum). If $f''(x^*)=0$ the test is inconclusive ($x^3$, $x^4$ at $0$).

**Taylor's theorem with remainder.** For $f$ $(n{+}1)$-times differentiable on an interval containing $a$ and $x$, there is $z$ between them with

$$
f(x)=\underbrace{\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k}_{P_n(x)\ \text{Taylor polynomial}}+\underbrace{\frac{f^{(n+1)}(z)}{(n+1)!}(x-a)^{n+1}}_{R_n(x)\ \text{remainder}}.
$$

The **Lagrange form** of the remainder (Stewart §11.10–11.11; Spivak Part III) is the key to error control: it says the error is "the next term, with the derivative evaluated at some unknown point $z$." For $e^x$ about $0$, $R_n(x)=e^{z}x^{n+1}/(n+1)!$, so on $[0,1]$ the error is bounded by $e/(n{+}1)!$ — a *provable* rate.

The **finance reading**: with $a=S_t$ and $x=S_t+\Delta S$,

$$
V(S_t+\Delta S)=V+\Delta\,\Delta S+\tfrac12\Gamma(\Delta S)^2+\tfrac16\text{Speed}(\Delta S)^3+\cdots,
$$

i.e. the delta–gamma–theta expansion is a Taylor expansion of the pricing function, and truncating at order 1 leaves the gamma term as the *remainder you are exposed to*.

**Integration and the FTC.** The definite integral $\int_b^c f$ is the limit of Riemann sums $\sum f(\xi_i)\Delta x_i$. Linearity and positivity are immediate; the **Fundamental Theorem of Calculus** is

$$
\int_b^c f'(x)\,dx=f(c)-f(b).
$$

Under the Kurzweil–Henstock (gauge) definition used in Bernstein's note, *every* derivative is integrable, so the FTC holds with no extra technical hypotheses — which is why $\mathbb E[f(X)]=\int f\,dF$ always makes sense for the densities finance uses.

---

### 3. Computational Implementation — Taylor convergence, its radius, and the FTC

Stdlib only. Three experiments: (A) truncation error of the Taylor polynomial of $e^x$ shrinking by factorially more digits; (B) the *radius of convergence* — the same series at $x=0.5$ (inside) versus $x=2$ (outside); (C) Riemann sums converging to an integral at rate $O(1/n)$.

```python
import math

# (A) Taylor polynomial of e^x about 0, evaluated at x=1
def taylor_exp(n, x):
    s, term = 0.0, 1.0
    for k in range(n + 1):
        if k > 0: term *= x / k
        s += term
    return s

print("Taylor P_n(1) of e^x about 0, vs e = 2.718281828459045")
for n in (1, 2, 3, 5, 8, 12, 16):
    p = taylor_exp(n, 1.0)
    print(f"  n={n:2d}  P_n(1)={p:.12f}  |error|={abs(p-math.e):.3e}")

# (B) Taylor of log(1+x) about 0: radius of convergence = 1
def taylor_log1p(n, x):
    return sum((-1)**(k+1) * x**k / k for k in range(1, n + 1))
print("\nlog(1+x) series at x=0.5 (inside radius 1):")
for n in (5, 20, 100):
    print(f"  n={n:3d}  P_n(0.5)={taylor_log1p(n,0.5):.10f}  exact={math.log(1.5):.10f}  err={abs(taylor_log1p(n,0.5)-math.log(1.5)):.2e}")
print("  same series at x=2.0 (outside radius -> diverges):")
for n in (5, 20, 100):
    print(f"  n={n:3d}  P_n(2.0)={taylor_log1p(n,2.0):.6e}")

# (C) FTC via left Riemann sums:  int_0^1 x^2 dx = 1/3
def left_riemann(g, a, b, n):
    h = (b-a)/n
    return h * sum(g(a + i*h) for i in range(n))
print("\nint_0^1 x^2 dx  (exact 1/3 =", 1/3, ")")
for n in (10, 100, 1000, 10000):
    L = left_riemann(lambda x: x*x, 0, 1, n)
    print(f"  n={n:6d}  L_n={L:.10f}  err={abs(L-1/3):.3e}")
```
```
Taylor P_n(1) of e^x about 0, vs e = 2.718281828459045
  n= 1  P_n(1)=2.000000000000  |error|=7.183e-01
  n= 2  P_n(1)=2.500000000000  |error|=2.183e-01
  n= 3  P_n(1)=2.666666666667  |error|=5.162e-02
  n= 5  P_n(1)=2.716666666667  |error|=1.615e-03
  n= 8  P_n(1)=2.718278769841  |error|=3.059e-06
  n=12  P_n(1)=2.718281828286  |error|=1.729e-10
  n=16  P_n(1)=2.718281828459  |error|=2.220e-15

log(1+x) series at x=0.5 (inside radius 1):
  n=  5  P_n(0.5)=0.4072916667  exact=0.4054651081  err=1.83e-03
  n= 20  P_n(0.5)=0.4054650927  exact=0.4054651081  err=1.54e-08
  n=100  P_n(0.5)=0.4054651081  exact=0.4054651081  err=0.00e+00
  same series at x=2.0 (outside radius -> diverges):
  n=  5  P_n(2.0)=5.066667e+00
  n= 20  P_n(2.0)=-3.435971e+04
  n=100  P_n(2.0)=-8.422741e+27

int_0^1 x^2 dx  (exact 1/3 = 0.3333333333333333 )
  n=    10  L_n=0.2850000000  err=4.833e-02
  n=   100  L_n=0.3283500000  err=4.983e-03
  n=  1000  L_n=0.3328335000  err=4.998e-04
  n= 10000  L_n=0.3332833350  err=5.000e-05
```

**Read the tables.** (A) The $e^x$ error drops by a factor of ~$1/n$ each extra term — factorial convergence, hitting machine precision (2.2e-15) by $n=16$. This is why "add one more Taylor term" is the cheapest accuracy in all of numerics. (B) The *same* series evaluated at $x=2$ blows up to $-8.4\times10^{27}$: **a Taylor series is only trustworthy inside its radius of convergence** ($|x|<1$ here). Calibrating an expansion too far from the expansion point is a classic modelling error. (C) The Riemann error falls by exactly $10\times$ each time $n$ grows by $10\times$ — the $O(1/n)$ law, made visible.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Truncating a Taylor series is a *choice with a price*, given by the remainder.** Delta hedging keeps only the first term; the *dropped* $\tfrac12\Gamma(\Delta S)^2$ is the whole hedging risk. The Lagrange remainder tells you its size — never expand without asking what you threw away.
2. **The radius of convergence is finite and bites.** As experiment (B) shows, the expansion of $\log(1+x)$ is *exactly* wrong outside $|x|<1$, not merely inaccurate. Local models (delta, duration) are only valid locally; a large move invalidates the expansion, it does not just degrade it.
3. **Fermat is not sufficient.** $f'(x^*)=0$ at $x^*=0$ for $x^3$ (a saddle), $x^4$ (a min) and $-x^4$ (a max). Always run the $f''$ test (and if $f''=0$, higher order) before declaring an optimum.
4. **Differentiability can fail at exactly the interesting point.** $\max(S-K,0)$ has no derivative at $S=K$; its second derivative is a Dirac mass there. Inconsistent-looking Greeks and FDM ringing around the strike are the numerical shadow of this kink.
5. **Integration by quadrature is cursed by dimension.** A left Riemann sum converges at $O(1/n)$ here, the trapezoid at $O(1/n^2)$ — but in $d$ dimensions a tensor-product rule costs $O(n^{-2/d})$, which is why high-dimensional integrals in finance are done by **Monte Carlo** ($O(n^{-1/2})$ in every dimension, Glasserman §1.1) rather than by quadrature.
6. **A 0/0 limit is not automatically "differentiate top and bottom."** L'Hôpital requires the hypotheses ($f(c)=g(c)=0$, differentiability, $g'\ne0$); on non-indeterminate forms it silently returns nonsense.

---

### 5. Canonical Literature & Study References

- **Bernstein, D. J.**: *Calculus for Mathematicians* (1997 draft) — Part 1 (continuity, open balls, $\epsilon$–$\delta$), Part 2 (Carathéodory derivative; sum/product/chain/quotient/power rules), Part 3 (supremum, IVT, max–min-value theorem), Part 4 (Fermat, Rolle, MVT, derivative-zero), Part 5 (Kurzweil–Henstock integral, FTC), Part 6 (limits and L'Hôpital). *The proof-based single-variable backstop for this page.*
- **Spivak, Michael**: *Calculus* (4th ed.) — Ch 5–11 (limits/continuity, differentiation, MVT, the Taylor polynomial, the integral). *The rigorous companion.*
- **Stewart, Clegg & Watson**: *Calculus: Early Transcendentals* (9th ed., 2020) — §11.10 Taylor and Maclaurin Series, §11.11 Applications of Taylor Polynomials (Taylor's inequality with the Lagrange remainder). *Worked-error treatment.*
- **Simon & Blume**: *Mathematics for Economists* — Ch 3 (using the first derivative, second derivatives and convexity, maxima/minima, second-order conditions). *The economics framing of the FOC/SOC.*

---

### 6. Connected Graph Bridges

- Back: [[foundations/calculus-and-optimization/01-from-zero-intuition|01 · From Zero]] · [[foundations/calculus-and-optimization/index|Index Hub]]
- Next: [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable Calculus]] (the same ideas in $\mathbb R^n$)
- Applied: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] (Taylor = delta–gamma) · [[foundations/numerical-methods/02-finite-difference-methods|Finite-Difference Methods]] (MVT-driven truncation error)
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]
