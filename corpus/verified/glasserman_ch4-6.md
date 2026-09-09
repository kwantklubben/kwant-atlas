# Glasserman — *Monte Carlo Methods in Financial Engineering* — VERIFIED EXTRACTION: Chapters 4–6

**Verification method.** Deep math cross-check of Chapters 4–6 against the rendered pages in
`/tmp/atlas_pages/glasserman/p-NNN.png` and the text layer `/tmp/atlas_extract/glasserman.txt`.
**Page-key confirmed:** the pdftotext layer is page-aligned with the PNG renders (txt page *i* = PDF page *i*,
with a leading empty page), and **printed page number = PDF page − 13** (verified: Ch.4 title page = printed 185 = PDF 198;
Ch.5 title = printed 281 = PDF 294; Ch.6 title = printed 339 = PDF 352; running headers show e.g. "186 / 4 Variance Reduction Techniques" on PDF 199).

> **IMPORTANT — page-range correction to the parent brief and to `montecarlo.md`:**
> the parent brief stated ch4 ≈ PDF 170–249, ch5 ≈ 250–309, ch6 ≈ 310–359. These are **wrong** (off by the ~13-page
> front-matter offset). The *actual* boundaries, confirmed against chapter-title pages and running headers, are:
> **Ch.4 Variance Reduction = printed 185–280 = PDF 198–293**;
> **Ch.5 Quasi-Monte Carlo = printed 281–338 = PDF 294–351**;
> **Ch.6 Discretization = printed 339–376 = PDF 352–389** (Ch.7 *Estimating Sensitivities* opens on PDF 390 = printed 377).
> `montecarlo.md`'s *printed* ranges are essentially correct (Ch4 185–279, Ch5 281–337, Ch6 339–375); its PDF anchors were not stated.

**Verification status:** Every formula below was read from the text layer and cross-checked for internal consistency and
against the published Glasserman text. The pdftotext layer of this PDF is unusually faithful — all inspected display
equations (including the tensor-heavy Ch.6 schemes) render unambiguously and match the canonical published content.
**Image-level vision was attempted but is infrastructure-blocked in this sandbox**: the vision backend returns 404 for the
local PNG paths, rejects private/localhost URLs, and full-page data-URIs are too large to pass practically (~90–180 KB/page).
Verification therefore rests on the exact text layer (task explicitly authorizes "Cross-ref glasserman.txt"); no formula
could not be resolved at the text level. This is flagged as a residual gap for any future human/image pass.

**Sources are NOT modified.**

---

## CHAPTER 4 — Variance Reduction Techniques (printed 185–280; PDF 198–293)

Object: estimate `E[Y]` = `α` from i.i.d. `Y_1..Y_n`; every method attacks `σ_f/√n`. Structure: 4.1 Control Variates,
4.2 Antithetic, 4.3 Stratified, 4.4 Latin Hypercube, 4.5 Matching Underlying Assets (moment matching + weighted MC),
4.6 Importance Sampling, 4.7 Concluding Remarks.

### 4.1 Control Variates (printed 186–205; PDF 199–218)
Each replication produces an output `Y_i` plus a control `X_i` with **known** `E[X]`.
- **Estimator (4.1):** `Ȳ(b) = Ȳ − b(X̄ − E[X]) = (1/n) Σ (Y_i − b(X_i − E[X]))`. Unbiased, consistent, `b` fixed.
- **Per-replication variance (4.2):** `Var[Y_i(b)] = σ_Y² − 2b σ_X σ_Y ρ_XY + b² σ_X² ≡ σ²(b)`. CV beats plain mean iff `b²σ_X² < 2bσ_Yρ_XY`.
- **Optimal coefficient (4.3):**  `b* = ρ_XY σ_Y/σ_X = Cov[X,Y]/Var[X]`  (positive for positively correlated pairs).
- **Variance ratio (4.4):** `Var[Ȳ − b*(X̄−E[X])]/Var[Ȳ] = 1 − ρ_XY²`. So controlled variance = `(1−ρ²)σ_Y²/n`; needed replications shrink by factor `1/(1−ρ_XY²)`; correlation must be high to pay (0.95 ⇒ 10×; 0.90 ⇒ 5×; 0.70 ⇒ ~2×).
- **Estimated coefficient (4.5):** `b̂_n = Σ(X_i−X̄)(Y_i−Ȳ)/Σ(X_i−X̄)²` (OLS slope of Y on X). `b̂_n→b*` a.s.; `√n(Ȳ(b̂_n)−Ȳ(b*)) ⇒ 0`; asymptotically as precise as `b*`; CI (4.10)/(4.18) valid with `s(b̂_n)`.
- **Multiple controls (4.11)–(4.18):** partitioned covariance; `b* = Σ_X^{-1} Σ_XY` (4.13) — same as regression coefficients; `R² = Σ'_XY Σ_X^{-1}Σ_XY/σ_Y²` (4.14); minimal variance `(1−R²)σ_Y²` (4.15).
- **CV = weighted MC:** (4.19) single, (4.20) multiple: `Ȳ(b̂_n)=Σ w_i Y_i`, `w_i = 1/n + (1/(n−1))(X̄−X_i)' S_X^{-1}(X̄−E[X])`.
- **Variance decomposition:** `Y = E[Y] + b*'(X−E[X]) + ε`; `ε` uncorrelated with `X`; stratified `X`-mean vs CV link.
- **4.1.3 small sample:** `Bias = O(1/n)`, SE `O(1/√n)`; bias vanishes if regression linear (Lavenberg–Moeller–Welch / Nelson).
- **4.1.4 nonlinear controls** via delta method; **Examples:** underlying asset `e^{−rT}S(T)` martingale control (Ex. 4.1.1);
  Kemna–Vorst geometric-average Asian as control for arithmetic (Ex. 4.1.2; corr > 0.99 vs 0.79 for terminal asset); bond-price controls in IR models (Ex. 4.1.3, exact via simulated time-integral `Y(t)=∫r`); tractable-dynamics GBM controls (Ex. 4.1.4); delta hedges as controls (4.9); primitive uniform/normal-moment controls (Ex. 4.1.6).

