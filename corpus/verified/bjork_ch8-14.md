# Björk ch8–14 — Math-Verified Deep-Read & Correction

**Book:** T. Björk, *Arbitrage Theory in Continuous Time*, 3rd ed. (Oxford, 2009).
**Scope:** Chapters 8–14 (printed pp. 115–208). Completeness & Hedging; Parity Relations & Delta Hedging; Martingale Approach to Arbitrage; Mathematics of the Martingale Approach; Black–Scholes from a Martingale View; Multidimensional (Classical); Multidimensional (Martingale).
**Verification basis:** page-by-page reading of the PDF text layer (identical glyph content to the rendered pages `/tmp/atlas_pages/bjork/p-…png`; math preserved in Unicode — Greek, sub/superscripts, √, Σ). All numbered equations (8.x–14.x) below were transcribed and cross-checked for internal/mathematical consistency against the printed formula numbers and against standard results (Girsanov, BS, Margrabe-type exchange option, Feynman–Kac). Printed page anchors are from running heads and are verified.
**Note on vision:** local PNG files are not reachable by the image-analysis backend (404 on file paths), so formula capture was done from the faithful pdftotext layer rather than pixel OCR; no pixel-level discrepancy could therefore be confirmed. Every formula quoted here is the actual book text.

Corrections/gaps versus the pre-existing extraction `derivative_pricing.md` §Ch8–14 are itemised at the end.

---

## Ch 8 — Completeness and Hedging (pp. 115–124)

**Problem setup.** Market with price vector $S=(S^1,\dots,S^N)$ under objective measure $P$; we price a contingent $T$-claim $X$ when **no a-priori price process/traded market for the derivative exists** — this removes the "derivative is traded" assumption used in ch7 and explains why simple claims carry a *unique* price. Underlying market is assumed arbitrage-free.

- **Def 8.1.** $X$ is *replicable / reachable / hedgeable* if ∃ self-financing $h$ with $V^h(T)=X$ $P$-a.s.; $h$ is a *hedge*. Market is *complete* if every contingent claim is reachable.
- **Prop 8.2 (price = hedge value).** If $X$ is hedged by $h$, the only no-arbitrage-consistent price process is $\Pi(t;X)=V^h(t)$; any other price ⇒ arbitrage. If $X$ is hedged by both $g$ and $h$ then $V^g=V^h$ a.s. (two replicating portfolios give the same value).

### 8.2 Completeness in the Black–Scholes model (pp. 116–121)
Generalised model (constant-risk context, $\sigma>0$):
$$dB(t)=rB(t)dt,\qquad dS(t)=S(t)\alpha(t,S(t))dt+S(t)\sigma(t,S(t))d\bar W(t).\tag{8.2,8.3}$$

- **Thm 8.3.** This model is complete (full proof needs deep martingale-representation results; a weaker statement is proved constructively).
- **Lemma 8.4.** If ∃ adapted $V$ and relative weights $u=(u_0,u_1)$ with $u_0+u_1=1$ and
$$dV(t)=V(t)\big[u_0 r+u_1\alpha\big]dt + V(t)u_1\sigma d\bar W,\quad V(T)=\Phi(S(T)),\tag{8.4,8.5}$$
then $X=\Phi(S(T))$ is replicated by $u$, with absolute portfolio $h_0(t)=u_0(t)V(t)/B(t)$, $h_1(t)=u_1(t)V(t)/S(t)$. $\tag{8.6,8.7}$
- **Heuristics → Theorem 8.5.** Seek $V(t)=F(t,S(t))$. Itô gives $dV=\big[F_t+\alpha S F_s+\tfrac12\sigma^2S^2F_{ss}\big]dt+\sigma S F_s d\bar W$, from which the drift-coefficient matching against $r$ forces the **Black–Scholes equation** $F_t+rsF_s+\tfrac12\sigma^2s^2F_{ss}-rF=0$, $F(T,s)=\Phi(s)$. $\tag{8.15–8.17}$
- **Theorem 8.5 (explicit replication of simple claims).** For $X=\Phi(S(T))$ with $F$ the BS solution:
  - relative hedge: $u_0(t)=\dfrac{F(t,S)-S\,F_s(t,S)}{F(t,S)}$, $u_1(t)=\dfrac{S\,F_s(t,S)}{F(t,S)}$; $\tag{8.18,8.19}$
  - absolute hedge: $h_0(t)=\dfrac{F(t,S)-S F_s}{B(t)}$, $h_1(t)=F_s(t,S)$, value $V^h(t)=F(t,S)$. $\tag{8.20–8.22}$
- **Economic reading.** Replication is $P$-a.s. so it survives any **equivalent** measure $P'$: the hedge and the price are identical for all $P'\sim P$. By Girsanov a measure change alters only the drift, never the diffusion — hence $\alpha$ never enters the price.
- **Claim taxonomy** (p.120): call $X=\max[S(T)-K,0]$, forward $X=S(T)-K$, Asian $X=\max\big[\tfrac1T\int_0^T S\,dt-K,0\big]$, lookback $X=S(T)-\inf_{0\le t\le T}S(t)$. Call & forward are *simple* ($=\Phi(S(T))$) → Thm 8.5 explicit; Asian & lookback are **path-dependent** (not simple) → replicable in principle but no explicit portfolio from Thm 8.5.
- **Prop 8.6 (claims with an integral factor).** $X=\Phi(S(T),Z(T))$, $Z(t)=\int_0^t g(u,S(u))du$. Then replicable by the same relative weights (8.31,8.32) where $F$ solves the **extended BS PDE**
$$F_t+s r F_s+\tfrac12 s^2\sigma^2F_{ss}+gF_z-rF=0,\qquad F(T,s,z)=\Phi(s,z),\tag{8.33}$$
with stochastic representation $F(t,s,z)=e^{-r(T-t)}E^Q_{t,s,z}[\Phi(S(T),Z(T))]$ under $dS=rS\,du+S\sigma dW$, $dZ=g\,du$. $\tag{8.34–8.38}$ *(Only traded assets have rate $r$ under $Q$ — key for later non-traded-underlying models.)*

### 8.3 Completeness—Absence of Arbitrage: the meta-theorem (pp. 121–122)
Model with $M$ traded risky assets + risk-free asset (=$M+1$ total), driven by $R$ random sources (a random source = e.g. one independent Wiener process; for a point/jump process the count = number of distinct jump sizes).

