---
title: "02 — Convex Risk Measures & the Deep-Hedging Objective: Variance, CVaR, Entropic"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - convex-risk-measures
  - cvar
  - entropic-risk
  - exponential-utility
  - hedging
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/01-from-zero-intuition|01 · From Zero]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 Coherent Risk Measures]].

---

### 1. Intuition & Practical Objective

Page 01 established that an incomplete market leaves a residual. This page answers the only remaining question: **what do you do with it?** The answer is to *rank* residual distributions, and the ranking device is a convex risk measure. Three objects dominate practice, and they are not interchangeable:

| risk measure | what it penalises | where it comes from | computable? |
|---|---|---|---|
| **variance** $\mathrm{Var}$ | both tails, equally | Föllmer–Sondermann projection, Markowitz | yes — closed form (a regression) |
| **CVaR**$_\alpha$ | the worst $(1-\alpha)$ tail only | Rockafellar–Uryasev, Basel/ES regulation | yes — a convex program, but no PDE |
| **entropic** $\rho_\gamma$ | *all* moments (exponential tilting) | exponential utility, indifference pricing | yes — **a quadratic BSDE** |

The last row is the hinge of the whole folder: *one* of these preferences is analytically tractable, and it is the one that generates a backward SDE — which is why pages 03–04 exist. The one-sentence essence:

> **Convex risk measures are the preference ordering that replaces no-arbitrage in an incomplete market; the entropic measure is the unique one of the family with a closed-form *dynamic* (BSDE) representation, and the mean–variance hedge is its small-risk-aversion limit — so the entire BSDE/Deep-BSDE machinery is the "utility" special case of deep hedging, while CVaR and general convex measures remain purely numerical.**

Three things to internalise:

1. **The risk measure is the objective, not a tuning knob.** §3 shows the *same data, same payoff, same instrument set*, giving optimal hedge ratios $0.56$, $0.59$, $0.66$ under variance, CVaR$_{97.5\%}$ and entropic risk. Nothing else changed.
2. **Entropic risk *is* exponential-utility indifference pricing.** With $U(x)=-e^{-\gamma x}$ the certainty-equivalent is exactly $\rho_\gamma$; the indifference price of a liability $H$ is $\rho_\gamma(H)=\frac1\gamma\ln\mathbb E[e^{\gamma H}]$. That is the bridge to the BSDE of §03 and to every nonlinear pricing result in the literature.
3. **Convexity is what makes learning legitimate.** $\delta\mapsto L_T^\delta$ is affine and $\rho$ is convex, so the deep-hedging objective is convex in the strategy — no spurious local minima from the economics. What *is* non-convex is the *parametrisation* (a neural network), which is why the optimisation is a machine-learning problem at all.

The practical objective: be able to write down and distinguish the three risk measures, know their robust (dual) representations, know the exact entropic/indifference-pricing correspondence, and know that the choice of measure — not the optimiser — determines the hedge.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The axiomatic frame

A *convex risk measure* on a space of bounded random variables is a map $\rho:\mathcal X\to\mathbb R$ with

$$
\text{(monotone) } X\le Y\Rightarrow\rho(X)\le\rho(Y);\quad
\text{(cash-additive) } \rho(X+c)=\rho(X)+c;\quad
\text{(convex) } \rho(\lambda X+(1-\lambda)Y)\le\lambda\rho(X)+(1-\lambda)\rho(Y).
$$

Cash-additivity makes $\rho(X)$ read as "the capital that must be added to $X$ to make it acceptable", which is exactly the desk meaning: the premium. Adding sub-additivity ($\rho(X+Y)\le\rho(X)+\rho(Y)$) upgrades *convex* to *coherent* (Artzner–Delbaen–Eber–Heath 1999) — the CVaR/ES family qualifies, the entropic family does not (it is convex but not coherent; it is *not* positively homogeneous).

The universal dual object is the **robust representation**

$$
\boxed{\ \rho(X)=\sup_{\mathbb Q\in\mathcal Q}\Big(\mathbb E_{\mathbb Q}[-X]-\alpha(\mathbb Q)\Big)\ }
$$

