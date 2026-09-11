---
title: "F.4.5 Girsanov's Theorem & the Risk-Neutral Measure"
tags:
  - foundations
  - stochastic-calculus
  - girsanov
  - risk-neutral
  - radon-nikodym
  - market-price-of-risk
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/04-sdes-and-simulation|04 · SDEs & Simulation]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Why does option pricing *ignore the drift of the stock*? Girsanov's theorem is the mechanism. It says: **you can change the probabilities (change measure) so that a Brownian motion *appears* to have a drift — or, in reverse, remove a drift — without changing its volatility, its quadratic variation, or its paths.** The reweighting is done by the Radon–Nikodym derivative $Z(T)$, built from the same exponential-martingale of §02.

The practical objective is one idea, stated sharply: **under the risk-neutral (martingale) measure $\mathbb Q$, every discounted asset price is a martingale, so derivative prices are just discounted $\mathbb Q$-expectations of the payoff.** The *market price of risk* $\Theta=(\mu-r)/\sigma$ is the knob that performs the switch; it converts the physical drift $\mu$ into the risk-free $r$ without touching $\sigma$. Nothing is claimed about what "really happens" — it is a *pricing* measure, not a prediction.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Girsanov, one dimension (Shreve II Thm 5.2.3; Shreve I Thm 1.56; Björk 11.3)
Let $W(t),\,0\le t\le T$ be BM on $(\Omega,\mathcal F,\mathbb P)$, $\Theta$ an adapted process. Define the **Radon–Nikodym derivative / Doléans–Dade exponential**
$$
Z(t)=\exp\Big\{-\!\int_0^t\Theta(u)\,dW(u)-\tfrac12\!\int_0^t\Theta^2(u)\,du\Big\},
$$
and the candidate BM $\widetilde W(t)=W(t)+\int_0^t\Theta(u)du$. Set $\tilde{\mathbb P}(A)=\int_A Z(T)\,d\mathbb P$. Then **under $\tilde{\mathbb P}$, $\widetilde W$ is a Brownian motion.** *(Needs the integrability condition $\mathbb E\int_0^T\Theta^2 Z^2du<\infty$, a Novikov-type condition, for $Z$ to be a genuine martingale — Shreve II footnote to (5.2.13).)*

**Properties (verified):** $Z$ is a $\mathbb P$-martingale with $dZ=-\Theta Z\,dW$, $Z(0)=1$, $\mathbb E Z(t)=1$; change-of-expectation $\tilde{\mathbb E}[X]=\mathbb E[Z(T)X]$; Bayes: $\tilde{\mathbb E}[Y\mid\mathcal F(s)]=\tfrac1{Z(s)}\mathbb E[Y Z(t)\mid\mathcal F(s)]$. **"Means change, variances don't":** the QV is unchanged, only the drift/mean rate shifts ($\mu\to r$); paths and $\sigma$ are untouched (Shreve II 5.2.22–23).

#### 2.2 Market price of risk & the risk-neutral stock (Shreve II 5.2.2; Shreve I §17.2; Glasserman §1.2)
Model $dS=\mu S\,dt+\sigma S\,dW$, discount $D(t)=e^{-\int_0^t R(s)ds}$. With **market price of risk**
$$
\Theta(t)=\frac{\mu(t)-R(t)}{\sigma(t)},
$$
the Girsanov shift makes $dS=\big(R+\sigma\Theta\,\big)S\,dt+\sigma S\,dW=R S\,dt+\sigma S\,d\widetilde W$, and
$$
d(D S)=\sigma D S\big[\Theta\,dt+dW\big]=\sigma D S\,d\widetilde W
$$
is a **$\mathbb Q$-martingale** — exactly the definition of a risk-neutral measure (Shreve II Def 5.4.3). $d\widetilde W=\Theta dt+dW$.

#### 2.3 Risk-neutral pricing formula (Shreve II 5.2.30/31; Björk Thm 10.18; Glasserman eq 1.39)
$$
V(t)=\tilde{\mathbb E}\Big[e^{-\int_t^T R(u)du}\,V(T)\,\Big|\,\mathcal F(t)\Big],
$$
with the money-market-normalized $\mathcal Q$-expectation the "cornerstone equation" of pricing. For constant $r,\sigma$ and a European payoff, this expectation *is* the Black–Scholes formula (Shreve II §5.2.5; Glasserman eq 1.44).

---

### 3. Computational Implementation — verify the martingale & RN price

