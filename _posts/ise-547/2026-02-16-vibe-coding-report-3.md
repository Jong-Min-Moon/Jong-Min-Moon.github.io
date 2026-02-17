---
layout: distill
title: "Vibe Coding Report: Group Anagrams"
description: "A report on generating a Group Anagrams script using AI prompts and iterative refinement."
tags: distill formatting
categories: vibe-coding
date: 2026-02-16
featured: false
project: ise-547
authors:
  - name: Jongmin Mun
    url: "https://jong-min.org/"
toc:
  - name: "A. Prompts"
  - name: "B. Final Generated Program"
  - name: "C. Inputs and Outputs"
  - name: "D. AI-Generated Analysis"

_styles: >
  .fake-img {
    margin-bottom: 12px;
  }
  .fake-img p {
    text-align: center;
    margin: 12px 0;
  }
---

## A. Prompts
This time, I took one further step of prompting to improve the code.
### Prompt 1 (Gemini 3 Pro)
> I am going to do vibe coding and I want you to help me write the first prompt. The problem is writing a python code that follows the following instruction:
>
> Given a list of words, group together all words that are anagrams of each other.
> Example:
> Input: [“listen”, “silent”, “enlist”, “rat”, “tar”]
> Output: [["listen","silent","enlist"], ["rat","tar"]]
>
> The input format examples are:
> *   **Input 1:** listen silent enlist inlets google giggle rat tar art
> *   **Input 2:** dusty study night thing cat act tac tacit attic tactic
> *   **Input 3:** state taste tates seats asset teats teat set eats east
> *   (Each line can be interpreted as a space-separated list of words.)
>
> Test cases must be written with these examples and the test output should clearly format and print the input and output. Do not hardcode the test code. Rather, use a formal testing framework like pytest and allowing dynamic user inputs, but use the inputs I provided on that framework.

### Prompt 2 (Cursor)
> Act as an expert Python developer. I want you to write a clean, efficient Python script to solve the "Group Anagrams" problem, along with a robust test suite using pytest.
>
> **The Objective:** Write a function that takes a space-separated string of words, parses it into a list, and groups all words that are anagrams of each other. Example: > Input: "listen silent enlist rat tar" Output: [["listen", "silent", "enlist"], ["rat", "tar"]]
>
> **Testing Requirements:**
> 1.  Use the `pytest` framework.
> 2.  Do not just hardcode the tests sequentially. Use `@pytest.mark.parametrize` to allow for dynamic, scalable testing.
> 3.  The test cases must clearly print the input string and the resulting grouped output to the console so I can visually verify it (ensure the test uses print statements or logs that can be seen when running `pytest -s`).
> 4.  Include the ability for a user to input their own string via standard input if run as a standalone script (e.g., under `if __name__ == "__main__":`).
>
> **Use the following inputs for your parameterized tests:**
> *   Test Case 1 Input: listen silent enlist inlets google giggle rat tar art
> *   Test Case 2 Input: dusty study night thing cat act tac tacit attic tactic
> *   Test Case 3 Input: state taste tates seats asset teats teat set eats east
>
> Please provide the complete Python code, including the main logic and the pytest suite in a single file or clearly separated blocks, complete with type hinting and docstrings.

### Prompt 3 (Gemini 3 Pro)
> Summarize the logic of the following program. Then, comment on how the program could be improved. give me a two-paragraph summary.

### Prompt 4 (Cursor)
> Refactor the `group_anagrams` Python script to implement the following improvements:
>
> 1.  **Algorithmic Optimization:**
>     Update the `group_anagrams` function to use a 26-element character frequency tuple as the dictionary key instead of sorting the characters. This will optimize the time complexity per word from $O(K \log K)$ to $O(K)$. You can use `ord(char) - ord('a')` to map lowercase characters to their respective indices.
> 2.  **Type Hinting Modernization:**
>     Completely remove the `from typing import List` import. Update all type hints across the entire file—including the function signature, variable annotations, and the pytest suite—to use modern Python built-in types (e.g., `list`, `dict`, `tuple` instead of `List`, `Dict`, `Tuple`).
>
> Please ensure all existing tests still pass, the interactive `__main__` block remains functional, and the docstrings are updated to reflect the new logic.

---

## B. Final Generated Program

