---
title: "05 — Failure Modes & Real-World Practice: Misclassification, Non-Portable Thresholds, and the Andersen Critique"
tags:
  - pillar-market-making
  - failure-modes
  - vpin
  - bulk-classification-error
  - andersen-bondarenko
---

**Basic Prerequisites:** [[pillars/06-market-making/toxic-order-flow-and-vpin/04-vpin|04 · VPIN]] and [[pillars/06-market-making/toxic-order-flow-and-vpin/02-probability-of-informed-trading|02 · PIN]].

---

### 1. Intuition & Practical Objective

VPIN and PIN are mathematically clean and empirically dangerous in five specific ways. This page names them precisely so a market maker or student knows *which* assumption is biting and *how* it shows up in practice. The objective is not cynicism — it is the discipline of knowing where the toxicity metric is an approximation so its output is read correctly.

The five failures, in one line each:

1. **Bulk/tick misclassification.** Direction is *inferred* from prices, so any price move can be signed as if it were informed one-sided flow.
2. **Non-portable thresholds.** VPIN's absolute level depends on the arbitrary bucket size $V$ and window $n$; "VPIN > 0.3" means nothing across instruments.
3. **Volatility, not information (the Andersen critique).** A high-VPIN episode may be high *volatility*, not high *toxicity* — the two are conflated by construction.
4. **The self-fulfilling kill-switch.** When many makers use the same VPIN threshold, a small toxicity spike triggers mass simultaneous withdrawal — the liquidity evaporation the metric is meant to predict.
5. **Data needs & the $\alpha\mu$ ridge.** PIN needs clean buy/sell counts and cannot separate $\alpha$ from $\mu$; VPIN needs fine, correctly-stamped trades and a well-chosen $\sigma_{\Delta P}$.

---

### 2. Mathematical Ground Truth & Derivations

**Bulk classification error, quantified.** BVC assigns $V_\tau^B=\sum Z(\Delta P_i/\sigma_{\Delta P})$. If a bucket's price change $\Delta P_i$ is *not* driven by informed flow but by volatility or a mechanical trend, the classification reads it as imbalance:

$$|V_\tau^S-V_\tau^B|=\left|\sum_i\left(1-2Z\!\left(\tfrac{\Delta P_i}{\sigma_{\Delta P}}\right)\right)\right|,$$

which grows as $|\Delta P_i|/\sigma_{\Delta P}$ grows. **Any** large price move — informed or not — inflates the measured imbalance and hence VPIN.

**Non-portability of the level.** VPIN's denominator is $nV$; changing $V$ rescales how imbalance accumulates across buckets. Because the same underlying tape yields *different* VPIN magnitudes at different $V$, the level is an artifact of the tuning choice, not a universal toxicity measure.

**The Andersen–Bondarenko logic.** Time-bar (trade-time) VPIN is strongly correlated with volume and realized volatility by construction, because the order-imbalance measure $E[|V^S-V^B|]$ is itself driven by the size and variability of price moves. A metric that rises with volatility cannot cleanly separate "informed flow" from "volatile flow," and ELO's specific claim that VPIN reliably foreshadowed the May 6, 2010 crash did not survive the critique's out-of-sample check.

---

### 3. Computational Implementation — the level depends on the tuning parameter (stdlib only)

Fix one tape with a genuinely toxic informed sell wave, and show that the average VPIN level moves substantially with the *arbitrary* bucket-size choice $V$ — so absolute thresholds are not portable.

