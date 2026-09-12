---
title: "A.7.5 Failure Modes & Practice"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - failure-modes
  - data-mining
  - look-ahead-bias
  - survivorship
---

**Basic Prerequisites:** [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] through [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]].

---

### 1. Intuition & Practical Objective

Every factor premium in this folder is an empirical claim - a historical average that something "paid." This page is the defense layer: it asks whether the premium is *real* or an artifact of how it was found and measured. The objective is one idea: **a backtested factor premium is a hypothesis with a strong prior against it - the discipline is to make the premium survive honesty about data mining, crowding, and stale accounting.**

Three biases, each a first-principles consequence of how factor research is actually done:

- **Data mining (multiple testing).** The factor literature searched *hundreds* of candidate characteristics over the same data. If you test enough random rules, one will look spectacular by pure chance - and the "best" of the batch is a statistical mirage, not a discovery. Green, Hand & Zhang (2017) tested ~100 return-predictive signals and found only a *handful* (they estimate 24 at a demanding $|t|\ge3$ Fama–MacBeth hurdle, and put forward a 10-signal model) carry independent information - the rest are redundancy and data-mining residue.
- **Factor crowding.** A published premium is an arbitrage with a half-life: once it is known and capitalized by others, the mispricing it exploited compresses. The value premium that Fama–French measured on 1963–1990 data is thinner on 2010s data - not because the accounting stopped, but because the factor became crowded.
- **Look-ahead and survivorship bias in construction.** Using *restated* (future-corrected) accounting data leaks the future into the "historical" backtest; using only firms that *survived* to today drops the ones that went bankrupt. Both inflate the measured premium exactly as if you had cheated, without touching a line of fraudulent code.

---

### 2. Mathematical Ground Truth & Derivations

**Multiple testing - the familywise-error explosion.** Suppose a *null* world with no real alpha. Testing $M$ independent candidate factors, each with a per-test false-positive rate $\alpha$, produces an expected number of false discoveries:

$$
\mathbb{E}[\text{false discoveries}] \approx M\alpha, \qquad
P(\text{at least one false discovery}) \approx 1-(1-\alpha)^M \xrightarrow[M \text{ large}]{} 1.
$$

With $\alpha=5\%$ and $M=200$, the chance of *some* spurious "premium" is effectively 100%. The standard remedy is the multiple-testing correction - the familywise or false-discovery-rate control that [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] formalizes.

**Look-ahead bias.** If book value is restated (write-downs recognized with hindsight), the *measured* B/M uses information unavailable at the sort date:

$$
\text{B/M}_\text{measured} = \frac{\text{BE}_\text{restated}}{\text{ME}} \neq \frac{\text{BE}_\text{as-reported}}{\text{ME}} = \text{B/M}_\text{tradable}.
$$

Because restated book values are lower (write-downs), the "cheapest" basket looks even cheaper in hindsight - the value premium measured on restated data is overstated. Point-in-time (as-reported) data is the only unbiased input.

**Survivorship.** Estimating the premium on the set of firms that exist *today* drops the firms that delisted by going bankrupt - which are disproportionately the *loser* tail of a value screen. The measured spread is biased upward by exactly the mass of the missing losers.

---

### 3. Computational Implementation - the biases, demonstrated, stdlib only

Two simulations. The first runs **200 random candidate factors** against a *null* universe (iid normal returns, no real alpha) and shows the data-mining mirage: the mean factor earns ~nothing, but the *best* of 200 "earns" +40%/yr - pure noise, manufactured by selection. The second shows **look-ahead bias**: a value screen on restated book values makes the cheap basket look cheaper than it really was.





*The two numbers to stare at.* In a world where **no factor works**, the average candidate earns a negligible +1.58%/yr - but simply *picking the best of 200* manufactures a +39.93%/yr "premium" out of pure noise. That gap (≈40 points) is the entire price of data mining. And on the value screen, restated book values drop the cheap-basket's B/M from 0.465 to 0.321 - the premium you'd measure with hindsight data is inflated by exactly that falseness.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Data mining / multiple testing (first principle: many tests, one null).** Test enough characteristics and a premium is guaranteed to appear by chance. *Discipline:* pre-register the hypothesis, control for multiple testing (familywise / FDR / deflated Sharpe), and demand out-of-sample confirmation. Green, Hand & Zhang's census is the map of how much of the "discovery" catalog is redundant.
2. **Factor crowding / decay (first principle: arbitrage has a half-life).** A published, capitalized premium compresses; the value premium's post-1990 weakening is the canonical example. *Discipline:* expect a published factor to be thinner than its discovery sample, and stress-test on recent, post-publication data.
3. **Look-ahead bias (first principle: no future information at the sort date).** Restated fundamentals leak the future into the backtest. *Discipline:* point-in-time, as-reported data only - [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]].
4. **Survivorship bias (first principle: the losers delist).** A value screen's losers go bankrupt and vanish from today's universe; measuring on survivors inflates the spread. *Discipline:* include delisted firms and their terminal returns.
5. **Redundancy across factors (first principle: correlated signals double-count).** Many "distinct" characteristics are the same underlying risk in different clothes. *Discipline:* check the correlation structure and prefer the parsimonious set - the 10-signal model in Green–Hand–Zhang over the full census.

---

### 5. References

- **Green, Jeremiah; Hand, John R. M. & Zhang, X. Frank**: "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns" (*RFS*, 2017)
- **Fama, Eugene & French, Kenneth**: "Choosing Factors" (*JFE*, 2018)
- **Bailey, Borwein, López de Prado & Zhu**: "The Probability of Backtest Overfitting" (*J. Computational Finance*, 2017)
- **Hou, Xue & Zhang**: "Replicating Anomalies" (*RFS*, 2020)
- **Novy-Marx, Robert**: "Backtesting Strategies Based on Multiple Signals" (working paper)
- **Loughran & McDonald**: "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks" (*JF*, 2011)

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Forward: [[fundamentals-accounting/quantitative-fundamental-investing/06-advanced-extensions|06 · Advanced Extensions (factor models, combining)]]
- Data layer: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (point-in-time hygiene) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (restatements, manipulation)
- Backtesting layer: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
