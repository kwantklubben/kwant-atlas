---
title: "04 - Risk Guards & Kill Switches"
tags:
  - pillar-quant-dev
  - production-trading-systems
  - risk-guards
  - kill-switch
  - pre-trade-risk
  - rate-limiting
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/production-trading-systems/03-monitoring-and-alerting|03 · Monitoring & Alerting]] and [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|FIX · Order Lifecycle & Connectivity]].

---

### 1. Intuition & Practical Objective

On 1 August 2012, a bad deployment at Knight Capital left an obsolete code path live on one of eight servers. Over 45 minutes it sent millions of unintended orders, accumulated a position the firm could not finance, and lost roughly **\$440 million**, which was more than the firm's equity — Knight was sold within days. Nothing in that system's *strategy* was wrong. What was missing was a component whose only job was to **say no**.

Risk guards and kill switches are that component. They sit *between* the strategy and the wire and they are the one part of the stack that must be correct when everything else is broken:

- **Risk guards** are per-action, always-on checks. They evaluate every order in the microseconds before it is serialised, and they *drop the order* if it violates a limit. They are fast, deterministic, and boringly simple — no model, no state machine beyond a token bucket.
- **Kill switches** are global, escalating, and stateful. When risk guards cannot save you (the strategy is misbehaving in a way no per-order rule anticipated), the kill switch **cancels everything, blocks new risk, and — at its final setting — flattens the book and disconnects.**

Three design principles, each a first principle:

1. **The guard must not be part of the strategy.** It must run in the same process but be unreachable from strategy code and unconfigurable at runtime by the strategy. If a strategy can turn off its own limit, the limit is decoration.
2. **Every limit must be expressible as a closed-form inequality on observable state.** No forecast, no model, no judgement. A guard that needs to think is a guard that can be talked out of it.
3. **The kill switch must have a bounded, pre-tested, *bounded-time* path to flat.** "We can always flatten manually" is false exactly when it matters (the market is fast and everyone else is also trying to cancel).

> **The one-sentence essence.** "Every order passes through an ordering of cheap deterministic checks (size, notional, price, rate, exposure) that either approves it or drops it; and above those sits a state machine that escalates RUNNING → WARNING → SOFT_HALT → HARD_HALT on realised loss, and that, at HARD_HALT, cancels all resting orders, blocks all new risk, flattens, and disconnects — with manual, cool-down-gated recovery."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Pre-trade guard predicates (order-level)

For an order $(q, P, \text{side})$ in instrument $i$ with current mid $P^{\text{nbbo}}$ and current signed position $q_i$:

$$
\begin{aligned}
&\text{(G1) fat-finger size:} && q \le Q_{\max}[i],\\
&\text{(G2) order notional:} && P\,q \le \mathcal{N}_{\max},\\
&\text{(G3) price collar:} && \left|\frac{P-P^{\text{nbbo}}}{P^{\text{nbbo}}}\right| \le \theta,\\
&\text{(G4) post-trade position:} && \big|q_i + \operatorname{sgn}(\text{side})\,q\big| \le \bar q_i,\\
&\text{(G5) post-trade gross:} && \sum_j \big|q_j + \delta_j q\big| P_j \le G_{\max}.
\end{aligned}
$$

Crucially, G4/G5 check the **post-trade** state, not the current state: a guard that checks the pre-trade position will happily approve the order that breaks the limit (the classic off-by-one in pre-trade risk).

#### 2.2 Token-bucket rate limiting

A token bucket $(B, R)$ — capacity $B$ tokens, refill rate $R$ tokens/second — satisfies, at time $t$ since the last refill,

$$b_t = \min\big(B,\; b_{t^-} + R\,\Delta t\big),\qquad \text{approve iff } b_t \ge 1,\ \text{then } b_t \leftarrow b_t - 1.$$

Its properties are what make it the right primitive for market access:

- **Steady-state rate $\le R$**, with the ability to burst up to $B$ — which matches how exchanges actually penalise you (bursts are free, sustained excess is not).
- **Bounded memory**: two numbers, so it can live in the hot path for nanoseconds.

The alternative, a sliding window counter, needs $O(R\,W)$ state and is far more expensive at wire speed. $B$ is chosen as your burst tolerance (e.g. 4–10 messages) and $R$ as the exchange's message-rate allowance, typically set to a *fraction* of the limit so the guard fires well before the venue's own throttle (which is punitive and often disconnects the session).

#### 2.3 The kill-switch escalation ladder

Let $L_t$ be the realised daily loss (positive = loss) and $L_{\max}$ the daily loss budget. The four states and their triggers:

$$
\begin{aligned}
\text{RUNNING} &\to \text{WARNING} &&\text{when } L_t \ge \alpha\,L_{\max}\quad(\alpha\approx0.6),\\
\text{WARNING} &\to \text{RUNNING} &&\text{when } L_t < \beta\,L_{\max}\quad(\beta\approx0.4,\ \text{hysteresis}),\\
\text{any} &\to \text{SOFT\_HALT} &&\text{when } L_t \ge L_{\max}\ \ \text{or rate} \ge 3\times\text{historical max} \ \text{or heartbeat loss},\\
\text{any} &\to \text{HARD\_HALT} &&\text{when } L_t \ge \gamma\,L_{\max}\ (\gamma\approx 2)\ \text{or flatten timeout}.
\end{aligned}
$$

