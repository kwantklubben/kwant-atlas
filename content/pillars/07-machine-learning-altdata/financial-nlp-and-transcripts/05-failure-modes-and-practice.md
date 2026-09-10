---
title: "05 — Failure Modes & Real-World Practice: Where Text Signals Die"
tags:
  - pillar-machine-learning
  - financial-nlp-and-transcripts
  - failure-modes
  - overfitting
  - look-ahead
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04 · Embeddings & Transformers]] and [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] (the discipline this page applies to text).

---

### 1. Intuition & Practical Objective

A text signal is a feature pipeline — **ingest → clean → features → model** — and it dies at any stage. This page names the failures that specifically kill *text* signals, ties each to a first principle, and *measures* the biggest one (n-gram overfitting). In one line each:

1. **Look-ahead from restated / leaked text** — the words you read today were not all knowable at the signal timestamp ([[fundamentals-accounting/data-sources-and-corporate-data/index|point-in-time hygiene]]).
2. **Dictionary misfit** — a general lexicon counts accounting vocabulary as sentiment (Loughran–McDonald 2011; [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02]]).
3. **Overfitting with many n-grams** — thousands of sparse, near-unique phrase features on a thin panel is the textbook $p\gg N$ problem (ESL Ch 18): in-sample perfection, out-of-sample collapse.
4. **Boilerplate / linguistic decay** — mandatory copy and decades-old phrasing flood the counts and dilute or fake the signal.
5. **Uncontrolled signal timing** — earnings-call text is public only after the call; filings after the open are not tradeable at the open.

> **The one-line takeaway.** "Ask of every text feature: *was this string, and this sentiment, knowable at the timestamp I'm using it?* — and *am I fitting more parameters than I have independent documents?*"

---

### 2. Mathematical Ground Truth & Derivations

**The pipeline's failure points.**

- **Look-ahead (first principle: no future information at the as-of timestamp).** A restated 10-K or a full call transcript contains strings a trader could not see on the trading day. Formally, if $\mathcal{D}(t)$ is the set of text knowable at $t$, any feature computed on $\mathcal{D}(t_{\text{now}})$ substitutes the restated, leaked, survivor-filtered record for what was actually knowable — the exact arithmetic of the restatement gap documented in [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|Data Sources §01]]. The fix is strict point-in-time (PIT) text: timestamp each document by its *public release*, and cut features at the as-of date.

- **Dictionary misfit.** Let $N_{\text{gen}}$ be the generic-dictionary negative set. Its false-negative count for a 10-K is large because $N_{\text{gen}}\cap\{\text{accounting terms}\}\ne\varnothing$ ("liability", "tax", "cost", "gross", "share", "unrealized"). The bias it injects is a *mechanical, domain-driven* increase in measured pessimism — independent of actual sentiment. Loughran–McDonald (2011) measure and remove it with finance-native lists.

- **Overfitting (first principle: parameters ≤ information).** A vocabulary of $|V|$ terms plus their $n$-grams gives $p$ features; with $N$ filings, the effective sample is $N_{\text{eff}}\approx N$ (overlapping text means less independent information than $N$). When $p\gg N_{\text{eff}}$, OLS fits noise exactly: the in-sample residual can be driven to zero while the out-of-sample prediction is worthless. The **curse of dimensionality** (ESL Ch 2) and the $p\gg N$ theory (ESL Ch 18) both predict exactly what the experiment below shows.

---

### 3. Computational Implementation — n-gram overfitting, measured

16 synthetic documents whose true signal comes from a handful of sentiment words, expanded into a 127-feature unigram+bigram space. As we add features, watch in-sample $R^2$ race to 1.000 while leave-one-out $R^2$ stays negative.

