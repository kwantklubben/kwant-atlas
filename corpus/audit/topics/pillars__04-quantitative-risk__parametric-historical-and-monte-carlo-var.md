# Audit: `content/pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/`

**Sole reviewer, adversarial pass.** Folder = 7 files (index hub + 6 sub-pages, `01`–`06`). Scope: (1) spelling/typos in prose (code/LaTeX excluded); (2) MATH — every boxed formula + worked example (delta-normal VaR, √T scaling, historical simulation, EWMA/vol filtering, MC VaR, Kupiec/Christoffersen backtests, age-weighting), cross-checked against Hull Ch 22–23 and Glasserman Ch 9 (both verified in `corpus/verified/`); (3) CODE — every ` ```python ` block executed under Python 3.14 and stdout diffed against the output fence; (4) COHERENCE — hub↔01 prereqs, jargon, wikilinks, contradictions. `content/_legacy/` ignored.

**Verdict: PASS with findings.** All **10 python blocks run cleanly and reproduce their documented output *exactly*** (every block is seeded; stdout is byte-matchable). All cross-method anchor numbers (`3,396.15 / 3,218.55 / 3,405.97`), the Student-$t(4)$ rate, the ghost-effect numbers (`3,465.15 / 3,195.63`), the delta–gamma comparison and the Kupiec/Christoffersen outputs are internally consistent and reproduce. **Two substantive findings:** one boxed formula is typeset wrong (**F1**, Christoffersen LR rendered as a fraction), and the historical-simulation rank is off-by-one (**F2**, code computes the *6th*-worst while the boxed formula + prose say *5th*-worst). Eight minor prose/coherence nits follow (**F3–F10**). No misspelled words detected in prose. All wikilinks resolve.

---

## 1. Code verification (10/10 blocks run, all pass — stdout exact)

Blocks extracted per file and executed under Python 3.14.7 (`python3`), stdout diffed against each file's documented fence. Every block is `random.seed`-ed, so agreement required zero judgement.

| File | § | Block | Result | Diff vs fence |
|---|---|---|---|---|
| index.md | 3 | parametric + historical + MC on shared portfolio | Ran clean | **Exact match** (`3,396.15 / 3,218.55 (rank 6) / 3,405.97`) |
| 01-from-zero-intuition.md | 3 | quantile of 1000 simulated losses (seed 1) | Ran clean | **Exact match** (`-67.69 / 2374.30 / 3432.97 / 4496.08`) |
| 02-parametric-var.md | 3 | wᵀΣw closed form + EWMA update | Ran clean | **Exact match** (`2,131,200.00 / 1,459.86 / 3,396.15 / 10,739.57 / 0.0001489`) |
| 03-historical-simulation.md | 3 | HS + EWMA vol filter (seed 20260910) | Ran clean | **Exact match** (`3,218.55 (rank 6 worst) / 0.0136`) — but see **F2** |
| 04-monte-carlo-var.md | 3a | MC VaR with quantile SE (seed 7, m=200k) | Ran clean | **Exact match** (`3,405.97, se=±13`) |
| 04-monte-carlo-var.md | 3b | FX put: full revaluation vs delta-only (seed 9, m=400k) | Ran clean | **Exact match** (`V0=0.0670 δ=-0.5616 γ=2.997; 0.0143 / 0.0153`) |
| 05-failure-modes-and-practice.md | 3 | Student-t(4) exceedance (seed 3, n=200k) | Ran clean | **Exact match** (`1.5565%`) — see **F10** |
| 05-failure-modes-and-practice.md | 3 | ghost effect (seed 5) | Ran clean | **Exact match** (`3,348.79 / 3,465.15 / 3,195.63`) |
| 06-advanced-extensions.md | 3a | delta–gamma vs full vs delta-only (seed 9, m=400k) | Ran clean | **Exact match** (`0.0153 / 0.0141 (0.99x) / 0.0143`) |
| 06-advanced-extensions.md | 3b | Kupiec + Christoffersen backtest (seed 11) | Ran clean | **Exact match** (`11/1000 LR=0.1 accept, Chr=0.24; 115/1000 LR=363.3 REJECT, Chr=0.76`) |

Independent re-derivations confirm the fences:
- **Kupiec** (computed independently): $x=11,T=1000\Rightarrow \text{LR}=0.09783$ (fence `0.098` ✓); $x=115,T=1000\Rightarrow 363.2922$ (fence `363.29` / `363.3` ✓).
- **Portfolio vol**: $\sqrt{2{,}131{,}200}=1459.863$; $\times z_{0.99}=3396.15$ ✓; $\times\sqrt{10}=10739.57$ ✓.
- **Put**: $V_0=0.0670$, $\delta=-0.5617$, $\gamma\approx2.997$ ✓; delta-only $=2.3263\cdot0.5616\cdot1.55\cdot0.12/\sqrt{252}=0.01531$ ✓.
- **t(4)** normalize `t4()/√2` is correct (t(4) variance $=d/(d-2)=2$) ✓.

## 2. Math verification

**Delta-normal / parametric (index, 01, 02, 05) — correct.** $\text{VaR}=z_\alpha\sigma_p\sqrt h$, $\sigma_p=\sqrt{w^T\Sigma w}$ (02 boxed eq.) is Hull Ch 22 eq. 22.3/22.4 ✓. Drift form $\text{VaR}=-w^T\mu+z_\alpha\sqrt{w^T\Sigma w}\sqrt h$ sign correct ✓. EWMA $\sigma^2_n=\lambda\sigma^2_{n-1}+(1-\lambda)u^2_{n-1}$, $\lambda=0.94$ = Hull eq. 23.7 ✓; GARCH(1,1) $V_L=\omega/(1-\alpha-\beta)$ = Hull eq. 23.8/23.9 ✓; PSD eq. 23.17 ✓ (all four confirmed in `corpus/verified/hull_ch19-23.md`).

**√h scaling (01, 02, index) — correct.** $\text{VaR}^{(h)}=\text{VaR}^{(1)}\sqrt h$ under i.i.d.; the i.i.d./GARCH caveat is stated. ✓

**Historical simulation (index, 03, 05) — formula correct, rank label wrong (F2).** Boxed $\widehat{\text{VaR}}_\alpha=L_{(\lceil n(1-\alpha)\rceil)}$ = empirical $\alpha$-quantile ✓; empirical-quantile asymptotic variance $\sqrt n(\hat x_p-x_p)\Rightarrow N(0,p(1-p)/f(x_p)^2)$ = Glasserman Ch 9 §9.1 ✓. The **rank value** disagrees with the prose — see F2.

**MC VaR (04) — correct.** Empirical-quantile estimator = same formula as HS ✓; Cholesky $A=[[\sigma_1,0],[\sigma_2\rho,\sigma_2\sqrt{1-\rho^2}]]$ satisfies $AA^T=\Sigma$ (verified: off-diagonal $=\sigma_1\sigma_2\rho$, diagonal-2 $=\sigma_2^2$ ✓); SE $=\sqrt{p(1-p)}/(\sqrt m\,\hat f(x_p))$ is the standard asymptotic quantile SE ✓. Real-world-vs-risk-neutral framing (Glasserman) correct ✓.

**Delta–gamma (06) — correct.** $\Delta V\approx\Theta\Delta t+\delta^T\Delta S+\tfrac12\Delta S^T\Gamma\Delta S$ = Hull 22.7/22.8 & Glasserman (9.2) ✓. Diagonalization "$-\tfrac12C^T\Gamma C=\Lambda$" gives the same eigenvalues as Glasserman's "eigenvalues of $-\tfrac12\Gamma\Sigma_S$" (the two matrices are similar), and the resulting loss $L\approx Q=a+\sum(b_jZ_j+\lambda_jZ_j^2)$, $a=-\Theta\Delta t$, matches Glasserman (9.4) ✓. Table 9.1 reduction factors (CV 2–5×, IS 7–27×, IS-S ~173×) match the corpus digest ✓.

**Backtests (index, 06) — Kupiec correct, Christoffersen typeset wrong (F1).** Kupiec $\text{LR}_{POF}=-2\ln[\frac{(1-p)^{T-x}p^x}{(1-\hat p)^{T-x}\hat p^x}]\sim\chi^2_1$, threshold 3.841, $\hat p=x/T$ ✓; conditional coverage $=\text{LR}_{POF}+\text{LR}_{ind}\sim\chi^2_2$ ✓; Basel zones (green ≤4/250, red ≥10/250) ✓; FRTB 97.5% ES ✓. The **Christoffersen independence LR is rendered as a ratio instead of a difference** — see F1.

## 3. Spelling & prose

No misspelled words detected in prose (technical terms, LaTeX and code stripped). Grammar/register consistent. The issues below are punctuation/grammar/likely-typo nits, not vocabulary errors (F3–F7).

## 4. Coherence

- **Hub↔01 prereqs:** consistent. Hub (index line 11) declares Linear-Algebra + Statistics as the folder-level prereqs for pages 02–06 and explicitly notes page 01 states its own smaller entry bar; page 01 (line 11) declares only Statistics & Inference. No contradiction ✓.
- **Anchor numbers ↔ sub-page outputs:** all flow from the executed blocks and agree across files (`3,396.15 / 3,218.55 / 3,405.97`; `3,465/3,196`; `0.0141/0.0143`; `LR=363.3`) ✓ except the rank/range nits (F2, F8).
- **Jargon:** delta-normal, filtered HS, ghost effect, EWMA/GARCH, delta–gamma, Kupiec/Christoffersen, conditional coverage, traffic-light zones — all used precisely ✓.
- **Wikilinks:** every `[[…]]` target in the folder resolves (checked against the content tree): `foundations/{linear-algebra-and-matrices,statistics-and-inference,econometrics-and-timeseries,numerical-methods,probability-and-measure-theory}/index`, `pillars/04-quantitative-risk/{var-and-expected-shortfall,extreme-value-theory-and-fat-tails,stress-testing-and-scenario-analysis}`, `pillars/03-derivative-pricing/black-scholes-merton/{index,04-greeks-and-hedging}` — **0 misses** ✓.

---

## Findings

### Substantive

**F1 — `06-advanced-extensions.md` line 53 (boxed Christoffersen formula): the independence LR is typeset as a *fraction*, but it must be a *difference*.**
Stated (LaTeX intact):
$$\text{LR}_{\text{ind}}=-2\Big[\tfrac{(n_{00}+n_{10})\log(1-p)+(n_{01}+n_{11})\log p}{-\;n_{00}\log(1-p_0)-n_{01}\log p_0-n_{10}\log(1-p_1)-n_{11}\log p_1}\Big]\sim\chi^2_1.$$
The `\tfrac{…}{…}` renders a ratio $\frac{\ln L_{\text{restricted}}}{-\ln L_{\text{unrestricted}}}$. The correct statistic is the **difference of the two log-likelihoods**:
$$\text{LR}_{\text{ind}}=-2\big[\underbrace{(n_{00}{+}n_{10})\log(1{-}p)+(n_{01}{+}n_{11})\log p}_{\ln L_{\text{restr}}}\;-\;\underbrace{\big(n_{00}\log(1{-}p_0)+n_{01}\log p_0+n_{10}\log(1{-}p_1)+n_{11}\log p_1\big)}_{\ln L_{\text{unrestr}}}\big].$$
The **code implements the correct difference** (lines 116–118), so only the displayed formula is wrong. (Contrast: the Kupiec formula two pages up correctly *is* a ratio $\frac{\text{null lik.}}{\text{alternative lik.}}$.) **Fix:** change `\tfrac{A}{B}` to `\big[A-\big(B\big)\big]` (i.e. `\big[(n_{00}+n_{10})\log(1-p)+(n_{01}+n_{11})\log p - n_{00}\log(1-p_0)-n_{01}\log p_0-n_{10}\log(1-p_1)-n_{11}\log p_1\big]`).

**F2 — `03-historical-simulation.md` line 71 (and `index.md` line 76): historical-simulation VaR is computed at the *6th*-worst P&L, while the boxed formula and prose say *5th*-worst.**
Stated (03 §2 line 40): *"e.g. $n=500,\ \alpha=0.99 \Rightarrow$ rank $\lceil 500\cdot0.01\rceil=5$, the 5th-worst loss"*; (03 §1 line 22): *"the 99\% VaR is (roughly) the 5th-worst of those 500 scenario P&Ls"*; (index line 39): `k=⌈n(1-α)⌉`. Hull convention is likewise 5th-worst (`corpus/verified/hull_ch19-23.md`: *"501 days → 500 scenarios, 5th-worst = 1-day 99% VaR"*).
But the code `k = math.ceil(n*(1-0.99))` evaluates to **6**, not 5: in IEEE double, `1-0.99 = 0.010000000000000009`, so `500*0.010000000000000009 = 5.0000000000000045` and `ceil → 6`. Hence `-sorted(scen)[k-1]` picks index 5 = the **6th-worst** P&L. Executed proof: for the same seed-20260910 path, **5th-worst = 3,289.54** vs **6th-worst = 3,218.55** — the documented `3,218.55` is the *6th*-worst. Page 03's own output fence (line 84) prints `(rank 6 worst)`, directly contradicting its §1/§2 prose "5th-worst"; and the code comment on line 71 (`# 5th worst P&L (ascending)`) is false (the code comment in index line 76, `# 5 -> 6th worst`, is self-contradictory but at least names the 6th).
**Fix (pick one):** (a) make the code match the stated formula — `k = round(n*(1-alpha))` or `k = n - int(math.floor(n*alpha))` / use exact integers (`n*(100-99)//100`), which yields 5 and changes the anchor value to **3,289.54**; or (b) if the 6th-worst is intended, correct the boxed formula/prose in index (line 39) and 03 (§1 line 22, §2 line 40) to state the 6th-worst convention and fix the line-71 comment. Options must be applied consistently across index and 03 (the value `3,218.55` appears in both).

