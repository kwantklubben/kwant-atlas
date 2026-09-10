---
title: "04 — Monte Carlo VaR (Simulate the Factors, Full Revaluation)"
tags:
  - pillar-quantitative-risk
  - parametric-historical-and-monte-carlo-var
  - monte-carlo-var
  - full-revaluation
  - variance-reduction
---

**Basic Prerequisites:** [[foundations/numerical-methods/index|Numerical Methods]] and [[foundations/statistics-and-inference/index|Statistics & Inference]] (Monte Carlo, CLT).

---

### 1. Intuition & Practical Objective

Monte Carlo VaR is the most powerful and most expensive of the three methods. The practical objective in one line: **simulate thousands (or hundreds of thousands) of plausible future moves of the risk factors, revalue the portfolio under each — or under an approximation — and read the quantile of the simulated losses.**

Why bother when parametric is fast and historical is simple? Because MC **controls the distribution you simulate from** and **handles arbitrary nonlinearity** by full revaluation. Two things neither of the other two can do:

- *Parametric* forces normality and linearity; *MC* can simulate fat-tailed, skewed, or regime-switching factor processes (Student-$t$, jumps, GARCH) — you choose the model.
- *Historical* replays the past verbatim; *MC* can stress the current portfolio under what *could* happen (the factor model's distribution), including scenarios no window has seen.

Glasserman Ch 9 frames it sharply (and the flat file gets it right): use the **real-world distribution of $\Delta S$ for the loss probability** (you want actual-risk probabilities), but the **risk-neutral distribution to revalue** an option (its price is a risk-neutral expectation — the RN measure is where the price lives). Mixing these two measures is the classic error.

The cost is raw compute: $m$ scenarios × (revaluation cost per portfolio), so a 100,000-option portfolio under 1M scenarios is heavy. That is exactly why the **delta–gamma approximation** exists ([[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06]]) and why variance reduction (antithetic, importance sampling) is a core MC tool.

---

### 2. Mathematical Ground Truth & Derivations

**The MC VaR estimator.** Let $L_i=-\Delta V_i$ be the portfolio loss under scenario $i$, where scenario $i$ draws a factor move $\Delta S_i$ from the chosen model and revalues the portfolio. Sort the losses and take the $\alpha$-quantile of the *empirical* distribution:

$$\widehat{\text{VaR}}_\alpha^{(MC)}=L_{(\lceil m(1-\alpha)\rceil)},$$

exactly the HS quantile formula of [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation|03]] — the difference is *where the scenarios come from* (simulated vs replayed-from-the-past).

**The factor model.** For $d$ Gaussian factors, $\Delta S\sim N(\mathbf{0},\Sigma)$, sample via Cholesky: $\Delta S=A Z$, $AA^T=\Sigma$, $Z\sim N(\mathbf{0},I)$ (Glasserman Ch 2; Hull Ch 21 §21.6). For non-normal factors, replace the normal with a fat-tailed model (Glasserman Ch 9 §9.3: Student-$t$, jumps) — this is MC's superpower over parametric.

**Revaluation: full vs partial — the variance/error tradeoff.**
- **Full revaluation:** value $V(S+\Delta S)$ under each scenario, $\Delta V=\Sigma_{\text{pos}}[V_{k}(S+\Delta S)-V_k(S)]$. Unbiased for the model, but slow.
- **Partial (delta/delta–gamma):** approximate $\Delta V\approx\delta^T\Delta S+\tfrac12\Delta S^T\Gamma\Delta S$, faster but biased for options. Glasserman Ch 9 uses the delta–gamma *both* as a control variate and as the sampling engine for importance sampling (twist the quadratic, revalue the true portfolio).

**The quantile's sampling error (Glasserman Ch 9 §9.1).** Same honest formula as HS:
$$\sqrt m\,(\widehat x_p-x_p)\Rightarrow N\!\Big(0,\tfrac{p(1-p)}{f(x_p)^2}\Big),\quad p=1-\alpha.$$
To halve the *absolute* uncertainty in the VaR you need $4\times$ the scenarios — the $\sigma/\sqrt m$ law. And since $f(x_p)$ is small in the tail, $f(x_p)^2$ in the denominator makes **tail quantiles diverge slowly** — exactly where variance reduction pays. Antithetic variates (the Glasserman Ch 4 Ch 4 §4.2) and importance sampling for rare tails (Ch 9 §9.2) attack exactly this.

---

### 3. Computational Implementation — MC VaR with honest error bars, stdlib only

We simulate the shared 2-asset portfolio under 200k scenarios and report both the VaR **and its standard error** (so no one mistakes MC for a precision instrument). The `3,405.97` reproduces the hub MC column; the `se` is the honest $\sqrt{p(1-p)}/(\sqrt m f(x_p))$ quantile error from §2.

