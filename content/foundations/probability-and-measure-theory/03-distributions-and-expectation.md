---
title: "03 — Distributions & Expectation: Random Variables, Laws, Independence"
tags:
  - foundations
  - probability-and-measure-theory
  - random-variables
  - distributions
  - expectation
  - independence
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/02-probability-spaces-and-filtrations|02 · Probability Spaces & Filtrations]].

---

### 1. Intuition & Practical Objective

A random variable is **a function on outcomes**, and its **distribution** is the probability it puts on each value range — two random variables can share a law while being different functions, and one variable can have two laws under two measures (Shreve II Def 1.2.3). "$\mathbb E[h(X)]$" is just the probability-weighted average of $h$ over the law of $X$, computed by the **standard machine** (indicator $\to$ simple $\to$ nonnegative $\to$ general) or, when a density exists, as $\int h(x)f_X(x)\,dx$.

The practical objective: understand the *three linked faces* of a distribution — (1) the law $\mu_X(B)=\mathbb P\{X\in B\}$ and its density; (2) expectation as an integral against the law, computable by **inverse transform** for simulation; (3) **independence** and the crucial fact that uncorrelated $\not\Rightarrow$ independent outside joint normality. This is the vocabulary every simulation (Glasserman Ch 2) and every moment/risk computation uses.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Random variables, laws, densities (Shreve II Def 1.2.3; Shreve I Ch 11)
$X:\Omega\to\mathbb R$ is a random variable if $X^{-1}(B)\in\mathcal F$ for every Borel $B$. Its **law** (distribution measure) is
$$\mu_X(B)=\mathbb P\{X\in B\}=\mathbb P\{X^{-1}(B)\}.$$
$X$ has a **density** $f_X:\mathbb R\to[0,\infty)$ iff $\mu_X(B)=\int_B f_X(x)\,dx$, i.e. iff $\mu_X\ll\text{Leb}$ (absolutely continuous w.r.t. Lebesgue); $f_X$ is the Radon–Nikodym derivative $d\mu_X/dx$ (Shreve I Ch 11). Two random variables sharing a law are *different objects* — "the RV and its distribution are distinct" (Shreve II Def 1.2.3).

#### 2.2 Expectation via the standard machine (Shreve II §1.4; Shreve I Thm 3.32)
$$\mathbb E[h(X)]=\int_\Omega h(X)\,d\mathbb P=\int_{\mathbb R}h(x)\,d\mu_X(x)=\int_{\mathbb R}h(x)f_X(x)\,dx.$$
The construction is inductive: indicator $\to$ simple $\to$ nonnegative $\to$ general (monotone convergence for the nonnegative step), and the limit theorems (MCT, Fatou, DCT) make passing limits through expectations legal.

#### 2.3 Inverse-transform sampling (Glasserman §2.2, eq. 2.13–2.14)
$$X=F^{-1}(U),\qquad F^{-1}(u)=\inf\{x: F(x)\ge u\},\qquad U\sim\text{Unif}[0,1].$$
This needs exactly **one uniform per sample** (minimal dimension — key for QMC) and gives $X=-\theta\log(1-U)\sim\text{Exp}(\theta)$ for the exponential, $\sin^2(U\pi/2)$ for the arcsine, etc. (Glasserman eqs. 2.13–2.14, p-070).

#### 2.4 Independence: sets, $\sigma$-algebras, variables (Shreve II §2.2)
Independent sets: $\mathbb P(A\cap B)=\mathbb P(A)\mathbb P(B)$; random variables independent if $\sigma(X),\sigma(Y)$ are. Criterion (Shreve II Thm 2.2.7(vi)): joint cdf / joint MGF factors. **Uncorrelated $\not\Rightarrow$ independent:** with $X$ standard normal and $Z=\pm1$ equally, $Y=ZX$ is standard normal, $\mathbb E[XY]=\mathbb E[X^2]\mathbb E[Z]=0$ (uncorrelated), yet $X,Y$ are dependent and have **no joint density** (Shreve II §2.2 Example). Only **jointly normal** variables make zero covariance imply independence (components independent iff covariance matrix diagonal, Shreve I §11.8).

---

### 3. Computational Implementation — inverse transform, expectation, and the independence trap

Simulate an exponential by inverse transform and check its mean and survival function; then exhibit the classic uncorrelated-but-dependent pair $Y=ZX$. Stdlib only.

