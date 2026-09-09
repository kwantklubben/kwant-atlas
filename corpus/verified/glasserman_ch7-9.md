# Glasserman, *Monte Carlo Methods in Financial Engineering* (Springer 2004)
# Chapters 7–9 — Math-Verified Deep-Read (vision + OCR cross-checked)

**Scope of this verification pass:** Chapters 7 (Estimating Sensitivities), 8 (Pricing American
Options by Simulation), 9 (Applications in Risk Management).
**Printed page range:** Ch 7 = pp. 377–420; Ch 8 = pp. 421–479; Ch 9 = pp. 481–537.
**Rendered-page (PNG) mapping:** PNG index = printed page + 14 (verified visually: PNG p-391 = printed 377,
p-485 = printed 471). So Ch7 ≈ PNG 391–434, Ch8 ≈ PNG 435–493, Ch9 ≈ PNG 495–551.
**Verification method:** read of `/tmp/atlas_pages/glasserman/*.png` (vision) cross-checked against the
high-fidelity OCR in `/tmp/atlas_extract/glasserman.txt`. Two independent vision reads (p-392 §7.1,
p-485 §8.7) confirmed the OCR reproduces the printed equations faithfully, incl. eq. numbering
(7.1)–(7.3), (8.58)–(8.61). OCR text layer is treated as reliable; notation below follows the book.
**Output is an independent corrected/verified extraction of the existing `/tmp/atlas_extract/montecarlo.md`
Ch7–9 sections.** Errors/gaps found there are listed at the end. Sources were NOT modified.

Notation shared by all three chapters: α(θ)=E[Y(θ)] price to be differentiated; X_i = X(t_i) state at i-th
exercise date; h_i, V_i, C_i discounted payoff / value / continuation value (time-0 dollars) under the
normalized DP recursion V_i = max(h_i, E[V_{i+1}|X_i]); L = portfolio loss over horizon Δt.

---

# CHAPTER 7 — Estimating Sensitivities ("Greeks")  (printed 377–420)

α(θ)=E[Y(θ)], θ any market/model parameter (θ=S_i(0) ⇒ α′ = delta, α″ = gamma; θ=vol ⇒ vega).
Two families: (i) finite differences — biased, need bias/variance balance; (ii) exact differentiation
(pathwise vs likelihood-ratio) — unbiased when applicable.

## 7.1 Finite-difference approximations (pp. 378–385)

Forward (7.1):  Δ̂_F(n,h) = [Ȳ_n(θ+h) − Ȳ_n(θ)]/h.  E = h⁻¹[α(θ+h)−α(θ)] (7.2).
Bias forward (7.3):  Bias(Δ̂_F) = ½ α″(θ) h + o(h).
Central (7.4):      Δ̂_C = [Ȳ_n(θ+h) − Ȳ_n(θ−h)]/(2h).
Bias central:       o(h); if α thrice diff., Bias(Δ̂_C) = (1/6) α‴(θ) h² + o(h²)   (7.6).

Variance: Var(Δ̂_F) = h⁻² Var(Ȳ_n(θ+h) − Ȳ_n(θ)) (7.7). For i.i.d. pairs, Var = n⁻¹ Var[Y(θ+h)−Y(θ)],
which is (7.8):
  Case (i)  O(1)      — independent sampling at θ, θ±h
  Case (ii) O(h)      — common random numbers (same U-stream)
  Case (iii) O(h²)    — common RN **and** output Y(·,ω) continuous in θ (only pathwise-valid region)
⇒ generic model Bias = b h^β, Var = σ²/(n h^η) (7.9): forward β=1, central β=2; η=2 (i) or η=1 (ii).

**Optimal MSE (7.1.2, pp. 381–383).** Choose h_n = h* n^−γ with γ = 1/(2β+η) (7.10); MSE = b²h_n^{2β} + σ²/(n h_n^η)
(7.11); RMSE = O(n^{−β/(2β+η)}); optimal h* = [ησ²/(2β b²)]^{1/(2β+η)}. CLT:
n^{β/(2β+η)}(Δ̂−α′(θ)) ⇒ N(b h*^β, σ²/h*^η). Table 7.1:

| Estimator | Var | Bias | h_n | RMSE |
|---|---|---|---|---|
| Δ̂_F,i  (forward, indep) | σ²/nh² | ½α″h | O(n^{−1/4}) | O(n^{−1/4}) |
| Δ̂_C,i  (central, indep) | σ²/nh² | (1/6)α‴h² | O(n^{−1/6}) | O(n^{−1/6}) |
| Δ̂_F,ii (forward, CRN)  | σ²/nh | ½α″h | O(n^{−1/3}) | O(n^{−1/3}) |
| Δ̂_C,ii (central, CRN)  | σ²/nh | (1/6)α‴h² | O(n^{−1/5}) | O(n^{−2/5})   ← asymptotically best

σ_{F,i}² = 2Var[Y(θ)]; σ_{C,i}² = Var[Y(θ)]/2 (denominator 2h). Case (iii): no bias–variance tradeoff, RMSE O(n^{−1/2}).

