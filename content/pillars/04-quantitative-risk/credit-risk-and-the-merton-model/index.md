---
title: "4.4 Credit Risk & the Merton Model"
tags:
  - pillar-quantitative-risk
  - credit-risk-and-the-merton-model
  - credit-risk
  - merton-model
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (the equity-as-call identity *is* BSM) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (CDFs, the normal quantile $N^{-1}$). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Credit risk is the risk of loss when a borrower does not pay. The *pricing* problem is subtle: unlike a stock, a bond's payoff depends on a **discrete, terminal, catastrophic event** — default — and the firm's ability to pay is not directly observable. Merton (1974) produced the founding insight in one stroke:

> **A firm's equity is a European call option on the firm's assets, struck at the face value of its debt.**

At maturity, equity holders pay off the debt if the firm is worth more than the debt and pocket the residual; otherwise they exercise limited liability, hand the firm to the bondholders, and walk away. Therefore the entire apparatus of Black–Scholes–Merton — the PDE, the risk-neutral measure, $N(d_1)$, $N(d_2)$ — applies *directly*, with firm value playing the role of the "stock" and debt the role of the "strike". Risk-neutral default probability is then simply $N(-d_2)$: the BSM exercise probability.

This folder is the model topic-folder for the Kwant-Atlas build. It is a *hub*: it (a) gives the **fast formula lookup** below (job #1), covering the structural (Merton), reduced-form (intensity), CDS pricing, and portfolio (Vasicek) layers, and (b) routes you to six sub-pages that walk from raw intuition through the structural model, distance-to-default and PD, reduced-form and CDS, the failure modes, and the portfolio extensions.

> **The one-sentence essence.** "Default is an option: equity is a call on firm assets, so a credit spread is the price of a put that the firm's owners hold against its creditors — and the probability of exercise is a Black–Scholes exercise probability."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from the verified corpus — Merton (1974) eqs. (10)–(18), Hull (11th ed.) §§24.2–24.9 eqs. (24.2)–(24.10), CreditMetrics (1997) Tables 1.8/6.2, and Vašíček (1987/1991) — and every number in the check column was **re-executed and reproduced exactly** (§3).

**Notation.** $V$ firm (asset) value, $E$ equity value, $D$ face value of debt (one zero-coupon bond, maturity $T$), $r$ risk-free rate, $\sigma_V$ asset volatility, $\sigma_E$ equity volatility, $R$ recovery rate, $N(\cdot)$ standard-normal CDF, $N^{-1}(\cdot)$ its quantile, $n(\cdot)$ standard-normal density.

**2.1 Structural (Merton) layer.** Everything follows from $E=\max(V-D,0)$, $F=V-E=\min(V,D)$:

| Quantity | Formula | Verified check (§3) |
|---|---|---|
| Equity (call) | $E=V\,N(d_1)-D\,e^{-rT}N(d_2)$ | $E_0{=}100,\sigma_E{=}0.40,D{=}350,T{=}1,r{=}5\%\Rightarrow V_0=432.9067$ |
| $d_1,d_2$ | $d_1=\dfrac{\ln(V/D)+(r+\tfrac12\sigma_V^2)T}{\sigma_V\sqrt T},\quad d_2=d_1-\sigma_V\sqrt T$ | $d_2=2.7900$ |
| Equity-vol identity | $\sigma_E E=N(d_1)\,\sigma_V V$ | $\Rightarrow\sigma_V=0.0926$ |
| Debt (risk-free − put) | $F=V\,N(-d_1)+D\,e^{-rT}N(d_2)$ | $F=332.9067$ |
| **Risk-neutral PD** | $\mathbb{Q}(\text{default})=N(-d_2)$ | $26.4$ bp |
| Risky yield (Merton eq. 14) | $R(t)-r=-\tfrac1t\ln\!\Big[\Phi(h_2)+\tfrac1d\Phi(h_1)\Big],\ d=D e^{-rt}/V$ | spread $0.71$ bp |
| Distance to default | $\mathrm{DD}=\dfrac{\ln(V/D)+(\mu-\tfrac12\sigma_V^2)T}{\sigma_V\sqrt T}$ | $2.7900$ (RN, $\mu{=}r$) |
| **PD (real-world)** | $\mathrm{PD}=N(-\mathrm{DD})$ | $\mu{=}10\%\Rightarrow 4.3$ bp |
| KMV default point | $D^{*}=\text{ST debt}+\tfrac12\,\text{LT debt}$ (empirical, Crosbie–Bohn) | — |

**2.2 Reduced-form (intensity) layer** (Jarrow–Turnbull 1995; Hull §24.4):

| Quantity | Formula | Verified check |
|---|---|---|
| Hazard from spread | $\lambda(T)=\dfrac{s(T)}{1-R}$ (Hull 24.2) | $s{=}150$ bp, $R{=}40\%\Rightarrow\lambda=250$ bp/yr |
| Survival / default | $Q(t)=e^{-\lambda t},\quad \mathrm{PD}(t)=1-e^{-\lambda t}$ | $Q(5)=0.8825$, $\mathrm{PD}=11.75\%$ |
| **CDS fair spread** | $s^{*}=\dfrac{C}{A+B}$ (PV protection ÷ PV premium+accrual) | recovers $150.00$ bp from $\lambda=2.5\%$ |
| Continuous approx | $s\approx\lambda\,(1-R)$ | $=150$ bp |

**2.3 Portfolio credit layer** (Vašíček one-factor / Gaussian copula, Hull 24.10; Bluhm §1.2.3):

| Quantity | Formula | Verified check |
|---|---|---|
| Conditional PD | $p(x)=N\!\Big(\dfrac{N^{-1}(p)-\sqrt\rho\,x}{\sqrt{1-\rho}}\Big)$ | — |
| **Asymptotic loss CDF** | $F(\theta)=N\!\Big(\dfrac{\sqrt{1-\rho}\,N^{-1}(\theta)-N^{-1}(p)}{\sqrt\rho}\Big)$ | $p{=}2\%,\rho{=}15\%$: $F(0.1763)=0.999$ |
| Loss quantile (Basel "formula") | $\theta_q=N\!\Big(\dfrac{N^{-1}(p)+\sqrt\rho\,N^{-1}(q)}{\sqrt{1-\rho}}\Big)$ | $\theta_{0.999}=0.17633$ (17.63% of EAD) |
| Portfolio UL (2 loans) | $\mathrm{UL}^2=\sum_i p_i(1-p_i)+2\rho\sqrt{p_1(1-p_1)p_2(1-p_2)}$ | Bluhm (1.13) |

> **Critical scaling caveat.** In the structural model the *observable* is equity, not firm value; $(\sigma_V,V_0)$ must be **solved** from the two-equation system, and that inversion is the single largest source of error (§5). In the reduced-form model the spread is *given* and PD is *implied* — the two layers calibrate to the same data but answer different questions (real-world vs risk-neutral).

---

### 3. Computational Implementation — the hub engine

This runs on the **standard library only** (`math.erf` gives the exact normal CDF, so there is no numpy/scipy dependency). It solves the Merton two-equation system by fixed-point iteration, then reports distance-to-default, PD, and the model credit spread.

```python
import math

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def solve_merton(E0, sigE, D, T, r, tol=1e-14, itmax=5000):
    """Invert equity observables (E0, sigE) into firm variables (V0, sigV).
       Equations: E = V N(d1) - D e^{-rT} N(d2)   and   sigE E = N(d1) sigV V."""
    V, sigV = E0 + D * math.exp(-r * T), sigE * (E0 / (E0 + D * math.exp(-r * T)))
    for _ in range(itmax):
        d1 = (math.log(V / D) + (r + 0.5 * sigV**2) * T) / (sigV * math.sqrt(T))
        d2 = d1 - sigV * math.sqrt(T)
        Vn = (E0 + D * math.exp(-r * T) * N(d2)) / N(d1)   # from the call equation
        sv = sigE * E0 / (V * N(d1))                        # from the vol identity
        if abs(Vn - V) < tol and abs(sv - sigV) < tol:
            V, sigV = Vn, sv; break
        V, sigV = Vn, sv
    d1 = (math.log(V / D) + (r + 0.5 * sigV**2) * T) / (sigV * math.sqrt(T))
    return V, sigV, d1, d1 - sigV * math.sqrt(T)

E0, sigE, D, T, r = 100.0, 0.40, 350.0, 1.0, 0.05
V0, sigV, d1, d2 = solve_merton(E0, sigE, D, T, r)
print(f"V0 = {V0:.4f}   sigmaV = {sigV:.4f}   d1 = {d1:.6f}   d2 = {d2:.6f}")
print(f"round trip: E = {V0*N(d1) - D*math.exp(-r*T)*N(d2):.6f} (target 100)   "
      f"sigmaE = {sigV*V0*N(d1)/E0:.6f} (target 0.40)")
print(f"DD = {d2:.4f}   PD = N(-d2) = {N(-d2)*1e4:.2f} bp")
```
```
V0 = 432.9067   sigmaV = 0.0926   d1 = 2.882599   d2 = 2.790018
round trip: E = 100.000000 (target 100)   sigmaE = 0.400000 (target 0.40)
DD = 2.7900   PD = N(-d2) = 26.35 bp
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Firm value is unobservable** — the model must invert equity into $(V_0,\sigma_V)$, an ill-conditioned problem whose error is amplified into the PD (a 1% error in $\sigma_E$ moves PD by $\approx 9\%$ here).
2. **Default only at maturity / continuous asset paths** — real firms *jump* to default between coupons; the diffusion cannot produce a surprise (the "credit-spread puzzle": the model gives $\sim0.7$ bp where markets quote $100{+}$ bp).
3. **Independence is false** — defaults cluster; asset correlation $\rho$ drives the entire tail of a portfolio loss distribution, and getting $\rho$ wrong mis-prices every CDO tranche.

---

### 5. Canonical Literature & Study References

- **Merton, Robert C.** — *On the Pricing of Corporate Debt: The Risk Structure of Interest Rates*, *Journal of Finance* 29(2):449–470 (1974). The primary source: eqs. (10)–(11) (equity = call), (12)–(13) (equity/debt values), (14) (risk premium). *Deep-read and formula-verified in the corpus.*
- **Hull, John C.** — *Options, Futures, and Other Derivatives* (11th ed.) — Ch 24 (ratings, transition matrices Table 24.4, hazard-from-spread 24.2, Merton 24.3–24.4, Credit VaR 24.9–24.10) and Ch 25 (CDS mechanics and valuation, one-factor Gaussian copula). *Verification report in the corpus.*
- **Bluhm, Overbeck & Wagner** — *Introduction to Credit Risk Modeling*, 2nd ed. (2010) — asset-value models (§1.2.3), factor decomposition $r_i=\beta_i\Phi_i+\varepsilon_i$, portfolio UL (1.13). *Read in the corpus.*
- **Gupton, Finger & Bhatia (J.P. Morgan)** — *CreditMetrics™ — Technical Document* (1997) — the one-year transition matrix (Table 1.8) and the rating-migration portfolio framework.
- **Vašíček, Oldřich** — *Probability of Loss on Loan Portfolio* (KMV, 1987) and *Limiting Loan Loss Probability Distribution* (1991) — the one-factor closed form behind Basel IRB.
- **Gregory, Jon** — *The xVA Challenge* (5th ed., 2025) — CVA $=\mathrm{LGD}\times\mathbb{E}[\mathrm{EE}\times\mathrm{PD}]$, jump-to-default, wrong-way risk, CDS-basis; the bridge from single-name default to counterparty pricing. *Corpus digest available.*

---

### 6. Connected Graph Bridges

- Foundational base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Sibling topic: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (the portfolio-loss machinery this folder feeds) · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] (the tail of the loss distribution)
- Sub-pages (in-folder): 01 From Zero · 02 Structural Model · 03 Distance-to-Default & PD · 04 Reduced-Form & CDS · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/01-from-zero-intuition|01 · From Zero]] — no prior credit knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/02-the-merton-structural-model|02 · Structural Model]] → [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/03-distance-to-default-and-pd|03 · Distance-to-Default & PD]] → [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/04-reduced-form-and-cds|04 · Reduced-Form & CDS]].
- **Robustness (practitioner/graduate):** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]]
