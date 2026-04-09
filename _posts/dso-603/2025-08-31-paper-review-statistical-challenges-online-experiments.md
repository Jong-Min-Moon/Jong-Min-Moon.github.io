---
layout: distill
title: "Paper review: Statistical Challenges in Online Controlled Experiments"
description: "A review of Larsen et al. (2024) on the statistical landscape and challenges of A/B testing in large-scale online environments."
date: 2025-08-31
categories: dso-603 experiment-design statistics
tags: a-b-testing online-experiments sutva sequential-testing
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Introduction
  - name: Key Statistical Challenges
    subsections:
      - name: Experimental Power
      - name: Heterogeneous and Long-term Effects
      - name: Sequential Testing
      - name: Violations of SUTVA
  - name: Organization and Culture
bib_file: dso-603
paper_key: larsenStatisticalChallengesOnline2024
---

# Introduction

Online Controlled Experiments (OCEs), commonly known as A/B testing, have become the gold standard for data-driven decision-making in the technology industry. Major firms like Google, Amazon, and Microsoft conduct thousands of experiments annually to evaluate new features, algorithms, and designs. However, as experimentation scales, several statistical challenges emerge that go beyond textbook randomized controlled trials.

In this paper, **Larsen et al. (2024)** provide a comprehensive review of these challenges, bridging the gap between academic statistical theory and industrial practice.

# Sensitivity and Small Treatment Effects



## Experimental Power

Despite having millions of users, online experiments often suffer from low statistical power when trying to detect small but business-critical improvements (e.g., a 0.1% change in revenue). The authors discuss variance reduction techniques, such as **CUPED** (Controlled-experiment Using Pre-Experiment Data), which uses pre-experiment information to reduce the variance of the treatment effect estimator without introducing bias.

## Heterogeneous and Long-term Effects

### Heterogeneous Treatment Effects (HTE)
Understanding *who* benefits from a feature is as important as knowing *if* it works on average. The paper reviews methods for HTE estimation, including causal forests and other machine learning approaches that help identify subgroups where the treatment effect deviates significantly from the mean.

### Long-term Effects
While business objectives are often long-term (e.g., user retention), experiments are typically short-term. The authors highlight the use of **surrogate metrics**—short-term behaviors that are predictive of long-term outcomes—and the challenges in validating them.

## Sequential Testing

In a fast-paced environment, practitioners often want to "peek" at results before the experiment ends. Traditional frequentist p-values are invalid under continuous monitoring, leading to inflated Type I error rates. The paper discusses:
- **Sequential Probability Ratio Tests (SPRT)**
- **Bayesian methods** that allow for more flexible stopping rules.
- **Always-valid p-values** that remain robust to early stopping.

## Violations of SUTVA

The Stable Unit Treatment Value Assumption (SUTVA) assumes that one user's assignment does not affect another's outcome. In network-heavy platforms (social media) or marketplaces (Uber, Airbnb), this assumption is frequently violated through:
- **Network interference**: A new feature for one user affects their friends.
- **Marketplace interference**: A discount for one buyer affects the supply available to another.

The authors review **cluster-randomized designs** and **switchback experiments** as primary tools to mitigate these interference effects.

# Organization and Culture

Statistical rigor is only one part of a successful experimentation program. The authors emphasize the "Culture of Experimentation," which includes:
- **Data Quality**: Using **A/A tests** to ensure the system is unbiased and **Sample Ratio Mismatch (SRM) tests** to detect bugs in randomization.
- **Trust**: Ensuring that the results are interpretable and that the organization respects the data over intuition.

This review serves as a call to action for academic statisticians to engage with the unique, high-dimensional, and dynamic problems found in online experimentation environments.
