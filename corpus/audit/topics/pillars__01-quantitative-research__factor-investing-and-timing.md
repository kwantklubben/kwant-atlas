# Audit Report — `pillars/01-quantitative-research/factor-investing-and-timing/`

- **Folder:** content/pillars/01-quantitative-research/factor-investing-and-timing/ (7 files)
- **Date:** 2026-09-10
- **Reviewer:** sole adversarial subagent
- **Scope:** spelling/typo (prose), math (boxed formulas + worked examples + cited numbers), code (all ```python blocks run and diffed), coherence (hub vs 01 prereq, jargon, links, contradictions)
- **Note:** content/_legacy ignored per instructions.

## Files checked (7)
index.md, 01-from-zero-intuition.md, 02-the-factor-zoo.md, 03-factor-crowding-and-capacity.md, 04-post-publication-decay.md, 05-failure-modes-and-practice.md, 06-advanced-extensions.md

## Code — 12/12 blocks reproduce their documented output fences EXACTLY (PASS)
Ran every ```python block (stdlib only) with the repo's python3; output diffed char-for-char against the documented output fence. All matched:
- index b1; 01 b1; 02 b1,b2; 03 b1,b2; 04 b1,b2; 05 b1,b2; 06 b1,b2
- Distinctive reproduced values: LS Sharpe 2.05 / IC 0.045 / Grinold 2.69 (01); Bonferroni 3.76 (02); break-even $630bn, one-way impact 10.0/3.2 bps (03); 14.8%/34.2% decay, 1176 months, cheap-vs-costly +32.2pp t=2.42 (04); IR table 0.28–1.50 (05); timing ICs 0.162/0.213, selection trap +0.32→+0.07 (06). No code errors.

## Citations verified against corpus PDF — PASS
`corpus/titles/refs/32_mclean_2016_does_academic_research_destroy.pdf` (pdftotext, authoritative cited source) confirms, verbatim/near:
- "out-of-sample decay … about 10%, but not statistically different from zero"; "post-publication decay … about 35%"; "statistically different from both 0% and 100%" (abstract).
- "an in-sample alpha of 5% is expected to decay to 3.25% post-publication"; "lower bound on the publication effect of about 25%" (line ~228–232).
- pooled t-statistic = −4.91 (01/04's "t≈−4.9" ✓).
- "82 different characteristics from 68 different studies" (04's "82 characteristics from 68 studies" ✓).
- "replicate 72 of the characteristics in-sample; for 10 … could not find statistically significant return predictability"; Fama–MacBeth cut-off |t|=1.50 (04's "t>1.50", "10 of 82" ✓).
- "a linear decay in predictability during the post-publication months" (04 ✓).
- higher post-publication volume/variance/short interest; greater declines for low-idiosyncratic-risk stocks; Jegadeesh & Titman momentum-increases-after-publication counter-example all present (04 ✓).

## Math — verified vs re-derived / vs formulas
Verified CORRECT: Grinold law IR=IC√breadth (01:51, 2.7; index:52, 0.17); 0.5/√12≈0.14 timing IC (01:54, 05:51, 06:49); false-discovery 300×0.0455=13.7 & Bonferroni z=3.76 (02:37,40); t≈2.07 (0.004/0.03·√240) (02:122); correlated-bets law σ_port=σ√(ρ+(1−ρ)/N) and IR`port`=IR1·√(N/(1+(N−1)ρ)) incl. ρ→0/1 limits (05:36–38; index:37); g`net` formula and A*∝g² capacity (03:40,44; code g=0.02→≈$160bn); decay power T*=(2σ/(αd))²=1176mo≈98yr (04:52); half-life ln2/λ (05:45); arcsin IC 51.4% (01:101); timing Grinold IRs 0.56/0.74 (06:96/105); 76/300 decile +1.75 s.d. spread geometry (01:95). MP decay math (10%/35%) correct. All numbers internally consistent EXCEPT the findings below.

## FINDINGS — errors

### HARD MATH ERRORS
- **[ERROR] 01-from-zero-intuition.md:51** — Stated: "IR≈2.7 — close to the **1.97** measured in §3". Correct: §3's own output (01:84 & 92) and prose (01:95) measure **2.05**; the "1.97" appears nowhere in the code output. Internal contradiction.
- **[ERROR] 03-factor-crowding-and-capacity.md:45** — Stated: "Capacity scales as **1/τ²**. A 4× higher-turnover version of the same factor has **16× less capacity**." Correct: from the folder's OWN boxed formulas — g`net`(A)=g−τ·2λσ·√(Aτ/(252·ADV)) (03:40) and the index's own break-even A*=(252·ADV/turn)·[g/(2·turn·λσ)]² (index:40) — the break-even is **A* ∝ 1/τ³**, so 4× turnover → **64× less capacity**, not 16×. Verified numerically: TURN=2→$630bn, TURN=8→$9.84bn (ratio exactly 64.0×). The τ² claim contradicts the formula on the same page.
- **[ERROR] index.md:39** — Stated: publication-decay lookup "OOS ≈ **58% of in-sample**". No such statistic exists: the corpus MP paper reports OOS decay ≈10% (⇒ survival ≈90%), and folder 04 (its own simulation: OOS survival 0.852) is consistent with ~90%. "58%" matches neither MP, nor 04, nor post-publication survival (65%/66%). Unsupported, internally inconsistent number.

### MINOR (numeric / precision / presentation)
- **[MINOR] 06-advanced-extensions.md:105** — "real … timing ICs … 0.03–0.08 … correspond to **Sharpe improvements of a few hundredths**". Correct: IC·√12 gives IR ≈ **0.10–0.28** (tenths, not hundredths — order-of-magnitude understatement).
- **[MINOR] 01-from-zero-intuition.md:95** — "0.003×3.51=1.05%/mo is **exactly** what the simulation delivers." Simulation delivers **+1.004%/mo**; 1.05% is the analytic value (≈, not exactly).
- **[MINOR/COHERENCE] index.md:41** — lookup lists factor-timing IC "≈0.16 (val) / 0.21 (trend)" without caveat; 06:105 explicitly labels these "implausibly strong… chosen so the mechanism is visible" and states REAL timing ICs are 0.03–0.08. Hub value shown without the disclaiming context could mislead a lookup reader.
- **[MINOR/INFO] 02-the-factor-zoo.md:51** — "best of m=1000 null backtests looks like a Sharpe of order 2–3 by construction." Formula given (√(2·ln m)) yields `√(2·ln 1000)=3.72` — "2–3" slightly understates the 3.7 sigmas (informational; the boxed formula is correct).

## Spelling — PASS
All prose run through hunspell (en_US); every flag is a proper noun (Cochrane, Grinold, Ilmanen, McLean, Fama…), a field term (mispricing, premia, backtest, decile, drawdowns, counterparty…), a British spelling used consistently (behavioural, realised, programme, artefact, catalogue(d)), or a LaTeX-extraction artifact. No genuine spelling/typo errors in prose.

## Links / coherence — PASS
- All 103 wikilink targets resolve (verified against content/ root; 0 broken). In-folder 01↔06 forward/back pointers, hub prereq note (index:11 "prereqs are for 02–06; 01 states its own" — consistent with 01:11), and 04→06 "Factor Timing" title all agree.
- Minor presentation note only: index table presents the multi-testing/IC/timing law and capacity correctly; the two table cells flagged above (index:39, index:41) are the only hub-lookup imperfections.

---

## Summary
- **Verdict:** PASS with corrections (code fully correct; cited MP statistics and formulas largely verified against the corpus paper; 3 hard math errors + 4 minor/clarification items, all fixes mechanical).
- **Total findings:** 7 (3 hard math errors, 4 minor).
- **blocks_run:** 12 (all reproduced documented output exactly).