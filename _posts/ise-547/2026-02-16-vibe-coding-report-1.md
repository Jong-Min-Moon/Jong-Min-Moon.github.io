---
layout: distill
title: "Vibe Coding Report 1: Word Frequency Analyzer"
description: "A report on generating a Word Frequency Analyzer using AI prompts and iterative refinement."
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

### Prompt 1 (Gemini 3 Pro)
> I am going to do vibe coding and I want you to help me write the first prompt. The problem is writing a python code that does:
> 
> **Problem 1: Word Frequency Analyzer**
> Write a program that takes in a block of text and outputs the 10 most frequent words, along with their counts. Ignore capitalization and punctuation. If two words have the same count, break ties by alphabetical order of the word. Return exactly k items if there are at least k unique words
> 
> The input format examples are:
> *   **Input 1:** "The quick brown fox jumps over the lazy dog. The dog wasn’t amused; the fox was."
> *   **Input 2:** "Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions."
> *   **Input 3:** "To be, or not to be—that is the question: Whether 'tis nobler in the mind to suffer..."

### Prompt 2 (Cursor)
> **Role & Objective:** Act as an expert Python developer. Write a highly optimized, clean, and well-documented Python function that acts as a Word Frequency Analyzer.
> 
> **Function Signature:** `def analyze_word_frequency(text: str, k: int = 10) -> list[tuple[str, int]]:` 
> 
> **Core Requirements:**
> *   **Parse the Text:** Process the input block of text and count the frequency of each word.
> *   **Normalization:** Ignore capitalization (treat "The" and "the" as identical).
> *   **Punctuation:** Remove all punctuation. (Note: Please handle contractions like "wasn't" or "can't" by keeping them as a single word without the apostrophe, e.g., "wasnt", OR specify if you prefer splitting them).
> *   **Sorting & Tie-Breaking:** Sort the output descending by frequency. If two or more words have the exact same count, break the tie by sorting those words in ascending alphabetical order.
> *   **Output Limit:** Return exactly k items as a list of tuples (word, count). If the text contains fewer than k unique words, return all available unique words sorted by the same rules.
> 
> **Test Cases to validate against:**
> *   Input 1: "The quick brown fox jumps over the lazy dog. The dog wasn’t amused; the fox was."
> *   Input 2: "Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions."
> *   Input 3: "To be, or not to be—that is the question: Whether 'tis nobler in the mind to suffer..."
> 
> Please provide the complete Python code, including the collections or re modules if you use them, and write a quick test block at the bottom to run the three inputs.

### Prompt 3 (Gemini 3 Pro)
> The cursor has generated a python code. Now write a prompt that orders it to write a test code: For each test case provided , it should clearly list the input you used and the exact output the program produced.
> 
> the inputs are:
> *   Input 1: "The quick brown fox jumps over the lazy dog. The dog wasn’t amused; the fox was."
> *   Input 2: "Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions."
> *   Input 3: "To be, or not to be—that is the question: Whether 'tis nobler in the mind to suffer..."

### Prompt 4 (Cursor)
> **Objective:**
> Write a test script to validate the word frequency function we just created. Do not use a silent testing framework like unittest; instead, write a script that runs the function against specific inputs and prints the results clearly to the console.
> 
> **Formatting Requirements:**
> For each test case, execute the function with k=10. The terminal output for each test case must be heavily formatted and clearly list both the raw input and the exact output. Use print statements to format it exactly like this example:
> 
> ```text
> ========================================
> TEST CASE 1
> ========================================
> INPUT:
> "The quick brown fox jumps over the lazy dog. The dog wasn’t amused; the fox was."
> 
> OUTPUT:
> [('the', 4), ('dog', 2), ('fox', 2), ('amused', 1), ('brown', 1), ...]
> ```
> 
> **The Test Inputs:**
> Please implement this for the following three inputs:
> *   Input 1: "The quick brown fox jumps over the lazy dog. The dog wasn’t amused; the fox was."
> *   Input 2: "Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions."
> *   Input 3: "To be, or not to be—that is the question: Whether 'tis nobler in the mind to suffer..."

### Prompt 5 (Gemini 3 Pro)
> Summarize the logic of the following program. Then, comment on how the program could be improved. give me a two-paragraph summary.

---

## B. Final Generated Program

### `word_frequency_analyzer.py` (Main Python Code)

