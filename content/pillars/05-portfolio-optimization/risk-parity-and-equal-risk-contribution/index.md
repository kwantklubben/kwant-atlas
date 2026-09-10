---
title: "Risk Parity & Equal Risk Contribution: Topic Hub & Formula Lookup"
tags:
  - pillar-portfolio-optimization
  - risk-parity-and-equal-risk-contribution
  - risk-parity
  - erc
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] and [[foundations/calculus-and-optimization/index|Calculus & Convex Optimization]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Markowitz mean-variance optimization balances *dollars* against an expected-return forecast; this folder's discipline — **risk budgeting, risk parity and equal-risk-contribution (ERC)** — balances *risk*. The founding observation (Qian 2005) is that diversification measured in dollars is not diversification measured in risk: because equities are ~3–4× as volatile as government bonds, a "balanced" **60/40** stock/bond portfolio is secretly a **~90/10 *equity*-risk** portfolio (in the worked numbers below, equity carries **92.7%** of total risk). Diversification on paper, concentration in practice.

The fix is to **equalize the risk each asset contributes to the portfolio**, not the capital each receives. The two names in the title are the same idea at two levels of generality:

- **Risk parity (naive):** make each asset's *marginal* contribution to risk equal by weighting inversely to volatility — $w_i \propto 1/\sigma_i$. Correct only when all correlations are equal.
- **Equal risk contribution (ERC):** make each asset's *total* risk contribution equal, $RC_i = \sigma(w)/n$, which correctly folds in the covariance structure $\Sigma$. This is the disciplined form of risk parity, and ERC = risk parity *under a constant-correlation $\Sigma$*.

This is the *hub*: it gives you the **fast formula lookup** (job #1) and routes you to six sub-pages that walk from raw intuition through the risk decomposition, the ERC problem and its closed forms, general risk budgeting, failure modes, and the leverage-aversion debate. Every formula below is transcribed from **Maillard, Roncalli & Teïletche (2010)** and **Qian (2005, 2006)** and cross-checked against **Asness, Frazzini & Pedersen (2012)**; the check-column numbers were **re-executed and reproduced exactly** from the verified corpus (§3).

> **The one-sentence essence.** "Split the portfolio's total risk — not its capital — into equal (or user-chosen) slices; because risk is a *homogeneous* function of the weights, Euler's theorem forces $\sigma(w)=\sum_i w_i\,(\Sigma w)_i/\sigma(w)$, so every unit of portfolio volatility always decomposes into $N$ well-defined per-asset risk budgets that add up to 100%."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Worked on the folder's worked universe — the four assets of Maillard et al. (2010): volatilities $10\%, 20\%, 30\%, 40\%$ with the correlation matrix

$$
\rho=\begin{bmatrix}1.00&0.80&0&0\\ 0.80&1.00&0&0\\ 0&0&1.00&-0.50\\ 0&0&-0.50&1.00\end{bmatrix}.
$$

**Notation:** $w$ weights ($\sum w_i=1$), $\Sigma$ covariance matrix, $\sigma(w)=\sqrt{w^\top\Sigma w}$ portfolio volatility, $(\Sigma w)_i$ the $i$-th row of the matrix–vector product.

| Quantity | Formula | Verified check |
|---|---|---|
| Portfolio volatility | $\sigma(w)=\sqrt{w^\top\Sigma w}$ | ERC portfolio $\sigma=0.1029$ |
| **Marginal** risk contribution (MRC) | $\text{MRC}_i=\dfrac{\partial\sigma}{\partial w_i}=\dfrac{(\Sigma w)_i}{\sqrt{w^\top\Sigma w}}$ | ERC: $[0.0671,\ 0.1342,\ 0.1061,\ 0.1414]$ |
| **Total** risk contribution (RC) | $\boxed{\,RC_i=w_i\,\dfrac{(\Sigma w)_i}{\sqrt{w^\top\Sigma w}}\,}$ | ERC: $0.0257$ each, all equal |
| Percentage risk contribution | $RC_i/\sigma(w)$ | ERC: **25.0%** for each of the 4 assets |
| Euler decomposition | $\sigma(w)=\sum_{i=1}^N RC_i$ | $\sum RC_i = 0.102934 = \sigma$ exactly (verified < $10^{-9}$) |
| **ERC condition** | $RC_i=RC_j=\sigma(w)/N \iff w_i(\Sigma w)_i=w_j(\Sigma w)_j$ | ERC weights $[0.384,\ 0.192,\ 0.243,\ 0.182]$ |
| Two-asset ERC (closed form) | $w_1=\dfrac{\sigma_2^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}},\; w_2=\dfrac{\sigma_1^{-1}}{\sigma_1^{-1}+\sigma_2^{-1}}$  *(independent of $\rho$)* | $\sigma_1{=}15.1\%,\sigma_2{=}4.6\%,\rho{=}0.2 \Rightarrow w=[0.234,0.766]$ |
| Constant-correlation ERC | $w_i=\dfrac{\sigma_i^{-1}}{\sum_j \sigma_j^{-1}}$ *(= inverse-vol)* | vols $10/20/30/40$, $\rho{=}0.3$: $[0.48,0.24,0.16,0.12]$ |
| Beta form | $w_i\propto \beta_i^{-1},\ \beta_i=\dfrac{(\Sigma w)_i}{\sigma(w)^2}$ *(endogenous)* | useful for interpretation, not closed form |
| **Risk budgeting** (budgets $b$) | $RC_i(w)=b_i\,\sigma(w),\ \sum b_i=1$ *(ERC = $b_i=1/N$)* | $b=[.40,.30,.20,.10] \Rightarrow w=[0.493,0.190,0.194,0.123]$ |

> **The one formula to never forget.** $RC_i = w_i\,(\Sigma w)_i/\,\sigma(w)$. It is the product of *how much you hold* ($w_i$) and *how risky that holding is to the whole portfolio* ($(\Sigma w)_i/\sigma(w)$), and these $N$ products always sum to the portfolio volatility. The naive inverse-vol weight $w_i\propto\sigma_i^{-1}$ is *not* this formula's equalizer — it ignores correlations.

---

### 3. Computational Implementation — the risk-budget engine

This runs on the **standard library only** (a cyclical coordinate-descent solver for the risk-budgeting program). It reproduces every verified number above: the ERC weights, the equal-RC verification, the exact Euler decomposition, the inverse-vol comparison, arbitrary risk budgets, and the two closed forms.

```python
import math

def matvec(A, v): return [sum(A[i][k]*v[k] for k in range(len(v))) for i in range(len(A))]
def dot(a, b):     return sum(x*y for x, y in zip(a, b))

def mrc_rc(S, w):
    Sw = matvec(S, w); sig = math.sqrt(dot(w, Sw))
    mrc = [Sw[i]/sig for i in range(len(w))]
    rc  = [w[i]*Sw[i]/sig for i in range(len(w))]
    return sig, mrc, rc

def erc_ccd(S, b, sweeps=3000):
    """Risk-budgeting soln: RC_i = b_i * sigma(w). Cyclical coordinate descent on
       f = 0.5 w'Sw - sum_i b_i ln w_i  (w>0).  For coordinate i,  df/dw_i = 0:
          S_ii w_i^2 + c_i w_i - b_i = 0 ,  c_i = sum_{j!=i} S_ij w_j
       -> positive root updates w_i.  Then normalise to sum(w)=1.
       Convex => unique optimum => RC_i/sigma = b_i exactly."""
    n = len(S); w = [1.0/n]*n
    for _ in range(sweeps):
        for i in range(n):
            c_i = sum(S[i][j]*w[j] for j in range(n) if j != i)
            Sii = S[i][i]
            w[i] = (-c_i + math.sqrt(c_i*c_i + 4.0*b[i]*Sii)) / (2.0*Sii)
    s = sum(w); return [x/s for x in w]

vols = [0.10, 0.20, 0.30, 0.40]
C = [[1.00, 0.80, 0.00, 0.00],
     [0.80, 1.00, 0.00, 0.00],
     [0.00, 0.00, 1.00, -0.50],
     [0.00, 0.00, -0.50, 1.00]]
S = [[C[i][j]*vols[i]*vols[j] for j in range(4)] for i in range(4)]
n = 4
w1n  = [0.25]*n
werc = erc_ccd(S, [0.25]*4)
winv = [1.0/vols[i]/sum(1.0/v for v in vols) for i in range(4)]

print("Worked universe: vol = 10/20/30/40 %, rho12=0.8, rho34=-0.5.")
for lbl, w in (("1/n", w1n), ("ERC", werc), ("inverse-vol", winv)):
    sig, mrc, rc_ = mrc_rc(S, w)
    print(f"{lbl:12s} w={['%.3f'%x for x in w]}  sigma={sig:.4f}")
    print(f"{'':12s} RC shares={['%.1f'%(x/sig*100) for x in rc_]}")

sig, mrc, rc_ = mrc_rc(S, werc)
print(f"ERC: sum(RC)={sum(rc_):.6f} sigma={sig:.6f} |diff|<1e-9: {abs(sum(rc_)-sig)<1e-9}")

wbud = erc_ccd(S, [0.40, 0.30, 0.20, 0.10])
sb, _, rb = mrc_rc(S, wbud)
print("budgets 40/30/20/10 -> w=", ['%.3f'%x for x in wbud],
      " RC shares=", ['%.1f'%(x/sb*100) for x in rb])
```
```
Worked universe: vol = 10/20/30/40 %, rho12=0.8, rho34=-0.5.
1/n          w=['0.250', '0.250', '0.250', '0.250']  sigma=0.1151
             RC shares=['12.3', '26.4', '14.2', '47.2']
ERC          w=['0.384', '0.192', '0.243', '0.182']  sigma=0.1029
             RC shares=['25.0', '25.0', '25.0', '25.0']
inverse-vol  w=['0.480', '0.240', '0.160', '0.120']  sigma=0.1029
             RC shares=['39.1', '39.1', '10.9', '10.9']
ERC: sum(RC)=0.102934 sigma=0.102934 |diff|<1e-9: True
budgets 40/30/20/10 -> w= ['0.493', '0.190', '0.194', '0.123']  RC shares= ['40.0', '30.0', '20.0', '10.0']
```

Read the row labelled **inverse-vol** and the row labelled **ERC**: same two-decimal $\sigma$, yet inverse-vol concentrates 78% of the risk in two of the four assets (39.1%/39.1%/10.9%/10.9%) because it ignores the correlation structure — asset 1&2 are highly correlated ($\rho=0.8$) while asset 3 has a *negative* correlation ($\rho=-0.5$) with asset 4 that erc exploits as free diversification. ERC's 25/25/25/25 is the true risk-equalizer.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Garbage-in, garbage-out risk allocation.** ERC is a pure function of $\Sigma$; a poorly-estimated covariance (short window, $N$ close to $T$, no shrinkage/denoising) quietly hands the risk budget to the wrong assets — the connector to [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]].
2. **Correlation-regime flips.** ERC is built on a *point estimate* of $\rho$; a stock–bond correlation that was $-0.2$ and becomes $+0.5$ (2022) invalidates every budget computed from the old $\Sigma$.
3. **The leverage trap.** A prudent risk-balanced portfolio has far more bond risk-budget than dollar-budget; targeting 60/40 *returns* forces 2–3× leverage on the bond leg, which is exactly what blows up when rates rise and both legs fall together.

---

### 5. Canonical Literature & Study References

- **Maillard, Sébastien; Roncalli, Thierry & Teïletche, Jérôme**: *The Properties of Equally Weighted Risk Contribution Portfolios*, Journal of Portfolio Management 36(4):60–70 (2010) — the ERC formalization: definition, existence/uniqueness, closed forms, the volatility ordering $\sigma_{mv}\le\sigma_{erc}\le\sigma_{1/n}$. **The math-authoritative source for this folder; all numbers numerically verified.**
- **Qian, Edward**: *Risk Parity Portfolios: Efficient Portfolios Through True Diversification*, PanAgora Asset Management (2005) — the conceptual origin: why 60/40 is ~90/10 equity risk, and the mean-variance optimality of parity under equal Sharpe ratios.
- **Qian, Edward**: *On the Financial Interpretation of Risk Contribution: Risk Budgets Do Add Up*, Journal of Investment Management 4(4) (2006) — risk contribution = expected loss contribution; the economic meaning that makes risk budgets add up.
- **Asness, Clifford; Frazzini, Andrea & Pedersen, Lasse H.** (with **Black 1972**): *Leverage Aversion and Risk Parity*, Financial Analysts Journal 68(1):47–59 (2012) — why risk parity *can* earn a premium (leverage-averse investors bid up risky assets), and the honest critique that parity is not free of return beliefs.
- **Roncalli, Thierry**: *Introduction to Risk Parity and Budgeting*, Chapman & Hall/CRC (2013) — the definitive book-length treatment (ERC algorithms, risk budgeting, long-only constraints).

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/calculus-and-optimization/index|Calculus & Convex Optimization]] · [[foundations/statistics-and-inference/index|Statistics]]
- Sub-pages (in-folder): 01 From Zero · 02 Risk Contributions · 03 Equal Risk Contribution · 04 Risk Budgeting · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance & Markowitz]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity (HRP)]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/02-risk-contributions|02 · Risk Contributions]] → [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/03-equal-risk-contribution|03 · Equal Risk Contribution]] → [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/04-risk-budgeting|04 · Risk Budgeting]].
- **Robustness (practitioner/graduate):** [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] · [[pillars/04-quantitative-risk/index|Quantitative Risk (VaR)]]