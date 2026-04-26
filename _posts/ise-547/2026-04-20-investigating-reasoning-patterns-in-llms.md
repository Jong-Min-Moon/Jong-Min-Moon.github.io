---
layout: distill
title: "Comparative Analysis of Chain-of-Thought Reasoning in Large Language Models"
description: "Assignment examining different Chain-of-Thought (CoT) prompting strategies in LLMs."
tags: distill language-models homework
categories: ise-547
date: 2026-04-20
featured: false
project: ise-547
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

We investigate how different Chain-of-Thought (CoT) prompting strategies influence reasoning quality in a large-language-model environment.
We compare five prompting methods on a set of reasoning problems and analyze:
- accuracy of final answers
- structure and clarity of intermediate reasoning
- typical reasoning errors (omission, over-reasoning, hallucination, arithmetic slips)

# 2. Task Overview
You will:
1. Apply five CoT prompting methods to every question.
2. Record reasoning traces and evaluate correctness.
3. Write a short report comparing the results.

# 3. Questions and prompts
We use the following questions:
| # | Domain | Question |
|---|---|---|
| 1 | Math (GSM8K) | A shop sells 3 apples for $5. If the price increases by 20%, how much will 12 apples cost? |
| 2 | Math | A farmer has 8 cows and buys 5 more. He then sells half of his total cows and later buys 3 calves. How many cows does he have now? |
| 3 | Science (ARC) | Copper wire, wooden stick, and rubber band are placed in an electric circuit. Which one lets current flow and why? |
| 4 | Causal | A plant receives less sunlight but the same amount of water and nutrients. How will its rate of photosynthesis and growth change, and why? |
| 5 | Multisentence reasoning | Mary put her cup on the table and left. John came, moved it to the shelf, and took the book that was under it. Where is the cup now, and who has the book? |
| 6 | Data Science | You run a two-sample Z-test for the difference in means and the confidence interval length is too wide. How to fix it? |
| 7 | Data Science | You are a data scientist at Doordash and run a regression with conversion as response and ETA as predictor. The coefficient is negative. How to fix it? |

For each of the questions, we use the following Chain-of-Thought   prompts:
 
| # | Method | Prompting Instruction |
|---|---|---|
| 1 | Zero-Shot CoT | Ask the question and append "Let's think step by step." |
| 2 | Few-Shot CoT | Provide 2–3 solved examples before the target question. |
| 3 | Self-Refine / Critic | After the first answer, re-prompt: "Review your reasoning and correct any mistakes." |
| 4 | Sub-Question Decomposition | Use a prompt to break the main problem into sub-questions, answer each, then combine. |
| 5 | Self-Consistency | Generate 5 independent reasoning traces and take a majority-vote answer. To obtain independent traces, use slightly different prompts for each trace. |



For Few-shot CoT, we use the following examples:

## 1) Apples Price Increase

### Example 1
**Question:** 3 apples cost $5. Price increases by 20%. Cost of 12 apples?  

**Solution:**
- Original price per apple = 5 ÷ 3 = $1.67  
- New price = 1.67 × 1.20 = $2.00  
- Cost of 12 apples = 12 × 2 = **$24**

---

### Example 2
**Question:** 3 apples cost $6. Price increases by 20%. Cost of 12 apples?  

**Solution:**
- Price per apple = 6 ÷ 3 = $2  
- New price = 2 × 1.20 = $2.40  
- Cost of 12 apples = 12 × 2.40 = **$28.80**

---

### Example 3
**Question:** 3 apples cost $9. Price increases by 20%. Cost of 12 apples?  

**Solution:**
- Price per apple = 9 ÷ 3 = $3  
- New price = 3 × 1.20 = $3.60  
- Cost of 12 apples = 12 × 3.60 = **$43.20**

---

## 2) Farmer and Cows

### Example 1
**Solution:**
- Start: 8 cows  
- Buys 5 → 13 cows  
- Sells half → 13 ÷ 2 = 6.5 (assume 6 sold, 7 left)  
- Buys 3 → 7 + 3 = **10 cows**

---

### Example 2
**Variation:** Start with 10 cows  

- Buys 6 → 16  
- Sells half → 8  
- Buys 2 → **10 cows**

---

### Example 3
**Variation:** Start with 12 cows  

- Buys 4 → 16  
- Sells half → 8  
- Buys 5 → **13 cows**

---

## 3) Electric Circuit Materials

