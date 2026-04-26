---
layout: page
title: Road Trip Advisor Chatbot
description: Llama-3.1-8B-Instruct fine-tuned chatbot trained on road trip questions and answers data.
importance: 3
---

<iframe
	src="https://jongminm-roadtrip-advisor.hf.space"
	frameborder="0"
	width="850"
	height="650"
></iframe>



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

Here is the neatly formatted, Markdown-ready version of your Jupyter Notebook script. 

I’ve converted the notebook text blocks into standard Markdown headers and paragraphs, placed all the Python code into syntax-highlighted blocks, and cleaned up the non-breaking spaces from the original text so the code is completely copy-pasteable without throwing indentation errors.

***

# Code: Road Trip Chatbot Fine-Tuning with Unsloth


## Installation

First, install the necessary dependencies. This handles the Unsloth environment and specific versions of `transformers` and `trl`.

```python
# %%capture
# import os, re
# if "COLAB_" not in "".join(os.environ.keys()):
#     !pip install unsloth  # Do this in local & cloud setups
# else:
#     import torch; v = re.match(r'[\d]{1,}\.[\d]{1,}', str(torch.__version__)).group(0)
#     xformers = 'xformers==' + {'2.10':'0.0.34','2.9':'0.0.33.post1','2.8':'0.0.32.post2'}.get(v, "0.0.34")
#     !pip install sentencepiece protobuf "datasets==4.3.0" "huggingface_hub>=0.34.0" hf_transfer
#     !pip install --no-deps unsloth_zoo bitsandbytes accelerate {xformers} peft trl triton unsloth
# !pip install transformers==4.56.2
# !pip install --no-deps trl==0.22.2
```

## Model Loading

Initialize Unsloth's `FastLanguageModel`. We use 4-bit quantization to reduce memory usage.

```python
from unsloth import FastLanguageModel
import torch

max_seq_length = 1024 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

# 4bit pre-quantized models we support for 4x faster downloading + no OOMs.
fourbit_models = [
    "unsloth/Llama-3.1-8B-bnb-4bit",      # Llama-3.1 15 trillion tokens model 2x faster!
    "unsloth/Llama-3.1-8B-Instruct-bnb-4bit",
    "unsloth/Llama-3.1-70B-bnb-4bit",
    "unsloth/Llama-3.1-405B-bnb-4bit",    # We also uploaded 4bit for 405b!
    "unsloth/Mistral-Nemo-Base-2407-bnb-4bit", # New Mistral 12b 2x faster!
    "unsloth/Mistral-Nemo-Instruct-2407-bnb-4bit",
    "unsloth/mistral-7b-v0.3-bnb-4bit",        # Mistral v3 2x faster!
    "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
    "unsloth/Phi-3.5-mini-instruct",           # Phi-3.5 2x faster!
    "unsloth/Phi-3-medium-4k-instruct",
    "unsloth/gemma-2-9b-bnb-4bit",
    "unsloth/gemma-2-27b-bnb-4bit",            # Gemma 2x faster!
] # More models at https://huggingface.co/unsloth

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)
```

## LoRA Adapters

We now add LoRA adapters so we only need to update 1 to 10% of all parameters.

```python
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)
```

## Dataset Preparation

Load and format the data using the Llama-3.1 Chat Template.

```python
import pandas as pd
from datasets import Dataset
from unsloth.chat_templates import get_chat_template

# 1. Apply the Llama-3.1 Chat Template
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3.1",
)

# 2. Load the Excel file directly
# (Make sure "fine_tune_data.xlsx" is uploaded to your Colab files!)
df = pd.read_excel('fine_tune_data.xlsx')

# 3. Keep the relevant columns and drop any empty rows
df = df[['User content', 'Assistant content']].dropna()

# 4. Format into the ChatML structure
def format_row(row):
    return {
        "messages": [
            {"role": "user", "content": str(row['User content']).strip()},
            {"role": "assistant", "content": str(row['Assistant content']).strip()}
        ]
    }

formatted_data = df.apply(format_row, axis=1).tolist()
chat_df = pd.DataFrame(formatted_data)

# 5. Convert to a Hugging Face Dataset
dataset = Dataset.from_pandas(chat_df)

# 6. Apply the formatting to convert 'messages' into text prompts for Llama 3.1
def formatting_prompts_func(examples):
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize=False, add_generation_prompt=False) for convo in convos]
    return { "text" : texts }

dataset = dataset.map(formatting_prompts_func, batched = True)

# Verify the first row looks correct
print(dataset[0]['text'])
```

## Train the Model

Now let's train our model. Because your dataset is only 30 rows, running `max_steps = 60` with gradient accumulation will drastically overfit the model or crash because it runs out of data. We need to switch from step-based training to epoch-based training.

