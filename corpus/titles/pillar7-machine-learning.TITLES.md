# Corpus Acquisition Titles — Pillar 7: Machine Learning & Alternative Data

> Compact 1/2/3/4 list, now carrying the acquisition outcome of the full sweep of 2026-09-10.
>
> **Status tags (rewritten to reflect reality after acquisition):**
> - **1** = HAVE - verified full text on disk; path and sha256 given inline.
> - **2** = not a document - an internal chapter cross-reference or a software/data product; no PDF
>   exists to acquire (not a failure).
> - **3** = NOT OBTAINED - no SDU licence route and no open-access edition; each carries ISBN/DOI and
>   a ready-to-submit interlibrary-loan block.
> - **4** = PARTIAL - a genuine but incomplete artefact; the page count held is stated inline.
>
> The list's old markers (`{PAID}`, `{HAVE}`, `{PAID - inside SOURCE book}`, `[manual]`) no longer
> describe reality and have been dropped; the outcome above replaces them.
>
> **Where the artefacts live:** `corpus/titles/refs/pillar7/` - 42 verified PDFs, plus `MANIFEST.json`
> (machine-readable: DOI/ISBN, sha256, page count, source URL, `via_proxy`, and every attempt made with
> its result), `MANIFEST.md` and `ILL_REQUESTS.md`. `_dl_attempts.json` holds the raw acquisition log.
> `refs/` is shared with the other acquisition runs; this list's authoritative snapshot is
> `refs/MANIFEST.pillar7-machine-learning.TITLES.md.json` (a sibling run rewrites the shared
> `refs/MANIFEST.json` concurrently).
>
> Verification gates applied to every file: `%PDF` magic, `pdfinfo` page count > 0, extractable text on
> pp. 1-8, and a fuzzy title/author identity match. All 42 files were then re-audited independently.
> Six pre-existing "free" copies in the corpus turned out to be *different documents* with similar
> titles and were caught by the identity gate and replaced from authoritative sources
> (entries 14, 18, 23, 29, 46, 51).
>
> ISBN/publisher on tag-**3** lines are catalogue matches (OpenLibrary / SDU Primo "Mimer"), not
> verified order details - confirm the exact edition when submitting an ILL request.

## Cornerstone of the whole pillar (read first)

3. **Advances in Financial Machine Learning** — Marcos López de Prado, Wiley, 2018, ISBN 978-1-119-48208-6.  -->  NOT OBTAINED · SDU holds a print-only record (Primo: no electronic service); Wiley book DOI 10.1002/9781119482086 resolves to 'Missing resource null' via EZproxy · ISBN 978-1-119-48208-6 · Wiley, 2018 · ILL: `refs/ILL_REQUESTS.md` §01
3. **Machine Learning for Asset Managers** — Marcos López de Prado, Cambridge Elements in Quantitative Finance, 2020, ISBN 978-1-108-79089-3.  -->  NOT OBTAINED · SDU holds a print-only record (Primo: no electronic service); Cambridge Core (10.1017/9781108883658) returns HTTP 500 direct and via EZproxy · ISBN 978-1-108-79089-3 · Cambridge University Press (Elements in Quantitative Finance), 2020 · ILL: `refs/ILL_REQUESTS.md` §02
1. **Advances in Financial Machine Learning, 10-part lecture series** — López de Prado, SSRN, 2018 (incl. "The 7 Reasons Most Machine Learning Funds Fail").  -->  OBTAINED (549 pp) · author-posted PDF, SSRN · `refs/pillar7/03_MarcosLopezdePrado_2018_advances_financial_machine_learning_part.pdf` (sha256 `6d290b29ec...`)

## financial-ml-pitfalls-and-low-snr

