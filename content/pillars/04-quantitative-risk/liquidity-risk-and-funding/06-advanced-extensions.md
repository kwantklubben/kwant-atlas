---
title: "06 — Advanced Extensions: Liquidity Spirals, Systemic Risk & Liquidity-Adjusted Pricing"
tags:
  - pillar-quantitative-risk
  - liquidity-risk-and-funding
  - liquidity-spirals
  - systemic-risk
  - liquidity-adjusted-capm
  - square-root-impact
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]] and [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

The two immediate extensions of the folder are **(a)** the *endogenous* liquidity spiral — where the impact coefficient itself becomes a function of aggregate deleveraging, turning the geometric amplification into a genuine bifurcation — and **(b)** the *pricing* of liquidity as a systematic risk factor, which turns liquidity from a cost footnote into a determinant of expected returns.

> **Why these first?** The geometric amplification $1/(1-k)$ of [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04]] is the *partial-equilibrium* spiral: it takes $\kappa$ as given. Real systemic events are *general-equilibrium*: deleveraging by many agents raises $\kappa$ (liquidity begets illiquidity), so the amplification factor itself rises with the size of the unwind — the origin of **multiple equilibria, fragility, and phase transitions** (bifurcations) in liquidity. The second extension, the liquidity-adjusted CAPM of Acharya & Pedersen (2005), explains why investors demand compensation for holding assets whose liquidity *fails in bad times* — the pricing counterpart to the risk management.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The endogenous impact coefficient and the bifurcation.** In the partial-equilibrium spiral, $\kappa$ is a constant. Systemically, market depth *falls* as the crowd unwinds — an inverse relation often summarised as $D(D_{\text{agg}})$ with $\partial D/\partial(\text{aggregate selling})<0$. Writing the market-impact coefficient from a square-root impact law (Bouchaud et al. 2009),
$$\Delta p=\sigma\,Y\sqrt{\frac{Q}{V}},\qquad Y\sim\mathcal{O}(1),$$
the coefficient $Y/(V)$ is not a constant: as the stressed volume $V$ shrinks and volatility $\sigma$ rises, **impact per unit sold rises**. Substituting $k(L,\text{stress})=L\,\kappa(\text{stress})$ into $S_{\text{total}}=S_0/(1-k)$, the system crosses from a stable fixed point ($k<1$, finite liquidation) to divergence ($k\ge1$) as stress rises — a **saddle-node/tipping** structure. This is the formal content of "liquidity spirals": the economy has **complementarities** (your selling makes my selling more damaging), hence multiple equilibria and the possibility of a sudden jump between them.

**2.2 The amplification multiplier — exact.** For the geometric feedback where each round's impact causes a further sale $L\kappa\times$ the previous round,
$$S_{\text{total}}=\sum_{j\ge0}(L\kappa)^j S_0=\frac{S_0}{1-L\kappa},\qquad |L\kappa|<1,$$
with **amplification** $1/(1-k)$ and a **pole at $k=1$**. The multiplier is the clean analogue, for liquidity, of the money multiplier and the Kahn–Keynes investment multiplier: a small exogenous shock is *leveraged* by the feedback between leverage and price impact.

**2.3 Liquidity-adjusted pricing (Acharya–Pedersen 2005; Foucault Ch 9).** The gross-return premium $R\simeq r+s/h$ (Foucault eq. 9.6) prices the *level* of illiquidity. But the priced risk is the **covariance** of illiquidity with market returns. Acharya–Pedersen's liquidity-adjusted CAPM (Foucault eq. 9.18) has **four betas**:
$$\mathbb{E}(R_i)-r=\beta_1\,\lambda_{\text{mkt}}+\beta_2\,\lambda_{\text{illiq commonality}}+\beta_3\,\lambda_{\text{return–illiq hedge}}+\beta_4\,\lambda_{\text{illiq–return}},$$
where $\beta_4$ prices the asset being **liquid when the market is falling** — the deepest failure. Empirically (Foucault Ch 9) the unexplained spread is ~$1.1\%$/yr and is *dominated by $\beta_4$*: what investors pay to avoid is not illiquidity per se but illiquidity **that arrives exactly with market stress**.

