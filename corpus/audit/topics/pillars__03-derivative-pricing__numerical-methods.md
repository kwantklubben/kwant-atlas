# Audit — `pillars/03-derivative-pricing/numerical-methods/`

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages). FDM (explicit/implicit/CN/θ-method, von Neumann, PSOR, penalty), Monte Carlo (estimator, Euler/Milstein, discretisation, Brownian bridge, variance reduction, QMC).
**Corpus cross-check:** `corpus/verified/duffy_ch1-7.md` (θ-method 7.4/7.7, Richardson 6.36, von Neumann 8.34–8.39), `duffy_ch8-12.md` (Lax 8.2, explicit BS bounds 12.15–12.18, ADI 19.x, penalty 28.x, PSOR 29.11), `glasserman_ch1-3.md`, `glasserman_ch4-6.md`, `glasserman_ch7-9.md` (estimator, VAR, LSM/duality), `haug_lookup-*`.
**Method:** (1) spelling/typo scan; (2) every boxed formula & worked example re-derived / re-run independently; (3) all 9 ```python blocks executed and diffed against their output fences; (4) hub↔sub-page coherence, link resolution, cross-page numeric consistency.

---

## VERDICT: **PASS WITH MINOR CORRECTIONS** — no broken formula and no broken code

**9/9 code blocks reproduce their fences character-for-character.** All boxed formulas (FDM schemes, von Neumann symbols, divided differences, estimator, MSE budget, control-variate, antithetic, stratified/LHS, importance-sampling, penalty, PSOR, LSM, ADI, Koksma–Hlawka, Brownian bridge/interpolation) are **correct**. The defects are one mislabelled θ-convention (operative formula/table are right) and a handful of narrative numerics/citations.

---

## Summary of findings

| # | Severity | File:line | Type | Stated | Correct |
|---|----------|-----------|------|--------|---------|
| 1 | **MEDIUM** | `index.md:40`, `02-finite-difference-methods.md:19` | MATH (convention label) | θ ∈ [0,1] is "the weight on the **new** time level", with θ=1 explicit / θ=0 implicit | In the displayed formula `(U^{n+1}−U^n)/k = (1−θ)𝓛U^{n+1} + θ𝓛U^n` the **new** level carries **(1−θ)**; θ is the weight on the **old** level (Duffy 7.4). The formula and the θ=1/0/½ table are correct; only the gloss is inverted. |
| 2 | **MEDIUM** | `05-failure-modes-and-practice.md:234` | MATH (numeric) | Euler −0.2430 one-step bias "is **23×** the Monte Carlo standard error" | se of the 1-step Euler estimator at n=2×10⁵ is ≈0.028 (per-path sd ≈12.7), so bias ≈**8.6×** (≈7.4× if σ_f=14.7 of page 03 is used). 23× is not reproducible from this page's own setup. |
| 3 | **MINOR** | `06-advanced-extensions.md:352` | MATH (numeric / narrative) | antithetic device "at **forty** times the path count" | 04 used 40 000 paths, 06's QMC uses 2 000 points → **20×**, not 40×. ("three times more" is also loose: the VR ratio is 31.4/4.41 ≈ 7×.) |
| 4 | **MINOR** | `03-monte-carlo-pricing.md:62` | Cross-ref | "the discretisation-aware case is **page 06's** s^{−β/(2β+1)}" | That formula lives on **page 04 (§2, efficiency rule)** and **page 05:47**, not page 06. |
| 5 | **MINOR** | `02-finite-difference-methods.md:139` | CODE comment | `# ... refine h and k together (M=nt=50,100,200)` | The loop below uses **M=nt = 100,200,400** (nt = 4000/8000/16000). Stale comment; output is correct. |
| 6 | **MINOR** | `index.md:62`, `03-monte-carlo-pricing.md:19` | Notation | `α̂−α ≈ 𝓝(0, σ_f/√n)` | Second argument of 𝓝 is the **variance**: should be 𝓝(0, σ_f²/n) (σ_f/√n is the s.d.). Common shorthand, but inconsistent with page 04's own variance-vs-sqrt discipline. |

---

## FINDING 1 — MEDIUM · θ mislabelled as the weight on the *new* time level

**Files/lines:** `index.md:40` ("…and $\theta$ as the weight on the **new** time level") and `02-finite-difference-methods.md:19` ("The $O(k)$ parameter is $\theta\in[0,1]$ (weight on the **new** time level)").

**Problem.** Both pages display

$$\frac{U^{n+1}-U^n}{k}=(1-\theta)\,\mathcal L U^{n+1}+\theta\,\mathcal L U^{n},\qquad \theta\in[0,1],$$

