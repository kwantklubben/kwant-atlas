# Pillar 6 Audit — Market Making & Liquidity Provision

**Scope audited:** `content/pillars/06-market-making/` — 9 topic-folders × (index.md + 6 sub-pages) = **63 pages**, plus the pillar hub `index.md` and 6 legacy flat notes. Reference pattern: `03-derivative-pricing/black-scholes-merton/`. Corpus reference: `corpus/pillar6-market-making.md` + `corpus/titles/pillar6-market-making.TITLES.md`; verified sources in `corpus/verified/` (hasbrouck_*, foucault_*).

**Date:** 2026-09-10 · **Verifier:** subagent audit · **Pillars audited against:** Pillar 2 (`02-algorithmic-hft`) and Pillar 4 (`04-quantitative-risk`).

---

## 1. COMPLETENESS

### 1.1 Corpus coverage vs built folders

The corpus explicitly plans **ten** sub-topic folders (`corpus/pillar6-market-making.md` §intro: *"Entries are mapped to the ten planned sub-topic folders"*). Nine are built:

| Corpus sub-topic | Built folder | Status |
|---|---|---|
| limit-order-book-mechanics | `limit-order-book-mechanics` | ✅ |
| avellaneda-stoikov-and-optimal-quoting | `avellaneda-stoikov-and-optimal-quoting` | ✅ |
| adverse-selection-and-glosten-milgrom | `adverse-selection-and-glosten-milgrom` | ✅ |
| spread-decomposition-and-roll | `spread-decomposition-and-roll-model` | ✅ |
| inventory-management-and-quote-skewing | `inventory-management-and-quote-skewing` | ✅ |
| toxic-order-flow-and-vpin | `toxic-order-flow-and-vpin` | ✅ |
| market-impact-and-depth | `market-impact-and-depth` | ✅ |
| liquidity-risk-and-asset-pricing | `liquidity-risk-and-asset-pricing` | ✅ |
| market-maker-economics-and-rebates | `market-maker-economics-and-rebates` | ✅ |
| **dealer-banks-and-otc** | **— MISSING —** | ❌ |

**Missing topic: `dealer-banks-and-otc`.** The corpus devotes a full section (`pillar6-market-making.md` §"dealer-banks-and-otc", lines 362–387) to OTC/dealer markets:
- Duffie, Gârleanu & Pedersen (2005), *Over-the-Counter Markets* (Econometrica 73(6)) — **[★ P] priority** anchor.
- Duffie (2012), *Dark Markets* — capstone book.
- Duffie (2010), *Slow-moving capital* — presidential-address bridge.
- Cross-lists: Bao–Pan–Wang (2011) corporate-bond illiquidity; Stoll (1978) / Ho–Stoll (1981); Hendershott–Menkveld (2014).

Duffie–Gârleanu–Pedersen 2005 is on the corpus's top-12 priority list (#11). No folder (or flat note) covers the search-and-bargaining OTC model. This is the only corpus sub-topic with no built folder.

**Partial mitigations:** corporate-bond/OTC-adjacent content surfaces in `liquidity-risk-and-asset-pricing` (illiquidity measures, priced factor) and `market-maker-economics-and-rebates` (dealer economics, Stoll 1978), so the *spirit* of OTC dealer economics leaks in — but the dedicated search/bargaining model (Duffie–Gârleanu–Pedersen), the OTC price-discovery mechanism, and *Dark Markets* are absent.

### 1.2 Coherence of the 9-folder partition (no awkward overlap)

The 9 folders partition Pillar 6 cleanly, with a deliberate two-layer logic:
- **Why the spread exists** → adverse-selection (GM) / market-impact (Kyle) / spread-decomposition (Roll–HS).
- **How a maker optimizes** → limit-order-book mechanics → avellaneda-stoikov quoting → inventory/quote-skewing.
- **How flow is measured** → toxic-order-flow/VPIN.
- **Economics** → market-maker-economics/rebates → liquidity-risk/asset-pricing.

**Overlap vs Pillar 2 (`02-algorithmic-hft`):** `market-impact-and-depth` overlaps with Pillar 2's `optimal-execution-and-almgren-chriss` (Almgren–Chriss, Obizhaeva–Wang, Gatheral live in both). The corpus explicitly cross-lists these ("Almgren & Chriss (2000) is already cited by the Atlas across both pillars") and the pillar-6 pages **correctly bridge** to `pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss` rather than duplicating the execution math. Division of labour is sound: Pillar 6 owns the *impact/microstructure* concept, Pillar 2 owns the *execution* application. ✅ (Except the broken `pillars/02-execution/...` links below.)

**Overlap vs Pillar 4 (`04-quantitative-risk`):** `liquidity-risk-and-asset-pricing` touches Pillar 4's liquidity-risk territory; pages cross-link to `04-quantitative-risk/var-and-expected-shortfall` and `liquidity-risk-and-margin-spirals`. Pillar 6 keeps the *asset-pricing/measuring* angle, Pillar 4 the *risk-management* angle. Reasonable. ✅

### 1.3 Pillar hub index.md — STALE (completeness gap at hub level)

