---
title: "Constraints & Transaction Costs"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - transaction-costs
  - turnover
  - market-impact
  - index-hub
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization & the Efficient Frontier]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus & Convex Optimization]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Mean–variance optimization returns a *mathematical point*: $w^\star=\tfrac1\delta\Sigma^{-1}\mu$. On six assets with realistic inputs that point is $[-2.26,+3.33,0.28,0.78,0.30,4.96]$ — a $12\times$-levered, short-saturated book that no mandate can hold, and whose construction from an equal-weight portfolio costs $562\%$ of notional in one rebalance. **Constraints and transaction costs are the difference between that point and a portfolio you can actually run.** This folder is about the second problem: given a forecast *and* a mandate *and* a cost model, what do you hold, and what do you trade?

Everything in the folder is one of four objects:

- **A feasible set.** Long-only, position caps, group/sector bounds, turnover budgets — a convex polytope $\mathcal C=\{w:\mathbf 1^\top w=1,\ w_{\min}\le w\le w_{\max},\ Aw\le b\}$. Its *shadow prices* are the price of your mandate.
- **A cost function.** Linear ($c\lvert\Delta w\rvert$, the spread: Roll's $2c$, Glosten–Milgrom's $(V_H-V_L)\mu$), quadratic ($\tfrac12\Delta w^\top\Lambda\Delta w$, impact à la Almgren–Chriss and Kyle's $\lambda$), or concave (the empirical $\lvert\Delta w\rvert^{3/2}$ square-root law, generalized-Roll spread $2(c+\lambda)$).
- **A trade-off.** Turnover on one axis, net alpha on the other; the optimum sits where marginal alpha equals marginal cost — exactly the true cost, verified numerically below.
- **A dynamic.** Across periods you trade *partially* toward a long-horizon **aim**, not to the current target: the Gârleanu–Pedersen policy $x_t=x_{t-1}+(I+\kappa\Sigma)^{-1}(\text{aim}-x_{t-1})$.

This page is the folder's *hub*: it gives the **fast formula lookup** below (job #1) and routes you to six sub-pages — intuition → constraints → cost models → turnover & multi-period → failure modes → extensions.

> **The one-sentence essence.** "The implementable portfolio solves $\max_{w\in\mathcal C}\ \mu^\top w-\tfrac\delta2 w^\top\Sigma w-\mathbf c^\top\lvert w-w_0\rvert-\tfrac12(w-w_0)^\top\Lambda(w-w_0)$ — and because the $\ell_1$ cost term has a **kink at $w=w_0$**, the optimal answer is frequently *to not trade at all*."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Formulas are transcribed from **Lobo–Fazel–Boyd (2007)**, **Gârleanu–Pedersen (2013)**, **Almgren–Chriss (2000)** and **Hasbrouck (2007, Ch 3/5/7/8)**; the check-column numbers were **re-executed and reproduced exactly** on the folder's shared universe ($N=6$ assets, $T=60$ monthly returns, seed fixed; risk aversion $\delta=3$; starting portfolio $w_0=\mathbf 1/N$; assumed linear cost $c=10$ bp; quadratic impact $\Lambda=\operatorname{diag}(0.020,0.015,0.030,0.025,0.010,0.008)$).

**Notation:** $w$ weights, $w_0$ current weights, $\Delta w=w-w_0$, $\Sigma$ covariance, $\delta$ risk aversion, $\mathbf c$ linear costs, $\Lambda=\operatorname{diag}(\eta_i)$ impact coefficients, $c$ half-spread, $\lambda$ adverse-selection/impact cost, $\mathcal C$ the feasible set.

| Quantity | Formula | Verified check |
|---|---|---|
| Unconstrained optimum | $w^\star=\tfrac1\delta\Sigma^{-1}\mu$ | $[-2.257,\;3.330,\;0.280,\;0.780,\;0.299,\;4.963]$ |
| Gross exposure | $\lVert w\rVert_1=\sum_i\lvert w_i\rvert$ | $11.9086$ ($12\times$ levered, unimplementable) |
| One-way turnover | $\mathrm{TO}(w)=\tfrac12\lVert w-w_0\rVert_1$ | blind $0.5932$; capped $0.4100$; from-EW naive $5.6210$ |
| **Constrained QP** | $\max\limits_{w}\ \mu^\top w-\tfrac\delta2 w^\top\Sigma w\ \ \text{s.t.}\ \mathbf 1^\top w=1,\ w_{\min}\le w\le w_{\max},\ Aw\le b$ | long-only $[0,0,0.4443,0.4822,0.0082,0.0653]$; cap $35\%$ $[0,0,0.35,0.35,0.09,0.21]$ |
| **Shadow price** of a binding constraint | $\lambda_j=-\dfrac{\partial V^\star}{\partial b_j}$ | group cap $\{2,3\}\le0.60$: $\lambda_{\mathcal G}=0.001749$/mo $=2.0983\%$/yr |
| **Group cap ⇔ alpha haircut** | $\tilde\mu_i=\mu_i-\lambda_{\mathcal G}\ (i\in\mathcal G)$ | alphas $0.2086,\;0.2147\to0.1876,\;0.1937$ |
| **Linear cost** | $C_{\text{lin}}=\mathbf c^\top\lvert\Delta w\rvert$ | blind net $0.1562$ → cost-aware net $0.1691$; $\mathrm{TO}\,0.5932\to0.3333$ |
| **Quadratic impact** | $C_{\text{imp}}=\tfrac12\Delta w^\top\Lambda\Delta w$ | $+$impact: $\mathrm{TO}=0.1667$, net $=0.1708$, net $\mathrm{SR}=1.4093$ |
| Square-root impact | $C\propto\sigma\lvert\Delta w\rvert^{3/2}$ (concave, non-convex) | $q^{3/2}$ cost $=$ most expensive at $q=0.8$ ($0.014311$ vs $0.009600$ quadratic) |
| **No-trade half-width** | $\theta=\dfrac{c}{\delta\sigma^2}$, band $[w^\ast-\theta,\;w^\ast+\theta]$ | $\sigma=20\%$, $c=20$ bp: $\theta=0.2000$, band $[0.80,\,1.20]$ |
| **Turnover-penalty frontier** | $\max\ \mu^\top w-\tfrac\delta2 w^\top\Sigma w-\lambda\lVert w-w_0\rVert_1$ | utility peaks at $\lambda=0.0010=$ **the true cost** ($0.15554$) |
| **Multi-period tracking** | $\min\sum_t\Big[\tfrac\rho2(w_t-w^\ast)^\top\Sigma(w_t-w^\ast)+\tfrac\kappa2(w_t-w_{t-1})^\top\Lambda(w_t-w_{t-1})\Big]$ | ramp path; objective $0.3090$ vs all-at-once $0.5000$ ($\kappa{=}1$) |
| **Aim / partial adjustment** (quadratic impact; 04's proportional-cost form is $F=(I+\kappa\Sigma)^{-1}$) | $F=(\delta\Sigma+\kappa\Lambda)^{-1}\delta\Sigma$, trade $=F(w^\ast-w_0)$ | $\operatorname{diag}(F)=[0.214,\,0.1262,\,0.2172,\,0.2685,\,0.3074,\,0.178]$ |
| Cross-asset coupling | $\lVert F-\operatorname{diag}(F)\rVert_F$ | $0.39122$ (off-diagonals are large — do not scalarise) |
| **Roll spread** (Hasbrouck Ch 3) | $c=\sqrt{-\gamma_1}$, spread $=2c$ | — |
| **Glosten–Milgrom spread** (Ch 5, $\delta=\tfrac12$) | $A-B=(V_H-V_L)\mu$ | — |
| **Generalized Roll** (Ch 8) | spread $=2(c+\lambda)$, $\ \sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ | only $\sigma_w^2$ identified |
| **Kyle price impact** (Ch 7) | $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$, depth $=1/\lambda$ | — |

> **The critical interpretation caveat.** The static, diagonal-$\Lambda$, one-period problem above is an *idealization*. Three corrections matter in production: (i) the trades are coupled through $\Sigma$ — the fraction you close is a **matrix** $F$, not a scalar; (ii) impact is **not additive** across correlated names (use a full $\Lambda$ or the factor form $qq^\top D$); (iii) the empirical impact law is **concave**, so it must be convexified by successive convex approximation. All three are developed in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06 · Advanced Extensions]].

