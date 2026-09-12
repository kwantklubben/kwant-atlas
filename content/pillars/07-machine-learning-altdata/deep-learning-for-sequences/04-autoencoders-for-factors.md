---
title: "7.6.4 Autoencoders for Factor Extraction"
tags:
  - pillar-machine-learning
  - deep-learning-for-sequences
  - autoencoders
  - factor-extraction
  - dimensionality-reduction
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/01-from-zero-intuition|01 · From Zero]] and [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (factor construction). A working knowledge of PCA helps - the central result is that the *linear* autoencoder **is** PCA.

---

### 1. Intuition & Practical Objective

An **autoencoder** learns to copy its input through a narrow bottleneck: it compresses $x$ to a short code $z$ (the **encoder**) and reconstructs $x$ from $z$ (the **decoder**). If the bottleneck is smaller than the input, the network cannot copy verbatim - it is *forced* to keep only the structure that explains most of the variation. That structure is exactly a **factor model**: the code $z$ is a handful of latent factors, and the decoder is the loading matrix.

Two "aha"s:

1. **Compression is a definition of "factor".** A good factor is a low-dimensional summary that reconstructs the data. An autoencoder's training objective - minimise reconstruction error - is precisely the factor-extraction objective, learned by gradient descent instead of eigen-decomposition.
2. **The linear autoencoder is PCA, exactly.** This is the honest punchline of the page: below a bottleneck dimension $k$, a linear autoencoder's optimum *is* the rank-$k$ PCA subspace (Eckart–Young / Baldi–Hornik). Nonlinearity is what buys you something PCA cannot - curved manifolds, sparse codes, denoising - and *that* is where the deep-learning content actually lives.

The practical objective: build factors with an autoencoder, and know exactly how much of the gain is real (nonlinearity) versus a reparametrisation of PCA (nothing).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The autoencoder objective

With encoder $E:\mathbb R^d\to\mathbb R^k$ and decoder $D:\mathbb R^k\to\mathbb R^d$, the reconstruction loss over $n$ samples is

$$
\boxed{\;\mathcal L(E,D)=\frac1n\sum_{i=1}^{n}\big\|x_i-D\big(E\,x_i\big)\big\|_2^2\;}
$$

For a **linear** autoencoder, $E\in\mathbb R^{k\times d}$, $D\in\mathbb R^{d\times k}$, and (absorbing the optimum) $DE$ is the orthogonal projector onto a $k$-dimensional subspace. The optimal subspace is given by the SVD. Write the centred data matrix $X=U\Sigma V^\top$ (economy SVD). Then the **Eckart–Young theorem** says the best rank-$k$ approximation is

$$
\hat X_k=U_k\Sigma_k V_k^\top,
$$

attained when $E=V_k^\top$ (rows $=$ top-$k$ right singular vectors, the principal directions) and $D=V_k$. Hence:

> **Theorem (Baldi & Hornik 1989).** A linear autoencoder with bottleneck $k$ trained to global optimality recovers the top-$k$ PCA subspace. Its reconstruction error equals the PCA error: $\mathcal L^\star=\tfrac1n\sum_{j>k}\sigma_j^2$ (mean squared error over the discarded singular values), which is $0$ when the data is exactly rank-$k$.

So a linear autoencoder is a *neural re-implementation of PCA*; the weights are a rotation of the principal directions, and the codes are the principal-component scores up to that rotation.

#### 2.2 What nonlinearity adds

Replacing linear maps with nonlinearities $z=\phi(W_e x+b_e)$, $\hat x=\psi(W_d z+b_d)$ lets the model represent a **curved** low-dimensional manifold - a set of latent factors that mix multiplicatively, not just additively. The gains over PCA are real but come at a cost:

- **Sparse autoencoder** - add an $L_1$ penalty: $\mathcal L+\lambda\|z\|_1$. Most code units are driven to exactly $0$, so each factor is "on" for few inputs (interpretable, regime-like factors).
- **Denoising autoencoder** - train to reconstruct $x$ from a corrupted $\tilde x$; the code must capture structure robust to noise, which suits the low-SNR financial regime.
- **Undercomplete vs overcomplete** - a bottleneck smaller than $d$ forces compression (the factor view); a bottleneck *larger* than $d$ requires a sparsity or noise penalty to avoid the identity function (the dictionary-learn view).
- **VAE** - a probabilistic autoencoder that learns a latent *distribution* $q(z\mid x)$ and can generate/sample; the bridge to latent-factor risk models with uncertainty.

For factors specifically, the encoding step is the *unsupervised* counterpart of [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|supervised factor ranking]]: it finds structure in $X$ without ever seeing a label, which is either a strength (no target leakage) or a weakness (unrelated to the return you care about) depending on the task.

