---
layout: distill
title: "Leetcode 26: Remove Duplicates from Sorted Array"
description: "A two-pointer approach to remove duplicates in-place from a sorted array"
tags: algorithms two-pointers arrays
categories: eee-2020
date: 2026-03-19
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Two-pointer approach

- We use two pointers: one pointer (`read`) to iterate through the current numbers, and another pointer (`compare`) to compare with the current number.
- Because the array is sorted, any duplicate elements will be adjacent to each other.
- This is the basic idea of same-direction-traversal two-pointer approach.


## Initialization
- `read` obviously starts from 1, because comparing the first number with the previous number is not possible.     
- `compare` starts from 0.

## Main loop

- `read` proceeds by a `for` loop starting from index 1.
- We check if the current element `nums[read]` is different from the previous element `nums[compare]`.
- If it is the same, we just increment `read`.
- If it is different, it means we have found a new unique element. We increase compare pointer, and place the unique element at `nums[compare]`.
- This is to keep the 'compare' as the earliest position of duplicates.
- `compare` only proceeds when we find a new unique element, ensuring all unique elements are packed at the front of the array and we always have `compare` <= `read`.

## Termination

- The loop terminates when `read` reaches the end of the array. The value of `compare+1` at this point will be the total number of unique elements.

# My solution

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        compare = 0
  
        for read in range(1, len(nums)):
            if nums[read] != nums[compare]:
                compare += 1
                nums[compare] = nums[read]
    
        return compare+1
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We only modify the array in-place and use two integer variables (`read` and `record`).
- **Time Complexity**: $O(n)$. We traverse the list of length $n$ exactly once.


