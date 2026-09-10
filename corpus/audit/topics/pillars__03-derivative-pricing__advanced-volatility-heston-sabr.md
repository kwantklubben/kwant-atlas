# Audit — `pillars/03-derivative-pricing/advanced-volatility-heston-sabr/`

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages). Heston SDE/PDE/Feller, characteristic function, Riccati ODEs, Lewis inversion, SABR 7.7 + β/ν/ρ asymptotics, Medvedev–Scaillet, Bergomi–Guyon (ch 8) identities, forward-variance/vol-of-vol term structure, SSR, jumps, calibration, digital/model-risk.
**Corpus cross-check:** `corpus/verified/gatheral_ch1-5.md` (Heston 2.1–2.18, implied var 3.17–3.19, SVJ/SVJJ), `gatheral_ch6-10.md` (7.3–7.13, SABR, Lee, digital/cliquet ch 8–10), `bergomi_ch6-10.md` (6.3–6.20, 7.39–7.40, 8.39–8.50, 9.16, 12.x), plus Haug/Hull/Shreve pointers.
**Method:** (1) spelling/typo scan; (2) every boxed formula & worked example re-derived / re-computed; (3) every ```python block executed and stdout diffed against its output fence; (4) hub↔sub-page coherence, link resolution, jargon first-use.

---

## VERDICT: **FAIL** — 6 errors found (2 math sign errors, 1 math slip, 1 numeric incoherence, 2 prose/formula nits)

All **7 of 7 code blocks execute and reproduce their output fences character-for-character**. Every boxed Heston/Riccati/Lewis formula, every Bergomi–Guyon constant, the Feller/Milstein conditions, the SABR skew/curvature laws and all headline numbers in the hub lookup table are correct. The failures are in two displayed reference formulas (signs), one intermediate expression, and hub↔sub-page consistency.

---

## Summary of findings

| # | Severity | File:line | Type | Issue |
|---|----------|-----------|------|-------|
| 1 | **HIGH** | `04-stochastic-vol-dynamics.md:83` | MATH (sign) | Two-factor skew (9.16a) numerator `k_iT−1−e^{−k_iT}` → should be `k_iT−1+e^{−k_iT}`; contradicts (6.20) on the same page *and* the `R_T` formula printed in the same display. |
| 2 | **MED** | `03-sabr-and-asymptotics.md:76`, `06-advanced-extensions.md:47`, `index.md:55` | MATH (sign) | Jump compensator defined as `μ_J = λ_J E[J−1]`; Gatheral's compensator is `μ_J = −λ_J E[J−1]`. With the printed `−2μ_J` the jump contribution to the short-dated variance skew comes out with the wrong sign. |
| 3 | **MINOR** | `03-sabr-and-asymptotics.md:65` | MATH (factor 2) | "`ρη/(2√v) = ρη/(4σ_BS)`" — the intermediate is off by 2; should be `ρη/(4√v)`. Final `ρη/(4σ_BS)` (Bergomi 6.18b) is right. |
| 4 | **MINOR** | `index.md:52` | COHERENCE (numeric) | Hub states vol-of-vol term-structure ratio "0.65 (3m) … 0.50 (5y)"; sub-page 04 computes/narrates 0.763 (3m) and 0.587 (5y). Not reproducible from the folder's own run. |
| 5 | **MINOR** | `index.md:50` | PROSE (typo) | Stray label "(10.000 yr)" in the Heston one-factor row; maturities listed are 0.05 / 0.25 / **1.000** yr. |
| 6 | **MINOR** | `06-advanced-extensions.md:39` | MATH (formula) | Jump multiplier written `(e^{α+δ}−1)`; with log-jump `~N(α,δ²)` it must be `(e^{α+δZ}−1)` (Z~N(0,1)). |

---

## FINDING 1 — HIGH · Two-factor ATMF-skew formula has a sign error (`04-stochastic-vol-dynamics.md:83`)

**File/line:** `04:83`.

**Stated:**
$$\mathcal S_T=\frac{\omega}{2}\sum_i w_i\rho_{iS}\frac{k_iT-1-e^{-k_iT}}{(k_iT)^2}.$$

**Correct:** the numerator is $k_iT-1+e^{-k_iT}\;(=k_iT-(1-e^{-k_iT}))$. Bergomi (6.20), printed on the **same page** (`04:55`) and verified in `corpus/verified/bergomi_ch6-10.md:97`, is

$$\mathcal S_T=\frac{\rho\sigma}{2\sqrt{V_0}}\frac{kT+e^{-kT}-1}{(kT)^2},$$

and the `R_T` formula printed in the *same display* one clause later (`04:83`) correctly uses $k_iT-(1-e^{-k_iT})$ — so the page contradicts itself.

**Derivation (one factor, flat curve):** from $S_T=\tfrac{1}{2 V^{3/2}T}\int_0^T\frac{T-\tau}{T}\mu(\tau)\,d\tau$ with $\mu\propto e^{-k\tau}$,
$$\int_0^T(T-\tau)e^{-k\tau}d\tau=\frac{kT-1+e^{-kT}}{k^2},$$
giving $S_T\propto(kT-1+e^{-kT})/(kT)^2$, which is $\tfrac12$ as $kT\to0$ (recovering $\rho\eta/(4\sqrt{\bar v})$) and $\propto1/(kT)$ for large $kT$. The printed $k_iT-1-e^{-k_iT}$ instead behaves like $-2/(kT)^2$ near $kT\to0$ and diverges — so it cannot reduce to (6.20).

**Fix:** replace `k_iT-1-e^{-k_iT}` with `k_iT-1+e^{-k_iT}` in (9.16a).

---

## FINDING 2 — MED · Jump-compensator sign is flipped (`03:76`, `06:47`, `index:55`)

**Locations:** `03-sabr-and-asymptotics.md:76`; `06-advanced-extensions.md:47`; `index.md:55`.

**Stated (03:76, boxed):**
$$\frac{\partial v_{BS}}{\partial k}\Big|_{k=0}\to\rho\,b(\sigma)-2\mu_J,\qquad \mu_J=\lambda_J\mathbb E[J-1].$$
and (06:47): "$\partial_k\sigma_{BS}^2|_0\to\rho\eta/2-2\mu_J$ with compensator $\mu_J=\lambda_J\mathbb E[J-1]$".

**Correct:** Gatheral's compensator is $\mu_J=-\lambda_J\,\mathbb E[J-1]$ (vision-verified, `corpus/verified/gatheral_ch1-5.md:110`: "risk-neutral drift µ = r + µ_J, µ_J = −λ(t)E[J−1]", with the skew `−2µ_J` at `:124`, eq. 5.10). The page dropped the minus, which flips the sign of the jump term.

**Independent confirmation.** For a Merton jump-diffusion with $\lambda=0.5,\ \alpha=-0.10,\ \delta=0.10,\ \sigma=0.20$ ($\kappa=\mathbb E[J-1]=-0.0906$) I computed $\partial_k\sigma_{BS}^2|_0$ from the exact CF + Lewis inversion: $-0.0847$ at $T{=}0.002$, converging toward $2\lambda\kappa=-0.0906$ — i.e. **negative**, as Gatheral's $-\!2\mu_J$ with $\mu_J=-\lambda\kappa$ requires. The page's $-\!2\mu_J$ with $\mu_J=+\lambda\kappa$ gives **$+0.0906$**, the wrong sign. Downward jumps must *steepen* the downward skew.

**Internal confirmation.** The page's own CF term (`06:43`) is $\psi(u)=-\lambda_J iu(e^{\alpha+\delta^2/2}-1)+\dots$ — the drift correction uses $-\lambda_J\mathbb E[J-1]$, exactly the opposite of the definition it prints.

**Fix:** define $\mu_J=-\lambda_J\mathbb E[J-1]$ (or, equivalently, write the skew as $+\,2\lambda_J\mathbb E[J-1]$). Applies to all three locations.

---

## FINDING 3 — MINOR · Off-by-2 intermediate in the Heston 7.6 specialisation (`03:65`)

**Stated:** "For Heston, $\eta\beta(v)=\eta$ gives $\rho\eta/(2\sqrt v)=\rho\eta/(4\sigma_{BS})$".

Since $\sqrt v=\sigma_{BS}$, the middle expression $\rho\eta/(2\sqrt v)$ equals $\rho\eta/(2\sigma_{BS})$, **not** $\rho\eta/(4\sigma_{BS})$. The correct chain: for Heston $b(\sigma)=\eta/2$ (since $\sigma=\sqrt v$, $d\sigma=\dots+\tfrac{\eta}{2}dZ_2$), so $\rho b(\sigma)/(2\sigma)=\rho\eta/(4\sqrt v)=\rho\eta/(4\sigma_{BS})$ — Bergomi (6.18b), which the page quotes correctly. The printed $2$ should be $4$.

---

## FINDING 4 — MINOR · Hub vol-of-vol ratio not reproducible (`index:52`)

Hub row: `| Vol-of-vol term structure (6.9) | … | vs power law (7.40): ratio 0.65 (3m) … 0.50 (5y) |`.

The folder's own computation (`04:211–221`, fence `04:245–252`) reports `Hest/bench` $=0.763$ at 0.10 yr, $\mathbf{1.000}$ at 0.25 yr (3 m, the normalisation point), and $0.587$ at 5 yr; and `04:260` narrates exactly those ($24\%$ low at 3 m, $41\%$ low at 5 y). Neither $0.65$ (3 m) nor $0.50$ (5 y) is produced. (They look like the *unnormalised* ratios at other maturities: raw $I(\lambda T)/[(0.25/T)^{0.4}]$ is $0.649$ at $\approx0.10$ yr and $0.500$ at 5 yr.) Fix the hub row to match 04: $0.76$ (3 m) … $0.59$ (5 y), or state the normalisation.

---

## FINDING 5 — MINOR · Prose typo in the hub lookup table (`index:50`)

`… | T=0.05/0.25/1 (10.000 yr) ⇒ σ̂_T=13.410/14.170/15.946% |`. The maturities are 0.05, 0.25 and **1.000** yr; "(10.000 yr)" is a stray leading zero. (The three values 13.410/14.170/15.946 match the `04` fence exactly.)

---

## FINDING 6 — MINOR · Jump multiplier missing the random factor (`06:39`)

**Stated:** $dS=\mu S\,dt+\sqrt v\,S\,dZ_1+(e^{\alpha+\delta}-1)S\,dq$, "with log-jump size $\sim\mathcal N(\alpha,\delta^2)$".

With a *random* lognormal jump the multiplier is $e^{\alpha+\delta Z}$ ($Z\sim\mathcal N(0,1)$), not the constant $e^{\alpha+\delta}$. As printed the term is deterministic, which contradicts the stated jump law (and the CF at `06:43`, which correctly uses $e^{\alpha+\delta^2/2}$, $e^{iu\alpha-u^2\delta^2/2}$). Minor notational defect (a fixed-size jump, not a lognormal one).

---

## Observations / nits (not counted)

- **Feller boundary equality** — `02:52`: "If $2\lambda\bar v\le\eta^2$ the origin is *regular and accessible*". For CIR the origin is accessible iff $2\kappa\theta<\sigma^2$ **strictly**; at equality ($2\lambda\bar v=\eta^2$) the boundary is inaccessible (entrance). The page's "$\le$ ⇒ accessible" overshoots at equality. (`index:37` states the strict form correctly.)
- **Hub pricer skew value** — `index:44` quotes `pricer: −0.138652 vs ρη/2=−0.138894`, while the sub-page `04` fence reports `−0.138331`/`−0.138404` at $T{=}0.005$–$0.01$. The hub value is reproducible only at a *much* finer resolution (I recovered exactly `−0.138652` at `n=60000, U=800`, $T{=}0.005$); it is consistent with the $\rho\eta/2$ asymptote but the resolution is not stated, so the hub number cannot be reproduced from the cited sub-page block.
- **Boxed (7.7) vs code bracket** — the boxed SABR formula (`03:41`) writes the $O(\tau)$ correction as $1+\tfrac14\rho\nu\sigma_0+\tfrac{2-3\rho^2}{24}\nu^2\tau$ (the first term without $\tau$), matching `corpus/verified/gatheral_ch6-10.md:237`; the §3 code (`03:138`) multiplies *both* terms by $\tau$. The two coincide at the test value $\tau=1$, so no output is affected, but the box and code differ for general $\tau$. Flagged as inherited from the source form, not a page error.
- `02:201` cites a 60 000-path Monte Carlo and a standard error ($\approx0.03$) that are not in any ```python``` block — unverifiable narrative (plausible, but not reproducible from the folder).

---

## Verified-correct items (no action)

### Formulas — ALL CORRECT (cross-checked against corpus)
- **Heston SDE** `index:36`, `01:55`, `02:36` $dS_t=\sqrt{v_t}S_tdZ_1,\ dv_t=-\lambda(v_t-\bar v)dt+\eta\sqrt{v_t}dZ_2,\ dZ_1dZ_2=\rho dt$ (Gatheral 2.1–2.2). *(Written driftless — legitimate in the forward measure, which is how the whole folder prices.)*
- **Heston PDE** `02:42`: exactly `corpus/…gatheral_ch1-5.md:45` (2.3), incl. the verified RHS sign $\lambda(\bar v-v)V_v$.
- **Feller** `02:50`, `index:37`: $2\lambda\bar v>\eta^2$. **Milstein** `02:210`, `05:37`: scheme $=[\sqrt{v_i}+\tfrac\eta2\sqrt{\Delta t}Z]^2-\lambda(v_i-\bar v)\Delta t-\tfrac{\eta^2}4\Delta t$, condition $4\lambda\bar v/\eta^2>1$ (Gatheral 2.18) — both correct.
- **PDE for $P_j$** `02:62` and **Riccati coeffs** `02:66`: $\alpha=-u^2/2-iu/2+iju$, $\beta=\lambda-\rho\eta j-\rho\eta iu$, $\gamma=\eta^2/2$, $r_\pm=(\beta\pm d)/\eta^2$, $d=\sqrt{\beta^2-4\alpha\gamma}$ — all match `gatheral_ch1-5.md:50–51`.
- **Riccati solution** `02:72` and **CF** `02:80`, `index:39`: $D=r_-(1-e^{-d\tau})/(1-ge^{-d\tau})$, $C=\lambda\{r_-\tau-\tfrac2{\eta^2}\ln\frac{1-ge^{-d\tau}}{1-g}\}$, $g=r_-/r_+$ (2.12/2.15) — exact; and the $r_-$ (not $r_+$) branch-cut choice is correctly recommended (`02:209`).
- **Lewis/Carr–Madan** `index:40`, `02:93`: $C=F_T-\frac{\sqrt{F_TK}}{\pi}\int_0^\infty\frac{du}{u^2+\frac14}\mathrm{Re}[e^{-iuk}\varphi_T(u-\tfrac i2)]$ (5.6) — exact.
- **Heston (3.18) ATM term structure** `index:43` and its critical caveat `index:58`, `02:203`: $(3.18)$'s literal $T\to0$ limit is $\bar v$, not $v_0$ — matches the corpus "notation subtlety" note; handled honestly.
- **(3.19) short skew → $\rho\eta/2$** `index:44`, `04:24`; **FPS (7.10)**, **interpolation (7.11)**, **Lewis $O(\eta)$ proof (7.12)**, **Lee $g(x)=2-4(\sqrt{x^2+x}-x)$** `03:82,90,94` — all match `gatheral_ch6-10.md`.
- **SABR (7.7)** `03:41` with $y=-\nu k/\sigma_0$, $f(y)=\ln\frac{\sqrt{1-2\rho y+y^2}+y-\rho}{1-\rho}$; **Taylor form** `03:47`; $S_0=\rho\nu/2$, $C_0=(2-3\rho^2)\nu^2/(6\sigma_0)$ `03:51` — match corpus verbatim.
- **Medvedev–Scaillet** `03:59,63` $I_1=\rho b(\sigma)z/2$, $\partial I/\partial k|_0\to\rho b(\sigma)/(2\sigma)$ — match.
- **Jump additivity** `03:76`, `index:55`: $\rho b(\sigma)-2\mu_J$ (form correct; only the $\mu_J$ *definition* sign is wrong — Finding 2).
- **Bergomi 6.3/6.4, 6.9, 6.20, 7.39, 7.40, 8.18, 8.20–8.21, 8.35–8.44, 9.5–9.6, 9.16b, 12.4/8.50** `04`, `06`, `index` — all match `bergomi_ch6-10.md` (incl. $R_T\in[1,2]$, $R_0=2$, Type I/II, $\nu_T=\nu\alpha_\theta\sqrt{\Sigma w_iw_j\rho_{ij}I_iI_j}$, the "radical covers only $\xi^t$" LSV covariance). **9.16a** is the sole exception (Finding 1).
- **SVJ CF & $\psi(u)$** `06:43` and **Table 5.5 SPX fit** (`v_0=0.0158,\bar v=0.0439,\eta=0.3038,\rho=-0.6974,\lambda=0.5394,\lambda_J=0.1308,\delta=0.0967,\alpha=-0.1151`) `06:48` — exact vs corpus.
- **Digital** `02:54`, `05:63`: $D=-\partial C_{BS}/\partial K-\text{vega}\,\partial\sigma_{BS}/\partial K$ — correct.
- **$R_T$ two-factor (9.16b)**, **SSR P&L** `04:83,127`; **Broadie–Glasserman–Kou $\beta\approx0.5826$** `05:228`; **Rate-vol (5.54–5.55)** `06:191` — all match corpus.

### Worked numbers — ALL CORRECT (re-executed)
- Feller/Milstein on Table 3.2: $0.09383<0.15031$; $4\lambda\bar v/\eta^2=1.24849>1$ ✅
- $\eta\to0$ collapse: Heston $7.96607957$ vs BSM $7.96556746$ ✅
- Table 3.2 IVs $19.573/16.895/14.234/11.989/10.993\%$; parity residual $0.0$ ✅
- $\varphi(-i)=1.000000000000$ at $T=0.01,1,5$ ✅ (the strong normalisation check)
- $T\to0$ ATM IV $\to\sqrt{v_0}=13.1903\%$; deterministic FV average $0.025427$ ($15.946\%$) ✅
- SABR ATM $19.7798\%$; skew $-0.137364=(\rho\nu/2)\cdot0.988991$; curvature $0.056971=0.057605\cdot0.988991$ ✅
- Bergomi–Guyon $8.40$: $0.150311=\nu^2$ ✅; Heston normal form $-0.369105$ ✅
- Heston FV curve $13.410/14.170/15.946\%$; skew limits $-0.369105$ / $-0.011140$; var-skew vs $-\rho\eta/2$ ✅
- ATMF skew (6.20) short/long limits $-0.367480$/$-0.010972$ vs $-0.369105$/$-0.011140$ ✅
- Euler neg-variance $1.946\%$ of steps, Milstein $0.000\%$ (min $3.1\times10^{-5}$) ✅
- Digital skew $0.118751$ ⇒ $11.9\%$ of notional ($26.4\%$ of value) ✅
- Calibration ridge: start1 RMS $8.11\times10^{-3}$ ($\kappa{=}1.868$), start2 RMS $5.43\times10^{-4}$ ($\kappa{=}2.003$) ✅
- 06 forward-variance: $\chi(t,T)\equiv\int_{T-t}^T\eta^2du$ to $10^{-15}$; $\mathbb E[\xi_t^T]\approx0.04$; $E[\sqrt V]< \sqrt{E[V]}$ gap $-0.037$ ✅

### Code blocks — execution & fence diff
**7 code blocks** extracted from 7 files, all executed in Python 3 (stdlib only). **7 of 7** reproduce their output fences **character-for-character** (deterministic seeds where MC is used). No nondeterminism issues.

### Coherence & links
- Structure: exactly index + 6 sub-pages; hub ⇄ sub-page navigation complete. ✅
- **All 26 unique wikilink targets resolve** (in-folder, BSM 02/03/04/05/06, VS 01–06, interest-rate, quant-risk, three foundations). ✅
- Prerequisite chain coherent: hub sets VS + stochastic-calculus for 02–06, `01` self-declares BSM-only; 02→01+BSM-02, 03→02+VS-04, 04→02+03, 05→02+04, 06→04+05. ✅
- Jargon: `CIR` is spelled out only in `02:18` but used undefined in `01:57` (the "stands alone" beginner page) — minor; `SSR` is defined at first use (`04:25`); `Bergomi–Guyon` first appears in the hub without a one-line gloss (defined at `04:87`).
- No spelling errors found in any of the 7 files (prose scanned after stripping code/LaTeX/math/wikilink syntax).

---

## Files checked (7)
1. `index.md` (source of findings 2b, 4, 5)
2. `01-from-zero-intuition.md`
3. `02-the-heston-model.md`
4. `03-sabr-and-asymptotics.md` (findings 2a, 3)
5. `04-stochastic-vol-dynamics.md` (finding 1)
6. `05-failure-modes-and-practice.md`
7. `06-advanced-extensions.md` (findings 2b, 6)

**Blocks run:** 7 · **Fence matches:** 7/7 · **Errors found:** 6
