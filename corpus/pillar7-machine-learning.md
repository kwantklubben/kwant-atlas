---
title: "Corpus Wishlist — Pillar 7: Machine Learning & Alternative Data"
pillar: 07-machine-learning-altdata
tags:
  - corpus
  - pillar-ml-altdata
---

# Corpus Wishlist — Pillar 7: Machine Learning & Alternative Data

This is the acquisition wishlist for the **Machine Learning & Alternative Data** pillar. It tracks the books, canonical papers, and (a few) courses we intend to add to the corpus, grouped by the pillar's sub-topics. Every entry has been verified to exist (title / author / venue / year). Markers are described in the legend below.

## Notes on scope and overlap

- **Members range from zero to near-professional in ML.** The beginner must learn machine learning itself from scratch *before* any of the financial ML material below makes sense. General ML/DL foundations (intro-to-ML texts, linear algebra, and the estimator fundamentals of the Atlas Foundations pillar) are **assumed as prerequisites and are deliberately NOT the focus of this wishlist** — they belong to the Foundations corpus, not Pillar 7. We list only the two or three foundational texts a beginner will reach for as stepping stones, flagged `[FOUND]`.
- **[HAVE]** entries below are already in the collection and are listed for routing/context only — do **not** re-acquire them.
- The **financial-ML-specific** literature is anchored on a single de facto canon: **Marcos López de Prado**'s two Wiley/Cambridge books. They are marked `[SOURCE]` and should be acquired first; nearly every sub-topic folder below routes back to chapters in them.
- Academic peer-reviewed papers (RFS, JF, JPM, Econometrica, etc.) are the durable half of the corpus; survey/tutorial items and open platforms are included where they carry real pedagogical weight.

## Legend

- `[HAVE]` — already owned in the corpus; listed for reference/routing, do not re-purchase.
- `[SOURCE]` — a central, must-own anchor for Pillar 7; acquire in the first wave.
- `[FOUND]` — foundational ML/prereq text that lives in the Foundations corpus; flagged for the beginner.
- `[CORE]` — strongly recommended: canonical paper/book that directly serves a sub-topic.
- `[NICE]` — worthwhile depth/supplement, lower priority.

---

## Cornerstone of the whole pillar (read first)

- **[SOURCE] *Advances in Financial Machine Learning*** — Marcos López de Prado, Wiley, 2018, ISBN 978-1-119-48208-6. THE hub of Pillar 7: fractional differentiation (Ch. 5), triple-barrier labeling (Ch. 3), purged & embargoed and combinatorial cross-validation (Ch. 7), meta-labeling and bet sizing (Ch. 3 & 10), feature importance (Ch. 8), ensemble methods, backtest overfitting & the deflated Sharpe ratio (Ch. 11), and ML for portfolio construction (Ch. 15–17). Feeds *almost every* sub-topic folder below; treat as the spine of the pillar.
- **[SOURCE] *Machine Learning for Asset Managers*** — Marcos López de Prado, Cambridge Elements in Quantitative Finance, 2020, ISBN 978-1-108-79089-3. The short, math-light companion covering meta-labeling, fractional differentiation, hyperparameter tuning under CPCV, and — centrally — covariance matrix denoising/detoning, Marcenko–Pastur shrinkage, and clustering for portfolio construction. Primary anchor for the `feature-engineering-and-meta-labeling` and `ml-for-portfolio` folders.
- **[NICE] *Advances in Financial Machine Learning*, 10-part lecture series** — López de Prado, 2018, on SSRN (10 freely posted lectures, incl. "The 7 Reasons Most Machine Learning Funds Fail"). Free video/notes companion to the flagship book; an inexpensive way to preview the material before buying.

---

## financial-ml-pitfalls-and-low-snr

Why standard ML fails in finance: microscopic SNR, non-stationarity, active adaptation by the market, and subtle leakage.

**Books**
- **[HAVE] *The Elements of Statistical Learning*** — Hastie, Tibshirani & Friedman, Springer, 2nd ed., 2009 (18 ch.). General ML theory foundation; the FOUNDATIONS corpus entry this pillar builds on.
- **[HAVE] *Analysis of Financial Time Series*** — Ruey S. Tsay, Wiley, 3rd ed., 2010. Regime/GARCH/time-series econometrics baseline (cross-listed from Foundations) that ML regime methods extend.