with $\mathcal Q$ a set of probability measures and $\alpha$ a penalty function (Föllmer–Schied). This is what turns "minimise a convex risk measure" into "minimise a worst case over a family of models" — the source of the distributionally-robust hedging of [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/06-advanced-extensions|06]].

#### 2.2 The three workhorse measures

**(i) Variance (quadratic).** $\rho(X)=\mathrm{Var}(X)=\mathbb E[(X-\mathbb E X)^2]$. It is *not* monotone (it ignores the mean), so in deep hedging it is used in the mean-demeaned form $\rho(R(\delta))$ with $R=\delta\Delta S-H$ — the residual already absorbs the mean. The optimal hedge is the regression

$$
\delta^\star=\frac{\mathrm{Cov}(\Delta S,H)}{\mathrm{Var}(\Delta S)} .
$$

**(ii) CVaR (expected shortfall).** With confidence $\alpha$,

$$
\boxed{\ \mathrm{CVaR}_\alpha(X)=\inf_{t\in\mathbb R}\Big\{t+\frac{1}{1-\alpha}\mathbb E\big[(X-t)^+\big]\Big\}=\frac{1}{1-\alpha}\int_\alpha^1\mathrm{VaR}_u(X)\,du=\mathbb E\big[-X\,\big|\,-X\ge\mathrm{VaR}_\alpha\big]\ }
$$

(Rockafellar–Uryasev 2000). It is coherent, and its robust representation uses the *absolutely continuous* set

$$
\mathcal Q_{\mathrm{CVaR}}=\Big\{\mathbb Q\ll\mathbb P:\ \frac{d\mathbb Q}{d\mathbb P}\le\frac{1}{1-\alpha}\Big\},\qquad \rho(X)=\sup_{\mathbb Q\in\mathcal Q_{\mathrm{CVaR}}}\mathbb E_{\mathbb Q}[-X].
$$

For $X\sim N(0,1)$ there is a closed form: $\mathrm{CVaR}_\alpha(X)=\varphi(z_\alpha)/(1-\alpha)$ with $z_\alpha=\Phi^{-1}(\alpha)$ — the check used in §3.

**(iii) Entropic risk.** For $\gamma>0$,

$$
\boxed{\ \rho_\gamma(X)=\frac1\gamma\ln\mathbb E\big[e^{\gamma X}\big]\ }
$$

which is monotone, cash-additive and convex, with $X\sim N(m,s^2)\Rightarrow\rho_\gamma(X)=m+\tfrac{\gamma}{2}s^2$ **exactly**. Its robust representation is the "reverse" one over *all* measures,

$$
\rho_\gamma(X)=\sup_{\mathbb Q\ll\mathbb P}\Big(\mathbb E_{\mathbb Q}[-X]-\tfrac1\gamma H(\mathbb Q\|\mathbb P)\Big),\qquad H=\text{relative entropy},
$$

which is the Girsanov log-density in the diffusion case — the exact reason it produces a *BSDE with a quadratic driver* (§03).

#### 2.3 Entropic risk = exponential-utility indifference pricing

Let $U(x)=-e^{-\gamma x}$ (CARA) and consider a seller of a liability $H$. The *indifference price* $p$ is the cash making her indifferent between selling (and hedging optimally) and not:

$$
\sup_\delta\mathbb E\big[U\big(p+X_T^\delta-H\big)\big]=\sup_\delta\mathbb E\big[U\big(X_T^\delta\big)\big].
$$

In the zero-hedge / complete-market case this collapses to

$$
-e^{-\gamma p}\mathbb E\big[e^{\gamma H}\big]=-1\quad\Longrightarrow\quad
\boxed{\ p^{\mathrm{ind}}=\frac1\gamma\ln\mathbb E\big[e^{\gamma H}\big]=\rho_\gamma(H)\ } .
$$

**The indifference price *is* the entropic risk measure of the liability.** This identity is the entire justification for calling the risk-measure-minimising hedge "utility-based", and it is what makes the entropic case solvable by a BSDE rather than by brute-force learning.

#### 2.4 The mean–variance limit (the bridge back to page 01)

Expand the entropic transform in small risk aversion:

