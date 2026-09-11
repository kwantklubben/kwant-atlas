---
title: "02 — Physical vs Transition Risk: Carbon Pricing, Pass-Through & Stranded Assets"
tags:
  - pillar-quantitative-risk
  - climate-and-esg-risk
  - transition-risk
  - physical-risk
  - carbon-pricing
  - stranded-assets
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · From Zero]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

The TCFD's central contribution was taxonomic: it split climate-related financial risk into **physical risk** and **transition risk**, and insisted both are *financial* risks that belong in the ordinary risk process. This page makes that taxonomy operational: how to turn a warming path into a physical drag, how to turn a carbon price into a portfolio P&L, and how to decide when an asset is **stranded**.

The two families behave very differently, and the difference drives every modelling choice:

- **Physical risk** is a *damage* process. **Acute** events (floods, storms, wildfires) are tail-like, local and insurable-ish; **chronic** shifts (mean temperature, precipitation, sea level) are slow, cumulative and effectively uninsurable. Physical risk is measured from climate (not financial) data and enters the P&L as a damage function or a scenario haircut.
- **Transition risk** is a *policy and technology* process. It is a **repricing** of an asset's cash flows when a carbon price, a mandate, or a substitute technology arrives — fast (disorderly) or slow (orderly). Transition risk is measured from emissions and policy data and enters the P&L as a **cost per tonne** (or an abatement-cost curve).

The bridge between them is the **carbon price**. An explicit price is charged (emissions trading systems, carbon taxes). A **shadow (internal) carbon price** is *not* charged — it is inserted into project appraisal so that long-lived assets are sized for a future price that may become explicit. Corporate and public practice both use shadow prices precisely because the explicit price is a *political* variable, not a market observable with a long history.

**Stranding** is the terminal case of transition risk: a capital asset whose operating cost exceeds its revenue at the prevailing (or expected) carbon price, before the end of its useful life. It is not a peak-oil story or a moral judgement — it is the arithmetic $p^*=m/\mathrm{EF}$ of §2 applied to a whole reserve or plant base.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The TCFD taxonomy as a decomposition

A firm's value is exposed to climate through two channels only (TCFD, 2017, Figure 1):

$$\underbrace{\Delta V/V_{\text{physical}}}_{\text{damage}\ \to\ \text{assets, costs, revenue}}\quad+\quad\underbrace{\Delta V/V_{\text{transition}}}_{\text{policy, tech, preference}\ \to\ \text{costs, demand, valuation}}.$$

Both are ultimately cash-flow shocks; both are **cumulative and non-stationary**, which is why neither can be mimicked by adding a stationary risk factor to a return model ([[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · §4]]).

#### 2.2 Carbon pricing: explicit price, shadow price, pass-through

Let a firm emit $E_i$ tCO2e on revenue $R_i$, so its intensity is $I_i=E_i/R_i$. A carbon price step $\Delta p$ (\$/tCO2e) creates a gross cost
$$C_i=\Delta p\cdot E_i=\Delta p\,I_i\,R_i .$$
With pass-through $\lambda_i\in[0,1]$ (the fraction the firm can put into its own selling prices), the retained cost is $(1-\lambda_i)C_i$, i.e. a margin hit of $(1-\lambda_i)I_i\Delta p$ on every unit of revenue. The **shadow carbon price** is the same formula with $\lambda=0$ and $\Delta p$ set to a policy corridor rather than a market price — the canonical external corridor being the High-Level Commission on Carbon Prices (Stern & Stiglitz, 2017): **$\$40$–$\$80$/tCO2e by 2020, $\$50$–$\$100$/tCO2e by 2030**, consistent with the Paris Agreement objective.

Pass-through is the crux and it is *heterogeneous*: a regulated utility with a cost-of-service tariff passes most of a carbon price through; a commodity chemicals producer facing import competition passes almost none. A single portfolio-level $\lambda$ is therefore a strong — and strongly consequential — assumption (hub §3: a $\$30$/t shock is $-15.33\%$ at $\lambda=0$ and $-3.07\%$ at $\lambda=0.8$).

#### 2.3 Stranded assets: the break-even carbon price

