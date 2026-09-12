---
title: "6.2.2 The Market-Maker's Problem"
tags:
  - pillar-market-making
  - avellaneda-stoikov-and-optimal-quoting
  - stochastic-control
  - reservation-price
  - hjb
---

**Basic Prerequisites:** [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/01-from-zero-intuition|01 · From Zero]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page states the **market-maker's optimization problem** precisely and derives its first object - the **reservation (indifference) price**. The practical objective: before solving for quotes, understand *what the dealer is maximizing*, *why exponential utility is the right choice*, and *how the arrival rates of orders enter the problem*. Everything is the AS 2008 setup (§2) restated with the derivations filled in.

The model has three ingredients:

1. **A price process** - the mid-price $S_t$ follows arithmetic Brownian motion $dS_u=\sigma dW_u$. It is the dealer's *marking* price, not a price at which he can trade costlessly.
2. **A utility objective** - the dealer maximizes the expected utility of terminal wealth $X_T+q_TS_T$ under **constant absolute risk aversion (CARA)**: $u(z)=-\exp(-\gamma z)$.
3. **An arrival-rate mechanism** - his limit orders fill as Poisson processes whose intensities *decrease with distance* from the mid: $\lambda(\delta)=Ae^{-k\delta}$.

> **Why exponential utility?** It is the unique (up to affine) utility with **no wealth effect**: the optimal strategy does not change when you scale wealth, so the reservation price is *independent of initial cash $x$*. That is what makes the whole problem separable - the same reason AS can define clean indifference prices.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The frozen-inventory value function

Consider first an **inactive** dealer who holds $q$ shares to time $T$ and cannot trade. His wealth is $X_T+qS_T = x+qS_T$ (no interest). Since $S_T = s + \sigma(W_T-W_t) \sim \mathcal{N}(s, \sigma^2\tau)$ with $\tau=T-t$,

$$
v(x,s,q,t)=\mathbb{E}_t\!\left[-\exp\!\left(-\gamma(x+qS_T)\right)\right]
=-\exp(-\gamma x)\,\exp(-\gamma q s)\,\exp\!\left(\frac{\gamma^2q^2\sigma^2\tau}{2}\right). \qquad (\text{AS }2.3)
$$

The derivation is Gaussian-integral bookkeeping: $\mathbb{E}[-\exp(-\gamma q S_T)] = -\exp(-\gamma qs + \tfrac12\gamma^2q^2\sigma^2\tau)$ because the moment generating function of $\mathcal{N}(s,\sigma^2\tau)$ is $\exp(\gamma q s + \tfrac12\gamma^2q^2\sigma^2\tau)$ evaluated at the right sign.

#### 2.2 Reservation (indifference) prices (AS Definition 1)

The **reservation bid** $r^b$ is the price making the dealer indifferent between his current portfolio and his portfolio *plus one share*:

$$
v(x-r^b,\,s,\,q+1,\,t) = v(x,\,s,\,q,\,t). \qquad (2.4)
$$

The **reservation ask** $r^a$ solves $v(x+r^a,\,s,\,q-1,\,t)=v(x,\,s,\,q,\,t)$ (2.5). Substituting the closed-form $v$ and cancelling (both sides share $-\exp(-\gamma x)$, and the indifference makes the price independent of $x$):

$$
r^a(s,q,t) = s + (1-2q)\frac{\gamma\sigma^2\tau}{2}, \qquad
r^b(s,q,t) = s + (-1-2q)\frac{\gamma\sigma^2\tau}{2}. \qquad (2.6\text{–}2.7)
$$

Their **average is the reservation price**

$$
\boxed{\;r(s,q,t)=\frac{r^a+r^b}{2}= s - q\,\gamma\,\sigma^2\,(T-t)\;}
$$

**Interpretation.** Long $(q>0)$ ⇒ $r<s$ (wants out). Short $(q<0)$ ⇒ $r>s$ (wants in). The wedge $\gamma\sigma^2\tau$ is the price of one unit of inventory risk; the skew is $q$ times that.

#### 2.3 Order arrivals and the intensity law

AS assume market buy orders lift the dealer's ask at Poisson rate $\lambda^a(\delta^a)$ and sell orders hit his bid at rate $\lambda^b(\delta^b)$, both decreasing in the distance from the mid. Aggregating the empirical market-order size distribution ($f_Q(x)\propto x^{-1-\alpha}$) with the logarithmic price-impact law ($\Delta p\propto\ln Q$) gives

