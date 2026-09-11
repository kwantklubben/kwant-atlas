---
title: "Liquidity Risk & Asset Pricing: Topic Hub & Formula Lookup"
tags:
  - pillar-market-making
  - liquidity-risk-and-asset-pricing
  - liquidity-premium
  - illiquidity
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] and [[foundations/statistics-and-inference/index|Statistics & Inference]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Two assets with *identical future cash flows* need not trade at the same price. If one can be sold instantly at the mid with no cost and the other costs 30 basis points every time you trade it, you will only hold the illiquid one if it *pays you to*. That compensation — the higher required expected return on less-liquid assets — is the **liquidity premium**, and the machinery for measuring it and understanding why it varies is this folder.

This is the **asset-pricing view of liquidity** — liquidity as a determinant of *prices, expected returns, and risk premia*. It is deliberately distinct from Pillar 4's **funding view** ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]), which asks *can I get the cash to hold a position?* Here the questions are:

1. **How do we measure illiquidity?** (Amihud ILLIQ, bid-ask spread, Roll, turnover)
2. **Is the *level* of illiquidity priced?** (cross-section: more illiquid ⇒ higher expected return)
3. **Is the *risk* of illiquidity priced?** (covariance of a stock's return with *aggregate* liquidity)
4. **Why does liquidity dry up exactly when you need it?** (commonality, crises, flight to quality)

This folder is the *hub*: it (a) gives the **fast formula lookup** below, and (b) routes to six sub-pages that walk from raw intuition through the measures, the priced-factor machinery, the crisis dynamics, the failure modes, and the bond-market extensions.

> **The one-sentence essence.** "Illiquidity is a cost that appears in prices twice: once as a *level* — more illiquid assets earn a higher expected return (Amihud 2002) — and once as a *risk* — assets that fall when aggregate liquidity falls earn a higher expected return too (Pástor–Stambaugh 2003; Acharya–Pedersen 2005)."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $r$ daily/period return; $\text{VOLD}$ dollar volume; $s$ relative bid-ask spread; $h$ holding period; $\hat{\gamma}_{i,t}$ per-stock price-impact coefficient; $L_t$ aggregate liquidity innovation; $c^i$ relative illiquidity cost of asset $i$; $r^M$, $c^M$ market return and market illiquidity.

| Quantity | Formula | Source / Verified check |
|---|---|---|
| **Amihud ILLIQ** | $\text{ILLIQ}_{iy}=\dfrac{1}{D_{iy}}\sum_{t=1}^{D_{iy}}\dfrac{\lvert R_{iyt}\rvert}{\text{VOLD}_{iyt}}$ | Amihud (2002) eq. (1); §3 |
| **Roll spread** | $S_R=2\sqrt{-\operatorname{cov}(\Delta p_{t+1},\Delta p_t)}$ | Roll (1984); Hasbrouck Ch 3 |
| **Amihud–Mendelson premium** | $R\simeq r+\dfrac{s}{h}$ | Foucault eq. (9.6); §3 |
| **PS liquidity innovation** | $L_t=\dfrac{1}{100}\,\hat{u}_t$ from $\Delta\hat\gamma_t=a+b\,\Delta\hat\gamma_{t-1}+c\big(\tfrac{m}{m_1}\big)_{t-1}\hat\gamma_{t-1}+u_t$ | Pástor–Stambaugh (2003) eqs. (7)–(8) |
| **PS liquidity beta** | $\beta_i^L=\dfrac{\operatorname{cov}(r_{i},L)}{\operatorname{var}(L)}$ | Pástor–Stambaugh (2003) §III |
| **AP commonality beta** | $\beta_1=\dfrac{\operatorname{cov}(c^i,c^M)}{\operatorname{var}(r^M-c^M)}$ | Acharya–Pedersen (2005) eq. (8) — **positive** premium |
| **AP return-vs-liquidity beta** | $\beta_2=\dfrac{\operatorname{cov}(r^i,c^M)}{\operatorname{var}(r^M-c^M)}$ | Acharya–Pedersen (2005) eq. (8) — **negative** premium (this is AP's $\beta_3$; we number the three liquidity betas $1,2,3$) |
| **AP down-market beta** | $\beta_3=\dfrac{\operatorname{cov}(c^i,r^M)}{\operatorname{var}(r^M-c^M)}$ | Acharya–Pedersen (2005) eq. (8) — **negative** premium |
| **Bao bond illiquidity** | $\gamma=-\operatorname{cov}(\Delta\ln P_{t+1},\Delta\ln P_t)$ | Bao, Pan & Wang (2011) — Roll-type |

**The Acharya–Pedersen liquidity-adjusted CAPM.** Required excess return = expected illiquidity cost + four covariance terms (each $\times\lambda_t$, the market risk premium):

$$
E_t(r^i_{t+1}) = r^f + E_t(c^i_{t+1}) + \lambda_t\left[\frac{\operatorname{cov}_t(r^i,r^M)}{\operatorname{var}(r^M-c^M)}+\frac{\operatorname{cov}_t(c^i,c^M)}{\operatorname{var}(r^M-c^M)}-\frac{\operatorname{cov}_t(r^i,c^M)}{\operatorname{var}(r^M-c^M)}-\frac{\operatorname{cov}_t(c^i,r^M)}{\operatorname{var}(r^M-c^M)}\right].
$$

> **Sign convention (the subtle part).** An asset whose *illiquidity* co-moves with *market illiquidity* ($\beta_1>0$) is bad to hold → requires a **higher** return. An asset whose *return* is high when the market is illiquid ($\beta_2>0$), or that stays *liquid* when the market falls ($\beta_3>0$), is good to hold → commands a **lower** return.

---

### 3. Computational Implementation — the measure engine

The core daily measure, computed and print-verified (full pipeline in [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]]):

```python
def amihud_illiq(returns, dollar_vol):
    """Amihud (2002) ILLIQ = mean(|daily return| / daily dollar volume)."""
    vals = [abs(r)/v for r, v in zip(returns, dollar_vol) if v > 0]
    return sum(vals)/len(vals) if vals else float('nan')

# small cap: big moves on tiny volume  |  mega cap: small moves on huge volume
small_ret, small_vol = [0.008, -0.012, 0.005], [3e6, 2.5e6, 3.2e6]
mega_ret,  mega_vol  = [0.001, -0.001, 0.002], [8e8, 7.5e8, 8.1e8]
print(f"Amihud ILLIQ small-cap = {amihud_illiq(small_ret, small_vol):.4e}")
print(f"Amihud ILLIQ mega-cap  = {amihud_illiq(mega_ret, mega_vol):.4e}")
```
```
Amihud ILLIQ small-cap = 3.0097e-09
Amihud ILLIQ mega-cap  = 1.6842e-12
```
The ratio is ~**1,800×**: an absolute price move of the same percentage costs thousands of times more to "move the price" per dollar in the small cap. That gap is what the cross-section of expected returns compensates.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — full analysis in [[pillars/06-market-making/liquidity-risk-and-asset-pricing/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Measurement error** — every illiquidity proxy measures the *cost of trading*, not the true price-impact function; ILLIQ is undefined on zero-volume days and noisy for infrequently traded names.
2. **Roll-estimator collapse** — the autocovariance-based spread is real only when returns have the *negative* autocorrelation the bid-ask bounce generates; positive autocovariance clamps the estimate to zero ("infinitely liquid" — wrong).
3. **Commonality & the liquidity spiral** — illiquidity co-moves across assets and spikes in down markets, so a beta estimated in calm times understates the risk that shows up in a crisis (the *level* of risk is not the *risk* of the level).

---

### 5. Canonical Literature & Study References

- **Amihud (2002).** *Illiquidity and stock returns: cross-section and time-series effects.* Journal of Financial Markets 5(1), 31–56. The ILLIQ measure and the two findings (cross-section premium, time-series market-premium response). *The anchor paper.*
- **Pástor & Stambaugh (2003).** *Liquidity risk and expected stock returns.* JPE 111(3), 642–685. Aggregate liquidity measure, innovations, and the priced liquidity beta (7.5% annual long-short spread).
- **Acharya & Pedersen (2005).** *Asset pricing with liquidity risk.* JFE 77(2), 375–410. The liquidity-adjusted CAPM and its three liquidity-risk betas.
- **Bao, Pan & Wang (2011).** *The illiquidity of corporate bonds.* Journal of Finance 66(3), 911–946. Roll-type $\gamma$ applied to bonds; large, common, crisis-spiking illiquidity.
- **Amihud, Mendelson & Pedersen (2013).** *Market Liquidity: Asset Pricing, Risk, and Crises.* Cambridge University Press. The founders' monograph — the folder capstone.
- **Hasbrouck.** *Market Microstructure: Foundations*, Ch 1–5, 11–15. Measurement (Roll, ILLIQ, effective spreads) and the price-impact view.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- **Funding counterpart (Pillar 4):** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] — the same two liquidities, but the funding/L-VaR and margin-spiral view.
- Sibling microstructure: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth (Kyle)]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & Roll Model]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]]
- Sub-pages (in-folder): 01 From Zero · 02 Illiquidity Measures · 03 Liquidity as a Priced Factor · 04 Liquidity Risk & Crises · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/liquidity-risk-and-asset-pricing/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Measures + code (undergrad/job-seeking):** [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]] → [[pillars/06-market-making/liquidity-risk-and-asset-pricing/03-liquidity-as-a-priced-factor|03 · Liquidity as a Priced Factor]].
- **Risk & robustness (practitioner/graduate):** [[pillars/06-market-making/liquidity-risk-and-asset-pricing/04-liquidity-risk-and-crises|04 · Liquidity Risk & Crises]] → [[pillars/06-market-making/liquidity-risk-and-asset-pricing/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/06-market-making/liquidity-risk-and-asset-pricing/06-advanced-extensions|06 · Advanced Extensions]].
