# Builder / Lookup-Perspective Audit — "Can a mid-project practitioner find the exact answer and debug fast?"

**Perspective:** The practitioner using the Atlas as a *lookup tool* and a *debugging service* — job #1 (find + understand quickly) and job #3 (debug from first principles). This is the opposite of the learner path: I know what I need, I just need it **now, exact, and verified**.
**Auditor date:** 2026-09-10. **Scope:** full `content/` tree (97 topic folders across foundations/accounting/8 pillars), home `index.md`, `visualizer.html`, and the Quartz build in `public/`.

**Method.** Every question was answered two ways, as a practitioner would: (a) *index-hop* (home → pillar index → topic hub → sub-page) and (b) *full-text search* (Quartz FlexSearch over `public/static/contentIndex.json`, 7.5 MB, rebuilt today — search is genuinely live on this site). Both paths scored for (i) clicks to answer, (ii) found?, (iii) complete + correct?

---

## 0. TL;DR Verdict

- **Job #1 (lookup) and Job #3 (debug) are the two strongest jobs in the Atlas.** The 97 topic folders are the real product: `index.md` hubs carry **real formula lookup tables with reproduced numeric checks**, and dedicated `05-failure-modes-and-practice.md` pages carry **symptom → broken-assumption → signature → remedy** tables with runnable reproductions. My 6 "hard formula/debug" questions were all answered on the first attempt, in 2–3 clicks, with exact, verified formulas.
- **The killer is the *entry surface*, not the depth.** To hit those superb hubs you must already know the pillar. There is **no glossary, no alphabetical term index, no cross-pillar formula/cheat-sheet index anywhere in `content/`** (0 hits for "glossary"). The only global entry points are (a) free-text search — which returns 100–300 undifferentiated hits for ordinary terms like "Kelly" or "shrinkage" — and (b) a home diagnostic matrix that covers only *8* symptoms. A practitioner who doesn't already know "this is a pillar-5 portfolio topic" is forced into search-triage.
- **Home routes users to the wrong nodes.** The home pillar lists and diagnostic matrix link to the **legacy flat notes** (`.../statistical-arbitrage-and-pairs-trading.md` etc.), while the pillar index pages link to the **new structured folder hubs** (`.../statistical-arbitrage-and-pairs/index.md`). Two parallel, differently-structured copies of 6 topics coexist, with inconsistent section numbering (§4 Failure Modes in legacy vs §5 in new). The lookup tables a power user wants are one extra, non-obvious click away.
- **One real factual error in the home diagnostic matrix** (wrong gamma-P&L formula).
- **Verdict:** GOOD-STRONG on lookup+debug *when you know where to look*; **the missing cross-pillar findability layer (glossary / formula index / expanded symptom matrix) and the home→legacy link routing are the blocking gaps** for the "best lookup guide" ambition.

---

## 1. Question Trace Table

Practitioner questions, scored by the *first* viable attempt (index-hop or search). "First-try" = resolved on the first navigation/search attempt with the need, complete and correct.