### Example 1
**Answer:** Copper wire lets current flow  
**Why:** Copper is a good conductor due to free electrons  

---

### Example 2
**Answer:** Wooden stick does NOT let current flow  
**Why:** Wood is an insulator (no free electrons)  

---

### Example 3
**Answer:** Rubber band does NOT let current flow  
**Why:** Rubber is an insulator and blocks current  

---

## 4) Plant with Less Sunlight

### Example 1
**Answer:**
- Photosynthesis decreases  
- Growth slows  
**Why:** Light is essential for photosynthesis  

---

### Example 2
**Answer:**
- Very low sunlight → very low photosynthesis  
- Plant may become weak or die  
**Why:** Energy production is limited  

---

### Example 3
**Answer:**
- Moderate reduction → slower growth, not stopped  
**Why:** Some photosynthesis still occurs  

---

## 5) Cup and Book Logic

### Example 1
**Answer:**
- Cup → on the shelf  
- Book → with John  

---

### Example 2
**Variation:** If John moves cup to desk  

- Cup → desk  
- Book → with John  

---

### Example 3
**Variation:** If John doesn’t take the book  

- Cup → shelf  
- Book → remains where it was  

---

## 6) Z-test Wide Confidence Interval

### Example 1
**Fix:** Increase sample size  
**Why:** Larger samples reduce standard error  

---

### Example 2
**Fix:** Reduce variability  
**Why:** Lower variance narrows interval  

---

### Example 3
**Fix:** Use lower confidence level (e.g., 95% → 90%)  
**Why:** Smaller margin of error  

---

## 7) Regression (Negative ETA Coefficient)

### Example 1
**Issue:** Longer ETA reduces conversion (negative coefficient)  
**Fix:** This may be correct — interpret it  
**Reason:** Customers prefer faster delivery  

---

### Example 2
**Fix:** Check confounders  
- Add variables (price, restaurant rating)  
**Why:** Omitted variables bias results  

---

### Example 3
**Fix:** Check causality  
- Use experiment or instrumental variables  
**Why:** Correlation ≠ causation  

# Results
Due to the time restriction, I was able to evaluate the first three strategies. The average correctess was:

6/7 for Zero-Shot CoT
7/7 for Few-Shot CoT
7/7 for Self-Refine / Critic

The wrong answer by Zero-shot was: 9.5 cows. The question was "A farmer has 8 cows and buys 5 more. He then sells half of his total cows and later buys 3 calves. How many cows does he have now?"

## Qualitative analysis:
Zero-shot CoT displayed **hallucination**: answering 9.5 cows where there cannot be 0.5 cow in this world. For the other questions and prompt strategies the reasoning was sound and logical. 


## Full prompts of all five methods you used for the first question:
```
1. Question: A shop sells 3 apples for $5. If the price increases by 20%, how much will 12 apples cost? Let's think step by step.


2. Question: A shop sells 3 apples for $5. If the price increases by 20%, how much will 12 apples cost? Learn from the following examples.
Question: 3 apples cost $6. Price increases by 20%. Cost of 12 apples?
Generated Reasoning: Price per apple = 6 ÷ 3 = $2
New price = 2 × 1.20 = $2.40
Cost of 12 apples = 12 × 2.40 = $28.80
Final Answer: Price per apple = 6 ÷ 3 = $2
New price = 2 × 1.20 = $2.40
Cost of 12 apples = 12 × 2.40 = $28.80


Question: 3 apples cost $9. Price increases by 20%. Cost of 12 apples?
Generated Reasoning: Price per apple = 9 ÷ 3 = $3
New price = 3 × 1.20 = $3.60
Cost of 12 apples = 12 × 3.60 = $43.20
Final Answer: Price per apple = 9 ÷ 3 = $3
New price = 3 × 1.20 = $3.60
Cost of 12 apples = 12 × 3.60 = $43.20


3. Original Question: A shop sells 3 apples for $5. If the price increases by 20%, how much will 12 apples cost? ... Review your reasoning and correct any mistakes. Provide your revised reasoning and final answer.


```
## Conclusion
Self-Refine / Critic and Few-Shot CoT performs similarly in terms of interpretability and correctness. However, Few-Shot CoT requires external examples. Therefore  Self-Refine / Critic is the best method among the three. 

 










# Code and Meta-prompts






Prompt used to run the experiment:

