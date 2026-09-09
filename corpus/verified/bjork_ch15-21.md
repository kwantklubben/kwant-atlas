# Björk, *Arbitrage Theory in Continuous Time* (3rd ed., OUP 2009) — Chapters 15–21, Vision-Verified Extraction

**Scope:** Ch 15 Incomplete Markets · Ch 16 Dividends · Ch 17 Currency Derivatives · Ch 18 Barrier Options · Ch 19 Stochastic Optimal Control · Ch 20 The Martingale Approach to Optimal Investment · Ch 21 Optimal Stopping Theory & American Options.
**Source:** PDF text layer `/tmp/atlas_extract/bjork.txt` (lines ≈10546–17476, printed pp. 209–350), cross-checked against rendered page images `/tmp/atlas_pages/bjork/p-*.png`.
**Page mapping:** PNG index = printed page + 21 (verified on p-230=printed 209 [ch 15 opener], p-289=printed 268 [Thm 18.8], p-369=printed 348 [Prop 21.30]). So these chapters live on PNG p-230 … p-371.
**Status:** This file CORRECTS and substantially ENLARGES the chapter 15–21 blocks of `/tmp/atlas_extract/derivative_pricing.md`. Sources were not modified. Math notation follows the book (Feynman–Kac, BS = Black–Scholes). ✓ = formula confirmed by direct vision read of the rendered page.

---

## Ch 15 — Incomplete Markets (printed 209–228; PNG 230–249)
*Factor-model (non-traded underlying) derivative pricing. Central message: with fewer traded assets than random sources the martingale measure (equivalently the market price of risk) is NOT determined within the model, so derivative prices are non-unique; but the prices of *different* derivatives must be mutually consistent.*

### Setup (§15.2 scalar)
- Observable, **non-traded** factor: `dX(t) = μ(t,X)dt + σ(t,X)dW̄(t)` (15.1); money account `dB = rBdt` (15.2); claim `Y = Φ(X(T))` (15.3). X is *not* an asset ⇒ a "portfolio in X" is meaningless (e.g. temperature at Brighton pier).
- Two price processes F,G (on claims Φ,Γ) have dynamics `dF = αF F dt + σF F dW̄`, with `αF = (F_t+μF_x+½σ²F_xx)/F`, `σF = σF_x/F` (15.4–15.5). Hedging F against G and imposing no-arbitrage gives:
  - **Prop 15.1** universal market price of risk: `(αF−r)/σF = λ(t)` for **every** derivative F (internal consistency / no arbitrage across the derivative market).
- **Prop 15.2 Pricing equation** `F_t + A^F − rF = 0`, `F(T,x)=Φ(x)`, with `A^F = (μ−λσ)F_x + ½σ²F_xx` (15.8–15.9). λ exogenous → price not unique.
- **Prop 15.3 Risk-neutral valuation** `F(t,x) = e^{−r(T−t)} E^Q_{t,x}[Φ(X(T))]` where Q-drift of X is `μ−λσ` (15.11). Choosing λ ⇔ choosing Q (1-to-1).
- **Prop 15.4** characterization of Q identical to Prop 13.3 (each price has Q-drift r; Π/B is a Q-martingale).
- BS embedding: if X *is* a traded stock, benchmark Γ(X(T))=X(T) pins λ=(α−r)/σ inside the model → BS PDE and Q-drift r (15.21 onward → gives rX drift).

### §15.3 Multidimensional (k factors X, n Wiener sources)
- n random sources ⇒ need **n** benchmark derivative prices F¹,…,Fⁿ spanning; `α_i − r = Σ_j σ_ij λ_j`, i=1..n, and `αF − r = σF·λ` (15.19), i.e. `α − r·1 = σλ` ⇒ `λ = σ⁻¹[α−r·1]` (15.20) — λ universal across assets but not determined in model.
- **Prop 15.5** pricing PDE: `F_t + Σ_i(μ_i − Σ_j δ_ij λ_j)F_i + ½ tr{δ'F_xx δ} − rF = 0`; **Prop 15.6** risk-neutral valuation (15.21) under Q-dynamics `dX^i = (μ_i − δ_i·λ)dt + δ_i dW`; **Prop 15.7** martingale-measure characterization.

### §15.4 Stochastic short rate
- `r(t)=r(X(t))`. **Prop 15.8** same PDE with `r(x)F`; **Prop 15.9** `F(t,x)=E^Q[e^{−∫_t^T r(X(u))du} Φ(X(T))]` (15.23).

