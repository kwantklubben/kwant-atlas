---
title: "01 — Calibration from Zero: What It Is & Why It's Not a Forecast"
tags:
  - pillar-derivative-pricing
  - calibration-and-market-practice
  - intuition
  - model-calibration
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/index|Black-Scholes-Merton Hub]]. No prior derivatives knowledge needed.

---

### 1. Intuition & Practical Objective

Start with the dumbest possible question: *if Black-Scholes says an option has one price, why does a desk need a "calibration" step at all?* Because the model has free parameters (volatility, and in fancier models several of them), and the market has already decided the *actual* prices. **Calibration is the act of choosing the parameters so the model agrees with the market.** Everything else on this page is unpacking that sentence.

Think of a model as a machine with dials. You feed it a strike and a maturity and it prints a price. The dials are $\\theta$ (for BSM just $\\sigma$; for Heston $v_0,\\bar v,\\lambda,\\eta,\\rho$; for SABR $\\alpha,\\beta,\\rho,\\nu$). Market quotes are the *answer key*. Calibration turns the dials until the machine's answers match the key.

Three things to un-learn first:

1. **Calibrating is not fitting history, and it is not forecasting.** You are not averaging past prices and you are not predicting the future. You are solving: "what parameter values make this model's *today* quotes equal the market's *today* quotes?" The parameters are a static snapshot of the market's view, not a law of motion.
2. **The market is the authority, not the model.** When model and market disagree, it is the *model* that is wrong. Calibration makes the model bow to the market. The moment you change the parameters tomorrow (recalibration), you are admitting the previous parameters were only ever a best-fit to yesterday.
3. **A good fit is necessary, not sufficient.** Fitting the smile perfectly does not mean the model's *dynamics* are right. Two models can agree on every vanilla price today and disagree violently on an exotic or a hedge ratio tomorrow (Bergomi Ch 2: this is the local-vol vs stochastic-vol distinction, and Ch 8: the volatility-of-volatility expansion).

---

### 2. Mathematical Ground Truth & Derivations

**The calibration problem, written down.** We observe $N$ market quotes $\\{O_i^{\\text{mkt}}\\}$ (option prices, or equivalently implied vols $\\hat\\sigma_i$). We pick a pricing function $P_i(\\theta)$ (model price for quote $i$ under parameters $\\theta$). Calibration is

$$\\hat\\theta = \\arg\\min_\\theta \\; \\mathcal{L}\\big(P_1(\\theta),\\dots,P_N(\\theta);\\; O_1^{\\text{mkt}},\\dots,O_N^{\\text{mkt}}\\big),$$

where $\\mathcal L$ is an **objective function** (a distance; the lookup table is on the [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]]). For BSM with a single free parameter $\\sigma$, this is a one-dimensional root-finding/minimization: find $\\sigma$ so the model call price equals the market call price.

**The single-parameter case is already instructive.** Given one market option, $\\sigma$ is chosen so $P(\\sigma)=O^{\\text{mkt}}$. Invert BSM: this $\\sigma$ is called the **implied volatility** — it is literally the BSM parameter calibrated to that one quote. With several quotes at once (a smile), no single $\\sigma$ fits all, so you must *trade off* which strikes matter most. That trade-off is exactly the choice of objective function.

**Two dangers that appear even here.**
- *Objective mismatch:* the price-RMSE optimum and the vol-RMSE optimum differ, because price is a nonlinear function of vol (dollar-weighted toward ATM).
- *Over-determination:* with more quotes than parameters, the fit is a compromise; the *residuals* tell you where the model is structurally wrong (the smile BSM cannot reach).

---

### 3. Computational Implementation — one dial, two objectives, two answers

Fit a *single* BSM vol $\\sigma$ to the whole market smile, first minimizing **price RMSE**, then **implied-vol RMSE**. The two answers differ — proof that the objective function is a real choice. Stdlib only.

