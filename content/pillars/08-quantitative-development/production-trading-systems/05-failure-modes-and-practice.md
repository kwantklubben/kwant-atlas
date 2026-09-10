---
title: "05 - Failure Modes & Practice: Reconciliation, Incidents & Post-Mortems"
tags:
  - pillar-quant-dev
  - production-trading-systems
  - failure-modes
  - reconciliation
  - incident-response
  - post-mortem
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/production-trading-systems/04-risk-guards-and-kill-switches|04 · Risk Guards & Kill Switches]] and [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/03-session-management|FIX · Session Management]].

---

### 1. Intuition & Practical Objective

The guards of [[pillars/08-quantitative-development/production-trading-systems/04-risk-guards-and-kill-switches|04]] defend against *anticipated* failure: they reject orders that violate a rule you wrote in advance. This page is about the other kind — the failures nobody wrote a rule for, which are, by construction, the ones that cause the largest losses. Three archetypes recur in every post-mortem archive:

1. **Runaway orders.** A retry loop, an unhandled state, or a stale signal file causes the system to emit orders *without bound*. This is the Knight Capital mechanism and it is the reason rate limits and kill switches exist.
2. **Stale positions.** Your internal book diverges from the venue's because a fill message was dropped, a cancel was mis-acknowledged, or a session died mid-order. From that instant, **every risk computation you perform is on a fiction** — your limits are enforced against a book that does not exist.
3. **Silent failures.** The monitor that quietly stopped monitoring; the reconciliation job that has been erroring for three days; the alert that fires into a channel nobody reads. A control that fails without announcing itself is the deepest failure mode here, because it removes your ability to *know* you are exposed.

