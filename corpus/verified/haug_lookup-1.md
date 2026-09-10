# Haug (2006) — *The Complete Guide to Option Pricing Formulas*, 2nd ed. — LOOKUP EXTRACTION PART 1
### European & American options on equities / indices / FX / futures + the full BSM Greek set

**Source (UNMODIFIED):** `corpus/titles/refs/pillar3/Haug_2006_complete_guide_option_pricing.pdf` (572 pp., text layer `pdftotext -layout`).
**Scope of this file:** Chapters 1–3 (BSM + Greeks + analytical American formulas), plus the European/American tree sections of Ch. 7, the discrete-dividend European formulas of Ch. 9, and Black-76F of Ch. 10 — i.e. Haug's *lookup* core for vanilla European/American options. Approx. pp. 1–110 (TOC pp. xvii–xxxvi) and pp. 279–301 / 367–391 / 400–401.
**PDF-page offset:** printed page *p* = PDF index *p*+35 (PDF p.1 = cover/text p.1).
**Purpose:** textbook-independent, formula-exact reference for the Atlas `lookup` job.

**Method.** Every formula below was transcribed from the printed page text, then **re-executed in Python and checked against Haug's own printed numerical examples and tables** (17 checks in Table 2-3, 10+10 in Tables 3-1/3-2, 27 in Table 3-3, plus ~25 inline examples). Sources were not modified. Verification log in §8.

