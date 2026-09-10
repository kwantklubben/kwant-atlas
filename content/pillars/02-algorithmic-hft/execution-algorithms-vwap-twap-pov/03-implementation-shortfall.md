---
title: "03 - Implementation Shortfall: Arrival Price and the Paper-versus-Reality Gap"
tags:
  - pillar-algorithmic-hft
  - execution-algos
  - implementation-shortfall
  - perold
  - arrival-price
  - benchmarks
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/02-twap-vwap-pov|02 - TWAP-VWAP-POV]] and basic probability.

---

### 1. Intuition & Practical Objective

VWAP/TWAP are *day* benchmarks: they ask "how close to the day's average did you get?" **Implementation shortfall (IS)** asks a harder and more honest question: *how much worse is your realized result than the paper decision you made at the moment you decided?* Perold (1988) invented it as **"paper versus reality."**

The idea is blunt. The portfolio manager's decision is a *paper* transaction: buy $q$ shares at the decision-time price $m_0$. The reality: you filled only a fraction $\\kappa$ at average price $\\bar p$, and by the time you finished, the price had moved to $m_t$. IS is the dollar gap between those two worlds, decomposed into two costs you can manage separately:

- **Execution cost** — you filled shares, but at a price worse than the decision price.
- **Opportunity cost** — you *didn't* fill shares, and the price ran away while you waited.

The practical objective of this page: define IS precisely, reproduce the corpus-verified Perold example, then drive home the **critical distinction between benchmarks** — IS (arrival price) is what a portfolio manager should judge execution by; VWAP is what a broker reports.

> **The one-sentence essence.** "Implementation shortfall compares the executed portfolio to the *decision*, not to the day — it is execution cost on what you traded plus opportunity cost on what you failed to trade."

---

### 2. Mathematical Ground Truth & Derivations

**Definition (Perold 1988; Foucault eq 2.29; Hasbrouck eq 14.1).** Let $q$ = desired shares, $\\kappa$ = fraction actually filled, $\\bar p$ = average execution price of the filled part, $m_0$ = decision (arrival) price, $m_t$ = terminal price. Then
$$\\boxed{\\;\\text{IS} = \\kappa\\,q\\,(\\bar p - m_0) + (1-\\kappa)\\,q\\,(m_t - m_0)\\;} = \\underbrace{\\text{execution cost}}_{\\kappa q(\\bar p-m_0)} + \\underbrace{\\text{opportunity cost}}_{(1-\\kappa)q(m_t-m_0)}.$$
For a **buy**, $\\bar p>m_0$ and $m_t>m_0$ are *losses* (positive IS). Hasbrouck writes the same idea in portfolio-vector form,
$$IS = (n_1-n_0)'(p-\\pi_0) + (v-n_1)'(\\pi_1-\\pi_0),$$
execution cost on actual shares traded plus opportunity cost on the shortfall $(v-n_1)$ — and notes the deep structural fact: **execution cost is zero-sum across users sharing the benchmark $\\pi_0$** (one trader's slippage is another trader's edge), while opportunity cost is *not* a transfer; it is pure tracking error.

**The delay decomposition.** Perold/Foucault further split the execution cost into the part attributable to *delay* (drift from decision to first fill) and the part attributable to the fills themselves:
$$\\kappa q(\\bar p - m_0) = \\underbrace{\\kappa q(\\bar p - m_\\tau)}_{\\text{market impact on fills}} + \\underbrace{\\kappa q(m_\\tau - m_0)}_{\\text{delay cost}}.$$

**Why IS beats VWAP as a decision benchmark.** VWAP is *realized-volume-weighted* over the whole day, so a patient broker that sets the day's volume "always beats" it (page 02). IS is anchored to the one price the PM controlled — **the decision price $m_0$** — so it measures what execution actually cost relative to the decision, which is what matters. This is the arrival-price benchmark.

---

### 3. Computational Implementation — reproduce Perold and fresh cases

Reproduce the corpus-verified Perold/Foucault example ($24{,}000$, 2.4% of paper value) and then compute a fresh partial-fill IS with a full decomposition. Stdlib only; reproduced exactly.

