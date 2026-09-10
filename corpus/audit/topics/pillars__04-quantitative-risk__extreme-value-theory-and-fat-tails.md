# Audit — extreme-value-theory-and-fat-tails (content/pillars/04-quantitative-risk/)

**Scope:** 7 files (index + 01–06). **Reconciled:** 8 python blocks extracted & diffed; 8/8 exact match to printed fences. 0 broken wikilinks.

---

## FINDINGS

### F1 — MATH ERROR (Student-t tail constant), 02-stylized-facts-of-fat-tails.md:33
Stated:
`1-F_ν(x) ~ 1/(B(1/2, ν/2) √ν) · x^{-ν}`
Correct (standard t-tail asymptotics):
`1-F_ν(x) ~ ν^{ν/2-1}/B(1/2, ν/2) · x^{-ν} = Γ((ν+1)/2) ν^{ν/2-1}/(√π Γ(ν/2)) · x^{-ν}`
The printed constant is missing the factor `ν^{ν/2-1}` (equivalently, the whole expression is off by a factor of `ν^{(ν-1)/2}`).
Verification: numerical complement of the t₄ survival at x=10 is `2.8e-4`; the stated formula predicts `3.75e-5`, the corrected predicts `3.0e-4`. (For ν=4 the stated constant is exactly 8× too small.)
**Severity: HIGH — a boxed/worked formula that a reader will quote.**

### F2 — MATH ERROR (GPD mean-excess identity missing the ξ·w term), 04-peaks-over-threshold.md:47 and 06-advanced-extensions.md:33
Both state the "GPD mean-excess identity (McNeil & Frey eq. 14)" as
`E[W−w | W>w] = (w+β̂)/(1−ξ̂)`
Correct:
`E[W−w | W>w] = (β̂ + ξ̂·w)/(1−ξ̂)`
The printed version drops the `ξ̂·w` term. Note the **boxed ES formula** derived from it (`(x_q+β−ξu)/(1−ξ)`) is CORRECT and numerically verified (ES(0.999)=0.20640 reproduces; hand-check ES−VaR at q=0.999 requires `(β+ξ(x_q−u))/(1−ξ)=0.0745`, which the () incorrect `(x_q+β)/(1−ξ)=0.2243` does not give). So the downstream result is right but the cited identity as transcribed is wrong.
**Severity: MEDIUM — inconsistent with the (correct) boxed ES; will confuse the derivation.** Fix the eq-14 transcription in BOTH files.

