---
layout: distill
title: "When Does Linear Regression Yield Causal Inference?"
description: "Unconfoundedness and Overlap"
date: 2025-08-25
categories: causal_inference statistics
tags: causal-inference linear-regression
project: causal_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
bibliography: 2025-08-25-when-does-linear-regression-yield-causal-inference.bib
toc:
  - name: RCT is the gold standard
  - name: Observational studies
  - name: Ignorability
  - name: Overlap
---

## RCT is the gold standard
The simplest solution to the fundamental problem of causal inference is to run a Randomized Controlled Trial (RCT). In an RCT, the treatment and control groups are **balanced** on average, meaning they are **drawn from the same underlying distribution**. In other words, the sample means $\bar{y}_0$ and $\bar{y}_1$ estimate the average outcomes under control and treatment for the **exact same population**. ATE estimation is simple: just take the difference in means: $$\text{ATE} = \bar{y}_1 - \bar{y}_0$$

## Observational studies
In reality, RCTs are often prohibitively expensive, meaning we frequently must rely on observational data. Unlike in an RCT, treatments in observational studies are not randomly assigned; they are simply observed. As a result, systematic differences usually exist between the treated and untreated groups—a problem known as confounding.

However, if certain assumptions are met, we can still estimate the Average Treatment Effect (ATE) from observational data. Doing so simply requires more sophisticated estimators, moving beyond a naive difference in means to methods like linear regression.


## Ignorability
The key assumption is ignorability (also known as unconfoundedness). Intuitively, this means that instead of having a single randomized trial for the entire population, we essentially have a "mini-RCT" for every specific value of our observed covariates. Mathematically, this is expressed as conditional independence :
$$Y^{(0)},Y^{(1)} \perp T \mid X$$
This is a strong assumption! It requires that we haven't missed any pre-treatment covariates (unobserved confounders) that affect both the treatment assignment and the outcome. However, if this assumption holds—alongside the positivity assumption—we can estimate the Average Treatment Effect (ATE) from observational data using linear regression.

## Overlap
While ignorability concerns the dependence structure of the data, our second requirement restricts the assignment probabilities. This assumption—known as positivity or overlap—requires that for every possible value of our covariates, we observe subjects in both the treatment and control groups. Mathematically, the probability of receiving treatment given the covariates must be strictly between zero and one:
$$0 < P(T=1 \mid X=x) < 1$$
for all $x$ in the support of $X$.
