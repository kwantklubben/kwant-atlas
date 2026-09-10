---
title: "01 — Quantitative Fundamental Investing from Zero: What a Factor Is & Why Accounting Predicts Returns"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - intuition
  - factor-investing
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|Core Financial Ratios · 01 From Zero]] (what a ratio is). No prior factor-model knowledge needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of quantitative fundamental investing with **no prior knowledge needed**. The objective is one idea: **a fundamental factor is an accounting number that, when you sort the whole market on it and hold one side, has historically out-earned the other side — reliably, across many years.** The entire folder is that idea, elaborated and then stress-tested.

Start with the absurd question a factor answers: *why would one pile of accounting numbers predict the future returns of a whole market?* It sounds like it shouldn't — but it does, and it has for a century. Benjamin Graham's whole tradition was "buy what's cheap *and* solid," but he did it by judgment. The quantitative revolution asked the mechanical version: can we write the rule as *"sort every stock on book-to-market, buy the cheapest tenth, sell the dearest tenth, repeat every year"* — and does that rule beat just owning the market? The answer from Fama–French 1992 is **yes**, and that is where this subject starts.

Three steps, three "aha"s:

1. **A factor is a sort, not a formula.** You never invest "in the B/M ratio." You rank the entire universe on B/M and hold the cheap side against the expensive side. The *sort* is the strategy; the accounting number is just the axis. This is why every factor in this folder is built the same way: **rank → split into portfolios → compare realized returns.** Learn that skeleton and every factor, from value to the F-score, is the same machine with a different axis.

2. **Accounting predicts returns because prices are slow to digest accounting.** Ball & Brown (1968) showed stock prices move *in the direction of* earnings news — accounting information moves markets. The factor literature's deeper claim is that prices under-react: a firm that is cheap on book value *and* financially strong keeps earning a premium for years afterward (Piotroski's under-reaction; Bernard & Thomas's post-earnings-announcement drift). Fundamental data predicts returns because the market is *systematically late* to re-price it.

3. **The premium is an average over a long horizon, not a guarantee for any single stock.** Value out-earns growth over decades, but in any single year the expensive-and-wonderful can crush the cheap-and-ugly. A factor is a *statistical* edge — a positive expected spread — and that is why [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] (crowding, data mining, drift) matters as much as the construction.

---

### 2. Mathematical Ground Truth & Derivations

**The value characteristic — book-to-market.** Let *BE* be the book value of common equity and *ME* the market value of equity (price $\times$ shares). The value factor sorts on

$$\text{B/M} = \frac{\text{BE}}{\text{ME}}.$$

The intuition is direct: *BE* is the accounting capital the shareholders actually put in and retained; *ME* is what the market currently prices it at. A high B/M (cheap) means the market prices the firm at little more than its book capital — Graham's bargain. A low B/M (dear) means the market is paying for future growth far above book. Fama–French 1992's central finding was that **high-B/M firms earned higher average returns than low-B/M firms**, and that this ordering survived controlling for beta.

**The sort-and-compare estimator.** With $N$ firms, rank them on the characteristic $c_i$, split into $K$ portfolios by rank, and compare equal-weighted average returns:

$$\overline{r}_k \;=\; \frac{1}{N_k}\sum_{i\,\in\,\text{portfolio }k} r_i, \qquad
\text{factor spread} \;=\; \overline{r}_K - \overline{r}_1.$$

If the characteristic is a *priced* factor, the spread $\overline{r}_K-\overline{r}_1$ is reliably positive over many re-balancing periods. This is the single estimator every construction in the folder reduces to — a fact worth remembering before any exotic factor design.

**Why earnings yield is value in disguise.** Book-to-market and earnings yield are two lenses on the same "cheapness" idea:

$$\text{E/P} = \frac{\text{NI}}{\text{ME}} = \frac{1}{\text{P/E}},$$

and Basu (1983) showed high-E/P (low P/E) firms earn more. Both ask "is the price cheap relative to a fundamental?" — the fundamental is book value in one case, earnings in the other.

---

### 3. Computational Implementation — the value sort, stdlib only

The entire discipline in one script: rank twelve firms on book-to-market, split into three value portfolios, and read off the realized return spread. This is the machine every later page scales up.

