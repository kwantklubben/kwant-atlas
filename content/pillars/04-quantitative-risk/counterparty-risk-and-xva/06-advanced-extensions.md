---
title: "06 — Advanced Extensions: FVA, MVA, KVA and WWR Modelling"
tags:
  - pillar-quantitative-risk
  - counterparty-risk-and-xva
  - fva
  - mva
  - kva
  - xva
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]] and [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

Counterparty risk is only the first cost of trading derivatives. A firm also **funds** the position, posts **initial margin**, and holds **regulatory capital** against it. Each of these has a price, and each gets its own adjustment. Together they are the **xVA** family:

$$
\text{Actual value}=\text{Base value}+\text{ColVA}-\text{CVA}+\text{DVA}-\text{FVA}-\text{MVA}-\text{KVA}.
$$

The practical objective is to see that **all the xVAs are the same integral shape** — an expected *usage profile* against a *cost curve* — so CVA is a template, not a special case:

| xVA | Usage profile (market component) | Cost curve (cost component) |
|---|---|---|
| CVA / DVA | EPE / ENE | counterparty / own default probability |
| FVA | EFV (expected future value) | own funding spread |
| MVA | EIM (expected initial margin) | IM funding spread |
| ColVA | expected collateral balance | collateral remuneration gap |
| KVA | expected capital (ECP) | cost of capital |

> **The two halves of funding.** **FVA is the cost of being *under*-collateralised** (you must fund the variation-margin shortfall). **MVA is the cost of being *over*-collateralised** (you must fund the posted initial margin). FVA can be a *benefit*; MVA essentially cannot.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 FVA = FCA + FBA

Funding value adjustment mirrors CVA but replaces the counterparty's credit spread with **your own funding spread** $FS$, and the exposure with the **expected future value** EFV (Gregory §18.2):

$$
\text{FVA}=-\sum_{i=1}^{m}\text{EFV}(t_i)\,\text{FS}(t_{i-1},t_i)\,(t_i-t_{i-1})=\text{FCA}+\text{FBA},\tag{18.3}
$$
$$
\text{FCA}=-\sum_i \text{EPE}(t_i)\,\text{FS}\,\Delta t,\qquad \text{FBA}=-\sum_i \text{ENE}(t_i)\,\text{FS}\,\Delta t.\tag{18.4}
$$

Positive value (an asset) must be funded → **FCA** cost; negative value (a liability) is a funding source → **FBA** benefit. The **Burgard–Kjær** integral form makes the analogy exact:
$$
\text{FCA}(t)=-\int_t^\infty \text{FS}(t,u)\,D_{r+\lambda_P+\lambda_C}(t,u)\,\text{EPE}(t,u)\,du.\tag{18.5}
$$

#### 2.2 The DVA/FBA double-count — the one thing to get right

**DVA and FBA are two names for the same benefit of a negative exposure.** DVA books it as *avoided payment on own default*; FBA books it as *funding relief*. Including both discounts the same cash flow twice (§18.2.5). When the funding spread equals the own-credit LGD-weighted hazard ($\text{FS}=\text{LGD}_P\lambda_P$), the two are **identical** (Burgard–Kjær). So a firm must choose exactly one of:

- **`CVA + FCA + FBA`** — "CVA + symmetric funding" (consistent with Basel III, which has no DVA), **or**
- **`CVA + DVA + FCA`** — "bilateral CVA + asymmetric funding".

Never `CVA + DVA + FCA + FBA`.

> **The FVA debate (Gregory §18.2.6).** Hull–White (2012a, 2014) argue funding costs should *not* enter a risk-neutral value: including them breaks the law of one price and creates arbitrage (buy from a low-funding bank, sell to a high-funding bank). The counter-view (Castagna, Carver, Kenyon–Green) is that there is *no market* for uncollateralised derivatives, so the "fair value" argument is void and FVA is real. Current settlement: FVA belongs in **pricing** (entry price maximising shareholder value); the debate persists on **valuation**. Only the *non-default* (liquidity) part of a funding spread is universally accepted as a true FVA — estimable from the CDS–bond basis. Hull–White's own decomposition reads $\text{CVA}+\text{DVA}+\text{FCA}+\text{DVA}_2$ (DVA₂ = benefit of defaulting on *funding* liabilities), which nets back to CVA+DVA at the firm level.

#### 2.3 MVA

Initial margin must be posted, segregated (non-rehypothecable), and funded. Its cost is
$$
\text{MVA}=-\int_0^\infty \mathbb{E}[\text{IM}(u)]\,\text{FS}(u)\,du\approx\sum_{i}\text{EIM}(t_i)\,\text{FS}(t_{i-1},t_i)\,(t_i-t_{i-1}).\tag{20.1}
$$

Key facts (§20.2–20.4): MVA is **asymmetric** (segregation means it is a cost only, never a benefit); the EIM profile can be **non-monotonic** (a large offsetting trade ageing out can *raise* future IM); and MVA is **not** trivially computed alongside CVA — future SIMM sensitivities are needed. **MVA and KVA are not mutually exclusive** (§20.4): posting more IM *raises* MVA but can *lower* KVA (less capital), and the optimum bilateral IM posting is generally **below** the full regulatory requirement.

#### 2.4 Modelling WWR (the rigorous route)

Beyond the correlation trick of [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05]], two families (Gregory §17.6.3):
- **Intensity approach** — a stochastic credit-spread intensity correlated with the exposure drivers; default drawn from the intensity. Tractable, but even $\pm100\%$ correlation tends to *understate* the true effect.
- **Structural approach** — map exposure and default distributions onto a **bivariate distribution (e.g. a Gaussian copula)**; no revaluation needed, stronger effect, but the dependence is opaque and hard to calibrate.
- **Jump approach** — the strongest empirical support: allow the exposure to jump *at* default. The only family that makes collateral genuinely ineffective.

