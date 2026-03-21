---
layout: distill
title: "Leetcode 1134: Armstrong Number"
description: "Determining if a number is an Armstrong number by extracting its digits."
tags: algorithms math
categories: eee-2020
date: 2018-09-20
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/armstrong-number/).

# Armstrong Number
- This is a very simple problem. I post this mainly to review **how to extract digits** from a number in python.
- An **Armstrong Number** (also known as a narcissistic number) is an integer that equals the sum of its own digits, each raised to the power of the number of digits. 
- For example, if $n = 153$, it has $3$ digits. The sum is $1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153$. Because $153 == 153$, it evaluates to true.
- To check this programmatically, we require three pieces of information: the individual digits, the total number of digits ($k$), and their computed sum.

- There are two primary ways to extract the digits:
  - String Conversion: no brainer. Just `str(n)`. Python's built-in type casting.
  - Mathematical Modulo: We can extract digits chronologically tracking backwards using the modulo operator (`n % 10`) and strip digits using integer division (`n // 10`).

## My solution

```python
class Solution:
    def isArmstrong(self, n: int) -> int:
        # Convert integer to string to easily count and iterate over digits
        n_str = []
        while n > 0:
            n_str.append(n % 10)
            n //= 10
        
        k = len(n_str)
        
        # Generator expression to calculate the sum of the digits raised to the power of k
        total_sum = sum(int(digit) ** k for digit in n_str)
        
        # Check if the calculated sum matches the original number
        return total_sum == n
```

## Complexity Analysis

- **Space Complexity**: $O(k)$ or $O(\log_{10} n)$. This represents the number of digits in $n$. We allocate extra memory to represent $n$ as a string array of characters. The mathematical modulo approach would optimize this to $O(1)$ constant space.
- **Time Complexity**: $O(k)$ or $O(\log_{10} n)$. We loop through the $k$ digits exactly once.

# Follow-up question: factorion
- Determine if given number is a *factorion*: a number equals to sum of factorials of its digits. For example, $145 = 1! + 4! + 5!$.
- Since we are dealing with equalities, we can use upper bound and lower bound to find a digit range to check. 
- Factorial lower bound is trivial: $1! \times k$. Number upper bound is of course larger than that. so this way is not very effective.
- Factorial upper bound is $9! \times k$. Number lower bound is $10^{k-1}$.  We can find a digit range to check. 

```python
class Solution:
    def isFactorion(self, n: int) -> bool:
        # Convert integer to string to easily count and iterate over digits
        n_str = []
        while n > 0:
            n_str.append(n % 10)
            n //= 10
        
        k = len(n_str)
        
        if 9! * k < 10**(k-1):
            return False
        # Generator expression to calculate the sum of the digits raised to the power of k
        total_sum = sum(int(digit) ** k for digit in n_str)
        
        # Check if the calculated sum matches the original number
        return total_sum == n
```
