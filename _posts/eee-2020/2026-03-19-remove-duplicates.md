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

- We use two pointers: one pointer (`read`) to iterate through the current numbers, and another pointer (`record`) to indicate the place where the replacement should occur.
- Because the array is sorted, any duplicate elements will be adjacent to each other.

## Initialization

- Start from index 1. Because index 0 must always have a unique element (the first element seen is never a duplicate of anything before it).
- Thus, `record` starts from 1. 

## Main loop

- `read` proceeds by a `for` loop starting from index 1.
- We check if the current element `nums[read]` is different from the previous element `nums[read - 1]`.
- If it is different, it means we have found a new unique element. We place this unique element at `nums[record]` and increment `record`.
- `record` only proceeds when we find a new unique element, ensuring all unique elements are packed at the front of the array.

## Termination

- The loop terminates when `read` reaches the end of the array. The value of `record` at this point will be the total number of unique elements.

# My solution

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # edge case: if empty array
        if not nums:
            return 0
            
        record = 1
        # start from index 1 because index 0 must have a unique element
        for read in range(1, len(nums)):
            # if we see a new unique element
            if nums[read] != nums[read - 1]:
                nums[record] = nums[read]
                record += 1
                
        return record
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We only modify the array in-place and use two integer variables (`read` and `record`).
- **Time Complexity**: $O(n)$. We traverse the list of length $n$ exactly once.

# Checklist
- [x] read solution
- [x] solve
