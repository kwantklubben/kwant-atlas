# Audit Report — `content/foundations/bayesian-statistics/`

Scope: 7 files (index.md + 01..06). Sole reviewer. Audited spelling/typos (prose only), every boxed formula and worked numeric example, every ` ```python ` block (run + stdout-diff), and cross-page coherence (prereqs, jargon, wikilinks, contradictions).

## 1. Verdict

**ACCEPT_WITH_FIXES.** All 7 code blocks run and their stdout matches the adjacent documented output exactly (7/7). All 26 unique wikilinks resolve. No spelling/typo issues and no doubled words found in prose. The math is almost entirely correct (Beta–Bernoulli, Normal–Normal precision-additivity, Gamma–Poisson, MAP penalty scaling, credible/predictive intervals, MH/Gibbs numerics, hierarchical shrinkage formula all re-verified). Two **substantive math errors** and two minor notation/imprecision notes require correction before the folder is considered clean:

1. **06:41** — the direction of the $n_j$ effect in the shrinkage narrative is **inverted** (contradicts the boxed formula on the same page and the page's own failure-mode #6).
2. **05:199** — the optimal RWM step-scaling exponent is **wrong** ($d^{-1/6}$ is the MALA result, not random-walk MH).
3. Minor: **index:39** notation mislabels $\mu$ as "noise".
4. Minor: **03:149** interval-width comparison mixes a 95% predictive interval with a 1-sd posterior interval for $\mu$.

## 2. Issues table

| File:Line | Problem (stated) | Correct | Severity |
|---|---|---|---|
| 06:41 | "Small $n_j$ or large $\tau^2$ $\Rightarrow$ little shrinkage; large $n_j$ or small $\tau^2$ $\Rightarrow$ strong pooling." The **$n_j$** direction is reversed. | $B_j=\sigma^2/(\sigma^2+n_j\tau^2)$, so **small** $n_j$ ⇒ **strong** shrinkage (B_j→1); **large** $n_j$ ⇒ **little** shrinkage. The $\tau^2$ clauses are correct. Contradicts the boxed formula (06:38) and failure-mode #6 (06:161: "groups with fewer observations shrink *more*"). Fix: "Small $n_j$ or small $\tau^2$ ⇒ strong pooling; large $n_j$ or large $\tau^2$ ⇒ little shrinkage." | **HIGH (math)** |
| 05:199 | "A random-walk MH scales as $O(d^{-1/6})$ optimal step decay" | For random-walk Metropolis on a product target the optimal **proposal variance scales as $d^{-1}$** ⇒ step (sd) ~ $d^{-1/2}$, optimal acceptance **0.234** (Roberts–Gelman–Gilks 1997). The $d^{-1/6}$ exponent is the MALA step-size scaling. Fix: "…scales as $O(d^{-1/2})$ step decay." | **HIGH (math)** |
| index:39 | Notation line ends "$\mu$ noise, $\tau$ signal (hierarchical)" | $\mu$ is the grand/population mean, not noise. In the hierarchy the noise variance is $\sigma^2$ (within-group), the signal variance is $\tau^2$ (between-group). Suggest "$\sigma^2$ noise, $\tau^2$ signal". | Low (notation) |
| 03:149 | "a posterior for $\mu$ of width $\pm0.06$" compared against the 95% predictive $[0.39,1.31]$ | $\mathrm{sd}[\mu\mid x]=\sqrt{s^2/n}=\sqrt{0.04/12}=0.0577$, so $\pm0.06$ is a **1-sd** statement, not a 95% interval ($\pm 0.127$). The qualitative claim (predictive wider) is correct but the contrast is apples-to-oranges. | Low (imprecision) |

No spelling typos, no doubled words, no broken sentences found in prose (code fences and LaTeX excluded).

## 3. Math verified

Every boxed formula and worked number re-derived or checked against the live code output:

- **Beta–Bernoulli**: $\mathrm{Beta}(a,b)+y/n\Rightarrow\mathrm{Beta}(a{+}y,b{+}n{-}y)$, mean $(a{+}y)/(a{+}b{+}n)$. Beta(2,2)+5/8 ⇒ Beta(7,5), mean 7/12=0.5833 ✓. Laplace rule 3/3 ⇒ 4/5 ✓.
- **Normal–Normal (known $\sigma^2$)**: precision-additivity $1/\tau_{\text{post}}^2=1/\tau^2+n/\sigma^2$; with $\tau^2{=}4,\sigma^2{=}1,n{=}10,\bar x{=}1.3$ ⇒ prec 10.25, var 0.0976, mean 1.2683 ✓ (code-verified).
- **Gamma–Poisson**: Gamma(2,1)+Σy=24,n=10 ⇒ Gamma(26,11), mean 26/11=2.3636, mode 2.2727 ✓.
- **Beta(7,5) summaries**: mean 0.5833 ✓, median 0.5881 ✓, MAP $(7{-}1)/(7{+}5{-}2)=0.6$ ✓; 95% equal-tailed CI [0.3079, 0.8325] ✓ (recomputed via NR incomplete-beta bisection; also independent check 0.3079/0.8325). Wald CI [0.2895, 0.9605] ✓.
- **Normal predictive (flat prior)**: $t_{n-1}(\bar x, s^2(1{+}1/n))$; n=12, $\bar x{=}0.85, s^2{=}0.04$ ⇒ $t_{0.975,11}=2.200985$, interval [0.3918, 1.3082] ✓; posterior for μ N(0.85, 0.003333) ✓.
- **Ridge/Gaussian-MAP**: $\lambda=\sigma^2/\tau^2=0.36/1=0.36$ ✓; normal eq. $(X^\top X+\lambda I)^{-1}X^\top y$ ✓. **Lasso/Laplace-MAP**: $\lambda=\sigma^2/b=0.36/0.12=3.00$ ✓; 7/10 coefficients exactly 0 ✓ (matches code). Coordinate-descent update $S(\rho,\lambda)/\sum x_{ij}^2$ consistent with objective $\tfrac12\|y-X\beta\|^2+\lambda\|\beta\|_1$ ✓.
- **MH on bimodal** $0.7N(-2,1)+0.3N(3,0.5^2)$: truth mean $0.7(-2){+}0.3(3)=-0.5$ ✓, variance $E[X^2]-0.25=6.275-0.25=6.025$ ✓; scale-4 run mean −0.5005, var 6.0405 ✓; scale-0.5 (poor mixing) mean −0.7246 ✓.
- **Gibbs bivariate normal** $\rho{=}0.8$: recovered corr 0.8007, means ≈0, vars ≈1 ✓.
- **Gibbs normal mean/variance**: $E[\mu]=1.1373$ vs analytic $(k_0\mu_0+n\bar y)/(k_0{+}n)=(0{+}12\cdot1.2333)/13=1.1385$ ✓ within MC error.
- **Hierarchical shrinkage**: $B_j=\sigma^2/(\sigma^2+n_j\tau^2)=1/(1+8\cdot0.824)=0.132$ ✓; Gibbs closed-form match (1.976 vs 2.022 etc.) ✓; spread 1.783→1.474 ✓.
- **Gelman–Rubin** $\hat R$ and **ESS** formulas (05:58–59) ✓.
- Bayes-factor $BF_{10}$ definition (02:61) ✓; BIC $-2\log\hat L+(\log n)d$ (ESL 7.35) ✓; FFBS backward step $p(z_t\mid z_{t+1},F_n)=p(z_t\mid z_{t+1},F_t)$ ✓.

## 4. Code run / match stats

| File | Block | Runs (exit 0) | Stdout matches doc |
|---|---|---|---|
| index.md | §3 sweep | ✓ | ✓ |
| 01-from-zero-intuition.md | belief update + grid check | ✓ | ✓ |
| 02-bayes-theorem-and-priors.md | 4 conjugate updates | ✓ | ✓ |
| 03-posterior-inference.md | mean/median/mode/CI/predictive | ✓ | ✓ |
| 04-bayesian-and-regularization.md | OLS/ridge/lasso | ✓ | ✓ |
| 05-mcmc.md | MH sweep + Gibbs bvn + Gibbs normal | ✓ | ✓ |
| 06-advanced-extensions.md | hierarchical Gibbs | ✓ | ✓ |

**7/7 blocks run successfully (stdlib only, no external deps); 7/7 stdout match the documented fences exactly.** All blocks are deterministic (fixed `random.seed`) — no timing/nondeterminism flags. No multiprocessing/fork blocks encountered.

## 5. Links & coherence

- **26 unique wikilinks, all resolve** (22 as `direct .md`, 4 via `/index.md`). No broken links.
- **Prerequisites:** index.md states folder-level prereqs (Probability & Measure Theory **and** Econometrics & Time Series) for pages 02–06, with 01 having its own smaller prereq. Each sub-page lists its own (02: 01+P&MT; 03: 02; 04: 02+Multivariable Calculus; 05: 03+Numerical Methods·Monte Carlo; 06: 05+04). No sub-page lists Econometrics explicitly despite the index claiming it is folder-level for 02–06 — minor framing tension, not a hard error (pages are internally sequenced consistently).
- **Jargon:** conjugate, posterior, marginal likelihood/evidence, MAP, credible vs confidence, full conditional, burn-in, Gelman–Rubin, ESS, FFBS, data augmentation all defined on first use. No undefined terms spotted.
- **Cross-page contradictions:** none beyond the 06:41 $n_j$ inversion (which also contradicts that page's own failure-mode #6). Numeric "verified check" column on index.md matches the sub-page outputs throughout.
- Code blocks require only `math`/`random` stdlib — runnable as documented. All "Stdlib only" claims true.
