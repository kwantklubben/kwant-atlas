---
title: "FIX Protocol & Exchange Connectivity"
tags:
  - pillar-quant-dev
  - fix-protocol
  - order-routing
  - exchange-connectivity
---

**Basic Prerequisites:** Networking fundamentals (TCP/IP, sockets) and message serialization.

---

### 1. Intuition & Practical Objective

How do financial institutions talk to exchanges and prime brokers across the globe?

The **Financial Information eXchange (FIX) protocol** is the universal international messaging standard for automated trade communication. Whether sending orders to the New York Stock Exchange, routing swaps through Goldman Sachs, or clearing crypto derivatives, trade messages are encoded in standardized FIX specifications.

---

### 2. Mathematical Ground Truth & Derivations

#### Tag-Value Syntax
FIX messages are composed of ASCII `Tag=Value` pairs separated by the SOH (Start of Header, ASCII `0x01`) delimiter:
`8=FIX.4.29=10535=D49=BUY_SIDE56=EXCHANGE34=10152=20240101-09:30:00.12311=ORD_00155=AAPL54=138=10040=244=150.2510=182`

Key FIX Tags:
- `35`: Message Type (`D` = New Order Single, `8` = Execution Report, `F` = Cancel Request, `0` = Heartbeat).
- `54`: Side (`1` = Buy, `2` = Sell, `5` = Short).
- `44`: Limit Price.
- `38`: Order Quantity.
- `39`: OrdStatus (`0` = New, `1` = Partially Filled, `2` = Filled, `4` = Canceled, `8` = Rejected).

#### Session State Management & Recovery
FIX sessions maintain strict message sequence numbers (`Tag 34: MsgSeqNum`).
- If the trading engine disconnects and reconnects with sequence number $M > N+1$, the counterparty sends a **Resend Request (`35=2`)**.
- The engine must deterministically replay all missed message states from its persistent transaction log.

---

### 3. Computational Implementation

```python
def build_fix_new_order_single(seq_num: int, cl_ord_id: str, sym: str, 
                               side: int, qty: int, price: float) -> str:
    """
    Constructs a valid FIX 4.2 New Order Single (35=D) message with checksum.
    """
    soh = ""
    body = (
        f"35=D{soh}"
        f"49=KWANT_BOT{soh}"
        f"56=EXCHANGE{soh}"
        f"34={seq_num}{soh}"
        f"52=20240101-09:30:00.000{soh}"
        f"11={cl_ord_id}{soh}"
        f"55={sym}{soh}"
        f"54={side}{soh}"
        f"38={qty}{soh}"
        f"40=2{soh}" # Limit order
        f"44={price:.2f}{soh}"
    )
    header = f"8=FIX.4.2{soh}9={len(body)}{soh}"
    raw_msg = header + body
    
    # Calculate Tag 10 checksum (sum of all ASCII bytes modulo 256)
    checksum = sum(raw_msg.encode("ascii")) % 256
    final_msg = f"{raw_msg}10={checksum:03d}{soh}"
    return final_msg

# Example FIX order
fix_packet = build_fix_new_order_single(101, "ORD_42", "AAPL", side=1, qty=500, price=150.50)
print("Generated FIX Packet:\n", fix_packet.replace("", "|"))
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Sequence Number Desynchronization:**
   - *Failure:* Crashing without persisting the last sent `MsgSeqNum` to disk.
   - *Symptom:* The exchange rejects all incoming orders with `SequenceNumberTooLow`, freezing trading operations until manual operator intervention.

2. **TCP Nagle's Algorithm Buffering:**
   - *Failure:* Forgetting to set `TCP_NODELAY` on the FIX socket.
   - *Symptom:* The OS buffers small packets, delaying order transmission by 40 to 200 milliseconds.

---

### 5. Canonical Literature & Study References

- **FIX Protocol Technical Specifications**: *FIX 4.2 / 4.4 Protocol Standards*, FIX Trading Community.

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/08-quantitative-development/production-risk-guards-and-kill-switches|Risk Guards]]
- Bridges to: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Order Types]]