---

### 3. Computational Implementation — FVA, the DVA/FBA overlap, and MVA

Build an ITM forward's EFV/EPE/ENE profile, compute FCA/FBA/FVA, show numerically that **DVA ≈ FBA** (so adding both double-counts), and price MVA from an initial-margin profile. Standard library only.

```python
import math, random

def Phi(x):  return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))

def profile_ITM(S0, K, T, r, sig, nsteps, npaths, seed=3):
    """ITM forward: V_t = S_t - K e^{-r(T-t)}, E[V_t] = S0 e^{rt} - K e^{-r(T-t)} > 0."""
    random.seed(seed); dt = T/nsteps
    EFV=[0.0]*(nsteps+1); EPE=[0.0]*(nsteps+1); ENE=[0.0]*(nsteps+1)
    for _ in range(npaths):
        S = S0
        for i in range(1, nsteps+1):
            t = i*dt
            S *= math.exp((r-0.5*sig**2)*dt + sig*math.sqrt(dt)*random.gauss(0,1))
            V = S - K*math.exp(-r*(T-t))
            EFV[i]+=V; EPE[i]+= max(V,0.0); ENE[i]+= min(V,0.0)
    return ([e/npaths for e in EFV],[e/npaths for e in EPE],[e/npaths for e in ENE])

S0, K, T, r, sig = 100.0, 95.0, 5.0, 0.03, 0.25
nsteps, npaths = 20, 100000; dt = T/nsteps
EFV, EPE, ENE = profile_ITM(S0, K, T, r, sig, nsteps, npaths)
disc = [math.exp(-r*i*dt) for i in range(nsteps+1)]

FS = 0.0100                                  # own funding spread 100bp
FCA = -sum(disc[i]*EPE[i]*FS*dt for i in range(1, nsteps+1))
FBA = -sum(disc[i]*ENE[i]*FS*dt for i in range(1, nsteps+1))
print(f"ITM forward: EFV(2y)={EFV[8]:.3f}  EPE(avg)={sum(EPE[1:])/nsteps:.3f}  ENE(avg)={sum(ENE[1:])/nsteps:.3f}")
print(f"FCA (funding cost)    = {FCA:8.4f}")
print(f"FBA (funding benefit) = {FBA:8.4f}")
print(f"FVA = FCA + FBA       = {FCA+FBA:8.4f}")

# --- DVA vs FBA: double counting when FS = LGD*lambda_P (Burgard-Kjaer) ---
s_P, LGD_P = 0.0100, 0.60; lam_P = s_P/LGD_P
DVA = -LGD_P*sum(disc[i]*ENE[i]*(math.exp(-lam_P*(i-1)*dt)-math.exp(-lam_P*i*dt)) for i in range(1, nsteps+1))
print(f"DVA (own credit)      = {DVA:8.4f}   == FBA = {FBA:8.4f}  (both from ENE -> do not add)")

# --- MVA: funding cost of posting initial margin over the life ---
FS_IM = 0.0080                               # 80bp IM funding spread
EIM_const = 2.33*math.sqrt(10.0/252.0)*sig*S0
MVA_const = sum(EIM_const*FS_IM*dt for i in range(1, nsteps+1))
EIM_decay = lambda t: (1.0 - t/T)*EIM_const
MVA_decay = sum(EIM_decay(i*dt)*FS_IM*dt for i in range(1, nsteps+1))
print(f"EIM (constant)        = {EIM_const:8.2f}   MVA = {MVA_const:8.4f}")
print(f"EIM (linear decay)    = {EIM_const/2:8.2f}   MVA = {MVA_decay:8.4f}")
```
```
ITM forward: EFV(2y)=19.148  EPE(avg)=27.192  ENE(avg)=-7.617
FCA (funding cost)    =  -1.2477
FBA (funding benefit) =   0.3439
FVA = FCA + FBA       =  -0.9038
DVA (own credit)      =   0.3258   == FBA =   0.3439  (both from ENE -> do not add)
EIM (constant)        =    11.60   MVA =   0.4641
EIM (linear decay)    =     5.80   MVA =   0.2205
```
Read the block: the ITM forward is an **asset** (EPE avg 27.2 vs ENE avg −7.6), so funding it costs **FCA = −1.25**; the small negative-exposure tail gives back **FBA = +0.34**, leaving **FVA = −0.90**. The critical line is **DVA (0.33) ≈ FBA (0.34)** — literally the same benefit computed two ways, which is *why* they must never be summed. And **MVA (0.46)** is the price of funding a constant ~\$11.6 IM; if the IM profile is assumed to decay linearly, MVA halves to **0.22** — a reminder that the *EIM shape* is where MVA model risk lives.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Summing DVA and FBA.** The single most common xVA accounting error — it double-counts the negative-exposure benefit (§2.2). Pick one framework and stick to it.
2. **Hedging the wrong FVA.** Only the *non-default* (liquidity) component of a funding spread is a genuine economic cost; the credit-default component overlaps with DVA. Using the whole bond spread inflates FVA (Morini–Prampolini; Hull–White 2014).
3. **MVA EIM oversimplification.** Forward-IM or amortisation proxies are decent for linear swap portfolios but **bad** for options and CCP-style methodologies, where IM is convex (§20.2.3). Understating EIM understates MVA.
4. **MVA/KVA asymmetry ignored.** Treating MVA and KVA inconsistently (pricing one, not the other) incentivises sub-optimal structures — 'backloading' to a CCP or discretionary IM that looks cheap on one adjustment but costs more on the other (§20.4).
5. **WWR model choice is not neutral.** Intensity models understate the effect; structural models are hard to calibrate; only jump models reproduce the empirically observed magnitudes. Choosing the intensity approach "because it is tractable" systematically understates CVA.
6. **The recursive valuation problem.** The true value is both an input to and an output of xVA (close-out references a value that already contains xVA). Practice uses linear superposition on a base value — an approximation that fails exactly when xVA is large (§3.3.2).

---

### 5. Canonical Literature & Study References

- **Gregory, Jon**: *The xVA Challenge* (5th ed., 2025) — Ch 16 (ColVA, base value, discounting), Ch 18 (FVA: Eqs 18.2–18.5, the double-count framework, the Hull–White debate), Ch 19 (KVA), Ch 20 (MVA: Eq 20.1, EIM, MVA/KVA link), §17.6.3 (WWR models), Ch 21 (xVA-desk hedging and JTD). *Deep-read and numerically re-verified in the corpus.*
- **Burgard & Kjær** (2011a,b, 2013): the funding-cost derivation and the conditions under which DVA ≡ FBA.
- **Hull & White** (2012a, 2014): the case against FVA in valuation; **Andersen, Duffie & Song** (2016): the shareholder-value view that FVA belongs in entry prices.
- **Brigo, Morini & Pallavicini** (2013): the rigorous CVA/FVA-with-collateral pricing framework.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]]
- Hub: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA — Topic Hub]]
- Sibling: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]
