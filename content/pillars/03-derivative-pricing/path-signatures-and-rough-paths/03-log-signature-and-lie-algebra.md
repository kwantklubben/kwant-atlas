---
title: "3.15.3 The Log-Signature, the Free Lie Algebra & Signature Uniqueness"
tags:
  - pillar-derivative-pricing
  - path-signatures-and-rough-paths
  - log-signature
  - free-lie-algebra
  - levy-area
  - signature-uniqueness
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/02-the-signature-algebra|02 · The Signature Algebra]] (Chen's identity and the shuffle product) and [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|Linear Algebra · 02 Vectors, Spaces & Matrices]].

---

### 1. Intuition & Practical Objective

The signature is a *huge* object - at level $k$ it has $d^k$ components, and level $k+1$ contains most of the information of level $k$ plus a little more. Two questions naturally follow, and they are the subject of this page:

1. **Compression: what is the smallest faithful summary?** Because Chen's identity makes the signature a *group-like* element, its **logarithm** - the **log-signature** - exists and retains only the genuinely independent shape information. At level 2 the log-signature is just the **Lévy area** (antisymmetric), at level 3 a pair of iterated brackets, and so on. In general it is a **Lie element** of the **free Lie algebra** - the "causality-free" core of the path, with the shuffle-redundant part stripped away.
2. **Uniqueness: does the signature determine the path?** The **Lyons signature uniqueness result** says *yes, up to the genuinely irrelevant information*: two paths with the same signature differ only by a **reparametrisation** (or, for rough paths, by a **tree-like** path - Boedihardjo et al.). The signature is therefore a *faithful* coordinate system: nothing about the geometry is lost, and nothing irrelevant is kept.

Two practical consequences drive the page:

3. **The log-signature is the compression you actually ship to a model.** The full signature carries shuffle-redundant coordinates (products of lower terms); the log-signature is the *minimal* basis - the same descriptive power with far fewer, mutually independent features. This is the standard pre-processing step in [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/06-advanced-extensions|signature-based machine learning]].
4. **Reparametrisation invariance is a feature, not a bug.** The signature (and log-signature) does not care how fast the path is traversed - it cares about the *route*. For geometric shape features this is ideal; it only becomes a problem when the *timing* of events is itself the signal, which is exactly what lead-lag reintroduces (§05).

The practical objective: be able to compute the log-signature from the signature by the tensor-algebra power series, verify the free-Lie-algebra (primitive) structure numerically, and state precisely the uniqueness theorem - including its *contrapositive* for distinct non-reparametrised paths.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The log-signature as a tensor-algebra series

The signature $S=S(X)\in T((\mathbb R^d))$ is an element with constant term $1$. Its **log-signature** is

$$
\ell(X)=\log S(X)=\sum_{n\ge1}\frac{(-1)^{n+1}}{n}(S-1)^{\otimes n},
$$

where $\otimes$ is the *concatenation* (tensor) product and $\log$ is the formal power-series logarithm of an associative algebra with unit. Truncated at level 3, the components are

$$
\ell^{i}=S^{i},\qquad \ell^{ij}=S^{ij}-\tfrac12 S^iS^j,\qquad \ell^{ijk}=S^{ijk}-\tfrac12\big(S^iS^{jk}+S^{ij}S^k\big)+\tfrac13 S^iS^jS^k,
$$

with all sums over *prefix/suffix* splits of the word (the tensor-algebra structure - see §3). Level 2 gives the **Lévy area matrix**, which is *antisymmetric*:

$$
\ell^{ij}=\tfrac12\big(S^{ij}-S^{ji}\big),\qquad \ell^{ij}=-\ell^{ji}.
$$

#### 2.2 Why the log-signature is a Lie element

A fundamental structural result (Lyons; Reutenauer) is that $\ell(X)$ is a **primitive / Lie element**: each level-$k$ piece lies in the degree-$k$ part of the **free Lie algebra** $\mathrm{Lie}(\mathbb R^d)$. Concretely, for $d=2$ and degree 3, the free Lie algebra has the left-nested bracket basis

$$
[1,[1,2]]=e_{112}-2e_{121}+e_{211},\qquad [2,[1,2]]=2e_{212}-e_{221}-e_{122},
$$

so a degree-3 tensor is a Lie element **iff** it is in the span of these two - a set of linear coefficient relations that can be checked numerically (and is, in §3). The content of this structure: the log-signature is the *minimal* non-redundant summary - all shuffle products of lower terms have been removed, so its components are genuinely independent. The number of independent degree-$k$ components of the log-signature (dimension of the free Lie algebra) is, by Witt's formula, $\frac1k\sum_{d'|k}\mu(d')\,d^{k/d'}$ - far smaller than $d^k$.

#### 2.3 Signature uniqueness (Lyons; Hambly–Lyons; Boedihardjo et al.)

The **Lyons uniqueness theorem** states: if two paths $X,Y$ of finite $p$-variation satisfy $S(X)=S(Y)$, then they are **tree-equivalent** - i.e. $Y$ is obtained from $X$ by a reparametrisation composed with the addition of a **tree-like path** (a path whose signature is the identity). For bounded-variation paths, Hambly & Lyons (2010) prove the stronger statement that the signature map is **injective on the reduced path group**: the signature determines the path *up to reparametrisation only* (no tree-like ambiguity survives in that class). For genuinely rough paths the uniqueness is established by Boedihardjo, Geng, Lyons & Yang (2016).

