# Pillar 7 Audit — Machine Learning & Alternative Data

**Pillar dir:** `content/pillars/07-machine-learning-altdata/`
**Audited:** 2026-09-10 · auditor: subagent
**Reference pattern:** `content/pillars/03-derivative-pricing/black-scholes-merton/`
**Corpus grounding:** `corpus/pillar7-machine-learning.md`, `corpus/titles/pillar7-machine-learning.TITLES.md`, `corpus/verified/`

**Verdict: PASS (with 2 minor documentation defects, no math or code errors).**

Scope audited: 9 topic-folders × (1 hub + 6 sub-pages) = **63 pages**, plus the pillar `index.md` hub and 6 legacy flat notes.

---

## 1. Completeness

### 1.1 The 9 folders vs. the corpus sub-topics

The corpus wishlist defines **10** sub-topic sections plus "Platforms & Tools". Mapping:

| Corpus sub-topic (`corpus/pillar7-…md`) | Realized in | Status |
|---|---|---|
| general ML foundations (ESL, Tsay) `[FOUND]` | Foundations pillar | by design |
| `financial-ml-pitfalls-and-low-snr` | `financial-ml-pitfalls-and-low-snr/` | ✅ covered |
| `purged-cross-validation-and-backtest-hygiene` | `purged-cross-validation-and-backtest-hygiene/` | ✅ covered |
| `tree-and-boosting-methods` | `tree-and-boosting-methods/` | ✅ covered |
| `feature-engineering-and-meta-labeling` | **Pillar 1** `feature-engineering-and-labeling/` | ⚠️ no Pillar-7 folder (cross-pillar) |
| `financial-nlp-and-transcripts` | `financial-nlp-and-transcripts/` | ✅ covered |
| `alternative-data-pipelines` | `alternative-data-pipelines-and-evaluation/` | ✅ covered |
| `regime-classification-hmm-gmm` | `regime-classification-hmm-and-gmm/` | ✅ covered |
| `deep-learning-for-sequences` | `deep-learning-for-sequences/` | ✅ covered |
| `reinforcement-learning-for-trading` | `reinforcement-learning-for-trading/` | ✅ covered |
| `ml-for-portfolio` | `ml-for-portfolio/` | ✅ covered |
| Platforms & Tools (Microsoft Qlib) | referenced on 4+ pages | ⚠️ no dedicated page |

**No corpus sub-topic is wholly absent.** The one deliberate omission is
`feature-engineering-and-meta-labeling` (triple-barrier labeling, fractional
differentiation, meta-labeling, bet sizing), which per the corpus *scope note*
(line 15) is non-financial-ML-specific and belongs to Pillar 1. It lives in
`content/pillars/01-quantitative-research/feature-engineering-and-labeling/`
and is **reciprocally cross-linked** (P7 purged-CV/03 and pitfalls/04,06 route
there; P1 index/04/05/06 route back to P7). Fractional differentiation still gets
its own derivation + code on `financial-ml-pitfalls-and-low-snr/04` and `/06`.

### 1.2 Overlap / coherence of the 9 folders

Coherence is **explicit and documented**, not accidental:

- **vs. Pillar 1 `feature-engineering-and-labeling`** — the meta-labeling /
  triple-barrier / fractional-differentiation material is owned by P1 and
  consumed by P7 (tags: "the labels being purged come from …"). No duplication.
- **vs. Pillar 1 `regime-detection`** — P7 `regime-classification-hmm-and-gmm`
  declares itself the **"machine-learning view"** and P1 `regime-detection` the
  **"econometric twin (Hamilton-filter view)"**, with two-way links on 8+ pages
  and an explicit "do NOT duplicate" note (`regime-classification-hmm-and-gmm/index.md:130`).
- **vs. Pillar 1 `backtesting-hygiene`** — P7 owns purged/embargoed CV & CPCV;
  P1 owns the Deflated Sharpe / PBO. P7's DSR references hand off cleanly.
- The internal arc is sound: folder 1–2 (evaluation machinery) → 3 (workhorse
  trees) → 4–5 (unstructured signals) → 6–8 (advanced) → 9 (portfolio). The hub
  states this and the "Reading Path" reproduces it in 5 stages.

### 1.3 Hub completeness

