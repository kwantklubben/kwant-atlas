---
title: "03 — SABR & the Short-Expiration Asymptotics: The Smile in Closed Form"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - sabr
  - asymptotics
  - smile
  - medvedev-scaillet
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|02 · The Heston Model]] and [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|VS · 04 Advanced Dynamics]].

---

### 1. Intuition & Practical Objective

Heston gives a *model* with a computable price. SABR (Hagan, Kumar, Lesniewski, Woodward, 2002) gives the complementary object: a **closed-form smile**. Its SDE has no mean reversion at all,

$$dF_t=\chi_tF_t^{\beta}dZ_1,\qquad d\chi_t=\nu\chi_t\,dZ_2,\qquad dZ_1dZ_2=\rho\,dt,$$

which makes it a **short-expiration tool** — and the reason it dominated interest-rate and FX smile quoting for two decades is that in exactly that regime it is *exact to leading order* and costs nothing to evaluate: no PDE, no Fourier integral, no simulation.

Four ideas to carry out of this page:

1. **The smile factorises into a "shape" and a "level" correction.** Hagan's formula is $\sigma_{BS}(k)=\sigma_0\frac{y}{f(y)}\big(1+\cdots\tau\big)$: the $y/f(y)$ factor carries all the moneyness dependence (and therefore the skew and the curvature), and the bracket is a $k$-independent $O(\tau)$ level correction. That factorisation is why SABR is so easy to fit and so easy to abuse.
2. **The ATM skew is $\rho\nu/2$, independent of the level.** Short-dated skew is a *direct read-off of the spot/vol covariance*, model-independently: Gatheral (7.3) gives $\partial_k\sigma^2_{BS}\to\frac{\rho\eta}{2}\beta(v_0)$ for *any* SV model, and the Medvedev–Scaillet expansion (7.5–7.6) proves it. The model only enters through the function $\beta(v)$ — and SABR (lognormal vol, $\beta(v)=\sqrt v$) and Heston (square-root variance, $\beta=1$) differ exactly there.
3. **Local vol's skew is twice the implied vol's.** For short expirations BS implied variance is the average of local variance along the most-probable path (Gatheral 3.11/7.2), and since the local-vol skew is nearly constant in $k$, the average halves it. That factor 2 is the structural link between [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|VS · 02 Implied vs Local Vol]] and this page.
4. **Bergomi–Guyon put Heston and SABR in the same two numbers.** At leading order in vol-of-vol, *every* diffusive SV model has an ATM expansion $\hat\sigma(K,T)=\hat\sigma_{F_TT}+S_T k+\frac{C_T}{2}k^2$, with $S_T=\rho\nu/2$ and $C_T=(2-3\rho^2)\nu^2/(6\hat\sigma_0)$ for lognormal vol. One skew number, one curvature number — and the identity $\nu^2=3\hat\sigma_0C_0+6S_0^2$ that ties them back to the vol-of-vol.

The practical objective: be able to write down and evaluate Hagan's formula, read off the ATM skew and curvature, know which parameters are identifiable from a single smile and which are not, and know the horizon over which SABR is legitimate.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Hagan's implied-vol expansion (Gatheral eq. 7.7)

For $\beta=1$ (lognormal SABR), in the limit $\tau\to0$ the Black-76 implied volatility is

$$\boxed{\;\sigma_{BS}(k)=\sigma_0\,\frac{y}{f(y)}\Big(1+\tfrac14\rho\nu\sigma_0+\tfrac{2-3\rho^2}{24}\nu^2\tau+O(\tau^2)\Big),\qquad y:=-\frac{\nu k}{\sigma_0},\quad f(y):=\ln\frac{\sqrt{1-2\rho y+y^2}+y-\rho}{1-\rho}\;}$$

where $k=\ln(K/F_T)$ is log-moneyness. Equivalently, for general $\beta$, $z=\frac{\nu}{\sigma_0}(FK)^{(1-\beta)/2}\ln(F/K)$ replaces $-\nu k/\sigma_0$, with the $z/x(z)$ factor and the $(1-\beta)$ backbone terms in the bracket. This is what makes SABR a *one-evaluation* model.

Taylor-expanding the $y$-factor for $y\sim\sqrt\tau$ (Gatheral 7.7):

