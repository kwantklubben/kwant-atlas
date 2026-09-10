# Spelling / Typo / Term-Consistency Audit — `content/` prose

**Scope:** all 710 markdown pages under `content/` **excluding `content/_legacy/`**.
Areas covered: `foundations/` (9 topic-folders), `fundamentals-accounting/` (8 folders),
`pillars/01-…-08-…` (8 pillars), plus the top-level `index.md`.
**Method:** programmatic. All pages walked; YAML frontmatter, fenced code blocks
(```` ``` ````/`~~~`), inline code (`` ` ``), and LaTeX math (`$…$`, `$$…$$`, `\[…\]`, `\(…\)`)
were stripped to isolate prose. Prose was then checked against three detectors:
(1) a curated misspelling dictionary, (2) a dictionary-based word-list scan
(`hunspell`/`aspell` unavailable on host → used `/usr/share/dict/cracklib-small` + technical
whitelist), (3) an edit-distance-1/2 nearest-word analysis. A separate pass aggregated every
`Name<dash>Name` compound to find terms rendered with **both** a hyphen and an en-dash.
British-vs-American differences, author names, and LaTeX/code tokens are **not** reported.

---

## 1. Genuine spelling / wrong-word / malformed-token errors

All line numbers are 1-based in the file named. Every item below was read in context and
confirmed to be a real error (not code, not math, not a name).

| File:line | Wrong | Correct | Note |
|---|---|---|---|
| `content/pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/02-the-kelly-formula.md:114` | `Pluggting` | `Plugging` | sentence-initial, malformed from a bulk edit ("Pluggting the even-money …") |
| `content/pillars/04-quantitative-risk/copulas-and-dependence/01-from-zero-intuition.md:128` | `Parameteric` | `Parametric` | misspelling inside a wikilink *display* text ("Parameteric, Historical & Monte Carlo VaR") |
| `content/pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/06-advanced-extensions.md:99` | `intepretability` | `interpretability` | "robustness-vs-intepretability trade" |
| `content/pillars/06-market-making/limit-order-book-mechanics/01-from-zero-intuition.md:19` | `hagging` | `haggling` | "hagging each one is impossible" (parallel to the preceding "they trade … they haggle") |
| `content/pillars/02-algorithmic-hft/colocation-and-clock-synchronization/06-advanced-extensions.md:107` | `raccing` | `racing` | BCS latency-race argument: "too-short recreates raccing" |
| `content/pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading.md:117` | `determinstic` | `deterministic` | "If the closing time is deterministic…" |
| `content/pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/04-evaluating-signal.md:22` | `wildy` | `wildly` | "A 0.05 IC that varies wildy is worthless" |

**Totals:** 7 distinct misspelled/malformed tokens, 7 files.

### Cross-check notes (not errors — recorded so they are not re-flagged)
- `fonctions` / `marges` (`copulas-and-dependence/02-sklars-theorem-and-copulas.md:197`) — the
  French title of Sklar (1959), *Fonctions de répartition à n dimensions et leurs marges* — correct.
- `AMARG`, `ATURN`, `ALEVER`, `AROA`, `ACCR` (`quantitative-fundamental-investing/04-quality-and-fscores.md:70`)
  — ticker-style variable names in a code block — correct.
- All `form the …` occurrences are the verb *form* (form a portfolio, form the logit) — correct.
- No bare `Ito` (all 158 occurrences use `Itô`), no `teh`, `adn`, `recieve`, `seperate`, `occured`,
  `wich`, `thier`, `alot`, `untill`, `definately`, `wierd` etc. anywhere in scope.

---

## 2. Term-consistency inconsistencies

### 2a. Hyphen vs en-dash in multi-name compounds (systemic)

The house style joins multi-author names with an **en-dash** (`Metropolis–Hastings`,
`Radon–Nikodym`, `Glosten–Milgrom`, `Baum–Welch`, `Benjamini–Hochberg`, …). A large minority of
pages instead use a plain **hyphen** for the same terms, and several terms are spelled *both ways*
inside a single page. 96 compounds were found with both forms; the highest-impact ones:

