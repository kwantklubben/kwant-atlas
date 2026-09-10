# Pillar 3 (Derivative Pricing) — Completeness & Topic-Coherence Audit

**Date:** 2026-09-10
**Auditor:** subagent (completeness pass)
**Repo:** `/home/alfred/local-repos/kwant-atlas`
**Scope audited:** `content/pillars/03-derivative-pricing/` (8 topic-folders, 56 folder pages, 8,935 lines) vs the intended Pillar-3 subtopic list in `corpus/pillar3-derivative-pricing.md` and `corpus/titles/pillar3-derivative-pricing.TITLES.md` (13 subtopics).
**Evidence base:** the actual content files, the six legacy flat notes, `corpus/verified/` (53 verified deep-reads), `corpus/handoff/*`, `content/index.md`, `content/visualizer.html`, `README.md`, git history.

---

## 1. What is built today

### 1.1 The 8 topic-folders (each = `index.md` hub + 6 sub-pages)

| Folder | Sub-pages | Lines |
|---|---|---|
| `black-scholes-merton/` | 01 from-zero · 02 PDE/derivation · 03 pricing formulas · 04 greeks-and-hedging · 05 failure-modes · 06 advanced | ~1,150 |
| `volatility-surfaces-and-smiles/` | 01 from-zero · 02 implied-vs-local-vol · 03 surface-models (SVI) · 04 advanced-dynamics · 05 failure-modes · 06 advanced | ~1,050 |
| `advanced-volatility-heston-sabr/` | 01 from-zero · 02 the-heston-model · 03 sabr-and-asymptotics · 04 stochastic-vol-dynamics · 05 failure-modes · 06 advanced | ~1,300 |
| `no-arbitrage-and-binomial/` | 01 from-zero · 02 no-arbitrage-and-risk-neutral · 03 binomial-trees-and-convergence · 04 fundamental-theorems · 05 failure-modes · 06 advanced | ~1,000 |
| `numerical-methods/` | 01 from-zero · 02 finite-difference · 03 monte-carlo · 04 variance-reduction · 05 failure-modes · 06 advanced | ~1,300 |
| `exotic-and-path-dependent-options/` | 01 from-zero · 02 barriers-and-digitals · 03 lookbacks-and-asians · 04 compound-chooser-quanto-exchange · 05 failure-modes · 06 advanced | ~950 |
| `interest-rate-and-term-structure/` | 01 from-zero · 02 bonds/yield-curve/forwards · 03 short-rate-models · 04 numeraire-hjm-market-models · 05 failure-modes · 06 advanced | ~1,150 |
| `counterparty-risk-and-xva/` | 01 from-zero · 02 exposure-and-margin · 03 cva-and-dva · 04 fva-and-mva · 05 failure-modes · 06 advanced | ~1,050 |

Every folder follows the same 6-section template (Intuition → Math/derivations → Implementation (runnable Python) → Failure modes → Literature → Graph bridges), and the formulas are cited to verified corpus pages (Haug §2/§3/§4, Gatheral 1.6/3.20, Bergomi 2.64/6.x, Glasserman 8.46–8.52, Gregory eq 17.3, Duffy 26.5–29.11). Build quality is high; this audit is **not** a depth critique of what exists.

### 1.2 The 6 legacy flat notes (still present, still linked)

`black-scholes-merton-and-feynman-kac.md` · `no-arbitrage-and-binomial-trees.md` · `implied-volatility-surface-and-smiles.md` · `advanced-volatility-heston-and-sabr.md` · `interest-rate-and-term-structure-models.md` · `the-greeks-and-dynamic-hedging.md` (+ `index.md` hub).

These are the pre-folder draft notes (6 per pillar cap). Handoff `02-PROJECT-STATE-AND-FILEMAP.md` §3b explicitly lists *"migrate/replace the 6 flat notes"* as outstanding work.

### 1.3 The intended scope (13 subtopics)