| # | Builder question | Path taken (clicks) | Found? | Complete & correct? | Notes / evidence |
|---|---|---|---|---|---|
| 1 | *My pairs-trading backtest Sharpe collapsed out of sample — what's wrong?* | Home diagnostic matrix row 2 → stat-arb **folder** 05-failure-modes (2 clicks) — or home pillar-list → `statistical-arbitrage-and-pairs-trading.md` §4. | ✅ | ✅ Complete | Diagnosis is *multi-cause and ranked*: structural break in cointegration (Chow/CUSUM/Bai–Perron test battery, the injected-I(1) residual algebra), data-snooping in pair selection (expected spurious ADF ≈ −2.88 for M=200), then costs/borrow/crowding (Do–Faff 57% decline). §2.3 even quantifies *why* a −2.9 ADF is expected under the null. A runnable Part A/B reproduction shows both the structural break and the OOS collapse of a data-snooped pair. |
| 2 | *I need the exact Almgren-Chriss optimal trajectory formula.* | Home → pillar 2 index → `optimal-execution-and-almgren-chriss/index.md` §2 lookup table (3 clicks) | ✅ | ✅ Exact | $x_j=X\frac{\sinh(\kappa(T-t_j))}{\sinh(\kappa T)}$, $\kappa=\sqrt{\lambda\sigma^2/\eta}$, plus $E$, $V$, half-life, **TWAP-horizon optimum $T^\star=\sqrt3\,\theta$**, implementation shortfall, nonlinear-impact variant. Every row carries a *re-executed numeric check* (κ=0.6011/day, x(1d)=545,055 held of 10⁶…). "One-sentence essence" boxes give the model in one line. |
| 3 | *How do I compute the deflated Sharpe ratio?* | Home → pillar 1 index → `backtesting-hygiene/index.md` §2 table (3 clicks) | ✅ | ✅ Exact & verified | DSR formula, SR₀ (order-statistic threshold), MinTRL, Harvey–Liu p_M, Bonferroni/Holm, **PBO/CSCV** all in one table; §3 reproduces the canonical Bailey–López de Prado example (DSR=0.8997 at N=100) in stdlib Python. Explicit caveat on the *independent*-trials N (§A.3) and the meaning of DSR<0.95. |
| 4 | *My Kalman filter is diverging.* | Search "diverging" → `signal-processing-and-kalman/05-failure-modes-and-practice.md` (2 clicks, first hit is the failure-modes page) | ✅ | ✅ Complete | Dedicated **divergence** row in the failure-mode table (over-smoothing / over-reacting / divergence / numerical breakdown / misspec / nonlinear), the formal mechanism (covariance becomes a *systematic underestimate*), the **divergence ratio = standardized innovation** $|y_t-Z_t s_{t\mid t-1}|/\sqrt{V_t}$, a 4-step diagnostic battery, and a runnable Q=0 reproduction showing the filter collapsing while reporting near-zero uncertainty. This is exactly the symptom→root-cause→fix a builder needs. |
| 5 | *What's the correct GARCH(1,1) unconditional variance?* | Home → pillar 1 index → `garch-and-volatility-modeling/index.md` §2 table (3 clicks) | ✅ | ✅ Exact | $\operatorname{Var}(a_t)=\alpha_0/(1-\alpha_1-\beta_1)$, with the stationarity condition $\alpha_1+\beta_1<1$ on the adjacent row, persistence, multistep forecast → unconditional, excess-kurtosis formula, IGARCH/EWMA, GJR, EGARCH, HAR-RV, DCC. Unconditional-variance theory (5.0e-05) vs simulation (5.63e-05) shown. |
| 6 | *I need the exact Avellaneda-Stoikov reservation price.* | Home → pillar 6 → `avellaneda-stoikov-and-optimal-quoting/index.md` §2 table (3 clicks) | ✅ | ✅ Exact | $r=s-q\gamma\sigma^2(T-t)$, reservation bid/ask, optimal quote $p^{a}=r+\psi/2$, $p^{b}=r-\psi/2$, stationary spread, **plus the critical scaling caveat** ("paper's spread column is only the k-term; the full spread adds $\gamma\sigma^2(T-t)$" — the single most common lookup error, pre-empted). |
| 7 | *Kelly criterion — what's the optimal fraction f\*? (I don't know which area it lives in.)* | Search "Kelly" (297 hits across ~25 files in 5+ pillars, incl. TWO full treatment locations: foundations/ergodicity/04 and portfolio-opt/kelly-criterion-and-bet-sizing) — **no glossary/term-index tells me the canonical home.** | ⚠️ Found, not *first-try clean* | ✅ content, ❌ findability | Content is excellent (full Kelly folder + the ergodicity treatment), but the term is atomised across both a Foundations area and Pillar 5 with **no cross-linking index of the two treatment sites and no glossary entry** to say "canonical formula live here." First search = 297 ranked hits with no curated pointer. This is the exact scenario a lookup guide must nail, and the Atlas currently relies on free-text search to bridge pillars. |
| 8 | *(Debug sample) Market maker fills 100 consecutive buys right before the crash.* | Home diagnostic matrix row 4 → `adverse-selection-and-glosten-milgrom` hub (1 click from home) | ✅ | ✅ | Matrix row: symptom → "Toxic order flow & adverse selection" → root cause (swept inside-spread passive orders, quote-skewing lag) → link to the A-S/Glosten–Milgrom hub. Confirms the *home diagnostic matrix is a functioning debug entry point* — but it covers only 8 curated rows (see gaps). |

**Scoring: 7 of 8 found on first try (Q7 found but not first-try-clean); all 8 contents complete and correct.** When the entry surface points to the right hub, the answer quality is A-grade: exact formulas, verified numeric checks, runnable reproductions, ranked failure causes.

---

## 2. Lookup-Infrastructure Assessment (job #1)

**What is genuinely strong (measured):**

