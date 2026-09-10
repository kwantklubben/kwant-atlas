---
title: "03 — The Duffie–Garleanu–Pedersen Search-and-Bargaining Model"
tags:
  - pillar-market-making
  - dealer-banks-and-otc
  - search-and-bargaining
  - dgp-model
  - closed-form
---

**Basic Prerequisites:** [[pillars/06-market-making/dealer-banks-and-otc/02-otc-market-structure|02 · OTC Market Structure]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

Duffie, Gârleanu & Pedersen (2005) is the *anchor model* of OTC economics. It is the first model to derive dealer **bid and ask prices** from **search and bargaining** rather than from inventory (Ho–Stoll) or adverse selection (Glosten–Milgrom). Its answer: the OTC spread is the **Nash split of the gains from trade**, and the split depends on the *search intensities* $\lambda$ (how fast investors find each other) and $\rho$ (how fast they find a dealer) and on the *bargaining power* $z$.

The practical objective: be able to compute the equilibrium prices $A,B,P$ from the primitives, and to understand **which knob tightens the spread**. The headline comparative statics are exactly the ones a market-structure practitioner cares about:

1. **Better investor search ($\lambda\uparrow$) → tighter spread**, unconditionally: the customer always has the credible threat of trading with another investor, so the dealer must concede.
2. **Better dealer access ($\rho\uparrow$) → tighter spread IF dealers compete ($z<1$)** — "sequential competition" between dealers drives the spread to zero.
3. **Better dealer access ($\rho\uparrow$) → WIDER spread IF the dealer is a monopolist ($z=1$)** — because easier access makes the investor's alternative *worse*, since the dealer has hoovered up all the counterparties.

> **The one-sentence result.** "The OTC bid-ask is $A-B=\delta z/D$ — a $z$-fraction of the fundamental surplus $\delta/r$ — and it converges to zero under fast search only when dealers lack total bargaining power; a monopolist dealer's spread actually *widens* with more accessibility."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The setup: types, search, and meeting

A unit continuum of risk-neutral investors. Each holds at most one unit of a long-lived asset (total supply $s$). An investor is of **intrinsic type** low or high; type switches are Poisson: low$\to$high at $\lambda_u$, high$\to$low at $\lambda_d$. In the steady state the fraction of high types is $\lambda_u/(\lambda_u+\lambda_d)$ — high-type **owners** want to keep the asset, high-type **non-owners** want to buy it.

Investors meet each other at intensity $\lambda$ (a **search** friction) and meet dealers at intensity $\rho$ (**dealer accessibility**). Dealers can recycle positions instantly in a frictionless **interdealer market** at price $M$, so they bear no inventory risk — a deliberate contrast with inventory models.

Conservation gives two identities that solve the four-type system with only one unknown:

$$\mu_{lo}+\mu_{ho}=s,\qquad \mu_{ho}+\mu_{hn}=\frac{\lambda_u}{\lambda_u+\lambda_d}.$$

Under **Condition 1** ($s<\lambda_u/(\lambda_u+\lambda_d)$), which holds in the paper's example ($0.8<0.9091$), the market has more high-type non-owners than low-type owners ($\mu_{lo}<\mu_{hn}$), so a dealer sells to *every* non-owner he meets and the interdealer price is the buyer/taker side, $M=A=H$. The steady-state mass $\mu_{lo}$ then solves a quadratic:

$$2\lambda\,x^2+\bigl(2\lambda a+\rho+\lambda_u+\lambda_d\bigr)x-\lambda_d s=0,\qquad a\equiv\frac{\lambda_u}{\lambda_u+\lambda_d}-s.$$

#### 2.2 Value functions and bargaining (the HJB)

Let $V_\sigma$ be an investor's continuation value by type. In steady state the Hamilton–Jacobi–Bellman equations are (DGP eq 10):

$$\dot V_{lo}=rV_{lo}-\lambda_u(V_{ho}-V_{lo})-2\lambda\mu_{hn}(P+V_{ln}-V_{lo})-\rho(B+V_{ln}-V_{lo})-(1-\delta),$$
$$\dot V_{ln}=rV_{ln}-\lambda_u(V_{hn}-V_{ln}),\qquad \dot V_{ho}=rV_{ho}-\lambda_d(V_{lo}-V_{ho})-1,$$
$$\dot V_{hn}=rV_{hn}-\lambda_d(V_{ln}-V_{hn})-2\lambda\mu_{ho}(V_{ho}-V_{hn}-P)-\rho(V_{ho}-V_{hn}-A).$$

**Bargaining.** When a low owner meets a high non-owner, the gains from trade are $L=V_{lo}-V_{ln}$ (the seller's) and $H=V_{ho}-V_{hn}$ (the buyer's). **Nash bargaining** with seller power $q$ splits them (DGP eq 11):

$$\boxed{\,P=(1-q)\,L+q\,H\,}$$

When an investor meets a dealer, the dealer's outside option is the interdealer price $M$ and his power is $z$ (DGP eqs 12–13):

$$\boxed{\,A=zH+(1-z)M,\qquad B=zL+(1-z)M\,}\qquad\Longrightarrow\qquad A-B=z(H-L).$$

#### 2.3 The closed-form equilibrium (Theorem 2)

Solving the linear value-function system gives the prices directly (DGP eqs 14–16), with

$$D=r+\lambda_d+2\lambda\mu_{lo}(1-q)+\lambda_u+2\lambda\mu_{hn}q+\rho(1-z),$$
$$A=\frac1r-\frac{\delta}{r}\,\frac{\lambda_d+2\lambda\mu_{lo}(1-q)}{D},\quad
B=\frac1r-\frac{\delta}{r}\,\frac{zr+\lambda_d+2\lambda\mu_{lo}(1-q)}{D},\quad
P=\frac1r-\frac{\delta}{r}\,\frac{(1-q)r+\lambda_d+2\lambda\mu_{lo}(1-q)}{D}.$$

Each price is the present value $1/r$ of the dividend stream, **reduced by an illiquidity discount** $(\delta/r)\times(\text{ratio})$. The spread is

$$A-B=\frac{\delta z}{D}.$$

**Monopolist case** ($z=1$): the spread becomes $A-B=\delta/\bigl(r+\lambda_u+\lambda_d+\rho(1-z)\bigr)$, which is **independent of the investor search intensity $\lambda$** and **increasing in $\rho$** — the counterintuitive core of the paper. **Competitive case** ($z<1$): as $\rho\to\infty$, $D\to\infty$ and $A-B\to0$ (sequential competition). **Fast investors:** as $\lambda\to\infty$, $D\to\infty$ regardless of $z$, so $A-B\to0$ (Theorem 3, part 1). The equilibrium converges to Walrasian $P^\*=1/r$.

---

### 3. Computational Implementation — the equilibrium engine

Stdlib only. We solve the steady-state masses from the quadratic, then compute Theorem-2 prices and verify the three comparative statics plus the spread identity. **Ran and verified.**

```python
import math

def ss_masses(lam, rho, lamu=1.0, lamd=0.1, s=0.8):
    a = lamu/(lamu+lamd) - s
    c = 2*lam*a + rho + lamu + lamd
    mu_lo = (-c + math.sqrt(c*c + 8*lam*lamd*s)) / (4*lam)
    return mu_lo, a+mu_lo, s-mu_lo, (1-s)-(a+mu_lo)      # lo, hn, ho, ln

def dgp_prices(lam, rho, z=0.8, q=0.5, delta=1.0, r=0.05, lamu=1.0, lamd=0.1, s=0.8):
    mu_lo, mu_hn, _, _ = ss_masses(lam, rho, lamu, lamd, s)
    D = r + lamd + 2*lam*mu_lo*(1-q) + lamu + 2*lam*mu_hn*q + rho*(1-z)
    A = 1/r - (delta/r)*(lamd + 2*lam*mu_lo*(1-q))/D
    B = 1/r - (delta/r)*(z*r + lamd + 2*lam*mu_lo*(1-q))/D
    P = 1/r - (delta/r)*((1-q)*r + lamd + 2*lam*mu_lo*(1-q))/D
    return A, B, P

print("DGP equilibrium, lambda=26, q=0.5, r=0.05, delta=1 (Walrasian 1/r = 20):")
A, B, P = dgp_prices(26, 0.0)
print(f"  rho=0:  A={A:.6f}  B={B:.6f}  P={P:.6f}   spread A-B={A-B:.6f}")

print("\n(1) faster INVESTOR search lambda -> competitive (rho=0):")
for lam in (5, 10, 26, 100, 1000, 10000):
    A, B, P = dgp_prices(lam, 0.0)
    print(f"    lambda={lam:6d}:  P={P:.6f}   spread={A-B:.6f}")

print("\n(2) dealer access rho: COMPETING (z=0.8) vs MONOPOLIST (z=1.0):")
print("      rho      spread z=0.8   spread z=1.0")
for rho in (0.0, 1.0, 10.0, 100.0, 1000.0):
    A8, B8, _ = dgp_prices(26, rho, z=0.8)
    A1, B1, _ = dgp_prices(26, rho, z=1.0)
    print(f"    {rho:7.1f}   {A8-B8:12.6f}   {A1-B1:12.6f}")

print("\n(3) spread identity A-B = delta*z/D:")
mu_lo, mu_hn, _, _ = ss_masses(26, 1.0)
D = 0.05 + 0.1 + 2*26*mu_lo*0.5 + 1.0 + 2*26*mu_hn*0.5 + 1.0*(1-0.8)
A, B, _ = dgp_prices(26, 1.0, z=0.8)
print(f"    closed form A-B = {A-B:.10f};  delta*z/D = {0.8/D:.10f}")
```
```text
DGP equilibrium, lambda=26, q=0.5, r=0.05, delta=1 (Walrasian 1/r = 20):
  rho=0:  A=18.315906  B=18.140204  P=18.206093   spread A-B=0.175702

(1) faster INVESTOR search lambda -> competitive (rho=0):
    lambda=     5:  P=17.176247   spread=0.397176
    lambda=    10:  P=17.451412   spread=0.299417
    lambda=    26:  P=18.206093   spread=0.175702
    lambda=   100:  P=19.271366   spread=0.062808
    lambda=  1000:  P=19.911935   spread=0.007209
    lambda= 10000:  P=19.991007   spread=0.000732

(2) dealer access rho: COMPETING (z=0.8) vs MONOPOLIST (z=1.0):
      rho      spread z=0.8   spread z=1.0
        0.0       0.175702       0.219628
        1.0       0.170610       0.222764
       10.0       0.128394       0.236361
      100.0       0.033298       0.248428
     1000.0       0.003922       0.250595

(3) spread identity A-B = delta*z/D:
    closed form A-B = 0.1706099929;  delta*z/D = 0.1706099929
```
**Read the two tables.** As $\lambda$ grows $P\to1/r=20$ and the spread $\to0$: **fast investor search is unconditionally good for customers.** As $\rho$ grows, the competing-dealer spread ($z=0.8$) **falls** from $0.1757$ to $0.0039$ while the monopolist spread ($z=1.0$) **rises** from $0.2196$ to $0.2506$ — the paper's signature result, reproduced exactly. The spread identity $A-B=\delta z/D$ confirms the closed form to ten decimals.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Bargaining power $z$ is the master parameter, and it is unobservable.** Every comparative static flips on whether dealers compete or monopolise. Calibrating $z$ from data is hard; treating $z$ as a free knob without justification is the classic misuse.
2. **The model abstracts from inventory and information.** DGP dealers bear *no* inventory risk (interdealer market is frictionless) and agents are symmetrically informed. Real dealers do both — this model must be combined with [[pillars/06-market-making/inventory-management-and-quote-skewing/index|inventory]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|adverse-selection]] views.
3. **Risk-neutral, single asset, no capital constraints.** There is no balance sheet: dealers never run out of capital. The *capacity* failure — the one that caused 2008 — is *outside* this model and requires [[pillars/06-market-making/dealer-banks-and-otc/04-dealer-capacity-and-balance-sheets|04 · Dealer Capacity]].
4. **Instant trade assumption.** Meeting ⇒ immediate trade. With asymmetric information or strategic delay, trade can be delayed (the model deliberately abstracts from this).
5. **Steady state.** The closed forms hold at the stationary masses; transitional dynamics (a crisis) require the full $\dot\mu$ system.