```python
"""
Group Anagrams: Given a space-separated string of words, group all words that are anagrams.
Includes pytest suite with parametrized tests and optional stdin input when run as script.
"""

from __future__ import annotations

from collections import defaultdict


def _char_frequency_key(word: str) -> tuple[int, ...]:
    """
    Build a 26-element tuple of letter counts (a-z) for the lowercase word.

    Uses ord(char) - ord('a') to map each letter to an index. Non-letter
    characters are ignored. O(K) per word where K = len(word).

    Returns:
        A tuple of 26 integers: count of 'a' at index 0, 'b' at 1, ..., 'z' at 25.
    """
    counts = [0] * 26
    for c in word.lower():
        if "a" <= c <= "z":
            counts[ord(c) - ord("a")] += 1
    return tuple(counts)


def group_anagrams(words_str: str) -> list[list[str]]:
    """
    Parse a space-separated string into words and group all anagrams together.

    Two words are anagrams if they have the same character frequencies (same
    count per letter a-z, ignoring case and non-letter characters). Keys are
    computed as 26-element frequency tuples in O(K) per word. Groups are
    returned in order of first occurrence; within each group, words keep
    their input order.

    Args:
        words_str: A single string of space-separated words.

    Returns:
        A list of lists; each inner list contains words that are anagrams
        of each other. Groups appear in order of first occurrence.

    Example:
        >>> group_anagrams("listen silent enlist rat tar")
        [['listen', 'silent', 'enlist'], ['rat', 'tar']]
    """
    if not words_str or not words_str.strip():
        return []

    words = words_str.split()
    # Key: 26-element frequency tuple (hashable); value: list of words with that signature
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)

    for word in words:
        key = _char_frequency_key(word)
        groups[key].append(word)

    # Return groups in order of first occurrence (iteration order of defaultdict)
    return list(groups.values())


# ---------------------------------------------------------------------------
# Pytest suite (parametrized, with visible input/output via print)
# Run with: pytest group_anagrams.py -v -s
# ---------------------------------------------------------------------------

import pytest


@pytest.mark.parametrize(
    "words_str,expected",
    [
        (
            "listen silent enlist inlets google giggle rat tar art",
            [
                ["listen", "silent", "enlist", "inlets"],
                ["google"],
                ["giggle"],
                ["rat", "tar", "art"],
            ],
        ),
        (
            "dusty study night thing cat act tac tacit attic tactic",
            [
                ["dusty", "study"],
                ["night", "thing"],
                ["cat", "act", "tac"],
                ["tacit", "attic"],
                ["tactic"],
            ],
        ),
        (
            "state taste tates seats asset teats teat set eats east",
            [
                ["state", "taste", "tates", "teats"],
                ["seats", "asset"],
                ["teat"],
                ["set"],
                ["eats", "east"],
            ],
        ),
    ],
    ids=["case_1_anagrams", "case_2_anagrams", "case_3_anagrams"],
)
def test_group_anagrams(words_str: str, expected: list[list[str]]) -> None:
    """Parametrized test: checks result and prints input/output for visual verification."""
    result = group_anagrams(words_str)
    print(f"\n  Input:  {words_str}")
    print(f"  Output: {result}")
    assert result == expected, f"Expected {expected}, got {result}"


def test_group_anagrams_empty() -> None:
    """Empty or whitespace-only input returns empty list."""
    assert group_anagrams("") == []
    assert group_anagrams("   ") == []


def test_group_anagrams_single_word() -> None:
    """Single word returns one group."""
    result = group_anagrams("hello")
    print(f"\n  Input:  hello")
    print(f"  Output: {result}")
    assert result == [["hello"]]


# ---------------------------------------------------------------------------
# Standalone script: read from stdin and print grouped anagrams
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Group Anagrams — Enter a space-separated list of words (or leave blank to exit):")
    try:
        user_input = input().strip()
    except EOFError:
        user_input = ""

    if not user_input:
        print("No input provided. Exiting.")
    else:
        result = group_anagrams(user_input)
        print(f"\nInput:  {user_input}")
        print(f"Output: {result}")
```

---

## C. Inputs and Outputs

```text
group_anagrams.py::test_group_anagrams[case_1_anagrams] 
  Input:  listen silent enlist inlets google giggle rat tar art
  Output: [['listen', 'silent', 'enlist', 'inlets'], ['google'], ['giggle'], ['rat', 'tar', 'art']]
PASSED
group_anagrams.py::test_group_anagrams[case_2_anagrams] 
  Input:  dusty study night thing cat act tac tacit attic tactic
  Output: [['dusty', 'study'], ['night', 'thing'], ['cat', 'act', 'tac'], ['tacit', 'attic'], ['tactic']]
PASSED
group_anagrams.py::test_group_anagrams[case_3_anagrams] 
  Input:  state taste tates seats asset teats teat set eats east
  Output: [['state', 'taste', 'tates', 'teats'], ['seats', 'asset'], ['teat'], ['set'], ['eats', 'east']]
PASSED
group_anagrams.py::test_group_anagrams_empty PASSED
group_anagrams.py::test_group_anagrams_single_word 
  Input:  hello
  Output: [['hello']]
PASSED
```

---

## D. AI-Generated Analysis

The updated Python script efficiently groups anagrams by replacing the previous sorting mechanism with a linear-time character-frequency counting approach. For each parsed word, it calls a helper function that tallies the occurrences of letters from 'a' to 'z' into a 26-element tuple, operating in strictly $O(K)$ time where $K$ is the word length. Because this fixed-length tuple is immutable, it serves as a perfect, hashable dictionary key in a defaultdict. As the script iterates through the input string, words sharing the same frequency signature are appended to the same list, and the grouped anagrams are ultimately returned in their original insertion order alongside a modern, fully typed test suite.

While the script is highly optimized for standard English text, its strict filtering of characters outside the lowercase 'a' to 'z' range leaves room for improvement regarding edge cases and internationalization. Because it silently ignores numbers, punctuation, and Unicode characters (like accented letters), strings with entirely different non-alphabetical characters could be incorrectly grouped together as anagrams if their base English letter counts match. To make the program universally robust, you could replace the fixed 26-element array with a `frozenset` derived from `collections.Counter(word.lower())`, which would safely and accurately hash any character from any language while maintaining excellent performance and actually shrinking the codebase.