``` markdown
You are given 7 questions. For EACH question, apply the following 5 prompting strategies and return both the reasoning (as text) and the final answer.

---

## Prompting Strategies to Apply

1. **Zero-Shot Chain-of-Thought (CoT)**  
   - Prompt: Ask the question and append:  
     **"Let's think step by step."**

2. **Few-Shot Chain-of-Thought (CoT)**  
   - Prompt: Provide 2–3 solved examples before the target question.  
   - Then ask the target question.

3. **Self-Refine / Critic**  
   - Step 1: Generate an initial answer with reasoning.  
   - Step 2: Re-prompt with:  
     **"Review your reasoning and correct any mistakes."**  
   - Return the refined reasoning and final answer.

4. **Sub-Question Decomposition**  
   - Prompt the model to:
     - Break the problem into smaller sub-questions  
     - Solve each sub-question  
     - Combine them into a final answer  

5. **Self-Consistency**  
   - Generate **5 independent reasoning traces** using slightly different prompts  
   - Extract the final answer from each trace  
   - Return:
     - All reasoning traces  
     - The **majority-vote final answer**

---

## Output Format (STRICT)

Return results in a table with the following columns:

| Question | CoT Method | Generated Reasoning | Final Answer |
|----------|------------|---------------------|--------------|

- Each question should have **5 rows** (one per method).
- Include **full reasoning text** (not summarized).
- For Self-Consistency:
  - Include all 5 reasoning traces in the "Generated Reasoning" column.
  - Clearly indicate the majority answer.

---

## Questions

1. A shop sells 3 apples for $5. If the price increases by 20%, how much will 12 apples cost?  
2. A farmer has 8 cows and buys 5 more. He then sells half of his total cows and later buys 3 calves. How many cows does he have now?  
3. Copper wire, wooden stick, and rubber band are placed in an electric circuit. Which one lets current flow and why?  
4. A plant receives less sunlight but the same amount of water and nutrients. How will its rate of photosynthesis and growth change, and why?  
5. Mary put her cup on the table and left. John came, moved it to the shelf, and took the book that was under it. Where is the cup now, and who has the book?  
6. You run a two-sample Z-test for the difference in means and the confidence interval length is too wide. How to fix it?  
7. You are a data scientist at Doordash and run a regression with conversion as response and ETA as predictor. The coefficient is negative. How to fix it?

---

## Additional Instructions

- Be precise and structured.
- Do not skip reasoning steps.
- Ensure answers are logically consistent.
- Use clear formatting for readability.
```


Python code

```

## Preparation
```python
from google import genai

client = genai.Client(api_key="AIzaSyC1SUudY4R2tslnwivz1r8hsVYtWiq4mqM")

# Testing with the Lite model
response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview", contents="Explain how AI works in a few words"
)
print(response.text)
```


## Questions

```python
questions = [
    "A shop sells 3 apples for $5. If the price increases by 20%, how much will 12 apples cost?",
    "A farmer has 8 cows and buys 5 more. He then sells half of his total cows and later buys 3 calves. How many cows does he have now?",
    "Copper wire, wooden stick, and rubber band are placed in an electric circuit. Which one lets current flow and why?",
    "A plant receives less sunlight but the same amount of water and nutrients. How will its rate of photosynthesis and growth change, and why?",
    "Mary put her cup on the table and left. John came, moved it to the shelf, and took the book that was under it. Where is the cup now, and who has the book?",
    "You run a two-sample Z-test for the difference in means and the confidence interval length is too wide. How to fix it?",
    "You are a data scientist at Doordash and run a regression with conversion as response and ETA as predictor. The coefficient is negative. How to fix it?"
]

for i, question in enumerate(questions):
    print(f"Question {i+1}: {question}")
