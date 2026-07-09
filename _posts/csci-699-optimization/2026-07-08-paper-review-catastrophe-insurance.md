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

# Summary

The escalating frequency and severity of natural disasters, exacerbated by climate change, underscore the critical role of insurance in facilitating recovery and promoting investments in risk reduction. This paper introduces a novel Adaptive Robust Optimization (ARO) framework tailored for the calculation of catastrophe insurance premiums, with a case study applied to the United States National Flood Insurance Program (NFIP). 

To the best of our knowledge, it is the first time an ARO approach has been applied to disaster insurance pricing. The methodology is designed to protect against both historical and emerging risks, the latter predicted by machine learning models, thus directly incorporating amplified risks induced by climate change. Using the US flood insurance data as a case study, optimization models demonstrate effectiveness in covering losses and produce surpluses, with a smooth balance transition through parameter fine-tuning. Among tested optimization models, results show ARO models with conservative parameter values achieving a low number of insolvent states with the least insurance premium charged.

Overall, optimization frameworks offer versatility and generalizability, making them adaptable to a variety of natural disaster scenarios, such as wildfires and droughts. This work not only advances the field of insurance premium modeling but also serves as a vital tool for policymakers and stakeholders in building resilience to the growing risks of natural catastrophes.

---

# The Problem
Traditional catastrophe insurance pricing struggles to adapt to the rapidly changing risk landscapes driven by climate change. As the frequency and severity of natural disasters like floods, wildfires, and droughts increase, static models often fail to capture emerging risks, leading to either under-pricing (which risks insolvency) or over-pricing (which reduces accessibility). A new approach is needed that can dynamically adapt to both historical data and machine learning predictions of future risks.

---

# The Proposed Method: Adaptive Robust Optimization

The authors propose an Adaptive Robust Optimization (ARO) framework to dynamically price catastrophe insurance premiums.

- **Robustness against Uncertainty:** By utilizing robust optimization, the model accounts for the worst-case scenarios within a defined uncertainty set, ensuring that premiums remain sufficient even when losses deviate from historical averages.
- **Adaptability:** The framework adapts over time by integrating machine learning models that predict emerging risks, allowing the insurance pricing to stay current with climate change impacts.
- **Application to the NFIP:** In a case study on the US National Flood Insurance Program (NFIP), the ARO approach demonstrated that it could effectively cover losses and generate surpluses. 
- **Parameter Tuning:** The balance between premium cost and insolvency risk can be smoothly transitioned through parameter fine-tuning. Conservative ARO models achieved the lowest number of insolvent states while charging the minimum necessary premiums.

> **Key Takeaway:** The ARO framework offers a versatile and mathematically rigorous tool for policymakers to build resilient insurance systems against the growing threat of natural catastrophes.
