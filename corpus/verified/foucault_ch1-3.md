# Per-Chapter Verification — Foucault, Pagano & Röell, *Market Liquidity* (2013), Ch 1–3

**Source text:** `/tmp/atlas_extract/foucault.txt` (Oxford Scholarship Online full-text)
**Extraction verified:** `/tmp/atlas_extract/market_microstructure.md` (Part 2, sections 1–2, pages 197–232)
**Method:** Text-based line-by-line cross-check of every formula and claim against the source.
**Verdict:** **PASS — high fidelity.** All key formulas and concepts for Ch 1–3 are present and correct. Only minor notation / framing notes flagged below (no substantive errors found).

> **Chapter-title mapping note.** The task labels the three chapters *Introduction; Trading and Liquidity; Economics of Adverse Selection*. The book's actual titles are: **Ch 1 Introduction** (this is the intro chapter, §§0.1–0.4); **Ch 2 "Measuring Liquidity"** (§§2.1–2.4 — this is the "Trading and Liquidity" content); **Ch 3 "Order Flow, Liquidity, and Securities Price Dynamics"** (§§3.1–3.6 — this is the "Economics of Adverse Selection" content). The extraction's Part-2 heading "(Intro, Ch 2)" / "(Ch 3)" maps correctly to these.

---

## Chapter 1 — Introduction (source lines 291–706)

