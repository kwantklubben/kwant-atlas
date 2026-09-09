---
title: "Pillar 5 Corpus Wishlist — Portfolio Construction & Optimization"
subtopic-folder: pillar5-portfolio-optimization
pillar: 5
tags:
  - corpus-wishlist
  - portfolio-construction
  - mean-variance
  - covariance-estimation
  - black-litterman
  - risk-parity
  - hierarchical-risk-parity
  - robust-optimization
  - kelly-criterion
  - multi-asset
---

# Pillar 5 Corpus Wishlist — Portfolio Construction & Optimization

> Covers the discipline of turning forecasts and raw asset returns into *deployable, robust* allocations: MPT / mean-variance (and why naive optimizers are "estimation-error maximizers"), covariance estimation with shrinkage and random-matrix denoising, Black-Litterman Bayesian blending, risk parity / equal-risk-contribution, hierarchical risk parity, robust optimization, constraints & transaction costs, Kelly / bet sizing, and multi-asset / factor allocation.

**Target reader level:** zero → near-professional quant member. Entries below are ordered roughly by reading order within each sub-topic (foundation first). Works already in the corpus are marked **[HAVE]** — do **not** re-acquire.

---

## Legend

Status tags (per entry):
- **[HAVE]** — already owned / verified in the corpus. Acquire only if you want a second copy.
- **[MUST-HAVE]** — canonical; a member reading this pillar should read at least this paper/book.
- **[STRONG]** — very high value, recommended.
- **[OPTIONAL]** — deepening / specialist material; grab when budget allows.
- **★** — flagged cornerstone: appears on the final Priority Acquisition shortlist.

Difficulty marks (for member routing): `[intro]` foundational, `[intermediate]`, `[advanced]`, `[reference]` (a book you consult, not read cover-to-cover).

Sub-topic folders planned (mirroring `content/pillars/05-portfolio-optimization/`):
`modern-portfolio-theory-and-mean-variance`, `covariance-estimation-shrinkage-rmt`, `black-litterman`, `risk-parity-and-equal-risk-contribution`, `hierarchical-risk-parity`, `robust-portfolio-optimization`, `constraints-and-transaction-costs`, `kelly-criterion-and-bet-sizing`, `multi-asset-and-factor-allocation`.

---

## Cross-cutting "already in corpus" (do not re-acquire)

- **Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning* (2nd ed., Springer 2009)** — **[HAVE]** `[reference]` Regularization (ridge/Lasso → L1/L2 portfolio shrinkage & sparse weights) and PCA/PCR (→ factor & RMT structure). Cited from ESL throughout covariance/robustness sections.
- **Tsay, *Analysis of Financial Time Series* (Wiley)** — **[HAVE]** `[intermediate]` Factor-model covariance estimation and dimension reduction feed straight into Ledoit-Wolf factor targets.
- **Foundational math (probability, linear algebra / matrix theory, multivariable calculus & convex optimization, econometrics & time series)** — **[HAVE]** `[intro]` The Markowitz QP, Σ⁻¹MV front, SOCP/SDP robust reformulations and RMT all assume this toolbox. Boyd & Vandenberghe *Convex Optimization* lives here conceptually (reference).

---

## 1. Modern Portfolio Theory & Mean-Variance

Folder: `modern-portfolio-theory-and-mean-variance`

