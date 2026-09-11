---
title: "02 - The Tick-to-Trade Pipeline: Stages, Pipelining, and Wire Time"
tags:
  - pillar-algorithmic-hft
  - fpga
  - tick-to-trade
  - pipelining
  - latency
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/01-from-zero-intuition|01 · From Zero]] and [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]].

---

### 1. Intuition & Practical Objective

Tick-to-trade is a **pipeline**: a market-data packet enters at one end and an order packet leaves at the other, through a fixed sequence of stages. This page names the stages, gives the latency and throughput of each, and shows why **pipelining is the trick that lets a 312.5 MHz FPGA keep up with a 100 Gbps wire** even though its clock is slower than a CPU's.

The pipeline, wire to wire:

1. **PHY / MAC** — the SFP+ transceiver deserializes the optical bitstream; the MAC strips the frame header. Latency ≈ 20–40 ns; the FPGA sees bits, not sockets.
2. **Feed parser (state machine in silicon)** — decodes NASDAQ ITCH 5.0 or CME MDP 3.0 by walking a fixed byte-offset state machine, *without buffering the whole packet*. Latency ≈ 10 ns; a software parser needs ~200 ns because it reads struct fields from memory.
3. **Hardware book builder** — applies the update to top-of-book registers held in on-chip Block RAM (BRAM). Latency ≈ 5 ns.
4. **Trigger matrix** — hardwired combinational logic: `if bid > threshold then fire`. Latency ≈ 10 ns in a single pipeline stage.
5. **Order injector** — pre-computed checksums, the OUCH/FIX frame is written to the TX FIFO and pushed straight to the transceiver. Latency ≈ 20 ns.

Total ≈ 65 ns. The same five jobs in kernel-bypass software cost ≈ 1,200 ns, because each one is a *loop over memory* rather than *wire*.

Three "aha"s:

1. **Latency is the sum of stages; throughput is the slowest stage.** These are *different* quantities and the confusion between them causes most bad architecture.
2. **Pipelining multiplies throughput at constant latency.** $S$ stages running concurrently process $S$ packets at once; end-to-end latency stays $S\cdot L$, but you emit one packet every $L$ instead of every $S\cdot L$. This is how a 312.5 MHz chip (3.2 ns/tick) feeds a 100 GbE port.
3. **The wire itself is a stage you cannot optimise away.** Serialization is $8B/\text{rate}$; a 1,500-byte MTU frame takes 1,200 ns to clock out at 10GbE. If your frames are big, framing *is* your latency.

> **Why it matters.** Every realistic tick-to-trade number is a sum over these stages. If you cannot point at the dominant stage in *your* pipeline, you cannot decide where to spend — and you will spend it in the wrong place.

---

### 2. Mathematical Ground Truth & Derivations

**Pipelined latency and throughput.** For $S$ stages each of processing time $L$:

$$
T_{\text{lat,pipe}} = S\cdot L \quad(\text{latency is unchanged by pipelining}),\qquad
\Theta_{\text{pipe}} = \frac{1}{L}\ \frac{\text{packets}}{\text{ns}},
$$

whereas a serial (non-overlapping) implementation has

$$
\Theta_{\text{ser}} = \frac{1}{S\cdot L} = \frac{1}{S}\,\Theta_{\text{pipe}}.
$$