**Papers**
- **[CORE] "Empirical Asset Pricing via Machine Learning"** — Shihao Gu, Bryan Kelly & Dacheng Xiu, *Review of Financial Studies* 33(5):2223–2273, 2020. The rigorous benchmark that quantifies the true (low) out-of-sample IC/SNR achievable on daily cross-sections and shows trees + shallow NNs dominate linear models — but only under disciplined OOS evaluation. Antidote to inflated claims.
- **[CORE] "Can Machines 'Learn' Finance?"** — Ronen Israel, Bryan Kelly & Tobias Moskowitz, *Journal of Investment Management*, 2020. A sober industry/academic verdict on where ML genuinely helps vs. overfits in asset management.
- **[NICE] "How to Avoid Machine Learning Pitfalls: A Guide for Academic Researchers"** — arXiv:2108.02497, 2021. General but excellent, finance-relevant catalog of leakage, feature-selection-before-split, and sequential-overfitting traps.
- **[NICE] "The Myth and Reality of Financial Machine Learning"** — López de Prado, SSRN 3120557, 2018. Short position paper on what financial ML can and cannot do; good framing for the beginner.

---

## purged-cross-validation-and-backtest-hygiene

Purged/embargoed k-fold & combinatorial purged CV; honest walk-forward testing; deflated performance metrics.

**Books**
- **[SOURCE] *Advances in Financial Machine Learning*** (Ch. 7 "Cross-Validation in Finance," Ch. 11 "Backtest Statistics") — see Cornerstone. Primary treatment of purging, embargoing, CPCV, and backtest-overfitting statistics.

**Papers**
- **[CORE] "The Probability of Backtest Overfitting"** — Bailey, Borwein, López de Prado & Zhu, *Journal of Computational Finance* 20(4):39–70, 2017. Introduces Combinatorially Symmetric Cross-Validation (CSCV) and the PBO measure; the formal machinery behind "your backtest is probably overfit."
- **[CORE] "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality"** — David H. Bailey & Marcos López de Prado, *Journal of Portfolio Management* 40(5):94–107, 2014. Corrects reported Sharpe ratios for the number of trials tried; the standard metric for judging whether a backtest result is real.
- **[CORE] "Backtest Overfitting in the Machine Learning Era: A Comparison of Out-of-Sample Testing Methods"** — *Expert Systems with Applications*, 2025 (arXiv-linked). Recent controlled comparison of walk-forward vs. purged vs. adaptive CPCV on synthetic noisy/non-stationary data; good modern summary for the pipeline sub-topic.
- **[NICE] "Detection of False Investment Strategies Using Unsupervised Learning Methods"** — López de Prado & Michael J. Lewis, *Quantitative Finance* 19(9), 2019. Uses clustering of strategy returns to expose clusters of indistinguishable (false) strategies — bridges backtest hygiene and the `ml-for-portfolio` clustering tools.

---

## tree-and-boosting-methods

Gradient boosting (LightGBM/XGBoost/CatBoost) and random forests as the workhorse of tabular quant ML; feature ranking.

**Books**
- **[SOURCE] *Advances in Financial Machine Learning*** (Ch. 7–8: purged CV applied to trees, MDA/MDI feature importance) — see Cornerstone.

**Papers**
- **[CORE] "Empirical Asset Pricing via Machine Learning"** — Gu, Kelly & Xiu, RFS 2020 (see Pitfalls). Documented empirical winner for *why* boosted trees and RFs are the industry default on tabular factor data.
- **[CORE] "XGBoost: A Scalable Tree Boosting System"** — Tianqi Chen & Carlos Guestrin, *KDD*, 2016. Original system paper for XGBoost; the reference for the algorithm most quants start with.
- **[CORE] "LightGBM: A Highly Efficient Gradient Boosting Decision Tree"** — Guolin Ke et al., *NeurIPS*, 2017. Microsoft's Leaf-wise GBDT; the current default in quant research pipelines (used in Qlib, see below).
- **[NICE] "CatBoost: Unbiased Boosting with Categorical Features"** — Liudmila Prokhorenkova et al., *NeurIPS*, 2018. Ordered-boosting variant that handles categorical leakage; worth one slot alongside LightGBM/XGBoost.
- **[NICE] *Understanding Random Forests: From Theory to Practice*** — Gilles Louppe, PhD thesis (arXiv:1407.7502), 2014. The cleanest formal treatment of RF feature-importance and bias; depth on how trees overfit/robustify.

---

## feature-engineering-and-meta-labeling

