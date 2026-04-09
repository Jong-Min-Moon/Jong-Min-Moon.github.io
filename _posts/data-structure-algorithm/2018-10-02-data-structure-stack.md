---
layout: distill
title: "Data Structure: Stack"
description: "An introduction to the Last-In-First-Out (LIFO) stack data structure and its common algorithmic patterns."
date: 2018-10-02
tags: data-structure stack
categories: data-structure-algorithm
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Introduction

- A **Stack** is a linear data structure that follows the **LIFO (Last-In-First-Out)** principle.
- This means the last element added to the stack will be the first one to be removed.
- A concrete example is the web browser: when you click the "Back" button, you are popped from the history stack to the most recently visited page. When you go all the way back, the back button is disabled.


# Basic Operations

A stack typically supports the following operations, all of which run in **$O(1)$** time:

| Operation   | Description                                  | Time Complexity |
| :---------- | :------------------------------------------- | :-------------- |
| `push(x)`   | Adds element `x` to the top of the stack.    | $O(1)$          |
| `pop()`     | Removes and returns the top element.         | $O(1)$          |
| `peek()`    | Returns the top element without removing it. | $O(1)$          |
| `isEmpty()` | Checks if the stack is empty.                | $O(1)$          |

In Python, a standard `list` is commonly used as a stack:
```python
stack = []
stack.append(1)  # push
stack.append(2)
top = stack[-1]  # peek
val = stack.pop() # pop
```

## Real-world Examples
- **Browser History**:
- **Undo/Redo**: Most text editors use a stack to keep track of changes.
- **Function Calls**: Compilers use a "Call Stack" to manage function execution and local variables.

---



---

# Pattern 1: Matching and Nesting

The most common use case for a stack is when you need to "remember" an opening element until its corresponding closing element is found. This is essential for parsing nested structures.

## [Leetcode 20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

### Intuition
- As we encounter opening brackets `(`, `[`, `{`, we push them onto the stack.
- When we see a closing bracket, it **must** match the most recently seen opening bracket (the top of our stack).
- If the stack is empty when we see a closing bracket, or if the top doesn't match, the string is invalid.

### Code (Python)
```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        
        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)
        
        return not stack
```

### Complexity
- **Time Complexity:** $O(N)$ where $N$ is the length of the string.
- **Space Complexity:** $O(N)$ in the worst case (e.g., all opening brackets).

---

# Pattern 2: State Management (Min Stack)

Sometimes we need a stack to support standard operations plus a special utility, like finding the minimum element in the entire stack at any moment in $O(1)$ time.

## [Leetcode 155. Min Stack](https://leetcode.com/problems/min-stack/)

### Intuition
- A single stack can't give us the minimum in $O(1)$ without extra space because if we pop the current minimum, we need to know what the *next* minimum is.
- **Approach:** Maintain a secondary stack (`min_stack`) that stores the minimum value at each "level" of the main stack.

### Code (Python)
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

---

# Advanced Preview: Monotonic Stack

A **Monotonic Stack** is a specialized stack where elements are always sorted (either increasing or decreasing). It is extremely powerful for finding the **"next greater element"** or **"next smaller element"** in an array in $O(N)$ time, which often replaces $O(N^2)$ brute force solutions.

We will cover this pattern in depth in a dedicated chapter.

---

# Summary Cheat Sheet

| Situation                              | Data Structure  |
| :------------------------------------- | :-------------- |
| Need to reverse something              | Stack           |
| Need to match nested pairs             | Stack           |
| Need to remember the most recent state | Stack           |
| Need to find "Next Greater Element"    | Monotonic Stack |

---

# Chapter Outline

- **Stack Introduction** (This post)
- **Queue Implementation using Stacks**
- **Monotonic Stack Mastery**
- **Expression Parsing (RPN, Calculators)**


## [Leetcode 1475: Final Prices With a Special Discount in a Shop](https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/description/)
U 
### Intuition
- A bruteforce is definitely $O(N^2)$
- Key to O(N): do not look forward. look backward. that lets us use stack.
- For each element, we look back for a larger element. We want the first larger element. 

### solution

```python
class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        # Create a copy of prices array to store discounted prices
        result = prices.copy()

        stack = deque()

        for i in range(len(prices)):
            # Process items that can be discounted by current price
            while stack and prices[stack[-1]] >= prices[i]:
                # Apply discount to previous item using current price
                result[stack.pop()] -= prices[i]
            # Add current index to stack
            stack.append(i)

        return result
```
### Reference
- [Leedcode editorial](https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/solutions/6154427/final-prices-with-a-special-discount-in-s7t8g/)


Note: If you are unfamiliar with the workings of monotonic stacks, try out these problems to practice:

496. Next Greater Element I 🔗
503. Next Greater Element II 🔗
739. Daily Temperatures 🔗
For a more comprehensive understanding of stacks, check out the Stack Explore Card 🔗. This resource provides an in-depth look at the stack data structure, explaining its key concepts and applications with a variety of problems to solidify understanding of the pattern.
# References
- [Python Stacks - Python Tutorial for Absolute Beginners | Mosh](https://youtu.be/NKmasqr_Xkw?si=mXpU5YSSdQjSynaw)