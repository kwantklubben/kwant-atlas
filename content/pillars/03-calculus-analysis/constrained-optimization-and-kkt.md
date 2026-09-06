---
title: "Constrained Optimization & KKT Conditions"
tags: [optimization, kkt, lagrange, convex]
---

# Constrained Optimization & KKT Conditions

Nearly every decision in quantitative finance is an optimization problem subject to constraints: maximizing expected return subject to risk budgets, sector limits, and leverage caps.

## 1. The General Non-Linear Program
$$\min_{\mathbf{x} \in \mathbb{R}^n} f_0(\mathbf{x})$$
$$\text{subject to} \quad f_i(\mathbf{x}) \le 0 \quad (i=1, \dots, m), \quad h_j(\mathbf{x}) = 0 \quad (j=1, \dots, p)$$

## 2. The Lagrangian Function
$$\mathcal{L}(\mathbf{x}, \boldsymbol{\lambda}, \boldsymbol{\nu}) = f_0(\mathbf{x}) + \sum_{i=1}^m \lambda_i f_i(\mathbf{x}) + \sum_{j=1}^p \nu_j h_j(\mathbf{x})$$

## 3. Karush-Kuhn-Tucker (KKT) Necessary Conditions
If $\mathbf{x}^*$ is a local minimum satisfying regularity conditions:
1. **Stationarity:** $\nabla_{\mathbf{x}} \mathcal{L}(\mathbf{x}^*, \boldsymbol{\lambda}^*, \boldsymbol{\nu}^*) = \mathbf{0} \iff \nabla f_0(\mathbf{x}^*) + \sum_{i=1}^m \lambda_i^* \nabla f_i(\mathbf{x}^*) + \sum_{j=1}^p \nu_j^* \nabla h_j(\mathbf{x}^*) = \mathbf{0}$
2. **Primal Feasibility:** $f_i(\mathbf{x}^*) \le 0 \quad \forall i$, and $h_j(\mathbf{x}^*) = 0 \quad \forall j$.
3. **Dual Feasibility:** $\lambda_i^* \ge 0 \quad \forall i$.
4. **Complementary Slackness:** $\lambda_i^* f_i(\mathbf{x}^*) = 0 \quad \forall i$.
   - *Interpretation:* Either constraint $i$ is binding ($f_i(\mathbf{x}^*) = 0$) and its shadow price $\lambda_i^* > 0$, OR the constraint is inactive ($f_i(\mathbf{x}^*) < 0$) and $\lambda_i^* = 0$.

### Convexity Guarantee
If $f_0, f_i$ are convex functions and $h_j$ are affine, the KKT conditions are **necessary and sufficient** for global optimality.
