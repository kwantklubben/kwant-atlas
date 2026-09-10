---
title: "06 — Advanced Extensions: Macro Stress Testing & Supervisory Stress Tests (CCAR, EBA, FRTB)"
tags:
  - pillar-quantitative-risk
  - stress-testing-and-scenario-analysis
  - macro-stress-testing
  - supervisory-stress-tests
  - ccar
  - frtb
  - stressed-expected-shortfall
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]] (default/loss modelling).

---

### 1. Intuition & Practical Objective

The firm-level stress tests of 01–05 treat the portfolio as a black box and shock *market* factors. **Macro (system-wide) stress testing** takes the view up a level: it shocks *macroeconomic variables* (GDP, unemployment, house prices, rates) and projects their effect through to *credit losses and capital ratios* — because the catastrophic scenarios are the ones that are *macro-driven*, not just market-driven. **Supervisory stress tests** (CCAR/DFAST in the US, EBA in Europe) are the regulators running exactly this on banks, in public, and setting capital from the results.

The objective: understand how a single macro shock — say, the 2025 CCAR severely-adverse scenario, unemployment +5.9pp to 10% and real GDP −7.8% — flows through a loan book into PDs, expected losses, and finally into whether a bank's **post-stress capital ratio stays above the regulatory minimum**. And, on the market-risk side, how the FRTB's **stressed Expected Shortfall** operationalizes "capital against the stress period, not the current period."

Three ideas, in one line each:

1. **Macro-to-loss linkage.** You need a *model* that maps $\Delta \text{GDP}, \Delta u$ to probabilities of default and loss given default; the stress shock enters at the top (macro) and exits at the bottom (capital ratio).
2. **Capital adequacy is the object.** A stress test is not "how much do we lose" but "does post-stress capital breach the minimum?" — the binding supervisory question since 2008.
3. **Stressed ES is the market-risk analogue.** FRTB requires the ES to be *re-calibrated to a 12-month stress period* (back to 2007), not the current window — regulatory codification of everything 02 argued about "calibrated to the wrong regime."

> **The one-sentence essence.** "Macro stress testing turns a top-down economic scenario into a bottom-up capital ratio — and because firms would not stress themselves hard enough, supervisors now pick the scenario and publish the result."

---

### 2. Mathematical Ground Truth & Derivations

**Macro→credit-loss linkage.** Let a loan book have exposure-at-default $\text{EAD}$, loss-given-default $\text{LGD}$, and a base probability of default $\text{PD}_0$. Map the macro scenario to a stressed PD via an exponential/exponential-logit factor model:

$$\text{PD}_{stress}=\text{PD}_0\,\exp\big(a\,\Delta u + b\,|\Delta g|\big),$$

where $\Delta u$ is the unemployment-rate *increase* (percentage points) and $\Delta g$ the GDP *decline* (%). Expected credit loss is then

$$\text{EL}=\text{PD}_{stress}\times\text{LGD}\times\text{EAD}.$$

Adding any market/trading loss $\text{L}_{mkt}$ gives total loss $\text{L}_{tot}=\text{EL}+\text{L}_{mkt}$, and post-stress capital and capital ratio follow:

$$\text{CET1}_{post}=\text{CET1}_0-\text{L}_{tot}, \qquad \text{CET1 ratio}_{post}=\frac{\text{CET1}_{post}}{\text{RWA}}.$$

The bank "fails" if the post-stress ratio drops below the regulatory minimum (e.g. 4.5% CET1) — the entire point of the supervisory exercise. (This is the structure behind CCAR/DFAST: the Fed publishes the macro scenario, banks project the losses, and the Fed compares projected capital ratios against thresholds. Schuermann 2014.)

**FRTB stressed Expected Shortfall.** Under the Internal Models Approach, the market-risk capital measure is a stressed ES, computed from a reduced set of risk factors $R$ over the most severe 12-month period of stress (back to 2007), then scaled by the ratio of full-factor to reduced-factor current ES (floored at 1) (FRTB §33.6):

$$\mathrm{ES}=\mathrm{ES}_{R,S}\times\frac{\mathrm{ES}_{F,C}}{\mathrm{ES}_{R,C}}, \qquad \frac{\mathrm{ES}_{F,C}}{\mathrm{ES}_{R,C}}\ge 1,$$

with ES at a 97.5% one-tailed confidence, daily, and liquidity-horizon-scaled (10–120 days, §33.4). The reduced factor set must explain **≥75%** of the full-model ES variation (§33.5). The math is the *same* stressed-ES machinery as [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & ES]] — the difference is *which window* the ES is calibrated to: the stress period, not the current one.

---

### 3. Computational Implementation — macro stress: does capital breach?

Stdlib only. A $10B loan book (RWA $8B, CET1 $1.0B, base PD 1.2%, LGD 45%) plus a $200M trading equity book, run under the baseline and the CCAR-style severely-adverse scenario (unemployment +5.9pp, real GDP −7.8%, equity −50%).

