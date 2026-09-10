---
title: "03 - Kernel Bypass & NICs: DPDK, Solarflare/Onload, Interrupts vs Polling"
tags:
  - pillar-quant-dev
  - low-latency-linux
  - kernel-bypass
  - dpdk
  - solarflare
  - onload
  - nic-tuning
  - busy-polling
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/low-latency-linux-and-networking/02-kernel-tuning-for-latency|02 · Kernel Tuning]] (isolation) and [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass (FPGA folder)]] — which this page extends with the *NIC-tuning and cost-model* details rather than duplicating.

---

### 1. Intuition & Practical Objective

Before any FPGA, there is a **~20× free speedup** sitting in the network stack. The Linux receive path raises an interrupt on packet arrival, context-switches into the kernel, copies the packet into kernel memory, runs the protocol layers, copies it again to user space, and wakes your thread — **~10–25 µs** and multi-µs of jitter. Almost all of it is overhead you do not need, and almost all of it is *unpredictable* (interrupt-driven).

**Kernel bypass** maps the NIC's DMA ring directly into your process's address space; a dedicated core **busy-polls** the ring (never sleeping, never interrupted, never yielding). No syscalls, no copies, no scheduler, no interrupts. Latency drops from ~10–25 µs to ~1.2 µs *and* the jitter collapses. The two mainstream routes: **DPDK** (fully userspace, owns the NIC) and **Solarflare/OpenOnload + EF_VI** (a transparent library that bypasses the kernel for the socket while the NIC still lives on the host).

The NIC is a stage you **configure**, not just read. **RSS** (receive-side scaling) splits packets across multiple queues so multiple cores can drain them in parallel; **flow-director / RFS** steers flows to the queue whose polling core owns that flow; **IRQ affinity** pins each queue's interrupts to a core. The objective: **every packet lands on the queue that its polling core owns, on the same NUMA node as that core, with no cross-socket bounce.**

> **One-sentence essence.** "Kernel bypass is the cheapest microsecond in the stack — it deletes the interrupt, the copies, and the scheduler from the hot path, dropping RX from ~10–25 µs to ~1.2 µs with near-zero jitter — and the NIC tuning (RSS/flow-director/IRQ affinity/NUMA) decides whether packets actually reach that polling core in one hop."

---

### 2. Mathematical Ground Truth & Derivations

**Per-core capacity.** A core at frequency $f$ (≈3 GHz) spends $c$ *cycles* per packet:

$$\Theta_{\text{core}}=\frac{f}{c}\ \text{pkt/s}.$$

Kernel path $c\approx2600$ cycles (≈870 ns) ⇒ ~1.15 M pkt/s; bypass $c\approx160$ cycles (≈53 ns) ⇒ ~18.75 M pkt/s. Sustaining 10GbE line rate (14.88 M pkt/s, 84 B min frames) needs

$$n_{\text{cores}}=\frac{R}{\Theta_{\text{core}}} = \frac{14.88\times10^6}{f/c}.$$

That is **~12.9 cores on the kernel path vs ~0.79 of one core bypassed** — the whole business case in one division. (A misconfigured bypass — polling core on the wrong NUMA node, $c\approx380$ cycles — still needs ~1.9 cores; NUMA matters even bypassed.)

