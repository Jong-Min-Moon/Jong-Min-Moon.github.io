---
layout: distill
title: "Leetcode 121: Best Time to Buy and Sell Stock"
description: "Iteratively updating minimums and maximum profits in a single pass"
tags: algorithms arrays optimal-substructure
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---
The original problem is [here](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/).
# Problem Solving Approaches

## 1. Brute Force ($O(N^2)$)
- Computes an $n \times n$ table to check every possible pair of buy and sell days.
- We calculate the profit for `prices[j] - prices[i]` (where $j > i$) and keep track of the maximum.
- **Problem**: This easily results in a Time Limit Exceeded error since checking all permutations scales quadratically.

## 2. Two-pass Approach ($O(2N)$)
- **Step 1**: Find the absolute minimum in the array.
- **Step 2**: Sift through the array *up front* (ahead of the absolute minimum) to find the maximum possible sell price.
- **Problem**: This will fail if the global minimum appears at the very end of the array, rendering it impossible to find a valid maximum *after* it since you must buy before you sell!

## 3. One-pass Optimal Approach ($O(N)$)
- Iterate through the prices exactly once.
- On each day, update the **minimum price seen so far**. 
- Then, calculate what our profit would be if we sold *today* (current price - minimum price seen so far) and update the **maximum profit** if this current profit is greater.

# My solution

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            # Update minimum price
            if price < min_price:
                min_price = price
            # Update maximum profit
            else:
                max_profit = max(max_profit, price - min_price)
                
        return max_profit
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We only maintain two integer tracking variables (`min_price` and `max_profit`).
- **Time Complexity**: $O(N)$. We make exactly one pass through the `prices` array.

# Checklist
- [x] (121) best time to buy and sell stocks
