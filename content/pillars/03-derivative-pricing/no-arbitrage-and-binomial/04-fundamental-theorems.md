---
title: "04 — The Fundamental Theorems of Asset Pricing"
tags:
  - pillar-derivative-pricing
  - no-arbitrage-and-binomial
  - fundamental-theorems
  - completeness
  - state-prices
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/02-no-arbitrage-and-risk-neutral|02 · No-Arbitrage & Risk-Neutral]] and linear algebra (rank, null space).

---

### 1. Intuition & Practical Objective

Everything so far has been constructive: build the hedge, read off the price. This page states the *theorems that say when the construction is possible at all* — the two results that turn derivative pricing from a collection of tricks into a theory.

- **First Fundamental Theorem (FT1).** No arbitrage $\iff$ there exists an equivalent martingale measure (EMM). Existence of a pricing measure is *exactly* the no-arbitrage condition — no more, no less.
- **Second Fundamental Theorem (FT2).** The market is complete — every claim is replicable, every price is unique — $\iff$ that measure is **unique**.

The practical objective: know the **three cases** a market can be in, and know which one you are in *before* quoting a price. Two of them do not have prices in the sense a trader means.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Definitions

**Arbitrage** (Shreve II Def 5.4.6; Björk Def 7.5). A self-financing strategy with $X(0)=0$, $X(T)\ge0$ a.s. and $\mathbb P\{X(T)>0\}>0$ — equivalently, a way to beat the money-market account risklessly.

**Equivalent martingale measure** (Shreve II Def 5.4.3; Björk Def 3.7). A measure $\widetilde{\mathbb P}\sim\mathbb P$ (same null sets) under which every discounted traded price $D(t)S_i(t)$ is a martingale. In the binomial, $\widetilde{\mathbb P}$ is the $\tilde p/\tilde q$ pair.

#### 2.2 The theorems

$$
\boxed{\textbf{FT1:}\quad\text{market is arbitrage-free}\iff\widetilde{\mathbb P}\text{ exists}}
$$

$$
\boxed{\textbf{FT2:}\quad\text{market is complete}\iff\widetilde{\mathbb P}\text{ is unique}}
$$

