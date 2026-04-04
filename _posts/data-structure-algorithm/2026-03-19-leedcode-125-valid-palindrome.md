---
layout: distill
title: "Leetcode 125: Valid Palindrome"
description: "A two-pointer approach to check if a string is a valid palindrome"
tags: algorithms two-pointers(inward) strings
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---
Original problem is [here](https://leetcode.com/problems/valid-palindrome/description/).

# Inward Traversal Two-Pointer Approach

- We need to compare left and right elements so obviously we need two pointers and they move toward the center.
- We place one pointer at the beginning (`left`) and one at the end (`right`).
- We systematically **squeeze** them towards the center, functioning as a `comparer`.
- If the characters at the `left` and `right` pointers ever mismatch, the string is not a palindrome.
- If the pointers cross each other without a mismatch, the string is a valid palindrome!

# Algorithm

## String Handling

- First we remove blanks and non-alphanumeric characters and convert the string to lowercase using `isalnum()` and `lower()`.
- We use **list comprehension**  to **filter and format** the string.
- Finally use `''.join()` to join the filtered characters into a string.

```python
cleaned_s = ''.join(c.lower() for c in s if c.isalnum())
```

> **Note**: While filtering the string upfront is very clean, an optimized solution would do this filtering *on the fly* during the two-pointer traversal to save $O(n)$ space.

## Initialization

- `left` points to `0` (the first character).
- `right` points to `len(cleaned_s) - 1` (the last character).

## Main loop

- We use a `while` loop that continues as long as `left < right`.
- At each step, we compare `cleaned_s[left]` and `cleaned_s[right]`.
- If they are not equal, we immediately return `False`.
- If they are equal, we move `left` to the right by 1 and `right` to the left by 1 (squeezing inwards).

## Termination

- If the loop finishes without returning `False`, it means all corresponding characters matched. We then return `True`.

# My solution

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = [c.lower() for c in s if c.isalnum()]
        s = ''.join(s)

        left = 0
        right = len(s)-1
        while left < right:
            if s[left] == s[right]:
                left += 1
                right -= 1
            else:
                return False
        return True
```

## Complexity Analysis

- **Space Complexity**: $O(n)$. We create a new cleaned string which takes space proportional to the original string length. An optimized in-place solution would achieve $O(1)$ space.
- **Time Complexity**: $O(n)$. We traverse the list to clean it, and then traverse it again with two pointers. Both take linear time.