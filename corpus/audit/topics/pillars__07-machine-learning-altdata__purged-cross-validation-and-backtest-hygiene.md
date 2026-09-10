# Audit — pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/

**Date:** 2026-09-10 · **Auditor:** sole adversarial reviewer · **Files checked:** 7/7

## Verdict

**PASS with minor issues.** Every boxed formula and the worked examples (purge
overlap rule, embargo, combinatorial split counter $\binom{N}{k}$, number of
backtest paths $\varphi[N,k]$, train fraction $\theta=1-k/N$, max-paths limit,
CPCV variance formula $\sigma^2[\mu_i]$, walk-forward average training points)
are correct as transcribed and are numerically reproduced by the in-page code.
All **9** Python blocks were extracted (3 stdlib-only, no imports beyond
`random`/`math`/`itertools`) and re-executed under Python 3.14.7; **9/9 reproduce
their documented output fences byte-for-byte.**

Found **4 errors** (2 substantive, 2 minor): one prose/table numeric mismatch on
page 03, one false asymptotic claim in the CPCV variance discussion (page 04),
one grammar break (page 04), one section-citation inconsistency (index vs
pages 04/05/06). Coherence is otherwise strong — prereq chain acyclic, hub ↔
sub-pages consistent, all wikilinks resolve.

---

## 1. Spelling / typos (prose)

All prose was stripped of code fences, inline code, `$…$`/`$$…$$`, wikilinks and
URLs, then spell-checked with `pyspellchecker` plus a curated common-typo list
(teh, recieve, seperate, occured, …). Remaining "unknown" tokens were all
technical or hyphenated coinages (`CPCV`, `AFML`, `PurgedKFold`, `near-duplicate`,
`walk-forward`, `off-diagonal`, `non-stationarity`, …). **No misspellings, no
doubled words, no stray punctuation artifacts found.**

## 2. Mathematics — every boxed formula + worked example verified

All formulas independently re-derived; the corpus cross-check is
`corpus/verified/esl_ch6-10.md:44–45` (ESL eq. 7.48, §7.10.2 "3% vs true 50%")
and the book TOC (Wiley) for chapter/section attributions. Confirmations:

- **Purge overlap rule** — three sufficient conditions + interval-intersection
  form `t_{i,0}≤t_{j,1} ∧ t_{j,0}≤t_{i,1}` (index:31, 01:46, 03:31–37) — correct
  and *complete*: if neither endpoint of $I$ lies in $J$, the intervals are
  disjoint or $J\subseteq I$, so the three cases exhaust overlap. ✓
- **Embargo** `Y_j=f[t_{j,0},\,t_{j,1}+h]`, `h≈0.01T`: $10/1000=1\%$ ✓
  (index:32, 03:43).
- **Splits** $\binom{N}{k}=\prod_{i=0}^{k-1}(N-i)/k!$; $N{=}6,k{=}2\Rightarrow15$ ✓
  (index:33, 04:28).
- **Paths** $\varphi[N,k]=\tfrac{k}{N}\binom{N}{k}=\prod_{i=1}^{k-1}\frac{N-i}{(k-1)!}$
  — algebra verifies $\tfrac{k}{N}\binom{N}{k}=\binom{N-1}{k-1}=\prod_{i=1}^{k-1}(N-i)/(k-1)!$;
  $\varphi[6,2]{=}5$, $\varphi[6,3]{=}10$, $\varphi[101,2]{=}100$ ✓ (index:34, 04:34).
- **Uniform membership** — each group is in exactly $\binom{N-1}{k-1}=\varphi$ test
  sets (04:32; code confirms all five $N{=}6,k{=}2$ groups appear 5×). ✓
- **Train fraction** $\theta=1-k/N$; $N{=}10,k{=}2\Rightarrow0.80$ ✓ (index:35).
- **Max paths** $\varphi_{\max}=\tfrac12\binom{T}{T/2}$; $T{=}30\Rightarrow77\,558\,760$
  (½·155 117 520) ✓ (index:36, 04:41).
