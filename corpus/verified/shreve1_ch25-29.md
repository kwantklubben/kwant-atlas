# Shreve I — Chapters 25–29 (combined/lecture edition): Math-Verified Extraction

> Scope & document identity (IMPORTANT — read first).
> The task brief assigned "Shreve I ch25–29" to rendered pages p-295..p-332 with the
> topic list "Fixed-Income Exotics / Random Walk Revisited / Reflection / First Passage /
> Perpetual American Options." That assignment does NOT match this PDF. Verified by vision
> reading of the actual pages and by chapter markers in the pdftotext layer
> (`shreve1.txt`): **PDF page 295 is *Ch 30 Hull–White model* (printed p.293), not Ch 25.**
> The real **Chapters 25–29 occupy PDF pages ≈ 249–294 (printed pp. 247–292)** and their
> content is:
> - Ch 25 **American Options** (perpetual American put, first-passage times, reflection
>   principle, drift adjustment, linear complementarity, hedging) — this single chapter
>   carries the themes the brief attributed to four separate chapters;
> - Ch 26 Options on dividend-paying stocks; Ch 27 Bonds, forward contracts, futures;
> - Ch 28 Term-structure models (incl. HJM); Ch 29 Gaussian processes.
>
> The PNG page index = printed page + 2 (front matter). Every formula below was checked
> against the PDF text layer, cross-checked by OCR/vision on the key pages, and verified
> analytically. This file is the first math-verified extraction of these chapter numbers;
> the referenced "existing extraction" `atlas_extract/shreve.md` maps a *different*
> numbering (Vol I ch1–11 + Vol II ch1–10) and contains none of this content (see
> *Corrections & flags* at the end).

---

## Ch 25. American Options  (PDF p-249..p-264; printed pp. 247–262)

One-factor risk-neutral GBM stock:  dS = rS dt + σS dB,  S(0)=x.
Intrinsic value of a put at t: (K − S(t))⁺. (Ch 25 is continuous-time; it is the companion
to the discrete random-walk theory of the earlier volumes.)

### 25.1 Preview of perpetual American put
Exercise threshold L ∈ [0,K]; exercise at first time stock is ≤ L:
- τ_L = min{t ≥ 0 : S(t) = L}
- v_L(x) = E[e^{−rτ_L}(K − S(τ_L))⁺] = K − x  if x ≤ L;  = (K−L)·E[e^{−rτ_L}]  if x > L.
Plan: compute v_L(x), then maximize over L ⇒ needs the law of τ_L.

### 25.2 First passage times for BM — first method (reflection principle)
τ = min{t ≥ 0 : B(t) = x}, x > 0. Uses (from "Ch 20") joint density of running maximum
M(t)=max_{0≤u≤t}B(u) and B(t):
IP{M(t)∈dm, B(t)∈db} = (2(2m−b))/(t√(2πt)) · exp(−(2m−b)²/(2t)) dm db,  m>0, b<m.
Hence IP{τ≤t} = IP{M(t)≥x} and the **first-passage density** (verified):
> IP{τ ∈ dt} = x/(t√(2πt)) · e^{−x²/(2t)} dt  =  x/√(2π) · t^{−3/2} e^{−x²/(2t)} dt.
**Laplace transform** (for α>0, x>0):  E e^{−ατ} = e^{−x√(2α)}.
(Ref. Karatzas & Shreve *Brownian Motion and Stochastic Calculus*, pp. 95–96.)

### 25.3 Drift adjustment
B̃(t) = βt + B(t);  Z(t) = exp{−βB(t) − ½β²t} = exp{−βB̃(t) + ½β²t}.
τ̃ = min{t≥0: B̃(t)=x}. Change measure only up to finite T: P̃(A)=∫_A Z(T)dP. Under P̃,
B̃ is a (nondrifted) BM on [0,T], and (optional stopping of the exponential martingale at
τ̃∧t) gives the **drift-adjusted first-passage density**:
> IP{τ̃ ∈ dt} = x/(t√(2πt)) · exp(−(x−βt)²/(2t)) dt,  t>0 (all t, since T arbitrary).

