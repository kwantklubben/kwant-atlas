# Shreve I — Chapters 9–13 (combined lecture edition): Math-Verified Deep-Read

> **Source:** `.../10scfi/Stochastic Calculus for Finance I The Binomial Asset Pricing Model.pdf`
> (combined lecture edition; the PDF on disk, extracted via `pdftotext` to `shreve1.txt`,
> and rendered as PNGs `p-001.png` … `p-349.png`).
> **Verification:** each formula below was checked against the rendered PNG pages and the
> `pdftotext` layer. Numeric worked examples were re-computed by hand and all check out.
> **Assigned range for this sub-task:** PDF pages **p-115 … p-151**.

## ⚠ CRITICAL FLAG — assigned chapter titles do not match the page content

The task brief labels these pages "Ch 9–12 (Information and Conditioning; Brownian Motion;
The Ito Integral; The Ito-Doeblin Formula)". **That mapping is wrong for this combined-edition PDF.**
Ground truth, established by vision-reading the rendered pages (printed page = PDF page − 2):

| PDF pages | Printed | Actual chapter in the combined edition |
|---|---|---|
| p-115…p-120 | 113–118 | **Ch 9. Pricing in terms of Market Probabilities: The Radon–Nikodym Theorem** |
| p-121…p-124 | 119–122 | **Ch 10. Capital Asset Pricing** |
| p-125…p-132 | 123–130 | **Ch 11. General Random Variables** |
| p-133…p-140 | 131–138 | **Ch 12. Semi-Continuous Models** |
| p-141…p-151 | 139–149 | **Ch 13. Brownian Motion** (first-passage/reflection continues onto p-152+) |

Consequences for the extraction:
- **"Information and Conditioning"** is a **Vol II** chapter title; it does **not** appear as a titled
  chapter anywhere in this combined Vol I PDF. It must not be sourced from these pages.
- **"The Ito Integral"** and **"The Ito–Doeblin Formula"** are **Ch 14** (p-155…) and **Ch 15**
  (p-169…) of this same PDF — they lie *outside* the assigned page range (p-115…p-151).
  The Ito material appears only as the Vol II Ch 4 entry in `shreve.md`.
- Within the assigned range, Brownian motion is covered as **Ch 13** (this is the discrete→continuous
  introduction: random walks → LLN/CLT → limit → definition → covariance → Markov → first passage).
  The full continuous BM treatment with quadratic variation, transition-density first-passage-Laplace
  transforms, reflection-principle joint densities, and GBM volatility lives in Vol II Ch 3 (`shreve.md`).

The verified deep-read below therefore covers the **actual** chapters found on the assigned pages.
Existing `shreve.md` entries cross-referenced: Vol I Ch 9, Ch 10, Ch 11 (all present, mostly correct —
one real error found in Ch 10, fixed below), plus the Ch 13 / BM material (covered in `shreve.md` only
via its Vol II Ch 3 entry).

---

## Ch 9. Pricing in terms of Market Probabilities: The Radon–Nikodym Theorem (p-113…p-120)

### Verified content
- **Radon–Nikodym theorem:** if P̃ ≪ P (P̃ absolutely continuous w.r.t. P), there is a nonnegative
  RV Z with `P̃(A) = ∫_A Z dP` for all `A ∈ F`. `Z` is the RN derivative. From this:
  `ẼX = E[XZ]` whenever `E|XZ| < ∞`. Equivalence iff `P(A)=0 ⇔ P̃(A)=0`; then `1/Z` is the RN
  derivative of P w.r.t. P̃, and `E Y = Ẽ[Y/Z]`. ✅ (p-113)
- **Example 9.1 (checked numerically):** 2-toss space, market `p=1/3, q=2/3`, risk-neutral
  `p̃=q̃=1/2`. `Z(ω)=P̃(ω)/P(ω)` gives `Z(HH)=9/4, Z(HT)=Z(TH)=9/8, Z(TT)=9/16`. Verified:
  P(HH)=1/9, P̃(HH)=1/4 ⇒ Z=9/4 ✓; P(HT)=2/9, P̃=1/4 ⇒ Z=9/8 ✓; P(TT)=4/9 ⇒ Z=9/16 ✓. (p-114)
- **Radon–Nikodym martingale:** `Z_k = E[Z|F_k]`, `k=0..n`, is a P-martingale
  (`E[Z_{k+1}|F_k]=E[Z|F_k]=Z_k`). (p-114)