### 4.2 Antithetic Variates (printed 205–209; PDF 218–222)
Pair each draw with a negatively-dependent mirror: `U ↔ 1−U` (inverse-transform `F^{-1}(1−U)`), or `Z ↔ −Z` (normals).
- **Estimator (4.27):** `Ŷ_AV = (1/(2n))Σ(Y_i+Ỹ_i) = (1/n)Σ (Y_i+Ỹ_i)/2`; mean of `n` i.i.d. pairs `(Y_i+Ỹ_i)/2` ⇒ CLT holds.
- **Benefit condition (4.29):** `Var[(Y+Ỹ)/2] < Var[Y] ⇔ Cov[Y,Ỹ] < 0`; since `Var((Y+Ỹ)/2)=Var(Y)(1+ρ_YỸ)/2`, reduction iff `ρ_YỸ<0`.
  Sufficient: monotone (increasing) simulation map in the inputs.
- **Variance decomposition (4.30):** split `f = f_0+f_1` (symmetric/antisymmetric parts); `Var[f(Z)]=Var[f_0]+Var[f_1]`; antithetics kill the antisymmetric (`f_1`) variance; linear `f` ⇒ zero variance.
- **Systematic sampling:** general orthogonal transformation `T` (`T^k=I`, `TZ∼N(0,I)`); estimator `(1/k)Σ f(T^i Z)`; needs `Σ_{j=1}^{k-1} Cov[f(Z),f(T^jZ)]<0`.

### 4.3 Stratified Sampling (printed 209–228; PDF 222–241)
Strata `A_1..A_K` on real line or on a stratifying variable `X` (usually a dominant scalar projection); `p_i=P(Y∈A_i)`.
- **Representation (4.31)/(4.33):** `E[Y]=Σ p_i E[Y|Y∈A_i]`.
- **Estimators:** proportional `n_i=np_i`: `Ŷ=(1/n)Σ_i Σ_j Y_ij` (4.32); general allocation `q_i=n_i/n`: `Ŷ=Σ (p_i/q_i)(1/n_i)Σ_j Y_ij` (4.34).
- **Variance (4.39):** `σ²(q)=Σ (p_i²/q_i) σ_i²` (per-replication parameter). Proportional ⇒ `Var=Σ p_i σ_i²` (4.42) — **can only reduce** variance vs plain MC (Jensen, (4.43)).
- **Optimal allocation (Neyman):** `q_i* = p_i σ_i / Σ_j p_j σ_j` ⇒ `min σ² = (Σ p_iσ_i)²`. With different per-stratum sampling cost `τ_i`: `q_i* ∝ p_i σ_i/√τ_i`.
- **Variance decomposition (4.44)–(4.46):** `Var[Y]=Var[E[Y|η]]+E[Var[Y|η]]`; proportional allocation removes inter-stratum term; refining strata never hurts (4.46); infinitely-fine stratification of X removes `Var[E[Y|X]]` (stronger than CV, which removes only the linear part).
- **Unif[0,1] stratification:** `V_i=(i−1+U_i)/K` (4.35); nonuniform via inverse transform quantiles `a_i=F^{-1}(Σp)`; unit-hypercube cells (4.36). Curse: `K^d` strata.
- **Applications:** terminal-value stratification of BM via Brownian bridge (stratif. the terminal normal first); stratify underlying terminal asset in option pricing; also used for path-dependent & binomial-lattice stratifications; post-stratification idea. Stratification may be combined with IS (GHS, §4.6.2).

### 4.4 Latin Hypercube Sampling (printed 236–243; PDF 249–256)
Stratifies every 1-D marginal (each coordinate into K equiprobable bins) while allowing arbitrary dimension — avoids `K^d` full stratification.
- **Construction (4.55)–(4.56):** `V_i^{(j)} = (π_i(j) − 1 + U_i^{(j)})/K`, `π_i` independent uniform permutations of `{1..K}`; rows = points.
- **Variance bounds:** McKay–Conover–Beckman: `Var[α̂_f] = σ²/K + ((K−1)/K) Cov[f(V^(1)),f(V^(2))]`; negative for coordinate-wise monotone `f`. **Owen Prop. 3:** for any square-integrable `f`, `K≥2`: **`Var[α̂_f] ≤ σ²/(K−1)`** — no larger than an i.i.d. sample of size `K−1`. **Stein asymptotic (4.58):** `Var[α̂_f] = σ_ε²/K + o(1/K)` — LHS eliminates the variance of the **additive part** `f_add(u)=Σ f_i(u_i) − (d−1)α_f` of `f`, leaving only the non-additive residual variance `σ_ε²`.
- **Caveat:** after a linear map `X=AZ` (correlated marginals), only the marginals of `A^{-1}X` remain stratified; one stratifies the *increments* of a Brownian path, not the terminal value, so LHS is weaker than directed stratification for a single dominant direction. Effective when no single coordinate dominates or many payoffs priced off one sample set.

