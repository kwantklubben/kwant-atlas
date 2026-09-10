# Audit Report: `content/pillars/03-derivative-pricing/interest-rate-and-term-structure/`

**Date:** 2026-09-10
**Folder:** `content/pillars/03-derivative-pricing/interest-rate-and-term-structure/` (7 files)
**Reviewer:** Sole adversarial reviewer (subagent)
**House style used:** wikilinks `[[full/path|Alias]]`; math `$..$`/`$$..$$`; folder = index hub + 6 sub-pages.

---

## Scope & verdict

**Verdict: APPROVE WITH MINOR PRECISION NOTES.** No wrong final formula, wrong sign/constant, or numerical error found. All 7 `python` blocks were extracted verbatim, executed, and diffed against their trailing output fences — **7/7 exact match**. All 17 boxed formulas and worked examples were re-derived / reproduced. Findings are notation & precision slips that do not change any computed value.

| Metric | Value |
|---|---|
| Files checked | 7 |
| Python blocks run | 7 (all MATLAB-checks passed; outputs match fences exactly) |
| Errors found | 4 (all minor; 1 math-precision, 3 notation/consistency) |
| Math formulas checked | 17 (Vasicek, CIR & Feller, H-W θ, HJM drift, Black caplet/swaption, Bachelier, swap rate, LFM drift/martingale, bias/forward-futures) |

---

## 1. Spelling & typos

- **No spelling errors found.** Targeted scan for common misspellings (`recieve`, `seperate`, `occured`, `untill`, `paramter`, `dependant`, etc.) returned nothing. Prose is clean. Domain terms (`numeraire`, `caplet`, `swaption`, `monte`, `carlo`, `lognormal`, `collateralized`) are used consistently.
- `Björk`/`Shreve`/`Brigo–Mercurio` diacritics are consistent throughout.

---

## 2. Mathematical accuracy — per formula / worked example

All formulas below were independently re-derived and, where computational, reproduced. **Code outputs in the repo match the fences exactly** (verbatim run), so every "Verified check" number in the index table is reproduced.

| Formula / claim | File:loc | Verdict |
|---|---|---|
| Stochastic discount `D(t,T)=B(t)/B(T)=e^{-∫_t^T r}` | index:37 | ✅ correct |
| ZCB `P(t,T)=E^Q[e^{-∫ r}]` | index:38 | ✅ correct |
| Instantaneous forward `f=-∂_T ln P`, `P=e^{-∫ f}` | index:39 | ✅ correct (binary identities) |
| Simple forward `L=(P(t,T)/P(t,S)-1)/τ`, flat 4% → 4.0403% | index:40 | ✅ `(1/0.9802-1)/0.5=0.0404` reproduced |
| **Vasicek** `B=(1-e^{-aτ})/a`, `A=exp{…}`; `P(0,5)=0.807678` | index:41, 03:49 | ✅ closed form correct; A matches standard `exp{(b-σ²/2a²)(B-τ)-σ²B²/4a}`; value reproduced |
| **CIR** `B=2(e^{hτ}-1)/((h+a)(e^{hτ}-1)+2h)`, `h=√(a²+2σ²)`; `P(0,5)=0.804696` | index:42, 03:59 | ✅ correct; value reproduced |
| **Feller** `2ab ≥ σ²` ⟹ r unattainable at 0 | 03:57, 03:119 | ✅ correct |
| **Hull–White** θ(t)=∂_T f^M(0,t)+a f^M(0,t)+σ²/2a(1-e^{-2at}); θ(0)=.0040,θ(5)=.0047 | index:43, 03:65 | ✅ correct; values reproduced |
| **HJM drift** `α(t,T)=σ(t,T)∫_t^T σ(t,s)ds` | index:44, 04:54 | ✅ correct |
| **Caplet=Black** `Cpl=P(0,T_i)τ[F N(d1)-K N(d2)]`, d1,v; `F=4.0403%,K=4%…=0.001637` | index:45 | ✅ value reproduced (see note E4 below on caption) |
| **Black swaption** `PS=C_{α,β}(0)[R(0)N(d1)-K N(d2)]`; 5y-into-5y ATM v=.15 → 0.023902 | index:46, 04:78 | ✅ reproduced |
| **Swap rate** `R=(P(t,T_α)-P(t,T_β))/C`, flat 4% 5y semi → 4.0403% | index:47, 02:45 | ✅ `R=0.04040268` reproduced |
| Forward price `=E^{Q^T}[Y]`; futures `=E^Q[Y]`; equal iff r deterministic | index:49, 04:44 | ✅ correct (Björk Ch29) |
| Radon–Nikodym `dQ^T/dQ = 1/[B(T)P(0,T)]`; pricing `Π_t(X)=P(t,T)E^{Q^T}[X]` | 04:36,40 | ✅ correct |
| Girsanov kernel between numeraires = vol difference | 04:42 | ✅ correct |
| LFM `dF_k=σ_k F_k dZ_k` under Q^{T_k} — caplet exact by Black | 04:66,70 | ✅ correct (BM Prop 6.4.1) |
| LFM drift under common measure `σ_kF_k[Σ ρ_kj τ_j σ_j F_j/(1+τ_jF_j)]dt + σ_kF_k dZ` | 04:74 | ✅ correct (BM Prop 6.3.3) |
| Bachelier caplet `Pτ[(F-K)N(d)+σ_N√T φ(d)]`, d=(F-K)/(σ_N√T) | 05:40 | ✅ correct formula |
| SABR/Hagan beta-skew `∝-½(1-β)`, vanna-skew `∝½ ρ λ` | 06:51 | ✅ correct; numeric smile reproduced |
| UPM mixture → implied-vol min at ATM | 06:55-59, 06:118-124 | ✅ reproduced (min 15.99% at 4.00/4.04%) |

