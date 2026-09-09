# Hasbrouck *Empirical Market Microstructure* — Per-Chapter Verification, Chapters 6–10

**Scope:** Text-based verification of the existing extraction `/tmp/atlas_extract/market_microstructure.md` against the source text `/tmp/atlas_extract/hasbrouck.txt` (Hasbrouck, OUP 2007).

**Chapters covered here (book ch → section in extraction md):**
- Ch 6 *Order Flow and the Probability of Informed Trading* → extraction §"5. Order Flow & PIN (Ch 6)"
- Ch 7 *Strategic Trade Models* (Kyle) → extraction §"6. Strategic Trade Models: Kyle (Ch 7)"
- Ch 8 *A Generalized Roll Model* → extraction §"7. Generalized Roll Model & Random-Walk Decompositions (Ch 8)"
- Ch 9 *Multivariate Linear Microstructure Models* → extraction §"8. Multivariate Linear Microstructure Models (Ch 9)"
- Ch 10 *Multiple Securities and Multiple Prices* → extraction §"9. Multiple Securities & Price Discovery (Ch 10)"

**Headline verdict:** The extraction is highly faithful and technically accurate for ch6–10. All central formulas (PIN, Kyle equilibrium, generalized-Roll autocovariances/identification, VMA/VAR/Cholesky random-walk decomposition, cointegration/VECM/information-share) match the source. Corrections are confined to presentation nuances (1 substantive: the Kyle expected-profit formula is mis-rendered/conditional-vs-unconditional), plus several minor qualifiers and completeness gaps. No source files were modified.

---

## CHAPTER 6 — Order Flow and the Probability of Informed Trading (PIN)
Extraction section: §"5. Order Flow & PIN (Ch 6)" (md lines 82–93).

### Verification per claim (against hasbrouck.txt lines 2558–2746)
- Buy/sell counts conditional on V high/low are binomial with p=(1∓µ)/2; mixture of binomials (eq 6.1–6.2). **CORRECT.**
- Event-uncertainty + Poisson arrivals: informed intensity µ, uninformed intensity ε, event prob α (Easley-Kiefer-O'Hara 1997; Easley-Hvidkjaer-O'Hara 2002). **CORRECT** (sect. 6.2; line 2631).
- Joint Poisson mixture Pr(b,s) = (1−α)Pr(b;ε)Pr(s;ε) + α[δ·Pr(b;ε)Pr(s;µ+ε) + (1−δ)·Pr(b;µ+ε)Pr(s;ε)] (eq 6.3). **CORRECT** — note the raw OCR text prints the last intensity as "εx" (typo in the PDF text layer); extraction correctly normalizes it to ε.
- Expected total arrival intensity = 2ε+αµ; **PIN = αµ/(αµ+2ε)** (eq 6.4). **CORRECT.**
- α and µ enter PIN only as product αµ; estimates of α and µ individually imprecise (negatively correlated), PIN stable/estimable. **CORRECT** (lines 2678–2691).
- MLE over daily buy/sell counts; PIN ≈ order-flow one-sidedness measure; sensibly related to information via slow news diffusion / fragmentation. **CORRECT** (sect. 6.3).

### Findings
- No errors found.
- Minor gap (optional): the extraction omits the book's point that in the daily likelihood only the *total* buy/sell count per day enters (not individual order sequence; line 2653–2654) — a nuance, not an error.
- Consistency note: the extraction's mapping table (md line 299) repeats PIN = αµ/(αµ+2ε) and in one spot (md line 89) writes "2ε" correctly; the Hasbrouck denominator is αµ+2ε. Consistent throughout. Good.

---

## CHAPTER 7 — Strategic Trade Models (Kyle 1985)
Extraction section: §"6. Strategic Trade Models: Kyle (Ch 7)" (md lines 96–106).

