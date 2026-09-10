---
title: "05 - Failure Modes & Practice: Desync, Duplicates & Certification"
tags:
  - pillar-quant-dev
  - fix-protocol
  - exchange-connectivity
  - failure-modes
  - duplicate-execution
  - certification
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|04 · Order Lifecycle & Connectivity]].

---

### 1. Intuition & Practical Objective

FIX connectivity fails in a small number of *structural* ways, and each one traces to a first principle: the session lost the thread of what was sent (a sequence gap), the client lost the thread of what the venue did (an order-state desync), or the two parted company silently (a heartbeat failure). This page names the failures precisely, **quantifies** them, and then covers the discipline that prevents them from reaching production: **certification and conformance testing** against the venue's own test harness.

The one idea: **a protocol failure is almost never "the message was wrong" — it is "the two sides disagree about history".** Every mitigation below is a mechanism for keeping the two histories identical.

---

### 2. Mathematical Ground Truth & Derivations

**The three roots.**

1. **Sequence divergence** — $N_{\text{in}} \ne M$ (gap) or $N_{\text{in}} > M$ (already-processed).
2. **State divergence** — the venue's `(14 CumQty, 151 LeavesQty, 39 OrdStatus)` disagrees with your replica.
3. **Liveness divergence** — one side believes the session is up while the other is dead.

**Gap arrival probability.** If a fraction $p$ of messages is lost (or reordered past the point of recovery), the probability that a gap has appeared within $n$ messages is

$$P(\text{gap within } n) = 1 - (1-p)^n, \qquad \mathbb{E}[\text{messages to first gap}] = \frac{1}{p}.$$

At $p = 0.2\%$, expect a gap roughly every **500 messages** — and a gap within 1,000 messages with probability $0.865$. Connectivity is *continuously* in recovery, not occasionally.

**Duplicate-execution loss.** If a replay of $k$ fills is processed twice, the position error is the summed replayed quantity,

$$\Delta q = \sum_{i \in \text{replayed}} \texttt{32 LastQty}_i,$$

which is an unhedged directional position. For two replayed fills of 200 and 300 shares that is **500 phantom shares** — precisely the case worked in §3.

**The un-acked-cancel exposure.** A cancel you sent but whose acknowledgement you missed leaves qty $q$ live for as long as it takes to detect (latency $\delta$). With a market move of $b$ basis points over $\delta$,

$$\text{risk} \approx q \cdot P \cdot \frac{b}{10^4}.$$

For $q=800$, $P=\$150.50$, $b=12$ bps that is **\$144.48** of uncontrolled exposure from a single missed ack.

**Certification as a coverage problem.** A venue certification suite is a finite set of scenarios; the risk of going live with an untested path is the fraction of the state machine × session-event cross-product left uncovered,

$$\text{coverage} = \frac{|\text{scenarios passed}|}{|\text{scenarios required}|}.$$

The required set is the **cross-product of order transitions and session events** — every state must survive every event (a fill during a resend, a cancel during failover, a logon mid-partial-fill).

**Duplicate-suppression condition.** A receiver is duplicate-safe iff every application message carries a key that repeats on replay and is unique per occurrence — the pair

$$(\texttt{11 ClOrdID},\ \texttt{17 ExecID})$$

— and the receiver keeps a set of seen `ExecID`s. `PossDupFlag(43)=Y` is the *hint*; the `ExecID` is the *proof*.

---

### 3. Computational Implementation — desync in numbers

We simulate the exact failure: a link drops, the session replays its log, and a client that ignores `PossDup`/`ExecID` double-counts the fills. Then we quantify gap arrival and cancel exposure. Stdlib only.

