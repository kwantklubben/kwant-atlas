---
title: "05 — Failure Modes & Practice: Cost Underestimation, Turnover Explosion, Constraint Interaction"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - failure-modes
  - cost-underestimation
  - turnover-explosion
  - tracking-drift
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/04-turnover-and-multi-period|04 · Turnover & the Multi-Period Trade-Off]].

---

### 1. Intuition & Practical Objective

Every failure in this folder is a *discrepancy between the objective you optimized and the objective you were actually paid on*. There are exactly three places that discrepancy enters, and each has a name in industry:

1. **Cost underestimation** — you optimized with $\hat c$ but the market charged $c_{\text{true}}>\hat c$. The optimizer then trades too much, and the extra trades earn less than they cost. This is *the* reason strategies die between backtest and production.
2. **Turnover explosion** — your alphas are noisy, your optimizer is linear in $\Sigma^{-1}$, and every fresh estimate re-shuffles the whole book. The portfolio becomes a perpetuum mobile of commissions: high gross, negative net.
3. **Constraint interaction & tracking drift** — a turnover budget or a tight cap does not just slow you down; it silently changes *where* you can be, so you accumulate an unmanaged gap to the target that you never fully close.

The practical objective of this page is diagnostic: given a strategy that looks good on paper and loses money live, decide in five minutes *which* of these three is happening, because the fixes are completely different (re-estimate costs / shrink the alphas / loosen the budget respectively).

> **The one-sentence essence.** "Optimizing with the wrong cost is a *bias*; optimizing a noisy alpha with no cost term is a *variance*; enforcing a budget without tracking the residual is a *drift* — and a strategy must survive all three."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Cost underestimation is a bias you can bound

Let $w(\hat c)$ solve the cost-aware problem with assumed cost $\hat c$ and true cost $c_{\text{true}}$. Realized certainty equivalent is

$$U(\hat c)=\mu^\top w(\hat c)-\tfrac\delta2 w(\hat c)^\top\Sigma\,w(\hat c)-c_{\text{true}}\lVert w(\hat c)-w_0\rVert_1 .$$

Because $w(\hat c)$ is the maximizer of the objective *with $\hat c$*, the envelope theorem gives

$$\frac{dU}{d\hat c}\Big|_{\hat c=c_{\text{true}}}=0,$$

so **$U$ is maximized exactly at the true cost** — and mistakes are locally second-order but *quadratic* in the error. In practice the curve is asymmetric: assuming $\hat c=0$ (a cost-free backtest) is a far bigger error than assuming $\hat c=2c_{\text{true}}$, because the zero-cost problem has no no-trade region at all and therefore trades continuously. §3(A) quantifies it.

#### 2.2 Turnover explosion is the estimation-error amplifier again

From the unconstrained first-order condition, the weight sensitivity to the alpha signal is

$$w^\star=\tfrac1\delta\Sigma^{-1}\mu\ \Longrightarrow\ dw^\star=\tfrac1\delta\Sigma^{-1}d\mu,$$

so an alpha revision $d\mu$ in the small-eigenvalue direction of $\Sigma$ moves weights by a *large* multiple. If alphas are re-estimated every period with noise of size $s$, the expected per-period turnover scales like $\tfrac1\delta\lVert\Sigma^{-1}\rVert\,s$ — the same $\Sigma^{-1}$ amplification that makes naive MVO an estimation-error maximizer ([[pillars/05-portfolio-optimization/robust-optimization/02-the-estimation-error-problem|02]]), now paid in *trading costs* rather than in risk. Two structural facts matter:

- **The $\ell_1$ no-trade band is the only brake.** Without it, turnover is linear in the noise; with it, small alpha revisions produce *zero* trade until the gap clears $\theta=c/(\delta\sigma^2)$.
- **The cost-blind annualized turnover is a property of the signal's noise, not of the market.** §3(B) shows a cost-blind optimizer at $10$ bp/month alpha noise turning over $3.83\times$/yr; the same optimizer on a noisier signal would turn further.

#### 2.3 A budget truncates, and the residual *accumulates*

If you cap per-period turnover at $\tau$ by scaling the trade, then whenever the required move exceeds $\tau$ you leave a residual gap

$$g_t=\bigl(w_t^{\text{target}}-w_t\bigr),\qquad \lVert g_t\rVert_1\ \text{persists and accumulates until the target stops moving}.$$

Over a horizon in which the target keeps revising, the steady-state gap is roughly the ratio of the per-period revision rate to the budget — you are chasing a moving object with a speed limit. §3(C) measures it. The first-principles warning: **a turnover budget is a tracking-error budget in disguise**, and it should be *chosen* with that in mind rather than set at "whatever the risk committee last used."

---

### 3. Computational Implementation — the three failure modes, measured

