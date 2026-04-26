---
layout: distill
title: "Causal Inference Overview"
description: "Understanding SUTVA and ignorability, fundamental assumptions in causal inference, what they mean, and what happens when they are violated."
date: 2025-08-23
categories: [dso-603, statistics]
tags: [causal-basics]
project: dso-603
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Rubin Potential Outcomes Framework
  - name: SUTVA
    subsections:
      - name: "1. Consistency: One Version of the Treatment"
      - name: "2. No Interference"
      - name: "What Happens When SUTVA is Violated?"
      - name: "How to Handle SUTVA Violations (Interference)"
  - name: "Ignorability: When Does Linear Regression Yield Causal Inference?"
    subsections:
      - name: "RCT is the gold standard"
      - name: "Observational studies"
      - name: "Ignorability"
      - name: "Overlap"
      - name: "Well specified linear model"
  - name: References
---

- Phase 1: Estimating treatment effects and uncertainty quantification.
- Phase 2: Policy learning for treatment assignment. Based on treatment effect estimation.
