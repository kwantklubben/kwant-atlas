---
title: "4.2.1 VaR from Zero"
tags:
  - pillar-quantitative-risk
  - parametric-historical-and-monte-carlo-var
  - intuition
  - quantile
  - risk-measures
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (quantiles, distributions).

---

### 1. Intuition & Practical Objective

This page builds the *why* of Value at Risk with **no prior risk knowledge needed**. The objective is one idea: **VaR is just a quantile of your portfolio's loss distribution - the number that says "I only lose more than this with probability $1-\alpha$."** Everything else in this folder is about *how to obtain that quantile in practice*, because you almost never know the true loss distribution; you have to estimate it from a model or from data.

Start with the dumbest framing. A trader holds a portfolio. Tomorrow the market moves and the portfolio gains or loses $\Delta V$ dollars. We don't know $\Delta V$ in advance - it is random, drawn from some distribution. Define the **loss** $L=-\Delta V$ (positive when we lose money, and a negative loss is a gain). The 99% VaR over one day is the number $v$ such that

$$
P(L > v) = 0.01,
$$

i.e. *99% of the time the loss is no worse than $v$; only on 1 day in 100 do we lose more.* Three mental "aha"s:

1. **VaR is a quantile, not an expectation.** It speaks about the *right tail* of the loss distribution, not its center. The mean loss could be tiny while VaR is huge - they answer different questions ("how much on a normal day" vs "how bad on a bad day").

2. **Confidence and horizon are the two knobs.** Raise confidence $99\%\to99.9\%$ and VaR grows (you go further into the tail); lengthen the horizon $1\text{ day}\to10\text{ days}$ and VaR grows like $\sqrt{h}$ under i.i.d. returns. There is no single "the VaR" - every VaR number is meaningless unless it comes with a confidence and a horizon.

3. **VaR is model-free as a *definition*, but not as a *number*.** The *definition* "the $\alpha$-quantile of the loss distribution" needs no assumptions. But computing it requires the distribution, and *that* is where the three methods part ways: **parametric** assumes the shape, **historical** samples it from the past, **Monte Carlo** builds it by simulation.

---

### 2. Mathematical Ground Truth & Derivations

**VaR as an inverse CDF.** Let $F_L(l)=P(L\le l)$ be the distribution of loss. The $\alpha$-quantile is the inverse

$$
\text{VaR}_\alpha = F_L^{-1}(\alpha) = \inf\{l : F_L(l)\ge\alpha\}.
$$

Because we defined loss as $L=-\Delta V$, a *larger* $L$ is worse, so the $\alpha$-quantile of $L$ is the number that the loss exceeds with probability $1-\alpha$.

**Horizon scaling (i.i.d. returns).** If returns are i.i.d. with variance $\sigma^2$ per day, the $h$-day loss variance is $h\sigma^2$, so for *any* distribution whose tail scales the same way, the quantile scales as

$$
\text{VaR}_\alpha^{(h)} = \text{VaR}_\alpha^{(1)} \cdot \sqrt{h}.
$$

This is the famous **$\sqrt{h}$ rule** (Hull Ch 22: "N-day VaR = 1-day VaR × √N"). It is *exact only under i.i.d. normal-ish returns* - when losses cluster (GARCH), the true $h$-day VaR scales slower or faster - a failure mode in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05]].

**Why a quantile at all? (vs the average loss).** The average loss (Expected Shortfall, [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|ES]]) answers "given I'm in the tail, how bad is it?", which is why regulators now prefer it. But VaR is the historically standard number: it is a *single market-stable capital figure* a board can hold, and it is *computable* from each of the three methods below.

---

### 3. Computational Implementation - "what is a quantile, really?"

There is literally nothing mysterious here: a quantile is one line of Python. We take a set of hypothetical daily portfolio losses (our "crystal ball" of the future) and just grab the right one. Stdlib only.



Watch the behavior: the **median loss is negative** (a typical day is a small *gain*), yet the 99% and 99.9% VaR are thousands of dollars in losses. That is exactly the tail-vs-center gap from §1 - and it shows why confidence matters: raise the confidence and the VaR rockets into the tail. Note `quantile()` sorts the *loss* upward, so the `k`-th smallest loss at rank `round(αn)` is exactly the $\alpha$-quantile.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The 99% VaR."** Saying just that is ambiguous - VaR lives in (confidence, horizon) space: 99% *what*? 1-day or 10-day? Differ by $\sqrt{10}\approx3.16$. Cite both, always.
2. **Quantile instability in the tail.** Less data lives out at 99.9%, so estimates bounce wildly (Glasserman Ch 9: quantile-estimation variance $\propto p(1-p)/f(x_p)^2$ blows up as $p\to0$). The 99.9% number in §3 is the *least* reliable of the four.
3. **Sign errors.** Loss $L=-\Delta V$; compute VaR on the wrong sign and you have quoted gains as risk. Getting VaR from P&L requires taking `-` exactly once, in the right place.
4. **VaR isn't subadditive.** $\text{VaR}(X+Y)$ can exceed $\text{VaR}(X)+\text{VaR}(Y)$ (Artzner et al. 1999; [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|ES is the coherent fix]]). Summing desk VaRs to get firm VaR can *understate* risk - dangerous precisely because it feels safe.

---

### 5. References

- **Hull**, *Options, Futures, and Other Derivatives*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*
- **Jorion, Philippe**: *Value at Risk: The New Benchmark for Managing Financial Risk* (3rd ed., 2006)

---

### 6. Connected Graph Bridges

- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] (quantiles, tail probabilities) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the measure's definition and its limits).
- Continue: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/02-parametric-var|02 · Parametric (delta-normal) VaR]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Index Hub]].
- Forward: [[foundations/numerical-methods/index|Numerical Methods]].