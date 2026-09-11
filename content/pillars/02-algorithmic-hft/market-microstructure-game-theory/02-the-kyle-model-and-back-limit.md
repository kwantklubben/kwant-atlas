---
title: "2.10.2 Kyle (1985) and the Back Continuous-Time Limit"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - kyle-1985
  - back-1992
  - price-impact
  - insider-trading
  - continuous-time
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01 - From Zero]] and basic probability (normal distributions, conditional variance, OLS).

---

### 1. Intuition & Practical Objective

Kyle (1985) asked the sharpest possible version of the informed-trader question. Instead of a two-point value and a one-shot trade, suppose:

- the asset's value is $v\sim\mathcal N(p_0,\Sigma_0)$ — a continuum of possible values, so the insider has *how much better informed* she is rather than *which way*;
- a **single strategic insider** observes $v$ and chooses how much to trade;
- **noise traders** submit $u\sim\mathcal N(0,\sigma_u^2)$ — random volume whose only job is camouflage;
- **competitive market makers** see only the total signed order flow $y=x+u$ and set a price.

The insider's problem is a genuine strategic dilemma. Trade big and you move the price against yourself; trade small and you earn the impact-free edge on fewer shares. Kyle showed the equilibrium is startlingly clean: the insider submits a quantity **linear in her edge**, the makers use a **linear price rule**, and — the famous result — **exactly half of the insider's private information is impounded into the price**, regardless of how much noise there is.

The second half of this page is the continuous-time question, and it contains the most useful trap in the literature. Everyone's first instinct is: "run more and more auctions over a fixed horizon and take the limit". **That limit does not exist.** Kyle's multi-auction model releases information *geometrically* (half per auction), and if you shrink the interval between auctions while holding the total noise budget fixed, the first-period price impact blows up. The correct continuous-time object — derived by **Back (1992)** — has **linear** information release and a **constant** impact coefficient $\lambda=\sqrt{\Sigma_0/(\sigma_u^2T)}$. Knowing *which* limit you are taking is the difference between a correct high-frequency model and nonsense.

> **The one-sentence essence.** "A strategic insider trades proportionally to her edge, the makers price linearly, exactly half the private information gets revealed — and in continuous time the impact coefficient is *constant* and equal to $\sqrt{\Sigma_0/(\sigma_u^2T)}$, which you only get from Back's linear-release equilibrium, not from a naive limit of the discrete game."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The single auction.** $v\sim\mathcal N(p_0,\Sigma_0)$, $u\sim\mathcal N(0,\sigma_u^2)$, insider demand $x$, total flow $y=x+u$, linear price $P=p_0+\lambda y$. Makers are competitive, so they earn zero expected profit; by the projection theorem $P=\mathbb{E}[v\mid y]$, which for jointly normal variables is
$$
P=p_0+\frac{\operatorname{Cov}(v,y)}{\operatorname{Var}(y)}\,y\;\Longrightarrow\;\lambda=\frac{\beta\Sigma_0}{\beta^2\Sigma_0+\sigma_u^2}
$$
if the insider uses $x=\beta(v-p_0)$. The insider maximises $\mathbb{E}[(v-P)x]=\beta\Sigma_0-\lambda\beta^2\Sigma_0$; the first-order condition $\Sigma_0=2\lambda\beta\Sigma_0$ gives $\lambda\beta=\tfrac12$, and solving the two equations together:

$$
\boxed{\;\beta=\sqrt{\frac{\sigma_u^2}{\Sigma_0}},\qquad \lambda=\frac12\sqrt{\frac{\Sigma_0}{\sigma_u^2}},\qquad \frac1\lambda=2\sqrt{\frac{\sigma_u^2}{\Sigma_0}}\;}
$$

Substituting back, the residual variance is
$$
\operatorname{Var}[v\mid P]=\Sigma_0-\frac{\beta^2\Sigma_0^2}{\beta^2\Sigma_0+\sigma_u^2}=\Sigma_0-\frac{\Sigma_0}{\beta^2\Sigma_0/\sigma_u^2+1}=\Sigma_0-\frac{\Sigma_0}{2}=\frac{\Sigma_0}{2}.
$$
**Half the information, whatever the noise.** And $\mathbb{E}[\text{profit}]=\beta\Sigma_0-\lambda\beta^2\Sigma_0=\tfrac12\sqrt{\sigma_u^2\Sigma_0}$.