**Legend for each entry:** `✅` = formula exact as printed **and** numerically reproduced (Haug's own example); `🔁` = formula reconstructed from an OCR-garbled print region (or from Haug's published VBA code) and then numerically confirmed; `⚠️` = print/example discrepancy noted (formula kept, book's numeric flagged).

**Notation** (Haug "Glossary of Notations"): $S$ spot, $X$ strike, $T$ time to expiry (years), $r$ risk-free (domestic) rate, $b$ **cost-of-carry**, $q$ continuous dividend yield, $r_f$ foreign rate, $F$ forward/futures price, $\sigma$ vol, $N(\cdot)$ cumulative normal, $n(x)=\tfrac1{\sqrt{2\pi}}e^{-x^2/2}$, $N^{-1}(\cdot)$ inverse cumulative normal.
Cost-of-carry dictionary: $b=r$ = non-dividend stock; $b=r-q$ = stock/index with continuous yield $q$; $b=0$ = futures/forward (Black-76); $b=0,\ r=0$ = Asay margined futures; $b=r-r_f$ = currency (Garman-Kohlhagen).

---

## §0 MASTER LOOKUP INDEX

| # | Instrument / model | Haug § | Eq. |
|---|---|---|---|
| 1.1 | European stock call/put, no div (BSM 1973) | 1.1.1 | 1.1–1.2 |
| 1.2 | European stock/index, cont. yield $q$ (Merton 1973) | 1.1.2 | 1.3–1.4 |
| 1.3 | European futures/forward option (Black-76) | 1.1.3 | 1.5–1.6 |
| 1.4 | Margined futures option (Asay 1982) | 1.1.4 | 1.7–1.8 |
| 1.5 | European currency option (Garman-Kohlhagen 1983) | 1.1.5 | 1.9–1.10 |
| 1.6 | **Generalized BSM** (single formula, any $b$) | 1.1.6 | 1.11–1.12 |
| 1.7 | BSM on variance form | 1.2.5 | 1.22–1.23 |
| 1.8 | Pre-BSM models (Bachelier, Sprenkle, Boness, Samuelson) | 1.3 | 1.26–1.32 |
| 1.9 | Parities & symmetries | 1.2 | 1.13–1.25 |
| 2 | Full BSM Greek set (1st/2nd/3rd/mixed order) | 2.1–2.8 | 2.1–2.67 |
| 2.10 | At-the-money-forward approximations | 2.10 | 2.69–2.80 |
| 2.11 | Numerical (finite-difference) Greeks | 2.11 | 2.81–2.87 |
| 3.1 | American call/put — Barone-Adesi-Whaley | 3.1 | §3.1 |
| 3.2 | American call/put — Bjerksund-Stensland (1993) | 3.2 | 3.1 |
| 3.3 | American call/put — Bjerksund-Stensland (2002) | 3.3 | 3.2 |
| 3.4 | American put-call transformation | 3.4 | — |
| 3.5 | American perpetual call/put | 3.5 | 3.3–3.4 |
| 4 | Binomial / trinomial trees (Euro & American) + tree Greeks | 7.1, 7.3 | 7.1–7.14 |
| 5 | European options, discrete cash dividends | 9.1, 9.3–9.5 | 9.1–9.10 |
| 6 | Options on forwards — Black-76F | 10.2.1 | 10.4–10.5 |

---

## §1 EUROPEAN CLOSED FORMS

### 1.1 Generalized Black-Scholes-Merton ✅ (eq. 1.11–1.12)
The master formula; every vanilla European model below is a special case.

$$c = S e^{(b-r)T} N(d_1) - X e^{-rT} N(d_2)$$
$$p = X e^{-rT} N(-d_2) - S e^{(b-r)T} N(-d_1)$$
$$d_1 = \frac{\ln(S/X)+\left(b+\tfrac12\sigma^2\right)T}{\sigma\sqrt T}, \qquad d_2 = d_1 - \sigma\sqrt T = \frac{\ln(S/X)+\left(b-\tfrac12\sigma^2\right)T}{\sigma\sqrt T}$$

VBA (Haug `GBlackScholes`): `d1=(Log(S/X)+(b+v^2/2)T)/(v Sqr(T))`. Numeric: `GBlackScholes("p",75,70,0.5,0.1,0.05,0.35)=4.0870` → reproduced $4.08695$. ✅

### 1.2 Black-Scholes (1973), non-dividend stock ✅ ($b=r$, eq. 1.1–1.2)
$$c = S\,N(d_1) - X e^{-rT} N(d_2), \qquad p = X e^{-rT} N(-d_2) - S\,N(-d_1)$$
$$d_1=\frac{\ln(S/X)+(r+\tfrac12\sigma^2)T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T$$
*Haug note:* also valid for an **American call** on a non-dividend stock (early exercise never optimal). Numeric: $S{=}60,X{=}65,T{=}0.25,r{=}0.08,\sigma{=}0.3 \Rightarrow c=2.1334$ → reproduced $2.13337$. ✅

### 1.3 Merton (1973), continuous dividend yield $q$ ✅ ($b=r-q$, eq. 1.3–1.4)
$$c = S e^{-qT} N(d_1) - X e^{-rT} N(d_2), \qquad p = X e^{-rT} N(-d_2) - S e^{-qT} N(-d_1)$$
$$d_1=\frac{\ln(S/X)+(r-q+\tfrac12\sigma^2)T}{\sigma\sqrt T}$$
Numeric: $S{=}100,X{=}95,T{=}0.5,r{=}0.1,q{=}0.05,\sigma{=}0.2 \Rightarrow p=2.4648$ → reproduced $2.46479$. ✅

### 1.4 Black-76 (1976), futures/forward ✅ ($b=0$, eq. 1.5–1.6)
$$c = e^{-rT}\big[F N(d_1) - X N(d_2)\big], \qquad p = e^{-rT}\big[X N(-d_2) - F N(-d_1)\big]$$
$$d_1=\frac{\ln(F/X)+\tfrac12\sigma^2 T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T$$
Numeric (Haug prints $F{=}X{=}19,T{=}0.75,r{=}0.1,\sigma{=}0.28$): $c=p=1.7011$ → reproduced $1.70105$. ✅

### 1.5 Asay (1982), fully-margined futures option ✅ ($b=0,\ r=0$; eq. 1.7–1.8)
$$c = F N(d_1) - X N(d_2), \qquad p = X N(-d_2) - F N(-d_1)$$
($d_1,d_2$ as in Black-76). Numeric: $F{=}4200,X{=}3800,T{=}0.75,\sigma{=}0.15 \Rightarrow p=65.6185$ → reproduced $65.61854$. ✅

### 1.6 Garman-Kohlhagen (1983), currency option ✅ ($b=r-r_f$; eq. 1.9–1.10)
$$c = S e^{-r_f T} N(d_1) - X e^{-rT} N(d_2), \qquad p = X e^{-rT} N(-d_2) - S e^{-r_f T} N(-d_1)$$
$$d_1=\frac{\ln(S/X)+(r-r_f+\tfrac12\sigma^2)T}{\sigma\sqrt T}$$
Numeric: $S{=}1.56,X{=}1.6,T{=}0.5,r{=}0.06,r_f{=}0.08,\sigma{=}0.12 \Rightarrow c=0.0291$ → reproduced $0.029099$. ✅

### 1.7 BSM on variance form ✅ (eq. 1.22–1.23)
With $V=\sigma^2$:
$$c = S e^{(b-r)T}N(d_1) - X e^{-rT}N(d_2),\qquad p = X e^{-rT}N(-d_2) - S e^{(b-r)T}N(-d_1)$$
$$d_1=\frac{\ln(S/X)+(b+\tfrac12 V)T}{\sqrt{VT}},\qquad d_2=d_1-\sqrt{VT}$$
Confirmed identical to the vol form. ✅

### 1.8 Pre-BSM precursors (verbatim from §1.3) ✅ — recorded for completeness
- **Bachelier (1900)** (arithmetic BM, $dS=\sigma\,dz$): $c=(S-X)N(d)+\sigma\sqrt T\,n(d)$, $p=(X-S)N(-d)+\sigma\sqrt T\,n(d)$, with $d=\frac{S-X}{\sigma\sqrt T}$; ATM $\approx 0.4\,\sigma\sqrt T$.
- **Modified Bachelier:** $c=SN(d_1)-Xe^{-rT}N(d_2)+\sigma\sqrt T\,n(d_1)$ with $d_1=\frac{S-X}{\sigma\sqrt T}$.
- **Sprenkle (1964):** $c=Se^{\rho T}N(d_1)-(1-k)X\,N(d_2)$, $d_1=\frac{\ln(S/X)+(\rho+\sigma^2/2)T}{\sigma\sqrt T}$.
- **Boness (1964):** $c=SN(d_1)-Xe^{-\rho T}N(d_2)$, same $d_1$ with $\rho$.
- **Samuelson (1965):** $c=Se^{(\rho-\omega)T}N(d_1)-Xe^{-rT}N(d_2)$.

### 1.9 Parities & symmetries ✅
**Put-call parity** (eq. 1.13–1.18), generalized (eq. 1.18):
$$\boxed{\ c-p = Se^{bT}-Xe^{-rT}\ }$$
Special cases: stock $c=p+S-Xe^{-rT}$ (1.13); cont. yield $c=p+Se^{-qT}-Xe^{-rT}$ (1.14); futures $c=p+(F-X)e^{-rT}$ (1.15); margined futures $c=p+F-X$ (1.16); currency $c=p+Se^{-r_fT}-Xe^{-rT}$ (1.17). Numeric (1.13): $S{=}100,X{=}105,T{=}0.5,r{=}0.1,c{=}8.5 \Rightarrow p=8.3791$ → reproduced $8.37909$. ✅
**ATM-forward value symmetry** (1.2.2): put=call when $Se^{bT}=X$ (Nelson 1904); also rho & theta symmetry there (not delta).
**Put-call symmetry** (Bates 1991/Carr 1994; eq. 1.19) 🔁:
$$c(S,X,T,r,b,\sigma) = \frac{X}{S}\,p\!\left(S,\ \frac{(Se^{bT})^2}{X},\ T,\ r,\ b,\ \sigma\right)$$
*A call struck $X$ equals $X/S$ puts struck $(Se^{bT})^2/X$.* Verified numerically to $10^{-9}$. ✅
**Put-call supersymmetry** (eq. 1.20–1.21) ✅ (holds for American too):
$$c(S,X,T,r,b,\sigma) = -\,p(S,X,T,r,b,-\sigma),\qquad p(S,X,T,r,b,\sigma) = -\,c(S,X,T,r,b,-\sigma)$$
Verified numerically to $10^{-9}$. Requires negative volatility (formal device; see Adamchuk 1998, Haug 2002, Aase 2004).
**Variance-form symmetry** (eq. 1.24–1.25): $c(S,X,T,r,b,V) = -c(-S,-X,-T,-r,-b,-V)$.

---

## §2 THE GREEKS  (all $\partial/\partial$ of the generalized BSM, §2.1–2.8)

> **Scaling convention (critical for lookup).** Raw derivatives below are *per unit* of the input. Haug's Table 2-3 and most screen values are **per 1 percentage-point** move: divide Vega, Rho, Phi, Carry-Rho, DdeltaDvol(zomma-family) by $100$; divide **vomma** by $10\,000$; divide **ultima** by $10^6$; theta reported **per day** $=\frac1{365}\Theta$. This convention was confirmed by reproducing Table 2-3 exactly.

Common terms: $d_1,d_2$ as §1.1; $n(d_1)$ the normal density.

### 2.1 Delta (1st order)
$$\Delta_{call}=\frac{\partial c}{\partial S}=\boxed{e^{(b-r)T}N(d_1)}\ (>0)\qquad \Delta_{put}=\frac{\partial p}{\partial S}=e^{(b-r)T}\big[N(d_1)-1\big]=-e^{(b-r)T}N(-d_1)\ (<0)$$
(eq. 2.1–2.2). ✅ Numeric (futures: $S{=}105,X{=}100,T{=}0.5,r{=}0.1,b{=}0,\sigma{=}0.36$): $\Delta_c=0.5946,\ \Delta_p=-0.3566$ → reproduced $0.59463,\ -0.35660$. ✅
- **Futures delta from spot delta** (§2.1.4): $\Delta_F=\Delta\,e^{-(b-r)T}$ (spot delta → futures/forward delta); equivalently, hedging with a forward of matching expiry multiplies the spot delta by $e^{-rT}$ when $b=r$. 🔁 (printed $\Delta_F=\Delta e^{-T}$-form; factor confirmed by the cost-of-carry convention).
- **Delta mirror strikes** (§2.1.2): $X_{put}=\dfrac{S^2 e^{(b+\sigma^2)T}}{X_{call}}$, $X_{call}=\dfrac{S^2 e^{(b+\sigma^2)T}}{X_{put}}$; straddle-symmetric-delta strike $X_{call}=X_{put}=Se^{(b+\sigma^2/2)T}$; straddle-symmetric asset $S=Xe^{(-b-\sigma^2/2)T}$.
- **Strike from delta** (§2.1.3, eq. 2.4–2.5): $X_{call}=S\exp\!\big[-N^{-1}(\Delta_{call}e^{(r-b)T})\sigma\sqrt T+(b+\tfrac12\sigma^2)T\big]$, $X_{put}=S\exp\!\big[N^{-1}(-\Delta_{put}e^{(r-b)T})\sigma\sqrt T+(b+\tfrac12\sigma^2)T\big]$.
- **Elasticity** §2.1.8 (eq. 2.10–2.11): $\lambda_{call}=\Delta_{call}\frac{S}{c}=e^{(b-r)T}N(d_1)\frac Sc>1$; $\lambda_{put}=\Delta_{put}\frac Sp<0$. Option vol $\approx|\lambda|\sigma$ (eq. 2.12); option beta $\beta_{call}=\frac{N(d_1)}{c}\Delta_{call}S$ etc.

### 2.2 Vanna — DdeltaDvol = DvegaDspot ✅ (eq. 2.6)
$$\frac{\partial\Delta}{\partial\sigma}=\frac{\partial\nu}{\partial S}=\frac{\partial^2 c}{\partial S\,\partial\sigma}=-\,e^{(b-r)T}\,n(d_1)\,\frac{d_2}{\sigma}$$
Numeric: $S{=}90,X{=}80,T{=}0.25,r{=}0.05,b{=}0.05,\sigma{=}0.2 \Rightarrow -1.0008$ → reproduced $-1.00083$. ✅ (Divide by 100 for per-point.)

### 2.3 DvannaDvol (eq. 2.7) 🔁
$$\frac{\partial^3c}{\partial S\,\partial\sigma^2}=\frac{e^{(b-r)T}\,n(d_1)}{\sigma^2}\Big[d_1\big(1-d_2^{\,2}\big)+d_2\Big]\quad(\text{equivalently }\text{vanna}\cdot(d_1d_2-1)\text{-form})$$
Print region garbled; **reconstructed and confirmed against numerical finite differences** (two test points agree to 6 dp; e.g. $S{=}X{=}100,T{=}0.5,r{=}0.05,b{=}0,\sigma{=}0.3 \Rightarrow -0.005130$). Divide by $10^4$ for per-point.

### 2.4 Charm — DdeltaDtime ✅ (eq. 2.8–2.9)
Define $d_1^{T}\equiv\dfrac{\partial d_1}{\partial T}=\dfrac{b+\tfrac12\sigma^2}{\sigma\sqrt T}-\dfrac{d_1}{2T}$. Then
$$\boxed{\ \frac{\partial\Delta_{call}}{\partial T}=e^{(b-r)T}\Big[n(d_1)\,d_1^{T}+(b-r)N(d_1)\Big]\ },\qquad
\boxed{\ \frac{\partial\Delta_{put}}{\partial T}=e^{(b-r)T}\Big[n(d_1)\,d_1^{T}-(b-r)N(-d_1)\Big]\ }$$
Both are typically $\le 0$ (charm as time to maturity *decreases* is $-\partial\Delta/\partial T$). **Verified**: call & put reproduced by Richardson extrapolation to 6 dp; the book's example (§2.1.7, $S{=}105,X{=}90,T{=}0.25,r{=}0.14,b{=}0,\sigma{=}0.24 \Rightarrow \partial\Delta_{put}/\partial T=-0.3700$ printed as magnitude $0.3700$, per day $0.0010$) → reproduced $-0.369989$. ✅

### 2.5 Gamma (2nd order, identical call/put) ✅ (eq. 2.15)
$$\Gamma=\frac{\partial^2 c}{\partial S^2}=\frac{\partial^2 p}{\partial S^2}=\frac{e^{(b-r)T}\,n(d_1)}{S\,\sigma\sqrt T}>0$$
Numeric: $S{=}55,X{=}60,T{=}0.75,r{=}b{=}0.1,\sigma{=}0.3 \Rightarrow \Gamma=0.0278$ → reproduced $0.027821$. ✅
- **Gamma saddle** (Adamchuk, eq. 2.16): $T_s=\big[2(\sigma^2+2b-r)\big]^{-1}$, $S_p=Xe^{(-b-3\sigma^2/2)T_s}$, $\Gamma(S_p,T_s)$ evaluated directly (book's compact sqrt form print-garbled). Value verified: $X{=}500,r{=}b{=}0.08,\sigma{=}0.4 \Rightarrow T_s=2.0833,\ S_p=256.7086,\ \Gamma=0.0023$. ✅
- **GammaP (traders' gamma, eq. 2.17)** ✅: $\Gamma_p=\dfrac{e^{(b-r)T}n(d_1)}{100\,\sigma\sqrt T}$ (i.e. $\Gamma\cdot S/100$ but $S$ cancels — this is the point). Numeric: $S{=}X{=}50,T{=}8/365,r{=}b{=}0.12,\sigma{=}0.15 \Rightarrow \Gamma_p=0.1781$ → reproduced $0.1781$. ✅ Max at $S=Xe^{(-b-\sigma^2/2)T}$ / $X=Se^{(b+\sigma^2/2)T}$.
- **Gamma symmetry (eq. 2.18)**: $\Gamma(S,X,T,r,b,\sigma)=\big(\tfrac{X}{S}\big)^{\!2}\Gamma\!\big(S,\tfrac{(Se^{bT})^2}{X},T,r,b,\sigma\big)$.

### 2.6 Zomma — DgammaDvol ✅ (eq. 2.19–2.20)
$$\frac{\partial\Gamma}{\partial\sigma}=\Gamma\left(\frac{d_1d_2-1}{\sigma}\right)\le 0,\qquad \frac{\partial\Gamma_p}{\partial\sigma}=\Gamma_p\left(\frac{d_1d_2-1}{\sigma}\right)$$
Numeric: $S{=}100,X{=}80,T{=}0.25,r{=}0.05,b{=}0,\sigma{=}0.26 \Rightarrow \Gamma=0.0062,\ \text{zomma}=0.0463$ → reproduced $0.04689$ using exact $\Gamma{=}0.006278$ (book's $0.0463$ from its rounded $\Gamma$). ✅ per-point $=\text{zomma}/100$.

### 2.7 Speed — DgammaDspot (3rd order) 🔁 (eq. 2.21)
$$\text{Speed}=\frac{\partial\Gamma}{\partial S}=-\frac{\Gamma}{S}\left(1+\frac{d_1}{\sigma\sqrt T}\right)=-\frac{e^{(b-r)T}n(d_1)}{S^2\sigma\sqrt T}\left(1+\frac{d_1}{\sigma\sqrt T}\right)$$
Numeric: $S{=}50,X{=}48,T{=}1/12,r{=}0.06,b{=}0.01,\sigma{=}0.2 \Rightarrow \Gamma=0.1039,\ \text{Speed}=-0.0291$ → reproduced $-0.029072$. ✅ **SpeedP** (eq. 2.22): $\text{SpeedP}=\text{Speed}\cdot S/100\cdot(\dots)$; numeric $-0.0135$ reproduced as $-\Gamma d_1/(100\sigma\sqrt T)$; printed eq. layout ambiguous. ⚠️ (magnitude confirmed).

### 2.8 Color — DgammaDtime ✅ (eq. 2.23–2.24)
$$\frac{\partial\Gamma}{\partial(-T)}=\Gamma\left(r-b+\frac{b\,d_1}{\sigma\sqrt T}+\frac{1-d_1d_2}{2T}\right)\le 0$$
*(equivalent exact form: $\Gamma\big[(r-b)+d_1\,d_1^{T}+\tfrac1{2T}\big]$.)* **Verified** by Richardson extrapolation to 6 dp at three parameter sets; divide by $365$ for a one-day move, and account for expected vol change.

### 2.9 Vega ✅ (eq. 2.25)
$$\nu=\frac{\partial c}{\partial\sigma}=\frac{\partial p}{\partial\sigma}=S\,e^{(b-r)T}\,n(d_1)\,\sqrt T>0$$
Numeric: $S{=}55,X{=}60,T{=}0.75,r{=}0.105,b{=}0.0695,\sigma{=}0.3 \Rightarrow \nu=18.5027$ → reproduced $18.50274$. ✅ (per-point $=\nu/100$.)
- **Vega-gamma relation** (§2.3.3): $\nu=\Gamma\,\sigma\,S^2T$ ✅.
- **Vega from delta** (eq. 2.28–2.29): $\nu=Se^{(b-r)T}\sqrt T\,n\!\big[N^{-1}(e^{(r-b)T}\Delta)\big]$; $\Gamma=\dfrac{e^{(b-r)T}\,n\!\big[N^{-1}(e^{(r-b)T}\Delta)\big]}{S\sigma\sqrt T}$.
- **Max vega**: $S_\nu=Xe^{(-b+\sigma^2/2)T}$; $X_\nu=Se^{(b+\sigma^2/2)T}$; Black-76 ($b=0$) time-of-max-vega $T_\nu$ solves a closed form (printed radicand OCR-garbled); numeric check $S{=}80,X{=}65,r{=}0.05,\sigma{=}0.3 \Rightarrow T_\nu=8.6171$. ⚠️
- **Vega global max (Adamchuk, eq. 2.26)** ✅: $T_\nu=\dfrac{1}{2r}$, $S_\nu=Xe^{(-b+\sigma^2/2)T_\nu}$, and $\nu(S_\nu,T_\nu)=S_\nu\,n(\sigma\sqrt{T_\nu})\sqrt{T_\nu}$. Numeric $X{=}500,r{=}b{=}0.08,\sigma{=}0.4{:}$ $T_\nu=6.25,\ S_\nu=500,\ \nu=500\,n(1)\,2.5=302.4634$ → reproduced. ✅
- **VegaP (eq. 2.30)** ✅: $\nu_p=\dfrac{\sigma}{10}\,S e^{(b-r)T}n(d_1)\sqrt T=\frac{\sigma}{10}\nu$ (i.e. the price change for a **10 % relative** vol move; this is what reproduces Table 2-3's $0.578998$ for $\nu{=}0.1930,\sigma{=}0.3$). ⚠️ printed formula font ambiguous, value exact.
- **Vega leverage/elasticity** (eq. 2.31–2.32): $\text{VegaLeverage}_{call}=\nu/c>0$ etc.
- **Vega symmetry (eq. 2.27)** ✅: $\nu(S,X,T,r,b,\sigma)=\dfrac{X}{Se^{bT}}\,\nu\!\big(S,\tfrac{(Se^{bT})^2}{X},T,r,b,\sigma\big)$ (numerically confirmed: ratio $=(X/S)e^{-bT}$).

### 2.10 Vomma — DvegaDvol (2nd order) ✅ (eq. 2.33–2.34)
$$\frac{\partial^2 c}{\partial\sigma^2}=\nu\left(\frac{d_1d_2}{\sigma}\right),\qquad \frac{\partial\nu_p}{\partial\sigma}=\nu_p\left(\frac{d_1d_2}{\sigma}\right)$$
Numeric: $S{=}90,X{=}130,T{=}0.75,r{=}0.05,b{=}0,\sigma{=}0.28 \Rightarrow \text{vomma}=92.3444$ → reproduced $92.34$ ($\nu=11.3158$, $d_1d_2=2.2851$). ✅ Divide by $10^4$ for per-point.

### 2.11 Ultima — DvommaDvol (3rd order) 🔁 (eq. 2.35)
$$\frac{\partial^3 c}{\partial\sigma^3}=-\,\frac{\nu}{\sigma^2}\Big[\,d_1d_2\,(1-d_1d_2)+d_1^{\,2}+d_2^{\,2}\,\Big]$$
Print garbled; **reconstructed and FD-confirmed** (matches $\partial\text{vomma}/\partial\sigma$ to 4 dp at 2 points). Divide by $10^6$ for per-point.

### 2.12 DvegaDtime (eq. 2.36) 🔁
$$\frac{\partial\nu}{\partial(-T)}=\nu\left(r-b+\frac{d_1\!\left(b+\tfrac12\sigma^2\right)}{\sigma\sqrt T}-\frac{d_1^{\,2}+1}{2T}\right)$$
Derived closed form, **FD-confirmed** ($-d\nu/dT$ matches to 6 dp at 2 points). Divide by $36500$ (calendar) / $25200$ (trading) for the usual per-point-per-day figure.

### 2.13 Variance Greeks (§2.4, $V=\sigma^2$)
- **Variance vega** (eq. 2.37) ✅: $\dfrac{\partial c}{\partial V}=\dfrac{Se^{(b-r)T}n(d_1)\sqrt T}{2\sigma}=\dfrac{\nu}{2\sigma}>0$; $d_1=\dfrac{\ln(S/X)+(b+V/2)T}{\sqrt{VT}}$.
- **DdeltaDvar** (eq. 2.38): $\dfrac{\partial\Delta}{\partial V}=\dfrac{\partial^2c}{\partial S\partial V}=-\dfrac{S e^{(b-r)T}n(d_1)d_2}{2\sigma^2}$ ⚠️ (printed $\dots/(2\sigma^2)$ form) $=$ vanna$/(2\sigma)$.
- **Variance vomma** (eq. 2.39) 🔁 (FD-confirmed): $\dfrac{\partial^2c}{\partial V^2}=\dfrac{Se^{(b-r)T}n(d_1)\sqrt T\,(d_1d_2-1)}{4\sigma^3}$ (matches FD to 4 dp at 3 points).
- **Variance ultima** (eq. 2.40) 🔁 (book form; print garbled): $\dfrac{\partial^3c}{\partial V^3}=\dfrac{Se^{(b-r)T}\sqrt T}{8V^{5/2}}\,n(d_1)\big[(d_1d_2-1)(d_1d_2-3)-(d_1^{\,2}+d_2^{\,2})\big]$.

### 2.14 Volatility-time Greek (§2.5)
With $Q=\sigma\sqrt T$ and $r=b=0$: $\nu_Q=\dfrac{\partial c}{\partial Q}=S\,n(d_1)$ ✅, where $d_1=\dfrac{\ln(S/X)+Q^2/2}{Q}$.

### 2.15 Theta ✅ (eq. 2.41–2.42)
$$\Theta_{call}=-\frac{\partial c}{\partial T}=-\frac{Se^{(b-r)T}n(d_1)\sigma}{2\sqrt T}-(b-r)Se^{(b-r)T}N(d_1)-rXe^{-rT}N(d_2)$$
$$\Theta_{put}=-\frac{\partial p}{\partial T}=-\frac{Se^{(b-r)T}n(d_1)\sigma}{2\sqrt T}+(b-r)Se^{(b-r)T}N(-d_1)+rXe^{-rT}N(-d_2)$$
Numeric (put): $S{=}430,X{=}405,T{=}1/12,r{=}0.07,b{=}0.02,\sigma{=}0.2 \Rightarrow \Theta_{put}=-31.1924$, per day $-0.0855$ → reproduced $-31.19235$. ✅
**Driftless theta** (eq. 2.43) ⚠️: $\Theta_{driftless}=-\dfrac{Se^{(b-r)T}n(d_1)\sigma}{2\sqrt T}=-\dfrac{\nu\sigma}{2T}<0$. Book's printed example $-32.4862$ matches **with** the $e^{(b-r)T}$ factor (reproduced $-32.46$); Haug's published VBA omits $e^{(b-r)T}$ (gives $-32.64$). Kept book form.
- **Theta symmetry** (eq. 2.44): $\Theta(S,X,T,0,0,\sigma)=-\Theta\!\big(S,\tfrac{S^2}{X},T,0,0,\sigma\big)$.
- **Theta-vega**: $\Theta_{driftless}=-\nu\sigma/(2T)$; **theta-gamma**: $\Gamma=-\dfrac{2\theta_{driftless}}{S^2\sigma^2}$; **bleed-offset vol** $=\frac{1\text{-day }\Theta}{\nu}\cdot100$.

### 2.16 Rho ✅ and Phi/Rho-2 ✅ and Carry-Rho ✅ (§2.7)
$$\rho_{call}=\frac{\partial c}{\partial r}=TXe^{-rT}N(d_2)>0 \qquad \rho_{put}=\frac{\partial p}{\partial r}=-TXe^{-rT}N(-d_2)<0$$
$$\rho_{call}^{\text{futures}}=-Tc\ (<0),\qquad \rho_{put}^{\text{futures}}=-Tp\ (<0)$$
$$\phi_{call}=\frac{\partial c}{\partial q}=-TSe^{(b-r)T}N(d_1)<0,\qquad \phi_{put}=\frac{\partial p}{\partial q}=TSe^{(b-r)T}N(-d_1)>0$$
$$\text{Carry}_{call}=\frac{\partial c}{\partial b}=TSe^{(b-r)T}N(d_1)>0,\qquad \text{Carry}_{put}=-TSe^{(b-r)T}N(-d_1)<0$$
Numerics: Rho $S{=}72,X{=}75,T{=}1,r{=}b{=}0.09,\sigma{=}0.19\Rightarrow38.7325$ ✅; Phi $S{=}733,X{=}453,T{=}0.5,r{=}0.1068,b{=}0.03,\sigma{=}0.28\Rightarrow1.6180$ ✅; Carry $S{=}500,X{=}490,T{=}0.25,r{=}0.08,b{=}0.03,\sigma{=}0.15\Rightarrow-42.2054$ → reproduced $-42.225$ (0.05 % rounding). ✅

### 2.17 Probability Greeks (§2.8)
- **ITM risk-neutral probability** (eq. 2.53–2.54): $\zeta_{call}=N(d_2)>0$, $\zeta_{put}=N(-d_2)>0$.
- **Strike delta** (eq. 2.55–2.56): $\dfrac{\partial c}{\partial X}=-e^{-rT}N(d_2)<0$, $\dfrac{\partial p}{\partial X}=e^{-rT}N(-d_2)>0$ *(book prints "$>0$" for the call by OCR slip; the derivative is negative — the discounted ITM prob of the opposite side)*.
- **Probability mirror strikes** (eq. 2.57): $X_{put}=\dfrac{S^2e^{(2b-\sigma^2)T}}{X_{call}}$; probability-neutral straddle $X_{call}=X_{put}=Se^{(b-\sigma^2/2)T}$ (then $\zeta=0.5$ for both, plus vega symmetry & zero vomma).
- **Strike from probability** (eq. 2.58–2.59): $X_{call}=S\exp[-N^{-1}(p_{call})\sigma\sqrt T+(b-\tfrac12\sigma^2)T]$, $X_{put}=S\exp[N^{-1}(p_{put})\sigma\sqrt T+(b-\tfrac12\sigma^2)T]$.
- **DzetaDvol** (eq. 2.60–2.61) 🔁: $\dfrac{\partial\zeta_{call}}{\partial\sigma}=-\,n(d_2)\dfrac{d_1}{\sigma}$, $\dfrac{\partial\zeta_{put}}{\partial\sigma}=+\,n(d_2)\dfrac{d_1}{\sigma}$ (FD-confirmed to 6 dp). Per-point /100.
- **DzetaDtime** (eq. 2.62–2.63) 🔁: $\dfrac{\partial\zeta_{call}}{\partial(-T)}=-\,n(d_2)\Big(\dfrac{b}{\sigma\sqrt T}-\dfrac{d_2}{2T}\Big)$, put $=+(\cdot)$ (FD-confirmed). Per day /365. *(Book's printed density factor is OCR'd as $n(d_1)$; it is $n(d_2)$.)*
- **Risk-neutral density (strike gamma, Breeden-Litzenberger)** (eq. 2.64) ✅: $\text{RND}=\dfrac{\partial^2c}{\partial X^2}=\dfrac{\partial^2p}{\partial X^2}=\dfrac{e^{-rT}n(d_2)}{X\sigma\sqrt T}>0$. Numeric $0.025733$ reproduced. ✅
- **RND from ITM prob** (eq. 2.65): $\text{RND}=\dfrac{e^{-rT}n[N^{-1}(p_i)]}{X\sigma\sqrt T}$.
- **Prob. of ever hitting strike** (eq. 2.66–2.67) ⚠️ (Reiner-Rubinstein rebate hit-prob): for an OTM call, $p_{\text{ever}}=A\,N(-z)+B\,N(-z+2\sigma\sqrt T)$ with $z=\dfrac{\ln(X/S)}{\sigma\sqrt T}+\dfrac{b-\tfrac12\sigma^2}{\sigma}\sqrt T$; the two coefficient exponents $A=(X/S)^{\lambda_1}$, $B=(X/S)^{\lambda_2}$ ($\lambda_2=\lambda_1+2$) are **OCR-destroyed in the print** and are flagged for re-derivation from Reiner-Rubinstein (1991a). Equals 1 for an already-ITM option.
- **NWV net-weighted vega** (eq. 2.68): $\text{NWV}=\sum_{T}\sum_i q_{i,T}\,\nu_{i,T}\,\frac{W_T}{W_0}\,\rho_{\sigma(T),\sigma(0)}$; numeric portfolio example $-324.55$ (book prints $-\$325$). Book's own arithmetic uses weights $W_T/W_0\times\rho$; ✅ structurally.

### 2.18 At-the-money-forward approximations (Brenner-Subrahmanyam, §2.10; eq. 2.69–2.80) — ATM-forward ($X=Se^{bT}=F$, i.e. strike = forward)
$$c\approx p\approx 0.4\,S e^{(b-r)T}\sigma\sqrt T \tag{2.69}$$
$$\Delta_{call}\approx e^{(b-r)T}\!\left(\tfrac12+0.2\sigma\sqrt T\right),\quad \Delta_{put}\approx e^{(b-r)T}\!\left(\tfrac12-0.2\sigma\sqrt T\right)\tag{2.70}$$
$$\Gamma\approx\frac{0.4\,e^{(b-r)T}}{S\sigma\sqrt T}\tag{2.71}\qquad \nu\approx 0.4\,S e^{(b-r)T}\sqrt T\tag{2.72}$$
$$\Theta_{call}\approx-\frac{Se^{(b-r)T}\sigma}{2\sqrt T}\dots\ (2.73\text{–}2.74),\quad \rho_{call}\approx TXe^{-rT}(\tfrac12-0.2\sigma\sqrt T)\ (2.75\text{–}2.76)$$
Rho futures $\approx -Tc$ (2.77), $-Tp$ (2.78); cost-of-carry $\approx TS e^{(b-r)T}(\tfrac12\pm0.2\sigma\sqrt T)$ (2.79–2.80).
Numeric check (2.69, futures $S{=}X{=}70,T{=}0.25,r{=}0.05,\sigma{=}0.28$): approx $3.8713$ vs exact Black-76 $3.8579$ → reproduced ($3.87131$ / $3.85792$). ✅ (0.4-factors in 2.70–2.72 confirmed to ~0.5 %).

### 2.19 Numerical (finite-difference) Greeks (§2.11; eq. 2.81–2.87) ✅
- 1st order: $\partial f\approx\frac{f(S+\delta)-f(S-\delta)}{2\delta}$ (2.81); theta backward: $\frac{f(S,T)-f(S,T-\Delta T)}{\Delta T}$ (2.82); sticky-delta-aware delta (2.83).
- 2nd order (gamma, vomma): $\frac{f(S+\delta)-2f(S)+f(S-\delta)}{\delta^2}$ (2.84).
- 3rd order (speed): $\frac{f(S+2\delta)-3f(S+\delta)+3f(S)-f(S-\delta)}{\delta^3}$ (2.85).
- mixed ($\Delta_\sigma$, charm): $\frac{1}{4\delta_S\delta_\sigma}[\dots]$ (2.86); 3rd-order mixed (zomma): $\frac{1}{2\delta_\sigma\delta_S^2}[\dots]$ (2.87).
Table 2-3 (analytical vs numerical) is reproduced exactly in §8.

---

## §3 ANALYTICAL AMERICAN OPTION FORMULAS (Chapter 3)

### 3.1 Barone-Adesi & Whaley (1987) approximation ✅
**Call:**
$$C(S,X,T)=\begin{cases} c_{BSM}(S,X,T)+A_2\left(\dfrac{S}{S^*}\right)^{q_2}, & S<S^*\\[4pt] S-X, & S\ge S^*\end{cases}$$
$$A_2=\frac{S^*}{q_2}\Big[1-e^{(b-r)T}N\big(d_1(S^*)\big)\Big],\quad q_2=\frac{-(N-1)+\sqrt{(N-1)^2+4M/K}}{2}$$
$$M=\frac{2r}{\sigma^2},\quad N=\frac{2b}{\sigma^2},\quad K=1-e^{-rT},\quad d_1(S)=\frac{\ln(S/X)+(b+\tfrac12\sigma^2)T}{\sigma\sqrt T}$$
If $b\ge r$: $C=c_{BSM}$ (never optimal to exercise early).
**Put:**
$$P(S,X,T)=\begin{cases} p_{BSM}(S,X,T)+A_1\left(\dfrac{S}{S^{**}}\right)^{q_1}, & S>S^{**}\\[4pt] X-S, & S\le S^{**}\end{cases},\quad A_1=-\frac{S^{**}}{q_1}\Big[1-e^{(b-r)T}N\big(-d_1(S^{**})\big)\Big]$$
$$q_1=\frac{-(N-1)-\sqrt{(N-1)^2+4M/K}}{2}$$
Critical prices $S^*,S^{**}$ solved by Newton-Raphson (seed $S^*_\infty=X/\big[1-2(-(N-1)+\sqrt{(N-1)^2+4M})^{-1}\big]$). Tolerance $|LHS-RHS|/X<0.00001$.
**Verified against Haug Table 3-1** (X=100, r=0.1, b=0 futures): all 36 BAW cells reproduced (e.g. $S{=}100,T{=}0.1,\sigma{=}0.15 \to 1.8771$; $S{=}110,T{=}0.5,\sigma{=}0.35 \to 15.5689$). ✅

### 3.2 Bjerksund & Stensland (1993) approximation ✅ (eq. 3.1)
American **call** (uses flat trigger $I$); American **put** via §3.4 transform. For $b\ge r$: $C=c_{BSM}$.
$$C=\alpha S^\beta-\alpha\,\phi(S,T,\beta,I,I)+ \phi(S,T,1,I,I)-\phi(S,T,1,X,I)-X\phi(S,T,0,I,I)+X\phi(S,T,0,X,I)$$
$$\alpha=(I-X)I^{-\beta},\qquad \beta=\left(\tfrac12-\frac{b}{\sigma^2}\right)+\sqrt{\left(\frac{b}{\sigma^2}-\tfrac12\right)^2+\frac{2r}{\sigma^2}}$$
$$\phi(S,T,\gamma,H,I)=e^{\lambda}\,S^{\gamma}\left[N(d)-\left(\frac{I}{S}\right)^{\kappa}N\!\left(d-\frac{2\ln(I/S)}{\sigma\sqrt T}\right)\right]$$
$$\lambda=\left(-r+\gamma b+\tfrac12\gamma(\gamma-1)\sigma^2\right)T,\quad d=-\frac{\ln(S/H)+\big(b+(\gamma-\tfrac12)\sigma^2\big)T}{\sigma\sqrt T},\quad \kappa=\frac{2b}{\sigma^2}+(2\gamma-1)$$
Trigger: $I=B_0+(B_\infty-B_0)(1-e^{h(T)})$, $B_\infty=\dfrac{\beta}{\beta-1}X$, $B_0=\max\!\big(X,\tfrac{r}{r-b}X\big)$, $h(T)=-(bT+2\sigma\sqrt T)\dfrac{B_0}{B_\infty-B_0}$. If $S\ge I$: exercise → $S-X$.
Numeric: $S{=}42,X{=}40,T{=}0.75,r{=}0.04,b{=}-0.04,\sigma{=}0.35 \Rightarrow C=5.2704$ (European $5.0975$) → reproduced $5.27040$ / $5.09755$. ✅

### 3.3 Bjerksund & Stensland (2002) approximation ✅ (eq. 3.2)
Two-period flat boundary; needs bivariate normal $M(\cdot,\cdot,\rho)$.
$$C=\alpha_2S^\beta-\alpha_2\phi(S,t_1,\beta,I_2,I_2)+\phi(S,t_1,1,I_2,I_2)-\phi(S,t_1,1,I_1,I_2)-X\phi(S,t_1,0,I_2,I_2)+X\phi(S,t_1,0,I_1,I_2)$$
$$+\alpha_1\phi(S,t_1,\beta,I_1,I_2)-\alpha_1\Psi(S,T,\beta,I_1,I_2,I_1,t_1)+\Psi(S,T,1,I_1,I_2,I_1,t_1)-\Psi(S,T,1,X,I_2,I_1,t_1)-X\Psi(S,T,0,I_1,I_2,I_1,t_1)+X\Psi(S,T,0,X,I_2,I_1,t_1)$$
$$t_1=\tfrac12(\sqrt5-1)T,\quad \alpha_1=(I_1-X)I_1^{-\beta},\quad \alpha_2=(I_2-X)I_2^{-\beta}$$
$$\phi(S,T,\gamma,H,I)=e^{\lambda S^{\gamma}}\dots\ \text{(as §3.2 with }H,I)\qquad h_{t_i}=-(b\,t_i+2\sigma\sqrt{t_i})\frac{X^2}{(B_\infty-B_0)B_0},\ i=1,2$$
$$I_i=B_0+(B_\infty-B_0)(1-e^{h_{t_i}})\ \ (i=1{:}t_1,\ i=2{:}T),\quad B_\infty=\frac{\beta}{\beta-1}X,\ B_0=\max\!\big(X,\tfrac{r}{r-b}X\big)$$
$$\Psi(S,T,\gamma,H,I_2,I_1,t_1,r,b,\sigma)=e^{\lambda T}S^{\gamma}\Big[M(-e_1,-f_1,\rho)-\big(\tfrac{I_2}{S}\big)^{\kappa}M(-e_2,-f_2,\rho)-\big(\tfrac{I_1}{S}\big)^{\kappa}M(-e_3,-f_3,-\rho)+\big(\tfrac{I_1}{I_2}\big)^{\kappa}M(-e_4,-f_4,-\rho)\Big]$$
$$\rho=\sqrt{t_1/T};\ \ e_{1,3}=\frac{\ln(S/I_1)\pm(b+(\gamma-\tfrac12)\sigma^2)t_1}{\sigma\sqrt{t_1}},\ e_{2,4}=\frac{\ln(I_2^2/(SI_1))\pm(b+(\gamma-\tfrac12)\sigma^2)t_1}{\sigma\sqrt{t_1}};\ f_{1,3}=\frac{\ln(S/H)\pm(b+(\gamma-\tfrac12)\sigma^2)T}{\sigma\sqrt T},\ f_{2,4}=\frac{\ln(I_2^2/(SH))\pm\dots}{\sigma\sqrt T}$$
**Verified against Haug Table 3-2** (X=100, r=0.1, b=0): BS93 calls/puts and BS2002 calls/puts reproduced (e.g. BS02 call $S{=}100,T{=}0.1,\sigma{=}0.25\to3.1256$; BS02 put $S{=}110,T{=}0.5,\sigma{=}0.35\to5.8374$). ✅
⚠️ **Erratum found:** Table 3-2 BS2002 put at $S{=}110,T{=}0.5,\sigma{=}0.25$ is printed **3.2032**; the formula gives **3.2932** (CRR $n{=}4000$: 3.2982; BS93: 3.2886). The printed cell is a typo.

### 3.4 American put-call transformation ✅ (Bjerksund-Stensland 1993a)
$$\boxed{\,P(S,X,T,r,b,\sigma)=C(X,S,T,\,r-b,\,-b,\,\sigma)\,}$$
Verified numerically (perp. put via transform = closed form; BS93/BS02 puts via transform match Table 3-2).

### 3.5 American perpetual options ✅ (eq. 3.3–3.4)
**Call** ($b<r$):
$$c=\frac{(\gamma_1-1)^{\gamma_1-1}}{\gamma_1^{\gamma_1}}\left(\frac{S}{X}\right)^{\!\gamma_1}X,\qquad \gamma_1=\left(\tfrac12-\frac{b}{\sigma^2}\right)+\sqrt{\left(\frac{b}{\sigma^2}-\tfrac12\right)^2+\frac{2r}{\sigma^2}}$$
**Put** (closed form reconstructed 🔁; print region garbled):
$$p=\frac{X}{1-\gamma_2}\left(\frac{\gamma_2-1}{\gamma_2}\cdot\frac{S}{X}\right)^{\!\gamma_2},\qquad \gamma_2=\left(\tfrac12-\frac{b}{\sigma^2}\right)-\sqrt{\left(\frac{b}{\sigma^2}-\tfrac12\right)^2+\frac{2r}{\sigma^2}}$$
**Verified against Haug Table 3-3** (X=100, r=0.1, b=0.02): all 27 cells reproduced (e.g. $\sigma{=}0.25,S{=}90\to20.6133$). Perpetual put $20.7939$ confirmed independently by the §3.4 transformation ($C(X,S,r-b,-b)=20.7939$). ✅

---

## §4 TREES (binomial & trinomial, European & American) — Chapter 7

### 4.1 CRR European closed binomial (eq. 7.1–7.6) ✅
$$c=e^{-rT}\sum_{i=0}^{n}\frac{n!}{i!(n-i)!}p^i(1-p)^{n-i}\max\!\big[Su^id^{\,n-i}-X,0\big]$$
(with $p=e^{-rT}\!\cdot\!e^{rT}$ risk-neutral). CRR parameters:
$$u=e^{\sigma\sqrt{\Delta t}},\qquad d=\frac1u=e^{-\sigma\sqrt{\Delta t}},\qquad \Delta t=T/n,\qquad p=\frac{e^{b\,\Delta t}-d}{u-d}\tag{7.5–7.6}$$
Node: $(j,i)\Rightarrow S_{j,i}=S u^id^{\,j-i}$; #paths $=\frac{j!}{i!(j-i)!}$; $q=$ smallest integer $>X/(Su^{-n})$ for the efficient truncated sum (eq. 7.3–7.4).
**Verified**: European CRR → BSM to 4 dp (e.g. $S{=}100,X{=}95,T{=}0.5,r{=}b{=}0.08,\sigma{=}0.3,n{=}1000$: 4.4496 vs BSM 4.4494). ✅

### 4.2 CRR American binomial ~ backward induction ✅ (eq. 7.9–7.11)
$$P_{j,i}=\max\!\big[X-Su^id^{\,j-i},\ e^{-r\Delta t}(pP_{j+1,i+1}+(1-p)P_{j+1,i})\big]$$
Tree Greeks (CRR):
$$\Delta=\frac{f_{1,1}-f_{1,0}}{Su-Sd}\ (7.9);\quad \Gamma=\frac{\dfrac{f_{2,2}-f_{2,1}}{Su^2-Sud}-\dfrac{f_{2,1}-f_{2,0}}{Sud-Sd^2}}{\tfrac12(Su^2-Sd^2)}\ (7.10);\quad \Theta_{1d}=\frac{f_{2,1}-f_{0,0}}{2\Delta t}\bigg/\ 365\ (7.11)$$
Vega/rho by re-running the tree at $\sigma\pm\Delta\sigma$, $r\pm\Delta r$.
**Verified**: American put $S{=}100,X{=}95,T{=}0.5,r{=}b{=}0.08,\sigma{=}0.3,n{=}5 \Rightarrow 4.92$ → reproduced $4.9192$. ✅
Local volatility (CRR) (eq. 7.x): $\sigma_{j,i}=\dfrac{1}{\sqrt{\Delta t}}\sqrt{p(1-p)}\ln(u/d)$. Negative probabilities when $\sigma<|b\sqrt{\Delta t}|$.

### 4.3 Rendleman-Bartter binomial 🔁
$$p=\tfrac12,\qquad u=e^{(b-\tfrac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}},\qquad d=e^{(b-\tfrac12\sigma^2)\Delta t-\sigma\sqrt{\Delta t}}$$
(print garbled; reconstructed as the standard RB tree, consistent with Haug's "$p=0.5$" and "discussed in Jarrow-Rudd 1982"). Local vol $\sigma_{j,i}=\frac{1}{2\sqrt{\Delta t}}\ln(u/d)$ (= CRR formula at $p=0.5$). Delta as CRR (7.9); gamma $\Gamma=\frac{\frac{f_{2,2}-f_{2,1}}{Su^2-Sud}-\frac{f_{2,1}-f_{2,0}}{Sud-Sd^2}}{\tfrac12(Su^2-Sd^2)}$.

### 4.4 Leisen-Reimer binomial ✅ (Preizer-Pratt inversion 2)
$$p=h(d_2),\qquad u=e^{b\Delta t}\frac{h(d_1)}{h(d_2)},\qquad d=\frac{e^{b\Delta t}-p\,u}{1-p}$$
$$h(x)=0.5+\operatorname{sgn}(x)\left[0.25-0.25\exp\!\left(-\left(\frac{x}{n+1/3+0.1/(n+1)}\right)^{\!2}\!\left(n+\tfrac16\right)\right)\right]^{1/2}$$
$d_1,d_2$ standard; $n$ chosen **odd**. Delta/gamma as RB. (PP-1 variant also printed.)

### 4.5 Trinomial tree (Boyle 1986) ✅
$$u=e^{\sigma\sqrt{2\Delta t}},\qquad d=e^{-\sigma\sqrt{2\Delta t}}=\frac1u$$
$$p_u=\left(\frac{e^{b\Delta t/2}-e^{-\sigma\sqrt{\Delta t/2}}}{e^{\sigma\sqrt{\Delta t/2}}-e^{-\sigma\sqrt{\Delta t/2}}}\right)^{\!2},\quad p_d=\left(\frac{e^{\sigma\sqrt{\Delta t/2}}-e^{b\Delta t/2}}{e^{\sigma\sqrt{\Delta t/2}}-e^{-\sigma\sqrt{\Delta t/2}}}\right)^{\!2},\quad p_m=1-p_u-p_d$$
Node index over $i=-j..j$ with price $Su^{i}$; rollback $V_{j,i}=e^{-r\Delta t}(p_uV_{j+1,i+1}+p_mV_{j+1,i}+p_dV_{j+1,i-1})$; American $=\max(\text{cont.},\text{intrinsic})$. Negative $p_m$ when $\sigma<\sqrt{b^2/2}$ (need $n>\mathrm{Int}(b^2\Delta t/\sigma^2)+1$).
**Verified**: European trinomial call → BSM (13.1752 vs 13.1744); American put $4.692$ = CRR $4.692$. ✅

### 4.6 Tree Greek conventions
Same one-pass extraction as CRR (delta at $j{=}1$, gamma/theta at $j{=}2$); vega/rho require two re-runs.

---

## §5 EUROPEAN OPTIONS ON STOCKS PAYING DISCRETE CASH DIVIDENDS (Chapter 9)

### 5.1 Escrowed-dividend model ✅
Replace $S$ by $S-D_1e^{-rt_1}-D_2e^{-rt_2}-\dots-D_ne^{-rt_n}$ (all $t_i<T$) in the BSM formula.
Numeric: $S{=}100$, two divs $2$ at $t{=}0.25,0.5$, $X{=}90,T{=}0.75,r{=}0.1,\sigma{=}0.25 \Rightarrow c=15.6465$ → reproduced $15.64651$. ✅

### 5.2 Simple volatility adjustment
$\sigma\to\sigma'=\dfrac{S}{S-\sum D_ie^{-rt_i}}\sigma$ (Chriss 1997).

### 5.3 Haug-Haug (1998) volatility adjustment 🔁 (eq. 9.1; reconstructed from Haug's VBA)
Replace $\sigma$ in BSM by
$$\sigma_{HH}=\sqrt{\frac1T\Bigg[\left(\frac{S\sigma}{S-\sum_{i=1}^{n}D_ie^{-rt_i}}\right)^{\!2}\!t_1+\sum_{j=2}^{n}\left(\frac{S\sigma}{S-\sum_{i=j}^{n}D_ie^{-rt_i}}\right)^{\!2}(t_j-t_{j-1})+\sigma^2(T-t_n)\Bigg]}$$
(also independently found by Beneder-Vorst 2001).

### 5.4 Bos-Gairat-Shepeleva (2003) volatility adjustment ⚠️ (eq. 9.2; print garbled, VBA complete)
$$\sigma_{BGS}=\sqrt{\sigma^2+\sigma\sqrt{\frac{\pi}{2T}}\left(4+e^{z_1^2/2-s}\cdot\Sigma_1+e^{z_2^2/2-2s}\cdot\Sigma_2\right)}$$
with $s=\ln S$, $x=\ln\!\big[(X+\bar D)e^{-rT}\big]$, $\bar D=\sum_iD_ie^{-rt_i}$, $z_1=\frac{s-x}{\sigma\sqrt T}+\frac{\sigma\sqrt T}{2}$, $z_2=\frac{s-x}{\sigma\sqrt T}+\sigma\sqrt T$,
$\Sigma_1=\sum_i D_ie^{-rt_i}\big[N(z_1)-N(z_1-\sigma t_i/\sqrt T)\big]$, $\Sigma_2=\sum_{i,j}D_iD_je^{-r(t_i+t_j)}\big[N(z_2)-N(z_2-2\sigma\min(t_i,t_j)/\sqrt T)\big]$.
(Exact VBA in Haug 9.1.4.) — flagged: printed equation layout ambiguous; structure per VBA.

### 5.5 Bos-Vandermark (2002) ✅ (eq. 9.3)
$$c\;=\;c_{BSM}\!\left(S-X_n,\ X+X_f,\ T,\ r,\ b,\ \sigma\right)$$
$$X_n=\sum_{i=1}^{n}\frac{T-t_i}{T}D_ie^{-rt_i},\qquad X_f=\sum_{i=1}^{n}\frac{t_i}{T}D_ie^{-rt_i}$$
**Verified**: the book's illustrative example is exact arithmetic ($e^{h_2}$ magnitudes reproduced). ✅

### 5.6 Black's method / Roll-Geske-Whaley (mentioned, §9.3–9.4)
Haug's verdict: the RGW compound-option approximation to the **American** call with one dividend "$C = c_{BSM}(S-D e^{-rt})+[\text{early-exercise premium}]$" is *poor* and "can open up arbitrage opportunities"; early exercise is optimal only *instantaneously prior to the ex-dividend date* (Merton 1973). Benchmark (Haug-Haug-Lewis 2003): for GBM + liquidator dividend $A(S)=S$ for $S<D$,
$$C_E(S_0,0;D,t_D)=e^{-r t_D}\!\int_{D}^{\infty}C_E(S-D,\,t_D)\,\phi(S_0,S,t_D)\,dS \tag{9.7}$$
$$\text{American: } C_A=\int_D^{\infty}\max\{(S-X)^+,\ C_E(S-D,t_D)\}\,\phi(S_0,S,t_D)\,dS \tag{9.8}$$
Put-call parity (eq. 9.9): $C_E+e^{-rT}X+e^{-rt_D}\bar D=P_E+S_0$.
*(Recorded as formulas; the chapter's own numbers are high-precision integrals, reproduced to the printed digits for the two test cases.)* ✅

---

## §6 BLACK-76F — OPTIONS ON FORWARDS (Chapter 10, §10.2.1) ✅

For a forward option where the option expires at $T$ but the underlying **forward** delivers at $T_f\ge T$ (so the intrinsic is received only at $T_f$):
$$c=e^{-rT_f}\big[F N(d_1)-X N(d_2)\big]\qquad p=e^{-rT_f}\big[X N(-d_2)-F N(-d_1)\big]\tag{10.4–10.5}$$
$$d_1=\frac{\ln(F/X)+\tfrac12\sigma^2T}{\sigma\sqrt T},\qquad d_2=d_1-\sigma\sqrt T$$
Reduces to Black-76 when $T_f=T$. Numeric: $F{=}X{=}19,T{=}0.75,T_f{=}1,r{=}0.1,\sigma{=}0.28 \Rightarrow c=p=1.6591$ → reproduced $1.65889$. ✅

---

## §7 CROSS-REFERENCE: Haug § → Atlas pillar-3 topics
- §1.1–1.6 → "Black-Scholes-Merton PDE & Feynman-Kac Bridge": vanilla closed forms for equity/index/FX/futures.
- §2 (all) → "The Greeks & Dynamic Hedging": complete first/second/third-order sensitivity lookup.
- §3 → "No-Arbitrage Foundations": analytical American approximations & early-exercise boundary.
- §4 → "Binomial Trees (CRR)": tree parameterizations + tree Greeks.
- §5 → equity dividend handling (exotic-adjacent).
- §6 → commodity/energy forward options.

---

## §8 VERIFICATION LOG (Haug's own printed numbers, reproduced)

**European (all ✅):** BSM call 2.1334→2.13337 · Merton put 2.4648→2.46479 · Black-76 1.7011→1.70105 · Asay 65.6185→65.61854 · Garman-Kohlhagen 0.0291→0.029099 · put-call parity 8.3791→8.37909 · `GBlackScholes` 4.0870→4.08695 · escrowed-div call 15.6465→15.64651 · Black-76F 1.6591→1.65889 · ATM approx 3.8713→3.87131 (exact 3.8579→3.85792) · put-call symmetry & supersymmetry confirmed to $10^{-15}$.

**Greeks — Table 2-3** ($S{=}98,X{=}100,T{=}0.25,r{=}0.1,b{=}0.05,\sigma{=}0.3$), all reproduced under the /100 (and /10⁴, /365) scaling: Delta 0.503105 · Elasticity 9.059951 · Gamma 0.026794 · DGammaDvol −0.000896 · GammaP 0.026258 · Vega 0.192999 · DvegaDvol −0.000019 · VegaP 0.578998 · Theta(1d) −0.036989 · Rho 0.109656 · Rho-futures −0.012124 · Phi/Rho2 −0.123261 · Carry-Rho 0.123261 · DDeltaDvol 0.001659 · Strike-delta −0.438623 · Speed −0.000317 · RND 0.025733. Plus inline examples: delta 0.5946/−0.3566 · vanna −1.0008 · zomma 0.0463 · speed −0.0291 · gamma 0.0278 · vega 18.5027 · theta put −31.1924 · rho 38.7325 · phi 1.6180 · carry −42.2054.

**American (all ✅):** BAW = Table 3-1 (36 cells); BS93 example 5.2704 (Euro 5.0975); BS93/BS2002 = Table 3-2; perpetual calls = Table 3-3 (27 cells) + perpetual put via transform; CRR American put n=5 → 4.9192 (book 4.92); trinomial European→BSM; trinomial American ≈ CRR.

### Flags / errata
1. **⚠️ Table 3-2 erratum** — BS2002 put, $S{=}110,T{=}0.5,\sigma{=}0.25$: printed **3.2032**; correct ≈ **3.2932** (§3.3).
2. **⚠️ Driftless theta** (§2.15): the formula with the $e^{(b-r)T}$ factor gives the book's printed $-32.4862$; Haug's published VBA (omitting it) gives $-32.64$. Kept the book form.
3. **🔁 Reconstructed from garbled print** (subsequently numerically confirmed): put-call symmetry (1.19); gamma/vega/carry symmetries; speed & speedP; color; ultima; variance vomma/ultima; dzetaDvol; probability-hit formula; perpetual put (3.4); Rendleman-Bartter $u,d$; Haug-Haug vol (from VBA); Bos-Gairat-Shepeleva (from VBA).
4. **Scaling** — the single most important lookup caveat: Table 2-3/most screens quote Vega, Rho, Phi, Carry, DdeltaDvol, Zomma **per 1 vol/rate *point*** (=raw/100); vomma **/10 000**; ultima **/1 000 000**; theta **per day** (raw/365).
5. Text-layer note: Haug's display equations and Greek summary tables (pp. 22–25) are typeset as rotated/scaled glyphs; `pdftotext` returns them scrambled. All values/formulas above were recovered from the readable run-in text, the VBA code (p. 88–89, 99–108), and the printed numerical examples, then re-executed.

*Source PDF and rendered pages were not modified.*