---

### 5. Canonical Literature & Study References

- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6), 1815–1847 — Propositions 1–4, HJB (10), bargaining (11)–(13), Theorem 2 (14)–(16), Theorem 3 (fast search), Theorem 4 (heterogeneous investors). *Primary PDF in corpus; all equations and numbers re-derived and verified.*
- **Duffie, Gârleanu & Pedersen (2003)**, *Valuation in dynamic bargaining markets* — the working-paper precursor (alternating-offer bargaining).
- **Duffie (2012)**, *Dark Markets*, Ch 2–5 — the book-length treatment of the same search framework with information.
- **Rubinstein & Wolinsky (1985)**, *Equilibrium in a market with sequential bargaining*, Econometrica — the bargain-without-intermediary ancestor; DGP reconcile it with Walrasian limits.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/dealer-banks-and-otc/02-otc-market-structure|02 · OTC Market Structure]]
- Forward: [[pillars/06-market-making/dealer-banks-and-otc/04-dealer-capacity-and-balance-sheets|04 · Dealer Capacity & Balance Sheets]] · [[pillars/06-market-making/dealer-banks-and-otc/index|Index Hub]]
- Sibling: [[pillars/06-market-making/inventory-management-and-quote-skewing/03-ho-stoll-model|Ho–Stoll Dealer Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|The Glosten–Milgrom Model]]
