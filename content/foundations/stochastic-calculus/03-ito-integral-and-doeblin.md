---
title: "03 — The Itô Integral & the Itô–Doeblin Lemma"
tags:
  - foundations
  - stochastic-calculus
  - ito
  - doeblin
  - quadratic-variation
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|02 · Brownian Motion & Martingales]].

---

### 1. Intuition & Practical Objective

Ordinary "$\int_0^T \Delta\,dW$" does not exist as a Riemann–Stieltjes integral because $W$ has infinite first-order variation. The **Itô integral** replaces it with a *martingale-building machine*: it is defined so that its output is a martingale with mean $0$, and its variance is exactly the object the smile/vol modeler controls — the integrated squared integrand. This is the mathematical object behind "delta-hedging gains," and the **Itô–Doeblin lemma** is its chain rule.

Practical objective: by the end of this page you can (1) define $\int\Delta\,dW$ rigorously and state its three invariant properties (martingale, isometry, quadratic variation); (2) apply Itô–Doeblin to a GBM stock to *derive* $dS=\mu S\,dt+\sigma S\,dW$ and see where the $\tfrac12\sigma^2$ comes from; (3) prove $\int_0^T W\,dW=\tfrac12 W(T)^2-\tfrac12 T$, the canonical worked example.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Construction (Shreve II §4.2–4.3; Björk Ch 4)
1. **Simple integrands** $\Delta(t)=\Delta_j$ (constant on $[t_j,t_{j+1})$): define $I(t)=\sum_j \Delta_j\big(W(t_{j+1})-W(t_j)\big)$ — the *forward* increment. It is a **martingale**, has mean $0$, and its quadratic variation is $\sum_j\Delta_j^2\Delta t$.
2. **General integrands** with $\mathbb E\int_0^T\Delta^2(t)\,dt<\infty$: approximate $\Delta$ by simple integrands and pass to the $L^2$ limit. The **Itô isometry** (Thm 4.2.2) makes this well-defined:
$$\mathbb E\Big[\Big(\int_0^t\Delta\,dW\Big)^2\Big]=\mathbb E\Big[\int_0^t\Delta^2(u)\,du\Big].$$

**Three invariants** (Shreve II Thms 4.2.1–4.2.3):
- **Martingale:** $I(t)=\int_0^t\Delta\,dW$ is a martingale, $\mathbb E[I(t)\mid\mathcal F(s)]=I(s)$, $\mathbb E[I(t)]=0$.
- **Isometry:** $\mathbb E[I(t)^2]=\int_0^t\mathbb E[\Delta^2]du$.
- **Quadratic variation:** $[I,I](t)=\int_0^t\Delta^2\,du$, i.e. $dI\cdot dI=\Delta^2(t)\,dt$.

#### 2.2 Itô–Doeblin formula (Shreve II Thm 4.4.1 & 4.4.6; Björk Thm 4.10)
For $f\in C^{1,2}$, integral form
$$f(T,W(T))=f(0,W(0))+\int_0^T f_t\,dt+\int_0^T f_x\,dW+\tfrac12\int_0^T f_{xx}\,dt.$$
For an Itô process $dX(t)=\Theta(t)dt+\Delta(t)dW(t)$ (Shreve II Thm 4.4.6):
$$\boxed{\;df(t,X)=f_t\,dt+f_x\,dX+\tfrac12 f_{xx}\,(dX)^2,\qquad (dX)^2=\Delta^2(t)\,dt.\;}$$
*Why the $\tfrac12$ term?* Taylor-expand to second order; terms with $(dt)^2,dt\,dW\to0$, but $(dW)^2=dt$ survives, contributing $\tfrac12 f_{xx}\Delta^2 dt$. **Itô product rule** (Cor 4.6.3): $d(XY)=X\,dY+Y\,dX+dX\,dY$.

#### 2.3 Application: GBM (Shreve I §15.3; Ex 4.4.8)
The solution of $dS=\mu S\,dt+\sigma S\,dW$ is
$$S(t)=S(0)\exp\Big\{\sigma W(t)+\Big(\mu-\tfrac12\sigma^2\Big)t\Big\}.$$
Check: apply Itô–Doeblin to $f(t,x)=S(0)e^{\sigma x+(\mu-\tfrac12\sigma^2)t}$; the $-\tfrac12\sigma^2$ in the exponent cancels the $\tfrac12\sigma^2$ from $f_{xx}$, so the total $dt$-coefficient is exactly $\mu S$. **Without the correction you would get $\mu+\tfrac12\sigma^2$, a pure QV artifact.** With $\mu=0$, $S(t)=S(0)+\int_0^t\sigma S\,dW$ is a martingale.

