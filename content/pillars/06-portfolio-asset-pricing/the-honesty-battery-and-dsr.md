---
title: "The Honesty Battery & Deflated Sharpe Ratio"
tags: [portfolio, honesty, dsr, psr, validation, de-prado]
---

# The Honesty Battery & Deflated Sharpe Ratio

The foundational methodology of KwantKlubben: every quantitative claim must be challenged by statistical deflation and permutation tests.

## 1. The Multiple-Testing Crisis
If an analyst tests $N = 1,000$ random moving average crossovers or neural network hyperparameter combinations on historical prices, the expected maximum Sharpe ratio under pure noise is:
$$\mathbb{E}[\max_{k=1,\dots,N} SR_k] \approx \sqrt{2 \ln N} + \frac{\gamma}{\sqrt{2 \ln N}} > 3.0$$
A reported backtest Sharpe of 3.0 is entirely consistent with zero true skill!

---

## 2. Probabilistic Sharpe Ratio (PSR)
Adjusts the observed Sharpe ratio $\widehat{SR}$ for non-Gaussian skewness $\gamma_3$ and kurtosis $\gamma_4$:
$$\text{PSR}(SR^*) = \Phi\left( \frac{(\widehat{SR} - SR^*) \sqrt{T-1}}{\sqrt{1 - \gamma_3 \widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2}} \right)$$

---

## 3. Deflated Sharpe Ratio (DSR)
Deflates PSR by replacing benchmark $SR^*$ with the expected maximum Sharpe ratio under the null hypothesis of multiple testing:
$$SR^* = \sqrt{V(\{SR_k\})} \left( (1 - \gamma)Z^{-1}\left(1 - \frac{1}{N}\right) + \gamma Z^{-1}\left(1 - \frac{1}{Ne}\right) \right)$$
Where $V(\{SR_k\})$ is the variance of trial Sharpes across all attempts, and $N$ is the total trial count.

## KwantKlubben Repo Verification
In `kwantklubben`, test your returns directly:
```bash
python -m honesty.test_honesty
```
Every research pull request must provide an `honesty_card` showing positive DSR and permutation $p$-value $< 0.05$.