`content/pillars/06-market-making/index.md` was **not updated** for the 9-folder build. Findings:
- It lists only **6** topics; omits `market-impact-and-depth`, `liquidity-risk-and-asset-pricing`, and `market-maker-economics-and-rebates` entirely.
- Its 6 links point to the **legacy flat notes** (`limit-order-book-mechanics-and-l3`, `the-avellaneda-stoikov-model`, etc.), not the 9 folder indexes.
- It offers no reading path to the new folder structure.

So a reader entering via the pillar hub is routed to old flat notes and never sees 3 of the 9 folders. The 9 folder hubs themselves are complete (each routes to its 6 sub-pages with an audience arc — see §2), but the **pillar-level hub is out of date**.

---

## 2. DEPTH & TEMPLATE

### 2.1 Locked-template compliance — **63 / 63 PASS (0 fail)**

Every one of the 63 pages (9 folders × 7 files) carries the locked template:
- frontmatter `title:` + `tags:` with **first tag `pillar-market-making`** ✅
- `**Basic Prerequisites:**` line ✅
- sections `### 1.` … `### 6.` ✅

Programmatic scan (frontmatter regex + section regex across all 63 files): **63 pass, 0 fail.**

### 2.2 Frontmatter / YAML safety (quartz build)

- **0** of 63 frontmatter titles contain backslashes or invalid YAML escapes (this was an earlier build breaker — git log `01b69ea` fixed the `avellaneda-stoikov/04` case; audit confirms no residual instances).
- **0** of 63 frontmatters fail `yaml.safe_load` (strict parse). 

### 2.3 Depth

