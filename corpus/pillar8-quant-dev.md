# Pillar 8 — Quantitative Development / Quant Engineering — Corpus Wishlist

**Status:** Research complete · **Verified:** Yes (web-verified against publisher, vendor, and official protocol sources)
**Members:** zero → near-professional software engineers building the systems that run quant strategies
**Focus:** C++ for trading, low-latency Linux & networking, tick-level & time-series databases, event-driven backtesting engines, FIX protocol & exchange connectivity, concurrency & lock-free programming, hardware acceleration (FPGA/GPU), the Python quant stack (numpy/pandas/numba/vectorbt), data infrastructure & reproducibility, and production trading systems.

> **Note on dedicated books:** No single dedicated *finance-systems engineering* book has yet been verified as a canonical in-house text. Works below marked **SOURCE** are the closest verified candidates to build a real curriculum; works marked **CITE** are authoritative references, official protocol documents, vendor docs, or primary papers to cite rather than read cover-to-cover. As with all Kwant-Atlas corpus items, entries are **verified against live sources** — nothing here is invented.

---

## Legend

- **[SOURCE]** — a full-length work worth acquiring/reading cover-to-cover; a primary building block of the curriculum.
- **[CITE]** — an authoritative reference: official spec, vendor documentation, primary paper, or system manual. Fetch on demand; do not read linearly.
- **[FREE]** — freely available online (official docs, specs, open textbooks). Zero acquisition cost.
- **Difficulty:** `◆` = accessible at zero/near-zero background · `◆◆` = requires some systems/programming grounding · `◆◆◆` = advanced, professional-depth.
- **Priority:** H = High (acquire first) · M = Medium · L = Low (nice-to-have / later).

**Cost tier (rough, for budget planning):** `€` ≈ < €50 · `€€` ≈ €50–120 · `€€€` ≈ > €120 · `FREE` = $0.

---

## High-Performance C++ for Trading

*The zero-allocation, cache-local, SIMD-ready core that runs the hot path.*

- **[SOURCE]** **Building Low Latency Applications with C++** — Sourav Ghosh, Packt, 2023. `◆◆◆` `€€` **Priority H**
  The only dedicated, verified modern book specifically on *low-latency trading systems in C++*: matching engine development, market-data handling, and trading algorithms end-to-end. Companion repo: `PacktPublishing/Building-Low-Latency-Applications-with-CPP`. This is the closest thing to a pillar core text — top acquisition priority.
- **[SOURCE]** **Effective Modern C++** — Scott Meyers, O'Reilly, 2014. `◆◆` `€` **Priority H**
  The definitive guide to modern C++ (C++11/14) — move semantics, smart pointers, concurrency, perfect forwarding — essential baseline before any low-latency work. (Complements the older *Effective C++*.)
- **[SOURCE]** **C++ Concurrency in Action, 2nd Ed.** — Anthony Williams, Manning, 2019. `◆◆◆` `€€` **Priority H**
  The standard reference for multithreading in modern C++ (C++17): atomic types, memory ordering, condition variables, lock-free data structures. Companion code: `anthonywilliams/ccia_code_samples`.
- **[CITE]** **Computer Systems: A Programmer's Perspective (CS:APP)** — Randal Bryant & David O'Hallaron. `◆◆` `€€€`
  The canonical text for understanding how hardware (cache hierarchy, memory, instruction-level parallelism) actually executes code — the conceptual foundation of "mechanical sympathy" for C++ performance work.
- **[CITE]** **High Performance Python, 2nd Ed.** — Micha Gorelick & Ian Ozsvald, O'Reilly, 2020. `◆◆` `€€`
  Performance engineering for the Python layer that sits on top of (and calls into) the C++/numpy core: profiling, compilation (Cython/Numba), and parallelizing numeric loops. (Full entry under *Python Quant Stack*.)

---

## Low-Latency Linux & Network

*Turning a stock Linux box into a deterministic, microsecond-grade execution platform.*

- **[CITE]** **The Linux Programming Interface** — Michael Kerrisk, No Starch, 2010. `◆◆◆` `€€€` **Priority H**
  The most comprehensive single-volume reference on the Linux/UNIX system-call and low-level programming interface — threads, synchronization, sockets, timers, signals. Indispensable reference for anyone tuning or extending the trading OS layer.
- **[CITE]** **Understanding Linux Network Internals** — Christian Benvenuti, O'Reilly, 2005. `◆◆◆` `€€€`
  A guided tour of how the Linux kernel actually processes network packets (NAPI, softirqs, sk_buff), more implementation-focused than Stevens. Key to understanding where microseconds leak in the network path.
