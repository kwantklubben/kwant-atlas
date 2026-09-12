---
title: "3.15.4 Rough Path Theory"
tags:
  - pillar-derivative-pricing
  - path-signatures-and-rough-paths
  - rough-paths
  - p-variation
  - levy-area
  - extension-theorem
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/02-the-signature-algebra|02 · The Signature Algebra]] and [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|Brownian Motion & Martingales]]. The Itô-integral side is [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|Itô Integral & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

Everything in pages 01–03 assumed the path is *nice enough* for its iterated integrals to be classically defined. Finance's paths are not: **realised volatility, spot, order flow and high-frequency price** are all at least as rough as **Brownian motion** - and rough vol is rougher still. For such paths the naive iterated integrals **do not converge**: they blow up, and the whole signature construction looks like it should fail. Rough path theory (Lyons 1998; Friz–Victoir 2010) is the precise answer to "what actually happens, and how do we make it work?" Its three pillars:

1. **The $p$-variation norm.** Roughness is not a binary fact but a number: the smallest $p\ge1$ such that the $p$-variation $\sum_k|\Delta X_{t_k}|^p$ stays finite. Smooth paths have $p=1$; Brownian motion has $p=2$ (its quadratic variation is finite, its linear variation is not); fractional noise can have $p>2$. The $p$-variation is the *correct* topology for controlling iterated integrals.
2. **The rough-path lift.** When the path is too rough for level-2 integrals to be classically well defined, the resolution is to *declare* the level-2 object (the **Lévy area**) as part of the data. A **geometric rough path** is the package $\mathbf X=(1,X,\mathbb X^2,\dots)$ of the path *and* its consistently-chosen iterated integrals, satisfying Chen's identity and the right analytic bounds. This is the "lift" - a canonical, stable choice (e.g. the Stratonovich area for Brownian motion).
3. **The extension theorem.** Given the lift to level $\lfloor p\rfloor$ (e.g. level 2 for a $p$-variation path with $p<3$), the **extension theorem** (Lyons) says the *whole* signature is determined and can be constructed recursively - the higher iterated integrals are *functions* of the lower levels, not new free choices. This is what makes the signature computable for rough paths: **choose the area, and Chen's identity + the bounds extend it to all levels.**

The practical objective: know that signatures are not just "for nice paths," know the role of $p$-variation in making them rigorous, and understand the lift as the single free, canonical choice (the area) that everything else is built from.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 $p$-variation and what it measures

The $p$-variation of $X:[0,T]\to\mathbb R^d$ is

$$
\|X\|_{p\text{-var}}=\Big(\sup_{\text{partitions}}\sum_k|X_{t_{k+1}}-X_{t_k}|^p\Big)^{1/p},
$$

finite for smooth paths at $p=1$ (total variation), finite for Brownian motion at $p=2$ (and only there, $p>2$), finite for fractional Brownian motion with Hurst $H$ at any $p>1/H$. The defining empirical fact, verified in §3:

- **Brownian:** the quadratic variation $\sum|\Delta B|^2\to T$ (finite, nonzero), the linear variation diverges, the cubic variation $\to0$.
- **Smooth:** linear variation is finite, and *every* higher $p$-variation $\to0$.

So Brownian motion is *exactly* the boundary $p=2$ - the reason the theory is organised around $p$-variation and why level-2 (the area) is the first "extra" piece the lift must supply.

#### 2.2 Why level-2 is the hard one: the rough-path lift

For a path of finite $p$-variation with $2\le p<3$, the level-1 signature is classically defined but the **level-2 iterated integral** is not (it depends on the refining sequence - Itô vs Stratonovich differ). The rough-path solution is to **choose** the area $\mathbb X^{ij}_{s,t}$ satisfying the analytic bound

$$
|\mathbb X^{ij}_{s,t}|\le C|t-s|^{2/p}
$$

and Chen's identity, and treat $\mathbf X=(X,\mathbb X)$ as the *fundamental object*. For Brownian motion the canonical choice is the **Stratonovich** area; §3 shows it is a finite, converging quantity under refinement - a well-defined rough-path lift - exactly where the raw level-1 variation blows up. The choice of area is the *one* free, non-redundant degree of freedom of the lift; everything above is determined.

#### 2.3 The extension theorem

The central result of Lyons 1998: a multiplicative functional $\mathbf X=(1,X,\mathbb X^2,\dots,\mathbb X^{\lfloor p\rfloor})$ satisfying Chen's identity and the analytic bounds **extends uniquely** to a full signature $\mathbf X=(1,X,\mathbb X^2,\mathbb X^3,\dots)$. Each higher level is constructed by an explicit limiting procedure from the lower ones, and the extension is continuous in the $p$-variation topology. Two consequences that matter:

- **Uniqueness of the extension:** the higher iterated integrals are not free; given the lift to level $\lfloor p\rfloor$ there is exactly one geometric signature.
- **Continuity / computability:** the signature of a rough path is the *limit* of the signatures of its (smooth) approximations - which is precisely why the explicit piecewise-linear sums in pages 01–03 are legitimate: for a geometric rough path they converge to the rough-path signature (Friz–Victoir). This is the bridge between the "nice path" algebra and the rough reality.

---

### 3. Computational Implementation - p-variation of Brownian vs smooth, and a stable rough-path lift

We (i) compute the partition $p$-variation of a seeded Brownian path at successively finer grids for $p=1,2,3$ and show the three regimes (diverge / converge to $T$ / vanish), (ii) do the same for a smooth sine path (all higher $p$-variation $\to0$), and (iii) compute the **Lévy area** of a 2D Brownian path under refinement, showing it is bounded and converges to a finite limit - a well-defined level-2 rough-path lift - where the $p<2$ variation diverges. Stdlib only, seeded (`random.seed`), deterministic.




**Reading the output.**

- **Three regimes, one path.** For the *same* Brownian sample: the $p=1$ variation *diverges* ($35.9\to100.9$ as the grid refines), the $p=2$ variation converges to $T=1$ ($1.014\to0.994$, finite and nonzero - the classic quadratic variation), and the $p=3$ variation collapses toward $0$ ($0.0365\to0.0124$). This is the exact "Brownian has finite variation iff $p\ge2$" statement made visible.
- **Smooth paths are the opposite.** The sine path has finite $p=1$ variation ($4.00$, the total variation of $\sin 2\pi t$) that does *not* diverge, and its higher $p$-variations *vanish* with refinement ($p{=}2$: $1.97\times10^{-1}\to1.23\times10^{-2}$; $p{=}3$: $1.05\times10^{-2}\to4.11\times10^{-5}$). Smoothness and Brownian roughness are separated by exactly the $p$-variation index.
- **The rough-path lift is stable where the variation is not.** The 2D Brownian **Lévy area** stays bounded and converges under refinement ($-0.106\to-0.093$, increments shrinking), i.e. it is a *well-defined* level-2 rough-path lift - even though the same path's $p<2$ variation blows up. This is the concrete content of the lift: you choose the area, and it is a finite, canonical object, whereas the naive level-2 integral over a rough path would depend on the discretisation convention (Itô vs Stratonovich).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming iterated integrals of financial paths "just converge."** They do not: at Brownian roughness the level-2 integral is not classically defined and depends on the refinement convention. Every signature computation on real data *implicitly* selects a rough-path lift; failing to make it explicit (Itô vs Stratonovich) is a silent source of arbitrariness. The geometric (Stratonovich / piecewise-linear) convention used throughout this folder is the canonical choice (Friz–Victoir).
2. **Treating $p$-variation as a fixed constant of a model.** It is a *norm*, and different co-ordinates of a system can have different roughness (e.g. spot vs its realised vol). The extension theorem needs the correct $p$ for the *whole* lift; underestimating $p$ overstates the control and invalidates the bounds.
3. **Believing the lift is "just an integral."** The level-2 area is a *choice* (with the Itô/Stratonovich ambiguity) before it is a computation. For **non-geometric** data (raw Itô-increment series) the chosen area may not satisfy the shuffle identity - the reason augmentation/lead-lag is required before signatures are meaningful (§05).
4. **Overlooking that uniqueness holds up to tree-like equivalence for rough paths.** The extension theorem gives a unique extension *given the lower lift*, but the signature as a whole determines the rough path only up to tree-like reparametrisation (Boedihardjo et al. 2016) - the same caveat as §03, sharpened for the rough case.
5. **Ignoring the discretisation-vs-lift distinction in Monte Carlo.** In simulation (§03 of [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Numerical Methods · 03 Monte Carlo]]) a fine Euler grid does *not* automatically converge to the geometric rough path; if the payoff depends on the area (as variance/vol products do), the scheme must target the *lifted* object, not the naked increments.

