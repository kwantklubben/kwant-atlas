---
title: "06 — Advanced Extensions: LCR, NSFR, Leverage Ratio & the Output Floor"
tags:
  - pillar-quantitative-risk
  - basel-and-regulation
  - liquidity-coverage-ratio
  - nsfr
  - leverage-ratio
  - output-floor
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|02 · Capital & RWA]] and [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]].

---

### 1. Intuition & Practical Objective

The risk-based capital ratio is necessary but not sufficient. Basel III bolts three more constraints onto it, each closing a hole the 2008 crisis exposed:

- **Liquidity Coverage Ratio (LCR)** — a **30-day survival test**: enough high-quality liquid assets to cover stressed net cash outflows for a month. Capital says "you can absorb the loss"; the LCR says "you can *pay* while you absorb it."
- **Net Stable Funding Ratio (NSFR)** — a **one-year structural funding test**: stable funding must cover illiquid assets. It stops a bank from funding long-dated assets with overnight money.
- **Leverage ratio** — a **non-risk-based backstop**: Tier 1 over *total exposure*, ignoring risk weights entirely, so that a bank cannot inflate its risk-based ratio by loading up on zero-weighted assets.
- **Output floor** — a **denominator floor**: internal-model RWA may not fall below $72.5\%$ of the standardised-approach RWA, capping the model gap ([[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05]]).

Together with the risk-based ratio these form **four constraints a bank must satisfy simultaneously**, and in practice a different one binds for different banks. Knowing *which* binds is the practitioner's craft.

---

### 2. Mathematical Ground Truth & Derivations

**Liquidity (BCBS 2013, d238; 2014, d295).**
$$
\boxed{\;\mathrm{LCR}=\frac{\text{Stock of HQLA}}{\text{Net cash outflows over 30 calendar days}}\ge100\%\;}\qquad
\boxed{\;\mathrm{NSFR}=\frac{\text{Available stable funding (ASF)}}{\text{Required stable funding (RSF)}}\ge100\%\;}
$$
HQLA is tiered (Level 1: cash/central-bank reserves/high-grade sovereigns, no haircut; Level 2A ~15%; Level 2B 25–50%), and stressed inflows are capped at $75\%$ of stressed outflows so a bank cannot net its way to a healthy ratio. ASF/RSF weight funding and assets by stability (retail deposits stable; wholesale short-term unstable; loans illiquid; HQLA liquid).

**Leverage ratio (BCBS 2010, d189).**
$$
\boxed{\;\text{Leverage ratio}=\frac{\text{Tier 1 capital}}{\text{Total exposure measure}}\ge3\%\;}
$$
This is the ratio that ignores risk weights. It exists because a bank can hold a huge book of low/zero-weighted assets (sovereigns, cash) with a fat risk-based ratio and yet be terrifyingly levered.

**Output floor (BCBS 2017, d424).**
$$
\boxed{\;\mathrm{RWA}_{\text{used}}=\max\!\big(\mathrm{RWA}_{\text{internal}},\ 72.5\%\times\mathrm{RWA}_{\text{SA}}\big)\;}
$$
phased in from $50\%$ (2022) to $72.5\%$ (1 January 2027). It is the direct legislative countermeasure to the model gap: however clever the internal model, at least $72.5\%$ of the standardised RWA counts.

> **Why four, not one.** Risk-based capital answers "is the book *risky*?"; leverage answers "is the book *big*?"; LCR answers "can you *survive a month of stress*?"; NSFR answers "is your funding *structurally sound*?" Each is blind to what the others see.

---

### 3. Computational Implementation — the four constraints + the floor

Standard library. Computes all four constraints and shows the floor biting.

```python
# 1) LCR
HQLA, net_outflows = 150.0, 130.0
print(f"LCR  = {HQLA/net_outflows*100:.1f}%  (min 100%)")
# 2) NSFR
ASF, RSF = 900.0, 850.0
print(f"NSFR = {ASF/RSF*100:.1f}%  (min 100%)")
# 3) leverage ratio
tier1, exposure = 140.0, 1750.0
print(f"leverage ratio = Tier1/exposure = {tier1/exposure*100:.2f}%  (min 3%)")
#    the leverage backstop biting a sovereign-heavy bank with a fat risk-based ratio
t1b, exp_b, rwa_b = 200.0, 10000.0, 500.0
print(f"  sovereign-heavy bank: risk-based {t1b/rwa_b*100:.0f}% but leverage {t1b/exp_b*100:.2f}% -> FAILS 3%")
# 4) output floor
cet1, rwa_int, rwa_sa, floor = 120.0, 1000.0, 1600.0, 0.725
rwa_used = max(rwa_int, floor*rwa_sa)
print(f"output floor: max({rwa_int:.0f}, {floor:.3f}*{rwa_sa:.0f}={floor*rwa_sa:.0f}) = {rwa_used:.0f}")
print(f"CET1 ratio: before floor {cet1/rwa_int*100:.2f}%  ->  after floor {cet1/rwa_used*100:.2f}%")
```
```
LCR  = 115.4%  (min 100%)
NSFR = 105.9%  (min 100%)
leverage ratio = Tier1/exposure = 8.00%  (min 3%)
  sovereign-heavy bank: risk-based 40% but leverage 2.00% -> FAILS 3%
output floor: max(1000, 0.725*1600=1160) = 1160
CET1 ratio: before floor 12.00%  ->  after floor 10.34%
```

