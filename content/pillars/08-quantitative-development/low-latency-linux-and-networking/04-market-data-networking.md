---
title: "8.4.4 Market-Data Networking"
tags:
  - pillar-quant-dev
  - low-latency-linux
  - market-data
  - multicast
  - udp
  - tcp
  - packet-timing
  - sequence-gap
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/low-latency-linux-and-networking/03-kernel-bypass-and-nics|03 · Kernel Bypass & NICs]] and [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]] (the wire formats this transport carries).

---

### 1. Intuition & Practical Objective

Market data arrives on a **multicast UDP** fabric (e.g. the ITCH binary feeds of §1) or point-to-point **TCP** (FIX sessions). The objective is to choose the right transport *and* to detect, in real time, when the fabric is degrading - because **a missed or late packet is a missed trade, and multicast gives you no retransmission for free.**

Two transports, two philosophies:

1. **TCP** - reliable, ordered, connection-oriented, but it adds retransmission, delayed-ACK/Nagle latency, and head-of-line blocking. Fine for order messages (FIX) where correctness beats speed; wrong for high-rate market data where a single lost packet would stall the whole book.
2. **UDP / multicast** - connectionless, no reliability, no ordering guarantee - but *that is the point*: it is the fastest way to broadcast a feed to many consumers. Exchanges ship market data as multicast UDP; the *consumer* is responsible for sequence-gap detection and gap-recovery (replay/backfill), not the network.

The core of this page is **packet timing**: measuring inter-arrival times (IAT), spotting jitter events, and detecting *sequence gaps* (lost packets). If a feed's IAT is nominally ~10 µs but occasionally 100 µs, or if sequence numbers jump, your book builder is working with stale or missing data - and you must know *before* the stale data trades.

> **One-sentence essence.** "Market data rides multicast UDP because it is the fastest broadcast there is - but reliability moves from the network to you, so the consumer's job is to *watch the clock and the sequence numbers*: IAT jitter tells you the fabric is degrading, and a sequence gap tells you data was lost and must be re-requested."

---

### 2. Mathematical Ground Truth & Derivations

**Nominal vs actual inter-arrival time.** For a feed at rate $\lambda$ messages/s, the nominal mean IAT is $1/\lambda$ (10 µs at 100k msg/s). Real feeds are bursty: within a batch of quotes, gaps shrink to ~1 µs; between batches they grow. **Jitter** is the deviation of actual IAT from the nominal - it is what you measure, and it is the early-warning signal of congestion, NIC coalescing, or a saturated receive core.

**Sequence-gap detection.** Each feed message carries a monotonically increasing sequence number $s_i$. If the last received was $s_{i-1}$ and the next is $s_i$ with

$$
s_i - s_{i-1} > 1 \;\Rightarrow\; \text{lost } (s_i-s_{i-1}-1)\ \text{messages}.
$$

A single dropped packet opens a *hole* in the book - that instrument's last-known price is now stale by one or more ticks, and the risk is that your strategy trades on the stale value. The recovery action (replay/backfill from the venue) is the topic of [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]]; *detecting* the hole is this page's job.

**Why you monitor IAT, not just counts.** A feed can carry the correct total message count while still being degraded: retransmission-free UDP has no ordering, so a *burst* of stale-then-caught-up data can look "fine" on a daily total. IAT percentiles expose the microsecond-scale stalls that totals hide.

---

### 3. Computational Implementation - multicast IAT jitter & sequence-gap detection

Simulates a ~100k msg/s multicast feed with bursty inter-arrival times, then (a) reports the IAT distribution (the jitter signal) and (b) detects three dropped messages by sequence-gap analysis. Stdlib only.




The IAT report is the health monitor: the *mean* (3.59 µs) is comfortably under the 10 µs nominal, but the **p99 IAT is 31.5 µs and ~2% of messages sit >25 µs apart** - those are the stalls a book-builder (and a strategy) would feel as stale quotes. And on the loss side: sequence-gap detection catches every one of the 3 dropped messages with zero false positives - the cheap, essential correctness guard on any multicast consumer.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **A gap you do not see is a stale trade.** Multicast has no retransmission; a lost packet is gone unless you detect it and re-request. Without sequence-gap monitoring, a 1-in-1000 drop silently staleness a quote and you trade on it.
2. **IAT jitter masquerading as "fine".** Burstiness and rare long gaps hide under a healthy mean. Monitor IAT *percentiles*, not averages - the mean is the feed's advertisement, the p99 is its actual health.
3. **TCP head-of-line blocking.** Putting high-rate market data over TCP means one retransmission stalls every message behind it. Know *why* multicast is used and do not "simplify" it back to TCP.
4. **Coalescing corrupts the timing signal.** NIC interrupt coalescing batches packets, adding fixed first-packet delay that reads as IAT jitter. When tuning the receive path, separate *true* fabric jitter from *local* coalescing artefacts (measure at the same point you intend to optimise).

---

### 5. Canonical Literature & Study References

- **Stevens, W. Richard (Fall, Kevin)** - *TCP/IP Illustrated, Vol. 1*, 2nd ed.: UDP/multicast semantics and why there is no delivery guarantee.
- **Nasdaq TotalView-ITCH 5.0 Specification** - the canonical multicast binary feed spec (also covers FPGA variants); the sequence-number scheme this page's gap detection reads.
- **Databento** - *Low-Latency Tuning Guide for Linux and Trading Systems*: multicast receive tuning on Linux.
- **FIX Protocol (fixtrading.org)** - FIX Latest/4.4 and FIXatdl: the point-to-point TCP counterpart on the order side.
- **Benvenuti, Christian** - *Understanding Linux Network Internals*: how the kernel receives/batches multicast UDP.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/low-latency-linux-and-networking/03-kernel-bypass-and-nics|03 · Kernel Bypass & NICs]]
- Forward: [[pillars/08-quantitative-development/low-latency-linux-and-networking/05-failure-modes-and-practice|05 · Failure Modes]] (data-quality failures)
- Wire formats: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]] (ITCH FPGA decoding)
- Clock plane (why timestamps on this feed must agree): [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Synchronization]]
