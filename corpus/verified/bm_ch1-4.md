# BM Chapters 1–4 — Per-Chapter Verification Report
(bm.txt lines: Ch1 2273–3335 · Ch2 3335–4564 · Ch3 4565–9367 · Ch4 9367–11778)

Source extraction checked: `derivative_pricing.md` PART B, Ch 1–4 entries (lines 209–246).
Method: full text read of each chapter body against the extraction's concept/result claims.

## VERDICT: content is accurate — no substantive errors found.
Every formula/claim the extraction makes for Ch 1–4 is confirmed present and correctly
stated in the book text. Flagged items below are **minor precision notes and coverage
gaps**, not errors. No source file was modified.

---

## Ch 1 — Definitions and Notation — VERIFIED ACCURATE
- Bank account `dB(t)=r_t B(t)dt, B(0)=1`, `B(t)=exp(∫_0^t r_s ds)` (1.1–1.2); short rate =
  instantaneous (spot) rate of accrual. ✓
- Stochastic discount factor `D(t,T)=B(t)/B(T)=exp(−∫_t^T r_s ds)` (1.4); note book stresses
  D(t,T) is RANDOM when rates stochastic and generally ≠ P(t,T) (P deterministic at t). ✓
- ZCB `P(t,T)`, `P(T,T)=1`; day-count conventions Actual/365, Actual/360, 30/360. ✓
- Spot rates: continuously-compounded `R(t,T)=−lnP/τ`, simply-compounded
  `L(t,T)=(1−P)/(τP)` (LIBOR is simply-compounded, Actual/360), annual `Y`, k-times `Y^k`;
  all collapse to `r(t)` as T→t. ✓
- Zero-coupon curve (= term structure) and zero-bond curve. Forward rates via FRA; simply
  compounded forward `F(t;T,S)=(1/τ)(P(t,T)/P(t,S)−1)` (1.20); instantaneous forward
  `f(t,T)=−∂_T ln P(t,T)`, `P(t,T)=exp(−∫_t^T f)`. ✓
- IRS: payer (PFS)/receiver (RFS); fixed leg `Nτ_i K`, floating `Nτ_i L(T_{i-1},T_i)`;
  RFS value = sum of FRAs = `−NP(t,T_α)+NP(t,T_β)+NΣτ_iKP(t,T_i)` (1.24). ✓
- Forward swap rate `S_{α,β}(t)=(P(t,T_α)−P(t,T_β))/(Σ_{i=α+1}^β τ_i P(t,T_i))` (1.25) = the
  fixed rate that zeroes the swap; also expressible via products of `1/(1+τ_j F_j)`. ✓
- Floating-rate note "always trades at par". Coupon-bearing bond value `Σ c_i P(t,T_i)`. ✓
- Caps/floors as payer/receiver-IRS executed only if positive; cap/floorlet; cap =
  sum of caplets; market Black pricing (1.26–1.27) with `Bl(K,F,v,ω)`; ATM/ITM/OTM. ✓
- Swaptions: payer/receiver; maturity=T_α, tenor=T_β−T_α; caplet-additive decomposition
  possible, NOT for swaptions (sum inside `(·)^+` ⇒ terminal correlation matters); market
  Black pricing (1.28–1.29); ATM/ITM/OTM. ✓

Precision notes / gaps (minor):
- Extraction abbreviates "spot L(S,T), forward F(t;S,T)" and lists the instruments, but
  omits: the FRA contract as the object defining forward rates; the fixed/floating leg
  structure of the IRS; the *stochastic-D vs bond-P distinction* (a conceptual cornerstone);
  "floating-rate note trades at par"; and the swap rate written in forward-rate products.
- "Forward swap rate S_{α,β}(t) (Level-1 rate)" — the label "Level-1" is not BM terminology;
  appears to be an Atlas-internal tag. Harmless but unexplained.

## Ch 2 — No-Arbitrage Pricing and Numeraire Change — VERIFIED ACCURATE
- Harrison–Kreps/Pliska continuous-time no-arbitrage: EMM Q (D(0,·)S a Q-martingale);
  complete market ⇔ unique Q; attainable claim uniquely priced `π_t=E(D(t,T)H|F_t)` (2.2). ✓
