---
title: "3.6.1 American Options from Zero"
tags:
  - pillar-derivative-pricing
  - american-options
  - intuition
  - early-exercise
  - optimal-stopping
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]]. *(No prior derivatives knowledge needed.)*

---

### 1. Intuition & Practical Objective

This page builds the *why* of American options with **no prior knowledge of optimal stopping**. The objective is one idea: **the right to exercise early is a choice, and a choice you are free to make is worth at least as much as a choice you are forced to make — the whole problem is to find the best moment to use it.**

Start with the dumbest question. A European put lets you sell the stock for $K$ *at* $T$. An American put lets you sell it for $K$ *any time up to* $T$. You would never pay *less* for the extra freedom — but would you pay more, and when would you use it?

Three "aha"s:

1. **Waiting is not free.** Exercising a put today gives you $K-S$ in cash today. That cash earns interest, and it stops falling in value if the stock keeps dropping. Holding instead keeps the option alive but you forgo the cash. So there is a genuine trade-off, and its balance point is a *stock price level* — the **exercise boundary**.

2. **Early exercise of a call is (almost) never optimal.** If you exercise a call you pay $K$ now and hold a stock. You could instead have kept the cash earning interest and sold the option later. For a **dividend-free** call this argument is decisive: **you never exercise early**, so the American call *equals* the European call (Haug §1.2; Shreve I Cor 2.25). With dividends the argument breaks — the dividend slips past you if you wait, so exercise can become optimal.

3. **There is a "price of waiting" everywhere.** The American value is the European value **plus an early-exercise premium**. This premium is exactly zero for a dividend-free call, positive for essentially every put, and positive for a dividend-paying call. It is the object the rest of this folder computes.

> **The picture.** Plot the American put value against spot $S$. For low $S$ the curve is the straight line $K-S$ (you exercise immediately — the option is "dead" and worth its intrinsic value). For high $S$ the curve sits strictly *above* $K-S$ and above the European curve (you hold). The two pieces meet at the free boundary $S^*$ — and there the curves are *tangent*, not kinked. That tangency is **smooth pasting**, covered in [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]].

---

### 2. Mathematical Ground Truth & Derivations

**The discrete recursion — everything starts here.** On a binomial lattice with node value $v_k(x)$ at time $k$ and payoff $g(x)=\max(K-x,0)$ for a put, the American value obeys (Shreve I §5.1):

$$
v_k(x)=\max\Big\{\underbrace{\tfrac{1}{1+r}\big[\tilde p\,v_{k+1}(ux)+\tilde q\,v_{k+1}(dx)\big]}_{\text{continuation}},\;\; \underbrace{g(x)}_{\text{exercise now}}\Big\},\qquad v_n(x)=g(x).
$$

At every node you simply compare **continuation** with **intrinsic**. Exercise where intrinsic wins. This is the *whole* algorithm — trees, finite differences and Monte Carlo LSM are all refinements of this single line.

**Worked example (Shreve I, Ex 5.1).** $S_0=4$, $u=2$, $d=\tfrac12$, $r=\tfrac14$, $n=2$, $K=5$, $\tilde p=\tilde q=\tfrac12$. Terminal payoffs: $v_2(16)=0,\ v_2(4)=1,\ v_2(1)=4$. Rolling back:

$$
v_1(8)=\tfrac45\big[\tfrac12\cdot0+\tfrac12\cdot1\big]=0.40,\qquad v_1(2)=\max\big\{\tfrac45\big[\tfrac12\cdot1+\tfrac12\cdot4\big],\,3\big\}=\max\{2,\,3\}=3.
$$

At the down node $S=2$ the intrinsic $3$ **beats** the continuation $2$ — that is early exercise, visible in a one-line computation. At the root, $v_0(4)=\max\{\tfrac45[\tfrac12(0.40)+\tfrac12(3)],\,1\}=\max\{1.36,1\}=1.36$. **The freedom to stop at $t=1$ raised the value from the European value $0.96$ (the same recursion without the max), while the *intrinsic* at the root is $1$.** The overhang $1.36-0.96=0.40$ is the early-exercise premium.

**Continuous-time version.** Replace the recursion by the optimal-stopping value (Shreve II §8.1)

