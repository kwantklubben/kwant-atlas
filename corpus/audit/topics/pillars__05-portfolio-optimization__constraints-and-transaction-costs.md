# Audit Report: `pillars/05-portfolio-optimization/constraints-and-transaction-costs/`

**Scope:** 7 files (hub `index.md` + 6 sub-pages). Sole adversarial review.
**Method:** prose typo scan; every boxed formula and worked example verified against first principles and/or re-executed code; all 7 ```` ```python ```` blocks run and stdout diffed against the documented output fences.
**Verdict: PASS WITH ISSUES.** All 7 code blocks run clean and match their documented output exactly; the math backbone is sound and self-consistent. Found 7 substantive errors (numeric/logic/attribution in prose readings and one LaTeX formula) and 2 minor coherence notes. No prose spelling/typos found (one "no no-trade" in `05:42` is correct English, not a typo).

---

## 1. CODE — blocks run and diff result

7 python blocks total (1 per file). All run with exit code 0. stdout diffed line-by-line against the output fence following each block: **all 7 IDENTICAL** (expected-line counts: index 5, 01 13, 02 5, 03 22, 04 20, 05 17, 06 16).

| File | Block | Verdict |
|---|---|---|
| index.md | net_mvo engine + no-trade θ | ✓ identical |
| 01 | unconstrained/long-only/cap35 | ✓ identical |
| 02 | box QP + group-cap bisection | ✓ identical |
| 03 | no-trade region + 3 cost families | ✓ identical |
| 04 | turnover frontier + multi-period ramp | ✓ identical |
| 05 | cost underestimation + backtest + budget | ✓ identical |
| 06 | matrix aim F + sparse rebalance | ✓ identical |

---

## 2. MATH — every boxed formula & worked example

Verified **correct** (consistent with re-execution and first principles):

- **01:37** unconstrained optimum `w* = (1/δ)Σ⁻¹μ`; **01:48** one-way TO = ½‖w−w0‖₁.
- **01:59 (box)** cost-aware objective `max μ'w − δ/2 w'Σw − c'|w−w0| − ½(w−w0)'Λ(w−w0)`.
- **01:63–67** piecewise no-trade solution (three cases) — correct; band edges `(μ∓c)/(δσ²)` = `w* ∓ θ`.
- **02:43 (box)** shadow price `λ_j = −∂V*/∂b_j` (envelope theorem) ✓; **02:49/53/57** group-cap ⇔ alpha-haircut identity ✓ (verified numerically: λ_G = 0.001749/mo, alphas 0.2086→0.1876, 0.2147→0.1937).
- **03:37 Roll** `γ0=2c²+σu², γ1=−c², c=√(−γ1)`, spread 2c ✓. **03:40 (box) generalized Roll** spread `2(c+λ)`, `γ0=c²+(c+λ)²+σu², γ1=−c(c+λ)` — and `γ0+2γ1 = λ²+σu²` verified algebraically ✓. **03:41 Kyle** `λ=½√(Σ0/σu²)`, depth 1/λ ✓.
- **03:57 (box)** cost-aware portfolio ✓. **03:61–62** no-trade: `θ=c/(δσ²)`; `w*−θ / w*+θ` edges ✓ (θ=0.20 for σ=20%, δ=3, c=20bp; band [0.80,1.20]).
- **04:33/39** penalty and budget forms ✓. **04:45** net α_ann = 12μ'w − 12c_true‖w−w0‖₁ ✓. **04:51** multi-period tracking objective ✓.
- **04:55** geometric decay `G = 1 + a/2 − √(a + a²/4)`, `a = ρσ²/(κη)` — derived from characteristic eq κr²−(2κ+ρ)r+κ=0; matches code (a=1 → G=0.38197, w₁=0.618). ✓
- **06:39–40 (box)** `F = (δΣ + κΛ)⁻¹δΣ` — verified numerically (closed-form vs BFGS max|diff| = 5.49e-09). diag(F) and ‖F−diag‖_F = 0.39122 match.
- **02:34–35, 39** box QP and KKT stationarity — sign conventions acceptable.
- Roll/Glosten–Milgrom/Amihud/Kyle coefficients in index table (lines 55–58) all standard ✓.
- No-trade band, gross exposure, gross-leverage, all checked numeric columns in index table reproduce from code (lines 41–54) ✓.

### MATH ERRORS (3)

**E1 — 06-advanced-extensions.md:59 — SCA tangent-quadratic majorant formula is wrong.**
Stated: `|Δw_i|^(3/2) ≤ (3/2)(Δw_i⁽ᵏ⁾)^(1/2)·Δw_i² − (1/2)(Δw_i⁽ᵏ⁾)^(3/2)`.
Problems: (a) not tight at the iterate — for x⁽ᵏ⁾, RHS = `(x⁽ᵏ⁾)^(3/2)·(1.5·x⁽ᵏ⁾ − 0.5)`, equals `|x|^(3/2)` only when x⁽ᵏ⁾=1; (b) not a valid upper bound — e.g. x⁽ᵏ⁾=1, x=0.25 gives RHS = −0.406 < 0.125 = f(x); (c) not tangent (derivative 3x ≠ 1.5√x at x=1).
Correct tangent quadratic majorant (tight + tangent + global upper bound): **`|Δw_i|^(3/2) ≤ (3/4)|Δw_i⁽ᵏ⁾|^(−1/2)·Δw_i² + (1/4)|Δw_i⁽ᵏ⁾|^(3/2)`**. Both the coefficient and the sign of the constant term in the doc are wrong.

**E2 — 06-advanced-extensions.md:147 — diag(F) liquidity attribution wrong (data contradicts).**
Prose: *"ranges from 0.1262 (asset 2, the most expensive to trade, η=0.030) to 0.3074 (asset 5, the cheapest, η=0.010) … varies by a factor of 2.4 across assets purely because of liquidity."*
Facts: η=[0.020, 0.015, **0.030**, 0.025, 0.010, **0.008**]. The η=0.030 asset is **asset 3** (F=0.2172), not asset 2 (η=0.015). The cheapest is **asset 6** (η=0.008), not asset 5. And F is *not* monotone in η: asset 6 (η=0.008, cheapest) has F=0.178, far below asset 5 (η=0.010, F=0.3074); the min-F asset 2 has only mid-range η=0.015. So the ordering is driven by the full covariance Σ, not "purely liquidity." (The 2.4× ratio 0.3074/0.1262 = 2.436 is correct; the attributions and "purely" are wrong.)

**E3 — 03-transaction-cost-models.md:160 — (C) reading contradicts its own printed table.**
Prose: *"Below q≈0.09 the linear cost dominates; … the concave square-root law is cheapest at small size but most expensive at large size."* Actual table values: at q=0.05 the **sqrt** term (0.000224) is the *largest* of the three (linear 0.000050, quadratic 0.000038); sqrt is the largest cost at *every* sampled q (0.05–0.80). So "linear dominates below 0.09" is false and "sqrt cheapest at small size" is false (sqrt is most expensive throughout the range shown). The linear↔quadratic crossover is at q = 0.001/0.015 ≈ 0.0667, not 0.09. The qualitative point (which cost model changes the optimizer direction) survives, but the specific dominance/cheapest claims contradict the data.

---

## 3. PROSE — numeric/logic errors in readings (4)

**E4 — 05-failure-modes-and-practice.md:154 — "60% of the annual cost bill disappears" → should be ~77%.**
Backtest (B): cost_ann 0.0077 → 0.0018; reduction = (0.0077−0.0018)/0.0077 = **76.6%** (consistent with the stated 76% turnover cut). 60% is wrong. (Also "gross alpha is equal": 0.2035 vs 0.2052 — cost-aware is actually slightly *higher*; "equal" is loose but tolerable.)

**E5 — 02-weight-constraints.md:123 — asset labels off-by-one / mispaired; "21%" wrong.**
Prose: *"moves asset 2 from 0.4443→0.35 and asset 3 from 0.4822→0.35 … into assets 5 and 6 (0.0653→0.21, 0.0082→0.09)."* Correct mapping (1-based from w=[0,0,0.4443,0.4822,0.0082,0.0653]): the 0.4443 weight is **asset 3** and 0.4822 is **asset 4** (assets 1–2 are already 0). And the redistribution is swapped: asset 5 goes 0.0082→0.09, asset 6 goes 0.0653→0.21 (0.0653 is asset 6's weight, 0.0082 is asset 5's). Freed notional = (0.4443−0.35)+(0.4822−0.35) = 0.2265 = **22.65%**, not "21%".

**E6 — 01-from-zero-intuition.md:133 — "the long-only book with 0.1932 gross".**
0.1932 is the **cap-35%** book's gross alpha (from code). The long-only book's gross alpha is 0.2071. Should say "the cap-35 book with 0.1932 gross" (or use 0.2071 for long-only).

**E7 — 01-from-zero-intuition.md:25 (and echoed 127) — "135 bp … in one rebalance" and "67 bp per year if you do it annually" misstate units.**
Re-execution: cost @10bp = c·sum|dw| = 0.001×11.2419 = **0.01124 ≈ 112 bp per rebalance** (one-shot, both sides); @50bp = 0.005×11.2419 = **0.0562 ≈ 562 bp per rebalance**. The stated "135 bp in one rebalance" and "67 bp per year if annually" match neither. (The code's "0.1349 ann / 0.6745 ann" are the *annualized-monthly* figures — 13.49%/yr = 1349 bp and 67.45%/yr = 6745 bp — and even those are 10–100× larger than "135"/"67" bp; the sentence appears to mix bp with per-rebalance and per-year interpretations.) Correct one-shot figures: ~112 bp @10bp, ~562 bp @50bp.

---

## 4. COHERENCE — hub, prereqs, links, contradictions

- **Hub vs 01 prereq:** consistent. Hub (index:12) correctly states folder-level prereqs (MVO + Calculus & Convex Opt) apply to pages 02–06 and that 01 has smaller, self-stated entry requirements. 01's prereq (Mean–Variance from Zero) is minimal. ✓
- **Sub-page wiring:** hub routes to six sub-pages and both directions link correctly; every wikilink target resolves to a real page (05 → 02/03/04/06 chain, 06 → 03/05, bridge links to Pillars 2/6, foundations, sibling topics). No dangling links found.
- **Jargon:** terms (no-trade region, shadow price, aim portfolio, transfer coefficient, SCA, big-M, SOCP) are introduced before first use; cross-references to 01/02 for no-trade derivation and to 06 for convexification are accurate.
- **CONTRADICTION (minor, coherence):** the "GP matrix fraction" is written two different ways. Hub intro (index:25) and 04:62–63 box use `x_t = x_{t-1} + (I + κΣ)⁻¹(aim − x_{t-1})`, with `aim = (I+κΣ)⁻¹(δΣ)⁻¹μ`; but the hub lookup table (index:53) and 06:39–40 box use `F = (δΣ + κΛ)⁻¹δΣ`. These are the proportional-cost vs quadratic-impact versions of the same named object and are not clearly distinguished, so a reader sees two different "matrix fraction" formulas for the GP aim. Recommend a one-line note that 04 uses proportional cost (identity cost matrix) while 06 uses quadratic impact (Λ).
- **MINOR (math precision):** 06:44 claims "The eigenvalues of F are δλᵢ/(δλᵢ+κηᵢ)". This requires Σ and Λ to be simultaneously diagonalizable (Λ is diagonal but Σ is full), so it is not generally exact — it's the same special case as 06:43. Worth a "when Σ,Λ commute" qualifier.
- 06:65 cross-impact form `Λ = qqᵀD` with cost `½(qᵀΔw)ᵀD(qᵀΔw)` is internally consistent *if D is scalar* (one-factor model, as labelled); for a matrix D the correct factorization is `Λ = qDqᵀ`. Not counted as an error given the "one-factor" label, but the notation is easy to misread.

---

## 5. SUMMARY

- **files_checked:** 7
- **blocks_run:** 7 (all identical to documented output)
- **errors_found:** 7 (E1–E7)
- **Minor notes:** 2 (GP matrix-fraction coherence; eigenvalue special-case)

**Recommendation:** fix E1 (majorant formula), E2 (η attribution), E3 ((C) reading), E4 (60%→77%), E5 (asset labels/21%→22.65%), E6 (0.1932 belongs to cap-35), E7 (bp unit arithmetic); add the two coherence clarifications.
