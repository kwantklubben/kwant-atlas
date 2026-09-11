---
title: "3.15.2 The Signature Algebra"
tags:
  - pillar-derivative-pricing
  - path-signatures-and-rough-paths
  - chens-identity
  - shuffle-product
  - iterated-integrals
  - tensor-algebra
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/01-from-zero-intuition|01 · From Zero]] and [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|Itô Integral & Itô's Lemma]]. The tensor-algebra background is [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|Linear Algebra · 02 Vectors, Spaces & Matrices]].

---

### 1. Intuition & Practical Objective

The signature is an infinite family of numbers, and an infinite family of numbers is only useful if it has *structure* — laws that let you manipulate it without computing every entry. The signature has exactly two structural laws, and they are the entire subject of this page:

1. **Chen's identity** — the signature *factorises* when you concatenate paths. If $X$ is $X^{(1)}$ followed by $X^{(2)}$, then the signature of the whole is the **tensor product** of the signatures of the parts. This is what makes the signature **recursive and fast**: any iterated integral over a long path is a finite combination of integrals over its pieces.
2. **The shuffle product identity** — the *product* of two signature terms is the signature of the *shuffle* of their words. This is what makes the signature **algebraically closed**: products of iterated integrals are again (linear combinations of) iterated integrals. It is the reason the signature can be a coordinate system for continuous path-functionals: the pointwise product of two functionals is represented by the shuffle product of their signature expansions.

Two consequences previewed here, developed later:

3. **The log-signature.** Chen's identity makes the signature a *group-like* element, so its *logarithm* exists and lands in the free Lie algebra — the compressed "only the independent shape information" version (§03).
4. **Universality.** Because products of signature terms close under the shuffle product, the linear span of signature functionals is closed under pointwise multiplication — the seed of the *universality* theorem that makes signatures the right feature space for [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/06-advanced-extensions|signature-based machine learning]] (§06).

The practical objective: be able to (a) state Chen's identity and the shuffle identity precisely, (b) verify both numerically by direct computation, and (c) use them to compute signatures of long paths from pieces, and to recognise that products of features stay inside the feature space.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Chen's identity

Let $X^{(1)}$ and $X^{(2)}$ be two paths, and $X=X^{(1)}\ast X^{(2)}$ their concatenation (run $X^{(1)}$, then $X^{(2)}$ shifted to start where $X^{(1)}$ ended). Then, in the tensor algebra $T((\mathbb R^d))$,

$$
\boxed{\;S(X^{(1)}\ast X^{(2)})=S(X^{(1)})\otimes S(X^{(2)})\;}
$$

i.e. for every word $w$,

$$
S^w(X^{(1)}\ast X^{(2)})=\sum_{uv=w} S^{u}(X^{(1)})\,S^{v}(X^{(2)}),
$$

where the sum runs over all *splits* of $w$ into a prefix $u$ and a suffix $v$ (both possibly empty). The proof is a one-liner: the region $0<t_1<\cdots<t_k<T$ splits, relative to the join point, into a "front part" where some $t$'s lie in $X^{(1)}$'s time and the rest in $X^{(2)}$'s time; the letters in the front part form the prefix $u$ and those in the back part the suffix $v$, and the double region integral separates. Chen's identity is why "compute the signature of a whole path" is never done brute-force: it is assembled from the signatures of its segments (the `S_word` method in §3 is exactly this).

#### 2.2 The shuffle product identity

The **shuffle** of two words $u=i_1\cdots i_a$ and $v=j_1\cdots j_b$, written $u\sqcup v$, is the multiset of all length-$(a+b)$ words that interleave $u$ and $v$ while preserving the internal order of each — so it has $\binom{a+b}{a}$ terms. The second structural law is that *ordinary products of signature coefficients are signature coefficients over shuffles*:

$$
\boxed{\;S^u(X)\,S^v(X)=\sum_{w\in\,u\sqcup v}S^{w}(X)\;}
$$

