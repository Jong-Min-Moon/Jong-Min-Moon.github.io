---
layout: distill
title: "Paper Review: Convexification of multi-period quadratic programs with indicators"
description: "A deep dive into the recent paper by Lee, Gómez, and Atamtürk on constructing tight convex relaxations for multi-period quadratic optimization problems with logical indicators."
date: 2026-03-30
categories: ise-617
tags: optimization mixed-integer-programming convexification multi-period
project: ise-617
math: true
paper_key: lee2024convexification
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Preliminaries
  - name: Overview
  - name: The Mathematical Setting
  - name: Core Methodology and Convexification
  - name: Algorithmic Contributions
  - name: Case Studies and Applications
  - name: Conclusion
---


# Preliminaries


## The fundamental law of linear programming
- Linear programming (LP) is the problem of optimizing a linear objective function $c^\top x$ subject to linear inequality constraints $Ax \le b$ and $x \ge 0$. 
- The best LP solution always occurs at a corner (an *extreme point*) of that region. 

### Intuition from one dimension
You’re minimizing a linear function over an interval. The minimum is always at one of the endpoints. 

### Intuition from two dimensions
- Let's go bird's eye view. 
- The feasible set is a polygon.
- Contour set is a set of decision variables with the same objective value.
- Since the objective is linear, the contour set is a flat line with direction $c$. The objective value increases in the direciton orthogonal to the contour line.
- Minimization is equivalent to chekcing every contour line and finding the minimum value. 
- This is equivalent to moving the line $y=c^\top x$ in the direction orthogonal to $c$. 
- Since the polygon has sharp vertices, the minimum value occurs at the first (or last) vertex.

### Two sentences Intuition
Linear functions have no curvature, and the feasible region (a polytope) is built from flat faces, so the optimum can’t hide in the middle. It gets pushed all the way out to the boundary, and specifically to a corner where constraints intersect.


## Problem Formulation
For $\mathbf{Q} \in \mathbb{R}^{n \times n}$, $\mathbf{a} \in \mathbb{R}^n$, $c \in \mathbb{R}^n$, and $\tilde{C} \subseteq \mathbb{R}^{n} \times \mathbb{R}^n$ is a projection of $C$ where $\mathbf{s}$ is marginalized out, we consider the following problem:
<p>
\begin{aligned}
\min_{x, z} \quad & x^\top \mathbf{Q} x + \mathbf{a}^\top x + c^\top z \\
\text{s.t.} \quad & x_i (1 - z_i) = 0, \quad z_i \in \{0,1\}, \quad i \in [n], 
\text{(switch constraints)}
\\
& (x, z) \in \tilde{C} \subseteq \mathbb{R}^{n} \times \mathbb{R}^n \text{(side constraints)}.
\end{aligned}
</p>

## Definition 1: Factorizable matrix
- Definition 1 introduces block-factorizable matrix. This is for multi-dimensional state variables. For scalar state variables, we don't need this complication.
- Let us focus on scalar state variables. A symmetric cost matrix $Q$ is factorizable if
<p>
\begin{equation*}
Q_{ij} = u_i v_j.
\end{equation*}
</p> 

- This means that Q is expresed by $2n$ parameters.

## Proposition 1 & 2

## Proposition 3: 2 by 2 rank-1 decomposition of the cost matrix inverse

### High Level Summary
- The cost matrix $Q$ is massive and complicated.
- However, its inverse $Q^{-1}$ has a very nice structue: it can be decomposed into a sum of $n$ independent, simple rank-one matrices.
- Moreover, each rank-one matrix has a very simple structure: almost everything is zero, except for a 2x2 block.
- Why do we care? Because this breakdown allows us to isolate the exact costs associated with taking specific actions between specific time periods.
- Corollary: principal submatrix of $Q$ can also be similarly decomposed.


## Overview

In the field of operations research, multi-period optimization problems containing both continuous decisions and discrete logical indicators (mixed-integer programs) are notoriously difficult to solve. The paper **"Convexification of Multi-period Quadratic Programs with Indicators" (arXiv:2412.17178)** by *Jisun Lee, Andrés Gómez, and Alper Atamtürk* tackles a vital class of these problems. Exploring convex quadratic costs intertwined with linear dynamics and indicator variables, the researchers propose a robust convexification methodology. 

