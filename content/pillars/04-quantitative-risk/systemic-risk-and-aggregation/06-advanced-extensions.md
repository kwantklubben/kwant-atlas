---
title: "06 — Advanced Extensions: Macroprudential Policy & Bellini Stress Integration"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - macroprudential
  - stress-integration
  - countercyclical-buffer
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/04-aggregating-risk-types|04 · Aggregating Risk Types]] and [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]].

---

### 1. Intuition & Practical Objective

The fixes to the failure modes of 05 are *structural*, not parametric, and they live at the **macroprudential** level — the level of the system, not the firm. This page is the **launchpad** for two ideas:

1. **Countercyclicality in policy.** Because per-firm VaR/leverage rules are procyclical (§05), regulators add a macroprudential layer that *builds* buffers in the boom so they are available in the bust, and that is calibrated on *credit/leverage growth* (the Credit-to-GDP gap) rather than *current volatility*. This is the **CCyB** and the broader "leaning against the wind" toolkit.
2. **Stress integration as the aggregation solution (Bellini).** Since cross-type aggregation by copula is model-fragile (§04), Bellini's practical alternative is to *integrate risk types through a shared macro factor*: one scenario-driver $Z$ (e.g. GDP, rates, spreads) simultaneously shocks the market book, the credit PDs, and liquidity, then all losses land in a single P&L. Integration *by scenario* sidesteps the untestable copula — you don't have to *assume* dependence, you *generate* it from a common macro path.

The objective: see that **the right aggregation is a *model of a shared economy*, not a statistical joiner of marginal distributions.**

---

### 2. Mathematical Ground Truth & Derivations

**Countercyclical capital buffer (BCBS 2010; the credit-gap rule).** Let $g_t$ be the credit-to-GDP gap (credit ratio minus its trend). The CCyB add-on is

$$
\text{buffer}_t = 0.3125\cdot\max(g_t-2,\,0)\quad\text{(i.e. }0\%\text{ at a 2pp gap, }2.5\%\text{ at }10\text{pp, capped at }2.5\%\text{),}
$$

so the buffer *rises as credit outgrows the trend* — before the bust — and *releases* as the gap shrinks, feeding capital back into the system during the downcycle. This is the anti-procyclical mirror of the VaR-target loop in §05: it removes the *need* to delever in the bust because capital was pre-positioned.

**Macro-factor credit link (Vasicek / Bellini CLE).** Let a single macro factor $Z\sim N(0,1)$ drive every borrower's default probability through a logistic link

$$
\text{PD}(Z) = \frac{1}{1+e^{-(\alpha+\beta Z)}}.
$$

Borrowers are independent *given* $Z$, so the portfolio default count for $N$ loans is, conditional on $Z$,

$$
L^{\text{credit}} = \frac{1}{N}\sum_{i=1}^{N}\mathbf{1}_{U_i \le \text{PD}(Z)}.
$$

Now add the bank's market (trading) book as a *function of the same $Z$*, $L^{\text{market}} = c + bZ + \xi$. The **integrated loss** is

$$
L^{\text{tot}}(Z) = w_m\,L^{\text{market}}(Z) + w_c\,L^{\text{credit}}(Z),
$$

and the bank's integrated expected shortfall is $\text{ES}_\alpha(L^{\text{tot}})$ over scenarios $Z\sim N(0,1)$ — a single number that commits the market and credit books to *the same* macro scenario. This is Bellini's core move: **aggregate by joint scenario, not by adding separately-estimated marginal capitals.** The resulting integrated ES is *different from* (and in §3 below, *below*) the naive sum of the two standalone ES, because a single scenario can't simultaneously trigger each book's own idiosyncratic tail — and that "un-achievable" sum is exactly the subadditivity slack of §04.

---

### 3. Computational Implementation — Bellini-style integrated stress

We run a bank with a trading book and a loan book under a shared macro factor $Z$. Standalone = each book's own ES estimated separately; integrated = ES of the sum under the *same* $Z$-scenario. Plus the CCyB credit-gap rule. Stdlib only.