```python
import math

def N(x):  return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

def bsm_call(S,X,T,r,sig):
    d1=(math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*N(d1)-X*math.exp(-r*T)*N(d2)

S0, T, r = 100.0, 1.0, 0.02
strikes = [70,80,90,100,110,120,130]
mkt_vol = [0.34,0.28,0.235,0.205,0.22,0.25,0.29]          # market smile
mkt_prc = [bsm_call(S0,K,T,r,v) for K,v in zip(strikes,mkt_vol)]

def prmse(sig):  # price RMSE  (dollar-weighted -> ATM dominates)
    return math.sqrt(sum((bsm_call(S0,K,T,r,sig)-p)**2 for K,p in zip(strikes,mkt_prc))/len(strikes))
def vrmse(sig):  # implied-vol RMSE (all strikes equal in vol space)
    return math.sqrt(sum((sig-v)**2 for v in mkt_vol)/len(mkt_vol))

def minimize(f,a,b,tol=1e-8):   # golden-section search, 1-D
    gr=(math.sqrt(5)-1)/2; c=b-gr*(b-a); d=a+gr*(b-a); fc,fd=f(c),f(d)
    while abs(b-a)>tol:
        if fc<fd: b,d,fd=d,c,fc; c=b-gr*(b-a); fc=f(c)
        else:     a,c,fc=c,d,fd; d=a+gr*(b-a); fd=f(d)
    return (a+b)/2

sig_p = minimize(prmse,0.05,0.6)
sig_v = minimize(vrmse,0.05,0.6)
print(f"price-RMSE-optimal sigma = {sig_p:.5f}   prmse={prmse(sig_p):.5f}")
print(f"vol-RMSE-optimal  sigma  = {sig_v:.5f}   vrmse={vrmse(sig_v):.5f}")
print(f"price RMSE of the vol-optimal fit = {prmse(sig_v):.5f}")
print(f"vol   RMSE of the price-optimal  = {vrmse(sig_p):.5f}")
```
```
price-RMSE-optimal sigma = 0.23904   prmse=1.03628
vol-RMSE-optimal  sigma  = 0.26000   vrmse=0.04318
price RMSE of the vol-optimal fit = 1.21277
vol   RMSE of the price-optimal  = 0.04799
```
Price-RMSE picks $\\sigma{=}0.239$ (biased to ATM where prices are largest); vol-RMSE picks $\\sigma{=}0.26$ (spreads error evenly across the smile). **Same market, same model, one free parameter — two calibrations.** That is the seed of the whole folder: calibration is a *decision*, not a computation.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating calibration as "the answer."** A best-fit $\\theta$ is conditional on today's quotes. Recalibrating tomorrow changes it — so any derivative priced on it inherits recalibration drift (see [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes]]).
2. **The residual you can't fit is information.** If a one-$\\sigma$ BSM fit leaves a systematic smile-shaped error, that is not noise to shrug off — it is the model telling you it is structurally wrong (constant vol cannot reach the wings). This is the motivation for local/stochastic vol.
3. **Wrong objective ⇒ wrong parameter.** Fitting in price space quietly ignores the wings; fitting in vol space can leave large dollar mispricings at ATM. Choose deliberately and report both.
4. **More parameters ≠ better.** A richer model (SABR, Heston) fits better but invites non-identifiability and overfitting — the machine has too many dials and many dial-settings print the same prices.

---

### 5. Canonical Literature & Study References

- **Bergomi**, *Stochastic Volatility Modeling*, Ch 1 (the break-even/P&L view that frames *why* we calibrate to market quotes), Ch 7 §7.5 (what "calibration" of a forward-variance model means and does not mean).
- **Gatheral**, *The Volatility Surface*, Ch 3 (calibration options for the implied-vol surface; why parameterizing implied vol directly is hard — sparse quotes and no-arbitrage interpolation).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 (volatility smiles: how they force calibration beyond BSM).

---

### 6. Connected Graph Bridges

- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black-Scholes-Merton Hub]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Continue: [[pillars/03-derivative-pricing/calibration-and-market-practice/02-the-calibration-problem|02 · The Calibration Problem]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
