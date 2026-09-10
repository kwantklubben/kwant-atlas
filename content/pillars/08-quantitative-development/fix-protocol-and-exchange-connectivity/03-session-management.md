---
title: "03 - FIX Session Management: Logon, Heartbeats, Sequence Numbers & Resend"
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

The **session layer** is what makes FIX more than a message format: it is a recovery protocol. Two engines open a TCP connection, exchange `Logon` (`35=A`), and from that moment keep a pair of **monotone counters** — one for each direction — so that a gap, a crash, or a reconnect is *detectable and repairable*. The practical objective of this page: know exactly how sequence numbers advance, how a gap becomes a `ResendRequest`, how the resend is answered, and how heartbeats prove a peer is alive.

The one idea to hold onto: **a sequence number is a receipt for a message the sender kept.** Because the sender *journals* every message it emits, it can always replay any range on demand. The receiver's counter says "here is what I still need"; the sender's log says "here is everything I ever sent". Together they reconstruct a stream that TCP alone could not guarantee after a restart.

---

### 2. Mathematical Ground Truth & Derivations

**The two counters.** Each side maintains:

$$N_{\text{out}} = \text{the MsgSeqNum to stamp on its next outbound message} \quad(\text{starts at }1),$$
$$N_{\text{in}} = \text{the MsgSeqNum it next expects to receive} \quad(\text{starts at }1).$$

On sending, $N_{\text{out}} \leftarrow N_{\text{out}} + 1$. The receiver's rule on receiving `MsgSeqNum = M` is the core of the whole protocol:

$$\text{action} =
\begin{cases}
\text{accept and process},\quad N_{\text{in}} \leftarrow M + 1, & M = N_{\text{in}},\\[3pt]
\text{send ResendRequest}(7{=}N_{\text{in}},\ 16{=}M-1), & M > N_{\text{in}},\\[3pt]
\text{ignore as duplicate}, & M < N_{\text{in}}.
\end{cases}$$

The **gap size** is $g = M - N_{\text{in}}$: exactly $g$ messages are missing, and the request covers $[N_{\text{in}},\,M-1]$.

**Answering a resend.** The sender replays stored messages in $[\,7\,,\,16\,]$ with `PossDupFlag(43)=Y` and `OrigSendingTime(122)` set to the message's original send time — so the receiver can tell a *resend* from a *new* message. Replayed administrative messages (`Logon A`, `Heartbeat 0`, `ResendRequest 2`) are **not** re-sent as-is; they are collapsed into a `SequenceReset-GapFill` (`35=4`, `123=Y`, `36=NewSeqNo`) that advances the receiver's counter past them. Application messages *are* re-sent.

**SequenceReset in two modes** — a critical distinction:

$$\texttt{4}\ (123{=}Y,\ \texttt{gap-fill}) :\ \text{advance } N_{\text{in}} \to 36,\ \text{silently skip admin msgs};$$
$$\texttt{4}\ (123{=}N,\ \texttt{reset}) :\ \text{hard reset } N_{\text{in}} \to 36,\ \text{**discard everything in between** (dangerous)}.$$

A bare reset is the mechanism by which missed orders are *forgotten* — intentionally, during a session "resynchronisation", and dangerously if used to paper over a bug.

**Heartbeats and the liveness contract.** With `HeartBtInt = H` seconds:

$$\text{send Heartbeat}(35{=}0)\ \text{if no message sent in } H;$$
$$\text{send TestRequest}(35{=}1)\ \text{if no message received in } H;$$
$$\text{disconnect if no reply (or any data) within } H \text{ afterwards.}$$

The `TestRequest` demands a `Heartbeat` bearing the same `TestReqID(112)`; no reply means the peer is dead and the session must be torn down rather than left half-open.

