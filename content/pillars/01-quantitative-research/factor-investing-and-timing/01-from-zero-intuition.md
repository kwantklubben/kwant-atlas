---
title: "1.10.1 Factor Investing from Zero"
tags:
  - pillar-quant-research
  - factor-investing-and-timing
  - intuition
  - cross-section
  - anomalies
---

**Basic Prerequisites:** none beyond school algebra. A reading of [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] helps but is not required for this page.

---

### 1. Intuition & Practical Objective

This page builds the *why* of factor investing with **no prior asset-pricing knowledge needed**. The objective is one idea: **a factor premium is not a prediction about any single stock — it is a rule for sorting a whole cross-section of stocks and holding the spread, and its power comes from the *width* of that cross-section, not the strength of the signal.**

Start with the dumbest question: *if markets are efficient, why would "buy cheap stocks" earn a premium?* Three answers, in increasing sophistication:

1. **It is compensation for risk.** Cheap (high book-to-market) firms are firms that have fallen on hard times; they are unusually exposed to bad times — recessions, financial distress, liquidity droughts. A risk-averse investor demands a higher expected return to hold them. Fama–French's HML is, on this reading, a *state variable*: the return that hurts precisely when everything else hurts. Cochrane (2011) makes the sharpest version of this: the fact that value portfolios *comove* — "if the value firms decline, they all decline together" — is what stops the Sharpe ratio rising without limit, and it is the real content of the value factor.
2. **It is a behavioural mispricing.** Investors over-extrapolate. They overpay for "growth stories" and shun boring, distressed firms; they chase winners and dump losers (momentum); they overpay for lottery-like high-volatility names. On this reading the premium is an arbitrage that should decay as capital crowds in.
3. **It is partly both, and it does not matter for the practitioner.** Ilmanen (2011): "If their profits represent (at least in part) risk premia rather than market inefficiencies, it is less likely that future excess returns will be fully competed away." The practical question is not *which story is true* but *how much of the premium survives, at what capacity, and whether any of the decay is predictable*.

**The four paradoxes a beginner must absorb.**

- **The premium is nearly invisible in any single month.** A factor premium of 3–5%/year with 15–20%/year volatility is a monthly Sharpe of ~0.02 — you cannot see it in a month, or even a year. It is visible only as the *average* of many independent bets. Grinold's law says why: $IR\approx IC\sqrt{\text{breadth}}$, and a factor has thousands of bets per year (300 stocks × 12 months).
- **A weak signal is still a good business.** Value's rank-correlation with next-month returns (its information coefficient) is on the order of 0.03–0.05. You would never trade one stock on that. Across 300 names it produces a Sharpe of ~2 (as §3 shows).
- **The factor is a *sort*, not a *list*.** The names in the value decile are not fixed; they churn as prices and book values move. The factor is a *rule* re-applied every period. That is why it is investable in a way that "buy stock X" is not.
- **Every premium is an arbitrage with a half-life.** The moment a premium is published and understood, capital moves in and it decays (McLean–Pontiff 2016). So the honest frame is: *a factor is a decaying asset, and your job is to estimate the decay curve.*

> **The one-sentence essence.** "A factor is a rule for sorting a cross-section on a characteristic and holding the spread — long-short, diversified across hundreds of names — whose premium is economically small per bet but large in aggregate because the cross-section is wide; and whose premium decays as capital crowds in."

---

### 2. Mathematical Ground Truth & Derivations

**From CAPM to the cross-section.** The CAPM says expected excess returns are proportional to market beta:
$$
\mathbb{E}[R_i]-R_f=\beta_i\big(\mathbb{E}[R_m]-R_f\big),\qquad \beta_i=\frac{\mathrm{Cov}(R_i,R_m)}{\mathrm{Var}(R_m)}.
$$
Fama and French (1992) tested this and found the relation is *flat*: "when the tests allow for variation in $\beta$ that is unrelated to size, the relation between market $\beta$ and average return is flat, even when $\beta$ is the only explanatory variable." What *does* line up with the cross-section is size and book-to-market:
$$
\mathbb{E}[R_i]-R_f=\beta_i\,MKT+\beta_{i,SMB}\,SMB+\beta_{i,HML}\,HML.
$$
The factors are built by sorting ([[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]] in the sibling folder); here we take them as given and ask how to *use* them.

