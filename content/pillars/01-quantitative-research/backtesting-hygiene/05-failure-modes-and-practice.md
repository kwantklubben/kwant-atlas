---
title: "1.2.5 Failure Modes & Real-World Practice"
tags:
  - pillar-quant-research
  - backtesting-hygiene
  - failure-modes
  - transaction-costs
  - protocol
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04 · The Deflated Sharpe Ratio]] and [[pillars/01-quantitative-research/backtesting-hygiene/02-why-backtests-lie|02 · Why Backtests Lie]].

---

### 1. Intuition & Practical Objective

Pages 01–04 named the *diseases*; this page is the **clinic**. The objective: a concrete, ordered protocol that a researcher runs before a backtest is allowed to influence a capital decision — and a numbered catalogue of the ways otherwise-good analyses fail. The discipline is not cynicism; it is knowing *exactly* where the number is soft so the residual can be measured and gated.

The theme of every failure mode: **a forgiving assumption applied at a place where the analyst benefits from the forgiveness.** Costs are assumed zero where they bite; $N$ is undercounted where it inflates; the sample is chosen after the outcome. Each is a first-principles violation of an exchangeability or an accounting identity, not a matter of taste.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Sharpe cost drag (why a few basis points flip a verdict)

If the strategy turns over fraction $\tau$ of its book **per year** and faces round-trip cost $c$ (proportional spread + fees), the annual cost drag is $\tau c$, so the net Sharpe is
$$
\widehat{SR}_{\text{net}}=\widehat{SR}_{\text{gross}}-\frac{\tau c}{\sigma_{\text{ann}}}\quad\text{(annualized, } \sigma_{\text{ann}}\text{ as annual vol).}
$$
The **drag scales as $\tau/\sigma_{\text{ann}}$**: high-frequency, low-vol strategies are crushed by costs that are irrelevant to slow, high-vol ones. This is *not* a modelling nicety — it is the single most common reason a Sharpe-2.0 backtest becomes a Sharpe-0.7 live strategy. Market impact adds a **square-root** term $\propto (\text{size}/\text{ADV})^{1/2}$ that makes the drag size-dependent (Almgren–Chriss); a flat "5 bps" assumption is itself a failure mode.

#### 2.2 Effective $N$ and the non-independence trap

Trials produced by tweaking one base signal are correlated; the selection threshold uses $\widehat N\approx\widehat\rho(M-1)+1$ (page 03). Reporting the raw sweep $M$ without $\widehat\rho$ is uninterpretable in both directions. **Guideline:** report the full sweep $M$, an estimated average correlation $\widehat\rho$, and the implied $\widehat N$.

#### 2.3 The decision gate

A defensible gate combines three independent corrections, all of which must pass:
$$
\underbrace{\text{DSR}\ge0.95}_{\text{selection bias + non-normality}}\ \wedge\ \underbrace{\widehat{SR}_{\text{net}}>0\ \text{after full costs}}_{\text{accounting}}\ \wedge\ \underbrace{T\ge\text{MinTRL}}_{\text{sample sufficiency}}\ \wedge\ \underbrace{\text{PBO}\ll0.5\ (\text{e.g.}\le0.05)}_{\text{selection robustness (page 06).}}
$$
Note the recursion: computing DSR needs $N$, which needs the search to have been *logged* — so the protocol must be enforced **during** research, not audited after.

#### 2.4 The order of operations (hygiene checklist)

1. **Pre-register** the hypothesis and the *plan* for the search; log every configuration (this fixes $\widehat N$).
2. **Point-in-time everything** — universe, fundamentals, prices, index membership.
3. **Split** by time (never randomly) into IS/tuning and a **vaulted** OOS, used *once*.
4. **Model costs** fully: spread, fees, borrow, and size-dependent impact, calibrated to *your* turnover.
5. **Compute** $\widehat{SR}_{\text{net}}$, skew, kurtosis, $\widehat N$, $V[\{\widehat{SR}_n\}]$.
6. **Gate** on DSR, MinTRL, and PBO; report all three.
7. **Freeze** the chosen configuration; any post-hoc change **resets** the OOS — the vault is spent.

---

### 3. Computational Implementation — when costs kill the strategy

A 5-year, high-turnover strategy with a **true gross annual Sharpe of 2.0**, found among $N{=}20$ trials. We apply proportional costs and recompute both the net Sharpe and the DSR (trial-SR dispersion 0.5 annualized). Stdlib only.