The practice that ties these together is **reconciliation**: the periodic comparison of your internal state against an external source of truth (the broker/clearing feed, the venue's drop copy), where any difference is a *break* that must be explained or escalated. Reconciliation is the only defence against stale positions, and its being-monitored is the only defence against silent failure.

> **The one-sentence essence.** "You cannot know your risk from your own book alone: periodically compare your internal positions and cash to an independent (broker/clearing) record, classify every difference as *timing* (explained by an in-flight trade) or *real* (unexplained, gates trading), and treat the health of the reconciliation job itself as a first-class monitored signal."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Position reconciliation

Let $q_i^{\text{int}}$ be the internal signed position in instrument $i$ as of a common as-of time $T$, and $q_i^{\text{ext}}$ the corresponding position from the external (clearing / drop-copy / broker) record. Define the **break**

$$b_i = q_i^{\text{int}} - q_i^{\text{ext}}.$$

The reconciliation rule is a tolerance test per instrument:

$$\text{break}_i \iff |b_i| > \epsilon_{\text{pos}},$$

but the *classification* is what makes it useful. Let $\mathcal{P}_i$ be the net quantity of trades in $i$ that the internal system knows about but which are legitimately not yet reflected externally (in-flight / unsettled / post-cutoff). Then

$$
\text{break}_i\ \text{is}\
\begin{cases}
\text{TIMING}, & b_i = P_i \ \text{and the trade is in }\mathcal{P}_i,\\[2pt]
\text{REAL}, & \text{otherwise.}
\end{cases}
$$

A **timing break** is a false alarm caused by as-of mismatch — the most common cause of reconciliation noise, and the reason the as-of timestamp must be part of the comparison, not an afterthought. A **real break** is an unexplained divergence: a lost fill, a broken cancel, a duplicated message, or (worst case) unauthorised activity.

Aggregate sanity checks catch what per-instrument tolerances let through:

$$\text{(A1) unexplained net: }\sum_i b_i \neq 0 \ \Rightarrow \text{investigate}, \qquad
\text{(A2) breaks allowed at most } K \text{ instruments}.$$

(A1) matters because a pair of offsetting breaks can each sit inside a per-name tolerance while hiding a genuine problem.

#### 2.2 Cash reconciliation

Cash is the second book that must agree. Starting from the previous day's reconciled cash $C_{-1}$, the internal expectation for today's cash is

$$C^{\text{int}}_{\text{expected}} = C_{-1} - \sum_{i} \big(P_i^{\text{fill}} q_i^{\text{fill}}\big) - \text{fees} + \text{financing} \pm \text{corporate actions},$$

where the sum is over signed fills (buys negative cash, sells positive), fees are commissions/venue fees, and financing is margin/borrow. The residual is

$$r = C^{\text{ext}} - C^{\text{int}}_{\text{expected}},\qquad \text{break} \iff |r| > \epsilon_{\text{cash}}.$$

The cash residual is a **powerful, low-dimensional check**: positions can look right while a fee is double-charged, a corporate action (split, dividend, merger) is unaccounted, or a synthetic fill is fabricated. A cash break with clean positions almost always means *fees, financing, or corporate actions* — and a position break with clean cash usually means *timing*.

#### 2.3 Break rate as a monitored statistic, and the control on the control

Let $N$ be the number of instruments reconciled and $K_t$ the number of real breaks at reconciliation $t$. Under a healthy system $K_t=0$ almost surely, so the useful monitored quantity is not $\mathbb{E}[K_t]$ but the **age of the last clean reconciliation** $A_t = t - t_{\text{last clean}}$ and the *fraction of reconciliations that completed*,

$$\rho = \frac{\#\{\text{reconciliations completed}\}}{\#\{\text{reconciliations attempted}\}}.$$

$\rho<1$ means the control itself is broken — a **silent failure** — and it is *the* signature to alert on. Concretely: an alert on `last_successful_reconciliation_age > 2 × interval` fires on the *absence* of the signal, which is the only way to catch a monitor that stopped monitoring.

#### 2.4 Break-age bounds the exposure

If a stale position goes undetected for $D$ minutes and the market moves at volatility $\sigma_{\text{ann}}$, the size of the error in your computed risk is on the order of

$$\Delta_{\text{risk}} \sim \sigma_{\text{ann}}\sqrt{\frac{D}{T_{\text{year}}}}\cdot Q_{\text{stale}}\cdot P,$$

i.e. **the undetected time $D$ directly multiplies your exposure error.** Reconciliation frequency is therefore a *risk* parameter: reconciling every 15 minutes instead of hourly cuts the worst-case blind window by $4\times$.

---

### 3. Computational Implementation — the reconciliation algorithm

Stdlib only. The routine reconciles positions across the union of instruments, classifies each break (MATCHED / TIMING / REAL) using a known in-flight ledger, and checks the cash residual against an expectation built from the day's signed fills. This is the exact shape of the end-of-day (and intraday) control.

```python
# --- end-of-day reconciliation: positions + cash (stdlib only) ---
from collections import defaultdict

internal = {"AAPL": 1200, "MSFT": -800, "TSLA": 450}   # our book, as of T
external = {"AAPL": 1000, "MSFT": -800, "TSLA": 400}   # clearing feed, as of T
pending  = {"AAPL": 200}                               # fills not yet in the feed
cash_broker, cash_expected, tol_pos, tol_cash = 1_000_000.0, 1_000_000.0, 0, 1.0

print("Position recon (as of T):")
breaks = []
for sym in sorted(set(internal) | set(external)):
    b = internal.get(sym, 0) - external.get(sym, 0)
    pend = pending.get(sym, 0)
    if abs(b) <= tol_pos:
        kind = "MATCHED"
    elif b == pend:
        kind = "TIMING (pending fill)"
    else:
        kind = "REAL BREAK"
        breaks.append((sym, b))
    print(f"  {sym:5s} internal={internal.get(sym,0):>6d} external={external.get(sym,0):>6d} "
          f"break={b:>+5d}  {kind}")

resid = cash_broker - cash_expected
print(f"\nCash recon: broker {cash_broker:,.2f} expected {cash_expected:,.2f} "
      f"residual {resid:+,.2f} -> {'MATCHED' if abs(resid) <= tol_cash else 'BREAK'}")
net_break = sum(b for _, b in breaks)
print(f"\nUnreconciled position units: {net_break:+d} across {len(breaks)} break(s)")
print("Gate: trading halts if any REAL BREAK or |cash residual| > tolerance")
```
```
Position recon (as of T):
  AAPL  internal=  1200 external=  1000 break= +200  TIMING (pending fill)
  MSFT  internal=  -800 external=  -800 break=   +0  MATCHED
  TSLA  internal=   450 external=   400 break=  +50  REAL BREAK

Cash recon: broker 1,000,000.00 expected 1,000,000.00 residual +0.00 -> MATCHED

Unreconciled position units: +50 across 1 break(s)
Gate: trading halts if any REAL BREAK or |cash residual| > tolerance
```
Read it as the discipline the whole page argues for: the AAPL difference is **explained by a known pending fill** and is therefore noise to be suppressed (alerting on it would be a false alarm — see [[pillars/08-quantitative-development/production-trading-systems/03-monitoring-and-alerting|03]]), while the TSLA $+50$ has **no explanation** and is a real break that, under the gate, halts trading until it is resolved. The cash book agreeing is what lets you localise the problem to positions rather than suspecting the whole ledger.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Silent failure — the reconciliation that stopped.** If $\rho<1$ and nobody alerts on it, you believe you are reconciled while you are blind. The alert must fire on the *absence* of a successful reconciliation (age since last clean run), never only on the presence of breaks.
2. **Timing breaks mistaken for real breaks.** Reconciling against a feed with a different cut-off produces a wall of spurious breaks, which trains operators to dismiss them. Always compare as-of the same timestamp and maintain an explicit in-flight ledger.
3. **Offsetting breaks inside tolerance.** A per-name tolerance of $\epsilon$ lets two instruments each drift by $\epsilon$ in opposite directions, hiding a breakout of aggregate exposure. Add the aggregate check (A1) and a break *count* limit (A2).
4. **Reconciliation as a batch afterthought.** Run it nightly and the blind window is a full day; run it intraday against the drop copy and it is minutes. Frequency is a risk parameter, and the exposure error scales as $\sqrt{D}$ in time (§2.4).
5. **Guards and reconciliation disagreeing.** If the guard enforces a limit against the internal book while the internal book is wrong, the guard is enforcing a fiction. Guards must be reconciled to, not trusted over, the external record.
6. **Incident response without a written runbook.** In a live incident, the person on call is stressed, half-informed, and under time pressure. Undocumented procedure is procedure executed wrongly. The runbook must be reachable from the alert, and must name the *first action* and the person who can authorise a flatten.
7. **Post-mortems that find a culprit instead of a cause.** "Operator error" is a description, not an explanation. The point of the post-mortem is to name the *missing control* that would have caught the error, and to add it — blameless, causal, and temporary-control-free (see [[pillars/04-quantitative-risk/operational-risk/index|Operational Risk]] for the loss-event taxonomy this maps onto).

---

### 5. Canonical Literature & Study References

- **SEC**, *Knight Capital Americas LLC* (Release 34-70694, 2013) — the canonical incident record; the control that was missing was, precisely, one that could halt the flow.
- **Beyer et al.**, *Site Reliability Engineering* (O'Reilly, 2016) — Ch 14–15 (managing incidents, emergency response), Ch 15 (post-mortem culture: blameless, learning-oriented).
- **Allspaw, John**, "Blameless PostMortems and a Just Culture" (Etsy Code as Craft, 2012) — the short, canonical articulation of cause-not-culprit.
- **Narang**, *Inside the Black Box*, 2nd ed. — the operational apparatus (reconciliation, trade matching, exception handling) of a real quant firm.
- **NautilusTrader — Official Documentation** (nautilustrader.io) — the engine's position/account state and its reconciliation-from-venue pattern.
- **BIS / BCBS**, *Principles for the Sound Management of Operational Risk* (2011) — reconciliation, segregation of duties, and control-monitoring as supervisory expectations; the regulatory frame for §2.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/production-trading-systems/04-risk-guards-and-kill-switches|04 · Risk Guards & Kill Switches]] · Hub: [[pillars/08-quantitative-development/production-trading-systems/index|Index Hub]]
- Next: [[pillars/08-quantitative-development/production-trading-systems/06-advanced-extensions|06 · Advanced Extensions]] (HA/failover; the reconciliation on reconnect)
- Related: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/05-failure-modes-and-practice|FIX · Failure Modes]] (session recovery and message loss) · [[pillars/08-quantitative-development/production-trading-systems/03-monitoring-and-alerting|03 · Monitoring & Alerting]] (how breaks become alerts)
- Cross-pillar: [[pillars/04-quantitative-risk/operational-risk/index|Operational Risk]] (loss-event taxonomy, frequency–severity) · [[pillars/04-quantitative-risk/index|Quantitative Risk Management]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]
- Base: [[foundations/numerical-methods/index|Numerical Methods]] (tolerances, floating-point comparison in reconciliation)