- Numeraire = any positive non-dividend-paying asset; relative prices `X/N` martingales
  under `Q^N`; RN derivative `dQ^U/dQ^N=(U_T N_0)/(U_0 N_T)` (2.5). ✓
- Fact One: price/numeraire martingale (so risk-neutral drift of any asset = r_t·S_t, and
  F_LIBOR is a martingale under its own-bond measure; forward swap rate martingale under the
  swap (annuity) measure). Fact Two: risk-neutral price invariant under change of numeraire. ✓
- Change-of-numeraire toolkit: drift-shift formula (2.12), shock/CdW formula (2.13),
  lognormal case (2.14–2.15), and DC-operator forms (2.16)–(2.18):
  `CdW^S = CdW^U − ρ DC(ln(S/U)) dt` — matches the extraction's stated form. ✓
- Convenient-numeraire recipe; forward measure `Q^T` (T-bond numeraire), pricing
  `π_t=P(t,T)E^T{H_T|F_t}` (2.20); simply-compounded forward rate spanning to T is a Q^T
  martingale (Prop 2.5.1), `E^T{L(S,T)}=F(t;S,T)`; `E^T{r_T}=f(t,T)` (Prop 2.5.2). ✓
- Fundamental pricing: `π_t=E[exp(−∫_t^T r_s ds) H_T|F_t]` (2.22); ZCB call option (2.23);
  `dQ^T/dQ = D(0,T)/P(0,T)`. Cap/floor = portfolio of European ZCB options via caplet
  ↔ bond-put/bond-call mapping with `X'=1/(1+Xτ_i), N'=N(1+Xτ_i)` (2.26–2.29). ✓
- Deferred payoffs (anticipate & discount), multiple payoffs (collapse to one terminal
  forward measure = "terminal measure", eq 2.30), foreign markets RN derivative
  `dQ^f/dQ=(Q_T B^f_T)/(Q_0 B_T)` (2.32) as a numeraire change B^f → B/Q. ✓

Precision notes / gaps (minor):
- Toolkit formula range "2.12–2.18" is accurate, though numbering in text is (2.11),(2.12)–
  (2.18) with (2.13),(2.14),(2.15) — a subset labelled 2.12–2.18 is fine.
- Extraction does not state the forward-measure martingale/expectation result
  (Prop 2.5.1/2.5.2) explicitly, nor the forward RN derivative — useful but optional additions.
- Book intro promises an explicit cap-AND-swaption example; Ch 2 actually works out the
  cap(let)/floor as bond options; swaption pricing under forward measures is left to later
  chapters. Extraction does not over-claim here.

## Ch 3 — One-Factor Short-Rate Models — VERIFIED ACCURATE
- Endogenous vs exogenous term-structure models; market price of risk connects Q^0↔Q; the
  model-selection checklist (positive rates? distribution? explicit bonds? explicit
  bond-option/cap/floor/swaption? mean reversion? volatility structure? forward-measure
  dynamics? MC? lattice? historical estimation) matches the extraction's list. ✓
- Vasicek `dr=k[θ−r]dt+σdW` (3.5); Gaussian, mean-reverting to θ, negative rates possible;
  bond `P=A e^{−Br}` (3.8), `B=(1/k)(1−e^{−k(T−t)})`; T-forward dynamics
  `dr=[kθ−B(t,T)σ²−kr]dt+σdW^T` (3.9); European ZCB-option closed form (Jamshidian, 3.10). ✓
- Dothan `dr=a r dt+σ r dW` (3.17); lognormal; only lognormal short-rate model with an
  (admittedly double-integral) explicit bond formula (3.20); NO bond-option formula. ✓
- Explosion: for any lognormal instantaneous-rate model `E[B(∆t)]=E[e^{∫_0^{∆t}r}]=∞`
  (Sandmann–Sondermann 1997: model rates with a strictly-positive compounding period
  lognormally instead); shared by Dothan/EV/Black–Karasinski; not affine. ✓
