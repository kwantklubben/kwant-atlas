---
title: "Financial NLP & Transcripts"
tags:
  - pillar-machine-learning
  - financial-nlp-and-transcripts
  - text-as-data
  - sentiment
  - index-hub
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (regression on the feature matrix) and [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] (why a text-derived signal dies without leak-proof evaluation). The *inputs* being mined are described in [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Over 80% of actionable corporate information arrives as **unstructured text**: 10-K/10-Q filings, earnings-call transcripts, press releases, analyst reports, and news wires. The discretionary analyst's skill is reading *between* the lines — tone, hedging, evasiveness, and year-over-year phrasing shifts. Financial NLP is that reading made **algorithmic, repeatable, and testable at scale**: quantify a document's sentiment, measure how much the words *changed* from last quarter, and regress those text features on subsequent returns.

The empirical spine is three results every quant should know cold:

1. **Tetlock (2007)** — the *negative-word fraction* of the *Wall Street Journal*'s "Abreast of the Market" column predicts down-pressure on returns and is followed by reversal; media pessimism is a measurable, market-moving feature.
2. **Loughran & McDonald (2011)** — generic sentiment dictionaries (Harvard's General Inquirer, Henry's list) are **badly miscalibrated for finance**: "tax", "cost", "liability", "share", "gross", and "unrealized" get mislabeled because they are not actually negative in an accounting context. Finance needs its **own** dictionary — the LM lists — built by hand-sorting 10-K word frequencies.
3. **Gentzkow, Kelly & Taddy (2019)** — "Text as Data" unifies the machinery: any text corpus is a sparse count matrix, and the *statistical* question is always the same — which low-dimensional function of the counts predicts an outcome (a return, a label, a topic) out of sample.

> **The one-sentence essence.** "Text is a signal when the *words a firm chose* — not just its reported numbers — carry incremental information, and that signal is extracted by turning documents into numeric feature vectors (dictionaries → bags of words → embeddings) and regressing the outcome on them *without* leaking the future."

This folder is the **hub**. It (a) gives the fast **bag-of-words → TF-IDF → sentiment → regression pipeline** and its two killer lookup numbers (the LM negative-fraction and the $p\gg N$ overfitting cost) below, and (b) routes to six sub-pages that climb from raw intuition to transformer-based earnings-call analysis.

---

### 2. Mathematical Ground Truth & Quick Lookup

**Notation.** Document $d$ as a count vector over the vocabulary: $\mathbf{x}_d\in\mathbb{N}^{|V|}$, where $x_{d,t}$ = number of times term $t$ appears in $d$. $N$ = number of documents, $df_t$ = document frequency (docs containing $t$).

**TF–IDF weight** (the standard feature rescaling that tames ubiquitous words):

$$
\text{tf-idf}(t,d)=\frac{x_{d,t}}{\sum_{t'} x_{d,t'}}\times\Big(\log\frac{N+1}{df_t+1}+1\Big).
$$

**Cosine similarity** (the Loughran–McDonald/Tetlock workhorse for "how similar are two documents", and the basis of the Cohen–Malloy–Nguyen linguistic-change metric):

$$
\text{cos}(\mathbf{v}_d,\mathbf{v}_{d'})=\frac{\mathbf{v}_d\cdot\mathbf{v}_{d'}}{\|\mathbf{v}_d\|\,\|\mathbf{v}_{d'}\|}.
$$

**Net sentiment / tone score** (the single most-used text feature):

$$
\text{tone}(d)=\frac{\#\text{positive words}-\#\text{negative words}}{\text{total words}},\qquad \text{neg-frac}(d)=\frac{\#\text{LM-negative words}}{\text{total words}}.
$$

**Text-to-signal regression** (the pricing of the feature):

$$
y_d=\beta_0+\beta_1\,\text{tone}(d)+\varepsilon_d,\qquad \text{$y_d$ = forward return (or a label)}.
$$

| Quantity | Formula | Verified check (this folder's runs) |
|---|---|---|
| TF–IDF feature matrix, 4-doc sample | §02 | doc0/3 LM-neg-proportion $0.333$; doc1 $0.000$ |
| Net-tone per news snippet | §03 | $+0.429,\ +0.333,\ 0.000,\ -0.571,\ -0.429,\ -0.286$ |
| OLS tone→return | §03 | $y=0.110+14.244\cdot\text{tone},\ R^2=0.790$ |
| Rank-2 word embedding cosines | §04 | $\cos(\text{earnings},\text{estimates})=0.983$; $\cos(\text{beat},\text{missed})=1.000$ |
| $p\gg N$ n-gram overfit | §05 | 16 docs · 127 features: in-sample $R^2=1.000$, leave-one-out $R^2=-0.433$ |
| Earnings-call exec Q&A tone → drift | §06 | $y=-0.150+10.797\cdot\text{tone},\ R^2=0.989$ |

---

### 3. Computational Implementation — the whole pipeline in ~40 lines

The full ingest → clean → features → model chain, reproduced identically on the sub-pages (stdlib + numpy only).

```python
# the four-step text-to-signal pipeline, end to end
import numpy as np

def tokenize(text):                       # 1) INGEST+clean: lowercase, split on punctuation
    return [w.lower() for w in text.replace(',', ' ').replace('.', ' ').split()]

POS = {"record", "raised", "expanded", "robust", "strong", "delivered"}
NEG = {"cut", "forecast", "charge", "impairments", "hurt", "loss", "reduced", "rose", "costs"}

def tone(text):                           # 2) FEATURES: net sentiment per document
    c = {}
    for w in tokenize(text):
        c[w] = c.get(w, 0) + 1
    n = sum(c.values()) or 1
    return (sum(v for w, v in c.items() if w in POS)
            - sum(v for w, v in c.items() if w in NEG)) / n

docs = ["we delivered record revenue and raised guidance",
        "margins expanded and demand remains robust",
        "results were in line with our plan",
        "costs rose and we cut our forecast",
        "a charge for impairments hurt reported earnings",
        "we took a loss and reduced guidance"]
X = np.array([[1.0, tone(d)] for d in docs])          # design matrix
y = np.array([8.0, 4.5, 0.2, -4.0, -6.5, -9.0])       # next-day drift (%)
beta, *_ = np.linalg.lstsq(X, y, rcond=None)          # 3) MODEL: OLS
pred = X @ beta
r2 = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
print("tone:", [f"{tone(d):+.3f}" for d in docs])
print(f"forward_return = {beta[0]:+.3f} + {beta[1]:+.3f}*tone   R^2 = {r2:.3f}")
```
```
tone: ['+0.429', '+0.333', '+0.000', '-0.571', '-0.429', '-0.286']
forward_return = +0.110 + +14.244*tone   R^2 = 0.790
```

---

### 4. Failure Modes & First-Principles Breakdowns (hub signposts)

The full analysis lives in [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Dictionary misfit** — applying a general (non-finance) lexicon to 10-Ks mislabels "liability", "tax", "gross" as negative; the *first principle* is that a word's valence is **domain-conditional** (Loughran–McDonald 2011).
2. **Look-ahead from restated/leaked text** — a 10-K you read today contains restatements a trader did not have at the close; a transcript's *full text* can embed a number only released after the call. Text must be timestamped point-in-time exactly like numbers (see [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]).
3. **Overfitting with many n-grams** — a vocabulary of thousands of sparse binary features on a few hundred filings is the canonical $p\gg N$ problem (ESL Ch 18): in-sample fit climbs to $R^2=1$ while out-of-sample collapses (this folder's run: $1.000$ vs $-0.433$).

---

### 5. Canonical Literature & Study References

- **Loughran, Tim & McDonald, Bill**, "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks," *Journal of Finance* 66(1):35–65, 2011 — the finance-specific LM dictionaries and the measurement of why generic lexicons fail. *Corpus PDF verified (`refs/pillar7/28_...`).*
- **Tetlock, Paul C.**, "Giving Content to Investor Sentiment: The Role of Media in the Stock Market," *Journal of Finance* 62(3):1139–1168, 2007 — the foundational media-content/returns result. *Corpus PDF verified.*
- **Gentzkow, Matthew, Kelly, Bryan & Taddy, Matt**, "Text as Data," *Journal of Economic Literature* 57(3):535–574, 2019 — the unifying count-matrix + prediction framework this folder operationalizes.
- **Araci, Dogu**, "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models," arXiv:1908.10063, 2019; and **Yang, Yi, Uy, Mark C.S. & Huang, Allen**, "FinBERT: A Pretrained Language Model for Financial Communications," arXiv:2006.08097, 2020 — the finance-domain transformers used for the deep-sentiment track.
- **Cohen, Lauren, Malloy, Christopher & Nguyen, Quoc**, "Lazy Prices," *Journal of Finance* 75(3):1371–1415, 2020 — linguistic change in filings as a priced signal.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 18 ($p\gg N$) and Ch 11 (the classic bag-of-words spam classifier). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] (the evaluation discipline every text signal inherits)
- Data provenance: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (point-in-time filings — where the text comes from) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (earnings management the text may reveal)
- Sibling topic: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alternative Data Pipelines & Evaluation]] (alt-data hygiene)
- Sub-pages (in-folder): 01 From Zero · 02 Bag-of-Words & LM Dictionary · 03 Sentiment & Tone · 04 Embeddings & Transformers · 05 Failure Modes · 06 Advanced Extensions (Earnings-Call Analysis)

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/01-from-zero-intuition|01 · From Zero]] — why words are priced, with the count-based demo.
- **Feature engineering + code (undergrad/job-seeking):** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02 · Bag-of-Words & LM Dictionary]] → [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03 · Sentiment & Tone]] (build the feature matrix and run the regression).
- **Deep models (graduate):** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04 · Embeddings & Transformers]].
- **Robustness (practitioner):** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/06-advanced-extensions|06 · Advanced Extensions (Earnings-Call Analysis)]].
- Forward: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]
