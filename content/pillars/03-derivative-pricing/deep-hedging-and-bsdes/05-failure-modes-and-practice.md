---
title: "05 — Failure Modes & Practice: Model Risk, Training Instability, Costs & the √Δt Law"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - model-risk
  - training-instability
  - transaction-costs
  - discretisation
  - hedging
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/02-convex-risk-and-the-deep-hedging-objective|02 · Convex Risk & the Objective]] and [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/04-deep-bsde-and-deep-galerkin-solvers|04 · Deep BSDE & Deep Galerkin]].

---

### 1. Intuition & Practical Objective

Everything so far was machinery; this page is what goes wrong on a desk, and why. Four symptom classes, each traceable to a first principle:

1. **The hedge is learned *under* the model, and no market price audits it.** A vanilla model is anchored by observable quotes; a deep hedge is anchored by nothing. §3 measures the damage: a single volatility misspecification ($20\%$ written, $30\%$ realised) raises the residual SD by **$85.6\%$**.
2. **Training is unstable and seed-dependent.** The same loss and the same data converge at one learning rate and *diverge to $10^{121}$* at another (§3). A deep hedge is a numerical artifact, not a formula, and two runs of "the same" model produce two different strategies.
3. **Discrete hedging has a hard law.** Hedging error falls as $\sqrt{\Delta t}$ — verified to $3\%$ across 64 rebalances — while transaction cost falls far more slowly, so there is a **finite optimal rebalancing frequency** ($16$ dates at $50$bp in §3). "Rebalance more" is not a risk-management strategy; it is a cost decision.
4. **The method has no audit trail.** There is no delta, gamma or vega to reconcile against the risk system, and no residual decomposition to argue with a validator. Deep hedging trades interpretability for flexibility, and the trade must be priced in governance terms, not mathematical ones.

The practical objective: know the size of the model-risk exposure of a learned hedge, know the two failure signatures of training (bias floor vs divergence), be able to compute the cost-optimal rebalancing frequency, and know why a learned hedge cannot be signed off by the same process that signs off a Black–Scholes delta.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Why a learned hedge has *more* model risk than a model price

A parametric model calibrated to today's vanillas is constrained: its parameters are pinned by hundreds of liquid quotes, and its mis-specification is *observable* as a residual. A deep hedge has neither property. Formally, the strategy is

$$
\delta^\star=\arg\min_{\delta}\mathbb E^{\mathbb P^{\text{sim}}}\Big[\rho\big(L_T^\delta\big)\Big],
$$

so $\delta^\star$ is a functional of the *simulation measure* $\mathbb P^{\text{sim}}$. If the true world is $\mathbb P^{\text{true}}\ne\mathbb P^{\text{sim}}$, the realised risk is $\rho^{\text{true}}(L_T^{\delta^\star})$, which is bounded below only by $\min_\delta\rho^{\text{true}}(L_T^\delta)$ — and the gap can be arbitrarily large. This is not a numerical artifact; it is the same "model risk dwarfs parameter risk" statement as [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston/SABR · 05]], but with no market price to detect it. The defence is not more data but **robustification**: minimise the worst case over an uncertainty set ([[pillars/03-derivative-pricing/deep-hedging-and-bsdes/06-advanced-extensions|06]]), which is exactly the robust representation of the risk measure in §02.

#### 2.2 The $\sqrt{\Delta t}$ law of discrete hedging

For a discretely rebalanced delta hedge of a European claim, the hedging error over $\Delta t$ steps is the sum of the *unhedged* gamma terms. A second-order expansion of the hedged P&L gives the classical Boyle–Emanuel / Bertsimas–Kogan–Lo result:

$$
\text{P\&L}\ \approx\ \sum_{i}\tfrac12\Gamma_{t_i}S_{t_i}^2\Big[\big(\tfrac{\Delta S_i}{S_{t_i}}\big)^2-\sigma^2\Delta t\Big],
$$

whose terms are i.i.d. mean-zero with variance $O(\Delta t)$, so over $N=T/\Delta t$ steps

