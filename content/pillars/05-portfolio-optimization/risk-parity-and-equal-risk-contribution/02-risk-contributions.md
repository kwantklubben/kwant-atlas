---
title: "02 — Risk Contributions: MRC, RC & the Euler Decomposition"
tags:
  - pillar-portfolio-optimization
  - risk-parity-and-equal-risk-contribution
  - risk-contribution
  - euler-decomposition
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Calculus (homogeneous functions, Euler's theorem)]] and [[foundations/linear-algebra-and-matrices/index|Linear algebra (quadratic forms, matrix–vector products)]].

---

### 1. Intuition & Practical Objective

Before we can *equalize* risk contributions we have to define them sharply. This page builds the exact, unambiguous decomposition of portfolio risk into per-asset pieces — the same object used by risk teams under the label **risk budgeting**. The objective is three well-defined quantities:

$$\underbrace{\text{MRC}_i}_{\text{marginal}} \xrightarrow{\times w_i} \underbrace{RC_i}_{\text{total}} \xrightarrow{\div \sigma(w)} \underbrace{RC_i/\sigma(w)}_{\text{percentage}}$$

1. **Marginal risk contribution (MRC$_i$):** if you add a *tiny* amount more of asset $i$ (say one more basis-point of weight, financed by cash), by how much does the portfolio's volatility change? This is simply the partial derivative $\partial\sigma/\partial w_i$.
2. **Total risk contribution (RC$_i$):** the slice of the portfolio's total volatility that is *attributable to* holding asset $i$ — holding $w_i$ of an asset whose marginal effect is MRC$_i$. RC$_i = w_i \times \text{MRC}_i$.
3. **Percentage contribution:** RC$_i/\sigma(w)$ — the fraction of total risk coming from asset $i$. **Crucially, these $N$ percentages always sum to 100%.** That is the "risk budgets do add up" result that Qian (2006) proved is more than a bookkeeping identity: it is (approximately) the *expected contribution to a portfolio loss*.

The practical payoff: once risk is decomposable, ETFs, pension books and hedge funds can *look inside* a portfolio and see which position is going to be responsible for the next big loss — and can then *set* the decomposition intentionally (that is risk budgeting, [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/04-risk-budgeting|04]]).

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Portfolio weights $w$ (summing to 1), covariance matrix $\Sigma$, portfolio variance $w^\top\Sigma w$ and volatility

$$\sigma(w)=\sqrt{w^\top\Sigma w}.$$

Verify the homogeneity claim first: $\sigma(\lambda w)=\sqrt{(\lambda w)^\top\Sigma(\lambda w)}=\lambda\sqrt{w^\top\Sigma w}=\lambda\,\sigma(w)$, a homogeneous function of degree 1.

**Marginal risk contribution.**

$$\text{MRC}_i=\frac{\partial\sigma}{\partial w_i}
=\frac{1}{2\sqrt{w^\top\Sigma w}}\cdot 2(\Sigma w)_i
=\frac{(\Sigma w)_i}{\sqrt{w^\top\Sigma w}}
=\frac{(\Sigma w)_i}{\sigma(w)},$$

where $(\Sigma w)_i$ is the $i$-th entry of the vector $\Sigma w$ — i.e. $\text{cov}(r_i, w^\top r)$, the covariance of asset $i$ with the whole portfolio. **This is a beautiful object:** the marginal risk of an asset is *not* its own volatility but its **covariance with the portfolio**.

**Total risk contribution & the Euler decomposition.** Euler's theorem for an $\mathbb{R}$-homogeneous-function-of-degree-1 says $\sigma(w)=\sum_i w_i\,\tfrac{\partial\sigma}{\partial w_i}$, hence

$$\boxed{\;\sigma(w)=\sum_{i=1}^N RC_i,\qquad RC_i:=w_i\,\frac{(\Sigma w)_i}{\sigma(w)}\;}$$

**Percentage contribution.** Dividing through by $\sigma(w)$ gives $1=\sum_i \tfrac{RC_i}{\sigma(w)}$. Each term $RC_i/\sigma(w)$ is the fraction of total risk from asset $i$. Two equivalent formulas for it (both useful):

$$\frac{RC_i}{\sigma(w)}=\frac{w_i(\Sigma w)_i}{\sigma(w)^2}=\frac{\text{cov}(r_i,\, w^\top r)}{\text{var}(w^\top r)},$$

which is exactly the **beta** of asset $i$ against the portfolio: the $N$ betas sum to 1, and the percentage risk contribution of asset $i$ is its portfolio-beta. This beta-reading is the cleanest way to *see* why a 60/40 stock/bond portfolio is ~90% equity risk — the equity leg's beta to the whole is ~0.9.

**What does RC actually mean? (Qian 2006).** RC is not a gratuitous decomposition. For a portfolio that suffers a loss $L$, the expected fraction of that loss attributable to asset $i$ is, under normality (Qian App. A):

$$c_i=\frac{\mathbb{E}[w_i r_i \mid w^\top r=L]}{L}=p_i+\frac{D_i}{L},\qquad D_i=w_i\mu_i-p_i\,\mu_R,\quad \mu_R=\sum_j w_j\mu_j,$$

