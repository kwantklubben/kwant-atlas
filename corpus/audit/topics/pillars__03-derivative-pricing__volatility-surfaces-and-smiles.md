# Audit — `content/pillars/03-derivative-pricing/volatility-surfaces-and-smiles/`

**Scope:** 7 files (index + 01–06). **Reviewer role:** sole adversarial reviewer.
**Method:** (1) every `python` block re-executed and diffed against its output fence; (2) every boxed/displayed formula re-derived AND cross-checked line-by-line against the verified corpus (`corpus/verified/gatheral_ch1-5.md`, `gatheral_ch6-10.md`, `bergomi_ch1-5.md`, `bergomi_ch6-10.md`); (3) spelling pass; (4) link-target + hub/child coherence pass.

**Bottom line:** the folder is mathematically sound — Dupire (strike + implied forms), SVI, the convex-order condition, the variance-swap smile integral, the SSR/LV forward-skew formulas, the Heston CF / ATM term structure / skew limits, and the Lewis Fourier pricer all match the corpus and/or re-derive correctly. No critical (wrong-result) math error. Nine minor issues, the only genuine *math* defect being one sign word in prose.

---

## 0. Code execution

All **7** python blocks run clean (stdlib only) and reproduce their output fences **exactly**:

| file | block | result vs fence |
|---|---|---|
| index.md | BSM→IV lookup | match |
| 01 | skew inversion + flat-vs-skew gap | match |
| 02 | Dupire two routes (0.042695 / 0.092003 / 0.009415; flat 0.04) | match |
| 03 | SVI slice, VS integral, BL density (min 0.017803) | match |
| 04 | LV SSR (→2.9684), Heston ATM term structure + skew limit (−0.1388 vs −0.1389) | match |
| 05 | butterfly/calendar detection, LV fwd-skew flattening (0.586×) | match |
| 06 | Heston CF, Lewis vs BS (diff ~1e-13), φ(0)=φ(−i)=1 | match |

Formula/constant spot-checks that PASS: Dupire implied-variance denominator `1 − (y/w)w_y + ¼(−¼ − 1/w + y²/w²)w_y² + ½w_yy` (identical to Gatheral 1.10; Bergomi 2.19 expands to it identically); SVI `w=a+b[ρ(k−m)+√((k−m)²+s²)]`, ATM skew `b(ρ − m/√(m²+s²))→bρ`, wings `b(1±ρ)`; VS integral + substitution `y=ln(K/F)/(σ√T) − σ√T/2` (Bergomi 4.21/5.17); γ-weighted implied variance with `e^{−rt}` (Bergomi 2.32); `S_T=(1/T)∫(t/T)α→α/2`, curvature `β/3` (Bergomi 2.48/2.50); `R_T=1+(1/T)∫S_t/S_T dt`, `R_∞=(2−γ)/(1−γ)` (Bergomi 2.64/2.82); forward skew 2.91/2.92; Heston 3.18/3.19, `ρη/2` short-dated; jump `∂v/∂k→ρb(σ)−2μ_J`; Lee `β*=2−4(√(x²+x)−x)`; Bergomi 7.13/7.40; Heston CF (2.11/2.12/2.14/2.15) and Lewis formula (validated numerically vs BS).

---

## 1. Findings (severity ordered)

### M1 — SIGN ERROR in prose (math), medium
**File:** `05-failure-modes-and-practice.md:45`
**Stated:** "For a *decreasing* skew term structure the bracket is negative, so `S_θ(τ) < S_{τ+θ}`."
**Correct:** the bracket is **positive**. The bracket defined one line above is `(1/θ)∫_τ^{τ+θ} S_t dt − S_{τ+θ}`; for a *decreasing* `S_t` the running average exceeds the endpoint, so the bracket is `> 0` (the numerical example confirms: 0.1283 − 0.1096 = +0.0187). The conclusion `S_θ(τ) < S_{τ+θ}` follows precisely *because* of the leading minus sign `− (τ/θ)(·)`. Fix: "the bracket is positive".
**Evidence:** `05:44` formula (Bergomi 2.91) + the file's own printed example `S_fwd(1.0,1.0) < S_term(1.0)`.

### M2 — Missing expectation in a stated constant (math/notation), minor
**File:** `03-surface-models.md:65`
**Stated:** `σ̂²_{VS,T} − σ̂_T² ≃ −⅓ λ J³`.
**Correct:** `≃ −⅓ λ ⟨J³⟩` (Berry–Esseen leading term of Bergomi 5.28/5.29, `λ⟨ln²(1+J)+2ln(1+J)−2J⟩`). The third *moment* is missing.
**Evidence:** `corpus/verified/bergomi_ch1-5.md:421,636`.

