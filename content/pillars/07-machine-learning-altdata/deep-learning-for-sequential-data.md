---
title: "Deep Learning for Sequential Data"
tags:
  - pillar-ml-altdata
  - deep-learning
  - lstm
  - transformers
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Calculus & Gradients]] and [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr|Financial ML Pitfalls]].

---

### 1. Intuition & Practical Objective

While tree-based models excel on cross-sectional tabular features, financial markets are fundamentally sequential: the exact temporal ordering of tick arrivals, limit order book cancellations, and macroeconomic releases contains rich dynamic context.

Deep Learning architectures designed for sequential data—Long Short-Term Memory networks (**LSTMs**), Temporal Convolutional Networks (**TCNs**), and **Temporal Fusion Transformers (TFT)**—model multi-scale temporal dependencies, processing raw tick streams and order book sequences directly without lossy manual feature engineering.

---

### 2. Mathematical Ground Truth & Derivations

#### Long Short-Term Memory (LSTM) Formulation
To solve the vanishing gradient problem of standard recurrent neural networks, Hochreiter & Schmidhuber (1997) introduced explicit gating:
1. **Forget Gate:** $f_t = \sigma(W_f x_t + U_f h_{t-1} + b_f)$
2. **Input Gate:** $i_t = \sigma(W_i x_t + U_i h_{t-1} + b_i)$
3. **Candidate Cell State:** $\tilde{C}_t = \tanh(W_c x_t + U_c h_{t-1} + b_c)$
4. **Cell State Update:** $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$
5. **Output Gate:** $o_t = \sigma(W_o x_t + U_o h_{t-1} + b_o)$
6. **Hidden State:** $h_t = o_t \odot \tanh(C_t)$

#### Temporal Convolutional Networks (TCN)
TCNs replace recurrence with 1D causal dilated convolutions:
$$(F *_d x)(t) = \sum_{k=0}^{K-1} f(k) \cdot x_{t - d \cdot k}$$
- **Causal:** Convolutions ensure prediction at time $t$ depends only on past elements $s \le t$ (zero lookahead).
- **Dilated ($d$):** Exponential dilation factor ($d = 1, 2, 4, 8, \dots$) expands the effective receptive field exponentially without exploding parameter counts.

#### Self-Attention in Transformers for Limit Order Books
$$A(Q, K, V) = \text{softmax}\left( \frac{Q K^T}{\sqrt{d_k}} + M \right) V$$
where $M$ is an upper-triangular masking matrix ($M_{ij} = -\infty$ for $j > i$) enforcing strict temporal causality.

---

### 3. Computational Implementation

```python
import numpy as np

def generate_causal_mask(seq_len: int) -> np.ndarray:
    """
    Generates causal upper-triangular attention mask to prevent lookahead bias.
    """
    mask = np.triu(np.full((seq_len, seq_len), -np.inf), k=1)
    return mask

# Verify causal mask structure
mask = generate_causal_mask(4)
print("Causal Attention Mask (Tokens cannot attend to future):\n", mask)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Parameter Explosion Overfitting:**
   - *Failure:* Training multi-layer deep Transformers with millions of weights on daily return data.
   - *Reality:* Financial markets don't have enough independent daily samples ($T \approx 5{,}000$ days over 20 years). Deep Learning strictly requires high-frequency tick or order book regimes where $N > 10^7$ observations exist.

2. **Inference Latency Overhead:**
   - *Failure:* A deep neural network takes 15 milliseconds to evaluate, rendering it useless for high-frequency market making where decisions must be made in 5 microseconds.

---

### 5. Canonical Literature & Study References

- **Goodfellow, Ian, Bengio, Yoshua, & Courville, Aaron**: *Deep Learning*, MIT Press, Chapters 9-10 (Convolutional & Sequence Modeling).
- **Lim, Bryan et al.**: *Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting*, International Journal of Forecasting 37(4), 1748-1764 (2021).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Bridges to: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr|Financial ML Pitfalls]]
- Bridges to: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems]]
