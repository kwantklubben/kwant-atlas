---
title: "4.10.3 Frequency–Severity Modeling"
tags:
  - pillar-quantitative-risk
  - operational-risk
  - poisson
  - lognormal
  - pareto
  - severity-distribution
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

The objective: **turn two one-dimensional problems - "how often do losses hit?" and "how big is each hit?" - into the building blocks of a capital model.** Frequency $N$ and severity $X$ are modelled *separately* because they are driven by different things (a process error rate vs. the size of what breaks) and because separating them multiplies the usable data. This page fits each half and produces the two quantities LDA needs most: the severity law $F_X$ and the expected loss $\mathbb{E}[S]=\lambda\,\mathbb{E}[X]$.

The two halves feel different to a beginner, and should:

1. **Frequency is *thin* in both axes but easy.** The count per year is one parameter, $\lambda$. Estimate it by the sample mean number of events per year. Poisson is the default because rare-event counts converge to it and it has no free parameters to overfit.
2. **Severity is where the danger lives.** Loss sizes are positive, right-skewed, and - critically - **heavy-tailed**: $1-F_X(x)\sim x^{-\xi}$ rather than decaying exponentially. The standard families are the **lognormal** (thin-to-moderate tail) and the **Pareto / GPD** (power tail), with the Hill estimator quantifying the tail exponent directly.
3. **The tail exponent, not the mean, drives capital.** A Pareto tail with exponent $\xi$ has $\mathbb{E}[X]=\xi x_m/(\xi-1)$ (finite only if $\xi>1$) but a 99.9% quantile that grows like a power law. Getting $\xi$ slightly wrong moves capital by multiples.

---

### 2. Mathematical Ground Truth & Derivations

#### Frequency: the Poisson law

The annual event count is modelled as $N\sim\text{Poisson}(\lambda)$:

$$
\mathbb{P}(N=n)=\frac{e^{-\lambda}\lambda^{n}}{n!},\qquad \mathbb{E}[N]=\text{Var}(N)=\lambda.
$$

The single parameter is estimated by the method of moments / MLE alike: $\hat\lambda=\bar n$ (sample mean events per year). The Poisson assumption embeds two strong premises - events arrive independently and at a constant rate - both of which are *violated* in stress (the failure-mode bridge to [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes]]). Generalizations (negative binomial, which adds a dispersion parameter) exist precisely to loosen these.

#### Severity: lognormal

$X\sim\text{Lognormal}(\mu,\sigma)$ means $\ln X\sim N(\mu,\sigma^2)$, with

$$
\mathbb{E}[X]=e^{\mu+\sigma^2/2},\qquad \text{Var}(X)=e^{2\mu+\sigma^2}\big(e^{\sigma^2}-1\big).
$$

**Fitting (method of moments):** given sample mean $m$ and sample variance $v$ of the observed losses, solve

$$
\sigma^2=\ln\!\Big(1+\frac{v}{m^2}\Big),\qquad \mu=\ln m-\tfrac12\sigma^2.
$$

Because $\ln X$ is normal, the exact MLE is also available (sample mean/var of the logged data); the two agree closely for reasonable samples.

#### Severity: Pareto (the heavy-tail workhorse)

$X\sim\text{Pareto}(x_m,\xi)$, survival function

$$
1-F_X(x)=\Big(\frac{x_m}{x}\Big)^{\xi},\qquad x\ge x_m,\ \xi>0.
$$

First moment: $\mathbb{E}[X]=\xi x_m/(\xi-1)$ for $\xi>1$, infinite otherwise. The exponent $\xi$ is the **tail index**; the smaller $\xi$, the fatter the tail and the larger the extreme quantiles.

**The Hill estimator** estimates $\xi$ from the $k$ largest order statistics $x_{(n)}\ge\cdots\ge x_{(n-k+1)}$:

$$
\hat\xi=\frac{k}{\displaystyle\sum_{i=0}^{k-1}\ln x_{(n-i)}-k\ln x_{(n-k)}},
$$

i.e., the reciprocal of the average log-excess of the top $k$ observations above the $(k{+}1)$-th largest. Choosing $k$ is a bias–variance trade; small $k$ is low-bias but high-variance ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]]).

#### The expected loss

Given fitted $\hat\lambda$ and severity law with $\hat{\mathbb{E}}[X]$,

$$
\text{EL}=\mathbb{E}[S]=\lambda\,\mathbb{E}[X],
$$

the (cheap) central-tendency anchor that LDA later scales to a tail number.

---

### 3. Computational Implementation - fit the severity from observed losses

Fit a lognormal to 300 simulated observed events by method of moments, then compute $\mathbb{E}[X]$ and EL. Stdlib only.




The fit recovers the true lognormal (mu≈10, sigma≈0.8) from 300 noisy events and yields the expected annual loss - the frequency–severity halves now feeding the aggregate model.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The mean says nothing about the tail.** Fitting severity by matching $\mathbb{E}[X]$ is fine for EL but worthless for VaR - two severity laws with identical means (lognormal vs Pareto $\xi{=}1.5$) differ by a factor ~5.8 in the 99.9% loss ([[pillars/04-quantitative-risk/operational-risk/04-aggregate-loss-and-lda|04 · Aggregate Loss & LDA]]). Fitting the body is not fitting the tail.
2. **Choosing lognormal "because it fits the middle"** is the classic underestimation error - a lognormal fits the bulk of op-risk data well and badly misses the power-law extreme events that define capital. Tail-appropriate families (Pareto/GPD, or lognormal-GPD spliced) are required.
3. **Poisson independence/constant-rate assumptions.** Real op-risk events cluster (a fraud wave, a pandemic, a systems migration) and co-move in stress. Clustered arrivals inflate the variance beyond Poisson's $\text{Var}(N)=\lambda$, and the clean convolution of [[pillars/04-quantitative-risk/operational-risk/04-aggregate-loss-and-lda|04 · Aggregate Loss]] quietly assumes it away.
4. **Hill $k$ selection & data scarcity.** The Hill estimate swings wildly with $k$ and with small samples (see [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes]] for the quantified instability). Quoting "the" tail index without a sensitivity study over $k$ is not a number, it is a guess.

---

### 5. Canonical Literature & Study References

- **Panjer, *Operational Risk: Modeling Analytics*** (2006), Ch 2–4 - frequency (Poisson, negative binomial) and severity families (lognormal, Pareto, Burr, GPD) with fitting and diagnostics.
- **Embrechts, Klüppelberg & Mikosch, *Modelling Extremal Events*** (1997) - the heavy-tail theory; §6.4–6.5 Hill and related tail estimators.
- **Hill, Bruce M., *A Simple General Approach to Inference About the Tail of a Distribution***, *Annals of Statistics* 3(5):1163–1174 (1975) - the Hill estimator, original source (in the corpus).
- **McNeil, Frey & Embrechts, *Quantitative Risk Management*** (2015), Ch 2 & Ch 7 - distribution fitting and EVT-based tail estimation. *Corpus-verified.*

---

### 6. Connected Graph Bridges

- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Back: [[pillars/04-quantitative-risk/operational-risk/02-loss-event-types|02 · Loss Event Types]]
- Forward: [[pillars/04-quantitative-risk/operational-risk/04-aggregate-loss-and-lda|04 · Aggregate Loss & LDA]] · [[pillars/04-quantitative-risk/operational-risk/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (negative-binomial / clustered-frequency methods)
