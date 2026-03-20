---
layout: distill
title: "Leetcode 704: Binary Search"
description: "A foundational $O(\\log n)$ search algorithm for sorted arrays."
tags: algorithms binary-search arrays dynamic-programming dp-1d
categories: eee-2020
date: 2018-09-20
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/binary-search/).

# Intuition
- Linear Search: iterate using for loop. Takes $O(n)$ time. Does not exploit the sorted property of the array.
- However, if the array is **sorted**, we can drastically improve the search time to $O(\log n)$ using **Binary Search**.
- Binary search operates similarly to how we look up a word in a physical dictionary: we split the dictionary in half, check if our word comes before or after the halfway mark, and then discard the irrelevant half.
- Binary search can be viewed as inward-traversal two-pointer approach (while loop) and dynmaic programming (recursion).

#  Two-Pointer Approach

## Algorithm

Binary search is effectively an inward-traversal two-pointer technique!

- We use one pointer (`left`) to track the start of our active search space.
- We use another pointer (`right`) to track the end of our active search space.
- At each step, we calculate the `mid` pointer.
- We then compare the `target` value with the value at `nums[mid]`:
  - If the target is equal to the `mid` value, we found it!
  - If the target is strictly **greater** than the `mid` value, it must exist in the right half of the remaining array. We update `left = mid + 1`.
  - If the target is strictly **less** than the `mid` value, it must exist in the left half of the remaining array. We update `right = mid - 1`.

### Termination

- The loop stops either when we find the target element, OR when the `left` pointer crosses the `right` pointer (`left > right`).
- More on the second condition: it is easy to see that the final iteration has always one element (think of four, three, two elements cases as previous iteration). Whether the target is greater or smaller than the `mid` value, the next situation is left>right.
- If `left > right`, it means our search space has collapsed completely and the target element is absolutely not in the array. We return `-1`.

## My solution

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        # Target not found
        return -1
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We only maintain a few integer variables (`left`, `right`, and `mid`) which require constant memory.
- **Time Complexity**: $O(\log n)$. At each iteration of the `while` loop, we halve the size of the search array. Consequently, the maximum number of times the loop can run is proportional to the base-2 logarithm of $n$.
