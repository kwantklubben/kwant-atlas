# Audit — `pillars/03-derivative-pricing/no-arbitrage-and-binomial/`

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages). No-arbitrage, replication, risk-neutral measure, state prices, CRR/up-down/p, martingale condition, FT1/FT2, complete vs incomplete, binomial→BSM convergence, American/perpetual options.
**Corpus cross-check:** `corpus/verified/shreve1_ch1-4.md`, `shreve1_ch5-8.md`, `shreve1_ch9-12.md`, `shreve2_ch4-5.md`, `bjork_ch1-7.md`, `hull_ch13-18.md` (Haug eq. numbering as cited in those files).
**Method:** (1) spelling/typo scan; (2) every boxed formula, table row and worked example re-derived and cross-checked against the verified corpus; (3) every ```python block executed and diffed against its output fence; (4) hub↔sub-page coherence, prerequisite chain, wikilink resolution.

---

## VERDICT: **FAIL** — 2 errors found (2 math/notation, 0 code, 0 spelling)

---

## Summary of findings

| # | Severity | File | Type | Issue |
|---|----------|------|------|-------|
| 1 | **MINOR–MODERATE** | `03-binomial-trees-and-convergence.md:47` | MATH (formula) | European truncated-sum start index stated as `i > X/(S u^{-n})` — dimensionally wrong; it is a price ratio, not an index (evaluates to ≈778 on the worked inputs). |
| 2 | **MINOR** | `06-advanced-extensions.md:47` | MATH (notation) | `log₂ S_k = S_0 + M_k` — wrong base-2 offset; should be `log₂ S₀ + M_k` (equivalently `S_k = S_0·2^{M_k}`). |

All **boxed formulas**, all lookup-table rows, and **all 10 ```python blocks + output fences** verified correct: the 10 code blocks were executed under Python 3 and **reproduce their fences character-for-character**. The two errors above are prose/derivation slips, not computational ones.

Plus 3 non-blocking notes (see end): a muddled martingale-condition sentence, one inconsistent wikilink alias, one typographic inconsistency.

---

## FINDING 1 — MINOR–MODERATE · truncated-sum threshold is not an index (`03-binomial-trees-and-convergence.md`)

**File/line:** `03-binomial-trees-and-convergence.md:47` (§2.2, "efficient truncation").

**Stated:**
> "Only nodes with $Su^id^{n-i}>X$ contribute, so one starts the sum at the smallest integer $i>X/(Su^{-n})$ — the standard speed-up … (Haug eq. 7.3–7.4)."

**Problem:** the threshold `i > X/(S u^{-n})` compares an integer node index `i` against a *price ratio*. The correct condition comes from solving the very inequality just written, `S u^i d^{n-i} > X`, for `i`:

$$i > \frac{\ln\!\big(X/(S d^{\,n})\big)}{\ln(u/d)} \qquad\Big(=\frac{\ln(X/S)+n\ln(1/d)}{\ln(u/d)}\Big).$$

**Numeric confirmation** (worked inputs `S=100, X=95, T=0.5, r=0.08, σ=0.30, n=1000` ⇒ `u=1.021440, d=0.979010`):
- Correct threshold: `i* = ln(95/(100·0.97901^1000)) / ln(1.021440/0.979010) = 496.18` ⇒ start the sum at `i = 497`. (Sanity: the first in-the-money node is at `i=497`, where `S u^497 d^503 ≈ 96.1 > 95`.)
- Stated expression: `X/(S u^{-n}) = 95 / (100·1.021440^{-1000}) = 778.14` — a dimensionless price ratio, not a node index. Taking it literally would either skip all in-the-money nodes or be nonsense as an index.

**Downstream impact:** none on the numbers — the code blocks compute the terminal/backward-induction values directly and all reproduce their fences. The defect is confined to the explanatory sentence.

**Fix:** replace `$i>X/(Su^{-n})$` with `$i>\dfrac{\ln(X/(S d^{n}))}{\ln(u/d)}$` (or simply "the smallest integer $i$ with $Su^id^{\,n-i}>X$").

