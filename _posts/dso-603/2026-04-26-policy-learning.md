---
layout: distill
title: "Policy Learning"
description: "Empirical Welfare Maximization, Policy Evaluation, and Regret Bounds"
date: 2026-04-26
categories: dso-603 statistics
tags: policy-learning causal-inference optimal-treatment
project: causal_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
bibliography: 2026-04-26-policy-learning.bib
toc:
  - name: Introduction
  - name: Statistical setting
  - name: Policy evaluation
  - name: Policy learning
  - name: Regret and convergence
  - name: Practical considerations
---

- The problem of learning optimal treatment assignment policies is closely related to—but subtly different from—the problem of estimating treatment heterogeneity

# Unconfoundedness
- In causal inference, we want to compare apple to apple.
- Unconfoundedness requires that the covariates are sufficiently informative such that assignment is as if at random once we condition on covariates
- Mathematically, $P(W|X)=P(W|X,Y)$

## Introduction
So far, we have focused on **estimation**: what is the average treatment effect (ATE)? What is the conditional average treatment effect (CATE)? While these are fundamental questions, in many real-world scenarios, the ultimate goal is **action**. We want to know: *who* should we treat to maximize the overall welfare?

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="_posts/dso-603/policy_learning_concept.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Policy learning shifts the focus from estimating parameters to finding an optimal decision rule. Instead of asking "how much does this drug help on average?", we ask "which patients should receive this drug to maximize health outcomes?"

## Statistical setting
We consider the standard potential outcomes framework. For each individual $i$, we observe:
- $X_i \in \mathcal{X}$: A vector of pre-treatment covariates.
- $W_i \in \{0, 1\}$: The treatment assignment.
- $Y_i \in \mathbb{R}$: The observed outcome, where $Y_i = Y_i(W_i)$ under SUTVA.

A **policy** $\pi$ is a mapping from the covariate space to the treatment space:
<p>
$$
\pi: \mathcal{X} \to \{0, 1\}.
$$
</p>
The goal is to find a policy $\pi$ that maximizes the **Value Function** $V(\pi)$, which is the expected outcome if everyone in the population followed policy $\pi$:
<p>
$$
V(\pi) = \mathbb{E}[Y_i(\pi(X_i))].
$$
</p>

## Policy evaluation
Before we can learn an optimal policy, we must be able to evaluate the value of a *given* policy $\pi$. Since we only observe one potential outcome for each individual, we rely on causal inference techniques to estimate $V(\pi)$.

### IPW Evaluator
Using the propensity score $e(x) = \mathbb{P}[W_i = 1 \mid X_i = x]$, we can define the IPW estimator for the value of policy $\pi$:
<p>
$$
\hat{V}_{IPW}(\pi) = \frac{1}{n} \sum_{i=1}^n \left( \frac{\mathbb{1}(\pi(X_i) = W_i) Y_i}{\mathbb{P}[W_i = \pi(X_i) \mid X_i]} \right).
$$
</p>
This is an unbiased estimator of $V(\pi)$ if the propensity score is known and overlap holds.

### AIPW Evaluator
Similar to ATE estimation, we can use Augmented IPW to improve efficiency and gain double robustness. Let $\hat{\mu}_{(w)}(x)$ be an estimate of the outcome model $\mathbb{E}[Y_i(w) \mid X_i = x]$. The AIPW value estimator is:
<p>
$$
\hat{V}_{AIPW}(\pi) = \frac{1}{n} \sum_{i=1}^n \left( \hat{\mu}_{(\pi(X_i))}(X_i) + \frac{\mathbb{1}(W_i = \pi(X_i)) (Y_i - \hat{\mu}_{(\pi(X_i))}(X_i))}{\mathbb{P}[W_i = \pi(X_i) \mid X_i]} \right).
$$
</p>

## Policy learning
Policy learning (or Empirical Welfare Maximization) aims to find a policy $\hat{\pi}$ within a pre-specified class $\Pi$ (e.g., shallow decision trees or linear rules) that maximizes the estimated value:
<p>
$$
\hat{\pi} = \arg\max_{\pi \in \Pi} \hat{V}(\pi).
$$
</p>
This can be rewritten as a weighted classification problem. Notice that maximizing $V(\pi)$ is equivalent to maximizing the gain over a baseline policy (say, treating no one, $\pi(x)=0$):
<p>
$$
V(\pi) - V(\pi_{0}) = \mathbb{E}[(\pi(X_i) - 0) \cdot (Y_i(1) - Y_i(0))] = \mathbb{E}[\pi(X_i) \cdot \tau(X_i)],
$$
</p>
where $\tau(x)$ is the CATE. In practice, we use scores $\hat{\Gamma}_i$ (like the AIPW scores for treatment effect) and solve:
<p>
$$
\hat{\pi} = \arg\max_{\pi \in \Pi} \frac{1}{n} \sum_{i=1}^n (2\pi(X_i) - 1) \hat{\Gamma}_i.
$$
</p>

## Regret and convergence
How well does our learned policy $\hat{\pi}$ perform compared to the best possible policy $\pi^*$ in the class $\Pi$? We measure this using **Regret**:
<p>
$$
R(\hat{\pi}) = V(\pi^*) - V(\hat{\pi}).
$$
</p>
A key result in policy learning <d-cite key="kitagawa2018who"></d-cite> is that for many policy classes with finite VC dimension $d$ (like decision trees), the regret decays at a rate of:
<p>
$$
R(\hat{\pi}) = O_P\left(\sqrt{\frac{d}{n}}\right).
$$
</p>
This means that even if we use complex machine learning models to estimate the nuisance parameters (propensity scores and outcome models), the performance of the learned policy depends primarily on the complexity of the *policy class* $\Pi$, not the complexity of the estimation models.

## Practical considerations
1. **Search Space**: The choice of $\Pi$ is a trade-off between flexibility and interpretability. Small decision trees are popular because they are easy for humans to follow.
2. **Optimization**: For complex policy classes, the optimization problem $\arg\max \hat{V}(\pi)$ can be computationally hard. Many implementations use surrogate losses or heuristic search.
3. **Software**: The `grf` package in R provides a powerful implementation of policy learning using causal forests to estimate the scores $\hat{\Gamma}_i$ <d-cite key="athey2021policy"></d-cite>.

By focusing on policy learning, we bridge the gap between statistical inference and decision-making, ensuring that our causal insights lead to optimal real-world actions.
