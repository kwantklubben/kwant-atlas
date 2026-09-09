# Hull 11th ed. — Per-Chapter Verification Report: Chapters 13–18

**Scope:** Hull, *Options, Futures and Other Derivatives* (11th ed., Global, 2022).
**Source reviewed (read-only):** `/tmp/atlas_extract/hull.txt` (pdftotext `-layout`), lines 14,829–21,530.
**Existing extraction reviewed:** `/tmp/atlas_extract/hull.md` §"Part D (Ch 13–18)" (lines 131–161) + master quick-index rows 30–37.
**Method:** text-based deep-read of every chapter section (Ch13: 13.1–13.11; Ch14: 14.1–14.8; Ch15: 15.2–15.12; Ch16: 16.1–16.5; Ch17: 17.1–17.6; Ch18: 18.1–18.7+), cross-checking every formula and equation number that the digest asserts.
**Date:** 2026-09-09. Source files NOT modified.

---

## 1. Verdict summary

**The hull.md extraction for Ch13–18 is ACCURATE.** No mathematical or conceptual errors found in the digest for these chapters. All key formulas, definitions, section attributions, and equation-number references stated in hull.md were confirmed verbatim against the printed text. Findings below are confirmations plus minor documentation/scope notes (no corrections required to hull.md content). The only text-quality issue lies in the *source* (hull.txt OCR artifacts), not in the digest.

---

## 2. Confirmed key results per chapter

### Ch 13 — Binomial trees (src 14,829–16,335)
- One-step no-arbitrage argument & replicating **delta**: `Δ = (f_u − f_d)/(S0u − S0d)` — **eq (13.1)** ✓ (hull.md ch13 bullet matches).
- Risk-neutral valuation: `f = e^(−rT)[p·f_u + (1−p)·f_d]` — **eq (13.2)**; `p = (e^(rT)−d)/(u−d)` — **eq (13.3)** ✓ (general q-form used by hull.md quick index is the correct q-generalization, q=0 base case).
- Two-step trees & backward induction — eqs (13.5)–(13.10) ✓.
- American options: backward induction with early-exercise check ✓ (13.5).
- Matching volatility: volatility matched if variance eq (13.12); solution **`u = e^(σ√Δt)`, `d = e^(−σ√Δt) = 1/u`** (13.15)/(13.16) — CRR (Cox-Ross-Rubinstein 1979); `a = e^(rΔt)` (13.18); `p = (a−d)/(u−d)` (13.17) ✓ (hull.md u/d/p rows correct).
- Convergence of European tree price to Black-Scholes-Merton as steps→∞ — stated in §13.9 and proved in chapter appendix ✓.
- **§13.11 Options on other assets** — treats index options (dividend yield q) and currency options (foreign rate rf) on trees ✓ (validates hull.md "options on indices/currencies (q-adjusted)" note; dividend yield use is via risk-neutral drift a = e^((r−q)Δt)).
- Note: ch13 itself does NOT value futures options in a dedicated section — those are Ch18/Ch21. hull.md lists only "options on indices/currencies… (q-adjusted)" for Ch13, which is fair; no over-claim.

### Ch 14 — Wiener processes & Itô's lemma (src 16,336–17,054)
- Markov property; Wiener process (mean 0, variance rate 1/yr); generalized Wiener `dx = a dt + b dz` (14.3) ✓.
- **GBM `dS = μS dt + σS dz`** — eq (14.6); discrete ΔS/S ≈ φ(μΔt, σ²Δt) (14.9) ✓.
- Correlated processes (§14.5) present ✓.
- **Itô's lemma** for x following `dx = a dt + b dz`: `dG = (∂G/∂x·a + ∂G/∂t + ½∂²G/∂x²·b²)dt + ∂G/∂x·b dz` — **eq (14.12)** ✓. Application to G(S,t) with GBM gives (14.14) ✓.
- Lognormal property: **`ln ST ~ N(ln S0 + (μ − σ²/2)T, σ²T)`** — eqs (14.18)/(14.19) ✓ (matches hull.md GBM/Itô rows).
- §14.8 Fractional Brownian motion (Hurst exponent H; rough-volatility context) present ✓ (hull.md "fractional Brownian motion (mentioned)" correct).

