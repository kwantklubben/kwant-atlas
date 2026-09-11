---
title: "4.4.6 Advanced Extensions"
tags:
  - pillar-quantitative-risk
  - credit-risk-and-the-merton-model
  - vasicek
  - portfolio-credit-risk
  - credit-ratings
  - transition-matrix
  - gaussian-copula
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/02-the-merton-structural-model|02 · Structural Model]] and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Every single-name model answers *"will this firm default?"* The question that actually matters for a bank or a fund is *"how much do we lose when several default together?"* — a **joint** question. This page is the launchpad from one obligor to a **portfolio**:

1. **The one-factor (Vasicek) model** — put every firm's asset return on a single common "state of the economy" load plus an idiosyncratic shock. It yields the *asymptotic loss distribution* in closed form, and it is the model behind the Basel IRB capital formula.
2. **The Gaussian copula** — the same dependence structure expressed as a copula over default times; the market's standard model for CDOs and basket CDS.
3. **Ratings & transition matrices** — the industry's discrete, non-market alternative (CreditMetrics): a firm migrates between rating states, and PD is read off the default column.

> **The unifying idea.** Portfolio credit risk is *entirely* a correlation problem. With $\rho=0$ a large portfolio is nearly default-free (diversification); with $\rho=1$ it is one giant obligor. Both the Vasicek closed form and the Basel capital formula are statements about that single number $\rho$.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The one-factor Gaussian model (Vašíček 1987/1991; Hull eq. 24.10)

Let obligor $i$'s standardised asset return decompose as
$$
X_i=\sqrt\rho\,Y+\sqrt{1-\rho}\,Z_i,\qquad Y,Z_i\overset{i.i.d.}{\sim}N(0,1),
$$
where $Y$ is the common systematic factor and $Z_i$ the idiosyncratic shock. Obligor $i$ defaults if $X_i<N^{-1}(p_i)$ (its default threshold). **Conditional on the factor $Y=x$**, defaults are independent with
$$
p_i(x)=N\!\Big(\frac{N^{-1}(p_i)-\sqrt\rho\,x}{\sqrt{1-\rho}}\Big).
$$

For a **large, homogeneous, equal-weighted** portfolio (infinite granularity), the portfolio loss fraction equals the conditional default rate $L=p(x)$, so the stochastic factor *becomes* the loss. Inverting for the loss CDF gives Vašíček's closed form:
$$
\boxed{\,F(\theta)=\Pr[L\le\theta]=N\!\Big(\frac{\sqrt{1-\rho}\,N^{-1}(\theta)-N^{-1}(p)}{\sqrt\rho}\Big)\,}
$$
and the loss quantile at confidence $q$ (this is the **Basel IRB form**):
$$
\boxed{\,\theta_q=N\!\Big(\frac{N^{-1}(p)+\sqrt\rho\,N^{-1}(q)}{\sqrt{1-\rho}}\Big).\,}
$$
The unexpected-loss capital per unit EAD is $\theta_{0.999}-\mathrm{EL}$ with $\mathrm{EL}=p\,\mathrm{LGD}$ (set $\mathrm{LGD}=1$ above). Hull eq. (24.10) is exactly $\theta_q$; the Basel corporate asset correlation is a decreasing function of PD, $\rho_{\text{Basel}}(p)=0.12\,w+0.24\,(1-w)$, $w=(1-e^{-50p})/(1-e^{-50})$.

#### 2.2 Credit ratings & transition matrices (CreditMetrics 1997; Hull §24.9)

Ratings give a **discrete** credit state. A one-year **transition matrix** $M$ collects $\Pr(\text{state }j\mid\text{state }i)$; the default column is the one-year PD for each rating. Because default is an *absorbing* state, multi-year cumulative default probabilities are read from matrix powers:
$$
\mathbb{P}(\text{default by year }n\mid i)=\big(M^{n}\big)_{i,\text{Default}}.
$$
CreditMetrics simulates each obligor's asset return against rating-specific thresholds (calibrated so the threshold probabilities reproduce the matrix), correlates the returns with a factor model, and reads the portfolio loss distribution off the simulated rating migrations. It is the discrete, simulation-based sibling of the Vasicek formula.

#### 2.3 CDO tranching and the correlation smile

