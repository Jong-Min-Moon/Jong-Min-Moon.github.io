---
layout: distill
title: "Paper review: Performance Guarantees for Individualized Treatment Rules"
description: "A review of Qian and Murphy (2011) on formulating individualized treatment rules via conditional outcome maximization with performance guarantees."
date: 2026-04-26
categories: [dso-603, statistics]
tags: [policy-learning, paper-review]
project: dso-603
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: "The Setup"
  - name: "The Old Way: Value Maximization"
  - name: "The Solution: Conditional Outcomes"
  - name: "The Guarantee: Theorem 3.1"
  - name: "The Catch and The Remedy"
bib_file: dso-603
paper_key: qianPerformanceGuaranteesIndividualized2011
---

## Personalizing Medicine: Guaranteeing the Performance of Treatment Rules

In clinical practice, "Many illnesses show heterogeneous response to treatment" (p. 15). Because a drug might cure one patient while causing adverse events in another, there is a massive push to individualize care (pp. 16, 17). The goal is simple: "recommend the treatment achieving the best predicted prognosis for that patient" (p. 22) in order to "optimize the mean response" (p. 23).

## The Setup

To build these rules, Qian and Murphy utilize data from a "single stage randomized trial" (p. 30). We start with pretreatment variables representing patient characteristics ($X$), a finite treatment space ($A$), an outcome ($R$), and a "known randomization distribution of A given X by $p(\cdot|X)$" (pp. 60, 63). The objective is to formulate an individualized treatment rule (ITR), defined as a "deterministic decision rule from $\mathcal{X}$ into the treatment space $\mathcal{A}$" (p. 61).

## The Old Way: Value Maximization

Historically, researchers relied on Value maximization when dealing with a simple class of rules (p. 79). They constructed estimators based on the mathematical value of a policy: 

<p>
$$
V(d)=E\left[\frac{1_{A=d(X)}}{p(A|X)}R\right]
$$
<\p>

While effective for simple models, "if the best rule within a larger class of ITRs is of interest, these approaches are no longer feasible" (p. 80) due to the computational limits of handling high-dimensional data (p. 32). (Note: the formula for $V(d)$ is shown on p. 75).

## The Solution: Conditional Outcomes

Instead of direct value maximization, the authors propose a conditional outcome approach. They prove that "an optimal ITR satisfies $d_0(X) \in \arg\max_{a\in\mathcal{A}} Q_0(X,a)$ a.s." (p. 86). By characterizing the optimal policy as the population conditional outcome maximizer, the rule simply becomes: predict the outcome for each treatment, and pick the highest one (pp. 83, 86).

## The Guarantee: Theorem 3.1

Why does this work? Theorem 3.1 proves that the "estimated ITR will be of high quality (i.e., have high Value) if we can estimate $Q_0$ accurately" (p. 88). It mathematically bounds the policy value error by the conditional outcome error, scaled by a margin condition (pp. 96, 102). This margin essentially "measures the difference in mean responses between the optimal treatment(s) and the best suboptimal treatment(s) at $x$" (p. 128). 

## The Catch and The Remedy

There is one major trap. If your approximation space doesn't contain the true model, "minimizing the prediction error may not result in the ITR... that maximizes the Value" (p. 152). This occurs "when the approximation space $\mathcal{Q}$ does not provide a treatment effect term close to the treatment effect term in $Q_0$" (p. 153).

**The Remedy:** To "deal with the mismatch between minimizing the prediction error and maximizing the Value", the authors consider "a large linear approximation space" via basis expansion (p. 162). By applying $l_1$-penalized least squares, this regression-based method sifts through high-dimensional data, prevents overfitting, and guarantees a highly effective, personalized treatment rule (pp. 162, 163, 180).