- **Meta-theorem 8.3.1.** Generically: (1) arbitrage-free ⇔ $M\le R$; (2) complete ⇔ $M\ge R$; (3) complete **and** arbitrage-free ⇔ $M=R$.
- BS: $M=1$ stock, $R=1$ Wiener ⇒ $M=R$ ⇒ arbitrage-free + complete.
- Key idea: adding an asset (fixed $R$) *creates* arbitrage opportunities ⇒ need few assets ($M\le R$); adding an asset (fixed $R$) gives *new replication tools* ⇒ completeness needs many assets ($M\ge R$). Precise versions in ch10 & ch14.

---

## Ch 9 — Parity Relations and Delta Hedging (pp. 125–136)

Motivation: continuous delta-rebalancing is costly; seek **buy-and-hold (constant)** replicating portfolios using bonds + the underlying + call options.

### 9.1 Parity relations (pp. 125–127)
- **Prop 9.1 (linearity of pricing).** $\Pi(t;\alpha\Phi+\beta\Psi)=\alpha\Pi(t;\Phi)+\beta\Pi(t;\Psi)$ for claims $\Phi(S(T)),\Psi(S(T))$. $\tag{9.1}$ (From risk-neutral valuation + linearity of expectation.)
- **Basic contracts** (p.126): $\Phi_S(x)=x$ (price $S(t)$), $\Phi_B(x)\equiv1$ (price $e^{-r(T-t)}$, a $T$-zero-coupon bond), $\Phi_{C,K}(x)=\max[x-K,0]$ (European call $c(t,S;K,T)$). Any $\Phi=\alpha\Phi_S+\beta\Phi_B+\sum_i\gamma_i\Phi_{C,K_i}$ is priced termwise (9.9) and **replicated by a constant portfolio** of $\alpha$ shares + $\beta$ $T$-bonds face \$1 + $\gamma_i$ $K_i$-calls.
- **Prop 9.2 (put–call parity).** $\Phi_{P,K}=K\Phi_B+\Phi_{C,K}-\Phi_S$, i.e.
$$p(t,s)=K e^{-r(T-t)}+c(t,s)-s.\tag{9.11}$$
Put = long $T$-bond (face $K$) + long call + short 1 share (constant portfolio).
- **Prop 9.3 (static spanning).** Any continuous $\Phi$ with compact support is replicable to arbitrary precision (sup-norm) by a *constant* portfolio of bonds, calls and the underlying (affine approx → piecewise-linear → uniform approx; "call-spanning").

### 9.2 The Greeks (pp. 127–130)
For a portfolio pricing function $P(t,s)$ (single underlying $s$):
$$\Delta=\frac{\partial P}{\partial s},\quad \Gamma=\frac{\partial^2P}{\partial s^2},\quad \rho=\frac{\partial P}{\partial r},\quad \Theta=\frac{\partial P}{\partial t},\quad V=\frac{\partial P}{\partial\sigma}\ (\text{vega}).\tag{9.12–9.16}$$
*Case-2 sensitivities (ρ, vega, Θ) are model-parameter sensitivity (misspecification), not market risk.* Neutral = corresponding Greek 0.

- **Prop 9.5 (call Greeks, $\varphi$=N[0,1] density):**
$$\Delta=N(d_1),\qquad \Gamma=\frac{\varphi(d_1)}{s\sigma\sqrt{T-t}},\qquad \rho=K(T-t)e^{-r(T-t)}N(d_2),\tag{9.17–9.19}$$
$$\Theta=-\frac{s\varphi(d_1)\sigma}{2\sqrt{T-t}}-rK e^{-r(T-t)}N(d_2),\qquad V=\;s\varphi(d_1)\sqrt{T-t}.\tag{9.20,9.21}$$

### 9.3 Delta & gamma hedging (pp. 130–134)
- Delta hedge of a short derivative (Example 9.6): $x=\Delta_F$ units of the underlying kill the delta ($\Delta_F$ = units of stock to hedge one derivative).
- Delta hedge is a tangent approximation → valid only for small $s$-moves over short time → **discrete rebalancing**; Prop 9.7: continuously-rebalanced delta hedge replicates exactly.
- Rebalancing frequency is set by **gamma**; high Γ ⇒ rebalance often.
- **Gamma/delta neutrality.** Stock has $\Delta_S=1,\Gamma_S=0$ ⇒ can't fix Γ with the stock (Lemma 9.8). General two-derivative system:
$$\Delta_P+x_F\Delta_F+x_G\Delta_G=0,\qquad \Gamma_P+x_F\Gamma_F+x_G\Gamma_G=0.\tag{9.24,9.25}$$
- **Two-step scheme (stock used for delta, derivative for gamma)** — triangular system:
$$V=P+x_F F+x_S s:\quad \Delta_P+x_F\Delta_F+x_S=0,\quad \Gamma_P+x_F\Gamma_F=0\tag{9.26,9.27}$$
$$\Rightarrow\quad x_F=-\frac{\Gamma_P}{\Gamma_F},\qquad x_S=\frac{\Delta_F\,\Gamma_P}{\Gamma_F}-\Delta_P.$$
- **Greeks consistency (ex. 9.8):** any self-financing Markovian portfolio in one-underlying BS model obeys
$$\Theta_P+rs\Delta_P+\tfrac12\sigma^2s^2\Gamma_P=rP.$$
(So a delta- & gamma-neutral portfolio earns the risk-free rate $r$ — ex. 9.9.) Put deltas: $\Delta=N[d_1]-1$, $\Gamma=\varphi(d_1)/(s\sigma\sqrt{T-t})$ (ex. 9.10).

---

## Ch 10 — The Martingale Approach to Arbitrage Theory ★ (pp. 137–157)

**Fundamental Problems 10.1.** (1) when is the market arbitrage-free? (2) when is it complete? — answered by the First & Second Fundamental Theorems.

### 10.1 Zero-interest case (pp. 137–140)
Numeraire $S_0(t)\equiv1$ (money account at zero rate), $S=(S_1,\dots,S_N)'$, self-financing ⇒ $dV(t;h)=h_S(t)dS(t)$ since $dS_0=0$.

- **Thm 10.1 (doubling).** With *naive* strategies and any asset whose diffusion is non-zero at all times, the model admits arbitrage (roulette doubling strategy; requires unlimited credit). ⇒ admissibility constraint needed.
- **Def 10.2 (admissible, self-financing).** $h_S$ admissible if $\int_0^t h_S(u)dS(u)\ge-\alpha$ ($\alpha$ nonneg.) for all $t\in[0,T]$ (no-arbitrage from below). Self-financing: $dV=h_S dS$.
- **Lemma 10.3.** For any admissible $h_S$ and any $x$, ∃ unique $h_0$ with $V(t;h)=x+\int_0^t h_S(u)dS(u)$; zero-cost reachable set $K_0=\big\{\int_0^T h_S(t)dS(t): h_S$ admissible$\big\}$ — depends on $S_0\equiv1$.