Stdlib check of the two pillars: (a) under $\mathbb Q$ (drift $r$), $\mathbb E^\mathbb Q[e^{-rT}S_T]=S_0$ (discounted stock is a martingale); (b) the discounted-payoff expectation reproduces the closed-form BSM call, and the market price of risk is computed.

```python
import math, random
random.seed(19)

def bsm_call(S,X,T,r,sig):
    d1=(math.log(S/X)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*0.5*(1+math.erf(d1/math.sqrt(2))) - X*math.exp(-r*T)*0.5*(1+math.erf(d2/math.sqrt(2)))

S0, X, T, r, sig, mu = 100.0, 100.0, 1.0, 0.05, 0.20, 0.15

# (a) Q-martingale: E^Q[e^{-rT} S_T] = S0  (drift = r, not mu!)
disc=[]
for _ in range(300000):
    Wn=random.gauss(0, math.sqrt(T))
    ST=S0*math.exp((r-0.5*sig*sig)*T + sig*Wn)
    disc.append(math.exp(-r*T)*ST)
print("E^Q[e^-rT S_T] = %.4f   (theory S0 = %.2f)" % (sum(disc)/len(disc), S0))

# (b) RN pricing formula vs BSM closed form
tot=0.0
for _ in range(300000):
    Wn=random.gauss(0, math.sqrt(T))
    ST=S0*math.exp((r-0.5*sig*sig)*T + sig*Wn)
    tot += max(ST-X, 0.0)
price = tot/300000*math.exp(-r*T)
print("V(0)=e^-rT E^Q[(S_T-K)^+] = %.4f   (BSM closed = %.4f)" % (price, bsm_call(S0,X,T,r,sig)))

# (c) market price of risk
Theta=(mu-r)/sig
print("market price of risk Theta=(mu-r)/sigma = %.2f   (so drift mu -> r)" % Theta)
```
```
E^Q[e^-rT S_T] = 100.0116   (theory S0 = 100.00)
V(0)=e^-rT E^Q[(S_T-K)^+] = 10.4270   (BSM closed = 10.4506)
market price of risk Theta=(mu-r)/sigma = 0.50   (so drift mu -> r)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Discounting under the wrong measure.** $e^{-rT}\mathbb E^{\mathbb P}[(S_T-K)^+]$ depends on $\mu$ and is *not* the price; only the $\mathbb Q$-expectation (drift $r$) is correct. This is the most common pricing bug in the wild ([[foundations/stochastic-calculus/06-advanced-extensions|06 · Feynman–Kac]] makes them equal *only* under $\mathbb Q$).
2. **Girsanov's integrability condition ignored.** Going through the formal computation without $\mathbb E\int_0^T\Theta^2Z^2du<\infty$ (Novikov) can produce a $Z$ that is a strict *local* martingale, not a martingale — and then $\mathbb E Z(T)\ne1$ and the measure change is invalid (a flagged omission in the corpus; Shreve II 5.2.13 footnote).
3. **Believing risk-neutral probabilities are "real."** $\mathbb Q$ is a reweighting that makes discounted prices martingales; it does not describe physical outcomes. Extrapolating $\mathbb Q$-statistics (e.g. $\mathbb E[W]$) as physical forecasts is a category error.
4. **Market price of risk needs $\sigma\ne0$.** $\Theta=(\mu-r)/\sigma$ is meaningless where the stock has no random component ($\sigma=0$); then there is no randomness to hedge and no drift to remove. Degenerate cases like this are how complete-market assumptions silently break (Shreve II §5.3).

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 5 (RN derivative machinery 5.2.1, Girsanov 5.2.3, stock under $\mathbb Q$, market price of risk, RN pricing 5.2.30/31, BSM by RN expectation §5.2.5).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 17 (Girsanov, risk-neutral measure) & Ch 12 (market price of risk, Cameron–Martin–Girsanov).
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 11 (martingale representation, Girsanov, Novikov), Ch 12 (BS from a martingale view; market price of risk $\lambda=(\alpha-r)/\sigma$).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §1.2 (radon–Nikodym, change-of-numeraire, market price of risk).

---

### 6. Connected Graph Bridges

- Back: [[foundations/stochastic-calculus/04-sdes-and-simulation|04 · SDEs & Simulation]]
- Forward: [[foundations/stochastic-calculus/06-advanced-extensions|06 · Advanced Extensions]] · [[foundations/stochastic-calculus/index|Index Hub]]
- Application: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] · [[pillars/03-derivative-pricing/black-scholes-merton/01-from-zero-intuition|BSM 01 · From Zero]]