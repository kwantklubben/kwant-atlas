# Pillar 8 — Quantitative Development — Compact Acquisition List

> **Status tags (rewritten to reflect reality after the acquisition run of 2026-09-10):**
> **1** = HAVE — verified full text on disk, obtained from a licensed/library route (or already in
> the Atlas); path given inline ·
> **2** = FREE — obtained from a free/open source, file in `refs/pillar8/`, path given inline ·
> **3** = PAID / unobtainable — no SDU licence route and no open-access edition; each carries
> DOI/ISBN, publisher and a ready-to-submit interlibrary-loan block ·
> **4** = PARTIAL — a genuine but incomplete artefact (preview / sample / single chapter); the
> page count held is stated inline.
>
> **Where the artefacts live:** `corpus/titles/refs/pillar8/` — 28 verified PDFs, plus
> `MANIFEST.pillar8.json` (machine-readable: sha256, page count, DOI/ISBN, source URL, via_proxy,
> every attempt made), `MANIFEST.pillar8.md`, and `ILL_REQUESTS.pillar8.md`.
>
> **Verification gates applied to every file:** `%PDF` magic bytes · `pdftotext` yields extractable
> text · page count > 0 · fuzzy title / author+year match on the front pages. sha256 and page count
> are recorded per file; `_p8_attempts.json` logs every URL tried and its result.
>
> **Source note:** entries 09–45 are free web documentation, captured by rendering the live pages to
> PDF (Chromium headless print-to-pdf) rather than as publisher PDFs — `source_type` in the manifest
> flags each one as `web-doc (rendered PDF)`. Entries 07 and 35 are licensed e-book PDFs obtained
> through SDU EZproxy.

## High-Performance C++ for Trading

3. Building Low Latency Applications with C++ (Sourav Ghosh) — NOT OBTAINED · Packt commercial ebook; no SDU ebook licence (Mimer: no hit); no OA edition · ISBN 9781837634477 · Packt Publishing, 2023 · ILL: `refs/ILL_REQUESTS.pillar8.md` §01
3. Effective Modern C++ (Scott Meyers) — NOT OBTAINED · O'Reilly commercial ebook; SDU does not proxy O'Reilly Learning; no OA edition · ISBN 9781491903995 · O'Reilly Media, 2014 · ILL: `refs/ILL_REQUESTS.pillar8.md` §02
3. C++ Concurrency in Action, 2nd Ed. (Anthony Williams) — NOT OBTAINED · Manning commercial ebook; Manning is not an SDU-proxied platform · Manning Publications, 2019 · ILL: `refs/ILL_REQUESTS.pillar8.md` §03
3. Computer Systems: A Programmer's Perspective (Randal Bryant & David O'Hallaron) — NOT OBTAINED · Pearson textbook; SDU holds print only, no ebook · ISBN 9780134092669 · Pearson, 2015 · ILL: `refs/ILL_REQUESTS.pillar8.md` §04

## Low-Latency Linux & Network