### Minor (prose / citations / coherence)

**F3 — `03-historical-simulation.md` line 11: stray closing quotation mark.** `**Basic Prerequisites:** … (order statistics)."` — the trailing `"` is spurious (no opening quote). Delete it.

**F4 — `03-historical-simulation.md` line 36: subject–verb agreement.** "The empirical distribution **functions assigns** mass $1/n$ to each observation" → "function assigns".

**F5 — `04-monte-carlo-var.md` line 46: spurious author name.** "(**Halton-Glasserman** Ch 4 §4.2)" — §4.2 is Glasserman's *Antithetic Variates* (`corpus/verified/glasserman_ch4-6.md` line 49); "Halton" (a QMC sequence, Ch 5) is out of place. → "(Glasserman Ch 4 §4.2)".

**F6 — `05-failure-modes-and-practice.md` line 98: "VS" casing.** "a bias **VS-variance** tradeoff" → "bias-vs-variance" (or "bias–variance").

**F7 — `03-historical-simulation.md` line 40: likely typo "RankMetrics".** "Hull's 501-day/5th-worst convention and **RankMetrics** variants differ by interpolation convention." The evident intended referent is **RiskMetrics** (the *RiskMetrics Technical Document*, cited correctly elsewhere in the folder). → "RiskMetrics". *(Low confidence — could be a deliberate "rank" + "RiskMetrics" portmanteau, but it appears nowhere else in the repo.)*