Page sizes: mean ≈ **10.1k chars** (min 6,999 · max 14,560). No thin/stub pages. Every folder ships a hub with a formula-lookup table, a `§3` computational engine with **executed, output-verified Python**, and a `§5` canonical-literature section. The AS and Kyle hubs are the standouts (full derivation + verified numerics + the paper's own table reproduced).

**Audience arc:** all 9 folder hubs carry a `### 6` "Recommended reading route" with three tiers — *absolute beginner* (01 From Zero) → *model + code, undergrad/job-seeking* (02→03→04) → *robustness, practitioner/graduate* (05→06). ✅ Consistent with the zero-to-near-professional audience in the corpus.

---

## 3. COHERENCE & LINKS

### 3.1 Wikilinks — 731 checked, **12 broken/dangling**

| # | File | Broken target | Cause / fix |
|---|---|---|---|
| 7 | `market-impact-and-depth/{01,02,03,04,05,06,index}.md` | `[[…limit-order-book-mechanics-and-l3/index]]` | Flat note is `limit-order-book-mechanics-and-l3.md` (no `/index`). Should be `[[…limit-order-book-mechanics/index]]` (the folder). |
| 4 | `market-impact-and-depth/{03,04,06,index}.md` | `[[pillars/02-execution/almgren-chriss/index]]` | Pillar 2 dir is `02-algorithmic-hft`, folder is `optimal-execution-and-almgren-chriss`. Should be `[[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index]]`. |
| 1 | `limit-order-book-mechanics/index.md` | `[[…limit-order-book-mechanics-and-l3\]]` | Trailing-backslash typo in the wikilink target. |

All 12 are concentrated in **two** folders (`market-impact-and-depth`, `limit-order-book-mechanics`); the other 7 folders have 0 broken links.

### 3.2 Stale-but-resolving legacy links (coherence, not breakage)

Many cross-folder links resolve only because the **legacy flat notes still exist** — e.g. `[[pillars/06-market-making/spread-decomposition-and-roll-model]]`, `[[…toxic-order-flow-and-vpin]]`, `[[…adverse-selection-and-glosten-milgrom]]`, `[[…inventory-management-and-quote-skewing]]` point to the old `.md` flat files, not the folder indexes. They are not dangling, but they (a) bypass the folder hubs and (b) are inconsistent with the folder-slug convention used elsewhere (`avellaneda-stoikov-and-optimal-quoting/index`, `limit-order-book-mechanics/index`). Recommend a pass that repoints cross-folder links to the folder `/index` hubs and retires the flat notes once nothing references them.

### 3.3 Hub completeness (per-folder)

Each of the 9 folder indexes lists all 6 sub-pages and a `### 6` Connected Graph Bridges + reading route (verified: route present in 9/9, `### 6` in 9/9, sub-page links 7–10 per hub). ✅ Folder-level linking is coherent; the defect is the **pillar-level** hub (§1.3).

---

## 4. MATH / CODE VERIFICATION

### 4.1 Executable code — all blocks run, outputs match

Across the 9 folders: **69 `python` blocks extracted. All 69 execute without error** (python3, numpy present). Of the 69: **66 outputs match** the documented expected output byte-for-byte (normalized); the remaining 3 are extraction artifacts on `spread-decomposition-and-roll-model/index.md`, where three code blocks share one combined output block — each block's individual output was re-run and matches its line of the combined block. **No non-running code and no numeric mismatch found.**

### 4.2 Formula spot-checks vs `corpus/verified/` (all correct)

| Model / result | Pillar-6 page | Verified reference | Verdict |
|---|---|---|---|
| AS reservation price `r = s − qγσ²(T−t)` | avellaneda-stoikov `index`/`03` | corpus line 106; AS(2008) | ✅ |
| AS total spread `ψ = γσ²(T−t) + (2/γ)ln(1+γ/k)` | avellaneda-stoikov `index` | AS eq 3.18; reproduces paper table 1.29/1.33/1.15 | ✅ |
| GM spread `A−B = 4(1−δ)δµ(V_H−V_L)/(1−(1−2δ)²µ²)`; δ=½ ⇒ `µ(V_H−V_L)` | adverse-selection `index`/`03` | Hasbrouck ch5 eq 5.7 | ✅ |
| Roll `c = √(−γ1)`, spread `2√(−γ1)` | spread-decomposition `03`/`index` | Hasbrouck ch3 | ✅ (0.04991 recovered) |
| PIN `= αµ/(αµ+2ε)` | toxic-flow `02` | Hasbrouck ch6 eq 6.4 | ✅ |
| EKOP Poisson-mixture likelihood + PIN MLE | toxic-flow `03` | Hasbrouck ch6 | ✅ |
| VPIN `= Σ\|V^S−V^B\|/(nV)` ≈ `αµ/(αµ+2ε)` | toxic-flow `04` | ELOP 2012 eq 9 | ✅ |
| Kyle `λ = ½√(Σ0/σu²)`, depth `1/λ`, `Var[v\|y]=Σ0/2`, conditional profit `(v−p0)²/2·√(σu²/Σ0)` | market-impact `02` | Hasbrouck ch7 eq 7.4/7.5 | ✅ (page even incorporates the verified ch7 conditional-vs-unconditional correction) |
| Huang–Stoll / Glosten–Harris `Δp_t = c(q_t−q_{t−1})+λq_t+u_t`, spread `2(c+λ)` | spread-decomposition `04` | Hasbrouck ch8 eq 8.2 | ✅ |
| Ho–Stoll reservation `r(I)=S̄−γσ²Iτ`, reservation spread `γσ²τ` | inventory `03` | Ho–Stoll 1981; matches AS reservation | ✅ |
| Amihud ILLIQ `(1/D)Σ\|R\|/VOLD` | liquidity-risk `02` | Amihud 2002; Hasbrouck ch9 | ✅ |
| Square-root law `I ≈ σY√(Q/V)`; temporary exp 3/5, permanent 1; Gatheral no-arb `δ≈γ≈0.5` | market-impact `04` | Almgren et al 2005; Gatheral 2010; Tóth 2011 | ✅ |

### 4.3 Minor observation (corpus transcription, not a pillar-page error)

`corpus/pillar6-market-making.md` line 106 transcribes the A–S half-spreads as `δ^a/b = (1/γ)ln(1+γ/κ) + ½σ²γ(T−t) ∓ ½qγσ²(T−t)`. The correct inventory coefficient (from the reservation formulation the pillar pages correctly use, and consistent with AS/GLFT) is `qγσ²(T−t)` — i.e. no `½`. The **pillar pages themselves are correct** (they use reservation `r = s − qγσ²τ` + `ψ/2`); this is a nuance in the *corpus* line, worth a one-word fix for future transcription reuse.

---

## 5. VERDICT

**PASS with minor gaps (one real completeness gap + 12 broken links in 2 folders + a stale pillar hub).**

| Dimension | Grade | Summary |
|---|---|---|
| Completeness | ⚠️ | 9/10 corpus sub-topics built; **`dealer-banks-and-otc` (Duffie OTC search model) missing**. Pillar-level hub stale — lists 6 topics (legacy flat notes), omits 3 of 9 folders. |
| Depth & template | ✅ | **63/63** locked-template pass; 0 YAML/backslash defects; mean ~10k chars; audience arc in all 9 hubs. |
| Coherence & links | ⚠️ | 719/731 wikilinks resolve; **12 broken** (all in `market-impact-and-depth` + `limit-order-book-mechanics`); many cross-links route to legacy flat notes instead of folder hubs. |
| Math & code | ✅ | **69/69 python blocks run**; outputs match; all 12 spot-checked formulas correct vs verified corpus (incl. AS paper table, Kyle, GM, PIN, VPIN, Roll, Amihud, Ho–Stoll). |

**Follow-ups (recommended, low effort, high value):**
1. Build `dealer-banks-and-otc/` (Duffie–Gârleanu–Pedersen 2005 anchor) — the only missing corpus sub-topic.
2. Rewrite the pillar hub `index.md` to route to the 9 folder indexes (currently routes to legacy flat notes and omits 3 folders).
3. Fix 12 broken wikilinks: repoint `limit-order-book-mechanics-and-l3/index` → `limit-order-book-mechanics/index` (7 files) and `pillars/02-execution/almgren-chriss/index` → `pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index` (4 files); strip trailing `\` in `limit-order-book-mechanics/index.md`.
4. Optional: repoint cross-folder links from legacy flat notes to folder `/index` hubs, then retire flat notes.
5. Optional: fix the `½` on the inventory term in `corpus/pillar6-market-making.md` line 106 (corpus-only).
