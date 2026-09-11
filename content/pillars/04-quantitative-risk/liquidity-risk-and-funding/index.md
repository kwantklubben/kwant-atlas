---
title: "Liquidity Risk & Funding: Topic Hub & Formula Lookup"
tags:
  - pillar-quantitative-risk
  - liquidity-risk-and-funding
  - liquidity-risk
  - funding-liquidity
  - index-hub
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] and [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]. *(these are the folder-level prerequisites; page `01` states its own, smaller, entry requirements. The **[VaR & ES]** prerequisite is needed from page `03` onward, the **[Parametric/Historical/MC VaR]** one only where the pages price a liquidation horizon.)*

---

### 1. Intuition & Practical Objective

A firm can be *solvent* on paper — assets exceed liabilities at mark-to-market — and still die in 48 hours. Liquidity risk is the gap between **what a position is worth on the screen** and **what you actually receive when you must sell it now, with borrowed money that can be recalled**.

This folder separates the two things everyone conflates:

- **Market liquidity** — the cost and speed of *trading an asset*. Its price is the **bid–ask spread**, its depth is the **price impact** of an order, its recovery is **resiliency** (Hasbrouck Ch 1.2; Foucault Ch 2).
- **Funding liquidity** — the ease of *financing a position* with cash or collateralised borrowing (repo). Its price is the **haircut/margin**, its limit is the **margin constraint** $P\le N/m$.

They are two sides of one feedback loop. When prices fall, the same losses (i) widen spreads and thin depth (market liquidity ↓) and (ii) raise margins and haircuts (funding liquidity ↓). The two effects feed each other — the **liquidity spiral** of Brunnermeier & Pedersen (2009), more precisely a **margin spiral** (margin ↑ → forced sale → price ↓ → margin ↑) riding on a **loss spiral** (loss ↑ → equity ↓ → forced sale → loss ↑).

This folder is the *hub*: it (a) gives the **fast formula lookup** below, and (b) routes to six sub-pages that walk from raw intuition through the two-liquidities distinction, the liquidation-cost/L-VaR machinery, the margin recursion, the failure modes, and the systemic extensions.

> **The one-sentence essence.** "Standard risk measures assume you can liquidate at the mid in zero time; liquidity risk is the price you pay — in spread, in market impact, and in margin — for the fact that you cannot, and the danger is that these three costs *increase together* exactly when you need them."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $V$ position value; $S=a-b$ absolute quoted spread, $s=(a-b)/m$ relative spread (Foucault eq. 2.1); $\sigma_s$ spread volatility; $z_\alpha=\Phi^{-1}(\alpha)$; $Q$ shares to liquidate; $D$ market depth (shares to move price by 1 currency unit); $N$ equity; $m$ margin/haircut; $\lambda$ price-impact coefficient (Kyle/Foucault).

| Quantity | Formula | Verified check (§3) |
|---|---|---|
| **Quoted spread** (absolute / relative) | $S=a-b,\quad s=\dfrac{a-b}{m},\quad m=\dfrac{a+b}{2}$ | Foucault eq. (2.1) |
| **Price impact (linear)** | $\Delta p=\lambda q,\qquad 1/\lambda=D$ = depth | Foucault eq. (2.8); Hasbrouck Ch 7 |
| **Impact half-move (VWAP)** | $\text{LC}_{\text{impact}}=\dfrac{Q^2}{2D}=\dfrac{\lambda Q^2}{2}$ | $Q{=}10^5,D{=}2{\times}10^5\Rightarrow $\$25{,}000 |
| **Exogenous spread cost** | $\text{LC}_{\text{exog}}=\tfrac12 V\left(S+z_\alpha\sigma_S\right)$ | $V{=}10^7,S{=}20\text{bp}\Rightarrow$\$15{,}816 |
| **Liquidity-adjusted VaR** | $\mathrm{LVaR}_\alpha=\mathrm{VaR}_\alpha+\text{LC}_{\text{exog}}+\text{LC}_{\text{impact}}$ | $465{,}270+15{,}816+25{,}000= $\$506{,}085 |
| **Liquidation horizon** | $T_{\text{liq}}=\dfrac{Q}{\text{ADV}\cdot\alpha}$ ($\alpha$ = participation cap) | $10^5/(2{\times}10^6{\cdot}0.2)=0.25$ day |
| **Horizon scaling (i.i.d.)** | $\mathrm{VaR}_T=\mathrm{VaR}_1\sqrt{T}$ | $T{=}10\Rightarrow\times3.162$ |
| **Margin constraint** | $P\le \dfrac{N}{m}\quad\Longleftrightarrow\quad L=\dfrac{P}{N}\le\dfrac1m$ | $m{=}20\%\Rightarrow L\le5\times$ |
| **Amihud illiquidity** | $I=\dfrac{|r_t|}{\text{Vol}_t}$ | small cap $4\times10^{-7}$ vs mega $2.5\times10^{-10}$ |
| **Roll spread estimator** | $S_R=2\sqrt{-\operatorname{cov}(\Delta p_{t+1},\Delta p_t)}$ | Foucault eq. (2.18); Hasbrouck Ch 3 |
| **Gross-return premium** | $R\simeq r+\dfrac{s}{h}$ ($h$ = holding period) | Foucault eq. (9.6) |
| **Spiral amplification** | $S_{\text{total}}=\dfrac{S_0}{1-k},\quad k=L\kappa$ | $k{=}0.5\Rightarrow\times2$; diverges as $k\to1$ |

