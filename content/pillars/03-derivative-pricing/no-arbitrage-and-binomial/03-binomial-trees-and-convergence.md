---
title: "3.2.3 Binomial Trees & Convergence to Black–Scholes"
tags:
  - pillar-derivative-pricing
  - no-arbitrage-and-binomial
  - crr
  - convergence
  - discrete-error
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/02-no-arbitrage-and-risk-neutral|02 · No-Arbitrage & Risk-Neutral]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

A one-period binomial has two states; a real market has a continuum. The **multi-period binomial tree** bridges the gap: chop $[0,T]$ into $n$ steps, put a two-state bet at each, and let the coin be re-tossed at every node. The stock after $n$ steps is $S_0u^{Y}d^{\,n-Y}$ with $Y\sim\text{Binomial}(n,p)$ — a *discrete* approximation to the lognormal. Price each node by backward induction and, as $n\to\infty$, the price converges to the Black–Scholes–Merton value.

The practical objective of this page is the **Cox–Ross–Rubinstein (CRR) recipe** — how to choose $u,d,p$ so the tree has the right volatility — plus an honest picture of the *error*: CRR converges at $O(1/n)$, **not monotonically**.

> **Why it matters beyond pedagogy.** A tree is the default engine for American options, discrete dividends, and any payoff with a kink or an exercise boundary — cases where BSM has no closed form. Knowing exactly how the discretization errs is what separates a reliable tree price from a plausible-looking wrong one.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 CRR parameters (Cox–Ross–Rubinstein 1979; Hull 13.15–13.18; Haug 7.5–7.6)

With $\Delta t=T/n$, choose the up/down factors to match the *volatility* of geometric Brownian motion:

$$
\boxed{\;u=e^{\sigma\sqrt{\Delta t}},\qquad d=\frac1u=e^{-\sigma\sqrt{\Delta t}}\;}
$$

so the log-increment per step is $\pm\sigma\sqrt{\Delta t}$ and the per-step log-variance is $4\sigma^2\Delta t\,p(1-p)\approx\sigma^2\Delta t$ for $p\approx\tfrac12$ — matching GBM's $\sigma^2\Delta t$. The tree is **recombining**: an up-then-down equals a down-then-up, so after $n$ steps there are $n+1$ nodes (not $2^n$), with

$$
S_{j,i}=S\,u^{i}d^{\,j-i}\quad\text{at step }j\text{ after }i\text{ up-moves},\qquad \#\text{paths}=\binom{j}{i}.
$$

The risk-neutral probability is the same bracket-derived expression as before, with $e^{b\Delta t}$ the per-step growth of the underlying's carry ($b=r$ stock, $b=r-q$ index/continuous yield):

$$
\boxed{\;p=\frac{e^{b\Delta t}-d}{u-d}\;}\qquad\text{(Hull 13.17)}
$$

#### 2.2 European closed form (CRR sum) and the efficient truncation

Because the terminal distribution is binomial, a European claim has a *finite sum* over terminal nodes (Haug eq. 7.1):

$$
V_0=e^{-rT}\sum_{i=0}^{n}\binom{n}{i}p^{i}(1-p)^{n-i}\max\!\big(Su^{i}d^{\,n-i}-X,\,0\big).
$$

Only nodes with $Su^id^{\,n-i}>X$ contribute, so one starts the sum at the smallest integer $i$ with $Su^{i}d^{\,n-i}>X$, i.e. $i>\big(\ln(X/S)-n\ln d\big)/\ln(u/d)$ — the standard speed-up from $O(n^2)$ backward induction to $O(n)$ for European claims (Haug eq. 7.3–7.4).

#### 2.3 American backward induction (Haug 7.9–7.11; Hull §13.5)

For an American contract the holder compares continuation with intrinsic value at **every** node:

$$
\boxed{\;P_{j,i}=\max\!\Big(X-Su^{i}d^{\,j-i},\;\;e^{-r\Delta t}\big[p\,P_{j+1,i+1}+(1-p)\,P_{j+1,i}\big]\Big)\;}
$$

The tree is the natural American engine: no free boundary to solve, the exercise region is discovered node by node. (Full treatment on [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/06-advanced-extensions|06 · Advanced Extensions]].)

#### 2.4 Convergence

As $n\to\infty$ with $\Delta t=T/n\to0$, the tree's terminal distribution converges to the lognormal $S_T=S_0e^{(r-\frac12\sigma^2)T+\sigma\sqrt T\,Z}$, and the CRR price converges to the BSM price at rate **$O(1/n)$** — *with a non-monotone, oscillating error*. The convergence theorem (Hull §13.9 and its appendix) is exact in the limit; the oscillation is a finite-$n$ artifact.

Other parameterizations trade one property for another (Haug §4.3–4.5): **Rendleman–Bartter** ($p=\tfrac12$, exponential $u/d$), **Jarrow–Rudd** (equal-probability lognormal matching), **Leisen–Reimer** (Peizer–Pratt inversion, $O(1/n^2)$-class accuracy at odd $n$), and the **trinomial** tree (Boyle 1986) with a third, middle state.

---

### 3. Computational Implementation — convergence and its oscillation

Stdlib only. Two experiments: ($a$) the European put price as $n$ grows against the closed form; ($b$) the CRR error for an **at-the-money American put**, which shows the oscillation.