$$
V(t)=\operatorname*{max}_{\tau\in\mathcal{T},\ \tau\ge t}\ \widetilde{\mathbb E}\!\left[e^{-r(\tau-t)}\,g(S_\tau)\,\Big|\,\mathcal{F}(t)\right],
$$

and the payoff/continuation comparison becomes the **free-boundary** statement: choose $\tau$ = first time $S$ hits the boundary. The boundary is continuous in time and never known in advance.

---

### 3. Computational Implementation — the recursion, and the premium it produces

Build the CRR tree, price a European and an American put, and watch the premium emerge. Stdlib only.

```python
import math

def N(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))

def bsm_put(S, X, T, r, sig):                                  # closed form, b=r
    d1 = (math.log(S/X) + (r + 0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1 - sig*math.sqrt(T)
    return X*math.exp(-r*T)*N(-d2) - S*N(-d1)

def crr_put(S, X, T, r, sig, n, american):
    dt = T/n; u = math.exp(sig*math.sqrt(dt)); d = 1.0/u
    p  = (math.exp(r*dt) - d)/(u - d)
    val = [max(X - S*u**(n-i)*d**i, 0.0) for i in range(n+1)]
    for j in range(n-1, -1, -1):
        cont = [math.exp(-r*dt)*(p*val[i] + (1-p)*val[i+1]) for i in range(j+1)]
        ex   = [X - S*u**(j-i)*d**i for i in range(j+1)]
        val  = [max(cont[i], ex[i]) if american else cont[i] for i in range(j+1)]
    return val[0]

S, X, T, r, sig = 100.0, 95.0, 0.5, 0.08, 0.30
print(f"European BSM put            = {bsm_put(S,X,T,r,sig):.4f}")
for n in (5, 25, 100, 1000):
    am = crr_put(S,X,T,r,sig,n,True)
    print(f"  American CRR n={n:5d}: {am:.4f}   premium over European = {am-crr_put(S,X,T,r,sig,n,False):+.4f}")
```
```
European BSM put            = 4.4494
  American CRR n=    5: 4.9192   premium over European = +0.2915
  American CRR n=   25: 4.6709   premium over European = +0.2443
  American CRR n=  100: 4.6962   premium over European = +0.2418
  American CRR n= 1000: 4.6921   premium over European = +0.2425
```
*(Haug §4.2 verifies the CRR American put $4.692$ at $n{=}1000$ against the same inputs.)* The premium is $\approx0.24$ in every fine tree — a real, stable quantity, not a discretisation artefact. Note also that the tree **oscillates** in its convergence (American values do not converge monotonically like European ones) — a preview of [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "American call = European call, always" over-generalisation.** This is *only* true without dividends (and with $r\ge0$). With a dividend the holder who waits loses the dividend, and early exercise can be optimal. The rule is "$b\ge r$ ⇒ never exercise", not "calls never exercise".
2. **Ignoring the free boundary and pricing the put as European.** Understates value by the early-exercise premium — a systematic, one-directional error that grows with $r$ and maturity.
3. **Confusing "exercise when it is deep in the money" with "exercise at the boundary".** The optimal rule is a *price level*, not a heuristic. Exercising too early throws away time value; too late throws away interest. Both show up as a value *below* the tree value (this is exactly the low bias of a suboptimal rule, quantified in [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/06-advanced-extensions|06 · Advanced Extensions]]).
4. **Forgetting that the boundary moves.** For a finite-maturity put the boundary is a *curve* $S^*(t)$ rising to $K$ at expiry; treating it as a constant is an approximation that goes wrong for long maturities.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance I*, §5.1 (the American recursion and the $S=2$ early-exercise node) and Ch 8.7 (binomial perpetual put). *Math-verified.*
- **Shreve**, *Stochastic Calculus for Finance II*, §8.1–8.2 (optimal-stopping value of an American security; no-early-exercise for a dividend-free call, Cor 8.5.3). *Math-verified.*
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §1.2 (American call = European, no dividends) and §4.2 (CRR American put $4.692$). *Numerically verified.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 13 (binomial American valuation, early-exercise boundary pictures).

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
- Continue: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/02-optimal-stopping-theory|02 · Optimal-Stopping Theory]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · Advanced Extensions]] (the same recursion, one page)
