---
title: "Market Impact & Depth: Topic Hub & Formula Lookup"
tags:
  - pillar-market-making
  - market-impact
  - kyle-lambda
  - depth
  - square-root-law
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation, projection theorem) and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (OLS, autocovariance). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Trade, and the price moves against you. That single fact — **market impact** — is the price of immediacy and the central quantity of liquidity. It is why a $1bn order cannot be filled at the screen price, why execution desks exist, and why two markets with the same quoted spread can differ tenfold in the true cost of trading.

This folder is the **market-impact & depth** topic-folder for Pillar 6. It is a *hub*: it gives you (a) the **fast formula-and-model lookup** below, and (b) six sub-pages that walk from first-principles intuition through the Kyle (1985) equilibrium, the temporary/permanent decomposition, the empirical square-root law, the practice of measuring impact, and the advanced transient-impact models.

> **The one-sentence essence.** "Depth is the amount of order flow needed to move the price by one unit; **Kyle's $\lambda$** is that unit impact, so market depth is $1/\lambda$ — and every impact model is a statement about how $\lambda$ behaves as a function of size, time and liquidity."

**Scope note.** Pillar 2 covers *optimal execution* (how to schedule a trade given an impact model). This folder is the **microstructure/impact-model view**: what *causes* the price to move and how to *measure* it. The two meet at [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Almgren–Chriss]].

*Primary verified sources:* Hasbrouck, *Empirical Market Microstructure* (Ch 7, Kyle; Ch 8, generalized Roll; Ch 9, multivariate; §9.9, impact proxies) — the deep-read verification reports `hasbrouck_ch6-10.md` / `hasbrouck_ch1-5.md` in the corpus — cross-checked against the primary papers (Kyle 1985; Almgren & Chriss 2000; Almgren et al. 2005; Bouchaud, Farmer & Lillo 2009; Gatheral 2010, 2013; Cont, Kukanov & Stoikov 2014).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $v$ = asset value (normally distributed), $x$ = informed demand, $u$ = noise order flow, $y=x+u$ = total order flow, $\lambda$ = price-impact coefficient, $P$ = price, $\Sigma_0$ = prior value variance, $\sigma_u^2$ = noise-flow variance.

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from the verified corpus and re-executed numerically (§3).

#### A. The Kyle (1985) single-auction equilibrium
| Quantity | Formula | Note |
|---|---|---|
| Informed demand | $x=\beta\,(v-p_0)$, $\;\beta=\sqrt{\sigma_u^2/\Sigma_0}$ | insider "slices and dices" |
| Price rule | $P=p_0+\lambda\,y=p_0+\lambda\,(x+u)$ | linear, set by competitive MMs |
| **Price impact / Kyle's lambda** | $\boxed{\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}}$ | $(\$/share)$ per unit signed flow |
| **Market depth** | $\boxed{1/\lambda=2\sqrt{\sigma_u^2/\Sigma_0}}$ | flow needed for a \$1 move |
| Info incorporated | $\mathrm{Var}[v\mid P]=\Sigma_0/2$ | exactly half, independent of noise |
| Insider profit (cond. on $v$) | $\mathbb{E}[\pi\mid v]=\dfrac{(v-p_0)^2}{2}\sqrt{\dfrac{\sigma_u^2}{\Sigma_0}}$ | Hasbrouck eq. 7.5 (Ch 7) |
| Insider profit (unconditional) | $\tfrac12\sqrt{\sigma_u^2\,\Sigma_0}$ | average over $v$ |
| Continuous-time limit | $dP_t=\lambda\,dY_t$ | $\lambda$ constant; $P$ is a martingale |