Triple-barrier labeling, fractional differentiation, meta-labeling, bet sizing, and microstructure/feature synthesis.

**Books**
- **[SOURCE] *Machine Learning for Asset Managers*** (Ch. 2–4: meta-labeling, fractional differentiation, sizing; Ch. 7 hyperparameter tuning under CPCV) — see Cornerstone.
- **[SOURCE] *Advances in Financial Machine Learning*** (Ch. 3–5: triple-barrier & meta-labels, sample weights, fractional differentiation) — see Cornerstone.

**Papers**
- **[CORE] "Meta-Labeling: Theory and Framework"** — Marcos López de Prado, SSRN 3197166, 2018. The note that defines secondary ML models for bet sizing/filtering on top of a primary signal; central to the folder.
- **[CORE] "Microstructure Features" survey within *Advances*** — López de Prado, Ch. 17 *Machine Learning for Asset Managers* context. Because it lives inside a SOURCE book, treat the two de Prado books as the canonical feature-engineering references rather than re-listing them.

---

## financial-nlp-and-transcripts

FinBERT and financial language models; 10-K/earnings-transcript NLP; dictionary vs. deep learning sentiment.

**Books**
- **[FOUND] *Speech and Language Processing*** — Dan Jurafsky & James H. Martin, 3rd ed. (draft online), Pearson. Standard NLP fundamentals the financial-NLP reader assumes; lives in the general NLP/FOUNDATIONS track.

**Papers**
- **[SOURCE] "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models"** — Dogu Araci, arXiv:1908.10063, 2019. The FinBERT model behind the widely used `ProsusAI/finbert` weights; the canonical financial-domain BERT adaptation this pillar builds on.
- **[CORE] "FinBERT: A Pretrained Language Model for Financial Communications"** — Yi Yang, Mark Christopher Siy Uy & Allen Huang, arXiv:2006.08097, 2020. The second, larger FinBERT variant trained on financial communications corpora; complements Araci's sentiment model for 10-K/transcript tasks.
- **[CORE] "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks"** — Tim Loughran & Bill McDonald, *Journal of Finance* 66(1):35–65, 2011. Foundation of finance-specific sentiment *dictionaries* (the LM lists) — the essential baseline that motivates going beyond generic NLP lexicons.
- **[CORE] "Giving Content to Investor Sentiment: The Role of Media in the Stock Market"** — Paul C. Tetlock, *Journal of Finance* 62(3):1139–1168, 2007. The classic media-content/returns study that seeded quantitative textual analysis in markets.

---

## alternative-data-pipelines

Point-in-time hygiene, alpha decay, and pipelines for credit-card, geolocation, satellite, web-scraped and transcript data.

**Books**
- **[CORE] *Big Data and Machine Learning in Quantitative Investment*** — Tony Guida, Wiley, 2019. The most complete practitioner book on building alternative-data and ML quant workflows end-to-end (data sourcing, cleaning, modeling, backtesting).

**Reports / Papers**
- **[CORE] "Casting the Net: How Hedge Funds Are Using Alternative Data"** — AIMA / SS&C Technologies, 2017 (industry survey, ~$720bn AUM respondents). The standard industry survey documenting which alt-data types funds actually use, and the practical challenges; ideal orientation reading.
- **[NICE] *Satellite / geolocation alt-data* vendor methodology briefs** — free, current vendor-level material on point-in-time construction and alpha decay (Eagle Alpha, YipitData public guides). Useful as living practice references rather than static books; treat as optional browsing, not corpus-grade acquisition.
- **[NICE] Qlib alt-data & pipeline case studies** — Microsoft Qlib examples (see *Platforms & Tools* below) ship point-in-time-aware factor workflows the member can run end-to-end as a first alt-data pipeline.

---

## regime-classification-hmm-gmm

Hidden Markov / Gaussian-mixture regime detection: Baum–Welch EM, Viterbi decoding, and regime-aware allocation.

**Books**
- **[HAVE] *Analysis of Financial Time Series*** — Tsay, Wiley, 3rd ed., 2010. Regime-switching and Markov-chain time-series coverage already in the corpus (Foundations cross-list); the econometric grounding for HMM regime models.

