# Gatheral — *The Volatility Surface* (2006) — VERIFIED EXTRACTION: Chapters 6–10

**Source PDF (NOT modified):** `/home/alfred/local-repos/kwant-atlas/corpus/titles/refs/pillar3/Gatheral_2006_volatility_surface.pdf`
**Rendered pages:** `/tmp/atlas_pages2/gatheral/p-NNN.png` (210 pages).
**Extraction method:** pdftotext text layer + vision cross-checks on the densest formula pages
(p-121 = Medvedev–Scaillet (7.5), p-127 = Lewis (7.12), p-125 = jumps (7.9)).

**IMPORTANT — chapter/topic mismatch with the parent brief.** The brief described ch6–10 as "The Heston
model; Volatility and jumps; The volatility surface and time series; Black-Scholes and beyond; Summary."
**That does NOT match this book.** Gatheral's actual ch6–10 are:
**Ch6 Modeling Default Risk, Ch7 Volatility Surface Asymptotics, Ch8 Dynamics of the Volatility Surface,
Ch9 Barrier Options, Ch10 Exotic Cliquets** (the Heston model is Ch2, adding jumps is Ch5, and the vol
surface is Ch3; there is no "Black-Scholes and beyond" chapter and **no summary/conclusion chapter and no
appendices** in this 2006 volume). Ch11 (Volatility Derivatives) is the final chapter but was outside this
assignment's 6–10 range. I extracted the *actual* ch6–10. The brief's "approx PDF 111–210" is also off:
**actual ch6–10 = PDF 105–163** (printed pp.74–132); Ch11 spans PDF 164–210.

**Verified page map** (0-indexed page n ⇒ PDF page n+1): Ch6 title=PDF 105, Ch7=118, Ch8=132, Ch9=138,
Ch10=153, Ch11=164. So Ch6 = PDF 105–117, Ch7 = 118–131, Ch8 = 132–137, Ch9 = 138–152, Ch10 = 153–163.

**Formula verification status.** The pdftotext layer is faithful for nearly all display equations and was
confirmed by direct vision reads on the ambiguous ones. Three places where the text layer dropped or
corrupted glyphs were resolved by vision: **(7.5)** has ρ² (not ρ) in the z² coefficient; the **Lewis (7.12)**
block has J⁽²⁾/t and η/(vt²)·J⁽¹⁾ (the text layer had spurious factors of 2); and the **jump formula (7.9)**
and the **CreditGrades survival probability** are given as best-effort reconstructions and are
**[RECONSTRUCTED]** — flagged inline, verify against the original papers (Medvedev–Scaillet 2004; Lewis 2000;
Finger 2002) if used as an exact reference.

---

## CHAPTER 6 — Modeling Default Risk (printed 74–86; PDF 105–117)

Central claim: for *single stocks*, the single most direct explanation of the volatility skew is **default
risk**. High credit spreads ⇒ extreme implied-volatility skews.

### 6.1 Merton's model of default (jump-to-ruin) — printed 74–76
Two model families: **structural** (default when an economic variable, e.g. firm value, hits a barrier; H-W and
CreditGrades) vs **reduced-form** (default is a random event with intensity; Duffie–Singleton). Merton (1974) is
the simplest reduced-form model: the stock jumps to zero with **hazard rate** λ(t), independent of the stock
process.

Contingent claims then satisfy the jump-diffusion valuation equation (5.3) with E[J]=0. For a call, V(JS,t)=0,
giving the **jump-to-ruin valuation equation**:
```latex
\frac{\partial V}{\partial t} + \tfrac12 \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV - \lambda(t)\Bigl(V - S \frac{\partial V}{\partial S}\Bigr) = 0  \tag{6.1}
```
i.e. exactly the **Black–Scholes equation with interest rate shifted to r + λ**. A call is worth the BS formula
with the risky rate. With zero recovery, the risky zero-coupon bond price is
```latex
B(t,T) = \exp\Bigl(-\!\int_t^T \bigl(r(s)+\lambda(s)\bigr)\,ds\Bigr)
```
The "shifted rate" r+λ is identified with the yield (risk-free rate + **credit spread**) of a risky bond.
Intuition: hedging with *risky* bonds keeps the replicating portfolio self-financing even through the jump to
ruin (bond and stock both jump to zero); hedging with risk-free bonds yields a windfall on default (call and
stock worthless, risk-free bonds fully recovered) in exchange for foregone carry.

**Implication for the skew:** BS implied vols are computed with the risk-free rate, but Merton prices calls with
the risky rate ⇒ this *induces* a downside skew that grows extreme as credit spreads rise. Fig. 6.1 (printed
76): 3-month implied vols at stock vol 20% for credit spreads 100/200/300 bp — downside skew is steep.

### 6.2 Capital structure arbitrage — printed 77–79
**Put-call parity across counterparties.** A put written *by the issuer* is worthless at default (zero
recovery) ⇒ valued with the risky rate. A put written by a *default-free* counterparty (e.g. an exchange) is
worth the strike at default. Denote risk-free/issuer values by subscripts 0/I; risk-free and issuer-written
*calls* have equal value (an issuer cannot default on its own stock). Result:
```latex
P_0 = C_0 + KB_0 - S = C_I + KB_0 - S = P_I + S - KB_I + KB_0 - S = P_I + K(B_0 - B_I)
```
With maturity-independent rates/spreads at t=0:
```latex
B_0 - B_I = e^{-rT}\bigl(1 - e^{-\lambda T}\bigr)
```
= discounted probability of default × strike. The risk-free put exceeds the risky put exactly by this amount —
i.e. the payoff of a **default put** in the credit-derivatives market.

**The arbitrage:** when equity-option market makers underpriced the default-induced skew, traders bought the
exchange-listed equity option and sold a default put, locking in risk-free profit. Later the trade reversed
via put spreads (e.g. buy one ATM put, sell two puts struck at ½·S — Fig. 6.2, positive payoff ⇒ pure
arbitrage if tradable flat/for credit). Table 6.1 (printed 79): one-year, 0.5-strike, ATM vol 20%:
lower bound (PV of strike × default prob) and upper bound (½ × ATM option = 0.0398 in each case) as function of
credit spread.