- **Lemma 2.28:** if X is `F_k`-measurable then `ẼX = E[X Z_k]`. (p-114)
- **Lemma 2.29 (change of conditional expectation):** if X is `F_k`-measurable and `0≤j≤k`, then
  `Ẽ[X|F_j] = (1/Z_j)·E[X Z_k | F_j]`. Proof via partial averaging; the figure 9.1 tree
  (Z₂(HH)=9/4, Z₁(H)=3/2, Z₁(T)=3/4, etc.) is consistent with Z₀=E Z=1. ✅ (p-115, vision-verified)
- **State price density (constant r):** `ζ_k = (1+r)^{-k} Z_k`, `k=0..n`. (p-115)
- **European derivative, payoff C_k at time k:**
  `V_0 = Ẽ[(1+r)^{-k}C_k] = E[ζ_k C_k]`; and for `0≤j≤k`:
  `V_j = (1+r)^j Ẽ[(1+r)^{-k}C_k|F_j] = ζ_j^{-1} E[ζ_k C_k | F_j]`. (p-116)
  Remark 9.3: `{ζ_j V_j}` is a P-martingale. ✅ (p-116)
- **American derivative `{G_k}`:**
  `V_0 = sup_{τ∈T_0} Ẽ[(1+r)^{-τ}G_τ] = sup_{τ∈T_0} E[ζ_τ G_τ]`;
  `V_j = ζ_j^{-1} sup_{τ∈T_j} E[ζ_τ G_τ | F_j]`. (p-116)
  Remark 9.4: `(a) {ζ_j V_j}` is a **P-supermartingale**; `(b) ζ_j V_j ≥ ζ_j G_j` ∀j;
  `(c) {ζ_j V_j}` is the *smallest* process with (a)+(b). (p-116/117)
  Interpretation: `ζ_k(ω)P(ω)` = time-0 value of a claim paying $1 at time k on path ω. (p-117)
- **Example 9.3 (European call, strike 5, expiry 2; r=1/4, u=2, d=1/2, S₀=4) — checked numerically:**
  ζ₀=1.00, ζ₁(H)=1.20, ζ₁(T)=0.60, ζ₂(HH)=1.44, ζ₂(HT)=ζ₂(TH)=0.72, ζ₂(TT)=0.36.
  Verified: ζ_k=(4/5)^k Z_k ⇒ ζ₁(H)=(4/5)(3/2)=1.20 ✓, ζ₂(HH)=(16/25)(9/4)=1.44 ✓,
  ζ₂(TT)=(16/25)(9/16)=0.36 ✓. Call: V₂(HH)=16−5=11; V₀=Σ_ω P(ω)ζ₂(ω)C₂(ω)=(1/9)(1.44)(11)=1.76 ✓
  (only path HH pays). Risk-neutral check: 1/(1+r)=4/5 ⇒ V₁(H)=(p̃·(4/5))·11=(1/2)(4/5)(11)=4.40 ✓,
  V₀=(1/2)(4/5)V₁(H)=(2/5)(4.4)=1.76 ✓. (p-117)
- **Example 9.3 (American put, strike 5) — checked numerically:** stopping rule (1)
  `τ(HH)=τ(HT)=2, τ(TH)=τ(TT)=1` gives value Σ P ζ_τ G_τ = (2/9)(0.72)(1) [HT] + (2/9)(1.8) [TH]
  + (4/9)(1.8) [TT] = 0.16+0.40+0.80 = **1.36**. Rule (2) stop at 2: (2/9)(0.72)(1)+ (2/9)(0.72)(1)
  + (4/9)(0.36)(4) = 0.16+0.16+0.64 = **0.96**. So rule (1) is optimal (value 1.36). ✅ (p-117/118)
- **Stochastic volatility binomial (§9.4):** `0<d_k<1+r_k<u_k` all `F_k`-measurable;
  `p̃_k=(1+r_k−d_k)/(u_k−d_k)`, `q̃_k=(u_k−1−r_k)/(u_k−d_k)`. Money market `M₀=1`,
  `M_k=(1+r_{k−1})M_{k−1}` (M_k is `F_{k−1}`-measurable). State price `ζ_k=(1/M_k)Z_k`.
  Wealth `X_{k+1}=Δ_k S_{k+1}+(1+r_k)(X_k−Δ_k S_k)`. **Martingales:** under P̃: `{S_k/M_k}`,
  `{X_k/M_k}`; under P: `{ζ_k S_k}`, `{ζ_k X_k}`. (p-118/119; **vision-verified p-119**)
  Pricing: `V_j = M_j Ẽ[C_k/M_k|F_j] = ζ_j^{-1} E[ζ_k C_k|F_j]`;
  American `V_j = M_j sup_{τ∈T_j} Ẽ[G_τ/M_τ|F_j] = ζ_j^{-1} sup_{τ∈T_j} E[ζ_τ G_τ|F_j]`. (p-119)
