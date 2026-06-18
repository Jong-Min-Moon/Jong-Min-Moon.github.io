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
  - name: Introduction
  - name: Key Methodological Contributions
    subsections:
      - name: Augmented Inverse Probability Weighting (AIPCW)
      - name: Sensitivity Analysis Framework
      - name: Handling High-Dimensional Data
  - name: Applications and Impact
bib_file: dso-603
paper_key: scharfsteinAdjustingNonignorableDropOut1999
---

The Problem: The article addresses the statistical challenge of making inferences about the mean of an outcome variable that is only observed for subjects who do not drop out of a study.The Model: To account for this missing data, the authors propose a stratified Cox proportional hazards model where the risk of dropping out depends on both the observed history of covariate variables and the potentially unobserved final outcome.The Bias Parameter: The degree to which the drop-out hazard depends on this unobserved outcome is governed by an unknown selection bias parameter, denoted as $a_0$.The Identifiability Issue: Because neither this bias parameter nor the true joint distribution of the full data can be uniquely identified from the observed data alone, the model cannot be evaluated using standard estimation methods without further assumptions.The Solution: To overcome this limitation, the authors propose a sensitivity analysis approach where $a_0$ is treated as a known variable, allowing researchers to estimate the outcome's mean and compute valid confidence intervals across a range of plausible bias parameters.