For asset $i$ with a break-even net margin $m_i$ (\$/unit of fuel) and an emission factor $\mathrm{EF}$ (tCO2e per unit of fuel), the carbon cost per unit is $\mathrm{EF}\cdot p$. The asset is **uneconomic** when
$$\boxed{\ p^*=\frac{m_i}{\mathrm{EF}}\quad\text{equivalently}\quad \mathrm{EF}\cdot p>m_i\ }$$
so for a reserve base $\{(v_i,m_i)\}$ the **stranded fraction** at carbon price $p$ is
$$\mathrm{SF}(p)=\frac{\sum_{i:\,m_i<\mathrm{EF}\,p} v_i}{\sum_i v_i}.$$
$\mathrm{SF}$ is a *cumulative distribution function of break-even margins*, rescaled — the classic "cost curve" used by PACTA-style alignment tools and by Carbon Tracker's unburnable-carbon framing. It is monotone, bounded in $[0,1]$, and its derivative is the reserve density at the margin. Crucially it is **not** a probability: it is a scenario-conditional fraction.

#### 2.4 Physical risk: from cumulative emissions to damage

The physical channel has a defensible three-link chain (IPCC AR5, WG1 Ch. 12):

1. **Emissions → warming.** The *transient climate response to cumulative carbon emissions* (TCRE) is approximately linear in cumulative CO2: $\Delta T\approx \mathrm{TCRE}\times(\text{cumulative GtCO}_2/1000)$, with the AR5 *likely* range $0.8$–$2.5\,^\circ$C per 1000 PgC, i.e. $\approx0.2$–$0.7\,^\circ$C per 1000 GtCO2.
2. **Warming → damage.** Integrated-assessment damage functions are conventionally **convex** in $\Delta T$: $D(\Delta T)=\theta\,\Delta T^2$ (the DICE-family functional form). The convexity is the substantive claim: each additional degree costs more than the last.
3. **Damage → value.** $V\mapsto V\,(1-D(\Delta T))$, applied to the exposed asset base rather than the whole portfolio.

**Honest labelling.** $\mathrm{TCRE}$ is a published, assessed quantity. $\theta$ is **not** a constant of nature and not a supervised calibration; it is a *model parameter*, and the code below treats it as an explicitly illustrative value so the arithmetic is verifiable without pretending to a calibration it does not have.

---

### 3. Computational Implementation — the stranded-asset cost curve and the physical drag

Panel (A) integrates a reserve cost curve into a stranded fraction at four carbon prices and compares the book's committed emissions with the remaining carbon budget. Panel (B) applies the convex damage function. Standard library only.

```python
# c3_transition.py — stranded-asset cost curve + physical-risk drag (page 02 §3)

# (A) reserves go uneconomic when the carbon cost exceeds the break-even margin
reserves = [   # (volume, Mbbl), (break-even net margin, $/bbl)
    (500.0, 12.0), (800.0, 18.0), (1200.0, 25.0), (1500.0, 32.0),
    (1800.0, 40.0), (1500.0, 48.0), (1000.0, 55.0), (700.0, 65.0),
]
EF = 0.43                       # tCO2e per barrel of oil burned
total = sum(v for v, _ in reserves)
print(f"(A) stranded assets: {total:,.0f} Mbbl of reserves at {EF} tCO2e/bbl")
for p in (0.0, 50.0, 100.0, 150.0):
    thr = EF * p
    str_ = sum(v for v, m in reserves if m < thr)
    print(f"    carbon price ${p:5.0f}/t -> threshold ${thr:5.1f}/bbl -> {100*str_/total:5.1f}% of reserves stranded")
committed = total * 1e6 * EF / 1e9                                  # GtCO2
print(f"    burning all reserves emits {committed:.2f} GtCO2 = {100*committed/420:.2f}% of the ~420 GtCO2")
print(f"    remaining budget for a two-thirds chance of 1.5C (IPCC SR1.5, from 2018)")

# (B) chronic physical risk as a quadratic damage drag on a real-asset book
theta = 0.006                   # illustrative: value fraction lost per (degC)^2
print("(B) physical-risk drag (illustrative quadratic damage function, theta = 0.006)")
for dt in (1.5, 2.0, 3.0, 4.0):
    print(f"    warming +{dt:.1f}C -> cumulative value loss {100*theta*dt*dt:5.2f}%")
```
```
(A) stranded assets: 9,000 Mbbl of reserves at 0.43 tCO2e/bbl
    carbon price $    0/t -> threshold $  0.0/bbl ->   0.0% of reserves stranded
    carbon price $   50/t -> threshold $ 21.5/bbl ->  14.4% of reserves stranded
    carbon price $  100/t -> threshold $ 43.0/bbl ->  64.4% of reserves stranded
    carbon price $  150/t -> threshold $ 64.5/bbl ->  92.2% of reserves stranded
    burning all reserves emits 3.87 GtCO2 = 0.92% of the ~420 GtCO2
    remaining budget for a two-thirds chance of 1.5C (IPCC SR1.5, from 2018)
(B) physical-risk drag (illustrative quadratic damage function, theta = 0.006)
    warming +1.5C -> cumulative value loss  1.35%
    warming +2.0C -> cumulative value loss  2.40%
    warming +3.0C -> cumulative value loss  5.40%
    warming +4.0C -> cumulative value loss  9.60%
```

