# Pillar 1 — Audit: Completeness, Depth & Template, Coherence & Links, Math/Code

**Scope:** `content/pillars/01-quantitative-research/` — the pillar `index.md` hub + **8 topic-folders**, each = `index.md` + `01-from-zero-intuition` … `06-advanced-extensions` = **56 pages** (7 per folder). Plus 6 legacy flat notes retained at the folder root.
**Reference pattern:** `content/pillars/03-derivative-pricing/black-scholes-merton/`.
**Corpus of record:** `corpus/pillar1-quantitative-research.md` + `corpus/titles/pillar1-quantitative-research.TITLES.md`; math cross-checked against `corpus/verified/` (tsay, esl) and the acquired primary sources in `corpus/titles/refs/pillar1/`.
**Auditor method:** every file read and template-checked programmatically (frontmatter/quoting/tag-order/prereq line/section headings); all 59 Python blocks extracted and **executed** against their printed outputs; all 613 in-prose wikilinks resolved against the file tree; ~13 key formulas cross-checked against the verified corpus and primary sources.

---

## 1. COMPLETENESS — does the 8-folder set cover intended Pillar 1 scope?

### Corpus wishlist → folder map

| Corpus section (wishlist) | Pillar-1 folder | Status |
|---|---|---|
| Statistical Arbitrage & Pairs Trading | `statistical-arbitrage-and-pairs` | ✅ covered |
| Momentum — Cross-Sectional & Time-Series (CTA) | `momentum` | ✅ covered |
| Fundamental Multi-Factor Models | `fundamental-multi-factor-models` | ✅ covered |
| Signal Processing & Kalman Filtering | `signal-processing-and-kalman` | ✅ covered |
| Feature Engineering & Labeling | `feature-engineering-and-labeling` | ✅ covered |
| Backtesting Hygiene (DSR, purged CV, snooping) | `backtesting-hygiene` | ✅ covered |
| Event Studies | `event-studies` | ✅ covered |
| Regime Detection | `regime-detection` | ✅ covered |
| Cointegration & Pairs Trading | *(embedded in stat-arb `02-cointegration-and-the-spread`)* | ◑ embedded (acceptable) |
| **Factor Investing & Factor Timing** | — | ❌ **MISSING** (only incidental mentions) |
| **GARCH & Volatility Modeling** | — | ❌ **MISSING** (only passing mentions) |

### Findings

1. **Strong core.** The eight folders map 1:1 onto the eight pillar-1 wishlist sections that are *named as folders* in the corpus, and each is built from first principles. Coverage of the eight chosen topics is complete and deep.
2. **MISSING — GARCH & Volatility Modeling.** The corpus wishlist devotes an entire section to it (Engle 1982, Bollerslev 1986, EGARCH, GJR-GARCH, HAR, Andersen-Bollerslev-Christoffersen-Diebold 2006, Tsay ch. 3 & 10) and lists 7 `SOURCE`/`CITE` items. **No folder covers volatility modelling.** GARCH-family terms appear only in passing (`regime-detection/06-advanced-extensions`, `signal-processing-and-kalman/06`, `event-studies/06`, `momentum/03`) — there is no dedicated volatility-forecasting / conditional-heteroskedasticity folder. Given that (a) vol forecasting underpins risk-scaling in momentum and VaR in Pillar 4, and (b) the wishlist marks it `SOURCE`-tier, this is the single largest gap.
3. **MISSING — Factor Investing & Factor Timing as such.** The corpus has a dedicated section (Ilmanen 2011/2022, Cochrane 2011, McLean & Pontiff 2016) whose thesis — almost all return predictability is time-varying discount-rate predictability, and published anomalies decay post-publication — is a *distinct* topic from static multi-factor *models*. Factor models are well covered (`fundamental-multi-factor-models`), and value–momentum interaction is handled (`momentum/04`), but there is no folder on factor premia/timing/crowding/decay. Recommend either a 9th folder or an explicit note folding these into `fundamental-multi-factor-models/06`.
4. **Cointegration standalone — not needed.** The corpus's "Cointegration & Pairs Trading" section plainly cross-references the stat-arb section ("whose cointegration construction this folder operationalizes") and points to Tsay ch. 8 as HAVE. The stat-arb folder's `02-cointegration-and-the-spread` + `06-advanced-extensions` (Johansen) cover it properly. Treating it as embedded rather than a 9th folder is the *right* call — no awkward overlap introduced.
5. **Market-microstructure alpha — correctly out of scope.** The pillar-1 wishlist does not create a microstructure folder; Hasbrouck is listed only as HAVE *context* for stat-arb spreads and backtests. Microstructure is owned by `02-algorithmic-hft` and `06-market-making`. Its scattered mentions here (execution/liquidity caveats in failure-mode sections) are appropriate cross-pillar bridges, not a gap.
6. **Folder set coherence / overlap.** The 8 folders are mutually distinct: mean-reversion (stat-arb) vs factor/momentum premia (fundamental, momentum) vs methodology/econometrics (event-studies, backtesting, regime-detection) vs adaptive state/ML layer (kalman, feature-engineering). The only near-overlaps are (i) momentum vs fundamental (momentum is a factor — handled by UMD cross-links) and (ii) kalman vs regime-detection (both state-space — handled by the "latent vs observed / time-varying param vs discrete regime" framing). Neither is awkward.

