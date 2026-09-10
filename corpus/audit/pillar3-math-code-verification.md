# Pillar 3 (Derivative Pricing) — Independent Math & Code Verification

**Scope:** `content/pillars/03-derivative-pricing/` — the 8 topic folders (black-scholes-merton,
volatility-surfaces-and-smiles, advanced-volatility-heston-sabr, no-arbitrage-and-binomial,
numerical-methods, exotic-and-path-dependent-options, interest-rate-and-term-structure,
counterparty-risk-and-xva) plus their 7 top-level pillar-overview pages.
**Authority:** `corpus/verified/` (hull_*, shreve*, bjork_*, bm_*, glasserman_*, gatheral_*, bergomi_*,
duffy_*, haug_lookup-*, gregory_*, …).
**Method:** (1) hand cross-check of sampled formulas against the corpus text; (2) automated
extraction of every ```python block + its following output block, executed with `python3`
(numpy/scipy installed only for the top-level overview pages), stdout diffed against the
page's claimed output block; (3) targeted numerical re-derivation of any suspicious formula.
**Date:** 2026-09-10.

---

## Verdict summary

| Category | Result |
|---|---|
| Formulas sampled (cross-checked vs corpus) | 22 |
| **Formula PASS** | **21** |
| **Formula FAIL** | **1** (general put-call parity — see F01) |
| Code blocks found / executed | 73 / 73 |
| **Code MATCH** (stdout == claimed) | **63** |
| Code NO-CLAIMED-OUTPUT (index/overview pages, ran clean) | 5 |
| Code **MISMATCH** (cosmetic only, values correct) | **3** (C01–C03) |
| Code hard FAIL (wrong output) | **0** |
| All 8 folders represented by ≥1 executed block | yes (min 5 blocks/folder) |

**Net:** the pillar is mathematically sound except for **one wrong general formula** (put-call
parity carried over from a transcription slip in the corpus), and three purely cosmetic
output-block formatting/ordering discrepancies. No code block produces wrong numerical output.

---

## Part 1 — Sampled formula verification (page vs. verified corpus)

Reference keys are the equation numbers in the corpus files.

### black-scholes-merton

| # | Formula (as written on the page) | Corpus source | Result |
|---|---|---|---|
| 1 | Generalized BSM `c = S e^{(b−r)T}N(d₁) − X e^{−rT}N(d₂)`, `p = X e^{−rT}N(−d₂) − S e^{(b−r)T}N(−d₁)`, `d₂=d₁−σ√T` | haug_lookup-1 §1.1.6 (eq 1.11–1.12); numeric c=2.13337, p=2.46479, Black-76 1.70105, GK 0.029099 | **PASS** (all four Haug numbers reproduce) |
| 2 | **Put–call parity** `c − p = S e^{bT} − X e^{−rT}` | haug_lookup-1 §1.9 (eq 1.18) *as transcribed* | **FAIL — see F01** |
| 3 | Bounds `c ≥ max(S e^{(b−r)T} − X e^{−rT}, 0)`, `p ≥ max(X e^{−rT} − S e^{(b−r)T}, 0)` | Hull 17/18; consistent with model | **PASS** |
| 4 | Greeks: `Δ_c=e^{(b−r)T}N(d₁)`, `Δ_p=−e^{(b−r)T}N(−d₁)`, `Γ=e^{(b−r)T}n(d₁)/(Sσ√T)`, `ν=Se^{(b−r)T}n(d₁)√T`, `Θ_c=−Se^{(b−r)T}n(d₁)σ/(2√T)−(b−r)Se^{(b−r)T}N(d₁)−rXe^{−rT}N(d₂)`, and `Γ=−2Θ_driftless/(S²σ²)`, `ν=ΓσS²T` | haug_lookup-1 §2.1, 2.5, 2.3.3 (eq 2.1–2.2, 2.15); numeric Δ=0.503105, Γ=0.026794, ν/100=0.192999, θ/day=−0.036989 | **PASS** (code reproduces every Haug value) |

### volatility-surfaces-and-smiles

| # | Formula | Corpus source | Result |
|---|---|---|---|
| 5 | Dupire strike form `∂C/∂T = ½σ²K²∂²C/∂K² + μ(C − K∂C/∂K)`, `μ=r−D` | gatheral 1.4 | **PASS** |
| 6 | Local vol `σ_L²(K,T) = (∂C/∂T)/(½K²∂²C/∂K²)` | gatheral 1.6 | **PASS** |
| 7 | Dupire in implied total variance `v_L = (∂_T w)/[1 − (y/w)w_y + ¼(−¼−1/w+y²/w²)w_y² + ½w_yy]` | gatheral 1.10 (vision-verified); bergomi 2.19 | **PASS** (matches both; Bergomi 2.19 expands identically, per corpus note) |
| 8 | `σ_L²(K,T)=E[v_T | S_T=K]`; gamma-weighted implied-variance average | gatheral 1.12, 3.5; bergomi 2.32 | **PASS** |
| 9 | SVI `w(k)=a+b[ρ(k−m)+√((k−m)²+s²)]` | gatheral 3.20 | **PASS** (param renamed σ→s vs vol; form identical) |

### advanced-volatility-heston-sabr

| # | Formula | Corpus source | Result |
|---|---|---|---|
| 10 | Heston CF: `α=−u²/2−iu/2+iju`, `β=λ−ρηj−ρηiu`, `γ=η²/2`, `r±=(β±d)/η²`, `d=√(β²−4αγ)` | gatheral 2.9–2.11 | **PASS** |
| 11 | `D=r₋(1−e^{−dτ})/(1−g e^{−dτ})`, `C=λ{r₋τ−(2/η²)ln[(1−g e^{−dτ})/(1−g)]}`, `g=r₋/r₊` | gatheral 2.12 | **PASS** |
| 12 | `φ_T(u)=exp(C v̄ + D v₀)`; checks φ(0)=1, φ(−i)=1; Lewis price `C=F−√(FK)/π ∫ du/(u²+¼) Re[e^{−iuk}φ(u−i/2)]` | gatheral 2.15, 5.6 | **PASS** (code verifies BS collapse + parity + martingale) |
| 13 | SABR (Hagan) `σ_BS=σ₀ (y/f(y))(1+¼ρνσ₀+((2−3ρ²)/24)ν²τ)`, `y=−νk/σ₀`, `f(y)=ln[(√(1−2ρy+y²)+y−ρ)/(1−ρ)]` | gatheral 7.7 | **PASS** (independently re-expanded: y/f(y)=1−½ρy+(2−3ρ²)/12 y²) |
| 14 | `S₀=ρν/2`, `C₀=(2−3ρ²)ν²/(6σ₀)`, Bergomi–Guyon `ν²=3σ₀C₀+6S₀²` | gatheral 7.7, bergomi 8.35a–c | **PASS** (re-derived by hand: ν²=3σ₀C₀+6S₀² holds exactly) |

### no-arbitrage-and-binomial

| # | Formula | Corpus source | Result |
|---|---|---|---|
| 15 | CRR `u=e^{σ√Δt}`, `d=1/u`, `p=(e^{bΔt}−d)/(u−d)`, `S_{j,i}=S u^i d^{j−i}`, European CRR sum, American induction `P_{j,i}=max(X−S…, e^{−rΔt}[pP_{j+1,i+1}+(1−p)P_{j+1,i}])` | hull 13.15/13.16/13.17/13.18; haug 7.1/7.9–7.11 | **PASS** (per-step log-variance 4σ²Δt·p(1−p) also verified correct) |

### numerical-methods

| # | Formula | Corpus source | Result |
|---|---|---|---|
| 16 | θ-scheme `(U^{n+1}−U^n)/k=(1−θ)LU^{n+1}+θLU^n`; von Neumann symbols: explicit `1−4λsin²(βh/2)` (λ≤½), CN `(1−2λsin²)/(1+2λsin²)` | duffy 8.34/8.35 (**erratum: printed 4λ², correct 4λ**), 8.37 | **PASS — erratum handled correctly** (page flags it explicitly) |
| 17 | MC estimator `α̂_n−α ≈ N(0, σ_f/√n)`; O(n^{−1/2}); exact GBM transition | glasserman 1.2 (CLT), 3.20–3.22 | **PASS** |

### exotic-and-path-dependent-options

| # | Formula | Corpus source | Result |
|---|---|---|---|
| 18 | Reiner–Rubinstein barrier blocks A–F, `μ=(b−σ²/2)/σ²`, `λ=√(μ²+2r/σ²)`, `x₁,x₂,y₁,y₂,z`; in–out parity table | haug_lookup-2 §5.1 (eq 4.51–4.52, `[V-8]`) | **PASS** (blocks match verbatim; Haug Table 4-13 values reproduce) |

### interest-rate-and-term-structure

| # | Formula | Corpus source | Result |
|---|---|---|---|
| 19 | Vasicek `B=(1−e^{−aτ})/a`, `A=exp{(B−τ)(a²b−½σ²)/a² − σ²B²/(4a)}` | bjork Prop 24.3 (ab−σ²/2 form) | **PASS** (b = *long-run mean* level → a²b convention; Brigo/Wikipedia standard, self-consistent with page's `dr=a(b−r)dt+σdW`, `b`=mean) |
| 20 | CIR `B=2(e^{hτ}−1)/((h+a)(e^{hτ}−1)+2h)`, `A=[2h e^{(a+h)τ/2}/((h+a)(e^{hτ}−1)+2h)]^{2ab/σ²}`, `h=√(a²+2σ²)`, Feller `2ab≥σ²` | bjork Prop 24.6 | **PASS** |
| 21 | Hull–White `θ(t)=∂_T f^M(0,t)+a f^M(0,t)+(σ²/2a)(1−e^{−2at})` | bjork Prop 24.8 (Lemma 24.7) | **PASS** |
| 22 | **Björk forward-vs-futures**: forward `f=E^{Q^T}[Y]`, futures `F=E^Q[Y]`, equal iff r deterministic | bjork Ch29 (**corpus-flagged correction**) | **PASS — correction handled correctly** (page cites "Björk Ch29 correction") |

### counterparty-risk-and-xva

| # | Formula | Corpus source | Result |
|---|---|---|---|
| 23 | `UCVA=−E[1_{τ≤T}V(t,τ)^+ LGD]`; `UCVA=−LGD∫λ_C D_{r+λ_C} EPE du`; discrete `−LGD Σ EPE·PD`; `DVA=−LGD_P∫λ_P D_{r+λ_C+λ_P} ENE du`; `BCVA=CVA+DVA`; spread approx `BCVA≈−EPE·s_C−ENE·s_P` | gregory eq 17.1/17.2/17.3/17.7a–c/17.9 | **PASS** |

### The one formula FAIL

**F01 — General put-call parity is wrong (black-scholes-merton/03 line 41, and index.md line 38).**

Page writes:
```
c − p = S e^{bT} − X e^{−rT}
```
This is **mathematically wrong** and **contradicts the page's own special cases** printed two
lines later (`stock c−p=S−Xe^{−rT}`; `yield c−p=Se^{−qT}−Xe^{−rT}`). The correct generalized
parity is
```
c − p = e^{−rT}( S e^{bT} − X ) = S e^{(b−r)T} − X e^{−rT}
```
(i.e. the forward `Se^{bT}` discounted, since in Haug's convention the forward is `F=Se^{bT}`).

Numerical confirmation (S=100, X=105, T=0.5, r=0.10, q=0.05 ⇒ b=0.05, model `c−p=−2.348098`):

| candidate form | value | verdict |
|---|---|---|
| model `c−p` | −2.348098 | — |
| `S e^{(b−r)T} − X e^{−rT}` | −2.348098 | ✅ correct |
| page's `S e^{bT} − X e^{−rT}` | **+2.652422** | ❌ wrong (factor e^{rT} on spot term) |
| page's own special case `S e^{−qT} − X e^{−rT}` | −2.348098 | ✅ correct |

Stock check (b=r): model `c−p=0.12091` = `S−Xe^{−rT}` ✅ but page's general form gives
`Se^{rT}−Xe^{−rT}=5.24802` ❌.

**Root cause:** the content page reproduces **verbatim** the corpus transcription
`corpus/verified/haug_lookup-1.md` line 95, which has the same defect. Haug's (1.18) is the
forward-discounted form `e^{−rT}(Se^{bT}−X)`; the corpus transcription dropped the `e^{−rT}`
factor on the spot term. The corpus's own Haug eq 1.13/1.14 special cases (verified numerically)
confirm the correct form. So this is a **corpus-inherited error propagated into two content pages**.

**Fix:** change both pages to `c − p = e^{−rT}(Se^{bT}−X) = Se^{(b−r)T}−Xe^{−rT}` (and correct
`corpus/verified/haug_lookup-1.md` eq 1.18).

---

## Part 2 — Code-block execution results

All 73 ```python blocks across the 63 Pillar-3 markdown files were extracted with their
following output block, executed, and stdout compared to the claimed output.

