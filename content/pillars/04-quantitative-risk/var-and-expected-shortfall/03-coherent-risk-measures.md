---
title: "4.1.3 Coherent Risk Measures"
tags:
  - pillar-quantitative-risk
  - var-and-expected-shortfall
  - coherent-risk
  - axioms
  - scenario-representation
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|02 · VaR Definition & Flaws]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Before Artzner–Delbaen–Eber–Heath (1999), "risk measure" meant *whatever a bank computed*. Their contribution was to ask: **what properties must any number claiming to be "risk" satisfy to be usable for regulating capital?** Four axioms. A measure satisfying all four is **coherent**. VaR fails one of them; ES passes all.

This page states the axioms, connects them to a *set of acceptable positions* (the deeper primitive), gives the **scenario representation** (every coherent measure is a worst-case expectation over a set of probability scenarios), and shows - numerically - which axiom VaR breaks.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The four axioms (Artzner Def. 2.4)

Fix the future net worth $X$ and a reference return $r$ (typically $r=1$; think of $X$ as P&L). A measure $\rho:\mathcal{G}\to\mathbb{R}$ is **coherent** iff:

| Axiom | Statement | Meaning |
|---|---|---|
| **T** Translation invariance | $\rho(X+\alpha r)=\rho(X)-\alpha$ | adding sure cash $\alpha$ reduces risk by $\alpha$ (risk is a *capital* number) |
| **S** Subadditivity | $\rho(X_1+X_2)\le\rho(X_1)+\rho(X_2)$ | "a merger does not create extra risk" |
| **PH** Positive homogeneity | $\rho(\lambda X)=\lambda\rho(X),\ \lambda\ge0$ | risk scales with size (no liquidity/concavity) |
| **M** Monotonicity | $X\le Y\ \Rightarrow\ \rho(Y)\le\rho(X)$ | more net worth is never riskier |

Consequences useful in practice: T gives $\rho(X+\rho(X)r)=0$ (the risk measure *is* the capital that makes the position acceptable); T + PH give $\rho(\alpha(-r))=\alpha$. Artzner notes **M rules out** mean–standard-deviation measures $\rho(X)=-\mathbb{E}_P[X]+\alpha\sigma_P(X)$, and **S rules out** semi-variance-type measures - i.e. the axioms are *restrictive*.

#### 2.2 The deeper primitive: acceptance sets (Artzner §2.2–2.4)

Define the acceptance set $\mathcal{A}=\{X:\rho(X)\le0\}$ - positions that need no extra capital. The measure is recovered as
$$
\rho_{\mathcal{A},r}(X)=\inf\{m: m\,r+X\in\mathcal{A}\}.
$$
**Axioms on $\mathcal{A}$** (contains the positive orthant $L^+$; avoids the strictly-negative orthant $L^{--}$; is **convex**; is a **positively homogeneous cone**) are *equivalent* to coherence of $\rho$ (Props. 2.1–2.2). This is why VaR's failure bites: its acceptance set is **not convex** ([[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|02 · §2.2]]).

#### 2.3 Representation: coherence ⇔ worst-case scenarios (Artzner §4.1)

**Proposition 4.1 (Artzner et al.).** $\rho$ is coherent **iff** there is a family $\mathcal{P}$ of probability measures on the states of the world such that
$$
\boxed{\ \rho(X)=\sup\{\mathbb{E}_P[-X/r] \mid P\in\mathcal{P}\}\ }
$$
i.e. every coherent risk measure is a **supremum of expected losses over a set of "generalized scenarios."** Conversely (Prop. 3.1) any $\rho_{\mathcal{P}}(X)=\sup_{P\in\mathcal{P}}\mathbb{E}_P[-X/r]$ is coherent (satisfying relevance iff $\bigcup_P \operatorname{supp}P=\Omega$). Adding more scenarios makes the measure **more conservative**. This is the theoretical roof over *all* coherent measures - including ES, which is the special case where $\mathcal{P}$ is the set of all measures agreeing with the base measure on the tail (equivalently the spectral representation in [[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|06 · Advanced Extensions]]).

