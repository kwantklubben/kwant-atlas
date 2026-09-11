---
title: "01 — Basel & Regulation from Zero: Why Banks Are Regulated"
tags:
  - pillar-quantitative-risk
  - basel-and-regulation
  - intuition
  - bank-capital
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (what "risk" means before it becomes a rule).

---

### 1. Intuition & Practical Objective

This page builds the *why* of bank regulation with **no prior regulatory knowledge needed**. The objective is one idea: **a bank is a leveraged, systemically important, partly-subsidised institution, and "capital" is the loss-absorbing buffer that makes its failure (a) less likely and (b) survivable without a taxpayer bailout.**

Start with the dumbest question: *why can't a bank just take any risk it likes with depositors' money?* Because four things break the ordinary discipline of the market:

1. **Leverage.** A bank funds itself mostly with debt (deposits, wholesale borrowing) and only a sliver of equity. At an 8% capital ratio a bank holds roughly **12.5 dollars of assets per dollar of equity** — so a 1% loss on assets is a **~12.5%** hit to equity. Leverage magnifies both return *and* ruin.
2. **Deposit insurance and the lender of last resort.** Once deposits are insured and the central bank stands ready to lend, depositors stop policing the bank's risk — and the bank gains an incentive to take *more* risk, since the upside is private and the downside is social. This is **moral hazard**.
3. **Contagion / externalities.** A bank's failure is not a private event: it freezes interbank funding and payment systems, hurting solvent bystanders. The private cost of failure is far below the social cost.
4. **Opacity.** Outsiders cannot easily see how risky a bank's book is, so market discipline is weak and slow.

Regulation is the response: force the bank's *owners* to hold a minimum equity cushion so that losses fall on them first, and standardise how much cushion each type of risk demands. That is **capital regulation**, and its skeleton is one number — the ratio of capital to **risk-weighted assets**.

Three "aha"s:

1. **Capital ≠ cash.** In regulation, "capital" means *equity and equity-like funding* (CET1), not the vault. It is the part of the funding that absorbs losses without triggering default, because it ranks last in a liquidation.
2. **Risk weighting is the whole game.** A dollar of cash and a dollar of unrated corporate loan are not equally risky; the framework scales each by a **risk weight** before summing. The dispute over *how* to weight is where most of Basel's complexity lives.
3. **A ratio is a shock absorber, and the arithmetic is shockingly blunt.** If a bank has an $r\%$ capital ratio against fully-weighted assets, a loss of $r\%$ of those assets wipes it out. An 8% ratio buys an 8% loss budget — thin, which is why the post-2008 reforms added buffers on top.

---

### 2. Mathematical Ground Truth & Derivations

**The buffer identity.** Let $A$ be assets, $E$ equity, and suppose for the moment all assets carry weight 100%, so $\mathrm{RWA}=A$. The capital ratio is
$$
r=\frac{E}{A},\qquad \text{so}\qquad \frac{A}{E}=\frac1r .
$$
A proportional loss of $L$ (dollars) on the assets leaves equity $E-L$, hence
$$
r_{\text{after}}=\frac{E-L}{A}=r-\frac{L}{A}.
$$
Setting $r_{\text{after}}=0$ gives the **maximum absorbable loss** $L^{*}=E=r\,A$ — i.e. the capital ratio *is* the loss budget (when risk weights are 100%):
$$
\boxed{\;L^{*}/A = r \;}\qquad\text{(all-in RW 100\%).}
$$

More generally, inserting risk weights decouples the two sides: the ratio is $E/\mathrm{RWA}$ but the loss falls on $A$, so a lower average risk weight *raises* the ratio without changing $E$ or $A$ — the seed of regulatory arbitrage ([[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05 · Failure Modes]]).

**The three pillars (Basel II onward).**
- **Pillar 1:** minimum capital $= 8\%\times\mathrm{RWA}$ for credit + market + operational risk.
- **Pillar 2:** supervisory review (ICAAP/SREP) for risks Pillar 1 misses.
- **Pillar 3:** public disclosure to restore market discipline.

**The history in one line each.** *Basel I* (1988): a crude risk-weight grid, $8\%$ total capital. *Basel II* (2004): three pillars, and internal models (**IRB**, **AMA**) allowed for credit and operational risk. *Basel III* (2010–2017): after the crisis, higher and better-quality capital (CET1 minima, buffers), a leverage backstop, liquidity ratios (LCR/NSFR), and the **output floor** that limits how far internal models can drive RWA down.

