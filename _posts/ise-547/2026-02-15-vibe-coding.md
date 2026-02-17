---
layout: distill
title: "Prompting for Vibe Coding"
description: "Strategies for effective AI-assisted coding: Structure, Iteration, and Meta-Prompting."
tags: distill formatting
categories: generative-ai
date: 2026-02-15
featured: false
mermaid:
  enabled: true
  zoomable: true
project: ise-547
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
toc:
  - name: "Structure & Preparation"
  - name: "Iterative Building (Coordinate Descent)"
  - name: "Reverse Meta Prompting"
  - name: "Handling Persistent Errors"

_styles: >
  .fake-img {
    margin-bottom: 12px;
  }
  .fake-img p {
    text-align: center;
    margin: 12px 0;
  }
---

## I. Structure & Preparation: Details Up Front

The most common mistake in AI-assisted coding ("Vibe Coding") is diving straight into the IDE without a plan. 

**Before using Cursor or any coding agent:**
1.  Go to your favorite high-reasoning LLM (e.g., Claude 3.5 Sonnet, GPT-4o).
2.  **Chat back and forth** to solidify your requirements.
3.  Ask it to **write the first prompt** for you, with clear specifications in titles and bullet points.
4.  Explicitly tell it: *"Build instructions that will be fed into Cursor."*

This "pre-prompting" step ensures that the coding agent receives a structured, unambiguous blueprint rather than a vague intent.

---

## II. Iterative Building: The Constraints & Don'ts

Building complex software with AI should be treated like a **Coordinate Descent Algorithm**: optimize one variable at a time while keeping others fixed.

For each iteration, focus on improving **one specific feature** while explicitly constraining the agent to leave other parts untouched.

**The Prompting Pattern:**
*   "Only improve [Feature X]..."
*   "Do **not** touch [Feature Y]..."
*   "Make sure not to break [Existing Functionality Z]..."

<div class="fake-img l-body">
  <div class="mermaid">
    graph TD
    A[Start Iteration] --> B{Choose Target Feature};
    B --> C[Fix All Other Variables];
    C --> D[Optimize Target];
    D --> E{Constraints Violated?};
    E -- Yes --> F[Revert & Refine Constraints];
    E -- No --> G[Commit & Next Iteration];
    F --> D;
  </div>
  <div class="caption">
    The Coordinate Descent approach to AI coding.
  </div>
</div>

---

## III. Reverse Meta Prompting

Don't just fix bugs; learn from them. **Reverse Meta Prompting** turns every error into an asset for future coding sessions.

**The Workflow:**
1.  **Resolve the Issue:** Work with the AI to fix a specific bug.
2.  **Summarize:** Ask the AI: *"Summarize what went wrong and exactly how it was fixed."*
3.  **Generate Prompt:** Ask natural follow-up: *"Generate a reusable prompt that I can use in the future to prevent or solve this specific challenge."*
4.  **Save:** Store this prompt in your personal library.

This creates a feedback loop where your "Vibe Coding" continually improves based on past experiences.

---

## IV. Handling Persistent Errors

When the AI gets stuck in a loop or errors keep recurring, stop and switch strategies. Use this 4-step protocol:

1.  **Ask "What have you tried?":** Force the AI to list its failed attempts. This prevents it from looping through the same ineffective fixes.
2.  **Explain Simply:** Re-explain the error in plain English. This provides fresh context and often helps align the AI's understanding with the root cause.
3.  **Alternate Approach:** Explicitly ask: *"Is there a completely different way to solve this?"*
4.  **Revert and Replay:** Rollbacks are your friend! It is often faster to revert to a clean state and try again than to untangle a messy, broken codebase.
