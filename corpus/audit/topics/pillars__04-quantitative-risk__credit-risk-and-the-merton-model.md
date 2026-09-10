# Audit: `content/pillars/04-quantitative-risk/credit-risk-and-the-merton-model/`

**Reviewer:** sole adversarial reviewer · **Files checked:** 7 · **Python blocks run:** 9/9 (all matched documented output fences exactly)

Scope: index.md hub + 6 sub-pages (01 From Zero … 06 Advanced Extensions). `content/_legacy/` ignored.

## Verdict

**FAIL (minor)** — the folder is mathematically sound in the mainline results, all 9 code blocks reproduce their documented output byte-for-byte, all check-column numbers in the hub are correct, and all 50 wikilinks resolve. However, **page 02 contains three real formula/sign errors** in the debt-PDE and comparative-statics sections (its most technical section), all of which contradict Merton (1974) and, for line 37, contradict the page's own eq. (10). A derivational reader of page 02 will be misled. No errors found in pages 01, 03, 04, 05, 06 or the hub's numerical checks.

---

## 1. MATH ERRORS (all in `02-the-merton-structural-model.md`)

### E1 — Debt PDE: wrong sign on the time-derivative term
- **Location:** `02-the-merton-structural-model.md:37`
- **Stated:** `F_t + ½σ_V²V² F_VV + rV F_V − rF = 0`
- **Correct:** `½σ_V²V² F_VV + rV F_V − rF − F_t = 0` (the time-derivative term is **−F_t**, not **+F_t**).
- **Evidence:** Merton (1974) eq. (8) is `½σ²V²F_VV + rV F_V − rF − F_τ = 0` with `F_t = −F_τ` (τ = time to maturity) — i.e. −F_t. The page's own equity PDE at **line 39** (`½σ²V² f_VV + rV f_V − r f − f_t = 0`) is exactly Merton's eq. (10) and is numerically correct. Since debt and equity both satisfy the *same* pricing PDE, line 37 and line 39 cannot both be right; line 37 uses the wrong (opposite) sign.
- **Numerical check:** for the page's own worked firm (V=500, D=300, r=3%, σ_V=20%, T=1), evaluating the written LHS against the true debt value F = V − E gives residual **−18.17** (≉ 0); the corrected −F_t form gives residual **0.00014** (≈ 0). The line as written is a false equation.

