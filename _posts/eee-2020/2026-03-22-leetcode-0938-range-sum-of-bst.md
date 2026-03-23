---
layout: distill
title: "Leetcode 938: Range Sum of BST"
description: "Calculating the sum of all nodes in a given range by traversing a Binary Search Tree."
tags: algorithms tree binary-search-tree depth-first-search
categories: eee-2020
date: 2026-03-22
featured: false
project: eee-2020
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

The original problem is [here](https://leetcode.com/problems/range-sum-of-bst/).

# In-order traversal approach
- BST can be thought of as a sorted array, because in-order traversal of a BST visits the nodes in ascending sorted order.

- So we can use in-order traversal to traverse the tree in sorted order.
- Then it is easy to check if the node is in the range `[low, high]`.

 
# Depth-First Search (DFS) Approach

- The easiest way to solve this is to traverse the entire tree and check if every node falls within the range `[low, high]`. However, this runs in $O(n)$ time regardless of the range as it checks every node.
- We can optimize this by taking advantage of the **Binary Search Tree (BST) property**:
  - The left child of a node is strictly **less than** the node's value.
  - The right child of a node is strictly **greater than** the node's value.
- This property enables us to skip (or prune) entire branches of the tree that cannot possibly contain values in our target range, vastly improving the average time complexity!

## Algorithm

- We can use a recursive depth-first search (DFS) function `dfs(node)`.
- **Base Case:** If the node is `None`, there's no value to add, so return `0`.
- **Recursive Step:**
  - If the `node.val` is between `low` and `high` (inclusive), we add `node.val` to our running sum. We then recursively call `dfs` on **both** the left and right children, because valid values might exist on both sides.
  - If the `node.val` is strictly **less** than `low`, we don't need to search the left subtree anymore because all values there will also be less than `low`. We simply return the result of `dfs` on the **right** child.
  - If the `node.val` is strictly **greater** than `high`, we don't need to search the right subtree because those values are even greater. We simply return the result of `dfs` on the **left** child.

## My Solution

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if root is None:
            return 0
        if (root.val < low):
            left_sum = 0
        else:
            left_sum = self.rangeSumBST(root.left, low, high)
        if (root.val > high):
            right_sum = 0
        else:
            right_sum = self.rangeSumBST(root.right, low, high)
        if (root.val < low) or (root.val > high):
            myself = 0
        else:
            myself = root.val

        return myself + left_sum + right_sum 
```

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        if not root:
            return 0
            
        # If the value is strictly less than low, skip the left subtree
        if root.val < low:
            return self.rangeSumBST(root.right, low, high)
            
        # If the value is strictly greater than high, skip the right subtree
        if root.val > high:
            return self.rangeSumBST(root.left, low, high)
            
        # If it is in range, include the node and check both subtrees
        return root.val + \
               self.rangeSumBST(root.left, low, high) + \
               self.rangeSumBST(root.right, low, high)
```

## Complexity Analysis

- **Time Complexity:** $O(n)$ in the worst case, where $n$ is the number of nodes in the BST. This happens if every node in the tree falls into the range `[low, high]`. On average, however, the time complexity will be much better than $O(n)$ because the BST property allows us to prune many branches.
- **Space Complexity:** $O(n)$ in the worst case for the recursion stack if the tree is heavily skewed (like a singly linked list). If the tree is balanced, the space complexity is bounded by the tree's height, leading to $O(\log n)$.




 

# References
- https://leetcode.com/problems/range-sum-of-bst/
- Range Sum of BST - Leetcode 938 - Python
 (https://youtu.be/uLVG45n4Sbg?si=DMU8T2_1CEiwSwQd)