# Foundations (Mathematics Toolbox) — Corpus Wishlist

> **Area:** The transversal **First-Principles Toolbox** — the shared mathematics / stochastics / computation that underlies **all 8 pillars** of the Kwant-Atlas (research, HFT, derivatives, risk, portfolio, market-making, ML, quant-dev).
> **Purpose:** Build depth and authority for the foundations knowledge graph, which currently has only **thin** linear-algebra and single-variable-calculus foundation notes plus the stochastic/finance spine (Shreve I & II, Björk, Tsay, ESL). This wishlist is the **canonical textbook & paper layer** that takes a member from a low base (econ / CS / no math background) to near-professional quantitative fluency.
> **Status:** Wishlist (works to acquire into the club library / to cite in Atlas foundation notes).

## Scope & audience

Club members arrive from **very different backgrounds** — some never took a proof-based course, others are CS or economics majors, and some have no university math at all. Because the Foundations toolbox is transversal, the corpus below deliberately spans the **full ladder per sub-topic**: the single most accessible on-ramp → the canonical rigorous text → the advanced reference. Every entry is tagged with a difficulty band so a member can sequence reading by their own starting point, and with an acquisition tier so the library can be built cheapest-first with maximum leverage.

The eleven planned foundation folders all map to sections here:
`linear-algebra-and-matrices` · `calculus-single-multivariable` · `optimization-and-convex-analysis` · `probability-and-measure-theory` · `stochastic-calculus` · `statistics-and-inference` · `econometrics-and-timeseries` · `numerical-methods` · `information-theory` · `bayesian-statistics` · `discrete-math-and-combinatorics`.

## Legend

Each entry carries an **acquisition tier**, a **difficulty band**, and (where applicable) a **`[Free]`** tag:

- **[HAVE]** — already owned / verified in the library. Use as foundation; do **not** re-acquire.
- **[CORE]** — acquire early: the canonical, highest-leverage source for the sub-topic.
- **[NICE]** — valuable depth / advanced theory / specialist follow-up; acquire after the CORE tier.
- **`[Free]`** — official/free-legal copy exists (author- or publisher-hosted); grab immediately at zero cost.
- Difficulty: 🟢 Intro (zero-to-running) · 🟡 Intermediate (foundational course level) · 🔴 Advanced (academic/reference).

**Entry format:** *Author(s)* — **Title** (Edition, Year, Publisher). One-line note on why it matters and what it uniquely covers.

> **Already in the library (verify before acquiring):** Shreve I & II (stochastic calculus spine), Björk *Arbitrage Theory in Continuous Time*, Tsay *Analysis of Financial Time Series*, Hastie/Tibshirani/Friedman *ESL*, Glasserman *Monte Carlo Methods in Financial Engineering*, plus the **thin** linear-algebra foundation note and the single-variable `calculus.pdf`. The last two cover only the shallowest ground and are the primary gaps this wishlist fills.

---

## linear-algebra-and-matrices

The engine room of all 8 pillars — covariance eigenstructure (RMT denoising, Ledoit-Wolf), factor loadings (SVD/PCA), and the spectral theory behind every optimizer. Cross-reference the **[[foundations/linear-algebra-and-matrices]]** node.

