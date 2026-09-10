---
title: "03 — Market Risk & FRTB: SA vs IMA, VaR → Expected Shortfall"
tags:
  - pillar-quantitative-risk
  - basel-and-regulation
  - frtb
  - expected-shortfall
  - internal-models
  - standardised-approach
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the measures being regulated) and [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] (how they are estimated).

---

### 1. Intuition & Practical Objective

Market risk is the oldest and most model-dependent corner of the capital framework. The 1996 Amendment let banks use their **own VaR models** to set capital — a radical move that made a bank's internal risk number legally binding. The 2008 crisis exposed the flaws (VaR's tail blindness, 10-day horizons too short for illiquid positions, and "backtesting pass but crisis fail"), and the **Fundamental Review of the Trading Book (FRTB, BCBS 2019)** rewrote the rules.

This page does two things. It gives the **two regimes side by side** — the 1996 VaR machinery and the FRTB ES machinery — and it shows the FRTB calculation honestly: how a base-horizon Expected Shortfall is scaled up position-by-position along **liquidity horizons**, stress-calibrated, and multiplied into a capital number.

The pivot is one substitution: **$\mathrm{VaR}_{99\%}\ \longrightarrow\ \mathrm{ES}_{97.5\%}$.** The confidence level drops to 97.5% precisely so that, under normality, the two are almost equal ($\mathrm{ES}_{97.5}/\mathrm{VaR}_{99}\approx1.005$, §3), while ES — which averages the tail — captures the *severity* VaR ignores. Everything else (liquidity horizons, stressed calibration, NMRF treatment) exists because 2008 proved a single 10-day VaR was not enough.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The 1996 regime (Basel II market risk)

Per BCBS (1996), capital is
$$\text{Capital}=\max\!\Big(\mathrm{VaR}_{t-1},\; m\cdot \tfrac1{60}\!\sum_{i=1}^{60}\mathrm{VaR}_{t-i}\Big),\qquad m\ge3,$$
with $\mathrm{VaR}$ the **99th percentile, one-tailed, 10-trading-day** measure, observation period $\ge1$ year, and $m$ **plus** an add-on of $0$–$1$ based on backtesting exceptions. RWA $=12.5\times$ capital.

#### 2.2 FRTB: standardised approach (SA)

The SA has three charges, added:
$$\text{SA}=\text{SBM}+\text{DRC}+\text{RRAO}.$$
- **SBM (sensitivities-based method):** for each risk class (GIRR, equity, FX, commodity, credit-spread), compute risk-weighted **delta**, **vega**, and **curvature** positions, aggregate within buckets then across buckets by a square-root-of-sum-of-squares correlation formula, and combine
$$\text{SBM}=\sqrt{\big(\text{delta charge}\big)^2+\big(\text{vega charge}\big)^2+\big(\text{curvature charge}\big)^2}.$$
- **DRC (default risk charge):** jump-to-default capital.
- **RRAO (residual risk add-on):** for exotic risks not captured above.

#### 2.3 FRTB: internal-models approach (IMA) — the ES engine

**(a) Confidence and base horizon (MAR33.2–33.3).** ES is computed **daily** at the **97.5th percentile**, one-tailed. The base liquidity horizon is $T=10$ days.

**(b) Liquidity-horizon scaling (MAR33.4).** ES is computed on the 10-day base and scaled per position along the prescribed liquidity horizons $LH_j\in\{10,20,40,60,120\}$ days:
$$\boxed{\;\mathrm{ES}=\sqrt{\;\mathrm{ES}_T(P)^2+\sum_{j\ge2}\Big(\mathrm{ES}_T(P,j)\cdot\sqrt{\tfrac{LH_j-LH_{j-1}}{T}}\Big)^2\;}\;}$$
where $\mathrm{ES}_T(P)$ is total portfolio ES at horizon $T$ over *all* risk factors, and $\mathrm{ES}_T(P,j)$ is ES over only the subset $Q(p_i,j)$ of risk factors with liquidity horizon $\ge LH_j$ (all others held constant). Illiquid risk factors therefore inflate capital through the later $j$ terms.

**(c) Stressed calibration (MAR33.5–33.7).** ES is calibrated to a 12-month stress period (the worst since 2007) using a reduced set of risk factors:
$$\mathrm{ES}=\mathrm{ES}_{R,S}\times\max\!\Big(1,\ \tfrac{\mathrm{ES}_{F,C}}{\mathrm{ES}_{R,C}}\Big),$$
where $R,S$ = reduced set / stressed observations, $F,C$ = full set / current observations. The ratio is **floored at 1** so stress cannot reduce capital.

