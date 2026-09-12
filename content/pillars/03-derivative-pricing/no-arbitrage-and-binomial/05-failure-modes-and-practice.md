---
title: "3.2.5 Failure Modes & Practice"
tags:
  - pillar-derivative-pricing
  - no-arbitrage-and-binomial
  - failure-modes
  - early-exercise
  - discretization-error
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/03-binomial-trees-and-convergence|03 · Trees & Convergence]].

---

### 1. Intuition & Practical Objective

A binomial engine is thirty lines of code and it is easy to make it produce a number that is *wrong in a specific, nameable way*. This page names those ways, with the numbers attached, so a practitioner can tell a real price from an artefact.

Five failures, in one line each:

1. **A step too coarse breaks the no-arbitrage bracket** - the risk-neutral probability leaves $[0,1]$ and the tree is an arbitrage machine.
2. **Applying a European formula to an American put** understates value by the early-exercise premium.
3. **Expecting (or fearing) early exercise on a dividend-free American call** - it never happens, and a tree "confirming" it is just showing discretization error.
4. **Trusting a single $n$** - CRR error oscillates and does not shrink monotonically.
5. **Discounting under the real-world measure** - the most common conceptual error, and the one that produces a plausible-looking wrong number.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The bracket is a constraint, not a convention

CRR requires $d<e^{r\Delta t}<u$, i.e. $e^{-\sigma\sqrt{\Delta t}}<e^{r\Delta t}<e^{\sigma\sqrt{\Delta t}}$, i.e.

$$
\sigma\sqrt{\Delta t}>r\Delta t\quad\Longleftrightarrow\quad \boxed{\;\sigma>r\sqrt{\Delta t}\;}
$$

Violate it and $p=\frac{e^{r\Delta t}-d}{u-d}$ leaves $[0,1]$: the "probability measure" is not a measure, the state prices $\zeta=\widetilde{\mathbb P}/(1+r)$ go negative, and a claim's value can be *below* its arbitrage bound. This is not a numerical bug; it is [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|FT1]] failing for the discretized market.

#### 2.2 Early exercise: the two asymmetric facts

**American put (and dividend-paying call).** The value satisfies the backward recursion

$$
v_k(x)=\max\Big\{\underbrace{\tfrac{1}{1+r}\big[\tilde p\,v_{k+1}(ux)+\tilde q\,v_{k+1}(dx)\big]}_{\text{continuation}},\;\underbrace{g(x)}_{\text{intrinsic}}\Big\},
$$

so $V^{\text{Am}}\ge V^{\text{Eu}}$ always, with a strictly positive **early-exercise premium** whenever the exercise region is non-empty. Applying the European formula is therefore a *lower bound*, not a price.

**American call, no dividend.** For a convex payoff with $g(0)=0$ and $r\ge0$ (Shreve Ch 7, Cor. 2.25) the discounted payoff $(1+r)^{-k}g(S_k)$ is a $\widetilde{\mathbb P}$-submartingale, so by optional sampling

$$
\widetilde{\mathbb E}\!\left[(1+r)^{-n}g(S_n)\right]=\max_{\tau}\widetilde{\mathbb E}\!\left[(1+r)^{-\tau}g(S_\tau)\right],
$$

hence $C^{\text{Am}}=c^{\text{BSM}}$ - **never exercise early**. A tree that appears to show otherwise is showing tree error, not economics.

#### 2.3 The American value as a supermartingale

The structural statement (Shreve Def 6.1): the discounted American value $\{(1+r)^{-k}V_k\}$ is the **smallest** $\widetilde{\mathbb P}$-supermartingale dominating the intrinsic process $\{G_k\}$; the optimal exercise time is $\tau^{*}=\min\{k:V_k=G_k\}$, the first node where value equals intrinsic. Hedging then needs *consumption* $C_k=V_k-\frac{1}{1+r}\widetilde{\mathbb E}[V_{k+1}\mid F_k]\ge0$ (Shreve Lemma 2.21) - the seller who loses an exercise race has already banked the difference.

---

### 3. Computational Implementation - the failures, in numbers

Stdlib only.

**Experiment 1 - breaking the bracket.** A long-dated single-step tree with $20\%$ volatility and a $5\%$ rate.



At $n{=}1$, $T{=}20$: $\sigma\sqrt{\Delta t}=0.894<r\Delta t=1.0$, so $u<e^{r\Delta t}$ and $p=1.134>1$. The same parameters with a fine step are perfectly well-behaved - the failure is *entirely* one of step size.

**Experiment 2 - early-exercise premium, and its absence for a call.**




The put carries a $+5.2\%$ early-exercise premium that no European formula can see. The call's "premium" is **negative and shrinking like $1/n$** - that gap is pure discretization error (the tree values are *below* the European price and converging upward). The economic prediction $C^{\text{Am}}=c^{\text{BSM}}$ is confirmed in the limit; a coarse tree merely looks like it disagrees.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The bracket, unguarded.** Always assert $d<e^{b\Delta t}<u$ inside a tree routine and raise on violation. The condition $\sigma>r\sqrt{\Delta t}$ will be met comfortably for equity-like inputs but *fails* for low vol, long maturity, or an accidental step size.
2. **European formula on an American put.** Understates by $0.2427$ ($5.2\%$) on the running example. The premium is *not* small when the put is in-the-money and rates are positive - it is the whole point of the contract.
3. **Hunting for an early-exercise boundary on a dividend-free call.** There is none ($C^{\text{Am}}=c^{\text{BSM}}$, Shreve Ch 7); an observed "boundary" at coarse $n$ is the discretization error of Experiment 2. With a *discrete dividend*, early exercise immediately before the ex-date can be optimal - a completely different mechanism (Hull §15.12, §13.5).
4. **Real-measure discounting.** $V_0=\mathbb E^{\mathbb P}[f]/(1+r)$ is wrong whenever $\tilde p\ne p$. Use $\mathbb E^{\widetilde{\mathbb P}}$ or, equivalently, $\mathbb E^{\mathbb P}[\zeta f]$ with $\zeta=\frac{d\widetilde{\mathbb P}/d\mathbb P}{1+r}$ ([[pillars/03-derivative-pricing/no-arbitrage-and-binomial/02-no-arbitrage-and-risk-neutral|02]]).
5. **Single-$n$ reporting.** Error oscillation ([[pillars/03-derivative-pricing/no-arbitrage-and-binomial/03-binomial-trees-and-convergence|03]]) means a favourite $n$ can be a lucky or unlucky one. Report an $n$-study or an averaged value.
6. **Wrong carry $b$.** Index/FX/commodity trees need $e^{(r-q)\Delta t}$ (or $e^{(r-r_f)\Delta t}$) as the growth factor, not $e^{r\Delta t}$ (Hull §13.11).

**Practice checklist.** Assert the bracket → choose $b$ from the instrument → average or smooth over $n$ → price European-and-tree to confirm the engine against the closed form → only then apply the American branch.

---

### 5. References

- **Shreve**, *Stochastic Calculus for Finance I*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Haug**, *The Complete Guide to Option Pricing Formulas*
- **Björk**, *Arbitrage Theory in Continuous Time*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/03-binomial-trees-and-convergence|03 · Trees & Convergence]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|04 · Fundamental Theorems]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/06-advanced-extensions|06 · Advanced Extensions]]
- Siblings: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · 05 Failure Modes]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
