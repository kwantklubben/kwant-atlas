---
title: "Tick-Level Databases & kdb+/q"
tags:
  - pillar-quant-dev
  - kdb-q
  - timeseries-databases
  - duckdb
---

**Basic Prerequisites:** Relational database concepts and SQL.

---

### 1. Intuition & Practical Objective

A single active trading day generates over 500 million raw tick messages across equity, options, and futures markets. Traditional row-oriented relational databases (PostgreSQL, MySQL) collapse under this volume: their row-by-row storage, B-tree indexes, and transactional locking overhead make querying billions of rows impossible.

Time-series databases in finance use **column-oriented storage** (such as **kdb+/q**, ClickHouse, and DuckDB/Parquet). By storing every column contiguously on disk and in memory, queries scanning 10 years of volume across 1,000 stocks execute in milliseconds via vectorized CPU memory scans.

---

### 2. Mathematical Ground Truth & Derivations

#### Column-Oriented Storage Mechanics
- **Row Store:** `[Time1, Sym1, Price1, Vol1], [Time2, Sym2, Price2, Vol2], ...`
  - Scanning price requires loading all unused timestamps, symbols, and sizes into cache.
- **Column Store:** `Price: [100.1, 100.2, 100.15, ...], Volume: [500, 1000, 200, ...]`
  - Querying `SUM(Volume)` reads contiguous blocks of memory with maximum memory bandwidth utilization ($> 50 \; \text{GB/s}$).

#### The As-Of Join (`aj`) Primitive
In quantitative research, joining market prices with asynchronous alternative data or quotes is fundamental. A standard SQL equi-join (`ON t1.time = t2.time`) fails because quotes and trades never have identical nanosecond timestamps.
The **as-of join (`aj`)** takes each trade at time $t$ and matches it with the **most recent preceding quote** on or before $t$:
$$\text{Quote}(t_{\text{trade}}) = \arg\max_{t_q \le t_{\text{trade}}} \{ \text{Quote}(t_q) \}$$

---

### 3. Computational Implementation

```python
import duckdb
import pandas as pd
import numpy as np

def demo_asof_join_duckdb():
    """
    Demonstrates high-performance As-Of Join in SQL using DuckDB.
    """
    con = duckdb.connect(database=":memory:")
    
    # Quotes table: changes periodically
    quotes_df = pd.DataFrame({
        "time": pd.to_datetime(["2024-01-01 09:30:00.100", "2024-01-01 09:30:00.500", "2024-01-01 09:30:01.200"]),
        "sym": ["AAPL", "AAPL", "AAPL"],
        "bid": [150.00, 150.05, 150.10],
        "ask": [150.02, 150.07, 150.12]
    })
    
    # Trades table: asynchronous executions
    trades_df = pd.DataFrame({
        "time": pd.to_datetime(["2024-01-01 09:30:00.250", "2024-01-01 09:30:00.900"]),
        "sym": ["AAPL", "AAPL"],
        "price": [150.02, 150.06],
        "size": [100, 200]
    })
    
    con.register("quotes", quotes_df)
    con.register("trades", trades_df)
    
    # DuckDB ASOF JOIN
    query = """
    SELECT t.time, t.sym, t.price, t.size, q.bid, q.ask
    FROM trades t
    ASOF JOIN quotes q
      ON t.sym = q.sym AND t.time >= q.time
    """
    res = con.execute(query).df()
    print("As-Of Joined Trade Executions with Prevailing Quotes:\n", res)

demo_asof_join_duckdb()
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Unsorted Time Index in As-Of Joins:**
   - *Failure:* Running an as-of join on out-of-order timestamps.
   - *Symptom:* Algorithmic complexity degrades from $\mathcal{O}(N + M)$ to $\mathcal{O}(N \times M)$, causing query execution times to blow up from 1 second to 4 hours.

2. **Memory Leaks in In-Memory Tick Buffers:**
   - *Failure:* Accumulating tick data in dynamic RAM dictionaries without an automated end-of-day disk partition flushing mechanism.

---

### 5. Canonical Literature & Study References

- **Psaila, Jeff**: *Q for Mortals: A Tutorial in q Programming and the kdb+ Database*, First Derivatives.
- **Hasbrouck, Joel**: *Empirical Market Microstructure*, Chapter 2.

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting]]
- Bridges to: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation|Alternative Data]]