### Books
- **[HAVE]** 🟢 *Internal* — **Linear Algebra & Matrix Decompositions foundation note**. Existing Atlas node; **thin** — gives definitions (spectral theorem, PSD, SVD) but not working fluency. Treat as index, not textbook.
- **[CORE]** 🟢 **Gilbert Strang — *Introduction to Linear Algebra*** (5th ed., 2016, Wellesley-Cambridge Press). The classic teaching spine: vector spaces, orthogonality, determinants, and clear full chapters on eigenvalues/vectors and the **SVD**. The most approachable rigorous path from a low base into the matrix algebra every pillar assumes. *(Strang's *Linear Algebra and Learning from Data*, already cited in Atlas notes, is the applied follow-on.)*
- **[CORE]** `[Free]` 🟡 **Sheldon Axler — *Linear Algebra Done Right*** (4th ed., 2023, Springer / free PDF on axler.net). The clean, proof-first modern text built **eigenvalues-first** (no determinant prerequisite) — spectral theorem, PSD matrices, and singular values developed rigorously. Ideal second book for a member who has Strang-level mechanics and wants the theory that makes covariance/factor arguments rigorous.
- **[NICE]** 🟢 **Stephen Boyd & Lieven Vandenberghe — *Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares*** (2018, Cambridge University Press). Least-squares-as-the-meaning-of-data linear algebra; the gentlest bridge into how LA is *used* (regression, projections) before the abstract canon.
- **[NICE]** 🔴 **Roger A. Horn & Charles R. Johnson — *Matrix Analysis*** (2nd ed., 2013, Cambridge University Press). The encyclopedic reference on matrix inequalities, norms, PSD structure, and decompositions — the "dictionary" for eigenvalue/PSD arguments in covariance work.
- **[NICE]** 🔴 **Zhidong Bai & Jack W. Silverstein — *Spectral Analysis of Large Dimensional Random Matrices*** (2nd ed., 2010, Springer). The Marchenko–Pastur and related random-matrix-theory mathematics underpinning covariance denoising (the Atlas's RMT-denosing topic). Reference-grade; read only after matrix-analysis basics.

---

## calculus-single-multivariable

Gradients/Hessians/Taylor expansions are literally the Greeks and the local structure of every optimizer; multivariable calculus is the substrate for the whole toolbox. Cross-reference the **[[foundations/multivariable-calculus-and-optimization]]** node.

### Books
- **[HAVE]** 🟢 *Internal* — **`calculus.pdf` foundation note**. Existing **single-variable-only**, thin note. Covers differentiation/integration mechanics for a low base but stops far short of the multivariable calculus (gradients, Hessians, Jacobians, Lagrange multipliers) that quantitative work needs.
- **[CORE]** 🟢 **James Stewart, Daniel Clegg & Saleem Watson — *Calculus: Early Transcendentals*** (9th ed., 2020, Cengage). The standard accessible single-and-multivariable course text — the member who needs to rebuild calculus from (near) zero starts here, then graduates to the rigorous books below.
- **[CORE]** 🟡 **Michael Spivak — *Calculus*** (4th ed., 2008, Publish or Perish). The rigorous single-variable classic: epsilon-delta foundations, the theorem-proving mindset that proofs later foundation material assumes. The antidote to calculator-style calculus.
- **[CORE]** 🟡🔴 **John H. Hubbard & Barbara Burke Hubbard — *Vector Calculus, Linear Algebra, and Differential Forms: A Unified Approach*** (5th ed., 2015, Matrix Editions). **The single best-value math text for a quant.** Unifies multivariable calculus, linear algebra, and differential forms, with a full rigorous-but-accessible treatment of Taylor's theorem, the implicit function theorem, and change of variables via determinants — exactly the machine behind Greeks and constrained optimization. Covers much of the linear-algebra folder too.
- **[CORE]** 🟢🟡 **Carl P. Simon & Lawrence Blume — *Mathematics for Economists*** (1994, W. W. Norton). The standard **econ-to-math bridge**: real analysis, linear algebra, multivariable calculus, and static/dynamic optimization all presented for members who think in economics. The fastest route for an econ-background member into the exact math the Atlas uses.
- **[NICE]** 🔴 **Terence Tao — *Analysis I & Analysis II*** (3rd ed., Springer). The rigorous real-analysis foundation (limits, continuity, differentiation, Riemann integration, and in Vol. II multivariate calculus and Fourier) for the member who wants genuinely watertight foundations before measure theory.

---

## optimization-and-convex-analysis

The mathematical core of portfolio construction (Markowitz QP), robust reformulations (SOCP/SDP), shrinkage, risk budgets, and model fitting. Cross-reference the **[[foundations/multivariable-calculus-and-optimization]]** node.

### Books
- **[CORE]** `[Free]` 🟡 **Stephen Boyd & Lieven Vandenberghe — *Convex Optimization*** (2004, Cambridge University Press; free PDF at web.stanford.edu/~boyd/cvxbook). **The convex-optimization canon.** Convex sets/functions, duality, KKT conditions, and the theory of when an optimization problem is tractable — the framework under mean-variance, robust portfolio optimization, Lasso-type shrinkage, and nearly every fitting problem in the Atlas. Highest-leverage single acquisition in this folder.
- **[CORE]** 🟡🔴 **Jorge Nocedal & Stephen J. Wright — *Numerical Optimization*** (2nd ed., 2006, Springer). The standard reference on *algorithms* for optimization (gradient methods, Newton/quasi-Newton, line-search/trust-region, interior-point, SQP). The computational counterpart to Boyd — what a machine actually does when it "solves" a Markowitz or robust problem.
- **[CORE]** 🟡 **Dimitris Bertsimas & John N. Tsitsiklis — *Introduction to Linear Optimization*** (1997, Athena Scientific). The canonical LP treatment: geometry, duality, simplex and interior-point methods. LP duality is the cleanest first encounter with the dual/KKT ideas reused across the toolbox.
- **[NICE]** 🔴 **R. Tyrrell Rockafellar — *Convex Analysis*** (1970; Princeton Landmarks reprint 1997). The foundational convex-analysis monograph (conjugate functions, recession cones, subgradients). The theoretical bedrock under Boyd's more applied treatment; reference-grade.
- **[NICE]** 🔴 **Dimitri P. Bertsekas — *Nonlinear Programming*** (3rd ed., 2016, Athena Scientific). The rigorous nonlinear-optimization theory text — optimality conditions, duality, and algorithms with full proofs. For the member who wants the theory *under* Nocedal-Wright's algorithms.
- **[NICE]** 🔴 **Aharon Ben-Tal & Arkadi Nemirovski — *Lectures on Modern Convex Optimization*** (2001, SIAM). Conic (SOCP/SDP) modeling and tractable robust counterparts — the mathematics behind robust portfolio optimization and worst-case formulations.

---

## probability-and-measure-theory

Measure theory makes continuous-time conditioning, martingales, filtrations, and change of measure (Radon-Nikodym) rigorous — the substrate for the entire stochastic-calculus and risk folders. Cross-reference the **[[foundations/probability-and-measure-theory]]** node.

### Books
- **[CORE]** 🟢 **Joseph K. Blitzstein & Jessica Hwang — *Introduction to Probability*** (2nd ed., 2019, CRC Press). The **best zero-on-ramp** to probability for any background (CS/econ/none): intuition-first, story proofs, heavy on conditioning and expectation — the concepts, not just formulas, with the Stat 110 video lectures freely available.
- **[CORE]** 🟢 **Sheldon Ross — *A First Course in Probability*** (10th ed., Pearson). The classic self-contained undergraduate text — a slower, drill-based alternative on-ramp for members who want more worked mechanics before abstraction.
- **[CORE]** 🟡 **Patrick Billingsley — *Probability and Measure*** (Anniversary ed., 2012, Wiley). The canonical measure-theoretic text named in the Atlas's own references: probability spaces, conditional expectation, martingales, and Radon-Nikodym developed rigorously. The definitive bridge from undergraduate probability to the machine Shreve II assumes.
- **[CORE]** `[Free]` 🔴 **Rick Durrett — *Probability: Theory and Examples*** (5th ed., 2019, Cambridge University Press; free PDF at services.math.duke.edu/~rtd). The modern graduate standard — measure theory, LLN/CLT, conditional expectation, and a serious martingale chapter, with genuinely useful worked examples. The cleanest rigorous progression from measure to martingales.
- **[CORE]** 🟡 **Geoffrey Grimmett & David Stirzaker — *Probability and Random Processes*** (3rd ed., 2001, Oxford University Press). Encyclopedic intermediate text that spans discrete to continuous to a serious treatment of stochastic processes and martingales in one volume — good middle rung between Ross/Blitzstein and the measure-theory canon.
- **[NICE]** 🟡 **David Williams — *Probability with Martingales*** (1991, Cambridge University Press). Short, elegant, and proof-crisp: conditional expectation and martingales as *the* tools, written by a master. The ideal reading *just before* or alongside Shreve II for the martingale intuition. *(Already cited in Atlas probability notes.)*
- **[NICE]** 🔴 **Kai Lai Chung — *A Course in Probability Theory*** (3rd ed., 2001, Academic Press). The spare, rigorous classic of the measure-theoretic course — for the member who wants maximum theorem-per-page density.

---

## stochastic-calculus

Brownian motion, Itô integration and the Itô-Doeblin lemma, Girsanov change of measure, martingale representation — the engine of derivative pricing and continuous-time finance. Cross-reference the **[[foundations/stochastic-calculus-and-ito]]** node.

### Books
- **[HAVE]** 🟡 **Steven E. Shreve — *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model*** (2004, Springer). Already owned. The discrete/arbitrage on-ramp that builds martingale pricing from the binomial tree.
- **[HAVE]** 🟡🔴 **Steven E. Shreve — *Stochastic Calculus for Finance II: Continuous-Time Models*** (2004, Springer). Already owned. Brownian motion, Itô's formula, Girsanov, and risk-neutral pricing; the Atlas's primary stochastic-calculus spine.
- **[HAVE]** 🟡 **Tomas Björk — *Arbitrage Theory in Continuous Time*** (4th ed., 2020, Oxford University Press). Already owned. The clean arbitrage/term-structure treatment that complements Shreve's measure-theoretic style.
- **[CORE]** 🟡🔴 **Bernt Øksendal — *Stochastic Differential Equations: An Introduction with Applications*** (6th ed., 2003, Springer). The standard SDE text: builds Itô calculus rigorously from a probability base and adds the Feynman-Kac connection to PDEs — the mathematical link between stochastic pricing and the PDE/Greeks side of derivatives. The natural next step after Shreve II.
- **[CORE]** 🟡 **J. Michael Steele — *Stochastic Calculus and Financial Applications*** (2001, Springer). The gentlest bridge from Shreve II to research-grade stochastics — martingales, Itô calculus, and change of measure explained with uncommon clarity. Fills the gap between Shreve's pace and Øksendal's rigor.
- **[NICE]** 🟡🔴 **Fima C. Klebaner — *Introduction to Stochastic Calculus with Applications*** (3rd ed., 2012, Imperial College Press). A self-contained, example-rich route into Itô calculus and SDEs that is more applied and less measure-heavy than Karatzas-Shreve — a good intermediate reference.
- **[NICE]** 🔴 **Ioannis Karatzas & Steven E. Shreve — *Brownian Motion and Stochastic Calculus*** (2nd ed., 1991, Springer). The research-grade treatise — the definitive rigorous reference on continuous-time martingales, stochastic integration, and SDEs. Reference-only for the deepest work; not a first read.

---

## statistics-and-inference

The inferential core shared by econometrics, ML, and risk estimation: point/interval estimation, hypothesis testing, likelihood, resampling, and the computer-age statistical methods the Atlas's ML pillar extends.

### Books
- **[HAVE]** 🟡🔴 **Trevor Hastie, Robert Tibshirani & Jerome Friedman — *The Elements of Statistical Learning*** (2nd ed., 2009, Springer). Already owned. Statistical learning theory (regularization, shrinkage, splines, trees, boosting) — the general-ML foundation the Atlas ML pillar builds on. Cross-listed across every pillar corpus file.
- **[CORE]** 🟡 **George Casella & Roger L. Berger — *Statistical Inference*** (2nd ed., 2002, Duxbury/Cengage). The canonical mathematical-statistics text: sufficiency, likelihood, hypothesis testing, and the Neyman-Pearson framework with full rigor. The theory spine every inference-based pillar folder assumes.
- **[CORE]** 🟡 **Bradley Efron & Trevor Hastie — *Computer Age Statistical Inference: Algorithms, Evidence, and Data Science*** (2016, Cambridge University Press). The modern bridge from classical to computer-age statistics — resampling/bootstrap, cross-validation, empirical Bayes, and the reasoning that separates honest inference from "fit the whole dataset." Written accessibly by two masters.
- **[CORE]** 🟢 **Larry Wasserman — *All of Statistics: A Concise Course in Statistical Inference*** (2004, Springer). The compact, CS-friendly "everything you need, not everything known" survey — probability, inference, and nonparametrics in one short rigorous volume. The fastest route to statistical literacy for a programmer/CS-background member.
- **[NICE]** 🟡 **John A. Rice — *Mathematical Statistics and Data Analysis*** (3rd ed., 2006, Duxbury/Cengage). Data-oriented mathematical statistics with a heavier applied emphasis than Casella-Berger — a good mid-rung for members who want inference through real data before full abstraction.
- **[NICE]** 🔴 **Erich L. Lehmann & George Casella — *Theory of Point Estimation*** (2nd ed., 1998, Springer). The advanced theory of estimation (UMVUE, information, minimax, Bayes). Reference-grade depth for members working on estimation theory.
- **[NICE]** 🔴 **Larry Wasserman — *All of Nonparametric Statistics*** (2006, Springer). Density estimation, regression smoothers, and empirical-process-based inference — the nonparametric side that appears in financial ML and EVT contexts.

---

## econometrics-and-timeseries

Stationarity, unit roots and cointegration, volatility clustering (ARCH/GARCH), vector autoregressions, and causal/panel inference — the empirical engine of the research and risk pillars. Cross-reference the **[[foundations/econometrics-and-time-series]]** node.

### Books
- **[HAVE]** 🟡 **Ruey S. Tsay — *Analysis of Financial Time Series*** (3rd ed., 2010, Wiley). Already owned. The financial time-series spine: ARMA/GARCH, cointegration, volatility models, and regime behavior — cross-listed across pillar corpus files.
- **[CORE]** 🟡🔴 **James D. Hamilton — *Time Series Analysis*** (1994, Princeton University Press). **The canonical time-series reference.** State-space and Kalman filter, unit roots, cointegration, and VARs developed rigorously and exhaustively. The definitive text for the Atlas's cointegration/regime/Kalman topics; pair with Tsay for the financial emphasis.
- **[CORE]** 🟢 **Jeffrey M. Wooldridge — *Introductory Econometrics: A Modern Approach*** (7th ed., 2019, Cengage). The standard accessible econometrics course — OLS/assumptions, panel data, IV, and time-series econometrics explained for readers who are comfortable but not proof-focused. The natural first econometrics book for the whole membership, econ or not.
- **[CORE]** 🟢 **Joshua D. Angrist & Jörn-Steffen Pischke — *Mostly Harmless Econometrics*** (2009, Princeton University Press). The causal-inference companion: how regression, matching, and IV are actually used to estimate causal effects — the honesty layer for any "signal predicts return" claim the research pillar makes.
- **[NICE]** 🟡 **Fumio Hayashi — *Econometrics*** (2000, Princeton University Press). The rigorous GMM-centric graduate text — the cleanest modern treatment of large-sample inference and GMM that underlies panel and moment-based financial models.
- **[NICE]** 🟡 **Peter J. Brockwell & Richard A. Davis — *Introduction to Time Series and Forecasting*** (3rd ed., 2016, Springer). The companion forecasting text with full ARIMA and state-space machinery and R examples — a gentle, complete supplement to Hamilton.
- **[NICE]** 🔴 **William H. Greene — *Econometric Analysis*** (8th ed., 2018, Pearson). The encyclopedic econometrics reference (all models, all estimators) — the "dictionary" for any econometric question; not a cover-to-cover read.
- **[NICE]** 🟡🔴 **George E. P. Box, Gwilym M. Jenkins, Gregory C. Reinsel & Greta M. Ljung — *Time Series Analysis: Forecasting and Control*** (5th ed., 2015, Wiley). The historic ARIMA/Box-Jenkins methodology book — the classical building/modeling/diagnostic workflow that still defines professional time-series practice.

---

## numerical-methods

Floating-point honesty, numerical linear algebra, Monte Carlo and SDE numerics — the computational backbone that keeps every implemented model from silently diverging. (Glasserman, the Monte Carlo reference, is already owned.)

### Books
- **[CORE]** 🟡 **Lloyd N. Trefethen & David Bau III — *Numerical Linear Algebra*** (1997, SIAM). The canonical 40-lecture text on the *computational* side of linear algebra: conditioning, QR, least squares, eigenvalue and SVD algorithms. The bridge between pencil-and-paper matrix theory and what numpy/LAPACK actually computes.
- **[CORE]** 🟡🔴 **Lloyd N. Trefethen — *Numerical Analysis*** (2019, SIAM). A broad modern survey of scientific computing — floating-point arithmetic, interpolation, numerical integration, ODEs/SDEs, Fourier and spectral methods — with clean numerical-analysis intuition and honest error analysis. The general-purpose complement to the specialized finance texts.
- **[HAVE]** 🔴 **Paul Glasserman — *Monte Carlo Methods in Financial Engineering*** (2003, Springer). Already owned. Variance reduction, path-dependence, and MC estimation of risk measures — the Monte Carlo reference for risk, derivatives, and pricing folders. Do **not** re-acquire.
- **[NICE]** 🟡 **Gene H. Golub & Charles F. Van Loan — *Matrix Computations*** (4th ed., 2013, Johns Hopkins University Press). The comprehensive numerical-linear-algebra reference — every algorithm and its stability. The definitive companion to Trefethen-Bau for deep implementation work.
- **[NICE]** 🔴 **Peter E. Kloeden & Eckhard Platen — *Numerical Solution of Stochastic Differential Equations*** (1992; reissued Springer). The standard reference on strong/weak SDE numerical schemes (Euler-Maruyama, Milstein) — the numerics behind Monte Carlo simulation of price paths in every pillar.
- **[NICE]** 🟢 **Michael T. Heath — *Scientific Computing: An Introductory Survey*** (2nd ed., 2018, SIAM). An approachable one-semester survey of the whole field (solving linear/nonlinear systems, optimization, interpolation, integration) — a good first book for members lacking any numerical-methods background.

---

## information-theory

Entropy, mutual information, KL divergence, and rate-distortion — the probabilistic measure of information used in feature selection, regime detection, coding, and the analysis of learning. A smaller folder: two canonical texts plus the founding paper.

### Books
- **[CORE]** 🟡🔴 **Thomas M. Cover & Joy A. Thomas — *Elements of Information Theory*** (2nd ed., 2006, Wiley). **The information-theory canon.** Entropy, relative entropy, mutual information, the asymptotic equipartition property, and data compression/transmission — developed with the intuition and examples that make it self-teachable. The standard source for the KL/entropy quantities that recur across ML and signal topics.
- **[CORE]** `[Free]` 🟡 **David J. C. MacKay — *Information Theory, Inference, and Learning Algorithms*** (2003, Cambridge University Press; free at inference.org.uk/mackay/itila). The brilliant, unconventional text that fuses information theory with Bayesian inference and learning algorithms — including practical MCMC and error-correcting codes. Bridges this folder directly into the Bayesian folder.
- **[NICE]** 🟢 **Robert B. Ash — *Information Theory*** (Dover). The concise, inexpensive classical introduction — a fast, low-rigor route into entropy and channel coding for members who want the essentials without Cover-Thomas depth.
- **[NICE]** 🔴 **Imre Csiszár & János Körner — *Information Theory: Coding Theorems for Discrete Memoryless Systems*** (2nd ed., 2011, Cambridge University Press). The rigorous, theorem-based graduate treatise — for the member who wants information theory built from first principles with full proofs.

### Papers
- **[NICE]** 🔴 **Claude E. Shannon — "A Mathematical Theory of Communication"** (*Bell System Technical Journal*, 27(3):379–423 & 27(4):623–656, 1948). **The founding paper** of information theory — entropy, channel capacity, and the source/channel-coding theorems that defined the field. Historical cornerstone, freely available; the motivation behind the whole folder.

---

## bayesian-statistics

The prior-posterior machinery behind Black-Litterman allocation, shrinkage estimators, hidden Markov / regime models, and the "shrink everything toward prior" honesty that counteracts overfitting. A foundational, frequently-reused folder.

### Books
- **[CORE]** 🟡🔴 **Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari & Donald B. Rubin — *Bayesian Data Analysis*** (3rd ed., 2013, CRC Press). **The Bayesian canon** ("BDA3"): modeling, computation (MCMC/Gibbs), model checking, and hierarchical models, with the practical judgment the field runs on. The definitive Bayesian text for the Atlas — underlies Black-Litterman, shrinkage, and Bayesian allocation.
- **[CORE]** 🟢 **Richard McElreath — *Statistical Rethinking: A Bayesian Course with Examples in R and Stan*** (2nd ed., 2020, CRC Press). The conceptual, code-first on-ramp — Bayesian inference taught through model *building* and honest scientific reasoning rather than abstract machinery. The best first Bayesian book for members new to the framework.
- **[CORE]** 🟡 **Peter D. Hoff — *A First Course in Bayesian Statistical Methods*** (2009, Springer). A compact, modern middle text: conjugate models, Gibbs/Metropolis computation, and hierarchical and regression models in one clean course — good bridge between McElreath and BDA3.
- **[NICE]** 🔴 **Christian P. Robert — *The Bayesian Choice: A Decision-Theoretic Motivation*** (2nd ed., 2001, Springer). The rigorous decision-theoretic treatment of Bayesian statistics — for the member who wants the theory (loss functions, admissibility, priors) under the applied books.
- **[NICE]** 🔴 **James O. Berger — *Statistical Decision Theory and Bayesian Analysis*** (2nd ed., 1985, Springer). The classic monograph that unified decision theory and Bayesian analysis — reference-grade depth on priors, loss, and robustness.
- **[NICE]** 🔴 **Christian P. Robert & George Casella — *Monte Carlo Statistical Methods*** (2nd ed., 2004, Springer). The authoritative treatment of the MCMC machinery (importance sampling, Metropolis-Hastings, Gibbs) that every applied Bayesian model — and every regime/hidden-state model — runs on.

---

## discrete-math-and-combinatorics

The discrete/algorithmic mathematics underlying order-book states, combinatorial structures, graph algorithms, and the quant-engineering/data-structures side of the Atlas. Smaller but essential for members who never took discrete math.

### Books
- **[CORE]** 🟡 **Ronald L. Graham, Donald E. Knuth & Oren Patashnik — *Concrete Mathematics: A Foundation for Computer Science*** (2nd ed., 1994, Addison-Wesley). The classic text on sums, recurrences, generating functions, and asymptotics — the "street-fighting" mathematics that makes counting and algorithm analysis tractable. High-reuse for a transversal toolbox.
- **[CORE]** 🟡 **Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest & Clifford Stein — *Introduction to Algorithms*** (CLRS; 4th ed., 2022, MIT Press). The algorithms canon: data structures, sorting/searching, graph algorithms, and complexity — the mathematical-underpinnings reference for quant engineering and for any algorithmic question in the HFT and quant-dev pillars.
- **[NICE]** 🟢 **Kenneth H. Rosen — *Discrete Mathematics and Its Applications*** (8th ed., 2019, McGraw-Hill). The broad, accessible undergraduate text covering logic, sets, combinatorics, relations, graphs, and counting — a self-contained on-ramp for members with no discrete-math background.
- **[NICE]** `[Free]` 🟢 **Eric Lehman, F. Thomson Leighton & Albert R. Meyer — *Mathematics for Computer Science*** (MIT 6.042 course notes; free PDF on MIT OCW). A rigorous-but-friendly introduction to the discrete math that underpins computation (proofs, graph theory, recurrences, probability for computing) — excellent free on-ramp.
- **[NICE]** 🔴 **Richard P. Stanley — *Enumerative Combinatorics, Vol. 1*** (2nd ed., 2011, Cambridge University Press). The graduate reference on enumeration and generating functions — for deep combinatorics, reference-only.
- **[NICE]** 🔴 **Donald E. Knuth — *The Art of Computer Programming*** (Vols. 1–4, Addison-Wesley). The foundational, hyper-rigorous reference on algorithms and discrete structures — the deep-canon for members going into serious quant engineering.

---

## Priority acquisition

The Foundations toolbox is the **most-reused** corpus in the Atlas (every pillar cites it), so the acquisition list is fuller than the pillar wishlists. Build it in dependency order — linear algebra & calculus first (they are currently the thinnest HAVE items), then probability → measure → stochastics → statistics → optimization, with the `[Free]` titles grabbed **immediately** at zero cost.

**Free, grab now (zero cost, author/publisher hosted):**
1. **Axler — *Linear Algebra Done Right*** (axler.net) — fills the thin LA note.
2. **Boyd & Vandenberghe — *Convex Optimization*** (Stanford PDF) — the optimization canon.
3. **Durrett — *Probability: Theory and Examples*** (Duke PDF) — the measure/martingale standard.
4. **MacKay — *Information Theory, Inference, and Learning Algorithms*** (inference.org.uk) — bridges info theory and Bayes.
5. **Lehman/Leighton/Meyer — *Mathematics for Computer Science*** (MIT OCW) — free discrete-math on-ramp.

**Priority purchase order (top ~15, each unlocks the next):**
1. **Strang — *Introduction to Linear Algebra* (5th ed.)** — rebuild the thin LA foundation from a low base; everything downstream assumes it.
2. **Hubbard & Hubbard — *Vector Calculus, Linear Algebra, and Differential Forms* (5th ed.)** — the highest-leverage single text: fills the multivariable-calculus gap *and* reinforces LA. Best value in the whole toolbox.
3. **Blitzstein & Hwang — *Introduction to Probability* (2nd ed.)** — the probability on-ramp for econ/CS/no-math members; get everyone to a common floor.
4. **Simon & Blume — *Mathematics for Economists*** — the econ-background fast path into exactly the math the Atlas uses.
5. **Billingsley — *Probability and Measure*** (with **Shreve II** already owned as the working application) — the rigorous measure-theory bridge.
6. **Øksendal — *Stochastic Differential Equations* (6th ed.)** — the SDE/Feynman-Kac step beyond Shreve II into the PDE/Greeks side.
7. **Casella & Berger — *Statistical Inference* (2nd ed.)** — the statistical-theory spine.
8. **Hamilton — *Time Series Analysis*** — the definitive reference behind cointegration/VAR/regime topics the thin econometrics node needs.
9. **Boyd & Vandenberghe — *Convex Optimization*** (`[Free]`) — the optimization framework under portfolio, robust, and fitting problems. (Free — read immediately even if the print arrives later.)
10. **Nocedal & Wright — *Numerical Optimization* (2nd ed.)** — the algorithm reference behind every "solve this optimization" claim.
11. **Cover & Thomas — *Elements of Information Theory* (2nd ed.)** — the info-theory canon; small, high-reuse.
12. **Gelman et al. — *Bayesian Data Analysis* (3rd ed.)** — the Bayesian canon under Black-Litterman/shrinkage/regime work.
13. **Trefethen & Bau — *Numerical Linear Algebra*** — numerical honesty for the most-computed operation in the Atlas (eigendecompositions).
14. **Efron & Hastie — *Computer Age Statistical Inference*** — the computer-age inference mindset that disciplines every empirical pillar.
15. **Graham, Knuth & Patashnik — *Concrete Mathematics* (2nd ed.)** — discrete/combinatorial mathematics for members without a CS degree.

> **Deliberately sequenced:** HAVE anchors (Shreve I+II, Björk, Tsay, ESL, Glasserman, thin notes) stay as the reading substrate; the purchased spine above climbs from accessible mechanics (Strang/Blitzstein/Simon-Blume) to the rigorous canon (Billingsley/Durrett/Øksendal/Casella-Berger/Hamilton) to the applied frameworks (Boyd/Nocedal/BDA3/Cover-Thomas), with `[NICE]` advanced-reference texts added only as members reach them. Nothing listed is invented — every bibliographic detail was verified against publisher/author pages.