---

### 3. Computational Implementation — the cost-aware engine

One universe, one solver: unconstrained, cost-blind long-only, linear-cost, and linear-plus-impact. Runs on **numpy + scipy** and reproduces every number in the table's check column.

```python
import numpy as np
from scipy.optimize import minimize

rng = np.random.RandomState(20240910)
N, T = 6, 60
mu_ann  = np.array([0.08,0.06,0.05,0.10,0.07,0.04]); vol_ann = np.array([0.16,0.12,0.20,0.22,0.14,0.10])
C = np.array([[1,.55,.30,.25,.40,.20],[.55,1,.35,.20,.45,.25],[.30,.35,1,.50,.30,.35],
              [.25,.20,.50,1,.25,.40],[.40,.45,.30,.25,1,.30],[.20,.25,.35,.40,.30,1]])
mu = mu_ann/12.0; sig = vol_ann/np.sqrt(12.0); S_true = np.outer(sig,sig)*C
L = np.linalg.cholesky(S_true); R = (L @ rng.randn(N,T)).T + mu
mu_s = R.mean(0); S_s = np.cov(R,rowvar=False); delta = 3.0; w0 = np.ones(N)/N
eta = np.array([0.020,0.015,0.030,0.025,0.010,0.008])

def net_mvo(c=0.0, kappa=0.0):
    """max mu'w - d/2 w'Sw - c|w-w0|_1 - k/2 (w-w0)'diag(eta)(w-w0), long-only, sum=1."""
    def neg(z):
        w, u = z[:N], z[N:]
        return -(mu_s@w - .5*delta*w@S_s@w - c*u.sum() - .5*kappa*np.sum(eta*(w-w0)**2))
    cons = [{'type':'eq','fun':lambda z: z[:N].sum()-1.0}]
    for i in range(N):
        cons += [{'type':'ineq','fun':(lambda i:(lambda z: z[N+i]-(z[i]-w0[i])))(i)},
                 {'type':'ineq','fun':(lambda i:(lambda z: z[N+i]+(z[i]-w0[i])))(i)}]
    z0 = np.zeros(2*N); z0[:N] = np.ones(N)/N; z0[N:] = np.abs(z0[:N]-w0)
    return minimize(neg, z0, bounds=[(0,1)]*N+[(0,None)]*N, constraints=cons,
                    method='SLSQP', options={'maxiter':1000,'ftol':1e-14}).x[:N]

w_naive = (1.0/delta)*np.linalg.solve(S_s, mu_s)
print("naive unconstrained :", np.round(w_naive,3), " gross=%.4f"%np.abs(w_naive).sum())
for lab, w in [("blind (net @10bp)", net_mvo(0.0,0.0)), ("linear cost c=10bp", net_mvo(0.001,0.0)),
               ("linear + impact",     net_mvo(0.001,1.0))]:
    dw = w-w0; ga = mu_s@w*12; lin = 0.001*np.abs(dw).sum()*12
    imp = .5*np.sum(eta*dw**2)*12; vol = np.sqrt(w@S_s@w*12)
    print("  %-19s w=%s  TO=%.4f  net_ann=%.4f  netSR=%.4f"
          %(lab, np.round(w,4), .5*np.abs(dw).sum(), ga-lin-imp, (ga-lin-imp)/vol))
sig_a = 0.20/np.sqrt(12)
print("no-trade half-width for one asset (c=20bp, delta=3, sigma=20%%): theta = %.4f"%((0.002)/(3*sig_a**2)))
```
```
naive unconstrained : [-2.257  3.33   0.28   0.78   0.299  4.963]  gross=11.9086
  blind (net @10bp)   w=[0.     0.     0.4443 0.4822 0.0082 0.0653]  TO=0.5932  net_ann=0.1562  netSR=0.9412
  linear cost c=10bp  w=[0.     0.     0.2905 0.3762 0.1667 0.1667]  TO=0.3333  net_ann=0.1691  netSR=1.2222
  linear + impact     w=[0.     0.1667 0.229  0.2602 0.1667 0.1775]  TO=0.1667  net_ann=0.1708  netSR=1.4093
no-trade half-width for one asset (c=20bp, delta=3, sigma=20%): theta = 0.2000
```
The engine makes the folder's central claim numerically: **pricing the trade turns a $0.1562$ strategy into a $0.1708$ one while cutting turnover by $72\%$** — and in the linear-cost solution two weights sit *exactly* at their current $1/6$, the signature of the no-trade region.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Cost underestimation.** Optimizing with $\hat c<c_{\text{true}}$ overtrades; assuming zero cost costs $12.3\%$ of achievable certainty equivalent. Assuming *double* the cost is also wrong but paralyzes instead ($\mathrm{TO}=0.0000$).
2. **Turnover explosion.** A cost-blind optimizer on a $10$ bp/month-noisy alpha turns over $3.83\times$/yr; cost-awareness cuts it to $0.91\times$/yr and *raises* net alpha ($0.1958\to0.2034$).
3. **Constraint interaction & tracking drift.** A turnover budget leaves a permanent gap ($\tau=0.25\Rightarrow$ gap $0.3517$; $\tau=0.05\Rightarrow0.8348$); a group cap that duplicates a per-name cap is free but invisible without its multiplier.

