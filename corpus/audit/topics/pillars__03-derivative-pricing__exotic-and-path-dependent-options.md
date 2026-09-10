# Audit — `content/pillars/03-derivative-pricing/exotic-and-path-dependent-options/`

**Reviewer:** sole adversarial reviewer · **Date:** 2026-09-10
**Files checked:** 7 (index + 01–06) · **Python blocks run:** 9 (all executed, stdlib-only)
**Verified sources cross-referenced:** `corpus/verified/haug_lookup-1.md`, `corpus/verified/haug_lookup-2.md`

## Verdict

**PASS WITH FIXES.** All six mathematical families are structurally correct, every boxed
formula matches the Haug transcription, and **all 9 code blocks execute and reproduce their
output fences**. No wrong formula, wrong sign, or wrong constant was found in any closed
form. Three genuine content defects remain (one internal contradiction, one transcription
digit, one prose-vs-output contradiction) plus three minor defects.

---

## 1. CODE — every block executed, diffed vs output fence

| File | Block (line) | Result |
|---|---|---|
| index.md | 57 | ✅ exact match (`4.6922`) |
| 01-from-zero-intuition.md | 53 | ⚠️ values correct; **fence line order ≠ print order** (see E4) |
| 02-barriers-and-digitals.md | 68 | ✅ exact match (6 values) |
| 03-lookbacks-and-asians.md | 54 | ✅ exact match (5 values) |
| 04-compound-chooser-quanto-exchange.md | 72 | ✅ exact match (6 values) |
| 05-failure-modes-and-practice.md | 46 | ✅ exact match (6 lines) |
| 05-failure-modes-and-practice.md | 99 | ✅ exact match (3 lines) |
| 06-advanced-extensions.md | 40 | ✅ exact match (5 lines) |
| 06-advanced-extensions.md | 87 | ✅ exact match (`6.1339`) |

Independently reproduced outside the corpus code as a cross-check: in–out parity digits
`c_di=3.3368`, `c_do=4.5126`; lookback sign-flip value `21.3531`; European put `5.5735`;
CRR American put `6.0896` (n=1000) / `6.0902` (n=5000). All match the prose.

## 2. MATH — boxed formulas & worked examples

Verified against Haug (via `haug_lookup-2.md`) and by re-execution:

- **Reiner–Rubinstein `A…F`** (02 §2.1): μ, λ, x₁,x₂,y₁,y₂,z and all six blocks match Haug
  4.51–4.52 exactly; the call combination table matches Table 4-13 for all four rows. ✅
- **In–out parity** `c_di+c_do=c_vanilla` (K=0) ✅; rebate caveat stated correctly.
- **Digitals** (cash d₂ / asset d₁ forms) ✅; both anchors reproduce (2.6710, 20.2069).
- **Floating lookback 4.39** ✅ (25.3534 vs book 25.3533); sign-flip → 21.353 → matches the
  stated "flip → 21.35" caveat.
- **Geometric Asian 4.91** (σ_A=σ/√3, b_A=½(b−σ²/6)) ✅ (4.6922).
- **Turnbull–Wakeman** moment formulas `b̄=ln M₁/T`, `σ̄²=ln M₂/T−2b̄` ✅ — confirmed verbatim
  against `haug_lookup-2.md:382`.
- **Compound put-on-call 4.29** ✅ (21.1964, I=538.3165 — both match book).
- **Chooser 4.26** ✅ (6.1071 via the decomposition; page correctly flags the ambiguous literal
  transcription — consistent with `haug_lookup-2.md:32–34`).
- **Complex chooser 4.27** — value ✅ (6.0507 ≈ book 6.0508, disclosed); **critical I wrong** (E2).
- **Margrabe 5.7** ✅ (1.5260), **Kirk 5.17** ✅ (2.1670), **quanto 5.39** ✅ (5.3280),
  **foreign-equity 5.35** ✅ (8.3056).
- **BGK** `H_D=H e^{±βσ√Δt}`, β=ζ(1/2)/√(2π)=0.5826 ✅; sign convention (+ above/− below) and
  code usage match.
- **LR/score delta** (05 §2): score `Z/(S₀σ√T)`, `E[Δ_LR]=Ke^{−rT}φ(d₂)/(S₀σ√T)` ✅ — derivable
  and reproduced numerically (0.027359 vs 0.027338).

## 3. ERRORS

