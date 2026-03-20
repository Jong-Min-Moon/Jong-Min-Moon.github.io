---
layout: distill
title: "Leetcode 27: Remove Element"
description: "A two-pointer approach to remove a specific element in-place from an array"
tags: algorithms two-pointers arrays same-direction-traversal
categories: eee-2020
date: 2026-03-19
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Two-pointer approach

- pointer `read` to read the new element
- pointer `save` to save the non-`val` element
- We remove `val` by moving the non-`val` elements to the front.
- This is the basic idea of the same-direction-traversal two-pointer approach.
- This problem is almost the same as Leetcode 26 ["Remove Duplicates from Sorted Array"](https://jong-min.org/blog/2026/remove-duplicates/). The only difference is that we need to remove a specific element `val` instead of duplicates.

## Initialization

- `read` starts from 0 to iterate over every element in the array.
- `save` starts from 0, tracking where the next non-`val` item should go.

## Main loop

- `read` proceeds by a `for` loop.
- We check if the current element `nums[read]` is different from `val`.
- If it is the same as `val`, we just increment `read`.
- If it is different, it means we have found a valid element. We place the element at `nums[save]` and increment `save` by 1.
- `save` only proceeds when we find a valid element, ensuring all non-`val` elements are packed at the front of the array and we always have `save <= read`.

## Termination

- The loop terminates when `read` reaches the end of the array (stop condition).


# My solution

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        save = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[save] = nums[read]
                save += 1
        return save
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We only modify the array in-place and use the integer variables (`read` and `save`).
- **Time Complexity**: $O(n)$. We traverse the list of length $n$ exactly once.
