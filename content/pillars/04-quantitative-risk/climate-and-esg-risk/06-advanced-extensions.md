---
title: "4.14.6 Advanced Extensions"
tags:
  - pillar-quantitative-risk
  - climate-and-esg-risk
  - euler-allocation
  - carbon-adjusted-pd
  - robust-risk-measures
  - climate-hedging
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · Climate Scenarios & Stress Testing]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|VaR/ES · 06 · Advanced Extensions]] (Euler's homogeneous-function theorem, spectral measures).

---

### 1. Intuition & Practical Objective

Once climate risk has become a *measurable exposure* (02), a *scenario distribution* (03) and a *data-quality problem* (05), three advanced questions remain open:

1. **How do you allocate it?** A firm needs a portfolio-level climate risk budget split across desks, sectors or funds so the parts sum to the whole — without an arbitrary "emissions share" rule. The answer is **Euler allocation** of a homogeneous risk measure, exactly as for market risk, with the **transition-shock factor** as one of the factors.
2. **How does it reach credit?** A carbon liability is a claim that ranks *behind* nothing — it is a cash outflow, so it behaves like additional debt. Capitalising it into the Merton model turns a climate exposure into a **probability of default**, which is the currency counterparty and credit risk speak.
3. **What if the distribution itself is unknowable?** Climate has *deep* uncertainty: the scenario set is a modelling choice, not a sampling distribution. The correct response is not a better point estimate but an **ambiguity-averse** (robust) risk measure — and this is where the folder returns to the coherent-risk-measure theory it started from.

The unifying observation: **the worst-case loss over a finite scenario set is already a coherent risk measure.** Artzner's scenario representation says $\rho(X)=\sup_{P\in\mathcal P}\mathbb E_P[-X/r]$ is coherent for any family $\mathcal P$ of probability measures ([[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 · §2.3]]). An NGFS scenario set with weights *is* such a family. So the "worst scenario" and the "probability-weighted scenario ES" are not ad hoc stress numbers — they are points in the theory of coherent risk measures, and the difference between them is exactly the difference between an **ambiguity set** and a **distribution**.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Factor Euler allocation of a portfolio ES

Let the loss be a linear function of two factors, $L=b_Mf_M+b_Tf_T$, with factor covariance $\Sigma=\begin{pmatrix}\sigma_M^2 & \rho\sigma_M\sigma_T\\ \rho\sigma_M\sigma_T & \sigma_T^2\end{pmatrix}$, where $f_M$ is a *market-loss* factor and $f_T$ a *transition-shock* factor ($\mathrm{Corr}=\rho>0$: a disorderly transition is a market event too). Then $\sigma_L=\sqrt{\mathbf b^{\top}\Sigma\,\mathbf b}$, and for a zero-mean normal loss

$$
\boxed{\ \mathrm{ES}_\alpha=\sigma_L\,k_\alpha,\qquad k_\alpha=\frac{\varphi(z_\alpha)}{1-\alpha},\qquad
\mathrm{EC}_i=\underbrace{b_i\frac{(\Sigma\mathbf b)_i}{\sigma_L}}_{\text{Euler contribution}}\,\cdot\, k_\alpha,\qquad \sum_i\mathrm{EC}_i=\mathrm{ES}_\alpha\ }
$$

The additivity is Euler's theorem for the positively homogeneous $\sigma_L$; the multiply-by-$k_\alpha$ step works because $\mathrm{ES}$ is positively homogeneous with the same degree ([[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|VaR/ES · 04 · §2.1]]). Explicitly,
$$
\mathrm{EC}_M=\frac{b_M^2\sigma_M^2+b_Mb_T\rho\sigma_M\sigma_T}{\sigma_L}k_\alpha,\qquad
\mathrm{EC}_T=\frac{b_T^2\sigma_T^2+b_Mb_T\rho\sigma_M\sigma_T}{\sigma_L}k_\alpha .
$$

**Three facts fall out of the cross term $b_Mb_T\rho\sigma_M\sigma_T$:**

- A **carbon-heavy** book ($b_T>0$) carries a strictly positive transition contribution, and total ES rises above the market-only book.
- A **green-tilted** book ($b_T<0$) has a *negative* transition contribution: the tilt is a **risk reducer** whenever $\rho>0$, because it pays off in exactly the states where the market factor is bad. This is the mathematics behind the "hedging climate risk" result of Andersson, Bolton & Samama (2016).
- The contribution is **not monotone in the exposure**: it is quadratic in $b_T$ with a linear cross term, so its sign depends on the *ratio* $b_T\sigma_T/(b_M\rho\sigma_M)$. Sizing a hedge by "emissions saved" is therefore not sizing a risk reduction ([[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · §4.8]]).

#### 2.2 Carbon-adjusted probability of default (Merton)

In the structural model, equity is a call on assets $A$ with strike equal to the debt $D$; default occurs if $A_T<D$. The **distance to default** and **default probability** are

$$
\boxed{\ \mathrm{DD}=\frac{\ln(A/D)+(\mu-\tfrac12\sigma_A^2)T}{\sigma_A\sqrt T},\qquad \mathrm{PD}=\Phi(-\mathrm{DD})\ }
$$

To make it carbon-aware, capitalise the *present value of the firm's future carbon costs* into the liability, $D\mapsto D+C$ — a first-order, transparent and conservative adjustment. Because $\mathrm{DD}$ is concave in $D$ while $\Phi(-\cdot)$ is convex, equal carbon-liability increments produce **increasing PD increments**: the credit channel amplifies a linearly-growing carbon exposure (verified in §3(B)). This is the natural bridge from climate risk to [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]], and it is the mechanism by which a transition scenario becomes loan losses in a supervisory stress test.

#### 2.3 Robust and spectral measures: the deep-uncertainty layer

Three nested refinements of "just use ES":

- **Ambiguity aversion (worst-case over a scenario set).** If $\mathcal P$ is the scenario family, $\rho(X)=\sup_{P\in\mathcal P}\mathbb E_P[-X]$ is coherent (Artzner Prop. 4.1) and requires no probabilities at all. This is the formal justification for stress-testing disciplines that refuse to weight NGFS scenarios.
- **Spectral weighting of the tail.** Acerbi's family $M_\varphi(L)=\int_0^1\varphi(u)\mathrm{VaR}_u(L)\,du$ with $\varphi$ non-decreasing lets a firm weight the *very* worst quantiles more heavily than ES does ($\varphi_{\mathrm{ES}}$ is a step at $\alpha$), which is the defensible way to express climate tail aversion without inventing a distribution ([[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|VaR/ES · 06 · §2.1]]). Kusuoka's representation says every law-invariant coherent measure is a mixture of expected shortfalls, so **the choice of climate risk measure is exactly the choice of a mixing measure over ES levels** — a policy, not a fact.
- **Carbon-efficient portfolios.** Constraining the transition factor, $\mathrm{Var}(L)$ minimised subject to $b_T\le\bar b_T$ (or subject to a carbon-intensity cap), traces a carbon-efficient frontier that is *not* the mean–variance frontier; Andersson–Bolton–Samama show it can be achieved at negligible tracking error ([[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]], [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Optimization]]).

