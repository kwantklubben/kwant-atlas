---
title: "03 — The European Pricing Formulas (Closed Forms, Dividends, FX, Futures)"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - closed-form
  - put-call-parity
  - black-76
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This is the **complete closed-form lookup page** for vanilla European options. The practical objective: one master formula (the *generalized* BSM with cost-of-carry $b$) that specializes to every vanilla model — plain stock, index with dividend yield $q$, currency, and futures. Each specialization is a single change of $b$. Every formula and every number below was verified against Haug's *Complete Guide to Option Pricing Formulas* (numerically reproduced) and cross-checked against Shreve II Ch 4–5 and Hull Ch 15/17/18.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Generalized Black–Scholes–Merton formula (Haug §1.1.6)

$$
\boxed{\;c = S\,e^{(b-r)T}N(d_1) - X\,e^{-rT}N(d_2)\;}
$$
$$
\boxed{\;p = X\,e^{-rT}N(-d_2) - S\,e^{(b-r)T}N(-d_1)\;}
$$
$$
d_1=\frac{\ln(S/X)+\left(b+\tfrac12\sigma^2\right)T}{\sigma\sqrt T},\qquad d_2=d_1-\sigma\sqrt T=\frac{\ln(S/X)+\left(b-\tfrac12\sigma^2\right)T}{\sigma\sqrt T}.
$$

**Cost-of-carry dictionary** — the entire menu is one variable $b$:

| Model | $b$ | Call $c$ |
|---|---|---|
| BSM stock (1973), no div | $r$ | $S\,N(d_1)-X\,e^{-rT}N(d_2)$ |
| Merton (1973), cont. yield $q$ | $r-q$ | $S\,e^{-qT}N(d_1)-X\,e^{-rT}N(d_2)$ |
| Black-76 futures/forward (1976) | $0$ | $e^{-rT}\left[F\,N(d_1)-X\,N(d_2)\right]$ |
| Garman–Kohlhagen currency (1983) | $r-r_f$ | $S\,e^{-r_fT}N(d_1)-X\,e^{-rT}N(d_2)$ |
| Asay margined futures (1982) | $0,\ r{=}0$ | $F\,N(d_1)-X\,N(d_2)$ |

#### 2.2 Put–Call Parity (Haug §1.2; Shreve II 4.5.29; Hull 18.1) — model-free

$$
c-p = S\,e^{(b-r)T}-X\,e^{-rT} = e^{-rT}\left(S\,e^{bT}-X\right).
$$

Special cases: stock $c-p=S-Xe^{-rT}$; continuous yield $c-p=Se^{-qT}-Xe^{-rT}$; futures $c-p=(F-X)e^{-rT}$; currency $c-p=Se^{-r_fT}-Xe^{-rT}$. *Parity is a pure no-arbitrage identity — it holds regardless of volatility and even for non-lognormal dynamics.*

#### 2.3 Price bounds (Hull 17, 18)

$$
c\ge\max\left(S\,e^{(b-r)T}-X\,e^{-rT},\,0\right),\qquad p\ge\max\left(X\,e^{-rT}-S\,e^{(b-r)T},\,0\right).
$$

#### 2.4 Interpretation

- $N(d_2)$ = risk-neutral probability that the option is exercised (Shreve II; Hull 15.8).
- $S\,e^{(b-r)T}N(d_1)$ = discounted expected stock price *in the money* under $\mathbb{Q}$.
- As $\sigma\to0$, a call limits to the forward value $S\,e^{(b-r)T}-X\,e^{-rT}$ (Hull §15.8).
- **American call, no dividends:** early exercise is never optimal, so the BSM formula is *also* the American price (Haug §1.2). American *puts* and dividend-paying calls need the tree/approximation machinery (Haug Ch 3).

---

### 3. Computational Implementation — the full pricing engine

A single function parameterized by $b$, with every specialization verified against Haug's published numbers. Stdlib only.