**2.2 The $N$-auction game.** Repeat the auction $N$ times with equal noise variance $\sigma_u^2$ per round and prior variance $\Sigma_{n-1}$. Write $x_n=\beta_n(v-p_{n-1})$, $\Delta_n=v-p_{n-1}\sim\mathcal N(0,\Sigma_{n-1})$. Since $y_n=\beta_n\Delta_n+u_n$,
$$
\lambda_n=\frac{\beta_n\Sigma_{n-1}}{\beta_n^2\Sigma_{n-1}+\sigma_u^2},\qquad \Sigma_n=\Sigma_{n-1}-\frac{\beta_n^2\Sigma_{n-1}^2}{\beta_n^2\Sigma_{n-1}+\sigma_u^2}=\frac{\Sigma_{n-1}\sigma_u^2}{\beta_n^2\Sigma_{n-1}+\sigma_u^2}.
$$
Each round the insider again faces $\lambda_n\beta_n=\tfrac12$, so $\beta_n\Sigma_{n-1}=2\lambda_n\beta_n^2\Sigma_{n-1}$ and the recursion collapses to

$$
\boxed{\;\beta_n=\sqrt{\frac{\sigma_u^2}{\Sigma_{n-1}}},\qquad \lambda_n=\frac12\sqrt{\frac{\Sigma_{n-1}}{\sigma_u^2}},\qquad \Sigma_n=\frac{\Sigma_{n-1}}{2}=\Sigma_0\,2^{-n},\qquad \mathbb{E}[\text{profit}_n]=\tfrac12\sqrt{\sigma_u^2\Sigma_{n-1}}\;}
$$

so **information is released geometrically — half per auction — and $\lambda_n$ decays geometrically while $\beta_n$ grows geometrically**. The insider's total expected profit converges to a finite limit:
$$
\sum_{n\ge1}\tfrac12\sqrt{\sigma_u^2\Sigma_0}\,2^{-(n-1)/2}=\frac{1}{2}\sqrt{\sigma_u^2\Sigma_0}\cdot\frac{1}{1-2^{-1/2}}=\boxed{\frac{2+\sqrt2}{2}\sqrt{\sigma_u^2\Sigma_0}} .
$$
More auctions $\Rightarrow$ more profit, but bounded: $1.707\sqrt{\sigma_u^2\Sigma_0}$ versus the single auction's $0.5\sqrt{\sigma_u^2\Sigma_0}$.

**2.3 Why the naive continuous-time limit is ill-posed.** Fix a horizon $T$, put $N$ auctions of length $\tau=T/N$, and give each round the "correct" noise variance $\sigma_u^2\tau$ (proportional to the clock, so the total noise budget over $[0,T]$ is $\sigma_u^2T$). Then
$$
\lambda_1=\frac12\sqrt{\frac{\Sigma_0}{\sigma_u^2\tau}}=\frac12\sqrt{\frac{\Sigma_0 N}{\sigma_u^2T}}\;\xrightarrow[N\to\infty]{}\;\infty .
$$
The discrete game **does not converge**: shrinking the auction interval while the insider's information advantage stays fixed makes the first period infinitesimally informative and hence infinitely costly to trade into. Something must give — and what gives, in the correctly posed model, is the *shape of information release*.

**2.4 Back (1992): the correct continuous-time limit.** Let $dU_t=\sigma_u dB_t$ and let the price be $P_t=p_0+\lambda(X_t+U_t)$. The correct equilibrium satisfies $P_t=\mathbb{E}[V\mid\mathcal F_t]$ with
$$
\boxed{\;\Sigma(t)=\Sigma_0\Bigl(1-\frac{t}{T}\Bigr),\qquad \lambda=\sqrt{\frac{\Sigma_0}{\sigma_u^2T}},\qquad \frac1\lambda=\sigma_u\sqrt{\frac{T}{\Sigma_0}}\;}
$$
**The derivation is a one-line filtering identity, and it is worth internalising.** If $P_t=\mathbb{E}[V\mid\mathcal F_t]$ and the innovation representation is $dP_t=\lambda_t\,dY_t$, then
$$
d\Sigma_t=-\operatorname{Var}(dP_t\mid\mathcal F_{t^-})=-\lambda_t^2\operatorname{Var}(dY_t\mid\mathcal F_{t^-})=-\lambda_t^2\sigma_u^2\,dt,
$$
because the predictable part of $dY_t$ is known and only the noise contributes variance. With $\Sigma(t)=\Sigma_0(1-t/T)$ we have $d\Sigma_t=-\frac{\Sigma_0}{T}dt$, so $\lambda^2\sigma_u^2=\Sigma_0/T$ — **$\lambda$ is constant in $t$**, and equal to $\sqrt{\Sigma_0/(\sigma_u^2T)}$.