```

## Solved examples

```python
solved_examples = [
    {
        "question": "A shop sells 3 apples for $5. If the price increases by 20%, how much will 12 apples cost?",
        "examples": [
            {
                "context": "3 apples cost $5. Price increases by 20%. Cost of 12 apples?",
                "solution": "Original price per apple = 5 \u00f7 3 = $1.67\nNew price = 1.67 \u00d7 1.20 = $2.00\nCost of 12 apples = 12 \u00d7 2 = $24"
            },
            {
                "context": "3 apples cost $6. Price increases by 20%. Cost of 12 apples?",
                "solution": "Price per apple = 6 \u00f7 3 = $2\nNew price = 2 \u00d7 1.20 = $2.40\nCost of 12 apples = 12 \u00d7 2.40 = $28.80"
            },
            {
                "context": "3 apples cost $9. Price increases by 20%. Cost of 12 apples?",
                "solution": "Price per apple = 9 \u00f7 3 = $3\nNew price = 3 \u00d7 1.20 = $3.60\nCost of 12 apples = 12 \u00d7 3.60 = $43.20"
            }
        ]
    },
    {
        "question": "A farmer has 8 cows and buys 5 more. He then sells half of his total cows and later buys 3 calves. How many cows does he have now?",
        "examples": [
            {
                "context": "Start: 8 cows",
                "solution": "Start: 8 cows\nBuys 5 \u2192 13 cows\nSells half \u2192 13 \u00f7 2 = 6.5 (realistically 6 or 7; assume 6 sold, 7 left)\nBuys 3 \u2192 7 + 3 = 10 cows"
            },
            {
                "context": "Variation: Start with 10 cows",
                "solution": "Buys 6 \u2192 16\nSells half \u2192 8\nBuys 2 \u2192 10 cows"
            },
            {
                "context": "Variation: Start with 12 cows",
                "solution": "Buys 4 \u2192 16\nSells half \u2192 8\nBuys 5 \u2192 13 cows"
            }
        ]
    },
    {
        "question": "Copper wire, wooden stick, and rubber band are placed in an electric circuit. Which one lets current flow and why?",
        "examples": [
            {
                "context": None,
                "answer": "Copper wire lets current flow",
                "why": "Copper is a good conductor due to free electrons"
            },
            {
                "context": None,
                "answer": "Wooden stick does NOT let current flow",
                "why": "Wood is an insulator (no free electrons)"
            },
            {
                "context": None,
                "answer": "Rubber band does NOT let current flow",
                "why": "Rubber is an insulator and blocks current"
            }
        ]
    },
    {
        "question": "A plant receives less sunlight but the same amount of water and nutrients. How will its rate of photosynthesis and growth change, and why?",
        "examples": [
            {
                "context": None,
                "answer": "Photosynthesis decreases\nGrowth slows",
                "why": "Light is essential for photosynthesis"
            },
            {
                "context": None,
                "answer": "Very low sunlight \u2192 very low photosynthesis\nPlant may become weak or die",
                "why": "Energy production is limited"
            },
            {
                "context": None,
                "answer": "Moderate reduction \u2192 slower growth, not stopped",
                "why": "Some photosynthesis still occurs"
            }
        ]
    },
    {
        "question": "Mary put her cup on the table and left. John came, moved it to the shelf, and took the book that was under it. Where is the cup now, and who has the book?",
        "examples": [
            {
                "context": None,
                "answer": "Cup \u2192 on the shelf\nBook \u2192 with John"
            },
            {
                "context": "Variation: If John moves cup to desk",
                "answer": "Cup \u2192 desk\nBook \u2192 with John"
            },
            {
                "context": "Variation: If John doesn\u2019t take the book",
                "answer": "Cup \u2192 shelf\nBook \u2192 remains where it was"
            }
        ]
    },
    {
        "question": "You run a two-sample Z-test for the difference in means and the confidence interval length is too wide. How to fix it?",
        "examples": [
            {
                "context": None,
                "fix": "Increase sample size",
                "why": "Larger samples reduce standard error"
            },
            {
                "context": None,
                "fix": "Reduce variability",
                "why": "Lower variance narrows interval"
            },
            {
                "context": None,
                "fix": "Use lower confidence level (e.g., 95% \u2192 90%)",
                "why": "Smaller margin of error"
            }
        ]
    },
    {
        "question": "You are a data scientist at Doordash and run a regression with conversion as response and ETA as predictor. The coefficient is negative. How to fix it?",
        "examples": [
            {
                "context": None,
                "issue": "Longer ETA reduces conversion (negative coefficient)",
                "fix": "This may be correct \u2014 interpret it",
                "reason": "Customers prefer faster delivery"
            },
            {
                "context": None,
                "fix": "Check confounders",
                "reason": "Add variables (price, restaurant rating)\nOmitted variables bias results"
            },
            {
                "context": None,
                "fix": "Check causality",
                "reason": "Use experiment or instrumental variables\nCorrelation \u2260 causation"
            }
        ]
    }
]
```

## Response Parsor

```python
import re