---

### 3. Computational Implementation - a linear autoencoder in numpy, checked against PCA

`numpy` only. We build data with a rank-$3$ factor structure **plus noise** in $10$ dimensions, compute the PCA rank-$3$ reconstruction error (the theoretical optimum), train a linear autoencoder $10\to3\to10$ by gradient descent, and show the two agree.




Read it as the theorem verified. The trained autoencoder's reconstruction error is **$0.1714$**, identical (to $0.000\%$) to the PCA optimum, and the three principal angles between the learned encoder subspace and the PCA subspace are all $\cos=1.0$ - the subspaces are **the same subspace**. The autoencoder was not a better factor model than PCA; it was a slower, gradient-trained *re-derivation* of it. That is the honest baseline you must beat with a nonlinear autoencoder before claiming any deep-learning gain.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"My autoencoder beat PCA" (it didn't).** With linear layers and no regularisation, the two coincide (verified above). Any apparent improvement is (a) not converged, (b) a nonlinearity you forgot you added, or (c) noise in the comparison. Always report the PCA baseline.
2. **Best reconstruction ≠ best factor.** The objective minimises *variance* reconstruction. A factor that is statistically loud may be *financially irrelevant*; autoencoders are unsupervised and know nothing about returns. Pair them with a supervised check (→ [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|tree-based factor ranking]]).
3. **Overcomplete autoencoders memorise.** If the bottleneck is $\ge d$ and there is no sparsity/denoising penalty, the network learns the identity (zero error, zero information). The bottleneck must be *smaller* or *regularised*.
4. **Factors drift.** Loadings fit on one period may no longer describe another (non-stationarity); a factor model is a *stationary* assumption (recall page 05's regime shift). Refit on a rolling window and monitor.
5. **PCA-of-returns recovers noise in the low-SNR regime.** With a weak signal, the top principal components of *features* are dominated by common noise unless the features are cleaned (standardise, sector-neutralise, fractionally differentiate). See [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering]].
6. **A domain caveat on the source.** *Advances in Financial Machine Learning* (López de Prado 2018) is often cited for "autoencoder factors", but AFML contains **no autoencoder chapter** - its deep-learning content is absent by design (Ch. 1 explicitly declines to cover deep/recurrent/convolutional nets), and its Ch. 19 is "Microstructural Features". The autoencoder canon here is Goodfellow et al. Ch. 14 and the finance application of Heaton, Polson & Witte (2017).

---

### 5. References

- **Goodfellow, Bengio & Courville**, *Deep Learning*, **Ch. 14 "Autoencoders"**
- **Baldi, P. & Hornik, K.** (1989), *Neural Networks and Principal Component Analysis: Learning from Examples Without Local Minima*, Neural Networks 2(1):53–58
- **Eckart, C. & Young, G.** (1936), *The Approximation of One Matrix by Another of Lower Rank*
- **Heaton, J.B., Polson, N.G. & Witte, J.H.** (2017), *Deep learning for finance: deep portfolios*, Applied Stochastic Models in Business and Industry 33(1):3–12
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, **Ch. 14.5** (PCA as the best rank-$q$ linear manifold, model eq. 14.49, objective eq. 14.50, SVD eq. 14.54)
- **Hinton, G. & Salakhutdinov, R.** (2006), *Reducing the Dimensionality of Data with Neural Networks*, Science

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/03-attention-and-transformers|03 · Attention & Transformers]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Supervised counterpart: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
- Feature inputs the encoder consumes: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]]
- Low-SNR reality check: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