---

## FINDING 2 — MINOR · wrong base-2 offset in the random-walk representation (`06-advanced-extensions.md`)

**File/line:** `06-advanced-extensions.md:47` (§2.2, "The random walk underneath").

**Stated:**
> "Under $\widetilde{\mathbb P}$, $\log_2 S_k=S_0+\!M_k$ with $M$ a symmetric $\pm1$ walk."

**Problem:** the offset must be `log₂ S₀`, not `S₀`. With this folder's running parameters `S₀=4, u=2, d=½`, the corpus states `S_k = S_0·2^{M_k}`, i.e.

$$\log_2 S_k = \log_2 S_0 + M_k = 2 + M_k .$$

As written, `log₂ S_k = S₀ + M_k = 4 + M_k` implies `S_k = 16·2^{M_k}`, contradicting `S₀=4` (and the tree values `S₁(H)=8, S₂(HH)=16` used immediately below).

**Corpus cross-check:** `shreve1_ch5-8.md:163` — "`S_k = S_0·2^{M_k}` with `M_k` a symmetric walk under the risk-neutral measure `P̃`". Confirms the `log₂ S₀` offset.

**Fix:** `$\log_2 S_k=\log_2 S_0+M_k$` (or `$S_k=S_0\,2^{M_k}$`).

---

## Verified-correct items (no action)

