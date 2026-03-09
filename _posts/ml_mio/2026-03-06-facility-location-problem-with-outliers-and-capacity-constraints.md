---
layout: distill
title: "Facility Location Problem with Outliers and Capacity Constraints"
description: "Exploring a variant of the Facility Location Problem incorporating outlier rejection and capacity constraints."
date: 2026-03-06
categories: ml_mio optimization
tags: optimization facility-location mixed-integer-programming
project: ml_mio
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Problem Description
  - name: Mathematical Formulation
  - name: Discussion Questions
---

## Problem Description

Suppose that we have $n$ data points $\{\mathbf{a}_i\}_{i=1}^n \subseteq \mathbb{R}^d$ representing their locations. We aim to select at most $k$ of these locations to serve as cluster centers. Each data point is then either assigned to exactly one center or classified as an outlier. This is modeled using a variant of the Facility Location Problem. Unlike the standard formulation, this version incorporates two specific features:

*   **Outlier Rejection**: Points that are too costly to assign to any center may be excluded from the clusters.
*   **Capacity Constraints**: An upper bound is imposed on the number of points that can be assigned to any single cluster.

### Decision Variables

*   $y_j \in \{0, 1\}$: Cluster center indicator. 1 if point $j$ is selected as a cluster center, 0 otherwise.
*   $x_{ij} \in \{0, 1\}$: Assignment indicator. 1 if point $i$ is assigned to cluster $j$, 0 otherwise.
*   $z_i \in \{0, 1\}$: Outlier indicator. 1 if point $i$ is classified as an outlier, 0 otherwise.

### Parameters

*   $d_{ij} > 0$: The distance between points $i$ and $j$.
*   $\lambda > 0$: The fixed cost of opening a facility.
*   $\rho > 0$: The penalty incurred for classifying a point as an outlier.
*   $C > 0$: The capacity limit, representing the maximum number of points any single cluster can accommodate.
*   $k$: maximum number of clusters.

## Solving the problem using integer programming

### Objective
- Intra-cluster distance: For cluster $j$, $\sum_{i=1}^n  d_{ij}x_{ij}$ is the total distance between points assigned to cluster $j$ and the cluster center $j$. We want to minimize sum of these intra-cluster distances over all clusters.
- Instead of fixing the number of clusters, use a data-driven approach by introducing a penalty for opening a facility.  $\lambda \sum_{j=1}^n y_j$  penalized opening too many facilities.
- $\rho z_i$ is the penalty incurred for classifying point $i$ as an outlier.
The problem can be formulated as the following Mixed-Integer Optimization (MIO) problem:

### Constraints
- i-perspective: ith location is only assigned to exactly one cluster center: $\sum_{j=1}^n x_{ij} = 1$. WE make a twist of being classified as outlier and being un-assigned: $\sum_{j=1}^n x_{ij} + z_i= 1$. So either assigned to a cluster, or labeled as an outlier.
- j-perspecice: when y_j =1, we have for cluster id j, it can handle up to C locations. when y_j = 0, no location can be assigned to cluster id j. Thus $\sum_{i=1}^n x_{ij} \le C y_j$.
- We set the maximum number of clusers . $\sum_{j=1}^n y_j \le k $

### Optimization problem
Combining these together, we have linear objective and linear constraint, so an binary integer program:
$$
\begin{align}
\min_{x,y,z} \quad &
\sum_{j=1}^n \left( \sum_{i=1}^n  d_{ij}x_{ij} \right) + \lambda \sum_{j=1}^n y_j + \rho \sum_{i=1}^n z_i \\
\text{s.t.} \quad & \sum_{j=1}^n x_{ij} + z_i = 1, \quad i=1, \dots, n \\
& \sum_{i=1}^n x_{ij} \le C y_j, \quad j=1, \dots, n \\
& \sum_{j=1}^n y_j \le k \\
& x \in \{0,1\}^{n \times n}, y \in \{0,1\}^n, z \in \{0,1\}^n
\end{align}
$$


# Outlier detection mechanism

The variables $z_i$ allow the model to detect and handle outliers by providing the option to exclude certain items from assignment at a penalty cost. This mechanism creates a trade-off between the assignment cost $d_{ij}$ and the penalty $\rho$ in the objective function.

From the constraint

$$
\sum_{j=1}^{n} x_{ij} + z_i = 1 \quad \forall i,
$$

each item $i$ must satisfy exactly one of the following two cases:

1. **Assigned to a facility.** If $z_i = 0$, then
$
\sum_{j=1}^{n} x_{ij} = 1
$ (one of $x_{ij}$ is turned on).
This means that item $i$ is assigned to exactly one facility $j$, and the model incurs the assignment cost $d_{ij}$.

2. **Declared an outlier.**
If $z_i = 1$, then
$
\sum_{j=1}^{n} x_{ij} = 0.
$
In this case, item $i$ is not assigned to any facility, and the model instead pays the fixed penalty $\rho$.

The choice between these two options is determined by the objective function. Assigning item $i$ to facility $j$ incurs the cost $d_{ij}$, while declaring it an outlier incurs the penalty $\rho$. As a result, the model will declare $\mathbf{a}_i$ an outlier and set $z_i = 1$ if
$$
\min_j d_{ij} > \rho.
$$
Otherwise, it may be cheaper to assign item $i$ to a facility.

In this way, the variables $z_i$ act as outlier indicators, allowing the model to avoid assigning items which is too far away from other items, where 'too far' is defined by $\rho$.



#  Branching Priority
In Mixed-Integer Optimization (MIO), the order in which the solver branches on variables can significantly impact the speed and efficiency of the Branch-and-Bound algorithm. We conducted a comparative study on the capacitated facility location problem with outliers, testing three different branching priority configurations for variables $x$ (assignments), $y$ (centers), and $z$ (outliers).

## Experimental Setup
To isolate the effect of branching priorities, the following solver configuration was used:
* **Time Limit:** 300 seconds (5 minutes).
* **Solver Constraints:** Gurobi cutting planes were deactivated to focus purely on the branching performance.
* **Hyperparameters:** $k=4$, $\lambda=100$, $\rho=20$, and $C=60$.

Then  we investigate  the solver’s progress (e.g., gap closure, nodes explored, solution time, etc).

##  Results



| Priority Order      | Nodes Explored | Simplex Iterations | Best Objective | Best Bound | Final Gap |
| :------------------ | :------------- | :----------------- | :------------- | :--------- | :-------- |
| **$x \to y \to z$** | 505,167        | 32,202,335         | 4,745.05       | 4,535.15   | **4.42%** |
| **$y \to z \to x$** | **770,975**    | 21,942,767         | 4,745.05       | 4,441.92   | 6.39%     |
| **$z \to y \to x$** | 436,648        | 30,263,949         | 4,745.05       | 4,448.20   | 6.26%     |

---

## Key Observations and Performance Analysis

####  Gap Closure and Solution Quality
While all three configurations reached the same "Best Objective" (4,745.05), the **$x \to y \to z$** priority achieved the **lowest optimality gap (4.42%)**. This suggests that in this specific model, branching on assignment variables ($x$) helps the solver improve the lower bound (Best Bound) more effectively than prioritizing the facility location variables ($y$).

##  Throughput vs. Efficiency
* **Highest Throughput:** The **$y \to z \to x$** configuration explored the most nodes (~771k). However, it resulted in the largest gap (6.39%). This indicates that while the solver moved quickly through the tree, the branches created by $y$ variables were less "informative" for pruning the search space.
* **Search Depth:** The **$z \to y \to x$** configuration explored the fewest nodes, suggesting that branching on outlier indicators leads to more complex subproblems (higher simplex iterations per node) without a proportional benefit in bound improvement.

## Solution Discovery
The **$y \to z \to x$** priority was the most prolific in finding feasible solutions (10 solutions found), whereas the other configurations found only one. If the goal of a project is to find *any* high-quality feasible solution quickly (incumbent discovery), prioritizing $y$ (the strategic "center" decisions) is the superior choice.


##  Conclusion
For this Capacitated Facility Location problem:
1. **To minimize the optimality gap:** Prioritize **$x$ (Assignment variables)**. Fixing these variables early seems to provide tighter relaxations.
2. **To find more feasible solutions:** Prioritize **$y$ (Center variables)**. Decisions regarding which facilities to open fundamentally shift the model structure, allowing the solver to find multiple valid configurations rapidly.
3. 



### 3. Penalization vs. Constraints
What happens to the optimal solution if you set $\rho = 0$? Furthermore, can the outlier penalty term in the objective be replaced by a hard constraint on the number of outliers allowed? Briefly explain your reasoning and discuss how this change might affect the feasibility of the problem.

### 4. Model Strengthening
Formulation (1) can be improved by adding a class of inequalities involving $x_{ij}$ and $y_j$ to “tighten” the linear relaxation.

*   What specific constraints would you suggest adding?
*   For a fixed combination of parameters, compare and report the (i) total solution time and (ii) the objective value of the root relaxation with and without these additional constraints.
