---
title: "06 — Advanced Extensions: Rough Heston, Markovian Lifts, VIX in Rough Vol & Microstructural Foundations"
tags:
  - pillar-derivative-pricing
  - rough-volatility-and-fractional-models
  - rough-heston
  - markovian-lift
  - vix
  - hawkes-process
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/02-the-rough-bergomi-model|02 · The rBergomi Model]].

---

### 1. Intuition & Practical Objective

rBergomi is the *minimal* rough model. This page maps the ladder of extensions, each fixing a specific shortcoming:

| rBergomi limitation | extension | what it buys |
|---|---|---|
| no characteristic function, non-Markovian, MC-only pricing | **rough Heston** (El Euch–Rosenbaum) | an affine-in-$\mathbb E[\int v]$ fractional Riccati system ⇒ semi-explicit Fourier pricing |
| simulation is slow (singular kernel, many steps) | **multifactor Markovian lifts** (rational approximations, small-$\varepsilon$ OU towers) | near-Markovian proxies with standard MC/PDE machinery |
| VIX/realized-variance joint fit to SPX is hard | **VIX-aware calibration** (Jacquier–Martini–Muguruza) | closed-form VIX futures ⇒ joint SPX/VIX calibration |
| H≈0.1 lacks a microstructural *explanation* | **Hawkes foundations** (Jaisson–Rosenbaum; Bacry–Muzy) | rough vol as the scaling limit of nearly-unstable heavy-tailed Hawkes flows |

The practical objective: know which extension is the right answer for which problem, what it costs (parameters, tractability, identifiability), and which are desk-ready versus research-frontier. The one thing to internalise: **every extension buys tractability at the price of either more parameters or an approximation error, and the empirical anchor is always the same — the H≈0.1 roughness and the $\psi(T)\propto T^{H-\frac12}$ skew.**

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Rough Heston (El Euch–Rosenbaum 2019)

Replace the Heston variance SDE's $dW$ with a fractional/Volterra driver:

$$v_t=v_0+\frac{1}{\Gamma(\alpha)}\int_0^t(t-s)^{\alpha-1}\kappa(\theta-v_s)\,ds+\frac{\nu}{\Gamma(\alpha)}\int_0^t(t-s)^{\alpha-1}\sqrt{v_s}\,dW_s,\qquad \alpha=H+\tfrac12,$$

with $0<\alpha<\tfrac12$ (the rough regime). The key tractability: the fractional Riccati system has a closed form, so the log-price characteristic function is

$$\varphi_t(u)=\exp\!\Big(\mathbb E\!\Big[\int_0^t v_s\,ds\Big]\Psi(u,t)+\dots\Big),$$

where $\Psi$ solves a fractional Riccati ODE (a Mittag-Leffler-type function). This restores a Fourier-pricing route that rBergomi lacks. Short-time ATM skew again behaves as $T^{\alpha-\frac12}=T^{H}$, and the model is *richer*: it reproduces both the rough skew and, via the $\mathbb E[\int v]$ leverage, the variance-swap/VIX structure.

#### 2.2 Multifactor Markovian lifts

The singular Volterra kernel $(t-u)^{\alpha-1}$ can be approximated by a sum of exponentials, yielding a *finite-dimensional* Markovian representation of the fractional driver:

$$(t-u)^{\alpha-1}\approx\sum_{j=1}^{M}w_j e^{-\kappa_j(t-u)},$$

so the fractional integral $\int_0^t(t-u)^{\alpha-1}X_udW_u$ becomes a sum of $M$ OU-like factors. This is the "rational approximation" programme (Harang–Langrené; Bayer–Friz; Abi Jaber–El Euch): $M$ factors of spectral accuracy capture the short-time skew to arbitrary precision, and then standard MC/PDE/Fourier machinery applies. Cost: $M$ extra state variables and a delicate small-$t$ blowup to preserve.

#### 2.3 VIX in rough vol (Jacquier–Martini–Muguruza 2018)

VIX is (a scaling of) the 30-day variance-swap variance $\frac{1}{\tau}\int_t^{t+\tau}\xi_t(u)du$. Because $\xi_t(u)$ is a lognormal forward-variance, VIX futures are $\mathbb E[\sqrt{\cdot}]$ — a concave functional, so VIX futures trade *below* the VS strike by Jensen (the same convexity gap as in the Markovian two-factor model of [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|SV · 06 Advanced Extensions]]). In rough vol this gap is a *closed form* for the futures price, which is what makes joint SPX/VIX calibration feasible without nested simulation.