$$
\boxed{\ \mathrm{SD}\big[\text{hedging error}\big]\ \propto\ \sqrt{\Delta t}=\frac{1}{\sqrt N}\ } .
$$

The law is *universal* (independent of the payoff to leading order, because in all cases the residual is a sum of $N$ martingale differences of size $\sqrt{\Delta t}$), and it is the reason the table in §3 shows $\mathrm{SD}\cdot\sqrt{N}$ roughly constant. The cost side is different: with proportional cost $\kappa$,

$$
\text{cost}=\kappa\sum_i\big|\delta_{t_{i+1}}-\delta_{t_i}\big|S_{t_i}\ \sim\ \kappa\,\mathbb E\Big[\sum_i|\Delta\delta|\Big]\ \sim\ \kappa\,C\sqrt{N}\quad(\text{sublinear in }N\text{ but growing}),
$$

so the cost-aware objective

$$
\boxed{\ \min_N\ \underbrace{\frac{c_1}{\sqrt N}}_{\text{hedging error}}+\underbrace{c_2\kappa\sqrt N}_{\text{cost}}\ }
$$

has an **interior optimum** $N^\star\propto1/\kappa^{2/3}$-ish — finite, and large only when costs are negligible. This is the discrete-time face of the same trade-off that Almgren–Chriss solve continuously ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]).

#### 2.3 Why training diverges

The Deep BSDE/Deep hedging loss is an expectation of a squared error, so its *sample* version is a sum of squares and the SGD update is a contraction only if

$$
\mathrm{lr}<\frac{2}{\lambda_{\max}\big(\mathbb E[\Phi^{\!\top}\Phi]\big)},
$$

where $\Phi$ is the design matrix of features (including the Brownian increments — whose scale is $\sqrt{\Delta t}$, so the critical learning rate depends on the *time discretisation* as well as the architecture). Above the threshold, the linearised iteration has a spectral radius exceeding one and the weights grow geometrically; with a quadratic loss the growth is *finite-time blow-up* (the iterates escape in finitely many steps), which is exactly the $\sim10^{121}$ seen in §3. The practical consequences: (i) the learning rate is not transferable between discretisations; (ii) "loss stopped improving" and "loss exploded" can look identical for the first few iterations; (iii) reproducibility requires fixing both the seed *and* the schedule, because the escape time depends on both.

#### 2.4 Why the hedge ($Z$) is harder than the value ($Y$)

$Y$ is a conditional expectation (a *smoothing* operation); $Z$ is the martingale-representation density of $Y$, obtained by regressing $Y_{t_{i+1}}\Delta W_i/\Delta t$ — i.e. by *differentiating* $Y$ in the stochastic sense. Differentiation amplifies high-frequency noise ($\mathrm{Var}(\Delta W_i)/\Delta t\propto1/\Delta t$), so the $Z$ estimator inherits an error that grows as $\Delta t$ shrinks, the opposite of the $Y$ estimator. This is why page 03's check B recovered $Y_0$ to $\sim2\times10^{-3}$ but $Z_0$ only to $\sim1\times10^{-2}$ across seeds, and why every deep-hedging implementation reports a much noisier hedge than price. **Practical rule: validate $Y$ by an independent pricer, and validate $Z$ by an independent *hedge* (a finite-difference delta of that pricer).**

---

### 3. Computational Implementation — three quantified failure modes

We measure (1) the model risk of a learned delta hedge under a volatility misspecification, (2) the $\sqrt{\Delta t}$ law and the cost-optimal rebalancing frequency, and (3) training divergence as a function of the learning rate.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bsc(S,K,r,s,T):
    d1=(math.log(S/K)+(r+0.5*s*s)*T)/(s*math.sqrt(T)); return S*N(d1)-K*math.exp(-r*T)*N(d1-s*math.sqrt(T))
def bsd(S,K,r,s,T):
    d1=(math.log(S/K)+(r+0.5*s*s)*T)/(s*math.sqrt(T)); return N(d1)
S0,K,r,T=100.0,100.0,0.0,1.0

