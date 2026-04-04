---
layout: distill
title: "Leetcode 283: Move Zeroes"
description: "A two-pointer approach to move all non-zero elements to the front of an array"
tags: algorithms two-pointers arrays same-direction-traversal taxi
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Two-pointer approach

- We need one pointer (`read`) to read the new number and decide whether it is 0 or not.
- If it is nonzero, we need to move it to the front. However we need to keep the order of the non-zero elements and we don't want to overwrite.
- Thus we need a second pointer (`record`) to keep track of the position where the next non-zero element should be placed.
- This is the basic idea of same-direction-traversal two-pointer approach.

## Initialization
- `read` obviously starts from 0.
- The first nonzero element would be placed at index 0, so `record` starts from 0.

## Main loop
- `read` proceeds by for loop.
`record` only proceeds when `nums[read]` is nonzero.
- Thus `record` is always less than or equal to `read`
- Thus we don't need to worry about overwriting or interval between the pointers

## Terminination
Easy. When `read` reaches the end of the array.

## Post processing
Easy. Fill the remaining positions in the array (from `record` to the end) with zeros.

## Caveats
- do not confuse nonzero with positive

# My solution

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        record = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                nums[record] = nums[read]
                record += 1
        for i in range(record, len(nums)):
            nums[i] = 0
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. Only constant space is used.
- **Time Complexity**: $O(n)$. We traverse the `nums` list first to move all non-zero elements to the beginning of the array which costs $O(n)$ time. At the worst case when the original array only consists of 0s, we will use $O(n)$ time to fill all remaining elements with 0s. Hence, the overall time complexity is $O(2n)$, which is simplified to $O(n)$. However, the total number of operations are still sub-optimal. The total operations (array writes) that the code does is $n$ (Total number of elements).


# References
- https://leetcode.com/problems/move-zeroes/editorial/
- https://www.youtube.com/watch?v=QzZ7nmouLTI&t=162s