```python
import math, random
from statistics import NormalDist
Z, Zi = NormalDist().cdf, NormalDist().inv_cdf
g, ann = 0.5772156649, 252.0

def expected_max_sr(N):
    if N <= 1: return 0.0
    return (1-g)*Zi(1-1.0/N) + g*Zi(1-1.0/(N*math.e))

def moments(xs):
    n=len(xs); m=sum(xs)/n
    m2=sum((x-m)**2 for x in xs)/(n-1)
    m3=sum((x-m)**3 for x in xs)/n; m4=sum((x-m)**4 for x in xs)/n
    sd=math.sqrt(m2)
    return m, sd, m3/sd**3, m4/sd**4

def dsr_from_returns(r, N, trial_sd_ann=0.5):
    m, sd, sk, ku = moments(r)
    sr = m/sd                                   # non-annualized
    sr0 = math.sqrt(trial_sd_ann**2/ann)*expected_max_sr(N)
    den = math.sqrt(1 - sk*sr + ((ku-1)/4.0)*sr**2)
    return sr*math.sqrt(ann), Z((sr-sr0)*math.sqrt(len(r)-1)/den)

random.seed(21)
T=1260; sd_ann=0.15; mu_ann=2.0*sd_ann         # target annual Sharpe 2.0
mu_d, sd_d = mu_ann/ann, sd_ann/math.sqrt(ann)
raw=[random.gauss(mu_d,sd_d) if random.random()>0.05 else random.gauss(mu_d-6*sd_d,sd_d*3) for _ in range(T)]
m0=sum(raw)/T; s0=math.sqrt(sum((x-m0)**2 for x in raw)/(T-1))
gross=[mu_d + (x-m0)/s0*sd_d for x in raw]     # standardize -> exact gross Sharpe
turnover=1.0                                   # 100%/day turnover
gm,gsd,gsk,gku = moments(gross)
print(f"gross annual Sharpe = {gm/gsd*math.sqrt(ann):.2f}  (turnover={turnover*100:.0f}%/day, N=20, trial-SR sd=0.5)\n")
for bps in (0.0, 1.0, 2.0, 3.0, 5.0):
    net=[r-turnover*bps/10000.0 for r in gross]
    sr,dsr = dsr_from_returns(net, 20)
    print(f"cost={bps:4.1f} bps: net annual Sharpe={sr:+.2f}  DSR={dsr:.4f}  {'PASS' if dsr>=0.95 else 'FAIL'}")
```
```
gross annual Sharpe = 2.00  (turnover=100%/day, N=20, trial-SR sd=0.5)

cost= 0.0 bps: net annual Sharpe=+2.00  DSR=0.9752  PASS
cost= 1.0 bps: net annual Sharpe=+1.83  DSR=0.9529  PASS
cost= 2.0 bps: net annual Sharpe=+1.66  DSR=0.9154  FAIL
cost= 3.0 bps: net annual Sharpe=+1.50  DSR=0.8569  FAIL
cost= 5.0 bps: net annual Sharpe=+1.16  DSR=0.6635  FAIL
```
A gate that **passes at zero cost fails at 2 bps** — a cost level no high-turnover strategy can honestly assume away. The lesson is not "costs bad"; it is that **selection-bias correction and cost accounting are not independent filters** — a corrected Sharpe and an uncorrected one live on opposite sides of the threshold, and both must be computed at the same point in the protocol.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **The missing $N$ (selection bias).** A backtest without the trial count is uninterpretable (Bailey & López de Prado). *First principle:* the reported statistic is a maximum, which has no meaning without the number of draws.
2. **Transaction-cost amnesia.** Assuming zero or fixed-dollar costs rather than proportional spread + quadratic impact. *Symptom:* live Sharpe collapses and is **negative at the assumed turnover**; the drag scales as $\tau/\sigma_{\text{ann}}$.
3. **Repeated holdout.** Using the "out-of-sample" set for many rounds of selection turns 5% false positives into *expected* ones (~20 applications). *Fix:* one vaulted use.
4. **Survivorship / point-in-time failure.** Backtesting today's constituents; using restated data. *First principle:* membership required past success — a selection filter baked into the sample.
5. **Look-ahead via vintages.** Fundamentals, index adds/drops, or vendor-adjusted prices known only later. *Symptom:* unnaturally smooth equity curves.
6. **Effective-$N$ blindness.** Treating 1,000 correlated variants as 1,000 independent bets (or as one). Report $M$, $\widehat\rho$, and $\widehat N$.
7. **Non-normality ignored.** Quoting Sharpe for a negatively-skewed, fat-tailed stream (carry, option-selling) whose true standard error is far larger — DSR's denominator exists precisely for this.
8. **Capacity & alpha-decay blindness.** A strategy can be statistically real yet too small to matter or decayed by the time it is deployed; neither DSR nor PBO knows about capacity.
9. **Metric gaming.** Sharpe on illiquid mark-to-model returns, or on smoothed series, understates variance and inflates the ratio — a data-quality door, not a statistics door.
10. **Publishing bias in the literature itself.** The documented "anomalies" you mine for ideas are the survivors of *other people's* searches; their prior inflation is inherited, not reset (White 2000; Harvey, Liu & Zhu's "most claimed findings are likely false").

---

### 5. Canonical Literature & Study References

- **Bailey, D. H. & López de Prado, M.**: *The Deflated Sharpe Ratio* (2014) — §"When should we stop testing?" and the selection-bias taxonomy (file-drawer, publication, survivorship, backfill).
- **Harvey, C. R. & Liu, Y.**: *Backtesting*, JPM (2015) — the haircut framework and its caveats (non-normal returns, risk-adjustment, choice of significance level, choice of method, number of tests).
- **Harvey, C. R., Liu, Y. & Zhu, H.**: *… and the Cross-Section of Expected Returns*, RFS 29(1) (2016) — the 316-factor zoo and the case for $t>3$ thresholds after multiple-testing adjustment.
- **Almgren, R. & Chriss, N.**: *Optimal Execution of Portfolio Transactions*, Journal of Risk (2001) — the market-impact cost model behind the $\tau c$ drag, in its size-dependent form.
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed.), §7.10.2 — the wrong-vs-right cross-validation demonstration (screening outside folds gives CV error $3\%$ vs true $50\%$).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04 · Deflated Sharpe]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|06 · Purged CV, PBO & Reality Check]]
- Siblings: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (triple-barrier labels determine the purge width) · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]] (turnover-heavy, cost-sensitive)
- Cross-pillar: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