A CDO splits the portfolio loss into tranches (equity $[0,a]$, mezzanine $[a,b]$, senior $[b,1]$). Each tranche's value depends on $\Pr[L>a]$ etc., i.e. **entirely on $\rho$**: as $\rho\uparrow$, more mass moves to both tails, making junior tranches safer and senior tranches riskier (Hull §25.9). Pricing each tranche implies a different $\rho$ — the **correlation smile/skew** — which is a direct sign that the Gaussian copula is a calibration device, not a structural description.

---

### 3. Computational Implementation — Vasicek closed form vs Monte Carlo, and the transition matrix

**A. Vasicek asymptotic loss distribution, verified against a finite-$n$ Monte Carlo.** Stdlib only.

```python
import math, random

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def Ninv(p):
    """Inverse standard-normal CDF (Acklam's algorithm), stdlib only."""
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,
        1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00]
    b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,
        6.680131188771972e+01,-1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,
       -2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00]
    d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,
       3.754408661907416e+00]
    pl=0.02425
    if p<pl:
        q=math.sqrt(-2*math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p<=1-pl:
        q=p-0.5; r=q*q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q=math.sqrt(-2*math.log(1-p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

p, rho = 0.02, 0.15
vq = lambda q: N((Ninv(p)+math.sqrt(rho)*Ninv(q))/math.sqrt(1-rho))   # Vasicek quantile
print(f"EL = p = {p:.4f}")
for q in (0.99, 0.999, 0.9999):
    print(f"  q={q}: Vasicek loss quantile = {vq(q):.5f}  ({vq(q)*100:.2f}% of EAD)")

random.seed(11)
n, nsim, thr = 1000, 200000, Ninv(p)
losses = []
for _ in range(nsim):
    Y = random.gauss(0.0, 1.0)
    nd = sum(1 for _ in range(n)
             if math.sqrt(rho)*Y + math.sqrt(1-rho)*random.gauss(0.0,1.0) < thr)
    losses.append(nd / n)
losses.sort()
mean = sum(losses) / len(losses)
print(f"MC n={n}, sims={nsim}: mean={mean:.5f}  q99={losses[int(0.99*nsim)]:.4f}  "
      f"q99.9={losses[int(0.999*nsim)]:.4f}")
print(f"Vasicek asymptotic q99.9 = {vq(0.999):.4f}")
```
```
EL = p = 0.0200
  q=0.99: Vasicek loss quantile = 0.10559  (10.56% of EAD)
  q=0.999: Vasicek loss quantile = 0.17633  (17.63% of EAD)
  q=0.9999: Vasicek loss quantile = 0.25293  (25.29% of EAD)
MC n=1000, sims=200000: mean=0.01997  q99=0.1070  q99.9=0.1830
Vasicek asymptotic q99.9 = 0.1763
```
The Monte Carlo mean recovers the input PD ($1.997\%\approx2\%$), and its $99.9\%$ quantile ($18.3\%$) is close to but slightly above the asymptotic Vasicek value ($17.6\%$) — the small **granularity** premium of a finite 1000-name portfolio. Note the scale of the risk: a $2\%$ PD portfolio loses $17.6\%$ of EAD at the $99.9\%$ level — **correlation, not the mean, is what makes the capital**.

**B. Cumulative default from a rating transition matrix (CreditMetrics / S&P).** Stdlib only.

