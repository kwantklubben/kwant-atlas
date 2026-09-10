# Audit: pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss

**Folder under review:** `content/pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/` (7 files: index + 6 sub-pages)
**Date:** 2026-09-10 · **Reviewer:** sole adversarial reviewer
**Method:** all 9 ```python blocks extracted and executed; formulas re-derived and re-computed independently; wikilinks resolved against the live tree; prose scanned for typos/doubled words/TeX-escape leakage.

---

## Verdict

**CLEAN (2 minor wording defects + 1 rendering defect + 1 unsupported figure).** Core math, all boxed formulas, all worked numeric examples, and all code blocks verified correct and self-consistent. The Almgren–Chriss engine (κ, θ, sinh trajectory, E/V, HJB, T\*=√3θ, OW block-continuous-block, dark-pool threshold, square-root-law penalty) is numerically exact. No mathematical error found.

---

## 1. Spelling / typography (excludes code & LaTeX)

- **[DEFECT — rendering]** `04-efficient-frontier-and-trajectory.md:105` — prose reads `the na\"ive (TWAP) strategy`. The `\"` is a TeX acute-accent macro that Markdown does **not** process; it will render a literal `na\"ive` (backslash + quote). Should be `naïve` (or plain `naive`, used elsewhere: `04:29`, `index:26`). One occurrence; searched all 7 files, the only `\"` leak.
- No doubled words (`is is`, `the the`, …) found in any file.
- No spelling/typo errors in prose identified (author names, journal refs, parameters all spelled correctly; accents on Almgren→Almgren, Obizhaeva, Gueant, Penalva, Kukanov, Sasha, Hauptmann correct).

## 2. Math verification

Every boxed formula and worked example was re-derived/independently recomputed. All correct. Details per page:

### index.md
- `E[x]=½γX²+εΣ|n_k|+(η̃/τ)Σn_k²`, `V[x]=σ²Στx_k²`, `η̃=η−½γτ` (line 41): correct (AC eqs 4-5,8). ✓
- `n_j = [2 sinh(½κτ)/sinh(κT)]·cosh(κ(T−t_{j−½}))·X` (line 51): verified against `−diff(x_j)` — max error **5.9e-10** shares. ✓
- Lookup values (lines 59-67) all recomputed: κ=0.6011/d, θ=1.6635 d, κT=3.006, x(1d)=545,055, x(T/2)=212,003, TWAP E=$644,500, AC E=$921,572, TWAP sd=$1,222,765, AC sd=$850,375, T\*=2.883, 12.4% sqrt-law penalty. All match. ✓
- **[MINOR]** Line 59 writes the urgency lookup as `κ=√(λσ²/η)=0.6011`. Substituting the stated η=2.5e-6 gives **0.6008**; the printed 0.6011 is produced by the discrete-sanitized `η̃=η−½γτ` (and matches the code on line 85 which deliberately uses `etat`). Formula notation loose (η vs η̃); value correct. Page 04:39 writes the same quantity correctly with `η̃`.
- **[MINOR]** θ reported both as 1.6635 (line 60, from κ with η̃) and 1.664 (line 67, from η) in the same hub table. Both round to the printed T\*=2.883; benign rounding, but a reader sees two θ values.

### 01-from-zero-intuition.md
- Two cost curves, page 01:44: `T\*=√(3η/λσ²)=√3θ`, `θ≡√(η/λσ²)=1/κ`. Recomputed: θ=1.6644 d, T\*=2.8828. Correct. ✓
- Uses simplified E (drops εX, uses η not η̃) — explicitly labeled "approximate" (§2/§3 code); self-consistent with its own output. Cf. hub full-cost E=$644,500 vs page-01 approx E(5d)=$625,000. Acceptable given the "≈" framing. Not flagged as error, but noted: page 01 and hub use different E conventions (page-01 ~ is the no-ε, η version).

### 02-the-execution-problem.md
- IS decomposition, effective/realized cost (str. 32,37): correct (Perold 1988; Hasbrouck 14.1-14.2). ✓
- `E[x]`,`V[x]` (str. 46,50): correct. ✓
- Decomposition worked example (str. 103): εX=$20,000 + ½γX²=$125,000 = $145,000; temp = η̃X²/T = 2.4975e-6·1e12/5 = **$499,500**; total $644,500. Verified exactly. ✓

### 03-the-almgren-chriss-model.md
- Discrete stationarity eq, `κ̃²=λσ²/η̃` (str. 40-41); Euler–Lagrange `ẍ=κ²x`, `κ=√(λσ²/η)` (str. 52); sinh trajectory + n_j (str. 47-48): all correct. ✓
- HJB (str. 62-68): `−V_t = min_ν[εν+ην²−νV_x]`, FOC `ν\*=(V_x−ε)/2η`, `−V_t=−(V_x−ε)²/4η`, ansatz `V(t,x)=εx+ηx²/(T−t)` giving ν\*=x/(T−t) and V(0,X)=εX+ηX²/T = $520,000. Re-derived and numerically checked — residual ≈ **1e-14** (machine level). ✓
- **[MINOR / unsupported figure]** Str. 128 claims "maximum relative residual **8.94e-10**" for the HJB ansatz. No code block computes this number (the §3 block solves the discrete optimum, not the HJB). Independent check yields ~1e-14, so the claim is *conservative, not wrong* — but the specific figure 8.94e-10 is uncorroborated and not reproducible from the given code.

