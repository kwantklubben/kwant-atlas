---
title: "6.5.4 Spread Decomposition"
tags:
  - pillar-market-making
  - spread-decomposition-and-roll-model
  - spread-decomposition
  - adverse-selection
  - order-processing
  - glosten-harris
  - huang-stoll
  - stoll
---

**Basic Prerequisites:** [[pillars/06-market-making/spread-decomposition-and-roll-model/03-the-roll-model|03 · The Roll Model]] and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (regression, autocovariance).

---

### 1. Intuition & Practical Objective

The Roll model measures the *total* spread but treats it as one number. Yet a market maker's revenue is not all profit — the spread pays for three distinct things:

1. **Order-processing costs** — the fixed, per-trade cost of doing business (clearing, settlement, bookkeeping, the labor of quoting). Modeled in the classic "cost-of-transacting" view (Demsetz 1968; Stoll's *naive* order-processing model; Roll's assumption).
2. **Inventory-holding costs** — the risk the maker bears by holding a nonzero inventory between trades (Stoll 1978; Ho & Stoll 1981). A dealer with a long inventory faces downside price risk, so it shades quotes down to unwind.
3. **Adverse-selection / information costs** — the expected loss to traders who know the value is about to move (Copeland & Galai 1983; Glosten & Milgrom 1985). The informed trade at the maker's quote, then the price moves against the maker.

The practical objective: **estimate the share of the spread that is each component.** This is the single most useful number for a market maker — it tells you how much of your spread revenue is real profit (order-processing + inventory) versus a transfer to informed flow (adverse selection), and hence how aggressively to quote, how wide, and whether your market is worth making.

In the generalized-Roll notation, the **total half-spread is $c+\lambda$**: $c$ = order-processing/inventory cost (the transitory part), $\lambda$ = adverse-selection cost (the permanent, price-impact part). The full decomposition literature is a refinement of splitting $c$ and $\lambda$, and of further splitting $c$ into order-processing vs inventory.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Glosten–Harris (1988): transitory vs permanent

Glosten & Harris specify the efficient price and trade price with trade-size-dependent components ($V_t$ = trade volume; $\lambda_0+\lambda_1 V_t$ adverse selection, $c_0+c_1 V_t$ order processing):

$$
m_t = m_{t-1} + u_t + q_t\,(\lambda_0+\lambda_1 V_t),
$$
$$
p_t = m_t + q_t\,(c_0+c_1 V_t).
$$

Taking differences, the observed price change decomposes into a **permanent** (information) piece $\lambda q_t$ and a **transitory** (order-processing) piece $c(q_t-q_{t-1})$:

$$
\Delta p_t = u_t + q_t(\lambda_0+\lambda_1 V_t) + \underbrace{c_0(q_t-q_{t-1})+c_1(q_t V_t-q_{t-1}V_{t-1})}_{\text{transitory}}.
$$

#### 2.2 The generalized Roll (Hasbrouck Ch 8) — the simplest estimable form

With constant $c,\lambda$ and efficient innovation $w_t=\lambda q_t+u_t$:

$$
p_t=m_t+c\,q_t,\qquad m_t=m_{t-1}+\lambda q_t+u_t,
$$
$$
\Delta p_t = c\,(q_t-q_{t-1}) + \lambda q_t + u_t,
$$
$$
\gamma_0 = c^2+(c+\lambda)^2+\sigma_u^2,\qquad \gamma_1 = -c\,(c+\lambda).
$$

**Total spread is $2(c+\lambda)$.** The autocovariance now captures the *product* of the two costs. Regression on trade direction separates them: $c$ is the coefficient on $q_t-q_{t-1}$ (the order-processing/transitory part), $\lambda$ on $q_t$ (the adverse-selection/permanent part). Note $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ is identified, but $\{c,\lambda,\sigma_u^2\}$ individually are **not** from autocovariances alone (2 moments, 3 unknowns) — hence the need for trade-direction data. This is the identification lesson that motivates the whole decomposition literature.

#### 2.3 Stoll (1989): reversal probability and size

Stoll models the spread through two observable parameters: the **probability of a price reversal** $\pi$ and the **size of a reversal** as a fraction of the quoted spread, $1-\delta$ (reversal size $=(1-\delta)S$). Each pure view of the spread pins them differently:

| Determinant of quoted spread | $\pi$ | $\delta$ |
|---|---|---|
| Pure order processing (Roll) | $\tfrac12$ | $0$ (reversal $=S$) |
| Pure adverse information (Copeland–Galai, Glosten–Milgrom) | $\tfrac12$ | $\tfrac12$ (reversal $=\tfrac12 S$) |
| Pure inventory holding (Ho–Stoll) | $>\tfrac12$ | $\tfrac12$ |

* The order-processing spread simply bounces the full distance $S$ (reversal $=S$, i.e. $\delta=0$) with reversal probability $\tfrac12$.
* The adverse-information view: after a trade conveys news, quotes shift by $\lambda$, so a reversal is only half the quoted spread ($\delta=\tfrac12$).
* The inventory view: the dealer shifts quotes to *induce* offsetting trades, so reversal probability exceeds $\tfrac12$ ($\pi>\tfrac12$).

Stoll relates the squared quoted spread to two serial covariances (transaction returns and quote returns) and estimates the components on NASDAQ/NMS data. **Key theoretical result: under both the inventory and adverse-information models, the realized spread is *less* than the quoted spread** — the dealer earns the quoted spread only in the pure order-processing world.

#### 2.4 Huang–Stoll (1997): the unified three-way decomposition

Huang & Stoll put order-processing, inventory, and adverse-selection in **one** framework (the general approach). Their structural model yields the trade-by-trade price change

