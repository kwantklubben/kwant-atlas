# Shreve, *Stochastic Calculus for Finance I* — Chapters 5–8
## MATH-VERIFIED, vision-corrected deep-read (combined/lecture edition, PDF pages 78–114)

**Verification method.** Formulas below were checked against the rendered page images at
`/tmp/atlas_pages/shreve1/p-078.png … p-114.png` (mostly p-079…p-112) and cross-referenced against the
typeset text `/tmp/atlas_extract/shreve1.txt` (page index = image number − 1). The random-walk core was
read **directly by vision_analyze** on the rendered PNGs: exponential martingale and `P{τ<∞}=1`
(p-099), the MGF derivation `E α^τ` (p-101, p-102), the strong-Markov / general-first-passage moment
`E α^{τ_m}` (p-104), the perpetual American put values (p-105), and the piecewise continuous value
function `v(x)` with the difference-equation conditions (p-108). Ch5–7 recursion/property formulas were
confirmed against the clean text of p-080…p-096 (American recursion worked example, consumption hedge,
optional sampling, Definition 6.1 (a)–(d), compound-European valuation, Jensen / no-early-exercise
corollary, stopped-martingale theorem). Minor 404 hiccups from the vision backend were bypassed by
waiting and retrying, or by cross-checking the legible raw text of the same page.

**IMPORTANT structural note / discrepancy vs. the requested chapter names.** The parent task labelled
these chapters *Random Walk / Interest-Rate-Dependent Assets / Toward Continuous-Time Models / General
Probability Theory* — the **standard** Shreve I titles. The PDF on disk is a **reorganized "lecture"
edition**; on PDF pages 78–114 it carries, in this order:
- **Ch 5  Stopping Times and American Options** (PDF p-079…p-086);
- **Ch 6  Properties of American Derivative Securities** (PDF p-087…p-092);
- **Ch 7  Jensen's Inequality** (PDF p-093…p-098);
- **Ch 8  Random Walks** (PDF p-099…p-112); Ch 9 (Radon–Nikodym) begins at p-113.

So only **Random Walk** of the four nominal topics lives in this page range (it is Ch 8 here, Ch 5 in the
standard edition). **Interest-Rate-Dependent Assets and Toward Continuous-Time Models** are not in
pp. 78–114 — they sit in the continuous-time half of this combined volume (and are cross-covered by
Shreve Vol II), and **General Probability Spaces** was already covered back in lecture-edition Ch 1
(§1.4, PDF ≈ p-045). The deep-read below reports what is actually typeset on pp. 78–114, which is the
math the existing extraction's "Ch 5–8" sections describe. PDF page number ≈ printed page number + 2
(e.g. p-080 = printed p78, p-099 = printed p97).

---

## Chapter 5 — Stopping Times and American Options (PDF p-079…p-086)

### 5.1 American Pricing
- **European recap:** terminal value `v_n(x) = g(x) = (K−x)⁺` for a put of strike `K`; backward recursion
  `v_k(x) = (1/(1+r))[ p̃ v_{k+1}(ux) + q̃ v_{k+1}(dx) ]`. Value at time 0 of the *European* option.
- **American option:** holder may exercise at any time `k`, receiving intrinsic `g(S_k)`; pricing replaces
  the plain risk-neutral recursion by
  `v_k(x) = max{ (1/(1+r))[ p̃ v_{k+1}(ux) + q̃ v_{k+1}(dx) ], g(x) }`
  (compare intrinsic with continuation value; when `g` exceeds continuation the option is exercised early).
- **Worked example (Ex 5.1, Fig 5.1)** — American put, `S0=4, u=2, d=1/2, r=1/4, p̃=q̃=1/2, n=2, K=5`
  (this is the same parameter set later reused in the perpetual put, Ch 8.7). `g(x)=(5−x)⁺`:
  - `v2(x)=(5−x)⁺`: `v2(16)=0, v2(4)=1, v2(1)=4`.
  - `v1(8)=max{(4/5)[½·0+½·1], 0} = 0.40`; `v1(2)=max{(4/5)[½·1+½·4], 3} = max{2,3}=3` (**early exercise**
    at the down node: intrinsic 3 > continuation 2).
  - `v0(4)=max{(4/5)[½·0.40+½·3], 1} = max{1.36,1} = 1.36` (note `(4/5)=1/(1+r)` since `r=1/4`).
  - **Delta hedge** from the H and T state equations `v1(S1(ω))=Δ0 S1(ω)+(1+r)(X0−Δ0 S0)` with `X0=v0(4)=1.36`
    gives `Δ0 = −0.43` (both states yield the same Δ0, consistency check). Short-selling the stock to hedge a put.