- **§9.5:** existence of conditional expectations follows from the RN theorem: given sub-σ-algebra G,
  X≥0 with ∫XdQ=1, define `P̃(A)=∫_A X dQ` on G; the RN derivative `Z=dP̃/dP|_G` is G-measurable and
  has the partial-averaging property, so `Z = E[X|G]` under Q. ✅ (p-120)

### Corrections to existing `shreve.md` (Ch 9)
- `shreve.md` writes "`Ẽ[X|F_j] = (1/Z_j) E[X Z_k |F_j]`" — **correct** (Lemma 2.29). No change.
- `shreve.md` writes "`V_j = (1/ζ_j)E[ζ_k C_k|F_j]`" and "`ζ_j V_j ≥ ζ_j G_j`" — both **correct**. No change.
- Minor: `shreve.md` called §9.5 "Another Applicaton [sic]" and used the term "state price density" for
  ζ in the general-vol case; fine. No math errors found in Ch 9.

---

## Ch 10. Capital Asset Pricing (p-121…p-124)

### Verified content
- **Problem:** agent with initial wealth X₀ maximizes `E log X_n` over portfolios.
  Since `{ζ_k X_k}` is a P-martingale, the **budget constraint** `E[ζ_n X_n] = X₀` holds (Remark 10.1).
  Conversely (Remark 10.2) any RV ξ with `E[ζ_n ξ]=X₀` is attainable (treat as a simple European claim
  with value X₀, hedge to reproduce). ⇒ reduces to a **constrained optimization**:
  maximize `E log ξ` s.t. `E[ζ_n ξ]=X₀`. (p-121)
- **Lagrange multiplier theorem (Theorem 1.30):** at optimum, `∂f/∂x_k = λ ∂g/∂x_k`, `g=0`.
  Applying: `1/x_k = λ ζ_n(ω_k)`, i.e. `x_k^* = 1/(λ ζ_n(ω_k))`, and the constraint forces
  `λ = 1/X₀`, so `ξ* = X₀/ζ_n`. (p-122; verified algebra)
