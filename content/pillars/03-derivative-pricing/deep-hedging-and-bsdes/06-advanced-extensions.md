---
title: "3.14.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - transaction-costs
  - leland
  - robust-hedging
  - high-dimensional
  - reinforcement-learning
  - frontier
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]].

---

### 1. Intuition & Practical Objective

Page 05 established the three hard constraints: model risk, training instability, costly rebalancing. Each has an extension, and each extension buys its fix at a price. This page is the ladder:

| failure | extension | what it buys | what it costs |
|---|---|---|---|
| proportional costs make fine rebalancing uneconomic | **Leland / asymptotic cost corrections**, cost-in-the-objective | a modified volatility / a modified driver | only valid asymptotically; a *first-order* fix |
| the hedge is learned under one model | **distributionally-robust / min–max hedging** | worst-case protection over an uncertainty set | the set is a choice; more conservative hedges |
| $d$ large, grid impossible | **Deep BSDE in high dimension** | prices and hedges at $d\sim100$ | no error bounds; harder training |
| the risk measure is dynamic and path-dependent | **risk-averse reinforcement learning** | CVaR/entropic objectives in an MDP | the classic RL instability, amplified |

The one-sentence essence:

> **Every extension of deep hedging exists to move a *friction* from the model into the objective - costs, model uncertainty, dimension, and dynamic risk preferences - and the price is always the same: a more conservative strategy whose conservatism is a *choice*, plus a harder optimisation problem with fewer guarantees.**

Three things to carry out of this page:

1. **Leland's correction is a driver modification, not a hedge trick.** Adding a transaction cost to the replication argument changes the *effective volatility* to $\sigma_L=\sigma\sqrt{1+\sqrt{2/\pi}\,\kappa/(\sigma\sqrt{\Delta t})}$ - i.e. it changes the driver of the BSDE. §3 shows it lowers cost and tail risk ($\mathrm{CVaR}_{5\%}$) but *not* variance: a fixed-scheme correction optimises a different functional than the one you may be measured on.
2. **Robustness is a min–max, hence an adversary.** The robust representation $\rho(X)=\sup_{\mathbb Q\in\mathcal Q}(\mathbb E_{\mathbb Q}[-X]-\alpha(\mathbb Q))$ of §02 means a robust hedge is trained against a worst case, and the inner supremum has to be *represented* - by a finite set of scenarios (cheap, interpretable, the §3 approach) or by an adversary network (expressive, unstable).
3. **Dimension and risk-aversion are where the method earns its keep.** Pricing in $d=100$ and hedging under CVaR are the two problems where nothing classical works; they are the reason the field exists at all.

The practical objective: be able to state and implement the Leland correction and know its limitations, build a cheap min–max robust hedge, know what "high-dimensional" actually buys and does not buy, and recognise the deep-hedging problem inside the reinforcement-learning formalism.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Transaction costs I: the modified driver

In continuous time with proportional cost $\kappa$ per unit traded notional, the self-financing condition is replaced by

$$
dY_t=\delta_t\,dS_t-\kappa\,S_t\,|d\delta_t|-\big(\text{liability accrual}\big),
$$

and $|d\delta_t|$ - the *total variation* of the strategy - is not approximable by a diffusion (it is of order $\sqrt{d\langle\delta\rangle_t}$, i.e. a local time). Two classical ways to proceed:

**(i) Leland's heuristic (1985).** Require the hedged P&L to have zero *expected* cost by widening the volatility:

$$
\boxed{\ \sigma_L^2=\sigma^2\Big(1+\sqrt{\tfrac{2}{\pi}}\,\frac{\kappa}{\sigma\sqrt{\Delta t}}\Big)\ }\qquad\text{i.e.}\qquad \delta^{\text{Leland}}_t=\frac{\partial C_{BS}}{\partial S}\Big|_{\sigma=\sigma_L}.
$$

The correction vanishes as $\Delta t\to0$ only if $\kappa\to0$; for fixed $\kappa$ the adjusted volatility *blows up* as the rebalancing interval shrinks - the mathematical statement that finer rebalancing is increasingly costly. Leland's derivation is asymptotic ($\kappa$ small, $\Delta t$ small, with $\kappa/\sqrt{\Delta t}$ fixed) and it is a *first-order* correction to *expected cost*; it is not optimal for variance or for CVaR, as §3 shows.