```python
import math, random
def N(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
z99 = 2.3263478740408408
pos=[40000.0,60000.0]; sd=[0.012,0.020]; rho=0.40; m=200_000

# Cholesky factor A of the 2x2 covariance [[s1^2, rho s1 s2],[rho s1 s2, s2^2]] : AA'=cov
A = [[sd[0], 0.0],
     [sd[1]*rho, sd[1]*math.sqrt(1-rho*rho)]]

random.seed(7)
losses=[]
for _ in range(m):
    Z=[random.gauss(0,1) for _ in range(2)]
    dS=[A[i][0]*Z[0]+A[i][1]*Z[1] for i in range(2)]   # correlated factor move
    losses.append(-(dS[0]*pos[0]+dS[1]*pos[1]))        # -P&L = loss (linear portfolio)
losses.sort()
VaR = losses[int(0.99*m)-1]

# standard error of the empirical quantile: se = sqrt(p(1-p)) / (sqrt(m) f_hat(x_p))
p=0.01; w=100.0
lo,hi=VaR-w,VaR+w
f_hat=sum(1 for l in losses if lo<=l<hi)/(m*(hi-lo))   # histogram density at VaR
se=math.sqrt(p*(1-p))/(math.sqrt(m)*f_hat)
print(f"MC VaR_99 (m={m}) = {VaR:,.2f}   se = +-{se:,.0f}")
print(f"  -> the tail number is a point estimate with a ~+/-{se:,.0f} 1-sigma band")
```
```
MC VaR_99 (m=200000) = 3,405.97   se = +-13
  -> the tail number is a point estimate with a ~+/-13 1-sigma band
```
*(The `±13` is honest: even 200k scenarios only pin the 99% VaR to ~±$13 — the same raw quantile noise HS carries in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation|03]]. Halving that band costs 4× the scenarios; importance sampling for the far tail is the lever (Glasserman Ch 9 §9.2).)*

**Where MC earns its keep — full revaluation beats delta-normal on an option.** Same idea, one FX put. Because the put is only mildly convex over one day, delta-normal is *close but not exact*; full revaluation is the benchmark and delta-gamma is the cheap fix (both taken to page 06):

```python
import math, random
def N(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2*math.pi)
def put(S,K,T,r,sig):
    d1=(math.log(S/K)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return K*math.exp(-r*T)*N(-d2)-S*N(-d1)
S,K,T,r,ann=1.55,1.60,0.5,0.03,0.12
dv=ann/math.sqrt(252); V0=put(S,K,T,r,ann)
d1=(math.log(S/K)+(r+0.5*ann**2)*T)/(ann*math.sqrt(T))
delta=-N(-d1); gamma=phi(d1)/(S*ann*math.sqrt(T))

m=400000; random.seed(9)
Lf=[]                      # full-revaluation losses
for _ in range(m):
    dS=S*dv*random.gauss(0,1)
    Lf.append(- (put(S+dS,K,T-1/252,r,ann)-V0))
Lf.sort()
print(f"put V0={V0:.4f} delta={delta:.4f} gamma={gamma:.3f}")
print(f"full-revaluation MC VaR_99 = {Lf[int(0.99*m)-1]:.4f}")
print(f"delta-only VaR_99          = {2.3263478740408408*abs(delta*S*dv):.4f} (the delta-normal shortcut)")
```
```
put V0=0.0670 delta=-0.5616 gamma=2.997
full-revaluation MC VaR_99 = 0.0143
delta-only VaR_99          = 0.0153 (the delta-normal shortcut)
```
The delta-normal shortcut and full revaluation differ by only ~7% here — *because this put's gamma is modest*. The whole point of delta–gamma and full revaluation is the *straddle-style* case (delta≈0, big gamma) where delta-normal is catastrophically wrong; that lives in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Delta–Gamma & Backtesting]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Garbage-in, garbage-out on the factor model.** MC with normal factors and the wrong correlation is just an expensive confirmation of a bad assumption. The distribution you *simulate from* is the model — choose it consciously (normality here is a hypothesis, not a law; see [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|EVT]]).
2. **Real-world vs risk-neutral confusion.** For *loss probability* use the **real-world** measure; for *revaluing an option* use the **risk-neutral** price. Using RN revalue prices for loss probs (or vice versa) misstates both (Glasserman Ch 9; the flat file's warning).
3. **The $\sigma/\sqrt m$ tail is cruel.** Halving VaR error = $4\times$ scenarios; tail quantiles need the most and converge slowest. Without variance reduction, "just raise $m$" is the classic brute-force error.
4. **Numerical error in revaluation.** Full revaluation of a path-dependent or American option needs an accurate pricer; a crude/dirty pricer injects its own bias bigger than the MC error (numerical methods: [[foundations/numerical-methods/index|Numerical Methods]]).
5. **MC ≠ historical ≠ parametric — they answer the same question with different models.** Running only MC and assuming it's "the truth" repeats the window/model mistake in a heavier coat. All three are biased estimates of the same quantile; only backtesting tells you which model fits the *realized* data ([[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Backtesting]]).

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering* — Ch 9 (applications in risk management: delta (9.1), delta–gamma (9.2), heavy-tail MC, importance sampling for the tail, quantile-estimation variance); Ch 2 (Cholesky/PC normal sampling); Ch 4 (variance reduction); Ch 1 (the $\sigma/\sqrt m$ foundation). *Math-verified in corpus.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.6 (MC in options/delta-gamma context) and Ch 22 §22.6 (MC for VaR, full vs partial simulation). *Verified in corpus.*
- **RiskMetrics / J.P. Morgan**, *RiskMetrics Technical Document* (1996) — the hybrid and full-revaluation MC traditions.

---

### 6. Connected Graph Bridges

- Base: [[foundations/numerical-methods/index|Numerical Methods]] (MC, variance reduction, quasi-MC) · [[foundations/probability-and-measure-theory/index|Probability & Measure]] (CLT, martingales, risk-neutral measure).
- Back: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation|03 · Historical Simulation]].
- Forward: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Delta–Gamma & Backtesting]].
- Measure: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (risk-neutral revaluation).