- **Hedging with consumption.** If the option is not exercised, the seller can extract consumption `C_k`;
  the value process follows `X_{k+1} = Δ_k S_{k+1} + (1+r)(X_k − C_k − Δ_k S_k)`. The discounted portfolio
  value `(1+r)^{−k}X_k` is a supermartingale, `X_k ≥ g(S_k)`, and `X` is the **smallest** process with these
  two properties. (Consumption `C_k` is made precise in Ch 6 Lemma 2.21.)

### 5.2 Stopping Times
- **Definition:** random `τ` (values `0,…,n`) is a stopping time iff `{τ=k} ∈ F_k` for every `k`
  (decision depends only on the first `k` tosses — "no look-ahead"). Stopping *at expiration* allowed.
- **Example of a non-stopping time:** one depending on the *future* running minimum `m_2 = min_{0≤j≤2}S_j`
  (p-082) — such random times are *not* `F_k`-measurable at the required times.
- **Information up to τ** (`F_τ`), atoms; **optional sampling** (Theorem 3.17): if `{Y_k,F_k}` is a
  martingale and `σ,τ` are bounded stopping times with `τ≤σ`, then `Y_τ = E[Y_σ | F_τ]`; `≤` for a
  submartingale, `≥` for a supermartingale. Consequence `E Y_τ = E Y_σ`, `Y_0 ≤ E Y_τ` for submartingales.
  Applied (Ex 5.5) to the discounted stock `(4/5)^k S_k` (a `P̃`-martingale): `Ẽ[(4/5)²S_2|F_τ]=(4/5)^τ S_τ`.

---

## Chapter 6 — Properties of American Derivative Securities (PDF p-087…p-092)

**Definition 6.1.** An American derivative security is an adapted nonneg process `{G_k}_{k=0}^n`
(`G_k` is `F_k`-measurable); exercising at `k` pays `G_k`. Four characterizing properties:

- **(a) Value is the optimal-stopping value**
  `V_k = (1+r)^k · max_{τ∈T_k} Ẽ[(1+r)^{−τ} G_τ | F_k]`,
  the maximum over stopping times `τ ≥ k` almost surely (`T_k` = stopping times taking values `k,…,n`).
- **(b) Smallest supermartingale.** `{(1+r)^{−k}V_k}_{k=0}^n` is the **smallest** supermartingale that
  dominates `{G_k}` (i.e. satisfies `V_k ≥ G_k` a.s. for all `k`).
- **(c) Optimal exercise time.** Any stopping time attaining `V_0 = Ẽ[(1+r)^{−τ}G_τ]` is optimal; in
  particular `τ* ≜ min{k : V_k = G_k}` is an optimal exercise time. Proof (p-092): if `τ₀` attains the
  maximum then `V_{τ₀}=G_{τ₀}` a.s., so `τ* ≤ τ₀`; optional sampling on the supermartingale shows `τ*`
  also attains the maximum.
- **(d) Hedge.** `Δ_k = (V_{k+1}(·,H)−V_{k+1}(·,T))/(S_{k+1}(·,H)−S_{k+1}(·,T))` (same difference-quotient
  form as European).

**Hedge with consumption (Lemma 2.21).** Define
`C_k = V_k − (1/(1+r)) Ẽ[V_{k+1}|F_k]`; the discounted supermartingale property makes `C_k ≥ 0` a.s.
Then `X_k = V_k` for all `k` under the recursion
`X_{k+1} = Δ_k S_{k+1} + (1+r)(X_k − C_k − Δ_k S_k)`, `X_0 = V_0`, with the book proof verifying
`X_{k+1}(H)=V_{k+1}(H)` by `(1+r)(V_k−C_k)=p̃ V_{k+1}(H)+q̃ V_{k+1}(T)` and the Δ algebra collapsing to
`V_{k+1}(H)`.

### 6.3 Compound European Derivative Securities
- A compound European security = `n+1` simple European securities, security `j` paying `C_j` (an
  `F_j`-measurable payoff) at time `j`. Value of the `j`-th at time `k≤j`:
  `V_k^{(j)} = (1+r)^k Ẽ[(1+r)^{−j} C_j | F_k]`.
- **Total value:** `V_0 = Σ_j V_0^{(j)} = Ẽ[ Σ_{j=0}^n (1+r)^{−j} C_j ]`.
- Superpose the per-payment hedges: short one unit, consume `V_0` at time 0, receive `C_k` and run the
  hedging portfolio each period; wealth reaches exactly 0 after the last payment.

