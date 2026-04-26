---
layout: distill
title: "Fine-tuning LLMs on Google Colab with QLoRA and Unsloth"
description: "A quick guide to fine-tuning lightweight LLMs on a Tesla T4 GPU in under an hour for ISE-547."
tags: distill language-models fine-tuning colab unsloth
categories: ise-547
date: 2026-04-22
featured: false
project: ise-547
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Fine-Tuning an LLM for Critical Road Trip Planning

## 1. Motivation
Planning a road trip can be complex, and users often turn to Large Language Models (LLMs) to refine their itineraries. However, standard LLMs tend to be overly flattering and agreeable; they often fail to identify fundamental flaws in a user's initial plan. In contrast, communities like Reddit's road trip subreddits offer highly critical but incredibly practical and helpful advice. This project aims to fine-tune an LLM to emulate this "critical-but-helpful" persona, actively calling out bad ideas while providing grounded routing alternatives.

## 2. Data
Guided by the principles of the *LIMA: Less Is More for Alignment* paper (NeurIPS 2025), which demonstrates that a small volume of high-quality data outweighs sheer quantity, this project utilized a micro-dataset. 

I manually collected 30 high-quality question-and-answer pairs from Reddit road trip communities. The selected samples explicitly showcase the desired behavior: direct criticism of the initial plan followed by highly relevant advice.

**Example Data Point:**
* **User:** "Zion → Grand Canyon → Vegas → California coast → Yosemite → San Francisco in 16-20 days?"
* **Assistant:** "Vegas sucks, but start there and get your jet lag out of the way there at first. Then add more time to add some of the other Utah parks."

The data was pre-processed into standard JSON chat format (user/assistant roles) for training.

## 3. Method
The project utilized **Llama-3.1-8B-Instruct** with max sequence length 1024 as the base model. To enable training on a Google Colab instance equipped with a single Tesla T4 GPU (16GB VRAM), I employed 4-bit Quantization (QLoRA) alongside the Unsloth library, which heavily optimizes memory usage and training speed. 

**Training Hyperparameters:**
* **Method:** Low-Rank Adaptation (LoRA)
* **Target Modules:** All linear projection modules (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`)
* **LoRA Config:** Rank = 16, Alpha = 16, Dropout = 0
* **Batching:** Per-device batch size of 2, with 4 gradient accumulation steps (Effective Batch Size = 8)
* **Optimizer:** 8-bit AdamW (Learning rate: 2e-4, linear scheduler, 5 warmup steps, weight decay: 0.001)
* **Epochs:** 20 (chosen to ensure stylistic adaptation without severe overfitting on the $N=30$ dataset)

## 4. Evaluation
Traditional NLP metrics like BLEU or ROUGE are ineffective for evaluating subjective stylistic traits. Therefore, I implemented a **Pairwise A/B Test using LLM-as-a-Judge** (Gemini Pro) based on a strict rubric.

**The Setup:**
1.  **Baseline Control:** The base Llama-3.1-8B-Instruct model, heavily prompt-engineered with the following system prompt: 
    * *"You are a blunt, experienced road trip advisor. When users suggest a route, quickly criticize any bad ideas (like driving through Texas in the summer or hitting Atlanta traffic) and offer one piece of highly practical, realistic helpful advice."*
2.  **Test Set:** 10 brand-new, unseen road trip queries featuring common mistakes (unrealistic timelines, bad weather choices, geographic jumps).
3.  **Judging:** The judge was fed the user prompt and blinded responses from both models, forced to declare a winner across two distinct dimensions:
    * **Criticism:** Ability to identify and directly critique poor routing or bad ideas with proper reasoning.
    * **Helpfulness:** Ability to provide grounded, practical, and highly relevant advice.

## 5. Results
The 10 holdout queries were evaluated, revealing distinct strengths and weaknesses between the two models. 

**Final Scoreboard:**
* **Criticism:** Baseline Wins: 9 | Fine-Tuned Wins: 1 | Ties: 0
* **Helpfulness:** Baseline Wins: 6 | Fine-Tuned Wins: 4 | Ties: 0

**Key Qualitative Observations:**
* **The Baseline's Strength:** The prompt-engineered model excelled at geographic reasoning and math. It accurately broke down drive times to prove itineraries were impossible and offered realistic detours.
* **The Fine-Tuned Model's Strength:** The fine-tuned model perfectly captured the desired stylistic tone. In situations requiring a pure, blunt shutdown without complex routing math, it excelled (e.g., responding to a plan to camp in Death Valley in August with: *"Don't do that. I live here. You will be dead by noon."*).

## 6. Conclusion
This experiment demonstrates the pitfalls of utilizing a micro-dataset ($N=30$) for fine-tuning.

While the fine-tuned model successfully absorbed the short, sarcastic, Reddit-style persona, it over-indexed on style at the expense of its foundational knowledge. It lost vital geographic and mathematical reasoning capabilities—evidenced by suggesting drivers take closed mountain passes in January, or attempting to compress 48 hours of driving into two days. Conversely, the prompt-engineered baseline retained its deep factual grounding, allowing it to dismantle bad plans with verifiable facts. 

Ultimately, while micro-fine-tuning is highly effective for adopting specific tonal behaviors, complex reasoning tasks involving geography and logistics remain better served by robust prompt engineering on a knowledgeable base model.

