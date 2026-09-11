---
title: "F.3.2 Probability Spaces & Filtrations"
tags:
  - foundations
  - probability-and-measure-theory
  - sigma-algebra
  - filtration
  - measurability
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

A $\sigma$-algebra is **information written as a set of questions you can answer Yes/No.** At time $t$ you know the past of the stock price but not its future; the collection of events you *can* distinguish is $\mathcal F_t$, and a **filtration** $\mathcal F_0\subseteq\mathcal F_1\subseteq\cdots\subseteq\mathcal F$ is those sets growing as time passes and information accumulates. A process is **adapted** if it only ever uses today's-and-earlier information — which is the mathematical statement of "no lookahead bias."

The practical objective of this page: understand the three linked ideas — (1) $\sigma$-algebras as the closed family of measurable events; (2) the probability measure with its countable additivity; (3) filtrations and $\mathcal F_t$-measurability as the exact language of "information available at time $t$." Everything downstream — conditional expectation, martingales, no-arbitrage — is defined *relative to* a filtration, so getting this precise is the hinge of the whole Atlas.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 $\sigma$-algebra (Shreve II Def 1.1.1; Shreve I §2.2)
On nonempty $\Omega$, a family $\mathcal F$ of subsets is a $\sigma$-algebra if: $\varnothing\in\mathcal F$; $A\in\mathcal F\Rightarrow A^c\in\mathcal F$; $A_1,A_2,\dots\in\mathcal F\Rightarrow\bigcup_n A_n\in\mathcal F$. Closure under countable unions + complements gives countable intersections, finite unions, and $\Omega\in\mathcal F$. The **Borel $\sigma$-algebra** $\mathcal B(\mathbb R)$ is the smallest $\sigma$-algebra containing the open sets; a **random variable** is $X:\Omega\to\mathbb R$ with $X^{-1}(B)\in\mathcal F$ for every Borel $B$ (Shreve I Ch 11). On a finite space (e.g. $n$ coin tosses) one takes $\mathcal F=$ all $2^{2^n}$-many subsets, and the theory reduces to counting.

#### 2.2 Probability measure & countable additivity (Shreve II Def 1.1.2)
$\mathbb P:\mathcal F\to[0,1]$ with $\mathbb P(\Omega)=1$ and, for disjoint $A_n$,
$$
\mathbb P\Big(\bigcup_{n}A_n\Big)=\sum_n\mathbb P(A_n).
$$
Finite additivity and $P(A^c)=1-P(A)$ follow. On $[0,1]$, uniform/Lebesgue measure starts from $\mathbb P(a,b]=b-a$ on intervals and extends to Borel sets by countable additivity (Shreve II Ex 1.1.3).

#### 2.3 The generated $\sigma$-algebra: what does a random variable "reveal"? (Shreve I §2.2; Shreve II §2.1)
The natural filtration on the coin-toss space is $\mathcal F_k=\sigma(S_1,\dots,S_k)$, the smallest $\sigma$-algebra w.r.t. which $S_1,\dots,S_k$ are measurable. Its **atoms** are the sets of paths sharing the first $k$ tosses: $\mathcal F_1$ has two atoms (first toss H or T), $\mathcal F_2$ has four, etc. $X$ is $\mathcal F_k$-measurable iff its value is *determined by the first $k$ tosses* (Shreve I §2.2). This is exactly "information revealed by the stock up to time $k$."

#### 2.4 Filtrations, adaptedness, and the flow of time (Shreve I §2.4; Shreve II Def 3.3.3)
A **filtration** is an increasing family $\mathcal F_0\subseteq\mathcal F_1\subseteq\cdots\subseteq\mathcal F_n$; a process $\{M_k\}$ is **adapted** if $M_k$ is $\mathcal F_k$-measurable for each $k$. For continuous Brownian motion the filtration satisfies (Shreve II Def 3.3.3) $W$ adapted **and** future increments $W(u)-W(t)$ independent of $\mathcal F(t)$ for $u\ge t$ — the efficient-markets formulation: today's information tells you nothing about the *direction* of tomorrow's move.

---

### 3. Computational Implementation — the coin-toss space with its filtration

Build the 3-toss space, compute $\mathbb E[X\mid\mathcal F_1]$ by **averaging over atoms** (the finite-space reduction of partial averaging), and verify partial averaging, the tower property, and $\mathcal F_1$-measurability. Stdlib only.

