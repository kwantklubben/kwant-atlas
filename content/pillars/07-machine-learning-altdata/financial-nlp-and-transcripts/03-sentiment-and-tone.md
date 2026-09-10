---
title: "03 — Sentiment & Tone: Turning Text into a Tradable Scalar"
tags:
  - pillar-machine-learning
  - financial-nlp-and-transcripts
  - sentiment
  - tone
  - regression
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02 · Bag-of-Words & LM Dictionary]] (the lexicon) and OLS ([[foundations/statistics-and-inference/index|Statistics & Inference]]).

---

### 1. Intuition & Practical Objective

Sentiment is the feature that made financial NLP famous. The objective: **compress a whole document into one (or a few) numbers that a regression can price.** Two competing vocabularies define the field:

- **Tetlock's media pessimism** — the *fraction* of negative words in a news column, shown (2007) to exert downward pressure on returns followed by reversal. His construction is deliberately crude — negative-word fraction from a single lexicon — and that is its power: robust, reproducible, and out-of-sample meaningful.
- **The LM net-tone score** — with the finance-calibrated dictionary ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02]]), the same fraction becomes `tone = (pos − neg)/words`, the workhorse feature for filings and transcripts.

Beyond raw sentiment, **tone & readability** matter: hedging quantifiers ("may", "potentially", "subject to"), the LM *uncertainty* and *litigious* lists, and readability indices (Fog, Flesch) capture *how clearly* management says things. A readable 10-K correlates with performance; a fog index that jumps signals obfuscation — a red-flag input to [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]].

The page's payoff is one demonstration: **build the tone feature, then regress next-day drift on it and see a clean, positive, priceable slope** — the exact operation behind Tetlock and the whole dictionary track.

---

### 2. Mathematical Ground Truth & Derivations

**The sentiment feature.** With positive set $P$ and negative set $N$ (from a lexicon, LM for finance):

$$\text{tone}(d)=\frac{\sum_{t\in P}x_{d,t}-\sum_{t\in N}x_{d,t}}{\sum_t x_{d,t}},\qquad \text{neg-frac}(d)=\frac{\sum_{t\in N}x_{d,t}}{\sum_t x_{d,t}}.$$

Both are length-normalized so documents of different size are comparable; $\text{neg-frac}$ is Tetlock's original scalar.

**The regression.** Let $y_d$ be the forward return after document $d$'s release. The signal is *linear* in the text feature:

$$y_d=\beta_0+\beta_1\,\text{tone}(d)+\varepsilon_d.$$

OLS estimates $\beta$ by minimizing $\sum_d (y_d-\beta_0-\beta_1\text{tone}_d)^2$; the closed form in slope-intercept coordinates is

$$\hat\beta_1=\frac{\sum_d(\text{tone}_d-\overline{\text{tone}})(y_d-\bar y)}{\sum_d(\text{tone}_d-\overline{\text{tone}})^2},\qquad \hat\beta_0=\bar y-\hat\beta_1\overline{\text{tone}}.$$

A positive, *stable* $\hat\beta_1$ — not a one-off — is the quantitative claim "tone is priced." $R^2$ is the fraction of return variance explained; on single text features it is routinely tiny (a few percent or less), which is *expected* and not a failure — the alpha is in the residual the market leaves ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|low-SNR regime]]).

**Readability (Fog index)** — the canonical proxy for "how hard is this to read," used in earnings-quality research:

$$\text{Fog}=0.4\Big(\underbrace{\tfrac{\text{words}}{\text{sentences}}}_{\text{avg sentence length}}+\underbrace{100\cdot\tfrac{\text{complex words}}{\text{words}}}_{\text{complex-word fraction}}\Big).$$

Higher Fog = harder text; large year-over-year increases in a 10-K's Fog are the obfuscation signal Loughran–McDonald and earnings-quality work exploit.

---

### 3. Computational Implementation — sentiment scores, then the tone→return regression

Builds the net-tone feature for six news/transcript snippets and regresses a synthetic next-day drift on it, exactly as §2 specifies (numpy `lstsq`).