### Formulas (boxed & in tables) — ALL CORRECT
- **No-arbitrage bracket** `index:33`, `01:35,50`, `05:35`: `d<1+r<u`; the strict form and the Björk Prop 2.3 non-strict / Prop 2.26 strict split (`01:40`) match `bjork_ch1-7.md`. Correct.
- **Risk-neutral probabilities** `index:34`, `01:54`, `03:39`, `05:35`: `p̃=(1+r−d)/(u−d)`, `q̃=(u−1−r)/(u−d)=1−p̃`; CRR `p=(e^{bΔt}−d)/(u−d)`. Correct (Shreve 1.8, Hull 13.17).
- **Replicating delta** `index:35`, `01:50`: `Δ₀=(f_u−f_d)/(S₀(u−d))` ≡ `(V1(H)−V1(T))/(S1(H)−S1(T))`. Correct (Shreve 1.6).
- **One-period / multiperiod RN valuation** `index:36,37`, `01:54,62`, `02:35`: `V₀=½ ₍₁₊ᵣ₎⁻¹[p̃f_u+q̃f_d]`, `V_k=(1+r)^k Ẽ[V_m/(1+r)^m|F_k]`. Correct (Shreve 1.9, §3.4).
- **State prices** `index:38,39`, `02:55–63`, `05:131`: `ζ(ω)=P̃(ω)/(1+r)`, `Σζ=1/(1+r)`, `V₀=Σζ f = E^P[ζ f]`, `ζ=Z/(1+r)`, `Z=dP̃/dP`. Correct; Björk Prop 3.18 / Shreve Ch 9 corroborated (`bjork_ch1-7.md:40`, `shreve1_ch9-12.md`).
- **CRR up/down/step-scaling** `index:40`, `03:31`, `06:20,55`: `u=e^{σ√Δt}`, `d=1/u=e^{−σ√Δt}`; log-step `±σ√Δt`. Correct (Hull 13.15/13.16).
- **Per-step log-variance** `03:33`: `4σ²Δt·p(1−p) ≈ σ²Δt` for `p≈½` — re-derived, exactly matches `σ²Δt[1−(2p−1)²]`. Correct.
- **European CRR closed sum** `index:42`, `03:45`: put/call terminal sums with binomial weights. Correct (Haug 7.1–7.6).
- **American backward induction** `index:43`, `03:53`, `05:43`, `06:30`: `P_{j,i}=max(X−Su^id^{j−i}, e^{−rΔt}[pP_{j+1,i+1}+(1−p)P_{j+1,i}])`. Correct (Haug 7.9–7.11).
- **Self-financing wealth identity** `02:47`: `X_{k+1}=(1+r)X_k+Δ_k(S_{k+1}−(1+r)S_k)`. Re-derived, correct; the bracket is a `P̃`-martingale increment since `p̃u+q̃d=1+r`. Correct (Shreve §3.3).
- **FT1/FT2** `index:44,45`, `04:36,38,44,46`: FT1 `no-arb ⟺ EMM exists`, FT2 `complete ⟺ EMM unique`; Farkas form `Z₀=D^Z q`, `q_j>0`, `Σq_j=1`; completeness dual `Im[D*]=R^M` / `Ker[D]=0`. Correct — `shreve2_ch4-5.md:95,96` (Thm 5.4.7 / 5.4.9) and `bjork_ch1-7.md:34,39` corroborate.
- **Market-price-of-risk system** `04:52`: `α_i−R=Σ_j σ_ij Θ_j`, i=1..m — "m equations, d unknowns". Correct (`shreve2_ch4-5.md:93`, eq. 5.4.18).
- **Three-case table** `04:62–66` (no solution / many / unique → arbitrage / interval / unique price). Correct (Shreve II §5.7).
- **American value as smallest supermartingale** `05:55`, `06:32–37`: Def 6.1(a)–(d), `τ*=min{k:V_k=G_k}`, consumption `C_k=V_k−(1+r)⁻¹Ẽ[V_{k+1}|F_k] ≥ 0` (Lemma 2.21). Correct (`shreve1_ch5-8.md:71,86,105`).
- **No-early-exercise for a dividend-free call** `05:47–51`: `Ẽ[(1+r)^{−n}g(S_n)] = max_τ Ẽ[(1+r)^{−τ}g(S_τ)]`, convex `g` with `g(0)=0`, `r≥0`, submartingale + optional sampling. Correct — matches Shreve Ch 7 **Corollary 2.25** (`shreve1_ch5-8.md:115–121`) verbatim in substance.
- **Perpetual American put** `index:46`, `06:39–43`: `v(x)=6/x (x≥3)`, `v(x)=5−x (0<x≤3)`, kink `(3,2)`, exercise on first `S≤2`; three-part supermartingale verification. Correct — `shreve1_ch5-8.md:190–194` (piecewise, §8.8) and `:171,227` (exercise rule, §8.6–8.7).
- **First-passage moments** `06:49`: `E[α^{τ_m}]=((1−√(1−α²))/α)^m`, `E[α^{τ_1}]=(1−√(1−α²))/α`. Correct (`shreve1_ch5-8.md:147,159`).
- **Bracket-failure condition** `05:35`: `σ>r√Δt` from `e^{−σ√Δt}<e^{rΔt}<e^{σ√Δt}`. Correct derivation.
- **Binomial→BSM limit** `03:59`, `06:59`: terminal `S_T=S_0e^{(r−½σ²)T+σ√T Z}`, convergence `O(1/n)` with oscillation. Correct (Hull §13.9).

### Worked numbers — ALL CORRECT (re-executed)
- One-period replication: `Δ₀=−0.5000`, `V₀=1.2000`, bond `3.2000`, both states replicate `0/3`; bracket `0.50<1.25<2.00` ✅
- Risk-neutral `p̃=q̃=0.5`; state prices `ζ(H)=ζ(T)=0.4`, `Σζ=0.8=1/1.25` ✅
- Discounted-stock martingale `Ẽ[S₁/(1+r)]=Ẽ[S₂/(1+r)²]=4.0=S₀`; price `1.2000` invariant across physical `p=0.5/0.6/0.9` ✅
- CRR `n=100`: `u=1.021440`, `d=0.979010`, `p=0.504126` ✅
- CRR European put: `n=1000 → 4.4496` vs BSM `4.4494` (Haug-verified pair) ✅; oscillation table `n=10…5000` reproduced ✅
- CRR American put `n=1000 → 4.6921`, early-exercise premium `0.2427` (+5.2%) ✅
- ATM American-put oscillation series `n=2…12` reproduced (5.73765 … 6.01855) ✅
- American call ≈ European (diff → 0 like `1/n`: −0.019972 / −0.001999 / −0.001000) ✅
- FT2 rank example: price interval `[0.595238, 0.666667]`; after 3rd asset unique `0.628571`; `ζ=(0.404762,0.380952,0.166667)`, `Σζ=0.952381` ✅
- Perpetual put `v(4)=1.5000`, `v(8)=0.7500`, `v(1)=4.0`, `v(2)=3.0`; `E[α^{τ_1}]=0.5`, `E[α^{τ_2}]=0.25` ✅
- Bracket-failure row `σ√Δt=0.894 < rΔt=1.0`, `p=1.133694` ✅

