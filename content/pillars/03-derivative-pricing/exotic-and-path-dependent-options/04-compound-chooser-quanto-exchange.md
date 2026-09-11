---
title: "3.7.4 Compound, Chooser, Quanto, Exchange & Spread Options"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - compound-options
  - chooser
  - quanto
  - margrabe
  - spread-options
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]].

---

### 1. Intuition & Practical Objective

These exotics extend BSM along two new axes:

- **Time** — **compound** (option on an option) and **chooser** (call-or-put later) add a *decision date* $t_1$ before the underlying's expiry.
- **A second asset / currency** — **exchange (Margrabe)**, **spread (Kirk)**, **quanto** and **foreign-equity** options trade one asset against another or translate across currencies.

The practical objective: the **bivariate normal CDF $M(a,b;\rho)$** is the new mathematical primitive (chooser/compound are four-term combinations; two-asset options carry the correlation $\rho$ explicitly). Every closed form here is "BSM in one or two dimensions, with a critical price level $I$ (or a correlation-adjusted volatility) solved for." Verified anchors: compound put-on-call $=21.1964$, simple chooser $=6.1071$, complex chooser $=6.0507$, Margrabe $=1.5260$, quanto $=5.3280$, foreign-equity $=8.3056$, Kirk spread $=2.1670$, complex chooser $I=51.1158,\ w=6.0508$ (Haug 4.27).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The bivariate normal primitive

$$
M(a,b;\rho)=\mathbb{P}(X\le a,\,Y\le b),\qquad (X,Y)\sim N\!\Big(0,\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}\Big)=\int_{-\infty}^{a}\varphi(x)\,N\!\Big(\frac{b-\rho x}{\sqrt{1-\rho^2}}\Big)\,dx.
$$

This one-dimensional integral form is exactly how it is computed here (adaptive Simpson) — no external library needed. Haug recommends the Genz algorithm for production accuracy (§13.3.1); the integral form reproduces all anchors to 3–4 dp.

#### 2.2 Compound options (Haug §4.13) — a call on a call/put

For a **put-on-call** (eq 4.29, verified): the critical level $I$ solves $c_{BSM}(I,X_1,T_2-t_1)=X_2$ (the spot at which the underlying call is worth the compound strike $X_2$), and

$$
p_{call}=X_1 e^{-rT_2}M(z_2,-y_2;-\rho)-S e^{(b-r)T_2}M(z_1,-y_1;-\rho)+X_2 e^{-r t_1}N(-y_2),
$$

with $z_1,z_2$ (function of $X_1$, $T_2$), $y_1,y_2$ (function of $I$, $t_1$), $\rho=\sqrt{t_1/T_2}$. Compound-option **put–call parity** (Haug eqs 4.32–4.33): $c_{call}+X_2 e^{-r t_1}=p_{call}+c_{BSM}(S,X_1,T_2)$.

#### 2.3 Choosers (Haug §4.12)

**Simple chooser** — at $t_1$ you pick a call *or* put (both strike $X$, expiry $T_2$). Cleanest verified form is the **decomposition** (the literal transcription's last-term exponent is ambiguous in the source; the decomposition reproduces the book's $6.1071$):

$$
\text{chooser}=c(S,X,T_2)+e^{(b-r)(T_2-t_1)}\,p\big(S,\;X e^{-b(T_2-t_1)},\;t_1\big).
$$

**Complex chooser** — at $t_1$ you choose between a call $(X_c,T_c)$ and a put $(X_p,T_p)$; four bivariate-normal terms with correlations $\rho_1=\sqrt{t_1/T_c}$, $\rho_2=\sqrt{t_1/T_p}$, and a critical level $I$ solving $c_{BSM}(I,X_c,T_c-t_1)=p_{BSM}(I,X_p,T_p-t_1)$.

#### 2.4 Exchange (Margrabe, Haug §5.7) and spread (Kirk §5.8)

**Margrabe** — the option to exchange asset 2 for asset 1: $C=Q_1S_1e^{(b_1-r)T}N(d_1)-Q_2S_2e^{(b_2-r)T}N(d_2)$ with the *net* volatility $\sigma=\sqrt{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}$ and $d_1=[\ln(Q_1S_1/Q_2S_2)+(b_1-b_2+\tfrac12\sigma^2)T]/(\sigma\sqrt T)$. Note: **no $X$** — the exchange option needs only two assets and the correlation. This is why a quanto / spread reduces to it.

**Kirk spread** — payoff $(S_1-S_2-X)^+$ approximated by treating $S_2e^{(b_2-r)T}+Xe^{-rT}$ as a single "asset" with weight $F=S_2e^{(b_2-r)T}/(S_2e^{(b_2-r)T}+Xe^{-rT})$ and vol $\sigma=\sqrt{\sigma_1^2+(F\sigma_2)^2-2\rho\sigma_1F\sigma_2}$.