- **Markowitz, "Portfolio Selection," *Journal of Finance* 7(1):77–91, 1952.** ★ **[MUST-HAVE]** `[intro]` The founding quadratic-programming paper: E-V rule, efficient set, diversification. Read before anything else.
- **Markowitz, *Portfolio Selection: Efficient Diversification of Investments*, Cowles Foundation / Wiley, 1959 (2nd ed. Blackwell, 1991).** **[STRONG]** `[intro]` The book-length treatment behind the 1952 note (mean-variance geometry, semivariance discussion, diversification math).
- **Tobin, "Liquidity Preference as Behavior Toward Risk," *Review of Economic Studies* 25(2):65–86, 1958.** **[STRONG]** `[intro]` Two-fund (separation) theorem: a riskless asset + one efficient risky portfolio — the theoretical spine behind the pillar's "tangency portfolio / two-fund separation" core topic.
- **Sharpe, "Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk," *Journal of Finance* 19(3):425–442, 1964.** **[STRONG]** `[intro]` Equilibrium tangency = market portfolio; the CAPM/SML that makes Markowitz allocations priceable. (Expect heavy overlap with the factor-investing / asset-pricing pillar — treat as joint acquisition.) Follow with **Sharpe, "Mutual Fund Performance," *Journal of Business* 39(1):119–138, 1966** for the Sharpe ratio itself.
- **Merton, "An Analytic Derivation of the Efficient Portfolio Frontier," *Journal of Financial and Quantitative Analysis* 7(4):1851–1872, 1972.** **[STRONG]** `[intermediate]` Closed-form MV frontier, global-min-variance portfolio, tangency formula — the algebra members need to code the frontier.
- **Best & Grauer, "On the Sensitivity of Mean-Variance-Efficient Portfolios to Changes in Asset Means," *Review of Financial Studies* 4(2):315–342, 1991.** **[STRONG]** `[advanced]` Why a 1% mean change can produce a 50%+ weight change — the formal statement of "MVO is an estimation-error maximizer."
- **Chopra & Ziemba, "The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice," *Journal of Portfolio Management* 19(2):6–11, 1993.** **[MUST-HAVE]** `[intro]` The clean, heavily-cited empirical result: errors in **means** dominate covariances ~10–11× and variances ~2× in the MV objective. Motivates the whole pillar.
- **Michaud & Michaud, *Efficient Asset Management: A Practical Guide to Stock Portfolio Optimization and Asset Allocation*, 2nd ed., Oxford University Press, 2008 (1st ed. 1998).** ★ **[MUST-HAVE]** `[intermediate]` "Markowitz optimization en masse" — Monte-Carlo resampling to build a stable resampled frontier; the classic industry fix for optimizer instability.
- **DeMiguel, Garlappi & Uppal, "Optimal Versus Naive Diversification: How Inefficient Is the 1/N Portfolio Strategy?" *Review of Financial Studies* 22(5):1915–1953, 2009.** ★ **[MUST-HAVE]** `[intermediate]` Across 14 models / 7 datasets, **no** sophisticated optimizer beats equal weighting out-of-sample (needs ~3,000–6,000 months of data). The sobering benchmark every optimizer must be measured against.
- **Kan & Zhou, "Optimal Portfolio Choice with Parameter Uncertainty," *Journal of Financial and Quantitative Analysis* 42(3):621–656, 2007.** **[STRONG]** `[advanced]` Bayesian/moment-shrinkage three-fund rule for estimation risk; the formal answer to "what do we do about wrong inputs."
- **Sharpe, "The Sharpe Ratio," *Journal of Portfolio Management* 21(1):49–58, 1994.** **[OPTIONAL]** `[intro]` The ex-ante vs ex-post definition and sampling issues behind the metric used to judge every optimized portfolio.

## 2. Covariance Estimation, Shrinkage & Random Matrix Theory

Folder: `covariance-estimation-shrinkage-rmt`

