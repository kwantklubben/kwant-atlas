# Audit — `content/pillars/06-market-making/liquidity-risk-and-asset-pricing/`

**Reviewer:** sole, adversarial · **Date:** 2026-09-10
**Files:** 7 (index + 01…06) · **Code blocks:** 9/9 extracted and executed · **Verdict:** PASS WITH FIXES

---

## 1. Verdict

The folder is **structurally sound and correct in its core apparatus.** Every boxed/citable
formula — Amihud ILLIQ, Roll spread, Amihud–Mendelson amortization `R ≃ r + s/h` (Foucault
eq. 9.6), the Pástor–Stambaugh innovation+beta, the full Acharya–Pedersen liquidity-adjusted
CAPM (eq. 8, all four terms and signs), and the Bao–Pan–Wang bond `γ` — matches its cited
source. All **9 `python` blocks run to completion with deterministic seeds and reproduce
their documented output fences byte-for-byte.** All 16 wikilink targets resolve.

Defects are **localized**: the single material problem is a **sign-interpretation inversion
in page 04's §3** (the estimator outputs are right, but the code's own labels and the closing
paragraph read the AP betas backwards). Secondary issues: a worked example in 03 proves
nothing (no true premium in the DGP), one AP beta misattribution, one PS-scaling notation
slip, one one-way-vs-round-trip ambiguity in 01, and a beta-numbering collision with the
source paper. No broken code, no broken link, no wrong constant, no wrong formula *as written*.

---

## 2. Issues

| # | file:line | Problem | Fix |
|---|---|---|---|
| 1 | `04-liquidity-risk-and-crises.md:79–81, 86–87, 89` | **Sign-interpretation inversion (material).** The code prints `beta2 = cov(r^i,c^M)/varnet = -0.0440 (NEGATIVE premium -> safer)` and `beta3 = cov(c^i,r^M)/varnet = -0.0468 (NEGATIVE premium -> safer)`. Under AP eq. (8) these terms enter **with a minus sign** (`−λ·cov(r^i,c^M)/var`, `−λ·cov(c^i,r^M)/var`), so a *negative* covariance makes the term **positive ⇒ HIGHER** required return ⇒ **riskier**, not "safer". The closing paragraph (line 89) repeats it: it claims the stock's "return is high when the market is illiquid (β2<0)" and "stays liquid when the market falls (β3<0)" — but the simulated stock is `r_i = 0.9·rM` (pro-cyclical return: *low* when the market is bad/illiquid) and `c_i = 1.0·cM` (illiquid when the market falls). Both statements contradict the generated data **and** the hub's own correct sign note (index:52). Consequently the claim that the "three channels pull required return in opposite directions" is false here: `0.0043 −(−0.0440) −(−0.0468) = +0.0951 > 0`, so **all three liquidity terms raise** the required return. | Relabel the two prints `(POSITIVE contribution -> riskier)`; rewrite line 89 to "the stock is illiquid and low-return exactly when the market is illiquid, so all three channels **add to** the required return". If the narrative intent was a genuine hedge asset, regenerate `c_i` with `cov(c^i, r^M) > 0` (liquid when market falls) and `r_i` with `cov(r^i, c^M) > 0`. |
| 2 | `03-liquidity-as-a-priced-factor.md:57–89` | **Worked example demonstrates no premium.** The DGP is `r_i = 0.006 + 1.0·rM + β_i·L + ε` with `L ~ N(0, 0.01²)`, so `E[r_i] = 0.006 + 0.008 + β_i·0 = 0.014` for **every** stock. There is no cross-sectional relation between true expected return and `β_L`; the reported "long-short (HIGH−LOW) = 3.0%/yr" is pure finite-sample noise. The text ("That spread is the liquidity-risk premium") states a conclusion the simulation cannot support. | Give the factor a non-zero mean priced loading — e.g. add `λ·true_beta` to the intercept, or draw `L` with mean `μ_L ≠ 0` so `E[r_i]` increases in `β_i` — then the positive spread is genuinely a premium. |
| 3 | `03-liquidity-as-a-priced-factor.md:21` | **Misattribution of the PS channel's beta.** "…the 'PS channel' that Acharya–Pedersen formalize as **their β2**." In AP (2005) eq. (8) `β2 = cov(c^i,c^M)/var(·)` is *commonality*; the return-vs-market-liquidity (PS) channel `cov(r^i,c^M)` is AP's **β3**. | "…that Acharya–Pedersen formalize as their β³" (or "their third beta"). |
| 4 | `index.md:41`; `03-liquidity-as-a-priced-factor.md:35` | **PS innovation scaling notation.** Written `c\big(\tfrac{m}{m_0}\big)_{t-1}\hat\gamma_{t-1}`; PS (2003) eq. (7) is `Δγ̂_t = a + bΔγ̂_{t-1} + c(m_{t-1}/m_1)γ̂_{t-1} + u_t`, where `m_1` is the aggregate market cap at the **sample start** (`m_0` is not defined in the paper). | Use `(m_{t-1}/m_1)`. |
| 5 | `01-from-zero-intuition.md:34–36` vs `:51–59` | **One-way vs round-trip ambiguity.** §2 defines `s_i` as "the round-trip cost … (the relative spread)", giving total `2s_i` over the bond's life ⇒ `2s_i/h` per year; but the formula boxed there is `R ≃ r + s_i/h`, and §3's code labels `s = 0.002` as "20 bp **one-way**". The page is internally inconsistent about what `s` is. (Foucault eq. 9.6 uses `s/h` with `s` the relative spread.) | Fix §2's wording: with `s` = one-way relative cost the round trip is `s` (buy and sell each cost `s`), so total ≈ `s` not `2s`; or keep `s` = spread and state the formula as `R ≃ r + s/h` with `s` the **spread**. |
| 6 | `index.md:43–45`; `04-liquidity-risk-and-crises.md:45–47` | **Beta-numbering collision with the source.** The folder numbers the three liquidity betas `β1, β2, β3`, but AP (2005) numbers the four betas `β1`(market), `β2`(commonality), `β3`(cov(r,c)), `β4`(cov(c,r)). The folder's β1/β2/β3 = AP's β2/β3/β4. Explicitly redefined, so not wrong *per se*, but it already produced issue #3. | Add one clause: "numbered `β2, β3, β4` in the source paper; we relabel them `β1, β2, β3` for the liquidity channels only." |
| 7 | `01:23`, `03:2,19,96`, `04:106` vs `03:49,104`, `index:93` | **Inconsistent diacritic (spelling/consistency).** "Pástor" and "Pastor" both appear (`04:106` and `05:93`-style citations accent it; `01:23`, `03:2`, `03:19`, `03:96` and `index:28,42` do not). | Standardize on **Pástor** in prose and citations. |

