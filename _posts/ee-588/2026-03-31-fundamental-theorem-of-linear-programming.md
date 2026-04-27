---
layout: distill
title: "The Fundamental Theorem of Linear Programming"
description: "A quick intuition and justification of why linear programming optima occur at extreme points."
date: 2026-03-31
categories: ee-588
tags: optimization linear-programming convex-optimization
project: ee-588
math: true
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Introduction
  - name: Intuition
  - name: Justification
---

# Introduction

At the core of linear optimization lies a foundational principle that dramatically simplifies how we search for optimal solutions.

> **The Fundamental Law of Linear Programming**  
> A linear programming problem involves optimizing a linear objective function $c^\top x$ subject to linear inequality constraints $Ax \le b$ and $x \ge 0$. The optimal solution is always attained at a **corner point** (or *extreme point*) of the feasible region.

A remarkable consequence of this theorem is its implication for non-convex sets:

> **Equivalence on Non-Convex Sets**  
> Minimizing a linear objective over a non-convex set of points yields the **same result** as minimizing it over the **convex hull** of those points, since the optimum always occurs at one of the extreme points.

***

# Intuition

Why do linear functions always push their optima to the boundary, specifically to the corners? We can build this intuition from the ground up:

### 1. One-Dimensional Perspective
Imagine minimizing a straight line $y = c^\top x$ over a closed interval $[a, b]$. Because there is no curvature, the function is either strictly increasing, strictly decreasing, or perfectly flat. Consequently, the minimum value is always found at one of the endpoints.

### 2. Two-Dimensional Perspective
If we move to two dimensions and take a bird's-eye view:

- **The Feasible Region**: This forms a polygon, bounded by flat faces.
- **Contour Sets**: A contour set represents all decision variables yielding the same objective value. Due to linearity, these contours are straight, parallel lines moving in the direction of $c$.
- **The Gradient**: The objective value increases in the direction strictly orthogonal to the contour lines.
- **The Search**: Minimization is geometrically equivalent to sweeping the contour line $y = c^\top x$ across the polygon in the direction opposite to $c$.
- **The Discovery**: Because the polygon possesses sharp vertices and the sweeping line is flat, the line will exit the polygon exactly at a vertex. This first (or last) point of contact identifies the minimum.

<aside>
**In Two Sentences:** Linear functions have no curvature, and the feasible region is built from flat faces. This pushes the optimum all the way out to the boundary, locking it firmly into a corner where constraints intersect.
</aside>

***

# Justification

To rigorously justify why minimizing a linear objective over a non-convex set $S$ is equivalent to minimizing over its convex hull $\operatorname{conv}(S)$, we can rely on established optimization theory.

### Step 1: Definition of the Convex Hull
The convex hull $\operatorname{conv}(S)$ is defined as the smallest convex set that contains all convex combinations of points from the original non-convex set $S$. Crucially, the extreme points of $\operatorname{conv}(S)$ are always drawn from the original set $S$.

### Step 2: Bauer's Maximum Principle
Bauer's Maximum Principle states that a continuous, convex function defined on a compact, convex set will attain its maximum (and since linear functions are both convex and concave, its minimum) at an **extreme point** of that set. 

### Step 3: Synthesis
1. By Bauer's Principle (and the Fundamental Theorem of Linear Programming), any optimal value of a linear objective over $\operatorname{conv}(S)$ must occur at an extreme point of $\operatorname{conv}(S)$.
2. Because the extreme points of $\operatorname{conv}(S)$ belong to the original set $S$, the optimum over the convex hull is actually an element of $S$.
3. Therefore, minimizing a linear objective over $S$ directly, or over arguably the "easier" space $\operatorname{conv}(S)$, yields the exact same optimal value.

### Key References
- **Fundamental Theorem of Linear Programming:** Formally states that LP optima are found at vertices.
- **Bauer's Maximum Principle:** Generalizes this concept, supporting the bounding of non-convex sets.
- **Convex Optimization:** See *Boyd & Vandenberghe (2004)*, Chapters 2 and 4, for formal proofs defining how linear objectives operate over geometric sets.
