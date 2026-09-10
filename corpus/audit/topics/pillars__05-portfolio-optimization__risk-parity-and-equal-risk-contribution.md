# Audit — `content/pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/`

**Reviewer:** sole, adversarial · **Date:** 2026-09-10
**Files:** 7 (index + 01…06) · **Code blocks:** 8/8 extracted and executed · **Verdict:** PASS WITH FIXES

---

## 1. Verdict

The folder is **structurally sound and mathematically correct in its core apparatus.**
Every boxed/citable formula (MRC `(Σw)_i/σ`, RC `w_i(Σw)_i/σ`, Euler decomposition,
ERC condition `w_i(Σw)_i=w_j(Σw)_j`, two-asset and constant-correlation closed forms,
beta form, the convex barrier / KKT stationarity, and the risk-budgeting program) re-derives
correctly, and **all eight `python` blocks run to completion and reproduce their documented
output fences byte-for-byte** (`rc=0`, exact string match). The Maillard et al. (2010)
worked universe and the Asness et al. (2012) flat-SML reconstruction reproduce exactly:
ERC weights `[0.384, 0.192, 0.243, 0.182]`, `σ_erc = 0.102934`, equal `RC = 0.0257`,
budget-tilt `[0.493, 0.190, 0.194, 0.123]`, tangency `≈88/12`, levered-parity Sharpe `0.550`.

