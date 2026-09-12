---
title: "4.12.1 Copulas from Zero"
tags:
  - pillar-quantitative-risk
  - copulas-and-dependence
  - intuition
  - dependence
  - diversification
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (joint vs marginal distributions).

---

### 1. Intuition & Practical Objective

This page builds the *why* of copulas with **no prior copula knowledge needed**. The objective is one idea: **the risk of a portfolio is not the sum of the risks of its positions; it is the sum plus a term that depends entirely on how the positions move together - and that term is a separate modelling choice you have to make, not something the individual risks tell you.**

Start with the dumbest question: *two positions, each with the same loss distribution. Is the portfolio risk determined?* The beginner says yes: "just add the VaRs." The beginner is wrong. Consider two assets, each with a standard-normal return, in an equal-weighted book. The book's loss is $-(A+B)/2$. Change **only the dependence** between $A$ and $B$:

1. **Independent** - $A$ and $B$ are unrelated. The book's volatility falls to $1/\sqrt2$ if each has unit volatility: diversification, the thing every textbook promises.
2. **Comonotone** - $B=A$ (perfect positive dependence). There is *no* diversification at all; the book is one asset in disguise.
3. **Countermonotone** - $B=-A$ (perfect negative dependence). The book is riskless; the two positions always cancel.

Same two marginals. Same dollars. The $95\%$ VaR of the book goes from **$0$ to $1.64$** depending on which of these is true. That gap is the whole subject.

> **Three steps.**
> 1. **Marginals are not enough.** Knowing each position's loss distribution leaves the portfolio loss distribution undetermined. Dependence is *additional* information.
> 2. **Dependence is a function of the ranks, not the levels.** What matters is not how *big* each loss is but how their *percentiles* line up. This is why rank correlation, not Pearson correlation, is the natural measure, and why a copula - a function on the unit square of percentiles - is the right object.
> 3. **Diversification is a copula statement.** "Diversification reduces risk" is true for the independence copula and false for the comonotone one. There is no diversification number that holds for all dependence structures with the same marginals - only a *range* (the Fréchet bounds).

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Let two positions have returns $A,B$ with *identical* standard-normal marginals, $A,B\sim N(0,1)$. The equal-weighted portfolio loss is $L=-(A+B)/2$ and its $95\%$ VaR is the $0.95$-quantile of $L$.

**Case 1 - independence.** $\mathrm{Var}(A+B)=2$ and $\mathrm{Var}(L)=\tfrac12$, so $L\sim N(0,\tfrac12)$ and

$$
\mathrm{VaR}_{0.95}(L)=z_{0.95}/\sqrt2=1.6449/1.4142=1.1631.
$$

**Case 2 - comonotone ($B=A$).** $L=-A$, so $L\sim N(0,1)$ and $\mathrm{VaR}_{0.95}=1.6449$.

**Case 3 - countermonotone ($B=-A$).** $L=0$ exactly; $\mathrm{VaR}_{0.95}=0$.

So with the same marginals the book VaR spans $[\,0,\ 1.6449\,]$. Nothing about $A$ or $B$ individually told us which one applies.

**The general statement (Fréchet).** For any joint distribution $F$ of $d$ positions with margins $F_i$, writing $u_i=F_i(x_i)$, the copula $C$ that links them is bounded:

$$
\max\!\Big(\sum_{i=1}^d u_i+1-d,\ 0\Big)\ \le\ C(u_1,\dots,u_d)\ \le\ \min(u_1,\dots,u_d).
$$

The lower bound is the **countermonotone** copula $W$ (positions perfectly negatively aligned), the upper bound the **comonotone** copula $M$ (perfectly positively aligned; $M(u)=\min u_i$). Every portfolio risk measure therefore lies in a band whose width is exactly the dependence uncertainty:

$$
\text{risk}(W)\ \le\ \text{risk}(C)\ \le\ \text{risk}(M)\quad\text{(for risk measures monotone in the concordance order, e.g. ES; plain VaR is not generally so).}
$$

**Why "ranks, not levels".** The copula is invariant under strictly increasing transformations of the margins: if you replace a loss in dollars by its logarithm, or a return by its rank, the copula does not change. Pearson correlation *does* change. That is the first clue that the correct dependence input is a rank quantity.

**The portfolio loss is a copula functional.** For a generic $d$-asset book with loss $L=\sum_i w_i\,\ell_i$, everything about $\mathbb{E}[L]$ is marginal, but everything about the *shape* of $L$'s distribution - skew, kurtosis, and every quantile above the mean - is a functional of the copula. That is why two books with identical marginals can have VaR $1.16$ and $1.64$.

---

### 3. Computational Implementation - same marginals, three risks

Stdlib only. We sample the three dependence structures explicitly and measure the book's $95\%$ VaR and Expected Shortfall; the simulation is checked against the analytic values of §2.




The simulation reproduces the analytic VaR to three decimals. The three books are **indistinguishable position-by-position** and differ in portfolio VaR by a factor of $\infty$ (from $0$ to $1.64$). No amount of marginal analysis could have told the risk manager which book she held - that information lives entirely in the copula.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"VaR is additive."** Only under the comonotone copula. Adding position VaRs is the *upper* Fréchet bound, not an estimate; using it is a deliberate worst-case assumption, not a neutral default.
2. **Pearson correlation as a dependence model.** Two variables can have Pearson $\rho=0$ and be strongly dependent (e.g. $B=A^2$), and Pearson $\rho$ is not invariant under monotone rescaling - so it cannot be a copula parameter. Rank correlations (Kendall, Spearman) are the invariant measures and are the correct calibration input (page 02).
3. **The "diversification number" illusion.** Reporting a single diversification benefit implicitly assumes independence. Independence is one copula among a continuum; a risk report that does not state its dependence assumption has hidden the largest assumption it makes.
4. **Tail vs centre.** In the centre of the distribution, independence is a benign assumption. In the tail - where VaR and ES live - the *same* marginals can produce joint losses an order of magnitude apart. Dependence matters most exactly where you are least able to check it. This is the seed of [[pillars/04-quantitative-risk/copulas-and-dependence/04-tail-dependence-and-t-copula|04 · Tail Dependence]].

---

### 5. References

- **McNeil, Frey & Embrechts (2015)**, *Quantitative Risk Management*
- **Embrechts, McNeil & Straumann (2002)**, *Correlation and Dependence in Risk Management: Properties and Pitfalls*
- **Nelsen, Roger B. (2006)**, *An Introduction to Copulas*, 2nd ed.
- **Embrechts, Klüppelberg & Mikosch (1997)**, *Modelling Extremal Events*
- **Hull (11th ed.)**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Continue: [[pillars/04-quantitative-risk/copulas-and-dependence/02-sklars-theorem-and-copulas|02 · Sklar's Theorem & Copulas]] · [[pillars/04-quantitative-risk/copulas-and-dependence/index|Index Hub]]
- Related risk: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the subadditivity question this page makes concrete) · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]