By strategically deriving closed-form inverses for specific block-factorizable cost matrices, the authors construct a strong convex hull and subsequently provide scalable, polynomial-time algorithms to solve underlying problems. 

---

## The Mathematical Setting

Multi-period problems govern how an optimal action at time $t$ fundamentally rests on actions taken previously, up to time $t-1$. The paper studies dynamic structures where the **state evolves dynamically as an affine function of**:
1. Previous state variables
2. Control decisions
3. Logical indicator (binary) variables in each period

The presence of quadratic costs and binary indicators means that the problem is a **Mixed-Integer Quadratic Program (MIQP)**, which introduces non-convexities that commercial solvers often struggle to branch-and-cut through efficiently, particularly as the number of time periods $n$ increases. 

---

## Core Methodology and Convexification

To overcome the combinatorial explosion natively found in MIQPs, the authors lean on the powerful theory of exact convexification. Their methodology is laid out in a few major steps:

### 1. Projecting Out the State Variables
The first significant step is to project out the explicit state variables. Given that the state unfolds through affine linear dynamics, substituting them through time condenses the problem down to control variables and indicator constraints. 

This results in a new MIQP, but with a highly structured cost matrix: a **block-factorizable** cost matrix.

### 2. Analytical Breakthrough: Closed-Form Inverse
In numerical optimization, dealing with factorizable density usually requires algorithmic factorization (like Cholesky). However, the authors leverage the explicit properties of these multi-period blocks to derive a **closed-form expression for the inverse** of these matrices.

### 3. Constructing the Convex Hull
Using the closed-form inverse formulation, the authors mathematically construct a **closed convex hull representation** of the epigraph describing the quadratic cost over this feasible region, situated in an extended space.

By characterizing the convex hull exactly, the continuous relaxation of this reformulated problem inherently mimics the tightest possible bounds of the original integer problem.

---

## Algorithmic Contributions

Armed with the convex hull formulation, the paper presents two actionable paths for algorithmic implementation:

1. **Second-Order Cone Programming (SOCP)**
   The authors successfully translate their extended convex hull directly into a tight SOCP formulation utilizing $\mathcal{O}(n^2)$ conic constraints. Given that modern solvers (like Gurobi or MOSEK) are exceptionally efficient at crunching SOCPs, bringing the mixed-integer problem down to an exact SOCP relaxation drastically prunes the branch-and-bound tree.

2. **Polynomial-Time Algorithm via Directed Acyclic Graphs (DAG)**
   Even further, for specific structural parameters, the researchers frame the optimization problem as finding the shortest path over a Directed Acyclic Graph (DAG), yielding an elegant polynomial-time algorithm to acquire the global optimal solution.

---

## Case Studies and Applications

The value of robust reformulations lies in real-world application, and the paper details case studies in diverse domains:

* **Statistical Learning**: Problems such as sparse regression or fused lasso variants naturally exhibit quadratic loss functions governed by binary indicators representing feature selection over structured correlations.
* **Hybrid System Control**: In mechanical engineering and robotics, non-linear system dynamics are often modeled as piecewise-affine local systems governed by binary transition indicators (i.e., "If the engine reaches Phase 2, follow Dynamic System B"). Tight convexification dramatically minimizes fuel/energy costs while respecting strict path-planning constraints.

---

## Conclusion

The work of Lee, Gómez, and Atamtürk represents an invaluable advancement in Mixed-Integer Quadratic Programming. By mathematically identifying the structure of multi-period problem cost matrices—and exactly defining their closed-form inverse—the paper offers a theoretical framework that transforms intractable time-series optimization into tight SOCPs and polynomial-time DAG resolutions. It stands as an essential read for researchers dealing with multi-period planning, inventory control, and robust machine learning optimization.

*(You can read the full preprint on arXiv: [2412.17178](https://arxiv.org/abs/2412.17178))*
