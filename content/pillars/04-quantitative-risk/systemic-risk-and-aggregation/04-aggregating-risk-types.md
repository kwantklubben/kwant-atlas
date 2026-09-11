---
title: "04 — Aggregating Different Risk Types: Copulas & the (Im)possibility of Naive Sums"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - risk-aggregation
  - copulas
  - expected-shortfall
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] and [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/03-systemic-risk-measures|03 · Systemic Risk Measures]].

---

### 1. Intuition & Practical Objective

This is the single most consequential *quantitative* problem in the pillar. A bank must report **one** P&L/QIS capital number, but it runs four different kinds of risk that are shot in different currencies on different clocks:

- **Market** — daily, mark-to-market, driven by factor returns.
- **Credit** — default-frequency, long horizon, driven by counterparty health.
- **Liquidity** — event-driven, worse in stress precisely when it matters.
- **Operational** — rare, heavy-tailed, almost independent of markets (until it isn't).

The objective: see **why no neutral "add them up" exists**, and why copula/scenario methods are the only defensible route. The intuition in one line: **expected shortfall is subadditive, so "sum of the marginal ES" is an unattainable upper bound — but treating the risk types as independent is catastrophically wrong in the tail, because the marginals are tail-*dependent* precisely when they should be independent.**

---

### 2. Mathematical Ground Truth & Derivations

**Why the naive sum is "safe-but-wrong".** For any dependence, $\text{ES}_\alpha$ is subadditive,

$$
\text{ES}_\alpha(X_1+X_2) \le \text{ES}_\alpha(X_1) + \text{ES}_\alpha(X_2),
$$

with equality **only** in perfect comonotonicity (one's tail *is* the other's). So summing the marginal ES (the regulator's simple approach) can only *overstate* — it keeps you solvent at the price of holding too much capital. The Basel formula for operational risk add-ons is a cousin of this: add risk types with a fixed "correlation" coefficient instead of measuring it.

**The shared-macro-factor truth.** In reality market, credit and liquidity losses are all driven by *one* macro state $Z$ (a recession is bad for all of them *at once*). So the naive *independence* model — `VaR_combined = sqrt(VaR_1² + VaR_2²)` from summing variances — is the dangerous direction: it treats tails as addable in quadratic form and **understates** the joint tail, because the covariance term $2\operatorname{Cov}(X_1,X_2)=2(\mathbb E[X_1X_2]-\mathbb E[X_1]\mathbb E[X_2])$ is far from zero exactly when $Z$ is extreme.

**Copula aggregation (Sklar).** A copula $C$ joins marginals and carries *only the dependence*:

$$
F_{X_1,\dots,X_n}(x_1,\dots,x_n) = C\big(F_{X_1}(x_1),\dots,F_{X_n}(x_n)\big).
$$

The **Gaussian copula** (one-factor form, Vasicek's model) is the industry default and encodes **zero upper-tail dependence**: two Gaussian-copula variables *asymptotically never* crash together. The **Student-t copula** (with low df) adds **tail dependence** — joint extremes are more likely. Choosing between them is not cosmetic: it decides the size of the aggregated tail capital.

**The aggregation fallacy in one sentence.** Because tail dependence $\lambda = \lim_{u\to 1} \mathbb{P}(X_1>F_1^{-1}(u)\mid X_2>F_2^{-1}(u))$ is essentially *unobservable* (you have ~zero joint-tail observations), the copula — not the data — sets the answer, and every choice errs: sum → overstates; independence → understates; Gaussian copula → assumes no tail dependence; t-copula → assumes a specific one.

---

### 3. Computational Implementation — two loss streams, Gaussian aggregation + tail dependence

**Part A — aggregating by correlation.** Two normal loss streams (market, credit). Naive sum = $\text{ES}(\text{market})+\text{ES}(\text{credit})$; then the true aggregate ES for varying correlation $\rho$. Stdlib only, closed form via the normal-ES formula.

```python
import math

def Phi(x):  return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))
def phi(x):  return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)

def Phinv(p):
    x = 0.0
    for _ in range(60):
        x -= (Phi(x) - p)/phi(x)
        if abs(Phi(x)-p) < 1e-15: break
    return x

def ES_normal(mu, sigma, alpha):
    return mu + sigma*phi(Phinv(alpha))/(1.0 - alpha)

s1, s2, alpha = 10.0, 14.0, 0.99
esm = ES_normal(0.0, s1, alpha); esc = ES_normal(0.0, s2, alpha)
naive = esm + esc
print(f"A. Standalone ES[0.99] market={esm:.2f}, credit={esc:.2f} -> naive sum={naive:.2f}")
for rho in (0.0, 0.5, 1.0):
    sS = math.sqrt(s1*s1 + s2*s2 + 2*rho*s1*s2)
    print(f"   corr={rho:.1f}: ES[0.99](market+credit)={ES_normal(0.0, sS, alpha):7.2f}  vs naive sum {naive:.2f}")
print("B. tail dependence (co-exceedance at 1%, baseline a^2=0.0001):")
import random
def gauss():
    u1 = max(random.random(), 1e-12)
    return math.sqrt(-2.0*math.log(u1)) * math.cos(2.0*math.pi*random.random())
def coexc(x, y, a):
    qx = sorted(x)[int(a*len(x))-1]; qy = sorted(y)[int(a*len(y))-1]
    return sum(1 for xi, yi in zip(x, y) if xi <= qx and yi <= qy)/len(x)
random.seed(1); N = 200000; f = math.sqrt(0.5)
xs, ys = [], []
for _ in range(N):
    z = gauss()
    xs.append(f*z + math.sqrt(1-f*f)*gauss()); ys.append(f*z + math.sqrt(1-f*f)*gauss())
df, xt, yt = 4, [], []
for _ in range(N):
    z = gauss(); w = (gauss()**2+gauss()**2+gauss()**2+gauss()**2)/df
    xt.append((f*z+math.sqrt(1-f*f)*gauss())/math.sqrt(w)); yt.append((f*z+math.sqrt(1-f*f)*gauss())/math.sqrt(w))
print(f"   Gaussian copula co-exceedance at 1% = {coexc(xs,ys,0.01):.4f}")
print(f"   t4-copula        co-exceedance at 1% = {coexc(xt,yt,0.01):.4f}")
```
```
A. Standalone ES[0.99] market=26.65, credit=37.31 -> naive sum=63.97
   corr=0.0: ES[0.99](market+credit)=  45.85  vs naive sum 63.97
   corr=0.5: ES[0.99](market+credit)=  55.65  vs naive sum 63.97
   corr=1.0: ES[0.99](market+credit)=  63.97  vs naive sum 63.97
B. tail dependence (co-exceedance at 1%, baseline a^2=0.0001):
   Gaussian copula co-exceedance at 1% = 0.0013
   t4-copula        co-exceedance at 1% = 0.0030
```

**Read the output.** **Part A:** the naive sum (63.97) is exactly the $\rho=1$ *comonotonic* case — you only "achieve" it if the two books crash perfectly together, which never happens. The true aggregate is 45.85 (independence) to 55.65 (corr 0.5), *lower* than the sum by 8–18 currency units of overstated capital. **Part B:** co-exceedance at the 1% level is **0.0013 under a Gaussian copula vs 0.0030 under a t-4 copula** — more than **2×** difference in joint-tail probability. The aggregated capital bearing line sits on that factor of two, and it is chosen by the copula *you* pick, not by the data. This is precisely the "unmeasurable tail dependence" that makes naive aggregation indefensible.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Naive sum = assuming perfect comonotonicity.** It can only overstate (safe, wasteful). Structural.
2. **Naive independence = assuming zero covariance.** Quadratic-covariance aggregation ignores the macro factor and *understates* the joint tail. Dangerous.
3. **Gaussian copula = assuming zero tail dependence.** Even at corr 0.5 its joint 1% tail is under-represented vs a fat-marginal / t-4 clumping (0.0013 vs 0.0030); Gaussian dependence asymptotically cannot model simultaneous crashes.
4. **The copula-freedom illusion.** When tail dependence is unobservable, the result is *decision-under-model-uncertainty*: report a *range* across copulas (Gaussian vs t vs Clayton) and stress the worst, exactly as Bellini's scenario-integration does ([[pillars/04-quantitative-risk/systemic-risk-and-aggregation/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 5. Canonical Literature & Study References

- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015), Ch 5 (copulas & dependence), §5.4 (tail dependence), §6.4 (aggregating risk with a copula). *In the corpus — the authoritative treatment.*
- **Bellini**, *Stress Testing and Risk Integration in Banks* (2016) — cross-risk-type integration via a shared macro factor (CLE/MCRE), the practical "how to build it".
- **Vašíček**, *Probability of Loss on Loan Portfolio* (1987) — the one-factor Gaussian copula at the heart of Basel IRB and CreditMetrics (bridges [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 24–25 — Gaussian copula for correlated default, tranching (see the verified notes in `corpus/verified/hull_ch24-28.md`, §24.9–25.10).

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/03-systemic-risk-measures|03 · Systemic Risk Measures]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/06-advanced-extensions|06 · Advanced Extensions]]
- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/operational-risk/index|Operational Risk]]