### Per-folder tally

| Folder | blocks | MATCH | MISMATCH | NO-CLAIMED | FAIL |
|---|---|---|---|---|---|
| black-scholes-merton | 9 | 9 | 0 | 0 | 0 |
| volatility-surfaces-and-smiles | 7 | 6 | 0 | 1 | 0 |
| advanced-volatility-heston-sabr | 7 | 7 | 0 | 0 | 0 |
| no-arbitrage-and-binomial | 10 | 10 | 0 | 0 | 0 |
| numerical-methods | 9 | 9 | 0 | 0 | 0 |
| exotic-and-path-dependent-options | 9 | 8 | 1 | 0 | 0 |
| interest-rate-and-term-structure | 7 | 5 | 2 | 0 | 0 |
| counterparty-risk-and-xva | 9 | 9 | 0 | 0 | 0 |
| **subtotal (8 folders)** | **67** | **63** | **3** | **1** | **0** |
| top-level pillar-overview pages | 6 | 0 | 0 | 4 | 0 (all run rc=0 with numpy/scipy) |

Every one of the 8 folders has ≥5 independently executed MATCH blocks. Blocks in the
top-level overview pages (`advanced-volatility-heston-and-sabr.md`,
`black-scholes-merton-and-feynman-kac.md`, `implied-volatility-surface-and-smiles.md`,
`interest-rate-and-term-structure-models.md`, `no-arbitrage-and-binomial-trees.md`,
`the-greeks-and-dynamic-hedging.md`) import numpy/scipy and have no following output block;
they all execute cleanly (rc=0) once numpy 2.5.3 / scipy 1.18.1 are present. Note: the claim
"stdlib-only" applies to the 8 folder pages; the overview pages are not stdlib-only.

