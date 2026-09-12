---
title: "7.6.6 Advanced Extensions"
tags:
  - pillar-machine-learning
  - deep-learning-for-sequences
  - tcn
  - gru
  - seq2seq
  - deepar
  - tft
  - deeplob
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/02-rnns-and-lstms|02 · RNNs & LSTMs]] and [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/03-attention-and-transformers|03 · Attention & Transformers]].

---

### 1. Intuition & Practical Objective

The previous pages gave the building blocks (recurrence, attention, autoencoding). This page is the **launchpad**: the architectures practitioners actually deploy for financial sequences, and the bridges to the topics that own each one. It covers four families:

1. **Temporal Convolutional Networks (TCN)** - replace recurrence with *causal dilated convolutions*: parallel, stable, with an exponentially growing receptive field.
2. **GRU** - the LSTM's leaner sibling (two gates, one state), often the practical default.
3. **Encoder–decoder / seq2seq with attention** - predict a whole *path* (multi-horizon), not a point.
4. **Probabilistic & microstructure models** - **DeepAR** (full predictive distributions), **TFT** (interpretable multi-horizon attention), and **DeepLOB** (CNN+LSTM over limit-order books).

Everything farther - reinforcement learning for trading, neural state-space models, foundation models for finance - is linked from here.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 TCN: causal dilated convolution (Bai, Kolter & Koltun 2018)

A TCN applies a stack of 1-D convolutions that are **causal** (no future leakage) and **dilated** (skip steps):

$$
(F*_d x)(t)=\sum_{k=0}^{K-1}f_k\;x_{\,t-d\,k}.
$$

With dilations $d\in\{1,2,4,\dots\}$ growing exponentially and $L$ layers of width $K$, the **receptive field** is

$$
\boxed{\;R=(K-1)\big(2^{L}-1\big)+1\;}
$$

so $K{=}2,\ L{=}3\Rightarrow R=8$ steps (verified in §3). The receptive field grows *exponentially* in depth while parameters grow only linearly - the reason a few TCN layers cover a long history. Each residual block is $z=\operatorname{Dropout}(\sigma(\text{WeightNorm}(F*_d x)))$ plus a skip connection, and the whole net is trained with plain backprop (no BPTT), so it **parallelises over time** - a decisive advantage over the RNN's sequential inference.

#### 2.2 GRU (Cho et al. 2014): two gates, one state

$$
z_t=\sigma(W_z h_{t-1}+U_z x_t),\qquad
r_t=\sigma(W_r h_{t-1}+U_r x_t),
$$
$$
\tilde h_t=\tanh\!\big(W(r_t\odot h_{t-1})+U x_t\big),\qquad
h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t .
$$

The GRU drops the LSTM's separate cell state and output gate. The **update gate** $z_t$ interpolates between keeping the old state and writing the new one - a single knob doing the job of the LSTM's forget+input pair. Empirically GRU and LSTM are close; GRU is cheaper and the common default when you do not need long memory.

#### 2.3 Encoder–decoder (seq2seq) with attention

To predict a *sequence* $y_{1:m}$ from $x_{1:T}$ (e.g. a multi-horizon return path), an encoder compresses the input and a decoder generates the output step by step, attending to the encoder states:

$$
c_i=\sum_{t=1}^{T}\alpha_{it}h_t,\qquad \alpha_{it}=\frac{\exp(\text{score}(s_{i-1},h_t))}{\sum_{t'}\exp(\text{score}(s_{i-1},h_{t'}))}.
$$

#### 2.4 Probabilistic, multi-horizon and microstructure models

- **DeepAR** (Salinas et al. 2020) - an autoregressive RNN whose output is a *distribution* parameterised at each step (e.g. $\hat\mu_t,\hat\sigma_t$ of a Gaussian, or negative-binomial counts). It is trained by maximising the likelihood, so it produces **full predictive distributions** - the right object for regime-aware position sizing and risk.
- **TFT** (Lim et al. 2021) - adds *variable selection*, *static covariate encoders*, and *interpretable multi-horizon attention* on top of an LSTM encoder/decoder; designed for the messy, mixed-frequency, covariate-rich series finance actually has.
- **DeepLOB** (Zhang, Zohren & Roberts 2019) - a deliberately *not-full-attention* architecture: convolutional filters capture the **spatial** structure of the limit-order book, LSTM layers capture **temporal** dependence. It beats prior methods on the FI-2010 benchmark and transfers across instruments, and is the canonical demonstration that deep sequence learning works when the data is deep and ordered.

---

