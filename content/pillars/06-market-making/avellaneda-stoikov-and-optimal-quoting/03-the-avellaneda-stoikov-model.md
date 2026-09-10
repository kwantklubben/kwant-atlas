---
title: "03 — The Avellaneda-Stoikov Model: Reservation Price & Optimal Spread"
tags:
  - pillar-market-making
  - avellaneda-stoikov-and-optimal-quoting
  - closed-form
  - optimal-spread
  - reservation-price
---

**Basic Prerequisites:** [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/02-the-market-maker-problem|02 · The Market-Maker Problem]].

---

### 1. Intuition & Practical Objective

This is the **complete closed-form lookup page** for the AS model. The practical objective: one master recipe for the optimal bid and ask quotes, with the derivation of the asymptotic solution the paper actually uses. Everything below is AS 2008 §3, cross-checked numerically against the paper's own tables.

The solution is a **two-step procedure**:

1. **Compute the reservation price** $r(s,q,t)$ — solve the PDE for $\theta$ (or use the asymptotic closed form) to get the dealer's inventory-adjusted fair value.
2. **Calibrate quotes to the book** — solve the implicit first-order conditions for the distances $\delta^a,\delta^b$, which for exponential intensities gives the closed-form spread.

The headline result is beautifully compact:

$$\boxed{\;p^{\text{ask}}=r+\tfrac12\psi,\qquad p^{\text{bid}}=r-\tfrac12\psi,\qquad
\psi=\gamma\sigma^2(T-t)+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right)\;}$$

with $r=s-q\gamma\sigma^2(T-t)$. **The quotes are the reservation price plus/minus half the spread — and the spread itself does not depend on inventory** (a consequence of exponential intensities). All inventory dependence lives in the skew of $r$.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The reduced equation for $\theta$

From [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/02-the-market-maker-problem|02]], the ansatz $u=-\exp(-\gamma x)\exp(-\gamma\theta(s,q,t))$ turns the HJB into (AS eq. 3.3)

$$\theta_t+\tfrac12\sigma^2\theta_{ss}-\tfrac12\sigma^2\gamma\,\theta_s^2
+\max_{\delta^b}\frac{\lambda^b(\delta^b)}{\gamma}\!\left[1-e^{-\gamma(s-\delta^b-r^b)}\right]
+\max_{\delta^a}\frac{\lambda^a(\delta^a)}{\gamma}\!\left[1-e^{-\gamma(s+\delta^a-r^a)}\right]=0,$$

with $\theta(s,q,T)=qs$. The first-order conditions for the two maxes give the **implicit quote distances** (AS eq. 3.6–3.7). For exponential intensities $\lambda^a(\delta)=\lambda^b(\delta)=Ae^{-k\delta}$ they solve explicitly.

#### 2.2 Asymptotic expansion in inventory $q$

Expand $\theta(q,s,t)=\theta_0+q\theta_1+\tfrac12 q^2\theta_2+\dots$ (3.10). The indifference relations (3.4)–(3.5) give

$$r^a=\theta_1+(1-2q)\theta_2+\dots,\qquad r^b=\theta_1+(-1-2q)\theta_2+\dots,$$

so that $r=\tfrac{r^a+r^b}{2}=\theta_1-2q\theta_2$ and the spread is $\delta^a+\delta^b=2\theta_2+\tfrac{2}{\gamma}\ln(1+\tfrac{\gamma}{k})$. Grouping orders of $q$:

- **Order 1:** $\theta^1_t+\tfrac12\sigma^2\theta^1_{ss}=0$, $\theta^1(s,T)=s$ ⇒ $\theta_1(s,t)=s$ — the reservation price at *zero* inventory is simply the mid-price.
- **Order $q^2$:** $\theta^2_t+\tfrac12\sigma^2\theta^2_{ss}-\tfrac12\sigma^2\gamma(\theta^1_s)^2=0$, $\theta^2(s,T)=0$ ⇒

$$\theta_2(s,t)=\tfrac12\sigma^2\gamma\,(T-t).$$

Hence $r=\theta_1-2q\theta_2=s-q\gamma\sigma^2(T-t)$, recovering the frozen-inventory reservation price, and the spread is

$$\delta^a+\delta^b = 2\theta_2+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right)=\gamma\sigma^2(T-t)+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right). \qquad (3.18)$$

**Reading the spread.** It has two economics:
- $\dfrac{2}{\gamma}\ln(1+\tfrac{\gamma}{k})$ — the **adverse-selection/book component**: wider when risk aversion $\gamma$ is high or the book is thin (small $k$). In the risk-neutral limit $\gamma\to0$ this tends to $2/k$ (finite).
- $\gamma\sigma^2(T-t)$ — the **inventory-risk component**: wider when the position can hurt (high $\gamma$, high $\sigma^2$, far from $T$). It vanishes at $t=T$.

#### 2.3 The two-component interpretation of $\theta$