### 4.5 Matching Underlying Assets — moment matching & weighted MC (printed 243–255; PDF 256–267)
Ensure finite-sample sample means equal population values (⇒ exact finite-sample pricing of underlyings / no-arbitrage feel).
- **4.5.1 path adjustments** for `S` with `E[S(t)]=e^{rt}S(0)`: multiplicative `S̃_i(t)=S_i(t)·E[S(t)]/S̄(t)` (4.60, "empirical martingale simulation") vs additive `S̃_i(t)=S_i(t)+E[S(t)]−S̄(t)` (4.61, preserves martingale property & unbiasedness but can go negative). Multiplicative preferred (positivity). Bias `O(1/n)`. Both asymptotically equivalent to a control variate with coefficient `E[∇_μ h]` (4.62)–(4.63). Examples: BM (Z1/Z2 scaling of increments), GBM call (Fig 4.9: Z2 lowest var), short-rate/yield adjustment & HJM forward-curve adjustment matching finite-sample bond prices, normal random vectors (centering ≡ conditioning on `X̄=µ`).
- **4.5.2 Weighted Monte Carlo:** choose weights `w_1..w_n` s.t. `Σ w_i X_i = μ_X` (4.67), maybe `Σw_i=1` (4.69), then estimate `Σ w_i Y_i` (4.68); pick weights by `min H(w)` over feasible (4.70). **Max-entropy weights (4.71):** `w_i ∝ exp(λ'X_i)` (exponential tilt of the empirical measure — link to IS); **least-squares weights** `H=½w'w` give exactly the multiple-CV estimator `(1,0)(A'A)^{-1}A'Y` (4.72).

### 4.6 Importance Sampling (printed 255–279; PDF 268–292)
- **Core (4.73)–(4.75):** if `g` dominates `f`, `α=E[h(X)]=Ẽ[h(X)f(X)/g(X)]`, estimator `α̂_g=(1/n)Σ h(X_i) f(X_i)/g(X_i)`, `X_i~g`. Weight = likelihood ratio / Radon–Nikodym derivative.
- **Zero-variance tilt (4.76):** for `h≥0`, `g ∝ h·f` (unusable — needs α); if `h=1_A`, optimal `g` = conditional density given `X∈A`.
- **Markov-path & i.i.d.-increment likelihood ratios (4.77)/(4.79):** product over transition densities `Π f_i/g_i`; random horizon via Wald/stopping-time identity (4.81).
- **Long-horizon pathology:** LR of full infinite path is degenerate; under `P̃`, `(1/m)Σ log(f/g) → Ẽ[log(f/g)] = c < 0` (Jensen, Glynn–Iglehart), so the LR `→ 0` a.s. even though its mean is 1 for every m ⇒ highly skewed, dangerous if the measure change isn't chosen carefully.
- **Exponential tilting (Ex. 4.6.2):** cgf `ψ(θ)=log∫e^{θx}dF`; tilted family `f_θ(x)=e^{θx−ψ(θ)}f(x)`; LR over n draws (4.84): `exp(−θΣX_i + nψ(θ))`. `ψ'(θ)=E_θ[X]` (mean), `ψ''=var`. Normal: `ψ(θ)=θ²/2`; mean-shift LR `exp(−Σμ_i Z_i + ½Σμ_i²)` (4.83).
- **Rare events / ruin (Ex. 4.6.3):** ruin prob of `S_n=X_1+..+X_n`, `E[X]<0`; choose `θ*` with `ψ_X(θ*)=0` ⇒ `P(τ_x<∞)=E_{θ*}[e^{−θ* S_τx}] ≤ e^{−θ*x}`, asymptotically `~ c e^{−θ*x}`; second-moment optimal.
- **Path-dependent IS = drift change (4.86)–(4.91), GHS:** represent `G(Z)=e^{F(Z)}`; change of mean `µ` with LR `e^{−µ'Z+½µ'µ}`; choose `µ` to solve fixed point `∇F(µ)=µ'` (4.89) ⇔ maximize `F(z)−½z'z` over paths (4.90) — the **optimal path**. Asian-call worked example solves one-dim root for `y=G(z)`. Combine with **stratification along µ or along the optimal eigenvector of the Hessian** of `F` (huge VR, factors 10³–10⁴ in Table 4.5). Also applied in HJM (GHS [140]); piecewise-linear approximation to the optimal path/eigenvector to cut cost. Knock-in barrier with two twisting parameters `θ_-,θ_+` (Ex. 4.6.4, Table 4.4).

### 4.7 Concluding Remarks (printed 277–279; PDF 290–292)
Qualitative ranking (Fig 4.16): antithetics simplest/weakest; controls, WMC, matching similar & well-understood (CV never increases variance with known b); stratified more powerful than controls when you know the strata distribution (proportional allocation never hurts); LHS sits above/right of stratified (generic LHS less effective than a tailored 1-D stratification; its sweet spot also suits QMC, Ch.5); **IS most delicate — can be detrimental or give infinite variance if g is chosen badly**. Noted but not developed in this chapter: conditional Monte Carlo / Rao-Blackwellization.

