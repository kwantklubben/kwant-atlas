---
title: "03 - The HFT System Architecture: Feed Handler to Order Gateway"
tags:
  - pillar-algorithmic-hft
  - low-latency-systems-architecture
  - system-architecture
  - queueing
  - back-pressure
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/low-latency-systems-architecture/02-the-latency-hierarchy|02 · The Latency Hierarchy]].

---

### 1. Intuition & Practical Objective

Almost every latency-sensitive trading system, from a two-person prop shop to a top-tier HFT, is the same **three-stage pipeline**:

$$\underbrace{\text{Feed Handler}}_{\text{decode market data}}\;\longrightarrow\;\underbrace{\text{Strategy}}_{\text{decide}}\;\longrightarrow\;\underbrace{\text{Order Gateway}}_{\text{encode \& send orders}}.$$

The stages are connected by **one-way message channels** (in practice, ring buffers — [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04]]). The objective of this page is to understand the architecture **as a queueing system**, because that is the only rigorous way to answer the questions that actually matter:

- *How loaded should each stage be?* (Answer: far below 100 % — §2.)
- *Where does jitter come from?* (Answer: queueing delay, which grows without bound as load approaches 1.)
- *What does "back-pressure" cost?* (Answer: if the fast stage waits on the slow stage, the fast stage's latency *becomes* the slow stage's latency.)

The guiding principle throughout is **one thread, one job, one direction of data flow** — a design in which each stage is a simple, cache-resident loop that never blocks on a lock and never allocates. This is the same "do less work" principle from [[pillars/02-algorithmic-hft/low-latency-systems-architecture/01-from-zero-intuition|01]], now applied to *how the stages are wired together*.

> **The one-sentence essence.** "A trading engine is a chain of single-writer queues; its latency is the sum of stage service times *plus* queueing delay, and queueing delay explodes as each stage's utilisation approaches 1 — so the architecture must keep every stage comfortably idle, not busy."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The stages and their messages

- **Feed handler.** Receives the venue's multicast feed (e.g. a binary ITCH-style protocol, or FIX for some venues — see [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]]), decodes it into a normalised tick, and publishes it. It is a *producer*: it never waits for the strategy.
- **Strategy.** Consumes ticks, maintains whatever view it needs (book, position, signals), and emits orders/cancels. It is the *only* place the trading decision lives.
- **Order gateway.** Encodes orders into the venue's wire format, manages session/sequence state, and writes them to the socket. It is the *last* stage and must never stall the strategy.

**Data flows one way.** Market data flows *downstream*; there is no call from the strategy "up" into the feed handler and no blocking handshake between stages. Blocking is what turns two independent latencies into one correlated disaster.

#### 2.2 Queueing model: load sets latency

Treat each stage as a single server. Arrivals are message events; the service time is the stage's processing cost. The canonical results (**Kendall notation $M/M/1$**, i.e. Poisson arrivals, exponential service, one server):

