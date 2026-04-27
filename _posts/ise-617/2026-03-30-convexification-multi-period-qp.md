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
  - name: Overview
  - name: The Mathematical Setting
  - name: Core Methodology and Convexification
  - name: Algorithmic Contributions
  - name: Case Studies and Applications
  - name: Conclusion
---



# Section 1: Problem Formulation
Given a number of periods $$n \in \mathbb{Z}_+$$, a vector $$c \in \mathbb{R}^n$$, and sequences of scalars $$\{r_i\}_{i=1}^{n+1}$$, $$\{f_i\}_{i=1}^n$$, $$\{b_i\}_{i=0}^n$$, $$\{P_i\}_{i=1}^{n+1}$$, and $$\{A_i\}_{i=1}^n$$ with $$r_i, f_i, b_i \in \mathbb{R}$$, $$A_i \neq 0$$, and $$P_i > 0$$, we consider a mixed-integer quadratic optimization problem (MIQP) of the form:

<p>
\begin{aligned}
\min_{s,x,z} \quad & \sum_{i=1}^{n+1} P_i(s_i - r_i)^2 + \sum_{i=1}^{n} f_i x_i + \sum_{i=1}^{n} c_i z_i \\
\text{s.t.} \quad & s_1 = b_0 \\
& s_{i+1} = A_i s_i + x_i + b_i, \quad i \in [n] \\
& x_i(1 - z_i) = 0, \quad z_i \in \{0, 1\}, \quad i \in [n] \\
& (s, x, z) \in C \subseteq \mathbb{R}^{n+1} \times \mathbb{R}^n \times \mathbb{R}^n
\end{aligned}
</p>

where $x \in \mathbb{R}^n$ is a vector whose $i$-th element corresponds to $x_i$ in period $i$.

* In each period, the system evolves according to the affine dynamics (1c): state $s_{i+1}$ depends on the previous state $s_i$ and a decision-maker's input $x_i$.
* Taking action $x_i$ incurs a variable cost $f_i x_i$ and a fixed cost $c_i$, modeled via the indicator constraint (1d) where $x_i \neq 0 \implies z_i = 1$.
* The convex quadratic objective terms penalize deviations between the state $s_i$ and a target $r_i$, while constraints (1e) encode any additional physical or logical system boundaries.

# Section 2

## Problem Reformulation
- State variables $s_i$, $i \in [n]$, in problem (1), can be projected out using the initial state condition (1b) and linear dynamics constraints (1c).  
- The resulting problem is described as follows.
Let $\mathbf{Q} \in \mathbb{R}^{n \times n}$, $\mathbf{a} \in \mathbb{R}^n$, $c \in \mathbb{R}^n$, and $\tilde{C} \subseteq \mathbb{R}^{n} \times \mathbb{R}^n$ be the projection of $C$ after the state variables $s$ are projected out. 

<p>
$$\begin{aligned}
\min_{x, z} \quad & x^\top \mathbf{Q} x + \mathbf{a}^\top x + c^\top z \\
\text{s.t.} \quad & x_i (1 - z_i) = 0, \quad z_i \in \{0,1\}, \quad i \in [n] \quad \text{(indicator constraints)} \\
& (x, z) \in \tilde{C} \subseteq \mathbb{R}^{n} \times \mathbb{R}^n \quad \text{(side constraints)}
\end{aligned}$$
</p>

* The indicator constraints dictate that if $z_i = 0$, then $x_i = 0$. If $z_i = 1$, $x_i$ is a free continuous variable in $\mathbb{R}$.

## Definition 1: Factorizable Matrix
* Reformulated problem is still hard to solve. However, sometimes the nature of the problem puts structure on $Q$ and it makes the problem easier. 
* We focus on factorizability of $Q$.
* While Definition 1 introduces block-factorizable matrices for multi-dimensional states, we focus here on scalar state variables.
* For scalar state variables, a symmetric positive definite cost matrix $Q$ is **factorizable** if:

<p>
$$Q_{ij} = u_i v_j$$
</p> 

* This structural property means $Q$ is fully defined by just $2n$ parameters.

