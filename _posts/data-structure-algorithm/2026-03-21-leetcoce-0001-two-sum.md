---
layout: distill
title: "Leetcode 1: Two Sum"
description: "Finding a pair of numbers that add up to a target dynamically using a one-pass Hash Map."
tags: algorithms hash-table arrays
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/two-sum/).

# Hash Map Approach
- The naive brute-force approach is to check all $n(n-1)/2$ possible pairs, taking $O(n^2)$ time.
- A key observation is, for each element, we need not pair it with all the others.
    - Since we know the target value, it suffices to find the index of `target-num`, aka `complement`.
    - So we reduce `n-1` paring into one lookup.
    - Hash map has $O(1)$ lookup time.
- we do the first pass of hash map creaction and seocnd path of complement lookup.
 - There can be a collision.
    - The example 3 is `nums = [3, 3], target = 6`.
    Since we are looking for two indices, recurrence larger than 2 is not a problem; we can forget from the 3rd recurrence.
    - For two occurrence, we need not do chaining, because the second occurrence will overwrite the first occurrence in the first pass, and if we need to return the indices of the same numbers, the first occurrence will lookup the second occurrence in the second pass.

# Algorithm

Instead of just tracking values, our Hash Map cache must map the **actual numbers seen** natively to their original **index positions** in the string array, because the prompt explicitly demands we return the indices.

1. **First pass:** Loop through the `nums` array linearly. Fill in the hash map where key is num and value is index. 
2. **Second pass:** Calculate the complement for each num, and check if the complement is in the hash map. If yes, return the index of the complement and the current index.
    - when `complement` = `num`, we need to distinguish between one occurrence and two occurrences. We should add `if` statement in `in` statement.

# My solution

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map = {}
        for i, num in enumerate(nums):
            map[num] = i
        for i, num in enumerate(nums):
            complement = target-num
            if complement in map and map[complement] != i:
                return [i,map[complement]]
```

## Complexity Analysis

- **Space Complexity**: $O(n)$. In the worst-case scenario where the exact valid array bounds pair is found clustered at the absolute end tail of the array, we would functionally log almost exactly $n-1$ discrete elements tracking into our active hash map array index limit.
- **Time Complexity**: $O(n)$. We strictly traverse the list measuring $n$ elements precisely once. Because searching dynamically for a functional key within a foundational Python dictionary implementation (`in seen`) resolves in constant $O(1)$ average boundaries, the heavy geometric loop operation boils entirely down to one clean linear array scan.