- **97/97 topic folders** each have the full skeleton `index.md` + `01…06`. (Programmatic count over the tree.)
- **94/97 `index.md` hubs are true lookup pages**, with a title like `"…: Topic Hub & Formula Lookup"`, a real markdown formula **table**, a `Quick-Reference Lookup` block, a **"verified check" column of re-executed numbers**, and §3 runnable code that reproduces them. This is the single best thing in the Atlas for a power user: the answer is at the top of the hub, not buried in a course.
- **The "one-sentence essence" boxed line** on every hub is a genuinely good anti-course pattern — the exact answer before any pedagogy.
- **Search is live.** Quartz FlexSearch is wired (`Component.Search()` in layout) and the index is built today (`public/static/contentIndex.json`, 7.5 MB). The built site has a working search bar over title+content+tags of all ~600+ pages.

**What is weak / missing (measured):**

- **No glossary — anywhere.** `grep -i glossary` in `content/` = **0 hits**. Symbols are massively overloaded across pillars ($\kappa$ = urgency-halflife / $k$ = queue-fill density / $\gamma$ = impact, risk-aversion, skewness…). A single-symbol lookup is impossible without a symbol/term index.
- **No cross-pillar term index / formula cheat-sheet index.** Kelly lives in *both* Foundations (ergodicity) and Pillar 5; shrinkage/RMT lives in Pillar 5 but is referenced in 5+ other pillars; DSR is discussed in Pillar 1 and repeatedly cross-referenced elsewhere. Nothing aggregates "which of the 600 pages is canonical for this term."
- **To use the index-hops you must know the pillar.** Home → pillar index → topic hub is a clean chain *only after you've guessed the pillar*. For a "best lookup guide," the whole-corpus term→page map is the missing layer.
- **3/97 hubs are prose, not tables** (no markdown table): `factor-investing-and-timing`, `fundamental-multi-factor-models`, `adverse-selection-and-glosten-milgrom`. They still contain the formulas (inline display equations) but lose the scanable row/check structure.
- **Home links route to legacy flat notes, not the formula hubs.** The home pillar lists and the diagnostic matrix point to old single-file notes (`backtesting-hygiene-and-deflated-sharpe.md`, `statistical-arbitrage-and-pairs-trading.md`, `signal-processing-and-kalman-filtering.md`, `cross-sectional-and-time-series-momentum.md`, `fundamental-multi-factor-models.md`, `feature-engineering-and-labeling.md`), while the pillar index pages link to the **new folder hubs**. The old notes are thinner (100–135 lines vs 129–169 for the new hubs) and lack the lookup tables and code engines. So the primary navigation surface lands the user one hop short of the best version.

---

## 3. Debug-Job Assessment (job #3)

**Structure present and effective:**

- **Home "First-Principles Diagnostic Matrix"** (8 rows) — a genuine symptom→failure-mode→root-cause→remedy-link table. All 8 remedy links resolve to topic hubs. Verified useful for the "market maker fills before crash" and "pairs spread diverges" traces.
- **Per-topic failure-mode pages:** **88/97** folders carry `05-failure-modes-and-practice.md`. (The 9 without are *all* Foundations math areas — Bayesian, calculus, econometrics, ergodicity, linear algebra, numerical, probability, statistics, stochastic — which use `06-advanced-extensions` instead; arguably fine for pure-math folders, but means a *practitioner debugging a model bug won't find a failure-mode page under pure math*, e.g. GARCH's convergence problems live in the pillar 1 GARCH folder, which is good, but unconditional-var stationarity gotchas also appear in foundations/econometrics §4 with no failure-mode page.)
- **The failure-mode pages are real diagnostic content**, not prose: symptom→broken-assumption→signature→remedy **tables** (Kalman divergence, pairs, DSR/N, GARCH), formal first-principles mechanisms, and **runnable reproductions** of the failure (a Q=0 filter diverging; a data-snooped pair collapsing OOS; a level-shift lags a mis-specified Q). This is precisely job #3.

**Gaps in the debug job:**

- **The home matrix is far too thin for a "diagnostic tool."** 8 curated rows cannot cover the hundreds of failure modes actually documented per-page. A practitioner whose symptom is "my covariance matrix isn't positive-definite," "my Monte Carlo Greeks have correlated errors," "my C++ backtest is non-deterministic," or "my HMM state path flickers" gets *no* home entry and must guess the pillar.
- **`grep -i "diagnostic matrix"`** — the matrix is a markdown table on home only; there is **no standing diagnostic index page**, and each topic's failure-mode table is buried 2–3 clicks down from a page that home doesn't directly link to (see routing issue above).
- **Symptom-language mismatch.** A builder thinks in symptoms ("diverging," "singular covariance," "look-ahead bias," "fill model too optimistic"). The Atlas is organised by *topic*, not *symptom*. The only symptom-language surfaces are the 8-row home matrix and free-text search (which does match symptom words like "diverging" well). No curated symptom→fix lookup exists.
- **Real factual error found — home diagnostic matrix, risk row:** the gamma-P&L given is $\tfrac12 S^4\sigma^4\Gamma^2\Delta t$. The standard daily gamma P&L / gamma–theta relationship is $\tfrac12\Gamma\,\sigma^2 S^2\,\Delta t$ (correct order $\Gamma\cdot\sigma^2$.S^2); the printed form ($S^4\sigma^4\Gamma^2$) is dimensionally and structurally wrong and would mislead a delta-hedger. The linked BSM/Greeks page itself is likely correct — the *matrix summary* is the bug.

