# Deep Audit — `content/foundations/probability-and-measure-theory/`

**Auditor:** sole adversarial reviewer (per-folder deep audit)
**Date:** 2026-09-10
**Scope:** 7 files — `index.md` (hub) + `01`…`06` sub-pages. Covers probability spaces,
filtrations, distributions/expectation, conditional expectation, martingales, Radon–Nikodym.
**Method:** full prose read; every boxed formula re-derived; every `python` block extracted,
executed (stdlib, `python3`), and byte-diffed against the documented output fence; every
`[[wikilink]]` resolved; every Shreve/Glasserman/ESL citation cross-checked against `corpus/verified/*.md`;
prose spell-checked with `hunspell` (en_US) after stripping code, LaTeX, frontmatter and wikilink syntax.

**Verdict: PASS (no blocking errors).** 5 findings, all minor/cosmetic; 0 wrong boxed formulas;
0 broken links; 0 misspellings. All 7 code blocks reproduce their documented numeric output exactly.

---

## 1. Spelling / typography — CLEAN

`hunspell -l` over the de-LaTeX-ed prose returned **only domain jargon and proper nouns** (Borel,
Fatou, MCT, DCT, SLLN, CLT, iid, integrable, Glasserman, Shreve, Nikodym, Girsanov, Casella,
Hastie, Tibshirani, …) plus `être` from the intentional French *raison d'être* (01:42). **No
misspellings, no doubled words** (regex `\b(\w+) \1\b` → 0 hits), **no unbalanced `$`/`$$`** on any
prose line, en-dash/em-dash usage consistent with house style.

---

## 2. Math — all boxed formulas and worked examples RE-DERIVED CORRECT

| Location | Statement | Verdict |
|---|---|---|
| index:37–47 | Hub lookup table (σ-algebra, measure, law, cond. exp., tower, martingale, exp. martingale, change of measure, RN, Jensen, Independence Lemma, CLT) | ✔ all standard & correct |
| 01:34 | countable additivity ⇒ `P(A^c)=1−P(A)`, `P(∅)=0` | ✔ |
| 01:41 | SLLN + CLT `α̂_n−α ≈ N(0, σ_f/√n)` (variance σ_f²/n ⇒ sd σ_f/√n) | ✔ |
| 02:30 | countable additivity; Lebesgue `P(a,b]=b−a` | ✔ |
| 02 worked example | `E[X|F_1]` on 3-toss tree (`S0=4,u=2,d=0.5`): H-atom paths S₃ = 32, 8, 8, 2 ⇒ mean 12.5; `∫_A X dP = 50/8 = 6.25` | ✔ 6.2500 confirmed by hand |
| 03:28/32/36 | law `μ_X(B)`; `E[h(X)]=∫h dμ_X=∫h f_X dx`; `X=F^{-1}(U)` | ✔ |
| 03:40 | uncorrelated≠independent, `Y=ZX`, `E[XY]=E[X²]E[Z]=0` | ✔ |
| 04:27 | partial-averaging definition | ✔ |
| 04:41 | bivariate normal `X|Y=y ~ N(ρ(σ₁/σ₂)y,(1−ρ²)σ₁²)`, `E[X|Y]=ρ(σ₁/σ₂)Y` | ✔ (Shreve I Ex 11.1, corpus p-129/130/131) |
| 05:27 | martingale/super `≤`/sub `≥`; `(pu+qd)=1,>1,<1` classification | ✔ |
| 05:32 | discounted-stock martingale `Ẽ[S_{k+1}/(1+r)^{k+1}|F_k]=S_k/(1+r)^k` | ✔ |
| 05:36 | `Z(t)=e^{σW(t)−½σ²t}` martingale | ✔ (Shreve II Thm 3.6.1) |
| 05:41 | `ẼX=E[XZ]`, `EY=Ẽ[Y/Z]` (Z>0) | ✔ |
| 05:45 | `e^{−θx−θ²/2}φ(x)=φ(x+θ)` (complete the square) | ✔ re-derived |
| 06:28 | RN `P̃(A)=∫_A Z dP`, `Z=dP̃/dP` | ✔ |
| 06:37–39 | MCT / Fatou / DCT (incl. Fatou direction `E[liminf]≤liminf E`) | ✔ |
| 06:31 | `Z(HH)=9/4, Z(HT)=9/8, Z(TT)=9/16` (Shreve I Ex 9.1) | ✔ (corpus p-114) |

**Citation cross-check (corpus/verified):** Def 1.1.1, Def 1.1.2, Ex 1.1.3, Def 1.2.3, Def 2.3.1,
Thm 2.3.2 (props i–v), Lemma 2.3.4, Thm 2.2.7(vi), Thm 1.6.1, Def 3.3.3, Thm 3.3.4, Thm 3.6.1,
Thm 3.6.2, Remark 3.6.3, Thms 1.4.5/1.4.9 — **all confirmed** in `shreve2_ch1-3.md`. Shreve I
Ex 9.1 / §9.5 / Lemma 2.29 / ζ_k / Thm 9.41 / §11.8 / §12.7 / §13.8 / Thm 3.32 / §5.3 — **all
confirmed** in `shreve1_*.md`. Glasserman eq. 1.39, eqs. 2.13–2.14 (p-070), §1.1, §1.2 — confirmed
in `glasserman_ch1-3.md`. ESL eq. 2.9 / eq. 2.13 — confirmed in `esl_ch1-5.md`.

---

## 3. Code — 7/7 blocks run; numeric output reproduced

All blocks are stdlib-only (`math`, `random`, `itertools`) with fixed seeds ⇒ deterministic.