Shreve II proves FT1 as Thm 5.4.7 and FT2 as Thm 5.4.9; Björk states both for the finite-state one-period model in Ch 3 (no-arbitrage ⟺ existence of strictly positive state prices, via **Farkas' lemma**; completeness ⟺ $\mathrm{Ker}[D]=0$).

**The operator form.** In Björk's one-period $M$-state, $N$-asset market with normalized prices $Z$, a portfolio $h\in\mathbb R^N$ costs $hZ_0$ and pays $hD^Z$ (the $M\times N$ payoff matrix, first row all ones). No-arbitrage says: no $h$ with $hZ_0\le0$ and $hD^Z>0$. Farkas' lemma converts that statement about *portfolios* into the existence of a positive vector $q$ with

$$
Z_0=D^Zq,\qquad q_j>0,\quad \textstyle\sum_jq_j=1 .
$$

Completeness is the dual statement $\mathrm{Im}[D^{*}]=\mathbb R^M$ — enough independent assets to span *every* state. **Two faces of one theorem: prices exist iff the payoff matrix is spanned; prices are unique iff it is spanned exactly.**

#### 2.3 Market price of risk (continuous formulation)

For $m$ stocks and $d$ Brownian drivers, $dS_i=\alpha_iS_i\,dt+S_i\sum_j\sigma_{ij}dW_j$, the EMM is built from $\Theta$ solving (Shreve II eq. 5.4.18)

$$
\alpha_i(t)-R(t)=\sum_{j=1}^{d}\sigma_{ij}(t)\,\Theta_j(t),\qquad i=1,\dots,m .
$$

These are **$m$ equations in $d$ unknowns** — one unknown per *source of randomness*, not per stock:

- **no solution** $\Rightarrow$ FT1 fails; the model has arbitrage (e.g. two stocks, one driver, inconsistent Sharpe ratios — Shreve Ex. 5.4.4).
- **non-unique solution** $\Rightarrow$ FT2 fails; the market is incomplete.
- **unique solution** ($m=d$, $\sigma$ invertible) $\Rightarrow$ complete market.

#### 2.4 The three cases (Shreve II §5.7)

| Case | EMM | Consequence |
|---|---|---|
| No solution | does not exist | model admits arbitrage — reject it |
| Many solutions | not unique | **incomplete**: non-replicable claims have a *price interval*, not a price (credit derivatives, jump risk, vol derivatives) |
| Exactly one | unique | **complete**: $V(t)=\frac{1}{D(t)}\widetilde{\mathbb E}[D(T)V(T)\mid F(t)]$ is *the* price |

And the stochastic-discount-factor view (Björk Prop 3.18) unifies them: $\Lambda=\frac{1}{1+R}\frac{dQ}{dP}$ has $\Pi(0;X)=\mathbb E^{\mathbb P}[\Lambda X]$; distinct EMMs are distinct $\Lambda$'s.

---

### 3. Computational Implementation — completeness is a rank statement

A three-state, one-stock market. Two assets (bond, stock) and three states: the payoff matrix has rank $2<3$, so $\mathrm{Ker}[D]\ne\{0\}$, the EMM is **not** unique, and a non-replicable claim has a **price interval**. Stdlib only.

```python
def solve(A, b):
    """Gaussian elimination with partial pivoting; A:nxn, b:n -> x."""
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]/M[c][c]
                for k in range(c, n+1): M[r][k] -= f*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

S0, R, pay = 1.0, 0.05, (1.2, 1.0, 0.8)     # bond 1->1.05; stock 1.00 -> these payoffs
half = 1.0/(1+R)
X = (1.0, 0.5, 0.2)                          # a claim to be priced
print(f"assets: bond 1->{1+R:.2f}, stock {S0:.2f}->{pay}")

# state prices zeta: sum = 1/(1+R) and sum(pay_i zeta_i) = S0  ->  1-parameter family
z1_minus_z3 = (S0 - half)/(pay[0] - pay[1])
t_hi = (half - z1_minus_z3)/2.0
print(f"  zeta1 - zeta3 = {z1_minus_z3:.6f} ; zeta2 = {half - z1_minus_z3:.6f} - 2*zeta3")
print(f"  positivity: 0 < zeta3 < {t_hi:.6f}")
lo   = z1_minus_z3*X[0] + (half - z1_minus_z3)*X[1]
coef = X[0] - 2*X[1] + X[2]
print(f"  claim payoff {X} -> price = {lo:.6f} + zeta3*({coef:.6f})")
prices = [(z1_minus_z3+t)*X[0] + (half - z1_minus_z3 - 2*t)*X[1] + t*X[2]
          for t in [0.0] + [i/20000*t_hi for i in range(1, 20000)] + [t_hi]]
print(f"  PRICE RANGE = [{min(prices):.6f} , {max(prices):.6f}]  (non-unique -> incomplete)")

# now add a third asset -> payoff matrix full rank -> EMM unique
pay3, S3 = (0.8, 0.9, 1.1), 0.85
rows = [(1.0, 1.0, 1.0), pay, pay3]
z = solve([list(r) for r in rows], [half, S0, S3])
print(f"  zeta = ({z[0]:.6f}, {z[1]:.6f}, {z[2]:.6f})  sum={sum(z):.6f}")
print(f"  check stock = {z[0]*pay[0]+z[1]*pay[1]+z[2]*pay[2]:.6f} ; asset3 = {z[0]*pay3[0]+z[1]*pay3[1]+z[2]*pay3[2]:.6f}")
print(f"  unique claim price = {sum(zi*xi for zi, xi in zip(z, X)):.6f}")
```
```
assets: bond 1->1.05, stock 1.00->(1.2, 1.0, 0.8)
  zeta1 - zeta3 = 0.238095 ; zeta2 = 0.714286 - 2*zeta3
  positivity: 0 < zeta3 < 0.357143
  claim payoff (1.0, 0.5, 0.2) -> price = 0.595238 + zeta3*(0.200000)
  PRICE RANGE = [0.595238 , 0.666667]  (non-unique -> incomplete)
  zeta = (0.404762, 0.380952, 0.166667)  sum=0.952381
  check stock = 1.000000 ; asset3 = 0.850000
  unique claim price = 0.628571
```

With two assets the state-price vector lives on a one-dimensional segment ($0<\zeta_3<0.357143$), and a claim whose payoff is *not* in the span of the traded assets has an entire **interval** of arbitrage-consistent prices, $[0.595238,\,0.666667]$. Add a third independent asset and the same claim prices uniquely at $0.628571$ — inside the interval, as FT2 guarantees it must be. **Incompleteness is not a modelling detail; it is the difference between a price and a range.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Quoting a point price in an incomplete market.** If the EMM is not unique, any single number is a *choice of measure*, not a no-arbitrage consequence. The honest output is the interval $[\min_\zeta\zeta\!\cdot\!X,\max_\zeta\zeta\!\cdot\!X]$ plus the economic argument that fixes a measure.
2. **Confusing "calibrated" with "unique".** A model fitted to a rich set of liquid prices can still have a non-unique measure; calibration narrows the interval but FT2 is a *rank* statement about the payoff matrix, not a fit statistic.
3. **Counting equations wrong.** The market-price-of-risk system has $m$ equations and $d$ unknowns ($d$ = drivers, not assets). Adding correlated assets without adding drivers does **not** create a new measure dimension; it creates *inconsistency* → arbitrage (Shreve Ex. 5.4.4).
4. **Assuming bounded payoffs are hedgeable.** FT2 says every claim is replicable *only* if the tree/market spans all states. Jumps or a second untraded risk source break the span ([[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes]]).
5. **Treating $\Lambda$ as observable.** The state-price density is implied by the market, not quoted in it; estimating it (or its $q$ in the tree) requires the market prices one is trying to price — a circularity that is exactly the calibration problem of the later pillar topics.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II* — §5.4.1–5.4.4 (multidim Girsanov, MRT, market-price-of-risk equations eq. 5.4.18, arbitrage Def 5.4.6 and Ex 5.4.4, FT1 Thm 5.4.7, FT2 Thm 5.4.9), §5.7 (the three-case summary). *Math-verified in the corpus.*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 3 — payoff matrix $D^Z$ (eq 3.4), no-arbitrage via Farkas' lemma, equivalent measures (Def 3.5), martingale measure (Def 3.7), martingale pricing and completeness (Prop 3.15), stochastic discount factor (Prop 3.18). *Math-verified.*
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 3 — the binomial model is **complete**: every simple European claim is hedgeable and the risk-neutral value is unique (§3.5).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 13 (the discrete, constructive version of completeness) and Ch 15/18.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/03-binomial-trees-and-convergence|03 · Trees & Convergence]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/06-advanced-extensions|06 · Advanced Extensions]]
- Siblings: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 PDE & Derivation]] (completeness via the Martingale Representation Theorem) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (an incomplete-market example)