---

## 4. Gaps + Proposed Fixes

| # | Gap (with file evidence) | Proposed fix |
|---|---|---|
| G1 | **No glossary / symbol dictionary.** 0 `glossary` hits in `content/`; symbols overloaded across pillars (κ, γ, k, λ, σ). | Create `content/glossary.md`: alphabetical term + symbol → canonical page(s) + one-line formula. Link it from home top nav and each pillar index. This is the #1 missing piece for "find a term without knowing the pillar." |
| G2 | **No cross-pillar formula / term index.** Kelly in 2 places, shrinkage in 6+ pillars, DSR cross-referenced ~30 files; nothing aggregates the canonical page. | Add `content/formula-index.md` (or a `pills`/`api`-style index) grouping "topic → canonical hub URL," seeded automatically from the 94 hub formula tables. Curate the ~600 highest-value formulas. |
| G3 | **Home routes to legacy flat notes, not the new formula hubs.** Home + matrix link `statistical-arbitrage-and-pairs-trading.md` etc.; pillar indexes link the folder hubs. | Repoint every home/pillar-list/matrix link to the folder `index` hubs (e.g. `statistical-arbitrage-and-pairs/index`). Either retire the legacy flat notes or turn them into redirects. Keep §-numbering consistent (new = §5 Failure Modes; legacy = §4). |
| G4 | **Diagnostic matrix too thin (8 rows) for a debug tool.** The real per-page content has 10× more failure modes with no symptom→fix aggregation. | Build `content/diagnostics.md`: machine-merge the `05-failure-modes-and-practice.md` tables (and §4 legacy tables) into one **symptom → cause → fix → page** matrix. Cut off "diverging," "singular covariance," "look-ahead bias," etc. |
| G5 | **3 hubs are prose, not tables** (`factor-investing-and-timing`, `fundamental-multi-factor-models`, `adverse-selection-and-glosten-milgrom`). | Convert their §2 to the row/check-table convention used by the other 94. |
| G6 | **9 Foundations folders lack failure-mode pages** (pure-math areas). | Acceptable for pure math, but add one-line "numerical/practice gotchas" blurb or a pointer to the pillar-1 model folders so a debugging reader isn't stranded. |
| G7 | **Factual error in home matrix risk row** (`$\tfrac12 S^4\sigma^4\Gamma^2\Delta t$`). | Fix to $\tfrac12\Gamma\sigma^2S^2\Delta t$ (gamma–theta relation). |
| G8 | Foundations `_legacy/` and top-level flat `.md` files create duplicate, parallel structures (also present in several pillars) that pollute search hits. | Prune or archive `_legacy/` out of the live index (Quartz `ignorePatterns` already excludes `.obsidian`, not `_legacy`); search noise directly costs lookup time (e.g. "Kelly" → 297 hits partly from `_legacy/`+legacy flat notes). |

---

## 5. Verdict

**GOOD-STRONG, with a blocking findability ceiling.**

- **What wins:** The 94 formula-lookup hubs with verified numeric checks + 88 failure-mode pages with runnable reproductions are the best possible substrate for a lookup+debug tool. When the entry surface lands on the right hub, a mid-project practitioner gets the exact formula (BQ2–6) or a diagnostics-first answer (BQ1, BQ4, BQ8) in 2–3 clicks, first try, correct and verified. **Depth ≥ 9/10.**
- **What costs it the "best lookup guide" title:** the entry layer. No glossary, no cross-pillar term/formula index, a home diagnostic matrix of only 8 rows, home routing that points at the older legacy notes, and three prose-only hubs. A practitioner must know the pillar already or gamble on 100–300 free-text hits. **Findability-for-unknown-location ≈ 4/10.**
- **Priority fixes (in order of payoff):** G3 (repaint home links → folder hubs), G1+G2 (glossary + formula index), G4 (aggregate diagnostic matrix), G7 (fix the formula error), G5 (3 prose hubs), G8 (prune `_legacy`/duplicates).
- **Bottom line:** adds real value on day one for anyone who already found the right pillar — the highest-value single improvement is making the *rest of the corpus* findable from a symptom or term *before* you know the pillar.