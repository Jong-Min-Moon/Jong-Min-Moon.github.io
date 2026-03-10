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

# Problem Description

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

# Formulating as an optimizaiton problem

### Objective
- Intra-cluster distance: For cluster $j$, $\sum_{i=1}^n  d_{ij}x_{ij}$ is the total distance between points assigned to cluster $j$ and the cluster center $j$. We want to minimize sum of these intra-cluster distances over all clusters.
- Instead of fixing the number of clusters, use a data-driven approach by introducing a penalty for opening a facility.  $\lambda \sum_{j=1}^n y_j$  penalized opening too many facilities.
- $\rho z_i$ is the penalty incurred for classifying point $i$ as an outlier.
The problem can be formulated as the following Mixed-Integer Optimization (MIO) problem:

### Constraints

- **i-perspective:** Each point must either be assigned to exactly one cluster or be classified as an outlier. This is expressed as  
  $$
  \sum_{j=1}^{n} x_{ij} + z_i = 1 \quad \forall i,
  $$  
  where $x_{ij} = 1$ if point $i$ is assigned to cluster $j$, and $z_i = 1$ if point $i$ is an outlier.

- **j-perspective:** Each cluster can only accommodate points if it is open, and cannot exceed its capacity $C$. Formally,  
  $$
  \sum_{i=1}^{n} x_{ij} \le C \, y_j \quad \forall j,
  $$  
  where $y_j = 1$ if cluster $j$ is opened.

- **Cluster limit:** The total number of clusters cannot exceed $k$, i.e.,  
  $$
  \sum_{j=1}^{n} y_j \le k.
  $$

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

The choice between these two options is determined by the objective function. Assigning item $i$ to facility $j$ incurs the cost $d_{ij}$, while declaring it an outlier incurs the penalty $\rho$. As a result, the model tends to declare $\mathbf{a}_i$ an outlier and set $z_i = 1$ if
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



# Penalization vs. Constraints

## When outlier penalty is 0
Consider the special case where the outlier penalty is set to $\rho = 0$. In this situation, declaring a point as an outlier incurs no cost in the objective function.

Recall that each point must satisfy

$$
\sum_{j=1}^{n} x_{ij} + z_i = 1.
$$

If $z_i = 1$, the point is treated as an outlier and contributes $\rho z_i = 0$ to the objective.  
If the point is assigned to a cluster center $j$, the model incurs the assignment cost $d_{ij} > 0$.

Since assigning a point always incurs a positive cost while declaring it an outlier costs nothing, the optimizer will always prefer

$$
z_i = 1, \qquad x_{ij} = 0 \quad \forall j.
$$

Consequently, no points are assigned to any cluster. Because opening a facility also incurs a cost $\lambda > 0$, the model will additionally set

$$
y_j = 0 \quad \forall j.
$$

Thus, the optimal solution becomes:

- $z_i = 1$ for all $i$ (all points are labeled as outliers),
- $x_{ij} = 0$ for all $i,j$ (no assignments),
- $y_j = 0$ for all $j$ (no facilities opened).

The resulting objective value is $0$.

This illustrates that the penalty parameter $\rho$ is essential for preventing the trivial solution where every point is classified as an outlier. In practice, $\rho$ must be chosen large enough so that assigning points to clusters becomes preferable to discarding them.

## Replacing the Outlier Penalty with a Hard Constraint

Instead of penalizing outliers in the objective function, we can impose a hard constraint on the maximum number of outliers allowed. Let $q$ denote the maximum number of items that may be classified as outliers. The constraint becomes

$$
\sum_{i=1}^{n} z_i \le q.
$$

In this formulation, the penalty term $\rho \sum_{i=1}^{n} z_i$ is removed from the objective function.

Under this model, the optimizer can declare at most $q$ points as outliers. Since declaring an outlier no longer incurs any penalty, the solver will typically use the outlier budget to exclude points that would otherwise incur large assignment costs $d_{ij}$. The solver does not necessarily use the full outlier budget $q$. Since declaring an outlier does not incur any penalty in this formulation, the solver will mark a point as an outlier only if doing so reduces the objective value by avoiding a large assignment cost $d_{ij}$. If assigning a point to a cluster is relatively inexpensive, the optimizer may prefer to assign it rather than declare it an outlier. Therefore, the constraint $\sum_{i=1}^{n} z_i \le q$ acts only as an upper bound on the number of outliers, and the optimal solution may contain fewer than $q$ outliers.