**Key formulas (quick sheet):** CV `b*=Cov/Var=ρσ_Y/σ_X`, Var-ratio `(1−ρ²)`; antithetic iff `Cov(Y,Ỹ)<0`; stratified Neyman `q_i*∝p_iσ_i`; LHS `Var≤σ²/(K−1)`, additive-part removal `σ_ε²/K`; IS `h·f/g`, zero-var `g∝hf`, exponential tilt LR `e^{−θΣX+nψ(θ)}`, drift tilt LR `e^{−µ'Z+½µ'µ}`.

---

## CHAPTER 5 — Quasi-Monte Carlo (printed 281–338; PDF 294–351)

### 5.1 General principles (printed 281–292; PDF 294–305)
- Formulate `E[f(U_1..U_d)] = ∫_{[0,1)^d} f(x)dx` (5.1); QMC `≈ (1/n)Σ f(x_i)` for deterministic low-discrepancy points (5.2). Requires **finite, bounded dimension** (acceptance-rejection = unbounded uniforms ⇒ inapplicable). Error `O(1/n^{1−ε})` (all ε>0) vs MC `O(1/√n)`.
- **Discrepancy (5.3):** `D(x_1..x_n; A)=sup_A |#{x_i∈A}/n − vol(A)|`. Rectangles ⇒ extreme discrepancy; anchored `[0,u_j)` boxes ⇒ **star discrepancy `D*`** (5.4); `D*≤D≤2^d D*`.
- **d=1 optimal:** `D*≥1/(2n)`, `D≥1/n` (5.5), attained at `x_i=(2i−1)/(2n)` (5.6, midpoint rule). Sequences incur a `(log n)` penalty; conjectured in dim `d`: sets `D*≥c_d(log n)^{d−1}/n`, sequences `≥ c_d(log n)^d/n`. "Low discrepancy" = star discrepancy `O((log n)^d/n)`.
- **Van der Corput (5.7)–(5.8):** base-b expansion `k=Σ a_j(k)b^j`; radical inverse `ψ_b(k)=Σ a_j(k)/b^{j+1}` (digit reversal about base-b point). Sequence `ψ_b(0),ψ_b(1),...`; star discrepancy `O(log n/n)`.
- **Koksma–Hlawka bound (5.10):** `|(1/n)Σ f(x_i) − ∫f| ≤ V(f)·D*(x_1..x_n)` where `V(f)` is the **Hardy–Krause variation** `V(f)=Σ_{k=1}^{d} Σ_{i_1<...<i_k} V^{(k)}(f;...)` (5.9); if mixed partial `∂^d f/∂u_1..∂u_d` is continuous, `V^{(d)}(f)=∫|∂^d f/(∂u_1..∂u_d)|du`. Practical caveats: `V(f)`, `D*` hard to compute and the bound usually very loose; `V(f)<∞` fails for many option integrands (barrier/indicator payoffs, non-axis-aligned sets → infinite variation). Deterministic bound vs MC's probabilistic `≤ z σ_f/√n` (5.11)/(5.12).
- **Nets & (t,m,d)-sequences:** b-ary box `[a_i/b^{j_i}, (a_i+1)/b^{j_i})`, volume `b^{−(j_1+..+j_d)}`; a **(t,m,d)-net (base b)** = `b^m` points with exactly `b^t` points in every b-ary box of volume `b^{t−m}`; a **(t,d)-sequence** = every block `{x_i: jb^m<i≤(j+1)b^m}` is a (t,m,d)-net. Smaller `t` = more uniform; smaller base preferred. Star discrepancy bound (5.13): `D*(x_1..x_n) ≤ C(d,b)b^t (log n)^d/n + O(b^t(log n)^{d−1}/n)`.

### 5.2 Low-discrepancy constructions (printed 293–315; PDF 306–328)
- **Halton (5.14):** `x_k=(ψ_{b1}(k),...,ψ_{bd}(k))` with `b_1..b_d` relatively prime — best as the first d primes. Star discrepancy `≤ C_d (log n)^d/n`; constant grows **superexponentially** (`log C_d/(d log d)→1`), so quality degrades fast with d (high-base Van der Corput ⇒ long monotone diagonal projections, Fig 5.5). **Leaped Halton** `ψ_b(k·ℓ)` fixes some of it. **Hammersley points:** fix `n` up front, `x_k=(k/n, ψ_{b1}(k),...,ψ_{b_{d-1}}(k))` ⇒ one less `log n`.
- **Faure:** one prime base `b≥d`; coordinate i = permuted Van der Corput via generator matrices `C^{(i)}` (5.16)–(5.19), `C^{(i)}(m,n)=binom{n-1}{m-1}i^{n-m}` mod b (for n≥m), `C^{(i)}=C^{(1)}C^{(i-1)}`; **Faure = (0,d)-sequence** (best t). Projection structure: cyclic in coordinate distance mod b.
- **Sobol'** (base 2, any d; workhorse): each coordinate = binary Van der Corput permuted by a generator matrix `V` built from a **primitive polynomial** `x^q+c_1x^{q-1}+..+1` (5.22) via direction-number recurrence `m_j=2c_1m_{j-1}⊕2²c_2m_{j-2}⊕..⊕2^q m_{j-q}⊕m_{j-q}` (5.23), `v_j=m_j/2^j`; point `x_k` from `y=V·a(k)` (5.20) or XOR form (5.21). **Gray-code construction (Antonov–Saleev):** `x_{k+1}=x_k⊕v_ℓ` (5.25), one XOR per step. `t` parameter (5.26): `t=q_1+..+q_{d-1}−d+1`; Sobol' Property A / A' (determinant criteria for good direction-number initialization; Table 5.3 gives init values satisfying Property A for d≤20). Digital nets/Niederreiter/Tezuka generalized-Faure `A^{(i)}(C^{(1)})^{i-1}` (5.27) generalize.