### 6.4 Optimal Exercise via Conversion
Choosing a stopping time converts the American security `{G_k}` into a compound European security with
per-period payment `C_j = G_j·1_{τ=j}`:
`V_0(τ) = Ẽ[Σ_j (1+r)^{−j} G_j 1_{τ=j}] = Ẽ[(1+r)^{−τ}G_τ]`.
Maximizing over `τ` recovers Definition 6.1(a); `τ*` attains it (see (c)).

---

## Chapter 7 — Jensen's Inequality (PDF p-093…p-098)

- **Conditional Jensen (Lemma 7.1):** for convex `φ`, `E[φ(X)|G] ≥ φ(E[X|G])`.
- **Theorem 1.24 (convex functions of martingales):** if `{Y_k}` is a martingale and `φ` convex then
  `{φ(Y_k)}` is a submartingale — proof is one line by conditional Jensen:
  `E[φ(Y_{k+1})|F_k] ≥ φ(E[Y_{k+1}|F_k]) = φ(Y_k)`.
- **Corollary 2.25 (no early exercise of an American call).** Let `g:[0,∞)→ℝ` be convex with `g(0)=0`
  (e.g. `g(x)=(x−K)⁺`), and `r ≥ 0`. For the American security with payoff `g(S_k)`,
  `Ẽ[(1+r)^{−n} g(S_n)] = max_τ Ẽ[(1+r)^{−τ} g(S_τ)]`
  — the American value equals the European value and `τ = n` is optimal (never early-exercise a
  dividend-free call). Key inequality: convexity with `g(0)=0` gives `g(λx) ≤ λg(x)` for `0≤λ≤1`, which
  combined with the discount factor `(1+r)^{−k} ≤ 1` (as `r≥0`) makes `(1+r)^{−k}g(S_k)` a submartingale;
  optional sampling finishes it.
- **Theorem 3.26 (stopped processes):** a stopped martingale/submartingale/supermartingale
  `Y_{k∧τ}` is still one — proof by conditioning on the `F_k`-set `{τ≤k}`:
  `E[Y_{(k+1)∧τ}|F_k]=Y_{k∧τ}`.

---

## Chapter 8 — Random Walks (PDF p-099…p-112)

### 8.1 First Passage Time
Toss a fair coin infinitely often (`P{H}=P{T}=1/2`), `Ω` = all infinite `H/T` sequences. Define
`Y_j=+1` on `H`, `−1` on `T`; `M_0=0`, `M_k=Σ_{j=1}^k Y_j` — the **symmetric random walk** (analogue of
Brownian motion; later "scaled" to reach BM). **First passage time to 1:**
`τ = min{k≥0 : M_k=1}`, `τ=∞` if the walk never reaches 1 (e.g. `ω=TTTT…`). This is the first time Heads
leads Tails by one.

### 8.2 τ is almost surely finite — the exponential martingale
`{M_k}` is a martingale; so is the **exponential martingale** (Homework; read on p-099)
`N_k = exp{ θM_k − k log( (e^θ+e^{−θ})/2 ) } = e^{θM_k} ( 2/(e^θ+e^{−θ}) )^k`,
with `(e^θ+e^{−θ})/2` the step MGF `E[e^{θY_j}]`. Stopping at `τ` and using the bound
`0 ≤ N_{k∧τ} ≤ e^θ` (since `M_{k∧τ}≤1` and the power base `<1`) lets one apply **bounded convergence** to
`1=E[N_{k∧τ}]`: as `k→∞`, `E[ N_τ ·1_{τ<∞} ]=1` whence `P{τ<∞}=1`. **(Verified by vision on p-099 and p-101.)**

### 8.3 The MGF of τ
From `E[ (2/(e^θ+e^{−θ}))^τ ] = e^{−θ}` (Eq. 2.3, p-101) and setting
`α = 2/(e^θ+e^{−θ})` (solve the quadratic in `e^{−θ}` and take the negative root so that `e^{−θ}<1`):
**`E[α^τ] = (1−√(1−α²))/α` for `0<α<1`** (Eq. 3.1, p-102). Root selection uses
`1−√(1−α²) < α ⇔ e^{−θ}<1`. **(Verified by vision on p-101 and p-102.)**

### 8.4 Expectation of τ is infinite
`E α^τ = (1−√(1−α²))/α`; differentiating,
`E[τ α^{τ−1}] = (1−√(1−α²))/(α²√(1−α²)) → ∞` as `α↑1`, so
**`P{τ<∞}=1` but `E τ = ∞`** (the walk eventually hits 1, but the expected waiting time diverges).