However, unlike the penalized formulation, the optimizer cannot discard an unlimited number of points. Once the outlier limit $q$ is reached, all remaining points must be assigned to some cluster center.

This change has two important implications:

1. **Different optimization behavior.**  
   In the penalized formulation, the model trades off assignment costs against the penalty $\rho$. In the constrained formulation, the model instead allocates a fixed “budget” of $q$ outliers to the most expensive points.

2. **Potential feasibility issues.**  
   If the capacity constraints and cluster limits are too restrictive, the problem may become infeasible when $q$ is too small. For example, if the total capacity of all allowed clusters cannot accommodate at least $n - q$ points, then no feasible assignment exists.

Thus, the hard-constraint formulation replaces the cost-based trade-off controlled by $\rho$ with a strict limit on the number of outliers.

# Model Strengthening

Formulation (1) can be improved by adding additional valid inequalities involving $x_{ij}$ and $y_j$ to **tighten the linear relaxation**.

## Tightening the Linear Relaxation

In the mixed-integer formulation, the variables satisfy

$$
x_{ij}, y_j, z_i \in \{0,1\}.
$$

During the LP relaxation solved inside branch-and-bound, these constraints are relaxed to

$$
0 \le x_{ij}, y_j, z_i \le 1.
$$

This allows **fractional solutions**, such as

$$
x_{i1} = 0.4, \quad x_{i2} = 0.6,
$$

which do not correspond to valid cluster assignments.

A **stronger formulation** adds valid inequalities that:
- do not remove any feasible integer solutions, but
- eliminate fractional LP solutions.

This leads to a **tighter relaxation** and improves the efficiency of the branch-and-bound algorithm.

---

## Linking Constraints

A standard strengthening constraint for facility location problems is

$$
x_{ij} \le y_j \qquad \forall i,j.
$$

### Interpretation

A point can only be assigned to facility $j$ if that facility is opened.

- If $y_j = 0$, then $x_{ij} = 0$ for all $i$.
- If $x_{ij} = 1$, the facility must be open ($y_j = 1$).

Although the model already includes the capacity constraint

$$
\sum_{i=1}^{n} x_{ij} \le C y_j,
$$

this constraint alone is **weak in the LP relaxation**. For example, the LP may produce

$$
y_j = 0.1, \quad x_{1j} = 0.05, \quad x_{2j} = 0.05,
$$

which represents a facility that is only partially open. Adding the constraints $x_{ij} \le y_j$ prevents such fractional assignments and significantly strengthens the relaxation.

---

## Global Capacity Constraint

Another useful inequality is

$$
\sum_{i=1}^{n}\sum_{j=1}^{n} x_{ij} \le C \sum_{j=1}^{n} y_j.
$$

This constraint states that the **total number of assignments cannot exceed the total available cluster capacity**. Although it is implied by the per-cluster capacity constraints, adding it explicitly often tightens the LP relaxation.

---

## Assignment–Facility Consistency

From the assignment constraint

$$
\sum_{j=1}^{n} x_{ij} + z_i = 1
$$

and the limit on the number of centers

$$
\sum_{j=1}^{n} y_j \le k,
$$

we can add the inequality

$$
\sum_{j=1}^{n} x_{ij} \le \sum_{j=1}^{n} y_j.
$$

This ensures that assignments only occur when facilities are opened and removes certain fractional LP solutions.


## Symmetry Breaking

The formulation also contains **symmetry**. Cluster centers correspond to indices $j=1,\dots,n$, but the labels of clusters are interchangeable. For example, opening centers at points $(3,10,25)$ or $(10,3,25)$ produces identical clusterings, yet the solver treats them as different solutions.

To reduce this redundancy, we can impose an ordering on the facility variables:

$$
y_1 \ge y_2 \ge \dots \ge y_n.
$$

This forces facilities to be opened in index order and eliminates equivalent symmetric solutions. Removing symmetry reduces the size of the search space and can significantly improve computational performance.

## Implementation
With these four tightening constraints, in the same setting as branching priority experiemnt, we have the following astonishing result: 0% gap in 2.5 seconds!

| Priority Order                     | Nodes Explored | Simplex Iterations | Best Objective | Best Bound | Final Gap | Time  |
| :--------------------------------- | :------------- | :----------------- | :------------- | :--------- | :-------- | :---: |
| **$x \to y \to z$** (original)     | 505,167        | 32,202,335         | 4,745.05       | 4,535.15   | **4.42%** | 300s  |
| **$x \to y \to z$** (strengthened) | 1              | 11,146             | 4,745.05       | 4,745.05   | 0.00%     | 2.5s  |