def parse_response(response_text):
    """
    Parses the text responses from a language model to extract 'Generated Reasoning'
    and 'Final Answer'.

    Args:
        response_text (str): The raw text response from the language model.

    Returns:
        dict: A dictionary with two keys: 'reasoning' and 'answer',
              containing the extracted strings. Returns empty string if a component
              cannot be extracted.
    """
    reasoning = ""
    final_answer = ""

    response_text = response_text.strip()

    # Try to extract Final Answer first (case-insensitive)
    final_answer_pattern = r"Final Answer:\s*(.*)"
    final_answer_match = re.search(final_answer_pattern, response_text, re.DOTALL | re.IGNORECASE)

    if final_answer_match:
        final_answer = final_answer_match.group(1).strip()
        # The reasoning should be in the text before the "Final Answer:" marker
        text_for_reasoning = response_text[:final_answer_match.start()].strip()
    else:
        # If no "Final Answer:" marker, the entire text might contain reasoning or be just an answer
        text_for_reasoning = response_text

    # Now try to extract Generated Reasoning from the relevant text (case-insensitive)
    reasoning_pattern = r"Generated Reasoning:\s*(.*)"
    reasoning_match = re.search(reasoning_pattern, text_for_reasoning, re.DOTALL | re.IGNORECASE)

    if reasoning_match:
        reasoning = reasoning_match.group(1).strip()

    # Special handling: If no explicit markers for either, assume the whole text is the answer.
    if not final_answer_match and not reasoning_match:
        final_answer = response_text

    return {"reasoning": reasoning, "answer": final_answer}

print("Function `parse_response` defined.")
```

## Zero-shot COT strategy

```python
import time

model_name = "gemini-3.1-flash-lite-preview"
max_retries = 5
retry_delay_seconds = 10

print(f"Applying Zero-Shot CoT strategy with model: {model_name}")

