---
title: "01 — Path Signatures from Zero: Why a Path Is More Than Its Endpoint"
tags:
  - pillar-derivative-pricing
  - path-signatures-and-rough-paths
  - intuition
  - iterated-integrals
  - signature
---

**Basic Prerequisites:** none beyond the idea of a curve and an integral (this page stands alone). The formal machinery begins at [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/02-the-signature-algebra|02 · The Signature Algebra]].

---

### 1. Intuition & Practical Objective

A time series is a **path** — a curve through a state space, drawn between a start time and an end time. The most naive summary of that path is its **endpoint**: where it *ended*. For a stock, that is the close price; for vol, the current level. This page is built on one idea, stated as a challenge:

> **The endpoint throws away almost everything. The signature is the systematic upgrade — an ordered, infinitely-deep hierarchy of summaries in which level 1 is the endpoint, level 2 is the *area swept* between coordinates (the shape of the loop), level 3 is the signed volume, and so on, such that the full collection recovers the path up to a harmless reparametrisation.**

Why finance should care: nearly every derivative contract is a **path-dependent functional** — an Asian depends on the whole average, a barrier on whether the path crossed a level, a variance swap on the integral of squared increments, a cliquet on a sequence of forward returns. The signature is the natural *coordinate system* for all of them: by a theorem (Lyons; §03) continuous path-functionals can be approximated as linear combinations of signature terms. Before any algebra, you need to *feel* the hierarchy, and that is the whole job of this page.

Three intuitions to carry out:

1. **Level 1 is the increment — it cannot see shape.** The integral $\int dX$ is just $X_T-X_0$. Two paths that begin and end identically are indistinguishable at level 1 no matter how different their shapes.
2. **Level 2 is the area — it sees the loop.** The double integral $\int\int_{s<t} dX^i_s dX^j_t$ encodes, through its antisymmetric part, the **oriented area** swept between coordinates $i$ and $j$. This is where "the path went clockwise around the loop" first registers. For two assets, the level-2 cross terms are literally the covariance structure of the increments — this is why the signature, not the endpoint, is the object an ML model should consume (§05–§06).
3. **Levels 1, 2, 3, … are a real hierarchy.** Information that is *invisible* at level $k$ routinely becomes visible at level $k+1$. The signature is only "complete" in the limit; the depth you need is set by the question you ask.

The practical objective: be able to look at a path and know which *level* of its signature answers your question, and to appreciate that the signature is a **lossless-in-the-limit** summary rather than an arbitrary set of hand-picked features.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The hierarchy of iterated integrals

Let $X:[0,T]\to\mathbb R^d$ be a path of bounded variation (for now — roughness is handled in §04). Write its coordinates $X^1,\dots,X^d$. The **signature** of $X$ is the collection of all iterated integrals, indexed by *words* $w=i_1\cdots i_k$ over the alphabet $\{1,\dots,d\}$:

$$
S^{i_1\cdots i_k}_{0,T}(X)=\int_{0<t_1<\cdots<t_k<T}dX^{i_1}_{t_1}\cdots dX^{i_k}_{t_k},\qquad S^{\emptyset}_{0,T}=1.
$$

Level $k$ (the word has $k$ letters) lives in the $k$-fold tensor power $(\mathbb R^d)^{\otimes k}$; collecting all levels gives an element of the tensor algebra. The ordering $0<t_1<\cdots<t_k$ is what makes the hierarchy *hierarchical*: you integrate level-$k$ information against more of the path to get level $k+1$.

#### 2.2 Why level 1 is blind and level 2 is not

Level 1 is immediate: $S^{i}_{0,T}=\int_0^T dX^i_t=X^i_T-X^i_0$ — a single number per coordinate, the endpoint (for a path starting at the origin). Level 2 splits into symmetric and antisymmetric parts:

$$
S^{ij}_{0,T}=\underbrace{\tfrac12 S^iS^j}_{\text{symmetric, from level 1}}+\underbrace{\tfrac12\big(S^{ij}-S^{ji}\big)}_{\text{antisymmetric, the area}}.
$$