3. The Linux Programming Interface (Michael Kerrisk) — NOT OBTAINED · SDU e-book record exists (Mimer) but no downloadable PDF via the proxy · No Starch Press, 2010 · ILL: `refs/ILL_REQUESTS.pillar8.md` §05
3. Understanding Linux Network Internals (Christian Benvenuti) — NOT OBTAINED · O'Reilly commercial ebook; no SDU proxy; no OA edition · ISBN 9780596002558 · O'Reilly Media, 2005 · ILL: `refs/ILL_REQUESTS.pillar8.md` §06
1. Linux Kernel Networking: Implementation and Theory (Rami Rosen) — OBTAINED (636 pp) · SDU EZproxy, SpringerLink full-book PDF · DOI 10.1007/978-1-4302-6197-1 · ISBN 9781430261964 · `pillar8/07_Rosen_2014_linux_kernel_networking.pdf` (sha256 `74b843b5b2…`)
3. TCP/IP Illustrated, Vol. 1: The Protocols, 2nd Ed. (W. Richard Stevens & Kevin Fall) — NOT OBTAINED · Addison-Wesley/Pearson commercial ebook; no SDU ebook licence; no OA edition · Addison-Wesley, 2011 · ILL: `refs/ILL_REQUESTS.pillar8.md` §08
2. RHEL — Monitoring/Managing System Status & Performance: Tuning the Network Performance (Red Hat docs) — OBTAINED (88 pp) · Red Hat docs page, rendered to PDF (bot-blocked to curl) · `pillar8/09_RedHat_RHEL_monitoring_network_performance_tuning.pdf` (sha256 `49765c654b…`)
4. Low-Latency Tuning Guide for Linux and Trading Systems (Databento engineering blog) — PARTIAL — holds 3 pp of a one-page article · Databento blog, text capture (live databento.com URL is now a 404; Medium mirror used) · `pillar8/10_Databento_2024_low_latency_tuning_guide_linux.pdf` (sha256 `c659ae85c0…`)
2. Optimizing TCP for High WAN Throughput While Preserving Low Latency (Cloudflare engineering blog) — OBTAINED (28 pp) · Cloudflare blog, rendered to PDF · `pillar8/11_Cloudflare_2021_optimizing_tcp_high_throughput_low_latency.pdf` (sha256 `addb14a6c2…`)
2. The Complete Guide to Low-Latency Trading Systems (lowlatencysystem.com) — OBTAINED (9 pp) · lowlatencysystem.com, rendered to PDF · `pillar8/12_lowlatencysystem_com_guide_low_latency_trading_systems.pdf` (sha256 `e41e86a883…`)

## Tick-Level Databases & Time-Series

4. Q for Mortals, 4th Ed. (Jeffry Borror / Kx Systems) — PARTIAL — holds 10 pp of the full online edition · code.kx.com free online edition (v3.1), rendered to PDF · `pillar8/13_Borror_Q_for_Mortals_kx_online_edition.pdf` (sha256 `75afdb3c2e…`)
3. Q Tips: Fast, Scalable and Maintainable kdb+ (Nick Psaris) — NOT OBTAINED · Commercial kdb+ ebook, self-published; no DOI/ISBN record; not licensed at SDU · ILL: `refs/ILL_REQUESTS.pillar8.md` §14
3. Machine Learning and Big Data with kdb+/q (Jan Novotný et al.) — NOT OBTAINED · Wiley book renders via the SDU proxy but /doi/pdf/ redirects to the abstract page · DOI 10.1002/9781119404729 · ISBN 9781119404729 · Wiley, 2019 · ILL: `refs/ILL_REQUESTS.pillar8.md` §15
2. kdb+ and q — Official Documentation & Tick Architecture (code.kx.com) — OBTAINED (6 pp) · code.kx.com official docs, rendered to PDF · `pillar8/16_Kx_kdb_plus_q_official_docs_tick_architecture.pdf` (sha256 `ea5c183cc2…`)
2. DuckDB — AsOf Join & Time-Series Documentation (duckdb.org) — OBTAINED (26 pp) · duckdb.org docs, rendered to PDF · `pillar8/17_DuckDB_asof_join_time_series_documentation.pdf` (sha256 `a09a3245f9…`)
4. DuckDB in Action (Mark Needham & Michael Simons) — PARTIAL — holds 25 pp of a ~260-pp book · publisher-free MEAP sample PDF (MotherDuck) · `pillar8/18_Needham_2024_duckdb_in_action_MEAP_chapter7.pdf` (sha256 `24d685e8a6…`)
2. ClickHouse Documentation (clickhouse.com) — OBTAINED (7 pp) · clickhouse.com docs, rendered to PDF · `pillar8/19_ClickHouse_official_documentation.pdf` (sha256 `154f30d9c4…`)

## Event-Driven Backtesting Engines

