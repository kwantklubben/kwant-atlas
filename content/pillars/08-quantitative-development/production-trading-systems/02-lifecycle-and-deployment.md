---
title: "02 - The Research-to-Production Lifecycle & Deployment"
tags:
  - pillar-quant-dev
  - production-trading-systems
  - lifecycle
  - canary
  - blue-green
  - deployment
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/production-trading-systems/01-from-zero-intuition|01 · From Zero]] and [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Event-Driven Backtesting Engines]].

---

### 1. Intuition & Practical Objective

A strategy does not "go live." It **graduates**, one gate at a time, and each gate exists to make a specific class of mistake expensive to pass rather than free. Deployment is the discipline that decides *how much capital a change is allowed to risk before it has earned more.*

The core asymmetry: **a code change carries no information about whether it is correct.** The developer believes it is; the developer is the least reliable witness. So the deployment system must convert "believe" into "have observed." That is what a canary is: you give the new build a *small* amount of real money and *watch*, and only increase exposure when the observed behaviour matches the predicted behaviour.

Two deployment patterns, in increasing order of safety and cost:

- **Blue-green:** two complete environments (blue = current, green = new). You bring green up cold, verify it, then switch 100% of traffic in one step. Rollback is a switch back. Simple, low-latency-to-deploy, but the *first instant of exposure is 100%* — you find out the build was bad at full size.
- **Canary:** route a small weight $w$ (1%, 5%, 25%…) to the new build and ramp. You find out the build is bad at 1% of the cost. This is the pattern trading systems should use, because the downside of a bad build is measured in money, not in user-visible errors.

> **The one-sentence essence.** "Deploy is a *risk decision*, not a technical event: the question is never 'does the new code work?' but 'how much money is exposed before we would notice it does not?' — so you ramp exposure (canary), define the metric that triggers rollback *before* deploying, and automate the rollback so it does not depend on a human being awake."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Exposure-hours: the quantity a rollout minimises

Model a bad build as producing a loss at rate $L$ (dollars per hour) whenever it is live at full traffic. If a rollout assigns traffic weight $w(t)\in[0,1]$ over a horizon $[0,T]$, the loss incurred is

$$\mathcal{L} = L\!\int_0^{T} w(t)\,dt = L \cdot \mathcal{E}, \qquad \mathcal{E} = \int_0^T w(t)\,dt \;\;(\text{exposure-hours}).$$

For a **big-bang** deploy, $w(t)=1$ until detection at $t=D$, so $\mathcal{E}=D$. For a **canary** with $K$ stages of weights $w_k$ held for $h_k$ hours,

$$\mathcal{E}_{\text{canary}} = \sum_{k=1}^{K} w_k h_k,$$

and the rollout **aborts** at the first stage where the cumulative loss exceeds the rollback threshold $\Theta$:

$$k^\* = \min\Big\{k : L\sum_{j\le k} w_j h_j \ge \Theta\Big\}.$$

The reduction factor $\mathcal{E}_{\text{big}}/\mathcal{E}_{\text{canary}}$ is the entire value proposition of the pattern, and it is *monotone* in how low the first weight is.

#### 2.2 The rollback-trigger design problem

The threshold $\Theta$ is a trade-off, not a constant. Roll back too eagerly and good deploys die to noise (high false-abort rate, release velocity collapses); too late and a bad deploy runs long. Under normal P&L noise with standard deviation $\sigma_\Delta$ per window and a rollback rule "abort if cumulative deviation $>k\sigma_\Delta$", the false-abort probability per window is $2(1-\Phi(k))$ — the same control-chart arithmetic as [[pillars/08-quantitative-development/production-trading-systems/03-monitoring-and-alerting|03 · Monitoring & Alerting]].

#### 2.3 Expected cost of a deploy programme

With per-deploy bad-build probability $p$, the expected loss per deploy is $p\,L\,\mathcal{E}$, and over $N$ deploys per year the annual expected loss is $p\,N\,L\,\mathcal{E}$. Note how the terms separate: **you control $N$ (release cadence), $\mathcal{E}$ (rollout pattern), and — only through testing — $p$.** Since the framework, engine, and strategy are all deployed through the same pipeline, $\mathcal{E}$ is the highest-leverage knob you own, and it is pure process.

#### 2.4 Blue-green vs canary

Blue-green is the $K=1$ special case: weights $w_1=1$, aborted at $h_1=D$. Canary dominates it on $\mathcal{E}$ whenever the first-stage weight is small, at the cost of a longer time-to-full-traffic and slightly higher state-complexity (two versions live simultaneously, so positions/P&L must be *attributable per version* — a bookkeeping burden the rollout creates).

---

### 3. Computational Implementation — the canary ramp with automatic rollback

Stdlib only, deterministic. The simulator ramps traffic $1\%\to5\%\to25\%\to100\%$ against a bad build, accumulates the loss at each stage, and trips an automatic rollback the moment the cumulative loss exceeds the threshold. It then compares the realised loss against the same bad build deployed big-bang.

