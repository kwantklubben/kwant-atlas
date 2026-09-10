---
title: "03 — Attention & Transformers: Query-Key Lookup, Causality & Multi-Head"
tags:
  - pillar-machine-learning
  - deep-learning-for-sequences
  - attention
  - transformer
  - causal-masking
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/02-rnns-and-lstms|02 · RNNs & LSTMs]] and linear algebra (dot products, softmax).

---

### 1. Intuition & Practical Objective

Recurrence compresses the past into **one vector** that is overwritten at each step. Attention does something different and powerful: it keeps **all** past states and lets the model *look back and choose* which ones to use. The mechanism is a **soft dictionary lookup**. Every past position offers a *key* $k_j$ and a *value* $v_j$; the current position issues a *query* $q_i$; the output is the similarity-weighted average of the values:

$$\text{output}_i=\sum_j \underbrace{\frac{\exp(q_i\cdot k_j)}{\sum_{j'}\exp(q_i\cdot k_{j'})}}_{\text{softmax weight (attention)}}\;v_j .$$

Three "aha"s:

1. **No fixed memory horizon.** Attention's path length between any two positions is $O(1)$ (they interact directly), versus $O(T)$ for recurrence. This is why Transformers learn long-range dependencies that RNNs cannot.
2. **It is fully parallel over time.** All queries and keys are computed at once — the reason Transformers train fast on GPUs, unlike the sequential BPTT of page 02.
3. **Causality must be *enforced*, not assumed.** In a *forecasting* task the query at $t$ must not see keys at $j>t$. A raw (bidirectional) attention will happily attend to the future — look-ahead leakage *inside the architecture*. The fix is an explicit **causal mask** $M$ (§3 verifies it produces an exact zero upper triangle).

The practical objective: read and write the attention formula correctly, and *never* build a forecasting model without a causal mask.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Scaled dot-product attention (Vaswani et al. 2017)

Given a matrix of $T$ queries $Q\in\mathbb R^{T\times d_k}$, keys $K\in\mathbb R^{T\times d_k}$, values $V\in\mathbb R^{T\times d_v}$:

$$\boxed{\;\operatorname{Attn}(Q,K,V)=\operatorname{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}+M\Big)V\;}$$

where $\operatorname{softmax}$ is applied **row-wise** and $M$ is the mask.

**Why divide by $\sqrt{d_k}$?** If the components of $q$ and $k$ are i.i.d. with mean $0$ and variance $1$, then $q\cdot k=\sum_{m=1}^{d_k}q_mk_m$ has mean $0$ and **variance $d_k$**. Unscaled, the logits grow like $\sqrt{d_k}$, pushing the softmax into a saturated region where one weight $\to1$ and the gradients $\to0$. Dividing by $\sqrt{d_k}$ restores unit variance and keeps the softmax in its informative range (§3 measures this: score stdev $1.45\to15.73$ as $d_k$ grows, and the softmax entropy collapses without the scaling).

#### 2.2 The causal mask

For an autoregressive / forecasting model,

$$M_{ij}=\begin{cases}-\infty & j>i\\[2pt] 0 & j\le i\end{cases}$$

so the pre-softmax logit for any future position is $-\infty$ and $\exp(-\infty)=0$. Position $i$ can attend **only** to $j\le i$. This is the exact attention analogue of the *no-look-ahead* requirement; without it, the model is trained on the answer.

#### 2.3 Multi-head attention and the Transformer block

One attention head computes one similarity notion. **Multi-head** attention runs $h$ heads in parallel subspaces and concatenates:

$$\text{MultiHead}=\operatorname{Concat}(\text{head}_1,\dots,\text{head}_h)\,W^O,\qquad
\text{head}_m=\operatorname{Attn}(QW_m^Q,KW_m^K,VW_m^V).$$

A Transformer block adds residual connections and a position-wise feed-forward net: $z=\operatorname{LayerNorm}(x+\text{MultiHead}(x))$, $y=\operatorname{LayerNorm}(z+\operatorname{FFN}(z))$. Positional encodings (sinusoidal or learned) are added to the inputs, because attention — unlike a recurrence — is permutation-invariant and otherwise cannot tell position $5$ from position $50$.

---

### 3. Computational Implementation — causal attention and the scaling argument

`numpy` + stdlib. Part A computes masked attention and proves the causality property; Part B measures why the $\sqrt{d_k}$ scaling exists.

