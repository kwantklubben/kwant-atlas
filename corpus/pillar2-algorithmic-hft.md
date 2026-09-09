---
title: "Pillar 2 Corpus Wishlist — Algorithmic & High-Frequency Trading"
tags:
  - corpus-wishlist
  - pillar-algorithmic-hft
  - algorithmic-trading
  - hft
  - low-latency
  - execution
---

# Pillar 2 Corpus Wishlist — Algorithmic & High-Frequency Trading

> Corpus acquisition list for **Pillar 2: Algorithmic & High-Frequency Trading** of the Kwant-Atlas.
> This pillar covers the *execution* side of the market: order types and market microstructure as seen by a trader, execution algorithms, optimal execution, low-latency system architecture, smart order routing, queue/fill dynamics, and hardware acceleration.
> **Member profile:** zero experience through near-Wall-Street. Entries are deliberately ordered beginner → expert per sub-topic.

**How to use this file:** entries are grouped under the planned sub-topic folders. Each entry carries a level tag, a short "why," and full metadata. Items marked **[HAVE]** are already in the Atlas. The final section gives a **Priority acquisition** shortlist — the ~10 works that give the biggest coverage-per-unit effort and should be bought/downloaded first.

---

## Legend

**Level tags**
- `BEGIN` — no quant background required; ideal on-ramp.
- `INT` — some math/CS or market familiarity useful; core working knowledge.
- `ADV` — graduate-level math or deep systems engineering; reference-grade depth.

**Status tags**
- `[HAVE]` — already owned/in the Atlas (verified). All others are acquisition targets (`[WANT]` implied).

**Sourcing honesty:** where a sub-topic (low-latency, FPGA, clock sync) genuinely lacks a canonical *textbook*, the entry is marked as official documentation / exchange spec / industry paper rather than a fabricated book. The field is documented in primary sources, not monographs.

---

## Foundational — Execution & HFT Overview

**Books**

- **Cartea, Álvaro; Jaimungal, Sebastián; Penalva, José** — *Algorithmic and High-Frequency Trading* (Cambridge University Press, 2015). `ADV` · **[WANT]`
  Why: The single best modern mathematical monograph bridging execution algorithms and market making — order-flow models, optimal execution, and microsecond strategies under one rigorous framework. The spine of this pillar for the mathematical members.

- **Johnson, Barry** — *Algorithmic Trading & DMA: An Introduction to Direct Access Trading Strategies* (4Myeloma Press, 2010). `INT` · **[WANT]`
  Why: The practitioner bible for the buy side — order types, DMA mechanics, execution algorithms, market microstructure from the desk's point of view. Readable and comprehensive; the best single "how the trading desk actually works" text.

- **Narang, Rishi K.** — *Inside the Black Box: A Simple Guide to Quantitative and High-Frequency Trading* (Wiley, 2nd ed., 2013). `BEGIN` · **[WANT]`
  Why: The standard accessible map of how quant/HFT strategies (including execution) are structured. Best starting point for a zero-experience member.

- **Aldridge, Irene** — *High-Frequency Trading: A Practical Guide to Algorithmic Strategies and Trading Systems* (Wiley Trading, 2nd ed., 2013). `INT` · **[WANT]`
  Why: Practical HFT covering infrastructure, latency budgets, and strategy types with worked examples — good bridge between finance prose and the systems reality.

