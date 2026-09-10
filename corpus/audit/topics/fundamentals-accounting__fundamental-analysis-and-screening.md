# Audit Report — `content/fundamentals-accounting/fundamental-analysis-and-screening/`

Scope: 7 files (index.md + 01..06). Sole reviewer. Audited spelling/typos (prose only), every boxed formula and worked numeric example, every ` ```python ` block (run + stdout-diff), and cross-page coherence (prereqs, jargon, wikilinks, contradictions).

## 1. Verdict

**ACCEPT_WITH_FIXES.** All 7 Python blocks run under stdlib and their stdout matches the adjacent documented output fences byte-for-byte (7/7). All 17 unique wikilinks resolve. The core math is correct and verified: the Graham Number `sqrt(22.5·EPS·BVPS)` and its derivation from the two price caps, the margin-of-safety example (35.87 → 16.4% → watch), the net-net / EPV / enterprising-caps worked example, the revenue-CAGR and composite z-score screens, the red-flag scanner, the value-trap detector, and the quantamental composite — all reproduced exactly. The Graham defensive screen (§3 index, 3/6 survivors) is mechanically correct and the narrative around it (Zeta = 8/9 value trap, Epsilon fails stability, Beta fails growth+leverage) matches the output.

No HIGH or MED math errors. Four **low-severity** issues (a code label that contradicts its own threshold, a prose/CFO-threshold mismatch, a naming inconsistency, and a slight over-attribution of the magic formula), plus minor UK/US spelling mixing:

1. **06:86-87** — the printed label says the veto fires at `mom < -1.5z`, but the code's actual threshold is `r[4] < -0.15` (i.e. a z of −0.15, not −1.5). Under a true −1.5σ rule Zeta Steel (z_mom = −1.145) would **not** be vetoed, and the narrative's whole punchline collapses; the −0.15 threshold is what actually produces the documented (correct) output. Label, not math.
2. **05:31** — prose trap formula states `CFO/NI < 1`, but the detector code (05:62) and index/04 use `< 0.8`. Internal inconsistency in the stated threshold.
3. Naming — 01:58/63 and index:58 call the flagship company "Alpha Machine **Works**"; the index §3 code, 03, 05, and 06 use "Alpha Machine". Cosmetic but jarring within a single folder.
4. **06:45** — the "magic formula" is characterized as `value = E/P + B/P, quality = ROIC`. Greenblatt's actual magic formula ranks on **earnings yield (E/P)** and ROIC only; it does not include B/P. The E/P+B/P "value" is this page's own composite, not the published magic formula.

Minor style: mixed UK/US spelling (e.g. 02 "capitalise"/"normalized", "analyzable"; 04 "recognised"; 02 "modernizes"). Not errors, but inconsistent within files.

## 2. Issues table

| File:Line | Problem (stated) | Correct | Severity |
|---|---|---|---|
| 06:86-87 | Code prints `Falling-knife veto (mom < -1.5z)` but applies `r[4] < -0.15` (mom is already z-scored). Zeta z_mom = −1.145 → under −1.5σ it would NOT veto. | Threshold is −0.15σ (0.15σ below mean); the label should say `mom < -0.15z`, or the threshold raised to −1.5 if that is the intent. The documented output fence matches the actual run, so output is correct — the label is what's wrong. | **LOW (code label)** |
| 05:31 | Prose trap condition uses `CFO/NI < 1` | Detector code (05:62) and the rest of the folder (index, 04) use `< 0.8`. Align the prose formula to `< 0.8`. | **LOW (prose/code threshold)** |
| 01:58,63; index:58 vs index §3/03/05/06 | "Alpha Machine **Works**" vs "Alpha Machine" | Pick one name across the folder. | LOW (naming) |
| 06:45 | "The 'magic formula' is the equal-weight special case with value = E/P + B/P and quality = ROIC." | Greenblatt's magic formula = ROIC + **Earnings Yield (E/P)**; it does not include B/P. Reword to `value = E/P` (or note E/P+B/P as this page's own value composite). | LOW (factual imprecision) |

No spelling typos, no doubled words found in prose (code/LaTeX excluded). UK/US spelling is mixed (see §1 #5) — minor.

## 3. Math verified

Every boxed formula and worked number re-derived or checked against live code output:

- **Graham Number** (01:44, index:44): from `P/E≤15` and `P/B≤1.5`, multiply → `P²≤22.5·EPS·BVPS` → `P_max=sqrt(22.5·2.60·22.0)=35.87` ✓. MOS `=(35.87−30)/35.87=16.4%` ✓; `1.5×price=45 > 35.87` → verdict `watch` ✓.
- **Defensive criteria** (index:33-43, 02:31-33): all seven thresholds (size $100M, CR≥2, LTD≤WC, 10-yr earnings, 20-yr dividends, ≥4/3 EPS growth, P/E≤15, P/B≤1.5, product≤22.5) match Graham's Ch 14 formulation. §3 screen reproduces exactly: Alpha 9/9, Beta 4/9, Delta 9/9, Epsilon 6/9, Zeta 8/9, Sigma 9/9 → 3/6 PASS ✓.
- **Enterprising criteria** (02:37): P/E<10, P/B≤1.5 (or ≤2/3 NCAV), dividend yield ≥2/3 bond yield — reasonable summary (Graham's formal list also includes the yield 2/3 of AAA; doc says "AA-bond" — acceptable paraphrase).
- **Net-net / NCAV** (02:41, code): `(180−90)/10 = 9.00/share`; buy floor `2/3·9 = 6.00`; price 9.00 → not a net-net ✓. EPV `18/0.10=180M → 18/share`, exactly 2× price ✓. Enterprising caps P/E `9/1.2=7.5≤10` ✓, P/B `9/7=1.29≤1.5` ✓.
- **10-yr Rev CAGR** (03): Alpha 11.6%, Sigma 12.8%, Delta 10.8%, Omega 8.8%, Kappa 6.05% (prose "6.1%" ✓ rounding). Hard gates (CAGR≥8%, OPM≥8%, NDE≤2, FCFy≥3%) admit Alpha/Delta/Sigma, reject Omega (OPM 7%, NDE 3.29) and Kappa (CAGR 6.1%, though NDE −0.38 pristine) ✓. Composite z-scores +2.60/+2.05/−4.65 match output ✓. Narrative (Delta ranks last on leverage 0.76 + thinnest FCF conversion 4.7%) ✓.
- **CFO/NI & DSO** (04): `90/105=0.857 > 0.8` → correctly NOT flagged; DSO jump `58−42=16 days` flagged ✓; 4 red / 1 green ✓.
- **Value-trap detector** (05): trap logic `F≤4 or ΔROA<0 or CFO/NI<0.8` → Zeta (F=3, ROA −0.05, CFO/NI 0.55) and Omega flagged; Alpha/Sigma candidates ✓. Cheapest-two (P/E 6.7 Zeta, 10.0 Sigma) split one-trap/one-candidate ✓ — Piotroski intuition correctly demonstrated.
- **Piotroski F-score** (06): all nine signals ([ROA>0],[CFO>0],[ΔROA>0],[CFO>ROA],[ΔLTD<0],[ΔCR>0],[no equity issue],[ΔGM>0],[ΔATO>0]) match Piotroski (2000); "high-F (8–9) beat low-F (0–1) within top BM tercile" ✓.
- **Quantamental composite** (06): z(E/P)+z(B/P) value, z(F)+z(GP) quality; Sigma +2.60 #1, Zeta 1.86 #2 (deep value), vetoed on momentum → FINAL Sigma + Alpha ✓.
- **Five-factor model** (06:49-51): β^{MKT,SMB,HML,RMW,CMA} decomposition and RMW/CMA = accounting-built ✓.
- Bibliographic facts: Fama–French 1992, 2015 (RMW/CMA), Novy-Marx 2013 gross profitability, Green–Hand–Zhang 2017 (94 characteristics), Sloan 1996 accruals, Piotroski 2000, Hou-Xue-Zhang q-factor — all correct journals/years.

## 4. Code run / match stats

| File | Block | Runs (exit 0) | Stdout matches doc |
|---|---|---|---|
| index.md | §3 Graham defensive screen | ✓ | ✓ |
| 01-from-zero-intuition.md | Graham Number + MOS + buy rule | ✓ | ✓ |
| 02-graham-criteria-and-value-investing.md | NCAV net-net + EPV + enterprising caps | ✓ | ✓ |
| 03-screening-metrics.md | hard filter + composite rank | ✓ | ✓ |
| 04-the-research-workflow.md | red-flag scanner | ✓ | ✓ |
| 05-failure-modes-and-practice.md | value-trap detector | ✓ | ✓ |
| 06-advanced-extensions.md | quantamental composite + veto | ✓ | ✓ |

**7/7 blocks run successfully (stdlib only); 7/7 stdout match the documented fences exactly.** All blocks deterministic (no RNG, no I/O, no external deps). "Runs on the standard library only" claims all true.

## 5. Links & coherence

- **17 unique wikilinks, all resolve** (in-folder 01–06 + index, and external hubs). No broken links.
- **Prerequisites:** index states folder-level prereqs (Core Financial Ratios + Equity Valuation) for 02–06, with 01 having its own smaller entry. Sub-pages list internally consistent prereqs (02←01; 03←Core+02; 04←03+Fin Stmt Analysis; 05←03–04; 06←03+05). No sub-page lists Equity Valuation explicitly despite index naming it folder-level for 02–06 — mild framing tension, not a hard error.
- **Jargon:** margin of safety, net-net, scuttlebutt, composite/z-score, F-score, RMW/CMA, survivorship/look-ahead all defined on first use. No undefined terms.
- **Cross-page contradictions:** none beyond the two LOW items above (06 label/threshold and 05 prose/CFO threshold). Sample universe, company metrics, and verdicts are consistent across pages.
- The "one company = Alpha Machine Works" naming (01, index:58) vs "Alpha Machine" (elsewhere) is the only naming divergence.

## 6. Recommendation

Fix the four LOW items: (1) correct the 06:86-87 veto label to match the −0.15 threshold (or raise the threshold to −1.5 if intended); (2) align 05:31 prose `CFO/NI<1` to `<0.8`; (3) unify "Alpha Machine (Works)"; (4) reword the 06:45 magic-formula attribution to E/P-only. Optionally harmonize UK/US spelling. Nothing blocks use; math and code are sound.
