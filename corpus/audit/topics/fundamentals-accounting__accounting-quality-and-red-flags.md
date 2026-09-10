# Audit: `content/fundamentals-accounting/accounting-quality-and-red-flags/`

**Sole reviewer, adversarial pass.** Folder = 7 files (index hub + 6 sub-pages). Scope: spelling/typos in prose (exclude code/LaTeX), math (every boxed formula + worked example, cross-checked vs Sloan/Dechow–Sloan–Sweeney/Beneish standard results), code (every ```python block executed and diffed), coherence (hub↔01 prereqs, jargon, links, contradictions). Ignored `_legacy/`.

**Verdict: PASS with 2 findings — one genuine math error in prose, one minor wording overstatement.** All 7 python blocks run cleanly under Python 3 and reproduce their documented output **exactly** (every block is seeded, output deterministic and byte-matchable). All boxed formulas, M-score weights, persistence coefficients, hedge-return schedules and accrued worked examples are arithmetically correct and consistent with the standard Sloan (1996) / Dechow, Sloan & Sweeney (1995) / Beneish (1999) numbers. One factual statement is wrong (F1). No spelling/typo errors in prose. All wikilinks resolve.

---

## 1. Code verification (7/7 blocks run, all pass)

Blocks extracted from each file, executed under Python 3.11, stdout diffed against each file's documented ```` ``` ```` output fence.

| File | Block | Result | Diff vs documented |
|---|---|---|---|
| index.md | §3 Sloan accrual engine + red-flag checklist | Ran clean (deterministic inputs) | **Exact match** |
| 01-from-zero-intuition.md | §3 "Same NI, different reality" | Ran clean | **Exact match** |
| 02-the-accrual-anomaly.md | §3 hand-rolled OLS + decile sort (seed 7) | Ran clean | **Exact match** (recovers 0.765 / 0.857) |
| 03-detecting-earnings-management.md | §3 Jones vs Modified Jones (seed 11) | Ran clean | **Exact match** |
| 04-red-flags-and-shenanigans.md | §3 five-signal detector on Redwing | Ran clean | **Exact match** |
| 05-failure-modes-and-practice.md | §3 four failure modes | Ran clean | **Exact match** |
| 06-advanced-extensions.md | §3 8-variable M-score (Redwing/Northstar) | Ran clean | **Exact match** |

Every line reproduced bit-for-bit, including the seeded OLS/Monte-Carlo blocks. No block is unseeded, so agreement required zero judgement.

## 2. Math verification

**Sloan / accrual machinery — all correct.** Balance-sheet accrual measure `(ΔCA−ΔCash)−(ΔCL−ΔSTD−ΔTP)−Dep` (index/01, eq. 44/37) is the standard Sloan measure. Worked examples verified by hand: Northstar `(40−15)−(35−10−15)−40 = −25` ✓ (ratio −25/640 = −3.91% ✓); Redwing `(200+20)−(40−5−0)−60 = +125` ✓ (+13.89% ✓); identity `NI = CFO + Accruals` holds for both (105=130−25 ✓; 44=−81+125 ✓). ROA decomposition `Accruals/avgTA + (NI−Accruals)/avgTA = NI/avgTA = ROA` (01, boxed eq.) — correct. Persistence coefficients γ₁=0.765, γ₂=0.855, α₁=0.841, decile-rank gap 0.565-vs-0.838, rank corr accruals/CFO = −0.53, rank corr accrual component vs accruals/earnings = 0.94, F=614, hedge 10.4%/4.8%/2.9% (t=4.71/3.15/1.64) — all match published Sloan (1996) Table 5/6 values. 02 §3's seeded OLS recovers 0.765 and 0.857 against the DGP's 0.765/0.855 (off by +0.002 on cash-flow, expected sampling noise).

**Discretionary-accrual models — all correct.** Healy (constant), DeAngelo (last-period), Jones (eq. 6, `α₁(1/A)+α₂(ΔREV/A)+α₃(PPE/A)`), Modified Jones (eq. 7, `ΔREV−ΔREC` adjustment), and Industry (median) models — equations, event-period-receivables adjustment logic, and the "bias toward zero" / power-at-1%-vs-5% story all verify against Dechow, Sloan & Sweeney (1995). §3 seed-11 simulation reproduces exactly the documented output (Jones −0.008 bias at 8%; Modified Jones +0.002; detection 0.00-vs-0.64 at 1%).

**Beneish M-score — formula and weights correct, one prose statement wrong (F1).** All eight variable definitions (DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA) and the scoring weights `−4.84 + 0.920·DSRI + 0.528·GMI + 0.404·AQI + 0.892·SGI + 0.115·DEPI − 0.172·SGAI + 4.679·TATA − 0.327·LVGI` match the canonical Beneish (1999) M-score, threshold `> −1.78`. §3 output (Redwing −1.73, Northstar −2.68) is internally correct and independently recomputed here (Redwing DSRI 1.146, TATA 0.136 ✓; Northstar DSRI 0.978, TATA −0.036 ✓). **Error:** line 46 asserts SGAI is "the only negative coefficient" — both SGAI (−0.172) *and* LVGI (−0.327) are negative, per the file's own formula and code. See F1.

**Red-flag / practice pages — all correct.** DSO = AR/Rev×365, cash conversion cycle, cumulative CFO/NI (`<1 ⇒ booked-but-never-cash`), goodwill-vs-sales growth test, OPM intensity = SBC/NI, concentration ratio — all formulas and thresholds standard and internally consistent. 05 §3 mode-3 cancellation (`+50` cash fabrication leaves `(dCA−dCash)` unchanged at 70) verified exactly; mode-1 reversal (100 → −20) and mode-4 binary composite (−15%→−2% ⇒ 1) verified. Cross-page numbers identical wherever repeated (10.4/4.8/2.9, 0.765/0.855, −1.78, −1.73/−2.68, +13.89/−3.91).

## 3. Spelling & prose

Full-prose vocabulary audit (all prose, LaTeX/code/wikilinks stripped): **zero misspelled/typo'd words.** Grammar and register consistent. Standard British spellings (manipulator, receivables, amortisation, capitalised) used consistently with the rest of the Atlas. No invented words, no fragments.

## 4. Coherence

- **Hub↔01 prereqs:** consistent. Hub (index line 11) says pages 02–06 need the two statement/ratio bases; page 01 declares its own smaller entry bar (Financial Statements & Accounting only). No contradiction.
- **Hub lookup table ↔ sub-page outputs:** all anchor values flow from actual computed results — operating accrual −25, accrual ratio −3.91%/+13.89%, M-score −1.73/−2.68, hedge +10.4%. Consistent.
- **Jargon:** Sloan, accrual component vs cash-flow component, nondiscretionary/discretionary, Modified Jones, Beneish M-score, DSO/CFO/NI, TATA — all used precisely.
- **Wikilinks:** all in-folder, base, sibling, forward, and factor-layer links resolve (checked every `[[…]]` target against the content tree; 0 real misses — the single grep "miss" is a wikilink-like token inside a ` ```python ` block, `[[1.0, r[2]]`, not a link).
- **One wording overstatement → F2** below.

---

## Findings (2)

**F1 — 06-advanced-extensions.md line 46: "SGAI is the only negative coefficient" is factually wrong.**
Stated: *"…$SGAI$ is the only *negative* coefficient: falling SG&A-per-sales is treated as suspicious…"*. Both SGAI (−0.172) and LVGI (−0.327) carry negative weights — visible in the file's own boxed formula (line 44) and code (line 83). The *interpretive point* (a *decrease* in SG&A-per-sales raises the score / is treated as suspicious) is correct and worth keeping; only the "only negative coefficient" framing is wrong. **Fix:** reword to "$SGAI$ and $LVGI$ are the two *negative* coefficients; of these, $SGAI$'s sign is the counter-intuitive one…" (or drop "only").

**F2 — 02-the-accrual-anomaly.md line 137: "match Sloan's pooled estimates (0.765, 0.855) to the third decimal" overstates.**
The seeded §3 run recovers $0.765$ and $0.857$, not $0.855$; 0.857 vs 0.855 match only to the **second** decimal (they differ at the third). The sentence's thrust (estimator and DGP agree) is true and the adjacent table correctly shows the actual 0.857; only the "to the third decimal" precision claim is loose. **Fix:** change to "…to the second decimal (0.857 vs 0.855, within sampling noise of the seeded DGP)" or just "closely match".