### 25.4 Drift-adjusted Laplace transform (verified)
> E e^{−ατ̃} = e^{xβ − x√(2α+β²)},  α>0, x>0.
(obtained from the nondrifted result by replacing α ↦ α+½β² and factoring e^{xβ}).
Letting α↓0 (Monotone Convergence; e^{−ατ̃}→1_{τ̃<∞}):  **P{τ̃<∞} = 1 if β ≥ 0,
and = e^{2xβ} < 1 if β < 0.** (Level x>0; a negative drift pulls the path away from the
level, so hitting is not a.s.)

### 25.5 First passage times — second method (martingale/optional sampling)
Y(t)=exp{σB(t)−½σ²t} is a martingale, so Y(t∧τ) is; 1=Y(0∧τ)=E Y(t∧τ).
On {τ<∞}: Y(t∧τ)→e^{σx−½σ²τ}; on {τ=∞}: →0 (DCT). Setting σ=√(2α) re-derives
E e^{−ατ}=e^{−x√(2α)}.

### 25.6–25.7 Perpetual American put (the headline solved result)
S(t)=x·exp{(r−½σ²)t+σB(t)}. Write the exponent as σ[(β-drift) t + B(t)] and hit x ⇔
drift-adjusted level. Setting γ = 2r/σ² and L* = 2rK/(σ²+2r) = (γ/(γ+1))K
(0 < L* < K). Value:
> v(x) = K − x  for 0 ≤ x ≤ L*  (exercise region);
> v(x) = (K − L*)(x/L*)^{−2r/σ²}  for x ≥ L*  (continuation region).

Verification (all re-checked):
- Continuation region: v = C x^{−γ}, γ=2r/σ². The Black–Scholes operator
  Lv := −rv + rxv′ + ½σ²x²v″ = Cx^{−γ}[−r − rγ + ½σ²γ(γ+1)] = 0 (since ½σ²γ(γ+1)=r(γ+1)).
- Exercise region: v=K−x ⇒ Lv = −r(K−x) + rx(−1) = −rK.
- Constant: value matching v(L*)=K−L* ⇒ C=(K−L*)(L*)^{2r/σ²}; maximize C in L gives L*=2rK/(σ²+2r).
- **Smooth pasting**: v′(x)=−1 for x<L*; for x>L*,
  v′(x)=−(2r/σ²)(K−L*)(L*)^{2r/σ²}x^{−2r/σ²−1}, and both one-sided limits at L* equal −1
  (checked: (2r/σ²)(K−L*)/L* = 1 since (K−L*)/L* = σ²/(2r)). [Figure 25.4]

**Linear complementarity / smallest-supermartingale characterization** (Ch 25.7):
for all x ≠ L*:  (a) rv − rxv′ − ½σ²x²v″ ≥ 0;  (b) v ≥ (K−x)⁺;  (c) at each x at least
one of (a),(b) is an equality. Two regions: C={x: v>(K−x)⁺} = "continue"; boundary L*;
exercise (or at L*) means "stop." Equivalently e^{−rt}v(S(t)) is (1) a supermartingale,
(2) ≥ e^{−rt}(K−S(t))⁺, (3) the smallest such process (the canonical three-property proof
uses the stopped-supermartingale inequality + Fatou in Case II S(0)>L*).

### 25.8 Hedging the put
Consumption-hedging portfolio: dX = Δ dS + r(X − ΔS)dt − C dt, equivalently
d(e^{−rt}X)= −e^{−rt}C dt + e^{−rt}ΔσS dB.  d(e^{−rt}v(S)) = −rK e^{−rt}1_{S(t)<L*} dt
+ e^{−rt}σS v′(S) dB. Hedge:  Δ(t)=v′(S(t));  consume C(t)=rK·1_{S(t)<L*}.  If S(t)<L*
then Δ=−1 (short one share, hold K in money market, consume the money-market interest rK).

### 25.9–25.10 Perpetual contingent claims; perpetual American call
General payoff h(S(t)): v(x)=sup_τ Eˣ[e^{−rτ}h(S(τ))], sup over stopping times.
Perpetual American call, h(S)=(S−K)⁺:  **v(x)=x for all x** (Theorem 10.63), achieved as a
limit; there is **no** optimal exercise time (Eˣ e^{−rτ}(S(τ)−K)⁺ < Eˣ e^{−rτ}S(τ) ≤ x = v(x)).