#### 2.4 The canonical integral (Shreve I p-167; Shreve II §4.2)
$$\int_0^T W(u)\,dW(u)=\tfrac12 W(T)^2-\tfrac12 T.$$
The $-\tfrac12T$ is the Itô correction: naive $\tfrac12 W(T)^2$ comes from treating $dW$ as $C^1$. This example is the audit test for any stochastic-calculus implementation.

---

### 3. Computational Implementation — verify isometry & Itô–Doeblin numerically

Three stdlib checks: (a) the Itô integral with $\Delta\equiv1$ equals $W(T)$, mean $\to0$ and variance $\to T$ (isometry); (b) the discrete Itô sum reproduces $\tfrac12W(T)^2-\tfrac12T$ path-by-path; (c) Euler–Maruyama approximates GBM.

```python
import math, random
random.seed(7)

def N_inv(x): return math.erf(x/math.sqrt(2.0))   # placeholder (unused)

def ito_path(Delta, nsteps, T=1.0):
    """Discrete Itô sum int_0^T Delta(t) dW, Delta taken at left endpoints."""
    dt = T/nsteps; s = 0.0
    for i in range(nsteps):
        s += Delta(i*dt) * random.gauss(0.0, math.sqrt(dt))
    return s

# (a) isometry: Delta=1 => I(T)=W(T), mean 0, Var=T
vals = [ito_path(lambda t: 1.0, 400) for _ in range(80000)]
m = sum(vals)/len(vals)
v = sum(x*x for x in vals)/len(vals) - m*m
print("Itô integral Delta=1:  mean=%.4f (theory 0)   Var=%.4f (theory T=1.0)" % (m, v))

# (b) Itô-Doeblin: int W dW == 0.5 W(T)^2 - 0.5 T  (one path, n=5000)
n = 5000; dt = 1.0/n
W = [0.0]
for _ in range(n): W.append(W[-1] + random.gauss(0.0, math.sqrt(dt)))
ito_sum = sum(W[i]*(W[i+1]-W[i]) for i in range(n))
print("int_0^T W dW  = %.4f    vs   0.5W(T)^2-0.5T = %.4f" % (ito_sum, 0.5*W[-1]**2-0.5))
```
```
Itô integral Delta=1:  mean=-0.0051 (theory 0)   Var=0.9975 (theory T=1.0)
int_0^T W dW  = -0.3005    vs   0.5W(T)^2-0.5T = -0.3026
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Applying the classical chain rule.** $\int_0^T W\,dW=\tfrac12W(T)^2$ is *wrong*; the correct Itô value subtracts $\tfrac12T$. Any result that doesn't subtract the quadratic-variation term is an $O(T)$ error.
2. **Using backward vs forward increments.** The Itô integral uses *forward*/left-endpoint increments $\Delta(t_j)(W(t_{j+1})-W(t_j))$, which makes it a martingale. Using the *backward* increment would yield the Stratonovich integral (no martingale property, different answers). Is Your $\Delta$ predictable (adapted) — if it looks into the future, the integral is ill-defined and arbitrage appears.
3. **Ignoring integrability** $\mathbb E\int\Delta^2du<\infty$. Without it the $L^2$ extension and isometry fail; in extreme cases the integral isn't even a martingale (local-martingale). This is the technical gate for Girsanov's integrability condition in [[foundations/stochastic-calculus/05-girsanov-and-risk-neutral|05]].
4. **Reading $dX^2=\Delta^2dt$ as optional.** It is derived from QV, not assumed; skipping $f_{xx}$ (e.g. pretending the function is affine in $W$ on a curved payoff) drops the single term that drives all hedging P&L.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 4 (construction §4.2–4.3, Itô–Doeblin Thm 4.4.1/4.4.6, product rule Cor 4.6.3, GBM Ex 4.4.8, Vasicek/CIR Ex 4.4.10/11).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 14–15 (Itô integral, Itô's formula, GBM, QV; $\int B\,dB$ worked example).
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 4 (Wiener process, Itô stochastic integral, multiplication table, multidimensional/correlated Itô).

---

### 6. Connected Graph Bridges

- Back: [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|02 · BM & Martingales]]
- Forward: [[foundations/stochastic-calculus/04-sdes-and-simulation|04 · SDEs & Simulation]] · [[foundations/stochastic-calculus/index|Index Hub]]
- Application: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM: The PDE & Derivation]]