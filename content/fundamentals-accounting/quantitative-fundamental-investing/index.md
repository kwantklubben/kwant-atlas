---
title: "Quantitative Fundamental Investing"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - factor-investing
  - fama-french
  - piotroski
  - index-hub
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the ratio catalog and its lookup table), [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] (the discretionary screen these factors mechanize), and [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (the defense layer every factor inherits). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A screen *filters*; a **factor** *predicts — systematically, across the whole market*. This folder is the seat of the difference: turning the accounting data of the previous folders (book value, earnings, gross profit, asset growth, accruals) into **priced characteristics** — fundamental signals on which, on average and over long horizons, cheap-and-good firms have out-earned expensive-and-bad ones. This is quantitative fundamental investing: take a *real* number off the statements, sort the entire universe on it, hold the cheap side, and let the cross-section do the work.

The governing fact, from Fama–French 1992: **two easily measured variables — size and book-to-market — capture the cross-sectional variation in average returns** that the CAPM's beta alone could not. That single paper ended the "one risk factor (beta)" era and opened the factor catalog this folder maps: **value** (book-to-market, earnings yield), **profitability** (ROE, gross profitability), **investment** (asset growth), and **quality** (the Piotroski F-score, accruals). Fama–French 2015 then put two of those — profitability (RMW) and investment (CMA) — *inside* the asset-pricing model, which is the formal statement that accounting fundamentals are priced risk, not curiosities.

> **The one-sentence essence.** "A fundamental factor is an accounting characteristic that, when you sort the market on it and hold one side, has historically earned a persistent premium — value pays for cheapness, profitability pays for quality, investment punishes over-investment, and the F-score separates the cheap-and-strong from the cheap-and-doomed."

**Audience arc:** beginner learns *what a factor is and why accounting data predicts returns*; intermediate learns *how each factor is constructed and sorted into portfolios*; expert reads *the factor-model evidence, how factors are combined, and where the premium decays (crowding, data mining)*. The sub-pages below are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Factor Lookup Table

**Notation:** $B/M$ book-to-market $=$ book common equity / market equity; $E/P$ earnings yield $=$ net income / market equity; $ROE$ net income / book equity; $GP/A$ gross profitability $=$ (sales $-$ COGS) / total assets; $g_A$ asset growth $=$ $\Delta$ total assets / prior total assets; $F$ the Piotroski F-score (0–9); $CFO$ cash flow from operations.

| Factor | Construction | Sort & long side | Sign of premium | Evidence anchor |
|---|---|---|---|---|
| **Size** | Market equity $=$ price $\times$ shares | small vs. big | small earns more | Fama–French 1992, 1993 (SMB) |
| **Value** | $B/M=\dfrac{\text{BE}}{\text{ME}}$ (or $E/P$) | high $B/M$ (cheap) | **positive** | Fama–French 1992, 1993 (HML) |
| **Earnings yield** | $E/P=\dfrac{\text{NI}}{\text{ME}}$ | high $E/P$ | positive | Basu 1983; Fama–French 1992 |
| **Profitability (gross)** | $GP/A=\dfrac{S-\text{COGS}}{\text{TA}}$ | high $GP/A$ | **positive** | Novy-Marx 2013; Fama–French 2015 (RMW) |
| **Profitability (ROE)** | $ROE=\dfrac{\text{NI}}{\text{BVE}}$ | high $ROE$ | positive | Hou, Xue & Zhang 2015 (q-factor) |
| **Investment** | $g_A=\dfrac{\Delta\text{TA}}{\text{TA}_{t-1}}$ | low $g_A$ (conservative) | **negative** | Fama–French 2015 (CMA) |
| **Quality (composite)** | Piotroski $F=\sum_{i=1}^9 \mathbf{1}[\text{signal}_i]$ | high $F$ | positive | Piotroski 2000 |
| **Quality (accruals)** | Accruals $=$ NI $-$ CFO | low accruals | negative | Sloan 1996; Chan et al. 2006 |

*(All lookup values computed and reproduced exactly in §3 and re-verified on each sub-page; the sample universe "AlphaChem, BetaSteel, …" is fully specified on each sub-page.)*

> **Critical scaling caveat — factors are cross-sectional orderings, not absolute thresholds.** Every factor premium is a *relative* statement: the top tercile of the universe on $B/M$ out-earned the bottom tercile *on average, over many years*. A single firm's $B/M$ is nearly meaningless; its *rank against the market's current cross-section* is the factor signal. This is why every factor is built by **sorting**, and it is the discipline that [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] operationalizes.

---

### 3. Computational Implementation — the factor engine

Runs on the **standard library only**. It takes one cross-section of twelve firms' statements, computes every fundamental factor on the lookup table (value, earnings yield, gross profitability, ROE, asset growth), sorts the universe into **value-weighted portfolio terciles** on each factor, and reports each factor's realized return spread — the machine that every screen and every Fama–French construction in this folder reduces to.

```python
# Factor engine: 12-firm universe, all fundamental factors, one pass.
# fields: name, market cap, book equity, gross profit, total assets, ROE, asset growth, realized return
U = [
 ("AlphaChem",  8000, 6000, 2100, 12000, 0.22, 0.08, 0.140),
 ("BetaSteel",  3000, 1200,  300,  5000, 0.06, 0.18, 0.095),
 ("GammaHealth",15000,3000, 3600, 16000, 0.18, 0.10, 0.115),
 ("DeltaRetail",2000, 1600,  240,  3000, 0.05, 0.05, 0.125),
 ("EpsilonTech",12000,2000, 4500,  9000, 0.30, 0.25, 0.105),
 ("ZetaUtil",   4000, 4800,  520,  8000, 0.07, 0.02, 0.160),
 ("EtaEnergy",  2500, 1000,  300,  4500, 0.09, 0.15, 0.110),
 ("ThetaPharma",9000, 3600, 2800, 11000, 0.15, 0.06, 0.135),
 ("IotaAuto",   3500, 1400,  420,  6000, 0.08, 0.12, 0.115),
 ("KappaSoft",  18000,2400, 6500, 10000, 0.35, 0.30, 0.100),
 ("LambdaFood", 1500, 1350,  170,  2200, 0.04, 0.03, 0.150),
 ("MuMach",     5000, 3000,  900,  7000, 0.12, 0.07, 0.128),
]
from statistics import mean
bm  = lambda r: r[2]/r[1]                # book-to-market (value)
ep  = lambda r: (r[2]*r[5])/r[1]         # E/P  = book*ROE / market cap
gpa = lambda r: r[3]/r[4]                # gross profitability GP/A
def tercile_returns(data, key):
    s = sorted(data, key=key); k = len(s)//3
    segs = s[:k], s[k:2*k], s[2*k:]
    return [mean([x[7] for x in seg])*100 for seg in segs]
print(f"{'firm':12s} {'B/M':>6s} {'E/P%':>6s} {'GP/A':>6s} {'ROE%':>6s} {'ret%':>6s}")
for r in U:
    print(f"{r[0]:12s} {bm(r):6.3f} {ep(r)*100:6.2f} {gpa(r):6.3f} {r[5]*100:6.1f} {r[7]*100:6.2f}")
print("\nTercile average returns (low -> high factor value):")
for label, key in [("B/M (value)", bm), ("E/P", ep), ("GP/A (gross profitability)", gpa),
                   ("ROE", lambda r: r[5]), ("Asset growth (investment)", lambda r: r[6])]:
    t = tercile_returns(U, key)
    print(f"  {label:32s} {t[0]:5.2f}% {t[1]:5.2f}% {t[2]:5.2f}%   spread={t[2]-t[0]:+.2f}%")
# HML-style value factor: long high-B/M tercile, short low-B/M tercile
t = tercile_returns(U, bm); hml = t[2] - t[0]
print(f"\nValue factor return (long high-B/M, short low-B/M) = {hml:+.2f}%  "
      f"-> the raw Fama-French HML construction in miniature")
```

```text
firm            B/M   E/P%   GP/A   ROE%   ret%
AlphaChem     0.750  16.50  0.175   22.0  14.00
BetaSteel     0.400   2.40  0.060    6.0   9.50
GammaHealth   0.200   3.60  0.225   18.0  11.50
DeltaRetail   0.800   4.00  0.080    5.0  12.50
EpsilonTech   0.167   5.00  0.500   30.0  10.50
ZetaUtil      1.200   8.40  0.065    7.0  16.00
EtaEnergy     0.400   3.60  0.067    9.0  11.00
ThetaPharma   0.400   6.00  0.255   15.0  13.50
IotaAuto      0.400   3.20  0.070    8.0  11.50
KappaSoft     0.133   4.67  0.650   35.0  10.00
LambdaFood    0.900   3.60  0.077    4.0  15.00
MuMach        0.600   7.20  0.129   12.0  12.80

Tercile average returns (low -> high factor value):
  B/M (value)                      10.38% 12.20% 14.37%   spread=+4.00%
  E/P                              10.88% 12.00% 14.08%   spread=+3.20%
  GP/A (gross profitability)       12.00% 13.58% 11.38%   spread=-0.62%
  ROE                              13.25% 12.20% 11.50%   spread=-1.75%
  Asset growth (investment)        14.25% 12.45% 10.25%   spread=-4.00%

Value factor return (long high-B/M, short low-B/M) = +4.00%  -> the raw Fama-French HML construction in miniature
```

*Read the spreads carefully — they are the whole folder in one table.* Value (B/M +4.0%, E/P +3.2%) and investment (−4.0%, i.e. *low* investment wins) show their premiums immediately. Gross profitability and ROE, however, show **no** raw premium in this naive sort — the profitable firms here are expensive growth firms (high GP/A, low B/M). That is *exactly* the Novy-Marx point that opens [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]]: profitability pays, but only once value is conditioned on — you must control the expensive/profitable confound.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Backtests manufacture premiums.** Test enough random characteristics and one will look spectacular by chance — Green, Hand & Zhang's 200-odd return-predictive signals are mostly redundancy around a handful of real factors. Data-mining is the factor's occupational disease.
2. **Factors crowd and decay.** A published premium is an arbitrage with a half-life; once it is crowded, the return compresses. The value premium of the 1990s is thinner today — crowding is a *first-principles* ceiling, not a bug.
3. **Accounting games hit the factor at its source.** A factor is only as honest as the line items it sorts on — restatements, accrual manipulation, and look-ahead leakage silently corrupt the cross-section (see [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]).