**F8 — `index.md` line 42: stated agreement range excludes two of the three values.** "land within sampling noise of each other ($\approx 3{,}300$–$3{,}400$)" — the three values are 3,396.15 (in range), **3,218.55** (below 3,300) and **3,405.97** (above 3,400). → "$\approx 3{,}200$–$3{,}400$" or "within $\sim5\%$".

**F9 — `06-advanced-extensions.md` lines 42 & 148: equation-number attribution.** Glasserman eq. **(9.4)** (the loss quadratic $L\approx Q=a+\sum(b_jZ_j+\lambda_jZ_j^2)$) lives in **§9.1** (pp. 481–492) per `corpus/verified/glasserman_ch7-9.md` line 229, not §9.2. The §9.2 citation is correct for the *MGF/inversion and Table 9.1* material, but line 42's "diagonalization (9.4)" and line 148's "Ch 9 §9.2 (delta–gamma diagonalization (9.4)…)" misplace the equation number. *(Low severity — a citation nit, no math error.)*

**F10 — `05-failure-modes-and-practice.md` line 67 (and `index.md` line 104): the Student-$t(4)$ rate is a noisy seed-3 sample presented as "the" rate.** The block (seed 3, n=200k) yields 1.5565%, which reproduces exactly, but the analytic value is **1.5108%** (closed-form $t_4$ survival) and an independent 5M-path run gives **1.5150%**. So the sample is ~1.7σ high, and the prose claim *"~56% more tail days than promised"* is nearer **~51%** in truth. The qualitative point (fat tails breach a variance-matched normal at well above 1%) is correct and unaffected. **Fix (optional):** state the rate as "$\approx1.5\%$" (analytic), or note it is a single 200k simulation. *(Low severity — a simulation artifact, not a formula error; the code is correct.)*

---

*Generated on a single adversarial pass: 7 files read in full; 10/10 python blocks extracted, executed under Python 3.14.7, and stdout-diffed; every boxed formula, worked example and anchor constant re-derived independently; all wikilinks and corpus equation citations checked.*
