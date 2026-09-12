---
title: "A.3.1 Equity Valuation from Zero"
tags:
  - fundamentals-accounting
  - equity-valuation
  - intuition
  - present-value
  - dcf
---

**Basic Prerequisites:** none - this page assumes no accounting or finance background.

---

### 1. Intuition & Practical Objective

This page builds the *why* of equity valuation with **no prior knowledge needed**. The objective is one idea: **a share is a claim on a stream of future cash, so its value today is that stream discounted back at a rate that reflects how risky the stream is.**

Start with the dumbest question: *why is a share worth anything at all?* Not because someone else might pay more for it tomorrow - that is a bet on a greater fool. It is worth something because owning it entitles you to a share of the cash the business will generate: dividends, buybacks, or the proceeds of a sale. Strip the ticket-tape away and **a stock is a claim on cash flows that have not happened yet.**

Three steps, three "aha"s:

1. **Value is about the future, not the past.** A firm with beautiful historical earnings and no prospect of future cash is worth little; a firm with losses today but a dominant, cash-generating future can be worth a fortune. Accounting measures *what happened*; valuation measures *what is expected*.

2. **Discounting is the price of waiting and of risk.** A dollar promised in ten years is worth less than a dollar today - partly because you could invest today's dollar (the *time value*), and partly because the promise might not be kept (the *risk premium*). The discount rate bundles both.

3. **Growth is only worth paying for when it earns above the cost of capital.** Investing more cash to grow faster *destroys* value if the return on that investment is below the discount rate. This single insight separates value investing from "growth at any price".

> **The one-sentence essence.** "Intrinsic value $=\sum_t \dfrac{\text{expected cash}_t}{(1+r)^t}$ - and growth is a *good* thing only when the return on reinvested cash exceeds $r$."

---

### 2. Mathematical Ground Truth & Derivations

**Present value of an explicit stream.** If the owner expects cash $C_1,C_2,\dots,C_n$ and then a terminal amount $V_n$, then today's value is

$$
V_0=\sum_{t=1}^{n}\frac{C_t}{(1+r)^t}+\frac{V_n}{(1+r)^n}.
$$

**The growing perpetuity (Gordon) shortcut.** If cash starts at $C_1$ and grows forever at constant $g<r$,

$$
V_0=\sum_{t=1}^{\infty}\frac{C_1(1+g)^{t-1}}{(1+r)^t}=\boxed{\dfrac{C_1}{r-g}}.
$$

This is the algebraic backbone of every terminal value (page 04). Two facts follow immediately and are worth memorising:

- **The value is dominated by the tail.** At $C_1=100$, $r=10\%$, $g=3\%$, the perpetuity is worth $1428.57$; the first ten years are only $48.2\%$ of it. More than *half* of the value sits in years 11 and beyond - which is exactly why the terminal value (page 04) and its assumptions dominate DCF output.
- **The denominator is fragile.** Both $r$ and $g$ move value inversely and *non-linearly*: raising $g$ from $3\%$ to $4\%$ adds $238$, a $16.7\%$ jump, on a single percentage point.

**Where growth creates value.** A firm growing at $g$ must reinvest to fund that growth. With a return on capital $\text{ROC}$, the reinvestment rate is $\text{RR}=g/\text{ROC}$, so the cash flow is

$$
\text{FCF}_1=\text{NOPAT}_1\,(1-\text{RR})=\text{NOPAT}_1\Big(1-\frac{g}{\text{ROC}}\Big),\qquad V_0=\frac{\text{NOPAT}_1\,(1-g/\text{ROC})}{r-g}.
$$

When $\text{ROC}=r$ this collapses to $V_0=\text{NOPAT}_1/r$ - **growth adds nothing**. When $\text{ROC}>r$ growth adds value; when $\text{ROC}<r$ growth *destroys* it. This is the fundamental growth equation that page 02 makes concrete.

---

### 3. Computational Implementation - present value, from scratch

Stdlib only. Part A shows the mechanics of discounting and the tail-dominance fact; Part B shows the growth/ROC value logic.



Read the table carefully: **the same earnings and the same growth rate produce values from $588.6$ to $1324.3$ purely as a function of the return on reinvested capital.** A firm earning $5\%$ on reinvestment while its cost of capital is $10\%$ is worth *less* than a no-growth firm - it is destroying value by growing.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "greater fool" confusion.** Treating price as value substitutes market sentiment for cash-flow fundamentals. Intrinsic value is a claim on cash; market price is a negotiation. Confusing them is the root of momentum-bubble losses.
2. **Growth ≠ value.** The single most expensive beginner error: assuming faster growth is always worth more. Growth only creates value when $\text{ROC}>r$; below that it is a value incinerator (see Part B: value falls from $1030$ to $588.6$).
3. **Ignoring the terminal tail.** Because $>50\%$ of value sits beyond year 10, a "conservative" five-year spreadsheet can still hide an aggressive perpetuity assumption. Never read a DCF without asking what fraction of value is terminal (page 04).
4. **Time-value/risk conflation.** The discount rate is not one number: it is $r_f$ (waiting) + a risk premium (uncertainty). Using a single "hurdle rate" for every firm ignores that risk differs across businesses, and that cash flows and discount rates must be matched (page 03).

---

### 5. Canonical Literature & Study References

- **John Burr Williams**, *The Theory of Investment Value* (1938) - the origin of the dividend/present-value framework; the intellectual root of this page.
- **Damodaran**, *Investment Valuation*, Ch 1–2 (why valuation matters; cash-flow/discount-rate matching) and Ch 11 (the fundamental growth equation, $\text{RR}=g/\text{ROC}$).
- **Graham**, *The Intelligent Investor*, Ch 8 & 20 - the "margin of safety" frame that this arithmetic exists to serve (see [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes]]).
- **Pinto et al. (CFA Institute)**, *Equity Asset Valuation*, Ch 1–2 - the professional overview of the value-driver tree.

---

### 6. Connected Graph Bridges

- Forward: [[fundamentals-accounting/equity-valuation/02-cash-flow-forecasting|02 · Cash-Flow Forecasting]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Downstream: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (value/quality factors)
