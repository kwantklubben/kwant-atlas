# Audit Suite — Index & Results (2026-09-10)

Post-build audit of the whole Atlas, run from seven independent perspectives. Each report
below lives in `corpus/audit/`. Findings were fixed where actionable; the remainder are
listed as recommendations.

## Reports

| Report | Perspective | Verdict |
| :--- | :--- | :--- |
| `spelling-audit.md` | Spelling / typo / term consistency | 10 genuine prose errors (fixed); 50 mixed hyphen/en-dash compound terms (normalised) |
| `math-audit.md` | Math correctness vs verified corpus | 2 confirmed errors + 1 caveat (fixed); everything else reproduces |
| `code-audit.md` | Every embedded Python block run + diffed | 767 blocks; 95.5% byte-exact; 3 non-self-contained + 3 missing-lib (fixed/noted) |
| `learner-perspective-audit.md` | Beginner "from zero" arc | Arc did not close (systemic); fixed — routing, hubs, start-here |
| `builder-lookup-audit.md` | Mid-project lookup + debug jobs | Strong per-node; missing global findability layer (fixed — glossary, diagnostics) |
| `expert-frontier-audit.md` | Expert / frontier depth | 06 level genuinely advanced; frontier gaps named (recommendations) |
| `coherence-audit.md` | Is it one coherent graph? | Coherent core, leaky perimeter; 2 contradictions + visualizer drift fixed |
| `pillar1..8-audit.md`, `foundations-audit.md`, `fundamentals-accounting-audit.md` | Per-area completeness/depth/links/math | All PASS or PASS-with-fixes; fixes applied |

## What was fixed (summary)

**Correctness**
- AC-HJB boxed sign error (Pillar 2); Vasicek/CIR α↔β parameter-role swap + Feller condition
  `2αβ`→`2κθ` (Foundations); generalized-BSM rho `b≠r` caveat (Pillar 3).
- Home-page gamma-loss formula was dimensionally wrong → `½Γ(ΔS)²`.
- Square-root impact exponent mislabel in the P2 hub (`α≈0.6` presented as the sqrt law).
- 3 non-self-contained Python blocks (inline `Phinv`; run-order notes); 3 stale output blocks synced.
- 10 genuine prose typos + 3 doubled words.

**Consistency**
- 50 multi-name compounds normalised to the en-dash house style; `Monte-Carlo`→`Monte Carlo`.
- 96 topic-folder hubs: prerequisite-scope clause ("hub prereqs are for pages 02–06").
- `_legacy/` migration of superseded flat notes in Pillars 2, 3, 5, 6, 8; hubs list canonical folders.

**Navigation / the three jobs**
- Home page: "New here? Start here" 3-step panel; Foundations relabelled as required.
- Foundations hub: consumption-order contract (core trio → per-pillar foundations) + exit ramp.
- Every pillar hub: "Before this pillar (foundations)" line; all 96 topic hubs: prerequisite-scope clause.
- `content/glossary.md` (171 term + symbol entries) and `content/diagnostics.md` (344 symptom→cause→fix
  rows across 9 areas) — the global findability layer the builder audit flagged as missing; both linked
  from the home page and all 10 area hubs.
- Counterparty-risk P3/P4 duplicated folder: mirrored scope notes partition the pricing/desk vs
  risk/regulatory views; quick-lookup tables added to 3 prose-only hubs.

## Outstanding recommendations (not blocking)

1. **Frontier gaps** (from `expert-frontier-audit.md`): Volterra/fractional models, deep hedging /
   BSDEs, signature / rough-path methods; rough Bergomi and LSV are present as forward pointers only.
2. **421 wikilinks still target legacy flat notes** that shadow folder hubs for 19 topics
   (`coherence-audit.md` §4d/§5). Harmless (they resolve) but a reader lands on a superseded
   single page instead of the maintained hub. Retire the flat notes or repoint the links.
3. **Visualizer edges are hardcoded** and can drift from the link graph; consider generating
   nodes/edges from `content/` at build time.
4. **Foundations folders have no `05-failure-modes-and-practice` page** (pure-math areas) —
   acceptable, but a one-line "numerical gotchas" blurb would help a debugging reader.

## Per-topic (one-agent-per-folder) audit — the deep pass

The perspective pass above sampled by theme. A **second, deeper pass assigns one dedicated
agent to EACH of the 97 topic-folders** (whole folder: spelling + math + code + coherence for
its 7 files). Reports land in `corpus/audit/topics/<area>__<folder>.md`.

This caught real errors the perspective pass missed — e.g. a wrong Marchenko–Pastur density
normalization, an ARMA(1,1) variance sign error, a swapped θ-method table, a hierarchical-
shrinkage direction inversion. Progress is tracked below as waves complete.

