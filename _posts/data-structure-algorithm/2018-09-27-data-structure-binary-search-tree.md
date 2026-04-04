---
layout: distill
title: "Data Structures: Binary Search Tree"
description: "A node-based binary tree data structure with properties that make it highly efficient for searching, inserting, and deleting elements."
tags: data-structures binary-search-tree tree algorithms
categories: data-structure-algorithm
date: 2018-09-27
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Basic Idea
- Binary search tree (BST) stores elements, with no duplicates, that supports:
    - `insert(x)`
    - `delete(x)`
    - `find(x)`
    - `traversal`
        - `map`
        - `iter`
        - ..
- each element has a key (always a number)  so that elements can be compared.
- It is designed to allow fast lookup, addition, and removal of items, and can be used to implement either dynamic sets of items or lookup tables. Using BST, we can build other data structures such as:
    - set
    - dictionary
    - map
- The advangate of BST is SPEED. Insert, delete, find in O(h), h is height, usaully log n order.

## Definition
- BST consists of nodes.
- Each node has at most two children, referred to as the left child and the right child.
- The fundemental property is called 'Binary search tree property': `left < root < right` (not <= or >=, because it does not allow duplicates)
- This property makes operations highly efficient, resembling binary search in a sorted array, but with the added benefit of dynamic insertion and deletion.

# Operations

- **Search / Insert / Delete:**
    - these operations are sequences of comparisons, so on average $O(\log n)$ comparisons are needed.
  - **Average Case:** $O(\log n)$. If the tree is reasonably balanced, each step down the tree cuts the search space in half.
  - **Worst Case:** $O(n)$. If the tree becomes entirely skewed (e.g., elements are inserted in already sorted order), it effectively degrades into a singly linked list.
- **Space Complexity:** $O(n)$ to store $n$ elements. The call stack for recursive operations might take up to $O(h)$ space, where $h$ is the height of the tree.
- *Self-balancing* binary search trees (like AVL trees or Red-Black trees) automatically keep their height minimal, guaranteeing $O(\log n)$ time for basic operations even in the worst case.

## Delete
- This is the trickiest operation. Requires recursions.
- three cases: 0, 1, 2 children (0 children = leaf node)
- 0 child: just remove the node. Base case.
- 1 child: replace the node with its child. Base case.
- 2 children: recursion.
    we have to do one of the following two traversals:
    - find the in-order successor (the smallest node in the right subtree), or
    - find the in-order predecessor (the largest node in the left subtree)

    - replace the node with the successor or predecessor.
    - Remove the successor or predecessor from the tree. This calls for another delete operation.
    - Recursion goes on until it reaches the node with 0 or 1 child.

# Traversal

## Depth-First Search (DFS)
- This method is classified with respect to order between subtrees and the root. 
- Subtrees call recursions so they are expensive. Node is usually cheap.
- Also, root note is always physically visited first. But in traversals visit means some operation, such as printing or computing.
### Post-order Traversal
Many problems in BST is solved by this traversal. The general idea is as follows:
1. Finding one or more base cases
2. Calling the same function on the left subtree
3. Calling the same function on the right subtree
4. Combining the results

The root is visited after visiting the left and right subtrees, because the results should be combined. So we do the expensive operations first.

### treeSum
A very easy example of traversal is to find the sum of all nodes in a tree.

```python
def treeSum(root):
    if root is None:
        return 0
    return root.val + treeSum(root.left) + treeSum(root.right)
```
Recursion keeps going down until it reaches the left most node and then next the base case (left child of the leaf is `None`)

### treeMax

```python
def treeMax(root):
    if root is None:
        return -float('inf')
    return max(root.val, treeMax(root.left), treeMax(root.right))
```

### treeHeight

```python
def treeHeight(root):
    if root is None:
        return 0
    return 1 + max(treeHeight(root.left), treeHeight(root.right))
```

### existsInTree

```python
def existsInTree(root, target):
    if root is None:
        return False
    if root.val == target:
        return True
    return existsInTree(root.left, target) or existsInTree(root.right, target)
```

### reverseTree
Create a mirror image of the tree.
```python
def reverseTree(root):
    if root is None:
        return
    else:
        reverseTree(root.left)
        reverseTree(root.right)
        root.left, root.right = root.right, root.left
    return root
```

## In-order Traversal
- `left -> root -> right`. 
- Because of the BST property, an in-order traversal of a BST visits the nodes in **ascending sorted order**.
- This allows us to think of a BST as a sorted array.
- Complexity: $O(n)$.

## Pre-order Traversal
- `root -> left -> right`. Often used for copying a tree.


# Implementation in Python

Below is a basic implementation of a Binary Search Tree node and some common operations like insert and search:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
            return
        
        curr = self.root
        while True:
            if val < curr.val:
                if not curr.left:
                    curr.left = TreeNode(val)
                    break
                curr = curr.left
            else:
                if not curr.right:
                    curr.right = TreeNode(val)
                    break
                curr = curr.right

    def search(self, val):
        curr = self.root
        while curr:
            if val == curr.val:
                return True
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return False
```

# References
- Binary Search Trees (BST) Explained in Animated Demo
 (https://youtu.be/mtvbVLK5xDQ?si=USIG2kMLdr2hrIhE)
- Data Structures: Binary Search Tree (https://youtu.be/i_Q0v_Ct5lY?si=1LRwlMGZX_fTdIOo)
- How to solve (almost) any binary tree coding problem
 (https://youtu.be/s2Yyk3qdy3o?si=79XX6gvPli3loC_P)
- Post-order tree traversal in 2 minutes
 (https://youtu.be/4zVdfkpcT6U?si=E4uA3Mv6oAnRLMxV)