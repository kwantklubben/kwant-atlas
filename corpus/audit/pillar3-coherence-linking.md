# Pillar 3 — Coherence & Cross-Linking Audit

**Pillar:** 03-derivative-pricing (Derivative Pricing & Structuring)
**Repo:** `/home/alfred/local-repos/kwant-atlas`
**Scope:** 8 topic-folders, their `index.md` hubs, 01–06 sub-pages, the pillar `index.md`, and the 7 legacy flat notes.
**Method:** programmatic extraction and resolution of every `[[wikilink]]` against the on-disk target set (folder `index.md` ↔ folder slug, `.md` ↔ slug), plus inbound/outbound link-graph analysis across all of `content/`, and manual reading of all hub indexes and a sample of sub-pages.
**Date:** 2026-09-10

---

## 0. Headline verdict

**Pillar 3 is content-complete and internally coherent as a *curriculum*, but it is NOT yet coherent as a *navigable atlas*.** The eight folders each contain a genuinely strong hub + six-page arc, and the scientific progression is sound. However the **migration from the old flat notes is unfinished**: the pillar index and the repo root index still point only at the legacy flat slugs, and the folders themselves still emit **102 links to old flat slugs** alongside their new-folder links. The result is a **split-brain navigation graph**: a reader lands on the old flat notes and never sees the new hubs, while **6 of the 8 new hubs have zero inbound links from anywhere else in the repo**.

- Coherence (subject matter progression): **GOOD**
- Cross-linking correctness (broken links): **NEAR-CLEAN — 1 broken link out of 588**
- Cross-linking consistency (new vs legacy slugs): **POOR — 102 legacy-slug refs**
- Entry points / reading path from repo root: **FAILING — the 8 folders are effectively orphaned from top-level navigation**
- Three-jobs coverage once inside a folder: **STRONG (lookup ✔ / study arc ✔ / failure modes ✔)**

---

## 1. Structural inventory

| Metric | Value |
|---|---|
| Topic-folders | 8 |
| Total `.md` files inside the pillar | 63 |
| — hub `index.md` (8) + sub-pages `01–06` (48) | 56 (the new structure) |
| — legacy flat notes | 6 |
| — pillar `index.md` | 1 |
| Total `[[wikilinks]]` inside the pillar | **588** |
| Broken wikilinks | **1** |
| Links to legacy flat slugs (still present) | **102** |
| Hubs with zero cross-folder inbound links | **6 of 8** |

Per-folder link profile (links emitted by all 7 files in the folder):

| Folder | files | wikilinks | self | cross-pillar(03) | foundations | other pillars |
|---|---|---|---|---|---|---|
| black-scholes-merton | 7 | 64 | 32 | 20* | 12 | 0 |
| volatility-surfaces-and-smiles | 7 | 62 | 31 | 24* | 7 | 0 |
| advanced-volatility-heston-sabr | 7 | 89 | 43 | 34* | 11 | 1 |
| no-arbitrage-and-binomial | 7 | 80 | 47 | 23* | 10 | 0 |
| numerical-methods | 7 | 71 | 44 | 20* | 7 | 0 |
| exotic-and-path-dependent-options | 7 | 67 | 32 | 22* | 13 | 0 |
| interest-rate-and-term-structure | 7 | 61 | 36 | 12* | 12 | 1 |
| counterparty-risk-and-xva | 7 | 60 | 35 | 10* | 5 | 10 |

\* "cross-pillar(03)" counts links to *other* Pillar-3 targets, but the majority of these point at **legacy flat slugs**, not new folder hubs — see §3.2.

---

## 2. Q1 — Do the 8 topics form a coherent pillar?

**Verdict: YES, the progression is logical and the topics are well-sequenced and connected.** The set covers the standard sell-side derivative-pricing canon and maps onto a defensible dependency order:

```
no-arbitrage-and-binomial   (discrete foundations: law of one price, CRR, FTAP)
        └─> black-scholes-merton   (continuous limit, PDE, closed forms, Greeks)
                ├─> volatility-surfaces-and-smiles   (the empirical σ object; Dupire/SVI)
                │       └─> advanced-volatility-heston-sabr   (Heston/SABR dynamics)
                ├─> numerical-methods   (PDE/MC/FFT engines that serve all of the above)
                ├─> exotic-and-path-dependent-options   (barriers, Asians, lookbacks, quantos)
                ├─> interest-rate-and-term-structure   (rates as the underlying)
                └─> counterparty-risk-and-xva   (the clean price + default/funding/capital)
```

