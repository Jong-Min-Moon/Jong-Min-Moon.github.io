---
layout: distill
title: "Leetcode 141: Linked List Cycle"
description: "Detecting a cycle in a linked list using Floyd's Tortoise and Hare algorithm."
tags: algorithms linked-list two-pointers hash-table
categories: data-structure-algorithm
date: 2018-09-20
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/linked-list-cycle/).

# Hash Set approach
- If there is no cycle, it is easy to recognize it by linear going through the list.
- if there is a cycle, we will go infinitely. We don't know the length of the list so we will just think that 'oh this list is really wrong'. We need some trick to detect that we are looping.
- We use hash map and use the node itself as a key. That's the beauty of hash map: anything can be a key. We don't use the value of the node because there can be a duplicate value.

## Algorithm

1. Initialize an empty hash set to store visited nodes.
2. Traverse the linked list starting from the head.
3. For each node, check if it is already in the hash set.
   - If yes, a cycle is detected, return True.
   - If no, add the node to the hash set and move to the next node.
4. If the end of the list is reached (None), no cycle exists, return False.

## My solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        nodemap = {}
        node_now = head
        while node_now:
            if node_now in nodemap:
                return True
            nodemap[node_now] = True
            node_now = node_now.next
        return False
```

## Complexity Analysis

- **Space Complexity**: $O(N)$. In the worst-case scenario where the exact valid array bounds pair is found clustered at the absolute end tail of the array, we would functionally log almost exactly $n-1$ discrete elements tracking into our active hash map array index limit.
- **Time Complexity**: $O(N)$. We strictly traverse the list measuring $n$ elements precisely once. Because searching dynamically for a functional key within a foundational Python dictionary implementation (`in seen`) resolves in constant $O(1)$ average boundaries, the heavy geometric loop operation boils entirely down to one clean linear array scan.

# Two Pointers approach
- We can completely optimize the memory cost down to $O(1)$ by borrowing a beautifully simple two-pointer concept known as **Floyd's Tortoise and Hare algorithm**.
- Imagine two runners on a track. One runner is fast, and the other is slow. If the track is a straight line, the fast runner will hit the finish line and the race ends. However, if the track is a closed circle (a cycle), the fast runner will eventually "lap" and physically intersect with the slow runner from behind.
- We map this into our list using two pointers:
  - `slow` pointer moves $1$ step at a time.
  - `fast` pointer moves $2$ steps at a time.

## Algorithm

1. Initialize `slow` and `fast` pointers synchronously at the `head` of the linked list.
2. Loop exclusively while `fast` and `fast.next` are valid nodes (if either is `None`, the list possesses a finite tail and therefore cannot be cyclical).
3. Step `slow` forward by one node (`slow = slow.next`).
4. Step `fast` forward by two nodes (`fast = fast.next.next`).
5. After updating, check if `slow == fast`. If they occupy the same node in memory, return `True`.
6. If the `while` loop cleanly exhausts, return `False`.

## My solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        
        # Traverse until the fast pointer exhausts the list length
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            # The hare caught up to the tortoise!
            if slow == fast:
                return True
                
        return False
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We strictly utilize two lightweight tracker nodes (`slow` and `fast`), slashing the heavy mapping footprint of the $O(N)$ Hash Set approach.
- **Time Complexity**: $O(N)$. If there is no cycle, the fast pointer reaches the list boundaries naturally in precisely $N/2$ steps. If there actually is a cycle, the cyclic distance between the two pointers never exceeds $N$, and since the fast pointer functionally closes that gap by exactly $1$ node per structural loop step, it terminates safely in $\le N$ time.

# References
- https://www.youtube.com/watch?v=gBTe7lFR3vc