$$
\ln\mathbb E[e^{-\gamma\xi}]=-\gamma\mathbb E[\xi]+\frac{\gamma^2}{2}\mathrm{Var}(\xi)+O(\gamma^3)
\quad\Longrightarrow\quad
\boxed{\ Y_0=-\frac1\gamma\ln\mathbb E[e^{-\gamma\xi}]=\mathbb E[\xi]-\frac{\gamma}{2}\mathrm{Var}(\xi)+O(\gamma^2)\ } .
$$

So **quadratic (variance-optimal) hedging is the $\gamma\to0$ limit of the entropic/BSDE problem**. This is why the Föllmer–Sondermann projection of page 01 is not a *different* theory from the BSDE one — it is its first-order approximation, and the two agree exactly in the limit. For a Gaussian terminal it is exact: $\xi\sim N(m,s^2)\Rightarrow Y_0=m-\tfrac{\gamma}{2}s^2$ (§03 check C confirms this numerically).

#### 2.5 Transaction-cost-aware objectives

Costs enter the objective, not the model: with proportional cost $\kappa$ on traded notional, the static one-period problem becomes

$$
\min_{c,\delta}\ \mathrm{Var}\big(c+\delta\Delta S-H\big)+\underbrace{\kappa\,|\delta|\,S_0}_{\text{cost}} ,
$$

