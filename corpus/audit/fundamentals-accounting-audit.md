# Audit — Fundamentals & Accounting Area

**Area path:** `content/fundamentals-accounting/`
**Corpus wishlist:** `corpus/fundamentals-accounting.md`
**Pattern reference:** `content/fundamentals-accounting/core-financial-ratios/`
**Audit date:** 2026-09-10
**Scope:** Completeness · Depth & Template · Coherence & Links · Math/Code verification

---

## 1. COMPLETENESS

The corpus wishlist defines **9 topics**; the repo implements **8 folders**. One topic is folded in.

| Corpus topic | Folder | Status |
|---|---|---|
| financial-statements-accounting | `financial-statements-and-accounting/` | ✅ Covered (renamed to add "and") |
| **financial-statement-analysis** | — | ⚠️ **No dedicated folder — folded in** |
| core-financial-ratios | `core-financial-ratios/` | ✅ Covered |
| equity-valuation | `equity-valuation/` | ✅ Covered |
| fundamental-analysis-and-screening | `fundamental-analysis-and-screening/` | ✅ Covered |
| capital-structure-and-corporate-finance | `capital-structure-and-corporate-finance/` | ✅ Covered |
| accounting-quality-and-red-flags | `accounting-quality-and-red-flags/` | ✅ Covered |
| quantitative-fundamental-investing | `quantitative-fundamental-investing/` | ✅ Covered |
| data-sources-and-corporate-data | `data-sources-and-corporate-data/` | ✅ Covered |

**No topics are truly missing** — the 8 folders map 1:1 onto the corpus scope. **No overlap** between folders was found; boundaries are clean (statements → ratios → valuation → screens → quality → corporate finance → factors → data). The one judgment call is the **financial-statement-analysis fold**:

**Assessment: fold is defensible but incomplete in linkage.** The corpus calls financial-statement-analysis "the analytical core of the whole area" and "the spine" (Penman FSA). In the repo, its content is **distributed, not consolidated**: the Palepu–Healy strategy→accounting→financial→prospective workflow, common-size, and GAAP/IFRS live in `financial-statements-and-accounting/06-advanced-extensions`; ratio decomposition/DuPont in `core-financial-ratios/02` & `04`; earnings quality in `accounting-quality-and-red-flags`. The distribution is reasonable, but **12 wikilinks across 4 folders still target a nonexistent `financial-statement-analysis/index` node** (see §3), i.e. the graph pretends the topic exists while no hub does. This is the single largest coherence defect. Resolution: either (a) re-point those links to `financial-statements-and-accounting/06-advanced-extensions` (+ `core-financial-ratios/02`) as the "statement analysis" entry, or (b) promote a dedicated analysis hub. Recommend (a).

---

## 2. DEPTH & TEMPLATE

**Total pages: 56** (8 folders × [index.md + 6 sub-pages 01–06]).

Every page was checked for the locked template: (a) YAML frontmatter with **first tag `fundamentals-accounting`**, (b) a `**Basic Prerequisites:**` line, (c) **6 numbered sections** (1. Intuition & Practical Objective, 2. Mathematical Ground Truth, 3. Computational Implementation, 4. Failure Modes & First-Principles Breakdowns, 5. Canonical Literature & Study References, 6. Connected Graph Bridges), (d) a **Python code block**, (e) a **claimed output block**.

**Template pass: 56 / 56 (100%).**