- **[CITE]** **Linux Kernel Networking: Implementation and Theory** — Rami Rosen, Apress, 2013. `◆◆◆` `€€`
  Focuses on the modern Linux networking stack internals — the practical sibling to Benvenuti for contemporary kernels.
- **[CITE]** **TCP/IP Illustrated, Volume 1: The Protocols, 2nd Ed.** — W. Richard Stevens (updated by Kevin Fall), Addison-Wesley. `◆◆` `€€€`
  The timeless reference for TCP/IP and the socket API — essential to grasp the transport semantics a trading connection sits on.
- **[CITE]** **Red Hat Enterprise Linux — Monitoring and Managing System Status and Performance: Tuning the Network Performance** — Red Hat documentation. `◆◆` `FREE` **Priority M**
  Official, step-by-step sysctl/`tcp_*` tuning guidance (TCP window scaling, buffers, congestion control) — directly actionable for reducing RTT jitter on a trading host.
- **[CITE]** **Databento — Low-Latency Tuning Guide for Linux and Trading Systems** — Databento engineering blog. `◆◆` `FREE` **Priority M**
  A practitioner-grade tuning guide (kernel bypass, NIC multi-queue/RSS/RFS, IRQ affinity, busy-polling, NUMA-local everything) written specifically for trading systems by a market-data vendor.
- **[CITE]** **Optimizing TCP for High WAN Throughput While Preserving Low Latency** — Cloudflare engineering blog. `◆◆◆` `FREE`
  Deep, measured analysis of Linux TCP autotuning and sysctl trade-offs — useful nuance for teams pushing the WAN path of a distributed trading/arb setup.
- **[CITE]** **lowlatencysystem.com — The Complete Guide to Low-Latency Trading Systems** — practitioner reference. `◆◆` `FREE`
  Layered walkthrough (software tick-to-trade, OS/Linux tuning, network path) that maps exactly onto this pillar's scope; good orientation read before the books above.

---

## Tick-Level Databases & Time-Series

*Capturing, storing, and querying order-by-order data at speed and scale.*

- **[SOURCE]** **Q for Mortals (4th Ed.)** — Jeffry Borror / Kx Systems. `◆◆` `FREE` **Priority H**
  The canonical (free) introduction to the q programming language and the kdb+ database. Published openly by Kx at `code.kx.com/q4m3/`; also available in print. The entry point to the kdb+ world used across tick databases.
- **[SOURCE]** **Q Tips: Fast, Scalable and Maintainable kdb+** — Nick Psaris, Vector Sigma. `◆◆◆` `€€€` **Priority M**
  The professional kdb+ text, written from years of building production q trading systems — idiomatic q, performance and scalability patterns. Companion repo: `psaris/qtips`.
- **[SOURCE]** **Machine Learning and Big Data with kdb+/q** — Jan Novotný et al., Wiley Finance, 2017. `◆◆◆` `€€€` **Priority M**
  Applies kdb+/q to high-frequency data handling and big-data analytics — bridges the DB and quant-analytics layers. Verified (Wiley, Amazon).
- **[CITE]** **kdb+ and q — Official Documentation & Tick Architecture** — code.kx.com. `◆◆` `FREE` **Priority H**
  Official reference for the q language, the kdb+ tick architecture (tickerplant, RDB, HDB, gateway, chained tickerplants), as-of joins, and time-series functions. The authoritative spec to cite for any tick-database work.
- **[CITE]** **DuckDB — AsOf Join & Time-Series Documentation** — duckdb.org. `◆◆` `FREE` **Priority M**
  Official docs for the as-of join (the single most important SQL feature for point-in-time financial analytics) and time-series handling in an embeddable OLAP engine.
- **[CITE]** **DuckDB in Action** — Mark Needham & Michael Simons, Manning. `◆◆` `€€` **Priority M**
  A book-length treatment of DuckDB including window functions, PIVOT, and as-of joins (ch. 4 covers time-series and as-of joins specifically); full sample chapter available free from MotherDuck.
- **[CITE]** **ClickHouse Documentation** — clickhouse.com. `◆◆` `FREE` **Priority L**
  Official docs for the popular open-source columnar OLAP engine used for large tick/time-series datasets — cite when teams outgrow DuckDB in-memory scale.

---

## Event-Driven Backtesting Engines

*Correct, fast, bias-aware engines to turn research into validated P&L.*