### 6.3 Local and implied volatility in the jump-to-ruin model — printed 79–81
Local volatility formula (1.6) from Ch1:
```latex
\sigma_{loc}^2(K,T,S) = \frac{\partial C/\partial T}{\tfrac12 K^2\, \partial^2 C/\partial K^2}  \tag{6.2}
```
Using BS linear homogeneity of C in (S,K), `K²∂²C/∂K² = S²∂²C/∂S²`, and the jump-to-ruin PDE in K, one gets
(zero rates/dividends; σ = diffusion vol, λ = hazard rate):
```latex
\sigma_{loc}^2(K,T,S) = \sigma^2 - \lambda \frac{K\,\partial C/\partial K}{\tfrac12 K^2 \partial^2 C/\partial K^2}
                     = \sigma^2 + 2\lambda\sigma\sqrt{T}\, \frac{N(d_2)}{N'(d_2)}
```
```latex
\text{with}\quad d_2 = \frac{\log(S/K) + \lambda T}{\sigma\sqrt{T}} - \frac{\sigma\sqrt{T}}{2}
```
For very low strikes K/S ≪ 1 (d₂ ≪ 0 ⇒ N(d₂) ≈ 1, N′(d₂)=(1/√(2π))e^{−d₂²/2}):
```latex
\sigma_{loc}^2(K,T,S) \approx \sigma^2 + 2\lambda\sigma\sqrt{T}\,\sqrt{2\pi}\; e^{+d_2^2/2}
```
Because implied variance is a gamma-weighted average of local variances (Ch3), implied vol in the jump-to-ruin
model rises very fast as strike decreases from ATM and flattens to σ for high strikes — unlike the
stochastic-vol case (which also produces a positive right wing). Fig 6.3 (λ=0.05, σ=0.2): local-variance
surface exploding at low strikes.

