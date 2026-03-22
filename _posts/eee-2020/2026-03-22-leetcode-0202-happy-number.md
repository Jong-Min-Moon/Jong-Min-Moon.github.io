---
layout: distill
title: "Leetcode 202: Happy Number"
description: "Determining if a number is a happy number using Hash Set and Two Pointers techniques."
tags: algorithms math two-pointers hash-table
categories: eee-2020
date: 2026-03-22
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/happy-number/).

- If 1 occurs, then the next number is again 1. So it is easy to detect if the number is happy.
- However, if the number is not happy, it will fall into a cycle. We need to detect the cycle.
- A no-brainer for loop dection is a hasp map. Linear complexity for both time and space. By linear it means linear in loop length, not the list length. So the loop can be very long. 

# Hash Set Approach

- As we repeatedly apply the process of summing the squares of the digits, the number will either reach 1 or fall into a cycle.
- A cycle means that the number will eventually repeat itself. Thus, we can use a hash set to keep track of the numbers we have already seen.
- If the current number is not in the hash set, we add it. If it is already in the hash set, it indicates a cycle, meaning the number is not happy.

## Algorithm

- Create an empty set `seen`.
- While `n` is not 1 and `n` is not in `seen`:
  - Add `n` to `seen`.
  - Calculate the sum of the squares of its digits and update `n` with this new value.
- If `n` becomes 1, return `true` (it is a happy number). Otherwise, if it loops (found in `seen`), return `false`.

## My Solution

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def get_next(number):
            total_sum = 0
            while number > 0:
                number, digit = divmod(number, 10)
                total_sum += digit ** 2
            return total_sum

        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = get_next(n)

        return n == 1
```

## Complexity Analysis

- **Time Complexity**: $O(\log n)$. Finding the next number costs $O(\log n)$ operations since the number of digits in a number $n$ is given by $\log_{10} n$. We also need to consider the number of steps it takes to reach 1 or cycle. It is known that the number of steps is well bounded.
- **Space Complexity**: $O(\log n)$. The space complexity is based on the maximum number of numbers we put in our set before reaching 1 or a cycle, which is also bounded.

# Two Pointers Approach

- The cycle finding part of this problem is conceptually identical to [Leetcode 141: Linked List Cycle](https://jong-min.org/blog/2018/leetcode-0141-linked-list-cycle/).
- We can view each number as a node in a linked list, where the next node is the result of summing the squares of the digits.
- We can use Floyd's Cycle-Finding Algorithm (Fast and Slow Pointers) to detect the cycle.
- The slow pointer moves one step at a time, while the fast pointer moves two steps. If there is a cycle, the fast pointer will eventually catch up to the slow pointer.

## Algorithm

- Initialize `slow_runner` to `n` and `fast_runner` to the next number of `n`.
- While `fast_runner` is not 1 and `slow_runner` != `fast_runner`:
  - Move `slow_runner` forward by one step.
  - Move `fast_runner` forward by two steps.
- If `fast_runner` reaches 1, then the number is happy (`return true`). Otherwise, if they intersect not at 1, a cycle exists (`return false`).

## My Solution

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def get_next(number):
            total_sum = 0
            while number > 0:
                number, digit = divmod(number, 10)
                total_sum += digit ** 2
            return total_sum

        slow_runner = n
        fast_runner = get_next(n)
        while fast_runner != 1 and slow_runner != fast_runner:
            slow_runner = get_next(slow_runner)
            fast_runner = get_next(get_next(fast_runner))
            
        return fast_runner == 1
```

## Complexity Analysis

- **Time Complexity**: $O(\log n)$. The time it takes to compute the next number is $O(\log n)$. The distance between the fast and slow runners decreases by 1 at each step, taking a bounded number of steps to meet.
- **Space Complexity**: $O(1)$. We only need two pointers to keep track of the current values, thus it uses $O(1)$ extra space.

# References
- https://leetcode.com/problems/happy-number/
- https://www.youtube.com/watch?v=ljz85bxOYJ0
- https://www.youtube.com/watch?v=1x2XPCR2YHI