whose solution is $\delta^\star(\kappa)=\big(\mathrm{Cov}(\Delta S,H)-\tfrac{\kappa S_0}{2}\big)/\mathrm{Var}(\Delta S)$ — the hedge **shrinks** linearly in $\kappa$. Multi-period, the cost term is $\kappa\sum_i|\delta_{t_i}-\delta_{t_{i-1}}|S_{t_i}$: a *path* functional, so the objective is no longer a function of a single number and the deep-hedging formulation becomes unavoidable. §05 quantifies both effects (the optimum frequency, and Leland's asymptotic correction in §06).

---

### 3. Computational Implementation — the risk measure picks the hedge

We (a) verify the closed forms of CVaR and entropic risk on a standard-normal sample, and (b) minimise three *different* convex risk measures over the one-period hedge ratio applied to a **jump-diffusion** residual, showing that the optimal hedge is a function of the preference, not of the data.

```python
import math, random

# ---------- (a) convex risk measures: CVaR and entropic, on a N(0,1) sample ----------
random.seed(1); n=200000
z=sorted(random.gauss(0.0,1.0) for _ in range(n))
def phi_inv(a):
    lo,hi=-10.0,10.0
    for _ in range(200):
        mid=0.5*(lo+hi)
        if 0.5*(1.0+math.erf(mid/math.sqrt(2.0)))<a: lo=mid
        else: hi=mid
    return 0.5*(lo+hi)
print("(a) convex risk measures on an empirical N(0,1) sample (n=200000, seed 1)")
print(f"    {'alpha':>7}{'VaR_alpha (emp)':>17}{'CVaR_alpha (emp)':>18}{'CVaR theory':>13}")
for a in (0.90,0.95,0.975,0.99):
    k=max(1,int(round((1.0-a)*n))); var=-z[k]; cvar=-(sum(z[:k])/k); zq=phi_inv(a)
    print(f"    {a:7.3f}{var:17.6f}{cvar:18.6f}{math.exp(-0.5*zq*zq)/math.sqrt(2.0*math.pi)/(1.0-a):13.6f}")
print(f"    {'gamma':>7}{'rho_gamma(X) emp':>17}{'theory gamma/2':>17}{'MC s.e.':>11}")
for g in (0.5,1.0,2.0):
    ex=[math.exp(g*x) for x in z]
    m=sum(ex)/n
    se=math.sqrt(sum((v-m)**2 for v in ex)/(n-1))/math.sqrt(n)/m/g     # delta-method s.e. of (1/g)ln E
    print(f"    {g:7.3f}{math.log(m)/g:17.6f}{g/2.0:17.6f}{se:11.6f}")

# ---------- (b) the deep-hedging objective: the risk measure picks the hedge ----------
S0,K,T=100.0,100.0,1.0
lam,muJ=0.05,-0.20                                  # P-model: 5% chance of a -20% log jump
m=60000; random.seed(7)
S=[]
for _ in range(m):
    x=-0.5*0.04+0.20*math.sqrt(T)*random.gauss(0.0,1.0)
    if random.random()<lam: x+=muJ
    S.append(S0*math.exp(x))
H=[max(s-K,0.0) for s in S]
g=1.0
def risks(d):
    R=[d*(s-S0)-h for s,h in zip(S,H)]; mu=sum(R)/m
    var=sum((x-mu)**2 for x in R)/m
    Rs=sorted(R); k=int(round(0.025*m)); cvar=-(sum(Rs[:k])/k-mu)
    ent=math.log(sum(math.exp(-g*(x-mu)) for x in R)/m)/g
    return var,cvar,ent
print("")
print("(b) minimising three different convex risk measures over the hedge ratio delta")
print(f"    residual R(delta)=delta*dS-H, dS=S_T-100, call K=100, T=1, sigma=20% + 5% x -20% jump")
print(f"    {'delta':>7}{'Var(R-E R)':>14}{'CVaR 97.5%':>14}{'entropic g=1':>15}")
best={'v':None,'c':None,'e':None}
for i in range(0,37):
    d=0.35+0.01*i
    v,c,e=risks(d)
    for key,val in (('v',v),('c',c),('e',e)):
        if best[key] is None or val<best[key][1]: best[key]=(d,val)
    if i%4==0: print(f"    {d:7.2f}{v:14.4f}{c:14.6f}{e:15.6f}")
print("    argmin:")
print(f"      variance-optimal delta = {best['v'][0]:.2f}   (Var={best['v'][1]:.4f})")
print(f"      CVaR-optimal     delta = {best['c'][0]:.2f}   (CVaR={best['c'][1]:.6f})")
print(f"      entropic-optimal delta = {best['e'][0]:.2f}   (Ent={best['e'][1]:.6f})")
v0=risks(best['v'][0]); v1=risks(best['c'][0]); v2=risks(best['e'][0])
print(f"    delta_var -> delta_CVaR : Var {v1[0]/v0[0]-1:+.2%},  CVaR {v1[1]/v0[1]-1:+.2%}")
print(f"    delta_var -> delta_ent  : Var {v2[0]/v0[0]-1:+.2%},  CVaR {v2[1]/v0[1]-1:+.2%}")
```
```
(a) convex risk measures on an empirical N(0,1) sample (n=200000, seed 1)
      alpha  VaR_alpha (emp)  CVaR_alpha (emp)  CVaR theory
      0.900         1.282803          1.758902     1.754983
      0.950         1.650703          2.068626     2.062713
      0.975         1.967220          2.344998     2.337803
      0.990         2.330179          2.671125     2.665214
      gamma rho_gamma(X) emp   theory gamma/2    MC s.e.
      0.500         0.251084         0.250000   0.002381
      1.000         0.500649         0.500000   0.002944
      2.000         1.003365         1.000000   0.009814

(b) minimising three different convex risk measures over the hedge ratio delta
    residual R(delta)=delta*dS-H, dS=S_T-100, call K=100, T=1, sigma=20% + 5% x -20% jump
      delta    Var(R-E R)    CVaR 97.5%   entropic g=1
       0.35       54.6302     28.263200      59.174021
       0.39       48.4870     25.998192      54.334277
       0.43       43.6640     23.734196      49.496162
       0.47       40.1611     21.518612      44.660349
       0.51       37.9783     19.571909      39.827792
       0.55       37.1157     18.228646      34.999835
       0.59       37.5731     17.729016      30.178391
       0.63       39.3507     18.024562      25.371248
       0.67       42.4484     18.970338      22.591493
       0.71       46.8662     20.304047      24.832277
    argmin:
      variance-optimal delta = 0.56   (Var=37.1063)
      CVaR-optimal     delta = 0.59   (CVaR=17.729016)
      entropic-optimal delta = 0.66   (Ent=22.505148)
    delta_var -> delta_CVaR : Var +1.26%,  CVaR -1.62%
    delta_var -> delta_ent  : Var +11.98%,  CVaR +3.73%
```

**Reading the output.**

- **(a) The closed forms are reproduced.** CVaR: the empirical values $1.7589/2.0686/2.3450/2.6711$ sit $0.2$–$0.3\%$ above the exact $\varphi(z_\alpha)/(1-\alpha)=1.7550/2.0627/2.3378/2.6652$ — the residual is the *discreteness of the empirical quantile* ($k=(1-\alpha)n$ atoms in the tail), which biases the estimate slightly upward. Entropic: $0.2511/0.5006/1.0034$ against $\gamma/2=0.25/0.5/1.0$, i.e. within one or two Monte-Carlo standard errors ($0.0024$–$0.0098$). Both families are correct to sampling precision, and the standard errors are reported so that "within tolerance" is a *measured* statement, not a claim.
- **(b) The preference, not the data, chooses the hedge.** All three columns are computed from **the same 60 000 residual paths**: variance is minimised at $\delta=0.56$, CVaR$_{97.5\%}$ at $0.59$, entropic ($\gamma=1$) at $0.66$. Moving from the variance hedge to the CVaR hedge *costs* $1.26\%$ of variance and *buys* $1.62\%$ of CVaR; the entropic hedge sacrifices $12\%$ of variance. There is no "correct" answer here — there is only the stated preference, and the spread between the three answers (a $18\%$ range in the hedge ratio, $0.56\to0.66$) is the *size of the modelling decision* a desk makes when it names its risk measure.
- **The jump does the work.** With a symmetric residual all three measures would coincide at the same $\delta$ (the residual is a linear function of $\delta$, and for a symmetric payoff the optima nearly agree). The downward $5\%$ jump makes the loss distribution *skewed*, and it is exactly the asymmetric measures (CVaR, entropic) that then demand a *larger* hedge. This is the same leverage/skew mechanism as [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr|stochastic volatility]], now applied to the *hedge* rather than the price.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Choosing the risk measure to make the hedge cheap.** Because the objective *is* the preference, a desk can loosen $\alpha$ (CVaR) or lower $\gamma$ (entropic) until the "optimal" hedge is the one it wanted. The mitigation is governance, not mathematics: the risk measure belongs to the risk function, not the trading desk. Compare [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]].
2. **Using variance as if it were a risk measure.** Variance is not monotone: adding a deterministic loss leaves it unchanged, and it penalises upside and downside identically. For a *short* option book, upside and downside are not symmetric and variance systematically under-hedges the left tail. It survives in practice only as the small-risk-aversion limit (§2.4) and because it has a closed form.
3. **Confusing CVaR's two definitions.** $\mathbb E[-X\mid -X\ge\mathrm{VaR}_\alpha]$ and $\inf_t\{t+\frac{1}{1-\alpha}\mathbb E[(X-t)^+]\}$ agree for continuous distributions but **differ for atoms**. Simulated P&Ls are *always* discrete, so the two estimators differ at the $O(1/n)$ level. State which one you implement (the infimum form is the convex program used in learning; the conditional-mean form is the reporting number). Here §3 reports the conditional-mean form after demeaning.
4. **Forgetting that cash-additivity requires the premium to be exogenous.** If $p$ is optimised jointly with $\delta$ under a non-mean-centred $\rho$ (e.g. raw CVaR), the objective is unbounded below in $p$ and the "optimum" is $-\infty$. The standard fix — used in §3 — is to *demean the residual*, i.e. optimise the shape of the risk and let cash handle the level.
5. **Reading the entropic $\gamma$ as a market parameter.** $\gamma$ is a *preference* (risk aversion), not a calibrated quantity, and it cannot be inferred from option prices. Calibrating $\gamma$ to make deep hedging reproduce a market price is circular: it fits the preference to a quantity that does not observe it.
6. **Assuming the robust representation is innocent.** $\rho(X)=\sup_{\mathbb Q\in\mathcal Q}(\mathbb E_{\mathbb Q}[-X]-\alpha(\mathbb Q))$ turns a risk-measure minimisation into a *min–max* problem, and the inner adversary has to be represented too (a second network, or an explicit finite set of measures as in §06). Deep hedging with CVaR is therefore an *adversarial* learning problem, with all the stability issues that implies ([[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading|RL for Trading]]).
7. **Treating transaction costs as a "small adjustment".** In the one-period problem the shift is $O(\kappa S_0/\mathrm{Var}(\Delta S))$ (tiny for small $\kappa$), which is why a single-period cost adjustment looks negligible. Multi-period, the cost is summed over the *path* and dominates the $\sqrt{\Delta t}$ gain from finer rebalancing (§05, §06). Never import the one-period intuition into the multi-period problem.
8. **Ignoring that the objective is $L^2$-convex but the *parametrisation* is not.** Convexity of the economics guarantees a unique optimum *in strategy space*; it says nothing about the loss surface in *weight space* once the strategy is a neural network. Multiple weight configurations represent (nearly) the same strategy and can have very different apparent loss (§05, training instability).

