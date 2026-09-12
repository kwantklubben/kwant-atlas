---
title: "1.6.4 Triple-Barrier & Meta-Labeling"
tags:
  - pillar-quant-research
  - feature-engineering-and-labeling
  - triple-barrier
  - meta-labeling
  - bet-sizing
  - precision-recall
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/feature-engineering-and-labeling/03-target-labeling|03 · Target Labeling]].

---

### 1. Intuition & Practical Objective

Most desks already have a view on **direction** - from a fundamental model, an econometric equation, a technical rule, or a human's intuition. The open question is not *which way* but *whether to bet and how much*. Asked to predict direction, an ML model wastes its capacity re-learning something you already know, and doubles the ways to be wrong.

**Meta-labeling** (López de Prado §3.6) is the fix: build a **secondary** classifier on top of the primary (directional) model whose only job is to answer a binary question - *"if I take this bet, will it win?"* - with labels $\{0,1\}$. The primary decides the **side** (long/short); the secondary decides the **size** (including zero). This page builds the machinery end-to-end and shows - with a trained secondary model - the precision/recall trade-off it is designed to exploit.

Two ideas carry the page:

1. **Expand `getEvents` with a `side` argument.** Once the side is known, the horizontal barriers need no longer be symmetric: a long uses $pt$ on the upside and $sl$ on the downside; a short flips them. The label becomes binary: $1$ if the *primary bet* was profitable, $0$ otherwise.
2. **Meta-labeling trades recall for precision.** The primary is chosen to have **high recall** (it finds the opportunities); the secondary **filters the false positives**, raising **precision** and therefore the F1-score.

> **The one-sentence essence.** "Let the primary model say *long or short*, and train a second model on $\{0,1\}$ labels - *was that call profitable?* - so that ML only ever has to decide *size*, never *side*."

---

### 2. Mathematical Ground Truth & Derivations

**From triple-barrier to meta-label.** Given side $s_i\in\{-1,+1\}$ from the primary model at $t_{i,0}$, define the oriented barriers
$$
\text{upper}_i=P_{i,0}\big(1+pt\cdot\sigma_{t_{i,0}}\big),\qquad \text{lower}_i=P_{i,0}\big(1-sl\cdot\sigma_{t_{i,0}}\big),
$$
and the **meta-label** (LdP §3.6, Snippets 3.6–3.7)
$$
y^{\text{meta}}_i=\begin{cases}1 & \text{if the primary bet would have been profitable}\\ 0 & \text{otherwise}\end{cases}\ \in\{0,1\}.
$$
In code, the label is read off the first barrier touched *relative to the side*: if the upper barrier is first, a long wins and a short loses; if the lower is first, a long loses and a short wins; if the vertical barrier is first, the sign of the return decides. Symmetric barriers correspond to $pt=sl$; asymmetric ones ($pt\ne sl$, e.g. $[1,2]$) encode a directional payoff and are the recommended general choice.

**Precision, recall, F1 (the metrics that matter).** With the confusion matrix over the test set,
$$
\text{Precision}=\frac{TP}{TP+FP},\qquad \text{Recall}=\frac{TP}{TP+FN},\qquad F_1=2\frac{\text{Precision}\cdot\text{Recall}}{\text{Precision}+\text{Recall}}.
$$
Recall is the analogue of *power* in hypothesis testing; precision is the analogue of $1-$ (false-discovery rate). A primary model tuned for recall accepts many bets and therefore many losers. The secondary model raises precision by **passing** (predicting $0$) on the bets it believes will lose. If the secondary has genuine skill, precision rises at a controlled cost to recall, and the F1 improves where the strategy operates.

**From probability to size.** Once the secondary outputs $\hat p_i=\Pr(y^{\text{meta}}_i=1\mid \mathcal F_t)$, the bet size is a monotone function of $\hat p_i$ - from **0** (pass) below a threshold to a larger allocation above it. This is the interface to bet sizing (LdP Ch 10) and is the reason meta-labeling is described as "learning the size, not the side": the primary's $s_i$ fixes the sign, the secondary's $\hat p_i$ fixes the magnitude.

**Why it helps (LdP §3.7, four reasons).** (i) It puts ML on top of a *white box* (the primary model), addressing the black-box objection and serving "quantamental" desks. (ii) Overfitting is limited because ML never chooses the side. (iii) Side and size can be built by *different* models for *different* conditions (e.g. one secondary for longs, a different primary for shorts). (iv) Mispredicting the *size* of the bets you take - high accuracy on small bets, low accuracy on large ones - ruins a book regardless of directional skill, so a model dedicated to sizing is worth its own pipeline.

---

### 3. Computational Implementation - meta-labeling lifts precision (and F1)

This is a controlled experiment: an unknown world in which a feature $z$ genuinely carries signal about whether the primary bet wins. We fit a logistic-regression secondary model (plain gradient descent, standard library), with a **time-ordered** train/test split and **train-only** feature scaling, then compare precision/recall/F1 with and without the filter. (The controlled construction is deliberate - it isolates the *mechanism*; in real data the feature may carry little or no signal.)



Read the table as the method's shape. The primary bets on everything, with precision 0.517 and recall 1.000 (F1 0.682). The secondary at threshold 0.5 **filters out 850 of 1,600 bets**, raising precision to **0.721** while keeping recall 0.653 (F1 0.686). Push the threshold to 0.7 and precision reaches 0.829 - but recall collapses to 0.322, so F1 *falls*. That is the precision/recall frontier in one line: **the secondary's threshold is a strategy decision, and F1 - not accuracy - is the metric to optimise.** The learned slope $+1.174$ recovers the true $1.2$, confirming the secondary learned the signal rather than noise.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Meta-labels leak the primary's side into the features.** If a feature encodes the primary's direction (e.g. the sign of the signal that set $s_i$), the secondary learns to re-derive the primary rather than to filter it. Keep the meta-features about *when* the primary is right, not *what* it said.
2. **Symmetric-by-reflex barriers.** Meta-labeling's power comes partly from asymmetric $pt\ne sl$; forcing symmetry discards the payoff structure. Choose them from the strategy.
3. **Overfitting the secondary.** Because the primary fixed the side, the loss surface is flatter - but a small, noisy meta-dataset still overfits. Purge/embargo the CV and regularise (the `l2` term here).
4. **Threshold chosen on the test set.** The decision threshold must be selected out-of-sample or it is just another tuned parameter inflating the score (see [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).
5. **Assuming the secondary has skill.** On real data the meta-features may carry little signal; a secondary that filters at chance *reduces* the number of bets without raising precision, costing recall for nothing. Always compare to the unfiltered primary.
6. **Bet size ignored.** A $\{0,1\}$ filter is the crudest use of the secondary; the probability $\hat p_i$ should drive the *size*, not just the on/off switch (LdP Ch 10).

---

### 5. References

- **López de Prado, M.**: *Advances in Financial Machine Learning* (2018)
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning*
- **Gu, Kelly & Xiu** (2020): *Empirical Asset Pricing via Machine Learning*

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/feature-engineering-and-labeling/03-target-labeling|03 · Target Labeling]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Continue: [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/01-quantitative-research/feature-engineering-and-labeling/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged CV, PBO & Reality Checks]] (how to validate a secondary model) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (a natural "primary" model)
- Cross-pillar: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
