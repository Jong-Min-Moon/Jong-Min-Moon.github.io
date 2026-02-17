---
layout: distill
title: "Vibe Coding Report: Palindrome Checker"
description: "A report on generating a Palindrome Checker using AI prompts and iterative refinement."
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
> I am going to do vibe coding and I want you to help me write the first prompt. The problem is writing a python code that follows the following instruction:
>
> Write a program that takes in a sentence and determines if it is a palindrome, ignoring capitalization, spaces, and punctuation.
> Example: “A man, a plan, a canal: Panama” → “This is a palindrome.”
>
> The input format examples are:
>
> *   **Input 1:** A man, a plan, a canal: Panama!
> *   **Input 2:** No 'x' in Nixon
> *   **Input 3:** Was it a car or a cat I saw?
>
> Test cases must be written with these examples and the test output should clearly format and print the input and output.

### Prompt 2 (Cursor)
> Act as an expert Python developer. I need a Python script that checks if a given sentence is a palindrome.
> Here are the strict requirements for the logic:
> *   The checker must completely ignore capitalization, spaces, and all punctuation. Only consider alphanumeric characters.
> *   The output should return a clean, user-friendly string, such as 'This is a palindrome.' or 'This is not a palindrome.'
>
> **Testing & Output Formatting Requirements:**
> Write a testing block that loops through a list of inputs. You must use exactly these test cases:
> 1.  "A man, a plan, a canal: Panama!"
> 2.  "No 'x' in Nixon"
> 3.  "Was it a car or a cat I saw?"
>
> When running the tests, format the console output so it clearly displays both the original input and the final evaluated output in a highly readable way. Keep the code elegant, Pythonic, and well-commented.

### Prompt 3 (Gemini 3 Pro)
> Summarize the logic of the following program. Then, comment on how the program could be improved. give me a two-paragraph summary.

---

## B. Final Generated Program

```python
"""
Palindrome checker: ignores case, spaces, and punctuation; considers only alphanumeric characters.
Returns user-friendly messages and includes a readable test runner.
"""

import re


def is_palindrome(s: str) -> bool:
    """
    Return True if the string is a palindrome when considering only alphanumeric
    characters (ignoring case, spaces, and punctuation); otherwise False.
    """
    # Keep only letters and digits, then normalize to lowercase for comparison
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return cleaned == cleaned[::-1]


def check_palindrome(s: str) -> str:
    """
    Check if the given sentence is a palindrome and return a user-friendly message.
    """
    if is_palindrome(s):
        return "This is a palindrome."
    return "This is not a palindrome."


def run_tests():
    """Run the required test cases and print original input and result in a readable format."""
    test_cases = [
        "A man, a plan, a canal: Panama!",
        "No 'x' in Nixon",
        "Was it a car or a cat I saw?",
    ]
    width = 60  # For consistent column alignment

    print("=" * (width * 2 + 9))
    print("PALINDROME CHECKER — Test Results")
    print("=" * (width * 2 + 9))

    for i, sentence in enumerate(test_cases, start=1):
        result = check_palindrome(sentence)
        print(f"\nTest {i}:")
        print(f"  Input:  {sentence}")
        print(f"  Output: {result}")

    print("\n" + "=" * (width * 2 + 9))


if __name__ == "__main__":
    run_tests()
```

---

## C. Inputs and Outputs

```text
Test 1:
  Input:  A man, a plan, a canal: Panama!
  Output: This is a palindrome.

Test 2:
  Input:  No 'x' in Nixon
  Output: This is a palindrome.

Test 3:
  Input:  Was it a car or a cat I saw?
  Output: This is a palindrome.
```

---

## D. AI-Generated Analysis

The provided Python program efficiently determines whether a given sentence is a palindrome by isolating its core alphanumeric characters and comparing the sequence to its reverse. At its core, the script utilizes the re (regular expression) module to strip away all spaces, punctuation, and special characters from the input string, subsequently standardizing the remaining characters to lowercase to ensure case-insensitivity. This sanitized string is then checked against a reversed slice of itself (`cleaned[::-1]`); if they match, a wrapper function returns a user-friendly confirmation message. Finally, a test-runner function iterates through a hardcoded list of specific test cases, neatly formatting and printing the original input alongside the evaluated result to the console.

While the script is highly readable and works perfectly for standard sentences, it could be optimized for both performance and extensibility. For instance, using the slicing method (`[::-1]`) creates a full copy of the string in memory, which could cause a bottleneck with exceptionally large text inputs; replacing this with a two-pointer approach—comparing characters from the beginning and end moving inwards—would reduce the space complexity to constant $O(1)$. Additionally, the regular expression pattern is recompiled every time the function is called; defining `re.compile(r"[^a-zA-Z0-9]")` globally would yield a slight speed boost. Finally, moving the hardcoded examples into a formal testing framework like `pytest` and allowing dynamic user inputs via the command line would elevate the script from a simple experiment to a robust, production-ready tool.
