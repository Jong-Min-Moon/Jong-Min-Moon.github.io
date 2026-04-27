---
layout: distill
title: "Understanding Chain-of-Thought Prompting: Why LLMs Need to 'Think' Before They Speak"
description: "A pedagogical look at Chain-of-Thought (CoT) prompting, its theoretical foundations, and its impact on LLM reasoning."
tags: distill language-models prompting ise-547
categories: ise-547
date: 2026-04-27
featured: false
project: ise-547
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

- LLMs emerge with the capability for step-by-step reasoning through in-context learning

Pre-training then prompting has gradually replaced pre-training then fine-tuning as the new paradigm in natural language processing.

First, we consider the few-shot standard prompting scenario, where prompt $T_{SP}$ includes instruction $I$ and few-shot demonstrations (several question-answer pairs). The model takes the question $Q$ and prompt $T$ as inputs and produces the answer prediction $A$ as its output, as shown in Equ. (1, 2).

<p>
$$T_{SP} = \{I, (x_1, y_1), \dots , (x_n, y_n)\} \tag{1}$$

$$p(A | T, Q) = \prod_{i=1}^{|A|} p_{LM}(a_i | T, Q, a_{<i}) \tag{2}$$
</p>

Next, we consider chain-of-thought prompting under a few-shot setting, wherein the prompt $T_{CoT}$ includes instruction, questions, answers, and rationales $e_i$. In chain-of-thought reasoning, the model no longer directly generates answers. Instead, it generates step-by-step reasoning trajectories $R$ before giving answers $A$, as shown in Equ. (3, 4, 5, 6).

<p>
$$T_{CoT} = \{I, (x_1, e_1, y_1), \dots , (x_n, e_n, y_n)\} \tag{3}$$

$$p(A, R | T, Q) = p(A | T, Q, R) \cdot p(R | T, Q) \tag{4}$$

$$p(R | T, Q) = \prod_{i=1}^{|R|} p_{LM}(r_i | T, Q, r_{<i}) \tag{5}$$ (same format as $p(A | T, Q) $, just A changed into R)

$$p(A | T, Q, R) = \prod_{j=1}^{|A|} p_{LM}(a_j | T, Q, R, a_{<j}) \tag{6}$$
</p>
- Note that reasonings are completed and then the answers are genereated. It's not zig zag.


### Advantages

- **Boosted Reasoning.** Chain-of-thought reasoning breaks down complex problems into manageable steps and establishes connections among these steps, thereby facilitating reasoning.
- **Offering Interpretability.** Chain-ofthought reasoning provides observable reasoning traces, allowing the user to understand the model’s decision, making the reasoning process transparent and trustworthy.
- **Advance Collaboration.** Fine-grained reasoning traces facilitate user-system interaction, allowing for altering the model’s execution trajectory, thereby fostering the development of autonomous agents powered by LLMs.