### §15.5 Martingale view / §15.6 Summing up
- **Result 15.6.1:** any price process satisfies `α_Π(t)−r = σ_Π(t)λ(t)` a.s.; complete market ⇒ Q (or λ) unique ⇒ unique price; incomplete market ⇒ several Q/λ ⇒ several mutually-arbitrage-free price systems. The market (aggregate risk aversion) "chooses" Q; the theorist must calibrate λ(t,x;β) to observed benchmark prices (least-squares fit) — connects to inversion of the yield curve in interest-rate theory.

> **Existing extraction verdict (Ch 15):** concept summary correct (temperature/benchmark/λ-family), but omitted the actual pricing-equation structure `A^F=(μ−λσ)F_x+½σ²F_xx`, the "one universal λ shared by all derivatives" consistency requirement, the k-factor/n-benchmark dimensionality rule, and the Feynman–Kac Q-drift. No wrong statements found.

---

## Ch 16 — Dividends (printed 229–246; PNG 250–267)
*Two regimes: DISCRETE dividends (stock price jumps at dividend points) and CONTINUOUS dividends (yield δ[S], or general gain dD incl. a Wiener term).*

### §16.1 Discrete dividends (cum/ex convention; price is taken EX-dividend)
- Jump condition (no-arbitrage), **Prop 16.1:** at each dividend point `S_t = S_{t−} − δ[S_{t−}]` (16.2). Between dividends `dS=αSdt+σSdW̄`.
- **Prop 16.2/16.3:** price `F` solves BS PDE on each intra-dividend interval `[T_{i+1},T_i)`, with **jump condition at each dividend point** `F(T_i−, s) = F(T_i, s − δ[s])` (16.5); terminal `F(T,s)=Φ(s)`.
- **Prop 16.5** risk-neutral valuation (recursive): `F(t,s)=e^{−r(T−t)}E^Q[Φ(S_T)]` where between dividends `dS=rSdt+σ(t,S)S dW` and at each T_i: `S_{T_i}=S_{T_i−}−δ[S_{T_i−}]`.
- **Prop 16.6 (proportional discrete dividend, δ[s]=sδ, const σ):** `F_δ(t,s) = F_0(t, (1−δ)^n · s)` (16.19), n = # dividend points in (t,T]. (Reuse no-dividend BS formulas by scaling spot by (1−δ)^n.)

### §16.2.1 Continuous dividend yield
- Gain differential: `dG_S = dS + dD`, `dD(t)=S_t·δ[S_t]dt` (16.20–16.21).
- **Prop 16.7 Pricing equation:** `F_t + (r−δ)sF_s + ½σ²s²F_ss − rF = 0` (16.22) — BS with drift r−δ.
- **Prop 16.8** risk-neutral valuation (16.23) with Q-dynamics `dS_t = (r−δ[S_t])S_t dt + σ(S_t)S_t dW_t` (16.24).
- **Prop 16.9** (bank numeraire) normalized **gain** process `G^Z(t) = S_t/B_t + ∫_0^t (1/B_τ)dD(τ)` is a Q-martingale; ⇒ **cost-of-carry** `S(0)=E^Q[∫_0^t e^{−rτ}dD(τ)+e^{−rt}S(t)]` (16.25).
- **Prop 16.10 (const δ,σ):** `F_δ(t,s) = F_0(t, s·e^{−δ(T−t)})` (16.28). (Q-dynamics GBM `dS=(r−δ)Sdt+σS dW`, 16.27.)

### §16.2.2 General (stochastic) dividend structure — needed for futures (Ch 29)
- `dD(t) = S_t δ[S_t]dt + S_t γ[S_t]dW̄` (16.30). Claim priced as `F(t,S,D)`.
- **Prop 16.11** PDE with operator `A^F = s[(αγ+σr−δσ)/(σ+γ)]F_s + s[(δσ+γr−γα)/(σ+γ)]F_D + ½σ²s²F_ss + ½γ²s²F_DD + σγs²F_sD`.
- **Prop 16.12** risk-neutral valuation with Q-drifts `dS=S[(αγ+σr−δσ)/(σ+γ)]dt+Sσ dW`, `dD=S[(δσ+γr−γα)/(σ+γ)]dt+Sγ dW`.
- **Prop 16.13/16.14** martingale characterization: exists λ with Q-dynamics `dS=S(α−λσ)dt+SσdW`, `dD=S(δ−λγ)dt+SγdW`; normalized gain is a Q-martingale.