**What the numbers say.** (i) All four constraints are met in the base case, but each has a *different* bank for which it binds first: the sovereign-heavy bank reports a **40% risk-based ratio and still fails leverage at 2.00%** — the exact hole the backstop fills. (ii) The output floor cuts a bank's apparent CET1 ratio from 12.00% to 10.34% by *adding RWA*, not by removing capital: $1.7$ points of reported strength that existed only because of the model. (iii) The binding constraint is an empirical fact about each bank, not a fixed rule — the practitioner's job is to know which.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Optimising one ratio, failing another.** A desk maximising return on risk-weighted assets will pile into low-$rw$, high-exposure assets (sovereign carry, repo) and blow the leverage ratio and the LCR. The constraints must be optimised *jointly*.
2. **LCR window-dressing.** The LCR is a point-in-time ratio; banks can flatter it around reporting dates by shortening funding or hoarding HQLA, then re-lever. Monitoring tools (maturity-mismatch metrics) exist precisely because a single ratio can be gamed.
3. **NSFR penalises the wrong business at the margin.** Very stable long-term assets (e.g. high-quality mortgages) still attract RSF, so the NSFR can push banks away from durable lending — a real design tension between stability and the supply of credit.
4. **The output floor is a blunt instrument.** It reduces RWA comparability problems but also penalises *good* internal models (that correctly measure low risk) alongside *bad* ones, and it bites hardest on low-risk, model-heavy books (e.g. mortgages). It is a backstop, not a risk measure.
5. **Four constraints ≠ one coherent objective.** They can conflict (liquidity hoarding vs lending; leverage vs low-risk assets). Regulatory "capital" is a multi-constraint feasibility problem, not a single number — the deepest practical lesson of the post-crisis framework.

---

### 5. Canonical Literature & Study References

- **BCBS** — *Basel III: The Liquidity Coverage Ratio and Liquidity Risk Monitoring Tools* (January 2013, BIS **d238**). $\mathrm{LCR}=\mathrm{HQLA}/\text{30-day net outflows}\ge100\%$, HQLA tiers, the inflow cap. *Read from the corpus PDF.*
- **BCBS** — *Basel III: The Net Stable Funding Ratio* (October 2014, BIS **d295**). $\mathrm{NSFR}=\mathrm{ASF}/\mathrm{RSF}\ge100\%$, one-year horizon, ASF/RSF weights. *Read from the corpus PDF.*
- **BCBS** — *Basel III: A Global Regulatory Framework* (2010, d189). The $3\%$ Tier 1 leverage ratio (parallel-run specification) and its rationale. *Read from the corpus PDF.*
- **BCBS** — *Basel III: Finalising Post-Crisis Reforms* (2017, d424). The revised leverage exposure measure and the output floor with its $50\%\to72.5\%$ phase-in. *Read from the corpus PDF.*
- **Brunnermeier & Pedersen** — *Market Liquidity and Funding Liquidity*, *RFS* **22**(6):2201–2238 (2009). The funding-liquidity spiral that motivated the LCR/NSFR; see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]].
- **Hull, John C.** — *Risk Management and Financial Institutions* (5th ed., 2018). The liquidity-risk and leverage chapters: LCR/NSFR mechanics and the leverage backstop. *Recommended textbook map.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Index Hub]]
- In-folder: [[pillars/04-quantitative-risk/basel-and-regulation/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|02 · Capital & RWA]] · [[pillars/04-quantitative-risk/basel-and-regulation/03-market-risk-and-frtb|03 · Market Risk & FRTB]] · [[pillars/04-quantitative-risk/basel-and-regulation/04-credit-and-operational-risk|04 · Credit & Operational Risk]]
- Sibling: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Risk Constraints & Mean–Variance]] (capital as an optimisation constraint)