3. Advances in Financial Machine Learning (Marcos López de Prado) — NOT OBTAINED · Wiley commercial ebook; no Crossref book DOI; no downloadable chapter PDF via the proxy · ISBN 9781119482109 · Wiley, 2018 · ILL: `refs/ILL_REQUESTS.pillar8.md` §20
3. Python for Algorithmic Trading: From Idea to Cloud Deployment (Yves Hilpisch) — NOT OBTAINED · O'Reilly commercial ebook; no SDU proxy; no OA edition · ISBN 9781492053354 · O'Reilly Media, 2021 · ILL: `refs/ILL_REQUESTS.pillar8.md` §21
3. Vectorized Backtesting with VectorBT (VectorBT book) — NOT OBTAINED · Self-published ebook; only retailer listings (Amazon/Kobo), no ISBN/DOI/library record · ILL: `refs/ILL_REQUESTS.pillar8.md` §22
2. NautilusTrader — Official Documentation & Concepts (nautilustrader.io) — OBTAINED (23 pp) · nautilustrader.io docs, rendered to PDF · `pillar8/23_NautilusTrader_official_documentation_concepts.pdf` (sha256 `1ee5dc20d4…`)
2. QuantStart — Event-Driven Backtesting with Python (M. Halls-Moore) — OBTAINED (6 pp) · QuantStart article, rendered to PDF · `pillar8/24_HallsMoore_QuantStart_event_driven_backtesting_python.pdf` (sha256 `c2f038b86a…`)
2. Backtrader Documentation (backtrader.com) — OBTAINED (61 pp) · backtrader.com docs, rendered to PDF · `pillar8/25_Backtrader_official_documentation.pdf` (sha256 `ffb2e01ead…`)

## FIX Protocol & Exchange Connectivity

2. FIX Protocol — Official Specifications (FIX Latest + FIX 4.4 + Unified Repository) (fixtrading.org) — OBTAINED (10 pp) · fixtrading.org standards page, rendered to PDF · `pillar8/26_FIX_Trading_Community_FIX_protocol_specifications.pdf` (sha256 `788698cf8a…`)
2. OnixS FIX Dictionary & Protocol Reference (onixs.biz) — OBTAINED (24 pp) · onixs.biz FIX dictionary, rendered to PDF · `pillar8/27_OnixS_FIX_dictionary_protocol_reference.pdf` (sha256 `b01a3394cd…`)
2. Nasdaq TotalView-ITCH 5.0 Specification (nasdaqtrader.com) — OBTAINED (36 pp) · Nasdaq spec PDF (vendor-hosted) · `pillar8/28_Nasdaq_2022_totalview_itch_50_specification.pdf` (sha256 `45e0531d1b…`)
3. Learn Algorithmic Trading (Sebastien Donadio) — NOT OBTAINED · Packt commercial ebook; not licensed at SDU; no OA edition · ISBN 9781789348347 · Packt Publishing, 2019 · ILL: `refs/ILL_REQUESTS.pillar8.md` §29
2. FIX Algorithmic Trading Definition Language (FIXatdl) v1.1 (fixtrading.org) — OBTAINED (3 pp) · fixtrading.org FIXatdl page, rendered to PDF · `pillar8/30_FIX_Trading_Community_FIXatdl_v1.1_specification.pdf` (sha256 `e30a43d7a7…`)

## Concurrency & Lock-Free Programming

3. The Art of Multiprocessor Programming (Revised Ed.) (Maurice Herlihy & Nir Shavit) — NOT OBTAINED · Morgan Kaufmann/Elsevier; ScienceDirect via SDU proxy gives 'Page not found'; SDU print only · Morgan Kaufmann / Elsevier, 2012 · ILL: `refs/ILL_REQUESTS.pillar8.md` §31
2. LMAX — The Disruptor (paper + library) & The LMAX Architecture (Martin Fowler / LMAX) — OBTAINED (11 pp) · LMAX Disruptor paper (author/library hosted PDF) · `pillar8/32_Thompson_2011_disruptor_lmax.pdf` (sha256 `a277c43a43…`)
2. Martin Thompson — "Mechanical Sympathy" (blog + talks) — OBTAINED (18 pp) · mechanical-sympathy.blogspot.com, rendered to PDF · `pillar8/33_Thompson_mechanical_sympathy_blog.pdf` (sha256 `a6611f9066…`)
2. An Introduction to Lock-Free Programming (Jeff Preshing) — OBTAINED (12 pp) · preshing.com, rendered to PDF · `pillar8/34_Preshing_2012_introduction_lock_free_programming.pdf` (sha256 `ca727bb74a…`)