**(A)** assume $\hat c\in\{0,5,10,25,50\}$ bp while the true cost is $25$ bp and watch realized utility; **(B)** a $24$-month backtest with noisy alphas, cost-blind vs cost-aware; **(C)** truncate turnover at a per-period budget and measure the accumulated tracking gap. numpy + scipy.

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

def net_mvo(mu_, w_prev, c):
    def neg(z):
        w,u = z[:N], z[N:]
        return -(mu_@w - .5*delta*w@S_s@w - c*u.sum())
    cons=[{'type':'eq','fun':lambda z: z[:N].sum()-1.0}]
    for i in range(N):
        cons += [{'type':'ineq','fun':(lambda i:(lambda z: z[N+i]-(z[i]-w_prev[i])))(i)},
                 {'type':'ineq','fun':(lambda i:(lambda z: z[N+i]+(z[i]-w_prev[i])))(i)}]
    z0=np.zeros(2*N); z0[:N]=np.ones(N)/N; z0[N:]=np.abs(z0[:N]-w_prev)
    return minimize(neg,z0,bounds=[(0,1)]*N+[(0,None)]*N,constraints=cons,
                    method='SLSQP',options={'maxiter':1000,'ftol':1e-14}).x[:N]

# (A) cost underestimation: assume c_hat, true cost = 25 bps
c_true = 0.0025
print("(A) cost underestimation   (TRUE cost = 25 bps)")
print("  assumed   TO      net_ann  netSR   utility")
for ch in (0.0, 0.0005, 0.0010, 0.0025, 0.0050):
    w = net_mvo(mu_s, w0, ch); dw = w - w0
    ga = mu_s@w*12; ca = c_true*np.abs(dw).sum()*12
    u = (mu_s@w - .5*delta*w@S_s@w - c_true*np.abs(dw).sum())*12
    vol = np.sqrt(w@S_s@w*12)
    print("  %5.0fbps   %.4f  %.4f   %.4f  %.5f"%(ch*1e4, .5*np.abs(dw).sum(), ga-ca, (ga-ca)/vol, u))

# (B) 24-month backtest with noisy alphas, noise 10 bps/month (true cost 10 bps)
print("\n(B) 24-month backtest, alpha noise 10 bps/month (true cost 10 bps)")
rng = np.random.RandomState(2024); H = 24; s = 0.001
sig_t = [mu_s + rng.randn(N)*s for _ in range(H)]
for lab, c in [("cost-blind", 0.0), ("cost-aware", 0.0010)]:
    w = np.ones(N)/N; to = cost = gross = 0.0
    for t in range(H):
        wn = net_mvo(sig_t[t], w, c); dw = wn - w
        to += .5*np.abs(dw).sum(); cost += 0.0010*np.abs(dw).sum(); gross += sig_t[t]@wn; w = wn
    print("  %-11s avg TO/period=%.4f (ann %.2f)  gross_ann=%.4f  cost_ann=%.4f  net_ann=%.4f"
          %(lab, to/H, to/H*12, gross/H*12, cost/H*12, (gross-cost)/H*12))

# (C) turnover-budget truncation -> tracking drift
print("\n(C) turnover-budget truncation vs tracking drift (H=12, budget tau/period)")
for tau in (0.05, 0.10, 0.25, None):
    rng = np.random.RandomState(2024); w = np.ones(N)/N; to = gap = 0.0
    for t in range(12):
        tgt = net_mvo(mu_s + rng.randn(N)*s, w, 0.0)          # cost-blind target
        dw = tgt - w
        if tau is not None and np.abs(dw).sum() > tau:
            dw = dw * (tau/np.abs(dw).sum())                  # truncate the trade
        w = w + dw
        to += .5*np.abs(dw).sum(); gap += np.abs(w-tgt).sum()
    print("  tau=%-5s avg TO=%.4f  avg ||w-target||_1=%.4f"
          %(("none" if tau is None else "%.2f"%tau), to/12, gap/12))
```
```
(A) cost underestimation   (TRUE cost = 25 bps)
  assumed   TO      net_ann  netSR   utility
      0bps   0.5932  0.1715   1.0334  0.13017
      5bps   0.4085  0.1716   1.1847  0.14016
     10bps   0.3333  0.1722   1.2452  0.14354
     25bps   0.1667  0.1711   1.3938  0.14850
     50bps   0.0000  0.1623   1.4039  0.14225

(B) 24-month backtest, alpha noise 10 bps/month (true cost 10 bps)
  cost-blind  avg TO/period=0.3188 (ann 3.83)  gross_ann=0.2035  cost_ann=0.0077  net_ann=0.1958
  cost-aware  avg TO/period=0.0758 (ann 0.91)  gross_ann=0.2052  cost_ann=0.0018  net_ann=0.2034

