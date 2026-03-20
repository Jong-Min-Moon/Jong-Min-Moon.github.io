---
layout: distill
title: "Leetcode 392: Is Subsequence"
description: "A two-pointer approach to check if one string is a subsequence of another"
tags: algorithms two-pointers strings same-direction-traversal
categories: eee-2020
date: 2018-09-20
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/is-subsequence/).
# Two-pointer approach
- one pointer to read 't' (`read`)
- another pointer to compare with 's' (`compare`)
- Both move in the same direction, making this another application of **same-direction-traversal**. The twist is that each pointer runs in different array.

# Algorithm

## Initialization

- Both pointers start at 0.

## Main loop
- Little bit tricky because two arrays have different lengths.
- Must stop either one of the pointers reaches the end of the array.
- Therefore we use `while` and `and` condition.
- **Operation:** Compare the characters at `t[read]` and `s[compare]`.
- **Pointer update:**
  - The `t` pointer (`read`) *always* increases by $1$ at each step, because we are continually scanning through the longer string.
  - The `s` pointer (`compare`) only increases *when there is a match* against `t` (i.e., `s[compare] == t[read]`).

## Termination

- The loop **ends** when either:
  - The `t` pointer (`read`) reaches the length of `t` (we've scanned the entire target string), OR
  - The `s` pointer (`compare`) reaches the length of `s` (we've successfully matched all characters in the target subsequence).

## Success Condition

- A **success** means we found all characters of `s` inside `t` in the correct relative order.
- With our pointer logic, a success simply means the `s` pointer equals the length of `s` (`compare == len(s)`).

# My solution

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        compare = 0
        read = 0 
        while read < len(t) and compare < len(s):
            if t[read] == s[compare]:
                compare +=1
            read +=1
        return compare==len(s)
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We only maintain two integer variables (`compare` and `read`), resulting in constant extra space.
- **Time Complexity**: $O(|t|)$. In the worst-case scenario, we traverse the string `t` exactly once to find all matches or determine failure.

