# Björk, *Arbitrage Theory in Continuous Time* (3rd ed., OUP 2009) — Ch 1–7
## Math-verified deep-read (vision + text cross-check)

**Source:** rendered pages `/tmp/atlas_pages/bjork/p-001.png … p-546.png`; text layer `/tmp/atlas_extract/bjork.txt`.
**Page map (verified by reading page tops):** printed page = PDF page − 21.
Ch1 PDF 22–25 (print 1–4) · Ch2 PDF 26–46 (print 5–25) · Ch3 PDF 47–60 (print 26–39) · Ch4 PDF 61–86 (print 40–65) · Ch5 PDF 87–104 (print 66–83) · Ch6 PDF 105–112 (print 84–91) · Ch7 PDF 113–135 (print 92–114).
**Verification basis:** direct vision reads of typeset pages p-028, p-032, p-033, p-034, p-045 (Ch2) and p-051, p-053, p-058, p-059 (Ch3) [Ch1–3 core]; remaining Ch3–7 formula pages were cross-verified against the pdftotext layer, which renders this book's displayed equations faithfully (all equation numbers match). Vision API was unavailable for the later Ch4–7 reads (persistent 404), so those rests on text-layer cross-reference only.

---

## CH 1 — Introduction (PDF 22–25 / print 1–4)
- C&H (Swedish) / ACME (American) currency example: forward FX contract vs European call on $1M USD, 8.00 SEK/$ spot, six-month delivery.
- **Def 1.1** European call: right (not obligation) to buy X USD at strike K at exercise date T; put = right to sell; *European* = exercise only at T; *American* = exercise any time before T (contrast noted, full theory deferred to Ch 21).
- Derivative = contingent claim on an underlying; a derivative asset exists in huge variety (calls/puts, American, FRA, convertibles, futures, bonds/bond options, caps/floors, swaps).
- **The two "answers" (pricing by discounted expected payoff; or pure supply–demand) are BOTH incorrect** given mild assumptions; correct price = relative price consistent with the underlying (no arbitrage). No equations in this chapter.

## CH 2 — The Binomial Model (PDF 26–46 / print 5–25)
*One-period model.* Assets: bond `B`, stock `S`. Portfolio `h=(x,y)`, `x` = position in bond, `y` = shares of stock.
- **Value process (Def 2.1):** `V_t^h = xB_t + yS_t` (t=0,1), `V_0^h = x + y·s`, `V_1^h = x(1+R) + y·s·Z`, where `Z ∈ {u,d}` is the gross stock return factor, `s=S_0`, bond gross return `1+R`.
- **Arbitrage portfolio (Def 2.2):** `V_0^h = 0` and `V_1^h > 0` with probability 1.
- **No-arbitrage (Prop 2.3):** market free of arbitrage ⇔ `d ≤ (1+R) ≤ u` (bracket). [In the multiperiod setting the strict form `d < (1+R) < u` (Prop 2.26) guarantees `q_u,q_d > 0`.]
- **Martingale / risk-neutral probabilities:** `q_u = (1+R−d)/(u−d)`, `q_d = (u−(1+R))/(u−d)`; `S_0 = (1/(1+R)) E^Q[S_1]`.
- **Replicating (hedging) weights (eqs 2.2–2.3, one-period; a simple claim `Φ` with payoff `Φ(u)`/`Φ(d)`):**
  `x = (1/(1+R)) · (uΦ(d) − dΦ(u))/(u−d)`,  `y = (1/s) · (Φ(u) − Φ(d))/(u−d)`.
  (Eqs 2.24–2.25 give the multiperiod analogue with time/state dependence: `x_t(k)`, `y_t(k)`.)
- **Pricing principle (Prop 2.9/2.10):** reachable claim ⇒ any price ≠ `V_0^h` ⇒ arbitrage; arbitrage-free binomial model is complete.
- **Risk-neutral valuation (Prop 2.11, eq 2.4):** `Π(0;X) = (1/(1+R)) E^Q[X]`; explicitly `Π(0;X) = (1/(1+R)){ [(1+R)−d)/(u−d)]·Φ(u) + [(u−(1+R))/(u−d)]·Φ(d) }`.
- **Multiperiod (Prop 2.25):** `Π(0;X) = (1/(1+R)^T) E^Q[X] = (1/(1+R)^T) Σ_k C(T,k) q_u^k q_d^{T−k} Φ(s u^k d^{T−k})`; `Y` = # up-moves ~ Binomial. Backward induction / dynamic replication; value process `V_t^h = x_t B_t + y_t S_t`.
- Worked example (p12–14): S0=100, R=0, K=110, S1∈{120,80}; q_u=q_d=0.5; price = 5 = cost of hedge `(x,y)=(−20, 1/4)`; prices are *preference-free*.