- Each hub's `**Basic Prerequisites:**` line correctly names its upstream topic (e.g. volatility-surfaces → BSM; Heston/SABR → volatility-surfaces; xVA → BSM + stochastic calculus). The dependency edges are real and acyclic.
- The `index.md` "one-sentence essence" and mermaid "Derivative Engineering Pipeline" in the pillar index express the same spine (quotes → curve → vol surface → model selection → engine → Greeks → hedging).
- Cross-folder §6 bridges consistently frame neighbours as "Forward topic-folder pages", "Sibling", "Base" — the *semantic* graph is deliberate and correct.
- Each folder runs the same 6-beat internal arc (Intuition → Ground Truth/derivations → Implementation → Failure Modes → Literature → Graph Bridges), so the eight folders read as one designed system rather than isolated pages.

**Minor content-cohesion gaps:**
- `numerical-methods` is *servant* to every other topic but is positioned (by the pillar index's omission, see §4) as if it were an afterthought. It is the natural hub for "how do I actually compute the Heston/swaption/xVA numbers"; the spine should route through it explicitly.
- There is no single pillar-level ordered **curriculum** (zero → expert). Each folder has its own audience arc, but nothing stitches the eight folders into a 20-step path. This is the main study-guide weakness (see §4/Q3).

---

## 3. Q2 — Cross-linking

### 3.1 Broken wikilinks: **1**

| # | Source file | Link text | Problem |
|---|---|---|---|
| 1 | `pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange.md` (line 13) | `[[foundations/multivariable-calculus-and-ito\|Stochastic Calculus & Itô's Lemma]]` | Target `foundations/multivariable-calculus-and-ito` **does not exist**. The real file is `foundations/multivariable-calculus-and-optimization`. The alias text is *also* wrong — it says "Stochastic Calculus & Itô's Lemma" (a copy-paste of the sibling link on the same line). Correct form: `[[foundations/multivariable-calculus-and-optimization\|Multivariable Calculus]]`. |

All other 587 wikilinks resolve against real targets (folder hubs, sub-pages, legacy notes, foundations files, other-pillar files). No dangling anchors, no malformed `[[` blocks.

### 3.2 The real cross-linking problem: legacy vs new slugs (102 refs)

Although 587/588 links *resolve*, resolution is not the same as pointing at the right object. Because the legacy flat notes are still present, links to the old slugs resolve "successfully" while bypassing the new hubs entirely. The new and legacy slugs differ subtly:

| New folder hub (should be target) | Legacy flat note (what is often linked) |
|---|---|
| `.../black-scholes-merton` | `.../black-scholes-merton-and-feynman-kac` |
| `.../no-arbitrage-and-binomial` | `.../no-arbitrage-and-binomial-trees` |
| `.../volatility-surfaces-and-smiles` | `.../implied-volatility-surface-and-smiles` |
| `.../advanced-volatility-heston-sabr` | `.../advanced-volatility-heston-and-sabr` |
| `.../interest-rate-and-term-structure` | `.../interest-rate-and-term-structure-models` |
| *(no new folder for the Greeks topic)* | `.../the-greeks-and-dynamic-hedging` |

Legacy-slug references emitted **by the new folders themselves**, per folder:

| Folder | legacy refs | new cross-folder refs |
|---|---|---|
| black-scholes-merton | **20** | 0 |
| exotic-and-path-dependent-options | **22** | 0 |
| volatility-surfaces-and-smiles | 14 | 10 |
| no-arbitrage-and-binomial | 14 | 11 |
| advanced-volatility-heston-sabr | 10 | 24 |
| interest-rate-and-term-structure | 10 | 2 |
| numerical-methods | 8 | 12 |
| counterparty-risk-and-xva | 4 | 6 |
| **Total** | **102** | **65** |

Notes:
- **`black-scholes-merton` (the flagship hub) and `exotic-and-path-dependent-options` emit ZERO new-folder cross-links** — all 20 and 22 of their outbound Pillar-3 links, respectively, go to legacy slugs. The flagship is the biggest offender.
- The mixed style is visible in the same §6 block, e.g. `no-arbitrage-and-binomial/06`: it links the *new* `.../black-scholes-merton` **and** the *old* `.../implied-volatility-surface-and-smiles` on the same line — an inconsistent migration.
- `numerical-methods/06` §6 links old `advanced-volatility-heston-and-sabr` and old `interest-rate-and-term-structure-models`; `exotic/06` §6 links old `advanced-volatility-heston-and-sabr`, old `interest-rate-and-term-structure-models`, and old `black-scholes-merton-and-feynman-kac`.
- `the-greeks-and-dynamic-hedging` is a legacy note with **no new-folder successor**; it is still linked from BSM, no-arbitrage, numerical, and volatility folders. Either fold it into `black-scholes-merton/04-greeks-and-hedging` or keep it deliberately as the Greeks hub — but decide, don't leave it dangling.

### 3.3 Every §6 "Connected Graph Bridges" block is present

All 63 files contain a `### 6. Connected Graph Bridges` section (or the hub equivalent). No file is missing the section. The structural scaffolding is uniform and complete.

### 3.4 Folder-level cross-link matrix (new-slug edges only)

```
rows = source, cols = target        BSM  vol  advv  narb  num  exo  ir   xva
black-scholes-merton                  -    0    0     0    0    0   0    0
volatility-surfaces-and-smiles        10   -    0     0    0    0   0    0
advanced-volatility-heston-sabr       10   14   -     0    0    0   0    0
no-arbitrage-and-binomial             11   0    0     -    0    0   0    0
numerical-methods                     12   0    0     0    -    0   0    0
exotic-and-path-dependent-options      0   0    0     0    0    -   0    0
interest-rate-and-term-structure       2   0    0     0    0    0   -    0
counterparty-risk-and-xva              6   0    0     0    0    0   0    -
```

Everything points into `black-scholes-merton` (51 new edges) or `volatility-surfaces-and-smiles` (14). **`advanced-volatility`, `no-arbitrage`, `numerical-methods`, `exotic`, `interest-rate`, and `counterparty-risk` receive ZERO new-folder cross-links.** Cross-linking is a hub-and-spoke pointing at BSM, not a web.

---

## 4. Q3 — Is there a clear READING PATH through the pillar?

**Verdict: NO pillar-level reading path exists. The entry points are stale.**

### 4.1 The pillar `index.md` links only legacy flat notes

`content/pillars/03-derivative-pricing/index.md` lists **6 topics**, all targeting **legacy flat slugs**:

1. `.../no-arbitrage-and-binomial-trees`
2. `.../black-scholes-merton-and-feynman-kac`
3. `.../the-greeks-and-dynamic-hedging`
4. `.../implied-volatility-surface-and-smiles`
5. `.../advanced-volatility-heston-and-sabr`
6. `.../interest-rate-and-term-structure-models`

**It contains zero wikilinks to any of the 8 new topic-folders.** It also **omits three whole topics** from its list: `numerical-methods`, `exotic-and-path-dependent-options`, and `counterparty-risk-and-xva`. (The substrings "black-scholes-merton", "no-arbitrage-and-binomial", "interest-rate-and-term-structure" appear only *inside* the legacy slugs, not as folder links.)

### 4.2 The repo root `content/index.md` has the same gap

The root index's Pillar-3 block lists the same six legacy flat slugs and **no new folder**. So the two canonical entry points into the pillar both route the reader to the superseded flat notes.

### 4.3 No top-level route reaches the new folders — 6 hubs are orphans

Link-graph reachability from `content/index.md`:
- Root index → legacy flat notes → (flat notes link only to other legacy flat notes and foundations).
- The 8 folders are **not referenced by the root index, the pillar index, or any file in any other pillar** (verified: zero non-Pillar-3 inbound edges to any of the 8 folders).
- Inbound links to the folder hubs: `black-scholes-merton` 21 (15 external — all from sibling P3 folders), `volatility-surfaces-and-smiles` 7 (1 external), and the remaining **six hubs have only self-referential inbound (≤6, all from within their own folder)**.

**Orphaned hubs (unreachable from any other page in the repo):**
`advanced-volatility-heston-sabr`, `no-arbitrage-and-binomial`, `numerical-methods`, `exotic-and-path-dependent-options`, `interest-rate-and-term-structure`, `counterparty-risk-and-xva`.

(The Quartz file-explorer sidebar will still expose the folders by browsing tree — so this is a *link-graph* orphaning, not total invisibility — but any reader who follows the index, as the atlas's design intends, will never arrive at these hubs.)

### 4.4 Sub-pages

The BSM and volatility sub-pages do receive external inbound links (from sibling folders' §6 blocks). Every sub-page of the other six folders has **zero external inbound** — again because those folders only cross-reference legacy slugs, not each other's sub-pages.

### 4.5 What a reading path *should* be

There is enough per-folder "audience arc" material to assemble a pillar path, but it is never assembled. Missing artifact: a single ordered route in the pillar `index.md`, e.g.

`no-arbitrage/01 → BSM/01–04 → volatility/01–03 → heston-sabr/01–04 → numerical/01–04 → exotic/01–04 → IRS/01–04 → xVA/01–04`, with a "fast lookup" table of the 8 hubs and a "debug from first principles" entry that points directly at the 8 `05-failure-modes-and-practice` pages.

---

## 5. Q4 — Does the pillar serve the three jobs?

| Job | Inside a folder | Verdict |
|---|---|---|
| **(1) FIND fast (lookup table)** | Every hub has a §2 "Quick-Reference Lookup" dense formula table with a *Verified check* column, and a "Critical caveat" callout. §5 lists the primary literature per folder. | **STRONG.** Consistent across all 8 hubs. The verified-number column is a genuine differentiator. |
| **(2) FOLLOW a path (study guide)** | Each hub's §6 carries a "Recommended reading route (audience arc)": Absolute beginner / Formulas+code / Robustness, all with full-slug sub-page links. Sub-pages also carry Back/Forward navigation footers. | **STRONG per folder, ABSENT per pillar.** No zero→expert route across the eight folders; no route from the pillar index into the folders at all. |
| **(3) DEBUG from first principles** | Every folder has a `05-failure-modes-and-practice` page + a §4 "Failure Modes" signpost table on the hub with 3–4 named breakdowns and their first-principles cause. | **STRONG.** Present and meaningfully written in all 8 folders. |

So: the *folder* unit is an excellent three-job artifact; the *pillar* unit fails jobs (1) and (2) at the top level because the index does not aggregate the hubs into a lookup table or a path.

---

## 6. Q5 — Coherence with the rest of the repo

**Foundations: GOOD.** All 8 folders link to `foundations/` — `stochastic-calculus-and-ito` is the ubiquitous base (every hub), plus `probability-and-measure-theory`, `multivariable-calculus-and-optimization`, `econometrics-and-time-series`. Counts per folder: BSM 12, vol 7, adv-vol 11, no-arb 10, numerical 7, exotic 13, IRS 12, xVA 5. These resolve (no broken foundations links except the single §3.1 typo).

**Other pillars: WEAK / one-sided.** Only `counterparty-risk-and-xva` links out to another pillar (10 links: `pillars/04-quantitative-risk/var-and-expected-shortfall` ×6, `.../credit-risk-and-the-merton-model` ×4, `.../stress-testing-and-scenario-analysis`, `.../extreme-value-theory-and-fat-tails`). The other 7 folders are islands w.r.t. the rest of the atlas. Natural missing bridges:
- `numerical-methods` → Pillar 08 (quant development / HPC Monte Carlo) and Pillar 01 (variance reduction in research).
- `volatility-surfaces` / `heston-sabr` → Pillar 04 (`var-and-expected-shortfall`, filter/regime risk) and Pillar 06 (market-making vol quoting).
- `exotic-and-path-dependent-options` → Pillar 06 (hedging flow).
- Conversely, **no other pillar links into Pillar 3** (verified: zero inbound from pillars 01/02/04/05/06/07/08).

**Legacy duplication:** the 6 legacy flat notes remain full standalone pages (no deprecation banner, no redirect), duplicating content now covered by the folders. This is the root cause of both the split navigation and the legacy-slug link drift. Decide their fate (redirect stubs → new hubs, or delete).

---

## 7. Findings summary (severity-ranked)

| # | Severity | Finding |
|---|---|---|
| F1 | **HIGH** | Pillar `index.md` and repo `content/index.md` link only legacy flat notes; **no link to any of the 8 new folders**. Three topics (numerical, exotic, xVA) missing from the topic list entirely. |
| F2 | **HIGH** | **6 of 8 folder hubs are link-orphans** (no inbound edge from outside their own folder); the pillar has no pillar-level reading path. |
| F3 | **MEDIUM** | **102 legacy-slug references** emitted by the new folders themselves; migration is ~60% old / 40% new and inconsistent within single §6 blocks. |
| F4 | **MEDIUM** | Cross-linking is hub-and-spoke toward BSM (51 new edges) + vol-surfaces (14); all other folders receive zero cross-folder links. |
| F5 | **LOW** | **1 broken wikilink**: `exotic/04` → `foundations/multivariable-calculus-and-ito` (nonexistent; alias text also wrong). |
| F6 | **LOW** | `the-greeks-and-dynamic-hedging` legacy note has no new-folder successor yet is still linked from 4 folders — decide keep/fold. |
| F7 | **LOW** | Other-pillar cross-linking is one-sided (only xVA → Pillar 04); 7 folders are atlas-islands. |
| F8 | **INFO** | No pillar-level zero→expert curriculum joining the 8 folders. Per-folder audience arcs are excellent. |

---

## 8. Recommended fixes (priority order)

1. **Rewrite the pillar `index.md`** to (a) list and link all **8 folder hubs** by full slug, (b) add a "Fast lookup" table (topic → hub → primary formulas → failure-mode page), and (c) add an explicit ordered **zero→expert reading path** across folders. Mirror the link list into `content/index.md`.
2. **Resolve the legacy notes**: convert the 6 flat notes into one-line redirect stubs pointing at their successor hub (or delete), so any remaining reference lands on the new structure.
3. **Rewrite the 102 legacy-slug refs** to the new folder/sub-page slugs (mechanical, per §3.2 table). Pay special attention to `black-scholes-merton` and `exotic-and-path-dependent-options`, which currently emit **zero** new-folder links.
4. **Fix the single broken link** (F5).
5. **Add inbound cross-links** so the 6 orphan hubs are reachable: at minimum, add each hub to the pillar index (fix #1 covers this) and add reciprocal §6 bridges from BSM/vol-surfaces into numerical, exotics, IRS, and xVA.
6. **Add other-pillar bridges** (numerical→08/01, vol→04/06, exotic→06) per §6.

---

## Appendix A — Broken wikilink list (complete)

```
1. content/pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange.md:13
   [[foundations/multivariable-calculus-and-ito|Stochastic Calculus & Itô's Lemma]]
   → target does not exist (correct file: foundations/multivariable-calculus-and-optimization; alias text also incorrect)
```

**Broken total: 1** (of 588 links, 99.83% resolve).

## Appendix B — Legacy-slug reference counts

```
black-scholes-merton                 20 legacy refs ; 0 new cross-folder
exotic-and-path-dependent-options    22 legacy refs ; 0 new cross-folder
volatility-surfaces-and-smiles       14 legacy refs ; 10 new cross-folder
no-arbitrage-and-binomial            14 legacy refs ; 11 new cross-folder
advanced-volatility-heston-sabr      10 legacy refs ; 24 new cross-folder
interest-rate-and-term-structure     10 legacy refs ; 2 new cross-folder
numerical-methods                     8 legacy refs ; 12 new cross-folder
counterparty-risk-and-xva             4 legacy refs ; 6 new cross-folder
                                     ---------------  ; ----------------
                                     102 total       ; 65 total
```

## Appendix C — Hub inbound-link (reachability) summary

```
hub                                     total inbound   from outside own folder
black-scholes-merton                         21            15
volatility-surfaces-and-smiles                7             1
advanced-volatility-heston-sabr               6             0   <-- orphan
no-arbitrage-and-binomial                     6             0   <-- orphan
numerical-methods                             6             0   <-- orphan
exotic-and-path-dependent-options             6             0   <-- orphan
interest-rate-and-term-structure              6             0   <-- orphan
counterparty-risk-and-xva                     6             0   <-- orphan
```
