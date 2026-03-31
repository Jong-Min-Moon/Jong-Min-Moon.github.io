---
layout: distill
title: "Notes: Lagrangian Relaxation and Decomposition"
description: "An overview of Lagrangian relaxation, decomposition techniques, subgradient methods, and their applications in large-scale optimization."
date: 2026-03-30
categories: ise-617
tags: optimization lagrangian-relaxation decomposition
project: ise-617
math: true
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Introduction
  - name: Lagrangian Relaxation
  - name: The Lagrangian Dual Problem
  - name: Subgradient Method
  - name: Lagrangian Decomposition
  - name: Summary
---

# Introduction

In large-scale optimization, we often encounter problems that are "easy" to solve if not for a few complicating constraints. For instance, a problem might decouple into many independent subproblems if we remove a set of coupling constraints. **Lagrangian Relaxation** is a powerful technique that absorbs these complicating constraints into the objective function, penalizing violations using *Lagrangian multipliers*.

# Lagrangian Relaxation

Consider the original primal problem (Integer or Mixed-Integer Program):

<p>
$$
\begin{aligned}
Z_{IP} = \max_{x} \quad & c^T x \\
\text{s.t.} \quad & A x \le b \quad \leftarrow \text{(Complicating constraints)}\\
& D x \le d \quad \leftarrow \text{(Easy constraints)}\\
& x \in \mathbb{Z}^n_+
\end{aligned}
$$
</p>

Let $X = \{ x \in \mathbb{Z}^n_+ : D x \le d \}$ be the set of "easy" feasible solutions. The complicating constraints $A x \le b$ tie the variables together or make the problem intractable. 

We can relax the constraints $A x \le b$ by introducing a vector of non-negative multipliers $\lambda \ge 0$ and moving the constraints to the objective function. The **Lagrangian Relaxation (LR)** problem is:

<p>
$$
\begin{aligned}
Z_{LR}(\lambda) = \max_{x \in X} \quad & c^T x + \lambda^T (b - A x) \\
= \max_{x \in X} \quad & (c^T - \lambda^T A) x + \lambda^T b
\end{aligned}
$$
</p>

### Property: Upper Bound
For any $\lambda \ge 0$, the optimal value of the Lagrangian relaxation $Z_{LR}(\lambda)$ provides an **upper bound** (for maximization problems) on the true optimal value $Z_{IP}$. 

Proof: Let $x^*$ be the optimal solution to the original IP. Since $x^*$ is feasible for the IP, it satisfies $A x^* \le b$, implying $b - A x^* \ge 0$. Because $\lambda \ge 0$, the penalty term $\lambda^T (b - A x^*) \ge 0$. Therefore:
<p>
$$ Z_{LR}(\lambda) \ge c^T x^* + \lambda^T (b - A x^*) \ge c^T x^* = Z_{IP} $$
</p>

# The Lagrangian Dual Problem

Since any $\lambda \ge 0$ gives an upper bound, we naturally want to find the **tightest** (lowest) upper bound. This leads to the **Lagrangian Dual Problem**:

<p>
$$ Z_D = \min_{\lambda \ge 0} Z_{LR}(\lambda) $$
</p>

By weak duality, we know that $Z_{IP} \le Z_D$. The difference $Z_D - Z_{IP}$ is called the **duality gap**. 

Compared to the LP relaxation bound $Z_{LP}$, the Lagrangian dual bound is at least as good: $Z_{IP} \le Z_D \le Z_{LP}$. If the set $X$ has the *Integrality Property* (i.e., solving the optimization problem over $X$ yields the same result as solving over its convex hull), then $Z_D = Z_{LP}$. If $X$ does not have the integrality property, $Z_D$ can be strictly tighter than $Z_{LP}$.

# Subgradient Method

The function $Z_{LR}(\lambda)$ is piecewise linear and convex, but non-differentiable everywhere. To solve the Lagrangian dual problem, we typically use the **Subgradient Method**.

At a given $\lambda^k$, let $x^k$ be the optimal solution to the Lagrangian relaxation. A **subgradient** of $Z_{LR}(\lambda)$ at $\lambda^k$ is simply the slack in the relaxed constraint:
<p>
$$ g^k = b - A x^k $$
</p>

