# Audit — `content/pillars/01-quantitative-research/backtesting-hygiene/`

**Reviewer:** sole, adversarial · **Date:** 2026-09-10
**Files:** 7 (index + 01…06) · **Code blocks:** 7/7 extracted and executed · **Verdict:** PASS WITH FIXES

---

## 1. Verdict

The folder is **structurally sound and mathematically correct in its core apparatus.**
Every boxed/citable formula (FWER, EVT expected-max, exact order statistic, selection
threshold, DSR, PSR variance, MinTRL, Harvey–Liu `p_M`, Bonferroni/Holm, PBO/CSCV,
White Reality Check) re-derives correctly, and **all seven `python` blocks run to
completion with deterministic seeds and reproduce their documented output fences byte-for-byte**
(including the MC columns). The canonical Bailey–López de Prado worked example
(`SR=2.5`, `T=1250`, `V=0.5/ann`, `skew=−3`, `kurt=10`) reproduces exactly:
`E[max]=2.5306`, `SR0(ann)=1.7894`, `DSR(100)=0.8997`, `N*=45.96` (non-normal) / `87.73` (normal).

Defects are **localized and non-fatal**: one malformed LaTeX token, one cost-drag formula
that contradicts its own "per period" wording, one self-contradictory impact exponent, one
prose mislabel of a MinTRL number, and one internally inconsistent decision gate. No
wrong sign, no wrong constant, no broken link, no non-running code.

---

## 2. Issues

| # | file:line | Problem | Fix |
|---|---|---|---|
| 1 | `04-deflated-sharpe-ratio.md:117` | **Prose mislabels the MinTRL number as the *un*-penalised one.** Text: "a Sharpe-2.5 record needs only ~0.7 years *ignoring* non-normality". But the tabulated `168` days (~0.7 yr, §3 output) is the value **with** `sk=−3, kurt=10`. *Ignoring* non-normality gives `1+(\Phi^{-1}(0.95)/s)^2 ≈ 110` days (~0.44 yr). The "0.7 yr" is the penalised figure, not the un-penalised one. | Rewrite: "…needs ~110 days *ignoring* non-normality, stretched to ~168 days (0.7 yr) once skew −3 / kurt 10 are priced in — negative skew is expensive." |
| 2 | `05-failure-modes-and-practice.md:27–28` | **Cost-drag formula contradicts its own definition.** Prose: "turns over fraction τ of its book **per period** … net per-period return is rᵗ = rₜ − τc, so the net Sharpe is `SR_net = SR_gross − τc/σ_ann`". With per-period τ, the annualised drag is `τc·n/σ_ann` (n = periods/yr, e.g. 252), not `τc/σ_ann` — the stated formula is short by ×n and understates the drag by ~252× for daily data. It is only correct if τ is *annual* turnover. (The §3 code sidesteps this by applying per-period cost directly; its 5 bp → `net 1.16` line is what the per-period reading demands.) | Either change the wording to "…fraction τ of its book **per year**", or write the formula as `SR_net = SR_gross − τc·n/σ_ann`. |
| 3 | `05-failure-modes-and-practice.md:29` | **Self-contradictory impact exponent.** "Market impact adds a **quadratic** term ∝ (size/ADV)^{3/2}". "Quadratic" implies exponent 2; the empirical square-root law implies 1/2; `3/2` is neither, and the phrase pairs an incompatible adjective with the power. | Pick one: "a **square-root** impact term ∝ (size/ADV)^{1/2}" (the standard empirical law, Almgren–Chriss-style), or drop the adjective if a `3/2` power is genuinely intended and cite it. |
| 4 | `02-why-backtests-lie.md:54` | **Malformed LaTeX.** Table cell reads `$d$$ free params raise apparent fit` — the stray second `$` closes math early and leaks a literal `$` into the rendered table (only odd-`$` line in the folder). | `$d$ free params raise apparent fit`. |
| 5 | `05-failure-modes-and-practice.md:38` | **Decision gate contradicts page 06.** The gate requires `PBO ≤ 0.5`, but 06 (§3 reading, line 101) states "PBO > 0.5 **or near it** condemns the selection process". As written the gate passes a strategy with PBO = 0.50, which 06 explicitly calls a condemnation — too weak to be a gate. | Tighten to `PBO \ll 0.5` (e.g. `PBO ≤ 0.05`), or restate as "PBO substantially below 0.5". |