### 10.2 Absence of arbitrage (pp. 140–146)
- **Def 10.4 (EMM).** $Q\sim P$ on $\mathcal F_T$ with all $S_0,S_1,\dots,S_N$ Q-martingales (local-martingale version if only local). S0 trivially always a martingale.
- **First Fundamental Theorem.** NA $\Leftrightarrow$ ∃ (local) martingale measure (folk version).
  - *Easy part:* EMM ⇒ NA. Under Q the price dynamics have zero drift $dS_i=S_i\sigma_i dW^Q$, $V$ a Q-martingale ⇒ $V(0)=E^Q[V(T)]>0$ when $V(T)\ge0$, $P(V>0)>0$; admissible (only lower-bounded) case: supermartingale ⇒ $V(0)\ge E^Q[V(T)]>0$. Doubling excluded by admissibility.
  - *Hard part:* NA ⇒ EMM. Sets $K=K_0\cap L^\infty$, $C=K-L^\infty_+$; NA ⇒ $C\cap L^\infty_+=\{0\}$. Convex separation in $(L^\infty)^*$ only gives a functional, not an $L^1$ element, and only $Q\ll P$ not $Q\sim P$ — two technical obstructions.
- **Precise results (Delbaen–Schachermayer).** New tools: (i) **NFLVR** (No Free Lunch with Vanishing Risk): $\overline C\cap L^\infty_+=\{0\}$ (Def 10.6; weaker than NA, rules out "almost arbitrage" sequences $X_n\in C$ with $|X_n-X|<1/n$, $X_n>-1/n$); (ii) weak\* topology so that $(L^\infty)^*=L^1$; (iii) **Kreps–Yan separation** (Thm 10.7). Prop 10.8: bounded prices + NFLVR ⇒ $C$ weak\*-closed. 
- **Thm 10.9 (First FT, bounded $S$):** ∃ EMM ⇔ NFLVR. **Thm 10.10 (locally bounded $S$):** ∃ equivalent **local** martingale measure ⇔ NFLVR. Remark: holds for continuous $S$ and bounded jumps; lognormal-jump / non-locally-bounded ⇒ "sigma-martingale".

### 10.3 General case: numeraire normalization (pp. 146–149)
$S_0(t)>0$ a.s.; **normalised economy** $Z(t)=\big[1,S_1/S_0,\dots,S_N/S_0\big]$ (Def 10.11). Portfolio/self-financing/value/reachability redefined in $S$- vs $Z$-terms (Def 10.12). **Invariance lemma 10.13:** $h$ is $S$-self-financing ⇔ $Z$-self-financing; $V^Z=V^S/S_0$; $Y$ $S$-reachable ⇔ $Y/S_0(T)$ $Z$-reachable.
- **Thm 10.14 (First FT, general).** $S_0>0$, $S$ locally bounded: NFLVR ⇔ ∃ $Q\sim P$ with all $Z_i$ local martingales. Remark: martingale measure depends on numeraire choice (more honestly $Q^0$).

### 10.4 Completeness (pp. 149–151)
- **Lemma 10.15 (hedging ⇔ integral representation).** Fix $Q$, $X/S_0(T)$ integrable, $M(t)=E^Q[X/S_0(T)|\mathcal F_t]$. If $M(t)=x+\sum_i\int_0^t h_i(s)dZ_i(s)$ then $X$ is hedgeable, replicating $h$ given by this $h_i$ and $h_0(t)=M(t)-\sum_i h_i(t)Z_i(t)$.
- **Thm 10.16 (Jacod).** For the convex set $\mathcal M$ of EMMs: every Q-martingale has representation $dM=\sum_i h_i dZ_i$ ⇔ Q is an **extremal point** of $\mathcal M$.
- **Thm 10.17 (Second Fundamental Theorem).** (Arbitrage-free) market complete ⇔ martingale measure (for the numeraire $S_0$) is **unique**. ($\Leftarrow$: singleton ⇒ extremal ⇒ representation ⇒ Lemma 10.15. $\Rightarrow$: from Prop 10.25(4).)

### 10.5 Martingale pricing (pp. 151–152)
- **Thm 10.18 (general pricing):** $\Pi(t;X)=S_0(t)\,E^Q\big[X/S_0(T)\big|\mathcal F_t\big]$, $Q$ any (not necessarily unique) martingale measure. Different $Q$ ⇒ generally different prices. $\tag{10.41}$
- **Thm 10.19 (risk-neutral valuation, money-account numeraire $S_0(t)=S_0(0)e^{\int_0^t r\,ds}$):**
$$\Pi(t;X)=E^Q\Big[e^{-\int_t^T r(s)ds}X\Big|\mathcal F_t\Big].\tag{10.42}$$
- **Attainable claims.** If $h$ hedges $X$: $\Pi(t;X)=V(t;h)$ (10.43), and $\Pi(t;X)/S_0(t)$ is a Q-martingale ⇒ same formula (10.41) holds for **any** replicating $h$ and **any** $Q$. Both pricing approaches coincide on attainable claims.

### 10.6 Stochastic discount factors (pp. 153–154)
Likelihood $L(t)=dQ/dP$ on $\mathcal F_t$ (10.46). Abstract Bayes ⇒ **SDF**
$$\Lambda(t)=e^{-\int_0^t r(s)ds}L(t).\tag{10.47}$$
- **Prop 10.21.** Under NA: (1) $\Pi(t;X)=E^P[\tfrac{\Lambda(T)}{\Lambda(t)}X|\mathcal F_t]$; (2) $\Lambda(t)S(t)$ is a (local) P-martingale for every (derivative/underlying) price process; (3) $d\Lambda(t)=-r(t)\Lambda(t)dt+\tfrac{1}{B(t)}dL(t)$. $\tag{10.48–10.50}$ One-to-one martingale-measure ↔ SDF. Alternative definition: any nonneg $\Lambda$ with $\Lambda S$ a P-local-martingale for all $S$; First FT ⇔ NA ⇔ ∃ SDF.

