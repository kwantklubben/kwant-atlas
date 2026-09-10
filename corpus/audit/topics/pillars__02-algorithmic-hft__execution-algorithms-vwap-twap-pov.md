# Audit — `content/pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/`

**Reviewer:** sole, adversarial · **Date:** 2026-09-10
**Files:** 7 (index + 01…06) · **Code blocks:** 7/7 extracted and executed · **Verdict:** PASS WITH FIXES

---

## 1. Verdict

The folder is **structurally sound**: the hub is a real hub (comparison table + core benchmark
formulas + six routed sub-pages), the IS boxed formula is correct and its Perold/Foucault example
(`$24,000` = 2.4% of paper) reproduces exactly, and **all seven `python` blocks run to completion on
Python 3.14 and reproduce their documented output fences byte-for-byte** (all are seed-pinned:
`Random(7/11/21/33)`, so deterministic cross-machine).

But "reproduces its fence" is **not** the same as "correct" here: two blocks reproduce an
*internally buggy* computation, and three others report costs under a wrong unit label. Net
defects are the **bps units (`×100` used where bps need `×1e4`, and a missing `/VWAP` divisor),
a variable-shadowing bug in the 06 volume-spike block, one covariance-identity sign flip, two
malformed/typo'd formulas, and two prose spelling/grammar slips.** No broken wikilink.
Counted errors: **10**.

---

## 2. Issues

| # | file:line | Problem | Fix |
|---|---|---|---|
| 1 | `01-from-zero-intuition.md:56` (code), `:63` (fence), `:66` (prose) | **bps mis-unit by ×100.** Per-share cost in bps = `1e4·cost/notional`, but the code computes `100*sweep/(X*S0)`. Sweep cost `$25,020,000` on `$100,000,000` notional is **2502 bps (25.02%)**, not "25.02 bps"; TWAP is **52 bps**, not "0.52 bps". Prose `:66` ("~\$25\$ bps… under \$1\$ bps") inherits the ×100 error. `05` uses `1e4·cost/(X·S0)` for the same class of number — so the folder is internally inconsistent. | Change `100*` → `1e4*` in the f-string; fix the fence (`2502`/`52`) and the prose ("~2500 bps… ~50 bps"). |
| 2 | `02-twap-vwap-pov.md:76–77` (code), `:85` (fence), `:92` (prose) | **"vs VWAP" bps missing the ÷benchmark.** Line 76/77 print `1e4*(ev-vwap_bench)` (raw dollar diff ×1e4) while the *same line* prints "vs arrival" as `1e4*(ev-S0)/S0` (correctly normalized). Result: fence shows `TWAP … vs VWAP -603.94 bps` where the true value is `1e4·(100.7436-100.8039)/100.8039 = -5.98 bps`. The prose `:92` says "$\approx6$ bps" — **the fence and the prose contradict each other.** | Divide by `vwap_bench`: `1e4*(et-vwap_bench)/vwap_bench`; fence becomes `-5.98 bps`. |
| 3 | `06-advanced-extensions.md:72` (code), `:88` (fence), `:95` (prose) | **Variable-shadowing bug → wrong share.** `vol_spike=[v*(3.0 if k==k_spike else 1.0) for k in range(B)]` — `v` is **not** the comprehension's value; it leaks from the earlier loop `for k,v in enumerate(vol)` (line 56) and is pinned to `vol[12]=0.11579`. So `vol_spike` is 3× a *constant* bucket, not 3× bucket 10. Printed "**20.0%** of realized day volume"; the correct 3×-bucket-10 share is **22.77%**. Bug propagates to the prose `:95` ("realizes 20.0% of the day"). | `vol_spike=[vol[k]*(3.0 if k==k_spike else 1.0) for k in range(B)]`; fence/prose become `22.8%`. |
| 4 | `06-advanced-extensions.md:76` (code), `:95` (prose) | **Double normalization.** `100*X*vol[k_spike]/Z/X` divides by `Z` again, but `vol` is already normalized (`vol=[b/Z for b in base]`). "FIXED VWAP ships **9.4%** of parent" should be the forecast weight itself, `100*vol[k_spike] = **8.95%**`. | Drop the `/Z`: `100*vol[k_spike]`; prose → "8.9%". |
| 5 | `02-twap-vwap-pov.md:39` | **Sign flip in the TWAP−VWAP identity.** Text: `\bar p_TWAP − VWAP = Cov_φ(p,φ)` "where the day's volume sits". In the page's own worked example `\bar p_TWAP=100.7436 < VWAP=100.8039`, so LHS `= −0.0604`, while the price–volume covariance is **positive** (rising tape, volume concentration to the heavy close): `Σ(φ−1/B)(p−p̄)=+0.0604`. The standard relation is `VWAP − \bar p_TWAP = Cov(p,φ)`. | Write `\bar p_TWAP − VWAP = −\,Cov_φ(p,φ)` (or move the covariance to the other side). |
| 6 | `03-implementation-shortfall.md:86` | **Prose mislabels the \$20,000 case.** "…filling everything at the decision price gives \$20,000." Filling at the *decision* price (`\bar p=m_0=50`) gives **IS = 0**; the `$20,000` is the `κ=1` full-fill value at `\bar p=50.40` (execution cost only) — exactly what the §3 code prints (`If kappa=1 … = 20,000`). | Rewrite: "…while a full fill at the realized price `\bar p=50.40` gives \$20,000." |
| 7 | `index.md:43` | **Wrong subscript in the boxed VWAP formula.** `\text{VWAP}=\sum_{k=1}^K w_t\,p_k` uses `w_t` (a bucket index `t` that the sum does not bind) instead of the defined `w_k = v_k/\sum v_k`. The sibling page `02:33` writes it correctly. | `\sum_{k=1}^K w_k\,p_k`. |
| 8 | `01-from-zero-intuition.md:32` | **Malformed LaTeX in the impact formula.** `h(v) = \varepsilon + \frac{\eta}{\tau}\,n,_\text{ per share,}` — stray commas + text inside math mode (`,_\text{ per share,}`) render as garbage, and the symbol should be the rate `v`, not `n`. | `$$h(v) = \varepsilon + \frac{\eta}{\tau}\,v \quad\text{per share,}$$` (then `n\cdot h(n/\tau)` is consistent). |
| 9 | `05-failure-modes-and-practice.md:34` | **Spelling.** "…so the schedule is *not* a **reproduceable** linear prediction." | `reproducible`. |
| 10 | `02-twap-vwap-pov.md:99` | **Grammar (article).** "…bad on any day with **an U-shaped** profile…". "U" is pronounced /juː/ → "a". | `a U-shaped`. |

