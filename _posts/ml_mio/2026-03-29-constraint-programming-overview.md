---
layout: distill
title: "An Overview of Constraint Programming (CP)"
description: "Exploring the fundamentals of Constraint Programming (CP), how it differs from MILP, and its powerful constraint propagation mechanisms for solving complex combinatorial problems."
date: 2026-03-29
categories: ml_mio
tags: optimization constraint-programming algorithms combinatorial-search
project: ml_mio
---

## Introduction to Constraint Programming (CP)

While Mixed-Integer Linear Programming (MILP) is the workhorse of operations research, it is not the only paradigm for solving complex optimization problems. **Constraint Programming (CP)** is a highly expressive programming paradigm particularly well-suited for combinatorial puzzles, scheduling, and logistical routing problems where relationships between variables are highly non-linear, logical, or structural.

Instead of defining a problem purely with linear equations and inequalities, CP allows practitioners to model problems using high-level **global constraints** and logical relationships. The solver then finds solutions (or proves that none exist) by interleaving logical deduction (constraint propagation) with tree search (backtracking).

---

## The Core Components of CP

A Constraint Satisfaction Problem (CSP) or Constraint Optimization Problem (COP) relies on three fundamental components:

1. **Variables ($V$):** The unknowns that need to be decided.
2. **Domains ($D$):** The finite set of possible values that each variable can take. Unlike MILP, where continuous variables are common and binary/integer restrictions are added, CP typically starts with discrete, finite domains (e.g., $x \in \{1, 2, 3, 4, 5\}$).
3. **Constraints ($C$):** The rules that define which combinations of values are allowed.

### Global Constraints

The true expressive power of CP comes from its vocabulary of constraints. Instead of formulating a big-M linear constraint to represent "two events cannot overlap," CP solvers offer native **global constraints**.

A classic example is `AllDifferent(x1, x2, ..., xn)`. In MILP, enforcing that $n$ integer variables take distinct values requires $O(n^2)$ binary variables and constraints. In CP, `AllDifferent` is a single mathematical construct that the solver natively understands and optimizes internally using matching algorithms from graph theory.

Other powerful global constraints include:
- `Cumulative(start_times, durations, resource_demands, capacity)` for scheduling under resource limits.
- `Element(index, array, value)` for array lookups and complex assignments.
- `Circuit(nodes)` for solving Traveling Salesperson-like problems.

---

## How Constraint Solvers Work

Unlike MILP, which relies heavily on solving continuous LP relaxations to find bounds, CP relies on **Constraint Propagation** and **Search**.

### 1. Constraint Propagation (Domain Filtering)
When a variable's domain changes (e.g., a choice is made during the search), the solver triggers reasoning algorithms attached to each constraint. The goal is to deduce that certain values in the domains of *other* variables can no longer participate in any feasible solution, and safely remove them.

For example, if we have $X, Y \in \{1, 2, 3\}$ and the constraint $X < Y$:
- If the solver branches by assigning $X = 3$, the constraint propagates: there is no value in $Y$'s domain strictly greater than 3.
- Thus, the solver instantly detects a conflict without having to evaluate $Y = 1$ or $Y = 2$.

### 2. Search Strategy (Backtracking)
Because propagation alone cannot usually solve $\mathcal{NP}$-hard problems, the solver must guess by branching. It picks a variable, picks a value from its domain, and then applies constraint propagation.
- If a domain becomes empty, a **dead end (conflict)** is reached, and the solver backtracks to try a different value.
- The order in which variables and values are chosen (branching heuristics) drastically affects performance. Techniques like *First-Fail* (picking the variable with the smallest remaining domain) are standard defaults in CP frameworks.

---

## CP vs. MILP: When to use what?

Though both paradigms solve mathematical optimization problems, they excel in entirely different areas:

| Feature | Mixed-Integer Linear Programming (MILP) | Constraint Programming (CP) |
| :--- | :--- | :--- |
| **Modeling Strengths** | Economic costs, allocations, flows, scaling constraints. Best if the problem is easily visualized linearly. | Complex logical rules, non-linear dependencies, sequencing, timetabling. |
| **Solving Mechanism** | Linear programming relaxations, cutting planes, branch-and-bound. | Domain filtering (propagation), inference, backtracking search. |
| **Continuous Variables** | Native and highly efficient. | Not native; typically requires discretization or specialized continuous CP branches. |
| **Weakness** | Struggles heavily with dense logical "If-Then" constraints (Big-M issues) and pure combinatorial puzzles (e.g., Sudoku). | Struggles with dense problems that have weak logical inference but strong objective bounds (e.g., knapsack problems). |

---

## Modern Hybrid Approaches

Because the strengths of MILP and CP are almost perfectly orthogonal, modern operations research often relies on **hybrid solvers** (like CPLEX CP Optimizer or Google OR-Tools). 

These hybrid frameworks leverage **Benders Decomposition** or **Logic-Based Benders Decomposition**, handling the continuous and heavily constrained financial aspects with an LP/MILP solver while delegating complex scheduling and sequencing to a CP engine.

## Summary
Constraint Programming is a robust, dynamic method for finding feasible solutions (and proving optimality) in heavily constrained environments. Whenever your problem is dominated by strict logical bounds rather than cost-minimization gradients, CP is likely the superior approach.
