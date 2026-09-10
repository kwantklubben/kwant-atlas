---
title: "06 — Advanced Extensions: Delta–Gamma VaR, Cornish–Fisher, and Limit Systems"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - delta-gamma-var
  - cornish-fisher
  - risk-limits
  - frtb-sbm
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/02-var-definition-and-flaws|VaR: Definition & Flaws]].

---

### 1. Intuition & Practical Objective

Two things turn a pile of sensitivities into a risk-management system:

1. **A number.** The *delta–gamma* (a.k.a. quadratic) approximation puts the second-order term back into VaR, so that a quantile can be computed from sensitivities alone — no full revaluation, no Monte Carlo. This is the RiskMetrics/Hull framework, and it is the reason a bank can compute a portfolio VaR in milliseconds for a trading desk that reprices a million instruments.
2. **A constraint.** **Limit systems** convert sensitivities into a governance structure: a maximum delta, a maximum gamma, a vega bucket cap, a VaR limit, an escalation procedure. The sensitivity vector is not an *answer*; it is the *unit of account* in which risk appetite is written.

The key insight this page delivers: **the sign of the gamma determines the direction of the error in a delta-normal VaR.** Long gamma makes the P&L distribution positively skewed, thinning the left tail — so delta-normal VaR *overstates*. Short gamma does the reverse and delta-normal *understates* the exact case a limit system exists to catch.

---

### 2. Mathematical Ground Truth & Derivations

**The two models (Hull §22.5, eq. 22.6–22.8).**

- **Linear (delta-normal):** with exposure vector $b$, factor covariance $\Sigma$, and horizon $h$,
$$\Delta V=b^\top\Delta f,\qquad \mathrm{VaR}_\alpha=z_\alpha\sqrt{b^\top\Sigma b}\quad\bigl(=z_\alpha\,|\delta|\,\sigma S\sqrt h\ \text{for one equity factor}\bigr).$$
Assumes the P&L is **normal**, i.e. that the portfolio is **linear** in the factors. It is exactly a *sensitivity* method: it needs only deltas.

- **Quadratic (delta–gamma):** with the Hessian $H$ (gamma and cross-gamma),
$$\Delta V=b^\top\Delta f+\tfrac12\Delta f^\top H\Delta f .$$
For a single equity factor with $\Delta S=\sigma S Z,\ Z\sim N(0,1)$, this is a **quadratic form in a normal**:
$$\Delta V=aZ+bZ^2,\qquad a=\delta\,\sigma S,\quad b=\tfrac12\gamma\,\sigma^2S^2 .$$

**Exact moments of $aZ+bZ^2$** (derived from $\mathbb{E}[Z^2]=1,\ \mathbb{E}[Z^4]=3,\ \mathbb{E}[Z^6]=15$):

$$\mathbb{E}[\Delta V]=b,\quad \operatorname{Var}(\Delta V)=a^2+2b^2,\quad
\gamma_1=\frac{6a^2b+8b^3}{(a^2+2b^2)^{3/2}},\quad
\gamma_2^{\text{ex}}=\frac{3a^4+60a^2b^2+60b^4}{(a^2+2b^2)^2}-3 .$$

Note the pure-gamma limit ($a=0$): $\gamma_1=2\sqrt2\approx2.83$ and $\gamma_2^{\text{ex}}=12$ — the moments of a $\chi^2_1$, as they must be. **A gamma-only position is a chi-square, not a normal**, and calling it normal is a modelling error with a known, computable size.

**The Cornish–Fisher quantile correction.** The true quantile of a skewed, fat-tailed distribution is approximated from the normal quantile $z$:

$$z^{\text{CF}}_\alpha=z+\frac{(z^2-1)}{6}\gamma_1+\frac{(z^3-3z)}{24}\gamma_2-\frac{(2z^3-5z)}{36}\gamma_1^2,\qquad
\mathrm{VaR}^{\Delta\gamma}_\alpha=-\mathbb{E}[\Delta V]+\sqrt{\operatorname{Var}}\;z^{\text{CF}}_{\alpha}\bigl(-\,\gamma_1,\gamma_2\bigr),$$