```python
def IS(q, kappa, pbar, m0, mt):
    """Foucault eq 2.29: IS = kappa*q(pbar-m0) + (1-kappa)*q(mt-m0)."""
    return kappa*q*(pbar-m0) + (1-kappa)*q*(mt-m0)

# Foucault verified example: 3000x(101-100)+7000x(103-100)=24000 (2.4% of paper)
q=10000; kappa=0.3; pbar=101.0; m0=100.0; mt=103.0
print("Foucault example: q=10000 k=0.3 pbar=101 m0=100 mt=103")
print(f"  IS = {IS(q,kappa,pbar,m0,mt):,.0f}   (corpus-verified 24,000)\n")

# Fresh: buy 50,000 @ arrival 50.00; fill 40,000 @ 50.40; EOD price 51.20
q=50000; kappa=40000/50000; pbar=50.40; m0=50.00; mt=51.20
exec_cost = (q*kappa)*(pbar-m0); opp_cost = q*(1-kappa)*(mt-m0)
is_ = IS(q,kappa,pbar,m0,mt)
print("Perold decomposition, q=50000 k=0.8 pbar=50.40 m0=50.00 mt=51.20")
print(f"  Execution cost   = kappa*q(pbar-m0)   = {exec_cost:,.0f}")
print(f"  Opportunity cost = (1-kappa)q(mt-m0) = {opp_cost:,.0f}")
print(f"  IS total                              = {is_:,.0f}")
print(f"  basis points of decision value: {1e4*is_/(q*m0):.2f} bps\n")
print(f"If kappa=1 (full fill): IS = execution cost only = {IS(q,1.0,pbar,m0,mt):,.0f}")
print(f"If pbar=mt (fills all at terminal): no opp cost, IS = {IS(q,kappa,mt,m0,mt):,.0f}")
```
```
Foucault example: q=10000 k=0.3 pbar=101 m0=100 mt=103
  IS = 24,000   (corpus-verified 24,000)

Perold decomposition, q=50000 k=0.8 pbar=50.40 m0=50.00 mt=51.20
  Execution cost   = kappa*q(pbar-m0)   = 16,000
  Opportunity cost = (1-kappa)q(mt-m0) = 12,000
  IS total                              = 28,000
  basis points of decision value: 112.00 bps

If kappa=1 (full fill): IS = execution cost only = 20,000
If pbar=mt (fills all at terminal): no opp cost, IS = 60,000
```

**Read the numbers.** The untouched-Foucault case reproduces $24{,}000$ exactly. The fresh case: execution cost on the 40,000 filled shares is $16{,}000 = 0.8\\cdot50{,}000\\cdot(50.40-50)$; opportunity cost on the 10,000 unfilled shares is $12{,}000 = 0.2\\cdot50{,}000\\cdot(51.20-50)$. **Observe the knife-edge**: if the trader had been perfectly patient and filled everything at the terminal price, IS would be $60{,}000$ (all opportunity, no estimate saved), while filling everything at the realized average price $\\bar p=50.40$ gives $20{,}000$ (execution cost only, no opportunity cost) — the schedule is the map between these, which is exactly the Almgren–Chriss trajectory of the sibling folder.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Benchmark choice changes your "score."** IS relative to decision price is what the PM cares about; VWAP slippage is what the broker reports. They routinely disagree, and — because VWAP is gameable — one shows "alpha" that is really a benchmarking artifact (Harris 2003; Hasbrouck Ch 14).
2. **Opportunity cost is real but invisible in glossy reports.** A broker that fills only half your order shows a *great* execution cost on the filled half while the unfilled half's drift dominates. Perold's whole point is **IS must charge the miss.**
3. **IS is a random variable before you trade.** $\\bar p$ and $m_t$ are unknown ex-ante; only their distribution is. Optimizing IS therefore means optimizing $\\mathbb{E}[\\text{IS}]$ and its variance (the AC objective) — never a single static guess.
4. **Execution cost is a transfer, not a loss.** Because it nets to zero across users sharing $\\pi_0$, a desk can look "low cost" by being on the right side of a transfer. Aggregate IS is a *selection* statistic, not a *quality* statistic (Hasbrouck Ch 14).

---

### 5. Canonical Literature & Study References

- **Perold, André F.** — "The implementation shortfall: Paper versus reality," *Journal of Portfolio Management* 14(3), 4-9 (1988). *The origin of the IS benchmark.*
- **Foucault, Pagano, Roëll** — *Market Liquidity* (2013), Ch 2, eq 2.29 (IS decomposition + delay split) with the $24{,}000$ worked example. *Corpus verification `foucault_ch1-3.md`: verified exactly.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 14 eq 14.1 (portfolio IS, zero-sum property). *Corpus verification `hasbrouck_ch11-15.md`.*
- **Almgren & Chriss** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000). *The arrival-price / IS objective as a mean-variance optimization.*

---

### 6. Connected Graph Bridges

- Continue: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/04-scheduling-and-volume-profiles|04 · Scheduling & Volume Profiles]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/05-failure-modes-and-practice|05 · Failure Modes]]
- Model link: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|Optimal Execution · The Execution Problem]]
- Transaction costs context: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]