### 25.11–25.12 Finite expiration (put & general American contingent claim)
Value v(t,x)=sup_{t≤τ≤T} Eˣ[e^{−r(τ−t)}h(S(τ))]; free-boundary problem; v, v_t, v_x
continuous across boundary, v_xx jumps. VI on [0,T]×[0,∞): (a) rv − v_t − rxv_x − ½σ²x²v_xx ≥ 0;
(b) v ≥ h(x); (c) equality holds at every point. Optimal exercise time:
τ = min{t ≥ 0 : v(t,S(t)) = h(S(t))}. e^{−rt}v(t,S(t)) is the smallest supermartingale
dominating e^{−rt}h(S(t)). [Put figure: continuation region satisfies BSM equation with
v(T,x)=(x−K)⁺, v=K−x in the stop region with v_t=0,v_x=−1,v_xx=0 and Lv=−rK.]

---

## Ch 26. Options on dividend-paying stocks  (PDF p-265..p-268; printed ~263–266)

### 26.1 American option with convex payoff (Theorem 1.64)
dS(t)=r(t)S(t)dt+σ(t)S(t)dB(t), r(t)≥0 a.s., no dividends. h convex on x≥0, h(0)=0
(e.g. h(x)=(x−K)⁺). Then an American claim paying h(S(t)) at exercise need **not be
exercised early** — waiting to expiration loses nothing. Proof: for 0≤λ≤1 convexity gives
h(λx)=h((1−λ)0+λx) ≤ (1−λ)h(0)+λh(x)=λh(x); using discounted-stock martingale S(t)/Γ(t)
and conditional Jensen, the European claim value dominates the American intrinsic value.

### 26.2 Dividend-paying stock
r, σ constant; dividend coefficient δ, 0<δ<1; dividend at t₁∈(0,T).
S(t)= S(0)e^{(r−½σ²)t+σB(t)} (0≤t≤t₁), and = (1−δ)S(t₁)e^{(r−½σ²)(t−t₁)+σ(B(t)−B(t₁))} (t₁<t≤T).
American **call**: in (t₁,T] not optimal to exercise ⇒ value is the usual BS formula
v(t,x)=xN(d₊(T−t,x)) − K e^{−r(T−t)}N(d₋(T−t,x)),
d±(T−t,x) = [log(x/K) + (T−t)(r ± σ²/2)]/(σ√(T−t)).
Value just before the dividend (drop by factor (1−δ) at t₁):
> w(t₁,x) = max{ (x−K)⁺,  v(t₁, (1−δ)x) }.
**Theorem 2.65**: for 0≤t≤t₁ the value is w(t,S(t)) with
w(t,x)=E^{t,x}[e^{−r(t₁−t)}w(t₁,S(t₁))], which solves the BS PDE on [0,t₁]
(−rw + w_t + rxw_x + ½σ²x²w_xx=0) with terminal condition above and boundary w(t,0)=0.
Hedge: Δ(t)=w_x(t,S(t)) on [0,t₁], Δ(t)=v_x(t,S(t)) on (t₁,T].

### 26.3 Hedging at time t₁
- Case I: v(t₁,(1−δ)x) ≥ (x−K)⁺ → don't exercise; w(t₁,x)=v(t₁,(1−δ)x) and
  Δ(t₁)=w_x(t₁,x) = (1−δ)v_x(t₁,(1−δ)x) = (1−δ)Δ(t₁+). Reaching this post-dividend position
  = reinvesting the dividend received: Δ(t₁+)=(1/(1−δ))Δ(t₁)=Δ(t₁)+[δΔ(t₁)S(t₁)/((1−δ)S(t₁))].
- Case II: v(t₁,(1−δ)x) < (x−K)⁺ → owner exercises just before the dividend, receives x−K;
  the seller's hedge has x−K pre-dividend and pockets the drop v(t₁,(1−δ)x) below intrinsic
  if unexercised, continuing the hedge.

---

## Ch 27. Bonds, forward contracts and futures  (PDF p-269..p-276; printed ~267–274)

