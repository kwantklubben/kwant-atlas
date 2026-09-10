# Audit — `pillars/04-quantitative-risk/liquidity-risk-and-funding/`

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages). Market vs funding liquidity, Amihud ILLIQ, bid–ask spread decomposition, Kyle λ / price impact, liquidation cost & L-VaR, liquidation horizon, margin recursion (Brunnermeier–Pedersen), fire-sale externality, margin procyclicality, NSFR/LCR.
**Corpus cross-check:** `corpus/verified/foucault_ch1-3.md` (eq 2.1–2.10, Roll 2.11–2.18 + biases, Stoll 2000 numbers), `corpus/verified/foucault_ch7-10.md` (eq 9.6/9.9 regression, L-CAPM 9.18 four-betas, 1.1%/yr, DG–P search spread), `corpus/verified/hasbrouck_*` (Ch 1.2 / Ch 3 / Ch 7 / Ch 9.9), `corpus/verified/hull_*` (√N scaling, LCR/NSFR).
**Method:** (1) prose spelling/typo scan (code/LaTeX excluded); (2) every boxed formula, display equation and worked example re-derived and checked against the corpus verified digests; (3) **every** ```python block executed in Python 3 and diffed character-for-character against its output fence; (4) hub↔sub-page coherence, notation consistency, jargon first-use, wikilink resolution (all 7 files, every `[[...]]`).

---

## VERDICT: **PASS (with minor fixes)** — 8 defects, 0 high-severity; **all 7 python blocks reproduce their fences exactly**; **every boxed/display formula is mathematically correct**; 0 broken wikilinks. The defects are two false prose claims about the 04 simulation, one inconsistent worked-example narrative in 03, and a folder-wide `S` notation clash.

---

## Summary of findings

| # | Severity | File:line | Type | Issue |
|---|----------|-----------|------|-------|
| 1 | **MINOR** | `04-margin-and-funding-spirals.md:101` | MATH / claim vs own code | "the loss spiral alone would have left the fund at \$8.5M equity and **4.85×** leverage — **alive and unforced**." Neither number is right — see F1. |
| 2 | **MINOR** | `04-margin-and-funding-spirals.md:103` | MATH / claim vs own code | "raising `haircut_step` to 0.15 makes the process run away (**equity → 0 within three rounds**)." Verified false — equity stabilises at ~\$4.83M — see F2. |
| 3 | **MINOR** | `03-liquidation-cost-and-lvar.md:96` | MATH / internal consistency | "even for a **\$5M order** in a **\$200M-ADV name** … a \$50M order carries **100× the per-unit** impact drag." \$-order and ADV contradict the block's own `V=10_000_000`, `Q=100_000`, `D=200_000`; 100× is the *total*-cost ratio for 10× size, not the per-unit ratio — see F3. |
| 4 | **MINOR** | `index.md:34,38,41` + `03:32–33` vs `01:36` / `02:38` | COHERENCE / notation | Folder-wide clash: index & 03 use **`S` = relative spread** `(a−b)/m`; 01 & 02 use **`S` = absolute** `a−b`, `s` = relative. Foucault's own convention (eq 2.1) is `S = a−b`, `s = (a−b)/m`. See F4. |
| 5 | **MINOR** | `index.md:11` vs sub-pages | COHERENCE / prereq | Hub declares `Parametric, Historical & Monte Carlo VaR` a folder-level prerequisite for pages **02–06**; **no** sub-page lists it (02→01+VaR&ES; 03→02+VaR&ES; 04→03+VaR&ES; 05→04+03; 06→04+05). See F5. |
| 6 | **TRIVIAL** | `02-market-vs-funding-liquidity.md:93` | NUMERIC | "the Amihud ratio separates cap tiers by **four orders of magnitude**." Printed range is 2.5×10⁻¹⁰ → 4×10⁻⁷ = **1600× ≈ 3.2 orders**, not four. |
| 7 | **TRIVIAL** | `04-margin-and-funding-spirals.md:41` | MATH notation | "linear impact, `κ = 1/(D·m)`-like" — the extra `m` does not follow from `Δp = λq`, `D = 1/λ`; the page's own code uses `κ = impact_coef/ADV`. Loose/imprecise. |
| 8 | **NOTE (low confidence)** | `03:25`, `05:34–36` | MODEL ASSERTION | "schedule/impact cost scales like **T** (linear-impact)" is asserted, not derived, and is not the standard result (temporary linear impact ⇒ ∝Q²/T; permanent ⇒ ∝Q²; timing risk ⇒ ∝√T). Arithmetically self-consistent (`16/4 = 4×`), but the ∝T premise needs a stated model. |

---

## FINDING 1 — MINOR · false "loss-spiral-alone" counterfactual (`04:101`)

**Stated:** "…This is the margin spiral doing the damage: the loss spiral alone would have left the fund at **\$8.5M equity and 4.85× leverage** — **alive and unforced**."

**Re-run of the page's own recurrence** with `impact_coef=0, haircut_step=0` (pure loss spiral, constant `m=0.20`, `N0=10M, P0=50M, shock=−3%`):

```
0 N=8.500M P=48.500M m=0.20 sale=0.000M lev=5.706   # at the shock, leverage jumps 5.00→5.71×
1 N=8.500M P=42.500M m=0.20 sale=6.000M lev=5.000   # constraint BINDS: forced sale of $6.0M
2..8 N=8.500M P=42.500M m=0.20 sale=0.000M lev=5.000
```

**Correct:** even with **zero impact and a constant haircut**, the fund is **forced to sell \$6.0M** in round 1 (because the 3% shock pushes leverage to 5.71× > 1/m = 5×), settling at **equity \$8.5M / position \$42.5M / leverage 5.00×**. So the claim is wrong on both counted: it is **not** "unforced" (the margin constraint binds at t=1), and the surviving leverage is **5.00×**, not **4.85×** (4.85 = 48.5/10 would be position ÷ *initial* equity, which is not the leverage definition `L=P/N` used everywhere else in the folder).

**Fix:** delete "alive and unforced", or restate as "the loss spiral alone would have forced a \$6M sale and left the fund at \$8.5M equity, 5.00× leverage."

---

## FINDING 2 — MINOR · false "runaway" parameter claim (`04:103`)

**Stated:** "…Setting `impact_coef=0` recovers the pure loss spiral; **raising `haircut_step` to 0.15 makes the process run away (equity → 0 within three rounds)**."

**Re-run of the page's own function with `haircut_step=0.15`** (all other defaults):

```
0 N=8.500M P=48.500M m=0.20
1 N=5.564M P=22.816M m=0.35 sale=24.214M
2 N=4.897M P=10.803M m=0.50 sale=11.688M
3 N=4.826M P= 8.108M m=0.60 sale= 2.641M   # m hits the m_cap=0.60
4 N=4.825M P= 8.042M m=0.60 ...
```

**Correct:** equity goes 8.5 → 5.56 → 4.90 → **4.83M and stabilises**; it never approaches 0. (`m_cap=0.60` caps the margin spiral, and with impact ∝ sale the fixed point is finite.) The *position* collapses hard (\$48.5M → \$8.0M), but the sentence's literal claim — **equity → 0 within three rounds** — is false.

**Fix:** replace with the true statement (e.g., "`haircut_step=0.15` collapses the book from \$48.5M to \$8.1M in three rounds while equity stabilises near \$4.8M") or actually pick parameters that diverge.

---

## FINDING 3 — MINOR · worked-example narrative contradicts the code block (`03:96`)

**Stated:** "the impact cost (\$25,000, 25 bp) *exceeds* the exogenous spread cost (15.8 bp) **even for a \$5M order in a \$200M-ADV name** — and it grows as $Q^2$, so **a \$50M order carries 100× the per-unit impact drag**."

**Problems:**
1. **\$-order:** the block sets `V = 10_000_000`, `Q = 100_000`, `D = 200_000`. `Q·price = V ⇒ price ≈ \$100/share`, so the order being priced is **≈\$10M, not \$5M**. The "\$5M" appears nowhere in the block or in §2.
2. **"\$200M-ADV name":** ADV is never given in this block (§2.3 only mentions ADV generically; the 04 simulation uses `ADV=200_000_000` for a *different* example). Importing `\$200M-ADV` here is unsupported by anything in 03.
3. **"100× the per-unit impact drag":** the per-share drag is `λQ/2` (page's own §2.2), which scales **linearly** in `Q`. A \$10M→\$50M increase is 5× size ⇒ **5× per-unit**, **25× total**. "100×" equals the *total-cost* ratio `(Q₂/Q₁)²` for a **10×** size jump — i.e. it conflates the **total** impact cost with the **per-unit** drag, and assumes a base of \$5M rather than the block's \$10M.

**Fix:** state the order value implied by the block (\$10M) and drop or correct "$200M-ADV"; rewrite as "a position 5× larger carries 25× the total impact cost (5× per unit)."

---

## FINDING 4 — MINOR · folder-wide `S` notation clash (`index:34,38,41`, `03:32–33` vs `01:36`, `02:38`)

- **01:36** — `S = a − b` (quoted, absolute) and `s = (a−b)/m` (relative). **02:38** — same. Both correctly cite **Foucault eq. 2.1**, whose source definition is exactly `S = a − b`, `s = (a−b)/m` (`corpus/verified/foucault_ch1-3.md:31`).
- **index:34** notation line — "`S=(a-b)/m` **relative** quoted spread"; **index:38** row "**Relative spread** `S=(a-b)/m`"; **index:41** uses "`S = 20 bp`" as a *relative* spread. **03:32–33** likewise calls `S` the "relative spread."

So `S` means the **absolute** spread in 01/02 and the **relative** spread in index/03 — directly opposite. A reader hopping from 03 back to 01 will mis-scale by the price level.

**Fix:** adopt the source convention everywhere — `S = a − b` (quoted), `s = (a−b)/m` (relative) — and in index/03 rename the relative spread to `s` (and `σ_s`).

---

## FINDING 5 — MINOR · hub prerequisite disagrees with sub-pages (`index:11`)

**Stated (`index:11`):** "**Basic Prerequisites:** `VaR & Expected Shortfall` **and** `Parametric, Historical & Monte Carlo VaR`. *(these are the folder-level prerequisites for pages 02–06…)*"

But every sub-page's own prerequisite line is:
- 02 → 01 + VaR & ES · 03 → 02 + VaR & ES · 04 → 03 + VaR & ES · 05 → 04 + 03 · 06 → 04 + 05.

**No** page lists `parametric-historical-and-monte-carlo-var`. Either add it where intended or drop it from the hub's folder-level claim.

---

## FINDING 6 — TRIVIAL · "four orders of magnitude" (`02:93`)

The block prints Amihud `I` of **2.5×10⁻¹⁰** (mega), **1×10⁻⁸** (mid), **4×10⁻⁷** (small). Max/min = 1600 ≈ **10³·²**, i.e. **~3.2 orders**, not four. Fix: "three orders of magnitude (1600×)".

---

## FINDING 7 — TRIVIAL · imprecise `κ` parenthetical (`04:41`)

"If forced sales of size `S` move the price by `κS` (linear impact, `κ = 1/(D·m)`-like)". From `Δp = λq` with `D = 1/λ`, a sale of `x` shares moves the price by `x/D` *currency units*; there is no `m` in that mapping, and the page's own §3 code uses `move = impact_coef·sale/ADV`, i.e. `κ = impact_coef/ADV`. The `·m` looks spurious. Fix: drop the parenthetical or state the actual κ used by the code.

---

## FINDING 8 — NOTE (low confidence) · asserted `∝T` schedule-cost scaling (`03:25`, `05:34–36`)

**Claim:** "the *schedule* of forced execution adds cost that scales like **T** in the worst (linear-impact) case" (03:25), and the 05 table row "Impact cost of a rate-limited schedule | **∼T** (linear-impact)". Under standard Almgren–Chriss: temporary linear impact of an evenly-spread order ⇒ cost ∝ `Q²/T`; permanent linear impact ⇒ ∝ `Q²` (independent of T); timing risk ⇒ ∝ `σ√T`. None gives `∝T`.

The page's own arithmetic is internally consistent (`T/math.sqrt(T)`, `16/4 = 4×`), and it is hedged with "in the worst (linear-impact) case", so this may be an intentional bespoke model — but it needs to be stated. Flagging for the author to either derive the `∝T` term or soften it.

---

## Verified-correct (no action)

**Boxed/display formulas — all correct:**
- `LC_impact = Q²/2D = λQ²/2` (03:37, boxed) ✓ — VWAP half-move, `k`-independent; matches index:40 and the index code (\$25,000).
- `LC_exog = ½V(S + z_α σ_S)` (03:33) ✓ — Bangia–Diebold–Schuermann–Stroughair; reproduces \$15,816.
- `L-VaR = VaR_market + LC_exog + LC_impact` (03:19,47; index:42) ✓.
- `T_liq = Q/(ADV·α)` (03:43) ✓ (0.25 d in index).
- `VaR_T = VaR₁√T` (index:44) ✓ (×3.162 at T=10).
- `P ≤ N/m ⟺ L = P/N ≤ 1/m` (01:41; index:45; 04:32) ✓.
- Amihud `I = |r_t|/Vol_t` (02:44; index:46) ✓ source eq 2.9.
- Roll `S_R = 2√(−cov(Δp_{t+1},Δp_t))` (02:47; index:47) ✓ source eq 2.18.
- Kyle `Δm_t = λq_t + ε_t`, `1/λ = depth` (02:41; index:39) ✓ source eq 2.8.
- Effective half-spread `S_e = d(p−m)` (02:39) ✓ source eq 2.3.
- `R ≃ r + s/h` (02:57; index:48; 06:34) ✓ source eq 9.6; regression `R_i = 0.0036 + 0.00672β_i + 0.211s_i` ✓ (exact, incl. the 0.00672 digit).
- Margin recursion `m_{t+1}=m_0+β·Vol_t`, `P^max=N_t/m_{t+1}`, `Sale=(P−P^max)⁺` (index:53) ✓.
- LCR `= HQLA/(30-day net outflows) ≥ 100%` (2013, d238); NSFR `= ASF/RSF ≥ 100%` (2014, d295) (index:59–60; 04:48–49; 06) ✓ — doc IDs correct.
- Spiral `S_total = S₀/(1−Lκ)` (index:49; 04:42; 06:31) ✓; `k=0.5 ⇒ ×2` ✓; pole at `k=1` ✓.
- Fire-sale `Cost_i = (κ/2)Q_iQ_agg` (social) vs `(κ/2)Q_i²` (private) (05:39) ✓ — two funds ⇒ 100% understatement ✓.
- `m = z_α σ_MPOR = z_α σ√(Δt_MPOR)` (02:53; 04:38; 05:43) ✓.
- Square-root impact `Δp = σY√(Q/V)`, `Y~O(1)` (06:27) ✓; L-CAPM four betas (06:35) ✓ source eq 9.18, "~1.1%/yr dominated by β4" ✓; DG–P search spread (06:38) ✓ source eq 9.15.
- Stoll (2000) via Foucault: `λ>0` for 98%, significant 63%; 0.75% smallest-cap vs 0.52% largest (02:42) ✓ — verbatim from `foucault_ch1-3.md:41`.
- Roll biases: underestimate by `2√(η(1−η))`, by `2(1−δ)`, Choi–Salandro–Shastri `δ≈0.7 ⇒ ~0.6` (02:99) ✓ source.
- 01 examples: 10 bp on \$12.5M = \$12,500 ✓; haircut 2%→50× … 10%→10× = 80% leverage loss ✓; 5× lev, 3% drop = 15% equity ✓.
- 04 simulation (defaults) output fence reproduced character-for-character, incl. total \$37.29M / 74.6% and 3.62% round-1 move ✓.
- 06 amplification block: every converging row matches `1/(1−k)`; k=1.00 row correctly DIVERGES ✓.

**CITATIONS:** all corpus references resolve to real verified digests; BCBS doc numbers (d238/d295/d457), journal/vol/page fields (RFS 22(6):2201–2238; JEP 23(1):77–100; JFM 5(1):31–56; JFE 77(2):375–410; Econ. 73(6); JF 39(4)/52(1)/66(3); JPE 111(3)) check out.

**LINK CHECK:** 0 broken wikilinks across the 7 files. The "flat note" targets (`pillars/04-quantitative-risk/liquidity-risk-and-margin-spirals`) and the cross-pillar execution/portfolio bridges all resolve. `index:24` correctly mirrors the folder's own §1 framing; hub↔sub-page §-routing (`(§5)`→05, `(§4)`→04) is coherent.

---

## Code-block execution log

Extracted 7 ```python/```output fence pairs (one per file, incl. `index.md`) and ran each under Python 3:

| File | Block | Result |
|---|---|---|
| `index.md` | L-VaR formula engine | **MATCH** (rc=0) |
| `01-from-zero-intuition.md` | market + funding cost | **MATCH** (rc=0) |
| `02-market-vs-funding-liquidity.md` | Amihud + VaR-margin | **MATCH** (rc=0) |
| `03-liquidation-cost-and-lvar.md` | VaR/L-VaR/horizon | **MATCH** (rc=0) |
| `04-margin-and-funding-spirals.md` | margin-spiral sim | **MATCH** (rc=0) |
| `05-failure-modes-and-practice.md` | externality + horizon | **MATCH** (rc=0) |
| `06-advanced-extensions.md` | amplification multiplier | **MATCH** (rc=0) |

**7 of 7 blocks run and reproduce their output fences exactly** (stderr empty, rc=0 for all).
