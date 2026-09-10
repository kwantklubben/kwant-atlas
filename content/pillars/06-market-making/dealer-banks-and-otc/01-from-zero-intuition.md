---
title: "01 — Dealer Banks & OTC Markets from Zero: Why OTC Exists"
tags:
  - pillar-market-making
  - dealer-banks-and-otc
  - intuition
  - otc-markets
---

**Basic Prerequisites:** [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]].

---

### 1. Intuition & Practical Objective

This page explains **why over-the-counter (OTC) markets exist at all** — with no prior knowledge of dealer banks needed. The objective is one idea: **when a trade is *customized* and *infrequent*, an exchange cannot match it, so a dealer must stand in the middle — and the dealer's price is set by negotiation, not by an auction.**

Start with the dumbest question: *why isn't everything traded on a stock exchange?* A stock exchange is a beautiful machine: everyone trades the same standardized share, thousands of buyers and sellers arrive every second, and a continuous auction sets one price. But most of finance is **not** standardized:

- A pension fund wants a 27-year interest-rate swap with a specific notional schedule to hedge a pension liability. No one else wants that exact contract.
- A bank wants to sell a $40m tranche of a specific corporate bond. The bond rarely trades; there is no crowd.
- An airline wants to hedge jet-fuel exposure with a bespoke collar.

For these, **there is no continuous market, only a search for a counterparty**, and someone must be willing to be the counterparty *now*. That someone is a **dealer** — typically a dealer bank — who quotes a price, takes the position onto its balance sheet, and earns the **bid-ask spread** for providing immediacy.

Three steps, three "aha"s:

1. **Standardization is what makes an exchange possible.** Exchanges need *fungibility* (every unit identical) and *volume*. Customized contracts have neither, so they cannot be centrally matched. They trade **bilaterally**: one buyer, one seller, one negotiated price.

2. **Immediacy is a product you must pay for.** If you want to trade *now*, you either (a) wait and search for the other side, or (b) pay a dealer to take the other side instantly. The bid-ask spread is the price of option (b). This is exactly the "supply of dealer services" view (Stoll 1978) — the dealer sells a service, and the spread is its fee.

3. **The price is a bargain, not an auction.** Because the two sides meet bilaterally, the price depends on each side's **outside option** — how easily each could find someone else. A single trade price in an OTC market encodes both the asset's value *and* the relative bargaining power of the two parties. This is the insight that becomes the search-and-bargaining model (Duffie–Gârleanu–Pedersen 2005).

> **The one-sentence essence.** "An OTC market is not an auction with many participants but a **search market with two**: a dealer who sells immediacy and a customer who needs it, haggling over a price that reflects how fast each can find an alternative."

---

### 2. Mathematical Ground Truth & Derivations

**The first, simplest model: a dealer's bid-ask as the price of immediacy.**

Suppose an asset will be worth $V$ to the *current* holder at some horizon, but the holder has a **liquidity need** — a pure discount-rate/impatience cost $\delta$ per unit time of holding when they would rather not (Duffie–Gârleanu–Pedersen call low intrinsic type $lo$). If an investor must hold forever, the asset's value to them is the present value of a stream that is penalized by $\delta$:

$$V^{lo}=\int_0^\infty e^{-rt}(1-\delta)\,dt=\frac{1-\delta}{r},\qquad V^{hn}=\int_0^\infty e^{-rt}\,dt=\frac{1}{r}.$$

The **gain from trade** between a low-type owner (wants to sell) and a high-type non-owner (wants to buy) is therefore

$$H-L=\frac1r-\frac{1-\delta}{r}=\frac{\delta}{r}.$$

That gap — the fundamental surplus — is the maximum total *spread* the two sides could ever split. In a frictionless Walrasian world they would jump straight to $P^\*=1/r$ and split the surplus costlessly. **In a search world they cannot**: each side can only trade when a counterparty is *found*.

**Search turns the split into a spread.** Let $\lambda$ be the intensity at which an investor meets *another investor*, and $\rho$ the intensity at which an investor meets a **dealer**. When two investors meet they Nash-bargain and split the surplus with the seller getting $(1-q)$ and buyer $q$:

$$P=(V_{lo}-V_{ln})(1-q)+(V_{ho}-V_{hn})q.$$

When an investor meets a **dealer**, the dealer has an outside option — unloading in the frictionless **interdealer market** at price $M$ — and bargaining power $z$, so:

$$A=zH+(1-z)M,\qquad B=zL+(1-z)M,\qquad\Longrightarrow\qquad A-B=z(H-L).$$

**This is the whole intuition in one line:** *the OTC bid-ask spread is a fraction $z$ of the fundamental surplus $\delta/r$, where $z$ is how much of the bargaining power the dealer holds.* A dealer with all the power ($z=1$) takes the entire surplus; perfect competition ($z\to0$) closes the spread to zero.