**The margin recursion (Brunnermeier–Pedersen 2009).** A leveraged trader with equity $N_t$, position $P_t$, and margin $m_t=N_t^{\text{req}}/P_t$ is forced to sell whenever the constraint binds. One stress round is:

$$
m_{t+1}=m_0+\beta\,\text{Vol}_t,\qquad P_t^{\max}=\frac{N_t}{m_{t+1}},\qquad \text{Sale}_t=\left(P_t-P_t^{\max}\right)^+,\qquad
N_{t+1}=N_t-\underbrace{P_t\,g\!\left(\frac{\text{Sale}_t}{\text{ADV}}\right)}_{\text{fire-sale impact loss}}.
$$

Two multiplicative forces hit the constraint at once: $N_t$ falls in the numerator (loss spiral) *and* $m_{t+1}$ rises in the denominator (margin spiral). Neither alone closes the firm; together they do.

**Regulatory definitions (BCBS).** Funding-liquidity risk is regulated in two ratios:
$$
\text{LCR}=\frac{\text{HQLA}}{\text{Net cash outflows over 30 days}}\ge100\%,\qquad
\text{NSFR}=\frac{\text{Available stable funding}}{\text{Required stable funding}}\ge100\%.
$$
LCR is a 30-day survival test (BCBS 2013, d238); NSFR is a one-year structural funding test (BCBS 2014, d295). Both are *funding*-liquidity rules — they do not constrain the market liquidity of the assets, which is the other half of the spiral.

---

### 3. Computational Implementation — the formula engine

Standard library only. This reproduces every verified number above (all six experiments were **executed and reproduced exactly**; the full runs live on the sub-pages).

```python
import math

def Phi(x):  return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))
def lvar(V, sigma, alpha, S, sigma_S, Q, D):
    """Liquidity-adjusted VaR = market VaR + exogenous spread cost + impact cost."""
    z  = 2.3263478740408408                     # Phi^-1(0.99)
    VaR = z*sigma*V
    LC  = 0.5*V*(S + z*sigma_S)                 # exogenous (bid-ask) liquidation cost
    imp = Q*Q/(2.0*D)                           # endogenous market-impact cost (1/lambda=D)
    return VaR, LC, imp, VaR + LC + imp

V, sigma, S, sigS, Q, D = 1e7, 0.02, 0.0020, 0.0005, 1e5, 2e5
VaR, LC, imp, LV = lvar(V, sigma, 0.99, S, sigS, Q, D)
print(f"1-day 99% VaR        = ${VaR:,.0f}")
print(f"exogenous spread LC  = ${LC:,.0f}  ({LC/V*1e4:.2f} bp)")
print(f"market-impact LC     = ${imp:,.0f}  ({imp/V*1e4:.2f} bp)")
print(f"L-VaR (all-in)       = ${LV:,.0f}   (+{LV/VaR*100-100:.2f}% over VaR)")
```
```
1-day 99% VaR        = $465,270
exogenous spread LC  = $15,816  (15.82 bp)
market-impact LC     = $25,000  (25.00 bp)
L-VaR (all-in)       = $506,085   (+8.77% over VaR)
```

