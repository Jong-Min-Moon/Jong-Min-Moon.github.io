---
layout: distill
title: "k-means Clustering"
description: "Formulating and implementing k-means clustering as a mixed-integer optimization problem."
tags: distill machine-learning optimization clustering
categories: ml_mio
date: 2026-03-09
featured: false
project: ml_mio
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
toc:
  - name: "Problem Definition"
  - name: "Mixed-Integer Formulation (k=2)"
  - name: "Questions"
---

## Problem Definition

Suppose that we have $n$ data points $\{\mathbf{x}_i\}_{i=1}^n \subseteq \mathbb{R}^d$ in Euclidean space. We aim to find exact $k$ partitions $S_1, \dots, S_k$ of these $n$ points that minimizes the sum of squared errors (SSE) defined by:

$$
\text{SSE}(S_1, \dots, S_k) := \sum_{l=1}^k \sum_{i \in S_l} \|\mathbf{x}_i - \mu_l\|^2,
$$

where $\mu_l := \frac{1}{|S_l|} \sum_{i \in S_l} \mathbf{x}_i$ is the centroid of cluster $l$. The $k$-means clustering problem can be formulated as:

$$
\begin{align}
\min_{\mu_1, \dots, \mu_k, S_1, \dots, S_k} & \sum_{l=1}^k \sum_{i \in S_l} \|\mathbf{x}_i - \mu_l\|^2 \\
\text{s.t.} & \quad S_1, \dots, S_k \text{ form a partition of } \{1, \dots, n\}, \\
& \quad \mu_1, \dots, \mu_k \in \mathbb{R}^d.
\end{align}
$$

Note that any optimal solution $\mu_1^*, \dots, \mu_k^*, S_1^*, \dots, S_k^*$ satisfies the centroid condition $\mu_l^* = \frac{1}{|S_l^*|} \sum_{i \in S_l^*} \mathbf{x}_i$; therefore, we do not need to explicitly impose this as a constraint.

---

# Mixed-Integer Formulation ($k=2$)

In this problem, we will formulate and implement the $k$-means problem step-by-step for the case where $k = 2$. 

## Variables
We define the following variables to linearize the cluster assignments:

- **Centroids:** $\mu_l \in \mathbb{R}^d$ for $l = 1, 2$ represent cluster centroids.
- **Assignments:** $z \in \{0, 1\}^n$ assigns each point to a cluster:
  $$
  z_i = 
  \begin{cases} 
  0 & \text{if } i \in S_1, \\
  1 & \text{if } i \in S_2.
  \end{cases}
  $$
- **Error Vectors:** $\mathbf{r}_{il} \in \mathbb{R}^d$ for $l = 1, 2$ measures the errors between $\mathbf{x}_i$ and $\mu_l$ only if point $i$ belongs to $S_l$:
  $$
  \mathbf{r}_{i}^l = 
  \begin{cases} 
  \mathbf{x}_i - \mu_l & \text{if } i \in S_l, \\
  0 & \text{otherwise.}
  \end{cases}
  $$
- **Eraser Vectors:** $\mathbf{w}_{il}$ for $l = 1, 2$ are auxiliary variables used to “cancel out” the errors when a point does not belong to a cluster:
  $$
  \mathbf{w}_{i}^l = 
  \begin{cases} 
  0 & \text{if } i \in S_l, \\
  \text{otherwise,} & \mathbf{w}_{i}^l \in \mathbb{R}^d.
  \end{cases}
  $$

## Objective
Because of the definition of $\mathbf{r}_{i}^l$, the objective function is defined as $\sum_{l=1}^2 \sum_{i=1}^n \|\mathbf{r}_{i}^l \|^2$.

## Constraints

### Big-M Formulation for Eraser Vectors

Eraser vectors are constrained using a large constant \(M > 0\):

$$
- M (1 - z_i) \mathbf{1} \le \mathbf{w}_i^1 \le M (1 - z_i) \mathbf{1}, \quad \forall i
$$

$$
- M z_i \mathbf{1} \le \mathbf{w}_i^2 \le M z_i \mathbf{1}, \quad \forall i
$$

**Interpretation:**  

- If point \(i\) is assigned to cluster 1 (\(z_i = 0\)), then \(\mathbf{w}_i^1 = 0\), so the error vector is \(\mathbf{r}_i^1 = \mathbf{x}_i - \mu_1\).  
- If point \(i\) is **not** assigned to cluster 1 (\(z_i = 1\)), \(\mathbf{w}_i^1\) can take any value in \([-M, M]^d\), effectively removing the contribution of \(\mathbf{r}_i^1\) from the objective.  
- The same logic applies to cluster 2 and \(\mathbf{w}_i^2\).

---

### Relationship Between Error and Eraser Vectors

The error vectors are defined as:

$$
\mathbf{r}_i^l = \mathbf{x}_i - \mu_l - \mathbf{w}_i^l, \quad \forall i, l
$$

**Interpretation:**  

If \(\mathbf{w}_i^l\) can be nonzero, the optimizer will set \(\mathbf{w}_i^l = \mathbf{x}_i - \mu_l\) when the point is **not assigned** to cluster \(l\), effectively zeroing out the corresponding error.  

This ensures that errors are counted **only for points actually assigned** to a given cluster.


**Interpretation:**  
- The solver treats the two error vectors as mutually exclusive: if one is nonzero, the other must be zero.  
- This is equivalent to enforcing that a point contributes to exactly **one cluster**’s error, tightening the LP relaxation significantly.



### 3. Implementation
We ran the k-means model using **Gurobi** with a **5-minute time limit**.  

To set up the problem, we carefully chose **Big-M values** based on the spatial distribution of the **Ruspini dataset** and set \(M = 1 \times 10^2\). The Big-M is used to enforce the eraser vectors in the MIQCP formulation.  

---

## Run Results

After 5 minutes, the solver's gap remained large:

| Metric         | Value     |
| -------------- | --------- |
| Best Objective | 1,757,688 |
| Best Bound     | 1,592,261 |
| Gap (%)        | 62.4%     |
| Nodes Explored | 265       |
| Runtime (s)    | 275       |

This indicates that the MIQCP is **still hard to solve exactly**, and we may need to **tighten the formulation** for better convergence.


The solver returned the following centroids:

```python
array([[ 66.32243059, 129.07219318],
       [ 41.92044401,  48.09716577]])
```

to visualize:
```liquid
{% include figure.html path="assets/img/kmeans_out.png" class="img-fluid rounded z-depth-1" %}
```

Visually, the clusters look reasonable, suggesting that the problem may not be infeasible. It is possible that choosing 
$k=2$ clusters is limiting the solver from finding a lower objective.