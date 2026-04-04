---
layout: distill
title: "Leetcode 13: Roman to Integer"
description: ""
tags: algorithms strings arrays two-pointers sliding-window
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---
- The original problem is [here](https://leetcode.com/problems/roman-to-integer/).

# Sliding window approach
- Let's just write down to see the pattern: I, II, III, IV, V, VI, VII, VIII, IX, X, ...
- The changepoint is IV, IX, as pointed out in the problem.
- One number can be represented by up to 4 characters. However, the punchine is we don't need to count based on one number.
- We can naturally add when small number is to the right of large number. 
    - We need not treat the added number as one number.
    - We can treat them as separate. For example, treat `III` is 1+1+1, not as 3.
- Thus, we just need to convert either one or two characters into a number to get the answer.
- The operation revolves around: **read two, process (add or subtract) one**.
-  We read the current character and the *next* character. If the current character is smaller than the next character (like `I` before `V`), we subtract it. Otherwise, we add it.
- This is a sliding window approach of size 2.

# Algorithm

## Initialization
- `total` starts at 0.

## Main loop
- Iterate through the string `s` from left to right.
- At each position `i`, compare the value of the current character `s[i]` with the value of the next character `s[i+1]`.
- If `s[i]` is smaller than `s[i+1]`, subtract the value of `s[i]` from `total`.
- Otherwise, add the value of `s[i]` to `total`.
- Then increase `i` by 1, not two. Thus we are sliding size 2 window by 1 step.

## Termination
- The loop ends when `i` reaches the end of the string `s`.

## Success Condition
- The final value of `total` is the integer representation of the Roman numeral.

## My solution

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        total = 0
        for i in range(len(s)):
            if (i < len(s)-1) and (roman_map[s[i]] < roman_map[s[i+1]]):
                total -= roman_map[s[i]]
            else:
                total += roman_map[s[i]]
        return total
```
 
