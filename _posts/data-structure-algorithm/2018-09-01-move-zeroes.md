---
layout: distill
title: "Leetcode 283: Move Zeroes"
description: "A two-pointer approach to move all non-zero elements to the front of an array"
tags: algorithms two-pointers arrays same-direction-traversal taxi
categories: data-structure-algorithm
date: 2018-09-01
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# If new array is allowed
- The problem becomes trivial.
- Linearly read the array, if the element is nonzero, then append it to the new array. Finally, append the remaining zeros to the new array.

# Two-pointer approach: reader and writer
- In-place restriction requires two pointers.


## Core logic
* We need a pointer (`read`) that traverses linearly to check if the current number is 0.
* If the number at `read` is nonzero, we move it. Since computers don't physically move data, this is accomplished through copying and deleting.
* We explicitly copy the number. Deletion is implicit (handled by overwriting).
* To maintain the order of non-zero elements without improperly overwriting them, we need a second pointer (`record`).
* `record` tracks where the next non-zero element should be placed, advancing only when a number is copied to it.
* This is the basic idea of the same-direction two-pointer approach.

## To prevent overwriting
1. Reader always moves forward, writer sometimes moves forward, thus reader>=writer
2. We write EVERY non-zero value observed (no exception)
Therefore, any non-zero value that is overwritten by the writer was previously read and written too!

## Algorithm Steps
Initialization - main loop - termination - post processing
### Initialization
- `read` obviously starts from 0.
- The first nonzero element would be placed at index 0, so `record` starts from 0.

### Main loop
- `read` proceeds by for loop.
`record` only proceeds when `nums[read]` is nonzero.
- Thus `record` is always less than or equal to `read`
- Thus we don't need to worry about overwriting or interval between the pointers

### Terminination
Easy. When `read` reaches the end of the array.

### Post processing
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