- **Ledoit & Wolf, "Improved Estimation of the Covariance Matrix of Stock Returns with an Application to Portfolio Selection," *Journal of Empirical Finance* 10(5):603–621, 2004.** ★ **[MUST-HAVE]** `[intermediate]` The canonical analytical shrinkage of the sample covariance toward a single-index target — well-conditioned, invertible Σ for N≈T universes. Basis of sklearn's `LedoitWolf`.
- **Ledoit & Wolf, "A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices," *Journal of Multivariate Analysis* 88(2):365–411, 2004.** **[STRONG]** `[advanced]` Constant-correlation target + optimal shrinkage intensity; the mathematically cleaner companion to the JEF paper.
- **Ledoit & Wolf, "Nonlinear Shrinkage Estimation of Large-Dimensional Covariance Matrices," *Annals of Statistics* 40(2):1024–1060, 2012.** **[OPTIONAL]** `[advanced]` Oracle nonlinear shrinkage of eigenvalues — the current state of the art when members outgrow linear shrinkage. (Free at ledoit.net.)
- **Jorion, "Bayes–Stein Estimation for Portfolio Analysis," *Journal of Financial and Quantitative Analysis* 21(3):279–292, 1986.** **[STRONG]** `[intermediate]` Shrinkage toward the global-mean portfolio; the classic pre-Ledoit-Wolf result that shrinking means improves out-of-sample portfolio performance.
- **Laloux, Cizeau, Bouchaud & Potters, "Noise Dressing of Financial Correlation Matrices," *Physical Review Letters* 83(7):1467–1470, 1999.** ★ **[MUST-HAVE]** `[intermediate]` The RMT "noise dressing" result: most empirical cross-asset correlation is Marchenko–Pastur noise → the *why* behind covariance denoising.
- **Plerou, Gopikrishnan, Rosenow, Amaral, Guhr & Stanley, "Random Matrix Approach to Cross Correlations in Financial Data," *Physical Review E* 65:066126, 2002.** **[STRONG]** `[advanced]` Confirms the RMT bulk-plus-few-large-eigenvalues structure of equity correlation matrices.
- **Bouchaud & Potters, *Theory of Financial Risk and Derivative Pricing: From Statistical Physics to Risk Management*, 2nd ed., Cambridge University Press, 2003 (corrected 2011).** ★ **[STRONG]** `[intermediate]` Fat tails + the physics view of correlation matrices; RMT denoising in practical chapters. Bridges to the Extreme-Value/fat-tails pillar.
- **Potters & Bouchaud, *A First Course in Random Matrix Theory for Physicists, Engineers and Data Scientists*, Cambridge University Press, 2020.** **[OPTIONAL]** `[advanced]` The dedicated, modern RMT textbook members can actually read (Marchenko–Pastur, Wishart, eigenvalue bounds) — good when Bai–Silverstein is too dense.
- **Bai & Silverstein, *Spectral Analysis of Large Dimensional Random Matrices*, 2nd ed., Springer, 2010.** **[OPTIONAL]** `[reference]` The rigorous mathematics of Marchenko–Pastur that all the above papers lean on. For the member who wants proofs, not heuristics.

## 3. Black-Litterman

Folder: `black-litterman`

