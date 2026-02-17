---
layout: distill
title: "Vibe Coding Report: Recursive Maze Solver"
description: "A report on generating a Recursive Maze Solver using AI prompts and iterative refinement."
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

This time, I did two iterative steps of prompting to build and improve the code.

### Prompt 1 (Gemini 3 Pro)
> I am going to do vibe coding and I want you to help me write the first prompt. The problem is writing a python code that follows the following instruction:
>
> **Problem 4: Recursive Maze Solver (Basic)**
> A maze is represented as a grid of 0s and 1s in text form (for example, each line of text corresponds to a row). 0 means open, 1 means wall. Write a program that finds a path from the top-left corner to the bottom-right corner, if one exists, and prints it. The grid is assumed to be rectangular, with all lines having equal length.
>
> The input format examples are:
>
> (Each maze is a text grid of 0/1; top-left is start, bottom-right is goal. You can input each of these as a matrix e.g., numpy array, or as a list of lists. Whatever decision you make for the input format is fine, as long as it's reasonable and you can use it for all three inputs below; the same note applies also to Problem 5)
>
> *   **Input 1**
>     ```text
>     0010
>     0010
>     0000
>     0110
>     0000
>     ```
> *   **Input 2**
>     ```text
>     000
>     110
>     010
>     010
>     000
>     ```
> *   **Input 3 (no valid path—should be handled gracefully)**
>     ```text
>     010
>     111
>     010
>     000
>     ```
>
> Test cases must be written with these examples and the test output should clearly format and print the input and output. Do not hardcode the test code. Rather, use a formal testing framework like pytest and allowing dynamic user inputs, but use the inputs I provided on that framework.

### Prompt 2 (Cursor)
> Act as an expert Python developer. I want you to write a Python solution for a "Recursive Maze Solver" along with a robust pytest test suite.
>
> **The Problem:** A maze is represented as a grid of 0s and 1s. 0 means open space, and 1 means a wall. Write a program that recursively finds a path from the top-left corner (0, 0) to the bottom-right corner, if one exists, and returns/prints it. The grid is rectangular.
>
> **Implementation Details:**
> 1.  Choose a reasonable input format for the maze (e.g., a list of lists of integers, or a NumPy array) and stick to it.
> 2.  The solver must use a recursive approach (like Depth-First Search with backtracking).
> 3.  It should return the path as a list of coordinate tuples (e.g., `[(0,0), (1,0), ...]`) or return a clear indicator (like `None` or an empty list) if no path exists.
>
> **Testing Requirements:**
> 1.  Use the `pytest` framework. Do not just write a basic `if __name__ == "__main__":` block.
> 2.  Use `@pytest.mark.parametrize` to dynamically pass the following 3 test cases into the test function.
> 3.  Within the test, clearly print the formatted input grid, followed by the output path (or a "No valid path" message) so that when run with `pytest -s`, the user can visually verify the results.
>
> **Test Cases to Parameterize:**
> *   Input 1 (Valid Path Expected): `0010 0010 0000 0110 0000`
> *   Input 2 (Valid Path Expected): `000 110 010 010 000`
> *   Input 3 (No Valid Path - Handle Gracefully): `010 111 010 000`
>
> Please output the complete, runnable Python script containing both the solver class/function and the pytest suite.

### Prompt 3 (Gemini 3 Pro)
> Summarize the logic of the following program. Then, comment on how the program could be improved. give me a two-paragraph summary.

---

## B. Final Generated Program

```python
"""
Recursive Maze Solver: Finds a path from top-left (0,0) to bottom-right using DFS with backtracking.
Maze format: list of lists of integers; 0 = open, 1 = wall.
"""

from __future__ import annotations


def solve_maze(grid: list[list[int]]) -> list[tuple[int, int]] | None:
    """
    Find a path from (0, 0) to the bottom-right corner of the grid using recursive DFS with backtracking.

    Args:
        grid: Rectangular grid of 0s (open) and 1s (wall). Must be non-empty.

    Returns:
        A list of (row, col) coordinate tuples from start to end, or None if no path exists.
    """
    if not grid or not grid[0]:
        return None

    rows, cols = len(grid), len(grid[0])
    start, end = (0, 0), (rows - 1, cols - 1)

    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return None

    visited: set[tuple[int, int]] = set()
    path: list[tuple[int, int]] = []

    def _in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols

    def _dfs(r: int, c: int) -> bool:
        if (r, c) == end:
            path.append((r, c))
            return True
        if not _in_bounds(r, c) or grid[r][c] == 1 or (r, c) in visited:
            return False

        visited.add((r, c))
        path.append((r, c))

        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if _dfs(r + dr, c + dc):
                return True

        path.pop()
        visited.discard((r, c))
        return False

    if _dfs(start[0], start[1]):
        return path
    return None


def grid_from_string(s: str) -> list[list[int]]:
    """
    Parse a multi-line string of 0s and 1s (one row per line) into a grid.

    Example:
        >>> grid_from_string("01\\n10")
        [[0, 1], [1, 0]]
    """
    return [[int(ch) for ch in line.strip()] for line in s.strip().splitlines() if line.strip()]


def format_grid(grid: list[list[int]]) -> str:
    """Return a readable string representation of the grid."""
    return "\n".join("".join(str(cell) for cell in row) for row in grid)


# ---------------------------------------------------------------------------
# Pytest suite (parametrized, with visible grid and path via print)
# Run with: pytest maze_solver.py -v -s
# ---------------------------------------------------------------------------

import pytest


@pytest.mark.parametrize(
    "grid_str,has_path",
    [
        (
            """
            0010
            0010
            0000
            0110
            0000
            """,
            True,
        ),
        (
            """
            000
            110
            010
            010
            000
            """,
            True,
        ),
        (
            """
            010
            111
            010
            000
            """,
            False,
        ),
    ],
    ids=["valid_path_1", "valid_path_2", "no_path"],
)
def test_maze_solver(grid_str: str, has_path: bool) -> None:
    """Parametrized test: prints grid and path (or 'No valid path') for visual verification."""
    grid = grid_from_string(grid_str)
    result = solve_maze(grid)
    rows, cols = len(grid), len(grid[0])
    end = (rows - 1, cols - 1)

    print(f"\n  Grid ({rows}x{cols}):")
    print("  " + format_grid(grid).replace("\n", "\n  "))
    if result:
        print(f"  Path ({len(result)} steps): {result}")
        assert result[0] == (0, 0), "Path must start at (0, 0)"
        assert result[-1] == end, "Path must end at bottom-right"
        assert has_path, "Expected a valid path"
    else:
        print("  No valid path.")
        assert not has_path, "Expected no path"

    assert (result is not None and len(result) > 0) == has_path


def test_maze_solver_empty() -> None:
    """Empty grid returns None."""
    assert solve_maze([]) is None
    assert solve_maze([[]]) is None


def test_maze_solver_single_cell() -> None:
    """Single open cell is a trivial path."""
    result = solve_maze([[0]])
    print(f"\n  Grid: [[0]]")
    print(f"  Path: {result}")
    assert result == [(0, 0)]


def test_maze_solver_start_or_end_wall() -> None:
    """If start or end is a wall, return None."""
    assert solve_maze([[1, 0], [0, 0]]) is None
    assert solve_maze([[0, 0], [0, 1]]) is None


# ---------------------------------------------------------------------------
# Standalone: run solver on a small example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    example = grid_from_string(
        """
        0010
        0010
        0000
        0110
        0000
        """
    )
    print("Maze:")
    print(format_grid(example))
    path = solve_maze(example)
    if path:
        print(f"\nPath: {path}")
    else:
        print("\nNo valid path.")
```

---

## C. Inputs and Outputs

```text
maze_solver.py::test_maze_solver[valid_path_1] 
  Grid (5x4):
  0010
  0010
  0000
  0110
  0000
  Path (8 steps): [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (3, 3), (4, 3)]
PASSED
maze_solver.py::test_maze_solver[valid_path_2] 
  Grid (5x3):
  000
  110
  010
  010
  000
  Path (7 steps): [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
PASSED
maze_solver.py::test_maze_solver[no_path] 
  Grid (4x3):
  010
  111
  010
  000
  No valid path.
PASSED
maze_solver.py::test_maze_solver_empty PASSED
maze_solver.py::test_maze_solver_single_cell 
  Grid: [[0]]
  Path: [(0, 0)]
PASSED
```

---

## D. AI-Generated Analysis

The provided Python program implements a Depth-First Search (DFS) algorithm with backtracking to find a route through a grid-based maze. It begins by validating the grid, immediately returning None if the matrix is empty or if the starting or ending cells are walls. A nested recursive helper function, `_dfs`, handles the core traversal by exploring adjacent cells in a specific order (right, down, left, up). As it navigates, it appends the current coordinates to a path list and marks them in a visited set to prevent getting stuck in infinite loops. If the algorithm encounters a dead end, it backtracks by popping the current cell from the path and discarding it from the visited set, continuing this trial-and-error process until it either reaches the bottom-right goal or exhausts all possible routes.

While the code is well-formatted and includes a robust pytest suite, the algorithm itself has a critical performance flaw and room for architectural improvement. The inclusion of `visited.discard((r, c))` during backtracking forces the program to "forget" dead ends, allowing alternative paths to redundantly explore known bad routes; this severely degrades performance to exponential time complexity on open grids, and removing that single line would instantly optimize the search to run in linear time, or $O(R \times C)$. Furthermore, because it relies on the Python call stack, deep recursions in large mazes will eventually trigger a `RecursionError`, a limitation that an iterative stack-based approach would completely avoid. Finally, DFS only guarantees finding any path rather than the optimal one. Would you like me to rewrite this solver using a Breadth-First Search (BFS) algorithm so that it always finds the shortest possible path?