**A sort is a cross-sectional regression.** Sort the $N$ stocks on characteristic $C_i$ into $J$ equally weighted bins, and read the mean return of the top bin minus the bottom bin. Cochrane (2011, §II.B) points out that **portfolio sorts are nonparametric cross-sectional regressions using non-overlapping histogram weights**: the "slope" of a regression $\mathbb{E}[R^e\mid C]=a+bC$ and the "1–10 spread" of a sort estimate the same object with different weighting functions. As the number of bins grows, the sort converges to the (nonparametric) conditional mean function.

**The information coefficient.** Define the standardized characteristic $z_{it}=(C_{it}-\bar C_t)/\sigma_{C,t}$. The IC at time $t$ is the cross-sectional correlation
$$
IC_t=\mathrm{corr}_i(z_{it},\,R_{i,t+1}).
$$
If we form a portfolio with weights $w_i\propto z_i$ (a long-short characteristic portfolio), the expected return of that portfolio is $\mathbb{E}[R_w]=IC\cdot\sigma_{\text{cross-sectional return}}\cdot\sqrt{N_{\text{effective}}}$ in magnitude — the precise statement of "breadth amplifies a weak signal." The **fundamental law of active management** (Grinold 1989) makes this an information ratio:
$$
IR\approx IC\times\sqrt{\text{breadth}}.
$$

**Worked numbers.** For a factor with IC $=0.045$ and breadth $=12\times 300=3600$ independent stock-months per year, $IR\approx0.045\times\sqrt{3600}=0.045\times60=2.7$ — close to the 2.05 measured in §3 (the gap is the imperfect independence of the bets and the decile-truncation loss). This is the *entire* reason factor investing exists: the signal is weak, the cross-section is wide.

**Why the same law kills factor timing.** Factor timing makes *one bet per month* on the factor itself. Its breadth is $\approx12$. To achieve an IR of 0.5 — a modest active strategy — you would need
$$
IC_{\text{timing}}=\frac{0.5}{\sqrt{12}}\approx0.14,
$$
an information coefficient nearly *three times* as strong as a good stock-selection signal, applied to a single, highly volatile bet. That is why the standard practitioner verdict (Ilmanen) is: "Let us not move from the extreme of no market timing to the other extreme of thinking it is easy."

---

### 3. Computational Implementation — one factor, end to end

Stdlib only. Build a synthetic cross-section with a known premium, sort it into deciles, hold the long-short, and read off the three numbers that define a factor: the spread, the IC, and the Sharpe ratio.

```python
import math, random
random.seed(199)
N, T = 300, 240                  # 300 stocks, 20 years of months
LAM, SIG = 0.003, 0.06           # TRUE premium 0.30%/mo per 1 s.d. of char; 6%/mo idio vol
spreads, slopes, ics = [], [], []
for _ in range(T):
    c = [random.gauss(0, 1) for _ in range(N)]          # standardized characteristic
    r = [LAM*c[i] + random.gauss(0, SIG) for i in range(N)]   # returns = premium*c + noise
    pairs = sorted(zip(c, r)); k = N//10
    spreads.append(sum(p[1] for p in pairs[-k:])/k - sum(p[1] for p in pairs[:k])/k)
    mc = sum(c)/N; mr = sum(r)/N
    num = sum((c[i]-mc)*(r[i]-mr) for i in range(N))
    den = sum((c[i]-mc)**2 for i in range(N))
    slopes.append(num/den)                                          # x-sectional regression slope
    ics.append(num/math.sqrt(den*sum((r[i]-mr)**2 for i in range(N))))  # IC
def mean(xs): return sum(xs)/len(xs)
m = mean(spreads); sd = math.sqrt(sum((x-m)**2 for x in spreads)/(len(spreads)-1))
print(f"decile 10 minus decile 1  = {m*100:+.3f}%/mo   (true premium {LAM*100:.2f}%/mo)")
print(f"cross-sectional slope     = {mean(slopes)*100:+.3f}%/mo")
print(f"mean information coeff.   = {mean(ics):+.3f}")
print(f"long-short Sharpe (ann.)  = {m/sd*math.sqrt(12):.2f}")
print(f"Grinold check: IC*sqrt(12*N) = {mean(ics)*math.sqrt(12*N):.2f}")
```
```
decile 10 minus decile 1  = +1.004%/mo   (true premium 0.30%/mo)
cross-sectional slope     = +0.272%/mo
mean information coeff.   = +0.045
long-short Sharpe (ann.)  = 2.05
Grinold check: IC*sqrt(12*N) = 2.69
```