**Extrapolation (p.384):** (4/3)Δ̂_C,ii(n,h) − (1/3)Δ̂_C,ii(n,2h) removes the O(h²) bias ⇒ bias O(h⁴),
RMSE O(n^{−4/9}) with h=O(n^{−1/9}) (near 1/√n).
**Second derivatives (p.385):** central Δ̂Γ = [Ȳ(θ+h) − 2Ȳ(θ) + Ȳ(θ−h)]/h², bias O(h²); variance
O(h^{−4}) indep., O(h^{−3}) CRN ⇒ RMSE O(n^{−2/7}) — 2nd derivatives are fundamentally harder than 1st.
**Multiple parameters (pp.385–386):** m-dim θ needs 2m+1 (central) / m+1 (forward) parameter values, O(m²)
for all Γ_ij — motivates response-surface / first & second order models ΔY=Σβ_i h_i (+Σβ_ij h_i h_j) (7.13/7.14).

## 7.2 Pathwise derivative estimates (IPA)  (pp. 386–401)

α′(θ) = E[Ẏ(θ)], Ẏ(θ)=dY(θ,ω)/dθ with the random-number stream ω held fixed (7.15). Valid iff the
interchange (7.16) E[dY/dθ]=dE[Y]/dθ holds; requires uniform integrability of difference quotients.

Canonical estimators (all on one simulated path, small extra cost, no bias, low variance):
- **Call delta (Ex. 7.2.1):** dY/dS(0) = e^{−rT} [S(T)/S(0)] 1{S(T)>K}; mean = BS delta Φ(d). (7.20)
- **Vega (call):** dY/dσ = e^{−rT}(−σT + √T·Z) S(T) 1{S(T)>K}; equivalently
  e^{−rT} [log(S(T)/S(0)) − (r+½σ²)T]/σ · S(T)·1{S(T)>K} — form independent of simulation scheme.
- **Asian delta:** 1{S̄>K} e^{−rT} S̄/S(0), S̄=mean S(t_i). **Lookback put delta:** Y/S(0).
- **Max-of-d assets (Ex.7.2.4):** ∂Y/∂S_i(0) = e^{−rT} [S_i(T)/S_i(0)] 1{S_i>max_{j≠i}S_j, S_i>K}.
- **General SDE (7.2.3):** Euler-differentiate the discretization; pathwise derivative recursion (7.24)
  Δ̂(i+1)=Δ̂(i)[1+a′(X̂(i))h+b′(X̂(i))√h Z_{i+1}], Δ̂(0)=1; continuous-time analogue dΔ = a′(X)Δ dt + b′(X)Δ dW (7.25).
  Cost-saving approximations: freeze a′,b′ at time-0 (or update every k steps).
- **Square-root / CIR (Ex.7.2.5):** X(t)∼c1·χ²_ν(c2 X(0)); recursion for dX(t_i)/dX(0) through (7.22).
- **Smoothing (pp.399–401):** digital & barrier payoffs can be made pathwise-tractable by conditioning:
  digital: E[Y|S(T−ε)] gives density-based term (1/(S σ√ε)) φ(...); barrier knock-out: change to the
  *conditioned* (never-crossing) process S̃ with likelihood-ratio = product of one-step survival probs (7.30).

**Unbiasedness conditions (7.2.2, pp.393–396).** Y(θ)=f(X_1(θ),…,X_m(θ)); require:
(A1) each X_i(θ) differentiable a.s.; (A2) P(X(θ) ∈ D_f)=1; (A3) **f Lipschitz** (|f(x)−f(y)|≤k_f‖x−y‖);
(A4) X_i Lipschitz in θ with integrable κ_i. Then pathwise Ẏ unbiased, and (A4) with E[κ²]<∞ ⇒ Case (iii).

**Failure modes.** Digital payoff ⇒ pathwise derivative exists a.s. yet is **zero and uninformative**
(genuine delta comes from the strike-crossing that pathwise misses). Same for barriers (knock in/out)
and for **gamma** of any discontinuous-of-derivative payoff: the derivative of a call payoff is a digital.
Rule of thumb: pathwise applies when payoff is continuous in the parameter (Lipschitz); fails for digitals,
barriers, and generally 2nd derivatives.

## 7.3 Likelihood-Ratio (score-function) method  (pp. 401–418)

Differentiate the density, not the payoff. E_θ[Y]=∫f(x)g_θ(x)dx; (7.31) d/dθ = ∫f(x)(dg_θ/dθ)dx; (7.32)
estimator  **f(X)·ġ_θ(X)/g_θ(X)**,  ġ = dg_θ/dθ, score = d log g_θ/dθ = ġ_θ/g_θ. No smoothness needed in f.