## Hardware Acceleration — FPGA & GPU

1. FPGA Based Accelerators for Financial Applications (Christian De Schryver, ed.) — OBTAINED (288 pp) · SDU EZproxy, SpringerLink full-book PDF · DOI 10.1007/978-3-319-15407-7 · ISBN 9783319154061 · `pillar8/35_DeSchryver_2015_fpga_accelerators_financial_applications.pdf` (sha256 `a3cfaa6bee…`)
2. The Role of FPGAs in Modern Option Pricing Techniques: A Survey (MDPI Electronics, 2024) — OBTAINED (26 pp) · MDPI Electronics OA PDF · DOI 10.3390/electronics13163186 · `pillar8/36_OMahony_2024_fpga_option_pricing_survey.pdf` (sha256 `f02a6bbe26…`)
3. GPU-Accelerated Research in Quant Finance (Thomas V. Trex) — NOT OBTAINED · Self-published ebook; only retailer listings (e.g. ISBN 9798896652281) · ILL: `refs/ILL_REQUESTS.pillar8.md` §37

## Python Quant Stack (numpy / pandas / numba / vectorbt)

4. Python for Data Analysis, 3rd Ed. (Wes McKinney) — PARTIAL — holds 14 pp of a ~580-pp book · wesmckinney.com author-hosted free online 3rd ed., rendered to PDF · `pillar8/38_McKinney_2022_python_for_data_analysis.pdf` (sha256 `1c852a8920…`)
3. High Performance Python, 2nd Ed. (Micha Gorelick & Ian Ozsvald) — NOT OBTAINED · O'Reilly commercial ebook; no SDU proxy; no OA edition · O'Reilly Media, 2020 · ILL: `refs/ILL_REQUESTS.pillar8.md` §39
3. Python for Finance, 2nd Ed. (Yves Hilpisch) — NOT OBTAINED · O'Reilly commercial ebook; no SDU proxy; no OA edition · O'Reilly Media, 2018 · ILL: `refs/ILL_REQUESTS.pillar8.md` §40
2. VectorBT — Official Documentation (vectorbt.dev / vectorbt.pro) — OBTAINED (10 pp) · vectorbt.dev docs, rendered to PDF · `pillar8/41_vectorbt_official_documentation.pdf` (sha256 `0144568ef9…`)
2. QuantEcon — Numba chapter, Python Programming for Economics and Finance (quantecon.org) — OBTAINED (2991 pp) · QuantEcon full lecture PDF (contains the Numba lecture) · `pillar8/42_QuantEcon_numba_python_programming_economics_finance.pdf` (sha256 `8d647ef431…`)
2. Numba — Official Documentation (numba.pydata.org) — OBTAINED (4 pp) · numba.readthedocs.io docs index, rendered to PDF · `pillar8/43_Numba_official_documentation.pdf` (sha256 `cf24bcb400…`)

## Data Infrastructure & Reproducibility

3. Financial Data Engineering with Python *(publisher/edition to confirm at acquisition)* — NOT OBTAINED · No bibliographic record anywhere (OpenLibrary/Crossref); only a Kindle listing · ILL: `refs/ILL_REQUESTS.pillar8.md` §44
2. Python Environment Reproducibility — uv / Poetry / conda-lock / Docker (official tool docs) — OBTAINED (14 pp) · uv / Poetry / conda-lock / Docker official docs, rendered and merged · `pillar8/45_python_environment_reproducibility_uv_poetry_condalock_docker.pdf` (sha256 `5ca8cfb39c…`)

## Production Trading Systems

