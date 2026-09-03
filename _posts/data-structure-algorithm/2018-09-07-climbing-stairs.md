---
layout: distill
title: "Leetcode 70: Climbing Stairs"
description: "Solving the Climbing Stairs problem using recursion, recursion tree analysis, and memoization."
tags: algorithms dynamic-programming dp-1d recursion memoization
categories: data-structure-algorithm
date: 2018-09-07
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/climbing-stairs/).

# Problem Statement

You are climbing a staircase that takes $n$ steps to reach the top. Each time you can either climb $1$ or $2$ steps. In how many distinct ways can you climb to the top?

---

# Approach 1: Brute Force

## Algorithm

In this brute force approach, we take all possible step combinations (i.e., $1$ and $2$) at every step. At every step, we call the recursive function for taking $1$ step and $2$ steps, and return the sum of the returned values of both branches:

$$\text{climbStairs}(i, n) = \text{climbStairs}(i + 1, n) + \text{climbStairs}(i + 2, n)$$

where:
- $i$ defines the current step.
- $n$ defines the destination step.

### Base Cases

- If $i > n$: We stepped past the destination step, so there are $0$ valid ways (return `0`).
- If $i == n$: We reached exactly the target step, counting as $1$ valid combination (return `1`).

## Implementation

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        def climb(i: int, n: int) -> int:
            if i > n:
                return 0
            if i == n:
                return 1
            return climb(i + 1, n) + climb(i + 2, n)

        return climb(0, n)
```

## Complexity Analysis

- **Time Complexity:** $O(2^n)$. At each step, the recursion branches into $2$ subproblems. The size of the recursion tree will be $O(2^n)$.
- **Space Complexity:** $O(n)$. The depth of the recursion tree can go up to $n$ (when taking $1$ step at a time), which determines the maximum size of the call stack.

### Recursion Tree for $n = 5$

The recursion tree for $n = 5$ demonstrates how redundant calculations explode exponentially:

```
                            (0)
                      /             \
                   (1)               (2)
                 /     \           /     \
               (2)     (3)       (3)     (4)
              /   \   /   \     /   \   /   \
            (3)  (4) (4)  (5) (4)  (5) (5)  (6)
            ...
```

Notice that subproblems like `(2)`, `(3)`, and `(4)` are computed over and over again along different paths.

---

# Approach 2: Recursion with Memoization

## Algorithm

In the previous approach, we are redundantly calculating the result for every step. Instead, we can store the result of each step in a `memo` array and directly return the cached result whenever that step is called again.

In this way, we are **pruning the recursion tree** with the help of the `memo` array and reducing the size of the recursion tree down to $n$.

```
                    (0)
                  /     \
               (1)      (2) [cached]
              /   \
            (2)   (3) [cached]
           /   \
         (3)   (4) [cached]
        /   \
      (4)   (5) [base]
     /   \
   (5)   (6)
```

Every state from $0$ to $n$ is evaluated only once, transforming an exponential search tree into a linear sequence of subproblems.

## Implementation

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        memo = [0] * (n + 1)

        def climb(i: int, n: int) -> int:
            if i > n:
                return 0
            if i == n:
                return 1
            if memo[i] > 0:
                return memo[i]

            memo[i] = climb(i + 1, n) + climb(i + 2, n)
            return memo[i]

        return climb(0, n)
```

## Complexity Analysis

- **Time Complexity:** $O(n)$. The size of the recursion tree is reduced to $n$ since each subproblem is evaluated at most once.
- **Space Complexity:** $O(n)$. The recursion depth can still reach $n$, and the `memo` array takes $O(n)$ auxiliary space.