**Papers**
- **[CORE] "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle"** — James D. Hamilton, *Econometrica* 57(2):357–384, 1989. The foundational Markov regime-switching paper every finance HMM/GMM treatment descends from.
- **[CORE] "Regime Changes and Financial Markets"** — Andrew Ang & Allan Timmermann, *Annual Review of Financial Economics* 4:313–337, 2012. The canonical survey linking estimated regimes to fat tails, heteroskedasticity, skewness, and portfolio choice; bridges stats to allocation.
- **[CORE] "Regime Shifts: Implications for Dynamic Strategies"** — Kritzman, Page & Turkington, *Financial Analysts Journal* 68(3), 2012. Practitioner paper applying regime detection to dynamic asset-allocation (Markov-switching on macro data); the concrete use-case for the pillar's HMM/GMM folder.
- **[NICE] "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition"** — Lawrence R. Rabiner, *Proceedings of the IEEE* 77(2):257–286, 1989. The canonical algorithm-level HMM tutorial (Baum–Welch, Viterbi, forward–backward) for members who need the mechanics behind finance applications.

---

## deep-learning-for-sequences

LSTM/GRU, temporal convolutional networks, and transformers (TFT) for tick/bar and macro series; distributional forecasts.

**Books**
- **[FOUND] *Deep Learning*** — Ian Goodfellow, Yoshua Bengio & Aaron Courville, MIT Press, 2016. Standard deep-learning text the sequential-DL reader assumes; Foundations/FOUNDATIONS-track prereq rather than Pillar-7-specific.

**Papers**
- **[CORE] "Long Short-Term Memory"** — Sepp Hochreiter & Jürgen Schmidhuber, *Neural Computation* 9(8):1735–1780, 1997. The original LSTM; required context for why sequence models entered trading.
- **[CORE] "An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling"** — Shaojie Bai, J. Zico Kolter & Vladlen Koltun, arXiv:1803.01271, 2018. Defines Temporal Convolutional Networks (TCNs), the pillar's preferred cheap-alternative-to-RNN sequence model.
- **[CORE] "Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting"** — Bryan Lim, Sercan Ö. Arık, Nicolas Loeff & Tomas Pfister, *International Journal of Forecasting* 37(4), 2021 (arXiv:1912.09363). The attention-based, interpretable multi-horizon architecture the pillar's TFT ambition points to.
- **[NICE] "DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks"** — David Salinas et al., *International Journal of Forecasting*, 2020 (arXiv:1704.04110). Standard probabilistic/LSTM forecast model producing full predictive distributions (useful for regime-aware uncertainty).
- **[NICE] "Attention Is All You Need"** — Vaswani et al., *NeurIPS*, 2017. The Transformer paper; general DL prereq referenced by the TFT work — include only if not already in the FOUNDATIONS deep-learning track.

---

## reinforcement-learning-for-trading

RL formalisms (MDP, Q-learning, policy gradients, PPO) applied to portfolio/trading decisions; RL's real pitfalls in finance.

**Books**
- **[FOUND] *Reinforcement Learning: An Introduction*** — Richard S. Sutton & Andrew G. Barto, 2nd ed., MIT Press, 2018. The RL canonical text; a general-ML prereq that the trading-RL folder builds on (FOUNDATIONS-track unless the member already owns it).

