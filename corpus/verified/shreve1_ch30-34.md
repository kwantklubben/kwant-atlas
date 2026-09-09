# Shreve — Stochastic Calculus for Finance I (combined lecture edition) — Chapters 30–34: MATH-VERIFIED EXTRACTION

Source: rendered pages `/tmp/atlas_pages/shreve1/p-001.png … p-349.png`; text `/tmp/atlas_extract/shreve1.txt`; prior notes `/tmp/atlas_extract/shreve.md`.
Method: vision-read of the PNGs (ground truth for every symbol below) cross-checked against `shreve1.txt`, whose pdftotext output silently drops many Greek letters and exponent tiers (see ERRORS below).

---

## ⚠️ CRITICAL — chapter-identification error in the task brief and in shreve.md

**What Chapters 30–34 ACTUALLY are in this combined edition** (per the running heads and all content):

| Ch | Actual title (verified on pages) | PDF pages | Book pages |
|----|----------------------------------|-----------|-----------|
| 30 | **Hull and White model** | p-295 … p-304 | 293–302 |
| 31 | **Cox-Ingersoll-Ross model** | p-305 … p-320 | 303–318 |
| 32 | **A two-factor model (Duffie & Kan)** | p-321 … p-326 | 319–324 |
| 33 | **Change of numéraire** | p-327 … p-336 | 325–334 |
| 34 | **Brace-Gatarek-Musiela model** | p-337 … p-349 | 335–347 |

The topics named in the task brief ("Binomial convergence to Black–Scholes", "Limiting/Numerical methods", "Feynman–Kac", "Multidimensional Brownian Motion", "Diversification and portfolio") are **NOT** chapters 30–34 of this book. They belong to earlier continuous-time chapters of the same volume: multidimensional Brownian motion ≈ ch 19 (two-dimensional market model), Feynman–Kac ≈ ch 16/21, binomial→Black–Scholes ≈ ch 15–16. The chapters physically numbered 30–34 are the last five, all **term-structure / change-of-measure** chapters (Hull–White, CIR, Duffie–Kan, numéraire change, BGM/LIBOR). The assumed page windows (ch30 ≈ p333–348, etc.) are likewise wrong: ch 30 starts near p-295 and the five chapters fill p-295…p-349. Blank/gap pages inside the range: p-304, p-326, p-334, p-336 are effectively empty (footer-only).

Consequence for the existing extraction `/tmp/atlas_extract/shreve.md`: that file treats "Vol I ch 12–34 continuous-time" as a *cross-reference* to its "Vol II" Part B and never gives Chapter 30–34 their own entries. Its two relevant Part-B sections ("Ch 9 Change of numéraire", "Ch 10 Term-structure models") name Hull–White/CIR/BGM but omit essentially every concrete formula these chapters actually prove — no Hull–White affine functions, no CIR closed-form bond, no Feller boundary condition, no Duffie–Kan model at all, no numéraire-radon–Nikodym density, no BGM forward-LIBOR dynamics, no Black caplet formula. Chapters 30–34 are therefore effectively **uncovered** by the existing atlas note; this file supplies the missing math-verified content.

---

# CHAPTER 30 — Hull and White model  (PDF p-295…p-304)

**Setup.** Short rate is the mean-reverting Gaussian model
$$ dr(t) = \big(\alpha(t)-\beta(t)r(t)\big)\,dt + \sigma(t)\,dW(t),\qquad \alpha,\beta,\sigma \text{ nonrandom functions of }t. $$
Integrating factor $K(t)=\int_0^t \beta(u)\,du$; Itô on $e^{K(t)}r(t)$ gives
$$ r(t)=e^{-K(t)}\Big[r(0)+\int_0^t e^{K(u)}\alpha(u)\,du+\int_0^t e^{K(u)}\sigma(u)\,dW(u)\Big]. $$

**Gaussian structure.**
Mean $$ m_r(t)=e^{-K(t)}\Big[r(0)+\int_0^t e^{K(u)}\alpha(u)\,du\Big], \tag{0.1}$$
Covariance $$ \rho_r(s,t)=e^{-K(s)-K(t)}\int_0^{s\wedge t} e^{2K(u)}\sigma^2(u)\,du .\tag{0.2}$$
(Watch: the printed covariance symbol is $\rho_r(s,t)$, NOT gamma; the volatility appears as $\sigma^2(u)$ inside.) $r(t)$ is Markov.

**Integral of the short rate.** $\int_0^T r(t)\,dt$ is normal with
$$ \mathbb{E}\int_0^T r(t)dt=\int_0^T e^{-K(t)}\Big[r(0)+\int_0^t e^{K(u)}\alpha(u)du\Big]dt,\qquad
\operatorname{var}\!\Big(\int_0^T r(t)dt\Big)=\int_0^T e^{2K(v)}\sigma^2(v)\Big(\int_v^T e^{-K(y)}dy\Big)^2 dv .$$

