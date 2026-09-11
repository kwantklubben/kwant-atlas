---
title: "02 — Recurrent Networks: RNNs, the Vanishing Gradient & LSTM Gates"
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

A recurrent network is a state machine with **shared weights**: at every step it reads the input $x_t$, combines it with its current memory $h_{t-1}$, and produces a new memory $h_t$. Because the *same* cell is applied at every time step, the model is compact and can in principle remember arbitrarily far back. In practice the *original* RNN could not — its memory decays geometrically with distance because the gradient used to train it vanishes (§3: $|{\partial h_T}/{\partial h_0}|\sim10^{-27}$ at $T{=}50$). **Long Short-Term Memory (LSTM)** solved this with a second, *additive* memory channel — the cell state $C_t$ — gated by learned forget/input/output gates. That single change is why recurrence became usable for trading-length sequences at all.

The practical objective: understand (a) what a recurrent cell computes, (b) *why* the naive version fails, and (c) how the gates fix it — so you can read LSTM/GRU code and reason about what the model can and cannot learn from a financial series.

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

Because $\tanh'\le1$ and the recurrence multiplies, the **product of many $<1$ factors decays geometrically** — the network effectively cannot learn dependencies more than a handful of steps long. This is the Bengio–Simard–Frasconi (1994) result, and it is the single reason recurrence was considered impractical for long sequences until LSTM.

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

a product of *gate* values (not of weights times saturating derivatives). If the forget gate learns $f_s\approx1$, the gradient passes essentially **undamped across arbitrary distances** — the **constant-error-carousel (CEC)**. There is no $\|W\|^T$ penalty on this path; the gates can *learn* the memory horizon instead of having it imposed by the weight norm. The GRU (Cho et al. 2014) achieves a similar effect with two gates and a single state (§06).

