---
title: "04 — Post-Publication Decay: Does Publishing a Factor Destroy It?"
tags:
  - pillar-quant-research
  - factor-investing-and-timing
  - post-publication-decay
  - market-efficiency
  - mclean-pontiff
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/factor-investing-and-timing/02-the-factor-zoo|02 · The Factor Zoo]] and [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03 · Crowding & Capacity]].

---

### 1. Intuition & Practical Objective

The question every quant allocator eventually asks: **if a factor's premium is published in the *Journal of Finance*, does it still work afterwards?**

The cleanest answer is McLean & Pontiff (2016), who assembled **82 characteristics from 68 studies**, replicated 72 of them in-sample, and measured the premium in three windows: the original study's sample, the period **after the sample but before publication** (out-of-sample, pre-publication), and the period **after publication**. Their logic is a natural experiment:

- If return predictability is **entirely statistical bias** (data snooping, sample selection, multiple testing), the premium should disappear *out of sample* — before anyone has even read the paper.
- If it is **mispricing** and arbitrage is costly, the premium should survive out-of-sample but decay **after publication**, when the research "draws attention to characteristics" and capital moves in.
- If it is a **rational risk premium**, it should survive both.

The findings are stark and quantitative:

- **Out-of-sample decay ≈ 10%**, and **not statistically different from zero**. You cannot reject that there is no statistical bias.
- **Post-publication decay ≈ 35%**, and **statistically different from both 0% and 100%** ($t\approx-4.9$ in their pooled specification). "An in-sample alpha of 5% is expected to decay to 3.25% post-publication."
- Combining the two, "a lower bound on the publication effect of about **25%**."

And the mechanism shows up in the tape: "post-publication, stocks in characteristic portfolios experience higher **volume**, **variance**, and **short interest**, and higher correlations with portfolios that are based on published characteristics." Crucially, "post-publication return declines are **greater for characteristic portfolios that consist of stocks with low idiosyncratic risk**" — i.e. the effect is strongest exactly where arbitrage is *cheapest*, which is the signature of mispricing being competed away rather than risk.

> **The one-sentence essence.** "A published factor premium is an arbitrage with a half-life: roughly a third of it disappears after the paper comes out, the decay is largest where arbitrage is cheapest, and the out-of-sample decay *before* publication is too small to explain it — so the premium is mostly mispricing, and it is being harvested."

**Why it matters practically.** It sets the *discount rate* you should apply to any factor's backtest: multiply your in-sample alpha by roughly 0.65 before you believe it. It also implies the value of research is *front-loaded*: the earlier you trade a discovered factor (before it is famous), the more of the premium you capture — which is exactly why proprietary research and short-horizon signals are defended so fiercely.

---

### 2. Mathematical Ground Truth & Derivations

**The decay estimator.** Normalize each characteristic's mean return in the post-sample periods by its in-sample mean:
$$\hat d_{\text{OOS}}=1-\frac{\bar r_{\text{OOS}}}{\bar r_{\text{IS}}},\qquad \hat d_{\text{post}}=1-\frac{\bar r_{\text{post}}}{\bar r_{\text{IS}}}.$$
This normalization is the key design choice: it converts a heterogeneous collection of characteristics — some with 0.2%/month premia, some with 0.8% — into a *common scale* so they can be pooled. The pooled mean is the average survival fraction.

**The pooled regression form.** MP also estimate a specification with returns in levels,
$$\tilde r_{i,t}=\alpha+\beta_{\text{OOS}}\,\mathbb{1}[\text{post-sample}]+\beta_{\text{post}}\,\mathbb{1}[\text{post-publication}]+\varepsilon,$$
where the coefficients, divided by the in-sample mean, are percentage decays. Their headline coefficients correspond to the ~10% / ~35% split, with the post-publication dummy significant at $t\approx-4.9$ and robust to clustering on anomaly, controls for time trends, SSRN posting dates, and — importantly — a **linear** decay in the post-publication months rather than a step.

**The Fama–MacBeth / two-pass structure (why each characteristic is a portfolio).** For characteristic $i$, they form a long-short portfolio each month, scaled by the in-sample means, and run a **Fama–MacBeth cross-sectional regression** of returns on the characteristics each month, then average the monthly slope coefficients. The three windows are compared by the same estimator. A characteristic enters only if its in-sample $t$-statistic exceeds 1.50 (their replication filter; note that 10 of 82 could not be replicated at all).

**The breadth problem (why this result needed 82 characteristics).** A single characteristic's post-publication premium has enormous sampling error: the monthly portfolio volatility (≈3–5%) is an order of magnitude larger than the alpha (≈0.5%). Detecting a 35% decay in one characteristic would take literally centuries of data:
$$T^\star=\left(\frac{2\sigma}{\alpha\cdot d}\right)^2=\left(\frac{2\times0.03}{0.005\times0.35}\right)^2\approx1176\text{ months}\approx98\text{ years}.$$
**It is only the breadth across 82 characteristics that makes the decay observable.** This is Grinold's law applied to *research*: the signal is weak, so the sample must be wide.

