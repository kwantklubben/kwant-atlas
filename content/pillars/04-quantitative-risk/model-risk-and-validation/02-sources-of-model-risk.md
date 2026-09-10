---
title: "02 — Sources of Model Risk: Derman's Taxonomy & the Error Budget"
tags:
  - pillar-quantitative-risk
  - model-risk-and-validation
  - model-risk
  - taxonomies
  - error-budget
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/model-risk-and-validation/01-from-zero-intuition|01 · Model Risk from Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|The European Pricing Formulas]] (the Greeks used as error sensitivities).

---

### 1. Intuition & Practical Objective

Model risk is not one thing that "goes wrong"; it is a **set of independent failure channels**, each with a different owner, a different detection method, and a different fix. This page names them precisely and turns them into an **error budget**: a quantitative decomposition of the gap between a model's output and the truth, in which each channel contributes a dollar amount.

Two canonical taxonomies anchor the field, and they are complementary:

- **SR 11-7 (regulatory, two causes).** Model risk arises because (1) a model may have **fundamental errors** — it produces inaccurate outputs relative to its design objective; or (2) a model may be **misused** — applied outside its assumptions, or with a misunderstanding of its limitations.
- **Derman (1996, seven types).** A finer practitioner taxonomy that separates, crucially, *being wrong about the world* from *being right about the model and wrong about the arithmetic*. Derman's warning: *"you're worse off thinking you have a model and relying on it than in simply realizing there isn't one."*

The objective: given a live model, fill in the budget $\Delta V=\Delta_{\text{form}}+\Delta_{\text{param}}+\Delta_{\text{impl}}+\Delta_{\text{use}}$ with actual numbers, so "model risk" becomes a number with a sign and an owner rather than a worry.

---

### 2. Mathematical Ground Truth & Derivations

**The two taxonomies, mapped.** Each SR-11-7 cause expands into Derman's types, and each type maps to one term of the error budget.

| Derman (1996) type | SR-11-7 cause | Error-budget channel | Primary detection |
|---|---|---|---|
| Inapplicability of modeling | fundamental error | *form* (unbounded) | conceptual soundness — is the phenomenon model-able at all? |
| Incorrect model (wrong factors / dynamics / dependence / deterministic-vs-stochastic split) | fundamental error | *form* | conceptual soundness + benchmark comparison |
| Unstable data | fundamental error | *parameter* | calibration-window sensitivity, orthogonal data |
| Correct model, incorrect solution | fundamental error | *implementation* | analytic vs numerical test on a solvable case |
| Badly approximated solution | fundamental error | *implementation* | convergence study (grid/time-step refinement) |
| Software and hardware bugs | fundamental error | *implementation* | independent re-implementation, boundary tests |
| Correct model, inappropriate use | misuse | *use* | usage inventory, limits, "effective challenge" |

**The budget, first order.** Let $V_\theta$ be the model value and $\theta=(\sigma,r,q,\dots)$ its calibrated parameters. A first-order (delta/gamma) expansion gives
$$\Delta V=\underbrace{\big(V_{\theta^\star}-V^\star\big)}_{\text{form}}-\underbrace{\sum_i \frac{\partial V}{\partial\theta_i}\,\Delta\theta_i}_{\text{parameter}}\;+\;\underbrace{\mathcal{O}\big(\|\Delta\theta\|^2\big)}_{\text{convexity}}+\underbrace{\varepsilon_{\text{impl}}}_{\text{implementation}},$$
where $\Delta\theta_i$ is the *calibration error* in parameter $i$ and $\varepsilon_{\text{impl}}$ the discretisation/bug term. The parameter channel is dominated by the **Greeks**: $\Delta_{\text{param}}V\approx\sum_i G_i\,\Delta\theta_i$ with $G_i=\partial V/\partial\theta_i$ (e.g. vega for $\sigma$, rho for $r$).

**Adding channels.** If the channels are approximately independent, the total model-risk standard deviation adds in **quadrature**:
$$\sigma_{\text{total}}=\sqrt{\sigma_{\text{form}}^2+\sigma_{\text{param}}^2+\sigma_{\text{impl}}^2+\sigma_{\text{use}}^2}.$$
Two consequences worth stating: (i) a channel you have **not measured is not zero** — the budget is a *lower* bound on ignorance; (ii) the largest channel dominates the sum, so effort belongs on the biggest term, not on the smallest "bug".

**Error sensitivity as a scale.** The parameter channel scales **linearly** in the calibration error (vega × 1 vol-point), while form error is a *model-level* jump that no amount of calibration removes. Empirically, for a vanilla option the ordering is often form > parameter > implementation — which is why "we recalibrated daily" answers the wrong question.

---

### 3. Computational Implementation — building the error budget

Take an at-the-money 1-year call, $S=X=100$, $r=5\%$, $\sigma=20\%$. We price the *same* contract under five lenses: the analytic BSM value; a $\pm1$ vol-point parameter error (vega); a $\pm1$bp rate error (rho); a 50-step CRR tree (discretisation); a 360-vs-365 day-count bug; and a Merton jump-diffusion model (form error). Stdlib only.

