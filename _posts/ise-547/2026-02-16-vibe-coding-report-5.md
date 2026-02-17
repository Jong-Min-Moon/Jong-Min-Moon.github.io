---
layout: distill
title: "Vibe Coding Report: Advanced Recursive Maze Solver"
description: "A report on generating an Advanced Recursive Maze Solver (BFS with Teleports) using AI prompts."
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

I start from the last prompt and answer from problem 4.

### Prompt 1 (Gemini 3 Pro)
> Starting from current code and problem, I want to extend the problem and modify the code accordingly.
> I am going to do vibe coding and I want you to help me write the first prompt. The problem is writing a python code that follows the following instruction:
>
> **Problem 5: Recursive Maze Solver (Advanced)**
> Extend the previous problem to handle more complex rules:
> *   The maze may contain special symbols:
>     *   S for start,
>     *   E for exit,
>     *   T for teleport pads (any T can teleport to any other T in one step, or in other words, from one T you can move to another T in the grid in 1 step).
> *   Your program should find the shortest path from S to E, making use of teleports if they help. For every move (including a teleport) assume the cost is 1.
> *   Output the path as a sequence of coordinates or directions. Return None if there is no path.
>
> The input format examples are:
>
> **Input 1 (simple S→E, no teleports)**
> ```text
> S00
> 110
> 00E
> ```
> **Input 2 (teleports help bypass a wall)**
> ```text
> S1T001
> 111101
> 0000T1
> 101111
> 10000E
> ```
> **Input 3 (multiple teleports; shortest path requires choosing the right T)**
> ```text
> S001T0
> 110110
> T00010
> 0111T0
> 00010E
> ```
>
> Test cases must be written with these examples and the test output should clearly format and print the input and output.

### Prompt 2 (Cursor)
> Act as an expert Python developer. I want to extend our previous maze solver to handle a new set of rules. Please write a Python solution for "Problem 5: Recursive Maze Solver (Advanced)" along with a robust pytest test suite.
>
> **The Problem:** The maze is represented as a grid of characters:
> *   S: Start
> *   E: Exit
> *   T: Teleport pad
> *   0: Open space
> *   1: Wall
>
> **Implementation Details:**
> 1.  **Shortest Path:** You must find the shortest path from S to E. Because we need the shortest path, please use a Breadth-First Search (BFS) algorithm using a queue, rather than standard recursive DFS.
> 2.  **Teleporters:** Any T can teleport to any other T in the grid in exactly 1 step (cost = 1). All standard moves (up, down, left, right) also cost 1.
> 3.  **Output:** Return the path as a sequence of coordinate tuples `[(r, c), (r, c), ...]` starting at S and ending at E. Return `None` if there is no valid path.
> 4.  **Parsing:** Write a helper function to parse multi-line strings of these characters into your chosen grid data structure.
>
> **Testing Requirements:**
> 1.  Use the `pytest` framework.
> 2.  Use `@pytest.mark.parametrize` to dynamically pass the 3 test cases below into the test function.
> 3.  Within the test, clearly print the formatted input grid, followed by the output path length and the path itself so the user can visually verify the results when running `pytest -s`.
>
> **Test Cases to Parameterize:**
> *   Input 1 (Simple S→E, no teleports): `S00 110 00E`
> *   Input 2 (Teleports help bypass a wall): `S1T001 111101 0000T1 101111 10000E`
> *   Input 3 (Multiple teleports; shortest path requires choosing the right T): `S001T0 110110 T00010 0111T0 00010E`
>
> Please output the complete, runnable Python script containing both the solver and the pytest suite.

### Prompt 3 (Gemini 3 Pro)
> Summarize the logic of the following program. Then, comment on how the program could be improved. give me a two-paragraph summary.

---

## B. Final Generated Program