- All 56 pages: frontmatter present, first tag `fundamentals-accounting` ✓
- All 56 pages: `Basic Prerequisites:` line present ✓
- All 56 pages: sections `### 1.` … `### 6.` present and numbered 1–6 ✓ (section-2 titles vary slightly by design — "…& Derivations", "…& Lookup Table", "…— the accounting identities" — all consistent with the template's *section* contract)
- All 56 pages: ≥1 ```` ```python ```` block ✓ and ≥1 output block ✓

**Depth rating: High, with consistent audience arc.** Every folder runs the same 01→06 ladder: `01-from-zero-intuition` (zero prior knowledge) → mid-tier computational/mechanical pages → `05-failure-modes-and-practice` → `06-advanced-extensions`. Each `index.md` carries an explicit "audience arc" and "recommended reading route" for absolute-beginner / intermediate / expert. Code is consistently **stdlib-only** (no external deps), so every block is reproducible as-is. Canonical literature is cited per-page with chapter-level pointers (Penman ch/eq, Altman, Piotroski, Beneish, Sloan, Fama–French), grounding the corpus acquisitions. No page is a stub; depth is uniform across all 8 folders.

Minor note: the data-sources folder's code blocks are more reference/pipeline-oriented (XBRL tag mapping, bias measurement) than formula-driven — appropriate to a "data provenance" topic, not a defect.

---

## 3. COHERENCE & LINKS

**Area index (`content/fundamentals-accounting/index.md`) lists all 8 topics** ✓ with a two-track reading path (top-down for beginners: 1→2→3→4; bottom-up rigor for practitioners: 2→5→6→7→8) and cross-links to pillars 1, 5, 7 and Foundations. The 8 topics cohere around a single thesis (statements → signals → value → quality → financing → factors → data) stated in the hub intro.

**Wikilink scan:** 660 wikilinks in the area; **26 unresolvable (non-code)** broken links in two distinct classes:

**(A) 20 links to two stale/folded targets** (the real defect):
- **8× → `fundamentals-accounting/financial-statements-accounting/index`** — *old folder name* missing "and". Lives in: `core-financial-ratios/index` (×2), `core-financial-ratios/01-from-zero` (×2), `capital-structure-and-corporate-finance/index` (×2), `capital-structure-and-corporate-finance/01-from-zero` (×2). → Repoint to `financial-statements-and-accounting/index`.
- **12× → `fundamentals-accounting/financial-statement-analysis/index`** — the **folded topic** that has no folder. Lives in: `core-financial-ratios/index` (×2), `core-financial-ratios/01` (×1), `core-financial-ratios/02` (×1), `core-financial-ratios/03` (×1), `financial-statements-and-accounting/index` (×1), `…/02` (×1), `…/06` (×1), `fundamental-analysis-and-screening/index` (×1), `fundamental-analysis-and-screening/04` (×2), `accounting-quality-and-red-flags/index` (×1). → Repoint to the fold target (§1).

**Notably, the *pattern reference* folder (`core-financial-ratios/index.md`) is itself the worst offender** — its prerequisites line (L10) and graph-bridge section (L139) carry both broken targets.

**(B) 6 links with a stray `\` before `]]`** inside table cells, making the target carry a trailing backslash and fail to resolve:
- `data-sources-and-corporate-data/06-advanced-extensions.md` (×4: 01, 02, 03, 05), `…/01-from-zero` (×1: 02), `…/03-commercial-providers` (×1: 02). → Remove the `\`.

All **cross-pillar and cross-area links resolve** (pillars/01, /05, /07, foundations) — the broken set is confined to intra-area stale targets. **Recommendation:** batch-fix (A)+(B) in one pass; both are mechanical.

---

## 4. MATH / CODE VERIFICATION

**9 Python blocks executed (stdlib) across 7 folders; 9/9 produced output exactly matching the claimed block in the page.**

| Folder / page | Verifies | Result |
|---|---|---|
| `financial-statements-and-accounting/index` | Accounting identity **A = L + E** (double-entry ledger) | ✅ Assets 15,800 = Liab 5,000 + Equity 10,800 |
| `core-financial-ratios/index` | **ROIC**, ROE/ROCE decomposition, **Altman Z**, P/E×EY=1 | ✅ Z=5.78, ROE==ROCE, P/E×EY=1.0000 |
| `core-financial-ratios/06-advanced-extensions` | Altman Z + **Piotroski F-score** (9 signals) | ✅ Z=5.78 safe; F-score 7/9 |
| `equity-valuation/03-cost-of-capital` | **WACC**, levered beta, k_e | ✅ WACC 0.1560; deleveraging ladder |
| `equity-valuation/04-terminal-value-and-ev-to-equity` | **DCF** (explicit + terminal value), EV→equity | ✅ V_op 2001.9, TV=74.6% of value |
| `capital-structure-and-corporate-finance/02-modigliani-miller` | **MM Prop I & II**, flat WACC, home-made-leverage arbitrage, tax shield | ✅ flat WACC 10%; V_L=V_U+τD |
| `accounting-quality-and-red-flags/06-advanced-extensions` | **Beneish M-score** (8 vars), threshold −1.78 | ✅ Redwing −1.73 flagged; Northstar −2.68 not |
| `quantitative-fundamental-investing/04-quality-and-fscores` | F-score screen + value/quality premium | ✅ HIGH-F avg 17.00% vs LOW-F 8.75% |

**Formula spot-checks against sources — all correct:**
- **A = L + E** ✓ (Penman eq 2.1); articulation CFO+CFI+CFF=Δcash ✓
- **ROIC = NOPAT / avg Invested Capital** ✓ (119/510 = 23.33%)
- **WACC = w_d·k_d(1−τ) + w_e·k_e** ✓; CAPM k_e ✓
- **Altman Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5**, X4 = MV/total liabilities, decimal-fraction inputs — weights and threshold (>2.99 safe, <1.81 distress) match the 1968 paper ✓
- **MM**: Prop I value irrelevance, Prop II rE = rU + (D/E)(rU−rD) with flat WACC; with tax V_L = V_U + τD ✓
- **Piotroski F-score**: 9 binary signals (ROA, CFO, ΔROA, Accrual, ΔMargin, ΔTurnover, ΔLeverage, ΔLiquidity, EQ-offer), sum 0–9 ✓
- **Beneish M**: 8 ratios (DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA), M > −1.78 → likely manipulator ✓

**No math/code errors found.** Every executed block reproduced the claimed output byte-for-byte.

---

## 5. SUMMARY OF FINDINGS

**Verdict: PASS with minor-link-fixes required.**

- **Completeness:** 8/8 folders cover the 9 corpus topics; financial-statement-analysis folded into `financial-statements-and-accounting` — fold is reasonable in content distribution but leaves 12 dangling links to the nonexistent node.
- **Template:** 56/56 pages pass (first tag `fundamentals-accounting`, prerequisites, 6 sections, Python + output).
- **Coherence:** area index lists all 8 with a reading path; topics cohere. **26 broken/unresolvable wikilinks** (8 stale old-name, 12 folded-topic, 6 stray-backslash) — all intra-area, all mechanical to fix.
- **Math/Code:** 9/9 executed blocks match claimed output; all 8 spot-check formulas correct. No errors.

**Actions required (all mechanical):**
1. Repoint 8× `financial-statements-accounting/index` → `financial-statements-and-accounting/index`.
2. Repoint 12× `financial-statement-analysis/index` → the fold target (`financial-statements-and-accounting/06-advanced-extensions` and/or `core-financial-ratios/02`), or add a dedicated analysis hub.
3. Remove stray `\` in 6 data-sources table-cell wikilinks.
