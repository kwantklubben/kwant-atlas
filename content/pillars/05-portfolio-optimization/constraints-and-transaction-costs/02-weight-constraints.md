---
title: "02 — Weight Constraints: Long-Only, Caps, and Group Bounds"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - long-only
  - position-caps
  - group-constraints
  - shadow-price
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Weight constraints are the practitioner's first line of defence, and they do three jobs at once:

- **Feasibility** — a long-only mandate with a $35\%$ cap cannot be short $225\%$ in anything; the constraint *deletes* the region of portfolio space where the estimation-error fantasy lives.
- **Specification** — an index fund, a $130/30$ fund, a UCITS vehicle and a pension mandate are *defined* by their constraint sets. The constraint is not a limitation on the strategy; it *is* the strategy's mandate.
- **Risk management** — sector, country, issuer and factor caps prevent the optimizer from expressing one concentrated bet through many correlated names.

The practical objective of this page is to make the *cost* of a constraint precise. Every constraint you add either (a) does not bind — in which case it is free, or (b) binds — in which case it has a **shadow price**: a number, in units of certainty-equivalent utility, that tells you exactly what one more unit of that constraint would buy. That number is what you negotiate with risk and compliance about.

> **The one-sentence essence.** "A constraint is a *knife* applied to the feasible set: it slices away part of portfolio space; the Lagrange multiplier of a binding constraint is the *price* of the slice, and a group cap is exactly equivalent to *subtracting that price from the alphas* of the group it restricts."

---

### 2. Mathematical Ground Truth & Derivations

**The box-constrained QP.** The standard solved problem is

$$
\max_{w}\ \mu^\top w-\tfrac\delta2\,w^\top\Sigma w
\qquad\text{s.t.}\qquad \mathbf 1^\top w=1,\quad w_{\min}\le w\le w_{\max},\quad Aw\le b .
$$

**KKT / shadow price.** For a binding constraint $a_j^\top w=b_j$ with multiplier $\lambda_j\ge0$, stationarity reads

$$
\mu-\delta\Sigma w-\nu\mathbf 1-\sum_j\lambda_j a_j\mp\zeta=0,
$$

where $\nu$ is the budget multiplier and $\zeta\ge0$ the box multipliers ($\zeta_i>0$ only when $w_i=w_{\min}$ or $w_{\max}$). By the envelope theorem the multiplier is the marginal value of the constraint:

$$
\boxed{\ \lambda_j=-\frac{\partial V^\star}{\partial b_j}\ },\qquad V^\star=\max_{w\in\mathcal C}\ \mu^\top w-\tfrac\delta2 w^\top\Sigma w .
$$

So $\lambda_j$ is *the certainty-equivalent return you forgo per unit of tightness*. It is the right currency for arguing about constraints.

**The group-cap ⇔ alpha-haircut theorem.** Suppose the only additional constraint is a group cap $\sum_{i\in\mathcal G} w_i\le g$ with multiplier $\lambda_{\mathcal G}$. Stationarity over the group members is

$$
\mu_i-\delta(\Sigma w)_i-\nu-\lambda_{\mathcal G}=0\quad(i\in\mathcal G).
$$

Compare this with the *unconstrained-in-group* problem whose alphas have been **reduced** by $\lambda_{\mathcal G}$:

$$
\tilde\mu_i=\mu_i-\lambda_{\mathcal G}\quad(i\in\mathcal G).
$$

The first-order conditions are identical. Therefore:

$$
w^\star\big(\text{group cap }g\big)\;=\;w^\star\big(\text{uncapped, alphas }\mu-\lambda_{\mathcal G}\mathbf 1_{\mathcal G}\big),
$$

for the value of $\lambda_{\mathcal G}$ that makes the group sum exactly $g$. **A group/sector cap is nothing but a uniform alpha haircut on the group** — which is why sector-neutralising a signal and capping sector exposure give nearly the same portfolio. §3 verifies the identity numerically.

**Two warnings embedded in the math.**

1. *Caps on weights are not caps on risk.* The constraint set is a box in $w$-space, but the risk is $w^\top\Sigma w$. Highly correlated names each at the $35\%$ cap can aggregate into a single factor bet far above $35\%$ of risk. The correct object to cap is the *factor exposure* $Bw$, i.e. an $A w\le b$ row with $A=B$ — not a diagonal box.
2. *Constraints interact.* A $35\%$ per-name cap and a $60\%$ group cap overlap: if the cap already forces the group sum below $60\%$, the group constraint is **non-binding and free** (§3). Always check which multipliers are non-zero before paying for a constraint.

---

### 3. Computational Implementation — long-only, caps, and the price of a group cap

Same $N=6$ universe as [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01]]. We solve (i) long-only, (ii) long-only with a $35\%$ cap, and (iii) long-only with a **$60\%$ group cap** on assets $\{2,3\}$, found by bisecting the equivalent alpha haircut $\lambda_{\mathcal G}$. numpy + scipy.

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
mu_s = R.mean(0); S_s = np.cov(R,rowvar=False); delta = 3.0

def mvo(mu_, lo=0.0, hi=1.0):                              # long-only box MVO
    neg = lambda w: -(mu_@w - 0.5*delta*w@S_s@w)
    r = minimize(neg, np.ones(N)/N, bounds=[(lo,hi)]*N,
                 constraints=[{'type':'eq','fun':lambda w: w.sum()-1}],
                 method='SLSQP', options={'maxiter':2000,'ftol':1e-16})
    return r.x
ce = lambda w: mu_s@w - 0.5*delta*w@S_s@w                  # certainty equivalent

