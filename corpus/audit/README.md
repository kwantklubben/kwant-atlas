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
- Every pillar hub: "Before this pillar (foundations)" line.
- `content/glossary.md` (term + symbol index) and `content/diagnostics.md` (global symptom→cause→fix).

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

## How to re-run

- **Code:** extract each ```python block, run with `python3 -c`, diff against the following output fence
  (use a temp *file* for blocks with multiprocessing).
- **Links:** resolve every `[[target]]` against the set of existing `content/**/<name>.md` and
  `<dir>/index.md`; ignore numeric/math literals and inline-code spans (false positives).
- **Build:** `npx quartz build` (fails loudly on a bad YAML title — no backslashes in `title:`).