---

### 3. Computational Implementation — allocating a climate risk budget and carbon-adjusting a PD

Panel (A) splits a portfolio ES into market and transition contributions for three books, verifying Euler additivity to machine precision. Panel (B) capitalises a carbon liability into the Merton model. Standard library only.

```python
# c7_advanced.py — Euler allocation of a climate risk budget + carbon-adjusted PD (page 06 §3)
import math

phi = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
Phi = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
z975 = 1.9599639845400545
k975 = phi(z975) / 0.025                      # ES(97.5%) per unit sigma

# ---------- (A) factor Euler allocation of a portfolio ES ----------
# loss L = b_M*f_M + b_T*f_T, factors = market-loss and transition-shock, Corr = rho
sig_M, sig_T, rho = 0.011, 0.010, 0.25
print("(A) Euler: ES splits into additive factor contributions (alpha = 97.5%)")
for name, b_T in (("market-only book   ", 0.00), ("carbon-heavy book  ", 0.60), ("green-tilted book  ", -0.10)):
    b_M = 1.0
    var = b_M*b_M*sig_M*sig_M + b_T*b_T*sig_T*sig_T + 2*b_M*b_T*rho*sig_M*sig_T
    sd = math.sqrt(var)
    cM = (b_M*b_M*sig_M*sig_M + b_M*b_T*rho*sig_M*sig_T) / sd
    cT = (b_T*b_T*sig_T*sig_T + b_M*b_T*rho*sig_M*sig_T) / sd
    ES = sd * k975
    print(f"    {name} (b_T={b_T:+.2f}): sd={sd:.6f}  ES={ES:.6f}")
    print(f"        market contrib {cM*k975:.6f} ({100*cM/sd:5.1f}%)   transition contrib {cT*k975:.6f} ({100*cT/sd:5.1f}%)")
    print(f"        sum = {(cM+cT)*k975:.6f}  (diff vs ES {abs((cM+cT)*k975-ES):.1e})")

# ---------- (B) carbon-adjusted Merton PD ----------
A, D0, sigA, mu, T = 100.0, 80.0, 0.20, 0.03, 1.0
print("(B) Merton distance-to-default with carbon costs capitalised into the liability")


def pd_merton(D):
    dd = (math.log(A / D) + (mu - 0.5 * sigA * sigA) * T) / (sigA * math.sqrt(T))
    return dd, Phi(-dd)


for C in (0.0, 5.0, 10.0, 15.0):
    dd, p = pd_merton(D0 + C)
    print(f"    carbon liability PV +{C:5.1f} (debt {D0+C:5.1f}) -> DD = {dd:.5f}   PD = {100*p:5.2f}%")
```
```
(A) Euler: ES splits into additive factor contributions (alpha = 97.5%)
    market-only book    (b_T=+0.00): sd=0.011000  ES=0.025716
        market contrib 0.025716 (100.0%)   transition contrib 0.000000 (  0.0%)
        sum = 0.025716  (diff vs ES 0.0e+00)
    carbon-heavy book   (b_T=+0.60): sd=0.013784  ES=0.032224
        market contrib 0.023320 ( 72.4%)   transition contrib 0.008904 ( 27.6%)
        sum = 0.032224  (diff vs ES 6.9e-18)
    green-tilted book   (b_T=-0.10): sd=0.010794  ES=0.025233
        market contrib 0.025612 (101.5%)   transition contrib -0.000379 ( -1.5%)
        sum = 0.025233  (diff vs ES 0.0e+00)
(B) Merton distance-to-default with carbon costs capitalised into the liability
    carbon liability PV +  0.0 (debt  80.0) -> DD = 1.16572   PD = 12.19%
    carbon liability PV +  5.0 (debt  85.0) -> DD = 0.86259   PD = 19.42%
    carbon liability PV + 10.0 (debt  90.0) -> DD = 0.57680   PD = 28.20%
    carbon liability PV + 15.0 (debt  95.0) -> DD = 0.30647   PD = 37.96%
```