### F3 — MATH/NUMERICAL ERROR (6σ recurrence period), 01-from-zero-intuition.md:20
Text: "P(X<−6σ)=Φ(−6)≈1.0×10⁻⁹, roughly once in 4 billion trading days — about 16 million years."
Φ(−6)=9.87×10⁻¹⁰ ⇒ 1e-9 corresponds to **~1.0 billion days** (single-sided) ≈ **~4 million years** at 250 trading days/yr (≈2.0 Myr two-sided). "4 billion days / 16 million years" is **~4× too large**. (This also clashes with the index's 5σ line, which correctly uses the two-sided convention ~1.7M days.)
**Severity: MEDIUM — narrative quantity is wrong by a factor of 4.**

### F4 — INACCURATE CHECK VALUE in the hub lookup table, index.md:39
"GPD mean excess … ξ=0.36 → e(u) ≈ 2.7× scale"
With the folder's own run values (β=0.01167, u=0.03183, ξ=0.36): `e(u)=(β+ξu)/(1−ξ)=0.0361`, ratio **3.10×** the scale, not 2.7×. The number in the "Verified check" column does not reproduce the stated formula.
**Severity: LOW — cosmetic but the column claims "re-executed and reproduced exactly."**

### F5 — MINOR COHERENCE NIT, index.md:11
Index says the folder-level prerequisites for pages 02–06 are Probability Theory **and** VaR & Expected Shortfall. Page 02's own header lists only Probability Theory; 05 lists only 04; 06 lists 04+05. VaR&ES is genuinely required only by 04. The index blanket is looser than the page-level headers.
**Severity: LOW / informational.**

---

## What was verified clean
- **GEV family** (index:32, 01:38, 03:28): `exp{−(1+ξx)^{−1/ξ}}`, Gumbel limit `e^{−e^{−x}}` — correct conventions (ξ>0 Fréchet, =0 Gumbel, <0 Weibull).
- **Pickands–Balkema–de Haan / GPD CDF** (04:29–35): excess distribution and GPD CDF `1−(1+ξy/β)^{−1/ξ}` — correct.
- **GPD mean-excess function** `e(u)=(β+ξu)/(1−ξ)` (index:39, 02:38, 04:35) — correct (F2's error is only in the eq-14 transcription, not this).
- **Tail estimator** (index:40, 04:40): `1−(N_u/n)(1+ξ(x−u)/β)^{−1/ξ}` — correct.
- **EVT VaR** (index:41, 04:46): `u+(β/ξ)[((n/N_u)(1−q))^{−ξ}−1]` — correct, reproduces 0.1319.
- **EVT ES** (index:42, 04:48): `(x_q+β−ξu)/(1−ξ)` — correct, reproduces 0.2064.
- **Hill estimator** (index:43, 03:42): `(1/k)Σ log(X_(i)/X_(k+1))` descending — correct; α̂=k/Σlog — correct.
- **Pickands estimator** (index:44, 03:46): `(1/log2)·log[(X_(n−k)−X_(n−2k))/(X_(n−2k)−X_(n−4k))]` — correct.
- **Tail-index conventions / moments** (index:46, 01:28, 02:34): m-th moment exists iff m<α; α=ν for t_ν; ξ=1/ν — consistent everywhere; no inversion.
- **VaR extrapolation logic** (04:119): fits e.g. empirical over-shoot at q=0.9999 due to ~2 obs — correct reading of the reproduced output.

## Code: 8/8 blocks exact
- index.md b0 (EVT engine): u=0.03183 Nu=999 ξ=0.360 β=0.01167; VaR(0.999)=0.13189 emp 0.13606; ES 0.20640/0.22405 — exact.
- 01 b0 (block maxima): normal 14.2, t₃ 3.0, t₆ 4.8 — exact. (Note: t₆ nominal α=6 shows 4.8 due to estimator noise; prose acknowledges "keep their tail index" loosely — acceptable, text is honest that t₃ is the clean case.)
- 02 b0 (stylized facts): kurtosis 3.00/54.8/546.3; P(>4–6σ); ACF1 r² +0.364 vs r 0.016 — exact.
- 03 b0 (Hill/Pickands): Hill 3.67/3.76/3.60/3.28; Pickands −0.112 / +0.122 — exact.
- 04 b0 (POT VaR/ES): 3 quantiles exact.
- 05 b0 (threshold sensitivity): ξ 0.260/0.300/0.360/0.340/0.540 — exact.
- 05 b1 (conditional EVT): ξ=0.080 β=0.750 z_0.99=3.104; EVT VaR 0.7100 vs normal 0.5322 — exact; "33% higher" ✓ (0.710/0.532=1.334).
- 06 b0 (Gaussian copula): ρ=0.7 both=0.0194 cond=0.390; ρ=0 cond=0.046 — exact.
All blocks are seeded (deterministic); no nondeterminism.

## Coherence & links
- 7 files = index hub + 6 sub-pages ✓; hub signposts to 05 ✓; each page links back to hub ✓.
- 0 broken wikilinks (all `pillars/…/index` and `foundations/…/index` targets exist).
- Jargon (§numbers, "de Haan §3.2.2", McNeil & Frey eq.10/14, ASTIN, JEF) internally consistent; no contradiction between hub table and page formulas except F1–F2.

---

## Verdict
**FAIL (needs fixes)** — technically excellent, code all matches, core formulas (GEV/GPD/VaR/ES/Hill/Pickands) correct; but F1 (wrong Student-t tail constant) and F2 (eq-14 identity missing a term, two pages) are genuine math errors a reader would carry forward, and F3 is a wrong worked number. F1–F3 must be corrected before sign-off; F4–F5 trivial.

Summary: 5 findings (2 HIGH/math, 1 MEDIUM, 2 LOW). Files checked 7; blocks run 8/8 exact.