#### 2.4 ES as coherence repair (Artzner §5.1)

Artzner's concrete repair uses the *tail conditional expectation* (TailVaR):
$$
\mathrm{TCE}_\alpha(X)=-\mathbb{E}_P[X/r\mid X/r\le-\mathrm{VaR}_\alpha(X)],\qquad
\mathrm{WCE}_\alpha(X)=-\inf\{\mathbb{E}_P[X/r\mid A]:\mathbb{P}(A)>\alpha\}.
$$
He proves $\mathrm{TCE}_\alpha\le\mathrm{WCE}_\alpha$ (Prop. 5.1), with equality when $\mathbb{P}$ is uniform and the discounted outcomes are distinct (Prop. 5.3). And the sharpest statement of VaR's status (Prop. 5.2):
$$
\mathrm{VaR}_\alpha(X)=\inf\{\rho(X):\rho\ \text{coherent},\ \rho\ge\mathrm{VaR}_\alpha\},
$$
i.e. **VaR is the least coherent measure that dominates it.** Any coherent measure you pick (ES, WCE) must be *at least* as large as VaR - coherence costs conservatism, and this identity quantifies the gap.

---

### 3. Computational Implementation - the axioms, checked numerically

We encode discrete loss distributions as pmfs and test all four axioms for VaR and ES on the defaultable-bond example. Stdlib only.




Both measures satisfy **T, PH, M**. VaR fails **S**; ES passes. That single `False` is the entire twentieth-century risk-management debate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Scenario-set mis-specification.** The representation $\rho(X)=\sup_{P\in\mathcal{P}}\mathbb{E}_P[-X/r]$ is only as good as $\mathcal{P}$. Too small and the measure is optimistic ("model risk" - Artzner's Remark: add other models' distributions to $\mathcal{P}$); too large and every position looks maximally risky. ES corresponds to a *specific* $\mathcal{P}$; choosing "coherent" does not remove the modelling choice.
2. **Homogeneity is an idealisation.** Axiom PH ignores liquidity: if liquidating a position moves the price, then $\rho(\lambda X)<\lambda\rho(X)$, and the axiom over-states large-position risk (Artzner's own caveat on Axiom PH). This is the formal reason liquidity-adjusted risk measures are needed ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]]).
3. **Coherence ≠ correctness of the loss distribution.** The axioms constrain the *functional*, not the *distribution*. A coherent measure on a wrong $\mathbb{P}$ is still wrong. Coherence buys aggregation safety, not predictive accuracy ([[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Estimation & Backtesting]]).
4. **Dominance cost of repair (Prop. 5.2).** Any coherent measure dominating VaR is *at least* VaR. Replacing VaR with ES raises the reported capital number - a governance decision as much as a mathematical one, which is exactly why the Basel switch needed a calibration ($97.5\%$ ES $\approx$ $99\%$ VaR; [[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|06 · §Basel]]).

---

### 5. Canonical Literature & Study References

- **Artzner, Delbaen, Eber & Heath**, *Coherent Measures of Risk* (1999) - §2.2–2.4 (acceptance-set axioms; coherence Def. 2.4), §3.3 (VaR's non-convex acceptance set), §4.1 (Prop. 4.1, scenario representation), §5.1 (TCE/WCE; Props. 5.1–5.3). *Primary source; read in full from the corpus PDF.*
- **Föllmer & Schied**, *Stochastic Finance: An Introduction in Discrete Time* - the modern axiomatic treatment (convex risk measures, monetary measures of risk).
- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015), Ch 2 - coherence, convexity, and law-invariant measures in textbook form.
- **Acerbi & Tasche**, *On the Coherence of Expected Shortfall*, *J. Banking & Finance* 26(7) (2002) - ES coherence under general distributions.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|02 · VaR Definition & Flaws]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|04 · Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/06-advanced-extensions|06 · Spectral & Euler]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