```python
# 05 - failure modes: a drop + ignorant replay desyncs order state
SOH = "\x01"

class Book:
    """Client-side view of a single order, keyed by ClOrdID(11)."""
    def __init__(self):
        self.exec_ids = set()      # ExecID(17) dedup set
        self.filled = 0

    def on_exec(self, cl_ord_id, exec_id, last_qty, use_dedup=True):
        if use_dedup and exec_id in self.exec_ids:
            return False           # duplicate got discarded
        self.exec_ids.add(exec_id)
        self.filled += last_qty
        return True

# --- scenario: the link drops after the fill; the exec report is replayed ---
fills = [("ORD_42", "E1", 200), ("ORD_42", "E2", 300)]   # replayed from log

print("Replay WITHOUT PossDup/ExecID dedup (bug):")
bad = Book()
for cid, eid, q in fills + fills:            # the whole batch is replayed twice
    bad.on_exec(cid, eid, q, use_dedup=False)
print(f"  filled = {bad.filled}  (true fill = {sum(q for *_, q in fills)})  "
      f"-> phantom {bad.filled - sum(q for *_, q in fills)} shares")

print("\nReplay WITH ExecID(17) dedup (correct):")
good = Book()
for cid, eid, q in fills + fills:
    good.on_exec(cid, eid, q, use_dedup=True)
print(f"  filled = {good.filled}  (true fill = {sum(q for *_, q in fills)})  "
      f"-> phantom {good.filled - sum(q for *_, q in fills)} shares")

# --- sequence-number drift: how fast does a stale counter desync? ---
print("\nSequence drift: if 0.2% of messages are dropped, the first gap")
print("  arrives, on average, after 1/0.002 = 500 messages.")
p = 0.002
for n in (100, 500, 1000):
    print(f"  P(gap within {n:4d} msgs) = 1-(1-p)^n = {1-(1-p)**n:.3f}")

# --- the cost of one missed cancel-ack: unhedged shares at risk ---
qty, price, gap_bps = 800, 150.50, 12       # market moves 12 bps before detection
risk = qty * price * gap_bps / 10_000
print(f"\nUn-acked cancel: {qty} shares x {price} x {gap_bps} bps = ${risk:,.2f} "
      f"of uncontrolled exposure")
```
```
Replay WITHOUT PossDup/ExecID dedup (bug):
  filled = 1000  (true fill = 500)  -> phantom 500 shares

Replay WITH ExecID(17) dedup (correct):
  filled = 500  (true fill = 500)  -> phantom 0 shares

Sequence drift: if 0.2% of messages are dropped, the first gap
  arrives, on average, after 1/0.002 = 500 messages.
  P(gap within  100 msgs) = 1-(1-p)^n = 0.181
  P(gap within  500 msgs) = 1-(1-p)^n = 0.632
  P(gap within 1000 msgs) = 1-(1-p)^n = 0.865

Un-acked cancel: 800 shares x 150.5 x 12 bps = $144.48 of uncontrolled exposure
```
The first two blocks are the desync proof: the same replay produces **500 phantom shares** without dedup and **zero** with it. The last two are the *budgets*: how often a gap arrives (every ~500 messages at 0.2% loss) and what a single missed cancel costs (\$144.48). Reliability engineering is the discipline of paying a little (dedup state, journaling, certification) to avoid these.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Sequence-number desynchronization.** *Root:* failing to persist `MsgSeqNum` (or the log) across a crash. *Symptom:* the venue rejects with `SequenceNumberTooLow`, or forces a resend the engine cannot satisfy; trading freezes until an operator intervenes. *Mitigation:* journal every outbound/inbound message to durable storage *before* it is acted upon.
2. **Duplicate execution on replay.** *Root:* processing a resent `ExecutionReport` as new. *Symptom:* double-counted `CumQty`, phantom position (500 shares here), wrong P&L. *Mitigation:* dedup on `ExecID(17)`; treat `PossDupFlag(43)=Y` as a warning to *check*, never as the check itself.
3. **Order-state desync from a dropped report.** *Root:* a lost `ExecutionReport` with the session still believing it is in sync. *Symptom:* your `LeavesQty` diverges from the venue's; you hedge against a position that does not exist. *Mitigation:* assert `151 == 38 − 14` on every report and reconcile (query order status) on mismatch.
4. **Cancelling at the wrong time.** *Root:* a cancel crossing a fill in flight, or replacing an order that already filled. *Symptom:* an open order you believe cancelled, or a replace that duplicates exposure. *Mitigation:* carry `41 OrigClOrdID`; handle the `OrderCancelReject (35=9)` path explicitly.
5. **TCP Nagle buffering.** *Root:* leaving `TCP_NODELAY` unset, so the OS coalesces small writes. *Symptom:* order transmission delayed by up to the Nagle-delayed-ACK window (tens to hundreds of ms) — catastrophic for latency-sensitive flow. *Mitigation:* set `TCP_NODELAY` (and generally use a tuned, low-latency socket stack; see [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]]).
6. **Silent session death.** *Root:* no timely heartbeat/test-request enforcement. *Symptom:* quoting into a dead link; the OS happily buffers while the venue hears nothing. *Mitigation:* enforce `HeartBtInt`, `TestRequest`, and auto-disconnect.
7. **Midday/invalid logon and resync storms.** *Root:* reconnecting with stale or wrong sequence numbers. *Symptom:* a large `ResendRequest` or a hard `SequenceReset` that silently drops messages. *Mitigation:* persist both counters; prefer gap-fill over reset; alert on any hard reset.
8. **Clock/time skew.** *Root:* unsynchronised clocks on `52 SendingTime` / `122 OrigSendingTime` validation. *Symptom:* spurious rejects on resends or on session-time checks. *Mitigation:* disciplined NTP/PTP (see [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Colocation & Clock Synchronization]]).
9. **Log-replay backlog.** *Root:* an outage longer than the log can hold, or a drain rate slower than arrival. *Symptom:* replay takes longer than the outage and never catches up. *Mitigation:* size the log for MTTR; monitor backlog vs drain time.
10. **Certification gaps.** *Root:* shipping without exercising every transition × session event. *Symptom:* a production failure on the one path never tested (a fill during failover, a replace during resend). *Mitigation:* the conformance suite below.

