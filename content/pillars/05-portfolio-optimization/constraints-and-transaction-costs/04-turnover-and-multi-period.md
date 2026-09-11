---
title: "04 — Turnover Control & the Multi-Period Trade-Off"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - turnover
  - multi-period
  - trade-off-frontier
  - gârleanu-pedersen
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]].

---

### 1. Intuition & Practical Objective

Turnover is the *rate* at which you convert an alpha model into trading. Everything in this folder lives on this axis: a brilliant signal rebalanced daily at $300\%$ annual turnover can lose money, while a modest signal rebalanced quarterly can compound. This page answers the two questions a practitioner actually faces:

1. **How much may I trade?** Two controls: **penalize** turnover with a linear price $\lambda$ (an economic cost), or **budget** it with a hard constraint $\lVert w-w_0\rVert_1\le\tau$ (a risk control). The first requires you to know your cost; the second does not, and is therefore what risk desks prefer.
2. **How fast should I converge?** The target is a *moving* object — alphas revise every period. The great insight of the dynamic-trading literature (Gârleanu & Pedersen 2013) is that you should trade **partially toward an "aim" portfolio**, not jump to the current target, because a jump buys a noisy estimate you will want to undo next period.

> **The one-sentence essence.** "Turnover is a *dial*, and the optimal setting is where the marginal alpha of one more unit of trading equals the marginal cost of executing it — in a static problem that is a penalty $\lambda$; across periods it is a *fraction* of the way to a long-horizon aim."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Two ways to control turnover

**Penalty form.** Add $\lambda\lVert w-w_0\rVert_1$ to the objective:

$$
\max_{w\in\mathcal C}\ \ \mu^\top w-\tfrac\delta2 w^\top\Sigma w-\lambda\,\lVert w-w_0\rVert_1 .
$$

By the envelope logic of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02]], $\lambda$ *is* the model's assumed cost per unit of trading. Choosing $\lambda$ therefore means choosing a cost forecast — and §3 shows that the certainty-equivalent-optimal $\lambda$ lands exactly on the true cost, which is the cleanest possible statement of "price your trades honestly."

**Budget form.** Instead cap the $\ell_1$ distance:

$$
\max_{w\in\mathcal C}\ \ \mu^\top w-\tfrac\delta2 w^\top\Sigma w\quad\text{s.t.}\quad \lVert w-w_0\rVert_1\le\tau .
$$

This is *convex*, needs no cost estimate, and is the form a risk committee is happy to mandate ("no more than $20\%$ turnover per rebalance"). The price of the budget is its shadow price — exactly the $\lambda$ that the penalty form would have used.

**The trade-off frontier.** Sweep either control and plot the pairs $(\text{turnover},\ \text{net alpha})$:

$$
\text{net }\alpha_{\text{ann}}(\lambda)=\underbrace{12\,\mu^\top w(\lambda)}_{\text{gross}}-\underbrace{12\,c_{\text{true}}\lVert w(\lambda)-w_0\rVert_1}_{\text{realized cost}} .
$$

#### 2.2 The multi-period problem and partial adjustment

Over $H$ periods, ignoring the path is a mistake. The canonical tracking problem is

$$
\min_{\{w_t\}}\ \sum_{t=1}^{H}\Big[\tfrac\rho2\,(w_t-w^\ast)^\top\Sigma\,(w_t-w^\ast)\;+\;\tfrac\kappa2\,(w_t-w_{t-1})^\top\Lambda\,(w_t-w_{t-1})\Big],
$$

a **tracking-error penalty on $w_t$** plus a **cost penalty on the move**. In the scalar case this is a tridiagonal linear system whose solution is a monotone ramp to the target, and its asymptotic behaviour is *geometric*:

$$
w_t-w^\ast\;\approx\;G^{\,t}\,(w_0-w^\ast),\qquad G=1+\tfrac{a}{2}-\sqrt{a+\tfrac{a^2}{4}},\quad a=\frac{\rho\sigma^2}{\kappa\eta}.
$$

- **Cheap trading ($\kappa$ small, $a$ large) ⇒ $G\to0$:** jump to the target at once.
- **Expensive trading ($\kappa$ large, $a$ small) ⇒ $G\to1$:** creep toward it; over a finite horizon you may never arrive.

**The Gârleanu–Pedersen aim (preview of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).** With predictable returns and *proportional* costs, the optimal policy is

$$
\boxed{\ x_t=x_{t-1}+(I+\kappa\Sigma)^{-1}\big(\text{aim}_t-x_{t-1}\big)\ },\qquad
\text{aim}=(I+\kappa\Sigma)^{-1}\big(\delta\Sigma\big)^{-1}\mu,
$$