**Nitpicks (not counted as errors):**

- `03-the-multiple-testing-problem.md:50,133` — "overstates … by ~28% at N=100". Exact ratio `3.2250/2.5306 = 1.274` → **27.4%**. "~28%" is a loose round-up; consider 27%.
- **Sibling-link target inconsistency (link-following only).** This folder links siblings to the flat `.md` aliases `…/statistical-arbitrage-and-pairs-trading` (index.md:119, 05:137) and `…/signal-processing-and-kalman-filtering` (06:132), whereas the pillar index targets the folder hubs `…/statistical-arbitrage-and-pairs/index` and `…/signal-processing-and-kalman/index`. Both resolve (the flat files exist), so no broken link — but the two conventions should be unified.

---

## 3. Math verified (re-derived independently)

Reference for the ESL items: `corpus/verified/esl_ch6-10.md` (eq. 7.9 bias–variance ✓, 7.12 in-sample var `(p/N)σ_ε²` ✓, 7.24 optimism `(2d/N)σ_ε²` ✓, 7.32 `df=tr(S)` ✓, 7.48 K-fold ✓; §7.10.2 wrong-vs-right CV `3%` vs true `50%` ✓, §7.10.3 CV undershoot unless retrained per fold ✓). The DSR / Harvey–Liu / PBO / White sources are **not** in `corpus/verified/`; those were validated by re-derivation from the stated formulas.

| Formula (location) | Check | Result |
|---|---|---|
| FWER `1−(1−α)^N`; `α=0.05,N=100` (index:31, 03:34) | `1−0.95^100 = 0.99408` | ✓ 0.9941 |
| EVT `√(2 ln N)+γ/√(2 ln N)`, `N=100` (03:42) | `3.03485+0.5772/3.03485` | ✓ 3.2250 |
| Exact order stat `(1−γ)Φ⁻¹(1−1/N)+γΦ⁻¹(1−1/(Ne))` (03:45, 01:58, 04:68, index:33) | N=100→2.5306; N=1000→3.2551; N=10→1.5746 | ✓ all |
| Threshold `SR0 = √V·E[max Z]` (03:48, 04:39) | `√(0.5/252)·2.5306·√252 = 1.7894` | ✓ |
| PSR variance `(1−γ₃SR+(γ₄−1)/4·SR²)/(T−1)` (04:31) | algebra + Lo(2002) form | ✓ |
| **DSR** boxed (04:41, index:35) | `sr=0.157485, sr0=0.044544·2.5306=0.11274`, denom `√(1+3·0.157485+2.25·0.02480)=√1.5283=1.2363`; `Φ((0.157485−0.11274)·√1249/1.2363)=Φ(1.2794)` | ✓ 0.8997 |
| **MinTRL** boxed (04:53, index:36) | `SR=2.5/√252`, factor `=1+3SR+2.25SR²=1.5283`, `(Φ⁻¹(0.95)/SR)²=(10.4446)²` | ✓ 168 d |
| Harvey–Liu `t=SR√T`, `p_M=1−(1−p_S)^N` (03:54) | `0.75/√12·√240=3.3541`, `p_S=0.000796`, `p_M=0.14727`; `HSR=Φ⁻¹(1−p_M/2)/√240·√12` | ✓ 0.3241, 56.8% |
| Holm sequential (03:35) | `min{1,max_{j≤i}(N−j+1)p_(j)}` standard | ✓ |
| Effective-N `N̂≈ρ̂(M−1)+1` (index:41, 03:65, 05:33) | Bailey–LdP App. 3 | ✓ |
| PBO `ω̄=r̄/(N+1)`, `λ_c=ln(ω̄/(1−ω̄))`, `PBO=Pr[λ<0]` (06:44–46) | CSCV, C(10,5)=252 combos | ✓ 252 |
| White RC `V=max_k√n·f̄_k`, `V*=max_k√n(f̄*_k−f̄_k)` (06:52–55) | standard | ✓ |
| Coin example "wins 5 and loses 5" (01:35) | rule vs `−,−,+,−,+,+,−,−,+,−` → 5 correct | ✓ |
| IS/OOS random-walk collapse (02:25 vs §3) | text "Sharpe ≈1.3 → ≈0" vs code `+1.33 / −0.01` | ✓ consistent |
| "non-normality costs ~4 pp at N=100" (04:117) | `0.9421−0.8997=0.0424` | ✓ |
| Almgren–Chriss "quadratic ∝ (size/ADV)^{3/2}" (05:29) | **inconsistent** | ✗ see issue #3 |