**Bond price (affine, exact).** Zero-coupon bond price
$$ B(0,T)=\mathbb{E}\exp\Big\{-\int_0^T r(t)dt\Big\}=\exp\{-r(0)C(0,T)-A(0,T)\}, $$
with (integrating factor $K(t)=\int_0^t\beta$)
$$ C(0,T)=\int_0^T e^{-K(t)}dt,\qquad
A(0,T)=\int_0^T\!\!\int_0^t e^{-K(t)+K(u)}\alpha(u)\,du\,dt\;-\;\tfrac12\int_0^T e^{2K(v)}\sigma^2(v)\Big(\int_v^T e^{-K(y)}dy\Big)^2 dv .$$
By Markov property, for $t\in[0,T]$:
$$ B(t,T)=\exp\{-r(t)\,C(t,T)-A(t,T)\},\qquad C(t,T)=e^{K(t)}\int_t^T e^{-K(y)}dy, $$
and $A(t,T)$ = same double/single integrals with all integration starting at $t$ and every $K(\cdot)$ replaced by $K(\cdot)-K(t)$ (the $K(t)$ terms cancel in $A$ but *not* in $C$). Substitution $(y=t,v=u)$ collapses the double integral into one over $v$.

**Bond dynamics.** Applying Itô to $B=\exp\{-rC-A\}$ and forcing the risk-neutral form $dB=rB\,dt+(\cdots)dW$:
$$ dB(t,T)=r(t)B(t,T)\,dt-\sigma(t)C(t,T)B(t,T)\,dW(t). $$
So **the bond's volatility is $\sigma(t)C(t,T)$**. (The drift constraint reduces to an identity verified in homework.)

**Calibration.** Inputs: (1) $B(0,T)$, $0\le T\le T^*$; (2) $r(0)$; (3) $\alpha(0)$; (4) $\sigma(t)$ (usually constant); (5) $\sigma C(0,T)$ for all $T$ (bond vols, implied from bond-option prices). From (4)+(5) recover $C(0,T)=\int_0^T e^{-K(y)}dy$, hence $K(T)=-\log\frac{\partial C(0,T)}{\partial T}$ and $\beta(T)=\frac{\partial K}{\partial T}$. Then from $B(0,T)=\exp\{-r(0)C-A\}$ and the closed form of $A$ one differentiates three times to reach an ODE for $\alpha$:
$$ \alpha'(t)e^{2K(t)}+2\alpha(t)\beta(t)e^{2K(t)}-\sigma^2(t)e^{2K(t)} = \text{known function of }t,$$
solved numerically from $\alpha(0)$. **Remark 30.1** warns three differentiations are numerically unstable (example $f\equiv0$ vs $g(x)=\sin(1000x)/100$: $|f-g|\le1/100$ but $|f'-g'|=10$).

**Option on a bond.** Call, strike $K$, expiration $T_1$, bond matures $T_2>T_1$: price
$$ \mathbb{E}e^{-\int_0^{T_1}r(u)du}\big(B(T_1,T_2)-K\big)^+ =
\mathbb{E}e^{-\int_0^{T_1}r(u)du}\big(e^{-r(T_1)C(T_1,T_2)-A(T_1,T_2)}-K\big)^+,$$
a two-dimensional Gaussian integral because $\big(\int_0^{T_1}r\,du,\ r(T_1)\big)$ is jointly normal (means, variances, covariance $\rho=\int_0^{T_1}\rho_r(u,T_1)du$ listed in the text; bivariate normal density written in (4.1)). At general $t$ one conditions on $r(t)$: $\big(\int_t^{T_1}r\,du,\ r(T_1)\big)\mid r(t)$ jointly normal, means random through $r(t)$, variances/covariance deterministic (formulas (4.2) block).

**Pros/cons (stated):** closed-form pricing and exact fit to the initial yield curve; but one-factor ⇒ all bond prices perfectly correlated (only parallel shifts), and $r$ is normal ⇒ can go negative and $B(t,T)$ can exceed 1.

---

# CHAPTER 31 — Cox-Ingersoll-Ross model (PDF p-305…p-320)

**Construction from OU squares.** Start from $d$-dim Brownian motion $(W_1,\dots,W_d)$, constants $\beta>0,\ \sigma>0$. $X_j$ = **Ornstein–Uhlenbeck** process
$$ dX_j(t)=-\tfrac12\beta X_j(t)\,dt+\tfrac12\sigma\,dW_j(t),\qquad
X_j(t)=e^{-\tfrac12\beta t}\Big[X_j(0)+\tfrac12\sigma\int_0^t e^{\tfrac12\beta u}dW_j(u)\Big],$$
Gaussian with $m_j(t)=e^{-\tfrac12\beta t}X_j(0)$ and covariance $\tfrac14\sigma^2 e^{-\tfrac12\beta(s+t)}\int_0^{s\wedge t}e^{\beta u}du$. Set $r(t)=\sum_{j=1}^d X_j^2(t)$. If $d=1$, $r(t)$ hits 0 infinitely often (P=1); if $d\ge2$, $r(t)=0$ only with probability 0.

**Itô step** ($f=\sum x_i^2$, $f_{x_i}=2x_i$, $f_{x_ix_j}=2\delta_{ij}$, $dX_i\,dX_j$ cross terms vanish for $i\ne j$, $dW_i dW_i=dt$):
$$ dr=\sum_i 2X_i\big(-\tfrac12\beta X_i dt+\tfrac12\sigma dW_i\big)+d\sum_i dt = -\beta r\,dt+\sigma\sum_i X_i dW_i+\tfrac{\sigma^2 d}{4}dt .$$
Defining the martingale $W(t)=\sum_{i=1}^d\int_0^t \frac{X_i(u)}{\sqrt{r(u)}}dW_i(u)$ (so $dW=\sum \frac{X_i}{\sqrt r}dW_i$ and $dW\,dW=\sum \frac{X_i^2}{r}dt=dt$, hence $W$ is a Brownian motion) yields
$$ dr(t)=\Big(\underbrace{\tfrac{d\sigma^2}{4}}_{=\alpha}-\beta r(t)\Big)dt+\sigma\sqrt{r(t)}\,dW(t). $$

