---
title: "7.6 Deep Learning for Sequences"
tags:
  - pillar-machine-learning
  - deep-learning-for-sequences
  - lstm
  - attention
  - autoencoders
  - index-hub
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (gradients, backpropagation) and [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] (why finance is a hard learning problem). The classical ancestor of every model here - the linear state-space / Kalman filter - lives at [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A cross-sectional model asks: *given today's features, what is tomorrow's expected return?* A **sequence model** asks a strictly harder question: *given today's features **and the path that led here**, what comes next?* That extra word - the path - is the whole subject. Financial data arrives as an ordered stream (tick arrivals, order-book updates, bar returns, macro releases), and the ordering itself carries information that an order-blind model throws away.

This folder is the topic-hub for **deep learning for sequential data** in Kwant-Atlas. It (a) gives the **fast architecture/formula lookup** below - job #1 of a hub - and (b) routes you to six sub-pages that walk you from raw intuition through the recurrent, attention, and autoencoder families, the low-SNR reality that governs whether to use any of them, and the extensions (TCN, GRU, DeepAR, TFT, DeepLOB).

> **The one-sentence essence.** "A sequence model is a *learned state machine*: a recurrence (RNN/LSTM) or an attention mechanism (Transformer, TCN) compresses the entire past into a state that predicts the future - but in finance the state is learned from a **low-signal, non-stationary** stream, so the binding constraint is almost never architecture, it is **data and validation discipline**."

The honest framing up front, because it decides everything after it: **deep sequence models are not automatically better than gradient-boosted trees in finance.** On the medium-frequency tabular problems that dominate the industry, well-tuned trees match or beat deep nets (Gu, Kelly & Xiu 2020 tested both). Deep sequence models earn their place only where there is *raw ordered structure with no good manual features* - limit-order-book microstructure, high-frequency tick streams - where the sample size $N$ reaches $10^6$–$10^9$ and the sequence itself is the feature.

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $x_t$ input, $h_t$ hidden state, $C_t$ LSTM cell state, $\sigma$ logistic sigmoid, $\odot$ Hadamard (element-wise) product, $W/U$ recurrent/input weight matrices, $d_k$ attention head dimension, $M$ causal mask, $L$ layers, $K$ filter width. **All checks below were re-executed and reproduced exactly (see §3).**

| Quantity | Formula | Verified check |
|---|---|---|
| **Vanilla RNN** state | $h_t=\tanh\!\big(W h_{t-1}+U x_t+b\big)$ | - |
| **BPTT gradient chain** | $\dfrac{\partial h_T}{\partial h_0}=\displaystyle\prod_{t=1}^{T}\operatorname{diag}\!\big(1-h_t^2\big)\,W$ | $W{=}0.9,T{=}20\Rightarrow 8.66\times10^{-11}$ |
| Exploding-gradient bound | $\|\partial h_T/\partial h_0\|\le\|W\|^T$ | grows when $\|W\|>1$ |
| **LSTM gates** | $\begin{aligned}f_t&=\sigma(W_f h_{t-1}+U_f x_t+b_f)\\ i_t&=\sigma(W_i h_{t-1}+U_i x_t+b_i)\\ o_t&=\sigma(W_o h_{t-1}+U_o x_t+b_o)\end{aligned}$ | forget/input/output, all in $(0,1)$ |
| LSTM candidate & update | $\tilde C_t=\tanh(W_c h_{t-1}+U_c x_t+b_c)$; $\;C_t=f_t\odot C_{t-1}+i_t\odot\tilde C_t$ | additive (constant-error-carousel) path |
| LSTM hidden output | $h_t=o_t\odot\tanh(C_t)$ | - |
| **CEC gradient** (cell path) | $\dfrac{\partial C_T}{\partial C_0}=\displaystyle\prod_{t=1}^{T}f_t$ | $f{=}0.99,T{=}50\Rightarrow 0.605$ (vs $5.4\times10^{-27}$ RNN at the same $T{=}50$) |
| **Scaled dot-product attention** | $\operatorname{Attn}(Q,K,V)=\operatorname{softmax}\!\Big(\dfrac{QK^\top}{\sqrt{d_k}}+M\Big)V$ | rows sum to $1$; $\max(\text{upper-tri})=0$ |
| Causal mask | $M_{ij}=-\infty$ for $j>i$, $0$ otherwise | strictly no look-ahead |
| Multi-head attention | $\operatorname{Concat}(\text{head}_1,\dots,\text{head}_h)W^O$ | $h$ parallel subspaces |
| **Linear autoencoder loss** | $\min_{E,D}\;\tfrac1n\sum_i\|x_i-D\,E\,x_i\|_2^2$ | trained AE MSE $=$ PCA optimum to $-0.000\%$ |
| Linear-AE optimum | $\hat D\hat E$ spans the top-$k$ SVD subspace (Eckart–Young) | $\cos(\text{principal angles})=[1,1,1]$ |
| Sparse-AE penalty | $L=\|x-Dz\|_2^2+\lambda\|z\|_1$ | drives most code units to $0$ |
| **TCN dilated causal conv** | $(F*_d x)(t)=\sum_{k=0}^{K-1}f_k\,x_{t-d\,k}$ | output$[t]$ depends on $s\le t$ only |
| TCN receptive field | $R=(K-1)\big(2^{L}-1\big)+1$ | $K{=}2,L{=}3\Rightarrow R=8$ |

> **Critical decision caveat (AFML Ch. 1; Gu–Kelly–Xiu 2020).** The lookup table tells you *how* to build these models, not *whether* to. Before reaching for any row above, check the **data budget**: with $N$ effective (non-overlapping) samples and $p$ parameters you need $N\gg p$, and financial returns have an *effective* sample size far smaller than the calendar count because of serial correlation and non-stationarity. Section 05 turns this into a decision rule.

---

### 3. Computational Implementation - the architecture probe

Runs on `numpy` + stdlib only. It reproduces the four headline numbers in §2 in a single pass: the vanishing-gradient gap between a vanilla RNN and an LSTM, the causal property of masked attention, and the TCN receptive field.




Read it as the folder's thesis in numbers: the vanilla RNN's gradient from 50 steps ago is $\sim 10^{-27}$ (vanished - it cannot learn long-range dependencies at all), while the LSTM's *cell* gradient is still $0.605$ (the gates keep the memory channel open). Attention sidesteps the recurrence entirely and builds a strictly causal, row-normalised weighted average. The TCN reaches 8 steps into the past with only 3 layers and 2-wide filters.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the decision rule and practice checklist live in [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Data hunger vs low SNR** - deep nets carry $10^4$–$10^8$ parameters; that needs an *effective* sample count finance rarely supplies, so they overfit where trees do not ($\S$05).
2. **Non-stationarity** - the data-generating process shifts (regimes, arbitrage decay); a sequence model trained on regime A can have *negative* $R^2$ on regime B ($\S$05).
3. **Look-ahead leakage** - attention and recurrence both invite subtle future-peeking (no causal mask, or target leakage); this is the same disease the [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]] folder treats, in architectural clothing ($\S$03).
4. **Opacity & unhedgeable model risk** - a black-box sequence model is hard to reason about when it breaks, and breaks silently under regime change ($\S$05).

