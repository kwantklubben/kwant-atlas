---
title: "5.7.1 The Kelly Criterion from Zero"
tags:
  - pillar-portfolio-optimization
  - kelly-criterion
  - bet-sizing
  - intuition
  - log-utility
---

**Basic Prerequisites:** [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|03 · Multiplicative Growth]] (log returns, volatility drag).

---

### 1. Intuition & Practical Objective

This page builds the *why* of Kelly with **no prior quantitative knowledge needed**. The objective is one idea: **betting maximises expected wealth, but expected wealth is the wrong thing to maximise - the thing that decides whether you get rich or go broke is the *growth rate* of your bankroll, $\mathbb{E}[\ln W]$, and it has a unique optimal size.**

Start with the dumbest question: *if I have an edge, should I bet as much as I can?* Imagine a coin that lands heads 55% of the time. Every bet: win and you double your stake, lose and you lose it. The expected value per dollar staked is $0.55(1)-0.45(1)=+0.10$, a 10% edge. If expected value were the objective, you'd bet everything, every round: $E[W]$ after $n$ rounds is $(1+f(2p-1))^n$, which grows fastest at $f=1$ (bet it all).

But **betting everything is certain death.** One loss out of a long enough run and you have a zero bankroll that never recovers - and with $p=0.55$ you *will* eventually hit a loss. Expected wealth loves this; you do not. The resolution is to maximise not $\mathbb{E}[W]$ but $\mathbb{E}[\ln W]$ - the growth rate that your *own single path through time* actually compounds at.

Three steps, three "aha"s:

1. **Bet zero and you never grow - bet too much and volatility eats you.** Compounding is geometric: $W_n=W_0(1+f)^S(1-f)^F$, so the per-round growth rate is $g(f)=p\ln(1+f)+q\ln(1-f)$, which is **concave** - it goes *up* then *down*, and past a critical fraction it turns *negative* even though the edge is positive. There is a middle sweet spot.
2. **The growth rate is the only number that survives compounding.** $E[W]$ is an average *across parallel worlds*; $g(f)$ is the average *along your one real path*. For multiplicative wealth these differ - the entire lesson of [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]].
3. **The optimum is computable, not a vibe.** Maximising a concave function of $f$ gives a closed-form maximiser. That maximiser is the **Kelly fraction** $f^*$, unique and explicit.

> **Takeaway.** The right objective is the growth rate $g=\mathbb{E}[\ln W]$, not expected wealth. Its maximiser $f^*$ is Kelly's famous bet size - and it is systematically *smaller* than "bet as much as the edge suggests", because volatility drag punishes overbetting harder than it rewards boldness.

---

### 2. Mathematical Ground Truth & Derivations

**The concave growth function.** Bet a fixed fraction $f$ on each fair-odds coin toss with $p>1/2$, $q=1-p$. After $n$ trials with $S$ heads and $F=n-S$ tails,

$$
W_n=W_0(1+f)^S(1-f)^F
\;\Longrightarrow\;
\boxed{\;g(f)=p\ln(1+f)+q\ln(1-f)\;}
$$

**Derivation by maximisation.** This is concave: $g''(f)=-p/(1+f)^2-q/(1-f)^2<0$, so the critical point is the unique global max. Set $g'(f)=\frac{p}{1+f}-\frac{q}{1-f}=0$:

$$
f^*=p-q.
$$

**Why $\mathbb{E}[\ln W]$ and not $\mathbb{E}[W]$.** The expected terminal wealth at full Kelly grows like $E[W]\propto(1+2p-1)^n$, maximised at $f=1$. But $\ln W$ - the growth you actually live with - is maximised at $f^*=p-q$, which for $p=0.55$ is only $0.10$. The gap between "maximise the mean" and "maximise the median/typical path" is precisely the Jensen gap of multiplicative growth from the foundations folder.

**The critical fraction $f_c$.** Since $g(0)=0$, $g$ rises to a positive peak at $f^*$, then falls through zero at a unique $f_c>f^*$. For any $f>f_c$ the growth rate is negative and ruin is almost sure. For $p=0.55$, $f_c=0.1987$ - just $2\times$ the full-Kelly fraction is already a losing strategy.

---

### 3. Computational Implementation - the growth-rate landscape

Stdlib only. Sweep the growth function, then simulate what *actually* happens at the Kelly fraction vs. betting everything.




Read the first block: the growth rate is *positive* only between $f=0$ and $f_c\approx0.199$; the **maximum is at $f=0.10$**, and beyond $f\approx0.2$ the edge turns into a guaranteed-loss machine. The second block is the punchline: **betting everything turns your $+10\%$ edge into almost-sure ruin**, while betting the Kelly fraction (a fifth as much) grows a bankroll $2.7\times$ over 200 bets with zero ruin in 40,000 trials.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Expected value says bet it all."** $\mathbb{E}[W]$ is maximised by all-in, but it is the *ensemble* average across parallel worlds - not what one investor's single path compounds. Maximising $\mathbb{E}[W]$ when wealth multiplies is the classic non-ergodicity trap ([[foundations/ergodicity-and-statistical-mechanics/02-ensemble-vs-time-averages|02 · Ensemble vs Time Averages]]).
2. **Reading "$f_c=0.199$" as a safety margin.** It is not: $f_c$ is the boundary of *certain* ruin, not a target. Any estimate error that pushes the deployed fraction above $f_c$ - and overbetting is cheaper to do accidentally than underbetting - destroys the account deterministically.
3. **Treating this as a growth maximiser for *what* to bet, not *whether* to bet.** Kelly only sizes a position whose edge is real. If $p\le1/2$ there is no positive $f^*$ and the whole discussion is moot - sizing does not manufacture a signal.

---

### 5. Canonical Literature & Study References

- **Kelly, J. L. jr.**: *A New Interpretation of Information Rate*, Bell System Technical Journal 35(4) (1956) - the original growth-rate-vs-information connection. *Corpus-verified.*
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006), §2 - the coin-toss case, $g(f)$, $f^*=p-q$, the critical fraction and Thorp's Theorem 1. *Corpus-verified.*
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion* (2011) - the collected history and theory.

---

### 6. Connected Graph Bridges

- Base: [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|Multiplicative Growth & Volatility Drag]] · [[foundations/ergodicity-and-statistical-mechanics/02-ensemble-vs-time-averages|Ensemble vs Time Averages]]
- Continue: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/02-the-kelly-formula|02 · The Kelly Formula]] · [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Index Hub]]