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

"bigram model"
Let's start by assuming that the next token is only dependent on the previous token, i.e., $P(w_t|w_1^{t-1}) = P(w_t|w_{t-1})$. This is a valid language model. It's just that not that good. In fact in real language model like GPT we also cannot use all previous tokenes. It's capped,    for example million.

then the language model becomes:
$$
    \hat{P}(w_1^T) = \prod_{t=1}^{T} \hat{P}(w_t|w_{t-1})
$$


### How to count
I want to compute $P(Cat|The)$ by counting. 

the key point is we only care about the conditionals, not marginals. 

Do not count the marginals.
count "the _" not "the". count "the" followed b y something, not count "the" only. In these examples it's easy because all the are followed by other word. but if there's a setnence "I went to the" then we don't count "the" in this sentence. if we have trigram model, than we should count "the _ _".

18 "the_"

THen count "the cat"
C(the _) = 18
C(the cat) = 3

then $P(Cat|The) = \frac{C(the cat)}{C(the_)} = \frac{3}{18} = \frac{1}{6}$

some probabilities can be 0.

2. introduce dummy \<S\> token at the start of the sentence. the reason is only to estiamte conditional probabilities. n-gram model requires n-1 start tokens

# What if we have web-scale data?
what would happen to our bigram and trigarm model> does the amount of data mattrer? to what extent?

how might you try to improve your probability estimates?

More importantly, how do you know your probability estiamtes are good> what's the true metric of sucess?



Another example.
..
...
...

1. using a biagram model, what is the probability of 'walked' after 'when it got ark the cat'?
   because of the bigram mdoel. actually we only need to estimate P(walked|cat).
2. what if we don;t make that assumption? we go back to the defintion of language model:
P(walked|when it got dark the cat)=P(when|<S>) * p(it|<S> when) P (got|<S> when it)...
= 0 because one of the probabilty is 0.
So as the model gets complicated, there;s more cahnge that setnences have zero probabilities, if not enough data. bigger model requires more data



trigram model
p(the cat jumped over)
=
p(the|s s) * p(cat|s the) * p(jumped|the cat) * p(over| cat jumped)

p(jumped | the cat) = C(the cat jumped) / C(the cat _). always the last is blank




when computing perplexity, assume the start token exists at the beginning


what the formula tells us: perpexity is bouned by 1. small is better