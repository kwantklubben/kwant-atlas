---
title: "05 — Failure Modes & Real-World Practice"
tags:
  - pillar-market-making
  - limit-order-book-mechanics
  - adverse-selection
  - queue-position
  - latency
  - failure-modes
---

**Basic Prerequisites:** [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04 · Matching & Priority]].

---

### 1. Intuition & Practical Objective

The mechanics of pages 01–04 are *clean*: deterministic matching, exact queue positions, well-defined states. Real markets are hostile to that cleanliness in a small number of specific, repeatable ways. This page names them precisely so a practitioner knows **which mechanical assumption to distrust and how the violation shows up in money**.

The three that matter, in one line each:

1. **Adverse selection at the touch** — passive fills are not random; they cluster exactly when the price is about to move against you, so the spread is a *premium for a written option*, not profit.
2. **Queue-position risk** — you can be right about price and still never fill, or fill only in the states you least want. Waiting behind a large queue is not neutral.
3. **Latency** — the book you act on is a stale copy; anyone faster can convert your resting quote into a free option and exercise it against you.

Everything else (spoofing, fleeting liquidity, feed desync) is a variation on these three.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The toxic-fill identity.** Post a buy limit $h$ below the mid (a passive quote capturing half-spread $h$). A sell order arrives and fills it. Conditional on the fill, the "true" value of the asset has moved by $J>0$ against you with probability $\pi$ (an **informed** counterparty) and not moved otherwise. Your per-fill P&L is

$$\pi_{\text{fill}}=\begin{cases} h, & \text{uninformed (prob }1-\pi),\\ h-J, & \text{informed (prob }\pi),\end{cases}
\qquad\Longrightarrow\qquad \boxed{\ \mathbb{E}[\pi_{\text{fill}}]=h-\pi J\ } .$$

The quote is profitable only while the informed share is below the **break-even toxicity**

$$\pi^\star=\frac{h}{J}.$$