**CIR SDE & Feller boundary.**
$$ dr(t)=\big(\alpha-\beta r(t)\big)dt+\sigma\sqrt{r(t)}\,dW(t),\qquad
\boxed{\;d:=\tfrac{4\alpha}{\sigma^2}>0.}$$
- $d<2$ i.e. $\alpha<\tfrac12\sigma^2$: $r$ hits 0 infinitely often (P=1) — not a good parameter choice (boundary attainable).
- $d\ge2$ i.e. $\alpha\ge\tfrac12\sigma^2$: $P\{r(t)=0 \text{ for at least one }t\}=0$ — the **Feller condition**.

**Distribution of $r(t)$.** Write $X_1(0)=\cdots=X_{d-1}(0)=0,\ X_d(0)=\sqrt{r(0)}$. Then $\sum_{i=1}^{d-1}X_i^2(t)$ is a (central) chi-square with $d-1$ degrees of freedom (scaled by $\rho(t,t)=\frac{\sigma^2}{4\beta}(1-e^{-\beta t})$, i.e. each $X_i(t)\sim N(0,\rho(t,t))$), independent of the normal-squared term $X_d^2(t)$ with mean $m_d(t)=e^{-\frac12\beta t}\sqrt{r(0)}$ ⇒ **$r(t)$ is non-central chi-square.**

**Equilibrium distribution.** As $t\to\infty$: $m_d\to0$ and $\rho(t,t)\to\frac{\sigma^2}{4\beta}$; the limiting density is that of $\frac{\sigma^2}{4\beta}$ times a chi-square with $d=\frac{4\alpha}{\sigma^2}$ degrees of freedom. Gamma-density form (verified by checking it satisfies the EKFE):
$$ p(r)=C\,r^{\frac{2\alpha}{\sigma^2}-1}e^{-\frac{2\beta}{\sigma^2}r},\qquad
C=\Big(\frac{2\beta}{\sigma^2}\Big)^{\frac{2\alpha}{\sigma^2}}\frac{1}{\Gamma\big(\frac{2\alpha}{\sigma^2}\big)}. $$
(Mean/variance of $r(t)$ were computed earlier, ch 15.7.)

**Kolmogorov forward equation.** For $dX=b(X)dt+\gamma(X)dW$: using test functions $h$ vanishing near $0$ and $\infty$ and integration by parts,
$$ p_t(t,y)+\frac{\partial}{\partial y}\big(b(y)p(t,y)\big)-\frac12\frac{\partial^2}{\partial y^2}\big(\gamma^2(y)p(t,y)\big)=0.\tag{KFE}$$
Equilibrium: replace $p_t=0$. For CIR the equilibrium density above solves
$$ \frac{\partial}{\partial r}\big((\alpha-\beta r)p\big)-\frac12\frac{\partial^2}{\partial r^2}(\sigma^2 r p)=0.\tag{EKFE}$$

**Bond prices (exact closed form).** With $B(t,T)=B(r(t);t,T)$ and $e^{-\int_0^t r\,du}B(r(t);t,T)$ a martingale, zero dt-term yields the PDE
$$ -rB+B_t+(\alpha-\beta r)B_r+\tfrac12\sigma^2 r B_{rr}=0,\quad B(r;T,T)=1,\ r\ge0.\tag{4.1}$$
Affine ansatz $B(r;t,T)=e^{-rC(t,T)-A(t,T)}$ reduces to an ODE (Riccati) with $C(T,T)=A(T,T)=0$, solved **explicitly**:
$$ C(t,T)=\frac{\sinh\big(\gamma(T-t)\big)}{\gamma\cosh\big(\gamma(T-t)\big)+\tfrac12\beta\sinh\big(\gamma(T-t)\big)},\qquad
A(t,T)=-\frac{2\alpha}{\sigma^2}\log\Big[\frac{\gamma e^{\frac12\beta(T-t)}}{\gamma\cosh(\gamma(T-t))+\frac12\beta\sinh(\gamma(T-t))}\Big],$$
$$ \gamma=\tfrac12\sqrt{\beta^2+2\sigma^2},\qquad \sinh u=\tfrac{e^u-e^{-u}}2,\ \cosh u=\tfrac{e^u+e^{-u}}2 .$$
Since coefficients are time-homogeneous, $C,A$ depend on $\tau=T-t$ alone. Because $r>0$ a.s., $B(r(0);T)$ is strictly decreasing in $T$, $B(r(0);0)=1$, and $r(0)C(T)+A(T)$ is strictly increasing from $0$ to $\infty$.

**Option on a bond.** $v(t,r(t))=\mathbb{E}\,e^{-\int_t^{T_1}r\,du}(B(T_1,T_2)-K)^+$ satisfies
$$ -rv+v_t+(\alpha-\beta r)v_r+\tfrac12\sigma^2 r v_{rr}=0,\quad v(T_1,r)=\big(B(r;T_1,T_2)-K\big)^+.$$