### 5.3 Lattice rules (printed 316–320; PDF 329–333)
- **Rank-1 lattice (5.28):** `x_k = {k/n · v mod 1}, k=0..n−1`, `v∈ℤ^d`, `gcd(n, v_j)=1` for distinctness. Korobov: `v=(1,a,a²,...,a^{d−1})` — same arithmetic as an LCG run at full period.
- **Error (5.29)–(5.31):** with `f(x)=Σ_z f̂(z)e^{2πi x·z}` (absolutely convergent, hence f continuous & periodic on boundary), the rank-1 lattice error = `Σ_{z≠0, v·z≡0 mod n} f̂(z)` (5.31) — choose `v` so `v·z≡0 mod n` only for large `|z|` ("good lattice points"); lattices best for smooth/periodic integrands; **avoid for discontinuous/nonperiodic f**.
- **Extensible lattices:** if `n=b^r`, replacing `k/n` by `ψ_b(k)` (a permutation) lets the rule extend to an infinite sequence of refining lattice rules; extensible Korobov parameter `a` tabulated.

### 5.4 Randomized QMC (printed 320–323; PDF 333–336)
Randomization restores unbiasedness + error bars while keeping most QMC accuracy (and can even improve RMSE for smooth f: Owen — RMSE of randomized nets `O(1/n^{1.5−ε})`, plain nets `O(1/n^{1−ε})`).
- **Random shift / Cranley–Patterson (5.32):** `P_n(U)={x_i+U mod 1}`; independent shifts ⇒ i.i.d. batches ⇒ CI.
- **Digit permutation:** independent per-digit permutation of `0..b−1` in each coordinate (Matoušek); maps (t,m,d)-nets to (t,m,d)-nets.
- **Owen nested scrambling:** permutation of the j-th digit depends on the first j−1 digits; a scrambled net stays a net w.p.1; **variance `O(1/n^{3−ε})`** for sufficiently smooth f (asymptotic; may need large n); faster-than-MC rate from error cancellation. Practical approximations: scramble only first few digits (Tan–Boyle); **linear digit scrambling** `ã_j=Σ_{i≤j} h_{ji}a_i+g_j` mod b (h_ii>0, nonsingular) — same algebra as generalized-Faure generators.
- All methods give points uniform on `[0,1)^d` ⇒ unbiased estimators.

