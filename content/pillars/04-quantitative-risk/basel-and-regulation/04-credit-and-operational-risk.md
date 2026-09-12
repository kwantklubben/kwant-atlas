---
title: "4.9.4 Credit & Operational Risk"
tags:
  - pillar-quantitative-risk
  - basel-and-regulation
  - credit-risk
  - irb
  - operational-risk
  - asrf
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (PD, LGD, distance-to-default, the Vasicek one-factor model) and [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|02 · Capital & RWA]].

---

### 1. Intuition & Practical Objective

Credit risk is the largest RWA category for almost every bank; operational risk is the smallest but the one where the regulator gave up on internal models. This page covers both, and the common theme is **SA vs internal model**: the standardised approach applies regulator-set weights, while the internal approach lets the bank supply its own parameters - and the difference in capital can be enormous.

- **Credit risk.** SA weights a loan by asset class and (where available) external rating: sovereign, bank, corporate, retail, mortgage. **IRB** instead plugs the bank's own **PD**, **LGD**, **EAD**, and **M** into the **ASRF** (asymptotic single-risk-factor) closed form - the same Vasicek one-factor formula behind portfolio credit-VaR. Foundation IRB: bank supplies PD, supervisor supplies LGD/EAD. Advanced IRB: bank supplies all four.
- **Operational risk.** Basel II offered SA (Basic Indicator / Standardised) and the **AMA** (Advanced Measurement Approach), a full internal loss-distribution model. The AMA was abused (op-risk RWA fell, then losses appeared), and the **2017 finalisation removed it**, replacing everything with one **Standardised Measurement Approach (SMA)**: capital $=$ Business Indicator Component $\times$ Internal Loss Multiplier. Op risk is now the one Pillar-1 risk with *no* internal-model route.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 SA credit risk weights (BCBS 2006)

A sample of the standardised grid (exposure × weight → RWA):

| Exposure | Weight |
|---|---|
| Sovereign, AAA–AA | 0% |
| Bank, AAA–AA (or good, unrated) | 20% |
| Residential mortgage | 35% |
| Retail | 75% |
| Corporate, unrated | 100% |
| Past-due / high-risk | 150%+ |

#### 2.2 IRB credit risk - the ASRF capital formula

For a corporate/retail exposure with probability of default $\mathrm{PD}$, loss-given-default $\mathrm{LGD}$, and maturity $M$:
$$
\boxed{\;K=\underbrace{\Big[\mathrm{LGD}\cdot N\!\Big(\tfrac{N^{-1}(\mathrm{PD})+\sqrt R\,N^{-1}(0.999)}{\sqrt{1-R}}\Big)-\mathrm{PD}\cdot\mathrm{LGD}\Big]}_{\text{conditional expected loss above PD}\cdot\text{LGD}}\times\mathrm{MA}\;}
$$
with the **asset correlation**
$$
R=0.12\,\frac{1-e^{-50\,\mathrm{PD}}}{1-e^{-50}}+0.24\Big(1-\frac{1-e^{-50\,\mathrm{PD}}}{1-e^{-50}}\Big),
$$
and the **maturity adjustment** $b=(0.11852-0.05478\ln \mathrm{PD})^2$, $\ \mathrm{MA}=\dfrac{1+(M-2.5)b}{1-1.5b}$. The numerator $N^{-1}(\mathrm{PD})+\sqrt R\,N^{-1}(0.999)$ is the **Vasicek one-factor** conditional-default-probability argument at the 99.9% confidence level (Hull eq. 24.10): the $N^{-1}(0.999)$ shock is the systematic factor, $\sqrt R$ its loading. Then $\mathrm{RWA}=K\times12.5\times\mathrm{EAD}$ (and historically $\times1.06$ for the Basel II scaling factor).

#### 2.3 Operational risk - the SMA (BCBS 2017)