---

## 4. Code stats

| File | Block | Runs | Seed | Output fence |
|---|---|---|---|---|
| index.md | hygiene engine (DSR + E[max] + crossings) | ✓ rc=0 | none (deterministic) | exact match |
| 01-from-zero-intuition.md | coin-search A + MC best-Sharpe B | ✓ rc=0 | 0, 1 | exact match |
| 02-why-backtests-lie.md | 72-strategy MA-crossover IS/OOS | ✓ rc=0 | 5 | exact match |
| 03-the-multiple-testing-problem.md | E[max] table + MC 20k + haircut + FWER/Bonferroni | ✓ rc=0 | 7 | exact match |
| 04-deflated-sharpe-ratio.md | DSR sweep + normal contrast + MinTRL | ✓ rc=0 | none (deterministic) | exact match |
| 05-failure-modes-and-practice.md | cost-drag DSR schedule | ✓ rc=0 | 21 | exact match |
| 06-advanced-extensions.md | CSCV PBO (noise vs skilled) | ✓ rc=0 | 11 | exact match |

**7/7 blocks run; 7/7 reproduce their documented stdout exactly.** All MC blocks are
seed-pinned, so they are deterministic cross-machine (no nondeterministic blocks).
Stdlib-only imports (`math`, `statistics`, `random`, `itertools`) — no dependency risk.

---

## 5. Links & coherence

- **Wikilinks in folder: 69 total** (index 14, 01 8, 02 12, 03 8, 04 8, 05 8, 06 11). **All 69 resolve** to an existing `content/` file or folder-hub.
- **Hub ↔ 01 prereq line consistent:** index:11 scopes the folder prerequisites to pages 02–06 and explicitly defers page 01 to its own smaller entry requirements; 01:11 says "none beyond high-school probability". No conflict.
- **Cross-folder bridges** to `foundations/probability-and-measure-theory`, `feature-engineering-and-labeling`, `07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr`, `signal-processing-and-kalman` all resolve.
- **Contradiction found:** gate `PBO ≤ 0.5` (05:38) vs 06:101 "PBO ≈ 0.5 condemns" — issue #5.
- **Jargon first-use:** DSR/PSR/MinTRL/FWER/PBO/CSCV/SPA/EVT/IS-OOS all defined at or before first use (FWER index:31; DSR index:35; PSR 04:18; PBO 06:22; CSCV 06:22). Clean.
- **Terminology consistency:** "look-ahead" hyphenated uniformly (4/4); "out-of-sample" uniform. No typos found in prose (spell-scan → only domain/British terms, all legitimate).

---

## 6. Notes / caveats

- Only the ESL claims are backed by a `corpus/verified/` file (`esl_ch6-10.md`); the DSR,
  Harvey–Liu, PBO (Bailey–Borwein–LdP–Zhu 2017), White RC, Hansen SPA and Bruss 1/e
  results are cited to primary literature not present in `corpus/verified/`. They were
  validated by independent re-derivation above, not by source text.
- The `python` blocks were run with `python3` from the repo root; each block is
  self-contained (no cross-block imports) and produced the exact fences shown.