```python
# --- canary vs big-bang: expected loss exposure of a bad deploy (stdlib only) ---
p_bad = 0.20                # probability that a given deploy is bad
loss_per_hour = 50_000.0    # loss rate while a bad build is live at 100% traffic
detect_hours = 2.0          # time to notice and abort at full exposure (big-bang)

big_bang_exposure = detect_hours * 1.0     # exposure-hours

stages = [(0.01, 0.5), (0.05, 0.5), (0.25, 0.5), (1.00, 0.5)]  # (weight, hours)
threshold = 5_000.0                        # loss that trips automatic rollback

print("Canary ramp, bad deploy (loss rate ${:,.0f}/h):".format(loss_per_hour))
cum = elapsed = 0.0
for w, h in stages:
    stage_loss = loss_per_hour * w * h
    cum += stage_loss; elapsed += h
    print(f"  {w*100:5.1f}% traffic for {h:.1f}h -> +${stage_loss:9,.0f} "
          f"cumulative ${cum:10,.0f}")
    if cum >= threshold:
        print(f"  -> AUTO-ROLLBACK at t={elapsed:.1f}h, loss ${cum:,.0f}")
        break

print(f"\nTime under a bad build: big-bang {big_bang_exposure:.2f} h vs canary {elapsed:.2f} h")
big_loss = loss_per_hour * big_bang_exposure
print(f"Realised loss:  big-bang ${big_loss:,.0f} vs canary ${cum:,.0f} "
      f"({big_loss/cum:.1f}x reduction)")
print(f"Expected loss per deploy: big-bang ${p_bad*big_loss:,.0f} "
      f"vs canary ${p_bad*cum:,.0f}")
```
```
Canary ramp, bad deploy (loss rate $50,000/h):
    1.0% traffic for 0.5h -> +$      250 cumulative $       250
    5.0% traffic for 0.5h -> +$    1,250 cumulative $     1,500
   25.0% traffic for 0.5h -> +$    6,250 cumulative $     7,750
  -> AUTO-ROLLBACK at t=1.5h, loss $7,750

Time under a bad build: big-bang 2.00 h vs canary 1.50 h
Realised loss:  big-bang $100,000 vs canary $7,750 (12.9x reduction)
Expected loss per deploy: big-bang $20,000 vs canary $1,550
```
The headline: **the same bug, the same detection speed, a $12.9\times$ difference in realised loss** — because the canary let the loss announce itself at 1% of exposure instead of 100%. Note also that the canary's `Time under a bad build` (1.50 h) is *shorter* than big-bang's (2.00 h) despite more stages, because the abort is automated and the ramp front-loads the cheap observation.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The canary that is not canaried.** Routing "10% of signals" while the strategy shares one position and one risk budget means the *risk* of the new build is already 100%. True canarying requires **separate capital, separate risk limits, and separate P&L attribution** per version — otherwise you have deployed the new build at full size and merely labelled it.
2. **Rollback that needs a human.** An automatic rollback bound to an automated metric (`cumulative loss > Θ`) fires in seconds; a rollback that pages a human fires in tens of minutes. If the trigger path includes a person, model it as $\Theta\to\infty$ for the purpose of $\mathcal{E}$.
3. **Deploy-time state drift.** Restarting the system resets in-memory state; if the strategy's state (position, working orders, VWAP accumulators) is not *recovered from the broker*, the new process starts believing it is flat. This is the deployment-flavoured version of [[pillars/08-quantitative-development/production-trading-systems/05-failure-modes-and-practice|05 · Failure Modes]]' stale-position bug.
4. **Configuration as an untracked dependency.** "The deploy was fine, somebody changed a limit." Version the *limits* with the code — a limit edited out-of-band is an unreviewed code change to the one component whose job is to say no.
5. **Promoting on P&L alone.** A canary that matches P&L but shows double the intended order rate is broken in a way that has not cost money *yet*. Gate promotion on the full metric set (rate, reject ratio, latency, reconciliation status), not just the bottom line.

---

### 5. Canonical Literature & Study References

- **Davey**, *Building Winning Algorithmic Trading Systems*, Ch 6–9 (walk-forward → paper → live; the gating discipline this page formalises).
- **Narang**, *Inside the Black Box*, 2nd ed., Ch 5–7 (the production pipeline and the operational apparatus around the alpha model).
- **Beyer et al.**, *Site Reliability Engineering* (O'Reilly, 2016), Ch 8 & 27 — release engineering, canarying, and the error-budget framing of rollout safety.
- **Humble & Farley**, *Continuous Delivery* (Addison-Wesley, 2010) — blue-green, deployment pipelines, and the principle that deploy and release should be separate events.
- **NautilusTrader — Official Documentation** (nautilustrader.io) — a real live runtime's separation of configuration, adapters, and risk engine, as the concrete instantiation of "deploy ≠ release".

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/production-trading-systems/01-from-zero-intuition|01 · From Zero]] · Hub: [[pillars/08-quantitative-development/production-trading-systems/index|Index Hub]]
- Next: [[pillars/08-quantitative-development/production-trading-systems/03-monitoring-and-alerting|03 · Monitoring & Alerting]] (the metrics that trigger rollback) · [[pillars/08-quantitative-development/production-trading-systems/05-failure-modes-and-practice|05 · Failure Modes]]
- Related: [[pillars/08-quantitative-development/production-trading-systems/04-risk-guards-and-kill-switches|04 · Risk Guards & Kill Switches]] (the last-line limit if the rollout trigger fails) · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/03-session-management|FIX · Session Management]] (connectivity during a rolling restart)
- Base: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
