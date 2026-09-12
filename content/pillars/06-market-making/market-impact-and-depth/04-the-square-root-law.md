---
title: "6.7.4 The Square-Root Law of Market Impact"
tags:
  - pillar-market-making
  - market-impact
  - square-root-law
  - concavity
  - latent-liquidity
  - gatheral
---

**Basic Prerequisites:** [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|03 · Temporary vs Permanent]] and [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (book shape).

---

### 1. Intuition & Practical Objective

Kyle's linear rule, $P=p_0+\lambda y$, is the correct description of impact at the margin - for **small** orders over **short** horizons. Stretch it to large orders and it fails, badly and in a specific direction: **real market impact is concave - it grows roughly as the square root of order size.** Doubling your order does *not* double your impact; it multiplies it by about $\sqrt2\approx1.41$.

This single fact - the **square-root law** - is the most important empirical regularity in execution:

$$
I \;\approx\; \sigma\,Y\sqrt{\frac{Q}{V}}\quad(\text{or}\ \propto\sigma\sqrt{\text{participation rate}}),
$$

where $Q$ is the order size, $V$ the average volume, $\sigma$ the daily volatility, and $Y$ an $O(1)$ constant. It is why execution algorithms are not simply "trade the same fraction forever": they must account for the *concavity* of cost, which changes the optimal schedule, the marginal cost of size, and the answer to "should we even trade this?"

**Why concave, not linear?** Two complementary pictures:

1. **The book is not a wall - it's a hill.** Depth does not sit uniformly at every price; it thins as you move away from the touch. Squeeze more size into the market and you find progressively *less* liquidity per price level, so the price you must reach grows sublinearly in size. The canonical econophysics model (Bouchaud, Mézard & Potters 2002) formalises the order book as a diffusive object: the liquidity density at distance $\ell$ from the mid grows *linearly* in $\ell$, so cumulative liquidity grows as $\ell^2$ and the price needed to absorb a volume imbalance grows as $\sqrt{\Delta V}$ (§3 proves this numerically).

2. **Volatility sets the yardstick.** Empirically, impact scales with volatility and the *participation rate* (your share of the flow), not with raw size. Tóth et al. (2011) argue the deep reason: the ultimate submitters of large orders are *insensitive* to price moves of the order of daily volatility during execution, so impact accumulates as a random walk and ends up $\propto\sqrt{Q}$.

> **The one-sentence essence.** "Impact is concave in size - roughly the square root of participation - because liquidity thins with distance and because execution is a race against volatility; a linear-impact assumption understates the cost of small orders and overstates it for large ones."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The latent-liquidity origin of $\sqrt{Q}$

Model the book by its **cumulative liquidity** $L(\ell)$: the number of shares resting within a price distance $\ell$ of the mid. Two book shapes:

- **Flat book** (density $\rho(\ell)=\rho_0$ constant): $L(\ell)=\rho_0\ell$, so absorbing a flow $\Delta V$ needs a move $\ell=\Delta V/\rho_0$ - **linear** impact (Kyle).
- **Diffusive book** ($\rho(\ell)=\rho_0\ell$, the empirically observed thinning): $L(\ell)=\tfrac12\rho_0\ell^2$, so
$$
\Delta V=\tfrac12\rho_0\ell^2\;\Longrightarrow\;\boxed{\ \ell=\sqrt{\frac{2\,\Delta V}{\rho_0}}\ \propto\ \sqrt{\Delta V}\ }\quad\text{- square-root impact.}
$$

The square-root law, in this picture, is simply a statement about the *shape* of the book. (Order signs are long-memory - autocorrelation $C_\tau\sim\tau^{-\gamma}$ with $\gamma\approx0.5$ - which is what keeps the book diffusive and reproduces the same concavity under a propagator treatment.)

#### 2.2 The empirical functional form (Almgren et al. 2005)

Fitting power laws $g(v)=c\,|v|^\alpha\mathrm{sgn}(v)$, $h(v)=c'|v|^\beta\mathrm{sgn}(v)$ to real metaorders gives

$$
I=\gamma\,\sigma\,\frac{X}{V}\Big(\frac{\Theta}{V}\Big)^{1/4}\quad(\text{permanent}),\qquad
J=\frac{I}{2}+\mathrm{sgn}(X)\,\eta\,\sigma\Big(\frac{X}{VT}\Big)^{3/5}\quad(\text{realized}),
$$

with $X$ order size, $V$ average daily volume, $\Theta$ shares outstanding, $T$ execution duration in volume time, and fitted coefficients

$$
\gamma=0.314\pm0.041,\qquad \eta=0.142\pm0.0062 .
$$

Three messages: (i) the **permanent exponent is fixed at $1$** (linear, forced by no-arbitrage - Huberman–Stanzl); (ii) the **temporary exponent is $3/5$**, *not* the square root $1/2$ - the pure square-root model is rejected at 95%; (iii) the residual $R^2$ is under 1% because volatility dominates the *realized* impact of any single order, which is exactly why impact estimation requires averaging over many metaorders.

#### 2.3 The Bouchaud–Farmer–Lillo exponent

For a propagator model with order-sign autocorrelation decaying as $C_\tau\sim\tau^{-\gamma}$, an executed metaorder of $N$ slices has impact scaling as $N^{1-\beta}$ with $\beta=(1-\gamma)/2$. Empirical $\gamma\approx0.5\Rightarrow\beta\approx0.25\Rightarrow$ impact $\sim N^{3/4}$. The impact also scales as $\pi^{\beta}$ in the participation rate $\pi$: **the slower the execution, the smaller the impact** (and in the limit of infinitely slow execution, impact $\to0$). This is the same qualitative message as the temporary/permanent split of page 03, derived from order-flow memory rather than from resilience.

#### 2.4 The no-arbitrage constraint on concavity (Gatheral)

Concavity cannot be arbitrary, or the market admits **price manipulation**. Gatheral (2010): for a transient-impact model $S_t=S_0+\int_0^t h(\dot X_s)G(t-s)\,ds$ with impact function $h(x)=c|x|^\delta\mathrm{sgn}(x)$ and decay kernel $G(\tau)=\tau^{-\gamma}$,

$$
\boxed{\ \text{price manipulation exists}\iff \gamma+\delta<1\ }.
$$

Empirically $\delta\approx0.5$ (square-root impact) and $\gamma\approx0.5$ (square-root decay) - sitting *exactly on the boundary*, so observed impact is just barely consistent with no-dynamic-arbitrage. A finite-at-zero kernel such as **exponential decay** combined with any **nonlinear** impact function is ruled out (Prop. 22.14) - the price-impact decay must be *slow* (power-law), a striking theoretical constraint on any "impact decays in seconds" claim.

---

### 3. Computational Implementation - why the book's shape gives $\sqrt{\ }$

Sweep a volume imbalance $\Delta V$ through two books and fit the log-log slope. A **diffusive** book (liquidity per price level $\propto$ distance, $\rho(\ell)=\ell$) gives slope $\tfrac12$; a **flat** book gives slope $1$. Stdlib only.





The regression recovers the square-root exponent **0.5054** on the diffusive book and **1.0000** on the flat book - confirming the derivation: *the concavity of impact is a direct consequence of how liquidity is distributed away from the touch.* The analytic check $\sqrt{2\Delta V}=141.4$ matches the simulated 141 exactly.

**How a practitioner measures the exponent.** Regress $\log I$ on $\log(Q/V)$ across a sample of metaorders (Almgren et al.'s procedure). The slope is your estimate of the exponent: $\approx1$ means the venue behaves linearly (thin, Kyle-like), $\approx0.5$ means square-root, and anything below $1$ with slow impact decay is consistent with no-dynamic-arbitrage.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Fitting linear impact to square-root data.** The most damaging misspecification: linear models **overstate** the cost of large orders (they treat impact as proportional, so the fitted line sits above the concave curve at the large sizes) and mis-price the marginal cost of size, which is precisely the decision a large order turns on.
2. **Over-fitting the exponent.** Almgren et al. reject the pure $\tfrac12$ square root at 95% in favour of $\tfrac35$; quoting "the square-root law" as exact is a simplification. The *sign* of the concavity is robust; the exact exponent is venue- and size-regime-dependent.
3. **Ignoring that impact scales with volatility, not size alone.** $I\propto\sigma\sqrt{Q/V}$ means the same order costs twice as much in a high-vol regime. Backtests that fix $\sigma$ under-charge exactly when it matters most.
4. **Assuming fast impact decay.** A kernel that decays too quickly (e.g. exponential) plus nonlinear impact **implies arbitrage** (Gatheral) - it lets a strategy buy, wait, sell, and profit risklessly. Empirically impact decays *slowly*, so any model that "resets" impact within a day is suspect.
5. **Confusing the square-root law of *temporary* impact with *permanent* impact.** The empirical concavity is in the temporary/realized component; the permanent component is (approximately) linear. Applying a square-root rule to permanent impact contradicts no-arbitrage (Huberman–Stanzl).
6. **Neglecting the participation-rate dependence.** Impact scales with *how you cut the order*, not just its size: the same order executed at a higher participation rate has strictly higher impact ($\pi^\beta$). A backtest that ignores participation is not measuring impact, it is measuring size.

---

### 5. Canonical Literature & Study References

- **Almgren, R., Thum, C., Hauptmann, H. & Li, H. (2005)**, *Direct estimation of equity market impact*, Risk 18(7), 57–62. *The fitted exponents and coefficients ($\gamma=0.314$, $\eta=0.142$, temporary $\beta=3/5$, square root rejected). Primary PDF in corpus (`45_Almgren_2005_...`).*
- **Bouchaud, J.-P., Farmer, J. D. & Lillo, F. (2009)**, *How markets slowly digest changes in supply and demand*. *Order-flow long memory, impact concavity, the $N^{1-\beta}$ and $\pi^\beta$ results. Primary PDF in corpus (`44_Bouchaud_2009_...`).*
- **Gatheral, J. (2010)**, *No-dynamic-arbitrage and market impact*, Quantitative Finance 10(7), 749–759. *The $\gamma+\delta\ge1$ constraint and the exclusion of exponential decay + nonlinear impact. Primary PDF in corpus (`42Gatheral2010_...`).*
- **Gatheral, J. & Schied, A. (2013)**, *Dynamical models of market impact and algorithms for order execution*. *Remark 22.15: $\delta\approx0.5,\gamma\approx0.5$; Tóth et al. mechanism. Primary PDF in corpus (`46_Gatheral_2013_...`).*
- **Tóth, B., Lempérière, Y., Deremble, C., de Lataillade, J., Kockelkoren, J. & Bouchaud, J.-P. (2011)**, *Anomalous price impact and the critical nature of liquidity in financial markets*, Phys. Rev. X 1, 021006. *The square-root law across a very large range of sizes and the insensitivity mechanism.*
- **Bouchaud, J.-P., Mézard, M. & Potters, M. (2002)**, *Statistical properties of stock order books*, Quantitative Finance 2(4), 251–256. *The diffusive-book model behind the square root. Primary PDF in corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|03 · Temporary vs Permanent]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
- Forward: [[pillars/06-market-making/market-impact-and-depth/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/market-impact-and-depth/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/06-market-making/market-impact-and-depth/index|Index Hub]]
- Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Almgren–Chriss (Pillar 2)]] (the scheduler consumes this cost function) · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]] (Amihud is a square-root-flavoured proxy)