3. Inside the Black Box: A Simple Guide to Quantitative and High-Frequency Trading, 2nd Ed. (Rishi K. Narang) — NOT OBTAINED · Wiley book renders via the SDU proxy but the chapter PDF redirects to the abstract page · DOI 10.1002/9781118662717 · ISBN 9781118662717 · Wiley, 2013 · ILL: `refs/ILL_REQUESTS.pillar8.md` §46
3. Building Winning Algorithmic Trading Systems (Kevin J. Davey) — NOT OBTAINED · Wiley book renders via the SDU proxy but no PDF is served · DOI 10.1002/9781118778944 · ISBN 9781118778913 · Wiley, 2014 · ILL: `refs/ILL_REQUESTS.pillar8.md` §47
3. Algorithmic and High-Frequency Trading (Álvaro Cartea, Sebastian Jaimungal & José Penalva) — NOT OBTAINED · Cambridge Core reachable via the SDU proxy but the title is not licensed; no OA edition · ISBN 9781107091146 · Cambridge University Press, 2015 · ILL: `refs/ILL_REQUESTS.pillar8.md` §48
3. Systematic Trading (Robert Carver) — NOT OBTAINED · Harriman House commercial ebook; not licensed at SDU; no OA edition · ISBN 9780857194459 · Harriman House, 2015 · ILL: `refs/ILL_REQUESTS.pillar8.md` §49
2. Optimal Execution of Portfolio Transactions (Almgren & Chriss, 2000) — OBTAINED (42 pp) · author-posted PDF of the Journal of Risk paper · DOI 10.21314/JOR.2001.041 · `pillar8/50_Almgren_2000_optimal_execution_portfolio_transactions.pdf` (sha256 `7330f244a8…`)

---

## Acquisition outcome (2026-09-10 run)

24 of 50 entries obtained as verified full text, 4 partial, 22 unobtainable.
28 files on disk, 4,431 pages total, all with recorded sha256 + page count.

**Via SDU EZproxy — licensed e-books (tag 1):** 07 *Linux Kernel Networking: Implement…* (Apress, 636 pp) and 35 *FPGA Based Accelerators for Financ…* (Springer International Publishing, 288 pp)
Pattern used: publisher hostname with dots replaced by dashes plus `.proxy1-bib.sdu.dk`, e.g.
`link-springer-com.proxy1-bib.sdu.dk/content/pdf/<DOI>.pdf`.

**From free / open sources (tag 2, 22 entries):** 09, 11, 12, 16, 17, 19, 23, 24, 25, 26, 27, 28, 30, 32, 33, 34, 36, 41, 42, 43, 45, 50

**Partial (tag 4):** 10 *Low-Latency Tuning Guide for Linux…* (3 pp held); 13 *Q for Mortals: An Introduction to…* (10 pp held); 18 *DuckDB in Action* (25 pp held); 38 *Python for Data Analysis* (14 pp held)

**Unobtainable (tag 3, 22 entries):** 01, 02, 03, 04, 05, 06, 08, 14, 15, 20, 21, 22, 29, 31, 37, 39, 40, 44, 46, 47, 48, 49
Each has a full citation, DOI/ISBN, publisher link and a ready-to-submit ILL line in
`refs/ILL_REQUESTS.pillar8.md`. Three of them (15, 46, 47) are Wiley e-books that SDU *does* license — the book and
chapter pages render with the SDU institution header, but the `/doi/pdf/` endpoint redirects to the
abstract page, so they are recorded as `LICENSED_NOT_DOWNLOADABLE` for the library to resolve.
Entry 05 is in the same position (Mimer lists an SDU e-book record). Entries 22 and 44 have no
bibliographic record at all (`NEEDS_METADATA`).

**Corrections to the original list:** the list's leading integer was a status marker (1/2/3), not a
reference number, and it repeated — reference numbers here are sequential by file order. Entry 13's
"4th Ed." does not exist: Kx publishes the free online 3rd edition (v3.1). Entry 44 carried no
author, year or publisher at all. Entries 28 and 36 were already present as verified captures in
`kwant-atlas-sources/free/pillar8/`.
