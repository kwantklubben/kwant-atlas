---
title: "3.15.5 Failure Modes & Practice"
tags:
  - pillar-derivative-pricing
  - path-signatures-and-rough-paths
  - lead-lag
  - time-augmentation
  - geometric-rough-paths
  - signature-hedging
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/02-the-signature-algebra|02 · The Signature Algebra]] and [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/04-rough-path-theory|04 · Rough Path Theory]].

---

### 1. Intuition & Practical Objective

Pages 01–03 proved beautiful identities about the signature *of a path*. This page is about the gap between that theory and raw financial data, and the two standard bridges across it:

1. **Raw data is non-geometric.** The signature identities (shuffle product, geometric rough-path structure) hold for *geometric* (Stratonovich) iterated integrals. Financial increments are *Itô-type* - and on top of that, a **univariate** series is pathologically uninformative: the signature of a 1D path is just its endpoint. The two fixes are **time augmentation** and the **lead-lag transform**, both of which *geometricise* the data and make the signature informative. They are not optional pre-processing; they are what makes the theory applicable at all.
2. **Signatures are hedging instruments.** Because path-functionals are representable (universally) as combinations of signature terms, the *ingredients of a hedge* - the quantities a desk needs to replicate a path-dependent payoff - are themselves signature features. The cleanest example: the **variance-swap payoff** (realized variance) is, up to a factor, the **Lévy area** of the lead-lag path, i.e. a level-2 signature coefficient. Signatures do not merely *describe* paths; they *price and hedge* them.

Three practical claims:

3. **The endpoint is not the signal.** For a univariate path, $S^{11}=\tfrac12(S^1)^2$ is determined by the endpoint - the raw signature contains *no shape information*. Augmenting with time, $X_t\mapsto(t,X_t)$, restores a meaningful area (the signed area under the path).
4. **Lead-lag makes the area equal a variance.** The lead-lag path $(X_t, X_{t+\delta})$-style construction turns the **quadratic variation** into the **Lévy area** of the transformed path. Since realized variance *is* a (stylised) variance-swap payoff, the lead-lag signature is a direct pricing/hedging object - the bridge used in the literature (Lyons–Ni–Zhang) for rough-vol lead-lag signatures.
5. **Truncation, augmentation and the lift are coupled choices.** The depth to which you truncate, how you augment, and which rough-path lift you implicitly selected together determine what your signature does and does not see (§4).

The practical objective: know how to take a raw time series, geometricise it (time augmentation or lead-lag), compute a meaningful truncated signature/log-signature, and connect specific signature features to specific hedging quantities.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The failure: raw 1D and Itô-type data

A 1D path $X_t$ has signature with words over a single letter; every level is a power of the endpoint, $S^{1^k}=(S^1)^k/k!$. So the raw 1D signature carries **only the endpoint** - all shape is gone. For a multivariate path the situation is better but still Itô-flawed: the *classical* (Itô) iterated integrals fail the shuffle identity (an Itô correction at the diagonal), so the object that falls out of raw increments is not a geometric signature.

#### 2.2 Time augmentation

For a path $X_t$ (any dimension), the **time augmentation** is $\widehat X_t=(t,X_t)\in\mathbb R^{d+1}$. Adding time as a coordinate achieves three things at once: the path becomes *strictly* non-degenerate (time strictly increases), the level-2 cross terms with time acquire meaning (the area under the path), and the leading behaviour is regularised. §3 shows two same-endpoint univariate paths whose raw signatures are identical but whose augmented signatures differ exactly through the area $-\int X_t\,dt$ captured at level 2. Time augmentation is the minimal geometricisation: it requires no extra parameters.

#### 2.3 The lead-lag transform

The **lead-lag** transform of a discrete path $X_0,X_1,\dots,X_n$ builds a path in $\mathbb R^{2d}$ that moves the *lead* copy first and the *lag* copy second:

$$
X_0^{lead}=X_0^{lag}=X_0,\qquad\text{then }\ (X_1,X_0)\to(X_1,X_1)\to(X_2,X_1)\to\cdots
$$

Between each pair of sample points the lead-lag path sweeps a right triangle in the (lead,lag) plane, so its **Lévy area** equals

$$
\boxed{\;\mathrm{Area}_{\text{lead-lag}}=\tfrac12\sum_{k}\big(X_{k+1}-X_k\big)^2=\tfrac12\,\text{realized variance}\;}
$$

Each little triangle has legs $\Delta X_k,\Delta X_k$ (area $\tfrac12\Delta X_k^2$), and the sum is exact - §3 verifies it to $10^{-14}$. Consequences: (a) the lead-lag path is **geometric** (the shuffle identities hold on it - the cross-covariance between lead and lag *is* the quadratic covariation), and (b) the *variance-swap payoff* $=$ realized variance $=2\times$ the lead-lag Lévy area, a level-2 signature term. This is the mathematical core of **signature-based pricing of variance** and of the **lead-lag signature of rough volatility** (Lyons–Ni–Zhang).

