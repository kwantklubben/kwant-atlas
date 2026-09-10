---
title: "02 — Market Liquidity vs Funding Liquidity: Measurement & the Two Curves"
tags:
  - pillar-quantitative-risk
  - liquidity-risk-and-funding
  - market-liquidity
  - funding-liquidity
  - amihud
  - margin
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/01-from-zero-intuition|01 · From Zero]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]].

---

### 1. Intuition & Practical Objective

This page makes the market-vs-funding distinction *measurable*. The objective: given a position, produce two numbers — **how illiquid is the asset** (market side) and **how leveraged can I be against it** (funding side) — and see that they are driven by the same underlying quantity, **volatility**.

The three notions of liquidity (Foucault Ch 1 §0.4) put the vocabulary in place:

| Notion | Question it answers | Practical proxy |
|---|---|---|
| **Market liquidity** | How costly/fast to trade the asset? | spread, price impact, Amihud ratio, depth |
| **Funding liquidity** | How easily can I finance holding it? | haircut/margin, repo rollover, LCR/NSFR |
| **Monetary liquidity** | How much money exists in the system? | M1/M2, monetary base |

Market and funding liquidity are the pair that interact; monetary liquidity is the macro backdrop (this folder stays with the first two).

> **The essential bridge.** A lender sets the haircut $m$ from the *risk* of the collateral. A common rule is $m = z_\alpha\sigma$ — the collateral's value-at-risk. So **market volatility $\sigma$ is the common driver**: when $\sigma$ rises, the asset simultaneously becomes costlier to trade *and* harder to finance. The two "liquidities" are not independent factors; they are two faces of $\sigma$ (Brunnermeier–Pedersen 2009).

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Measuring market liquidity (Foucault Ch 2; Hasbrouck Ch 9).**

- **Quoted/relative spread** (Foucault eq. 2.1): $S=a-b$, $s=(a-b)/m$.
- **Effective half-spread** (eq. 2.3): $S_e = d\,(p-m)$, $d=\pm1$ the trade direction — the *actual* cost of a trade relative to the prevailing midquote, capturing price improvement.
- **Price impact / Kyle lambda** (eq. 2.8; Hasbrouck Ch 7):
$$\Delta m_t=\lambda q_t+\varepsilon_t,\qquad \frac1\lambda = \text{market depth}.$$
  Stoll (2000), cited in Foucault: $\lambda>0$ for 98% of stocks and significant for 63%; the price impact of a unit order is ~0.75% for the smallest NYSE/AMEX caps vs ~0.52% for the largest.
- **Amihud illiquidity ratio** (Amihud 2002; Foucault eq. 2.9):
$$I_t=\frac{|r_t|}{\text{Vol}_t}\quad\text{(price move per currency traded)},$$
  with the **Amivest liquidity ratio** its reciprocal $L_t=\text{Vol}_t/|r_t|$ (eq. 2.10).
- **Roll spread estimator** (Foucault eq. 2.18; Hasbrouck Ch 3): from the negative autocovariance induced by bid–ask bounce,
$$S_R=2\sqrt{-\operatorname{cov}(\Delta p_{t+1},\Delta p_t)}.$$
- **Resiliency**: the speed at which these costs decay after a trade — the third leg of Hasbrouck's depth/breadth/resiliency triad.

**2.2 Measuring funding liquidity (the haircut).**

A secured lender advances $P(1-m)$ against collateral worth $P$, so the borrower's equity is $mP$ and the constraint is $P\le N/m$. Setting the haircut from the collateral's VaR at confidence $\alpha$ over the *margin period of risk* (MPOR, the liquidation delay in the event of default) gives the risk-based rule
$$m=z_\alpha\,\sigma_{\text{MPOR}}=z_\alpha\,\sigma\sqrt{\Delta t_{\text{MPOR}}}.$$
This is why a vol spike *automatically* tightens funding: both $z_\alpha\sigma$ and the MPOR itself lengthen in stress.

**2.3 The return premium: market liquidity is priced.** Foucault eq. (9.6) shows the **gross expected return** required on an illiquid asset:
$$R\simeq r+\frac{s}{h},\qquad h=\text{expected holding period},$$
so an asset with spread $s$ must earn an extra $s/h$ per period; the Amihud–Mendelson clientele logic and the liquidity-adjusted CAPM of Acharya–Pedersen (2005) generalise this into four liquidity betas (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/06-advanced-extensions|06 · Advanced Extensions]]). Estimated cross-sectionally (Foucault Ch 9), $R_i=0.0036+0.00672\,\beta_i+0.211\,s_i$ — the spread term is economically large.

---

### 3. Computational Implementation — Amihud across caps and margin from vol

Two computations: the **asset-side** illiquidity ratio on three cap tiers, and the **funding-side** maximal leverage implied by a VaR-margin rule at rising volatility. Stdlib only.