**(d) Aggregation and multiplier (MAR33.15, 33.41).** The bank-wide modellable charge mixes the unconstrained and constrained (per-risk-class) ES:
$$\mathrm{IMCC}=\rho\,\mathrm{IMCC}(C)+(1-\rho)\sum_{i}\mathrm{IMCC}(C_i),\qquad \rho=0.5,$$
and the eligible-desk capital is
$$C_A=\max\!\big(\mathrm{IMCC}_{t-1}+\mathrm{SES}_{t-1},\; m_c\cdot\overline{\mathrm{IMCC}}+\overline{\mathrm{SES}}\big),\qquad m_c\ge1.5,$$
with $m_c=1.5$ plus a $0$–$0.5$ backtesting add-on, plus a separate **SES** charge for non-modellable risk factors (NMRFs), a **DRC** model (99.9%, one-year VaR), and the PLA-test surcharge for amber-zone desks. The eligible total is
$$\mathrm{IMAG}_{,A}=C_A+\mathrm{DRC},\qquad \text{then}\quad \mathrm{RWA}=12.5\times\text{capital}.$$

> **Reading the two regimes together.** 1996: capital $=3\times$ a 99%/10-day VaR. FRTB: capital $=1.5\times$ a 97.5% ES *stretched along liquidity horizons and stress-calibrated*. The multiplier looks smaller, but the horizon scaling and stress calibration more than make up for it — the model is *more* conservative where granularity is poor.

---

### 3. Computational Implementation — the ES engine and SA/IMA comparison

**Experiment 1 — liquidity-horizon ES and IMA capital.** Base horizon $T=10$; partial ES contributions at the base horizon; aggregate; stress-calibrate; multiply. Stdlib only.

```python
import math
T, LH = 10.0, [10,20,40,60,120]
ES_partial = {2:60.0, 3:40.0, 4:25.0, 5:10.0}     # ES over the LH>=j subset
ES_T_P = 100.0                                    # portfolio ES at horizon 10
terms = [ES_T_P**2]
for j in range(2,6):
    sc = math.sqrt((LH[j-1]-LH[j-2])/T)
    terms.append((ES_partial[j]*sc)**2)
    print(f"  j={j}: LH={LH[j-1]:3d}  scaling=sqrt({LH[j-1]-LH[j-2]}/10)={sc:.4f}  ES_part {ES_partial[j]:.0f} -> {ES_partial[j]*sc:6.2f}")
ES = math.sqrt(sum(terms))
print(f"ES (97.5%, liquidity-adjusted) = {ES:.4f}")

ES_RS, ES_FC, ES_RC = 110.0, 100.0, 140.0         # reduced/stressed, full/current, reduced/current
ratio = max(1.0, ES_FC/ES_RC)
print(f"stressed calibration ratio max(1,{ES_FC}/{ES_RC}) = {ratio:.4f}")
ES_cal = ES*ratio
mc = 1.5
print(f"IMA capital = m_c*ES = {mc}*{ES_cal:.4f} = {mc*ES_cal:.4f}")
print(f"RWA = 12.5 x capital = {12.5*mc*ES_cal:.2f}")
```
```
  j=2: LH= 20  scaling=sqrt(10/10)=1.0000  ES_part 60 ->  60.00
  j=3: LH= 40  scaling=sqrt(20/10)=1.4142  ES_part 40 ->  56.57
  j=4: LH= 60  scaling=sqrt(20/10)=1.4142  ES_part 25 ->  35.36
  j=5: LH=120  scaling=sqrt(60/10)=2.4495  ES_part 10 ->  24.49
ES (97.5%, liquidity-adjusted) = 136.5650
stressed calibration ratio max(1,100.0/140.0) = 1.0000
IMA capital = m_c*ES = 1.5*136.5650 = 204.8475
RWA = 12.5 x capital = 2560.59
```

**Experiment 2 — 1996 VaR vs FRTB ES, and the SA-vs-IMA gap.** A \$1bn portfolio with 2% daily volatility; then an illustrative SA SBM aggregation vs the IMA.

```python
import math
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)
z99, z975 = 2.326347874, 1.959963985
sig_d, V = 0.02, 1e9
VaR99_10 = z99 * sig_d * V * math.sqrt(10)
ES975_10 = phi(z975)/0.025 * sig_d * V * math.sqrt(10)
print(f"1996 VaR 99%/10d      = {VaR99_10:,.0f}")
print(f"FRTB ES 97.5%/10d     = {ES975_10:,.0f}   ratio ES/VaR = {ES975_10/VaR99_10:.4f}")
print(f"1996 capital (m=3)    = {3*VaR99_10:,.0f}   -> RWA {3*VaR99_10*12.5:,.0f}")
print(f"FRTB capital (mc=1.5) = {1.5*ES975_10:,.0f}   -> RWA {1.5*ES975_10*12.5:,.0f}")

# SA SBM: aggregate delta/vega/curvature per risk class by square-root-of-sum-of-squares
delta = {"IR":5e6,"EQ":3e6,"FX":2e6,"CRQ":1.5e6,"CM":1e6}
vega  = {"IR":1.2e6,"EQ":0.9e6,"FX":0.5e6,"CRQ":0.4e6,"CM":0.3e6}
curv  = {"IR":0.8e6,"EQ":0.6e6,"FX":0.0,"CRQ":0.3e6,"CM":0.2e6}
agg = lambda d: math.sqrt(sum(v*v for v in d.values()))
dR, vR, cR = agg(delta), agg(vega), agg(curv)
SBM = math.sqrt(dR**2 + vR**2 + cR**2)
DRC = 1.5e6
print(f"SA SBM delta={dR:,.0f} vega={vR:,.0f} curvature={cR:,.0f}  ->  SBM = {SBM:,.0f}")
print(f"SA total (SBM+DRC) = {SBM+DRC:,.0f}  ->  RWA {(SBM+DRC)*12.5:,.0f}")
```
```
1996 VaR 99%/10d      = 147,131,158
FRTB ES 97.5%/10d     = 147,855,631   ratio ES/VaR = 1.0049
1996 capital (m=3)    = 441,393,475   -> RWA 5,517,418,434
FRTB capital (mc=1.5) = 221,783,446   -> RWA 2,772,293,076
SA SBM delta=6,422,616 vega=1,658,312 curvature=1,063,015  ->  SBM = 6,717,887
SA total (SBM+DRC) = 8,217,887  ->  RWA 102,723,582
```

