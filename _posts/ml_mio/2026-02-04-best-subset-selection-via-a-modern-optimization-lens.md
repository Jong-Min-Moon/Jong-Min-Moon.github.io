---
layout: distill
title: "Best Subset Selection via a Modern Optimization Lens"
description: "Lecture summary for 02-04-2026 on Best Subset Selection"
date: 2026-02-04
categories: ml_mio optimization statistics
tags: machine-learning mixed-integer-programming best-subset-selection
project: ml_mio
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
bibliography: 2026-02-04-best-subset-selection.bib
toc:
  - name: Overview
  - name: Best Subset Selection (BSS) Problem
  - name: Modern Optimization Approach
  - name: Computational Advantages
---

## Best-Subsets: Current Approaches and Limitations

**Lasso ($\ell_1$-regularization)** is an extremely effective proxy for best-subset selection. Its primary strengths are:

* **Computation:** As a convex optimization problem, it benefits from fast, well-understood solvers.
* **Theory:** The statistical properties and convergence rates are well-documented.

However, Lasso can fall short in terms of both **variable selection consistency** and **prediction error**. This is highlighted by the following risk bound 

$$\sup_{\|\beta^*\|_0 \leq k} \frac{1}{n} \mathbb{E}(\|\mathbf{X}\hat{\beta}_{L1} - \mathbf{X}\beta^*\|_2^2) \lesssim \frac{1}{\gamma^2} \frac{\sigma^2 k \log p}{n}$$
This bound is tight (minimax optimal; <d-cite key="raskutti_minimax_2011"></d-cite>:)
### The Impact of High Correlation
A critical factor in this bound is the compatibility constant (or restricted eigenvalue) **$\gamma$**, which depends heavily on the design matrix $\mathbf{X}$. 

Specifically, when the correlation between columns of $\mathbf{X}$ is strong, **$\gamma$ becomes very small**. Because $\gamma^2$ appears in the denominator, the error bound "blows up," leading to poor predictive performance and unstable variable selection. This sensitivity to collinearity is a well-known limitation of the Lasso framework compared to exact $L_0$ methods.

## $\ell_0$ approach

This paper focuses on solving the **$\ell_0$-constrained** least squares problem to certifiable optimality:

$$\min_{\beta} \frac{1}{2} \|\mathbf{y} - \mathbf{X}\beta\|_2^2 \quad \text{s.t.} \quad \|\beta\|_0 \leq k$$

The methodology integrates tools from various branches of mathematical optimization. While **Mixed-Integer Programming (MIP)** is a core component, the approach also leverages **Discrete First-Order Methods**. These methods are directly motivated by traditional first-order techniques in convex optimization and are applied to the following general problem:

$$\min_{\beta} g(\beta) \quad \text{s.t.} \quad \|\beta\|_0 \leq k$$

Here, $g(\beta)$ is a convex function that satisfies the **Lipschitz gradient condition**:

$$\|\nabla g(\beta) - \nabla g(\beta_0)\| \leq \ell \cdot \|\beta - \beta_0\|$$

By combining these discrete methods with modern computational techniques from MIP, the framework can handle significantly larger feature spaces than previous exact $\ell_0$ approaches while maintaining global optimality guarantees.

## Mixed Integer Optimization (MIO)

**Mixed Integer Optimization (MIO)** is a mature subfield of mathematical optimization that provides a robust framework for modeling and solving structured non-convex problems. Because the field is so well-established, we have a deep understanding of the "under-the-hood" mechanics within modern solvers.

### Complexity vs. Practicality
While MIO is **worst-case NP-hard**, this theoretical classification does not mean these problems are unsolvable. The prevailing attitude in modern operations research is that NP-hardness is a "challenge accepted". The goal is to find efficient ways to solve these problems in practice. 

### The MIO Renaissance
We have seen a significant rise in the utility of **Mixed Integer Optimization (MIO)** due to dramatic improvements in both software and algorithms over the last decade. Leading solvers like **Gurobi** and **CPLEX** have demonstrated nearly a **2x speedup every year**, independent of hardware advancements.

This exponential growth in computational efficiency has led major tech companies, including **Google** and **Microsoft**, to rely on Gurobi to solve their most complex large-scale optimization problems. Given this revolution in the "workhorse" tools of mathematical optimization, the paper poses a provocative and fundamental question:

> **"Why not statistics?"**

If MIO can solve massive industrial logistics and scheduling problems, it should be leveraged to provide certifiable, global solutions to the structured non-convex problems inherent in statistical learning, such as best-subset selection.