### 04-efficient-frontier-and-trajectory.md
- Convexity, tangency `dE/dV|_λ=−λ`, front-table values, "naive TWAP never efficient" claim, λ=1e-7 cost/risk deltas ($7.7k cost for $67k sd cut — rechecked from table: ΔE=7,688, Δsd=67,416 ✓). All correct. ✓

### 05-failure-modes-and-practice.md
- Square-root law, `Σ n_k h(n_k/τ)=η τ^{−α} Σ n_k^{1+α}` (str. 34), concave-per-share/convex-in-n argument, characteristic-time scaling `T_⋆∝X^{(α−1)/(α+1)}`: mathematically sound. ✓
- **Experiment A** (str. 52-96): AC schedule over-pays **12.40%** ($145,717) under √law; quarter splits (AC 52.95/25.85/12.94/8.26 vs sqrt 74.44/16.23/5.88/3.45): reproduced exactly. ✓
- **Experiment B** (str. 102-137): 22.57% loss for 4× under-estimate; **defect in prose** (see below).
- **[DEFECT — wording]** Str. 146 says "**10.3% for a 4x over-estimate**". The printed 10.30% corresponds to used λ=1e-5 with true λ=4e-6, i.e. a **2.5× over-estimate**, not 4×. Independently computed: the true 4× over-estimate (λ=1.6e-5) costs **24.11%**, not 10.3%. The 22.6%-for-4×(under) figure is correct; the companion over-estimate figure is mislabeled. Fix: "10.3% for a 2.5× over-estimate."

### 06-advanced-extensions.md
- Nonlinear-impact characteristic time `T_⋆=(αηX^{α−1}/λσ²)^{1/(α+1)}` (str. 30), finite-`T_max` formula (str. 31): consistent with Almgren (2003); no numeric example to reproduce (cited result).
- OW cost/resilience recursion (str. 36): correct recursion.
- **Defect below** on the OW-symmetry claim.
- Dark-pool threshold (str. 48, 107-130): `p\*=δ/(c_lit+δ)=1.25/3.76=0.3324`, table reproduced exactly. ✓
- **[DEFECT — code/prose mismatch]** Str. 103 claims the OW symmetry is "an exact check: in the risk-neutral limit (λ=0) the two blocks are equal to machine precision (n1/nN=1.000000 for ρ=0.05,0.2,0.5)". **The displayed code block (str. 60-94) runs λ=1e-6** (see `sigma, lam = 0.95, 1e-6`), whose output shows n1≠nN (86,212 vs 61,309 at ρ=0.05), and its loop is over ρ=(0.05,0.15,0.40,0.90) — **ρ=0.2 and 0.5 never appear**. I independently ran the model at true λ=0: the symmetry does hold exactly (n1=nN for ρ=0.05,0.2,0.5). So the *mathematics is correct*, but the claim is **not demonstrated by the shown code** and cites ρ values the block never runs. The λ=0 verification belongs in a (missing) risk-neutral block; the current table is explicitly a λ=1e-6 run.

## 3. Code verification

All 9 ```python blocks extracted and executed; **every documented output fence matches stdout exactly** (byte-for-byte, incl. the 12.4%, 22.57%, 0.3324, 545,055, MC mean=645,241, OW quarter-splits). `blocks_run = 9`, `blocks_failed = 0`.

## 4. Coherence & links

- **Hub ↔ 01 prerequisites:** index:11 correctly states hub prereqs apply to pages 02-06, "page 01 states its own, smaller, entry requirements"; page 01 says "None." Consistent. ✓
- **Jargon first-use:** TWAP defined at 01:35; VWAP at index:23; η/γ/ε/λ/κ/θ all defined at index:31 before use. `L-VaR` first appears unexpanded in the index lit-reference block (index:132) and is used without definition at index:63,66 — minor (defined later pages). Not flagged as error.
- **Internal folder links (01↔…↔06, index):** all resolve (verified each `…/optimal-execution-and-almgren-chriss/0X-…` target exists).
- **Cross-folder hub links:** the 9 bare-folder links (e.g. `[[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|…]]`) point at a *folder* name, not `<folder>/index`. No such `.md` exists at that path; the hubs live at `<folder>/index.md`. **However** this is repo-wide convention (same bare-folder style used 20×/32×/19× elsewhere across the tree and mixed with `/index` variants), not a defect specific to this folder — so not scored as an error here.
- `hasbrouck_ch11-15.md` corpus reference resolves (file exists). ✓
- Verified sources list (Almgren-Chriss, Almgren03, OW13, Gatheral, Cont et al, BL98, Hasbrouck, Cartea et al, Gueant) matches §5 references. No contradicts between hub table and any sub-page numbers.

## Files / count

- Files checked: **7** (index + 6 sub-pages).
- Code blocks run: **9** (all pass, matching documented output).
- **Errors found: 3** substantive defects —
  1. `04:105` — `\"` TeX accent leaks into rendered prose (`na\"ive`); rendering defect.
  2. `05:146` — "10.3% for a 4x over-estimate" mislabel; the 10.30% is for a 2.5× over-estimate (a real 4× over costs 24.11%).
  3. `06:103` — OW λ=0 symmetry claim cites code output / ρ-values (0.2, 0.5; λ=0) that the displayed λ=1e-6 block never produces; claim true but not demonstrated and mismatched with the shown table.
- Minor (informational, not scored): index:59 η-vs-η̃ notation for κ; index θ 1.6635 vs 1.664; index:132 L-VaR first-use unexpanded; 03:128 HJB "8.94e-10" figure unsupported by any block.