i.e. trade a **matrix fraction** $(I+\kappa\Sigma)^{-1}$ of the gap between the aim portfolio and the current book — not all of it. The matrix is non-diagonal, so a signal in one name moves several weights: cross-asset cost coupling (verified in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).

---

### 3. Computational Implementation — the frontier and the ramp

**(A)** sweep the linear penalty $\lambda$ and report turnover, gross alpha, *realized* net alpha at a true cost of 10 bp, net Sharpe and certainty-equivalent utility. **(B)** solve the multi-period tracking problem and compare the optimal ramp to "all at once" and "equal slices." numpy + scipy.

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
c_true = 0.0010                                            # TRUE linear cost, 10 bps

def net_mvo(lam):
    """max mu'w - d/2 w'Sw - lam|w-w0|_1, long-only, sum=1."""
    def neg(z):
        w, u = z[:N], z[N:]
        return -(mu_s@w - .5*delta*w@S_s@w - lam*u.sum())
    cons = [{'type':'eq','fun':lambda z: z[:N].sum()-1.0}]
    for i in range(N):
        cons += [{'type':'ineq','fun':(lambda i:(lambda z: z[N+i]-(z[i]-w0[i])))(i)},
                 {'type':'ineq','fun':(lambda i:(lambda z: z[N+i]+(z[i]-w0[i])))(i)}]
    z0 = np.zeros(2*N); z0[:N] = np.ones(N)/N; z0[N:] = np.abs(z0[:N]-w0)
    return minimize(neg, z0, bounds=[(0,1)]*N+[(0,None)]*N, constraints=cons,
                    method='SLSQP', options={'maxiter':1000,'ftol':1e-14}).x[:N]

print("(A) turnover-penalty frontier  (true cost 10 bps)")
print("  lambda    TO      gross    net      netSR   utility")
for lam in (0.0,0.00025,0.0005,0.00075,0.001,0.0015,0.002,0.003,0.004):
    w = net_mvo(lam); dw = w - w0
    ga = mu_s@w*12; net = (mu_s@w - c_true*np.abs(dw).sum())*12
    vol = np.sqrt(w@S_s@w*12)
    u = (mu_s@w - .5*delta*w@S_s@w - c_true*np.abs(dw).sum())*12
    print("  %.5f  %.4f  %.4f  %.4f  %.4f  %.5f"
          %(lam, .5*np.abs(dw).sum(), ga, net, net/vol, u))

# (B) multi-period partial adjustment (scalar, quadratic impact)
def trajectory(H=8, kappa=1.0, rho=1.0, wt=1.0, w_start=0.0):
    """min sum_t rho/2 (w_t-wt)^2 + kappa/2 (w_t-w_{t-1})^2,  w_0 = w_start"""
    A = np.zeros((H,H))
    for i in range(H):
        A[i,i] += rho + (kappa if i==H-1 else 2*kappa)
        if i>0:   A[i,i-1] -= kappa
        if i<H-1: A[i,i+1] -= kappa
    b = rho*wt*np.ones(H); b[0] += kappa*w_start
    return np.linalg.solve(A, b)

print("\n(B) multi-period partial adjustment (target=1.0, start=0.0, H=8)")
for kap in (0.25, 1.0, 4.0, 16.0):
    print("  kappa=%5.2f  path=%s"%(kap, np.round(trajectory(kappa=kap),4)))
def obj(path, kap, rho=1.0, wt=1.0, w_start=0.0):
    prev = w_start; c = 0.0
    for w in path:
        c += rho/2*(w-wt)**2 + kap/2*(w-prev)**2; prev = w
    return c
for kap in (1.0, 4.0, 16.0):
    print("  kappa=%5.2f: objective  all-at-once=%.4f  equal-slice=%.4f  optimal=%.4f"
          %(kap, obj(np.ones(8),kap), obj(np.arange(1,9)/8,kap), obj(trajectory(kappa=kap),kap)))
```
```
(A) turnover-penalty frontier  (true cost 10 bps)
  lambda    TO      gross    net      netSR   utility
  0.00000  0.5932  0.2071  0.1928  1.1621  0.15153
  0.00025  0.4998  0.2015  0.1895  1.2228  0.15349
  0.00050  0.4085  0.1962  0.1863  1.2862  0.15486
  0.00075  0.3334  0.1922  0.1842  1.3319  0.15554
  0.00100  0.3333  0.1922  0.1842  1.3320  0.15554
  0.00150  0.1667  0.1811  0.1771  1.4427  0.15450
  0.00200  0.1667  0.1811  0.1771  1.4427  0.15450
  0.00300  0.1667  0.1811  0.1771  1.4427  0.15450
  0.00400  0.0952  0.1731  0.1709  1.4326  0.14952

