# Fundamentals & Accounting — Titles Acquisition List

> Compact 1/2/3 list derived from `corpus/fundamentals-accounting.md`, now carrying the
> acquisition outcome of the full sweep described below.
>
> **Status tags (rewritten to reflect reality after acquisition):**
> **1** = HAVE — verified full text on disk, path given inline · **2** = FREE, file or access note on
> disk (nothing left to acquire) · **3** = PAID / unobtainable — no SDU licence, no OA edition; each
> has an ISBN/DOI and an interlibrary-loan block.
>
> **Where the artefacts live:** `corpus/titles/refs/` (verified PDFs, `MANIFEST.json`,
> `MANIFEST.md`, `ILL_REQUESTS.md`, `_attempts.json` = every URL tried and its result).
> `refs/` is shared with the other acquisition runs, and each build unions its own snapshot back
> into `MANIFEST.json`; this list's authoritative copy is `refs/MANIFEST.fundamentals-accounting.TITLES.md.json`.
> Verification gates applied to every file: `%PDF` magic, pdftotext text layer, page count > 0,
> fuzzy title/author match; sha256 + page count recorded in the manifest.
> Original markers: `[manual]` (free paper, no file yet) is dropped once the file exists;
> `[data-access]` is kept since those entries stay data services.
> ISBN/publisher on tag-**3** lines are best-effort catalogue matches (OpenLibrary / SDU Primo
> Mimer), not verified order details — confirm the exact edition when submitting an ILL request.
> Entries **18, 19, 20** are pinned by hand because the raw catalogue record would have
> misdirected the request (reprint house, wrong imprint, foreign-language edition).

## Financial Statements / Accounting (from zero)
3. Financial Statements: A Step-by-Step Guide to Understanding and Creating Financial Reports (Thomas R. Ittelson) — SDU: not held as ebook · Career Press, 2009 · ILL: `refs/ILL_REQUESTS.md#01`
3. The Accounting Game: Basic Accounting Fresh from the Lemonade Stand (Darrell Mullis & Judith Orloff) — SDU: not held as ebook · Internet Archive: lending-only · ILL: `refs/ILL_REQUESTS.md#02`
3. The Interpretation of Financial Statements (Benjamin Graham & Spencer B. Meredith) — SDU: print only · Internet Archive: lending-only · ISBN 9780060115661 · HarperCollins, 1937 · ILL: `refs/ILL_REQUESTS.md#03`
3. Intermediate Accounting (Donald E. Kieso, Jerry J. Weygandt & Terry D. Warfield) — SDU: print only · ISBN 9780471426387 · Wiley, 1974 · ILL: `refs/ILL_REQUESTS.md#04`

## Financial Statement Analysis
3. Financial Statement Analysis and Security Valuation (Stephen H. Penman) — SDU: print only · ISBN 9780073379661 · McGraw-Hill/Irwin, 2001 · ILL: `refs/ILL_REQUESTS.md#05`
3. Accounting for Value (Stephen H. Penman) — SDU: print only · ISBN 9780231521857 · Columbia University Press, 2010 · ILL: `refs/ILL_REQUESTS.md#06`
3. Financial Statement Analysis (K. R. Subramanyam) — SDU: print only · ISBN 9780073379432 · McGraw-Hill/Irwin, 2009 · ILL: `refs/ILL_REQUESTS.md#07`
3. Business Analysis and Valuation: Using Financial Statements (Krishna Palepu & Paul Healy) — SDU: not held as ebook · ISBN 9781844804931 · Cengage, 2007 · ILL: `refs/ILL_REQUESTS.md#08`
3. Financial Statement Analysis: A Practitioner's Guide (Martin Fridson & Fernando Alvarez) — SDU: print only · ISBN 9780471409175 · Wiley, 2002 · ILL: `refs/ILL_REQUESTS.md#09`

