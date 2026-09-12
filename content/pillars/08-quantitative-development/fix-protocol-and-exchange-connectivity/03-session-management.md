---
title: "8.8.3 FIX Session Management"
tags:
  - pillar-quant-dev
  - fix-protocol
  - exchange-connectivity
  - session-management
  - sequence-numbers
  - resend
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/02-the-fix-protocol|02 · The FIX Protocol]] (message structure, `35`/`34`/`43`/`122`).

---

### 1. Intuition & Practical Objective

The **session layer** is what makes FIX more than a message format: it is a recovery protocol. Two engines open a TCP connection, exchange `Logon` (`35=A`), and from that moment keep a pair of **monotone counters** - one for each direction - so that a gap, a crash, or a reconnect is *detectable and repairable*. The practical objective of this page: know exactly how sequence numbers advance, how a gap becomes a `ResendRequest`, how the resend is answered, and how heartbeats prove a peer is alive.

The one idea to hold onto: **a sequence number is a receipt for a message the sender kept.** Because the sender *journals* every message it emits, it can always replay any range on demand. The receiver's counter says "here is what I still need"; the sender's log says "here is everything I ever sent". Together they reconstruct a stream that TCP alone could not guarantee after a restart.

---

### 2. Mathematical Ground Truth & Derivations

**The two counters.** Each side maintains:

$$
N_{\text{out}} = \text{the MsgSeqNum to stamp on its next outbound message} \quad(\text{starts at }1),
$$
$$
N_{\text{in}} = \text{the MsgSeqNum it next expects to receive} \quad(\text{starts at }1).
$$

On sending, $N_{\text{out}} \leftarrow N_{\text{out}} + 1$. The receiver's rule on receiving `MsgSeqNum = M` is the core of the whole protocol:

$$
\text{action} =
\begin{cases}
\text{accept and process},\quad N_{\text{in}} \leftarrow M + 1, & M = N_{\text{in}},\\[3pt]
\text{send ResendRequest}(7{=}N_{\text{in}},\ 16{=}M-1), & M > N_{\text{in}},\\[3pt]
\text{ignore as duplicate}, & M < N_{\text{in}}.
\end{cases}
$$

The **gap size** is $g = M - N_{\text{in}}$: exactly $g$ messages are missing, and the request covers $[N_{\text{in}},\,M-1]$.

**Answering a resend.** The sender replays stored messages in $[\,7\,,\,16\,]$ with `PossDupFlag(43)=Y` and `OrigSendingTime(122)` set to the message's original send time - so the receiver can tell a *resend* from a *new* message. Replayed administrative messages (`Logon A`, `Heartbeat 0`, `ResendRequest 2`) are **not** re-sent as-is; they are collapsed into a `SequenceReset-GapFill` (`35=4`, `123=Y`, `36=NewSeqNo`) that advances the receiver's counter past them. Application messages *are* re-sent.

**SequenceReset in two modes** - a critical distinction:

$$
\texttt{4}\ (123{=}Y,\ \texttt{gap-fill}) :\ \text{advance } N_{\text{in}} \to 36,\ \text{silently skip admin msgs};
$$
$$
\texttt{4}\ (123{=}N,\ \texttt{reset}) :\ \text{hard reset } N_{\text{in}} \to 36,\ \text{**discard everything in between** (dangerous)}.
$$

A bare reset is the mechanism by which missed orders are *forgotten* - intentionally, during a session "resynchronisation", and dangerously if used to paper over a bug.

**Heartbeats and the liveness contract.** With `HeartBtInt = H` seconds:

$$
\text{send Heartbeat}(35{=}0)\ \text{if no message sent in } H;
$$
$$
\text{send TestRequest}(35{=}1)\ \text{if no message received in } H;
$$
$$
\text{disconnect if no reply (or any data) within } H \text{ afterwards.}
$$

The `TestRequest` demands a `Heartbeat` bearing the same `TestReqID(112)`; no reply means the peer is dead and the session must be torn down rather than left half-open.

**Resend log sizing.** The outbound log must hold at least the largest plausible outage: for rate $R$ (msg/s) and outage $\tau$ seconds, the backlog is $B = R\tau$ messages, $\dot S = R s$ bytes/s of storage. This is the operational cost of the reliability guarantee.

---

### 3. Computational Implementation - a session with gap detection and resend

We model both sides of a FIX session: an outbound log for replay, an expected-inbound counter, gap detection, resend request, and the gap-fill that resynchronises the counters. Stdlib only.



Read the trace as the recovery proof: the server sees `seq=3` while expecting `1`, reports a gap of size $3-1=2$, requests exactly `[1,2]`, accepts the two replayed `PossDup` messages, and then accepts `seq=3` - ending with $N_{\text{in}}=4$, identical to the sender's $N_{\text{out}}$. **The two counters converge; that is session correctness.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Losing the log on crash (sequence blow-up).** If `N_out` is persisted but the *messages* are not, the engine must answer a `ResendRequest` it cannot satisfy. The only legal recovery is a `SequenceReset` that *admits* the loss - which means the venue may never learn of orders your engine sent. Journaling is not optional; it is the receipt.
2. **Duplicate execution from a naïve replay.** A resent `ExecutionReport` carries `43=Y`; if you process it as new you double the fill. This is the classic desync (worked in [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **The `SequenceReset-Reset` foot-gun.** `123=N` (hard reset) *discards* the messages in the reset range. Using it to clear a stubborn gap hides real orders; only gap-fill (`123=Y`) is safe for routine resends.
4. **Midday logon with a stale sequence.** Reconnecting with the wrong `MsgSeqNum` in `Logon` triggers either a resend or a `SequenceNumberTooLow` reject; the recovery is deterministic but only if the engine knows which of its counters the venue last saw.
5. **Half-open sockets.** TCP keep-alive is far too slow (minutes) for a trading session; without FIX heartbeats you can sit quoting into a dead link. The `TestRequest`/`Heartbeat` exchange is the *only* timely liveness proof.
6. **Heartbeat interval too long.** `HeartBtInt` is a latency ceiling on failure detection: a 30 s interval means up to 30 s of trading into a dead peer. Venues often mandate a range (commonly 10–60 s).
7. **Clock skew on `OrigSendingTime`.** Resends carry `52` (new send time) and `122` (original send time); a receiver that validates `52` strictly, or a sender with skewed clocks, creates spurious rejects.

---

### 5. References

- **FIX Trading Community**, *FIX 4.4 Specification, Volume 2
- **FIX Trading Community**, *FIX Latest
- **OnixS**, *FIX Dictionary & Protocol Reference*

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/02-the-fix-protocol|02 · The FIX Protocol]]
- Forward: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|04 · Order Lifecycle & Connectivity]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/index|Index Hub]]
- Deep-dive: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes]] (desync and duplicate execution)
- Context: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]] (why the log and the session sit in the hot path)
