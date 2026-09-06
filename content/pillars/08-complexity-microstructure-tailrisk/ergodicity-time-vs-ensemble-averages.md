---
title: "Ergodicity: Time vs Ensemble Averages"
tags: [complexity, ergodicity, kelly-criterion, ruin]
---

# Ergodicity: Time vs Ensemble Averages

The ergodicity problem (Peters & Gell-Mann, 2016) exposes why standard expected utility theory leads investors to ruin.

## 1. The Core Paradox
- **Ensemble Average:** The average outcome across $N$ parallel universes at time $t$:
  $$\langle X(t) \rangle = \frac{1}{N} \sum_{i=1}^N X_i(t)$$
- **Time Average:** The long-run average outcome experienced by a single individual over time $T$:
  $$\overline{X} = \lim_{T \to \infty} \frac{1}{T} \int_0^T X(t) dt$$

A system is **ergodic** if and only if:
$$\langle X \rangle = \overline{X}$$

### The Coin Toss Experiment
Toss a coin: Heads you gain $+50\%$; Tails you lose $-40\%$.
- **Ensemble Average:** $\mathbb{E}[R] = \frac{1}{2}(+0.50) + \frac{1}{2}(-0.40) = +5\%$ per toss. Over 1,000 parallel players, average wealth grows!
- **Time Average for 1 Player:** After 2 tosses (1 heads, 1 tails):
  $$W_2 = W_0 \times (1 + 0.50) \times (1 - 0.40) = W_0 \times 1.50 \times 0.60 = 0.90 W_0$$
  The player loses **$-10\%$ every two tosses!** The time average growth rate is:
  $$g = \mathbb{E}[\ln(1 + R)] = \frac{1}{2}\ln(1.5) + \frac{1}{2}\ln(0.6) \approx -0.053 \implies -5.3\% \text{ per toss!}$$
  Almost every individual player goes mathematically bankrupt ($W_t \to 0$ as $t \to \infty$), even though the ensemble average explodes to infinity due to a microscopic fraction of extraordinarily lucky paths.

---

## 2. The Kelly Criterion (Log Wealth Optimization)
To maximize long-run time-average wealth growth and prevent ruin, an investor must maximize expected log wealth:
$$f^* = \arg\max_f \mathbb{E}[\ln(1 + f R)] = \frac{p \cdot b - q}{b}$$
Where $p$ is win probability, $q = 1 - p$, and $b$ is the win/loss payout ratio.