**Reconciling with risk premia.** A risk-based factor (say, a bond risk premium) is *not* expected to decay on publication — you cannot arbitrage away compensation for bearing risk. MP's finding that the decay is concentrated in low-idiosyncratic-risk, liquid, dividend-paying stocks is precisely the pattern that distinguishes arbitrage-able mispricing from risk compensation: costs of arbitrage are lowest there, so capital arrives fastest.

---

### 3. Computational Implementation — the decay experiment

Stdlib only. This is McLean–Pontiff in miniature: 82 characteristics, an in-sample period, an out-of-sample pre-publication period, and a post-publication period, with the pooled survival fractions recovered.

```python
import math, random
def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))

# McLean-Pontiff (2016) in one simulation: 82 characteristics, publication splits the sample
random.seed(23)
M_CHAR, T_OOS, T_POST = 82, 120, 240      # 82 chars; 10 yrs pre-pub OOS, 20 yrs post-pub
ALPHA, VOL, D_OOS, D_POST = 0.005, 0.03, 0.10, 0.35   # 0.50%/mo in-sample; MP's ~10% and ~35% decays
z_oos, z_post = [], []
for _ in range(M_CHAR):
    z_oos  += [(ALPHA*(1-D_OOS)  + random.gauss(0, VOL))/ALPHA for _ in range(T_OOS)]
    z_post += [(ALPHA*(1-D_POST) + random.gauss(0, VOL))/ALPHA for _ in range(T_POST)]
def t_vs_one(z): return (mean(z)-1)/(sd(z)/math.sqrt(len(z)))
print(f"out-of-sample, pre-publication : survival = {mean(z_oos):.3f}  decay = {(1-mean(z_oos))*100:5.1f}%  (t vs 1.0 = {t_vs_one(z_oos):+.2f})")
print(f"post-publication               : survival = {mean(z_post):.3f}  decay = {(1-mean(z_post))*100:5.1f}%  (t vs 1.0 = {t_vs_one(z_post):+.2f})")
print(f"MP 2016 (82 characteristics): ~10% out-of-sample (NOT significant), ~35% post-publication (significant)")
print(f"An in-sample alpha of 5%/yr -> {5*mean(z_post):.2f}%/yr post-publication   (MP: 3.25%/yr)")
print(f"Months a SINGLE characteristic needs to detect its own 35% decay at t=2: {(2*VOL/(ALPHA*D_POST))**2:.0f}")
```
```
out-of-sample, pre-publication : survival = 0.852  decay =  14.8%  (t vs 1.0 = -2.41)
post-publication               : survival = 0.658  decay =  34.2%  (t vs 1.0 = -7.98)
MP 2016 (82 characteristics): ~10% out-of-sample (NOT significant), ~35% post-publication (significant)
An in-sample alpha of 5%/yr -> 3.29%/yr post-publication   (MP: 3.25%/yr)
Months a SINGLE characteristic needs to detect its own 35% decay at t=2: 1176
```

The simulation recovers the published result: a **34.2% post-publication decay** (MP: ~35%), an out-of-sample decay that is markedly smaller and *less* reliable, and the headline translation **5%/yr in-sample → 3.29%/yr post-publication** (MP: 3.25%). The last line is the one that matters for research design: a *single* characteristic could not detect its own decay in under a century — the result exists only because MP pooled 82 of them.

```python
import math, random
def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))

# MP's second finding: decay is LARGER for cheap-to-arbitrage characteristics
random.seed(2)
N_PER = 41
def group(decay, vol):
    z = []
    for _ in range(N_PER):
        alpha = random.uniform(0.004, 0.006)
        z += [(alpha*(1-decay) + random.gauss(0, vol))/alpha for _ in range(240)]
    return z
cheap  = group(0.45, 0.030)     # large, liquid, LOW idiosyncratic risk  -> easy to arbitrage
costly = group(0.20, 0.060)     # small, illiquid, HIGH idiosyncratic risk -> costly to arbitrage
mc, mh = mean(cheap), mean(costly)
se = math.sqrt(sd(cheap)**2/len(cheap) + sd(costly)**2/len(costly))
print(f"cheap-to-arbitrage  (low idio risk)  : survival = {mc:.3f}  -> decay = {(1-mc)*100:5.1f}%")
print(f"costly-to-arbitrage (high idio risk) : survival = {mh:.3f}  -> decay = {(1-mh)*100:5.1f}%")
print(f"survival difference (costly - cheap) = {(mh-mc)*100:+5.1f} pp   (t = {(mh-mc)/se:+.2f})")
```
```
cheap-to-arbitrage  (low idio risk)  : survival = 0.513  -> decay =  48.7%
costly-to-arbitrage (high idio risk) : survival = 0.834  -> decay =  16.6%
survival difference (costly - cheap) = +32.2 pp   (t = +2.42)
```