```python
# The core idea: sort the universe on B/M, hold the cheap side, watch the spread.
# fields: name, book equity, market cap, next-year return
U = [
 ("AlphaChem",  6000,  8000, 0.140),
 ("BetaSteel",  1200,  3000, 0.095),
 ("GammaHealth",3000, 15000, 0.115),
 ("DeltaRetail",1600,  2000, 0.125),
 ("EpsilonTech",2000, 12000, 0.105),
 ("ZetaUtil",   4800,  4000, 0.160),
 ("EtaEnergy",  1000,  2500, 0.110),
 ("ThetaPharma",3600,  9000, 0.135),
 ("IotaAuto",   1400,  3500, 0.115),
 ("KappaSoft",  2400, 18000, 0.100),
 ("LambdaFood", 1350,  1500, 0.150),
 ("MuMach",     3000,  5000, 0.128),
]
from statistics import mean
def bm(r): return r[1]/r[2]                      # book-to-market
print(f"{'firm':12s} {'B/M':>6s} {'ret%':>6s}")
for r in U: print(f"{r[0]:12s} {bm(r):6.3f} {r[3]*100:6.2f}")
s = sorted(U, key=bm); k = len(s)//3
cheap, middle, dear = s[2*k:], s[k:2*k], s[:k]   # cheap = HIGH B/M
for lab, seg in [("CHEAP (high B/M)", cheap), ("MIDDLE", middle), ("DEAR (low B/M)", dear)]:
    print(f"  {lab:18s} avg B/M={mean([bm(r) for r in seg]):.3f}  avg ret={mean([r[3] for r in seg])*100:.2f}%")
spread = mean([r[3] for r in cheap])*100 - mean([r[3] for r in dear])*100
print(f"\nValue spread (CHEAP - DEAR) = {spread:+.2f}%  -> the sort pays")
```

```text
firm            B/M   ret%
AlphaChem     0.750  14.00
BetaSteel     0.400   9.50
GammaHealth   0.200  11.50
DeltaRetail   0.800  12.50
EpsilonTech   0.167  10.50
ZetaUtil      1.200  16.00
EtaEnergy     0.400  11.00
ThetaPharma   0.400  13.50
IotaAuto      0.400  11.50
KappaSoft     0.133  10.00
LambdaFood    0.900  15.00
MuMach        0.600  12.80
  CHEAP (high B/M)   avg B/M=0.912  avg ret=14.37%
  MIDDLE             avg B/M=0.450  avg ret=12.20%
  DEAR (low B/M)     avg B/M=0.225  avg ret=10.38%

Value spread (CHEAP - DEAR) = +4.00%  -> the sort pays
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing "a factor" with "a formula."** The value edge lives in the *sort across the whole market*, not in any single firm's B/M. One cheap stock can stay cheap forever (a value trap); the premium is the *average* over thousands of firms and many years. Reading any single stock's B/M as a factor signal is the beginner error.
2. **Believing the spread is a guarantee.** The +4.00% here is a *realized sample* spread; in a given year the dear side can win. Factors are expected-value edges with long, painful drawdowns — which is exactly why [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] exists.
3. **Ignoring that profitability can swamp a naive value sort.** This page's sort pays because the sample was chosen so. Real markets confound — the profitable-but-expensive firm earns a lot yet looks "dear" on B/M alone. That is the Novy-Marx critique and the reason value must be combined with profitability ([[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]]).

---

### 5. Canonical Literature & Study References

- **Ball, Ray & Brown, Philip**: "An Empirical Evaluation of Accounting Income Numbers" (*JAR*, 1968) — the origin of "accounting earnings move prices"; the empirical foundation of the whole fundamental-information line.
- **Basu, Sanjoy**: "The Relationship Between Earnings Yield, Market Value and Return for NYSE Common Stocks" (*JFE*, 1983) — the E/P effect.
- **Fama & French**: "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — size + book-to-market capture the cross-section; the founding result of this page.
- **Bernard, Victor & Thomas, Jacob**: "Post-Earnings-Announcement Drift" (*JAR*, 1989) — the market under-reacts to the implications of earnings; the under-reaction channel that explains why fundamental data predicts returns.
- **Graham, Benjamin**: *The Intelligent Investor* — the qualitative ancestor: cheap-and-solid; the quant version is what this folder builds.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|Core Financial Ratios · 01 From Zero]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Forward: [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Base: [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]]