The practical reading is the contrapositive, which §3 verifies: **if two paths are not reparametrisations of each other, their signatures differ.** And the constructive content of the theorem is *reparametrisation invariance* - $S(X\circ\varphi)=S(X)$ for any monotone $\varphi$ - which is also verified directly.

---

### 3. Computational Implementation - the log-signature, its Lie structure, invariance, and uniqueness

We (i) build the log-signature to level 3 by the tensor-algebra series from the exact iterated integrals, (ii) verify the level-2 antisymmetry and the level-3 free-Lie-algebra coefficient relations, (iii) verify reparametrisation invariance by collinear subdivision, and (iv) verify the uniqueness contrapositive on two distinct non-reparametrised paths. Stdlib only, deterministic.




**Reading the output.**

- **The log-signature is a Lie element, verified at degree 2 and 3.** Level 2 is exactly antisymmetric ($L^{12}=-0.5$, $L^{21}=+0.5$, residual $0$) - i.e. the Lévy area, an element of $\wedge^2\mathbb R^2=\mathrm{Lie}_2(\mathbb R^2)$. Level 3 satisfies *all five* coefficient relations defining the free Lie algebra basis $\{[1,[1,2]],[2,[1,2]]\}$ to $\sim10^{-15}$ ($L^{111}=L^{222}=0$, $L^{121}=-2L^{112}$, etc.). The log-signature is provably not an arbitrary tensor - it lives in the minimal non-redundant Lie subspace, with $L_3=a[1,[1,2]]+b[2,[1,2]]$, $a=-37/12$, $b=-8/3$.
- **Reparametrisation invariance holds to machine precision.** Subdividing each segment into 2, 3, or 5 collinear pieces changes the path only by a *reparametrisation* (more breakpoints on the same route); the signature is unchanged to $\sim10^{-14}$ at level 3. This is the flip side of uniqueness: the signature is blind to the *speed* of traversal.
- **Uniqueness's contrapositive is real.** P and Q share their endpoints yet are not reparametrisations of each other (opposite orientations), and their signatures differ - the areas are $+4.50$ and $-4.50$. A signature that agreed would force a reparametrisation/tree-like relation, which these paths do not have.
- **The compression is dramatic.** $d=2$, degree 3: the signature has $2^1+2^2+2^3=14$ components; the log-signature has $\dim\mathrm{Lie}=2+1+2=5$ (Witt's formula). The log-signature is the *shuffle-redundancy-free* core - the reason it, not the full signature, is what an ML pipeline consumes (§06).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Computing the log-signature with the wrong product.** The tensor-algebra log uses *prefix/suffix (concatenation)* splits of words - only 2 proper splits at level 3 ($i|jk$, $ij|k$), not the 6 interleavings. Using shuffle splits (or worse, the Itô convention) yields a non-Lie, non-primitive object whose "log-signature" is meaningless. This is the single most common implementation error.
2. **Reading the signature (not the log-signature) as independent features.** The signature carries shuffle-redundant coordinates - $S^{ij}+S^{ji}=S^iS^j$ - so its components are highly collinear. Models fed raw signature features silently re-learn the shuffle relations; the log-signature removes that redundancy by construction.
3. **Forgetting that uniqueness is up to tree-like equivalence.** For rough paths the signature determines the path only up to tree-like ambiguity (Boedihardjo et al. 2016); for bounded-variation paths (Hambly–Lyons) the map is injective on the reduced path group. Claiming "the signature IS the path" overstates the theorem for the genuinely rough case.
4. **Treating reparametrisation invariance as costless.** It is a feature for geometric shape (§1), but if the *timing* of moves is the signal (e.g. the intraday structure of order flow, or the lead-lag in vol), the raw signature discards exactly that information. Lead-lag/time augmentation (§05) is the deliberate re-insertion of time.

---

### 5. Canonical Literature & Study References

- **Lyons, Terry J.** (1998), *Differential equations driven by rough signals*, Rev. Mat. Iberoamericana 14(2) - the signature group, group-likeness, the log-signature and its Lie-algebra structure; the uniqueness result. *Primary math-verified source.*
- **Hambly, B. & Lyons, T.** (2010), *Uniqueness for the signature of a path of bounded variation and the reduced path group*, Annals of Mathematics 171(1), 109–167 - injectivity of the signature on the reduced path group. *The sharp bounded-variation uniqueness.*
- **Boedihardjo, H., Geng, X., Lyons, T., Yang, D.** (2016), *The signature of a rough path: uniqueness*, Advances in Mathematics 293, 720–737 - uniqueness for rough paths beyond bounded variation.
- **Reutenauer, C.** (1993), *Free Lie Algebras* (Oxford) - Lyndon words, the bracket basis, Witt's formula, primitives of the tensor algebra. *Math reference for §2.2.*
- **Chevyrev & Kormilitzin** (2016), *A Primer on the Signature Method in Machine Learning*, arXiv:1603.03788 - §4–5: the log-signature as feature compression; the dimension counts. *Primary applied reference.*
- **Friz & Victoir** (2010), *Multidimensional Stochastic Processes as Rough Paths*, Ch 7–9 - the group of rough paths and the log in the free Lie algebra. *Math-verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/02-the-signature-algebra|02 · The Signature Algebra]]
- Forward: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/04-rough-path-theory|04 · Rough Path Theory]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Index Hub]]
- Theory: [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|Linear Algebra · 02 Vectors & Matrices]] (tensor products) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