---

### 5. Canonical Literature & Study References

- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291 — the convex-risk objective, the explicit treatment of the *entropic* case via a **quadratic BSDE**, the robust/CVaR set-up, and the neural-network parametrisation of the strategy. *The primary source.*
- **Artzner, P., Delbaen, F., Eber, J.-M., Heath, D.** (1999), *Coherent measures of risk*, Mathematical Finance 9(3), 203–228 — the axioms. **Föllmer, H. & Schied, A.** (2004), *Stochastic Finance: An Introduction in Discrete Time* (de Gruyter) — convex risk measures and the robust representation $\rho(X)=\sup_{\mathbb Q}(\mathbb E_{\mathbb Q}[-X]-\alpha(\mathbb Q))$. **Frittelli, M. & Rosazza Gianin, E.** (2002), *Putting order in risk measures* — convex, not necessarily coherent.
- **Rockafellar, R.T. & Uryasev, S.** (2000), *Optimization of conditional value-at-risk*, Journal of Risk 2, 21–41 — the $\inf_t\{t+\frac{1}{1-\alpha}\mathbb E[(X-t)^+]\}$ form. **Acerbi, C. & Tasche, D.** (2002), *On the coherence of expected shortfall* — the conditional-mean form and its estimation.
- **Föllmer, H. & Sondermann, D.** (1986), *Hedging of non-redundant contingent claims*; **Schweizer, M.** (2001), *A guided tour through quadratic hedging approaches* — the variance/quadratic branch and its $L^2$ projection. **Föllmer, H. & Leukert, P.** (2000), *Efficient hedging: cost versus shortfall risk*, Finance & Stochastics 4, 117–146 — shortfall-risk objectives, the ancestor of the CVaR objective here.
- **Musiela, M. & Zariphopoulou, T.** (2004), *A valuation algorithm for indifference prices in incomplete markets*, Finance & Stochastics 8, 399–414 — indifference pricing with exponential utility and the entropic correspondence $p^{\mathrm{ind}}=\frac1\gamma\ln\mathbb E[e^{\gamma H}]$. **Henderson, V. & Hobson, D.** (2004), *Utility indifference pricing — an overview*. **Davis, M.** (1997), *Option pricing in incomplete markets*.
- **Almgren, R. & Chriss, N.** (2001), *Optimal execution of portfolio transactions*, Journal of Risk 3, 5–39 — the cost/risk trade-off that underlies the multi-period cost objective (see [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]). **Bouchard, B., Moreau, L., Soner, H.M.** (2018), *On the pricing of explicit transaction costs* and **Guéant, O.** (2016), *The Financial Mathematics of Market Liquidity* — transaction-cost pricing.
- **Hull, J.**, *Options, Futures, and Other Derivatives*, Ch 20 §20.5 (**minimum-variance delta**, the practitioner's face of the quadratic hedge) and Ch 22–23 (VaR/ES and the risk side). *Verification report in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 Coherent Risk Measures]]
- Forward: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]] (why entropic risk is a quadratic BSDE) · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Index Hub]]
- Risk measures in the risk pillar: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|VaR/ES · 04 Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|VaR/ES · 05 Failure Modes]]
- Cost side: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs|Constraints & Transaction Costs]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|P5 · 03 Transaction-Cost Models]] · [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|MM · 03 Temporary vs Permanent Impact]]
- Utility/hedging classics: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|VS · 05 Failure Modes]]
- Robustness: [[pillars/05-portfolio-optimization/robust-optimization|Robust Optimization]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]]
