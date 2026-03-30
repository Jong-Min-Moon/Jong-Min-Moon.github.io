---
layout: distill
title: "Leetcode 977. Squares of a Sorted Array"
description: "Solving the Squares of a Sorted Array problem using a Two Pointers approach."
date: 2026-03-29
categories: eee-2020
tags: leetcode two-pointers(inward) array algorithm
project: eee-2020
---

The original problem is [here](https://leetcode.com/problems/squares-of-a-sorted-array/description/).
## Two Pointers Approach

The brute force approach is square $(O(N))$ and then sort $(O(N \log N))$. So the total time complexity is $O(N \log N)$. However, this is a stupid approach because it does not use the fact that the original array is sorted. The follow-up question calls for $O(N)$ time complexity.

 
- What we fear is signs; If the numbers are all positive all negative the problem is trivial.
- Let's assume the array contains both positive and negative numbers.
-  Since the array is pre-sorted, `nums[0]` is the negative number with the largest magnitude. `nums[n-1]` is the positive number with the largest magnitude.
- As we move the pointer inward by one index, we encounter the next largest magnitude number.
- So we can compare the absolute values of the elements at the `left` and `right` pointers. We square the larger one, place it at the result array from the end, and move the corresponding pointer inward.

### When do we stop?
- if negative or positive numbers are exhausted, the problem becomes trivial. But there's no harm in continuing the loop until the pointers cross each other.

### Code (Python)

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

### Complexity
- **Time Complexity:** $O(N)$ because calculating the squares and placing them in the correct spot requires exactly one pass over the array.
- **Space Complexity:** $O(N)$ because we are allocating a new array of size $N$ to store the result, as required by the problem statement.


# References
- How to Solve Squares of a Sorted Array Efficiently in One Go!
[link](https://youtu.be/KyKeW6PZiWo?si=apgkBtA99pbZWm-7)