It follows from Fubini: for geometric (Stratonovich / rough-path) integrals the product of two iterated integrals equals the integral over the product of the ordered simplexes, which decomposes into the disjoint ordered regions indexed by the shuffles. Its practical content: the algebra of signature *features* under pointwise multiplication is closed — a fact with a name, *universality* (the linear span is a dense algebra of continuous functionals, §06).

#### 2.3 The two laws together: group-like structure

Chen's identity says $X\mapsto S(X)$ is a group homomorphism from path-concatenation to the group of group-like elements of the tensor algebra. The shuffle identity says the image is also closed under the shuffle (pointwise) product. The intersection of these two structures is what makes the **log-signature** $\log S(X)$ a **Lie element** (primitive: $\Delta\ell=\ell\otimes1+1\otimes\ell$) — the subject of [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/03-log-signature-and-lie-algebra|03 · Log-Signature & Uniqueness]]. Both laws are identities that can be checked numerically, and §3 checks them to machine precision.

#### 2.4 A caution: which integral convention?

Both laws hold **exactly** for the *geometric* (Stratonovich / rough-path) iterated integrals — i.e. those defined by the explicit Riemann–Stieltjes sums along a piecewise-linear path, which is what our code computes. For **Itô** integrals the shuffle identity *fails* (an Itô-correction term appears at the diagonal). This is the mathematical reason raw (non-augmented) financial data must be **geometricised** by time augmentation or the lead-lag transform before signatures are meaningful (§05). The code below uses the geometric convention throughout, so both identities hold to machine precision.

---

### 3. Computational Implementation — Chen's identity and the shuffle product, verified exactly

We compute iterated integrals of a piecewise-linear path by explicit sums, then verify: (a) **Chen's identity** by splitting a path into two halves and comparing the direct signature with the tensor product of the halves, at levels 2 *and* 3; (b) **the shuffle identity** for representative word pairs; (c) the consistency of a *second, independent* engine (`S_word`, which evaluates any word's integral via Chen's identity across the segments) with the direct sums. Stdlib only, deterministic.

