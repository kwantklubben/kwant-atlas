---
title: "05 — Failure Modes & Real-World Practice"
tags:
  - pillar-quantitative-risk
  - credit-risk-and-the-merton-model
  - failure-modes
  - jump-to-default
  - credit-spread-puzzle
  - model-risk
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/04-reduced-form-and-cds|04 · Reduced-Form & CDS]] and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/03-distance-to-default-and-pd|03 · Distance-to-Default & PD]].

---

### 1. Intuition & Practical Objective

The Merton model is *mathematically exact and empirically wrong in four specific ways*. This page names them precisely, so a practitioner knows which assumption to distrust and how the failure shows up in money terms. The objective is not cynicism — it is knowing exactly where credit risk modelling becomes an approximation, so the residual can be measured and managed.

The four failures, in one line each:

1. **Firm value is unobservable** — the model inverts equity into $(V,\sigma_V)$; that inversion is ill-conditioned and amplifies input error into PD.
2. **No jumps → no jump-to-default** — a pure diffusion cannot produce a sudden collapse, so it badly understates short-horizon default.
3. **The credit-spread puzzle** — the model's own spreads are orders of magnitude too small at short maturities, so it cannot be trusted for spread quoting.
4. **Defaults are correlated** — every single-name model is silent about the joint event that actually kills a portfolio.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Where the assumptions live

Every Merton result rests on four interlocking assumptions:
- **(A1) Observable, lognormal firm value** — one diffusion with *constant* $\sigma_V$; the model's inputs $(V_0,\sigma_V)$ must be *inferred*, not observed.
- **(A2) Debt is a single zero-coupon bond; default only at $T$.** No interim defaults, coupons, covenants, or rollover.
- **(A3) Continuous, frictionless markets; no jump-to-default, no illiquidity.** Else the no-arbitrage replication underlying the call price fails.
- **(A4) Constant $r$, known and constant recovery.** Recovery is a *fraction of firm value* in the model ($R_V=V/D$ relationship), not of face.

#### 2.2 Failure 1 — the ill-conditioned inversion

DD and PD are defined through $(\ln(V/D),\sigma_V)$, but we *solve* for $V,\sigma_V$ from equity observables whose levels are noisy. Differentiating the vol identity $\sigma_E E=N(d_1)\sigma_V V$ shows $\partial\sigma_V/\partial\sigma_E>0$ with an elasticity greater than one near the money — equity-vol error is *amplified* into asset-vol error, and PD is convex in $\sigma_V$. Page 03's firm shows the effect: a $+1\%$ relative error in $\sigma_E$ moves PD by $\approx 9\%$.

#### 2.3 Failure 4 — correlation is the whole portfolio story

For a portfolio of $n$ loans with PDs $p_i$ and pairwise default correlation $\rho$, the unexpected loss satisfies (Bluhm 2010, eq. 1.13)
$$\mathrm{UL}^2=\sum_i p_i(1-p_i)+2\rho\sqrt{p_1(1-p_1)\,p_2(1-p_2)}\quad(\text{2 loans}),$$
and in general $\mathrm{UL}^2=\sum_{i,j}\rho_{ij}\sqrt{p_i(1-p_i)\,p_j(1-p_j)}$. When $\rho=0$ risk diversifies to $\sum p_i(1-p_i)$; when $\rho=1$ the portfolio behaves as **one obligor with $n$-fold intensity** — pure concentration risk. A single-name model has no $\rho$ in it at all; that is why portfolio credit risk needs the factor model of page 06.

---

### 3. Computational Implementation — the failures, measured

**Experiment 1 — PD sensitivity and the credit-spread puzzle.** Stdlib only.