#### 2.4 Signature-based hedging

The **universality** of the signature (linear combinations of signature terms approximate any continuous path-functional) makes the signature the natural *basis* for hedging: a payoff $F(X)$ is approximated by $\sum_w \alpha_w S^w(X)$, and a delta/vega-style hedge is built from the sensitivity of those basis terms. In the Malliavin / functional-Itô framework (Dupire; Cont–Fournié) the hedging weights are signature-driven. The concrete, fully-computable instance in this folder is the variance swap: its payoff is a signature feature (the lead-lag area), so a variance-swap hedge is a *signature-level-2* position, exactly as the log-contract replication of [[foundations/econometrics-and-timeseries/04-volatility-modeling|Volatility Modeling]] suggests. Signatures give a systematic coordinate system for this replication rather than an ad hoc set of contracts.

---

### 3. Computational Implementation - geometricisation (lead-lag & time augmentation) and the variance-swap signature

We (i) build the **lead-lag** transform of a seeded random-walk path and verify the Lévy-area-equals-half-realized-variance identity to machine precision, (ii) show **time augmentation** makes two same-endpoint univariate paths distinguishable (identical raw 1D signature, different augmented areas), and (iii) state the **variance-swap payoff as a signature feature**. Stdlib only, deterministic (`random.seed`).




**Reading the output.**

- **Lead-lag turns a variance into an area, exactly.** The lead-lag path's **Lévy area** equals half the realized variance to $1.4\times10^{-14}$. This is not an approximation - each lead-lag triangle contributes exactly $\tfrac12\Delta X_k^2$. The consequence is the workhorse identity of signature pricing: the variance-swap payoff (realized variance) is a *level-2 signature coefficient* of the lead-lag path.
- **Time augmentation restores the shape that 1D throws away.** The two paths have identical raw 1D signatures ($S^1=2.0$, $S^{11}=2.0$ - the endpoint in disguise) but their time-augmented areas differ: $-0.667$ vs $+0.667$, i.e. the signed area under the two different curves. Augmentation is the minimal fix that makes univariate signatures carry information.
- **The hedge is a signature position.** Because realized variance $=2\times(\text{lead-lag area})$, a variance-swap hedge is literally a trade in a level-2 signature feature of the lead-lag path. This is the concrete, checkable seed of signature-based hedging: the building blocks of path-dependent hedges are signature coefficients, not hand-chosen contracts.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Feeding raw 1D signatures to a model.** A univariate signature is the endpoint in disguise ($S^{11}=\tfrac12(S^1)^2$); the model learns nothing about the path's shape. Always time-augment or lead-lag univariate data first - this is the single most common mistake in applied signature work (Chevyrev–Kormilitzin stress it explicitly).
2. **Using Itô integrals and expecting geometric identities.** The shuffle product and the geometric rough-path structure hold only for Stratonovich-type (piecewise-linear / geometric) integrals. Raw increments give an Itô object that fails the identities; the lead-lag and time-augmented constructions are *exactly* the fixes that restore the geometric convention.
3. **Reading reparametrisation invariance as "time doesn't matter."** It matters enormously - that is the *point* of lead-lag. The raw signature is speed-blind, which is a feature for geometry and a bug when the timing/order of events is the signal (order flow, lead-lag of vol). Lead-lag deliberately re-encodes time so that the *order* of lead/lag coordinates carries the cross-covariance information.
4. **Truncating without a scale.** The signature's high levels carry small, fast oscillations; truncating at low level literally discards the short-time structure - exactly what rough vol depends on (§06). The truncation level and the time step are jointly decided, not separately.
5. **Treating the lead-lag area as "free."** The identity §3 is exact for a *given* sampling; it is a *chosen* lift of the raw series, and its value is convention-dependent (Itô vs Stratonovich, choice of time grid). What is robust is the *relation* between the area and realized variance, not the absolute area on any one realisation.

---

### 5. References

- **Chevyrev, I. & Kormilitzin, A.** (2016), *A Primer on the Signature Method in Machine Learning*, arXiv:1603.03788
- **Lyons, T. J., Ni, H., Zhang, H.** (2019), *Machine Learning Models of Financial Time Series*, arXiv:1905.11666
- **Chevyrev, I. & Oberhauser, H.** (2022), *Signature moments to characterize laws of stochastic processes* (J. Mach. Learn. Res.)
- **Dupire, B.** (2009) / **Cont, R. & Fournié, D.-A.** (2010), *Functional Itô calculus*
- **Gatheral, Jaisson & Rosenbaum** (2018), *Volatility is rough*
- **Friz & Victoir** (2010), *Multidimensional Stochastic Processes as Rough Paths*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/04-rough-path-theory|04 · Rough Path Theory]]
- Forward: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Index Hub]]
- Cross-links: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Rough Volatility]] · [[foundations/econometrics-and-timeseries/04-volatility-modeling|Volatility Modeling]] (realized variance, variance swaps) · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Numerical Methods · 03 Monte Carlo]] (simulation of lifted paths) · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