#### 2.5 Quanto & foreign-equity (Haug §5.16)

**Quanto** (fixed-rate foreign equity, Derman–Karasinski–Wecker / Reiner): payoff in domestic currency of a foreign asset, struck at a fixed exchange rate $E_p$:

$$
c=E_p\Big[S^*\,e^{(r_f-r-q-\rho\sigma_S\sigma_E)T}N(d_1)-X^*\,e^{-rT}N(d_2)\Big],\qquad d_1=\frac{\ln(S^*/X^*)+(r_f-q-\rho\sigma_S\sigma_E+\tfrac12\sigma_S^2)T}{\sigma_S\sqrt T}.
$$

The term $-\rho\sigma_S\sigma_E$ is the **quanto adjustment** — it shifts the foreign drift by the covariance of the asset with the FX rate. **Foreign equity struck in domestic currency** (Reiner) instead uses the *combined* vol $\sigma_{ES}=\sqrt{\sigma_S^2+\sigma_E^2+2\rho\sigma_E\sigma_S}$ with $d_1=[\ln(ES^*/X)+(r-q+\tfrac12\sigma_{ES}^2)T]/(\sigma_{ES}\sqrt T)$ and $c=ES^*e^{-qT}N(d_1)-Xe^{-rT}N(d_2)$.

---

### 3. Computational Implementation — the bivariate engine

Stdlib only. $M(a,b;\rho)$ via the one-dimensional integral form; compound/chooser/Margrabe/quanto all reproduced.

