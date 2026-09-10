---
title: "01 — Probability & Measure Theory from Zero: Intuition & the Why"
tags:
  - foundations
  - probability-and-measure-theory
  - intuition
  - law-of-large-numbers
  - central-limit-theorem
---

**Basic Prerequisites:** Elementary set theory and arithmetic.

---

### 1. Intuition & Practical Objective

This page builds the *why* of probability with **no prior probability theory needed**. The objective is one idea: **probability is a way of assigning "how much of the space" a set of outcomes takes up, and the tools that make finance rigorous — expectations, conditioning, martingales — are all just disciplined counting/summing over sets.**

Start with the dumbest question: *why does the coin you flip forever not give each outcome a probability?* Because there are *uncountably many* infinite sequences of Heads/Tails ($\Omega_\infty$ is uncountable, Shreve II §1.1). You cannot give positive mass to a single path in a continuous space (a stock price path, a return in continuous time) — the only sensible questions are about **sets of paths** ("does the price stay above $90$?"), and you measure those sets. That single shift — from counting *outcomes* to measuring *sets* — is the whole subject in one move.

Four "aha"s:

1. **Probability is a measure of sets.** A probability space $(\Omega,\mathcal F,\mathbb P)$ assigns a number $\mathbb P(A)\in[0,1]$ to every event $A$ in a family $\mathcal F$ that is closed under complements and countable unions (a $\sigma$-algebra). Countable additivity — $\mathbb P(\cup A_i)=\sum\mathbb P(A_i)$ for disjoint $A_i$ — is the "mass doesn't disappear" rule.
2. **Expectation is a weighted average that the Law of Large Numbers makes real.** If $X$ is a payoff, $\mathbb E[X]$ is its probability-weighted average; the average of many iid draws converges to it (SLLN), and their error is $O(1/\sqrt n)$ (CLT). That is the entire engine of Monte Carlo pricing (Glasserman Ch 1).
3. **Conditional expectation is "best prediction given information."** $\mathbb E[X\mid\mathcal G]$ is the $\mathcal G$-measurable random variable closest to $X$ in mean-square (the regression function $f(x)=\mathbb E[Y\mid X=x]$ of ESL Ch 2) — not a guess, a projection.
4. **A martingale is a fair game.** If the expected next value given all history equals the present value, $\mathbb E[M_{t+1}\mid\mathcal F_t]=M_t$, there is no edge to exploit — and "prices under the risk-neutral measure are martingales" is how no-arbitrage pricing is stated.

---

### 2. Mathematical Ground Truth & Derivations

**The probability space (Shreve II Def 1.1.1–1.1.2).** A $\sigma$-algebra $\mathcal F$ on nonempty $\Omega$ contains $\varnothing$, is closed under complements and countable unions (hence countable intersections and $\Omega\in\mathcal F$). A probability measure is $\mathbb P:\mathcal F\to[0,1]$ with $\mathbb P(\Omega)=1$ and **countable additivity** for disjoint events:

$$\mathbb P\Big(\bigcup_{n}A_n\Big)=\sum_n\mathbb P(A_n)\;\Rightarrow\;\mathbb P(A^c)=1-\mathbb P(A),\ \mathbb P(\varnothing)=0.$$

On a finite space one takes $\mathcal F=$ all subsets; on $[0,1]$ the **uniform (Lebesgue) measure** is defined first on intervals by $\mathbb P(a,b]=b-a$ and extended to Borel sets by countable additivity (Shreve II Ex 1.1.3).

**Expectation = the "standard machine" (Shreve II §1.4–1.5).** Integrals on uncountable spaces are built in four steps — indicator $\to$ simple $\to$ nonnegative $\to$ general — and computed via densities: $\mathbb E[h(X)]=\int h(x)\,f_X(x)\,dx$ (Shreve I Ch 11 Thm 3.32). The limit theorems — Monotone Convergence, Fatou, Dominated Convergence — justify passing limits through expectations (Shreve II Thms 1.4.5/1.4.9), which is exactly what makes "stop the martingale and let $t\to\infty$" legal in Ch 3.

**The two theorems that run Monte Carlo (Glasserman §1.1).** For iid $U_i$ with $\alpha=\mathbb E[f(U)]$:
$$\hat\alpha_n=\frac1n\sum_{i=1}^n f(U_i)\xrightarrow{\text{a.s.}}\alpha \quad\text{(SLLN)},\qquad \hat\alpha_n-\alpha\approx N\!\Big(0,\tfrac{\sigma_f}{\sqrt n}\Big)\quad\text{(CLT)}.$$
The standard error $\sigma_f/\sqrt n$ is **independent of dimension** — the raison d'être of MC in high-dimensional pricing (Glasserman §1.1; the error rate is $O(n^{-1/2})$ in any $d$).

