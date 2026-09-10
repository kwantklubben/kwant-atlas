---
title: "05 — Failure Modes & Real-World Practice"
tags:
  - pillar-quantitative-risk
  - basel-and-regulation
  - failure-modes
  - regulatory-arbitrage
  - procyclicality
  - model-approval
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/basel-and-regulation/03-market-risk-and-frtb|03 · Market Risk & FRTB]] and [[pillars/04-quantitative-risk/basel-and-regulation/04-credit-and-operational-risk|04 · Credit & Operational Risk]].

---

### 1. Intuition & Practical Objective

The capital framework is a *model of risk written into law*, and every model has failure modes. This page names the three that matter most for practitioners, ties each to first principles, and quantifies each so the failure is a number, not a slogan:

1. **Regulatory arbitrage** — because capital scales with *risk weight*, not *risk*, a bank can raise its ratio by re-labelling the same economic exposure (securitisation, guarantees, model approval). The firm's reported safety improves; the system's does not.
2. **Procyclicality** — risk weights, PDs, and volatilities all rise in a downturn, so required capital *increases* exactly when banks can least raise it, amplifying the cycle the rules were meant to dampen.
3. **Model approval & measurement error** — the internal approaches (IRB, IMA) let a bank supply its own parameters. If validation is weak, the bank's capital becomes a number it controls against itself, and the supervisor's sign-off becomes the only real check.

The objective is not cynicism. It is the discipline of knowing *which lever* a ratio can be moved with, so that a reported improvement can be interrogated: did the bank reduce risk, or reduce the *weight*?

---

### 2. Mathematical Ground Truth & Derivations

**Arbitrage in one identity.** The ratio is $E/\sum_i E_i\,rw_i$. Holding capital $E$ and exposure $E_i$ fixed, any *reduction in $rw_i$* raises the ratio:
$$\frac{\partial}{\partial rw_i}\Big(\frac{E}{\mathrm{RWA}}\Big)=-\frac{E\,E_i}{\mathrm{RWA}^2}<0 .$$
So the cheapest way to "improve" capital is never to de-risk — it is to find the lowest $rw_i$ for the same cash-flow. The reform countermeasure is to *reduce the scope* for $rw$ differences: the **output floor** ($\mathrm{RWA}\ge72.5\%\,\mathrm{RWA}_{\text{SA}}$, §06) caps how far internal models may cut RWA below the standardised measure.

**Procyclicality as a function of ratings/vol.** RWA moves with $rw(\text{rating})$, and PD moves with the cycle, so
$$\frac{\partial \mathrm{RWA}}{\partial \text{downturn}}>0\quad\Longrightarrow\quad \frac{\partial (\text{capital ratio})}{\partial \text{downturn}}<0 .$$
The framework's attempted antidotes: the **countercyclical buffer** (build CET1 in good times, release in bad), through-the-cycle PD calibration, and the output floor. None fully removes the feedback.

**Measurement error compounds through the ratio.** If a bank's IRB/IMA parameters understate true risk, both the numerator (via how capital is computed) and the denominator (RWA) are affected; a systematic underestimation of loss given default, say, cuts capital more than proportionally because it also lowers the conditional-loss term $N^{-1}(\mathrm{PD})+\sqrt R\,N^{-1}(0.999)$.

---

### 3. Computational Implementation — the three failures in numbers

Stdlib only. Each block is a concrete, exploitable or dangerous effect.

**Failure 1 — regulatory arbitrage via securitisation.**

```python
corp = 100*1.00*0.08      # $100 corporate loan, RW 100%, 8% capital
sez  = 100*0.20*0.08      # $100 AAA RMBS tranche, RW 20%
print(f"$100 corporate RW100%: capital ${corp:.2f}")
print(f"$100 AAA RMBS  RW 20%: capital ${sez:.2f}")
print(f"capital released by re-wrapping = ${corp-sez:.2f} per $100  ({(corp-sez)/corp*100:.0f}% relief)")
```
```
$100 corporate RW100%: capital $8.00
$100 AAA RMBS  RW 20%: capital $1.60
capital released by re-wrapping = $6.40 per $100  (80% relief)
```

**Failure 2 — procyclicality: a book-wide rating migration.**

