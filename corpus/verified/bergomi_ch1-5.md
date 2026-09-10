# Bergomi — *Stochastic Volatility Modeling* (Chapman & Hall/CRC, 2016) — Verified Deep-Read, Ch. 1–5 (+ Ch. 6–7)

**Source PDF:** `/home/alfred/local-repos/kwant-atlas/corpus/titles/refs/pillar3/Bergomi_2015_stochastic_volatility_modeling.pdf`
(105 MB, 520 pp; pdfTeX; Title "Stochastic Volatility Modeling", Author Lorenzo Bergomi, © 2016 Taylor & Francis, ISBN-13 978-1-4822-4407-6.)
**Rendered pages:** `/tmp/atlas_pages2/bergomi/p-001.png … p-270.png`
**Text layer:** regenerated with `pdftotext -layout … /tmp/atlas_pages2/bergomi.txt` (28 770 lines; the pre-existing `bergomi.txt` did not exist — it was created during this task; **source PDF not modified**).
**Page convention:** book page *n* = PDF page *n + 17* (Chapter 1 opens on PDF p. 18 = book p. 1). Chapter spans (book pp): Ch1 1–24, Ch2 25–102, Ch3 103–132, Ch4 133–150, Ch5 151–200, Ch6 201–216, Ch7 217–300.