```python
"""
Word Frequency Analyzer

Parses text, normalizes words (lowercase, no punctuation), counts frequencies,
and returns the top-k (word, count) pairs sorted by count descending with
alphabetical tie-breaking.
"""

import re
from collections import Counter

def analyze_word_frequency(text: str, k: int = 10) -> list[tuple[str, int]]:
    """
    Analyze word frequency in the given text and return the top-k words.

    Words are normalized: lowercased and stripped of punctuation. Contractions
    (e.g., "wasn't", "can't") are kept as single tokens with the apostrophe
    removed ("wasnt", "cant").

    Args:
        text: Input string to analyze.
        k: Maximum number of (word, count) pairs to return (default 10).

    Returns:
        List of up to k tuples (word, count), sorted by count descending.
        Ties in count are broken by word ascending alphabetically.
        Fewer than k items if the text has fewer unique words.
    """
    if not text or not text.strip():
        return []

    # Normalize: lowercase for case-insensitive counting
    normalized = text.lower()

    # Handle contractions: remove apostrophes so "wasn't" -> "wasnt", "'tis" -> "tis"
    normalized = normalized.replace("'", "")

    # Remove all remaining punctuation (keep only letters, digits, spaces)
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)

    # Split on whitespace and drop empty tokens
    words = normalized.split()

    if not words:
        return []

    # Count occurrences
    counts = Counter(words)

    # Sort: primary key = count descending, secondary key = word ascending
    sorted_items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    return sorted_items[:k]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [
        (
            "The quick brown fox jumps over the lazy dog. The dog wasn't amused; the fox was.",
            10,
        ),
        (
            "Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions.",
            10,
        ),
        (
            "To be, or not to be—that is the question: Whether 'tis nobler in the mind to suffer...",
            10,
        ),
    ]

    for i, (text, k) in enumerate(test_cases, start=1):
        print(f"--- Input {i} (k={k}) ---")
        result = analyze_word_frequency(text, k)
        for word, count in result:
            print(f"  {word!r}: {count}")
        print()
```

### `test_word_frequency.py`

```python
"""
Test script for analyze_word_frequency.
Runs the function against three fixed inputs with k=10 and prints
formatted results to the console (no unittest).
"""

from word_frequency_analyzer import analyze_word_frequency

K = 10

INPUT_1 = "The quick brown fox jumps over the lazy dog. The dog wasn't amused; the fox was."
INPUT_2 = "Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions."
INPUT_3 = "To be, or not to be—that is the question: Whether 'tis nobler in the mind to suffer..."


def run_test(case_num: int, text: str) -> None:
    print("========================================")
    print(f"TEST CASE {case_num}")
    print("========================================")
    print("INPUT:")
    print(repr(text))
    print()
    result = analyze_word_frequency(text, k=K)
    print("OUTPUT:")
    print(result)
    print()


if __name__ == "__main__":
    run_test(1, INPUT_1)
    run_test(2, INPUT_2)
    run_test(3, INPUT_3)

```

---

## C. Inputs and Outputs

```text
========================================
TEST CASE 1
========================================
INPUT:
"The quick brown fox jumps over the lazy dog. The dog wasn't amused; the fox was."

OUTPUT:
[('the', 4), ('dog', 2), ('fox', 2), ('amused', 1), ('brown', 1), ('jumps', 1), ('lazy', 1), ('over', 1), ('quick', 1), ('was', 1)]

========================================
TEST CASE 2
========================================
INPUT:
"Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions."

OUTPUT:
[('data', 4), ('bricks', 1), ('cant', 1), ('clay', 1), ('decisions', 1), ('drives', 1), ('i', 1), ('make', 1), ('said', 1), ('sherlock', 1)]

========================================
TEST CASE 3
========================================
INPUT:
"To be, or not to be—that is the question: Whether 'tis nobler in the mind to suffer..."

OUTPUT:
[('to', 3), ('be', 2), ('the', 2), ('in', 1), ('is', 1), ('mind', 1), ('nobler', 1), ('not', 1), ('or', 1), ('question', 1)]
```

---

## D. AI-Generated Analysis

The program calculates the top k most frequent words in a string by systematically cleaning, counting, and sorting the text. It begins by converting the entire input to lowercase and manually stripping out apostrophes so that contractions are merged into single alphanumeric tokens (e.g., "wasn't" becomes "wasnt"). Next, it uses a regular expression to replace all remaining non-alphanumeric characters with spaces, which safely removes punctuation and treats characters like em-dashes as word separators. After splitting this sanitized string into a list of words, it tallies their frequencies using `collections.Counter`. Finally, the script sorts the dictionary items using a custom lambda function—prioritizing highest counts first (`-x[1]`), while resolving ties alphabetically (`x[0]`)—and returns the top k slice.

While the script is highly effective for basic English text, it could be improved for better scalability and internationalization. The current regular expression `[^a-z0-9\s]` strips out all non-ASCII characters, meaning accented words (like "café" or "naïve") will be improperly fractured; swapping this for a Unicode-aware regex would make the parser much more robust. Additionally, the current sorting method evaluates the entire vocabulary of the text at once (`sorted(counts.items(), ...)`), which is inefficient for massive datasets. While `Counter(words).most_common()` doesn't natively support alphabetical tie-breaking, implementing a custom priority queue (using the `heapq` module) to maintain only the top k elements in memory would significantly improve the algorithm's performance on book-length inputs.
