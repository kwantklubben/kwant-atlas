---
title: "Execution Backtesting & Simulation: Topic Hub & Formula Lookup"
tags:
  - pillar-algorithmic-hft
  - execution-backtesting
  - simulation
  - fill-model
  - index-hub
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] and [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A **signal backtest** asks "if I could trade at the price series, would this rule have made money?" An **execution backtest** asks the harder question: "given the order I *actually sent*, into the book that *actually existed*, with the latency I *actually have* — did it fill, at what price, and what did that cost?" The two are different sciences. The first needs a price series; the second needs a **model of the matching process**, because a *fill is not a price observation* — it is the outcome of a queue, a priority rule, and market impact.

This folder is the **execution-backtesting-and-simulation topic-folder** for Pillar 2. It is a *hub*: it gives you **(a) the fast formula/decision lookup** below (job #1) and **(b) routes you to six sub-pages** that go from zero-knowledge intuition, through *why execution backtests lie*, the fill model, market replay vs Monte Carlo, the failure modes that make a simulated edge evaporate in production, and the modern extensions (agent-based LOB simulators, simulator validation).

> **The one-sentence essence.** "An execution backtest is only as honest as its **fill model**: you must simulate whether an order fills from the *outflow ahead of it in the queue* — $\text{filled}=(\xi-x)^+-(\xi-x-L)^+$ — and you must price the post-fill adverse drift; a backtest that equates a printed trade with your fill, looks past the decision time, or assumes trading at the mid will report an edge that does not exist."

**Scope note (vs the siblings).** This folder is the *meta* view: how to simulate and validate *any* execution logic. The *micro-event* mechanics (queue position, fill probability) live in [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]; the *scheduling* of a block lives in [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]; the *statistical* honesty of a signal backtest lives in [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (multiple testing, deflated Sharpe). This folder is where those three meet at the **fill assumption**.

*Primary verified sources:* Hasbrouck, *Empirical Market Microstructure* (2007) Ch 14–15 (implementation shortfall, effective/realized cost, order placement) and Ch 3 (Roll bounce); Almgren & Chriss (2000); Almgren, Thum, Hauptmann & Li (2005); Cont & Kukanov (2017); Cont, Stoikov & Talreja (2010); Gould et al. (2013); Abergel et al., *Limit Order Books* (2016); López de Prado, *Advances in Financial Machine Learning* (2018) Ch 11–13. All numbers below were **re-executed and reproduced** (see §3).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $x$ = shares **ahead** of your order in the FIFO queue; $Q$ = level depth; $L$ = your size; $\xi$ = cumulative **outflow from the front** (trades + cancels ahead) over the quote's life; $\mu$ = trade-arrival rate; $s$ = quoted spread; $\ell$ = round-trip latency; $v$ = participation rate; $m_t$ = efficient (mid) price, $p_t$ = trade price.

**Quick-Reference Lookup (job #1).** All formulas below were re-executed and reproduced numerically (§3); the "Verified check" column carries the exact run output.

| Quantity | Formula | Verified check |
|---|---|---|
| FIFO fill condition | $\text{Filled}(x,L,\xi)=(\xi-x)^+-(\xi-x-L)^+$ | replay: optimistic $1.0000$ vs FIFO $0.3686$ |
| Fill probability by $T$ (Poisson trades) | $\mathbb{P}(\xi(T)\ge x)=1-\sum_{k<x}\dfrac{(\mu T)^k e^{-\mu T}}{k!}$, $\xi(T)\sim\text{Poisson}(\mu T)$ | $\mu T{=}1200,\ x{=}1200$: closed $0.5038$ |
| Expected fill (exponential outflow) | $\mathbb{E}[\text{filled}]=m\!\left(e^{-Q/m}-e^{-(Q+L)/m}\right)$ | $Q{=}1000,L{=}1000,m{=}3000\Rightarrow609.34$ (MC $609.51$) |
| Fill fraction vs queue position | $\mathbb{E}\!\left[\min\big((\xi-x)^+,L\big)\right]/L$ | $x{=}0\Rightarrow0.9762$, $x{=}1000\Rightarrow0.2238$ |
| Fill time (pure trades) | $\sim\text{NegBin}(x,p)$, mean $x/\mu$ | mean $100$ ticks at $x{=}5,p{=}0.05$ |
| Latency pick-off | $\mathbb{P}\approx 1-e^{-\rho\ell}$ | $0.05$ ms $\to0.0488$; $10$ ms $\to1.0000$ |
| Implementation shortfall (Perold) | $\text{IS}=\underbrace{(n_1-n_0)'(p-\pi_0)}_{\text{execution}}+\underbrace{(v-n_1)'(\pi_1-\pi_0)}_{\text{opportunity}}$ | Hasbrouck Ch 14, eq 14.1 |
| Effective vs realized cost | $p_t-m_t=(p_t-m_{t+5})+(m_{t+5}-m_t)$ | impact $=m_{t+5}-m_t$ |
| AC expected cost / impact | $E[x]=\tfrac12\gamma X^2+\varepsilon\textstyle\sum|n_k|+\tfrac{\tilde\eta}{\tau}\sum n_k^2$ | temp. impact $\eta X^2/T$: $ $\$25{,}000\!\to\!\1{,}250 |
| Square-root impact law (idealized) | $\Delta P\approx Y\,\sigma\,(Q/V)^{\alpha}$ with $\alpha=\tfrac12$ | toy ln-ln fit exponent $0.4922$, $R^2{=}0.9401$ |
| Realized-impact exponent (empirical, Almgren et al. 2005) | $\Delta P\approx Y\,\sigma\,(Q/V)^{\alpha}$ with $\alpha\approx0.6$ | the *empirical* exponent is steeper than the idealized $\tfrac12$ — see [[pillars/06-market-making/market-impact-and-depth/index\|Market Impact & Depth]] |
| Market replay estimate | one path $f(\omega_{\text{recorded}})$ | replay $1.0000$ vs MC mean $0.6384$ CI $[0.6259,0.6509]$ |
| Monte Carlo standard error | $\text{SE}=\sigma/\sqrt N$ | $N{=}100\Rightarrow0.0451$; $N{=}10^5\Rightarrow0.001426$ |

> **Critical caveat.** $\xi$ (outflow) and $Q$ (depth) enter differently. A backtest that fills on "$Q$ traded" **ignores the queue ahead** and is the single most common lie; a backtest that fills on "any print at my price" ignores both queue *and* size. And **cancels ahead are not trades** — they are a large, correlated part of $\xi$ (Gould et al. 2013), so ignoring them is the bias in the *opposite* direction (under-filling a real quote, over-filling a backtest that only counts trades).

---

### 3. Computational Implementation — the fill-model engine

Runs on the standard library (plus `numpy` for one regression). It reproduces every verified number above: the Cont–Kukanov expected-fill closed form matches Monte Carlo, the FIFO binomial fill fraction falls with queue position, and the naive "any print" rule saturates at $1.0000$.

```python
import random, math
from math import comb
random.seed(11)

# --- (A) Cont-Kukanov expected fill, xi ~ Exp(mean m), vs Monte Carlo ---
def E_fill(Q, L, m):
    return m * (math.exp(-Q / m) - math.exp(-(Q + L) / m))          # closed form
def E_fill_mc(Q, L, m, n=60000):
    return sum(min(max(random.expovariate(1.0/m) - Q, 0.0), L) for _ in range(n)) / n

for Q in (0, 1000, 3000):
    cl = E_fill(Q, 1000, 3000)
    print(f"Q={Q:>4}: closed={cl:7.2f}  MC={E_fill_mc(Q,1000,3000):7.2f}")

# --- (B) FIFO fill fraction vs queue position: Binomial(T=300, p=0.08), 50 sh/trade ---
S, P, T, L = 50.0, 0.08, 300, 1000.0
def E_fraction(x):
    return sum(comb(T,k)*P**k*(1-P)**(T-k)*min(max(k*S - x, 0.0), L) for k in range(T+1)) / L
print("(B) FIFO fill fraction vs queue ahead x:")
for x in (0, 400, 800, 1000):
    print(f"   x={x:>4}: {E_fraction(x):.4f}")
print("(C) optimistic model (any print fills 100%) vs conservative:")
for x in (0, 400, 800, 1000):
    print(f"   x={x:>4}: optimistic=1.0000  conservative={E_fraction(x):.4f}"
          f"  overstatement={1/E_fraction(x):.2f}x")

# --- (D) Poisson trade-arrival upper tail: xi(T) ~ Poisson(mu T) share outflow ---
def poisson_tail(x, lam):                        # P(X >= x), X~Poisson(lam), log-space stable
    return max(0.0, 1.0 - sum(math.exp(-lam + k*math.log(lam) - math.lgamma(k+1)) for k in range(int(x))))
print("(D) Poisson fill probability (mu*T = 1200 share outflow):")
for x in (600, 1200, 1500):
    print(f"   x={x:>5}: P(xi>=x)={poisson_tail(x, 1200.0):.4f}")
```
```
Q=   0: closed= 850.41  MC= 848.49
Q=1000: closed= 609.34  MC= 609.51
Q=3000: closed= 312.85  MC= 316.49
(B) FIFO fill fraction vs queue ahead x:
   x=   0: 0.9762
   x= 400: 0.7728
   x= 800: 0.4024
   x=1000: 0.2238
(C) optimistic model (any print fills 100%) vs conservative:
   x=   0: optimistic=1.0000  conservative=0.9762  overstatement=1.02x
   x= 400: optimistic=1.0000  conservative=0.7728  overstatement=1.29x
   x= 800: optimistic=1.0000  conservative=0.4024  overstatement=2.49x
   x=1000: optimistic=1.0000  conservative=0.2238  overstatement=4.47x
(D) Poisson fill probability (mu*T = 1200 share outflow):
   x=  600: P(xi>=x)=1.0000
   x= 1200: P(xi>=x)=0.5038
   x= 1500: P(xi>=x)=0.0000
```
Read it as the whole folder in miniature: the binomial closed form and its Monte Carlo agree to ~3 decimals (the model is *simulable*); and the naive fill rule is **fine when you are at the front of the queue and catastrophic when you are not** — exactly the regime a backtest with no queue awareness cannot see.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full failure analysis lives in [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Optimistic fills (the standing-queue delusion).** Treating "a trade printed at my price" as "I filled" books fills that never happened; measured on [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/05-failure-modes-and-practice|05]] (F1), the naive rule booked **800 shares** where FIFO fills **234** ($3.4\times$ overbooking).
2. **Ignoring the queue.** The fill condition is $\xi\ge x$, not $\xi\ge 0$; no-queue fills can overstate edge by nearly an order of magnitude (\$16.00 vs \$1.86 per order).
3. **Look-ahead in replay.** Deciding the fill from data *after* the cancellation/decision time inflated $P(\text{fill})$ from $0.3301$ to $1.0000$ in the toy replay.
4. **Latency omission.** Your modeled fill assumes you acted instantly; real quotes are stale for $\ell$ and the fraction of *adverse* fills rises with it ($P\!\approx\!1-e^{-\rho\ell}$).
5. **Ignoring your own impact.** A backtest that assumes your order does not move the price omits a cost that scales as $\eta X^2/T$ (\$25{,}000 on a 1-day 100k-share liquidation — not a rounding error).

---

### 5. Canonical Literature & Study References

- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5–40 (2000). *The permanent/temporary-impact cost model an execution simulator must calibrate ($E[x]$, $V[x]$, $\eta$, $\gamma$).* `ADV`
- **Almgren, Thum, Hauptmann & Li** — "Direct estimation of equity market impact," *Risk* 18(7), 58–62 (2005). *The empirical impact parameters a realistic simulator is calibrated to; the square-root/power-law shape.* `ADV`
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (OUP, 2007), Ch 14 (implementation shortfall, effective/realized cost, VWAP) and Ch 15 (prospective costs, order placement, diffusion-barrier execution, censoring). *Corpus verification `hasbrouck_ch11-15.md` / `hasbrouck_ch1-5.md`.* `INT`
- **Cont, Rama; Kukanov, Arseniy** — "Optimal order placement in limit order markets," *Quantitative Finance* 17(4), 553–571 (2017). *The fill function $(\xi-Q)^+-(\xi-Q-L)^+$ and its use as a simulation primitive.* `ADV`
- **Cont, Stoikov & Talreja** — "A stochastic model for order book dynamics," *Operations Research* 58(3), 549–563 (2010). *The tractable queue model fast enough for Monte Carlo fill simulation — the standard substrate of execution backtests (corpus sub-topic "Backtesting & Simulation of Execution").* `ADV`
- **Gould, Porter, Williams, McDonald, Fenn & Howison** — "Limit order books," *Quantitative Finance* 13(11), 1709–1742 (2013). *The survey listing the stylized facts any credible execution simulator must reproduce (and the cancel-to-trade ratios that break naive fills).* `ADV`
- **Abergel, Anane, Chakraborti, Jedidi & Toke** — *Limit Order Books* (Cambridge, 2016). *Agent-based LOB simulation and order-placement micro-simulation used to test execution logic.* `ADV`
- **López de Prado, Marcos** — *Advances in Financial Machine Learning* (Wiley, 2018), Ch 11 (the dangers of backtesting), Ch 12 (backtesting through cross-validation), Ch 13 (backtesting on **synthetic** data). *The case for Monte Carlo/synthetic execution evaluation and the overfitting discipline.* `INT`

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Poisson processes, first passage) · [[foundations/numerical-methods/index|Numerical Methods]] (Monte Carlo, standard error) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (Roll bounce, autocovariance)
- Sibling in-pillar: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] (the fill model in depth) · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (the cost model to calibrate) · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] (where latency enters) · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]]
- Cross-pillar: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (the signal-backtest half of the honesty problem) · [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (the impact an execution simulator must reproduce)

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Mechanics + models (undergrad/job-seeking):** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/02-why-execution-backtests-lie|02 · Why Execution Backtests Lie]] → [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/03-the-fill-model|03 · The Fill Model]] → [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/04-market-replay-vs-monte-carlo|04 · Market Replay vs Monte Carlo]].
- **Robustness (practitioner/graduate):** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/06-advanced-extensions|06 · Advanced Extensions]].
- Sub-pages (in-folder): 01 From Zero · 02 Why They Lie · 03 The Fill Model · 04 Replay vs Monte Carlo · 05 Failure Modes · 06 Extensions