```python
import math

def increments(X):
    d=len(X[0]); n=len(X)-1
    return [[X[k+1][i]-X[k][i] for i in range(d)] for k in range(n)], d, n

def lev1(X):
    inc,d,n=increments(X); return [sum(inc[k][i] for k in range(n)) for i in range(d)]
def lev2(X):                       # exact, piecewise-linear: sum k<l  + 1/2 diag
    inc,d,n=increments(X); S=[[0.0]*d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            s=0.0
            for k in range(n):
                for l in range(k+1,n): s+=inc[k][i]*inc[l][j]
            for k in range(n): s+=0.5*inc[k][i]*inc[k][j]
            S[i][j]=s
    return S
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

def compositions(total,parts):     # nonnegative compositions
    if parts==1: yield (total,); return
    for a in range(total+1):
        for rest in compositions(total-a,parts-1): yield (a,)+rest

def S_word(X,w):                   # ANY word's integral, exact via Chen across segments
    inc,d,n=increments(X); m=len(w); tot=0.0
    for comp in compositions(m,n):
        prod=1.0; idx=0
        for k in range(n):
            c=comp[k]
            if c>0:
                seg=1.0
                for letter in w[idx:idx+c]: seg*=inc[k][letter]
                prod*=seg/math.factorial(c); idx+=c
        tot+=prod
    return tot

def shuffle(a,b):                  # all interleavings preserving order
    if not a: return [b]
    if not b: return [a]
    r=[]
    for w in shuffle(a[1:],b): r.append([a[0]]+w)
    for w in shuffle(a,b[1:]): r.append([b[0]]+w)
    return r

X=[(0.0,0.0),(2.0,0.0),(2.0,3.0),(6.0,1.0),(3.0,2.0)]   # the running demo path
S1=lev1(X); S2=lev2(X); S3=lev3(X)
print("demo path X; level-1 S1=%s" % [round(v,1) for v in S1])
print("level-2 S2 =")
for i in range(2): print("   ",[round(S2[i][j],4) for j in range(2)])

# (0) two independent engines agree
e2=max(abs(S_word(X,[i,j])-S2[i][j]) for i in range(2) for j in range(2))
e3=max(abs(S_word(X,[i,j,k])-S3[i][j][k]) for i in range(2) for j in range(2) for k in range(2))
print("engines agree:  lev2 err=%.0e  lev3 err=%.1e"%(e2,e3))

# (1) Chen's identity at level 2 and 3, splitting X after the 2nd segment
m=2; X1,X2=X[:m+1],X[m:]
a1,a2,a3=lev1(X1),lev2(X1),lev3(X1); b1,b2,b3=lev1(X2),lev2(X2),lev3(X2)
chen2=[[a2[i][j]+a1[i]*b1[j]+b2[i][j] for j in range(2)] for i in range(2)]
chen3=[[[a3[i][j][k]+a2[i][j]*b1[k]+a1[i]*b2[j][k]+b3[i][j][k]
         for k in range(2)] for j in range(2)] for i in range(2)]
print("Chen identity:  lev2 residual = %.0e   lev3 residual = %.1e"%(
    max(abs(chen2[i][j]-S2[i][j]) for i in range(2) for j in range(2)),
    max(abs(chen3[i][j][k]-S3[i][j][k]) for i in range(2) for j in range(2) for k in range(2))))

# (2) shuffle identity: S^u S^v = sum_{w in u shuffle v} S^w
print("shuffle identity (lhs = S^u*S^v, rhs = sum over shuffles):")
for (u,v) in (([0],[1]),([0],[0])):
    lhs=S_word(X,u)*S_word(X,v); rhs=sum(S_word(X,w) for w in shuffle(u,v))
    print("   <S^%s,S^%s>: lhs=%.4f rhs=%.4f  res=%.0e (nterms=%d)"%(u,v,lhs,rhs,abs(lhs-rhs),len(shuffle(u,v))))
for (u,v) in (([0],[1,0]),([0],[0,1])):
    lhs=S_word(X,u)*S_word(X,v); rhs=sum(S_word(X,w) for w in shuffle(u,v))
    print("   <S^%s,S^%s>: res=%.1e (nterms=%d)"%(u,v,abs(lhs-rhs),len(shuffle(u,v))))
for (u,v) in (([0,1],[1,0]),([0,0],[1,1])):
    lhs=S_word(X,u)*S_word(X,v); rhs=sum(S_word(X,w) for w in shuffle(u,v))
    print("   <S^%s,S^%s>: res=%.0e (nterms=%d)"%(u,v,abs(lhs-rhs),len(shuffle(u,v))))
```
```
demo path X; level-1 S1=[3.0, 2.0]
level-2 S2 =
    [4.5, 2.5]
    [3.5, 2.0]
engines agree:  lev2 err=0e+00  lev3 err=8.9e-16
Chen identity:  lev2 residual = 0e+00   lev3 residual = 8.9e-16
shuffle identity (lhs = S^u*S^v, rhs = sum over shuffles):
   <S^[0],S^[1]>: lhs=6.0000 rhs=6.0000  res=0e+00 (nterms=2)
   <S^[0],S^[0]>: lhs=9.0000 rhs=9.0000  res=0e+00 (nterms=2)
   <S^[0],S^[1, 0]>: res=3.6e-15 (nterms=3)
   <S^[0],S^[0, 1]>: res=1.8e-15 (nterms=3)
   <S^[0, 1],S^[1, 0]>: res=0e+00 (nterms=6)
   <S^[0, 0],S^[1, 1]>: res=4e-15 (nterms=6)
```

**What the output establishes.**