```python
import math
EAD, RWA, CET1 = 10e9, 8e9, 1.0e9
PD0, LGD = 0.012, 0.45
EQ_BOOK = 200e6

def macro_loss(dU, dGDP, eq_move):
    pd  = PD0*math.exp(0.25*dU + 0.12*abs(dGDP))      # macro -> stressed PD
    el  = pd*LGD*EAD                                   # credit expected loss
    tl  = el + max(-eq_move*EQ_BOOK, 0.0)              # + trading loss on equity book
    post = CET1 - tl
    return pd, el, tl, post, post/RWA

print("scenario                 PD      EL       tot-loss  post-CET1  ratio")
for tag,dU,dGDP,eq in (("Baseline",0.0,1.0,-0.03),
                       ("Severely adverse",5.9,-7.8,-0.50)):
    pd,el,tl,post,ratio = macro_loss(dU,dGDP,eq)
    print(f"{tag:20s}  {pd*100:4.1f}%  {el/1e9:.2f}B$  {tl/1e9:.2f}B$    {post/1e9:.2f}B$     {ratio*100:5.2f}%")
print("Regulatory minimum CET1 ratio: 4.5%")
```
```
scenario                 PD      EL       tot-loss  post-CET1  ratio
Baseline               1.4%  0.06B$  0.07B$    0.93B$     11.66%
Severely adverse      13.4%  0.60B$  0.70B$    0.30B$      3.73%
Regulatory minimum CET1 ratio: 4.5%
```
The severely-adverse scenario pushes the macro-driven PD from 1.4% to 13.4%, producing $0.70B of total loss that drives post-stress CET1 to $0.30B — a **3.73% ratio, below the 4.5% minimum. The bank fails the stress test.** Note the market leg (equity −50%) is the *small* part; the *macro-to-credit* linkage is what breaks capital. This is why supervisors insist on macro scenarios: the killer is credit losses, invisible to a market-only factor stress.

**FRTB stressed ES, worked numerically.** If the stress-period reduced-factor ES is $\mathrm{ES}_{R,S}=100$, the current full-factor ES $\mathrm{ES}_{F,C}=120$, and the current reduced-factor ES $\mathrm{ES}_{R,C}=90$, then $\mathrm{ES}=100\times\tfrac{120}{90}=133.3$. The ratio $120/90=1.33>1$ exceeds the floor of 1, so the full-factor ES's richer risk coverage *raises* the capital charge above the raw stressed ES — the scaling ensures the reduced-factor stress period is not artificially cheapened.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Model risk in the macro→PD link.** The exponential map is a *model* with its own error; a wrong slope $a,b$ (calibrated on a benign sample) understates exactly the deep-recession PDs the stress is meant to capture. This is **model risk** (the risk that a model is wrong in an unmeasurable way) compounded by stress: the map is extrapolated into a regime it never observed.
2. **Reverse-causality / feedback loops.** A macro stress that lowers capital can itself trigger deleveraging, fire-sales, and further macro decline (the Brunnermeier–Pedersen loss/funding spiral; [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk]]). Most bank-level stress tests are *static* (no feedback), so they understate the second round. Supervisors partially compensate with system-wide exercises (e.g. the 2009 SCAP, EBA EU-wide tests).
3. **Stressed-ES window selection.** FRTB lets the bank pick the 12-month stress period, subject to the reduced-set ≥75% variation rule; different windows give different ES. Window- and reduced-set *choice* is itself a scenario-selection-bias form of model risk — the regulator constrains it but cannot eliminate it.
4. **Severity ratchet and gaming.** Because post-stress capital determines payouts, banks have incentive to build models that make stress losses look small (a governance failure, not a math one). This is precisely why CCAR/DFAST *run* the models in parallel and impose capital *floors* — the structure exists to counteract the bias that BIS 2009 documented.

---

### 5. Canonical Literature & Study References

- **Federal Reserve**: *2025 Stress Test Scenarios* (CCAR/DFAST) — the severely-adverse scenario used above: unemployment +5.9pp to a 10% peak, real GDP −7.8%, equity −50%, house prices −33%, CRE −30%, VIX peak 65; global market shock + counterparty-default components. *Primary source, directly verified.*
- **BCBS (BIS)**, *Minimum Capital Requirements for Market Risk* (FRTB, 2019, d457) — §33: stressed ES @97.5%, stress-period calibration back to 2007, reduced-factor-set ≥75% rule, liquidity-horizon scaling 10–120 days. *Primary source, directly verified.*
- **Schuermann**, *Stress Testing Banks*, *IJCB* 10(2) (2014) — comparative analysis of SCAP, CCAR, and EBA exercises; design, disclosure, and the geography problem.
- **Quagliariello (ed.)**, *Stress-testing the Banking System* (2009); **Bellini**, *Stress Testing and Risk Integration in Banks* (2016) — macro and bank-level methodology handbooks.
- **Brunnermeier & Pedersen (2009)**, **Brunnermeier (2009)** — the funding-spiral mechanics that static bank stress tests omit.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]] (the default/loss modelling under the macro PD) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (ES, ESF/ESR scaling) · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] (the feedback loop)
- Forward: [[pillars/04-quantitative-risk/index|Pillar 4 · Quantitative Risk]] (capital & model-risk layers that stress feeds into) · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk]] (the funding feedback a macro loss triggers)
