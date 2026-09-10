# Audit: content/pillars/06-market-making/market-maker-economics-and-rebates/

**Reviewer:** sole adversarial reviewer. **Date:** 2026-09-10
**Files checked:** 7 (index hub + 6 sub-pages). **Code blocks run:** 7/7.

## Verdict
**PASS with 2 minor math errors + 1 minor wording issue.** Math is overwhelmingly sound: all 12 boxed/worked formulas verify, all 7 code blocks run and match their output fences, all wikilinks resolve, and the empirical anchors agree with `corpus/verified/*.md`. Two prose claims inside worked-example paragraphs state a wrong arithmetic relationship; neither is in a boxed equation.

---

## 1. Spelling / typos (prose)
No prose spelling/typo errors found. (The one hit on the automated scan — `f_m f_m` in index line 29 — is legitimate LaTeX notation `$f_m$ make fee ($f_m=-r$...)`, not a typo.)

## 2. Math verification

### Boxed formulas — all correct
- **01** line 43 `π = h + r − λ − c_inv − f_take·1[taker]` — verified with worked example (0.010+0.002−0.006−0.001 = 0.005 ✓).
- **01** line 46 `h* = λ + c_inv − r` = 0.006+0.001−0.002 = 0.005 ✓.
- **02** line 41 `E[π] = h + r − λ − c_inv − E[f_take]` ✓.
- **02** line 37 sign convention verified: side=+1 (sells), move = −side·Δm, E[side·Δm]=λ>0 enters as −λ ✓.
- **03** line 35 `S^cum = S^raw + 2f_t` = 0.020+2(0.003) = 0.026 ✓.
- **03** line 37 `S^net = S^raw + 2r` ✓; **03** line 41 neutrality `S^cum = S^net + 2f_net` = (0.020+0.004)+2(0.003−0.002) = 0.026 ✓.
- **03** line 45 `h^raw = h^net − r` ✓; **03** line 51 pass-through gap formula ✓.
- **04** line 38 `N* = eQ/C` = 0.014·10⁹/2×10⁶ = 7 ✓; **04** line 47 `R_τ = τ/2 + r − λ` ✓; **04** line 53 `τ^min = 2(λ−r)` = 2(0.004) = 0.008 ✓.
- **05** line 36/38 `E[π_trade] = h + r − π`, break-even `π* = h + r` ✓; **05** line 47 inventory penalty −½γσ²q² ✓.
- **06** line 52 `p* = h^eff − λ_retail − c_other` = 0.008−0.001−0.002 = 0.005 ✓.
- **Index** lookup table rows all verified (π, N*=7, residual +0.001, τ^min=0.008, p*=0.005) ✓.

### Worked examples verified by execution
- **01** gross 0.012, net +0.0050, rebate 40% of net, desk $500k/day, without-rebate $300k (rebate = 67% of P&L) — all confirmed by code ✓.
- **02** simulated adverse term = **−0.005979** (reproduced exactly; prose cites 0.4% gap, actual 0.36% — acceptable rounding), net +0.0050, without rebate +0.0030, rebate 40% ✓.
- **03** fine-tick neutrality (cum-fee 0.0260 in every row) and coarse-tick breakdown (0.0280, 0.0320) confirmed ✓.
- **04** break-even N*=7, N=10 → −$600k; tick-floor residuals match ✓.
- **05** toxicity tolerance π* = 0.0100→0.0120→0.0140; inventory terminal 3002, 20× and 400× claims correct ✓.
- **06** p*=0.005, tick lever e_min/residual table matches ✓.

### MATH ERRORS
- **ERROR 06:107** — Stated: "$0.05 tick ... lifts the protected rent Rτ to **+$0.0210** — **more than 3×** the rent at a $0.01 tick (+$0.0010)". **Actual: 0.0210/0.0010 = 21×** (the code output at 06:96–100 gives Rτ=+0.0010 at τ=0.01 and +0.0210 at τ=0.05). The "3×" figure is the *edge-floor* ratio (0.0270/0.0070 ≈ 3.9), not the rent ratio. Correct statement: rent is **21×** the $0.01-tick rent. (The "4× the half-spread" clause: 0.0210/0.0050 ≈ 4.2 ✓.)
- **ERROR 01:94** — Stated: "removing it cuts the desk's profit **by two-thirds** ($500k → $300k)". **Actual: $500k→$300k is a 40% (two-fifths) cut**, not two-thirds (two-thirds of $500k = $333k → $167k). The 67% figure elsewhere (code line 91, "rebate is 67% of P&L") is rebate/no-rebate P&L (0.002/0.003), a *different base* than the cut of total profit. Correct: "cuts profit by 40%".

### Minor wording / imprecision
- **04:103** — "Quadrupling the tick ($0.005→$0.020) **quadruples the protected rent** (−0.0015→+0.0060...)". The tick does 4×, but the rent goes from a **negative** residual (−0.0015, i.e. no rent — race overshoots) to +0.0060; it is a sign-flipping swing, not a quadrupling. The swing magnitude 0.0075 = 3τ/2 is correct. Suggest rephrasing as "swings the residual from −0.0015 to +0.0060".
- **02:105** — prose rounds the sampling gap to "0.4%" where the reproduced value is 0.36% (0.005979 vs 0.006). Benign rounding; not an error.

## 3. Code audit
- **Blocks run: 7/7** (one per file). All 7 exit code 0 and **stdout matches the output fence** line-for-line.
- Only diff: **03** — actual output has a leading blank line (from `print(f"\n{label}:")`) that is omitted from the fence's first line. Cosmetic; content identical.
- `import random` blocks (02, 05) are deterministic (seeded); reproduced byte-identical.
- The `-0.005979` cited in 02 prose is not itself printed by the fence (fence shows rounded −0.0060), but the underlying value is correct — minor presentational gap only.

## 4. Coherence
- **Hub vs 01 prereq:** consistent — hub explicitly notes page 01 states its own smaller entry requirements; 01 correctly declares none.
- **Wikilinks:** 0 broken links across all 7 files (checked against content tree incl. index/ pages).
- **Prereq chain** is acyclic and correct: 01→02→03→04→05/06, 06 prereq correctly only 03+04.
- **Jargon:** terms (maker, taker, rebate, cum-fee spread, PFOF, maker-taker, tick size) used consistently across all files and hub lookup table.
- **Cross-file consistency:** the shared constants (h=0.010, r=0.002, λ=0.006, c_inv=0.001, τ=0.01) are identical in every worked example; all reproduce π=0.005.
- **Empirical anchors vs corpus:** NYSE Arca 30¢/21¢ (CF 2012 fn 3) and TSX 27.5¢/40¢ (MP 2015) internally consistent with the cited anchors; Hasbrouck Ch 14 realized-cost `p_t − m_{t+5}` and info-permanent/inventory-transient claims confirmed in `corpus/verified/hasbrouck_ch11-15.md` ✓.
- No contradictions found beyond the two errors above.

## Recommendations
1. Fix 06:107 multiplier (3× → 21× for the rent comparison).
2. Fix 01:94 (two-thirds → 40%/two-fifths cut).
3. Optionally reword 04:103 ("quadruples the protected rent" → sign-flipping swing) and add the leading blank line to the 03 output fence.