### Code blocks — execution & fence diff
**10 code blocks** across 7 files, all executed under Python 3. **10 of 10** output fences match execution **character-for-character** (after whitespace trim). No broken logic, no randomness-dependent divergence.

### Coherence & links
- Structure: exactly `index.md` + 6 sub-pages (`01`–`06`); no stragglers. ✅
- All **wikilinks resolve** (18 distinct targets, none missing): hub↔sub-pages, foundations (probability-and-measure-theory, stochastic-calculus), sibling topics (black-scholes-merton + its 01/02/04/05 sub-pages, advanced-volatility-heston-sabr, interest-rate-and-term-structure, volatility-surfaces-and-smiles). ✅
- Prerequisite chain coherent: hub declares probability+algebra for `02`–`06` and notes `01` self-declares a smaller set (`01:11`); `02←01`, `03←02`, `04←02`, `05←03`, `06←04+05` — all consistent with content order. ✅
- No jargon drift or hub↔sub-page contradictions found. Where the hub signposts failure modes it defers correctly to `05`.
- Spelling/typos: **none** found in any of the 7 files.

---

## Non-blocking notes (no error, optional polish)

1. `02-no-arbitrage-and-risk-neutral.md:41` — "Under the *physical* measure, $S_k$ is a martingale only if $pu+qd=1$; here $pu+qd\ne1+r$ in general …". The two clauses mix the *undiscounted* martingale condition (`pu+qd=1`) with the *discounted* one (`pu+qd=1+r`). Both statements are individually true, but the juxtaposition reads as if `1` and `1+r` were interchangeable; splitting it ("`S_k` is a P-martingale only if `pu+qd=1`, whereas the *discounted* stock is a P-martingale only if `pu+qd=1+r`, which fails in general …") would be cleaner.
2. `03-binomial-trees-and-convergence.md:11` vs `index.md:117` (and `06:162`) — the same target `foundations/stochastic-calculus/index` carries three different aliases: `Stochastic Calculus & Itô's Lemma` (03) vs `Stochastic Calculus & Itô` (index/06). Cosmetic; align the alias.
3. `06-advanced-extensions.md:39` — `$p̃=q̃=\tfrac12$` uses Unicode combining tildes (`p̃`, `q̃`) inside math, whereas every other page uses `$\tilde p$`/`$\tilde q$`. Purely typographic; normalize to `\tilde p=\tilde q=\tfrac12`.
4. (Citation span, informational) `06:39` attributes both the piecewise value function *and* the exercise rule to "Shreve Ch 8.8"; the corpus places the piecewise formula in §8.8 (`shreve1_ch5-8.md:190`) and the binomial exercise rule in §8.6–8.7 (`:161–174`). No numerical consequence — cite `§8.6–8.8` if precision is wanted.

---

## Files checked (7)
1. `index.md`
2. `01-from-zero.md`
3. `02-no-arbitrage-and-risk-neutral.md`
4. `03-binomial-trees-and-convergence.md`
5. `04-fundamental-theorems.md`
6. `05-failure-modes-and-practice.md`
7. `06-advanced-extensions.md`

**Blocks run:** 10 · **Errors found:** 2