**Completeness verdict:** 8/8 chosen topics complete and correctly bounded; **2 corpus topics absent** (GARCH/volatility modelling; factor investing & timing).

---

## 2. DEPTH & TEMPLATE

### Locked template — per-page checklist
Requirements: (a) YAML frontmatter with **quoted** `title`; (b) `tags:` list whose **first** tag is `pillar-quant-research`; (c) a `**Basic Prerequisites:**` line; (d) exactly six sections in order — `### 1. Intuition & Practical Objective` → `2. Mathematical Ground Truth & Derivations` → `3. Computational Implementation` (Python fence **with** printed-output block) → `4. Failure Modes & First-Principles Breakdowns` → `5. Canonical Literature & Study References` → `6. Connected Graph Bridges`.

| Folder | Files | Quoted title | First tag = pillar-quant-research | Prereq line | All 6 sections, exact headings | Python + output block | **Full pass** |
|---|---|---|---|---|---|---|---|
| statistical-arbitrage-and-pairs | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| backtesting-hygiene | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| fundamental-multi-factor-models | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| momentum | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| signal-processing-and-kalman | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| feature-engineering-and-labeling | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| event-studies | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| regime-detection | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| **TOTAL** | **56** | **56/56** | **56/56** | **56/56** | **56/56** | **56/56** | **56/56** |

**Template verdict: PASS 56/56 (strict).** Zero heading deviations, zero unquoted titles, zero missing prerequisite lines, zero first-tag errors. Every page — including every `index.md` and every `06-advanced-extensions.md` — carries a runnable stdlib-only Python block **with** a printed-output block.

**One stylistic deviation (cosmetic, all 7 pages of one folder):** `fundamental-multi-factor-models/*.md` fences its output blocks as ` ```text ` where the template (and every other folder, and the BSM reference) uses a bare ` ``` ` fence. Output content is present and correct; only the fence language tag differs. One-line fix per page if strict uniformity is wanted.

### Depth per folder (read + size proxy)

| Folder | Lines | Words | Py blocks | Depth rating |
|---|---|---|---|---|
| statistical-arbitrage-and-pairs | 1,130 | 12,876 | 8 | **Deep** |
| backtesting-hygiene | 965 | 11,524 | 7 | **Deep** |
| fundamental-multi-factor-models | 923 | 11,047 | 7 | **Adequate→Deep** |
| momentum | 893 | 10,586 | 7 | **Adequate** |
| signal-processing-and-kalman | 1,045 | 12,597 | 7 | **Deep** |
| feature-engineering-and-labeling | 1,013 | 12,951 | 7 | **Deep** |
| event-studies | 855 | 9,785 | 7 | **Adequate** (shallowest) |
| regime-detection | 1,055 | 12,723 | 9 | **Deep** |
| **TOTAL** | **7,879** | **94,089** | **59** | — |

