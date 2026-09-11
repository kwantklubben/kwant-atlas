---
title: "7.4.1 Financial NLP from Zero"
tags:
  - pillar-machine-learning
  - financial-nlp-and-transcripts
  - intuition
  - text-as-data
---

**Basic Prerequisites:** None beyond basic statistics; [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]] for the map.

---

### 1. Intuition & Practical Objective

Why should a quant care about words at all? The numbers are right there in the 10-Q. The answer is **incremental information**: reported numbers are *standardized, delayed, and gamed*, but the words a firm chooses are partly **uncontrolled** — and uncontrolled information is what a signal is made of.

Three mechanisms make text genuinely informative:

1. **Tone is priced but under-reacted.** Tetlock (2007) showed that a single column's pessimism *predicts* downward price pressure and then reversal — i.e. media text contains information the market does not fully absorb instantly. If it were fully absorbed, there would be nothing to measure. The residual drift is the alpha.

2. **Text carries what the table of numbers cannot.** A CEO's prepared remarks and, more so, the live Q&A, contain forecasts, guidance language, hedging ("we *expect*", "potentially", "assuming"), evasiveness, and sentiment about *future* states. Cohen–Malloy–Nguyen (2020) find that firms that silently change their 10-K wording — with no number changing — underperform by over 7% a year: the *wording itself* is the disclosure.

3. **Language choice is a discretionary accounting output.** Earnings numbers are accrual estimates a manager chooses ([[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]); the words are chosen even more freely. Both Dechow–Ge–Schrand (2010) and Healy–Wahlen (1999) model earnings quality as the gap between reported and real performance — text is the observable record of how management narrates that gap, and obfuscation is itself diagnostic.

The objective of this page is one idea: **a document is a vector, and the counts in that vector are already a tradable feature.** No deep learning required to start — the histogram of words already separates a bullish from a bearish call.

---

### 2. Mathematical Ground Truth & Derivations

**The bag-of-words representation.** A document $d$ is mapped to a count vector over a fixed vocabulary:

$$
\mathbf{x}_d=\big(x_{d,1},\,x_{d,2},\,\dots,\,x_{d,|V|}\big),\qquad x_{d,t}=\#\{\text{occurrences of term }t\text{ in }d\}.
$$

Order is discarded ("bag"), so "results beat estimates" and "estimates beat results" produce the *same* vector — the cheapness that makes bag-of-words scale to millions of documents, and the approximation embeddings will later fix ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04]]).

**From counts to a score.** With a sentiment lexicon (a set $P$ of positive, $N$ of negative terms) the natural feature is the net-tone fraction:

$$
\text{tone}(d)=\frac{\sum_{t\in P}x_{d,t}\;-\;\sum_{t\in N}x_{d,t}}{\sum_{t} x_{d,t}}.
$$

This is the feature Tetlock regressed on returns and the feature the whole dictionary track of financial NLP is built on. Its statistical content: a *fraction*, so document length cancels — a 5-page and a 50-page filing are comparable.

**Why the market doesn't arbitrage it away.** If tone forecast returns with certainty, prices would adjust on release and the forecast vanish. What survives is the *weak but real* correlation with drift that does not get fully traded out because it is noisy, slow, and mixed with the fundamental signal — exactly the low-SNR regime of [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]].

---

### 3. Computational Implementation — counts already separate the two calls

The simplest possible text feature: count the words. Run this and *see* that the histogram alone separates a bullish from a bearish release — no model, no training.

```python
def tokenize(text):
    return [w.lower() for w in text.replace(',', ' ').replace('.', ' ').split()]

bull = ("Revenues grew eleven percent driven by record demand. Our margins expanded "
        "and we raised full year guidance. We see robust momentum into next quarter.")
bear = ("Revenues fell short of guidance. We cut our forecast and our margins contracted. "
        "Headcount reductions and inventory writedowns weigh on near term results.")

POS = {"grew", "record", "expanded", "raised", "robust", "momentum", "guidance"}
NEG = {"fell", "short", "cut", "contracted", "reductions", "writedowns", "weigh", "headcount"}

for name, txt in [("bull", bull), ("bear", bear)]:
    counts = {}
    for w in tokenize(txt):
        counts[w] = counts.get(w, 0) + 1
    pos = sum(v for w, v in counts.items() if w in POS)
    neg = sum(v for w, v in counts.items() if w in NEG)
    total = sum(counts.values())
    print(f"{name:5s} total_words={total:3d}  pos_hits={pos}  neg_hits={neg}  "
          f"net={pos-neg:+d}  net_fraction={(pos-neg)/total:+.3f}")
```
```
bull  total_words= 24  pos_hits=7  neg_hits=0  net=+7  net_fraction=+0.292
bear  total_words= 23  pos_hits=1  neg_hits=8  net=-7  net_fraction=-0.304
```

The bull call nets $+0.292$; the bear call $-0.304$ — opposite signs, clean separation, from nothing but word counts and a tiny lexicon. That is the entire bag-of-words intuition; everything later is about making these counts *calibrated* ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02]]) and *regressed on returns* ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"More words is more informative" is false — rarefaction.** A 50-page boilerplate 10-K is *less* informative per word than a 2-page press release. The first principle is that signal is *fractional*: divide by length (as §2 does) or the count is dominated by drafting verbosity, not information. Failing to normalize is the entry-level error.
2. **Dictionary valence is domain-conditional.** "Liability", "tax", "gross", "unrealized" are accounting-normal words but look *negative* to a generic lexicon. Counting them as pessimism fabricates sentiment that does not exist — the exact misfit Loughran–McDonald (2011) measure and the reason [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02]] exists.
3. **Timing: the text's *release* date, not the call date, is the signal timestamp.** A transcript exists publicly only after the call ends (often after close); a filing after the market is open is not tradeable at the open. Using the *wrong* timestamp is look-ahead by construction — see [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05]] and [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]].

---

### 5. Canonical Literature & Study References

- **Tetlock, Paul C.**, "Giving Content to Investor Sentiment," *Journal of Finance* 62(3), 2007 — the foundational "text predicts returns" result (media pessimism → drift then reversal). *Corpus PDF verified.*
- **Loughran, Tim & McDonald, Bill**, "When Is a Liability Not a Liability?" *Journal of Finance* 66(1), 2011 — the motivation for finance-specific dictionaries.
- **Cohen, Lauren, Malloy, Christopher & Nguyen, Quoc**, "Lazy Prices," *Journal of Finance* 75(3), 2020 — silent wording changes in 10-Ks forecast underperformance ($>7\%$/yr).
- **Gentzkow, Matthew, Kelly, Bryan & Taddy, Matt**, "Text as Data," *JEL* 57(3), 2019 — the unified count-matrix view this page's demo is the seed of.
- **Dechow, Patricia, Ge, Weili & Schrand, Catherine**, "Understanding Earnings Quality," 2010 — text as the narration of the earnings-quality gap (*corpus ref `40_Dechow_2010`*).

---

### 6. Connected Graph Bridges

- Base: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] (the low-SNR regime text signals live in)
- Continue: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02 · Bag-of-Words & LM Dictionary]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]]
- Earnings context: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]
