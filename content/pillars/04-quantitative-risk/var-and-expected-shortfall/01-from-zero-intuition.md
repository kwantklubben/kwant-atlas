---
title: "4.1.1 Value at Risk & Expected Shortfall from Zero"
tags:
  - pillar-quantitative-risk
  - var-and-expected-shortfall
  - intuition
  - tail-risk
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (a CDF and a quantile are all you need).

---

### 1. Intuition & Practical Objective

This page builds the *why* of VaR and Expected Shortfall with **no prior risk-management knowledge needed**. The objective is one idea: **VaR tells you where the tail begins; ES tells you how bad the tail is.** VaR reports a single quantile and says nothing about how severe the losses beyond it can be; a portfolio built to satisfy only VaR can therefore hide extreme tail risk, which is exactly what Expected Shortfall captures.

Start with the manager's sentence everyone has heard: *"Our 1-day $99\%$ VaR is $ $\$5 million."* Unpack it literally: over the next day, the loss will exceed \5m only about $1$ day in $100$. It says **nothing** about what happens on that one day. Do you lose \$5{,}000{,}001 - or \$100 million and the firm? VaR is deliberately silent, because it is a *quantile*, not an average.

Three steps:

1. **VaR is a percentile, not a severity.** Line up 100 simulated tomorrows, order them worst-to-best, and read off the loss at rank $99$ (for $99\%$ VaR). Everything worse than that line is *discarded*. That discard is exactly what makes VaR fragile.

2. **Expected Shortfall averages what VaR throws away.** ES is the **mean of the worst $1\%$** - the conditional expectation of the loss *given* it breached VaR. It is larger than VaR by construction ($\mathrm{ES}_\alpha\ge\mathrm{VaR}_\alpha$) and it *moves* when the tail worsens, which VaR does not.

3. **The decisive difference is diversification.** Two separately-safe bets can be jointly dangerous under VaR, so VaR says *merging them created risk* - an absurdity that breaks risk limits, capital allocation, and decentralised governance. ES never does this. That is the whole coherence story ([[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|03 · Coherent Risk Measures]]), previewed here with numbers.

---

### 2. Mathematical Ground Truth & Derivations

**The two definitions, in words and symbols.** Let $L=-\Delta V$ be the loss over the horizon and $\alpha$ the confidence level (e.g. $0.99$):

$$
\mathrm{VaR}_\alpha(L)=F_L^{-1}(\alpha)=\inf\{l:\mathbb{P}(L\le l)\ge\alpha\},\qquad
\mathrm{ES}_\alpha(L)=\mathbb{E}\big[L\,\big|\,L\ge \mathrm{VaR}_\alpha(L)\big].
$$

VaR is the $\alpha$-quantile of the loss distribution; ES is the mean excess over that quantile. Both are **monetary amounts** (same units as $L$).

**The subadditivity koan (after Artzner §3.3), made discrete.** Take two independent bonds. Each loses \$100 with probability $4\%$ and loses nothing with probability $96\%$. Ask for the $95\%$ VaR of each *alone* and then of the *merged* position:

- Alone: $\mathbb{P}(L>0)=4\%\le 5\%$, so the $95\%$ quantile is $\mathrm{VaR}_{95\%}=0$. Each bond looks riskless.
- Merged: $\mathbb{P}(\text{at least one defaults})=1-(0.96)^2=7.84\%>5\%$. The $95\%$ quantile is now $100$.

So $\mathrm{VaR}_{95\%}(A+B)=100\not\le \mathrm{VaR}_{95\%}(A)+\mathrm{VaR}_{95\%}(B)=0$. **A merger created measured risk from nothing** - the opposite of diversification. ES behaves: $\mathrm{ES}_{95\%}(A)=\mathrm{ES}_{95\%}(B)=80$ and $\mathrm{ES}_{95\%}(A+B)=103.2\le 160$.

**Why the tail matters in money terms.** For a normal loss $L\sim\mathcal{N}(\mu,\sigma^2)$ the closed forms are (Hull eq. 22.1)
$$
\mathrm{VaR}_\alpha=\mu+\sigma z_\alpha,\qquad \mathrm{ES}_\alpha=\mu+\sigma\frac{\varphi(z_\alpha)}{1-\alpha},\qquad z_\alpha=\Phi^{-1}(\alpha).
$$
At $\alpha=0.99$ the ratio $\mathrm{ES}/\mathrm{VaR}=1.1457$: the average loss *beyond* the $99\%$ line is $14.6\%$ larger than the line itself - an amount VaR never reports. Under fat tails the gap explodes.

---

### 3. Computational Implementation - the two-bond koan, by hand and by Monte Carlo

We enumerate the loss distribution exactly (no simulation noise), then confirm it with a Monte Carlo book of 50 bonds. Stdlib only.




Read the first two lines aloud: identical economic exposures, and VaR *doubles in extremity* purely because the positions were *combined*. ES gives a sane, sub-additive answer. That is the paper's whole complaint in one table.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "it's just a percentile" trap.** A quantile is not a loss; it is a *threshold*. Reporting only VaR hides the entire loss-given-breach distribution. Always report ES (or the full tail) alongside any VaR number.
2. **Mistaking the tail *frequency* for the tail *size*.** VaR controls how often you breach; it ignores how deep the breach is. A strategy selling far-OTM options maximises small gains while pushing catastrophic losses just past the quantile - profitable until it is fatal ([[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **Confidence-level superstition.** "$99\%$" is a *convention*, not a guarantee. With $250$ trading days a year, a $99\%$ one-day VaR is breached about $2.5$ times per year - the estimator itself must be backtested, not trusted (Kupiec's POF test; [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]).
4. **Sign and convention confusion.** VaR/ES are reported as *positive loss numbers*; a loss of $L=-100$ has $\mathrm{VaR}=100$. P&L sign errors flip a risk limit into a green light.

---

### 5. References

- **Artzner, Delbaen, Eber & Heath**, *Coherent Measures of Risk*, *Mathematical Finance* 9(3) (1999)
- **Hull**, *Options, Futures, and Other Derivatives*
- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015)
- **Rockafellar & Uryasev**, *Optimization of Conditional Value-at-Risk*, *J. Risk* 2(3) (2000)

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Continue: [[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|02 · VaR Definition & Flaws]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] (what happens when the tail is power-law)