**Why doesn't competition always close it?** Because a search market is *inherently uncompetitive* — you trade with the one counterparty you happened to meet, not with "the market." Prices converge to Walrasian only as search gets *fast enough that a better outside option is credible*. That is the deep result of the folder's model page.

---

### 3. Computational Implementation — why dealers matter for allocation

We simulate an OTC market of investors who may trade **only directly with each other** (no dealer, $\rho=0$), at meeting intensity $\lambda$. Each asset is worth more to a high intrinsic type, so *efficient allocation* means every asset ends up held by a high type. Search frictions leave the market misallocated; faster search (or a dealer) fixes it. Stdlib + numpy; ran and verified.

```python
import numpy as np

def simulate(lam, N=4000, steps=20000, dt=0.001, lamu=1.0, lamd=0.1, s=0.8, seed=7):
    rng = np.random.default_rng(seed)
    hold = np.zeros(N, dtype=bool); hold[:int(s*N)] = True
    hi = rng.random(N) < lamu/(lamu+lamd)           # intrinsic high type?
    for _ in range(steps):
        hi[rng.random(N) < lamu*dt] = True
        hi[rng.random(N) < lamd*dt] = False
        npair = rng.poisson(lam*N*dt/2)             # random meetings
        if npair:
            a = rng.integers(0,N,npair); b = rng.integers(0,N,npair); m = a != b
            for i,j in zip(a[m],b[m]):
                if hold[i] and not hi[i] and not hold[j] and hi[j]:
                    hold[i],hold[j]=False,True       # lo owner sells to hn nonowner
                elif hold[j] and not hi[j] and not hold[i] and hi[i]:
                    hold[j],hold[i]=False,True
    return (hold & hi).sum()/max(hold.sum(),1)       # allocation efficiency

print("OTC direct-trade search: allocation efficiency vs investor search intensity lam")
for lam in (2, 5, 10, 26, 50, 100):
    print(f"  lam={lam:4d} (mean wait {1/lam:.3f}): efficiency = {simulate(lam):.4f}")
```
```text
OTC direct-trade search: allocation efficiency vs investor search intensity lam
  lam=   2 (mean wait 0.500): efficiency = 0.9372
  lam=   5 (mean wait 0.200): efficiency = 0.9472
  lam=  10 (mean wait 0.100): efficiency = 0.9634
  lam=  26 (mean wait 0.038): efficiency = 0.9753
  lam=  50 (mean wait 0.020): efficiency = 0.9862
  lam= 100 (mean wait 0.010): efficiency = 0.9922
```
Allocation efficiency **rises monotonically** with search intensity and approaches the Walrasian limit of $1$ (every asset held by a high type). The gap between the curve and $1$ is the **search-friction cost** — exactly the illiquidity the dealer is paid to remove. Note the dimension: at $\lambda=2$ (an investor finds another investor about once every half-period), $6.3\%$ of assets sit in the "wrong" hands.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"OTC" is not "unregulated chaos" — it is a different mechanism.** Beginners assume no exchange means no market structure. In fact OTC markets have rich structure: designated dealers, interdealer brokers, RFQ (request-for-quote) platforms, trade-reporting regimes. Confusing "no central book" with "no rules" is the first error.
2. **Customization is the cause, not the bug.** The reason a corporate bond or a bespoke swap trades OTC is that *each contract is unique*, so there is no fungible crowd to match. Blaming OTC for "illiquidity" misses that the illiquidity is intrinsic to the customization.
3. **The spread is not the dealer's "greed."** It is the price of *immediacy and inventory risk-bearing*. Stoll's dealer-services view (1978) — and every model in this folder — derives the spread from a service rendered, not spite.
4. **Two identical assets can trade at two prices at the same instant.** In a bilateral market, price depends on who you found and how much they needed to trade. Price *dispersion* (not a single price) is a defining OTC feature (bridged to [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]]).

---

### 5. Canonical Literature & Study References

- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6) — the search model this folder is built on; §1 motivates OTC existence. *Primary PDF in corpus.*
- **Duffie (2012)**, *Dark Markets*, Princeton UP — Ch 1 (why OTC markets are search markets).
- **Stoll (1978)**, *The supply of dealer services in securities markets*, Journal of Finance 33(4) — the dealer-as-service-provider view of the spread. *Primary PDF in corpus.*
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 1–2 — the taxonomy of market mechanisms, dealer vs. order-driven. *Verified in corpus.*

---

### 6. Connected Graph Bridges

- Base: [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates]]
- Continue: [[pillars/06-market-making/dealer-banks-and-otc/02-otc-market-structure|02 · OTC Market Structure]] · [[pillars/06-market-making/dealer-banks-and-otc/index|Index Hub]]
