---
title: "05 — Failure Modes & Real-World Practice: WWR, Double-Counting, JTD"
tags:
  - pillar-derivative-pricing
  - counterparty-risk
  - xva
  - wrong-way-risk
  - failure-modes
  - jump-to-default
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/04-fva-and-mva|04 · FVA & MVA]].

---

### 1. Intuition & Practical Objective

The xVA formulas in this folder rest on assumptions that are *quietly strong*. This page names them precisely, so a practitioner knows **which** assumption to distrust and **how** the failure shows up in money terms. The objective is not cynicism — it is knowing exactly where the model is an approximation so the residual risk can be measured and managed (the same discipline as [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|Black–Scholes' failure modes]]).

The failures, in one line each:
1. **Wrong-way risk (WWR)** — exposure and counterparty credit are assumed independent; in reality default is *more likely when exposure is high*, so CVA is underpriced.
2. **DVA / FBA double-counting** — two frameworks price the same negative-exposure benefit twice.
3. **Jump-to-default (JTD)** — CVA is a *smooth* function of spread, but real defaults are *jumps*; the delta hedge cannot protect the jump loss.

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live.** Every CVA/DVA in this folder assumes, explicitly or implicitly (Gregory 17.2, 17.6):
- **(A1) Independence** of exposure, default probability, and LGD (no WWR).
- **(A2) Exposure is computed unconditionally**, not conditional on default.
- **(A3) Default is a diffusion** — spread gamma is continuous; the close-out is the base value.

**(A1)/(A2) fail ⇒ WWR.** The correct exposure is $EPE(t,t_i|\,\tau_C=t_i)$ — exposure *given* the counterparty defaults at $t_i$. With a single correlation $\rho$ between the exposure and credit drivers, corr +50% **roughly doubles** EPE and −50% at least halves it (Gregory §17.6.2). Crucially, WWR **increases with the counterparty's credit quality** — the default of a strong name is a bigger shock — and matters most for the systemic parties that post margin (Pykhtin–Sokol 2013: jump-based WWR erodes the collateral benefit precisely when the margin is posted).

**(A3) fails ⇒ JTD.** Gregory Eq 21.2:

$$JTD\ P\&L = -(\text{Current exposure})\times LGD + (\text{CDS hedge notional})\times LGD_{CDS} - \text{current xVA contribution}.$$

For an ITM portfolio without a single-name hedge, JTD is **always negative** — a jump through the exposure is a first-order loss no smooth hedge captures (Gregory §21.2.5).

**The double-counting structure** (Gregory §18.2.5). DVA (own default avoids paying the derivative) and FBA (negative exposure gives a funding benefit) describe the *same* cash flow. Burgard–Kjaer reconcile: $FBA\equiv DVA$ when the funding spread equals $LGD_P\,\lambda_P$ and all terms are additive at netting-set level — so the frameworks are consistent *only if you do not take both*. The two acceptable packages:

$$CVA + \underbrace{FCA+FBA}_{\text{symmetric funding}}\qquad\text{or}\qquad \underbrace{CVA + DVA}_{\text{bilateral}} + FCA.$$

---

### 3. Computational Implementation — the failures in numbers

Three experiments, stdlib only.

**Experiment 1 — WWR in Monte Carlo.** A common stress factor $X$ drives both exposure (loading $\rho$) and default ($X>x$). Conditional-on-default EPE is compared with the unconditional (no-WWR) number.

```python
import math, random
def epe_wwr(mu, sig, rho, x, n=200000):
    random.seed(7)
    tot_un = tot_c = 0.0; ncond = 0
    for _ in range(n):
        X = random.gauss(0, 1); Z = random.gauss(0, 1)
        E = mu + sig * (rho * X + math.sqrt(1 - rho * rho) * Z)
        tot_un += max(E, 0.0)
        if X > x:                    # default = latent stress factor X spikes
            tot_c += max(E, 0.0); ncond += 1
    return tot_un / n, tot_c / ncond

print("=== WWR: conditional-on-default EPE vs unconditional EPE (E ~ N(10,20)) ===")
for rho in (-0.5, 0.0, 0.5):
    un, cond = epe_wwr(10.0, 20.0, rho, 1.0)
    print(f"  corr {rho:+.1f}: unconditional EPE={un:.2f}   conditional={cond:.2f}   ratio={cond/un:.2f}")
print("Gregory 17.6: corr +50% roughly DOUBLES EPE; -50% at least halves it.")
```
```
=== WWR: conditional-on-default EPE vs unconditional EPE (E ~ N(10,20)) ===
  corr -0.5: unconditional EPE=13.93   conditional=4.75   ratio=0.34
  corr +0.0: unconditional EPE=13.96   conditional=13.88   ratio=0.99
  corr +0.5: unconditional EPE=13.99   conditional=25.84   ratio=1.85
Gregory 17.6: corr +50% roughly DOUBLES EPE; -50% at least halves it.
```

**Experiment 2 — DVA / FBA double-counting.**

```python
benefit_once = 8.7
print(f"FBA counted once = +{benefit_once};  once via FBA + once via DVA = "
      f"+{2*benefit_once} (inflated). Use CVA+FCA+FBA  OR  CVA+DVA+FCA, never both.")
```
```
FBA counted once = +8.7;  once via FBA + once via DVA = +17.4 (inflated). Use CVA+FCA+FBA  OR  CVA+DVA+FCA, never both.
```

**Experiment 3 — Jump-to-default P&L (Eq 21.2).**

```python
CE, lgd = 40.0, 0.60; xva_contrib = 2.0
print(f"unhedged : JTD = -CE*LGD - xVA_contrib       = {-CE*lgd - xva_contrib:+.1f}")
cds_not, cds_lgd = 60.0, 0.60
print(f"hedged   : JTD = -CE*LGD + CDSnot*CDS_LGD - xVA = {-CE*lgd + cds_not*cds_lgd - xva_contrib:+.1f}")
```
```
unhedged : JTD = -CE*LGD - xVA_contrib       = -26.0
hedged   : JTD = -CE*LGD + CDSnot*CDS_LGD - xVA = +10.0
```

WWR is real and asymmetric: at +50% correlation the conditional EPE is **1.85×** the unconditional (the independence model undercharges by ~half); at −50% it collapses to 0.34× (right-way risk, overcharge). The JTD experiment shows the hedge is doing real work — it turns a guaranteed −26 loss into +10 — but a hedge needs the *right* notional and maturity, which is exactly the management problem of [[pillars/03-derivative-pricing/counterparty-risk-and-xva/06-advanced-extensions|06 · Advanced Extensions]].

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **The independence delusion (A1 fails).** Almost every basic CVA treats exposure, PD and LGD as independent. Under real WWR this underprices CVA — by roughly 2× at +50% correlation. The safe fix is conditional exposure $EPE(\cdot|\tau)$ (Gregory §17.6).
2. **Unconditional exposure (A2 fails).** Computing EPE from market paths alone is the *implicit* no-WWR assumption. It is not a neutral choice — it is a bet that default and exposure are uncorrelated.
3. **Double-counting DVA with FBA.** Including both discounts the negative-exposure benefit twice. Two acceptable packages, never a mix (Gregory §18.2.5).
4. **Jumps break the smooth-CVA view (A3 fails).** CVA's spread-gamma is continuous; a real default is a jump. Delta-hedging CVA with CDS protects the *spread* move, not the *jump* — the JTD loss above is the unhedged piece (Gregory §21.2.5).
5. **Credit limits vs CVA.** Credit *limits* are a portfolio concentration control; CVA is a *price*. CVA rewards fewer counterparties (netting), limits reward more (diversification) — conflating the two misprices and misallocates (Gregory §3.1.5).

---

### 5. Canonical Literature & Study References

- **Gregory**, *The xVA Challenge*, Ch 17 §17.6 (wrong-way risk), §18.2.5 (double-counting), Ch 21 §21.2 (hedging, JTD, beta hedging, limits/P&L explain). *Primary; numbers verified.*
- **Pykhtin, Michael & Andrew Sokol (2013)**: *Exposure under systematic credit impact* — jump-based WWR erodes the collateral benefit.
- **Rosen, Dan & David Saunders (2012)**: *CVA the wrong way* — WWR quantification.
- **Hull & White (2012, 2014)** / **Kenyon & Green (2014)** / **Morini & Prampolini (2010)**: the FVA/DVA double-counting debate.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/04-fva-and-mva|04 · FVA & MVA]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Structural Model]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