Defects are **localized and non-fatal**: one **subscript-swapped closed form** in the hub
(it contradicts the page's own numeric check *and* the sibling sub-page), one **duplicated
volatility subscript** in page 05, and one **stray `?` superscript** in a page-06 inequality.
No wrong sign in the core formulas, no wrong constant in any worked number, no non-running
code, no broken link.

---

## 2. Issues

| # | file:line | Problem | Fix |
|---|---|---|---|
| 1 | `index.md:48` | **Two-asset ERC closed form has the subscripts swapped.** Hub states `$w_1=\dfrac{\sigma_2^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}},\; w_2=\dfrac{\sigma_1^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}}$`. For the hub's own check numbers (`σ1=15.1%, σ2=4.6%`) this gives `w1 = 0.7665`, but the very same table cell reports `w=[0.234, 0.766]` — i.e. `w1 = 0.234`. The correct form (which *is* given correctly in `03-equal-risk-contribution.md:46`) is `w_i = σ_i⁻¹/(σ1⁻¹+σ2⁻¹) = σ_j/(σ1+σ2)`. Independent re-derivation (Euler RC equalization ⇒ `w₁²σ₁² = w₂²σ₂²`, ρ cancels) confirms `w1 = σ1⁻¹/Σ = 0.2335`. | Rewrite as `$w_1=\dfrac{\sigma_1^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}}=\dfrac{\sigma_2}{\sigma_1+\sigma_2},\; w_2=\dfrac{\sigma_2^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}}=\dfrac{\sigma_1}{\sigma_1+\sigma_2}$` (match page 03). |
| 2 | `05-failure-modes-and-practice.md:43` | **Duplicated volatility subscript.** "Equity $\sigma_b=18\%$, bonds $\sigma_b=6\%$" — both legs labelled `σ_b`; the equity leg should be `σ_e` (or `σ_E`). The block's code correctly uses `ve, vb = 0.18, 0.06`, so this is a prose-notation slip only. | `Equity $\sigma_e=18\%$, bonds $\sigma_b=6\%$`. |
| 3 | `06-advanced-extensions.md:27` | **Malformed LaTeX / stray character.** The flat-SML inequality reads `$\frac{\mu_B-r_f}{\sigma_B^{?}} > \frac{\mu_S-r_f}{\sigma_S}$` — the `^{?}` is a stray placeholder superscript and renders a literal `?` on the denominator. | `$\frac{\mu_B-r_f}{\sigma_B} > \frac{\mu_S-r_f}{\sigma_S}$`. |

**Nitpicks (not counted as errors):**

- `index.md:124` — lowercase mid-sentence acronym: "…a *negative* correlation ($\rho=-0.5$) with asset 4 that **erc** exploits as free diversification." Should be uppercase **ERC** (all other occurrences are uppercase).
- `index.md:24` — "the check-column numbers were re-executed and reproduced exactly from the **verified corpus** (§3)." The worked universe (Maillard–Roncalli–Teïletche; Qian) is **not** present in `corpus/verified/` (that directory holds only bergomi/bjork/bm/duffy/esl/foucault/gatheral/glasserman/gregory/hasbrouck/haug/hull/shreve/tsay). The numbers *are* reproduced — by the hub's own §3 code, not by a verified source file. Consider "…re-executed in §3 below" and note the primary source is not in `corpus/verified/`.
- `01-from-zero-intuition.md:18` vs `:26` — the eggs illustration quotes "15% stock vol and 5% bond vol" while the carried worked example uses "σ_E=15.1%, σ_B=4.6%" (both attributed to Qian). Approximately consistent; harmonic, but the two number sets in one page invite confusion.

---

## 3. Math verified (re-derived independently)

| Formula (location) | Check | Result |
|---|---|---|
| MRC `(Σw)_i/σ(w)` (index:43, 02:38–43) | ERC universe ⇒ `[0.0671, 0.1342, 0.1061, 0.1414]` | ✓ exact |
| RC boxed `w_i(Σw)_i/σ(w)` (index:44, 02:47) | ERC ⇒ `0.025734` each; pct `25.00%` each | ✓ |
| Euler `σ=Σ RC_i` (index:46, 01:42, 02:47) | `Σ RC = 0.102934 = σ`, `|diff|<1e-9` | ✓ |
| ERC condition `w_i(Σw)_i=w_j(Σw)_j` (index:47, 03:40) | equivalent to `w₁²σ₁²=w₂²σ₂²` (ρ cancels) | ✓ |
| **Two-asset closed form** (index:48) | stated form gives `w1=0.7665` ≠ tabulated `0.234` | ✗ see issue #1 |
| Two-asset closed form (03:46) | `w1=σ1⁻¹/Σ=0.2335`, `w2=σ2⁻¹/Σ=0.7665`; ρ-independent | ✓ |
| Constant-correlation ERC `w_i=σ_i⁻¹/Σσ_j⁻¹` (index:49, 03:51) | vols 10/20/30/40 ⇒ `[0.48,0.24,0.16,0.12]` | ✓ |
| Beta form `w_i∝β_i⁻¹`, `β_i=(Σw)_i/σ²` (index:50, 03:55–59) | `RC_i=w_iβ_iσ`; ERC ⇒ `w_iβ_i=const` ⇒ `w_i∝β_i⁻¹` | ✓ |
| Risk budgeting `RC_i=b_iσ(w)` (index:51, 04:32) | `b=[.4,.3,.2,.1] ⇒ w=[0.493,0.190,0.194,0.123]`, realized `40/30/20/10` | ✓ |
| `b=[.5,.3,.1,.1] ⇒ w=[0.566,0.178,0.146,0.110]`, realized `50/30/10/10` (04:92) | code output | ✓ |
| Volatility ordering `σ_mv≤σ_erc≤σ_1/N` (03:28, index:140) | barrier family `Σln w_i≥c`; `c=−NlnN` is the **max** of `Σln w_i` (AM–GM) ⇒ binding ⇒ 1/N; `c=−∞` ⇒ MV | ✓ |
| Two-asset 60/40 risk share (01:78, index:17) | `σ=0.09599`, equity share `=0.9271` | ✓ 92.7% |
| Parity `wE=0.2335, wB=0.7665, σ=0.0546`, share `50.0%` (01:79) | code output | ✓ |
| Qian loss-contribution `c_i=p_i+D_i/L` (02:57) | formula well-formed | ✓ |
| 1/n decomposition `MRC/RC/pct` = `12.3/26.4/14.2/47.2%` (02:92–94, index:115) | code output | ✓ |
| 05 Failure A: `1.83×` at ρ=−0.4; `14.70%` realized at ρ=+0.6 → **63% overshoot** (05:62–69) | `0.1470/0.0900=1.633` | ✓ |
| 05 Failure B: est `w=[0.430,0.215,0.203,0.152]`; realized on true Σ `32.1/32.1/17.9/17.9` (05:99–103) | code output; prose "32/32/18/18" consistent | ✓ |
| 06 flat-SML `(μ_B−r_f)/σ_B > (μ_S−r_f)/σ_S` (06:27) | math content correct; **`σ_B^{?}` typo** | ✗ see issue #3 |
| 06 Sharpe `stocks 0.381 / bonds 0.471`; tangency `w=[0.116,0.884]`, SR `0.554` (06:80–81) | `0.072/0.189=0.381`, `0.016/0.034=0.471`; S⁻¹x normalized | ✓ |
| 06 parity `w=[0.152,0.848]`, `σ=0.0446`, `L=4.23×`; levered Sharpe `0.550`; edge `≈3.19 pp` (06:82–88) | code output; `10.39−7.20=3.19` | ✓ |

---

## 4. Code stats

| File | Block | Runs | Output fence |
|---|---|---|---|
| index.md | risk-budget engine (ERC + inverse-vol + budgets) | ✓ rc=0 | exact match |
| 01-from-zero-intuition.md | two-asset 60/40 vs parity | ✓ rc=0 | exact match |
| 02-risk-contributions.md | 1/n MRC/RC/Euler decomposition | ✓ rc=0 | exact match |
| 03-equal-risk-contribution.md | ERC by CCD + inverse-vol compare | ✓ rc=0 | exact match |
| 04-risk-budgeting.md | arbitrary budgets (3 vectors) | ✓ rc=0 | exact match |
| 05-failure-modes-and-practice.md | Failure A: correlation-regime leverage | ✓ rc=0 | exact match |
| 05-failure-modes-and-practice.md | Failure B: wrong-Σ misallocation | ✓ rc=0 | exact match |
| 06-advanced-extensions.md | flat-SML / tangency / levered parity | ✓ rc=0 | exact match |

**8/8 blocks run; 8/8 reproduce their documented stdout exactly.** Stdlib-only (`math`) —
no dependency risk. All deterministic (no RNG), so cross-machine reproducible. Note: the
CCD solvers sweep 3000–6000 iterations; results are stable and match the fences to the
printed precision.

---

## 5. Links & coherence

- **Wikilinks in folder: 80 total** (index 20, 01 11, 02 10, 03 11, 04 9, 05 11, 06 8).
  **All 80 resolve** to an existing `content/` file or folder-hub.
- **Hub ↔ 01 prereq line consistent:** `index.md:11` scopes the folder prerequisites
  (linear algebra + calculus) to pages `02`–`06` and explicitly defers page `01` to its own
  smaller entry requirements; `01-from-zero-intuition.md:10` says "none — this page needs no
  prior finance theory." No conflict.
- **Hub ↔ sub-page coherence:** index §2 lookup table is fully consistent with the sub-pages
  (ERC weights, σ, RC, budgets, constant-correlation form, beta form) — the **sole**
  divergence is the hub's swapped two-asset closed form (issue #1), which the numeric column
  and `03:46` both contradict.
- **Jargon first-use:** MRC/RC defined at 02:20–22 and index:43; ERC at index:22/03:16;
  risk budgeting at 02:16/04:16; CCD at 03:69; BAB / leverage aversion / HRP at 06:29/06:99.
  All defined at or before first substantive use. Clean.
- **Cross-page claims consistent:** "92.7% equity risk" (index:17 ↔ 01:78); "47.2% of risk in
  asset 4" (02:98 ↔ 03:26); "inverse-vol 39.1/39.1/10.9/10.9" (03:117 ↔ index:119–124);
  "32/32/18/18" (05:29 ↔ 05:100). No contradictions found beyond issue #1.
- **Bridges resolve** to sibling topics (`modern-portfolio-theory-and-mean-variance`,
  `covariance-shrinkage-and-denoising`, `hierarchical-risk-parity`,
  `constraints-and-transaction-costs`) and `foundations/*` / `pillars/04-quantitative-risk`.
- **Terminology:** "risk parity" vs "risk budgeting" vs "ERC" used consistently with the
  stated ERC ⊂ risk-budgeting generalization.

---

## 6. Notes / caveats

- The **Maillard–Roncalli–Teïletche (2010)**, **Qian (2005, 2006)**, **Asness–Frazzini–Pedersen
  (2012)**, **Griveau-Billion–Richard–Roncalli (2013)**, **Black (1972)**, **Litterman (1996)**,
  **DeMiguel et al. (2009)**, **Ledoit–Wolf (2004)**, **Hallerbach (2003)** and
  **López de Prado (2016)** sources are **not present in `corpus/verified/`**. Every numeric
  claim was therefore validated by independent re-derivation / re-execution here, not against
  source text. This is the one place the folder's own "verified corpus" wording (index:24)
  overstates its grounding.
- The four worked-universe inputs (vols `10/20/30/40%`, `ρ12=0.8`, `ρ34=−0.5`) are constant
  across all eight blocks, so every block is self-contained and deterministic; no cross-block
  imports. Blocks were run with `python3` from the repo root.
- No spell-checker dictionary is installed on the host (`hunspell -D` → no `en_US`), so the
  prose pass was a manual read plus a programmatic scan for doubled words, stray math tokens,
  and unbalanced `$$` (all clean except the items listed).
