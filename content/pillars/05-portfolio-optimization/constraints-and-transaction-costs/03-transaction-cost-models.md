---
title: "03 — Transaction-Cost Models: Linear Spreads, Quadratic and Square-Root Impact"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - transaction-costs
  - market-impact
  - no-trade-region
  - roll-model
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]] and [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02 · Weight Constraints]].

---

### 1. Intuition & Practical Objective

A trade of size $\Delta w$ costs money in three distinct ways, and treating them as one number is the classic modeling error:

1. **The spread (linear, unavoidable).** Cross the bid–ask and you pay roughly half the spread per share, plus commissions, exchange fees and taxes. This cost is **linear** in the quantity traded and *independent of size* — the same per-unit price whether you buy a hundred shares or a hundred thousand, up to the point where you have eaten the top of the book.
2. **Market impact (convex, size-dependent).** Once your order consumes more than the displayed liquidity, you *walk the book* and then you *signal* your intent to others. The price moves against you, and the larger the order the worse the average price. This cost is **convex** in the quantity traded.
3. **The square-root law (empirical, concave).** Measured across markets, realized impact scales roughly like $\sigma\sqrt{Q/V}$ — the *cost* therefore scales like $Q^{3/2}$, which is **concave** in $Q$. Doubling the order does not double the cost.

The practical objective is to know which term dominates at your size — and it is a knife-edge. At small size the linear term rules and the optimizer has a clean no-trade region. At large size the convex impact term rules and the optimizer trades *less and slower*. At institutional size the concave square-root law rules, and the problem is no longer convex, so you must either convexify it (a conservative approximation) or accept that the true optimum may require mixing orders.

> **The one-sentence essence.** "Cost is a *function of the trade*, not a constant: linear at the touch, convex when you walk the book, concave when you measure the square-root law — and the shape of that function, not its level, is what determines whether you rebalance, how much, and how fast."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Where the linear coefficient comes from (microstructure)

The linear coefficient $c$ is not a free parameter — it is the *spread*, and microstructure gives it a structural decomposition.

- **Roll (1984), Hasbrouck Ch 3.** With an efficient price $m_t=m_{t-1}+u_t$ and a round-trip transactional cost $c$, trade prices are $p_t=m_t+q_tc$ with $q_t=\pm1$. Then $\gamma_0\equiv\operatorname{Var}(\Delta p_t)=2c^2+\sigma_u^2$ and $\gamma_1\equiv\operatorname{Cov}(\Delta p_{t-1},\Delta p_t)=-c^2$, so
$$c=\sqrt{-\gamma_1},\qquad \text{spread}=2c .$$
- **Glosten–Milgrom (1985), Hasbrouck Ch 5.** With a symmetric value prior ($\delta=\tfrac12$) and fraction $\mu$ of informed traders, the zero-profit spread is $A-B=(V_H-V_L)\mu$ — the *adverse-selection* component.
- **Generalized Roll (Hasbrouck Ch 8).** Split the cost into a non-informational part $c$ and an adverse-selection/price-impact part $\lambda$: $m_t=m_{t-1}+\lambda q_t+u_t$, $p_t=m_t+cq_t$, so
$$\boxed{\ \text{spread}=2(c+\lambda)\ },\qquad \gamma_0=c^2+(c+\lambda)^2+\sigma_u^2,\quad \gamma_1=-c(c+\lambda),$$
with only $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ identified from two autocovariances. **Kyle (1985), Hasbrouck Ch 7** supplies the equilibrium price impact $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ as a function of value uncertainty $\Sigma_0$ and noise-trading variance $\sigma_u^2$, with $1/\lambda$ the *market depth*. **Amihud's illiquidity ratio** $I_t=\lvert r_t\rvert/\text{Vol}_t$ is the standard empirical proxy for $\lambda$ (Hasbrouck Ch 9.9).

#### 2.2 Quadratic impact (convex)

Model per-trade impact cost with a diagonal matrix $\Lambda=\operatorname{diag}(\eta_1,\dots,\eta_N)$ reflecting each asset's depth:

$$C_{\text{impact}}(\Delta w)=\tfrac12\,\Delta w^\top\Lambda\,\Delta w=\tfrac12\sum_i\eta_i\,(\Delta w_i)^2 .$$