Note the structure: *more* spread $h$ tolerates *more* toxicity, and *larger* informed moves $J$ require *less*. This is the seed of the entire adverse-selection literature ([[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]]) and of toxicity metrics like VPIN ([[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]).

**2.2 Queue position as a race.** Your order sits behind $Q_0$ lots. It clears when aggressive flow has consumed $Q_0$ lots at your price — at execution rate $\mu$, an effective queue-clearing rate $\mu/Q_0$. Meanwhile an adverse price move arrives at rate $\nu$. The two are competing exponential clocks, so

$$P(\text{adverse move before fill})\approx\frac{\nu}{\nu+\mu/Q_0}\ \xrightarrow[\ Q_0\uparrow\ ]{}\ 1 .$$

The **expected wait to fill** (execute $Q_0+s$ lots at rate $\mu$) is

$$\mathbb{E}[T]\approx\frac{Q_0+s}{\mu},$$

linear in the queue ahead. Combining the two: a deep queue makes you **slow *and* selectively filled** — the worst of both — because long queues clear only during aggressive bursts, which is precisely when the price is moving.

**2.3 Latency as a loss term.** Suppose an adverse signal (a large order, a related-venue move) arrives and predicts aggressive flow at rate $\mu_{\text{mo}}$; you must cancel within your latency $\delta$ before that flow lands. The fill is picked off unless your cancel wins the race:

$$P(\text{picked off})=1-e^{-\mu_{\text{mo}}\delta},$$

so with signal rate $\lambda$ the **loss rate** is

$$\text{Loss}=\lambda\big(1-e^{-\mu_{\text{mo}}\delta}\big)(J-h).$$

For small $\delta$ this is $\approx\lambda\mu_{\text{mo}}\delta\,(J-h)$ — **linear in latency**, and the multiplicative $J-h$ is why the same latency is cheap in a tight, calm book and ruinous in a wide, fast one. Latency is not "speed for its own sake"; it is the cost of racing for the cancel.

---

### 3. Computational Implementation — the three risks in numbers

The script quantifies all three: the toxic-fill P&L curve (closed form + Monte Carlo), the queue-race odds, and the latency loss term. Standard library only.

```python
# 05 — Three first-principles risks of passive liquidity: toxicity, queue position, latency
import random

# --- A. Adverse selection: expected P&L of a passive fill at the touch ---
h, J = 0.01, 0.05          # half-spread captured ($); adverse move if counterparty is informed ($)
print("expected P&L per passive fill  E = h - pi*J")
for pi in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
    e = h - pi * J
    tag = "break-even" if abs(e) < 1e-12 else ("in the black" if e > 0 else "BLEEDING")
    print(f"  pi={pi:.2f}   E[P&L]={e:+.4f}   {tag}")
print(f"break-even informed share  pi* = h/J = {h/J:.2f}\n")

random.seed(7)
def mc(pi, n=400000):
    return sum((0.0 if random.random() >= pi else -J) + h for _ in range(n)) / n

for pi in (0.10, 0.25):
    print(f"  Monte Carlo pi={pi:.2f}: E[P&L]={mc(pi):+.5f}  (closed form {h-pi*J:+.5f})")

# --- B. Queue position: time-to-fill and the race with an adverse price move ---
mu, nu, my_size = 100.0, 0.5, 50    # lots/s executed at the touch; adverse moves/s; my size
print("\nqueue-position economics (mu=100 lots/s, nu=0.5 moves/s, size=50):")
print(f"{'Q ahead':>8} {'E[full wait] s':>15} {'P(adverse before fill)':>23}")
for Q in (0, 50, 200, 500, 1000):
    wait = (Q + my_size) / mu
    p_adv = nu / (nu + mu / max(Q, 1))   # race: reach front (rate mu/Q) vs adverse move (nu)
    print(f"{Q:>8d} {wait:>15.3f} {p_adv:>23.3f}")

# --- C. Latency: a stale quote is a free option for anyone faster ---
lam, mo_rate = 100.0, 50.0           # toxic-opportunity signals/s; aggressive-order rate/s
print("\nlatency is a loss term (signals/s=100, aggressive flow/s=50, J=0.05, h=0.01):")
print(f"{'latency':>10} {'picked off/fill':>16} {'expected loss $/s':>18}")
for delta in (0.0001, 0.001, 0.01):
    p_pick = 1 - pow(2.718281828459045, -mo_rate * delta)   # P(MO lands before cancel)
    print(f"{delta*1000:>8.2f}ms {p_pick:>16.5f} {lam*p_pick*(J-h):>18.4f}")
```
```
expected P&L per passive fill  E = h - pi*J
  pi=0.05   E[P&L]=+0.0075   in the black
  pi=0.10   E[P&L]=+0.0050   in the black
  pi=0.15   E[P&L]=+0.0025   in the black
  pi=0.20   E[P&L]=-0.0000   break-even
  pi=0.25   E[P&L]=-0.0025   BLEEDING
  pi=0.30   E[P&L]=-0.0050   BLEEDING
break-even informed share  pi* = h/J = 0.20

  Monte Carlo pi=0.10: E[P&L]=+0.00501  (closed form +0.00500)
  Monte Carlo pi=0.25: E[P&L]=-0.00250  (closed form -0.00250)

queue-position economics (mu=100 lots/s, nu=0.5 moves/s, size=50):
 Q ahead  E[full wait] s  P(adverse before fill)
       0           0.500                   0.005
      50           1.000                   0.200
     200           2.500                   0.500
     500           5.500                   0.714
    1000          10.500                   0.833

latency is a loss term (signals/s=100, aggressive flow/s=50, J=0.05, h=0.01):
   latency  picked off/fill  expected loss $/s
    0.10ms          0.00499             0.0200
    1.00ms          0.04877             0.1951
   10.00ms          0.39347             1.5739
```
Three readings. **Toxicity:** at $\pi=0.20$ the passive quote earns exactly nothing; a mere 30% informed flow turns a \$0.01 half-spread into a \$0.005-per-fill bleed — quoted spreads are *calibrated* to this. **Queue:** at $Q_0=1{,}000$ you wait an order of magnitude longer *and* face an 83% chance the adverse move beats your fill; the queue converts a "cheap" back-of-book quote into a lottery you expect to lose. **Latency:** moving from 0.1 ms to 10 ms (100× slower) raises the pick-off rate from 0.5% to 39% and the loss from \$0.02/s to \$1.57/s — an ~80× increase, which is why co-location and kernel-bypass exist ([[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Adverse selection at the touch (the spread is an option premium).** The fill event is *informative*: you are filled more often when you are about to be wrong. $\mathbb{E}[\pi]=h-\pi J$ goes negative past $\pi^\star=h/J$. Any strategy that treats the quoted spread as a riskless margin is short an unpriced option.
2. **Queue-position risk (right, but never filled — or filled only when wrong).** A resting order's expected fill is governed by the size ahead of it, not its price. Deep queues mean long waits *and* adverse selection, because long queues clear mainly in aggressive bursts. Passive liquidity has **fill risk** and **selective-fill risk** simultaneously; both are structural consequences of FIFO priority ([[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04]]).
3. **Latency pick-off (a stale quote is a free option).** The book you act on is a reconstruction of a past state; a faster participant can trade the *current* book against your *stale* quote. The loss is linear in latency, $\approx\lambda\mu_{\text{mo}}\delta(J-h)$, and explodes with $J$ — so latency risk is *state-dependent*, worst exactly when volatility is high.
4. **Feed desynchronisation (the state is wrong).** Dropped, duplicated, or out-of-sequence L3 messages corrupt the reconstruction. The failure is silent: the book still looks valid (uncrossed, sane sizes) but every derived signal — spread, imbalance, queue position, OFI — is computed on a wrong state. Mitigation is sequence-number gap detection and periodic snapshot resync.
5. **Manipulative / fleeting liquidity (a valid state is not a truthful one).** **Spoofing** posts large orders outside the touch and cancels before execution; **fleeting liquidity** flashes quotes that vanish on contact. The matching engine cannot distinguish intent from commitment, so *depth is not belief*. Metrics built on quoted size (naive OFI, depth-weighted imbalance) are fooled; size-weighted *executed* flow is not.
6. **Self-trade and crossed-book handling.** A single participant on both sides of a trade is either prevented (self-match prevention, which can cancel a *genuine* hedge) or allowed (creating wash trades and capital/regulatory problems). And because a crossing order must match immediately, a "crossed book" in your reconstruction is not a signal — it is proof your state has already drifted.

---

### 5. Canonical Literature & Study References

- **Hasbrouck**, *Empirical Market Microstructure*, Ch 5 (sequential-trade models: quote revision after a trade, spread and trade-impact as the principal empirical implications; market failure when uninformed flow is price-sensitive) — *verified in the corpus*.
- **Foucault, Pagano & Röell**, *Market Liquidity*, Ch 3 (adverse selection ⇒ permanent impact; order-processing ⇒ instant reversal; inventory ⇒ slow reversal; the full picture, Fig 3.8–3.9) — *verified in the corpus*.
- **Glosten & Milgrom (1985)**, *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders* — the canonical adverse-selection spread.
- **Easley, Kiefer, O'Hara & Paperman (1996)** / **Easley, Hvidkjaer & O'Hara (2002)** — PIN and the probability of informed trading; the empirical toxicity measure.
- **Bouchaud, Farmer & Lillo**, *How markets slowly digest changes in supply and demand* (2009) — price impact, liquidity provision, and the empirical mechanics of execution risk.
- **Menkveld & Zoican (2017)**, *Need for speed? Exchange latency and liquidity* — the latency/liquidity trade-off formalised.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04 · Matching & Priority]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Index Hub]]
- Forward: [[pillars/06-market-making/limit-order-book-mechanics/06-advanced-extensions|06 · Advanced Extensions]]
- Related: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/limit-order-book-mechanics-and-l3|Limit Order Book Mechanics & L3 Data]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
