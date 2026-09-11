---
title: "06 — Advanced Extensions: Earnings-Call Analysis & the Full Pipeline"
tags:
  - pillar-machine-learning
  - financial-nlp-and-transcripts
  - earnings-calls
  - pipeline
  - advanced
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03 · Sentiment & Tone]] and [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04 · Embeddings & Transformers]].

---

### 1. Intuition & Practical Objective

Earnings calls are the *highest-signal* financial text because they are **two-staged**: a scripted opening (prepared remarks) and a spontaneous **Q&A** that management cannot fully script. The discretionary analyst's edge is reading the Q&A — the hedging, the evasions, the unquantified caveats. Earnings-call analysis quantifies that edge by:

1. **Separating the stages** — prepared remarks carry boilerplate and managed tone; the **Q&A** carries the incremental, less-filtered information. Measuring them separately is itself the feature.
2. **Weighting by speaker and content** — an unquantified answer from the CFO about a charge is worth more than a scripted "we remain confident."
3. **Running the full pipeline** — ingest (transcript segments) → clean (tokenize) → features (per-segment tone, linguistic change vs last quarter) → model (regress post-call drift on executive Q&A tone).

This is where the folder's pieces assemble: the LM-calibrated tone ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02]]/[[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03]]) is the feature; the Q&A-vs-prepared split is the *textual* analog of the earnings-quality idea that spontaneous disclosures are more informative than scripted ones ([[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]); and a FinBERT ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04]]) contextual head replaces the dictionary when labeled training data justify it.

**The advanced theme, one sentence:** *"the information in an earnings call is not uniform — it concentrates in the least-scripted, least-boilerplate text, so the pipeline must separate, weight, and timestamp that text before any model sees it."*

---

### 2. Mathematical Ground Truth & Derivations

**The weighted executive-tone feature.** For a call with Q&A segments $s$, each with word count $w_s$ and net tone $\text{tone}(s)$, the executive-weighted score is

$$
\text{ExecTone}=\frac{\sum_{s\in\text{Q\&A},\,s\in\{\text{CEO,CFO}\}} w_s\cdot\text{tone}(s)}{\sum_{s\in\text{Q\&A},\,s\in\{\text{CEO,CFO}\}} w_s},
$$

a *word-weighted* average so longer, more substantive answers dominate. Contrast the two summary scalars you would otherwise conflate:

$$
\overline{\text{tone}}_{\text{prepared}}=\frac1{|P|}\sum_{s\in P}\text{tone}(s),\qquad \overline{\text{tone}}_{\text{Q\&A}}=\frac1{|Q|}\sum_{s\in Q}\text{tone}(s).
$$

A systematic *gap* — scripted optimism vs. guarded Q&A — is itself a signal (the "tone gap" used in the earnings-call literature to flag management holding back).

**The cross-sectional model.** Across $n$ firms, regress post-call drift on executive Q&A tone:

$$
y_i=\beta_0+\beta_1\,\text{ExecTone}_i+\varepsilon_i,
$$

estimated by OLS (normal equations as in [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03]]). A stable positive $\beta_1$ is the claim that Q&A tone is priced.

**Linguistic change as a separate signal.** Using TF–IDF document vectors ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary|02]]):

$$
\Delta\text{Text}_t=1-\cos(\mathbf{v}_{t},\mathbf{v}_{t-1}),
$$

the "Lazy Prices" construction (Cohen–Malloy–Nguyen 2020): *silent* wording changes in a firm's filings — no number changed — forecast underperformance. This is a *structural* text feature orthogonal to sentiment, and it generalizes directly to year-over-year transcript comparison.

---

### 3. Computational Implementation — the full pipeline on a mini call + cross-section

Ingests a transcript, separates prepared vs Q&A, computes the word-weighted executive Q&A tone, and regresses post-call drift across five firms.

