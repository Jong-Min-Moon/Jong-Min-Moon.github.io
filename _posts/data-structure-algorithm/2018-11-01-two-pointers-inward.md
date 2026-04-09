---
layout: distill
title: "Two Pointers - inward traversal"
description: "A comprehensive guide to the two-pointer algorithmic pattern"
tags: algorithms two-pointers
categories: data-structure-algorithm
date: 2018-10-01
featured: false
project: data-structure-algorithm
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---





# Easy

## [Leetcode 125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/)

### Intuition

- We need to compare left and right elements so obviously we need two pointers and they move toward the center.
- We place one pointer at the beginning (`left`) and one at the end (`right`).
- We systematically **squeeze** them towards the center, functioning as a `comparer`.
- If the characters at the `left` and `right` pointers ever mismatch, the string is not a palindrome.
- If the pointers cross each other without a mismatch, the string is a valid palindrome!

### String Handling

- First we remove blanks and non-alphanumeric characters and convert the string to lowercase using `isalnum()` and `lower()`.
- We use **list comprehension**  to **filter and format** the string.
- Finally use `''.join()` to join the filtered characters into a string.

```python
cleaned_s = ''.join(c.lower() for c in s if c.isalnum())
```

> **Note**: While filtering the string upfront is very clean, an optimized solution would do this filtering *on the fly* during the two-pointer traversal to save $O(n)$ space.

### Initialization

- `left` points to `0` (the first character).
- `right` points to `len(cleaned_s) - 1` (the last character).

### Main loop

- We use a `while` loop that continues as long as `left < right`.
- At each step, we compare `cleaned_s[left]` and `cleaned_s[right]`.
- If they are not equal, we immediately return `False`.
- If they are equal, we move `left` to the right by 1 and `right` to the left by 1 (squeezing inwards).

### Termination

- If the loop finishes without returning `False`, it means all corresponding characters matched. We then return `True`.

### My solution

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = [c.lower() for c in s if c.isalnum()]
        s = ''.join(s)

        left = 0
        right = len(s)-1
        while left < right:
            if s[left] == s[right]:
                left += 1
                right -= 1
            else:
                return False
        return True
```

## [Leetcode 977. Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/description/)

### Intuition

- The brute force approach:  squaring takes $O(N)$ time and then sorting takes $O(N \log N)$. So the total time complexity is $O(N \log N)$. 
- However, this is a stupid approach because it does not use the fact that the **original array is sorted**. The follow-up question calls for $O(N)$ time complexity.

 
- What we fear is signs; If the numbers are all positive or all negative, the problem is trivial.
- Let's assume the array contains both positive and negative numbers.
-  Since the array is pre-sorted, `nums[0]` is the negative number with the largest magnitude. `nums[n-1]` is the positive number with the largest magnitude.
- As we move the pointer inward by one index, we encounter the next largest magnitude number.
- So we can compare the absolute values of the elements at the `left` and `right` pointers. We square the larger one, place it at the result array from the end, and move the corresponding pointer inward.

### When do we stop?
- if negative or positive numbers are exhausted, the problem becomes trivial. But there's no harm in continuing the loop until the pointers cross each other.

### Code (Python)

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n  = len(nums)
        result = [0]*n
        left = 0
        right = n-1
        while left <= right:
            sq_left = nums[left]**2
            sq_right = nums[right]**2
            index_result = right-left
            if sq_left < sq_right:
                result[index_result] = sq_right
                right -=1
            else:
                result[index_result] = sq_left
                left += 1
        return result
            
```

### Complexity
- **Time Complexity:** $O(N)$ because calculating the squares and placing them in the correct spot requires exactly one pass over the array.
- **Space Complexity:** $O(N)$ because we are allocating a new array of size $N$ to store the result, as required by the problem statement.


### References
- [How to Solve Squares of a Sorted Array Efficiently in One Go!](https://youtu.be/KyKeW6PZiWo?si=apgkBtA99pbZWm-7)

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