```python
from trl import SFTConfig, SFTTrainer

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    packing = False, # Can make training 5x faster for short sequences.
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        num_train_epochs = 20,
        learning_rate = 2e-4,
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.001,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none", # Use TrackIO/WandB etc
    ),
)

# Show current memory stats
gpu_stats = torch.cuda.get_device_properties(0)
start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)

print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
print(f"{start_gpu_memory} GB of memory reserved.")

trainer_stats = trainer.train()
```

## Inference

Let's run the model! You can change the instruction and input—leave the output blank.

```python
FastLanguageModel.for_inference(model)

messages = [
    {"role": "user", "content": "I am driving from Texas to California, any route tips? I will stop by at Tuscon"}
]

# 1. Add return_dict=True so it packages the attention_mask for you
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True
).to("cuda")

from transformers import TextStreamer
text_streamer = TextStreamer(tokenizer, skip_prompt=True)

# 2. Unpack inputs with ** and explicitly state the pad_token_id
_ = model.generate(
    **inputs,
    streamer=text_streamer,
    max_new_tokens=128,
    pad_token_id=tokenizer.eos_token_id
)
```

## Evaluation

We evaluate the fine-tuned model against the base Llama-3.1 model using LLM-as-a-judge (Gemini).

### Baseline Inference

```python
import torch
import gc
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

# 1. Define your test set (Unseen data)
test_prompts = [
    "I'm the only driver and I plan to drive 14 hours a day for 4 days straight to get from Seattle to Miami. What energy drinks or snacks do you recommend to stay awake?",
    "Driving from NYC to Los Angeles. I only have 3 days total for the whole trip. What are the absolute must-see stops along the way?",
    "Planning a road trip from Boston to DC on the Friday afternoon before Thanksgiving. I want to take I-95 straight down through New York and Philly. Good idea?",
    "Driving from Dallas to El Paso tomorrow. Going straight through on I-20 and I-10. Are there any cool hidden gems on this route or should I just power through?",
    "I'm doing a 5-day trip in Utah. I want to see Zion, Bryce, Capitol Reef, Canyonlands, Arches, and also spend a day at the Grand Canyon in Arizona. What's the best itinerary to fit this all in?",
    "Road trip down the California coast! We have 2 days to get from San Francisco to San Diego. We want to stop and hike in Big Sur, see the Hollywood sign, and spend a few hours at Santa Monica pier.",
    "Me and my buddies are driving a convertible from Chicago to Denver in mid-January. What scenic backroads should we take through the mountains?",
    "Driving through Death Valley in mid-August. I want to do some dispersed camping a few miles off the main paved road to save money. What kind of tent do I need?",
    "Taking my 2004 Honda Civic with 200,000 miles on a 4,000-mile road trip through the Rockies. Any tips for mountain driving?",
    "Renting an RV for the absolute first time! We are going from SF down Highway 1 to LA. I hear the cliff views are great. Any RV-specific tips for driving that specific road?"
]

# 2. Load the BASE model
max_seq_length = 2048
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    load_in_4bit = True,
)
tokenizer = get_chat_template(tokenizer, chat_template="llama-3.1")
FastLanguageModel.for_inference(model)

# 3. Define the Prompt Engineering baseline
sys_prompt = "You are a blunt, experienced road trip advisor. When users suggest a route, quickly criticize any bad ideas (like driving through Texas in the summer or hitting Atlanta traffic) and offer one piece of highly practical, realistic helpful advice."

baseline_responses = []

print("Generating Baseline Responses...")
for prompt in test_prompts:
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": prompt}
    ]
    inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=128, pad_token_id=tokenizer.eos_token_id)

    # Slice the output to only get the assistant's new response (ignore the prompt)
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    baseline_responses.append(response)

# 4. CLEAR MEMORY so the next model can load safely
del model, tokenizer
gc.collect()
torch.cuda.empty_cache()
print("Baseline generated and memory cleared!")
```

### Fine-Tuned Inference

```python
# 1. Load your FINE-TUNED model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "llama_lora_reddit_roadtrip", # The folder where your adapters were saved
    max_seq_length = max_seq_length,
    load_in_4bit = True,
)
tokenizer = get_chat_template(tokenizer, chat_template="llama-3.1")
FastLanguageModel.for_inference(model)

finetuned_responses = []

print("Generating Fine-Tuned Responses...")
for prompt in test_prompts:
    # Notice: No system prompt here! We rely purely on the fine-tuning.
    messages = [
        {"role": "user", "content": prompt}
    ]
    inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=128, pad_token_id=tokenizer.eos_token_id)

    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    finetuned_responses.append(response)

# CLEAR MEMORY again
del model, tokenizer
gc.collect()
torch.cuda.empty_cache()
print("Fine-tuned generated and memory cleared!")
```

### Save Evaluation Results