- CIR `dr=k(θ−r)dt+σ√r dW` (3.21), positivity iff `2kθ>σ²`; noncentral chi-squared
  transition density; bond `P=A e^{−Br}` with `h=√(k²+2σ²)` (3.24–3.25); bond option closed
  form via chi-squared (3.26). ✓
- EV `dr=r(θ+σ²/2 − a ln r)dt+σr dW` (3.30); always mean-reverting; no explicit bond/option
  formulas; lognormal ⇒ explosion; not affine. ✓
- Affine term structure: `R(t,T)=α(t,T)+β(t,T)r(t)` ⇔ `P=A(t,T)e^{−B(t,T)r}`; ATS ⇐
  (always) affine drift/variance `b(t,x)=λx+η, σ²(t,x)=γx+δ`; converse (ATS ⇒ affine
  coefficients) only in the time-homogeneous case; A,B solve
  `∂_t B+λB−½γB²+1=0 (B(T,T)=0)` and `∂_t[ln A]−ηB+½δB²=0 (A(T,T)=1)` — matches extraction
  exactly, incl. the "time-homogeneous" qualifier on necessity. Forward-rate absolute vol
  `σ_f=(∂_T B)σ(t,r)` (3.29). ✓
- Hull–White extended Vasicek `dr=[ϑ(t)−ar]dt+σdW` (3.33); exact fit via
  `ϑ(t)=∂_T f^M(0,t)+a f^M(0,t)+(σ²/2a)(1−e^{−2at})` (3.34); Gaussian; x=HW-0 Vasicek with
  `α(t)=f^M(0,t)+(σ²/2a²)(1−e^{−at})²`, `r=x+α`; bond `P=A e^{−Br}` (3.39); ZCB call/put,
  caps/floors closed form (3.40–3.43); coupon-bond options & swaptions via Jamshidian
  decomposition (3.44–3.46); 2-stage trinomial tree (tree for x, then displace nodes). ✓
- Deterministic-shift extension: given base model `x`, set `r_t=x_t+ϕ(t;α)` (3.66); bond
  price factorizes (3.67); exact initial fit iff `ϕ=f^M(0,t)−f^x(0,t;α)` (3.68); option
  formulas preserved (3.72); applies to VAS (VAS++ ≡ HW), CIR (CIR++), Dothan (shifted
  lognormal), EV (EEV). ✓
- CIR++: `dx=k(θ−x)dt+σ√x dW`, `r=x+ϕ`; shifted noncentral-χ² distribution; affine; exact
  fit + explicit bond & bond-option (chi-squared, 3.78) + caps/floors + Jamshidian swaptions;
  trinomial tree (via y=√x); early-exercise dynamic programming; MC; positivity condition
  analysis (3.9.3). ✓
- JCIR: `dr=k(θ−r)dt+σ√r dW+dJ` with exponentially-distributed positive jumps; affine
  (log-affine bond); JCIR++ referenced to credit chapters; yields higher implied vols. ✓
- Volatility structures (humped/time-dependent), implied cap-vol curves & swaption surfaces,
  real-data calibration — present (3.6, 3.7, 3.12–3.14). ✓

Precision notes / gaps (minor):
- Extraction's affine ODEs and the "necessary & sufficient (time-homogeneous)" wording are
  faithful. Note the forward (sufficient) direction holds for arbitrary time-dependent
  coefficients; only the converse requires time-homogeneity — the extraction's compression
  is acceptable.
- "CIR++ ... positive rates + exact fit (best of both)": exact fit always holds; positivity
  is guaranteed only under parameter restrictions (conditions on ϕ/f^CIR, §3.9.3). The
  extraction conveys this as a best-of-both property — worth flagging the caveat for precision.

