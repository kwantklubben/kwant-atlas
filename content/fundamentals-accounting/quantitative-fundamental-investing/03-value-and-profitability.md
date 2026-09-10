---
title: "03 — Value & Profitability: Book-to-Market, Earnings Yield, and Novy-Marx's Gross Profitability"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - value-factor
  - profitability
  - novy-marx
---

**Basic Prerequisites:** [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] and [[fundamentals-accounting/core-financial-ratios/03-valuation-multiples|Core Financial Ratios · Valuation Multiples]].

---

### 1. Intuition & Practical Objective

Value says *buy cheap*; profitability says *buy good*. This page is where the two meet — and where the naivest reading of each fails. The objective is one idea from Robert Novy-Marx (2013): **profitability is "the other side of value" — profitable firms earn higher returns than unprofitable ones, even though they are systematically more expensive.** And the reverse is the value trap: the cheapest stocks by book-to-market are often cheap *because* they are unprofitable.

The two facts sit awkwardly together, and resolving them is the whole craft:

- **Value works** — high book-to-market (cheap) and high earnings-yield firms earned higher average returns (Basu 1983; Fama–French 1992).
- **But a naive value sort is a value-trap machine.** The *cheapest* firms by B/M are disproportionately distressed, unprofitable businesses whose cheapness is a correct forecast of deterioration. Buying "cheap" blindly buys the junk.
- **Profitability is the filter that rescues it.** Novy-Marx's gross profitability — the rawest measure of pricing power, gross profit over assets — predicts returns with *roughly the same power as book-to-market*, and it is *negatively* correlated with it (profitable firms are more expensive). So the two correct each other: value filters the froth, profitability filters the traps.

The practical output is the **combined screen**: rank on value *and* profitability and hold the intersection — the "good *and* cheap" basket that Greenblatt's magic formula (earnings yield + ROIC) and Piotroski's F-score (value + quality) both operationalize. This page builds the value and profitability axes; [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]] builds the quality composite.

---

### 2. Mathematical Ground Truth & Derivations

**Value characteristics.** With *BE* book equity, *ME* market equity, *NI* net income:

$$\text{B/M} = \frac{\text{BE}}{\text{ME}}, \qquad
\text{E/P} = \frac{\text{NI}}{\text{ME}} = \frac{1}{\text{P/E}}.$$

Both ask "is the price cheap relative to a fundamental?" High B/M anchors value on book capital; high E/P anchors it on earnings. Both are *priced*: Fama–French 1992 showed the cross-section is captured by size + B/M, and E/P carries value information of its own.

**Profitability — Novy-Marx's gross profitability.** Let $GP = S - \text{COGS}$ be gross profit and *TA* total assets:

$$\frac{GP}{A} = \frac{S - \text{COGS}}{\text{TA}}.$$

Deliberately stripped down to the layer *before* SG&A, R&D, interest and taxes, gross profitability is the purest accounting signal of the business's pricing power — how much of every sales dollar survives the direct cost of goods. Novy-Marx (2013) shows high-$GP/A$ firms earn higher returns *despite* having higher valuation ratios (more expensive) — the empirical wedge that value alone misses.

**The trap and the resolution.** Because high-$GP/A$ firms tend to be *low*-B/M (expensive growth), a single sort on B/M and a single sort on $GP/A$ are two near-independent (in fact mildly negatively correlated) orderings. The two-factorial claim is:

$$\text{good}\;\&\;\text{cheap} = \text{rank}(B/M)\;\cap\;\text{rank}(GP/A),$$

and the composite that Fama–French 2015 embeds in the model — **HML (value) + RMW (profitability)** — is precisely this pair, with each roughly neutralized against size.

---

### 3. Computational Implementation — the "other side of value" in one script

Stdlib only. Twelve firms with book equity, market cap, gross profit and assets. The script (a) shows the **gross profitability premium** is monotone, (b) shows that **profitable firms are more expensive yet earn more** — the naive value sort *loses* here because cheap = unprofitable — and (c) shows that **within the cheap basket, the profitable firms beat the value traps.**