### MISMATCH detail — all cosmetic (values identical)

| id | block | file | nature |
|---|---|---|---|
| C01 | blk027 | exotic-and-path-dependent-options/01-from-zero-intuition.md | print **order** differs: page claims vanilla→BSM→lookback; code prints vanilla→lookback→BSM. All three values identical (4.4295 / 4.4197 / 8.7952). |
| C02 | blk039 | interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates.md | formatting only: `T=1` vs `T=1.0`, `err=1.4e-11` vs `1.3e-11` (floating-point print), one extra blank line. All values identical. |
| C03 | blk043 | interest-rate-and-term-structure/06-advanced-extensions.md | page's claimed block omits the code's final explanatory line `(rho=-0.3 -> downward ATM skew; nu=0.5 -> curvature -> smile)` and blank-line grouping. All vol values identical. |

None affects a computed number. Recommend syncing the displayed output blocks to actual
execution for cosmetic cleanliness; no mathematical impact.

### Heavy blocks (not a failure)

Three folder blocks are pure-Python and exceed a 20 s budget (Heston quadrature + Newton iv
root-find in `advanced-volatility-heston-sabr/05`, CIR/Vasicek MC in
`interest-rate-and-term-structure/03`, PSOR American FD in `numerical-methods/06`). Given
~280 s they all complete **rc=0 and MATCH** their claimed output. No bug.

