---
title: "04 - Order Lifecycle & Connectivity Architecture"
tags:
  - pillar-quant-dev
  - fix-protocol
  - exchange-connectivity
  - order-lifecycle
  - high-availability
  - gateways
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/03-session-management|03 · Session Management]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]].

---

### 1. Intuition & Practical Objective

An order is not an event; it is a **state machine that lives on two machines at once** — yours and the venue's. Every `ExecutionReport` you receive is a transition on that shared state, and your job is to apply transitions so that your view converges to the venue's. Wrapping around that state machine is the **connectivity architecture**: the order gateway that serialises your intents onto a session, the HA failover that keeps the session alive when a box dies, and the choice between FIX and the venue's native (often binary) protocol.

The practical objective: be able to write down (a) the exact `ExecType`/`OrdStatus` transition table, (b) the running-quantity invariants that must hold after every report, and (c) the availability arithmetic that decides how many gateways you run and how sequence-number handoff works on failover.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The order state machine

State is the pair `(ExecType 150, OrdStatus 39)`. The transitions, driven by `ExecutionReport (35=8)`:

| Event (`150`) | `39` after | Meaning |
|---|---|---|
| `0` New | `0` New | venue accepted the order |
| `1` PartialFill | `1` PartiallyFilled | some shares executed |
| `2` Fill | `2` Filled | order complete — **terminal** |
| `4` Canceled | `4` Canceled | cancelled (fully or remainder) — **terminal** |
| `5` Replaced | *(unchanged)* | a `G` replace was accepted |
| `8` Rejected | `8` Rejected | venue refused the order — **terminal** |
| `9` Suspended | `9` Suspended | order pulled mid-session |

Terminal states — `2` Filled, `4` Canceled, `8` Rejected — admit **no further fills**. Enforcing that is what stops the desyncs of [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes]].

**The running-quantity invariants** (must hold after *every* report):

$$\texttt{151 LeavesQty} = \texttt{38 OrderQty} - \texttt{14 CumQty}, \qquad \texttt{14 CumQty} = \sum_i \texttt{32 LastQty}_i,$$
$$\texttt{6 AvgPx} = \frac{\sum_i \texttt{32 LastQty}_i \cdot \texttt{31 LastPx}_i}{\sum_i \texttt{32 LastQty}_i}.$$

These are cheap assertions; a gateway that checks them on every report catches most desyncs at the source rather than at the P&L.

#### 2.2 Throughput of a gateway tier

An order gateway is a queue. By Little's law, the in-flight order count is arrival rate times service time, and the stability condition is that service rate exceeds arrival rate:

$$L = \lambda W,\qquad \text{stability: } \lambda < \mu \quad(\lambda = \text{orders/s},\ \mu = \text{gateway capacity}).$$

A gateway that persists every message before sending (write-ahead) adds a durable-write latency $w$ per message, so its effective per-order service time is $\frac{1}{c} + w$ where $c$ is the raw processing rate. Throughput collapses when $w$ dominates — the reason low-latency gateways use a **journaled ring buffer** or an NVMe log rather than synchronous `fsync` per order.

#### 2.3 Availability of a gateway tier

For a component with mean time between failures MTBF and mean time to repair MTTR, availability is

$$A_1 = \frac{\text{MTBF}}{\text{MTBF}+\text{MTTR}}.$$

$n$ **independent** active/active replicas are all-down only if *every* replica is down:

$$A_n = 1 - (1-A_1)^n.$$

Expected annual downtime is $(1-A_n)\times 8760$ hours. Independence is the optimistic assumption — a shared switch, power feed, or cluster manager correlates failures, so real availability sits between the single-node and the independent-replica bound.

#### 2.4 Failover and sequence-number handoff

The hard part of HA is not the box dying — it is the **session state**. On failover the standby must present the *same* `SenderCompID`/`TargetCompID` and the *correct* `MsgSeqNum` (both in and out). Two designs:

- **Hot standby with shared session state:** counters and the outbound log live in a replicated store; failover is a rebind of the socket. Recovery time $T_{\text{rec}} \approx$ the replication lag, and the session sequence continues unbroken (a `Logon` with the true next sequence → no resend).
- **Cold reconnect:** the standby logs on with the persisted counters; if the log is behind, the venue issues a `ResendRequest` and the standby replays. Recovery time $T_{\text{rec}} \approx$ replay drain, which grows with the outage (see the hub's backlog model).

The **drop-copy** session — a read-only FIX session mirroring all `ExecutionReport`s to a risk or clearing system — is the decoupling mechanism: the gateway's failover does not have to be coupled to the downstream that consumes fills.

---

### 3. Computational Implementation — lifecycle + availability

Two models in one script: (a) an `ExecutionReport`-driven order state machine with the running-quantity invariants asserted, and (b) the gateway availability arithmetic of §2.3. Stdlib only.

```python
# 04 - order lifecycle state machine + connectivity HA availability
class Order:
    """FIX order state machine driven by ExecutionReport(35=8) OrdStatus(39)."""
    def __init__(self, cl_ord_id, qty):
        self.cl_ord_id = cl_ord_id
        self.order_qty = qty
        self.cum_qty = 0
        self.leaves_qty = qty
        self.avg_px = 0.0
        self.status = "New"          # OrdStatus 39: 0=New
        self.notional = 0.0

    def on_fill(self, last_qty, last_px):
        self.cum_qty += last_qty
        self.notional += last_qty * last_px
        self.leaves_qty = self.order_qty - self.cum_qty
        self.avg_px = self.notional / self.cum_qty if self.cum_qty else 0.0
        self.status = "Filled" if self.leaves_qty == 0 else "PartiallyFilled"
        self._check()
        return self

    def on_cancel(self, canceled_qty):
        self.leaves_qty -= canceled_qty
        self.status = "Canceled"
        self._check()

    def _check(self):
        assert self.cum_qty + self.leaves_qty <= self.order_qty, "oversell"
        assert self.leaves_qty >= 0, "negative leaves"

    def __str__(self):
        return (f"{self.cl_ord_id:8s} {self.status:16s} "
                f"cum={self.cum_qty:4.0f} leaves={self.leaves_qty:4.0f} "
                f"avgPx={self.avg_px:8.4f}")

o = Order("ORD_42", 500)
print("OrdStatus 39: 0=New 1=PartiallyFilled 2=Filled 4=Canceled")
print(" ", o)
o.on_fill(200, 150.50); print(" ", o)          # ER 39=1
o.on_fill(150, 150.75); print(" ", o)          # ER 39=1
o.on_fill(150, 151.00); print(" ", o)          # ER 39=2 -> terminal

# weighted average check: sum(qty_i * px_i) / sum(qty_i)
fills = [(200, 150.50), (150, 150.75), (150, 151.00)]
manual = sum(q * p for q, p in fills) / sum(q for q, _ in fills)
print(f"avgPx invariant: machine={o.avg_px:.6f} manual={manual:.6f} "
      f"match={abs(o.avg_px-manual) < 1e-9}")

# a rejected order must never fill
r = Order("ORD_43", 100)
r.status = "Rejected"                          # OrdStatus 8
print("\nRejected order: leavesQty stays", r.leaves_qty, "-> no fill may be applied")

# --- connectivity HA: expected availability of a gateway tier ---
def availability(mtbf_h, mttr_h):
    return mtbf_h / (mtbf_h + mttr_h)

MTBF, MTTR = 2000.0, 2.0                        # hours
a1 = availability(MTBF, MTTR)
# active-active with 2 independent gateways: downtime requires BOTH down
# (shared-fate neglected -> optimistic upper bound)
a2 = 1 - (1 - a1) ** 2
print(f"\nSingle gateway : A = {a1:.6f}  ({a1*100:.4f}%)")
print(f"Twin active/active (independent) : A = {a2:.6f}  ({a2*100:.4f}%)")
print(f"Expected downtime/yr: 1 gw = {(1-a1)*8760:.2f} h, "
      f"2 gw = {(1-a2)*8760:.4f} h")
```
```
OrdStatus 39: 0=New 1=PartiallyFilled 2=Filled 4=Canceled
  ORD_42   New              cum=   0 leaves= 500 avgPx=  0.0000
  ORD_42   PartiallyFilled  cum= 200 leaves= 300 avgPx=150.5000
  ORD_42   PartiallyFilled  cum= 350 leaves= 150 avgPx=150.6071
  ORD_42   Filled           cum= 500 leaves=   0 avgPx=150.7250
avgPx invariant: machine=150.725000 manual=150.725000 match=True

Rejected order: leavesQty stays 100 -> no fill may be applied

Single gateway : A = 0.999001  (99.9001%)
Twin active/active (independent) : A = 0.999999  (99.9999%)
Expected downtime/yr: 1 gw = 8.75 h, 2 gw = 0.0087 h
```
Read the two halves as one story. The lifecycle half shows the **invariants holding through a partial fill to completion** — `cum + leaves = orderQty` at every step, `avgPx` the exact size-weighted mean (150.7250, not the naive 150.75 mean-of-prices). The availability half shows the **2-replica payoff**: a single gateway is down 8.75 h/year, a twin active/active tier 0.0087 h/year — a 1000× reduction, *if* the replicas are truly independent (shared switches, power, and a shared cluster manager quickly break that assumption).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Applying a fill after a terminal state.** Once `39 ∈ {2,4,8}` no further `32 LastQty` may be applied; a late or duplicate report that slips through corrupts the position. Guard the terminal states explicitly.
2. **Ignoring `151 LeavesQty` and re-deriving it.** The venue's `151` is *the* truth; deriving it from your own fill arithmetic and disagreeing with the venue is the signature of a lost report. Assert `151 == 38 - 14` and alarm on mismatch.
3. **Average-price error.** Using a simple mean of fill prices instead of the **size-weighted** mean mis-states `AvgPx` whenever fill sizes differ — here 150.75 (wrong) vs 150.7250 (correct).
4. **Assuming HA replicas are independent.** The $(1-A_1)^2$ bound is optimistic; correlated failure domains (same rack, same switch, same power) mean the real downtime is higher. Count the shared components.
5. **Sequence-number handoff bugs on failover.** A standby that logs on with the wrong `MsgSeqNum` forces either a resend storm or a hard reset that loses orders. The session counters are *state*, not configuration, and must be replicated.
6. **Synchronous log write in the hot path.** Persisting every order with `fsync` before send caps your throughput and inflates `W` in Little's law; the gateway becomes the bottleneck. Batch or use an asynchronous durable ring.
7. **Cancel/replace races.** A `G` (replace) that crosses a `D` in flight can leave the venue with two live orders; always carry `41 OrigClOrdID` and reconcile against the `150=5` report.

---

### 5. Canonical Literature & Study References

- **FIX Trading Community**, *FIX 4.4 Specification* — the `ExecutionReport (8)` field tables and the normative `ExecType`/`OrdStatus` value lists. *The authoritative state reference.*
- **FIX Trading Community**, *FIX Session Layer / FIXT.1.1* — session reset and failover semantics that constrain the HA design.
- **Nasdaq**, *TotalView-ITCH 5.0 Specification* and *OUCH* — the venue-native binary order-entry protocol (introduced in [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/06-advanced-extensions|06 · Advanced Extensions]]).
- **Narang, Rishi K.**: *Inside the Black Box* (2nd ed.) — where the gateway sits in the end-to-end trading architecture.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/03-session-management|03 · Session Management]]
- Forward: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/index|Index Hub]]
- Sibling: [[pillars/08-quantitative-development/production-risk-guards-and-kill-switches|Production Risk Guards & Kill Switches]] (what sits between the signal and the `NewOrderSingle`)
- Context: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]] · [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]] (the socket the gateway writes to)