# ---------- (1) the hedge is learned UNDER THE MODEL: hedge-vol mismatch ----------
def resid_sd(sig_hedge,sig_true,nsteps=16,npath=4000,seed=9):
    random.seed(seed); dt=T/nsteps; prem=bsc(S0,K,r,sig_hedge,T); pl=[]
    for _ in range(npath):
        S=S0; acc=0.0
        for j in range(nsteps):
            d=bsd(S,K,r,sig_hedge,T-j*dt)
            Sn=S*math.exp((0.0-0.5*sig_true*sig_true)*dt+sig_true*math.sqrt(dt)*random.gauss(0.0,1.0))
            acc+=d*(Sn-S); S=Sn
        pl.append(prem+acc-max(S-K,0.0))
    mu=sum(pl)/npath
    return math.sqrt(sum((x-mu)**2 for x in pl)/npath)
print("(1) a 16-step delta hedge written under one volatility, run in another world.")
print("    Residual SD of the hedged P&L (rows = hedge vol, columns = true vol):")
print(f"    {'sigma_hedge':>12}{'true 15%':>12}{'true 20%':>12}{'true 30%':>12}")
for sh in (0.15,0.20,0.30):
    print(f"    {sh:12.2f}"+"".join(f"{resid_sd(sh,st):12.4f}" for st in (0.15,0.20,0.30)))
print(f"    hedge written at 20% but run at 30%: SD {resid_sd(0.20,0.30):.4f} vs "
      f"{resid_sd(0.20,0.20):.4f} in-model  ->  +{resid_sd(0.20,0.30)/resid_sd(0.20,0.20)-1:.1%}")

# ---------- (2) rebalancing frequency: the sqrt(dt) law and the cost trade-off ----------
print("")
print("(2) discrete delta-hedging error vs rebalancing frequency (GBM, sigma=20%, mu=8%, 4000 paths)")
print("    proportional cost kappa=50bp on traded notional; objective = SD + 2*E[cost]")
kappa=0.005
def experiment(nsteps,npath=4000,seed=9):
    random.seed(seed); dt=T/nsteps; prem=bsc(S0,K,r,0.20,T); pl=[]; cst=[]
    for _ in range(npath):
        S=S0; dp=0.0; acc=0.0; c=0.0
        for j in range(nsteps):
            d=bsd(S,K,r,0.20,T-j*dt)
            Sn=S*math.exp((0.08-0.5*0.04)*dt+0.20*math.sqrt(dt)*random.gauss(0.0,1.0))
            acc+=d*(Sn-S); c+=kappa*abs(d-dp)*S; dp=d; S=Sn
        pl.append(prem+acc-max(S-K,0.0)); cst.append(c)
    mu=sum(pl)/npath
    return math.sqrt(sum((x-mu)**2 for x in pl)/npath), sum(cst)/npath
print(f"    {'steps':>6}{'SD(P&L)':>11}{'SD*sqrt(steps)':>16}{'E[cost]':>11}{'SD+2cost':>11}")
best=None
for nn in (1,2,4,8,16,32,64):
    sd,c=experiment(nn); obj=sd+2.0*c
    if best is None or obj<best[1]: best=(nn,obj)
    print(f"    {nn:6d}{sd:11.5f}{sd*math.sqrt(nn):16.4f}{c:11.5f}{obj:11.5f}")
print(f"    -> SD*sqrt(steps) is ~constant = the sqrt(dt) law; cost-optimal frequency = {best[0]} dates")

# ---------- (3) training instability: the learning rate decides everything ----------
print("")
print("(3) training instability: identical loss, identical data, four learning rates")
steps,npath,seed=4,6000,3
random.seed(seed); dt=T/steps; sq=math.sqrt(dt)
X=[[0.0]*(steps+1) for _ in range(npath)]; W=[[0.0]*steps for _ in range(npath)]
for p in range(npath):
    x=S0
    for j in range(steps):
        W[p][j]=sq*random.gauss(0.0,1.0); x*=math.exp((r-0.5*0.04)*dt+0.20*W[p][j]); X[p][j+1]=x