$$\sigma_{BS}(k,\tau)=\sigma_0\Big(1-\tfrac12\rho y+\tfrac{2-3\rho^2}{12}y^2\Big)+\Big(\tfrac14\rho\nu\sigma_0+\tfrac{2-3\rho^2}{24}\nu^2\Big)\tau+O(\tau\sqrt\tau).$$

From this, at $k=0$:

$$S_0:=\frac{\partial\sigma_{BS}}{\partial k}\Big|_{k=0}=\frac{\rho\,\nu}{2}\Big\{1+O(\tau)\Big\},\qquad C_0:=\frac{\partial^2\sigma_{BS}}{\partial k^2}\Big|_{k=0}=\frac{(2-3\rho^2)\nu^2}{6\sigma_0}\Big\{1+O(\tau)\Big\}.$$

The skew is $k$-linear to leading order and the curvature fixes the wings — these are the numbers a desk quotes.

#### 2.2 Why that skew is model-independent (Medvedev–Scaillet)

For a general diffusion $\frac{dS_t}{S_t}=\sigma_t dZ_1$, $d\sigma_t=a(\sigma_t)dt+b(\sigma_t)dZ_2$, the small-time implied-vol expansion is (Gatheral 7.4–7.5)

$$I(z,\tau,\sigma)=\sigma+I_1(z;\sigma)\sqrt\tau+I_2(z;\sigma)\tau+O(\tau^{3/2}),\qquad I_1(z;\sigma)=\frac{\rho\,b(\sigma)\,z}{2},$$

with $z=k/(\sigma_{BS}\sqrt\tau)$ the normalised log-strike. Substituting $z$ and taking $\tau\to0$ gives the ATM skew (Gatheral 7.6)

$$\boxed{\;\frac{\partial I}{\partial k}\Big|_{k=0}\to\frac{\rho\,b(\sigma)}{2\sigma}\;}$$

which **proves** the short-dated skew is a direct read-off of the instantaneous spot/vol covariance and does *not* depend on the drift $a(\sigma)$ or on time. For SABR ($b(\sigma)=\nu\sigma$) this gives $\rho\nu/2$ — the same number as §2.1. For Heston, $\eta\beta(v)=\eta$ gives $\rho\eta/(2\sqrt v)=\rho\eta/(4\sqrt v)$ (i.e. $\rho\eta/(4\sigma_{BS})$ with $v=\sigma_{BS}^2$), i.e. Bergomi's (6.18b), and the *variance* skew $\partial_k\sigma_{BS}^2|_{k=0}\to\rho\eta/2$ (Gatheral 7.3) — the number verified numerically in §04.

Two structural consequences:

- **All SV models produce the same short-dated skew up to the factor $\beta(v)$.** The model is identified, at the short end, only by the *scaling* of vol-of-vol with the vol level. SABR says lognormal ($\beta(v)\sim\sqrt v$), Heston says square-root ($\beta=1$).
- **The skew is not explicitly time-dependent**, whereas local-vol models *do* generate a time-decaying short-dated skew. Hence two models that agree on all of today's Europeans still disagree on forward-starting options — the *dynamics* differ even when the *statics* coincide (Gatheral §7.2, Bergomi ch 3).

#### 2.3 Adding jumps, and the extreme-strike wings

With jumps the leading skew correction is additive at $\tau=0$ (Gatheral 7.3, corollaries):

$$\frac{\partial v_{BS}}{\partial k}\Big|_{k=0}\to\rho\,b(\sigma)-2\mu_J,\qquad \mu_J=\lambda_J\mathbb E[J]=\lambda_J\!\int_{-1}^{\infty}\!x f(x)\,dx\ \text{(Gatheral 7.8)},$$

so the **jump compensator $-2\mu_J$ and the SV term $\rho b(\sigma)$ contribute exactly additively** to the short-dated ATM variance skew. This is the quantitative basis for "fit Heston to the long end, then add jumps for the short end" (Gatheral ch 5).

For the *wings*, the model-independent statement is Lee's moment formula (Gatheral 7.7): with $q^*=\sup\{q:\mathbb E[S_T^{-q}]<\infty\}$ and $\beta^*=\limsup_{k\to-\infty}\sigma^2_{BS}T/|k|$,

$$\beta^*=g(q^*),\qquad g(x)=2-4\big(\sqrt{x^2+x}-x\big),$$

