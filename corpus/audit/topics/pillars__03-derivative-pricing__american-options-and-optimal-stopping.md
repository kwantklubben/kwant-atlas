# Audit: pillars/03-derivative-pricing/american-options-and-optimal-stopping

**Reviewer:** sole adversarial reviewer · **Date:** 2026-09-10
**Files checked:** 7 (index + 01–06) · **Code blocks run:** 7 (all stdlib, exit 0)
**Scope:** spelling, math, code, coherence. `content/_legacy/` ignored.

---

## Verdict: 2 math errors, 1 output-fence cosmetic, 2 minor text nits

---

## 1. CODE AUDIT — all 7 blocks run, 6 exact matches, 1 cosmetic fence diff

Every ` ```python ` block extracted, run with the repo's stdlib-only style, and diffed
against its output fence (trailing whitespace normalized).

| File:block | Run | Diff vs fence |
|---|---|---|
| index:0 | exit 0 | **MATCH** |
| 01:0 | exit 0 | **MATCH** |
| 02:0 | exit 0 | **COSMETIC DIFF** (below) |
| 03:0 | exit 0 | **MATCH** |
| 04:0 | exit 0 | **MATCH** |
| 05:0 | exit 0 | **MATCH** |
| 06:0 | exit 0 | **MATCH** |

### Error E3 (cosmetic) — `02-optimal-stopping-theory.md:105` (output fence)
The code emits two leading spaces on **every** level line (`print(f"  level {j}: …")`),
but the fence's first line drops them:
```
expected:  level 0: [(4.0, 1.36)]
actual :    level 0: [(4.0, 1.36)]     # leading 2 spaces missing in fence
```
Numeric output is otherwise identical. Fix: add the two spaces before `level 0` in the fence.

---

## 2. MATH AUDIT — every boxed formula and worked example checked

### Verified correct (computed independently)
- **Perpetual put, no div** (index:39–40, 03:36–43): `L* = γK/(1+γ) = 2rK/(2r+σ²)`.
  K=100,r=10%,σ=25% → γ=3.2, L*=76.1905, V(90)=13.9719, v′(L*)=−1 (smooth pasting). All reproduce exactly.
- **Perpetual put with cost-of-carry b** (index:41, 03:45–50): Haug Table 3-3 value 20.7939 reproduced.
- **BAW call** (index:43, 03:52–59): 1.8769 vs Haug 1.8771; 15.5684 vs 15.5689. Code matches fence.
- **BS-1993 call** (index:44, 03:61–69): 5.2704 (Haug 5.2704); European 5.0975. Exact.
- **Early-exercise premium** (index:46, 01:82–91): 4.6921−4.4496=0.2425. Reproduced.
- **LCP residual `min(V−payoff, Lv)=0`** (04:56, 04:100–121): verified at exercise side (Lv=+10=rK) and continuation side (Lv=0). Correct.
- **Free-boundary / smooth pasting maximisation** (04:89–92): argmax over L = 76.1900 vs closed form 76.1905 ✓.
- **Long-dated CRR → perpetual limit** (04:94–98): T=5→13.4540, T=20→13.9438 vs perpetual 13.9719. Monotone ✓.
- **BAW error vs CRR** (05:83–86): +0.45% @T=0.5 → +1.96% @T=3. Fence & prose ("+2%") consistent.
- **Bermudan vs continuous** (05:88–94): 12/yr 6.0423 (91% of premium), 4/yr 5.9560 (74%), 1/yr = 5.5719 = European. Premium recovery percentages verified: 0.4704/0.5178=90.8%, 0.3841/0.5178=74.2%. Prose ✓.
- **LSM + duality bracket** (06:158–167): interval [6.0461, 6.6440] contains true 6.0902. Reproduced exactly; `contains: True`.
- **Duality boxed identity** (06:52): `V0 = inf_M E[max_k(h_k−M_k)]`, M0=0 — standard Rogers / Haugh–Kogan form. Correct.

### Error E1 (math) — `01-from-zero-intuition.md:45` (Shreve Ex 5.1 worked example)
**Stated:** "The freedom to stop at t=1 raised the value from **1** — the European root
value is what the same recursion gives without the max. The overhang **1.36−1.0** is the
early-exercise premium."
**Correct:** The same recursion *without* the max (pure discounted-expected-payoff
rollback) gives European root value = **0.96**, not 1.0. Terminal payoffs 0,1,4 under
p̃=q̃=½ give E = 0.25·0 + 0.5·1 + 0.25·4 = 1.5; × 1/(1.25)² = **0.96**.
So the premium is **1.36 − 0.96 = 0.40**, not 0.36.
(Re-derived three ways: discounted terminal expectation, no-max rollback = 0.96, and
American−European = 1.36−0.96 = 0.40.) The "1" is the intrinsic value K−S0=1 at the root,
which is *not* the European value. Fix the sentence and the two numerals.

### Error E2 (math / internal inconsistency) — `04-free-boundary-and-complementarity.md:60`
**Stated:** the complementarity system is `V ≥ g,  Lv ≤ 0,  (V−g)·(Lv) = 0`.
**Problem:** `Lv` is defined at 04:46 as the **negative** of the BSM operator,
`Lv := rV − rSV_S − ½σ²S²V_SS`, and 04:48–50 establish **Lv ≥ 0** (equals `rK` in the
exercise region). §2.3 then states `Lv ≤ 0` for the same symbol, a sign flip.
**Correct:** with the negative-operator convention used by the boxed `min(V−intrinsic, Lv)=0`
formula and by the verified code (Lv=+10=rK in the exercise region), the complementarity
system must read **`Lv ≥ 0`**. As written, §2.3's `Lv ≤ 0` contradicts §2.2 and the boxed
formula it claims to be equivalent to. Fix the inequality sign to `≥`.

---

## 3. COHERENCE AUDIT

- **Hub vs 01 prerequisite:** consistent — hub (index:11) states 01 has its own smaller entry requirements; 01 declares stochastic calculus only. Pages 02–06 prerequisite chain is internally consistent.
- **Cross-folder links:** all 25 unique wikilinks across the 7 files resolve to existing `.md` files (checked against `content/`). No broken links. References to numerical-methods, BSM, no-arbitrage, foundations, exotic/volatility folders all valid.
- **Failure-mode numbers carry over correctly** between hub (index:110–111) and 05 (T=3 → +2%; Bermudan 4×/yr → ≈0.13). Verified against code.
- **No sign-flip in prose vs code:** 04's sign caveat (04:128) correctly warns readers — but §2.3's own `Lv ≤ 0` (E2) is the very slip it warns about.
- **No jargon misuse detected** across pages; notation (`γ`, `L*`, `b`, `q`, `N(·)`) is consistent with the hub's definition (index:35).

### Minor text nits (no factual impact)
- **N1** — `02-optimal-stopping-theory.md:130`: "Els 8.5.28–30" should read "**Eqs.** 8.5.28–30" (typo).
- **N2** — `05-failure-modes-and-practice.md:38`: "their error is **`O(·)` small**" — dangling `O(·)` placeholder, likely a missed `<something>` token; should name the small parameter (e.g. `O(T)` for short maturity).

---

## Summary of required fixes
| ID | File:line | Severity | Fix |
|---|---|---|---|
| E1 | 01:45 | **Math** | European root value = 0.96, premium = 0.40 (not 1.0 / 0.36) |
| E2 | 04:60 | **Math** | Change `Lv ≤ 0` to `Lv ≥ 0` in the complementarity system |
| E3 | 02:105 | Cosmetic | Add 2 leading spaces before `level 0` in the output fence |
| N1 | 02:130 | Nit | "Els" → "Eqs." |
| N2 | 05:38 | Nit | Complete the `O(·)` placeholder |
