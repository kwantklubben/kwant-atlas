---
title: "5.6.4 Constraint-Based Robustness & Resampling (Michaud)"
tags:
  - pillar-portfolio-optimization
  - robust-optimization
  - constraints
  - resampling
  - turnover
  - weight-caps
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/robust-optimization/03-robust-formulations|03 · Robust Formulations]] and [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]].

---

### 1. Intuition & Practical Objective

Robustness does not require uncertainty sets. Two older, blunter, and remarkably effective techniques sit between "naive MVO" and "formal robust optimization":

- **Constraints as robustness.** Long-only, weight caps, sector bounds, and turnover limits are the practitioner's default. They are not cosmetic - they *change the geometry of the feasible set* so the optimizer can no longer express its extreme opinions. A $35\%$ cap is a hard statement that "no model output, however noisy, justifies a $500\%$ position."
- **Resampling (Michaud).** Instead of optimizing one estimated $(\hat\mu,\hat\Sigma)$, optimize *many* resampled versions, then average the resulting weights. The idea (Michaud & Michaud 1998) is that a portfolio averaged over the estimation-error distribution is less brittle than the single "optimal" point.

The practical objective is to know **what each actually buys you** - and, crucially, what it does not. This page shows, on the shared data, that constraints are the real stabilizer, while naive resampling **fails to cure a biased estimate** and can even amplify it. That negative result is the honest bridge to the formal robust formulations of [[pillars/05-portfolio-optimization/robust-optimization/03-robust-formulations|03]].

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The constrained model

The practically-used MVO is a **quadratic program** over a box (plus simplex):

$$
\max_{w}\ \hat\mu^\top w-\tfrac\delta2 w^\top\hat\Sigma w
\quad\text{s.t.}\quad \mathbf 1^\top w=1,\ \ w_{\min}\le w\le w_{\max}.
$$

With $w_{\min}=0$ it is **long-only** (no short sales); with a common $w_{\max}$ it caps concentration. This is a convex QP solved by active-set/interior-point methods - every real optimizer since Markowitz uses some version.

**Turnover constraint.** To control trading cost, add $\lVert w-w_{\text{prev}}\rVert_1\le\tau$ (an $\ell_1$ ball) - convex, and itself a robustness statement about the *path*, not just the endpoint (see [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]).

**Why constraints help (first principles).** Unconstrained MVO's optimum is $w^\star=\frac1\delta\hat\Sigma^{-1}\hat\mu$. The problem is that this point sits *outside* any sane region of portfolio space, in the short-saturated tail where estimation error dominates. Clipping the feasible set to the simplex/box removes exactly those directions. The cost is real - Clarke, de Silva & Thorley (2002) quantify it as a **transfer coefficient** $\mathrm{TC}<1$ that discounts achievable information ratio ($\mathrm{IR}\approx\mathrm{IC}\times\sqrt{\text{breadth}}\times\mathrm{TC}$) - but the benefit (survival) usually dominates.

#### 2.2 Resampling (Michaud)

Michaud's procedure:

1. Estimate $(\hat\mu,\hat\Sigma)$ from the sample.
2. Draw $B$ bootstrap samples of the return history (non-parametric resample, or parametric draws from $\mathcal N(\hat\mu,\hat\Sigma)$).
3. Optimize MVO on each; collect the $B$ weight vectors $\{w^{(b)}\}$.
4. Report the **average** $\bar w=\frac1B\sum_b w^{(b)}$ (and/or a resampled efficient frontier in which portfolios are ranked by their resampled risk/reward).

The claim is that $\bar w$ is more stable than the single $w^\star$. The subtlety - and where the method is often over-sold - is that **step 2 resamples around the same point estimate that is itself biased by the overfit**. Averaging over resamples reduces the *variance* contribution of the frontier, but it does **not** remove the bias in $\hat\mu$; if the center is wrong, all $B$ optimizations inherit the wrong center. Goldfarb & Iyengar (2003, §1) make this critique precisely: sampling-based and scenario approaches "do not provide any hard guarantees on the portfolio performance."