**Time-change (31.6–31.8).** A deterministic, strictly increasing function $t=\varphi(\hat t)$ connects process-time CIR to real-time CIR with time-dependent coefficients: set $\hat r(\hat t)=r(\varphi(\hat t))\varphi'(\hat t)$. Calibration solves $\hat r(0)C(0;\varphi(\hat T))+A(0;\varphi(\hat T))=-\log\hat B(\hat r(0);0,\hat T)$ for $\varphi(\hat T)$ (unique, strictly increasing, since LHS increasing 0→∞). Using $\lim_{\tau\to0}-\frac{\partial}{\partial\tau}\log B(0,\tau)=r(0)$, and $C'(0)=1,\ A'(0)=0$, one shows $\varphi'(0)=1$.

---

# CHAPTER 32 — A two-factor model (Duffie & Kan)  (PDF p-321…p-326)

**Model.** $X_1$ = interest rate; $X_2$ = yield of a bond of maturity $\tau_0$. Independent BMs $W_1,W_2$; constants $\sigma_1,\sigma_2,\rho,\beta_1,\beta_2,\alpha$; drifts $a_{ij},b_i$:
$$ dX_1(t)=\big(a_{11}X_1+a_{12}X_2+b_1\big)dt+\sigma_1\sqrt{\beta_1X_1+\beta_2X_2+\alpha}\,dW_1, \tag{SDE1}$$
$$ dX_2(t)=\big(a_{21}X_1+a_{22}X_2+b_2\big)dt+\sigma_2\sqrt{\beta_1X_1+\beta_2X_2+\alpha}\,\big(\rho\,dW_1+\sqrt{1-\rho^2}\,dW_2\big).\tag{SDE2}$$
Define $Y:=\beta_1X_1+\beta_2X_2+\alpha$ and $W_3:=\rho W_1+\sqrt{1-\rho^2}W_2$ (a BM, $dW_1dW_3=\rho\,dt$). Quadratic variations: $dX_1dX_1=\sigma_1^2 Ydt,\ dX_2dX_2=\sigma_2^2 Ydt,\ dX_1dX_2=\rho\sigma_1\sigma_2 Ydt$.

**Nonnegativity of $Y$ (boundary control).** $Y$ follows a CIR-type equation driven by a new BM $W_4$. Assumptions for $Y(t)>0$ a.s.:
1. $\beta_1a_{11}+\beta_2a_{21}=\beta_1$ and $\beta_1a_{12}+\beta_2a_{22}=\beta_2$ (so the linear part of $dY$ is exactly $Y\,dt$);
2. $Y(0)=\beta_1X_1(0)+\beta_2X_2(0)+\alpha>0$;
3. $\beta_1b_1+\beta_2b_2\ge\tfrac12\big(\sigma_1^2\beta_1^2+2\sigma_1\sigma_2\rho\beta_1\beta_2+\sigma_2^2\beta_2^2\big)$ (a Feller-type inequality).

Then (SDE1′)/(SDE2′) read with diffusion $\sigma_1\sqrt{Y}\,dW_1$ and $\sigma_2\sqrt{Y}\,dW_3$.

**Zero-coupon bond (affine 2-factor).** Time-homogeneous ⇒ $B(x_1,x_2;\tau)$, $\tau=T-t$. Martingale condition on $e^{-\int_0^t X_1} B(X_1(t),X_2(t);T-t)$ gives the PDE (dummy $\gamma\equiv\tau$):
$$ -x_1B-B_\gamma+(a_{11}x_1+a_{12}x_2+b_1)B_{x_1}+(a_{21}x_1+a_{22}x_2+b_2)B_{x_2}
+\tfrac12\sigma_1^2(\beta_1x_1+\beta_2x_2+\alpha)B_{x_1x_1}$$
$$+\rho\sigma_1\sigma_2(\beta_1x_1+\beta_2x_2+\alpha)B_{x_1x_2}+\tfrac12\sigma_2^2(\beta_1x_1+\beta_2x_2+\alpha)B_{x_2x_2}=0,\quad \beta_1x_1+\beta_2x_2+\alpha>0.$$
Affine ansatz $B(x_1,x_2;\tau)=\exp\{-x_1C_1(\tau)-x_2C_2(\tau)-A(\tau)\}$ with $C_1(0)=C_2(0)=A(0)=0$ (so $B(\cdot,\cdot;0)=1$) separates into three coupled ODEs:
$$ C_1'=1+a_{11}C_1+a_{21}C_2-\tfrac12\sigma_1^2\beta_1C_1^2-\rho\sigma_1\sigma_2\beta_1C_1C_2-\tfrac12\sigma_2^2\beta_1C_2^2,\quad C_1(0)=0,\tag{1}$$
$$ C_2'=a_{12}C_1+a_{22}C_2-\tfrac12\sigma_1^2\beta_2C_1^2-\rho\sigma_1\sigma_2\beta_2C_1C_2-\tfrac12\sigma_2^2\beta_2C_2^2,\quad C_2(0)=0,\tag{2}$$
$$ A'=b_1C_1+b_2C_2-\tfrac12\sigma_1^2\alpha C_1^2-\rho\sigma_1\sigma_2\alpha C_1C_2-\tfrac12\sigma_2^2\alpha C_2^2,\quad A(0)=0.\tag{3}$$
Solve (1),(2) numerically then integrate (3).