#### 2.4 Hawkes microstructural foundations (Jaisson–Rosenbaum 2016)

Rough vol has a bottom-up explanation: a **nearly-unstable Hawkes process** (a self-exciting point process whose branching ratio approaches 1 from below) converges, under a heavy-tailed jump distribution and in the right rescaling, to a fractional process with $H<1/2$. In Jaisson–Rosenbaum, the *order flow* of price jumps is a Hawkes process; its cumulative intensity converges to a rough fractional diffusion — so the $H\approx0.1$ roughness is *emergent from microstructure* rather than an exogenous assumption. This is the deepest of the extensions: it turns rough vol from a fit into a scaling limit.

---

### 3. Computational Implementation — the short-end blowup that a Markovian lift cannot fake

We demonstrate the structural obstruction at the heart of the lift programme: the rough Volterra kernel $(x)^{H-\frac12}$ **diverges** as $x\to0$, while *any* finite sum of exponentials (the Markovian representation) is **bounded** there. This is precisely why a naive finite-factor approximation fails at the short end, and why the rigorous lifts add a dedicated small-time factor. Stdlib only.

```python
import math
# Rough Volterra kernel vs finite Markovian (exponential-sum) representation.
#   Kernel g(x)=x^{H-1/2}: DIVERGES as x->0 (H<1/2).
#   Any finite exponential tower sum_j w_j e^{-kappa_j x} is BOUNDED as x->0 (-> sum w_j).
#   => a finite Markovian lift can never reproduce the short-end blowup of the kernel.
def kernel(x,H): return x**(H-0.5) if x>0 else float('inf')
def finite_exp_tower(x, M, k0=1.0, growth=2.5):
    tot=0.0
    for j in range(M):
        tot+=math.exp(-k0*growth**j*x)   # weights set to 1 for the boundedness point
    return tot
print("== boundedness test: rough kernel x^{H-1/2} vs any finite Markovian (exponential) tower ==")
print("   H=0.14: kernel -> inf as x->0; finite tower -> finite (sum of M weights)")
print(f"    {'x':>9} {'kernel x^{H-1/2}':>16} {'tower M=5':>10} {'tower M=20':>11}")
for x in (1.0, 0.1, 0.01, 1e-3, 1e-5):
    print(f"    {x:9.2e} {kernel(x,0.14):16.4f} {finite_exp_tower(x,5):10.4f} {finite_exp_tower(x,20):11.4f}")
print("   -> as x->0 the tower -> M (bounded), the kernel -> inf : a Markovian lift MUST add a")
print("      dedicated small-time factor to carry the short-dated skew blowup.")
print()
print("== rough-Heston short-time skew exponent vs rBergomi T^{H-1/2} (identical by construction) ==")
for H in (0.10, 0.14, 0.30):
    print(f"    H={H:4.2f}:  exponent H-1/2 = {H-0.5:.3f}  ->  psi(T) ~ T^{H-1/2} in both models")
```
```
== boundedness test: rough kernel x^{H-1/2} vs any finite Markovian (exponential) tower ==
   H=0.14: kernel -> inf as x->0; finite tower -> finite (sum of M weights)
            x kernel x^{H-1/2}  tower M=5  tower M=20
     1.00e+00           1.0000     0.4519      0.4519
     1.00e-01           2.2909     2.4486      2.4487
     1.00e-02           5.2481     4.4368      4.9026
     1.00e-03          12.0226     4.9365      7.4095
     1.00e-05          63.0957     4.9994     12.4347
   -> as x->0 the tower -> M (bounded), the kernel -> inf : a Markovian lift MUST add a
      dedicated small-time factor to carry the short-dated skew blowup.

== rough-Heston short-time skew exponent vs rBergomi T^{H-1/2} (identical by construction) ==
    H=0.10:  exponent H-1/2 = -0.400  ->  psi(T) ~ T^-0.4 in both models
    H=0.14:  exponent H-1/2 = -0.360  ->  psi(T) ~ T^-0.36 in both models
    H=0.30:  exponent H-1/2 = -0.200  ->  psi(T) ~ T^-0.2 in both models
```

