---
layout: distill
title: "Paper review: Catastrophe Insurance: An Adaptive Robust Optimization Approach"
description: "A review of Bertsimas and Zeng (2024) on applying adaptive robust optimization to catastrophe insurance pricing."
date: 2026-07-08
categories: csci-699
tags: optimization insurance robust-optimization
project: csci-699-optimization
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
toc:
  - name: "Summary"
  - name: "The Problem"
  - name: "The Proposed Method: Adaptive Robust Optimization"
bib_file: csci-699-optimization
paper_key: bertsimas_catastrophe_2024
---

* This paper uses a simple linear programming formulation to compute catastrophic insurance premiums.
* Since the problem parameters—specifically, future losses—are uncertain, the authors employ robust optimization with uncertainty sets.
* **Punchline 1:** The uncertainty set is the union of two distinct sets: one derived from normal approximations, and the other from machine learning prediction uncertainties.
* Consequently, the robust optimization problem transforms into a min-max optimization problem, for which the paper derives an equivalent explicit formulation.
* Finally, the paper introduces a mechanism to incorporate historical data, giving the approach a data-fusion flavor. The resulting problem is then solved via adaptive robust optimization.

# LP Formulation
The formulation requires a demand function $f$.

$$
\min_{p_{i,t}} \sum_{i=1}^N \sum_{t=1}^T f(p_{i,t}) p_{i,t}
$$

**Subject to:**

<p>
$$
|p_{i,t} - p_{i,t-1}| \leq \gamma_1, \quad \forall i \in [N], t \in [T]
$$

$$
\sum_{t=1}^T f(p_{i,t}) p_{i,t} - \sum_{t=1}^T f(p_{i,t}) l_{i,t} \geq \delta, \quad \forall i \in [N]
$$

$$
p_{i,t} \in \mathbb{R}_+, \quad \forall i \in [N], t \in [T]
$$
</p>

- Interpretation: collect minimum premium to cover the loss and other expenses ($\delta$)
# Sources of Uncertainty

* The rarity of catastrophic events leads to a lack of comprehensive historical data.
* Climate change renders the historical data we *do* have increasingly unreliable.
* Thus, historical data must be supplemented with predictions from machine learning or physics-based models. However, these models are probabilistic and inherently subject to misspecification.

# Uncertainty Set 1: Normal Approximation
* This approach builds on Bertsimas's prior work. 
* Assuming losses follow a normal distribution, future losses are modeled as values whose sum deviates from the historical mean by a specific number of historical standard deviations.
* Broadly speaking, leveraging the mean and variance aligns perfectly with standard actuarial principles. Much like standard pricing and risk practices at commercial carriers like Cincinnati Insurance, companies routinely utilize the mean (Average Annual Loss, AAL) and variance (or uncertainty, often embedded in permissible loss ratios) for capital allocation or post-catastrophe model adjustments to premiums.

# Uncertainty Set 2: Machine Learning Prediction
* **Assumption 1:** A specific catastrophe rarely occurs more than once within a reasonable multi-year timeframe.
* **Assumption 2:** A peril is considered catastrophic only when the resulting loss exceeds a threshold $\Theta$.
* The ML model outputs the probabilities of exceeding this threshold. Allowing for an $\epsilon$-margin of error, an uncertainty set of binary indicators is created where the sum of the indicators approximates the sum of these probabilities. The aforementioned assumptions are then used to link these indicator values directly to the projected loss values.
 