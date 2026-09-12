---
title: "3.2.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - no-arbitrage-and-binomial
  - american-options
  - optimal-stopping
  - continuous-time
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|04 · Fundamental Theorems]] and [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

The binomial model is not just the toy that BSM approximates. Two of its features survive the limit and are *harder* in continuous time, so the tree is where they should be learned:

1. **Early exercise.** An American claim is a *free-boundary / optimal-stopping* problem. In a tree the boundary is discovered node by node; in continuous time it is a smooth-pasting condition. Everything a desk does with American puts, Bermudan swaptions, or callable structures starts here.
2. **The passage to continuous time.** Scaling the random walk $u=e^{\sigma\sqrt{\Delta t}}$, $d=e^{-\sigma\sqrt{\Delta t}}$ as $\Delta t\to0$ produces Brownian motion and the lognormal - which is *why* the tree price converges to the BSM price, and why "binomial = discrete BSM" is a theorem and not an analogy.

This page closes the folder by making both directions concrete.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 American pricing as optimal stopping (Shreve Ch 5–6)

$$
v_n(x)=g(x),\qquad\boxed{\;v_k(x)=\max\Big\{\tfrac{1}{1+r}\big[\tilde p\,v_{k+1}(ux)+\tilde q\,v_{k+1}(dx)\big],\;g(x)\Big\}\;}
$$

**Characterizing properties** (Shreve Def 6.1):

- **(a) Value = optimal stopping value:** $V_k=(1+r)^k\max_{\tau\ge k}\widetilde{\mathbb E}\big[(1+r)^{-\tau}G_\tau\mid F_k\big]$ over stopping times $\tau$ ($\{\tau=k\}\in F_k$ - *no look-ahead*).
- **(b) Smallest supermartingale:** $\{(1+r)^{-k}V_k\}$ is the smallest $\widetilde{\mathbb P}$-supermartingale dominating $\{G_k\}$.
- **(c) Optimal exercise time:** $\tau^{*}=\min\{k:V_k=G_k\}$ attains the maximum.
- **(d) Hedge:** same difference quotient as the European case, but with a **consumption** stream $C_k=V_k-\frac{1}{1+r}\widetilde{\mathbb E}[V_{k+1}\mid F_k]\ge0$ (Lemma 2.21).

The perpetual (infinite-horizon) version has a clean closed form. With $u=2,d=\tfrac12,r=\tfrac14,K=5$ and $p̃=q̃=\tfrac12$, the candidate value is piecewise (Shreve Ch 8.8)

$$
v(x)=\begin{cases}\dfrac{6}{x}, & x\ge3,\\[4pt] 5-x, & 0<x\le3,\end{cases}\qquad\text{exercise the first time }S\le2 .
$$

Verified the only way an American value can be: (i) $v(x)\ge(5-x)^+$ everywhere; (ii) $\{(4/5)^kv(S_k)\}$ is a supermartingale; (iii) $v$ is the *smallest* such process.

#### 2.2 The random walk underneath (Shreve Ch 8)

Under $\widetilde{\mathbb P}$, $\log_2 S_k=\log_2 S_0+M_k$ (equivalently $S_k=S_0\,2^{M_k}$) with $M$ a symmetric $\pm1$ walk. First-passage moments come from the exponential martingale: for $0<\alpha<1$,

$$
\mathbb E[\alpha^{\tau_1}]=\frac{1-\sqrt{1-\alpha^2}}{\alpha}\qquad\Longrightarrow\qquad \mathbb E[\alpha^{\tau_m}]=\left(\frac{1-\sqrt{1-\alpha^2}}{\alpha}\right)^{m}.
$$

With $\alpha=\tfrac45$ this is $\tfrac12$, which prices the perpetual put by hand: stopping at $S=2$ gives $3\cdot\tfrac12=\tfrac32$; stopping at $S=1$ gives $4\cdot(\tfrac12)^2=1$; so $\tfrac32$ (stop at 2) is optimal. (The walk bridges to Brownian motion through Donsker's theorem - the same scaling this page verifies numerically.)

#### 2.3 Toward continuous time

Each step is $\log(S_{k+1}/S_k)=\pm\sigma\sqrt{\Delta t}$. Summing $n$ steps gives

$$
\log\frac{S_T}{S_0}=\sigma\sqrt{\Delta t}\sum_{k=1}^{n}\varepsilon_k,\qquad \varepsilon_k=\pm1,\quad\Delta t=\frac{T}{n},
$$

whose variance is $\sigma^2T$ and whose standardized sum converges (CLT / Donsker) to $N\big((r-\tfrac12\sigma^2)T,\sigma^2T\big)$ - the **lognormal of geometric Brownian motion**. Substituting that limiting distribution into the risk-neutral expectation $e^{-rT}\widetilde{\mathbb E}[(S_T-K)^+]$ *is* the Black–Scholes–Merton derivation ([[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02]]) - which is exactly why the CRR price converges to the BSM price $O(1/n)$.

Beyond the limit, the two structural extensions are **jump-diffusion** (Merton 1976: a Poisson mixture of lognormals, closed form but an *incomplete* market - FT2 fails, [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|04]]) and **stochastic/local volatility** ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]).

---

### 3. Computational Implementation - three checks, stdlib only

**(a) The step scaling becomes Gaussian** - $\log u=-\log d$ at every $\Delta t$, so the walk is a symmetric random walk in the log.




**(b) The perpetual American put** - the piecewise closed form and the first-passage moments, against Shreve's worked numbers.



$v(4)=1.5$ and $v(8)=0.75$ match the random-walk rule values exactly, and $v(x)=6/x$ reproduces $3\cdot(\tfrac12)^{j-1}$ on $x=2^j$ - the piecewise formula and the stopping rule are the same object.

**(c) American via CRR** - the tree as the practical American engine.




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Applying the European recursion to an American claim.** The single `max` with intrinsic value *is* the American algorithm; omitting it silently returns the European price and a $5\%$-scale error.
2. **Getting the measurability wrong.** A stopping time must satisfy $\{\tau=k\}\in F_k$. "Exercise when the *running minimum* hits a level" is a valid stopping rule only if evaluated with information available at $k$; using $S_{k+1}$ is look-ahead and overstates value (Shreve §5.2's explicit non-example).
3. **Assuming an American hedge is the European hedge.** Where exercise is optimal the delta hedge is *undefined* by the two terminal equations (Shreve Ex. 5.1 yields inconsistent $\Delta_1(T)$), which is exactly why the supermartingale-plus-consumption formulation (Lemma 2.21) is the correct object.
4. **Reading the continuous limit too literally.** Convergence to BSM is $O(1/n)$ *with oscillation* and assumes the lognormal; a tree calibrated to make the one-step distribution lognormal does not make the multi-step distribution lognormal at finite $n$.
5. **Confusing "converges to BSM" with "BSM is right".** The tree converges to BSM *because both assume a single lognormal driver*. Real markets jump and smile; where the tree adds value is precisely where BSM has no closed form (American, discrete dividends, path-dependence), not where it claims to be exact.

---

### 5. References

- **Shreve**, *Stochastic Calculus for Finance I*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Haug**, *The Complete Guide to Option Pricing Formulas*
- **Björk**, *Arbitrage Theory in Continuous Time*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