$$
\lambda(\delta)=\Lambda\,\mathbb{P}(\Delta p>\delta)=A\,e^{-k\delta}, \qquad A=\Lambda/\alpha,\;\; k=\alpha K. \qquad (2.11)
$$

($A$ = baseline arrival intensity; $k$ = how fast fills die off as you quote further out - the "liquidity density" of the book.)

#### 2.4 The Hamilton–Jacobi–Bellman equation (AS eq. 3.1–3.3)

With the dealer controlling $\delta^a,\delta^b$, wealth jumps as $dX_t=p^a dN^a_t - p^b dN^b_t$ and inventory is $q_t=N^b_t-N^a_t$. The value function

$$
u(s,x,q,t)=\max_{\delta^a,\delta^b}\mathbb{E}_t\!\left[-\exp\!\left(-\gamma(X_T+q_TS_T)\right)\right]
$$

solves the HJB equation

$$
u_t+\tfrac12\sigma^2u_{ss}
+\max_{\delta^b}\lambda^b(\delta^b)\!\left[u(s,x-s+\delta^b,q+1,t)-u(s,x,q,t)\right]
+\max_{\delta^a}\lambda^a(\delta^a)\!\left[u(s,x+s+\delta^a,q-1,t)-u(s,x,q,t)\right]=0,
$$

with terminal condition $u(s,x,q,T)=-\exp(-\gamma(x+qs))$. The two "max" terms are simply **the expected gain from a filled bid (inventory $+1$, cash $-p^b$) and a filled ask (inventory $-1$, cash $+p^a$)**, weighted by their arrival intensities. Because utility is exponential, the ansatz

$$
u(s,x,q,t)=-\exp(-\gamma x)\,\exp(-\gamma\theta(s,q,t)) \qquad (3.2)
$$

reduces the problem to a scalar equation for $\theta$ (AS eq. 3.3), which is the object the next page solves. Applying Definition 1 to the ansatz gives the clean relations $r^b=\theta(s,q+1,t)-\theta(s,q,t)$ and $r^a=\theta(s,q,t)-\theta(s,q-1,t)$ - the reservation prices are *first differences of $\theta$ in $q$*.

---

### 3. Computational Implementation - verifying the reservation price

We solve the indifference conditions (2.4)–(2.5) **numerically by bisection** on the exponential value function, and check they match the closed forms (2.6)–(2.7).



The numerically-solved indifference prices match eqs. (2.6)–(2.7) to machine precision, and their mean is the reservation price $r=s-q\gamma\sigma^2\tau$. At $q=+4$ the dealer values a share at $ $\$98.40, \1.60 below the \$100 mid - he is long and wants out.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Choosing the wrong risk measure.** Exponential (CARA) utility is what buys the wealth-independent reservation price. Swap in mean–variance and the clean separation survives *approximately* (AS appendix shows the analogous $R^a,R^b$ for geometric BM), but other risk measures change the skew non-linearly (Cartea & Jaimungal 2015). "Why exponential?" is a real modelling choice, not a detail.
2. **The intensity law is an empirical bet.** $\lambda(\delta)=Ae^{-k\delta}$ is *derived* from a power-law order-size distribution plus a logarithmic impact law - assume a different impact law (e.g. $\Delta p\propto Q^\beta$) and the intensity becomes a power law $B\delta^{-\alpha/\beta}$, changing the optimal spread. The functional form is a modelling choice that must be checked against the book.
3. **No drift, no autocorrelation, no information.** The mid-price has *no* predictable component in the AS setup. Any alpha signal (a drift $\mu$, an OFI-based forecast) is outside the model, and treating $dS=\sigma dW$ as literal when the flow is informed is the root cause of the failure modes in [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05 · Failure Modes]].
4. **Unbounded inventory.** The frozen-inventory problem allows any $q$; the reservation skew grows linearly in $q$ but never forbids a position. Real systems impose caps - see Guéant's bounded-inventory treatment in [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/06-advanced-extensions|06 · Advanced Extensions]].

---

### 5. References

- **Avellaneda & Stoikov (2008)**, Quantitative Finance 8(3)
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Math. & Financial Econ. 7(4)
- **Ho & Stoll (1981)**, JFE 9(1)

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/03-the-avellaneda-stoikov-model|03 · The AS Model]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics]]
