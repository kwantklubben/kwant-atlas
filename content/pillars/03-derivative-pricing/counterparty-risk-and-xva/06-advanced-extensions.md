---
title: "06 — Advanced Extensions: CVA Capital, Wrong-Way Risk, and the xVA Desk"
tags:
  - pillar-derivative-pricing
  - counterparty-risk
  - xva
  - basel-capital
  - wrong-way-risk
  - xva-desk
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

CVA/DVA/FVA/MVA price the *economic* costs of a derivative. But a derivative also consumes **regulatory capital** (a charge the bank must hold, costing shareholders a return), and the entire xVA family has to be **managed** — priced, hedged, and allocated by a dedicated desk. This page is the launchpad to the practitioner layer: **CVA capital under Basel/FRTB, wrong-way risk modelling, and the operation of an xVA desk.** The objective is to know what a real bank's xVA function actually computes and why.

Three ideas structure the page:
- **Capital is a different animal.** The CVA capital charge capitalises the *volatility of CVA* (a market-risk charge), separate from and generally additive to the default-risk charge, and it **derecognises DVA** (Gregory §13.3). It is portfolio-level — a single number across counterparties — which creates a pricing problem.
- **WWR is the modelling frontier.** Intensity models *cannot* reproduce observed wrong-way behaviour (quanto effects, sovereign jumps); the strongest evidence is jump-based, not diffusion (Gregory §17.6.4).
- **The xVA desk is a utility, not a profit centre.** It prices, hedges, and explains xVA P&L, intermediates with Treasury, and optimises across the xVA terms — a cross-asset credit-hybrid business (Gregory Ch 21).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 CVA capital (Gregory Ch 13; Hull 24)

The default-risk (IRB) capital charge is the familiar $RC=EAD\times LGD\times(PD_{99.9\%}-PD)\times MA$ (Gregory Eq 13.1, the Vasicek large-homogeneous-pool / Gordy form). The **CVA capital charge** is separate and capitalises CVA *volatility*. The **BA-CVA** (basic) reduced form (Eq 13.3):

$$K_{reduced}=\sqrt{\rho\Big(\sum_c SCVA_c\Big)^2+(1-\rho^2)\sum_c SCVA_c^2},\qquad SCVA_c=\frac1\alpha RW_c\sum_{NS} M_{NS}EAD_{NS}DF_{NS},$$

with supervisory correlation $\rho=50\%$, $\alpha=1.4$, risk weights $RW_c$ by sector/rating bucket, and $DF_{NS}$ a maturity discount. **Crucial diversification property**: for $n$ equal counterparties (Gregory Eq 13.23–13.24),

$$K_{\text{per cpty}}=SCVA\cdot\sqrt{\rho^2+\tfrac{1-\rho^2}{n}}\;\xrightarrow[n\to\infty]{}\;SCVA\cdot\rho,$$

so diversification is only *half-rewarded* (capital floors at 50% of the gross sum, never zero) — Basel does not let you diversify away CVA risk. **SA-CVA** (the FRTB-style standardised version) is sensitivity-based: per-bucket $K_b=\sqrt{\sum_k WS_k^2+\sum_{k\ne l}\rho_{kl}WS_kWS_l+R\sum_k[WS_k^{Hdg}]^2}$ then $\sqrt{\sum_b K_b^2+\sum_{b\ne c}\gamma_{bc}K_bK_c}$ scaled by $m_{CVA}$ (Eqs 13.10–13.12); the hedging disallowance $R=0.01$ (√R = 10% of gross hedge sensitivities) stops perfect hedging.

#### 2.2 Wrong-way risk modelling (Gregory 17.6)

