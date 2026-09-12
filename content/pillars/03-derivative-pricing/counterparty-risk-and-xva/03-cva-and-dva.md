---
title: "3.10.3 CVA & DVA"
tags:
  - pillar-derivative-pricing
  - counterparty-risk
  - cva
  - dva
  - bilateral-credit
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/02-exposure-and-margin|02 · Exposure & Margin]].

---

### 1. Intuition & Practical Objective

Credit Value Adjustment (CVA) is the **price of counterparty risk** - it internalises the expected loss from your counterparty's default into the derivative's value (Gregory Ch 17). Debt Value Adjustment (DVA) is its mirror image: the benefit of *your own* default (the liabilities you don't pay). The practical objective: compute both, understand why they oppose each other, and know exactly which credit numbers feed in.

The three questions CVA answers (Gregory 17.2): *Does the counterparty default? What is my exposure then? How much do I lose?* In symbols,

$$
CVA(t) \approx -LGD\sum_{i=1}^{m} EPE(t,t_i)\times PD(t_{i-1},t_i),
$$

which is the discrete form of the continuous integral

$$
CVA(t) = -LGD\int_t^{\infty}\lambda_C(u)\,D_{r+\lambda_C}(t,u)\,EPE(t,u)\,du.
$$

Three ideas matter:
- **It is a product of market risk and credit risk.** EPE is the *market* component (how big is the exposure); PD × LGD is the *credit* component (how likely is default, how much is lost). This is the "market × credit" split that makes CVA both a derivatives problem and a credit problem.
- **Default probabilities are risk-neutral, market-implied.** Since the accounting standards moved CVA to a *market* (hedging/exit-price) basis, PDs come from CDS credit spreads, not historical default rates (Gregory §3.1.7; Hull 24.5 - risk-neutral PDs exceed real-world ones).
- **DVA is the other half of the same coin.** Your counterparty prices *your* default as a DVA against you; "my CVA is your DVA" is what makes bilateral pricing symmetric (Gregory 17.3).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The CVA formula (Gregory Eqs 17.1–17.3)

**Direct form** - simulate the default time $\tau$, value the portfolio once at $\tau$:

$$
UCVA(t) = -\mathbb{E}\!\left[\mathbf{1}_{\tau\le T}\,V(t,\tau)^+\,LGD\right].
$$

**Path-wise / discrete form** - the workhorse (Eq 17.3):

$$
UCVA(t) \approx -LGD\sum_{i=1}^{m} EPE(t,t_i)\times PD(t_{i-1},t_i),
$$

where $EPE(t,t_i)=\mathbb{E}[V(t,t_i)^+]$ is the discounted expected positive exposure at date $t_i$ and $PD(t_{i-1},t_i)$ the default probability over that interval (independence ⇒ default enters only via PD). With flat $\lambda$, $PD(a,b)=e^{-\lambda a}-e^{-\lambda b}$.

**The credit inputs.** From a CDS spread $s$ and $LGD=1-R$, the hazard is $\lambda=s/LGD$ (Hull 24.2; BM 21.25), survival $Q(\tau>t)=e^{-\lambda t}$. The LGD-adjusted form (Eq 17.5) splits the *market* LGD (used to strip PDs from CDS, usually senior unsecured) from the *actual* expected LGD; when seniority matches they **cancel to first order** - changing LGD 60%→50% moves CVA <2% (Gregory §17.2.6).

**CVA as a spread** (Eq 17.4), valid for roughly-flat EPE/PD profiles: $UCVA \approx -\overline{EPE}\times s$.

#### 2.2 DVA and the bilateral framework (Gregory 17.3)

DVA is the own-default side, driven by the **ENE** (your counterparty's positive exposure / your negative exposure):

$$
DVA(t) = -LGD_P\int_t^{\infty}\lambda_P(u)\,D_{r+\lambda_C+\lambda_P}(t,u)\,ENE(t,u)\,du.
$$

The bilateral value is

$$
BCVA = CVA + DVA,
$$

with the discrete forms (Eqs 17.8a/b) carrying the *survival probability of the other party* (the "first-to-default" effect):

$$
CVA(t) = -LGD_C\sum_{i} EPE(t,t_i)\,PD_C(t_{i-1},t_i)\,[1-PD_P(0,t_{i-1})],
$$
$$
DVA(t) = -LGD_P\sum_{i} ENE(t,t_i)\,PD_P(t_{i-1},t_i)\,[1-PD_C(0,t_{i-1})].
$$

Key facts:
- **ENE ≤ 0 ⇒ DVA ≥ 0**: DVA is a *benefit* opposing CVA (your default wipes out the debt you owe).
- **Spread approximation** (Eq 17.9): $BCVA \approx -\overline{EPE}\,s_C - \overline{ENE}\,s_P$; when $\overline{EPE}\approx-\overline{ENE}$, $BCVA\approx-\overline{EPE}(s_C-s_P)$ - **the weaker (higher-spread) party pays the stronger**. Gregory Table 17.3: 10y swaps, both LGD 60%, own spread < counterparty: $UCVA\,{-}29.9 / UDVA\,{+}8.1 / BCVA\,{-}21.5$ (pay-fixed).
- **Accounting vs capital**: IFRS 13 *requires* own-credit (DVA) in liability fair value; Basel III *derecognises* DVA from capital (Gregory §17.3.5, §13.3.1). Hence the debate in [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]].

#### 2.3 Wrong-way risk (Gregory 17.6)

The standard formulas assume independence. **Wrong-way risk (WWR)** = unfavourable dependence between exposure and counterparty credit quality (default is more likely when exposure is high). Replace $EPE(t,t_i)$ with the *conditional* $EPE(t,t_i|\tau_C=t_i)$. Canonical WWR: buying a put on a name correlated to the counterparty; an FX forward with a sovereign paying local currency; a corporate *paying* fixed when rates fall in a recession. Gregory's key empirical result: **corr +50% roughly doubles EPE; −50% at least halves it** - and WWR *increases* as the counterparty's credit quality rises (a strong-name default is a bigger shock).

---

### 3. Computational Implementation - unilateral and bilateral CVA in full

A stylised 5-year payer swap with discounted EPE/ENE profiles and two credit curves. Stdlib only; reproduces the "market × credit × LGD" product and the unilateral→bilateral contrast.



Notice the *structure*: the counterparty is riskier than you (150bp vs 100bp), so CVA (−1.35) exceeds DVA (+0.47) and the swap is a *cost* to you (BCVA −0.89). The spread approximation (−0.40) has the same sign but is rough because the EPE/ENE profiles are not flat - exactly Gregory's caveat on Eq 17.4.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using historical PDs.** Real-world (historical) default rates are lower than risk-neutral (CDS-implied) ones; pricing CVA with historical PDs undercharges for risk and contradicts the market/exit-price basis required by accounting (Gregory §3.1.7, §17.2; Hull 24.5).
2. **Ignoring wrong-way risk.** Under the independence assumption, CVA is structurally *underpriced* when default and exposure co-move - corr +50% ≈ doubles EPE (Gregory §17.6). The assumption is *no-WWR*, not a neutral one.
3. **Adding standalone CVAs.** CVA is a netting-set quantity; the standalone sum over-tells the portfolio CVA because it ignores netting (Gregory Eq 17.10). Incremental/marginal CVA must be computed on the *netting set*, not trade-by-trade.
4. **Mixing LGDs.** Using one LGD to strip PDs from CDS and a different one as the loss severity - without the "actual vs market" separation of Eq 17.5 - distorts both inputs. When seniority matches, the LGDs cancel to first order; force them apart only when the waterfall justifies it (Gregory §17.2.6).

---

### 5. References

- **Gregory**, *The xVA Challenge*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Brigo & Mercurio**, *Interest Rate Models*
- **Pykhtin, Michael & Steven Zhu (2007)**: *A Guide to Modeling Counterparty Credit Risk*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/02-exposure-and-margin|02 · Exposure & Margin]]
- Forward: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/04-fva-and-mva|04 · FVA & MVA]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Index Hub]]
- Credit theory: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Structural Model]] · [[foundations/probability-and-measure-theory/index|Probability & Measure]]