This is the time-integrated version of the Almgren–Chriss *permanent + temporary* impact model ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Pillar 2]]), compressed into one rebalance. Convexity is the whole point: the optimization stays a QP and the answer is unique and computable.

#### 2.3 The square-root law (concave → non-convex)

Empirically $C_{\text{impact},i}\propto\sigma_i\,\lvert\Delta w_i\rvert^{3/2}$ (since impact $\propto\sigma\sqrt{Q/V}$ and cost $=\text{impact}\times Q$). Concavity has a sharp consequence: the marginal cost of the *last* unit is *lower* than the average, so a concave-cost optimizer wants to **concentrate** trades rather than spread them — the opposite of the convex case. Non-convexity also means the KKT conditions no longer certify a global optimum, and practical solvers use successive convex approximations (the $\ell_1$-or-quadratic upper/lower surrogates of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).

#### 2.4 The cost-aware portfolio problem

$$\boxed{\ \max_{w\in\mathcal C}\ \ \mu^\top w-\tfrac\delta2 w^\top\Sigma w\;-\;\mathbf c^\top\lvert w-w_0\rvert\;-\;\tfrac12(w-w_0)^\top\Lambda(w-w_0)\ }$$

The **no-trade region** (derived in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01]]) is the defining feature: for a single asset the optimal action is

$$w^\star=\begin{cases}w_0 & \bigl\lvert w_0-w^\ast\bigr\rvert\le\theta,\\ w^\ast\mp\theta & \text{otherwise},\end{cases}\qquad
\theta=\frac{c}{\delta\sigma^2},\quad w^\ast=\frac{\mu}{\delta\sigma^2}.$$

Written for a portfolio, the $i$-th asset moves only if the alpha gain *in the direction of the trade* exceeds the per-unit cost — which is why the cost-aware solution below leaves two of six weights *exactly* at their current values.

---

### 3. Computational Implementation — the three cost families

**(A)** the single-asset no-trade region in closed form; **(B)** the full portfolio with (i) no cost, (ii) linear only, (iii) linear + quadratic impact, plus a sweep of the impact severity $\kappa$; **(C)** the cost curves of the three laws. numpy + scipy.

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
eta = np.array([0.020,0.015,0.030,0.025,0.010,0.008])       # impact: less liquid -> larger

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

# (A) one-asset no-trade region, closed form
sig_a = 0.20/np.sqrt(12); mu_a, d_a, c_a = 0.01, 3.0, 0.002
w_star = mu_a/(d_a*sig_a**2); theta = c_a/(d_a*sig_a**2)
print("(A) single asset: w* = %.4f  theta = %.4f  no-trade band = [%.4f, %.4f]"
      %(w_star, theta, w_star-theta, w_star+theta))
for w_cur in (0.70, 0.85, 1.20, 1.40):
    w = w_cur if abs(w_star-w_cur) <= theta else (w_star-theta if w_cur < w_star-theta else w_star+theta)
    print("    w0=%.2f -> w_opt=%.4f  trade=%+.4f"%(w_cur, w, w-w_cur))

# (B) cost-aware portfolio, linear spread + quadratic impact
print("(B) cost-aware (blind / linear only / linear+impact):")
for lab, c, k in [("blind", 0.0, 0.0), ("linear", 0.001, 0.0), ("lin+impact", 0.001, 1.0)]:
    w = net_mvo(c, k); dw = w-w0
    ga = mu_s@w*12; lin = 0.001*np.abs(dw).sum()*12; imp = .5*np.sum(eta*dw**2)*12
    vol = np.sqrt(w@S_s@w*12); net = ga-lin-imp
    print("  %-11s TO=%.4f gross=%.4f lin=%.5f imp=%.5f net=%.4f vol=%.4f netSR=%.4f w=%s"
          %(lab, .5*np.abs(dw).sum(), ga, lin, imp, net, vol, net/vol, np.round(w,4)))
print("  kappa sweep (c=0.001):")
for k in (0.0,0.25,0.5,1.0,2.0,4.0):
    w = net_mvo(0.001, k); dw = w-w0
    ga = mu_s@w*12; imp = .5*np.sum(eta*dw**2)*12; net = ga-0.001*np.abs(dw).sum()*12-imp
    vol = np.sqrt(w@S_s@w*12)
    print("    k=%.2f TO=%.4f imp_ann=%.5f net_ann=%.4f netSR=%.4f w=%s"
          %(k, .5*np.abs(dw).sum(), imp, net, net/vol, np.round(w,4)))

