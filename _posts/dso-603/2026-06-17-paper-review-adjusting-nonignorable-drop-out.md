---
layout: distill
title: "Paper review: Adjusting for Nonignorable Drop-Out Using Semiparametric Nonresponse Models"
description: "A review of Scharfstein, Rotnitzky, and Robins (1999) on handling nonignorable missing data and conducting sensitivity analysis using semiparametric methods."
date: 2026-06-17
categories: dso-603 missing-data statistics
tags: nonignorable-dropout sensitivity-analysis aipcw
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: The Problem
  - name: The Model
  - name: The Solution
  - name: "Example: ACTG 175 Study"
bib_file: dso-603
paper_key: scharfstein_adjusting_1999
---
# The Problem

**The Data Generating Process:** The observed data for a subject consists of:
$$O = (Q, \Delta, \Delta Y, \bar{V}(Q))$$

**Variable Definitions:** * $Q$: Time to drop-out. If a subject completes the study, $Q=T$.
* $\Delta = I(Q \ge T)$: The drop-out indicator.
* $Y$: The primary outcome of interest.
* $\bar{V}(Q)$: The covariate history, which is only observed up to the time of drop-out.

**The Goal:** Estimation and inference regarding the unconditional expectation (mean) of the outcome variable, denoted as $\mu_0 = \mathbb{E}[Y]$.

**The Challenge:** The drop-out indicator $\Delta$ is a function of $Q$. If $Q$ is strictly independent of $Y$, estimation is straightforward because the observed data represents a completely random subsample. However, in most clinical or real-world settings, drop-out is informative. For example, patients with severe disease progression may be more likely to drop out, while healthier patients remain. Because $\Delta$ often depends on the potentially unobserved outcome $Y$, analyzing only the observed cases will lead to biased estimation.

# The Model

To address the estimability of $\mu_0$, the authors assume a specific underlying structure and propose a stratified Cox proportional hazards model. 

**Model Mechanics:**
In this framework, the risk of dropping out depends on both the observed history of covariate variables ($\bar{V}$) and the potentially unobserved final outcome ($Y$).

**The Bias Parameter:**
The degree to which the drop-out hazard relies on the unobserved outcome is governed by an unknown selection bias parameter, denoted as $a_0$. 

**Theoretical Limitations (Theorem 1):**
Without parametric assumptions on the joint distribution of $Y$ and $\bar{V}$ or $Q$, the paper establishes two critical facts:
* Neither the bias parameter $a_0$ nor the true joint distribution of the full data can be uniquely identified from the observed data alone.
* If we know the marginal distribution of the observed data ($F_O$) and assume a specific value for the selection bias parameter ($a_0$), there always exists a configuration for the rest of the Cox model that perfectly aligns with $F_O$ and $a_0$.

**Implications of Theorem 1:**
Because the observed data distribution $F_O$ can be easily estimated, the data itself can never reject a hypothesized value of $a_0$. In short: $a_0$ cannot be estimated from the data alone. However, if a value for $a_0$ is fixed, the outcome mean $\mu_0$ becomes estimable.

# The Solution

To overcome the inherent non-identifiability of the model, the authors propose a structured sensitivity analysis. By treating the selection bias parameter $a_0$ as a known, fixed variable, researchers can estimate the outcome's mean and compute valid confidence intervals across a plausible range of bias parameters. This allows analysts to evaluate how robust their conclusions are to varying assumptions about the missing data mechanism.

# Example: ACTG 175 Study

**Context:** A clinical trial comparing four treatments for HIV.

**Outcome Variable:** CD4 count measured at the end of the study period.

**Initial Findings:** Based purely on the mean of the observed outcomes, Treatment 2 appears to be the most effective (as shown in Table 3 of the paper).

**Sensitivity Analysis Application:** The authors apply their methodology by systematically varying the values of $a_0$ for each treatment arm. By plotting the estimated treatment effects across this range, researchers can visualize the area of uncertainty and determine if Treatment 2 remains superior even under pessimistic assumptions about nonignorable drop-out.