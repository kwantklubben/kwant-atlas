---
title: "F.4.1 Stochastic Calculus from Zero"
tags:
  - foundations
  - stochastic-calculus
  - intuition
  - brownian-motion
---

**Basic Prerequisites:** Elementary probability only (a random variable, expectation, the normal distribution) — **no measure theory required at this entry point**; the measure-theoretic machinery is developed from [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|02]] onward.

---

### 1. Intuition & Practical Objective

The entire subject is one sentence: **Brownian motion $(W(t))$ accumulates squared increments at rate 1 — that is, $(dW)^2 = dt$ — so the "calculus" that describes prices is not the calculus you learned in school.** Classical $df = f'(x)\,dx$ works because $dx^2$ is negligible. For $W$, $dW^2$ is *not* negligible; instead, over any interval, $\sum(\Delta W)^2 \to$ (elapsed time) deterministically. This is the single mechanism behind every surprise in quantitative finance (the $\tfrac12\sigma^2$ in geometric-Brownian drift, the martingale measure, the Itô correction).

Build it in three "aha"s, from the discrete to the continuous:

1. **A random walk is a martingale in disguise.** Flip fair coins: $M_k=\sum_{j=1}^k X_j$, $X_j=\pm1$. It has zero drift, so $\mathbb E[M_{k+1}\mid\mathcal F_k]=M_k$ — a fair game. Scale steps down ($\pm1/\sqrt n$) and speed up ($n$ steps per unit time): $M_k/\sqrt{k}$ looks Gaussian (CLT), and as $n\to\infty$ the interpolated process converges to Brownian motion (Shreve I §13.4; a functional CLT / Donsker).

2. **The size of the step determines the smoothness.** Because the scaled step is $\pm1/\sqrt n$ (not $\pm1/n$), squared steps are $1/n$ and *don't vanish when summed over $n$ steps*: $\sum$ of (square) $\approx n\cdot(1/n)=1$ per unit time. That is exactly why BM has unbounded first-order variation but finite quadratic variation $T$. A $C^1$ function (step $\propto 1/n$) would have $(dt)^2\to0$; a BM path moves too fast.

3. **"$\int$ with a $dW$" is a different beast.** You cannot interpret $\int_0^T W\,dW$ as a Riemann–Stieltjes integral, because classical calculus yields $\tfrac12 W(T)^2$, but the true (Itô) value is $\tfrac12 W(T)^2-\tfrac12 T$. The subtraction is the quadratic-variation correction. The beginner must *unlearn* the classical answer before learning the Itô one.

---

### 2. Mathematical Ground Truth & Derivations

**From random walk to BM (Shreve I §13.3–13.5).** Let $M_k$ be the symmetric random walk and define the scaled process
$$
W^{(n)}(t)=\frac{1}{\sqrt n}M_{nt}.
$$
The CLT (via MGFs, Shreve I Thm 3.39) gives $M_{nt}/\sqrt{nt}\xrightarrow{d}N(0,1)$; by independence of increments the whole interpolated trajectory converges weakly to BM. BM is defined (Shreve II Def 3.3.1) by
$$
W(0)=0,\quad W\text{ continuous},\quad W(t)-W(s)\sim N(0,\,t-s)\ \text{independent increments}.
$$
Key structural facts: covariance $\mathbb E[W(s)W(t)]=\min(s,t)$ (Shreve I §13.6), and $W$ is both a **martingale** and a **Markov** process (Shreve II Thm 3.3.4, §3.5).

**Quadratic variation — the heart.** For any partition $\Pi$ of $[0,T]$,
$$
[W,W](T)=\lim_{\|\Pi\|\to0}\sum_j\big(W(t_{j+1})-W(t_j)\big)^2=T.
$$
*Why:* each squared increment has mean $t_{j+1}-t_j$ and variance $2(t_{j+1}-t_j)^2$; by a law-of-large-numbers the sum collapses to $\sum(t_{j+1}-t_j)=T$ (Shreve II Thm 3.4.3). The informal bookkeeping is then
$$
(dW)^2=dt,\qquad dW\,dt=0,\qquad dt\,dt=0 \quad\text{(Shreve II eqs 3.4.10–13).}
$$