## Propositions 1 & 2: Convex Hull of the Epigraph
- Recall the epigraph reformulation of the optimization problem, for example, page 134 of Boyd & Vandenberghe.
- We replace the objective function with new variable $\tau$, and move the problem into the graph space: the constraint becomes the epigraph constraint $\tau \ge x^\top Q x$ s.t. $x_i(1-z_i)=0, z_i \in \{0,1\}$.
- The objective becomes a linear function. Now, minimum over the epigraph constraint set is equivalent to the minimum over the closed convex hull of the epigraph constraint set.
- SO the strategy is to 1) find the closed convex hull of the epigraph constraint set and 2) solve the convex problem.
- Temporarily setting aside the side constraints $\tilde{C}$, we focus strictly on the quadratic objective and indicator constraints.
- We form the mixed-integer epigraph of the quadratic cost:

<p>
$$X_Q := \left\{ (x, z, \tau) \in \mathbb{R}^n \times \{0,1\}^n \times \mathbb{R}_+ \;:\; \tau \ge x^\top Q x,\; x_i (1 - z_i) = 0,\; i \in [n] \right\}$$
</p>

* Due to the binary variables, $X_Q$ is a non-convex, fragmented space. 
* Proposition 1 states its closed convex hull can be perfectly described by introducing a new matrix $\mathbf{W} \in \mathbb{R}^{n \times n}$ governed by two conditions:


### 1. The PSD Constraint
<p>
$$\exists\, W \in \mathbb{R}^{n \times n} \text{ such that } \begin{pmatrix} W & x \\ x^\top & \tau \end{pmatrix} \succeq 0$$
</p>
This Schur complement constraint forces the feasible region into a smooth, upward-facing bowl, smoothly tying together the total cost ($\tau$), the spike magnitudes ($x$), and $W$.

## 2. The Polyhedral Set of Inverses
The matrix $W$ must belong to a specific polyhedral set $P_Q$, defined by the convex hull of the inverses of all principal submatrices of $Q$:
<p>
$$P_Q = \operatorname{conv}\left\{ (e_S,\; \hat{Q}^{-1}_S) \;:\; S \subseteq [n]\right\}$$
</p>
where $e_S$ is the indicator vector of $S$, and $\hat{Q}^{-1}_S$ is the principal submatrix of $Q^{-1}$ indexed by the active spike periods in $S$.

### Combining the Pieces
The complete convex hull of $X_Q$ is formulated as:
<p>
$$\operatorname{cl}\,\operatorname{conv}(X_Q) = \left\{ (x, z, \tau) \in \mathbb{R}^{2n+1} \;:\; \exists\, W \in \mathbb{R}^{n \times n} \text{ such that } \begin{pmatrix} W & x \\ x^\top & \tau \end{pmatrix} \succeq 0,\; (z, W) \in P_Q \right\}$$
</p>

*(Note: Proposition 2 extends this exact logic to block-factorizable matrices for multi-dimensional cases).*


# Section 3: Convexification
* While Proposition 1 provides the theoretical convex hull, constructing $P_Q$ requires computing $2^n$ matrix inverses (one for every possible combination of spikes), which is computationally intractable.
* To resolve this, we exploit the **factorizable** structure of $Q$.
    * **Proposition 3:** The inverses of $Q$ and its submatrices $Q_S$ decompose into a sum of $n$ simple rank-one matrices.
    * **Section 3.1 & 3.2:** Leveraging this, only $\mathcal{O}(n^2)$ matrices are needed to compute all possible $Q_S^{-1}$. 
* This allows the impossible polyhedron $P_Q$ to be perfectly modeled using basic network flow algebra and a shortest-path algorithm.

## Proposition 3 and Remark 1: $2 \times 2$ Rank-1 Decomposition
* If $Q$ is factorizable, $Q^{-1}$ decomposes into a sum of $n$ independent rank-one matrices.
* Crucially, the non-zero footprint of each rank-one matrix is strictly a $2 \times 2$ block, isolating the exact costs of jumping between specific, consecutive active time periods.
* **Remark 1:** This decomposition holds true for any principal submatrix $Q_S$.

## Corollary 1, Example 2, Definition 2, and Observation 1
These results prove that the system's dynamics are entirely localized. 

### Corollary 1
* For an active subset $S$ of size $k$, $Q_S^{-1}$ is the sum of $k$ rank-one $2 \times 2$ matrices.
* Computing the $\ell$-th component matrix strictly requires data from two consecutive active periods ($\ell$ and $\ell+1$) and ignores all other elements in $S$.