### E2 — Second derivative substitution: wrong sign
- **Location:** `02-the-merton-structural-model.md:38`
- **Stated:** `using F_VV = f_VV, F_V = 1 − f_V (Merton eq. 15)`
- **Correct:** `F_VV = −f_VV` (and `F_V = 1 − f_V`). Since F = V − f, `F_VV = d²(V−f)/dV² = −f_VV`.
- **Impact:** the stated substitution is algebraically wrong. (With the correct −F_VV *and* the corrected −F_t, line 37 reduces exactly to the equity PDE at line 39, so the derivation's *conclusion* is right but the intermediate identity it cites is not.)

### E3 — Comparative statics: F_r formula wrong
- **Location:** `02-the-merton-structural-model.md:58`
- **Stated:** `F_r = −t·F < 0`
- **Correct:** Merton (1974) eq. (15) gives `F_r = −f_r < 0`; the exact value is `F_r = −t·D·e^{−rt}·N(d2) < 0`.
- **Evidence:** `∂F/∂r` where F = V·N(−d1) + D·e^{−rt}·N(d2): the d1/d2 drift terms cancel (using V·n(d1)=D·e^{−rt}·n(d2)), leaving `−t·D·e^{−rt}·N(d2)`. Numerically −289.79 vs the stated −tF = −291.05 (0.4% off, i.e. not an identity). **The sign (< 0) is correct**; only the formula is wrong.

> Note: Merton's eq. (15) states `F_r = −f_r < 0`; the page replaced a trivially-true identity with an incorrect one. The other four entries in line 58 (`F_V=1−f_V>0`, `F_B=−f_B>0`, `F_t=−f_t<0`, `F_{σ_V²}=−f_{σ_V²}<0`) are all correct and match Merton eq. (15).

## 2. PROSE / NOTATION (minor)

### P1 — Undefined symbol "K" in the debt-decomposition sentence
- **Location:** `01-from-zero-intuition.md:33`
- **Stated:** "Since $V=E+F$ and $F=\min(V,D)=D-K$ plus a put (put–call parity)…"
- **Issue:** `K` is never defined and the phrase "D−K plus a put" is garbled. The correct identity is `F = min(V,D) = D − max(D−V,0) = D − (put)`. The page already states the correct form (riskless-minus-put) at line 46, so line 33 is redundant and confusing. Suggest rewriting as "F = min(V,D) = D minus a put (put–call parity)".

## 3. COHERENCE / CLAIMS

### C1 — "formula-verified in the corpus" is overstated for Merton
- **Locations:** `index.md:31` ("transcribed from the verified corpus — Merton (1974) eqs. (10)–(18)"), `02:132`, `03:119`, and pages' "formula-verified in the corpus" notes.
- **Issue:** No Merton verification `.md` exists under `corpus/verified/` (that directory has hull, shreve, tsay, bjork, glasserman, gregory, etc. but no merton file). Merton (1974) is present only as raw PDFs under `corpus/titles/refs/pillar4/`. The "verified in the corpus" claim for Merton formulas is not backed by a verified source file the way the Hull/Bluhm citations are. (Worth noting: I verified Merton eqs. (8)/(10)/(15) directly against the PDF `35_Merton_1974_on_the_pricing_of_corporate_debt.pdf`, and the errors E1–E3 are real regardless.)

### C2 — Hub check-column provenance (very minor)
- `index.md:31` says "every number in the check column was … reproduced in §3", but the reduced-form (Q(5)=0.8825, CDS 150bp) and Vasicek (θ_0.999=0.17633) check numbers are actually reproduced in the **sub-page** code blocks (04 and 06), not in hub §3. All of them are nonetheless correct (verified by execution).

### C3 — Page-01 prerequisite framing (very minor, not an error)
- `index.md:11` claims page 01 has "smaller, entry requirements," but page 01 (`01:11`) lists the *same* two folder-level prerequisites (Probability & Measure Theory and BSM). Its distinguishing feature is only "no prior credit *knowledge*" (it does require BSM). Minor framing mismatch, not a factual error.

---

## 4. CODE VERIFICATION (9/9 blocks — actual count run)

Every ```python block was extracted and executed with `python3`; stdout was diffed against the following documented output fence.

| # | File | Block | Result |
|---|------|-------|--------|
| 1 | index.md | Merton engine (V0, σV, d1/d2, PD) | ✅ MATCH |
| 2 | 01-from-zero-intuition.md | payoff-split table | ✅ MATCH |
| 3 | 02-the-merton-structural-model.md | forward/inverse map | ✅ MATCH |
| 4 | 03-distance-to-default-and-pd.md | DD, both PDs, spread | ✅ MATCH |
| 5 | 04-reduced-form-and-cds.md | hazard + CDS fair-spread recovery | ✅ MATCH |
| 6 | 05-failure-modes-and-practice.md | PD sensitivity + spread puzzle | ✅ MATCH |
| 7 | 05-failure-modes-and-practice.md | jump-to-default + MC | ✅ MATCH |
| 8 | 06-advanced-extensions.md | Vasicek closed form vs MC + quantiles | ✅ MATCH |
| 9 | 06-advanced-extensions.md | transition-matrix cumulative defaults | ✅ MATCH |

All documented outputs are exactly reproducible (incl. MC path counts 400,000 and 200,000 and the Acklam inverse-normal quantile). No fabricated/incorrect output fences.

## 5. MATH CHECK-VALUES (hub tables) — all correct

- Merton engine: V0=432.9067, σV=0.0926, d1=2.882599, d2=2.7900, F=332.9067, PD=26.35 bp, spread=0.71 bp, real-world PD(μ=10%)=4.3 bp — all confirmed by execution.
- Reduced-form: λ=250 bp/yr from s=150bp,R=40%; Q(5)=0.8825, PD(5)=11.75%; CDS fair spread recovers 150.00 bp; s≈λ(1−R)=150bp — confirmed.
- Vasicek: θ_0.999=0.17633 (17.63% of EAD); F(0.1763)=0.999; q99=0.10559; MC mean≈1.997%≈2%, MC q99.9=18.3% vs asymptotic 17.6% (granularity premium) — confirmed.
- Merton debt formula F = B e^{−rt}[Φ(h2)+(1/d)Φ(h1)] with h1,h2 — numerically equals V−E (291.0542) and the risky-yield/spread values, confirming eq. (14) forms.
- Statics: F_t<0, F_σV²<0 verified numerically (debt falls in time-to-maturity and volatility).
- Jarrow–Turnbull, recovery/LGD (λ=s/(1−R)), default-correlation UL (Bluhm 1.13) formulas: consistent and correctly used; no other formula errors found across pages 01, 03, 04, 05, 06.

## 6. LINKS

- 50 unique wikilink targets across the 7 files; **0 broken** (all resolve under `content/`). Hub↔sub-page graph and cross-pillar links (VaR/ES, EVT, Black–Scholes–Merton, Probability & Measure Theory, Liquidity Risk, Stress Testing) all present and valid.

## 7. PRIORITIZED FIX LIST

1. `02:37` — change `F_t +` to `− F_t` (or write `½σ_V²V² F_VV + rV F_V − rF − F_t = 0`). [HIGH — false equation]
2. `02:38` — `F_VV = f_VV` → `F_VV = −f_VV`. [HIGH]
3. `02:58` — `F_r = −t F < 0` → `F_r = −f_r < 0` (Merton eq. 15), optionally with the exact `−t D e^{−rt} N(d2)`. [HIGH]
4. `01:33` — remove `=D−K` (undefined K); use `F = D − (put)`. [LOW]
5. `index:31` and page "formula-verified in the corpus" notes for Merton — either add a Merton verification `.md` to `corpus/verified/` or soften the claim (only raw PDFs exist). [LOW]
