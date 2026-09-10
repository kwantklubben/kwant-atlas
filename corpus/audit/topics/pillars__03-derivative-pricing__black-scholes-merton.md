# Audit — `pillars/03-derivative-pricing/black-scholes-merton/`

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages). BSM PDE, risk-neutral pricing, Greeks, hedging, implied vol.
**Corpus cross-check:** `corpus/verified/haug_lookup-1.md`, `haug_lookup-2.md` (Haug §1/§2 verified numerics), Shreve/Björk/Hull citations in text.
**Method:** (1) spelling/typo scan; (2) every boxed formula & worked example re-derived; (3) every ```python block executed and diffed against its output fence; (4) hub↔sub-page coherence, link resolution.

---

## VERDICT: **FAIL** — 2 errors found (1 high-severity code bug, 1 minor math sub-claim)

---

## Summary of findings

| # | Severity | File | Type | Issue |
|---|----------|------|------|-------|
| 1 | **HIGH** | `06-advanced-extensions.md` | CODE (logic) | Merton jump-diffusion MC has a broken Poisson sampler; the "jump" result is not a jump-diffusion price. |
| 2 | **MINOR** | `04-greeks-and-hedging.md` | MATH (sub-claim) | Rho caveat's "agrees with compact form when b=r" is false. |

All **8 boxed formulas, all worked examples in the hub/03/04 lookup tables, and 8 of 9 code blocks** verified correct. 8 of 9 blocks' output fences match actual execution exactly (the 9th — the Merton MC — *matches its fence* because the fence was generated from the buggy code; the *code itself* is wrong).

---

## FINDING 1 — HIGH · Merton jump-diffusion MC is broken (`06-advanced-extensions.md`)

**File/line:** `06-advanced-extensions.md:101-103` (code), `:118` (output fence), `:120` (narrative).

**Problem:** The Poisson jump counter never fires. In block B the sampler is:

```python
L = math.exp(-lam*T); p = 1.0; nJ = 0; u = random.random()   # sample Poisson
while u > p:
    nJ += 1; p *= lam*T/nJ
