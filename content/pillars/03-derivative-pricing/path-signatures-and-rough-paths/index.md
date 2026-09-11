---
title: "Path Signatures & Rough Paths: Iterated Integrals, Chen's Identity & the Signature of a Path — Topic Hub & Formula Lookup"
tags:
  - pillar-derivative-pricing
  - path-signatures-and-rough-paths
  - signature
  - iterated-integrals
  - rough-paths
  - log-signature
  - signature-kernel
  - machine-learning
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|Itô Integral & Itô's Lemma]] and [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (tensor algebra). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A financial time series *is* a path: spot, vol, order flow, a yield curve — each is a curve through a state space, recorded only at sample times. Almost every quantitative problem is, at bottom, "summarize this path faithfully enough to decide." The **signature of a path** is the principled answer to that: the complete, ordered inventory of **iterated integrals** of the path. It is a hierarchy — level 1 remembers the *increment* (where the path ended), level 2 remembers the *area* between coordinates (the shape of the loop, the covariances), level 3 the *signed volumes*, and so on. Collecting all levels recovers essentially the *whole path*, up to the genuinely irrelevant information (reparametrisation).

This folder is the topic-hub for two interlocking subjects:

1. **The signature and its algebra** — the tensor algebra of iterated integrals, **Chen's identity** (the signature factorises under concatenation), the **shuffle product identity** (products of integrals are integrals over shuffles), the **log-signature** and the **free Lie algebra**, and **Lyons' uniqueness theorem** (the signature determines the path up to tree-like equivalence).
2. **Rough path theory** — the reason the construction is *stable*: for paths rougher than finite variation (Brownian motion, realised volatility, order flow) the iterated integrals are not classically well defined, and **rough path theory** (Lyons 1998; Friz–Victoir 2010) supplies the analytic control — the **$p$-variation** norm, the **rough-path lift**, and the **extension theorem** — that makes signatures rigorous and computable *in the wild*.

The one-sentence essence:

> **The signature is a complete, reparametrisation-invariant, hierarchically-ordered summary of a path built from iterated integrals; its two algebraic laws — Chen's identity and the shuffle product — are what make it computable, and rough path theory is what makes it rigorous for the irregular paths that finance actually produces; on top of that invariant summary one builds the log-signature (a compression into a Lie element), the expected signature and the signature kernel (universal features for machine learning on paths), and lead-lag / time augmentation (the fix that restores the shuffle law for raw, non-geometric data).**

This folder is a *hub*: (a) the fast formula lookup below, and (b) six sub-pages that walk from raw intuition through the signature algebra, the log-signature and uniqueness, rough path theory, the practical failure modes (augmentation, lead-lag, hedging), and the frontier (expected signatures, signature kernels, signatures in machine learning, and lead-lag signatures for rough vol).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $X=(X^1,\dots,X^d)$ a path in $\mathbb R^d$ over $[0,T]$, $S(X)_{0,T}=(1,S^1,\dots,S^w,\dots)$ its **signature** (a point in the tensor algebra $T((\mathbb R^d))$), $S^w$ the iterated integral indexed by the word $w=i_1\cdots i_k$, $\Delta_k=X_{t_{k+1}}-X_{t_k}$ the increments of a piecewise-linear discretisation, $u\shuffle v$ the shuffle of two words, $\ell=\log S(X)$ the **log-signature**, $[u,v]$ the tensor/Lie bracket, $B$ a Brownian motion, $H$ the Hurst exponent, $K(X,Y)$ the signature kernel.