- **BS delta (Ex.7.3.1):** estimator e^{−rT}(S(T)−K)⁺ · Z/(S(0) σ √T) (7.34); score Z/(S(0)σ√T). Vega score = Z²/σ − √T Z − 1/σ. Same score works for any payoff (e.g. digital delta). Score has mean 0.
- **Asian delta (Ex.7.3.2):** score = Z_1/(S(0)σ√t_1) — only the first transition's density carries S(0). (7.36)
- **Asian vega (Ex.7.3.3):** score = Σ_j [(Z_j²−1)/σ − Z_j√(t_j−t_{j−1})] — all m transitions contribute. (7.37)
- **Gaussian vectors (Ex.7.3.4):** X∼N(µ(θ),Σ): score (X−µ)ᵀΣ⁻¹µ̇(θ) (7.38); for Σ(θ):
  score = −½tr(Σ⁻¹Σ̇) + ½(X−µ)ᵀΣ⁻¹Σ̇Σ⁻¹(X−µ) (7.39). Multiasset delta uses i-th component of ZᵀA⁻¹/(S_i(0)√T).
- **Square-root diff (Ex.7.3.5):** reduce noncentral-χ² to normal-with-random-mean representation; score ∝ √(c2 X(0)) scale.
- **Gamma (7.3.3):** 2nd-derivative estimator **f(X)·g̈_θ(X)/g_θ(X)** (7.44), g̈=d²g/dθ². BS gamma:
  g̈/g = [ζ²−1]/(S(0)²σ²T) − ζ/(S(0)²σ²T) with ζ=Z (7.45). Gaussian (mean): g̈_µ/g_µ = [(X−µ)²−σ²]/σ⁴.
  Mixed PW/LR & LR/PW estimators give much lower variance than pure LR for gamma (Table 7.2).

**Bias & variance (7.3.2).** Valid = limit of importance-sampling differences (7.41); needs absolute
continuity (g_θ+h a.c. w.r.t. g_θ). Counterexample U(0,θ) gives score −1/θ, wrong-sign estimate −½ vs true ½
(p.407). Rank-deficient normal (Σ singular) breaks LR. Score variance grows as t_1↓0 (path-start singularity),
grows with #dates m (score is a martingale, variance ↑ with steps), and explodes when measures become mutually
singular (Girsanov, vol change over [0,T]). Score is mean-zero ⇒ usable as a control variate.

---

# CHAPTER 8 — Pricing American Options by Simulation  (printed 421–479)

Value = sup_τ E[U(τ)] over stopping times, U discounted exercise payoff; Bermudan = finite exercise dates
t_1<…<t_m (0 excluded). DP (8.6–8.7): V_m=h_m, V_i(x)=max{h_i(x), E[V_{i+1}(X_{i+1})|X_i=x]}.
Continuation values (8.11): C_i(x)=E[V_{i+1}(X_{i+1})|X_i=x], C_m≡0; C_i=E[max(h_{i+1},C_{i+1})|X_i=x] (8.12).
Stopping rule from approximate continuation values (8.13): τ̂=min{i: h_i(X_i) ≥ Ĉ_i(X_i)}.
American put: τ*=inf{t≥0: S(t)≤b*(t)} for an optimal boundary b* (8.3).

**Theme (p.421, restated throughout):** high bias ⇐ using future info (backward induction over a finite path
set / Jensen); low bias ⇐ suboptimal exercise rule. Separating them yields an interval straddling the price.

## 8.1–8.2 Problem formulation & parametric approximations (pp. 421–430)

Parametric class of stopping rules τ_θ: V_0^θ = sup_θ E[h_{τ(θ)}]. Since Θ ⊂ admissible T: **V_0^θ ≤ V_0**
(LOW, suboptimality, 8.14). In-sample estimator V̂_0^{θ̂} = max over θ of sample means is biased **HIGH** w.r.t.
V_0^θ by Jensen (E[max] ≥ max E) (8.15). ⇒ meta-algorithm: (1) simulate n_1 paths; (2) optimize θ̂;
(3) **second independent pass** at fixed θ̂ gives E[V̂_0^{θ̂}]=V_0^{θ̂} ≤ V_0 — genuinely LOW-biased.
So a *sound* parametric implementation is only guaranteed low-biased after the second pass (Broadie–Glasserman 65,66).
Optimization decomposes into m−1 sequential 1-D searches (Andersen threshold rules, Bermudan swaptions);
parametric **value-function** form C_i(x,θ_i)=Σ θ_ij ψ_j(x) (basis functions) is the §8.6 prototype.

## 8.3 Random tree methods (pp. 430–440) — Broadie–Glasserman 65

Branching parameter b≥2; tree depth m ⇒ b^m nodes (**exponential in m**, practical only m≲5). Backward DP with
equal branch weights (8.20) = **high** estimator: E[V̂_i|node] ≥ V_i (8.21, Jensen). Low estimator (8.23–8.25):
use all-but-one successors to decide exercise, the left-out one to value continuation, average over all b
leave-one-out choices ⇒ **low** estimator v̂. Both converge to V_0 as b→∞ and are (per node) contraction-stable
(|max(a,c1)−max(a,c2)|≤|c1−c2|, 8.22). n i.i.d. trees ⇒ conservative ~90% CI
[v̄−z s_v/√n, V̄+z s_V/√n] that tightens to V_0. Depth-first storage O(mb+1) nodes; pruning where exercise is
suboptimal + antithetic branching + European control variates (Broadie–Glasserman–Kou 69).

## 8.4 State-space partitioning (pp. 441–443)