- **statistical-arbitrage-and-pairs — Deep.** Full pipeline: intuition → Engle-Granger two-step + ECM + OU spread → pairs selection/hedge → trading rules/backtest → failure modes → Johansen. Recovers a **known** simulated OU truth (β̂=0.9955 vs 1.0, θ̂=0.199 vs 0.20, half-life 3.48 vs 3.47 d) — a strong verification pattern.
- **backtesting-hygiene — Deep.** The winner's-curse → multiple-testing → DSR → purged CV arc is complete; DSR page reproduces the canonical Bailey-LdP worked example (N=46 crossing at DSR=0.950).
- **fundamental-multi-factor-models — Adequate→Deep.** FF3/FF5 regression, factor construction (2×3 sorts), Fama-MacBeth cross-section, factor zoo. Slightly below the pillar average in words (smallest of the deep tier).
- **momentum — Adequate.** XSMOM ranking engine, TSMOM, value-momentum interaction, crashes. Solid but the thinnest math density of the factor group (smallest folder).
- **signal-processing-and-kalman — Deep.** State-space → Kalman recursion → time-varying beta → failure modes → smoothing/particle filters. Matrix KF cross-checked against the scalar recursion to 3.5e-12.
- **feature-engineering-and-labeling — Deep.** Fixed-horizon flaws → feature construction → target labeling → triple-barrier/meta-labeling → failure modes → fractional differentiation. Meta-labeling page is a controlled, reproducible precision/recall experiment.
- **event-studies — Adequate (shallowest).** Methodology → AR/CAR → testing → failure modes → extensions. Correct and well-sourced, but the smallest folder (855 lines / 9.8k words) and the one with the output-mismatch defect (§4 below).
- **regime-detection — Deep.** Markov-switching (Hamilton filter, EM) → threshold (SETAR/STAR) → HMM → failure modes → extensions. Only folder with more than one Python block per page in places; highest py-block count (9).

### Audience arc (beginner → expert)
Served in every folder via the locked `01`→`06` progression (`01` = "no prior knowledge needed", `06` = expert/O-something extensions), and reinforced by each `index.md`'s explicit "Recommended reading route". The **pillar hub** `index.md` adds a 3-stage route (Start → Intermediate → Expert) across the eight folders. Arc is coherent and complete.

---

## 3. COHERENCE & LINKS

- **Pillar coherence: PASS.** The eight topics cohere as one pillar under the hub's "Quantitative Alpha Lifecycle" mermaid diagram (hypothesis → data → features → model → purged backtest/DSR → execution → allocation → decay). Cross-folder bridges are explicit and bidirectional in every `06`/`05` page.
- **Hub completeness: PASS.** `pillars/01-quantitative-research/index.md` lists **all 8** folders with one-line descriptions, a **3-stage reading path**, the lifecycle diagram, and correctly retains the 6 legacy flat notes under "Original Notes".
- **Wikilinks: PASS — 0 broken.** All **613** in-prose wikilinks (code fences and inline code excluded) resolve to existing targets. No dangling links to non-existent folders. (An initial naive scan flagged 9 "broken" links that were all Python list literals such as `[[1.0, z[i]]]` and `[[se2]]` inside code fences — false positives, not real links.)
- **Reference-pattern parity.** Each pillar-1 folder has the same 7-file shape as `black-scholes-merton/` (index + 6 sub-pages) with identical section structure.

---

## 4. MATH / CODE

### 4a. Python execution — 59 blocks extracted, executed, outputs compared

| Result | Count |
|---|---|
| Blocks extracted (all with printed-output blocks) | 59 |
| Ran successfully, output **matches exactly** | 57 |
| Ran successfully, output **MISMATCH** | **1** (real defect) |
| Slow but **correct** (exceeded a 60 s cap; verified on a longer run) | 1 |

