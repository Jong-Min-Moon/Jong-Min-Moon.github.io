---
layout: post
title: "EE 588: Convex Sets"
date: 2026-04-25 09:15:00-0700
description: "Foundational concepts of convex sets, including definitions, examples, and operations that preserve convexity."
tags: optimization convex-analysis
categories: ee-588
project: ee-588
---

### Definition
A set $C \subseteq \mathbb{R}^n$ is **convex** if the line segment between any two points in $C$ lies in $C$. Formally, for any $x_1, x_2 \in C$ and any $\theta$ with $0 \leq \theta \leq 1$, we must have:
$$\theta x_1 + (1-\theta) x_2 \in C$$

### Important Examples of Convex Sets

#### 1. Hyperplanes and Halfspaces
- **Hyperplane**: $\{x \mid a^\top x = b\}$
- **Halfspace**: $\{x \mid a^\top x \leq b\}$

#### 2. Euclidean Balls and Ellipsoids
- **Euclidean Ball**: $B(x_c, r) = \{x \mid \|x - x_c\|_2 \leq r\}$
- **Ellipsoid**: $\{x \mid (x - x_c)^\top P^{-1} (x - x_c) \leq 1\}$, where $P = P^\top \succ 0$.

#### 3. Norm Balls
A norm ball $\{x \mid \|x\| \leq r\}$ is convex for any norm $\|\cdot\|$.

#### 4. Polyhedra
A polyhedron is the intersection of finitely many halfspaces and hyperplanes:
$$P = \{x \mid Ax \preceq b, Cx = d\}$$

#### 5. Positive Semidefinite Cone
The set of symmetric positive semidefinite matrices $S^n_+ = \{X \in S^n \mid X \succeq 0\}$ is a convex cone.

### Operations that Preserve Convexity

To establish that a set is convex, one can often show it is obtained from simple convex sets through operations that preserve convexity:

1. **Intersection**: The intersection of any number of convex sets is convex.
2. **Affine Functions**: If $f$ is an affine function ($f(x) = Ax + b$), then:
   - If $S$ is convex, its image $f(S) = \{f(x) \mid x \in S\}$ is convex.
   - If $S$ is convex, its inverse image $f^{-1}(S) = \{x \mid f(x) \in S\}$ is convex.
3. **Perspective Function**: $P(x, t) = x/t$ (for $t > 0$) preserves convexity.
4. **Linear-fractional Functions**: A composition of a perspective function and an affine function.

### Convex Combination and Convex Hull
- **Convex Combination**: $\sum_{i=1}^k \theta_i x_i$ where $\theta_i \geq 0$ and $\sum \theta_i = 1$.
- **Convex Hull**: The set of all convex combinations of points in $S$, denoted $\text{conv}(S)$. It is the smallest convex set that contains $S$.



# Polytope
A polytope is a geometric object with flat sides that exists in any number of dimensions. It is the broad, overarching mathematical term used to describe shapes that are bounded by straight lines or flat planes.You can think of a polytope as the ultimate generalization of shapes you already know, scaled up (or down) into any dimension:0-Dimensional Polytope: A single point.1-Dimensional Polytope: A line segment.2-Dimensional Polytope: A polygon (like a triangle, square, or hexagon).3-Dimensional Polytope: A polyhedron (like a cube, pyramid, or dodecahedron).4-Dimensional Polytope (and higher): Often just called an $n$-polytope (like a hypercube or tesseract in 4D).Two Ways to Define a PolytopeIn mathematics, particularly in geometry and optimization, there are two common ways to define a polytope. They represent the exact same shape, just described differently:1. The V-description (Vertices):A polytope is the "convex hull" of a finite set of points. If you take a handful of points in space and wrap a tight, flat-sided skin around them (like stretching a rubber band around pegs on a board), the enclosed solid shape is a polytope.2. The H-description (Half-spaces):A polytope is the bounded intersection of a finite number of closed half-spaces. Imagine taking a solid block of wood and making several perfectly straight, flat cuts with a saw. The geometric block you have left over is a polytope.Why Does This Matter to You?Given your recent questions about Mixed-Integer Programming (MIP) and optimization, the H-description is incredibly relevant.In linear optimization, every linear constraint you write (e.g., $x_1 + x_2 \le 5$) cuts the mathematical space in half, creating a "half-space." When you combine all your linear constraints, the overlapping region where they are all satisfied is your feasible region.If that feasible region doesn't stretch off into infinity, it is a polytope. When a solver looks for the optimal solution to a standard convex linear program, it is effectively sliding along the flat edges and checking the sharp corners (vertices) of this high-dimensional polytope to find the best answer.

### Optimization
The maxima and minima of a linear function on a polytope occur at the **vertices** (corners), not in the interior or not even along the edges.


# Simplex