---

### 3. Computational Implementation — the shock absorber in numbers

The single most convincing way to *see* why capital matters: take a bank, hit it with losses, watch the ratio. Stdlib only.

```python
def shock(exposure, rw, cap_ratio, loss_pct):
    """Return (equity, ratio_after) for a bank whose assets lose loss_pct."""
    rwa  = exposure * rw
    cap0 = cap_ratio * rwa
    cap1 = cap0 - loss_pct * exposure
    return cap0, cap1, cap1 / rwa

exposure, rw, r = 1000.0, 1.0, 0.08
print(f"bank: assets={exposure:.0f}  avg RW={rw:.0%}  capital ratio={r:.1%}  ->  {exposure/(r*exposure*rw)*1:.1f}x levered")
for L in (0.02, 0.05, 0.08, 0.12):
    cap0, cap1, r1 = shock(exposure, rw, r, L)
    state = "solvent" if r1 > 0 else "WIPED OUT"
    print(f"  asset loss {L:5.0%}: equity {cap0:6.1f} -> {cap1:6.1f}   ratio {r:.1%} -> {r1:5.1%}   {state}")
for r0 in (0.045, 0.08, 0.12):
    print(f"  a bank with a {r0:.1%} capital ratio absorbs a {r0:.1%} loss on fully-weighted assets")
```
```
bank: assets=1000  avg RW=100%  capital ratio=8.0%  ->  12.5x levered
  asset loss    2%: equity   80.0 ->   60.0   ratio 8.0% ->  6.0%   solvent
  asset loss    5%: equity   80.0 ->   30.0   ratio 8.0% ->  3.0%   solvent
  asset loss    8%: equity   80.0 ->    0.0   ratio 8.0% ->  0.0%   WIPED OUT
  asset loss   12%: equity   80.0 ->  -40.0   ratio 8.0% -> -4.0%   WIPED OUT
  a bank with a 4.5% capital ratio absorbs a 4.5% loss on fully-weighted assets
  a bank with a 8.0% capital ratio absorbs a 8.0% loss on fully-weighted assets
  a bank with a 12.0% capital ratio absorbs a 12.0% loss on fully-weighted assets
```

**Read the table.** At an 8% ratio the bank survives a 5% asset loss but is wiped out by an 8% loss — and a 12% loss leaves equity *negative*, meaning creditors and the deposit insurer take the hit. The entire reform agenda (higher CET1 minima, buffers, the leverage backstop) exists because 8% was too thin when losses came in correlated waves in 2008.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "capital = money in the vault" trap.** Regulatory capital is *funding structure*, not liquidity. A bank can hold plenty of cash and still be under-capitalised; conversely "well-capitalised" says nothing about whether it can meet a run (that is the LCR's job, §06).
2. **Leverage makes small errors fatal.** Because $A/E=1/r$, the same *percentage* asset loss produces a $1/r$–times larger equity hit. Risk controls calibrated on asset returns systematically understate the equity (solvency) impact.
3. **Moral hazard is structural, not a behavioural quirk.** Deposit insurance and LOLR remove depositor discipline; capital rules are the *substitute* discipline, which is why they must bind even when a bank would prefer them not to.
4. **Risk weights are a model of risk.** The buffer is only as good as $rw_i$. Under-weight a real risk and the "shock absorber" is fiction — this is precisely the regulatory-arbitrage and procyclicality failures developed in [[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Hull, John C.** — *Risk Management and Financial Institutions* (5th ed., 2018). The Basel I/II/III chapters: the clearest narrative of *why* the rules exist and how they evolved (read alongside the primary BCBS texts). *The recommended entry text.*
- **BCBS** — *Basel III: A Global Regulatory Framework for More Resilient Banks and Banking Systems* (2010, BIS d189). The minimum ratios and buffer stack, in the regulators' own words. *Read from the corpus PDF.*
- **BCBS** — *Basel II: International Convergence of Capital Measurement and Capital Standards* (2006). The three-pillar architecture and the risk-weight grid. *Read from the corpus PDF.*
- **Hull, John C.** — *Options, Futures, and Other Derivatives* (11th ed.), Ch 24 (credit ratings, recovery rates ~40%, the Merton/Vasicek credit model). *Verified per chapter in the corpus.*

---

### 6. Connected Graph Bridges

- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]
- Continue: [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|02 · Capital & RWA]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Index Hub]]