Partition state space into cells A_i1..A_ib_i; approximate transition probs p_ijk=P(X_{i+1}∈A_{i+1,k}|X_i∈A_ij)
and averaged payoffs h_ij=E[h_i|X_i∈A_ij] estimated by simulation; finite DP V_ij=max{h_ij,Σ_k p_ijk V_{i+1,k}}
(8.26). First phase biased high (Jensen); second phase = implementable suboptimal stopping ⇒ low-biased.
Exponential in dimension d ⇒ not for high-dim problems (Barraquand–Martineau; Bally–Pagès quantization).

## 8.5 Stochastic mesh (pp. 443–459) — Broadie–Glasserman 66

Keep b nodes per time step (mesh, not tree): generate independent paths then interconnect all nodes at
consecutive steps. Backward recursion (8.27): V̂_ij = max{h_i(X_ij), (1/b)Σ_k W^i_{jk} V̂_{i+1,k}};
root V̂_0 = (1/b)Σ_k V̂_{1k} (8.28). Weights W^i_{jk} must satisfy conditions:
(M1) Markovian mesh ({X_0..X_{i-1}} ⟂ {X_{i+1}..X_m} | X_i); (M2) W^i_{jk} deterministic fn of X_i, X_{i+1};
(M3) (1/b)Σ_k E[W^i_{jk} V_{i+1}(X_{i+1,k})|X_i] = C_i(X_ij) — weighted avg = true continuation value in expectation.
(M1)–(M3) ⇒ mesh estimator biased **high** (Jensen, pp.446–447).

**Low estimator (8.32–8.34):** extend weights W^i_k(x) to all states; continuation Ĉ_i(x)=(1/b)Σ W^i_k(x)V̂_{i+1,k};
simulate independent path; stop at τ̂=min{i:h_i(X_i)≥Ĉ_i(X_i)}; v̂=h_{τ̂}(X_{τ̂}) — LOW (any policy ≤ optimal).

**Likelihood-ratio weights (8.5.2).** Nodes at i+1 have density g (e.g. marginal g_{i+1}); want weights making
(1/b)ΣW·V̂ → ∫ V_{i+1}(y) f_{i+1}(X_ij,y) dy = C_i(X_ij). Hence (8.36) W^i_{jk}= f_{i+1}(X_ij, X_{i+1,k})/g(X_{i+1,k}).
LR weights are the only *completely general* weights (Radon–Nikodym uniqueness, 8.37). Concrete variants:
- independent-path (8.38): W=1 on k=j; f_{i+1}(X_ij,·)/g_{i+1}(·) else.
- (8.39): W^i_{jk}= f_{i+1}(X_ij,X_{i+1,k}) / [g_i(X_ik) f_{i+1}(X_ik,X_{i+1,k})], k≠j.
- (8.41) averaging / stratified draw: W^i_{jk}= f_{i+1}(X_ij,X_{i+1,k}) / [(1/b)Σ_ℓ f_{i+1}(X_iℓ,X_{i+1,k})];
  has the attractive "sum into a node" property (1/b)Σ_j W^i_{jk}=1 (8.42), which replaces exponentially-growing
  product-of-weights variance with constant 1 for European payoff.
**Costs:** mesh O(mb²); each low-estimator path O(mb). Fast Gauss transform → O(mb) (Broadie–Yamamoto 70).
When no transition density: constrained weights (Broadie et al. 68) via known conditional expectations g(x)=E[G(X_{i+1})|X_i=x] with constraints (1/b)Σ W G = g(X_ij) (8.44), ΣW=b (8.45), min convex H (quadratic or entropy).

**Interleaving estimator (p.449, Longstaff–Schwartz form):** V̂_ij = h_{τ̂_i}(X̃_{τ̂_i}) where if at a node
h_i < Ĉ_i you continue by *simulating forward from that node* under the estimated policy; blends high & low bias.

## 8.6 Regression-based methods & weights (pp. 459–470)

Continuation value is the regression E[V_{i+1}(X_{i+1})|X_i=x] on current state. Model (8.46–8.47):
C_i(x)=β_iᵀψ(x), ψ basis fns; β_i = (E[ψ(X_i)ψ(X_i)ᵀ])⁻¹ E[ψ(X_i)V_{i+1}(X_{i+1})] = B_ψ⁻¹ B_ψV (8.48).
LS estimate β̂_i=B̂_ψ⁻¹ B̂_ψV from pairs (X_ij, V̂_{i+1,j}) with B̂_ψ, B̂_ψV sample moments (8.49); continuation Ĉ_i(x)=β̂_iᵀψ(x) (8.50).

**Two distinct estimators — keep separate:**
- **Regression DP (Tsitsiklis–van Roy):** V̂_ij=max{h_i(X_ij), Ĉ_i(X_ij)} (8.51) then average. Generally biased
  **high** when basis is imperfect (uses fitted continuation to both decide and value).