- **Theorem 1.31 (verification):** for fixed Z>0, `f(x)=log x − xZ` is maximized at `x=1/Z`
  (f'=1/x−Z=0, f''=−1/x²<0), giving `log x − xZ ≤ log(1/Z)−1`. Take Z=ζ_n/X₀ and expectations:
  `E log ξ − (1/X₀)E[ζ_n ξ] ≤ E log ξ* − 1`; using the budget constraint `E[ζ_n ξ]=X₀` gives
  `E log ξ ≤ E log ξ*`. ✅ (p-123)
- **Summary:** optimal terminal wealth `X_n = X₀/ζ_n`, so `ζ_n X_n = X₀`; by the martingale property
  `ζ_k X_k = E[ζ_n X_n|F_k] = X₀`, hence **`X_k = X₀/ζ_k` for all k**. (p-124)
- **Optimal hedge — ⚠ correction to `shreve.md`:** the optimal portfolio is
  `Δ_k(ω) = [ X₀/ζ_{k+1}(H) − X₀/ζ_{k+1}(T) ] / [ S_{k+1}(H) − S_{k+1}(T) ]`
  — the **difference of reciprocals** `X₀/ζ_{k+1}`, because `X_{k+1}=X₀/ζ_{k+1}`.
  (p-124; **vision-verified**.) The existing `shreve.md` writes
  `Δ_k=(ζ_{k+1}(·,H)−ζ_{k+1}(·,T))/(S_{k+1}(·,H)−S_{k+1}(·,T))·X₀` — **this drops the reciprocal
  and is WRONG.** Fix: `Δ_k = X₀·(1/ζ_{k+1}(H) − 1/ζ_{k+1}(T))/(S_{k+1}(H)−S_{k+1}(T))`.

---

## Ch 11. General Random Variables (p-125…p-132)

### Verified content
- **Random variable:** `X:Ω→IR` is a RV iff `X^{-1}(B)∈F` for every Borel `B∈B(IR)`. Induces the
  **law** `μ_X(B) = P{X^{-1}(B)} = P{X∈B}`, a measure on `(IR, B(IR))` (Williams' `L_X`). (p-125)
- **Density:** `f_X:IR→[0,∞)` with `μ_X(B)=∫_B f_X dx`; `dμ_X(x)=f_X(x)dx`; `f_X` is the RN
  derivative of `μ_X` w.r.t. Lebesgue measure; X has a density iff `μ_X ≪ Leb` (B of measure zero ⇒
  `P{X∈B}=0`). (p-125/126)
- **Expectation (Theorem 3.32):** `E h(X) = ∫h(X)dP = ∫_{IR}h(x)dμ_X(x) = ∫_{IR}h(x)f_X(x)dx`
  (by the standard machine, starting from h=1_B). ✅ (p-126)
- **Two RVs:** joint law `μ_{X,Y}(C)=P{(X,Y)∈C}`, `C∈B(IR²)`; joint density `f_{X,Y}:IR²→[0,∞)`;
  `E k(X,Y)=∫∫k(x,y)f_{X,Y}(x,y)dxdy`. (p-127)
- **Marginal density:** `f_Y(y)=∫_{IR}f_{X,Y}(x,y)dx`; then `μ_Y(B)=∫_B f_Y dy`. ✅ (p-128)
- **Conditional expectation via densities:** `E[h(X)|Y]=g(Y)` with
  `g(y)=∫h(x)f_{X|Y}(x|y)dx`, where **conditional density** `f_{X|Y}(x|y)=f_{X,Y}(x,y)/f_Y(y)`
  (Theorem 7.33; verified by the partial-averaging identity `∫_B∫h(x)f_{X|Y}f_Y dxdy
  = ∫_B∫h(x)f_{X,Y}dxdy`). Notation `E[h(X)|Y=y]=g(y)`. (p-128/129)
- **Bivariate normal (Example 11.1):** `(X,Y)` joint density with σ₁,σ₂>0, −1<ρ<1. Verified:
  marginal `Y ~ N(0, σ₂²)`; conditional `X|Y=y ~ N(ρ(σ₁/σ₂)y, (1−ρ²)σ₁²)`; so
  `E[X|Y] = ρ(σ₁/σ₂)Y` and `E[(X−ρ(σ₁/σ₂)Y)²] = (1−ρ²)σ₁²`. Best linear/square-error estimator of X
  based on Y is `ρ(σ₁/σ₂)Y` (unbiased, minimal expected square error; no other Y-based estimator beats
  it). ✅ (p-129/130/131)
- **Multivariate normal (§11.8):** column vectors; `f_X(x) = (det A)^{1/2}/(2π)^{n/2}
  exp{−½(x−μ)^T A (x−μ)}`, where `μ=E X` and `A^{-1}=E[(X−μ)(X−μ)^T]` is the covariance matrix
  ((i,j) element `E[(X_i−μ_i)(X_j−μ_j)]`). Components independent **iff** `A^{-1}` is diagonal,
  `A^{-1}=diag(σ₁²,…,σ_n²)`. (p-131; note: text points to Øksendal App. A for the proof.) ✅
- **Bivariate normal again (§11.9):** `A^{-1}=[[σ₁², ρσ₁σ₂],[ρσ₁σ₂, σ₂²]]` ⇒
  `A = (1/(1−ρ²))·[[1/σ₁², −ρ/(σ₁σ₂)],[−ρ/(σ₁σ₂), 1/σ₂²]]` and `det A = 1/(σ₁²σ₂²(1−ρ²))`,
  giving the displayed density with exponent `−(1/(2(1−ρ²)))[(x₁−μ₁)²/σ₁²
  − 2ρ(x₁−μ₁)(x₂−μ₂)/(σ₁σ₂) + (x₂−μ₂)²/σ₂²]`. ✅ (p-132)
- **MGF (§11.10):** for jointly normal X with covariance `A^{-1}` and mean μ,
  `E e^{u^T X} = exp{½ u^T A^{-1} u + u^T μ}`. Reading means/covariances off the MGF; independent
  jointly-normal iff `E e^{u^T X} = exp{Σ_j(½σ_j²u_j² + u_jμ_j)}`. ✅ (p-132)

### Corrections to existing `shreve.md` (Ch 11)
- All `shreve.md` Ch 11 formulas verified **correct**: law/density, `E h(X)`, conditional density
  ratio, bivariate-normal conditional mean/variance, multivariate-normal density, `A^{-1}`=covariance,
  independence⇔diagonal, and MGF. No errors found.

---

## Ch 12. Semi-Continuous Models (p-133…p-140) — **MISSING from `shreve.md` (gap)**

> This chapter is **absent** from the existing `shreve.md` (which jumps from Vol I Ch 11 to Vol II).
> It is a genuine chapter of the combined edition bridging the binomial and continuous models. It
> must be added.

### Verified content
- **Discrete-time Brownian motion (§12.1):** `Y_1,…,Y_n` iid standard normal under P;
  `B₀=0`, `B_k=Σ_{j=1}^k Y_j`. Filtration `F₀={∅,Ω}`, `F_k=σ(Y_1,…,Y_k)=σ(B_1,…,B_k)`.
  - **Theorem 1.34:** `{B_k}` is a **martingale** under P (`E[B_{k+1}|F_k]=E[Y_{k+1}]+B_k=B_k`). ✅ (p-133)
  - **Theorem 1.35:** `{B_k}` is **Markov**: `E[h(B_{k+1})|F_k]=g(B_k)` with
    `g(b)=∫h(y+b)(1/√(2π))e^{−y²/2}dy` (Independence Lemma). ✅ (p-134)
- **Stock price process (§12.2):** parameters `μ∈IR` (mean rate of return), `σ>0` (volatility),
  `S₀>0`. `S_k = S₀ exp{σB_k + (μ−½σ²)k}`; equivalently
  `S_{k+1} = S_k exp{σY_{k+1} + (μ−½σ²)}`. Verified:
  `E[S_{k+1}|F_k] = S_k e^{μ−½σ²}E[e^{σY}] = S_k e^{μ−½σ²}e^{½σ²} = e^μ S_k` ✅;
  `log(S_{k+1}/S_k) = σY_{k+1}+(μ−½σ²)` so mean `μ−½σ²`, variance `σ²`. (p-134/135)
- **Remainder of market (§12.3):** money market `M_k=e^{rk}` (so `M_{k+1}/M_k=e^r`);
  portfolio `Δ_0,…,Δ_{n−1}` each `F_k`-measurable; wealth
  `X_{k+1}=Δ_k S_{k+1}+e^r(X_k−Δ_k S_k)=Δ_k(S_{k+1}−e^r S_k)+e^r X_k`; discounted wealth
  `X_{k+1}/M_{k+1}=Δ_k(S_{k+1}/M_{k+1}−S_k/M_k)+X_k/M_k`. (p-135)
- **Risk-neutral measure (§12.4):** P̃ equivalent to P with `{S_k/M_k}` a P̃-martingale.
  **Theorem 4.36:** if P̃ is risk-neutral, every discounted wealth process `{X_k/M_k}` is a P̃-martingale
  (regardless of portfolio). ✅ (p-135/136)
- **Risk-neutral pricing (§12.5):** for an `F_n`-measurable payoff V_n (possibly path-dependent),
  `X₀=Ẽ[V_n/M_n]`; hedge a short position by starting with X₀ and a self-financing portfolio.
  **Remark 12.1:** hedging in this semi-continuous model is usually *impossible* (not enough trading
  dates) — this difficulty disappears in the fully continuous model. (p-136)
- **Arbitrage / FTAP-easy (§12.6):** an arbitrage is a portfolio with `X₀=0`, `P(X_n≥0)=1`,
  `P(X_n>0)>0` (P market measure). **Theorem 6.37 (FTAP, easy part):** existence of a risk-neutral
  measure ⇒ no arbitrage. Proof uses `Ẽ[X_n/M_n]=0` and equivalence of P, P̃. ✅ (p-136/137)
- **Market price of risk (§12.7, "Stalking the risk-neutral measure"):**
  `S_{k+1}/M_{k+1} = (S_k/M_k) exp{σY_{k+1} + (μ−r−½σ²)}`
  `= (S_k/M_k) exp{σ(Y_{k+1}+(μ−r)/σ) − ½σ²} = (S_k/M_k) exp{σỸ_{k+1} − ½σ²}`,
  where `Ỹ_{k+1}=Y_{k+1}+(μ−r)/σ` and **`Θ=(μ−r)/σ` is the market price of risk**. (p-137/138)
  Want P̃ under which `Ỹ_1,…,Ỹ_n` are iid standard normal ⇒ `Ẽ[S_{k+1}/M_{k+1}|F_k]
  = (S_k/M_k)e^{½σ²}e^{−½σ²} = S_k/M_k` ✓.
- **Cameron–Martin–Girsanov (§12.7):** `Z = exp{Σ_{j=1}^n(−ΘY_j − ½Θ²)}`
  `= exp{−ΘΣY_j − ½nΘ²}`. Verified `EZ=1`:
  `E exp{−ΘΣY_j}=e^{½nΘ²}` cancels `e^{−½nΘ²}` ✓; `Z≥0`; `P̃(A)=∫_A Z dP` is a probability measure
  (P̃(Ω)=EZ=1). **Verification that under P̃ the `Ỹ_j` are iid standard normal** (MGF):
  `Ẽ exp{Σu_jỸ_j} = E[exp{Σu_j(Y_j+Θ) − ΣΘY_j − ½nΘ²}]
  = exp{Σ(½(u_j−Θ)² + u_jΘ − ½Θ²)} = exp{½Σu_j²}` ⇒ standard normal, independent. ✅ (p-138/139)
- **Pricing a European call (§12.8):** `S_n = S₀ exp{σB_n + (μ−½σ²)n}
  = S₀ exp{σΣỸ_j + (r−½σ²)n}` (drift of μ cancels — verified algebra in text). Price of
  `(S_n−K)^+` at 0: `Ẽ[e^{−rn}(S_n−K)^+] = ∫(S₀ exp{σb+(r−½σ²)n}−K)^+ (1/√(2πn))e^{−b²/2n} db`
  (since `ΣỸ_j~N(0,n)` under P̃). **This is the Black–Scholes price; it does not depend on μ.** ✅ (p-140)

### New content for `shreve.md`
- Add a Ch 12 entry: semi-continuous models, discrete-time Brownian motion `B_k=ΣY_j` (martingale +
  Markov), `S_k=S₀ exp{σB_k+(μ−½σ²)k}` with `E[S_{k+1}|F_k]=e^μS_k`, risk-neutral measure, FTAP-easy,
  market price of risk `Θ=(μ−r)/σ`, Cameron–Martin–Girsanov `Z=exp{−ΘΣY_j−½nΘ²}`, Black–Scholes price
  independent of μ. This is the discrete bridge to Vol II Ch 3 (Brownian motion) and Ch 5 (Girsanov).

---

## Ch 13. Brownian Motion (p-141…p-151) — partial (through first-passage + reflection)

> This is the combined edition's **Ch 13**, the discrete→continuous introduction to Brownian motion.
> `shreve.md` currently covers BM only through its **Vol II Ch 3** entry; this Ch 13 material is the
> natural precursor and overlaps Vol II Ch 3. Add as its own entry (or merge into Vol II Ch 3).

### Verified content
- **Symmetric random walk (§13.1):** `X_j=+1` if `ω_j=H`, `−1` if `ω_j=T`; `M₀=0`,
  `M_k=Σ_{j=1}^k X_j`. (p-141)
- **LLN (§13.2, Theorem 2.38):** `M_k/k → 0` a.s. Proof by MGF:
  `φ_k(u)=E exp{(u/k)M_k}=(½e^{u/k}+½e^{−u/k})^k`; `log φ_k = k log(½e^{u/k}+½e^{−u/k})`; with
  `x=1/k`, L'Hôpital gives `lim log φ_k = lim_{x→0} (u(e^{ux}−e^{−ux})/2)/((e^{ux}+e^{−ux})/2) = 0`
  (limit MGF = e⁰ = that of constant 0). ✅ (p-141/142)
- **CLT (§13.3, Theorem 3.39):** `M_k/√k → N(0,1)` in distribution. MGF:
  `φ_k(u)=E exp{(u/√k)M_k}=(½e^{u/√k}+½e^{−u/√k})^k`; `log φ_k = k log(½e^{u/√k}+½e^{−u/√k})`;
  with `x=1/√k`, applying L'Hôpital twice yields `lim log φ_k = ½u²` ⇒ limit MGF `e^{½u²}`, the
  standard-normal MGF. ✅ (p-142/143)
- **BM as limit of random walks (§13.4):** `B^{(n)}(t)=(1/√n)M_{nt}` (linear interpolation between
  lattice points). For B^(100): `B^{(100)}(1)=M_{100}/10` mean 0 var 1; `B^{(100)}(2)=M_{200}/10`
  mean 0 var 2; increments `B(2)−B(1)` independent of `B(1)`; path continuous. Let `n→∞`. (p-143/144)
- **Definition of BM (§13.5):** `B(0)=0`; `B(t)` continuous in t; independent increments:
  for `0=t₀<t₁<…<t_n`, `Y_j=B(t_j)−B(t_{j−1})` are independent, `E Y_j=0`, `var Y_j=t_j−t_{j−1}`. (p-145)
- **Covariance (§13.6):** for `s≤t`, `E[B(s)B(t)]=E[B(s)(B(t)−B(s))]+E[B(s)²]=0+s=s`;
  hence `E[B(s)B(t)]=s∧t` for all `s,t≥0`. ✅ (p-145/146)
- **Finite-dimensional distributions (§13.7):** `(B(t₁),…,B(t_n))` jointly normal with covariance
  matrix `C_{ij}=t_i∧t_j` (e.g. `[[t₁,t₁,…,t₁],[t₁,t₂,…,t₂],…,[t₁,t₂,…,t_n]]`). ✅ (p-146)
- **Filtration (§13.8):** `{F(t)}` with `B(t)` F(t)-measurable and increments after t independent of
  F(t); constructed from `{B(s)∈C}, s∈[0,t], C∈B(IR)` closed under σ-algebra properties. (p-146)
- **Martingale (§13.9, Theorem 9.40):** `E[B(t)|F(s)]=B(s)` (uses independent increments). ✅ (p-147)
- **Exponential martingale (§13.9, Theorem 9.41):** for any `Θ∈IR`,
  `Z(t)=exp{−ΘB(t)−½Θ²t}` is a martingale
  (`E[Z(t)|F(s)]=Z(s)E exp{−Θ(B(t)−B(s))−½Θ²(t−s)}` = Z(s), using the MGF
  `E e^{−ΘΔB}=e^{½Θ²(t−s)}`). ✅ (p-147). *This is the martingale that seeds the CMG/change-of-measure
  in Ch 12 and Girsanov in Vol II Ch 5.*
- **Limit of a binomial model (§13.10):** n-th model with `u_n=1+σ/√n`, `d_n=1−σ/√n`, `r=0`,
  `p̃_n=q̃_n=1/2`. With `#_k(H)+#_k(T)=k`, `#_k(H)−#_k(T)=M_k`, so
  `#_k(H)=½(k+M_k)`, `#_k(T)=½(k−M_k)`. Take n steps per unit time, `t=k/n`:
  `S^{(n)}(t)=(1+σ/√n)^{½(nt+M_{nt})}(1−σ/√n)^{½(nt−M_{nt})}`.
  **Theorem 10.42:** as `n→∞`, `S^{(n)}(t)` converges in distribution to `exp{σB(t)−½σ²t}` (B a BM);
  the `−½σ²t` correction is necessary for martingality. Proof: `log(1+x)=x−½x²+O(x³)`,
  `log S^{(n)}(t)=nt(½log(1+σ/√n)+½log(1−σ/√n))
  + M_{nt}(½log(1+σ/√n)−½log(1−σ/√n)) → −½σ²t + σ·(M_{nt}/√n)`, and `M_{nt}/√n → B(t)`. ✅ (p-147/148)
- **Starting at x (§13.11):** `P^x(B(0)=x)=1`; distribution of `B(t)` under `P^x` = that of
  `x+B(t)` under `P^0`. (p-149)
- **Markov property (§13.12, Theorem 12.43):** `E[h(B(s+t))|F(s)] = E^{B(s)}[h(B(t))]` via the
  Independence Lemma (`g(x)=E[h(x+(B(s+t)−B(s)))]=E^x[h(B(t))]`). BM has the **strong** Markov
  property: for stopping time `τ` (`τ=min{t≥0:B(t)=x}`, Example 13.1),
  `E[h(B(τ+t))|F(τ)] = E^x[h(B(t))]`. ✅ (p-149/150/151)
- **Transition density (§13.13):** `p(t,x,y)=(1/√(2πt)) e^{−(y−x)²/(2t)}`, with
  `g(x)=E^x[h(B(t))]=∫h(y)p(t,x,y)dy`; `E[h(B(s+t))|F(s)]=∫h(y)p(t,B(s),y)dy`;
  strong Markov: `E[h(B(τ+t))|F(τ)]=∫h(y)p(t,x,y)dy`. (**vision-verified p-151**). ✅ (p-151)
- **First passage time (§13.14):** `τ=min{t≥0:B(t)=x}`, `x>0`. `exp{ΘB(t∧τ)−½Θ²(t∧τ)}` is a martingale
  ⇒ `E exp{ΘB(t∧τ)−½Θ²(t∧τ)}=1`. Let `t→∞` (Bounded Convergence; process bounded by `e^{Θx}`)
  ⇒ `E[e^{Θx−½Θ²τ}·1_{τ<∞}]=1`, so `e^{Θx}E[e^{−½Θ²τ}1_{τ<∞}]=1`. Let `Θ↓0` ⇒ `P{τ<∞}=1`;
  hence `E e^{−½Θ²τ}=e^{−Θx}`. (**vision-verified p-151**). ✅ (p-151/152)
  With `λ=½Θ²`: **`E e^{−λτ}=e^{−x√(2λ)}`**; differentiating w.r.t. λ and `λ↓0` gives
  `E τ = ∞`. **Conclusion:** BM reaches level x with probability 1; expected time to reach x is
  infinite. ✅ (p-152)
- **Reflection principle (§13.14, start):** `P{τ≤t, B(t)<x}=P{B(t)>x}` (reflection);
  `P{τ≤t}=P{τ≤t,B(t)<x}+P{τ≤t,B(t)>x}=P{B(t)>x}+P{B(t)≥x}=2P{B(t)>x}`
  `= (2/√(2πt))∫_x^∞ e^{−y²/2t}dy`. (p-152; continues beyond assigned range)

### Notes / gaps for `shreve.md` (Ch 13)
- This chapter is the **discrete/limit introduction** to BM. `shreve.md`'s Vol II Ch 3 entry covers the
  fully continuous BM (quadratic variation, GBM, transition-density first-passage Laplace transform,
  reflection joint densities of `(M,W)`) — those results are NOT on the assigned pages (they are in
  Vol II Ch 3 / later Vol I Ch 14–15 of the combined edition). Ensure the two are cross-linked.
- No math errors found in the Ch 13 content on these pages; all MGF/limit computations verified.

---

## Summary of corrections / gaps vs. existing `shreve.md`

1. **MAJOR (task framing):** pages p-115…p-151 are NOT "Information and Conditioning / Ito Integral /
   Ito-Doeblin". They are Ch 9 (Radon–Nikodym), Ch 10 (CAPM), Ch 11 (General RVs), Ch 12 (Semi-Continuous),
   Ch 13 (Brownian Motion). The Ito integral/formula are at Ch 14–15 (p-155…p-178) and "Information and
   Conditioning" is a Vol II title. Do not source those topics from these pages.
2. **Ch 10 formula error in `shreve.md`:** the optimal hedge was given as
   `Δ_k = (ζ_{k+1}(H)−ζ_{k+1}(T))/(S_{k+1}(H)−S_{k+1}(T))·X₀`. **Correct form:**
   `Δ_k = (X₀/ζ_{k+1}(H) − X₀/ζ_{k+1}(T))/(S_{k+1}(H)−S_{k+1}(T))` (difference of reciprocals). Fixed here.
3. **Ch 12 (Semi-Continuous Models) is MISSING** from `shreve.md` — add it (content above).
4. **Ch 13 (BM, limit construction) is only partially represented** (via Vol II Ch 3) — add/merge the
   Ch 13 entry above (LLN/CLT, scaling to BM, covariance `s∧t`, exponential martingale, binomial limit
   `exp{σB−½σ²t}`, first passage `E e^{−λτ}=e^{−x√(2λ)}`, reflection `P{τ≤t}=2P{B(t)>x}`).
5. **Ch 9 and Ch 11 verified error-free** in the existing extraction (a few cosmetic/OCR-only typos in
   the raw `shreve1.txt`, e.g. "Applicaton", line-break-fractured fractions, `V1(HH)`→`V2(HH)`, but no
   mathematical content is lost and all worked examples re-compute correctly).
6. **Verification method:** every numeric example re-computed by hand (Ch 9 European call V₀=1.76,
   American put optimal value 1.36 vs 0.96; state-price tree ζ values; Z(HH)=9/4 etc.), and key
   formula pages (p-115, p-119, p-124, p-151) confirmed by direct vision-reading of the rendered PNGs.

## Files
- **This verified extraction:** `/tmp/verified/shreve1_ch9-12.md`
- Inputs (unmodified): `/tmp/atlas_pages/shreve1/p-113…p-152.png`, `/tmp/atlas_extract/shreve1.txt`,
  `/tmp/atlas_extract/shreve.md`.