### Ch 15 — Black-Scholes-Merton model (src 17,554–19,252)
- Assumptions (incl. no dividends during life); §15.4 volatility incl. historical estimator & trading-day time convention ✓.
- **BSM PDE** `∂f/∂t + rS·∂f/∂S + ½σ²S²·∂²f/∂S² = rf` — **eq (15.16)** ✓ (hull.md row 33 correct; digest cites "15.16" ✓).
- Risk-neutral valuation rationale (PDE free of μ) ✓ (15.7).
- Pricing formulas **`c = S0·N(d1) − K·e^(−rT)·N(d2)`** (15.20); **`p = K·e^(−rT)·N(−d2) − S0·N(−d1)`** (15.21); **`d1 = [ln(S0/K)+(r+σ²/2)T]/(σ√T)`, `d2 = d1 − σ√T`** ✓ (hull.md rows 34–36 correct, incl. eq-number cross-refs).
- Interpretation: `N(d2)` = risk-neutral probability of exercise; `S0·N(d1)·e^(rT)` = expected stock price in RN world conditional-type term ✓.
- N(x) standard normal CDF (15.9); §15.10 Warrants & ESOs; **§15.11 implied volatility** (invert σ from market price; VIX/SPX mention) ✓ (hull.md "implied vol — invert formula, root-finding" correct).
- **§15.12 Dividends** — European options on stocks paying known *dollar* dividends: replace **`S0` by `S0 − I`** (PV of dividends during life, discounted from ex-dividend dates); Black's approximation for American call with one dividend ✓. **Confirming scope note:** the dividend-*yield* q formulation (`S0·e^(−qT)`) is NOT derived in Ch15 body — it belongs to Ch17 (index/FX) and Ch13 §13.11 (tree drift). hull.md Ch15 line "replace S0 by S0e^(−qT) **or** S0 − I" mixes both; both are correct, but attributing the q-form to Ch15 is a (harmless) location looseness — it is Ch17's result. Recommended wording fix only.