---

### 5. Canonical Literature & Study References

- **Lyons, Terry J.** (1998), *Differential equations driven by rough signals*, Rev. Mat. Iberoamericana 14(2), 215–310 - $p$-variation control, the rough-path lift, and the **extension theorem**. *The primary math-verified source of this page.*
- **Lyons, T., Caruana, M., Lévy, T.** (2007), *Differential Equations Driven by Rough Paths*, Springer LNM 1908 - the systematic monograph; §1–3 for the lift and extension.
- **Friz, P. K. & Victoir, N.** (2010), *Multidimensional Stochastic Processes as Rough Paths*, Cambridge Studies in Adv. Math. 120 - geometric rough paths, Brownian rough paths, the continuity of the signature under $p$-variation, and the Itô/Stratonovich distinction. *The modern comprehensive treatment; math-verified.*
- **Friz, P. K. & Hairer, M.** (2014), *A Course on Rough Paths* (Springer) - a graduate-level, shorter account; Ch 1–3.
- **Boedihardjo, H., Geng, X., Lyons, T., Yang, D.** (2016), *The signature of a rough path: uniqueness*, Advances in Mathematics 293 - uniqueness for rough paths (up to tree-like equivalence).
- **Gatheral, Jaisson & Rosenbaum** (2018), *Volatility is rough* - the empirical *rougher-than-Brownian* vol paths ($H\approx0.1$) that make rough path theory not just rigorous but *necessary* for vol, §06.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/03-log-signature-and-lie-algebra|03 · Log-Signature & Uniqueness]]
- Forward: [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|Brownian Motion & Martingales]] · [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|Itô Integral & Itô's Lemma]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Applied: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Rough Volatility]] · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Numerical Methods · 03 Monte Carlo]]
