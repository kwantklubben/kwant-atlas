---
title: "4.4.4 Reduced-Form (Intensity) Models & CDS Pricing"
tags:
  - pillar-quantitative-risk
  - credit-risk-and-the-merton-model
  - reduced-form
  - intensity-model
  - cds
  - credit-derivatives
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/03-distance-to-default-and-pd|03 · Distance-to-Default & PD]] and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/02-the-merton-structural-model|02 · Structural Model]].

---

### 1. Intuition & Practical Objective

The structural model asks *why* a firm defaults (asset value crosses a barrier). The **reduced-form** model does not ask why at all — it models default as an exogenous *event* that arrives with a time-varying **intensity** (hazard rate) $\lambda_t$:

$$
\mathbb{P}(\tau\in(t,t+dt]\mid \tau>t)=\lambda_t\,dt.
$$

The default time $\tau$ is the first jump of a counting process. This is the model that credit *markets* actually use, for three reasons:

1. **It calibrates directly to prices.** Credit spreads — and especially CDS quotes — are liquid and observable. Reduced-form models invert them into a hazard curve. No unobservable firm value is needed.
2. **Default can happen at any instant**, not only at maturity — fixing the structural model's biggest empirical defect (jump-to-default).
3. **It prices credit derivatives cleanly.** The survival probability $Q(t)=e^{-\lambda t}$ (flat intensity) gives the fair CDS spread in closed form, and the same machinery powers CVA (Gregory, Ch 17).

The practical objective: **bootstrap a hazard curve from market spreads and price a CDS to confirm the quoted spread is recovered.**

> **The duality.** Structural $=$ *cause* (asset process, firm fundamentals); reduced-form $=$ *symptom* (spread-implied hazard). They are linked by *Hull's identity* $\lambda(T)=s(T)/(1-R)$ — the spread *is* the market's hazard, adjusted for recovery.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Survival probability and the hazard rate

With deterministic intensity $\lambda(t)$, the survival probability to $t$ and the default density are
$$
Q(t)=\mathbb{P}(\tau>t)=\exp\!\Big(-\int_0^t\!\lambda(u)\,du\Big),\qquad
\mathbb{P}(t_0<\tau\le t_1)=Q(t_0)-Q(t_1).
$$
For **flat** intensity $\lambda$: $Q(t)=e^{-\lambda t}$ and the cumulative default probability is $1-e^{-\lambda t}$.

#### 2.2 Hazard from a credit spread (Hull eq. 24.2)

A risky bond yields $r+\lambda(1-R)$ in the simplest setup (risk-neutral, expected loss $=$ expected excess return), so
$$
\boxed{\;\lambda(T)=\frac{s(T)}{1-R}\;}
$$
where $s(T)$ is the credit spread to maturity $T$ and $R$ the recovery rate ($\mathrm{LGD}=1-R$). Hull §24.4 refines this by *bootstrapping* piecewise-constant hazard rates to match observed bond prices exactly (Examples 24.1–24.2); the flat-intensity formula is the first step of that recursion.

> **Interpretation.** $\lambda$ is the *risk-neutral* default intensity: the market's expected loss rate per unit time, grossed up by risk aversion. Historical (physical) default frequencies are lower — the same $\mathbb{Q}$-vs-$\mathbb{P}$ gap as in page 03.

#### 2.3 CDS mechanics and valuation (Hull §25.1–25.2)

A **credit default swap** is insurance: the protection buyer pays a periodic premium (spread $s$ times notional, quarterly in arrears) and receives, on a credit event, a payoff of $\mathrm{LGD}=1-R$. For a unit notional and quarterly payments at $t_k=k\,\Delta$:
- **Premium leg** (PV of premiums while alive + accrual on default):
$$
A+B=\sum_k \Delta\,D(t_k)\,Q(t_k)\;+\;\sum_k \tfrac{\Delta}{2}\,D(t_k)\,[Q(t_{k-1})-Q(t_k)],
$$
- **Protection leg** (PV of LGD paid at default):
$$
C=\sum_k (1-R)\,D(t_k)\,[Q(t_{k-1})-Q(t_k)].
$$
The **fair (par) spread** sets the two legs equal:
$$
\boxed{\;s^{*}=\frac{C}{A+B}\;}
$$
(Hull §25.2, "fair spread $s=C/(A+B)$", Example 25.1). The **mark-to-market** of an existing CDS is PV(protection) − PV(premiums) at the contractual spread. **CDS–bond basis** $=$ CDS spread − bond spread; negative when bonds are cheap relative to CDS (funding/liquidity effects; Gregory §14.3.4).

#### 2.4 The continuous approximation

With continuously-paid premium and no accrual, equating legs gives $s\approx\lambda(1-R)=\lambda\,\mathrm{LGD}$: fair spread $\approx$ hazard $\times$ loss-given-default. This is why $\lambda=s/(1-R)$ in §2.2 is *not* a coincidence — CDS and spread are two readings of the same intensity.