**(ii) The BSDE/HJB route.** The exact problem is a *nonlinear* pricing equation of the form

$$
u_t+\tfrac{\sigma^2}{2}S^2u_{SS}+\tfrac{\sigma^2S^2u_S^2\,\kappa}{\dots}=0,
$$

studied by Davis–Panas–Zariphopoulou (1993) and Whalley–Wilmott (1997), which in the BSDE language is a driver $f$ **concave in $z$**. This is the mathematically honest formulation and the one deep hedging attacks directly: put the cost term (a path functional) into the objective $\rho(L_T^\delta)$ and let the network optimise it. **The practitioner rule that falls out of both: the optimal rebalancing frequency is finite and is a function of $\kappa$ - never of machine speed.**

#### 2.2 Transaction costs II: the frequency trade-off

With discrete rebalancing at $N$ dates, §05's law $\mathrm{SD}\propto N^{-1/2}$ and the cost $\propto N^{1/2}$ combine into

$$
\min_N\ \frac{c_1}{\sqrt N}+c_2\kappa\sqrt N\ \Longrightarrow\ N^\star=\frac{c_1}{c_2\kappa}\ \ \text{(the two terms balancing)},
$$

which is the *same* structure as the Almgren–Chriss liquidation trade-off in [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]. The measured optimum in §05 at $\kappa=50$bp is $N^\star=16$ - and it is a *business* number (it depends on $\kappa$ and on the risk measure), not a numerical one.

#### 2.3 Robust (min–max) hedging

Let $\mathcal U$ be a set of candidate models (here: volatilities $\sigma\in[0.15,0.25]$). The robust hedge is

$$
\boxed{\ \delta^{\mathrm{rob}}=\arg\min_{\delta}\ \max_{\sigma\in\mathcal U}\ \rho\big(L_T^\delta(\sigma)\big)\ } .
$$

This is the *primal* problem; the **dual** is the robust representation of the risk measure over a set of measures $\mathcal Q$, and the two coincide when $\mathcal U$ and $\mathcal Q$ are appropriately paired (a minimax theorem - convexity in $\delta$, concavity/compactness in $\sigma$). Three structural facts:

- The robust hedge is **not** any single-model hedge; it is the hedge whose *worst case* is smallest. In §3 it coincides with the most extreme model's hedge - a general phenomenon when the worst case is attained at a boundary of $\mathcal U$.
- **The uncertainty set is a modelling choice with a first-order effect.** Enlarging $\mathcal U$ makes the hedge more conservative and the robust price higher - the same "price of robustness" as in [[pillars/05-portfolio-optimization/robust-optimization|Robust Optimization]].
- **Robustness is cheap when the objective is flat.** §3's worst-case SD improves only $7.5065\to7.4852$ ($0.28\%$) across a $[15\%,25\%]$ vol set: for a *one-period* variance objective the min–max hedge buys very little, because the SD is not very sensitive to $\delta$ near the optimum. The larger the uncertainty set and the more *asymmetric* the risk measure (CVaR!), the more robustness is worth paying for.

#### 2.4 High dimension, and what it does (and does not) buy

Deep BSDE's headline result is $d=100$. The mechanism: with a grid the cost of a $d$-dimensional PDE is $O(N^d)$, whereas Monte Carlo averaging is $O(n^{-1/2})$ *in any dimension* and a neural network represents $u(t,\cdot)$ with a parameter count that grows far more slowly than the grid. Formally, the loss is

$$
\mathbb E\big[(\xi-Y_T^\theta)^2\big],\qquad Y_T^\theta=Y_0^\theta-\sum_i f(t_i,Y_i^\theta,Z_i^\theta)\Delta t+\sum_i Z_i^\theta\cdot\Delta W_i,
$$

with $Z_i^\theta\in\mathbb R^{1\times d}$ now a *matrix-valued* network output (a Jacobian), so the per-step network must learn the full gradient. Two honest caveats:

- **Monte Carlo error is dimension-free in rate, not in constant.** The variance of the terminal payoff grows with $d$ (a basket call is riskier than an ATM call), so the path count needed for a fixed accuracy grows with $d$. The correct claim is "$O(n^{-1/2})$ regardless of $d$", not "equally accurate at any $d$".
- **The *hedging* problem is harder than the *pricing* problem in high dimension.** Pricing needs $Y_0$; hedging needs the whole $Z$ process (the Jacobian). The deep-hedging paper's experiments are typically in low dimension for exactly this reason - and this is an honest gap between the pricing literature and the hedging literature.

#### 2.5 Risk-averse reinforcement learning

The deep-hedging problem is a *finite-horizon Markov decision process* with a risk-sensitive objective:

$$
\text{state}=(t,S_t,\delta_{t^-}),\quad \text{action}=\delta_t,\quad \text{reward}=-\kappa|\delta_t-\delta_{t^-}|S_t,\quad \text{terminal cost}=\rho\big(\cdot\big).
$$

and one optimises $\rho$ of the *cumulative* reward. Two consequences:

- **Risk-averse RL** (CVaR-RL, entropic-RL) is the same mathematics: a Bellman recursion with a *nonlinear* (risk) aggregator, whose continuous-time limit is a BSDE with a driver given by the risk measure. **This is why BSDEs are not an alternative to RL but its continuous-time skeleton.**
- The *classical* RL pathologies apply: reward normalisation, sparse terminal signals, non-stationarity, and a train/evaluation mismatch. Deep hedging inherits all of them, plus the fact that its "environment" is a simulator the modeller wrote - i.e. the model risk of §05 is *built in*. See [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|RL · 04 Policy Gradient & Actor-Critic]].

---

### 3. Computational Implementation - Leland's correction and a min–max robust hedge

We (1) implement the Leland-adjusted delta and measure it against the plain Black–Scholes delta under a $2\%$ proportional cost, and (2) compute the min–max robust one-period delta over a volatility-uncertainty set.




**Reading the output.**

- **(1) Leland lowers *cost* and *tail risk*, not *variance* - and the trade is regime-dependent.** At $n=16$ the adjusted volatility is $22.97\%$ (from $20\%$), and the resulting hedge reduces expected cost $3.546\to3.391$ ($-4.4\%$) and $\mathrm{CVaR}_{5\%}$ $3.875\to3.558$ ($-8.2\%$), while the raw SD *rises* $1.709\to1.769$ ($+3.5\%$). Two lessons: (i) Leland's expansion is calibrated to *expected cost*, so it improves cost-control functionals and not dispersion - the objective determines whether "the fix worked"; (ii) at $n=64$ the variance penalty grows ($+30\%$), consistent with the corrected volatility growing as $1/\sqrt{\Delta t}$. **Leland is a first-order tool whose sign of benefit depends on the loss functional you are measured on.**
- **(2) The min–max hedge collapses to the most extreme model - and buys very little here.** All three single-model hedges have worst-case SD within $1\%$ of each other ($7.5563$, $7.5065$, $7.4852$), and the robust optimum is *exactly* the $25\%$ delta $0.5997$. Two honest observations: first, when the worst case is attained at a boundary of the uncertainty set, the robust hedge **is** that boundary's hedge (no averaging, no "in-between" solution); second, for a *symmetric, one-period variance* objective the price of robustness is negligible ($0.28\%$). Robustness pays when the risk measure is asymmetric (CVaR) or the uncertainty set is large - otherwise the adversarial formulation is mostly a *governance* statement, not a P&L improvement.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating Leland's $\sigma_L$ as "the" cost-adjusted model.** It is an asymptotic expansion valid for small $\kappa$ with $\kappa/\sqrt{\Delta t}$ fixed, derived for *expected cost*, and it breaks down (and becomes *worse* than plain Black–Scholes, as the $n=64$ row of §3 shows) outside its regime. The exact problem is a nonlinear HJB/BSDE with a concave driver - use it directly (deep hedging) when costs are material.
2. **Calibrating the uncertainty set $\mathcal U$ to make the robust hedge palatable.** The set *is* the conservatism. Choosing it after seeing the answer ("shrink $\mathcal U$ until the hedge looks reasonable") makes the whole robustification decorative. $\mathcal U$ belongs to risk management, exactly as $\rho$ and $\alpha$ do.
3. **Assuming the robust hedge is a hedge against everything.** It is a min–max over *the specified set*. Model risk outside $\mathcal U$ (e.g. a jump the set does not contain) is not covered, and the robust hedge can be *more* fragile than the nominal one to such a misspecification because it is tuned to a boundary.
4. **Importing "$d=100$ works" from pricing to hedging.** The high-dimensional results are for the *value*; the hedge needs the full Jacobian $Z\in\mathbb R^{1\times d}$ at every step, whose estimation is the harder and less-benchmarked problem. Do not present a pricing success as a hedging success.
5. **Ignoring that the dimension enters the *variance*, not just the architecture.** Monte-Carlo error is dimension-free in *rate*; a $d$-asset basket has a larger terminal variance, so the path count for fixed accuracy grows with $d$. Efficiency claims must be stated per unit of accuracy, not per unit of dimension.
6. **Assuming risk-averse RL is a different subject.** It is the same BSDE structure with a nonlinear (risk) aggregator in the Bellman recursion; the continuous-time limit of CVaR-RL is a BSDE with a driver determined by the risk measure. Treating them as separate literatures duplicates effort and loses the comparison/duality theory.
7. **Forgetting that RL's environment is a simulator you wrote.** All of deep hedging's model risk (page 05) is present, plus RL's own instabilities. The composite failure mode - a risk-averse agent over-optimising a mis-specified simulator - is the most expensive mistake in this space and does not appear in single-period academic experiments.
8. **Buying extensions for their asymptotics rather than their mechanism.** Leland's correction, robustness, high dimension and risk-averse RL each fix a *specific* friction. Adopting one because it is fashionable (or because it fits better) is exactly the failure mode of [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston/SABR · 06]] §4: extensions are bought to fix *dynamics/frictions*, and the price is paid in identifiability, stability and interpretability.