**Certification & conformance testing (the practice).** Before going live with a venue you must pass its **certification suite**, which is built from the same three roots:

- **Session tests:** logon sequence negotiation, heartbeat timeout, `TestRequest`/`Heartbeat` exchange, forced disconnect mid-session, reconnect with correct/incorrect sequence, resend request/replay, `SequenceReset` gap-fill and hard reset.
- **Order tests:** every `OrdStatus` transition, partial fills to completion, cancel and cancel/replace, rejects (`35=3` session-level and `OrdStatus=8` order-level), duplicate `ClOrdID`.
- **Robustness tests:** malformed tags, bad `BodyLength`/`CheckSum`, unknown message types, out-of-order application messages, a fill delivered during a resend.
- **Conformance discipline:** a deterministic, replayable harness whose scenarios are the **state-machine × session-event cross-product**; the coverage metric of §2 is the exit criterion. Test on the venue's **UAT/certification environment** with the *same* configuration as production (same `HeartBtInt`, same session IDs) — a passing test on different settings certifies nothing.

---

### 5. Canonical Literature & Study References

- **FIX Trading Community**, *FIX 4.4 Specification* and *FIX Latest* — the normative value lists for `OrdStatus`, `ExecType`, and the session-level reject codes; the definitions the certification suite tests against.
- **FIX Trading Community**, *FIX Unified Repository* — generate your conformance test matrix directly from the data dictionary rather than from memory.
- **OnixS**, *FIX Dictionary & Protocol Reference* — the readable treatment of resend, `PossDupFlag`, and the `SequenceReset` modes that underpin failure modes 1, 2, and 7.
- **López de Prado, Marcos**, *Advances in Financial Machine Learning* — the broader discipline of testing for correctness before trusting a system's output; the mindset transfers directly to connectivity certification.
- **Databento / Red Hat**, *low-latency Linux & networking tuning guides* — the socket-level fixes behind failure mode 5.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|04 · Order Lifecycle & Connectivity]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/03-session-management|03 · Session Management]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/index|Index Hub]]
- Forward: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]] · [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]]