**Panel (A).** The contributions sum to the portfolio ES to machine precision ($6.9\times10^{-18}$ for the carbon-heavy book) — the additivity that makes a climate risk *budget* possible. The carbon-heavy book carries $27.6\%$ of its ES from the transition factor despite being only $20\%$ emissions-adjacent in construction; the green-tilted book shows a **negative** transition contribution ($-1.5\%$) and a *lower* total ES ($0.025233$) than the market-only book ($0.025716$) — the hedging result of §2.1, made numeric. Note the green book's market contribution *exceeds* total ES ($101.5\%$): the parts are additive, but an individual contribution may exceed the whole when another contribution is negative — a fact worth stating before someone reports a "negative risk budget" as an error.

**Panel (B).** The carbon liability is concave-in-$\mathrm{DD}$ and convex-in-$\mathrm{PD}$: each $ $\$5 increment of capitalised carbon cost raises PD by 7.2$, $8.8$, $9.8$ points — increasing increments from a linear exposure. A transition scenario therefore converts into credit losses **faster than proportionally**, which is why supervisory exercises report both a market-risk and a credit-risk leg of the same scenario.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Euler needs homogeneity — liquidity and convexity break it.** Axiom PH fails for large positions and for non-linear (option-like) climate payoffs, so the additive split understates the marginal risk of *scaling up* a carbon exposure. Liquidity-adjust before allocating ([[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|VaR/ES · 06 · §4.2]]).
2. **Reading contribution as exposure.** The transition contribution is quadratic in $b_T$ plus a cross term; a larger carbon exposure can *lower* the contribution, and a hedge can show a positive one for small sizes. Allocate on contributions, report exposures separately.
3. **A negative contribution treated as an error.** A green tilt legitimately produces a negative risk contribution (§3(A)). Risk-budget systems that clamp contributions at zero destroy the hedging signal.
4. **Capitalising carbon costs into debt without a horizon convention.** $C$ is a *present value* of a cost path, so its magnitude depends on the discount rate and the path — publish both; a PD shift of 20 points from unspecified discounting is not a result.
5. **Merton's own limitations imported silently.** The distance-to-default model assumes lognormal assets, a single zero-coupon liability and a constant $\sigma_A$; none improves by adding a carbon term ([[pillars/04-quantitative-risk/credit-risk-and-the-merton-model|Credit Risk & the Merton Model]]).
6. **Ambiguity dressed as probability.** If you compute a probability-weighted scenario ES, you have *chosen* a measure; if you compute a worst-case, you have chosen an ambiguity set. Both are coherent, both are defensible, and they answer different questions — never mix them inside one reported number ([[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · §4.5]]).
7. **Spectral choice as a governance decision.** Because climate tail aversion has no agreed weight function, the choice of $\varphi$ (or the mixture over ES levels in Kusuoka's representation) is a *policy* that should be owned by the risk committee, published, and stress-tested for sensitivity — exactly as the regulator's and the firm's $\varphi$ differ in market risk.
8. **Optimising against a climate constraint without a scenario-consistent objective.** A carbon cap imposed inside a mean–variance optimiser can trade one factor for another without changing the true scenario exposure; validate the resulting portfolio on the *scenario* engine of 03, not on the constraint you imposed.

---

### 5. Canonical Literature & Study References

- **Acerbi, C. & Tasche, D.** — *On the Coherence of Expected Shortfall*, *J. Banking & Finance* 26(7):1487–1503 (2002) — Euler allocation (component CVaR) of ES, the additivity verified in §3(A).
- **Acerbi, C.** — *Spectral Measures of Risk: A Coherent Representation of Subjective Risk Aversion*, *J. Banking & Finance* 26(7):1505–1518 (2002) — the spectral family and the role of the weight function $\varphi$.
- **Kusuoka, S.** — *On Law Invariant Coherent Risk Measures*, *Advances in Mathematical Economics* 3:83–95 (2001) — every law-invariant coherent measure is a mixture of expected shortfalls.
- **Artzner, Delbaen, Eber & Heath** — *Coherent Measures of Risk*, *Mathematical Finance* 9(3):203–228 (1999) — the scenario representation (Prop. 4.1) that makes a scenario stress test a coherent risk measure.
- **Andersson, M., Bolton, P. & Samama, F.** — *Hedging Climate Risk*, *Financial Analysts Journal* 72(3):13–32 (2016) — carbon-efficient portfolios at negligible tracking error; the green-tilt result of §2.1.
- **Merton, R.C.** — *On the Pricing of Corporate Debt: The Risk Structure of Interest Rates*, *Journal of Finance* 29(2):449–470 (1974) — the structural model used in §2.2.
- **Bolton, P. & Kacperczyk, M.** — *Do investors care about carbon risk?*, *JFE* 142(2):517–549 (2021) — the empirical counterpart of the transition factor.
- **BCBS** — *Climate-related Financial Risks — Measurement Methodologies* (2021) — supervisory treatment of climate risk aggregation across risk types. *[REG]* (Extended reading: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]].)

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · Climate Scenarios & Stress Testing]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/index|Index Hub]]
- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|VaR/ES · 06 · Spectral & Euler]] · [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (Euler's theorem)
- Sibling: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Risk Constraints & Mean–Variance]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & Equal Risk Contribution]] (the same Euler idea, different budget rule) · [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Optimization]]
