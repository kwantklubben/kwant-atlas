---
title: "02 — Vector Spaces, Matrices & the Geometry of Returns"
tags:
  - foundations
  - linear-algebra
  - vector-spaces
  - linear-independence
  - gram-schmidt
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/01-from-zero-intuition|01 · From Zero]] (or high-school vector geometry).

---

### 1. Intuition & Practical Objective

A vector is a *point in space with a meaning attached*: a vector of $N$ returns is one point in $\mathbb{R}^N$, and a matrix is a linear rule that maps vectors to vectors. The practical objective of this page is three precise, non-negotiable ideas the rest of the Atlas leans on: **linear independence** (do my $N$ asset returns genuinely span $N$ directions, or are some just combinations of others?), **basis / dimension** (how many independent risk sources are really there?), and **orthogonality** (which directions carry *uncorrelated* risk). These three words — *independent, spanning, orthogonal* — are the entire grammar of factor models and PCA.

A financial statement of the same idea (Tsay §8–9): if three assets are driven by two macro factors, then their returns lie on a 2-dimensional plane inside $\mathbb{R}^3$ — *linearly dependent*. The **rank** of the matrix of their returns tells you the true number of independent risk drivers. Rank-deficiency is not a mathematical curiosity; it is the *N>T* problem and the collinearity/collateral problem (highly correlated assets, and the same names posted as collateral).

---

### 2. Mathematical Ground Truth & Derivations

**Vector space & inner product.** $\mathbb{R}^n$ with the standard inner product $\langle x,y\rangle=x'y=\sum_i x_i y_i$ is a real vector space. The induced norm (length) is $\|x\|=\sqrt{\langle x,x\rangle}$, and two vectors are **orthogonal** iff $x'y=0$. Orthogonality of returns is exactly *zero covariance* — the reason correlation-structured factor models decompose into independent pieces.

**Linear independence & rank.** Vectors $v_1,\dots,v_k$ are **linearly independent** if the only combination $\sum_j c_j v_j=0$ is the trivial one ($c=0$). The **rank** of a matrix is the number of independent columns (equivalently rows). For a $T\times N$ return matrix, $\text{rank}(X)\le\min(T,N)$ — the seed of the $N>T$ trap: with $T$ observations you can have **at most** $T$ independent columns.

**Basis, dimension, span.** A *basis* is a maximal set of independent vectors; every vector in the space is a unique combination of them. **Dimension** = size of any basis = rank. Orthogonal projections and regression are both "find the best combination of basis vectors."

**Gram–Schmidt.** Any set of independent vectors can be turned into an orthonormal basis by subtracting, from each new vector, its projections onto the already-orthonormal ones:

$$q_k=\frac{v_k-\sum_{j<k}\langle v_k,q_j\rangle\,q_j}{\big\|v_k-\sum_{j<k}\langle v_k,q_j\rangle\,q_j\big\|}.$$

This is the *algorithm* behind $QR$ and the geometric meaning of "de-correlating" a set of signals (Glasserman Ch 2's Cholesky does the same thing numerically for random variables).

---

### 3. Computational Implementation — Gram–Schmidt finds the true dimension

Implementing Gram–Schmidt from scratch shows linear dependence directly: a dependent vector's residual has zero norm and is **dropped**, so the number of orthonormal vectors that survive *is the rank*. Stdlib only.

```python
import math

def dot(u, v): return sum(a*b for a, b in zip(u, v))
def norm(u):   return math.sqrt(dot(u, u))

def gram_schmidt(vectors):
    """Return an orthonormal basis for span(vectors); drops linearly dependent vectors."""
    basis = []
    for v in vectors:
        w = [float(a) for a in v]
        for q in basis:                       # remove the component already spanned by q
            w = [w[i] - dot(v, q)*q[i] for i in range(len(v))]
        n = norm(w)
        if n > 1e-12:                          # independent: keep, normalize
            basis.append([a/n for a in w])
    return basis

# (a) three independent vectors -> 3 orthonormal vectors, Q'Q = I
q = gram_schmidt([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]])
print(f"independent set:   {len(q)} orthonormal basis vectors")
print(f"Q'Q = {[[round(dot(q[i],q[j]),10) for j in range(len(q))] for i in range(len(q))]}")

# (b) a dependent set (v3 = v1 + v2) -> rank 2, the third is dropped
qd = gram_schmidt([[1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [2.0, 1.0, 1.0]])
print(f"dependent set:     {len(qd)} orthonormal basis vectors  (rank = 2, < 3)")
```
```
independent set:   3 orthonormal basis vectors
Q'Q = [[1.0, 0.0, 0.0], [0.0, 1.0, -0.0], [0.0, -0.0, 1.0]]
dependent set:     2 orthonormal basis vectors  (rank = 2, < 3)
```
The dependent set collapses to **rank 2** because its third vector was just a combination of the first two — the same collapse happens when three assets are driven by two factors. `rank(X)` *is* the number of independent risk sources, and this is the first-principles root of why an $N>T$ covariance matrix has rank $\le T$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Collinearity is rank-deficiency in disguise.** Two perfectly correlated assets are dependent columns; their combination has no unique solution in regression ($X'X$ becomes singular). This is the linear-algebra form of the "multicollinearity" a risk book hits before a singular-matrix crash.
2. **Rank is bounded by both $T$ and $N$.** With $T=250$ daily returns you cannot have more than 250 independent columns even with $N=500$ assets. Believing a $500\times500$ sample covariance is full-rank is the *N>T* trap ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]).
3. **Orthogonality is not absence of dependence in finite samples.** Two sample-orthogonal return vectors have zero *estimated* covariance but can be strongly dependent through higher moments or shared latent factors; Gram–Schmidt de-correlates only in the linear sense.

---

### 5. Canonical Literature & Study References

- **Strang**, *Introduction to Linear Algebra* (5th ed.), Ch 1 (vectors), Ch 3 (spaces, independence, basis, dimension), Ch 4 (orthogonality, Gram–Schmidt, $QR$). *Corpus PDF available.*
- **Tsay**, *Analysis of Financial Time Series*, §9.4 (PCA as orthogonal dimension reduction), §9.5 (factor model with $m$ latent drivers — rank structure). *Verified.*
- **Horn & Johnson**, *Matrix Analysis*, Ch 0–1 (vector spaces, inner products, rank inequalities).

---

### 6. Connected Graph Bridges

- Back: [[foundations/linear-algebra-and-matrices/01-from-zero-intuition|01 · From Zero]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Continue: [[foundations/linear-algebra-and-matrices/03-linear-systems-and-decompositions|03 · Linear Systems & Decompositions]] · [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]] · [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05 · SVD, PCA & Regression]]
- Forward: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]] (cointegration = rank structure of a shared trend) · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]] (clustering as structure on a correlation graph)