| Wave | Area | Folders | Status |
| :--- | :--- | :--- | :--- |
| 1 | foundations (8 folders) | bayesian, calculus, econometrics, ergodicity, linear-algebra, numerical-methods, probability, statistics | ✅ done, fixes committed |
| 2 | foundations/stochastic-calculus + fundamentals-accounting (8) | — | ✅ done, fixes committed |
| 3 | pillars/01-quantitative-research (10) | — | ✅ done, fixes committed |
| 4 | pillars/02-algorithmic-hft (9) + pillars/03 black-scholes-merton | — | ✅ done, fixes committed |
| 5 | pillars/03-derivative-pricing (remaining 10) | — | ✅ done, fixes committed |
| 6 | pillars/04-quantitative-risk (1st 4) | var-and-expected-shortfall, parametric-historical-and-monte-carlo-var, extreme-value-theory-and-fat-tails, copulas-and-dependence | ✅ done, fixes committed |
| 7 | pillars/04-quantitative-risk (2nd 4) | credit-risk-and-the-merton-model, stress-testing-and-scenario-analysis, liquidity-risk-and-funding, operational-risk | ✅ done, fixes committed |
| 8 | pillars/04-quantitative-risk (last 4) | model-risk-and-validation, basel-and-regulation, risk-factor-sensitivities, systemic-risk-and-aggregation | ✅ done, fixes committed |
| 9 | pillars/05-portfolio-optimization (1st 4) | modern-portfolio-theory-and-mean-variance, covariance-shrinkage-and-denoising, black-litterman, risk-parity-and-equal-risk-contribution | ✅ done, fixes committed |
| 10 | pillars/05-portfolio-optimization (2nd 4) | hierarchical-risk-parity, robust-optimization, constraints-and-transaction-costs, kelly-criterion-and-bet-sizing | ✅ done, fixes committed |
| 11 | pillars/06-market-making (1st 4) | adverse-selection-and-glosten-milgrom, spread-decomposition-and-roll-model, avellaneda-stoikov-and-optimal-quoting, inventory-management-and-quote-skewing | ✅ done, fixes committed |
| 12 | pillars/06-market-making (2nd 4) | limit-order-book-mechanics, toxic-order-flow-and-vpin, market-impact-and-depth, market-maker-economics-and-rebates | ✅ done, fixes committed |
| 13 | pillars/06 (last 2) + pillars/07 (1st 2) | dealer-banks-and-otc, liquidity-risk-and-asset-pricing, financial-ml-pitfalls-and-low-snr, purged-cross-validation-and-backtest-hygiene | ✅ done, fixes committed |
| 14 | pillars/07-machine-learning-altdata (next 4) | regime-classification-hmm-and-gmm, tree-and-boosting-methods, financial-nlp-and-transcripts, alternative-data-pipelines-and-evaluation | ✅ done, fixes committed |
| 15 | pillars/07 (last 3) + pillars/08 (1st) | deep-learning-for-sequences, reinforcement-learning-for-trading, ml-for-portfolio, high-performance-cpp-for-trading | running |
| 16-17 | pillars/08 (remaining 8) | — | queued |

**Pillar 7 (9 folders) code: 69/69 blocks byte-exact as of wave 14.**

**Pillar 6 (12 folders) is now fully audited and fixed** — 53/53 code blocks byte-exact.

**Pillar 5 (9 folders) is now fully audited and fixed** — 55/55 code blocks byte-exact.

**Pillar 4 (13 folders) is now fully audited and fixed** — 106/106 code blocks byte-exact.

**Pacing:** waves of **4** concurrent agents (one dedicated agent per topic-folder), per instruction.

## Structural check: fence pairing (repo-wide)

Beyond the per-folder audits, a **repo-wide fence-pair check** walks every page, executes each
python block, and compares stdout to the *immediately following* fence. It caught a class of bug
the per-folder pass structurally could not: **12 output fences whose closing backticks were glued
onto the last line of output** (`...nothing lost)\`\`\``), so the fence never closed and the
following prose rendered *inside* the code block. Fixed across 5 black-litterman pages + 1 kelly
page + 6 concurrency pages.

Note on judgement: several Pillar-8 pages intentionally document **timing benchmarks** (numpy vs
loop speedups, allocation ns/op, heap-vs-sorted-list ratios). Those outputs cannot be byte-stable
and are **not** errors — the checker flags them; a human must classify. The rule: a mismatch is
only a defect if the code is deterministic. If the page's fence header says "ms"/"ns/op"/"x", it's
a benchmark.

## How to re-run


- **Code:** extract each ```python block, run with `python3 -c`, diff against the following output fence
  (use a temp *file* for blocks with multiprocessing).
- **Links:** resolve every `[[target]]` against the set of existing `content/**/<name>.md` and
  `<dir>/index.md`; ignore numeric/math literals and inline-code spans (false positives).
- **Build:** `npx quartz build` (fails loudly on a bad YAML title — no backslashes in `title:`).