**Conditional expectation and martingales previewed.** $\mathbb E[X\mid\mathcal G]$ is $\mathcal G$-measurable and satisfies **partial averaging** $\int_A\mathbb E[X\mid\mathcal G]d\mathbb P=\int_A X\,d\mathbb P$ ∀$A\in\mathcal G$ (Shreve II Def 2.3.1). A martingale is adapted + integrable with $\mathbb E[M_t\mid\mathcal F_s]=M_s$ (Shreve I §2.4). Both get full pages below ([[foundations/probability-and-measure-theory/04-conditional-expectation|04 · Conditional Expectation]], [[foundations/probability-and-measure-theory/05-martingales|05 · Martingales]]).

---

### 3. Computational Implementation — *see* the LLN and the CLT

Simulate a fair coin and watch the sample mean converge to $0.5$; then simulate many sample means of $k$ uniforms and check their spread and the 68–95–99.7 rule. Stdlib only.

```python
import math, random
random.seed(7)
# (1) LLN: sample mean of fair coin -> 1/2
n = 200000
flips = [1.0 if random.random() < 0.5 else 0.0 for _ in range(n)]
print("LLN: sample mean of fair coin (theory 0.5)  = %.4f" % (sum(flips)/n))
# (2) CLT: std of sample mean of k=100 Unif[0,1]
sigma = 1.0/math.sqrt(12.0)
B, k = 40000, 100
means = [sum(random.random() for _ in range(k))/k for _ in range(B)]
m = sum(means)/B
var_ = sum((x-m)**2 for x in means)/(B-1)
print("CLT: std of sample mean (k=100 Unif)       = %.4f (theory %.4f)" % (math.sqrt(var_), sigma/math.sqrt(k)))
# (3) 68-95-99.7 on standardized sample means
zs = [(x-m)/math.sqrt(var_) for x in means]
in1 = sum(1 for z in zs if abs(z)<=1.0)/B
in2 = sum(1 for z in zs if abs(z)<=2.0)/B
print("CLT: P(|Z|<1) = %.4f (theory 0.6827)        " % in1)
print("CLT: P(|Z|<2) = %.4f (theory 0.9545)        " % in2)
```
```
LLN: sample mean of fair coin (theory 0.5)  = 0.5006
CLT: std of sample mean (k=100 Unif)       = 0.0288 (theory 0.0289)
CLT: P(|Z|<1) = 0.6822 (theory 0.6827)
CLT: P(|Z|<2) = 0.9546 (theory 0.9545)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Counting outcomes instead of measuring sets.** On an uncountable space, "probability of the path $S_t=100.000$" is $0$ for each path yet the union of paths has probability $1$. Assigning mass to outcomes, not sets, is exactly what $\sigma$-algebras prevent — the root motivation for the whole subject (Shreve II §1.1).
2. **Treating $\mathbb E[\cdot]$ as "the value it will take."** The LLN gives *convergence in average*, not a prediction for any single draw. A martingale can have huge variance and still be perfectly "fair" — see [[foundations/probability-and-measure-theory/05-martingales|05 · Martingales]].
3. **Believing the sample mean is exact.** The CLT error $\sigma_f/\sqrt n$ is *probabilistic*; halving the error needs $4\times$ samples, one extra decimal needs $100\times$. With no convergence theorem you cannot even justify the MC estimate (Glasserman §1.1).
4. **Conditioning on zero-probability events via the schoolbook ratio.** $\mathbb P(A\mid B)=\mathbb P(A\cap B)/\mathbb P(B)$ is undefined for $\mathbb P(B)=0$; only partial averaging defines conditioning there. See [[foundations/probability-and-measure-theory/04-conditional-expectation|04 · Conditional Expectation]].

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 1 §1.1 (uncountability of $\Omega_\infty$; Def 1.1.1 $\sigma$-algebra; Def 1.1.2 measure; Ex 1.1.3 Lebesgue), §1.4–1.5 (standard machine, MCT/Fatou/DCT, expectations via densities).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 1 §1.5 (finite probability spaces), Ch 11 (law, density, $\mathbb E h(X)=\int h\,f\,dx$).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §1.1 (MC estimator, SLLN, CLT, standard error $O(n^{-1/2})$, dimension-independence).

---

### 6. Connected Graph Bridges

- Base: none (this is the entry point) · [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (expectations as integrals)
- Continue: [[foundations/probability-and-measure-theory/02-probability-spaces-and-filtrations|02 · Probability Spaces & Filtrations]] · [[foundations/probability-and-measure-theory/index|Index Hub]]
- Forward: [[foundations/stochastic-calculus/index|Stochastic Calculus]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