i.e. $c_i\approx p_i$ (the risk budget) **plus a correction that vanishes** for (a) zero expected returns, (b) mean-variance-optimal portfolios, or (c) large losses $L$ relative to the sub-optimality term. In words: **the risk contribution is a good predictor of the loss contribution, and it gets better as the loss gets large** — exactly when it matters. Risk teams can therefore budget risk *before* the loss and be confident it tracks who pays after.

---

### 3. Computational Implementation — decompose a real worked universe

On Maillard et al. (2010)'s four-asset universe (vols 10/20/30/40%, $\rho_{12}=0.8$, $\rho_{34}=-0.5$), compute MRC, RC and percentage RC for the naive 1/n portfolio, and *verify the Euler decomposition sums exactly to $\sigma$*.

```python
import math
vols = [0.10, 0.20, 0.30, 0.40]
C = [[1.00, 0.80, 0.00, 0.00],
     [0.80, 1.00, 0.00, 0.00],
     [0.00, 0.00, 1.00, -0.50],
     [0.00, 0.00, -0.50, 1.00]]
S = [[C[i][j]*vols[i]*vols[j] for j in range(4)] for i in range(4)]
def decompose(w):
    Sw = [sum(S[i][k]*w[k] for k in range(4)) for i in range(4)]
    sig = math.sqrt(sum(w[i]*Sw[i] for i in range(4)))
    MRC = [Sw[i]/sig for i in range(4)]
    RC  = [w[i]*Sw[i]/sig for i in range(4)]
    return sig, MRC, RC

sig, MRC, RC = decompose([0.25, 0.25, 0.25, 0.25])   # 1/n
print(f"1/n portfolio: sigma = {sig:.4f}")
print("MRC   =", ['%.4f'%x for x in MRC])
print("RC    =", ['%.4f'%x for x in RC])
print("pct   =", ['%.1f%%'%(x/sig*100) for x in RC])
print(f"sum RC = {sum(RC):.4f}  ==  sigma  ->  Euler decomposition holds: "
      f"{abs(sum(RC)-sig)<1e-9}")
```
```
1/n portfolio: sigma = 0.1151
MRC   = ['0.0565', '0.1216', '0.0652', '0.2172']
RC    = ['0.0141', '0.0304', '0.0163', '0.0543']
pct   = ['12.3%', '26.4%', '14.2%', '47.2%']
sum RC = 0.1151  ==  sigma  ->  Euler decomposition holds: True
```

Read the **pct** line. The 1/n portfolio holds 25% of capital in every asset, yet asset 4 (the 40%-vol commodity, negatively correlated with asset 3) is responsible for **47.2%** of all risk, while asset 1 (10% vol) is only **12.3%**. Capital-equal is risk-concentrated — the exact phenomenon risk parity exists to fix. And the bottom line confirms the construction is exact: the four contributions sum to $\sigma$ to machine precision.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Risk is non-additive in *capital* but additive in *contribution*.** A common objection ("risks don't add up") conflates $w_i\sigma_i$ with $RC_i$. Standard deviation is *not* additive in weights — but RC is defined precisely so that the decomposition holds. Qian (2006) exists to defuse exactly this confusion.
2. **RC is a volatility statement, not a downside statement.** The RC decomposition uses $\sigma$; when returns are far from normal, the *small*-loss contributions are not well captured — only tails/large losses are (that is where VaR/CVaR contributions from [[pillars/04-quantitative-risk/index|Quantitative Risk]] step in, and where Qian shows Cornish–Fisher VaR contributions do better).
3. **Betas are interior, not exogenous.** Percentage RC = portfolio-beta, but that beta is a *function of $w$ itself*. You cannot read an asset's "fair" risk share off the standalone covariance matrix; the decomposition depends on the very portfolio it describes.

---

### 5. Canonical Literature & Study References

- **Qian, Edward**: *On the Financial Interpretation of Risk Contribution: Risk Budgets Do Add Up*, Journal of Investment Management 4(4) (2006) — risk contribution **as** expected contribution to loss; the beta reading; the $D_i/L$ correction that vanishes for large losses / mean-variance-optimal portfolios.
- **Maillard, Roncalli & Teïletche** (2010) — §2.1, the MRC / RC / Euler decomposition in the context of the ERC portfolio (vector form $\text{MRC}=\Sigma x/\sqrt{x^\top\Sigma x}$).
- **Hallerbach, Winfried**: *Decomposing Portfolio Value-at-Risk: A General Analysis*, Journal of Risk 5(2) (2003) — the extension of the same Euler decomposition to general *linear-homogeneous* risk measures (VaR), a precondition for any risk measure to be "budgetable."

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/01-from-zero-intuition|01 · From Zero]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/03-equal-risk-contribution|03 · Equal Risk Contribution]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/04-risk-budgeting|04 · Risk Budgeting]]
- Base: [[foundations/calculus-and-optimization/index|Calculus]], [[pillars/04-quantitative-risk/index|Quantitative Risk (VaR/CVaR)]]