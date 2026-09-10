---
title: "05 — Failure Modes & Desk Practice: Stability, Identifiability, Conventions"
tags:
  - pillar-derivative-pricing
  - calibration-and-market-practice
  - failure-modes
  - ill-posed
  - market-data
  - conventions
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/calibration-and-market-practice/03-calibrating-local-vol|03 · Calibrating Local Vol]] and [[pillars/03-derivative-pricing/calibration-and-market-practice/04-calibrating-stochastic-vol|04 · Calibrating Stochastic Vol]].

---

### 1. Intuition & Practical Objective

This page names the three ways calibration goes wrong — **overfitting**, **instability**, **non-identifiability** — ties each to a first-principles cause, and then describes how a real desk survives them (market data, conventions, and the discipline of *distrusting* the calibrated model). The objective is not cynicism: it is knowing precisely *which* assumptions to distrust so the residual model risk can be measured and managed.

Three structural facts do the damage:
1. **Differentiation amplifies noise.** Local vol needs *second derivatives* of prices; noisy quotes ⇒ huge local-vol spikes or negative variance. (Ill-posedness.)
2. **The smile fixes combinations, not parameters.** SABR's $\\beta/\\rho$, Heston's $\\kappa/\\eta$ are collinear; different parameters fit identically. (Non-identifiability.)
3. **The model is static but the market is not.** A parameter set fit to today is not a law of motion; recalibration drift is real P&L risk. (Overfitting + model risk.)

---

### 2. Mathematical Ground Truth & Derivations

**Ill-posedness of the local-vol inversion (Gatheral 1.10; Bergomi 2.19).** The local variance is

$$v_L(y,T) = \\frac{\\partial w/\\partial T}{1-\\tfrac{y}{w}w_y+\\tfrac14\\big(-\\tfrac14-\\tfrac1w+\\tfrac{y^2}{w^2}\\big)w_y^2+\\tfrac12 w_{yy}},$$

which contains $w_{yy}$ — a **second finite difference**. If observed with noise $\\varepsilon$ at grid spacing $dy$, the second difference has error $\\sim \\varepsilon/dy^2$, and the denominator $\\tfrac12w_{yy}$ can be driven to $0$ (or negative, i.e. strike arbitrage / negative butterfly). Near a zero denominator, $v_L\\to\\pm\\infty$. This is the textbook ill-posed inverse problem: the forward map (smile → local vol) is smoothing, so its inverse is unstable.

**Non-identifiability (Bergomi Ch 6, Ch 8; Gatheral Ch 3).** The ATMF skew is, to first order, a *weighted integral of the instantaneous spot/vol covariance*:

$$\\mathcal S_T = \\frac{1}{\\hat\\sigma_T^2T}\\int_0^T\\frac{T-t}{T}\\big\\langle d\\ln S_t\\,d\\hat\\sigma_T(t)\\big\\rangle\\,dt \\qquad \\text{(Bergomi eq 2.89)}.$$

The *combination* is fixed by the smile; how it is split between $\\rho$ and $\\eta$ (or $\\beta$ and $\\rho$) is not. That split changes the **dynamics** ($R_T$, the skew-stickiness ratio) without changing the static fit — hence identical fits with different hedge ratios.

**Conventions that quietly change the answer.** Calibration output is only meaningful given a convention set (Bergomi Ch 5 on variance swaps makes this vivid): implied vs realized vol, log-returns vs arithmetic returns in the variance payoff ($\\ln^2$ vs standard returns flips the sign of the third-order term), $\\ln K/F$ vs $\\ln K/S$ moneyness, per-point vs per-unit vol scaling, the dividend model (continuous yield vs discrete), and the discount curve. Two desks with the same data and model but different conventions report different calibrated parameters.

---

### 3. Computational Implementation — instability in numbers

Reconstruct local vol from a smooth smile *with and without* realistic bid/ask noise (~0.4 vol pts, white across strikes). The differentiation amplifies the noise catastrophically. Stdlib only.

