---
title: "03 — The Black–Litterman Formula: Bayesian Posterior & Optimal Weights"
tags:
  - pillar-portfolio-optimization
  - black-litterman
  - bayesian-updating
  - posterior
  - master-formula
---

**Basic Prerequisites:** [[foundations/bayesian-statistics/03-posterior-inference|Posterior Inference]] and [[pillars/05-portfolio-optimization/black-litterman/02-reverse-optimization|Reverse Optimization]].

---

### 1. Intuition & Practical Objective

This page derives **the core BL update**: how views and the market prior combine into one posterior mean $\bar\mu$ and a posterior covariance $M$. The objective is a pair of formulas — the **full conjugate form** and the numerically-stable **Master formula** — plus the final unconstrained optimal-weights expression. If §02 gave you a sane *starting* place, this section gives you the *blending algorithm*.

The intuition is a leveraged weighted average. Your prior says "the market is right, $r\sim\mathcal{N}(\Pi,\tau\Sigma)$." Each view says "I think the market is wrong along direction $P_i$ by $Q_i$." Where they meet is a **precision-weighted compromise**: pieces of the world you're confident about (small $\Omega$) get honored almost fully; pieces the market calls (large prior uncertainty or weak view) get mostly ignored. The Master formula makes it explicit — the posterior is the prior *plus* a confidence-weighted correction proportional to the **view residual** $(Q-P\Pi)$.

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Prior on the (unknown, random) expected-return vector $r$:
$$r \sim \mathcal{N}(\Pi,\ \tau\Sigma).$$
Views, expressed as a noisy linear constraint on $r$ (Black–Litterman 1992, Idzorek eq. 5–6):
$$P\, r = Q + \varepsilon,\qquad \varepsilon \sim \mathcal{N}(0_H,\ \Omega),$$
where $P$ is $K\times N$, $Q$ is $K$, $\Omega$ is $K\times K$. Each row of $P$ is a view: **absolute** view on asset $i$ has $P_{ki}=1$; **relative** view "$i$ out-returns $j$ by $q$" has $P_{ki}=+1,\ P_{kj}=-1$ and $Q=q$.

**Bayesian posterior (conjugate Gaussian).** By the standard Normal–Normal update (the same machinery as Bayesian linear regression — ESL §3; see [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|Bayes & Priors]]), the posterior is Normal with:
$$\bar\mu = \Big[(\tau\Sigma)^{-1}+P^T\Omega^{-1}P\Big]^{-1}\Big[(\tau\Sigma)^{-1}\Pi+P^T\Omega^{-1}Q\Big],$$
$$M = \Big[(\tau\Sigma)^{-1}+P^T\Omega^{-1}P\Big]^{-1}.$$
Here $(\tau\Sigma)^{-1}$ is the **prior precision**, $P^T\Omega^{-1}P$ the **view precision** projected into asset space, and the posterior precision is their sum. This is a precision-weighted average — exactly like a Bayesian ridge estimate.

**The Master formula (numerically stable).** Directly inverting $(\tau\Sigma)^{-1}$ invites numerical trouble. The Woodbury identity (Sherman–Morrison) transforms the mean into
$$\bar\mu = \Pi + \tau\Sigma P^T\big[P\,\tau\Sigma\,P^T+\Omega\big]^{-1}\big(Q-P\Pi\big).$$
The structure is beautiful: $\Pi$ (market) **plus** the *leverage* $\tau\Sigma P^T$ times the *Kalman gain* $[P\tau\Sigma P^T+\Omega]^{-1}$ times the *view residual* $(Q-P\Pi)$. The gain matrix is only $K\times K$ (small) — that is why it is the workhorse implementation.

**Final weights.** Unconstrained MVO on $\bar\mu$ with risk-aversion $\delta$:
$$w^\* = \tfrac{1}{\delta}\Sigma^{-1}\bar\mu.$$

**Limits (shot through with sanity).** If there are no views ($P=0$), $\bar\mu=\Pi$ and $w^\*=\tfrac1\delta\Sigma^{-1}\Pi=w_{mkt}$ exactly. If a view has $\Omega\to\infty$ (no confidence), the gain $\to0$ and again $\bar\mu\to\Pi$. Both identities are the first thing every implementation should test.

---

### 3. Computational Implementation — both forms, both limits