`index.md` lists **all 9** folders (numbered) **and** a 5-stage Reading Path,
plus a mermaid production-pipeline diagram and an "Original Notes" section
linking the 6 legacy flat notes. ✅

---

## 2. Depth & Template

**Template = frontmatter (title + tags, FIRST tag `pillar-machine-learning`) +
`**Basic Prerequisites:**` line + sections `### 1.`…`### 6.`**

| Check | Result |
|---|---|
| Pages scanned | **63** (9 folders × 7 files) |
| frontmatter title present | 63/63 |
| tags present | 63/63 |
| **first tag = `pillar-machine-learning`** | **63/63** |
| `Basic Prerequisites` line present | 63/63 |
| sections `### 1.`–`### 6.` all present | 63/63 |
| **TEMPLATE PASS** | **63/63** |

No page fails. Within every folder the 7 files are `index.md` + the six
locked slots `01-from-zero-intuition … 06-advanced-extensions` (folder-specific
titles on 02–04), exactly mirroring the BSM reference folder.

**Depth.** Page sizes 7.4k–14.2k chars (median ≈10.7k); per-folder totals
58.6k–84.6k chars. Every page carries a runnable code block with a pasted
expected output, and §5 anchors to a specific corpus chapter/paper. This is
deep, research-grade prose, not stubs.

**Audience arc.** Consistent across all folders: `01` = zero-prior intuition,
`02–04` = the derivations + implementation, `05` = failure modes, `06` = advanced
extensions. The five-stage hub Reading Path stages the arc at the pillar level.

**Minor tag note (not a template failure):** the pillar hub `index.md` and the 6
legacy flat notes use the pillar tag `pillar-ml-altdata`, whereas the 63 topic
pages use `pillar-machine-learning`. The two tag vocabularies coexist. The
stated locked template applies to the *pages*, which all pass; worth unifying
the hub/flat-note tag for graph consistency.

---

## 3. Coherence & Links

- **Wikilink resolution:** **859** `[[…]]` wikilinks across the pillar
  (`content/pillars/07-machine-learning-altdata/**/*.md`). **0 genuinely broken.**
  All 859 resolve to an existing page (folder `index` or file).
- **Non-canonical link style (10 links — hardening, not breakage).** Ten links
  use the `[[ path ]]` form (a leading *and* trailing space inside the brackets)
  and target a bare **folder name with no `/index`**:
  - `[[ pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene ]]`
    → `financial-nlp-and-transcripts/05`, `regime-classification-hmm-and-gmm/05`,
    `/06`, `/index` (4×)
  - `[[ pillars/07-machine-learning-altdata/financial-nlp-and-transcripts ]]`
    → `deep-learning-for-sequences/03`, `/06` (2×)
  - `[[ pillars/05-portfolio-optimization/constraints-and-transaction-costs ]]`
    → `reinforcement-learning-for-trading/04`, `/05`, `/06`, `/index` (4×)
  They resolve only because Obsidian trims the whitespace and falls back
  `folder → folder/index`. Under a strict filename resolver (no trim, no
  folder→index fallback) all 10 dangle. Every other link in the pillar uses the
  canonical `[[path/subpage|label]]`, `[[path/index|label]]`, or `[[flat-note|label]]`
  form (no spaces, explicit `/index`), so these 10 are outliers. **Recommend:**
  normalize to `[[pillars/07-machine-learning-altdata/<folder>/index]]` (add
  `/index`, drop the spaces) for consistency and strict-resolver safety.
  Confirmed by a strict filesystem-map walk over all 859 targets (16 flagged; 6
  are the `[[t_{i,0},t_{i,1}]]` math-interval artifacts below, 10 are this class).
- **Apparent "broken" links are a math-notation artifact, not links:** six
  occurrences of the interval notation `[[t_{i,0},t_{i,1}]]` inside `$…$`
  (double square brackets). Obsidian/Katex renders the inner `[…]` literally, so
  `f[[t_{j,0},t_{j,1}]]` prints as `f[[t_{j,0},t_{j,1}]]` instead of `f[t_{j,0},t_{j,1}]`,
  and a wikilink-aware renderer may even try (and fail) to resolve it. Files:
  - `purged-cross-validation-and-backtest-hygiene/01-from-zero-intuition.md:44` (×2)
  - `purged-cross-validation-and-backtest-hygiene/03-purging-and-embargo.md:29,43` (×3)
  - `purged-cross-validation-and-backtest-hygiene/index.md:32` (×1)
  Fix: replace `[[…]]` with `[…\]` inside the math delimiters.