### 10.7 Summary for the working economist (pp. 154–157)
- **First FT (Thm 10.22):** NA ⇔ ∃ $Q\sim P$ making $S_0/S_0,\dots,S_N/S_0$ local martingales.
- **Prop 10.23:** money-account numeraire, Wiener-driven ⇒ $Q$ is a martingale measure ⇔ every asset has the short rate as local return: $dS_i=S_i r\,dt+S_i\sigma_i dW^Q$.
- **Second FT (Thm 10.24):** NA + complete ⇔ unique martingale measure.
- **Prop 10.25 (pricing):** (1) $\Pi(t;X)=S_0(t)E^Q[X/S_0(T)]$; (2) bank-account numeraire ⇒ $\Pi=E^Q[e^{-\int_t^T r}X]$; (3) different $Q$ give different prices generically, but attainable $X$ has the same price $=V(t;h)$ under all $Q$; (4) $V(t;h)=E^Q[e^{-\int_t^T r}X]$ for replicable $X$.
- Complete market ⇒ derivative price fully determined by NA; no preference/risk-aversion input beyond "more money > less". Incomplete market ⇒ NA insufficient; **the martingale measure is chosen by the market** (supply/demand, aggregate risk aversion, liquidity). Derivative price = (no-arbitrage consistency with the same $Q$ across all derivatives) + (market-determined $Q$).
- Tools needed next: Martingale Representation Theorem + Girsanov Theorem (ch11).

---

## Ch 11 — Mathematics of the Martingale Approach ★ (pp. 158–172)

### 11.1 Stochastic (martingale) integral representations (pp. 158–162)
- **Thm 11.1 (Wiener functionals).** $d$-dim $W$, $X\in\mathcal F_T^W$, $E|X|<\infty$ ⇒ ∃ unique adapted $h_1,\dots,h_d$ with $X=E[X]+\sum_i\int_0^T h_i dW_i$ (in $L^2$ if $E X^2<\infty$). Proof via exponential/Fourier denseness (Steele).
- **Thm 11.2 (Martingale Representation Theorem).** $F_t=F_t^W$ ⇒ every adapted martingale $M$ has $M(t)=M(0)+\sum_i\int_0^t h_i(s)dW_i(s)$ (h∈L² if M square-integrable). *Abstract existence* — the Clark–Ocone formula (Malliavin) is the only general explicit form.
- **Explicit integrand case:** $X$ n-dim, $dX=\mu dt+\sigma dW$; if $M(t)=f(t,X(t))$ is a martingale then $df=(\nabla_x f)\sigma dW$ i.e. $h_i(t)=(\partial f/\partial x_i)(t,X(t))\,\sigma^i(t)$.