```python
import numpy as np
np.set_printoptions(precision=3, suppress=True)

def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

def attention(Q, K, V, causal=True, scale=True):
    dk = Q.shape[-1]
    S = Q @ K.T
    if scale:                        # divide by sqrt(d_k)
        S = S / np.sqrt(dk)
    if causal:                       # mask j > i  (no look-ahead)
        mask = np.triu(np.ones_like(S), k=1).astype(bool)
        S = np.where(mask, -1e30, S)
    W = softmax(S)
    return W, W @ V

rng = np.random.default_rng(0)
T, d = 6, 4
Q = rng.normal(0, 1, (T, d)); K = rng.normal(0, 1, (T, d))
V = np.arange(T*d, dtype=float).reshape(T, d)

W, out = attention(Q, K, V, causal=True)
print("causal attention weights W = softmax(QK^T/sqrt(d_k) + M):")
print(W)
print("row sums (=1):", W.sum(axis=1))
print("upper triangle is exactly zero (no attention to the future):",
      bool(np.allclose(np.triu(W, k=1), 0.0)))

# effect of the 1/sqrt(d_k) scaling: score variance and softmax entropy grow with d_k
def entropy(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())

rng = np.random.default_rng(1)
print("\nmean score stdev and mean attention entropy vs d_k (T=8, random Q,K):")
for dk in (4, 64, 256):
    Qi = rng.normal(0, 1, (8, dk)); Ki = rng.normal(0, 1, (8, dk))
    raw = Qi @ Ki.T
    ent_raw = entropy(softmax(raw)[0])
    ent_scaled = entropy(softmax(raw / np.sqrt(dk))[0])
    print("  d_k=%3d : stdev(scores)=%.2f  H(unscaled)=%.3f  H(scaled)=%.3f"
          % (dk, raw.std(), ent_raw, ent_scaled))
```
```
causal attention weights W = softmax(QK^T/sqrt(d_k) + M):
[[1.    0.    0.    0.    0.    0.   ]
 [0.366 0.634 0.    0.    0.    0.   ]
 [0.288 0.473 0.24  0.    0.    0.   ]
 [0.133 0.582 0.151 0.133 0.    0.   ]
 [0.053 0.103 0.156 0.404 0.284 0.   ]
 [0.136 0.201 0.18  0.119 0.278 0.086]]
row sums (=1): [1. 1. 1. 1. 1. 1.]
upper triangle is exactly zero (no attention to the future): True

mean score stdev and mean attention entropy vs d_k (T=8, random Q,K):
  d_k=  4 : stdev(scores)=1.45  H(unscaled)=1.776  H(scaled)=1.979
  d_k= 64 : stdev(scores)=8.96  H(unscaled)=0.613  H(scaled)=1.675
  d_k=256 : stdev(scores)=15.73  H(unscaled)=0.158  H(scaled)=1.753
```

Read it as two facts. First, the weight matrix is **lower-triangular by construction** — the upper triangle is exactly zero, every row sums to $1$, and position $0$ can only attend to itself. This is what makes an attention forecasting model honest; drop the mask and you have built a leak. Second, the scaling matters: at $d_k{=}256$ the unscaled score standard deviation is $15.73$ and the softmax entropy collapses to $0.158$ (attention has pinned almost all weight on one key — gradient-starved), whereas the $\sqrt{d_k}$-scaled version stays at $1.75$, near the maximum-entropy value $\ln 8=2.08$ for $8$ positions.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Missing causal mask = look-ahead leakage.** The most common and most damaging bug. A bidirectional/encoder-only attention over a *forecasting* target sees the future by construction. Always verify $\operatorname{triu}(W,1)=0$ on a test batch. (The validation-side twin of this is the [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]] folder.)
2. **$O(T^2)$ cost in time and memory.** Attention scales quadratically with sequence length; a full LOB day at tick resolution is millions of tokens. This is the practical reason *microstructure* models use *local* attention or convolution (DeepLOB) rather than a full Transformer.
3. **Attention weights are not explanations.** High attention on a timestep does not prove it *caused* the prediction; "attention is not explanation" (Jain & Wallace 2019). Use it as a diagnostic, not a story.
4. **Positional encoding is not neutral in finance.** Time is not a uniform grid (trading hours, overnight gaps, information-driven bars). Naive positional encoding imposes a regularity the market does not have.
5. **Over-parameterisation on small data.** A single Transformer block has millions of weights; on $N\sim10^3$ financial samples it will memorise. Attention is a tool for the *large-$N$ microstructure* regime, not for monthly bars.

---

### 5. Canonical Literature & Study References

- **Vaswani, Ashish et al.** (2017), *Attention Is All You Need*, NeurIPS — scaled dot-product attention, multi-head, the Transformer. The $1/\sqrt{d_k}$ justification is in §3.2.1.
- **Lim, Bryan et al.** (2021), *Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting*, IJF 37(4) — the finance/time-series adaptation: variable selection, static covariates, multi-horizon attention.
- **Goodfellow, Bengio & Courville**, *Deep Learning*, **Ch. 10** (§10.4 "Encoder–Decoder Sequence-to-Sequence Architectures" and the attention mechanism) — the pedagogical derivation.
- **Zhang, Zohren & Roberts** (2019), *DeepLOB: Deep Convolutional Neural Networks for Limit Order Books*, IEEE TSP 67(11), arXiv:1808.03668 — the microstructure model that shows **convolution + LSTM can beat full attention** when $T$ is huge and locality matters.
- **Jain, S. & Wallace, B.** (2019), *Attention is not Explanation* — the cautionary result in §4.3.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/02-rnns-and-lstms|02 · RNNs & LSTMs]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/04-autoencoders-for-factors|04 · Autoencoders for Factors]]
- Multi-horizon forecasting target: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/06-advanced-extensions|06 · Advanced Extensions]] (TFT, DeepAR)
- Leakage discipline (validation side): [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged Cross-Validation & Backtest Hygiene]]
- Text/NLP attention (same mechanism, different data): [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Financial NLP & Transcripts]]
