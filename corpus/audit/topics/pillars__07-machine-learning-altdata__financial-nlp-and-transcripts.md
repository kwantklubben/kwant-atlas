# Audit — `pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/`

**Target:** 7 files (index.md, 01–06). **Date:** 2026-09-11.
**Method:** read all 7 files; executed every ```python block with Python 3.13 (numpy present) and diffed stdout against each file's printed output fence; independently recomputed the math identities and worked-example numbers; validated all 16 unique wikilinks resolve to existing `.md` files.

## Verdict: PASS (0 hard errors, 2 minor observations)

---

## 1. Spelling / typography (prose only)

No misspellings, doubled-letter errors, or broken words found in prose across all 7 files. Domain terms used correctly: *evasiveness, obfuscation, rarefaction, miscalibrated, writedowns, neg-fraction, point-in-time*. Dashes (en/em) and the `Loughran–McDonald` / `Cohen–Malloy–Nguyen` hyphenation are consistent.

## 2. Math — every boxed formula + worked example verified

| Formula / example | File:line | Verdict |
|---|---|---|
| TF–IDF `(x/Σx)·(log((N+1)/(df+1))+1)` | index.md:37, 02:32 | Correct (smooth-idf, matches sklearn `TfidfTransformer`) |
| TF–IDF worked matrix (doc0=0.160 impairment, doc1=0.137 demand, doc2=0.128 liability, idf=1.916 for all df=1 terms) | 02:92–110 | **Recomputed by hand and by run — exact** |
| LM-neg-proportion doc0/1/2/3 = 0.333/0.000/0.067/0.333 | 02:105–110 | Correct (4/12, 0/14, 1/15, 4/12) |
| Cosine similarity | index:41, 02:38 | Standard, correct |
| Net tone `(pos−neg)/total` + neg-frac | index:45, 01:40, 03:32 | Correct |
| tone worked values +0.429…−0.286 | index:99, 03:105–111 | Correct (recomputed per doc) |
| OLS tone→return `y=0.110+14.244·tone, R²=0.790` | index:55/100, 03:113 | Correct (lstsq run + manual) |
| β₁/β₀ closed form (centered) | 03:42 | Correct |
| Fog index `0.4(words/sent + 100·complex/words)` | 03:48 | Correct Gunning–Fog |
| PPMI `max(0, log P(t,c)/P(t)P(c))` | 04:31 | Correct |
| Truncated SVD `v_t=(U_kΣ_k)_{t,:}` | 04:35 | Correct |
| Attention `softmax(QKᵀ/√d_k)·V` | 04:41 | Correct |
| Rank-2 embedding cosines (earnings–estimates 0.983, beat–missed 1.000, guidance–outlook 0.842, costs–margins 0.999) | 04:144–149 | **Exact vs run output**; top-2 singular values 8.103/7.584, var 0.216 — exact |
| ExecTone word-weighted average | 06:33 | Correct; run gives −0.032, exact |
| prepared/Q&A mean tone +0.156/−0.075 | 06:120 | Exact vs run |
| Cross-section OLS `y=−0.150+10.797·tone, R²=0.989` | 06:122 | Exact vs run |
| ΔText = 1−cos(v_t, v_{t−1}) | 06:49 | Correct (Lazy Prices) |

No wrong formula, sign, or constant found.

## 3. Code — all 7 blocks executed

- `index.md` block (design-matrix `lstsq`) → stdout matches fence exactly.
- `01` count demo → **bull net=+7 / 0.292, bear net=−7 / −0.304** — exact.
- `02` TF–IDF + LM proportions → exact (full 10-row matrix).
- `03` sentiment + manual normal-equations OLS → exact (b0=+0.110, b1=+14.244, R²=0.790).
- `04` PPMI–SVD embeddings → exact (all 34 vectors + 6 cosines + singular values).
- `05` n-gram overfitting (127 features, 16 docs) → exact; in-sample R²=1.000 at 30 features, leave-one-out −0.433. **Note:** at D=20 LOO jumps to −1.906 (negative), D=30 back to −0.433 — all leave-one-out values negative as the prose claims.
- `06` transcript pipeline + cross-section OLS → exact.

**7/7 blocks run and matched.** Each page is a single self-contained block; no cross-block chaining needed (each block redefines its own helpers).

## 4. Coherence

- Hub lists 6 sub-pages → all 6 files exist with matching titles/routes.
- Prereq chains are consistent and monotone (01→02→03→04→05, 03/04→06); each page's §6 "Back/Forward" links agree with the hub's route recommendations.
- All 16 unique wikilink targets resolve (verified against the repo tree). `fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition` (05:33) resolves.
- Hub §2 verified-check table reproduces the folder's run outputs exactly.
- Corpus refs named (`28_…`, `25_…`, `40_Dechow_2010`, `39_Healy_1999`) consistent with sibling audits; ESL `esl_ch11-18.md` and J&M verified files present in `corpus/verified/`.

## Minor observations (non-blocking)

1. **index.md:57** — the verified-check row reads "16 docs · 127 features: in-sample R²=1.000, leave-one-out R²=−0.433". The in-sample 1.000 and LOO −0.433 actually occur at the **30-feature** model (05:135); at the full 127-feature space in-sample is also 1.000 but LOO is *below* −0.433 (05's prose correctly scopes it to "30 of 127 features"). The hub conflates the two scopes. Cosmetic, not a wrong number — 05 itself is accurate.
2. **04:43 / 02:127** — Jurafsky & Martin 3rd-ed chapter citation for transformers/attention ("Ch 11") may be one off (attention/pretraining is Ch 10 in the 3rd ed.); Ch 6 for TF–IDF is correct. This is a citation nit, not a math error.

## Files
- Checked: 7
- Code blocks run: 7 (all matched)
- Errors found: 0 hard / 2 minor observations