- **CPCV variance** $\sigma^2[\mu_i]=\varphi^{-1}\sigma_i^2[1+(\varphi-1)\bar\rho_i]$
  — correct (variance of the mean of $\varphi$ equicorrelated estimators);
  $\bar\rho{=}0.3,\sigma_i^2{=}1$: $\varphi{=}1\Rightarrow1.0$, $\varphi{=}2\Rightarrow0.65$,
  $\varphi{=}10\Rightarrow0.37$, $\varphi{=}100\Rightarrow0.3070$ ✓ (index:37, 04:45,
  05:37, 06:39). Sanity $\varphi^{-1}\sigma_i^2\le\sigma^2[\mu_i]<\sigma_i^2$ holds for
  $\varphi>1$ ✓ (see error 2 for the false limit that follows it).
- **Walk-forward average training points**
  $\frac1{T-t_0}\sum_{\tau=t_0+1}^{T}(\tau-1)$; $T{=}100$, $t_0{=}10/20/40\Rightarrow
  54.5/59.5/69.5$ ✓ (06:31, code).
- **Sample loss** $(2h_{label}+h)/T$: $h_{label}{=}20,h{=}10,T{=}1000\Rightarrow5\%$
  vs code 4.9% ✓ (03:45, 05:31).
- **Sheppard sign-agreement** $\mathrm{P}(y_t{=}y_{t+1})=\tfrac12+\tfrac1\pi\arcsin\rho$
  with $\rho=(h-1)/h$ (01:38–40) — correct; simulated $h{=}10\Rightarrow0.858$ vs
  closed form $0.856$ ✓.
- **ESL** $k$-fold eq. 7.48 and the wrong-vs-right §7.10.2 "3% vs true 50%"
  (index:122, 02:98) — matches corpus (`esl_ch6-10.md:44–45`). ✓
- **Chapter/section attributions** — AFML Ch. 7 "Cross-Validation in Finance"
  (7.4.1 purging, 7.4.2 embargo, 7.5 sklearn bugs) and Ch. 12 "Backtesting
  through Cross-Validation" (12.2 WF, 12.3 CV, 12.4.1 splits, 12.4.2 algorithm,
  12.4.3 examples, **12.5** "How CPCV Addresses Backtest Overfitting") all match
  the published TOC. ✓ (see error 4 for the one citation slip).

## 3. Code — execution audit

Extracted **every** ```python block (9 total) and re-ran each with
`python3` 3.14.7, diffing stdout against the following live output fence.

| File | Line | Block | stdout == fence |
|---|---|---|---|
| 01-from-zero-intuition.md | 56 | label agreement vs horizon $h$ | ✅ exact |
| 02-why-standard-cv-fails.md | 41 | nearest-in-time label leakage vs fold thickness | ✅ exact |
| 03-purging-and-embargo.md | 53 | per-fold purge/embargo bookkeeping | ✅ exact |
| 04-combinatorial-purged-cv.md | 59 | split + path counters | ✅ exact |
| 05-failure-modes-and-practice.md | 51 | sample loss vs label horizon | ✅ exact |
| 05-failure-modes-and-practice.md | 81 | single-path vs CPCV variance | ✅ exact |
| 06-advanced-extensions.md | 55 | walk-forward warm-up average | ✅ exact |
| 06-advanced-extensions.md | 77 | CPCV variance table $\rho\in\{0,0.3,0.8\}$ | ✅ exact |
| index.md | 47 | leakage signature + CPCV path counter | ✅ exact |

**Blocks run: 9/9 — 9/9 exact stdout match.** Seed-fixed Monte Carlo
(`random.Random`) reproduces byte-for-byte, e.g. 01 ⇒ 0.501/0.669/0.795/0.858/
0.900/0.933; 02 ⇒ standard 0.451→0.854 (blocks 478/40/5/1) with purged pinned at
0.426–0.535; 04 ⇒ $\varphi[6,2]{=}5,\varphi[6,3]{=}10,\varphi[101,2]{=}100$.
(Note: index's demo uses a different, shorter fold list — `(N//5, 20, 1)` — than
02's `(N//5, 40, 5, 1)`; both are internally self-consistent and both reproduce,
so this is a benign duplication, not an error.)

## 4. Coherence — hub vs sub-pages, jargon, links