Setup: dS(t)=r(t)S(t)dt+σ(t)S(t)dW under risk-neutral P; every P-martingale is an integral
vs W. Accumulation factor Γ(t)=exp(∫_0^t r(u)du).
Zero-coupon bond:  B(t,T) = E[(Γ(t)/Γ(T))|F(t)] = E[exp(−∫_t^T r(u)du)|F(t)].
dB(t,T)=r(t)B(t,T)dt + (Γ(t)ψ(t))dW(t) for some process ψ (bond is itself tradable; any two of
{stock, money market, bond} hedge any claim). If r nonrandom: B(t,T)=exp(−∫_t^T r(u)du), dB=rB dt.

### 27.1 Forward price
T-forward price F(t) = S(t)/B(t,T) (choose F(t) so the forward has zero value at t:
E[(1/Γ(T))(S(T)−F(t))|F(t)]=0 ⇒ F(t)=S(t)/B(t,T)). Remark: F(t) is the agreed delivery price,
not the (zero) contract value.

### 27.2 Hedging a forward
Value at t of a forward entered at 0: V(t)=E[(Γ(t)/Γ(T))(S(T)−F(0))|F(t)] = S(t) − F(0)B(t,T).
Hedge (short forward): short F(0) bonds at 0 → income F(0)B(0,T)=S(0); buy 1 share; at T
portfolio worth S(T)−F(0); deliver. (Short forward can alternatively be hedged with stock+money
market but that needs a term-structure model.)

### 27.3–27.4 Futures
Marking to market keeps value zero. Discrete: at t_{k+1} long receives ψ(t_{k+1})−ψ(t_k).
Continuum no-cost condition: E[∫_t^T (1/Γ(u))dψ(u)|F(t)] = 0, 0≤t≤T.
**Definition 27.1** T-future price ψ(t) is F(t)-adapted with (a) ψ(T)=S(T) a.s. and
(b) that martingale/zero condition. **Theorem 3.66** the unique process is
> ψ(t) = E[S(T)|F(t)],  0≤t≤T   (a P-martingale).
(Proof: (b) ⇔ ψ is a martingale.) Cash flow from 0 to T sums to ψ(T)−ψ(0)=S(T)−ψ(0); taking
delivery at T costs total ψ(0).

### 27.5 Forward–future spread
ψ(0)−F(0) = E[S(T)] − S(0)/E[1/Γ(T)]. If 1/Γ(T) and S(T) uncorrelated ⇒ ψ(0)=F(0).
Positive correlation (stock rises with falling rates) ⇒ ψ(0) ≤ F(0): long-future holder receives
income when stock rises but reinvests at declining rates, and pays when rates rise — compensated
by a lower future price.

### 27.6 Backwardation and contango
dS=μS dt+σS dW. Under risk-neutral measure dS=rS dt+σS dW̃, S(T)=S(0)e^{(r−½σ²)T+σW̃(T)}.
Since 1/Γ(T)=e^{−rT} nonrandom, uncorrelated ⇒ future price ψ(t)=F(t)=e^{r(T−t)}S(t),
ψ(0)=e^{rT}S(0). Market expected future spot: E P S(T)=e^{μT}S(0).
- μ>r ⇒ ψ(0) < E P S(T): **normal backwardation**;
- μ<r ⇒ ψ(0) > E P S(T): **contango**.

---

## Ch 28. Term-structure models  (PDF p-277..p-285; printed ~275–283)

Short rate r(t) adapted to W; Γ(t)=exp(∫_0^t r(u)du). Primitives = default-free zero-coupon
bonds B(t,T) paying $1 at T (0≤t≤T≤T*).

**Theorem (FTAP, "0.67")** Model is arbitrage-free iff ∃ measure P̃ ~ P such that for every T,
B(t,T)/Γ(t) is a P̃-martingale. Since dB(t,T)=ν(t,T)B dt + σ(t,T)B dW (ν=mean return), P is
risk-neutral iff ν(t,T)=r(t); else change measure.

### 28.1–28.3 Factor method & terminology
Start from factor SDE dX=a dt+b dW; set r(t)=r(X(t)); define B(t,T)=E[exp(−∫_t^T r(u)du)|F(t)];
(ch 27) B has mean return r ⇒ no arbitrage. Interest-rate-dependent assets: coupon bond
Σ_{k: t<T_k} P_k B(t,T_k); call on zero: E[(Γ(t)/Γ(T₁))(B(T₁,T)−K)⁺|F(t)].
Terminology: term-structure model ⇒ family {B(t,T):0≤t≤T≤T*}; yield to maturity
Y(t,T)=−log B(t,T)/(T−t) (B exp{(T−t)Y}=1).

