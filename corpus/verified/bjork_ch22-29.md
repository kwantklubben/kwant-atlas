# Björk, *Arbitrage Theory in Continuous Time* (3rd ed., OUP 2009) — Chapters 22–29: Verified, Math-Corrected Extraction

**Scope:** Printed pages ≈ p350–p460 (Ch 22–29) + p337–546 (includes Ch 21 tail + Appendices A–C). Chapter boundaries verified against `bjork.txt` page headers and the book's table of contents.

**Verification method:** Full-text cross-reference of `/tmp/atlas_extract/bjork.txt` (pdftotext layer, clean for this typeset book) against the canonical math for every formula in Ch 22–29, plus cross-check against the prior `/tmp/atlas_extract/derivative_pricing.md`. Direct vision-read of the PNG renders was **blocked by the image-analysis backend** (it cannot reach local file paths — 404 — nor private/localhost URLs, and full-page data-URLs exceed practical inlining). Verification below therefore rests on the clean text layer, which is internally consistent and matches every standard result. Any doubt is flagged inline.

---

## CHAPTER LISTING — VERIFIED (corrects the task's chapter list)

The task brief listed chapters as "…Martingale Models for Short Rate; **Inflation & Interbank**; HJM Framework; **Musiela Parametrization**; Change of Numeraire; LIBOR and Swap Market Models". **This does not match the 3rd edition.** Verified actual Ch 22–29:

| Ch | Title | Start page |
|----|-------|-----------|
| 22 | Bonds and Interest Rates | 350 |
| 23 | Short Rate Models | 364 |
| 24 | Martingale Models for the Short Rate | 374 |
| 25 | Forward Rate Models (HJM; §25.3 Musiela Parametrization) | 388 |
| 26 | Change of Numeraire ★ | 396 |
| 27 | LIBOR and Swap Market Models | 417 |
| 28 | Potentials and Positive Interest ★ | 438 |
| 29 | Forwards and Futures | 452 |

There is **no** "Inflation & Interbank" chapter and **no** standalone "Musiela" chapter in this edition (Musiela is §25.3). (Inflation/foreign-currency material lives in Ch 17; interbank/LIBOR conventions in Ch 22 §22.2.1 and Ch 27.) If a different edition was intended, that edition must be specified — the verified content below is for the 2009 3rd edition, which is the edition the provided pages/text represent.

---

## Ch 22. Bonds and Interest Rates (p350–363) — VERIFIED CORRECT

Definitions (all confirmed):
- Zero-coupon T-bond `p(t,T)`, `p(t,t)=1`; coupon bonds = static portfolios of ZCBs: `p(t)=K·p(t,Tn)+Σ_{i=1}^n c_i p(t,T_i)` (eq 22.13); standardized: `p(t)=K[p(t,Tn)+rδΣp(t,T_i)]` (22.14).
- **LIBOR forward** `L(t;S,T)=−(p(t,T)−p(t,S))/((T−S)p(t,T))`; **LIBOR spot** `L(S,T)=−(p(S,T)−1)/((T−S)p(S,T))` (Def 22.2). (Derived from `1+(T−S)L=p(t,S)/p(t,T)`.)
- Continuously compounded forward `R(t;S,T)=−(log p(t,T)−log p(t,S))/(T−S)`; instantaneous forward `f(t,T)=−∂_T log p(t,T)`; short rate `r(t)=f(t,t)`.
- Money account `B(t)=exp(∫_0^t r ds)`, `dB=rB dt` (Def 22.3).
- `p(t,T)=p(t,s)·exp(−∫_s^T f(t,u)du)`, in particular `p(t,T)=exp(−∫_t^T f(t,s)ds)` (Lemma 22.4).
- **Floating-rate bond:** `p(t)=p(t,T0)` (eq 22.15); par at `T0`.
- **Interest-rate swap** (forward, settled in arrears), `d_i=Rδ (i<n)`, `d_n=1+Rδ`: `Π(t)=K p(t,T0)−K Σ d_i p(t,T_i)` (Prop 22.6); **swap rate** `R=(p(0,T0)−p(0,Tn))/(δ Σ_{i=1}^n p(0,T_i))` (Prop 22.7).
- **Yield:** ZCB `y(t,T)=−log p(t,T)/(T−t)`; yield to maturity; **Macaulay duration** `D=(Σ T_i c_i e^{−yT_i})/p`; `dp/dy = −D·p` (Prop 22.11); **convexity** `C=∂²p/∂y²`.
- **Toolbox Prop 22.5** (relation between dynamics; under any measure): with `dp=p m dt+p v dW`, `df=α dt+σ dW`, `dr=a dt+b dW`:
  - `α = v_T·v − m_T`, `σ = −v_T` (22.4)
  - `a = f_T(t,t)+α(t,t)`, `b = σ(t,t)` (22.5)
  - Forward-specified bond dynamics: `dp = p[ r + A + (1/2)||S||² ]dt + p S dW`, with `A=−∫_t^T α(t,s)ds`, `S=−∫_t^T σ(t,s)ds` (22.6).
  - Money account = rolling-over just-maturing bonds (`dV=rV dt`, 22.12).