```python
import math

def N(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))
def bsm_put(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1 - sig*math.sqrt(T)
    return X*math.exp(-r*T)*N(-d2) - S*N(-d1)

def crr(S, X, T, r, sig, n, american=False):
    dt = T/n; u = math.exp(sig*math.sqrt(dt)); d = 1.0/u
    p = (math.exp(r*dt)-d)/(u-d); disc = math.exp(-r*dt)
    val = [max(X - S*u**i*d**(n-i), 0.0) for i in range(n+1)]
    for j in range(n-1, -1, -1):
        val = [disc*(p*val[i+1]+(1.0-p)*val[i]) for i in range(j+1)]
        if american:
            val = [max(val[i], X - S*u**i*d**(j-i)) for i in range(j+1)]
    return val[0]

# (a) European put: S=100, X=95, T=0.5, r=8%, sigma=30%  (Haug-verified inputs)
S, X, T, r, sig = 100.0, 95.0, 0.5, 0.08, 0.30
ex = bsm_put(S, X, T, r, sig)
print(f"BSM closed form put = {ex:.4f}")
for n in (10, 25, 50, 100, 200, 500, 1000, 2000, 5000):
    v = crr(S, X, T, r, sig, n)
    print(f"  n={n:5d}  CRR={v:.4f}  |err|={abs(v-ex):.5f}")

# (b) at-the-money American put: S=X=100, T=1, r=5%, sigma=20%
print("oscillation (ATM):")
for n in range(2, 13):
    print(f"  n={n:2d} amer={crr(100,100,1.0,0.05,0.20,n,True):.5f}")
```
```
BSM closed form put = 4.4494
  n=   10  CRR=4.6012  |err|=0.15180
  n=   25  CRR=4.4265  |err|=0.02286
  n=   50  CRR=4.4491  |err|=0.00026
  n=  100  CRR=4.4544  |err|=0.00499
  n=  200  CRR=4.4552  |err|=0.00581
  n=  500  CRR=4.4518  |err|=0.00238
  n= 1000  CRR=4.4496  |err|=0.00026
  n= 2000  CRR=4.4502  |err|=0.00082
  n= 5000  CRR=4.4497  |err|=0.00035
oscillation (ATM):
  n= 2 amer=5.73765
  n= 3 amer=6.49956
  n= 4 amer=5.88280
  n= 5 amer=6.36783
  n= 6 amer=5.95464
  n= 7 amer=6.27036
  n= 8 amer=5.97350
  n= 9 amer=6.23677
  n=10 amer=6.00426
  n=11 amer=6.21377
  n=12 amer=6.01855
```

Read the table as two messages. First, CRR **does** converge: $n{=}1000$ gives $4.4496$ against BSM's $4.4494$ (exactly Haug's verified pair). Second, the error **does not fall monotonically** — it drops to $0.00026$ at $n{=}50$, rises to $0.00581$ at $n{=}200$, falls again. The ATM American series is worse: values jump by $\sim0.5$ as $n$ changes parity, because the terminal payoff kink sits exactly on a tree node for even $n$ and between nodes for odd $n$. This is the well-documented CRR oscillation.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Trusting a single $n$.** Because the error oscillates, doubling $n$ can make the price *worse*. Standard practice: average $n$ and $n+1$ (or $n\pm1$) prices, or use a smoothing scheme (Leisen–Reimer, or averaging the payoff over $\pm$ half a node). Reporting one tree value without an $n$-study is not a price.
2. **Negative "probabilities".** CRR needs $d<e^{r\Delta t}<u$, i.e. $r\sqrt{\Delta t}<\sigma$. With small $\sigma$ or a coarse step (long-dated, few nodes) $p$ leaves $[0,1]$ and the tree admits arbitrage — see [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes]].
3. **Drift vs carry.** Using $b=r$ for an index/FX/commodity with a yield or foreign rate silently drops an $e^{-q\Delta t}$ / $e^{-r_f\Delta t}$ factor from every node; the per-step growth factor is $e^{b\Delta t}$, not $e^{r\Delta t}$ (Hull §13.11).
4. **Recombination assumed, not checked.** The CRR tree recombines because $d=1/u$. Non-CRR variants (e.g. non-constant local volatility, "displaced" trees) may not; then node counts explode and the $O(n^2)$ cost becomes a real constraint.
5. **Tree "Greeks" carry discretization noise.** Delta from adjacent nodes, $\Delta=\frac{f_{1,1}-f_{1,0}}{Su-Sd}$ (Haug 7.9), is a finite difference on a coarse grid; its error is larger than the price error and inherited from the same oscillation.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 13 — one-step delta (13.1), risk-neutral valuation (13.2–13.3), two-step trees (13.5–13.10), volatility matching (13.12–13.18), American backward induction, §13.9 convergence and its appendix, §13.11 index/currency trees. *Verification report in the corpus.*
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §4.1 (CRR European closed binomial, eq 7.1–7.6; §4.2 American and tree Greeks, eq 7.9–7.11), §4.3–4.5 (Rendleman–Bartter, Leisen–Reimer, trinomial). *Numerically verified: the $4.4496$ vs $4.4494$ pair used above is Haug's own check.*
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 1–3 — the recursive, measure-theoretic version of the same backward induction.
- **Cox, Ross & Rubinstein (1979)**, *Option pricing: a simplified approach*, J. Financial Economics 7 — the original tree.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/02-no-arbitrage-and-risk-neutral|02 · No-Arbitrage & Risk-Neutral]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|04 · Fundamental Theorems]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/06-advanced-extensions|06 · Advanced Extensions]]
- Siblings: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]]