- **Chan, Ernest** — *Algorithmic Trading: Winning Strategies and Their Rationale* (Wiley, 2013). `INT` · **[WANT]`
  Why: Executable, code-follow-along treatment of algorithmic strategies including execution logic. Pragmatic counterweight to the theory books.

- **Hasbrouck, Joel** — *Empirical Market Microstructure: The Institutions, Economics, and Econometrics of Securities Trading* (Oxford University Press, 2007). `ADV` · **[HAVE]**
  Why: Already in the Atlas — the authoritative econometric treatment of markets and order flow. Microstructure foundation this pillar builds on.

- **Foucault, Thierry; Pagano, Marco; Röell, Ailsa** — *Market Liquidity: Theory, Evidence, and Policy* (Oxford University Press, 2013). `INT` · **[HAVE]**
  Why: Already in the Atlas — liquidity, transaction costs, and market-design theory from the academic mainstream.

- **O'Hara, Maureen** — *Market Microstructure Theory* (Blackwell, 1995). `ADV` · **[WANT]**
  Why: The classic price-formation theory monograph (Kyle, Glosten-Milgrom, dealer models). Date is old but it remains the theoretical bedrock you must know to read modern execution papers.

---

## Sub-topic: Market Microstructure & Order Types

**Books**

- **Harris, Larry** — *Trading and Exchanges: Market Microstructure for Practitioners* (Oxford University Press, 2003). `BEGIN` · **[WANT]**
  Why: The definitive plain-English book on who trades, how markets are structured, why transaction costs exist, and how every order type behaves. Universally recommended first read; indispensable background for every other entry in this pillar.

- **Abergel, Frédéric; Anane, Marouane; Chakraborti, Anirban; Jedidi, Aymen; Toke, Ioane Muni** (eds.) — *Limit Order Books* (Cambridge University Press, 2016). `ADV` · **[WANT]**
  Why: State-of-the-art quantitative treatment of limit order book models, optimal order placement, and market impact — the modern execution-side microstructure reference.

**Papers**

- **Gould, M. D.; Porter, M. A.; Williams, S.; McDonald, M.; Fenn, D. J.; Howison, S. D.** — "Limit order books," *Quantitative Finance* 13(11), 1709–1742 (2013). `ADV` · **[WANT]**
  Why: The canonical structured survey of LOB empirical facts and models. Read before Abergel et al. Free on arXiv (1012.0349).

---

## Sub-topic: Queue Position & Fill Probability

**Papers** (this sub-topic lives almost entirely in the academic literature)

- **Cont, Rama; Stoikov, Sasha; Talreja, Rishi** — "A stochastic model for order book dynamics," *Operations Research* 58(3), 549–563 (2010). `ADV` · **[WANT]**
  Why: The foundational tractable model of a limit order book as a system of queues — the basis for computing fill probabilities, queue-position survival, and execution likelihood analytically.

- **Lo, Andrew W.; MacKinlay, A. Craig; Zhang, June** — "Econometric models of limit-order executions," *Journal of Financial Economics* 65(1), 31–71 (2002). `ADV` · **[WANT]**
  Why: The classic empirical model of limit-order execution times (survival analysis on real order data). Directly answers "how long until my limit order fills / cancels."

- **Cont, Rama; Kukanov, Arseniy** — "Optimal order placement in a limit order book," *Quantitative Finance* 17(4), 2017. `ADV` · **[WANT]**
  Why: Unifies the queue/fill perspective with optimal execution — when to post passive vs. cross the spread given queue position and adverse-selection risk.

---

## Sub-topic: Execution Algorithms (VWAP / TWAP / POV / Implementation Shortfall)

**Books**

- **Kissell, Robert; Glantz, Morton; Malamut, Roberto** — *Optimal Trading Strategies: Quantitative Approaches for Managing Market Impact and Trading Risk* (AMACOM, 2003). `INT` · **[WANT]**
  Why: The desk standard on transaction cost analysis and building/slicing strategies around VWAP, TWAP, POV, and implementation-shortfall benchmarks. The core how-to for the "sell the block without moving the market" problem.

- **Kissell, Robert** — *The Science of Algorithmic Trading and Portfolio Management* (Academic Press / Elsevier, 2014). `INT` · **[WANT]**
  Why: The modernized successor to the 2003 book — TCA, optimal trading algorithms, and portfolio transition management from the practitioner who codified the field.

- **Johnson, Barry** — *Algorithmic Trading & DMA* (2010). `INT` · **[WANT]** — see Foundational. Its execution-algorithm chapters are the most digestible walk-through of VWAP/TWAP/POV/IS logic outside pure TCA texts.

**Papers**

- **Perold, André F.** — "The implementation shortfall: Paper versus reality," *Journal of Portfolio Management* 14(3), 4–9 (1988). `INT` · **[WANT]**
  Why: The origin of the Implementation Shortfall benchmark that every execution algorithm is graded against. Short, foundational, must-read.

---

## Sub-topic: Optimal Execution (Almgren–Chriss and Beyond)

**Papers** (the intellectual core of Pillar 2 — read in this order)

- **Bertsimas, Dimitris; Lo, Andrew W.** — "Optimal control of execution costs," *Journal of Financial Markets* 1(1), 1–50 (1998). `ADV` · **[WANT]**
  Why: The starting point — dynamic-programming formulation of best execution that the Almgren–Chriss framework generalizes.

- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5–40 (2000). `ADV` · **[WANT]**
  Why: THE canonical paper of this pillar — permanent vs. temporary impact, the risk/cost trade-off, and the efficient-frontier of liquidation trajectories. Already summarized in the Atlas content pages; the paper is the source.

- **Almgren, Robert** — "Optimal execution with nonlinear impact functions and trading-enhanced risk," *Applied Mathematical Finance* 10(1), 1–18 (2003). `ADV` · **[WANT]**
  Why: Extends the linear model to empirically real nonlinear impact — where the textbook Almgren–Chriss breaks down.

- **Almgren, Robert; Thum, Chee; Hauptmann, Emmanuel; Li, Hong** — "Direct estimation of equity market impact," *Risk* 18(7), 58–62 (2005). `ADV` · **[WANT]**
  Why: The empirical companion — how to fit real market-impact curves to actual order data. Bridges theory and the TCA tools above.

- **Obizhaeva, Anna; Wang, Jiang** — "Optimal trading strategy and supply/demand dynamics," *Journal of Financial Markets* 16(1), 1–32 (2013). `ADV` · **[WANT]**
  Why: The resilience-aware model: when the book replenishes after you trade, the optimal schedule becomes discrete (big-then-small), overturning pure Almgren–Chriss intuition.

- **Gatheral, Jim** — "No-dynamic-arbitrage and market impact," *Quantitative Finance* 10(7), 749–759 (2010). `ADV` · **[WANT]**
  Why: The consistency constraint every market-impact model must satisfy — guards against building arbitrageable execution models.

**Books / Monographs**

- **Guéant, Olivier** — *The Financial Mathematics of Market Liquidity: From Optimal Execution to Market Making* (Chapman & Hall/CRC Financial Mathematics Series, 2016). `ADV` · **[WANT]**
  Why: The rigorous modern monograph covering optimal execution and its natural partner, optimal market making — a systematic framework from a leading researcher.

- **Cartea, Jaimungal, Penalva** — *Algorithmic and High-Frequency Trading* (2015). `ADV` · **[WANT]** — see Foundational. Its optimal-execution chapters extend Almgren–Chriss to a stochastic-control setting.

---

## Sub-topic: Smart Order Routing & Fragmentation

**Papers**

- **O'Hara, Maureen; Ye, Mao** — "Is market fragmentation harming market quality?" *Journal of Financial Economics* 100(3), 459–474 (2011). `INT` · **[WANT]**
  Why: The empirical anchor on whether routing orders across a fragmented, multi-venue market (the whole premise of smart order routing) helps or hurts.

- **Degryse, Hans; de Jong, Frank; van Kervel, Vincent** — "The impact of dark trading and visible fragmentation on market quality," *Review of Finance* 19(4), 1587–1622 (2015). `ADV` · **[WANT]**
  Why: Extends fragmentation analysis to dark pools and lit-venue fragmentation — SOR must decide not just *where* but *lit vs. dark*.

- **Menkveld, Albert J.** — "High-frequency trading and the new market makers," *Journal of Financial Markets* 16(4), 712–740 (2013). `INT` · **[WANT]**
  Why: Why HFT venues concentrate where fast intermediaries can act as de facto market makers across fragmented markets — the routing context SOR operates in.

**Practical grounding**

- **Johnson, Barry** — *Algorithmic Trading & DMA* (2010). `INT` · **[WANT]** — DMA/smart-routing mechanics and order-lifecycle chapters are the most concrete practical treatment of routing and smart order types.

---

## Sub-topic: Colocation & Clock Synchronization

> There is **no canonical textbook** for this sub-topic — it is documented in exchange specs, market-design papers, and a small set of serious books. Entries reflect that reality.

**Books**

- **MacKenzie, Donald** — *Trading at the Speed of Light: How Ultrafast Algorithms Are Transforming Financial Markets* (Princeton University Press, 2021). `BEGIN` · **[WANT]**
  Why: The authoritative socio-technical account of colocation, microwave links, and the physical race to the matching engine. Non-technical but deeply informed — best on-ramp for the latency tier and its market-design consequences.

- **Lewis, Michael** — *Flash Boys: A Wall Street Revolt* (W.W. Norton, 2014). `BEGIN` · **[WANT]** *(optional / light)*
  Why: The cultural context that made latency arbitrage and colocation public knowledge. Not technical, but sets the vocabulary and the "why it matters."

**Papers & Primary Specs**

- **Budish, Eric; Cramton, Peter; Shim, John** — "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response," *Quarterly Journal of Economics* 130(4), 1547–1621 (2015). `INT` · **[WANT]**
  Why: The market-design critique that reframes the colocation/latency arms race as an artifact of continuous-time matching; proposes batch auctions. Central reading for the regulatory/systems angle.

- **IEEE 1588-2008 / PTP standard** and **exchange colocation & timestamp specifications** (CME, Nasdaq, Cboe market-tech specs; NIST PTP guidance). `INT` · **[WANT]** *(primary documentation)*
  Why: The ground truth on clock sync (PTP/1588) and matching-engine geography. Primary docs are the correct source here — flag for acquisition of the public specs, not a book.

---

## Sub-topic: Hardware Acceleration & FPGA / Kernel Bypass

> Like clock sync, this sub-topic is documented mainly in conference papers, vendor engineering docs, and open-source projects rather than textbooks. Several entries are primary sources.

**Papers**

- **Leber, Christian; Geib, Benjamin; Litz, Heiner** — "High Frequency Trading Acceleration Using FPGAs," *Proceedings of the 21st International Conference on Field Programmable Logic and Applications (FPL 2011)*. `ADV` · **[WANT]**
  Why: The widely-cited proof-of-concept that FPGAs can parse exchange feeds and run tick-to-trade logic in hardware at wire speed — the entry point to the silicon tier.

**Primary Documentation / Open Source**

- **DPDK documentation** (dpdk.org) and **Solarflare/Onload & OpenOnload kernel-bypass docs** — the standard low-latency networking stacks named throughout the Atlas. `INT` · **[WANT]** *(primary documentation)*
  Why: Kernel bypass, busy-polling, and zero-copy receive paths are documented here; these are the de-facto references used by trading-system engineers.

**Books / Context**

- **Aldridge, Irene** — *High-Frequency Trading* (2nd ed., 2013). `INT` · **[WANT]** — infrastructure/latency chapters give the systems context around FPGA and kernel-bypass decisions.
- **MacKenzie, Donald** — *Trading at the Speed of Light* (2021). `BEGIN` · **[WANT]** — the physical/hardware tier told accurately for non-hardware members.

---

## Sub-topic: Low-Latency Systems Architecture

**Books**

- **MacKenzie, Donald** — *Trading at the Speed of Light* (Princeton, 2021). `BEGIN` · **[WANT]** — see Colocation; the best single account of the end-to-end low-latency stack and its economics.

**Papers**

- **Hasbrouck, Joel; Saar, Gideon** — "Low-latency trading," *Journal of Financial Markets* 16(4), 646–679 (2013). `INT` · **[WANT]**
  Why: Defines and measures the low-latency / "latency-sensitive" trader empirically — gives you the numbers (order lifetimes, cancel rates) that systems architecture must satisfy.

- **Biais, Bruno; Foucault, Thierry; Moinas, Sophie** — "Equilibrium fast trading," *Journal of Financial Economics* 116(2), 292–313 (2015). `ADV` · **[WANT]**
  Why: The theory of *when* investing in speed is privately profitable but socially wasteful — the economic frame for deciding whether low-latency architecture is worth building at all.

**Primary Documentation**

- **Exchange matching-engine & FIX/ITCH protocol specs** (CME, Nasdaq, Cboe, Eurex) — the actual interface the low-latency stack must speak. `INT` · **[WANT]** *(primary documentation)*

---

## Sub-topic: Backtesting & Simulation of Execution

> Execution backtesting is distinct from signal backtesting: it requires modeling the order book, queue, and market impact rather than a price series. The canonical material is the LOB-modeling literature, not generic backtest books.

**Books**

- **Abergel et al.** — *Limit Order Books* (Cambridge, 2016). `ADV` · **[WANT]** — see Microstructure; includes agent-based LOB simulation and order-placement micro-simulation used to test execution logic.
- **Chan, Ernest** — *Algorithmic Trading* (2013). `INT` · **[WANT]** — code-driven backtesting of strategies incl. execution variants; the practical complement.

**Papers**

- **Cont, Stoikov, Talreja** — "A stochastic model for order book dynamics," *Operations Research* 58(3), 549–563 (2010). `ADV` · **[WANT]** — the model is fast enough for Monte-Carlo simulation of fills, the standard substrate for execution backtests.
- **Almgren, Thum, Hauptmann, Li** — "Direct estimation of equity market impact," *Risk* 18(7), 58–62 (2005). `ADV` · **[WANT]** — impact parameters a realistic execution simulator must calibrate.
- **Gould et al.** — "Limit order books," *Quantitative Finance* 13(11), 1709–1742 (2013). `ADV` · **[WANT]** — the survey tells you which LOB stylized facts a credible execution simulator must reproduce (and which models fail).

---

## Priority Acquisition Shortlist

Buy/download these first — they give the largest coverage-per-effort and let a reader climb from zero to near-Wall-Street:

1. **Harris, Larry — *Trading and Exchanges*** (2003). `BEGIN` — the universal first read; underlies every other sub-topic.
2. **Johnson, Barry — *Algorithmic Trading & DMA*** (2010). `INT` — the practitioner core: order types, execution algos, DMA, desk mechanics.
3. **Kissell, Glantz & Malamut — *Optimal Trading Strategies*** (2003). `INT` — TCA + slicing strategy how-to (VWAP/TWAP/POV/IS).
4. **Almgren & Chriss — "Optimal execution of portfolio transactions"** (Journal of Risk, 2000). `ADV` — the canonical paper; free PDF available.
5. **Bertsimas & Lo — "Optimal control of execution costs"** (J. Financial Markets, 1998). `ADV` — read immediately before #4.
6. **Cartea, Jaimungal & Penalva — *Algorithmic and High-Frequency Trading*** (2015). `ADV` — the deep mathematical spine for serious members.
7. **Perold — "The implementation shortfall"** (1988). `INT` — short, free, and every benchmark's origin.
8. **Cont, Stoikov & Talreja — "A stochastic model for order book dynamics"** (Operations Research, 2010). `ADV` — the queue/fill and execution-simulation foundation.
9. **Abergel et al. — *Limit Order Books*** (2016) + **Gould et al. survey** (2013). `ADV` — LOB modeling survey + monograph for microstructure depth.
10. **Budish, Cramton & Shim — "The High-Frequency Trading Arms Race"** (QJE, 2015). `INT` — the market-design critique of the latency arms race.
11. **MacKenzie — *Trading at the Speed of Light*** (2021). `BEGIN` — the low-latency/hardware tier told accurately and readably.
12. **O'Hara — *Market Microstructure Theory*** (1995). `ADV` — completes the theoretical bedrock for reading modern execution papers.

*Acquisition notes:* #1, #2, #6, #11 are physical/ebook monographs (purchase). #4, #5, #7, #9 (survey), #10 have free official PDFs (journal/arXiv/repec) — download to the corpus `papers/` folder first at zero cost. #8 and the impact papers (Almgren 2003/2005, Obizhaeva–Wang, Gatheral 2010) are also freely available from authors' pages for the "advanced" reader who wants the full optimal-execution chain.