### Example 2
* Using a $5 \times 5$ matrix $Q$, suppose $S = \{1, 2, 4, 5\}$ (period 3 is inactive). 
* $Q_S^{-1}$ and $Q^{-1}$ share the exact same $2 \times 2$ rank-one building blocks, *except* for the bridge connecting the indices adjacent to the missing period (the jump from 2 to 4).

### Definition 2 & Observation 1
* **Definition 2** formalizes these "bridges" as link matrices $\Lambda_{i \to j}$, defining the cost to jump between consecutive active indices ($i < j$) or from an index to the end ($i \to n+1$).
* **Observation 1:** Only $\binom{n+1}{2}$ of these link matrices need to be pre-calculated to construct $Q_S^{-1}$ for *any* possible subset $S \subseteq [n]$.

## Propositions 4, 5, and Theorem 6
* **Propositions 4 & 5** map these link matrices to a Directed Acyclic Graph. They prove that $P_Q$ can be perfectly described using $\mathcal{O}(n^2)$ continuous path variables ($w$), and that the vertices of this network flow formulation are naturally integral.

<p>
$$P_Q = \left\{ (z, W) \in \mathbb{R}^{n + n^2} \;:\; \exists\, w \in \mathbb{R}^{\frac{(n+1)(n+2)}{2}} \text{ such that (14) holds} \right\}$$
</p>

* **Theorem 6** yields the final, compact, and tractable representation of the convex hull:

<p>
$$\operatorname{cl}\,\operatorname{conv}(X_Q) = \left\{ (x, z, \tau) \in \mathbb{R}^{2n+1} \;:\; \exists\, W \in \mathbb{R}^{n \times n},\; w \in \mathbb{R}^{\frac{(n+1)(n+2)}{2}}_{+} \text{ such that } \begin{pmatrix} W & x \\ x^\top & \tau \end{pmatrix} \succeq 0 \text{ and (14) holds} \right\}$$
</p>

# Section 4: Algorithms

## Without Side Constraints: Shortest Path Problem (SPP)
If the side constraints $\tilde{C}$ are empty, the convex hull formulation guarantees integral extreme points. We can project out $x$ and $W$ to solve the problem directly:

<p>
$$\begin{aligned}
\min_{x, z, \tau} \quad & \tau + a^\top x + c^\top z \\
\text{s.t.} \quad & (x, z, \tau) \in \operatorname{cl}\,\operatorname{conv}(X_Q)
\end{aligned}$$
</p>

**Proposition 9** shows this reduces to solving a shortest path problem on a directed acyclic graph $G=(V,A)$ in $\mathcal{O}(n^2)$ time:
<p>
$$V = \{0, \ldots, n+1\}, \quad A = \{(i,j) : 0 \le i < j \le n+1\}$$
</p>
with arc costs $\ell_{ij}$ given by:
<p>
$$\ell_{ij} = \begin{cases} 0, & i = 0,\; 1 \le j \le n+1, \\[6pt] c_i - \dfrac{1}{4} a^\top \Lambda_{[i \to j]} a, & 1 \le i < j \le n+1. \end{cases}$$
</p>

**Corollary 3** translates this back to the original scalar notation for $Q$:
<p>
$$\ell_{ij} = \begin{cases} 0, & i = 0, \; 1 \le j \le n+1, \\[2mm] c_i - \dfrac{\left( u_j a_i - u_i a_j \right)^2}{4 u_i \left( u_j v_i - u_i v_j \right)}, & 1 \le i < j \le n, \\[1mm] c_i - \dfrac{a_i^2}{4 u_i v_i}, & 1 \le i \le n, \; j = n+1. \end{cases}$$
</p>

## With Side Constraints: SOCP
**Proposition 10 and Corollary 4** state that when side constraints ($\tilde{C}$) are present, the shortest path algorithm cannot be used directly. Instead, the PSD matrix $W$ is decomposed, allowing the convex hull to be formatted as a tight Second-Order Cone Program (SOCP). This preserves the convex geometry while seamlessly integrating the real-world side constraints.


# Case study 1: Deconvolution of calcium imaging data

This paper models the generative process of calcium concentration using an **AR(1) model**, which expresses the observed fluorescence trace $r_i$ as a noisy version of the unobserved calcium concentration $s_i$. 

In this model, the calcium concentration $s_i$ decays exponentially over time until a spike $x_i$ occurs, instantaneously increasing the concentration. With a decay rate $\alpha \in (0, 1)$ and Gaussian noise $\epsilon_i \overset{i.i.d.}{\sim} N(0, \sigma^2)$, $i \in [n]$, the generative model is expressed by:

<p>
\begin{align}\label{generative_model}
r_i &= \rho_0 + \rho_1 s_i + \epsilon_i, \quad i \in [n + 1] \\
s_{i+1} &= \alpha s_i + x_i, \quad i \in [n]
\end{align}
</p>

where $x_i \geq 0, i \in [n]$. As the spike detection is scale-invariant, we assume $\rho_1 = 1$, and $\rho_0$ can be set to $0$ with a minor modification. Then, the calcium concentration can be estimated by solving the following optimization problem:

<p>
\begin{align*}
\min \quad & \frac{1}{2} \sum_{i=1}^{n+1} (s_i - r_i)^2 + \lambda \sum_{i=1}^{n} z_i \\    
\text{s.t.} \quad & x_i = s_{i+1} - \alpha s_i \geq 0, \quad i \in [n] \\
& x_i (1 - z_i) = 0, \quad i \in [n] \\
& z_i \in \{0, 1\}, \quad i \in [n]
\end{align*}
</p>

### Synthetic Data Generation
This paper do not use real data. It only uses synthetic data, generated using the model $\eqref{generative_model}$, where $x_i$ is i.i.d. drawn from Poisson($\mu$).  We randomly generate ten instances for each combination of ($n, \mu, \sigma$), where $n \in \{50, 100, 150, 200, 250, 300\}$, $\mu \in \{0.01, 0.02, 0.03, 0.04, 0.05\}$ and $\sigma \in \{0.05, 0.1, 0.15, 0.2, 0.25\}$.






# TBD 1
To truly grasp the Linear Matrix Inequality (LMI) used here, it helps to see it not just as a block of algebra, but as a clever geometric "trick." 

The specific LMI we are looking at is:
$$
\begin{bmatrix} \mathbf{W} & \mathbf{x} \\ \mathbf{x}^\top & \tau \end{bmatrix} \succeq 0
$$

Here is the step-by-step breakdown of exactly what this matrix inequality is doing, why it is necessary, and how it connects to your original problem.

### 1. The Core Problem: Quadratic "Bowls"
In your original problem, you had the constraint:
$$\tau \ge \mathbf{x}^\top \mathbf{Q} \mathbf{x}$$

The term $\mathbf{x}^\top \mathbf{Q} \mathbf{x}$ forms a curved, multidimensional "bowl" (a parabola). Optimization solvers that handle mixed-integer problems (like your binary $\mathbf{z}$ variables) **hate** curves. They are designed to slide along flat planes and straight edges. We need a way to represent this curved bowl using only flat, linear math.

### 2. The Trace Trick (Lifting)
By the rules of linear algebra, a quadratic form can be rewritten using the **Trace** operator (the sum of the diagonal elements of a matrix):
$$\mathbf{x}^\top \mathbf{Q} \mathbf{x} = \text{Tr}(\mathbf{Q} \mathbf{x} \mathbf{x}^\top)$$

Notice the term $\mathbf{x} \mathbf{x}^\top$. This is an $n \times n$ matrix created by multiplying the vector $\mathbf{x}$ by itself. 

Because we want to get rid of the $\mathbf{x}$ multiplying by $\mathbf{x}$ (which creates the curve), we **invent a brand new matrix variable** and call it $\mathbf{W}$. We want $\mathbf{W}$ to perfectly replace $\mathbf{x} \mathbf{x}^\top$. If we do this, our objective/constraints become beautifully linear: we just multiply the constants in $\mathbf{Q}$ by the variables in $\mathbf{W}$.

### 3. The Rank Problem
Here is the catch: if we strictly demand that $\mathbf{W} = \mathbf{x} \mathbf{x}^\top$, we haven't actually made the problem easier. The constraint $\mathbf{W} = \mathbf{x} \mathbf{x}^\top$ forces $\mathbf{W}$ to be a "Rank-1" matrix. 

In mathematics, a Rank-1 constraint is highly non-convex. It is like taking a solid block of clay and demanding that the solver only look at the exact outer surface of one sharp edge. It shatters convexity.

### 4. The LMI Relaxation (The "Shrink Wrap")
Because we cannot demand exactly $\mathbf{W} = \mathbf{x} \mathbf{x}^\top$, we **relax** the problem. Instead of forcing them to be exactly equal, we demand that $\mathbf{W}$ is *greater than or equal to* $\mathbf{x} \mathbf{x}^\top$ in a matrix sense. 