w_lo, w_cap = mvo(mu_s), mvo(mu_s, hi=0.35)
print("long-only:", np.round(w_lo,4), " CE=%.6f"%ce(w_lo))
print("cap35    :", np.round(w_cap,4), " CE=%.6f"%ce(w_cap))

# group cap on {2,3} at 0.60  ==  alpha haircut lambda_G  (bisection on lambda_G)
G = [2,3]
def solve_g(lam):
    m = mu_s.copy(); m[G] -= lam
    return mvo(m)
lo, hi = 0.0, 0.01
for _ in range(60):
    mid = 0.5*(lo+hi)
    if solve_g(mid)[G].sum() > 0.60: lo = mid
    else: hi = mid
lamG = 0.5*(lo+hi); wg = solve_g(lamG)
print("group cap 60pct {2,3}: lambda_G=%.6f monthly (%.4f pct ann)  w=%s  sum=%.4f  CE=%.6f"
      %(lamG, lamG*12*100, np.round(wg,4), wg[G].sum(), ce(wg)))
print("   raw alpha_ann", np.round(mu_s[G]*12,4), "-> haircut", np.round((mu_s[G]-lamG)*12,4))
print("   CE loss vs long-only = %.6f"%(ce(w_lo)-ce(wg)))
```
```
long-only: [0.     0.     0.4443 0.4822 0.0082 0.0653]  CE=0.013814
cap35    : [0.   0.   0.35 0.35 0.09 0.21]  CE=0.013670
group cap 60pct {2,3}: lambda_G=0.001749 monthly (2.0983 pct ann)  w=[0.     0.     0.26   0.34   0.1473 0.2527]  sum=0.6000  CE=0.013528
   raw alpha_ann [0.2086 0.2147] -> haircut [0.1876 0.1937]
   CE loss vs long-only = 0.000286
```

Three verified findings:

- **The cap is a knife, not a haircut.** The $35\%$ cap moves asset 3 from $0.4443\to0.35$ and asset 4 from $0.4822\to0.35$ and pushes the freed $22.65\%$ into assets 5 and 6 ($0.0082\to0.09$, $0.0653\to0.21$). Certainty equivalent falls $0.013814\to0.013670$; the difference is the **price of the cap** in monthly utility.
- **The group cap *is* an alpha haircut.** Capping $\{2,3\}$ at $60\%$ is exactly reproduced by subtracting $\lambda_{\mathcal G}=0.001749$ monthly from both assets' alphas — i.e. **$2.10\%$/yr off each** ($0.2086\to0.1876$, $0.2147\to0.1937$). The identity is exact, not approximate: the constraint prices itself as a uniform alpha penalty on the restricted group.
- **Constraints interact — and can become redundant.** Re-solve with *both* the $35\%$ cap and the $60\%$ group cap and the answer is again $[0,0,0.26,0.34,0.1473,0.2527]$: the group cap already pins $w_2+w_3=0.60$ with neither weight above $0.34$, so the per-name cap never binds. The general lesson: always read the multipliers — a constraint with a zero multiplier is one you are not paying for, and a redundant cap adds reporting burden without changing a single weight.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Capping weights, not risk.** A $35\%$ per-name cap on a block of eight $0.9$-correlated names permits an $80\%$-of-risk single-factor exposure. Weight caps are a *liquidity/concentration* tool; factor caps ($Bw\le b$) are the *risk* tool. Conflating them is the most common institutional error.
2. **Over-tight caps collapse to $1/N$.** As $w_{\max}\to1/N$, the box alone determines the answer and the alphas become irrelevant. You have re-derived the naive portfolio with extra steps and thrown away all signal — the constraint cost curve is convex, and the last increment of tightness is the most expensive ([[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05]]).
3. **Asymmetric caps create hidden tilts.** Capping a long-only book at $35\%$ while leaving the minimum at $0$ implicitly favours small assets; if the cap binds on the *high-alpha* names only, the realized portfolio systematically under-weights exactly where the signal is strongest — a *transfer coefficient* below $1$ (Clarke–de Silva–Thorley 2002).
4. **Ignoring the price of a constraint.** A risk committee that says "cap everything at $10\%$" is making a quantitative statement about forgone utility whether it knows it or not. §3's $\lambda_{\mathcal G}$ is the number that should appear in the meeting notes; without it, constraint-setting is guesswork.

---

### 5. Canonical Literature & Study References

- **Frost & Savarino (1988)**, *For better performance: constrain portfolio weights*, Journal of Portfolio Management — the classic argument that weight constraints reduce estimation risk.
- **Clarke, de Silva & Thorley (2002)**, *Portfolio Constraints and the Fundamental Law of Active Management*, FAJ 58(5):48–66 — the transfer coefficient $\mathrm{TC}<1$ that quantifies what a constraint set costs in information ratio.
- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed. — active risk, tracking-error budgets, constrained active construction and the fundamental law.
- **Lobo, Fazel & Boyd (2007)**, Annals of OR 152:341–365 — convex formulation with the box and linear constraints, plus the fixed-cost extension.
- **Markowitz (1952)**, *Portfolio Selection*, JoF 7(1):77–91 — the original QP whose feasible set is the object we are drawing knives across.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]]
- Siblings: [[pillars/05-portfolio-optimization/robust-optimization/04-constraints-and-resampling|Robust Optimization · Constraints as Robustness]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance & the Efficient Frontier]]
- Cost continuation: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]]
- Foundations: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (KKT, Lagrange multipliers, the envelope theorem) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