### Verification per claim (hasbrouck.txt lines 2747–3010)
- v~N(p0,Σ0); informed demand x; noise u~N(0,σu²); MM observes total y=x+u, price p=λy+µ. **CORRECT** (sect. 7.1).
- λ = inverse measure of liquidity (price impact); 1/λ = market depth. **CORRECT** (also implied by Fig 7.1 caption).
- Informed profit π=(v−p)x, Eπ=x(v−λx−µ) ⇒ x=(v−µ)/2λ; with linear conjecture x=α+βv ⇒ α=−µ/2λ, β=1/2λ. **CORRECT** (eq 7.1). Extraction's shorthand "x=β(v−µ), β=1/(2λ)" is valid at equilibrium µ=p0.
- Bivariate normal projection E[Y|X=x] = µY + (σXY/σX²)(x−µX). **CORRECT.**
- Equilibrium (eq 7.4): λ = ½√(Σ0/σu²); β = √(σu²/Σ0); µ=p0. **CORRECT.**
- Var[v|p] = Var[v|y] = Σ0/2 — half the private information impounded, independent of noise intensity. **CORRECT** (lines 2876–2879).
- Multi-period: Δx_n = β_n(v−p_{n−1})Δt; p_n = p_{n−1}+λ_n(Δx_n+Δu_n); informed "slices and dices"; total order flow uncorrelated. **CORRECT** (eqs sect. 7.2).
- Huberman-Stanzl (2004): linear price schedules of Kyle model do not allow manipulation; only linear price schedules have this property. **CORRECT** (line 2977–2979).

### CORRECTION(S)
1. **[Substantive — presentation]** The extraction renders informed profit as "Eπ = ½√(σu²Σ0)·…". The book (eq 7.5, line 2864–2868) gives the profit **conditional on the value realization**: `Eπ = ((v−p0)²/2)·√(σu²/Σ0)`, and states it is increasing in the divergence (v−p0)² and in noise-trading variance σu². The expression "½√(σu²Σ0)" is only the *unconditional* expected profit (average over the v-distribution) and is NOT how Hasbrouck presents it. Moreover Hasbrouck's drivers are the squared divergence (v−p0)² and noise variance; for a *given* v the profit actually **decreases** in Σ0. The extraction's "increasing in … value uncertainty" is only true unconditionally. Recommend flagging conditional-vs-unconditional and citing (v−p0)²·√(σu²/Σ0)/2.

### Findings
- Otherwise accurate. Note the extraction's "1/λ = depth" is standard and consistent with the book's Fig 7.1 ("market depth … over time").

---

## CHAPTER 8 — A Generalized Roll Model
Extraction section: §"7. Generalized Roll Model & Random-Walk Decompositions (Ch 8)" (md lines 110–122).

### Verification per claim (hasbrouck.txt lines 3011–3538)
- Efficient price m_t=m_{t−1}+w_t, w_t=λq_t+u_t; p_t=m_t+cq_t; c = noninformational cost, λ = adverse-selection/price-impact cost. **CORRECT** (eq 8.1).
- Bid/ask symmetric about m_{t−1}+u_t; spread = 2(c+λ). **CORRECT** (lines 3062–3064).
- Δp_t = c(q_t−q_{t−1}) + λq_t + u_t (eq 8.2). **CORRECT.**
- γ0 = c²+(c+λ)²+σu²; γ1 = −c(c+λ) (eq 8.3). **CORRECT.**
- Model has 3 structural params {λ,c,σu²} but only 2 autocovariances / 2 MA params {θ,σε²} → under-identified; but **σw² = λ²+σu² = γ0+2γ1 IS identified**. **CORRECT** (lines 3097–3114).
- Pricing error s_t=p_t−m_t; σs²=Var(s_t); lower bound σs² ≥ θ²σε², attained when all info is trade-related (σu²=0); no upper bound. **CORRECT** (sect. 8.5; eq 8.7, lines 3213–3240).
- Beveridge-Nelson (1981) / Watson (1986) random-walk (permanent/transitory) decomposition: from MA Δp_t=θ(L)ε_t, σw²=θ(1)²σε²; pricing error σs²=ΣC_i²σε², C_i=−Σ_{j>i}θ_j. **CORRECT** (eqs 8.10–8.12). Invariant to identification — **CORRECT** (line 3335).
- Variance ratio (eq 8.14): V_{M,N} = [Var(p_t−p_{t−M})/M]/[Var(p_t−p_{t−N})/N]. **CORRECT.**
- AGF g_x(z)=θ(z⁻¹)θ(z)σε². **CORRECT** (Appendix, line 3494).
- Filtered state estimate f_t=E*[m_t|p_t,p_{t−1},…] = p_t+θε_t. **CORRECT** (sect. 8.4).

### Findings
- [Minor] Extraction: ">1 if microstructure inflates short-horizon variance." The book states this more precisely: with **M<N** (M the shorter horizon), typically V_{M,N}>1, and V declines toward 1 as M→N. Suggest adding the "M<N (shorter horizon in numerator)" qualifier.
- OCR/book-internal note (not an extraction error): the Appendix line printing σw² = [φ(1)]²σε² (line 3509) conflicts with the correct relation σw²=φ(1)⁻²σε² given in Exercise 8.2 — a typesetting slip in the source; the ARMA form σw²=φ(1)⁻²θ(1)²σε² is the correct generalization. Not carried into the extraction.
- Gap (optional): extraction does not mention the general result that σw² is time-scaled (variance per unit time; Var(m_t−m_{t−k})=kσw², and long-run price variance ≈ kσw²), a key economic motivation for why σw² is identified even though the spread components are not.