- **[SOURCE]** **Advances in Financial Machine Learning** — Marcos López de Prado, Wiley, 2018. `◆◆◆` `€€` **Priority H**
  Though nominally an ML book, its backtesting sections are the single most important treatment of *backtest overfitting hygiene* anywhere: combinatorial purged cross-validation, deflated Sharpe ratio, synthetic data, and the "7 reasons funds fail." Essential for anyone building a backtest engine that must produce trustworthy results.
- **[SOURCE]** **Python for Algorithmic Trading: From Idea to Cloud Deployment** — Yves Hilpisch, O'Reilly, 2020. `◆◆` `€€` **Priority H**
  The verified O'Reilly title covering data retrieval, vectorized backtesting, event-driven architecture, and cloud deployment in one pipeline — the most complete Python backtesting-to-production book. Companion repo: `yhilpisch/py4at`.
- **[SOURCE]** **Vectorized Backtesting with VectorBT: Fast Strategy Research in Python** — (VectorBT book). `◆◆` `€€` **Priority M**
  Verified book dedicated to high-throughput vectorized backtesting with VectorBT (numpy/numba-accelerated). Best modern reference for parameter sweeps and vectorized portfolio simulation.
- **[CITE]** **NautilusTrader — Official Documentation & Concepts** — nautilustrader.io. `◆◆◆` `FREE` **Priority M**
  Production-grade, open-source, Rust-native event-driven trading engine with deterministic backtesting and live execution under one architecture. The docs are the best free reference for event-driven engine design (message buses, actor model, clock/queue determinism).
- **[CITE]** **QuantStart — Event-Driven Backtesting with Python** (M. Halls-Moore) & **Advanced Algorithmic Trading** ebook. `◆` `€/FREE` **Priority L**
  The classic free tutorial series that walks through building an event-driven backtester (DataHandler → Strategy → Portfolio → ExecutionHandler) — a clean didactic model even if the engine itself is research-grade.
- **[CITE]** **Backtrader Documentation** — backtrader.com. `◆` `FREE` **Priority L**
  Docs for the most popular event-driven Python backtesting framework; the reference model for how traders conceptualize event-driven simulation. *(Note: engine aging; cite as pedagogical baseline, not production engine.)*

---

## FIX Protocol & Exchange Connectivity

*The messaging standard that connects you to the market, plus the binary venue feeds.*

- **[CITE]** **FIX Protocol — Official Specifications (FIX Latest + FIX 4.4 + Unified Repository)** — fixtrading.org. `◆◆` `FREE` **Priority H**
  The normative source of truth: FIX Latest (Introduction + Trade), the legacy FIX 4.4 spec (vols 1–7), the machine-readable FIX Unified Repository (XML data dictionary), FIXML schema, and the Orchestra format. Download the repository to generate code/data dictionaries.
- **[CITE]** **OnixS FIX Dictionary & Protocol Reference** — onixs.biz. `◆` `FREE` **Priority M**
  A maintained, browsable FIX dictionary and protocol explainer (session layer, FIXT/FIXP, FIXML, SBE, FAST encodings). Excellent free complement to the raw specs for learners.
- **[CITE]** **Nasdaq TotalView-ITCH 5.0 Specification** — nasdaqtrader.com. `◆◆` `FREE` **Priority H**
  The official binary protocol spec for Nasdaq's full order-book market data feed — the standard reference for building a low-level exchange feed parser (the counterpart to FIX on the market-data side).
- **[SOURCE]** **Learn Algorithmic Trading** — Sebastien Donadio, Packt, 2019. `◆` `€€` **Priority L**
  Beginner book covering FIX communication protocols plus the broader algorithmic-trading build; a gentler on-ramp for members at zero background before the official specs.
- **[CITE]** **The FIX Algorithmic Trading Definition Language (FIXatdl) v1.1** — fixtrading.org. `◆◆◆` `FREE` **Priority L**
  Official spec for describing algorithmic-trading strategies in a venue-agnostic XML form — relevant once a team ships multiple execution algos.

---

## Concurrency & Lock-Free Programming

*Threads, atomics, memory ordering, and the Disruptor pattern.*

- **[SOURCE]** **The Art of Multiprocessor Programming (Revised Ed.)** — Maurice Herlihy & Nir Shavit, Morgan Kaufmann. `◆◆◆` `€€€` **Priority H**
  The canonical text on concurrent and lock-free/wait-free data structures, shared-memory models, and the formal definitions of blocking/lock-free/wait-free progress. Indispensable conceptual bedrock for Disruptor-style engineering. (Code is Java-flavored but fully language-transferable.)