**Nitpicks (not counted):**
- `02:43` — "the inverse of a volume-weighted ILLIQ" is loose: Amivest `ΣVOLD/Σ|R|` is the inverse of an *equal-day-mean* ILLIQ, not volume-weighted. Reword to "volume-weighted inverse illiquidity ratio".
- `05:47–53` Experiment 1 computes `p` but never uses it (dead variable).
- `06:38` "aggregate γ roughly doubled by Aug 2007 and tripled by Mar 2008" is a BPW (2011) claim; not verifiable against `corpus/verified/` (no BPW source present) — left as-is, source-consistent in tone.

---

## 3. Math verified (re-derived independently)

AP eq. (8) confirmed against the NYU Stern copy of Acharya & Pedersen (2005); PS eqs. (1)/(7)/(8)
confirmed against the UPenn copy of Pástor & Stambaugh (2003); Foucault eq. 9.6 against
`corpus/verified/foucault_ch4-6.md:39`.

| Formula (location) | Check | Result |
|---|---|---|
| AP liquidity-adjusted CAPM, boxed (index:50, 04:37–41) | `E(r^i)=r^f+E(c^i)+λ[ cov(r^i,r^M)+cov(c^i,c^M)−cov(r^i,c^M)−cov(c^i,r^M) ]/var(r^M−c^M)` | ✓ matches AP eq. (8) term-for-term |
| AP Σ sign note (index:52) | positive `cov(c^i,c^M)` ⇒ +; positive `cov(r^i,c^M)`, `cov(c^i,r^M)` ⇒ − | ✓ correct |
| AP beta definitions (index:43–45, 04:45–47) | three cov betas over `var(r^M−c^M)` | ✓ (numbering ⚠ issue #6) |
| Amihud ILLIQ (index:38, 02:39) | `(1/D)Σ|R|/VOLD` | ✓ |
| Roll `S_R` (index:39, 02:35, 05:29) | `cov(Δp_t,Δp_{t-1}) = −c²`; `S_R=2√(−cov)` | ✓ (derived: `c²·E[(q_t−q_{t-1})(q_{t-1}−q_{t-2})]=−c²`) |
| Amihud–Mendelson (index:40, 01:34–38) | `R ≃ r + s/h` | ✓ Foucault eq. 9.6 (see issue #5 on `s`) |
| PS innovation (index:41, 03:35–37) | `Δγ̂_t = a+bΔγ̂_{t-1}+c(m/m_0)_{t-1}γ̂_{t-1}+u_t`; `L_t=û_t/100` | ✓ structure/scaling (⚠ `m_0`→`m_1`, issue #4) |
| PS liquidity beta (index:42, 03:41) | `β^L = cov(r,L)/var(L)`, `λ>0` | ✓ |
| Bao γ (index:46, 06:36) | `γ = −cov(Δln P_{t+1}, Δln P_t) > 0` | ✓ |
| Bao AR(1) transitory noise (06:32) | `η_t=ρη_{t-1}+ε_t, |ρ|<1` | ✓ |
| Worked example: index ILLIQ (index:60–75) | `3.0097e-09`, `1.6842e-12`, ratio ≈1787 | ✓ ~1,800× |
| Worked example: amortization (01:50–67) | `0.002/h` → 10.000 / 2.500 / 0.400 / 0.200 %/yr | ✓ |
| Worked example: ILLIQ 252d (02:53–77) | `9.4050e-09`, `1.0969e-11`, `857×` | ✓ |
| Worked example: Roll bounce (02:81–107) | `0.0350`(true 0.04), `0.3994`(true 0.40) | ✓ |
| Worked example: PS sort (03:57–88) | `1.626%`, `1.876%`, `0.250%/mo` | ✓ runs (⚠ issue #2 on interpretation) |
| Worked example: AP betas (04:57–88) | `net_var=0.00050`, `b1=+0.0043`, `b2=−0.0440`, `b3=−0.0468` | ✓ arithmetic (⚠ issue #1 on labels) |
| Worked example: Roll momentum (05:45–60) | `acov=+0.00009`, Roll→`0.00000` | ✓ |
| Worked example: zero-volume ILLIQ (05:65–73) | `1.500e-09`, `3/6 days` | ✓ |
| Worked example: bond γ (06:50–78) | `1.6089e-07`, `2.6273e-06`, `16.3×` | ✓ |

---

## 4. Code execution

All **9** Python blocks (1 in `index`, 1 in `01`, 2 in `02`, 1 in `03`, 1 in `04`, 2 in `05`,
1 in `06`) were extracted from the fenced ```` ```python ```` blocks and executed with `python3`.
Every block reproduced its documented output fence **exactly** (string-equal, including the
deterministic `random.seed` values 1/3/7/11/5/21). No block errored, no stderr, no output drift.

## 5. Coherence & links

- **Hub ↔ 01 prereq:** index:11 declares `Econometrics & Time Series` + `Statistics & Inference`
  as folder prerequisites for pages 02–06 and routes page 01 to its own "basic algebra only"
  entry (01:10) — consistent and correctly qualified.
- **Jargon first-use:** `ILLIQ`, `VOLD`, `Kyle λ`, `liquidity beta`, `commonality`, `flight to
  quality` are all defined on first use in 01/02 and cross-linked thereafter. Fine.
- **Links:** all **16** wikilink targets resolve (folder hubs `index.md` or `.md` files present):
  `foundations/econometrics-and-timeseries`, `foundations/statistics-and-inference`,
  `pillars/04-.../liquidity-risk-and-funding/{index,03-liquidation-cost-and-lvar,04-margin-and-funding-spirals}`,
  `pillars/06-market-making/{market-impact-and-depth,spread-decomposition-and-roll-model,toxic-order-flow-and-vpin,inventory-management-and-quote-skewing}/index`, and the six in-folder pages. No broken links.
- **Contradictions:** the one real internal contradiction is the 04 §3 sign reading vs the hub's
  §2 sign note (issue #1). Also the 01 one-way/round-trip ambiguity (#5).
- **File count:** 7 files = index hub + 6 sub-pages ✓ (matches the "six sub-pages" claim at index:26).