---

## Ch 23. Short Rate Models (p364–373) — VERIFIED CORRECT

- Model `dr=μ(t,r)dt+σ(t,r)dW̄` under P (23.1); money account `dB=rB dt`; bonds are derivatives of r.
- **Answer: bond prices are NOT uniquely determined by the P-dynamics of r** (market incomplete; M=0 traded assets excluding bank, R=1 random source). Need market price of risk.
- Bond `p(t,T)=F(t,r(t);T)`, `F(T,r;T)=1`. Portfolio of an S-bond and T-bond kills dW ⇒ **market price of risk**:
  - `(α_T(t)−r(t))/σ_T(t) = λ(t)` for all T — **same λ for all maturities** (Prop 23.1); λ has dimension "risk premium per unit volatility".
- **Term structure equation (Prop 23.2):** `F_t^T + {μ−λσ}F_r^T + (1/2)σ²F_rr^T − rF^T = 0`, `F^T(T,r)=1`. λ is exogenous, not pinned by the model.
- **Risk-neutral valuation (Prop 23.3):** `p(t,T)=F(t,r(t);T)=E^Q_{t,r}[e^{−∫_t^T r(s)ds}]` with Q-dynamics `dr={μ−λσ}ds+σdW` (23.21–23.22). Different λ ⇒ different Q ⇒ different bond prices.
- **General claim** `X=Φ(r(T))`: `Π(t;Φ)=F(t,r(t))` solves same PDE with `F(T,r)=Φ(r)`; `F=E^Q_{t,r}[e^{−∫r ds}Φ(r(T))]` (Prop 23.4).
- Forward rate under Q: `f(t,T)=E^Q[r(T)e^{−∫r}]/E^Q[e^{−∫r}]` (Exercise 23.2 form).

---

## Ch 24. Martingale Models for the Short Rate (p374–387) — VERIFIED CORRECT

- **Result 24.1.1:** term structure + all derivatives determined by Q-dynamics of r (only `μ−λσ` matters under Q). **Martingale modeling** = specify r directly under Q.
- **Standard Q-dynamics (verified):**
  1. Vasicek `dr=(b−ar)dt+σdW`, a>0
  2. CIR `dr=a(b−r)dt+σ√r dW`
  3. Dothan `dr=ardt+σr dW`
  4. Black–Derman–Toy `dr=Θ(t)r dt+σ(t)r dW`
  5. Ho–Lee `dr=Θ(t)dt+σdW`
  6. Hull–White extended Vasicek `dr=(Θ(t)−a(t)r)dt+σ(t)dW`, a(t)>0
  7. Hull–White extended CIR `dr=(Θ(t)−a(t)r)dt+σ(t)√r dW`
