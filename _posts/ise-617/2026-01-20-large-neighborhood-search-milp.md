---
layout: distill
title: "Large Neighborhood Search (LNS) for Mixed-Integer Linear Programming (MILP)"
description: "An overview of Large Neighborhood Search (LNS) heuristics for solving complex Mixed-Integer Linear Programs (MILP), exploring core concepts, 'destroy and repair' methods, and popular frameworks like RINS and Local Branching."
date: 2026-01-20
categories: ise-617
tags: optimization milp heuristics large-neighborhood-search
project: ise-617
---
Large Neighborhood search is a heuristic algorithm for solving large-scale optimization problems.  It is a combination of local search and CP/MIP (constraint programming / mixed-integer programming).


# Intuition from Combination of CP and Local Search
Find a feasible solution using constraint programming

Then Repeat:
1. Select a large neighborhood of the current solution
2. Find an optimal solution in the neighborhood using constraint programming
 
 This works because:
 1. CP is good for finding feasible solutions.
 2. CP is good at optimizing small combinatorial spaces.

The algorithm is almost technology independent: MIP can replace CP here.
### How to define a neighborhood?
The neiborhood can be defined as follows: (there are many options)
- given a feasible point, fix a subset of variables. 
- Let the other variable free.
- In other words, neighborhood is the set of all feasible solutions that agree with the fixed variables.
- Which variable to choose is problem-specific. We have to exploit the problem structure such as spatial or temporal structure. But sometimes just random neighborhood is good enough.

## Introduction to MILP and Computational Challenges

Mixed-Integer Linear Programming (MILP) is a powerful mathematical framework used to model and solve complex optimization problems across operations research, supply chain management, scheduling, and engineering. While modern commercial solvers (such as Gurobi, CPLEX, and FICO Xpress) are incredibly sophisticated, finding the exact optimal solution for large-scale, real-world MILP instances is often $\mathcal{NP}$-hard and computationally intractable within a reasonable timeframe.

To deal with this complexity, researchers and practitioners often employ **primal heuristics**—methods designed to find "good" or "near-optimal" feasible solutions quickly, even if optimality cannot be mathematically proven. One class of highly successful heuristics in this domain is **Large Neighborhood Search (LNS)**.

---

## What is Large Neighborhood Search (LNS)?

Large Neighborhood Search (LNS) is an iterative metaheuristic that explores the solution space by partially destroying a known feasible solution and then rebuilding (or repairing) it in hopes of discovering a better one.

While standard local search methods operate on "small" neighborhoods (e.g., flipping a single binary variable or swapping two items), LNS explores significantly larger neighborhoods. Because the neighborhood is so large, exploring it exhaustively is usually impossible. Instead, LNS relies on exact optimization methods (often by solving a smaller, restricted version of the original MILP) to navigate this neighborhood and find the best possible repair.

### The "Destroy" and "Repair" Framework

At its algorithmic core, LNS operates through two alternating steps applied to an incumbent solution $x^*$:

1. **Destroy Operator:** A subset of variables in $x^*$ is heavily modified or "freed." The values of these variables are unassigned, while the remaining variables are rigidly fixed to their values in $x^*$. This creates a smaller, sub-problem (often called a restricted master problem).
2. **Repair Operator:** The algorithm attempts to optimally (or near-optimally) reassign the freed variables to minimize the objective function, subjected to all original constraints, plus the fixed variables. Because this sub-problem is much smaller than the original MILP, it can often be solved quickly using an exact MILP solver.

If the "repaired" solution is strictly better than the incumbent $x^*$, it becomes the new incumbent, and the process repeats.

---

## LNS Strategies in the Context of MILP

When applying LNS generally, destroy and repair operators are often highly problem-specific. However, over the past two decades, several generic **MIP-based LNS heuristics** have been developed to operate automatically inside commercial solvers without requiring the user to write specific operators.

Two prominent, general-purpose LNS strategies for MILP include **Local Branching** and **Relaxation Induced Neighborhood Search (RINS)**.

### 1. Local Branching 

Introduced by Fischetti and Lodi (2003), Local Branching explores the neighborhood of an incumbent solution by adding linear constraints (local branching cuts) to the original problem. 

Given an incumbent binary solution $x^*$, a "local branching constraint" restricts the search space so that any new solution can differ from $x^*$ in at most $k$ binary variables:

$$ \sum_{j \in B: x_j^* = 1} (1 - x_j) + \sum_{j \in B: x_j^* = 0} x_j \le k $$

Where $B$ is the set of index variables for all binaries. The solver explores this reduced neighborhood (known as the $k$-opt neighborhood) as a sub-MILP. If a better solution is found, the incumbent is updated.

### 2. Relaxation Induced Neighborhood Search (RINS)

Designed by Danna, Rothberg, and Le Pape (2005) and heavily utilized by IBM CPLEX and Gurobi, RINS is a highly effective generic heuristic. 

RINS works by comparing the current best incumbent integer solution ($x^*$) against the optimal solution of the continuous LP relaxation at the current node of the branch-and-bound tree ($x^{LP}$).
- If $x_j^*$ and $x_j^{LP}$ agree on a variable (i.e., $x_j^* = x_j^{LP}$ for some variable $j$), that variable is temporarily fixed to that value.
- If they disagree, the variable is left "free."

A sub-MIP is formulated on the free variables and handed to the solver with a strict node or time limit. RINS leverages the intuition that variables showing consensus between the continuous relaxation and the integer incumbent are highly likely to maintain those values in an optimal or near-optimal solution.

---

## Advanced Variations of LNS

Modern LNS implementations often utilize adaptive machine learning techniques:

- **Adaptive Large Neighborhood Search (ALNS):** Instead of using a single fixed destroy and repair operator, ALNS maintains a portfolio of multiple heuristic operators. It uses a roulette-wheel selection continuously updated based on past performance to dynamically choose the best operators for the specific problem instance.
- **Machine Learning for Variable Fixing:** Contemporary research uses Graph Neural Networks (GNNs) or Random Forests to predict which variables should be fixed (Destroy phase), replacing the traditional randomized or LP-based metrics with predictive models learned offline from similar MILP instances.

## Why Use LNS?

**Pros:**
1. **Scalability:** By restricting the problem size, LNS can find high-quality solutions for massive instances that standard Branch-and-Bound algorithms choke on.
2. **Generality:** Heuristics like RINS and Local Branching require zero problem-specific knowledge to implement; they rely strictly on the mathematical structure.
3. **Flexibility:** It beautifully hybridizes heuristics with exact methods (Matheuristics).

**Cons:**
1. **Tuning Dependent:** The success of LNS is highly tied to the size of the neighborhood. If it's too large, the sub-problem will stall and become computationally expensive. If it's too small, the search space becomes trapped in local optima.
2. **No Guarantee of Optimality:** Since it is fundamentally a primal heuristic, LNS cannot prove that a solution is optimal; it only bounds the upper limits.

## Summary

Large Neighborhood Search offers an elegant compromise between heuristic speed and exact algorithmic rigor. By systematically destroying and repairing portions of a solution through sub-MIP formulations, LNS algorithms like RINS and Local Branching have fundamentally elevated the primal performance of commercial MILP optimization software today. 

# References
- Discrete Optimization || 01 Large Neighborhood Search asymmetric TSP with time windows 8 42 [link](https://youtu.be/FpwKZhX5X8M?si=QibyaGdaiLX2rsvU)