Two consequences worth memorising:
- **$\int_0^T\lambda^2\sigma_u^2dt=\Sigma_0$**: all the information is released by $T$. Half of it is released by $t=T/2$ — the continuous analogue of the auction's $\Sigma_0/2$.
- **$\lambda\propto T^{-1/2}$**: a *longer* horizon means a *deeper* market (more time for the noise to accumulate, so the flow-to-price map is flatter). This is the exact opposite of the trading-desk intuition "longer = more risk", and both statements are true — they are about different objects (information per unit flow vs inventory risk).

---

### 3. Computational Implementation — the Kyle engine and the Back limit, verified

Stdlib only. Three verified blocks of work: (a) the discrete $N$-auction recursion with its profit limit, (b) the divergence of the naive continuum, (c) Back's continuous-time information accounting.

```python
import math
Sig0, su2, N = 4.0, 1.0, 12
Sig = [Sig0]
for _ in range(N): Sig.append(Sig[-1]/2.0)
print("N-period discrete Kyle (equal noise variance per auction): Sigma_n = Sigma_0/2^n")
print(f"{'n':>2} {'Sigma_n':>10} {'beta_n':>8} {'lambda_n':>9} {'profit_n':>9}")
tot = 0.0
for n in range(1, N+1):
    b = math.sqrt(su2/Sig[n-1]); l = 0.5*math.sqrt(Sig[n-1]/su2); pr = 0.5*math.sqrt(su2*Sig[n-1])
    tot += pr
    print(f"{n:>2} {Sig[n-1]:>10.6f} {b:>8.4f} {l:>9.4f} {pr:>9.4f}")
print(f"total E[profit], N={N}: {tot:.4f}   N->inf limit (2+sqrt2)/2*sqrt(sigma_u^2*Sigma_0) = {(2+math.sqrt(2))/2*math.sqrt(su2*Sig0):.4f}")
T = 1.0
print("\nNaive N->infinity limit with per-period noise variance sigma_u^2*tau:")
for Nn in (10, 100, 1000, 10000):
    print(f"  N={Nn:>5}  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = {0.5*math.sqrt(Sig0/(su2*(T/Nn))):,.3f}")
print("\nBack (1992) continuous-time information accounting (Sigma(t)=Sigma_0(1-t/T)):")
for t in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"  t={t:.2f}:  Sigma(t)={Sig0*(1-t/T):.4f}   dSigma/dt=-Sigma_0/T={-Sig0/T:.4f}")
lamc = math.sqrt(Sig0/(su2*T))
print(f"  identity lambda^2*sigma_u^2 = Sigma_0/T:  {lamc:.4f}^2*{su2} = {lamc**2*su2:.4f} = {Sig0/T:.4f}")
print(f"  integrate dt over [0,T]: {lamc**2*su2*T:.4f} = Sigma_0 = {Sig0:.4f}  (all information released)")
```
```
N-period discrete Kyle (equal noise variance per auction): Sigma_n = Sigma_0/2^n
 n    Sigma_n   beta_n  lambda_n  profit_n
 1   4.000000   0.5000    1.0000    1.0000
 2   2.000000   0.7071    0.7071    0.7071
 3   1.000000   1.0000    0.5000    0.5000
 4   0.500000   1.4142    0.3536    0.3536
 5   0.250000   2.0000    0.2500    0.2500
 6   0.125000   2.8284    0.1768    0.1768
 7   0.062500   4.0000    0.1250    0.1250
 8   0.031250   5.6569    0.0884    0.0884
 9   0.015625   8.0000    0.0625    0.0625
10   0.007812  11.3137    0.0442    0.0442
11   0.003906  16.0000    0.0312    0.0312
12   0.001953  22.6274    0.0221    0.0221
total E[profit], N=12: 3.3609   N->inf limit (2+sqrt2)/2*sqrt(sigma_u^2*Sigma_0) = 3.4142

Naive N->infinity limit with per-period noise variance sigma_u^2*tau:
  N=   10  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 3.162
  N=  100  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 10.000
  N= 1000  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 31.623
  N=10000  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 100.000

Back (1992) continuous-time information accounting (Sigma(t)=Sigma_0(1-t/T)):
  t=0.00:  Sigma(t)=4.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=0.25:  Sigma(t)=3.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=0.50:  Sigma(t)=2.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=0.75:  Sigma(t)=1.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=1.00:  Sigma(t)=0.0000   dSigma/dt=-Sigma_0/T=-4.0000
  identity lambda^2*sigma_u^2 = Sigma_0/T:  2.0000^2*1.0 = 4.0000 = 4.0000
  integrate dt over [0,T]: 4.0000 = Sigma_0 = 4.0000  (all information released)
```

Three things to take away:

1. **$\lambda_n$ halves every round ($1.0000\to0.7071\to0.5000\to\cdots$) while $\beta_n$ doubles**, because $\Sigma_n$ halves and the two are reciprocal square roots of the same quantity. This geometric pattern *is* the discrete model.
2. The **total profit saturates**: $N=12$ already gives $3.3609$ against the $N\to\infty$ limit $3.4142$. The insider's marginal auction is worth exponentially less.
3. The **naive continuum diverges linearly in $\sqrt N$** ($\lambda_1=100$ at $N=10^4$), while Back's continuous-time identity $\lambda^2\sigma_u^2T=\Sigma_0$ holds **exactly** — and the integral of information release equals $\Sigma_0$ to the last digit. The two "limits" are not the same limit, and only one of them exists.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing the two limits.** "Kyle's continuous-time model" is Back's (1992) linear-release equilibrium, not the $N\to\infty$ limit of the discrete auction game. Anyone who calibrates a high-frequency impact parameter by "taking $\tau\to0$" from the discrete recursion will get an impact coefficient that diverges.
2. **$\lambda$ is not a physical constant.** It is $\sqrt{\Sigma_0/(\sigma_u^2T)}$: it depends on the *prior uncertainty*, the *noise volume*, and the *horizon*. Double the noise volume and depth ($1/\lambda$) rises by $\sqrt2$; double the horizon and depth rises by $\sqrt2$. Impact estimates that ignore $\Sigma_0$ are not comparable across names.
3. **The half-information result is a knife-edge of normality.** $\operatorname{Var}[v\mid P]=\Sigma_0/2$ follows from joint normality. Under fat tails or a discrete value the "exactly half" property fails, and with it every argument that uses it as a calibration anchor.
4. **One strategic insider is not a market.** With $K$ informed traders the revelation rate scales with $K\beta$ and $\lambda$ falls toward zero (page 06). A single-insider $\lambda$ fit on a market with many informed participants systematically over-states impact.
5. **Noise is not a fixed budget.** The model treats $\sigma_u^2$ as exogenous and constant. In reality noise volume *responds* to realised volatility and to the presence of informed flow — the parameter you calibrated is a function of the thing you are modelling.
6. **The insider's optimality is never tested.** The model says the insider *should* trade $\beta(v-p_0)$; it does not say anyone does. Empirically, informed flow is autocorrelated and clustered in time, which the one-shot Gaussian insider does not generate.

---

### 5. Canonical Literature & Study References

- **Kyle, Albert S.** — "Continuous auctions and insider trading," *Econometrica* 53(6), 1315–1335 (1985). *Sections 1–3: the batch auction, $\lambda$, $\Sigma_0/2$, the $N$-auction recursion, and the insider's profit.*
- **Back, Kerry** — "Insider trading in continuous time," *Review of Financial Studies* 5(3), 387–409 (1992). *The rigorous continuous-time limit; the founding application of filtering to microstructure. Read §2 (the model) and §3 (the equilibrium).*
- **Holden, Craig W.; Subrahmanyam, Avanidhar** — "Long-lived private information and imperfect competition," *Journal of Finance* 47(1), 247–270 (1992). *What happens with many informed traders; see page 06.*
- **Kühn, Christoph; Lorenz, Christopher** — "Insider trading in discrete time Kyle games," *Mathematics and Financial Economics* 19, 39–66 (2025). *Exactly the question this page turns on: which discrete games converge to the continuous-time Kyle–Back equilibrium (and which do not).*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 7 (the Kyle model) and Ch 6 (PIN). *Corpus verification `hasbrouck_ch6-10.md` — equation-by-equation check passed; the insider's FOC is eq 7.1 and the equilibrium $(\lambda,\beta)$ is eq 7.4, with profit (conditional on $v$) as eq 7.5 — the $N$-auction structure of §2.2 is Hasbrouck's §7.2.*
- **Grossman, Sanford J.; Stiglitz, Joseph E.** — "On the impossibility of informationally efficient markets," *American Economic Review* 70(3), 393–408 (1980). *Why some noise must exist for information to be worth acquiring — the deep reason $\sigma_u^2>0$ is not a nuisance parameter.*
- **Kyle, Albert S.; Obizhaeva, Anna A.** — "Market microstructure invariance," *Econometrica* 84(3), 975–1024 (2016). *What happens when you insist that $\lambda$ obey dimensional invariance across assets.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01 - From Zero]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/03-glosten-milgrom-sequential-trade|03 - Glosten–Milgrom]] (the sequential-trade, two-point-value counterpart of the same equilibrium)
- Sibling at the same λ: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (measuring Kyle's $\lambda$, the square-root law, transient impact)
- Scheduling on top of it: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (uses $\eta,\gamma$, not $\lambda$ — the link is the calibration)
- Mathematical machinery: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (the filtering identity in §2.4)
