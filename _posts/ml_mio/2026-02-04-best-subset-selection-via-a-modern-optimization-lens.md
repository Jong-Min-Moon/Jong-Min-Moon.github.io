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
paper_key: bertsimasBestSubsetSelection2016
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
The cardinality constraint makes problem  NP-hard. Exisiting statistical literature do not scale to problem sizes larger than p = 30.


However, this paper integrates tools from various branches of mathematical optimization. While **Mixed-Integer Programming (MIP)** is a core component, the approach also leverages **Discrete First-Order Methods**. These methods are directly motivated by traditional first-order techniques in convex optimization and are applied to the following general problem:

$$\min_{\beta} g(\beta) \quad \text{s.t.} \quad \|\beta\|_0 \leq k$$

Here, $g(\beta)$ is a convex function that satisfies the **Lipschitz gradient condition**:

$$\|\nabla g(\beta) - \nabla g(\beta_0)\| \leq \ell \cdot \|\beta - \beta_0\|$$

By combining these discrete methods with modern computational techniques from MIP, the framework can handle significantly larger feature spaces than previous exact $\ell_0$ approaches while maintaining global optimality guarantees.

### Generalization and Flexibility of the MIO Framework

A significant advantage of the framework proposed by Bertsimas et al. (2016) is its inherent flexibility, as it can be seamlessly adapted to several variants of the best-subset regression problem. The general formulation is expressed as:

$$\min_{\beta} \frac{1}{2} \|\mathbf{y} - \mathbf{X}\beta\|_q^q \quad \text{s.t.} \quad \|\beta\|_0 \le k, \quad \mathbf{A}\beta \le \mathbf{b}$$

This adaptability allows for several powerful modeling extensions:

* **Diverse Loss Functions**: The parameter $q \in \{1, 2\}$ allows the user to switch between a **least squares** loss ($q=2$) and a **least absolute deviation** (L1) loss ($q=1$) on the residuals $\mathbf{r} := \mathbf{y} - \mathbf{X}\beta$.
* **Structured Constraints**: The inclusion of $\mathbf{A}\beta \le \mathbf{b}$ enables the integration of **polyhedral constraints**, allowing for the enforcement of specific domain knowledge or structural requirements directly within the optimization.
 
 

## Mixed Integer Optimization (MIO)
**Mixed Integer Optimization (MIO)** is a mature subfield of mathematical optimization that provides a robust framework for modeling and solving structured non-convex problems. Because the field is so well-established, we have a deep understanding of the "under-the-hood" mechanics within modern solvers.

### Diverse Problem Classes
The framework is highly versatile, supporting various problem types including:
* **Mixed Integer Linear Optimization (MILO)**
* **Mixed Integer Second-Order Cone Programming (MISOCP)**

### A Comprehensive Solver Ecosystem
Users can choose from a wide range of powerful solvers depending on their specific needs:
* **Commercial Solvers**: Industry leaders include **Gurobi**, **CPLEX**, and **Xpress**.
* **Non-commercial/Open-Source Solvers**: Reliable options include **SCIP**, **CBC**, **GLPK**, and **lpsolve**.

### Seamless Integration
MIO tools are easily accessible through modern programming interfaces, allowing for flexible implementation across different environments:
* **Languages**: Full support for **Python**, **R**, **Matlab**, and **Julia** (specifically through **JuMP**).
### Complexity vs. Practicality
While MIO is **worst-case NP-hard**, this theoretical classification does not mean these problems are unsolvable. The prevailing attitude in modern operations research is that NP-hardness is a "challenge accepted". The goal is to find efficient ways to solve these problems in practice. 



### The MIO Renaissance
We have seen a significant rise in the utility of **Mixed Integer Optimization (MIO)** due to dramatic improvements in both software and algorithms over the last decade. Leading solvers like **Gurobi** and **CPLEX** have demonstrated nearly a **2x speedup every year**, independent of hardware advancements.