**Defect D1 — stale output block (reproducible mismatch).**
`content/pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car.md`
**Code fence:** line 52. **Output fence:** lines 78–94. **Prose citing the stale numbers:** lines 91, 96.
The code uses `random.seed(23)` and is fully deterministic, yet its output does **not** match the printed block. Re-running the block twice gives identical results differing from the document:

| Quantity | Printed in doc | Actual code output |
|---|---|---|
| day-0 AR_t | `+1.454%` | `+1.482%` |
| CAR(-1,+1) | `+2.372%  t=+4.62` | `+1.930%  t=+3.54` |
| CAR(0,+1) | `+1.925%  t=+4.59` | `+1.973%  t=+4.43` |
| s(AR_t) est. window | `0.297%` | `0.315%` |

The narrative in §3 ("a decisive +4.62", "the day-0 mean … +1.45%") quotes the **stale** block, so the prose currently misstates its own code's output. The signal is still significant (t=+3.54) either way, but the numbers must be regenerated (or the seed restored) so code, output, and prose agree. **Only genuine code defect in the pillar.**

**Non-defect — `backtesting-hygiene/01-from-zero-intuition.md` (code fence line 53).** Timed out under a 60 s cap (the inner Monte-Carlo is O(reps·N·T) ≈ 3×10⁸ `gauss` draws at N=1000), but on a longer run (≈74 s) completes and its output **matches the printed block exactly** (best-win-rates 0.700/0.850/0.552; MC best SR 0.020/0.885/1.453/1.889 vs theory 0.000/0.909/1.461/1.879). Correct — just slow; consider trimming `reps` or N if CI time matters.

All remaining 57 blocks ran stdlib-only (two Kalman pages import `numpy`, available in this environment, and both ran clean and matched).

### 4b. Formula spot-checks (~13) against verified corpus / primary sources

| # | Where | Claim | Source | Verdict |
|---|---|---|---|---|
| 1 | stat-arb `02` §2.1 | Engle–Granger ECM, `∇x_t=αβ'x_{t-1}+…` (Tsay Eq. 8.33) | `verified/tsay_ch7-9.md:59` | ✅ exact |
| 2 | stat-arb `02` §2.1 | ADF on residual; EG 5% CV ≈ −3.34, not −2.86 | Engle-Granger 1987 / MacKinnon; Tsay §8.6 | ✅ correct |
| 3 | stat-arb `02` §2.2 | ECM `α1`,`α2` opposite sign (Tsay Eq. 8.45) | `verified/tsay_ch7-9.md:66` | ✅ correct |
| 4 | stat-arb `02` §2.3 | OU stationary variance `σ²/(2θ)` | Avellaneda-Lee 2010 Eq. (14) | ✅ exact |
| 5 | stat-arb `02` §2.3 | half-life `τ½ = ln2/θ` | Tsay Ch 2 (`ℓ=ln0.5/ln|φ|`) | ✅ exact |
| 6 | stat-arb `02` §2.3 | Avellaneda-Lee `κ=−log(b)·252`, filter `κ>252/30` ⇒ `b<0.9672` | Avellaneda-Lee 2010 §3 | ✅ exact |
| 7 | backtesting `04` §2 | DSR: `SR0=√V·E[max]`, PSR variance `(1−γ3·SR+(γ4−1)/4·SR²)/(T−1)` | Bailey-LdP 2014 | ✅ exact; code reproduces N=46→0.950 |
| 8 | fundamental `02` §2.1 | FF3 regression, `β̂=(X'X)⁻¹X'y`; code recovers true betas | FF 1993; ESL Ch 3 | ✅ stdlib OLS runs, recovers 1.209/0.585/−0.457 |
| 9 | momentum `02` §2 | XSMOM decomposition `E[r^XS]=tr(Ω)/N − 1'Ω1/N² + 12σ²_m` | MOP 2012 Eq. (6) | ✅ **exact** (verbatim match to source text) |
| 10 | kalman `03` §2.1 | Kalman recursion (Tsay Eq. 11.64), `L_t=T_t−K_tZ_t` | `verified/tsay_ch10-12.md:38` | ✅ exact |
| 11 | kalman `03` §2.3 | scalar local-level gain/update | Tsay Eq. 11.14 | ✅ correct; matrix↔scalar agree to 3.5e-12 |
| 12 | feature `04` §2 | triple-barrier oriented barriers; meta-label {0,1}; precision/recall/F1 | LdP AFML §3.6–3.7 | ✅ correct |
| 13 | regime `02` §2 | Hamilton filter; `π0=(1−P11)/(2−P00−P11)`; durations 3.7/11.3 qtrs | Hamilton 1989; `verified/tsay_ch4-6.md:22` | ✅ exact (Tsay: 3.69/11.31) |
| 14 | regime `03` §1 | SETAR ergodicity `φ¹·φ²<1`; threshold grid search; **3-regime** threshold-cointegration thresholds −0.0226/0.0377 | Tsay Ch 4, §8.7 | ✅ **correctly gives two thresholds** — avoids the 2-vs-3-regime error the corpus flagged elsewhere |