| Term | Hyphen | En-dash | Sample file:line (hyphen form) |
|---|---|---|---|
| `Avellaneda-Stoikov` | 13 | 32 | `content/index.md:84`; `pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index.md` |
| `Black-Scholes` | 31 | 6 | `content/fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity.md:54` |
| `Black-Scholes-Merton` | 73 | 7 | `content/index.md:92` |
| `Fama-French` | 10 | 49 | `content/fundamentals-accounting/index.md`; `…/quantitative-fundamental-investing/index.md` |
| `Ledoit-Wolf` | 8 | 29 | `content/index.md`; `pillars/05-portfolio-optimization/index.md` |
| `Ornstein-Uhlenbeck` | 4 | 4 | `content/index.md`; `pillars/01-quantitative-research/index.md` |
| `Glosten-Milgrom` | 21 | 76 | `content/index.md` |
| `Black-Litterman` | 35 | 47 | `foundations/econometrics-and-timeseries/05-cointegration-and-multivariate.md` |
| `Radon-Nikodym` | 3 | 33 | `foundations/index.md` |
| `Almgren-Chriss` | 53 | 71 | `content/index.md` |
| `Metropolis-Hastings` | 2 | 21 | `foundations/numerical-methods/06-advanced-extensions.md` |
| `Crank-Nicolson` | 13 | 18 | `foundations/numerical-methods/index.md` |
| `Mean-Variance` | 43 | 15 | `foundations/bayesian-statistics/index.md` |
| `Feynman-Kac` | 22 | 20 | `foundations/stochastic-calculus/06-advanced-extensions.md` |
| `Garman-Kohlhagen` | 3 | 4 | `pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas.md` |
| `Engle-Granger` | 6 | 15 | `foundations/index.md` |
| `Dickey-Fuller` | 2 | 8 | `pillars/01-quantitative-research/feature-engineering-and-labeling.md` |
| `Breeden-Litzenberger` | 3 | 14 | `pillars/03-derivative-pricing/interest-rate-and-term-structure/06-advanced-extensions.md` |
| `Ho-Stoll` | 4 | 18 | `pillars/06-market-making/inventory-management-and-quote-skewing/03-ho-stoll-model.md` |
| `Kothari-Warner` | 1 | 43 | `pillars/01-quantitative-research/event-studies/04-statistical-testing.md` |
| `Marchenko-Pastur` | 8 | 21 | `foundations/linear-algebra-and-matrices/06-advanced-extensions.md` |

…and the remaining mixed compounds (both forms present, lower counts):
`Acharya-Pedersen, Amihud-Mendelson, BCBS-IOSCO, Barone-Adesi-Whaley, Barroso-Santa-Clara,
Baum-Welch, Benjamini-Hochberg, Bergomi-Guyon, Beta-Bernoulli, Bias-Variance, Bjerksund-Stensland,
Box-Muller, Brown-Warner, Brunnermeier-Pedersen, Burgard-Kjaer, Carr-Madan,
Cartea-Jaimungal-Penalva, Chambers-Mallows-Stuck, Cont-Kukanov, Cont-Kukanov-Stoikov,
Cont-Stoikov-Talreja, Cornish-Fisher, Cox-Ingersoll-Ross, Cox-Ross-Rubinstein, Daniel-Moskowitz,
Delta-Gamma, Duffie-Garleanu-Pedersen, Eckart-Young, ES-SPY, Euler-Maruyama, Euler-Mascheroni,
Expectation-Maximization, Fisher-Tippett-Gnedenko, Forward-Backward, Gamma-Poisson, Gauss-Jordan,
Glosten-Harris, Granger-Ramanathan, Hamilton-Jacobi-Bellman, Harvey-Liu, Haugh-Kogan, He-Litterman,
Huang-Stoll, Huberman-Stanzl, Hull-White, Lance-Williams, Lee-Ready, Ljung-Box, Longstaff-Schwartz,
Marshall-Olkin, McLean-Pontiff, McNeil-Frey, Moskowitz-Ooi-Pedersen, Myers-Majluf, NJ-London,
NY-Chicago, Nelder-Mead, Newton-Raphson, Normal-Normal, Pastor-Stambaugh, Peaceman-Rachford,
Pickands-Balkema, Pollaczek-Khinchine, Scholes-Williams, TF-IDF, VaR-ES, Variance-Covariance,
Wu-Zhang, Yule-Walker` (plus the geographic pairs `London-Frankfurt/London-NY/Chicago-NY/Chicago-New`).