The subgradient update rule is:
<p>
$$ \lambda^{k+1} = \max\{ 0, \lambda^k - \alpha_k g^k \} $$
</p>
where $\alpha_k > 0$ is the step size. A common choice for the step size is the Polyak step size:
<p>
$$ \alpha_k = \frac{\pi_k (Z_{LR}(\lambda^k) - Z_{LB})}{\|g^k\|^2} $$
</p>
where $Z_{LB}$ is a known lower bound (from any feasible solution) and $\pi_k \in (0, 2]$ is a parameter that is iteratively decreased.

# Lagrangian Decomposition

**Lagrangian Decomposition** (also known as variable splitting or Guignard-Kim decomposition) is a specialized application of Lagrangian relaxation. It is primarily used when a problem contains multiple sets of complex constraints that, if separated, would make the problem significantly easier to solve. We achieve this by duplicating variables to artificially decouple these constraint sets.

#### **1. The Original Problem**
Suppose we have an optimization problem where a decision variable must satisfy two distinct sets of constraints simultaneously:

$$
\begin{aligned}
\max_{x} \quad & c^T x \\
\text{s.t.} \quad & x \in X \\
& x \in Y
\end{aligned}
$$

* **Context:** Finding a solution in $X \cap Y$ directly is computationally difficult. However, optimizing over $X$ alone or $Y$ alone might be easy (e.g., one might represent a shortest-path problem, while the other represents a knapsack problem).

#### **2. Variable Splitting (The "Trick")**
To exploit the fact that $X$ and $Y$ are easy to solve independently, we introduce a copy of the variable $x$, denoted as $y$, and add a linking equality constraint:

$$
\begin{aligned}
\max_{x, y} \quad & c^T x \\
\text{s.t.} \quad & x \in X \\
& y \in Y \\
& x - y = 0 \quad \leftarrow \text{(The Complicating Constraint)}
\end{aligned}
$$

**The Strategy:** The art of Lagrangian Decomposition lies in recognizing how to partition the problem constraints. By artificially separating the decision variables, we can exploit the underlying structure of the problem. We intentionally define the sets $X$ and $Y$ such that they map to independent, well-known, and computationally tractable sub-models. The difficulty of the problem is moved out of the constraints ($X \cap Y$) and shifted into the objective function via a penalty for violating $x = y$.

#### **3. Relaxing the Linking Constraint**
Now, we relax the equality constraint $x - y = 0$ by introducing a vector of Lagrangian multipliers, $\lambda$. Because $x - y = 0$ is an equality constraint, $\lambda$ is unrestricted in sign. We move this constraint into the objective function to penalize any differences between $x$ and $y$:

$$
\begin{aligned}
Z_{LD}(\lambda) = \max_{x, y} \quad & c^T x + \lambda^T (y - x) \\
\text{s.t.} \quad & x \in X, \; y \in Y
\end{aligned}
$$

#### **4. Decomposing into Subproblems**
By regrouping the terms in the objective function ($c^T x - \lambda^T x + \lambda^T y$), the problem beautifully and entirely decomposes into two independent subproblems:

1.  **The $x$-subproblem:** $\max_{x \in X} (c - \lambda)^T x$
2.  **The $y$-subproblem:** $\max_{y \in Y} \lambda^T y$

#### **5. Solving and Theoretical Bounds**
To find the optimal multipliers, we solve the subproblems independently for a fixed $\lambda$. We then update $\lambda$ iteratively—typically using the **subgradient method**, where the subgradient is simply the difference between the solutions of the two subproblems at iteration $k$: 
$$g^k = y^k - x^k$$

We repeat this process until $x$ and $y$ converge (or the duality gap closes). 

**Why use this over standard relaxation?** Lagrangian decomposition frequently provides tighter bounds than standard Lagrangian relaxation. This is because solving the decomposed problem effectively optimizes over the intersection of the convex hulls of $X$ and $Y$:

$$Z_{LD} = \max \{ c^T x : x \in \text{conv}(X) \cap \text{conv}(Y) \}$$

This bound is theoretically stronger than optimizing over $\text{conv}(X \cap Y)$, making it a highly effective method for finding strong upper bounds for complex integer programming problems.

# Summary
Lagrangian methods are incredibly effective for large-scale optimization, specially in unit commitment, facility location, and network routing, by breaking down massive, coupled problems into smaller, independent subproblems that are computationally tractable.
