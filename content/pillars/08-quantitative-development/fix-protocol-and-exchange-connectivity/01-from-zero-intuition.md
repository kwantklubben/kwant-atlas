---
title: "8.8.1 FIX From Zero"
tags:
  - pillar-quant-dev
  - fix-protocol
  - exchange-connectivity
  - intuition
  - tag-value
---

**Basic Prerequisites:** none - this page assumes no messaging background, only that you have seen a stock ticker.

---

### 1. Intuition & Practical Objective

This page builds the *why* of exchange connectivity with **no prior protocol knowledge**. The objective is one idea: **an order is a message, and the market is a conversation you must keep exactly in sync - not a form you fill in.**

Start with the dumbest question: *how does your computer actually tell an exchange "buy 100 shares of AAPL"?* There is no API call that reaches into the exchange's server. What happens is you open a **TCP connection**, and you and the exchange agree to exchange **text messages** in a rigid format called FIX. Each message is a list of `tag=value` pairs glued together by an invisible delimiter (the byte `0x01`, called SOH). That is the *entire* idea: a telegram, not a database write.

Three "aha"s, in order:

1. **The wire is text, and text has rules.** FIX is deliberately human-readable: `55=AAPL` means "symbol = AAPL", `54=1` means "side = buy". You can `print()` a FIX message and read it. That readability is *why* it won the industry - decades of traders debugging over telnet - and it is also its cost: ASCII is verbose compared to binary.

2. **A message is a state transition, not a command.** When you send `NewOrderSingle`, the order does not "happen"; you enter a *shared state* where the venue will send back `ExecutionReport` messages that acknowledge, fill, or reject it. Both sides now hold an obligation to agree on that state forever.

3. **Reliability is a contract you build on top of TCP.** TCP guarantees that the *bytes* arrive in order - if the connection stays up. But your process can crash and the connection can die. FIX therefore carries its **own** sequence numbers so that after a reconnect both sides can prove they saw the same messages, and re-send whatever was missed. TCP gives you bytes; FIX gives you *history*.

---

### 2. Mathematical Ground Truth & Derivations

**The message as a tuple of fields.** A FIX message is an ordered sequence of $(t_i, v_i)$ pairs - tag, value - terminated by the checksum:

$$
\text{msg} = \big[(t_1,v_1),\dots,(t_n,v_n)\big].
$$

Every wire byte is either **payload** (a tag, an `=`, or a value) or **framing** (the SOH separators plus the `=` signs). The framing overhead is the ratio of pure syntax to total length:

$$
\text{overhead} = \frac{\#\{=\} + \#\{\text{SOH}\}}{\text{len}(\text{msg})}.
$$

**Bandwidth.** A link carries messages at a rate fixed by capacity and message size. For capacity $C$ (bit/s) and size $s$ (bytes):

$$
R_{\max} = \frac{C}{8s}\ \text{msg/s}.
$$

**The conversation, in round trips.** A single order's life is at least a round trip (send order → ack) and usually two (send → ack → fill). If each leg costs $\bar t$, the *minimum* time from decision to confirmed fill is

$$
T_{\text{confirm}} \ge 2\bar t,
$$

which is why connectivity latency is measured in round trips, not in bandwidth. This is the number that colocation buys down (see [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Colocation & Clock Synchronization]]).

**The integrity check.** A FIX trailer adds a checksum so that a corrupted message is *detected*, not silently acted upon:

$$
\texttt{10} = \Big(\sum_i b_i\Big) \bmod 256,
$$

where $b_i$ are the ASCII byte values of everything from `8=FIX.4.2` up to (but not including) `10=`. Corruption that changes any byte changes the sum with high probability.

---

### 3. Computational Implementation - build, read, and size a FIX order

This is the "hello world" of the folder: hand-build a `NewOrderSingle`, verify its checksum, decode it back to a dict, and compute how many such messages fit on a link. Stdlib only.



Read it as the beginner's first two facts: **one order is ~165 bytes and ~20% of that is pure framing** (the `=` and SOH bytes carry no information), and a 1 Gbps link could carry **757,576 such messages per second**. Real trading systems are nowhere near their bandwidth limit - they are limited by **latency and by protocol semantics**, which is where the rest of this folder goes.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating the wire as reliable-permanent.** TCP only guarantees ordered bytes *while the connection lives*. A process crash or a NIC reset drops the session; without FIX's own sequence numbers you have no way to know what the venue saw. The protocol exists precisely because "the socket is up" is not "the counterparty and I agree."
2. **Trusting a message without its checksum.** If you decode by splitting on SOH and never verify `10`, a garbled byte becomes a garbled *order* (a flipped digit in `38=500` becomes `38=580`). Verify the trailer before acting - the next page makes this strict.
3. **Confusing bandwidth with latency.** The 757k msg/s figure tempts beginners to think speed is a bandwidth problem. It is not: the binding constraint is the **round-trip time**, so `T_confirm >= 2 t̄` - and that is what buys colocation, not fatter pipes.
4. **Reading SOH as printable.** SOH is `0x01`, an invisible control byte - dumping a FIX message to a terminal shows the values glued together. Always translate SOH to a visible marker (here, `|`) when debugging.

---

### 5. Canonical Literature & Study References

- **FIX Trading Community**, *FIX Protocol - Introduction & Session Layer* (fixtrading.org) - read the Introduction chapter first; it states the tag-value grammar and the session concept in prose, before you meet the message tables.
- **OnixS**, *FIX Dictionary & Protocol Reference* - the gentlest explanation of the session layer and the tag-value syntax for a first-time reader.
- **Donadio, Sebastien**, *Learn Algorithmic Trading* (Packt, 2019) - a zero-background tour that introduces FIX communication inside the broader algorithmic-trading build.

---

### 6. Connected Graph Bridges

- Continue: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/02-the-fix-protocol|02 · The FIX Protocol]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/index|Index Hub]]
- Context: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]] (what those tags select) · [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]] (the socket underneath)