- **Inversion of the yield curve:** fit model params α so `p(0,T;α)=p̂(0,T)` ∀T (24.27). Diffusion same under P & Q; Q-drift params from market prices.
- **Affine term structure (ATS):** `p(t,T)=F(t,r;T)=e^{A(t,T)−B(t,T)r}` (Def 24.1). If `μ(t,r)=α(t)r+β(t)` and `σ²(t,r)=γ(t)r+δ(t)`, then (Prop 24.2):
  - `B_t + α(t)B − (1/2)γ(t)B² = −1`, `B(T,T)=0` (**Riccati**, 24.24)
  - `A_t = β(t)B − (1/2)δ(t)B²`, `A(T,T)=0` (24.25)
  - In the time-homogeneous case ATS ⇒ affine μ,σ² necessary. **All listed models except Dothan and BDT are affine.**
- **Vasicek term structure (Prop 24.3):** `B(t,T)=(1/a)(1−e^{−a(T−t)})`; `A(t,T)={B(t,T)−T+t}(ab−σ²/2)/a² − σ²B²(t,T)/(4a)`. r Gaussian, bond prices lognormal.
- **Ho–Lee (Prop 24.4):** `B=T−t`; exact fit with `Θ(t)=∂_T f̂(0,t)+σ²t`. Bond option (Prop 24.5): `c(t,T,K,S)=p(t,S)N(d)−p(t,T)K N(d−σ_p)`, `d=(1/σ_p)log[p(t,S)/(p(t,T)K)]+σ_p/2`, `σ_p=σ(S−T)√T`.
- **CIR (Prop 24.6):** `F^T(t,r)=A_0(T−t)e^{−B(T−t)r}`, `γ=√(a²+2σ²)`, `B(x)=2(e^{γx}−1)/[(γ+a)(e^{γx}−1)+2γ]`, `A_0(x)=[2γe^{(a+γ)x/2}/((γ+a)(e^{γx}−1)+2γ)]^{2ab/σ²}`.
- **Hull–White extended Vasicek (Prop 24.8):** `dr={Θ(t)−ar}dt+σdW`, `B(t,T)=(1/a)(1−e^{−a(T−t)})`; choose `Θ(T)=f̂_T(0,T)+ġ(T)+a{f̂(0,T)+g(T)}`, `g(t)=σ²/(2a²)(1−e^{−at})²` ⇒ **exact fit to initial forward curve** (Lemma 24.7) — why HW is popular.
- **Bond option HW & Vasicek (Prop 24.9):** `c(t,T,K,S)=p(t,S)N(d)−p(t,T)K N(d−σ_p)`, `σ_p²=[(1−e^{−a(S−T)})/a]²·[σ²/(2a)](1−e^{−2a(T−t)})`.

---

## Ch 25. Forward Rate Models (HJM) (p388–395) — VERIFIED CORRECT

- Model whole forward curve: `df(t,T)=α(t,T)dt+σ(t,T)dW̄`, `f(0,T)=f̂(0,T)` (25.1–25.2) — **perfect fit to initial curve by construction** (no yield-curve inversion). Bonds via `p(t,T)=exp(−∫_t^T f(t,s)ds)`.
- **HJM drift condition under P (Theorem 25.1):** NA ⇒ ∃ d-dim λ with
  `α(t,T) = σ(t,T)·∫_t^T σ(t,s)' ds − σ(t,T)λ(t)` (25.4).
- **HJM drift condition under Q (Prop 25.2):** `α(t,T)=σ(t,T)·∫_t^T σ(t,s)' ds` (25.9). Volatility σ freely specifiable; drift determined. Algorithm: choose σ, then α, observe f̂(0,·), integrate.
- **Constant σ ⇒ Ho–Lee:** `r(t)=f̂(0,t)+σ²t²/2+σW(t)`, `dr={f̂_T(0,t)+σ²t}dt+σdW` (exact fit).
- **Musiela parameterization (§25.3, Prop 25.4):** with time-to-maturity `x=T−t`, `r(t,x)=f(t,t+x)`; **Musiela equation:**
  `dr(t,x) = {F r(t,x) + D(t,x)}dt + σ_0(t,x)dW`, where `F=∂/∂x`, `σ_0(t,x)=σ(t,t+x)`, `D(t,x)=σ_0(t,x)∫_0^x σ_0(t,s)ds` (25.20) — an infinite-dimensional SDE.