**Reading the output.** The boundedness test is the honest heart of the lift problem: as $x\to0$, the rough kernel $x^{H-\frac12}$ grows without bound ($1.00\to63.10$ as $x:1\to10^{-5}$), while the finite exponential tower is trapped below its finite weight-sum ($5$ for $M{=}5$, $20$ for $M{=}20$). The tower can match the kernel at *intermediate* lags but is structurally incapable of the short-end divergence that carries the ATMF skew $\psi(T)\propto T^{H-\frac12}$. That is exactly why the rigorous Markovian lifts (Harang–Langrené, Abi Jaber–El Euch) wrap a dedicated small-time factor around the exponential tower. The second block confirms the *structural* consistency: rough Heston and rBergomi share the same short-time skew exponent $H-\tfrac12$ by construction — the roughness is carried by the single parameter $H$, whichever model you price with.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using a naive exponential lift for the short end.** As §3 shows, a plain sum of exponentials *cannot* reproduce the divergent $x^{H-\frac12}$ kernel near $x=0$ (error $\to100\%$). A correct lift needs a small-time blow-up factor; otherwise the short-dated skew is silently capped and you've reverted to a Markovian model.
2. **Rough Heston is affine in $\int v$, not in $v$.** Its tractability rests on the fractional Riccati structure of the *integrated* variance; mistaking it for standard Heston's affine-in-$v$ characteristic function breaks the derivation.
3. **Joint SPX/VIX calibration is not free.** It requires the VIX futures *closed form*; without it (i.e. nested simulation) the joint fit is numerically prohibitive. Adopt the closed-form route (JMM 2018) or accept the cost.
4. **Hawkes foundations are a scaling limit, not the model.** The microstructural derivation is asymptotic (nearly-unstable branching, heavy tails, specific rescaling); it motivates and explains $H<1/2$ but does not hand you a calibrated pricing model. Don't present the micro-foundation as a pricing alternative.
5. **H remains the empirical anchor.** Every extension is calibrated to the same $H\approx0.1$ (variogram) and $\psi(T)\propto T^{H-\frac12}$ (skew). If an extension needs a different $H$ to fit, that is a red flag, not a free parameter.
6. **More parameters always fit better.** The rough-Heston and lift programmes add parameters; the relevant test is whether they change a *dynamic* quantity (VIX term structure, SSR, forward skew) in the direction the market says — otherwise they are unidentifiable noise (the same lesson as [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|SV · 06 Advanced Extensions]]).

---

### 5. Canonical Literature & Study References

- **El Euch & Rosenbaum (2019)**, *The characteristic function of rough Heston models*, Mathematical Finance 29(1), 3–38 — the fractional Riccati system and the (semi-)closed-form characteristic function.
- **Jaisson & Rosenbaum (2016)**, *Rough fractional diffusions as scaling limits of nearly unstable heavy tailed Hawkes processes*, Annals of Applied Probability 26(5), 2860–2882 — the microstructural (Hawkes) foundation of roughness.
- **Jacquier, Martini & Muguruza (2018)**, *On VIX futures in the rough Bergomi model*, Quantitative Finance 18(1), 45–61 — closed-form VIX futures and joint SPX/VIX calibration.
- **Abi Jaber & El Euch (2019)** and **Harang & Langrené (2019)**, multifactor/rational Markovian approximations of the Volterra kernel — the lift programme of §2.2.
- **Bayer, Friz & Gatheral (2016)**, *Pricing under rough volatility*, Quantitative Finance 16(6), 887–904 — the rBergomi base model.
- **Bacry & Muzy (2014)**, *Hawkes model for price and trades high-frequency dynamics* — the Hawkes framing of price jumps.
- **Gatheral, Jaisson & Rosenbaum (2018)**, *Volatility is rough*, Quantitative Finance 18(6), 933–949 — the empirical anchor ($H\approx0.1$).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/index|Index Hub]]
- Sibling / back-references: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|SV · 06 Advanced Extensions]] (the launchpad that first flagged rough vol) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR (flat note)]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|VS · 06 Advanced Extensions]]
- Forward: [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Calibration & Market Practice]] (fitting rough vol to SPX/VIX) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Quantitative Risk (VaR/ES)]] (fat tails, model risk) · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] (fractional / Volterra calculus)
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (point processes, Hawkes) · [[foundations/numerical-methods/index|Numerical Methods]] (MC, approximation theory)