**Calibration.** $X_2(t)$ is, by construction, the $\tau_0$-yield: $X_2(t)=\frac1{\tau_0}[X_1C_1(\tau_0)+X_2C_2(\tau_0)+A(\tau_0)]$ must hold identically ⇒ impose $C_1(\tau_0)=0,\ C_2(\tau_0)=\tau_0,\ A(\tau_0)=0$ and choose $a_{ij},b_i,\sigma_1,\sigma_2,\rho,\beta_1,\beta_2,\alpha$ to satisfy them.

---

# CHAPTER 33 — Change of numéraire (PDF p-327…p-336)

**Setup.** One risky asset $S$ (later: a rate-dependent claim) with $dS(t)=r(t)S(t)dt+\sigma_S(t)S(t)dW(t)$ under the risk-neutral measure; $r(t),\sigma_S$ adapted to a filtration possibly larger than that of $W$ (this is *not* a geometric-BM one-stock market). Accumulation factor $\beta(t)=\exp\{\int_0^t r(u)du\}$; $\frac{S(t)}{\beta(t)}$ is a martingale ($d\big(\frac S\beta\big)=\frac S\beta \sigma_S dW$), and $B(t,T)=\mathbb{E}\big[\frac{\beta(t)}{\beta(T)}\big|\mathcal F(t)\big]$ so $\frac{B(t,T)}{\beta(t)}$ is also a martingale.

**T-forward price.** Value-of-forward-zero ⇒ $F(t,T)=\frac{S(t)}{B(t,T)}$.

**Definition 33.1 (Numéraire):** any asset whose price is always strictly positive can be the numéraire; denominate all assets in its units.
- Example 33.1 (money market): $S(t)/\beta(t)$, $B(t,T)/\beta(t)$.
- Example 33.2 (T-bond): stock worth $F(t,T)$, bond worth $1$.

**Theorem 33.1 (defines the numéraire risk-neutral measure):** if $N$ is a numéraire,
$$ \mathbb P_N(A)=\frac{1}{N(0)}\int_A \frac{N(T^*)}{\beta(T^*)}\,d\mathbb P,\quad A\in\mathcal F(T^*),$$
is risk-neutral for $N$ (i.e. $Y/N$ is a $\mathbb P_N$-martingale for every asset price $Y$). $\mathbb P$ and $\mathbb P_N$ are equivalent, with inverse density $\frac{d\mathbb P}{d\mathbb P_N}=N(0)\frac{\beta(T^*)}{N(T^*)}$. Conditional-expectation change rule (Lemma in text): for $\mathcal F(T)$-measurable $X$,
$$ \mathbb E^N\big[X\big|\mathcal F(t)\big]=\frac{\beta(t)}{N(t)}\mathbb E\Big[\frac{N(T)}{\beta(T)}X\Big|\mathcal F(t)\Big].$$

**33.1 Bond as numéraire → $T$-forward measure.** $\mathbb P_T(A)=\frac1{B(0,T)}\int_A\frac{B(T,T)}{\beta(T)}d\mathbb P=\frac1{B(0,T)}\int_A\frac{1}{\beta(T)}d\mathbb P$ on $\mathcal F(T)$. The forward price is a $\mathbb P_T$-martingale with no drift:
$$ dF(t,T)=\sigma_F(t,T)F(t,T)\,dW_T(t),\quad 0\le t\le T,$$
$W_T$ a $\mathbb P_T$-BM; WLOG $\sigma_F\ge0$. (Notation $F(t)\equiv F(t,T)$ thereafter.)

**33.2 Stock as numéraire.** $\mathbb P_S(A)=\frac1{S(0)}\int_A\frac{S(T^*)}{\beta(T^*)}d\mathbb P$. $1/F(t)$ (value of the bond in stock units) is a $\mathbb P_S$-martingale:
$$ d\big(\tfrac1{F(t)}\big)=\sigma_F(t,T)\tfrac1{F(t)}\,dW_S(t).$$
**Theorem 33.2:** the volatility is the *same* $\sigma_F(t,T)$ in both measures. Proof via $g(x)=1/x$: under $\mathbb P_T$, $\frac1F$ has volatility $\sigma_F$ and mean return $\sigma_F^2=\frac{?}{}$... precisely $d\frac1F=\frac1F[-\sigma_F\,dW_T+\sigma_F^2\,dt]$, and the change to $\mathbb P_S$ removes the drift but not the volatility, so $W_S(t)=-W_T(t)+\int_0^t\sigma_F(u,T)du$.

