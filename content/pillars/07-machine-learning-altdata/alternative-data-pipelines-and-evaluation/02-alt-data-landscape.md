---
title: "7.5.2 The Alt-Data Landscape"
tags:
  - pillar-machine-learning
  - alternative-data-pipelines-and-evaluation
  - alternative-data
  - breadth
  - uniqueness
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/01-from-zero-intuition|01 · From Zero]] and [[foundations/statistics-and-inference/index|Statistics & Inference]].

---

### 1. Intuition & Practical Objective

This page is the **map**: what alternative datasets *are*, how they are categorized, and - the practical question every PM asks - *is a given dataset worth anything to a portfolio?* The objective is the framework that answers "worth anything": the **Fundamental Law of Active Management**, which says the value of a signal is $\text{IR}=\text{IC}\sqrt{B}$, and its extension to *combining* signals, which says a new dataset's worth is governed not by its own IC but by its **uniqueness** - how much of it is *not already* in the signals you trade.

The central reframing: **alt-data rarely raises your IC; it raises your breadth.** Almost no single dataset has a large IC (weak signals are the norm - see [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]]). What a *portfolio* of unique signals does is multiply your number of independent bets $B$ - and $\sqrt{B}$ is where the leverage lives. Twenty genuinely-uncorrelated $IC{=}0.03$ signals beat one $IC{=}0.06$ signal, because $\text{IR}$ grows like $\sqrt{n}$ while IC grows like $n$ only in a fantasy where the signals are perfect.

---

### 2. Mathematical Ground Truth & Derivations

**The Fundamental Law.** For a signal with information coefficient IC and $B$ independent bets per period (rebalances × names, adjusted for correlations),

$$
\boxed{\;\text{IR}=\text{IC}\cdot\sqrt{B}\cdot\text{TC}\;},
$$

with transfer coefficient $\text{TC}\in[0,1]$ capturing implementation friction (constraints, costs, capacity). Breadth, not IC, is the lever most strategies actually pull - and alt-data is the main way to add breadth because each *unique* dataset is a new, weakly-correlated bet stream.

**Combining $n$ signals with correlation.** Let each of $n$ alphas have standalone IC and let $\rho$ be their common pairwise correlation. An equal-weight composite has IC and IR

$$
\text{IC}_{\text{comb}}=\text{IC}\cdot\sqrt{\frac{n}{1+(n-1)\rho}},\qquad
\text{IR}_{\text{comb}}=\text{IC}\sqrt{\frac{n}{1+(n-1)\rho}}\sqrt{B}.
$$

**The two limits are the whole lesson:** as $n\to\infty$ with $\rho=0$, $\text{IC}_{\text{comb}}\sim\text{IC}\sqrt{n}$ (unbounded - every new independent alpha helps); with $\rho>0$, the denominator gives the ceiling $\text{IC}_{\text{comb}}\to\text{IC}/\sqrt{\rho}$, a *finite* wall. **Correlated alt-data saturates; unique alt-data compounds.**

**Required IC vs breadth.** Setting $\text{IR}=1$ (a decent standalone strategy) and reading off IC:

$$
\text{IC}^\star=1/\sqrt{B}:\quad B=12\Rightarrow 0.289,\quad B=52\Rightarrow 0.139,\quad B=252\Rightarrow 0.063.
$$

A monthly strategy needs an enormous IC to "work" alone; a daily strategy needs a tiny one. This is why alt-data desks are obsessed with *frequency* and *breadth*.

**Uniqueness (why the margin is in the residual).** If a model already uses a factor $f$, a new signal $s$ contributes only its orthogonal part. Define uniqueness $U=1-R^2$ from regressing $s$ on $f$ (and the existing factor set):

$$
U \;=\; 1-R^2,\qquad R^2=\frac{\operatorname{Var}(\hat s)}{\operatorname{Var}(s)},\qquad \hat s = \text{projection of }s\text{ on the existing factors}.
$$

The *marginal* IR contribution of $s$ scales with $\sqrt{U}$, not with its raw IC. A signal with $\text{IC}=0.05$ and $U=0.18$ adds less than a signal with $\text{IC}=0.03$ and $U=0.99$.

---

### 3. Computational Implementation - breadth, correlation, and the ceiling

Stdlib only. It computes the Fundamental Law for a single alpha, the $\sqrt{n}$ compounding of *independent* alphas, the **saturation wall** when they are correlated, and the IC required for $\text{IR}=1$ at each breadth.




Read the two middle blocks together. With **independent** alphas, ten $IC{=}0.03$ signals combine to $\text{IC}=0.0949$ and $\text{IR}=1.506$ - the $\sqrt{n}$ compounding, real diversification. With **correlated** alphas ($\rho=0.7$), adding signals barely helps: $\text{IR}$ rises from $0.517$ ($n{=}2$) to only $0.564$ ($n{=}25$) - it hits the $\text{IC}/\sqrt{\rho}$ wall. **The marginal value of an alt-data dataset is its correlation to what you already trade, not its standalone IC.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"We have 500 datasets" - but they are all the same signal.** Correlated alt-data (card panels from two vendors, three satellite providers of parking-lot counts) adds almost no breadth. The first principle: **breadth counts independent bets, not tickers or feeds**; $\text{IC}_{\text{comb}}$ saturates at $\text{IC}/\sqrt{\rho}$.
2. **Backtesting the IC and ignoring capacity/transfer.** A big IC in a tiny, illiquid name set with no capacity is worthless ($\text{TC}\ll1$). The law has three factors; optimizing IC alone is optimizing $\tfrac13$ of the problem.
3. **The uniqueness illusion.** A new signal with high raw IC but high correlation to your existing model (low $U$) is *already priced into your P&L*; adding it double-counts and inflates the backtest. Always compute the residual ([[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/06-advanced-extensions|06 · Advanced Extensions]]).
4. **Frequency ≠ breadth.** Rebalancing the *same* signal more often does not create independent bets when the signal is autocorrelated; $B$ must be an *effective* bet count after accounting for serial and cross-sectional correlation ([[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).

---

### 5. Canonical Literature & Study References

- **Grinold, Richard C. & Kahn, Ronald N.**: *Active Portfolio Management* (2nd ed.) - the Fundamental Law $\text{IR}=\text{IC}\sqrt{B}\text{TC}$ (Ch. 6) and breadth; the source of this folder's valuation framework.
- **López de Prado**, *Advances in Financial Machine Learning*, **§2.2.4** (the alt-data taxonomy: individuals / business processes / sensors, after Kolanovic & Krishnamachari) - the categories mapped here. *Corpus PDF verified.*
- **Kolanovic & Krishnamachari**, *Big Data and AI Strategies* (J.P. Morgan, 2017) - the taxonomy and the practical categorization of alt-data by source.
- **Guida, Tony**, *Big Data and Machine Learning in Quantitative Investment* (Wiley, 2019) - breadth, capacity, and the economics of adding datasets to a live book.
- **AIMA / SS&C**, *Casting the Net* (2017) - which datasets funds actually buy and the breadth-vs-crowding reality of the market.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/03-the-pipeline|03 · The Pipeline]] → [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/04-evaluating-signal|04 · Evaluating Signal]]
- Framework source: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (why breadth must be *effective* breadth, and the multiple-testing cost of hunting many signals) · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]]
- Where the data comes from: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]