| File | Block | Result |
|---|---|---|
| index.md | §3 5-check sweep (LLN/CLT/CE/martingale/exp-martingale) | EXACT |
| 01 | LLN + CLT + 68-95-99.7 | values EXACT (trailing whitespace nit — see F5) |
| 02 | coin-toss filtration: partial averaging 6.2500, tower 0.0000 | EXACT |
| 03 | inverse-transform Exp(2), uncorrelated pair, E[X²] | EXACT |
| 04 | bivariate-normal conditional mean; MSE 2.5698 vs 2.5600 | EXACT |
| 05 | martingale, risk-neutral 5.0000, exp martingale, RN recenter | EXACT |
| 06 | RN derivatives, L² orthogonality, MC CLT | EXACT |

Independent hand-checks of the printed numbers also pass: `1/√12/√100 = 0.02887` ✓; 06 CLT
`σ_f=√(½−(2/π)²)=0.3078 ⇒ σ_f/√200=0.02176` ✓; 05 risk-neutral `p̃=(1.25−0.5)/1.5=0.5 ⇒ Ẽ[S]=5` ✓.

---

## 4. Coherence — hub ↔ sub-pages consistent; links resolve

- Hub `index:12` prerequisite framing ("folder prereqs for 02–06; 01 states its own smaller entry
  requirements") matches `01:11` ("Elementary set theory and arithmetic") — consistent, not a contradiction.
- Hub check-column values all trace to a sub-page or the hub's own §3 block: 6.2500 & 0.0000 → 02;
  0.1675 & 1.0009 & 0.0290 → index §3; 1.0020 & −0.0005 → 05; 9/4… → 06. Consistent.
- Failure-mode framing is non-contradictory across hub §4 and 02/03/05/06 §4 (lookahead ↔ 02, uncorrelated≠indep ↔ 03,
  wrong-measure ↔ 05, absolute continuity ↔ 06).
- All 6 sub-pages carry the canonical 6-section skeleton; prerequisite chain 01→02→03→04→05→06 is intact.
- Every `[[wikilink]]` (incl. cross-folder targets `pillars/03-…/black-scholes-merton/index`,
  `foundations/stochastic-calculus/05-girsanov-and-risk-neutral`, `pillars/04-…/var-and-expected-shortfall`,
  `foundations/numerical-methods/03-monte-carlo`) resolves to an existing `.md`/`index.md`. **0 broken links.**

---

## 5. Findings (5 — all minor; no blocker)

**F1 (moderate — code/claim mismatch). `03-distributions-and-expectation.md:63` (block, §3).**
The block is introduced as exhibiting the "uncorrelated-but-**dependent**" pair `Y=ZX`, but the
statistic it prints is the sign test `P(X>0,Y>0)` vs `P(X>0)P(Y>0)`. For this construction the sign
events are *genuinely independent* (`P(Y>0|X>0)=P(Z=1)=½=P(Y>0)`), so both sides equal 0.25
(printed 0.2490 vs 0.2498 — equal). The demo therefore prints evidence *for* independence and cannot
exhibit the dependence it claims (dependence lives in `|Y|=|X|`, e.g. `E[Y²|X]=X²`).
*Stated:* exhibits dependence. *Correct:* use a magnitude/sign-of-magnitude statistic
(`E[|Y| ∣ |X|>1]=E[|X| ∣ |X|>1]`, or `P(|Y|>1 | X>1)=1`), not the sign split.

**F2 (minor — math exposition). `04-conditional-expectation.md:45`.**
"the regression MSE decomposes as `E[Var(Y|X)]` plus irreducible noise" — `E[Var(Y|X)]` **is** the
irreducible noise (ESL eq. 2.46: `EPE = σ²_ε + Bias² + Var`, with `σ²_ε = E[Var(Y|X)]`), so the
sentence double-counts it and omits the reducible terms.
*Stated:* `E[Var(Y|X)]` + irreducible noise. *Correct:* irreducible `E[Var(Y|X)]` **plus** the
model's squared bias and variance terms.

**F3 (minor — citation). `04-conditional-expectation.md:90`.**
Cites "(Shreve II §2.5)" for zero-probability conditioning. The verified corpus locates the
conditional-expectation material in §2.3 (Def 2.3.1, Thm 2.3.2) and §2.4 (properties/densities);
**§2.5 is not corroborated** as containing this. Suggest `§2.3` (or drop the section number).

**F4 (minor — citation scope). `index.md:121`.**
"Shreve I Ch 1 (§1.1–1.5: probability spaces, coin-toss)". In the verified edition, §1.1 *is* the
Binomial Asset Pricing Model; the probability-space/coin-toss machinery is §1.2–§1.5
(`corpus/verified/shreve1_ch1-4.md`). *Correct:* restrict to "§1.2–1.5".

**F5 (cosmetic — output fence whitespace). `01-from-zero-intuition.md:70–71`.**
The documented output fence's last two lines carry trailing spaces that the program does not emit;
all numeric values are byte-identical after `strip()`. Trim the trailing spaces to make the fence
an exact diff.

---

## 6. Summary

- Files checked: **7/7**. Code blocks run: **7/7** (all numeric outputs reproduced; 6 byte-exact, 1 cosmetic whitespace).
- Boxed formulas / worked examples: **all correct** on independent re-derivation.
- Links: **0 broken**. Spelling: **0 errors**.
- Findings: **5** (F1 moderate; F2–F4 minor citation/exposition; F5 cosmetic). **No blocking error; folder content is sound.**

**Re-run recipe:** `python3 -c` each ```python block (stdlib only, seeds fixed) and diff against the
following output fence; resolve `[[target]]` against `content/**/<name>.md` and `<dir>/index.md`.