---

## CHAPTER 9 — Multivariate Linear Microstructure Models
Extraction section: §"8. Multivariate Linear Microstructure Models (Ch 9)" (md lines 126–139).

### Verification per claim (hasbrouck.txt lines 3539–4329)
- System y_t=[Δp_t, x_t']' (price change first, expositional). **CORRECT.**
- VMA y_t=θ(L)ε_t; VAR y_t=φ1y_{t−1}+…+ε_t; invertibility ↔ VMA roots; VAR from series expansion of θ(L)⁻¹. **CORRECT** (sect. 9.1).
- Structural model: q_t=v_t+βv_{t−1} (MA(1), β>0); w_t = u_t+λv_t (efficient price driven by the *order innovation* v_t); Δp_t = u_t+λv_t+c[(v_t+βv_{t−1})−(v_{t−1}+βv_{t−2})] (eq 9.6). **CORRECT.**
- Impulse response ψ_s(ε0)=θ_sε0; cumulative IRF b_s(ε0)=Σ_{k≤s}ψ_k(ε0). **CORRECT** (eqs 9.13–9.14).
- Cholesky Σ=F'F imposes a causal ordering; factor form ε=F'z. **CORRECT** (sect. 9.4). NOTE book-internal notational wobble: the prose says F is "upper triangular" while the displayed 2×2 factor (eq 9.17) is lower-triangular; the random-walk application (eq 9.20) uses an upper-triangular F. Extraction's "Σ=F'F" is faithful and unaffected.
- Random-walk variance σw²=[θ(1)]₁[θ(1)]₁' (first row of θ(1)); for nondiagonal Σ, Cholesky: d=[θ(1)]₁F', σw²=Σd_i² (eqs 9.22–9.23). **CORRECT.** Illustrated recovery of public-info (σu²) and private/trade-info (λ²σv²) components: σw²=σu²+λ²σv². **CORRECT** (eq 9.23).
- λ²σv² absolute info measure; λ²σv²/σw² relative (≈R² of Δp on trades). **CORRECT** (lines 3949–3958).
- Pricing-error lower bound σs²=Σ_k C_k C_k', C_k=−Σ_{j>k}[θ_j]_1 (eq 9.24). **CORRECT.**
- Signing: q_t=Sign(p_t−m_t); signed order vars q_tV_t / avoid convex transforms (fat-tailed volume; Hasbrouck 1991a used q_tV_t²); event-time vs wall-clock; trade prices vs quote midpoints (midpoint lower short-run transient volatility / less bid-ask bounce, equal long-run volatility). **CORRECT** (sect. 9.7).
- Other structural models: Glosten-Harris (1988) m_t=m_{t−1}+u_t+q_t(λ0+λ1V_t), p_t=m_t+q_t(c0+c1V_t), rounding to ticks, nonlinear filtering (sect. 9.8.1, eq 9.26) — **CORRECT**; Madhavan-Richardson-Roomans (1997) q_t=ρq_{t−1}+v_t, VARMA (eq 9.6 / Exercise 9.2) — **CORRECT**.
- Price impact from returns+volume (sect. 9.9): Amivest/liquidity ratio L=(|Vol_t|/|r_t|); Amihud illiquidity ratio I=(|r_t|/|Vol_t|) — better proxy for λ (Hasbrouck 2005). **CORRECT** (lines 4317–4328).

### Findings
- No errors. Only optional enrichment: (a) the book notes causality in the illustrative model is one-way (trades→prices), but richer VARs admit reverse (e.g., momentum) effects; (b) σw² is invariant to choice of x_t (same value in univariate vs comprehensive multivariate) though the filtered estimate f_t and the info attributions do depend on x_t — an important caveat not in the extraction.

---

## CHAPTER 10 — Multiple Securities and Multiple Prices
Extraction section: §"9. Multiple Securities & Price Discovery (Ch 10)" (md lines 143–150).

### Verification per claim (hasbrouck.txt lines 4330–4911)
- Stacked single-security models OK when no cointegration; fail for multiple prices of same security / arbitrage-linked securities. **CORRECT.**
- Cointegration definition; bid/ask spread stationary; forward/spot parity; Engle-Granger (1987). **CORRECT** (sect. 10.2).
- Cointegrated VMA is **non-invertible** ⇒ no convergent VAR in first differences ⇒ need VECM. **CORRECT** (sect. 10.2.3; line 4595–4598).
- VECM (eq 10.13) Δp_t = φ1Δp_{t−1}+…+β(z_{t−1}−b)+ε_t; error z_{t−1}=A'p_{t−1} = vector of (price−first-price) differences (eq 10.14). **CORRECT.**
- b = vector of mean errors (e.g., long-run average spread for [ask,bid]). **CORRECT** (lines 4703–4706).
- Random-walk decomposition p_t = m_t·ι + s_t, m_t scalar common to all prices (eq 10.15); σw²=[θ(1)]₁[θ(1)]₁'; rows of θ(1) identical. **CORRECT.**
- Information share = relative contribution d_i²/σw² of price i's innovations to the common efficient price; report min & max over all causal permutations (Cholesky orderings). **CORRECT** (lines 4726–4744).
- Gonzalo-Granger (1995) permanent/transitory decomposition: factor weights β̃ = θ(1)₁/ι′θ(1)₁ (long-run VMA coefficients normalized to sum to unity); m_t*=β̃'p_t; s_t* has no long-run effect. **CORRECT** (lines 4758–4770). Extraction covers GG qualitatively and the Hasbrouck-info-share-vs-GG comparison.
- Pairs trading + caveats: data-snooping biases (understate test size when pair selected ex post) and structural breaks in long-run error means. **CORRECT** (sect. 10.3.4).
- VECM β coefficients = speed-of-adjustment / price leadership. **CORRECT** (lines 4652–4657).
- Wall-clock vs event time for multi-price; interval choice; quote/trade-price propagation ("last sale"); timestamp quality; polynomial distributed lags to curb parameter explosion. **CORRECT** (sect. 10.4).

### Findings
- No errors.
- Gaps (optional, worth flagging for the mapped Atlas page "price-discovery-and-information-shares"):
  1. The book's central *why-VECM* logic — cointegrated systems have no convergent differenced VAR (VMA non-invertible, θ*₀ singular) — is not captured; only the mechanical VECM form is given.
  2. The concrete identifying intuition of the two-venue example (crossing/primary market; one price contemporaneous-with-bounce, other one-period-stale) and that the common filtered efficient price is recovered from the VMA is omitted.
  3. The time-aggregation rationale: as Σ off-diagonal grows (coarse intervals / aggregation), info-share bounds widen and become more ordering-sensitive — hence shorter intervals give tighter bounds. The extraction lists wall-clock/interval selection but not this specific motivation.
  4. GG weights formula β̃=θ(1)₁/ι′θ(1)₁ is absent (qualitative only).

---

## Consolidated corrections (errors / imprecisions to fix)
1. **Ch7 (Kyle) expected profit — mis-rendered and conditional-vs-unconditional confusion.** Replace "Eπ = ½√(σu²Σ0)…" with the book's conditional form `Eπ = ((v−p0)²/2)·√(σu²/Σ0)` (eq 7.5). The "½√(σu²Σ0)" figure is the *unconditional* average and is not stated by Hasbrouck. Drivers: squared value divergence (v−p0)² and noise variance σu² (camouflage). Note for a *fixed* v profit declines in Σ0, so "increasing in value uncertainty" holds only unconditionally.
2. **Ch8 variance ratio — qualifier.** Add "M<N (shorter horizon M in numerator)" to the ">1 if microstructure inflates short-horizon variance" statement; V_{M,N}>1 typically holds for M<N and declines toward 1 as M→N.
3. (Optional editorial) Ch8: add the time-scaling result Var(m_t−m_{t−k})=kσw² / long-run variance ≈ kσw², which is the economic reason σw² is identified while spread components are not.

## Consolidated gaps (optional additions)
1. Ch6: buys and sells enter the daily likelihood only through the daily total.
2. Ch9: σw² invariant to the information set x_t vs f_t and the variance attribution both x_t-dependent; one-way trade→price causality in the illustrative model.
3. Ch10: non-invertibility/no-differenced-VAR rationale for VECM; two-venue crossing-market example intuition; shorter-interval→tighter-information-share-bounds; GG weights formula β̃=θ(1)₁/ι′θ(1)₁.

---

**Do NOT modify sources:** This document modifies nothing under /tmp/atlas_extract/. It is an advisory verification report.
