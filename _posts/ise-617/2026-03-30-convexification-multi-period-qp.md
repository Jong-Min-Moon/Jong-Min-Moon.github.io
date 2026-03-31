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


