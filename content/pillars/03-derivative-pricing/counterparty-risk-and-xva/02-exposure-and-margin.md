---
title: "02 — Exposure, Netting & Margin: EE/PFE/EPE and the MPoR"
tags:
  - pillar-derivative-pricing
  - counterparty-risk
  - exposure
  - netting
  - collateral
  - initial-margin
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Exposure is the *raw material* every xVA term is built on, and margin is the single most powerful tool for reshaping it. This page makes both precise. The practical objective: **know, at every future time $t$, what your counterparty could owe you (positive exposure), how to shrink it with netting and collateral, and how much *residual* exposure survives after margin — because that residual, over the **margin period of risk (MPoR)** , is exactly what the next pages price.**

Two ideas drive everything:
- **Exposure metrics are integrals of the future value distribution.** EPE, ENE, PFE are all just summaries of $V(t)$'s distribution at each horizon.
- **Margin converts exposure into a *gap* risk.** Variation margin (VM) tracks the running value; initial margin (IM) absorbs the *MPoR gap* — the moves between the last margin call and close-out. A zero-threshold, perfectly-collected two-way margin can drive exposure to near zero, but never exactly zero, because of the MPoR (Gregory Ch 7, Ch 9).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Exposure metrics (Gregory Ch 11, App. 11A)

For a portfolio value $V(t)\sim N(\mu,\sigma)$ at horizon $t$, with $z=\mu/\sigma$:

$$EFV(t)=\mu,\qquad PFE_\alpha(t)=\mu+\sigma\Phi^{-1}(\alpha),\qquad EPE(t)=\sigma\phi(z)+\mu\Phi(z),\qquad ENE(t)=\sigma\phi(z)-\mu\Phi(-z).$$