```python
import math

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def solve_merton(E0, sigE, D, T, r, tol=1e-14, itmax=5000):
    V, sigV = E0 + D * math.exp(-r * T), sigE * (E0 / (E0 + D * math.exp(-r * T)))
    for _ in range(itmax):
        d1 = (math.log(V / D) + (r + 0.5 * sigV**2) * T) / (sigV * math.sqrt(T))
        d2 = d1 - sigV * math.sqrt(T)
        Vn = (E0 + D * math.exp(-r * T) * N(d2)) / N(d1)
        sv = sigE * E0 / (V * N(d1))
        if abs(Vn - V) < tol and abs(sv - sigV) < tol:
            V, sigV = Vn, sv; break
        V, sigV = Vn, sv
    d1 = (math.log(V / D) + (r + 0.5 * sigV**2) * T) / (sigV * math.sqrt(T))
    return V, sigV, d1 - sigV * math.sqrt(T)

E0, D, T, r = 100.0, 350.0, 1.0, 0.05
print("PD sensitivity to equity volatility (asset-value error amplification):")
for sigE in (0.36, 0.38, 0.40, 0.42, 0.44):
    V, sigV, d2 = solve_merton(E0, sigE, D, T, r)
    print(f"  sigmaE={sigE:.2f}: sigmaV={sigV:.4f}  PD={N(-d2)*1e4:7.2f} bp")
a = N(-solve_merton(E0, 0.400, D, T, r)[2]); b = N(-solve_merton(E0, 0.404, D, T, r)[2])
print(f"  +1% relative sigmaE -> PD {a*1e4:.2f} -> {b*1e4:.2f} bp  (ratio {b/a:.3f})")

print("\nMerton credit-spread puzzle (T=1, r=5%):")
for Dd in (350.0, 320.0, 300.0):
    V, sigV, d2 = solve_merton(E0, 0.40, Dd, T, r)
    d1 = (math.log(V / Dd) + (r + 0.5 * sigV**2) * T) / (sigV * math.sqrt(T))
    F = Dd * math.exp(-r * T) * N(d2) + V * N(-d1)
    R = -math.log(F / Dd) / T
    print(f"  D={Dd:.0f}: PD={N(-d2)*1e4:6.1f}bp  model spread={(R - r)*1e4:.2f}bp (market often 100-200bp)")
```
```
PD sensitivity to equity volatility (asset-value error amplification):
  sigmaE=0.36: sigmaV=0.0832  PD=   9.21 bp
  sigmaE=0.38: sigmaV=0.0879  PD=  16.19 bp
  sigmaE=0.40: sigmaV=0.0926  PD=  26.35 bp
  sigmaE=0.42: sigmaV=0.0973  PD=  40.33 bp
  sigmaE=0.44: sigmaV=0.1021  PD=  58.66 bp
  +1% relative sigmaE -> PD 26.35 -> 28.82 bp  (ratio 1.094)

Merton credit-spread puzzle (T=1, r=5%):
  D=350: PD=  26.4bp  model spread=0.71bp (market often 100-200bp)
  D=320: PD=  24.3bp  model spread=0.69bp (market often 100-200bp)
  D=300: PD=  22.8bp  model spread=0.68bp (market often 100-200bp)
```
Two first-principles failures in numbers: PD rises **super-linearly** with equity vol (a $1\%$ input error becomes a $\sim9\%$ PD error), and the model's credit spread is under **$1$ bp** for a firm the market would charge $100{+}$ bp — Merton (1974) famously under-predicts short-maturity spreads because it forces default to the maturity date.

**Experiment 2 — jump-to-default.** Add an independent Poisson(λ) collapse on top of the Merton diffusion. Default now arrives either as a jump or as a diffusion breach at $T$, giving the closed form
$$\mathrm{PD}_{\text{jump}}=\big(1-e^{-\lambda T}\big)+e^{-\lambda T}N(-d_2).$$