In matrix math, "greater than or equal to" means the difference between them is a **Positive Semidefinite** matrix:
$$\mathbf{W} - \frac{1}{\tau} \mathbf{x} \mathbf{x}^\top \succeq 0$$
*(Note: the $\tau$ is included here to bound the specific geometry of your epigraph formulation).*

This relaxation is exactly what creates the "convex hull" or the "shrink wrap" around the problem. It turns the hollow, impossible-to-solve Rank-1 shell into a solid, convex shape that solvers can easily navigate.

### 5. The Schur Complement
So, how do we get from $\mathbf{W} - \frac{1}{\tau} \mathbf{x} \mathbf{x}^\top \succeq 0$ to the final LMI? We use a famous theorem in linear algebra called the **Schur Complement**. 

The Schur Complement theorem states that for any matrices $\mathbf{A}, \mathbf{B}, \mathbf{C}$, the non-linear matrix inequality:
$$\mathbf{A} - \mathbf{B} \mathbf{C}^{-1} \mathbf{B}^\top \succeq 0$$
is mathematically **100% equivalent** to the much simpler, linear block matrix:
$$\begin{bmatrix} \mathbf{A} & \mathbf{B} \\ \mathbf{B}^\top & \mathbf{C} \end{bmatrix} \succeq 0$$

If we map our variables to this theorem ($\mathbf{A} = \mathbf{W}$, $\mathbf{B} = \mathbf{x}$, and $\mathbf{C} = \tau$), we instantly get your LMI:
$$
\begin{bmatrix} \mathbf{W} & \mathbf{x} \\ \mathbf{x}^\top & \tau \end{bmatrix} \succeq 0
$$

### Summary
The LMI is a mathematical translation. It takes the difficult, non-convex quadratic curve $\tau \ge \mathbf{x}^\top \mathbf{Q} \mathbf{x}$, pulls it into a higher dimension using a surrogate matrix $\mathbf{W}$, and uses the Schur Complement to write it as a perfectly flat, convex Positive Semidefinite block. This allows the algorithm to solve your spike-train inference problem exactly and efficiently.

# TBD 2
This is a fantastic and highly insightful question. You have spotted the exact conceptual leap that makes these proofs tricky to read. 

If the feasible region is formed by an intersection of an LMI (a giant, curved convex cone) and a polytope (flat planes with sharp corners), why does proving that *only the flat part* has integer corners guarantee that the solution to the *entire* problem is an integer?

Here is why Proposition 5 is the final nail in the coffin that guarantees a tight relaxation, broken down into three logical steps.

### 1. The "Division of Labor" in the Variables
In this extended formulation, the math divides the variables into two distinct groups that are handled by two distinct geometries:

* **The Continuous "Bowl" (The LMI):** The LMI $\begin{bmatrix} \mathbf{W} & \mathbf{x} \\ \mathbf{x}^\top & \tau \end{bmatrix} \succeq 0$ strictly governs the continuous variables. Its only job is to describe the smooth, quadratic relationship between $\mathbf{x}$, $\mathbf{W}$, and the epigraph variable $\tau$. **Notice what is missing from the LMI: $\mathbf{z}$ and $\mathbf{w}$.** The LMI contains absolutely no constraints on the integer variables. 
* **The Discrete "Walls" (The Polytope):** The polytope defined by (14) governs the logic of the spike train. It dictates the rules for $\mathbf{z}$ (when a spike happens) and $\mathbf{w}$ (the lifted variables representing combinations of spikes). 

Because the LMI doesn't constrain $\mathbf{z}$ at all, the geometric boundaries—the "walls" and "corners"—in the $\mathbf{z}$-dimension of this mathematical space are **entirely defined by the polytope**. 

### 2. Linear Objectives Seek Extreme Points
Look at the objective function of the relaxed problem: 
$$\min \quad \tau + \mathbf{a}^\top \mathbf{x} + \lambda \sum_{i=1}^n z_i$$

Notice that this objective function is **perfectly linear**. There are no squares or curves in the objective itself; all the curvature was pushed into the LMI constraint.

A fundamental rule of optimization is that when you minimize a linear objective function over a closed convex set, the optimal solution will always lie on the boundary of that set, and specifically at an **extreme point** (a vertex/corner). 

