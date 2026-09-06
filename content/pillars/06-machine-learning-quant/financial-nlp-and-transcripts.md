---
title: "Financial NLP & Transcripts (Quartr)"
tags: [machine-learning, nlp, quartr, pead, alternative-data]
---

# Financial NLP & Transcripts (Quartr)

Unstructured textual disclosures contain rich qualitative information that is not immediately reflected in numerical quarterly EPS figures.

## Mining Corporate Disclosures
- **Earnings Call Transcripts:** Analyzing executive tone, question-and-answer evasion, and forward guidance sentiment using Transformers and LLMs.
- **KwantKlubben Integration:** Dump transcripts to `data/raw/` using `data/sources/quartr.py`.
- **Post-Earnings Announcement Drift (PEAD):** Combining positive unexpected earnings surprises with positive sentiment tone to predict multi-week price drift.