**Worked examples / MC convergences** — all reproduced:
- 01 Vasicek MC `P(0,5)=0.807521` vs closed `0.807678` ✅
- 03 Vasicek/CIR closed vs MC err `2.1e-4 / 2.8e-4`; Feller `2ab=0.0200≥σ²=0.0025`; H-W MC exact-fit `0.818932` vs `e^-0.2=0.818731` ✅
- 04 caplet `0.002377`, LFM martingale `E^{Q^Ti}[F]=0.040420≈F(0)=0.040403`, swaption `0.023902`, forward=futures `104.0811` ✅
- 05 explosion `c/(1-ct)` → `1000%` at 19.9yr; Bachelier `K=0 → 0.010620` ✅
- 02 reconstruction `err~10^-11`, cap/floor parity `err 3.0e-05` ✅

---

## 3. Code audit — every ```python block run & diffed

All blocks executed with Python 3 and compared line-by-line (ignoring trailing whitespace/blank lines) against the following output fence.

| File | Block | Result |
|---|---|---|
| index.md | formula engine (Vasicek/CIR/caplet) | ✅ EXACT MATCH |
| 01-from-zero-intuition.md | Vasicek MC bond | ✅ EXACT MATCH |
| 02-bonds-yield-curve-forward-rates.md | curve toolkit + cap/floor parity | ✅ EXACT MATCH |
| 03-short-rate-models.md | closed vs MC + Feller + H-W θ | ✅ EXACT MATCH |
| 04-numeraire-hjm-and-market-models.md | caplet + LFM martingale + swaption | ✅ EXACT MATCH |
| 05-failure-modes-and-practice.md | explosion + Bachelier/Black + corr + instability | ✅ EXACT MATCH |
| 06-advanced-extensions.md | UPM smile + SABR vol | ✅ EXACT MATCH |

**7/7 blocks run, 7/7 exact.** Stdlib-only claim holds (only `math` + `random` imported).

---

## 4. Coherence / links / jargon