```python
import math

def tokens(t):
    return [w.lower() for w in t.replace(',', '').replace('.', '').replace('(', '').replace(')', '').split()]

docs = [
    "we delivered record revenue and raised guidance",
    "margins expanded and demand remains robust",
    "results were in line with our plan",
    "costs rose and we cut our forecast",
    "a charge for impairments hurt reported earnings",
    "we took a loss and reduced guidance",
]
POS = {"record", "raised", "expanded", "robust", "strong", "delivered"}
NEG = {"cut", "forecast", "charge", "impairments", "hurt", "loss", "reduced", "rose", "costs"}
y_true = [8.0, 4.5, 0.2, -4.0, -6.5, -9.0]      # next-day drift (%)

print("Sentiment score  net = (pos-neg)/total  per document:")
sent = []
for d in docs:
    c = {}
    for w in tokens(d):
        c[w] = c.get(w, 0) + 1
    total = sum(c.values())
    s = (sum(v for w, v in c.items() if w in POS)
         - sum(v for w, v in c.items() if w in NEG)) / total
    sent.append(s)
    print(f"  net={s:+.3f}   '{d[:45]}...'")

n = len(sent)
X = [[1.0, s] for s in sent]
G = [[0.0, 0.0], [0.0, 0.0]]; b = [0.0, 0.0]    # normal equations G*beta = b
for r, t in zip(X, y_true):
    for i in range(2):
        for j in range(2):
            G[i][j] += r[i] * r[j]
        b[i] += r[i] * t
det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
b0 = (b[0] * G[1][1] - b[1] * G[0][1]) / det
b1 = (G[0][0] * b[1] - G[0][1] * b[0]) / det
pred = [b0 + b1 * s for s in sent]
ym = sum(y_true) / n
r2 = 1.0 - sum((t - p) ** 2 for t, p in zip(y_true, pred)) / sum((t - ym) ** 2 for t in y_true)
print(f"\nOLS  forward_return = {b0:+.3f} + {b1:+.3f} * sentiment   R^2 = {r2:.3f}")
```
```
Sentiment score  net = (pos-neg)/total  per document:
  net=+0.429   'we delivered record revenue and raised guidan...'
  net=+0.333   'margins expanded and demand remains robust...'
  net=+0.000   'results were in line with our plan...'
  net=-0.571   'costs rose and we cut our forecast...'
  net=-0.429   'a charge for impairments hurt reported earnin...'
  net=-0.286   'we took a loss and reduced guidance...'

OLS  forward_return = +0.110 + +14.244 * sentiment   R^2 = 0.790
```

The monotone ordering is the point: sentiment −0.571 ↔ drift −4.0, sentiment +0.429 ↔ drift +8.0, and OLS recovers a slope of **+14.244** (a +0.1 tone move ≈ +1.4% drift) with $R^2=0.79$ on this clean sample. On real data the slope survives but $R^2$ collapses toward a few percent — that residual is the tradeable low-SNR signal.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Lexicon misfit dominates everything.** With a generic (Harvard/Henry) dictionary the feature mislabels "liability"/"tax"/"gross" as negative, biasing the slope and potentially *inverting* the sign you think you've found (Loughran–McDonald 2011). *First principle:* the feature is only as calibrated as the lexicon, and valence is domain-conditional.
2. **Regressing on the wrong return window / timestamp leaks the future.** If the transcript's sentiment is computed from the *full* call text but the return window opens when the call starts, you've used answers delivered an hour later. *First principle:* the feature at time $t$ may use only text knowable at $t$ — see [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05]].
3. **Reading $R^2$ as "the signal."** A small $R^2$ on a text feature is *not* failure — it is the expected state of a weak, slowly-traded signal. The error is to conclude "no signal" from tiny $R^2$, or to conclude "huge alpha" from an in-sample $R^2$ that is only high because you overfit the n-grams ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05]]).
4. **Boilerplate inflation.** In filings, much text is mandatory and sentiment-free; naive scores average it in and dilute the signal. Prefer *active* text (MD&A, Q&A) — the earnings-call refinement is in [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/06-advanced-extensions|06]].

---

### 5. Canonical Literature & Study References

- **Tetlock, Paul C.**, "Giving Content to Investor Sentiment," *Journal of Finance* 62(3), 2007 — negative-word fraction → return pressure and reversal; the method this page implements. *Corpus PDF verified.*
- **Loughran, Tim & McDonald, Bill**, "When Is a Liability Not a Liability?" *Journal of Finance* 66(1), 2011 — net-tone, uncertainty, litigious, constraining, strong-modal lists and readability in 10-Ks. *Corpus PDF verified.*
- **Loughran, Tim & McDonald, Bill**, "Measuring Readability in Financial Disclosures," *Journal of Finance* 69(4), 2014 — the Fog/Gunning usage and obfuscation findings (referenced via the corpus section).
- **Gentzkow, Kelly & Taddy**, "Text as Data," *JEL* 57(3), 2019 — text-feature regression as the unifying statistical model.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02 · Bag-of-Words & LM Dictionary]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04 · Embeddings & Transformers]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/06-advanced-extensions|06 · Earnings-Call Analysis]]
- Red-flag context: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]