---

### 3. Computational Implementation - constraints vs resampling

Same universe. We compare the unconstrained optimum, the long-only box, and the Michaud average, and we measure the **dispersion** of resampled weights - the quantity resampling is supposed to tame.



Two verified, and deliberately honest, results:

- **The constraint is the workhorse.** Clipping to the long-only box collapses the $-2.26/\!+\!4.96$ short-saturated optimum to a diversified $[0.078,0.158,0.205,0.214,0.171,0.173]$ with gross exposure $1.00$. (Here the $35\%$ cap is not even binding - long-only alone already does the job on this $N=6$ universe.) The robust max-min portfolio of [[pillars/05-portfolio-optimization/robust-optimization/03-robust-formulations|03]] lands in essentially the same place: **box-uncertainty and hard caps both act as penalties on large positions.**
- **Naive resampling does not stabilize the unconstrained problem.** The Michaud average has gross exposure $13.92$ - *more* extreme than the single naive solution ($11.91$), and the per-draw gross exposure has standard deviation $5.49$, roaming around a mean of $16.45$. Resampling from a model centered on an overfit $\hat\mu$ reproduces the overfit in every draw. **This is the failure the formal robust formulation is designed to fix**, not a bug in the code.

> **The design lesson.** If you are starting from an unreliable center, resampling *propagates* the unreliability. What actually helps is (a) imposing constraints (drop the extreme feasible directions) and/or (b) shrinking the center toward something stable (shrinkage, Black–Litterman prior, or a robust worst-case set). Resampling is best used *on top of* those, to build a distribution of portfolios rather than to replace them.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Constraints are a blunt instrument with a measurable cost.** Long-only and caps improve stability but discard information - the transfer coefficient $\mathrm{TC}<1$ (Clarke, de Silva & Thorley 2002) is exactly how much of your signal the constraints "leak." Cap too tight and you have simply built $1/N$ with extra steps.
2. **Resampling is not a cure for a biased estimate.** §3 shows it; Goldfarb & Iyengar (2003) state it. Resampling reduces *frontier-sampling* variance, not *input* bias. Marketing it as a guarantee is a category error.
3. **Turnover constraints can hide regime change.** A tight $\ell_1$ turnover budget keeps you glued to a stale portfolio when the world has moved; robustness about *inputs* is not robustness about *regimes*.
4. **Cap asymmetry / hidden concentration.** Capping each asset at $0.35$ while leaving correlations free lets the *portfolio* concentrate in a single risk factor. Caps on *weights* are not caps on *risk* - the residual factor exposure must be checked separately (bridge to factor risk models).

---

### 5. Canonical Literature & Study References

- **Michaud, R. & Michaud, R.** *Efficient Asset Management*, 2nd ed., OUP, 2008 - resampling and the resampled efficient frontier.
- **Lobo, Fazel & Boyd (2007)**, *Portfolio Optimization with Linear and Fixed Transaction Costs*, Annals of OR 152:341–365 - convex cost-aware formulations.
- **Clarke, de Silva & Thorley (2002)**, *Portfolio Constraints and the Fundamental Law of Active Management*, FAJ 58(5):48–66 - the transfer coefficient quantifying the cost of constraints.
- **DeMiguel, Garlappi & Uppal (2009)**, RFS 22(5) - the sobering $1/N$ benchmark constrained portfolios must beat.
- **Goldfarb & Iyengar (2003)**, Math. of OR 28(1):1–38, §1 - explicit critique of sampling-based remedies lacking guarantees.
- **Frost & Savarino (1988)**, *For better performance: constrain portfolio weights*, JPM - the classic argument that weight constraints reduce estimation risk.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/robust-optimization/03-robust-formulations|03 · Robust Formulations]]
- Method siblings: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] (a constraint-free stabilizer) · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|HRP]] (inversion-free)
- Forward: [[pillars/05-portfolio-optimization/robust-optimization/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/05-portfolio-optimization/robust-optimization/index|Index Hub]]