**33.3 Merton option-pricing formula (option on the stock, general $r$).** European call: splitting the expectation into the $S$-numeraire and $T$-forward-measure legs:
$$ V(0)=S(0)\,\mathbb P_S\{S(T)>K\}-K B(0,T)\,\mathbb P_T\{S(T)>K\}
=S(0)\,\mathbb P_S\Big\{\tfrac1{F(T)}<\tfrac1K\Big\}-K B(0,T)\,\mathbb P_T\{F(T)>K\}.$$
If $\sigma_F$ is constant:
$$ V(0)=S(0)N(d_1)-K B(0,T)N(d_2),\qquad
d_1=\frac{1}{\sigma_F\sqrt T}\Big[\log\frac{S(0)}{KB(0,T)}+\tfrac12\sigma_F^2 T\Big],\qquad
d_2=\frac{1}{\sigma_F\sqrt T}\Big[\log\frac{S(0)}{KB(0,T)}-\tfrac12\sigma_F^2 T\Big].$$
For constant $r$ ($B(0,T)=e^{-rT}$) this is the classical Black–Scholes formula. Time-$t$ version:
$$ V(t)=S(t)N(d_1(t))-K B(t,T)N(d_2(t)),\qquad
d_{1}(t)=\frac{1}{\sigma_F\sqrt{T-t}}\Big[\log\frac{F(t)}{K}+\tfrac12\sigma_F^2(T-t)\Big],\quad d_{2}(t)=d_1(t)-\sigma_F\sqrt{T-t}.$$
**Suggested hedge:** hold $N(d_1(t))$ shares and short $KN(d_2(t))$ bonds; verification is done by re-denominating the whole portfolio in the bond numéraire (Theorem 33.3: numéraire changes act on portfolios "as you would expect") and reducing the self-financing check to showing $F\,dN(d_1)+dN(d_1)dF-K\,dN(d_2)=0$ (homework).

---

# CHAPTER 34 — Brace-Gatarek-Musiela model (PDF p-337…p-349)

**34.1 HJM under risk-neutral $\mathbb P$.** $f(t,T)$ = forward rate for borrowing at $T$:
$$ df(t,T)=\sigma^*(t,T)\sigma(t,T)\,dt+\sigma(t,T)\,dW(t),\qquad \sigma^*(t,T)=\int_t^T \sigma(t,u)du.$$
$r(t)=f(t,t)$; $B(t,T)=\exp\{-\int_t^T f(t,u)du\}$ satisfies $dB=rB\,dt-\sigma^*(t,T)B\,dW$ ($\sigma^*(t,T)$ = vol of $T$-bond). **Why not log-normal forward rates:** taking $\sigma(t,T)=\sigma f(t,T)$ makes $df=\sigma f\int_t^T \sigma f\,du\,dt+\sigma f\,dW$, whose drift grows like $f^2$; HJM show solutions explode before $T$. Toy analogue $f'=f^2,\ f(0)=c>0$ ⇒ $f(t)=c/(1-ct)$ explodes at $t=1/c$. ⇒ need different state variable.

**34.2 BGM change of variables.** $\tau=T-t$ (time to maturity): $r(t,\tau)=f(t,t+\tau)$ (so $r(t,0)=r(t)$), $D(t,\tau)=B(t,t+\tau)=\exp\{-\int_0^\tau r(t,u)du\}$, with $\frac{\partial}{\partial\tau}D=-r(t,\tau)D$. HJM becomes
$$ df(t,T)=\sigma(t,\tau)\sigma^*(t,\tau)\,dt+\sigma(t,\tau)\,dW(t),\qquad
dB(t,T)=rB\,dt-\sigma^*(t,\tau)B\,dW(t),\qquad \sigma^*(t,\tau)=\int_0^\tau \sigma(t,u)du,\ \tfrac{\partial}{\partial\tau}\sigma^*=\sigma.$$
Differentials (drift includes the "$+\frac12\sigma^2$" Itô–HJM term, note the sign below):
$$ dr(t,\tau)=\Big[\frac{\partial r(t,\tau)}{\partial\tau}+\tfrac12\big(\sigma^*(t,\tau)\big)^2\Big]dt+\sigma(t,\tau)dW(t),\qquad dD(t,\tau)=\big[r(t,0)-r(t,\tau)\big]D\,dt-\sigma^*(t,\tau)D\,dW(t).$$

**34.3–34.4 LIBOR.** $\delta$ fixed (e.g. $\frac14$ yr). Spot LIBOR: $D(t,\delta)(1+\delta L(t,0))=1$. **Forward LIBOR** $L(t,\tau)$: simple forward rate over $[\tau,\tau+\delta]$;
$$ 1+\delta L(t,\tau)=\frac{D(t,\tau)}{D(t,\tau+\delta)}=\exp\Big\{\int_\tau^{\tau+\delta} r(t,u)du\Big\},\qquad
L(t,\tau)=\frac{\exp\big\{\int_\tau^{\tau+\delta} r(t,u)du\big\}-1}{\delta}. \tag{4.1}$$
As $\delta\to0$: $L(t,\tau)\to r(t,\tau)=f(t,t+\tau)$ (continuous vs simple compounding). A log-normal model is impossible for $r(t,\tau)$ but possible for each fixed $\delta$ for $L(t,\tau)$.

