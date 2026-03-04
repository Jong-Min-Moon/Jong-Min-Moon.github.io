---
layout: distill
title: "Potential Outcome Framework and Matching Estimators"
description: "An introduction to the Neyman-Rubin causal model and matching methods"
date: 2026-03-03
categories: causal_inference statistics
tags: causal-inference matching potential-outcomes
project: causal_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Potential Outcome Framework
  - name: Treatment Effects
  - name: Assumptions for Identifying Causal Effects
  - name: Matching Estimators
  - name: Conclusion
---

## Potential Outcome Framework
The Potential Outcome Framework, also known as the Neyman-Rubin Causal Model, is the foundation for defining causal effects. For any individual $i$, we define two potential outcomes:
- $Y_i^{(1)}$ (or $Y_i(1)$): The outcome if the individual receives the treatment.
- $Y_i^{(0)}$ (or $Y_i(0)$): The outcome if the individual receives the control.

The causal effect for an individual $i$ is simply the difference between these two potential outcomes:
$$\tau_i = Y_i^{(1)} - Y_i^{(0)}$$

However, the **fundamental problem of causal inference** is that we can only observe one of these potential outcomes for any given individual. If an individual receives the treatment ($T_i = 1$), we observe $Y_i = Y_i^{(1)}$, and $Y_i^{(0)}$ becomes a missing counterfactual. The observed outcome can be written as:
$$Y_i = T_i Y_i^{(1)} + (1 - T_i) Y_i^{(0)}$$

## Treatment Effects
Since individual causal effects cannot be directly observed, we focus on average causal effects at the population level:

**Average Treatment Effect (ATE)**: The expected causal effect for a randomly selected individual from the population.
$$\text{ATE} = \mathbb{E}[Y_i^{(1)} - Y_i^{(0)}]$$

**Average Treatment Effect on the Treated (ATT)**: The expected causal effect for the subpopulation that actually receives the treatment.
$$\text{ATT} = \mathbb{E}[Y_i^{(1)} - Y_i^{(0)} \mid T_i = 1]$$

## Assumptions for Identifying Causal Effects
To estimate these causal effects from observational data, where treatment assignment is not randomized, we must rely on two key assumptions:

1. **Ignorability (Unconfoundedness)**: Conditional on observed covariates $X$, the potential outcomes are independent of treatment assignment.
$$Y^{(0)}, Y^{(1)} \perp T \mid X$$
This assumes we have measured all relevant confounders that affect both the treatment assignment and the outcome.

2. **Overlap (Positivity)**: For any set of covariate values, individuals have a non-zero probability of receiving either the treatment or the control.
$$0 < P(T=1 \mid X=x) < 1 \quad \forall x$$

## Matching Estimators
When ignorability and overlap hold, we can use **Matching estimators** to estimate causal effects. The intuition behind matching is to simulate a randomized experiment by finding individuals in the control group who are "similar" to individuals in the treatment group based on their observed covariates $X$.

For every treated unit $i$, matching finds one or more control units with similar covariate values $X_j \approx X_i$ to proxy the missing counterfactual $Y_i^{(0)}$. 

Types of matching include:
- **Exact Matching**: Matches individuals with identical covariate values. This suffers from the curse of dimensionality because finding exact matches becomes nearly impossible with many covariates.
- **Distance Matching**: Uses distance metrics (like Mahalanobis distance) to find the nearest neighbors in the covariate space.
- **Propensity Score Matching (PSM)**: Instead of matching directly on covariates $X$, PSM matches individuals on the probability of receiving treatment given their covariates, known as the propensity score $e(X) = P(T=1 \mid X)$. This reduces the matching problem to a single dimension.

Matching algorithms might use 1-to-1 matching (e.g., nearest neighbor) or 1-to-many matching. They can also match with or without replacement. Once matched, the average differences in outcomes between the matched treated and control units provide an estimate for the ATT or ATE.

## Conclusion
Matching provides an intuitive and non-parametric way to address confounding in observational studies by mimicking an RCT setup. It fundamentally relies on the critical assumption of unconfoundedness—that all relevant confounders are observed.
