---
title: "06 — Advanced Extensions: Stochastic Models of the Order Book"
tags:
  - pillar-market-making
  - limit-order-book-mechanics
  - order-flow-imbalance
  - queue-reactive
  - hawkes
  - zero-intelligence
---

**Basic Prerequisites:** [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04 · Matching & Priority]] and [[pillars/06-market-making/limit-order-book-mechanics/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Pages 01–05 treated the book mechanically: a state and a deterministic engine. This page treats it **probabilistically** — as a stochastic process whose *statistics* can be modelled, calibrated, and used to forecast. The objective is to place the four canonical modelling families on one map and show what each buys you, so you can choose the right level of abstraction for a task:

| Family | Core idea | Buys you | Costs you |
|---|---|---|---|
| **Zero-intelligence (ZI)** | random arrivals, no strategy | a *null model*: how much price formation is mechanical | ignores informed flow entirely |
| **Markovian / queueing** | Markov chain in queue sizes, rates by distance | tractable spread/spread-depth distributions | strong Markov assumption |
| **Queue-reactive** | touch queues mean-revert to empirical targets | realistic short-horizon price-move probabilities | needs rich calibration |
| **OFI / micro-price** | price change $\propto$ order-flow imbalance | a stable, tradeable impact law | non-stationary under spoofing |

> **The one-sentence essence.** "The order book is a Markov-modulated queueing system whose *shape* is largely mechanical (zero-intelligence reproduces the spread), while its *dynamics* carry the information — and the single most useful dynamic law is that the mid-price moves linearly in order-flow imbalance."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The Markovian queueing model (Cont, Stoikov & Talreja 2010).** Represent the book as queue sizes $Q_i$ at price levels $i$ on both sides. The process is a continuous-time Markov chain driven by three event types, with intensities that depend on the level's **distance from the touch**:

$$
\begin{aligned}
\text{limit add at }(i,\eta):&\quad \lambda^{\text{lim}}_i(p)\ \text{rate, jump } Q_i\to Q_i+\eta,\\
\text{cancel at }(i,\eta):&\quad \lambda^{\text{can}}_i(p),\ \text{jump } Q_i\to Q_i-\eta,\\
\text{market order of size }\eta:&\quad \lambda^{\text{mkt}}(p),\ \text{consume best levels.}
\end{aligned}
$$

Because the intensities are functions of *distance* rather than absolute price, the chain is (approximately) translation-invariant, and one can solve for the joint distribution of the spread, the next price move, and the book's depth. The empirical anchor — that deposit/cancel rates are nearly flat in distance (Bouchaud, Mézard & Potters 2002) — is what makes the model tractable and the book approximately "linear in distance" away from the touch.

**2.2 Order Flow Imbalance and the price-impact law (Cont, Kukanov & Stoikov 2014).** Define the per-event bid/ask contribution

$$
I^b_t=\begin{cases} q^b_t, & b_t>b_{t-1}\\ q^b_t-q^b_{t-1}, & b_t=b_{t-1}\\ -q^b_{t-1}, & b_t<b_{t-1}\end{cases}
\qquad
I^a_t=\begin{cases} -q^a_t, & a_t>a_{t-1}\\ q^a_t-q^a_{t-1}, & a_t=a_{t-1}\\ q^a_{t-1}, & a_t<a_{t-1}\end{cases}
$$

$$
\text{OFI}_t=I^b_t-I^a_t,\qquad \Delta m_t=\beta\,\text{OFI}_t+\varepsilon_t ,
$$

with the slope **inversely proportional to depth** — the deeper the book, the smaller the price move per unit of imbalance. Cont et al. document an almost perfect linear fit empirically; OFI is the pillar's core micro-price signal ([[pillars/06-market-making/limit-order-book-mechanics|LOB Mechanics & L3 Data]]). The size-weighted touch, the **microprice**

$$
m^{\text{micro}}_t=\frac{q^b_t a_t+q^a_t b_t}{q^b_t+q^a_t},
$$

is the static counterpart of the same idea: it prices the *weights*, not the level.

**2.3 Queue-reactive dynamics (Huang, Lehalle & Rosenbaum).** The refined short-horizon model: at the touch, queue sizes are **mean-reverting** to empirical, state-dependent targets $\bar q^\pm$; price changes occur when a touch queue is depleted or improves. This reproduces the empirical fact that *imbalance at the touch forecasts the next move* — which is exactly what a market maker monetises. The transition probability takes the form

$$
P(\text{up-tick}\mid q^b,q^a)=\Phi\!\left(\frac{q^b-\bar q^b}{\theta^b}\right)\cdot\Psi\!\left(\frac{\bar q^a-q^a}{\theta^a}\right),
$$

rising with bid-heavy and ask-light queues.

**2.4 Self-exciting (Hawkes) order flow.** Trade and cancel arrivals cluster in time. A Hawkes process captures this:

$$
\lambda(t)=\mu+\sum_{t_i<t}\phi(t-t_i),\qquad \phi\ge0,\qquad n=\int_0^\infty\phi(s)\,ds<1,
$$

where $n$ is the **branching ratio** (the average number of offspring events per event). $n\to1$ means near-critical, clustered flow; $n$ estimated empirically is high and time-varying, which is *why* volatility clusters and why impact estimates drift. This is the natural bridge to [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] and to market-impact models.

---

### 3. Computational Implementation — a zero-intelligence book, and OFI in it

The classic result (Smith, Farmer, Gillemot & Krishnamurthy 2003) is that **even a market with zero strategic intelligence produces a positive spread and a sensible depth**: those are *mechanical* consequences of random arrival. We simulate such a book, then recover the OFI impact law from its event stream. Standard library only.

```python
# 06 — Zero-intelligence continuous double auction (Smith et al. 2003) + OFI price impact
import random

def zi_book(seed=11, N=100000, p_lim=0.25, p_mkt=0.45, cancel_mean=8.0,
            offset_mean=2.5, lim_mean=5.0, mkt_mean=5.0, tick=0.01, seed_sz=10):
    """Zero-intelligence CDA: random limit/market/cancel arrivals on a $0.01 grid."""
    random.seed(seed)
    bids, asks = {}, {}
    def put(d, p, s): d[p] = d.get(p, 0) + s
    def top(d, side): return (max(d) if side == 'B' else min(d)) if d else None
    for k in range(1, 3):
        put(bids, round(100.00 - k * tick, 2), seed_sz)
        put(asks, round(100.00 + k * tick, 2), seed_sz)
    def market(side, size):                       # side='B' lifts asks, 'A' hits bids
        book = asks if side == 'B' else bids
        while size > 0 and book:
            p = top(book, 'A' if side == 'A' else 'B')
            t = min(size, book[p]); book[p] -= t; size -= t
            if book[p] == 0: del book[p]
    snap, ref = [], 100.00
    for _ in range(N):
        r = random.random(); bb = top(bids, 'B'); ba = top(asks, 'A')
        if r < p_lim:                                                    # limit order
            side = random.choice('BA'); off = 1 + int(random.expovariate(1 / offset_mean))
            sz = 1 + int(random.expovariate(1 / lim_mean))
            if side == 'B':
                p = round((bb if bb is not None else (ba - tick if ba is not None else ref)) - off * tick, 2)
                market('B', sz) if (ba is not None and p >= ba) else put(bids, p, sz)
            else:
                p = round((ba if ba is not None else (bb + tick if bb is not None else ref)) + off * tick, 2)
                market('A', sz) if (bb is not None and p <= bb) else put(asks, p, sz)
        elif r < p_lim + p_mkt:                                          # market order
            market(random.choice('BA'), 1 + int(random.expovariate(1 / mkt_mean)))
        else:                                                            # cancellation
            book = bids if random.random() < 0.5 else asks
            if book:
                p = random.choice(list(book)); book[p] -= 1 + int(random.expovariate(1 / cancel_mean))
                if book[p] <= 0: del book[p]
        bb1, ba1 = top(bids, 'B'), top(asks, 'A')
        if bb1 is not None and ba1 is not None:
            snap.append((bb1, bids[bb1], ba1, asks[ba1])); ref = (bb1 + ba1) / 2
    return snap

def ofi_regression(snap, bucket=500):
    """Regress d(mid) on Order Flow Imbalance (Cont, Kukanov & Stoikov 2014) per bucket."""
    X, Y = [], []
    for i in range(bucket, len(snap), bucket):
        o = 0
        m0 = (snap[i - bucket][0] + snap[i - bucket][2]) / 2
        m1 = (snap[i][0] + snap[i][2]) / 2
        for j in range(i - bucket + 1, i + 1):
            bb0, bs0, ba0, as0 = snap[j - 1]
            bb1, bs1, ba1, as1 = snap[j]
            Ib = bs1 if bb1 > bb0 else (bs1 - bs0 if bb1 == bb0 else -bs0)
            Ia = -as1 if ba1 > ba0 else (as1 - as0 if ba1 == ba0 else as0)
            o += Ib - Ia
        X.append(o); Y.append(m1 - m0)
    n = len(X); mx, my = sum(X) / n, sum(Y) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(X, Y))
    sxx = sum((x - mx) ** 2 for x in X); syy = sum((y - my) ** 2 for y in Y)
    return sxy / sxx, sxy * sxy / (sxx * syy), len(X)

sp = zi_book(seed_sz=10)
spreads = [ba - bb for bb, _, ba, _ in sp]
depths = [bs + as_ for _, bs, _, as_ in sp]
print(f"events kept        = {len(sp)}")
print(f"mean spread        = {sum(spreads)/len(spreads):.4f}   (positive spread from random arrival alone)")
print(f"mean best depth    = {sum(depths)/len(depths):.1f} lots")

b1, r1, k1 = ofi_regression(sp)
print(f"\nshallow book:  beta = {b1:.4e}   R^2 = {r1:.4f}   buckets = {k1}")
b2, r2, k2 = ofi_regression(zi_book(seed_sz=300))
print(f"deep book:     beta = {b2:.4e}   R^2 = {r2:.4f}   buckets = {k2}")
```
```
events kept        = 23051
mean spread        = 0.0428   (positive spread from random arrival alone)
mean best depth    = 11.5 lots

shallow book:  beta = 2.2594e-03   R^2 = 0.6231   buckets = 46
deep book:     beta = 1.6781e-03   R^2 = 0.3795   buckets = 46
```
Two results, both load-bearing. **First:** a book assembled entirely from coin flips sustains a **positive spread of ~4 ticks** and a stable depth (~11.5 lots) — so depth and spread are *mechanical*, not evidence of strategy. **Second:** even here, $\Delta m$ is linearly explained by OFI with $R^2\approx0.62$, and the slope **falls from $2.26\times10^{-3}$ to $1.68\times10^{-3}$ when the book is deepened** — the inverse-depth relation of §2.2 recovered from a synthetic book. Real markets sharpen this fit to near-perfect (Cont et al.), because informed and correlated flow adds *signal* on top of the mechanical baseline; zero-intelligence has only the baseline.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The null model is not the model.** ZI reproduces the *spread* and a rough OFI slope, but it cannot price *information*: it has no informed traders, so it cannot generate the permanent impact or the toxicity that dominate real market-maker P&L. Using ZI dynamics as a trading model confuses a mechanical baseline for a forecast.
2. **Markov assumption vs long memory.** The queueing models assume the state is Markov in the queue sizes. Real order flow is self-exciting (Hawkes) with long-memory clustering, so intensities estimated in one regime under-predict activity in the next. The branching ratio $n$ approaching 1 is a warning, not a constant.
3. **OFI is not stationary under manipulation.** The OFI impact law is stable *on average* but is a function of the *book* — and the book is gameable. Spoofing layers inflate "depth", suppressing measured $\beta$; cancellation bursts in the moment of impact distort the OFI input. The law holds cleanly only on executed, non-spoofed flow.
4. **Parameters drift faster than you can calibrate.** Deposit/cancel/impact rates shift with volatility regime, tick size, and venue rules. A queue-reactive or OFI model calibrated on a calm month is *mis-specified*, not merely stale, in a crisis — the exact failure of the Avellaneda–Stoikov family too ([[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|The Avellaneda–Stoikov Model]]).
5. **Grid/discretisation artefacts.** Every result above lives on a tick grid $\delta\mathbb{Z}$. Tick-size changes, sub-penny venues, and hidden liquidity break the "one queue per price" abstraction, and the book becomes a *hidden* queueing system that no model in this page observes directly.

---

### 5. Canonical Literature & Study References

- **Cont, Stoikov & Talreja (2010)**, *A stochastic model for order book dynamics*, Operations Research 58(3), 549–563 — the Markovian queue model of §2.1.
- **Cont, Kukanov & Stoikov (2014)**, *The price impact of order book events*, Journal of Financial Econometrics 12(1), 47–88 — OFI, the linear price-impact law, inverse-depth slope (§2.2).
- **Smith, Farmer, Gillemot & Krishnamurthy (2003)**, *Statistical theory of the continuous double auction*, Quantitative Finance 3(6), 481–514 — the zero-intelligence baseline simulated in §3.
- **Huang, Lehalle & Rosenbaum (2015)**, *Simulating and analysing the queue-reactive model*, Journal of Statistical Mechanics — touch-queue mean reversion and short-horizon move probabilities (§2.3).
- **Bouchaud, Mézard & Potters (2002)**, *Statistical properties of stock order books*, Quantitative Finance 2(4), 251–256 — empirical book shape and deposit/withdrawal rates.
- **Bouchaud, Farmer & Lillo (2009)**, *How markets slowly digest changes in supply and demand* — order-flow clustering, impact, and the Hawkes view (§2.4).
- **Rosu (2009)**, *A dynamic model of the limit order book*, Review of Financial Studies 22(11) — general-equilibrium spread and depth dynamics.
- **Gould, Porter, Williams, McDonald, Fenn & Howison (2013)**, *Limit order books*, Quantitative Finance 13(11) — the review hub for the whole folder.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/limit-order-book-mechanics/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Index Hub]]
- Forward topic-folder pages: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|The Avellaneda–Stoikov Model]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
- Related data page: [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics & L3 Data]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]
- Base: [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