- **Two independent engines agree.** The direct explicit sums and the Chen-composition method `S_word` differ by $0$ at level 2 and $8.9\times10^{-16}$ at level 3. That agreement is itself the first numerical proof that the explicit sums and Chen's identity describe *the same* object — the sum-by-segments method is Chen's identity, and it reproduces the brute-force integrals.
- **Chen's identity holds to machine precision.** Splitting the demo path after the second segment and forming the tensor product of the halves reproduces the direct level-2 signature *exactly* ($0$ residual) and the level-3 signature to $8.9\times10^{-16}$. The factorisation is not an approximation — it is the law the signature obeys.
- **The shuffle identity holds to the same order.** At level 2 ($u=[0],v=[1]$) the residual is exactly $0$; at level 3 and for $2\times2$ shuffles it is $\sim10^{-15}$. The number of shuffle terms matches the binomial count ($2$ for $1\times1$, $3$ for $1\times2$, $6$ for $2\times2$). Products of features really do stay inside the feature space.
- **The geometric convention is what makes it work.** Because every integral here is a Riemann–Stieltjes integral along a piecewise-linear path (Stratonovich-type), both laws hold exactly. Had we fed raw Itô increments, the shuffle residuals would *not* vanish — the diagonal correction the shuffle hides is the Itô term (§2.4, §05).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using Itô iterated integrals and expecting the shuffle to hold.** Raw increments give the *non-geometric* (Itô) signature: the shuffle identity picks up an Itô correction at the diagonal and fails. Signatures on raw financial data must be built on the geometric (Stratonovich / rough-path) convention — that is exactly what augmentation and lead-lag restore (§05).
2. **Forgetting that Chen's identity needs the pieces to share a boundary.** Concatenation means $X^{(1)}$ ends where $X^{(2)}$ begins; if you compute the pieces independently with different offsets, the tensor product is wrong. Reparametrisation of the *whole* path is harmless (§03); changing the join is not.
3. **Treating the shuffle count as "a lot of terms" and truncating the word set ad hoc.** The shuffle of two length-3 words has $\binom{6}{3}=20$ terms; feature spaces explode. Universality says you *can* express everything, not that you *should* — truncation is a modelling choice with a price (§03, §06).
4. **Believing products of signatures are "new information."** They are not: the shuffle identity means any product is a linear combination of *already-existing* signature terms. If a model's feature set includes both a product and its shuffle components, it is linearly redundant — a silent collinearity that inflates apparent fit.

---

### 5. Canonical Literature & Study References

- **Lyons** (1998), *Differential equations driven by rough signals*, Rev. Mat. Iberoamericana 14(2) — §2–§3: Chen's identity and the shuffle relation as the two structural laws of the signature; the group-like / Lie-algebra picture. *The primary math-verified source.*
- **Chevyrev & Kormilitzin** (2016), *A Primer on the Signature Method in Machine Learning*, arXiv:1603.03788 — §2 (Chen's identity, shuffle, algebra structure) and §4 (the tensor algebra as the feature space; universality sketch). *Primary applied reference.*
- **Reutenauer, C.** (1993), *Free Lie Algebras* (Oxford) — the combinatorics of shuffles, Lyndon words and the free Lie algebra behind §2.3. *Math reference.*
- **Friz & Victoir** (2010), *Multidimensional Stochastic Processes as Rough Paths*, Ch 7–9 — geometric rough paths, the shuffle (multiplicativity) relation and its precise statement; the Itô-versus-Stratonovich distinction. *Math-verified.*
- **Lyons, Caruana & Lévy** (2007), *Differential Equations Driven by Rough Paths* — the systematic development of the two identities. *Math reference.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/03-log-signature-and-lie-algebra|03 · Log-Signature & Uniqueness]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|Itô Integral & Itô's Lemma]] · [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|Linear Algebra · 02 Vectors & Matrices]] (tensor products) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]