Verified concepts:
- Two key concepts of market microstructure: **market liquidity** and **price discovery** (l. 300–303, 365–366). ✓
- **Liquidity** = degree to which an order can be executed within a short time frame at a price close to the security's consensus value; illiquid markets have ask well above bid; the **bid-ask spread is a common measure of illiquidity** (l. 368–376). ✓
- **Price discovery** = speed and accuracy with which transaction prices incorporate information available to market participants (l. 409–410). ✓
- **Tension between price discovery and liquidity** — info arriving via trading pressure hurts liquidity (Morton-Thiokol / Challenger episode, NYSE trading halt) (l. 430–438). ✓
- **Three dimensions of liquidity** (§0.4, l. 593–694): **market liquidity** (0.4.1), **funding liquidity** (0.4.2, banks' cash/credit + maturity transformation), **monetary liquidity** (0.4.3, money supply M1/M2/M3, monetary base). ✓
- **Market ↔ funding liquidity feedback → liquidity spirals** (Brunnermeier-Pedersen 2009) (l. 657–660). ✓
- Puzzles: liquidity varies over time (U-shaped intraday spreads; crisis widening), block trades move prices then reverse, concentration of trading, hidden orders/dark pools vs sunshine trading, deviations from no-arbitrage (Siamese twins) (l. 490–591). ✓
- Illiquidity affects equilibrium asset prices → link to asset pricing (Ch 9) and corporate finance (Ch 10) (l. 463–488). ✓

**Extraction coverage:** Present (three notions of liquidity + spiral in Part 2 §1 "Key concepts"). No error.

---

## Chapter 2 — "Measuring Liquidity" (source lines 2003–3045)

### Verified spread measures (all formulas match source):
- **Quoted spread** `S = a − b`; relative `s = (a − b)/m`, `m = (a + b)/2` — eq (2.1) (l. 2176–2184). ✓
- **Weighted-average (depth-adjusted) spread** `S(q) = ā(q) − b̄(q)`, relative `s(q) = (ā(q) − b̄(q))/m` — eq (2.2) (l. 2196–2203); increases with trade size q, deeper market ⇒ milder increase. ✓
- **Effective half-spread** `Se ≡ d(p − m)` (absolute, eq 2.3, l. 2232) and relative `Se ≡ d·(p−m)/m` (eq 2.4, l. 2239); `d` = +1/−1 order direction, `m` = midquote just before transaction; retrospective; captures price improvement (l. 2251–2256). ✓
- **Lee-Ready (1991) algorithm** for signing trades: buy if price closer to ask, sell if closer to bid; midpoint resolved by tick rule (uptick= buy) (Box 2.1, l. 2317–2321). Accuracy **~85%**, misclassifies midpoints/small trades/large-caps (Odders-White 2000) (l. 2333–2336). ✓
- **Realized half-spread** `Sr = d_t(p_t − m_{t+Δ}) = d_t(p_t − m_t) − d_t(m_{t+Δ} − m_t)` — eq (2.5) (l. 2370); measures liquidity-supplier profit on unwind at t+Δ. ✓
- `E(Sr) = E(Se) − E(d_t(m_{t+Δ} − m_t))` — eq (2.6) (l. 2379). ✓
- SEC Rule 605 **Dash-5** monthly reports of execution quality (effective/realized spreads, speed) since 2000 (l. 2399–2403). ✓

### Other implicit-cost measures:
- **VWAP** = `Σ w_t p_t`, `w_t = |q_t| / Σ|q_t|` (eq 2.7, l. 2437–2440); flaws: depends on own order, can be gamed by slow trickling (l. 2451–2465). ✓
- **Price impact** `Δm_t = λ q_t + ε_t`, `q_t` = order imbalance (eq 2.8, l. 2477); `1/λ` = **market depth** (l. 2490). Stoll (2000): λ positive for 98% of stocks, significant for 63%; 0.75% impact for lowest-cap NYSE/AMEX vs 0.52% for highest-cap (l. 2501–2504). ✓
- **Amihud (2002) illiquidity ratio** `I_t = |r_t| / Vol_t` (eq 2.9, l. 2525). ✓
- **Amivest liquidity ratio** `L_t = Vol_t / |r_t|` (eq 2.10, l. 2532); low value = illiquid. ✓
- **Non-trading measures:** fraction of no-trade days (= zero-return days) as illiquidity proxy (Lesmond-Ogden-Trzcinka 1999; Bekaert-Harvey-Lundblad 2007) (l. 2562–2565); requires only daily-returns series; drawback: overestimates illiquidity when a liquid market trades without price change (l. 2572–2578). ✓

### Roll's measure (eq 2.11–2.18, l. 2607–2705) — verified exactly:
- Midquote random walk `m_t = m_{t−1} + ε_t` (eq 2.11). ✓
- `a_t = m_t + S/2`, `b_t = m_t − S/2` (eq 2.12–2.13). ✓
- `p_t = m_t + (S/2)d_t` (eq 2.14). ✓
- `Δp_t = (S/2)(d_t − d_{t−1}) + ε_t` (eq 2.15). ✓
- **`cov(p_{t+1}−p_t, p_t−p_{t−1}) = −S²/4`** (eq 2.17, l. 2689). ✓
- **Roll estimator `S_R = 2√(−cov(Δp_{t+1}, Δp_t))`** (eq 2.18, l. 2703). ✓
- Assumptions: (a) balanced flow `Pr(d_t=1)=½`; (b) no autocorrelation in orders; (c) orders carry no news (uncorrelated with ε); (d) zero expected return (l. 2658–2666). ✓

### Roll's biases — all four, verified with the *underestimation factors* (matching extraction):
- **(a) Unbalanced flow** `Pr(d_t=1)=η`: `cov = −η(1−η)S²` (eq 2.19); unbiased `S_a = √(−cov/(η(1−η)))` (eq 2.20); **`S_R = 2√(η(1−η))·S_a` → underestimates by factor `2√(η(1−η))`** (eq 2.20, l. 2765–2771). ✓
- **(b) Autocorrelated orders** `Pr(d_{t+1}=d_t)=δ`: `cov = −(1−δ)²S²` (eq 2.21); unbiased `S_b = (1/(1−δ))√(−cov)` (eq 2.22); **underestimates by `2(1−δ)`**; Choi-Salandro-Shastri estimate δ≈0.7 ⇒ underestimate by factor 0.6 (l. 2792–2806). ✓
- **(c) Informed flow** (ε and d positively correlated): attenuates bounce → **underestimates** (l. 2816–2820). ✓
- **(d) Time-varying expected returns** `m_t = m_{t−1} + r̄_t + ε_t` (eq 2.23): `cov(Δp_{t+1},Δp_t) = cov(r̄_{t+1},r̄_t) − S²/4` (eq 2.25); positive `cov(r̄_{t+1},r̄_t)` can swamp bounce → positive autocov → impute 0 (Harris 1990) (l. 2882–2884); George-Kaul-Nimalendran (1991) correction via time-varying `r̄_t` (l. 2871–2873). ✓
- **Roll works better at high frequency** (shorter intervals ⇒ bounce dominates) (l. 2885–2886). ✓

### Implementation shortfall (Perold 1988) (eq 2.27–2.29, l. 2933–2955) — verified exactly:
- Paper return `R_p = q(m_t − m_0)`; actual `R_a = κq(m_t − p̄)` (κ = fraction filled).
- **`IS ≡ q(m_t − m_0) − κq(m_t − p̄) = κq(p̄ − m_0) + (1−κ)q(m_t − m_0)`** = execution cost + opportunity cost. ✓
- Delay split: `κq(p̄ − m_0) = κq(p̄ − m_τ) + κq(m_τ − m_0)` (eq 2.30). ✓
- Numeric example: 3000×(101−100) + 7000×(103−100) = 24,000 (2.4% of paper value). ✓
- **Resiliency** = speed at which liquidity returns after a trade (l. 3032–3036). ✓

**Extraction coverage:** All formulas, both bias underestimation factors (unbalanced flow `2√(η(1−η))`, autocorrelation `2(1−δ)`), informed-flow and time-varying-drift biases, Amihud/Amivest, non-trading measures, and implementation shortfall are present and numerically correct. ✓

---

## Chapter 3 — "Order Flow, Liquidity, and Securities Price Dynamics" (source lines 3499–5830)

### Framework:
- Three cost types for liquidity suppliers: **(i) adverse-selection, (ii) order-processing (+rents), (iii) inventory-holding** (l. 3618–3622); each has a distinct price-dynamics signature (l. 3633–3638). ✓
- **EMH benchmark:** `p_t = μ_t ≡ E(v|Ω_t)` (eq 3.1); `E[μ_{t+1}|Ω_t] = μ_t` (eq 3.2); `p_t = E(p_{t+1}|Ω_t)` martingale (eq 3.3); `Δp_{t+1} = ε_{t+1}` (eq 3.4). Violations: intraday volatility too high (French-Roll 1986; Roll 1988), positive spreads, negative serial correlation (AGF example: −0.45) (l. 3760–3765). ✓

### Glosten-Milgrom model (Bagehot/Treynor adverse selection) — verified exactly:
- Setting: informed trader arrives with prob **π**, liquidity trader with 1−π (buys/sells each with prob ½); value binary `{v_H, v_L}`; `θ_t = Pr(v_H)`; `μ_t = θ_t v_H + (1−θ_t)v_L` (eq 3.6). ✓
- Quotes: `a_t = E(v|Ω_{t−1}, d_t=+1)`, `b_t = E(v|Ω_{t−1}, d_t=−1)` (eq 3.5/3.7). ✓
- **First-trade spread (θ₀ = ½): `S₁ ≡ a₁ − b₁ = π(v_H − v_L)`** (eq 3.12, l. 3999); adverse-selection cost ↑ with π and with (v_H − v_L) (l. 4004–4016). ✓
- **General spread** (eq 3.13–3.15): `a_t = μ_{t−1} + s_a^t`, `b_t = μ_{t−1} − s_b^t` with
  `s_a^t = πθ_{t−1}(1−θ_{t−1})/[πθ_{t−1} + (1−π)½]·(v_H−v_L)`,
  `s_b^t = πθ_{t−1}(1−θ_{t−1})/[π(1−θ_{t−1}) + (1−π)½]·(v_H−v_L)`,
  `S_t = a_t − b_t = s_a^t + s_b^t`. ✓ (Extraction reproduces this bracket form exactly.)
- **Third determinant: beliefs θ_{t−1}.** Spread greatest at θ=0.5, →0 as θ→1 or 0; widens before announcements/openings (l. 4067–4078). ✓
- **Bayes belief updates** (eq 3.16–3.17): `θ_t⁺ = [(1+π)/2 / (πθ_{t−1} + (1−π)/2)]·θ_{t−1}`; `θ_t⁻ = [(1−π)/2 / (π(1−θ_{t−1}) + (1−π)/2)]·θ_{t−1}`. ✓ (Extraction's ratio form is algebraically identical.)
- **Price discovery:** `p_t = μ_t = θ_t v_H + (1−θ_t)v_L` (eq 3.22); converges to v_H iff **π>0**, speed ↑ with π; **semi-strong EMH holds**; **strong form if π=1** (l. 4249–4278, 4287–4291). ✓
- **Liquidity vs informational-efficiency tradeoff** (l. 4361–4368). ✓
- `μ_t = μ_{t−1} + s(d_t)d_t` (eq 3.24); `p_t − p_{t−1} = s(d_t)d_t` (eq 3.27); **`var(Δp_t) = var(s(d_t)d_t)`** — trading is a source of volatility, correlated with spread (eq 3.28, l. 4466–4471). ✓
- Market-failure possibility when uninformed trading is price-sensitive (exercise 6, l. 4085–4088). ✓

### Order-processing costs — verified exactly:
- `a_t = μ_{t−1} + γ + s_a^t` (eq 3.29); `b_t = μ_{t−1} − γ − s_b^t` (eq 3.30). ✓
- **Spread `S_t = 2γ + s_a^t + s_b^t`** (eq 3.31). ✓
- `p_t = μ_{t−1} + (s(d_t)+γ)d_t` (eq 3.32) ⇒ **`p_t = μ_t + γd_t`** (eq 3.33); `|p_t − μ_t| = γ` transient deviation. ✓
- **ST impact `= s_a^t + γ`** (eq 3.34); **LT impact `= s_a^t`** (eq 3.36); **`ST − LT = γ`** (eq 3.37) → negative serial correlation / reversals. ✓
- **Dealer rents (Box 3.1):** γ = γ_c + γ_r (operating cost + non-competitive rent); **cannot separate processing cost from rents using price dynamics alone** (l. 4624–4640). ✓

### Inventory-risk models (Stoll 1978) — verified exactly:
- **Mean-variance** `U = E_t(w_{t+1}) − (ρ/2)·var_t(w_{t+1})` (eq 3.43); inverse supply `p_t = μ_t + ρσ_ε²(y_t − z_t)` (eq 3.44); equilibrium `p_t = m_t + ρσ_ε²d_t` (midquote `m_t = μ_t − ρσ_ε² z_t`); **spread `S_t = 2ρσ_ε²`** (eq 3.46). ✓
- **Mean-standard-deviation** `U = E_t(w_{t+1}) − ρ·sd(w_{t+1})` (eq 3.47); price interval `p_t ∈ [μ_t − ρσ_ε, μ_t + ρσ_ε]` (eq 3.48); **spread `S_t = 2ρσ_ε`** (eq 3.50). ✓
- **Multi-period:** `p_t = μ_t − ρσ_ε z_{t+1}` (eq 3.56); **midquote `m_t = μ_t − ρσ_ε z_t`** (eq 3.57); `a_t = μ_t − ρσ_ε z_t + ρσ_ε` (eq 3.58), `b_t = μ_t − ρσ_ε z_t − ρσ_ε` (eq 3.59); spread `S_t = 2ρσ_ε`. ✓
- `m_t − m_{t−1} = ρσ_ε d_{t−1} + ε_t` (eq 3.60); **ST impact `= p_t − m_t = ρσ_ε`** (eq 3.61). ✓
- **Price pressure** = inventory holding cost; inventories mean-revert (`|z_{t+1}| = |z_t| − 1`); impact **transient, reverses gradually** (vs instantly for order-processing) (l. 5104–5136). ✓
- **Hendershott-Menkveld (2010):** price pressure per $1000 of inventory = **1.01 bp (small caps)** vs **0.02 bp (large caps)**; inventory contributes **0.17% (large) – 1.20% (small)** of daily volatility (l. 5058–5059, 5151–5152). ✓
- Long-position dealers more likely to execute buy orders (Reiss-Werner 1998; Hansch-Naik-Viswanathan 1998) (l. 5063–5065). ✓

### Section 3.6 "The Full Picture" — verified:
- Adverse selection ⇒ **permanent** impact; order-processing ⇒ **instant reversal**; inventory ⇒ **slow/gradual reversal** (Fig 3.8–3.9, l. 5226–5252). ✓

**Extraction coverage:** All GM formulas (including full bracket spread form, S₁=π(v_H−v_L), belief updates, price discovery, π=1 strong-form), order-processing (2γ + s_a + s_b, ST−LT=γ, rents), and inventory (2ρσ_ε², 2ρσ_ε, p_t/m_t markdown, Hendershott-Menkveld numbers) are present and correct. ✓

---

## Corrections & flags (none substantive)

1. **Notation only (GM, Ch 3):** extraction writes the first-trade special case as "δ=½"; the book's notation is **θ₀ = ½** (the prior belief of a high value). The math is correct; δ is not a parameter of the GM model (δ is used in Roll/Ch-2 autocorrelation). Suggest relabeling to `θ₀=½` for consistency and to avoid collision with the Roll autocorrelation parameter.
2. **Chapter-title naming:** task's "Trading and Liquidity" = book Ch 2 *"Measuring Liquidity"*; task's "Economics of Adverse Selection" = book Ch 3 *"Order Flow, Liquidity, and Securities Price Dynamics"* (which covers adverse selection + order-processing + inventory). The extraction's chapter citations (Intro/Ch 2, Ch 3) are correct.
3. **Minor gap (Ch 1):** extraction condenses the Intro; the explicit **tension between price discovery and liquidity** (Challenger/Morton-Thiokol) and the **explicit-cost vs implicit-cost split** (commissions/taxes/fees vs gap-to-midquote) are described in Ch 2 but the explicit-vs-implicit distinction could be made more prominent in the intro/chapter-2 "Key concepts". Present in source (l. 2056–2063), adequately covered.
4. **Minor omission (Ch 2):** the extraction does not spell out the *VWAP gaming / order-dependence* caveat in its main body, though it's covered in the Hasbrouck part; it is in the source (l. 2451–2465). Optional enrichment.
5. **No numeric errors found** in any extracted formula (Roll covariance −S²/4, Roll estimator 2√(−cov), both bias factors, GM spread, ST/LT impact, inventory spreads, IS decomposition, Amihud/Amivest).

**Recommended fix applied to extraction? No** — sources are read-only for this task. Recommendation only.
