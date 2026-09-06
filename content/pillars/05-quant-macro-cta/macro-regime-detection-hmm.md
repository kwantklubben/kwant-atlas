---
title: "Macro Regime Detection (HMMs)"
tags: [macro, regime, hmm, machine-learning]
---

# Macro Regime Detection (HMMs)

Financial markets behave completely differently during expansions, inflation shocks, liquidity squeezes, and recessions. Static models that assume constant parameters fail across regime transitions.

## Hidden Markov Models (HMM)
An HMM assumes the market transitions between unobservable latent states (e.g. State 0: Low Volatility Bull Market; State 1: High Volatility Bear Market).
- Transitions are governed by a Markov transition matrix $\mathbf{P}$.
- Asset returns in each state follow distinct Gaussian or Student-t emission distributions.
- Portfolio rules use the smoothed probability of being in State 1 to dynamically reduce leverage or rotate into defensive assets.
