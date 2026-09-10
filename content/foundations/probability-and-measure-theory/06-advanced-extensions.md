---
title: "06 — Advanced Extensions: Measure Theory, Radon–Nikodym & Convergence Theorems"
tags:
  - foundations
  - probability-and-measure-theory
  - measure-theory
  - radon-nikodym
  - convergence-theorems
  - lebesgue-integral
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/05-martingales|05 · Martingales]].

---

### 1. Intuition & Practical Objective

These are the *foundations of the foundations*: the results that make "expectation" and "conditioning" well-defined and the theorems that let you move limits inside expectations. **Radon–Nikodym** turns one measure into another as a density — the mathematical license for the risk-neutral change of measure. The **convergence theorems** (Monotone, Fatou, Dominated) are why you may stop a martingale and let $t\to\infty$, pass a limit under $\int$, or claim $\frac1n\sum f(U_i)\to\mathbb E[f]$ almost surely (Glasserman §1.1). The **Lebesgue/standard machine** is how expectation itself is built on uncountable spaces.

The practical objective: understand the complete toolkit that (a) proves a conditional expectation exists (via Radon–Nikodym, Shreve I §9.5); (b) makes the change of measure $\mathbb P\to\widetilde{\mathbb P}$ rigorous (Shreve II §1.6; Shreve I Ch 9); (c) justifies every Monte Carlo and every discrete limit — the theoretical reason "it's just an average" is sound.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Radon–Nikodym & change of measure (Shreve II Thm 1.6.1; Shreve I Ch 9)
$\widetilde{\mathbb P}$ is **absolutely continuous** w.r.t. $\mathbb P$ ($\widetilde{\mathbb P}\ll\mathbb P$) if $\mathbb P(A)=0\Rightarrow\widetilde{\mathbb P}(A)=0$. Then there is a nonnegative $Z$ with
$$\widetilde{\mathbb P}(A)=\int_A Z\,d\mathbb P\quad\forall A\in\mathcal F,\qquad Z=\frac{d\widetilde{\mathbb P}}{d\mathbb P}.$$
**Equivalence** ($\widetilde{\mathbb P}\sim\mathbb P$) iff $Z>0$ a.s.; then $1/Z$ is the RN derivative of $\mathbb P$ w.r.t. $\widetilde{\mathbb P}$ and $\mathbb E Y=\widetilde{\mathbb E}[Y/Z]$ (Shreve II Thm 1.6.1; Shreve I Ch 9). **Existence of conditional expectation as a corollary** (Shreve I §9.5): for $X\ge0$ with $\int X\,d\mathbb Q=1$, define $\mathbb P'(A)=\int_A X\,d\mathbb Q$ on a sub-$\sigma$-algebra $\mathcal G$; the RN derivative of $\mathbb P'$ w.r.t. $\mathbb Q$ restricted to $\mathcal G$ is $\mathcal G$-measurable and has the partial-averaging property, so it *is* $\mathbb E[X\mid\mathcal G]$.

On the finite market (Shreve I Ex 9.1), $Z(\omega)=\widetilde{\mathbb P}(\omega)/\mathbb P(\omega)$ gives $Z(HH)=\frac94,\ Z(HT)=Z(TH)=\frac98,\ Z(TT)=\frac9{16}$ (verified), and $Z_k=\mathbb E[Z\mid\mathcal F_k]$ is a $\mathbb P$-martingale; the **state-price density** is $\zeta_k=(1+r)^{-k}Z_k$ with $\zeta_jV_j$ a $\mathbb P$-martingale and European value $V_0=\mathbb E[\zeta_kC_k]$ (Shreve I Ch 9).

#### 2.2 Expectation = the Lebesgue integral & the standard machine (Shreve II §1.4–1.5)
The integral is built on the $y$-axis partition (Lebesgue, not Riemann): indicator $\to$ simple $\to$ nonnegative $\to$ general. Computation via density: $\mathbb E[h(X)]=\int h(x)f_X(x)\,dx$ (Shreve I Thm 3.32); the density is the RN derivative of the law w.r.t. Lebesgue measure.

#### 2.3 The convergence theorems (Shreve II Thms 1.4.5/1.4.9)
- **Monotone Convergence (MCT):** $0\le X_n\uparrow X$ a.s. $\Rightarrow$ $\mathbb E[X_n]\uparrow\mathbb E[X]$.
- **Fatou's Lemma:** $X_n\ge0$ $\Rightarrow$ $\mathbb E[\liminf X_n]\le\liminf\mathbb E[X_n]$.
- **Dominated Convergence (DCT):** $X_n\to X$ a.s. and $|X_n|\le Y$ integrable $\Rightarrow$ $\mathbb E[X_n]\to\mathbb E[X]$.

These justify passing limits through expectations everywhere in Ch 3 — the stopped exponential martingale $Z(t\wedge\tau_m)$ with dominated/monotone convergence yields $P\{\tau_m<\infty\}=1$ and $\mathbb E[\tau_m]=\infty$ (Shreve II Thm 3.6.2, Remark 3.6.3). The SLLN/CLT that run Monte Carlo are themselves consequences (Glasserman §1.1).

#### 2.4 Conditional expectation as $L^2$ orthogonal projection (Shreve II Def 2.3.1)
$\mathbb E[X\mid\mathcal G]$ minimizes $\mathbb E[(X-V)^2]$ over $\mathcal G$-measurable $V$: the residual is orthogonal to every $\mathcal G$-measurable variable, $\mathbb E[(X-\mathbb E[X\mid\mathcal G])\cdot V]=0$. This is the measure-theoretic statement of "best predictor," and the root of the ESL regression function $\mathbb E[Y\mid X=x]$ (ESL eq. 2.13) and its MSE decomposition.