```python
import math, random
def N(x):   return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)

def bsm_call(S,X,T,r,sig):
    d1=(math.log(S/X)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*N(d1)-X*math.exp(-r*T)*N(d2)
def bsm_put(S,X,T,r,sig):
    d1=(math.log(S/X)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return X*math.exp(-r*T)*N(-d2)-S*N(-d1)
def vega(S,X,T,r,sig):
    d1=(math.log(S/X)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); return S*phi(d1)*math.sqrt(T)
def rho_c(S,X,T,r,sig):
    d1=(math.log(S/X)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return T*X*math.exp(-r*T)*N(d2)
def crr_put(S,X,T,r,sig,n):
    dt=T/n; u=math.exp(sig*math.sqrt(dt)); d=1/u; p=(math.exp(r*dt)-d)/(u-d)
    val=[max(X-S*u**(n-i)*d**i,0.0) for i in range(n+1)]
    for j in range(n-1,-1,-1):
        val=[math.exp(-r*dt)*(p*val[i]+(1-p)*val[i+1]) for i in range(j+1)]
    return val[0]
def merton_call(S,X,T,r,sig,lam,mJ,sJ,n=300000,seed=7):
    random.seed(seed)
    driftJD=(r-lam*(math.exp(mJ+0.5*sJ*sJ)-1.0)-sig*sig/2)*T; sdt=sig*math.sqrt(T); tot=0.0
    for _ in range(n):
        z=random.gauss(0,1); L=math.exp(-lam*T); prod=random.random(); kk=0
        while prod>L: kk+=1; prod*=random.random()
        js=sum(random.gauss(mJ,sJ) for _ in range(kk))
        tot+=max(S*math.exp(driftJD+sdt*z+js)-X,0.0)
    return math.exp(-r*T)*tot/n

S,X,T,r,sig = 100.,100.,1.,0.05,0.20
c0 = bsm_call(S,X,T,r,sig)
e_vol  = vega(S,X,T,r,sig)*0.01                      # parameter: 1 vol point
e_rate = rho_c(S,X,T,r,sig)*0.0001                   # parameter: 1 bp
e_disc = abs(crr_put(S,X,T,r,sig,50)-bsm_put(S,X,T,r,sig))   # implementation: discretisation
e_day  = abs(bsm_call(S,X,T*365/360,r,sig)-c0)       # implementation: day-count bug
e_form = abs(merton_call(S,X,T,r,sig,0.5,-0.05,0.10)-c0)     # model form: jumps
total  = math.sqrt(e_vol**2+e_rate**2+e_disc**2+e_day**2+e_form**2)

print(f"base call = {c0:.4f} ; vega = {vega(S,X,T,r,sig):.4f} ; rho = {rho_c(S,X,T,r,sig):.4f}")
for nm,e in [("parameter:vol-1pt",e_vol),("parameter:rate-1bp",e_rate),
             ("implementation:discretisation",e_disc),("implementation:day-count-360",e_day),
             ("model-form:jump-diffusion",e_form)]:
    print(f"  {nm:32s} {e:.5f}  ({100*e/c0:.3f}% of price)")
print(f"  QUADRATURE TOTAL                 {total:.4f}  ({100*total/c0:.3f}% of price)")
```
```
base call = 10.4506 ; vega = 37.5240 ; rho = 53.2325
  parameter:vol-1pt                0.37524  (3.591% of price)
  parameter:rate-1bp               0.00532  (0.051% of price)
  implementation:discretisation    0.03989  (0.382% of price)
  implementation:day-count-360     0.08888  (0.851% of price)
  model-form:jump-diffusion        0.52719  (5.045% of price)
  QUADRATURE TOTAL                 0.6544  (6.262% of price)
```

Reading the budget: the 1-vol-point calibration error alone moves the price by $3.59\%$ — larger than the day-count bug ($0.85\%$) and the discretisation error ($0.38\%$) *combined*. The jump-diffusion form error ($5.05\%$) dominates all parameter channels. The quadrature total is $6.26\%$ of price. Note the vega number $37.524$ is exactly the raw vega from the Pillar-3 Greek table — the budget is built from quantities you already compute.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Calibrating to the wrong observable.** Fitting $\sigma$ to a price that was itself produced by a different model makes $\Delta\theta$ absorb (and hide) the form error — the parameter channel looks small because it is doing the form channel's job. This is the "unstable data" channel in disguise.
2. **The budget's missing terms.** Derman's "inapplicability" and SR-11-7's "misuse" have **no Greek** — they cannot be measured by perturbation. Omitted *the most dangerous* channels from your quadrature sum, and the total is a floor, not an estimate.
3. **Correlated channels.** Quadrature assumes independence; calibration error and form error are often positively correlated (a bad model needs a distorted $\sigma$ to fit the smile). The independent sum then *understates* total error.
4. **Convergence theatre.** A discretisation study that refines a grid while the *form* is wrong certifies the wrong number to more decimals — "correct model, incorrect solution" read backwards.
5. **Day-count and convention bugs are model risk.** Derman's point: the most avoidable large errors hide in the simple part (counting coupons, day-count, settlement dates) while attention sits on the exotic part.

---

### 5. Canonical Literature & Study References

- **Derman, E.**, *Model Risk*, Goldman Sachs QSR Notes (1996) — the seven types ("WHAT ARE MODELS?", "THE TYPES OF MODEL RISK", "AVOIDING MODEL RISK"). *Read in full from the corpus PDF (44_Derman_1996_model_risk.pdf).*
- **Federal Reserve / OCC**, *SR 11-7* (2011) — the two causes of model risk and "Accounting for model uncertainty". *Read in full from the corpus PDF.*
- **Morini, M.**, *Understanding and Managing Model Risk* (2011), Ch 1–3 — the quantitative treatment of model-parameter pricing and model-risk premia.
- **Hull, J. C.**, *Options, Futures, and Other Derivatives*, Ch 15 — the Greeks used as error sensitivities. *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/model-risk-and-validation/01-from-zero-intuition|01 · Model Risk from Zero]]
- Forward: [[pillars/04-quantitative-risk/model-risk-and-validation/03-validation-and-backtesting|03 · Validation & Backtesting]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|European Pricing Formulas]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Greeks & Hedging]]
