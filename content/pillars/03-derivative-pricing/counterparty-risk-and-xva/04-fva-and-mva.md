---
title: "04 — FVA & MVA: The Cost of Funding (Under- and Over-Collateralisation)"
tags:
  - pillar-derivative-pricing
  - counterparty-risk
  - xva
  - fva
  - mva
  - funding
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]].

---

### 1. Intuition & Practical Objective

Credit risk (CVA/DVA) is about *default*. **Funding** is about *cash*. This page prices the two funding adjustments: **FVA** (Funding Value Adjustment, the cost/benefit of financing the derivative's value and margin) and **MVA** (Margin Value Adjustment, the cost of posting initial margin). The practical objective: compute each, understand the crucial asymmetry — *FVA can be a cost or a benefit, MVA is almost always a cost* — and avoid the double-counting that plagues naive implementations.

The one-line distinction (Gregory §16.3.2):
- **FVA = cost of being *under*-collateralised** (variation margin, running value).
- **MVA = cost of being *over*-collateralised** (initial margin, segregated and non-rehypothecable).

Where does funding come from? It is literally **value − margin** (Gregory Eq 18.1). A derivative with positive value must be *funded* — you borrow to finance the asset — a cost. A negative value gives you a funding *benefit* (the "borrowing" is a liability others fund you for). Under perfect collateralisation value − margin ≈ 0 and there is no FVA; under- or partial collateralisation leaves a residual to fund.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 FVA (Gregory Ch 18)

The funding profile is the **EFV** (expected future value) of the transaction. Symmetric FVA (Eq 18.3):

$$FVA = -\sum_{i=1}^{m} EFV(t_i)\times FS(t_{i-1},t_i)\times(t_i-t_{i-1}),$$

where $FS(t_{i-1},t_i)\approx\frac{FS(0,t_i)t_i-FS(0,t_{i-1})t_{i-1}}{t_i-t_{i-1}}$ is the *forward* funding spread over the valuation (OIS) rate. Because $EPE+ENE=EFV$, FVA splits into

$$FVA = FCA + FBA,\qquad FCA=-\sum_i EPE(t_i)\,FS\,\Delta t,\qquad FBA=-\sum_i ENE(t_i)\,FS\,\Delta t.$$

- **FCA** (Funding Cost Adjustment): cost of funding *positive* exposure.
- **FBA** (Funding Benefit Adjustment): benefit of *negative* exposure.
- Compared to CVA (Eq 17.3), the **bank's funding spread replaces the counterparty credit spread, and EFV replaces EPE** (Gregory §18.2.4).

**The FVA debate.** Hull & White (2012) argued FVA should not be in pricing/valuation at all: including a party's own funding cost breaks price symmetry and the law of one price, and creates arbitrage (buy options from a low-funding-cost bank, sell to a high-cost one). The counter (Kenyon & Green 2014; shareholder view): there is *no* market for uncollateralised derivatives, so incremental FVA belongs in entry prices when maximising shareholder value. The current consensus: **FVA in pricing under the shareholder view is broadly accepted; FVA in *accounting* valuation is contested** (Gregory §18.2.6).

**The double-counting trap.** DVA (own default avoids paying) and FBA (negative exposure gives a funding benefit) price the *same* benefit twice. Two consistent frameworks (Gregory §18.2.5):
- **CVA + symmetric funding** = `CVA + FCA + FBA` (Basel III consistent, no DVA; the majority market choice for pricing), or
- **Bilateral CVA + asymmetric funding** = `CVA + DVA + FCA` (IFRS 13 consistent).
Never both DVA *and* FBA.

#### 2.2 MVA (Gregory Ch 20)

Initial margin is segregated, non-rehypothecable, custodian-held, and (for cash IM) remunerated at or below OIS — so it is a **liability, not an asset** (Gregory Table 20.3: cost only, asymmetric, sub-OIS reference). MVA (Eq 20.1):

$$MVA \approx -\sum_{i=1}^{m} EIM(t_i)\times FS(t_{i-1},t_i)\times(t_i-t_{i-1}),$$

where $EIM$ is the discounted **expected initial-margin profile**. IM evolves through portfolio ageing (it can *increase* as offsetting long-dated trades mature), look-back-window roll, and annual SIMM recalibration (Gregory §20.2.3) — which is why MVA is *not* trivially computable alongside CVA.

**MVA vs KVA trade-off (Gregory §20.4).** Posting more IM raises MVA (more funding) but *lowers* KVA (less capital, since IM covers exposure). The optimal posted IM is generally **below** the full regulatory requirement, because KVA relief under SA-CCR has *diminishing* returns (conservative add-ons + the 5% floor). **KVA and MVA must be treated equivalently in pricing**, or the bank incentivises sub-optimal structures (backloading to a CCP, discretionary IM).

---

### 3. Computational Implementation — FVA decomposition and MVA

Stdlib only. The FVA example uses consistent profiles (EPE + ENE = EFV), so FCA + FBA must equal FVA exactly — a built-in sanity check.

```python
import math
t   = [1, 2, 3, 4, 5]
efv = [30.0, 42.0, 46.0, 40.0, 28.0]          # funding profile (EFV)
ene = [-6.0, -9.0, -10.0, -9.0, -6.0]
epe = [efv[i] - ene[i] for i in range(5)]     # EPE + ENE = EFV  (Gregory 18.4)
fs0 = 0.0060                                  # funding spread 60bp vs OIS

def disc(sp, tt): return math.exp(-sp * tt)
def fw(sp, i):    return (disc(sp, t[i]-1) - disc(sp, t[i])) / 1.0    # 1y forward spread

fva = sum(efv[i] * fw(fs0, i) for i in range(5))
fca = sum(epe[i] * fw(fs0, i) for i in range(5))
fba = sum(ene[i] * fw(fs0, i) for i in range(5))
print("=== FVA = FCA + FBA over a 5y payer-swap funding profile ===")
print(f"EFV={efv}")
print(f"EPE={[round(v,1) for v in epe]}   ENE={[round(v,1) for v in ene]}   (EPE+ENE=EFV)")
print(f"FCA = -{fca:.3f}   (cost: EPE x funding spread)")
print(f"FBA = +{-fba:.3f}   (benefit: |ENE| x funding spread)")
print(f"FVA = -{fva:.3f}   and  FCA+FBA = -{fca+fba:.3f}  (consistent)")

print()
print("=== MVA = sum EIM(t_i) * FS * dt  (Eq 20.1) - IM cost is one-way ===")
eim   = [100.0, 88.0, 70.0, 50.0, 30.0]      # expected initial-margin profile
fs_im = 0.0100                               # sub-OIS IM funding, 100bp
mva = sum(eim[i] * fw(fs_im, i) for i in range(5))
print(f"EIM={eim}")
print(f"MVA = -{mva:.3f}   (cost only; segregated IM gives no FBA-type benefit)")
```
```
=== FVA = FCA + FBA over a 5y payer-swap funding profile ===
EFV=[30.0, 42.0, 46.0, 40.0, 28.0]
EPE=[36.0, 51.0, 56.0, 49.0, 34.0]   ENE=[-6.0, -9.0, -10.0, -9.0, -6.0]   (EPE+ENE=EFV)
FCA = -1.336   (cost: EPE x funding spread)
FBA = +0.236   (benefit: |ENE| x funding spread)
FVA = -1.100   and  FCA+FBA = -1.100  (consistent)

=== MVA = sum EIM(t_i) * FS * dt  (Eq 20.1) - IM cost is one-way ===
EIM=[100.0, 88.0, 70.0, 50.0, 30.0]
MVA = -3.314   (cost only; segregated IM gives no FBA-type benefit)
```
The payer swap is a *net asset* (EFV > 0 throughout), so FVA is a cost; but notice FBA is positive because the swap occasionally has negative value. MVA is larger than FVA here because initial margin (100→30) dwarfs the variation-margin funding profile — typical of a bilaterally-margined trade.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Inconsistent profiles.** FVA is built on EPE + ENE = EFV. If you feed EPE and ENE from one model and EFV from another, FCA + FBA ≠ FVA — a silent, hard-to-catch inconsistency. The check is built into the code above.
2. **Double-counting DVA with FBA.** Counting the benefit of a negative exposure twice (own-default *and* funding) double-discounts the cash flow (Gregory §18.2.5). Pick `CVA + FCA + FBA` *or* `CVA + DVA + FCA` and stick to it.
3. **Symmetric FVA where funding is asymmetric.** Symmetric FVA assumes you borrow and lend at the *same* unsecured spread; real funding is asymmetric (borrow unsecured, lend at OIS) and must be computed at the funding-set level, not trade level (Gregory §18.3, Eqs 18.8–18.9). This is inconsistent with the NSFR.
4. **MVA as a benefit.** Unlike FVA, segregated IM can *never* be a funding benefit — posting IM is a liability with no rehypothecation. Pricing MVA as if it could net against FBA is wrong.

---

### 5. Canonical Literature & Study References

- **Gregory**, *The xVA Challenge*, Ch 14 (funding, margin, capital costs), Ch 16 (ColVA, perfect collateralisation, base value), Ch 18 (FVA), Ch 20 (MVA). *Primary; all numbers verified.*
- **Piterbarg, Vladimir (2010)**: *Funding beyond discounting* (Risk) — the marginal-funding/perfect-collateralisation base value.
- **Burgard, Christoph & Martin Kjaer (2011a,b)**: *Partial differential equation representations of derivatives with bilateral counterparty risk and funding costs* — the FCA/DVA integral framework.
- **Hull & White (2012, 2014)** and **Kenyon & Green (2014)**: the FVA debate (against / for).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]]
- Forward: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/interest-rate-and-term-structure-models|Interest Rate & Term Structure Models]] (the discounting/FVA connection)