- **Hub completeness:** `index.md` lists all 9 folders + Reading Path + flat-note
  index (see §1.3).
- **Cross-pillar coherence:** strong and bidirectional (P1 backtesting-hygiene,
  feature-engineering-and-labeling, regime-detection; Foundations). No orphan pages.

---

## 4. Math & Code

### 4.1 Method
- Extracted **75** ```python blocks from the 63 pages. Performed **two runs**:
  (a) each block standalone; (b) all blocks of a page concatenated (notebook order),
  then compared programmatic stdout against the page's pasted expected-output block.
- Environment: python3, numpy 2.5.3, scipy 1.18.1 (sklearn/lightgbm/xgboost/torch/pandas **not** installed).

### 4.2 Result
| Metric | Value |
|---|---|
| Pages with embedded expected output | 63 |
| **Exact stdout match** | **61 / 63** |
| Mismatches | 2 (both in `financial-nlp-and-transcripts/`, documentation artifacts — see below) |
| Pages whose concatenated blocks error | 0/63 |
| Blocks with a genuine runtime error | 0 |
| Legacy flat notes needing absent libs | 3 (`pandas`/`sklearn`) — environment limitation, not code defects |

Two standalone blocks (`regime-classification-hmm-and-gmm/05-…` at file lines 94 &
112) are *sequential* snippets that reference functions/vars defined in an earlier
block of the same page ("continues from Experiment 1's em_gmm"). They run cleanly
when the page's blocks are concatenated in order — a notebook-style pattern, not an error.

### 4.3 Formula spot-checks (against the verified corpus)

| Formula / result | Page | Verdict |
|---|---|---|
| **Purging** — 3 overlap conditions + interval intersection `t_{i,0}≤t_{j,1} ∧ t_{j,0}≤t_{i,1}` | purged-CV/03 | ✅ correct (AFML §7.4.1) |
| **Embargo** — extend test label to `t_{j,1}+h`, `h≈0.01T` | purged-CV/03 | ✅ correct (AFML §7.4.2) |
| **Purge/embargo fold bookkeeping** (T=1000,h=20,k=5,emb=10 → 4.9% loss) | purged-CV/03 code | ✅ ran, output matches exactly |
| **CPCV splits** `C(N,k)` and **paths** `φ[N,k]=(k/N)C(N,k)=∏_{i=1}^{k-1}(N-i)/(k-1)!` | purged-CV/04 | ✅ algebra verified (φ=C(N-1,k-1)); code reproduces φ[6,2]=5, φ[20,10]=92378 |
| **CPCV variance** `σ²[μ]=φ⁻¹σ²[1+(φ-1)ρ̄]` | purged-CV/04,06 | ✅ correct (AFML §12.5); code matches |
| **Walk-forward avg-train** `(1/(T-t0))Σ(τ-1)` | purged-CV/06 | ✅ correct; output matches |
| **DSR** `Φ[(SR̂−SR0)√(n−1)/√(1−γ₃SR̂+((γ₄−1)/4)SR̂²)]`, `SR0=√(2 ln N)/√n` | pitfalls/06 | ✅ correct PSR/DSR form; `√(2 ln N)` is the standard asymptotic E[max] (page flags it `≈`; the exact Bailey–LdP E[max] with Euler–Mascheroni γ lives in Pillar 1 `backtesting-hygiene/04`) |
| **IC / rank-IC / ICIR / t** `IC_p=corr(x,y)`, `ICIR=IC̄/σ_IC`, `t=ICIR√P` | alt-data/04 | ✅ correct (Grinold–Kahn); code matches (ICIR=0.919, t=14.59) |
| **IR = ICIR·√B_eff** / Fundamental Law `IR=IC√B·TC` | alt-data/04 | ✅ correct |
| **Decay** `IC(h)=IC0 e^{−λh}`, `t_1/2=ln2/λ` | alt-data/04 | ✅ correct; fit recovers λ̂=0.1175 vs 0.12 |
| **EM** — ELBO/Jensen, `Q(θ;θ_old)`, monotone `ℓ(θ_new)≥ℓ(θ_old)`, GMM updates `π_k,μ_k,Σ_k` | regime/03 | ✅ correct (ESL 14.61–64); code confirms monotone, matches |
| **HMM forward–backward** α/β recursions, γ/ξ, Baum–Welch `A_{ij}`, Viterbi δ | regime/04 | ✅ correct (Rabiner 1989); code matches (Viterbi 95.8% agreement) |
| **LSTM gates** f/i/C̃/C/o + CEC `∂C_T/∂C_t=∏f_s`; RNN vanishing `∏diag(1−h²)W`, `≤‖W‖^T` | deep-learning/02 | ✅ correct (Hochreiter–Schmidhuber); code matches |
| **Attention** `softmax(QKᵀ/√d_k + M)V`, causal mask, multi-head | deep-learning/03 | ✅ correct (Vaswani 2017); code matches (causal upper-triangle exactly 0) |
| **Fractional differentiation** `w_k=(−1)^k C(d,k)`, `C(d,k)=∏(d−i+1)/i`, `X_t^(d)=Σ w_k X_{t−k}` | pitfalls/04,06 | ✅ correct (AFML Ch. 5) |
| **MDI / MDA / SFI** `MDI_ℓ=(1/M)ΣΣî²·1(v(t)=ℓ)`, `MDA_j=Score_OOS−Score_{OOS,π_j}` | tree/06 | ✅ correct (ESL 10.42; AFML §8.3) |
| **Model averaging / stacking** `f̂=Σw_k f̂_k` | tree/06 | ✅ correct (ESL 8.8) |

### 4.4 Defects found

1. **Wrong pasted output — `financial-nlp-and-transcripts/02-bag-of-words-and-lm-dictionary.md:95`.**
   The "guidance" row of the TF-IDF matrix is transcribed with the `0.137` under
   column `d0` and `0.000` under `d1`. The token "guidance" occurs in **document 1**,
   so the correct row is `guidance  1.916  0.000  0.137  0.000  0.000`
   (verified by executing the page's own code). The *code and math are correct*;
   only the embedded snapshot is mis-transcribed. (`demand`, also in doc1, is
   pasted correctly as `0.000 0.137 …`, so the row was simply swapped by hand.)
2. **Stylized (non-literal) output — `financial-nlp-and-transcripts/04-embeddings-and-transformers.md`.**
   The pasted block is a hand-edited *excerpt*: it truncates the vocabulary list
   with a literal `...  (...)`, reorders rows (semantic grouping rather than the
   program's alphabetical print), and drops inter-column spacing. Every floated
   **value is correct** (`cos(earnings,revenue)=0.347`, `cos(beat,missed)=1.000`,
   `cos(guidance,outlook)=0.842`, `cos(costs,margins)=0.999`, `cos(guidance,earnings)=0.383`),
   so this is a presentation choice, not a math error — but it is not a
   reproducible verbatim run and is worth aligning for consistency with the other 61 pages.

No wrong formulas, no incorrect derivations, and no non-running code were found.

---

## Summary

- **Completeness:** 9 folders cover 9 of the corpus's 10 sub-topics; the 10th
  (`feature-engineering-and-meta-labeling`) is deliberately housed in Pillar 1
  and bidirectionally cross-linked. Qlib "Platforms & Tools" is referenced but
  has no dedicated page. Overlaps with Pillar 1 are handled explicitly and cleanly.
- **Template:** **63/63 pages pass** the locked template (title, first tag
  `pillar-machine-learning`, Basic Prerequisites, §§1–6).
- **Coherence/links:** 859 wikilinks, **0 genuinely broken** (hub lists all 9 +
  reading path). Two cosmetic items: 10 links use non-canonical `[[ path ]]`
  spacing + bare-folder targets (resolve only via Obsidian's folder→index
  fallback — normalize to `/index`), and 6 `[[t_{i,0},t_{i,1}]]` interval
  notations that may render/resolve as a wikilink (use single brackets).
- **Math/code:** 61/63 pages reproduce their pasted output **exactly**; 2 NLP
  pages have output-transcription issues (1 wrong cell; 1 hand-edited excerpt).
  All spot-checked formulas (purge/embargo, CPCV paths & variance, DSR, IC/ICIR,
  IR, EM/GMM, HMM forward–backward, LSTM gates, attention, fracdiff, MDI/MDA)
  are correct and every code block runs.
