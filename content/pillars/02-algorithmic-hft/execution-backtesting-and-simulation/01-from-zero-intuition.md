---
title: "01 - Execution Backtesting from Zero: Signal vs Execution"
tags:
  - pillar-algorithmic-hft
  - execution-backtesting
  - intuition
  - implementation-shortfall
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of execution backtesting with **no prior knowledge needed**. The objective is one idea: **a trade price and a fill are not the same thing.** A signal backtest treats the price series as something you can *transact at on demand*. An execution backtest cannot — because the price series is the **output** of a matching process, and *whether you get to participate in that process* is a separate, harder question.

Start with the dumbest question: *why can't I just test my execution algorithm by backtesting on prices?* Because "buy 10,000 shares at 10:00" is not an instruction a price series can honour. To turn it into a fact you must answer three things the price series never asked:

1. **Did I fill at all?** A market order fills (minus size you walk through), but a *limit* order only fills if the queue ahead of you is consumed. Book that as a coin that may come up "no."
2. **At what price relative to the decision price?** You buy at the *ask*, not the mid — you pay the half-spread on entering and again on exiting.
3. **Did the market move because of me, or against me?** Your own order has impact, and your passive fills are adversely selected.

Three "aha"s:

1. **The mid is a theory; the trade is a price.** The Roll model (Hasbrouck Ch 3) writes the trade price as $p_t = m_t + q_t\,c$: the efficient price plus a $\pm c$ bounce at half the spread. A backtest that fills at $m_t$ has *silently deleted $c$ per share on every trade.*
2. **A fill is a queue event, not a price event.** "The market printed at my price" $\ne$ "I filled." You fill when the cumulative outflow **ahead of you** passes your position: $\xi \ge x$. Ignoring $x$ is the single largest source of fake edge.
3. **Execution cost is a *separate return stream*.** Perold's *implementation shortfall* decomposes realised vs paper P&L into an **execution cost** (how badly you paid) and an **opportunity cost** (what you failed to execute). A signal backtest sets the first to zero and the second to zero by assumption.

> **The one-sentence essence.** "A signal backtest tells you whether the *idea* was right; an execution backtest tells you whether the *idea survives contact with the order book* — and these two answers can have opposite signs for the same alpha."

---

### 2. Mathematical Ground Truth & Derivations

**The two experiments, side by side.** Suppose a signal earns an expected favourable move $\alpha_H$ over a holding horizon of $H$ ticks, and the mid moves $\sigma\sqrt{H}$ of noise. Then

- **Signal backtest P&L per trade** (fill at mid, both legs, full size): $\;g = \alpha_H + \varepsilon,\qquad \varepsilon \sim \mathcal N(0,\sigma^2 H).$
- **Execution backtest P&L per trade** (you cross the spread in and out, and pay impact per leg): $\;g_{\text{exec}} = \alpha_H - s - 2\,h,\;$ where $s$ is the quoted spread and $h$ the per-leg temporary impact.

The Sharpe ratios are the same denominator $\sigma\sqrt H$; the cost terms subtract **expected value only**. So

$$
\text{SR}_{\text{signal}}=\frac{\alpha_H}{\sigma\sqrt H},\qquad
\text{SR}_{\text{exec}}=\frac{\alpha_H-s-2h}{\sigma\sqrt H},
$$

and the whole game is the *sign and size of $s+2h$ relative to $\alpha_H$*.

**Perold's implementation shortfall** (Hasbrouck Ch 14, eq 14.1) is the accounting identity that makes the omission precise. With $n_0$=initial position, $v$=desired position, $n_1$=final position, decision/arrival price $\pi_0$, terminal price $\pi_1$:

$$
\text{IS}=\underbrace{(n_1-n_0)'(p-\pi_0)}_{\text{execution cost}}+\underbrace{(v-n_1)'(\pi_1-\pi_0)}_{\text{opportunity cost}},
$$

A signal backtest that assumes you always trade the full size at $\pi_0$ forces **both** terms to zero. An execution backtest must simulate $p$ (the realised fill price, from the book) *and* $n_1$ (the realised filled quantity, from the queue).

**Effective vs realized cost** (Hasbrouck Ch 14, eq 14.2) splits what you paid into spread and impact:

$$
p_t-m_t=\underbrace{\big(p_t-m_{t+5}\big)}_{\text{realized cost}}+\underbrace{\big(m_{t+5}-m_t\big)}_{\text{price impact}}.
$$

A backtest that records only $p_t$ still misses the $m_{t+5}-m_t$ impact term — the part of the move that is *yours*.

---

### 3. Computational Implementation — the same alpha, two verdicts