**Quick-Reference Lookup (job #1).** Every formula below is stated in the verified form used throughout the folder, and every number in the check column was **re-executed** (§3 and the sub-pages) with stdlib-only, deterministic code.

| Quantity | Formula | Verified check |
|---|---|---|
| **Signature, level 0** | $S^{\emptyset}_{0,T}=1$ (empty word) | constant by construction |
| **Signature, level 1** | $S^{i}_{0,T}=\displaystyle\int_0^T dX^i_t=X^i_T-X^i_0$ | demo path: $S^1=(3,2)$ (endpoint) |
| **Signature, level 2** (piecewise-linear, explicit sum) | $S^{ij}=\sum_{k<l}\Delta^i_k\Delta^j_l+\tfrac12\sum_k\Delta^i_k\Delta^j_k$ | demo: $S^{11}{=}4.5,\ S^{12}{=}2.5,\ S^{21}{=}3.5,\ S^{22}{=}2.0$ |
| **Signature, level 3** (piecewise-linear, explicit sum) | $S^{ijk}=\sum_{a<b<c}\Delta^i_a\Delta^j_b\Delta^k_c+\tfrac12\sum_{a<c}\Delta^i_a\Delta^j_a\Delta^k_c+\tfrac12\sum_{a<b}\Delta^i_a\Delta^j_b\Delta^k_b+\tfrac16\sum_a\Delta^i_a\Delta^j_a\Delta^k_a$ | demo: $S^{112}=9.166667$, $S^{122}=4.166667$ |
| **Chen's identity** (concatenation) | $S^{w}(X^{(1)}\ast X^{(2)})=\displaystyle\sum_{uv=w}S^{u}(X^{(1)})\,S^{v}(X^{(2)})$ | residual **$0$** (lev 2), $8.9\times10^{-16}$ (lev 3) |
| **Shuffle product identity** | $S^{u}S^{v}=\displaystyle\sum_{w\in\,u\shuffle v}S^{w}$ | lev-2 residual **$0$**; lev-3 $\sim1.8\times10^{-15}$ |
| **Log-signature / Lévy area, lev 2** | $\ell^{ij}=S^{ij}-\tfrac12S^iS^j=\tfrac12(S^{ij}-S^{ji})$ (antisymmetric) | $L^{12}{=}{-}0.5,\ L^{21}{=}{+}0.5,\ L^{ij}{+}L^{ji}=0$ |
| **Reparametrisation invariance** | $S(X\circ\varphi)=S(X)$ for any monotone $\varphi$ | lev-2 err **$0$**; lev-3 $\sim1\times10^{-14}$ |
| **Lyons uniqueness** | $S(X)=S(Y)\Rightarrow X,Y$ differ by reparametrisation / tree-like path | two non-reparametrised paths $\Rightarrow$ areas $+4.5$ vs $-4.5$ |
| **Brownian quadratic variation** | $\sum_k|\Delta B_{t_k}|^2\to T$ | grid $16000$: $0.9935$ (with $T=1$) |
| **Brownian $p$-variation** | finite iff $p\ge2$ (infinite for $p<2$) | $p{=}1$: $35.9\to100.9$ (diverges); $p{=}3$: $0.0365\to0.0124$ ($\to0$) |
| **Lead-lag area $=$ realized variance** | $\mathrm{Area}=\tfrac12\sum_k\Delta X_k^2$ | $A=15.172146$, diff $1.4\times10^{-14}$ |
| **Time augmentation** | 1D signature $\equiv$ endpoint; $(t,X_t)$ restores area | same-endpoint paths: $S^{11}{=}2.0$ both; areas $-0.667$ vs $+0.667$ |
| **Expected signature, 1D BM** | $\mathbb E[S^{1^m}]=0$ (odd), $=\tfrac{T^m/2}{m!}(m{-}1)!!$-type (even) | MC: $0.49055$ vs $0.5$; $0.11719$ vs $0.125$ |
| **Signature kernel** | $K(X,Y)=\sum_w S^w(X)S^w(Y)$ | $K(X,X)=56.75,\ K(X,Y)=170.5$; Cauchy–Schwarz OK |
| **Rough-vol short skew** | $\partial_k\sigma_{BS}\sim T^{H-\frac12},\ H\approx0.1$ | empirical (Gatheral–Jaisson–Rosenbaum 2018) |

> **Critical caveat (flagged in the corpus).** The level-2 and level-3 formulas above are *exact* for a piecewise-linear path but are *Riemann–Stieltjes / Stratonovich-type* iterated integrals. For truly rough paths (Brownian vol) the same sums converge to the **Stratonovich** iterated integral only after a geometric rough-path lift has been chosen; the classical (Itô) integral has different, non-geometric terms that *violate* the shuffle identity. Every identity in this table is stated for the **geometric** (Stratonovich / rough-path) convention — the one the whole ML-on-signatures literature uses. §04 quantifies the difference.

---

### 3. Computational Implementation — the signature engine

Stdlib only (`math`, `itertools`, `random`) — no numpy/scipy. The whole folder runs on two primitives: the **explicit iterated-integral sums** for a piecewise-linear path (levels 1–3, exact), and the **segments composition method** (`S_word`) that evaluates *any* word's integral exactly via Chen's identity across the breakpoints. Every identity in §2 is verified to machine precision by the engine:

```python
import math

# ---- exact iterated integrals of a piecewise-linear path ----
def increments(X):
    d=len(X[0]); n=len(X)-1
    return [[X[k+1][i]-X[k][i] for i in range(d)] for k in range(n)], d, n

def lev1(X):
    inc,d,n=increments(X)
    return [sum(inc[k][i] for k in range(n)) for i in range(d)]

def lev2(X):                              # S^ij = sum_{k<l} + 1/2 diag   (exact, PL path)
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

def compositions(total,parts):            # nonnegative compositions
    if parts==1: yield (total,); return
    for a in range(total+1):
        for rest in compositions(total-a,parts-1): yield (a,)+rest

def S_word(X,w):                          # any word's integral, exact via Chen across segments
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

def shuffle(a,b):                         # all interleavings preserving order
    if not a: return [b]
    if not b: return [a]
    r=[]
    for w in shuffle(a[1:],b): r.append([a[0]]+w)
    for w in shuffle(a,b[1:]): r.append([b[0]]+w)
    return r

# ---- the running demo path (deterministic, integer increments) ----
X=[(0.0,0.0),(2.0,0.0),(2.0,3.0),(6.0,1.0),(3.0,2.0)]
S1=lev1(X); S2=lev2(X); S3=lev3(X)
print("level-1 signature (endpoint) S1 =",[round(v,6) for v in S1])
print("level-2 signature S2 =")
for i in range(2): print("   ",[round(S2[i][j],6) for j in range(2)])
print("Lévy area = 0.5*(S2[0][1]-S2[1][0]) =",0.5*(S2[0][1]-S2[1][0]))

# consistency of the two engines
e2=max(abs(S_word(X,[i,j])-S2[i][j]) for i in range(2) for j in range(2))
e3=max(abs(S_word(X,[i,j,k])-S3[i][j][k]) for i in range(2) for j in range(2) for k in range(2))
print("S_word vs direct sums:  lev2 err=%.1e  lev3 err=%.1e"%(e2,e3))

# Chen's identity on the two halves
m=2; X1,X2=X[:m+1],X[m:]
a1,a2=lev1(X1),lev2(X1); b1,b2=lev1(X2),lev2(X2)
chen=[[a2[i][j]+a1[i]*b1[j]+b2[i][j] for j in range(2)] for i in range(2)]
print("Chen lev2 residual =",max(abs(chen[i][j]-S2[i][j]) for i in range(2) for j in range(2)))

# shuffle identity
for (u,v) in (([0],[1]),([0],[0,1]),([0,1],[1,0])):
    lhs=S_word(X,u)*S_word(X,v)
    rhs=sum(S_word(X,w) for w in shuffle(u,v))
    print("shuffle <S^%s,S^%s>: res=%.1e"%(u,v,abs(lhs-rhs)))

# log-signature level 2 (Lévy area matrix) must be antisymmetric
L=[[S2[i][j]-0.5*S1[i]*S1[j] for j in range(2)] for i in range(2)]
print("log-signature lev2 antisymmetry max|L+L^T| =",
      max(abs(L[i][j]+L[j][i]) for i in range(2) for j in range(2)))
```
```
level-1 signature (endpoint) S1 = [3.0, 2.0]
level-2 signature S2 =
    [4.5, 2.5]
    [3.5, 2.0]
Lévy area = 0.5*(S2[0][1]-S2[1][0]) = -0.5
S_word vs direct sums:  lev2 err=0.0e+00  lev3 err=8.9e-16
Chen lev2 residual = 0.0
shuffle <S^[0],S^[1]>: res=0.0e+00
shuffle <S^[0],S^[0, 1]>: res=1.8e-15
shuffle <S^[0, 1],S^[1, 0]>: res=0.0e+00
log-signature lev2 antisymmetry max|L+L^T| = 0.0
```

The two engines — the **direct explicit sums** and the **Chen-composition `S_word`** — agree to $10^{-15}$, which is itself a *numerical proof* that the explicit sums and Chen's identity describe the same object. Chen's identity then holds to machine zero at level 2 and $10^{-15}$ at level 3; the shuffle identity holds to the same order; and the level-2 log-signature (the Lévy area) is exactly antisymmetric — the first hint that the log-signature is a **Lie element**, not a general tensor (§03).

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The signature of a 1D path is just its endpoint.** A single coordinate has no area, no loop, no shape — $S^{11}=\tfrac12(S^1)^2$ is determined by $S^1$. Using raw univariate signatures is throwing the path away. The fix is time augmentation or lead-lag (§05).
2. **Non-geometric (Itô) data breaks the shuffle law.** The identities in §2 hold for *geometric* (Stratonovich / rough-path) integrals; raw increments are Itô-type and the shuffle relation fails at the diagonal. Augmenting is not optional — it is the fix (§05).
3. **Truncation is a modelling choice with a price.** The signature is infinite; any computation truncates at level $N$. The price is the *reparametrisation-scale* information in the high levels — small, fast oscillations live at high level, so truncation literally throws away the short-time structure (the one that matters for rough vol, §06).
4. **The signature is not a probability distribution.** Reparametrisation invariance means the signature is *insensitive to the speed* of the path — perfect for geometric features, wrong if the *timing* (e.g. the arrival structure of order flow) is itself the signal. Lead-lag reintroduces time, carefully (§05).
5. **Expected signatures are not moments to be read naively.** The expected signature is a universal characterising object (Chevyrev–Lyons), but Monte Carlo estimates converge slowly at high level — the weights decay only factorially — so truncation error and estimator bias interact (§06).
6. **Roughness is a regularity statement, not a style choice.** A $p$-variation norm below what the data actually supports gives *uncontrolled* iterated integrals; the whole rough-path apparatus exists because you cannot ignore this (§04).

---

### 5. Canonical Literature & Study References

- **Lyons, Terry J.** (1998), *Differential equations driven by rough signals*, Revista Matemática Iberoamericana 14(2), 215–310 — **the foundational paper**: $p$-variation control, the rough-path lift, the extension theorem, and uniqueness of the signature. *The primary math-verified source of this folder.*
- **Lyons, T., Caruana, M., Lévy, T.** (2007), *Differential Equations Driven by Rough Paths* (Springer Lecture Notes 1908) — the standard monograph of the theory; the full signature/extension framework.
- **Lyons, T. J., Ni, Hao, Zhang, Hao** (2019), *Machine Learning Models of Financial Time Series*, arXiv:1905.11666 — signature kernels and lead-lag signatures applied to (rough) volatility and financial series; the applied bridge this folder leans on for §05–§06.
- **Hambly, B., Lyons, T.** (2010), *Uniqueness for the signature of a path of bounded variation and the reduced path group*, Annals of Mathematics 171(1), 109–167 — the sharp uniqueness result: the signature determines a bounded-variation path up to tree-like equivalence (the basis for §03's uniqueness statement).
- **Chevyrev, Ilya & Kormilitzin, Andrey** (2016), *A Primer on the Signature Method in Machine Learning*, arXiv:1603.03788 — the standard practitioner introduction: iterated integrals, lead-lag, expected signature, feature engineering for ML. *The primary applied reference for §01, §05–§06.*
- **Friz, Peter K. & Victoir, Nicolas** (2010), *Multidimensional Stochastic Processes as Rough Paths* (Cambridge Studies in Advanced Mathematics 120) — the modern comprehensive treatment; geometric rough paths, the extension theorem, Brownian rough paths. *Math-verified.*
- **Boedihardjo, H., Geng, X., Lyons, T., Yang, D.** (2016), *The signature of a rough path: uniqueness*, Advances in Mathematics 293, 720–737 — uniqueness for *rough* paths (beyond bounded variation), closing the gap this folder flags in §03–§04.
- **Gatheral, Jaisson & Rosenbaum** (2018), *Volatility is rough* — the $H\approx0.1$ empirical finding and the lead-lag signature of rough vol, linked from §06.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|Brownian Motion & Martingales]] · [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|Itô Integral & Itô's Lemma]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (tensor algebra) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Sibling topics: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Advanced Volatility — Heston & SABR]] (rough vol lives here) · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Exotic & Path-Dependent Options]] (the pricing objects that live *on* paths) · [[pillars/03-derivative-pricing/numerical-methods/index|Numerical Methods]] (simulation of the paths)
- Related flat notes: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Rough Volatility (from the SV side)]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/03-lookbacks-and-asians|Lookbacks & Asians]] · [[foundations/econometrics-and-timeseries/04-volatility-modeling|Volatility Modeling]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
- Sub-pages (in-folder): 01 From Zero · 02 The Signature Algebra · 03 Log-Signature & Uniqueness · 04 Rough Path Theory · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/01-from-zero-intuition|01 · From Zero]] — needs only the idea of a path and an integral.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/02-the-signature-algebra|02 · The Signature Algebra]] → [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/03-log-signature-and-lie-algebra|03 · Log-Signature & Uniqueness]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/04-rough-path-theory|04 · Rough Path Theory]] → [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/06-advanced-extensions|06 · Advanced Extensions]].
- Back-references: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston & SABR · 06 (rough vol launchpad)]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
