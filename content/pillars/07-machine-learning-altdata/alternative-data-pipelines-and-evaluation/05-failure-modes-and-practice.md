---
title: "05 — Failure Modes & Practice: Backfill, Survivorship, Panel Bias, Compliance"
tags:
  - pillar-machine-learning
  - alternative-data-pipelines-and-evaluation
  - failure-modes
  - backfill-bias
  - survivorship-bias
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/03-the-pipeline|03 · The Pipeline]] and [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/04-evaluating-signal|04 · Evaluating Signal]].

---

### 1. Intuition & Practical Objective

Every alt-dataset is a **survivor of its own history**, and a naive backtest inherits the future as if it were the past. This page quantifies the four ways alt-data lies to a backtest — **backfill bias, survivorship bias, panel/coverage drift, and look-ahead** — each tied to a first principle and each turned into a *number* rather than a warning. It is the defense layer that makes the pipeline of page 03 and the protocol of page 04 trustworthy.

The deepest principle is the same one [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|Data Sources · 05]] states for fundamentals: **a dataset is a function of when you looked at it.** Today's vendor database $\mathcal{D}(t_{\text{now}})$ encodes every backfilled value, deleted entity, and restated number since inception. A backtest that reads $\mathcal{D}(t_{\text{now}})$ for a decision made at $t<t_{\text{now}}$ is not imprecise — it is **reading information flow from the future**, and the resulting performance measures the leak, not the strategy.

---

### 2. Mathematical Ground Truth & Derivations

**Backfill bias.** A vendor assigns missing early history a value that was unknown at the time ("backfilling"), or overwrites it with a later correction ("reinstatement") — AFML §2.2.1. Let the as-originally-known value be $x^{\text{pit}}_{t}$ and the backfilled value $x^{\text{bf}}_{t}=x^{\text{pit}}_{t}+c_{t}$, where the correction $c_t$ is *informed* by the outcome $y_t$ (that is what a correction is). Then

$$
\text{IC}_{\text{bf}}=\operatorname{corr}(x^{\text{pit}}+c,\,y)>\operatorname{corr}(x^{\text{pit}},\,y)=\text{IC}_{\text{pit}}\qquad\text{because } \operatorname{cov}(c,y)>0.
$$

**The inflation is largest in the oldest data** — exactly where backfill is strongest and where a long backtest "proves" the signal.

**Survivorship bias.** Let the true universe average be over all entities that existed at $t$, $\bar r=\frac1N\sum_{i=1}^N r_i$, and the vendor universe average be over today's survivors, $\bar r_{\text{surv}}=\frac1M\sum_{i\in\text{live}} r_i$ with $M<N$:

$$
\text{Bias}_{\text{surv}}=\bar r_{\text{surv}}-\bar r>0,
$$

strictly positive because the delisted firms are, on average, the losers. For alt-data this bites *twice*: the entity universe may be survivor-filtered, and **the panel itself** (which stores a vendor covers) is survivor-selected.

**Panel / coverage drift.** A card panel's observed spend is $S^{\text{obs}}_t = \alpha_t\,S^{\text{true}}_t$ where $\alpha_t$ = the panel's *coverage share*. If an issuing bank leaves at $t^\star$, $\alpha$ drops discontinuously yet $S^{\text{true}}$ is unchanged, so the signal reads

$$
\frac{S^{\text{obs}}_{t^\star+1}}{S^{\text{obs}}_{t^\star}}=\frac{\alpha_{t^\star+1}}{\alpha_{t^\star}}\approx0.7 \;(\text{a fake }-30\%\text{ "collapse"}),
$$

i.e. **vendor attrition masquerades as a demand shock** — and it is the single most famous alt-data false signal. The fix: model the *share* (relative to a control) or normalize by panel size each period.

**Look-ahead (restated once more, because it is the most common).** Using $t_E$ instead of $t_K$ (page 03) or the *final* restated value at its first release date both inject future information; the resulting IC is inflated by exactly the leaked covariance.

---

### 3. Computational Implementation — the two headline biases in numbers

numpy only. **Part A** injects a realistic backfill (early values revised toward the outcome) and measures the IC inflation; **Part B** simulates a firm universe where weak firms delist and measures the survivorship bias in the mean return.

