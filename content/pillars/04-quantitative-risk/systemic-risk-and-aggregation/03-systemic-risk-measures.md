---
title: "03 — Systemic Risk Measures: CoVaR, MES, SRISK, and Marginal Contribution"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - covar
  - mes
  - srisk
  - systemic-risk-measures
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] and [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/02-contagion-and-networks|02 · Contagion & Networks]].

---

### 1. Intuition & Practical Objective

Network contagion (§02) tells you *that* systems can collapse; systemic-risk measures try to tell you *which firm* is most dangerous, so a supervisor can charge capital or demand resolution. This page covers the three workhorse measures. The objective: keep their **conditioning direction** straight, do the mathematics correctly, and compute them on a tiny system where you can *see* what each one does.

The three questions a supervisor might ask, and which measure answers it:

| Question | Measure | It conditions on… |
|---|---|---|
| "How much does *firm i* lose when the *system* is in trouble?" | **MES** — marginal expected shortfall | the **system's** tail |
| "How much does the *system* lose when *firm i* is in trouble?" | **CoVaR** — conditional VaR | the **firm's** tail |
| "How much *capital* will firm i need in a crisis?" | **SRISK** — capital shortfall | an explicit **crisis scenario** |

MES and CoVaR are *opposite directions of the same conditioning*. Getting them backwards is the single most common conceptual error.

---

### 2. Mathematical Ground Truth & Derivations

Let firm $i$ return be $r_i$, the system (market) return be $R$, and let $\alpha$ be a small tail probability (e.g. $5\%$).

**MES (Acharya–Pedersen–Philippon–Richardson).** In expected-shortfall form, the system's ES is a value-weighted sum of member MESes:

$$\text{ES}_\alpha(R) = \sum_i w_i\,\mathbb{E}[\,r_i \mid R \le \text{VaR}_\alpha(R)\,] \equiv \sum_i w_i\,\text{MES}_{i,\alpha}.$$

Intuitively each firm contributes to system tail risk in proportion to *its own expected return inside the system's tail*. A firm that is *spread-hurting-but-small* can have large MES even if its weight $w_i$ is modest.

**CoVaR (Adrian–Brunnermeier).** CoVaR is the VaR of the system *conditional on firm $i$ being at its own VaR*:

$$\Pr\!\Big(X^{\text{system}} \le \text{CoVaR}_i^{\alpha} \;\Big|\; X^i = \text{VaR}_i^{\alpha} \Big) = \alpha,$$

and the **ΔCoVaR** is the *contribution* — how much worse the system's tail is when firm $i$ is distressed than in its median state:

$$\Delta\text{CoVaR}_i = \text{CoVaR}_i^{\alpha} - \text{CoVaR}_i^{50\%},$$

(the textbook baseline is the firm's median state $\text{VaR}_i^{50\%}$; the common practical simplification — used by this page's code and the hub — takes the *unconditional system VaR* as the baseline, which is the figure quoted below). Note it is a *difference of conditional quantiles*, not a sensitivity/derivative — ΔCoVaR is *not* a calculus gradient, a point often muddled in practice.

**SRISK (Brownlees–Engle).** A crisis scenario (cumulative market loss over some horizon ≥ threshold). Each firm's capital shortfall is

$$\text{SRISK}_i = \mathbb{E}\big[\,k\,A_i - E_i \mid \text{crisis}\,\big]_+,$$

where $A_i$ = assets, $E_i$ = equity, $k$ = required capital ratio (≈8% post-crisis). SRISK is the amount of fresh capital firm $i$ would need to keep ratio $k$ in the crisis — an *economic-resources* measure rather than a tail-quantile one, and the one regulators most directly convert into "systemically important" designations.

**The three agree on direction, not on magnitude** — a bank can be top-MES and bottom-SRISK (e.g. a high-marginal-risk but deeply-capitalised firm). Use all three, never one alone.

---

### 3. Computational Implementation — CoVaR & MES on a 2-bank system

We build a two-bank system from a common factor $F\sim N(0,1)$ plus idiosyncratic noise, so banks are correlated at $\rho = \sigma_F^2/(\sigma_F^2+\sigma_{\text{id}}^2) = 0.5$. Then we estimate, by direct simulation, the tail quantities. Stdlib only (Box–Muller).