```python
import math

transcript = [
    ("CEO", "prepared", "We delivered record revenue and raised guidance for the year."),
    ("CFO", "prepared", "Margins expanded and costs remained flat in the quarter."),
    ("Analyst", "qa", "Can you explain the decline in free cash flow?"),
    ("CEO", "qa", "That reflects one-time restructuring charges, not a deterioration."),
    ("Analyst", "qa", "Should we expect further impairments ahead?"),
    ("CFO", "qa", "No, we have taken the loss and the balance sheet is clean going forward."),
    ("CEO", "qa", "We remain confident in strong demand into next year."),
]
POS = {"record", "raised", "expanded", "strong", "confident", "growth", "increased", "beat"}
NEG = {"decline", "charges", "impairments", "loss", "deterioration", "cut", "fell", "missed"}

def clean(text):
    return [w.lower() for w in text.replace(',', ' ').replace('.', ' ').split()]

def tone(text):                       # features: net sentiment per segment
    c = {}
    for w in clean(text):
        c[w] = c.get(w, 0) + 1
    total = sum(c.values()) or 1
    return (sum(v for w, v in c.items() if w in POS)
            - sum(v for w, v in c.items() if w in NEG)) / total

seg = []
for speaker, role, text in transcript:
    seg.append((speaker, role, tone(text), len(clean(text))))

prep = [t for _, r, t, _ in seg if r == "prepared"]
qa   = [t for _, r, t, _ in seg if r == "qa"]
print(f"prepared-remarks mean tone = {sum(prep)/len(prep):+.3f}   "
      f"Q&A mean tone = {sum(qa)/len(qa):+.3f}")

num = wsum = 0.0                      # word-weighted executive Q&A tone
for speaker, role, t, n in seg:
    if speaker in ("CEO", "CFO") and role == "qa":
        num += t * n; wsum += n
exectone = num / wsum
print(f"executive Q&A tone (word-weighted) = {exectone:+.3f}")

# cross-section: (exec Q&A tone, post-call 5-day drift) across 5 firms
firms = [(0.31, 3.2), (0.15, 1.1), (-0.02, 0.1), (-0.22, -2.4), (-0.41, -4.8)]
n = len(firms)
X = [[1.0, s] for s, _ in firms]; y = [r for _, r in firms]
G = [[0.0, 0.0], [0.0, 0.0]]; b = [0.0, 0.0]
for r, t in zip(X, y):
    for i in range(2):
        for j in range(2):
            G[i][j] += r[i] * r[j]
        b[i] += r[i] * t
det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
b0 = (b[0] * G[1][1] - b[1] * G[0][1]) / det
b1 = (G[0][0] * b[1] - G[0][1] * b[0]) / det
pred = [b0 + b1 * s for s, _ in firms]
ym = sum(y) / n
r2 = 1.0 - sum((t - p) ** 2 for t, p in zip(y, pred)) / sum((t - ym) ** 2 for t in y)
print(f"cross-section OLS: drift = {b0:+.3f} + {b1:+.3f} * exec_qa_tone   R^2 = {r2:.3f}")
```
```
prepared-remarks mean tone = +0.156   Q&A mean tone = -0.075
executive Q&A tone (word-weighted) = -0.032
cross-section OLS: drift = -0.150 + +10.797 * exec_qa_tone   R^2 = 0.989
```

The numbers carry the whole story. The **prepared remarks** are optimistic (+0.156) but the **Q&A** is guarded (−0.075): management leads with confidence and then hedges under questioning — the tone gap a purely scripted analysis would miss. Weighted over CEO/CFO Q&A the executive tone is −0.032, and across the five-firm cross-section drift tracks it with slope **+10.797** and $R^2=0.99$. On a real panel $R^2$ will fall far below this clean sample, but the *direction* — spontaneous Q&A tone is priced, and it differs from scripted tone — is exactly the mechanism the earnings-call literature reports.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading the whole call as one blob.** Averaging sentiment over scripted + spontaneous text dilutes the Q&A signal with boilerplate (the prepared/Q&A gap measured above is invisible to a single score). *Fix:* separate and weight the stages.
2. **Transcript timing.** A call is public only after it ends — usually after the close. Computing features from the *full* transcript and backdating them to the pre-call open is look-ahead by construction ([[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05]]).
3. **Overfitting the segments.** Each call yields many per-segment features but few independent quarters; a model with more features than firms is the $p\gg N$ trap again. *Fix:* keep features few and principal, screen in-fold.
4. **Speaker misassignment / transcript errors.** ASR transcripts misattribute and garble; a CEO's answer tagged to an analyst inverts the weighting. *Fix:* validate speaker tags and weight conservatively.
5. **Earnings-quality confound.** Tone correlates with the *reported* numbers; without controlling for the accrual content you may be pricing the accruals, not the words ([[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]).

---

### 5. Canonical Literature & Study References

- **Cohen, Lauren, Malloy, Christopher & Nguyen, Quoc**, "Lazy Prices," *Journal of Finance* 75(3), 2020 — the linguistic-change metric ($1-\cos$) and its return predictability. *Corpus section referenced.*
- **Araci, Dogu**, "FinBERT," arXiv:1908.10063, 2019; **Yang, Uy & Huang**, "FinBERT," arXiv:2006.08097, 2020 — contextual sentiment for transcripts when labeled data justify deep models.
- **Dechow, Patricia, Ge, Weili & Schrand, Catherine**, "Understanding Earnings Quality," 2010 — text as the narration of the earnings-quality gap (*corpus ref `40_Dechow_2010`*).
- **Healy, Paul & Wahlen, James**, "A Review of the Earnings Management Literature," *Journal of Accounting & Economics* 27(2), 1999 — disclosure choice and the narrative incentives behind managed tone (*corpus ref `39_Healy_1999`*).
- **Loughran & McDonald**, "When Is a Liability Not a Liability?" *Journal of Finance* 66(1), 2011 — the LM dictionaries underlying every tone feature here. *Corpus PDF verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/03-sentiment-and-tone|03 · Sentiment & Tone]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/04-embeddings-and-transformers|04 · Embeddings & Transformers]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Index Hub]]
- Earnings quality: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (the narrative of managed numbers)
- Data & hygiene: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data (PIT text)]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alternative Data Pipelines & Evaluation]]
- Models: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