---

## Part 3 — Corpus-flagged caveats: were they handled correctly?

| Caveat (corpus) | Handling in Pillar 3 | Verdict |
|---|---|---|
| **Gatheral (3.18)** ATM term-structure limit returns `v̄` (long-run mean), not `v₀` | advanced-volatility-heston-sabr/02 (§4 caveat), /index (explicit "Critical caveat"), /04 — page states the literal T→0 limit is `v̄` not `v₀`, physical limit is `v₀`, and quotes both (13.191% vs 0.0354). | **Handled correctly** |
| **Duffy (6.10)** printed `h⁴/4!`, correct `h²/4!` | numerical-methods/01 — "Duffy's printed second-derivative error term carries a typographical h⁴ (eq. 6.10) — the Taylor expansion and the stated O(h²) force h²." | **Handled correctly** |
| **Duffy (8.34)/(8.35)** printed `4λ²`, correct `4λ` | numerical-methods/02 — text explicitly says "Duffy's printed symbols (8.34)–(8.35) show 4λ²; the surrounding algebra and the printed condition λ≤½ both force a single λ — a typographical error corrected above." Uses the correct `1−4λsin²(βh/2)`. | **Handled correctly** |
| **Björk Ch29** forward-vs-futures correction (futures = E^Q[Y] always; forward = E^{Q^T}[Y] only ≈ E^Q when r deterministic) | interest-rate-and-term-structure/04 and /index — stated correctly and labelled "(Björk Ch29 correction)". | **Handled correctly** |
| **haug_lookup-2** reconstructed/`[T]` formulas | Barrier/binary blocks (§4.17, §4.19) are the `[V-8]` fully-verified block; content reproduces it verbatim and the barrier code matches Haug Table 4-13. Compound/chooser page notes the source ambiguity and uses the verified decomposition. | **Handled correctly** |
| **Haug (1.18)** generalized put-call parity | **NOT flagged** — the corpus transcription itself is defective (missing `e^{−rT}`), and the pillar propagated it to 2 pages (see F01). | **Error propagated** |

---

## Artifacts

- Extraction/run scripts: `/tmp/extract_p3.py`, `/tmp/run_p3.py`, `/tmp/run_slow.py`,
  `/tmp/run_missing.py`, `/tmp/tally.py`, `/tmp/cmp_slow.py`
- Raw block + report JSON: `/tmp/p3_blocks/blocks.json`, `report.json`, `report_slow.json`
- Extracted block sources: `/tmp/p3_blocks/blk_000.py` … `blk_072.py`

## Recommendations

1. **Fix F01** in `black-scholes-merton/03-the-pricing-formulas.md` (line 41) and
   `black-scholes-merton/index.md` (line 38): use `c−p = e^{−rT}(Se^{bT}−X)`. Also correct
   `corpus/verified/haug_lookup-1.md` eq (1.18).
2. Optionally sync the three cosmetic output blocks (C01–C03) to actual execution output.
