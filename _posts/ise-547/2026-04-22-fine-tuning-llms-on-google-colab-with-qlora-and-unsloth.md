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

# Motivation

Planning a road trip is a hassle. People can strat with their initial plans based on their preferences and knwoledge and than start modifying it by chatting with LLMs. 
However, LLMs are known to be notoriously flattering. They may not be able to find  flaws in your initial plan and they may agree with your unreasonable requests.  In contrast, users in reddit roadtrip subreddits are known to be quite critical but at the same time they  provide very helpful comments. Therefore, I was motivated to fine-tune an LLM that can generate critical-but-helpful comments for road trip planning. 



# Data
The paper LIMA: Less Is More for Alignment (neurips 2025) written by Meta researchers show that small number (around 1000) of high-quality training data is enough for fine-tuning. Which means that the quality (and diversity) outwieghs quantity when it comes to fine-tuning. 

I thus collected, in person,  30 samples of (User content, Assistant content) pairs from reddit roadtrip subreddits. I chose comment that explicitly express criticisim to the user's initial plan, but than they provide very helpful comments. For example, the following is a sample of my collected data

```
question: Zion → Grand Canyon → Vegas → California coast → Yosemite → San Francisco in 16-20 days? 
answer: Vegas sucks, but start there and get your jet lag out of the way there at first. Then add more time to add some of the other Utah parks
```

I pre-processed the data into the following format
```
{
  "messages": [
    {
      "role": "user",
      "content": "Zion → Grand Canyon → Vegas → California coast → Yosemite → San Francisco in 16-20 days? "
    },
    {
      "role": "assistant",
      "content": "Vegas sucks, but start there and get your jet lag out of the way there at first. Then add more time to add some of the other Utah parks"
    }
  ]
}

# Method
I aim to fine-tune a model on a Google Colab Tesla T4 (which has 16GB of VRAM) in under an hour using  **4-bit Quantization (QLoRA)**. 
Since my dataset is very small ($N=30$), the actual training time will take less than an hour.

 Pretrained model I will use is *   **Llama-3-8B-Instruct :**   A 8B parameter model normally wouldn't fit on a T4, but using 4-bit quantization, it only takes about 6-7GB of VRAM.

 I will use the [Unsloth library](https://github.com/unslothai/unsloth) to speed up the training process. Unsloth is a library that speeds up the training process of LLMs by using 4-bit quantization and other optimization techniques. THey also provide the colab notebook.

# Result

# Data Preprocessing

I inspected your `fine_tune_data.xlsx - Sheet1.csv` file. Here is what you need to know about it:

*   It contains exactly 30 valid rows.
*   The actual text is in `User content` and `Assistant content`.
*   There are two noisy columns (`Unnamed: 0` and `Unnamed: 3`) that contain NaN values and stray URLs which need to be dropped.

Modern LLMs expect data to be formatted as a "Chat" or "Messages" list. I have written the code below that you can copy and paste directly into your Google Colab notebook to load, clean, and format the data using the Hugging Face `datasets` library:

```python
import pandas as pd
from datasets import Dataset

# 1. Load the data
df = pd.read_csv('fine_tune_data.xlsx - Sheet1.csv')

# 2. Drop the empty/noisy columns and keep only the text
df = df[['User content', 'Assistant content']]

# 3. Handle any potential missing values (just in case)
df = df.dropna()

# 4. Reformat into the standard Hugging Face ChatML/Message format
def format_chat(row):
    return {
        "messages": [
            {"role": "user", "content": str(row['User content']).strip()},
            {"role": "assistant", "content": str(row['Assistant content']).strip()}
        ]
    }

# Apply the formatting
formatted_data = df.apply(format_chat, axis=1).tolist()
chat_df = pd.DataFrame(formatted_data)

# 5. Convert to Hugging Face Dataset object for training
hf_dataset = Dataset.from_pandas(chat_df)

# Check the first row to ensure it looks right
print(hf_dataset[0]['messages'])
```

*(Note: I also went ahead and processed this for you in the background! I wrote the cleaned, ready-to-train files to your working directory as `cleaned_chat_data.csv` and `cleaned_chat_data.jsonl` if you prefer to just upload the cleaned JSONL directly to Colab).*

# Next Steps for Colab

1.  **Open a new Google Colab notebook** and select **T4 GPU** in the Runtime settings.
2.  **Go to the Unsloth GitHub page** and copy their standard Llama 3 or Phi-3 conversational Colab notebook.
3.  **Replace their sample dataset step** with the preprocessing code above.
4.  **Set your training parameters:** Because $N=30$ is so small, set `num_train_epochs` to something between 3 and 5, and set `per_device_train_batch_size` to 2.
