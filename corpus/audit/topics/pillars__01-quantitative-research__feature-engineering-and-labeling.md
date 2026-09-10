# Audit Report — content/pillars/01-quantitative-research/feature-engineering-and-labeling/

**Reviewer:** sole adversarial reviewer (subagent)
**Scope:** 7 files (index.md + 01–06). `content/_legacy/` ignored.
**Date:** 2026-09-10

## Summary

| File | Code blocks | Output fence matches | Math | Spelling |
|---|---|---|---|---|
| index.md | 1 | ✅ | 1 coherence issue | clean |
| 01-from-zero-intuition.md | 1 | ✅ | **1 error** | clean |
| 02-feature-construction.md | 1 | ✅ | ✅ | clean |
| 03-target-labeling.md | 1 | ✅ | ✅ | clean |
| 04-triple-barrier-and-meta-labeling.md | 1 | ✅ | ✅ | clean |
| 05-failure-modes-and-practice.md | 1 | ✅ | ✅ | clean |
| 06-advanced-extensions.md | 1 | ✅ | ✅ | clean |

**Verdict: FAIL** — 1 substantive math/coherence error (page 01 worked example) + 1 minor coherence issue (index lookup table).

---

## 1. Spelling / typo scan (prose only, code & LaTeX excluded)

Ran a full dictionary-based scan on prose tokens (code fences, `$..$`/`$$..$$` math, and `[[wikilinks]]` stripped). **No misspellings or typos found.** House style (`[[full/path|Alias]]`, `$..$`, `$$..$$`, `§`, en-dashes) applied consistently throughout.

---

## 2. Math verification

### Worked example error — page 01, line 44 (**ERROR**)

- **Stated:** "the fixed-horizon label says 'held, ended down'; the triple-barrier label says 'stopped out at −4.5%'."
- **Correct / the printed example (§3, lines 94–98):** the reproducible example is `fixed-horizon=-1, triple-barrier=+1`. The path rises to `max=106.21`, breaching the **upper** (profit-taking) barrier `104.47`, so the triple-barrier label is **+1** = *took profit at **+4.5%*** (upper touched first). The narrative describes the triple-barrier label as `−1` ("stopped out at **−4.5%**", lower barrier first), which is the *opposite* outcome, and would in fact *agree* with the fixed-horizon `−1` (both down) — contradicting the sentence's own claim that they "disagree."
- **Correct statement:** "...the triple-barrier label says 'took profit at +4.5%'." (Sign and barrier action both wrong; magnitude ±4.47% ≈ 4.5% is consistent with the printed `upper=104.47 / lower=95.53`.)

### fracdiff weights (index 41, 01 48, 06 33–35) — VERIFIED ✅
- Recursion `w_0=1, w_k=-w_{k-1}(d-k+1)/k` reproduces the binomial series. For `d=1` gives `{1,-1,0,0,0}` (pure first difference); `d=0.3` gives decaying `{1,-0.3,-0.105,-0.0595,...}`. Matches LdP eq. 5.3–5.5. FFD `ℓ*` definition correct.
- Binomial expansion `(1-B)^d=Σ(-1)^k C(d,k) B^k` stated correctly.

### Triple-barrier boundaries (index 36–37, 03 33–40) — VERIFIED ✅
- Upper `P(1+pt·σ)`, lower `P(1−sl·σ)`, vertical `t_0+h`; `t_{i,1}=min(t_0+h, inf{...})`; label convention (+1 upper 1st / −1 lower 1st / `sgn(return)` on vertical) all correct and consistent across pages.
- The §3 printed example boundary math reproduces exactly: `0.5·0.02·√20=4.47%` → upper 104.47, lower 95.53, max 106.21 > 104.47 ⇒ +1. (The code path and output fence both MATCH.)

### Meta-label precision/recall/F1 (index 38, 04 39–41, 04 §3) — VERIFIED ✅
- Precision/Recall/F1 formulas correct. Code block output MATCHES documented fence exactly (primary P=0.517/R=1.000/F1=0.682; thr 0.5 → P=0.721/R=0.653/F1=0.686; thr 0.7 → P=0.829/R=0.322). Independent F1 recomputation confirms `2·0.517·1.0/1.517=0.682`. Meta-label definition `y^meta=1[s_i r_{i,1}>0]` matches LdP §3.6.

### Concurrency / average uniqueness (index 39–40, 05 46, 06 44–46) — VERIFIED ✅
- `c_t`, `ū_i`, effective-N definitions correct and consistent across all three pages; formulas match LdP Ch 4. Worked numbers (index: N=407.6/1450, 3.6×; page 05: 9.2/500, 54.5×) reproduced exactly by code runs.

### Sample-weight loss (06 48–50) — VERIFIED ✅
- Weighted cross-entropy `L=-Σ w_i[y ln p̂ + (1-y)ln(1-p̂)]` correct.