and then tabulate **θ=1 ⇒ explicit, θ=0 ⇒ implicit, θ=½ ⇒ CN**. The θ parameter multiplies $\mathcal L U^{n}$ (the **old** level); the new level carries $(1-\theta)$. The accompanying prose says the opposite. This is exactly Duffy's Ch-7 convention, which `corpus/verified/duffy_ch1-7.md` records twice (eq. 7.4 `(U^{n+1}−U^n)/k = θA U^n + (1−θ)A U^{n+1}`, θ=1 explicit, θ=0 implicit; and the explicit warning "*in (7.4) the old level carries weight θ*", lines 605/610/850).

**Evidence the page's own code agrees with "old level":** `02-finite-difference-methods.md:109` writes `w = 1.0 - theta   # weight on the new time level`, i.e. the **code** correctly identifies (1−θ) as the new-level weight — contradicting the prose eleven lines earlier. Same inversion in the hub.

**Not an error in the formula or table** — those are standard and correct; only the verbal gloss is wrong. **Fix:** change both parentheticals to "(θ = weight on the **old** time level; the new level carries 1−θ)" — or state simply "θ=1 explicit, θ=0 implicit".

---

## FINDING 2 — MEDIUM · "23× the Monte Carlo standard error" not reproducible

**File/line:** `05-failure-modes-and-practice.md:234`.

**Stated:** "Euler's −0.2430 bias at one step is $23\times$ the Monte Carlo standard error, so no path count removes it."

**Check.** The estimator is `euro_call_mc(200000, 1, s)` — one Euler step, n = 2×10⁵. Re-running the page's own routine: per-path s.d. of the discounted Euler payoff ≈ **12.69**, so the standard error is $12.69/\sqrt{2\times10^5}\approx 0.0284$; bias/se ≈ **8.6×**. Using page 03's σ_f = 14.71 instead gives $0.243/0.0329\approx 7.4\times$. To make the claim true you would need ≈ 1.4–1.9×10⁶ paths, not 2×10⁵. On the same page, the text's own "±0.02 Monte Carlo noise" would give ≈12×, not 23×.

**The qualitative point stands** (the −0.2430 bias dwarfs the sampling error, so more paths cannot fix it) — only the multiplier is wrong. **Fix:** replace "23×" with "≈9×" (or "≈8×").

---

## FINDING 3 — MINOR · "forty times the path count" is twenty

**File/line:** `06-advanced-extensions.md:352`.

**Stated:** QMC's 31.4× variance reduction is "three times more than the antithetic device of page 04 achieved at forty times the path count."

**Check.** Page 04's antithetic estimator used `N_TOT = 40000` paths per replication (output: VR = 4.41×). Page 06's QMC uses `NPTS = 2000` points (output: 31.4×). Path ratio = 40000/2000 = **20×**, not 40×. The VR ratio is 31.4/4.41 ≈ 7×, so "three times more" is at best the RMSE interpretation (5.6/2.1 ≈ 2.7×). **Fix:** "…at twenty times the path count"; consider rephrasing the fold-change.

---

## FINDING 4 — MINOR · mis-attributed formula ("page 06's")

**File/line:** `03-monte-carlo-pricing.md:62`: "…the discretisation-aware case is page 06's $s^{-\beta/(2\beta+1)}$."

The budget/MSE-balancing result $\sqrt{\mathrm{MSE}}\propto s^{-\beta/(2\beta+1)}$, $\delta^*\propto s^{-1/(2\beta+1)}$ is boxed on **page 04** (`04-variance-reduction-and-efficiency.md:79`) and restated on **page 05:47**. Page 06 does not state it. **Fix:** change "page 06's" → "page 04's (and page 05's)".

---

## FINDING 5 — MINOR · stale code comment in block `02`

**File/line:** `02-finite-difference-methods.md:139`: `# observed convergence order: refine h and k together (M=nt=50,100,200)`.

The loop immediately below calls `pde_call(…,100,4000,…)`, `(…,200,8000,…)`, `(…,400,16000,…)` — i.e. **M = 100,200,400**. The comment's "50,100,200" is leftover from a different run. Output is unaffected. **Fix:** correct the comment to "M=100,200,400".

---

## FINDING 6 — MINOR · normal-approximation notation

**Files/lines:** `index.md:62` and `03-monte-carlo-pricing.md:19`: $\hat\alpha_n-\alpha\approx\mathcal N\!\big(0,\tfrac{\sigma_f}{\sqrt n}\big)$.