# (C) impact-law shapes
print("(C) cost of trading quantity q (linear 1bp/u, quadratic 0.5*0.03*q^2, sqrt 0.02*q^1.5):")
for q in (0.05,0.10,0.20,0.40,0.80):
    print("    q=%.2f  linear=%.6f  quadratic=%.6f  sqrt(3/2)=%.6f"
          %(q, 0.001*q, .5*0.03*q*q, 0.02*q**1.5))
```
```
(A) single asset: w* = 1.0000  theta = 0.2000  no-trade band = [0.8000, 1.2000]
    w0=0.70 -> w_opt=0.8000  trade=+0.1000
    w0=0.85 -> w_opt=0.8500  trade=+0.0000
    w0=1.20 -> w_opt=1.2000  trade=-0.0000
    w0=1.40 -> w_opt=1.2000  trade=-0.2000
(B) cost-aware (blind / linear only / linear+impact):
  blind       TO=0.5932 gross=0.2071 lin=0.01424 imp=0.03665 net=0.1562 vol=0.1659 netSR=0.9412 w=[0.     0.     0.4443 0.4822 0.0082 0.0653]
  linear      TO=0.3333 gross=0.1922 lin=0.00800 imp=0.01518 net=0.1691 vol=0.1383 netSR=1.2222 w=[0.     0.     0.2905 0.3762 0.1667 0.1667]
  lin+impact  TO=0.1667 gross=0.1802 lin=0.00400 imp=0.00535 net=0.1708 vol=0.1212 netSR=1.4093 w=[0.     0.1667 0.229  0.2602 0.1667 0.1775]
  kappa sweep (c=0.001):
    k=0.00 TO=0.3333 imp_ann=0.01518 net_ann=0.1691 netSR=1.2222 w=[0.     0.     0.2905 0.3762 0.1667 0.1667]
    k=0.25 TO=0.1973 imp_ann=0.00674 net_ann=0.1715 netSR=1.3701 w=[0.     0.136  0.2362 0.2944 0.1667 0.1667]
    k=0.50 TO=0.1667 imp_ann=0.00567 net_ann=0.1712 netSR=1.3986 w=[0.     0.1667 0.2282 0.2718 0.1667 0.1667]
    k=1.00 TO=0.1667 imp_ann=0.00535 net_ann=0.1708 netSR=1.4093 w=[0.     0.1667 0.229  0.2602 0.1667 0.1775]
    k=2.00 TO=0.0922 imp_ann=0.00163 net_ann=0.1683 netSR=1.4250 w=[0.0745 0.1667 0.201  0.2179 0.1667 0.1732]
    k=4.00 TO=0.0476 imp_ann=0.00044 net_ann=0.1658 netSR=1.4202 w=[0.1191 0.1667 0.1845 0.1934 0.1667 0.1697]
(C) cost of trading quantity q (linear 1bp/u, quadratic 0.5*0.03*q^2, sqrt 0.02*q^1.5):
    q=0.05  linear=0.000050  quadratic=0.000038  sqrt(3/2)=0.000224
    q=0.10  linear=0.000100  quadratic=0.000150  sqrt(3/2)=0.000632
    q=0.20  linear=0.000200  quadratic=0.000600  sqrt(3/2)=0.001789
    q=0.40  linear=0.000400  quadratic=0.002400  sqrt(3/2)=0.005060
    q=0.80  linear=0.000800  quadratic=0.009600  sqrt(3/2)=0.014311
