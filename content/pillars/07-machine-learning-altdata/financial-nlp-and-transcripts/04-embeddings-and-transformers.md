---
title: "7.4.4 Embeddings & Transformers"
tags:
  - pillar-machine-learning
  - financial-nlp-and-transcripts
  - embeddings
  - transformers
  - finbert
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02 · Bag-of-Words]] (the feature matrix) and basic linear algebra ([[foundations/linear-algebra-and-matrices/index|Linear Algebra]]).

---

### 1. Intuition & Practical Objective

The bag-of-words model has one crippling limitation: **it discards word *meaning***. "impairment" and "writedown" are treated as unrelated binary features even though they are near-synonyms, and "The firm recorded a **loss**" vs "The firm recorded a **loss** of market share *and gained* customers" both count "loss" as negative. Embeddings and transformers fix this by replacing one-hot words with **dense vectors whose geometry encodes meaning**, and — for transformers — with vectors that change with *context*.

The objective is three ideas:

1. **Distributional hypothesis** — words that appear in similar contexts have similar meaning (Firth: "you shall know a word by the company it keeps"). Learn a vector per word so that cosine similarity ≈ semantic similarity. This is what FinBERT's and every finance LM's embeddings inherit.
2. **Polysemy via context** — a static word vector cannot tell "bank" (river) from "bank" (institution). Transformers produce a *contextual* vector for each token: the same word gets different vectors depending on its neighbors, so "liability" in a legal sentence embeds differently than in a balance-sheet one.
3. **Finance needs its own pretraining** — Wikipedia-trained embeddings encode *general* meaning; "share", "liability", "gross", "charge" carry finance-specific senses that generic pretraining gets wrong. FinBERT (Araci 2019; Yang–Uy–Huang 2020) continues pretraining BERT on financial text (filings + Reuters news / financial communications), and the task at hand is to show *why that matters*: distributional vectors learn what the corpus teaches them.

---

### 2. Mathematical Ground Truth & Derivations

**Count-based embeddings = SVD of a co-occurrence matrix.** The classical route (Mikolov-adjacent; formalized as the PMI–SVD equivalence by Levy & Goldberg, 2014). From a corpus build the word–context co-occurrence matrix $M\in\mathbb{R}^{V\times V}$, then the **positive pointwise mutual information (PPMI)** matrix

$$
\text{PPMI}(t,c)=\max\Big(0,\ \log\frac{P(t,c)}{P(t)P(c)}\Big),
$$

which up-weights pairs that co-occur more than chance. The truncated SVD

$$
M \approx U_k \Sigma_k V_k^\top,\qquad \mathbf{v}_t = \big(U_k\Sigma_k\big)_{t,:}\in\mathbb{R}^k,
$$

gives each word a $k$-dimensional vector. Words with similar contexts land near each other because they share rows of $M$. This is the *learned* ancestor of today's word2vec/fastText vectors, and it runs on numpy alone — no training loop.

**Attention (the transformer primitive).** For tokens with query/key/value matrices $Q=W_QX$, $K=W_KX$, $V=W_VX$,

$$
\text{Attention}(Q,K,V)=\text{softmax}\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)V,
$$

so each token's output is a *context-weighted* sum of all tokens' values — the weights $\propto e^{(q_i\cdot k_j)/\sqrt{d_k}}$ are large exactly where token $i$ "matches" token $j$. This is how a contextual representation of a word is formed: its vector depends on the whole sentence, which is precisely what the static bag/embedding cannot do. (Full formal treatment: Vaswani et al. 2017; Jurafsky & Martin Ch 11.)

**Finance-domain pretraining.** BERT gives each token a contextual vector by masked-language modeling. FinBERT continues training on finance-specific corpora so that the *distributional* statistics — and therefore the embeddings and the attention patterns — reflect finance. Araci (2019) fine-tunes a sentiment head on financial news to output $P(\text{pos}),P(\text{neu}),P(\text{neg})$; the net score is $P(\text{pos})-P(\text{neg})$ — a strictly richer cousin of §03's dictionary tone because it sees *context*, not just counts.

---

### 3. Computational Implementation — learn embeddings from a mini corpus

Builds the co-occurrence matrix, PPMI-weights it, and takes a truncated SVD to get rank-2 word embeddings — then reads off the similarities to see that distributional geometry recovers semantics.