```

`p` starts at `1.0` and `u = random.random()` is in `[0,1)`, so the loop condition `u > p` (i.e. `u > 1.0`) is **never true**. `nJ` stays `0` on every path, so `J = 0` always and **no jumps are ever simulated**. The code silently degenerates to a *constant-vol lognormal* with the jump-adjusted drift `r − λκ`.

**Consequence:** The printed `Merton jump-diffusion MC (lam=2) = 26.0969` is NOT a Merton jump-diffusion price. It is the price of a one-factor lognormal with drift inflated by the `−λκ` compensator (with `κ = e^{-0.10+0.5·0.01}−1 = −0.09063`, the drift term becomes `r − ½σ² − λκ = 0.05 − 0.02 + 0.1813 = 0.2113`, i.e. a 21% annual drift instead of 5%). The measured `E[ST]` under the broken code was **126.06** vs the correct martingale value **105.13 = 100·e^{0.05·1}** — confirming the drift overstatement.

**Correct value:** The exact Poisson-mixture-of-lognormals price (sum over n of Poisson weights × lognormal call, recomputed from first principles) is **13.3506**; a corrected MC with a working sampler (Knuth Poisson: increment `k` while `exp(−λT)` falls, i.e. `while p > L: k+=1; p*=random()`) gives **13.34** at 500k paths. So the correct Merton price is ~**13.3**, only modestly above pure BSM `10.4506` — **not** 26.10.

**Narrative error:** The text at `:120` concludes "The two-factor jump model prices dramatically higher — constant-vol BSM cannot represent the tail risk." With `λ=2, μJ=−0.10, σJ=0.10` (small negative jumps), the true premium over BSM is ~28%, not "dramatically higher" (~150%). The entire experiment as written demonstrates nothing about jumps.

**Fix:** correct the Poisson sampler (e.g. Knuth's algorithm) and re-run; recompute the stated value (~13.3) and soften the conclusion accordingly.

---

## FINDING 2 — MINOR · Rho caveat's "agrees when b=r" is false (`04-greeks-and-hedging.md`)

**File/line:** `04-greeks-and-hedging.md:44-46`.

**Problem:** The (otherwise excellent and correct) caveat states the full generalized rho

> ρ_call = −T·S·e^{(b−r)T}N(d1) + T·X·e^{−rT}N(d2) … *which agrees with the compact form when b=r but differs otherwise.*

This is **incorrect at b=r**. Substituting `b=r` into the stated generalized formula gives

ρ_call(b=r) = −T·S·N(d1) + T·X·e^{−rT}N(d2),

which is **not** equal to the compact form `T·X·e^{−rT}N(d2)` (they differ by the term `−T·S·N(d1)`).

**Numeric confirmation** (standard BSM, S=100, X=100, T=1, r=0.05, σ=0.20): compact form `T X e^{-rT}N(d2)` = **53.23**; the caveat's own formula evaluated at b=r = **−10.45**. They do not agree.

**Root cause of the confusion:** the *true* standard-BSM rho (`b=r`, where `r` enters `d1,d2`) *is* the compact form `T X e^{-rT}N(d2)` — the `n(d1)`/`n(d2)` terms cancel via `S·n(d1)=X·e^{-rT}·n(d2)`. The generalized-form rho (`b` treated as an independent input, `d1,d2` independent of r) is the different formula the caveat writes, and it never collapses to the compact form at b=r. The caveat conflates these two.

**Note:** the *practical* claims in the caveat are correct and important — (a) Haug's table prints the compact convention (§2.16, matches 0.109656), and (b) at the worked example (b=0.05≠r=0.10) the true generalized derivative is **negative** (verified: −1.3605). Only the "agrees when b=r" sentence is wrong.

**Fix:** replace "which agrees with the compact form when b=r but differs otherwise" with something like "which is the correct rho when b is an independent input; it does NOT reduce to the compact form at b=r — the compact form is instead the correct rho of standard BSM where r enters d1,d2."

---

## Verified-correct items (no action)

### Formulas (boxed & in tables) — ALL CORRECT
- **BSM PDE** `01:50-52`, `02:41`: ∂V/∂t + rS∂V/∂S + ½σ²S²∂²V/∂S² − rV = 0; dΠ = (V_t+½σ²S²V_SS)dt = r(V−ΔS)dt. Correct (Hull 15.16; Shreve II 4.5.14).
- **d1/d2** `index:34-35`, `03:27`: ln(S/X)+(b±½σ²)T over σ√T. Correct.
- **Generalized call/put** `index:36-37`, `03:25-26`: correct cost-of-carry forms.
- **Cost-of-carry dictionary** `index:30`, `03:29-37`: b=r, r−q, 0, r−r_f — all correct; specializations (Merton/Black-76/GK/Asay) correct.
- **Put–call parity** `index:38`, `03:41`: c−p = S·e^{(b−r)T} − X·e^{−rT}; special cases correct; numerically verified.
- **Greeks table** `index:39-43`, `04:35-42`: Delta/Gamma/Vega/Theta/Rho (Haug §2.1–2.7) all match corpus; signs correct. Rho futures −Tc (−Tp) correct (Haug §2.16).
- **Gamma–theta / vega–gamma** `index:44`, `04:21,50`: ½ΓS²σ²=−Θ_driftless; Γ=−2Θ_driftless/(S²σ²); ν=ΓσS²T; Θ_driftless=−νσ/(2T). All correct.
- **Vanna/Volga** `04:54`: Vanna=−e^{(b−r)T}N'(d1)d2/σ; Volga=ν·d1d2/σ. Correct (Haug §2.3.3).
- **Price bounds** `03:47`, **ATM-forward approx** `index:45` (0.4·S·e^{(b−r)T}·σ√T, Brenner–Subrahmanyam). Correct.
- **Girsanov/risk-neutral** `02:52-64`: Z(t) form, W̃, dS=R S dt+σS dW̃, pricing formula 5.2.30/31. Correct.
- **Feynman–Kac** `02:68-73`: correct.
- **Merton closed form** `06:40` (formula only): σ_n = √(σ²+nσJ²/T), λ'=λ(1+κ). Correct as stated (the *code* implementing it is broken — Finding 1).
- **Delta-hedging P&L residual** `04:108,112`, `05:40`: ½ΓS²[(ΔS/S)²−σ²Δt], variance ∝ ½S⁴σ⁴Γ²Δt. Correct.

### Worked numbers — ALL CORRECT (re-executed)
Hub/index and 03/04 lookup tables:
- BSM call 2.13337, Merton put 2.46479, Black-76 1.70105, GK 0.029099 ✅
- Put-call parity 105.57354 ✅ · lower bound 0.12091 ≤ c=5.69445 ✅
- Delta 0.503105 · Gamma 0.026794 · Vega 19.2999/0.1930 · Theta −0.036989/day · Rho 10.9656/0.1097 ✅
- Gamma–theta 11.5800 ✅ · ATM approx 3.8713 vs exact 3.8579 ✅ (verified with e^{(b−r)T} factor included — initial naive check omitting it gave 3.92, corrected to 3.8713)
- Index/01 BSM call 10.4506 put 5.5735, parity 0.00e+00 ✅
- 01 binomial convergence: 4.4494 → 4.4496 as n↑; Haug-verified ✅
- 02 MC: closed form 10.4506, MC 10.6402/10.4839 ✅ (O(1/√n) gap as claimed)
- 04 Greeks vs Table 2-3 ✅ · 06 American put CRR 4.6921, premium 0.2427 ✅ (Haug §4.2 confirms)
- 05 delta-hedging P&L: frictionless mean≈0, stdev 0.9436; 0.5% costs mean −1.5371 ✅ (matches fence exactly, internally consistent)
- 05 constant-vol delusion: 24.5888 / 10.4506 / 3.2475 ✅

### Code blocks — execution & fence diff
**9 code blocks** extracted from 7 files, all executed in Python 3. **8 of 9** output fences match execution **character-for-character** (after whitespace trim). The 9th (`06` Merton MC) also matches its fence but the *code is logically broken* (Finding 1) — the fence faithfully records a wrong result.

### Coherence & links
- Structure: exactly index + 6 sub-pages (`01`–`06`); no stragglers. ✅
- All **wikilinks resolve** (none missing): hub↔sub-pages, foundations (stochastic-calculus, calculus-and-optimization), sibling topics (no-arbitrage-and-binomial, volatility-surfaces-and-smiles, heston-sabr, interest-rate-and-term-structure). ✅
- Prerequisite chain coherent: hub declares stochastic-calculus + calculus for 02–06, 01 self-declares smaller; 04→03, 05→04, 06→03+05 — all consistent with content order. ✅
- No jargon drift or contradictions between hub and sub-pages found. ✅
- Spelling/typos: none found in any of the 7 files.

---

## Files checked (7)
1. `index.md`
2. `01-from-zero-intuition.md`
3. `02-the-pde-and-derivation.md`
4. `03-the-pricing-formulas.md`
5. `04-greeks-and-hedging.md`
6. `05-failure-modes-and-practice.md`
7. `06-advanced-extensions.md`

**Blocks run:** 9 · **Errors found:** 2