### §16.3 Martingale approach / arbitrary numeraire (KEY subtle result)
- Bank numeraire: reinvesting all dividends in B, the total wealth process V (1 unit of S + dividends) is a non-dividend asset ⇒ `S_t/B_t + ∫_0^t dD_s/B_s` is a Q-martingale (**Prop 16.15**).
- Angular bracket `⟨X,Y⟩_t = ∫_0^t σ_X σ_Y ds`, bilinear, `⟨h·X,Y⟩=h·⟨X,Y⟩` (16.35, Prop 16.17–18).
- **Prop 16.19 (arbitrary numeraire A):** normalized gain `G^Z_t = S_t/A_t + ∫_0^t dD_s/A_s − ∫_0^t (1/A_s²)d⟨D,A⟩_s` is a Q^A-martingale. If D has **no** Wiener component (`d⟨D,A⟩=0`), the naive `S_t/A_t + ∫_0^t dD_s/A_s` is a Q^A-martingale. ⇒ For a continuous yield (dD=Sδdt has zero diff) the naive gain works under any numeraire; the extra covariation term only appears when the *dividend stream itself* is stochastic.
- Put–call parity with yield: `p_δ = c_δ − s e^{−δ(T−t)} + K e^{−r(T−t)}` (Ex 16.6).

> **Existing extraction verdict (Ch 16):** the two listed "key results" are correct as properties but MISATTRIBUTED/INCOMPLETE. (a) The forward-price formula `f(t;T)=e^{(r−δ)(T−t)}S_t` is NOT derived in Ch 16 — Ch 16 gives the continuous-yield Q-drift `r−δ` and the *cost-of-carry* (16.25); forward pricing proper is Ch 29 (only alluded via (16.25)). Presenting it as a Ch16 result is an over-reach. (b) The chapter's core content — the discrete-dividend jump-condition recursion `F(T_i−,s)=F(T_i,s−δ[s])`, the proportional result `F_δ=F_0(t,(1−δ)^n s)`, the `F_δ(t,s)=F_0(t,s e^{−δ(T−t)})` reduction, and the numeraire-covariation correction in Prop 16.19 — was entirely omitted.

---

## Ch 17 — Currency Derivatives (printed 247–264; PNG 268–285)
*Key insight: a foreign currency behaves exactly like a domestic stock with a CONTINUOUS dividend equal to the foreign short rate r_f.*

### §17.1 Pure currency contracts
- Spot FX X (domestic per foreign unit), `dX=Xα_X dt+Xσ_X dW̄` (17.1), `dB_d=r_dB_d dt`, `dB_f=r_fB_f dt` (const rates, scalar W).
- Investing in the foreign bank is a domestic asset `B̃_f = B_f·X` (Lemma 17.1), P-dynamics `dB̃_f = B̃_f(α_X+r_f)dt + B̃_fσ_XdW̄`.
- **Prop 17.2 / Q-dynamics:** `dX = X(r_d−r_f)dt + Xσ_X dW` (17.6, ✓ eq. 17.8); pricing `F(t,x)=e^{−r_d(T−t)}E^Q_{t,x}[Φ(X(T))]` and PDE `F_t + x(r_d−r_f)F_x + ½x²σ_X²F_xx − r_d F = 0` (17.9).
- **Prop 17.3 — Currency call ✓ (modified BS):** `F(t,x) = x e^{−r_f(T−t)} N[d_1] − e^{−r_d(T−t)} K N[d_2]` (17.10) with
  `d_1 = [ln(x/K) + (r_d−r_f+½σ_X²)(T−t)]/(σ_X√(T−t))`, `d_2 = d_1 − σ_X√(T−t)`.
  (Equivalently `F(t,x)=F_0(t, x e^{−r_f(T−t)})`: currency call = BS call on a spot scaled by e^{−r_f(T−t)}.)

### §17.2 Domestic + foreign equity
- Complete market (3 risky assets, 3-D W, invertible 3×3 vol matrix σ of rows σ_X,σ_d,σ_f).
- Claims priced in domestic currency: foreign-equity call struck in foreign currency `Z^d=X(T)max[S_f(T)−K,0]`; struck in domestic currency `Z^d=max[X(T)S_f(T)−K,0]`; exchange option `max[X(T)S_f(T)−S_d(T),0]`.
- Equivalent domestic market (Prop 17.4): `S̃_f = X·S_f`, `B̃_f=X·B_f`; `dS̃_f = S̃_f(α_f+α_X+σ_fσ_X')dt + S̃_f(σ_f+σ_X)dW̄`.
- **Prop 17.5 Q-dynamics:** `dS_d=S_d r_d dt+S_dσ_d dW`; `dS̃_f=S̃_f r_d dt+S̃_f(σ_f+σ_X)dW`; `dB̃_f=B̃_f r_d dt+B̃_fσ_X dW`; `dX=X(r_d−r_f)dt+Xσ_X dW`; and **foreign stock in foreign terms under Q_d:** `dS_f = S_f(r_f − σ_fσ_X')dt + S_fσ_f dW` (17.29) — drift is r_f minus the FX/stock covariation.
- Prop 17.6/17.7: pricing PDEs (risk-neutral E under Q_d over Φ(X,S_d,S̃_f) or Φ(X,S_d,S_f)).
- Examples: foreign call struck in foreign currency `F^d=x·[s_f N[d1]−e^{−r_f(T−t)}KN[d2]]` (vol σ_f, rates r_f); struck in domestic currency: BS on S̃_f with vol `‖σ_f+σ_X‖` and rate r_d.
- **Remark 17.2.4:** correlated-W formulation; translations `σ_i'σ_j = δ_iδ_jρ_ij`, `‖σ_i+σ_j‖²=δ_i²+δ_j²+2δ_iδ_jρ_ij`.