**E1 (content contradiction) — `01-from-zero-intuition.md:96`**
Stated: *"a barrier checked daily is **cheaper** than one checked continuously."*
This directly contradicts `02-barriers-and-digitals.md:125` (*"a continuously-monitored
down-and-out is cheaper than a discretely-monitored one"*) and `05-failure-modes-and-practice.md:20`
(*"the discrete price is systematically **above** the continuous one for knock-outs"*).
Correct: for a **knock-out**, discrete monitoring is *more* expensive (the grid misses
touches → higher survival value); the daily/cheaper claim holds only for a **knock-in**.
The unqualified sentence is wrong in the knock-out framing that 01 itself uses (its §2 table
example is a down-and-out call). Fix: qualify per knock-in/knock-out, or align with 02/05.

**E2 (transcription error) — `index.md:43` and `04-compound-chooser-quanto-exchange.md:155`**
Stated: complex-chooser critical `I = 51.1156`.
Verified source (`corpus/verified/haug_lookup-2.md:46,583`): `I = 51.1158`. Digit transposition.
Fix: change both occurrences to **51.1158**. (`04:24` and `index:43` also print the value as
`6.0507`; the book/verified value is `6.0508` — disclosed as "book 6.0508" in the hub but not
in `04:24`, which states 6.0507 bare.)

**E3 (prose contradicts own output) — `06-advanced-extensions.md:123`**
Stated: *"LSM sits within its own seed-to-seed noise (~±0.03 for N=40000) of the binomial value,
**consistently from below** as expected of a suboptimal stopping rule."*
The block prints **LSM = 6.1339**; the page's own binomial benchmark is **6.0902**, so the gap is
**+0.0437** — larger than the stated ±0.03 **and on the wrong side**. `6.1339 > 6.0902`
contradicts the low-bias claim the same sentence asserts (the page's own §4.3 notes in-sample
overfit *inflates* the estimate). Fix: correct the sentence — the printed run is *above* the
binomial value (in-sample foresight bias), not "from below".

**E4 (output-fence order) — `01-from-zero-intuition.md:83–87`**
The fence lists `vanilla → closed-form → lookback`, but the program prints
`vanilla → lookback → closed-form`. Values are right; a copy-paste reorder. Fix: reorder the
fence to match print order.

**E5 (dangling reference) — `index.md:33`**
Barrier row cites *"combination table §5.1"*. No §5.1 exists in this folder or the hub; the
combination table is `02-barriers-and-digitals.md` §2.1. Fix: point to `02 … §2.1`.

**E6 (numeric inconsistency) — `06-advanced-extensions.md:21` vs `:81`**
§1 prose: *"verified 8400× below"*; the block output: *"variance reduction = 8415x"*. Reconcile
to 8415× (or state "~8400×").

## 4. COHERENCE / MINOR OBSERVATIONS (not counted)

- **`06:83`** — "collapses the arithmetic-Asian MC standard error from 0.012 to 0.0001 — a
  **four-orders-of-magnitude variance reduction**". SE drop is ×~92 (two orders); the *variance*
  ratio is 8415 ≈ 10^3.9. Mixing SE and variance in one clause. Wording only; displayed `0.0001`
  is a rounding of ≈0.000131, so the printed `8415x` is self-consistent.
- **`03:118`** — "The lookback MC **matches** the reflection-principle closed form" while the
  printed MC is 25.1114 vs closed 25.3534 (~1.0% gap). The gap is the discrete-monitoring bias of
  the 200-step MC (correctly sign-directed, since discrete min ≥ true min), not drift — but
  "matches" overstates it. Suggest "approaches … (residual gap = discrete monitoring)".
- **`index.md:29`** — notation block defines `$K$ rebate/digital payout` while `X` is strike; the
  hub data rows also use `K` as the digital payout `10`/`1`. Consistent, but `K` is overloaded
  (rebate vs digital payout) within one page — consider a note.
- **Spelling/typos:** none. A dictionary pass over the prose (excluding code) returned only
  math/code tokens and hyphenated technical terms; `Haugh–Kogan` (`06:32`) is the correct
  author name, not a typo.
- **Wikilinks:** all 15 distinct wikilink targets resolve to existing files/folders. ✅
- **Prereq scope:** hub line 11 correctly scopes pages 02–06 and notes page 01 states its own
  smaller entry requirement; 01:11, 02:11, 03:11, 04:13, 05:12, 06:12 chain correctly. ✅
- **Cross-number consistency:** hub §2 check-column digits all agree with the sub-page code
  outputs and with `corpus/verified/haug_*` (barrier 6.7924/8.4482, asymmetry, digests 2.6710/
  20.2069, lookback 25.3534, Asian 4.6922, compound 21.1964/538.3165, chooser 6.1071, Margrabe
  1.5260, quanto 5.3280, foreign-equity 8.3056, Kirk 2.1670, BGK 94.027→5.9831). ✅

## Summary

| Severity | Count | IDs |
|---|---|---|
| Content error (formula/sign/constant/prose) | 3 | E1, E2, E3 |
| Defect (fence/reference/inconsistency) | 3 | E4, E5, E6 |
| Observation (not counted) | 4 | §4 |

No incorrect closed-form formula, sign, or constant was found. The three content errors are one
contradiction (01 vs 02/05), one digit (I=51.1156→51.1158), and one prose/output contradiction
(LSM "from below").