- **Longstaff–Schwartz LSM (8.52):** V̂_ij = h_i(X_ij) if h_i≥Ĉ_i(X_ij) else V̂_{i+1,j} (take value from the *realized*
  continuation path = "interleaving"); omit OTM nodes h_i=0 in the regression. **Low-biased.** (Clément–Lamberton–Protter 86:
  limit = true price iff (8.46) holds exactly, else suboptimal ⇒ low.)

**Regression ⇔ implicit mesh weights (8.6.2):** Ĉ_i(X_ij)=(1/b)Σ_k W^i_{jk}V̂_{i+1,k} with
W^i_{jk}=ψ(X_ij)ᵀ B̂_ψ⁻¹ ψ(X_ik)  (8.54); with a constant basis function this is
W^i_{jk}=1 + b/(b−1)·(ψ(X_ij)−ψ̄)ᵀ S_ψ⁻¹(ψ(X_ik)−ψ̄)  (8.56) — weights symmetric, can be negative, "price"
exactly only functions linear in the basis. Note: regression weights connect X_ij↔X_ik (same time step, via the
mesh of *upstream* states) whereas LR weights connect X_ij↔X_{i+1,k}. Cost O(Mb) per step vs O(b²) for general mesh.

Numerical test (Ex. 8.6.1, two-asset max option, true 13.90 at S0=100): regression-DP overestimates unless basis
includes interaction S1S2, max(S1,S2), h̃; low & LSM ≈ and accurate; include max{0,Ĉ} and exercise only if h>Ĉ.

## 8.7 Duality — upper bounds (pp. 470–478) — Rogers 308 / Haugh–Kogan 172

Primal V_0(X_0)=sup_τ E[h_τ(X_τ)]. For any martingale M with M_0=0, optional sampling ⇒ E[h_τ]≤E[max_{k=1..m}(h_k(X_k)−M_k)];
taking sup on the left and inf over such M (8.58):
**V_0(X_0) = sup_τ E[h_τ(X_τ)] = inf_M E[ max_{k=1..m} (h_k(X_k) − M_k) ],  M martingale, M_0=0**
(equality attained). Optimal M built from value process via martingale differences
Δ_i = V_i(X_i) − E[V_i(X_i)|X_{i-1}] (= V_i − C_{i-1}(X_{i-1}), 8.59/8.64), M_i=Σ_{s≤i}Δ_s, M_0=0 (8.60), E[Δ_i|X_{i-1}]=0 (8.61);
then V_0(X_0)=max_{k=1..m}(h_k(X_k)−M_k) (8.63) so equality is attained. Any near-optimal M̂ gives a valid **upper bound**
V_0 ≤ E[max_k(h_k−M̂_k)] (8.65).
Practical martingales from: (i) **approximate value function** Ĉ_i, V̂_i=max{h_i,Ĉ_i}: use Δ̂_i=V̂_i(X_i)−E[V̂_i(X_i)|X_{i-1}]
estimated by **nested single-step** simulation (8.66–8.67) — still martingale differences even for finite n ⇒ guaranteed upper bound.
(ii) **stopping rules** τ_i (Andersen–Broadie): Δ̂_i=E[h_{τ_i}(X_{τ_i})|X_i]−E[h_{τ_i}(X_{τ_i})|X_{i-1}] (8.69), with
E[h_{τ_i}|X_i]=h_i(X_i) if h_i≥Ĉ_i else E[h_{τ_{i+1}}|X_i] (8.70); subpaths follow the policy (random number of steps).
Regression link: if C_i is exactly linear in basis (8.46), the regression residual Δ_{i+1}=V_{i+1}−βᵀψ(X_i) IS the optimal
martingale difference; otherwise residuals only approximate it (explains Table 8.3: dual helps most when basis is poor).

---

# CHAPTER 9 — Applications in Risk Management  (printed 481–537)

Market risk: S = vector of m prices/rates, ΔS change over horizon Δt (2 weeks reg.), loss L=−ΔV = V(S,t)−V(S+ΔS,t+Δt).
Distribution objective/real-world for ΔS, risk-neutral for revaluation. VaR p: P(L>x_p)=p (p=0.01 ⇒ 99% VaR);
quantile of loss, not subadditive (Artzner et al.), whereas conditional excess E[L|L>x] is coherent.

## 9.1 Loss probabilities & Value-at-Risk (pp. 481–492)

**Normal linear (delta) model:** ΔS∼N(0,Σ_S), ΔV=δᵀΔS (9.1) ⇒ L normal.
**Delta-gamma (9.2):** ΔV ≈ (∂V/∂t)Δt + δᵀΔS + ½ΔSᵀΓΔS, δ_i=∂V/∂S_i, Γ_ij=∂²V/∂S_i∂S_j. With ΔS=CZ, CCᵀ=Σ_S,
choose C to diagonalize: −½CᵀΓC = Λ=diag(λ_1..λ_m) (λ_j = eigenvalues of −½ΓΣ_S), b=−Cᵀδ:
(9.4)  **L ≈ Q = a + Σ_{j=1..m}(b_j Z_j + λ_j Z_j²),  a=−(∂V/∂t)Δt.**
**MGF/CGF of Q (9.5):** ψ(θ)=aθ + ½Σ_j[θ²b_j²/(1−2θλ_j) − log(1−2θλ_j)], valid max_j θλ_j<1/2; characteristic fn
φ̂(u)=e^{ψ(iu)}; invert to get P(Q≤x) via inversion integral (9.6) (Abate–Choudhury–Whitt; Rouvinez).