- $\theta_1$ = reservation price at zero inventory.
- $\theta_2=\tfrac12\gamma\sigma^2\tau$ = **sensitivity of the quotes to inventory**. If $\theta_2$ is large, accumulating $q>0$ drives the quotes aggressively down. The skew per unit inventory is exactly $2\theta_2\gamma\dots$ — see [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|04 · Inventory & Risk Aversion]].

---

### 3. Computational Implementation — the AS quote engine + paper verification

The engine below reproduces the paper's own spread column **exactly**. NumPy only.

```python
import numpy as np

def as_quotes(s, q, gamma, sigma, tau, k):
    """Optimal AS quotes. tau = T - t (remaining horizon).
       r   = s - q*gamma*sigma^2*tau            (reservation price)
       psi = gamma*sigma^2*tau + (2/gamma)*ln(1+gamma/k)  (total spread)
       ask = r + psi/2, bid = r - psi/2."""
    r   = s - q*gamma*sigma**2*tau
    psi = gamma*sigma**2*tau + (2.0/gamma)*np.log(1.0 + gamma/k)
    return r, r + psi/2.0, r - psi/2.0, psi

s, gamma, sigma, tau, k = 100.0, 0.1, 2.0, 1.0, 1.5
print("inventory skew (AS, sigma=2, T-t=1, gamma=0.1, k=1.5):")
for q in (-10, -5, 0, 5, 10):
    r, ask, bid, psi = as_quotes(s, q, gamma, sigma, tau, k)
    print(f"  q={q:+3d}: reservation={r:8.4f}  bid={bid:8.4f}  ask={ask:8.4f}  spread={psi:.4f}")

print("\nspread component (2/gamma)ln(1+gamma/k) vs AS paper Tables 1-3:")
for gamma in (0.01, 0.1, 0.5):
    print(f"  gamma={gamma:4.2f}: (2/g)ln(1+g/k)={(2.0/gamma)*np.log(1.0+gamma/k):.4f}")
```
```
inventory skew (AS, sigma=2, T-t=1, gamma=0.1, k=1.5):
  q=-10: reservation=104.0000  bid=103.1546  ask=104.8454  spread=1.6908
  q= -5: reservation=102.0000  bid=101.1546  ask=102.8454  spread=1.6908
  q= +0: reservation=100.0000  bid= 99.1546  ask=100.8454  spread=1.6908
  q= +5: reservation= 98.0000  bid= 97.1546  ask= 98.8454  spread=1.6908
  q=+10: reservation= 96.0000  bid= 95.1546  ask= 96.8454  spread=1.6908

spread component (2/gamma)ln(1+gamma/k) vs AS paper Tables 1-3:
  gamma=0.01: (2/g)ln(1+g/k)=1.3289
  gamma=0.10: (2/g)ln(1+g/k)=1.2908
  gamma=0.50: (2/g)ln(1+g/k)=1.1507
```
The stationary spread column reproduces the paper's Tables 1–3 ($\gamma=0.1\Rightarrow1.29$, $\gamma=0.01\Rightarrow1.33$, $\gamma=0.5\Rightarrow1.15$) to their published precision. Note the skew: at $q=+10$ *both* quotes sit $\$2$ below the mid (bid $95.15$, ask $96.85$) — the dealer is actively trying to sell.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Quote crossing / marketable quotes.** If the skew $q\gamma\sigma^2\tau$ exceeds half the spread, the "bid" rises above the "ask" of the *unskewed* market, or the quote becomes marketable (crosses the spread). Production engines clamp $\delta^{a},\delta^{b}\ge 0$ and cap $|q|$; the raw formula does not.
2. **Inventory-independent spread is an artefact.** $\delta^a+\delta^b$ is independent of $q$ *only* because intensities are exponential and the expansion is linear. A quadratic approximation of the arrival term makes $\theta_2$ solve a nonlinear PDE (AS §3.2) and restores inventory dependence — don't over-claim the closed form.
3. **The linear $\theta$ expansion is only good near $q=0$.** Guéant et al. (2013) show the approximation degrades for large inventories, where the true quotes must be clamped by an inventory limit. The AS formula is a *local* (small-$q$) result.
4. **Spread is quoted around $r$, not $s$.** A common bug is to quote the spread symmetrically about the mid and *then* add the skew — double-counting inventory. The correct construction: skew the centre to $r$ first, then add $\pm\psi/2$.

---

### 5. Canonical Literature & Study References

- **Avellaneda & Stoikov (2008)**, Quantitative Finance 8(3), §3.1 (optimal quotes, eq. 3.6–3.13) and §3.2 (asymptotic expansion in $q$, eq. 3.14–3.18). *The canonical derivations; eq. (3.18) reproduced and verified above.*
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, Math. & Financial Econ. 7(4) — the rigorous HJB solution and closed-form asymptotics that supersede the linear expansion for large $q$.
- **Cartea, Jaimungal & Penalva (2015)**, *Algorithmic and High-Frequency Trading*, Ch 10–11 — the A–S model as a special case of the general market-making framework.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/02-the-market-maker-problem|02 · The Market-Maker Problem]]
- Forward: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|04 · Inventory & Risk Aversion]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Index Hub]]
- Sibling: [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