**Nitpicks (not counted):**

- `index.md:47` and `02-twap-vwap-pov.md:44` call `\text{TE}=\sqrt{\sum_t(w_t^{\text{exec}}-\phi_t)^2}` the "**RMS** deviation". It is an unnormalized L2 norm, not RMS (RMS would divide by `\sqrt B` or take `\sqrt{\text{mean}}`). Either say "L2 deviation" or add the `1/B`.
- `01-from-zero-intuition.md:66` "The **unbonded** `\varepsilon X` fixed cost" — "unbonded" appears to be a typo (likely "unbundled" or "un-sliced"); as written it is not a word in this context.
- `02-twap-vwap-pov.md:89–90` — a stray blank line sits between the last output line and the closing ``` fence.
- Hub prereq wording (`index.md:13`) scopes folder prerequisites to pages 02–06 and defers 01 to its own smaller entry set; `01:11` states only the microstructure base. **Consistent** — no issue, noted for completeness.

---

## 3. Math verified (re-derived / re-executed independently)

| Formula / example (location) | Check | Result |
|---|---|---|
| IS boxed eq (index:51, 03:34) | `κq(\bar p−m_0)+(1−κ)q(m_t−m_0)` algebra; matches Hasbrouck 14.1 structure | ✓ |
| Perold/Foucault example `$24,000` (03:56–58) | `3000·1 + 7000·3 = 3000+21000`; `/1e6 = 2.4%` of paper | ✓ 24,000 / 2.4% |
| Fresh IS decomposition (03:61–70) | `0.8·50000·0.40=16,000`; `0.2·50000·1.20=12,000`; total `28,000`; `1e4·28000/(50000·50)=112 bps` | ✓ all |
| AC temporary-impact split (01:33) | `Σ n_t²` with `N` equal slices → `X²/N`; sweep/TWAP ratio `50` | ✓ |
| Sweep vs slice `$25,020,000 / $520,000` (index:59, 01:46) | `1e6·(0.02+2.5e-5·1e6)=25.02e6`; `50·(20000·(0.02+2.5e-5·20000))=520,000` | ✓ |
| 02 VWAP-engine exactness (02:83–87) | VWAP engine avg `= day VWAP = 100.8039`; TE `0.0000` by construction; TWAP TE `0.0607` | ✓ |
| VWAP−TWAP gap (02:85 vs 92) | true `1e4·Δ/VWAP = 5.98 bps`, prose "≈6 bps" ✓ — but the fence's `-603.94 bps` ✗ (issue #2) | ✗ fence |
| 04 profile estimation / renormalization (04:81–88) | children sum to exactly `100,000`; `TE_clean=0.0080`, `TE_news=0.0741` (=9.26× clean, "nine times" ✓), `TE_TWAP=0.1238` | ✓ |
| 05 gaming concession (05:82) | `Σ (X/B)·0.02 = X·0.02 = $2,000`; `1e4·2000/(1e5·100)=2.00 bps` | ✓ |
| 05 misestimation (05:85–86) | `φ_0=5.26%`, realized `12.57%`, TE `0.0762` | ✓ |
| 05 adverse selection (05:92) | `60000·(104.0−100.3)=148,000`; `148000/4e6·1e4=370 bps` | ✓ |
| 06 benchmark-aware bps (06:83–85) | `bps=1e4(p−S0)/S0`; `+84.10`, `+65.67`, diff `+18.43` | ✓ |
| 06 spike bucket share (06:88) | correct value `22.77%`, printed `20.0%` | ✗ issue #3 |
| 06 "ships 9.4% of parent" (06:76) | correct `8.95%` | ✗ issue #4 |
| 01 per-share bps (01:63) | correct `2502 / 52 bps`, printed `25.02 / 0.52 "bps"` | ✗ issue #1 |
| TWAP−VWAP = Cov (02:39) | worked example sign contradicts | ✗ issue #5 |

---

## 4. Code stats

| File | Block | Runs | Seed | Output fence |
|---|---|---|---|---|
| index.md | sweep-vs-TWAP temporary impact | ✓ rc=0 | none (deterministic) | exact match |
| 01-from-zero-intuition.md | sweep vs 50-slice TWAP + bps | ✓ rc=0 | none | exact match (values carry ×100 bug) |
| 02-twap-vwap-pov.md | build+simulate TWAP/VWAP, tracking error | ✓ rc=0 | 7 | exact match (fence carries the ÷-bug) |
| 03-implementation-shortfall.md | Perold/Foucault IS + fresh decomposition | ✓ rc=0 | none | exact match |
| 04-scheduling-and-volume-profiles.md | profile estimation, randomized exact schedule | ✓ rc=0 | 11 | exact match |
| 05-failure-modes-and-practice.md | gaming / misestimation / adverse selection | ✓ rc=0 | 21 | exact match |
| 06-advanced-extensions.md | benchmark-aware vs POV | ✓ rc=0 | 33 | exact match (two logic bugs reproduce) |

**7/7 blocks run; 7/7 reproduce their documented stdout exactly.** Stdlib-only (`random`, `math`) —
no dependency risk. All stochastic blocks are seed-pinned → deterministic cross-machine.

---

## 5. Links & coherence

- **Wikilinks in folder:** all resolve against `content/` — verified present:
  `market-microstructure-and-order-types/index`, `foundations/calculus-and-optimization/index`,
  `optimal-execution-and-almgren-chriss/{index,02-the-execution-problem,03-the-almgren-chriss-model,06-advanced-extensions}`,
  `queue-position-and-fill-probability/index`, `pillars/06-market-making/{market-impact-and-depth,adverse-selection-and-glosten-milgrom}/index`,
  `pillars/05-portfolio-optimization/constraints-and-transaction-costs/index`. **No broken links.**
- **Hub ↔ 01 prereq consistent:** `index:13` scopes folder prereqs to pages 02–06 and explicitly
  defers page 01; `01:11` states only the microstructure base. No conflict.
- **Jargon first-use:** parent order (01), VWAP/TWAP/POV (02), IS/arrival price (03), U-shaped
  profile (04), zero-sum/TE (05), AC frontier (06) — all defined at or before first substantive use.
  Clean.
- **Hub vs sub-page contradiction:** hub says `01` needs only microstructure; consistent.
  The one real hub↔page numeric contradiction is the `02` fence-vs-prose bps mismatch (issue #2).
- **Terminology:** "implementation shortfall"/"IS", "arrival price", "tracking error" used uniformly.
  Only spelling/grammar slips are #9 and #10.

---

## 6. Notes / caveats

- Blocks were run from `/tmp` with `python3 3.14.7`; each is self-contained (no cross-block imports)
  and produced the exact fences shown, including the fences that encode issues #1–#4.
- The IS/Perold and Foucault `eq 2.29` claims are cited to `corpus/verified/foucault_ch1-3.md` and
  `hasbrouck_ch11-15.md`; the boxed formula and the `$24,000` example were independently re-derived
  above and are correct. The AC / Bertsimas–Lo / Cartea et al. citations are not in `corpus/verified/`;
  the AC child-trajectory formula (`x_t=X\sinh(κ(T−t))/\sinh(κT)`, `κ=√(λσ²/η)`) at `06:36` is the
  standard form and checks out by inspection.