**No math error, wrong formula, or unit error found.** All ~13 spot-checks agree with the verified corpus / primary sources.

**Minor documentation wrinkle (not a numeric error):** `stat-arb/02` §2.3 packs two different coefficients under the symbol `b`: the derivation states the AR(1) coefficient `b=e^{−θΔt}` (which would imply `θ=−ln(b)/Δt`), then boxes `θ=−ln(1+b)/Δt` labelled "(Euler approx)". The boxed form is the **correct exact** relation for the *Δz-regression* slope coefficient used in the code (`bc[1]=φ−1`), and the code's numbers are right (θ̂=0.199, half-life 3.48). Recommend disambiguating the notation (e.g. use `φ` for the AR coefficient and `b` for the Δ-regression slope) and dropping the "Euler approx" label, which is inaccurate for an exact-discretisation relation.

---

## 5. Summary

| Dimension | Verdict |
|---|---|
| **Completeness** | 8/8 chosen topics complete & well-bounded; **2 corpus topics missing** (GARCH/volatility modelling; factor investing & timing); cointegration correctly embedded; microstructure correctly out of scope. |
| **Depth & Template** | **Template PASS 56/56 (strict).** Depth: 5 Deep, 3 Adequate(→Deep). Audience arc served. One cosmetic deviation (```text output fences in `fundamental-multi-factor-models`, 7 pages). |
| **Coherence & Links** | **PASS.** 613/613 wikilinks resolve; hub lists all 8 folders with a 3-stage reading path; pillar coheres. |
| **Math / Code** | **1 real defect** (stale output in `event-studies/03`, code+prose disagree). 57/57 other executed blocks match; 1 slow-but-correct. ~13 formula spot-checks all correct. |

**Actionable fixes (priority order):**
1. **P1 —** Regenerate/repair the output block in `event-studies/03-abnormal-returns-and-car.md` (lines 78–94) and align the §3 prose (lines 91, 96) with the code's actual output (seed 23 → t=+3.54, day-0 +1.482%). *(Only concrete code defect.)*
2. **P2 —** Add a **GARCH & Volatility Modeling** folder (or an explicit sub-folder note) — the largest missing corpus topic, `SOURCE`-tier in the wishlist.
3. **P2 —** Cover **factor investing & timing** (Ilmanen, Cochrane, McLean-Pontiff) — new folder or fold into `fundamental-multi-factor-models/06`.
4. **P3 —** Normalise the output-fence language tag in `fundamental-multi-factor-models/*.md` (```text → bare ```) for template uniformity.
5. **P3 —** Disambiguate the `b` notation in `stat-arb/02` §2.3 and drop the "Euler approx" label.
6. **P3 —** Trim the Monte-Carlo size in `backtesting-hygiene/01` (fence line 53) so it runs in <60 s.