```python
import pandas as pd
from google.colab import files

# 1. Combine the lists into a pandas DataFrame
results_df = pd.DataFrame({
    "Question": test_prompts,
    "Baseline Response": baseline_responses,
    "Fine-Tuned Response": finetuned_responses
})

# 2. Save the DataFrame to a CSV file
csv_filename = "evaluation_results.csv"
results_df.to_csv(csv_filename, index=False, encoding='utf-8')

print(f"Results successfully saved to {csv_filename}!")

# 3. Automatically download the file to your computer
files.download(csv_filename)
```

### LLM-as-a-Judge (Gemini)

```python
import os
import random
import time
import google.generativeai as genai
from google.api_core import exceptions

# Initialize the Gemini judge
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

judge_model = genai.GenerativeModel('gemini-1.5-flash')

# Updated scoreboard to track both dimensions
results = {
    "Criticism": {"Baseline Wins": 0, "Fine-Tuned Wins": 0, "Ties": 0},
    "Helpfulness": {"Baseline Wins": 0, "Fine-Tuned Wins": 0, "Ties": 0}
}

for i, prompt in enumerate(test_prompts):
    baseline_ans = baseline_responses[i]
    finetuned_ans = finetuned_responses[i]

    # Blind the test
    is_baseline_a = random.choice([True, False])
    ans_a = baseline_ans if is_baseline_a else finetuned_ans
    ans_b = finetuned_ans if is_baseline_a else baseline_ans

    # UPDATED PROMPT: Asks for two specific lines at the end
    judge_prompt = f"""You are an impartial judge evaluating two AI assistants. The user is asking for road trip advice.
Please evaluate which Assistant performs better across two dimensions:
1. Criticism: Does the assistant actively identify and critique poor routing, unrealistic timelines, or bad ideas in a direct manner, with proper reasons without unnecessary offends?
2. Helpfulness: Does the assistant provide grounded, practical, and highly relevant advice?

[User Question]: {prompt}

[Assistant A]: {ans_a}

[Assistant B]: {ans_b}

Evaluate both assistants. Then, on a new line at the very end of your response, explicitly declare the winners for EACH category by writing EXACTLY these two lines:
Criticism Winner: [A, B, or Tie]
Helpfulness Winner: [A, B, or Tie]
"""

    max_retries = 5
    judge_eval = ""

    for attempt in range(max_retries):
        try:
            response = judge_model.generate_content(
                judge_prompt,
                generation_config=genai.GenerationConfig(temperature=0.0)
            )
            judge_eval = response.text
            break

        except (exceptions.ServiceUnavailable, exceptions.ResourceExhausted, exceptions.InternalServerError) as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)

    # --- UPDATED PARSING LOGIC ---
    crit_winner_raw = "Tie"
    help_winner_raw = "Tie"

    for line in judge_eval.split('\n'):
        if "Criticism Winner:" in line:
            crit_winner_raw = line.split(":")[1].strip().replace("[", "").replace("]", "")
        elif "Helpfulness Winner:" in line:
            help_winner_raw = line.split(":")[1].strip().replace("[", "").replace("]", "")

    def map_winner(raw_winner, is_baseline_a):
        if raw_winner == "A":
            return "Baseline" if is_baseline_a else "Fine-Tuned"
        elif raw_winner == "B":
            return "Fine-Tuned" if is_baseline_a else "Baseline"
        return "Tie"

    crit_winner = map_winner(crit_winner_raw, is_baseline_a)
    help_winner = map_winner(help_winner_raw, is_baseline_a)

    print(f"\n--- Query {i+1} ---")
    print(f"Criticism Winner: {crit_winner}")
    print(f"Helpfulness Winner: {help_winner}")
    print(f"Judge Rationale:\n{judge_eval}")

    # Tally results
    if crit_winner == "Baseline": results["Criticism"]["Baseline Wins"] += 1
    elif crit_winner == "Fine-Tuned": results["Criticism"]["Fine-Tuned Wins"] += 1
    else: results["Criticism"]["Ties"] += 1

    if help_winner == "Baseline": results["Helpfulness"]["Baseline Wins"] += 1
    elif help_winner == "Fine-Tuned": results["Helpfulness"]["Fine-Tuned Wins"] += 1
    else: results["Helpfulness"]["Ties"] += 1

print("\n=========================")
print("      FINAL RESULTS      ")
print("=========================")
print("\n--- CRITICISM ---")
for k, v in results["Criticism"].items():
    print(f"{k}: {v}")

print("\n--- HELPFULNESS ---")
for k, v in results["Helpfulness"].items():
    print(f"{k}: {v}")
```

## Save Finetuned Models

 
```python
# Create a free account at huggingface.co and get an Access Token from your settings
HF_TOKEN = " "

# Push the model to Hugging Face in the highly-compressed Q4_K_M format
model.push_to_hub_gguf(
    "jongminm/roadtrip-advisor-bot", # Change this to your username!
    tokenizer,
    quantization_method="q4_k_m",
    token=HF_TOKEN
)
```