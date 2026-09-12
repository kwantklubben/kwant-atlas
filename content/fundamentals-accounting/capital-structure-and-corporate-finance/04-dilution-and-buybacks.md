---
title: "A.6.4 Dilution & Buybacks"
tags:
  - fundamentals-accounting
  - capital-structure-and-corporate-finance
  - dilution
  - buybacks
  - dividends
---

**Basic Prerequisites:** [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]] and [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03 · Debt, Equity & Seniority]].

---

### 1. Intuition & Practical Objective

The number of shares and how it changes is where capital structure meets shareholder value. **Dilution** and **buybacks** are the two levers that change the share count, and both are routinely *misunderstood* through the lens of the single most-gamed accounting number in finance: **EPS** = net income ÷ shares outstanding.

The objective of this page is the discipline that separates the *arithmetic* from the *economics*:

- **Dilution is a wealth transfer, not just a math problem.** When a firm issues new shares, it sells part of the residual claim. If it issues at a price *below* what the shares are intrinsically worth, value flows from **old holders to new holders** - this is the exact mechanism of the Myers–Majluf "underinvestment" trap in [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]].
- **A buyback's EPS accretion is mechanical, not value-creating.** Retiring shares raises EPS by construction ($NI$ ÷ fewer shares). But the cash spent was an *earning asset*; if it was earning at the cost of capital, the buyback destroys exactly the earnings it appears to create. The honest test is **ROIC**: does the firm have projects that beat the cost of capital? If yes, *reinvest*; if no, *pay out* (Jensen 1986's free-cash-flow point).
- **Dividends and buybacks are the same value decision.** Both return cash to shareholders. Which is better is a *tax and signaling* question, not a value question - under MM's frictionless world, payout policy doesn't change firm value at all (irrelevance), and the real question is only *whether the cash should leave at all* (agency - see [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]]).

---

### 2. Mathematical Ground Truth & Derivations

**EPS mechanics.** With $NI$ net income and $n$ shares outstanding,

$$
\text{EPS} = \frac{NI}{n}.
$$

A buyback of $b$ shares (cash spent $= b \cdot P$) leaves $n-b$ shares, so *ceteris paribus* $\text{EPS} = \frac{NI}{n-b} > \frac{NI}{n}$ - **EPS always rises from a buyback.** The trap is the *ceteris paribus*: if the $bP$ of cash was generating earnings at the firm's return on assets $a$, then true net income falls to $NI - bP \cdot a$, and the honest post-buyback EPS is $\frac{NI - bP\,a}{n-b}$. Whether EPS truly rose depends on $a$ vs. the *return the market required on the equity retired* - i.e., vs. the cost of equity, which is exactly where ROIC enters.

**The payout-vs-reinvest decision (Jensen 1986).** Define *free cash flow* as cash flow in excess of what all positive-NPV projects require. For a firm with free cash flow $FCF$ and required return $\rho$ (its cost of capital), investing the cash in a project returning $g < \rho$ *destroys* value:

$$
\text{NPV of reinvesting} = \underbrace{\frac{FCF \cdot g}{\rho}}_{\text{PV of the weak project}} - FCF < 0.
$$

The value-maximizing choice is to **pay the cash out** (dividend or buyback) when $g < \rho$, and to **reinvest** only when $g \ge \rho$. This is the dividend-policy-vs-ROIC rule: the payout decision is governed by whether internal reinvestment earns above the cost of capital, not by any virtue of paying dividends per se.

**Dilution as wealth transfer.** Let firm value be $V$ with $n$ shares (intrinsic value $V/n$). Issuing $m$ new shares at price $p < V/n$ (as under information asymmetry, [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]]) raises $mp$ of cash. New value and per-share value:

$$
V' = V + mp, \qquad \text{per-share} = \frac{V + mp}{n + m}.
$$

Old holders' stake becomes $\frac{n}{n+m}V'$; the shortfall $\frac{V}{n}$ vs. per-share is a **transfer from old to new holders**. When that transfer exceeds the project's NPV, old holders are *worse off* by investing - the Myers–Majluf underinvestment result.

---

### 3. Computational Implementation - dilution transfer and buyback EPS, stdlib only

Runs on the standard library. First quantifies the wealth transfer when shares are issued *below* intrinsic value (the dilution risk); then shows a buyback's EPS accretion and the ROIC test that exposes it as arithmetic, not value.





The dilution panel is the red flag: issuing at $8$ when shares are worth $10$ hands **$40$ of old-holder value to new holders** - exactly why managers resist equity issues (bad-news signal) and why dilution risk matters. The buyback panel is the EPS illusion: the naive EPS jumps to $1.556$, but once you subtract the earnings the spent cash would have produced, the "accretion" mostly evaporates ($1.478$) - no value was created by the repurchase itself.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Celebrating EPS accretion as value.** A buyback that raises EPS while the repurchased cash earned at the cost of capital creates *zero* shareholder value - it only changed the denominator. The failure is reading the arithmetic without the ROIC test (did the firm have a positive-NPV use for the cash?).
2. **Missing dilution as a wealth transfer.** Issuing below intrinsic value silently moves value from old to new holders. The "dilution" is not the share-count math (that's inevitable when raising equity) - it is *the gap between issue price and intrinsic value*. Under information asymmetry that gap is the whole problem (Myers–Majluf).
3. **"Buybacks are always good" / "dividends are always good."** Both are ways to return cash; the *correct* question (Jensen 1986) is whether the cash should leave at all. Paying out when ROIC > cost of capital (plenty of good projects) destroys growth; hoarding when ROIC < cost of capital destroys value through weak reinvestment.
4. **Forgetting that payout policy is value-irrelevant under MM.** Dividends vs. buybacks differ in taxes and signal content, not in the underlying value transfer. A firm can change its payout *form* endlessly without creating value - only the *decision to return vs. reinvest cash* against ROIC creates or destroys it.
5. **Ignoring the signaling read of both actions.** Because issuing is a bad-news signal and buybacks/dividends a good-news signal (asymmetric information), the *announcement* moves price even when the cash-flow economics are neutral - a real, if information-driven, channel the arithmetic alone misses.

---

### 5. Canonical Literature & Study References

- **Myers & Majluf**, "Corporate Financing and Investment Decisions…" (*JFE*, 1984) - the issue-below-intrinsic wealth transfer and the underinvestment trap; the formal dilution channel. *Verified against the paper text.*
- **Jensen**, "Agency Costs of Free Cash Flow…" (*AER*, 1986) - the free-cash-flow / payout-vs-reinvest rule (reinvest only if ROIC ≥ cost of capital). *Verified against the paper text.*
- **Brealey, Myers & Allen**, *Principles of Corporate Finance*, Ch 16 - dividend policy, buybacks, and the MM dividend-irrelevance result.
- **Graham & Dodd**, *Security Analysis* (6th ed.) - the classic warning that warrants and convertibles "siphon off" part of future appreciation from common holders (the original dilution concern).
- **Damodaran**, *Applied Corporate Finance* - dividend and buyback decisions for real firms, with the sustainable-payout framework.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03 · Debt, Equity & Seniority]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Index Hub]]
- Forward: [[fundamentals-accounting/capital-structure-and-corporate-finance/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06 · Advanced Extensions]]
- Valuation link: [[fundamentals-accounting/equity-valuation/index|Equity Valuation - DCF & payout]] · [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|Core Financial Ratios - ROIC]]
