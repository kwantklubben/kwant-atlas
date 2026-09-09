# Shreve, *Stochastic Calculus for Finance II — Continuous-Time Models*: Chapters 4–5 — Math-Verified Deep-Read
## Verification source & method

- **Scope:** Vol II Ch 4 *Stochastic Calculus* and Ch 5 *Risk-Neutral Pricing*.
- **Existing extraction reviewed:** `/tmp/atlas_extract/shreve.md` (Vol II ch4/ch5 entries, lines 186–225).
- **Text layer used as ground truth for math:** `/tmp/atlas_extract/shreve2.txt` (the PDF's own pdftotext layer; carries section/equation numbers and the standard-math glyph set, e.g. `(4.5.14)`, `(5.2.11)`).
- **Vision note (flagged honestly):** the vision backend became unavailable mid-task. `p-120.png` WAS vision-confirmed (it shows **book page 100, §3.4.1 First-Order Variation**, Section 3 *Brownian Motion* — not Ch 4), establishing the page-mapping correction below. After that single success the backend returned persistent HTTP-404 errors for every further page (p-209, p-139, p-230, and copies thereof), so the deep mathematical verification was completed rigorously against the identical PDF's text layer + the prior extraction rather than by OCR/vision of the remaining PNGs. No PNG page-image was relied on beyond the one confirmed frame.

---

## ⚠ CRITICAL CORRECTION — page mapping is off by ≈19–20
The task brief said *"ch4 p120–169, ch5 p170–209"* (atlas PNG numbers). **This is wrong for this PDF** and will misroute any per-page work.

Empirically established (vision on `p-120.png` + form-feed book-page-header count in `shreve2.txt`):
- `p-120.png` = **book p.100** → **Section 3 (Brownian Motion)**, not Ch 4.
- **PDF page number ≈ book page number + 19** (front matter offset). Equivalently **book page = PDF page − 19**.
- Form-feed/printed-header count: printed page "126" (Ch 4 §4.2) sits at PDF page 145 ⇒ 145−126 = 19.

Correct ranges for the genuine Shreve II chapters (atlas PNGs / book pages):
| Chapter | Book pages | PDF pages (PNG) | Section span (book) |
|---|---|---|---|
| **4 Stochastic Calculus** | ≈120–208 | **≈139–227** (`p-139`…`p-227`) | 4.1 intro≈120; 4.2 Itô int. simple≈126–131; 4.3 general≈133–137; 4.4 Itô–Doeblin≈137–153; 4.5 BSM≈153–164; 4.6 multivariable≈166–172; 4.7 Brownian bridge≈172–182; 4.8 summary≈183; 4.9 notes≈186; 4.10 exercises≈190–208 |
| **5 Risk-Neutral Pricing** | ≈209–262 | **≈228–281** (`p-228`…`p-281`) | 5.1 intro≈209; 5.2 RN measure≈209–220; 5.3 Martingale Representation≈221–223; 5.4 Fundamental Theorems≈224–234; 5.5 Dividend-paying stocks≈235–240; 5.6 Forwards & futures≈241–248; 5.7 summary≈249; 5.8/5.9 notes/exercises≈250–262 |

The brief's "ch5 p170–209" band actually lies inside Ch 4 (Itô–Doeblin → BSM → Brownian bridge); genuine Ch 5 begins ≈`p-228`.

---

# Chapter 4 — Stochastic Calculus (book pp. 120–208)

Sections: 4.1 Introduction · 4.2 Itô's Integral for Simple Integrands · 4.3 Itô's Integral for General Integrands · 4.4 Itô–Doeblin Formula · 4.5 Black–Scholes–Merton Equation · 4.6 Multivariable Stochastic Calculus · 4.7 Brownian Bridge · 4.8 Summary · 4.9 Notes · 4.10 Exercises.

## Key concepts (verified)
- Itô integral as trading gain against Brownian motion; constructed first for **simple (elementary/step) adapted integrands**, then for **general adapted, square-integrable integrands** by approximation and an isometry (L² extension). Integral is a martingale; mean zero; quadratic variation equals ∫Δ²du.
- **Itô–Doeblin formula** in differential & integral form (the extra ½f″(dW)² term survives because of nonzero quadratic variation; multiplication table dW·dW = dt, dt·dW = dW·dt = 0, dt·dt = 0).
- Applications: generalized geometric BM; Itô integral of a deterministic integrand is Gaussian; **Vasicek** and **Cox–Ingersoll–Ross** short-rate models (mean-reversion; closed vs. no closed form).
- BSM PDE, its explicit solution, the **Greeks** (delta, theta, gamma, vega), forward-contract value & price, **put–call parity** (model-free).
- Multivariable Itô calculus: d-dimensional BM (independent components), Itô–Doeblin for several processes, **Itô product rule**, Lévy characterization (recognize a BM / independent BMs), correlated BMs.
- Brownian bridge & Gaussian processes (Monte-Carlo motivation).

## Key formulas/results (all cross-checked to text)
- Itô integral = martingale (Thm 4.2.1); **Itô isometry** (Thm 4.2.2): `E[I(t)²]=E[∫₀ᵗ Δ²(u)du]`; **quadratic variation** (Thm 4.2.3): `[I,I](t)=∫₀ᵗ Δ²(u)du`, i.e. `dI·dI=Δ²(t)dt`.
- General integrands: `Δ` adapted with `E∫₀ᵀ Δ²(t)dt < ∞` (4.3.1).
- **Itô–Doeblin, BM** (Thm 4.4.1, f(t,x)): `f(T,W(T)) = f(0,W(0)) + ∫₀ᵀ fₜ dt + ∫₀ᵀ f_x dW + ½∫₀ᵀ f_xx dt`; differential form `df = fₜdt + f_x dW + ½f_xx dW·dW`, `dW·dW=dt`.
- **Itô–Doeblin, Itô process** (Thm 4.4.6): for `dX(t)=Θ(t)dt+Δ(t)dW(t)`:
  `df(t,X)=fₜdt+f_x dX+½f_xx dX·dX` with `dX·dX=Δ²(t)dt`
  `= fₜdt + f_x Δ dW + f_x Θ dt + ½ f_xx Δ² dt`. *(The prior extraction's `df=fₜdt+f_x dX+½f_xx dX·dX` form is correct.)*
- **Generalized GBM** (Ex. 4.4.8): `S(t)=S(0)exp{∫₀ᵗσ(s)dW(s)+∫₀ᵗ(α(s)−½σ²(s))ds}` solves `dS=αSdt+σSdW`. With `α=0`, `S(t)=S(0)+∫σS dW` is a martingale. Constant coefficients → log-normal.
- **Itô integral of deterministic integrand** (Thm 4.4.9): `I(t)=∫₀ᵗΔ(s)dW(s)` is Gaussian, mean 0, variance `∫₀ᵗΔ²(s)ds` (proof via MGF of the exponential martingale).
- **Vasicek** (Ex. 4.4.10): `dR=(α−βR)dt+σdW` ⇒ `R(t)=e^{−βt}R(0)+ (α/β)(1−e^{−βt}) + σe^{−βt}∫₀ᵗ e^{βs}dW(s)`. Gaussian, mean `e^{−βt}R(0)+(α/β)(1−e^{−βt})`, variance `(σ²/2β)(1−e^{−2βt})` — positive prob. of going negative.
- **CIR** (Ex. 4.4.11): `dR=(α−βR)dt+σ√R dW` (α,β,σ>0). No closed-form solution. Expectation **same as Vasicek**: `E R(t)=e^{−βt}R(0)+(α/β)(1−e^{−βt})`. Variance (set X=e^{βt}R, use Itô on X², (4.4.38)):
  `Var R(t) = (σ²/β)R(0)(e^{−βt}−e^{−2βt}) + (ασ²/2β²)(1−e^{−βt})²`, `lim_{t→∞}=ασ²/(2β²)`. Nonnegative (vol vanishes at 0; drift αdt pushes back up). *(Prior extraction's CIR formulas verified correct.)*
- **BSM equation** (4.5.14): `cₜ + rxc_x + ½σ²x²c_xx = rc`, `0≤t<T, x≥0`; terminal `c(T,x)=(x−K)⁺`; boundary `c(t,0)=0`, growth `c~(x−e^{−r(T−t)}K)` as x→∞. **Solution** (4.5.19):
  `c(t,x)=xN(d₊)−Ke^{−r(T−t)}N(d₋)`, `d± = [log(x/K)+(r±½σ²)τ]/(σ√τ)`, τ=T−t. (BSM-function `BSM(τ,x;K,r,σ)`.)
- **Greeks** (Ex. 4.9; verified): delta `c_x=N(d₊)`; theta `c_t=−rKe^{−rτ}N(d₋)−(σx/(2√τ))N′(d₊)`; gamma `c_xx=N′(d₊)/(σx√τ)`; vega `∂c/∂σ>0`. Delta and gamma >0, theta <0.
- **Delta-hedging rule** (4.5.11): `Δ(t)=c_x(t,S(t))` (equate dW terms); equating dt terms gives the BSM PDE. Drift α does NOT enter — "volatility (not drift) is the pricing parameter"; delta-neutral long-gamma intuition.
- **Forward contract** (4.5.6): value `f(t,x)=x−e^{−r(T−t)}K`; forward **price** `For(t)=e^{r(T−t)}S(t)` (value of K making forward zero — not the value of a forward).
- **Put–call parity** (4.5.29, model-free): `f=c−p` ⇒ `c−p = x−e^{−r(T−t)}K`; put formula `p=Ke^{−rτ}N(−d₋)−xN(−d₊)`.
- **d-dim BM**: components independent 1-d BMs; `[Wᵢ,Wᵢ]=t`, `[Wᵢ,Wⱼ]=0` (i≠j) ⇒ `dWᵢdWⱼ=0` i≠j (independent). Correlated BMs built via `W₃=ρW₁+√(1−ρ²)W₂`; `dW₁dW₃=ρdt` (Ex. 4.6.6).
- **Multivariable Itô–Doeblin** (4.6.2, two processes): `df(t,M₁,M₂)=fₜdt+f_x dM₁+f_y dM₂+½f_xx dM₁dM₁+f_xy dM₁dM₂+½f_yy dM₂dM₂`.
- **Itô product rule** = Corollary 4.6.3: `d(XY)=X dY+Y dX+dX dY`.
- **Lévy**: Thm 4.6.4 (1-d: cont. martingale from 0 with `[M,M]=t` is a BM); Thm 4.6.5 (2-d: add `[M₁,M₂]=0` ⇒ independent BMs).
- **Brownian bridge** (4.7): Gaussian process `B(t)=W(t)−(t/T)W(T)`; `B(0)=B(T)=0`; `Cov(B(s),B(t))=s(1−t/T)=s(T−t)/T` (0≤s≤t≤T). Representable as a scaled stochastic integral and as a BM conditioned on W(T)=0. Gaussian process definition `(X(t₁)…X(tₙ))` jointly normal for all times.

---

# Chapter 5 — Risk-Neutral Pricing (book pp. 209–262)

Sections: 5.1 intro · 5.2 Risk-Neutral Measure (5.2.1 Girsanov single-BM · 5.2.2 Stock under RN · 5.2.3 Value of portfolio · 5.2.4 Pricing under RN · 5.2.5 Deriving BSM) · 5.3 Martingale Representation Theorem (5.3.1 one BM · 5.3.2 Hedging with one stock) · 5.4 Fundamental Theorems of Asset Pricing (5.4.1 multidim Girsanov & MRT · 5.4.2 multidim model · 5.4.3 Existence of RN measure · 5.4.4 Uniqueness) · 5.5 Dividend-Paying Stocks · 5.6 Forwards and Futures · 5.7 Summary · 5.8 Notes · 5.9 Exercises.

## Key concepts (verified)
- Two big theorems drive the chapter: **Girsanov** (change of measure to remove drift) and **Martingale Representation** (every martingale w.r.t. a BM filtration is an Itô integral). From them come the **two Fundamental Theorems of Asset Pricing**.
- Risk-neutral measure = equivalent measure making **discounted** stock prices martingales; construction via the **market price of risk**; risk-neutral pricing formula (binomial Vol-I (2.4.10/11) analogue); BSM recovered by risk-neutral expectation.
- Hedging = matching MRT integrand to Δ(t)σ(t)D(t)S(t); completeness when every F(T)-claim is hedgeable.
- Multidimension: market-price-of-risk equations `AΘ=b`; existence (no arbitrage) ⟺ solvable; uniqueness (complete) ⟺ unique solution (m=d and A invertible / rank conditions).
- Dividend-paying stocks (continuous rate & lumps): reinvested-discounted stock is the martingale; discounted price alone is not.
- Forwards vs futures; marking to market; forward–futures spread.

## Key formulas/results (cross-checked)
- **RN-derivative machinery** (5.2.1): `P̃(A)=∫_A Z dP`, `ẼX=E[XZ]`, `Z` the Radon–Nikodym derivative `Z=dP̃/dP`; `Z(t)=E[Z|F(t)]` is a P-martingale. Lemma 5.2.2 (change of conditional expectation): `Ẽ[Y|F(s)]=(1/Z(s))·E[YZ(t)|F(s)]` (0≤s≤t).
- **Girsanov 1-d** (Thm 5.2.3): W a BM on (Ω,F,P), Θ adapted; `W̃(t)=W(t)+∫₀ᵗΘ(u)du`, `Z(t)=exp{−∫₀ᵗΘ(u)dW(u) − ½∫₀ᵗΘ²(u)du}`; set `Z=Z(T)`; then `E Z=1` and under `P̃` (`dP̃=Z(T)dP`) `W̃` is a BM. Proof via **Lévy** (`[W̃,W̃]=[W,W]=t`, continuous, martingale under P̃). P̃ and P are equivalent (`Z>0` a.s.). *Technical condition assumed (footnote to (5.2.13)): `E∫₀ᵀΘ²(u)Z²(u)du<∞` so the stochastic integral (5.2.14) exists & Z is a martingale.* *(Prior extraction omitted this integrability condition — flagged.)*
- **Stock under P̃**: model `dS=αSdt+σSdW`; discount `D(t)=e^{−∫₀ᵗR(s)ds}`, `dD=−R D dt`; **market price of risk** `Θ(t)=(α(t)−R(t))/σ(t)`; `d(DS)=σDS[Θdt+dW]=σDS dW̃` (5.2.22) ⇒ DS a P̃-martingale; under P̃ `dS=R S dt+σS dW̃` (5.2.23); `S(t)=S(0)exp{∫σ dW̃ +∫(R−½σ²)ds}`. Change of measure changes mean rate (α→R) but not volatility/paths.
- **Portfolio value** (5.2.25–27): `dX=ΔdS+R(X−ΔS)dt`; `d(DX)=ΔσDS[Θdt+dW]=Δ·d(DS)=ΔσDS dW̃` ⇒ discounted portfolio value a P̃-martingale (Lemma 5.4.5 multidim).
- **Risk-neutral pricing formula** (5.2.30/31): `D(t)V(t)=Ẽ[D(T)V(T)|F(t)]` ⇔ `V(t)=Ẽ[e^{−∫ₜᵀR(u)du}V(T)|F(t)]`.
- **BSM by RN expectation** (5.2.5): with r,σ const, `V(T)=(S(T)−K)⁺`, `S(T)=S(t)exp{−σ√τ Y+(r−½σ²)τ}`, Y~N(0,1); result `c(t,x)=BSM(τ,x;K,r,σ)=xN(d₊)−Ke^{−rτ}N(d₋)`. This *derives* the solution of (4.5.14).
- **MRT 1-d** (Thm 5.3.1): F = filtration generated by W; every F-martingale `M(t)=M(0)+∫₀ᵗΓ(u)dW(u)`. *(Filtration must be exactly the one generated by W — more restrictive than Girsanov's filtration hypothesis.)*
- **Girsanov+MRT** (Cor 5.3.2): with F generated by W, under P̃ both the BM claim and the MRT representation `M(t)=M(0)+∫₀ᵗΓ(u)dW̃(u)` hold for P̃-martingales.
- **Hedging with one stock** (5.3.2): `D(t)V(t)` is a P̃-martingale ⇒ MRT `D V=V(0)+∫Γ dW̃` (5.3.4). Set `X(0)=V(0)` and choose `Δ` s.t. **`Δ(t)σ(t)D(t)S(t)=Γ(t)`** i.e. `Δ(t)=Γ(t)/(σ(t)D(t)S(t))` (5.3.7/8) ⇒ X(T)=V(T) a.s. Two assumptions: σ(t)≠0 (else BM randomness not in stock), and F generated by W (no extra uncertainty). Model **complete** = every F(T)-claim hedgeable. MRT guarantees existence of a hedge but not how to find Γ (deferred to Ch 6). *(Prior extraction's `Γ=ΔσDS`, `V(0)=Ẽ[D(T)V(T)]` correct.)*
- **Girsanov multidim** (Thm 5.4.1): Θ(t)=(Θ₁…Θ_d) adapted; `W̃(t)=W(t)+∫₀ᵗΘ(u)du` (componentwise `W̃_j=W_j+∫Θ_j du`), `Z(t)=exp{−∫₀ᵗΘ·dW − ½∫₀ᵗ‖Θ‖²du}`; under `P̃=dP̃=Z(T)dP` the process `W̃` is a **d-dimensional** BM (components *independent* under P̃). Proof via d-dim Lévy.
- **MRT multidim** (Thm 5.4.2): F generated by d-dim W; any F-martingale `M(t)=M(0)+∫₀ᵗΓ(u)·dW(u)` for adapted d-dim Γ; version under P̃ (after Girsanov) holds too.
- **Multidim market model** (5.4.6): `dSᵢ=αᵢSᵢdt+SᵢΣⱼσᵢⱼdWⱼ`, i=1..m; discounted `d(DSᵢ)=DSᵢ[(αᵢ−R)dt+ΣⱼσᵢⱼdWⱼ]` (5.4.15).
- **Risk-neutral measure** (Def 5.4.3): P̃ equivalent to P and `D(t)Sᵢ(t)` a P̃-martingale ∀i.
- **Market price of risk equations** (5.4.18): `αᵢ(t)−R(t)=Σ_{j=1}^d σᵢⱼ(t)Θⱼ(t)`, i=1..m — **m equations, d unknowns** Θ₁..Θ_d (one per source of randomness, not per stock). If solvable, Girsanov gives P̃ making `d(DSᵢ)=DSᵢΣⱼσᵢⱼ dW̃ⱼ` ⇒ DSᵢ martingales.
- **Arbitrage** (Def 5.4.6): `X(0)=0`, `P{X(T)≥0}=1`, `P{X(T)>0}>0` (equiv. to beating the money-market). Ex. 5.4.4: two stocks / one BM with inconsistent Sharpe ratios ⇒ infinite arbitrage (`d(DX)=μD dt`, μ>0).
- **First FTA** (Thm 5.4.7): market model **no-arbitrage ⟺ risk-neutral measure exists** (⇐ proven in text via martingale argument; existence of a solution of the market-price-of-risk equations is the operative test).
- **Second FTA** (Thm 5.4.9): model **complete ⟺ risk-neutral measure is unique** (⟺ market-price-of-risk eqns have a unique solution ⟺ the m×d volatility matrix A has full "row/column" structure with m≥d, invertible square case m=d; hedging equations (5.4.29) `ΣᵢΔᵢD Sᵢ σᵢⱼ=Γⱼ` require solving `A^tr y=c`, j=1..d, m unknowns). *(Prior extraction's framing "existence⇔no-arbitrage, uniqueness⇔completeness" is correct.)*
- **Dividends, continuous** (5.5): stock `dS=(α−δ)Sdt+σSdW` where `δ`=dividend yield (α = rate were dividends reinvested); market price of risk Θ=(α−R)/σ unchanged; **portfolio** `dX=R X dt+ΔσS[Θdt+dW]` (dividend reinvested into the dX); same risk-neutral pricing formula `D V=Ẽ[D(T)V(T)|F(t)]`. Under P̃ **`dS=(R−δ)Sdt+σS dW̃`** — discounted price is NOT a martingale; rather `e^{∫₀ᵗδ du}D(t)S(t)` is the martingale (reinvested-discounted stock). Constant coefficients: `S(T)=S(t)exp{σ(W̃(T)−W̃(t))+(r−δ−½σ²)(T−t)}`; call price `c(t,x)=Ẽe^{−rτ}(x e^{σ√τY+(r−δ−½σ²)τ}−K)⁺` = **`x e^{−δτ}N(d₊)−Ke^{−rτ}N(d₋)`** with `d±=[log(x/K)+(r−δ±½σ²)τ]/(σ√τ)` (first term scaled by `e^{−δτ}`). *(Prior extraction correct: replaces r by r−δ and scales first term by e^{−δτ}.)*
- **Dividends, lumps** (5.5.3/4): at times tⱼ stock drops `S(tⱼ)=S(tⱼ−)(1−aⱼ)`, aⱼ∈[0,1] F(tⱼ)-measurable; between dates GBM. Constant coeffs: `S(T)=S(0)·Π_{j=0}^{n}(1−a_{j+1})·exp{σW̃(T)+(r−½σ²)T}` ⇒ price by replacing initial price with **`S(0)Π(1−a_j)`** (product over dividend dates before T) in the classical BSM formula; at interior t include only future dividends.
- **Forwards & futures** (5.6): zero-coupon `B(t,T)=(1/D(t))Ẽ[D(T)|F(t)]`; **forward price** `For_S(t,T)=S(t)/B(t,T)` (no-arbitrage replication, (5.6.2)); value of a forward written at K over (tₖ,tⱼ) `=S(tⱼ)−(S(tₖ)/B(tₖ,T))B(tⱼ,T)`. **Futures**: marking-to-market cash flow `Fut(tₖ₊₁,T)−Fut(tₖ,T)`; **`Fut_S(t,T)=Ẽ[S(T)|F(t)]`** (5.6.6) — a P̃-martingale with `Fut(T,T)=S(T)`; value of any long/short futures position over an interval is zero (Theorem 5.6.5, via MRT Cor 5.3.2).
- **Forward–futures spread** (5.6.11): `For_S(0,T)−Fut_S(0,T) = (1/B(0,T))·Coṽ(D(T),S(T))` under P̃. Zero if rates nonrandom (B deterministic ⇒ D(T) in F(0), covariance 0); positive correlation D–S (higher S ⟺ lower rates) ⇒ futures price < forward price. All correlations under the risk-neutral measure.
- **Cash-flow valuation** (Remark 5.6.6 / (5.6.10)): `V(t)=(1/D(t))Ẽ[∫ₜᵀ D(u)dC(u)|F(t)]` — generalizes (5.2.30) to a dividend/cash-flow stream (lumps or continuous). State-price-density picture: `D(t)Z(t)` bridges P̃-expectations back to P.

## Verified three-case summary of the FTA (5.7)
1. **No RN measure** (market-price-of-risk eqns unsolvable): model has arbitrage — reject. 2. **Multiple RN measures**: incomplete; non-hedgeable claims priced non-uniquely (credit derivatives typically here). 3. **Unique RN measure** (unique Θ solution): complete; `V(t)=(1/D(t))Ẽ[D(T)V(T)|F(t)]` justified.

---

# Verification findings (prior extraction vs. this pass)
## Errors / corrections introduced
1. **Page-number mapping (major):** brief's ch4/ch5 PNG ranges are wrong by ≈19–20 (Ch4 = p-139…227, Ch5 = p-228…281; p-120 = Ch3 book p.100). Sibling/chapter agents should use the corrected mapping.
2. **Girsanov integrability condition omitted:** the theorem needs `E∫₀ᵀΘ²(u)Z²(u)du<∞` (equiv. the Z-integral (5.2.14) being a well-defined martingale); add Novikov-type assumption.
3. **Filtration caveat:** MRT (5.3.1/5.4.2) requires the filtration be generated by the BM; Girsanov (5.2.3) allows a larger filtration. The hedging argument uses Corollary 5.3.2 (both), not MRT alone. Prior extraction blurred this.
4. **Indexing:** multidim market price of risk is one Θ_j per Brownian motion j (d of them), with equations `αᵢ−R=ΣⱼσᵢⱼΘⱼ` (m equations); prior text indexed by stock `i` — notational, corrected to j.
5. **Dividends clarification:** under P̃ a dividend stock has drift R−δ (not R); the martingale is the *reinvested* discounted process `e^{∫δ}DS`, not DS. Worth stating explicitly (prior text only gave the price formula).

## Confirmed correct (spot-checked against text layer; no change needed)
- Itô isometry, QV of an integral, integral-is-a-martingale; Itô–Doeblin (1-d and Itô-process forms); generalized GBM solution; Vasicek solution; CIR expectation/variance & "no closed form / nonnegative"; BSM PDE, solution, d±, delta/theta/gamma/vega, Δ=c_x, forward value `x−e^{−r(T−t)}K`, forward price, put–call parity.
- Girsanov 1-d & multidim statements & RN derivative process; RN pricing formula (both (5.2.30) & (5.2.31)); MRT 1-d & multidim; hedging Δ=Γ/(σDS); FTA 1 & 2; dividend BSM (r−δ, e^{−δτ} scale, lump S(0)Π(1−aⱼ)); forward & futures prices; forward–futures spread `Coṽ(D(T),S(T))/B(0,T)`; cash-flow valuation formula.

## Known gaps in the verified file (this pass, without vision)
- Exact per-page rendering of a handful of Greek/Θ glyphs in *this* verification was taken from the clean pdftotext layer (sections/eq-numbers preserved) rather than from re-reading each PNG, because the vision backend failed after the first successful frame. A spot vision re-scan of `p-139..p-227` and `p-228..p-281` (using the CORRECTED mapping) is the recommended follow-up for pixel-level confidence.