## Ch 4 — Two-Factor Short-Rate Models — VERIFIED ACCURATE
- Motivation (4.1): one-factor models force perfect (corr=1) correlation between rates of
  all maturities at a given instant (Vasicek example), which is unrealistic; two factors give
  non-perfect maturity correlation and materially better calibration of correlation-sensitive
  products such as European swaptions. ✓ (matches extraction's stated rationale)
- G2++ dynamics (4.4–4.5): `r(t)=x(t)+y(t)+ϕ(t)`, `dx=−a x dt+σdW_1`, `dy=−b y dt+η dW_2`,
  `dW_1 dW_2=ρdt`; Gaussian, negative rates possible with small probability. ✓
- Bond price: `P(t,T)=(P^M(0,T)/P^M(0,t)) exp{A(t,T)}` (4.14) with
  `A=½[V(t,T)−V(0,T)+V(0,t)]−B(a,t,T)x(t)−B(b,t,T)y(t)`. ✓
- Exact fit condition `ϕ(T)=f^M(0,T)+(σ²/2a²)(1−e^{−aT})²+(η²/2b²)(1−e^{−bT})²
  +ρ(ση/ab)(1−e^{−aT})(1−e^{−bT})` (4.12). **Remark 4.2.1** confirms: only the INTEGRAL of ϕ
  is needed, computed directly from the market discount curve — no need to differentiate or
  interpolate the forward curve. ✓ (extraction's Remark 4.2.1 note is exactly right)
- Forward-rate vol `σ_f(t,T)=√(σ²e^{−2a(T−t)}+η²e^{−2b(T−t)}+2ρσηe^{−(a+b)(T−t)})` (4.16);
  humped structure possible only for ρ<0. ✓
- T-forward-measure factor dynamics (Lemma 4.2.2, eq 4.18); Gaussian r under Q^T (4.20);
  ZCB call/put closed forms (4.21–4.24); caplets/floorlets and caps/floors closed form
  (4.27–4.30); swaptions via a 1-D numerical integral (Theorem 4.2.3, 4.31). ✓
- Equivalence with the Hull–White two-factor model (4.32) proven explicitly (4.2.5) by the
  transformations σ,η,ρ,ϕ — so G2++ ≡ shifted HW two-factor. ✓
- Approximating binomial tree in both dimensions (4.2.6); calibration examples (4.2.7). ✓
- CIR2 / CIR2++ (4.3): two independent square-root (CIR) factors `dx=k_1(θ_1−x)dt+σ_1√x dW_1`,
  `dy=k_2(θ_2−y)dt+σ_2√y dW_2`, ξ=x+y; shown equivalent to Longstaff–Schwartz (1992b)
  (`ξ=μ_x X+μ_y Y`); bond price = product of one-factor CIR bonds (4.38); affine 2-D term
  structure; forward-measure dynamics factor-by-factor as in one-factor CIR (3.27); bond
  options/caps/floors via 2-D noncentral-χ² integral (4.40, Longstaff–Schwartz / Chen–Scott
  1-D reduction). CIR2++ adds `ϕ` to fit the initial curve exactly (`ϕ=f^M−f^1(x)−f^1(y)`,
  4.42). Positive rates under parameter restrictions; forward-rate vol curve only decreasing
  (no hump) — needs ρ≠0 which would destroy tractability; Gaussian-mapping (Brigo–Alfonsi)
  restores tractability. ✓
- Short rate = sum of two independent noncentral-χ² (fatter tails than Gaussian) for CIR2++. ✓

Precision notes / gaps (minor):
- Extraction's G2++ bullet is fully accurate. The swaption price is a *numerical 1-D
  integral*, not a closed form — extraction does not mislabel it. Jamshidian's decomposition
  is NOT available in two-factor CIR2++ (needs numerical integration/MC/tree) — worth noting.
- Extraction gives CIR2/CIR2++ one line; a fuller entry would note the LS model equivalence
  via `x=μ_x X, y=μ_y Y` parameter mapping and the LS/Chen–Scott integral form.

## Chapter-title / boundary integrity
The extraction's four PART-B Ch 1–4 headers match the actual BM chapter titles
("Definitions and Notation"; "No-Arbitrage Pricing and Numeraire Change"; "One-Factor
Short-Rate Models"; "Two-Factor Short-Rate Models") and each chapter's described scope maps
1:1 to the corresponding body text. No content was attributed to the wrong chapter.

---
File written 2026-09-09. Text-based verification of `/tmp/atlas_extract/derivative_pricing.md`
BM Ch1–4 against `/tmp/atlas_extract/bm.txt`. Sources unmodified.