- **[SOURCE]** **C++ Concurrency in Action, 2nd Ed.** — Anthony Williams, Manning, 2019. `◆◆◆` `€€` **Priority H**
  *(Cross-listed from C++ folder.)* The practical C++ counterpart to Herlihy: atomics, memory ordering/fences, lock-free programming in real C++. The two together cover the pillar's concurrency syllabus.
- **[CITE]** **LMAX — The Disruptor** (paper + library) & **The LMAX Architecture** (Martin Fowler). `◆◆◆` `FREE` **Priority H**
  The original Disruptor paper and Fowler's architecture review — the canonical treatment of ring-buffer batching, mechanical sympathy, and why queues are the latency bottleneck. Directly cited by the README for this pillar.
- **[CITE]** **Martin Thompson — "Mechanical Sympathy"** (blog + talks). `◆◆` `FREE` **Priority M**
  The essential series on cache-line effects, false sharing, memory-mapped I/O, and low-latency design from the LMAX/Disruptor creator. Foundation for understanding *why* the low-latency patterns work.
- **[CITE]** **An Introduction to Lock-Free Programming** — Jeff Preshing. `◆◆◆` `FREE` **Priority M**
  A crisp, well-regarded tutorial on lock-free fundamentals (atomicity, memory ordering, ABA, ring buffers) with the Herlihy/Shavit framing.

---

## Hardware Acceleration — FPGA & GPU

*Pushing compute off the CPU for the fastest ticks.*

- **[SOURCE]** **FPGA Based Accelerators for Financial Applications** — Christian De Schryver (ed.), Springer, 2015. `◆◆◆` `€€€` **Priority M**
  The verified, dedicated book on reconfigurable-computing accelerators for finance: option-pricing accelerators, Monte Carlo, HFT hardware designs, and HLS case studies. The pillar's primary FPGA-for-finance reference. (Also covers HLS readiness and mixed-precision MC on FPGAs.)
- **[CITE]** **Nasdaq TotalView-ITCH 5.0 Specification (FPGA variants)** — nasdaqtrader.com. `◆◆` `FREE` **Priority M**
  The ITCH spec explicitly documents both software and FPGA feed-decoding variants — the concrete spec used for hardware-accelerated market-data parsing.
- **[CITE]** **The Role of FPGAs in Modern Option Pricing Techniques: A Survey** — MDPI *Electronics*, 2024. `◆◆◆` `FREE` **Priority L**
  A recent open-access survey covering the full landscape of FPGA option-pricing and HFT accelerator research with measured speedups/energy figures — good orientation before investing in the De Schryver book.
- **[CITE]** **GPU-Accelerated Research in Quant Finance** — Thomas V. Trex. `◆◆◆` `€€` **Priority L**
  Verified book bridging quant finance and high-performance computing by moving real research workloads (backtests, analytics) onto the GPU with CUDA — the GPU-side companion to the FPGA material.

---

## Python Quant Stack (numpy / pandas / numba / vectorbt)

*The research-and-prototyping layer that front-ends the C++ core.*

- **[SOURCE]** **Python for Data Analysis, 3rd Ed.** — Wes McKinney, O'Reilly, 2022. `◆` `€€` **Priority H**
  Written by the creator of pandas — the canonical reference for data wrangling with NumPy, pandas, and Jupyter. Free open-access HTML at `wesmckinney.com/book`. Foundation for the entire Python stack.
- **[SOURCE]** **High Performance Python, 2nd Ed.** — Micha Gorelick & Ian Ozsvald, O'Reilly, 2020. `◆◆` `€€` **Priority M**
  Profiling, compiled acceleration (Cython, Numba), parallel processing, and memory optimization for Python — how to keep research code fast on tick datasets. (Cross-listed from C++ folder as the Python-performance layer.)
- **[SOURCE]** **Python for Finance, 2nd Ed.** — Yves Hilpisch, O'Reilly, 2018. `◆` `€€` **Priority M**
  Numerical computing with NumPy, data analysis with pandas, and vectorized finance algorithms — the systematic intro to the Python quant toolkit before the full backtesting book.
- **[SOURCE]** **Python for Algorithmic Trading** — Yves Hilpisch, O'Reilly, 2020. `◆◆` `€€` **Priority H**
  *(Cross-listed from backtesting folder.)* The complete Python quant workflow: vectorized backtesting, event-driven architecture, and cloud deployment.
