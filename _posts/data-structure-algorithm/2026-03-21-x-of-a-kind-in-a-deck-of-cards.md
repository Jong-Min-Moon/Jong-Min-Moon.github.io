---
layout: distill
title: "Leetcode 914: X of a Kind in a Deck of Cards"
description: "Grouping elements by checking the Greatest Common Divisor (GCD) of their frequencies."
tags: algorithms hash-table math arrays
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/x-of-a-kind-in-a-deck-of-cards/).

# Intuition
- The problem asks us if we can sort an integer array of cards into partitions of size $X \ge 2$, where every partition contains exactly the same number.
- For this to be solvable, we must know the exact volume of each card cluster. This is natively solved by tracking frequencies using a **Hash Map**.
- Let's say we have 4 copies of `Card A` and 6 copies of `Card B`. Can we partition them into identical groups of the same size $X$? 
  - Yes! We can partition both of them into subgroups of exactly size $2$: i.e., two groups of A—(A,A) (A,A)—and three groups of B—(B,B) (B,B) (B,B). 
  - Notice that 2 evenly divides into both 4 and 6. 
- The mathematical revelation here is that the **Greatest Common Divisor (GCD)** of all our card frequencies across the entire deck must simply evaluate to $\ge 2$! If the GCD is 1, a baseline $X \ge 2$ configuration is physically impossible.

# Hash Map & GCD Approach

## Algorithm
1. **Frequency Counting:** Utilize a hash map (`collections.Counter` in Python) to build out our frequency table. This completes our grouping volume awareness in $O(n)$ linear time.
2. **Value Extraction:** Extract specifically the raw frequency counts from the dictionary values map (since the actual card numbers themselves play no role in uniform divisibility bounds).
3. **Compute Overall GCD:** Cumulatively aggregate the greatest common divisor strictly across all count values. We can use Python's `math.gcd` sequentially traversing over the values map array using `functools.reduce`.
4. **Validation:** If the absolute computed aggregate GCD of all partition volumes evaluates to $\ge 2$, return `True`.

## My solution

```python
import collections
from math import gcd
from functools import reduce

class Solution:
    def hasGroupsSizeX(self, deck: list[int]) -> bool:
        # 1. Count frequencies of each integer card via Hash Map
        count = collections.Counter(deck)
        
        # 2 & 3. Iteratively compute the GCD tracing through the entire frequency array
        # reduce() continuously applies the gcd to rolling pair-wise values 
        overall_gcd = reduce(gcd, count.values())
        
        # 4. Validate the partitioning bounds
        return overall_gcd >= 2
```

## old solution

```
class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        if len(deck) == 1:
            return False
        count = {}
        for num in deck:
            count[num] = count.get(num, 0) + 1

        min_count = len(deck)+1
        for num in count:
            if count[num] < min_count:
                min_count = count[num]
        result = 0
        for j in range(2, min_count+1):
            if (min_count % j == 0):
                if sum(((count[i] % j) > 0) for i in count) == 0:
                    return True

        return False
```
## Complexity Analysis

- **Space Complexity**: $O(n)$ where $n$ is the total length of the deck array. In the worst-case scenario where every card boasts a unique integer, the hash map keys scale linearly with $n$.
- **Time Complexity**: $O(N \log C)$ worst case. Where $N$ is building the underlying frequency map in linear time limits, and calculating the active Euclidean GCD algorithm spanning across up to $N$ entries dictates a maximum bound determined by $\log C$, heavily contingent on bounds of the fractional frequencies evaluated.