- **Black & Litterman, "Global Portfolio Optimization," *Financial Analysts Journal* 48(5):28–43, 1992.** ★ **[MUST-HAVE]** `[intermediate]` The origin: reverse optimization from market-cap equilibrium, then blend in views; produces diversified, non-extreme portfolios that fix MVO instability.
- **He & Litterman, "The Intuition Behind Black-Litterman Model Portfolios," Goldman Sachs Investment Management, 1999 (SSRN #334304).** **[MUST-HAVE]** `[intermediate]` The accessible worked intuition (which views tilt which weights, view confidence, etc.) — most practitioners learn the mechanics from this note.
- **Satchell & Scowcroft, "A Demystification of the Black–Litterman Model: Managing Quantitative and Traditional Portfolio Construction," *Journal of Asset Management* 1(2):138–150, 2000.** **[STRONG]** `[intermediate]` Clean derivation of the BL posterior and its special cases; useful second source on the math.
- **Idzorek, "A Step-by-Step Guide to the Black-Litterman Model," 2005 (SSRN #3479867).** ★ **[STRONG]** `[intermediate]` The widely-used practitioner cookbook; introduces the intuitive 0–100% view-confidence method for setting the view-uncertainty matrix Ω. Free PDF widely mirrored.

## 4. Risk Parity & Equal Risk Contribution

Folder: `risk-parity-and-equal-risk-contribution`

- **Qian, "Risk Parity Portfolios: Efficient Portfolios Through True Diversification," PanAgora Asset Management, 2005.** ★ **[MUST-HAVE]** `[intro]` The conceptual origin: why 60/40 is secretly ~90/10 *equity* risk; equalize risk, not dollars, then lever up.
- **Qian, "On the Financial Interpretation of Risk Contribution: Risk Budgets Do Add Up," *Journal of Investment Management* 4(4), 2006 (SSRN #684221).** **[STRONG]** `[intermediate]` Formalizes marginal / percentage contribution to risk so ERC and risk budgeting are well-defined — the mathematical glue.
- **Maillard, Roncalli & Teïletche, "The Properties of Equally Weighted Risk Contribution Portfolios," *Journal of Portfolio Management* 36(4):60–70, 2010.** ★ **[MUST-HAVE]** `[intermediate]` The ERC formalization: existence, uniqueness, relation to MV & 1/N, and why ERC sits between them. The paper that made ERC a discipline.
- **Asness, Frazzini & Pedersen, "Leverage Aversion and Risk Parity," *Financial Analysts Journal* 68(1):47–59, 2012.** **[STRONG]** `[intermediate]` A theory of *why* risk parity can earn a premium (leverage-averse investors bid up risky assets → safer assets earn higher risk-adjusted returns).
- **Roncalli, *Introduction to Risk Parity and Budgeting*, Chapman & Hall/CRC Financial Mathematics Series, 2013.** ★ **[STRONG]** `[intermediate]` The definitive book-length treatment: risk contribution math, ERC algorithms, risk budgeting, long-only constraints, and cross-asset examples. Covers far more than risk parity alone (also useful for HRP foundations).

## 5. Hierarchical Risk Parity

Folder: `hierarchical-risk-parity`

- **López de Prado, "Building Diversified Portfolios that Outperform Out-of-Sample," *Journal of Portfolio Management* 42(4):59–69, 2016.** ★ **[MUST-HAVE]** `[intermediate]` HRP itself: correlation-distance + tree clustering + recursive bisection, never inverting a covariance matrix → robust when N>T and to estimation error. Compares favorably to MVO/RP out-of-sample.
- **López de Prado, *Advances in Financial Machine Learning*, Wiley, 2018 (Chs. 16–17).** **[STRONG]** `[intermediate]` The canonical book chapter exposition of HRP and the Hierarchical Equal Risk Contribution (HERC) extension, plus the information-theoretic/clustering machinery. **Cross-pillar:** this book is central to the ML & alternative-data pillar too — coordinate acquisition rather than double-buy.
- **Raffinot, "Hierarchical Clustering-Based Asset Allocation," *Journal of Portfolio Management* 44(2):89–99, 2017/18 (special multi-asset issue).** **[STRONG]** `[advanced]` HACA — graph-partitioning alternative to HRP using a hierarchical clustering *based* on a factor model; the natural next step after HRP for a practitioner exploring the cluster family. (Follow with his 2022 "Hierarchical Clustering-Based Risk Parity.")

## 6. Robust Portfolio Optimization

Folder: `robust-portfolio-optimization`

- **Goldfarb & Iyengar, "Robust Portfolio Selection Problems," *Mathematics of Operations Research* 28(1):1–38, 2003.** ★ **[MUST-HAVE]** `[advanced]` The seminal deterministic robust-MVO paper: model parameters as uncertain-but-bounded, worst-case formulations that stay tractable (SOCP/SDP) and dramatically reduce weight instability.
- **Fabozzi, Kolm, Pachamanova & Focardi, *Robust Portfolio Optimization and Management*, Wiley, 2007.** ★ **[STRONG]** `[reference]` The broad, unified book: estimation error, resampling vs robust vs BL, robust estimation of inputs, and practical QP/SOCP formulations. A reference shelf item for the whole pillar.
- **Tütüncü & Koenig, "Robust Asset Allocation," *Annals of Operations Research* 132:157–187, 2004.** **[OPTIONAL]** `[advanced]` Robust reformulations of MV and VaR/CVaR-constrained allocation against uncertainty in moments; complements Goldfarb-Iyengar.
- **Ben-Tal, El Ghaoui & Nemirovski, *Robust Optimization*, Princeton University Press, 2009.** **[OPTIONAL]** `[reference]` The general robust-optimization math (uncertainty sets, robust counterparts, tractability). Not finance-specific — background [HAVE]-adjacent, grab only if a member dives into theory.

## 7. Constraints & Transaction Costs

Folder: `constraints-and-transaction-costs`

- **Lobo, Fazel & Boyd, "Portfolio Optimization with Linear and Fixed Transaction Costs," *Annals of Operations Research* 152:341–365, 2007.** ★ **[MUST-HAVE]** `[intermediate]` Convex formulations (incl. nonconvex-fixed-cost relaxation) of cost-aware allocation — the modeling backbone of the "quadratic market-impact penalty" core topic. Free PDF at Stanford (Boyd's site).
- **Gârleanu & Pedersen, "Dynamic Trading with Predictable Returns and Transaction Costs," *Journal of Finance* 68(6):2309–2340, 2013.** ★ **[STRONG]** `[advanced]` The optimal dynamic policy: trade partially toward an "aim" portfolio *ahead* of the current target when costs are proportional to turnover; closed form. Bridges portfolio construction → execution (see cross-pillar note below).
- **Almgren & Chriss, "Optimal Execution of Portfolio Transactions," *Journal of Risk* 3(2):5–39, 2000/01.** **[STRONG]** `[intermediate]` Permanent + temporary impact model and the efficient trading frontier. **Cross-pillar:** fully owned by Pillar 2 (optimal execution) — treat as a shared reference, not a double acquisition here.
- **Grinold & Kahn, *Active Portfolio Management: A Quantitative Approach for Producing Superior Returns and Controlling Risk*, 2nd ed., McGraw-Hill, 2000.** ★ **[MUST-HAVE]** `[reference]` The practitioner's bible for turning forecasts into constrained active portfolios: alpha/beta, tracking error, transfer coefficient, transaction-cost-adjusted rebalancing, and the Fundamental Law context. The single most-cited book in portfolio construction — worth owning pillar-wide.
- **Grinold, "The Fundamental Law of Active Management," *Journal of Portfolio Management* 15(3):30–37, 1989.** **[MUST-HAVE]** `[intermediate]` IR ≈ IC × √breadth — the law that ties signal quality and breadth to achievable active performance.
- **Clarke, de Silva & Thorley, "Portfolio Constraints and the Fundamental Law of Active Management," *Financial Analysts Journal* 58(5):48–66, 2002.** **[STRONG]** `[advanced]` Introduces the transfer coefficient (TC) — how long-only, turnover, and other constraints "leak" value so realized IR < IR_max. The bridge between raw optimization theory and what constraints actually cost. (Also valuable under Pillar 1.)

## 8. Kelly Criterion & Bet Sizing

Folder: `kelly-criterion-and-bet-sizing`

- **Kelly, "A New Interpretation of Information Rate," *Bell System Technical Journal* 35(4):917–926, 1956.** ★ **[MUST-HAVE]** `[intro]` The source: maximizing expected log-growth rate (E log W) as the bet-sizing objective; growth-optimal but aggressive without de-rating. Free scans at archive.org / Princeton.
- **Thorp, "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market," in *Handbook of Asset and Liability Management*, Vol. 1 (Zenios & Ziemba eds.), North-Holland, 2006; repr. in MacLean–Thorp–Ziemba (2011).** **[MUST-HAVE]** `[intermediate]` The definitive practical treatment: fractional Kelly, edge/odds sizing, ruin avoidance, and application to securities. Free PDF at gwern.net.
- **MacLean, Thorp & Ziemba (eds.), *The Kelly Capital Growth Investment Criterion: Theory and Practice*, World Scientific, 2011.** **[STRONG]** `[reference]` The anthology collecting the key Kelly literature (Kelly, Breiman, Thorp, MacLean–Ziemba "good/bad properties") in one volume — ideal if members want breadth without hunting scattered papers.

## 9. Multi-Asset & Factor Allocation

Folder: `multi-asset-and-factor-allocation`

- **Ang, *Asset Management: A Systematic Approach to Factor Investing*, Oxford University Press, 2014.** ★ **[MUST-HAVE]** `[intermediate]` The modern canonical text on allocating across asset classes *and* factor premia (value, momentum, carry, defensive, etc.) rather than mere asset-class labels. Bridges Pillars 1 (factor models) and 5 (how to hold them).
- **Meucci, *Risk and Asset Allocation*, Springer Finance, 2005.** ★ **[STRONG]** `[intermediate]` Univariate/multivariate statistics → copulas → flexible allocation, including the original and extended Black-Litterman treatments. A rigorous single-text backbone for the pillar's statistical side.
- **Qian, Hua & Sorensen, *Quantitative Equity Portfolio Management: Modern Techniques and Applications*, Chapman & Hall/CRC, 2007.** **[STRONG]** `[intermediate]` QEPM: factor-based expected returns, active risk budgeting, and constrained portfolio construction in one applied text — good industry-style companion to Grinold-Kahn.
- **Ilmanen, *Expected Returns: An Investor's Guide to Harvesting Market Rewards*, Wiley, 2011.** **[OPTIONAL]** `[intro]` A practical tour of what premium each asset class / factor is actually paying and why — ideal for zero-to-intermediate members choosing *which* building blocks to allocate across before optimizing.

---

## Priority Acquisition (top ~12)

Top-tier, pillar-critical works to acquire first. Order = expected value per dollar for this member population. Cross-pillar items noted to avoid double-buying.

1. **Markowitz (1952), "Portfolio Selection"** — the founding paper; cheap/free, read by everyone. `$0` PDF (JSTOR).
2. **Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (2000)** — the pillar-wide reference book on constrained portfolio construction. Buy hard copy.
3. **Ledoit & Wolf (2004), *J. Empirical Finance* "Improved Estimation of the Covariance Matrix…"** — the workhorse Σ estimator. `$0` (ledoit.net).
4. **Black & Litterman (1992), "Global Portfolio Optimization"** — canonical; scannable from institutional archives.
5. **Laloux et al. (1999), *PRL* "Noise Dressing of Financial Correlation Matrices"** — the RMT motivation. `$0` (arXiv cond-mat/9810255).
6. **Maillard, Roncalli & Teïletche (2010), "The Properties of Equally Weighted Risk Contribution Portfolios"** — ERC formalization. Free SSRN/publisher draft.
7. **López de Prado (2016), "Building Diversified Portfolios that Outperform Out-of-Sample"** — HRP. SSRN preprint `$0`.
8. **Ang, *Asset Management* (2014)** — factor allocation synthesis. Buy.
9. **Michaud & Michaud, *Efficient Asset Management*, 2nd ed. (2008)** — resampling / error-aware optimization. Buy.
10. **DeMiguel, Garlappi & Uppal (2009), "Optimal Versus Naive Diversification"** — the 1/N benchmark every optimizer must beat. Free.
11. **Meucci, *Risk and Asset Allocation* (2005)** — rigorous statistics + BL backbone. Buy (out-of-print copies circulate; PDF widely mirrored at arpm.co).
12. **Roncalli, *Introduction to Risk Parity and Budgeting* (2013)** — if risk parity is a chosen depth area, this is the one book that covers ERC + risk budgeting comprehensively. Buy.

**Coordinate / de-dupe across pillars:** Grinold-Kahn & the Fundamental-Law family and Clarke-de-Silva-Thorley overlap Pillar 1 (quantitative research); Almgren-Chriss overlaps Pillar 2 (execution); López de Prado *AFML* overlaps Pillar 7 (ML/alt-data); Bouchaud-Potters and fat-tails overlap Pillar 4 (risk). Decide a single owner per work and let other pillars reference it.