$$
\mathrm{ORC}=\mathrm{BIC}\times\mathrm{ILM},\qquad \mathrm{RWA}_{\text{op}}=12.5\times\mathrm{ORC}.
$$
The **Business Indicator Component** scales the **Business Indicator** $BI$ by marginal coefficients $\alpha_i$:
$$
\mathrm{BIC}=\begin{cases}0.12\,BI, & BI\le €1\,\text{bn}\\[2pt] 0.12\cdot1+0.15\,(BI-1), & 1<BI\le €30\,\text{bn (€bn)}\\[2pt] 0.12\cdot1+0.15\cdot29+0.18\,(BI-30), & BI>€30\,\text{bn (€bn)}\end{cases}
$$
The **Internal Loss Multiplier** folds in the bank's own loss history through the Loss Component $LC=15\times$ average annual losses:
$$
\mathrm{ILM}=\ln\!\Big(e-1+\big(\tfrac{LC}{\mathrm{BIC}}\big)^{0.8}\Big),
$$
so $\mathrm{ILM}=1$ when $LC=\mathrm{BIC}$, $\mathrm{ILM}>1$ for a lossy bank, $\mathrm{ILM}<1$ for a clean one. **Capital literally rises and falls with a bank's own realised losses.**

---

### 3. Computational Implementation - IRB vs SA, and the op-risk SMA

Standard library (normal CDF from `math.erf`, inverse from a rational approximation).

**Experiment 1 - IRB risk weights vs the flat SA weight.**




**Experiment 2 - operational risk via the SMA.**



(The €35bn row reproduces the regulator's own worked example - $\mathrm{BIC}=0.12+29\times0.15+5\times0.18=€5.37\text{bn}$ - a direct check that the bucket arithmetic is right.)

**What the numbers say.** (i) IRB is *not* uniformly cheaper: at PD 0.03% it yields a 14.4% RW but at PD 5% a 149.9% RW, so it is more risk-sensitive than SA in both directions. (ii) For a typical 1%-PD corporate the IRB RW (92.3%) is close to the flat SA 100%, which is why the arbitrage was never about plain corporates but about the *tails* and about low-PD assets. (iii) The SMA makes op-risk capital *increase with the bank's own losses* - an elegant self-punishing design that removed the AMA's incentive to under-model.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **IRB parameters are the bank's own.** Foundation IRB isolates PD, but advanced IRB lets the bank set LGD, EAD, and M - and a low-balled LGD directly cuts capital. Supervisory validation is the only check; weak validation is a first-order failure ([[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05]]).
2. **Procyclicality is built into IRB.** PD and LGD rise in downturns, so IRB RWA *rises* exactly when capital is scarce - the opposite of what a stabiliser should do. This is the canonical procyclicality failure and a core motivation for the output floor and buffers.
3. **The AMA was gamed out of existence.** Banks' op-risk models predicted low capital; realised losses (conduct, litigation) exceeded them badly. The regulator's response - abolishing the internal route - is a case study in why model-based capital needs a backstop.
4. **SA is blunt but hard to game.** Flat asset-class weights ignore real differences in borrower quality; a bank can hold high-quality and low-quality exposure at the same weight. Comparability rose; risk sensitivity fell. The post-crisis reform trades between the two.
5. **The 1.06 scaling factor and floor mechanics.** Small multiplicative factors and floors sound cosmetic but move RWA by billions; never ignore a "scaling factor" in the rules.

---

### 5. References

- **BCBS** - *Basel II: International Convergence of Capital Measurement and Capital Standards* (2006). SA risk-weight grid, the IRB formula, the three pillars. *Read from the corpus PDF.*
- **BCBS** - *Basel III: Finalising Post-Crisis Reforms* (2017, d424). Revised SA credit risk weights, the removal of the AMA, and the SMA for operational risk (Business Indicator, BIC, ILM, ORC$=\mathrm{BIC}\times\mathrm{ILM}$). *Read from the corpus PDF; the €35bn BIC example is checked numerically above.*
- **Hull, John C.** - *Options, Futures, and Other Derivatives* (11th ed.)
- **Vašíček, Oldřich** - *Probability of Loss on Loan Portfolio* (1987, KMV). The one-factor Gaussian model underpinning the IRB capital formula.
- **Gupton, Finger & Bhatia (J.P. Morgan)** - *CreditMetrics™ Technical Document* (1
- **Bluhm, Overbeck & Wagner** - *Introduction to Credit Risk Modeling* (2nd ed., 2010). Accessible derivation of the ASRF formula and portfolio loss distributions.
- **Panjer, Harry H.** - *Operational Risk: Modeling Analytics* (2006, Wiley). The loss-distribution approach that the AMA was built on

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|02 · Capital & RWA]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Index Hub]]
- Prerequisite / sibling: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA]] (the CVA charge)
- Forward: [[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/basel-and-regulation/06-advanced-extensions|06 · Advanced Extensions]]