## CH 3 — A More General One Period Model (PDF 47–60 / print 26–39)
Market: N assets `S^1,…,S^N`, M states `ω_1,…,ω_M`; numeraire `S^1`; normalized prices `Z_t^i = S_t^i/S_t^1` (with `Z_t^1 ≡ 1`).
- **Payoff matrix `D^Z` (eq 3.4):** M×N-structured with first row all 1s (numeraire row) and rows `Z_1^i(ω_j)`. A portfolio `h∈R^N` has zero initial cost `hZ_0=0` and produces payoff vector `hD^Z`.
- **No-arbitrage / First Fundamental Theorem (finite-state; via Farkas' Lemma):** market is arbitrage-free ⇔ ∃ strictly positive probabilities `q_j>0`, `Σq_j=1`, with `Z_0 = D^Z q`, i.e. `Z_0^i = Σ_j Z_1^i(ω_j) q_j` for each asset `i`.
- **Equivalent measures (Def 3.5):** `Q~P` ⇔ `P(A)=0 ⇔ Q(A)=0`.
- **Martingale (Def 3.6):** `E[X_m|F_n]=X_n` for all `n≤m`.
- **Martingale measure (Def 3.7):** `Q~P` and every normalized price process `Z^i` is a Q-martingale.
- **Martingale pricing (Prop 3.15, money-account numeraire, eq 3.18):** arbitrage-free prices of a claim `X` are exactly `Π(0;X) = (1/(1+R)) E^Q[X]` for some martingale measure `Q`; replicable claims have a unique price `= V_0^h` independent of `Q`.
- **Completeness (Prop 3.15, Second Fundamental Theorem):** market complete ⇔ martingale measure unique ⇔ `Ker[D]=0 ⇔ Im[D*]=R^M`.
- **Stochastic discount factors (3.6):** `L = dQ/dP`, `Λ(ω) = L(ω)/(1+R)`; **Prop 3.18:** `Π(0;X) = E^P[Λ·X]`. Λ is the Arrow–Debreu state-price system; one-to-one with martingale measures.

## CH 4 — Stochastic Integrals (PDF 61–86 / print 40–65)
- Wiener process; filtrations/information; Itô stochastic integral `∫ H dW` (forward increments); quadratic variation.
- **Key facts (eqs 4.19–4.22):** `E[ΔW]=0`, `E[(ΔW)^2]=Δt`, `Var[ΔW]=Δt`, `Var[(ΔW)^2]=2(Δt)^2` ⇒ formal **`(dW)^2 = dt`** (eqs 4.23, 4.26).
- **SDE notation:** `X(t)=a+∫_0^t μ ds + ∫_0^t σ dW` ⇔ `dX(t)=μ(t)dt+σ(t)dW(t)`, `X(0)=a`.
- **Itô's formula (Thm 4.10 / Prop 4.11, eq 4.28/4.30):** for `Z=f(t,X)`, `f∈C^{1,2}`,
  `df(t,X) = (∂f/∂t + μ ∂f/∂x + ½σ² ∂²f/∂x²)dt + σ ∂f/∂x dW`
  — i.e. `df = f_t dt + f_x dX + ½ f_xx (dX)²` under the multiplication table `(dt)²=0`, `dt·dW=0`, `(dW)²=dt`.
- **Gaussian stochastic integrals (Lemma 4.15):** `X(t)=∫_0^t σ(s)dW(s)` with deterministic σ ⇒ `X(t)~N(0, ∫σ² ds)`.
- **Multidimensional Itô (Thm 4.16, eq 4.37):** `dX_i = μ_i dt + Σ_j σ_ij dW_j`, `Z=f(t,X)`, `f:R_+×R^n→R`:
  `df = (∂f/∂t)dt + Σ_i (∂f/∂x_i) dX_i + ½ Σ_{i,j} (∂²f/∂x_i∂x_j) dX_i dX_j`
  with `(dt)²=0`, `dt·dW_i=0`, `(dW_i)²=dt`, `dW_i·dW_j=0 (i≠j)`. Equivalent generator form with `C=σσ'` and trace/Hessian `½ tr[σ H σ]dt`.
- **Correlated Wiener processes (4.8):** `W=δ W̄` (δ n×d, rows unit length) ⇒ `W_i = Σ_j δ_ij W̄_j`; correlation `ρ = δδ'`, `ρ_ij dt = Cov[dW_i,dW_j]`. **Multiplication table (Prop 4.18):** `dW_i·dW_j = ρ_ij dt` (in particular 2D `dW_1 dW_2 = ρ dt`). Vector Itô with correlation `df = (f_t + Σμ_i f_{x_i} + ½Σσ_i σ_j ρ_ij f_{x_ix_j})dt + Σ σ_i f_{x_i} dW_i`; translation between the two formalisms (Prop 4.19).

## CH 5 — Differential Equations (PDF 87–104 / print 66–83)
- **SDEs:** `dX_t = μ(t,X_t)dt + σ(t,X_t)dW_t`; existence/uniqueness.
- **Geometric Brownian motion (Prop 5.2):** solution of `dX_t = αX_t dt + σX_t dW_t`, `X_0=x_0` is
  `X(t) = x_0 exp((α − ½σ²)t + σW(t))`; `E[X_t] = x_0 e^{αt}`. (α = drift of log-return density; the `−½σ²` is Itô's correction.)
- **Linear SDE (Prop 5.3):** `dX_t = (AX_t+b_t)dt + σ_t dW_t` has solution `X_t = e^{At}x_0 + ∫_0^t e^{A(t−s)}b_s ds + ∫_0^t e^{A(t−s)}σ_s dW_s` (matrix exponential `e^{At}=Σ A^k t^k/k!`).
- **Infinitesimal operator (Def 5.4):** `(Ah)(t,x) = Σ_i μ_i(t,x) ∂h/∂x_i + ½ Σ_{i,j} C_ij(t,x) ∂²h/∂x_i∂x_j`, `C=σσ'`; Dynkin/Itô/Kolmogorov-backward operator. Itô takes form `df = (∂f/∂t + Af)dt + [∇_x f]σ dW`.
- **Feynman–Kac (Props 5.5, 5.6):**
  - `F_t + μ F_x + ½σ² F_xx = 0`, `F(T,x)=Φ(x)` ⇒ `F(t,x)=E_{t,x}[Φ(X_T)]` (X solves the associated SDE).
  - With discounting: `F_t + μF_x + ½σ²F_xx − rF = 0`, `F(T,x)=Φ(x)` ⇒ **`F(t,x) = e^{−r(T−t)} E_{t,x}[Φ(X_T)]`** (multidim: Prop 5.8, eq 5.39). Martingale-characterization Prop 5.9.
- **Kolmogorov equations:**
  - **Backward (Props 5.10, 5.11):** `∂P/∂s + AP = 0` on `(s,y)`, `P(t,y;t,B)=1_B(y)`; for density `∂p/∂s + Ap = 0`.
  - **Forward / Fokker–Planck (Prop 5.12):** `∂p/∂t = A^*p`, adjoint `(A^*f)(t,x) = −∂_x[μf] + ½∂²_{xx}[σ²f]` (scalar); multidim `A^*f = −Σ∂_{x_i}[μ_i f] + ½Σ∂²_{x_ix_j}[C_ij f]`. Gaussian / GBM density examples.

## CH 6 — Portfolio Dynamics (PDF 105–112 / print 84–91)
Discrete-time motivation → continuous-time Itô limit (emphasizes *forward* increments; the naive `S(t)dh(t)+c dt=0` is wrong because of Itô cross-term `dh·dS`).
- **Definitions (6.1/6.2):** portfolio strategy `h(t)` (F^S-adapted), Markovian `h(t)=h(t,S(t))`, **value process `V^h(t) = Σ_i h_i(t)S_i(t) = h(t)·S(t)`**.
- **Self-financing (Def 6.2, eq 6.11):** no exogenous in/outflow ⇒ `dV^h(t) = Σ_i h_i(t)dS_i(t) − c(t)dt` (no consumption: `dV^h = h·dS`).
- **Relative portfolio (Def 6.3, eq 6.12):** `u_i(t) = h_i(t)S_i(t)/V^h(t)`, `Σ u_i = 1`.
- **Relative form (Lemma 6.4, eq 6.13):** `dV^h(t) = V^h(t) Σ_i u_i(t) dS_i(t)/S_i(t) − c(t)dt`.
  For the two-asset (stock GBM `dS=αS dt+σS dW̄` + bond `dB=rB dt`) case this gives `dV = V[ u_s(αdt+σdW̄) + u_B r dt ]` (the general result in (6.13); explicit specialization as in Ch7 eq (7.21)).
- **Lemma 6.5 (representation):** if `dZ = Z Σ q_i dS_i/S_i − c dt` with `Σ q_i=1`, then `(h,c)` with `h_i = q_i Z/S_i` is self-financing with `V^h=Z`, `u=q`.
- **Dividends (6.3):** cumulative dividends `D_i(t)`; continuous yield `dD_i = δ_i dt`; **gain process `G = S + D`**; self-financing `dV^h = Σ h_i dG_i − c dt` (eq 6.21); relative form `dV^h = V Σ u_i dG_i/S_i − c dt` (eq 6.22).

## CH 7 — Arbitrage Pricing / Black–Scholes (PDF 113–135 / print 92–114)
- **Setup:** market `dB = rB dt`, `dS = S(t)α(t,S(t))dt + S(t)σ(t,S(t))dW̄`; simple claim `X=Φ(S(T))`; price `Π(t;X)=F(t,S(t))`.
- **Arbitrage possibility (Def 7.5):** self-financed `h`, `V^h(0)=0`, `P(V^h(T)≥0)=1`, `P(V^h(T)>0)>0`.
- **Prop 7.6 (locally riskless portfolio):** if `dV^h = k(t)V^h dt` then `k(t)=r(t)` for all t, or there is arbitrage ("only one short rate on an arbitrage-free market"). *[This is the precise form of the "no dW-term ⇒ must be rV dt" heuristic.]*
- **Price-process ansatz (Assumption 7.2.2):** `Π(t;X)=F(t,S(t))`. By Itô the derivative has `α_π F = F_t+αS F_s+½σ²S²F_ss`, `σ_π F = σS F_s` (eqs 7.19–7.20). Hedging a two-asset portfolio `(u_s,u_π)` to kill the `dW̄` term (eqs 7.23–7.24), then Prop 7.6 ⇒ `u_s α+u_π α_π = r`.
- **Black–Scholes PDE (Thm 7.7, eqs 7.31–7.32):** on `[0,T]×R_+`
  `F_t(t,s) + r s F_s(t,s) + ½ s² σ²(t,s) F_ss(t,s) − r F(t,s) = 0`,  `F(T,s)=Φ(s)`.
  Drift α of underlying is **absent** — pricing is relative, only σ matters.
- **Risk-neutral valuation (Thm 7.8, eq 7.39):** `F(t,s) = e^{−r(T−t)} E^Q_{t,s}[Φ(S(T))]`, where Q-dynamics `dS = rS dt + σS dW` (change of drift α→r); `Q` is the *martingale measure*.
- **Martingale property (Prop 7.9):** for every traded asset, normalized price `Z(t)=Π(t)/B(t)` is a Q-martingale.
- **Black–Scholes formula (Prop 7.10, eqs 7.48–7.50), European call, Φ(x)=max[x−K,0], constant α,σ:**
  `F(t,s) = s N[d1(t,s)] − e^{−r(T−t)} K N[d2(t,s)]`,
  `d1(t,s) = [ ln(s/K) + (r + ½σ²)(T−t) ] / (σ√(T−t))`,  `d2(t,s) = d1(t,s) − σ√(T−t)`,
  `N` = standard normal CDF. Integral form `F(t,s)=e^{−r(T−t)}∫Φ(se^z)f(z)dz` with `Z~N((r−½σ²)(T−t), σ²(T−t))`.
- **Options on futures / forward contracts (7.6):**
  - **Forward price (Prop 7.11):** `f(t;T,X)=E^Q_{t,s}[X]`; for `X=S_T`, `f(t;T)=e^{r(T−t)}S_t`.
  - **Prop 7.12:** if short rate is deterministic, futures price = forward price, `F(t;T,X)=E^Q_{t,s}[X]`.
  - **Black-76 (Prop 7.13, eq 7.55):** European call on a futures (delivery T1>T): `c = e^{−r(T−t)}[ F N[d1] − K N[d2] ]`, `d1 = [ln(F/K)+½σ²(T−t)]/(σ√(T−t))`, `d2 = d1 − σ√(T−t)`, `F` = futures price.
- **Volatility (7.7):**
  - **Historical:** sample log-returns `ξ_i=ln(S(t_i)/S(t_{i−1}))`, `E[ξ_i]=(α−½σ²)Δt`, `Var[ξ_i]=σ²Δt`; estimate `σ̂ = S_ξ/√Δt` (sample st.dev.), approx. std error `D(σ̂)≈σ̂/√(2n)`.
  - **Implied:** solve `p = c(s,t,T,r,σ,K)` for σ from a benchmark market price → implied volatility; implied-vol curve as function of K (smile), in/out/at-the-money (Remark 7.7.1).
- **American options (7.8, PDF 131+):** introduces American contracts (early exercise) and price bounds (e.g. American call ≥ European; no-arbitrage constraints); full free-boundary treatment deferred to Ch 21.

---

## Corrections / gaps vs existing extraction (`derivative_pricing.md` PART A, Ch 1–7)
Overall the existing Ch1–7 extraction is **mathematically accurate**; no formula is wrong. Issues found:
1. **[Attribution] Ch6 "key result" mis-placed.** "if value dynamics has no dW-term it must equal rVdt (else arbitrage)" is **Prop 7.6 in Ch7** (print p97 / PDF 118), not established in Ch6. Ch6 itself only derives the self-financing dynamics (eqs 6.11, 6.13, 6.21–6.22). Keep the statement (it is correct) but attribute to Ch7 / Prop 7.6.
2. **[Presentation] Ch6 example formula.** Existing text's `dV = V[u_s(αdt+σdW̄)+u_B r dt]` is not a *displayed* Ch6 equation; the book's general displayed forms are (6.13)/(6.22) `dV = V Σ u_i dS_i/S_i − c dt`. The two-asset specialization is correct (matches Ch7 eq (7.21) structure) but should be labeled as a consequence, not a book equation.
3. **[Completeness] Ch2 non-strict vs strict no-arbitrage.** One-period Prop 2.3 uses `d ≤ (1+R) ≤ u`; the strict `d < (1+R) < u` (Prop 2.26) is what guarantees strictly positive martingale probabilities and appears in the multiperiod proof. Worth stating both to avoid the appearance of contradiction.
4. **[Minor gap] Ch7 §7.8 American options** (PDF 131–134) introduces early exercise and price bounds but is omitted from the extraction's Ch7 bullet (acceptable if intentionally deferred to Ch21 — flag it).
5. **[Refinement] SDF exact form (Ch3).** Existing extraction states `Z_0^i = E[Λ·Z_1^i]`. Book's displayed result (Prop 3.18, eq 3.20, money-account numeraire) is `Π(0;X) = E^P[Λ·X]` with `Λ = (1/(1+R))·(dQ/dP)`. Compatible, but quote the exact `Π(0;X)=E^P[ΛX]` form for fidelity.
6. **[Confirmations]** All core displayed formulas verified exactly: binomial hedging weights (2.2–2.3), q_u/q_d, risk-neutral valuation (2.4, 2.25); Ch3 FTs + Farkas; Itô scalar/multidim/correlated multiplication tables & trace form; GBM solution (5.15) & E[X_t]; FK with discount (5.36/5.39); infinitesimal operator; KBE/KFE (Fokker–Planck) adjoint; self-financing & gain process; BS PDE (7.31), risk-neutral valuation (7.39), BS formula (7.48–7.50), forward (7.51–7.52), futures=forward (7.53), Black-76 (7.55), hist/implied volatility.