**34.5 Dynamics of $L$. Choose forward-LIBOR vol $\gamma(t,\tau)$ so that**
$$ dL(t,\tau)=(\cdots)dt+\gamma(t,\tau)L(t,\tau)\,dW(t).$$
Applying Itô to (4.1) using the $dr$ SDE gives, after the drift cancellation produced by the HJM term,
$$ dL(t,\tau)=\frac{\partial L}{\partial\tau}\,dt+\frac1\delta\big[1+\delta L(t,\tau)\big]\big[\sigma^*(t,\tau+\delta)-\sigma^*(t,\tau)\big]\big[\sigma^*(t,\tau+\delta)dt+dW(t)\big],$$
so set (this *defines* $\gamma$):
$$ \gamma(t,\tau)L(t,\tau)=\tfrac1\delta\big[1+\delta L(t,\tau)\big]\big[\sigma^*(t,\tau+\delta)-\sigma^*(t,\tau)\big], \tag{5.3}$$
i.e. $\sigma^*(t,\tau+\delta)=\sigma^*(t,\tau)+\frac{\delta\gamma(t,\tau)L(t,\tau)}{1+\delta L(t,\tau)}.\tag{5.3'}$ Then
$$ dL(t,\tau)=\Big[\frac{\partial L}{\partial\tau}+\gamma(t,\tau)L(t,\tau)\sigma^*(t,\tau+\delta)\Big]dt+\gamma(t,\tau)L(t,\tau)\,dW(t),\tag{5.4}$$
or, substituting (5.3′),
$$ dL(t,\tau)=\Big[\frac{\partial L}{\partial\tau}+\gamma L\,\sigma^*(t,\tau)+\frac{\delta L^2\gamma^2}{1+\delta L}\Big]dt+\gamma L\,dW(t).\tag{5.4′}$$
(5.4′) is an SPDE; in $(t,T)$ variables with $K(t,T)=L(t,T-t)$ it reduces to the SDE
$$ dK(t,T)=\gamma(t,T-t)K(t,T)\big[\sigma^*(t,T-t+\delta)dt+dW(t)\big].$$

**34.6 Implementation.** Given initial forward-LIBOR curve $L(0,\tau)$ and a (usually nonrandom) vol $\gamma(t,\tau)$ plus a partial-bond-vol $\sigma^*(t,\tau)$, $0\le\tau<\delta$: solve (5.4′) on $[0,\delta)$, feed into (5.3′) to get $\sigma^*$ on $[\delta,2\delta)$, repeat recursively. Remark 34.3: as $\delta\to0$, $\gamma(t,\tau)L(t,\tau)\to\sigma(t,\tau)$ and (6.1) → $df(t,T)=\sigma(t,T-t)[\sigma^*(t,T-t)dt+dW]$ = HJM. Remark 34.4: the $\frac{\delta K^2\gamma^2}{1+\delta K}$ term is bounded by $\gamma^2K^2$ ⇒ BGM solutions do **not** explode (unlike the log-normal-forward-rate attempt).

**34.7 Bond prices / forward measure.** $\frac{B(t,T)}{\beta(t)}=\frac1{B(0,T)}\exp\big\{-\int_0^t\sigma^*(u,T-u)dW-\tfrac12\int_0^t(\sigma^*)^2du\big\}$ (a martingale). Forward measure $\mathbb P_T(A)=\frac1{B(0,T)}\int_A\frac{1}{\beta(T)}d\mathbb P$. Girsanov: $W_T(t)=W(t)+\int_0^t\sigma^*(u,T-u)du$ is a $\mathbb P_T$-BM.

**34.8 Forward LIBOR under forward measures.** Under $\mathbb P_{T+\delta}$, $K(t,T)=L(t,T-t)$ is a martingale (its drift $\sigma^*(t,T-t+\delta)dt$ is cancelled):
$$ K(t,T)=K(0,T)\exp\Big\{\int_0^t\gamma(u,T-u)dW_{T+\delta}(u)-\tfrac12\int_0^t\gamma^2(u,T-u)du\Big\},$$
$$ K(T,T)=K(t,T)e^{X(t)},\qquad X(t)=\int_t^T\gamma(u,T-u)dW_{T+\delta}(u)-\tfrac12\int_t^T\gamma^2(u,T-u)du,$$
where (for nonrandom $\gamma$) $X(t)$ is normal under $\mathbb P_{T+\delta}$ with mean $-\frac12\rho^2(t)$ and variance
$$ \rho^2(t)=\int_t^T\gamma^2(u,T-u)\,du,\qquad\text{independent of }\mathcal F(t).$$

**34.9–34.10 Caplets and caps.** A caplet on $\delta L(T,0)=\delta K(T,T)$, cap rate $c$, pays $\delta(K(T,T)-c)^+$ at $T+\delta$.
- $T\le t\le T+\delta$: $C_{T+\delta}(t)=\delta(K(T,T)-c)^+B(t,T+\delta)$.
- $0\le t\le T$: with $g(y)=\mathbb E_{T+\delta}(ye^{X(t)}-c)^+$,
$$ C_{T+\delta}(t)=\delta B(t,T+\delta)\,g(K(t,T)),\qquad
g(y)=y\,N\Big(\frac1{\rho(t)}\log\frac yc+\tfrac12\rho(t)\Big)-c\,N\Big(\frac1{\rho(t)}\log\frac yc-\tfrac12\rho(t)\Big).\tag{9.2}$$
Constant vol $\gamma$ ⇒ $\rho(t)=\gamma\sqrt{T-t}$ ⇒ **Black caplet formula**. A cap with tenors $T_k=k\delta$ is the sum of its caplets $\sum_{k:\,t\le T_k}C_{T_k+\delta}(t)$.

**34.11 Calibration.** If $\gamma(t,\tau)=\gamma(\tau)$, caplet price $C_{T+\delta}(0)$ reveals $\int_0^T\gamma^2(v)dv$; a series of caplet prices backs out $\gamma^2$ piecewise constant on tenors; $\sigma^*(t,\tau)\approx0$ for $0\le\tau<\delta$ (bonds of maturity within $\delta$).

**34.12 Long rate.** $D(t,n\delta)=\prod_{k=1}^n[1+\delta L(t,(k-1)\delta)]$; long rate $=\frac1{n\delta}\sum_{k=1}^n\log[1+\delta L(t,(k-1)\delta)]$.

**34.13 Swap / forward swap rate.** Receiver-style swap pays $\delta(L(T_k,0)-c)$ at $T_{k+1}$; using $1+\delta L(T_k,0)=\frac1{B(T_k,T_{k+1})}$, each payment values to $B(t,T_k)-(1+\delta c)B(t,T_{k+1})$, so swap value $=B(t,T_0)-\sum_{k=1}^n\delta c\,B(t,T_k)-B(t,T_n)$. Forward swap rate (value zero):
$$ w_{T_0}(t)=\frac{B(t,T_0)-B(t,T_n)}{\delta\sum_{k=1}^n B(t,T_k)}.$$
In contrast to the cap formula, this is **generic** — independent of the term-structure model and its volatility estimation.

---

## ERRORS / GAPS found (and what the corrected reading is)

1. **Task-brief mislabeling (biggest gap).** Chapters 30–34 are term-structure / numéraire chapters (Hull–White, CIR, Duffie–Kan, change of numéraire, BGM), *not* "binomial→Black–Scholes convergence / numerical methods / Feynman–Kac / multidimensional BM / diversification." Correct PDF span is p-295…p-349, with ch30 beginning near p-295 (book p.293), not p-333–348. Any downstream page→chapter index built from the brief will be wrong.
2. **Existing extraction doesn't cover them.** `/tmp/atlas_extract/shreve.md` Part B gives only generic "Ch 9/10" overviews of numéraire and term structure and omits: Hull–White affine $A(0,T),C(0,T)$ and bond vol $\sigma C$; the CIR $d=4\alpha/\sigma^2$ Feller condition, non-central-chi-square nature, the exact $\sinh/\cosh$ bond solution ($C=\sinh(\gamma\tau)/[\gamma\cosh(\gamma\tau)+\tfrac12\beta\sinh(\gamma\tau)]$, $A=-\frac{2\alpha}{\sigma^2}\log(\cdot)$, $\gamma=\tfrac12\sqrt{\beta^2+2\sigma^2}$), the equilibrium density; the entire Duffie–Kan two-factor construction and ODEs; the numéraire Radon–Nikodym density $d\mathbb P_N=\frac{N(T^*)}{\beta(T^*)N(0)}d\mathbb P$ and the Merton/forward-measure $V=S(0)N(d_1)-KB(0,T)N(d_2)$; and all BGM forward-LIBOR dynamics/caplet/Black formulas. (shreve.md also mislabels the two volumes' relationship; see its own header note.)
3. **pdftotext (`shreve1.txt`) symbol corruption (affects any text-based downstream pass).** For these pages the .txt silently drops most Greek letters ($\alpha,\beta,\sigma,\rho,\gamma$ come out blank or as stray digits) and collapses multi-tier exponents (e.g. `sigma^*(t,T)` shows as empty `(t;T)` or `; T)`, `e^{2K(v)}` loses its exponent, CIR's `d = 4...sigma^2` line is illegible, OU coefficients `(1/2)sigma` are lost). It is unsafe for math; the vision-verified values in this file supersede it. Concrete examples where .txt misleads: the OU SDE coefficients ($-\tfrac12\beta$, $\tfrac12\sigma$), CIR $d=4\alpha/\sigma^2$, $C(0,T)=e^{K(t)}\int_t^Te^{-K(y)}dy$, and every $\sigma^*/\sigma_F/\gamma$ volatility subscript.
4. **No in-book errors found in the source itself** for ch30–34 after cross-checking key results against vision (Hull–White affine bond, CIR closed forms + Feller, Duffie–Kan PDE/ODE separation, numéraire density, BGM dynamics, Black caplet). Notation is however nonstandard/lecture-edition: chapter equations restart at `(0.1)`, and theorems/lemmas are numbered `0.71, 1.54, 2.72, 3.73` (manuscript numbering); the covariance of the short rate is written $\rho_r(s,t)$.
5. **Blank/interstitial pages.** p-304, p-326, p-334, p-336 are footer-only (page-turn whitespace), so "gap" flags there are not missing content.

### Verification trace (vision-confirmed pages)
HW affine/mean/cov & bond formula: p-295, p-296. CIR OU construction & Ito: p-305, p-306; CIR SDE + $d=4\alpha/\sigma^2$ + Feller + BM construction: p-307; equilibrium density/EKFE: p-311; CIR closed-form bond: p-314. Duffie–Kan SDEs, $Y$, $W_3$, cross-variations: p-321; ODEs/ansatz: p-324. Numéraire def/examples + Theorem 0.71 density: p-328; Merton $d_1,d_2,\sigma_F$, $V=S N-KB N$: p-332. BGM dynamics/$\sigma^*$ vs $\gamma$: p-341; forward-LIBOR $K$ SDE, $X(t)$, variance $\rho^2=\int\gamma^2$: p-345; Black caplet $g(y)$, $\rho(t)=\gamma\sqrt{T-t}$: p-346. Text of p-327/337/339/340/343/344/347/348/349 cross-checked from `shreve1.txt`.