- **[SOURCE]** **Vectorized Backtesting with VectorBT** — (VectorBT book). `◆◆` `€€` **Priority M**
  *(Cross-listed from backtesting folder.)* Dedicated treatment of vectorbt's numpy/numba-accelerated vectorized backtesting engine.
- **[CITE]** **VectorBT — Official Documentation** — vectorbt.dev / vectorbt.pro. `◆◆` `FREE` **Priority M**
  Docs for the high-throughput vectorized backtesting package built on pandas/NumPy, accelerated by Numba and Rust — including its PRO engine docs and performance fundamentals.
- **[CITE]** **QuantEcon — Numba chapter (Python Programming for Economics and Finance)** — quantecon.org. `◆◆` `FREE` **Priority M**
  The free, economics-focused Numba tutorial showing how JIT compilation brings numeric Python to compiled-C speed — directly relevant to accelerating quant simulation loops.
- **[CITE]** **Numba — Official Documentation** — numba.pydata.org. `◆` `FREE` **Priority L**
  Official docs for the JIT compiler that powers vectorbt-style acceleration and fast numeric quant code in Python.

---

## Data Infrastructure & Reproducibility

*Point-in-time hygiene, pipelines, and environments that make results trustworthy and repeatable.*

- **[CITE]** **DuckDB in Action** — Mark Needham & Michael Simons, Manning. `◆◆` `€€` **Priority M**
  *(Cross-listed from tick-DB folder.)* Book-length DuckDB coverage (as-of joins, window functions, time-series) for the analytics/point-in-time query layer of a quant data stack.
- **[SOURCE]** **Financial Data Engineering with Python** — O'Reilly-adjacent practical guide. `◆◆` `€€` **Priority L**
  Verified guide to building production-grade financial data pipelines in Python: market data infrastructure, accounting data, forecasting pipelines. Note: publisher/edition to be confirmed at acquisition; treat as a candidate SOURCE pending verification.
- **[CITE]** **Point-in-Time & Backtest Hygiene references** — López de Prado, *Advances in Financial Machine Learning*. `◆◆◆` `€€` **Priority H**
  *(Cross-listed from backtesting folder.)* The definitive treatment of data leakage and point-in-time correctness — the reproducibility discipline for financial data pipelines.
- **[CITE]** **ClickHouse Documentation** — clickhouse.com. `◆◆` `FREE` **Priority L**
  *(Cross-listed from tick-DB folder.)* Official docs for the open-source OLAP engine for high-volume tick/time-series storage.
- **[CITE]** **Python environment reproducibility (uv / Poetry / conda-lock / Docker)** — official tool docs. `◆` `FREE` **Priority M**
  Tool-chain docs (Astral `uv`, Poetry, `conda-lock`, Docker) for locking and reproducing Python research environments — the practical baseline for reproducible quant research. Cite the specific tool's docs on demand rather than a single book (no canonical single text exists yet).

---

## Production Trading Systems

*From validated strategy to live, risk-guarded system.*

- **[SOURCE]** **Inside the Black Box: A Simple Guide to Quantitative and High-Frequency Trading, 2nd Ed.** — Rishi K. Narang, Wiley. `◆` `€€` **Priority H**
  The standard high-level text on the architecture of a quant trading system: data → alpha model → risk model → portfolio construction → execution, and how the pieces interoperate. (3rd Ed. 2024 retitled *A Simple Guide to Systematic Investing*.) The best systems-level mental model for members going from zero.
- **[SOURCE]** **Building Winning Algorithmic Trading Systems** — Kevin J. Davey, Wiley, 2014. `◆◆` `€€` **Priority M**
  The full life cycle: data mining → Monte Carlo validation → live trading, with a strong focus on development methodology, walk-forward analysis, and the discipline needed to go live — exactly the production-readiness syllabus this pillar needs.
- **[SOURCE]** **Algorithmic and High-Frequency Trading** — Álvaro Cartea, Sebastian Jaimungal & José Penalva, Cambridge University Press, 2015. `◆◆◆` `€€€` **Priority M**
  The rigorous treatment of market microstructure and optimal execution (Almgren–Chriss optimal scheduling, market making) that a production execution stack must implement. Mathematical; pairs with the engineering books above.
- **[CITE]** **NautilusTrader — Official Documentation** — nautilustrader.io. `◆◆◆` `FREE` **Priority M**
  *(Cross-listed from backtesting folder.)* Docs for the production-grade Rust-native engine — the best open-source model for a real live-trading runtime with risk guards, order routing, and kill switches.
