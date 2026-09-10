---
title: "02 — The Calibration Problem: Objectives, Regularization & Stability"
tags:
  - pillar-derivative-pricing
  - calibration-and-market-practice
  - objective-function
  - regularization
  - least-squares
  - overfitting
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/calibration-and-market-practice/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Once you accept that calibration is a *decision*, the next question is: **which decision?** This page makes the three knobs of that decision precise and shows them fighting each other:

1. **The objective function** — what distance are you minimizing (implied-vol RMSE, price RMSE, relative error)?
2. **The parameterization** — how many dials does the model have, and what shape can it reach?
3. **The regularization** — what penalty keeps the answer stable and non-pathological?

The practical objective is a single discipline: **you want the fit that is good today and not dangerous tomorrow.** A model that nails today's quotes by contorting itself (high-degree smile, over-tuned SABR parameters) is worse than a slightly worse fit that is stable. This is the bias–variance trade-off made concrete: fit error (bias) buys you, in exchange, instability and non-identifiability (variance). Regularization is the control knob between them.

---

### 2. Mathematical Ground Truth & Derivations

**The objective function family.** With residuals $r_i(\\theta) = \\text{model}_i(\\theta) - \\text{market}_i$ in implied-vol, price, or relative-price space, the three standard objectives are

$$\\mathcal{L}_{\\sigma^2} = \\frac{1}{N}\\sum_i \\big(\\hat\\sigma^{\\text{model}}_i - \\hat\\sigma^{\\text{mkt}}_i\\big)^2, \\qquad
\\mathcal{L}_{C^2} = \\frac{1}{N}\\sum_i \\big(C^{\\text{model}}_i - C^{\\text{mkt}}_i\\big)^2, \\qquad
\\mathcal{L}_{\\text{rel}} = \\frac{1}{N}\\sum_i \\Big(\\frac{C^{\\text{model}}_i - C^{\\text{mkt}}_i}{C^{\\text{mkt}}_i}\\Big)^2.$$

Because price is nonlinear in vol (vega $=S e^{(b-r)T} n(d_1)\\sqrt T$ is largest at ATM), $\\mathcal L_{C^2}$ weights ATM strikes far more than $\\mathcal L_{\\sigma^2}$. **Implied vol is the market unit** (it is what is quoted), so desks almost always fit in vol space — a model that reproduces quoted vols is tradeable; one that merely reproduces some prices may not be.

**The bias–variance decomposition** (standard statistics, restated for calibration). For a fitted parameter $\\hat\\theta$:

$$\\mathbb{E}\\big[(\\hat\\theta-\\theta^*)^2\\big] = \\underbrace{\\big(\\mathbb{E}[\\hat\\theta]-\\theta^*\\big)^2}_{\\text{bias}^2} + \\underbrace{\\operatorname{Var}(\\hat\\theta)}_{\\text{variance}},$$

where $\\theta^*$ is the "true" (unknowable) market parameter. A rich model reduces bias (fits today) but inflates variance (noisy, unstable tomorrow). **Regularization trades bias for variance**: minimize

$$\\mathcal J(\\theta) = \\mathcal L(\\theta) + \\lambda \\lVert \\theta-\\theta_0\\rVert^2 \\qquad \\text{(ridge / $\\ell_2$),}$$

pulling $\\hat\\theta$ toward a prior $\\theta_0$ at the cost of a slightly worse fit. In least-squares form with design features, the ridge solution is the classic `$(X^\\top X + \\lambda I)^{-1}X^\\top y$` — adding $\\lambda$ to the diagonal of the (ill-conditioned) normal matrix is *exactly* what stabilizes it.

**The overfitting mechanism, made explicit.** Fitting an $n$-th degree polynomial to $N$ noisy smile points: as $n\\to N$, the in-sample residual $\\to0$ (perfect fit) while the *between-point and extrapolated* behavior becomes wild, because the high-degree coefficients are determined by noise. The second derivative (butterfly) swings sign; the extrapolated vol explodes. Ridge shrinks those coefficients.

---

### 3. Computational Implementation — overfitting vs ridge on a smile

Fit implied-vol slices of increasing polynomial degree to a noisy market smile, then watch the extrapolation destabilize; then show ridge pulling it back. Stdlib only.