- **All 16 wikilink targets resolve** (checked against `content/`). `black-scholes-merton` links point at the folder root (other pages use the same `.../black-scholes-merton` folder form; resolves to index via folder link) — consistent with sibling usage. No broken links.
- Hub/folder structure correct: index.md is the hub; 6 sub-pages; prerequisite chains are strictly linear (01→02→03→04→05→06), each `Back`/`Forward`/`Base` bridge consistent.
- Index hub states "page 01 states its own, smaller, entry requirements" — ✅ accurate (01 lists only Stochastic Calc, while hub lists Stochastic Calc + Multivariable Calc for 02–06).
- Jargon consistent: `short rate`, `instantaneous forward`, `simple/LIBOR forward`, `annuity (swap) measure`, `forward measure`, `numeraire` all used with identical meaning across pages.
- **Forward price = E^{Q^T}[Y], futures = E^Q[Y], equal iff r deterministic** stated consistently in index:49, 04:44, 05 failure #4. No contradictions.
- HJM-explosion and "model simple (LIBOR) rates instead" storyline consistent across index:95, 04 §2.3, 05 §2.
- One internal-consistency observation (non-error): 05 boxed Black/Bachelier caplets show a `P·τ` multiplier (per BM 1.26ff), but the block's `blk`/`bach` functions omit the day-count τ; harmless because the example uses τ=1.0, and the fence still matches.

---

## Findings (minor — none affect final numbers)

**E1 (math-precision, minor).** Index:49 and 04:42 attribute *both* forward LIBOR `L(t;T,S)` and the instantaneous forward `f(t,T)` to the same forward measure `Q^T`. Correctly: `f(t,T)` is a `Q^T`-martingale (numeraire P(·,T)), but `L(t;T,S)=(P(t,T)/P(t,S)-1)/(S-T)` is a martingale under **`Q^S`** (numeraire P(·,S)) — the two maturity indices differ. The LFM section (04:64-70) already states this correctly (`F_k=L(t;T_{k-1},T_k)` is a martingale under `Q^{T_k}`). Fix suggestion: "the forward measure `Q^T` makes `f(t,T)` a martingale and the forward measure `Q^S` makes `L(t;T,S)` a martingale."

**E2 (notation inconsistency, minor).** 04:70 writes caplet `d_1 = (ln(F_i/K)+½v_i²(t,T_i))/(v_i√(T_i-t))` with `v_i²=∫_t^{T_{i-1}}σ_i²(s)ds`. The vol-horizon indices disagree (integral to `T_{i-1}`, squared-vol label `T_i`, denominator horizon `T_i-t`). Black's d1 needs a *single* consistent vol accumulation window; the code in the same page uses `T_i` uniformly, so nothing is miscalculated. Fix suggestion: use one index (e.g. `v_i²=∫_t^{T_{i-1}}σ_i²(s)ds` and `d1=(ln(F_i/K)+½v_i²)/v_i`).

**E3 (formula-vs-code τ mismatch, minor; no numeric effect).** 05:40 Bachelier boxed formula and 05:38 Black caplet include a `τ` (day-count) multiplier `P·τ[…]`, but the accompanying block's `bach(...)`/`blk(...)` define the price *without* the τ multiplier. Since the demonstration uses τ=1.0, the fence value is unaffected. For transferability, either add `tau` to the code or note the τ=1 simplification.

**E4 (caption precision, minor).** Index:45 verifies the "Flat/ATM caplet" with code `caplet_black(0.040403,0.04,…)`, i.e. **F=4.0403%**, K=4%. The table caption reads "F=K=4%", which is slightly off (the noisier flat-curve forward F=4.0403% is used). The check number `0.001637` is correct for that F; only the caption's "F=K=4%" should be "F=4.0403%, K=4%".

---

## Summary recommendation

All content is **substantially correct**: formulas, closed forms, MC reproductions, and all 7 code blocks are verified exact. The four findings are notation/precision slips with **zero impact on any computed value**. Recommend approval with the minor fixes in E1–E4 (E1 being the only math-adjacent precision point and worth correcting in both index:49 and 04:42).