**MC estimation of P(L>x):** plain avg of 1{L_i>x}. Historical sim = special case. **Quantile estimation:**
empirical quantile x̂_p=F̂^{-1}_{L,n}(1−p); CLT (9.7): √n(x̂_p−x_p) ⇒ N(0, p(1−p)/f(x_p)²) — density in denominator
magnifies variance for extreme p; nonparametric order-statistic CI [L_(r),L_(s)) with binomial coverage.

## 9.2 Variance reduction via the delta-gamma approximation (pp. 492–506) — GHS 142,143,144

**CV (9.9):** p̂_cv = (1/n)Σ1{L_i>x} − β̂[(1/n)Σ1{Q_i>y} − P(Q>y)] (exact P(Q>y) from transform). Modest gains (2–5×);
weak because indicators 1{L>x},1{Q>y} poorly correlated in the far tail. Hesterberg–Nelson: equals weighted/poststratified estimator; gives quantile estimates at all x from one set of weights.

**Importance sampling — exponential twisting of Q:** measure dP_θ/dP = e^{θQ−ψ(θ)} (9.10); estimator e^{−θQ+ψ(θ)}1{L>x}.
2nd moment ≤ e^{−θx+ψ(θ)} (9.11). **Remarkable fact:** under P_θ, Z is still multivariate normal, *diagonal*:
(9.12) Z_j ~ N(µ_j(θ), σ_j²(θ)), µ_j(θ)=θb_j/(1−2θλ_j), σ_j²(θ)=1/(1−2θλ_j) — i.e. mean-shift in the b_j direction and
variance-inflation for λ_j>0 ("delta-only / gamma-only" tilting). Twisting parameter θ_x solves ψ′(θ_x)=x (9.15)
(= E_θ[Q]=x centers the loss). Asymptotically optimal: for λ_max=max_j λ_j>0,
P(Q>x)=exp(−½λ_max x+o(x)) and the IS 2nd moment = exp(−λ_max x+o(x)) (twice the rate ⇒ fastest possible).
Sampling: draw Z∼N(µ,Σ), set ΔS=CZ, revalue.

**Stratified IS (9.2.3):** strata from Q-distribution under P_θ via inversion (φ̂_θ(u)=e^{ψ(θ+iu)−ψ(θ)}, 9.18);
generate Z conditioned on Q∈A_k by acceptance–rejection (strata are ellipses in Z-space); combined estimator (9.17).
**Poststratification** alternative. Table 9.1: CV≈2–5×, IS≈7–27×, IS-S (stratified) up to ~173× at small p.

## 9.3 Heavy-tailed setting (pp. 506–520)

Tail classes by mgf existence: (i) light (normal/bounded); (ii) exponential tail (gamma, e.g. exp θ*x); (iii) heavy:
E[e^{θX}]=∞ ∀θ>0, moments finite for r<ν (stable/Pareto, regularly varying x^{−ν}). Student t_ν density ∝(1+x²/ν)^{−(ν+1)/2},
P(X>x)∼c·x^{−ν}; var ν/(ν−2) for ν>2; t = Z/√(Y/ν), Z∼N(0,1), Y∼χ²_ν. Multivariate t_ν,Σ density (9.19):
f ∝ (1+ xᵀΣ⁻¹x/ν)^{−(ν+m)/2}; representation (9.20–9.21): X = ξ/√(Y/ν) = AZ/√(Y/ν) (marginals t_ν, uncorrelated but NOT independent).
**t-copula (9.22):** allow different ν_i per marginal via X̃_i = F^{-1}_{ν_i}(F_ν(X_i)).

**Heavy-tail delta-gamma (9.3.2):** Q=a+Σ(b_j X_j+λ_j X_j²) (9.24), X multivariate t. No mgf (category iii) and no
independence of summands ⇒ **indirect delta-gamma**: define Q_x=(Y/ν)(Q−x)=Σ terms (9.25) so P(Q≤x)=P(Q_x≤0) (9.26).
Conditional on Y, Q_x is quadratic in independent normals ⇒ conditional mgf (9.27), and with φ_Y the mgf of Y:
mgf of Q_x: φ_x(θ)=φ_Y(α(θ))·∏_j (1−2θλ_j)^{−1/2}, α(θ)=(a−x)θ/ν + ½Σ θ²b_j²ν/(1−2θλ_j) (9.28–9.29); t-case φ_Y(θ)=(1−2θ)^{−ν/2}.