### 3. Computational Implementation - causal dilated conv, receptive field, and a GRU

`numpy` + stdlib. Part A builds a causal dilated convolution from scratch, prints the output, verifies the receptive field, and *proves* causality by perturbing the last input and checking which outputs move; Part B runs a GRU forward pass.




Read it as the TCN's two defining properties, verified. The three-layer dilated stack with dilations $1,2,4$ has a receptive field of exactly **$8$** steps ($R=(K-1)(2^L-1)+1=8$), and the output is a smoothed ramp that "catches up" from the zero-padding. The causality check is the important one: perturbing input $[15]$ (the last element) changes **only** output $[15]$ - nothing downstream, nothing upstream, because there is nothing downstream. `output[t]` depends on inputs $s\le t$ only, which is exactly the property a trading model requires and which the GRU (Part C) enforces through its interpolation gate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Transformer everywhere."** Full attention is $O(T^2)$; a tick-level LOB series is far too long. The microstructure answer is convolution + local recurrence (DeepLOB), not global attention. Match the architecture to the length scale.
2. **Receptive field ≠ useful memory.** A TCN with $R=8$ cannot see a 200-step regime; widen dilations or add layers deliberately, and remember the *effective* dependency is whatever the data supports.
3. **Seq2seq exposes you to compounding error.** An autoregressive decoder fed its own predictions drifts; for multi-horizon forecasting prefer direct multi-horizon heads (TFT) or scheduled sampling.
4. **Probabilistic ≠ risk-managed.** DeepAR gives you a predictive distribution, but if the distribution is mis-specified (fat tails ignored, regime unmodelled) the "uncertainty" is false comfort. Validate calibration, not just point accuracy.
5. **Transfer/overfit tension.** DeepLOB transfers across instruments *because* order-book structure is universal; a model confounded by instrument-specific quirks will not. Test cross-instrument transfer explicitly.
6. **The bridge to RL is not free.** Reinforcement-learning-for-trading (page-linked) inherits every problem here - low SNR, non-stationarity, and now *non-stationary reward* - plus its own (sample inefficiency, reward hacking). Treat it as the same discipline, one layer up.
7. **Latency budget.** Even TCNs must respect the decision deadline; verify per-step inference cost against the [[pillars/02-algorithmic-hft/low-latency-systems-architecture|low-latency]] budget before deployment.

---

### 5. Canonical Literature & Study References

- **Bai, Shaojie, Kolter, J. Zico & Koltun, Vladlen** (2018), *An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling*, arXiv:1803.01271 - the TCN; causal dilated convolutions and the receptive-field result.
- **Cho, Kyunghyun et al.** (2014), *Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation*, EMNLP - the GRU.
- **Salinas, David et al.** (2020), *DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks*, International Journal of Forecasting (arXiv:1704.04110) - full predictive distributions from an autoregressive RNN.
- **Lim, Bryan, Arık, Sercan Ö., Loeff, Nicolas & Pfister, Tomas** (2021), *Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting*, IJF 37(4):1748–1764 (arXiv:1912.09363) - interpretable multi-horizon attention with static covariates.
- **Zhang, Zihao, Zohren, Stefan & Roberts, Stephen** (2019), *DeepLOB: Deep Convolutional Neural Networks for Limit Order Books*, IEEE TSP 67(11):3001–3012, arXiv:1808.03668 - the canonical CNN+LSTM microstructure model (the "Zhang 2020" extended treatment is the Oxford-Man follow-on).
- **Goodfellow, Bengio & Courville**, *Deep Learning*, **Ch. 10** (§10.4 encoder–decoder, attention) and **Ch. 9** (convolutional structure - the basis of the TCN and DeepLOB's spatial filters).
- **Sutton, Richard S. & Barto, Andrew G.** (2018), *Reinforcement Learning: An Introduction* (2nd ed.) - the bridge to RL-for-trading; the sequential-decision formalisation of the same data.
- **Microsoft Qlib** (arXiv:2009.11189) - the reference implementation: LightGBM/XGBoost/CatBoost **and** LSTM/GRU/Transformer/TFT backends with purged-style evaluation; the closest thing to a runnable embodiment of Pillar 7's stack.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/03-attention-and-transformers|03 · Attention & Transformers]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Index Hub]]
- Classical state-space cousin (neural SSMs / neural ODEs generalise it): [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]]
- Microstructure data & latency: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/06-market-making/index|Market Making]]
- Regime-aware uncertainty: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]]
- NLP sequence models (same attention machinery): [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Financial NLP & Transcripts]]