**Verification tags used below**
- **[V]** — formula re-read from the rendered page image with vision and confirmed symbol-for-symbol.
- **[T]** — transcribed from the text layer (text layer verified good; layout of displayed equations is column-garbled but content is recoverable and internally cross-checked against Bergomi's own "Chapter's digest" restatements).
- **[R]** — **reconstructed / flagged**: the text layer mangled the layout; the stated form is my reconstruction, re-derived or cross-checked against an independent restatement in the book. Treat as "high confidence but confirm against the page image before relying on a coefficient."

**Scope note.** The assigned range (PDF pp. 1–260 = book pp. 1–243) is actually *Chapters 1–5 plus Chapter 6 and the first half of Chapter 7*. Chapters 1–5 as Bergomi numbers them are: **1** Introduction, **2** Local volatility, **3** Forward-start options, **4** Stochastic volatility – introduction, **5** Variance swaps. The task's parenthetical labels ("Implied volatility; The smile; volatility dynamics; forward variance") describe *topics*, not the printed chapter titles. Because "forward variance curve and its dynamics" is explicitly requested, I extended coverage to **Ch. 6 (Heston in the forward-variance framework)** and **Ch. 7 (Forward variance models)** as far as PDF p. 260. Two items named in the brief live *outside* this range and are noted, not covered: the **Bergomi–Guyon expansion** proper (Ch. 8 "The smile of stochastic volatility models", book pp. 307–355) and the **n-th order volatility-of-volatility** machinery (Ch. 8 §8.2–8.4 onward). Ch. 5 Appendix B gives the first-order (single-cumulant) ancestor of that expansion and is covered.

---

## Chapter 1 — Introduction (book pp. 1–24; PDF pp. 18–41)

**Thesis of the chapter.** A model is not validated by its fidelity to realized price dynamics; it is validated as an *accounting device* (a "pricing equation") that decomposes the P&L of a hedged position into pieces whose sign and size the trader can anticipate. Practitioners do not use the Black–Scholes *model*, but "everybody uses the Black–Scholes *equation*." A model is **usable** ("market model") iff there exist state- and time-dependent break-even levels for the second-order P&L terms that are *payoff-independent*: if the gamma of a portfolio vanishes then so must its theta.

### 1.1 Characterizing a usable model — the Black–Scholes equation

Key concepts: carry P&L; gamma/theta decomposition; break-even variance; break-even covariance matrix; market model; the distinction between *carry* P&L (gamma/theta) and *mark-to-market* P&L.

**Formulas**

- **[T]** Payoff consistency / terminal condition:
$$P(t=T,S) = f(S),\quad \forall S \tag{1.1}$$
- **[T]** Daily P&L of a short delta-hedged option (two pieces: theta, gamma):
$$\mathrm{P\&L} = -\Big[\frac{dP}{dt} - rP + (r-q)S\frac{dP}{dS}\Big]\delta t \;-\; \frac{1}{2}S^2\frac{d^2P}{dS^2}\Big(\frac{\delta S}{S}\Big)^2 \tag{1.2}$$
- **[T]** Compact form with $A=\frac{dP}{dt}-rP+(r-q)S\frac{dP}{dS}$, $B=\frac12 S^2\frac{d^2P}{dS^2}$:
$$\mathrm{P\&L} = -A(t,S)\,\delta t - B(t,S)\Big(\frac{\delta S}{S}\Big)^2 \tag{1.3}$$
Usability requires $\mathrm{sign}(A)\ne \mathrm{sign}(B)\ \forall t,S$. Money is neither made nor lost for $\frac{\delta S}{S}=\pm\sqrt{-A/B}\,\sqrt{\delta t}$.
- **[T]** Break-even condition $A=-\hat\sigma^2 B$ gives the **Black–Scholes equation**:
$$\frac{dP_{\hat\sigma}}{dt} - rP_{\hat\sigma} + (r-q)S\frac{dP_{\hat\sigma}}{dS} = -\frac{\hat\sigma^2}{2}S^2\frac{d^2P_{\hat\sigma}}{dS^2}
\quad\Longleftrightarrow\quad
\frac{dP}{dt} + (r-q)S\frac{dP}{dS} + \frac{\hat\sigma^2}{2}S^2\frac{d^2P}{dS^2} = rP \tag{1.4}$$
- **[T]** Canonical carry P&L in terms of realized vs break-even quadratic variation:
$$\mathrm{P\&L} = -\frac{S^2}{2}\frac{d^2P_{\hat\sigma}}{dS^2}\Big(\frac{\delta S^2}{S^2} - \hat\sigma^2\delta t\Big) \tag{1.5}$$
- **[T]** Multi-asset P&L: $\mathrm{P\&L} = -A\,\delta t - \tfrac12\sum_{ij}\varphi_{ij}\frac{\delta S_i\delta S_j}{S_iS_j}$ with $\varphi_{ij}=S_iS_j\frac{d^2P}{dS_idS_j}$ (1.6). Diagonalising $\varphi=T\,\phi\,T^{\!\top}$ turns it into a sum of independent one-asset P&Ls in the "basket" coordinates $\delta z_k = T_k^{\!\top}U$.
- **[T]** Existence of positive break-even weights $\omega_k>0$ with $A=-\tfrac12\sum_k\varphi_k\omega_k$ (1.7) yields the **break-even covariance** form
$$\mathrm{P\&L} = -\frac12\sum_{ij}\varphi_{ij}\Big(\frac{\delta S_i\delta S_j}{S_iS_j} - C_{ij}\,\delta t\Big),\qquad C=T\,\omega\,T^{\!\top}>0 \tag{1.8}$$
$C$ is any positive matrix, and is interpreted as an *implied* covariance matrix of break-even levels.

### 1.2 How (in)effective is delta hedging?

Key concepts: realized vs implied volatility; variance-of-variance $\Omega$; kurtosis $\kappa$; the variance/variance autocorrelation function $f(\tau)$; why daily-hedged P&L dispersion is dominated by vol-of-vol, not by fat tails.

**Formulas**

- **[T]** Total discounted P&L over the option's life (daily rehedges $t_i$):
$$\mathrm{P\&L} = -\sum_i e^{-rt_i}\frac{S_i^2}{2}\frac{d^2P_{\hat\sigma}}{dS^2}(t_i,S_i)\big(r_i^2-\hat\sigma^2\delta t\big),\qquad r_i=\frac{S_{i+1}-S_i}{S_i} \tag{1.9}$$
- **[T]** Return decomposition $r_i=\sigma_i\sqrt{\delta t}\,z_i$, $\langle z_i\rangle=0,\ \langle z_i^2\rangle=1$, $z_i$ iid and independent of $\sigma_i$ (1.10).
- **[R]** Variance of the aggregated P&L. Let $\Omega=\dfrac{\langle\sigma^4\rangle-\hat\sigma^4}{\hat\sigma^4}$ (dimensionless "variance of daily variances") and $\kappa$ the excess kurtosis. Then
$$\mathrm{Var}\Big[\sum_i(\sigma_i^2z_i^2-\hat\sigma^2)\delta t\Big]=\hat\sigma^4\Big[(2+\kappa)\sum_i\delta t^2+\Omega\sum_{i\ne j}f_{ij}\,\delta t^2\Big] \tag{1.11}$$
with $f_{ij}=\dfrac{(\sigma_i^2-\hat\sigma^2)(\sigma_j^2-\hat\sigma^2)}{\sqrt{\langle\sigma_i^4\rangle-\hat\sigma^4}\sqrt{\langle\sigma_j^4\rangle-\hat\sigma^4}}$. *(Layout-garbled in the text layer; reconstructed and confirmed by matching eq. (1.15)'s stated coefficients — see verification notes.)*
- **[T]** **Vega/gamma relationship** in Black–Scholes (derived in Ch. 5 App. A, eq. 5.66):
$$\frac{dP_{\hat\sigma}}{d\hat\sigma} = S^2\frac{d^2P_{\hat\sigma}}{dS^2}\,\hat\sigma T \tag{1.12}$$
- **[R]** Standard deviation of final P&L in units of vega:
$$\mathrm{StDev(P\&L)} = \hat\sigma\,\frac{dP_{\hat\sigma}}{d\hat\sigma}\,\frac{1}{2T}\sqrt{(2+\kappa)\sum_i\delta t^2 + \Omega\sum_{i\ne j}f_{ij}\,\delta t^2} \tag{1.13}$$
- **[T]** Black–Scholes case ($\Omega=0,\kappa=0$, $N$ rehedges, $N\delta t=T$):
$$\mathrm{StDev(P\&L)} = \frac{1}{\sqrt{2N}}\,\hat\sigma\,\frac{dP_{\hat\sigma}}{d\hat\sigma} \tag{1.14}$$
i.e. the P&L dispersion equals the option's vega times the standard deviation of the historical-volatility estimator on the same rehedge schedule. For a 1y ATM call, $\hat\sigma=20\%$, $P=7.97\%$: $\mathrm{StDev}\simeq 4.5\%$ of the option price.
- **[R]** Real case (convert sums to integrals; $\Omega$ = dispersion of daily variances, $f$ their autocorrelation):
$$\mathrm{StDev(P\&L)} = \hat\sigma\frac{dP_{\hat\sigma}}{d\hat\sigma}\sqrt{\frac{2+\kappa}{4N}+\frac{\Omega}{2T^2}\int_0^T(T-\tau)f(\tau)\,d\tau} \tag{1.15}$$
*(reconstructed from garbled layout; coefficients confirmed to reduce to (1.14) when $\Omega=\kappa=0$, and to (1.16) when $f(\tau)=\rho e^{-k\tau}$.)*
- **[T]** With exponential fit $f(\tau)=\rho e^{-k\tau}$ (empirically $\rho=0.78$, $1/k=45$ days for financial stocks):
$$\frac{\mathrm{StDev(P\&L)}}{\hat\sigma\,dP_{\hat\sigma}/d\hat\sigma} \simeq \sqrt{\frac{2+\kappa}{4N}+\frac{\rho\Omega}{2}\frac{kT-1+e^{-kT}}{(kT)^2}} \tag{1.16}$$
Typical empirical values: $\Omega\in[1.5,4]$ (use 2), $\kappa\simeq 5$.

**Practical notes.** For 1y ATM, BS gives 4.5%-of-price StDev; reality gives **~35% of the option price** (2.8% absolute) — "one third of the premium." Except for very short maturities the dispersion is generated by *volatility/volatility correlation*, not return tails. Conclusion: **delta hedging alone is insufficient; options must be hedged with options.**

### 1.3 On the way to stochastic volatility

Key concepts: gamma-hedging with a vanilla split into *carry* (gamma/theta) vs *mark-to-market* (vega/vanna) P&L; why using options as hedges trades *realized-vol* exposure for *implied-vol dynamics* exposure; the vanna–volga method; forward-smile / skew-dependent exotic risk.

**Formulas / techniques**

- **[T]** Gamma-hedge ratio: $\lambda=\dfrac{d^2P/dS^2}{d^2O/dS^2}$ (1.18). Gamma profiles are not homothetic ⇒ hedge is only locally valid.
- **[T]** Hedged-position P&L at second order in $\delta S,\delta\hat\sigma_O$: vega/vanna terms appear with **no offsetting theta** (1.19–1.20). This is the central defect: "while in the Black–Scholes pricing equation we had a parameter (the implied volatility) to control how the gamma and theta terms for the spot offset each other, we have no equivalent parameter … for gammas on $\hat\sigma_O$."
- **[T]** Vanna–volga market-adjusted price (footnote 13): $P^{\mathrm{Mkt}}=P^{BS}(\hat\sigma_0)+\sum_i\lambda_i[O_i^{BS}(\hat\sigma_i)-O_i^{BS}(\hat\sigma_0)]$ (1.21), and its second-derivative (vanna–volga) representation (1.22). Historical use: interpolating implied vols; **no guarantee of arbitrage-free interpolation**.
- **[T]** **Barrier option (Example 1).** Carr–Chou static replication in BS: for $S<L$, $g(S)=f(S)$; for $S>L$,
$$g(S)=-\Big(\frac{L}{S}\Big)^{\frac{2r}{\sigma^2}-1}f\!\Big(\frac{L^2}{S}\Big) \tag{1.23a,b}$$
With $r=0$: $g(S)=1$ for $S<L$, $g(S)=-\tfrac{S}{L}$ for $S>L$ — two digitals struck at $L$, minus one ZCB, minus $\tfrac1L$ calls struck at $L$. Double digital value $D=2\big[D^{BS}_L(\hat\sigma_L)+\frac{dP^{BS}_L}{d\hat\sigma}\frac{d\hat\sigma_K}{dK}\big|_L\big]-1$ (1.24): **barrier price is dominated by the ATMF skew prevailing when the spot hits the barrier** ($\sim 8\%$ correction for an equity index — not small).
- **[T]** **Forward-start / cliquet (Example 2).** Payoff $(S_{T_2}/S_{T_1}-k)^+$ (1.25). For $k=1$ (ATMF), zero rates,
$$P\simeq\frac{1}{\sqrt{2\pi}}\,\hat\sigma\,\sqrt{T_2-T_1} \tag{1.26}$$
$P$ is independent of $S$ — the cliquet's real underlying is the **forward implied volatility** for maturity $T_2$ observed at $T_1$.

**Chapter digest (verbatim content).** Delta hedging removes order-one $\delta S$; a break-even condition at order two in $\delta S$ ⇒ a parabolic pricing equation with a probabilistic (diffusion) interpretation — "*the argument goes this way and not the other way around*." With multiple hedges, usability ⇔ existence of a break-even covariance matrix. Delta hedging alone leaves too much P&L dispersion; vol-of-vol correlation dominates. Using options for gamma-hedging immunises against realized volatility but exposes you to implied-volatility dynamics — hence SV models model *implied* vol dynamics, not realized vol.

---

## Chapter 2 — Local volatility (book pp. 25–102; PDF pp. 42–119)

**Thesis.** Local volatility (LV) is the simplest **market model**: exactly calibratable to *any* arbitrage-free smile; it treats vanilla option prices as initial values of hedge instruments, on the same footing as $S$. Its cost: **one-factor** — implied vols are 100% correlated with each other and with $S$, and their volatilities/break-even levels are entirely dictated by the smile used for calibration. It has a Markov representation in $(t,S)$. The local-vol function $\sigma(t,S)$ "has no physical significance" — it is a by-product of that representation; the model is *meant* to be recalibrated daily, and that recalibration is legitimate.

### 2.1–2.2 SDE, Dupire formula, no-arbitrage

- **[V]** LV SDE:
$$dS_t = (r-q)S_t\,dt + \sigma(t,S_t)\,S_t\,dW_t \tag{2.1}$$
- **[T]** Pricing PDE (same as (1.4) with $\sigma(t,S)$):
$$\frac{dP}{dt} + (r-q)S\frac{dP}{dS} + \frac{\sigma(t,S)^2}{2}S^2\frac{d^2P}{dS^2} = rP \tag{2.2}$$
- **[V]** **Dupire formula** ($C(K,T)$ = market call price):
$$\boxed{\;\sigma(t,S)^2 = 2\,\frac{\dfrac{dC}{dT} + qC + (r-q)K\dfrac{dC}{dK}}{K^2\dfrac{d^2C}{dK^2}}\;\Bigg|_{\substack{K=S\\T=t}}\;} \tag{2.3}$$
> **[V]** Vision read of p. 43 confirmed the structure and the leading factor 2 with denominator $K^2\,d^2C/dK^2$; the small term $qC$ at the line break is present in the text layer and in the Ch. 2 digest restatement (PDF p. 113). Use the form above.
- **[T]** **Dupire equation** (general, diffusive $\sigma_t$, no LV assumption):
$$\mathbb{E}[\sigma_T^2\,|\,S_T=K] = 2\,\frac{\dfrac{dC}{dT} + qC + (r-q)K\dfrac{dC}{dK}}{K^2\dfrac{d^2C}{dK^2}} \tag{2.6}$$
Consequence (**Gyöngy**): two diffusive processes produce the same vanilla smile iff $\mathbb{E}[\sigma_T^2|S_T=K]$ coincide; the effective local vol is $\sigma^2(t,S)=\mathbb{E}[\sigma_t^2|S_t=S]$.
- **[T]** **Forward equation** (with $\sigma(t=T,S=K)$; IC $C(K,0)=(S_0-K)^+$):
$$\frac{dC}{dT} + (r-q)K\frac{dC}{dK} - \frac{\sigma^2(T,K)}{2}K^2\frac{d^2C}{dK^2} = -qC \tag{2.7}$$
- **[T]** Density link: $\dfrac{d^2C(K,T)}{dK^2}=e^{-rT}\mathbb{E}[\delta(S_T-K)] = e^{-rT}\rho_{KT}$ (2.8).
- **[T]** **No-arbitrage conditions.** *Strike arbitrage* ⇔ $d^2C/dK^2<0$ (butterfly spread). *Maturity arbitrage* ⇔ violation of the **convex-order condition**
$$e^{qT_1}C(kF_{T_1},T_1)\le e^{qT_2}C(kF_{T_2},T_2),\ \ T_1\le T_2 \tag{2.9}$$
- **[T]** Convex-order for implied vols: with $f(k,\tau)=\mathbb{E}[(U_\tau-k)^+], U_\tau=e^{-\tau/2+W_\tau}, \tau(T)=\hat\sigma_{kT}^2T$,
$$\tau_1\le\tau_2 \iff f(k,\tau_1)\le f(k,\tau_2) \;\Longleftrightarrow\; T_1\hat\sigma_{kT_1}^2\le T_2\hat\sigma_{kT_2}^2 \tag{2.14}$$
i.e. **total implied variance $T\hat\sigma_{kF_T,T}^2$ is increasing in $T$ at fixed moneyness $k$** (2.15).
- **[T]** General convex payoffs $f(S_T)=h(S_T/F_T)$, $h$ convex: unique BS implied vol; and
$$T_2\hat\sigma_{T_2}^2\ge T_1\hat\sigma_{T_1}^2 \tag{2.17}$$
- **Practical note.** "Steep short-maturity equity skews are *no evidence* that jumps are needed" — LV will reproduce any non-arbitrageable smile.

### 2.3 From implied vols to local vols

- **[V]** **Dupire in implied-vol coordinates** ($y=\ln(K/F_t)$, $f(t,y)=(t-t_0)\hat\sigma_{Kt}^2$, $F_t=S_0e^{(r-q)(t-t_0)}$):
$$y=\ln\!\frac{K}{F_t} \tag{2.18a},\qquad f(t,y)=(t-t_0)\,\hat\sigma_{Kt}^2 \tag{2.18b}$$
$$\sigma^2(t,S) = \frac{\dfrac{df}{dt}}{\Big(\dfrac{y}{2f}\dfrac{df}{dy}-1\Big)^2 + \dfrac12\dfrac{d^2f}{dy^2} - \dfrac14\Big(\dfrac14+\dfrac1f\Big)\Big(\dfrac{df}{dy}\Big)^2}\;\Bigg|_{y=\ln(S/F_t)} \tag{2.19}$$
> **[V]** Page 34 (PDF p. 50) vision read confirmed the denominator terms $\big(\tfrac{y}{2f}f_y-1\big)^2$, $+\tfrac12 f_{yy}$, $-\tfrac14(\tfrac14+\tfrac1f)f_y^2$ (the OCR rendered "$1/f$" ambiguously as "$1/y$"; $1/f$ is correct and dimensionally consistent). The form expands exactly to the standard Gatheral expression $1-\tfrac{y}{f}f_y+\big(\tfrac{y^2}{4f^2}-\tfrac1{16}-\tfrac1{4f}\big)f_y^2+\tfrac12 f_{yy}$ — **verified**.
- **[T]** **Interpolation rules.** In $(y,t)$ coordinates the convex-order condition is simply $f_{i+1}(y)\ge f_i(y)$ ("$f$ profiles must not cross"). Affine interpolation in $t$:
$$f(t,y)=\frac{T_{i+1}-t}{T_{i+1}-T_i}f_i(y)+\frac{t-T_i}{T_{i+1}-T_i}f_{i+1}(y) \tag{2.20}$$
ensures (a) convex-order on $[T_i,T_{i+1}]$, (b) LV for $t\in[T_i,T_{i+1}]$ depends *only* on smiles at $T_i,T_{i+1}$. Extrapolation: affine $f_i(y)=a_iy+b_i$ with $|a_i|\le2$ needed for denominator positivity at large $y$. (SVI cited as an arbitrage-free parametric surface.)
- **[T]** **Dividends — exact solution.** Map $S_t=\alpha(t)X_t-\delta(t)$ with
$$\alpha(t)=e^{(r-q)t}\!\!\prod_{t_i<t}\!(1-y_i),\quad \delta(t)=\!\!\sum_{t_i<t}\!c_ie^{(r-q)(t-t_i)}\!\!\prod_{t_i<t_j<t}\!(1-y_j) \tag{2.21}$$
$X$ driftless, no dividend jumps; then
$$\sigma(t,S)=\frac{S+\delta(t)}{S}\,\sigma_X(t,X(S,t)) \tag{2.22}$$
- **[T]** **Dividends — approximate solution** (yields a usable $y$-definition). Matching condition across a dividend $(1-z,c)$ at $\tau$:
$$\hat\sigma_{K\tau^-}=\hat\sigma_{(1-z)K-c,\;\tau^+} \tag{2.23}$$
Bos–Vandermark effective-dividend functions
$$\alpha(T)=\prod_{t_i<T}(1-y_i),\quad \delta S(T)=\sum_{t_i<T}\frac{T-t_i}{T}c_i^*e^{-(r-q)t_i},\quad \delta K(T)=\sum_{t_i<T}\frac{t_i}{T}c_i^*e^{(r-q)(T-t_i)} \tag{2.24}$$
with $c_i^*=c_i\prod_{t_i<t_j<T}(1-y_j)$. Amend
$$y=\ln\!\frac{K+\delta K(t)}{\alpha(t)S_0-\delta S(t)}-(r-q)(t-t_0),\qquad f(t,y)=(t-t_0)\hat\sigma_{Kt}^2 \tag{2.26}$$
Then $f$ is continuous across dividend dates and (2.23) holds exactly. **Recipe:** smooth interpolation of $f$ in $(t,y)$ with this $y$; feed into (2.19). Exactly recovers $\sigma(t,S)=\sigma_0$ from a flat surface.

### 2.4 From local vols to implied vols

Key concepts: implied variance as a *gamma-weighted* average of local variance; the order-one expansion; skew/curvature of the smile; the ATMF skew; the Berestycki–Busca–Florent harmonic average at $T\to0$.

- **[T]** Fundamental identity (models I, II; delta-hedge in model I, realize model II):
$$P_2(0,S_0,\bullet)=P_1(0,S_0)+\mathbb{E}_2\!\Big[\int_0^T e^{-rt}\frac{S_t^2}{2}\frac{d^2P_1}{dS^2}\big(\sigma_{2t}^2-\sigma_1(t,S_t)^2\big)dt\Big] \tag{2.30}$$
- **[T]** Hence **implied variance = dollar-gamma-weighted average of local variance**:
$$\hat\sigma_{KT}^2 = \frac{\mathbb{E}_{\sigma(t,S)}\big[\int_0^T e^{-rt}S_t^2\frac{d^2P_{\hat\sigma_{KT}}}{dS^2}\,\sigma^2(t,S)\,dt\big]}{\mathbb{E}_{\sigma(t,S)}\big[\int_0^T e^{-rt}S_t^2\frac{d^2P_{\hat\sigma_{KT}}}{dS^2}\,dt\big]} \tag{2.32}$$
and the dual version (2.33). *(First shown by Dupire, late '90s.)*
- **[T]** Order-one expansion around a deterministic vol $\sigma_0(t)$, with $u=\sigma^2=u_0+\delta u$, $\omega_t=\int_0^t\sigma_0^2(u)du$:
$$\delta(\hat\sigma_{KT}^2)=\frac{\mathbb{E}_{\sigma_0}\big[\int_0^T e^{-rt}\,\delta u(t,S)\,S^2\frac{d^2P_{\sigma_0}}{dS^2}dt\big]}{\mathbb{E}_{\sigma_0}\big[\int_0^T e^{-rt}S^2\frac{d^2P_{\sigma_0}}{dS^2}dt\big]} \tag{2.35}$$
using $\mathbb{E}_{\sigma_0}[e^{-rt}S^2 d^2P_{\sigma_0}/dS^2]=S_0^2\,d^2P_{\sigma_0}/dS^2|_{t=0,S_0}$ (dollar gamma is a martingale, (2.36)).
- **[T]** Exact order-one formula:
$$\hat\sigma_{KT}^2 = \frac{1}{T}\int_0^T\!\!dt\!\int_{-\infty}^{+\infty}\!\!\frac{dy}{\sqrt{2\pi}}e^{-y^2/2}\;u\!\Big(t,\;F_te^{\frac{\omega_t}{\omega_T}x_K+\frac{\sqrt{(\omega_T-\omega_t)\omega_t}}{\omega_T}y}\Big) \tag{2.40}$$
with $x_K=\ln(K/F_T)$, $F_t=S_0e^{(r-q)t}$; exact when $u$ depends on $t$ only.
- **[T]** Around a **constant** $\sigma_0$ (used thereafter for simplicity):
$$\hat\sigma_{KT}=\frac1T\int_0^T\!\!dt\!\int_{-\infty}^{+\infty}\!\!\frac{dy}{\sqrt{2\pi}}e^{-y^2/2}\;\sigma\!\Big(t,\;F_te^{\frac{t}{T}x_K+\sigma_0\sqrt{\frac{(T-t)t}{T}}\,y}\Big) \tag{2.42}$$
Crude "most-likely-path" version: $\hat\sigma_{KT}\simeq\frac1T\int_0^T\sigma\big(t,F_te^{(t/T)\ln(K/F_T)}\big)dt$ (2.43). **Accuracy caveat:** (2.42) is *not* accurate enough for equity trading; the density's dependence on $\sigma(t,S)$ is essential. For realistic equity smiles there is no cheap alternative to solving the forward equation (2.7) numerically. (2.42) is useful for the **skew** (a difference of vols), not for absolute levels.
- **[T]** Local-vol param. $\sigma(t,S)=\sigma(t)+\alpha(t)x+\tfrac{\beta(t)}2x^2$, $x=\ln(S/F_t)$ (2.44). Then
$$\hat\sigma_{KT}=\frac1T\int_0^T\sigma(t)dt+\frac{\sigma_0^2T}{2}\frac1T\int_0^T\frac{(T-t)t}{T^2}\beta(t)dt+\Big(\frac1T\int_0^T\frac{t}{T}\alpha(t)dt\Big)x_K+\frac12\Big(\frac1T\int_0^T\frac{t^2}{T^2}\beta(t)dt\Big)x_K^2 \tag{2.47}$$
- **[T]** **ATMF skew and curvature** (order one in $\alpha,\beta$):
$$\mathcal S_T\;\equiv\;\frac{d\hat\sigma_{KT}}{d\ln K}\Big|_{\text{ATMF}}=\frac1T\int_0^T\frac{t}{T}\,\alpha(t)\,dt \tag{2.48}$$
$$\frac{d^2\hat\sigma_{KT}}{d\ln K^2}\Big|_{\text{ATMF}}=\frac1T\int_0^T\Big(\frac{t}{T}\Big)^2\beta(t)\,dt \tag{2.49}$$
- **[T]** Constant $\alpha,\beta$: $\mathcal S_T=\alpha/2$ (2.50a), curvature $=\beta/3$ (2.50b) — **implied skew is half the local skew; implied curvature one third of local curvature.**
- **[T]** Power-law local skew $\alpha(t)=\alpha_0(t/\tau_0)^\gamma$ for $t>\tau_0$ (2.51):
$$\mathcal S_T=\begin{cases}\alpha_0/2,&T\le\tau_0\\[2pt]\dfrac{1}{2-\gamma}\alpha_0\Big(\dfrac{\tau_0}{T}\Big)^\gamma-\dfrac{1}{2(2-\gamma)}\alpha_0\Big(\dfrac{\tau_0}{T}\Big)^2,&T\ge\tau_0\end{cases} \tag{2.52}$$
Long maturity: $\mathcal S_T\simeq\frac1{2-\gamma}\alpha_0(\tau_0/T)^\gamma$ (2.53) — **implied skew decays with the same exponent $\gamma$ as the local skew**, rescaled by $1/(2-\gamma)$. Equity: $\gamma\approx\tfrac12$.
- **[T]** **Exact short-maturity result** (Berestycki–Busca–Florent): the *inverse* of implied vol is the average of the inverse of local vol:
$$\frac{1}{\hat\sigma(T{=}0,Se^y)}=\frac1y\int_0^y\frac{du}{\sigma(T{=}0,Se^u)}\quad\Longleftrightarrow\quad \frac{1}{\hat\sigma(T{=}0,K)}=\frac{1}{\ln(K/S)}\int_S^K\frac{1}{\sigma(T{=}0,S)}\frac{dS}{S} \tag{2.54}$$
Harmonic, not quadratic, average — because there is no temporal averaging as $T\to0$.

### 2.5 The dynamics of the local volatility model

Key concepts: **Skew Stickiness Ratio (SSR)** $R_T$; the $R=2$ rule; vol-of-vol determined by the ATMF skew.

- **[T]** ATMF-vol response to spot (order one in $\alpha$):
$$\frac{d\hat\sigma_{KT}}{d\ln K}\Big|_{K=F_T}=\frac1T\int_0^T\frac{t}{T}\alpha(t)dt \tag{2.59a},\quad \frac{d\hat\sigma_{KT}}{d\ln S_0}\Big|_{K=F_T}=\frac1T\int_0^T\Big(1-\frac tT\Big)\alpha(t)dt \tag{2.59b}$$
$$\frac{d\hat\sigma_{F_TT}}{d\ln S_0}=\frac1T\int_0^T\alpha(t)dt=\mathcal S_T+\frac1T\int_0^T\mathcal S_t\,dt \tag{2.59c}$$
Using $\alpha(t)=\frac{d}{dt}(t\mathcal S_t)+\mathcal S_t$ (2.56): $\dfrac{d\hat\sigma_{F_TT}}{d\ln S_0}=\mathcal S_T+\frac1T\int_0^T\mathcal S_t\,dt$ (2.57). With constant $\mathcal S$: **$\dfrac{d\hat\sigma_{F_TT}}{d\ln S_0}=2\mathcal S_T$** (2.58). Around a time-dependent $\bar\sigma(t)$: (2.60a–c).
- **[T]** **SSR** definition and general (regression) form:
$$R_T=\frac{1}{\mathcal S_T}\frac{d\hat\sigma_{F_TT}}{d\ln S_0} \tag{2.61},\qquad R_T=\frac{1}{\mathcal S_T}\frac{\big\langle d\hat\sigma_{F_TT}\,d\ln S_0\big\rangle}{\big\langle (d\ln S_0)^2\big\rangle} \tag{2.62}$$
$R_T=1$: **sticky-strike** (fixed-strike vols frozen, ATMF slides along the smile). $R_T=0$: **sticky-delta** (smile translates with spot; fixed log-moneyness vols frozen). Sticky-delta holds for all $T$ in models with iid increments of $\ln S$ (e.g. jump-diffusion); sticky-strike only as a long-maturity limit of some SV models.
- **[V]** LV approximation:
$$\boxed{\;R_T = 1+\frac1T\int_0^T\frac{\mathcal S_t}{\mathcal S_T}\,dt\;} \tag{2.64}$$
> **[V]** Confirmed on p. 52 (PDF p. 69): integral $0\to T$, integrand $\mathcal S_t/\mathcal S_T$ (calligraphic $\mathcal R,\mathcal S$ in the book). Slight overestimate for strong skews.
- **[T]** Around time-dependent $\bar\sigma(t)$: $R_T=1+\frac1T\int_0^T\frac{\bar\sigma_t^2}{\bar\sigma_t\bar\sigma_T}\frac{\mathcal S_t}{\mathcal S_T}dt$ (2.65).
- **[T]** **$R=2$ rule**: if $\mathcal S$ (or $\alpha$) is maturity-independent, $R_T=2\ \forall T$ (2.66); and $\lim_{T\to0}R_T=2$ (2.68) for any (smooth) LV.
- **[T]** **The $R=2$ rule is exact** for time-independent LV $\sigma(t,S)\equiv\sigma(S/F_t)$ (2.69). Proof via the **backward/forward symmetry**
$$\hat\sigma_{S\frac{F_t}{F_T},\,T}\Big(\frac{F_t}{F_T}K\Big)=\hat\sigma_{KT}(S),\qquad\text{zero rates: }\hat\sigma_{ST}(K)=\hat\sigma_{KT}(S) \tag{2.78}$$
which gives $\frac{d\hat\sigma_{KT}}{d\ln K}=\frac{d\hat\sigma_{KT}}{d\ln S_0}$ (2.79) hence $R_T=2$ exactly. $\lim_{T\to0}R_T=2$ exact for *any* LV (via (2.54)).
- **[T]** Power-law-decaying skew: with $\mathcal S_T\propto T^{-\gamma}$, $R_T\to\frac{2-\gamma}{1-\gamma}$ for large $T$ (2.80–2.81) — $\gamma=\tfrac12\Rightarrow R_\infty=3$. $\gamma=1\Rightarrow R_\infty=\infty$, in fact $R_T\propto\ln T$.
- **[T]** **Volatilities of volatilities** in LV. Since $\hat\sigma_{F_TT}=R_T\mathcal S_T\,d\ln S_t+\bullet\,dt$ (2.82) and $d\langle\ln S^2\rangle=\hat\sigma_{F_00}^2dt$:
$$\mathrm{vol}(\hat\sigma_{F_TT})=R_T\,\mathcal S_T\,\frac{\hat\sigma_{F_00}}{\hat\sigma_{F_TT}}=\Big(\mathcal S_T+\frac1T\int_0^T\mathcal S_t\,dt\Big)\frac{\hat\sigma_{F_00}}{\hat\sigma_{F_TT}}\quad(2.83);\qquad \lim_{T\to0}\mathrm{vol}(\hat\sigma_{F_TT})=2\mathcal S_T \tag{2.85}$$
Long maturities: $\mathrm{vol}(\hat\sigma_{F_TT})\to\frac{2-\gamma}{1-\gamma}\mathcal S_T$ (2.86).
- **[T]** SSR↔covariance identity (order one in $\alpha$; more generally Ch. 8 §8.4):
$$\mathcal S_T=\frac{1}{\hat\sigma_T^2T}\int_0^T\frac{T-t}{T}\,\big\langle d\ln S_t\;d\hat\sigma_T(t)\big\rangle\,dt \tag{2.89}$$
i.e. the ATMF skew = $\frac{T-t}{T}$-weighted integral of the instantaneous spot/ATMF-vol covariance over $[0,T]$. **Consequence:** LV generates *larger* SSRs and *weaker* future skews than time-homogeneous SV models calibrated to the same smile.

**Practical notes (empirical, Euro Stoxx 50).** (2.64) reproduces the actual LV SSR to ~5% except at the long end of a strong smile. May 16 2013 / Oct 4 2010 fits: $\tau_0=0.12,\gamma=0.52$ / $\tau_0=0.15,\gamma=0.37$, giving $R_\infty=3.1/2.6$. A strong SSR can merely reflect a weak/vanishing skew, not large vol-of-vol.

### 2.6 Future skews and volatilities of volatilities

- **[T]** LV future ATMF skew (forward date $\tau$, residual maturity $\theta$):
$$\mathcal S_\theta(\tau)=\frac1\theta\int_\tau^{\tau+\theta}\frac{t-\tau}{\theta}\alpha(t)\,dt \tag{2.90}$$
- **[T]** In terms of today's skew term-structure:
$$\mathcal S_\theta(\tau)=\mathcal S_{\tau+\theta}-\frac{\tau}{\theta}\Big(\frac1\theta\int_\tau^{\tau+\theta}\mathcal S_t\,dt-\mathcal S_{\tau+\theta}\Big) \tag{2.91}$$
For decreasing term structure: $|\mathcal S_\theta(\tau)|\le|\mathcal S_{\tau+\theta}|\ll|\mathcal S_\theta|$ — **future skews are systematically weaker.** Power-law short-$\theta$ limit:
$$\mathcal S_\theta(\tau)\propto\Big(\frac{\theta}{\tau}\Big)^\gamma\mathcal S_\theta \tag{2.92}$$

**Practical note.** LV future skews and future vol-of-vols are *not lockable*; they change with recalibration ⇒ large unpredictable carry P&L when residual gammas/cross-gammas are sizeable. This is the central indictment of LV for forward-smile products.

### 2.7 Delta and carry P&L

Key concepts: the "LV delta" $\Delta^{LV}=dP^{LV}/dS|_{\sigma\ \text{fixed}}$ is **meaningless**; the real delta is the **market-model delta** $\Delta^{MM}=dP/dS|_{O_{KT}\ \text{fixed}}$ (2.108); the **sticky-strike delta** $\Delta^{SS}=dP/dS|_{\hat\sigma_{KT}\ \text{fixed}}$ (2.98) is what a desk trades if it hedges vanillas by their BS deltas: $\Delta^{MM}+\frac{dP}{dO_{KT}}\!\bullet\!\frac{dO^{BS}_{KT}}{dS}=\Delta^{SS}$, i.e. $\Delta^{SS}-\frac{dP}{dO_{KT}}\!\bullet\!\frac{dP^{BS}_{KT}}{dS}=\Delta^{MM}$.

- **[T]** Carry P&L in implied-vol representation — **typical of a market model** (payoff-independent break-even levels):
$$\mathrm{P\&L} = \underbrace{-\frac{dP}{dS}\big(\delta S-(r-q)S\delta t\big)-\frac{dP}{d\hat\sigma_{KT}}\!\bullet\!(\delta\hat\sigma_{KT}-\mu_{KT}\delta t)}_{\text{order 1}}\;-\;\frac12S^2\frac{d^2P}{dS^2}\Big[\tfrac{\delta S^2}{S^2}-\sigma^2(t,S)\delta t\Big]\;-\;\frac{d^2P}{dS\,d\hat\sigma_{KT}}\!\bullet\!\Big[S\hat\sigma_{KT}\tfrac{\delta S\,\delta\hat\sigma_{KT}}{S\hat\sigma_{KT}}-\sigma(t,S)\nu_{KT}\delta t\Big]\;-\;\frac12\frac{d^2P}{d\hat\sigma_{KT}d\hat\sigma_{K'T'}}\!\bullet\![\cdots] \tag{2.105a–d}$$
with $\nu_{KT}=\frac{1}{\hat\sigma^{LV}_{KT}}\frac{d\Sigma^{LV}_{KT}}{dS}S\sigma(t,S)$ and $\mu_{KT}=\frac{d\Sigma^{LV}_{KT}}{dt}+\frac12\sigma^2(t,S)S^2\frac{d^2\Sigma^{LV}_{KT}}{dS^2}+(r-q)S\frac{d\Sigma^{LV}_{KT}}{dS}$ (2.103).
- **[T]** In **option-price** representation (drift becomes model-independent $rO_{KT}$):
$$\mathrm{P\&L} = -\frac{dP}{dS}(\delta S-(r-q)S\delta t)-\frac{dP}{dO_{KT}}\!\bullet\!(\delta O_{KT}-rO_{KT}\delta t)-\frac12\frac{d^2P}{dS^2}\big[\delta S^2-\sigma^2(t,S)S^2\delta t\big]-\frac{d^2P}{dS\,dO_{KT}}\!\bullet\!\big[\delta S\,\delta O_{KT}-\sigma^2(t,S)S^2\tfrac{d\Omega^{LV}_{KT}}{dS}\delta t\big]-\frac12\frac{d^2P}{dO_{KT}dO_{K'T'}}\!\bullet\![\cdots] \tag{2.107a–d}$$
- **[T]** LV as an explicit market model: $dS_t=(r-q)S_tdt+\sigma_tS_tdW_t^S$ (2.109a), $dO_{KT,t}=rO_{KT,t}dt+\lambda_{KT,t}dW_t^{KT}$ (2.109b), $O_{KT,t=T}=(S_T-K)^+$ (2.110), with $W^{KT}_t\equiv W_t$ (2.111a), $\sigma_t=\sigma[O_{KT,t},t,S_t](t,S_t)$ (2.111b), $\lambda_{KT,t}=\sigma_tS_t\frac{d\Omega^{LV}_{KT}}{dS}|_{t,S_t,\sigma[\cdot]}$ (2.111c). Alternative definition: **LV = the (unique) diffusive market model with a one-dimensional Markov representation in $(t,S)$.**

**Practical notes.** (i) The delta of a vanilla option *is not a meaningful notion in a market model* — S and $O_{KT}$ are both hedge instruments; asking for the delta of one hedge instrument wrt another is like asking for the delta of $S_2$ wrt $S_1$ in a 2-asset basket (the p. 74 metaphor: correlation sets only the *break-even cross-gamma*, never the delta). (ii) Delta and the covariance structure are unrelated issues. (iii) SSR properties (short-maturity $R=2$, model-independent) are irrelevant for delta-hedging. (iv) If one insists on delta-hedging residual vega, use $\Delta=\frac{dP}{dS}+\frac{dP}{d\hat\sigma_{KT}}\!\bullet\!\beta_{KT}$ with $\beta_{KT}$ the **historical** regression coefficient.

### 2.8 Digression — payoff-dependent break-even levels

**[T]** Call-spread example (short 90, long 110, 1y). If each vanilla is delta-hedged at its own implied vol, the P&L at the spot where $\frac{d^2P^{BS_1}}{dS^2}=\frac{d^2P^{BS_2}}{dS^2}$ reduces to $\mathrm{P\&L}=\frac12S^2\frac{d^2P^{BS_1}}{dS^2}(\hat\sigma_{K_1T}^2-\hat\sigma_{K_2T}^2)\delta t$ (2.114) — **"free money" where gamma vanishes**. Risk-managing both in one model ((2.115)) distributes theta sensibly: theta is paid where gamma is large and zero where gamma vanishes. Rationale for market models.

### 2.9 The vega hedge

Key concepts: vega-hedging an exotic against *all* perturbations of the local-vol function; the conditional dollar-gamma $\varphi$; the densities $\mu(\tau,K)$.

- **[T]** Source equation for $\delta P$ under $\sigma^2\to\sigma^2+\delta\sigma^2$; Feynman–Kac:
$$\delta P = \frac12\int_0^T\!\!dt\,e^{-rt}\!\!\int_0^\infty\!\!dS\,\rho(t,S)\,\varphi(t,S)\,\delta\sigma^2(t,S) \tag{2.117}$$
- **[T]** **Conditional dollar gamma**:
$$\varphi(t,S)=\mathbb{E}_\sigma\Big[S^2\frac{d^2P}{dS^2}(t,S,\bullet)\,\Big|\,S,t\Big] \tag{2.118}$$
- **[T]** Hedge density of vanilla options $\Pi=\int_0^T\!\!d\tau\int_0^\infty\!\!dK\,\mu(\tau,K)C_{K\tau}$ (2.119); with operator
$$\mathcal Lf=\frac{df}{dt}+(r-q)S\frac{df}{dS}+\frac12S^2\frac{d^2}{dS^2}\big(\sigma^2(t,S)f\big)-rf \tag{2.120}$$
(so $\mathcal L\varphi=0$ for European payoffs), the density is
$$\boxed{\;\mu(\tau,K)=-\frac{1}{K^2}\,\mathcal L\varphi(\tau,K)\;} \tag{2.121}$$
(calling and put options give $\mu_iK_i^2\delta(S-K_i)$). In a flat-LV perturbation, $\varphi$ reduces to a weighted Monte-Carlo expectation (2.123) whose weight $w$ is the classical BS gamma weight (variance blows up when $t_k-t$ is small). **This is Dupire's result [41]; further developed by Henry-Labordère [59].**
- **[T]** Calibration meaningfulness:
$$P=P^0+\int_0^T\!\!d\tau\!\int_0^\infty\!\!dK\,\mu(\tau,K)\big[C_{K\tau}-C^0_{K\tau}\big] \tag{2.124}$$
**The price produced by a calibrated model is as credible as the hedge it implies.** If the hedge is not static, both hedge and price are questionable.

### 2.10 Markov-functional models

- **[T]** $S_t=f(t,W_t)$ (2.125) with $\frac{df}{dt}+\frac12\frac{d^2f}{dx^2}=(r-q)f$ (2.126) and $\sigma(t,S)=\frac{d\ln f}{dx}|_{x=f^{-1}(t,S)}$ (2.127). Given the smile at $T$, $f(T,x)=F^{-1}\big(N(x/\sqrt T)\big)$ (2.128). MFM is a *special* LV, calibratable at most to a *single* maturity (Carr–Madan [23]). Multi-asset Gaussian-copula pricing ≡ a multi-asset LV model with the copula's correlation matrix.
- **Practical note:** MFMs rare for equities, natural for rates/commodities/VIX futures (maturities match fixing dates).

### Appendix A — the Uncertain Volatility Model (UVM)

- **[T]** $\sigma(t,S)=\sigma_{\max}$ if $d^2P/dS^2>0$, $=\sigma_{\min}$ if $<0$; nonlinear PDE
$$\frac{dP}{dt}+(r-q)S\frac{dP}{dS}+\frac12\max_{\sigma\in\{\sigma_{\min},\sigma_{\max}\}}\Big(\sigma^2S^2\frac{d^2P}{dS^2}\Big)=rP \tag{2.130}$$
HJB for $P=\max_{\sigma_t\in[\sigma_{\min},\sigma_{\max}]}\mathbb{E}[f(S_T)]$ (2.131). Sub-additive: $P\le P_1+P_2$.
- **[T]** **$\lambda$-UVM** (Lagrangian UVM, Avellaneda et al.): $P(F)=P^{UVM}(F-\sum\lambda_iO_i)+\sum\lambda_iP^{Mkt}(O_i)$ (2.132); optimality
$$\lambda=\arg\min_\lambda\big[P^{UVM}(F-\textstyle\sum\lambda_iO_i)+\sum\lambda_iP^{Mkt}(O_i)\big],\qquad P(F)=\min_\lambda[\cdots] \tag{2.133}$$
Optimality ⇒ $P^{UVM}_{F-\sum\lambda_iO_i}(O_i)=P^{Mkt}(O_i)$ (2.137), equivalent to the constrained stochastic-control problem
$$P(F)=\max_{\substack{\sigma_t\in[\sigma_{\min},\sigma_{\max}]\\ \mathbb{E}_\sigma[O_i]=P^{Mkt}(O_i)}}\mathbb{E}_\sigma[F] \tag{2.138}$$
Setting $\sigma_{\min}=0,\sigma_{\max}=\infty$ gives model-independent lower/upper bounds (dual to sub/super-replication). Bid/offer spread $P(F)-\underline P(F)$ measures how vanilla-like the exotic is.
- **[T]** **Leland's transaction-cost formula** ($k$ = round-trip spread, $\gamma=\sqrt{2/\pi}$):
$$\hat\sigma^*_{\Gamma^+}=\sqrt{\hat\sigma^2+k\gamma\frac{\hat\sigma}{\sqrt{\delta t}}},\qquad \hat\sigma^*_{\Gamma^-}=\sqrt{\hat\sigma^2-k\gamma\frac{\hat\sigma}{\sqrt{\delta t}}} \tag{2.139}$$
$\gamma=\sqrt{2/\pi}$ overestimates (Student tails are more realistic); $\delta t$ enters explicitly — as $\delta t\to0$ or spreads widen, $\hat\sigma^*_{\Gamma^-}$ ceases to exist and one must move to a Davis–Panas–Zariphopoulou utility-based delta (bang-bang; with $\Delta_\pm=\Delta^{BS}\pm\frac{1}{S}\big(\tfrac{3}{4}e^{-r(T-t)}\lambda k^2\big)^{1/3}\Gamma_\$^{2/3}$).

---

## Chapter 3 — Forward-start options (book pp. 103–132; PDF pp. 120–149)

**Thesis.** Cliquets (forward-start options) are options on **forward implied volatility**. They can be perfectly vega/gamma/theta-hedged (in a deterministic-vol model) with **log contracts** (or $S\ln S$ contracts for FVAs), leaving exactly two residual, un-hedgeable risks: **(δP₁) volatility-of-volatility** over $[0,T_1]$ and **(δP₂) forward-smile risk** at $T_1$. Vanilla smiles barely constrain cliquet prices. LV **misprices both** δP₁ and δP₂.

### 3.1 Pricing and hedging

**Terminology.** Bergomi deliberately avoids the "forward smile" $\hat\sigma_{kT_1T_2}$ (implied from the forward-start price) — it is an *aggregate* of forward-smile and vol-of-vol risk with no historical counterpart, and is invariably more convex than a market smile of maturity $T_2-T_1$.

- **[T]** BS with time-dependent vol: $\hat\sigma_T^2=\frac{1}{T-t}\int_t^T\sigma^2(u)du$; cliquet price
$$P=e^{-r(T_1-t)}G(\hat\sigma_{T_1T_2}),\qquad \hat\sigma_{T_1T_2}^2=\frac{(T_2-t)\hat\sigma_{T_2}^2-(T_1-t)\hat\sigma_{T_1}^2}{T_2-T_1} \tag{3.1, 3.2}$$
Convex-order: $(T_2-t)\hat\sigma_{T_2}^2\ge(T_1-t)\hat\sigma_{T_1}^2$ (3.3).
- **[T]** **Vanilla portfolio with spot-independent vega.** $P=Kf(S/K)$, $\mathrm{Vega}_K(S)=K\phi(S/K)$; $\mathrm{Vega}_\Pi(S)=\int dK\rho(K)K\phi(S/K)$ (3.4); independent of $S$ iff
$$\rho(K)\propto\frac{1}{K^2} \tag{3.5}$$
which is the **log contract** $-2\ln S$ (Neuberger [75]). Twice the density is the payoff.
- **[T]** **European replication** (Breeden–Litzenberger / Carr–Madan): with $K_0=F_T$,
$$P_f=f(F_T)e^{-r(T-t)}+\int_0^{F_T}\!\frac{d^2f}{dK^2}P_K\,dK+\int_{F_T}^\infty\!\frac{d^2f}{dK^2}C_K\,dK \tag{3.7}$$
For $f=-2\ln S$: $-2\ln S=-2\ln S_0-\frac{2}{S_0}(S-S_0)+\int_0^{S_0}\frac{2}{K^2}(K-S)^+dK+\int_{S_0}^\infty\frac{2}{K^2}(S-K)^+dK$ (5.15 in Ch.5).
- **[T]** Log-contract price and its constant dollar gamma:
$$Q_T(t,S)=-2e^{-r(T-t)}\Big[\ln S+(r-q-\tfrac{\hat\sigma^2}{2})(T-t)\Big]\quad(3.8);\qquad S^2\frac{d^2Q_T}{dS^2}=2e^{-r(T-t)} \tag{3.10}$$
- **[T]** **The cliquet hedge** (zero vegas in $\hat\sigma_{T_1},\hat\sigma_{T_2}$):
$$\Pi=-P+\frac{N}{2}\Big(e^{r(T_2-T_1)}Q^{T_2}-Q^{T_1}\Big),\qquad N=\frac{1}{(T_2-T_1)\hat\sigma_{T_1T_2}}\frac{dG}{d\hat\sigma_{T_1T_2}} \tag{3.9}$$
Hedge ratios are $t$- and $S$-independent (**static**) — a decisive virtue. Residual P&L:
$$\mathrm{P\&L}_\Pi=e^{-r(T_1-t)}\Big[-\big(G(\hat\sigma)-G(\hat\sigma+\delta\hat\sigma)\big)+\frac{dG}{d(\hat\sigma^2)}\delta(\hat\sigma^2)\Big] \tag{3.11}$$
Which, to order 2, is
$$\mathrm{P\&L}_\Pi=-\frac{e^{-r(T_1-t)}}{2}\frac{d^2G}{d(\hat\sigma_{T_1T_2}^2)^2}\,\delta(\hat\sigma^2_{T_1T_2})^2 \tag{3.12}$$
For an ATMF call ($G\simeq\hat\sigma_{T_1T_2}\sqrt{T_2-T_1}/\sqrt{2\pi}$, (3.13)): $\mathrm{P\&L}_\Pi\simeq e^{-r(T_1-t)}\frac{\sqrt{T_2-T_1}}{\sqrt{2\pi}}\frac{1}{2\hat\sigma_{T_1T_2}}(\delta\hat\sigma_{T_1T_2})^2$ (3.14) — **we make money whenever $\hat\sigma_{T_1T_2}$ moves** (δP₁ is *negative*, a price reduction).
- **[T]** At $T_1$ the at-the-money call is worth $P^{BS}(S_{T_1},K=S_{T_1},T_2;\hat\sigma_{K=S_{T_1}T_2}(T_1))$ (3.15), but our scheme prices it at $P^{BS}(S_{T_1},K=S_{T_1},T_2;\hat\sigma_{T_2}(T_1))$ (3.16) — **the difference is δP₂ (forward-smile risk).**
- **[T]** Quoted price:
$$P=e^{-rT_1}G(\hat\sigma_{T_1T_2}(t{=}0))+(\delta P_1+\delta P_2) \tag{3.17}$$

**Practical notes.** Forward volatility $\hat\sigma_{T_1T_2}$ is hedgeable with vanillas; forward smile and vol-of-vol are **not** and must be priced from exogenous (historical or implied) levels. Digital/narrow-call-spread cliquets have negligible $\hat\sigma_{T_1T_2}$ sensitivity: $\delta P_2$ *is* the price — a **pure forward-smile instrument**. "*An at-the-money forward call does have forward-smile sensitivity.*" Model choice: continuous forward-variance models (Ch.7) have no separate handles on spot-starting smile vs future smiles; local-stochastic models (Ch.12) calibrate to the vanilla smile so $\delta P_2\to0$ (implying less control on future smiles); **discrete** forward-variance models give separate handles on δP₁ and δP₂.

### 3.1.7 Model-independent bounds (from vanilla smiles)

**[T]** Super-replication LP: $\mathrm{UB}=\min_{\lambda,\mu,\Delta(S_1),c}\big[c+\sum_i\lambda_iC_{K_iT_1}+\sum_j\mu_jC_{K_jT_2}\big]$ s.t. $c+\sum_i\lambda_i(S_1-K_i)^++\sum_j\mu_j(S_2-K_j)^++\Delta(S_1)(S_2-S_1)\ge(S_2/S_1-1)^+\ \forall(S_1,S_2)$; solvable by simplex. Dual = max cliquet price over joint densities matching both marginals and $E[S_{T_2}|S_{T_1}]=S_{T_1}$ (Henry-Labordère).

**Numerical results** ($T_1=1y$, $T_2=2y$, flat 20% smiles). Forward ATM call: $\hat\sigma_{\min}\simeq9\%$, $\hat\sigma_{\max}\simeq25\%$. 95/105 forward call spread: $CS_{\min}\simeq1.6\%$, $CS_{\max}\simeq7.7\%$ (skews −8% … +8% — vs a typical index 1y skew of 3%). Adding the ATM-forward-call price (20%): $CS\in[1.8\%,7.2\%]$ — barely tighter. Adding a congruent 90/110 forward call spread (22%/18%): $CS\in[4.25\%,6.7\%]$ (skew −1% … +5.5%). **Conclusion: only prices of payoffs whose risk is *congruent* narrow the range; exotics is not a brokerage business.**

### 3.1.9 Forward volatility agreements (FVAs)

- **[T]** Payoff $(S_{T_2}-kS_{T_1})^+$; more generally $S_{T_1}g(S_{T_2}/S_{T_1})$: $P(t,S)=Se^{-q(T_1-t)}G(\hat\sigma_{T_1T_2})$ (3.18) — vega is **linear in $S$**, so the hedge is a density $\rho(K)\propto1/K$, i.e. the **$S\ln S$ contract** ($f(S)=S\ln S$).
- **[T]** $R_T(t,S)=Se^{-q(T-t)}\big[\ln S+(r-q)(T-t)+\tfrac{(T-t)\hat\sigma_T^2}{2}\big]$ (3.19), $\frac{dR_T}{d\hat\sigma_T}=Se^{-q(T-t)}(T-t)\hat\sigma_T$ (3.20). Hedge $\Pi=-P+N(e^{q(T_2-T_1)}R_{T_2}-R_{T_1})$ (3.23), $N$ as before. Residual $\mathrm{P\&L}_\Pi=-\frac{Se^{-q(T_1-t)}}{2}\frac{d^2G}{d(\hat\sigma^2)^2}\delta(\hat\sigma_{T_1T_2}^2)^2$ (3.24).
- **Key point:** starting from (3.18) one would identify *spot/forward-vol covariance* as a main risk; using the correct $S\ln S$ hedges, **spot/volatility covariance risk is not relevant** — it is offset by the hedge instruments.

### 3.2 Forward-start options in the local volatility model

- **[T]** Log-contract implied vol approximation (order one in $\delta\sigma$ around $\sigma_0$, $\beta=0$):
$$\hat\sigma_T=\frac1T\int_0^T\sigma(t)dt-\frac{\sigma_0^2T}{2}\mathcal S_T \tag{3.28,3.30}$$
$$\frac{d\hat\sigma_T}{d\ln S_0}=\frac1T\int_0^T\alpha(t)dt=\frac{d\hat\sigma_{F_TT}}{d\ln S_0} \tag{3.29, 3.31}$$
(3.30 is a relationship *between implied vols*: $\hat\sigma_T\simeq\hat\sigma_{F_TT}-\frac{\hat\sigma_{F_TT}^2T}{2}\mathcal S_T$.) **Accuracy: poor for real smiles** (Fig. 3.1/3.2 — the LV of a Euro Stoxx smile is not of the log-linear form; the log contract's *constant* dollar gamma makes its implied vol sensitive to the density far from the money). Right order of magnitude for $d\hat\sigma_T/d\ln S_0$ only.
- **[T]** Forward-vol dynamics (order one in $\alpha$):
$$d\hat\sigma_{T_1T_2}=\Big(\frac{1}{T_2-T_1}\int_{T_1}^{T_2}\alpha(u)du\Big)d\ln S_t \tag{3.33}$$
**The vol-of-vol of a forward vol is set entirely by the local skew over $[T_1,T_2]$**; LV is **not time-homogeneous** (with $T_2-T_1$ fixed, the vol of $\hat\sigma_{T_1T_2}$ does not depend on $T_1-t$). Future skew:
$$\mathcal S_\theta(S_{T_1},T_1)=\int_0^1\alpha(T_1+u\theta)u\,du \tag{3.34};\qquad \mathcal S_\theta(S_{T_1},T_1)\propto T_1^{-\gamma}\ll\mathcal S_\theta(S_0,0)$$
- **[T]** Vega hedge of a forward-start call in LV. At $T_1^+$: $\varphi(T_1^+,S)=\frac{1}{\sigma_0(T_2-T_1)S}\frac{1}{S}\frac{dP^{BS}}{d\sigma_0}|_{K=kS}$; discrete density at $T_1$:
$$\Psi_1(K)=-\frac{1}{K^2}\varphi(T_1^+,S)=-\frac{1}{K^2}\frac{1}{\sqrt{2\pi}\,\sigma_0\sqrt{T_2-T_1}}e^{-\frac{\big(\ln k+\sigma_0^2(T_2-T_1)/2\big)^2}{2\sigma_0^2(T_2-T_1)}} \tag{3.36}$$
$\propto1/K^2$ — **exactly the log-contract hedge** of §3.1.4 (static, $S_0$- and $T_1$-independent). But the **$T_2$ density** $\Psi_2(K)=\frac{1}{K^2}\varphi(T_2^-,K)$ (3.38) and a **continuous density** for intermediate maturities are *not* static. Our §3.1.4 hedge (options of $T_1,T_2$ only) is preferable; LV's non-static vega hedge (and hence its price) is "suspicious."

**Chapter digest (key).** Cliquets ⇒ dynamically hedged log contracts; carry P&L = gamma P&L on forward vol + forward-smile adjustment. Calibration on vanilla smile has little relevance. FVAs ⇒ $S\ln S$ contracts. LV dynamics of forward vol set by local skew on $[T_1,T_2]$, not time-homogeneous ⇒ **LV misprices vol-of-vol**; future skews too weak ⇒ **LV misprices forward-smile risk**. If an LV vega hedge is not static, both the hedge and the price are untrustworthy.

---

## Chapter 4 — Stochastic volatility: introduction (book pp. 133–150; PDF pp. 150–167)

**Thesis.** "Hoping to construct a market model for vanilla options by modeling implied volatilities of vanilla options directly is a **dead end**" (also for local volatilities, whose drifts are non-local). The tractable state variables are **forward variances of specific European payoffs** — the **power payoffs** $\big(S_T/F_T\big)^p$; for $p\to0$ these are log contracts / variance swaps.

### 4.1–4.2 Modeling implied vols / local-vol dynamics — why it fails

- **[T]** If one *tries* $dS=\sigma SdW^S$, $dC_{KT}=\Lambda_{KT}dW^{KT}$ (4.1) with $C_{KT}(T)=(S_T-K)^+$ (4.2), or $dS=\sigma SdW^S$, $d\hat\sigma_{KT}=\mu_{KT}dt+\lambda_{KT}dW^{KT}$ (4.3) with $\lim_{t\to T}(T-t)\hat\sigma^2_{KT,t}=0$ (4.4): the risk-neutral drift of $\hat\sigma_{KT}$ is forced (quoted from [80]):
$$\mu_{KT}=\frac{1}{\hat\sigma_{KT}}\Big[\frac{\hat\sigma_{KT}^2-\sigma^2}{2(T-t)}-\frac{d_1d_2}{2}\lambda^2_{KT}+\frac{1}{\sqrt{T-t}}\rho\sigma\lambda_{KT}\Big]$$
with $d_1=\frac{1}{\hat\sigma_{KT}\sqrt{T-t}}\big[\ln\frac{F_T(S_t)}{K}+\frac{\hat\sigma^2_{KT}(T-t)}{2}\big]$, $d_2=d_1-\hat\sigma_{KT}\sqrt{T-t}$. Constraint: $\lim_{T\to t}\hat\sigma_{ST,t}=\sigma_t$ (4.5). **The initial smile information has to be embedded in the process for $\sigma$ in a convoluted way** ⇒ impractical.
- **[T]** Modeling the **local-vol function dynamics** $\sigma_t(\tau,S)$: $\sigma_t=\sigma_t(t,S_t)$ (4.6); $d\sigma^2_{\tau S}=\mu_{\tau S}dt+\lambda_{\tau S}dW^{\tau S}$ (4.7) with $\sigma^2_{\tau S}=2\frac{dC_{KT}/dT}{K^2d^2C_{KT}/dK^2}|_{K=S,T=\tau}$ (4.8). Drift (Kani–Derman [39]; re-derived by Carmona–Nadtochiy [21]):
$$\mu_{\tau S}=-\frac{\lambda_{\tau S}}{\rho_{\tau S}}\Big[S\frac{d\rho_{\tau S}(t,S,\sigma^2)}{dS}\Big]\sigma_{tS}\frac{\langle dW^SdW^{\tau S}\rangle}{dt}+\frac12\int_t^\tau\!\!du\!\int_0^\infty\!\!dx\,\rho_{ux}\,x^2\frac{d^2\rho_{\tau S}(ux,\sigma^2)}{dx^2}\,\lambda_{ux}\frac{\langle dW^{ux}dW^{\tau S}\rangle}{dt} \tag{4.14}$$
**Non-local, involves forward transition densities for all $u$** ⇒ computationally too expensive; only two trivial solutions ($\lambda_{\tau S}\equiv0$ ⇒ LV; or all local vols uncorrelated ⇒ *also* collapses to LV).

### 4.3 Power payoffs and forward variances

- **[T]** Power payoff $S_T^p$:
$$Q_{pT}=e^{-r(T-t)}F_T^p\,e^{\frac{p(p-1)}{2}(T-t)\hat\sigma^2} \tag{4.15}$$
$\hat\sigma_{pT}$ well-defined for $p\ne0,1$ (concave for $p\in]0,1[$, convex otherwise). For $p\in[0,1]$ prices always finite (Lee [67] gives the growth-rate bounds in $\ln K$ linked to moment indices $p^\pm$).
- **[T]** Characteristic function and Matytsin's moneyness:
$$\frac{Q_{pT}}{F_T^p}e^{r(T-t)}=\mathbb{E}\big[e^{px}\big]=L(p),\ x=\ln\frac{S_T}{F_T};\qquad z(K)=\frac{\ln(K/F_T)}{\hat\sigma_{KT}\sqrt T}-\frac{\hat\sigma_{KT}\sqrt T}{2} \tag{4.16, 4.17}$$
$$L(p)=\int_{-\infty}^{+\infty}\frac{1}{\sqrt{2\pi}}e^{-\frac{z^2}{2}}e^{-p(\frac{\omega^2}{2}+z\omega)}\frac{d\omega/dz}{1+p}\,dz,\qquad \omega(z)=\hat\sigma_{K(z)T}\sqrt T \tag{4.18}$$
$p$-dependent moneyness $y=z+p\,\omega(z)$:
$$y(K)=\frac{\ln(K/F_T)}{\hat\sigma_{KT}\sqrt T}+\Big(p-\frac12\Big)\hat\sigma_{KT}\sqrt T \tag{4.19}$$
($p=0$: $y=d_2$; $p=1$: $y=d_1$; $K\leftrightarrow y$ monotone.)
- **[T]** **Master relation between vanilla and power-payoff implied vols:**
$$e^{\frac{p(p-1)}{2}\hat\sigma_{pT}^2}=\int_{-\infty}^{+\infty}\frac{dy}{\sqrt{2\pi}}e^{-\frac{y^2}{2}}e^{\frac{p(p-1)}{2}\hat\sigma_{K(y,p)T}^2} \tag{4.20}$$
$p\to0$ (**log contract**, Chriss–Morokoff [32]):
$$\hat\sigma_{\ln S}^2=\int_{-\infty}^{+\infty}\frac{dy}{\sqrt{2\pi}}e^{-y^2/2}\hat\sigma_{K(y)T}^2,\qquad y(K)=\frac{\ln(K/F_T)}{\hat\sigma_{KT}\sqrt T}-\frac{\hat\sigma_{KT}\sqrt T}{2} \tag{4.21a,b}$$
$p\to1$ (**$S\ln S$ contract**):
$$\hat\sigma_{S\ln S}^2=\int_{-\infty}^{+\infty}\frac{dy}{\sqrt{2\pi}}e^{-y^2/2}\hat\sigma_{K(y)T}^2,\qquad y(K)=\frac{\ln(K/F_T)}{\hat\sigma_{KT}\sqrt T}+\frac{\hat\sigma_{KT}\sqrt T}{2} \tag{4.22a,b}$$
**Practical:** (4.21) is far less sensitive to discretisation than (3.7) — a Gauss–Hermite quadrature with ~10 points is accurate; exactly $\hat\sigma_0$ for a flat smile.
- **[T]** **Forward variances.** Convex order ⇒ $(T_2-t)\hat\sigma_{pT_2}^2\ge(T_1-t)\hat\sigma_{pT_1}^2$ (4.23). Discrete and continuous:
$$\xi_{pT_1T_2}=\frac{(T_2-t)\hat\sigma_{pT_2}^2-(T_1-t)\hat\sigma_{pT_1}^2}{T_2-T_1} \tag{4.24};\qquad \xi_{pT}=\frac{d}{dT}\big[(T-t)\hat\sigma_{pT}^2\big] \tag{4.25}$$
**The variance curve $\{\xi_{pT}\}$ is the state variable set.**
- **[T]** **Dynamics.** $dS=\sigma SdW^S$, $d\xi_{pT}=\mu_{pT}dt+\lambda_{pT}dW^{pT}$ (4.26). Since $Q_{pT}=S^pe^{\frac{p(p-1)}{2}\int_t^T\xi^{p\tau}d\tau}$ (4.27), requiring $Q$ driftless gives
$$\mu_T=-\Big[p\sigma\lambda_T\rho_{ST}+\frac{p(p-1)}{2}\int_t^T\rho_{Tu}\lambda_T\lambda_u\,du\Big] \tag{4.29}$$
and $T\to t$ gives the **key constraint**
$$\xi_t^t=\sigma_t^2 \tag{4.30}$$
i.e. **the short end of every variance curve equals the instantaneous variance of $S$.** Final SDEs:
$$dS_t=\sqrt{\xi_t^t}\,S_tdW_t^S \tag{4.31a};\qquad d\xi_t^{pT}=-\Big[p\sqrt{\xi_t^t}\,\lambda_{Tt}\rho_{ST}+\frac{p(p-1)}{2}\int_t^T\rho_{Tu}\lambda_{Tt}\lambda_{ut}\,du\Big]dt+\lambda_{Tt}dW_t^T \tag{4.31b}$$
- **[T]** **Markov representation attempt** (Cheyette-style ansatz $\alpha_i(T)\beta_{it}$, $\beta_{it}=e^{k_it}$, $\alpha_i(T)=\alpha_ie^{-k_iT}$):
$$\xi_t^T=\xi_0^T+\sum_i\alpha_i(T)\Big[-\frac{p(p-1)}{2}\sum_jB_{ij,t}(A_j^T-A_j^t)+x_t^i\Big] \tag{4.33}$$
with $dx_t^i=-p\rho_{iS}\beta_{it}\sqrt{\xi_t^t}\,dt-\frac{p(p-1)}{2}\sum_jB_{ij,t}\alpha_j(t)dt+\beta_{it}dW_t^i$ (4.35a), $dB_{ij,t}=\rho_{ij}\beta_{it}\beta_{jt}dt$ (4.35b), $dS_t=\sqrt{\xi_0^t+\sum_i\alpha_i(t)x_t^i}\,S_tdW_t^S$ (4.35c); $\xi_t^t=\xi_0^t+\sum_i\alpha_i(t)x_t^i$ (4.34). **BUT:** unlike forward *rates*, variances must stay positive and there is no guarantee that $\xi_t^t\ge0$; the Cheyette ansatz **does not transpose**. "There does not seem to be a solution unless $p=0$ or $p=1$."
- **[T]** Multiple variance curves: a solution for one $p^*$ generates $\xi_t^p$ for all $p$, but their **initial conditions cannot be set** ⇒ no exact smile calibration. Only the term structure $\hat\sigma_{p^*T}$ is calibrated exactly.
- **[T]** **$p\to0$ (log contract).** With $\zeta_t^T\equiv\xi^{p=0,T}$:
$$dS_t=\sqrt{\zeta_t^t}\,S_tdW_t^S,\qquad d\zeta_t^T=\lambda_t^TdW_t^T \tag{4.36}$$
**Forward variances of log contracts are driftless.** Caveats: log contracts not traded (need all strikes), and with cash dividends $E[S_{T_2}|S_{T_1}]=F_{T_2}/F_{T_1}$ fails. **Rescue: variance swaps are traded; (4.36) survives with $\zeta^T$ replaced by VS forward variances** — the building blocks of Ch. 7.

**Chapter digest (key).** Direct modeling of vanilla implied vols is a dead end; so is modeling local-vol dynamics (non-local drifts). Power payoffs $p$ give tractable variance curves; $p\to0$ has **zero drift**.

---

## Chapter 5 — Variance swaps (book pp. 151–200; PDF pp. 168–217)

**Thesis.** A variance swap is (up to second order in $\delta S/S$) a delta-hedged log contract run at *zero implied vol*. Therefore, **in any diffusive model, $\hat\sigma_{VS,T}=\hat\sigma_T$ and every diffusive model calibrated to a given smile prices VSs identically** — VS and log-contract forward variances coincide ($\xi^T=\zeta^T$). The difference $\hat\sigma_{VS,T}-\hat\sigma_T$ measures the **implied skewness of short-horizon returns**; it is non-zero only in non-diffusive (jump/Lévy) models, and inferring it from a calibrated jump model is "unreasonable." Practically, $\hat\sigma_{VS,T}=\hat\sigma_T$.

### 5.1 VS forward variances

- **[T]** Market convention (N trading days):
$$\frac{252}{N}\sum_{i=0}^{N-1}\Big[\ln^2\frac{S_{i+1}}{S_i}-\hat\sigma_{VS,T}^2(t)\Big] \tag{5.1}\quad\longrightarrow\quad \frac{1}{T-t}\sum_{i=0}^{N-1}\Big[\ln^2\frac{S_{i+1}}{S_i}-\hat\sigma_{VS,T}^2(t)\Big] \tag{5.2}$$
- **[T]** Discrete forward variance:
$$\hat\sigma_{VS,T_1T_2}^2(t)=\frac{(T_2-t)\hat\sigma_{VS,T_2}^2(t)-(T_1-t)\hat\sigma_{VS,T_1}^2(t)}{T_2-T_1} \tag{(5.4)}$$
it is **positive and driftless** — a long-$(T_2-t)$/short-$(T_1-t)e^{-r(T_2-T_1)}$ VS position can be unwound at $t_0$ for a P&L $(T_2-T_1)[\hat\sigma_{VS,T_1T_2}^2(t_0)-\hat\sigma_{VS,T_1T_2}^2(t)]$ (5.5) **linear in the change of the forward variance, at zero cost**. Continuous VS forward variance:
$$\xi_t^T=\frac{d}{dT}\big[(T-t)\hat\sigma_{VS,T}^2(t)\big],\qquad d\xi_t^T=\bullet\,dW_t^T \tag{5.6}$$
- **Contrast with equity:** to get a P&L linear in $\delta S$ you must borrow and pay interest; forward VS variances have **zero pricing drift** ($\xi^T$ has no financing cost).

### 5.2 Relationship to log contracts

- **[T]** VS payoff (undiscounted) ≈ discounted sum of the gamma part of daily gamma/theta P&Ls at *zero* implied vol:
$$e^{-rT}\sum_{i=0}^{N-1}\Big(\frac{\delta S_i}{S_i}\Big)^2=\sum_{i=0}^{N-1}e^{-rt_i}e^{-r(T-t_i)}\Big(\frac{\delta S_i}{S_i}\Big)^2 \tag{5.8}$$
- **[T]** Matching condition: find $P$ with
$$\frac12S^2\frac{d^2P_{\hat\sigma=0}}{dS^2}=e^{-r(T-t)} \tag{5.9}$$
Solution: the **log contract** $Q_T$ (3.8), with $dQ_T^{\hat\sigma=0}/dS=-2e^{-r(T-t)}/S$, $\frac12S^2d^2Q_T^{\hat\sigma=0}/dS^2=e^{-r(T-t)}$ (5.11).
- **[T]** VS strike:
$$\hat\sigma_{VS,T}^2=\frac{e^{rT}}{T}\big(Q^{market}_T-Q_T^{\hat\sigma=0}\big) \tag{5.12}\qquad\Longrightarrow\qquad \hat\sigma_{VS,T}=\hat\sigma_T,\ \ \xi_t^T=\zeta_t^T \tag{5.13,5.14}$$
- **[V]** Equivalent vanilla-replication formula:
$$\hat\sigma_{VS,T}^2=\frac{e^{rT}}{T}\int_0^\infty\frac{2}{K^2}\big(P^{market}_{KT}-P^{\hat\sigma_{KT}=0}_{KT}\big)dK \tag{5.16}$$
with $P^{\hat\sigma=0}_{KT}=e^{-rT}(Se^{(r-q)T}-K)^+$; call/put parity makes the integrand identical for calls and puts. Holds only without cash-amount dividends (else use (5.47)).
- **[T]** Direct weighted-average formula (from Ch.4 (4.21)): **[V]**-verified structure
$$\hat\sigma_{VS,T}^2=\int_{-\infty}^{+\infty}\frac{dy}{\sqrt{2\pi}}e^{-y^2/2}\hat\sigma_{K(y)T}^2,\qquad y(K)=\frac{\ln(K/F_T)}{\hat\sigma_{KT}\sqrt T}-\frac{\hat\sigma_{KT}\sqrt T}{2} \tag{5.17a,b}$$
**Practical:** (5.17)/(4.21) is the efficient route (insensitive to discretisation; exact for flat smiles). But $\hat\sigma_T$ is very sensitive to the **extrapolation of the smile outside traded strikes**; market makers invert the other way (infer low-strike implied vols from VS quotes).

### 5.3 Impact of large returns

- **[T]** Diffusive case: $dS_t=(r-q)S_tdt+\sigma_tS_tdW_t$ (5.19); from (2.30)–(2.31),
$$P_{\sigma T}=P_{\hat\sigma_T=0}+e^{-rT}\mathbb{E}_\sigma\Big[\int_0^T\sigma_t^2dt\Big] \tag{5.21};\qquad \hat\sigma_{VS,T}^2=\mathbb{E}_\sigma\Big[\frac1T\int_0^T\sigma_t^2dt\Big]=\frac{e^{rT}}{T}\big(P^{Market}_T-P^{\hat\sigma_T=0}_T\big) \tag{5.22,5.23}$$
⇒ **any diffusive model calibrated to the smile gives the same $\hat\sigma_{VS,T}$**, and $\hat\sigma_{VS,T}=\hat\sigma_T$.
- **[T]** Jump-diffusion $dS_t=\sigma_tS_tdW_t^S+S_{t^-}\big(JdN_t-\lambda\bar Jdt\big)$ (5.24). Then:
$$\hat\sigma_T^2=\mathbb{E}\Big[\frac1T\int_0^T\sigma_t^2dt\Big]-2\lambda\big[\ln(1+J)-J\big]\Big\langle\cdot\Big\rangle \tag{5.25};\qquad \hat\sigma_{VS,T}^2=\mathbb{E}\Big[\frac1T\int_0^T\sigma_t^2dt\Big]+\lambda\langle\ln^2(1+J)\rangle \tag{5.27}$$
- **[V]** **The jump-diffusion spread:**
$$\hat\sigma_{VS,T}^2-\hat\sigma_T^2=\lambda\big\langle\ln^2(1+J)+2\ln(1+J)-2J\big\rangle \tag{5.28}$$
> **[V]** Confirmed on p. 159 (PDF p. 176); $\langle\cdot\rangle$ = expectation over the iid jump size $J$. (Independent re-derivation: the bracket $=J^2-J^3+\cdots+2J-J^2+\tfrac23J^3+\cdots-2J=-\tfrac13J^3+\cdots$ ✓.)
- **[V]** Expansion in powers of $J$ (leading term at order 3):
$$\hat\sigma_{VS,T}^2-\hat\sigma_T^2\simeq-\frac13\lambda J^3 \tag{5.29}$$
> **[V]** Derivation checked: first non-vanishing order is $J^3$ (order $J^2$ indistinguishable from diffusion), $\lambda J^n\sim J^{n-2}$ with $\lambda\propto1/J^2$ as $J\to0$ ⇒ $n=3$ dominates. ✓
- **[T]** Calibrating jumps to the smile (Ch.10 (10.26)): $\mathcal S_T\simeq\frac{\lambda J^3}{6\hat\sigma_T^3T}$ (5.30) ⇒
$$\hat\sigma_{VS,T}^2-\hat\sigma_T^2\simeq-2\hat\sigma_T^3\mathcal S_T T \tag{5.31};\qquad \hat\sigma_{VS,T}\simeq\hat\sigma_T\big(1-\hat\sigma_T\mathcal S_T T\big) \tag{5.32}$$
For a 1y index VS, $\hat\sigma_T=20\%$, $\mathcal S_T=-0.2$ ⇒ −4% correction ≈ 1 vol point.
- **[T]** **Model-free** (long VS vs short delta-hedged log contract, per $\Delta t$):
$$\mathrm{P\&L}=2\big(e^{r_i}-1\big)-2r_i-r_i^2-\big(\hat\sigma_T^2-\hat\sigma_{VS,T}^2\big)\Delta t \tag{5.35}$$
$$\mathrm{P\&L}\simeq\frac{r_i^3}{3}-\big(\hat\sigma_T^2-\hat\sigma_{VS,T}^2\big)\Delta t \tag{5.36}\quad\Longrightarrow\quad \hat\sigma_{VS,T}^2-\hat\sigma_T^2\simeq-\frac{\langle r^3\rangle}{3\Delta t}\simeq-\frac{s_{\Delta t}}{3}\hat\sigma_T^3\Delta t^{3/2} \tag{5.37}$$
$$\frac{\hat\sigma_{VS,T}}{\hat\sigma_T}-1\simeq-\frac{s_{\Delta t}}{6}\hat\sigma_T\sqrt{\Delta t} \tag{5.38}$$
with $s_{\Delta t}=\langle r^3\rangle/\langle r^2\rangle^{3/2}$ the skewness of daily log-returns.
- **[T]** Inferring short-return skewness from the smile (combining 5.37 and 5.31):
$$s_{\Delta t}\simeq\frac{6\,\mathcal S_T T}{\sqrt{\Delta t}} \tag{5.39}$$
For 1y, $\mathcal S_T=-0.2$, $\Delta t=1/252$: $s_{\Delta t}\simeq-19$ — absurdly large (much bigger than realized). This is because jump models with small jumps force $\mathcal S_T\propto1/T$ (via $s_T\propto1/\sqrt T$ and the Ch.5 App.B identity $\mathcal S_T=s_T/(6\sqrt T)$ (5.40)). Market skews scale like $1/\sqrt T$, so the assumption is unsupported.

**Practical notes.** (i) Realized daily skewness is order 1 (sign varies), giving only ~0.2% relative adjustment to $\hat\sigma_{VS,T}$ — negligible. (ii) A historical estimator of the mismatch, $\frac12\big(\frac{\langle r^2\rangle}{\langle 2(e^r-1)-2r\rangle}-1\big)$ (5.41), is very noisy; max 2.5% around the 1987 crash. (iii) For a stress reserve, use (5.42): $\hat\sigma_{VS,T}^2=\hat\sigma_T^2+\varepsilon\big[\ln^2(1+J)+2\ln(1+J)-2J\big]$ with $\varepsilon$ = annualised jump probability, $J<0$ for equities (e.g. $\varepsilon=12$, $J=-5\%$ ⇒ +0.13%).
- **Practical note on conventions.** The market convention uses $\ln^2$; had it used standard returns $(S_{i+1}/S_i-1)$, the order-3 term would be $-\tfrac23r^3$ rather than $+\tfrac13r^3$ — a *sign flip* in the leading mismatch.

### 5.4 Impact of strike discreteness

**[T]** With discrete strikes $\Delta\ln K=5\%$, the replication error is ±2% on $\hat\sigma_T$ (≈±0.5 vol point at 20%) and *unbiased noise*; with $\Delta\ln K=1\%$ it is acceptable for 1y. This is a *second*, independent reason for a market $\hat\sigma_{VS,T}\ne\hat\sigma_T$ spread.

### 5.5 Conclusion

**[T]** (i) If log contracts were traded, $\hat\sigma_{VS,T}$ and $\hat\sigma_T$ would be separate market parameters, their difference measuring the implied skewness of daily returns ($dS=\sigma_tS_tdW^S_t$, $d\zeta_t^T=\lambda_t^TdU_t^T$, $d\xi_t^T=\psi_t^TdV_t^T$). (ii) Absent liquid log contracts, pricing VSs with a smile-calibrated jump model is incoherent. (iii) VSs are *more* liquid than far OTM vanillas, so $\hat\sigma_{VS,T}$ is a market parameter and desks choose the low-strike extrapolation to enforce $\hat\sigma_{VS,T}=\hat\sigma_T$. (iv) **Base assumption of the remainder of the book:**
$$\boxed{\;dS_t=\sqrt{\xi_t^t}\,S_tdW_t^S,\qquad d\xi_t^T=\lambda_t^TdW_t^T\;}\tag{5.43}$$
(v) To *dissociate* $\hat\sigma_{VS,T}$ from $\hat\sigma_T$ within a diffusive model, apply the additive adjustment (5.42) to realized variance / to $\zeta^T$:
$$\ln^2\frac{S_{i+1}}{S_i}\to\ln^2\frac{S_{i+1}}{S_i}+(\lambda\Delta)\big[\ln^2(1+J)+2\ln(1+J)-2J\big];\qquad \zeta_t^T=\xi_t^T+\lambda\big[\ln^2(1+J)+2\ln(1+J)-2J\big]$$
with $\lambda,J$ (or time-dependent $\lambda$) calibrated to the market spread. (This is not a jump model: vanillas are still priced diffusively.)

### 5.6 Dividends

- **[T]** Payoff impact: $\mathbb{E}[\ln^2\frac{S_{i+1}}{S_i}]=\sigma^2\Delta t+\ln^2\frac{S_i-d}{S_i}+2(r-q-\tfrac{\sigma^2}{2})\Delta t\ln\frac{S_i-d}{S_i}$ (5.44); the last two terms are negligible for stocks (returns adjusted by $d$) and for indexes (many small dividends; $n\ln^2(1-q/n)\sim1/n$; e.g. $\sigma_r=20.005\%$).
- **[T]** Replication impact: $\frac12S^2d^2Q_T/dS^2=\big[S/(S-\sum_{t<T_j<T}d_j)\big]^2$ (5.45) ≠ 1. Supplement the log contract with European payoffs $E^j(S)=2\ln\big(\frac{S-d_j}{S}\big)$ (5.46) maturing at dividend dates:
$$\hat\sigma_{VS,T}^2=\frac{e^{rT}}{T}\Big[Q^{market}_T-Q^{\hat\sigma=0}_T+\sum_{T_j<T}\big(E^{market}_j-E^{\hat\sigma_j=0}_j\big)\Big] \tag{5.47}$$

### 5.7 Pricing VSs with a PDE

- **[T]** (Preferred for indexes, equivalent to (5.47) by §5.3.1):
$$\hat\sigma_{VS,T}^2=\frac1T\int_0^TU(0,S_0),\qquad \frac{dU}{dt}+(r-q)S\frac{dU}{dS}+\frac{\sigma^2(t,S)}{2}S^2\frac{d^2U}{dS^2}=-\sigma^2(t,S) \tag{5.48,5.49}$$
terminal $U(T,S)=0$; dividend matching $U(T_j^-,S)=U(T_j^+,S-d_j)$. Index convention (returns not stripped of dividends) adds a discontinuity (5.51): $U(T_j^-,S)=U(T_j^+,S-d_j(S))+\ln^2\big(1-\frac{d_j(S)}{S}\big)$; **must cap the effective dividend yield** ($d_j(S)\to\max(d_j(S),y_j^{\max}S)$, $y_j^{\max}<1$) or steep index smiles inflate this term unreasonably.
- **[T]** Adjusting for large returns within the PDE: (5.52) $\hat\sigma_{VS,T}^2=\hat\sigma_T^2-\frac13\varepsilon J^3$ and (5.53)
$$\frac{dU}{dt}+(r-q)S\frac{dU}{dS}+\frac{\sigma^2(t,S)}{2}S^2\frac{d^2U}{dS^2}=-\Big(\sigma^2(t,S)-\frac13\varepsilon J^3\Big) \tag{5.53}$$
constant $J,\varepsilon$: $U(0,S_0)-\tfrac13(\varepsilon T)J^3$. For weighted VSs replace $\sigma^2\to w(S)\sigma^2$ and take $\varepsilon J^3\equiv-\mu\hat\sigma^3(t,S)$ (calibrate $\mu$ to VS quotes).

### 5.8 Interest-rate volatility

- **[T]** $\hat\sigma_T$ is the implied vol of the **forward** $F_t^T$; a VS pays the realized variance of the **spot** $S_t$. With Ho–Lee normal rate vol $\sigma_r$ and correlation $\rho$:
$$\hat\sigma_T^2=\hat\sigma_{VS,T}^2+\rho\hat\sigma_{VS,T}\sigma_rT+\frac{\sigma_r^2T^2}{3} \tag{5.54}\qquad\Longrightarrow\qquad \hat\sigma_{VS,T}=\hat\sigma_T-\frac{\rho}{2}\sigma_rT \tag{5.55}$$
For $\hat\sigma_T=25\%$, 5 bps/day, $\rho=50\%$, 5y: $\hat\sigma_{VS,T}=24\%$ — **one vol point; not small.** This dominates the $\hat\sigma_{VS,T}$ mismatch for long maturities (or an inappropriate dividend model).

### 5.9 Weighted variance swaps

- **[T]** $\frac{1}{T-t}\sum w(S_i)\ln^2\frac{S_{i+1}}{S_i}-\frac{\Delta t}{T-t}\hat\sigma^2\sum w(S_i)$ (5.56). Replication at order two in $\delta S$: terminal European payoff $f$ with $\frac12S^2f''(S)=w(Se^{-\mu(T-t)})$ (5.58) — impossible unless $w\equiv1$; so set $\mu=0$ (risk-manage at zero implied vol with $q=r$) and add a continuous density $(r-q)$ of unhedged European options of payoffs $e^{-r(T-\tau)}S\frac{df}{dS}$ over $[0,T]$.
- **[T]** Examples: **gamma swap** $w(S)=S$ ⇒ $f(S)=2S\ln S$, strike $=\hat\sigma_{S\ln S}$ (≤ $\hat\sigma_{VS}$; density $2/K$ beats $2/K^2$ for strong skews). **Arithmetic VS** $w(S)=S^2$ ⇒ $f$ is a parabola: **the only exactly-replicable variance payoff even for large returns**. **Corridor VS** $w(S)=\mathbf 1_{[L,H]}$ ⇒ truncated log contract (explicit piecewise $f$); barrier crossings generate a mismatch $\frac{(S_{i+1}-S_i)^2}{H^2}-\frac{(S_{i+1}-H)^2}{H^2}$ that *none* of the standard term-sheet provisions matches — must be estimated and folded into the strike.

### Appendix A — timer options

- **[T]** Adjust $\hat\sigma_t$ in real time so each gamma/theta P&L is absorbed: $\frac12(\sigma_t^2-\hat\sigma_t^2)\delta t+(T-t)\hat\sigma_t\delta\hat\sigma_t=0$; with $Q_t=\int_0^t\sigma_\tau^2d\tau$:
$$\hat\sigma_t^2=\frac{\hat\sigma_{t=0}^2T-Q_t}{T-t} \tag{5.67}$$
Yields a P&L whose sign is that of $Q_T-\hat\sigma_{t=0}^2T$ (either positive, or negative from the time $\tau$ when $Q_\tau$ exhausts the budget).
- **[T]** **Vega/gamma relationship** derivation: $V=\hat\sigma S^2\frac{d^2P_{\hat\sigma}}{dS^2}(T-t)$ (5.66); proof uses $e^{-r(T-t)}\frac{d^nP_{\hat\sigma}}{d\ln S^n}$ martingale for all $n$ (equivalent to the classical BS vega–gamma relationship (1.12)).
- **[T]** **Timer option price (model-independent, zero rates/repo, diffusion):**
$$P_{BS}(S,Q;\overline Q)=\mathbb{E}\Big[f\Big(Se^{-\frac{\overline Q-Q}{2}+\sqrt{\overline Q-Q}\,Z}\Big)\Big] \tag{5.68}$$
— Black–Scholes with vol 1 and maturity $\overline Q-Q$. Conditions for model-independence: $\frac{dP}{dt}=0$ (5.70a) and $\frac{S^2}{2}\frac{d^2P}{dS^2}+\frac{dP}{dQ}=0$ (5.70b) — "Black–Scholes with time replaced by quadratic variation." Weighted quadratic variation $\delta Q=\mu(S)\sigma_t^2\delta t$ ⇒ $\frac{S^2}{2}\frac{d^2P}{dS^2}+\mu(S)\frac{dP}{dQ}=0$. Non-zero $r,q$ re-introduce physical time: requires (5.72a,b), giving $P(t,S,Q)=e^{rt}p(Se^{-(r-q)t},Q)$ and the settlement $e^{-r(T-\tau)}f(S_\tau e^{(r-q)(T-\tau)})$ (5.73). Higher-order residual: $\mathrm{P\&L}=\big(\frac{S^2}{2}\frac{d^2P}{dS^2}+\frac{S^3}{3}\frac{d^3P}{dS^3}\big)\frac{\delta S^3}{S^3}$ (5.71) — orders of magnitude smaller than a vanilla's gamma P&L (factor $\delta S/S$).
- **[T]** **Leveraged ETFs.** With leverage $\beta$: $\delta\ln I=\beta\,\delta\ln S+\big(r-\beta(r-q)\big)\delta t-\frac{\beta(\beta-1)}{2}\delta Q$; hence
$$I(t,S,Q)=I_0e^{rt}\Big(\frac{S}{S_0e^{(r-q)t}}\Big)^{\beta}e^{-\frac{\beta(\beta-1)}{2}Q} \tag{5.75}$$
A pure delta strategy; model-independent in a diffusive setting. $\beta\to0$ limit: $\lim_{\beta\to0}\frac1\beta\big(e^{-rT}\frac{I_T}{I_0}-1\big)=\ln\frac{S_T}{S_0e^{(r-q)T}}+\frac{Q_T}{2}$ (5.76) — the VS replication again.

### Appendix B — perturbation of the lognormal distribution

Key concepts: cumulant-generating function; Gram–Charlier expansion; keeping forward variances/log-contract vols fixed.

- **[T]** $L(q)=\ln\int e^{-qz}\rho(z)dz$ (5.77); for normal $L_0(q)=\frac{\Sigma^2}{2}(q+q^2)$ (5.78); cumulants $\kappa_n$ from $L(q)=\sum_n\frac{(-1)^n}{n!}\kappa_nq^n$; $\kappa_3$ relates to skewness, $\kappa_4$ to excess kurtosis. Perturb $\delta\kappa_n$, $n\ge3$:
$$L(q)=L_0(q)+\sum_{n=3}^\infty\frac{(-1)^n}{n!}\delta\kappa_nq^n \tag{5.79}$$
- **[T]** **Normalization choices** (keeping $E[S_T]=F_T$ ⇔ $L(-1)=0$): (a) shift only, $\delta\kappa_1=-\sum_{n\ge3}\delta\kappa_n/n!$; (b) variance only, $\delta\kappa_2=-2\sum_{n\ge3}\delta\kappa_n/n!$:
$$L(q)=L_0(q)+\sum_{n=3}^\infty\frac{\delta\kappa_n}{n!}\big[(-1)^nq^n-q^2\big] \tag{5.80}$$
(c) mixed with free $\theta_n$ (5.81).
- **[T]** **Density perturbation (Gram–Charlier):**
$$\rho(z)=\rho_0(z)+\delta\rho(z),\qquad \delta\rho(z)=\sum_{n=1}^\infty\frac{\delta\kappa_n}{n!}(-1)^n\frac{d^n\rho_0(z)}{dz^n} \tag{5.83, Gram–Charlier}$$
$$\delta\rho(z)=\sum_{n=3}^\infty\frac{\delta\kappa_n}{n!}\Big((-1)^n\frac{d^n}{dz^n}-\frac{d^2}{dz^2}\Big)\rho_0(z) \tag{5.85 (normalization 5.80)}$$
- **[T]** Since $\hat\sigma_T^2=\frac2T\frac{dL}{dq}|_{q=0}=-\frac{2}{T}\kappa_1$ (5.82), **keeping $\kappa_1$ fixed keeps the log-contract/VS implied vol unchanged** (the economically motivated normalization (5.80)).
- **[T]** **Price perturbation:** $\delta P=\sum_{n=3}^\infty\frac{\delta\kappa_n}{n!}\big(\frac{d^n}{d\ln S^n}-\frac{d^2}{d\ln S^2}\big)P_0$ (5.88); **implied-vol perturbation:**
$$\delta\hat\sigma=\frac{1}{\hat\sigma_0T}\sum_{n=3}^\infty\frac{\delta\kappa_n}{n!}\frac{\frac{d^nP_0}{d\ln S^n}-\frac{d^2P_0}{d\ln S^2}}{\frac{d^2P_0}{d\ln S^2}-\frac{dP_0}{d\ln S}}+\frac{1}{\hat\sigma_0T}\sum_{n=3}^\infty\frac{\delta\kappa_n}{n!}\theta_n \tag{5.90}$$
$\theta_n\ne0$ shifts all implied vols uniformly (does not affect the skew).
- **[T]** **ATMF skew at order one in the cumulants:**
$$\mathcal S_T=\frac{1}{\sqrt T}\sum_{n=3}^\infty\frac{\delta\kappa_n}{n!}\frac{\int_0^\infty\big((-1)^n\frac{1}{2}\frac{d^n\rho_0}{dz^n}+\frac{d^{n+1}\rho_0}{dz^{n+1}}-\frac12\frac{d^2\rho_0}{dz^2}+\frac{d^3\rho_0}{dz^3}\big)(e^z-1)dz}{\Sigma\rho_0(0)} \tag{5.91}$$
With $\delta\kappa_3=s\Sigma^3,\delta\kappa_4=\kappa\Sigma^4$:
$$\mathcal S_T=\frac{1}{\sqrt T}\Big(\frac{s}{6}+\frac{\kappa}{12}\hat\sigma_0\sqrt T+\cdots\Big) \tag{5.92}$$
and, retaining only $\delta\kappa_3$,
$$\boxed{\;\mathcal S_T=\frac{s}{6\sqrt T}\;} \tag{5.93}$$
**(5.93) is "remarkably robust — presumably because it involves no volatility reference level, only the dimensionless skewness."** This is the first-order seed of the Ch. 8 (Bergomi–Guyon) volatility-of-volatility expansion.

---

## Chapter 6 — Heston as a one-factor forward-variance model (book pp. 201–216; PDF pp. 218–233)

*(Included because it is the natural foil for Ch. 7 and introduces the vol-of-vol term structure criterion.)*

- **[T]** Heston SDEs: $dS_t=\sqrt{V_t}S_tdW_t$, $dV_t=-k(V_t-V_0)dt+\sigma\sqrt{V_t}dZ_t$ (6.1), $\mathrm{corr}=\rho$; $V_t=\xi_t^t=\sigma_t^2$; $\sigma$ (not a lognormal vol) has dimension time$^{-1}$.
- **[T]** Forward variances: $\xi_t^T=V_0+e^{-k(T-t)}(V_t-V_0)$ (6.3); VS vol:
$$\hat\sigma_T^2(t)=V_0+\frac{1-e^{-k(T-t)}}{k(T-t)}(V_t-V_0) \tag{6.4}$$
- **[T]** Heston in forward-variance form:
$$dS_t=\sqrt{\xi_t^t}S_tdW_t,\qquad d\xi_t^T=\sigma e^{-k(T-t)}\sqrt{\xi_t^t}\,dZ_t \tag{6.5}$$
A **one-factor Markov-functional model** for forward variances — but with the constraint $\frac{d\xi_0^T}{dT}=-k(\xi_0^T-V_0)$ (6.2): **cannot accommodate a general VS term structure.**
- **[T]** **Drift of $V_t$ has nothing to do with "market price of risk":** it is the slope of the short end of the variance curve,
$$dV_t=\frac{d\xi_t^T}{dT}\Big|_{T=t}dt+\lambda_t^tdZ_t^t$$
- **[T]** Vol-of-vol term structure: $\mathrm{vol}(\hat\sigma_T)\propto\frac{1-e^{-k(T-t)}}{k(T-t)}$ (6.9) for flat VS term structure; short $T$: $\to1$; long $T$: $\propto1/(T-t)$. **Heston cannot fit the empirical power-law vol-of-vol term structure over a wide maturity range.** Short ATMF vols are **normal**, not lognormal, with normal vol $\sigma/2$.
- **[T]** Vol-of-vol **smile**: $\hat\sigma_T(t)\ge\hat\sigma_T^{\min}(t)=\sqrt{V_0\big(1-\frac{1-e^{-k(T-t)}}{k(T-t)}\big)}$ — VS vols are floored; vols of VS vols vanish near the floor (a substantial effect).
- **[T]** **ATMF skew (order one in $\sigma$).** $\delta P=\frac{\rho\sigma}{2}\int_0^T V_\tau(V)\frac{1-e^{-k(T-\tau)}}{k}d\tau\big(\frac{d^3P_0}{d\ln S^3}-\frac{d^2P_0}{d\ln S^2}\big)$ (6.16 is the implied-vol version):
$$\mathcal S_T=\frac{1}{\hat\sigma_T^3T^2}\frac{\rho\sigma}{2}\int_0^T V_\tau\frac{1-e^{-k(T-\tau)}}{k}d\tau \tag{6.17b};\qquad \hat\sigma_{F_TT}=\hat\sigma_T\Big(1+\frac{\hat\sigma_T T}{2}\mathcal S_T\Big) \tag{6.17a}$$
Short maturities: $\hat\sigma_{F_TT}=\sqrt V\big(1+\frac{\rho\sigma T}{8}\big)$ (6.18a), $\mathcal S_T=\frac{\rho\sigma}{4\sqrt V}=\frac{\rho\sigma}{4\hat\sigma_{F_TT}}$ (6.18b). Long: $\mathcal S_T=\frac{\rho\sigma}{2\sqrt{V_0}}\frac{1}{kT}$ (6.19b) — **decays as $1/T$.** Flat VS term structure:
$$\frac{d\hat\sigma_{KT}}{d\ln K}\Big|_{\text{ATMF}}=\frac{\rho\sigma}{2\sqrt{V_0}}\frac{kT+e^{-kT}-1}{(kT)^2} \tag{6.20}$$
- **[T]** Order-one-in-$\sigma$ **skew** is accurate to ~10%; the difference $\hat\sigma_{F_TT}-\hat\sigma_T$ is *poorly* approximated at order one (order two needed — see Ch. 8 §8.2).

**Practical/structural criticisms.** (i) Heston hard-wires $\mathcal S_T\propto1/\hat\sigma_{F_TT}$ (inverse dependence of skew on vol level), which reality does not show. (ii) It is a one-factor model with an embedded time scale $1/k$; the vol-of-vol and skew scalings are structural. (iii) Making $V_0(t)$ time-dependent to fit the VS term structure is legitimate (VSs are hedges); making $\sigma$ or $\rho$ time-dependent is questionable unless cliquets of varying maturities can be traded. (iv) The real problem "lies not so much with the model … but with its usage: which practical pricing or hedging issue naturally calls for SDE (6.5)?"

---

## Chapter 7 — Forward variance models (book pp. 217–300; PDF pp. 234–317; covered here to PDF p. 260 ≈ book p. 243)

**Thesis.** Model the variance curve $\xi_t^T$ directly as state variables alongside $S$. Exactly calibrated to a VS term structure *by construction*; designed for direct control of the term structure of vol-of-vol, the term structure of ATMF skew, the smile of vol-of-vol. Key device: a **Markov-functional representation** of the whole curve via a few Ornstein–Uhlenbeck factors $X^i$, which is **exactly simulable**.

### 7.1 Pricing equation

- **[T]** P&L of a delta- and vega-hedged short option:
$$\mathrm{P\&L}=-\Big[P(t+\delta t,S+\delta S,\xi+\delta\xi)-(1+r\delta t)P(t,S,\xi)\Big]+\frac{dP}{dS}(\delta S-(r-q)S\delta t)+\int_t^T\frac{\delta P}{\delta\xi^u}\delta\xi^u$$
Break-even covariances:
$$\mu(t,u)\delta t=\Big\langle\frac{\delta S}{S}\delta\xi^u\Big\rangle_t \tag{7.2a};\qquad \nu(t,u,u')\delta t=\big\langle\delta\xi^u\delta\xi^{u'}\big\rangle_t \tag{7.2b}$$
- **[T]** Desired carry form with $\sigma(t,S,\xi)^2=(\hat\sigma_t^t)^2=\xi_t^t$ (no free theta) ⇒ **pricing equation**
$$\frac{dP}{dt}+(r-q)S\frac{dP}{dS}+\frac{\xi_t^t}{2}S^2\frac{d^2P}{dS^2}+\frac12\int_t^T\!\!\int_t^T\!\!du\,du'\,\nu(t,u,u',\xi)\frac{\delta^2P}{\delta\xi^u\delta\xi^{u'}}+\int_t^T\!\!du\,\mu(t,u,\xi)S\frac{\delta^2P}{dS\delta\xi^u}=rP \tag{7.4}$$
with $P=\mathbb{E}[g(S_T)|S_t=S,\xi_t^u=\xi^u]$ and SDEs $dS_t=(r-q)S_tdt+\sqrt{\xi_t^t}S_tdW_t^S$, $d\xi_t^u=\lambda_t^udW_t^u$, subject to (7.5)–(7.6).

### 7.2 A Markov representation

- **[T]** Lognormal forward variances with **time-homogeneous** vol: $d\xi_t^T=\omega(T-t)\xi_t^TdW_t^T$ (7.7); solution (7.8). Requirements for a Markov-functional representation: $\omega(u)=\omega e^{-ku}$ (7.9) ⇒ driven by a single OU process $dX_t=-kX_tdt+dW_t$, $X_0=0$:
$$\boxed{\;\xi_t^T=\xi_0^T\exp\Big(\omega e^{-k(T-t)}X_t-\frac{\omega^2}{2}e^{-2k(T-t)}\mathbb E[X_t^2]\Big)\;}\qquad \mathbb E[X_t^2]=\frac{1-e^{-2kt}}{2k} \tag{7.10}$$
> **[V]** Confirmed on p. 221 (PDF p. 238), symbol-for-symbol. $\omega$ = lognormal vol of the zero-maturity forward variance.

### 7.3 $N$-factor models

- **[V]** $d\xi_t^T=\omega\alpha_w\xi_t^T\sum_iw_ie^{-k_i(T-t)}dW_t^i$ (7.11); $\omega=2\nu$ (7.12a); $\alpha_w=1/\sqrt{\sum_{ij}w_iw_j\rho_{ij}}$ (7.12b). Here $\nu$ is the lognormal vol of a *VS volatility* of vanishing maturity; $\omega=2\nu$ since variance is the square.
> **[V]** (7.11),(7.12a,b) confirmed on p. 221 (PDF p. 238).
- **[T]** Solution: $\xi_t^T=\xi_0^T\exp\big(\omega\sum_iw_ie^{-k_i(T-t)}X_t^i-\frac{\omega^2}{2}\sum_{ij}w_iw_je^{-(k_i+k_j)(T-t)}\mathbb E[X_t^iX_t^j]\big)$ (7.13), $dX_t^i=-k_iX_t^idt+dW_t^i$, $X_0^i=0$ (7.14).
- **[T]** **Exact simulation** (no time-stepping needed for variance-only payoffs): $X^i_{\tau_{n+1}}=e^{-k_i\delta\tau}X^i_{\tau_n}+\delta X^i$ (7.15); $\mathbb E[X^i_{\tau_{n+1}}X^j_{\tau_{n+1}}]=e^{-(k_i+k_j)\delta\tau}\mathbb E[X^iX^j]+\mathbb E[\delta X^i\delta X^j]$ (7.16);
$$\mathbb E[\delta X^i\delta X^j]=\rho_{ij}\frac{1-e^{-(k_i+k_j)\delta\tau}}{k_i+k_j} \tag{7.17};\qquad \mathbb E[\delta W^S\delta X^i]=\rho_{iS}\frac{1-e^{-k_i\delta\tau}}{k_i} \tag{7.18}$$
- **[T]** Vol of vol and correlations:
$$\omega(T-t)=(2\nu)\alpha_w\sqrt{\sum_{ij}w_iw_j\rho_{ij}e^{-(k_i+k_j)(T-t)}} \tag{7.19};\qquad \rho_t(\xi^T,\xi^{T'})=\frac{\sum_{ij}w_iw_j\rho_{ij}e^{-(k_i(T-t)+k_j(T'-t))}}{\sqrt{\sum_{ij}w_iw_j\rho_{ij}e^{-(k_i+k_j)(T-t)}}\sqrt{\cdots(T'-t)}} \tag{7.20}$$
$$\nu_T(t)=\nu\alpha_w\sqrt{\sum_{ij}w_iw_j\rho_{ij}f_i(t,T)f_j(t,T)},\qquad f_i(t,T)=\frac{\int_t^T\xi_t^\tau e^{-k_i(\tau-t)}d\tau}{\int_t^T\xi_t^\tau d\tau} \tag{7.22}$$
$\nu_T(t)$ = instantaneous lognormal vol of $\hat\sigma_T(t)$; $\nu_t(t)=\nu$ (global scale factor). Forward VS vol $\hat\sigma_{T_1T_2}(t)=\sqrt{\frac{1}{T_2-T_1}\int_{T_1}^{T_2}\xi_t^\tau d\tau}$; $\nu_{T_1T_2}(t)$ similarly with $f_i(t,T_1,T_2)$ (7.23).
- **[T]** **Flat VS term structure:** with $I(x)=\frac{1-e^{-x}}{x}$ (7.25),
$$\nu_T(t)=\nu\alpha_w\sqrt{\sum_{ij}w_iw_j\rho_{ij}I(k_i(T-t))I(k_j(T-t))} \tag{7.24}$$
$$\nu_{T_1T_2}(t)=\nu\alpha_w\sqrt{\sum_{ij}w_iw_j\rho_{ij}I(k_i(T_2-T_1))I(k_j(T_2-T_1))}\,e^{-(k_i+k_j)(T_1-t)} \tag{7.26}$$
⇒ time-homogeneous (functions of $T-t$ resp. $T_1-t,T_2-t$ only). **Reference case for parameter setting.**
- **[T]** Spot/variance and variance/variance break-even functions:
$$\mu(t,u,\xi)=\omega\alpha_w\sqrt{\xi_t^t\xi_t^u}\sum_i\rho_{SX^i}w_ie^{-k_i(u-t)} \tag{7.27a};\qquad \nu(t,u,u',\xi)=\omega^2\alpha_w^2\xi_t^u\xi_t^{u'}\sum_{ij}\rho_{ij}w_iw_je^{-k_i(u-t)}e^{-k_j(u'-t)} \tag{7.27b}$$
**Crucial practical point (vega-hedging):** $N$ model factors set the *rank and structure of the break-even covariance matrix*, **not** the hedge ratios. The purpose of a vega hedge is to immunise against *all* deformations $\delta\xi^T$ of the curve, not just those the model's own Brownian factors allow. "Calculation of deltas is not connected in any way to the covariance structure of the hedging instruments in the model at hand."

### 7.4 A two-factor model

- **[T]** One factor is equivalent to Heston: $\nu_T(t)=\nu I(k(T-t))=\nu\frac{1-e^{-k(T-t)}}{k(T-t)}$ = (6.9). **Insufficient flexibility.**
- **[T]** Two OU processes, mixing parameter $\theta\in[0,1]$:
$$d\xi_t^T=(2\nu)\xi_t^T\alpha_\theta\Big[(1-\theta)e^{-k_1(T-t)}dW_t^1+\theta e^{-k_2(T-t)}dW_t^2\Big] \tag{7.28};\qquad \alpha_\theta=\frac{1}{\sqrt{(1-\theta)^2+\theta^2+2\rho_{12}\theta(1-\theta)}} \tag{7.29}$$
With $x_t^T=\alpha_\theta\big[(1-\theta)e^{-k_1(T-t)}X_t^1+\theta e^{-k_2(T-t)}X_t^2\big]$ (7.30) → $d\xi_t^T=(2\nu)\xi_t^Tdx_t^T$ (7.32), $(dx_t^T)^2=\eta^2(T-t)dt$ (7.31a) with
$$\eta(u)=\alpha_\theta\sqrt{(1-\theta)^2e^{-2k_1u}+\theta^2e^{-2k_2u}+2\rho_{12}\theta(1-\theta)e^{-(k_1+k_2)u}} \tag{7.31b},\quad \eta(0)=1$$
$$\xi_t^T=\xi_0^Tf^T(t,x_t^T),\qquad f^T(t,x)=e^{\omega x-\frac{\omega^2}{2}\chi(t,T)},\ \omega=2\nu \tag{7.33,7.34}$$
$$\chi(t,T)=\int_{T-t}d\tau\,\eta^2(\tau)\ \ (7.35)\ \text{(explicit form with }k_1,k_2,\rho_{12}\text{ factors, (7.35))}$$
- **[T]** $\hat\sigma_T$ dynamics: $\frac{d\hat\sigma_T}{\hat\sigma_T}=\nu\alpha_\theta\big[(1-\theta)A_1dW_t^1+\theta A_2dW_t^2\big]+\bullet dt$ (7.36,7.37), $A_i=\frac{\int_t^T\xi_t^\tau e^{-k_i(\tau-t)}d\tau}{\int_t^T\xi_t^\tau d\tau}$ (7.38);
$$\nu_T(t)=\nu\alpha_\theta\sqrt{(1-\theta)^2A_1^2+\theta^2A_2^2+2\rho_{12}\theta(1-\theta)A_1A_2} \tag{7.39}$$
- **[T]** **Benchmark vol-of-vol form** (empirical power law):
$$\nu_T^B(t)=\sigma_0\Big(\frac{\tau_0}{T-t}\Big)^{\alpha} \tag{7.40}$$
Typical: $\alpha=0.4$, $\tau_0=3$m, $\sigma_0\approx100\%$ **implied** (realized 3m VS vol-of-vol ≈60% for Euro Stoxx 50; implied ≈2×). Table 7.1 gives three parameter sets matching this benchmark out to 5y with $\rho_{12}=-70\%,0,+70\%$; e.g. Set II: $\nu=174\%,\theta=0.245,k_1=5.35,k_2=0.28$. **Two factors capture a power-law vol-of-vol term structure over a wide maturity range, with 1/k₁, 1/k₂ well separated.**
- **[T]** Correlation structure: correlations are invariant under $k_i\to k_i+c$; the relevant scales are $1/(k_i-k_j)$. In a two-factor model $\rho(\xi^T,\xi^{T'})$ depends only on $k_1-k_2$: **a single correlation time scale** — the main motivation for a third factor. Note that $\rho(\xi^T,\xi^{T'})\to1$ for $T,T'\gg1/(k_1-k_2)$.
- **[T]** Variance-swaption smile (option on $\hat\sigma_{T_1T_2}$): weak increasing (nearly lognormal), well approximated by the strike-independent level
$$2\hat\nu_{T_1T_2}(T_1)=2\sqrt{\frac1{T_1}\int_0^{T_1}\nu_{T_1T_2}^2(t)dt} \tag{7.41}$$

### 7.5 Calibration — the vanilla smile

**[T]** Natural underliers: $S$ and *forward variances / VS volatilities*. "Calibrating" to a VS/ATMF term structure = inputting underlier values (hardly a calibration); fitting model parameters to the whole smile is different and its hedge ratios may reflect model-specific structure. Forward-variance models are equivalently **market models for spot and a one-dimensional term structure of implied vols at a given moneyness**, with exogenously specified dynamics.

### 7.6 Options on realized variance

- **[T]** Payoff $\frac{1}{2\hat\sigma_{\mathrm{ref}}}\big(\hat\sigma_r^2(T)-\hat\sigma^2\big)^+$; for ATM ($\hat\sigma=\hat\sigma_T$) and to order one this is $(\hat\sigma_r(T)-\hat\sigma_T)^+$.
- **[T]** **Simple model (SM).** The underlying $U_t=\dfrac{Q_t+(T-t)\hat\sigma_T^2(t)}{T}$ (7.43) is exactly replicated by $\frac{T-t}{T}$ VS contracts of maturity $T$ (P&L $=U_{t'}-U_t$, (7.42)); $U$ is driftless, $U_0=\hat\sigma_T^2(0)$, $U_T=Q_T/T$, and the option pays $(U_T-\hat\sigma^2)^+$. From $U_t=\frac1T\big[\int_0^t\xi_\tau^\tau d\tau+\int_t^T\xi_t^\tau d\tau\big]$ (7.44). SDE:
$$\frac{dU_t}{U_t}=2R_t\frac{T-t}{T}\nu_T(t)dW_t,\qquad R_t=\frac{\hat\sigma_T^2(t)}{U_t}=\frac{T\hat\sigma_T^2(t)}{Q_t+(T-t)\hat\sigma_T^2(t)} \tag{7.46,7.47}$$
- **[T]** Approximation $R_\tau\simeq R_t$ ⇒ $U$ lognormal ⇒ Black–Scholes:
$$P(t,U)=P_{BS}(t,U,\sigma_{\mathrm{eff}},T),\qquad \sigma_{\mathrm{eff}}^2=\frac1{T-t}\int_t^T4R_t^2\Big(\frac{T-\tau}{T}\Big)^2\nu_T^2(\tau)d\tau \tag{7.49a,b}$$
At inception $R_0=1$: $P(0)=P_{BS}(0,\hat\sigma_T^2(0),\sigma_{\mathrm{eff}},T)$ (7.50a), $\sigma_{\mathrm{eff}}^2=\frac1T\int_0^T4\big(\frac{T-\tau}{T}\big)^2\nu_T^2(\tau)d\tau$ (7.50b); with the benchmark (7.53): $\sigma_{\mathrm{eff}}=\frac{2\sigma_0}{\sqrt{3-2\alpha}}\big(\frac{\tau_0}{T}\big)^\alpha$.
- **Conclusion (important):** options on realized variance are hedged by dynamically trading variance swaps of the option's residual maturity (hedge count $\frac{T-t}{T}\frac{dP}{dU}$); **their value depends only on $\nu_T(t)$ for $t\in[0,T]$** — i.e. on the *vol-of-vol curve*, not on the detailed forward-variance dynamics. Table 7.2: SM vs exact two-factor MC agree to ~2-3% (6m ATM call: exact 2.94–2.97%, SM 2.86–2.93%; benchmark 2.82%).
- **[T]** Term-structure correction: replacing $R_\tau$ by $\frac{T\hat\sigma_{\tau T}^2(t)}{Q_t+(T-t)\hat\sigma_T^2(t)}$ (7.54) gives
$$\sigma_{\mathrm{eff}}^2=\frac{1}{T-t}\int_t^T\Big(\frac{T-\tau}{T}\Big)^2\Big(\frac{T\hat\sigma_{\tau T}^2(t)}{Q_t+(T-t)\hat\sigma_T^2(t)}\Big)^2\nu_T^2(\tau)d\tau \tag{7.55}$$
and at $t=0$ (7.56). The option then acquires exposure to $Q_t$ and intermediate VS vols — hedged by an intermediate continuous VS density $\lambda(\tau)=-\frac{dP}{d\sigma_{\mathrm{eff}}^2}\frac{8(\tau-t)(T-\tau)}{(T-t)T}\frac{T\hat\sigma_{\tau T}^2(t)}{(Q_t+(T-t)\hat\sigma_T^2(t))^2}\nu_T^2(\tau)$ (7.58) plus a discrete VS of maturity $T$, $\mu_T=\frac{dP}{d\sigma_{\mathrm{eff}}^2}\frac{d\sigma_{\mathrm{eff}}^2}{d\hat\sigma_T^2}$.
- **[T]** **Key structural result:** the vega hedge *is also the gamma/theta hedge* — because $\hat\sigma_\tau^2(t)$ always appears coupled with $Q_t$ as $Q_t+(\tau-t)\hat\sigma_\tau^2(t)$ (a package exactly replicated by a VS), the VS position hedging the term-structure sensitivity simultaneously hedges the $Q_t$ sensitivity. Also, $\lambda(\tau),\mu_T$ satisfy $\int_0^T\lambda(\tau)d\hat\sigma_\tau^2d\tau+\mu_Td\hat\sigma_T^2=0$ (uniform rescaling of VS vols leaves $\sigma_{\mathrm{eff}}$ unchanged).

**Practical pitfall noted.** If realized vol is systematically *below* implied VS vol (typical for indexes), $R_t>1$ and the realized vol of $U$ exceeds the priced level ⇒ a short call on realized variance loses money steadily even when instantaneous $\nu_T$ matches. This exposure is what the term-structure VS hedge addresses.

---

## Cross-cutting: the "Bergomi framework"

- **Forward variance curve and its dynamics.** State variables $(S_t,\{\xi_t^T\})$; $\xi_t^T$ are driftless (zero financing cost, hedgeable via VS/VS term structure); the **short end is the instantaneous variance**, $\xi_t^t=\sigma_t^2$ (4.30) — the universal constraint across all $p$. The curve's dynamics are specified by vol-of-vol $\nu_T(t)$ (or $\omega(T-t)$) and correlations; the *drift* is then determined so that VS/log-contract prices are martingales (4.29). The **Markov-functional** device (exponentially decaying vol structure ⇔ OU factors) makes the whole curve simulable from finitely many state variables (7.10)–(7.14), exactly.
- **Where the genuine "Bergomi–Guyon expansion" lives.** It is **Chapter 8** ("The smile of stochastic volatility models", book pp. 307–355), i.e. **beyond the assigned page range**: §8.2 expansion of the price in volatility of volatility, §8.3 expansion of implied vols, §8.4 a representation of European option prices in diffusive models (order-one vol-of-vol), §8.6–8.7 application to one-factor/Heston and the two-factor model, §8.9 forward-start options/future smiles, §8.10 impact of the *smile of vol-of-vol* on the vanilla smile. **n-th order volatility-of-volatility** appears from §8.2 onward plus appendix C ("partial resummation of higher orders"). The *first-order seed* of that machinery is Ch. 5 Appendix B (cumulant/Gram–Charlier expansion, eq. (5.88), (5.90), (5.93)) covered above.
- **Vol-of-vol observables.** Instantaneous (lognormal) vol of $\hat\sigma_T$ is $\nu_T(t)$; for short maturities $\mathrm{vol}(\hat\sigma_{F_TT})\simeq2\mathcal S_T$ in LV (2.85) and in SV models the smile of vol-of-vol is *positive and vol-dependent* ($d\hat\sigma_{ATM}=\bullet\,dt+\hat\sigma_{ATM}^\gamma dZ$, $\gamma>1$ empirically). The **smile of vol-of-vol** is a separate control in the two-factor model via the *non-lognormality* of $f^T$ (modifying (7.34)) — treated in §7.7.1.
- **Unifying diagnostic.** The single most useful invariant across all chapters: **the ATMF skew equals a weighted integral of the instantaneous spot/vol covariance** — $\mathcal S_T=\frac{1}{\hat\sigma_T^2T}\int_0^T\frac{T-t}{T}\langle d\ln S_t\,d\hat\sigma_T(t)\rangle dt$ (2.89). Redistributing that covariance over $[0,T]$ at fixed integral leaves $\mathcal S_T$ (the *static* smile) unchanged but changes $R_T$ (the *dynamics*). This is exactly why LV and SV models with the same smile have different SSRs and different future skews.

---

## Verification notes (formulas flagged)

**Read directly from rendered page images and confirmed symbol-for-symbol (vision):**
- (2.3) Dupire formula — p. 26 / PDF p. 43. Text layer and Ch. 2 digest (PDF p. 113) both give numerator $dC/dT+qC+(r-q)K\,dC/dK$ and denominator $K^2d^2C/dK^2$ with leading factor 2; the vision read confirmed the structure and the factor 2 (the tiny $qC$ was dropped at a line break in the vision output — the text layer and the book's own digest retain it).
- (2.19) Dupire in implied-vol coordinates — p. 34 / PDF p. 50. Denominator rederived and checked against the standard Gatheral form; expands exactly. The OCR rendered "$1/f$" ambiguously as "$1/y$"; $1/f$ is correct.
- (2.64) SSR in the local-volatility model, $R_T=1+\frac1T\int_0^T(\mathcal S_t/\mathcal S_T)dt$ — p. 52 / PDF p. 69; integral limits and subscripts confirmed.
- (5.28) and (5.29) jump-diffusion VS/log-contract variance spread and its $-\frac13\lambda J^3$ leading term — p. 159 / PDF p. 176. (5.29) independently re-derived by Taylor expansion.
- (7.10) exponential-vol Markov representation of $\xi_t^T$; (7.11) $N$-factor SDE; (7.12a,b) $\omega=2\nu$, $\alpha_w$ normalization — p. 221 / PDF p. 238. Exact match.

**Reconstructed / flagged [R] (layout-garbled in the text layer; re-derived and/or cross-checked against an internal restatement — high confidence but confirm the coefficient on the page image before quoting a number):**
- (1.11) variance of the aggregated gamma/theta P&L — reconstructed so as to reproduce the coefficients of (1.14) and (1.15) in their respective limits.
- (1.13) and (1.15) standard deviation of the final P&L in the general (real) case — reconstructed from the garbled pdf layout; both reduce correctly to (1.14) ($\Omega=\kappa=0$) and (1.15) $\to$ (1.16) for $f(\tau)=\rho e^{-k\tau}$. **Highest-risk reconstructions in Ch. 1.**
- (1.16) — the right-hand side prefactor $\rho\Omega/2$ is read from the text layer and confirmed consistent with (1.15) under $f(\tau)=\rho e^{-k\tau}$; treat the exact placement of $2$ vs $T$ as verified-by-consistency only.

**Transcribed from the text layer [T] (column layout mangled but content recovered; cross-checked against Bergomi's own per-chapter "Chapter's digest" restatements, which independently repeat most key formulas — e.g. (2.3), (2.19), (2.40), (2.42), (2.48), (2.54), (2.61), (2.64), (2.87)/[=(2.64)], (5.2), (5.17), (5.43), (6.5), (7.11)):** all other numbered formulas listed above.

**Known limitations / caveats.**
- The text layer for *displayed* equations is column-garbled throughout (pdftotext -layout interleaves multi-line fractions); inline and short equations are clean. Any coefficient-critical formula not marked [V] should be re-checked against the rendered page.
- Pages beyond PDF p. 270 are not rendered in `/tmp/atlas_pages2/bergomi/` (only p-001…p-270 exist, with gaps); Ch. 7 coverage therefore stops at PDF p. 260 (≈ book p. 243, §7.6.5) as the task specified. Sections 7.6.6–7.8 (VIX futures/options, discrete forward-variance models) and all of Ch. 8+ are outside this extraction.
- The source PDF was **not modified**; the only file created from it is `/tmp/atlas_pages2/bergomi.txt` (regenerated text layer; the previously assumed file did not exist).