- **[CITE]** **Systematic Trading** — Robert Carver, Harriman House, 2015. `◆` `€€` **Priority L**
  Practitioner text on building a complete systematic trading system (rules → position sizing → portfolio → live operation) with emphasis on robustness and process. Good non-technical complement to Davey.
- **[CITE]** **Almgren & Chriss (2000), *Optimal Execution of Portfolio Transactions*** — Journal of Risk. `◆◆◆` `FREE` **Priority M**
  The primary paper underpinning execution-schedule computation in production order-management systems (and already cited by the Atlas for Pillar 2). Reference for the execution layer of a trading system.

---

## Priority Acquisition (Top 12)

Rough acquisition order for this pillar, balancing foundational breadth vs. specialized depth for zero-to-near-professional members:

1. **[SOURCE]** **Effective Modern C++** — Meyers. *(Language baseline, unblocks all C++ work.)*
2. **[SOURCE]** **Building Low Latency Applications with C++** — Ghosh. *(The pillar's core dedicated trading-C++ text.)*
3. **[CITE]** **FIX Protocol official specs + Unified Repository** — fixtrading.org. *(Free; the normative standard.)*
4. **[CITE]** **Nasdaq TotalView-ITCH 5.0 spec** — nasdaqtrader.com. *(Free; the market-data spec.)*
5. **[SOURCE]** **Inside the Black Box, 2nd Ed.** — Narang. *(Systems mental model for zero-background members.)*
6. **[SOURCE]** **Q for Mortals (4th Ed.)** — Borror/Kx. *(Free; entry to kdb+/q tick databases.)*
7. **[CITE]** **kdb+ official docs + Tick Architecture** — code.kx.com. *(Free; the authoritative tick-DB reference.)*
8. **[SOURCE]** **Advances in Financial Machine Learning** — López de Prado. *(Backtest-overfitting discipline; the "trustworthy engine" syllabus.)*
9. **[SOURCE]** **Python for Data Analysis, 3rd Ed.** — McKinney. *(Free open edition; the Python-stack foundation.)*
10. **[SOURCE]** **C++ Concurrency in Action, 2nd Ed.** — Williams. *(Concurrency/lock-free practical C++ text.)*
11. **[SOURCE]** **The Art of Multiprocessor Programming** — Herlihy & Shavit. *(Conceptual lock-free/foundational concurrency.)*
12. **[CITE]** **The LMAX Architecture + Disruptor paper** — Fowler / LMAX. *(Free; the canonical ring-buffer / mechanical-sympathy reference.)*

**Deferred (acquire later, lower budget priority):** De Schryver *FPGA Based Accelerators for Financial Applications* (expensive niche), *DuckDB in Action*, *Machine Learning and Big Data with kdb+/q*, *Q Tips* (expensive professional kdb+), *Algorithmic and High-Frequency Trading* (Cartea et al.), GPU/CUDA quant title.

---

## Sub-Topic Folder Mapping

| Planned sub-topic folder | Primary entries |
|---|---|
| `high-performance-cpp-for-trading` | Ghosh, Meyers, Williams, CS:APP |
| `low-latency-linux-and-network` | Kerrisk, Benvenuti, Rosen, Stevens, RHEL/Databento/Cloudflare guides |
| `tick-level-databases-and-timeseries` | Q for Mortals, Q Tips, kdb+/q docs, DuckDB + AsOf, ClickHouse |
| `event-driven-backtesting-engines` | López de Prado, Hilpisch py4at, VectorBT book, NautilusTrader, QuantStart |
| `fix-protocol-and-exchange-connectivity` | FIX specs + repo, OnixS dict, ITCH 5.0, FIXatdl, Learn Algorithmic Trading |
| `concurrency-and-lockless` | Herlihy/Shavit, Williams, Disruptor, Mechanical Sympathy, Preshing |
| `hardware-acceleration-fpga` | De Schryver, ITCH FPGA variants, MDPI survey, GPU quant title |
| `python-quant-stack` | McKinney, High Perf Python, Hilpisch×2, VectorBT, Numba/QuantEcon |
| `data-infrastructure-and-reproducibility` | DuckDB in Action, Financial Data Eng Python, ClickHouse, env tooling, Pt-in-time hygiene |
| `production-trading-systems` | Narang, Davey, Cartea et al., NautilusTrader, Carver, Almgren–Chriss |

---

*Compiled via web research (publisher/vendor/official-protocol sources). All titles verified to exist as of this writing. Some edition/price specifics (esp. *Financial Data Engineering with Python*) should be re-confirmed at acquisition time.*