- **Hub ↔ 01 prereq:** index:11 marks the *folder-level* prereqs (Probability &
  Measure Theory + Backtesting Hygiene) as applying to pages 02–06 and explicitly
  defers page 01's own smaller requirement to 01 itself; 01:10 states exactly that
  (Backtesting Hygiene only). **Consistent, acyclic.**
- **Prereq chain:** 02←01, 03←02, 04←03, 05←04, 06←04+05. Linear, no cycles. ✓
- **Cross-page numbers:** hub §4's signposts agree with the sub-page lists
  (leakage §02, sample loss §05, single-path §04, missing-$N$ §05/06); the
  $11\%$@$h{=}50$ figure is consistent between index:111 and 05:77,105. ✓
- **Wikilinks:** every target resolves —
  `foundations/probability-and-measure-theory/index`,
  `pillars/01-quantitative-research/{backtesting-hygiene,feature-engineering-and-labeling}/index`,
  `pillars/07-machine-learning-altdata/{tree-based-factor-ranking-and-purged-cv,
  financial-ml-pitfalls-and-low-snr/index}`, and all six in-folder pages. ✓
- **Jargon:** CPCV, DSR, WF, DSR expanded at first substantive use. Minor: `PBO`
  (index:11) and `CSCV` (index:120) are used before being spelled out
  ("The Probability of Backtest Overfitting" / CSCV-PBO) in §5.

---

## Errors found (file:line — stated → correct)

1. **[substantive, numeric prose/table mismatch]** `03-purging-and-embargo.md:89` —
   "Folds 1–4 each purge $\approx38$ overlapping training labels and embargo $10$."
   The file's own printed table (03:81–85) shows fold 1 purge = **19**, folds 2–4 =
   38, fold 5 = **20**. Correct statement: folds **2–4** purge $\approx38$; the
   first fold purges only 19 (its test block is at the start of the sample, so
   nothing precedes it to overlap) and the last fold 20. The companion sentence
   "The purge is symmetric (labels before *and* after the test block overlap it)"
   likewise holds only for the interior folds 2–4.
2. **[substantive, math/false limit]** `04-combinatorial-purged-cv.md:51` —
   "$\sigma^2[\mu_i]\to0$ as $\varphi\to\infty$". With fixed $\bar\rho_i>0$ the
   limit is $\sigma_i^2\bar\rho_i$, not 0 (since
   $\sigma^2[\mu_i]=\sigma_i^2(\bar\rho_i+(1-\bar\rho_i)/\varphi)$). This also
   contradicts the page's own sandwich two lines above and page 06:93
   ("with highly correlated paths ($\bar\rho=0.8$) … variance barely falls below
   $0.8$"). Correct: $\sigma^2[\mu_i]\to\bar\rho_i\,\sigma_i^2$; it tends to 0 only
   in the independent-path case $\bar\rho_i=0$.
3. **[grammar]** `04-combinatorial-purged-cv.md:57` — "…the general counters, and
   the **verify that** every group is tested in exactly $\varphi$ paths." Broken
   clause; should be "…and **verifies that** every group…" (or "…and the **check
   that**…").
4. **[consistency, section citation]** `index.md:119` attributes "the variance
   formula" to **§12.4**, while `04:122`, `05:114` and `06:107` all attribute it to
   **§12.5**. Per the book TOC the variance/overfitting discussion lives in §12.5
   ("How Combinatorial Purged Cross-Validation Addresses Backtest Overfitting") and
   §12.4 is the method itself; the index should cite §12.5 for the variance formula.

*Minor, not counted:* `index.md:11` and `index.md:120` use the acronyms **PBO** and
**CSCV** before expanding them (spelled out only in §5's reference line) — the hub
should expand on first use. `04:57` "the book's headline numbers" is fine. The
index §3 demo duplicating a shortened version of 02's leakage experiment is benign.

## Summary

- Formulas/examples: **correct** (purge, embargo, splits, paths, $\theta$,
  max-paths, CPCV variance, WF-average, Sheppard, ESL 7.48 / §7.10.2).
- Code: **9/9 blocks run, 9/9 exact stdout match.**
- Defects: **4** (1 prose/table numeric mismatch, 1 false asymptotic claim,
  1 grammar break, 1 section-citation inconsistency).
- No broken wikilinks; prereq chain and hub/sub-page coverage coherent.