**Papers**
- **[CORE] "Deep Direct Reinforcement Learning for Financial Signal Representation and Trading"** — Yue Deng, Feng Bao, Youyong Kong, Zhiquan Ren & Qionghai Dai, *IEEE Transactions on Neural Networks and Learning Systems*, 2017 (arXiv:1803.11155). One of the most-cited concrete RL-for-trading systems; a realistic (non-overhyped) implementation template.
- **[CORE] "Human-level Control through Deep Reinforcement Learning"** — Volodymyr Mnih et al., *Nature* 518:529–533, 2015. The DQN paper; required algorithmic context for deep Q-learning approaches common in trading RL.
- **[CORE] "Proximal Policy Optimization Algorithms"** — John Schulman et al., arXiv:1707.06347, 2017. PPO — the stable policy-gradient method most finance RL frameworks (incl. Qlib's RL) use; needed to read modern trading-RL code.
- **[NICE] "The Evolution of Reinforcement Learning in Quantitative Finance" survey** — *ACM Computing Surveys* / arXiv survey, 2024. Broad 100+ paper survey of RL in quant finance; useful as an orientation/index even if too broad for focused study. (Verify the specific arXiv/venue before acquisition.)

---

## ml-for-portfolio

ML for covariance estimation & shrinkage, Marcenko–Pastur denoising, clustering, and hierarchical/diversified portfolio construction.

**Books**
- **[SOURCE] *Machine Learning for Asset Managers*** (Ch. 5–6: covariance estimation, denoising/detoning, Marcenko–Pastur; Ch. 8: clustering) — see Cornerstone. The primary anchor for this folder.

**Papers**
- **[CORE] "Building Diversified Portfolios That Outperform Out of Sample"** — Marcos López de Prado, *Journal of Portfolio Management* 42(4):59–69, 2016. Introduces Hierarchical Risk Parity (HRP) via graph clustering; the canonical ML-for-portfolio paper of the pillar.
- **[CORE] "A Robust Estimator of the Efficient Frontier"** — Marcos López de Prado, SSRN 3469961, 2019. Compares MCD/SK/NaN/TS/DNN covariance estimators against the naive 1/N benchmark; practical recipe for robust covariance in mean-variance optimization.
- **[NICE] "Marchenko–Pastur theorem" primer within *ML for Asset Managers*** — lives in the SOURCE book; listed here only to note that random-matrix-theory denoising is the mechanism the folder's covariance estimators rely on.

---

## Platforms & Tools (optional running practice)

Hands-on platforms are not "corpus" in the book sense, but Qlib in particular doubles as a reference implementation of the pillar's pipeline (LightGBM defaults, purged-style evaluation, RL module, feature processors).

- **[CORE] Microsoft Qlib** — open-source AI-oriented quant platform (github.com/microsoft/qlib); paper "Qlib: An AI-oriented Quantitative Investment Platform," arXiv:2009.11189, 2020. Ships point-in-time factor datasets, Alpha158/Alpha360 feature sets, LightGBM/XGBoost/CatBoost and LSTM/GRU/Transformer/TFT backends, and an RL module — the closest thing to a runnable embodiment of Pillar 7's stack.

---

## Priority acquisition (top ~12)

Buy in roughly this order. Waves: **W1** = unlock the whole pillar; **W2** = depth per sub-topic; **W3** = breadth/free items.

| # | Item | Why / wave |
|---|------|-----------|
| 1 | *Advances in Financial Machine Learning* — López de Prado (2018) | **[SOURCE]** Spine of Pillar 7; spans ~8 of 10 sub-topics. **W1** |
| 2 | *Machine Learning for Asset Managers* — López de Prado (2020) | **[SOURCE]** Companion: meta-labeling, covariance/denoising, clustering. **W1** |
| 3 | "Empirical Asset Pricing via Machine Learning" — Gu, Kelly & Xiu, RFS 2020 | **[CORE]** Rigorous SNR/IC baseline + why trees/NNs win. **W1** (free PDF) |
| 4 | "The Probability of Backtest Overfitting" — Bailey et al. (2017) | **[CORE]** Formalizes CSCV/PBO backtest hygiene. **W1** (free) |
| 5 | "The Deflated Sharpe Ratio" — Bailey & López de Prado (2014) | **[CORE]** Standard honest-performance metric. **W1** (free) |
| 6 | *Big Data and Machine Learning in Quantitative Investment* — Guida (2019) | **[CORE]** Alt-data pipeline anchor. **W2** |
| 7 | "FinBERT: Financial Sentiment Analysis…" — Araci (2019) | **[SOURCE]** Financial-NLP anchor (ProsusAI weights). **W2** (free) |
| 8 | "Temporal Fusion Transformers…" — Lim et al. (2021) | **[CORE]** Sequence/attention target architecture. **W2** (free) |
| 9 | "Regime Changes and Financial Markets" — Ang & Timmermann (2012) | **[CORE]** Regime survey; bridges to allocation. **W2** (free) |
| 10 | "Building Diversified Portfolios That Outperform Out of Sample" — de Prado (2016) | **[CORE]** HRP; ML-for-portfolio anchor. **W2** (free) |
| 11 | XGBoost (Chen & Guestrin, KDD 2016) + LightGBM (Ke et al., NeurIPS 2017) papers | **[CORE]** Boosting canon. **W2** (free) |
| 12 | *Reinforcement Learning: An Introduction* — Sutton & Barto, 2nd ed. | **[FOUND]** RL prereq if not already in FOUNDATIONS. **W2/W3** |

All peer-reviewed journal articles above (RFS, JPM, JCF, QF, IJF, Econometrica) and the arXiv/SSRN papers are freely downloadable, so the marginal cost of the hard-copy backlog is concentrated in items **1, 2, 6** and any Foundations-tier ML textbooks still missing.