## Core Financial Ratios — predictive frameworks
1. "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy" — Z-score (Edward I. Altman, JF 1968) — HAVE — full text `refs/10_Altman_1968_financial_ratios_discriminant_analysis.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1111/j.1540-6261.1968.tb00843.x
3. "Valuation Ratios and the Long-Run Stock Market Outlook" (John Y. Campbell & Robert J. Shiller, JPM 1998) — PAYWALLED — Journal of Portfolio Management is not in SDU's A-Z database list; pm-research via EZproxy 404s; Unpaywall/Semantic Scholar report closed access; no author copy found. Free alternative (different document): NBER WP 8221 `Valuation Ratios…: An Update` (2001) — https://www.nber.org/system/files/working_papers/w8221/w8221.pdf · ILL: `refs/ILL_REQUESTS.md#11`
1. "Financial Ratios and the Probabilistic Prediction of Bankruptcy" — O-score (James Ohlson, JAR 1980) — HAVE — full text `refs/12_Ohlson_1980_financial_ratios_probabilistic_prediction.pdf` · via SDU EZproxy (jstor.org/stable/2490395) · DOI 10.2307/2490395
3. Corporate Financial Distress and Bankruptcy (Edward I. Altman) — SDU: print only · ISBN 9780471691891 · Wiley, 1993 · ILL: `refs/ILL_REQUESTS.md#13`

## Equity Valuation
3. Investment Valuation: Tools and Techniques for Determining the Value of Any Asset (Aswath Damodaran) — SDU: not held as ebook · Internet Archive: lending-only · ILL: `refs/ILL_REQUESTS.md#14`
3. The Dark Side of Valuation: Valuing Young, Distressed, and Complex Businesses (Aswath Damodaran) — SDU: not held as ebook · no IA/OL copy · ILL: `refs/ILL_REQUESTS.md#15`
3. Valuation: Measuring and Managing the Value of Companies (Tim Koller, Marc Goedhart & David Wessels, McKinsey) — SDU: print only · ISBN 9781394279470 · John Wiley & Sons, Inc., 2025 · ILL: `refs/ILL_REQUESTS.md#16`
3. Equity Asset Valuation (Jerald E. Pinto, Elaine Henry, Thomas R. Robinson & John D. Stowe, CFA Institute) — SDU: print only · ISBN 9780470579657 · Wiley, 2010 · ILL: `refs/ILL_REQUESTS.md#17`
3. The Theory of Investment Value (John Burr Williams) — Internet Archive: lending-only · in copyright (US); public-domain scan not available · Harvard University Press (orig. 1938) · ILL: `refs/ILL_REQUESTS.md#18`

## Fundamental Analysis & Screening (Graham school)
3. Security Analysis (Benjamin Graham & David Dodd) — Internet Archive: lending-only · ISBN 9780071412285 · McGraw-Hill (6th ed.), 1934 · ILL: `refs/ILL_REQUESTS.md#19`
3. The Intelligent Investor (Benjamin Graham) — SDU: print only · ISBN 9780060752613 · HarperBusiness (2005 ed.) · ILL: `refs/ILL_REQUESTS.md#20`
3. Common Stocks and Uncommon Profits and Other Writings (Philip A. Fisher) — Internet Archive: lending-only · ISBN 9780471119289 · Wiley, 1996 · ILL: `refs/ILL_REQUESTS.md#21`
3. Value Investing: From Graham to Buffett and Beyond (Bruce Greenwald, Judd Kahn, Paul Sonkin & Michael van Biema) — SDU: not held as ebook · no IA/OL copy · ILL: `refs/ILL_REQUESTS.md#22`
3. The Five Rules for Successful Stock Investing (Pat Dorsey, Morningstar) — Internet Archive: lending-only · ISBN 9780471647775 · Wiley, 2003 · ILL: `refs/ILL_REQUESTS.md#23`