**Consequence for the drift of a log-price.** For geometric Brownian motion $S(t)=S(0)e^{\sigma W(t)+\left(\mu-\tfrac12\sigma^2\right)t}$ (Shreve I Thm 15.3), *applying* Itô's lemma recovers $dS=\mu S\,dt+\sigma S\,dW$. The $\tfrac12\sigma^2$ is forced: exponentiate the differential form and the $(dW)^2=dt$ rule generates the correction *backwards* — the answer is consistent only if the exponent carries $-\tfrac12\sigma^2$. Missing it would make $\mathbb E[\log(S_T/S_0)]$ grow with $\tfrac12\sigma^2$, a pure artifact of nonzero quadratic variation, not a real drift.

---

### 3. Computational Implementation — *see* the quadratic variation

Simulate BM and watch $\sum(\Delta W)^2\to T$ regardless of path; then check that a pushed ($\sigma\,dW$) version has quadratic variation $\sigma^2 T$ — the direct, quantitative meaning of "$(dW)^2=dt$". Stdlib only.

```python
import math, random
random.seed(42)

def bm_path(n, T=1.0):
    dt = T/n
    W, dWs = [0.0], []
    for _ in range(n):
        d = random.gauss(0.0, math.sqrt(dt)); dWs.append(d); W.append(W[-1]+d)
    return W, dWs

T = 1.0
for n in (1000, 10000, 100000):
    _, dWs = bm_path(n, T)
    qv = sum(d*d for d in dWs)
    print("BM path  n=%6d : sum(Delta W)^2 = %.4f   (theory T = %.4f)" % (n, qv, T))

# martingale check: E[W(t) | F(s)] = W(s)  vs  quadratic "predictable" sd of increments
n = 100000; dt = T/n
incs = [random.gauss(0.0, math.sqrt(dt)) for _ in range(n)]
sd = math.sqrt(sum(x*x for x in incs)/n)      # since mean ~ 0
print("increment stdev = %.4f   (theory sqrt(dt) = %.4f)" % (sd, math.sqrt(dt)))
```
```
BM path  n=  1000 : sum(Delta W)^2 = 1.0389   (theory T = 1.0000)
BM path  n= 10000 : sum(Delta W)^2 = 0.9912   (theory T = 1.0000)
BM path  n=100000 : sum(Delta W)^2 = 1.0038   (theory T = 1.0000)
increment stdev = 0.0032   (theory sqrt(dt) = 0.0032)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating $(dW)^2$ as negligible.** This is the single most common and most damaging error. Ordinary calculus drops all second-order terms; for $W$ the second-order term *is* the leading stochastic one. Symptom: your Itô expansions disagree with simulation.
2. **Confusing quadratic variation with total variation.** BM has infinite first-order variation ($\int_0^T|dW|=\infty$), but finite quadratic variation. The "infinite" part is why you cannot treat $dW$ as a classical $C^1$ differential, and why the Itô integral needs its own construction (Shreve II §4.2–4.3).
3. **Random-walk intuition with wrong scaling.** A symmetric walk with step $\pm1$ (not $\pm1/\sqrt n$) has quadratic variation $\to\infty$ and *does not* converge to BM. The correct scaling that produces finite quadratic variation is the essence of the construction.
4. **Believing $W$ is differentiable.** BM is nowhere differentiable; it has no Riemann–Stieltjes derivative. Any "chain rule" for $W$ must go through Itô–Doeblin, not the classical chain rule — see [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|03 · Itô Integral & Doeblin]].

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance I*, Ch 13 (random walk → BM: LLN/CLT MGF proofs, scaling, covariance, first passage & reflection) — the cleanest discrete-to-continuous bridge.
- **Shreve**, *Stochastic Calculus for Finance II*, Ch 3 §3.4 (quadratic variation, Def 3.4.1, Thm 3.4.3, the $dW\,dW=dt$ rules).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 3 §3.1 (exact BM construction, covariance $\min(s,t)$, Brownian bridge).

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Continue: [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|02 · Brownian Motion & Martingales]] · [[foundations/stochastic-calculus/index|Index Hub]]