---

### 3. Computational Implementation — verify RN derivative, the projection, and CLT

Check the discrete RN derivative values, the $L^2$ orthogonality of the conditional-expectation residual, and the CLT standard error of an MC estimator. Stdlib only.

```python
import math, random
random.seed(23)
# (1) Radon-Nikodym derivative on 2-toss space (Shreve I Ex 9.1)
p,q,pt,qt=1/3.,2/3.,1/2.,1/2.
Z={}
for h in (0,1,2):
    t=2-h
    P=(p**h)*(q**t); Pt=(pt**h)*(qt**t)
    Z[(h,t)]=Pt/P
print("RN derivative Z=P~/P: Z(HH)=%.4f Z(HT)=%.4f Z(TT)=%.4f (theory 9/4, 9/8, 9/16)"
      % (Z[(2,0)],Z[(1,1)],Z[(0,2)]))
# (2) L2 projection: conditional expectation is orthogonal projection
s1,s2,rho=1.0,1.0,0.7
N=300000
X1=[random.gauss(0,1) for _ in range(N)]
X2=[rho*x1+math.sqrt(1-rho*rho)*random.gauss(0,1) for x1 in X1]
X=[x*x for x in X2]
bins={}
for x1,x in zip(X1,X):
    key=round(x1/0.2)*0.2
    g=bins.setdefault(key,[0,0.0]); g[0]+=1; g[1]+=x
pred={k:g[1]/g[0] for k,g in bins.items() if g[0]>0}
orth=sum((x-pred[round(x1/0.2)*0.2])*x1 for x1,x in zip(X1,X))/N
print("L2 projection: E[(X-E[X|X1])*V(X1)]=%.4f (theory 0)" % orth)
# (3) CLT standard error of the MC estimator (convergence theorems in action)
alpha=2/math.pi
B,k=30000,200
ests=[sum(math.cos(math.pi/2*random.random()) for _ in range(k))/k for _ in range(B)]
m=sum(ests)/B
sdf=math.sqrt(sum((e-m)**2 for e in ests)/(B-1))
sone=math.sqrt(sum((math.cos(math.pi/2*random.random())-alpha)**2 for _ in range(50000))/50000)
print("MC CLT: std of mean(k=200)=%.4f vs sigma/sqrt(k)=%.4f" % (sdf, sone/math.sqrt(k)))
print("MC estimate of alpha=2/pi: %.4f (theory %.4f)" % (m, alpha))
```
```
RN derivative Z=P~/P: Z(HH)=2.2500 Z(HT)=1.1250 Z(TT)=0.5625 (theory 9/4, 9/8, 9/16)
L2 projection: E[(X-E[X|X1])*V(X1)]=0.0001 (theory 0)
MC CLT: std of mean(k=200)=0.0218 vs sigma/sqrt(k)=0.0218
MC estimate of alpha=2/pi: 0.6370 (theory 0.6366)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Missing the absolute-continuity direction.** Radon–Nikodym builds $\widetilde{\mathbb P}$ from a density $Z\ge0$ with $\mathbb E Z=1$; **equivalence** is the *extra* $Z>0$ a.s. assumption (Shreve II Thm 1.6.1). Assuming equivalence when only absolute continuity holds, or vice-versa, silently breaks the inverse density $1/Z$.
2. **Exchanging limit and expectation without a convergence theorem.** $\lim\mathbb E[X_n]=\mathbb E[\lim X_n]$ is false in general; only under MCT (monotone), Fatou (inequality), or DCT (dominated) does it hold (Shreve II §1.4). The stopped-martingale first-passage computation relies exactly on this.
3. **Requiring densities where there are none.** Not every law has a density — $\mu_X\ll\text{Leb}$ is exactly the condition (Shreve I Ch 11). The $Y=ZX$ pair has *no joint density* despite each marginal being normal; forcing one misrepresents the dependence.
4. **Treating the MC average as deterministic.** $\frac1n\sum f(U_i)$ is a random variable whose error is $O(\sigma_f/\sqrt n)$; without SLLN/CLT you cannot justify either convergence or the error bar (Glasserman §1.1).
5. **Confusing measurability with integrability.** A random variable can be $\mathcal F$-measurable yet non-integrable; expectation and conditional expectation are defined only on (suitable) integrable objects. Unbounded payoffs need the standard machine's limit step.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 1 (Def 1.1.1–1.1.2, standard machine, MCT/Fatou/DCT Thms 1.4.5/1.4.9, RN Thm 1.6.1), Ch 2 (conditional expectation existence, properties).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 9 (Radon–Nikodym, state price density, Ex 9.1, existence of conditional expectation §9.5), Ch 11 (law, density as RN derivative w.r.t. Lebesgue, multivariate normal independence ⇔ diagonal covariance).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §1.1 (MC estimator, SLLN, CLT, standard error), §1.2 (risk-neutral measure via RN).
- **Casella & Berger**, *Statistical Inference*, Ch 4 (distributions, moments) — the classical distributional companion (PDF in the corpus).

---

### 6. Connected Graph Bridges

- Back: [[foundations/probability-and-measure-theory/05-martingales|05 · Martingales]] · [[foundations/probability-and-measure-theory/index|Index Hub]]
- Forward topic-folder: [[foundations/stochastic-calculus/index|Stochastic Calculus]] (Girsanov as the continuous Radon–Nikodym, martingale representation) · [[foundations/numerical-methods/03-monte-carlo|Monte Carlo]] (SLLN/CLT in practice)
- Theory: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (risk-neutral pricing is a RN measure change) · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