One alpha, evaluated two ways. The signal backtest fills at the mid; the execution backtest pays the spread on both legs plus impact. Stdlib only.

```python
import random, math, statistics as st
random.seed(42)

H       = 20       # holding period (ticks)
sigma_1 = 0.02     # per-tick mid vol ($)
alpha_H = 0.06     # TRUE expected favourable H-tick move ($) -- the edge
N       = 60000

def run(spread, impact, N=N, seed=42):
    random.seed(seed)
    gross, net = [], []
    for _ in range(N):
        realized = alpha_H + random.gauss(0, sigma_1 * math.sqrt(H))   # in signal direction
        gross.append(realized)
        net.append(realized - spread - 2 * impact)                     # cross in AND out
    return st.mean(gross), st.pstdev(gross), st.mean(net), st.pstdev(net)

print(f"per-trade edge = ${alpha_H:.2f}, per-trade vol = ${sigma_1*math.sqrt(H):.4f}")
print(f"{'regime':20s} {'spread':>7s} {'imp/leg':>8s} | signal-BT mean/SR | exec-BT mean/SR")
for lab, sp, im in (("tight market", 0.02, 0.010),
                    ("wide market", 0.04, 0.020),
                    ("liquid / rebate", 0.005, 0.002)):
    gm, gs, nm, ns = run(sp, im)
    print(f"{lab:20s} {sp:7.3f} {im:8.3f} | {gm:+.4f} / {gm/gs:6.3f} | {nm:+.4f} / {nm/ns:6.3f}")
```
```
per-trade edge = $0.06, per-trade vol = $0.0894
regime                spread  imp/leg | signal-BT mean/SR | exec-BT mean/SR
tight market           0.020    0.010 | +0.0601 /  0.671 | +0.0201 /  0.224
wide market            0.040    0.020 | +0.0601 /  0.671 | -0.0199 / -0.222
liquid / rebate        0.005    0.002 | +0.0601 /  0.671 | +0.0511 /  0.570
```

The signal backtest is **identical in all three rows** ($\text{SR}=0.671$): it never sees cost. The execution backtest takes the *same alpha* to $\text{SR}=0.224$ in a tight market, to $\text{SR}=-0.222$ (a loser) in a wide market, and back to $0.570$ where costs are tiny. **The alpha did not change; the verdict did.** This is why "backtested Sharpe" is meaningless without the fill and cost model underneath it.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Filling at the mid (deleting the spread).** The Roll model says the trade price is $m_t\pm c$. A mid-fill backtest earns a half-spread it can never collect; on a strategy that trades often, this is a pure fiction with an unbounded cumulative cost.
2. **Assuming full size fills.** A signal backtest assumes $n_1=v$ in Perold's identity. Real limit orders are **censored**: only a minority of submitted limit orders ever execute (Hasbrouck Ch 15 reports roughly $13\%$ in the Hasbrouck–Saar data). Unfilled size is the **opportunity cost** term, invisible to the naive test.
3. **Ignoring your own impact.** Treating $p=\pi_0$ drops the $m_{t+5}-m_t$ term; for any size beyond a rounding lot the omitted cost is linear in the metaorder and can exceed the alpha entirely.
4. **Benchmark confusion.** VWAP, arrival price, and close are different benchmarks; a strategy can look great vs VWAP and terrible vs arrival (Hasbrouck Ch 14). The "execution backtest" number is only as good as the benchmark it is measured against.
5. **One-way thinking.** Costs are subtracted on *both* legs and on *every* reprice. A backtest that charges entry only, or only charges when the trade is a taker, will systematically flatter the strategy.

---

### 5. Canonical Literature & Study References

- **Perold, André F.** — "The implementation shortfall: paper vs. reality," *Journal of Portfolio Management* 14(3), 4–9 (1988). *The origin of every execution benchmark; the execution/opportunity-cost decomposition.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 14 (implementation shortfall eq 14.1; effective/realized cost eq 14.2; VWAP and its gaming) and Ch 3 (the Roll trade-price model $p_t=m_t+q_tc$). *Corpus verification `hasbrouck_ch11-15.md` / `hasbrouck_ch1-5.md`.*
- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2) (2000) — the $E[x]$/$V[x]$ cost that a proper execution backtest charges.
- **Harris, Larry** — *Trading and Exchanges* (2003) — the practitioner vocabulary of benchmarks, shortfall, and order handling.

---

### 6. Connected Graph Bridges

- Base: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (the signal-backtest half)
- Continue: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/02-why-execution-backtests-lie|02 · Why Execution Backtests Lie]] · [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Index Hub]]
- Cost model to calibrate: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] · [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]
