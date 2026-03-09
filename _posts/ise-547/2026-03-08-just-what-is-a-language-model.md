---
layout: distill
title: "JUST WHAT IS A LANGUAGE MODEL?"
description: "An introduction to language models: prediction, generation, and probabilities."
tags: distill language-models
categories: ise-547
date: 2026-03-08
featured: false
project: ise-547
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

A language model is a **statistical model** designed to predict and generate plausible language. These models work by estimating the probability of a token or sequence of tokens occurring within a longer sequence of tokens.

### Plausible language
Plausible language refers to human-generated language—that is, language written by people and intended to be read by people. For example, articles from the The Wall Street Journal represent plausible language because they are produced by human writers for human readers.	

### Statistical model
A language model is **not necessarily a machine learning model**. More generally, it is a statistical model.

What makes a model statistical is the presence of parameters that must be estimated from data. Once we assume a model with unknown parameters and estimate those parameters using observed data, we are working within a statistical framework.

For example, predicting tokens using maximum likelihood estimation (MLE) is a statistical approach. Because it assumes parameters and estimates them from language data, it qualifies as a language model.

The key point is that a language model assumes parameters and estimates them from data. What defines it as statistical is the existence of parameters to estimate, not the specific method used to estimate them.

### Within a Longer Sequence of Tokens
A language model learns a conditional distribution. The word conditional is extremely important here. The model learns the probability of a token (or a sequence of tokens) given a context, where the context is another token or sequence of tokens occurring earlier within a longer sequence of tokens.

In other words, a language model estimates the probability of language conditioned on its surrounding context.

Because of this, marginal probabilities are generally not very meaningful in language modeling. What matters instead are conditional probabilities—the probability of a token given the context that precedes it.

# MORE FORMALLY...

A statistical model of language can be represented by the conditional probability of the next word given all the previous ones, since

$$\hat{P}(w_1^T) = \prod_{t=1}^{T} \hat{P}(w_t|w_1^{t-1}),$$

$w_t$ is the $t$-th word, and writing sub-sequence $w_i^j = (w_i, w_{i+1}, \dots, w_{j-1}, w_j)$.
What researchers do is to estimate the conditonal probabilities on the right-hand side from data.







`When I hear rain on my roof, I _______ in my kitchen.`
Here, if you use 'in my kitchen' to predict the blank, it is not the language model. the blank should only depend on previous tokens, not the future tokens.  

### Intuitively:
If a langauge model is a good model, than it would assign higher probability to the plausiable labuage (lefthand side) than the implausible language (righthand side).

* **P(We notice a man) > P(We are man notice)**
* **P(We notice a man) > P(A plant notice a man)**
* **P(we notice a man on earth) > P(we a earth man on notice)**
**Credit: Zhisheng Tang**  
**Bengio Y et al. 2000**

# But How do we get these probabilites?
The answer is: there's more than one way! But let's start with one simple, intuitive way that works resonably well in simple cases: **counting** AKA maximum likelihood estimation (MLE).

Let's start by assuming that the next token is only dependent on the previous token, i.e., $P(w_t|w_1^{t-1}) = P(w_t|w_{t-1})$. This is a valid language model. It's just that not that good. In fact in real language model like GPT we also cannot use all previous tokenes. It's capped,    for example million.