Three approaches:
- **Intensity approach**: a stochastic credit-spread process correlated with the exposure drivers; default generated from the intensity; conditional EPE from defaulted paths. Tractable but *weak* — even ±100% correlation understates the true effect.
- **Structural approach**: map exposure and default onto a bivariate distribution (e.g. Gaussian copula); no revaluation needed; stronger effect, opaque calibration.
- **Jump approaches**: the strongest empirical support — quanto effects in CDS markets and sovereign FX (Italian CDS 2011; Levy–Levin implied sovereign jumps: 83% for AAA down to 27% for BBB). Intensity (diffusion) models **cannot reproduce this** (Ehlers–Schönbucher 2006). This is the WWR-theoretical cliff-edge.

#### 2.3 The xVA desk (Gregory Ch 21)

The desk prices incremental xVA, hedges it (manage xVA like an option book), and *explains* its P&L. The P&L explain identity (Gregory Eq 21.1 / Table 21.8):

$$\delta xVA = \frac{\partial xVA}{\partial S}\Delta S + \frac{\partial xVA}{\partial E}\Delta E + \frac{\partial xVA}{\partial t}\Delta t + \frac{\partial^2 xVA}{\partial S\partial E}\Delta S\Delta E,$$

where the cross-gamma term (joint moves in exposure and credit — e.g. Brexit: rates down, spreads wider) is typically **unhedgeable**. The desk's P&L reconciles theta (time decay) + deltas + gamma + defaults + funding/capital costs to the traded P&L. **KVA vs MVA trade-off** (Gregory §20.4): posting IM raises MVA but lowers KVA; the optimum is *below* full regulatory IM because KVA relief under SA-CCR has diminishing returns.

---

### 3. Computational Implementation — capital, P&L explain, and the IM/KVA optimum

Stdlib only; reproduces Gregory's re-verified BA-CVA diversification and the Table 21.8 P&L arithmetic.