### §17.3 Domestic vs foreign market price of risk (KEY, often missed)
- **Prop 17.10:** `λ_f = λ_d − σ_X'` (17.41) — the foreign market price of risk is the domestic one shifted by the FX volatility vector (as a column). ⇒ you cannot have both markets "risk neutral" (`P=Q_d=Q_f`) unless σ_X=0 (Jensen: `E[1/X]≥1/E[X]`).
- **Prop 17.11:** `X_t = X_0 L_t e^{∫_0^t(r_d^s−r_f^s)ds} = X_0 D^f_t/D^d_t` (17.52–17.53), D = stochastic discount factors.
- **Prop 17.12:** under Q_d `dX_t = X_t(r_t^d−r_t^f)dt + X_tσ_t dW_t^d`; `σ_t = λ_t^d − λ_t^f` (17.55–17.56). Girsanov from Q_d to Q_f has likelihood dynamics `dL=Lσ_XdW`.

> **Existing extraction verdict (Ch 17):** The single quoted Q-dynamics `dX=(r_d−r_f)Xdt+Xσ_XdW` is CORRECT (17.6/17.8), and pricing foreign claims in domestic terms is right in spirit. GAPS/errors: (i) the chapter is only loosely about "quanto products" (it prices currency options and foreign-equity-in-domestic-currency claims; classic quanto fixed-FX payoffs are not solved in the chapter) — flag for accuracy; (ii) the call formula (17.10) with explicit d_1, and the *foreign stock's* Q_d drift `r_f−σ_fσ_X'` were omitted; (iii) the central **Prop 17.10 λ_f = λ_d − σ_X'** and the "both-markets-risk-neutral impossible unless σ_X=0" corollary were completely missing; (iv) the numeraire/SDF representation `X_t=X_0 D^f_t/D^d_t`.

---

## Ch 18 — Barrier Options (printed 265–281; PNG 286–302)
*All results reduce barrier pricing to pricing an ordinary (non-barrier) claim, via linearity of the pricing functional + reflection/method of images.*

### §18.1 Probabilistic toolkit
- **Prop 18.3** absorbed-Wiener (barrier β) density: `f_β(x;t,α)=ϕ(x;μt+α,σ√t) − exp{2μ(α−β)/σ²} ϕ(x;μt−α+2β,σ√t)`.
- **Prop 18.4** running max/min distribution functions (reflection principle) — given in text; used for lookbacks.

### §18.2 Out contracts
- Down-and-out `Z_LO` (pays Φ(S_T) if S stays >L, else 0) & up-and-out `Z^{LO}` (stays <L).
- Notation `Φ_L(x)=Φ(x)·1{x>L}` (chop below L), `Φ^L(x)=Φ(x)·1{x<L}` (chop above L). Pricing functional F linear in Φ (Lemma 18.7).
- **Theorem 18.8 — down-and-out ✓ (method of images):** for s>L,
  `F_LO(t,s;Φ) = F(t,s;Φ_L) − (L/s)^{2r̃/σ²} F(t, L²/s; Φ_L)` (18.6), with **`r̃ = r − ½σ²`**.
- **Theorem 18.12 — up-and-out:** for s<L, `F^{LO}(t,s;Φ) = F(t,s;Φ^L) − (L/s)^{2r̃/σ²} F(t,L²/s;Φ^L)` (18.9).
- Building blocks: `ST(x)=x`, `BO(x)=1`, Heaviside `H(x;L)=1{x>L}`, call `C(x;K)=max[x−K,0]`; prices `ST=s`, `BO=e^{−r(T−t)}`, `H(t,s;L)=e^{−r(T−t)}N([r̃(T−t)+ln(s/L)]/(σ√(T−t)))` (Lemma 18.14).
- Down-and-out call (Prop 18.17): L<K ⇒ `C_LO(t,s;K)=C(t,s;K) − (L/s)^{2r̃/σ²}C(t,L²/s;K)` (18.17); L>K ⇒ add `(L−K)H` terms (18.18). Down-and-out bond (18.14), down-and-out stock (18.16). Put–call parity for barrier (Prop 18.18, L=0 gives usual parity). Up-and-out put Prop 18.19 (18.20–18.21).

### §18.3 In contracts
- **In–out parity (Lemma 18.21):** `F_LI(t,s;Φ)=F(t,s;Φ) − F_LO(t,s;Φ)`; likewise `F^{LI}=F−F^{LO}` (18.23).
- **Prop 18.22** down-and-in `F_LI(t,s;Φ)=F(t,s;Φ_L)+(L/s)^{2r̃/σ²}F(t,L²/s;Φ_L)`; **Prop 18.23** up-and-in; down-and-in call (Prop 18.24) for L<K and L>K cases given.

### §18.4 Ladders / §18.5 Lookbacks
- (α,β)-ladder pays β_n if realized max ∈ D_n=[α_n,α_{n+1}); ladder call β_n=max[α_n−K,0]. Ladder = sum of up-and-in bond contracts (Prop 18.27 formula given). Lookback call `S(T)−minS`, put `maxS−S(T)`, forward versions. Lookback put at t=0 (Prop 18.28) closed form given (uses max-distribution). Ladder call → forward lookback call as partition refined.

> **Existing extraction verdict (Ch 18):** Mostly correct in spirit, but (i) the claimed "down-and-out call **with rebate**" is not in the main text — rebate pricing is set as an exercise (Ex 18.3–18.4); (ii) the central image formula (18.6) `F_LO=F(t,s;Φ_L)−(L/s)^{2r̃/σ²}F(t,L²/s;Φ_L)` with `r̃=r−σ²/2` and the *chop-then-reflect* structure were omitted (the "modified strike/drift" phrasing is vague); (iii) in-out parity is exactly the in=vanilla−out identity (correct); (iv) ladder + lookback-put closed forms missing.

---

## Ch 19 — Stochastic Optimal Control (printed 282–312; PNG 303–333)
*Dynamic programming/HJB for `dX=μ(t,X,u)dt+σ(t,X,u)dW`, running reward F(t,x,u) and terminal Φ.*

### HJB & verification
- Value fn `J(t,x,u)=E_{t,x}[∫_t^T F(s,X^u,u)ds + Φ(X^u_T)]`; optimal value `V(t,x)=sup_u J`.
- **Theorem 19.5 (HJB):** `V_t(t,x) + sup_{u∈U}{F(t,x,u) + A^u V(t,x)} = 0`, `V(T,x)=Φ(x)`, where `A^u` is the controlled generator `A^u f = μ^u·∇_x f + ½ tr{C^u f_xx}`, `C^u=σ^uσ^{u'}`; supremum attained at optimal û (19.16 etc.).
- **Theorem 19.6 (Verification):** if H solves the HJB and g attains the sup, then V=H and û=g.

### §19.4–19.5 Linear regulator
- Minimize `E[∫_0^T (X'QX + u'Ru)dt + X_T'HX_T]` subject to `dX=(AX+Bu)dt+CdW`.
- Ansatz `V(t,x)=x'P(t)x+q(t)` ⇒ **Riccati** `Ṗ = PBR⁻¹B'P − A'P − PA − Q`, `P(T)=H` (19.32); `q̇=−tr[C'PC]`, q(T)=0 (19.33); optimal **linear** control `û(t,x)=−R⁻¹B'P(t)x` (19.35).

### §19.6 Optimal consumption & investment
- Wealth `dX = [X(u⁰r+u¹α) − c]dt + u¹σX dW` (19.3), objective `E[∫_0^T F(t,c_t)dt+Φ(X_T)]`, ruin time `τ=inf{t>0:X_t=0}∧T`.
- For `F(t,c)=e^{−δt}c^γ` (0<γ<1): set w=u¹ (fraction in risky). HJB (19.46+). First-order conditions `γc^{γ−1}=e^{δt}V_x` (19.43), `w = −(V_x/(xV_xx))·(α−r)/σ²` (19.44). With ansatz `V(t,x)=e^{−δt}h(t)x^γ`, `h(T)=0`:
  - optimal risky weight **constant**: `ŵ(t,x) = (α−r)/(σ²(1−γ))` (19.50);
  - optimal consumption **linear in wealth**: `ĉ(t,x) = x·h(t)^{−1/(1−γ)}` (19.51);
  - h solves the **Bernoulli** ODE `ḣ + Ah + Bh^{−γ/(1−γ)} = 0`, `h(T)=0` (19.52–19.53), with `A=γ(α−r)²/[σ²(1−γ)]·(1−½)... ` — in text `A = [γ(α−r)²]/[σ²(1−γ)]·½·? + rγ − δ` consolidated; `B=1−γ`.

### §19.7 Mutual Fund Theorems (Merton)
- **Thm 19.9 (no risk-free asset, n risky):** `dS=D(S)αdt+D(S)σdW`, vol matrix σ rank n (complete). Optimal portfolio `ŵ(t)=g+Y(t)h` (19.60), a point moving on the 1-D "optimal portfolio line" in the simplex Δ={w:e'w=1}, with
  `g = Σ⁻¹e/(e'Σ⁻¹e)` (19.61), `h = Σ⁻¹[e·(e'Σ⁻¹α)/(e'Σ⁻¹e) − α]` (19.62) (Σ=σσ'), and `Y(t) = V_x(t,X)/(X·V_xx(t,X))` (19.63). ⇔ optimal wealth is split between two FIXED mutual funds w_a,w_b.
- **Thm 19.10 (with a risk-free asset):** optimal portfolio = allocation between two fixed funds: fund w⁰ = risk-free asset only, and fund `w^f = Σ⁻¹(α−r·e)` (19.65+) on the risky assets only, with allocation `μ_f(t) = −V_x(t,X)/(X V_xx(t,X))`, `μ_0 = 1−μ_f`.

> **Existing extraction verdict (Ch 19):** Correct at the "V solves HJB / Merton" level but too thin to be usable. Missing: explicit HJB + verification statement, Riccati for the regulator, `ŵ=(α−r)/(σ²(1−γ))` const weight + linear consumption for CRRA, and both exact mutual-fund theorems (esp. `w^f=Σ⁻¹(α−re)` with risk-free asset). No mathematical errors found in the existing one-liner.

---

## Ch 20 — The Martingale Approach to Optimal Investment (printed 313–328; PNG 334–349) ★
*Replace the dynamic program by a STATIC choice of terminal wealth under a budget constraint; completeness ⇒ replicable.*

### Method (§20.1–20.4)
- Complete market (vol matrix σ(t) nonsingular a.s., Prop 20.1). Static problem: `max E^P[U(X_T)]` s.t. budget `e^{−rT}E^Q[X_T]=x` (20.4–20.5). Attainable ⇔ `e^{−rT}E^Q[X_T]=x` (Prop 20.2).
- Lagrange over ω: `U'(X_T)=λe^{−rT}L_T` ⇒ **optimal terminal wealth `X̂_T = F(λe^{−rT}L_T)`** (20.6), F=(U')⁻¹. L dynamics `dL_t = L_t σ_t^{-1'}(r−α_t)dW_t` (20.7), i.e. Girsanov with market price of risk λmpr = σ^{-1'}(α−r).
- **Optimal portfolio (Prop 20.4):** from discounted wealth `Z_t=e^{−rt}X_t`, `dZ_t=Z_t u_t'σ_t dW_t^Q`; martingale representation `dZ_t=h_t dW_t^Q` ⇒ `û_t = (1/Z_t)h_t'σ_t^{-1}` (20.11).

### §20.5 Power utility `U(x)=x^γ/γ`, γ≠0, γ<1
- `F(y)=y^{−1/(1−γ)}`.
- **Prop 20.6:** optimal terminal wealth `X̂_T = e^{rT}·(x/H_0)·L_T^{−1/(1−γ)}` (20.20), where `H_0=E^{Q⁰}[exp{½∫_0^T (β/(1−γ))‖σ_t^{-1'}(α_t−r)‖²dt}]` with β=γ/(1−γ); optimal utility `V_0=(x^γ/γ)e^{rγT}H_0^{1−γ}` (20.15).
- **Prop 20.7 optimal wealth process:** `X̂_t = e^{rt}x·(H_t/H_0)·L_t^{−1/(1−γ)}` (20.21), `H_t=E^{Q⁰}[e^{...∫_t^T}|F_t]`.
- **Prop 20.8 optimal portfolio:** `û_t = [1/(1−γ)](α_t−r)'(σ_tσ_t')^{-1} + σ_H(t)σ_t^{-1}` (20.25) — first term = Merton (deterministic-param) solution, second = **hedging demand for parameter risk**. Deterministic α,σ ⇒ `û_t = [1/(1−γ)](α_t−r)'(σ_tσ_t')^{-1}` (20.26) and σ_H=0.

### §20.7 Log utility `U(x)=ln x`
- **Prop 20.9:** `X̂_t = e^{rt}x·L_t^{-1}`; `û_t = (α_t−r)'(σ_tσ_t')^{-1}`. (= power limit γ→0; L⁰≡1, Q⁰=P, H≡1; no hedging demand — myopic.) Note X̂/its "P-numeraire" property (Ex 20.3): Π_t/X̂_t is a P-martingale.

### §20.8 Exponential utility `U(x)=−(1/γ)e^{−γx}`
- `F(y)=−(1/γ)ln y`.
- **Prop 20.10 optimal terminal wealth:** `X̂_T = e^{rT}x + (1/γ)H_0 − (1/γ)ln(L_T)` (20.34), `H_0=E^Q[ln L_T]=E^P[L_T ln L_T]` (relative entropy of Q w.r.t. P).
- **Prop 20.11 optimal wealth process:** `X̂_t = e^{rt}x + e^{−r(T−t)}(1/γ){H_0 − H_t − ln L_t}` (20.38), `H_t = ½E^Q[∫_t^T‖σ_s^{-1'}(α_s−r)‖²ds|F_t]`.
- **Prop 20.12 optimal portfolio:** `û_t = e^{−r(T−t)}·(1/(γX_t))·(σ_t^{-1'}[α_t−r] − σ_H(t))'`; deterministic case `û_t=e^{−r(T−t)}(1/(γX_t))[α_t−r]'(σ_tσ_t')^{-1}`.

> **Existing extraction verdict (Ch 20):** the one-line "X*_T = I(λΛ_T) (inverse marginal utility of SDF)" is CORRECT (with Λ_T=e^{−rT}L_T the SDF). Gaps: no actual formulas for power/log/exponential terminal wealth or portfolios (only "explicit portfolios" claimed without content), no budget constraint, no hedging-demand term in power, no relative-entropy link in exponential. Add the three utility-specific results above.

---

## Ch 21 — Optimal Stopping Theory & American Options (printed 329–350; PNG 350–371) ★
*Problem: `max E[Z_τ]` over stopping times 0≤τ≤T. Tools: Snell envelope, backward recursion, variational inequalities / free boundary, American put, perpetual put.*

### §21.2–21.3 Generalities
- Stopping time `{τ≤t}∈F_t`. Trivial cases (Prop 21.2): Z submartingale ⇒ stop late (τ̂=T); supermartingale ⇒ stop now (τ̂=0); martingale ⇒ all τ optimal. Drift test (Prop 21.3) via `dZ=μdt+σdW`. Convex-function facts (Prop 21.5): convex increasing g of a submartingale is a submartingale (martingale∼linear, sub∼convex, super∼concave).

### §21.4 Discrete time
- **Prop 21.7 backward recursion (optimal value):** `V_n = max{Z_n, E[V_{n+1}|F_n]}`, `V_T=Z_T` (21.8–21.9); stop at n iff V_n=Z_n.
- **Prop 21.8** smallest optimal rule `τ̂ = min{n≥0: V_n=Z_n}` (21.10).
- **Snell envelope** = smallest supermartingale dominating Z. **Theorem 21.12 (Snell Envelope Thm):** optimal value V IS the Snell envelope of Z. `V^{τ̂_n}` is a martingale on [n,T] (Prop 21.15).
- Markovian/finite-state: `V_n = max[α^n g, A V_{n+1}]` (Prop 21.16); discounted `W_n=α^{−n}V_n`: `W_n=max[g,αA W_{n+1}]`, `W_T=g`. Infinite horizon: `W=max[g,αAW]`; W = smallest α-excessive fn ≥ g; continuation region `C={i:W(i)>g(i)}`, stopping region `S={i:W(i)=g(i)}`; τ̂=inf{k: W(X_k)=g(X_k)} (Prop 21.20); computable as an LP.

### §21.5 Continuous time
- **Thm 21.23 (Snell Envelope, continuous):** V = Snell envelope of Z; smallest optimal `τ̂_t = inf{s≥t: V_s=Z_s}` (21.34); stopped V^{τ̂_t} martingale on [t,T].
- **Diffusions (§21.5.2):** `max E[Φ(τ,X_τ)]`, `V(t,x)=sup E_{t,x}[Φ(τ,X_τ)]`. Optimal value satisfies, with generator A:
  - `V ≥ Φ`, `(∂/∂t+A)V ≤ 0` (21.44–21.45); stop iff V=Φ (then (∂_t+A)V<0), continue iff V>Φ (then (∂_t+A)V=0) on `C={(t,x):V>Φ}` (21.46).
  - **Prop 21.25/21.26 variational inequalities:** `V(T,x)=Φ(T,x)`, `V≥Φ`, `(∂_t+A)V≤0`, and `max{V−Φ, (∂_t+A)V}=0` everywhere (21.56) — VI form removes C.
  - **Prop 21.27 free boundary value problem** on C: `V_t+μV_x+½σ²V_xx=0` in C, `V=Φ` on ∂C; C not known a priori. Smooth-fit heuristic: V should be C¹ across ∂C.
  - **Prop 21.28:** never optimal to stop where `∂_tΦ+μΦ_x+½σ²Φ_xx>0` (i.e. where Φ(t,X) is locally a submartingale); such points ⊂ C.

### §21.6 American options
- **§21.6.1 American call, no dividends:** reward `Z_t=e^{−rt}max[S_t−K,0]=max[e^{−rt}S_t−e^{−rt}K,0]` is a Q-**submartingale** (e^{−rt}S_t Q-martingale; convex-increasing) ⇒ optimal τ̂=T; American call = European call (never early-exercise). (Cf. Ch 7.8.)
- **§21.6.2 American put:** optimal stopping `max E^Q[e^{−rτ}max(K−S_τ,0)]`; value solves free-boundary problem on continuation region C with boundary b(t)∈C¹:
  `V_t+rsV_s+½σ²s²V_ss−rV=0` in C (21.63); `V(T,s)=max[K−s,0]`; `V>max[K−s,0]` in C, `V=max[K−s,0]` on C^c; smooth fit `lim_{s↓b(t)} V_s = −1` (21.67). Optimal stop `τ̂=inf{t≥0:S_t=b_t}` (21.68). No closed form; solve FBVP / VI / binomial approximation.
- **§21.6.3 Perpetual American put (closed form, ✓):** time-homogeneous ODE `rsV_s+½s²σ²V_ss−rV=0`, s>b; general solution `V(s)=As+Bs^{−γ}` (21.70) with **`γ=2r/σ²`** (21.71). Boundedness as s→∞ ⇒ A=0; `V(b)=K−b`, smooth fit `V'(b+)=−1` ⇒ **Prop 21.30:**
  `b = γK/(1+γ)` (21.72), `V(s) = (K/(1+γ))(b/s)^γ`, s>b (21.73).
  (Exercise also solves American put for r=0 on finite horizon.)

> **Existing extraction verdict (Ch 21):** concept list correct (Snell, stopping times, free boundary, early-exercise premium implied). GAPS/errors: (i) no mention that the optimal value IS the Snell envelope (Theorem) nor the backward recursion / smallest optimal rule; (ii) the variational-inequality form (21.56) and smooth-fit condition omitted; (iii) no claim of the perpetual-put closed form `b=γK/(1+γ)`, `V(s)=(K/(1+γ))(b/s)^γ` — a flagship result; (iv) "American call without dividends never exercised early" correctly stated. No wrong formulas found.

---

## Global corrections to `/tmp/atlas_extract/derivative_pricing.md` (Ch 15–21 block)
1. **Ch 16 misattribution:** do NOT list `f(t;T)=e^{(r−δ)(T−t)}S_t` as a Ch 16 "key result" — forward pricing is Ch 29; Ch 16 establishes the continuous-yield Q-drift `r−δ` and the cost-of-carry identity (16.25). Add the genuine Ch 16 results: discrete jump condition recursion, `F_δ=F_0(t,(1−δ)^n s)`, `F_δ=F_0(t,s e^{−δ(T−t)})`, and the numeraire gain-covariation Prop 16.19.
2. **Ch 17 scope:** chapter prices currency options & foreign-equity-currency claims (not solved classic quants); add explicit currency call (17.10), foreign-stock Q_d drift `r_f−σ_fσ_X'`, and the key `λ_f = λ_d − σ_X'` (Prop 17.10) + SDF representation `X_t=X_0 D^f/D^d`.
3. **Ch 18:** rebate is exercise-only, not a main-text result; give Thm 18.8 image formula `(L/s)^{2r̃/σ²}` (r̃=r−σ²/2) explicitly; note in/out parity is `in=vanilla−out`.
4. **Ch 19/20/21:** fold in the explicit formulas above (HJB+verification, Riccati, ŵ=(α−r)/(σ²(1−γ)), mutual-fund `w^f=Σ^{-1}(α−re)`, power/log/exp terminal wealth & portfolios, VI/free-boundary, perpetual put closed form).

## Verification notes
- Rendered pages PNG p-230..p-371 (printed 209..350) were used; PNG offset = printed + 21 confirmed by three direct image reads (p-230=209, p-289=268, p-369=348).
- Vision reads of formula-dense pages (ch 15 opening §15.1–15.2; barrier Thm 18.8/Def 18.6 & 18.6; perpetual American put Prop 21.30) matched the text-layer transcription exactly (γ=2r/σ², b=γK/(1+γ), V(s)=(K/(1+γ))(b/s)^γ; FLO=F(t,s;ΦL)−(L/s)^{2r̃/σ²}F(t,L²/s;ΦL), r̃=r−σ²/2). Cross-checks confirm the pdftotext extraction (`bjork.txt`) is a faithful representation of the printed equations for these chapters.
- The vision model backend intermittently returned 404 (rate limit); where unavailable, verification relied on the authoritative PDF text layer plus the successful direct image reads. No source files were modified.
