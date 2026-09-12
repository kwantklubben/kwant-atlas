---
title: "4.10.4 Aggregate Loss & the Loss Distribution Approach (LDA)"
tags:
  - pillar-quantitative-risk
  - operational-risk
  - loss-distribution-approach
  - compound-poisson
  - operational-var
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[pillars/04-quantitative-risk/operational-risk/03-frequency-severity-modeling|03 · Frequency–Severity]].

---

### 1. Intuition & Practical Objective

The objective: **fuse the frequency and severity halves into one object - the distribution of annual total loss $S$ - and read the capital number off its tail.** This is the **Loss Distribution Approach (LDA)**, the quantitative core of operational-risk capital. Given a frequency law for $N$ and a severity law for $X$, LDA computes the aggregate-loss distribution $F_S$, from which:

- **Expected loss** $\text{EL}=\mathbb{E}[S]=\lambda\,\mathbb{E}[X]$ (the cheap average);
- **Operational VaR** $\text{VaR}_{99.9}=F_S^{-1}(0.999)$ (the one-year, 99.9% tail);
- **Unexpected loss** $\text{UL}_{99.9}=\text{VaR}_{99.9}-\text{EL}$,

and the Basel II AMA capital is $\text{EL}+\text{UL}$ at the 99.9% / one-year soundness standard (¶667).

Three "aha"s:

1. **$S$ is a random *sum of a random number* of losses** - a *compound* Poisson process. Its distribution is *not* a scaled-up severity; it is a convolution of severity with frequency, and it is heavier-tailed than either alone.
2. **The 99.9% quantile cannot be "seen" in the data** - no bank has 1,000 years of history. So $F_S$ must be *built* (by convolution, recursion, or Monte Carlo), not *observed*.
3. **Everything hinges on the severity tail.** At equal expected severity, a Pareto tail gives a 99.9% loss ~5.8× the lognormal's. LDA is a machine for turning a severity-tail choice into a capital number - the machine is correct, the input is everything.

---

### 2. Mathematical Ground Truth & Derivations

#### The compound Poisson aggregate

With $N\sim\text{Poisson}(\lambda)$ and $X_i\sim F_X$ iid independent of $N$,

$$
S=\sum_{i=1}^{N}X_i\qquad (S=0\ \text{when }N=0).
$$

**Expectation** (Wald's identity) and **variance**:

$$
\mathbb{E}[S]=\mathbb{E}[N]\,\mathbb{E}[X]=\lambda\,\mathbb{E}[X],\qquad
\text{Var}(S)=\mathbb{E}[N]\,\mathbb{E}[X^2]=\lambda\,\mathbb{E}[X^2].
$$

**Moment-generating function** (the cleanest expression of the convolution):

$$
M_S(t)=\mathbb{E}[e^{tS}]=\mathbb{E}\!\big[\mathbb{E}[e^{tS}\mid N]\big]
=\sum_{n=0}^{\infty}\frac{e^{-\lambda}\lambda^{n}}{n!}\big[M_X(t)\big]^{n}
=\exp\!\big[\lambda\,(M_X(t)-1)\big].
$$

This is the compound-Poisson signature: the aggregate MGF is the *exponential of* the severity MGF, encoding how Poisson frequency and severity convolve.

#### LDA capital

$$
\text{VaR}_{\alpha}=F_S^{-1}(\alpha),\qquad
\text{UL}_{\alpha}=\text{VaR}_{\alpha}-\mathbb{E}[S],\qquad
\text{Capital}_{\text{AMA}}=\text{EL}+\text{UL}_{0.999}.
$$

#### Analytic computation: Panjer recursion

When severity is discretized to integer units with probabilities $f_j=\mathbb{P}(X=j)$, the aggregate probability mass $g_k=\mathbb{P}(S=k)$ obeys the **Panjer recursion** (valid for the Poisson, $\mathbb{P}(N=n)=\tfrac{\lambda^n}{n!}e^{-\lambda}$, which is of the form $p_n=(a+\tfrac{b}{n})p_{n-1}$ with $a=0,\ b=\lambda$):

$$
g_k=\frac{1}{1-a f_0}\sum_{j=1}^{k}\Big(a+\frac{b\,j}{k}\Big)f_j\,g_{k-j},
$$

*(Here $g_0=\mathbb{P}(S=0)=\sum_n p_n f_0^n=e^{-\lambda(1-f_0)}$.)* The recursion gives $F_S$ *exactly* (up to discretization error) in $O(K^2)$ - the classical alternative to Monte Carlo used throughout Panjer (2006). Both routes converge to the same aggregate distribution.

---

### 3. Computational Implementation - Monte Carlo LDA with two severity tails

Simulate the compound Poisson directly, read $\text{EL},\text{VaR}_{99.9},\text{UL}$ from the empirical aggregate, and compare a lognormal severity against an **equal-mean Pareto** severity to expose the tail's dominance. Stdlib only.




Read the last line: **the MC expected loss matches the exact $\lambda\,\mathbb{E}[X]$** (Wald), and both severity choices cost the same "average" - yet the Pareto's 99.9% loss is **5.8× the lognormal's** (€7.88M vs €1.35M), and its VaR/EL ratio jumps from 2.24 to 13.1. The aggregate tail inherits the severity tail almost wholesale.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The tail is an input, not an output.** LDA correctly propagates whatever severity tail you feed it - which is why a lognormal "fit" produces €1.35M while a defensible Pareto produces €7.88M. Choosing the wrong family is the dominant error and is invisible in the EL.
2. **MC tail error.** The 99.9% quantile is estimated from $0.001M$ of $M$ paths - at $M=200{,}000$ only ~200 paths define it, so $\text{VaR}_{99.9}$ carries sampling noise that MC alone cannot shrink quickly (Glasserman Ch 1: $O(M^{-1/2})$). Use Panjer recursion or variance reduction when the tail must be tight ([[pillars/04-quantitative-risk/operational-risk/06-advanced-extensions|06 · Advanced Extensions]]).
3. **Independence is built into the formula.** $\mathbb{E}[S]=\lambda\mathbb{E}[X]$ and the MGF factorization assume independent events. Stress-time clustering and cross-event-type dependence break the compound-Poisson convolution, and LDA then *under-states* the true aggregate (the dependence failure mode, [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **Capital addition across cells.** Basel allows correlations across business-line/event-type estimates (AMA ¶669(d)); naively *summing* cell VaRs (perfect-correlation assumption) overstates total capital, while assuming independence understates it. Either way the choice is a model assumption to validate, not a freebie.

---

### 5. References

- **Panjer, *Operational Risk: Modeling Analytics*** (2006)
- **McNeil, Frey & Embrechts, *Quantitative Risk Management*** (2015)
- **Glasserman, *Monte Carlo Methods in Financial Engineering*** (2004, Springer)
- **BCBS, *Basel II*** (2006), ¶667 (99.9%/one-year AMA soundness standard) and ¶669(d) (correlations across estimates)
- **Shevchenko, *Modelling Operational Risk Using Bayesian Inference*** (2011)

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/04-quantitative-risk/operational-risk/03-frequency-severity-modeling|03 · Frequency–Severity]]
- Back: [[pillars/04-quantitative-risk/operational-risk/02-loss-event-types|02 · Loss Event Types]]
- Forward: [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/operational-risk/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the risk-measure it computes) · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]] (the tail it needs)