## Capital Structure & Corporate Finance
3. Principles of Corporate Finance (Richard Brealey, Stewart Myers & Franklin Allen) — SDU: print only · ISBN 9781260013900 · McGraw-Hill, 1981 · ILL: `refs/ILL_REQUESTS.md#24`
3. Corporate Finance (Jonathan Berk & Peter DeMarzo) — Internet Archive: lending-only · ISBN 9780134101477 · Prentice Hall, 2006 · ILL: `refs/ILL_REQUESTS.md#25`
3. Applied Corporate Finance (Aswath Damodaran) — Internet Archive: lending-only · ISBN 9780471206521 · Wiley, 2001 · ILL: `refs/ILL_REQUESTS.md#26`
3. The Theory of Corporate Finance (Jean Tirole) — SDU: print only · ISBN 9780691125565 · Princeton University Press, 2006 · ILL: `refs/ILL_REQUESTS.md#27`
3. Financial Markets and Corporate Strategy (Mark Grinblatt & Sheridan Titman) — Internet Archive: lending-only · ISBN 9780071157612 · McGraw-Hill, 1998 · ILL: `refs/ILL_REQUESTS.md#28`
1. "The Cost of Capital, Corporation Finance and the Theory of Investment" — M&M (Franco Modigliani & Merton H. Miller, AER 1958) — HAVE — full text `refs/29_Modigliani_1958_the_cost_of_capital_corporation_finance.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.2307/1809766
1. "Corporate Financing and Investment Decisions When Firms Have Information That Investors Do Not Have" — pecking order (Stewart C. Myers & Nicholas S. Majluf, JFE 1984) — HAVE — full text `refs/30_Myers_1984_corporate_financing_and_investment.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1016/0304-405X(84)90023-0
1. "Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure" (Michael C. Jensen & William H. Meckling, JFE 1976) — HAVE — full text `refs/31_Jensen_1976_theory_of_the_firm_managerial_behavior.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1016/0304-405X(76)90026-X
1. "Agency Costs of Free Cash Flow, Corporate Finance, and Takeovers" (Michael C. Jensen, AER 1986) — HAVE — full text `refs/32_Jensen_1986_agency_costs_of_free_cash_flow.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.2307/1818789

