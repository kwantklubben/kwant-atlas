---
title: "02 - The FIX Protocol: Message Structure & Common Messages"
tags:
  - pillar-quant-dev
  - fix-protocol
  - exchange-connectivity
  - message-structure
  - checksum
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/01-from-zero-intuition|01 · From Zero]] and basic ASCII/byte manipulation.

---

### 1. Intuition & Practical Objective

A FIX message is **structured, not free-form**. Every message is the same three-part envelope — **header, body, trailer** — with fixed rules about ordering, two integrity fields, and a small dictionary that turns a four-bit code like `35=D` into a full order instruction. The practical objective of this page is the **complete message reference**: the field-by-field structure, the exact `BodyLength`/`CheckSum` arithmetic, and a working **encoder + strict parser** that round-trips a `NewOrderSingle` and an `ExecutionReport` and *rejects* corruption.

The single most important idea is that the envelope is **self-validating**. The header carries `9 = BodyLength`, the trailer carries `10 = CheckSum`, and both are derived from the message itself — so any receiver can prove the message it decoded is the message that was sent, before it acts on a single order. This is what lets a FIX engine trust a byte stream it did not author.

---

### 2. Mathematical Ground Truth & Derivations

**The envelope.** Every FIX message is:

$$\underbrace{\texttt{8=BeginString \;| \; 9=BodyLength \;| \; 35=MsgType \;| \; \cdots}}_{\text{header}},\;
\underbrace{\texttt{body fields}}_{\text{the point}},\;
\underbrace{\texttt{10=CheckSum}}_{\text{trailer}}.$$

Ordering is *normative*: `8` is always first, `9` second, `35` third, `10` last. Violating it is a protocol error, not a style choice.

**BodyLength (tag 9).** Let the message be the byte string $M$. With `B` the index just after the SOH terminating the `9` field, and `E` the index of the first byte of the `10` field:

$$\texttt{9} = E - B \quad\text{(in bytes, }\text{not characters — FIX is ASCII, so they coincide).}$$

In words: `9` counts **everything from after the `9` field up to and including the SOH immediately before `10=`**. It excludes header fields `8` and `9` and excludes the trailer.

**CheckSum (tag 10).** Sum every ASCII byte from `8=` through the SOH that precedes `10=`, take it modulo 256, and render it as three zero-padded decimal digits:

$$\texttt{10} = \Big(\sum_{i \in [0,E)} b_i\Big) \bmod 256,\qquad \texttt{10} = \text{fmt}(c, \text{“03d”}),\quad \text{so } \texttt{10}=007\ \text{not}\ \texttt{7}.$$

**Integrity properties.** A single flipped bit changes the byte sum by at most $\pm 128$ (well within the mod-256 range), so a corrupted message almost always yields a mismatch — *detection*, not correction. Two independent checks (length and checksum) mean an attacker or a bit-flip must satisfy *both*, which is why a strict parser validates in order: structure → `BeginString` → `BodyLength` → `CheckSum`.

**Common message bodies (the ones you will actually send/receive).**

| `35` | Message | Required/typical body tags |
|---|---|---|
| `D` | NewOrderSingle | `11` ClOrdID, `55` Symbol, `54` Side, `38` OrderQty, `40` OrdType, `44` Price (limit), `59` TIF, `60` TransactTime |
| `8` | ExecutionReport | `37` OrderID, `11` ClOrdID, `17` ExecID, `150` ExecType, `39` OrdStatus, `55`, `54`, `38`, `32` LastQty, `31` LastPx, `151` LeavesQty, `14` CumQty, `6` AvgPx |
| `F` | OrderCancelRequest | `41` OrigClOrdID, `11` ClOrdID, `55`, `54`, `38` |
| `G` | OrderCancelReplaceRequest | `41`, `11`, new `38`/`44` — the *replace* |
| `V` | MarketDataRequest | `262` MDReqID, `263` SubscriptionRequestType, `55` Symbol, `267` NoMDEntryTypes |
| `A` | Logon | `98` EncryptMethod, `108` HeartBtInt |
| `2` | ResendRequest | `7` BeginSeqNo, `16` EndSeqNo |
| `4` | SequenceReset | `123` GapFillFlag, `36` NewSeqNo |

**ExecType (`150`) vs OrdStatus (`39`)** — a classic trap. `150` says *what just happened* (0=New, 1=PartialFill, 2=Fill, 4=Canceled, 5=Replace, 8=Rejected); `39` says *what state the order is in now*. They usually agree but diverge on the transition (a `150=5` replace leaves `39` unchanged).

---

### 3. Computational Implementation — a validating encoder/parser

The encoder builds well-formed messages; the parser is **strict** — it rejects bad framing, bad `BeginString`, a length mismatch, and a checksum mismatch — and detects two kinds of tampering. Stdlib only.