```python
import math, random

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def vpin_tape(prices, volumes, V, n):
    dps, prev = [], prices[0]
    for p, v in zip(prices, volumes):
        for _ in range(v):
            dps.append(p - prev)
        prev = p
    mean = sum(dps) / len(dps)
    sd = math.sqrt(sum((x - mean)**2 for x in dps) / (len(dps)-1))
    Vb, Vs, cum, b, s = [], [], 0.0, 0.0, 0.0
    for x in dps:
        pbuy = N(x / sd); cum += 1.0; b += pbuy; s += (1 - pbuy)
        if cum >= V:
            Vb.append(b); Vs.append(s); cum, b, s = 0.0, 0.0, 0.0
    vp = [sum(abs(Vb[i] - Vs[i]) for i in range(t - n, t)) / (n * V)
          for t in range(n, len(Vb) + 1)]
    return sum(vp) / len(vp)

# A fixed tape with one truly-toxic informed sell wave in the middle third.
rng = random.Random(3); base = 2000.0; P, Vol = [], []
for t in range(1500000):
    toxic = 600000 <= t < 1000000
    drift = -0.05 if toxic else 0.0
    side = -1 if (toxic and rng.random() < 0.85) else (1 if rng.random() < 0.5 else -1)
    base += drift + side * 0.02 + rng.gauss(0, 0.01)
    P.append(base); Vol.append(rng.randint(1, 4))

print("The SAME tape, one truly-toxic informed sell wave, VPIN level vs bucket size V (n=15):")
for V in (10000, 50000, 100000):
    print(f"  V={V:7d}:  average VPIN = {vpin_tape(P, Vol, V, 15):.4f}")
print("The absolute VPIN level moves a lot with the arbitrary bucket-size choice V. So a fixed")
print("threshold like 'VPIN > 0.3 is toxic' is not portable across instruments or settings -- ELO's")
print("own caveat that what matters is the POSITION of a VPIN in its own distribution, not its level.")
```
```
The SAME tape, one truly-toxic informed sell wave, VPIN level vs bucket size V (n=15):
  V=  10000:  average VPIN = 0.2572
  V=  50000:  average VPIN = 0.3006
  V= 100000:  average VPIN = 0.3896
The absolute VPIN level moves a lot with the arbitrary bucket-size choice V. So a fixed
threshold like 'VPIN > 0.3 is toxic' is not portable across instruments or settings -- ELO's
own caveat that what matters is the POSITION of a VPIN in its own distribution, not its level.
```

The same toxic tape reads 0.26, 0.30, or 0.39 purely depending on $V$. A trader who sets a hard alarm at 0.30 would have fired on one tuning and slept through another. The defensible practice: standardize $V$ and $n$, then benchmark each VPIN reading against *its own* historical distribution — never against a universal constant.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Misclassification by construction.** BVC and the tick rule infer direction from prices, so a *non*-informed price move (volatility cluster, public trend, index move) is signed as one-sided informed flow, inflating VPIN. The remedy is to cross-check a high-VPIN against a volume/volatility baseline ([[pillars/06-market-making/toxic-order-flow-and-vpin/04-vpin|04 · VPIN]]).
2. **Non-portable absolute thresholds.** As shown above, the level is an artifact of $V$ and $n$. Use distributional position, not a fixed cutoff.
3. **Conflating toxicity with volatility (Andersen & Bondarenko 2014).** Because the imbalance measure grows with price-move size, VPIN is driven by volume/volatility and does not robustly separate informed flow from noise — and did not reliably predict the flash crash. Read VPIN as a flow-imbalance gauge, not an information oracle.
4. **The self-fulfilling kill-switch.** Mass adoption of the same VPIN threshold means a shared alarm: when it triggers, all makers pull quotes at once — manufacturing the very liquidity evaporation the metric predicts. (This is the coordination-failure side of the flash-crash narrative.)
5. **Data hunger.** VPIN needs fine, correctly-stamped intraday data and a well-chosen $\sigma_{\Delta P}$; PIN needs reliable daily buy/sell counts and still cannot separate $\alpha$ from $\mu$ (the ridge). Garbage in, garbage out applies doubly to a metric that *signs* every tick.

---

### 5. Canonical Literature & Study References

- **Andersen, T. G. & Bondarenko, O. (2014)**, *VPIN and the flash crash*, J. Financial Markets 17, 1–46 — the essential critique: VPIN is dominated by volume/volatility; the flash-crash prediction does not hold up. *Primary PDF: `35_Andersen_2014...` in corpus.*
- **Easley, López de Prado & O'Hara (2012)**, *Flow toxicity and liquidity in a high-frequency world*, RFS 25(5) — the original VPIN claim, and their own caveat that VPIN's *position in its distribution*, not its level, is what matters. *Primary PDF in corpus.*
- **Hasbrouck (2007)**, Ch 6 — the $\alpha\mu$ identification ridge that limits how much PIN can be trusted. *Math-verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/toxic-order-flow-and-vpin/04-vpin|04 · VPIN]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/03-the-ekop-model|03 · The EKOP Model]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Index Hub]]
- Forward: [[pillars/06-market-making/toxic-order-flow-and-vpin/06-advanced-extensions|06 · Advanced Extensions]] (how to *use* the gauge despite the failures)
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|Adverse Selection · Failure Modes]] (the winner's curse and toxicity ≠ volatility) · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] (the crash channel)