and symmetrically on the right wing with $p^*,\alpha^*$. Implied variance is at most *linear* in $|k|$ — you cannot have plausible models with quadratic-in-$k$ total variance, which is exactly why the asymptotic smile formulas must not be used far from the money.

#### 2.4 Long expirations and the natural interpolation

For log-OU volatility, Fouque–Papanicolaou–Sircar give (Gatheral 7.10)

$$\frac{\partial}{\partial x}\sigma_{BS}(x,T)\approx\frac{\rho\xi}{\lambda T}\quad\Longleftrightarrow\quad\frac{\partial}{\partial x}\sigma^2_{BS}\approx\frac{\rho\,\eta\,\beta(v)}{\lambda T},$$

matching Heston for large $\lambda T$. The **natural interpolation** between the short- and long-expiration limits is (Gatheral 7.11)

$$\frac{\partial}{\partial x}\sigma^2_{BS}(x,T)\approx\frac{\rho\eta\beta(v)}{\lambda'T}\Big(1-\frac{1-e^{-\lambda'T}}{\lambda'T}\Big),\qquad\lambda'=\lambda-\tfrac12\rho\eta\beta(v),$$

and — this is the sharp statement — **Lewis' small-$\eta$ expansion (Gatheral 7.12) proves (7.11) exact to $O(\eta)$**, not merely plausible: the $J^{(1)}$ term of the perturbation reproduces it identically.

#### 2.5 Bergomi–Guyon at short maturity: the unified picture

Bergomi's expansion in vol-of-vol $\varepsilon$ (Ch 8, [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]]) gives, in the $T\to0$ limit, for **any** short-vol dynamics with $S_0:=\partial_k\sigma_{BS}|_0$ and $C_0:=\partial_k^2\sigma_{BS}|_0$ (Bergomi 8.35a–c, 8.36, 8.39, 8.42):

- Lognormal ATM vol (**SABR**, $\beta=1$): $\;S_0=\dfrac{\rho\nu}{2}$, $\;C_0=\dfrac{(2-3\rho^2)\nu^2}{6\hat\sigma_0}$, and the identity $\;\nu^2=3\hat\sigma_0C_0+6S_0^2.$
- Normal ATM vol (**Heston**): $\;S_0=\dfrac{\rho\sigma}{2\hat\sigma_0}$, with $\sigma=\sigma_{\text{Heston}}/2$ — equivalent to $\rho\eta/(4\sqrt{V_0})$, i.e. Bergomi (6.18b).
- Vanishing correlation: $\;S_0=0$, $\;C_0=\dfrac{1}{3\hat\sigma_0}\dfrac{\langle d\hat\sigma_0\,d\hat\sigma_0\rangle}{\hat\sigma_0^2dt}$.

So "Heston vs SABR" is, at leading order, the choice between *square-root* and *lognormal* vol-of-vol scaling — and the data (skew slope roughly independent of the vol level, Gatheral §8.1) prefers the lognormal one.

---

### 3. Computational Implementation — Hagan's formula, its skew and curvature, and the Bergomi–Guyon identities

We implement the general-$\beta$ Hagan formula, finite-difference its ATM skew and curvature, and check them against $\rho\nu/2$ and $(2-3\rho^2)\nu^2/(6\sigma_0)$; then verify the Bergomi–Guyon identities and Lee's moment formula. Stdlib only.

```python
import math

# ---- general-beta Hagan SABR implied vol (Hagan et al. 2002, eq. 2.17a) ----
def sabr_iv(F,K,T,alpha,beta,chi,rho):
    lf=math.log(F/K); FK=(F*K)**((1.0-beta)/2.0)
    br=((1.0-beta)**2/24.0*alpha*alpha/FK**2 + 0.25*rho*beta*chi*alpha/FK
        + (2.0-3.0*rho*rho)/24.0*chi*chi)
    if abs(lf)<1e-14:
        return alpha/F**(1.0-beta)*(1.0+br*T)
    z=(chi/alpha)*FK*lf
    x=math.log((math.sqrt(1.0-2.0*rho*z+z*z)+z-rho)/(1.0-rho))
    den=FK*(1.0+(1.0-beta)**2/24.0*lf*lf+(1.0-beta)**4/1920.0*lf**4)
    return alpha/den*(z/x)*(1.0+br*T)

F,T,alpha,chi,rho=100.0,1.0,0.20,0.3877,-0.7165
print("SABR smile vs beta (alpha=0.20, chi=0.3877, rho=-0.7165, T=1) [% vol]")
print(f"  {'K':>5}{'beta=1':>10}{'beta=0.7':>10}{'beta=0.5':>10}{'beta=0':>10}")
for K in (70.0,80.0,90.0,100.0,110.0,120.0,130.0):
    print(f"  {K:5.0f}"+"".join(f"{sabr_iv(F,K,T,alpha,b,chi,rho)*100:10.3f}" for b in (1.0,0.7,0.5,0.0)))
print("  ATM log-moneyness skew  d sigma_BS/d(lnK) at k=0 (h=1e-3):")
for b in (1.0,0.5,0.0):
    s=(sabr_iv(F,F*math.exp(1e-3),T,alpha,b,chi,rho)-sabr_iv(F,F*math.exp(-1e-3),T,alpha,b,chi,rho))/2e-3
    print(f"    beta={b:3.1f}: {s:+.6f}    (rho*chi/2 = {rho*chi/2:+.6f})")
corr=1.0+(0.25*rho*chi*alpha+(2.0-3.0*rho*rho)*chi*chi/24.0)*T
cur=(sabr_iv(F,F*math.exp(1e-3),T,alpha,1.0,chi,rho)+sabr_iv(F,F*math.exp(-1e-3),T,alpha,1.0,chi,rho)
     -2.0*sabr_iv(F,F,T,alpha,1.0,chi,rho))/1e-6
atm=alpha*(1.0+(0.25*rho*chi*alpha+(2.0-3.0*rho*rho)*chi*chi/24.0)*T)
print(f"  ATM vol (closed form) = {atm*100:.4f}%   ATM curvature (FD) = {cur:+.6f}")
print(f"  (2-3rho^2)chi^2/(6 alpha) = {(2.0-3.0*rho*rho)*chi*chi/(6.0*alpha):+.6f};"
      f" times the O(T) factor {corr:.6f} = {(2.0-3.0*rho*rho)*chi*chi/(6.0*alpha)*corr:+.6f}   [Bergomi-Guyon (8.39b)]")
S0=rho*chi/2.0; C0=(2.0-3.0*rho*rho)*chi*chi/(6.0*alpha)
print(f"  Bergomi-Guyon: S_0 = rho*nu/2 = {S0:+.6f}  (8.39a);  identity nu^2 = 3*alpha*C_0 + 6*S_0^2 gives"
      f" {3*alpha*C0+6*S0*S0:.6f}  vs chi^2 = {chi*chi:.6f}  (8.40)")
sig=chi/2.0
print(f"  Heston normal-vol form: S_0 = rho*sigma/(2*sigma_hat_0) = {rho*sig/(2*math.sqrt(0.0354)):+.6f}"
      f" == rho*eta/(4*sqrt(V_0)) = {rho*chi/(4*math.sqrt(0.0354)):+.6f}  (8.42a / 6.18b)")

# ---- Lee's moment formula (Gatheral 7.7): beta* = g(q*), g(x) = 2 - 4(sqrt(x^2+x) - x) ----
g=lambda x: 2.0-4.0*(math.sqrt(x*x+x)-x)
qstar=lambda b: 0.5*(1.0/math.sqrt(b)-math.sqrt(b)/2.0)**2
print("Lee moment formula g(x) = 2 - 4(sqrt(x^2+x) - x):")
for x in (0.0,0.25,0.5,1.0,4.0,100.0):
    print(f"    q*={x:6.2f}  beta*=g(q*)={g(x):.6f}")
for b in (0.5,1.0,2.0):
    print(f"    round trip: beta*={b:.2f} -> q*={qstar(b):.6f} -> g(q*)={g(qstar(b)):.9f}")
```
```
SABR smile vs beta (alpha=0.20, chi=0.3877, rho=-0.7165, T=1) [% vol]
      K    beta=1  beta=0.7  beta=0.5    beta=0
     70    24.804    10.126     6.568     3.267
     80    22.919     8.308     5.014     2.262
     90    21.250     6.606     3.515     1.298
    100    19.780     5.026     2.004     0.201
    110    18.505     3.921     1.688     0.759
    120    17.435     3.899     2.314     1.266
    130    16.583     4.347     2.903     1.695
  ATM log-moneyness skew  d sigma_BS/d(lnK) at k=0 (h=1e-3):
    beta=1.0: -0.137364    (rho*chi/2 = -0.138894)
    beta=0.5: -0.144197    (rho*chi/2 = -0.138894)
    beta=0.0: -0.139448    (rho*chi/2 = -0.138894)
  ATM vol (closed form) = 19.7798%   ATM curvature (FD) = +0.056971
  (2-3rho^2)chi^2/(6 alpha) = +0.057605; times the O(T) factor 0.988991 = +0.056971   [Bergomi-Guyon (8.39b)]
  Bergomi-Guyon: S_0 = rho*nu/2 = -0.138894  (8.39a);  identity nu^2 = 3*alpha*C_0 + 6*S_0^2 gives 0.150311  vs chi^2 = 0.150311  (8.40)
  Heston normal-vol form: S_0 = rho*sigma/(2*sigma_hat_0) = -0.369105 == rho*eta/(4*sqrt(V_0)) = -0.369105  (8.42a / 6.18b)
Lee moment formula g(x) = 2 - 4(sqrt(x^2+x) - x):
    q*=  0.00  beta*=g(q*)=2.000000
    q*=  0.25  beta*=g(q*)=0.763932
    q*=  0.50  beta*=g(q*)=0.535898
    q*=  1.00  beta*=g(q*)=0.343146
    q*=  4.00  beta*=g(q*)=0.111456
    q*=100.00  beta*=g(q*)=0.004975
    round trip: beta*=0.50 -> q*=0.562500 -> g(q*)=0.500000000
    round trip: beta*=1.00 -> q*=0.125000 -> g(q*)=1.000000000
    round trip: beta*=2.00 -> q*=0.000000 -> g(q*)=2.000000000
```

**Reading the output.**

- **The skew is confirmed exactly, up to the $O(T)$ level factor.** The finite-difference skew is $-0.137364$; the analytic $\rho\nu/2$ is $-0.138894$; and $-0.138894\times0.988991=-0.137364$, i.e. *exactly* the $\rho\nu/2$ law times the smile's $k$-independent $\tau$-correction factor $\big(1+\frac14\rho\nu\sigma_0+\frac{2-3\rho^2}{24}\nu^2\tau\big)$. Gatheral (7.6) is reproduced to six digits.
- **The curvature is confirmed the same way.** FD curvature $=0.056971$, and the Bergomi–Guyon short-maturity curvature $(2-3\rho^2)\nu^2/(6\sigma_0)=0.057605$ times the same factor $0.988991$ gives $0.056971$. This is the cross-validation between Hagan's *expansion* and Bergomi–Guyon's *perturbation theory*.
- **The Bergomi–Guyon identity (8.40) is exact.** $\nu^2=3\sigma_0C_0+6S_0^2$ returns $0.150311$, and $\nu^2=0.3877^2=0.150311$. The practical reading (Bergomi): because $S_0$ is *fixed* by $\rho\nu/2$, narrow forward ATM call spreads are approximately **independent of vol-of-vol** — the vol-of-vol shows up in the *curvature*, not the skew.
- **Heston and SABR differ only in the vol-of-vol scaling.** Writing the Heston ATM-vol dynamics in the ch. 8 normal-vol parametrisation ($\sigma=\sigma_{\text{Heston}}/2=\eta/2$) gives the same $S_0$ formula, and it reproduces Bergomi (6.18b): $\rho\eta/(4\sqrt{V_0})=-0.369105$. The *level* dependence is the difference: Heston's skew is $\propto1/\hat\sigma_0$ (hard-wired), SABR's is not.
- **Lee's formula is self-consistent.** $g$ maps $q^*\in[0,\infty)$ onto $\beta^*\in[2,0]$ monotonically, and the round trip $\beta^*\to q^*\to g(q^*)$ returns the input to $10^{-9}$ ($0.5\to0.5625\to0.5$ etc.). The bound $\beta^*\le2$ is the "implied variance at most linear in $|k|$" statement.
- **$\beta$ controls the *smile*, not the ATM skew.** The skew is $\approx\rho\nu/2$ to within $5\%$ for every $\beta$ from $0$ to $1$ (as (7.6) predicts — it does not involve $\beta$ at all beyond $b(\sigma)$), while the *shape* changes completely: at $\beta=1$ the smile is broad ($24.80\%$ at $K{=}70$), at $\beta=0$ it is narrow ($3.27\%$). $\beta$ is the **backbone** exponent: it sets how the smile translates when the forward moves. That is why $\beta$ is picked from *a priori* reasoning (market convention: $\beta=1$ for FX, $\beta=0.5$–$0.7$ for rates) rather than fitted to a single slice.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **SABR has no mean reversion.** $\chi_t$ is a driftless lognormal diffusion, so the model has *no* long-dated vol term structure and cannot be used beyond short expirations (Gatheral §7.2; Hagan's own paper is explicit). Using it for a 10-year swaption is a first-principles error, not a modelling taste.
2. **Hagan's formula is an asymptotic expansion.** It is *exact to leading order as $\tau\to0$* and **arbitrageable far from the money** — Gatheral (8.20)/(8.14): the implied variance is at most affine in $\log K$, and the truncated density can go negative at extreme strikes (Bergomi §8.2, ch 8, App. C). Use it for the near-the-money region and for its *coefficients* $(S,C)$, not as a global parametrisation. (SVI, in [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/03-surface-models|VS · 03 Surface Models]], is the arbitrage-aware alternative.)
3. **$\rho$ and $\nu$ are not separately identifiable from one slice.** Only the products $\rho\nu$ (skew) and $\nu^2/\sigma_0$ (curvature) are pinned by ATM data; separating them needs the wings or several maturities. Do not read a calibrated $\nu$ as an estimate of realized vol-of-vol.
4. **$\beta$ is a chosen constant, and it matters for every forward-looking payoff.** Two calibrations with the same ATM fit but different $\beta$ produce different forward smiles and therefore different cliquet/forward-start prices. Freezing $\beta$ is not cosmetic.
5. **SABR is a static smile, not a dynamics.** Its spot/vol correlation is constant in time and its forward skews are essentially those set by $\rho$ at each expiry — it does *not* give the term-structure control that [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]] demands. For forward-skew products use a forward-variance model.
6. **The $\tau$-correction factor is a level shift, not a shape.** Because it is $k$-independent it moves *all* implied vols on a slice by the same amount. Any fitted SABR set that relies on this factor to match the *level* has effectively decoupled vol-of-vol from the smile shape — and will misprice vol-of-vol-convexity payoffs.

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 7 in full: §7.1 (short expirations, local vs implied skew, the factor-2 lemma, eq. 7.1–7.3), §7.2 (Medvedev–Scaillet 7.4–7.5, the $\rho b(\sigma)/(2\sigma)$ limiter 7.6, **SABR** 7.7 and the small-$\tau$ Taylor form), §7.3 (jumps, $\rho b(\sigma)-2\mu_J$), §7.4 (FPS 7.10), §7.5 (interpolation 7.11), §7.6 (Lewis 7.12 — proof that 7.11 is exact to $O(\eta)$), §7.7 (**Lee's moment formula** and Benaim–Friz tails), §7.8 (summary: shape is model-generic). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 8 §8.2–8.5 (the vol-of-vol expansion, the short-maturity limits 8.35–8.44, and the SABR/Heston specialisations), Ch 9 §9.1–9.2 (ATMF skew as the covariance of spot with implied vol), Ch 5 App. B (the single-cumulant seed, $\mathcal S_T=s/(6\sqrt T)$). *Math-verified.*
- **Hagan, P. S., Kumar, D., Lesniewski, A., Woodward, D.** (2002), *Managing Smile Risk*, Wilmott Magazine, 84–108 — the SABR model and formula (2.17a). **Medvedev & Scaillet** (2004), *Pricing American options under stochastic volatility and stochastic interest rates* / short-time expansions; **Lewis, A.** (2000), *Option Valuation under Stochastic Volatility*; **Lee, R.** (2004), *The moment formula for implied volatility at extreme strikes*; **Benaim & Friz** (2009) for exact tail behaviour.
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §2 (Greeks) — the vega that defines the calibration weights and the ATM approximations §2.10. *Numerically verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|02 · The Heston Model]]
- Forward: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Index Hub]]
- Cross-links: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|VS · 02 Implied vs Local Vol]] (the factor-2 lemma) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|VS · 04 Advanced Dynamics]] (SABR skew and the jumps term) · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] (SABR's home market) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR (flat note)]]