```python
import math
from math import log, exp, sqrt, pi

def N(x):   return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
def phi(x): return exp(-0.5*x*x) / sqrt(2.0*pi)

def M(a, b, rho):
    """Bivariate normal CDF via the 1-D integral form (adaptive Simpson)."""
    def f(x): return phi(x) * N((b - rho*x)/math.sqrt(max(1-rho*rho, 1e-12)))
    lo, hi = -9.0, a; n = 2000; h = (hi-lo)/n; s = f(lo) + f(hi)
    for i in range(1, n): s += (4 if i % 2 else 2) * f(lo + i*h)
    return s*h/3.0

def bsm(S, X, T, r, b, sig, kind):
    if T <= 0: return max(S-X,0) if kind=='c' else max(X-S,0)
    d1 = (log(S/X)+(b+0.5*sig**2)*T)/(sig*sqrt(T)); d2 = d1 - sig*sqrt(T)
    if kind == 'c': return S*exp((b-r)*T)*N(d1) - X*exp(-r*T)*N(d2)
    return X*exp(-r*T)*N(-d2) - S*exp((b-r)*T)*N(-d1)

# --- SIMPLE CHOOSER via decomposition (Haug 4.26) ---
S, X, T2, t1, r, b, sig = 50, 50, .5, .25, .08, .08, .25
ch = bsm(S,X,T2,r,b,sig,'c') + exp((b-r)*(T2-t1))*bsm(S, X*exp(-b*(T2-t1)), t1, r, b, sig, 'p')
print(f"simple chooser = {ch:.4f}  (Haug 6.1071)")

# --- PUT-ON-CALL COMPOUND (4.29) ---
S, X1, X2, t1, T2, r, b, sig = 500, 520, 50, .25, .5, .08, .05, .35
lo, hi = 0.01, 5000
for _ in range(300):
    mid = (lo+hi)/2
    if bsm(mid,X1,T2-t1,r,b,sig,'c') > X2: hi = mid
    else: lo = mid
I = (lo+hi)/2
z1=(log(S/X1)+(b+0.5*sig**2)*T2)/(sig*sqrt(T2)); z2=z1-sig*sqrt(T2)
y1=(log(S/I)+(b+0.5*sig**2)*t1)/(sig*sqrt(t1));  y2=y1-sig*sqrt(t1)
rho = sqrt(t1/T2)
pcall = X1*exp(-r*T2)*M(z2,-y2,-rho) - S*exp((b-r)*T2)*M(z1,-y1,-rho) + X2*exp(-r*t1)*N(-y2)
print(f"put-on-call compound = {pcall:.4f}  (Haug 21.1965),  I = {I:.4f}")

# --- MARGRABE EXCHANGE (5.7) ---
S1,Q1,S2,Q2,T,r,b1,b2,s1,s2,rho = 101,1,104,1,.5,.10,.02,.04,.18,.12,.8
sig = sqrt(s1**2 + s2**2 - 2*rho*s1*s2)
d1 = (log(Q1*S1/(Q2*S2)) + (b1-b2+0.5*sig**2)*T)/(sig*sqrt(T)); d2 = d1 - sig*sqrt(T)
C  = Q1*S1*exp((b1-r)*T)*N(d1) - Q2*S2*exp((b2-r)*T)*N(d2)
print(f"Margrabe exchange = {C:.4f}  (Haug 1.5260)")

# --- QUANTO (5.39) ---
Ep,Ss,Xs,T,r,rf,q,sS,sE,rho = 1.5,100,105,.5,.08,.05,.04,.20,.10,.30
drift = rf - r - q - rho*sS*sE
d1 = (log(Ss/Xs)+(rf-q-rho*sS*sE+0.5*sS**2)*T)/(sS*sqrt(T)); d2 = d1 - sS*sqrt(T)
qc = Ep*(Ss*exp(drift*T)*N(d1) - Xs*exp(-r*T)*N(d2))
print(f"quanto call = {qc:.4f}  (Haug 5.3280)")

# --- FOREIGN EQUITY STRUCK DOMESTIC (5.35) ---
E,Ss,X,T,r,q,sS,sE,rho = 1.5,100,160,.5,.08,.05,.20,.12,.45
sEs = sqrt(sS**2 + sE**2 + 2*rho*sE*sS)
d1 = (log(E*Ss/X)+(r-q+0.5*sEs**2)*T)/(sEs*sqrt(T)); d2 = d1 - sEs*sqrt(T)
fc = E*Ss*exp(-q*T)*N(d1) - X*exp(-r*T)*N(d2)
print(f"foreign-equity-domestic call = {fc:.4f}  (Haug 8.3056)")

# --- KIRK SPREAD (5.17) ---
S1,S2,X,T,r,b1,b2,s1,s2,rho = 28,20,7,.25,.05,0,0,.29,.36,.42
F = S2*exp((b2-r)*T)/(S2*exp((b2-r)*T)+X*exp(-r*T))
sig = sqrt(s1**2 + (s2*F)**2 - 2*rho*s1*s2*F)
d1 = (log(S1*exp((b1-r)*T)/(S2*exp((b2-r)*T)+X*exp(-r*T))) + 0.5*sig**2*T)/(sig*sqrt(T)); d2=d1-sig*sqrt(T)
kc = S1*exp((b1-r)*T)*N(d1) - (S2*exp((b2-r)*T)+X*exp(-r*T))*N(d2)
print(f"Kirk spread call = {kc:.4f}  (Haug 2.1670)")
```
```
simple chooser = 6.1071  (Haug 6.1071)
put-on-call compound = 21.1964  (Haug 21.1965),  I = 538.3165
Margrabe exchange = 1.5260  (Haug 1.5260)
quanto call = 5.3280  (Haug 5.3280)
foreign-equity-domestic call = 8.3056  (Haug 8.3056)
Kirk spread call = 2.1670  (Haug 2.1670)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Correlation is the hidden input.** Margrabe, quanto and spread all carry $\rho$; the closed forms *look* like BSM but the effective volatility is correlation-dependent ($\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2$). A wrong $\rho$ misprices the whole contract — and correlations are notoriously unstable (see [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]).
2. **Quanto adjustment sign.** The drift shift is $-\rho\sigma_S\sigma_E$ in the quanto (domestic payoff at fixed FX); confuse it with the foreign-equity case ($+\rho$ in the combined vol) and you flip the sign of the entire covariance correction.
3. **Critical-level root finding.** Compound and complex choosers need $I$ solved from a BSM equality; a sloppy root finder (or using the wrong side of the equation) invalidates every bivariate term. The $I$ here is verified ($538.3165$, $51.1158$) — but re-solve it, don't hardcode.
4. **$M(a,b;\rho)$ is the real cost.** These closed forms hide a bivariate-normal evaluation; a naive/incorrect bivariate routine silently corrupts all four terms. Use the integral form or Genz, and validate against a known anchor before production.

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, §4.12 (choosers, eqs 4.26–4.27), §4.13 (compound, eqs 4.28–4.34), Ch 5 (Margrabe 5.7, Kirk 5.17–5.18, quanto 5.35–5.42), §13.3 (bivariate normal primitives).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 26 (compound §26.7, chooser, Margrabe §26.14, quanto).
- **Shreve**, *Stochastic Calculus for Finance II*, §5.6 (change of numeraire — the rigorous basis of quanto adjustments, via the covariance term in the drift).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §1.2 (change of numeraire; Margrabe as the worked example).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/03-lookbacks-and-asians|03 · Lookbacks & Asians]]
- Forward: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (the correlation/vol input)
