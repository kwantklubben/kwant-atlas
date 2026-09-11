---
title: "03 — Temporary vs Permanent Impact: The Two Components"
tags:
  - pillar-market-making
  - market-impact
  - temporary-impact
  - permanent-impact
  - almgren-chriss
  - resilience
---

**Basic Prerequisites:** [[pillars/06-market-making/market-impact-and-depth/02-the-kyle-model|02 · The Kyle Model]] and [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]].

---

### 1. Intuition & Practical Objective

Every impact you observe is the sum of two things that behave nothing alike:

- **Permanent impact** — the part of the price move that *stays*. The market has genuinely re-priced the asset (because your flow was informative, or because a large imbalance permanently cleared). Sell a stock and watch the price settle 20bp lower *for good*: that is permanent impact. It is **schedule-independent**: it depends on *how much* you trade, not on *how you slice it*.
- **Temporary impact** — the part that *decays*. You are consuming liquidity faster than it replenishes, so the price you pay is temporarily worse; once you stop, the book refills ("resilience") and the price snaps back. It is **schedule-sensitive**: trade more slowly and it shrinks.

**Why this is the most important distinction in execution.** If you mistake *temporary* impact for *permanent*, you will conclude that trading slowly is pointless (it isn't — it removes the temporary part). If you mistake *permanent* for *temporary*, you will schedule an order assuming the price will revert when it never will — and you will systematically lose money on every large trade. The realized cost of your execution (the VWAP impact) is a mixture: it is worse than the permanent impact but better than the instantaneous peak, and *where* it lands between them is precisely what your execution algorithm controls.

> **The one-sentence essence.** "Permanent impact is the price you truly pay for the liquidity of the asset and is fixed by size; temporary impact is the price you pay for trading *fast* and is a dial your execution schedule turns."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Almgren–Chriss decomposition

Sell $X$ shares in $N$ discrete slices, $n_k$ shares at time $t_k$, so $\sum_k n_k=X$. The price has a **permanent** drift and a **temporary** concession:

$$
S_k=S_0+\gamma\sum_{j\le k}n_j\ \ (\text{permanent}),\qquad
\tilde S_k=S_k+\epsilon\,\mathrm{sgn}(n_k)+\tilde\eta\,\frac{n_k}{\tau}\ \ (\text{temporary execution price}).
$$

Here $g(v)=\gamma v$ is the permanent impact function and $h(v)=\epsilon\,\mathrm{sgn}(v)+\tilde\eta\,v$ the temporary one; $\epsilon$ is the fixed (spread-plus-fee) cost and $\tilde\eta$ the variable concession per unit trade rate. The realized cost of the program is $\sum_k n_k\,\tilde S_k - X S_0$, whose expectation is

$$
\boxed{\ \mathbb E[x]=\tfrac12\gamma X^2+\epsilon\sum_k|n_k|+\tilde\eta\sum_k n_k^2\ },\qquad \tilde\eta=\eta-\tfrac12\gamma,
$$

and whose variance is $\mathrm{Var}[x]=\tfrac12\sigma^2\sum_k\tau_k x_k^2$ (the uncertain future price of the shares you still hold). Two immediate consequences:

- The **permanent term $\tfrac12\gamma X^2$ is independent of the schedule** — every child order size drops out of it (the sum telescopes). *You cannot schedule permanent impact away.*
- The **temporary term $\tilde\eta\sum_k n_k^2$ is minimised by spreading the order out** (making the $n_k$ small). Trading very slowly drives it toward zero — the "min-impact" / TWAP limit.

Trading off expected cost against timing risk yields the **efficient frontier**, and for linear impact the optimal trajectory is the closed form

$$
x_j=\frac{\sinh\!\big(\kappa(T-t_j)\big)}{\sinh(\kappa T)}X,\qquad \kappa\approx\sqrt{\frac{\tilde\lambda\sigma^2}{\tilde\eta}}\quad(\text{Gatheral's }\kappa),
$$

which interpolates between constant-rate (risk-neutral, $\kappa\to0$) and front-loaded (risk-averse, $\kappa\to\infty$) execution. *(The scheduling problem itself is Pillar 2; here the point is the arithmetic of the two components.)*

#### 2.2 The temporary component is exactly what the price does `back`

Define the **transient** pressure $T_n$ as an AR(1)-like decay: $T_n=\rho\,T_{n-1}+\eta\,n_n$, with recovery factor $\rho\in[0,1)$ (resilience). Then the observed mid is $m_n+T_n$ where $m_n$ carries the permanent drift. After execution stops ($n_n=0$), $T_n\to\rho^n T\to0$ and the price settles at $m_\infty=S_0+\gamma X$ — **the permanent level**. The gap between the peak and the permanent level is the temporary impact that "comes back".

#### 2.3 The statistical version — generalized Roll

Hasbrouck's generalized Roll model makes the same split *in transaction data*:

$$
\Delta p_t=c\,(q_t-q_{t-1})+\lambda\,q_t+u_t,
$$

with $q_t\in\{+1,-1\}$ the trade sign, $c$ the **transitory** (order-processing / inventory / bid-ask bounce) component and $\lambda$ the **permanent** (adverse-selection) component. The spread is $2(c+\lambda)$, and the identified random-walk variance is $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$. The transitory component is exactly the $q_t-q_{t-1}$ "bounce"; the permanent component is the $\lambda q_t$ that shifts the efficient price. *(Glosten–Harris 1988 estimate the same decomposition with size-dependent $\lambda$; Huang–Stoll 1997 is the three-way ordering/inventory/adverse-selection version.)*

#### 2.4 Resilience and the finite-book correction

If the book refills immediately, all impact is temporary and total cost is zero for infinitesimal trade rates — absurd, so permanent impact must exist. If the book never refills, all impact is permanent — equally wrong. The truth is a **decay**: Obizhaeva & Wang (2013) show that with a resilient book the optimal strategy is a **block at the start, a block at the end, and a linear ramp between** — precisely because the temporary impact you create will *partly come back*, and you can re-use that resilience.

---

### 3. Computational Implementation — the same order, four speeds

One sell of $X=-10^6$ shares, executed at four speeds (10, 25, 100, 500 child orders). Permanent coefficient $\gamma=+2\times10^{-6}$/share (so a *sell* has negative signed flow and pushes the price down), transient coefficient $\eta=+8\times10^{-6}$/share, per-slice decay $\rho=0.90$. Stdlib only.

```python
def propagator(X, n_slices, gamma_perm, eta_temp, rho, S0=50.0):
    """Discrete temporary-vs-permanent impact.
       X (signed) sold over n_slices child orders; transient pressure decays by rho
       each slice.  Returns (permanent impact, peak impact, execution VWAP impact)."""
    q = X / n_slices
    m = S0            # permanent / efficient price
    T = 0.0           # transient pressure (price units)
    extreme = S0; notional = 0.0
    for _ in range(n_slices):
        m += gamma_perm * q              # permanent drift accumulates with size
        T = rho * T + eta_temp * q       # new transient pressure + decayed old
        mid = m + T
        extreme = min(extreme, mid) if X < 0 else max(extreme, mid)
        notional += mid * q              # we trade at the observed (impacted) mid
    return gamma_perm * X, extreme - S0, notional / X - S0

print("Temporary vs permanent: same size X, different execution speed")
print(f"{'slices':>7} {'speed':>6} {'permanent':>11} {'peak impact':>12} {'exec VWAP imp':>14}")
for n in (10, 25, 100, 500):
    perm, peak, vwap = propagator(-1_000_000, n, 2e-6, 8e-6, 0.90)
    print(f"{n:>7} {n/10:>5.0f}x {perm:>11.4f} {peak:>12.4f} {vwap:>14.4f}")
```
```
Temporary vs permanent: same size X, different execution speed
 slices  speed   permanent  peak impact  exec VWAP imp
     10     1x     -2.0000      -7.2106        -4.4105
     25     2x     -2.0000      -4.9703        -3.1707
    100    10x     -2.0000      -2.8000        -1.7380
    500    50x     -2.0000      -2.1600        -1.1591
```

Read the table:
- **Permanent impact is constant at $-2.0000$** across a fifty-fold speed range — the per-share permanent impact $\gamma X=2\times10^{-6}\times(-10^6)=-$ \$2 (in total dollars, \tfrac12\gamma X^2=-\$1\text{M}), schedule-independent.
- **Peak (adverse) impact falls from $-7.21$ to $-2.16$** as execution slows: the temporary component $\to0$, and the peak converges on the permanent level.
- **Realized VWAP impact** is always *between* the two ($-4.41$ down to $-1.16$): it is what you actually pay, and it is the quantity your execution schedule controls.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Double-charging the permanent part.** A common bug: charging the *full* observed impact to every slice *and* also counting the permanent drift — effectively paying $\gamma X$ twice. The Almgren–Chriss bookkeeping charges $\tfrac12\gamma X^2$ once (the $\tfrac12$ comes from the fact that the shares you sell early escape the full permanent drop).
2. **Assuming the price reverts when it doesn't.** If the flow is informed, "temporary" impact can become permanent the moment the market infers the information — the Kyle half-information result (page 02). Distinguishing temporary from permanent in real data requires waiting and observing the post-trade decay (the Almgren et al. 2005 methodology: $S_{\text{post}}-S_0$ gives permanent, $\bar S-S_0$ gives realized).
3. **Ignoring resilience.** Treating the book as statically thin over-charges repeated trading; treating it as instantly-resilient under-charges the first block. Obizhaeva–Wang's block-ramp-block solution is the correct minimal model when resilience matters.
4. **Confusing the transitory bounce with information.** In the generalized Roll model, a *negative* first autocovariance ($\gamma_1=-c(c+\lambda)$) is the bid-ask bounce; a persistent positive response to signed flow is the permanent $\lambda$. Mislabelling the bounce as information (or vice-versa) corrupts every downstream estimate.
5. **The linear/quadratic trap.** The clean $\tfrac12\gamma X^2+\tilde\eta\sum n_k^2$ form relies on **linear** impact; real temporary impact is *concave* (page 04), so the quadratic penalty is a local approximation that mis-sizes large orders.

---

### 5. Canonical Literature & Study References

- **Almgren, R. & Chriss, N. (2000)**, *Optimal execution of portfolio transactions*, Journal of Risk 3(2), 5–39. *Permanent/temporary split, the linear cost function, the efficient frontier, the $\sinh$ trajectory. Primary PDF in corpus (`Almgren_2000_...`).*
- **Almgren, R., Thum, C., Hauptmann, H. & Li, H. (2005)**, *Direct estimation of equity market impact*, Risk 18(7), 57–62. *The empirical operationalisation: pre-trade, post-trade, realized prices; $\gamma,\eta$ fitted. Primary PDF in corpus.*
- **Obizhaeva, A. & Wang, J. (2013)**, *Optimal trading strategy and supply/demand dynamics*, J. Financial Markets 16(1), 1–32. *Resilience and the block-ramp-block solution.*
- **Hasbrouck, J. (2007)**, *Empirical Market Microstructure*, Ch 8. *Generalized Roll $\Delta p_t=c(q_t-q_{t-1})+\lambda q_t+u_t$, spread $2(c+\lambda)$, $\sigma_w^2=\gamma_0+2\gamma_1$; verified in corpus (`hasbrouck_ch6-10.md`, Ch 8).*
- **Glosten, L. R. & Harris, L. E. (1988)**, *Estimating the components of the bid/ask spread*, JFE 21(1), 123–142. *The size-dependent transitory/permanent decomposition. Primary PDF in corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-impact-and-depth/02-the-kyle-model|02 · The Kyle Model]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
- Forward: [[pillars/06-market-making/market-impact-and-depth/04-the-square-root-law|04 · The Square-Root Law]] · [[pillars/06-market-making/market-impact-and-depth/index|Index Hub]]
- Pillar 2: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Almgren–Chriss Optimal Execution]] (the scheduling problem built on this decomposition) · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (resilience measured in the book)