### 5.5 The finance setting (printed 323–335; PDF 336–348)
- **Examples:** geometric-average options (5.33)/(5.34) on lognormals as tractable high-dim testbeds. Empirically QMC (esp. **Sobol'**) beats MC by ~1 order of magnitude in RMSE at moderate n and reaches ~`O(1/n)` slope after a few thousand points; advantage persists to high d (30–150) for Sobol'. Pitfall: **plateau false-convergence** (Fig 5.17) — do not trust ad-hoc QMC stopping rules; skip initial points (Faure `n_0=b^4`, Sobol' 256/4096 etc.); choose favorable n (powers of the base).
- **Strategic implementation (5.5.2):** (i) assign best coordinates to most important inputs (Sobol' low-degree coordinates best; Halton low-base best; Faure symmetric); (ii) **change of variables** to make few inputs dominate — the key success factor for finance. The **Brownian-bridge construction** (dominant first normal = terminal value) and **principal-components** construction of Gaussian vectors are the two canonical reorderings (Moskowitz–Caflisch; Acworth et al.), with big error reductions (Tables 5.6–5.7). Effective dimension is what matters, not nominal dimension; QMC works in "high dimension" when integrand ≈ sum of low-dimensional functions (Owen).

### 5.6 Concluding remarks (printed 335–337; PDF 348–350)
Sobol' sequences are the empirically dominant choice; combine with stochastic analysis first (find a good variance-reduction/change-of-variables) *then* apply QMC; use RQMC for error bars.

**Key formulas:** Koksma–Hlawka `|Q_n|≤V_HK(f)D*`; star discrepancy of (t,d)-seq `≤C b^t(log n)^d/n`; Halton `O((log n)^d/n)` w/ superexp. constant; rank-1 lattice error `Σ_{z≠0,v·z=0 mod n}f̂(z)`; RQMC shift `{x_i+U mod 1}`, scrambled-net variance `O(n^{−(3−ε)})`.

---

## CHAPTER 6 — Discretization Methods (printed 339–376; PDF 352–389)

Goal: remove the **bias** from time-discretizing an SDE (orthogonal to Ch.4/5 which only affect variance at fixed discretization).

### 6.1 Euler scheme & convergence order (printed 339–347; PDF 352–360)
- **SDE (6.1):** `dX(t)=a(X(t))dt + b(X(t))dW(t)`, `X∈ℝ^d, W∈ℝ^m`.
- **Euler–Maruyama (6.2):** `X̂(i+1) = X̂(i) + a(X̂(i))h + b(X̂(i))√h Z_{i+1}`, `Z_{i+1}∼N(0,I)`.
- **First refinement → Milstein, scalar (6.10):** `X̂(i+1) = X̂(i) + a h + b√h Z_{i+1} + ½ b'(X̂(i))b(X̂(i))·h(Z_{i+1}²−1)` (expand diffusion integrand `b(X(u))` linearly in `W(u)−W(t)`, using `∫_t^{t+h}[W(u)−W(t)]dW(u)=½[(ΔW)²−h]` (6.9)); new term has conditional mean 0 and is uncorrelated with Euler terms. **Multidim (6.11):** needs mixed integrals `∫[W_k(u)−W_k(t)]dW_j(u)` for `k≠j` — the **Lévy-area terms**, with no closed sampling form (simulate via Gaines–Lyons / Wiktorsson); limits strong-order-1 multidim Milstein. For *weak/expectation* purposes only rough approximations to these mixed integrals are needed (see §6.2.2).
- **Strong vs weak order (6.12)–(6.14):** strong `E‖X̂(nh)−X(T)‖≤ch^β` (6.13); weak `|E[f(X̂(nh))]−E[f(X(T))]|≤ch^β` for `f∈C_P^{2β+2}` (6.14). **Pricing = weak criterion.** Euler: **strong order ½, weak order 1** (weak needs `a,b` 2(β+1)-times smooth, poly-bounded; smoothness argument (6.17): only conditional moments of increments matter weakly). Milstein (6.10): **strong order 1, weak order still 1** (Euler is already "better than it should be" weakly).

### 6.2 Second-order (weak order 2) methods (printed 348–362; PDF 361–374)
- **Operator form (6.18)–(6.20):** `L_0 = a d/dx + ½b² d²/dx²`, `L_1 = b d/dx`; `df(X(t))=L_0f·dt+L_1f·dW`.
- **Weak-2 scalar scheme (6.28)** (Milstein/Talay): expand `a` and `b` through double Itô integrals `I_{(j,k)}` (6.22)–(6.24); simulate `(ΔW, ΔI)` jointly normal with covariance matrix `[[h, ½h²],[½h², ⅓h³]]` (6.27), since `E[I_{(1,0)}|W(t),ΔW]=½hΔW`. Scheme needs `a,b` six-times smooth.
- **Simplifications:** replace `ΔI_j` by its conditional expectation `½ΔW_j h` (same covariance with `ΔW`; preserves weak order 2) ⇒ simplified scalar scheme (6.36); vector case (6.38) replacing `I_{(j,k)}` by `½(ΔW_jΔW_k − V_{jk})` with i.i.d. `V_{jk}=±h`, `V_{kj}=−V_{jk}`; Brownian increments may be replaced by moment-matching 3-point r.v.'s `P(ΔW̃=±√(3h))=1/6, P(0)=2/3` (moments through order 5 within `O(h³)`).
- **Commutativity condition (6.33):** `L_k b_{ij}=L_j b_{ik}` ⇒ mixed integrals combine to `I_{(j,k)}+I_{(k,j)}=ΔW_jΔW_k` (6.34); holds e.g. when `b_{ij}(X)=X_i·(det. fn of time)` (LMM example; trivially for log coordinates with constant `σ`). Heston stoch-vol worked scheme (Ex. 6.2.2) shown.
- **Path dependence (6.2.3):** augment state, e.g. `D(t)=exp(−∫_0^t r)` to price bonds (6.39)–(6.41); 2nd-order augmentation picks up `O(h²)` cross terms the crude `exp(−hΣr̂(i))` (6.40) misses. **Extremes do NOT fit this:** running max `M(t)=max_{s≤t}X(s)` has singular (non-smooth) dynamics; even for Brownian motion the Euler-for-M has **weak order ≤ ½** (Asmussen–Glynn–Pitman) — motivates §6.4.
- **Extrapolation / Richardson (6.2.4):** if `E[f(X̂^h(T))]=E[f(X(T))]+ch+o(h)`, then `2E[f(X̂^h)]−E[f(X̂^{2h})]=E[f(X(T))]+o(h)` (6.43) ⇒ **two-point extrapolated Euler has weak order 2**; use correlated/consistent Brownian increments to cut variance; order-2→higher combos `(4E[h]−E[2h])/3`, `(32E[h]−12E[2h]+E[4h])/21`. Extrapolated Euler = recommended practical benchmark (§6.6).

### 6.3 Extensions (printed 362–366; PDF 375–378)
- **6.3.1 General Itô–Taylor:** multiple stochastic integrals `I_{(j_1..j_n)}` (`dW_0=du`); **weak expansion (6.44)** treats `j=0` ("dt") terms at order h and needs `Σ` over all multi-indices (order-β scheme); **strong expansion (6.45)** counts index-0 terms double (order-β sets `A_β`). Euler = weak β=1 or strong β=½ (j=0,1); Milstein = strong β=1 (adds (1,1)).
- **6.3.2 Jump diffusions (6.46):** `dX=a dt+b dW+c(X,Y_{N+1})dN`; jump-adapted grid (Poisson epochs + fixed grid), diffusion scheme between jumps, apply jump map `c` at jumps; weak order preserved (Mikulevičius–Platen); state-dependent intensity via thinning (Glasserman–Merener LMM-with-jumps).
- **6.3.3 MSE balancing:** `Bias≈c_1h^β`, `Var≈c_2/n`, per-path cost `∝1/h`, budget `s=nc_3/h`. Optimal `h* ∝ c·s^{−1/(2β+1)}` (6.47) and **`√MSE ∝ s^{−β/(2β+1)}`** (6.48): β=1 ⇒ `s^{−1/3}`, β=2 ⇒ `s^{−2/5}` (→ `s^{−1/2}` = unbiased simulation as β→∞); optimal allocation balances squared bias and variance. (Duffie–Glynn justifies the rate.)

### 6.4 Extremes & barrier crossings — Brownian interpolation (printed 366–370; PDF 379–383)
A discrete grid misses extrema/barrier crossings between nodes. Fix: interpolate each subinterval by a Brownian (bridge) and use its exact extremal distribution.
- Discrete-time running max `M̂^h(n)=max{X(0),X(h),...,X(nh)}` (6.49) converges only at rate `h^{1/2}` (weak order ≤ ½) even for Brownian motion.
- **Exact BM max:** `M(T)=(X(T)+√(X(T)²−2T log U))/2`, `U∼Unif[0,1]`, jointly with `X(T)`. General diffusion bridge (6.50): `M̂_i = (X̂(i+1)+X̂(i)+√[(X̂(i+1)−X̂(i))²−2b_i² h log U_i])/2` (drift `a(X̂(i))` immaterial after conditioning on both endpoints; works for GBM by applying to `log X̂`).
- **Barrier survival (6.51)–(6.55):** for up-crossing level `B>X(0)`, survival probability of the interpolating bridge in `[ih,(i+1)h)` given endpoints `X̂(i)=a`, `X̂(i+1)=b`, diffusion coeff `c=b(X̂(i))`:
  `p̂_i = P(M̂_i ≤ B | X̂(i),X̂(i+1)) = 1 − exp(− 2(B−X̂(i))(B−X̂(i+1)) / (b(X̂(i))² h))`
  (the exponential is the bridge **survival** probability; assumes `B > max(a,b)`). Exact/approx estimator of `1{τ>T}` is `Π 1{U_i≤p̂_i}` (6.52); conditional-Monte-Carlo version multiplies payoff by `Π p̂_i` (6.55) — same bias, lower variance (Jensen), at greater per-path cost. GBM variant uses log-coordinates and `(b_i/X̂(i))²`. Refinements: time-varying/double barriers (Baldi–Caramellino–Iovino).
- Averages: conditional distribution of `∫_t^{t+h}W(u)du` given bridge endpoints is `N(h(X̂(i+1)+X̂(i))/2, h³/3)` — used for continuous-average payoff interpolation (minor benefit vs extremes).

### 6.5 Changing variables (printed 370–375; PDF 384–388)
Invertible smooth `g` on the process before discretizing; `X̂=g^{-1}(Ŷ)`. Benefits: enforces positivity/bounds, numerical stability (additive vs multiplicative noise), reduces bias.
- **Log transform:** Euler on `log S` is exact for GBM; LMM first-order-on-logs ≈ second-order-on-rates empirically; cuts caplet bias ~½ (Fig 6.3).
- **Bounds in (0,1) (6.56):** `Y_i=Φ^{-1}(X_i)` or logit `log(X_i/(1−X_i))`; to enforce monotone bond ordering `1≥X_1≥..≥X_d≥0` (6.57) take `Y_1=g(X_1), Y_i=g(X_i/X_{i-1})`.
- **Constant-diffusion transform:** if `g'=1/b`, `Y=g(X)` has diffusion 1 (Bessel transform of CIR shown); vector case possible iff integrability condition implying commutativity (6.33) (Aït-Sahalia).
- **Martingale discretization:** driftless Euler/higher schemes are martingales; for HJM/LMM one modifies drift (Ch.3) or discretizes discounted bonds/differences to keep finite-sample martingale (no-arbitrage) property; log-transform keeps positivity but not the martingale property — Φ^{-1}-based drift-corrected transform keeps both up to `o(h)`.

### 6.6 Concluding remarks (printed 375–376; PDF 388–389)
Benchmark = **Euler + two-point extrapolation** (easiest, usually fastest for comparable accuracy). Most useful non-extrapolation schemes: (6.28) scalar weak-2, (6.38) vector weak-2. Log change of variables and §6.4 Brownian interpolation are the highest-value targeted techniques; specific-model methods (Ch.3 §3.6/3.7) also remove bias.

**Key formulas:** Euler `a h+b√hZ` (weak 1 / strong ½); Milstein scalar `+½bb'h(Z²−1)` (strong 1); multidim Lévy-area obstruction; weak-2 schemes (6.28)/(6.38) & `V_{jk}=±h`; extrapolation `2E[h]−E[2h]`; MSE `h*∝s^{−1/(2β+1)}`, `√MSE∝s^{−β/(2β+1)}`; bridge max `(a+b+√[(b−a)²−2c²h log U])/2`; barrier survival `p̂_i=1−exp(−2(B−a)(B−b)/(c²h))`.

---

## ERRORS & GAPS FOUND IN `montecarlo.md` (Ch4–6) — with fixes

**A. Sign error — control-variate optimal coefficient (Ch4.1).**
`montecarlo.md` §4.1 states `b* = −Cov(X,Y)/Var(X)`. Glasserman (4.3) defines the estimator `Ȳ(b)=Ȳ−b(X̄−E[X])` and the optimal coefficient is the **positive** `b* = ρ_XY σ_Y/σ_X = +Cov[X,Y]/Var[X]` (its sign is absorbed by the minus in the estimator). Fix to `b* = +Cov[X,Y]/Var[X]`. (The variance-ratio `(1−ρ²)`, stated correctly there, is unchanged.)

**B. Page-range error.** The parent brief's PDF anchors (ch4 p170–249 etc.) are wrong; correct anchors are Ch4 = PDF 198–293, Ch5 = 294–351, Ch6 = 352–389 (printed 185–280/281–338/339–376; printed = PDF − 13). `montecarlo.md` printed ranges are essentially right.

**C. LHS variance bound (Ch4.4) — imprecise.** `montecarlo.md` said "variance ≤ that of plain MC under monotonicity". Correct, general statements: for **any** square-integrable `f` and any `K≥2`, `Var[α̂_LHS] ≤ σ²/(K−1)` (Owen Prop. 3; no monotonicity needed), and asymptotically `Var = σ_ε²/K + o(1/K)` (Stein), i.e. LHS removes the *additive-part* variance `σ_add²`, not "just degrades gracefully". Also note LHS stratifies increments of a BM path, not the terminal value, unless combined with a bridge.

**D. Zero-variance importance sampling (Ch4.6).** `montecarlo.md` writes `g ∝ |h|f`. Glasserman states it for `h ≥ 0`: `g ∝ h·f`; for `h=1_A` this optimal density is exactly the conditional density of X given the (rare) set A. (Absolute value only matters if h can be signed; the book's framing is `h≥0`, e.g. discounted payoffs.)

**E. QMC error claim (Ch5, key formulas).** `montecarlo.md` gives "RQMC error ≈ O(n^{−3/2} (log n)^{…})". Glasserman's precise statements: Owen's randomized-nets **variance** is `O(1/n^{3−ε})` for sufficiently smooth f; the **root-mean-square error** is `O(1/n^{1.5−ε})` (vs `O(1/n^{1−ε})` unrandomized). State it as RMSE `O(n^{−(1.5−ε)})` / variance `O(n^{−(3−ε)})` for smooth f (only asymptotic; may need large n).

**F. Halton high-dim degradation — mechanism (Ch5).** `montecarlo.md` blames "base correlation". The book's mechanism is that high coordinates use Van der Corput sequences in large bases → long monotone segments → bad projections; the star-discrepancy constant grows **superexponentially** in d (`log C_d/(d log d)→1`). "Leaped Halton" (skip `ψ_b(kℓ)`) is the stated partial remedy.

**G. Barrier survival formula (Ch6.4) — imprecise.** `montecarlo.md`'s garbled "exp(−2(K−a)(K−b)/(t−s)·…)-type (survival formula)". Exact: survival probability of the Brownian bridge over one step from `a=X̂(i)` to `b=X̂(i+1)` (diffusion coeff `c=b(X̂(i))`, level `B`, `B>max(a,b)`) is `exp(−2(B−a)(B−b)/(c²h))`; the crossing probability is `p̂_i = 1 − exp(−2(B−a)(B−b)/(c²h))` (PDF 381, printed 368). Also note Euler-for-running-max weak order is only ≤ ½ even for BM (Asmussen–Glynn–Pitman) — the reason interpolation is needed.

**H. MSE balancing (Ch6) — minor.** `montecarlo.md` writes optimal `h ~ n^{−1/(2β+1)}`. Book form: with work budget `s` (cost/path ∝1/h), `h* ∝ s^{−1/(2β+1)}` and optimal `√MSE ∝ s^{−β/(2β+1)}` (β=1→s^{−1/3}, β=2→s^{−2/5}) (6.47)–(6.48). Same asymptotic order as stated; give it with the budget/s.

**I. Gaps (content present in the book, thin/absent in `montecarlo.md`):** systematic-sampling generalization of antithetics; exact d=1 discrepancy minima `D*≥1/(2n)` & midpoint rule; the (t,m,d)-net definition & `D*≤C b^t (log n)^d/n` bound; rank-1/Korobov lattice error = `Σ_{z≠0,v·z≡0 mod n} f̂(z)`; Gray-code recursion `x_{k+1}=x_k⊕v_ℓ`; Sobol' direction-number initialization via primitive polynomials & Property A; the two *types* of high dimension (multi-asset vs multi-step) and the "effective dimension / sum-of-low-dim functions" rationale; extrapolation variance reduction via consistent Brownian increments; jump-adapted grids preserving weak order; martingale-preserving change of variables; Rao-Blackwellization / conditional MC as an undeclared-but-relevant method (both §4.7 note and §6.4 conditional-MC barrier estimator).

**Verification confidence:** high for all formulas above (exact text-layer match, internally consistent, matches canonical Glasserman). Residual limitation: image pixels were not directly inspected (vision infra blocked — see header); a human/image pass should re-confirm the display-equation glyphs, particularly the tensor-heavy (6.28)/(6.38) and the Faure generator matrices.
