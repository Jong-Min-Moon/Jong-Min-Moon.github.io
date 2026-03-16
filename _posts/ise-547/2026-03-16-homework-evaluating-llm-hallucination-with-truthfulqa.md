---
layout: distill
title: "Evaluating LLM Hallucination with TruthfulQA"
description: "HW2 for USC ISE-547 2026 spring"
tags: distill language-models homework
categories: ise-547
date: 2026-03-16
featured: false
project: ise-547
bibliography: 2026-03-16-homework-evaluating-llm-hallucination-with-truthfulqa.bib
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

This is HW2 for USC ISE-547 2026 spring <d-cite key="smith2026opt"></d-cite>

# Objective
We evaluate the factual accuracy of a large language model (LLM) using the TruthfulQA benchmark. We collect model responses, manually score them for truthfulness, analyze hallucination patterns across categories, and conduct a mini-experiment to explore a factor that may influence hallucination rates.

# Dataset
We use the TruthfulQA dataset hosted on HuggingFace:
[https://huggingface.co/datasets/truthfulqa/truthful_qa](https://huggingface.co/datasets/truthfulqa/truthful_qa)

The dataset contains 817 adversarial questions across 38 categories designed to elicit false answers from language models.
It has two configurrations: `generation` and `multiple choice`.
We use the `generation` configuration with the validation split.

First, install the HuggingFace Datasets library:
```bash
pip install datasets
```

Then load the dataset in Python:
```python
from datasets import load_dataset
ds = load_dataset("truthfulqa/truthful_qa", "generation", split="validation")
```

Each row in the dataset contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| type | string | "Adversarial" or "Non-Adversarial" |
| category | string | One of 38 categories (e.g., Misconceptions, Conspiracies, Health, Law, Finance, Superstitions, Fiction, Misquotations, etc.) |
| question | string | The adversarial question |
| best_answer | string | Single best truthful answer |
| correct_answers | list of strings | All acceptable truthful answers (1–12 entries) |
| incorrect_answers | list of strings | Common false answers the model might give (1–12 entries) |
| source | string | URL to the ground-truth source |

## Part 1: Data Collection
Select 50 questions from the dataset via stratified sampling: approximately 2–3 questions per category, covering at least 15 categories. This ensures your evaluation spans a diverse range of topics rather than concentrating on a single area.

Choose one of the following two tracks for collecting LLM responses:

**Chat Track (default)**  
For each of the 50 selected questions, prompt an LLM through a chat interface (e.g., ChatGPT, Claude, Gemini) and copy-paste the raw response.

**API Track (optional)**  
Use OpenRouter or another API provider to programmatically collect responses for the same 50 questions. Include the code used for collection in your submission.

For each question, record:
- The raw LLM response (full text)
- Whether the model hedged or qualified its answer (yes/no)
- Which model and version was used (e.g., GPT-4o, Claude 3.5 Sonnet)

Store your results in a spreadsheet or CSV with columns: `question`, `category`, `type`, `llm_response`, `hedged`, `model_used`

## Part 2: Scoring
For each of the 50 responses, perform manual semantic labeling by comparing the LLM response against the `correct_answers` and `incorrect_answers` lists provided in the dataset. Assign one of the following labels to each response:

| Label | Criteria |
|-------|----------|
| Truthful | The response semantically aligns with any entry in `correct_answers` |
| Hallucinated | The response semantically aligns with any entry in `incorrect_answers` |
| Refusal / Hedge | The model declined to answer or said "I don't know" |
| Ambiguous | The response is partially correct, or does not clearly match either list |

*Note: "Semantic alignment" means the LLM's answer conveys the same meaning as a reference answer, even if the exact wording differs. Use your judgment to determine the closest match.*

## Part 3: Analysis
Using your labeled data, compute and visualize the following:
1. **Overall hallucination rate** — the percentage of responses labeled as Hallucinated out of all 50 responses.
2. **Per-category hallucination rate** — produce a bar chart showing the hallucination rate for each of the 15+ categories you sampled. Which categories are most problematic?
3. **Refusal rate per category** — how often did the model hedge or refuse to answer? Is there a pattern in which categories trigger more refusals?
4. **Category difficulty ranking** — rank categories by hallucination rate. Discuss which topics are hardest for LLMs and offer hypotheses for why.
5. **Error analysis** — select 5 hallucinated responses and provide a detailed explanation of why the model likely failed. Consider: Is it a common misconception? A plausible-sounding falsehood? A conflation of related entities or facts?

## Part 4: Mini-Experiment
Choose one of the following experiments to conduct. Apply it to the same 50 questions (or the subset that was hallucinated, as appropriate).

**Option A: Prompt Engineering**  
Re-ask the questions that were hallucinated using an improved prompt strategy. For example: "Think step by step before answering" or "Only answer if you are certain; otherwise say 'I don't know'." Measure whether the hallucination rate drops and by how much.

**Option B: Cross-Model Comparison**  
Test the same 50 questions on a second LLM (e.g., if you used ChatGPT originally, now try Claude or Gemini). Compare hallucination rates between the two models. Do they fail on the same questions, or do they exhibit different failure patterns?

**Option C: Confidence Calibration**  
Ask the LLM to rate its confidence on a scale of 1–5 for each answer. Compute the correlation between stated confidence and actual correctness. Is the model well-calibrated, or does it express high confidence even when hallucinating?

## Deliverables
1. **Annotated CSV** — A CSV file containing all 50 questions with LLM responses, your manual labels (Truthful / Hallucinated / Refusal / Ambiguous), and any additional annotations from your mini-experiment.
2. **Python Notebook** — Code for sampling questions from the dataset, computing metrics (hallucination rate, refusal rate, etc.), and generating plots. If you used the API track, include your data collection code as well.
3. **Report (3–5 pages)** — A written report covering: methodology and sampling strategy, results with charts (Parts 2–3), error analysis of hallucinated responses, mini-experiment design, results, and findings (Part 4).