```python
# --- market liquidity: Amihud illiquidity ratio I = |r| / Volume (Foucault eq. 2.9) ---
def amihud(r, vol_shares):
    return abs(r) / vol_shares

rows = [("MegaCap  (vol 20M sh)", 0.005, 20_000_000),
        ("MidCap   (vol  1M sh)", 0.010, 1_000_000),
        ("SmallCap (vol 50k sh)", 0.020, 50_000)]
for name, r, v in rows:
    I = amihud(r, v)
    print(f"{name}: I=|r|/Vol = {I:.3e}  (per $1 traded -> {I*1e9:.4f} bp/million)")

# --- funding liquidity: risk-based margin m = z_alpha * sigma -> max leverage 1/m ---
for sig in (0.01, 0.02, 0.04, 0.08):
    m = 2.326 * sig
    print(f"daily vol {sig*100:4.0f}%  -> VaR-margin m=z*sig = {m*100:5.2f}%  -> max leverage 1/m = {1/m:6.2f}x")
```
```
MegaCap  (vol 20M sh): I=|r|/Vol = 2.500e-10  (per $1 traded -> 0.2500 bp/million)
MidCap   (vol  1M sh): I=|r|/Vol = 1.000e-08  (per $1 traded -> 10.0000 bp/million)
SmallCap (vol 50k sh): I=|r|/Vol = 4.000e-07  (per $1 traded -> 400.0000 bp/million)
daily vol    1%  -> VaR-margin m=z*sig =  2.33%  -> max leverage 1/m =  42.99x
daily vol    2%  -> VaR-margin m=z*sig =  4.65%  -> max leverage 1/m =  21.50x
daily vol    4%  -> VaR-margin m=z*sig =  9.30%  -> max leverage 1/m =  10.75x
daily vol    8%  -> VaR-margin m=z*sig = 18.61%  -> max leverage 1/m =   5.37x
```

Two observations. **First**, the Amihud ratio separates cap tiers by *four orders of magnitude* — market liquidity is not a single number but an asset-specific attribute that varies violently across the universe. **Second**, because $m=z_\alpha\sigma$, an eightfold rise in volatility (1%→8%) cuts the permitted leverage **eightfold** (43×→5.4×). Funding liquidity is a strictly decreasing function of the same volatility that thins market liquidity. That is the mechanism the spiral builds on.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Roll's estimator assumes things that break.** Foucault Ch 2 shows the Roll spread is biased **downward** by unbalanced order flow (by factor $2\sqrt{\eta(1-\eta)}$), by autocorrelated orders (by $2(1-\delta)$; Choi–Salandro–Shastri estimate $\delta\approx0.7\Rightarrow$ underestimate by ~0.6), and by informed flow; and can be **swamped or sign-flipped** by time-varying expected returns. Using a single Roll number as "the" spread is a category error in a trending market.
2. **Amihud is a proxy, not a price.** $\mathrm{Vol}_t$ is shares (or value) *traded*, not *offered*. A market with a quoter but no trades reports infinite illiquidity; one with a huge trade reports false liquidity. Hasbrouck notes the Amihud ratio is a *better* proxy for $\lambda$ than the Amivest ratio, but still a proxy.
3. **Haircuts are not exogenous constants.** The $m=z_\alpha\sigma$ rule embeds a *positive feedback* (vol↑ ⇒ margin↑ ⇒ forced selling ⇒ vol↑) that a static margin assumption suppresses. Treating $m$ as fixed converts a spiral into a straight line.
4. **Funding liquidity is not the same as having assets.** A firm can hold liquid assets (high market liquidity) and still fail on funding if it cannot *roll* short-term borrowing — the 2007 ABCP/SIV failure mode (Brunnermeier 2009). Market liquidity of the collateral ≠ access to cash against it.
5. **Time-variation is the risk, not the level.** Liquidity is U-shaped intraday and crisis-widening; the premium $s/h$ is priced *because* $s$ and $h$ move together in bad states — the priced risk is liquidity's covariance with the market, not its average.

---

### 5. Canonical Literature & Study References

- **Foucault, Pagano & Röell** — *Market Liquidity* (2013), Ch 2 (spread measures, Lee–Ready, Roll + its four biases, implementation shortfall, resiliency) and Ch 9 (liquidity and asset prices, eq. 9.6/9.9). *Verified in corpus.*
- **Hasbrouck** — *Empirical Market Microstructure* (2007), Ch 1.2 (depth/breadth/resiliency), Ch 3 (Roll $S_R=2\sqrt{-\gamma_1}$), Ch 7 (Kyle $\lambda$, $1/\lambda$ = depth), Ch 9.9 (Amihud/Amivest). *Verified in corpus.*
- **Amihud, Y.** — *Illiquidity and Stock Returns*, *JFM* 5(1):31–56 (2002) — the $|r|/\text{Vol}$ ratio. **Roll, R.** — *A Simple Implicit Measure of the Effective Bid-Ask Spread*, *JF* 39(4) (1984).
- **Brunnermeier & Pedersen** (2009) — the market↔funding coupling; **Brunnermeier** (2009) — the 2007–08 case study.
- **BCBS** — LCR (2013, d238) and NSFR (2014, d295) — the regulatory funding-liquidity definitions.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03 · Liquidation Cost & L-VaR]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]]
- Siblings: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]