From `corpus/pillar3-derivative-pricing.md` / `corpus/titles/pillar3-derivative-pricing.TITLES.md`: options-fundamentals-and-markets; no-arbitrage-and-binomial; stochastic-calculus-for-pricing; black-scholes-merton; greeks-and-dynamic-hedging; volatility-surfaces-and-smiles; local-vol-and-stochastic-vol; numerical-methods; exotic-and-path-dependent-options; american-options-and-optimal-stopping; interest-rate-and-fixed-income-derivatives; counterparty-risk-and-xva; calibration-and-market-practice.

---

## 2. Intended-topic → built-coverage map

| # | Intended topic | Status | Where the material lives |
|---|---|---|---|
| 1 | **options-fundamentals-and-markets** | ❌ **MISSING** (no folder, no owner) | Fragments only: `black-scholes-merton/01` opens from zero on *pricing*, not on *products/markets*; Hull product catalogues are *cited* in literature sections of BSM/exotics/IR but never presented. Payoffs, conventions, futures/forwards mechanics, option-market microstructure, greeks-as-market-conventions: not taught anywhere in Pillar 3. |
| 2 | no-arbitrage-and-binomial | ✅ Folder | `no-arbitrage-and-binomial/` — 01–06, incl. FTAP, CRR, American backward induction, optimal stopping seeds. |
| 3 | **stochastic-calculus-for-pricing** | ❌ **MISSING in Pillar 3** (delivered at Foundations, thin) | `content/foundations/stochastic-calculus-and-ito.md` — **one 120-line flat note** covering BM, quadratic variation, 1-D & multi-asset Itô, Girsanov. Missing from that note: conditional expectation/Radon-Nikodym measure theory, martingale representation theorem, FTAP, change of numeraire, Feynman–Kac. Those live *dispersed* in `no-arbitrage-and-binomial/04`, `black-scholes-merton/02`, `interest-rate-and-term-structure/04`. |
| 4 | black-scholes-merton | ✅ Folder | `black-scholes-merton/` — PDE derivation, formulas, Feynman–Kac, greeks, failure modes. |
| 5 | **greeks-and-dynamic-hedging** | ⚠️ **FOLDED** (partial) | Statics are well covered by `black-scholes-merton/04-greeks-and-hedging.md` (full 1st/2nd/3rd-order Greek set, Haug-verified, scaling conventions, gamma–theta identity). **Dynamics are not**: discrete-hedging P&L variance, hedge-error economics, transaction costs/Leland, pin risk, vanna/volga *trading*, position management — present only in a 4-bullet failure-mode list (`bsm/05`) and in the legacy flat note `the-greeks-and-dynamic-hedging.md`. |
| 6 | volatility-surfaces-and-smiles | ✅ Folder (absorbs half of #7) | `volatility-surfaces-and-smiles/` — IV inversion, smile→density, Dupire local vol, SVI, sticky rules, variance swaps, skew dynamics. |
| 7 | local-vol-and-stochastic-vol | ✅ **Split across two folders** (no folder of this name) | Local vol → `volatility-surfaces-and-smiles/02,03,04`; stochastic vol → `advanced-volatility-heston-sabr/` (Heston CF, SABR expansion, Bergomi forward-variance, rough vol). Defensible split, but see overlap §4.1. |
| 8 | numerical-methods | ✅ Folder | `numerical-methods/` — FD/PSOR/penalty, MC, variance reduction, QMC, LSM, duality. |
| 9 | exotic-and-path-dependent-options | ✅ Folder | `exotic-and-path-dependent-options/` — barriers, digitals, lookbacks, Asians, compounds, chooser, quanto, exchange. |
| 10 | **american-options-and-optimal-stopping** | ❌ **MISSING as a topic; scattered** | Theory: `no-arbitrage-and-binomial/06` §2.1 ("American pricing as optimal stopping", Shreve ch 5–6) and `bsm/06`. Numerics: `numerical-methods/06` §2.1 (LCP, PSOR, penalty, LSM, duality) and `exotic-and-path-dependent-options/06` (LSM again). Backward induction: `no-arbitrage-and-binomial/03`. **No folder owns**: optimal-stopping theory as a subject (stopping times, Snell envelope, Doob decomposition, perpetual American), the exercise boundary / free-boundary problem as a topic, Monte-Carlo American methods as a topic (LSM vs stochastic mesh vs duality), analytic American approximations (Haug §3 series, Bjerksund–Stensland, Roll–Geske–Whaley). |
| 11 | interest-rate-and-fixed-income-derivatives | ✅ Folder | `interest-rate-and-term-structure/` — curve bootstrapping, Vasicek/CIR/Hull–White, HJM, LMM. |
| 12 | counterparty-risk-and-xva | ✅ Folder | `counterparty-risk-and-xva/` — exposure/margin, CVA/DVA, FVA/MVA/KVA. |
| 13 | **calibration-and-market-practice** | ⚠️ **FOLDED/dispersed** (no owner) | Vol calibration → `volatility-surfaces-and-smiles/03` (SVI fit), `advanced-volatility-heston-sabr/05` (calibration/hedging practice); rates calibration → `interest-rate-and-term-structure/04,05`; xVA mildly in `counterparty-risk-and-xva/04`. **No folder owns**: calibration as a discipline (objective functions, weighting, regularization, arbitrage-free constraints across expiries), market conventions (day counts, vol quotes, delta conventions, FX conventions), structuring/desk practice. |

**Score: 6 of 13 intended topics have a folder of their own** (no-arbitrage, BSM, vol-surfaces, numerical-methods, exotics, IR, xVA = 7, counting IR+xVA); **1 is a documented split** (local-vol-and-stochastic-vol → 2 folders); **3 have no home at all** (options-fundamentals, stochastic-calculus-for-pricing, american-options-and-optimal-stopping); **2 are folded with a real coverage gap on their dynamic/practice half** (greeks-and-dynamic-hedging, calibration-and-market-practice).

---

## 3. Verified corpus support for the missing topics

All of the following exist today in `corpus/verified/` and are described as math-verified. **The corpus can support building every missing topic** — the gap is editorial ownership, not source material.

### 3.1 `options-fundamentals-and-markets` — buildable
- `hull_ch1-6.md` (145 L) — markets/mechanics, futures/forwards, hedging with futures, interest rates, forward/FX.
- `hull_ch7-12.md` (134 L) — swaps, securitisation, OIS/FRA, binomial, Wiener/Itô intro, Black–Scholes–Merton.
- `hull_ch13-18.md`, `hull_ch19-23.md` (Ch 19 "The Greek Letters"), `hull_ch24-28.md`, `hull_ch29-37.md` — full vanilla/product/risk catalogue.
- `haug_lookup-1.md` (384 L) — cost-of-carry dictionary, every European/American variant, market conventions of scaling (per-vol-point Vega/Rho, per-day theta).
- Papers obtained per `TITLES.md`: Black & Scholes (1973), Merton (1973) — both FOUND as PDFs.
- **Source gap:** Natenberg, Sinclair ×2, Black (1976) are `NOT OBTAINED · LICENSED_NOT_DOWNLOADABLE` (ILL). Desk-practice colour will be thinner than intended until these land; Hull + Haug suffice for a solid folder.

### 3.2 `stochastic-calculus-for-pricing` — buildable, and already half-written
- `shreve2_ch1-3.md` — general probability, σ-algebras, conditional expectation, Brownian motion, martingale/Markov property, quadratic variation, reflection principle.
- `shreve2_ch4-5.md` — Itô calculus and risk-neutral pricing.
- `shreve2_ch6-7.md` — connections with PDEs (Feynman–Kac, CIR bond, Večeř PDE) and exotic options.
- `shreve1_ch13-16.md` — Itô–Doeblin, **Girsanov**, **martingale representation theorem**, **fundamental theorems of asset pricing**.
- `shreve1_ch17-20.md`, `shreve1_ch21-24.md` (numeraire change, bonds/term structure, HJM), `shreve1_ch25-29.md`, `shreve1_ch30-34.md` (stopping times, perpetual American).
- `bjork_ch1-7.md`, `bjork_ch8-14.md` (completeness & hedging, parity relations, the martingale approach, BS from a martingale view, multidimensional), `bjork_ch15-21.md`, `bjork_ch22-29.md`.
- Free/obtained whole-book PDFs per `TITLES.md`: Øksendal (403 pp), Musiela & Rutkowski (521 pp), Karatzas & Shreve (429 pp).
- Already exists in Atlas form (thin): `content/foundations/stochastic-calculus-and-ito.md`.

### 3.3 `american-options-and-optimal-stopping` — strongly buildable
- `shreve2_ch8-10.md` (171 L) — **Ch 8 "American Derivative Securities"**, verified: value as a max over stopping times, optional sampling, submartingale argument (no early exercise for a dividendless call), **perpetual American put solved**, exercise boundary; plus Ch 9 change of numeraire, Ch 10 term structure.
- `bjork_ch15-21.md` (220 L) — **Ch 21 "Optimal Stopping Theory & American Options"** with theorems/propositions numbered.
- `glasserman_ch7-9.md` (350 L) — **Ch 8 "Pricing American Options by Simulation"** (parametric stopping rules, stochastic mesh, LR mesh weights, regression/LSM eqs 8.46–8.52, duality 8.58/8.65) + Ch 7 sensitivities.
- `haug_lookup-1.md` §3 — analytical American formulas (BAW, Bjerksund–Stensland, Roll–Geske–Whaley, perpetual, American-on-futures), numerically verified.
- `shreve1_ch5-8.md`, `shreve1_ch30-34.md` — discrete stopping times / perpetual American.
- Papers FOUND: **Longstaff & Schwartz (2001)**, **Broadie & Glasserman stochastic mesh (2004)**.
- **Source gap:** Detemple, *American-Style Derivatives* — `NOT OBTAINED`.

### 3.4 `calibration-and-market-practice` — buildable, with an FX-practice hole
- `gatheral_ch1-5.md` (SVI eq 3.20, Heston CF) and `gatheral_ch6-10.md` (surface asymptotics ch 7, surface dynamics ch 8, barriers ch 9, cliquets ch 10).
- `bergomi_ch1-5.md` (649 L) and `bergomi_ch6-10.md` (519 L) — smile calibration practice, forward-variance, smile dynamics.
- `bm_ch5-8.md` (Ch 5 HJM, **Ch 6 LFM/LSM, Ch 7 "Cases of Calibration of the LIBOR Market Model"**, Ch 8 MC tests) + `bm_ch9-12/13-17/18-23.md` (1016-page Brigo–Mercurio is the rates-calibration reference).
- `haug_lookup-2.md` (607 L) — Ch 12 volatility & correlation, Ch 13 distributions.
- Papers FOUND: SVI (Gatheral & Jacquier 2014), SABR (Hagan et al. 2002), Heston (1993), Dupire (1994), Derman–Kani (1994), Gatheral lecture notes.
- **Source gap:** FX / desk practice — Wystup, Castagna, Natenberg, Sinclair all `NOT OBTAINED`. A folder can be built on vol + rates calibration; the FX-conventions half must be deferred or written from Haug's convention tables only.

### 3.5 `greeks-and-dynamic-hedging` — buildable (statics already done)
- `haug_lookup-1.md` §2 — complete first/second/third-order Greek set + Table 2-3 (the repo already reproduces it in `bsm/04`).
- `hull_ch19-23.md` — Ch 19 "The Greek Letters".
- `glasserman_ch7-9.md` — Ch 7 estimating sensitivities (pathwise vs likelihood-ratio, finite-difference bias/variance).
- Breeden & Litzenberger (1978) — FOUND (butterfly/static-hedging ↔ risk-neutral density).
- **Source gap:** Taleb *Dynamic Hedging*, Leland (1985) — `NOT OBTAINED`. The desk-practice half (hedge P&L decomposition, transaction-cost hedging, jumps, pin risk) is exactly what these two would supply.

---

## 4. Overlap, redundancy and coherence findings

### 4.1 `volatility-surfaces-and-smiles` ↔ `advanced-volatility-heston-sabr` — real overlap, currently managed by cross-links only
The two folders are framed as *statics* vs *dynamics/models* (`vs/index.md` §1 vs `av/index.md` §1), and they do cross-link deliberately (`av/04` → `vs/04`; `vs/index.md` → `av/`). But the same results are derived in both:
- ATM short-dated skew $\partial_k\sigma_{BS}^2 \to \rho\eta/2$ — `vs/03` §2.1 and `volatility-surfaces-and-smiles/index.md` lookup table, **and** `av/03` §2.1–2.2.
- Local-vol "factor 2" / most-probable-path result — `vs/02` §2.3–2.4 **and** `av/03` §2.1 item 3.
- Skew-stickiness ratio and Type I/II classification (Bergomi ch 9) — `vs/04` §2.1–2.2 **and** `av/04` §2.2.
- Bergomi–Guyon two-parameter expansion — `vs/04` §2.4 **and** `av/03` §2.5, `av/04` §2.3.
- Heston characteristic function / Fourier inversion — `vs/index.md` lookup **and** `av/02`, `av/04` code.

Verdict: not a *mistaken* split (it matches the corpus's own local-vol/stochastic-vol distinction), but it is the pillar's largest redundancy. Fix: add an explicit **ownership rule** to both hubs (VS owns surface objects: IV, Dupire, SVI, statics/no-arb; AV owns stochastic-vol dynamics: Heston CF, SABR expansion, Bergomi forward-variance, rough vol), and replace duplicated derivations in one of the pair with a link.

### 4.2 The greeks material is split awkwardly between a folder sub-page and a flat note
`bsm/04-greeks-and-hedging.md` is the *better* treatment (full 3rd-order set: vanna/volga/zomma/vomma/ultima, per-point scaling, gamma–theta identity, Haug-verified numerics). The legacy flat note `the-greeks-and-dynamic-hedging.md` is retained as a "sibling" — folder pages literally say *"See also the flat sibling topic The Greeks & Dynamic Hedging"* (`bsm/04` §5, §6). That is the awkward artifact: two pages on the same topic, one inside a folder and one at pillar root, with the flat note also carrying content the folders lack (pin risk, discrete-hedging error variance, Taleb/Hull desk references). Currently `vanna`/`volga` appear in only two files, and `volga` in only one — the higher-order Greek material is thin outside `bsm/04`.

### 4.3 American-option methods are triplicated
LSM is implemented **three times**: `numerical-methods/06` (§2.1 + code, PSOR/tree/LSM comparison), `exotic-and-path-dependent-options/06` (§ "Tool 2 — Longstaff–Schwartz American put", its own code and its own numeric result), and referenced again in `no-arbitrage-and-binomial/06` §2.1. Each instance is individually fine (they serve numerical-methods = "how to compute", exotics = "American exotics"), but the *topic* American-options-and-optimal-stopping has no owner, so there is no single place that defines the theory, the exercise boundary, and the estimator bias taxonomy. Classic "no home → duplicated everywhere, complete nowhere".

### 4.4 Calibration is spread over three folders with no owner
SVI fitting in `vs/03`; SV calibration in `av/05`; LMM calibration in `ir/04/05`. Cross-cutting subjects with no owning folder tend to be the ones that drift; this is one.

### 4.5 The 8 new folders are effectively orphaned in the site
This is the pillar's biggest *coherence* defect, independent of topic coverage:
- `content/pillars/03-derivative-pricing/index.md` "Core Pricing & Structuring Topics" still lists **the 6 old flat notes** and none of the 8 folders.
- `content/index.md` (home hub, §3 block) and its diagnostic matrix (`content/index.md:86`, `:171`) still link **only the old flat notes**.
- `content/visualizer.html` hard-codes node `path` values for exactly 6 Pillar-3 nodes — `no-arbitrage-and-binomial-trees`, `black-scholes-merton-and-feynman-kac`, `the-greeks-and-dynamic-hedging`, `implied-volatility-surface-and-smiles`, `advanced-volatility-heston-and-sabr`, `interest-rate-and-term-structure-models`. **No node exists for any of the 8 new folders**, so they are invisible in the graph (handoff flagged this as the #1 silent-staleness risk).
- `README.md` Pillar 3 blurb still describes the old 6-topic set.
- Conversely, the new folder pages clutter their "Connected Graph Bridges" sections with `Related flat notes:` links (34 references to the Heston/SABR flat note, 27 to the IV-surface flat note, etc.), i.e. the *new* content points backwards at the *superseded* draft.

Net effect: the pillar reads as two parallel, mutually-referencing structures. This is scheduled work (handoff §3b "migrate/replace the 6 flat notes" + lockstep maintenance) but it is currently unresolved, and it is what makes an otherwise strong build *feel* incomplete.

---

## 5. Verdict

**The topic set is NOT complete, and one structural issue makes it feel less coherent than it is.**

- **Complete:** 7 of the 13 intended subtopics have a proper, well-built folder of their own, and the split of `local-vol-and-stochastic-vol` across two folders is defensible (it mirrors the corpus's own distinction) provided an ownership rule is written down.
- **Incomplete:** three intended topics have **no home** — `options-fundamentals-and-markets`, `stochastic-calculus-for-pricing`, `american-options-and-optimal-stopping`; two more are **folded with a real gap on the half that the corpus actually asks for** — `greeks-and-dynamic-hedging` (statics done, dynamics missing) and `calibration-and-market-practice` (dispersed, no owner).
- **Buildable now:** the verified corpus supports every one of these (Shreve I/II, Björk, Glasserman ch 7–9, Haug lookup 1/2, Gatheral, Bergomi, Brigo–Mercurio, Hull ch 1–23, plus the LSM/mesh/SVI/SABR/Heston papers). The blocker is editorial, not bibliographic; the residual *source* gaps are FX/desk-practice (Natenberg, Sinclair, Wystup, Castagna, Taleb, Detemple — all `NOT OBTAINED`) and they degrade only the practice half of a few pages.
- **No topic in the built set is out of scope**, and no two folders are wholesale duplicates — the VS↔AV pair and the greeks split are the only meaningful redundancies.

### Recommended actions (to make Pillar 3 complete)

**ADD as new folders (priority order):**
1. **`american-options-and-optimal-stopping`** — highest-value add. Strongest verified backing of any missing topic (`shreve2_ch8-10`, `bjork_ch15-21` ch 21, `glasserman_ch7-9` ch 8, `haug_lookup-1` §3, LSM + stochastic-mesh papers), currently unowned and triplicated. Owns: optimal-stopping theory, free boundary, Snell envelope, analytic American approximations, MC American methods + duality.
2. **`options-fundamentals-and-markets`** — the pillar's declared entry point. Hull ch 1–12 verified + Haug conventions + Black–Scholes/Merton 1973 papers. Owns: payoffs, futures/forwards, market mechanics, conventions, put-call parity, price-quote plumbing. Without it, `bsm/01-from-zero-intuition` is doing double duty as both "what an option is" and "what BSM is".
3. **`calibration-and-market-practice`** — cross-cutting, no owner today, and the source backing is unusually good (`bm_ch5-8` ch 7 is literally "Cases of Calibration of the LMM"; Gatheral SVI; Bergomi; Haug ch 12). Scope this one to *vol + rates calibration + conventions* and defer the FX-conventions half until Wystup/Castagna arrive, or write it from Haug's cost-of-carry/convention tables.

**FOLD (do not create a folder):**
4. **`greeks-and-dynamic-hedging`** — the static half is *adequately* covered by `black-scholes-merton/04-greeks-and-hedging.md` (full verified Greek set; a new folder would duplicate it). Instead: rename that page to `04-greeks-and-dynamic-hedging.md`, absorb the legacy note's dynamic-hedging content (hedge-error variance, pin risk, transaction-cost/Leland, position management), and keep it inside BSM. Revisit a split only when Taleb/Natenberg land.
5. **`local-vol-and-stochastic-vol`** — keep the 2-folder split, but publish the ownership rule (§4.1) in both hubs.

**DECIDE AND RECORD:**
6. **`stochastic-calculus-for-pricing`** — either (a) build it as a Pillar-3 folder from `shreve2_ch1-7` + `shreve1_ch13-16/21-24` + `bjork_ch1-14`, or (b) formally keep its home in Foundations and expand `content/foundations/stochastic-calculus-and-ito.md` from a 120-line flat note into a multi-page topic (measure theory → Itô → Girsanov → martingale representation → FTAP → numeraire → Feynman–Kac). Option (b) fits the fact that Pillar 3 folders already link to it (BSM/01, BSM/02, no-arb/02, no-arb/04, IR/04 all depend on it). Whatever is chosen, the pillar index must say which, so the dependency is visible.

**HOUSEKEEPING (without which the pillar will not read as complete):**
7. Retire the 6 flat notes: either delete them after porting any unique content, or convert each into a one-paragraph pointer. In the same pass update `content/pillars/03-derivative-pricing/index.md`, `content/index.md` (+ diagnostic matrix), `README.md`, and the hard-coded `content/visualizer.html` node/edge table so the 8 (soon 11) folders are visible and linked, and strip the "Related flat notes" bridge lines from folder pages.

**Target end state:** 11–12 Pillar-3 folders (current 8 + american-options + options-fundamentals + calibration, with stochastic-calculus either added as the 12th or formally rehomed in Foundations), zero legacy flat notes, one hub that lists them all.

---

## Appendix A — File inventory used in this audit

| Path | Role |
|---|---|
| `content/pillars/03-derivative-pricing/index.md` | Pillar hub — **stale**: lists only the 6 legacy notes |
| `content/pillars/03-derivative-pricing/<8 folders>/{index,01..06}.md` | 56 pages, 8,935 lines, template-conformant |
| `content/pillars/03-derivative-pricing/<6 legacy flat notes>.md` | superseded draft, still the hub's link target |
| `content/index.md:83-88`, `:171` | home hub + diagnostic matrix — link the legacy notes only |
| `content/visualizer.html` | 6 hard-coded Pillar-3 node paths, none for the new folders |
| `content/foundations/stochastic-calculus-and-ito.md` | the only stochastic-calculus "home" today (120 lines) |
| `corpus/pillar3-derivative-pricing.md`, `corpus/titles/pillar3-derivative-pricing.TITLES.md` | the 13-subtopic intended scope |
| `corpus/verified/` (53 files) | Hull 1–37, Shreve I/II, Björk 1–29, Glasserman 1–9, Brigo–Mercurio 1–23, Gatheral, Bergomi, Duffy, Gregory, Haug lookup 1–2 |
| `corpus/handoff/02-PROJECT-STATE-AND-FILEMAP.md` §3b, §5 | build state; "migrate/replace the 6 flat notes" |
| `corpus/handoff/04-NEXT-SESSION-BRIEF.md` | Pillar-3-first plan, lockstep-maintenance requirement |

## Appendix B — Coverage matrix at a glance

```
INTENDED (13)                        FOLDER?   MATERIAL PRESENT?   OWNER
options-fundamentals-and-markets      ✗         fragments           none          <- ADD
no-arbitrage-and-binomial             ✓         yes                 folder
stochastic-calculus-for-pricing       ✗ (P3)    yes (Foundations)   foundations   <- DECIDE
black-scholes-merton                  ✓         yes                 folder
greeks-and-dynamic-hedging            ✗         statics yes         bsm/04        <- FOLD/rename
volatility-surfaces-and-smiles        ✓         yes                 folder
local-vol-and-stochastic-vol          ✗ (split) yes (2 folders)     vs/ + av/     <- write rule
numerical-methods                     ✓         yes                 folder
exotic-and-path-dependent-options     ✓         yes                 folder
american-options-and-optimal-stopping ✗         scattered x3        none          <- ADD (top priority)
interest-rate-and-fixed-income-derivs ✓         yes                 folder
counterparty-risk-and-xva             ✓         yes                 folder
calibration-and-market-practice       ✗         dispersed x3        none          <- ADD
```
