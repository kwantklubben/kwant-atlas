---
title: "Real Analysis, Topology & Measure Theory"
tags: [analysis, measure-theory, topology, lebesgue]
---

# Real Analysis, Topology & Measure Theory

Advanced quantitative finance requires rigorous limits, convergence theorems, and measure theory. Without measure theory, concepts like "risk-neutral pricing" or "conditional expectation given a filtration" cannot be mathematically defined.

## 1. Metric Spaces and Compactness
- **Metric Space $(X, d)$:** A set with a distance function $d(x, y)$ satisfying positivity, symmetry, and the triangle inequality $d(x, z) \le d(x, y) + d(y, z)$.
- **Compactness (Heine-Borel Theorem):** A subset of $\mathbb{R}^n$ is compact if and only if it is closed and bounded. Continuous functions on compact sets attain their maximum and minimum (guaranteeing solutions exist in financial optimization).

---

## 2. Lebesgue Integration vs. Riemann Integration
The Riemann integral partitions the domain (x-axis) into vertical slices. If a function is highly oscillatory or discontinuous (such as indicator functions on rational numbers), Riemann sums fail to converge.

The **Lebesgue integral** partitions the range (y-axis) into horizontal slices and measures the "size" of the pre-image set:
$$\int_X f \, d\mu = \lim_{n \to \infty} \sum_{k} y_k \cdot \mu(\{x \in X : y_k \le f(x) < y_{k+1}\})$$

### The Three Master Convergence Theorems:
1. **Monotone Convergence Theorem (MCT):** If $0 \le f_1 \le f_2 \le \dots$ and $f_n \to f$, then $\lim \int f_n d\mu = \int f d\mu$.
2. **Fatou's Lemma:** $\int \liminf f_n d\mu \le \liminf \int f_n d\mu$.
3. **Dominated Convergence Theorem (DCT):** If $|f_n| \le g$ where $g$ is integrable, and $f_n \to f$ almost everywhere, then:
   $$\lim_{n \to \infty} \int f_n \, d\mu = \int f \, d\mu$$
   *Financial Use:* Allows interchanging limits and expectation operators: $\lim_{t \to T} \mathbb{E}[V(S_t)] = \mathbb{E}[\lim_{t \to T} V(S_t)]$.