$$
\Delta p_t = \frac{S}{2}(q_t-q_{t-1}) + \lambda\,\frac{S}{2}\,q_{t-1} + u_t,
$$

where $\tfrac{S}{2}(q_t-q_{t-1})$ is the transitory (order-processing) part and $\lambda \tfrac{S}{2}q_{t-1}$ is the adverse-selection + inventory part driven by the *previous* trade's direction (the dealer reacts to the last trade). By restricting $\lambda$ and adding inventory terms, Huang–Stoll show how to identify the three components separately. The **two-way** (order-processing vs information) split is their baseline; the inventory piece is the refinement.

---

### 3. Computational Implementation — estimate $c$ and $\lambda$ from a trade tape

Simulate a Glosten–Harris/Huang–Stoll tape (trade prints at $m_t+q_tc$, then the efficient price absorbs the impact $\lambda q_t$), then run the regression $\Delta p_t = c\,(q_t-q_{t-1})+\lambda q_{t-1}+u_t$ via the normal equations to recover both components and the total spread. *(The boxed generalized-Roll equation above places the impact on the contemporaneous $q_t$; the equivalent Huang–Stoll regression places it on the lagged $q_{t-1}$ with a matching regressor, so both recover the same $c,\lambda$.)* Stdlib only.

```python
import random

random.seed(99)
def simulate_gh(n=20000, c=0.02, lam=0.015, sig_u=0.005):
    m = 100.0; qs = []; ps = []
    for _ in range(n):
        m += random.gauss(0, sig_u)
        q = random.choice([-1, 1])
        ps.append(m + q*c); qs.append(q)
        m += lam*q                 # adverse-selection impact AFTER the trade
    return qs, ps

qs, ps = simulate_gh()
dp = [ps[i]-ps[i-1] for i in range(1, len(ps))]
X1 = [qs[i]-qs[i-1] for i in range(1, len(qs))]     # regressor: transitory/order-processing
X2 = [qs[i-1]       for i in range(1, len(qs))]     # regressor: adverse-selection (prev trade)

def dot(a, b): return sum(x*y for x, y in zip(a, b))
A11, A12, A22 = dot(X1,X1), dot(X1,X2), dot(X2,X2)
b1, b2 = dot(X1,dp), dot(X2,dp)
det = A11*A22 - A12*A12
c_est   = (b1*A22 - b2*A12)/det
lam_est = (b2*A11 - b1*A12)/det
print(f"order-processing c        = {c_est:.4f}   (true 0.0200)")
print(f"adverse-selection lambda  = {lam_est:.4f}   (true 0.0150)")
print(f"total half-spread c+lambda= {c_est+lam_est:.4f}   (true 0.0350)")
print(f"total quoted spread 2(c+l) = {2*(c_est+lam_est):.4f}   (true 0.0700)")
print(f"adverse-selection share   = {lam_est/(c_est+lam_est):.1%}")
```
```
order-processing c        = 0.0200   (true 0.0200)
adverse-selection lambda  = 0.0150   (true 0.0150)
total half-spread c+lambda= 0.0350   (true 0.0350)
total quoted spread 2(c+l) = 0.0700   (true 0.0700)
adverse-selection share   = 42.8%
```

The regression cleanly separates the transitory (order-processing) half-spread $c= $ \$0.02 from the permanent (adverse-selection) half-spread \lambda= \$0.015. Almost 43% of the maker's half-spread is expected to be given back to informed flow — exactly the kind of number a quoting desk needs.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Under-identification.** Two autocovariances cannot pin down three parameters $\{c,\lambda,\sigma_u^2\}$. Use trade-direction (signed) data and the regression form, or the estimate is arbitrary. This is the single most important identification warning.
2. **Order-processing vs inventory confusion.** The regression above folds inventory into $c$ (the transitory part). Splitting inventory from order-processing needs quote data and/or inventory-constrained models (Stoll 1989, Huang–Stoll 1997's restricted models). Treat "order-processing" estimates as "transitory" unless the model explicitly separates them.
3. **Wrong sign on $q_t$.** The Lee–Ready (1991) algorithm signs trades (trade vs prevailing quote) because the aggressor side is what matters. Mis-signing destroys the $\lambda$ estimate (see [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]).
4. **Price impact ≠ mechanical.** $\lambda$ is a signal-extraction / competitive-market quantity, not a causal "impact" of your order alone (Hasbrouck Ch 5, 9). Reading $\lambda q_t$ as a guaranteed move misinterprets the estimate.

---

### 5. Canonical Literature & Study References

- **Glosten & Harris (1988)**, *Estimating the components of the bid/ask spread*, Journal of Financial Economics 21(1), 123–142 — the transitory-vs-permanent (order-processing vs information) decomposition.
- **Stoll (1989)**, *Inferring the components of the bid-ask spread: theory and empirical tests*, Journal of Finance 44(1), 115–134 — reversal probability $\pi$ and reversal size $\delta$; order-processing vs inventory vs adverse-information on NASDAQ/NMS.
- **Huang & Stoll (1997)**, *The components of the bid-ask spread: a general approach*, Review of Financial Studies 10(4), 995–1034 — the unified three-component framework.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 8 (generalized Roll, $\sigma_w^2=\gamma_0+2\gamma_1$ identification) and Ch 9 (Glosten–Harris, MRR, multivariate VAR) — *verified per-chapter in the corpus*.
- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1), 47–73 — the inventory-holding model.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/spread-decomposition-and-roll-model/03-the-roll-model|03 · The Roll Model]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/02-quoted-effective-realized|02 · Quoted / Effective / Realized]]
- Forward: [[pillars/06-market-making/spread-decomposition-and-roll-model/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/06-advanced-extensions|06 · Advanced Extensions]]
- Base: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] (why $\lambda>0$) · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] (the inventory half) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (regression)