---

### 5. References

- **Leland, H.E.** (1985), *Option pricing and replication with transactions costs*, Journal of Finance 40(5), 1283–1301
- **Cont, R.** (2006), *Model uncertainty and its impact on the pricing of derivative instruments*, Mathematical Finance 16(3), 519–547; **Glasserman, P. & Xu, X.** (2014), *Robust risk measurement and model risk*, Quantitative Finance 14(1), 29–58; **Föllmer, H. & Schied, A.** (2004), *Stochastic Finance* (robust representation)
- **Han, J., Jentzen, A., E, W.** (2018), *Solving high-dimensional partial differential equations using deep learning*, PNAS 115(34), 8505–8510
- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291
- **Gierjatowicz, P., Sabate-Vidales, M., Šiška, D., Szpruch, Ł., Žurič, Ž.** (2020), *Robust pricing and hedging via neural SDEs*, and **Horvath, B., Muguruza, A., Tomas, M.** (2021), *Deep learning volatility*, Quantitative Finance
- **Chow, Y., Tamar, A., Mannor, S., Pavone, M.** (2015), *Risk-sensitive and robust decision-making: a CVaR optimization approach*, NeurIPS; **Tamar, A., Glassner, Y., Mannor, S.** (2015), *Optimizing the CVaR via sampling*; **Mäki, H. et al.** (2020), *Risk-averse deep hedging*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/04-deep-bsde-and-deep-galerkin-solvers|04 · Deep BSDE & Deep Galerkin]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Index Hub]]
- Costs & execution: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/06-market-making/market-impact-and-depth|Market Impact & Depth]] · [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|MM · 03 Temporary vs Permanent Impact]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|P5 · 03 Transaction-Cost Models]]
- Robustness & risk: [[pillars/05-portfolio-optimization/robust-optimization|Robust Optimization]] · [[pillars/05-portfolio-optimization/robust-optimization/03-robust-formulations|P5 · 03 Robust Formulations]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/model-risk-and-validation/06-advanced-extensions|MRV · 06 Advanced Extensions]]
- RL & frontier: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading|Reinforcement Learning for Trading]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|RL · 04 Policy Gradient & Actor-Critic]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston/SABR · 06 Advanced Extensions]] (rough vol, LSV - the model side of the same frontier)
- Verification & governance: [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/06-advanced-extensions|CMP · 06 Advanced Extensions]] · [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/04-reproducibility|P8 · 04 Reproducibility]]