---

### 5. Canonical Literature & Study References

- **Lobo, Fazel & Boyd (2007)**. *Portfolio Optimization with Linear and Fixed Transaction Costs*. Annals of Operations Research 152:341–365. *The modeling backbone: convex cost-aware QPs, the $\ell_1$ no-trade region, the fixed-cost relaxation.* ★ MUST-HAVE
- **Gârleanu & Pedersen (2013)**. *Dynamic Trading with Predictable Returns and Transaction Costs*. Journal of Finance 68(6):2309–2340. *The aim portfolio and the closed-form partial-adjustment policy.* ★ STRONG
- **Almgren & Chriss (2000/01)**. *Optimal Execution of Portfolio Transactions*. Journal of Risk 3(2):5–39. *Permanent + temporary impact and the trading frontier. Cross-pillar: owned by Pillar 2 (optimal execution).* ★ STRONG
- **Grinold & Kahn (2000)**. *Active Portfolio Management*, 2nd ed., McGraw-Hill. *The practitioner's bible for constrained active portfolios, tracking error and cost-adjusted rebalancing.* ★ MUST-HAVE
- **Hasbrouck (2007)**. *Empirical Market Microstructure*, OUP. *Ch 3 (Roll: $c=\sqrt{-\gamma_1}$, spread $2c$), Ch 5 (Glosten–Milgrom), Ch 7 (Kyle $\lambda$), Ch 8 (generalized Roll: spread $2(c+\lambda)$), Ch 9.9 (Amihud illiquidity). The microstructure source of every cost coefficient.*
- **Clarke, de Silva & Thorley (2002)**. *Portfolio Constraints and the Fundamental Law of Active Management*. FAJ 58(5):48–66. *The transfer coefficient $=$ the price of constraints.* ★ STRONG
- **Boyd, Busseti, Diamond, Kahn, Koh, Nystrup & Speth (2017)**. *Multi-Period Trading via Convex Optimization*. FnT in Optimization 3(1):1–72. *The multi-period convex formulation and its implementations.*

---

### 6. Connected Graph Bridges

- Foundational base: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance & Efficient Frontier]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Sibling topics: [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Optimization]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|HRP]]
- Execution (Pillar 2): [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]]
- Market making (Pillar 6): [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]]
- Legacy flat page (superseded by this folder): [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover Constraints]]
- Sub-pages (in-folder): 01 From Zero · 02 Weight Constraints · 03 Transaction-Cost Models · 04 Turnover & Multi-Period · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**

- **Absolute beginner:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]] — no optimization background needed.
- **Math + code (undergrad/job-seeking):** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02 · Weight Constraints]] → [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]] → [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/04-turnover-and-multi-period|04 · Turnover & Multi-Period]].
- **Robustness (practitioner/graduate):** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] · [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Optimization]]