```python
import numpy as np

rng = np.random.default_rng(3)

# ============ (A) BACKFILL BIAS ============
n = 500
x_pit = rng.normal(size=n)
recency = np.linspace(0, 1, n)                 # 0 = oldest, 1 = newest
y = 0.6*x_pit + rng.normal(size=n)
x_final = x_pit + 0.5*(1 - recency)*y + rng.normal(0, 0.2, n)  # backfill toward y

def corr(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a*b).sum()/np.sqrt((a**2).sum()*(b**2).sum()))

print("(A) BACKFILL BIAS")
print(f"  IC using point-in-time values  = {corr(x_pit, y):+.4f}")
print(f"  IC using backfilled/restated   = {corr(x_final, y):+.4f}")
print(f"  inflation (backfill leak)      = {corr(x_final,y)-corr(x_pit,y):+.4f}")
old = slice(0, n//2)
print(f"  old half: PIT={corr(x_pit[old],y[old]):+.4f}  backfilled={corr(x_final[old],y[old]):+.4f}"
      f"  gap={corr(x_final[old],y[old])-corr(x_pit[old],y[old]):+.4f}")

# ============ (B) SURVIVORSHIP BIAS ============
N, Y = 400, 10
# 25% of firms are chronically weak (mean -8%/yr); rest are healthy (+8%/yr)
weak = rng.random(N) < 0.25
mean_r = np.where(weak, -0.08, 0.08)
rets = mean_r[:, None] + rng.normal(0, 0.25, (N, Y))     # firm x year returns
# weaker firms are likelier to delist each year (absorbed/bankrupt)
delisted_year = np.full(N, Y, dtype=int)
alive = np.ones(N, dtype=bool)
for t in range(Y):
    cum = rets[:, :t+1].sum(axis=1)                       # cumulative so far
    p_die = np.clip(-cum * 0.8, 0.0, 0.9)                 # bad firms die
    die = alive & (rng.random(N) < p_die)
    delisted_year[die] = t
    alive = alive & ~die

# honest universe average: mean over all firm-years while each firm was alive
mask_alive = np.arange(Y)[None, :] < delisted_year[:, None]
all_firm_mean = rets[mask_alive].mean()
# survivor-only universe: firms still alive at the END, averaged over all years
final_alive = np.arange(Y) == Y-1                    # (Y,) -> the last year
surv_mask = mask_alive & final_alive[None, :]        # keep final survivors, all years
survivor_mean = rets[surv_mask].mean()

print("\n(B) SURVIVORSHIP BIAS")
print(f"  firms delisted over {Y} years: {int((delisted_year<Y).sum())}/{N}")
print(f"  true all-firm mean annual return = {all_firm_mean*100:+.2f}%")
print(f"  survivor-only mean annual return = {survivor_mean*100:+.2f}%")
print(f"  survivorship bias                = {(survivor_mean-all_firm_mean)*100:+.2f}% / yr")
```
```
(A) BACKFILL BIAS
  IC using point-in-time values  = +0.4509
  IC using backfilled/restated   = +0.6069
  inflation (backfill leak)      = +0.1561
  old half: PIT=+0.4454  backfilled=+0.6766  gap=+0.2313

(B) SURVIVORSHIP BIAS
  firms delisted over 10 years: 176/400
  true all-firm mean annual return = +6.43%
  survivor-only mean annual return = +9.38%
  survivorship bias                = +2.95% / yr
```

Read both. **Backfill** lifts the measured IC from $+0.4509$ to $+0.6069$ — a $+0.1561$ inflation — and the gap is nearly **50% larger in the old half** ($+0.2313$ vs $+0.1561$ overall), exactly where a long backtest finds its "evidence." **Survivorship** adds **+2.95%/yr** of phantom return: the true universe earned $+6.43\%$ but today's survivors earned $+9.38\%$, so a backtest on the survivor universe manufactures almost half again the true return out of nothing. Both biases are pure bookkeeping errors — and both flatter the strategy at precisely the moments you would have gotten killed live.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Backfill & reinstatement time-travel (AFML §2.2.1).** Vendors overwrite history with corrections; storing only the latest value changes your past whenever you re-run. Keep multiple knowledge-dated versions; forbid backwards edits.
2. **Survivorship, in the universe *and* the panel.** Delisted names and dropped panel members are the losers; excluding them is not "clean data," it is a selection on the outcome. Quantified above at $+2.95\%$/yr.
3. **Panel / coverage drift read as demand.** Vendor attrition ($\alpha_t$ changing) fakes a $-30\%$ collapse overnight. Model *share* or normalize by panel size; never trust a level you didn't coverage-adjust.
4. **Look-ahead by event-time tagging.** The $t_K$ vs $t_E$ mistake (page 03) is the most common of all; it silently doubles an IC. Testable before any modelling.
5. **Overfitting the evaluation.** Searching $K$ datasets and reporting the best $t$-stat ignores that the winner is selected on noise; deflate for $K$ (deflated Sharpe / PBO). The evaluation is a search and must be corrected like one.
6. **Compliance / MNPI.** Ingesting web-scraped data that violates ToS, or a feed that embeds material non-public information (e.g. an unresolved earnings number inferred from a leaked transcript), exposes the fund to insider-trading liability. *First principle:* alt-data must be built from **public or properly-licensed** primary sources; "we found it on the web" is not a legal basis for trading it.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning* — **§2.2.1** (backfilled/reinstated values; the period-end indexing error), **Ch. 11** (backtest errors, quoting Luo et al.'s "Seven Sins": survivorship, look-ahead, storytelling, data snooping, transactions costs...). *Corpus PDF verified.*
- **Luo, Yin et al.**: "Seven Sins of Quantitative Investing" (Deutsche Bank, 2014) — the practical failure checklist this page quantifies.
- **Bailey, López de Prado, et al.**: "The Probability of Backtest Overfitting" and "The Deflated Sharpe Ratio" — the multiple-testing corrections that make "overfitting the evaluation" a *number*.
- **Guida, Tony**, *Big Data and Machine Learning in Quantitative Investment* (Wiley, 2019) — panel construction, coverage, and vendor due diligence in practice.
- **In-repo companion:** [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|Data Sources · 05 Failure Modes & Practice]] — the same biases derived for fundamentals; read side by side.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/04-evaluating-signal|04 · Evaluating Signal]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling failure analysis: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]]
- Provenance discipline: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
