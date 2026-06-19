---
layout: distill
title: "Paper review: A Distributional Approach for Causal Inference Using Propensity Scores"
description: "A review of Tan (2006) on estimating average causal effects and improving upon propensity score methods using a distributional approach."
date: 2026-06-18
categories: dso-603 causal-inference statistics
tags: propensity-score causal-inference doubly-robust
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: "The Problem: The Unconfoundedness Assumption"
  - name: "The Solution: Sensitivity Analysis via Linear Programming"
bib_file: dso-603
paper_key: tan_distributional_2006
---
### **The Problem: The Unconfoundedness Assumption**

* **Standard ATE Estimation:** Estimating causal effects relies on the "unconfoundedness" assumption—meaning the treatment $T$ is assigned independently of the potential outcomes $(Y_0, Y_1)$ given observed covariates $X$. 
* Under this assumption, we can use methods like **Outcome Regression** (estimating the outcome based on $X$ and $T$, then averaging over $X$) or **Inverse Probability Weighting (IPW)** (weighting the observed data using the propensity score $\pi(X)$ to balance the covariates). These two methods are just change of orders.
* **The Violation:** If there is unmeasured confounding, the true probability of an outcome given a treatment, $P(Y_t \mid X)$, cannot be perfectly identified from the observed data $P(Y_t \mid T=t, X)$ because we cannot observe counterfactuals.

---

### **The Solution: Sensitivity Analysis via Linear Programming**

* **Measuring Confounding:** The paper models unmeasured confounding using a density ratio (Radon-Nikodym derivative), denoted as $\lambda_0$ and $\lambda_1$. By Bayes' rule, this acts as an odds ratio. It represents how much the odds of receiving treatment differ between two subjects who have the exact same observed covariates $X$, but different unobserved traits.
* **Bounding the Odds:** The method bounds this deviation by a sensitivity parameter, $\Gamma$. The model restricts the unmeasured confounding to the range $\Gamma^{-1} \leq \lambda_t \leq \Gamma$. When $\Gamma = 1$, there is no unmeasured confounding.
* **Modified Weighting:** Because the unconfoundedness assumption is broken, the standard IPW weights are no longer fixed by $X$. Instead, the weights vary across sample index $i$ by the unknown factor $\lambda_{ti}$.
* **Enforcing Constraints:** The method preserves a critical property of IPW: the weighted marginal distribution of the covariates $X$ in the treatment/control groups must still equal the overall marginal probability of $X$ in the full sample. Mathematically, this means enforcing constraints like $\int \lambda_t d\hat{G}_t = 1$.
* **Worst-Case Computation:** Using these constraints and the $\Gamma$ bounds on the decision variables ($\lambda_t$), the paper uses **Linear Programming (LP)** to compute the strict lower and upper bounds for the expected outcomes $E(Y_0)$ and $E(Y_1)$. If the estimated treatment effect remains significant even at a high $\Gamma$, the study's conclusions are highly robust to hidden biases.