```python
import math, random
random.seed(3)
def atm(T): return 0.15 + 0.05*math.exp(-T)
def sbar(y,T): return atm(T)*(1.0-0.30*y+0.50*y*y)
def clean_w(y,T): return T*sbar(y,T)**2

def v_loc_fd(wfun,y,T,dy=0.05,dT=0.01):          # finite-difference Gatheral (1.10)
    wy=(wfun(y+dy,T)-wfun(y-dy,T))/(2*dy)
    wyy=(wfun(y+dy,T)-2*wfun(y,T)+wfun(y-dy,T))/(dy*dy)
    wt=(wfun(y,T+dT)-wfun(y,T-dT))/(2*dT)
    W=wfun(y,T)
    den=1.0-(y/W)*wy+0.25*(-0.25-1.0/W+y*y/(W*W))*wy*wy+0.5*wyy
    return wt/max(den,1e-9), den

noise=[(round(-0.5+0.05*i,3), random.gauss(0,0.004)) for i in range(21)]  # ~0.4 volpt bid/ask
def noisy_w(y,T):
    j=min(range(len(noise)),key=lambda i:abs(noise[i][0]-y))
    return T*(sbar(y,T)+noise[j][1])**2

T=0.5
print("Local vol from a smooth smile vs from the same smile + bid/ask noise:")
for y in (-0.30,-0.20,-0.10,0.0,0.10,0.20):
    vc,_=v_loc_fd(clean_w,y,T); vn,dn=v_loc_fd(noisy_w,y,T)
    print(f"  y={y:+.2f}: clean v_loc={vc:6.4f}   noisy v_loc={vn:11.3f}   (denominator {dn:+.4f})")
vals=[v_loc_fd(noisy_w,round(-0.45+0.05*i,3),T)[0] for i in range(19)]
print("  noisy v_loc over full grid: min=%.4f  max=%.2f   (true level ~0.024-0.048)"%(min(vals),max(vals)))
bad=sum(1 for v in vals if v<0 or v>0.3)
print("  points with negative/absurd v_loc (of %d): %d"%(len(vals),bad))
```
```
Local vol from a smooth smile vs from the same smile + bid/ask noise:
  y=-0.30: clean v_loc=0.0480   noisy v_loc=      0.043   (denominator +0.8060)
  y=-0.20: clean v_loc=0.0375   noisy v_loc=      0.130   (denominator +0.2633)
  y=-0.10: clean v_loc=0.0308   noisy v_loc=      0.026   (denominator +1.1101)
  y=+0.00: clean v_loc=0.0266   noisy v_loc=      0.036   (denominator +0.7885)
  y=+0.10: clean v_loc=0.0243   noisy v_loc=      0.033   (denominator +0.7913)
  y=+0.20: clean v_loc=0.0236   noisy v_loc=      0.027   (denominator +0.9148)
  noisy v_loc over full grid: min=0.0167  max=43406990.52   (true level ~0.024-0.048)
  points with negative/absurd v_loc (of 19): 1
```
A *0.4-vol-point* wiggle in the smile blows one reconstructed local variance up to **$4.3\\times10^7$** — six orders of magnitude above the true level — and swings the butterfly denominator to near zero. This is why desks never invert raw quotes: they first fit a **smooth, arbitrage-free parametric surface** (SVI, a parametric LV, a calibrated SV model) and only then invert, and they clip/smooth the result. The instability is structural, not a code bug.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Ill-posed inversion (differentiation amplifies noise ~$1/dy^2$).** The local-vol map needs second derivatives of prices; raw-quote noise explodes it (Experiment above). *Fix:* smooth/parameterize the smile first, regularize, clip local variance to be positive and bounded.
2. **Non-identifiability (smile fixes combinations, not parameters).** SABR $\\beta/\\rho$ and Heston $\\kappa/\\eta$ trade off; identical fits, different hedges. *Fix:* fix a convention ($\\beta{=}0.5$ equity, $\\beta{=}1$ FX), use term structure, or ridge-regularize toward a prior ([[pillars/03-derivative-pricing/calibration-and-market-practice/04-calibrating-stochastic-vol|04 · Stochastic Vol]]).
3. **Overfitting (rich model, sparse data).** Enough parameters drive today's residuals to zero and tomorrow's prices to nonsense — the far wings have few quotes, so that is where overfit surfaces break. *Fix:* cross-validate, penalize (ridge), check no-arbitrage (butterfly $\\ge0$, total variance increasing in $T$).
4. **Convention drift.** Two desks with identical data and model but different conventions (moneyness, log vs arithmetic returns, dividend model, discount curve, per-point scaling) get different parameters — a silent reconciliation risk.
5. **Recalibration drift (model risk).** The calibrated model is static; when the market moves you recalibrate, and the *change* in the calibrated surface is itself unhedgeable P&L (Bergomi Ch 2.6: LV future skews are not lockable). The desk prices the deal *and* the cost of holding the model's dynamics.
6. **Incomplete-market assumption ($\\phi{=}0$).** Setting the price of vol risk to zero is a choice; it is invisible in the vanilla fit but changes exotic prices.

**Desk practice distilled.** *Fit in implied vol (the quoted unit). Smooth, then invert (never invert raw quotes). Fix or regularize the non-identifiable parameters. Check no-arbitrage after every calibration. Report residuals — they flag where the model is structurally wrong. And treat every calibration as a snapshot, not a law of motion.*

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 1 & 3 (local-vol inversion eq 1.10; SVI as a smooth arbitrage-free surface; why direct implied-vol parameterization is hard with sparse quotes).
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 2 (eq 2.89: skew = covariance integral; eq 2.20 interpolation; instability and the "no physical significance" warning; Ch 2.6 on forward skews), Ch 5 (conventions: $\\ln^2$ vs returns, dividends, eqs 5.31–5.54).
- **Duffy**, *Finite Difference Methods in Financial Engineering*, Ch 8–12 (numerical stability of the schemes used once a calibrated LV surface must be *priced* with).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 (smiles, model risk, calibration in practice).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/calibration-and-market-practice/04-calibrating-stochastic-vol|04 · Calibrating Stochastic Vol]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/calibration-and-market-practice/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-and-sabr|Heston & SABR]] · [[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva|Counterparty Risk & XVA]]