Three readings. **(i)** The decile spread (+1.004%/mo) is *larger* than the per-unit premium (0.30%/mo) because a decile is not a point: under normality the top decile of the characteristic sits at $+1.75$ s.d. and the bottom at $-1.75$, so the spread spans about $3.5$ s.d. — and $0.003\times3.51=1.05\%$/mo is exactly what the simulation delivers. **(ii)** The IC is only 0.045 — a signal you would dismiss in any single-stock context (it puts 51.4% of names on the right side of the median, barely better than a coin flip). **(iii)** The Sharpe is 2.05, and Grinold's law predicts 2.69. That gap *is* the lesson: factor investing is a breadth game, and the residual gap is the cost of discretizing a continuous signal into deciles and the imperfect independence of the bets.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The single-stock illusion.** Beginners judge a factor by its hit rate on the stocks they know. A factor is a *cross-sectional average over hundreds of names*; evaluating it on a handful is measuring noise. The IC of 0.045 above means $\tfrac12+\arcsin(0.045)/\pi\approx51.4\%$ of names are on the right side of the median — barely better than a coin flip per name.
2. **The `LAM`-is-constant illusion.** The engine above assumes the premium is fixed. In reality the premium *varies over time* and *decays after publication* — that is the subject of [[pillars/01-quantitative-research/factor-investing-and-timing/04-post-publication-decay|04 · Post-Publication Decay]]. Assuming a constant premium is the single most consequential beginner error.
3. **The `breadth = N` illusion.** The Grinold check over-predicts because the bets are not independent: stocks share market and industry shocks, so effective breadth is smaller than $12N$. Correlated bets are the mechanism behind [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03 · Crowding & Capacity]].
4. **The "it's risk-free" illusion.** A long-short factor has *zero* market beta by construction but it is not riskless: its beta to *itself* is 1, its drawdowns are long and deep, and its tails are fatter than the Gaussian the Sharpe ratio assumes (see [[pillars/01-quantitative-research/factor-investing-and-timing/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Fama, Eugene & French, Kenneth**, "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — the flat-beta finding and the size/BM result that launched factor investing. *Verified against the corpus paper.*
- **Cochrane, John H.**, "Presidential Address: Discount Rates" (*JF*, 2011) §II — "a zoo of new factors"; sorts-as-regressions; the comovement argument. *Verified against the corpus paper.*
- **Grinold, Richard**, "The Fundamental Law of Active Management" (*JPM*, 1989) — $IR\approx IC\sqrt{\text{breadth}}$.
- **Ilmanen, Antti**, *Expected Returns* (Wiley, 2011), Ch 1 — the practitioner's case for value/carry/momentum and the warning against extremes on timing. *Verified against the corpus book.*

---

### 6. Connected Graph Bridges

- Continue: [[pillars/01-quantitative-research/factor-investing-and-timing/02-the-factor-zoo|02 · The Factor Zoo]] · [[pillars/01-quantitative-research/factor-investing-and-timing/index|Index Hub]]
- The construction half: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[pillars/01-quantitative-research/momentum/index|Momentum]]