### 28.4–28.5 Forward rates
Forward rate agreement (borrow $1 at T, repay at T+Δ, rate fixed at t): portfolio of buying a
T-zero and shorting B(t,T)/B(t,T+Δ) units of the (T+Δ)-zero; effective rate
R(t,T,T+Δ) = −[log B(t,T+Δ) − log B(t,T)]/Δ.
Instantaneous forward rate (Δ→0):  **f(t,T) = −∂_T log B(t,T)**, so
B(t,T)=exp(−∫_t^T f(t,u)du). Recovering short rate:  **r(t) = f(t,t)**.

### 28.6–28.8 Heath–Jarrow–Morton
Forward curve given as df(t,T)=α(t,T)dt+σ(t,T)dW with σ(u,T)>0; B(t,T)=exp(−∫_t^T f(t,u)du).
With α*(t,T)=∫_t^T α(t,u)du and **σ*(t,T)=∫_t^T σ(t,u)du** (bond volatility), Itô gives
dB(t,T)=B(t,T)[r(t) − α*(t,T) + ½(σ*(t,T))²]dt − σ*(t,T)B(t,T)dW.
- P is a risk-neutral measure ⇔ **α*(t,T) = ½(σ*(t,T))²**; differentiating in T ⇔
  **α(t,T) = σ(t,T)σ*(t,T)**.  (7.1)/(7.2) — equivalent.
- If (7.1) fails, pass to P̃ via Girsanov with dW̃=Θ(t)dt+dW (Z(t)=exp(−∫Θ dW−½∫Θ²du),
  P̃(A)=∫_A Z(T*)dP). Bond mean return under P̃ is r ⇔ **α*(t,T)=½(σ*)²+σ*Θ** (7.3) ⇔
  **α(t,T)=σ(t,T)σ*(t,T)+σ(t,T)Θ(t)** (7.4).
**Theorem 7.68 (HJM)**: the forward-rate family is arbitrage-free iff ∃ adapted Θ(t) satisfying
(7.3) [equiv (7.4)]. Market price of risk = [−α*+½(σ*)²]/σ*, and no-arbitrage requires it be
independent of maturity T; then Θ=−[−α*+½(σ*)²]/σ*.
Under the risk-neutral measure (drop Θ, W̃↦W):
> dB(t,T)=r(t)B(t,T)dt − σ*(t,T)B(t,T)dW̃(t);
> df(t,T)=σ(t,T)σ*(t,T)dt + σ(t,T)dW̃(t),  σ(t,T)=∂_T σ*(t,T), σ*(T,T)=0.
Implementation needs only initial market data B(0,T) and bond volatilities σ*(t,T); Θ, α and the
market measure never appear (Remark 28.3: vol is unaffected by change of measure).

---

## Ch 29. Gaussian processes  (PDF p-287..p-294; printed ~285–292)

**Definition 29.1** X(t), t≥0 Gaussian if every finite set (X(t₁),…,X(t_n)) is jointly normal.
Distribution determined by mean m(t)=EX(t) and covariance ρ(s,t)=E[(X(s)−m(s))(X(t)−m(t))]
(covariance matrix Σ; joint density and MGF given in standard form
E exp{Σ u_k X(t_k)}=exp{u·mᵀ+½u·Σ·uᵀ}).

### 29.1 Example: Brownian motion
W is Gaussian: m=0, ρ(s,t)=s∧t (write W(t)=W(s)+(W(t)−W(s)), independent increments).

**Theorem 1.69 (integral w.r.t. BM, deterministic integrand)**  Let σ(u) be nonrandom;
X(t)=∫_0^t σ(u)dW(u) is a **Gaussian process** with m(t)=0 and
ρ(s,t)=∫_0^{s∧t} σ²(u)du. Proof (sketch) via m.g.f.: d(e^{uX})=ue^{uX}σ dW+½u²e^{uX}σ²ds,
E e^{uX(s)}=exp{½u²∫_0^sσ²}; two-time m.g.f. shows (X(s),X(t)) jointly normal with
Cov=∫_0^{s∧t}σ². Remarks: normality is the hard part (that's why m.g.f.'s); means/variances need
only Itô isometry E X²(s)=∫_0^sσ² du and E[X(s)(X(t)−X(s))]=0. If σ is *stochastic*, X need not
be Gaussian, though it is still a martingale with E X²=∫Eσ². When σ nonrandom, X is also Markov:
conditioned on F(s), X(t) is N(X(s), ∫_s^t σ²).