```python
labels = ["AAA","AA","A","BBB","BB","B","CCC","D"]
M = [                                    # one-year transitions (%), Default = last column
 [90.81,8.33,0.68,0.06,0.12,0.00,0.00,0.00],
 [ 0.70,90.65,7.79,0.64,0.06,0.14,0.02,0.00],
 [ 0.09,2.27,91.05,5.52,0.74,0.26,0.01,0.06],
 [ 0.02,0.33,5.95,86.93,5.30,1.17,0.12,0.18],
 [ 0.03,0.14,0.67,7.73,80.53,8.84,1.00,1.06],
 [ 0.00,0.11,0.24,0.43,6.48,83.46,4.07,5.20],
 [ 0.22,0.00,0.22,1.30,2.38,11.24,64.86,19.79],
 [ 0.00,0.00,0.00,0.00,0.00,0.00,0.00,100.0],   # default is absorbing
]
M = [[x/sum(r) for x in r] for r in M]           # normalise rows to 1

def mm(A,B):                                     # matrix multiply
    Bt = list(zip(*B))
    return [[sum(a*b for a,b in zip(row,col)) for col in Bt] for row in A]

def power(A,p):
    R = [[1.0 if i==j else 0.0 for j in range(len(A))] for i in range(len(A))]
    for _ in range(p): R = mm(R,A)
    return R

for horizon in (1,2,5,10):
    P = power(M,horizon)
    print(f"year {horizon:2d} cumulative default: " +
          "  ".join(f"{labels[i]}={P[i][7]*100:6.3f}%" for i in (0,2,3,4,5,6)))
```
```
year  1 cumulative default: AAA= 0.000%  A= 0.060%  BBB= 0.180%  BB= 1.060%  B= 5.201%  CCC=19.788%
year  2 cumulative default: AAA= 0.002%  A= 0.148%  BBB= 0.481%  BB= 2.586%  B=10.416%  CCC=33.233%
year  5 cumulative default: AAA= 0.038%  A= 0.644%  BBB= 2.105%  BB= 8.671%  B=24.406%  CCC=54.163%
year 10 cumulative default: AAA= 0.295%  A= 2.401%  BBB= 6.611%  BB=19.673%  B=40.890%  CCC=66.828%
```
The one-year numbers reproduce the matrix's default column exactly (BBB $0.18\%$, BB $1.06\%$, B $5.20\%$, CCC $19.79\%$); matrix powers give the multi-year cumulative default rates (BBB $\to6.6\%$ over ten years). This is the discrete, ratings-based route to PD — the CreditMetrics alternative to the continuous distance-to-default of page 03.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Correlation is the whole game and the least reliable input.** $\rho$ drives the $99.9\%$ quantile almost entirely (with $p$ fixed, $\rho$ from $0.15$ to $0.30$ roughly doubles senior-tranche risk), yet asset correlation is estimated with wide error bands and varies through the cycle.
2. **The Gaussian copula has zero tail dependence.** Two firms' default times are asymptotically *independent* in a Gaussian copula, so it understates **joint** extreme default clusters — the 2008 failure mode. Student-$t$ and other copulas with tail dependence are the standard repair, but the correlation is then no longer a single number.
3. **Infinite granularity is an idealisation.** The Vasicek closed form assumes a large homogeneous portfolio; concentrated or small portfolios need the finite-$n$ distribution (the MC above shows the size of the granularity gap).
4. **Transition matrices are historical and through-the-cycle.** They ignore the current state of the economy, contain rating-migration serial dependence, and their default column is estimated from a finite history — applying the matrix *unchanged* in a crisis understates default (Hull §24.9; CreditMetrics §6 warns against naive matrix multiplication over long horizons).
5. **Ratings are coarse and lag.** A rating move is a lagging, bucketed proxy for continuous changes in asset value and spread — the discrete model throws away exactly the information DD exploits.

---

### 5. Canonical Literature & Study References

- **Vašíček, Oldřich** — *Probability of Loss on Loan Portfolio* (KMV, 1987) and *Limiting Loan Loss Probability Distribution* (1991): the one-factor conditional PD and the asymptotic loss CDF. *Primary source; formula-verified in the corpus.*
- **Hull**, *Options, Futures, and Other Derivatives* — §24.9 (credit VaR, Vasicek eq. 24.10, CreditMetrics), §25.8–25.10 (CDO tranching, one-factor Gaussian copula standard market model, eqs. 25.5–25.12), §25.9 (role of correlation). *Verification report in the corpus.*
- **Gupton, Finger & Bhatia (J.P. Morgan)** — *CreditMetrics™ — Technical Document* (1997) — Table 1.8/2.1 (one-year transition matrix used above) and the migration-simulation portfolio framework.
- **Bluhm, Overbeck & Wagner** — *Introduction to Credit Risk Modeling*, Ch 2 (uniform default intensity and correlation, §2.2.2) and §1.2.3–1.3 (multi-factor asset-correlation model, portfolio UL). *Corpus digest available.*
- **BCBS** — *Basel III: Finalising Post-Crisis Reforms* (2017) — the IRB asset-correlation formula and its PD-dependent weighting; the regulatory descendant of the Vasicek result.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/04-reduced-form-and-cds|04 · Reduced-Form & CDS]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Index Hub]]
- Siblings: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the quantile $\theta_q$ *is* a credit VaR) · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]] (the joint-tail failure of the Gaussian copula) · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Index Hub]]