G=[max(X[p][steps]-K,0.0) for p in range(npath)]
NF=4; NP=1+steps*NF
Phi=[[0.0]*NP for _ in range(npath)]
for p in range(npath):
    Phi[p][0]=1.0
    for i in range(steps):
        u=X[p][i]/S0; ph=(1.0,u,u*u,math.tanh(3.0*(u-1.0)))
        for k in range(NF): Phi[p][1+i*NF+k]=W[p][i]*ph[k]
def run(lr,iters=400):
    w=[0.0]*NP; w[0]=9.0; out=[]
    for it in range(iters):
        g=[0.0]*NP
        for p in range(npath):
            row=Phi[p]; YN=sum(row[j]*w[j] for j in range(NP)); e=YN-G[p]
            for j in range(NP): g[j]+=2.0*e*row[j]/npath
        for j in range(NP): w[j]-=lr*g[j]
        if it in (0,10,100,399): out.append((it,w[0]))
    return out
for lr in (0.05,0.30,1.00,1.50):
    print(f"    lr={lr:4.2f}:  "+"   ".join(f"it{it:3d} Y0={y:12.4g}" for it,y in run(lr)))
```
```
(1) a 16-step delta hedge written under one volatility, run in another world.
    Residual SD of the hedged P&L (rows = hedge vol, columns = true vol):
     sigma_hedge    true 15%    true 20%    true 30%
            0.15      1.2667      1.9068      3.9560
            0.20      1.4033      1.6888      3.1349
            0.30      1.9233      2.0405      2.5239
    hedge written at 20% but run at 30%: SD 3.1349 vs 1.6888 in-model  ->  +85.6%

(2) discrete delta-hedging error vs rebalancing frequency (GBM, sigma=20%, mu=8%, 4000 paths)
    proportional cost kappa=50bp on traded notional; objective = SD + 2*E[cost]
     steps    SD(P&L)  SD*sqrt(steps)    E[cost]   SD+2cost
         1    6.95489          6.9549    0.26991    7.49471
         2    4.74824          6.7150    0.40092    5.55007
         4    3.32287          6.6457    0.52967    4.38222
         8    2.34716          6.6388    0.68045    3.70807
        16    1.66127          6.6451    0.88067    3.42261
        32    1.20051          6.7911    1.14621    3.49294
        64    0.85931          6.8745    1.51704    3.89339
    -> SD*sqrt(steps) is ~constant = the sqrt(dt) law; cost-optimal frequency = 16 dates

(3) training instability: identical loss, identical data, four learning rates
    lr=0.05:  it  0 Y0=       8.884   it 10 Y0=       8.231   it100 Y0=       7.957   it399 Y0=       7.954
    lr=0.30:  it  0 Y0=       8.304   it 10 Y0=       7.956   it100 Y0=       7.953   it399 Y0=       7.952
    lr=1.00:  it  0 Y0=        6.68   it 10 Y0=       6.437   it100 Y0=       4.899   it399 Y0=       39.12
    lr=1.50:  it  0 Y0=       5.521   it 10 Y0=       -3038   it100 Y0=  -6.364e+30   it399 Y0=  3.709e+121