This exponential growth in computational efficiency has led major tech companies, including **Google** and **Microsoft**, to rely on Gurobi to solve their most complex large-scale optimization problems. Given this revolution in the "workhorse" tools of mathematical optimization, the paper poses a provocative and fundamental question:

> **"Why not statistics?"**

If MIO can solve massive industrial logistics and scheduling problems, it should be leveraged to provide certifiable, global solutions to the structured non-convex problems inherent in statistical learning, such as best-subset selection.

# Mixed Integer Quadratic Programming (MIQP)
 
The general form of a Mixed Integer Quadratic Programming (MIQP) problem is defined as follows:

$$\min_{\alpha} \alpha^T \mathbf{Q} \alpha + \alpha^T \mathbf{a}$$

**Subject to:**
* **Linear Constraints**: $\mathbf{A}\alpha \le \mathbf{b}$
* **Discrete Variables**: $\alpha_i \in \{0, 1\}, \quad i \in \mathcal{I}$
* **Continuous Variables**: $\alpha_j \ge 0, \quad j \notin \mathcal{I}$

### Parameters and Notation
* **Input Parameters**: $\mathbf{a} \in \mathbb{R}^m$, $\mathbf{A} \in \mathbb{R}^{k \times m}$, and $\mathbf{b} \in \mathbb{R}^k$.
* **Quadratic Matrix**: $\mathbf{Q} \in \mathbb{R}^{m \times m}$ is assumed to be **positive semidefinite**, ensuring the objective remains convex.
* **Inequalities**: The symbol "$\le$" denotes element-wise inequalities.
* **Variable Set**: The optimization is performed over $\alpha \in \mathbb{R}^m$, which contains both discrete indices ($\mathcal{I} \subset \{1, \dots, m\}$) and continuous indices.
# Best-Subset Selection via  MIO 
To implement the best-subset selection problem within an MIO framework, the standard least squares objective is coupled with "Big-M" constraints to bridge the continuous coefficients $\beta$ and the binary indicators $z$.

 
The problem is formally expressed as:

$$\min_{\beta, z} \frac{1}{2} \|\mathbf{y} - \mathbf{X}\beta\|_2^2$$

**Subject to:**
* **Big-M Constraints:** $-M z_i \le \beta_i \le M z_i, \quad i = 1, \dots, p$
* **Binary Indicators:** $z_i \in \{0, 1\}, \quad i = 1, \dots, p$
* **Sparsity Constraint:** $\sum_{i=1}^{p} z_i \le k$

### Logical Coupling via Big-M
The parameter $M$ is a sufficiently large constant (e.g., $M = 1000$) that enforces the relationship between variable selection and estimation:
* **If $z_i = 0$:** The constraint forces the coefficient $\beta_i$ to be exactly zero.
* **If $z_i = 1$:** The coefficient $\beta_i$ is free to take any value within the practical range $[-M, M]$.

### Certifiable Optimality
A primary advantage of this approach is the **Certificate of Optimality** provided by MIP technology. Unlike heuristic methods, MIO solvers systematically tighten the gap between the **upper bound** (the best feasible solution found) and the **lower bound** (the theoretical best possible value).



This allows for controlled convergence; the solver can be stopped once a pre-defined **optimality gap** (e.g., 1% or 5%) is achieved, providing a rigorous guarantee on the solution's proximity to the global optimum.

![MIP trajectory](assets/img/MIP_trajectory_typical.png)

The paper claims that for $n \leq 1000, p \leq 1000$, the MIO approach can solve the best-subset selection problem to good quality within a few minutes, but certificates of optimality can take longer.

 

### Improvement 1. Implied Inequalities
A standard strategy in integer programming is to introduce **implied inequalities** that, while mathematically redundant, significantly tighten the feasible region for the solver's relaxation. This leads to much tighter lower bounds and faster pruning of the branch-and-bound tree.

