---
title: "6.4.6 Advanced Extensions"
tags:
  - pillar-market-making
  - kyles-lambda
  - pin
  - market-impact
  - price-discovery
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]].

---

### 1. Intuition & Practical Objective

The GM model reveals *why* the spread exists; this page launches the extensions that make it operational. GM gives **belief-driven** inference (informed traders arrive, the maker learns). Its three main descendants, all bridged here, attack different practical gaps:

1. **Kyle (1985) - strategic size, not just direction.** The informed trader chooses *how much* to trade, optimally hiding in noise volume. Out comes **Kyle's lambda** $\lambda$ - price impact per unit of order flow - and the celebrated result that exactly half of the private information is impounded in one round: $Var[v\mid y]=\Sigma_0/2$.
2. **PIN (Easley–Kiefer–O'Hara 1997) - estimating the informed fraction $\pi$.** $\pi$ is a *parameter*; PIN estimates it from daily buy/sell counts via a Poisson mixture, giving the empirical number the whole GM machinery needs.
3. **Event uncertainty (Easley–O'Hara 1992) - time is information.** When information events are themselves random, the arrival *pattern* (lulls, bursts) is informative - the bridge to modern toxicity and order-arrival models.

The objective: compute a Kyle equilibrium, recover its price-impact and impounding facts, and get the PIN formula in hand - all runnable.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Kyle (1985) one-shot equilibrium (Hasbrouck Ch 7)

$v\sim N(p_0,\Sigma_0)$; informed demand $x=\frac{v-p_0}{2\lambda}=\beta(v-p_0)$; noise $u\sim N(0,\sigma_u^2)$; market maker sees total flow $y=x+u$ and posts

$$
p=\lambda y+\mu,\qquad \lambda=\tfrac12\sqrt{\tfrac{\Sigma_0}{\sigma_u^2}},\qquad \beta=\sqrt{\sigma_u^2/\Sigma_0},\qquad \mu=p_0.
$$

**Kyle's lambda** $\lambda$ is the price impact per unit order flow; depth is $1/\lambda$. Magnitudes: $Var[v\mid p]=Var[v\mid y]=\Sigma_0/2$ - **half the private information is impounded, independent of noise intensity** - and informed profit $\mathbb{E}\pi=\frac{(v-p_0)^2}{2}\sqrt{\sigma_u^2/\Sigma_0}$ rises with the squared value divergence and with noise-trading variance (camouflage). Multi-period: the insider "slices and dices," $\Delta x_n=\beta_n(v-p_{n-1})\Delta t$, each round pricing in a further sliver (Hasbrouck Ch 7 §7.2). Price impact model in practice: $\Delta P=\lambda\,Q$ - the market-impact workhorse.

#### 2.2 PIN - the empirical informed probability (Hasbrouck Ch 6; EKOH 1997)

On each of many days an information event occurs with probability $\alpha$; when it does, informed traders arrive at intensity $\mu$ and always trade on the right side; uninformed arrive on both sides at intensity $\epsilon$. Daily buys $b\sim Poisson$, sells $s\sim Poisson$, so over $D$ days the likelihood is a Poisson-mixture of textbooks (eq 6.3) whose model parameters $\alpha,\mu,\epsilon$ are estimated by MLE, giving

$$
\mathrm{PIN}=\frac{\alpha\mu}{\alpha\mu+2\epsilon}\in[0,1].
$$

The *product* $\alpha\mu$ is identified (so PIN is stable/estimable even though $\alpha,\mu$ separately are imprecise - Hasbrouck Ch 6). PIN is the empirical estimate of the GM informed-fraction and of order-flow toxicity.

#### 2.3 Event uncertainty & the timing of information (Easley–O'Hara 1992)

When the arrival of information itself is uncertain, the *absence of trades* is informative: no-trade intervals are low-information states, bursts are high-information. Trade *timing* becomes a signal - the step from "does order direction tell me anything?" to "does the pattern of order arrivals tell me anything?" That is the theoretical backbone of modern order-flow-imbalance and toxic-flow detection.

---

### 3. Computational Implementation - Kyle lambda, impounding, and PIN (stdlib only)





The run confirms the two invariant facts of the informed-trading family: Kyle's price **immediately impounds the informed demand** (residual $p-v\approx0$), and exactly **half** the private information is incorporated in a single round ($Var[v\mid y]=2.0=\Sigma_0/2$). And PIN translates the model into an operational toxicity number: $0.43\to0.69$ as informed intensity rises. These are the numbers a maker or a researcher actually uses to set toxicity hedges and measure price impact.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Kyle's "lambda" is not a constant.** The one-shot $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ is a model value; empirically, price impact is concave in size, time-varying, and inventory/vol sensitive. Treating $\lambda$ as a static per-share parameter misprices large orders (see [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] for the inventory-driven correction).
2. **PIN's parameter bundle.** Only $\alpha\mu$ is well identified; $\alpha$ and $\mu$ separately are imprecise (Hasbrouck Ch 6). Don't over-interpret individual PIN pieces; the product is the stable quantity.
3. **The martingale property is about the maker's info, not your model.** "Prices are martingales" in GM refers to the *maker's* information set. If your model under-uses the right conditioning variables, the residual predictability is yours to miss - the semi-strong-form claim does not protect a poorly-specified model.
4. **One-shot Kyle hides the multi-period slicing.** The single-round result (half impounded) is the kernel of a sequence in which the insider spreads a finite information advantage over many rounds to raise total profit. Reading the one-shot as "all information enters instantly" mistakes the kernel for the process.

---

### 5. Canonical Literature & Study References

- **Kyle (1985)**, *Continuous auctions and insider trading*, Econometrica 53(6), 1315–1335 - the strategic model; $\lambda,\beta$, equilibrium, multi-period slicing. *Primary PDF in corpus; math verified via Hasbrouck Ch 7.*
- **Easley, Kiefer & O'Hara (1997)**, *The information content of the trading process*, JFE 44(1), 159–186 - the POISSON model and PIN. *Primary PDF: `37_Easley_1997...` in corpus.*
- **Easley & O'Hara (1992)**, *Time and the process of security price adjustment*, J. Finance 47(2), 577–605 - information uncertainty and no-trade unemployment. *Primary PDF: `22_Easley_1992...` in corpus.*
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 6 (PIN) and Ch 7 (Kyle) - both **math-verified** (`hasbrouck_ch6-10.md`; note Ch 7 conditional-profit form $\mathbb{E}\pi=\frac{(v-p_0)^2}{2}\sqrt{\sigma_u^2/\Sigma_0}$).
- **Glosten (1994)**, *Is the electronic open limit order book inevitable?*, J. Finance 49(4), 1127–1161 - why a competitive electronic book survives adverse selection; the modern queue-level version of this model (*primary PDF: `23_Glosten_1994...` in corpus; SUP reading*).

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Index Hub]]
- Forward/in-pillar: [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN (PIN in production)]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov Optimal Quoting (reservation pricing over this impact/inventory)]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model (measuring λ empirically)]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]