(C) turnover-budget truncation vs tracking drift (H=12, budget tau/period)
  tau=0.05  avg TO=0.0250  avg ||w-target||_1=0.8348
  tau=0.10  avg TO=0.0500  avg ||w-target||_1=0.6581
  tau=0.25  avg TO=0.1250  avg ||w-target||_1=0.3517
  tau=none  avg TO=0.2425  avg ||w-target||_1=0.0000
```

Four verified readings:

- **(A) The optimizer is honest about cost — you have to be honest too.** Utility peaks at $\hat c=25$ bp $=c_{\text{true}}$ ($0.14850$), exactly the envelope-theorem prediction. Assuming *zero* cost costs $12.3\%$ of the achievable certainty equivalent ($0.14850\to0.13017$); assuming *double* ($50$ bp) costs $4.2\%$ ($0.14225$) and drives turnover to literally **zero** ($\text{TO}=0.0000$) — you leave the entire book untouched even though trading is profitable. **The asymmetry is the lesson: underestimating costs overtrades, overestimating them paralyzes.**
- **(B) Cost-awareness cuts turnover by $76\%$ and *raises* net alpha.** Cost-blind: annualized turnover $3.83\times$, gross $0.2035$, net $0.1958$. Cost-aware: turnover $0.91\times$, gross $0.2052$, net $0.2034$. Gross alpha is essentially unchanged ($0.2035\to0.2052$) — the cost-aware optimizer gives up nothing — yet $\approx77\%$ of the annual cost bill disappears. This is the clearest possible refutation of the folk belief that "cost-aware optimization costs you alpha."
- **(C) A turnover budget leaves a permanent tracking gap.** With $\tau=0.25$/period the residual gap is $0.3517$ in $\ell_1$; tighten to $\tau=0.05$ and the gap balloons to $0.8348$ — the portfolio is more than $80\%$ of notional away from its own target, *on average*, forever. The gap is not a transient; it is the steady state of chasing a moving target under a speed limit.
- **(C) The budget's benefit is invisible in the gap.** Look at what the budget actually purchased: at $\tau=0.25$ you spend half the turnover ($0.1250$ vs $0.2425$) of the cost-blind policy for a gap of $0.35$. Whether that is a good trade *requires the cost model* — which is why a budget without a cost estimate is a blind policy.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Backtesting at zero cost.** The most common single error in quantitative finance. It removes the no-trade region entirely, so the backtest trades continuously and reports an alpha that exists only in the absence of a market. Always backtest with the *assumed* cost inside the optimizer and the *true* (conservatively high) cost applied to realized returns.
2. **Underestimating impact for large notional.** Proportional costs are known; impact is estimated. When AUM grows, the same weights imply larger trades, $\eta$ rises with size, and a strategy that worked at \$10M stops working at \$1B — not because the signal decayed but because the *cost function changed*. Re-estimate $\eta$ as a function of your own AUM, not from a vendor deck.
3. **Treating noise in alphas as signal to trade on.** Every fresh estimate looks like an opportunity to a cost-blind optimizer. The remedy is two-sided: shrink the alphas ([[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]]) *and* price the trades.
4. **Setting the turnover budget without a tracking-error target.** §3(C) shows the budget *is* a tracking-error budget. A risk committee that sets $\tau=0.05$ "to be safe" is silently choosing an $0.83$ tracking gap per period. Make the substitution explicit.
5. **Ignoring the constraint price when combining constraints.** A per-name cap plus a group cap plus a turnover budget interact (§02): after enough constraints, the marginal one is free and the binding one is invisible. Always report the active set and the multipliers, not just the weights.

---

### 5. Canonical Literature & Study References

- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed. — the marginal-alpha = marginal-cost rebalancing discipline and its failure modes.
- **Lobo, Fazel & Boyd (2007)**, Annals of OR 152:341–365 — the convex cost model whose parameters you must estimate honestly.
- **Almgren & Chriss (2000/01)**, Journal of Risk 3(2) — the impact model behind the "underestimating impact" failure. *Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Pillar 2]].*
- **Clarke, de Silva & Thorley (2002)**, FAJ 58(5):48–66 — the transfer coefficient as the accounting of constraint-induced information loss.
- **DeMiguel, Garlappi & Uppal (2009)**, RFS 22(5):1915–1953 — the sobering benchmark: sophisticated optimizers must beat $1/N$ *net of costs* to be worth running.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 3 & 9.9 — the empirical spread range ($\$0.01$–$\$0.49$ in one stock-month) and the Amihud illiquidity ratio as the calibration warning for any single $c$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/04-turnover-and-multi-period|04 · Turnover & the Multi-Period Trade-Off]]
- Siblings: [[pillars/05-portfolio-optimization/robust-optimization/05-failure-modes-and-practice|Robust Optimization · 05]] (input-error failure modes) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|MVO · Estimation-Error Maximizers]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]]
- Continue: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06 · Advanced Extensions]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