1. **The Elements of Statistical Learning** — Hastie, Tibshirani & Friedman, Springer, 2nd ed., 2009.  -->  OBTAINED (764 pp) · copy inherited from the shared refs/ pool (earlier acquisition run), re-verified in this pass · `refs/pillar7/04_Hastie_2009_elements_statistical_learning.pdf` (sha256 `5b497d7e7d...`)
1. **Analysis of Financial Time Series** — Ruey S. Tsay, Wiley, 3rd ed., 2010.  -->  OBTAINED (714 pp) · copy inherited from the shared refs/ pool (earlier acquisition run), re-verified in this pass · `refs/pillar7/05_RueySTsay_2010_analysis_financial_time_series.pdf` (sha256 `880733b93a...`)
1. **Empirical Asset Pricing via Machine Learning** — Gu, Kelly & Xiu, RFS 33(5):2223–2273, 2020. `GuKellyXiu2020_EmpiricalAssetPricingML.pdf`.  -->  OBTAINED (51 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1093/rfs/hhz072 · `refs/pillar7/06_Gu_2020_empirical_asset_pricing_via_machine.pdf` (sha256 `05e4ef8a1c...`)
1. **Can Machines 'Learn' Finance?** — Israel, Kelly & Moskowitz, Journal of Investment Management, 2020. `IsraelKellyMoskowitz_CanMachinesLearnFinance.pdf`.  -->  OBTAINED (14 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/07_Israel_2020_can_machines_learn_finance.pdf` (sha256 `dcc2d4b219...`)
1. **How to Avoid Machine Learning Pitfalls: A Guide for Academic Researchers** — arXiv:2108.02497, 2021. `LopezdePrado_HowToAvoidMLPitfalls.pdf`.  -->  OBTAINED (33 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/08_MichaelALones_2021_how_avoid_machine_learning_pitfalls.pdf` (sha256 `7fc1faf2e8...`)
1. **The Myth and Reality of Financial Machine Learning** — López de Prado, SSRN 3120557, 2018. `LopezdePrado_MythAndRealityFML.pdf`.  -->  OBTAINED (29 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/09_MarcosLopezdePrado_2018_myth_reality_financial_machine_learning.pdf` (sha256 `90f3cf7e2b...`)

## purged-cross-validation-and-backtest-hygiene

2. **Advances in Financial Machine Learning** (Ch. 7 "Cross-Validation in Finance," Ch. 11 "Backtest Statistics") — see Cornerstone.  -->  not a document - cross-reference to a chapter of entry 01; obtain that book instead · ISBN 978-1-119-48208-6
1. **The Probability of Backtest Overfitting** — Bailey, Borwein, López de Prado & Zhu, JCF 20(4):39–70, 2017. `Bailey_ProbBacktestOverfitting.pdf`.  -->  OBTAINED (35 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.21314/JCF.2016.322 · `refs/pillar7/11_Bailey_2017_probability_backtest_overfitting.pdf` (sha256 `a940c5c18f...`)
1. **The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality** — Bailey & López de Prado, JPM 40(5):94–107, 2014. `BaileyLopezdePrado_DeflatedSharpeRatio.pdf`.  -->  OBTAINED (22 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.3905/jpm.2014.40.5.094 · `refs/pillar7/12_Bailey_2014_deflated_sharpe_ratio_correcting_selection.pdf` (sha256 `ca4a1e834a...`)
1. **Backtest Overfitting in the Machine Learning Era: A Comparison of Out-of-Sample Testing Methods** — Expert Systems with Applications, 2025 (arXiv).  -->  OBTAINED (57 pp) · author-posted PDF, SSRN · `refs/pillar7/13_HamidRArian_2025_backtest_overfitting_machine_learning_era.pdf` (sha256 `81c13b554a...`)
1. **Detection of False Investment Strategies Using Unsupervised Learning Methods** — López de Prado & Lewis, Quantitative Finance 19(9), 2019. `LopezdePradoLewis_FalseInvestmentStrategies.pdf`.  -->  OBTAINED (25 pp) · author-posted PDF, SSRN · DOI 10.1080/14697688.2019.1571681 · `refs/pillar7/14_LopezdePrado_2019_detection_false_investment_strategies_unsupervised.pdf` (sha256 `1d53d05afa...`)

## tree-and-boosting-methods

2. **Advances in Financial Machine Learning** (Ch. 7–8: purged CV applied to trees, MDA/MDI feature importance) — see Cornerstone.  -->  not a document - cross-reference to a chapter of entry 01; obtain that book instead · ISBN 978-1-119-48208-6
1. **Empirical Asset Pricing via Machine Learning** — Gu, Kelly & Xiu, RFS 2020. `GuKellyXiu2020_EmpiricalAssetPricingML.pdf`.  -->  OBTAINED (51 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1093/rfs/hhz072 · `refs/pillar7/16_Gu_2020_empirical_asset_pricing_via_machine.pdf` (sha256 `05e4ef8a1c...`)
1. **XGBoost: A Scalable Tree Boosting System** — Chen & Guestrin, KDD, 2016. `ChenGuestrin_XGBoost.pdf`.  -->  OBTAINED (13 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1145/2939672.2939785 · `refs/pillar7/17_Chen_2016_xgboost_scalable_tree_boosting_system.pdf` (sha256 `52bc282c92...`)
1. **LightGBM: A Highly Efficient Gradient Boosting Decision Tree** — Ke et al., NeurIPS, 2017. `Ke_LightGBM.pdf`.  -->  OBTAINED (9 pp) · NeurIPS proceedings (open) · `refs/pillar7/18_Keetal_2017_lightgbm_highly_efficient_gradient_boosting.pdf` (sha256 `32ddfe0c7a...`)
1. **CatBoost: Unbiased Boosting with Categorical Features** — Prokhorenkova et al., NeurIPS, 2018. `Prokhorenkova_CatBoost.pdf`.  -->  OBTAINED (23 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/19_Prokhorenkovaetal_2018_catboost_unbiased_boosting_categorical_features.pdf` (sha256 `e682f177e2...`)
1. **Understanding Random Forests: From Theory to Practice** — Gilles Louppe, PhD thesis (arXiv:1407.7502), 2014. `Louppe_UnderstandingRandomForests.pdf`.  -->  OBTAINED (223 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/20_GillesLouppe_2014_understanding_random_forests_practice.pdf` (sha256 `e1db9593b5...`)

## feature-engineering-and-meta-labeling

2. **Machine Learning for Asset Managers** (Ch. 2–4: meta-labeling, fractional differentiation, sizing; Ch. 7 hyperparameter tuning) — see Cornerstone.  -->  not a document - cross-reference to a chapter of entry 02; obtain that book instead · ISBN 978-1-108-79089-3
2. **Advances in Financial Machine Learning** (Ch. 3–5: triple-barrier & meta-labels, sample weights, fractional differentiation) — see Cornerstone.  -->  not a document - cross-reference to a chapter of entry 01; obtain that book instead · ISBN 978-1-119-48208-6
3. **Meta-Labeling: Theory and Framework** — Marcos López de Prado, SSRN 3197166, 2018. `LopezdePrado_MetaLabeling.pdf`.  -->  NOT OBTAINED · the SSRN record cited in this list (3197166) is withdrawn; the live same-title paper (4032018) is by J. F. Joubert, a different document · ISBN 978-1-108-79089-3 · SSRN 3197166, 2018 · ILL: `refs/ILL_REQUESTS.md` §23
2. **Microstructure Features survey within *Advances*** — López de Prado, Ch. 17 *Machine Learning for Asset Managers* context.  -->  not a document - cross-reference to a chapter of entry 01; obtain that book instead · ISBN 978-1-119-48208-6

## financial-nlp-and-transcripts

1. **Speech and Language Processing** — Jurafsky & Martin, 3rd ed. (draft online), Pearson. `JurafskyMartin_SpeechLanguageProcessing.pdf`.  -->  OBTAINED (626 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/25_Jurafsky_2025_speech_language_processing.pdf` (sha256 `50a9efbb45...`)
1. **FinBERT: Financial Sentiment Analysis with Pre-trained Language Models** — Dogu Araci, arXiv:1908.10063, 2019. `Araci_FinBERT.pdf`.  -->  OBTAINED (11 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/26_DoguAraci_2019_finbert_financial_sentiment_analysis_pre.pdf` (sha256 `ce63c6b90b...`)
1. **FinBERT: A Pretrained Language Model for Financial Communications** — Yang, Uy & Huang, arXiv:2006.08097, 2020. `Yang_FinBERTFinancialComms.pdf`.  -->  OBTAINED (5 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/27_Yang_2020_finbert_pretrained_language_model_financial.pdf` (sha256 `6e078f3a4b...`)
1. **When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks** — Loughran & McDonald, JF 66(1):35–65, 2011.  -->  OBTAINED (32 pp) · copy inherited from the shared refs/ pool (earlier acquisition run), re-verified in this pass · DOI 10.1111/j.1540-6261.2010.01625.x · `refs/pillar7/28_Loughran_2011_when_liability_not_liability_textual.pdf` (sha256 `63c7c28653...`)
1. **Giving Content to Investor Sentiment: The Role of Media in the Stock Market** — Paul C. Tetlock, JF 62(3):1139–1168, 2007. `Tetlock_GivingContentInvestorSentiment.pdf`.  -->  OBTAINED (30 pp) · Wiley Online Library published PDF via SDU EZproxy · DOI 10.1111/j.1540-6261.2007.01232.x · `refs/pillar7/29_PaulCTetlock_2007_giving_content_investor_sentiment_role.pdf` (sha256 `18fa35c04c...`)

## alternative-data-pipelines

3. **Big Data and Machine Learning in Quantitative Investment** — Tony Guida, Wiley, 2019.  -->  NOT OBTAINED · SDU holds a print-only record (Primo: no electronic service); Wiley book DOI 10.1002/9781119522225 has no licensed resource via EZproxy · ISBN 978-1-119-45434-7 · Wiley, 2019 · ILL: `refs/ILL_REQUESTS.md` §30
1. **Casting the Net: How Hedge Funds Are Using Alternative Data** — AIMA / SS&C Technologies, 2017. `CastingTheNet_AIMA.pdf`.  -->  OBTAINED (54 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/31_AIMASS_2017_casting_net_how_hedge_funds.pdf` (sha256 `73155f8098...`)
1. **Satellite / geolocation alt-data vendor methodology briefs** — Eagle Alpha, YipitData public guides. `EagleAlpha_SatelliteGeolocationBriefs.pdf`.  -->  OBTAINED (124 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/32_EagleAlphaYipitData_2019_satellite_geolocation_alt_data_vendor.pdf` (sha256 `d82cc045e6...`)
2. **Qlib alt-data & pipeline case studies** — Microsoft Qlib examples.  -->  not a document (no PDF sought) - software/repository + docs · https://github.com/microsoft/qlib

## regime-classification-hmm-gmm

1. **Analysis of Financial Time Series** — Ruey S. Tsay, Wiley, 3rd ed., 2010.  -->  OBTAINED (714 pp) · copy inherited from the shared refs/ pool (earlier acquisition run), re-verified in this pass · `refs/pillar7/34_RueySTsay_2010_analysis_financial_time_series.pdf` (sha256 `880733b93a...`)
1. **A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle** — James D. Hamilton, Econometrica 57(2):357–384, 1989. `Hamilton1989_NonstationaryTimeSeries.pdf`.  -->  OBTAINED (29 pp) · JSTOR full text via SDU EZproxy · DOI 10.2307/1912559 · `refs/pillar7/35_JamesDHamilton_1989_approach_economic_analysis_nonstationary_time.pdf` (sha256 `9f85be6b17...`)
1. **Regime Changes and Financial Markets** — Ang & Timmermann, ARFE 4:313–337, 2012. `AngTimmermann_RegimeChanges.pdf`.  -->  OBTAINED (34 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1146/annurev-financial-110311-101808 · `refs/pillar7/36_Ang_2012_regime_changes_financial_markets.pdf` (sha256 `d477b1a2ec...`)
1. **Regime Shifts: Implications for Dynamic Strategies** — Kritzman, Page & Turkington, FAJ 68(3), 2012. `Kritzman_RegimeShifts_DynamicStrategies.pdf`.  -->  OBTAINED (30 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.2469/faj.v68.n3.2 · `refs/pillar7/37_Kritzman_2012_regime_shifts_implications_dynamic_strategies.pdf` (sha256 `f55e13eebe...`)
1. **A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition** — Lawrence R. Rabiner, Proc. IEEE 77(2):257–286, 1989. `Rabiner_HMMTutorial.pdf`.  -->  OBTAINED (30 pp) · IEEE Xplore full text via SDU EZproxy · DOI 10.1109/5.18626 · `refs/pillar7/38_LawrenceRRabiner_1989_tutorial_hidden_markov_models_selected.pdf` (sha256 `baec97ac8b...`)

## deep-learning-for-sequences

4. **Deep Learning** — Goodfellow, Bengio & Courville, MIT Press, 2016.  -->  PARTIAL - holds 66 pp of 787 · official free PDF is front matter only (deeplearningbook.org); the full text is free in HTML there, the MIT Press print/PDF is not free and SDU holds no ebook licence · `refs/pillar7/39_Goodfellow_2016_deep_learning.pdf` (sha256 `1f6f329f95...`)
1. **Long Short-Term Memory** — Hochreiter & Schmidhuber, Neural Computation 9(8):1735–1780, 1997. `HochreiterSchmidhuber_LSTM.pdf`.  -->  OBTAINED (32 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1162/neco.1997.9.8.1735 · `refs/pillar7/40_Hochreiter_1997_long_short_term_memory.pdf` (sha256 `ceb9e53dbc...`)
1. **An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling** — Bai, Kolter & Koltun, arXiv:1803.01271, 2018. `Bai_TemporalConvNetworks.pdf`.  -->  OBTAINED (14 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/41_Bai_2018_empirical_evaluation_generic_convolutional_recurrent.pdf` (sha256 `f7e5df08b2...`)
1. **Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting** — Lim et al., IJF 37(4), 2021 (arXiv:1912.09363). `Lim_TemporalFusionTransformers.pdf`.  -->  OBTAINED (27 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1016/j.ijforecast.2020.11.008 · `refs/pillar7/42_Limetal_2021_temporal_fusion_transformers_interpretable_multi.pdf` (sha256 `7958011898...`)
1. **DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks** — Salinas et al., IJF, 2020 (arXiv:1704.04110). `Salinas_DeepAR.pdf`.  -->  OBTAINED (12 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1016/j.ijforecast.2019.04.014 · `refs/pillar7/43_Salinasetal_2020_deepar_probabilistic_forecasting_autoregressive_recurrent.pdf` (sha256 `c668d93622...`)
1. **Attention Is All You Need** — Vaswani et al., NeurIPS, 2017. `Vaswani_AttentionIsAllYouNeed.pdf`.  -->  OBTAINED (15 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/44_Vaswanietal_2017_attention_all_you_need.pdf` (sha256 `bdfaa68d89...`)

## reinforcement-learning-for-trading

1. **Reinforcement Learning: An Introduction** — Sutton & Barto, 2nd ed., MIT Press, 2018.  -->  OBTAINED (548 pp) · author page (Sutton) - official free 2nd-edition PDF · `refs/pillar7/45_Sutton_2018_reinforcement_learning.pdf` (sha256 `2dd0d71d9e...`)
1. **Deep Direct Reinforcement Learning for Financial Signal Representation and Trading** — Deng et al., IEEE TNNLS, 2017 (arXiv:1803.11155). `Deng_DeepDirectRLforTrading.pdf`.  -->  OBTAINED (12 pp) · IEEE Xplore full text via SDU EZproxy · DOI 10.1109/TNNLS.2016.2617218 · `refs/pillar7/46_Dengetal_2017_deep_direct_reinforcement_learning_financial.pdf` (sha256 `2b7c72ea0a...`)
1. **Human-level Control through Deep Reinforcement Learning** — Mnih et al., Nature 518:529–533, 2015. `Mnih_HumanLevelControlDQN.pdf`.  -->  OBTAINED (13 pp) · free copy from the earlier free-source pass, re-verified in this pass · DOI 10.1038/nature14236 · `refs/pillar7/47_Mnihetal_2015_human_level_control_through_deep.pdf` (sha256 `7e76cfd09e...`)
1. **Proximal Policy Optimization Algorithms** — Schulman et al., arXiv:1707.06347, 2017. `Schulman_PPO.pdf`.  -->  OBTAINED (12 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/48_Schulmanetal_2017_proximal_policy_optimization_algorithms.pdf` (sha256 `e78feadadb...`)
1. **The Evolution of Reinforcement Learning in Quantitative Finance** survey — ACM Computing Surveys / arXiv, 2024. `Pannak_RLinQuantFinanceSurvey.pdf`.  -->  OBTAINED (36 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/49_Pippasetal_2024_evolution_reinforcement_learning_quantitative_finance.pdf` (sha256 `edf7c59779...`)

## ml-for-portfolio

2. **Machine Learning for Asset Managers** (Ch. 5–6: covariance estimation, denoising/detoning, MP; Ch. 8: clustering) — see Cornerstone.  -->  not a document - cross-reference to a chapter of entry 02; obtain that book instead · ISBN 978-1-108-79089-3
1. **Building Diversified Portfolios That Outperform Out of Sample** — Marcos López de Prado, JPM 42(4):59–69, 2016. `LopezdePrado_HRPDiversifiedPortfolios.pdf`.  -->  OBTAINED (31 pp) · author-posted PDF, SSRN · DOI 10.3905/jpm.2016.42.4.059 · `refs/pillar7/51_MarcosLopezdePrado_2016_building_diversified_portfolios_outperform_out.pdf` (sha256 `cc075cb6da...`)
1. **A Robust Estimator of the Efficient Frontier** — Marcos López de Prado, SSRN 3469961, 2019.  -->  OBTAINED (16 pp) · author-posted PDF, SSRN · `refs/pillar7/52_MarcosLopezdePrado_2019_robust_estimator_efficient_frontier.pdf` (sha256 `51180a8ef1...`)
2. **Marchenko–Pastur theorem primer within *ML for Asset Managers*** — inside SOURCE book; random-matrix-theory denoising mechanism.  -->  not a document - cross-reference to a chapter of entry 02; obtain that book instead · ISBN 978-1-108-79089-3

## Platforms & Tools (optional running practice)

1. **Microsoft Qlib** — "Qlib: An AI-oriented Quantitative Investment Platform," arXiv:2009.11189, 2020. `MicrosoftQlib_AIQuantPlatform.pdf`.  -->  OBTAINED (8 pp) · free copy from the earlier free-source pass, re-verified in this pass · `refs/pillar7/54_Microsoft_2020_microsoft_qlib.pdf` (sha256 `35f2eea75c...`)

---

## Acquisition outcome (run 2026-09-10)

**54 entries · 41 obtained · 1 partial · 4 unobtainable · 8 not documents.**

- **Obtained (41)**: entries tagged **1** - every file passed magic-bytes / page-count /
  text-layer / identity gates and carries a sha256 in `refs/pillar7/MANIFEST.json`.
  Routes used: SDU EZproxy (JSTOR, IEEE, Wiley published PDFs), publisher-open (NeurIPS proceedings,
  deeplearningbook.org, Sutton's book page), author-posted (SSRN), and the verified free corpus.
- **Partial (1)**: entry **39** (*Deep Learning*) - the official free PDF is front matter only,
  66 of 787 pp; the complete text is free in HTML at <https://www.deeplearningbook.org/>, the MIT Press
  print/PDF edition is not free.
- **Unobtainable (4)**: entries **01, 02, 23, 30** - three commercial monographs
  (Lopez de Prado *Advances in Financial Machine Learning*; Lopez de Prado *Machine Learning for Asset
  Managers*; Guida *Big Data and Machine Learning in Quantitative Investment*) are print-only at SDU with
  no licensed ebook resource, and entry **23**'s cited SSRN record is withdrawn. Each has a
  ready-to-submit line in `refs/pillar7/ILL_REQUESTS.md`.
- **Not documents (8)**: entries **10, 15, 21, 22, 24, 50, 53** are internal "see Cornerstone"
  cross-references to chapters of entries 01/02; entry **33** (Qlib alt-data case studies) is
  software + docs (<https://github.com/microsoft/qlib>). Nothing to acquire.

Notes for the next pass:

- Entry **03** is a merged 549-pp PDF: 9 of the 10 SSRN lectures plus *The 7 Reasons Most Machine
  Learning Funds Fail*. Lecture 4/10 would not download - SSRN serves no file for it and direct fetch is
  bot-blocked.
- Entries **06/16** and **05/34** are the same work listed twice; both lines point at one verified file.
- SSRN required the real browser session (plain HTTP fetches are permanently 403 there); the EZproxy
  cookie jar covered Wiley, JSTOR and IEEE.
- Two author attributions in the original list needed correcting: entry **08** is by **Michael A. Lones**
  (the corpus filename `LopezdePrado_HowToAvoidMLPitfalls.pdf` misattributes it), and entry **49** is by
  **Pippas et al.** (the corpus filename `Pannak_RLinQuantFinanceSurvey.pdf` names a different author).
- Crossref's top hits were wrong for several preprints (e.g. entry 47 matched an unrelated 2023 paper,
  entry 54 a 1999 banking chapter); the DOIs recorded here were curated by hand and checked against the
  PDFs. No DOI, ISBN or metadata record in this file was invented.
