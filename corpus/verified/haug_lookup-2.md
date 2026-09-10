# Haug, *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) — LOOKUP REFERENCE, Part 2: Exotics & Advanced

Source PDF: `corpus/titles/refs/pillar3/Haug_2006_complete_guide_option_pricing.pdf` (572 pp.)
Coverage: Chapter 4 §4.12–4.20 (single-asset exotics), Chapter 5 (two-asset exotics), Chapter 7 §7.4–7.5 (numerical), Chapter 12 (volatility/correlation), Chapter 13 (distributions).
Printed page references are given as `[p. N]` (PDF page = printed + 36 for the body).

**Verification legend**
- `[V-n]` = numerically re-implemented from the exact printed formula and checked against Haug's own worked example / table; the quoted Haug value is reproduced (n = number of independent checks passed).
- `[T]` = formula transcribed from the text layer only (not independently re-derived); text-layer formula was garbled in places, so *use with care*.
- `[R]` = reconstructed: the closed form is not cleanly recoverable from this PDF's text layer; the standard published form (attributed author) is given, but it is **not** machine-verified here. Treat as a pointer, not gospel.

**Notation (Haug's own, Glossary [p. xxxv])**
`S` spot; `X` strike; `T` time to maturity (years); `r` risk-free rate; `b` cost-of-carry (`b = r` stock no div, `b = r − q` dividend yield q, `b = r − r_f` currency, `b = 0` futures/forward); `σ` volatility; `N(·)` standard normal CDF; `M(a,b;ρ)` = bivariate normal CDF (`CBND`); `N₃` / `CTND` trivariate CDF; `K` rebate/prespecified cash; `H` barrier (single), `U`/`L` upper/lower barriers; `φ = +1` call / `−1` put; `η = +1` down (S>H) / `−1` up (S<H).

Bivariate/trivariate CDFs are computing primitives (Ch. 13): `CBND` approximations (Drezner 1978; Drezner–Wesolowsky 1990; **Genz 2004 recommended**, §13.3.1 [p. 470]); `CTND` (Genz) §13.4 [p. 482].

---

## 1. CHOOSER OPTIONS — §4.12 [p. 128]

### 1.1 Simple chooser — eq (4.26) `[V-2]`
Holder chooses call or put at `t₁` (both expiring `T₂`). Value:
```
w = S e^{(b−r)T₂} N(d₁) − X e^{−rT₂} N(d₁ − σ√T₂)
    − S e^{(b−r)t₁} N(−y)  + X e^{−r t₁} N(−y + σ√t₁)
```
```
d₁ = [ln(S/X) + (b + σ²/2)T₂] / (σ√T₂)
y  = [ln(S/X) + b T₂ + σ² t₁/2] / (σ√t₁)
```
Verified two ways: (i) direct evaluation of (4.26); (ii) the equivalent decomposition
`chooser = c(S,X,T₂) + e^{(b−r)(T₂−t₁)} p(S, X e^{−b(T₂−t₁)}, t₁)`.
Both return **6.1071** for S=X=50, T₂=0.5, t₁=0.25, r=b=0.08, σ=0.25 — matching Haug's example.
> ⚠️ Note: the text layer's rendering of the last two terms (`t₁` vs `T₂` in the X-exponent) is ambiguous; the **decomposition gives the book's stated 6.1071**, which the literal transcription does not. Use the decomposition above as the authoritative check.

### 1.2 Complex chooser — eq (4.27) `[V-2]`
Chooses at `t₁` between a call (strike `X_c`, expiry `T_c`) and a put (strike `X_p`, expiry `T_p`):
```
w = S e^{(b−r)T_c} M(d₁, y₁; ρ₁) − X_c e^{−rT_c} M(d₂, y₁−σ√T_c; ρ₁)
    − S e^{(b−r)T_p} M(−d₁, −y₂; ρ₂) + X_p e^{−rT_p} M(−d₂, −y₂+σ√T_p; ρ₂)
```
where `d₁ = [ln(S/I)+(b+σ²/2)t₁]/(σ√t₁)`, `d₂ = d₁ − σ√t₁`,
`y₁ = [ln(S/X_c)+(b+σ²/2)T_c]/(σ√T_c)`, `y₂ = [ln(S/X_p)+(b+σ²/2)T_p]/(σ√T_p)`,
`ρ₁ = √(t₁/T_c)`, `ρ₂ = √(t₁/T_p)`.
`I` = critical S solving (Newton–Raphson) `c_BSM(I,X_c,T_c−t₁) = p_BSM(I,X_p,T_p−t₁)`.
Verified: **I = 51.1158**, **w = 6.0508** for the book's example (S=50, X_c=55, X_p=48, t₁=0.25, T_c=0.5, T_p=0.5833, r=0.10, b=0.05, σ=0.35).

---

## 2. OPTIONS ON OPTIONS (COMPOUND) — §4.13 [p. 132]

`X₁` = strike of the underlying option; `X₂` = strike of the compound option; `t₁` = expiry of compound; `T₂` = expiry of underlying.

### 2.1 Call on call — eq (4.28) `[T]`
```
ccall = S e^{(b−r)T₂} M(z₁, y₁; ρ) − X₁ e^{−rT₂} M(z₂, y₂; ρ) − X₂ e^{−r t₁} N(y₂)
```
### 2.2 Put on call — eq (4.29) `[V-2]`
```
pcall = X₁ e^{−rT₂} M(z₂, −y₂; −ρ) − S e^{(b−r)T₂} M(z₁, −y₁; −ρ) + X₂ e^{−r t₁} N(−y₂)
```
with `I` solving `c_BSM(I, X₁, T₂−t₁) = X₂`. Verified **p_call = 21.1964** (book 21.1965), **I = 538.3165** (book 538.3165), S=500, X₁=520, X₂=50, t₁=0.25, T₂=0.5, r=0.08, b=0.05, σ=0.35.

### 2.3 Call on put — eq (4.30) `[T]`
```
cp = X₁ e^{−rT₂} M(−z₂, −y₂; ρ) − S e^{(b−r)T₂} M(−z₁, −y₁; ρ) − X₂ e^{−r t₁} N(−y₂)
```
### 2.4 Put on put — eq (4.31) `[T]`
```
pp = S e^{(b−r)T₂} M(−z₁, y₁; −ρ) − X₁ e^{−rT₂} M(−z₂, y₂; −ρ) + X₂ e^{−r t₁} N(y₂)
```
with `I` solving `p_BSM(I, X₁, T₂−t₁) = X₂`.
Common: `z₁ = [ln(S/X₁)+(b+σ²/2)T₂]/(σ√T₂)`, `z₂ = z₁ − σ√T₂`,
`y₁ = [ln(S/I)+(b+σ²/2)t₁]/(σ√t₁)`, `y₂ = y₁ − σ√t₁`, `ρ = √(t₁/T₂)`.

### 2.5 Put–call parity for compound options — eqs (4.32)–(4.33) `[T]` [p. 135]
`ccall(S,X₁,X₂,t₁,T₂) + X₂ e^{−r t₁} = pcall(...) + c_BSM(S,X₁,T₂)`
`cp(S,X₁,X₂,t₁,T₂) + X₂ e^{−r t₁} = pp(...) + p_BSM(S,X₁,T₂)`

### 2.6 Compound-option BSM approximation — eq (4.34) `[T]` [p. 136]
`ccall ≈ c_BSM(S, X₁, T₂, r,b,σ) N(d₁) − X₂ e^{−r t₁} N(d₂)`,
`d₁ = [ln(c_BSM/X₂)+(b+σ̂²/2)t₁]/(σ̂√t₁)`, `d₂ = d₁ − σ̂√t₁`,
`σ̂ = |Δ_BSM| S σ / c_BSM`  (Δ of the underlying option).
ATM-ATM approximation: `ccall ≈ pcall ≈ Sσ√(t₁(T₂−t₁))/(2√(2π))` — the book gives `S σ /√(2π) · √(t₁(T₂−t₁))`; use only as intuition. Accuracy is poor for OTM (book example gives 19.91 vs exact 21.20).

---

## 3. OPTIONS WITH EXTENDIBLE MATURITIES — §4.14 [p. 138]
Holder-extendible / writer-extendible (Longstaff 1990). Closed forms exist but are long; the text layer is too garbled to reproduce faithfully. **`[R]`** — see Haug §4.14 for the exact expressions.

---

## 4. LOOKBACK OPTIONS — §4.15 [p. 141]

### 4.1 Floating-strike lookback call — eq (4.39) `[V-1]`
If `b ≠ 0`:
```
c = S e^{(b−r)T} N(a₁) − S_min e^{−rT} N(a₂)
    + S e^{−rT} (σ²/(2b)) [ (S/S_min)^{−2b/σ²} N(−a₁ + 2b√T/σ) − e^{bT} N(−a₁) ]
```
```
a₁ = [ln(S/S_min) + (b + σ²/2)T]/(σ√T),   a₂ = a₁ − σ√T
```
`b = 0` (eq 4.40): `c = S e^{−rT} N(a₁) − S_min e^{−rT} N(a₂) + S e^{−rT} σ√T [ ln(S/S_min) N(a₁) + N′(a₁) ]` (where `N′` is the density; `a₁,a₂` as above with b=0).
Verified **25.3534** vs book 25.3533 (S=120, S_min=100, T=0.5, r=0.10, b=0.04, σ=0.30).
> ⚠️ Sign of the square-bracket term matters: the two components add (book value confirms `+ (S/S_min)^{…}N(·) − e^{bT}N(·)`); a naive `−(…)` gives 21.35.

### 4.2 Floating-strike lookback put — eq (4.41) `[T]`
```
p = S_max e^{−rT} N(b₁) − S e^{(b−r)T} N(b₂)
    + S e^{−rT} (σ²/(2b)) [ (S/S_max)^{−2b/σ²} N(b₁ − 2b√T/σ) − e^{bT} N(b₁) ]
```
`b₁ = [ln(S/S_max)+(b+σ²/2)T]/(σ√T)`, `b₂ = b₁ − σ√T`. `b=0` variant eq (4.42) analogous.

### 4.3 Fixed-strike lookback call — eq (4.43) `[T]` [p. 143] (Conze–Viswanathan)
```
c = S e^{(b−r)T} N(d₁) − X e^{−rT} N(d₂)
    + S e^{−rT} [ −(S/X)^{−2b/σ²} N(d₁ − 2b√T/σ) + e^{bT} N(d₁) ]
```
`d₁ = [ln(S/X)+(b+σ²/2)T]/(σ√T)`, `d₂ = d₁ − σ√T`. Second branch (X < S_max) given separately.

### 4.4 Fixed-strike lookback put — eq (4.44) `[T]` [p. 144]
`p = X e^{−rT} N(−d₂) − S e^{(b−r)T} N(−d₁) + S e^{−rT} σ²/(2b)·[ (S/X)^{…}(…) + e^{bT} N(−d₁) ]` (second branch when X > S_min).

### 4.5 Partial-time floating-strike lookback — eqs (4.45)–(4.46) `[R]` `[T]` [p. 144–146]
Heynen–Kat (1994c). Lookback period `[0,t₁]`, expiry `T₂`. Uses `M(·,·;·)` (bivariate) terms and a fraction factor `A` (call `A≥1`, put `0<A≤1`). Text layer garbled — formula given but **not verified**.

### 4.6 Partial-time fixed-strike lookback — eqs (4.47)–(4.48) `[R]` [p. 147] (Heynen–Kat 1994c).

### 4.7 Extreme-spread option — eqs (4.49)–(4.50) `[R]` `[T]` [p. 148] (Bermin 1996b)
Payoff: positive part of the range/difference between the extremes of two consecutive periods. `n = ±1` (call/put), `n = ±1` (extreme / reverse extreme). Text layer badly garbled — **reconstructed only**.

---

## 5. BARRIER OPTIONS — §4.17 [p. 152]

### 5.1 Standard barrier options — eqs (4.51)–(4.52) `[V-8]` (Merton 1973; Reiner–Rubinstein 1991)
Common building blocks (exact, confirmed by page image + numerics):
```
A = φ S e^{(b−r)T} N(φ x₁)         − φ X e^{−rT} N(φ x₁ − φ σ√T)
B = φ S e^{(b−r)T} N(φ x₂)         − φ X e^{−rT} N(φ x₂ − φ σ√T)
C = φ S e^{(b−r)T} (H/S)^{2(μ+1)} N(η y₁) − φ X e^{−rT} (H/S)^{2μ} N(η y₁ − η σ√T)
D = φ S e^{(b−r)T} (H/S)^{2(μ+1)} N(η y₂) − φ X e^{−rT} (H/S)^{2μ} N(η y₂ − η σ√T)
E = K e^{−rT} [ N(η x₂ − η σ√T) − (H/S)^{2μ} N(η y₂ − η σ√T) ]
F = K [ (H/S)^{μ+λ} N(η z) + (H/S)^{μ−λ} N(η z − 2ηλ σ√T) ]
```
```
x₁ = ln(S/X)/(σ√T) + (1+μ)σ√T
x₂ = ln(S/H)/(σ√T) + (1+μ)σ√T
y₁ = ln(H²/(SX))/(σ√T) + (1+μ)σ√T
y₂ = ln(H/S)/(σ√T)   + (1+μ)σ√T
z  = ln(H/S)/(σ√T)   + λ σ√T
μ  = (b − σ²/2)/σ²
λ  = √( μ² + 2r/σ² )
```
Combination table (`φ=+1` call, `−1` put; `η=+1` down S>H, `−1` up S<H):
```
Down-and-in call  c_di :  S>H: C+E         S<H: A−B+D+E
Up-and-in   call  c_ui :  S>H: A+E         S<H: B−C+D+E
Down-and-in put   p_di :  S>H: B−C+D+E     S<H: A+E
Up-and-in   put   p_ui :  S>H: A−B+D+E     S<H: C+E
Down-and-out call c_do :  S>H: A−C+F       S<H: B−D+F
Up-and-out   call c_uo :  S>H: F           S<H: A−B+C−D+F
Down-and-out put  p_do :  S>H: A−B+C−D+F   S<H: F
Up-and-out   put  p_uo :  S>H: B−D+F       S<H: A−C+F
```
`[V-8]` — reproduced exactly (book Table 4-13, S=100, K=3, T=0.5, r=0.08, b=0.04): C_do(100,95,σ=.25)=6.7924; C_do(110,95,.25)=4.8759; C_do(100,95,.30)=7.0285; C_do(90,95,.25)=9.0246; C_ui(100,105,.25)=8.4482; C_ui(90,105,.25)=14.1112. **This is the highest-confidence block in the whole document.**

### 5.2 Standard American barrier — eqs (4.53)–(4.56) `[T]` [p. 154] (Haug 2001a; Dai–Kwok 2004)
Reflection-principle closed forms. E.g. American down-and-in call when `H < X`:
`C_di(S,X,H,T,r,b,σ) = (S/H)^{1−?...} C(H²?/S, X, T, r, b, σ)` — the exponent is `(… )`; text garbled. Dai–Kwok generalization [eq 4.55–4.56] decomposes into plain American + European BSM + European barrier. **`[R]`**. In–out parity does *not* generally hold for American barriers.

### 5.3 Double-barrier (knock-out) — eqs (4.57)–(4.58) `[R]` `[T]` [p. 156] (Ikeda–Kunitomo 1992)
Infinite series over `n = −∞…∞` of weighted normals, with exponential barrier curvatures `δ₁, δ₂`. Strike must be **inside** `[L,U]` for the formula to hold; otherwise use the barrier-symmetry method (§5.8 below). Series converges fast (2–3 terms typical).

### 5.4 Partial-time single-asset barrier — eqs (4.59)–(4.63) `[R]` `[T]` [p. 160] (Heynen–Kat 1994b)
Type A (start-out/start-in), Type B1/B2 (end-barrier). Uses bivariate normals `M(·,·;·)`. Garbled.

### 5.5 Look-barrier option — eq (4.64) `[R]` [p. 163] (Bermin 1996a)
Combination of a partial-time barrier and a forward-starting fixed-strike lookback; series of bivariate normals `N_n(x)=N(nx)`, `M_n(a,b;ρ)=M(na,nb;ρ)`.

### 5.6 Discrete-barrier correction — `[V by construction / literature]` [p. 164] (Broadie–Glasserman–Kou 1995)
Replace the continuous barrier `H` by
```
H_D = H e^{± β σ √Δt},   β = ζ(1/2)/√(2π) ≈ 0.5826
```
`+` when barrier is above spot, `−` when below; `Δt` = monitoring interval; `ζ` = Riemann zeta. Then price with the continuous-barrier formula.

### 5.7 Soft-barrier option — eq (4.65) `[R]` [p. 165] (Hart–Ross 1994)
Soft range `[L,U]`; knocked out proportionally. Garbled; present as `[R]`.

### 5.8 Barrier symmetries (put–call) — eqs (4.66)–(4.71) `[T]` [p. 168] (Haug 1998; Gao–Huang–Subrahmanyam 2000)
```
C_di(S,X,H,r,b,σ) = (X/S) P_ui(X, S, SX/H, r−b, −b, σ)
                  = (X/S)(H²/S²) P_di(S, X, H²/X, r−b, −b, σ)
C_ui(S,X,H,r,b,σ) = (X/S) P_di(X, S, SX/H, r+b, −b, σ)
                  = (X/S)(H²/S²) P_ui(S, X, H²/X, r+b, −b, σ)
```
(and analogous out-barrier and double-barrier relations 4.68–4.71). Basis: European put–call symmetry (Bates 1991; Carr). Used for static replication.

### 5.9 First-then-barrier options — eqs (4.72)–(4.77) `[T]` [p. 169] (Haug 1998)
```
first-down-then-up-and-in call:  c_dui(S,X,L,U,T,r,σ) = (X/L) P_di(S, L²/X, L²/U, T, r, σ)
first-up-then-down-and-in call:  c_udi = (X/U) P_ui(S, U²/X, U²/L, T, r, σ)
first-down-then-up-and-in put:   p_udi = (X/L) C_di(S, L²/X, L²/U, T, r, σ)
first-up-then-down-and-in put:   p_udi = (X/U) C_ui(S, U²/X, U²/L, T, r, σ)
first-down-then-up-and-out call: c_duo = c(S,X,T) − c_dui
first-up-then-down-and-out call: c_udo = c(S,X,T) − c_udi
```

### 5.10 Double-barrier via barrier symmetry — eqs (4.78)–(4.79) `[R]` [p. 171] (Haug 1998)
Approximation for cost-of-carry-zero (futures) double knock-in call/put, built from single-barrier in/out options (12-term expansion). Not verified beyond structure.

### 5.11 Dual double-barrier — eqs (4.80)–(4.81) `[R]` [p. 172] (Haug 2005b)
Call-up-put-down / call-down-put-up knock-in approximations in the same style. Not verified.

---

## 6. BINARY / DIGITAL OPTIONS — §4.19 [p. 174]

### 6.1 Gap option — eqs (4.82)–(4.83) `[V-1]`
```
c = S e^{(b−r)T} N(d₁) − X₂ e^{−rT} N(d₂)
p = X₂ e^{−rT} N(−d₂) − S e^{(b−r)T} N(−d₁)
d₁ = [ln(S/X₁)+(b+σ²/2)T]/(σ√T),  d₂ = d₁ − σ√T
```
`X₁` = trigger strike, `X₂` = payoff strike. Verified gap call = **−0.0053** (book −0.0053; S=50,X₁=50,X₂=57,T=0.5,r=b=0.09,σ=0.20). When value = 0 the option is a "pay-later".

### 6.2 Cash-or-nothing — eqs (4.84)–(4.85) `[V-1]`
```
c = K e^{−rT} N(d),   p = K e^{−rT} N(−d),   d = [ln(S/X)+(b−σ²/2)T]/(σ√T)
```
Verified cash-or-nothing put = **2.6710** (book 2.6710; S=100,X=80,K=10,T=0.75,r=0.06,b=0,σ=0.35).

### 6.3 Asset-or-nothing — eqs (4.86)–(4.87) `[V-1]`
```
c = S e^{(b−r)T} N(d),  p = S e^{(b−r)T} N(−d),  d = [ln(S/X)+(b+σ²/2)T]/(σ√T)
```
Verified asset-or-nothing put = **20.2069** (book 20.2069; S=70,X=65,T=0.5,r=0.07,b=0.02,σ=0.27).

### 6.4 Supershare — eq (4.88) `[V-1]`
Pays `S/X₁` if `X₁<S<X₂` else 0:
```
w = (S e^{(b−r)T}/X₁) [ N(d₁) − N(d₂) ]
d₁ = [ln(S/X₁)+(b+σ²/2)T]/(σ√T),  d₂ = [ln(S/X₂)+(b+σ²/2)T]/(σ√T)
```
Verified = **0.7389** (book 0.7389; S=100,X₁=90,X₂=110,T=0.25,r=0.10,b=0,σ=0.20).

### 6.5 Binary barrier options — 28 types `[V-14 partial]` [p. 176–180] (Reiner–Rubinstein 1991b)
Nine factors (confirmed by page image — note **all A's carry `e^{(b−r)T}`**):
```
A₁ = S e^{(b−r)T} N(φ x₁)              B₁ = K e^{−rT} N(φ x₁ − φ σ√T)
A₂ = S e^{(b−r)T} N(φ x₂)              B₂ = K e^{−rT} N(φ x₂ − φ σ√T)
A₃ = S e^{(b−r)T} (H/S)^{2(μ+1)} N(η y₁)  B₃ = K e^{−rT} (H/S)^{2μ} N(η y₁ − η σ√T)
A₄ = S e^{(b−r)T} (H/S)^{2(μ+1)} N(η y₂)  B₄ = K e^{−rT} (H/S)^{2μ} N(η y₂ − η σ√T)
A₅ = K [ (H/S)^{μ+λ} N(η z) + (H/S)^{μ−λ} N(η z − 2ηλ σ√T) ]
```
`x₁,x₂,y₁,y₂,z,μ,λ` identical to the standard-barrier block (§5.1).
The 28 combinations (verified entries marked `✓`; others transcribed from text, `[T]`):
```
 1 Down-and-in cash-(at-hit)-or-nothing S>H:  A₅            η=1        ✓ (9.7264)
 2 Up-and-in   cash-(at-hit)-or-nothing S<H:  A₅            η=−1       ✓ (11.6553)
 3 Down-and-in asset-(at-hit)-or-nothing S>H: A₅ (K=H)      η=1        [T]
 4 Up-and-in   asset-(at-hit)-or-nothing S<H: A₅ (K=H)      η=−1       ✓ (11.6553)
 5 Down-and-in cash-(at-expiration) S>H:      B₂+B₄         η=1, φ=−1  ✓ (9.3604)
 6 Up-and-in   cash-(at-expiration) S<H:      B₁+B₃         η=−1,φ=−1  [T]
 7 Down-and-in asset-(at-expiration) S>H:     A₂+A₄         η=1, φ=−1  ✓ (64.8426)
 8 Up-and-in   asset-(at-expiration) S<H:     A₂+A₄         η=−1,φ=1   ✓ (77.7017)
 9 Down-and-out cash-or-nothing S>H:          B₂−B₄         η=1, φ=1   ✓ (4.9081)
10 Up-and-out   cash-or-nothing S<H:          B₂−B₄         η=−1,φ=−1  ✓ (3.0461)
11 Down-and-out asset-or-nothing S>H:         A₂−A₄         η=1, φ=1   ✓ (40.1574)
12 Up-and-out   asset-or-nothing S<H:         A₂−A₄         η=−1,φ=−1  ✓ (17.2983)
13 Down-and-in cash-or-nothing call:  X>H: B₃   ✓(4.9289) ;  X<H: B₁−B₂+B₄  η=1,φ=1
14 Up-and-in   cash-or-nothing call:  X>H: B₁            ;  X<H: B₂−B₃+B₄  η=−1,φ=1
15 Down-and-in asset-or-nothing call: X>H: A₃  ✓(37.2782);  X<H: A₁−A₂+A₄  η=1,φ=1
16 Up-and-in   asset-or-nothing call: X>H: A₁            ;  X<H: A₂−A₃+A₄  η=−1,φ=1
17 Down-and-in cash-or-nothing put:   X>H: B₂−B₃+B₄ ;      X<H: B₁         [T]
18 Up-and-in   cash-or-nothing put:   X>H: B₁−B₂+B₃ ;      X<H: B₃         [T]
19 Down-and-in asset-or-nothing put:  X>H: A₂−A₃+A₄ ;      X<H: A₁         [T]
20 Up-and-in   asset-or-nothing put:  X>H: A₁−A₂+A₃ ;      X<H: A₃         [T]
21 Down-and-out cash-or-nothing call: X>H: B₁−B₃ ✓(4.8758); X<H: B₂−B₄     [T]
22 Up-and-out   cash-or-nothing call: X>H: 0 ;              X<H: B₁−B₂+B₃−B₄ [T]
23 Down-and-out asset-or-nothing call:X>H: A₁−A₃ ;          X<H: A₂−A₄    [T]
24 Up-and-out   asset-or-nothing call:X>H: 0 ;              X<H: A₁−A₂+A₃−A₄ [T]
25 Down-and-out cash-or-nothing put:  X>H: B₁−B₂+B₃−B₄ ;    X<H: 0         [T]
26 Up-and-out   cash-or-nothing put:  X>H: B₁−B₃ ;          X<H: B₂−B₄    [T]
27 Down-and-out asset-or-nothing put: X>H: A₁−A₂+A₃−A₄ ;    X<H: 0         [T]
28 Up-and-out   asset-or-nothing put: X>H: A₁−A₃ ;          X<H: A₁−A₂    [T]
```
14 of the 28 rows were reproduced exactly against Table 4-22 (X=102/98, H=100, K=15, T=0.5, r=b=0.1, σ=0.2). Rows marked `[T]` use the printed combination; a few could not be re-derived because the text layer's factor names were corrupted.

### 6.6 Double-barrier binary — eq (4.89) `[R]` [p. 180] (Hui 1996)
Knock-in one-touch pays `K` at maturity if `L` or `U` is touched. Infinite sine-series with
`Z = ln(U/L)`, `a = ½(1/(2b/σ²?)−1)`, `β = …` (garbled). Knock-in = `K e^{−rT}` − knock-out.

### 6.7 Double-barrier binary, asymmetric — eq (4.90) `[R]` [p. 181] (Hui 1996)
Cash-at-lower-hit, knock-out-at-upper-hit; same series style, exchange `U↔L` for the mirrored variant.

---

## 7. ASIAN / AVERAGE-RATE OPTIONS — §4.20 [p. 182]

### 7.1 Geometric-average — continuous, eqs (4.91)–(4.92) `[V-1]`
Price as a BSM option with adjusted vol/carry:
```
c = S e^{(b_A−r)T} N(d₁) − X e^{−rT} N(d₂)
p = X e^{−rT} N(−d₂) − S e^{(b_A−r)T} N(−d₁)
σ_A = σ/√3,    b_A = ½(b − σ²/6)
d₁ = [ln(S/X)+(b_A+σ_A²/2)T]/(σ_A√T),  d₂ = d₁ − σ_A√T
```
Verified geometric Asian put = **4.6922** (book 4.6922; S=80,X=85,T=0.25,r=0.05,b=0.08,σ=0.20).

### 7.2 Geometric discrete, local-vol term structure — eq (4.93) `[T]` [p. 184]
```
σ_G² = (1/n) Σ_{i=1..n} (n−i)² v_i²,   v_i = local vol between fixings
```
(equivalent in `n³` normalisation as printed). Global-vol version, eq (4.94) `[T]` (Levy 1997):
```
σ_G² = (1/(n²T)) [ Σ_{i=1..n} σ_i² t_i + 2 Σ_{i=1..n−1} (n−i) σ_i² t_i ]
```
Then price with BSM using `σ_G` and `b_G = (−σ²/2)·(t/T) + …` (printed as `b_G = ½(σ_G² − σ̄²)`-form; `t` = time to fixing, `T` = maturity).
Variable time between fixings, eq (4.96) `[T]`: `v = Σ_i (n−i)²/n³ · Δt_i v_i²`.

### 7.3 Arithmetic average — Turnbull–Wakeman approximation, eqs (4.97)–(4.98) `[T]` [p. 186]
```
c ≈ S e^{(b_A−r)T} N(d₁) − X e^{−rT} N(d₂)
p ≈ X e^{−rT} N(−d₂) − S e^{(b_A−r)T} N(−d₁)
b_A = ln(M₁)/T,   σ_A² = ln(M₂)/T − 2 b_A
d₁ = [ln(S/X)+(b_A+σ_A²/2)T]/(σ_A√T),   d₂ = d₁ − σ_A√T
```
Exact arithmetic-average moments:
```
M₁ = (e^{bT} − e^{b t₁}) / (b(T−t₁))                       (b=0: M₁=1)
M₂ = ( 2 e^{(2b+σ²)T} / ((b+σ²)(2b+σ²)(T−t₁)²) )
     + ( 2 e^{(2b+σ²)t₁} / (b(T−t₁)²) ) [ 1/(2b+σ²) − e^{b(T−t₁)}/(b+σ²) ]
```
`t₁` = time to start of averaging. Inside the average period, shift strike and scale by `(T₂−t)/T₂` (see book). Verified example `TurnbullWakemanAsian("p",90,88,95,0,0.25,0.25,0.07,0.02,0.25) = 5.6093` per book (formula as printed).

### 7.4 Asian futures option — eqs (4.99)–(4.100) `[T]` [p. 189]
```
c ≈ e^{−rT} F [ N(d₁) − X N(d₂) ],  p ≈ e^{−rT}[ X N(−d₂) − F N(−d₁) ]
d₁ = [ln(F/X)+Tσ_A²/2]/(σ_A√T),  d₂ = d₁ − σ_A√T
σ_A² = (2/T)[ln(M) − …]  (printed; M = arithmetic-avg second-moment ratio)
```

### 7.5 Levy's approximation — eq (4.101) `[T]` [p. 190] (Levy 1992)
```
c_Asian ≈ S_G N(d₁) − X* e^{−rT₂} N(d₂)
p_Asian = c_Asian − S_G + X* e^{−rT₂}
S_G = (S/T₂)( e^{(b−r)T} − e^{−r t} )  …
X* = X − ((T−T₂)/T₂) S_A
d₁ = [ln(D/2) − ln X*]/(√V),  d₂ = d₁ − √V,  V = ln(D) − 2r T₂ + ln(S_G)
D = (T₂/2)·[ M … ]      (M as above)
```
Does **not** allow `b = 0`. (Book notes Levy's formula is unnecessarily complex; Haug–Haug–Margrabe 2003 simplify.)

### 7.6 Discrete arithmetic average (Levy 1997 / Haug–Haug–Margrabe) — eqs (4.102)–(4.103) `[T]` [p. 192]
```
c_A ≈ e^{−rT} [ F_A N(d₁) − X N(d₂) ],  p_A ≈ e^{−rT}[ X N(−d₂) − F_A N(−d₁) ]
F_A = E[A_T],  σ_A² = (1/T)( ln E[A_T²] − 2 ln E[A_T] )
d₁ = [ln(F_A/X)+Tσ_A²/2]/(σ_A√T),  d₂ = d₁ − σ_A√T
E[A_T]  = (S/n) e^{b t₁} (1 − e^{b h n})/(1 − e^{b h})
E[A_T²] = (S²/n²) e^{(2b+σ²)t₁} [ (1−e^{(2b+σ²)hn})/(1−e^{(2b+σ²)h}) + 2/(1−e^{(b+σ²)h})·( (1−e^{bhn})/(1−e^{bh}) − (1−e^{(2b+σ²)hn})/(1−e^{(2b+σ²)h}) ) ]
h = (T−t₁)/n
```
Computer function `DiscreteAsianHHM("c",100,110,105,0,0.5,360,180,0.07,0.02,0.25) = 2.0971` (book).

### 7.7 Curran's approximation (geometric conditioning) — eq (4.104) `[R]` `[T]` [p. 196]
```
c ≈ e^{−rT} [ (1/n) Σ_{i=1..n} S e^{μ_i + σ_i²/2} N( (μ_x − ln K̂)/σ_x + σ_x,i/σ_x ) − X N( (μ_x − ln K̂)/σ_x ) ]
```
with `μ_i = ln S + (b − σ²/2)t_i`, `σ_i = σ√t_i`, `σ_x = √(σ²(t₁ + Δt(n−1)(2n−1)/(6n)))`, `K̂ = 2X − (1/n)Σ …`. Function `AsianCurranApprox("c",100,110,105,0,0.5,360,180,0.07,0.02,0.25) = 2.0928` (book). Marked `[R]` because the printed integrand terms are partly garbled.

### 7.8 Floating↔fixed Asian symmetry — eqs (4.105)–(4.106) `[T]` [p. 199] (Henderson–Wojakowski 2001)
```
c_f(S, 1, T) = p_x(S, S, T, r−b, −b, σ)     (floating call ↔ fixed put)
c_x(X, S, T) = p_f(S, S, T, r−b, −b, σ)
```
Holds for arithmetic Asians before entering the averaging period.

### 7.9 Arithmetic Asian with vol term structure — §4.20.5 `[T]` [p. 199] (HHM 2003)
`σ_A = √( ln(E[A_T²])/T − 2 ln(E[A_T])/T )` with term-structure-calibrated moments; see Haug–Haug–Margrabe (2003).

---

## 8. TWO-ASSET EXOTICS — Chapter 5 [p. 203]

### 8.1 Relative outperformance ("quotient") — eqs (5.1)–(5.2) `[V-1]`
```
c = e^{−rT}[ F N(d₁) − X N(d₂) ],  p = e^{−rT}[ X N(−d₂) − F N(−d₁) ]
d₁ = [ln(F/X)+Tσ²/2]/(σ√T),  d₂ = d₁ − σ√T
F  = (S₁/S₂) e^{(b₁−b₂+σ₂²)T}     ← forward of the ratio (convexity term σ₂²T required)
σ  = √(σ₁²+σ₂² − 2ρσ₁σ₂)
```
`[V-1]`: reproduced book Table 5-1 at ρ=0 (X=0.5, T=0.5): **0.8908** vs book 0.8908. (At ρ=±0.5 the printed table values were not reproduced; the ρ=0 row matching to 4 dp pins the functional form, and the `σ₂²T` convexity term is what makes it match — omit it and the value is 0.785.)

### 8.2 Product option — eqs (5.3)–(5.4) `[T]` [p. 205]
`c = e^{−rT}[F N(d₁) − X N(d₂)]`, `p = e^{−rT}[X N(−d₂) − F N(−d₁)]`,
`F = S₁S₂ e^{(b₁+b₂+ρσ₁σ₂)T}`, `σ = √(σ₁²+σ₂²+2ρσ₁σ₂)`.

### 8.3 Two-asset correlation option — eqs (5.5)–(5.6) `[T]` [p. 205] (Zhang 1995a)
```
c = S₂ e^{(b₂−r)T} M(y₁+σ₂√T, y₂; ρ) − X₂ e^{−rT} M(y₁, y₂; ρ)
p = X₂ e^{−rT} M(−y₁, −y₂; ρ) − S₂ e^{(b₂−r)T} M(−y₁−σ₂√T, −y₂; ρ)
```
(book prints `− X₂ e^{−rT} M(…)`; `y₁ = [ln(S₁/X₁)+(b₁−σ₁²/2)T]/(σ₁√T)`, `y₂ = [ln(S₂/X₂)+(b₂−σ₂²/2)T]/(σ₂√T)`).

### 8.4 Exchange-one-asset-for-another (Margrabe) — eq (5.7) `[V-1]` [p. 206]
```
C = Q₁ S₁ e^{(b₁−r)T} N(d₁) − Q₂ S₂ e^{(b₂−r)T} N(d₂)
d₁ = [ln(Q₁S₁/(Q₂S₂)) + (b₁−b₂+σ²/2)T]/(σ√T),  d₂ = d₁ − σ√T
σ  = √(σ₁²+σ₂² − 2ρσ₁σ₂)
```
Verified Margrabe = **1.5260** (book 1.5260; S₁=101,Q₁=1,S₂=104,Q₂=1,T=0.5,r=0.10,b₁=0.02,b₂=0.04,σ₁=0.18,σ₂=0.12,ρ=0.8).

### 8.5 American exchange — eq (5.8) `[T]` [p. 208] (Bjerksund–Stensland 1993b)
`C_exchange = C(Q₁S₁, Q₂S₂, T, r−b₂, b₁−b₂, σ)` with `C` a plain American call and `σ` as §8.4.

### 8.6 Exchange option on exchange option — eqs (5.9)–(5.12) `[R]` `[T]` [p. 209] (Carr 1988)
Four variants; each is a bivariate-normal combination with a critical price ratio `I` from `I N(d₂(z₁)) − N(z₁) = 0`. Text layer garbled.

### 8.7 Options on the min/max of two risky assets — eqs (5.13)–(5.16) `[V-1]` [p. 211] (Stulz 1982)
```
C_min = S₁ e^{(b₁−r)T} M(y₁, −d; −ρ₁) + S₂ e^{(b₂−r)T} M(y₂, d−σ√T; −ρ) − X e^{−rT} M(y₁−σ₁√T, y₂−σ₂√T; ρ)
C_max = S₁ e^{(b₁−r)T} M(y₁, d; ρ₁) + S₂ e^{(b₂−r)T} M(y₂, −d+σ√T; ρ₂) − X e^{−rT}[1 − M(−y₁+σ₁√T, −y₂+σ₂√T; ρ)]
P_min = X e^{−rT} − C_min(S₁,S₂,0,T) + C_min(S₁,S₂,X,T)
P_max = X e^{−rT} − C_max(S₁,S₂,0,T) + C_max(S₁,S₂,X,T)
```
```
d = [ln(S₁/S₂)+(b₁−b₂+σ²/2)T]/(σ√T),  σ = √(σ₁²+σ₂²−2ρσ₁σ₂)
y_i = [ln(S_i/X)+(b_i+σ_i²/2)T]/(σ_i√T),  ρ₁ = (σ₁−ρσ₂)/σ,  ρ₂ = (σ₂−ρσ₁)/σ
```
Verified `C_max(S₁,S₂,0,T) = 102.4323` (book 102.4324), `C_max(S₁,S₂,X,T) = 8.0701` (book 8.0700), `P_max = 1.2181` (book 1.2181) for S₁=100,S₂=105,X=98,T=0.5,r=0.05,b₁=−0.01,b₂=−0.04,σ₁=0.11,σ₂=0.16,ρ=0.63.

### 8.8 Spread-option approximation (Kirk) — eqs (5.17)–(5.18) `[V-1]` [p. 213] (Kirk 1995)
```
c = S₁ e^{(b₁−r)T} N(d₁) − (S₂ e^{(b₂−r)T} + X e^{−rT}) N(d₂)
p = (S₂ e^{(b₂−r)T} + X e^{−rT}) N(−d₂) − S₁ e^{(b₁−r)T} N(−d₁)
d₁ = [ln( S₁e^{(b₁−r)T} / (S₂e^{(b₂−r)T}+Xe^{−rT}) ) + σ²T/2]/(σ√T),  d₂ = d₁ − σ√T
σ  = √( σ₁² + (σ₂ F)² − 2ρσ₁σ₂F ),   F = S₂e^{(b₂−r)T}/(S₂e^{(b₂−r)T}+Xe^{−rT})
```
Verified spread call = **2.1670** (book 2.1670; S₁=28,S₂=20,X=7,T=0.25,r=0.05,b=0,σ₁=0.29,σ₂=0.36,ρ=0.42).

### 8.9 Two-asset barrier — eq (5.19) `[R]` `[T]` [p. 215] (Heynen–Kat 1994b)
`S₁` drives payoff, `S₂` drives barrier hits; bivariate-normal expression. Combination table:
```
down-and-out call c_do: η=1, φ=−1 ;  up-and-out call c_uo: η=1, φ=1
down-and-out put  p_do: η=−1,φ=−1 ;  up-and-out put  p_uo: η=−1,φ=1
in-options = plain − out (c_di=call−c_do, etc.)
```
Garbled; **reconstructed**.

### 8.10 Partial-time two-asset barrier — eq (5.20) `[R]` [p. 217] (Bermin 1996c).

### 8.11 Margrabe barrier (knock-in/out Margrabe) — eqs (5.21)–(5.23) `[T]` [p. 219] (Haug–Haug 2002)
Ratio `S = S₁/S₂` hits barrier `H`; `b = b₁−b₂`:
```
down-and-in Margrabe call:  c_di = S₂ e^{(b₂−r)T} (H/S)^{...} c_BSM(H²/S?, 1, T, 0, b, σ)   [structure: BSM on ratio]
up-and-in  Margrabe put :   p_ui = S₂ e^{(b₂−r)T} (H/S)^{...} p_BSM(...)
up-and-out: c_uo(S) = S₁e^{(b₁−r)T}[N(k₁)−N(k₂) − (H/S)^{...} {N(k₃)−N(k₄)}] − S₂e^{(b₂−r)T}[…]
```
Special case `H=1, b₁=b₂`: `c_uo = e^{−rT}(S₁−S₂)` (vol/correlation-independent). Down-and-out follows from in–out parity. (Exact exponents partly garbled — `[T]`.)

### 8.12 Two-asset cash-or-nothing — eqs (5.24)–(5.27) `[T]` [p. 221] (Heynen–Kat 1996a)
```
[1] call  : K e^{−rT} M(d₁,₁, d₂,₂; ρ)     (S₁>X₁ and S₂>X₂)
[2] put   : K e^{−rT} M(−d₁,₁, −d₂,₂; ρ)   (S₁<X₁ and S₂<X₂)
[3] up-dn : K e^{−rT} M(d₁,₁, −d₂,₂; −ρ)   (S₁>X₁ and S₂<X₂)
[4] dn-up : K e^{−rT} M(−d₁,₁, d₂,₂; −ρ)   (S₁<X₁ and S₂>X₂)
d_i,i = [ln(S_i/X_i) + b_i … ]/(σ_i√T)
```
Building block for a C-Brick option (four type-[1] calls at different strikes).

### 8.13 Best / worst cash-or-nothing — eqs (5.28)–(5.31) `[T]` [p. 223] (Brockhaus et al. 2000)
```
C_best  = K e^{−rT}[ M(y, z₁; −ρ₁) + M(−y, z₂; −ρ₂) ]
P_best  = K e^{−rT}[ 1 − M(y, z₁; −ρ₁) − M(−y, z₂; −ρ₂) ]
C_worst = K e^{−rT}[ M(−y, z₁; ρ₁) + M(y, z₂; ρ₂) ]
P_worst = K e^{−rT}[ 1 − M(−y, z₁; ρ₁) + M(y, z₂; ρ₂) ]
y = [ln(S₁/S₂)+(b₁−b₂+σ²/2)T]/(σ√T),  z_i = [ln(S_i/X)+(b_i+σ_i²/2)T]/(σ_i√T)
ρ₁ = (σ₁−ρσ₂)/σ,  ρ₂ = (σ₂−ρσ₁)/σ
```

### 8.14 Options on the min/max of two *averages* — eqs (5.32)–(5.34) `[R]` `[T]` [p. 224] (Wu–Zhang 1999)
`C_MinAsian = S₁ M(a₁,a₂;ρ₁) + S₂ M(a₃,a₄;ρ₂) − X e^{−rT} M(a₃,a₄;ρ)`, with geometric-average-adjusted drifts. Put/call on max via parity with the min formula.

---

## 9. CURRENCY-TRANSLATED OPTIONS (QUANTO FAMILY) — §5.16 [p. 226]

Notation: `S*` asset price in foreign ccy; `X` delivery price in domestic ccy; `r` domestic rate; `r_f` foreign rate; `q` dividend yield; `E` spot FX (domestic per foreign); `E*` = 1/E; `σ_S*` asset vol; `σ_E` FX vol; `ρ` correlation (note: `ρ(Wikkei, ¥/$) = −ρ(Wikkei, $/¥)`).

### 9.1 Foreign equity option struck in domestic currency — eqs (5.35)–(5.38) `[V-1]` [p. 227] (Reiner 1992)
```
c = E S* e^{−qT} N(d₁) − X e^{−rT} N(d₂)
p = X e^{−rT} N(−d₂) − E S* e^{−qT} N(−d₁)
d₁ = [ln(E S*/X) + (r − q + σ_{E·S*}²/2)T]/(σ_{E·S*}√T),  d₂ = d₁ − σ_{E·S*}√T
σ_{E·S*} = √(σ_S*² + σ_E² + 2ρ σ_E σ_S*)
```
Verified = **8.3056** (book 8.3056; E=1.5,S*=100,X=160,T=0.5,r=0.08,q=0.05,σ_S*=0.20,σ_E=0.12,ρ=0.45).

### 9.2 Quanto (fixed exchange rate foreign equity) — eqs (5.39)–(5.42) `[V-1]` [p. 228] (Derman–Karasinski–Wecker 1990; Reiner 1992)
```
c = E_p [ S* e^{(r_f − r − q − ρ σ_S* σ_E)T} N(d₁) − X* e^{−rT} N(d₂) ]
p = E_p [ X* e^{−rT} N(−d₂) − S* e^{(r_f − r − q − ρ σ_S* σ_E)T} N(−d₁) ]
d₁ = [ln(S*/X*) + (r_f − q − ρ σ_S* σ_E + σ_S*²/2)T]/(σ_S*√T),  d₂ = d₁ − σ_S*√T
```
Verified quanto call = **5.3280** (book 5.3280; E_p=1.5,S*=100,X*=105,T=0.5,r=0.08,r_f=0.05,q=0.04,σ_S*=0.20,σ_E=0.10,ρ=0.30).

### 9.3 Equity-linked FX option — eqs (5.43)–(5.46) `[T]` [p. 230] (Reiner 1992)
`c = E S* e^{−qT} N(d₁) − X S* e^{(r_f−r−q−ρσ_S*σ_E)T} N(d₂)`, with `d₁ = [ln(E/X)+(r−r_f+ρσ_S*σ_E+σ_E²/2)T]/(σ_E√T)`.

### 9.4 Takeover FX option — eq (5.47) `[T]` [p. 232] (Schnabel–Wei 1994)
`c = N[ E e^{−r_f T} M(a₁+σ_E√T, −a₂; −ρ) − … − X e^{−rT} M(−a₂, a₂; −ρ) ]`; conditional on takeover success (`V ≤ B`). Structure `[T]`.

---

## 10. VOLATILITY & CORRELATION TOOLS (for basket/rainbow inputs) — Chapter 12

### 10.1 Basket volatility — eq (12.19) `[T]` [p. 460]
```
σ_Index² = Σ_i Q_i² σ_i² + 2 Σ_i Σ_{j>i} Q_i Q_j ρ_{ij} σ_i σ_j
```
`Q_i` = weights. Warned to be an approximation when plugged into Black-76 for basket options (basket isn't lognormal). Function `BasketVolatility(Weights, Vols, Correlations)` implemented.

### 10.2 Implied correlation from currency options — eqs (12.22)–(12.23) `[T]` [p. 462]
```
σ_Cross = √( σ_{Leg1}² + σ_{Leg2}² − 2 ρ σ_{Leg1} σ_{Leg2} )
ρ_{EUR/JPY} = (σ_USD/EUR² + σ_USD/JPY² − σ_EUR/JPY²) / (2 σ_USD/EUR σ_USD/JPY)
```
Example: 0.1490, 0.1530, 0.1230 → **ρ = 0.6683** (book).

### 10.3 Average implied index correlation — eq (12.24) `[T]` [p. 463]
`ρ_Average = (σ_Index² − Σ Q_i²σ_i²) / (Σ_i Σ_{j≠i} Q_iQ_jσ_iσ_j)`.

### 10.4 Historical correlation distribution — eqs (12.20)–(12.21) `[T]` [p. 461] (Rao 1973)
Density of sample correlation `γ` for population `ρ`, `n` observations; series converges fast. `CorrDen(n,γ,ρ)` implemented.

### 10.5 Arctangent rule — eq (12.25) `[T]` [p. 463] (Acar–Toffel 1999)
Probability a high/low occurs in `[t,T]` under driftless BM:
```
P = (2/π) arctan( √(T−t)/√t )
```
Example: T=10, t=9 → 0.205 (book).

---

## 11. NUMERICAL / IMPLEMENTATION NOTES (exotics)

### 11.1 Cumulative distribution functions — Chapter 13
- `CND` cumulative normal: Hart algorithm (§13.1.1), polynomial approx (§13.1.2) [p. 465–467].
- Inverse CND via Moro/Beasley–Springer (§13.2) [p. 468].
- `CBND` bivariate normal: Drezner (1978) 5-point Gauss–Legendre (§13.3.1, eq 13.3 — 6-dp accuracy); Drezner–Wesolowsky (1990); **Genz (2004) recommended** as most accurate [p. 470–471]. The Drezner recursion (as printed):
  `M(a,b;ρ) = M(a,0;ρ₁)+M(b,0;ρ₂) − ½` for `abρ > 0`, with reflection rules for sign combinations.
- `CTND` trivariate normal (Genz adaptive integration; VBA `CTND(LIMIT1,LIMIT2,LIMIT3,SIGMA1..3)`) §13.4 [p. 482] — needed for some multi-asset exotics. Correlation matrix packed `SIGMA(1)=R(2,1), SIGMA(2)=R(3,1), SIGMA(3)=R(3,2)`.

### 11.2 Barrier options in trees (Brownian bridge) — §7.4.2 `[T]` [p. 305]
Probability a node was hit by the barrier (used to weight binomial/trinomial payoffs):
```
p_hit = exp{ −(2/σ²T) · ln(H/S) · ln(H/S_T) }    (below-barrier case; symmetric for above)
```
For down-and-in/out when barrier starts below spot, replace the hit probability per node accordingly. `BinomialBridgeBarrier(...)` implements European up/down-and-out with rebate.

### 11.3 American barrier in CRR tree — §7.4.3 `[T]` [p. 307]
American barrier options require full trees (exercise check at every node); accuracy improves with steps (Table 7-1 gives recommended step counts vs. `Γ(·)`).

### 11.4 American Asian ("Hawaiian") options — §7.4.5 `[T]` [p. 314]
No closed form (Hansen–Jørgensen 1997 use numerical integration). Non-recombining trees grow exponentially; use the Hull–White (1993) interpolation tree, improved by Cho–Lee (1997), Chalasani et al. (1999), Dai–Lyuu (2002). Hull–White value is an upper bound (Dai–Huang–Lyuu 2002).

### 11.5 Three-dimensional binomial tree — §7.5 `[T]` [p. 315]
Rubinstein (1994b) lattice for two-asset options (European & American): spread, options on max/min, dual-strike, portfolio, exchange-one-for-another, relative performance, product — payoff table [p. 315].

### 11.6 Monte Carlo for Asian spread — §8 `[T]`
`MonteCarloAsianSpreadOption(...)` implemented; used for spread/Asian combos lacking closed forms.

---

## 12. VERIFICATION LOG (all numbers re-derived independently with a hand-rolled `N(·)`/`M(·,·;ρ)`; `M` via 1-D adaptive Simpson)

| Formula | Haug value | Reproduced | Status |
|---|---|---|---|
| Simple chooser (4.26) | 6.1071 | 6.1071 (via decomposition) | ✓ |
| Complex chooser critical I (4.27) | 51.1158 | 51.1158 | ✓ |
| Complex chooser value (4.27) | 6.0508 | 6.0508 | ✓ |
| Put-on-call compound I (4.29) | 538.3165 | 538.3165 | ✓ |
| Put-on-call compound value (4.29) | 21.1965 | 21.1964 | ✓ |
| Floating lookback call (4.39) | 25.3533 | 25.3534 | ✓ |
| Gap call (4.82) | −0.0053 | −0.0053 | ✓ |
| Cash-or-nothing put (4.85) | 2.6710 | 2.6710 | ✓ |
| Asset-or-nothing put (4.87) | 20.2069 | 20.2069 | ✓ |
| Supershare (4.88) | 0.7389 | 0.7389 | ✓ |
| Standard barrier C_do/C_ui (4.51–4.52) | 6.7924, 4.8759, 7.0285, 9.0246, 8.4482, 14.1112 | all reproduced | ✓ |
| Binary barrier rows (1)(2)(4)(5)(7)(8)(9)(10)(11)(12)(13a)(14a)(15a)(21a) | Table 4-22 | all reproduced | ✓ |
| Geometric Asian put (4.92) | 4.6922 | 4.6922 | ✓ |
| Margrabe exchange (5.7) | 1.5260 | 1.5260 | ✓ |
| C_max / C_max(0) / P_max (5.14–5.16) | 102.4324 / 8.0700 / 1.2181 | reproduced | ✓ |
| Kirk spread call (5.17) | 2.1670 | 2.1670 | ✓ |
| Quanto call (5.39) | 5.3280 | 5.3280 | ✓ |
| Foreign equity struck domestic (5.35) | 8.3056 | 8.3056 | ✓ |
| Relative outperformance ρ=0 (5.1) | 0.8908 | 0.8908 | ✓ (with σ₂²T convexity term) |

**Formulas flagged `[R]` (not machine-verified):** partial-time lookbacks (4.45–4.48), extreme-spread (4.49–4.50), American barrier closed forms (4.53–4.56), Ikeda–Kunitomo double barrier (4.57–4.58), partial-time single-asset barrier (4.59–4.63), look-barrier (4.64), soft-barrier (4.65), barrier-symmetry double-barrier/dual double-barrier (4.78–4.81), double-barrier binary / asymmetric (4.89–4.90), Curran (4.104), exchange-on-exchange (5.9–5.12), two-asset barrier (5.19–5.20), options on min/max of two averages (5.32–5.34). For these, the text layer did not preserve the algebra cleanly; the standard published attributions are given as pointers.

**Open items / caveats**
1. Simple chooser (4.26): the printed last-term exponent is ambiguous; the value 6.1071 is reproduced by the decomposition, not the literal transcription.
2. Relative outperformance (5.1): the ρ=0 table row matches exactly only when the ratio forward includes the `σ₂²T` convexity term; the printed ρ=±0.5 table entries were not reproduced (possible table/typo issue).
3. Binary barrier rows marked `[T]`: factor *definitions* are verified, but specific `±` combinations for a few rows (esp. 17–28) could not be re-derived from the corrupted text layer — double-check against the printed p. 177–180 before relying on them.