### 8.5 Strong Markov property; general first passage times
At `τ_1` the value `M_{τ_1}=1` is non-random, so by the **strong Markov property** the process restarts
and `τ_2 − τ_1` has the distribution of `τ_1`. Hence (p-104)
`E[α^{τ_2}|F_{τ_1}] = α^{τ_1}E[α^{τ_2−τ_1}]` and, generally,
**`E[α^{τ_m}] = ( (1−√(1−α²))/α )^m`** for the first passage to level `m`. **(Verified by vision on p-104.)**

### 8.6–8.7 Example: the perpetual American put (binomial)  — p-104…p-107
Binomial model with `u=2, d=1/2, r=1/4, p̃=q̃=1/2`, payoff `(5−S_k)⁺` (strike `K=5`), so
`S_k = S_0·2^{M_k}` with `M_k` a symmetric walk *under the risk-neutral measure* `P̃`; discount factor
`1/(1+r)=4/5`. **(Verified by vision on p-104 and p-105.)** Value under exercise rules (at `S_0=4`):
- **Rule 0** — stop immediately: value `(5−4)=1`.
- **Rule 1** — stop as soon as the price falls to 2 (`τ = min{k : M_k=−1}`):
  `V = Ẽ[(4/5)^τ (5−S_τ)⁺] = 3·Ẽ[(4/5)^{τ_1}] = 3·(1/2) = 3/2`
  (using `E α^{τ_1}=(1−√(1−α²))/α` with `α=4/5` → `(1−3/5)/(4/5)=1/2`).
- **Rule 2** — stop as soon as the price falls to 1 (`τ_{−2}`):
  `V = 4·Ẽ[(4/5)^{τ_2}] = 4·(1/2)² = 1`.
- **Optimal:** Rule 1, value **`3/2`** at `S_0=4` — exercise when the price falls to 2.
- For `S_0=8=2³` (needs two down steps): value `3·Ẽ[(4/5)^{τ_2}]=3·(1/4)=3/4`.
- **General (powers of 2, `j≥1`):** `v(2^j) = 3·(1/2)^{j−1}` (stop when price ≤ 2, i.e. `(j−1)` down
  steps). If `S_0=2^j≤2` (`j≤1`) one **exercises immediately**: `v(2^j)=5−2^j`.
- **Three-part verification** (Ch 8.7, as for any candidate American value `v(S_k)`): show
  (a) `v(S_k) ≥ (5−S_k)⁺`; (b) `{(4/5)^k v(S_k)}` is a supermartingale; (c) `{v(S_k)}` is the **smallest**
  process with (a)+(b). In fact `v(S_k)` is the value of the explicit rule "exercise the first time
  `S ≤ 2`," so (c) is automatic and only (a),(b) are checked. Numeric gap checks on p-107: the
  supermartingale inequality is an **equality** in the continuation region, at `S_0=4` (`x=4≥3`):
  `(4/5)[½v(8)+½v(2)] = (4/5)[½·(3/4)+½·3] = 3/2 = v(4)`; the gap is `4/5` at the boundary `S_0=2` where
  `v(2)=3 > (4/5)[½v(4)+½v(1)] = (4/5)(11/4) = 11/5` (value already at intrinsic, so one exercises), and
  the gap is `1` in the deep exercise region `S_0≤1` — a genuine strict supermartingale inequality
  wherever the option is exercised early.

### 8.8 Difference Equation (continuous value function) — p-108
Idealizing to *all* `x>0`, the perpetual-put value `v(x)` should satisfy
(a) `v(x) ≥ (K−x)⁺` ∀x;
(b) `v(x) ≥ (1/(1+r))[ p̃ v(ux) + q̃ v(dx) ]` ∀x;
(c) at each `x`, **either** (a) or (b) holds with equality.
For `K=5, u=2, d=1/2, r=1/4` (`p̃=q̃=1/2`) the candidate is the **piecewise function**
**`v(x) = { 6/x  for x ≥ 3;  5−x  for 0 < x ≤ 3 }`** (kink at `(x,v)=(3,2)`; `6/3=2=5−3`).
Note `6/x` on `x=2^j` (`j≥1`) reproduces `3(1/2)^{j−1}`, and `5−x` reproduces immediate exercise below
the threshold. The supermartingale inequality (b) holds with strictness exactly outside `2<x<4`, matching
the free-boundary picture. **(Piecewise formula and conditions (a)(b)(c) verified by vision on p-108.)**

