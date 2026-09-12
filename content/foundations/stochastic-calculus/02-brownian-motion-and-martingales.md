---
title: "M.4.2 Brownian Motion & Martingales"
tags:
  - foundations
  - stochastic-calculus
  - brownian-motion
  - martingales
  - quadratic-variation
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[foundations/stochastic-calculus/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Brownian motion is the *canonical fair game in continuous time*: it moves, but has no drift, so its best predictor of the future given the present information is the present value. That single property - the **martingale property** $\mathbb E[W(t)\mid\mathcal F(s)]=W(s)$ - is the backbone of all no-arbitrage pricing, because "prices under the risk-neutral measure are martingales" is how modern pricing is stated.

The practical objective of this page: understand the *three linked faces of BM* - (1) Gaussian increments and the covariance $\min(s,t)$; (2) the martingale and Markov properties and their exponential cousin $e^{\sigma W-\tfrac12\sigma^2t}$; (3) the fact that BM "runs fast," i.e. quadratic variation $=t$ and infinite first-order variation. These give the toolkit (independent increments, stopping, first-passage) used constantly in barrier options, simulation, and Girsanov.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Definition & covariance (Shreve II Def 3.3.1; Shreve I §13.5–13.7)
A process $W(t),\,t\ge0$ is **BM** if: $W(0)=0$; paths are continuous; increments $W(t_{i+1})-W(t_i)$ are independent and $N(0,\,t_{i+1}-t_i)$-distributed. Then $\operatorname{Cov}(W(s),W(t))=\min(s,t)$ and finite-dimensional laws are jointly normal with $C_{ij}=t_i\wedge t_j$. **Equivalent characterizations** (Shreve II Thm 3.3.2): independent normal increments ⇔ jointly-normal-with-that-covariance ⇔ the joint MGF form (3.3.5). *Normal increments make "uncorrelated ⇒ independent" true here - a huge simplification that fails for general processes.*

#### 2.2 Martingale property (Shreve II Thm 3.3.4)
Using independence of the future increment $W(t)-W(s)$ from $\mathcal F(s)$:
$$
\mathbb E[W(t)\mid\mathcal F(s)]=\mathbb E[W(s)+(W(t)-W(s))\mid\mathcal F(s)]=W(s)+0=W(s).
$$
$W$ is also **Markov**: the only relevant information in $\mathcal F(s)$ is $W(s)$ itself, with transition density $$p(\tau,x,y)=\frac{1}{\sqrt{2\pi\tau}}e^{-\frac{(y-x)^2}{2\tau}},\qquad \mathbb E[f(W(t))\mid\mathcal F(s)]=\int f(y)\,p(t-s,W(s),y)\,dy.$$ (Shreve II §3.5; via the Independence Lemma, Shreve II Lemma 2.3.4.)

#### 2.3 The exponential martingale (Shreve II Thm 3.6.1; Shreve I Thm 9.41)
For constant $\sigma$,
$$
Z(t)=\exp\Big\{\sigma W(t)-\tfrac12 \sigma^2 t\Big\}\quad\Longrightarrow\quad \mathbb E[Z(t)\mid\mathcal F(s)]=Z(s).
$$
*Proof.* Condition, factor $Z(s)$, and use the increment MGF $\mathbb E e^{\sigma(W(t)-W(s))}=e^{\tfrac12\sigma^2(t-s)}$, which exactly cancels the $\tfrac12\sigma^2$ correction. This process is the seed of Girsanov's change of measure ([[foundations/stochastic-calculus/05-girsanov-and-risk-neutral|05 · Girsanov]]).

#### 2.4 Quadratic variation & the first-passage time (Shreve II §3.4, §3.6)
$$
[W,W](T)=\lim\sum_j(\Delta W_j)^2=T\quad\Rightarrow\quad(dW)^2=dt.
$$
Let $\tau_m=\min\{t\ge0: W(t)=m\}$ ($m>0$). Stopping the exponential martingale at $\tau_m$ and letting $t\to\infty$ via dominated convergence gives (Shreve II Thm 3.6.2):
$$
\mathbb E\big[e^{-\alpha\tau_m}\big]=e^{-m\sqrt{2\alpha}}\quad(\alpha>0),\qquad \mathbb E\tau_m=\infty.
$$
So BM *reaches every level with probability 1 but takes, on average, infinitely long* - a striking, exactly-quantified tension. The **reflection principle** (Shreve II eq 3.7.6) turns barrier/threshold probabilities into tail probabilities:
$$
\mathbb P\{M(t)\ge m,\ W(t)\le w\}=\mathbb P\{W(t)\ge 2m-w\},\qquad M(t)=\max_{0\le s\le t}W(s).
$$

---

### 3. Computational Implementation - verify martingale & exponential-martingale in one shot

Simulate many paths, condition on the state at a fixed time $s$, and check that the sample mean of the later value equals the conditioned state (martingale property); then average the exponential martingale and compare to 1. Stdlib only.




---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Zero drift" ≠ "stays put."** A martingale can have enormous variance - BM, discounted asset prices, everything fair-but-volatile. The martingale property says only that the *conditional mean* of the future is the present, never that the path is flat. Treating "martingale" as "predictable at the level" misreads the definition.
2. **Uncorrelated ≠ independent (outside Gaussian).** Only for *jointly normal* processes does zero covariance imply independence (Shreve II §2.2, Example). Many intuitions that "work" for BM fail for general processes; the independence cutoff is the Gaussian assumption, not a general fact.
3. **$\mathbb E\tau_m=\infty$ surprises everyone.** First-passage is almost-sure but mean-infinite; naive simulation (finite horizon) massively understates hitting probabilities, and pricing barrier options from a short simulation is biased. This underlies the continuity-correction and Brownian-interpolation literature (Glasserman Ch 6).
4. **Mismatched variance in simulation.** Mis-scale the step variance: drawing $\Delta W\sim N(0,dt)$ from $N(0,\Delta t)$ over a *different* grid quietly violates $\operatorname{Var}=t-s$ and breaks every downstream QV/martingale check.

---

### 5. References

- **Shreve**, *Stochastic Calculus for Finance II*
- **Shreve**, *Stochastic Calculus for Finance I*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*

---

### 6. Connected Graph Bridges

- Back: [[foundations/stochastic-calculus/01-from-zero-intuition|01 · From Zero]]
- Forward: [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|03 · Itô Integral & Doeblin]] · [[foundations/stochastic-calculus/index|Index Hub]]
- Theory: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]