**Theorem 1.70 (time-integrated Gaussian)**  σ,h nonrandom; X(t)=∫_0^t σ(u)dW(u),
Y(t)=∫_0^t h(u)X(u)du. Then Y is a Gaussian process, m_Y=0, and (verified by direct two-fold
integration over regions, Fig. 29.1a–c):
> ρ_Y(s,t) = ∫_0^{s∧t} σ²(v) · [∫_v^s h(y)dy] · [∫_v^t h(y)dy] dv.
(Sanity check σ=h=1, s≤t gives ∫_0^s(s−v)(t−v)dv = s²t/2 − s³/6 = Cov(∫_0^sW,∫_0^tW).)
Remark 29.4: Y is **neither Markov nor a martingale** —
E[Y(t)|F(s)] = Y(s) + X(s)∫_s^t h(u)du.

---

## Corrections & flags

1. **Page-range / chapter-title premise of the brief is wrong for this PDF.**
   The brief maps ch25–29 to rendered pages 295–332; those pages are actually
   Ch 30 (Hull–White), Ch 31 (CIR) and the start of Ch 32 (BGM area) — verified by vision
   (p-295 shows "Ch 30 Hull and White model," printed p.293). The genuine chapters 25–29 sit at
   PDF pages ≈249–294 (printed 247–292), mapped via chapter headers in the pdftotext layer.
   If a sibling/consumer expects fixed-income *applications* (Hull–White/CIR/Gaussian term
   structure) under "ch25–29," that content is in Ch 30–31 at p295+ and is NOT here.
2. **Chapter-topic list mismatch.** The brief's five topics (Random Walk Revisited / Reflection
   Principle / First Passage Times / Perpetual American Options) are all realized inside the
   actual **Ch 25 "American Options"** (§25.1–25.7). There is no separate per-topic chapter for
   them in the 25–29 block; conversely actual Ch 29 is *Gaussian processes* and Ch 28 is
   *term-structure/HJM*, which the brief's title list does not mention.
3. **No pre-existing extraction to correct.** The referenced existing extraction
   `atlas_extract/shreve.md` covers a different numbering (Vol I ch1–11 discrete + Vol II
   ch1–10 continuous) and contains nothing for combined-edition chapters 25–29. No other
   per-chapter extraction file was found under /tmp/atlas_extract. This markdown is therefore a
   fresh, math-verified extraction rather than a patch of a prior file.
4. **No mathematical errors found in the source text layer** after verification. The raw
   pdftotext layer is internally consistent with every checked result: first-passage density
   and Laplace transforms (nondrifted and drifted), perpetual-put value/boundary/smooth
   pasting/linear complementarity/hedge, dividend-stock recursion and delta, forward–future
   price relations, HJM drift conditions (7.1)–(7.4) and Theorem 7.68, and the two Gaussian
   integral theorems. Ambiguities resolved during reading (pdftotext re-orders equation tokens
   and mangles superscripts/subscripts): e.g. the perpetual-put exponent is exactly −2r/σ² and
   L* = 2rK/(σ²+2r); the drift-adjusted Laplace factor is e^{xβ−x√(2α+β²)} (not any drift-only
   variant); the HJM integral conditions have the explicit ∫_t^T form given above.
5. **Numbering quirks preserved.** Theorems carry the lecture-edition's global numbering
   (Theorem 1.64/2.65/3.66/7.68/1.69/1.70, "Theorem 0.67"); sections are locally numbered.
   Kept verbatim so cross-references inside the source resolve.

*Verification basis: /tmp/atlas_pages/shreve1/p-249..p-294 (vision + local OCR of the PDF's own
text layer in /tmp/atlas_extract/shreve1.txt), plus analytical re-derivation of every displayed
result. No source files were modified.*