### M3 — Internal inconsistency in the Heston CF argument (math), minor
**File:** `06-advanced-extensions.md:39` vs `06-advanced-extensions.md:47`
**Stated (l.39):** the CF uses `x = ln(F_T/K)`. **Stated (l.47):** "`φ(−i)=E[e^{x}]=1` (the martingale condition `F_T=E[S_T]`)".
These cannot both hold: under `x=ln(F_T/K)` with deterministic `F_T`, `E[e^{x}] = F_T/K ≠ 1`; the identity `φ(−i)=1` (which the code verifies, line 116/117) holds only for the forward-relative `x = ln(S_T/F_T)`. The code implements the forward-relative convention. Fix: either redefine `x=ln(S_T/F_T)` at l.39, or restate the identity as `φ(−i)=F_T/K` at l.47.
**Evidence:** `06` code + fence `phi(0)=1.0000000000  phi(-i)=1.0000000000`; Gatheral 2.15 / corpus `gatheral_ch1-5.md:60`.

### R1 — Citation mix-up (reference), minor
**File:** `04-advanced-dynamics.md:66`
**Stated:** "The **natural interpolation** … is **Bergomi eq 7.11**, which Lewis's small-η expansion proves exact to O(η) (Gatheral §7.6, eq 7.11–7.12)."
**Correct:** eq (7.11)/(7.12) is **Gatheral's** (the same sentence cites "Gatheral §7.6, eq 7.11–7.12"). Should read "Gatheral eq 7.11".
**Evidence:** `corpus/verified/gatheral_ch6-10.md:311,346-351`.

### S1 — Spelling (typo)
**File:** `02-implied-vs-local-vol.md:125` — "a one-factor completeness is a **straightjacket**" → **straitjacket**.

### S2 — Proper-noun capitalization (typo)
**File:** `02-implied-vs-local-vol.md:24` — "**gyöngy**/averaging" → **Gyöngy** (the same name is capitalized as "Gyöngy" in `index.md:39`).

### C1 — Over-claim about a check (coherence), minor
**File:** `06-advanced-extensions.md:45`
**Stated:** the Heston two-probability form "…Both use the same φ and must agree — **the cross-check used below**."
The code in §3 below does **not** implement the two-probability form; it (i) validates the Lewis integrator against the BS closed form, (ii) checks `φ(0)=φ(−i)=1`, (iii) prints a Heston smile. Either add the two-probability cross-check or drop the phrase. (The `δ_j` in the written two-probability formula is also left undefined.)

### C2 — Self-referential wikilink (coherence)
**File:** `index.md:103` (also `01:118`, `02:142`)
The link `[[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]]`, presented as a "related flat note / sibling", resolves to **this folder's own `index.md`** (verified: target exists but is the hub itself). Harmless but self-referential — should point to a genuine net-new note or be removed.

### C3 — SVI arbitrage claim vs the folder's own counter-example (coherence), minor
**File:** `03-surface-models.md:22` (cf. `03:130`) claims SVI "is built to avoid butterfly/calendar arbitrage", yet `05-failure-modes-and-practice.md:69-77,96` exhibits a plain SVI slice with **butterfly arbitrage** (min density −6.92). Raw 5-parameter SVI is *not* automatically arbitrage-free; only SVI with the calendar/butterfly constraints (or SSVI) is. `05:136` itself says independently-fitted slices "will violate calendar no-arbitrage". Soften `03:22`.

---

## 2. Clean areas (explicitly checked, no defects)

- **Links:** all `[[…]]` targets in all 7 files resolve (0 broken).
- **Hub ↔ children:** prereq chain 01→02→03→04→05→06 consistent; index §2 lookup-table numbers all reproduce the code fences; §4 failure-mode signposts agree with 05.
- **Terminology/jargon:** sticky-strike (idx 1 / δσ/δS=0) vs sticky-delta (0) consistent across 02/03/04; `SVI`, `SSR`, `RV`/`LV`, `BL density`, `convex order` used consistently.
- **No contradictions** found between the hub and 01 (the "01 states its own smaller prereqs" caveat in `index:11` is satisfied by `01:11`).

---

## 3. Recommended fixes (priority)

1. `05:45` — "negative" → "positive" (**only real math correction**).
2. `02:125` straitjacket; `02:24` Gyöngy (spelling).
3. `04:66` "Bergomi eq 7.11" → "Gatheral eq 7.11".
4. `06:39`/`06:47` reconcile the `x` definition with `φ(−i)=1`.
5. `03:65` `−⅓λJ³` → `−⅓λ⟨J³⟩`.
6. `06:45` drop/repair "the cross-check used below"; define `δ_j`.
7. `index:103`/`01:118`/`02:142` de-self-reference the index link; `03:22` soften the SVI-arbitrage claim.

**Verdict: PASS WITH MINOR ISSUES** — content is technically correct and code-verified; 1 prose sign error + 2 typos + 1 citation slip + 5 minor consistency/coherence nits.