Two readings. First, the stranded fraction is **violently convex in the carbon price**: $0\%\to14.4\%\to64.4\%\to92.2\%$ across $\$0\to\$150$/t. A portfolio's "stranding risk" is therefore not a number but a *curve*, and reporting a single point on it is a hidden assumption about the policy path. Second, the physical drag at $+3^\circ$C ($5.40\%$) is the same order as the transition hit — **the two families are comparable in magnitude, and in a hot-house scenario you pay the physical one instead of the transition one, not instead of both.**

Cross-check against the earlier identity: at $p=\$100$/t the threshold is $\mathrm{EF}\cdot p=0.43\times100=\$43$/bbl, so $\$43$ separates economic from stranded reserves — which is exactly the $64.4\%$ cut in the table.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Modelling transition risk as a return factor.** A regression of returns on a carbon-price change gives a *contemporaneous* pass-through coefficient, not a stranding exposure; the stranding loss is a level shift that a short sample cannot contain ([[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · §4.1]]).
2. **A single pass-through for the whole portfolio.** $\lambda$ is firm-, sector- and jurisdiction-specific and is the most influential assumption in any carbon-price stress test (hub §3: $5\times$). Use a range and report the range.
3. **Treating the cost curve as a probability.** $\mathrm{SF}(p)$ is the fraction stranded *conditional on* $p$; it carries no probability attached to $p$. Multiplying it by a subjective scenario probability silently converts a scenario into a forecast.
4. **Ignoring the emission factor's uncertainty.** $\mathrm{EF}$ and $E_i$ come from disparate reporting regimes with different boundaries and vintages; a $\pm20\%$ error in $E_i$ is a $\pm20\%$ error in the stranding threshold $\mathrm{EF}\cdot p$ and thus moves $p^*$ materially ([[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · §2]]).
5. **Damage-function laundering.** Publishing a physical-risk number computed from a quadratic $D(\Delta T)=\theta\Delta T^2$ without disclosing $\theta$ turns a *parameter choice* into an apparent measurement. Always report $\theta$, its range, and whether damage is applied to the exposed base or the whole book.
6. **Double-counting.** Transition and physical risk are *correlated in the scenario set* (hot-house worlds have a low transition price and high physical damage; net-zero worlds the reverse), so summing independently-stressed transition and physical losses overstates the total. They must be drawn from a *single coherent scenario* ([[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · §2]]).

---

### 5. Canonical Literature & Study References

- **TCFD**, *Recommendations of the Task Force on Climate-related Financial Disclosures* (FSB, 2017), Figure 1 — the physical/transition risk taxonomy and the recommended metrics (WACI, carbon footprint). *Primary source.*
- **High-Level Commission on Carbon Prices** (Stern, N. & Stiglitz, J., chairs), *Report of the High-Level Commission on Carbon Prices* (World Bank, 2017) — the explicit shadow-price corridor ($\$40$–$\$80$ by 2020; $\$50$–$\$100$ by 2030).
- **World Bank**, *Shadow Price of Carbon in Economic Analysis — Guidance Note* (2017) — how shadow prices enter project appraisal.
- **IPCC**, *Climate Change 2013: The Physical Science Basis* (AR5, WG1 Ch. 12) — TCRE and its likely range; *Global Warming of 1.5 °C* (SR1.5, 2018, Ch. 2) — the remaining carbon budget.
- **Carbon Tracker Initiative**, *Unburnable Carbon: Are the World's Financial Markets Carrying a Carbon Bubble?* (2011) — the origin of the stranded-asset framing.
- **PACTA / RMI**, *Paris Agreement Capital Transition Assessment* methodology notes — forward-looking alignment using company production plans and sectoral pathways.
- **NGFS**, *Climate Scenarios for Central Banks and Supervisors* — the scenario-consistent pairing of transition and physical risk used in §4.6.
- **Bolton, P. & Kacperczyk, M.**, *Do investors care about carbon risk?*, *Journal of Financial Economics* 142(2):517–549 (2021) — the empirical carbon premium that prices this exposure.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · Climate Scenarios & Stress Testing]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/04-esg-scores-and-the-carbon-premium|04 · ESG Scores & the Carbon Premium]]
- Sibling: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (the Merton route from a carbon liability to a PD, extended in 06)
