---
layout: distill
title: "Leetcode 169: Majority Element"
description: "Finding the majority element in an array using a Hash Map frequency table."
tags: algorithms hash-table arrays taxi
categories: eee-2020
date: 2018-09-20
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/majority-element/).

# Hash Map Approach
- We first need to count the frequency of each number. $O(n)$ if we use hash map.
- If we sort after counting the frequency, it takes $O(n \log n)$.
- We can solve in $O(n)$ if we track both the **frequency** of each number and the **maximum frequency** seen so far.
- The problem asks us to find the "majority element"—an element that appears more than $\lfloor n / 2 \rfloor$ times. We can be certain that such an element always exists in the array.
- A **Hash Map** is an excellent choice to save a frequency table since we get $O(1)$ updates and lookups!


# Algorithm

- **Initialization:**
  - Create an empty hash map `count` to store our frequency table.
  - Keep track of the "best pair" using two tracker variables: `res` (the number itself) and `max_count` (the frequency of that number). Initializing these to $0$ is fine.
- **Linear Scan:**
  - We linearly scan and read the entire array.
  - For each number `n`, we safely update its count in the hash map using `.get()`: `count[n] = count.get(n, 0) + 1`. 
  - After updating the hash map for number `n`, we compare its new frequency (`count[n]`) with our current tracked `max_count`.
  - If it is strictly greater, we update our best pair: `res = n` and `max_count = count[n]`.
- **Completion:** Iteration finishes and `res` securely holds the number corresponding to the highest frequency!

*(Note: There is also an $O(1)$ space solution to this problem known as the Boyer-Moore Voting Algorithm, but using a Hash Map frequency table is a very robust general string/array counting pattern!)*

## My solution

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        count = {}
        res = 0
        max_count = 0
        
        for n in nums:
            # Update the hashmap frequency table
            count[n] = count.get(n, 0) + 1
            
            # Compare with the best pair
            if count[n] > max_count:
                res = n
                max_count = count[n]
                
        return res
```

## Complexity Analysis

- **Space Complexity**: $O(n)$. In the worst case, if there are many distinct elements, the hash map keys will scale proportionally to the distinct entries in the array.
- **Time Complexity**: $O(n)$. We do a single linear read through the array, doing $O(1)$ operations under the hood for hash map writes and lookups.