Verifies both formulas agree exactly, the zero-view identity recovers $w_{mkt}$, and the $\Omega\to\infty$ limit also returns to the market.

```python
import numpy as np
from numpy.linalg import inv as inv

Sigma = np.array([[0.040,0.015,0.010],[0.015,0.030,0.012],[0.010,0.012,0.050]])
w_mkt = np.array([0.50,0.30,0.20]); delta, tau = 2.5, 0.05
Pi = delta * (Sigma @ w_mkt)

def prior_precision():  return inv(tau*Sigma)

def posterior_mu(P, Q, Om):
    """Full conjugate form."""
    Sp  = P.T @ inv(Om) @ P
    return inv(prior_precision() + Sp) @ (prior_precision()@Pi + P.T@inv(Om)@Q)

def master_mu(P, Q, Om):
    """Numerically stable Woodbury form."""
    return Pi + (tau*Sigma@P.T) @ inv(P@(tau*Sigma)@P.T + Om) @ (Q - P@Pi)

P = np.array([[1.0,0.0,-1.0]]); Q = np.array([0.04])
Om = np.diag(np.diag(P @ (tau*Sigma) @ P.T))

mu_full = posterior_mu(P,Q,Om); mu_master = master_mu(P,Q,Om)
print("full form   :", np.round(mu_full,6))
print("master form :", np.round(mu_master,6), "  agree =", np.allclose(mu_full,mu_master))

w = (1.0/delta) * inv(Sigma) @ mu_master
print("optimal w   :", np.round(w,4), " sum=", round(w.sum(),4))

# zero-view -> market
print("no-view w   :", np.round((1.0/delta)*inv(Sigma)@Pi,4), "== w_mkt",
      np.allclose((1.0/delta)*inv(Sigma)@Pi, w_mkt))

# infinite-uncertainty view -> market
w_inf = (1.0/delta) * inv(Sigma) @ master_mu(P,Q,np.array([[1e10]]))
print("Omega->inf  :", np.round(w_inf,4), "== w_mkt",
      np.allclose(w_inf, w_mkt))
```
```
full form   : [0.070589 0.047684 0.040714]
master form : [0.070589 0.047684 0.040714]   agree = True
optimal w   : [0.5579 0.3    0.1421]  sum= 1.0
no-view w   : [0.5 0.3 0.2] == w_mkt True
Omega->inf  : [0.5 0.3 0.2] == w_mkt True
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Inverting $(\tau\Sigma)^{-1}$ directly.** If $\Sigma$ is near-singular (near-collinear assets), $\tau\Sigma$ is too, and the full form amplifies noise. The Master formula never forms $(\tau\Sigma)^{-1}$ — use it.
2. **Confusing $M$ with $\Sigma$. $\bar\mu$'s covariance is $M$ (posterior *estimate* uncertainty), not the assets' return covariance $\Sigma$. For portfolio risk (rather than return-estimate risk) you generally want $\Sigma+M$ combined — see [[pillars/05-portfolio-optimization/black-litterman/06-advanced-extensions|06 · Advanced Extensions]].
3. **Over-constraining views.** If two views overlap the same assets ($P$ rows correlated), $P^T\Omega^{-1}P$ can be ill-conditioned; ensure $\Omega\neq 0$ and views are linearly independent.

---

### 5. Canonical Literature & Study References

- **Black & Litterman (1992)**, §The Combined Model — the original posterior derivation.
- **Satchell & Scowcroft (2000)**, §2 — the cleanest derivation of the posterior and its special cases.
- **Idzorek (2005)**, §Steps 1–7 — computation of $\bar\mu$ and $w^\*$ step by step.
- **Bayesian bridge**: the Normal–Normal conjugate update is the same form as Bayesian linear regression — see **Hastie, Tibshirani & Friedman**, *ESL*, §3.3 (Bayesian ridge) in the verified corpus `esl_ch1-5.md`.

---

### 6. Connected Graph Bridges

- Base: [[foundations/bayesian-statistics/03-posterior-inference|Posterior Inference]] · [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|Bayes & Priors]] · [[pillars/05-portfolio-optimization/black-litterman/02-reverse-optimization|02 · Reverse Optimization]]
- Continue: [[pillars/05-portfolio-optimization/black-litterman/04-views-and-confidence|04 · Views & Confidence]] · [[pillars/05-portfolio-optimization/black-litterman/index|Index Hub]]