**Heavy-tail importance sampling (9.3.3):** can't twist Q (no mgf) — **twist Q_x**: dP_θ/dP=e^{θQ_x−ψ_x(θ)} (9.30);
θ_x minimizes ψ_x (root of ψ_x′(θ_x)=0). Under P_θ (Theorem 4.1 GHS 144): Y has density f_{Y,θ}(y)=e^{α(θ)y}f_Y(y)/φ_Y(θ)
(9.31) — for χ²_ν this is a gamma — and, given Y, Z_j∼N(µ_j,σ_j²) with (9.32) µ_j=θb_j(Y/ν)/(1−2θλ_j), σ_j²=1/(1−2θλ_j).
Sample Y→Z→X=Z/√(Y/ν)→ΔS=CX→L; estimator e^{−θ_x Q_x+ψ_x(θ_x)}1{L>x} (9.33). Asymptotically optimal (polynomial rate):
P(Q>x)=O(x^{−ν/2}), 2nd moment O(x^{−ν}) = twice rate. Stratify Q_x. Table 9.2: VR factors up to ~134 (IS-S), larger than in the normal case.

## 9.4 Credit risk (pp. 520–535)

**9.4.1 Default times & valuation.** Intensity λ: 1{τ≤t}−∫₀ᵗλ du is a martingale (9.35). Survival:
P(τ>T)=E[e^{−∫λ}] (9.36); defaultable zero-bond = E[e^{−∫(r+λ)}] (9.37) (discount at r+λ); Duffie–Singleton recovery ⇒
rate r+λ·L(u) (loss-given-default). Simulation of default from intensity: cumulative intensity ∫₀ᵗλ du exponential(1);
τ=inf{t: ∫₀ᵗλ du=ξ} (9.38). CIR default time closed form F_τ(t)=1−e^{A(t)+C(t)λ(0)} (9.39) ⇒ inverse-transform sample.
Ratings: Jarrow–Lando–Turnbull Markov chain, default intensity q(X(t),0).

**9.4.2 Dependent defaults.** Factor model (equity correlations / CreditMetrics, Gupton et al.): X_i=a_i1Z_1+…+a_ikZ_k+b_iε_i,
a_i·a_i+b_i²=1 (9.40). Default-time dependence: τ_i=F_i^{-1}(U_i), U_i=1−e^{−ξ_i} (9.41); **normal copula**
U_i=Φ^{-1}(X_i) (9.42); τ_i=F_i^{-1}(Φ(X_i)) (9.45, Li). General copula F(x)=C(F_1(x_1),…,F_m(x_m)),
C_F(u)=F(F_1^{-1}(u_1),…,F_m^{-1}(u_m)) (9.43–9.44).

**9.4.3 Portfolio credit risk.** L=Σ_i Y_i c_i, Y_i=default indicator, c_i=loss given default, marginal p_i.
Independent case: mgf of L = ∏_i[p_i e^{c_i θ}+(1−p_i)] (invert / saddlepoint). Equal p,c: twist each Y_i, likelihood
ratio e^{θL−mψ(θ)}; estimator (9.46); θ_x root of ψ′(θ_x)=x/m ⇒ E_θ[L]=x (9.47).
**Dependent (factor) case:** thresholds x_i=Φ^{-1}(1−p_i) (9.48); X=AZ+Bε (9.49), conditional default prob
p̃_i = P(Y_i=1|Z)=1−Φ((x_i−a_iZ)/b_i) (9.50). Conditional cumulant ψ_{L|Z}(θ)=Σ log[p̃_i e^{θc_i}+(1−p̃_i)] (9.51);
twist each obligor conditionally given Z to p̃_i(θ̃_x)=p̃_i e^{θ̃_x c_i}/(p̃_i e^{θ̃_x c_i}+1−p̃_i) (9.52) with ψ′_{L|Z}(θ̃_x)=x,
θ̃_x=max{0,θ}; estimator e^{−θ̃_x L+ψ_{L|Z}(θ̃_x)}1{L>x} (9.53). Then ALSO twist the factors Z to mean µ (likelihood ratio
e^{−µᵀZ+½µᵀµ}); combined estimator (9.55). Choice of µ: in the one-factor equi-ρ model µ rises from 0 (ρ=0) to
Φ^{-1}(1−p) (ρ=1, 9.57); VR factors 30–50 at p≈1%.

---

# ERRORS / GAPS FOUND IN EXISTING `/tmp/atlas_extract/montecarlo.md` Ch7–9 (and corrections applied above)

**Chapter 7**
1. Header "pp. 377–419" — chapter ends p.420 (7.4 Concluding Remarks; Ch8 opens 421). Cosmetic.
2. §7.1 "…jointly with h·√n tuned" is imprecise. Exact optimal scaling: independent-sampling forward/central h∝n^{−1/4}/n^{−1/6};
   common-random-number forward/central h∝n^{−1/3}/n^{−1/5}; the central+CRN estimator dominates (RMSE O(n^{−2/5})); Case (iii)
   gives RMSE O(n^{−1/2}) with no bias–variance tradeoff. Omitted: extrapolation ⇒ O(n^{−4/9}); second-derivative (gamma) FD
   RMSE O(n^{−2/7}); multi-parameter cost (2m+1 / O(m²) points). **Gap — added.**