```python
import math, random
random.seed(2026)

F = 100.0
ks  = [-0.35,-0.25,-0.15,-0.05,0.0,0.05,0.15,0.25,0.35]
mkt = [0.335,0.295,0.252,0.218,0.205,0.215,0.248,0.288,0.330]
y   = [mkt[i]+random.gauss(0,0.002) for i in range(len(ks))]   # bid/ask noise

def polyval(c,x): return sum(c[i]*x**i for i in range(len(c)))

def fit_poly(xs, ys, degree, lam=0.0):      # ridge-regularized normal equations
    n = degree+1
    G = [[sum(x**(i+j) for x in xs)+(lam if i==j else 0.0) for j in range(n)] for i in range(n)]
    r = [sum(x**i*v for x,v in zip(xs,ys)) for i in range(n)]
    A=[row[:] for row in G]; b=r[:]
    for col in range(n):                     # gaussian elimination
        piv=max(range(col,n),key=lambda rr:abs(A[rr][col]))
        A[col],A[piv]=A[piv],A[col]; b[col],b[piv]=b[piv],b[col]
        for rr in range(col+1,n):
            f=A[rr][col]/A[col][col]
            for cc in range(col,n): A[rr][cc]-=f*A[col][cc]
            b[rr]-=f*b[col]
    x=[0.0]*n
    for rr in range(n-1,-1,-1):
        x[rr]=(b[rr]-sum(A[rr][cc]*x[cc] for cc in range(rr+1,n)))/A[rr][rr]
    return x

for deg in (2, 6):
    c = fit_poly(ks, y, deg)
    rmse = math.sqrt(sum((polyval(c,k)-v)**2 for k,v in zip(ks,y))/len(ks))
    print(f"degree={deg}: in-sample vol RMSE={rmse:.5f}"
          f"   extrapolated vol @k=+0.6: {polyval(c,0.6):.4f}  @k=-0.6: {polyval(c,-0.6):.4f}")

c6 = fit_poly(ks, y, 6)
c6r= fit_poly(ks, y, 6, lam=0.02)
rmse6 = math.sqrt(sum((polyval(c6,k)-v)**2 for k,v in zip(ks,y))/len(ks))
rmseR = math.sqrt(sum((polyval(c6r,k)-v)**2 for k,v in zip(ks,y))/len(ks))
print(f"degree=6 ridge lam=0.02: in-sample RMSE={rmseR:.5f} (vs plain {rmse6:.5f})"
      f"   extrapolated @k=+0.6: {polyval(c6r,0.6):.4f}  @k=-0.6: {polyval(c6r,-0.6):.4f}")
```
```
degree=2: in-sample vol RMSE=0.00818   extrapolated vol @k=+0.6: 0.5689  @k=-0.6: 0.5835
degree=6: in-sample vol RMSE=0.00169   extrapolated vol @k=+0.6: 1.4161  @k=-0.6: 1.0344
degree=6 ridge lam=0.02: in-sample RMSE=0.02443 (vs plain 0.00169)   extrapolated @k=+0.6: 0.4181  @k=-0.6: 0.4317
```
The degree-6 polynomial cuts the in-sample RMSE by $5\\times$ (0.0082 → 0.0017) but extrapolates a *vol of 1.42* where the true smile is ~0.35 — the fit is chasing noise. Ridge costs a little in-sample fit (RMSE 0.024) but restores sane extrapolation (0.42). **This is calibration's central trade-off, in numbers.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Overfitting the smile.** A parameterization with enough knobs can drive today's residuals to zero while being worthless (or dangerous) elsewhere — the degree-6 extrapolation above is the pathology. The market does not quote far wings densely, so those are where overfit surfaces misbehave most.
2. **Objective mismatch.** Fitting price-RMSE instead of vol-RMSE silently biases the fit toward ATM and away from the wings; relative-price error blows up on cheap OTM options. State the objective explicitly (see [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]] table).
3. **Ill-conditioned normal equations.** With collinear parameters the Gram matrix $X^\\top X$ is near-singular; tiny quote noise swings the solution hugely. Ridge ($+\\lambda I$) is the first-principles fix (used directly in **04 · Stochastic Vol** for the $\\kappa/\\xi$ ridge).
4. **Forgetting that a fit is static.** A parameter set that fits today is not a model of tomorrow. The bias–variance knob you set now determines how much the calibration drifts when the market moves — see [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 3 (why parameterizing implied vol directly is hard; SVI as a stable arbitrage-free surface; fitting all expirations simultaneously under no calendar-spread arbitrage).
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 2 (interpolation rules that preserve no-arbitrage — affine-in-$t$ with non-crossing $f$ profiles, eq 2.20), Ch 7 §7.5 (what a calibrated forward-variance model actually fixes).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 (smiles and model calibration in practice).
- **Brigo–Mercurio**, *Interest Rate Models*, Ch 7 (calibration as a sequence of solvable least-squares/cascade steps in the LFM — see [[pillars/03-derivative-pricing/calibration-and-market-practice/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/calibration-and-market-practice/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/calibration-and-market-practice/03-calibrating-local-vol|03 · Calibrating Local Vol]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
