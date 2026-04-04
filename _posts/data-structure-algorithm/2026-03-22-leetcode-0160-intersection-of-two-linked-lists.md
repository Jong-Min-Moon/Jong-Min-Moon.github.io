---
layout: distill
title: "Leetcode 160: Intersection of Two Linked Lists"
description: "Finding the node at which the intersection of two singly linked lists begins using the Two Pointers technique."
tags: algorithms linked-list two-pointers
categories: data-structure-algorithm
date: 2026-03-22
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/intersection-of-two-linked-lists/).

# Hash map approach
- The problem is very similar to [Leetcode 141: Linked List Cycle](https://jong-min.org/blog/2018/leetcode-0141-linked-list-cycle/).
- Detecting overlap is a look-up operation. If we can do one lookup in O(1) time, we can solve this problem in O(N+M) time.

## Algorithm
- Traverse the first list and store all the nodes in a hash map.
- Then, traverse the second list and check if the node is in the hash map.
- If it is, we have found the intersection node. Return that node.
- If we reach the end of the second list without finding the intersection node, return `None` (`null` object in Java).

## My solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        map_a = {}
        node_a_now = headA
        while node_a_now:
            map_a[node_a_now] = True
            node_a_now = node_a_now.next
        node_b_now = headB
        while node_b_now:
            if node_b_now in map_a:
                return node_b_now
            node_b_now = node_b_now.next
        return None
```

# Two Pointers Approach

- The space complexity of the hash map approach is O(N+M). Can we do better?
- If there exists an interecation, we can think of the two lists as
  - A = A' + C
  - B = B' + C
  - where C is the common part of the two lists.
- Therefore if we treverse A and B in two ways:
  - A -> B: we traverse A' + C + B' + C
  - B -> A: we traverse B' + C + A' + C
- A' + C + B' and B' + C + A' have the same length. Therefore if we treverse A and B in two ways, we will reach the intersection node at the same time (the second C part)
- If there is no intersection. A = A', B = B'. A' + B' and B' + A' have the same length. Therefore if we treverse A and B in two ways, we will reach the end of the lists at the same time (None).

## Algorithm

- **Pointers Initialization:** Set two pointers, `pA` and `pB`, pointing to `headA` and `headB` respectively.
- **Traversal:** Move both pointers one step at a time.
- **Switching Tracks:** 
  - When `pA` reaches the end of list A, redirect it to the head of list B.
  - When `pB` reaches the end of list B, redirect it to the head of list A.
- **Intersection:** If the two lists intersect, pointers `pA` and `pB` will eventually meet at the intersection node. For simplicity of the algrithm, do not stop at the first intersection because to do that we need to check the intersection at every step. Rather, just go on to the end and return the last node on intersection.
- **No Intersection:** If the lists do not intersect, both pointers will eventually reach the end of the switched lists at the same time and both become `None`. The loop will terminate, and we can safely return `None`.

## My solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        if not headA or not headB:
            return None
            
        pA, pB = headA, headB
        
        while pA != pB:
            # If pointer reaches the end, switch to the other list's head
            # Otherwise, move to the next node
            pA = pA.next if pA else headB
            pB = pB.next if pB else headA
            
        return pA
```

## Complexity Analysis

- **Space Complexity**: $O(1)$. We only use two pointers (`pA` and `pB`), which requires constant extra space regardless of the size of the linked lists.
- **Time Complexity**: $O(N + M)$, where $N$ and $M$ are the lengths of the two linked lists. In the worst-case scenario, each pointer traverses both lists exactly once before meeting at the intersection node or `None`.

# References
- https://www.youtube.com/@CodingNinjaExAmazon?sub_confirmation=1

