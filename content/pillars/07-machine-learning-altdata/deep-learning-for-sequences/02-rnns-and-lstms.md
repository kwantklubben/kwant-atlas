---
title: "7.6.2 Recurrent Networks"
tags:
  - pillar-machine-learning
  - deep-learning-for-sequences
  - rnn
  - lstm
  - vanishing-gradient
  - bptt
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/01-from-zero-intuition|01 · From Zero]] (the state idea) and [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (the chain rule).

---

### 1. Intuition & Practical Objective

A recurrent network is a state machine with **shared weights**: at every step it reads the input $x_t$, combines it with its current memory $h_{t-1}$, and produces a new memory $h_t$. Because the *same* cell is applied at every time step, the model is compact and can in principle remember arbitrarily far back. In practice the *original* RNN could not - its memory decays geometrically with distance because the gradient used to train it vanishes (§3: $|{\partial h_T}/{\partial h_0}|\sim10^{-27}$ at $T{=}50$). **Long Short-Term Memory (LSTM)** solved this with a second, *additive* memory channel - the cell state $C_t$ - gated by learned forget/input/output gates. That single change is why recurrence became usable for trading-length sequences at all.

The practical objective: understand (a) what a recurrent cell computes, (b) *why* the naive version fails, and (c) how the gates fix it - so you can read LSTM/GRU code and reason about what the model can and cannot learn from a financial series.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The vanilla RNN and its unrolled graph

$$
h_t=\tanh\!\big(W h_{t-1}+U x_t+b_h\big),\qquad \hat y_t=\operatorname{softmax}\!\big(V h_t+b_y\big).
$$

The model is a deep network whose depth equals the sequence length $T$, with all layers sharing $W$. Training is **backpropagation through time (BPTT)**: unroll the graph and apply the chain rule.

#### 2.2 Why the gradient vanishes (or explodes)

The gradient of any loss at time $T$ w.r.t. an early state is a product of per-step Jacobians:

$$
\frac{\partial h_T}{\partial h_k}=\prod_{t=k+1}^{T}\frac{\partial h_t}{\partial h_{t-1}}
=\prod_{t=k+1}^{T}\operatorname{diag}\!\big(1-h_t^2\big)\,W .
$$

Each factor is a matrix whose norm is at most $\|W\|\cdot\max|\tanh'|\le\|W\|$. Therefore:

$$
\Big\|\frac{\partial h_T}{\partial h_0}\Big\|\;\le\;\|W\|^{T}\quad\Longrightarrow\quad
\begin{cases}\|W\|<1: & \text{gradient}\to 0\ \text{(vanishes)}\\ \|W\|>1: & \text{gradient}\to\infty\ \text{(explodes)}\end{cases}
$$

Because $\tanh'\le1$ and the recurrence multiplies, the **product of many $<1$ factors decays geometrically** - the network effectively cannot learn dependencies more than a handful of steps long. This is the Bengio–Simard–Frasconi (1994) result, and it is the single reason recurrence was considered impractical for long sequences until LSTM.

#### 2.3 LSTM gates (Hochreiter & Schmidhuber 1997)

The fix is a **second state $C_t$** whose update is *additive*, not multiplicative, and gated:

$$
\begin{aligned}
f_t&=\sigma\!\big(W_f h_{t-1}+U_f x_t+b_f\big) &&\text{(forget: how much of }C_{t-1}\text{ to keep)}\\
i_t&=\sigma\!\big(W_i h_{t-1}+U_i x_t+b_i\big) &&\text{(input: how much new info to write)}\\
\tilde C_t&=\tanh\!\big(W_c h_{t-1}+U_c x_t+b_c\big) &&\text{(candidate cell content)}\\
C_t&=f_t\odot C_{t-1}+i_t\odot\tilde C_t &&\text{(additive cell update)}\\
o_t&=\sigma\!\big(W_o h_{t-1}+U_o x_t+b_o\big),\qquad h_t=o_t\odot\tanh(C_t) &&\text{(output gate)}\\
\end{aligned}
$$

The crucial term is the cell update. The gradient along the **cell path** is

$$
\frac{\partial C_T}{\partial C_t}=\prod_{s=t+1}^{T}f_s ,
$$

a product of *gate* values (not of weights times saturating derivatives). If the forget gate learns $f_s\approx1$, the gradient passes essentially **undamped across arbitrary distances** - the **constant-error-carousel (CEC)**. There is no $\|W\|^T$ penalty on this path; the gates can *learn* the memory horizon instead of having it imposed by the weight norm. The GRU (Cho et al. 2014) achieves a similar effect with two gates and a single state (§06).

> **A subtlety.** The CEC solves the *optimisation* problem (training long-range dependencies), not the *statistical* problem (overfitting with little data). An LSTM can now *fit* a long memory; whether that memory generalises is a question about data, addressed in [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation - LSTM forward pass and the vanishing gradient

Stdlib + `numpy`. Part A runs a hand-weighted LSTM forward and prints every gate at each step; Part B measures the gradient magnitude $|{\partial h_T}/{\partial h_0}|$ for a vanilla RNN against the LSTM cell path $\prod f_t$.




Read it as the derivation in numbers. The vanilla RNN at $W{=}0.9$ loses seven orders of magnitude between $T{=}10$ ($8.6\times10^{-4}$) and $T{=}20$ ($8.7\times10^{-11}$) - the 20th-step dependency carries essentially zero gradient, so the cell can never learn it. The LSTM cell path with $f{=}0.99$ still transmits **$0.605$** of the gradient at $T{=}50$ - $26$ orders of magnitude larger. That gap *is* the LSTM.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Vanishing/exploding gradients (the disease LSTM treats).** A vanilla RNN cannot learn long-range structure; see the table. Exploding gradients (large $W$, or the $1.2$ row's transient growth) are handled separately by **gradient clipping** (Pascanu et al. 2013) - a hard cap on the gradient norm per step.
2. **Gates do not create signal.** An LSTM can *represent* a long memory; with a low-SNR target it will happily fit spurious long memories that don't generalise. Architecture fixes optimisation, not statistics (→ [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **BPTT is sequential and slow.** Recurrence cannot be parallelised over time (step $t$ needs step $t-1$), which is both a training-time and, for high-frequency trading, an **inference-latency** problem - the motivation for the convolutional and attention alternatives in pages 03 and 06.
4. **Truncated BPTT biases the gradient.** In practice you unroll only $k$ steps to fit memory; that reintroduces exactly the truncation the LSTM was meant to avoid, so the *effective* horizon is your chosen unroll length, not the architecture.
5. **Numerical saturating tanh/sigmoid.** Early in training, gates sit near $0.5$ and the cell state can drift; input scaling (standardising features) matters as much here as in feed-forward nets.

---

### 5. References

- **Hochreiter, S. & Schmidhuber, J.** (1997), *Long Short-Term Memory*, Neural Computation 9(8):1735–1780
- **Goodfellow, Bengio & Courville**, *Deep Learning*, **Ch. 10** (§10.2: the recurrence, BPTT, the vanishing-gradient discussion; the LSTM/GRU subsection)
- **Bengio, Simard & Frasconi** (1994), *Learning Long-Term Dependencies with Gradient Descent is Difficult*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, **Ch. 11** (§11.4–11.5: back-propagation, weight decay, early stopping)
- **Bai, Kolter & Koltun** (2018), *An Empirical Evaluation of Generic Convolutional and Recurrent Networks*, arXiv:1803.01271

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/03-attention-and-transformers|03 · Attention & Transformers]] (the non-recurrent route to long-range memory) · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/04-autoencoders-for-factors|04 · Autoencoders for Factors]]
- Latency reality: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] (why sequential inference is expensive)
- Optimisation base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
