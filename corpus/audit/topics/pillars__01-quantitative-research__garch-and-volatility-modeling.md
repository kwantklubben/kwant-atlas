# Audit — content/pillars/01-quantitative-research/garch-and-volatility-modeling/

**Reviewer:** sole/adversarial. **Date:** 2026-09-10.
**Files checked (7):** `index.md`, `01-from-zero-intuition.md`, `02-arch-and-garch.md`, `03-asymmetric-models.md`, `04-realized-vol-and-har.md`, `05-failure-modes-and-practice.md`, `06-advanced-extensions.md`.
**Code blocks run (7):** one ```python block per file, executed with CPython 3 (stdlib only). All 7 exited 0.
**Method:** extracted each python fence programmatically, re-ran it, and diffed stdout against the adjacent documented output fence. Every math claim cross-checked against `corpus/verified/tsay_ch1-3.md`, `tsay_ch7-9.md`, `tsay_ch10-12.md` and re-derived by hand. Wikilinks resolved against the `content/` root. Prose typo scan over LaTeX/code-stripped text.

## Verdict: PASS WITH FIXES
Math is sound, all 7 code blocks reproduce their documented fences byte-for-byte, and all 22 wikilink targets resolve. Two hub errors (`index.md` §2 table) are the substantive findings; the rest are minor code/spec and attribution nits.

---

## 1. CODE — all blocks reproduce (0 errors)
Every documented output fence matches the live run exactly, including the hub's simulated GARCH, the 02 MLE fit, the 03 GJR/EGARCH asymmetry, the 04 HAR regression, the 05 break-inflates-persistence fit, and the 06 DCC recursion.

| File | Block | Result |
|---|---|---|
| index.md §3 | GARCH sim, seed 42 | persists .98, var 5.0000e-05 vs 5.6286e-05 — **match** |
| 01 §3 | regime toy, seed 5 | ACF table + 23.33% adjacency — **match** |
| 02 §3 | GARCH MLE (Nelder–Mead), seed 7 | MLE line + h-step path — **match** |
| 03 §3 | GJR/EGARCH news-impact | 1.4779 ratio, 82.2% — **match** |
| 04 §3 | RV unbiasedness + log-HAR OLS, seed 123 | 1.4396e-04, R²=0.6797, Σslopes=0.9420 — **match** |
| 05 §3 | break persistence, seed 2024 | 0.9913 vs 0.9384 — **match** |
| 06 §3 | DCC, seed 99 | mean ρ=**0.5916**, term structure — **match** |

## 2. MATH — boxed formulas & worked examples
Re-derived / verified as **correct**:
- GARCH(1,1) recursion, stationarity `Σ_{max(p,q)}(α_i+β_i)<1`, unconditional variance `α0/(1−Σα−Σβ)`, ARMA(1,1) representation `a_t²=α0+(α1+β1)a_{t−1}²+η_t−β1η_{t−1}`, multistep decay `σ_h²(ℓ)=α0+πσ_h²(ℓ−1)` (02 §2, index §2).
- ARCH(1) kurtosis `3(1−α1²)/(1−3α1²)` (02:35) ✓ matches Tsay §3.4.1.
- GARCH(1,1) Gaussian excess kurtosis `6α1²/(1−2α1²−(α1+β1)²)` (index:47) ✓ — re-derived; matches Tsay §3.16.
- Half-life `ln½/lnπ ≈ 34` days for π=0.98 (02:52) ✓.
- EGARCH g-form `lnσ_t²=ω+βlnσ_{t−1}²+θz_{t−1}+γ(|z_{t−1}|−E|z|)`, slope θ+γ (z≥0) / θ−γ (z<0), leverage via **θ<0** (03:30–31) ✓ — correctly distinguishes the S-Plus form (γ<0), matching the corpus caution at `tsay_ch1-3.md:104`.
- GJR variance `α0/(1−α1−½γ1−β1)` and persistence `α1+½γ1+β1` (03:36,41) ✓.
- RV unbiasedness; Parkinson `(H−L)²/(4ln2)≈0.3607(H−L)²`; Yang–Zhang `k=0.34/(1.34+(n+1)/(n−1))` (04) ✓.
- HAR-RV three-timescale spec, DCC `Q_t=(1−θ1−θ2)Q̄+θ1εε′+θ2Q_{t−1}`, `R_t=J_tQ_tJ_t`, BEKK `Σ_t=AA′+ΣA_i(a a′)A_i′+ΣB_jΣB_{j}′` with **raw** shocks (06) ✓ — matches `tsay_ch10-12.md:14,17,23`.
- IBM −2σ vs +2σ ≈ 37% leverage (03:17) ✓ — corpus says 37.4% (`tsay_ch1-3.md:93`).
- Tsay §10.7 Cisco+Intel ordering $57,117 < $57,648 < $58,180 (06:46) ✓ — confirmed `tsay_ch10-12.md:18`.

No wrong formula, sign, or constant found in any prose/boxed formula.

## 3. ERRORS / FINDINGS

### E1 — WRONG CONSTANT (hub). `index.md:53`
- **Stated:** DCC check column: `mean ρ̂ = 0.5930 vs target 0.60 ✓`.
- **Correct:** the executable in `06-advanced-extensions.md:56–81` (seed 99, deterministic) yields **0.5916** — confirmed by live run and by 06:98 & 06:108, which both report **0.5916**. The hub contradicts its own sub-page.
- **Fix:** `0.5930` → `0.5916`.

### E2 — UNSUPPORTED "VERIFIED" CHECK. `index.md:48`
- **Stated:** EWMA/RiskMetrics row check column: `corr(EWMA,GARCH) = 0.9523 ✓`.
- **Problem:** no code in this folder (hub §3, 02, 06, or anywhere in the repo) simulates EWMA or computes this correlation. Repo-wide grep for `0.9523` returns only this line. It is presented as a reproduced number but reproduces nothing.
- **Fix:** either add the EWMA-vs-GARCH simulation that produces it, or drop the check cell / mark it as imported without reproduction.

Both E1 and E2 also falsify the hub's blanket claim at `index.md:33`: *"The numbers in the check column were re-executed and reproduced exactly."*

### E3 — MINOR (logic). `06-advanced-extensions.md:118`
- **Stated:** failure-mode #5 — "a CCC or low-correlation assumption systematically understates portfolio VaR … the verified Tsay ordering ($57.1k<57.6k<58.2k) is a mild illustration".
- **Problem:** in the cited ordering the **constant-correlation** case is the **largest** VaR ($58,180), so the ordering illustrates that *ignoring correlation entirely* (univariate, $57,117) understates — it does **not** support "CCC understates". The evidence and the claim pull in opposite directions.
- **Fix:** reword — attribute the understatement to the univariate/zero-correlation case, not to CCC; or find the crisis episode where CCC is breached low.

### E4 — MINOR (code vs spec, off-by-one). `04-realized-vol-and-har.md:66,70` vs formula at `:38`
- **Stated formula (§2):** `RV̄_t^(h) = (1/h) Σ_{j=1}^h RV_{t−j+1}` — a mean of **h** values (5, 22).
- **Code:** `avg = lambda span,t: sum(lr[t-span:t+1])/(span+1)` and `avg(5,t)`, `avg(22,t)` — averages **span+1 = 6 and 23** values, and each regressor re-includes `lr[t]` (the "daily" term) so daily/weekly/monthly windows double-count day *t*.
- **Impact:** cosmetic for a synthetic demo (the fence reproduces), but the code does not implement the stated HAR windows.
- **Fix:** use `lr[t-span+1:t+1]/(span)` for true 5/22-day means (or document the inclusive convention).

### E5 — MINOR (jargon). `index.md:44`, `02-arch-and-garch.md:48`
- Stated: "π=α1+β1 (**AR root** of the a_t² ARMA(1,1))". π is the AR **coefficient**; the characteristic root is 1/π. Imprecise, not wrong in effect.
- **Fix:** "AR coefficient (persistence)" or "reciprocal of the AR root".

### E6 — MINOR (attribution). `06-advanced-extensions.md:114`
- Stated: "Prefer factor or Cholesky structures for large k (Tsay §10.5–10.6)".
- Corpus places the **Cholesky-GARCH / Cholesky-correlation** derivation at **§10.4.1** (`tsay_ch10-12.md:16`, Eqs 10.28/10.30), not §10.5–10.6.
- **Fix:** cite §10.4.1 for Cholesky (verify §10.5–10.6 before retaining).

### E7 — MINOR (coherence). `index.md:11` vs `06-advanced-extensions.md:11`
- Hub declares the folder-level prerequisites for pages 02–06 as *Econometrics & Time Series* + *Probability & Measure Theory* only, but page 06 additionally requires **Linear Algebra** (matrices, PD, Cholesky). The hub's folder-level prereq list is incomplete.
- **Fix:** add Linear Algebra to the hub prereq line.

## 4. SPELLING / TYPO
No typos found in prose. LaTeX and code were excluded from the scan; the `content/` tree was LaTeX/code-stripped before scanning. Note the two spellings **"Heteroscedasticity"** (Engle 1982, index:122) and **"Heteroskedasticity"** (Bollerslev 1986 / Nelson 1991, index:123–124, 02:150, 03:108) are the **correct, distinct** spellings of those papers' actual titles — not an inconsistency to fix. British spellings (`optimiser`, `parameterisation`, `behaviour`, `modelling`) are used consistently; `modelling` at 06:126 is part of Bollerslev (1990)'s real title.

## 5. COHERENCE / LINKS
- All **22** distinct wikilink targets resolve to existing files (0 broken).
- Hub ↔ sub-page structure (index + 6 sub-pages) is consistent; reading-route arc and in-folder cross-links (01→02→03→04, 05→06) are coherent.
- No other hub↔sub-page numeric contradiction beyond E1/E2.
