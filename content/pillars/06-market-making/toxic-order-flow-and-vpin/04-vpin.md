---
title: "04 — VPIN: Volume-Synchronized Probability of Informed Trading, with Bulk-Volume Classification"
tags:
  - pillar-market-making
  - vpin
  - bulk-volume-classification
  - volume-clock
  - toxicity
---

**Basic Prerequisites:** [[pillars/06-market-making/toxic-order-flow-and-vpin/02-probability-of-informed-trading|02 · PIN]] (what VPIN estimates) and [[pillars/06-market-making/toxic-order-flow-and-vpin/01-from-zero-intuition|01 · From Zero]] (the volume clock).

---

### 1. Intuition & Practical Objective

PIN is a *daily, trade-count* measure. In high-frequency markets that is too coarse and too slow: a single large institutional order is split into thousands of trades, an information event can unfold in minutes, and the *number* of trades is a poor proxy for the *volume* of information. **VPIN** (Easley, López de Prado & O'Hara 2012) fixes both problems at once:

- It works in **volume time** — equal-sized volume buckets, not daily bars — so each measurement contains a comparable amount of trading (and information).
- It measures **imbalance**, $|V^S-V^B|$, which is the observable that reveals the informed fraction.

The practical objective: take a raw trade tape (timestamps, prices, volumes), sign every unit of volume as buy or sell, pack it into volume buckets, and compute a **rolling VPIN** that rises when the flow turns one-sided and toxic — an early-warning gauge for a maker (and the metric ELO claimed it spiked before the May 6, 2010 flash crash).

The only hard sub-problem is **signing** volume as buy or sell, because the tape does not tell you who initiated. VPIN's signature answer is **bulk-volume classification (BVC)**: within a bar, classify the *whole* bar's volume probabilistically from the price change, instead of classifying each trade by a tick rule.

---

### 2. Mathematical Ground Truth & Derivations

**Volume bucketing.** The tape is divided into consecutive buckets of exactly $V$ shares. In bucket $\tau$, with buy-volume $V_\tau^B$ and sell-volume $V_\tau^S$, we have $V_\tau^B+V_\tau^S=V$.

**Bulk-volume classification (BVC).** Take the per-unit price changes $\Delta P_i$ in the bucket. Because $E[\,|V^S-V^B|\,]\approx\alpha\mu$, classify each volume unit by the standard-normal CDF $Z$ of its (normalized) price change (ELO 2012, Appendix A):

$$
V_\tau^B=\sum_{i\in\tau}Z\!\left(\frac{\Delta P_i}{\sigma_{\Delta P}}\right),\qquad
V_\tau^S=V-V_\tau^B.
$$

A large positive price change is almost surely a buy ($Z\to1$); a large negative change almost surely a sell ($Z\to0$); a zero change splits 50/50. This is the *bulk* (bar-wide, probabilistic) analogue of the per-trade Lee–Ready tick rule.

**VPIN.** Over a rolling window of the most recent $n$ buckets:

$$
\boxed{\;\mathrm{VPIN}=\frac{\sum_{\tau=1}^{n}\left|V_\tau^S-V_\tau^B\right|}{\sum_{\tau=1}^{n}\left(V_\tau^S+V_\tau^B\right)}=\frac{\sum_{\tau=1}^{n}\left|V_\tau^S-V_\tau^B\right|}{n\,V}\;}
$$

Since each bucket has exactly $V$ volume, the denominator is $nV$. Because $E[|V^S-V^B|]/E[V^S+V^B]=\alpha\mu/(\alpha\mu+2\epsilon)$, **VPIN estimates the same PIN ratio — in volume time** (ELO eq. 9):

$$
\mathrm{VPIN}\approx\frac{\alpha\mu}{\alpha\mu+2\epsilon}.
$$

ELO's default: $V=\tfrac1{50}$ of average daily volume and $n=50$, updated after every bucket (rolling — bucket 51 in, bucket 1 out). Updating in volume time makes each update a comparable amount of information, and faster during bursts exactly when information arrives faster.

---

### 3. Computational Implementation — BVC + rolling VPIN on a synthetic toxic tape (stdlib only)

Simulate an E-mini-like tape: balanced flow, then a long one-sided *informed selling* burst, then recovery. Sign volume with BVC, bucket, and roll.

```python
import math, random

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))   # std normal CDF

def volume_buckets(prices, volumes, V):
    """Pack a trade tape into volume buckets of V shares; bulk-classify buy/sell."""
    dps, prev = [], prices[0]
    for p, v in zip(prices, volumes):
        for _ in range(v):
            dps.append(p - prev)                 # carry the price change over each unit volume
        prev = p
    mean = sum(dps) / len(dps)
    sd = math.sqrt(sum((x - mean) ** 2 for x in dps) / (len(dps) - 1))
    Vb, Vs, cum, b, s = [], [], 0.0, 0.0, 0.0
    for x in dps:
        pbuy = N(x / sd); cum += 1.0; b += pbuy; s += (1 - pbuy)
        if cum >= V:
            Vb.append(b); Vs.append(s); cum, b, s = 0.0, 0.0, 0.0
    return Vb, Vs

def vpin_series(Vb, Vs, n):
    return [sum(abs(Vb[i] - Vs[i]) for i in range(t - n, t)) / (n * V)
            for t in range(n, len(Vb) + 1)]

# Synthetic tape: quiet balanced flow -> long TOXIC informed sell burst -> recovery.
rng = random.Random(3); base = 2000.0; prices, volumes = [], []
for t in range(300000):
    toxic = 120000 <= t < 220000                       # one-sided informed selling wave
    drift = -0.08 if toxic else 0.0
    side = -1 if (toxic and rng.random() < 0.85) else (1 if rng.random() < 0.5 else -1)
    base += drift + side * 0.02 + rng.gauss(0, 0.01)
    prices.append(base); volumes.append(rng.randint(1, 4))

V, n = 5000, 40
Vb, Vs = volume_buckets(prices, volumes, V)
vp = vpin_series(Vb, Vs, n)
print(f"{len(Vb)} volume buckets (V={V}); rolling VPIN (n={n}) -> {len(vp)} updates")
print(f"  VPIN pre-burst   (quiet flow, buckets ~10-50)  = {sum(vp[2:10])/8:.4f}")
print(f"  VPIN during burst (toxic flow, buckets ~60-110) = {sum(vp[25:70])/45:.4f}")
print(f"  VPIN post-burst  (recovery, buckets ~115-150)   = {sum(vp[-8:])/8:.4f}")
print("Balanced flow -> low VPIN. One-sided informed flow -> VPIN climbs toward its peak.")
```
```
150 volume buckets (V=5000); rolling VPIN (n=40) -> 111 updates
  VPIN pre-burst   (quiet flow, buckets ~10-50)  = 0.0065
  VPIN during burst (toxic flow, buckets ~60-110) = 0.6087
  VPIN post-burst  (recovery, buckets ~115-150)   = 0.0924
Balanced flow -> low VPIN. One-sided informed flow -> VPIN climbs toward its peak.
```

VPIN reads the tape exactly as advertised: **~0.007** on balanced flow (buys and sells cancel), **~0.61** during the one-sided informed selling wave (the toxicity spike), and **~0.09** on recovery. That separation is the entire value of the metric — a real-time, volume-synchronized reading of how informed (and therefore how dangerous) the current flow is.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **BVC is probabilistic, not truthful.** It *infers* direction from price moves, so a price move that is *not* caused by informed flow gets signed as if it were. A volatility cluster or a public trend can manufacture imbalance ([[pillars/06-market-making/toxic-order-flow-and-vpin/05-failure-modes-and-practice|05 · Failure Modes]]).
2. **The absolute level is not portable.** VPIN depends on the arbitrary choices of $V$ and $n$; what matters is a VPIN's *position in its own distribution*, not a fixed threshold.
3. **It is an imbalance gauge, not a crash oracle.** VPIN measures flow one-sidedness; it does not know whether that side is informed or simply panicky/mechanical (the Andersen–Bondarenko critique).
4. **Classification at zero price change.** Units with $\Delta P=0$ get a 50/50 split, understating the true imbalance of that volume — a systematic bias when much volume trades at unchanged prices.

---

### 5. Canonical Literature & Study References

- **Easley, López de Prado & O'Hara (2012)**, *Flow toxicity and liquidity in a high-frequency world*, RFS 25(5), 1457–1493 — the VPIN construction: volume bucketing, bulk-volume classification, eq. 9, Appendix A algorithm. *Primary PDF: `33Easley2012_flow_toxicity_and_liquidity_in.pdf`.*
- **Easley, López de Prado & O'Hara (2011)**, *The microstructure of the "flash crash"*, J. Portfolio Management 37(2) — VPIN spiking before May 6, 2010; the applied motivation. *Primary PDF: `34_Easley_2011...`.*
- **Lee & Ready (1991)**, *Inferring trade direction from intraday data*, J. Finance 46(2) — the tick-rule signing VPIN generalizes. *Primary PDF: `36_Lee_1991...`.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/toxic-order-flow-and-vpin/03-the-ekop-model|03 · The EKOP Model]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/02-probability-of-informed-trading|02 · PIN]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Index Hub]]
- Forward: [[pillars/06-market-making/toxic-order-flow-and-vpin/05-failure-modes-and-practice|05 · Failure Modes]] (misclassification, thresholds, the Andersen critique) · [[pillars/06-market-making/toxic-order-flow-and-vpin/06-advanced-extensions|06 · Advanced Extensions]] (VPIN as a live risk signal)
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]]