### ESL / Tsay citation check against corpus/verified
- ESL eq. 2.43 (basis expansion `f=Σθ_m h_m`), eq. 2.17 (additive), eq. 5.1, eq. 5.3 (truncated-power cubic spline basis), eq. 5.16 (`df_λ=trace(S_λ)`, λ-dependent), eq. 14.49/14.50/14.54 (PCA model / reconstruction-min / SVD) — **all confirmed present and correctly numbered** in `corpus/verified/esl_*.md`.
- Natural cubic spline df claim (02 38): cubic spline with K interior knots = K+4 params; natural spline = K df (frees 4 df) — **matches the corpus correction exactly** (the corpus itself flags the "K+3" garbling; this folder uses the corrected K+4/K form). ✅
- Tsay eq. 9.1–9.4 (factor model), §9.4.1 variance share `λ_i/Σλ_j`, BARRA eq. 9.7–9.8 — **all confirmed** in `corpus/verified/tsay_ch7-9.md`.

---

## 3. Code verification — all blocks RUN and DIFFED

All 7 `python` blocks extracted, executed with `python3` (exit 0), and diffed (normalized) against their documented output fences. **All 7 MATCH.**

| File | Block | Result |
|---|---|---|
| 01 | fixed-horizon vs triple-barrier disagreement | ✅ 19.7%, example path reproduced |
| 02 | spline-basis R² comparison | ✅ 0.332 / 0.830 / 0.915 |
| 03 | EWMA-vol triple-barrier | ✅ 49.9/50.1%, mean σ=0.0201, first-20 labels |
| 04 | meta-labeling precision/recall | ✅ 0.517→0.721, slope +1.174 |
| 05 | overlap + look-ahead barrier width | ✅ 9.2/500, 54.5×; 1.8% disagree |
| 06 | d* search + memory corr | ✅ d*≈0.2–0.3, corr table |
| index | fracdiff + triple-barrier + uniqueness | ✅ d*=0.3, 660/790, 407.6 |

Note: index §3 and page 06 §3 use different RNG streams (index builds `level` from seed 42 directly; page 06 first consumes seed 42 building `prices`, so its `level` differs), hence slightly different DF stats (index d=0.3→−6.46; page 06 d=0.2→−2.87 pass). Both are self-consistent with their own code/output fences; the minor d* discrepancy (index reports 0.3, page 06 0.2–0.3) is a deliberate two-simulation illustration, not an error.

---

## 4. Coherence / links / jargon

- **Wikilink integrity:** 69 links (after stripping aliases and excluding code fences) — **0 broken**; every target resolves to a `.md` or `index.md`.
- **Hub ↔ page-01 prereq:** index.md explicitly notes page 01 has smaller entry requirements than pages 02–06; page 01's stated prereqs (Probability & Measure Theory, no ML) match. ✅
- **Jargon consistency:** `t_{i,0}`/`t_{i,1}`, `pt/sl`, `σ_t`, `ū_i`, `c_t`, `ℓ*`, `d*` used consistently across all files. Triple-barrier label convention identical everywhere. ✅
- **Barrier-config taxonomy** (03 42): `[pt,sl,t1]` with the eight cases, `[1,1,1]`/`[0,1,1]`/`[1,1,0]` useful, `[0,1,0]`/`[0,0,0]` illogical — matches LdP §3.4. ✅
- **Minor coherence issue — index.md line 39 (table row "Concurrency").** The "Verified check" cell claims **"max c_t=61"**, and line 30 asserts "All formulas below were re-executed and reproduced numerically (see §3)." But the index's own §3 block uses `H=20, stride=1` (events 50..1499), which yields **max c_t = 16**, not 61. The value 61 originates from page 05's different configuration (`H=60`). So the index lookup table cites a "verified" number that its own §3 does not reproduce and that comes from a different simulation config. It is a *correct* folder-wide number (page 05 does output 61), so this is a coherence/attribution issue rather than a numerical error — the index should either print max c_t from its own run or label the source as page 05's config. **Minor.**

---

## Findings

1. **[ERROR — math/coherence] 01-from-zero-intuition.md:44** — Worked-example narrative contradicts the printed, reproducible example: text says triple-barrier label = "stopped out at −4.5%" (a −1 / lower-barrier outcome), but the §3 example (and reproduced run) is triple-barrier = **+1**, upper barrier touched first = "took profit at **+4.5%**". The stated pair would also *agree* (both −1), contradicting the sentence's "disagree" claim. Fix the sign/action (should be +4.5%, profit-take).
2. **[MINOR — coherence] index.md:39** — Lookup-table "Verified check" cites `max c_t=61` which its own §3 (H=20, stride 1) cannot reproduce (that config gives max 16); 61 is page 05's (H=60) number. Re-run/print c_t in index §3 or attribute the 61 to page 05's config.

All 7 code blocks pass; all references verified; no spelling issues; no broken links.
