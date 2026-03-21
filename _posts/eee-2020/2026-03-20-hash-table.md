---
layout: distill
title: "Data Structures: Hash Table"
description: "A foundational dictionary data structure allowing for $O(1)$ average associative lookups."
tags: data-structures hash-table dictionary arrays
categories: eee-2020
date: 2018-09-20
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Basic Idea
- Hash table is a key-value lookup.
- This means that it saves the data as key-value pairs very quickly, and fetch the data for given key very quickly.
- Importantly, keys are not necessarily integers or contiguous. They can be strings, objects, etc (for integer keys, arrays are already good enough)
- good for saving dynamic set of data
- For coding test, just remember that it does insert, delete, search in O(1) on average. Especially good for search!
- It uses a hash function to convert a key into an integer index (or hash code) and link it to the value.

# Hash Function and Collisions

- A hash function puts input -> hash code -> index
- after each mapping, we go to much smaller spaces
- this smaller space is the punchline; it boosts the speed
- However, since the number of possible keys is typically far larger than the number of buckets, **hash collisions**—where two different keys generate the exact same integer index—are inevitable.
- A common solution for collisions is chaning, which is to use linked list at each bucket when a collision occurs.

# Implementation in Python

In Python, the built-in `dict` (dictionary) and `set` objects are heavily optimized implementations of hash tables:

```python
# Initialization
my_hash_map = {}

# Insert - O(1) average time
my_hash_map["apple"] = 5
my_hash_map["banana"] = 10

# Lookup - O(1) average time
if "apple" in my_hash_map:
    print(my_hash_map["apple"]) # Output: 5

# Delete - O(1) average time
del my_hash_map["banana"]
```

# References
- https://youtu.be/shs0KM3wKv8?si=vc9605Sc9Gavtjha