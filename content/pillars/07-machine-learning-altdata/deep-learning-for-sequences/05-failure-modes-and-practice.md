---
title: "7.6.5 Failure Modes & Practice"
tags:
  - pillar-machine-learning
  - deep-learning-for-sequences
  - failure-modes
  - low-snr
  - overfitting
  - non-stationarity
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/02-rnns-and-lstms|02 · RNNs & LSTMs]] and [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/04-autoencoders-for-factors|04 · Autoencoders for Factors]].

---

### 1. Intuition & Practical Objective

Every architecture on the previous pages is *expressive*. Expressiveness is a liability in finance, where the signal-to-noise ratio is microscopic and the data-generating process moves under your feet. This page is the **decision gate**: it quantifies the three ways deep sequence models fail in finance, ties each to a first principle, and ends with a concrete rule for **when DL is justified and when a gradient-boosted tree is simply the better tool**.

The three failures, in one line each:

1. **Data hunger** - deep nets have far more parameters than finance can supply *effective* samples for, so they overfit where a shallow model (or a tree with depth limits) does not.
2. **Non-stationarity** - the process that generated the training set is not the process you will trade; a model can fit regime A perfectly and have *negative* $R^2$ on regime B.
3. **Opacity** - a learned sequence model is hard to debug, hard to attribute, and fails silently under regime change.

The objective is the discipline of *measuring* all three before trusting the model - and the four-row decision table in §2.3.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Data hunger: the effective-sample budget

Classical learning theory bounds generalisation error by model complexity over sample size. For a model with $p$ free parameters and $N$ training examples, the gap between training and test error grows roughly like $\sqrt{p/N}$. Deep sequence models sit at $p\sim10^{4}$–$10^{8}$; finance supplies daily returns at $N\sim10^{3}$ (twenty years of one asset) unless you go to high frequency.

Worse, the **effective** sample size is much smaller than the calendar count, because financial observations are serially correlated. If the lag-$1$ autocorrelation is $\rho$, the effective size is roughly

$$
N_{\text{eff}}\approx N\,\frac{1-\rho}{1+\rho}.
$$

A daily return series with $\rho=0.1$ over $N=2500$ days has $N_{\text{eff}}\approx2045$; a 1-minute series with heavy overlap can lose an order of magnitude. This is why the binding constraint is *not* architecture: it is how many genuinely independent, informative observations exist.

The levers that trade expressiveness for robustness (all from ESL Ch. 11):

- **Weight decay / $L_2$ regularisation** - penalise $\|W\|^2$; keeps weights small, shrinks the effective complexity.
- **Early stopping** - stop when validation error turns up; equivalent to a shrunk model.
- **Dropout** - randomly zero activations during training; a variance-reduction device.
- **Small models** - one layer with few units usually beats a deep stack on financial $N$.

#### 2.2 Non-stationarity: the distribution moves

Assume returns follow a regime-switching process: at each time the process is in one of a few regimes, each with its own dynamics (see [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification]] for the HMM machinery). A model trained on regime $A$ estimates the regime-$A$ conditional. Applied to regime $B$ it is mis-specified, and the out-of-sample $R^2$ can be *worse than predicting the mean* ($R^2<0$). §4 quantifies this: $R^2=+0.76$ in-regime, $-0.68$ out-of-regime.

The remedy is not a better architecture but a **validation regime**: walk-forward splits, purged/embargoed CV, refit windows, and regime-aware features - i.e. the practice of the sibling [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]] folder.

#### 2.3 When DL is justified vs trees - the decision rule

| Condition | Use trees (LightGBM/XGBoost) | Deep sequence model earns its place |
|---|---|---|
| Data type | tabular, cross-sectional factors | raw ordered stream (ticks, LOB, waveform) |
| Effective $N$ | $10^2$–$10^4$ | $10^6$–$10^9$ |
| Signal strength | very low (Sharpe from many weak bets) | higher per-event (microstructure edge) |
| Manual features | good features exist / are cheap | features are the hard part; let the net learn them |
| Latency | not binding, or modest | must be fast (or use TCN, not RNN) |
| Interpretability need | high | lower, or attention provides a diagnostic |

The empirical anchor: **Gu, Kelly & Xiu (2020)** ran a horse race of models on the same cross-sectional return data and found **gradient-boosted trees among the best performers**, with neural nets competitive only with heavy tuning and much more data - a direct refutation of "deep learning is automatically better." Deep sequence models win where the *sequence itself is the feature* - **DeepLOB** (Zhang et al. 2019) on limit-order-book data is the canonical case: CNN + LSTM over a deep, ordered order book, with enough ticks to justify the parameters.

---

### 3. Computational Implementation - the three failures in numbers