(B) multi-period partial adjustment (target=1.0, start=0.0, H=8)
  kappa= 0.25  path=[0.8284 0.9706 0.9949 0.9991 0.9999 1.     1.     1.    ]
  kappa= 1.00  path=[0.618  0.8541 0.9443 0.9787 0.9919 0.9969 0.9987 0.9994]
  kappa= 4.00  path=[0.3902 0.6279 0.7725 0.8603 0.9132 0.9444 0.9616 0.9693]
  kappa=16.00  path=[0.2135 0.3779 0.5034 0.5979 0.6672 0.7157 0.7465 0.7614]
  kappa= 1.00: objective  all-at-once=0.5000  equal-slice=1.1562  optimal=0.3090
  kappa= 4.00: objective  all-at-once=2.0000  equal-slice=1.3438  optimal=0.7803
  kappa=16.00: objective  all-at-once=8.0000  equal-slice=2.0938  optimal=1.7083
```

Three verified readings:

- **(A) The utility-optimal $\lambda$ is exactly the true cost.** Certainty-equivalent utility peaks at $0.15554$ over $\lambda\in[0.00075,\,0.0010]$, and $0.0010$ *is* the true 10 bp cost used to compute realized net alpha. Miss it low ($\lambda=0$) and you overtrade: turnover $0.5932$, net Sharpe $1.1621$, utility $0.15153$. Miss it high ($\lambda=0.004$) and you undertrade: turnover drops to $0.0952$ but gross alpha falls to $0.1731$ and utility to $0.14952$. **The frontier is a hump, and its peak is the honest cost.**
- **(A) Net Sharpe and utility disagree — know which you are optimizing.** Net Sharpe rises monotonically with $\lambda$ ($1.1621\to1.4427$) because shrinking risk raises the ratio, while *utility* peaks in the middle because it also counts the alpha you gave up. A desk judged on Sharpe will always over-penalize turnover; a desk judged on dollars will not. State the objective before tuning the dial.
- **(B) The optimal path is a geometric ramp, and "all-at-once" is only right when trading is cheap.** With $\kappa=1$ the optimum (objective $0.3090$) beats both all-at-once ($0.5000$) and equal slices ($1.1562$). As impact grows to $\kappa=16$ the ramp flattens dramatically ($w_1=0.2135$ vs $0.618$ at $\kappa=1$) and the *advantage over all-at-once explodes* ($1.7083$ vs $8.0000$): at high cost, front-loading is catastrophic. Note the path never reaches the target within $H=8$ at $\kappa=16$ — the horizon is a real constraint, and "finish rebalancing" is a choice, not an identity.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tuning $\lambda$ by feel instead of by cost.** §3 shows the penalty is a *cost forecast*; setting it "to be safe" makes you skip good trades. The correct discipline is to set $\lambda$ equal to your measured marginal cost (or to the shadow price of a turnover budget you have committed to).
2. **The turnover budget hides regime change.** A tight $\tau$ glues the portfolio to a stale book exactly when the world has moved (a regime shift looks identical to noise in a one-period problem). Budgets are about *inputs* you can see; robustness about *regimes* is a different tool ([[pillars/05-portfolio-optimization/robust-optimization/05-failure-modes-and-practice|Robust · 05]]).
3. **Single-period myopia.** Re-solving "optimally" every period with a fresh target front-loads trades and re-trades the same signal repeatedly — the turnover spiral of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05]]. The fix is the partial-adjustment / aim policy, not a bigger penalty.
4. **Ignoring the trading horizon.** The ramp of §3(B) shows the target may be unreachable in $H$ periods at high cost. Pretending you will "finish the rebalance" next week when the cost model says otherwise is a forecast error, and it is a systematic one.

---

### 5. Canonical Literature & Study References

- **Gârleanu, Nicolae & Pedersen, Lasse Heje (2013)**, *Dynamic Trading with Predictable Returns and Transaction Costs*, Journal of Finance 68(6):2309–2340 — the aim portfolio and the closed-form partial-adjustment policy. ★ STRONG
- **Boyd, Busseti, Diamond, Kahn, Koh, Nystrup & Speth (2017)**, *Multi-Period Trading via Convex Optimization*, Foundations and Trends in Optimization 3(1):1–72 — the multi-period convex formulation and its tractability.
- **Lobo, Fazel & Boyd (2007)**, Annals of OR 152:341–365 — the linear/fixed-cost static problem underlying the penalty form.
- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed. — the marginal-alpha = marginal-cost rebalancing rule.
- **Clarke, de Silva & Thorley (2002)**, FAJ 58(5):48–66 — transfer-coefficient accounting when turnover is constrained.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] (the *within-day* version of the ramp) · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]]
- Siblings: [[pillars/05-portfolio-optimization/robust-optimization/04-constraints-and-resampling|Robust · Constraints as Robustness]] (turnover as a $w$-space constraint) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] (churn from noisy inputs)
- Continue: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06 · Advanced Extensions]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
