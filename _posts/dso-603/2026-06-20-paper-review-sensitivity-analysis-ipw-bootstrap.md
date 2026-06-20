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

### **The Problem: Untestable Assumptions**

* **The Core Issue:** In observational studies, methods like Inverse Probability Weighting (IPW) rely heavily on the assumption of "no unmeasured confounding" (also known as strict ignorability). We assume all variables affecting both treatment and outcome are observed and accounted for in the propensity score.
* **The Violation:** This assumption cannot be verified using empirical data. If unmeasured confounders exist, the standard IPW estimator will be biased, and the resulting confidence intervals will not provide the correct coverage for the true causal effect.

---

### **The Solution: Marginal Sensitivity Models and Percentile Bootstrap**

* **Marginal Sensitivity Model (MSM):** To address the uncertainty of unmeasured confounding, the authors employ a marginal sensitivity model. This model extends Rosenbaum's well-known sensitivity analysis framework (traditionally used for matched studies) to a broader set of applications including weighting estimators.
* **Bounding the Confounding:** The MSM bounds the odds ratio of the unknown true propensity score versus the estimated propensity score (based on observed covariates) by a sensitivity parameter $\Gamma$. If $\Gamma = 1$, there is no unmeasured confounding. As $\Gamma$ increases, we allow for more severe violations of the ignorability assumption.
* **Constructing Confidence Intervals:** The goal is to construct robust confidence intervals for the IPW estimators that maintain nominal coverage even when the data generating distribution falls anywhere within the bounds of the marginal sensitivity model. 
* **The Percentile Bootstrap and Minimax Inequality:** Evaluating the worst-case bounds over all possible unmeasured confounders is computationally daunting. The authors creatively combine a **percentile bootstrap** approach with a **generalized minimax/maximin inequality**. This mathematical trick transforms an intractable infinite-dimensional optimization problem into a tractable linear fractional programming problem.
* **Efficiency:** Because the problem is reduced to linear fractional programming, the bounds for the treatment effect under a given $\Gamma$ can be computed highly efficiently, allowing researchers to rapidly assess how sensitive their findings are to hidden biases.