```python
import math, random

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

V, sigV, d2 = 432.9067, 0.0926, 2.7900        # from the worked firm (pages 02-03)
D, T, r, lam_j = 350.0, 1.0, 0.05, 0.01        # 1% annual jump intensity
PD_mer = N(-d2)
PD_jump = (1 - math.exp(-lam_j * T)) + math.exp(-lam_j * T) * PD_mer
print(f"Merton PD = {PD_mer*1e4:.2f} bp")
print(f"with Poisson jump (lam=1%/yr): PD = {PD_jump*1e4:.2f} bp")

# Monte Carlo confirmation of the jump-augmented PD
random.seed(3)
ns, cnt = 400000, 0
for _ in range(ns):
    if random.random() < 1 - math.exp(-lam_j * T):   # jump to default
        cnt += 1; continue
    Z = random.gauss(0.0, 1.0)
    VT = V * math.exp((r - 0.5 * sigV**2) * T + sigV * math.sqrt(T) * Z)
    if VT < D:
        cnt += 1
print(f"MC ({ns} paths) PD = {cnt/ns*1e4:.2f} bp")
```
```
Merton PD = 26.35 bp
with Poisson jump (lam=1%/yr): PD = 125.59 bp
MC (400000 paths) PD = 126.58 bp
```
A mere $1\%$ annual jump intensity **nearly quintuples** the default probability, because the jump term dominates at short horizons where the diffusion is nearly default-free. This is the structural model's missing catastrophe, and precisely why **reduced-form/intensity models dominate practice for short-dated credit** (page 04).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Unobservable asset value (A1).** The model's inputs are inferred, not observed; the inversion is ill-conditioned and PD is convex in the inferred $\sigma_V$ — $1\%$ in, $9\%$ out (Experiment 1).
2. **No jump-to-default (A3).** A diffusion cannot collapse; adding the smallest realistic jump channel multiplies PD several-fold (Experiment 2). This is the single most important structural defect and the reason markets are priced with intensities.
3. **The credit-spread puzzle (A2).** Merton spreads are far below market at short maturities (Experiment 1), because default is forced to $T$ and the firm cannot default between coupons. Black–Cox first-passage barriers and jump-diffusion partially repair this.
4. **Correlation (A4).** Single-name models contain no $\rho$; portfolio risk is *entirely* a correlation story (Bluhm eq. 1.13), and the Gaussian-copula correlation that credit markets used was not a physical quantity — its mis-estimation underpriced mezzanine tranches in 2008.
5. **Recovery and LGD are random.** Recovery is correlated with default rates and varies with seniority; treating it as a constant biases every derived intensity and CVA.
6. **Model risk per se.** Swapping $D$ for the KMV default point $D^{*}=\mathrm{ST}+\tfrac12\mathrm{LT}$, or changing the horizon, moves the answer without changing the data — exactly the "right model, wrong inputs" failure Derman (1996) warned about, and a required item under SR 11-7.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives* — §24.5 (risk-neutral vs real-world PD), §24.6 (Merton equity inversion), §24.3 (recovery, average $\approx40\%$). *Verification report in the corpus.*
- **Merton (1974)** — §V–VI (the comparative statics that make spreads too small; coupon/callable extensions). *Primary source.*
- **Gregory, Jon** — *The xVA Challenge* (5th ed., 2025) — §17.6.4 (jump-to-default: intensity models *cannot* reproduce observed jump risk; Levy–Levin 83% implied jumps for AAA), §17.6 (wrong-way risk), §3.3.5 (recovery/LGD conventions). *Corpus digest available.*
- **Bluhm, Overbeck & Wagner** — *Introduction to Credit Risk Modeling* (2010) — §1.2 (portfolio UL, eq. 1.13; concentration vs diversification). *Corpus digest available.*
- **Derman, Emanuel** — *Model Risk* (1996) — the taxonomy of model error; the frame for failure #6.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/04-reduced-form-and-cds|04 · Reduced-Form & CDS]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/03-distance-to-default-and-pd|03 · DD & PD]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/06-advanced-extensions|06 · Portfolio Credit & Vasicek]]
- Siblings: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]] (the jump/thin-tail problem) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & ES]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk]]