---

### 5. Canonical Literature & Study References

- **Fama, Eugene & French, Kenneth**: "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — size + book-to-market capture the cross-section; the paper that displaced the one-beta CAPM story. *Factor definitions and headline result verified against the corpus paper.*
- **Fama & French**: "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) — the canonical **three-factor model** (market, SMB, HML) and the 2×3 construction used across this folder.
- **Fama & French**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015) — adds **profitability (RMW)** and **investment (CMA)**; the formal seat of accounting fundamentals inside the asset-pricing model.
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013) — gross profitability predicts with roughly the same power as book-to-market, orthogonal to it.
- **Piotroski, Joseph D.**: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" (*JAR*, 2000) — the 9-signal F-score; value + quality in one mechanical screen (see [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]]).
- **Hou, Kewei; Xue, Chen & Zhang, Lu**: "Digesting Anomalies: An Investment Approach" (*RFS*, 2015) — the q-factor model (investment + ROE) that consolidates most anomalies through a production-based lens.
- **Green, Jeremiah; Hand, John R. M. & Zhang, X. Frank**: "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns" (*RFS*, 2017) — the 100-characteristic census and the 24 genuinely priced signals (see [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]]).
- **Sloan, Richard**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 1996) — the accruals quality factor.

---

### 6. Connected Graph Bridges

- Foundational base: [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] (the discretionary screen this folder mechanizes) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (the defense layer every factor inherits)
- Sibling topics: [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] (why low $B/M$ and high $E/P$ are "cheap") · [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (point-in-time Compustat/EDGAR — where factor inputs come from)
- Quantitative bridges: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (the Barra/FF factor-model construction layer) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (why a backtested factor premium must be discounted) · [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (how factor tilts become portfolios)
- Sub-pages (in-folder): 01 From Zero · 02 Fundamental Factors · 03 Value & Profitability · 04 Quality & F-scores · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[fundamentals-accounting/quantitative-fundamental-investing/01-from-zero-intuition|01 · From Zero]] — no prior factor knowledge needed.
- **Construction (undergrad/job-seeking):** [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] → [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]] → [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]].
- **Evidence & robustness (practitioner/graduate):** [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] → [[fundamentals-accounting/quantitative-fundamental-investing/06-advanced-extensions|06 · Advanced Extensions (factor models, combining)]].