**2.4 The search/OTC channel (Duffie–Gârleanu–Pedersen 2005).** For non-exchange assets, market liquidity and funding liquidity are jointly determined by a search-and-bargaining friction (Foucault Ch 9): the spread depends on dealer bargaining power $\phi$, meeting intensity $\psi$, and investor types, e.g. $S=(1+z)c/[2(r+2\psi)+(1-2\psi)\phi(1-z)]$. This is the rigorous bridge to OTC markets (corporate bonds — Bao et al. 2011; CDS) where "market liquidity" is literally a search cost.

**2.5 Systemic-risk metrics built on liquidity.** Regulators and academics convert these ideas into measures: the **Amihud illiquidity ratio** aggregated to market level; **liquidity co-movement** (Chordia–Roll–Subrahmanyam 2000; Hasbrouck–Seppi 2001); **fire-sale / deleveraging spillover** measures; and the BCBS **LCR/NSFR** plus the **margin-procyclicality** workstream (setting margin on through-the-cycle rather than point-in-time risk to damp the spiral). The unifying principle: *measure the covariance, not the level.*

---

### 3. Computational Implementation — the amplification multiplier and its pole

We compute the total forced liquidation for a range of leverage $L$ and impact feedback $\kappa$, verify it against the closed form $1/(1-L\kappa)$, and locate the divergence. Stdlib only.

```python
def amplified_sale(S0, L, kappa, tol=1e-12, itmax=100000):
    """Geometric feedback: each round's impact causes L*kappa x the previous sale."""
    S, prev, it = S0, S0, 0
    for it in range(1, itmax + 1):
        add = L * kappa * prev
        if add < tol:
            break
        S += add; prev = add
    return S, it

print("initial forced sale S0=$10M, feedback k = L*kappa:")
for L in (2.0, 5.0, 10.0):
    for kap in (0.02, 0.05, 0.10):
        S, it = amplified_sale(10.0, L, kap)
        k = L * kap
        closed = 10.0 / (1 - k) if k < 1 else float('inf')
        note = "converges" if k < 1 else "DIVERGES"
        print(f"  L={L:4.1f} kappa={kap:.2f}: k={k:.2f}  total=${S:8.2f}M  "
              f"closed-form 1/(1-k)=${closed:8.2f}M  iters={it:3d}  {note}")
```
```
initial forced sale S0=$10M, feedback k = L*kappa:
  L= 2.0 kappa=0.02: k=0.04  total=$   10.42M  closed-form 1/(1-k)=$   10.42M  iters= 10  converges
  L= 2.0 kappa=0.05: k=0.10  total=$   11.11M  closed-form 1/(1-k)=$   11.11M  iters= 14  converges
  L= 2.0 kappa=0.10: k=0.20  total=$   12.50M  closed-form 1/(1-k)=$   12.50M  iters= 19  converges
  L= 5.0 kappa=0.02: k=0.10  total=$   11.11M  closed-form 1/(1-k)=$   11.11M  iters= 14  converges
  L= 5.0 kappa=0.05: k=0.25  total=$   13.33M  closed-form 1/(1-k)=$   13.33M  iters= 22  converges
  L= 5.0 kappa=0.10: k=0.50  total=$   20.00M  closed-form 1/(1-k)=$   20.00M  iters= 44  converges
  L=10.0 kappa=0.02: k=0.20  total=$   12.50M  closed-form 1/(1-k)=$   12.50M  iters= 19  converges
  L=10.0 kappa=0.05: k=0.50  total=$   20.00M  closed-form 1/(1-k)=$   20.00M  iters= 44  converges
  L=10.0 kappa=0.10: k=1.00  total=$1000010.00M  closed-form 1/(1-k)=$     infM  iters=100000  DIVERGES
```