with the skewness sign flipped because VaR is a quantile of the **loss** $L=-\Delta V$.

**Limit systems (the governance layer).** Typical structure, in the units established on the index page:

| Limit type | Unit | Measures | Failure it prevents |
|---|---|---|---|
| Delta limit | shares / $\$$ notional | directional exposure | concentrated directional bets |
| Gamma limit | $\Delta$-change per $1\%$ move | convexity / realised-vs-implied | being short the crash convexity |
| Vega limit | $\$$ per vol point, **bucketed by expiry** | vol exposure | unhedged surface shape |
| Theta limit | $\$$ per day | carry bleed | slow insolvency of a long-gamma book |
| **VaR / ES limit** | currency, one-day or ten-day | the aggregate | the whole |
| Stress limit | currency, per scenario | non-linearity beyond the model | the tail the model cannot see |

**The escalation rule that makes limits real:** limits are *hard* at the desk level (breach $=$ mandatory reduction next session) and *soft* at the division level (breach $=$ notification and a remediation plan). Without a stated action, a limit is a report. This is where the sensitivity machinery connects to policy — see [[pillars/04-quantitative-risk/basel-and-regulation|Basel & Regulation]] for the same structure at regulatory scale (the FRTB sensitivities-based method prescribes **delta, vega and curvature** buckets, which is this page's mathematics written into capital law).

---

### 3. Computational Implementation — delta-normal vs delta-gamma vs full revaluation, and a limit dashboard

One Monte Carlo run prices the *truth*. Then the two sensitivity models are compared for a **long** and a **short** gamma book, showing that the error flips sign with the position — the central practical message of this folder. Stdlib only.

```python
import math, random
def N(x):   return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)
def bsm(S,X,T,r,b,sig):
    d1=(math.log(S/X)+(b+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return (S*math.exp((b-r)*T)*N(d1)-X*math.exp(-r*T)*N(d2), d1, d2)

z99 = 2.3263478740408408
S,X,T,r,b,sig = 100.,100.,0.5,0.05,0.05,0.20
h  = 1.0/252.0                       # one-day horizon
sd = sig*math.sqrt(h)                # daily vol of the factor
c0, d1, d2 = bsm(S,X,T,r,b,sig); n1=phi(d1); e=math.exp((b-r)*T); sq=math.sqrt(T)
D = e*N(d1)                          # delta
G = e*n1/(S*sig*sq)                  # gamma

# ---------- ground truth: full-revaluation Monte Carlo, one run ----------
random.seed(20260910); m = 2_000_000
long_loss, short_loss = [], []
for _ in range(m):
    dS = S*sd*random.gauss(0,1)                     # 1-day normal factor move
    dP = bsm(S+dS,X,T,r,b,sig)[0] - c0              # FULL revaluation
    long_loss.append(-100.0*dP); short_loss.append(+100.0*dP)
long_loss.sort(); short_loss.sort()

def delta_gamma_CF(qty):
    """Closed-form delta-gamma VaR with the Cornish-Fisher correction."""
    a  = qty*D*sd*S
    bb = 0.5*qty*G*(sd*S)**2
    var = a*a + 2*bb*bb; std = math.sqrt(var)
    mu3 = 6*a*a*bb + 8*bb**3
    mu4 = 3*a**4 + 60*a*a*bb*bb + 60*bb**4
    g1  = mu3/std**3                      # skewness of P&L
    g2  = mu4/std**4 - 3.0                # excess kurtosis of P&L
    skewL, kurtL, z = -g1, g2, z99        # moments of the LOSS
    zcf = z + (z*z-1)*skewL/6 + (z**3-3*z)*kurtL/24 - (2*z**3-5*z)*skewL*skewL/36
    return (-bb) + std*zcf, a, bb, std, g1, g2, zcf

for qty, losses, name in ((+100., long_loss, "LONG  100 calls"),
                          (-100., short_loss,"SHORT 100 calls")):
    k  = int(0.99*m)
    mcVaR = losses[k-1]
    mcES  = sum(losses[k:])/(m-k)
    dnVaR = z99*abs(qty*D)*sd*S                        # delta-normal
    dgVaR,a,bb,std,g1,g2,zcf = delta_gamma_CF(qty)     # delta-gamma
    print(f"{name}: delta-normal VaR={dnVaR:.4f} ({100*(dnVaR-mcVaR)/mcVaR:+.2f}%)   "
          f"delta-gamma VaR={dgVaR:.4f} ({100*(dgVaR-mcVaR)/mcVaR:+.2f}%)   MC VaR={mcVaR:.4f}  MC ES={mcES:.4f}")
    print(f"   a={a:+.4f} b={bb:+.4f} std={std:.4f} skew(PnL)={g1:+.6f} exkurt={g2:.6f} z_CF={zcf:.6f}")

# ---------- the limit dashboard written from the same sensitivities ----------
net = {"delta":59.7734, "gamma":2.7359, "vega/pt":27.3587, "theta/day":-2.2236}
lim = {"delta":100.0,   "gamma":2.5,     "vega/pt":30.0,     "theta/day":3.0}
print(f"\n{'risk':<10}{'net':>10}{'limit':>9}{'util %':>9}  status")
for k in net:
    u = abs(net[k])/lim[k]*100
    print(f"{k:<10}{net[k]:>10.4f}{lim[k]:>9.1f}{u:>9.2f}  {'BREACH' if u>100 else 'ok'}")
print(f"{'VaR 1d 99%':<10}{163.1099:>10.4f}{200.0:>9.1f}{163.1099/200*100:>9.2f}  ok")
```
```
LONG  100 calls: delta-normal VaR=175.1914 (+7.41%)   delta-gamma VaR=163.4461 (+0.21%)   MC VaR=163.1099  MC ES=184.4278
   a=+75.3075 b=+2.1713 std=75.3700 skew(PnL)=+0.172757 exkurt=0.039804 z_CF=2.197391
SHORT 100 calls: delta-normal VaR=175.1914 (-6.19%)   delta-gamma VaR=186.9374 (+0.10%)   MC VaR=186.7489  MC ES=215.9900
   a=-75.3075 b=-2.1713 std=75.3700 skew(PnL)=-0.172757 exkurt=0.039804 z_CF=2.451453

risk             net    limit   util %  status
delta        59.7734    100.0    59.77  ok
gamma         2.7359      2.5   109.44  BREACH
vega/pt      27.3587     30.0    91.20  ok
theta/day    -2.2236      3.0    74.12  ok
VaR 1d 99%  163.1099    200.0    81.55  ok
```

**Four readings.**

1. **The error flips sign with the position, and this is the whole lesson.** Delta-normal VaR is **$+7.41\%$ too high** for the long-gamma book and **$-6.19\%$ too low** for the short-gamma book — using the *identical* volatility, delta magnitude and confidence level. The difference is the sign of $b=\tfrac12\gamma\sigma^2S^2$, i.e. the skewness of the P&L. **A delta-only VaR is conservative for the option buyer and dangerously optimistic for the option seller.**
2. **Delta-gamma is accurate to a fraction of a percent** in both cases ($+0.21\%$, $+0.10\%$) at a one-day horizon — which is exactly why it survived as the industry's pre-Monte-Carlo workhorse, and exactly why it fails over ten days or in stress (see [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **The chi-square limit is visible in the moments.** For a gamma-dominated position ($a\to0$) the formulas give skewness $2\sqrt2$ and excess kurtosis $12$; here $a=75.3$ dwarfs $b=2.17$, so the deviations are small ($\gamma_1=\pm0.173$) — *but the sign is the sign of the position*.
4. **Delta-normal alone would have passed this book.** The dashboard's delta utilisation is $59.77\%$ — comfortable — while the **gamma limit is in breach at $109.44\%$**. A limit system that watches only delta (or only VaR) reports this book as fine. The gamma and vega columns are not decoration; they are the limits that bind.

> **The FRTB echo.** The sensitivities-based method in Basel's Fundamental Review of the Trading Book requires exactly these three buckets — **delta, vega, curvature** — risk-weighted and aggregated per risk class. The regulatory capital regime is this page's mathematics, with the aggregation rules fixed by law. See [[pillars/04-quantitative-risk/basel-and-regulation|Basel & Regulation]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Cornish–Fisher is an expansion, not a distribution.** It is a truncated cumulant series; for extreme skew/kurtosis (short-dated gamma books, deep tails) the corrected quantile can become non-monotone or even exceed the feasible range. Always sanity-check $z^{\text{CF}}$ against the second model.
2. **Delta-gamma assumes the *factor* is normal.** The quadratic form handles the portfolio's non-linearity but not the factor's fat tails. Both errors must be handled: non-linearity by the Hessian, fat tails by the factor distribution (EVT / historical simulation).
3. **Cross-gamma is where multi-factor books hide.** With $N$ factors the Hessian has $N(N-1)/2$ cross terms; most systems report only the diagonal. A book of options on correlated underlyings has a large off-diagonal exposure that is invisible in a per-factor gamma report.
4. **Limits without an action are reports.** The mechanism that makes a limit a limit is the stated consequence of breach, the escalation path, and the *time* allowed to cure. A limit system is an operating procedure with arithmetic attached, not the reverse.
5. **Limits must be in the same units as the hedge.** A vega limit in raw units while the desk hedges per-point is a $100\times$ mismatch; a theta limit per trading day while the report is per calendar day is a $45\%$ mismatch. Unit mismatches are the most common cause of a limit system that appears to work and does not.
6. **A VaR limit is not a stress limit.** The 99% one-day quantile says nothing about a five-sigma week. Every sensitivity-based VaR limit must be paired with a scenario/stress limit that is *not* derived from the same local model (see [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]]).

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 22 §22.5 (the linear model eq. 22.6 and the quadratic delta–gamma model eq. 22.7/22.8 with cross-gamma $\gamma_{ij}$; Cornish–Fisher for non-normal percentiles) and §22.6–22.8 (MC comparison, backtesting). *Verified in the corpus (`hull_ch19-23.md`).*
- **J.P. Morgan / RiskMetrics**: *Technical Document*, 4th ed. (1996) — the original delta-gamma methodology for options under delta-normal VaR; the practical template every bank copied.
- **Dowd, Kevin**: *Measuring Market Risk* (2nd ed., 2005) — the clearest self-contained derivation of delta-normal and delta-gamma VaR and the Cornish–Fisher correction.
- **Fisher, R. A. & Cornish, E. A.**: *Moments and Cumulants in the Specification of Distributions*, *Biometrika* **30**(3–4):262–291 (1938) — the quantile expansion itself.
- **Alexander, Carol**: *Market Risk Analysis, Vol. IV (Value at Risk Models)* (2008) — the accuracy limits of quadratic approximations and the crossover point to full-revaluation VaR.
- **BCBS**: *Minimum Capital Requirements for Market Risk* (January 2019, d457 — **FRTB**) — the sensitivities-based method (delta / vega / curvature, bucketed and risk-weighted) and the ES replacement for VaR; the regulatory endpoint of this entire folder.
- **RiskMetrics / MSCI** and **Hull, *Risk Management and Financial Institutions*** — the standard limit-system structure (delta/gamma/vega/theta, VaR, stress) as implemented in bank practice.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · VaR Extensions (delta–gamma & backtesting)]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|Expected Shortfall (the coherent measure FRTB substitutes for VaR)]]
- Forward: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/basel-and-regulation|Basel & Regulation (FRTB SBM: delta, vega, curvature)]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · The Greeks]] · [[foundations/numerical-methods/index|Numerical Methods]]