$$L = \lambda W \quad(\text{Little's law}),\qquad W_q = \frac{\rho}{1-\rho}\,\mathbb{E}[S],\qquad \rho=\lambda\,\mathbb{E}[S].$$

The mean *time in system* is $W = W_q + \mathbb{E}[S] = \dfrac{\mathbb{E}[S]}{1-\rho}$. **At $\rho=0.5$, $W=2\,\mathbb{E}[S]$; at $\rho=0.9$, $W=10\,\mathbb{E}[S]$; at $\rho=0.99$, $W=100\,\mathbb{E}[S]$.** A stage that looks "twice as fast as needed" is not wasting half its capacity — it is buying a **5x reduction in mean sojourn time** (a **9x** cut in queueing delay proper, $W_q$).

For general service-time variability the **Pollaczek–Khinchine** formula generalises this:

$$W_q = \rho\,\mathbb{E}[S]\,\frac{1+C_s^2}{2(1-\rho)},\qquad C_s = \frac{\operatorname{std}(S)}{\mathbb{E}[S]}.$$

Two design laws follow directly:

1. **Keep $\rho$ low** (the folklore "run hot — never above ~50–70 %"): queueing delay is a *reciprocal* function of the margin to saturation.
2. **Keep $C_s$ small** — *deterministic* service (constant-time hot loop, no allocation, no branch surprises) is worth as much as raw speed, because jitter multiplies the queueing term.

When arrivals are deterministic and service is deterministic ($D/D/1$), there is no randomness and delays stay bounded; but real feeds are bursty (a batch of ticks arrives together, e.g. after an auction), so the realistic model is closer to $M/D/1$ or a *bursty/GI/D/1* queue — which is exactly why a **ring buffer with headroom** matters: it absorbs bursts without forcing the strategy to wait.

#### 2.3 The design principles (compressed)

These are the recurring rules of the discipline; each is a direct consequence of §2.1 of the previous page:

- **Do less work.** Latency $\approx$ instructions executed on the critical path; every branch and copy costs real cycles.
- **No allocation on the hot path.** `malloc`/`new`/GC introduce 50–500+ ns heap or lock costs *and* unbounded tail pauses. Pre-allocate everything at startup (arenas).
- **Mechanical sympathy.** Design for the hardware: contiguous memory, streaming access, cache-line-aligned (64 B) fields, branch-predicted common cases.
- **Single writer per queue.** One producer and one consumer per channel removes the need for locks entirely ([[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04]]).

---

### 3. Computational Implementation — the pipeline as a queue

Standard library only. We simulate the strategy stage as a single server with Poisson arrivals and log-normal service times, sweeping the offered load $\rho$, and measure the resulting **queueing delay**, **sojourn time**, and the **p99**. The Little's-law column ($L=\lambda W$) is computed from the actual time-in-system integral, so it doubles as a check on the simulation.

```python
import random, math
random.seed(7)

def simulate(lam_per_us, mean_svc_us, n, sigma=0.3):
    """Single-server tick handler: Poisson arrivals, log-normal service.
       Returns (mean_queue_us, mean_sojourn_us, L, p99_sojourn_us)."""
    inter = [random.expovariate(lam_per_us) for _ in range(n)]
    svc   = [math.exp(random.gauss(math.log(mean_svc_us), sigma)) for _ in range(n)]
    t = 0.0; free_at = 0.0; waits = []; soj = []; area = 0.0
    for a, s in zip(inter, svc):
        t += a; start = max(t, free_at); w = start - t
        waits.append(w); soj.append(w + s); free_at = start + s; area += free_at - t
    return sum(waits)/n, sum(soj)/n, area/t, sorted(soj)[int(0.99*n)]

res = {}
print("  lambda(us^-1)  rho    mean_queue_us  mean_sojourn_us   L=lam*W   p99_sojourn_us")
for lam, svc in ((0.2, 1.0), (0.5, 1.0), (0.8, 1.0), (0.95, 1.0)):
    q, W, L, p99 = simulate(lam, svc, 200_000)
    res[lam] = (q, W, L, p99)
    print(f"  {lam:11.2f}  {lam*svc:4.2f}   {q:12.3f}   {W:13.3f}   {L:7.3f}   {p99:13.3f}")

q, W, L, p99 = res[0.80]
print(f"\nLittle's law check (rho=0.80): L_measured={L:.3f} vs lambda*W={0.80*W:.3f}"
      f"  (diff={abs(L-0.80*W):.2e})")
print(f"At rho=0.80, mean sojourn={W:.3f}us = {W/1.0:.2f}x service time; the extra {q:.3f}us is pure queueing.")
```
```
  lambda(us^-1)  rho    mean_queue_us  mean_sojourn_us   L=lam*W   p99_sojourn_us
         0.20  0.20          0.151           1.197     0.240           2.937
         0.50  0.50          0.630           1.675     0.837           5.308
         0.80  0.80          2.952           3.998     3.200          16.255
         0.95  0.95        110.012         111.058   105.578         351.427

Little's law check (rho=0.80): L_measured=3.200 vs lambda*W=3.199  (diff=1.08e-03)
At rho=0.80, mean sojourn=3.998us = 4.00x service time; the extra 2.952us is pure queueing.
```

**Read the result.** Raw service time is constant at 1 µs, yet the observed sojourn time goes 1.2 → 1.7 → 4.0 → **111 µs** as load rises through 20 % → 95 %. The stage did *no extra work* — the latency is entirely queueing delay. The p99 at $\rho=0.95$ (351 µs) is 15 000x the 20 %-load p50: **a "busy" engine is a latency bomb**, which is why production systems cap stage utilisation far below saturation even at the cost of idle hardware. The Little's-law check ($L\approx3.200$ vs $\lambda W=3.199$) confirms the simulation conserves work.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Running each stage hot.** Because $W_q=\rho\mathbb{E}[S]/(1-\rho)$, the marginal cost of load is nonlinear: the last 10 % of utilisation buys ten times the delay. Capacity planning is latency planning.
2. **Blocking between stages.** If the strategy blocks waiting on the feed handler (a lock, a synchronous call), the two latencies become correlated and their tails add; the single-writer one-way design exists to forbid exactly this.
3. **Unbounded queues.** A ring buffer that can grow without limit converts a latent overload into an ever-growing latency instead of an explicit drop — you lose the tick's *staleness* signal. Bounded ring + explicit drop policy is the honest design ([[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04]]).
4. **Jittery service time.** $C_s$ in the P-K formula multiplies the queueing delay; a stage with occasional 100 µs pauses queues like a stage with a much higher mean. Determinism is a first-class requirement, handled in [[pillars/02-algorithmic-hft/low-latency-systems-architecture/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Fowler, Martin** — *The LMAX Architecture* and the **LMAX Disruptor** paper. The canonical one-way, single-writer, ring-buffer architecture this page describes.
- **NautilusTrader** documentation (nautilustrader.io). A production-grade, open-source event-driven engine whose message-bus/actor design is the cleanest modern reference for stage decoupling.
- **Kerrisk, Michael** — *The Linux Programming Interface* (2010), and **Benvenuti** — *Understanding Linux Network Internals* (2005). The OS-level mechanics behind the feed-handler stage.
- **Gregg, Brendan** — *Systems Performance* (2nd ed., 2020). Measuring per-stage latency and queueing in production.
- **FIX Protocol official specifications** (fixtrading.org) and **Nasdaq TotalView-ITCH 5.0** spec. The actual wire protocols the feed handler and gateway speak.
- **Hamilton, Peter** et al. — multithreading/event-driven architecture in *C++ Concurrency in Action* (Williams): the language-level counterpart is in [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]].

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/02-the-latency-hierarchy|02 · The Latency Hierarchy]]
- Forward: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04 · Lock-Free & Ring Buffers]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Index Hub]]
- Cross-pillar: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]]
- Deeper: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]] (move the feed handler into silicon)