The **hysteresis gap $\alpha>\beta$ is not optional.** Without it, a P&L series oscillating around the threshold produces a state machine that flickers, and a flickering guard drops good orders and blocks recovery. Every production state machine needs dead-band.

**Semantics of each state** (the actions are as important as the triggers):

| State | New orders | Resting orders | Connectivity |
|---|---|---|---|
| RUNNING | allowed (subject to G1–G5) | untouched | up |
| WARNING | allowed, alerts fired | untouched | up |
| SOFT_HALT | **rejected** | **cancel all** | up (so cancels reach the venue) |
| HARD_HALT | **rejected** | **cancel all** | **flatten, then disconnect** |

Note the ordering constraint that makes the ladder work: SOFT_HALT keeps the connection *up* precisely so the cancels can be delivered; only HARD_HALT (all else failed) drops the wire. A kill switch that disconnects before it finishes cancelling leaves the resting orders live at the venue — the classic "I killed it and it kept trading" bug.

#### 2.4 Latency budget for the guard

The whole guard must fit inside the tick-to-trade budget (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]]); the canonical figure is **~0.25 µs of a 2.00 µs budget (~12.5%)** for G1–G5 plus the token bucket. That is the price of the only code that protects you, and it is cheap.

---

### 3. Computational Implementation — the guard + kill-switch state machine

Stdlib only, no wall clock: the "clock" is an explicit `t` in the event stream, so the trace is exactly reproducible. The class implements G1–G3, the token bucket, and the four-state ladder with hysteresis and manual-reset-only recovery from HARD_HALT.

```python
# --- kill-switch state machine + pre-trade guard (stdlib only, no wall clock) ---
RUNNING, WARNING, SOFT_HALT, HARD_HALT = "RUNNING", "WARNING", "SOFT_HALT", "HARD_HALT"

class Guard:
    """Pre-trade limits + a 4-state kill switch driven by an explicit clock."""
    def __init__(self, qty_cap, notional_cap, loss_cap, rate, burst):
        self.qty_cap, self.notional_cap, self.loss_cap = qty_cap, notional_cap, loss_cap
        self.rate, self.burst = rate, burst          # tokens/sec, bucket capacity
        self.tokens, self.t_last = burst, 0.0
        self.state, self.pnl = RUNNING, 0.0
    def _refill(self, t):
        self.tokens = min(self.burst, self.tokens + (t - self.t_last) * self.rate)
        self.t_last = t
    def check(self, t, px, qty, mid, realized):
        self._refill(t); self.pnl = realized
        # --- state transitions ---
        if self.pnl <= -2.0 * self.loss_cap:
            self.state = HARD_HALT
        elif self.pnl <= -self.loss_cap and self.state != HARD_HALT:
            self.state = SOFT_HALT
        elif self.state == RUNNING and self.pnl <= -0.6 * self.loss_cap:
            self.state = WARNING
        elif self.state == WARNING and self.pnl > -0.4 * self.loss_cap:
            self.state = RUNNING
        # --- gates, in order ---
        if self.state == HARD_HALT:
            return "REJECT", "HARD_HALT: cancel-all + flatten + disconnect"
        if self.state == SOFT_HALT:
            return "REJECT", "SOFT_HALT: cancel-all, no new risk"
        if qty > self.qty_cap:
            return "REJECT", f"max order qty {qty}>{self.qty_cap}"
        if px * qty > self.notional_cap:
            return "REJECT", f"max notional {px*qty:,.0f}>{self.notional_cap:,.0f}"
        if abs(px - mid) / mid > 0.03:
            return "REJECT", f"price collar {100*abs(px-mid)/mid:.2f}%>3%"
        if self.tokens < 1.0:
            return "REJECT", "rate limit: token bucket empty"
        self.tokens -= 1.0
        return "APPROVE", "ok"

g = Guard(qty_cap=5_000, notional_cap=100_000.0, loss_cap=25_000.0, rate=4.0, burst=4.0)
scenario = [  # (t, px, qty, mid, realized pnl)
    (0.00, 150.00, 200, 150.05,      0.0),
    (0.10, 150.00, 200, 150.05,      0.0),   # orders at t=0 and t=0.1 -> bucket nearly drained
    (0.10, 150.00, 200, 150.05,      0.0),
    (0.50, 150.00, 9000, 150.05,     0.0),   # fat finger
    (1.00, 160.00, 200, 150.05,      0.0),   # price collar
    (2.00, 150.00, 200, 150.05, -16_000.0),  # WARNING threshold
    (3.00, 150.00, 200, 150.05, -26_000.0),  # SOFT_HALT
    (4.00, 150.00, 200, 150.05, -55_000.0),  # HARD_HALT
    (5.00, 150.00,  10, 150.05, -55_000.0),  # stays hard-halted: manual reset only
]
print(f"{'t':>5s} {'state':>10s} {'pnl':>9s}  verdict  reason")
for t, px, qty, mid, pnl in scenario:
    v, why = g.check(t, px, qty, mid, pnl)
    print(f"{t:5.2f} {g.state:>10s} {pnl:9,.0f}  {v:<7s}  {why}")
```
```
    t      state       pnl  verdict  reason
 0.00    RUNNING         0  APPROVE  ok
 0.10    RUNNING         0  APPROVE  ok
 0.10    RUNNING         0  APPROVE  ok
 0.50    RUNNING         0  REJECT   max order qty 9000>5000
 1.00    RUNNING         0  REJECT   price collar 6.63%>3%
 2.00    WARNING   -16,000  APPROVE  ok
 3.00  SOFT_HALT   -26,000  REJECT   SOFT_HALT: cancel-all, no new risk
 4.00  HARD_HALT   -55,000  REJECT   HARD_HALT: cancel-all + flatten + disconnect
 5.00  HARD_HALT   -55,000  REJECT   HARD_HALT: cancel-all + flatten + disconnect
```
Read the trace as the guard's lifeline: the fat-finger and collar orders are rejected while the system is healthy and fully trading (they were never risk to the book); then loss pulls the ladder through WARNING (still trading, humans alerted), SOFT_HALT (orders refused, everything cancelled), and HARD_HALT (**sticky**: at $t=5.00$, with P&L recovered in principle, the guard still refuses — a good strategy cannot talk the kill switch back down; only an operator can).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **In-flight orders during a kill.** Setting a flag in memory does nothing to the orders already sitting in the socket buffer or the exchange's matching engine. A kill switch is only real once it (a) stops *issuing*, (b) *cancels* what is out, and (c) waits for cancel acknowledgements. Without (b)/(c) you have a paused strategy and a live book — the Knight Capital shape.
2. **Cancel-on-disconnect absent.** If the session dies while resting quotes are live, an exchange without COD leaves those quotes exposed to the next price move. The guard must therefore assume *any* disconnect could leave a position, and reconciliation on reconnect must be mandatory — never "resume from in-memory state."
3. **Guards that check pre-trade state.** G4/G5 applied to the *current* position approve the very order that breaches the limit. Always evaluate the hypothetic post-trade book.
4. **Limits that can be reconfigured by the strategy.** A limit set from a config file the strategy can write, or from a runtime API the strategy can call, is not a limit. Limits belong to the risk component, versioned with the deployment.
5. **No hysteresis.** Without the dead-band, a P&L series hovering at the threshold produces a flickering state machine that blocks recovery orders and produces alert noise (see [[pillars/08-quantitative-development/production-trading-systems/03-monitoring-and-alerting|03 · Monitoring & Alerting]] on alert fatigue).
6. **Flatten without a plan.** "Flatten" during a fast market with a limit order at the mid does not flatten; it posts and waits. The runbook must specify the *aggressive* order type, the max slippage accepted, and what to do when the flatten order is partially filled and the venue is closed.
7. **Dead-man's switch.** The kill-switch process itself must be watched by an independent watchdog (and the watchdog by a third thing), or its death is indistinguishable from calm.