So pipelining gives an **$S\times$ throughput gain at zero latency cost** — the single most important fact in hardware feed handling. A serial pipeline is *unstable* whenever the arrival rate $\lambda > 1/(SL)$; its queue then grows without bound (Little's law below), which is why the serial numbers in §3 explode.

**Wire serialization.** A frame of $B$ bytes on a link of rate $R$ (bits/ns) occupies the wire for

$$
t_{\text{wire}} = \frac{8B}{R}.
$$

With the standard 84-byte minimum frame (64 B frame + 8 B preamble/SFD + 12 B inter-frame gap): 67.20 ns at 10GbE, 26.88 ns at 25GbE, 6.72 ns at 100GbE. The corresponding **line-rate packet ceilings** are $R/8B$: 14.88, 37.20, and 148.81 M pkt/s.

**Little's law (buffering).** For a stable system, the mean number in flight is

$$
N = \lambda\,T.
$$

At line rate 14.88 M pkt/s with $T = 30$ ns, $N = 0.45$ packets — **less than one packet of buffering is needed**. This is the theoretical reason an FPGA can hold its entire book and pipeline in on-chip BRAM and why its queueing delay is effectively zero.

**Single-cycle trigger.** At $f = 312.5$ MHz, one clock tick is $1/f = 3.2$ ns. The comparator-plus-register logic fits in a single tick (3.2 ns); with its pipeline registers the trigger stage's end-to-end latency is ~10 ns — *deterministic*, not "usually fast."

---

### 3. Computational Implementation — pipelining, wire time, Little's law

Stdlib only. A deterministic discrete-event simulation runs the same 5-stage parser serially and pipelined, then we tabulate wire serialization and in-flight occupancy.

```python
def simulate(pipelined, S, L, interval, n):
    free = [0.0]*(S if pipelined else 1)
    lat = []; done = 0.0
    for i in range(n):
        a = i*interval; s = a
        if pipelined:
            for k in range(S):
                start = max(s, free[k]); fin = start+L; free[k] = fin; s = fin
            lat.append(s-a); done = s
        else:
            start = max(a, free[0]); fin = start+S*L; free[0] = fin
            lat.append(fin-a); done = fin
    return sum(lat)/n, n/done

S, L, interval, n = 5, 4.0, 6.0, 2000
print(f"5-stage parser, stage latency L = {L} ns, packet arrival every {interval} ns, {n} packets")
for mode, pl in (("serial   ", False), ("pipelined", True)):
    avg, thr = simulate(pl, S, L, interval, n)
    print(f"  {mode}: mean latency = {avg:8.2f} ns | throughput = {thr*1000:7.1f} M pkt/s ({thr:.4f} pkt/ns)")

print("\nwire serialization time (8*bytes / line-rate):")
for rate, name in ((10, "10GbE"), (25, "25GbE"), (100, "100GbE")):
    row = []
    for size, label in ((84, "min-frame 84B"), (256, "ITCH msg 256B"), (1500, "MTU 1500B")):
        row.append(f"{label}: {8*size/rate:7.2f} ns")
    print(f"  {name:6s} " + " | ".join(row))

print("\nLittle's law  N = lambda * T  (in-flight packets):")
for lam, T in ((10e6, 20e-9), (14.88e6, 30e-9), (1e6, 1000e-9)):
    print(f"  lambda = {lam/1e6:6.2f} M pkt/s, T = {T*1e9:7.1f} ns -> N = {lam*T:6.2f} in flight")
```
```
5-stage parser, stage latency L = 4.0 ns, packet arrival every 6.0 ns, 2000 packets
  serial   : mean latency = 14013.00 ns | throughput =    50.0 M pkt/s (0.0500 pkt/ns)
  pipelined: mean latency =    20.00 ns | throughput =   166.5 M pkt/s (0.1665 pkt/ns)

wire serialization time (8*bytes / line-rate):
  10GbE  min-frame 84B:   67.20 ns | ITCH msg 256B:  204.80 ns | MTU 1500B: 1200.00 ns
  25GbE  min-frame 84B:   26.88 ns | ITCH msg 256B:   81.92 ns | MTU 1500B:  480.00 ns
  100GbE min-frame 84B:    6.72 ns | ITCH msg 256B:   20.48 ns | MTU 1500B:  120.00 ns

Little's law  N = lambda * T  (in-flight packets):
  lambda =  10.00 M pkt/s, T =    20.0 ns -> N =   0.20 in flight
  lambda =  14.88 M pkt/s, T =    30.0 ns -> N =   0.45 in flight
  lambda =   1.00 M pkt/s, T =  1000.0 ns -> N =   1.00 in flight
```

Three lessons in the numbers. **(i)** The pipelined parser holds **20.00 ns** latency (exactly $S\cdot L$) but pushes **166.5 M pkt/s**, while the serial version collapses to **50.0 M pkt/s** ($1/(SL)$) and its *mean latency explodes to 14,013 ns* because arrivals (every 6 ns) outrun its 20 ns service time — the queue grows without bound. Same hardware, same stages; the only difference is overlap. **(ii)** Wire time is not a rounding error: a 1,500-byte frame costs **1,200 ns** of wire at 10GbE — larger than an entire FPGA pipeline. Small frames and fast links are a latency feature. **(iii)** Little's law says line-rate FPGA needs **$N=0.45$** packets of buffer, so on-chip BRAM is ample and queueing delay is nil.

For reference, the same trigger stage as silicon — one clock tick, deterministic:

```verilog
module tick_trigger (          // one pipeline stage @ 312.5 MHz = 3.2 ns
    input  wire        clk,
    input  wire [31:0] tick_price,
    input  wire [31:0] threshold,
    input  wire        valid,
    output reg         fire
);
    always @(posedge clk)
        fire <= valid & (tick_price >= threshold);
endmodule
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing latency with throughput.** Buying a 100 GbE NIC to "reduce latency" when your feed is 10 GbE and you are latency-sensitive is a throughput purchase that changes nothing. Latency is a *chain*; throughput is a *bottleneck*.
2. **Serial (non-pipelined) hot paths.** A software parser that decodes one packet fully before starting the next is $\Theta_{\text{ser}}$; under a burst it queues and its *latency* (not just its throughput) explodes, exactly as the simulation shows (14,013 ns). Overlap or die.
3. **Big frames / undersized links.** 1,200 ns of MTU wire time at 10GbE dominates a 65 ns FPGA. Optimise your framing and line rate before your logic.
4. **Buffering everything.** If your design must buffer whole packets before parsing, you have reintroduced the memory hierarchy the FPGA was supposed to eliminate — latency returns to software-like values.
5. **Ignoring the inter-frame gap.** Line-rate packet ceilings (14.88 M pkt/s at 10GbE) include preamble and IFG; capacity plans that assume 64 B payloads will be ~30% optimistic.

---

### 5. Canonical Literature & Study References

- **Nasdaq** — *TotalView-ITCH 5.0 Specification*, message formats and the software/FPGA decode variants the parser must implement.
- **Leber, Geib & Litz** (FPL 2011) — the FPL proof-of-concept's stage-by-stage pipeline; the direct ancestor of the five stages above.
- **De Schryver (ed.)** — *FPGA Based Accelerators for Financial Applications* (2015), HFT hardware-design chapters: pipeline depth, clock budgets, HLS mapping.
- **DPDK documentation** — the software pipeline (RX rings, burst sizes, prefetch) this page's numbers are benchmarked against.
- **Hasbrouck & Saar** (2013), "Low-latency trading," *JFM* 16(4) — the empirical order-cancellation rates a pipeline must satisfy.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/01-from-zero-intuition|01 · From Zero]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/03-fpga-vs-cpu-vs-gpu|03 · FPGA vs CPU vs GPU]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass & Networking]]
- Software counterpart: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]]
- Why the order matters: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