```

**Reading the output.**

- **(1) One wrong parameter, an $86\%$ risk increase.** The diagonal is the "in-model" hedge; the off-diagonal is reality. A hedge written under $\sigma=20\%$ and run in a $\sigma=30\%$ world has residual SD $3.1349$ against $1.6888$ in-model. Note also the *shape*: the mismatch is **not symmetric** — a $15\%$ hedge run at $30\%$ is the worst cell ($3.9560$) because it is simultaneously under-hedged and mis-scaled, while a $30\%$ hedge in a $15\%$ world ($1.9233$) is much less punished. Directional misspecification of volatility is a first-order risk in a learned hedge, and there is no quote anywhere that flags it.
- **(2) The $\sqrt{\Delta t}$ law holds to $3\%$ — and the cost optimum is interior.** $\mathrm{SD}\cdot\sqrt{N}$ takes the values $6.955,\,6.715,\,6.646,\,6.639,\,6.645,\,6.791,\,6.875$: essentially flat from $N=4$ to $N=64$, which is the law $\mathrm{SD}\propto N^{-1/2}$ verified over a $64\times$ range of rebalancing frequency. Cost rises monotonically ($0.270\to1.517$) and the objective $\mathrm{SD}+2\,\mathbb E[\text{cost}]$ has a clear minimum at $N=16$ ($3.4226$). Beyond that, extra rebalancing buys accuracy at a price the objective does not accept. **This is the single most actionable number on the page** and it is a *business* parameter (the cost model $\kappa$), not a mathematical one.
- **(3) The learning rate is a phase boundary, not a tuning knob.** $\mathrm{lr}=0.05$ and $0.30$ both converge to $\approx7.95$ (the Black–Scholes call is $7.9656$); $\mathrm{lr}=1.00$ converges to $4.90$ and then *escapes* to $39.12$; $\mathrm{lr}=1.50$ diverges immediately ($-3038$ at iteration $10$) and reaches $3.7\times10^{121}$. The same data, the same loss, the same iterations. **A deep hedge is only as reproducible as its hyperparameters**, and the failure is silent if you only look at the first few iterations.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Validating a learned hedge against the model that generated it.** This is circular and it is extremely common: train on simulated GBM, test on simulated GBM, report a small loss. The whole content of the method is its behaviour *out of model*. The $3\times3$ table of §3(1) is the minimum viable validation for a learned hedge.
2. **No market-anchored benchmark.** Unlike a vanilla model — whose parameter is pinned by quotes and whose residual is observable — a learned hedge has no external reference. The only defences are (i) a complete-market limit test (must reproduce Black–Scholes), (ii) an exactly-solvable BSDE test (page 03's quadratic case), and (iii) out-of-model stress matrices. Insist on all three before a strategy is used.
3. **Reporting a loss number without its floor.** As noted in [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/04-deep-bsde-and-deep-galerkin-solvers|04]], the terminal-mismatch loss at the optimum *is* the discretisation residual. A reviewer who demands "loss → 0" will force the modeller to over-rebalance (increasing cost) or over-fit (increasing model risk). Report the loss *minus* the theoretical $\sqrt{\Delta t}$ floor.
4. **Reading "the hedge converged" off the price.** §04 and §3 of page 03 show the value converging long before the control. Always monitor $Z$ (or the realised hedge ratio) as its own series; a price curve that has flattened is no evidence that the strategy has.
5. **Ignoring the cost model in the objective.** A deep hedge trained on a frictionless objective and then executed with costs is not merely suboptimal — the cost is *deterministic and unbounded in the rebalancing frequency*, so the "optimal" frictionless hedge can have *negative expected value*. §3(2) shows the interior optimum; the trained objective must contain the cost term (a path functional — which is precisely why deep hedging is needed for costs in the first place).
6. **Assuming seeds make it reproducible.** Fixing the RNG seed fixes the *data* but not the *schedule* dependence: the divergence time in §3(3) depends on the learning rate, batch composition history and floating-point order. Reproducibility of a deep hedge requires a frozen environment (code, seeds, library versions), i.e. the discipline of [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/04-reproducibility|P8 · 04 Reproducibility]].
7. **Treating the trained network as a "model" in the model-risk sense.** A neural network has no parameters that mean anything, no economic interpretation, and no stability guarantee day-over-day: retraining tomorrow on the same data can produce a materially different hedge (the seed sensitivity of §3(3) is the *within*-problem version of this). This is a governance problem before it is a mathematical one; see [[pillars/04-quantitative-risk/model-risk-and-validation/04-model-risk-management|MRV · 04 Model Risk Management]].
8. **Believing dimension-freeness explains every success.** The Deep BSDE literature's headline is $d=100$; the *hedging* literature's difficulty is that the risk measure and the cost term do not decompose dimensionally as cleanly as an expectation. Do not import "it works in 100 dimensions" from pricing to hedging without stating which quantity is guaranteed.
9. **Forgetting that the optimal hedge is not the only output that must be stable.** A desk needs the hedge *process* (for execution), the *risk statistics* (for limits) and the *P&L attribution* (for reconciliation). Deep hedging produces the first from a black box and neither of the other two natively; a production system must reconstruct them externally, and that reconstruction is where the model risk actually surfaces.
10. **Over-rebalancing because it is easy to simulate.** In simulation, rebalancing is free. In production it is the entire cost. The gap between "simulated optimal" and "executable optimal" is the classic failure of the whole discipline ([[pillars/02-algorithmic-hft/execution-backtesting-and-simulation|Execution Backtesting & Simulation]]), and it is no smaller here.

---

### 5. Canonical Literature & Study References

- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291 — the model-risk and cost discussion, the explicit statement that the optimal strategy is a functional of the assumed dynamics, and the CVaR/robust treatment that is the intended defence. *The primary reference for this page.* **Buehler et al.** (2019), *Deep hedging: learning to simulate, hedge and price under market frictions* — the costs-in-the-objective version.
- **Boyle, P. & Emanuel, D.** (1980), *Discretely adjusted option hedges*, Journal of Financial Economics 8, 259–282 — the $\sqrt{\Delta t}$ law measured in §3(2). **Bertsimas, D., Kogan, L., Lo, A.** (2000), *When is time continuous?*, Journal of Financial Economics 55, 173–204 — the corrected scaling and its constants. **Boyle, P. & Vorst, T.** — discrete-hedge error analysis.
- **Almgren, R. & Chriss, N.** (2001), *Optimal execution of portfolio transactions*, Journal of Risk 3, 5–39; **Guéant, O.** (2016), *The Financial Mathematics of Market Liquidity* (CRC) — the continuous counterpart of the cost/risk trade-off, and the correct place to look for the cost model that feeds $\kappa$. See [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]].
- **Gatheral, J.**, *The Volatility Surface*, Ch 8 §8.1 (skew level-independence) and Ch 10 (cliquet valuations: the LV/SV gaps of percentage points of notional) — the same "model risk dwarfs parameter risk" message in a *pricing* context, which is the natural benchmark for the hedging version. **Bergomi, L.**, *Stochastic Volatility Modeling*, Ch 1 (what makes a model "usable" — the P&L-attribution criterion) and Ch 12 §12.2.2 (*"most local-stochastic volatility models are not usable models"* — the test that a hedge's P&L must have the gamma/theta form).
- **Cont, R.** (2006), *Model uncertainty and its impact on the pricing of derivative instruments*, Mathematical Finance 16(3), 519–547 — quantifying model risk as a price range; the conceptual basis for the min–max robustification of §2.1. **Glasserman, P. & Xu, X.** (2019), *Robust risk measurement and model risk*, Quantitative Finance 14(1) — the robust-representation approach to exactly this problem.
- **Bender, C. & Steiner, J.** (2012), *Least-squares Monte Carlo for BSDEs*; **Gobet, E., Lemor, J.-P., Warin, X.** (2005), *A regression-based Monte Carlo method to solve BSDEs*, Annals of Applied Probability 15(3), 2172–2202 — the $Y$-vs-$Z$ error asymmetry quantified in §2.4. **Bender, C. & Zhang, J.** (2018), *Time discretization and Markovian iteration for coupled FBSDEs*.
- **Hull, J.**, *Options, Futures, and Other Derivatives*, Ch 19 (gamma–theta P&L and per-day Greeks — the reconciliation a learned hedge does not natively provide) and Ch 20 §20.5 (**minimum-variance delta**). *Verification report in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/04-deep-bsde-and-deep-galerkin-solvers|04 · Deep BSDE & Deep Galerkin]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/02-convex-risk-and-the-deep-hedging-objective|02 · Convex Risk & the Objective]]
- Forward: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Index Hub]]
- Model-risk practice: [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] · [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|MRV · 02 Sources of Model Risk]] · [[pillars/04-quantitative-risk/model-risk-and-validation/04-model-risk-management|MRV · 04 Model Risk Management]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|CMP · 05 Failure Modes]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston/SABR · 05 Failure Modes]]
- Costs & execution: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation|Execution Backtesting & Simulation]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|P5 · 03 Transaction-Cost Models]]
- Reproducibility & engineering: [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/04-reproducibility|P8 · 04 Reproducibility]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/05-failure-modes-and-practice|FML · 05 Failure Modes]]