**What the numbers say.** (i) $\mathrm{ES}_{97.5}$ and $\mathrm{VaR}_{99}$ are nearly identical under normality (ratio $1.0049$) — the choice of 97.5% is exactly this calibration, not a loosening. (ii) The *multiplier* change ($3\to1.5$) bisects the capital on an identical measurement, so the added conservatism of FRTB comes from the horizon scaling and stress calibration, not the multiplier. (iii) Under our illustrative sensitivities the SA and IMA diverge sharply — the divergence is precisely why supervisors worry about which approach a desk uses, and why an output floor backstops the choice (§06).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tail blindness under VaR.** A 99% VaR is one quantile: change the worst loss from $\$3$ to $\$15$ and VaR does not move ([[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & ES]]). Replacing it with ES is the direct fix; the 97.5% level keeps the scale comparable.
2. **A 10-day VaR is too short for illiquid positions.** You cannot exit a credit or structured position in two weeks without moving the market. FRTB's liquidity-horizon scaling assigns 20–120 days by risk-factor category precisely to embed this — the $j\ge2$ terms are the illiquidity tax.
3. **Backtesting is necessary but not sufficient.** A model can pass daily backtests and still fail a crisis; the 2008 lesson drove the **PLA test** (green/amber/red desk classification), the $0$–$0.5$ backtesting add-on, and the mandatory **stress calibration**. Passing the test is a floor, not a guarantee.
4. **NMRFs are unavoidable.** Risk factors without enough real price observations cannot be modelled, so they get a punitive stress-scenario charge (SES). A book heavy in esoteric risk factors faces SA-like capital regardless of IMA approval — the granularity limit is real.
5. **Model approval is a governance gate, not a truth test.** The IMA and IRB depend on supervisory approval of the bank's *own* parameters; weak validation is a first-order source of under-capitalisation ([[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05]]).

---

### 5. Canonical Literature & Study References

- **BCBS** — *Minimum Capital Requirements for Market Risk* (January 2019, BIS **d457**, FRTB). The primary source for everything above: MAR33.4 (liquidity-horizon ES formula), MAR33.3 (97.5%), MAR33.5–33.7 (stressed calibration), MAR33.15/33.41 (aggregation, $m_c\ge1.5$), MAR32 (backtesting/PLA), MAR21 (SBM). *Read in full from the corpus PDF.*
- **BCBS** — *Amendment to the Capital Accord to Incorporate Market Risks* (1996, BIS). The 99%/10-day VaR, multiplier $\ge3$, $0$–$1$ backtesting add-on. *Read from the corpus PDF.*
- **BCBS** — *Supervisory Framework for the Use of Backtesting in Conjunction with the Internal Models Approach to Market Risk Capital Requirements* (1996). The traffic-light zones behind the add-on.
- **Nadarajah et al.** — *Sensitivities-Based Method and Expected Shortfall under FRTB* (2023, corpus PDF) and the FRTB survey literature (2015–2019) in *Journal of Risk / Quantitative Finance*. Where SBM (delta/vega/curvature) meets ES in practice.
- **Hull, John C.** — *Options, Futures, and Other Derivatives* (11th ed.), Ch 22 (VaR/ES, the 1996/Basel numbers, backtesting). *Numerically verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|02 · Capital & RWA]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Index Hub]]
- Prerequisite / sibling: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]
- Forward: [[pillars/04-quantitative-risk/basel-and-regulation/04-credit-and-operational-risk|04 · Credit & Operational Risk]] · [[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/basel-and-regulation/06-advanced-extensions|06 · Advanced Extensions]]
- Risk-factor mapping input: [[pillars/04-quantitative-risk/basel-and-regulation/03-market-risk-and-frtb|this folder · sensitivities]]