The second parameter of $\mathcal N(\cdot,\cdot)$ is the **variance**; the sampling variance is $\sigma_f^2/n$ (the $1/\sqrt n$ is the standard deviation). Page 04 is careful to distinguish $\mathrm{Var}[Y_i(b)]$ from $b^*$ etc., so this is an internal inconsistency as well as a notational slip. **Fix:** write $\mathcal N(0,\sigma_f^2/n)$.

---

## Verified-correct items (no action)

### Formulas / boxed math — ALL CORRECT
- **θ-method family** `index:42`, `02:21` `(U^{n+1}−U^n)/k=(1−θ)𝓛U^{n+1}+θ𝓛U^n`, θ∈[0,1] — matches **Duffy 7.4** exactly (see Finding 1 for the label only).
- **von Neumann symbols** `index:54-56`, `02:47-51`, `05:33`: explicit $1−4λ\sin^2(ξ/2)$; implicit $1/(1+4λ\sin^2(ξ/2))$; CN $(1−2λ\sin^2)/(1+2λ\sin^2)$. Match Duffy (8.34)–(8.39).
- **"typographical 4λ²" claim** `index:52`, `02:53` — **honest and corpus-verified**: `duffy_ch1-7.md` lines 780/847 record the glyph-level `4λ²` on pp. 116–117 (eqs. 8.34/8.35) with the single-λ correction. Likewise the (6.10) `h⁴` typo claim `01:56`, `02:56` matches corpus line 846.
- **Lax equivalence triangle** `index:58`, `02:30` (consistency + stability ⇔ convergence; order (p,q)). Correct.
- **Divided differences** `01:52-54` (centred O(h²), one-sided O(h), second difference O(h²)). Correct.
- **BSM PDE** `01:40` and **exact GBM transition** `01:46`, `03:26,41`. Correct.
- **BS explicit bounds** `02:61`, `05:43`: $h\le 2σ/|μ|$, $k\le1/(2σ/h²−b)$, and BS $h\le σ^2S_j/r$, $k\le1/(σ^2j^2+r)$ — verbatim **Duffy 12.15–12.18** (corpus line 58). The hub's $k\le h^2/(σ^2S_{\max}^2)$ is their large-j limit — consistent.
- **Convection–diffusion explicit condition** `02:57`: $R^2/2\leλ\le\tfrac12$ (corpus line 823 / Duffy 8.2). Correct.
- **Il'in fitting factor** `02:65`: $\tildeσ_j=\frac{μ_jh}{2}\coth\frac{μ_jh}{2σ_j}$. Correct.
- **Call boundary conditions** `02:71`, `05:52`, `01:153`, `index:74`. Correct (and the $x=S/(S+K)$ BC-free transform is correctly attributed to Duffy Ch 4/30).
- **Estimator + CLT + pricing identity** `03:19,35`; risk-neutral drift / volatility invariance `03:37`. Correct apart from Finding 6.
- **Brownian bridge** `03:47` (mean and variance $(s−u)(t−s)/(t−u)$) — the empirical check `03:163-165` reproduces $s(t−s)/t=0.25$ to 3 dp.
- **MSE budget** `03:59-60`, `04:77-81`, `05:47`: bias² $O(δ^{2β})$, variance $O(1/n)$, $\mathrm{RMSE}=O(s^{−β/(2β+η)})$, $\delta^*\propto s^{−1/(2β+1)}$, β=1 ⇒ $s^{−1/3}$ vs $s^{−1/2}$. All correct.
- **Control variate** `04:40-46`: variance $σ_Y^2−2bσ_Xσ_Yρ+b^2σ_X^2$, $b^*=ρσ_Y/σ_X$, ratio $1−ρ^2$. Correct.
- **Antithetic** `04:50-51`: $\mathrm{Var}[(Y+\tilde Y)/2]=\frac{σ_Y^2}{2}(1+ρ_{Y\tilde Y})$ — verified by expansion. Correct.
- **Stratified / Neyman / LHS** `04:57-65`. Correct.
- **Importance sampling** `04:69-75`: LR $f/g$; exponential tilt LR $e^{−θΣX_i+nψ(θ)}$; Gaussian drift-tilt LR $e^{−μ'Z+\frac12 μ'μ}$. Correct (and the code's `exp(-tilt*Z+0.5*tilt*tilt)` matches).
- **Richardson / extrapolated implicit Euler** `05:37`: $V(t+k)=2U^{(2)}_{k/2}−U^{(1)}_k$, $U^{(1)}=(I+kA)^{−1}V$, $U^{(2)}=(I+\frac k2A)^{−2}V$ — **verbatim Duffy (6.36)** (corpus lines 525-540).
- **Brownian-interpolation max & survival prob.** `05:49-50`. Correct (Glasserman §6.4/6.51 form).
- **American complementarity / smooth pasting / penalty** `06:29-38`: matches corpus (Duffy 26.x, 28.15–28.17, 28.32, Thm 28.3 $k\leε/(rK)$).
- **PSOR update** `06:42-43` (Duffy 29.11), **LSM & duality** `06:49-54` (Glasserman 8.46–8.52, 8.58/8.65, T-vR high-biased / LSM low-biased — correctly distinguished).
- **PEACEMAN–Rachford ADI legs** `06:60-61`; PR two-leg unconditionally stable / 3-leg 3-D not / mixed-derivative breakdown / Yanenko — all match corpus (Duffy 19.5–19.7, 19.34, 19.37, 20.8–20.9).
- **Koksma–Hlawka** `06:69-72` (Glasserman 5.10) and the unbiasedness-by-randomisation / plateau caveat. Correct.

### Worked examples — ALL numerical claims verified except Findings 2 & 3
- `index:143-147`: exact 10.4506; binomial n=200 err −0.0100; CN M=nt=200 err −0.0099 ✅
- `01:132-141,144`: full convergence table and the stated error sequences (0.0399→0.0100→0.0020 tree; 0.0398→0.0099→0.0025 CN) ✅
- `02:183-206`: combined orders (2.00/1.98, 2.01/2.00), time orders (implicit 1.01, CN 2.00), explicit blow-up −1.96×10⁷, heat λ=0.5 boundary value 4.965e-05, λ=0.6 → −5.2×10⁷⁷ ✅
- `03:154-171`: RMSE ≈σ_f n^{−1/2} (RMSE·√n flat 14–15.6), one-batch se 0.0465, bridge variance 0.250401, geometric-Asian MC 5.6471 vs closed 5.6374, arithmetic 5.8640 (AM≥GM) ✅ — the geometric closed-form routine was independently re-derived against the textbook Kemna–Vorst formula and agrees (m=8→6.1377, m=12→5.9402, m=52→5.6374).
- `04:204-225`: antithetic 4.41×; European CV 6.80× = 1/(1−0.9235²) ✅; Asian CV 1256.7× at ρ=0.99960; deep-OTM digital IS 0.0435%, RMSE ratio ≈915 ✅
- `05:191-224`: 32.4× gamma inflation (0.70717/0.02182), 5.87× at Δt=0.0625, explicit k_max=2.50e-03, Euler bias sequence, S_max=120 → −0.2157 ✅ (only the "23×" of Finding 2 fails)
- `06:183-189,268-279,345-349`: PSOR upward convergence to CRR 4.6921, LSM 4.6765 (below benchmark, as required), premium 0.2271 vs 0.2427; ADI 0.139038 vs exact 0.138911; QMC 31.4× — all ✅ except the "forty times" of Finding 3.

### Code blocks — execution & fence diff
**9 blocks** (index 1, 01 1, 02 1, 03 1, 04 1, 05 1, 06 3) extracted and executed in Python 3.14. **9/9 output fences match execution character-for-character** (whitespace-trimmed). Block logic was also read for hidden bugs (as in the BSM audit's Poisson-sampler case): none found — CRR/CN/θ-solver, Thomas, Euler-Maruyama, log-Euler, Brownian bridge, CV/IS estimators, PSOR, LSM, PR-ADI and Halton/invnorm are all correctly implemented.

### Coherence, links, spelling
- Structure: exactly `index.md` + `01`–`06`; no stragglers. Prerequisite chain self-consistent (hub declares stochastic-calculus + calculus for 02–06; 01 self-declares the BSM hub; sub-pages chain 01→02→03→04→05→06).
- **All 55 wikilinks resolve** to existing files (hub↔sub-pages, `black-scholes-merton/*`, `foundations/*`, `no-arbitrage-and-binomial`, `advanced-volatility-heston-sabr`, `interest-rate-and-term-structure`, `volatility-surfaces-and-smiles`). No broken links.
- Cross-page numbers agree (e.g. σ_f=14.71 shared between 01:135 and 03:161; tree benchmark 4.6921 shared between 05:246 and 06:174).
- **Spelling/typos:** none found. All non-dictionary tokens are legitimate hyphenated compounds or British spellings (discretis*, centred, neighbour, regularisation, modelling, unrandomised).

---

## Files checked (7)
1. `index.md`
2. `01-from-zero.md`
3. `02-finite-difference-methods.md`
4. `03-monte-carlo-pricing.md`
5. `04-variance-reduction-and-efficiency.md`
6. `05-failure-modes-and-practice.md`
7. `06-advanced-extensions.md`

**Blocks run:** 9 · **Errors found:** 6 (2 substantive: θ-label convention, "23×"; 4 minor)
