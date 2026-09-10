# Coherence & Consistency Audit — Is the Atlas *one* graph across pillars?

**Scope:** `content/` (94 topic-folders across 8 pillars + 9 foundations + 8 fundamentals-accounting = 111 hubs; 747 md files; 8,119 path-style wikilinks; `content/visualizer.html`).
**Method:** systematic extraction of every hub's `**Basic Prerequisites:**` vs its `01-from-zero-intuition.md` counterpart; pairwise scope-note / overlap scan of the named cross-pillar pairs (and all duplicate folder/term slugs); wikilink resolution; visualizer node-path resolution; targeted number cross-checks.
**Snapshot:** 2026-09-10 ~21:0x. *Note: the repo was being edited concurrently during this audit* — see [§3](#3-hubpage-prerequisite-mismatches), where the specifically-flagged `risk-factor-sensitivities` case was fixed mid-audit.

---

## 0. Verdict (short)

The Atlas is **substantially one coherent graph, but with a leaky perimeter**. The *inside* of the graph is strong: 97/97 topic hubs share an identical 6-section template; 8,118 of 8,119 path-style wikilinks resolve; the ~16 cross-pillar topic pairs are — with **one clear exception** — well-partitioned with explicit **"Scope note"** callouts; a shared quantity (Kelly `S²/2+r`, Haug Greeks, `ES₉₇.₅` vs `VaR₉₉`) is genuinely single-sourced and reproduced identically across pillars. The failures are all at the **edges**: (a) one duplicated topic treated twice with no partition note; (b) two genuine content contradictions; (c) 16 hubs whose stated prerequisite contradicts their own on-ramp page; (d) a D3 visualizer whose node slugs are 5 topics stale (2 of them dead links); and (e) 421 wikilinks aimed at **legacy flat notes** that shadow the live hubs for 19 topics.

**Verdict: COHERENT CORE, LEAKY PERIMETER — not three disconnected systems, but not yet one airtight graph.**

---

## 1. Cross-pillar overlap table

16 overlap/duplication pairs examined (the 6 named in the brief + 10 adjacent). "Well-partitioned" = an explicit *scope note* / deliberate-divergence statement exists on at least one side.

| # | Topic | Pillars / folders | Well-partitioned? | Evidence |
|---|-------|-------------------|-------------------|----------|
| 1 | **Greeks** | P3 `black-scholes-merton` ↔ P4 `risk-factor-sensitivities` | ✅ **Yes (exemplary)** | P4 hub states the pivot explicitly: *"Pillar 3 derives the Greeks … Pillar 4 uses the Greeks"* (`risk-factor-sensitivities/index.md:20-23`). Same Haug numbers reused verbatim (`Δ=0.503105, Γ=0.026794, ν=0.192999`) — one source of truth, no drift. |
| 2 | **Counterparty Risk & xVA** | P3 `counterparty-risk-and-xva` ↔ P4 `counterparty-risk-and-xva` | ❌ **No — the one muddy pair** | **Identical folder slug in two pillars**, both 7-page / 6-section hubs, both primary-source Gregory, both define `CVA = −LGD∫λ·D·EPE`. **Neither hub names the other; neither carries a scope note.** The angle *does* differ (P3 = desk/pricing, FVA/MVA; P4 = risk/regulatory, SA-CCR/netting) but the reader cannot tell from either page. See fixes. |
| 3 | **Liquidity** | P4 `liquidity-risk-and-funding` ↔ P6 `liquidity-risk-and-asset-pricing` | ✅ Yes | P6 hub: *"deliberately distinct from Pillar 4's funding view … here the questions are [asset pricing]"* (`liquidity-risk-and-asset-pricing/index.md`). Clean partition. |
| 4 | **Backtesting (stats)** | P1 `backtesting-hygiene` ↔ P2 `execution-backtesting-and-simulation` | ✅ Yes | P2 scope note routes the statistics to P1: *"the statistical honesty of a signal backtest lives in Backtesting Hygiene"*. |
| 5 | **Backtesting (engine)** | P1 `backtesting-hygiene` ↔ P8 `event-driven-backtesting-engines` | ⚠️ **Partial** | Distinct angle (engine architecture vs multiple-testing), but the **P8 hub has no scope note** naming P1/P2 — partition is implicit only. |
| 6 | **Backtesting (ML CV)** | P1 `backtesting-hygiene` ↔ P7 `purged-cross-validation-and-backtest-hygiene` | ✅ Yes | P7 hub: *"the companion to the classical backtesting-hygiene folder … but for the ML pipeline"*. |
| 7 | **Feature engineering** | P1 `feature-engineering-and-labeling` ↔ P7 (`purged-cv`, `tree-and-boosting-methods`, `deep-learning-for-sequences`, `alternative-data-pipelines`) | ✅ Yes | P7 pages cite P1 as the label/interval prerequisite; P1's Triple-Barrier is referenced, not re-derived. |
| 8 | **Regime detection** | P1 `regime-detection` ↔ P7 `regime-classification-hmm-and-gmm` | ✅ Yes (explicit) | P7 hub: *"The econometric twin of this folder lives in Pillar 1 … that folder is the Hamilton-filter view; **this** folder is the machine-learning view: GMM/K-means, EM, HMM as a generative model."* |
| 9 | **Almgren–Chriss / impact** | P2 `optimal-execution-and-almgren-chriss` ↔ P6 `market-impact-and-depth` | ✅ Yes (two-way) | Both hubs carry mirrored scope notes: P2 = *scheduling* view, P6 = *impact-model* view; P2 explicitly forwards to P6 and vice-versa. |
| 10 | **Volatility modeling** | P1 `garch-and-volatility-modeling` ↔ `foundations/econometrics-and-timeseries/04-volatility-modeling` | ⚠️ Partial | P1 hub links the foundations sibling; but the **staleness risk is real** (two live GARCH derivations). No explicit "this extends that" note on the foundations side. |
| 11 | **Kelly / growth** | P5 `kelly-criterion-and-bet-sizing` ↔ `foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion` | ✅ Yes | Same example reproduced identically (`f*=2.2222, g=S²/2+r=0.115556`) on both; P5 references foundations explicitly. **Model of cross-layer single-sourcing.** |
| 12 | **Covariance / RMT** | P5 `covariance-shrinkage-and-denoising` ↔ `foundations/linear-algebra-and-matrices/06-advanced-extensions` | ⚠️ Partial | Same Marchenko–Pastur law `λ±=(1±√(N/T))²` derived on both layers; different examples, no conflict, but no partition note. |
| 13 | **VaR family** | P4 `var-and-expected-shortfall` ↔ P4 `parametric-historical-and-monte-carlo-var` (same pillar) | ⚠️ Partial | Adjacent and cross-linked (P4-PAR → P4-VAR); boundary (definition/coherence vs computation) is implicit. |
| 14 | **Transaction cost / impact** | P5 `constraints-and-transaction-costs` ↔ P6 `market-impact-and-depth` ↔ P2 AC | ⚠️ Partial | Same square-root law appears on all three; **no scope note on the P5 side** pointing to P2/P6. |
| 15 | **Execution family (intra-pillar)** | P2 `execution-algorithms-vwap-twap-pov` ↔ `optimal-execution-and-almgren-chriss` | ✅ Yes | P2 hubs carry "Scope note (vs the sibling folder)" on essentially every folder. |
| 16 | **Momentum** | P1 `momentum` ↔ P1 `factor-investing-and-timing` | ✅ Yes | `factor-investing-and-timing` hub declares itself the *"investing and practice half"* with MFFM as sibling. |

**Score:** 11 well-partitioned · 5 partial · **1 muddy (the P3/P4 xVA duplicate)**.
The brief's six named pairs are all well-partitioned **except** that the brief did not name the one genuinely muddy pair (#2) — the duplicate `counterparty-risk-and-xva` folder is the real redundancy.

---

## 2. Contradictions found

Two genuine contradictions (same quantity, two different values/forms). Both are cross-page and reproducible.

### C1 — Square-root impact exponent: **α ≈ 0.6 vs α = 0.5**

- **Side A:** `pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index.md:46`
  > `| Square-root impact law | ΔP ≈ Y σ (Q/V)^α, α ≈ 0.6 | toy ln-ln fit exponent 0.4922, R²=0.9401 |`
- **Side B (contradicts A on the same page's own sub-page):** `pillars/02-algorithmic-hft/execution-backtesting-and-simulation/06-advanced-extensions.md:100` and `:111`
  > `(2) sqrt-impact fit: exponent=0.4922 (theory 0.5)`
- **Side C:** `pillars/06-market-making/market-impact-and-depth/04-the-square-root-law.md:22` and `:44`
  > `I ≈ σ Y √(Q/V)` … `ℓ = √(2ΔV/ρ₀) ∝ √(ΔV) — square-root impact`
  (and `index.md:60`: *"impact grows as the **square root** of order size"*)

The P2 hub labels the law "square-root" yet prints **α ≈ 0.6**; its own sub-page computes **theory 0.5** and the P6 canonical treatment uses **0.5**. (`α≈3/5` is the *Almgren et al. 2005 realized-impact* exponent, so the hub is echoing a different quantity while calling it the square-root law — a genuine, fixable inconsistency, not just notation.)

### C2 — Unhedged gamma loss: **½ S⁴σ⁴Γ²Δt vs ½Γ(ΔS)²**

- **Side A (home page):** `content/index.md:208` (the "Why Is My Strategy Failing?" diagnostic matrix)
  > `… unhedged Gamma loss $\frac{1}{2} S^4 \sigma^4 \Gamma^2 \Delta t$.`
- **Side B (the pillar source of truth):** `pillars/04-quantitative-risk/risk-factor-sensitivities/index.md:59` and `:160`, `02-delta-gamma-vega.md:31`, `01-from-zero-intuition.md:30`; and `pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging.md:108`
  > `ΔV ≈ … + ½ Γ (ΔS)² …` / residual `∼ ½ Γ S²[(ΔS/S)² − σ²Δt]`

Side A is dimensionally wrong (`S⁴σ⁴Γ²`, and it squares Γ) and contradicts the ½Γ(ΔS)² form used everywhere in the pillars. The **home page — the most-visited node — carries a formula that is wrong and inconsistent with its own referenced page** (`black-scholes-merton`).

*(No numeric contradiction was found among the other cross-checked quantities: Kelly `S²/2+r=0.115556`, Haug Greeks, `ES₉₇.₅/VaR₉₉=1.0049`, Basel `k≥3` / `1.5×`, McLean–Pontiff OOS 10% / post-pub 35%, Hendershott `0.28%` — all agree across files.)*

---

## 3. Hub/page prerequisite mismatches

Every topic hub opens with `**Basic Prerequisites:**`, and every `01-from-zero-intuition.md` carries its own. **These disagree in 84 of 94 folders.** Two severities matter.

### 3a. Flat contradictions — hub names a topic, its own on-ramp page says "none / no prior X needed": **16 folders**

| Folder | Hub prerequisite (says) | `01-from-zero` prerequisite (says) |
|---|---|---|
| `pillars/01-quantitative-research/backtesting-hygiene` | Probability & Measure Theory (order stats, EVT, hypothesis testing) | "none beyond high-school probability" |
| `pillars/01-quantitative-research/signal-processing-and-kalman` | Linear Algebra + Probability | "none beyond high-school algebra" |
| `pillars/02-algorithmic-hft/colocation-and-clock-synchronization` | Calculus + Low-Latency Systems Architecture | "None — assumes zero prior knowledge" |
| `pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising` | Linear Algebra + Probability (Wishart) | "none — needs only `wᵀΣw`" |
| `pillars/06-market-making/limit-order-book-mechanics` | P2 Market Microstructure + Probability | "none … arithmetic and a little patience" |
| `pillars/06-market-making/liquidity-risk-and-asset-pricing` | Econometrics + Statistics | "none beyond basic algebra" |
| `pillars/06-market-making/market-maker-economics-and-rebates` | Glosten–Milgrom + Avellaneda–Stoikov | "none — only bid/ask" |
| `pillars/08-quantitative-development/data-infrastructure-and-reproducibility` | Tick-Level DBs + Data Sources | "none beyond running a Python script" |
| `pillars/08-quantitative-development/event-driven-backtesting-engines` | Backtesting Hygiene + Market Microstructure | "None. Comfort with Python … beginner entry point" |
| `pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity` | Low-Latency Linux + Market Microstructure | "none — only that you have seen a ticker" |
| `pillars/08-quantitative-development/python-quant-stack` | Pillar 1 + Numerical Methods | "none beyond basic Python" |
| `pillars/08-quantitative-development/tick-level-databases-and-timeseries` | Tick-Level DBs (itself) + HPC C++ | "none beyond basic SQL and Python" |
| `foundations/calculus-and-optimization` | Linear Algebra & Matrices | "none … arithmetic" |
| `foundations/ergodicity-and-statistical-mechanics` | Probability + Calculus | "none; arithmetic" |
| `foundations/numerical-methods` | Linear Algebra + Calculus + Probability | "High-school calculus and a first course in linear algebra" |
| `fundamentals-accounting/equity-valuation` | **Statistics & Inference + Econometrics** | "none — no accounting or finance background" |

`equity-valuation` is the most suspicious: a *fundamentals* hub requiring *foundations statistics + econometrics* while its own on-ramp declares no prerequisites — this looks like a copied/modelled prereq line rather than a designed one.

### 3b. The specifically-flagged case — **now fixed**

`pillars/04-quantitative-risk/risk-factor-sensitivities`: the hub **did** require *"Pillar 3 · The Greeks & Dynamic Hedging"* while `01-from-zero-intuition.md:22` read *"No options knowledge required."* **During this audit the hub was rewritten** (mtime 21:01, consistent with commit `52110f45 fix(learner-arc): close the from-zero arc gaps`). It now reads:

> `**Basic Prerequisites:** Multivariable Calculus (only the idea of a partial derivative — **no options knowledge required at this entry point**; the Pillar-3 Greeks are developed/utilised from 02 · Delta, Gamma & Vega onward).`

**Resolved** — cited here as the template for how the other 16 should be fixed (i.e. *state the on-ramp is prerequisite-free and say where the harder material begins*, rather than deleting the folder-level prereq).

### 3c. Scope-difference (hub = folder-level, on-ramp = page-level) — **68 folders, mild**

In most remaining folders the from-zero prerequisite is a *subset* of the hub's, or says "no prior X **for this page**". This is a defensible design (hub = prerequisites for pages 02–06; page 01 = standalone on-ramp) **but it is not signposted anywhere**, so a reader who lacks the hub prerequisite may bounce before reaching the page written for them. Recommended: a one-line convention on the hub — *"Basic Prerequisites = for the folder's advanced pages; `01` assumes none."*

---

## 4. One-graph & template assessment

### 4a. Template consistency — **excellent**

- **97 / 97** topic hubs carry the identical six-section skeleton in identical order:
  `1. Intuition & Practical Objective · 2. Mathematical Ground Truth … · 3. Computational Implementation … · 4. Failure Modes & First-Principles Breakdowns · 5. Canonical Literature & Study References · 6. Connected Graph Bridges`.
  Sections 1, 4, 5, 6 are **name-identical** everywhere; only §2/§3 descriptors vary (e.g. "& Derivations" vs "& Lookup Table", "— the formula engine"), which is intentional variety, not drift. 3 P7 hubs append "(hub signposts)" to §4 — cosmetic.
- **Hub structure** is uniform: pillar hubs = `Core Topics / Reading Path / (diagram) / Original Notes`; topic hubs = 6 sections + `Connected Graph Bridges`.
- **One pillar-level inconsistency:** `pillars/03-derivative-pricing/index.md` is the **only** pillar hub with **no "Original Notes" section** (3 headings vs 4); every other pillar hub has it.
- **One home-page inconsistency:** `content/index.md`'s diagnostic matrix links some rows to **legacy flat notes** (`…/backtesting-hygiene-and-deflated-sharpe`) and others to **folder hubs** (`…/statistical-arbitrage-and-pairs/index`) — mixed target style within one table.

### 4b. "One graph" instruments

| Instrument | Present? | Assessment |
|---|---|---|
| Single home hub (`content/index.md`) | ✅ | Mermaid taxonomy + diagnostic matrix + reading paths. |
| Per-hub formula lookups | ✅ | Every hub has a §2 lookup table — but these are **per-topic**, there is **no cross-pillar formula index**. |
| Glossary | ❌ | **None anywhere in `content/`** (grep "glossary" → 0). A cross-pillar glossary is the single biggest missing "one-graph" artefact. |
| Cross-links | ✅ | 8,119 path-style wikilinks; **8,118 resolve** (1 false-positive from math notation). Genuinely well-wired. |
| D3 visualizer | ⚠️ | See 4c. |

### 4c. Visualizer reflects the real links? — **partly; it has drifted**

- 107 nodes / 255 hand-curated edges vs **8,119 live wikilinks** — so the graph is a curated *subset*, not derived from the vault. That is a design choice, but it means the visualizer **cannot be trusted as the map** and will keep drifting.
- **5 of 94 topic folders are represented by pre-reorganisation slugs** that no longer name a live folder:
  | Visualizer node | Path in `visualizer.html:288` | Live folder |
  |---|---|---|
  | `P6-LOB` | `/pillars/06-market-making/limit-order-book-mechanics-and-l3` | `limit-order-book-mechanics` — **DEAD** (slug survives only in `_legacy/`) |
  | `P6-AS` | `/pillars/06-market-making/the-avellaneda-stoikov-model` | `avellaneda-stoikov-and-optimal-quoting` — **DEAD** |
  | `P7-TREE` | `/pillars/07-machine-learning-altdata/tree-based-factor-ranking-and-purged-cv` | `tree-and-boosting-methods` (links to legacy flat note) |
  | `P7-NLP` | `/pillars/07-machine-learning-altdata/financial-nlp-and-earnings-transcripts` | `financial-nlp-and-transcripts` (legacy flat note) |
  | `P7-SEQ` | `/pillars/07-machine-learning-altdata/deep-learning-for-sequential-data` | `deep-learning-for-sequences` (legacy flat note) |
- **Mixed path conventions:** P1/P2/P6/P7 nodes use `/folder`; P3/P4/P5/P8/FA nodes use `/folder/index`. Inconsistent (both may work in Quartz, but it signals two authors).
- No dangling edges (all 255 endpoints resolve to declared nodes) — internally consistent, just externally stale.

### 4d. Duplicate slugs (legacy flat notes shadow live hubs)

For **19 topics** there exist **two pages of the same slug**: a flat `pillars/<n>/<topic>.md` and a `<topic>/index.md` hub. Wikilinks written as `[[pillars/…/<topic>]]` are therefore **ambiguous**, and **421 wikilinks across the corpus use that ambiguous form** (top offenders: `backtesting-hygiene-and-deflated-sharpe` ×59, `var-and-expected-shortfall` ×54, `fundamental-multi-factor-models` ×36, `extreme-value-theory-and-fat-tails` ×36). Many are in *foundations* and *fundamentals* pages pointing "up" into Pillar 1/4. This is the largest single structural coherence leak: **the graph is partly wired to the pre-hub Atlas.** (The pillar hubs' deliberate "Original Notes" sections account for some, but far from all, of these.)

---

## 5. Number-consistency issues

**Clean, single-sourced (positive findings):**

- **Greeks:** `Δ=0.503105, Γ=0.026794, ν/pt=0.192999, Θ/day=−0.036989, ρ/pt=0.109656` — identical in P3 BSM (index, `04-greeks-and-hedging.md:95-97`) and P4 `risk-factor-sensitivities` (index:39-43,145; `02:106`). One verified source, reused.
- **Kelly bridge:** `f*=2.2222, g=S²/2+r=0.115556` identical in `foundations/ergodicity…/04-kelly-criterion.md:153` and `pillars/05…/kelly-criterion-and-bet-sizing/02-the-kelly-formula.md:104` and `03:91`. No drift.
- **Basel:** `VaR₉₉ multiplier k≥3` (1996) and `FRTB ES₉₇.₅ m꜀≥1.5`, `ES₉₇.₅/VaR₉₉=1.0049` consistent across `var-and-expected-shortfall` and `basel-and-regulation`.
- **Almgren–Chriss:** `κ=0.601133/day, θ=1.6635 d, κT=3.0057` consistent across index/03/04 of the AC folder.
- **McLean–Pontiff:** OOS 10% / post-pub 35% / lower bound 25% consistent between `factor-investing-and-timing/04` and `index.md:97`.
- **Reservation price in P6:** `r=98.4` (AS hub) vs `r=98.40` (inventory hub) — same value, formatting only.

**One number inconsistency found** — see **C1** (square-root exponent 0.6 vs 0.5). No other same-quantity/different-value pair was found in the sampled cross-checks.

---

## 6. Verdict & recommended fixes

**Verdict: COHERENT CORE, LEAKY PERIMETER.** The Atlas largely succeeds at being one graph from one source of truth — the templates, the cross-links, and the shared numbers are in genuinely good shape, and the cross-pillar partitioning is explicit in 11/16 examined pairs. It falls short of "one coherent whole" in five concrete, fixable ways.

### Priority fixes

1. **Resolve the `counterparty-risk-and-xva` duplicate (P3 vs P4).** Either (a) promote one as canonical and reduce the other to a scope-pointing stub, or (b) keep both but add the missing mirrored **scope notes** ("P3 = pricing/desk & FVA/MVA view → see P4 for the regulatory/netting view", and vice-versa) and distinct hub titles. *Currently the only muddy overlap.*
2. **Fix C2 on the home page:** `content/index.md:208` → replace `½ S⁴σ⁴Γ²Δt` with `½Γ(ΔS)² = ½Γ S²σ²Δt`.
3. **Fix C1:** align `execution-backtesting-and-simulation/index.md:46` with the rest — either `α ≈ 0.5` (square-root) or relabel as "realized-impact exponent ≈ 3/5 (Almgren et al. 2005)" to match its own sub-page's "theory 0.5".
4. **Close the 16 hub/page prerequisite contradictions (§3a)** using the pattern just applied to `risk-factor-sensitivities`; add a one-line hub convention ("hub prereqs = for pages 02–06; `01` assumes none") to cover the 68 scope-difference cases.
5. **Re-slug the 5 stale visualizer nodes** and **derive the edges from the wikilink graph** (or at minimum regenerate the node list from `content/` on build) so the D3 graph cannot drift again. Normalise the `/folder` vs `/folder/index` convention.
6. **Retire or de-ambiguate the 19 legacy flat notes:** either delete them (the hubs supersede them) or rename with a `-legacy` suffix, then repoint the 421 ambiguous wikilinks at the `…/index` hubs.
7. **Consider the two missing "one-graph" artefacts:** a cross-pillar **formula index** and a single **glossary** (neither exists today).

---

*Audit artefacts: this file. Companion audits in `corpus/audit/` (math-audit, code-audit, learner-perspective-audit, per-pillar).*