- Exercise results worth noting: Hull–White as HJM has `df(t,T)=α dt+σ e^{−a(T−t)}dW`; deterministic-σ HJM ⇒ Gaussian rates, lognormal bonds; foreign-rate drift correction `α_f=σ_f(∫σ_f ds−σ_X)`.

---

## Ch 26. Change of Numeraire ★ (p396–416) — VERIFIED CORRECT

- **Invariance lemma** (26.1): S self-financing ⇔ Z=S/β self-financing for any positive Itô β.
- **Likelihood process** Q0→Q1: `L^1_0(t)=(S_0(0)/S_1(0))·(S_1(t)/S_0(t))` (26.18); **Girsanov kernel = volatility difference** `φ^1_0(t)=σ_1(t)−σ_0(t)` (26.20).
- **T-forward measure (Def 26.6, Prop 26.7):** `dQ^T/dQ = p(t,T)/(B(t)p(0,T))` (26.21); Girsanov kernel = T-bond volatility `v(t,T)`. `Q=Q^T` iff r deterministic (Lemma 26.9).
- **Pricing:** `Π(t;X)=p(t,T)E^T[X|F_t]` (Prop 26.8). General: `Π(t;X)=S_1(t)E^{Q_1}[X/S_1(T)|F_t]`.
- **Expectation hypothesis (Lemma 26.10):** `f(t,T)` is a `Q^T`-martingale, so `f(t,T)=E^T[r(T)|F_t]` — holds under Q^T, **not** under P or Q.
- **Geman–El Karoui–Rochet (GER, Prop 26.11/26.12):** for European call `X=max[S(T)−K,0]`:
  `Π(0;X)=S(0)Q^S(S(T)≥K) − K·p(0,T)Q^T(S(T)≥K)` (26.29). If volatility of `Z_{S,T}=S/p(·,T)` is deterministic: `Π(0;X)=S(0)N(d_1)−K·p(0,T)N(d_2)` (26.39), with `Σ²_{S,T}(T)=∫_0^T|σ_{S,T}(t)|²dt`, `d_2=(ln[S(0)/(Kp(0,T))]−Σ²/2)/√Σ²`, `d_1=d_2+√Σ²`.
- **Hull–White bond option (Prop 26.13):** call on T2-bond, maturity T1:
  `Π(0;X)=p(0,T2)N(d_1)−K·p(0,T1)N(d_2)`, `Σ² = σ²/(2a³)(1−e^{−2aT1})(1−e^{−a(T2−T1)})²` (26.49).
- **Short-rate Q^T-dynamics (26.53):** `dr={Θ(t)−ar−σ²B(t,T)}dt+σdW^T`; `r(T)~N[f(t,T), σ²/(2a)(1−e^{−2a(T−t)})]` under Q^T (Prop 26.14).
- **General Gaussian forward rates (Prop 26.15):** `Π(0;X)=p(0,T1)N(d_1)−K·p(0,T0)N(d_2)`, `σ_{T1,T0}(t)=−∫_{T0}^{T1}σ(t,s)ds`.
- **Caps/floors (§26.8):** caplet `X_i=Kδ max[L(T_{i−1},T_i)−R,0]`; a caplet ⇔ `1+δR` put options on the T_i-bond struck at `1/(1+δR)`.
- **Numeraire portfolio (§26.9, Prop 26.16):** value process X of the log-optimal portfolio; `Π_t/X_t` is a P-martingale, `Π(t;Z)=X_t E^P[Z/X_T|F_t]`.

---

## Ch 27. LIBOR and Swap Market Models (p417–437) — VERIFIED CORRECT