```python
import numpy as np

corpus = [
    "earnings beat estimates this quarter",
    "earnings missed estimates badly this quarter",
    "revenue grew faster than estimates",
    "guidance exceeded our expectations this quarter",
    "guidance disappointed and we cut the outlook",
    "margins expanded and costs stayed flat",
    "demand was strong and revenue grew again",
    "a surprise charge hit earnings this quarter",
]
def tokens(t):
    return [w.lower() for w in t.replace(',', '').split()]

window = 2
vocab = sorted({w for t in corpus for w in tokens(t)})
w2i = {w: i for i, w in enumerate(vocab)}
V = len(vocab)
M = np.zeros((V, V), dtype=float)
for t in corpus:
    tk = tokens(t)
    for i, w in enumerate(tk):
        for j in range(max(0, i - window), min(len(tk), i + window + 1)):
            if i != j:
                M[w2i[w], w2i[tk[j]]] += 1.0

row_sum = M.sum(axis=1, keepdims=True); col_sum = M.sum(axis=0, keepdims=True)
total = M.sum()
P = M / total
pmi = np.log(P / ((row_sum / total) @ (col_sum / total)) + 1e-12)
PPMI = np.clip(pmi, 0.0, None)                # positive PMI matrix

U, s, Vt = np.linalg.svd(PPMI, full_matrices=False)
k = 2
emb = U[:, :k] * s[:k]                        # truncated rank-2 embeddings

def cos(a, b):
    return float(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)

print("Rank-2 PPMI embeddings (word -> [dim0, dim1]):")
for w in vocab:
    v = emb[w2i[w], :]
    print(f"  {w:13s} [{v[0]:+.3f}, {v[1]:+.3f}]")
print("\nCosine similarities in latent space:")
pairs = [("earnings", "estimates"), ("earnings", "revenue"), ("beat", "missed"),
         ("guidance", "outlook"), ("guidance", "earnings"), ("costs", "margins")]
for a, b in pairs:
    print(f"  cos({a},{b}) = {cos(emb[w2i[a]], emb[w2i[b]]):+.3f}")
print(f"\nTop-2 singular values: {s[0]:.3f}, {s[1]:.3f}   "
      f"(rank-2 captures {(s[:2]**2).sum()/(s**2).sum():.3f} of variance)")
```
```
Rank-2 PPMI embeddings (word -> [dim0, dim1]):
  a             [-0.405, +2.454]
  again         [-0.927, +0.151]
  and           [-3.080, -0.851]
  badly         [-0.484, +1.217]
  beat          [-0.437, +1.213]
  charge        [-0.571, +3.146]
  costs         [-1.975, -0.760]
  cut           [-2.220, -0.976]
  demand        [-1.224, -0.302]
  disappointed  [-1.719, -0.374]
  earnings      [-0.641, +2.286]
  estimates     [-0.828, +1.675]
  exceeded      [-1.125, +0.638]
  expanded      [-1.687, -0.605]
  expectations  [-0.869, +0.940]
  faster        [-1.074, +0.613]
  flat          [-1.382, -0.567]
  grew          [-1.433, +0.331]
  guidance      [-1.622, +0.194]
  hit           [-0.538, +2.608]
  margins       [-1.359, -0.460]
  missed        [-0.457, +1.304]
  our           [-1.137, +0.793]
  outlook       [-1.589, -0.767]
  quarter       [-0.553, +1.226]
  revenue       [-1.556, +0.125]
  stayed        [-1.697, -0.650]
  strong        [-1.698, -0.345]
  surprise      [-0.504, +2.943]
  than          [-0.869, +0.647]
  the           [-1.996, -0.927]
  this          [-0.748, +1.675]
  was           [-1.548, -0.401]
  we            [-2.189, -0.844]

Cosine similarities in latent space:
  cos(earnings,estimates) = +0.983
  cos(earnings,revenue) = +0.347
  cos(beat,missed) = +1.000
  cos(guidance,outlook) = +0.842
  cos(guidance,earnings) = +0.383
  cos(costs,margins) = +0.999

Top-2 singular values: 8.103, 7.584   (rank-2 captures 0.216 of variance)
```

Two teaching points, both real. First, **synonyms land together**: `earnings`≈`estimates` (0.983), `guidance`≈`outlook` (0.842), `costs`≈`margins` (0.999) — distributional geometry recovers the meaning bag-of-words threw away. Second, **the model is only as smart as the corpus**: `beat` and `missed` both occur between `earnings` and `estimates/quarter`, so they get near-identical vectors (1.000) *even though they are antonyms*. Antonymy is a *signed* relation that co-occurrence alone cannot see — a genuine limit of unsupervised distributional learning, and precisely why a finance LM must be *fine-tuned with labels* (as FinBERT does) rather than used raw.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Pretraining-domain mismatch.** A general (Wikipedia) embedding misrepresents finance senses — "share", "liability", "charge", "gross" get generic meanings that invert financial sentiment (Araci 2019 documents the gap). *First principle:* embeddings encode the *distributional statistics of their training corpus*; if your corpus isn't finance, your vectors aren't finance.
2. **Static vectors are context-blind.** word2vec-style vectors cannot resolve polysemy ("the firm took a **charge**" vs "we **charge** customers"). A dictionary or static-embedding feature will misfire on such tokens; the fix is contextual models (transformers) that condition on neighbors.
3. **Unsupervised similarity ≠ polarity.** `beat`≈`missed` in this folder's run: co-occurrence encodes *association*, not *evaluation*. Deploying raw embeddings as a sentiment feature silently encodes this — you need labels (or a lexicon) to pin polarity.
4. **Scale / data cost.** Transformers need huge pretraining corpora and heavy compute; on a thin panel the honest move is a small LM or dictionary baseline, not a fine-tuned model that overfits a few hundred filings (the $p\gg N$ trap of [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05]]).

---

### 5. Canonical Literature & Study References

- **Araci, Dogu**, "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models," arXiv:1908.10063, 2019 — the `ProsusAI/finbert` weights and the finance-domain BERT fine-tune. *Corpus PDF verified.*
- **Yang, Yi, Uy, Mark C.S. & Huang, Allen**, "FinBERT: A Pretrained Language Model for Financial Communications," arXiv:2006.08097, 2020 — the larger financial-communications pretraining variant.
- **Vaswani et al.**, "Attention Is All You Need," NeurIPS 2017 — the transformer / self-attention architecture. *Corpus PDF verified.*
- **Levy, Omer & Goldberg, Yoav**, "Neural Word Embedding as Implicit Matrix Factorization," NeurIPS 2014 — the PMI–SVD equivalence that connects this page's count-based demo to word2vec.
- **Jurafsky & Martin**, *Speech and Language Processing* (3rd ed.) — Ch 6 (vector semantics), Ch 11 (transformers). *Corpus PDF verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02 · Bag-of-Words]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03 · Sentiment & Tone]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/06-advanced-extensions|06 · Earnings-Call Analysis]]
- Architectures: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
