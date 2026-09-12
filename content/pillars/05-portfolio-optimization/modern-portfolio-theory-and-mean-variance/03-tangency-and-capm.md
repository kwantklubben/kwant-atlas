---
title: "5.1.3 Tangency Portfolio, the Capital Market Line & CAPM"
tags:
  - pillar-portfolio-optimization
  - modern-portfolio-theory-and-mean-variance
  - tangency-portfolio
  - capm
  - sharpe-ratio
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · The Efficient Frontier]].

---

### 1. Intuition & Practical Objective

Once a riskless (or low-risk) asset exists, the investor's decision splits cleanly: **how much to put in cash vs. in one "best" risky portfolio** - and that best risky portfolio is the same for everyone, independent of risk aversion (Tobin's two-fund separation). That portfolio is the **tangency portfolio** $w_{\text{tan}}$: the point where the line from the riskless rate $r_f$ just touches (is tangent to) the risky frontier. It is *by construction* the portfolio with the **maximum Sharpe ratio**
$$
\text{SR}(w)=\frac{w^T\mu-r_f}{\sqrt{w^T\Sigma w}}.
$$
The practical objective: compute $w_{\text{tan}}$, its Sharpe ratio and the **Capital Market Line** $\mu=r_f+\text{SR}_{\max}\sigma$ on which every efficient risky-plus-cash portfolio lies - and then the **CAPM/Security Market Line**, the equilibrium statement that each asset's expected excess return is proportional to its *beta* against the tangency (market) portfolio. The entire CAPM is the frontier machinery read at the tangency point.

---

### 2. Mathematical Ground Truth & Derivations

**Tangency = maximum Sharpe (Merton 1972, §IV).** Maximizing SR over the budget line $w^T\mathbf{1}=1$ gives the first-order condition with
$$
\boxed{\;w_{\text{tan}}=\frac{\Sigma^{-1}(\mu-r_f\mathbf{1})}{\mathbf{1}^T\Sigma^{-1}(\mu-r_f\mathbf{1})}\;}
$$
(Merton eq. 44), valid whenever $r_f<\mu_{\text{mv}}=A/C$ (the tangency portfolio is then efficient; if $r_f\ge A/C$ the tangency lies on the *inefficient* branch and no finite tangency exists in the equilibrium sense - Merton §IV).

**Sharpe and the CML.** Let $\mu_t=w_{\text{tan}}^T\mu$ and $\sigma_t^2=w_{\text{tan}}^T\Sigma w_{\text{tan}}$. Two identities hold exactly:
$$
\text{SR}_{\max}^2=\frac{(\mu_t-r_f)^2}{\sigma_t^2}=C r_f^2-2A r_f+B\qquad\text{and}\qquad \mu_t-r_f=\text{SR}_{\max}\,\sigma_t=\sqrt{C r_f^2-2A r_f+B}\;\sigma_t.
$$
So the **Capital Market Line** is $\mu=r_f+\text{SR}_{\max}\,\sigma$, and *every* optimal portfolio is a blend of cash and $w_{\text{tan}}$: $w=\theta w_{\text{tan}}+(1-\theta)\mathbf{0}_{\text{cash}}$, with $\theta$ determined by risk aversion. This is Tobin's separation theorem: **all investors hold the same risky fund, only the cash/risky mix differs.**

**Security Market Line / CAPM (Sharpe 1964; Merton §V, eq. 45–47).** Under the equilibrium that the market portfolio is the tangency portfolio, each asset prices according to its covariance with the market:
$$
\boxed{\;\mu_i-r_f=\beta_i\,(\mu_M-r_f),\qquad \beta_i=\frac{\sigma_{iM}}{\sigma_M^2}=\frac{\Sigma_i\cdot w_M}{\sigma_M^2}\;}
$$
i.e. CAPM is a *security market line*: expected excess return is linear in $\beta$. Crucially, this holds **identically** for the tangency portfolio given *any* $\mu,\Sigma$ - it's a mathematical identity ($(\mu-r_f\mathbf{1})=D_t\,\Sigma w_t$ collapses to $\beta_i(\mu_M-r_f)$), not an empirical fit. The empirical content lives entirely in the assumption that *observed* prices reflect this equilibrium.

---

### 3. Computational Implementation - from covariance to tangency to CAPM

Stdlib only. Everything follows from $\Sigma^{-1}(\mu-r_f\mathbf{1})$. (All results cross-checked against `numpy`; they match to machine precision.)



Read the output: the theoretical Sharpe identity $(C r_f^2-2A r_f+B)=0.085121$ reproduces the *computed* $\text{SR}^2$ exactly, and the SML identity $\mu_i-r_f=\beta_i(\mu_M-r_f)$ holds to **all shown digits** (zero difference) for every asset - the tangency portfolio is self-consistent as a "market" by construction.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tangency requires $r_f<A/C$.** If the riskless rate is at or above the min-variance return, the tangency point vanishes (Merton §IV) - the "market" portfolio isn't a finite ray, and schools that draw a tangent regardless are drawing an impossible line.
2. **Sharpe maximization inherits every input error, doubled.** $w_{\text{tan}}\propto\Sigma^{-1}(\mu-r_f\mathbf{1})$ is the *most* fragile object in the folder - it needs both $\mu$ (hard) and $\Sigma^{-1}$ (amplifying), so the tiniest estimation error in the excess returns dominates the weights. This is the "estimation-error maximizer" alert of [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]].
3. **CAPM is an identity, not a discovery.** The SML holds by algebra for the tangency portfolio; the *empirical* claim is that real markets price expectations that way (and that the true market portfolio exists and is mean-variance-efficient). Testing CAPM is testing the market portfolio's measurability, not the algebra.
4. **The riskless asset is fictional.** Real borrowing is limited, taxed, and risky; proxy rates and short constraints break the clean cash/risky separation and the linear CML.

---

### 5. References

- **Merton, Robert C.**: *An Analytic Derivation of the Efficient Portfolio Frontier*, JFQA 7(4):1851–1872 (1972)
- **Tobin, James**: *Liquidity Preference as Behavior Toward Risk*, RES 25(2):65–86 (1958)
- **Sharpe, William F.**: *Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk*, Journal of Finance 19(3):425–442 (1964)
- **Bodie, Kane & Marcus**, *Investments*

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · Efficient Frontier]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|04 · Min-Variance & Constraints]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]]
- Sibling: [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] (reverse-optimizes means so the tangency = market weights) · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]]