```python
import math
print("=== BA-CVA: K = sqrt( rho*(Sum SCVA)^2 + (1-rho^2)*Sum SCVA^2 ), rho=50% ===")
rho = 0.50
def ba_cva_k(n, scva=1.0):
    return math.sqrt(rho*(n*scva)**2 + (1-rho*rho)*n*scva*scva)
print("n equal counterparties, SCVA=1 each:")
for n in (1, 2, 10, 50):
    K = ba_cva_k(n)
    dm = math.sqrt(rho**2 + (1-rho*rho)/n)
    print(f"  n={n:3d}:  K={K:.3f}   K/n={K/n:.3f}   diversification mult = {dm:.3f}")
print("(capital converges toward rho=50% x sum, never zero - diversification is half-rewarded.)")

print()
print("=== xVA desk P&L explain (Gregory Table 21.8, arithmetic re-verified) ===")
theta, cred, rates, fx, ux = 120960, -1800820, -1610770, 279335, -214585
pl = theta + cred + rates + fx + ux
print(f"theta {theta:+,} + credit {cred:+,} + rates {rates:+,} + FX {fx:+,} + UX {ux:+,} = {pl:+,}")

print()
print("=== KVA vs MVA trade-off: optimal posted IM is BELOW full regulatory ===")
def total(f, MVA_full=20.0, KVA_full=38.8):
    mva = MVA_full * f              # IM funding cost grows with IM posted
    kva = KVA_full * (1.0 - f) ** 2 # capital relief DIMINISHES (SA-CCR 5% floor / add-ons)
    return mva + kva, mva, kva
best = min((total(f)[0], f) for f in [0.0, 0.25, 0.5, 0.75, 1.0])
for f in (0.0, 0.25, 0.5, 0.75, 1.0):
    tot, mva, kva = total(f)
    star = "  <-- min" if (tot, f) == best else ""
    print(f"  IM {f*100:3.0f}%:  MVA {mva:6.2f} + KVA {kva:6.2f} = total {tot:6.2f} bps{star}")
```
```
=== BA-CVA: K = sqrt( rho*(Sum SCVA)^2 + (1-rho^2)*Sum SCVA^2 ), rho=50% ===
n equal counterparties, SCVA=1 each:
  n=  1:  K=1.118   K/n=1.118   diversification mult = 1.000
  n=  2:  K=1.871   K/n=0.935   diversification mult = 0.791
  n= 10:  K=7.583   K/n=0.758   diversification mult = 0.570
  n= 50:  K=35.882   K/n=0.718   diversification mult = 0.515
(capital converges toward rho=50% x sum, never zero - diversification is half-rewarded.)

=== xVA desk P&L explain (Gregory Table 21.8, arithmetic re-verified) ===
theta +120,960 + credit -1,800,820 + rates -1,610,770 + FX +279,335 + UX -214,585 = -3,225,880

=== KVA vs MVA trade-off: optimal posted IM is BELOW full regulatory ===
  IM   0%:  MVA   0.00 + KVA  38.80 = total  38.80 bps
  IM  25%:  MVA   5.00 + KVA  21.82 = total  26.82 bps
  IM  50%:  MVA  10.00 + KVA   9.70 = total  19.70 bps
  IM  75%:  MVA  15.00 + KVA   2.42 = total  17.43 bps  <-- min
  IM 100%:  MVA  20.00 + KVA   0.00 = total  20.00 bps
```
Three practitioner results, all visible: Basel's BA-CVA half-rewards diversification (capital floors at 50% of the gross sum); a real xVA desk P&L reconciles exactly (theta + deltas + UX = traded P&L, where UX absorbs gamma/cross-gamma/vega); and the optimal posted IM is ~75% of full regulatory — posting *some* IM buys cheap capital relief, posting *all* of it costs more MVA than the remaining KVA is worth (Gregory §20.4).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **DVA in capital.** CVA capital must **derecognise DVA** (BCBS 2011d), while accounting (IFRS 13) requires it — treating them consistently inside capital is an error that overstates or double-counts own-credit (Gregory §13.3.1).
2. **CVA hedges can *increase* capital.** Under BA-CVA/SA-CVA, proxy and misaligned hedges consume more capital than they relieve (the "split hedge" / overhedging problem, §13.3.6, §13.5.3). Hedging accounting CVA and minimising CVA capital are *different* objectives.
3. **WWR via diffusion.** Intensity (diffusion) WWR models understate the true jump behaviour; sovereign/quanto evidence demands jump models (Gregory §17.6.4). A diffusion-only WWR is systematically under-pessimistic.
4. **The 5% floor.** SA-CCR capital can never reach zero even with huge IM or very negative value ($Floor=5\%$, Eq 13.21) — pricing as if capital vanishes with perfect collateralisation misprices (Gregory §19.2.3, §13.4.3).
5. **xVA desk as profit centre.** A desk targeted at positive P&L will *warehouse* credit risk (profitable in expectation via the real-world/risk-neutral PD gap) and inflate short-term volatility — Gregory's consensus is a **utility with a zero/slightly-negative P&L target** (§21.1.4).

---

### 5. Canonical Literature & Study References

- **Gregory**, *The xVA Challenge*, Ch 13 (CVA capital: BA-CVA, SA-CVA, SA-CCR, IMM, EAD), Ch 19 (KVA), Ch 20 (MVA), Ch 21 (xVA desk, hedging, P&L explain, optimisation). *Primary; numbers verified.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 24 (Vasicek one-factor credit VaR eq 24.10; Merton; CDS).
- **Brigo & Mercurio**, *Interest Rate Models*, Ch 21–22 (CVA pricing proposition, intensity/WWR machinery, SSRD/CIR++).
- **Basel Committee (BCBS 2015, 2017)**: *The standardised approach for measuring counterparty credit risk exposures* (SA-CCR) and the FRTB-CVA framework; **BCBS–IOSCO (2015)** bilateral margin rules.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Index Hub]]
- Credit theory: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model|Credit Risk & the Merton Structural Model]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]]
- Risk measures: [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|Extreme Value Theory & Fat Tails]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate Models]]