3. §7.2 lists "max-of for some cases" among pathwise failures — **incorrect as stated.** Pathwise applies fine to max/lookback/
   Asian/spread (all Lipschitz payoffs, Ex. 7.2.2/7.2.4). What truly fails: digital payoffs (pathwise derivative is identically 0 —
   "spike"/strike-crossing term missed), barrier options, and generally gamma (2nd derivatives). The md's phrase "then the indicator
   term only works when the payoff derivative is a.s.-defined" garbles the real criterion (continuity/Lipschitz, conditions A1–A4). **Corrected.**
4. Missing: the pathwise estimators are single-path & low-variance; explicit vega/delta formulas and the smoothing-by-conditioning trick
   for digital/barrier (7.29/7.30) were absent. **Added.**
5. §7.3 gamma key-formula "∂²ln f/∂θ² + (∂ln f/∂θ)² term" is only loosely right. The LR 2nd-derivative estimator is
   f(X)·g̈_θ(X)/g_θ(X) (7.44); and the mixed PW/LR estimators are the low-variance practical choice for gamma. **Added precise forms.**
6. Missing throughout §7: the whole *scope/bias* story (absolute continuity in LR; score-martingale ⇒ variance grows with #dates;
   LR score variance ↑ as first transition gap t_1→0). **Added.**

**Chapter 8**
1. §8.2 "parametric …→ gives low-biased estimator" — **over-simplified/wrong.** In-sample θ̂-optimization is HIGH-biased (Jensen,
   8.15) relative to V_0^θ, and V_0^θ≤V_0 overall; only the second, independent pass (Step 3) is guaranteed low-biased. Direction of
   the two biases can't be assumed to cancel. **Corrected.**
2. §8.5: adds "general framework with weighted estimators" but omits the mesh recursion (8.27), the M1–M3 conditions, that the DP
   (mesh) value is biased HIGH by Jensen, and the LR-weight formulas (8.36/8.38/8.41) incl. the sum-into-a-node property (8.42).
   **Gap — added.**
3. §8.6 conflates the Tsitsiklis–van Roy regression DP estimator (max{h,Ĉ} — generally HIGH-biased) with Longstaff–Schwartz LSM
   (low-biased). These must be kept distinct. md's claim "regression ⇔ a particular implicit mesh weighting" is correct and now made
   explicit via W^i_jk=ψ(X_ij)ᵀB̂_ψ⁻¹ψ(X_ik) (8.54). md's β_i formula = (E[ψψᵀ])⁻¹E[ψ V_{i+1}] is correct (8.48). **Clarified.**
4. §8.7 duality formula is malformed/confusing ("min over martingale M of E[max(e^{−rt}h_t−M_t)] + E[M_0·…]").
   Clean statement (all variables already discounted, M_0=0): V_0=sup_τE[h_τ]=inf_M E[max_{k}(h_k−M_k)], M martingale with M_0=0;
   optimal M from Δ_i=V_i−E[V_i|X_{i-1}]. **Corrected.**
5. md doesn't mention the two practical martingale constructions (from approximate value fns via nested sim, 8.66; from stopping rules,
   8.69) nor the regression-residuals connection. **Added.**

**Chapter 9**
1. §9.1 "VaR=α-quantile of loss P(L≤VaR)=α": Glasserman defines the 99% VaR by P(L>x_p)=p (p=0.01) — an upper tail probability.
   The md's phrasing (L≤VaR) is the conventional complementary form; sign convention differs but equivalent. Flagged; kept both noted.
2. §9.2 diagonalization md "express loss via Σ(½λ_j z_j² + Δ_j z_j)" is the right idea; exact book form: L≈Q=a+Σ(b_jZ_j+λ_jZ_j²),
   λ_j = eigenvalues of −½ΓΣ_S, and the θ-twist keeps Z normal with shifted mean and inflated variance (9.12) — a fact md omits.
   **Added the twisted-parameters and asymptotic-optimality result (P(Q>x)=e^{−½λ_max x+o(x)}).**
3. §9.3 md "delta-gamma under heavy tails; VR that respects heavy tails" is hand-wavy. The mechanism is the **indirect** delta-gamma
   (Q_x, mgf via φ_Y, 9.25–9.29) and IS by twisting Q_x — not Q, which has no mgf — with Y twisted to a gamma and Z mean/variance
   changed given Y (9.31–9.32). **Added.**
4. §9.4 md "importance sampling / exponential tilting across the common factor" is directionally right but missing the concrete scheme:
   thresholds x_i=Φ^{-1}(1−p_i) (9.48), conditional default probs (9.50), conditional exponential twisting of the Yi given Z (9.52–9.53),
   and the additional factor-mean twist µ (9.55) with µ→Φ^{-1}(1−p) as ρ→1. **Added.**
5. md §9.4 wrongly frames credit-risk only as "dependent defaults / copulas" and "rare-event IS": the chapter's valuation half
   (default times via intensity, τ=inf{t:∫λ=ξ}, bond pricing at r+λ, ratings-transition intensity) was missing. **Added.**

Overall: existing extraction is broadly accurate on *which* method goes where and on narrative, but is too shallow on
conditions-for-validity and omits most concrete formulas, and contains two substantive mis-statements (pathwise applicability to
"max-of," §8.2 bias direction) and one malformed formula (duality). This file supersedes montecarlo.md Ch7–9 for math content.