### 3. Why Proposition 5 Seals the Deal
The optimization solver is trying to push the value of $\mathbf{z}$ down as far as possible because of the penalty $\lambda \sum z_i$. 

As the solver pushes $\mathbf{z}$ down, it slides along the smooth surface of the LMI until it slams into the "walls" created by the polytope constraints (14). Because the objective is linear, the solver won't stop in the middle of a flat wall; it will slide all the way into the sharpest corner (the extreme point) of the $\mathbf{z}$-space to find the absolute minimum cost.

This is exactly what Proposition 5 proves: **Every single corner (extreme point) of the polytope (14) happens to be a perfect integer in $\mathbf{z}$.**

### Summary
Even though the overall shape is partially curved due to the LMI, the curvature only exists in the $\mathbf{x}$, $\mathbf{W}$, and $\tau$ directions. In the $\mathbf{z}$ direction, the shape is a flat-sided polytope. Because the linear objective forces the solver into the corners of this polytope, and Proposition 5 guarantees all those corners are integers, the solver is mathematically forced to hand you a solution where $\mathbf{z} \in \{0,1\}$, making the continuous relaxation perfectly **tight**.


# TBD 3
Yes, they are! You have hit on the exact reason why finding the closed convex hull is the "holy grail" of optimization. 

Because the binary variables $\mathbf{z}^*$ are guaranteed to be integers at the optimum, the continuous variables $\mathbf{x}^*$ and the epigraph variable $\tau^*$ **automatically collapse back into the exact, globally optimal solutions for the original non-convex problem.**

Here is the step-by-step mechanical breakdown of why finding an integer $\mathbf{z}$ mathematically forces $\mathbf{x}$ and $\tau$ to be correct.

### 1. The Collapse of the Continuous Boundaries (Handling $\mathbf{x}$)
In the original problem, the relationship between $\mathbf{x}$ and $\mathbf{z}$ was the non-linear logic switch: $x_i(1 - z_i) = 0$. 

To build the convex hull (the polytope part), the authors had to replace that logic switch with continuous linear inequalities (often called perspective or big-M relaxations). For example, bounding $x_i$ so that as $z_i$ shrinks toward $0$, $x_i$ is forced to shrink too. 

However, once Proposition 5 guarantees that the optimal $z_i^*$ lands exactly on $0$ or $1$, those continuous relaxed inequalities instantly "snap" back into their strict logical forms:
* If the solver chooses $z_i^* = 0$, the polytope boundaries immediately clamp down and force $x_i^* = 0$.
* If the solver chooses $z_i^* = 1$, the boundaries open up, allowing $x_i^*$ to freely take whatever continuous value perfectly minimizes the quadratic bowl.

Because $\mathbf{z}^*$ is integral, $\mathbf{x}^*$ is perfectly valid under the original rules.

### 2. The Tightness of the Epigraph (Handling $\tau$)
Remember that we relaxed the exact quadratic equation into an inequality using the LMI: $\tau \ge \mathbf{x}^\top \mathbf{Q} \mathbf{x}$. 

Because the objective function ($\min \tau + \dots$) constantly pushes $\tau$ downward, the only thing stopping $\tau$ from dropping to negative infinity is that LMI boundary. The solver will always push $\tau$ until it hits the floor. 

When $\mathbf{z}$ is fractional (in a bad relaxation), the "floor" of the LMI might be artificially lower than the true quadratic bowl, resulting in a $\tau$ that is "cheating." But because we are operating on the exact closed convex hull, and $\mathbf{z}^*$ is integral, the "floor" of the relaxation at that specific integer point touches the original quadratic bowl perfectly. Therefore, the solver naturally stops pushing exactly where $\tau^* = (\mathbf{x}^*)^\top \mathbf{Q} \mathbf{x}^*$.

### The Fundamental Theorem of Relaxations
There is a foundational rule in optimization that governs this exact scenario:

> **If you solve a relaxed version of a problem, and the optimal solution happens to be perfectly feasible in the original unrelaxed problem, then it is the guaranteed global optimum of the original problem.**

Because solving over $\text{cl conv}(X_Q)$ gives you a strictly binary $\mathbf{z}^*$, the point $(\mathbf{x}^*, \mathbf{z}^*, \tau^*)$ is $100\%$ feasible in your original, non-convex $X_Q$. Therefore, the continuous $\mathbf{x}^*$ you get out of the solver is the exact physiological spike amplitude you are looking for, and $\tau^*$ is the exact quadratic loss.