- **LIBOR forward** `L_i(t)=(1/α_i)(p_{i−1}(t)−p_i(t))/p_i(t)` (27.1); **caplet** `X_i=α_i·max[L_i(T_{i−1})−R,0]` (27.2); cap = sum of caplets.
- **Black-76 caplet (Def 27.2):** `Capl^B_i(t)=α_i·p_i(t){L_i(t)N(d_1)−R N(d_2)}`, `d_1=(1/(σ_i√(T_i−t)))ln(L_i(t)/R)+σ_i√(T_i−t)/2`, `d_2=d_1−σ_i√(T_i−t)` (27.4–27.6). Market quotes implied **flat** vs **spot/forward** volatilities.
- **LMM (Def 27.5):** `dL_i(t)=L_i(t)σ_i(t)dW^i(t)` under its own `Q^i` (27.11). **`L_i` is a Q^i-martingale** (Lemma 27.4). Caplet prices are Black-type (Prop 27.6): `Capl_i(t)=α_i·p_i(t){L_i(t)N(d_1)−R N(d_2)}` with `Σ²_i(t,T)=∫_t^T|σ_i(s)|²ds`.
- **Terminal (Q^N) measure & existence (Prop 27.7):** `dL_i(t)=−L_i(t)[Σ_{k=i+1}^N α_k L_k(t)/(1+α_k L_k(t))·σ_k(t)σ_i'(t)]dt+L_i(t)σ_i(t)dW^N(t)` (27.30). Girsanov kernel between consecutive measures: `α_i L_i(t)/(1+α_i L_i(t))·σ_i'(t)` (27.27); likelihood `η^i_{i−1}=a_i(1+α_i L_i)`, `a_i=p_i(0)/p_{i−1}(0)` (27.21). Note: book defines `η^j_i=dQ^j/dQ^i=(p_i(0)/p_j(0))(p_j(t)/p_i(t))` (27.20); prior extraction's index convention (`dQ^i/dQ^{i−1}`) is the reciprocal — same content, flagged for clarity.
- **Discrete savings account (§27.6):** `B(T_n)=Π_{k=0}^{n−1}[1+α_{k+1}L(T_k,T_{k+1})]` (27.42); `dQ^B/dQ^N=p(0,T_N)B(T_N)` (Prop 27.8).
- **Swaps (§27.7):** forward swap rate `R_{nN}(t)=(p_n(t)−p_N(t))/S_{nN}(t)`, **accrual factor** `S_{nN}(t)=Σ_{i=n+1}^N α_i p_i(t)` (27.47–27.49); payer-swap value `PS^n_N(t;K)=(R^n_N(t)−K)S^n_N(t)`.
- **Black-76 swaption (Def 27.13):** `PS^n_N(t)=S^n_N(t){R^n_N(t)N(d_1)−K N(d_2)}`.
- **SMM (Def 27.15):** `dR_{nk}(t)=R_{nk}(t)σ_{n,k}(t)dW_{nk}(t)` under `Q^k_n`; swap rate is Q-martingale under the accrual-factor numeraire (Lemma 27.14). Cannot model all swap rates simultaneously (Remark 27.9.1).
- **Calibration:** choose deterministic σ_i with `σ̄_i=(1/T_i)∫_0^{T_{i−1}}|σ_i(s)|²ds` (27.33/27.34); Euler and log-Euler (ln-L_i) discretizations for MC (27.35/27.37).

---

## Ch 28. Potentials and Positive Interest ★ (p438–451) — VERIFIED CORRECT

- **Stochastic discount factor** `Z_t=e^{−∫_0^t r_s ds}·L_t`, `L_t=dQ_t/dP_t` (28.1); `dZ_t=−r_t Z_t dt+dM_t` (28.2); `p(t,T)=E^P[Z_T|F_t]/Z_t` (28.3).
- **Prop 28.1:** if r>0 and `lim_{T→∞}p(0,T)=0`, then Z is a **probabilistic potential** (nonneg supermartingale, `E[Z_t]→0`). Converse holds.
- **Flesaker–Hughston (Prop 28.2, Theorem 28.4):** with `X(t,T)=E^P[Z_T|F_t]`, `p(t,T)=X(t,T)/X(t,t)`. For a **positive term structure** (`∂_T p≤0`, `lim_{T→∞}p=0`), there exist positive martingales `M(t,T)` and positive deterministic Φ with
  `p(t,T)=∫_T^∞ Φ(s)M(t,s)ds / ∫_t^∞ Φ(s)M(t,s)ds` (28.8); canonical `M(t,T)=−X_T(t,T)=E^P[r_T Z_T|F_t]`, `Φ(s)=−p_T(0,s)` (28.9–28.10). **Converse** (Jin–Glasserman, Prop 28.5).
