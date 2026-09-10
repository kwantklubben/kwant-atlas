# Audit — `content/pillars/04-quantitative-risk/risk-factor-sensitivities/`

**Date:** 2026-09-10 · **Reviewer:** sole adversarial reviewer (per-folder pass)
**Files checked:** 7 (hub + 01–06) · **Code blocks run:** 7 · **Code/output mismatches:** 0
**Verdict:** CONDITIONAL PASS — every numeric claim and every code block reproduces exactly; **6 defects** found (2 genuine math defects, 1 internal contradiction, 1 imprecise magnitude claim, 1 typo, 1 citation mislabel).

---

## 1. Code execution (run every block, diff stdout vs fence)

All ```` ```python ```` blocks were extracted, executed under `python3` (stdlib only), and their stdout compared **byte-for-byte** against the following output fence.

| Block | File | Result |
|---|---|---|
| 0 | `index.md` (L81–143) | ✅ exact match |
| 0 | `01-from-zero-intuition.md` (L66–88) | ✅ exact match |
| 0 | `02-delta-gamma-vega.md` (L63–104) | ✅ exact match |
| 0 | `03-rates-and-key-rate-duration.md` (L65–110) | ✅ exact match |
| 0 | `04-factor-exposures.md` (L65–104) | ✅ exact match |
| 0 | `05-failure-modes-and-practice.md` (L66–101) | ✅ exact match |
| 0 | `06-advanced-extensions.md` (L74–131) | ✅ exact match (incl. 2 M-rep Monte Carlo, seed 20260910, deterministic) |

**Blocks run: 7. Zero mismatches.**

---

## 2. Math verification (every boxed formula + worked example)

Independently re-derived (not just re-run) and confirmed **correct**:

- **Greeks (index:39–43, 02:41–45).** Δ, Γ, ν, Θ, ρ match Haug Table 2-3 values (0.503105 / 0.026794 / 0.192999 / −0.036989 / 0.109656). Θ defined as −∂V/∂T is consistent with the coded formula (both equal ∂V/∂t). Gamma–theta identity ½ΓS²σ² = −Θ_driftless exactly reproduces 5.471732 (02:29, 02:51, 05:100/112).
- **Vanna/Volga (02:51).** ∂Δ/∂σ = −e·n(d1)·d2/σ ✔; volga = ν·d1d2/σ ✔; ν = ΓσS²T ✔.
- **Forward/futures Greeks (02:55).** Δ_fwd = e^{−qT}, Δ_fut = e^{(r−q)T}, H_F = e^{−(r−q)T}H_A — matches `corpus/verified/hull_ch19-23.md` (eq 19.5/19.6) ✔.
- **Book aggregation (02:22, 02:113).** Net Δ=73.9422, Γ=1.3816, ν=18.8943, Θ=−1.2743, ρ=30.2788; short-put gamma contribution −1.3543 and delta contribution +14.17 all verified ✔.
- **Rates (03:34–53).** D_mod, 𝒞, DV01, KRD definitions and the central-difference KRD/2h↔bp identity are correct; Σ KRD = parallel DV01 holds to 1.42e−14 ✔. Hand-checked node-1 KRD (0.000925) and node-5 KRD (0.043467) from first principles ✔.
- **Factor model (04).** σ_p² = bᵀΣ_f b + wᵀDw ✔; Σ = BΣ_f Bᵀ + D ✔; parameter collapse K(K+1)/2+K = 44 vs N(N+1)/2 = 125,250 ✔; Euler derivatives ∂σ_p/∂b_k = (Σ_f b)_k/σ_p and ∂σ_p/∂σ_ε,i = w_i²σ_ε,i/σ_p ✔; component-vol allocation sums to σ_p = 2,282.44 and equals the variance share ✔.
- **Quadratic-form moments (index:70, 06:40–44).** E=b, Var=a²+2b², γ₁=(6a²b+8b³)/(a²+2b²)^{3/2}, γ₂=(3a⁴+60a²b²+60b⁴)/(a²+2b²)²−3 — all re-derived from Z-moments ✔. Pure-gamma limit a=0 gives γ₁=2√2, γ₂^ex=12 = χ²₁ moments ✔.
- **Cornish–Fisher (index:73, 06:50–53).** Coefficient form and the loss-skew sign flip (z^CF(−γ₁, γ₂), VaR = −E[ΔV] + √Var·z^CF) correct ✔.
- **All quoted percentages** (247%, +71%, 33%, 29%, 4.2%/8.5%, 109.44%, ±7.41%/−6.19%, 77.6%, 12.6%, R²=0.874, 45% trading-vs-calendar theta) recomputed ✔.

---

## 3. Defects found

| # | File:line | Severity | Stated | Correct |
|---|---|---|---|---|
| 1 | `05-failure-modes-and-practice.md:49` | **logic / internal contradiction** | Vanna row: “**spot and vol fall together**” | In an equity selloff spot falls while implied vol **rises** (the leverage effect). This contradicts the same file at **05:52** (“spot falls and implied vol rises”) and contradicts the sign convention ΔS<0, Δσ>0 used everywhere else. Should read e.g. “spot falls and vol rises together”. |
| 2 | `05-failure-modes-and-practice.md:58` | **math (dimension)** | “its **variance is ½Γ²S⁴σ⁴Δt**” for the step-Δt P&L of 05:56 | Per-step variance is **½Γ²S⁴σ⁴Δt²** (the Δt must be squared; otherwise the units are currency²·time, not currency²). Accumulated over horizon T it is ½Γ²S⁴σ⁴·T·Δt. **MC-confirmed**: with dt=1/252, 1/1000, 1/10000 the empirical variance scales as dt² (1.416e−3 → 8.96e−5 → 8.95e−7). |
| 3 | `02-delta-gamma-vega.md:119` | **math (magnitude)** | delta-hedged P&L “realised with standard deviation proportional to **\|Γ\|S²σ√Δt**” | Per-step std is **∝ Γ²…→ ΓS²σ²Δt** (σ squared, Δt not √Δt); even under the intended (aggregate) reading it is ∝ ΓS²σ²√(TΔt). σ should be σ² — the text is also inconsistent with the sibling formula at 05:56/05:58. |
| 4 | `02-delta-gamma-vega.md:47` | **math (prose claim)** | “gamma and vega … both peak at-the-money and **decay with √T**” | Only **gamma** decays (∝1/√T). **ATM vega grows with maturity** (∝√T): verified numerically — ATM raw vega = 12.54 (T=0.1), 19.64 (0.25), 27.36 (0.5), 37.52 (1.0), 49.91 (2.0). |
| 5 | `01-from-zero-intuition.md:106` | **spelling** | “floating-point **cancelation**” | “**cancellation**” (also the only US/GB-inconsistent spelling; the file otherwise uses GB “modelling”). |
| 6 | `01-from-zero-intuition.md:114` | **citation mislabel** | “Hull … **Ch 21 §21.8 (computing Greeks from a finite-difference grid** — the same central-difference idea used here)” | Per `corpus/verified/hull_ch19-23.md`, §21.8 is Hull’s **finite-difference *pricing* machinery** (implicit eq 21.27 / explicit eq 21.34 / Crank–Nicolson), not a Greeks-from-grid section. The bump-and-revalue/central-difference method described here is Hull’s numerical-Greeks material, not §21.8’s PDE grid. |

### Non-counted cosmetic notes
- `index.md:145` (and the print label in the code at `index.md:105`): the output label reads “**Haugar:**” — a typo for “Haug”. It sits inside a code fence/print string, so it is **excluded by the spelling rule**, but it renders in the document and is inconsistent with `02`, which prints “Haug call:”.
- `index.md:50` claims “Every table in this folder states its convention in the header.” The hub and 06 tables are fine, but the `02` and `05` tables carry no unit convention in the header (units are stated in surrounding prose). Soft overclaim.

---

## 4. Coherence

- **Hub ↔ sub-pages:** hub §6 sub-page list (01–06) matches the actual files; hub’s stated folder prerequisites for 02–06 are satisfied by each page’s own stated prerequisites; hub:12 correctly notes page 01 has smaller entry requirements (01:11 = calculus only) ✔.
- **Jargon:** *vanna/volga* first used in hub §2 but defined on `02` (acceptable signposting); *key-rate duration*, *Euler/component volatility*, *cross-gamma* all defined before use in their pages ✔.
- **Links:** all **29** wikilink targets resolve to real files/dirs — **zero dead links** ✔.
- **No contradictions found** between hub and pages on units/scaling (Vega/Rho per 1 pt = raw/100, Theta per day = raw/365, DV01 per bp = ×10⁻⁴ are stated identically in hub:44/50, 02:47, 03:22) — apart from defect #1 above.

## 5. Summary

The folder is numerically sound: **all 7 code blocks reproduce their fenced stdout exactly**, and the entire formula set (Greeks, DV01/KRD ladder, duration/convexity, factor/Euler decomposition, quadratic-form moments, Cornish–Fisher VaR) is correct. The defects are localized: one internal contradiction (05:49), one dimensional error in a variance statement (05:58), one imprecise std-scaling claim (02:119), one incorrect maturity-scaling claim for vega (02:47), one typo (01:106), and one citation mislabel (01:114).