**Why busy-polling is stable and interrupts are not.** With interrupts, processing cost grows with rate and the system has a positive-feedback failure mode (interrupt *livelock*): higher rate ⇒ more interrupts ⇒ less real work ⇒ queues grow (Little's law) ⇒ more delay. Busy-polling makes cost **constant per packet**, so latency stays flat until the core saturates — a hard ceiling instead of a soft cliff. The §3 model shows the jitter gap directly: interrupt-driven p99 ~33 µs, busy-poll p99 ~1.6 µs.

**Interrupt coalescing is a jitter tax.** Coalescing (waiting to batch interrupts) raises throughput but adds a *fixed* delay to the first packet of a batch — pure added latency and variance on a latency-sensitive path. When you need per-packet determinism, coalescing is the enemy; you turn it off or bypass interrupts entirely.

---

### 3. Computational Implementation — the bypass cost model & interrupt-vs-poll latency

Two models, one script: (a) the cores-required arithmetic at 10GbE line rate, and (b) the latency distribution of interrupt-driven vs busy-polled RX. Stdlib only.

```python
import random, math
def pct(xs, p):
    xs = sorted(xs); return xs[int(round(p/100.0*(len(xs)-1)))]
f = 3.0e9                    # core frequency, Hz
R = 14.88e6                  # 10GbE line rate, min-frame pkt/s
print(f"10GbE line rate {R/1e6:.2f} M pkt/s (84 B min frame)\n")
for tag, c in (("kernel stack", 2600.0), ("bypass/busy-poll", 160.0),
               ("bypass+NUMA-bounce", 380.0)):
    cap = f / c
    print(f"{tag:20s} per-core cap {cap/1e6:6.2f} M pkt/s ; "
          f"cores for line rate = {R/cap:5.2f}")
print("\nRSS on bypass cores (18.75 M pkt/s each):")
for Q in (1, 2, 4):
    per_q = R / Q
    print(f"  {Q} queues -> {per_q/1e6:5.2f} M pkt/s/queue -> "
          f"{per_q/(f/160.0):4.2f} cores/queue, total {per_q/(f/160.0)*Q:4.2f}")

print("\nInterrupt-driven vs busy-poll RX latency (us):")
random.seed(3)
def dist(mode, n=150000):
    xs = []
    for _ in range(n):
        if mode == "irq":
            x = math.exp(random.gauss(math.log(8), 0.5))
            if random.random() < 0.01:
                x += math.exp(random.gauss(math.log(40), 0.6))   # rare interrupt storm
        else:
            x = math.exp(random.gauss(math.log(1.2), 0.12))      # flat busy-poll
        xs.append(x)
    return xs
for mode in ("irq", "poll"):
    xs = dist(mode)
    print(f"{mode:5s} latency: p50={pct(xs,50):5.2f} p99={pct(xs,99):6.2f} "
          f"p99.9={pct(xs,99.9):7.2f} max={max(xs):7.1f} us")
```
```
10GbE line rate 14.88 M pkt/s (84 B min frame)

kernel stack         per-core cap   1.15 M pkt/s ; cores for line rate = 12.90
bypass/busy-poll     per-core cap  18.75 M pkt/s ; cores for line rate =  0.79
bypass+NUMA-bounce   per-core cap   7.89 M pkt/s ; cores for line rate =  1.88

RSS on bypass cores (18.75 M pkt/s each):
  1 queues -> 14.88 M pkt/s/queue -> 0.79 cores/queue, total 0.79
  2 queues ->  7.44 M pkt/s/queue -> 0.40 cores/queue, total 0.79
  4 queues ->  3.72 M pkt/s/queue -> 0.20 cores/queue, total 0.79

Interrupt-driven vs busy-poll RX latency (us):
irq   latency: p50= 8.03 p99= 33.32 p99.9=  98.10 max=  348.5 us
poll  latency: p50= 1.20 p99=  1.58 p99.9=   1.73 max=    2.1 us
```

Two concrete reads. **(1)** Bypass turns a 13-core networking problem into a fraction of one core — and RSS lets you parallelise further *without* adding cores (total stays ~0.79 across 1–4 queues). **(2)** Beyond the 6.7× mean drop (8.03 → 1.20 µs), the **jitter collapses harder than the mean**: p99.9 drops from 98.1 to 1.7 µs (58×), max from 348 to 2.1 µs. Interrupt-driven RX is fast on average and *catastrophic in the tail*; busy-polling is fast *and* flat.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Interrupt livelock.** With interrupts, throughput demand can overwhelm the core: more interrupts ⇒ less real work ⇒ queues grow ⇒ delay. Busy-poll removes the positive feedback, but only if you actually poll — a half-configured bypass that still raises interrupts gets the worst of both.
2. **NUMA-crossed bypass.** Polling core pinned to socket 0, NIC RX ring on socket 1 ⇒ every polled packet crosses the interconnect (~40–80 ns + contention). "Bypassed" but still slow. (Verified: bypass+NUMA-bounce needs 1.88 cores vs 0.79 clean.)
3. **Misrouted flows (RSS/flow-director drift).** Flow-director rules steer a flow to the wrong queue, so packets land on a core that is *not* the one draining them — they queue up or bounce. Config drift here is silent: mean flat, p99 up.
4. **Interrupt coalescing left on.** If you are not bypassing, coalescing adds fixed batch latency to the first packet — a jitter tax on the exact percentile that decides races. Turn it off when determinism matters.

---

### 5. Canonical Literature & Study References

- **DPDK documentation** (dpdk.org) — the definitive kernel-bypass receive-path reference.
- **Solarflare OpenOnload & EF_VI documentation** — the transparent-bypass alternative; the second mainstream route.
- **Databento** — *Low-Latency Tuning Guide for Linux and Trading Systems*: RSS/RFS, IRQ affinity, busy-polling, NUMA-local, written for trading.
- **Benvenuti, Christian** — *Understanding Linux Network Internals*: NAPI/softirq/interrupt path the bypass replaces (why bypass works).
- **Rosen, Rami** — *Linux Kernel Networking*: the modern-stack sibling.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/low-latency-linux-and-networking/02-kernel-tuning-for-latency|02 · Kernel Tuning]]
- Forward: [[pillars/08-quantitative-development/low-latency-linux-and-networking/04-market-data-networking|04 · Market-Data Networking]] (multicast/UDP on top of this path)
- Silicon endpoint (do not duplicate): [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass (FPGA folder)]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]]
- Systems frame: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]