> **The point of the check.** The two liquidation costs together add \$40{,}816 — $8.77\%$ — to a VaR that a standard risk engine would report as the whole story. On an illiquid book the impact term dominates and can exceed the market-risk term outright.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Ignoring the liquidation horizon.** VaR assumes a zero-time exit at the mid; real liquidation takes $T_{\text{liq}}=Q/(\text{ADV}\cdot\alpha)$ days, during which the market keeps moving *against* you. The two errors compound: you scale risk by $\sqrt T$ but the cost of the forced sale by $T$ (§5).
2. **Fire-sale externality.** A fund's private liquidation cost uses *its own* order size; when a crowd liquidates the same asset, each bears the *others'* impact. Private cost understates social cost — the exact mechanism behind crowded-unwind contagion and the reason liquidity is a system-wide, not firm-level, risk (§5).
3. **Funding vs market liquidity interaction.** Margin depends on *volatility*, and volatility is *caused by* forced selling. Treating the haircut as an exogenous constant breaks precisely when it matters — in the crisis (§4).

---

### 5. Canonical Literature & Study References

- **Brunnermeier, Markus K. & Pedersen, Lasse Heje** — *Market Liquidity and Funding Liquidity*, *Review of Financial Studies* **22**(6):2201–2238 (2009). The margin/loss-spiral model — the theory behind the whole folder. **The primary source.** (In corpus as `58_Brunnermeier_2009_market_liquidity_and_funding_liquidity.pdf`.)
- **Brunnermeier, Markus K.** — *Deciphering the Liquidity and Credit Crunch 2007–2008*, *Journal of Economic Perspectives* **23**(1):77–100 (2009). The narrative-and-mechanism account; the accessible case study of the spirals in action.
- **Foucault, Thierry, Pagano, Marco & Röell, Ailsa** — *Market Liquidity: Theory, Evidence and Policy* (Oxford, 2013). Ch 1 (three dimensions of liquidity: market, funding, monetary), Ch 2 (spread/impact measurement, Roll, Amihud, implementation shortfall), Ch 9 (liquidity and asset prices). *Verified per chapter in the corpus.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (Oxford, 2007). Ch 1 (liquidity = depth, breadth, resiliency), Ch 3 (Roll model, spread $2c$), Ch 7 (Kyle $\lambda$, depth $1/\lambda$), Ch 9 (Amihud/Amivest ratios). *Verified per chapter in the corpus.*
- **Hull, John C.** — *Risk Management and Financial Institutions* (Wiley), liquidity-risk chapter (liquidity trading risk, L-VaR, the Basel LCR/NSFR). *Risk-engineering companion to this folder.*
- **Amihud, Yakov** — *Illiquidity and Stock Returns: Cross-Section and Time-Series Effects*, *J. Financial Markets* **5**(1):31–56 (2002). The $|r|/\text{Vol}$ illiquidity ratio — the standard empirical proxy. (In corpus.)
- **Acharya, Viral & Pedersen, Lasse Heje** — *Asset Pricing with Liquidity Risk*, *J. Financial Economics* **77**(2):375–410 (2005). Liquidity as a priced factor — the return-premium bridge (§6). (In corpus.) Also **Pastor & Stambaugh (2003)** *Liquidity Risk and Expected Stock Returns* (Pillar 6 refs).
- **[REG]** **BCBS** — *Basel III: The Liquidity Coverage Ratio and Liquidity Risk Monitoring Tools* (2013, BIS d238) and *Basel III: The Net Stable Funding Ratio* (2014, BIS d295). The regulatory definitions of funding-liquidity risk.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
- Sub-pages (in-folder): 01 From Zero · 02 Market vs Funding · 03 Liquidation Cost & L-VaR · 04 Margin & Funding Spirals · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover Constraints]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/01-from-zero-intuition|01 · From Zero]] — no prior quant-finance needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/02-market-vs-funding-liquidity|02 · Market vs Funding Liquidity]] → [[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03 · Liquidation Cost & L-VaR]] → [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]].
- **Robustness (practitioner/graduate):** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/04-quantitative-risk/liquidity-risk-and-funding/06-advanced-extensions|06 · Advanced Extensions (Spirals & Systemic Risk)]].