### 8.9–8.10 Distribution of τ and the Reflection Principle — p-109…p-112
- **Distribution of the first passage time to 1** (must occur at an odd time `2j−1`):
  `P{τ=1} = 1/2`, and for `j=2,3,…`
  **`P{τ=2j−1} = (1/2)^{2j−1} · (2j−2)!/( (j−1)! · j )`**  [= `(1/2)^{2j−1}·(1/j)·C(2j−2,j−1)`].
  Numeric check: `j=2` gives `(1/2)³·(2!)/(1!·2)=1/8` — the single path `T H H` of length 3 that first
  hits +1 at time 3, out of 8 equally likely paths. (Formula confirmed from text pp. 110–112.)
- **Reflection principle** (Fig 8.5, 8.6; §8.10): to count the paths reaching level 1 by time `2j−1`,
  count all with `M_{2j−1}=1` and double-count all with `M_{2j−1} ≥ 3` (reflecting across level 1 maps
  each "hits 1 and ends ≥ 3" path to an "ends ≤ −1" path):
  **`P{τ ≤ 2j−1} = P{M_{2j−1}=1} + 2P{M_{2j−1}≥3} = 1 − P{M_{2j−1}=−1}`**.
  - Why the final form: by symmetry `P{M≥3}=P{M≤−3}` and the three disjoint events
    `{M=1},{M≥3},{M≤−3}` exhaust everything but `{M=−1}`, giving the `1−P{M_{2j−1}=−1}` expression.
  - Distribution from differences:
    `P{τ=2j−1} = P{τ≤2j−1} − P{τ≤2j−3} = P{M_{2j−3}=−1} − P{M_{2j−1}=−1}`,
    then binomial counting at times `2j−3` and `2j−1` produces the `(1/2)^{2j−1}(2j−2)!/((j−1)!j)` form.

---

## Corrections / errata flagged against the existing `shreve.md` Ch 5–8 sections

The extraction's Ch5–8 formulas were verified **correct**; no transcription is numerically wrong. Points
to record as corrections/clarifications:

1. **Chapter identity (naming) mismatch (the only substantive issue).** `shreve.md`'s "Ch 5–8" are the
   *lecture-edition* chapters (Stopping Times & American / Properties of American / Jensen / Random
   Walks) on PDF pp. 78–114. These do **not** correspond to standard Shreve I Ch 5–8 titles. If the Atlas
   expects the four standard chapters (Random Walk, Interest-Rate-Dependent Assets, Toward Continuous-Time,
   General Probability), three of them are *not* on pp. 78–114: Interest-Rate and Toward-Continuous are in
   the continuous-time half; General Probability is in lecture Ch 1 §1.4. Only **Random Walk** overlaps.
2. **Perpetual-put parameter set was implicit** in `shreve.md` (line 104). Pin it down:
   `u=2, d=1/2, r=1/4` (`(1+r)=5/4`), `K=5`, `p̃=q̃=1/2`, `S_k=S_0·2^{M_k}`; optimal rule is "exercise the
   first time the price is **at or below 2**" (not merely "falls to 2" — for `S_0≤2` one exercises
   immediately, value `5−S_0`); rigorous analysis restricted to `S_0=2^j`.
3. **Perpetual-put continuous formula (line 104) is right but should state the kink:** `v(x)=6/x` for
   `x≥3` and `v(x)=5−x` for `0<x≤3`, meeting at `(3,2)`; and the supermartingale inequality (b) is strict
   (value > continuation) precisely in `2<x<4` (the exercise region near the boundary).
4. **Add the general first-passage moment** `E[α^{τ_m}] = ((1−√(1−α²))/α)^m` (extraction only gives the
   `m=1` case) and record that it comes from the strong Markov property + taking-out-what-is-known.
5. **Minor labeling:** `shreve.md` line 70 states the optional-sampling equality for martingales; note the
   book states Theorem 3.17 for submartingales (`≤`) and derives the martingale equality as the special
   case — identical content, keep as is.
6. **Clarify Definition 6.1(a)** carries the explicit factor `(1+r)^k` outside the conditional maximum
   (`V_k = (1+r)^k max_{τ≥k} Ẽ[(1+r)^{−τ}G_τ|F_k]`), matching `shreve.md` line 79's `V_0` form.

**Verified by direct vision_analyze of rendered PNGs:** p-099 (exponential martingale / `P{τ<∞}=1`),
p-101 (Eq. 2.3, `E[α^τ]`), p-102 (quadratic solve, `E α^τ = (1−√(1−α²))/α`, `Eτ=∞` derivative),
p-104 (`E α^{τ_m}` strong Markov, perpetual-put binomial setup), p-105 (perpetual-put rule values `3/2`, `1`),
p-108 (`v(x)=6/x`/`5−x`, difference-equation conditions). Text of pp. 110–112 cross-checked the reflection
principle and first-passage distribution. Source files were **not** modified.