#### SOS-1
Any feasible solution to formulation above will have $(1 − z_i)\beta_i = 0$ for every $i \in \{1, \dots, p\}$. This constraint can be modeled via integer optimization using Specially Ordered Sets of Type  (SOS-1), as follows:  $(1 − z_i)\beta_i = 0 \Leftrightarrow (\beta_i, 1 − z_i) : \text{SOS-1}$,  for every $i = 1, \dots, p$. 
This removed the specification of big-M. However, in practice, it is better to keep it. Even more, it's better to add additional $\ell_1$ constraint. As a result, we have:

$$\begin{aligned}
& \min_{\boldsymbol{\beta}, \mathbf{z}} & & \frac{1}{2} \boldsymbol{\beta}^T (\mathbf{X}^T \mathbf{X}) \boldsymbol{\beta} - \langle \mathbf{X}' \mathbf{y}, \boldsymbol{\beta} \rangle + \frac{1}{2} |\mathbf{y}|2^2 \
\\
& \text{s.t.} & & (\beta_i, 1 - z_i) : \text{SOS-1}, \quad i = 1, \dots, p \
\\& & & z_i \in {0, 1}, \quad i = 1, \dots, p \
\\& & & \sum_{i=1}^{p} z_i \leq k \
\\& & & -M_U \leq \beta_i \leq M_U, \quad i = 1, \dots, p \
\\& & & |\boldsymbol{\beta}|_1 \leq \mathcal{M}_\ell
\end{aligned} \quad (2.5)$$

 
$$\quad \sum_{i=1}^{p} z_i \leq k$$

 The original $\ell_0$ problem is strengthened by incorporating these additional norm constraints:

$$\min_{\beta} \|\mathbf{y} - \mathbf{X}\beta\|_2^2$$

$$\text{s.t.} \quad \|\beta\|_0 \leq k$$
$$\|\beta\|_{\infty} \leq \delta_{11}, \quad \|\beta\|_1 \leq \delta_{21}$$
$$\|\mathbf{X}\beta\|_{\infty} \leq \delta_{12}, \quad \|\mathbf{X}\beta\|_1 \leq \delta_{22}$$

By bounding the coefficients and their projections ($\mathbf{X}\beta$) in both $L_1$ and $L_\infty$ spaces, the solver can discard suboptimal regions of the search space much more aggressively.

---

### 2. Polyhedral Outer Approximation: Simplifying Curves into Straight Lines

Nonlinear optimization is difficult and slow to solve directly. To overcome this, we approximate the "curvy" problem using a sequence of **Mixed-Integer Linear Programs (MILP)**, which modern solvers can handle with extreme efficiency.
Think of it like approximating a circle by drawing a many-sided polygon around it; as you add more sides (straight lines), your approximation gets closer and closer to the actual curve.

#### The Mathematical Framework
Modern solvers perform best when working with linear or piecewise-linear structures. To handle a quadratic (squared) objective like least-squares within this linear framework, we use a **polyhedral outer approximation** $\mathcal{P}$:

$$\mathcal{P} \subset \left\{ \beta : \frac{1}{2} \|\mathbf{y} - \mathbf{X}\beta\|_2^2 \leq t \right\}$$

This approach breaks down the global "curvy" loss into individual, manageable pieces using auxiliary variables $t_i$ and residuals $r_i$:

* **Aggregate Loss**: We ensure the sum of individual errors stays below a total threshold $t$: $\sum_{i \in [n]} t_i \leq t$.
* **Individual Residual Bounds**: Each specific error point $r_i^2$ is bounded by its own $t_i$: $r_i^2 \leq t_i, \quad i \in [n]$.
* **Residual Definition**: The residual is the difference between our prediction and the actual data: $\mathbf{r} = \mathbf{y} - \mathbf{X}\beta$.



#### Why This Works
Instead of trying to solve the complex squared term all at once, the algorithm surrounds the quadratic curve with a series of **linear tangential cuts**—flat planes that touch the curve. This allows the solver to leverage high-speed linear programming engines to iteratively refine the solution. Each time the solver finds a point outside the true curve, it adds a new "flat" constraint to slice away that suboptimal region, eventually "wrapping" the solution tightly around the global optimum.