for i, question_text in enumerate(questions):
    prompt = f"{question_text} Let's think step by step."
    
    attempt = 0
    success = False
    while attempt < max_retries and not success:
        try:
            # Generate content from the model
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            model_response_text = response.text

            # Parse the response
            parsed_output = parse_response(model_response_text)

            # Store the results
            all_results.append({
                "question": question_text,
                "method": "Zero-Shot CoT",
                "reasoning": parsed_output["reasoning"],
                "answer": parsed_output["answer"]
            })
            print(f"Processed question {i+1}/{len(questions)} (Attempt {attempt + 1})")
            success = True

        except Exception as e:
            attempt += 1
            error_message = str(e)
            if attempt < max_retries:
                print(f"Error processing question {i+1} (Attempt {attempt}): {error_message}. Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)
            else:
                print(f"Failed to process question {i+1} after {max_retries} attempts: {error_message}")
                all_results.append({
                    "question": question_text,
                    "method": "Zero-Shot CoT",
                    "reasoning": f"Error during generation: {error_message}",
                    "answer": f"Error during generation: {error_message}"
                })

print(f"Finished processing {len(all_results)} questions with Zero-Shot CoT.")
print(f"First result entry: {all_results[0] if all_results else 'No results'}")
```

## Few-shot COT strategy

```python
import time

model_name = "gemini-3.1-flash-lite-preview"
max_retries = 5
retry_delay_seconds = 10

print(f"Applying Few-Shot CoT strategy with model: {model_name}")

# It's good practice to clear results or use a separate list for Few-Shot CoT if you want to compare.
# For this task, we will append to all_results, assuming previous runs populated it with Zero-Shot results.
# If you wanted to run Few-Shot exclusively, you might do: all_results = [] here.

for i, question_text in enumerate(questions):
    # Find the corresponding solved_example for the current question
    current_solved_example = next((ex for ex in solved_examples if ex["question"] == question_text), None)

    if not current_solved_example:
        print(f"Warning: No solved example found for question: {question_text}. Skipping Few-Shot CoT for this question.")
        continue

    # Construct the examples part of the prompt
    example_prompt_parts = []
    for example in current_solved_example.get("examples", []):
        if "context" in example and example["context"] is not None:
            example_prompt_parts.append(f"Question: {example["context"]}")
        elif "answer" in example:
            # Handle cases where examples might have a simple answer structure
            example_prompt_parts.append(f"Question: {current_solved_example["question"]}") # Re-use original question for context if example context is missing

        example_prompt_parts.append(f"Generated Reasoning: {example.get('solution', example.get('why', ''))}")
        example_prompt_parts.append(f"Final Answer: {example.get('answer', example.get('solution', '')).strip()}")
        example_prompt_parts.append("\n") # Add a newline to separate examples

    # Combine example parts, current question, and instruction
    prompt = "\n".join(example_prompt_parts) + f"Question: {question_text} Let's think step by step."

    attempt = 0
    success = False
    while attempt < max_retries and not success:
        try:
            # Generate content from the model
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            model_response_text = response.text

            # Parse the response
            parsed_output = parse_response(model_response_text)

            # Store the results
            all_results.append({
                "question": question_text,
                "method": "Few-Shot CoT",
                "reasoning": parsed_output["reasoning"],
                "answer": parsed_output["answer"]
            })
            print(f"Processed question {i+1}/{len(questions)} (Few-Shot CoT, Attempt {attempt + 1})")
            success = True

        except Exception as e:
            attempt += 1
            error_message = str(e)
            if attempt < max_retries:
                print(f"Error processing question {i+1} (Few-Shot CoT, Attempt {attempt}): {error_message}. Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)
            else:
                print(f"Failed to process question {i+1} (Few-Shot CoT) after {max_retries} attempts: {error_message}")
                all_results.append({
                    "question": question_text,
                    "method": "Few-Shot CoT",
                    "reasoning": f"Error during generation: {error_message}",
                    "answer": f"Error during generation: {error_message}"
                })

print(f"Finished processing {len(questions)} questions with Few-Shot CoT.")
print(f"First Few-Shot result entry: {next((r for r in all_results if r['method'] == 'Few-Shot CoT'), 'No results')}")
```


## Self-refine COT strategy
```python
import time

model_name = "gemini-3.1-flash-lite-preview"
max_retries = 3
retry_delay_seconds = 5

print(f"Applying Self-Refine / Critic Strategy with model: {model_name}")

for i, question_text in enumerate(questions):
    # --- Step 1: Generate initial response ---
    initial_prompt = question_text

    initial_response_text = ""
    parsed_initial_output = {"reasoning": "", "answer": ""}
    
    attempt = 0
    success = False
    while attempt < max_retries and not success:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=initial_prompt
            )
            initial_response_text = response.text
            parsed_initial_output = parse_response(initial_response_text)
            success = True
        except Exception as e:
            attempt += 1
            error_message = str(e)
            if attempt < max_retries:
                print(f"Error generating initial response for question {i+1} (Attempt {attempt}): {error_message}. Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)
            else:
                print(f"Failed to generate initial response for question {i+1} after {max_retries} attempts: {error_message}")
                parsed_initial_output["reasoning"] = f"Error during initial generation: {error_message}"
                parsed_initial_output["answer"] = f"Error during initial generation: {error_message}"
                break # Exit retry loop if all retries fail

    # --- Step 2: Construct self-refine prompt ---
    self_refine_prompt = (
        f"Original Question: {question_text}\n\n"
        f"Initial Generated Reasoning: {parsed_initial_output['reasoning']}\n"
        f"Initial Final Answer: {parsed_initial_output['answer']}\n\n"
        "Review your reasoning and correct any mistakes. Provide your revised reasoning and final answer."
    )

    # --- Step 3: Generate refined response ---
    refined_response_text = ""
    parsed_refined_output = {"reasoning": "", "answer": ""}

    attempt = 0
    success = False
    while attempt < max_retries and not success:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=self_refine_prompt
            )
            refined_response_text = response.text
            parsed_refined_output = parse_response(refined_response_text)
            success = True
        except Exception as e:
            attempt += 1
            error_message = str(e)
            if attempt < max_retries:
                print(f"Error generating refined response for question {i+1} (Attempt {attempt}): {error_message}. Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)
            else:
                print(f"Failed to generate refined response for question {i+1} after {max_retries} attempts: {error_message}")
                parsed_refined_output["reasoning"] = f"Error during refinement generation: {error_message}"
                parsed_refined_output["answer"] = f"Error during refinement generation: {error_message}"
                break # Exit retry loop if all retries fail

    # Store the results of the refined response
    all_results.append({
        "question": question_text,
        "method": "Self-Refine / Critic",
        "reasoning": parsed_refined_output["reasoning"],
        "answer": parsed_refined_output["answer"]
    })
    print(f"Processed question {i+1}/{len(questions)} (Self-Refine / Critic, Attempt {attempt + 1 if success else 'Failed'})")

print(f"Finished processing {len(questions)} questions with Self-Refine / Critic.")
print(f"First Self-Refine result entry: {next((r for r in all_results if r['method'] == 'Self-Refine / Critic'), 'No results')}")
```