The simulation reproduces the closed form $S_0/(1-k)$ to the printed precision for every converging case. The message is in the last row and in the **shape**, not any single number: at $k=0.1$ the amplifier is a mild $\times1.11$; at $k=0.5$ it is $\times2$; and at $k=1$ the iteration runs without bound — **the total deleveraging required is finite only if the feedback is bounded away from 1.** Since $\kappa$ *rises* with stress in the general-equilibrium model (§2.1), a system calibrated at $k=0.5$ in normal times can cross $k=1$ in a crisis with no change to individual leverage: *the fragility is in the feedback, not in anyone's balance sheet.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Partial equilibrium mistaken for the whole.** The closed form $1/(1-k)$ assumes $\kappa$ fixed. Taking $\kappa$ constant across a stress scenario deletes the very nonlinearity (systemic amplification) the scenario exists to measure. Stress $\kappa$ and $L$ jointly.
2. **The pole is a warning, not a forecast.** Beyond $k=1$ the model produces divergence — which in reality becomes a *policy intervention* (circuit breakers, central-bank liquidity, margin holidays) or a market closure. A model that reports "infinite loss" is reporting "your assumptions have broken"; the right output is the *distance to $k=1$*, not the loss at it.
3. **Pricing model risk in the L-CAPM.** The four Acharya–Pedersen betas require estimating *time-varying, illiquid risk factors* — the hardest estimation in asset pricing. $\beta_4$ (illiquidity–return) dominates the premium but is the least stably estimated; report sensitivity (Foucault Ch 9; Pastor–Stambaugh 2003).
4. **Square-root vs linear impact model risk.** The functional form of $\kappa(Q)$ changes the multiplier's level (not its pole). Do not report a single amplification number without the impact-law caveat; the qualitative tipping survives, the quantitative claim does not (see [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]).
5. **Systemic metrics are lagging.** Liquidity co-movement and Amihud aggregates are computed from *realised* trades; they spike *after* the spiral has begun and give little warning. Early-warning work (margin-use, repo-haircut dispersion, dealer inventory) is more forward-looking but coarser.
6. **Regulatory procyclicality remains.** LCR/NSFR reduce the *probability* of a funding spiral but can *amplify* one if all banks meet them simultaneously (the buffer is a common-mode liability). Margin-procyclicality rules (through-the-cycle margin) target the same failure but trade protection for cost in normal times — a genuine, unresolved trade-off.
7. **Liquidity spirals cross the risk-type boundary.** A funding spiral is a *liquidity* event that becomes a *credit* event (counterparty default) that becomes a *market* event (fire-sale prices) — Pillar 4's risk types are not separable in a crisis, which is why integrated stress testing ([[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]) is the only honest frame.

---

### 5. Canonical Literature & Study References

- **Brunnermeier & Pedersen** (2009) — the spiral foundations extended here; **Brunnermeier** (2009) — the crisis narrative.
- **Acharya, V. & Pedersen, L.H.** — *Asset Pricing with Liquidity Risk*, *JFE* 77(2):375–410 (2005). The four-beta liquidity-adjusted CAPM. (Corpus: `61_Acharya_2005_...pdf`.)
- **Pastor, L. & Stambaugh, R.** — *Liquidity Risk and Expected Stock Returns*, *JPE* 111(3) (2003). Liquidity as a priced systematic factor. (Pillar 6 refs.)
- **Bouchaud, J.-P., Farmer, J.D. & Lillo, F.** — *How Markets Slowly Digest Changes in Supply and Demand* (2009) — square-root impact, the endogenous $\kappa$. (Pillar 6 refs.)
- **Duffie, Gârleanu & Pedersen** — *Over-the-Counter Markets*, *Econometrica* 73(6) (2005) — the search-based joint determination of market and funding liquidity (Foucault Ch 9).
- **Hasbrouck & Seppi** (2001) / **Chordia, Roll & Subrahmanyam** (2000) — liquidity commonality, the empirical basis of a *systematic* liquidity factor. **Amihud (2002)** — the aggregate illiquidity measure.
- **Bao, J., Pan, J. & Wang, J.** — *The Illiquidity of Corporate Bonds*, *JF* 66(3) (2011) — market liquidity as search cost in OTC markets. (Pillar 6 refs.)
- **BCBS** — LCR (2013, d238), NSFR (2014, d295), and the margin-procyclicality / *Principles for Sound Stress Testing* (2009) workstreams.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Index Hub]]
- In-folder: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/02-market-vs-funding-liquidity|02 · Market vs Funding Liquidity]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]]
- Systemic / stress: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]
- Portfolio / pricing: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover Constraints]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]
- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
