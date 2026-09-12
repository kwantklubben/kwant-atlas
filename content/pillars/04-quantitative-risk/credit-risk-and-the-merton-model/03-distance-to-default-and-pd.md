---
title: "4.4.3 Distance to Default & Default Probability"
tags:
  - pillar-quantitative-risk
  - credit-risk-and-the-merton-model
  - distance-to-default
  - default-probability
  - kmv
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/02-the-merton-structural-model|02 · The Merton Structural Model]].

---

### 1. Intuition & Practical Objective

Once you have inverted equity into firm value and asset volatility, default probability is one step away - but the step contains the field's most important distinction. **Distance to default** (DD) is the number of asset-volatility standard deviations between today's firm value and the default point:

$$
\mathrm{DD}=\frac{\ln(V/D)+(\mu-\tfrac12\sigma_V^2)T}{\sigma_V\sqrt T}.
$$

It answers the practitioner's question directly: *how far is this firm from the wall, measured in the units in which the firm actually moves?* Two firms with the same leverage are not equally risky - the one with the more volatile assets is closer to default in the only metric that matters.

The subtlety: **which drift $\mu$?** Use the risk-neutral drift $r$ and $\mathrm{PD}=N(-\mathrm{DD})$ is the *risk-neutral* default probability $N(-d_2)$ - the right object for **pricing** (CDS, bonds, CVA). Use the physical (expected) return $\mu$ and you get the *real-world* PD - the right object for **risk management and capital**. These differ, and the risk-neutral PD is systematically higher. Getting this distinction wrong is the most common conceptual error in credit risk.

> **Why DD is the right coordinate.** $N(-\mathrm{DD})$ is monotone in DD, and DD separates the *two* things that matter - leverage ($\ln(V/D)$) and business risk ($\sigma_V$) - while normalising by the horizon. KMV's empirical EDF mapping is built entirely on DD.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Real-world vs risk-neutral default probability

Under the physical measure the firm value has drift $\mu$; under the risk-neutral measure it has drift $r$. The probability the firm defaults is $\mathbb{P}(V_T<D)$ in each world, and both are $N(-\text{DD})$ with the appropriate drift:

$$
\mathrm{DD}^{\text{RN}}=\frac{\ln(V/D)+(r-\tfrac12\sigma_V^2)T}{\sigma_V\sqrt T}=d_2,\qquad
\mathrm{DD}^{\mathbb{P}}=\frac{\ln(V/D)+(\mu-\tfrac12\sigma_V^2)T}{\sigma_V\sqrt T}.
$$

So $\mathbb{Q}(\text{default})=N(-d_2)$ **exactly**, while the real-world $\mathrm{PD}=N(-\mathrm{DD}^{\mathbb{P}})$. Because risky assets have a risk premium, $\mu>r$, hence $\mathrm{DD}^{\mathbb{P}}>\mathrm{DD}^{\text{RN}}$ and
$$
\underbrace{N(-d_2)}_{\text{risk-neutral}} \;>\; \underbrace{N(-\mathrm{DD}^{\mathbb{P}})}_{\text{real-world}}\quad\text{for a risk-averse market.}
$$
(Hull §24.5: risk-neutral PDs exceed historical PDs; the gap is the risk premium. The real-world PD is the one to compare with S&P/Moody's historical default tables.)

#### 2.2 The KMV default point (Crosbie–Bohn empirical refinement)

Plain Merton sets the barrier at *total* debt $D$. Moody's KMV found empirically that firms default when assets fall below
$$
D^{*}=\text{short-term debt}+\tfrac12\,\text{long-term debt},
$$
because long-term debt does not come due immediately. Substituting $D^{*}$ for $D$ in $\ln(V/D)$ raises DD for long-dated-debt-heavy firms and is the practical form used by EDF vendors. (Bluhm §1.2.3 refers to this as the calibrated *default point* of the asset-value model.)

#### 2.3 From PD to credit spread (Merton eq. 14)

The spread is not $N(-d_2)$ scaled - it is the *risky yield minus $r$* obtained from the debt value:
$$
R(t)-r=-\frac1t\ln\Big\{\Phi[h_2]+\tfrac1d\Phi[h_1]\Big\},\qquad d=D e^{-rt}/V,\quad R(t)=-\frac1t\ln\!\frac{F}{D}.
$$
For a firm at the money (large $\sigma_V$, high leverage) this is the price of the put the shareholders hold; for a safe firm it collapses to a fraction of a basis point - which is exactly where the model fails empirically (page 05).

#### 2.4 The DD → PD map in practice

Three mappings coexist: (i) the Gaussian $N(-\mathrm{DD})$; (ii) KMV's **empirical** EDF map, which maps DD to an *observed* historical default rate (fatter-tailed than Gaussian); and (iii) rating-agency cumulative default tables. All three are monotone in DD; only (i) is the model's own output.

---

### 3. Computational Implementation - DD, both PDs, and the credit spread

Continuing the worked firm from page 02 ($E_0=100$, $\sigma_E=0.40$, $D=350$, $T=1$, $r=5\%$). Stdlib only.



Three verified takeaways: (1) the risk-neutral PD is $26.4$ bp; (2) a realistic risk premium ($\mu=10\%$) *lowers* the real-world PD to $4.3$ bp - six times smaller; (3) the model's own credit spread is $0.71$ bp, which no market would ever quote for this firm. (2) and (3) are the seeds of page 05.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Risk-neutral ≠ real-world PD.** Quoting $N(-d_2)$ as "the probability of default" for risk purposes is wrong by a factor of several here. Pricing uses $\mathbb{Q}$; capital and limits use $\mathbb{P}$ (Hull §24.5).
2. **The Gaussian PD is too thin-tailed.** $N(-\mathrm{DD})$ underestimates tail default rates; KMV re-maps DD onto *empirical* EDFs for this reason. The $N(-d_2)$ from a lognormal firm value is a *model* probability, not a robust frequency (see [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]]).
3. **DD is only as good as the inversion.** DD inherits every error from the $(V,\sigma_V)$ solve. In practice $\sigma_V$ is estimated with large noise, and DD is highly sensitive to it (page 05 quantifies a $\sim9\%$ PD move per $1\%$ move in $\sigma_E$).
4. **The default point is a judgement call.** $D$, or $D^{*}=\text{ST}+\tfrac12\text{LT}$, or a barrier - the DD level shifts with the choice, and it is calibrated, not derived.

---

### 5. References

- **Hull**, *Options, Futures, and Other Derivatives*
- **Merton (1974)**
- **Bluhm, Overbeck & Wagner** - *Introduction to Credit Risk Modeling*
- **Gupton, Finger & Bhatia** - *CreditMetrics™ Technical Document* (1997): the transition-matrix analogue (PD read off the default column) as the discrete alternative to DD.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/02-the-merton-structural-model|02 · Structural Model]]
- Forward: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/04-reduced-form-and-cds|04 · Reduced-Form & CDS]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the quantile of the credit loss distribution DD feeds)
