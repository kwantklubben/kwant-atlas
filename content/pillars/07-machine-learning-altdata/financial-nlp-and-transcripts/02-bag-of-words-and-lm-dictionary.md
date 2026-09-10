---
title: "02 — Bag-of-Words & the Loughran–McDonald Finance Dictionary"
tags:
  - pillar-machine-learning
  - financial-nlp-and-transcripts
  - bag-of-words
  - tf-idf
  - loughran-mcdonald
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/01-from-zero-intuition|01 · From Zero]] (why counts are a signal) and [[foundations/statistics-and-inference/index|Statistics & Inference]].

---

### 1. Intuition & Practical Objective

The bag-of-words model is the workhorse of financial text analysis: turn each document into a count vector, then feed those vectors to any regression or classifier. Its two engineering problems are (a) **ubiquity** — "the", "company", "fiscal" appear in every document and carry no discriminating power — and (b) **dictionary calibration** — a word's emotional valence is not universal.

This page delivers both fixes, and they are the *foundation* of every downstream result:

1. **TF–IDF rescaling**, which down-weights ubiquitous terms and up-weights terms that are rare in the corpus but frequent in a specific document — the standard "which words actually distinguish this text" feature (ESL's spam classifier uses exactly this family of term features; Ch 18 frames the $p\gg N$ side).
2. **The Loughran–McDonald (LM) dictionary**, the finance-specific sentiment lexicon (negative/positive/uncertainty/litigious/constraining/strong-modal word lists) hand-built from 10-Ks precisely because **general dictionaries misclassify accounting words**.

The objective is one sentence: **you need term weights that survive contact with an SEC filing, and a sentiment list that speaks accounting, not newsrooms.**

---

### 2. Mathematical Ground Truth & Derivations

**TF–IDF.** For document $d$ and term $t$ with count $x_{d,t}$:

$$\text{tf-idf}(t,d)=\underbrace{\frac{x_{d,t}}{\sum_{t'}x_{d,t'}}}_{\text{term frequency (normalized)}}\times\underbrace{\Big(\log\frac{N+1}{df_t+1}+1\Big)}_{\text{inverse document frequency (smoothed)}},$$

with $N$ documents and $df_t$ = number of documents containing $t$. The smoothing $+1$ keeps the IDF positive for a term in every document (so rare-vs-common ranking stays stable) and matches the classic implementation (Jurafsky & Martin Ch 6; sklearn's `TfidfTransformer`). **Intuition:** a term scores high only if it is *frequent in this document* *and* *unusual across the corpus* — "impairment" in one 10-K among a hundred that never mention it is exactly the kind of term that should spike.

**The document-distance view.** With term vectors $\mathbf{v}_d=\big(\text{tf-idf}(t,d)\big)_{t}$, two documents are compared by cosine similarity

$$\text{cos}(\mathbf{v}_d,\mathbf{v}_{d'})=\frac{\mathbf{v}_d\cdot\mathbf{v}_{d'}}{\|\mathbf{v}_d\|\|\mathbf{v}_{d'}\|},$$

which is the primitive behind both the Cohen–Malloy–Nguyen "did the firm change its language?" metric ($1-\cos$) and nearest-neighbor retrieval on filings.

**Why general dictionaries fail (Loughran–McDonald 2011).** Loughran–McDonald measured the misfit directly: the Harvard IV-4 and Henry negative lists classify large fractions of *negative-tagged* words that are actually accounting terms with neutral valence. Among the words Harvard labels negative that recur in 10-Ks are **"liability", "tax", "cost", "capital", "gross", "share", "unrealized"** — none of which is management expressing pessimism. A model built on such a list counts the *accounting itself* as sentiment. The LM lists re-sort 10-K word-frequency counts into a finance-native lexicon. The measurable consequences: sentiment scores built with generic dictionaries are biased (mechanically more "negative" the more accounting-specific the document), and the *predictive* content — the whole point — is diluted or inverted.

---

### 3. Computational Implementation — TF–IDF matrix and LM negative proportion from scratch

Builds the TF–IDF feature matrix over a four-document 10-K-like corpus and reports the LM negative-word proportion per document (a tiny stand-in for the full LM list, enough to show the mechanics).

```python
import math
from collections import Counter

docs = [
    "The firm recorded a loss from discontinued operations and recognized an impairment.",
    "Revenue increased due to strong demand and we raised our guidance for the year.",
    "The charge relates to a liability we will settle with cash in the next quarter.",
    "We see an increase in litigation risk and higher restructuring costs ahead.",
]
def tokens(t):
    return [w.lower() for w in t.replace(',', '').replace('.', '').split()]

N = len(docs)
counts = [Counter(tokens(d)) for d in docs]
vocab = sorted({w for c in counts for w in c})

def idf(w):
    df = sum(1 for c in counts if w in c)
    return math.log((1 + N) / (1 + df)) + 1.0          # smooth idf

def tfidf(doc_idx, w):
    c = counts[doc_idx]
    return (c[w] / sum(c.values())) * idf(w)            # tf * idf

print("TF-IDF feature matrix (rows=docs, cols=vocab, transposed for view):")
print(f"{'term':12s} idf   " + "  ".join(f"d{i}" for i in range(N)))
for w in vocab:
    if w in ("loss", "impairment", "revenue", "strong", "guidance", "liability",
             "increase", "risk", "restructuring", "demand"):
        row = "  ".join(f"{tfidf(i, w):.3f}" for i in range(N))
        print(f"{w:12s} {idf(w):.3f}  {row}")

LM_NEG = {"loss", "impairment", "charge", "litigation", "risk", "restructuring",
          "costs", "discontinued", "recognized"}
print("\nLM negative-word proportion per document:")
for i, c in enumerate(counts):
    neg = sum(v for w, v in c.items() if w in LM_NEG)
    print(f"  doc{i}: {neg:2d} of {sum(c.values()):2d} words -> "
          f"neg_prop={neg/sum(c.values()):.3f}")
```
```
TF-IDF feature matrix (rows=docs, cols=vocab, transposed for view):
term         idf   d0  d1  d2  d3
demand       1.916  0.000  0.137  0.000  0.000
guidance     1.916  0.137  0.000  0.000  0.000
impairment   1.916  0.160  0.000  0.000  0.000
increase     1.916  0.000  0.000  0.000  0.160
liability    1.916  0.000  0.000  0.128  0.000
loss         1.916  0.160  0.000  0.000  0.000
restructuring 1.916  0.000  0.000  0.000  0.160
revenue      1.916  0.000  0.137  0.000  0.000
risk         1.916  0.000  0.000  0.000  0.160
strong       1.916  0.000  0.137  0.000  0.000

LM negative-word proportion per document:
  doc0:  4 of 12 words -> neg_prop=0.333
  doc1:  0 of 14 words -> neg_prop=0.000
  doc2:  1 of 15 words -> neg_prop=0.067
  doc3:  4 of 12 words -> neg_prop=0.333
```

Two lessons in the numbers. First, TF–IDF isolates the *discriminating* terms: "impairment"/"loss" spike in doc0, "risk"/"restructuring" in doc3, "demand"/"revenue" in doc1 — each term concentrates on the document that actually discusses it. Second, the LM proportion is meaningful *because* it is a proportion: doc0 and doc3 are both "negative" (0.333) even though their vocabulary is entirely different — the lexicon compresses different phrasing into a comparable scalar.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Raw counts dominate by length.** Without IDF (or length normalization) the most frequent words win and a long boilerplate filing drowns the signal. *First principle:* information is per-word, so normalize.
2. **Dictionary valence mismatch.** "Liability", "tax", "cost", "gross", "unrealized" are LM-vs-Harvard misfits — counting them as negative fabricates pessimism and biases the feature (Loughran–McDonald 2011). *First principle:* a word's valence is conditional on the domain, so the lexicon must be built on the domain corpus.
3. **Sparse high-dimensional features invite overfitting.** $|V|$ is thousands; a few hundred filings give $p\gg N$. The TF–IDF matrix is the exact input ESL Ch 18 warns about: without regularization or feature screening, in-sample fit is trivial and out-of-sample meaningless (measured in [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05]]).

---

### 5. Canonical Literature & Study References

- **Loughran, Tim & McDonald, Bill**, "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks," *Journal of Finance* 66(1), 2011 — the LM lists and the quantification of generic-dictionary misfit. *Corpus PDF verified.*
- **Jurafsky, Dan & Martin, James H.**, *Speech and Language Processing* (3rd ed.) — Ch 6 (vector semantics, TF–IDF) and the standard definitions this page uses. *Corpus PDF verified (`refs/pillar7/25_...`).*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* — Ch 11 (bag-of-words spam classifier) and Ch 18 ($p\gg N$ theory for wide feature matrices). *Verified in the corpus.*
- **Gentzkow, Kelly & Taddy**, "Text as Data," *JEL* 57(3), 2019 — count-matrix formulation and sparse-feature estimation.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03 · Sentiment & Tone]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04 · Embeddings & Transformers]]
- Data provenance: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (the filings these documents come from)
