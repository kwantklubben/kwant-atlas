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

The bag-of-words model has one crippling limitation: **it discards word *meaning***. "impairment" and "writedown" are treated as unrelated binary features even though they are near-synonyms, and "The firm recorded a **loss**" vs "The firm recorded a **loss** of market share *and gained* customers" both count "loss" as negative. Embeddings and transformers fix this by replacing one-hot words with **dense vectors whose geometry encodes meaning**, and - for transformers - with vectors that change with *context*.

The objective is three ideas:

1. **Distributional hypothesis** - words that appear in similar contexts have similar meaning (Firth: "you shall know a word by the company it keeps"). Learn a vector per word so that cosine similarity ≈ semantic similarity. This is what FinBERT's and every finance LM's embeddings inherit.
2. **Polysemy via context** - a static word vector cannot tell "bank" (river) from "bank" (institution). Transformers produce a *contextual* vector for each token: the same word gets different vectors depending on its neighbors, so "liability" in a legal sentence embeds differently than in a balance-sheet one.
3. **Finance needs its own pretraining** - Wikipedia-trained embeddings encode *general* meaning; "share", "liability", "gross", "charge" carry finance-specific senses that generic pretraining gets wrong. FinBERT (Araci 2019; Yang–Uy–Huang 2020) continues pretraining BERT on financial text (filings + Reuters news / financial communications), and the task at hand is to show *why that matters*: distributional vectors learn what the corpus teaches them.

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

gives each word a $k$-dimensional vector. Words with similar contexts land near each other because they share rows of $M$. This is the *learned* ancestor of today's word2vec/fastText vectors, and it runs on numpy alone - no training loop.

**Attention (the transformer primitive).** For tokens with query/key/value matrices $Q=W_QX$, $K=W_KX$, $V=W_VX$,

$$
\text{Attention}(Q,K,V)=\text{softmax}\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)V,
$$

so each token's output is a *context-weighted* sum of all tokens' values - the weights $\propto e^{(q_i\cdot k_j)/\sqrt{d_k}}$ are large exactly where token $i$ "matches" token $j$. This is how a contextual representation of a word is formed: its vector depends on the whole sentence, which is precisely what the static bag/embedding cannot do. (Full formal treatment: Vaswani et al. 2017; Jurafsky & Martin Ch 11.)

**Finance-domain pretraining.** BERT gives each token a contextual vector by masked-language modeling. FinBERT continues training on finance-specific corpora so that the *distributional* statistics - and therefore the embeddings and the attention patterns - reflect finance. Araci (2019) fine-tunes a sentiment head on financial news to output $P(\text{pos}),P(\text{neu}),P(\text{neg})$; the net score is $P(\text{pos})-P(\text{neg})$ - a strictly richer cousin of §03's dictionary tone because it sees *context*, not just counts.

---

### 3. Computational Implementation - learn embeddings from a mini corpus

Builds the co-occurrence matrix, PPMI-weights it, and takes a truncated SVD to get rank-2 word embeddings - then reads off the similarities to see that distributional geometry recovers semantics.




Two teaching points, both real. First, **synonyms land together**: `earnings`≈`estimates` (0.983), `guidance`≈`outlook` (0.842), `costs`≈`margins` (0.999) - distributional geometry recovers the meaning bag-of-words threw away. Second, **the model is only as smart as the corpus**: `beat` and `missed` both occur between `earnings` and `estimates/quarter`, so they get near-identical vectors (1.000) *even though they are antonyms*. Antonymy is a *signed* relation that co-occurrence alone cannot see - a genuine limit of unsupervised distributional learning, and precisely why a finance LM must be *fine-tuned with labels* (as FinBERT does) rather than used raw.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Pretraining-domain mismatch.** A general (Wikipedia) embedding misrepresents finance senses - "share", "liability", "charge", "gross" get generic meanings that invert financial sentiment (Araci 2019 documents the gap). *First principle:* embeddings encode the *distributional statistics of their training corpus*; if your corpus isn't finance, your vectors aren't finance.
2. **Static vectors are context-blind.** word2vec-style vectors cannot resolve polysemy ("the firm took a **charge**" vs "we **charge** customers"). A dictionary or static-embedding feature will misfire on such tokens; the fix is contextual models (transformers) that condition on neighbors.
3. **Unsupervised similarity ≠ polarity.** `beat`≈`missed` in this folder's run: co-occurrence encodes *association*, not *evaluation*. Deploying raw embeddings as a sentiment feature silently encodes this - you need labels (or a lexicon) to pin polarity.
4. **Scale / data cost.** Transformers need huge pretraining corpora and heavy compute; on a thin panel the honest move is a small LM or dictionary baseline, not a fine-tuned model that overfits a few hundred filings (the $p\gg N$ trap of [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05]]).

---

### 5. References

- **Araci, Dogu**, "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models," arXiv:1908.10063, 2019
- **Yang, Yi, Uy, Mark C.S. & Huang, Allen**, "FinBERT: A Pretrained Language Model for Financial Communications," arXiv:2006.08097, 2020
- **Vaswani et al.**, "Attention Is All You Need," NeurIPS 2017
- **Levy, Omer & Goldberg, Yoav**, "Neural Word Embedding as Implicit Matrix Factorization," NeurIPS 2014
- **Jurafsky & Martin**, *Speech and Language Processing* (3rd ed.)

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02 · Bag-of-Words]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03 · Sentiment & Tone]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/06-advanced-extensions|06 · Earnings-Call Analysis]]
- Architectures: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