#### B. Temporary vs permanent impact (Almgren–Chriss 2000)
- Permanent: $g(v)=\gamma v$ — price drift $\propto$ cumulative executed size, **schedule-independent**.
- Temporary: $h(v)=\epsilon\,\mathrm{sgn}(v)+\tilde\eta\,v$ — the concession to *attract liquidity now*, schedule-sensitive.
- Expected cost: $\mathbb{E}[x]=\tfrac12\gamma X^2+\epsilon\!\sum_k|n_k|+\tilde\eta\!\sum_k n_k^2$, with $\tilde\eta=\eta-\tfrac12\gamma$; risk $\mathrm{Var}[x]=\tfrac12\sigma^2\sum\tau_k x_k^2$.
- Optimal trajectory: $x_j=\dfrac{\sinh\!\big(\kappa(T-t_j)\big)}{\sinh(\kappa T)}X$, $\;\kappa\approx\sqrt{\tilde\lambda\sigma^2/\tilde\eta}$ (Gatheral's $\kappa$).

#### C. Empirical impact (Almgren et al. 2005)
- $I=\gamma\,\sigma\,\dfrac{X}{V}\Big(\dfrac{\Theta}{V}\Big)^{1/4}$ (permanent), $\;J=\dfrac{I}{2}+\mathrm{sgn}(X)\,\eta\,\sigma\Big(\dfrac{X}{VT}\Big)^{3/5}$ (realized).
- Fitted: $\gamma=0.314\pm0.041$, $\eta=0.142\pm0.0062$; permanent exponent fixed at $1$ (no-arbitrage); temporary exponent $\beta=3/5$ (square root $\beta=\tfrac12$ rejected at 95%).

#### D. The square-root law
$$I \;\propto\; \sigma\,\sqrt{\frac{Q}{V}},$$
impact grows as the **square root** of order size (or participation rate): dominating today's execution models. Discounted origin (Bouchaud et al. 2009): for power-law order-sign autocorrelation $C_\tau\sim\tau^{-\gamma}$, impact $\sim N^{1-\beta}$ with $\beta=(1-\gamma)/2$; empirical $\gamma\approx0.5\Rightarrow$ impact $\sim N^{3/4}$ and, in the latent-liquidity picture, $\sqrt{Q}$.

#### E. No-dynamic-arbitrage constraint (Gatheral 2010)
Transient model $S_t=S_0+\int_0^t h(\dot X_s)G(t-s)\,ds$ with $h(x)=c|x|^\delta\mathrm{sgn}\,x$, $G(\tau)=\tau^{-\gamma}$:
$$\text{price manipulation exists}\iff \gamma+\delta<1 .$$
Empirically $\delta\approx\tfrac12,\gamma\approx\tfrac12$ sit right on the boundary — impact is *just barely* consistent with no-arbitrage.

#### F. Impact as a microstructure measurement (Hasbrouck)
- Generalized Roll (Ch 8): $\Delta p_t=c(q_t-q_{t-1})+\lambda q_t+u_t$, spread $=2(c+\lambda)$ (transitory $c$, permanent $\lambda$); identified random-walk variance $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$.
- OFI (Cont et al. 2014): $\Delta P\approx\lambda_{\mathrm{OFI}}\cdot\mathrm{OFI}$, $\lambda_{\mathrm{OFI}}\propto 1/\text{depth}$.
- Amihud illiquidity: $I=\mathbb{E}\!\left[|r_t|/\text{\$Vol}_t\right]$; Amivest liquidity ratio $L=\text{Vol}/|r|$; Amihud is the better $\lambda$ proxy (Hasbrouck 2005).

---

### 3. Computational Implementation — the Kyle model engine (stdlib only)

Simulate the single-auction equilibrium, recover $\lambda$ from order flow by OLS, and check that exactly half the private information is impounded. **Ran and verified** (exact output below; full experiment in [[pillars/06-market-making/market-impact-and-depth/02-the-kyle-model|02 · The Kyle Model]]).

```python
import math, random

def kyle_sim(p0=100.0, Sigma0=4.0, sig_u2=1.0, n=300000, seed=11):
    """Single-auction Kyle equilibrium: v~N(p0,Sigma0); x=beta(v-p0); y=x+u;
       P=p0+lambda*y with lambda=0.5*sqrt(Sigma0/sig_u2)."""
    lam  = 0.5 * math.sqrt(Sigma0 / sig_u2)      # price impact
    beta = math.sqrt(sig_u2 / Sigma0)            # insider aggressiveness
    random.seed(seed); sv, su = math.sqrt(Sigma0), math.sqrt(sig_u2)
    syy = svy = prof = 0.0
    for _ in range(n):
        v = p0 + sv*random.gauss(0,1); u = su*random.gauss(0,1)
        x = beta*(v-p0); y = x+u; P = p0 + lam*y
        prof += (v-P)*x; svy += (v-p0)*y; syy += y*y
    slope = svy/syy                              # OLS of (v-p0) on order flow y
    resid = Sigma0 - slope*slope*(syy/n)         # Var[v|y] empirically
    return lam, beta, slope, resid, prof/n

lam, beta, slope, resid, prof = kyle_sim()
print(f"lambda theory    = {lam:.4f}   [0.5*sqrt(Sigma0/sigma_u^2)]")
print(f"beta   theory    = {beta:.4f}   [sqrt(sigma_u^2/Sigma0)]")
print(f"lambda from OLS  = {slope:.4f}   <- impact recovered from flow")
print(f"Var[v|y] resid   = {resid:.4f}   [theory Sigma0/2 = 2.0000]")
print(f"insider profit   = {prof:.4f}   [theory 0.5*sqrt(sigma_u^2*Sigma0) = 1.0000]")
print(f"market depth     = {1/lam:.4f}")
```
```
lambda theory    = 1.0000   [0.5*sqrt(Sigma0/sigma_u^2)]
beta   theory    = 0.5000   [sqrt(sigma_u^2/Sigma0)]
lambda from OLS  = 0.9998   <- impact recovered from flow
Var[v|y] resid   = 1.9982   [theory Sigma0/2 = 2.0000]
insider profit   = 0.9969   [theory 0.5*sqrt(sigma_u^2*Sigma0) = 1.0000]
market depth     = 1.0000
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/06-market-making/market-impact-and-depth/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Impact-model misspecification.** Fitting a *linear* model to square-root data gives systematically wrong cost forecasts at scale; the permanent exponent is pinned to $1$ by no-arbitrage, the temporary exponent is not.
2. **Temporary-vs-permanent confusion.** Counting temporary impact as permanent *double-charges* a strategy (and vice-versa); the realized VWAP sits between them and only the permanent part survives a round trip.
3. **Non-linearity & impact decay.** Concave (square-root) impact breaks the quadratic-optimisation machinery of linear Almgren–Chriss; exponential impact decay plus nonlinear impact *implies arbitrage* (Gatheral).
4. **Depth is dynamic.** The book refills ("resilience"); treating depth as static understates cost of repeated trading and is why OFI slope $\propto1/\text{depth}$ drifts intraday.

---

### 5. Canonical Literature & Study References

- **Kyle, A. S. (1985)**, *Continuous auctions and insider trading*, Econometrica 53(6), 1315–1335. *The anchor. Primary PDF in corpus (`40_Kyle_1985_...`); model verified via Hasbrouck Ch 7.*
- **Almgren, R. & Chriss, N. (2000)**, *Optimal execution of portfolio transactions*, Journal of Risk 3(2), 5–39. *The temporary/permanent split and the efficient frontier. Primary PDF in corpus.*
- **Almgren, R., Thum, C., Hauptmann, H. & Li, H. (2005)**, *Direct estimation of equity market impact*, Risk 18(7), 57–62. *Empirical $\gamma,\eta$ and the $3/5$ exponent. Primary PDF in corpus.*
- **Bouchaud, J.-P., Farmer, J. D. & Lillo, F. (2009)**, *How markets slowly digest changes in supply and demand*, in *Handbook of Financial Markets*. *The econophysics review: impact concavity, order-flow long memory, propagation. Primary PDF in corpus.*
- **Gatheral, J. (2010)**, *No-dynamic-arbitrage and market impact*, Quantitative Finance 10(7), 749–759. *The $\gamma+\delta\ge1$ constraint. Primary PDF in corpus.*
- **Gatheral, J. & Schied, A. (2013)**, *Dynamical models of market impact and algorithms for order execution*, in *Handbook on Systemic Risk*. *Rigorous transient-impact synthesis. Primary PDF in corpus.*
- **Cont, R., Kukanov, A. & Stoikov, S. (2014)**, *The price impact of order book events*, Journal of Financial Econometrics 12(1), 47–88. *OFI and impact $\propto1/$depth. Primary PDF in corpus.*
- **Hasbrouck, J. (2007)**, *Empirical Market Microstructure*, OUP. *Ch 7 (Kyle), Ch 8 (generalized Roll $\lambda$), Ch 9 (multivariate, §9.9 impact proxies). Deep-read verified in corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
- Sibling topics (in-pillar): [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (the sequential-trade counterpart to Kyle) · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov Optimal Quoting]]
- Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Almgren–Chriss Optimal Execution (Pillar 2)]] (the scheduling side of the same model) · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]] (Amihud is the impact proxy that gets priced)
- Sub-pages (in-folder): 01 From Zero · 02 The Kyle Model · 03 Temporary vs Permanent · 04 The Square-Root Law · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/market-impact-and-depth/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Model + code (undergrad/job-seeking):** [[pillars/06-market-making/market-impact-and-depth/02-the-kyle-model|02 · The Kyle Model]] → [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|03 · Temporary vs Permanent]] → [[pillars/06-market-making/market-impact-and-depth/04-the-square-root-law|04 · The Square-Root Law]].
- **Robustness (practitioner/graduate):** [[pillars/06-market-making/market-impact-and-depth/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/06-market-making/market-impact-and-depth/06-advanced-extensions|06 · Advanced Extensions]].
