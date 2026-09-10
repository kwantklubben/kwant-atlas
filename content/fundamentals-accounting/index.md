---
title: "Fundamentals & Accounting: The Cross-Cutting Area Hub"
tags:
  - fundamentals-accounting
  - accounting
  - equity-analysis
  - cross-cutting-area
  - index-hub
---

> 🔎 **Looking something up?** Jump to the [[glossary|Glossary]] for a term/symbol, or the [[diagnostics|Diagnostic Index]] for a symptom → cause → fix.

# Fundamentals & Accounting

> *"The numbers nominate; the business case confirms."*

**Fundamentals & Accounting** is the Atlas's cross-cutting area — it sits *alongside* the **8 operational pillars** and the shared **Foundations toolbox**, not inside either. Where the pillars teach the machinery of alpha, execution, pricing, risk, optimization, market making, machine learning, and engineering, this area covers the **company underneath every security**: how its business is reported (statements), how that reporting is turned into signals (ratios, screens, factors), what the claim is worth (valuation), how it is financed (capital structure), when the reporting lies (quality & red flags), and where the raw facts come from (data provenance).

It matters to **both** audiences:

- **Quantitative projects** consume fundamental data at scale — Fama–French and Barra style factors, value/profitability/investment sorts, point-in-time fundamental panels — and an unwittingly wrong as-of date or a naive restatement policy silently destroys a backtest.
- **Discretionary / fundamental projects** live or die on reading the filings, judging accrual quality, and building a defensible valuation — the Graham–Buffett–Penman line of reasoning.

The two are the same discipline viewed at different frequencies: *the accounting is the ground truth; the quant layer is what you do once that ground truth is machine-readable and honest.*

---

## 📚 Core Topics

1. **[[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]]** — The scoreboard of a business: the accounting equation, double-entry, the three statements (balance sheet, income statement, cash flow), and accrual vs cash.
2. **[[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]]** — Relate every flow to the stock that earned it: profitability (ROE, ROIC), valuation multiples (P/E, EV/EBITDA), liquidity, leverage, and the ratio lookup table.
3. **[[fundamentals-accounting/equity-valuation/index|Equity Valuation]]** — What is a claim on a business worth today: discounted cash flow, cost of equity vs WACC, terminal value, multiples and comps, and the margin of safety.
4. **[[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]]** — Turn the ratio catalog into candidate lists: Graham-style value criteria, mechanical screen rules, and the "screen to nominate, read to reject" workflow.
5. **[[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]** — The defense layer: accruals anomaly, earnings management, Beneish's M-score, Sloan's accruals, and the checklist for when reported numbers cannot be trusted.
6. **[[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]]** — How a firm pays for itself: Modigliani–Miller irrelevance and its frictions, the tax shield vs distress/agency costs, and payout policy.
7. **[[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]]** — Turn accounting characteristics into *priced factors*: value, profitability, investment, accruals and the F-score, systematic sorts, and long-horizon premia.
8. **[[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]** — Provenance and timing: filings (SEC EDGAR, XBRL), vendors, restatements, and point-in-time / as-of hygiene to keep backtests honest.

---

## 🧭 Reading Path

**Beginner (new to accounting):** start at the on-ramp and climb.
**1 → 2 → 3 → 4.** Topic 1 gives you what a balance sheet *is*; topic 2 turns those statements into ratios you can actually interpret; topic 3 asks what the business is worth; topic 4 turns valuation into mechanical candidate lists. With those four you can read a 10-K, compute the standard ratios, and run a first screen.

**Practitioner (quant or analyst):** the same spine, then the robustness layer.
**2 (decomposition) → 5 → 6 → 7 → 8.** Ratio *decomposition* (ROE = RNOA + FLEV×SPREAD) is the analytical core; **5** tells you when the inputs are gamed, **6** gives the corporate-finance theory behind leverage and coverage, **7** scales everything into cross-sectional factors, and **8** is the non-negotiable plumbing that keeps a fundamental backtest from reading the future through a restated database.

In short: **beginner goes top-down (statements → ratios → valuation → screens); the practitioner goes bottom-up on rigor (decompose → distrust → ground in provenance → scale into factors).**

---

## 🔗 Where This Area Connects

- **[[pillars/01-quantitative-research/index|Pillar 1 · Quantitative Research]]** — fundamental multi-factor models (Fama–French, Barra) are built directly on this area's data; see [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]].
- **[[pillars/05-portfolio-optimization/index|Pillar 5 · Portfolio Optimization]]** — value/quality/profitability factors become the inputs to portfolio construction and risk models.
- **[[pillars/07-machine-learning-altdata/index|Pillar 7 · Machine Learning & AltData]]** — filings, earnings transcripts, and XBRL feeds are the alternative/structured data this area's topics feed.
- **[[foundations/index|First-Principles Toolbox & Foundations]]** — the mathematics (statistics, econometrics, linear algebra) that underpins factor testing and valuation.