---

### 3. Computational Implementation — bootstrap hazard, price the CDS, recover the spread

Stdlib only. Start from a quoted $5$-year CDS spread, imply the hazard, build the survival curve, then price the swap from first principles and check that the fair spread equals the quote.

```python
import math

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

# --- reduced-form: implied hazard from a quoted 5y CDS spread (Hull 24.2) ---
s   = 0.0150          # quoted 5y CDS spread = 150 bp
R   = 0.40            # recovery rate; LGD = 60%
lam = s / (1.0 - R)   # lambda = s / (1 - R)
print(f"quoted spread = {s*1e4:.0f} bp, R = {R:.0%} -> hazard lambda = {lam*1e4:.1f} bp/yr")

def surv(t): return math.exp(-lam * t)
def pd_between(t0, t1): return surv(t0) - surv(t1)

T, r = 5.0, 0.02
print(f"survival 5y = {surv(T):.4f}   PD(<=5y) = {1 - surv(T):.4f}")

# --- CDS pricer: quarterly premium + accrual; protection = LGD on default ---
def cds_fair_spread(T, r, lam, R, m=4):
    dt = 1.0 / m
    A = B = C = 0.0
    for k in range(1, int(T * m) + 1):
        t = k * dt
        df = math.exp(-r * t)
        A  += dt * df * surv(t)                 # premiums while alive
        dfl = pd_between(t - dt, t)
        B  += 0.5 * dt * df * dfl               # accrual on default in the period
        C  += (1.0 - R) * df * dfl              # protection payment
    return C / (A + B)

fair = cds_fair_spread(T, r, lam, R)
print(f"fair CDS spread from flat hazard = {fair*1e4:.2f} bp  (target {s*1e4:.0f} bp)")
```
```
quoted spread = 150 bp, R = 40% -> hazard lambda = 250.0 bp/yr
survival 5y = 0.8825   PD(<=5y) = 0.1175
fair CDS spread from flat hazard = 150.00 bp  (target 150 bp)
```
The pricer recovers the input spread to the basis point, closing the loop between the spread-implied hazard and the CDS contract. The $11.75\%$ cumulative 5-year PD is the **risk-neutral** default probability the market is charging for — visibly higher than any agency's historical 5-year BB default rate, the $\mathbb{Q}$-vs-$\mathbb{P}$ gap again.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Deterministic intensity ignores spread volatility and jump risk.** Real spreads are stochastic and *jump* on credit events; a single $\lambda$ cannot produce a spread jump. Stochastic-intensity extensions (CIR-type $\lambda_t$) and jump-to-default models are the fixes (Gregory §17.6.4).
2. **The recovery rate is unobservable and assumed.** Everything scales with $(1-R)$; yet recovery is random, correlated with default, and junior/senior-dependent. Hull notes plain-vanilla CDS values are famously *insensitive* to $R$ when pricing is self-consistent — but getting $R$ wrong biases $\lambda$ and therefore every CVA on that name.
3. **Single-name intensity says nothing about correlation.** Pricing a portfolio (tranches, $k$th-to-default) needs a *dependence* structure, usually the Gaussian copula — whose correlation is not a physical quantity and which was at the centre of the 2008 CDO failure (the "correlation smile"). See [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/06-advanced-extensions|06 · Portfolio Credit & Vasicek]].
4. **Wrong-way risk.** Intensity and exposure are not independent in reality (a counterparty's default probability rises exactly when your exposure to it is largest). Treating them as independent understates CVA — the reason Gregory elevates wrong-way risk to a first-class failure mode.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives* — §24.4 (hazard from spread, eq. 24.2, bootstrapping), §25.1–25.2 (CDS mechanics, fair spread $s=C/(A+B)$, Examples 25.1/25.2), §25.3 (indices), §25.9 (correlation and tranching). *Verification report in the corpus.*
- **Jarrow & Turnbull (1995)** — *Pricing Derivatives on Financial Securities Subject to Credit Risk*, *Journal of Finance* 50(1):53–85 — the founding reduced-form intensity paper (spread-driven default). *Corpus bibliography.*
- **Gregory, Jon** — *The xVA Challenge* (5th ed., 2025) — Ch 3.3 (real-world vs risk-neutral PD, recovery/LGD), §14.3.4 (CDS–bond basis), §17.6 (wrong-way risk). *Corpus digest available.*
- **Bielecki & Rutkowski** — *Credit Risk: Modeling, Valuation and Hedging* (2002) — the rigorous intensity/doubly-stochastic theory and hedging of defaultable claims. *Corpus available.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/03-distance-to-default-and-pd|03 · Distance-to-Default & PD]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/02-the-merton-structural-model|02 · Structural Model]]
- Forward: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/06-advanced-extensions|06 · Portfolio Credit & Vasicek]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the tail of the loss the intensity generates)