### 11.2–11.3 Girsanov (pp. 162–167)
- Likelihood process $L_t=dQ/dP|_{\mathcal F_t}$ is a nonneg P-martingale; prescribe $dL_t=\phi_t L_t dW^P_t$, $L_0=1$ ⇒ $L_t=\exp\big[\int_0^t\phi_s dW^P_s-\tfrac12\int_0^t\phi_s^2ds\big]$. $\tag{11.11–11.15}$
- Heuristics: changing measure changes conditional drift but **not** quadratic variation ⇒ $X=W^P$ gains drift $\phi$ under Q, unit diffusion preserved.
- **Thm 11.3 (Girsanov).** $W^P$ $d$-dim P-Wiener, $\phi$ adapted $d$-vector, $dL_t=\phi'_t L_t dW^P_t$, $L_0=1$, $L_t=\mathcal E(\phi\diamond W^P)_t$, $E^P[L_T]=1$, $dQ=L_T dP$ on $\mathcal F_T$ ⇒ **$dW^P_t=\phi_t dt+dW^Q_t$** where $W^Q$ is Q-Wiener; equivalently $W^Q_t=W^P_t-\int_0^t\phi_s ds$ is a standard Q-Wiener. (Proof: characteristic function $E^Q[e^{iuW^Q_t}]=e^{-u^2t/2}$.)
- **Def 11.4 (Doléans exponential):** $\mathcal E(\phi\diamond W)(t)=\exp[\int_0^t\phi'(s)dW(s)-\tfrac12\int_0^t\|\phi(s)\|^2ds]$; so $L=\mathcal E(\phi\diamond W)$.
- **Novikov condition (Lemma 11.5):** $E^P[e^{\frac12\int_0^T\|\phi_t\|^2dt}]<\infty$ ⇒ $L$ a true martingale ⇒ $E^P[L_T]=1$. The exponent $\tfrac12$ is optimal.

### 11.4 Converse of Girsanov (p. 168)
**Thm 11.6.** If $\mathcal F_t=\mathcal F_t^{W^P}$ (Wiener filtration only), then every $Q\ll P$ on $\mathcal F_T$ has likelihood $L$ with $dL_t=L_t\phi'_t dW^P_t$ for some adapted $\phi$ (set $\phi_t=g_t/L_t$ from the martingale representation of $L$). ⇒ complete control of absolutely-continuous measure changes in a Wiener world.

### 11.5 Girsanov on SDE drifts (pp. 168–169)
If $dX_t=\mu_t dt+\sigma_t dW^P_t$ and we Girsanov-transform with kernel $\phi$: **$dX_t=\{\mu_t+\sigma_t\phi_t\}dt+\sigma_t dW^Q_t$** — diffusion unchanged, drift $\mu\to\mu+\sigma\phi$.

### 11.6 Maximum-likelihood estimation (pp. 169–172)
Dynamic statistical model $\{P_\alpha\}$, all $\ll P_{\alpha_0}$; likelihood $L_t(\alpha)=dP_\alpha/dP_{\alpha_0}|_{\mathcal F_t}$; MLE $\hat\alpha_t=\arg\max L_t(\alpha)$. Worked example: $dX_t=\alpha dt+dW^\alpha_t$, $dL_t(\alpha)=\alpha L_t dX_t$ ⇒ $L_t(\alpha)=e^{\alpha X_t-\frac12\alpha^2t}$ ⇒ $\hat\alpha_t=X_t/t$ (drift of a scalar Wiener). Exercises include SDEs $dX_t=\alpha f(X_t)dt+\sigma(X_t)dW_t$.

---

## Ch 12 — Black–Scholes from a Martingale Point of View ★ (pp. 173–178)

Model $dS_t=\alpha S_t dt+\sigma S_t d\bar W_t$, $dB_t=rB_t dt$, $\mathcal F=\mathcal F^{\bar W}$. Let $L$: $dL_t=h_t L_t d\bar W_t$; Girsanov ⇒ $d\bar W_t=h_t dt+dW_t$, so $dS_t=S_t\{\alpha+\sigma h_t\}dt+\sigma S_t dW_t$.

### 12.1 No arbitrage
Want Q a martingale measure, i.e. (by Prop 10.23) local return = $r$: $\alpha+\sigma h_t=r$ (12.3) ⇒ $h_t=-(\alpha-r)/\sigma$: **deterministic, constant** Girsanov kernel. **Market price of risk** $\lambda=(\alpha-r)/\sigma$ ("risk premium per unit risk"), with $h=-\lambda$ (Lemma 12.1).
- **Thm 12.2.** BS model is arbitrage-free (First FT).
- Extended model $dS_t=\alpha_tS_tdt+\sigma_tS_td\bar W_t$, $dB_t=r_tB_tdt$ ($\sigma_t\neq0$, Novikov): kernel $h_t=-({\alpha_t-r_t})/{\sigma_t}$ (12.6). Remark: solvability really requires only $\sigma_t=0\Rightarrow\alpha_t=r_t$ (a locally-riskless stock must earn $r$).

### 12.2 Pricing
Risk-neutral valuation $\Pi(t;X)=e^{-r(T-t)}E^Q[X|\mathcal F_t]$ under $dS=rSdt+\sigma S dW$. The fundamental object is this expectation (valid for **all** claims); the BS **PDE** is only for simple claims $X=\Phi(S_T)$ (Kolmogorov backward equation).

### 12.3 Completeness
- **Thm 12.3.** BS (standard & extended) is complete (Second FT: kernel unique via Girsanov-converse 11.6). But abstract ⇒ self-contained proof via MRT:
- Normalise $Z_0=B/B\equiv1$, $Z_1=S/B$; with $M(t)=E^Q[X/B(T)|\mathcal F_t]$: Q-dynamics $dZ_1=Z_1\sigma dW$, so $dW=dZ_1/(Z_1\sigma)$. MRT gives $dM=g\,dW$ ⇒ set $h_1(t)=g(t)/(\sigma Z_1(t))$, $h_0(t)=M(t)-h_1(t)Z_1(t)$. $\tag{12.13,12.14}$
- **Thm 12.4.** Every $T$-claim with $E^Q[X/B(T)]<\infty$ is replicable (generalises ch8; replicating portfolio abstract via MRT).
- Simple claims: $M(t)=e^{-rT}E^Q[\Phi(S_T)]$; put $M(t)=f(t,S(t))$ solving the backward/BS-form PDE with terminal $f(T,s)=e^{-rT}\Phi(s)$. $g(t)=\sigma S(t)f_s(t,S)$, $h_1(t)=B(t)f_s(t,S)$, $h_0(t)=f(t,S)-S f_s$. Undiscount with $F=e^{rt}f$:
- **Prop 12.5.** Recovering ch8: $h_0(t)=\tfrac{F(t,S)-S F_s(t,S)}{B(t)}$, $h_1(t)=F_s(t,S)$, $V=F(t,S)$, $F$ the BS solution. $\tag{12.15,12.16}$

---

## Ch 13 — Multidimensional Models: Classical Approach (pp. 179–195)

### 13.1 Setup (pp. 179–181)
$n$ risky assets $S=(S_1,\dots,S_n)'$ driven by $n$ **independent** P-Wieners $W=(\bar W_1,\dots,\bar W_n)'$ (exactly $n$: by meta-theorem ≥n for NA, ≥n for completeness ⇒ precisely n).
$$dS_i=\alpha_i S_i dt+S_i\textstyle\sum_j\sigma_{ij}d\bar W_j;\qquad dB=rB\,dt\tag{13.1,13.2}$$
with constant $\alpha_i,\sigma_{ij}$, **volatility matrix $\sigma$ nonsingular**. Row-vector notation $\sigma_i=[\sigma_{i1}\dots\sigma_{in}]$: $dS_i=\alpha_iS_i dt+S_i\,\sigma_i d\bar W$ (13.3). With $D[x]=\operatorname{diag}(x_1,\dots,x_n)$, $\alpha$ the drift column vector:
$$dS(t)=D[S(t)]\,\alpha\,dt+D[S(t)]\,\sigma\,d\bar W(t).\tag{13.6}$$

### 13.2 Pricing — the multidimensional BS PDE (pp. 181–187)
Assume $\Pi(t;X)=F(t,S(t))$ exists; attempt to "beat the risk-free asset" by a self-financing portfolio in $S_1..S_n,B,F$ (n+2 assets → n+1 weight degrees of freedom). Itô on $F$: $dF=F\,\alpha_F dt+F\,\sigma_F d\bar W$ where
$$\alpha_F=\frac1F\Big[F_t+\textstyle\sum_i\alpha_iS_iF_i+\tfrac12\operatorname{tr}\{\sigma'D[S]F_{ss}D[S]\sigma\}\Big],\qquad \sigma_F=\frac1F\textstyle\sum_i S_iF_i\sigma_i,\tag{13.8,13.9}$$
with $F_t=\partial F/\partial t$, $F_i=\partial F/\partial s_i$, $F_{ss}=[\partial^2F/\partial s_i\partial s_j]$. Setting $dV=V\{(r+\beta)dt+0\cdot d\bar W\}$ requires killing $n$ Wiener terms and imposing rate $r+\beta$. The $(n+1)\times(n+1)$ coefficient matrix $H$ (13.10) must be singular (else a synthetic bank at $r+\beta>\;r$ ⇒ arbitrage). Singularity of $H'$ ⇒ its first column is a combination of the others: ∃ real $\lambda_1,\dots,\lambda_n$ (the **market prices of risk**) with
$$\alpha_i-r=\textstyle\sum_j\sigma_{ij}\lambda_j\ (i=1..n),\qquad \alpha_F-r=\textstyle\sum_j\sigma_{Fj}\lambda_j.\tag{13.13,13.14}$$
- The $\lambda$-vector solves $\alpha-r\mathbf 1_n=\sigma\lambda$ ⇒ uniquely $\lambda=\sigma^{-1}[\alpha-r\mathbf 1_n]$ (since σ nonsingular). $\tag{13.15}$
- Substituting σF and αF yields the **multidimensional pricing PDE**:
$$\boxed{\;F_t+\textstyle\sum_{i=1}^n rs_iF_i+\tfrac12\operatorname{tr}\{\sigma'D[s]F_{ss}D[s]\sigma\}-rF=0,\quad F(T,s)=\Phi(s)\;}\tag{Thm 13.1 (13.20)}$$
- **Remark 13.2.1.** $\operatorname{tr}\{\sigma'D[s]F_{ss}D[s]\sigma\}=\sum_{i,j}s_is_jF_{ij}C_{ij}$ with covariance $C_{ij}=[\sigma\sigma']_{ij}$. *(If $\sigma$ is scaled so asset rows $\sigma_i\cdot\sigma_j=\rho_{ij}\sigma_i\sigma_j$, this is $\sum\rho_{ij}\sigma_i\sigma_js_is_jF_{ij}$ — the correlated form.)*
- **Remarks.** Drift $\alpha$ absent (only $\sigma$ matters — same Girsanov reason as scalar). Coefficients may be made time/state dependent ($\alpha(t,S),\sigma(t,S)$, $\sigma$ invertible ∀t,s) — trace term then uses $\sigma(t,s)$.

### 13.3 Risk-neutral valuation (pp. 187–188)
**Thm 13.2.** $F(t,s)=e^{-r(T-t)}E^Q_{t,s}[\Phi(S(T))]$ under $Q$-dynamics $dS_i=rS_i dt+S_i\sigma_i dW^Q$.
**Prop 13.3.** Q characterized equivalently by: (1) risk-neutral valuation property for every price process; (2) every price has short-rate local return under Q (same volatility vector as under P); (3) normalized $\Pi/B$ is a martingale.

### 13.4 Reducing the state space (pp. 188–192)
Assume $\Phi$ **homogeneous of degree 1** ($\Phi(t\cdot s)=t\Phi(s)$) and $\sigma$ constant. Homogeneity gives $\Phi(s_1,\dots,s_n)=s_n\Phi(s_1/s_n,\dots,s_{n-1}/s_n,1)$. Ansatz $F(t,s_1,\dots,s_n)=s_nG(t,s_1/s_n,\dots,s_{n-1}/s_n)$ (13.22) reduces the **n-variable** PDE to an **(n−1)-variable** PDE for $G$:
$$\boxed{\;G_t(t,z)+\tfrac12\textstyle\sum_{i,j=1}^{n-1}z_iz_jG_{ij}(t,z)D_{ij}=0,\qquad G(T,z)=\Psi(z)\;}\tag{Prop 13.4 (13.26,13.28)}$$
with $z_i=s_i/s_n$, $\Psi(z_1,\dots,z_{n-1})=\Phi(z_1,\dots,z_{n-1},1)$, and
$$D_{ij}=C_{ij}+C_{nn}+C_{in}+C_{nj}\quad(C=[\sigma\sigma']).\tag{13.27}$$
Interpretation: it is the zero-rate pricing PDE for claim $Y=\Psi(Z(T))$ where $dZ=D[Z]\tilde\sigma d\tilde W$ with $\tilde\sigma\tilde\sigma'=D$ (drift irrelevant). Constant-σ is needed so $D$ doesn't depend on the full $s$-vector.

**Example 13.5 (exchange option, Margrabe-type).** $S_1,S_2$ with $dS_i=S_i\alpha_i dt+S_i\sigma_i d\bar W_i$ independent. Claim $X=\max[S_1(T)-S_2(T),0]$ homogeneous. Reduce $F(t,s_1,s_2)=s_2G(t,s_1/s_2)$; $G$ solves $G_t+\tfrac12 z^2G_{zz}(\sigma_1^2+\sigma_2^2)=0$, $G(T,z)=\max[z-1,0]$ — a strike-1 European call in a zero-rate world with volatility $\sqrt{\sigma_1^2+\sigma_2^2}$. Hence
$$F(t,s_1,s_2)=s_1N[d_1]-s_2N[d_2],\qquad z=s_1/s_2,$$
$$d_1=\frac{\ln z+\tfrac12(\sigma_1^2+\sigma_2^2)(T-t)}{\sqrt{(\sigma_1^2+\sigma_2^2)(T-t)}},\quad d_2=d_1-\sqrt{(\sigma_1^2+\sigma_2^2)(T-t)}.$$
*(Exercise 13.3: correlation $\rho$ generalises to variance $\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2$; Ex. 13.5 generalizes to homogeneous degree $\beta$.)*

### 13.5 Hedging (pp. 192–194)
- **Thm 13.7 (replication weights, σ invertible).** The market is complete; for $X=\Phi(S(T))$ the replicating relative weights are
$$u_i(t)=\frac{S_i(t)F_i(t,S(t))}{F(t,S(t))}\ (i=1,\dots,n),\qquad u_0(t)=1-\textstyle\sum_iu_i,\tag{13.36}$$
with $F$ the pricing-PDE solution. (Proof: Itô on $V=F$, match (13.34) diffusions, use PDE.) Full completeness for non-simple claims needs the martingale machinery (ch14).

---

## Ch 14 — Multidimensional Models: Martingale Approach ★ (pp. 196–208)

### Setup (pp. 196–197)
$k$-dim P-Wiener $\bar W$; $n$ risky assets $S_1,\dots,S_n$, plus possibly a non-price "state" factor $X$:
$$dS_i=\alpha_i(t)S_i dt+S_i\textstyle\sum_{j=1}^k\sigma_{ij}(t)d\bar W_j,\qquad dB=r(t)Bdt,\tag{14.1,14.2}$$
compact: $dS=D[S]\alpha dt+D[S]\sigma d\bar W$ with $D=\operatorname{diag}$ (14.3). No a-priori equality of $k$ and $n$; $r,\alpha,\sigma$ merely adapted (may be path dependent / hidden-state driven). **$X$ must contain no price process** — price components go in $S$ (Remark 14.0.1); same $\bar W$ drives $S$ and $X$ (WLOG by stacking). Note: filtration may carry extra randomness (e.g. an independent Poisson $N$) — central for completeness below.

### 14.1 No arbitrage (pp. 197–199)
Candidate martingale measure via Girsanov: $dL=L\,\phi'(t)d\bar W$, $L=\mathcal E(\phi\diamond\bar W)$; $d\bar W=\phi dt+dW$ (W Q-Wiener) gives
$$dS=D[S]\{\alpha+\sigma\phi\}dt+D[S]\sigma dW.\tag{14.8}$$
Martingale-measure condition: each asset's local return $=r$, i.e. the **martingale-measure equation**
$$\sigma(t)\phi(t)=r(t)-\alpha(t)\tag{14.10}\quad\Leftrightarrow\quad\alpha+\sigma\phi=r.$$
- **Prop 14.1.** NA requires $r(t)-\alpha(t)\in\operatorname{Im}[\sigma(t)]$ a.s. ∀t (necessary); sufficient if ∃ solution $\phi$ making $\mathcal E(\phi\diamond\bar W)$ a true martingale.
- **Def 14.2.** Girsanov kernel $\phi$ *admissible* if it solves (14.10) and $\mathcal E(\phi\diamond\bar W)$ is a martingale (integrability, cf. Prop 14.10).
- **Def 14.3 / Prop 14.4 (generic NA).** The model is *generically arbitrage-free* (arbitrage-free for every sufficiently-integrable $\alpha$) ⇔ $\sigma(t):\mathbb R^k\to\mathbb R^n$ is **surjective** (rank n), requiring $n\le k$.
- (14.10) involves only $S$, not $X$ — NA constrains only *traded* assets.
- **Prop 14.5.** Under a Q generated by $\phi$: $dS=rD[S]dt+D[S]\sigma dW$ (14.12); factor $X$: $dX=\{\mu_X+\sigma_X\phi\}dt+\sigma_XdW$ (14.13).

### 14.2 Completeness (pp. 199–200)
**Prop 14.6.** Assume generic NA and a **purely Wiener filtration** $\mathcal F_t=\mathcal F_t^{\bar W}$. Then (modulo integrability) the market is complete ⇔ **$k=n$ and $\sigma(t)$ invertible** a.s. ∀t. (*Reason:* with extra sources of randomness — e.g. an independent Poisson $N$ — Girsanov only reshuffles the Wiener part, so even a unique solution of (14.10) leaves $N$-measure changes free ⇒ claims $X=\Phi(N(T))$ unhedgeable. Converse-of-Girsanov 11.6 forces every equivalent change through a Wiener Girsanov kernel, making measure uniqueness ⇔ uniqueness of (14.10) solution ⇔ σ injective $k\le n$; combined with generic NA $n\le k$ gives $k=n$, σ invertible.)

### 14.3 Hedging (pp. 200–202)
Assumption 14.3.1: generic NA ($\operatorname{Im}\sigma=\mathbb R^n$) and $\mathcal F=\mathcal F^{\bar W}$; fix Q. For $X\in L^1(Q)$, $M(t)=E^Q[X/B(T)|\mathcal F_t]$; hedgeable ⇔ $dM=h\,dZ$ (Z=S/B). MRT: $dM=g\,dW$ ($g$ row k-vector); Q-dynamics $dZ=D[Z]\sigma dW$ (14.21) ⇒ need to solve $hD[Z]\sigma=g$, i.e. $\sigma'D[Z]h'=g'$ (14.23). Solvable ⇔ $g'(t)\in\operatorname{Im}[\sigma'(t)]$.
- **Prop 14.7.** Under Assumption 14.3.1 the model is complete ⇔ $\operatorname{Im}[\sigma'(t)]=\mathbb R^k$ (14.24) (i.e. σ injective). Replicating portfolio:
$$h_S(t)=g(t)\sigma^{-1}(t)D^{-1}[Z(t)],\qquad h_0(t)=M(t)-h(t)Z(t).\tag{14.25,14.26}$$
- **Thm 14.8 (Second FT, Wiener-driven, self-contained proof).** Complete ⇔ martingale measure unique, via duality $\{\operatorname{Im}[\sigma']\}^\perp=\operatorname{Ker}[\sigma]$: completeness ⇔ $\operatorname{Ker}\sigma=\{0\}$ ⇔ uniqueness of (14.10). NA and completeness are **adjoint**/dual concepts ((14.10) vs (14.23)).

### 14.4 Pricing (p. 202)
Risk-neutral valuation $\Pi(t;X)=e^{-r(T-t)}E^Q[X|\mathcal F_t]$, $dS=D[S]r\,dt+D[S]\sigma dW^Q$ (14.28,14.29).

### 14.5 Markovian models & PDEs (pp. 203–204)
Return to ch13 Markovian case ($k=n$, constant invertible σ, Wiener filtration): pricing function solves the same PDE (14.31) as Thm 13.1, recovered from Kolmogorov backward equation. Hedging weights from Itô match-up:
$$h_i(t)=\frac{\partial F}{\partial S_i}(t,S(t))\ (i=1,\dots,n),\qquad h_0(t)=\frac1{B(t)}\Big[F(t,S)-\textstyle\sum_i\frac{\partial F}{\partial S_i}S_i\Big],\tag{14.32,14.33}$$
recovering Thm 13.7 in relative weights.

### 14.6 Market prices of risk (pp. 204–205)
Write $\lambda=-\phi$ (λ = market price of risk vector, $\phi$ Girsanov kernel):
$$\alpha(t)-r(t)=\sigma(t)\lambda(t),\qquad \text{componentwise } \alpha_i-r=\textstyle\sum_j\sigma_{ij}\lambda_j.\tag{14.35,14.36}$$
- λ$_j$ = market price of risk for Wiener factor $j$ (aggregate risk aversion to factor $j$); **the same λ prices all assets.** Under NA ∃ λ; **complete** market ⇒ λ (and Q) unique ⇒ unique derivative prices; **incomplete** ⇒ many consistent λ, Q, fixed only by supply/demand.

### 14.7 Stochastic discount factors (pp. 205)
$\Lambda(t)=e^{-\int_0^t r\,ds}L(t)$, $L=\mathcal E(\phi\diamond\bar W)$ ⇒ explicit
$$\Lambda(t)=\exp\Big[\textstyle\int_0^t\phi'(s)d\bar W(s)-\tfrac12\int_0^t(\|\phi\|^2+r)ds\Big]=\exp\Big[-\textstyle\int_0^t\lambda'd\bar W-\tfrac12\int_0^t(\|\lambda\|^2+r)ds\Big].\tag{14.37,14.38}$$

### 14.8 Hansen–Jagannathan bounds (pp. 205–208)
For surjective σ (generic NA), (14.39) has solutions; pick the minimal-Euclidean-norm one.
- **Prop 14.9 (linear algebra).** For surjective $A_{n\times k}$ and $Ax=y$: $A'A$ invertible, unique minimum-norm solution $\hat x=(A'A)^{-1}A'y$. $\tag{14.40}$
- **Prop 14.10.** $\hat\phi=[\sigma'\sigma]^{-1}\sigma'[r-\alpha]$ minimises $\|\phi\|$ among all (14.39)-solutions, i.e. $\|\hat\phi(t)\|\le\|\phi(t)\|$ ∀t; if $\hat\phi$ satisfies Novikov, the model is arbitrage-free. Corresponding minimal market price of risk $\hat\lambda=[\sigma'\sigma]^{-1}\sigma'[\alpha-r]$, $\|\hat\lambda\|\le\|\lambda\|$ for all admissible λ.
- **Prop 14.11 (Hansen–Jagannathan).** For any asset (underlying or derivative) with P-dynamics $d\pi=\pi\alpha_\pi dt+\pi\sigma_\pi d\bar W$ and Sharpe-ratio process $(\alpha_\pi-r)/\sigma_\pi$ (conditional mean excess return per unit total volatility):
$$\Big\|\frac{\alpha_\pi(t)-r(t)}{\sigma_\pi(t)}\Big\|\;\le\;\|\hat\lambda(t)\|\;\le\;\|\lambda(t)\|\qquad\forall\ \text{admissible }\lambda.\tag{14.44}$$
*(Proof: $\sigma_\pi\lambda=\alpha_\pi-r$; Cauchy–Schwarz; holds for λ̂ in particular.)*
- **SDF dynamics & interpretation.** $d\Lambda=-r\Lambda dt+\Lambda\phi'd\bar W=-r\Lambda dt-\Lambda\lambda'd\bar W$ (14.45,14.46) — λ (and φ) is the SDF volatility vector. HJ bounds ⇔ lower bound on SDF volatility for an observed Sharpe ratio, or upper bound on Sharpe ratio for observed SDF volatility. (Exercise 14.2: general admissible λ = λ̂ + μ with μ ⊥ rows of σ.)

---

## Corrections & gaps vs. the existing `derivative_pricing.md` extraction

The pre-existing ch8–14 entries were **qualitatively correct but far too thin** and contained the following issues; the deep-read above corrects/supplements them:

1. **Ch 8 was a stub** (2 bullets) and gave an *inexact* meta-theorem reading. Corrected full statement: arbitrage-free ⇔ $M\le R$; complete ⇔ $M\ge R$; complete+arbitrage-free ⇔ $M=R$ (random source = per-independent-Wiener; for jump/point processes, per distinct jump size). Added the constructive completeness content (Thm 8.5 explicit hedge, Lemma 8.4, Prop 8.6 path-dependent/Asian PDE $+gF_z$, measure-invariance/replication-a.s. argument explaining $\alpha$-independence).
2. **Ch 9 stub.** Added the three parity/static-replication results (linearity Prop 9.1, put–call parity $p=Ke^{-r(T-t)}+c-s$, call-spanning Prop 9.3), the *full call Greek formulas* (Δ,Γ,ρ,Θ,vega with φ(d₁), exact signs), put Δ $=N[d_1]-1$, the delta- and delta+gamma-neutral hedging systems and the two-step triangular solution, and the Greeks-consistency PDE $\Theta+rs\Delta+\tfrac12\sigma^2s^2\Gamma=rP$.
3. **Ch 10 thin / no proofs.** Existing summary was accurate but high-level. Added the structure (S0≡1 case, doubling-strategy Thm 10.1, admissibility, $K_0$), NA ⇒ EMM proof architecture (NFLVR, weak\*, Kreps–Yan), Delbaen–Schachermayer statements (bounded/local/sigma-martingale), numeraire invariance lemma, Jacod theorem, SDF machinery ($\Lambda=e^{-\int r}L$, $d\Lambda=-r\Lambda dt+\frac1B dL$, $\Pi=E^P[\frac{\Lambda(T)}{\Lambda(t)}X]$), and the market-chooses-Q summary.
4. **Ch 11** already accurate (Girsanov $L_t=\exp(\int\phi dW-\tfrac12\int\phi^2)$, $W^P=W^Q+\int\phi$, converse, drift $\mu\to\mu+\sigma\phi$). Confirmed verbatim; added martingale-representation (Thm 11.2), Doléans exponential, Novikov condition (exponent ½ optimal), MLE application.
5. **Ch 12** adequately characterised but thin; added the key numbers $h=-\lambda=-(\alpha-r)/\sigma$ (deterministic/constant), extended-model kernel $h_t=-(\alpha_t-r_t)/\sigma_t$, and the MRT-based completeness construction $h_1=g/(\sigma Z_1)$, $h_0=M-h_1Z_1$ recovering $h_1=F_s$, $h_0=(F-sF_s)/B$.
6. **Ch 13 gap/inexactness.** The extraction's PDE $F_t+\sum rs_iF_i+\tfrac12\sum\rho_{ij}\sigma_i\sigma_j s_is_jF_{ij}-rF=0$ is the **correlated special form**; the book's exact statement is $F_t+\sum rs_iF_i+\tfrac12\operatorname{tr}\{\sigma'D[s]F_{ss}D[s]\sigma\}-rF=0$ with trace $=\sum s_is_jF_{ij}C_{ij}$, $C=[\sigma\sigma']$. Both given; the trace/covariance form is authoritative (and is what survives state-dependent σ). Added state-space reduction (homogeneous Φ, D-matrix (13.27)) and the exchange-option formula $F=s_1N[d_1]-s_2N[d_2]$ with $\sqrt{\sigma_1^2+\sigma_2^2}$, and hedging weights $u_i=s_iF_i/F$ (Thm 13.7) — all previously missing.
7. **Ch 14 gap.** Existing text captured risk premia $\alpha_i-r=\lambda\cdot\sigma_i$ and the SDF/HJ essentials but omitted the completeness criterion and the working mechanisms. Added: martingale-measure equation $\sigma\phi=r-\alpha$ and generically-arbitrage-free ⇔ σ surjective ($n\le k$); completeness ⇔ $k=n$ and σ invertible (Wiener filtration) + the Poisson caveat; hedging equation $\sigma'D[Z]h'=g'$ and $h_S=g\sigma^{-1}D[Z]^{-1}$; minimal-norm $\hat\phi,\hat\lambda$; precise HJ bound $\|\frac{\alpha_\pi-r}{\sigma_\pi}\|\le\|\hat\lambda\|\le\|\lambda\|$; SDF dynamics $d\Lambda=-r\Lambda dt-\Lambda\lambda'd\bar W$.
8. **Chapter coverage/headers.** The pre-existing doc placed ch13 under "Multidimensional Models classical" — retained; no mis-numbering found in headers. The extraction's claim that completeness ⇔ unique EMM for BS (ch8→ch10/12 tie) is correct.

**Outstanding limitations to flag to the atlas:** (i) image-pixel OCR could not be performed (vision backend unreachable for local PNGs) — transcription is from the lossless pdftotext layer, so sub/superscript and fraction layout was reconstructed from context and verified for internal consistency, but a human spot-check of 2–3 visually dense pages (e.g. pp. 133, 189, 201) is advised; (ii) the 3rd-edition TOC maps ch8–14 to printed pp. 115–208 exactly as extracted here (no pagination drift).