`numpy` + stdlib. Part A shows overfitting on a **pure-noise** target as the feature count $p$ approaches the sample count; Part B shows ridge (weight decay) repairing it; Part C shows non-stationarity - a model fit on one regime evaluated on another.




Read it as the whole folder's cautionary tale. In Part A the target is **pure noise** - there is *nothing* to learn - yet training $R^2$ climbs to $1.000$ as $p\to N_{\text{train}}$, while out-of-sample $R^2$ collapses to $-834$: a model with more parameters than data memorises the noise exactly and generalises catastrophically. (A deep sequence net is this, with $p$ in the millions.) Part B shows the cure: **weight decay** pulls OOS $R^2$ from $-409$ back toward $0$ - the honest value, since $y$ is unrelated to $X$ - by shrinking the parameters. Part C shows non-stationarity: the model recovers regime A's coefficients almost exactly ($0.594,0.307$ vs true $0.60,0.30$) and scores $R^2=+0.757$ *in* regime, but $-0.680$ on regime B - worse than predicting the mean, because the fitted rule actively mis-predicts when the dynamics flip.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Data hunger / overfitting (the $\sqrt{p/N}$ wall).** Deep nets need effective samples finance rarely supplies. Mitigations: weight decay, dropout, early stopping, and *smaller models first* (ESL Ch. 11). The $p\to N$ blow-up above is the mechanism.
2. **Non-stationarity (the process moves).** A model is a snapshot of a process that changes; without walk-forward/purged validation and rolling refits it silently degrades. Measured above: $+0.76\to-0.68$.
3. **Opacity (black-box model risk).** You cannot easily explain why a stacked LSTM changed its forecast, and it fails *silently*. Prefer interpretable architectures (attention diagnostics, monotone constraints, small trees) when the model feeds a risk decision; the pipeline-hygiene on this is the same discipline the pillar applies to trees.
4. **Look-ahead / leakage.** Both recurrence and attention invite future-peeking (missing causal mask; target leakage via overlapping labels). Always pair the model with the [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]] machinery.
5. **Data-snooping / selection bias.** Even an *honest* deep model is a draw from a search over architectures and hyper-parameters; the more configurations you tried, the higher the chance the winner is luck. Deflate the Sharpe over the number of trials ([[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).
6. **The architecture-is-not-the-problem illusion.** AFML Ch. 1's central warning: most ML funds fail on *data structure, labelling, and validation*, not because they chose LSTM over Transformer. A perfect architecture on leaked, mislabelled data is worthless.
7. **Latency / cost.** Sequential inference (RNN) is slow per step and full attention is $O(T^2)$; if the strategy needs microsecond decisions, the architecture must be a TCN or a small model, and the compute cost enters the alpha directly.

---

### 5. Canonical Literature & Study References

- **Gu, Kelly & Xiu** (2020), *Empirical Asset Pricing via Machine Learning*, Review of Financial Studies 33(5):2223–2273 - the horse race: gradient-boosted trees are among the best models on the same data deep nets are applied to; the empirical basis for §2.3.
- **López de Prado**, *Advances in Financial Machine Learning* (2018), **Ch. 1** and the *10 reasons most ML funds fail* - the low-SNR/overfitting framing and the "the bottlenecks are data, not architecture" warning. *Correction of a common mis-citation:* AFML has **no** deep-learning chapters (Ch. 19 = Microstructural Features, Ch. 20 = Multiprocessing), and Ch. 1 explicitly declines to cover deep/recurrent/convolutional nets.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, **Ch. 11** (§11.5: weight decay eq. 11.16, early stopping, input scaling, the nonconvex/multi-minima warnings) - the anti-overfit recipe used in §2.1.
- **Heaton, Polson & Witte** (2017), *Deep learning for finance: deep portfolios*, Appl. Stochastic Models Bus. Ind. 33(1):3–12 - the finance-DL canonical application and its data requirements.
- **Zhang, Zohren & Roberts** (2019), *DeepLOB*, IEEE TSP 67(11), arXiv:1808.03668 - the positive case: deep sequence learning that *does* generalise, because the microstructure data is deep and ordered and $N$ is large.
- **Zhang, Z.** (2020), *Deep Learning for Limit Order Books* / related Oxford-Man work - the extended treatment of LOB sequence learning; read alongside DeepLOB.
- **Bailey & López de Prado** (2014), *The Deflated Sharpe Ratio* - correcting reported performance for the number of trials (§4.5).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/04-autoencoders-for-factors|04 · Autoencoders for Factors]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/06-advanced-extensions|06 · Advanced Extensions]]
- The disease and its validation cure: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged Cross-Validation & Backtest Hygiene]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene (DSR/PBO)]]
- Why the SNR is low: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
- The tree alternative: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
- Regime machinery: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]]