The **Lévy area** $\tfrac12(S^{ij}-S^{ji})$ is exactly the oriented area swept by the path between coordinates $i$ and $j$ (Green's theorem). It is *not* recoverable from the endpoint — the loop that returns to its start has $S^i=0$ yet carries arbitrary area. This is the cleanest demonstration that the signature is a genuinely higher-order object.

#### 2.3 Same endpoints, different path — where each level fails

A one-parameter family of shapes all share their endpoints; each successive level of the signature is the "next" invariant that tells them apart. §3 makes this numerical: two paths with identical level-1 *and* identical level-2 signatures are still separated at level 3. The moral: **truncating the signature at level $N$ is a real modelling choice** — it commits you to seeing only the shape features of depth $\le N$.

---

### 3. Computational Implementation — the endpoint, the area, and the depth of the hierarchy

We compute iterated integrals of piecewise-linear paths **by explicit sums** (exact, no simulation): level 1 is a sum of increments; level 2 is $\sum_{k<l}\Delta^i_k\Delta^j_l+\tfrac12\sum_k\Delta^i_k\Delta^j_k$ (the half-diagonal term is the within-segment contribution); level 3 is the analogous triple sum. Stdlib only, deterministic.

```python
import math
def increments(X):
    d=len(X[0]); n=len(X)-1
    return [[X[k+1][i]-X[k][i] for i in range(d)] for k in range(n)], d, n
def lev1(X):
    inc,d,n=increments(X); return [sum(inc[k][i] for k in range(n)) for i in range(d)]
def lev2(X):
    inc,d,n=increments(X); S=[[0.0]*d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            s=0.0
            for k in range(n):
                for l in range(k+1,n): s+=inc[k][i]*inc[l][j]
            for k in range(n): s+=0.5*inc[k][i]*inc[k][j]
            S[i][j]=s
    return S
def area(X):
    S=lev2(X); return 0.5*(S[0][1]-S[1][0])

# two 2D paths, same start (0,0) and same end (3,3), different shapes
P=[(0.0,0.0),(3.0,0.0),(3.0,3.0)]   # go right, then up
Q=[(0.0,0.0),(0.0,3.0),(3.0,3.0)]   # go up, then right
print("Two paths, SAME start (0,0) and SAME end (3,3):")
print("  P = (0,0)->(3,0)->(3,3)   (right, then up)")
print("  Q = (0,0)->(0,3)->(3,3)   (up, then right)")
print("  level-1 signature (endpoint only):  P S1 = %s   Q S1 = %s   (identical!)"%(
    [round(v,1) for v in lev1(P)],[round(v,1) for v in lev1(Q)]))
print("  level-1 signature S11 = 0.5*(endpoint)^2:  P = %.2f   Q = %.2f   (still identical!)"%(
    0.5*(lev1(P)[0]**2),0.5*(lev1(Q)[0]**2)))
print("  Lévy area  A = (S^12 - S^21)/2:  P = %+.2f   Q = %+.2f   (NOW they differ)"%(
    area(P),area(Q)))

# a third path that returns to the start: a closed loop — level 1 is zero, area is not
R=[(0.0,0.0),(3.0,0.0),(3.0,3.0),(0.0,3.0),(0.0,0.0)]
print("\nClosed loop R = (0,0)->(3,0)->(3,3)->(0,3)->(0,0):")
print("  level-1 S1 = %s  (endpoint = start: all zero)"%[round(v,1) for v in lev1(R)])
print("  but Lévy area = %+.2f  (the loop carries a signed area, invisible to level 1)"%area(R))
print("  and level-2 S2[0][1] = %.2f,  S2[1][0] = %.2f"%(
    lev2(R)[0][1],lev2(R)[1][0]))

# the hierarchy: level 3 adds signed volume / second-order shape
def lev3(X):
    inc,d,n=increments(X); S=[[[0.0]*d for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            for k in range(d):
                s=0.0
                for a in range(n):
                    for b in range(a+1,n):
                        for c in range(b+1,n): s+=inc[a][i]*inc[b][j]*inc[c][k]
                for a in range(n):
                    for c in range(a+1,n): s+=0.5*inc[a][i]*inc[a][j]*inc[c][k]
                for a in range(n):
                    for b in range(a+1,n): s+=0.5*inc[a][i]*inc[b][j]*inc[b][k]
                for a in range(n): s+=(1.0/6.0)*inc[a][i]*inc[a][j]*inc[a][k]
                S[i][j][k]=s
    return S
# two different paths that share the SAME endpoint AND the SAME Lévy area
U=[(0.0,0.0),(2.0,0.0),(2.0,3.0),(0.0,3.0)]          # square, area +? 
V=[(0.0,0.0),(3.0,0.0),(1.0,3.0),(0.0,3.0)]          # different shape, area ?
print("\nLevel 3 separates paths that level 2 cannot (U and V have IDENTICAL lev1 AND lev2):")
for name,Xp in (("U",U),("V",V)):
    print("  %s:  S1=%s  area=%+.2f  S^112=%+.3f  S^122=%+.3f"%(
        name,[round(v,1) for v in lev1(Xp)],area(Xp),lev3(Xp)[0][1][1],lev3(Xp)[0][1][1]))
```
```
Two paths, SAME start (0,0) and SAME end (3,3):
  P = (0,0)->(3,0)->(3,3)   (right, then up)
  Q = (0,0)->(0,3)->(3,3)   (up, then right)
  level-1 signature (endpoint only):  P S1 = [3.0, 3.0]   Q S1 = [3.0, 3.0]   (identical!)
  level-1 signature S11 = 0.5*(endpoint)^2:  P = 4.50   Q = 4.50   (still identical!)
  Lévy area  A = (S^12 - S^21)/2:  P = +4.50   Q = -4.50   (NOW they differ)

Closed loop R = (0,0)->(3,0)->(3,3)->(0,3)->(0,0):
  level-1 S1 = [0.0, 0.0]  (endpoint = start: all zero)
  but Lévy area = +9.00  (the loop carries a signed area, invisible to level 1)
  and level-2 S2[0][1] = 9.00,  S2[1][0] = -9.00

Level 3 separates paths that level 2 cannot (U and V have IDENTICAL lev1 AND lev2):
  U:  S1=[0.0, 3.0]  area=+6.00  S^112=+9.000  S^122=+9.000
  V:  S1=[0.0, 3.0]  area=+6.00  S^112=+10.500  S^122=+10.500
```

**Reading the output.**

- **The endpoint is blind.** P and Q have identical level-1 signatures $S^1=[3,3]$ (and therefore identical $S^{11}=4.5$) yet are completely different paths — one goes right then up, the other up then right.
- **The area is the first shape detector.** Their **Lévy areas** are $+4.5$ and $-4.5$: the orientation of the loop is reversed. Green's theorem turns this into the signed area between the curve and its chord, and it is *antisymmetric* (swapping coordinates flips the sign) — exactly the kind of invariant a covariance-blind endpoint summary can never produce.
- **A closed loop has zero endpoint but full area.** The loop R starts and ends at the origin, so $S^1=[0,0]$; yet its area is $+9$ and its level-2 matrix is $S^{12}=9$, $S^{21}=-9$. If all you look at is "where did it end," you have missed the entire loop — which is the entire payoff of a barrier or a variance swap.
- **The hierarchy is real: level 3 sees what level 2 cannot.** U and V share the *entire* level-1 *and* level-2 signature ($S^1=[0,3]$, area $+6$, all of $S^2$) — you literally cannot tell them apart at depth 2 — yet their level-3 integrals $S^{112}$ differ ($9.000$ vs $10.500$). The shape difference between "bulge on the right" and "bulge on the left" lives one level higher. This is why the signature is an *infinite* object: there is always one more level of shape.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The close price is the signal."** For path-dependent payoffs ([[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Exotic & Path-Dependent Options]]) the endpoint is the *least* informative scalar in the whole hierarchy — a barrier cares about the maximum, an Asian about the average, a variance swap about the increments. Level 1 is the right answer only when the payoff is genuinely $F(S_T)$.
2. **Using a 1D signature on univariate data.** A single coordinate has *no area*: $S^{11}=\tfrac12(S^1)^2$ is a function of the endpoint, so the raw 1D signature is the endpoint in disguise. The fix (time augmentation, lead-lag) is the subject of [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/05-failure-modes-and-practice|05 · Failure Modes & Practice]].
3. **Stopping at level 2 "because the area is the interesting bit."** As the U/V example shows, depth-2-identical paths separate at depth 3. The level you need is set by the *question*; a truncated signature is a deliberate approximation with a measurable information price.
4. **Reading the signed area as an unsigned shape measure.** The Lévy area is *oriented*: $+4.5$ and $-4.5$ are opposite orientations, and for assets this orientation is exactly the sign of the cross-covariance (lead vs lag matters, §05). Symmetrising it away discards the signal.

---

### 5. Canonical Literature & Study References

- **Chevyrev & Kormilitzin** (2016), *A Primer on the Signature Method in Machine Learning*, arXiv:1603.03788 — §2–3: the iterated-integral hierarchy, the area interpretation, and the first worked examples. *The primary applied reference for this page.*
- **Lyons** (1998), *Differential equations driven by rough signals*, Rev. Mat. Iberoamericana 14(2) — §2: the signature as the natural object, motivation from the endpoint-only failure.
- **Hambly & Lyons** (2010), *Uniqueness for the signature of a path of bounded variation and the reduced path group*, Annals of Mathematics 171 — the formal statement that the *whole* signature (not any truncation) determines the path; the mathematical target that the hierarchy is converging to.
- **Friz & Victoir** (2010), *Multidimensional Stochastic Processes as Rough Paths*, Ch 1–2 — the analytic foundations of iterated integrals over irregular paths. *Math-verified.*

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Continue: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/02-the-signature-algebra|02 · The Signature Algebra]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/03-lookbacks-and-asians|Lookbacks & Asians]] (payoffs that *are* path functionals) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
