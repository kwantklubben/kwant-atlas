---
title: "03 — Factor Construction: SMB, HML, RMW, CMA via Independent Sorts"
tags:
  - pillar-quant-research
  - fundamental-multi-factor-models
  - factor-construction
  - fama-french
  - hedge-portfolio
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/fundamental-multi-factor-models/02-fama-french-factor-model|02 · The FF Factor Model]] (the regression the constructed factors feed into).

---

### 1. Intuition & Practical Objective

The factors of the previous page are not handed down; they are **built by sorting**. The practical objective of this page: reproduce the exact Fama–French recipe so you can construct SMB, HML, RMW, and CMA from raw data (or from Ken French's library), understand *why* each step exists, and then feed the result into the time-series regression. A factor is a **long-short hedge portfolio** — a traded spread between the extreme groups of a sort — so its return is the *price* of that style risk.

The four FF factors and the characteristics they sort on:

| Factor | Name | Sort on | Long side | Interpretation |
|---|---|---|---|---|
| **MKT** | Market | — | the market | the one-factor benchmark |
| **SMB** | Size | market cap (ME) | small | small-cap risk premium |
| **HML** | Value | book-to-market (B/M) | high B/M (cheap) | value risk premium |
| **RMW** | Profitability | operating profitability (OP) | robust (high OP) | profitability premium |
| **CMA** | Investment | asset growth / investment (Inv) | conservative (low Inv) | punishes over-investment |

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The canonical 2×3 construction (FF 2015, §4; FF 1993)

At each rebalance (in June, using prior-fiscal-year accounting with a lag to avoid look-ahead):

1. **Size breakpoint:** the NYSE **median** market cap splits stocks into *Small* and *Big* (S/B). *Only NYSE stocks set breakpoints* — the sample then covers NYSE+AMEX+NASDAQ, so extreme microcaps cannot dominate the splits.
2. **Second-sort breakpoints:** the NYSE **30th and 70th percentiles** of B/M (for HML), operating profitability (for RMW), or investment (for CMA) give three groups (Low/Mid/High).
3. **Independent 2×3 sorts** → six value-weighted portfolios (value-weighted so the factor isn't swamped by microcap noise).

Define $R_{xy}$ as the value-weighted return of the portfolio in size class $x\in\{S,B\}$ and signal class $y$. Then:

$$\text{HML}=\frac{R_{SH}+R_{BH}}{2}-\frac{R_{SL}+R_{BL}}{2}\quad\text{(high B/M minus low B/M, averaged over small \& big),}$$
$$\text{RMW}=\frac{R_{SR}+R_{BR}}{2}-\frac{R_{SW}+R_{BW}}{2}\quad\text{(robust minus weak profitability),}$$
$$\text{CMA}=\frac{R_{SC}+R_{BC}}{2}-\frac{R_{SA}+R_{BA}}{2}\quad\text{(conservative minus aggressive investment),}$$

and the **size factor** is the average of the three size spreads — one from each of the B/M, OP, and Inv sorts (FF 2015 §4):
$$\text{SMB}=\frac{\text{SMB}_{B/M}+\text{SMB}_{OP}+\text{SMB}_{Inv}}{3}.$$

#### 2.2 Why 2×3 and value-weighted? (first-principles design choices)

- **Two size × three signal groups** balances power against noise: the 30/70 breakpoints keep enough stocks in the extreme HML groups to be diversified, while independent (not sequential) sorts let each signal vary holding the others roughly fixed.
- **Value-weighting** keeps factor returns economically meaningful — a market-cap-weighted long-short is tradeable at low cost, unlike an equal-weight microcap spread (which Tsay notes would be dominated by illiquid names).
- **The 6-month accounting lag** (June rebalance on prior-December fiscal data) enforces point-in-time availability and is the FF defense against look-ahead bias.

#### 2.3 Relation to the factor-mimicking portfolio

Every factor return is a linear combination of underlying portfolio returns — a **factor-mimicking portfolio**. In the BARRA formalism (Tsay §9.3.1), the factor realization is $\hat f_t=\omega^\top r_t$ with portfolio weights $\omega=(X^\top V^{-1}X)^{-1}X^\top V^{-1}$; in the FF formalism the weights are the simple $\pm\tfrac12$ (or $\pm\tfrac13$) patterns above. Both are the same object: a traded portfolio whose return tracks a priced characteristic. See [[pillars/01-quantitative-research/fundamental-multi-factor-models/04-cross-sectional-models|04 · Cross-Sectional Models]].

---

### 3. Computational Implementation — building SMB and HML from a cross-section

We reproduce the 2×3 independent sort on a synthetic 200-stock monthly cross-section: split on median size, split on 30/70 B/M percentiles, form six value-weighted portfolios, and compute SMB and HML. Stdlib only.

```python
import math, random

random.seed(5)
N = 200
stocks = [[math.exp(random.gauss(5.0,1.4)), math.exp(random.gauss(0.0,0.9)),
           random.gauss(0.008,0.07)] for _ in range(N)]   # (size, B/M, return)

def median(xs):
    s = sorted(xs); m = len(s)//2
    return s[m] if len(s) % 2 else (s[m-1]+s[m])/2
def q(xs, p):
    s = sorted(xs); k = int(p*len(s)); return s[min(k, len(s)-1)]
def avg(xs): return sum(xs)/len(xs)

med_size = median([s[0] for s in stocks])                       # NYSE median (here: sample)
b30, b70 = q([s[1] for s in stocks],0.30), q([s[1] for s in stocks],0.70)

groups = {(g,j): [] for g in ('S','B') for j in ('L','M','H')}
for s in stocks:
    g = 'S' if s[0] < med_size else 'B'
    j = 'L' if s[1] < b30 else ('H' if s[1] > b70 else 'M')
    groups[(g,j)].append(s)
def vw(grp):                                            # value-weighted by size
    tot = sum(s[0] for s in grp)
    return sum(s[0]*s[2] for s in grp)/tot if grp else 0.0
R = {k: vw(v) for k, v in groups.items()}

SMB = avg([R[('S','L')],R[('S','M')],R[('S','H')]]) - avg([R[('B','L')],R[('B','M')],R[('B','H')]])
HML = avg([R[('S','H')],R[('B','H')]]) - avg([R[('S','L')],R[('B','L')]])

print("Six value-weighted portfolios (monthly ret):")
for g in ('S','B'):
    for j in ('L','M','H'):
        print(f"  {g}-{j}: {R[(g,j)]*100:+.3f}%")
print(f"\nSMB = small avg - big avg  = {SMB*100:+.3f}%")
print(f"HML = high B/M - low B/M   = {HML*100:+.3f}%")
```
```
Six value-weighted portfolios (monthly ret):
  S-L: -0.014%
  S-M: +0.878%
  S-H: +1.778%
  B-L: -2.111%
  B-M: -1.046%
  B-H: +2.995%

SMB = small avg - big avg  = +0.935%
HML = high B/M - low B/M   = +3.448%
```

*This is the whole construction in one script*: two independent sort dimensions, six value-weighted cells, and the two long-short differences that *are* SMB and HML. RMW and CMA are built identically, substituting operating profitability and investment for B/M in the second sort.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Breakpoint universe ≠ investment universe.** If you set breakpoints on *all* stocks instead of NYSE-only, a flood of tiny NASDAQ names drags the "Big" bucket down to illiquid microcaps and the factor becomes untradeable. The NYSE-breakpoint rule exists precisely to prevent this.
2. **Sort dimension overlap (B/M vs OP vs Inv are correlated).** Because value, profitability, and investment are correlated, HML, RMW, and CMA are *not* mutually neutral — each carries an unknown mix of the others' exposures, which makes the separate regression slopes hard to interpret (FF 2015 explicitly warns about this). The 2×2×2×2 four-sort variant controls for all simultaneously.
3. **Value-weighting vs equal-weighting flips results.** An equal-weighted small-cap long-short is dominated by the most extreme, often illiquid, names; the "factor" then prices noise and microcap liquidity rather than a systematic risk premium.
4. **Point-in-time discipline.** Using restated accounting or current (rather than lagged) book values leaks information into the factor and inflates its apparent premium. The 6-month lag is not an accident.

---

### 5. Canonical Literature & Study References

- **Fama & French**, "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) — the original SMB/HML 2×3 construction.
- **Fama & French**, "A Five-Factor Asset Pricing Model" (*JFE*, 2015), §4 — the precise 2×3 and 2×2×2×2 recipes for SMB, HML, RMW, CMA; value-weighting and NYSE-breakpoint rules. *Construction verified against the corpus paper.*
- **Tsay**, *Analysis of Financial Time Series*, §9.3.2 — Fama–French hedge portfolios; §9.3.1 — factor-mimicking portfolios $\hat f_t=\omega^\top r_t$. *Math-verified.*
- **Ken French Data Library** — official SMB/HML/RMW/CMA returns (the reference implementation of these recipes).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/fundamental-multi-factor-models/02-fama-french-factor-model|02 · The FF Factor Model]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/fundamental-multi-factor-models/04-cross-sectional-models|04 · Cross-Sectional Models]] (Barra-style construction of factor returns from exposures)
- Fundamentals: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]]
- Sibling: [[pillars/01-quantitative-research/momentum/index|Momentum Factors]]
