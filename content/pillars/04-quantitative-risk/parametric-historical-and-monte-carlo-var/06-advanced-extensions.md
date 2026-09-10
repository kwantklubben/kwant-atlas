---
title: "06 — Advanced Extensions: Delta–Gamma Approximations & Backtesting VaR"
tags:
  - pillar-quantitative-risk
  - parametric-historical-and-monte-carlo-var
  - delta-gamma
  - backtesting-var
  - kupiec-test
  - christoffersen-test
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/02-parametric-var|02 · Parametric]] and [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Two practical problems remain after the three VaR methods are understood:

1. **Options are nonlinear — delta-normal VaR can't price their risk.** The fix is the **delta–gamma approximation**: keep the convexity (second-order) term the delta-only method throws away. It is the middle rung between the fast-but-linear delta-normal and the exact-but-slow full revaluation.
2. **A VaR model is only a model — you must check it against reality.** The fix is **backtesting**: compare the model's predicted breach rate with what actually happened. The two canonical statistics are **Kupiec's Proportion-of-Failures (frequency)** and **Christoffersen's independence (clustering)**.

The practical objective of this page: the exact delta–gamma math, a clean demonstration of where it helps, and a runnable Kupiec + Christoffersen backtest — plus the regulatory context (Basel traffic-light zones, FRTB's shift to ES).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Delta–gamma: the quadratic approximation of the P&L

**Delta-normal (linear, Hull Ch 22 eq. 22.6).** For $N$ factors, $\Delta P\approx\sum_i S_i\delta_i\Delta x_i = \delta^T\Delta S$, $a_i=S_i\delta_i$. Suitable only when the portfolio is delta-linear in the factors.

**Delta–gamma (quadratic, Hull Ch 22 eq. 22.7/22.8; Glasserman Ch 9 eq. 9.2).** Add the curvature:
$$\Delta V \approx \frac{\partial V}{\partial t}\Delta t + \delta^T\Delta S + \tfrac12\Delta S^T\Gamma\Delta S,$$
$\delta_i=\partial V/\partial S_i$, $\Gamma_{ij}=\partial^2V/\partial S_i\partial S_j$ (the cross-gammas matter). For one factor this is the familiar
$$\Delta V\approx\Theta\Delta t + \delta\,\Delta S + \tfrac12\gamma\,(\Delta S)^2.$$

The *point*: $\gamma>0$ (long options) means the P&L bends, so a **linear** delta-normal VaR systematically misstates the risk — it ignores that the position gains/loses convexly as the move grows.

**Diagonalizing to a sum of quadratic forms (Glasserman Ch 9 §9.2).** Write $\Delta S=CZ$, $CC^T=\Sigma$, and diagonalize $-\tfrac12C^T\Gamma C=\Lambda=\text{diag}(\lambda_1,\dots,\lambda_m)$. Then the loss is a quadratic in independent normals
$$L\approx Q=a+\sum_{j=1}^{m}\big(b_jZ_j+\lambda_jZ_j^2\big),\qquad a=-\Theta\Delta t.$$
Its moment-generating function is closed form, which (i) gives a fast VaR via inversion, and (ii) is the *exact* sampling engine for importance sampling in the tail (Glasserman §9.2; Table 9.1: CV≈2–5×, IS≈7–27×, stratified-IS up to ~173× variance reduction for tail probabilities).

**Where it helps / where it doesn't.** For mild convexity (a near-ATM FX put, one day), delta-gamma reproduces full-revaluation VaR almost exactly; delta-only is off a few percent. For **delta-neutral, gamma-heavy** positions (a long straddle: $\delta\approx0$ but big $\gamma$), delta-only claims "no risk" while the realized tail risk is real — exactly the case full revaluation and delta–gamma exist to catch (see the failure mode in 05/Reference).

#### 2.2 Backtesting VaR — Kupiec POF and Christoffersen independence

**Kupiec (1995) Proportion-of-Failures (POF).** Let $x$ be breaches ($L_t>\text{VaR}_\alpha$) over $T$ days, expected rate $p=1-\alpha$ under $H_0$. The likelihood-ratio statistic
$$\text{LR}_{\text{POF}}=-2\ln\!\Big[\tfrac{(1-p)^{T-x}p^{x}}{(1-\hat p)^{T-x}\hat p^{x}}\Big]\sim\chi^2_1,\qquad \hat p=\tfrac{x}{T}.$$
Reject at 5% if $\text{LR}_{\text{POF}}>3.841$ (the $\chi^2_1$ 95% point). This only checks the *rate* — it is blind to ordering.

**Christoffersen (1998) independence.** A model can pass Kupiec yet have its breaches **clustered** (all in one crash week) — the worst failure mode there is. Build the $2\times2$ transition count matrix $\{n_{ij}\}$ of the violation sequence ($0\to0,0\to1,1\to0,1\to1$). Let $p_0=n_{01}/(n_{00}+n_{01})$, $p_1=n_{11}/(n_{10}+n_{11})$, and overall $p=(n_{01}+n_{11})/(n_{00}+n_{01}+n_{10}+n_{11})$. The independence LR
$$\text{LR}_{\text{ind}}=-2\Big[\tfrac{(n_{00}+n_{10})\log(1-p)+(n_{01}+n_{11})\log p}{-\;n_{00}\log(1-p_0)-n_{01}\log p_0-n_{10}\log(1-p_1)-n_{11}\log p_1}\Big]\sim\chi^2_1.$$
Reject at 5% if $>3.841$. Combined **(conditional) coverage = $\text{LR}_{\text{POF}}+\text{LR}_{\text{ind}}\sim\chi^2_2$** catches both wrong-rate *and* clustering.

**Regulatory reading (BCBS 1996).** Supervisors grade internal-models VaR by breaches: green (≤4 exceptions in 250) to red (≥10) with escalating capital multipliers — the frequency test mapped to a capital add-on. Modern FRTB (2019) moves market-risk capital from 99% VaR to **97.5% Expected Shortfall** for that exact reason (VaR's non-subadditivity and tail blindness) — see [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & ES]].

---

### 3. Computational Implementation — delta–gamma and the backtest, stdlib only

**A. Delta–gamma recovers full-revaluation VaR on the FX put (the canonical comparison).** Same put as [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/04-monte-carlo-var|04]]:

```python
import math, random
def N(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2*math.pi)
def put(S,K,T,r,sig):
    d1=(math.log(S/K)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return K*math.exp(-r*T)*N(-d2)-S*N(-d1)
S,K,T,r,ann=1.55,1.60,0.5,0.03,0.12
dv=ann/math.sqrt(252); V0=put(S,K,T,r,ann)
d1=(math.log(S/K)+(r+0.5*ann**2)*T)/(ann*math.sqrt(T))
delta=-N(-d1); gamma=phi(d1)/(S*ann*math.sqrt(T))

m=400000; random.seed(9); Lf,Ldg,Ldl=[],[],[]
for _ in range(m):
    dS=S*dv*random.gauss(0,1)
    Lf.append(-(put(S+dS,K,T-1/252,r,ann)-V0))          # full revaluation
    Ldg.append(-(delta*dS + 0.5*gamma*dS*dS))            # delta-gamma (drop tiny theta)
    Ldl.append(-(delta*dS))                               # delta-only
def q(L): L=sorted(L); return L[int(0.99*m)-1]
qdl, qdg, qf = q(Ldl), q(Ldg), q(Lf)
print(f"VaR_99 delta-only       = {qdl:.4f}   (linear: misses convexity)")
print(f"VaR_99 delta-gamma      = {qdg:.4f}   ({qdg/qf:.2f}x vs full)")
print(f"VaR_99 full revaluation = {qf:.4f}   (benchmark)")
```
```
VaR_99 delta-only       = 0.0153   (linear: misses convexity)
VaR_99 delta-gamma      = 0.0141   (0.99x vs full)
VaR_99 full revaluation = 0.0143   (benchmark)
```
Delta-only is ~7% off on a *mildly* convex put; delta–gamma lands within 1% of the full-revaluation benchmark. On a **delta-neutral straddle** the delta-only estimate collapses toward zero while the true VaR stays real — that gap is why delta–gamma exists and why full revaluation is the standard for options-heavy books.

**B. Backtest a 99% VaR model and watch Kupiec catch a bad one (stdlib).** A well-calibrated model produces ~10 breaches/1000 days and is accepted; an under-stated-vol model breaches 115× and is rejected by Kupiec (while — instructive — still failing *nothing* on independence, because its breaches are scattered, not clustered):

```python
import math, random
z99=2.3263478740408408
def var_seq(true_sig, model_sig, days):
    return [1 if -random.gauss(0,true_sig) > z99*model_sig else 0 for _ in range(days)]
def kupiec(v, p=0.01):
    T=len(v); x=sum(v); ph=x/T
    if x==0: lr=-2*math.log((1-p)**T)
    else:    lr=-2*(math.log(((1-p)**(T-x))*(p**x))-math.log(((1-ph)**(T-x))*(ph**x)))
    return x,lr, lr>3.841
def christ(v):
    n=len(v); n00=n01=n10=n11=0
    for k in range(1,n):
        if v[k-1]==0 and v[k]==0: n00+=1
        elif v[k-1]==0 and v[k]==1: n01+=1
        elif v[k-1]==1 and v[k]==0: n10+=1
        elif v[k-1]==1 and v[k]==1: n11+=1
    n0=n00+n01; n1=n10+n11
    p0=n01/max(n0,1); p1=n11/max(n1,1); p=(n01+n11)/max(n00+n10+n01+n11,1)
    lr=-2*((n00+n10)*math.log(1-p)+(n01+n11)*math.log(p)
           -(n00*math.log(max(1-p0,1e-15))+n01*math.log(max(p0,1e-15))
             +n10*math.log(max(1-p1,1e-15))+n11*math.log(max(p1,1e-15))))
    return lr, lr>3.841

random.seed(11)
for name,ts,ms in (("well-calibrated", 0.012, 0.012), ("understated-vol", 0.012, 0.006)):
    v=var_seq(ts,ms,1000)
    x,lr,rej=kupiec(v); lri,reji=christ(v)
    print(f"{name:16s}: {x:3d} breaches/1000  Kupiec LR={lr:6.1f} ({'REJECT' if rej else 'accept'})  "
          f"Christoffersen LR={lri:5.2f} ({'REJECT' if reji else 'accept'})")
```
```
well-calibrated :  11 breaches/1000  Kupiec LR=   0.1 (accept)  Christoffersen LR= 0.24 (accept)
understated-vol : 115 breaches/1000  Kupiec LR= 363.3 (REJECT)  Christoffersen LR= 0.76 (accept)
```
The under-stated-vol model breaches ~11× too often — **Kupiec rejects it decisively** (LR 363 ≫ 3.841). Its breaches are scattered, so the independence test (correctly) sees no clustering — the two tests are *complementary*: Kupiec is the coverage check, Christoffersen the clustering check, and together the conditional-coverage test is their sum.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Delta–gamma still ignores higher-order risk (vanna, volga, jumps) and cross-gammas if $\Gamma_{ij}$ is dropped.** The quadratic bends, but a kink (jump) or stochastic vol defeats it — the gateway to [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|stress testing]] and full MC per scenario.
2. **Backtesting has low power at high confidence.** At 99% the expected breaches are sparse; a single bad run can under/over-reject. Basel's traffic-light zones (green ≤4/250 · red ≥10/250) exist precisely because small-sample frequency tests are noisy.
3. **Kupiec alone is blind to clustering** — a serial-crash model passes on count but is the most dangerous kind. Always pair it with Christoffersen independence (the conditional-coverage test).
4. **Backtest = history; the next regime may differ.** Passing a backtest on calm history rewards underestimating the next crisis. This is why regulators pair backtesting with **stress testing** and why FRTB moved to ES at 97.5%.
5. **VaR's subadditivity failure is structural.** Backtesting a subadditive measure can *reward* desks for concentrating risk — one reason ES/CVaR is the coherent successor ([[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & ES]]).

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 9 §9.2 (delta–gamma diagonalization (9.4), MGF/inversion, importance sampling, variance-reduction table 9.1). *Math-verified in corpus.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 §22.5 (linear eq. 22.6; quadratic delta–gamma eq. 22.7/22.8; Cornish–Fisher), Ch 22 §22.8 (backtesting). *Verified in corpus.*
- **Kupiec, Paul H.**: *Techniques for Verifying the Accuracy of Risk Measurement Models*, *Journal of Derivatives* 3(2):73–84 (1995) — the POF statistic.
- **Christoffersen, Peter F.**: *Evaluating Interval Forecasts*, *International Economic Review* 39(4):841–862 (1998) — the independence/conditional-coverage test.
- **BCBS**: *Supervisory Framework for the Use of Backtesting...* (1996) — the traffic-light zones; and *Minimum Capital Requirements for Market Risk* / *FRTB* (2019) — the structural shift from VaR to 97.5% ES.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Index Hub]].
- Forward: [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall (the coherent measure / FRTB successor)]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]].
- Theory: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Delta-Hedging]] (the source of $\delta,\gamma$) · [[foundations/numerical-methods/index|Numerical Methods]].

---

*All numbers above (`3,396.15 / 3,218.55 / 3,405.97`, the Student-$t(4)$ `1.5565%`, the ghost `3,465 / 3,196`, the delta-gamma `0.0141` vs full `0.0143`, and the backtest `LR=363.3` rejection) were generated and verified with the standard library only.*