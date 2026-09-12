---
title: "3.15.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - path-signatures-and-rough-paths
  - expected-signature
  - signature-kernel
  - machine-learning
  - rough-volatility
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/03-log-signature-and-lie-algebra|03 · Log-Signature & Uniqueness]] and [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. The statistical framing is [[foundations/statistics-and-inference/index|Statistics & Inference]].

---

### 1. Intuition & Practical Objective

Pages 01–05 built signatures for *single* paths. Almost every applied problem, though, is about a *distribution* of paths or a *similarity* between paths:

- *"Given the history of spot and vol, what is the expected payoff / hedge ratio?"* - an expectation over paths.
- *"Which of two historical episodes is more like today?"* - a similarity between paths.
- *"Train a model on thousands of intraday paths."* - a feature map into a vector space.

The signature answers all three through two upgrades, and this page is about them:

1. **The expected signature** $\mathbb E[S(X)]$ - the path-level analogue of the moment generating function. By the **Chevyrev–Lyons uniqueness theorem**, the expected signature **determines the law of the path** (under mild conditions): it is a universal, faithful characterisation of a *distribution* of paths, not just a descriptor of one. It is also the object that makes signature-based *pricing and hedging* rigorous - prices are expectations of path-functionals, and those functionals are signature-features.
2. **The signature kernel** $K(X,Y)=\langle S(X),S(Y)\rangle=\sum_w S^w(X)S^w(Y)$ - a positive-definite inner product on paths that respects the *ordered* geometry of the whole path. It lets any kernel method (SVM, Gaussian-process regression, kernel ridge) operate directly on paths without hand-engineered features, and it is computable recursively in linear time (the **signature kernel**, Kiraly–Oberhauser). This is the machine-learning face of the folder.

A third application closes the loop to finance:

3. **Lead-lag signatures for rough volatility.** Because vol is *rougher than Brownian* ($H\approx0.1$, Gatheral–Jaisson–Rosenbaum 2018), and because the lead-lag transform turns quadratic covariation into a signature (Lévy) area (§05), the **lead-lag signature of spot-and-vol** is exactly the right feature to learn the spot/vol dependence that prices vol products. Lyons–Ni–Zhang make this concrete: signature features of lead-lagged (log-price, vol) paths drive prediction of implied/realised vol. §3 shows the lead-lag Lévy area of a rough 2D path is a stable, computable object - the building block of those features.

The practical objective: know the expected signature and its uniqueness property, know the signature kernel and that it is computable and positive-definite, and see how lead-lag + signature features turn a rough-vol path into ML-ready inputs.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The expected signature and law-uniqueness

For a random path $X$ (a stochastic process over $[0,T]$), the **expected signature** is

$$
\mathbb E\big[S(X)\big]=\Big(\mathbb E[S^{w}(X)]\Big)_{w},\qquad \mathbb E[S^w(X)]=\int S^w(x)\,d\mu(x),
$$

where $\mu$ is the law of $X$. For a 1D Brownian motion, because $S^{1^k}=B_T^k/k!$, the expected signature is determined by the Gaussian moments: odd levels vanish and $\mathbb E[S^{11}]=T/2$, $\mathbb E[S^{1111}]=T^2/8$ - the exact values the §3 Monte Carlo reproduces. The central result (Chevyrev–Lyons 2016) is that, under mild moment conditions, **the expected signature characterises the law**: $\mathbb E[S(X)]=\mathbb E[S(Y)]\Rightarrow X\triangleq Y$ (the laws are equal). It is the path-space analogue of "the moment generating function determines the distribution" - and it is why the expected signature, not ad hoc summary statistics, is the *right* description of a path ensemble for pricing and hedging.

#### 2.2 The signature kernel

For two paths $X,Y$, the **signature kernel** is the inner product of their truncated-or-full signatures:

$$
\boxed{\;K(X,Y)=\langle S(X),S(Y)\rangle=\sum_{w} S^w(X)\,S^w(Y)\;}
$$

The sum runs over all words $w$ (in practice truncated at some level $N$). It is symmetric and **positive semi-definite** (it is a Gram-matrix of the signature feature map), so it is a valid kernel; §3 verifies the Cauchy–Schwarz inequality numerically. Because the signature is *reparametrisation-invariant* and *complete*, $K$ is a natural similarity between paths - two paths are close iff their ordered geometry (increments *and* areas *and* higher shape) is close. Computationally the kernel avoids materialising the (huge) truncated signature explicitly: it is evaluated recursively in $\mathcal O(T_1 T_2)$ time (Kiraly–Oberhauser 2019). This is the practical enabler for kernel methods on thousands of paths.

#### 2.3 Signatures, expected signatures, and pricing/hedging

A (path-dependent) payoff is a functional $F(X)$; universality says $F\approx\sum_w \alpha_w S^w$, so its risk-neutral price is $\mathbb E[F(X)]\approx\sum_w\alpha_w\mathbb E[S^w]=\langle\alpha,\mathbb E[S]\rangle$ - a *linear* function of the expected signature. This is the systematic content of signature-based pricing: **price vectors are linear functionals of the expected signature**, and hedging weights are the sensitivities of those functionals. The §3 Monte Carlo, by estimating $\mathbb E[S]$ for Brownian motion, is precisely the numerical ingredient of such a pricing scheme.

#### 2.4 Lead-lag signatures for rough volatility

Rough vol: $\ln\sigma$ is a fractional process with $H\approx0.1$ (Gatheral–Jaisson–Rosenbaum 2018), so the *spot-and-vol* joint path is genuinely rough and its level-2 iterated integrals require the rough-path lift. The **lead-lag transform** (§05) makes the quadratic covariation between spot and vol *visible as a signature area*, and the truncated signature (or kernel) of the lead-lagged $(X,\sigma)$ path becomes a rich, geometry-respecting feature set. Lyons–Ni–Zhang (2019) use exactly this: signature features of lead-lagged financial series predict vol, and the lead-lag area is the signature-level realisation of the spot/vol covariance. §3 computes the lead-lag Lévy area of a Brownian 2D path (the rough-vol building block) and shows it is stable under refinement.

---

### 3. Computational Implementation - expected signature, signature kernel, and the rough-vol lead-lag area

We (i) estimate the **expected signature** of 1D Brownian motion by seeded Monte Carlo and compare to the exact analytic values, (ii) evaluate the **signature kernel** between two paths (truncated level 2) and verify positive semi-definiteness via Cauchy–Schwarz, and (iii) compute the **lead-lag Lévy area** of a 2D Brownian path (the rough-vol feature building block) and check its stability under refinement. Stdlib only, seeded (`random.seed`), deterministic.




**Reading the output.**

- **The expected signature is the law's moment-generating object.** The Monte Carlo estimates converge to the analytic Gaussian values: $\mathbb E[S^{11}]=0.49055$ vs $0.5$ and $\mathbb E[S^{1111}]=0.11719$ vs $0.125$ (MC error ~$2\%$ at 4000 paths and a coarse 200-step grid), odd levels ~$0$. Since these moments characterise the law (Chevyrev–Lyons), estimating $\mathbb E[S]$ *is* estimating the law - the seed of signature-based pricing, where a price is a linear functional of the expected signature.
- **The signature kernel is a valid inner product on paths.** $K(X,Y)=170.5$ with $K(X,X)=56.75$, $K(Y,Y)=556.75$; Cauchy–Schwarz holds ($K_{XY}^2=29070.25\le31595.56$). The kernel is the similarity an SVM/GPR would feed on - computed here by explicit truncated sums, but in production by the linear-time recursive algorithm.
- **The rough-vol lead-lag area is a stable building block.** The lead-lag Lévy area of the 2D Brownian path stays bounded and converges under refinement ($+0.244\to+0.233$). This is the same construction §05 used for realized variance, now as the *spot/vol covariance* feature that lead-lag signature methods feed to a rough-vol predictor (Lyons–Ni–Zhang).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Estimating expected signatures with too few paths / too low truncation.** The signature levels decay only *factorially*, so high-level moments are small but slow to estimate; with a coarse grid and a few thousand paths the estimator error ($\sim2\%$ in §3) compounds at higher level. Budget the grid and the path count against the level you actually need.
2. **Believing the expected signature is the same as the mean path.** It is a *tensor-valued* moment - it captures the whole ordered geometry (areas, volumes) of the ensemble, not just an average trajectory. Reading it as a mean path loses the covariance content that is the whole point.
3. **Using the kernel without checking positive semi-definiteness / truncation convergence.** $K$ is PSD in the limit; a *truncated* kernel is PSD too (Gram of a finite feature map) but its values are truncation-dependent. Two implementations truncating at different levels give different "similarities" - fix the level by a stability study, not by convenience.
4. **Ignoring reparametrisation invariance when it matters.** The signature (and kernel) is speed-blind; if two paths differ only by how fast they were traversed, they are kernel-identical. When timing matters, lead-lag/time augmentation (§05) must be applied *before* the kernel - otherwise the "similarity" silently ignores the timing signal.
5. **Applying raw-signature features to univariate series.** Same failure as §05: a univariate signature is the endpoint in disguise, so the kernel/features learn nothing about shape. Always augment (time, lead-lag) univariate inputs first.
6. **Jumping to rough-vol lead-lag without the lift.** Rough paths need the geometric lift; the lead-lag area is a *chosen* lift whose value is convention-dependent. Computing it from raw increments without fixing the geometric convention gives an Itô-flawed, convention-arbitrary number (§04).

---

### 5. References

- **Chevyrev, I. & Lyons, T.** (2016), *Characteristic functions of measures on geometric rough paths*, Annals of Probability 44(6)
- **Chevyrev, I. & Kormilitzin, A.** (2016), *A Primer on the Signature Method in Machine Learning*, arXiv:1603.03788
- **Kiraly, F. & Oberhauser, H.** (2019), *Kernels for sequentially ordered data*, JMLR
- **Lyons, T. J., Ni, H., Zhang, H.** (2019), *Machine Learning Models of Financial Time Series*, arXiv:1905.11666
- **Gatheral, J., Jaisson, T., Rosenbaum, M.** (2018), *Volatility is rough*, Quantitative Finance 18(6)
- **Friz & Victoir** (2010), *Multidimensional Stochastic Processes as Rough Paths*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/03-log-signature-and-lie-algebra|03 · Log-Signature & Uniqueness]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Index Hub]]
- Forward / applications: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/02-rnns-and-lstms|RNNs & LSTMs]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman]]
- Sibling / theory: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Rough Volatility]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Quantitative Risk]]