### 6.4 Effect of default risk on option prices — printed 82–83
Empirical fit to Jan-05 options on **GT (Goodyear)** as of Oct 20, 2004 (GT at 9.40): best-fit Merton
parameters **λ = 0.01934, σ = 0.3946**. Table 6.2 compares bid/ask vols to Merton vols (e.g. strike 2.50:
Merton 145.2% vs bid 147.2%/ask ~; strike 10.00 (≈ATM): 38.1–45.0% vs Merton 43.1%). The Merton model fits the
**left wing** of the skew very well (Fig 6.4) but generates no right wing — the flat right wing reflects the
model's deterministic-volatility assumption, whereas the empirically observed positive right wing reflects
uncertainty in the future level of volatility. Realism check: zero-coupon price `P_t = e^{−λt}R + (1−e^{−λt})`,
with Bloomberg recovery R=0.4 gives credit spread c = 4.58% (vs GT's 5-yr CDS >5%). Main point: **most of the
skew for high-credit-spread stocks is default risk.**

### 6.5 The CreditGrades model (structural) — printed 84–86
Prototypical structural model: equity is a BS call on firm value V (Black–Scholes 1973 / Merton 1974). As V
falls, leverage rises ⇒ stock volatility rises ⇒ a skew. Problem: no significant *short-dated* credit spreads,
because V has too little time to diffuse to a fixed barrier. Finkelstein (2002)/Lardy (2002) fix this by making
the **default barrier uncertain** (lognormal).

**Setup:** `dV_t/V_t = σ dW` (driftless GBM). Default level is `L̄D` where D = debt per share, L̄ = mean recovery;
the recovery is lognormal:
```latex
L D = \bar{L} D\, e^{\lambda Z - \lambda^2/2}, \qquad Z \sim N(0,1),\ Z \perp W
```
**Survival probability.** Define
```latex
X_t := \sigma W_t - \lambda Z - \frac{\sigma^2 t}{2} - \frac{\lambda^2}{2}
\quad\Rightarrow\quad
\mathbb{E}[X_t] = -\frac{\sigma^2}{2}\Bigl(t + \frac{\lambda^2}{\sigma^2}\Bigr),\quad
\operatorname{Var}[X_t] = \sigma^2\Bigl(t + \frac{\lambda^2}{\sigma^2}\Bigr)
```
X is approximated by a Brownian motion X̂ with drift −σ²/2 and variance σ², started at 0 at time
`−Δt := −λ²/σ²` (moment-matching). Default occurs when `V_0 e^{σW_t−σ²t/2} = L̄D e^{λZ−λ²/2}`, i.e.
`X_t = log(LD/V_0) − λ²`. Survival probability is the hitting probability of a drifting BM, a BS-like formula:
```latex
P_t = N\Bigl(-\frac{A_t}{2} + \frac{\log d}{A_t}\Bigr) - d\, N\Bigl(-\frac{A_t}{2} - \frac{\log d}{A_t}\Bigr)
      \qquad d := \frac{V_0 e^{\lambda^2}}{L D},\quad A_t^2 := \sigma^2 t + \lambda^2
```
*(slightly garbled in the text layer; reconstructed — check the digitization/Finger 2002.)* P_t can be estimated
directly from bond/CDS prices (term structure of survival probability).

**Equity volatility.** `V ≈ LD + S` (neglecting option time value), so
```latex
\sigma \sim \frac{\delta V}{V} \approx \frac{\delta S}{S + LD} = \frac{\delta S}{S}\,\frac{S}{S+LD} \sim \sigma_S\,\frac{S}{S+LD}
```
As S rises (σ fixed) stock vol σ_S falls; as S → 0, σ_S grows like 1/S — the structural explanation of the skew.

**Calibration (6.3), in market observables:**
```latex
P_t = N\Bigl(-\frac{A_t}{2} + \frac{\log d}{A_t}\Bigr) - d\,N\Bigl(-\frac{A_t}{2} - \frac{\log d}{A_t}\Bigr)
```
```latex
d = \frac{S_0 + \bar{L}D}{L D}\,e^{\lambda^2}, \qquad
A_t^2 = \sigma_{S^*}^2\Bigl(\frac{S^*}{S^* + \bar{L}D}\Bigr)^2 t + \lambda^2
```
where S* is a reference stock price and σ_{S*} the stock vol there (σ rewritten via the equity-vol relation).
In Finger (2002) L̄ and λ come from historical recovery data, D from the balance sheet; the model links credit
spreads explicitly to the volatility skew.

---

## CHAPTER 7 — Volatility Surface Asymptotics (printed 87–100; PDF 118–131)

Question: how much does the vol-surface shape depend on the precise dynamics? Answer: **all SV-with-jumps
models generate essentially the same surface shape** — you cannot infer the specific volatility dynamics from a
single snapshot of the surface. The shape is (to first order) model-independent.

### 7.1 Short expirations — printed 87–89
Rewrite the generic SV SDEs (1.1)/(1.2) in log-moneyness `x := log(F/K)`, risk-neutral, with α, β independent
of S and t:
```latex
dx = -\frac{v}{2}\,dt + \sqrt{v}\,dZ_1
dv = \alpha(v)\,dt + \eta\, v^{\beta(v)}\, dZ_2 \tag{7.1}
```
With `dZ_2 = \rho\,dZ_1 + \phi\,dZ_1^*`, `\phi=\sqrt{1-\rho^2}`, eliminating `\sqrt{v}\,dZ_1`:
```latex
dv = \alpha(v,t)\,dt + \rho\eta\,\beta(v,t)\Bigl(dx + \frac{v}{2}dt\Bigr) + \phi\eta\,\beta(v)\sqrt{v}\,dZ_1^*
```
so `E[v+dv\,|\,dx] = v + \alpha(v)dt + \rho\eta\beta(v)(dx + (v/2)dt)`. For short times (α, β slowly varying):
```latex
v_{loc}(x,t) = \mathbb{E}[v_t\,|\,x_t=x] \approx v_0 + \Bigl(\alpha(v_0) + \frac{\rho\eta\beta(v_0) v_0}{2}\Bigr) t + \rho\eta\beta(v_0)\, x \tag{7.2}
```
The x-coefficient (skew slope) agrees with Lee (2001).

**Lemma: the local-volatility skew is twice as steep as the implied-volatility skew for short expirations.**
Proof: BS implied *total* variance is the integral of local variance along the most-probable path (≈ straight
line, Fig 7.1); since the local-variance slope is ~constant β(v₀), the average is half the slope:
```latex
\sigma_{BS}^2(k,T) \approx \frac{1}{T}\int_0^T v_{loc}(\tilde x_t,t)\,dt
  \approx \text{const} + \frac12\, \rho\eta\beta(v_0)\, x_T
```
Hence the **short-dated implied-variance skew**:
```latex
\frac{\partial}{\partial x}\sigma_{BS}(x,t)^2 = \frac{\rho\eta}{2}\,\beta(v_0) \tag{7.3}
```
For Heston (β(v)=1) this reproduces the earlier short-dated Heston skew.

### 7.2 The Medvedev–Scaillet result — printed 89–91
Perturbation expansion in small time τ with fixed normalized log-strike `z := k/(\sigma_{BS}(k,\tau)\sqrt{\tau})`,
for a diffusion
```latex
\frac{dS_t}{S_t} = \sigma_t dZ_1, \qquad d\sigma_t = a(\sigma_t)dt + b(\sigma_t)dZ_2 \tag{7.4}
```
Implied volatility (with σ = σ₀) has the short-term expansion
```latex
I(z,\tau,\sigma) = \sigma + I_1(z;\sigma)\sqrt{\tau} + I_2(z;\sigma)\,\tau + O(\tau\sqrt{\tau})
```
```latex
I_1(z;\sigma) = \frac{\rho\, b(\sigma)\, z}{2}
```
```latex
I_2(z;\sigma) = \frac16\Bigl\{\frac{b(\sigma)^2(1-\rho^2)}{\sigma} + \rho^2 b(\sigma)\,\partial_\sigma b(\sigma)\Bigr\}z^2
              + \frac{a(\sigma)}{2} + \frac{\rho\,\sigma\, b(\sigma)}{4} + \frac{1}{24}\frac{\rho^2 b(\sigma)^2}{\sigma}
              + \frac{1}{12}\frac{b(\sigma)^2}{\sigma} - \frac16 \rho^2 b(\sigma)\,\partial_\sigma b(\sigma) \tag{7.5}
```
*(ρ² verified by vision on p-121.)* Note: the limit of I as k→0 and τ→0 is the **instantaneous volatility σ** —
so even though instantaneous vol is unobservable, in liquid markets the surface is smooth enough to extrapolate
to the (τ=0, ATM) limit. Substituting `z = k/(I\sqrt{\tau})` and taking τ→0:
```latex
\left.\frac{\partial I}{\partial k}\right|_{k=0} \to \frac{\rho\, b(\sigma)}{2\sigma} \tag{7.6}
```
i.e. proves (7.3). The short-dated skew is **not explicitly time-dependent** — it depends only on the form of the
SDE for volatility. By contrast local-vol models imply short-dated skews that decay with time ⇒ forward-starting
options (strikes set later) cannot be priced identically by an SV and a LV model that both match today's
European options — their *dynamics* differ even if their *statics* match. This motivates a "wild generalization":
all SV models give the same skew up to the factor β(v), for all τ ≥ 0.

**The SABR model** (Hagan, Kumar, Lesniewski, Woodward 2002):
```latex
dS_t = \sigma_t S_t^{\beta} dZ_1, \qquad d\sigma_t = \chi\,\sigma_t\, dZ_2, \qquad dZ_1 dZ_2 = \rho\,dt
```
No mean reversion ⇒ good only for short expirations, but has an exact smile formula in the limit τ→0 (used to
fit α, β, ρ). For β=1 (lognormal SABR), formula (2.17a) reduces to:
```latex
\sigma_{BS}(k) = \sigma_0\, \frac{y}{f(y)}\, \Bigl(1 + \frac14 \rho\,\chi\,\sigma_0 + \frac{2-3\rho^2}{24}\chi^2 \tau + O(\tau^2)\Bigr) \tag{7.7}
```
```latex
y := -\chi\,\frac{k}{\sigma_0},\qquad f(y) := \log\!\Bigl(\frac{\sqrt{1-2\rho y + y^2} + y - \rho}{1-\rho}\Bigr)
```
The formula factorizes (one factor in y, one in τ). Taylor expansion (y ∼ √τ):
```latex
\sigma_{BS}(k,\tau) = \sigma_0\Bigl(1 - \tfrac12\rho y + \frac{2-3\rho^2}{12}y^2\Bigr)
    + \Bigl(\tfrac14\rho\chi\sigma_0 + \frac{2-3\rho^2}{24}\chi^2\Bigr)\tau + O(\tau\sqrt{\tau})
```
Substituting a(σ)=0, b(σ)=χσ₀ into (7.5) reproduces this exactly ⇒ **MS formula (7.5) and SABR agree for small
τ.** SABR implies `∂σ_BS/∂k|_{k=0} = ρ/2`, the special case of (7.6) with β(v)=√v and η=2χ (Ito on v=σ² gives
`dv = χ²v dt + 2χv dZ`).

### 7.3 Including jumps — printed 93–94 **[RECONSTRUCTED]**
SV-with-jumps model:
```latex
\frac{dS_t}{S_t} = \sigma_t dZ_1 + J(\sigma_t)\,dq_t, \qquad d\sigma_t = a(\sigma_t)dt + b(\sigma_t)dZ_2 \tag{7.8}
```
dq = Poisson process with intensity λ_J(σ_t); J is (−1,∞)-valued with density f; compensator
`μ_J = λ_J ∫_{-1}^{∞} x f(x)dx`. Jumps in volatility contribute nothing to the surface shape for very short
expirations. Short-dated implied vols:
```latex
I(z,\tau,\sigma) = \sigma + \tilde I_1(z;\sigma)\sqrt{\tau} + \tilde I_2(z;\sigma)\,\tau + O(\tau\sqrt{\tau})
```
```latex
\tilde I_1(z;\sigma) = I_1(z;\sigma) - \mu_J g(z) + \eta_J h(z)
```
```latex
\tilde I_2(z;\sigma) = I_2(z;\sigma) + \frac{1}{2\sigma}\bigl[\mu_J g(z) - \eta_J h(z)\bigr] z^2
      - \Bigl[\frac{\mu_J \sigma}{2} - \sigma\lambda_J + \frac{\mu_J^2}{\sigma} + \frac{\mu_J b(\sigma)\rho}{2\sigma}\Bigr] g(z)\, z
      - \Bigl[\frac{\eta_J \sigma}{2} + \sigma\chi_J - \frac{\mu_J\eta_J}{\sigma} - \frac{\eta_J b(\sigma)\rho}{2\sigma}\Bigr] h(z)\, z
      + \frac{\rho b(\sigma)\mu_J}{2\sigma} - \frac{\rho\,\partial_\sigma b(\sigma)\,\mu_J}{2}
      + \frac{\mu_J^2}{2\sigma} - \frac{\sigma\mu_J}{2} - \lambda_J\sigma \tag{7.9}
```
```latex
\text{where}\quad
\eta_J = \lambda_J\int_0^\infty x\,f(x)\,dx\ \ (\text{positive part of jump compensator}),\qquad
\chi_J = \lambda_J\int_0^\infty f(x)\,dx\ \ (\text{probability of an upward jump}),
```
```latex
g(z) = \frac{N(-z)}{N(z)},\qquad h(z) = \frac{1}{N(z)}
```
*(Formula (7.9) is the most heavily garbled block in the text layer; the structure above is reconstructed and
the definitions of g,h and the companion claim in the corollary "g(0)=1, h(0)=0" appear internally
inconsistent (if N is the CDF, h(0)=2, not 0) — treat as reconstructed and verify against Medvedev–Scaillet
(2004).)* All jump terms vanish when there are no jumps.

**Corollaries (limiting skews, τ→0):**
- Jump-diffusion (deterministic vol): `∂I/∂k|_{k=0} → −μ_J/σ`.
- SVJ model: `∂I/∂k|_{k=0} → ρb(σ)/(2σ) − μ_J/σ`.
- Variance skew: `∂v_BS/∂k|_{k=0} → ρ\,b(σ) − 2\mu_J` — jump and SV effects on the ATM variance skew are
  **exactly additive at τ=0**.

### 7.4 Long expirations: Fouque–Papanicolaou–Sircar — printed 95–96
FPS (1999, 2000): in any SV model with mean-reverting volatility, for long-dated options the BS implied vol is
well approximated by a function of log-moneyness and T. For log-OU volatility:
```latex
dx = -\frac{\sigma^2}{2}dt + \sigma\,dZ_1, \qquad
d\log\sigma = -\lambda[\log\sigma - \log\bar\sigma]dt + \xi\,dZ_2
```
the skew slope (for large λT) is:
```latex
\frac{\partial}{\partial x}\sigma_{BS}(x,T) \approx \frac{\rho\,\xi}{\lambda T} \tag{7.10}
```
Translating to variance terms: dv ∼ 2σdσ = 2ξv dZ₂ ⇒ ηβ(v) = 2ξ√v, so
```latex
\frac{\partial}{\partial x}\sigma_{BS}(x,T)^2 \approx \frac{2\rho\xi\sqrt{v}}{\lambda T} = \frac{\rho\,\eta\,\beta(v)}{\lambda T}
```
matching the Heston skew (β=1) for large λT.

### 7.5 The natural interpolation (short↔long) — printed 96
Plausible interpolation between the short- and long-expiration skews (the Heston form from Ch3):
```latex
\frac{\partial}{\partial x}\sigma_{BS}(x,T)^2 \approx
  \frac{\rho\eta\beta(v)}{\lambda' T}\Bigl(1 - \frac{1 - e^{-\lambda' T}}{\lambda' T}\Bigr) \tag{7.11}
\qquad\text{with}\quad \lambda' = \lambda - \tfrac12 \rho\eta\beta(v)
```

### 7.6 Small volatility of volatility: Lewis — printed 96–97
Lewis (2000) perturb in the vol-of-vol η (assumed small) in any SV model of form (7.1). Equation (3.14), p.143:
```latex
v_{BS}(k,t) = \beta_0(v,t) + \beta_1(v,t)\,k + \beta_2(v,t)\,k^2 + O(\eta^3) \tag{7.12}
```
```latex
\beta_0(v,t) = v + \frac{1}{2}\frac{\eta}{t}J^{(1)} +
   \eta^2\Bigl[\frac{J^{(2)}}{t} - \frac12\frac{J^{(3)}}{v\,t^2}\bigl(1+\tfrac14 vt\bigr)
   - \frac{J^{(4)}}{v\,t^2}\bigl(1-\tfrac14 vt\bigr)
   + \frac{(J^{(1)})^2}{v^2 t^3}\bigl(\tfrac34 + \tfrac1{16} vt\bigr)\Bigr]
```
```latex
\beta_1(v,t) = \frac{\eta}{v\,t^2}J^{(1)} +
   \eta^2\Bigl[-\frac{J^{(4)}}{v\,t^2} - \frac{(J^{(1)})^2}{v^2 t^3}\Bigr]
```
```latex
\beta_2(v,t) = \eta^2\Bigl[\frac12\frac{J^{(3)}}{v^2 t^3} + \frac{J^{(4)}}{v^2 t^3} - \frac54\frac{(J^{(1)})^2}{v^3 t^4}\Bigr]
```
*(These exact β-formulas were taken from a vision read of p-127 and resolve factors of 2/denominators that the
text layer corrupted; J⁽²⁾ is absent from β₁,β₂. Verify against Lewis (2000) eq. (3.14) if used as exact.)*
Example 4 (p.144): `dv = -λ(v-\bar v)dt + η v^\phi dZ`, in the case v = v̄ (here v̄ = v):
```latex
J^{(1)} = v^{1/2+\phi}\,t\,\frac{\rho}{\lambda}\Bigl(1 - \frac{1-e^{-\lambda t}}{\lambda t}\Bigr)
```
```latex
J^{(3)} = \frac{\rho\, v^{2\phi}}{2\lambda^3}\Bigl(\frac32 + \lambda t + 2e^{-\lambda t} - \frac12 e^{-2\lambda t}\Bigr)
```
```latex
J^{(4)} = \frac{\rho^2 v^{2\phi}}{\lambda^3}\Bigl(\frac12 + \phi\bigl[-2 + \lambda t + (2+\lambda t)e^{-\lambda t}\bigr]\Bigr)
```
Substituting into (7.12):
```latex
\left.\frac{\partial v_{BS}}{\partial k}\right|_{k=0}
   = \frac{\rho\eta\, v^{\phi-1/2}}{\lambda t}\Bigl(1 - \frac{1-e^{-\lambda t}}{\lambda t}\Bigr) + O(\eta^2)
```
which is **exactly (7.11) to first order in η** — so (7.11) is not merely plausible but exactly correct to O(η).

### 7.7 Extreme strikes: Roger Lee — printed 97–99
Lee (2004): implied variance is bounded above by a function **linear in |k|** as |k|→∞, with the gradients of
the wings related to the maximal finite moments of the underlying. Let
```latex
q^* := \sup\{q : \mathbb{E}[S_T^{-q}] < \infty\}, \qquad
\beta^* := \limsup_{k\to -\infty}\frac{\sigma_{BS}(k,T)^2 T}{|k|}
```
Then β* ∈ [0,2] and `q^* = \frac{1}{2}(1/\sqrt{\beta^*} - \sqrt{\beta^*}/2)^2`; inverting, `β^* = g(q^*)` with
```latex
g(x) = 2 - 4\bigl(\sqrt{x^2 + x} - x\bigr)
```
Similarly for the right wing with `p^* := \sup\{p: \mathbb{E}[S_T^{1+p}] < \infty\}` and
`α^* := \limsup_{k\to +\infty}\sigma_{BS}^2 T/|k|`; `α^* = g(p^*)`. Assumes only existence of a martingale measure —
**completely model independent.**

Benaim–Friz (2006): under mild tail conditions the limsup becomes a true limit, giving full tail behaviour
(not just the upper bound). With F = CDF of returns x:
```latex
\frac{\sigma_{BS}(k,T)^2\,T}{k} \sim g\Bigl(-1 - \frac{\log[1-F(k)]}{k}\Bigr) \quad (k\to\infty) \tag{7.13}
```
```latex
\frac{\sigma_{BS}(-k,T)^2\,T}{k} \sim g\Bigl(\frac{-\log F(-k)}{k}\Bigr) \quad (k\to\infty) \tag{7.14}
```
and in most models `q^* = \lim_{k\to\infty} -\log F(-k)/k`, `p^* = \lim_{k\to\infty} (-1 - \log[1-F(k)]/k)`.
**BS example:** `1-F(k) \sim (1/\sqrt{2\pi})\,e^{-k^2/(2\sigma^2 T)}/k`, so `σ_BS² T/k ∼ g(−1+k/(2σ²T)) ∼ 2σ²T/(2k)`,
giving `σ_BS(k,T)² ∼ σ²` — trivially the flat BS smile, and the full Benaim–Friz result recovers the whole tail
(whereas the pure limsup would not exclude e.g. k/log k growth).
**SV models:** Drăgulescu–Yakovenko (2002) find the Heston CDF tail is linear in |k|, so (via Benaim–Friz) the
implied-variance tail is linear in |k| — a generic feature of SV models.

### 7.8 Asymptotics in summary — printed 100
**The general shape of the volatility surface does not depend much on the model.** Any SV-with-jumps model
generates a similar surface for appropriate parameter values. This is the chapter's core takeaway and the
rationale for the rest of the book's model-comparison exercises.

---

## CHAPTER 8 — Dynamics of the Volatility Surface (printed 101–106; PDF 132–137)

Since all SV models have the same surface *shape* (Ch7), one must look at **dynamics** — especially how the skew
depends on the volatility *level* — to differentiate models.

### 8.1 Dynamics of the skew under stochastic volatility — printed 101–102
Empirically `∂σ(k,t)/∂k` is ~independent of the volatility level over time. Translating to variance skew:
```latex
\frac{\partial}{\partial k}\sigma_{BS}(k,t)^2 = 2\sigma_{BS}\frac{\partial\sigma_{BS}}{\partial k} \sim v(k,t)
```
Comparing with (7.11), this implies `β(v) ∼ √v`, i.e. **variance is approximately lognormal**, in contrast to the
square-root process assumed by Heston. (Intuitive: high vol ⇒ vol-of-vol higher.) Whether square-root vs
lognormal matters depends on the hedged payoff: if the payoff depends on the skew and the skew is actually
volatility-level-dependent, assuming it is not loses money. **Even a wrong SV model beats LV:** a wrong SV model
off by ~1.5× if vol doubles, whereas LV generates almost *no* forward skew at all.

### 8.2 Dynamics of the skew under local volatility — printed 102–103
Empirically the skew slope *decreases* with time to expiration; for mean-reverting SV the term structure of the
variance skew follows (7.11), decaying with the coefficient `(1/(λ'T))(1 - (1-e^{-λ'T})/(λ'T))`. From the LV
formula (1.10) (`v_loc = (∂w/∂T)/(1 - wk\frac{∂w}{∂k} + \frac14(\frac14 - \frac1w + \frac{kw}{w^2}\frac{∂w}{∂k}^2 + ...)`,
where w = σ_BS²t) differentiating w.r.t. x and keeping the leading ∂w/∂k term (small for large T):
```latex
\frac{\partial v_{loc}}{\partial k} \approx \frac{\partial}{\partial T}\frac{\partial w}{\partial k} + \frac1w \frac{\partial w}{\partial T}\frac{\partial w}{\partial k}
```
so the **local-variance skew decays** with the BS total-variance skew. In LV models the *forward* surface is
computed by integrating local vols along the most-probable path; the forward surface is substantially flatter
than today's because all forward local skews are flatter. **Summary contrast: LV ⇒ future BS surfaces will be
flat (relative to today); SV ⇒ future surfaces look like today's (time-homogeneous skews).**

### 8.3 Stochastic implied volatility models — printed 103
If the underlying price is continuous (no jumps), the statics *and* dynamics of the IV surface are highly
constrained: option prices are martingales, `E[dC_t] = 0` forces a tight relation between sensitivities (which
yields e.g. (7.3)). Durrleman (2005) shows how to extract the instantaneous-variance dynamics from the observed
IV-surface dynamics near (τ→0, ATM), and vice-versa — but requires continuity. Jumps in the underlying (needed
for the surface shape) and observed jumps in the IV surface itself (Cont, da Fonseca, Durrleman 2002) both break
this.

### 8.4 Digital options and digital cliquets — printed 103–106
**Digital (call) option** D(K,T) pays 1 if S_T > K:
```latex
D(K,T) = -\frac{\partial C(K,T)}{\partial K} \tag{8.1}
```
Decomposing through the BS implied vol shows the skew contribution directly:
```latex
D(K,T) = -\frac{\partial C_{BS}}{\partial K} - \frac{\partial C_{BS}}{\partial\sigma_{BS}}\frac{\partial\sigma_{BS}}{\partial K}
```
Example (zero rates/dividends, 1-year ATM digital, ATM vol 25%, skew 3% per 10% strike):
`D(1,1) = N(-σ/2) − vega×skew = N(-0.125) + (1/√(2π))e^{-d²/2}×0.3 ≈ N(-0.125) + 0.4×0.3`. Ignoring the skew
term misprices the digital by **12% of notional**.

**Digital cliquet** = sequence of digital options with strikes set at future reset dates (usually ATM at reset);
pays `Coupon × θ(S_{t_i} - S_{t_{i-1}})` (θ = Heaviside) at t_i. Value is highly sensitive to the *forward* skew
assumption: LV sellers (forward skew too flat) price it **lower** and tend to win the deal and lose money. A
realistic 5-year 6% digital cliquet can be mispriced by up to 5.76% of notional (12% of the 48% coupon sum) — a
big multiple of typical margin.

---

## CHAPTER 9 — Barrier Options (printed 107–121; PDF 138–152)

Barrier options are core building blocks but their valuation can be **extremely model dependent** — quoted
prices sometimes cross the bid-offer across dealers. The chapter builds intuition via exactly-solvable limiting
cases, then applies the Ch7/Ch8 model-dynamics insights qualitatively.

**Definitions.** Knock-out: worthless when the barrier is reached. *Live-out* = knock-out that is significantly
in-the-money at knock-out. Knock-in = only exercisable if barrier hit (knock-in = −knock-out + European).
*Rebate*: money paid to the buyer if the barrier is hit (at hit or at expiration).

### 9.1 Limiting cases — printed 108–109
**Limit order / K=B below spot:** sell a knock-out call with barrier B=K<S₀, hedge with 1 stock, charge S₀−K.
With zero rates/dividends this hedge is perfect and **model independent** — delta 1, gamma 0, vega 0; the option
has no optionality (equivalent to a guaranteed-fill stop-loss). Real-world gap risk means the barrier should be
shifted to price it.
**European capped call** (call struck K, cap/barrier B>S₀, pays B−K if B hit): if B≫S₀ it prices like a
conventional European option with BS assumptions + the European implied vol — little model dependence. A
live-out call = capped call *minus* the one-touch rebate, so its intuition reduces to pricing the rebate.

### 9.2 The reflection principle — printed 109–112
Zero log-drift, constant-vol process `dx = σdZ`, `x = log(S/K)` (9.1). By symmetry the hitting probability of B
is twice the probability of finishing below B ⇒ **a one-touch option is worth exactly two European binary
options** (zero log-drift). Naive generalization: one-touch value / binary value = B(S₀)⁻¹. Tested for the
Heston–Nandi parameters of Ch4 (v̄=0.04, v=0.04, λ=10, η=1, ρ=−1, B(S₀)=0.54614 ⇒ predicted ratio 1.831): Fig 9.2
shows the ratio is **very sensitive to modeling assumptions** — accurate under LV, inaccurate under SV. European
binaries themselves are model independent (limits of call spreads, Fig 9.3).

### 9.3 The lookback hedging argument (Goldman–Sosin–Gatto) — printed 112–113
Lookback call pays (S̃−K)⁺, S̃ = max stock over the life. Zero log-drift, constant vol: hedge a short lookback
with **two European calls struck K**. When S hits K and moves up by δK, rebalance to two calls at K+δK; the
rebalancing profit
```latex
2C(K+\Delta K,K) - 2C(K+\Delta K,K+\Delta K) \approx -2\frac{\partial C}{\partial K}\Big|_{S=K}\Delta K
  = 2\,N(d_2)\big|_{S=K}\Delta K = \Delta K
```
(the last step using N(d₂)|_{S=K} = 1/2 at zero log-drift) exactly funds the lookback's new payoff ⇒ the hedge is
perfect. Taking a lookback-call-spread limit ⇒ **a one-touch is worth two European binaries at zero log-drift.**

### 9.4 Put-call symmetry — printed 113–114
Zero rates/dividends, constant vol: by BS inspection
```latex
C(S^2/B,\,K) = (K/B)\,P(S,\,B^2/K)
```
and a **down-and-out call** has the closed form
```latex
DO(S,K,B) = C(S,K) - C(S^2/B,\,K) = C(S,K) - \frac{K}{B}\,P\bigl(S,\frac{B^2}{K}\bigr)
```
`DO(B,K,B)=0` as expected. This gives a **static hedge**: long a European call at K, short (K/B) European puts
struck at the reflection of the log-strike in the log-barrier, K′ = B²/K; at the barrier the call value exactly
offsets the put value. Special case B=K: `DO(S,K,K) = C(S,K) − P(S,K) = S − K` — again no optionality.

### 9.5 Quasistatic hedging and qualitative valuation — printed 114–117
Generalize static hedging to arbitrary rates/dividends/vol structure: no exact static hedge exists, but a
portfolio with small payoffs under all reasonable scenarios can be built. Advanced version: the **Lagrangian
Uncertain Volatility Model** (Avellaneda–Levy–Parás 1995) — volatility bounded but uncertain; high when short
gamma, low when long gamma ⇒ bid/offer spread; optimizing over European-option weights minimizes the exotic
portfolio's bid-offer. Practically, determine the quasistatic hedge, then simulate its payoff mentally under
future S/vol scenarios ("mental Monte Carlo"). Results with Heston–Nandi Ch4 parameters (SV skew more negative
than LV forward skew):
- **OTM knock-out (B<K):** value slightly **lower under LV** than SV (both hedge options OTM, small effect) — Figs 9.5, 9.6.
- **One-touch:** hedge = strip of binaries at B; binaries worth *more* under SV ⇒ one-touch priced **lower under SV** — Fig 9.4.
- **Live-out (= capped call − one-touch):** capped call ~model independent, one-touch lower under SV ⇒ **live-out
  higher under SV** — Fig 9.7, substantial gap.
- **Lookback (K>S):** hedge = 2 calls; rebalancing sells call spreads which earn more under SV ⇒ **lookback lower
  under SV**; SV/LV ratio falls with strike (more elapsed time to first rebalance) — Fig 9.8.

### 9.6 Adjusting for discrete monitoring — printed 117–119
Discreteness is significant (barriers often monitored only at market close). Heuristic: on the day the discrete
max is first reached, the continuous max overshoots by ~a lookback worth `2·σ√(ΔT)/√(2π) ≈ 0.8σ√(ΔT)`, so
`Ṽ(B) ≈ V(B·e^{0.8σ√ΔT})`. **Broadie–Glasserman–Kou (1999)** theorem: with m monitoring points,
```latex
V_m(B) = V\bigl(B\,e^{\pm\beta\sigma\sqrt{T/m}}\bigr) + o(1/\sqrt{m}) \qquad (+\ \text{up},\ -\ \text{down})
```
```latex
\beta = -\frac{\zeta(1/2)}{\sqrt{2\pi}} \approx 0.5826
```
(ζ = Riemann zeta). Example: σ=0.32, daily monitoring (ΔT≈1/16): adjustment ≈ 0.32×0.6/16 ≈ 0.012, i.e. 1.2% of
barrier level. **Discretely monitored lookbacks:** `E[Ŝ_T] = E[S̃_T]e^{−βσ√ΔT}` (9.2), so the ATM lookback
```latex
\hat L(S_0,T) = \tilde L(S_0 e^{-\beta\sigma\sqrt{\Delta T}},T) - S_0\bigl(1 - e^{-\beta\sigma\sqrt{\Delta T}}\bigr)
```
### 9.7 Parisian options & applications — printed 120–121
Parisian: barrier knocks in/out only after the underlying stays outside the barrier for a minimum *window* —
reduces manipulation ("barrier wars") and has much tamer greeks. Constant-parameter Parisians price in
almost-closed form via Brownian excursion theory (Revuz–Yor ch12); general case via numerical PDE (Tavella–Randall).
**Applications:** *ladders* = strip of capped calls with increasing strikes (each barrier crossing locks in the
gain); as caps→strikes a ladder approximates a lookback (~2× European value); with ~10% spacing ~1.5× European.
*Ranges* (daily coupon while S stays in a band) = a one-touch double-barrier.
**Conclusion:** barrier prices must be adjusted for model sensitivity, but the limiting cases give solid
qualitative guidance; sometimes a barrier is *easier* to price than its European equivalent.

---

## CHAPTER 10 — Exotic Cliquets (printed 122–132; PDF 153–163)

A cliquet = sequence of cliquettes, forward-starting options whose strikes are set on reset dates; the most
obvious class of **forward-skew dependent** claims. Three real Mediobanca bonds are valued under Heston
(Stochastic Volatility) vs Local Volatility assumptions, using Heston–Nandi Ch4 parameters (v̄=0.04, v=0.04,
λ=10, η=1, ρ=−1) and the Ch4 Heston local-volatility approximation
```latex
v_{loc}(x_T,T) = \max\Bigl((\bar v - \bar v')e^{-\lambda' T} + \bar v' - \eta\,x_T\frac{1-e^{-\lambda' T}}{\lambda' T},\;0\Bigr)
```
with λ′ = λ + η/2, v̄′ = v̄λ/λ′; zero rates and dividends. These two sets of assumptions generate *almost
identical European option prices* — so any valuation difference is purely a *forward-skew/dynamics* effect.

### 10.1 Locally Capped, Globally Floored Cliquet ("Mediobanca Bond Protection 2002–2005", IT0003391353) — printed 122–125
Underlying EURO STOXX 50; guaranteed principal + annual coupon
```latex
\max\Bigl(\sum_{t=1}^{12}\min(\max(r_t,-0.01),+0.01),\; \text{MinCoupon}\Bigr),\qquad r_t = \frac{S_t - S_{t-1}}{S_{t-1}} - 1
```
MinCoupon=0.02 ⇒ annual coupon capped at 12%, floored at 2%. Without the global floor this is a strip of 1-month
ATM **call spreads** (local cap = upper strike), so intuition says it is very sensitive to forward skew (more
negative skew ⇒ higher call-spread value). Fig 10.1 confirms: at MinCoupon=2%, expected coupon under Heston =
**3.53%** vs LV = **2.55%** ⇒ upfront valuation difference **3×0.98 = 2.94%** (a big fraction of the exotic
provider's margin). LV substantially underprices because it generates forward skews that are too flat. The two
models agree at MinCoupon=12% (max coupon binding) and diverge most at MinCoupon=−1% (pure call-spread strip).
Actual coupons (11/25/2003–05): 3.91%, 3.55%, 4.14% ≈ the 3-yr euro swap (3.59% on issue) — diversification.

### 10.2 Reverse Cliquet ("Mediobanca 2000–2005 Reverse Cliquet Telecommunicazioni", IT0001458600) — printed 125–127
Basket of telecoms; guaranteed principal + final premium
```latex
P = \max\Bigl(0,\ \text{MaxCoupon} + \sum_{i=1}^{10}\min[0,r_i]\Bigr),\qquad r_i = \frac{\text{basket}_i - \text{basket}_{i-1}}{\text{basket}_i}
```
MaxCoupon=100% ⇒ max redemption 200%. Without the guaranteed redemption it is a strip of 6-month ATM puts
(investor is short puts); the global floor acts like a strip of OTM puts. **Little skew dependence**: Fig 10.3 —
at MaxCoupon=100% expected redemption 43.9% (Heston) vs 42.0% (LV). SV is consistently higher because the
global floor (OTM puts) is worth more under SV (flatter forward skew in LV world). Performance: basket fell ~70%
further after issue (83% max drawdown) — "don't catch a falling knife."

### 10.3 Napoleon ("Mediobanca 2002–2005 World Indices Euro Note Serie 46", IT0003487524) — printed 127–132
Guaranteed principal + annual coupon
```latex
\text{coupon}_i = \max\bigl[0,\ \text{MaxCoupon} + \tilde r_i\bigr],\qquad
\tilde r_i := \inf_{t_{i-1}<t_j<t_i} r_j
```
where r̃ᵢ is the average of the worst monthly returns of SPX, EURO STOXX 50, NIKKEI 225; MaxCoupon=10%. Each
cliquette has extreme dependence on the skew at strike-setting ⇒ the whole structure is **extremely forward-skew
dependent**; more negative skew ⇒ lower value (downside puts worth more). But — **the intuition fails here**
(Fig 10.5): at MaxCoupon=10% the expected coupon is ~identical (1.74% both). Reason: the Napoleon has huge
**volatility convexity** (coupon high at low vol, low at high vol), which LV underprices relative to SV; and when
the floor is hit, future vol has no further effect (vega→0), a cross-effect priced differently in the two models.
Moral: stress the **modeling assumptions themselves**, not just parameters within one model. Performance: coupons
1.70%/3.33%/5.55% vs 3-yr euro swap 3.26% on issue.
**More on Napoleons:** no clean decomposition into conventional options; the popular **independent-increment
technique** (returns independent even in squares) gets forward skews roughly right but has deterministic forward
vol ⇒ **underprices volatility convexity ⇒ underprices the Napoleon**. Since the lowest price wins the deal,
traders using the wrong model got the business (Jeffery 2004, RISK); ironically LV pricing would have lost less.
**Lesson: intuition is always fallible — try different modeling assumptions.**

---

## CROSS-CHAPTER SYNTHESIS (why the vol surface is the way it is — as these chapters bear on it)

The brief asked for "Gatheral's synthesis on why the vol surface is the way it is." The explicit synthesis lives
mostly in Ch1–3, but ch6–10 deliver the decisive pieces:
1. **Single stocks: default risk drives the skew.** Ch6 — high credit spreads force the BS-risky-rate pricing
   that produces extreme downside skews (Merton jump-to-ruin), and structural CreditGrades ties equity vol
   growth to leverage. Most of a high-credit-spread stock's skew is default risk.
2. **Shape is model-generic; dynamics distinguish models.** Ch7 — *all* SV-with-jumps models give the same
   surface shape (short-expiration skew ∝ ρηβ(v)/2; long-expiration ∝ ρηβ(v)/(λT); jumps additively contribute
   −2μ_J to the ATM variance skew at τ=0; extreme-strike wings governed by moment existence via Lee). Ch8 — you
   must look at *dynamics*: LV forward surfaces flatten (wrong for skew-dependent products); SV forward surfaces
   stay put (time-homogeneous), and the level-independence of the empirical skew points to **lognormal variance**.
3. **Consequence for pricing.** The choice of (SV vs LV) modeling assumptions — even more than parameter choice —
   materially changes forward-skew-sensitive claims: digitals (Ch8, 12% notional), barrier options (Ch9, up to
   cross-bid-offer), and exotic cliquets (Ch10, up to ~3% of notional for LCFG, large Napoleon swings). The
   recurring quantitative engine is the Heston–Nandi model of Ch4 used as the canonical SV benchmark against the
   Ch3/Ch4 Heston local-volatility proxy.

**Recurring techniques across the book's middle chapters:** (i) risk-neutral pricing via BS-type PDEs with
shifted rates (Ch6); (ii) short-time perturbation expansions + most-probable-path averaging of local variance
(Ch7); (iii) static/quasistatic hedging and reflection/pc-symmetry arguments for barrier claims (Ch9);
(iv) Monte Carlo valuation under paired (SV vs LV) dynamics with matched European prices to isolate the
forward-skew effect (Ch10); (v) default-risk models mapping credit spreads to the vol skew (Ch6).