> **A subtlety.** The CEC solves the *optimisation* problem (training long-range dependencies), not the *statistical* problem (overfitting with little data). An LSTM can now *fit* a long memory; whether that memory generalises is a question about data, addressed in [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation — LSTM forward pass and the vanishing gradient

Stdlib + `numpy`. Part A runs a hand-weighted LSTM forward and prints every gate at each step; Part B measures the gradient magnitude $|{\partial h_T}/{\partial h_0}|$ for a vanilla RNN against the LSTM cell path $\prod f_t$.

```python
import math
import numpy as np

# ---------- (A) LSTM forward pass, single unit, gates shown ----------
def sigmoid(z): return 1.0 / (1.0 + math.exp(-z))
def tanh(z):    return math.tanh(z)

# fixed hand-chosen weights so the arithmetic is inspectable
Wf, Wi, Wc, Wo = 0.9, 0.6, 0.8, 0.7     # recurrent weights
Uf, Ui, Uc, Uo = 1.0, 1.0, 1.0, 1.0     # input weights
bf, bi, bc, bo = 0.0, -0.5, 0.0, 0.0    # biases

x = [0.2, 0.9, -0.4, 1.5, 0.1]          # input series
h = 0.0; C = 0.0
print("t |    f_t    i_t    g_t    o_t |    C_t     h_t")
for t, xt in enumerate(x):
    f = sigmoid(Wf*h + Uf*xt + bf)
    i = sigmoid(Wi*h + Ui*xt + bi)
    g = tanh   (Wc*h + Uc*xt + bc)
    o = sigmoid(Wo*h + Uo*xt + bo)
    C = f*C + i*g
    h = o*tanh(C)
    print("%d | %6.3f %6.3f %6.3f %6.3f | %7.4f %7.4f" % (t, f, i, g, o, C, h))

# ---------- (B) vanishing gradient: vanilla RNN vs LSTM cell path ----------
print("\n|dh_T/dh_0| along a single vanilla-RNN unit h_t=tanh(W h_{t-1}+U x_t):")
for W in (0.5, 0.9, 1.2):
    rng = np.random.default_rng(0)
    xs = rng.normal(0, 1, 60)
    for T in (1, 5, 10, 20, 50):
        h = 0.0; jac = 1.0
        for t in range(T):
            a = W*h + xs[t]
            jac *= W * (1.0 - math.tanh(a)**2)   # W * tanh'(a)
            h = math.tanh(a)
        print("  W=%.1f  T=%2d : |grad| = %.3e" % (W, T, abs(jac)))

print("\n|dC_T/dC_0| along the LSTM cell-state (constant-error-carousel) path = prod f_t:")
for f in (0.5, 0.9, 0.99):
    for T in (1, 5, 10, 20, 50):
        print("  f=%.2f  T=%2d : f^T = %.3e" % (f, T, f**T))
```
```
t |    f_t    i_t    g_t    o_t |    C_t     h_t
0 |  0.550  0.426  0.197  0.550 |  0.0840  0.0461
1 |  0.719  0.605  0.734  0.718 |  0.5046  0.3342
2 |  0.475  0.332 -0.132  0.459 |  0.1960  0.0887
3 |  0.829  0.741  0.917  0.827 |  0.8425  0.5680
4 |  0.648  0.485  0.504  0.622 |  0.7906  0.4097

|dh_T/dh_0| along a single vanilla-RNN unit h_t=tanh(W h_{t-1}+U x_t):
  W=0.5  T= 1 : |grad| = 4.922e-01
  W=0.5  T= 5 : |grad| = 1.666e-02
  W=0.5  T=10 : |grad| = 4.897e-06
  W=0.5  T=20 : |grad| = 1.409e-13
  W=0.5  T=50 : |grad| = 5.627e-34
  W=0.9  T= 1 : |grad| = 8.859e-01
  W=0.9  T= 5 : |grad| = 2.854e-01
  W=0.9  T=10 : |grad| = 8.638e-04
  W=0.9  T=20 : |grad| = 8.660e-11
  W=0.9  T=50 : |grad| = 5.429e-27
  W=1.2  T= 1 : |grad| = 1.181e+00
  W=1.2  T= 5 : |grad| = 8.489e-01
  W=1.2  T=10 : |grad| = 2.739e-03
  W=1.2  T=20 : |grad| = 9.587e-11
  W=1.2  T=50 : |grad| = 1.617e-26

|dC_T/dC_0| along the LSTM cell-state (constant-error-carousel) path = prod f_t:
  f=0.50  T= 1 : f^T = 5.000e-01
  f=0.50  T= 5 : f^T = 3.125e-02
  f=0.50  T=10 : f^T = 9.766e-04
  f=0.50  T=20 : f^T = 9.537e-07
  f=0.50  T=50 : f^T = 8.882e-16
  f=0.90  T= 1 : f^T = 9.000e-01
  f=0.90  T= 5 : f^T = 5.905e-01
  f=0.90  T=10 : f^T = 3.487e-01
  f=0.90  T=20 : f^T = 1.216e-01
  f=0.90  T=50 : f^T = 5.154e-03
  f=0.99  T= 1 : f^T = 9.900e-01
  f=0.99  T= 5 : f^T = 9.510e-01
  f=0.99  T=10 : f^T = 9.044e-01
  f=0.99  T=20 : f^T = 8.179e-01
  f=0.99  T=50 : f^T = 6.050e-01
```

Read it as the derivation in numbers. The vanilla RNN at $W{=}0.9$ loses seven orders of magnitude between $T{=}10$ ($8.6\times10^{-4}$) and $T{=}20$ ($8.7\times10^{-11}$) — the 20th-step dependency carries essentially zero gradient, so the cell can never learn it. The LSTM cell path with $f{=}0.99$ still transmits **$0.605$** of the gradient at $T{=}50$ — $26$ orders of magnitude larger. That gap *is* the LSTM.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Vanishing/exploding gradients (the disease LSTM treats).** A vanilla RNN cannot learn long-range structure; see the table. Exploding gradients (large $W$, or the $1.2$ row's transient growth) are handled separately by **gradient clipping** (Pascanu et al. 2013) — a hard cap on the gradient norm per step.
2. **Gates do not create signal.** An LSTM can *represent* a long memory; with a low-SNR target it will happily fit spurious long memories that don't generalise. Architecture fixes optimisation, not statistics (→ [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **BPTT is sequential and slow.** Recurrence cannot be parallelised over time (step $t$ needs step $t-1$), which is both a training-time and, for high-frequency trading, an **inference-latency** problem — the motivation for the convolutional and attention alternatives in pages 03 and 06.
4. **Truncated BPTT biases the gradient.** In practice you unroll only $k$ steps to fit memory; that reintroduces exactly the truncation the LSTM was meant to avoid, so the *effective* horizon is your chosen unroll length, not the architecture.
5. **Numerical saturating tanh/sigmoid.** Early in training, gates sit near $0.5$ and the cell state can drift; input scaling (standardising features) matters as much here as in feed-forward nets.

---

### 5. Canonical Literature & Study References

- **Hochreiter, S. & Schmidhuber, J.** (1997), *Long Short-Term Memory*, Neural Computation 9(8):1735–1780 — the original LSTM; the constant-error-carousel argument (§2.3).
- **Goodfellow, Bengio & Courville**, *Deep Learning*, **Ch. 10** (§10.2: the recurrence, BPTT, the vanishing-gradient discussion; the LSTM/GRU subsection) — the authoritative derivation.
- **Bengio, Simard & Frasconi** (1994), *Learning Long-Term Dependencies with Gradient Descent is Difficult* — the classical vanishing-gradient result.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, **Ch. 11** (§11.4–11.5: back-propagation, weight decay, early stopping) — the anti-overfit recipe that carries over verbatim to recurrent nets.
- **Bai, Kolter & Koltun** (2018), *An Empirical Evaluation of Generic Convolutional and Recurrent Networks*, arXiv:1803.01271 — shows a well-tuned TCN matches or beats LSTMs on sequence benchmarks with more parallelism; read before assuming recurrence is necessary.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/03-attention-and-transformers|03 · Attention & Transformers]] (the non-recurrent route to long-range memory) · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/04-autoencoders-for-factors|04 · Autoencoders for Factors]]
- Latency reality: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] (why sequential inference is expensive)
- Optimisation base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