**Effect:** a reader (and any future search/replace) cannot rely on one canonical spelling; the
renderer shows `Avellaneda–Stoikov` and `Avellaneda-Stoikov` as visibly different strings in the
same pillar.

### 2b. `Monte Carlo` vs `Monte-Carlo`

- `Monte Carlo` (space): **308** occurrences across 122 files.
- `Monte-Carlo` (hyphen): **70** occurrences across 40 files, frequently in attributive position
  where the corpus elsewhere uses the space form — e.g. "Monte-Carlo mean" / "Monte-Carlo fill
  simulation" vs "Monte Carlo mean" / "Monte Carlo LSM".
- Sample: `pillars/02-algorithmic-hft/execution-backtesting-and-simulation/04-market-replay-vs-monte-carlo.md:113`
  ("Monte-Carlo mean") alongside the same file's space-form usage.
- (No en-dash form exists.)

### 2c. Terms checked and found **consistent** (no action)
- `Itô` — 158/158 accented; `Itô-Doeblin` 3/3; **zero** bare `Ito` or `Ito-Doeblin`.
- `Merton`, `Heston`, `SABR`, `GARCH` — single canonical form each.

---

## 3. Doubled words / malformed sentences

| File:line | Render | Should read | Note |
|---|---|---|---|
| `content/fundamentals-accounting/data-sources-and-corporate-data/index.md:43` | `never treat as as-first-published` | `never treat as first-published` (or `…as "as-published"`) | doubled **as** |
| `content/fundamentals-accounting/fundamental-analysis-and-screening/01-from-zero-intuition.md:82` | `This is the value-trap trap` | `This is the value trap` / `the value-trap` | doubled **trap** |
| `content/fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability.md:17` | `the reverse is the value-trap trap` | `…the value trap` | doubled **trap** |

No genuinely broken / garbled *sentences* were found: all 710 pages parse as coherent prose.
The `… and <math> and …`, `… vs <math> vs …`, `… of <math> of …` sequences that a naive
doubled-word regex flags are all legitimate — the repeated word is separated by an intervening
LaTeX expression (stripped before analysis). `IS is`, `no no-trade region`, `16,384-row row
groups`, and `it, it would have…` are likewise correct in context, not doublings.

---

## 4. Verdict + counts

- **Genuine errors (Section 1): 7** misspelled/malformed tokens in **7** files.
- **Doubled-word / broken-text errors (Section 3): 3** occurrences in **3** files.
- **Total genuine prose errors: 10**, across **10 distinct files**.
- **Term-consistency issues (Section 2): 96** multi-name compounds rendered with *both* hyphen and
  en-dash, plus the `Monte Carlo` / `Monte-Carlo` split (308 vs 70). These are *consistency*, not
  comprehension, failures, but they are the dominant finding by volume.

**Overall verdict: the prose is in very good spelling shape.** There is no class of systematic
misspelling and no comprehension-breaking garbling; the handful of genuine typos
(`Pluggting`, `Parameteric`, `intepretability`, `hagging`, `raccing`, `determinstic`, `wildy`) are
isolated and easily fixed. The real cleanup work is **normalising the hyphen-vs-en-dash treatment
of author-name compounds** — especially `Avellaneda-Stoikov`, `Black-Scholes(-Merton)`,
`Fama-French`, `Ledoit-Wolf`, `Ornstein-Uhlenbeck`, `Glosten-Milgrom`, `Black-Litterman`, and
`Monte Carlo` — to the en-dash house style already used by the majority of occurrences.
