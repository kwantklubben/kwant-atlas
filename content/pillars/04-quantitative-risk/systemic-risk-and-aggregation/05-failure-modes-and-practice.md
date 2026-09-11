---
title: "05 — Failure Modes & Real-World Practice (Procyclicality, Tail Dependence, Aggregation Fallacy)"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - failure-modes
  - procyclicality
  - agg-fallacy
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/04-aggregating-risk-types|04 · Aggregating Risk Types]].

---

### 1. Intuition & Practical Objective

Systemic-risk practice is not a software problem; it is a *feedback* problem. This page names the three ways the tools in 03–04 break, each tied to its first principle. The objective: know *exactly why* the "obvious" implementation is wrong, so the residual is measured rather than assumed away.

1. **Procyclicality** (feedback to the real economy): VaR/ES fall *in calm* and rise *in stress*, so capital and leverage automatically contract exactly when markets need them — the individually rational hedge is collectively destabilising.
2. **Unmeasurable tail dependence** (statistical ceiling): the quantity that decides aggregate capital — extreme joint-tail probability — has ~zero observations, so the copula/model choice, not the data, is doing the work.
3. **The aggregation fallacy** (logical ceiling): every way of adding market+credit+liquidity+operational silently asserts a dependence assumption that is either known-bad or directionally dangerous.

---

### 2. Mathematical Ground Truth & Derivations

