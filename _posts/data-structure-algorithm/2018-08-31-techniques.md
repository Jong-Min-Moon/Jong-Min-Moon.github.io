---
layout: distill
title: "Techniques"
description: "Techniques"
tags: algorithms two-pointers
categories: data-structure-algorithm
date: 2018-08-31
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---


# Two pointers

## Same Direction Traversal
One always moves, another sometimes moves

### One array
1. [Leetcode 283: Move Zeroes](https://jong-min.org/blog/2018/move-zeroes/)
2. [Leetcode 27: Remove Element](https://leetcode.com/problems/remove-element/description/) exactly same as 283: move zeros. compare to val instead of 0.
3. [Leetcode 26: Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/) exactly same as Leetcode 283: Move Zeroes, but here we compare the current element to the previous element. Also, start from index 1 rather than 0. one liner: include number the first time we see it, becuase last time is not clear.
4. [Leetcode 905: Sort Array by Parity](https://leetcode.com/problems/sort-array-by-parity/description/): two-pass algorithm with new array. Alternatively, quicksort for in-place.

### Two arrays
1. [Leetcode 392: Is Subsequence](https://jong-min.org/blog/2018/is-subsequence/): end cases for each of s and t. use while loop for two end cases. A deep problem with many solutions.




## Squeezing
1. [Leetcode 125. Valid Palindrome](https://jong-min.org/blog/2018/leedcode-125-valid-palindrome/): cleaned_s = ''.join(c.lower() for c in s if c.isalnum()) and squeezing. synchronous steps.
2. [Leetcode 977: Squares of a Sorted Array](https://jong-min.org/blog/2018/leetcode-977-squares-of-a-sorted-array/): asynchronous steps.


## Sliding windows




## Unidirectional traversal

In this approach, both pointers start at the same end of the data structure (usually the beginning) and move in the same direction:
These pointers generally serve two different but supplementary purposes. A common application of this is when we want 
- one pointer to find information (usually the right pointer),
- another to keep track of information (usually the left pointer).

## Inward traversal

This approach has pointers starting at opposite ends of the data structure and moving inward toward each other. The pointers move toward the center, adjusting their positions based on comparisons, until a certain condition is met, or they meet/cross each other. This is ideal for problems where we need to compare elements from different ends of a data structure. Palindrome is a good example of this approach.

 


### Staged traversal

In this approach, we traverse with one pointer, and when it lands on an element that meets a certain condition, we traverse with the second pointer:

> *Image represents a diagram illustrating a coding pattern, likely related to data processing or algorithm execution. The diagram shows two stages separated by a large right arrow. The first stage depicts a sequence of black dots enclosed in square brackets, representing data elements. An orange rectangular box labeled 'first' points downwards with an arrow to the second element in the sequence, indicating a process or function ('first') acting upon this specific element. The connection is shown with a dashed orange line forming a curved arc above the data sequence. The second stage, also enclosed in square brackets, shows the same data sequence but with a different transformation. A light-blue rectangular box labeled 'second' points downwards with an arrow to the second element in this new sequence, indicating a different process or function ('second') acting upon the same element. The connection is shown with a dashed light-blue line forming a curved arc above the data sequence. A third, identical orange box labeled 'first' is shown above the second stage, suggesting the 'first' process is applied again, possibly iteratively or in parallel with the 'second' process. The overall transformation shows how the initial data sequence is modified by the sequential or parallel application of the 'first' and 'second' processes.*

Similar to unidirectional traversal, both pointers serve different purposes. Here, the first pointer is used to search for something, and once found, a second pointer finds additional information concerning the value at the first pointer.

We discuss all of these techniques in detail throughout the problems in this chapter.

## When To Use Two Pointers?

A two-pointer algorithm usually requires a linear data structure, such as an array or linked list. Otherwise, an indication that a problem can be solved using the two-pointer algorithm, is when the input follows a predictable dynamic, such as a sorted array.

Predictable dynamics can take many forms. Take, for instance, a palindromic string. Its symmetrical pattern allows us to logically move two pointers toward the center. As you work through the problems in this chapter, you'll learn to recognize these predictable dynamics more easily.

Another potential indicator that a problem can be solved using two pointers is if the problem asks for a pair of values or a result that can be generated from two values.

## Real-world Example

Garbage collection algorithms: In memory compaction – which is a key part of garbage collection – the goal is to free up contiguous memory space by eliminating gaps left by deallocated (aka dead) objects. A two-pointer technique helps achieve this efficiently: a 'scan' pointer traverses the heap to identify live objects, while a 'free' pointer keeps track of the next available space to where live objects should be relocated. As the 'scan' pointer moves, it skips over dead objects and shifts live objects to the position indicated by the 'free' pointer, compacting the memory by grouping all live objects together and freeing up continuous blocks of memory.

## Chapter Outline

> *Image represents a hierarchical diagram illustrating different coding patterns categorized under the umbrella term 'Two Pointers'. A rounded rectangle at the top labeled 'Two Pointers' acts as the root node, branching down via dashed lines to three subordinate rectangular boxes representing distinct traversal types. The leftmost box, 'Inward Traversal,' lists four sub-problems: 'Pair Sum - Sorted,' 'Triplet Sum,' 'Largest Container,' and 'Is Palindrome Valid.' The rightmost box, 'Unidirectional Traversal,' contains a single sub-problem: 'Shift Zeros to the End.' Finally, the bottom box, 'Staged Traversal,' lists one sub-problem: 'Next Lexicographical Sequence.' The dashed lines indicate a hierarchical relationship, showing how each traversal type falls under the broader 'Two Pointers' category, and the listed items are specific problems solvable using that traversal technique.*

The two-pointer pattern is very versatile and, consequently, quite broad. As such, we want to cover more specialized variants of this algorithm in separate chapters, such as Fast and Slow Pointers and Sliding Windows.

https://bytebytego.com/courses/coding-patterns/two-pointers/introduction-to-two-pointers?fpr=javarevisited

https://youtu.be/QzZ7nmouLTI?si=UK9pinUIRmKT5hGp