```python
# The other side of value. fields: name, book, market, gross profit, assets, ROE
rows = [
 ("VulcanSteel",  4800,  4000,  480,  9000, 0.05),
 ("PioneerAuto",  3600,  4200,  540,  9800, 0.06),
 ("HeartlandBank",2800,  3800,  300,  7000, 0.07),
 ("IronCladUtil", 5200,  6200,  520,  8200, 0.06),
 ("SummitFood",   2600,  3400,  400,  8000, 0.08),
 ("TerraMining",  2200,  2800,  450,  7500, 0.10),
 ("MarinaLogist", 1800,  2600,  480,  7200, 0.11),
 ("VertexTech",   2100,  5200,  620,  7600, 0.13),
 ("PrismHealth",  1900,  6000,  700,  8000, 0.16),
 ("CobaltSemi",   1700,  7000,  880,  8200, 0.20),
 ("NovaSoftware", 1500,  9500,  980,  8400, 0.26),
 ("AetherCloud",  1300, 11000, 1150,  8600, 0.34),
]
from statistics import mean
bm  = lambda r: r[1]/r[2]                # book-to-market
gpa = lambda r: r[3]/r[4]                # gross profitability
ret = [0.04 + 0.30*gpa(r) for r in rows] # realized returns (increasing in GP/A)
print(f"{'firm':14s} {'B/M':>6s} {'GP/A':>6s} {'ret%':>6s}")
for r, rr in zip(rows, ret):
    print(f"{r[0]:14s} {bm(r):6.3f} {gpa(r):6.3f} {rr*100:6.2f}")
def terce(key):
    o = sorted(range(len(rows)), key=lambda i: key(rows[i])); k = len(rows)//3
    return [mean([ret[i] for i in o[s:s+k]])*100 for s in (0, k, 2*k)]
print(f"\nGross-profitability terciles (low->high): {[f'{x:.2f}%' for x in terce(gpa)]}  <- the premium")
print(f"Book-to-market   terciles (low->high): {[f'{x:.2f}%' for x in terce(bm)]}  <- naive value LOSES here")
# combination: within the cheap (high B/M) basket, split by profitability
half = len(rows)//2
cheap = sorted(range(len(rows)), key=lambda i: bm(rows[i]))[half:]
gbar = mean([gpa(rows[i]) for i in cheap])
prof  = [i for i in cheap if gpa(rows[i]) >  gbar]
traps = [i for i in cheap if gpa(rows[i]) <= gbar]
print(f"\nCHEAP (high B/M) basket split by profitability:")
print(f"  cheap AND profitable:    {[rows[i][0] for i in prof]}  avg ret={mean([ret[i] for i in prof])*100:.2f}%")
print(f"  cheap AND unprofitable:  {[rows[i][0] for i in traps]}  avg ret={mean([ret[i] for i in traps])*100:.2f}%  <- value traps")
```

```text
firm              B/M   GP/A   ret%
VulcanSteel     1.200  0.053   5.60
PioneerAuto     0.857  0.055   5.65
HeartlandBank   0.737  0.043   5.29
IronCladUtil    0.839  0.063   5.90
SummitFood      0.765  0.050   5.50
TerraMining     0.786  0.060   5.80
MarinaLogist    0.692  0.067   6.00
VertexTech      0.404  0.082   6.45
PrismHealth     0.317  0.087   6.62
CobaltSemi      0.243  0.107   7.22
NovaSoftware    0.158  0.117   7.50
AetherCloud     0.118  0.134   8.01

Gross-profitability terciles (low->high): ['5.51%', '6.04%', '7.34%']  <- the premium
Book-to-market   terciles (low->high): ['7.34%', '5.81%', '5.74%']  <- naive value LOSES here

CHEAP (high B/M) basket split by profitability:
  cheap AND profitable:    ['TerraMining', 'IronCladUtil', 'PioneerAuto']  avg ret=5.79%
  cheap AND unprofitable:  ['HeartlandBank', 'SummitFood', 'VulcanSteel']  avg ret=5.46%  <- value traps
```

*Read the two tercile lines together — they are Novy-Marx's headline.* Gross profitability is a clean monotone premium (5.51 → 6.04 → 7.34%). But a naive value sort goes the *wrong way* in this universe: the cheapest (highest B/M) tercile earns the *least* (5.74%) because the cheapest firms are exactly the unprofitable value traps. The resolution is the last block: within the cheap basket, the *profitable* cheap firms (5.79%) beat the unprofitable ones (5.46%). Profitability doesn't replace value — it is the filter that lets value work.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The value trap (cheap = bad).** The deepest first-principle failure of a naive value sort: cheapness is often a *correct* market forecast of deterioration. Buy "cheap" blindly and you buy the distressed and the dying. This is why every serious value implementation layers a quality/profitability filter on top (Novy-Marx, Piotroski, Greenblatt).
2. **Ignoring the value-profitability confound.** Sorting on one without controlling for the other misattributes the premium. A univariate B/M sort that ignores profitability over-weights the traps; a univariate $GP/A$ sort that ignores value over-weights expensive growth names. The two must be conditioned on each other (double-sort or multivariate).
3. **Convention drift in "profitability."** Gross profitability, ROE, and ROIC are *different* numbers with different denominators (assets, equity, invested capital) and different tax/loss conventions — see [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|Core Financial Ratios · Profitability]]. A "profitability factor" is only comparable if the definition is fixed.
4. **Non-monotonicity in practice.** Real value and profitability premia are concentrated in extreme deciles and can be weak or negative in the middle of the cross-section — the monotone tercile pattern on this page is a constructed idealization, not a market guarantee (see [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Fama & French**: "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — B/M and E/P as priced cross-sectional value drivers.
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013) — *gross profitability predicts with roughly the same power as book-to-market, and profitable firms earn more despite higher valuation ratios; verified against the corpus paper.*
- **Fama & French**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015) — HML (value) and RMW (profitability) as distinct priced factors.
- **Basu, Sanjoy**: "The Relationship Between Earnings Yield, Market Value and Return for NYSE Common Stocks" (*JFE*, 1983) — the E/P effect.
- **Greenblatt, Joel**: *The Little Book That Beats the Market* — the magic formula: rank on earnings yield + ROIC; the famous "good *and* cheap" combination this page's double-sort formalizes.
- **Hou, Xue & Zhang**: "Digesting Anomalies" (*RFS*, 2015) — ROE as the profitability leg of the q-factor model.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Forward: [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]] (the composite that layers quality onto value)
- Base: [[fundamentals-accounting/core-financial-ratios/03-valuation-multiples|Core Financial Ratios · Valuation Multiples]] · [[fundamentals-accounting/fundamental-analysis-and-screening/02-graham-criteria-and-value-investing|Graham Criteria & Value Investing]]
- Factor-model layer: [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]]