---

### 5. Canonical Literature & Study References

- **Goodfellow, Bengio & Courville**: *Deep Learning*, MIT Press (2016) - **Ch. 10 "Sequence Modeling: Recurrent and Recursive Nets"** (unrolling, BPTT, the vanishing-gradient problem, LSTM/GRU, the encoder–decoder family). *The core theory reference for this folder; the free HTML edition is at deeplearningbook.org (the MIT Press PDF is print-only - the corpus holds only the 66-page front matter).*
- **Hochreiter, Sepp & Schmidhuber, Jürgen**: *Long Short-Term Memory*, Neural Computation 9(8):1735–1780 (1997) - the LSTM paper; the constant-error-carousel argument is the reason §2's CEC gradient survives.
- **Vaswani et al.**: *Attention Is All You Need*, NeurIPS (2017) - scaled dot-product and multi-head attention; the Transformer.
- **Bai, Kolter & Koltun**: *An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling*, arXiv:1803.01271 (2018) - defines the TCN; the cheap, parallelisable alternative to recurrence.
- **Lim, Arık, Loeff & Pfister**: *Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting*, IJF 37(4):1748–1764 (2021) - the attention-based, interpretable multi-horizon architecture this pillar points to.
- **Heaton, Polson & Witte**: *Deep learning for finance: deep portfolios*, Applied Stochastic Models in Business and Industry 33(1):3–12 (2017) - the finance-DL canon: autoencoders/deep nets for factor construction and portfolio weights.
- **Zhang, Zohren & Roberts**: *DeepLOB: Deep Convolutional Neural Networks for Limit Order Books*, IEEE Trans. Signal Processing 67(11):3001–3012 (2019), arXiv:1808.03668 - the canonical CNN+LSTM microstructure model; the case where deep sequence learning demonstrably wins.
- **López de Prado, Marcos**: *Advances in Financial Machine Learning* (Wiley, 2018) - **Ch. 1 "Financial Machine Learning as a Distinct Subject"** and the *10 reasons most ML funds fail*. *Correction of a common mis-citation:* AFML contains **no autoencoder or RNN chapter** - its Ch. 19 is "Microstructural Features" and Ch. 20 is "Multiprocessing and Vectorization", none of which concerns deep learning; and AFML Ch. 1 explicitly declines to cover "the latest reincarnation of deep, recurrent, or convolutional neural networks", arguing the binding problems are data-structure, labelling, and validation ones. Cite it here for the **low-SNR / overfitting framing**, not for DL architecture.
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009) - **Ch. 11 "Neural Networks"** (PPR→MLP, back-propagation, weight decay and early stopping as the anti-overfit recipe). *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
- Classical sequence model (the linear ancestor): [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] - the Kalman filter is a *state-space* sequence model with a closed-form update; the RNN is its nonlinear, learned cousin.
- Feature side (what the sequence model replaces or consumes): [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]]
- Sibling (same pillar): [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged Cross-Validation & Backtest Hygiene]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
- Sub-pages (in-folder): 01 From Zero · 02 RNNs & LSTMs · 03 Attention & Transformers · 04 Autoencoders for Factors · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05]]
