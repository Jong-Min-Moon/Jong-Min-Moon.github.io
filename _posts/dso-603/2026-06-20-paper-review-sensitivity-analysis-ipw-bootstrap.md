---
layout: distill
title: "Paper review: Sensitivity Analysis for Inverse Probability Weighting Estimators via the Percentile Bootstrap"
description: "A review of Zhao, Small, and Bhattacharya (2019) on conducting robust sensitivity analysis for IPW estimators using marginal sensitivity models and the percentile bootstrap."
date: 2026-06-20
categories: dso-603 causal-inference statistics
tags: sensitivity-analysis inverse-probability-weighting bootstrap
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: "The Problem: Untestable Assumptions"
  - name: "The Solution: Marginal Sensitivity Models and Percentile Bootstrap"
bib_file: dso-603
paper_key: zhao_sensitivity_2019
---

# The Setup: The Data Generating Process
- Missing data problem is a common problem in causal inference literature, and share similarity with ATE estimation from observational data.
- For each subject $i \in \{1, 2, \dots, n\}$, we define the following variables:
  - $A_i$: An indicator variable where $A_i = 1$ if the response is observed, and $A_i = 0$ if it is missing.
  - $X_i \in \mathcal{X} \subset \mathbb{R}^d$: A vector of fully observed covariates.
  - $Y_i \in \mathbb{R}$: The target response variable. 

- We assume that $(A_1, X_1, Y_1), \dots, (A_n, X_n, Y_n)$ are independent and identically distributed (IID) from a joint true data-generating distribution, $F_0$. 

- Crucially, $Y_i$ is only observed if $A_i = 1$. In reality, the data we actually get to see is $(A_i, X_i, A_i Y_i)$. 

- Our goal is to estimate the true mean response in the complete data: 
<p>$$\mu := \mathbb{E}_0[Y]$$</p>

---

### The "Missing at Random" (MAR) Assumption

- Let's define *missingness mechanism* as the probability that a data point is observed.  
<p>$$e_0(x, y) = \mathbb{P}_0(A = 1 \mid X = x, Y = y)$$</p>

- Previous IPW methods for estimating $\mu$ rely on the **Missing at Random (MAR)** assumption:
<p>$$e_0(x, y) = e_0(x)$$</p>

- MAR assumes that the probability of missingness depends *only* on the observed covariates, not the unobserved response. 

- However, MAR is a strong assumption, and in many real-world scenarios, it is easily violated. 

---

### Sensitivity Model

- Because $e_0(x, y)$ cannot be identified from the data without the MAR assumption, we need a way to test how our estimate of $\mu$ changes if MAR is violated. 
- To do this, we use a user-specified function for $e_0(x, y)$ known as a **sensitivity model**. It's called a model because it is a user-specified function.



#### Definition: The Marginal Sensitivity Model
Fix a parameter $\Lambda \ge 1$. We assume that our missingness mechanism $e(x, y)$ belongs to a set $\mathcal{E}(\Lambda)$, defined as:

<p>$$\mathcal{E}(\Lambda) = \left\{ e(x, y) \in [0, 1] : \frac{1}{\Lambda} \le \text{OR}(e(x, y), e_0(x)) \le \Lambda, \text{ for all } x \in \mathcal{X}, y \in \mathbb{R} \right\}$$</p>

Where $\text{OR}$ is the **odds ratio**, defined as:
<p>$$\text{OR}(p_1, p_2) = \frac{p_1 / (1 - p_1)}{p_2 / (1 - p_2)}$$</p>

By adjusting $\Lambda$, you control the "budget" of unmeasured confounding. If $\Lambda = 1$, you are strictly enforcing the MAR assumption. As $\Lambda$ grows, you allow for more severe violations of MAR.

---

### The Logistic Representation
It is often much easier to write this model using the **logistic (logit) scale**. 

Let's define the logit functions for our probabilities:
<p>$$g_0(x) = \text{logit}\{e_0(x)\} = \log \left( \frac{e_0(x)}{1 - e_0(x)} \right)$$</p>
<p>$$g_0(x, y) = \text{logit}\{e_0(x, y)\}$$</p>

<p>$$h_0(x, y) = g_0(x) - g_0(x, y)$$</p>

So $h$ quantifies the degree of shift.
We can now express our sensitivity model probability as a function of this shift, $h$:
<p>$$e^{(h)}(x, y) = \left[ 1 + \exp\{h(x, y) - g_0(x)\} \right]^{-1}$$</p>

> **Key Takeaway:** The marginal sensitivity model simply puts a bound on the $L_\infty$-norm of $h$. 

If we define $\lambda = \log(\Lambda)$, the sensitivity model translates to:
<p>$$\mathcal{H}(\lambda) = \left\{ h : \mathcal{X} \times \mathbb{R} \to \mathbb{R} \text{ and } \|h\|_\infty \le \lambda \right\}$$</p>
It is  easy to see the model's behavior: as $h(x, y) \to \pm\infty$, the selection probability $e^{(h)}(x, y)$ approaches $0$ or $1$. 
 