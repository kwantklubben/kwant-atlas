---
title: "Financial NLP & Earnings Transcripts"
tags:
  - pillar-ml-altdata
  - nlp
  - finbert
  - earnings-transcripts
---

**Basic Prerequisites:** Basic NLP concepts (Tokenization, Word Embeddings, Transformers).

---

### 1. Intuition & Practical Objective

Over 80% of actionable financial data is unstructured text: corporate quarterly 10-Q/10-K filings, conference call transcripts, central bank speeches, and financial news wires.

Discretionary analysts spend hours listening to the tone and subtle phrasing shifts of CEOs during conference call Q&A sessions. Quantitative NLP automates this at institutional scale: quantifying sentiment, measuring structural textual divergence between consecutive quarterly filings, and extracting subtle tone hedging using domain-specific models like **FinBERT**.

---

### 2. Mathematical Ground Truth & Derivations

#### Linguistic Change Metric in SEC Filings (Cohen, Malloy, & Nguyen, 2020)
Let $D_t$ and $D_{t-1}$ be the tokenized document text of a firm's 10-K filing in consecutive years.
Compute cosine similarity between document term vectors:
$$\text{Cosine Sim}(D_t, D_{t-1}) = \frac{\mathbf{v}_t \cdot \mathbf{v}_{t-1}}{\|\mathbf{v}_t\| \|\mathbf{v}_{t-1}\|}$$
Linguistic change metric:
$$\Delta \text{Text}_t = 1 - \text{Cosine Sim}(D_t, D_{t-1})$$
**Empirical Finding:** Firms that make significant modifications to their Management Discussion & Analysis (MD&A) or Risk Factors sections underperform peers by over $-7\%$ annualized over the subsequent 12 months.

#### Domain-Specific Transformer Embeddings (FinBERT)
Standard BERT models trained on Wikipedia fail on financial nuance:
- Word: *"Liability"* $\to$ Wikipedia: Legal responsibility (neutral). Finance: Debt obligation (negative risk).
- Word: *"Share"* $\to$ Wikipedia: Distribute/collaborate (positive). Finance: Stock equity (neutral).

FinBERT (Araci, 2019) is pre-trained on corporate filings and Reuters financial news, fine-tuning classification heads for 3-class sentiment:
$$P(\text{Positive}), \quad P(\text{Neutral}), \quad P(\text{Negative})$$
The net sentiment score is:
$$\text{Score} = P(\text{Positive}) - P(\text{Negative})$$

---

### 3. Computational Implementation

```python
import numpy as np

def compute_transcript_qa_sentiment(qa_statements: list[dict]) -> float:
    """
    Computes net sentiment score on executive Q&A responses, 
    weighting analyst questions vs executive answers.
    """
    # Mock probability outputs from FinBERT model
    # statement: {"speaker": "CEO", "pos": 0.15, "neg": 0.05, "words": 45}
    total_words = 0
    weighted_sentiment = 0.0
    
    for s in qa_statements:
        if s["speaker"] in ["CEO", "CFO"]: # Filter to executive remarks
            net_s = s["pos"] - s["neg"]
            weighted_sentiment += net_s * s["words"]
            total_words += s["words"]
            
    return weighted_sentiment / total_words if total_words > 0 else 0.0

# Example mock conference call Q&A
sample_qa = [
    {"speaker": "Analyst", "pos": 0.10, "neg": 0.10, "words": 20},
    {"speaker": "CEO", "pos": 0.65, "neg": 0.05, "words": 80},
    {"speaker": "CFO", "pos": 0.20, "neg": 0.40, "words": 50},
]
score = compute_transcript_qa_sentiment(sample_qa)
print(f"Executive Net Sentiment Score: {score:+.3f}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Executive Tone Management & Boilerplate Gaming:**
   - *Failure:* Public CEOs employ media consultants who script answers to sound relentlessly optimistic.
   - *Remedy:* Focus on the Q&A spontaneous section rather than the prepared opening remarks; measure disfluencies ("uh", "um", pauses) and passive voice frequency.

2. **Linguistic Decay:**
   - *Failure:* Training an NLP dictionary or model on 2005 transcripts and applying it to 2024 tech earnings calls.

---

### 5. Canonical Literature & Study References

- **Cohen, Lauren, Malloy, Christopher, & Nguyen, Quoc**: *Lazy Prices*, Journal of Finance 75(3), 1371-1415 (2020).
- **Araci, Dogu**: *FinBERT: Financial Sentiment Analysis with Pre-trained Language Models*, arXiv:1908.10063 (2019).

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation|Alternative Data Pipelines]]
- Bridges to: [[pillars/01-quantitative-research/fundamental-multi-factor-models|Factor Models]]