```python
# 02 - the FIX protocol: encode + strict parse/validate + corruption detection
SOH = "\x01"
HEADER_TAGS = ("8", "9", "35")
TRAILER_TAGS = ("10", "93", "89")

def encode(msg_type, fields, begin_string="FIX.4.4"):
    body = f"35={msg_type}{SOH}" + "".join(f"{t}={v}{SOH}" for t, v in fields)
    header = f"8={begin_string}{SOH}9={len(body)}{SOH}"
    raw = header + body
    return f"{raw}10={sum(raw.encode('ascii')) % 256:03d}{SOH}"

def parse(raw):
    """Return (ok, dict, reason). Validates BodyLength(9) then CheckSum(10)."""
    if raw[-1] != SOH:
        return False, {}, "message does not end with SOH"
    body = raw[:-1].split(SOH)
    d = {}
    for pair in body:
        if "=" not in pair:
            return False, {}, f"malformed field {pair!r}"
        t, _, v = pair.partition("=")
        if t in d:
            return False, {}, f"duplicate tag {t}"
        d[t] = v
    if d.get("8") not in ("FIX.4.2", "FIX.4.4", "FIXT.1.1"):
        return False, d, "bad BeginString(8)"
    # BodyLength(9): bytes from after the 9=<len>SOH up to (not incl.) 10=
    i = raw.index(f"9={d['9']}{SOH}") + len(f"9={d['9']}{SOH}")
    j = raw.rindex(f"10={d['10']}{SOH}")
    if j - i != int(d["9"]):
        return False, d, f"BodyLength mismatch: 9={d['9']} but body is {j - i} bytes"
    cs = sum(raw[:j].encode("ascii")) % 256
    if f"{cs:03d}" != d["10"]:
        return False, d, f"checksum mismatch: computed {cs:03d}, field 10={d['10']}"
    return True, d, "valid"

# --- NewOrderSingle (35=D) ---
nos = encode("D", [("49", "KWANT_BOT"), ("56", "EXCHANGE"), ("34", "215"),
                   ("52", "20260101-09:30:00.000"), ("11", "ORD_42"),
                   ("21", "1"), ("55", "AAPL"), ("54", "1"),
                   ("60", "20260101-09:30:00.000"), ("38", "500"),
                   ("40", "2"), ("44", "150.50"), ("59", "0")])
ok, d, why = parse(nos)
print(f"NewOrderSingle : {ok} ({why})  type={d['35']}  size={len(nos)} bytes")

# --- ExecutionReport (35=8) ---
er = encode("8", [("49", "EXCHANGE"), ("56", "KWANT_BOT"), ("34", "9001"),
                  ("52", "20260101-09:30:00.010"), ("37", "EX_77"),
                  ("11", "ORD_42"), ("17", "EXEC_1"), ("150", "0"),
                  ("39", "1"), ("55", "AAPL"), ("54", "1"),
                  ("38", "500"), ("32", "200"), ("31", "150.50"),
                  ("151", "300"), ("14", "200"), ("6", "150.50")])
ok, d, why = parse(er)
print(f"ExecutionReport: {ok} ({why})  type={d['35']}  "
      f"lastQty(32)={d['32']} leavesQty(151)={d['151']} avgPx(6)={d['6']}")

# --- corruption is caught ---
bad = nos[:-4] + "999" + SOH
ok, d, why = parse(bad)
print(f"\ncorrupted checksum -> {ok} ({why})")

bad2 = nos.replace("38=500", "38=5000")
ok, d, why = parse(bad2)
print(f"tampered qty       -> {ok} ({why})")
```
```
NewOrderSingle : True (valid)  type=D  size=165 bytes
ExecutionReport: True (valid)  type=8  lastQty(32)=200 leavesQty(151)=300 avgPx(6)=150.50

corrupted checksum -> False (checksum mismatch: computed 164, field 10=999)
tampered qty       -> False (BodyLength mismatch: 9=142 but body is 143 bytes)
```
The two failure lines are the whole point. A corrupted checksum is caught by the **sum check**; a field whose value grew by a character is caught *earlier* by the **length check** (the body is now 143 bytes but `9` still claims 142). A strict parser validates cheap structural invariants first and only then the arithmetic one.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming padding on the checksum.** `10` must be exactly three digits — `7` is malformed, `007` is correct. A parser that compares integers instead of strings silently accepts a spec violation and can mismatch across venues.
2. **Recomputing `9` from the wrong start.** `BodyLength` starts *after* the `9` field, not after `8`. Off-by-one here means every message you build is rejected, or worse, every message you accept is mis-framed.
3. **Character vs byte length.** FIX is ASCII, so the two agree — until a venue or a symbol field carries non-ASCII (rare in FIX 4.4, fatal in a naive parser). Length is *bytes*.
4. **Confusing `150` ExecType with `39` OrdStatus.** Building a state machine on `150` alone mis-handles replaces; building it on `39` alone loses the *reason* for a transition. Track both.
5. **Ignoring the trailer when "just parsing".** Reading fields with a SOH split and no `10` verification turns a corrupted stream into corrupted orders — the exact failure the envelope exists to prevent.
6. **Field order non-compliance.** `8`, `9`, `35` then header, then body, then `10`. Some venues reject mild reordering; the safe rule is the spec's strict ordering.

---

### 5. Canonical Literature & Study References

- **FIX Trading Community**, *FIX 4.4 Protocol Specification, Volume 1 — Message Format* (fixtrading.org) — the normative definition of the header/body/trailer, `BodyLength`, and `CheckSum`, plus the full per-message field tables. *The authoritative reference for this page.*
- **FIX Trading Community**, *FIX Unified Repository* — the machine-readable XML data dictionary; generate a codec rather than hand-coding tag tables.
- **OnixS**, *FIX Dictionary & Protocol Reference* — the browsable companion to the specs; useful for looking up a single tag quickly.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/03-session-management|03 · Session Management]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/04-order-lifecycle-and-connectivity|04 · Order Lifecycle & Connectivity]] (turning `D` and `8` into a state machine)
