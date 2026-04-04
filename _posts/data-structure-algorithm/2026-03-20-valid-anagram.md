---
layout: distill
title: "Leetcode 242: Valid Anagram"
description: "Checking if two strings are anagrams of each other using a Hash Map."
tags: algorithms hash-table strings taxi
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/valid-anagram/).

# Hash Map Approach
- Using two pointers is disastrously slow: $O(n^2)$.
- Sorting the strings and comparing them directly takes $O(n \log n)$ time.
- An anagram and the original word should have exactly the same frequency table (keys and values). 
- A **Hash Map** is the perfect data structure for this! It gives us $O(1)$ dynamic storage and lookup, allowing us to rapidly track character frequencies. So in total $O(n)$.


## Algorithm

- **Length Check:** If the two strings `s` and `t` do not have the same length, they cannot possibly be anagrams. Return `False` early.
- **Frequency Counting:** We create a hash map (`count`) to store character frequencies.
  - We loop through the characters of both strings.
  - For each character in `s`, we **increment** its frequency count in the hash map.
  - For each character in `t`, we **decrement** its frequency count in the same hash map.
- **Validation:** Finally, we check the values in our hash map. If every key resolves to `0`, it means `s` and `t` completely balance each other out and are valid anagrams! If any value is non-zero, they are not.

## My solution

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
            
        count = {}
        
        # Build the frequency map
        for i in range(len(s)):
            count[s[i]] = count.get(s[i], 0) + 1
            count[t[i]] = count.get(t[i], 0) - 1
            
        # Check if all counts evaluate back to 0
        for val in count.values():
            if val != 0:
                return False
                
        return True
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. Although we use a hash map, the problem dictates that the strings only contain lowercase English letters. Therefore, the size of the hash map will never exceed 26 keys, making it constant space $O(1)$.
- **Time Complexity**: $O(n)$. We iterate through the strings of length $n$ exactly once to populate the hash map, leveraging $O(1)$ constant time lookups!
