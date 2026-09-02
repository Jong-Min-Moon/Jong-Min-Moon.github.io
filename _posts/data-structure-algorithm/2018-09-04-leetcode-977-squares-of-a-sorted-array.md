---
layout: distill
title: "Leetcode 977: Squares of a Sorted Array"
description: "A two-pointer inward traversal approach to square each number and sort the array in O(n) time"
tags: algorithms two-pointers(inward) arrays
categories: data-structure-algorithm
date: 2018-09-04
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

Original problem is [here](https://leetcode.com/problems/squares-of-a-sorted-array/description/).

# Inward Traversal Two-Pointer Approach

## Intuition

- The brute force approach: squaring takes $O(N)$ time and then sorting takes $O(N \log N)$. So the total time complexity is $O(N \log N)$.
- However, this is an inefficient approach because it does not use the fact that the **original array is sorted**. The follow-up question calls for $O(N)$ time complexity.
- What we fear is signs; If the numbers are all positive or all negative, the problem is trivial. Therefore Let's assume the array contains both positive and negative numbers.




### Pre-sorting gives us:
- Since the array is pre-sorted, `nums[0]` is the negative number with the largest magnitude. `nums[n-1]` is the positive number with the largest magnitude.
- As we move the pointers inward by one index, we encounter the next largest magnitude numbers.  

- So we can compare the squares (or absolute values) of the elements at the `left` and `right` pointers. We take the larger square, place it into the result array from the end, and move the corresponding pointer inward.

# Algorithm

## Initialization

- `left` points to `0` (the first element).
- `right` points to `n - 1` (the last element).
- Allocate a `result` array of size $N$: `result = [0] * n`.

## Main Loop

- We use a `while` loop that continues as long as `left <= right`.
- At each step:
  - Calculate `sq_left = nums[left]**2` and `sq_right = nums[right]**2`.
  - The target index from the end is `index_result = right - left`.
  - If `sq_left < sq_right`:
    - Place `sq_right` into `result[index_result]` and move `right` inward (`right -= 1`).
  - Else:
    - Place `sq_left` into `result[index_result]` and move `left` inward (`left += 1`).

## Termination

- If negative or positive numbers are exhausted, the problem becomes trivial, but there's no harm in continuing the loop until the pointers cross each other.
- When `left > right`, all $N$ elements have been processed and placed into `result`.

# My Solution

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n  = len(nums)
        result = [0]*n
        left = 0
        right = n-1
        while left <= right:
            sq_left = nums[left]**2
            sq_right = nums[right]**2
            index_result = right-left
            if sq_left < sq_right:
                result[index_result] = sq_right
                right -=1
            else:
                result[index_result] = sq_left
                left += 1
        return result
```

## Complexity Analysis

- **Time Complexity:** $O(N)$ because calculating the squares and placing them in the correct spot requires exactly one pass over the array.
- **Space Complexity:** $O(N)$ because we are allocating a new array of size $N$ to store the result, as required by the problem statement.

# References

- [How to Solve Squares of a Sorted Array Efficiently in One Go!](https://youtu.be/KyKeW6PZiWo?si=apgkBtA99pbZWm-7)