```python
import math, random

def gauss():
    u1 = max(random.random(), 1e-12)
    return math.sqrt(-2.0*math.log(u1)) * math.cos(2.0*math.pi*random.random())

def q(xs, alpha):
    s = sorted(xs); k = math.ceil(alpha*len(s)) - 1
    return s[max(0, k)]

random.seed(11)
N = 60000
rf, idio = 1.0, 1.0                     # equal factor/idio variance -> corr 0.5
rho = rf*rf/(rf*rf + idio*idio)
r1, r2 = [], []
for _ in range(N):
    F  = gauss()*math.sqrt(rf)
    r1.append(F + gauss()*math.sqrt(idio))
    r2.append(F + gauss()*math.sqrt(idio))
S = [(a+b)/2 for a, b in zip(r1, r2)]    # equal-weight system return

var_sys = q(S, 0.05)
ntail = sum(1 for s in S if s <= var_sys)
mes1  = sum(a for a, s in zip(r1, S) if s <= var_sys) / ntail
var1   = q(r1, 0.05)                      # hoist: don't sort inside the loop
covar1 = q([s for a, s in zip(r1, S) if a <= var1], 0.05)
deltacovar = covar1 - var_sys

print(f"bank correlation rho                = {rho:.3f}")
print(f"unconditional VaR[0.05](system)     = {var_sys:+.4f}")
print(f"MES of bank 1 given system tail     = {mes1:+.4f}")
print(f"CoVaR of system | bank1 distressed  = {covar1:+.4f}")
print(f"delta-CoVaR (bank1's contrib)       = {deltacovar:+.4f}")
```
```
bank correlation rho                = 0.500
unconditional VaR[0.05](system)     = -2.0138
MES of bank 1 given system tail     = -2.5240
CoVaR of system | bank1 distressed  = -3.4179
delta-CoVaR (bank1's contrib)       = -1.4042
```

**Read the output.** In the *system's* worst 5% ($\le -2.0138$) bank 1 loses on average **-2.52** — that's its **MES**; it is exposed *to* the system tail. When bank 1 *itself* is in its worst 5%, the *system's* 5% quantile drops from -2.01 to **-3.42** — that's **CoVaR**, the damage bank 1 does *to* the system; **ΔCoVaR = -1.40** is bank 1's marginal contribution. Same data, two opposite questions: MES says "how much this bank suffers in a crash," CoVaR says "how much the crash suffers because this bank exists." Both are larger in magnitude than the unconditional VaR — the connected bank both catches and *spreads* tail risk.

*(SRISK is scenario-based rather than quantile-based; it is not computed here because it needs a crisis-horizon capital projection — see §2 for the formula and §5 for its literature.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Direction confusion.** Swapping the conditioning (CoVaR vs MES) answers the wrong policy question and can rank banks oppositely. Always state *what is conditioned on*.
2. **CoVaR ≠ VaR of the stressed firm.** CoVaR is a *system* quantile conditioned on the *firm*; it is not a firm-level number rescaled. (Here it is -3.42, more negative than firm VaR.)
3. **Tail estimation is the weak link.** All three need reliable *extreme-tail* inputs (high $\alpha$, crisis scenarios), which historical data under-samples — the "unmeasurable tail dependence" failure of §05 is baked in here.
4. **Procyclical inputs.** If the measure uses current VaR/vol, it *rises exactly when the supervisor must force deleveraging* (see [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05 · Failure Modes]]). Countercyclical buffers are the patch (see [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 5. Canonical Literature & Study References

- **Adrian & Brunnermeier**, *CoVaR*, *American Economic Review* 106(7):1705–1741 (2016) — the CoVaR and ΔCoVaR measures.
- **Acharya, Pedersen, Philippon & Richardson**, *Measuring Systemic Risk*, *Review of Financial Studies* 30(1):2–47 (2017) — MES and the capital-shortfall view.
- **Brownlees & Engle**, *SRISK: A Conditional Capital Shortfall Measure of Systemic Risk*, *RFS* 30(1):49–79 (2017) — the SRISK scenario measure; the direct ancestor of the Fed's systemic-importance screens.
- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015), §8.4 — multivariate tail estimation that CoVaR/MES rest on. *In the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/02-contagion-and-networks|02 · Contagion & Networks]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/04-aggregating-risk-types|04 · Aggregating Risk Types]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05 · Failure Modes]]
- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|Coherent Risk Measures]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|Expected Shortfall]]