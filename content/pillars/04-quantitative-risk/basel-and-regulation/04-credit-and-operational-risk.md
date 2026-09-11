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

Credit risk is the largest RWA category for almost every bank; operational risk is the smallest but the one where the regulator gave up on internal models. This page covers both, and the common theme is **SA vs internal model**: the standardised approach applies regulator-set weights, while the internal approach lets the bank supply its own parameters — and the difference in capital can be enormous.

- **Credit risk.** SA weights a loan by asset class and (where available) external rating: sovereign, bank, corporate, retail, mortgage. **IRB** instead plugs the bank's own **PD**, **LGD**, **EAD**, and **M** into the **ASRF** (asymptotic single-risk-factor) closed form — the same Vasicek one-factor formula behind portfolio credit-VaR. Foundation IRB: bank supplies PD, supervisor supplies LGD/EAD. Advanced IRB: bank supplies all four.
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

#### 2.2 IRB credit risk — the ASRF capital formula

For a corporate/retail exposure with probability of default $\mathrm{PD}$, loss-given-default $\mathrm{LGD}$, and maturity $M$:
$$
\boxed{\;K=\underbrace{\Big[\mathrm{LGD}\cdot N\!\Big(\tfrac{N^{-1}(\mathrm{PD})+\sqrt R\,N^{-1}(0.999)}{\sqrt{1-R}}\Big)-\mathrm{PD}\cdot\mathrm{LGD}\Big]}_{\text{conditional expected loss above PD}\cdot\text{LGD}}\times\mathrm{MA}\;}
$$
with the **asset correlation**
$$
R=0.12\,\frac{1-e^{-50\,\mathrm{PD}}}{1-e^{-50}}+0.24\Big(1-\frac{1-e^{-50\,\mathrm{PD}}}{1-e^{-50}}\Big),
$$
and the **maturity adjustment** $b=(0.11852-0.05478\ln \mathrm{PD})^2$, $\ \mathrm{MA}=\dfrac{1+(M-2.5)b}{1-1.5b}$. The numerator $N^{-1}(\mathrm{PD})+\sqrt R\,N^{-1}(0.999)$ is the **Vasicek one-factor** conditional-default-probability argument at the 99.9% confidence level (Hull eq. 24.10): the $N^{-1}(0.999)$ shock is the systematic factor, $\sqrt R$ its loading. Then $\mathrm{RWA}=K\times12.5\times\mathrm{EAD}$ (and historically $\times1.06$ for the Basel II scaling factor).

#### 2.3 Operational risk — the SMA (BCBS 2017)

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

### 3. Computational Implementation — IRB vs SA, and the op-risk SMA

Standard library (normal CDF from `math.erf`, inverse from a rational approximation).

**Experiment 1 — IRB risk weights vs the flat SA weight.**

```python
import math
def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def Phi_inv(p):
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,
       -3.066479806614716e+01,2.506628277459239e+00]
    b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,
       -1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,
       4.374664141464968e+00,2.938163982698783e+00]
    d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00]
    if p<0.02425:
        q=math.sqrt(-2*math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p<=0.97575:
        q=p-0.5; r=q*q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q=math.sqrt(-2*math.log(1-p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

def irb_K(PD, LGD=0.45, M=2.5):
    R  = 0.12*(1-math.exp(-50*PD))/(1-math.exp(-50)) + 0.24*(1-(1-math.exp(-50*PD))/(1-math.exp(-50)))
    b  = (0.11852-0.05478*math.log(PD))**2
    MA = (1+(M-2.5)*b)/(1-1.5*b)
    K  = LGD*N((Phi_inv(PD)+math.sqrt(R)*Phi_inv(0.999))/math.sqrt(1-R)) - PD*LGD
    return K*MA, R, MA

for PD in (0.0003, 0.0025, 0.01, 0.02, 0.05):
    K,R,MA = irb_K(PD)
    print(f"PD={PD*100:6.2f}%  R={R:.4f}  MA={MA:.4f}  K={K*100:6.3f}%  RW={K*12.5*100:6.1f}%")
K1,_,_ = irb_K(0.01); EAD = 100e6
print(f"EAD $100m, PD=1%: IRB capital = ${K1*EAD:,.0f} (RW {K1*12.5*100:.1f}%)")
print(f"                  SA  capital = ${0.08*EAD:,.0f} (RW 100%)   relief = ${0.08*EAD-K1*EAD:,.0f}")
```
```
PD=  0.03%  R=0.2382  MA=1.9057  K= 1.155%  RW=  14.4%
PD=  0.25%  R=0.2259  MA=1.4273  K= 3.958%  RW=  49.5%
PD=  1.00%  R=0.1928  MA=1.2598  K= 7.385%  RW=  92.3%
PD=  2.00%  R=0.1641  MA=1.1993  K= 9.188%  RW= 114.9%
PD=  5.00%  R=0.1299  MA=1.1361  K=11.988%  RW= 149.9%
EAD $100m, PD=1%: IRB capital = $7,385,344 (RW 92.3%)
                  SA  capital = $8,000,000 (RW 100%)   relief = $614,656
```