**The procyclicality loop.** Let a value-at-risk-driven bank target leverage $\ell_t = c / \text{VaR}_t$ (hold enough capital that a $\text{VaR}_t$ loss won't breach it). During stress volatility $v_t$ spikes, so $\text{VaR}_t \approx z_\alpha v_t$ jumps, so required leverage $\ell_t$ *falls* — the bank must cut risk now, in the worst market. Selling illiquid assets at a fire-sale discount (penalty $~\propto v_t$) feeds *more* volatility and *more* forced selling:

$$
\text{stress}\;\Rightarrow\; v_t\!\uparrow\ \Rightarrow\ \text{VaR}_t\!\uparrow\ \Rightarrow\ \ell_t\!\downarrow\ \Rightarrow\ \text{fire-sales}\;\Rightarrow\; v_t\!\uparrow .
$$

This is the *loss spiral* and *margin spiral* of Brunnermeier–Pedersen (2009) viewed at the bank level: **per-firm risk-parity is systemically procyclical.** The fix (see 06) is *countercyclical* capital: build buffers in good times so they don't have to be built in bad ones.

**Tail dependence is a limit, not a parameter.** Upper-tail dependence is defined as a limit as the threshold recedes to infinity:

$$
\lambda_u = \lim_{u\to 1^+} \mathbb{P}\big(X_1 > F_1^{-1}(u) \,\big|\, X_2 > F_2^{-1}(u)\big).
$$

Estimating it from data means counting *joint extreme* events — scarce by construction. A Gaussian copula has $\lambda_u=0$ (no asymptotic tail dependence); a t-copula with df $<\infty$ has $\lambda_u>0$. Because $\lambda_u$ is a *limit*, no finite sample can pin it down; **the choice of $\lambda_u$ is an act of judgement, not estimation**, and it moves the aggregate capital materially (0.0013 vs 0.0030 in §04 — a >2× read on the 1% joint tail).

---

### 3. Computational Implementation — procyclicality in numbers

We run a bank through a GARCH(1,1) stress with a single $-6\sigma$ shock, under two leverage policies: **fixed** (constant leverage) vs **VaR-target** (cut leverage when vol rises, plus a fire-sale penalty ~ vol). The VaR-target bank's *compliance* is the source of *amplification*. Stdlib only.

```python
import math, random
def gauss():
    u1 = max(random.random(), 1e-12)
    return math.sqrt(-2.0*math.log(u1)) * math.cos(2.0*math.pi*random.random())

random.seed(3)
T = 400
bvol = 0.005
omega = (1.0 - 0.10 - 0.88)*bvol*bvol     # GARCH(1,1) a=.10 b=.88, unconditional var = bvol^2
a, b, l0 = 0.10, 0.88, 12.0

def simulate(vartarget):
    vol2t, W, sold, prev_l = bvol*bvol, 1.0, 0.0, l0
    for t in range(T):
        z = gauss()
        if t == 150: z = -6.0              # one -6 sigma stress shock
        r = math.sqrt(vol2t)*z
        var_t = math.sqrt(vol2t)
        l = min(l0*(bvol/var_t) if vartarget else l0, 16.0)   # VaR-target: halve leverage when var doubles
        if l < prev_l:
            amt = (prev_l - l)*W
            W  -= 0.03*(var_t/bvol)*amt    # fire-sale penalty scales with vol
            sold += amt
        W *= (1.0 + l*r)
        prev_l = l
        vol2t = omega + a*(r*r) + b*vol2t
    return W, sold

Wfix, sfix = simulate(False)
Wtar, star = simulate(True)
print(f"fixed leverage      : terminal wealth = {Wfix:.3f}    forced sales {sfix:.3f}")
print(f"VaR-target leverage : terminal wealth = {Wtar:.3f}    forced sales {star:.3f}")
```
```
fixed leverage      : terminal wealth = 0.612    forced sales 0.000
VaR-target leverage : terminal wealth = 0.011    forced sales 42.835
```

**Read the output.** The *fixed*-leverage bank takes the same $-6\sigma$ shock and comes out with **0.612** of its capital, with zero forced selling. The *VaR-target* bank — the one obeying the "safe" rule — ends at **0.011**, a near-total wipeout, after **42.835** of cumulative forced selling. The deleveraging it was *required* to do in the volatile period turned a survivable shock into ruin by selling into a vanishing liquid market. This is procyclicality made concrete: **the risk *measurement* (VaR up ⇒ capital need up) triggered the risk *creation* (sell ⇒ worsen the market ⇒ more vol ⇒ more selling).** The first-principles point: a measure that reacts to *current* volatility, applied as a *binding* capital/leverage constraint, is a positive-feedback amplifier of the very volatility it reports.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Procyclicality (feedback).** VaR/ES/leverage rules expand-and-contract with *current* vol, forcing selling in exactly the worst state — the §3 experiment: compliance destroys 0.011-vs-0.612 and sells 42.8×. First principle: a binding constraint driven by a lagging, mean-reverting volatility process creates its own momentum.
2. **Unmeasurable tail dependence (statistical).** Aggregate-capital drivers like $\lambda_u$ are limits with ~zero joint-tail data; Gaussian vs t-4 gives a >2× different 1% joint-tail (0.0013 vs 0.0030). First principle: you cannot estimate an asymptotic property from a finite sample of the rare region where it matters. Report the range across copulas and capitalise the worst.
3. **Aggregation fallacy (logical).** "Sum the ES" overstates (subadditivity: 63.97 vs true 45.85–55.65 in §04); "treat as independent" understates; Gaussian copula assumes $\lambda_u=0$. No dependence choice is innocent. First principle: aggregation is a *modelling* claim about unobservable dependence, so disclosure of the assumption is as important as the number.
4. **The hub-and-spoke blind spot.** Network measures need the full exposure matrix; bilateral/OTC data is incomplete, and the missing edges are the contagious ones (see [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/02-contagion-and-networks|02 · Contagion & Networks]]).
5. **The SRISK horizon.** Capital-shortfall measures depend on the (arbitrary, procyclical) crisis threshold and horizon; two defensible calibrations can rank the same banks differently.

---

### 5. Canonical Literature & Study References

- **Brunnermeier & Pedersen**, *Market Liquidity and Funding Liquidity*, *RFS* 22(6) (2009) — the loss/margin spiral, the micro-mechanism of §3's loop (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]]).
- **Adrian & Brunnermeier**, *CoVaR*, *AER* 106(7) (2016) — CoVaR as a feed-back measure; its procyclical sensitivity is a known defect.
- **McNeil, Frey & Embrechts**, *QRM* (2015), §5.4 (tail-dependence limits) and §6.4.2 (copula-risk aggregation and its model risk). *In the corpus.*
- **Embrechts, McNeil & Straumann**, *Correlation and Dependence in Risk Management* (2002) — the classic "correlation is not a good dependence measure for fat tails" argument.
- **BCBS**, *Principles for Sound Stress Testing Practices and Supervision* (2009) — the regulatory push that moved firms from pure VaR to scenario/stress capital (bridges [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/04-aggregating-risk-types|04 · Aggregating Risk Types]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/06-advanced-extensions|06 · Advanced Extensions (macroprudential & stress integration)]]
- Sibling: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]] (the amplification channel) · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]