---

### 5. Canonical Literature & Study References

- **SEC Rule 15c3-5** — *Risk Management Controls for Brokers or Dealers with Market Access* — the regulatory source for pre-trade risk controls (fat-finger, notional, rate, and the "direct and exclusive" control obligation).
- **U.S. SEC**, *In the Matter of Knight Capital Americas LLC* (Release 34-70694, 2013) — the canonical incident record; read it for the exact control gaps, not just the headline.
- **Narang**, *Inside the Black Box*, 2nd ed. — the risk engine as a first-class component of the trading system.
- **NautilusTrader — Official Documentation** (nautilustrader.io) — a live engine's `RiskEngine` with pre-trade checks and trading-state (active/halted) semantics: a concrete, inspectable model.
- **Beyer et al.**, *Site Reliability Engineering* (O'Reilly, 2016) — Ch 13–14 on emergency response and the "fail safe" design principle.
- **Cartea, Jaimungal & Penalva**, *Algorithmic and High-Frequency Trading* — Ch 1–2 (market access, order types) for what the guard is protecting the venue-side state machine from.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/production-trading-systems/03-monitoring-and-alerting|03 · Monitoring & Alerting]] · Hub: [[pillars/08-quantitative-development/production-trading-systems/index|Index Hub]]
- Next: [[pillars/08-quantitative-development/production-trading-systems/05-failure-modes-and-practice|05 · Failure Modes]] (what happens when the guard is also insufficient) · [[pillars/08-quantitative-development/production-trading-systems/06-advanced-extensions|06 · Advanced Extensions]] (kill switches at cluster scale)
- Related flat page (superseded thematically by this folder): [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]]
- Related: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] (the guard's ~0.25 µs slice of the budget) · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|FIX · Order Lifecycle]] (cancel semantics, COD)
- Cross-pillar: [[pillars/04-quantitative-risk/index|Quantitative Risk Management]] · [[pillars/04-quantitative-risk/operational-risk/index|Operational Risk]] (the incident taxonomy this page defends against)