```python
import math, random
random.seed(3)
# inverse-transform exponential X=-theta ln(1-U), theta=2
theta=2.0; N=200000
X=[-theta*math.log(1-random.random()) for _ in range(N)]
surv=sum(1 for x in X if x>2.0)/N
print("inverse-transform Exp(2): E[X]=%.4f (theory 2.0)" % (sum(X)/N))
print("  P(X>2)=%.4f  theory e^{-1}=%.4f" % (surv, math.exp(-1.0)))
# independence vs uncorrelated: X~N(0,1), Z=+-1, Y=ZX
M=200000
Xv=[random.gauss(0,1) for _ in range(M)]
Zv=[1 if random.random()<0.5 else -1 for _ in range(M)]
Yv=[x*z for x,z in zip(Xv,Zv)]
cov=sum(x*y for x,y in zip(Xv,Yv))/M
# dependence lives in the MAGNITUDES: |Y|=|X| exactly, so |X|>1 iff |Y|>1.
mag=sum(1 for x,y in zip(Xv,Yv) if abs(x)>1 and abs(y)>1)/M
pA=sum(1 for x in Xv if abs(x)>1)/M; pB=sum(1 for y in Yv if abs(y)>1)/M
print("uncorrelated: Cov(X,Y)=%.4f (theory 0)" % cov)
print("dependent?  P(|X|>1,|Y|>1)=%.4f vs P(|X|>1)P(|Y|>1)=%.4f" % (mag,pA*pB))
# expectation of a function / standard machine: E[X^2]=1
print("E[X^2]=%.4f (theory 1.0)" % (sum(x*x for x in Xv)/M))
```
```
inverse-transform Exp(2): E[X]=1.9995 (theory 2.0)
  P(X>2)=0.3681  theory e^{-1}=0.3679
uncorrelated: Cov(X,Y)=-0.0044 (theory 0)
dependent?  P(|X|>1,|Y|>1)=0.3166 vs P(|X|>1)P(|Y|>1)=0.1003
E[X^2]=0.9976 (theory 1.0)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing the random variable with its distribution.** Two RVs can share a law (e.g. $X$ and $-X$ for symmetric $X$) yet be different functions; one RV can have two laws under two measures. "Is $X$ normal?" is a statement about its *law*, never about the underlying $\omega$ map (Shreve II Def 1.2.3).
2. **Uncorrelated $\Rightarrow$ independent (the Gaussian-only shortcut).** It holds for *jointly normal* variables and fails almost everywhere else — the $Y=ZX$ example has zero covariance yet no joint density and clear dependence (Shreve II §2.2). This silently breaks factor/portfolio independence assumptions.
3. **Sampling a distribution without a valid generator.** Acceptance–rejection consumes an unbounded number of uniforms per sample, is not monotone in its inputs, and is incompatible with quasi-Monte Carlo; inverse transform is one-uniform-per-sample and monotone (Glasserman §2.2). Using an $O(d^3)$-unstable sampler quietly invalidates the downstream estimator.
4. **Dividing by $\mathbb P(B)$ when $\mathbb P(B)=0$.** The elementary conditional formula collapses on zero-probability conditioning; that is the road into the measure-theoretic conditional expectation ([[foundations/probability-and-measure-theory/04-conditional-expectation|04 · Conditional Expectation]]).

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 1 §1.2 (RV & distribution, Def 1.2.3), §1.4–1.5 (standard machine, MCT/Fatou/DCT), Ch 2 §2.2 (independence, Thm 2.2.7(vi), the uncorrelated-not-independent example).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 11 (law, density, $\mathbb E h(X)=\int h f\,dx$, bivariate & multivariate normal, independence iff diagonal covariance).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 2 (inverse transform, acceptance–rejection, Box–Muller, normal vectors).
- **Casella & Berger**, *Statistical Inference*, Ch 4 (distributions, moments, transformations of RVs) — the classical companion.

---

### 6. Connected Graph Bridges

- Back: [[foundations/probability-and-measure-theory/02-probability-spaces-and-filtrations|02 · Probability Spaces & Filtrations]] · [[foundations/probability-and-measure-theory/index|Index Hub]]
- Forward: [[foundations/probability-and-measure-theory/04-conditional-expectation|04 · Conditional Expectation]] · [[foundations/probability-and-measure-theory/05-martingales|05 · Martingales]]
- Applications: [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]] (tail distributions) · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (normal increments, lognormal prices)