```python
cet = 100.0
for mult, label in ((1.00,"base RW 100%"),(1.25,"one notch (RW 125%)"),(1.50,"two notches (RW 150%)")):
    rwa = 1000.0*mult
    print(f"  {label:22s} -> RWA {rwa:6.0f}   CET1 ratio {cet/rwa*100:5.2f}%")
```
```
  base RW 100%           -> RWA   1000   CET1 ratio 10.00%
  one notch (RW 125%)    -> RWA   1250   CET1 ratio  8.00%
  two notches (RW 150%)  -> RWA   1500   CET1 ratio  6.67%
```

**Failure 3 — the model gap: identical risk, different RWA.**

```python
cet = 100.0
for name, rwa in (("SA  bank", 1000.0), ("IRB bank", 850.0)):
    print(f"  {name}: RWA {rwa:.0f}   CET1 ratio {cet/rwa*100:.2f}%")
```
```
  SA  bank: RWA 1000   CET1 ratio 10.00%
  IRB bank: RWA 850   CET1 ratio 11.76%
```

**What the numbers say.** (i) Re-wrapping a \$100 corporate loan as a AAA securitisation tranche cuts its capital requirement by 80% **with no change in the underlying cash flows** — the arbitrage is a *classification* trade. (ii) A two-notch downgrade of an entire book lifts RWA 50% and pushes the CET1 ratio from 10.00% to 6.67% — a solvency-threatening fall caused entirely by the rating of unchanged positions. (iii) Two banks with the same economic risk can report 10.00% and 11.76% purely because one uses IRB — the denominator is not comparable, which is why the output floor exists. **All three failures live in the denominator, not the numerator.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Arbitrage → the ratio decouples from risk.** Because $E/\mathrm{RWA}$ falls in $rw$, the cheapest ratio improvement is re-labelling, not de-risking. Remedies: the output floor, leverage ratio (which ignores $rw$ entirely), and disclosure.
2. **Procyclicality → capital rises when it can least be raised.** Ratings, PDs, and volatilities are all cycle-dependent, so RWA is highest in the bust. The countercyclical buffer and through-the-cycle calibration reduce, but do not remove, the feedback (Brunnermeier-style amplification, [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]).
3. **Model approval → the sign-off is the only real check.** IRB/IMA parameters are the bank's own; a mis-validated PD or LGD understates capital and, because it is multiplicative, does so non-linearly. The AMA's abolition (§04) is the concrete case of a model route withdrawn after losses revealed the error.
4. **The leverage/RWA split means *two* liabilities to manage.** A bank can be comfortable on one ratio and thin on the other: low-RWA books pass the risk-based test but blow the 3% leverage test; low-leverage books pass leverage but can still be RWA-fragile. Practitioners must track both ([[pillars/04-quantitative-risk/basel-and-regulation/06-advanced-extensions|06]]).
5. **Liquidity is not in the capital ratio.** A bank can be well-capitalised and still die of a run — the reason the LCR/NSFR exist as separate, hard constraints (§06). Capital is a solvency buffer; liquidity is a survival buffer; they are not substitutes.

---

### 5. Canonical Literature & Study References

- **BCBS** — *Basel III: Finalising Post-Crisis Reforms* (2017, d424). The policy responses to these exact failures: constrained IRB use, the revised output floor, and the leverage backstop. *Read from the corpus PDF.*
- **BCBS** — *Basel III: A Global Regulatory Framework* (2010, d189). Introduces the capital conservation and countercyclical buffers explicitly to fight procyclicality. *Read from the corpus PDF.*
- **Brunnermeier, Markus K.** — *Deciphering the Liquidity and Credit Crunch 2007–2008*, *J. Economic Perspectives* **23**(1):77–100 (2009). The canonical narrative of how leverage, procyclical haircuts, and funding runs propagated — the crisis these failure modes produced. *Read from the corpus PDF.*
- **Hull, John C.** — *Risk Management and Financial Institutions* (5th ed., 2018). The regulation chapter's treatment of arbitrage, procyclicality, and the post-crisis fixes. *Recommended textbook map.*
- **Hull, John C.** — *Options, Futures, and Other Derivatives* (11th ed.), Ch 24 (default correlation, the Vasicek one-factor link between portfolio credit risk and regulatory capital). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/basel-and-regulation/03-market-risk-and-frtb|03 · Market Risk & FRTB]] · [[pillars/04-quantitative-risk/basel-and-regulation/04-credit-and-operational-risk|04 · Credit & Operational Risk]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/basel-and-regulation/06-advanced-extensions|06 · Advanced Extensions (LCR, NSFR, Leverage, Output Floor)]]
- Sibling: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] (Pillar 2)