## Accounting Quality & Red Flags
3. Financial Shenanigans: How to Detect Accounting Gimmicks and Fraud in Financial Reports (Howard M. Schilit, Jeremy Perler & Yoni Engelhart) — SDU: not held as ebook · no IA/OL copy · ILL: `refs/ILL_REQUESTS.md#33`
3. The Financial Numbers Game: Detecting Creative Accounting Practices (Charles W. Mulford & Eugene E. Comiskey) — SDU: print only · Internet Archive: lending-only · ISBN 0471370088 · Wiley, 2002 · ILL: `refs/ILL_REQUESTS.md#34`
3. Quality of Earnings (Thornton L. O'Glove) — Internet Archive: lending-only · ISBN 9780684863757 · Free Press, 1987 · ILL: `refs/ILL_REQUESTS.md#35`
1. "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" — accruals anomaly (Richard G. Sloan, TAR 1996) — HAVE — full text `refs/36_Sloan_1996_do_stock_prices_fully_reflect.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.2308/tar-9608042309
1. "Detecting Earnings Management" — modified-Jones model (Patricia M. Dechow, Richard G. Sloan & Amy P. Sweeney, TAR 1995) — HAVE — full text `refs/37_Dechow_1995_detecting_earnings_management.pdf` · via SDU EZproxy (jstor.org/stable/248303) · DOI 10.2308/tar-9505096112
1. "The Detection of Earnings Manipulation" — M-score (Messod D. Beneish, FAJ 1999) — HAVE — full text `refs/38_Beneish_1999_detection_earnings_manipulation.pdf` · via SDU EZproxy (tandfonline.com/doi/pdf/10.2469/faj.v55.n5.2296) · DOI 10.2469/faj.v55.n5.2296
1. "A Review of the Earnings Management Literature and Its Implications for Standard Setting" (Paul M. Healy & James M. Wahlen, Accounting Horizons 1999) — HAVE — full text `refs/39_Healy_1999_a_review_of_the_earnings_management.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.2308/acch.1999.13.4.365
1. "Understanding Earnings Quality: A Review of the Proxies, Their Determinants and Their Consequences" (Patricia Dechow, Weili Ge & Catherine Schrand, JAE 2010) — HAVE — full text `refs/40_Dechow_2010_understanding_earnings_quality_a_review.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1016/j.jacceco.2010.09.001
1. "Earnings Quality and Stock Returns" (Louis K. C. Chan, Narasimhan Jegadeesh & Josef Lakonishok, JF 2006) — HAVE — full text `refs/41_Chan_2006_earnings_quality_and_stock_returns.pdf` · via SDU EZproxy (jstor.org/stable/10.1086/500669) · DOI 10.1086/500669

## Quantitative Fundamental Investing — factors & evidence
1. "An Empirical Evaluation of Accounting Income Numbers" (Ray Ball & Philip Brown, JAR 1968) — HAVE — full text `refs/42_Ball_1968_empirical_evaluation_accounting_income.pdf` · via SDU EZproxy (jstor.org/stable/2490232) · DOI 10.2307/2490232
1. "The Cross-Section of Expected Stock Returns" (Eugene F. Fama & Kenneth R. French, JF 1992) — HAVE — full text `refs/43_Fama_1992_cross_section_expected_stock_returns.pdf` · via SDU EZproxy (onlinelibrary.wiley.com/doi/pdfdirect/10.1111/j.1540-6261.1992.tb04398.x) · DOI 10.2307/2329112
1. "Common Risk Factors in the Returns on Stocks and Bonds" (Eugene F. Fama & Kenneth R. French, JFE 1993) — HAVE — full text `refs/44_Fama_1993_common_risk_factors_in_the_returns_on.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1016/0304-405X(93)90023-5
1. "A Five-Factor Asset Pricing Model" (Eugene F. Fama & Kenneth R. French, JFE 2015) — HAVE — full text `refs/45_Fama_2015_a_five_factor_asset_pricing_model.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1016/j.jfineco.2014.10.010
1. "The Other Side of Value: The Gross Profitability Premium" (Robert Novy-Marx, JFE 2013) — HAVE — full text `refs/46_Novy-Marx_2013_the_other_side_of_value_the_gross.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1016/j.jfineco.2013.01.003
1. "Digesting Anomalies: An Investment Approach" — q-factor (Kewei Hou, Chen Xue & Lu Zhang, RFS 2015) — HAVE — full text `refs/47_Hou_2015_digesting_anomalies_an_investment.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1093/rfs/hhu068
1. "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" — F-score (Joseph D. Piotroski, JAR 2000) — HAVE — full text `refs/48_Piotroski_2000_value_investing_f_score.pdf` · via SDU EZproxy (jstor.org/stable/2672906) · DOI 10.2307/2672906
1. "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns" (Jeremiah Green, John R. M. Hand & X. Frank Zhang, RFS 2017) — HAVE — full text `refs/49_Green_2017_the_characteristics_that_provide.pdf` · free copy from the earlier free-source pass (`kwant-atlas-sources/free/fundamentals-accounting/`) · DOI 10.1093/rfs/hhx019
1. "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?" (Victor L. Bernard & Jacob K. Thomas, JAR 1989) — HAVE — full text `refs/50_Bernard_1989_post_earnings_announcement_drift.pdf` · via SDU EZproxy (jstor.org/stable/2491062) · DOI 10.2307/2491062
3. The Little Book That Beats the Market (Joel Greenblatt) — Internet Archive: lending-only · ISBN 9780470893661 · Simon & Schuster, 2005 · ILL: `refs/ILL_REQUESTS.md#51`
3. Quantitative Value: A Practitioner's Guide to Automating Intelligent Investment and Eliminating Behavioral Errors (Wesley R. Gray & Tobias E. Carlisle) — SDU: print only · ISBN 9781119205456 · Wiley, 2012 · ILL: `refs/ILL_REQUESTS.md#52`
3. What Works on Wall Street: The Classic Guide to the Best-Performing Investment Strategies (James P. O'Shaughnessy) — no IA/OL copy · ILL: `refs/ILL_REQUESTS.md#53`

## Data Sources & Corporate Data
2. SEC EDGAR — company filings, XBRL financial statements, structured APIs [data-access] — not a document (no PDF sought); access only · access note `kwant-atlas-sources/free/fundamentals-accounting/Data_SEC_EDGAR_access.txt` · https://www.sec.gov/edgar/sec-api-documentation
2. WRDS — Compustat (+ CRSP linkage) — not a document (no PDF sought); access only · https://wrds-www.wrds.upenn.edu/
2. Compustat Point-in-Time (WRDS PIT) — not a document (no PDF sought); access only · https://wrds-www.wharton.upenn.edu/pages/get-data/compustat-capital-iq-standard-poors/
2. Kenneth R. French Data Library — factor return series [data-access] — not a document (no PDF sought); access only · access note `kwant-atlas-sources/free/fundamentals-accounting/Data_KenFrench_DataLibrary_access.txt` · https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
2. XBRL US-GAAP / IFRS taxonomies [data-access] — not a document (no PDF sought); access only · access note `kwant-atlas-sources/free/fundamentals-accounting/Data_XBRL_Taxonomies_access.txt` · https://xbrl.us/xbrl-taxonomy/
1. "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks" (Tim Loughran & Bill McDonald, JF 2011) — HAVE — full text `refs/59_Loughran_2011_when_is_liability_not_liability.pdf` · via SDU EZproxy (jstor.org/stable/29789771) · DOI 10.1111/j.1540-6261.2010.01625.x

---

## Acquisition outcome (this pass)

22 of 59 entries obtained as verified full text, 5 are free data/access services
(not documents), 32 unobtainable — the latter are all commercial in-copyright books except
Campbell & Shiller 1998 (see entry 11).

- Obtained: entries tagged **1** (all in `refs/`, listed with sha256 and page count in `MANIFEST.md`).
- Unobtainable: every entry tagged **3**, with DOI/ISBN and a ready-to-submit ILL line in
  `refs/ILL_REQUESTS.md`.
- Not documents: entries 54–58 (`SEC EDGAR`, `WRDS`, `Compustat PIT`, `Ken French`, `XBRL`) are data
  services — access notes only, no PDF.
- Correction to this list: entries **12, 38, 50** were tagged `[manual]` (expected unobtainable) but
  were retrieved in full; entry **11** was tagged free/on-disk but no usable file existed, so it is
  the one paper still outstanding.

### DOI provenance (22 obtained papers)

- **Crossref-confirmed (16)**: printed among the Crossref candidates for that title — 10, 30, 31, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49.
- **Pinned from the publisher/JSTOR record (6)**: Crossref's ranking missed or returned nothing, so the DOI was read off the article page and checked against the title before the download:

  - **12** — `10.2307/2490395` — JSTOR stable 2490395 (Download link on the article page)
  - **29** — `10.2307/1809766` — JSTOR stable 1809766; page `<meta og:title>` matched before download
  - **32** — `10.2307/1818789` — JSTOR stable 1818789; page `<meta og:title>` matched before download
  - **38** — `10.2469/faj.v55.n5.2296` — Taylor & Francis article page (FAJ 55(5), 24–36)
  - **50** — `10.2307/2491062` — JSTOR stable 2491062; page `<meta og:title>` matched before download
  - **59** — `10.1111/j.1540-6261.2010.01625.x` — Wiley / JSTOR article page (JF 66(1), 35–65)

- Raw metadata responses for this list are cached in `refs/_meta_cache.json` (Crossref / OpenAlex / OpenLibrary); every download attempt and its result is in `refs/_attempts.json`.
- `refs/_meta.json` is **not** this list's cache: the concurrent pillar-1 run in the same directory writes and overwrites it. Audit only against `_meta_cache.json`.
- Re-audit: `python3 scripts/check_dois.py` (DOI provenance) and `python3 scripts/check_titles.py` (file + pointer integrity).