- §28.3 Changing base measure; §28.5 **Rogers' Markov potential approach** (Rogers 1997) via resolvents — generates positive-rate models. (Prior extraction's mention of "Rogers' Markov potential" confirmed.)

---

## Ch 29. Forwards and Futures (p452–457) — **CORRECTIONS APPLIED**

Prior extraction stated: *"forward price f(t;T,Y)=E^Q[X]; futures price F(t;T,Y)=E^Q[X] when short rate deterministic."* **This is incorrect/reversed.** Verified:

- **Forward price (Prop 29.3):**
  `f(t;T,Y)=Π(t;Y)/p(t,T)=E^{Q^T}_{t,x}[Y]` (29.4/29.7) — i.e. forward price = *forward-measure* expectation (equivalently `(1/p(t,T))E^Q[Y e^{−∫_t^T r ds}]`). It equals `E^Q[Y]` **only when the short rate is deterministic**.
- **Futures price (Prop 29.6):** `F(t;T,Y)=E^Q_{t,X_t}[Y]` (29.12) — the futures price is a **Q-martingale** and this holds **unconditionally** (no determinism assumption).
- **Equality:** `f(t;T,Y)=F(t;T,Y)=E^Q_{t,X_t}[Y]` iff the short rate is deterministic (29.13). In general forward ≠ futures (daily "marking to market" of futures introduces the financing/convexity difference).
- Futures contract = asset with price `Π(t)=0` and dividend `D(t)=F(t;T,Y)`, `F(T;T,Y)=Y` (Def 29.5); spot value of an existing forward at s = `Π(s;Y)−p(s,T)f(t;T,Y)`.

**Correct pithy statement:** *Forward price = E^Q^T[Y]; futures price = E^Q[Y]; they coincide iff r is deterministic.*

---

## FLAGGED ITEMS / GAPS

1. **[CORRECTION] Ch 29 forward/futures formulas** — the prior extraction assigned `E^Q` to the forward price unconditionally and to the futures price only under deterministic r. Correct: futures = `E^Q[Y]` always; forward = `E^T[Y]=Π(t;Y)/p(t,T)` (equals `E^Q[Y]` only when r deterministic). See Ch 29 above.
2. **[DISCREPANCY] Task chapter list** names "Inflation & Interbank" and "Musiela Parametrization" as separate chapters. Neither exists as a chapter in the 3rd edition; verified actual Ch 22–29 titles (table above). Musiela is §25.3; interbank/LIBOR is Ch 22 §22.2 + Ch 27; inflation/FX is Ch 17.
3. **[MINOR] Ch 27 terminal-measure likelihood index** — book convention `η^j_i=dQ^j/dQ^i=(p_i(0)/p_j(0))(p_j(t)/p_i(t))`; prior extraction wrote the reciprocal with a mixed index convention. Same substance; use the book's `η^{i−1}_i=(p_i(0)/p_{i−1}(0))(p_{i−1}(t)/p_i(t))=a_i(1+α_i L_i(t))`, `a_i=p_i(0)/p_{i−1}(0)`.
4. **[METHOD NOTE] PNG vision-read blocked.** The image-analysis backend could not ingest `/tmp/atlas_pages/bjork/p-*.png` (returns 404 for local paths, rejects private/localhost URLs, and full-page data-URLs are impractically large). All math above was instead verified against the clean `pdftotext` layer (`bjork.txt`), which is consistent and matches every standard result for this typeset OUP book. Recommend re-running a direct vision pass on the PNGs if pixel-level OCR confidence on the rendered glyphs is required.
5. **[GAP] Ch 24 bond-option for Ho–Lee and Ch 26 caps** are covered qualitatively; the extraction does not give Ho–Lee bond-option Σ_p explicitly in §26 context — included here (see Ch 24 Prop 24.5).

**Overall verdict:** The prior `derivative_pricing.md` Ch 22–28 extraction is accurate and math-sound (all formulas confirmed). The substantive error is confined to Ch 29 (forward/futures). Ch 22–28 stand as verified; Ch 29 corrected as above.