```python
import math, random

def tokens(t):
    return [w.lower() for w in t.replace(',', '').replace('.', '').split()]

def ngrams(tk, n):
    return ["_".join(tk[i:i + n]) for i in range(len(tk) - n + 1)]

random.seed(7)
TRUE = {"growth": 3.0, "demand": 2.0, "cut": -4.0, "loss": -5.0}
NOISE = ["firm", "results", "quarter", "plan", "operating", "segment", "capital",
         "review", "initiative", "environment", "process", "execution"]
N = 16
docs, y = [], []
for _ in range(N):
    tk = [random.choice(NOISE) for _ in range(random.randint(6, 9))]
    tk += random.sample(list(TRUE), random.randint(1, 2))   # inject the true drivers
    random.shuffle(tk)
    docs.append(tk)
    y.append(sum(TRUE.get(w, 0) for w in tk) + random.gauss(0, 0.6))

feats = []
for tk in docs:
    for w in ngrams(tk, 1) + ngrams(tk, 2):
        if w not in feats:
            feats.append(w)
P = len(feats)
print(f"corpus of {N} documents, {P} unigram+bigram features  -> p >> n ({P} > {N})")

def design(D):
    X = []
    for tk in docs:
        fs = set(tk) | set(ngrams(tk, 2))
        X.append([1.0] + [1.0 if feats[i] in fs else 0.0 for i in range(D)])
    return X

def ols(X, yy):
    p = len(X[0])
    G = [[0.0] * p for _ in range(p)]; b = [0.0] * p
    for r, t in zip(X, yy):
        for i in range(p):
            for j in range(p):
                G[i][j] += r[i] * r[j]
            b[i] += r[i] * t
    for i in range(p):
        G[i][i] += 1e-9
    A = [row[:] for row in G]; bb = b[:]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(A[r][col]))
        A[col], A[piv] = A[piv], A[col]; bb[col], bb[piv] = bb[piv], bb[col]
        for r in range(col + 1, p):
            f = A[r][col] / A[col][col]
            for c in range(col, p):
                A[r][c] -= f * A[col][c]
            bb[r] -= f * bb[col]
    coef = [0.0] * p
    for r in range(p - 1, -1, -1):
        coef[r] = (bb[r] - sum(A[r][c] * coef[c] for c in range(r + 1, p))) / A[r][r]
    return coef

def r2(yy, pred):
    ym = sum(yy) / len(yy)
    return 1.0 - sum((t - p) ** 2 for t, p in zip(yy, pred)) / sum((t - ym) ** 2 for t in yy)

def loo(D):
    Xf = design(D); errs = []
    for h in range(N):
        idx = [i for i in range(N) if i != h]
        coef = ols([Xf[i] for i in idx], [y[i] for i in idx])
        pred = sum(c * x for c, x in zip(coef, Xf[h]))
        errs.append((y[h] - pred) ** 2)
    ym = sum(y) / N
    return 1.0 - sum(errs) / sum((t - ym) ** 2 for t in y)

for D in (1, 2, 4, 8, 14, 20, 30):
    Xf = design(D)
    coef = ols(Xf, y)
    isr = r2(y, [sum(c * x for c, x in zip(coef, row)) for row in Xf])
    print(f"  features used={D:3d}:  in-sample R^2={isr:+.3f}   "
          f"leave-one-out R^2={loo(D):+.3f}")
```
```
corpus of 16 documents, 127 unigram+bigram features  -> p >> n (127 > 16)
  features used=  1:  in-sample R^2=+0.104   leave-one-out R^2=-0.171
  features used=  2:  in-sample R^2=+0.150   leave-one-out R^2=-0.283
  features used=  4:  in-sample R^2=+0.216   leave-one-out R^2=-0.638
  features used=  8:  in-sample R^2=+0.764   leave-one-out R^2=-0.499
  features used= 14:  in-sample R^2=+0.851   leave-one-out R^2=-0.520
  features used= 20:  in-sample R^2=+0.886   leave-one-out R^2=-1.906
  features used= 30:  in-sample R^2=+1.000   leave-one-out R^2=-0.433
```

This is the single most important number in the folder: with 30 of 127 n-gram features on 16 documents, the model reports **in-sample $R^2=1.000$** — perfect fit — while out-of-sample it is **worse than predicting the mean ($-0.433$)**. Every finance-NLP overfitting claim you will ever see is this exact shape: more phrase features than independent filings, and the "in-sample alpha" is memorized noise. The disciplines that prevent it — feature screening inside CV folds, regularization, purged/embargoed splits — are in [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] and [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged & Embargoed CV]].

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Look-ahead via restated / leaked text.** Using today's restated filing or the *full* (post-call) transcript at an earlier timestamp. *Fix:* timestamp every document by public release; features only from text knowable at as-of ([[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]).
2. **Dictionary misfit.** Generic lexicons count "liability", "tax", "gross", "unrealized" as negative, biasing the feature (Loughran–McDonald 2011). *Fix:* finance-native LM lists.
3. **Overfitting with many n-grams.** $p\gg N$ on sparse phrase features → in-sample $R^2\to1$, out-of-sample collapse (this page's run). *Fix:* screen features *inside* CV folds, regularize (lasso/elastic net — ESL Ch 18), cap $n$-gram order.
4. **Boilerplate and linguistic decay.** Mandatory copy dilutes counts; a 2005-trained lexicon misreads 2024 calls. *Fix:* target active text (MD&A, Q&A), and refresh vocabularies/models over time.
5. **Signal timing.** An earnings call that ends after close is not tradeable at the open; a filing released 4 p.m. is not tradeable at 9:30. *Fix:* use release timestamps and match the tradable window to them.

---

### 5. Canonical Literature & Study References

- **Loughran, Tim & McDonald, Bill**, "When Is a Liability Not a Liability?" *Journal of Finance* 66(1), 2011 — dictionary misfit measured and fixed. *Corpus PDF verified.*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* — Ch 2 (curse of dimensionality), Ch 18 ($p\gg N$: sparse methods, feature screening, the exact regime n-gram models live in). *Verified in the corpus.*
- **López de Prado, Marcos**, *Advances in Financial Machine Learning* — Ch 7 (purged/embargoed CV for overlapping text+returns) — see [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged & Embargoed CV]].
- **Gentzkow, Kelly & Taddy**, "Text as Data," *JEL* 57(3), 2019 — sparse-feature estimation and regularization for count matrices.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04 · Embeddings & Transformers]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/06-advanced-extensions|06 · Advanced Extensions (Earnings-Call Analysis)]]
- Disciplines: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged & Embargoed CV]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data (PIT hygiene)]]