**Experiment 2 — operational risk via the SMA.**

```python
import math
def bic(BI):                                   # BI in euro, buckets in €bn
    if BI<=1e9:   return 0.12*BI
    if BI<=30e9:  return 0.12*1e9 + 0.15*(BI-1e9)
    return 0.12*1e9 + 0.15*29e9 + 0.18*(BI-30e9)

for BI, avg_loss in ((2.0e9, 30e6), (35.0e9, 300e6)):
    B   = bic(BI)
    LC  = 15*avg_loss
    ILM = math.log(math.exp(1)-1 + (LC/B)**0.8)
    ORC = B*ILM
    print(f"BI=€{BI/1e9:4.1f}bn  BIC=€{B/1e9:.3f}bn  LC=€{LC/1e9:.3f}bn  ILM={ILM:.4f}  ORC=€{ORC/1e9:.4f}bn  RWA=€{ORC*12.5/1e9:.3f}bn")
```
```
BI=€ 2.0bn  BIC=€0.270bn  LC=€0.450bn  ILM=1.1703  ORC=€0.3160bn  RWA=€3.950bn
BI=€35.0bn  BIC=€5.370bn  LC=€4.500bn  ILM=0.9503  ORC=€5.1030bn  RWA=€63.787bn
```
(The €35bn row reproduces the regulator's own worked example — $\mathrm{BIC}=0.12+29\times0.15+5\times0.18=€5.37\text{bn}$ — a direct check that the bucket arithmetic is right.)

**What the numbers say.** (i) IRB is *not* uniformly cheaper: at PD 0.03% it yields a 14.4% RW but at PD 5% a 149.9% RW, so it is more risk-sensitive than SA in both directions. (ii) For a typical 1%-PD corporate the IRB RW (92.3%) is close to the flat SA 100%, which is why the arbitrage was never about plain corporates but about the *tails* and about low-PD assets. (iii) The SMA makes op-risk capital *increase with the bank's own losses* — an elegant self-punishing design that removed the AMA's incentive to under-model.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **IRB parameters are the bank's own.** Foundation IRB isolates PD, but advanced IRB lets the bank set LGD, EAD, and M — and a low-balled LGD directly cuts capital. Supervisory validation is the only check; weak validation is a first-order failure ([[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05]]).
2. **Procyclicality is built into IRB.** PD and LGD rise in downturns, so IRB RWA *rises* exactly when capital is scarce — the opposite of what a stabiliser should do. This is the canonical procyclicality failure and a core motivation for the output floor and buffers.
3. **The AMA was gamed out of existence.** Banks' op-risk models predicted low capital; realised losses (conduct, litigation) exceeded them badly. The regulator's response — abolishing the internal route — is a case study in why model-based capital needs a backstop.
4. **SA is blunt but hard to game.** Flat asset-class weights ignore real differences in borrower quality; a bank can hold high-quality and low-quality exposure at the same weight. Comparability rose; risk sensitivity fell. The post-crisis reform trades between the two.
5. **The 1.06 scaling factor and floor mechanics.** Small multiplicative factors and floors sound cosmetic but move RWA by billions; never ignore a "scaling factor" in the rules.

---

### 5. Canonical Literature & Study References

- **BCBS** — *Basel II: International Convergence of Capital Measurement and Capital Standards* (2006). SA risk-weight grid, the IRB formula, the three pillars. *Read from the corpus PDF.*
- **BCBS** — *Basel III: Finalising Post-Crisis Reforms* (2017, d424). Revised SA credit risk weights, the removal of the AMA, and the SMA for operational risk (Business Indicator, BIC, ILM, ORC$=\mathrm{BIC}\times\mathrm{ILM}$). *Read from the corpus PDF; the €35bn BIC example is checked numerically above.*
- **Hull, John C.** — *Options, Futures, and Other Derivatives* (11th ed.), Ch 24: §24.9 gives the **Vasicek one-factor** credit-VaR formula (eq. 24.10) that *is* the IRB conditional-default argument; §24.3 recovery ~40%; §24.4 hazard from spread (eq. 24.2). *Verified per chapter in the corpus.*
- **Vašíček, Oldřich** — *Probability of Loss on Loan Portfolio* (1987, KMV). The one-factor Gaussian model underpinning the IRB capital formula.
- **Gupton, Finger & Bhatia (J.P. Morgan)** — *CreditMetrics™ Technical Document* (1997). The rating-transition portfolio credit-risk framework — the practical ancestor of IRB.
- **Bluhm, Overbeck & Wagner** — *Introduction to Credit Risk Modeling* (2nd ed., 2010). Accessible derivation of the ASRF formula and portfolio loss distributions.
- **Panjer, Harry H.** — *Operational Risk: Modeling Analytics* (2006, Wiley). The loss-distribution approach that the AMA was built on — now historical, but the right reference for understanding what the SMA replaced.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|02 · Capital & RWA]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Index Hub]]
- Prerequisite / sibling: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA]] (the CVA charge)
- Forward: [[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/basel-and-regulation/06-advanced-extensions|06 · Advanced Extensions]]