```python
import math, random
def gauss():
    u1 = max(random.random(), 1e-12)
    return math.sqrt(-2.0*math.log(u1)) * math.cos(2.0*math.pi*random.random())
def PD(Z):
    return 1.0/(1.0 + math.exp(-(-4.0 + 1.2*Z)))     # logistic macro-credit link (Bellini)

random.seed(9)
M, N = 40000, 60
w_m, w_c = 1.0, 45.0
Lm, Lc = [], []
for _ in range(M):
    Z = gauss()
    market = 1.0 + 2.0*Z + 0.5*gauss()               # trading P&L, stress-sensitive
    p = PD(Z)
    ndef = sum(1 for _ in range(N) if random.random() < p)   # correlated via shared Z
    Lm.append(market); Lc.append(ndef/N)

def ES(x, alpha):
    s = sorted(x); k = int(alpha*len(s)) - 1
    return sum(s[k:])/(len(s)-k)

es_m = ES(Lm, 0.95); es_c = w_c*ES(Lc, 0.95)
Ltot = [a*w_m + b*w_c for a, b in zip(Lm, Lc)]
es_tot = ES(Ltot, 0.95)

print(f"mean PD: Z normal(0)={PD(0)*100:.2f}% | Z stress(+2)={PD(2)*100:.1f}% | Z boom(-2)={PD(-2)*100:.2f}%")
print(f"standalone ES[0.95] market={es_m:.2f}  credit={es_c:.2f}  -> naive sum={es_m+es_c:.2f}")
print(f"integrated ES[0.95] (shared Z scenario) = {es_tot:.2f}")
print(f"double-count avoided = {(es_m+es_c)-es_tot:.2f}")

print("CCyB: credit-to-GDP gap -> countercyclical buffer (2pp activation, 2.5% at 10pp):")
for g in (-2, -1, 0, 1, 2, 3, 2, 1, -1, -3):
    print(f"   gap={g:+3d}%  -> buffer={min(2.5, 0.3125*max(g-2.0,0.0)):.2f}%")
```
```
mean PD: Z normal(0)=1.80% | Z stress(+2)=16.8% | Z boom(-2)=0.17%
standalone ES[0.95] market=5.25  credit=9.12  -> naive sum=14.37
integrated ES[0.95] (shared Z scenario) = 14.13
double-count avoided = 0.24
CCyB: credit-to-GDP gap -> countercyclical buffer (2pp activation, 2.5% at 10pp):
   gap= -2%  -> buffer=0.00%
   gap= -1%  -> buffer=0.00%
   gap= +0%  -> buffer=0.00%
   gap= +1%  -> buffer=0.00%
   gap= +2%  -> buffer=0.00%
   gap= +3%  -> buffer=0.31%
   gap= +2%  -> buffer=0.00%
   gap= +1%  -> buffer=0.00%
   gap= -1%  -> buffer=0.00%
   gap= -3%  -> buffer=0.00%
```

**Read the output.** The macro factor does the coupling: lending PDs climb from 1.80% at the mean, through 0.17% in a boom, to **16.8%** in a $+2$ macro stress. The two standalone ES stack to **14.37**, but the integrated figure — market and credit forced onto the *same* macro scenario — is **14.13**: the naive sum overstates by ~0.24 because a single bad scenario can't simultaneously strain each book's *idiosyncratic* versus its *macro* component. More important than the (modest) saving is *what the method commits to*: it replaces an untestable copula with a tested **shared-economy model** — you audit the macro driver $Z$ and the PD and market-loading coefficients ($\beta$, $b$), which are identifiable from data, instead of trusting an unobservable $\lambda_u$. The CCyB rows make the policy explicit: the buffer is **zero while the gap is negative (bust) and builds to 1.9% at a +3% gap** — capital accumulate in the boom, released in the bust, precisely anti-procyclical to the §05 loop.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The macro factor is still a model.** Integrated stress is only as good as the assumed $Z$ and loadings; a wrong factor (or a tail that $N(0,1)$ can't reach) silently understates the joint tail. Scenario *selection* must itself be stress-tested (bridges [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]).
2. **CCyB is procyclical in its own right if mis-calibrated.** A gap computed with a bad "trend" can release buffers at the wrong time; the 2.5% cap is a policy judgement, not a calibration.
3. **Integrated ≠ correct.** Bellini integration plausibly beats naive summation, but it does not resolve tail-dependence ambiguity — it *pins*, rather than estimates, the dependence via the macroeconomic channel, so model risk moves but does not disappear.
4. **Regulatory gaming.** Any published systemic measure (MES/SRISK/CoVaR) invites arbitrage once banks optimise against it — a Goodhart failure inherent in all three-measure toolkits.

---

### 5. Canonical Literature & Study References

- **Bellini**, *Stress Testing and Risk Integration in Banks* (2016) — the CLE/MCRE macro-factor credit link and cross-risk-type integration, hands-on R/MATLAB; *the* practical reference (CORE in the corpus).
- **BCBS**, *Basel III: A Global Regulatory Framework for More Resilient Banks* (2010), and the 2017 finalisation — the CCyB, countercyclical toolkit (corpus refs: `63_BCBS_2017...finalising_post_crisis`, `67_BCBS_2010...`).
- **Schuermann**, *Stress Testing Banks*, *IJCB* 10(2) (2014) — the supervisory design that integrated macro scenarios into bank capital.
- **Quagliariello (ed.)**, *Stress-testing the Banking System* (2009) — system-wide vs bank-level macro stress integration.
- **McNeil, Frey & Embrechts**, *QRM* (2015) §6.4 — copula-risk aggregation as the theoretical backdrop Bellini's scenario approach sits on.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Index Hub]]
- Forward topic pages: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/basel-and-regulation/02-capital-and-rwa|Capital & RWA]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]]
- Sibling mechanism: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]] (what "release the buffer" prevents) · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (the PD/$Z$ link)