**Resend log sizing.** The outbound log must hold at least the largest plausible outage: for rate $R$ (msg/s) and outage $\tau$ seconds, the backlog is $B = R\tau$ messages, $\dot S = R s$ bytes/s of storage. This is the operational cost of the reliability guarantee.

---

### 3. Computational Implementation — a session with gap detection and resend

We model both sides of a FIX session: an outbound log for replay, an expected-inbound counter, gap detection, resend request, and the gap-fill that resynchronises the counters. Stdlib only.

```python
# 03 - session management: sequence numbers, gap detection, resend replay
SOH = "\x01"
RESEND_REQUEST, HEARTBEAT, LOGON = "2", "0", "A"

class FixSession:
    """One side of a FIX session. Keeps an outbound log (for replay) and a
    next-expected-inbound sequence number."""
    def __init__(self, name):
        self.name = name
        self.next_out = 1                       # outbound MsgSeqNum to use
        self.next_in = 1                        # inbound MsgSeqNum expected
        self.log = {}                           # seq -> (type, payload) for replay
        self.pos_dup = False                    # PossDupFlag(43) on replays

    def send(self, mtype, payload):
        seq = self.next_out
        self.log[seq] = (mtype, payload)
        self.next_out += 1
        return seq, mtype, payload

    def replay(self, begin, end):
        """Answer a ResendRequest(2) for [begin, end]; admin msgs are gap-filled
        with SequenceReset(4), app msgs are resent with PossDupFlag(43)=Y."""
        out = []
        for seq in range(begin, end + 1):
            if seq not in self.log:
                continue
            mtype, payload = self.log[seq]
            if mtype in (LOGON, HEARTBEAT, RESEND_REQUEST):
                out.append((seq, "4", f"SequenceReset NewSeqNo={seq+1}"))  # don't re-admin
            else:
                out.append((seq, mtype, f"PossDup=Y|{payload}"))
        return out

    def receive(self, seq, mtype, payload):
        """Return an action string. This is the heart of gap detection."""
        if seq == self.next_in:
            self.next_in += 1
            return "ACCEPT"
        if seq > self.next_in:
            gap_from = self.next_in              # expected
            gap_to = seq - 1                     # last missing
            return f"GAP: send ResendRequest(35={RESEND_REQUEST}) begin={gap_from} end={gap_to}"
        return "POSSIBLE_DUP: ignore (seq already processed)"

    def fill_gap(self, msg):
        """A ResendRequest is satisfied by replay; jump the expected pointer."""
        self.next_in = msg + 1
        return self.next_in

# --- normal flow ---
c, s = FixSession("CLIENT"), FixSession("SERVER")
for _ in range(3):
    c.send("D", "NewOrderSingle ORD_42")
print(f"client outbound log  = {sorted(c.log)}  next_out = {c.next_out}")

# --- a gap appears: server *should* have seen 1,2,3 but 1 and 2 were lost ---
print("\nserver processes seq 3 first (1 and 2 lost in transit):")
print("  ->", s.receive(3, "D", "NewOrderSingle ORD_42"))

# server asks for 1..2; client replays from its persistent log
replay = c.replay(1, 2)
for seq, mtype, payload in replay:
    print(f"  replay seq={seq} type={mtype} {payload}")
    if mtype == "4":
        print(f"    -> gap-filled; server next_in := {s.fill_gap(seq)}")
    else:
        print(f"    -> {s.receive(seq, mtype, payload)}")

# now the original seq 3 is accepted and the session is back in sync
print("  ->", s.receive(3, "D", "NewOrderSingle ORD_42"), f"| next_in={s.next_in}")

# --- heartbeat timing (why a silent peer must be probed) ---
HB = 30                                    # HeartBtInt seconds
print(f"\nHeartBtInt = {HB}s  -> send Heartbeat(35=0) if nothing sent in {HB}s;"
      f"\n  send TestRequest(35=1) if nothing received in {HB}s;"
      f"\n  disconnect if no Data(35=2/0/1) within {HB}s after that.")
for t in (0, 30, 60, 90):
    state = "idle" if t < HB else ("send HEARTBEAT" if t < 2*HB else "send TEST_REQUEST")
    print(f"  t={t:3d}s : {state}")
```
```
client outbound log  = [1, 2, 3]  next_out = 4

server processes seq 3 first (1 and 2 lost in transit):
  -> GAP: send ResendRequest(35=2) begin=1 end=2
  replay seq=1 type=D PossDup=Y|NewOrderSingle ORD_42
    -> ACCEPT
  replay seq=2 type=D PossDup=Y|NewOrderSingle ORD_42
    -> ACCEPT
  -> ACCEPT | next_in=4

HeartBtInt = 30s  -> send Heartbeat(35=0) if nothing sent in 30s;
  send TestRequest(35=1) if nothing received in 30s;
  disconnect if no Data(35=2/0/1) within 30s after that.
  t=  0s : idle
  t= 30s : send HEARTBEAT
  t= 60s : send TEST_REQUEST
  t= 90s : send TEST_REQUEST
```
Read the trace as the recovery proof: the server sees `seq=3` while expecting `1`, reports a gap of size $3-1=2$, requests exactly `[1,2]`, accepts the two replayed `PossDup` messages, and then accepts `seq=3` — ending with $N_{\text{in}}=4$, identical to the sender's $N_{\text{out}}$. **The two counters converge; that is session correctness.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Losing the log on crash (sequence blow-up).** If `N_out` is persisted but the *messages* are not, the engine must answer a `ResendRequest` it cannot satisfy. The only legal recovery is a `SequenceReset` that *admits* the loss — which means the venue may never learn of orders your engine sent. Journaling is not optional; it is the receipt.
2. **Duplicate execution from a naïve replay.** A resent `ExecutionReport` carries `43=Y`; if you process it as new you double the fill. This is the classic desync (worked in [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **The `SequenceReset-Reset` foot-gun.** `123=N` (hard reset) *discards* the messages in the reset range. Using it to clear a stubborn gap hides real orders; only gap-fill (`123=Y`) is safe for routine resends.
4. **Midday logon with a stale sequence.** Reconnecting with the wrong `MsgSeqNum` in `Logon` triggers either a resend or a `SequenceNumberTooLow` reject; the recovery is deterministic but only if the engine knows which of its counters the venue last saw.
5. **Half-open sockets.** TCP keep-alive is far too slow (minutes) for a trading session; without FIX heartbeats you can sit quoting into a dead link. The `TestRequest`/`Heartbeat` exchange is the *only* timely liveness proof.
6. **Heartbeat interval too long.** `HeartBtInt` is a latency ceiling on failure detection: a 30 s interval means up to 30 s of trading into a dead peer. Venues often mandate a range (commonly 10–60 s).
7. **Clock skew on `OrigSendingTime`.** Resends carry `52` (new send time) and `122` (original send time); a receiver that validates `52` strictly, or a sender with skewed clocks, creates spurious rejects.

---

### 5. Canonical Literature & Study References

- **FIX Trading Community**, *FIX 4.4 Specification, Volume 2 — Session Layer* (fixtrading.org) — the normative session rules: logon sequence negotiation, heartbeat/test-request semantics, resend/gap-fill, and the `SequenceReset` modes. *The authoritative reference for this page.*
- **FIX Trading Community**, *FIX Latest — Session Layer* — the modern restatement (FIXT.1.1 transport) with the same core invariants.
- **OnixS**, *FIX Dictionary & Protocol Reference* — the clearest free walkthrough of sequence numbers and resend for learners.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/02-the-fix-protocol|02 · The FIX Protocol]]
- Forward: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|04 · Order Lifecycle & Connectivity]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/index|Index Hub]]
- Deep-dive: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes]] (desync and duplicate execution)
- Context: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]] (why the log and the session sit in the hot path)