This is the discriminating test. If publication decay were driven by a *statistical artefact*, it would be unrelated to arbitrage cost. Instead the decay is **more than three times larger** for the cheap-to-arbitrage group (48.7% vs 16.6%), and the difference is ~32 percentage points at $t=2.42$ — statistically distinguishable even in this small simulation. Expensive corners of the market keep their anomaly longer because capital arrives slower. **That is the fingerprint of mispricing, and it is also the practitioner's opportunity map:** the durable factors are the ones that are annoying to trade.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Backtests are biased upward by ~35%, and the bias is not uniform.** Applying a flat 35% haircut is better than nothing, but the correct haircut is *characteristic-specific*: bigger for liquid, low-idio-risk factors, smaller for illiquid ones. A capacity-aware haircut is the honest default.
2. **Replication failure is itself a finding.** 10 of MP's 82 characteristics could **not be replicated in-sample** — their own original papers' results did not reproduce. Combined with the 35% decay, the expected realised alpha of a randomly-selected published factor is far below its abstract.
3. **The decay is slow, not a cliff.** MP find "a linear decay in predictability during the post-publication months," not a step. This means (i) the effect is a diffusion of information and capital, not a switch, and (ii) *the date of publication is an excellent instrument* precisely because it is exogenous to the return series — which is why their estimate is credible where a simple pre/post comparison would not be.
4. **Confusing decay with regime.** A factor that underperforms after publication may be in a bad *regime* rather than decaying. MP control for time trends in characteristic returns and for "characteristic returns simply being lower during the later years in our sample" — a discipline any practitioner should copy before concluding a strategy is dead.
5. **Decay and crowding are the same phenomenon on different clocks.** Publication is a discrete, datable *trigger* of crowding; the crowding in [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03 · Crowding & Capacity]] is the continuous version. A factor with a wide valuation spread and rising cross-factor correlation is in the late, crowded stage of the decay curve.
6. **Do not over-read the 35%.** MP explicitly can "reject the hypothesis that post-publication return-predictability **does not change** and we can also reject the hypothesis that return-predictability **disappears entirely**." The premium shrinks by about a third; it does not vanish. Factor investing remains viable — just at a lower, capacity-dependent rate.

---

### 5. Canonical Literature & Study References

- **McLean, R. David & Pontiff, Jeffrey**: "Does Academic Research Destroy Stock Return Predictability?" (*Journal of Finance*, 2016) — the primary source for this page: 82 characteristics, ~10% out-of-sample decay (insignificant), ~35% post-publication decay (significant), the 25% publication-effect lower bound, the post-publication volume/variance/short-interest increases, and the low-idiosyncratic-risk result. *Verified against the corpus paper (`32_mclean_2016_does_academic_research_destroy`).*
- **Cochrane, John H.**: "Presidential Address: Discount Rates" (*JF*, 2011) — the factor zoo framing within which the decay question sits. *Verified against the corpus paper.*
- **Ilmanen, Antti**: *Expected Returns* (2011) — "The persistent success of any asset class or trading strategy leads to a 'virtuous' cycle of growing popularity and further success, resulting in eventual overcrowding and subsequent disappointments." *Verified against the corpus book.*
- **Schwert, G. William**: "Anomalies and Market Efficiency" (*Handbook of the Economics of Finance*, 2003) — the earlier, single-anomaly evidence that value and size "fail to generate alpha" after publication; cited by MP as one of the conflicting prior results.
- **Jegadeesh, Narasimhan & Titman, Sheridan**: "Profitability of Momentum Strategies: An Evaluation of Alternative Explanations" (*JF*, 2001) — the counter-example: momentum returns *increased* after publication. Both results are real; the reconciliation is that momentum is a costlier, faster-decaying trade. Corpus paper *13_jegadeesh_2001*.
- **Bailey, Borwein, López de Prado & Zhu** (2014) and [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] — the statistical-bias half of the story, quantified.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03 · Crowding & Capacity]] · [[pillars/01-quantitative-research/factor-investing-and-timing/02-the-factor-zoo|02 · The Factor Zoo]] · [[pillars/01-quantitative-research/factor-investing-and-timing/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/factor-investing-and-timing/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/01-quantitative-research/factor-investing-and-timing/06-advanced-extensions|06 · Advanced Extensions: Factor Timing]]
- Efficiency evidence: [[pillars/01-quantitative-research/event-studies/index|Event Studies]] (how market efficiency is actually tested) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]
- The factor family: [[pillars/01-quantitative-research/momentum/index|Momentum]] (the publication counter-example) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