- **PFE** is the $\alpha$-quantile of $V$ — *exactly* a Value-at-Risk number (Gregory 2.6; Hull 24.7). PFE(99%) is exceeded with probability $\le1\%$.
- **EPE** averages all values with negatives set to zero; **ENE** averages the negatives (it is your counterparty's positive exposure).
- Both EPE and ENE **rise with volatility** $\sigma$ — an out-of-the-money option still has positive EPE because volatility can push it in-the-money. ENE $=\sigma\phi(z)-\mu\Phi(-z)\le0$, and **EPE + ENE = EFV** (partition of the value).

#### 2.2 Netting (Gregory Ch 6, Hull 24.7)

Under one netting agreement the exposure is on the *net* value, so for a netting set with trades $j$:

$$EPE^{NS}(t) = E\!\left[\max\!\Big(\sum_j V^j(t),\,0\Big)\right] \le \sum_j EPE^j(t).$$

Netting benefit grows with correlation: two offsetting trades (opposite sign) have a *large* netting reduction; directional trades have a small one. Netting is what makes CVA a **netting-set-level** quantity — you cannot sum standalone trade CVAs and get the right portfolio CVA (Gregory 17.4; the standalone sum $\ge$ netting-set CVA, Eq 17.10).

#### 2.3 Margin / collateral (Gregory Ch 7)

**Variation margin (VM)** tracks the base valuation; **initial margin (IM)** is *extra* margin, independent of value, absorbing the MPoR risk. "Initial margin relates to the variability of the value rather than the value itself" (Gregory §7.3.4). IM is the *mathematical opposite of a threshold*: IM ≡ a *negative* threshold, so TH and IM are never used together.

**Credit support amount** (two-way VM, Gregory Eq 7.3):

$$CSA = \max(V-K_C,0)-\max(-V-K_P,0)-C,$$

where $K_C,K_P$ are the two parties' thresholds and $C$ the margin already held. **The MPoR model** (Gregory Eq 15.3) — the residual exposure is the value *minus the margin that was posted a full MPoR ago*:

$$\text{Exposure}_t = \max\!\big(V_t - C_{t-MPoR},\,0\big),$$

with $C$ positive if you *receive* margin, negative if you post it. Two reasons margin can't eliminate exposure: (i) threshold undercollateralisation, and (ii) the MPoR/MTA discrete tracking error (Gregory §7.3.7). Regulatory MPoR: **5 days** centrally cleared / repos, **10 days** bilateral OTC (Gregory Ch 9; Hull 24.7).

#### 2.4 Initial margin sizing (Gregory Ch 9, Hull 24)

The variance-covariance IM (Gregory §9.4.3) is a parametric VaR:

$$IM_{\alpha,\tau} = \Phi^{-1}(\alpha)\,\sqrt{\tau}\,\sigma_P,$$

with $\Phi^{-1}(0.99)=2.33$, $\sqrt{10/252}=0.1992$. Regulatory IM must cover a **99% one-tailed, 10-day horizon using data incorporating a significant stress period** (BCBS–IOSCO 2015). The ISDA **SIMM** generalises this to a nested sequence of variance-covariance calculations over six risk classes (IR, credit-qualifying, credit-non-qualifying, equity, commodity, FX), with weighted sensitivities $WS=RW\times s\times CR$ (risk weight × net sensitivity × concentration factor) aggregated within a class by correlations — e.g. two-tenor delta margin $\sqrt{WS_1^2+WS_2^2+2\rho\,WS_1 WS_2}$ (Gregory Table 9.7). The standardised schedule is far more conservative (Gregory §9.4.1: >\$8trn of schedule-based margin estimated for the in-scope population), which is why SIMM was built.

---

### 3. Computational Implementation — IM sizing and the SIMM aggregation

Stdlib only; reproduces Gregory's re-verified variance-covariance cases and the SIMM two-tenor delta example.

```python
import math
def inv_normal(p, lo=-10.0, hi=10.0):
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if 0.5 * (1.0 + math.erf(mid / math.sqrt(2.0))) < p: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

print("=== Variance-covariance IM:  IM = Phi^-1(alpha) * sqrt(tau) * sigma_P ===")
def im_var(alpha, days, sig_annual):
    return inv_normal(alpha) * math.sqrt(days / 252.0) * sig_annual

sig = 100.0
print(f"annual sigma_P = {sig}")
print(f"  99% 10-day : {im_var(0.99, 10, sig):.2f}   (Gregory re-verified 46.4)")
print(f"  99%  5-day : {im_var(0.99, 5,  sig):.2f}   (32.8)")
print(f"  95% 10-day : {im_var(0.95, 10, sig):.2f}   (book prints 32.8; exact product 32.67)")
q = inv_normal(0.99)
es_mult = math.exp(-0.5 * q * q) / math.sqrt(2 * math.pi) / (1 - 0.99)   # 99% ES multiplier = 2.67
print(f"  99% ES(10d): {es_mult * math.sqrt(10/252) * sig:.2f}   (multiplier 2.67 -> 53.1)")

print()
print("=== SIMM two-tenor delta margin (Gregory Table 9.7) ===")
ws1, ws2, rho = 13797.0, 43427.0, 0.84
margin2 = math.sqrt(ws1**2 + ws2**2 + 2 * rho * ws1 * ws2)
print(f"SIMM delta margin = {margin2:.0f}   (Gregory 55,524; full tenors 59,540)")
print(f"gross sum (no offset) = {ws1+ws2:.0f}")

print()
print("=== Net standardised IM: (0.4 + 0.6*NGR) x Gross IM  (Eq 7.4) ===")
def net_im(ngr, gross): return (0.4 + 0.6 * ngr) * gross
g = 60000
print(f"  NGR=1.0: {net_im(1.0, g):.0f}   NGR=0.5: {net_im(0.5, g):.0f}   "
      f"NGR=0.0: {net_im(0.0, g):.0f}   (gross 60,000)")
```
```
=== Variance-covariance IM:  IM = Phi^-1(alpha) * sqrt(tau) * sigma_P ===
annual sigma_P = 100.0
  99% 10-day : 46.34   (Gregory re-verified 46.4)
  99%  5-day : 32.77   (32.8)
  95% 10-day : 32.77   (book prints 32.8; exact product 32.67)
  99% ES(10d): 53.09   (multiplier 2.67 -> 53.1)

=== SIMM two-tenor delta margin (Gregory Table 9.7) ===
SIMM delta margin = 55523   (Gregory 55,524; full tenors 59,540)
gross sum (no offset) = 57224

=== Net standardised IM: (0.4 + 0.6*NGR) x Gross IM  (Eq 7.4) ===
  NGR=1.0: 60000   NGR=0.5: 42000   NGR=0.0: 24000   (gross 60,000)
```
The IM table shows the *same* $\sigma_P=100$ at different horizons/levels, exactly the Gregory worked examples; the SIMM line shows how correlation (84% between the two tenors) shrinks margin below the gross sum.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Margin call frequency ≠ MPoR.** A daily margin *call* is consistent with a *10-day* MPoR; the MPoR is a model parameter (delay to declare default + liquidation), not the call period. Confusing them understates the residual exposure (Gregory §7.3.3, §15.5.2).
2. **MTA ⇒ path dependency.** With a minimum transfer amount, today's margin balance depends on the *previous* balance (Tables 7.6–7.7) — margin must be modelled on a continuous grid or with look-back points, not as an independent point estimate.
3. **Threshold + MTA are additive.** Margin is only called once exposure exceeds $TH+MTA$; adding rather than combining them is a classic implementation slip (Gregory §7.3.4).
4. **IM is not VM.** Subtracting initial margin from exposure to zero (as the old CEM allowed) drove EAD to zero — a key reason SA-CCR replaced it (Gregory 13.4.2). IM covers the *MPoR gap*, VM covers the *running value*; they are different risks.

---

### 5. Canonical Literature & Study References

- **Gregory**, *The xVA Challenge*, Ch 6 (netting), Ch 7 (margin/collateral, credit support amount), Ch 9 (initial margin methodologies, SIMM, variance-covariance IM), Ch 15 (quantifying exposure, MPoR model). *Primary; numbers verified.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 24 §24.7 (netting, collateral/cure period, downgrade triggers).
- **BCBS–IOSCO (2015)**: *Margin requirements for non-centrally cleared derivatives* — the 99% / 10-day / stressed-data anchor for regulatory IM.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/04-fva-and-mva|04 · FVA & MVA]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (PFE = VaR)
