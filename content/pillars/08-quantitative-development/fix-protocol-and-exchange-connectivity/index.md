---
title: "FIX Protocol & Exchange Connectivity: Topic Hub & Message Lookup"
tags:
  - pillar-quant-dev
  - fix-protocol
  - exchange-connectivity
  - order-routing
  - sessions
  - index-hub
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]] (TCP sockets, kernel bypass) and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]] (what an order *is* at the venue). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

An exchange is a **conversation partner**, not a database you query. You do not "submit" an order; you send a *message*, wait for the venue to acknowledge it, and then live with a shared state that both sides must keep in sync over an inherently unreliable wire. **FIX** — the *Financial Information eXchange* protocol — is the standard language for that conversation: a text, `tag=value` messaging format with its own **session layer** (logon, heartbeats, sequence numbers, resend) sitting *on top of* TCP.

The practical objective of this folder is to make you fluent in three layers at once: the **message** (what goes on the wire), the **session** (how two engines agree on what has been sent and received), and the **order lifecycle** (how a single order's state evolves so that your book and the exchange's book never disagree). This folder is a *hub*: it gives you the **fast message-tag lookup** below (job #1 of this pillar) and routes you to six sub-pages that walk from raw intuition to binary venue feeds.

> **The one-sentence essence.** "FIX is a *sequenced, recoverable conversation*: every message carries a tag-value payload and a monotone sequence number, and correctness means that after any drop, replay, or failover, **both sides reconstruct the identical order state from the same message stream**."

**The three laws of connectivity** (each a first principle, not a convention):

1. **Ordering is guaranteed by sequence numbers, not by TCP** — TCP gives you an ordered *byte* stream, but applications restart, and a byte stream has no memory of what your engine did before it crashed. Tags `34` (MsgSeqNum) give *application-level* order and recovery.
2. **State is shared and must converge** — your order book is a *replica* of the venue's; every `ExecutionReport` (`35=8`) is a state transition, and a lost one leaves you desynced until you resend.
3. **Reliability is expensive; exotic protocols trade it for speed** — binary feeds (ITCH/OUCH) drop the text framing and the rich session semantics to shave bytes and nanoseconds; you pay for that speed in recovery complexity.

---

### 2. Mathematical Ground Truth & Lookups

**Quick-reference lookup (job #1).** Every number below is reproduced by a verified script in §3 or a sub-page.

**Notation:** $R$ arrival rate (msg/s), $s$ message size (bytes), $C$ link capacity (bit/s), $\bar t$ round-trip latency, $B$ backlog (messages).

**Message rate and bandwidth.** A session's required bandwidth is the message rate times the message size:

$$
B_{\text{wire}} = 8\,R\,s \quad\text{(bit/s)},\qquad \text{link utilisation} = \frac{8Rs}{C}.
$$

For $R = 20{,}000$ msg/s at $s = 165$ B on a 1 Gbps link this is $26.4$ Mbit/s — only $2.64\%$ of the link, so **latency, not bandwidth, is the binding constraint.**

**Journal (resend-log) growth.** Every outbound message must be persisted for replay, so the log grows at

$$
\dot{S} = R\,s = \frac{B_{\text{wire}}}{8} \quad\text{(byte/s)}.
$$

**Sequence-number invariant.** Let $N_{\text{in}}$ be the next inbound sequence number expected. On receipt of message with `MsgSeqNum = M`:

$$
\text{action} =
\begin{cases}
\text{accept},\ N_{\text{in}} \leftarrow M+1 & M = N_{\text{in}},\\[2pt]
\text{ResendRequest}(N_{\text{in}}.\,,M-1) & M > N_{\text{in}}\ \ (\text{gap of } M-N_{\text{in}}),\\[2pt]
\text{discard (already seen)} & M < N_{\text{in}}.
\end{cases}
$$

The gap size is exactly $g = M - N_{\text{in}}$, and the request covers the half-open-closed range $[\,N_{\text{in}},\,M-1\,]$.

**Replay drain time.** A backlog $B$ replayed at rate $r$ clears in $B/r$: a 30 s outage at 20,000 msg/s leaves $B = 600{,}000$ messages, which at $10^6$ msg/s drains in $600$ ms.

**Little's law for the session.** Messages in flight $= R\,\bar t$; a single in-order session needs a window $\ge 1$, and $\bar t = 250\,\mu$s at 20,000 msg/s puts only $5$ messages in flight — FIX is a *conversation*, not a pipeline.

**FIX message anatomy.** A FIX message is a strictly ordered triplet: **header** → **body** → **trailer**, with `8` (BeginString) first, `9` (BodyLength) second, `35` (MsgType) in the header, and `10` (CheckSum) last. `BodyLength` counts the bytes between the `9`-field's SOH and the `10`-field's start; `CheckSum` is the byte sum modulo 256 rendered as three digits:

$$
\texttt{9} = \Big|\text{body}\Big|_{\text{bytes}},\qquad \texttt{10} = \Big(\sum_i b_i\Big) \bmod 256,\quad b_i \in [0,255].
$$

**Common message types (`35`) and key tags.**

| MsgType `35` | Message | Role |
|---|---|---|
| `0` | Heartbeat | session keep-alive |
| `1` | TestRequest | probe a silent peer |
| `2` | ResendRequest | request a sequence gap |
| `3` | Reject | session-level reject |
| `4` | SequenceReset | gap-fill / hard reset |
| `5` | Logout | graceful session end |
| `A` | Logon | session establish (HeartBtInt in `108`) |
| `D` | NewOrderSingle | submit an order |
| `F` | OrderCancelRequest | cancel an order |
| `G` | OrderCancelReplaceRequest | amend (cancel/replace) |
| `8` | ExecutionReport | order state transition (fill/ack/reject) |
| `V` | MarketDataRequest | subscribe to a quote stream |

| Tag | Name | Notes |
|---|---|---|
| `8` / `9` / `35` | BeginString / BodyLength / MsgType | header |
| `49` / `56` | SenderCompID / TargetCompID | who is talking |
| `34` / `52` | MsgSeqNum / SendingTime | sequence + timestamp |
| `43` | PossDupFlag | `Y` on a replayed message |
| `122` | OrigSendingTime | original send time of a resend |
| `11` / `37` | ClOrdID / OrderID | your id / venue id |
| `17` | ExecID | unique id per execution (dedup key) |
| `150` / `39` | ExecType / OrdStatus | transition type / resulting state |
| `38` / `32` / `31` | OrderQty / LastQty / LastPx | size and fill price |
| `151` / `14` / `6` | LeavesQty / CumQty / AvgPx | running state |
| `55` / `54` / `40` / `44` / `59` | Symbol / Side / OrdType / Price / TimeInForce | the order itself |
| `10` | CheckSum | trailer |

---

### 3. Computational Implementation — the order-flow budget

This hub ships one self-contained model that ties the folder together: a session's wire bandwidth, its resend-log growth, and its outage-replay time. Standard library only.

```python
# 00 - hub model: order-flow bandwidth budget + resend-log growth
orders_per_sec = 5_000
msg_bytes      = 165                  # a FIX NewOrderSingle/ExecutionReport
fills_per_order = 3                   # average ExecutionReports per order
msgs_per_sec   = orders_per_sec * (1 + fills_per_order)

wire_bps = msgs_per_sec * msg_bytes * 8
print(f"Order rate        : {orders_per_sec:,} orders/s")
print(f"Messages (incl. ER): {msgs_per_sec:,} msgs/s  ({msg_bytes} B each)")
print(f"Wire bandwidth    : {wire_bps/1e6:,.1f} Mbit/s")
print(f"  -> utilisation of a 1 Gbps link: {100*wire_bps/1e9:.2f}%")

# resend log: every outbound message must be journalled for replay
log_bytes_s = msgs_per_sec * msg_bytes
print(f"\nResend-log growth : {log_bytes_s/1e6:,.2f} MB/s"
      f"  = {log_bytes_s*3600/1e9:,.2f} GB/h"
      f"  = {log_bytes_s*3600*24/1e9:,.1f} GB/day")

# how long a 30 s disconnect takes to replay (single-threaded 1 M msg/s drain)
drain = 1_000_000
backlog = msgs_per_sec * 30
print(f"\n30 s outage backlog = {backlog:,} msgs; "
      f"replay at {drain:,} msg/s takes {backlog/drain*1000:,.1f} ms")

# Little's law: messages in flight = arrival rate x round-trip latency
rtt_us = 250.0
inflight = msgs_per_sec * rtt_us * 1e-6
print(f"\nLittle's law: in-flight msgs = {msgs_per_sec:,}/s x {rtt_us:.0f} us "
      f"= {inflight:.3f} -> a single in-order session must have a window >= 1")
```
```
Order rate        : 5,000 orders/s
Messages (incl. ER): 20,000 msgs/s  (165 B each)
Wire bandwidth    : 26.4 Mbit/s
  -> utilisation of a 1 Gbps link: 2.64%

Resend-log growth : 3.30 MB/s  = 11.88 GB/h  = 285.1 GB/day

30 s outage backlog = 600,000 msgs; replay at 1,000,000 msg/s takes 600.0 ms

Little's law: in-flight msgs = 20,000/s x 250 us = 5.000 -> a single in-order session must have a window >= 1
```
Read it as the operational consequence of the three laws: the **resend log is the real infrastructure cost** (285 GB/day for one session's outbound stream), and the replay drain time is the *floor* on how long a disconnect can keep you out of the market.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's fault analysis lives in [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Sequence-number desync** — crashing without persisting the last `MsgSeqNum` forces a `ResendRequest` (or a `SequenceNumberTooLow` rejection) and freezes trading until an operator clears it (this is law #1 failing).
2. **Order-state desync on replay** — reprocessing a resent `ExecutionReport` without checking `PossDupFlag`/`ExecID` double-counts a fill and leaves you short an unhedged position (law #2 failing).
3. **Silent session death** — a peer that stops sending with no heartbeat timeout leaves you quoting into a dead link; the OS buffers and the fills never come (the heartbeat contract, §03).

---

### 5. Canonical Literature & Study References

- **FIX Trading Community**: *FIX Protocol — Official Specifications (FIX Latest; FIX 4.4)* — fixtrading.org. The **normative source of truth**: message definitions, session-level rules, and the machine-readable **Unified Repository** (XML data dictionary) for code generation. *Priority H, free.*
- **FIX Trading Community**: *The FIX Algorithmic Trading Definition Language (FIXatdl) v1.1* — venue-agnostic XML descriptions of execution algos. *Referenced from [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/06-advanced-extensions|06 · Advanced Extensions]].*
- **OnixS**: *FIX Dictionary & Protocol Reference* — onixs.biz. A maintained, browsable explainer of the session layer, FIXT/FIXP, and the FAST/SBE/FIXML encodings. The gentlest free complement to the raw specs.
- **Nasdaq**: *TotalView-ITCH 5.0 Specification* — nasdaqtrader.com. The official binary market-data protocol (the market-data counterpart to FIX on the order-entry side). *Verified in the corpus; free.*
- **Donadio, Sebastien**: *Learn Algorithmic Trading* (Packt, 2019) — a zero-background on-ramp covering FIX communication before the official specs.

---

### 6. Connected Graph Bridges

- Sibling topic: [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]] (the TCP/kernel-bypass layer a FIX session sits on)
- Sibling topic: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] (the encoder/decoder hot path)
- Sibling topic: [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]] (the pre-trade check between signal and `NewOrderSingle`)
- Venue semantics: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]] (what the `40`/`59` fields actually mean)
- Latency context: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Colocation & Clock Synchronization]] (why the session's RTT is the whole game)
- Sub-pages (in-folder): 01 From Zero · 02 The FIX Protocol · 03 Session Management · 04 Order Lifecycle & Connectivity · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**

- **Absolute beginner (zero messaging background):** [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/01-from-zero-intuition|01 · From Zero]] — why an order is a *message*.
- **Engineering core (undergrad / job-seeking):** [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/02-the-fix-protocol|02 · The FIX Protocol]] → [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/03-session-management|03 · Session Management]] → [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|04 · Order Lifecycle & Connectivity]].
- **Robustness & scale (practitioner / graduate):** [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]] · [[pillars/08-quantitative-development/production-trading-systems/index|Risk Guards & Kill Switches]]