```

Four verified readings:

- **(A) The no-trade region is real and wide.** With $\sigma=20\%$ p.a., $\delta=3$ and $c=20\,\mathrm{bp}$, the half-width is $\theta=0.20$ — twenty *percentage points* of weight. A held weight of $0.85$ against a target of $1.00$ produces **zero trade**; only a deviation beyond $\pm0.20$ ($0.70$ or $1.40$) triggers a trade, and even then only *back to the band edge* ($0.80$/$1.20$), not to the target.
- **(B) Cost-awareness raises risk-adjusted return while cutting turnover.** The blind portfolio delivers $\mathrm{SR}_{\text{net}}=0.9412$ after its own trade costs. Adding only the linear spread lifts this to $1.2222$; adding quadratic impact lifts it to $1.4093$ — while turnover falls $0.5932\to0.3333\to0.1667$. Note the mechanics of the no-trade region: in the linear-only solution assets 5 and 6 sit *exactly* at their current $1/6=0.1667$; the optimizer declines to touch them.
- **(B, sweep) More impact severity ⇒ less trading, to a point.** As $\kappa$ rises from $0$ to $4$, turnover falls monotonically $0.3333\to0.0476$, but net Sharpe *peaks* near $\kappa\in[1,2]$ ($1.4093\to1.4250$) and then declines: over-penalizing impact leaves real alpha unharvested. This is the same dose-response curve as robustness ([[pillars/05-portfolio-optimization/robust-optimization/05-failure-modes-and-practice|05]]).
- **(C) The three laws cross.** Below $q\approx0.09$ the *linear* cost dominates; the quadratic overtakes it soon after; and the concave square-root law is *cheapest* at small size but *most expensive* at large size ($0.014311$ at $q=0.8$ vs $0.009600$ quadratic). **Which cost model you choose changes the direction the optimizer wants to move.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming static linear costs.** Treating cost as a constant $c$ in basis points is right at the touch and wrong the moment size matters. In illiquid names or at open/close, the convex and concave regimes dominate and the linear-only solution over-trades by a wide margin.
2. **Ignoring impact *additivity*.** Summing per-asset impact $\tfrac12\sum_i\eta_i\Delta w_i^2$ assumes your own names are independent. In reality trades share a factor: selling eight correlated names at once is *one* large market-wide trade, and the joint impact is larger than the sum of the parts (a cross-impact matrix $\Lambda$ with off-diagonal entries is the correct object; see [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).
3. **Using one $c$ for the whole universe.** Frontline names and small-caps differ by an order of magnitude in spread. A scalar $c$ makes the optimizer over-trade the expensive names and under-trade the cheap ones — precisely backwards. Hasbrouck's Ch 3 finding that the quoted spread ranged $\$0.01$–$\$0.49$ *within one stock over one month* is the empirical warning.
4. **Forgetting that the cost model is a forecast, not a measurement.** $\eta$ and $c$ are estimated from past executions under past conditions. Underestimating them by a factor of two is the single most common cause of a strategy that backtests well and loses money live — quantified in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05]].

---

### 5. Canonical Literature & Study References

- **Lobo, Fazel & Boyd (2007)**, *Portfolio Optimization with Linear and Fixed Transaction Costs*, Annals of OR 152:341–365 — convex cost-aware formulations; the linear-and-fixed-cost model.
- **Almgren & Chriss (2000/01)**, *Optimal Execution of Portfolio Transactions*, Journal of Risk 3(2):5–39 — permanent + temporary impact and the trading frontier. *Cross-pillar: owned by [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Pillar 2]].*
- **Hasbrouck (2007)**, *Empirical Market Microstructure* — Ch 3 (Roll: $c=\sqrt{-\gamma_1}$, spread $=2c$), Ch 5 (Glosten–Milgrom spread $=(V_H-V_L)\mu$), Ch 7 (Kyle: $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$), Ch 8 (generalized Roll: $\text{spread}=2(c+\lambda)$), Ch 9.9 (Amihud illiquidity $\lvert r\rvert/\text{Vol}$). *The microstructure source of every coefficient here.*
- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed. — transaction-cost-adjusted rebalancing and the marginal-cost = marginal-alpha rule.
- **Kyle (1985)**, *Continuous Auctions and Insider Trading*, Econometrica 53(6):1315–1335 — the equilibrium price-impact foundation.
- **Amihud (2002)**, *Illiquidity and Stock Returns*, Journal of Financial Markets 5(1):31–56 — the illiquidity-ratio proxy for $\lambda$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02 · Weight Constraints]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]]
- Microstructure source: [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit-Order-Book Mechanics & L3]]
- Continue: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/04-turnover-and-multi-period|04 · Turnover & the Multi-Period Trade-Off]]
- Foundations: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