### Ch 16 — Employee stock options (src 19,252–19,963)
- Contractual arrangements (vesting, exercisability, forfeiture); alignment debate; accounting (expensing at fair value); **valuation** §16.4: (a) BSM with "expected life" (no theoretical validity, noted), (b) binomial-tree lattice with rules adjusted for vesting / employee-turnover (forfeiture) probability / endogenous early-exercise probability; backdating scandal §16.5 ✓. Matches hull.md Ch16 bullet (early exercise, can't sell/hedge, dilution, suboptimal exercise, lattice models).
- Dilution treatment cross-ref §15.10 ✓.

### Ch 17 — Options on stock indices & currencies (src 19,963–20,584)
- Index options = asset paying known dividend yield q; currency = stock paying foreign rf (q→rf) ✓.
- Index/FX European pricing with **q**: `c = S0·e^(−qT)N(d1) − K·e^(−rT)N(d2)`, `d1 = [ln(S0/K)+(r−q+σ²/2)T]/(σ√T)` — eqs (17.4)/(17.5) ✓.
- **Currency (17.11)/(17.12)**: q→rf; bounds `c ≥ max(S0e^(−rfT) − Ke^(−rT),0)`; put-call parity `c + Ke^(−rT) = p + S0e^(−rfT)` ✓.
- **Forward-price (Black-type) re-expression:** `F0 = S0·e^((r−q)T)`; `c = e^(−rT)[F0·N(d1) − K·N(d2)]` with `d1 = [ln(F0/K)+σ²T/2]/(σ√T)` — eqs (17.8)/(17.9)/(17.13)/(17.14) ✓ (validates hull.md Ch17 bullet and quick-index FX/forward rows).
- Dividend-yield estimation from futures `q = r − (1/T)ln(F0/S0)` and from matched call/put pairs ✓.

### Ch 18 — Futures options & Black's model (src 20,752–21,530)
- Nature/reasons for popularity of futures options (18.1/18.2); **European spot vs futures option equivalence when futures matures with the option** (FT=ST) (18.3) ✓.
- **Put–call parity** `c + Ke^(−rT) = p + F0e^(−rT)` — **eq (18.1)** ✓; American-option inequality (18.2) ✓ (hull.md Ch18 parity correct).
- Bounds: `c ≥ max((F0−K)e^(−rT),0)` (18.3), `p ≥ max((K−F0)e^(−rT),0)` (18.4); American `C ≥ max(F0−K,0)` ✓.
- **§18.6 futures drift in RN world is ZERO (martingale)** — behaves like a stock paying dividend yield q=r; `dF = σF dz` (18.5) ✓ (hull.md "drift 0, martingale" correct; footnote 3 foreshadows the Ch28 numeraire subtlety re: futures vs forward measure — not needed here but consistent).
- **Black's model (1976):** `c = e^(−rT)[F0·N(d1) − K·N(d2)]` (18.7); `p = e^(−rT)[K·N(−d2) − F0·N(−d1)]` (18.8); `d1 = [ln(F0/K)+σ²T/2]/(σ√T)`, `d2 = d1 − σ√T` ✓ — exactly matches hull.md row 37/Ch18 formulas.

---

## 3. Issues & flags (no content corrections to hull.md required)

| # | Severity | Item |
|---|---|---|
| 1 | Info (source-only) | hull.txt has OCR glyph substitutions that do NOT affect the algebra and are **absent from hull.md**: Greek σ → Latin `s`; epsilon ε (standard-normal variate) → `P`; square-root `√` → overprinted `2` (so `σ√Δt` renders `s 2∆t`, `σ√T` → `s 2T`); prose `<` → `6` and `>` → `7`; `f(·)` distribution symbol → `f`. Verify any re-derived formula in the raw text by re-reading context, as these glyphs collide with real symbols (`s`=vol, `2`=squared). |
| 2 | Minor (location looseness) | hull.md Ch15 bullet attributes both `S0·e^(−qT)` and `S0 − I` to Ch15. Ch15 §15.12 covers **only** the known-*dollar*-dividend `S0 − I` (and Black's approximation for American calls). The continuous-dividend-yield `S0·e^(−qT)` form lives in **Ch17** (index/FX) and drives the Ch13 tree drift `a = e^((r−q)Δt)`. Not wrong, but if precise chapter attribution matters, move the q-form citation to Ch17. |
| 3 | Note (coverage) | Ch13 §13.11 "Options on other assets" covers dividend-paying stocks (q), stock-index and currency options on a tree via the risk-neutral growth factor; it does not value *futures* options — those require Ch18 (and numerical treatment in Ch21). hull.md's Ch13 wording is compatible; do not add futures options to Ch13's claims. |
| 4 | Note (verification basis) | Equation numbering quoted by hull.md (13.1, 13.15–13.18, 14.12, 15.16, 15.20/15.21, 17.4/17.5, 17.11/17.12, 18.1, 18.7/18.8) all match the printed numbers at the cited locations. |
| 5 | Confirm | hull.md quick-index GBM row and Ch15 "N(d2) = risk-neutral P(exercise)" and "as σ→0 limits to forward value" interpretations are all supported by §15.8 text. |

---

## 4. Recommended (optional) edits to hull.md — none mandatory

1. Ch15 bullet: "Dividends: replace S0 by `S0 − I` (known dollar dividends, §15.12); continuous-yield form `S0·e^(−qT)` derived in **Ch17**." (optional precision)
2. No formula in the digest requires correction. Master quick-index rows 30–37 and Part-D chapter entries are mathematically sound as verified against the printed source.

**Overall:** extraction is high-fidelity for Ch13–18; ship as-is. Any residual risk is in hull.txt glyph artifacts for downstream re-parsing, not in hull.md.