```python
import math

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bsm_general(S, X, T, r, b, sigma):
    """Generalized BSM (cost-of-carry b). b=r stock, r-q index, 0 futures, r-rf FX."""
    if T <= 0:
        return (max(S - X, 0.0), max(X - S, 0.0))
    d1 = (math.log(S/X) + (b + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    c = S*math.exp((b-r)*T)*N(d1) - X*math.exp(-r*T)*N(d2)
    p = X*math.exp(-r*T)*N(-d2) - S*math.exp((b-r)*T)*N(-d1)
    return c, p

# --- BSM stock, b=r  (Haug numeric: c=2.13337) ---
c, p = bsm_general(60, 65, 0.25, 0.08, 0.08, 0.30)
print(f"BSM call  S=60 X=65 T=.25 r=.08 sigma=.30 : c={c:.5f} (Haug 2.13337)")

# --- Merton, continuous yield q=5% -> b=r-q  (Haug: p=2.46479) ---
c, p = bsm_general(100, 95, 0.5, 0.10, 0.10-0.05, 0.20)
print(f"Merton put S=100 X=95 T=.5 r=.10 q=.05 sigma=.20 : p={p:.5f} (Haug 2.46479)")

# --- Black-76, futures, b=0  (Haug: c=p=1.70105) ---
F, X, T, r, sig = 19.0, 19.0, 0.75, 0.10, 0.28
d1 = (math.log(F/X) + 0.5*sig**2*T)/(sig*math.sqrt(T)); d2 = d1 - sig*math.sqrt(T)
cb = math.exp(-r*T)*(F*N(d1) - X*N(d2))
print(f"Black-76 F=X=19 T=.75 r=.10 sigma=.28 : c={cb:.5f} (Haug 1.70105)")

# --- Garman-Kohlhagen, currency, b=r-rf  (Haug: c=0.029099) ---
S, X, T, r, rf, sig = 1.56, 1.6, 0.5, 0.06, 0.08, 0.12
d1 = (math.log(S/X) + (r-rf+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1 - sig*math.sqrt(T)
cg = S*math.exp(-rf*T)*N(d1) - X*math.exp(-r*T)*N(d2)
print(f"Garman-Kohlhagen S=1.56 X=1.6 T=.5 r=.06 rf=.08 sigma=.12 : c={cg:.6f} (Haug 0.029099)")

# --- Put-call parity + lower bound check ---
c, p = bsm_general(100, 105, 0.5, 0.10, 0.10, 0.20)
lhs = c + 105*math.exp(-0.10*0.5); rhs = p + 100
print(f"parity: C+Xe^-rT={lhs:.5f} == P+S={rhs:.5f}")
print(f"lower bound (S-Xe^-rT)+ = {max(100-105*math.exp(-0.05),0):.5f}  <=  c={c:.5f}")
```
```
BSM call  S=60 X=65 T=.25 r=.08 sigma=.30 : c=2.13337 (Haug 2.13337)
Merton put S=100 X=95 T=.5 r=.10 q=.05 sigma=.20 : p=2.46479 (Haug 2.46479)
Black-76 F=X=19 T=.75 r=.10 sigma=.28 : c=1.70105 (Haug 1.70105)
Garman-Kohlhagen S=1.56 X=1.6 T=.5 r=.06 rf=.08 sigma=.12 : c=0.029099 (Haug 0.029099)
parity: C+Xe^-rT=105.57354 == P+S=105.57354
lower bound (S-Xe^-rT)+ = 0.12091  <=  c=5.69445
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Wrong $b$ for the instrument.** Pricing a currency option with $b=r$ (instead of $r-r_f$) or an index with $b=r$ (instead of $r-q$) misprices by exactly the missing $e^{-qT}$ / $e^{-r_fT}$ factor. The cost-of-carry dictionary is the first thing to check.
2. **Futures vs forward confusion.** Black-76 uses $b=0$ because under $\mathbb{Q}$ a futures price is a *martingale* (drift zero; Hull 18.6; Shreve II 5.6.6). Conflating it with the forward (which has drift $r-q$) changes the $d_1$ drift term.
3. **Dividend handling — yield vs discrete.** The $e^{-qT}$ form is for continuous yield (index/FX); for *known dollar* dividends you replace $S_0\to S_0-I$ (PV of dividends; Hull 15.12), not use the yield form. Mixing them is a classic error.
4. **Parity is only no-arbitrage, not a model statement.** Parity holds for any dynamics; do not read it as evidence the lognormal formula is correct.

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, §1 (all closed forms, §1.1–1.6), §1.2 (parities & symmetries), §1.3 (precursors), §2.10 (ATM approximations). *Numerically verified in the corpus.*
- **Shreve**, *Stochastic Calculus for Finance II*, §4.5 (solution, put formula, parity 4.5.29) and §5.5–5.6 (dividends, forwards/futures).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 15 (BSM, eq. 15.20/15.21), Ch 17 (index/FX), Ch 18 (futures & Black's model, eq. 18.7/18.8).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|02 · PDE & Derivation]]
- Forward: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|04 · Greeks & Hedging]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