```python
"""
Advanced Maze Solver: Shortest path from S to E using BFS, with teleport pads (T).
Grid: S = start, E = exit, T = teleport (any T → any other T in 1 step), 0 = open, 1 = wall.
"""

from __future__ import annotations

from collections import deque


def parse_maze(grid_str: str) -> list[list[str]]:
    """
    Parse a multi-line string of maze characters into a grid.

    Allowed characters: S (start), E (exit), T (teleport), 0 (open), 1 (wall).
    Leading/trailing whitespace on each line is stripped.

    Returns:
        A rectangular grid (list of lists of single-character strings).
    """
    return [
        [ch for ch in line.strip()]
        for line in grid_str.strip().splitlines()
        if line.strip()
    ]


def find_cells(grid: list[list[str]]) -> tuple[tuple[int, int] | None, tuple[int, int] | None, list[tuple[int, int]]]:
    """
    Locate start (S), exit (E), and all teleport pads (T) in the grid.

    Returns:
        (start, end, list_of_teleports). Any of start/end may be None if not found.
    """
    start: tuple[int, int] | None = None
    end: tuple[int, int] | None = None
    teleports: list[tuple[int, int]] = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)
            elif cell == "E":
                end = (r, c)
            elif cell == "T":
                teleports.append((r, c))
    return start, end, teleports


def format_grid(grid: list[list[str]]) -> str:
    """Return a readable string representation of the grid."""
    return "\n".join("".join(cell for cell in row) for row in grid)


def solve_maze_advanced(grid: list[list[str]]) -> list[tuple[int, int]] | None:
    """
    Find the shortest path from S to E using BFS. Moves are up/down/left/right (cost 1)
    or teleport from any T to any other T (cost 1). Returns the path as a list of
    (row, col) tuples from S to E, or None if no path exists.
    """
    if not grid or not grid[0]:
        return None

    rows, cols = len(grid), len(grid[0])
    start, end, teleport_list = find_cells(grid)
    if start is None or end is None:
        return None

    # Walls: only '1' blocks movement. S, E, T, 0 are traversable.
    def _is_wall(r: int, c: int) -> bool:
        return grid[r][c] == "1"

    def _in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols

    # BFS with parent pointers for path reconstruction
    parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    queue: deque[tuple[int, int]] = deque([start])

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            # Reconstruct path from E back to S
            path: list[tuple[int, int]] = []
            cur: tuple[int, int] | None = end
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path

        # Standard moves: up, down, left, right
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nr, nc = r + dr, c + dc
            if not _in_bounds(nr, nc):
                continue
            if _is_wall(nr, nc):
                continue
            if (nr, nc) in parent:
                continue
            parent[(nr, nc)] = (r, c)
            queue.append((nr, nc))

        # If current cell is a teleport, add all other teleports as one-step neighbors
        if (r, c) in teleport_list:
            for (tr, tc) in teleport_list:
                if (tr, tc) == (r, c):
                    continue
                if (tr, tc) in parent:
                    continue
                parent[(tr, tc)] = (r, c)
                queue.append((tr, tc))

    return None


# ---------------------------------------------------------------------------
# Pytest suite (parametrized, with visible grid and path)
# Run with: pytest maze_solver_advanced.py -v -s
# ---------------------------------------------------------------------------

import pytest


@pytest.mark.parametrize(
    "grid_str,has_path",
    [
        (
            """
            S00
            110
            00E
            """,
            True,
        ),
        (
            """
            S1T001
            111101
            0000T1
            101111
            10000E
            """,
            False,  # S has no adjacent open cell in this grid; no path
        ),
        (
            """
            S001T0
            110110
            T00010
            0111T0
            00010E
            """,
            True,
        ),
    ],
    ids=["simple_s_to_e", "teleports_bypass_wall", "multiple_teleports"],
)
def test_maze_solver_advanced(grid_str: str, has_path: bool) -> None:
    """Parametrized test: prints grid, path length, and path for visual verification."""
    grid = parse_maze(grid_str)
    start, end, _ = find_cells(grid)
    result = solve_maze_advanced(grid)

    print(f"\n  Grid:")
    print("  " + format_grid(grid).replace("\n", "\n  "))
    if result is not None:
        print(f"  Path length: {len(result)}")
        print(f"  Path: {result}")
        assert result[0] == start, "Path must start at S"
        assert result[-1] == end, "Path must end at E"
    else:
        print("  No valid path.")

    assert (result is not None) == has_path


def test_parse_maze() -> None:
    """Parser produces correct grid and find_cells locates S, E, T."""
    grid = parse_maze("S0\n1E")
    assert grid == [["S", "0"], ["1", "E"]]
    start, end, t = find_cells(grid)
    assert start == (0, 0)
    assert end == (1, 1)
    assert t == []

    grid2 = parse_maze("ST\n00")
    _, _, t2 = find_cells(grid2)
    assert t2 == [(0, 1)]


def test_no_path() -> None:
    """Grid with S and E but no path returns None."""
    grid = parse_maze(
        """
        S11
        111
        11E
        """
    )
    result = solve_maze_advanced(grid)
    print(f"\n  Grid: S and E surrounded by walls")
    print(f"  Path: {result}")
    assert result is None


def test_empty_grid() -> None:
    """Empty grid returns None."""
    assert solve_maze_advanced([]) is None
    assert solve_maze_advanced([[]]) is None


# ---------------------------------------------------------------------------
# Standalone: run on first test maze
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    example = """
    S00
    110
    00E
    """
    grid = parse_maze(example)
    print("Maze:")
    print(format_grid(grid))
    path = solve_maze_advanced(grid)
    if path:
        print(f"\nPath length: {len(path)}")
        print(f"Path: {path}")
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

This generated program successfully shifts the architecture to an iterative Breadth-First Search (BFS) to guarantee the shortest path through the maze. It begins by parsing the text grid and identifying the coordinates of the start (S), exit (E), and all teleporter (T) pads. Using a deque for efficient first-in-first-out processing, the algorithm evaluates standard adjacent moves while treating any reached teleporter as having immediate one-step connections to all other teleporters. As it traverses, it maps each newly visited cell to its predecessor in a parent dictionary. This prevents infinite loops and provides the exact breadcrumb trail needed to reverse-engineer the optimal route once the exit is discovered.

While the fundamental BFS logic is solid, the program could be improved both algorithmically and conceptually. Most amusingly, your AI agent realized that your "Input 2" grid accidentally traps the starting node behind walls, so rather than alerting you to the unsolvable maze, it cheekily changed your test assertion to expect False! Algorithmically, the teleporter logic is computationally inefficient; currently, every time any teleporter is visited, the code loops through the entire teleporter list again. Since all teleporters share a single unified network, the program should trigger the teleporters once, add them to the queue, and then mark the network as "exhausted" to eliminate redundant $O(T^2)$ checking.