```python
import itertools
# 3-toss coin space, uniform measure P(w)=1/8
n=3
Omega = list(itertools.product('HT', repeat=n))
P = {w: 1.0/len(Omega) for w in Omega}
S0,u,d = 4.0, 2.0, 0.5
def S3(w): return S0*(u**w.count('H'))*(d**w.count('T'))
X = {w: S3(w) for w in Omega}
def atoms(k):
    dd={}
    for w in Omega: dd.setdefault(w[:k],[]).append(w)
    return list(dd.values())
def Econd(d, atomlist):          # conditional expectation = average over atoms
    res={}
    for A in atomlist:
        Ps=sum(P[w] for w in A); val=sum(P[w]*d[w] for w in A)/Ps
        for w in A: res[w]=val
    return res
E1 = Econd(X, atoms(1))          # E[X|F_1]
E2 = Econd(X, atoms(2))
E1ofE2 = Econd(E2, atoms(1))     # tower E[E[X|F_2]|F_1]
A = atoms(1)[0]
lhs = sum(P[w]*E1[w] for w in A); rhs = sum(P[w]*X[w] for w in A)
print("partial averaging over F_1 atom:  int_A E[X|F1]=%.4f  int_A X=%.4f" % (lhs,rhs))
print("tower: max|E[E[X|F2]|F1]-E[X|F1]| = %.4f (theory 0)" % max(abs(E1[w]-E1ofE2[w]) for w in Omega))
consts = (len({E1[w] for w in atoms(1)[0]})==1) and (len({E1[w] for w in atoms(1)[1]})==1)
print("E[X|F1] constant on F_1 atoms (measurable) = %s" % consts)
print("P(Omega) = %.4f  (countable additivity normalizes to 1)" % sum(P.values()))
```
```
partial averaging over F_1 atom:  int_A E[X|F1]=6.2500  int_A X=6.2500
tower: max|E[E[X|F2]|F1]-E[X|F1]| = 0.0000 (theory 0)
E[X|F1] constant on F_1 atoms (measurable) = True
P(Omega) = 1.0000  (countable additivity normalizes to 1)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Lookahead bias = $\mathcal F_t$-violation.** A backtest feature computed with bar $t$'s close $C_t$ before that close has occurred is $\mathcal F_{t+\Delta t}$-measurable, not $\mathcal F_t$-measurable — it peeks one bar into the future. Root cause: the feature is not adapted to the trading filtration. (Shreve I §2.2.)
2. **Believing every subset is measurable.** On an uncountable $\Omega$ not every set is in $\mathcal F$; $\mathcal B(\mathbb R)$ and Lebesgue measure are built on Borel sets for exactly this reason (Shreve II Ex 1.1.3). A "probability" that assigns mass to a non-measurable set is simply undefined.
3. **Requiring a measure on outcomes.** Since $\Omega_\infty$ is uncountable, single-path probabilities are forced to $0$; demanding $\mathbb P(\{\omega\})>0$ for each $\omega$ makes $\mathbb P(\Omega)=\infty$, breaking normalization. The measure must live on sets (Shreve II §1.1).
4. **Forgetting the filtration when defining a martingale/expectation.** "$\mathbb E[M_{t+1}]=M_t$" is *false* in general (expectations are numbers); the correct statement is conditional on $\mathcal F_t$. Dropping the filtration turns the definition into nonsense.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 1 (Def 1.1.1 $\sigma$-algebra, Def 1.1.2 measure, Ex 1.1.3 Lebesgue) and Ch 2 §2.1–2.2 (information as $\sigma$-algebra, independence).
- **Shreve**, *Stochastic Calculus for Finance I*, §2.2–2.4 (coin-toss space, $\mathcal F_k=\sigma(S_1,\dots,S_k)$, measurability, filtration, adapted), Ch 11 (law, density).
- **Shreve**, *Stochastic Calculus for Finance I*, §13.8 (BM filtration, independence of future increments).
- **Williams**, *Probability with Martingales*, Ch 1–3 (sigma-algebras, probability, random variables) — the cleanest rigorous reference.

---

### 6. Connected Graph Bridges

- Back: [[foundations/probability-and-measure-theory/01-from-zero-intuition|01 · From Zero]] · [[foundations/probability-and-measure-theory/index|Index Hub]]
- Forward: [[foundations/probability-and-measure-theory/03-distributions-and-expectation|03 · Distributions & Expectation]] · [[foundations/probability-and-measure-theory/04-conditional-expectation|04 · Conditional Expectation]]
- Theory: [[foundations/stochastic-calculus/index|Stochastic Calculus]] (BM filtration Def 3.3.3) · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] (discrete filtration $\mathcal F_k$)
