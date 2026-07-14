---
layout: distill
title: "Paper review: Data Fusion for High-Resolution Estimation"
description: "A review of Guan et al. (2026) on fusing unbiased administrative data with biased survey data for high-resolution estimation."
date: 2026-07-09
categories: dso-603 causal-inference statistics
tags: data-fusion high-resolution-estimation sampling-bias
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: "The Problem: High-Resolution Estimation and Data Biases"
  - name: "The Solution: Data Fusion via KL Divergence"
bib_file: dso-603
paper_key: guan_data_2026
---

# The Problem: High-Resolution Estimation and Data Biases

- Creating high-resolution estimates of population health indicators is essential for precision public health.
- However, researchers are often faced with a trade-off between two distinct types of data:
  - **Administrative data**: Unbiased but typically only available at a low resolution (e.g., state or national level).
  - **Online surveys**: Available at a high resolution (e.g., county or zip code level), but potentially subject to significant sampling bias.
- The high-resolution data often suffers from selection bias where the probability of response is influenced by unit observables. 

---

# The Solution: Data Fusion via KL Divergence

- To address this challenge, the authors propose a method to "fuse" these two data sources.
- The core idea is to learn a distribution that minimizes the Kullback-Leibler (KL) divergence to the survey distribution.
- This learned distribution must satisfy two constraints:
  1. It must remain consistent with the unbiased administrative data.
  2. It must align with the assumed sampling bias model of the survey data.
- By combining the strengths of both data sources, this approach significantly reduces bias in high-resolution estimates compared to using either data source independently.
- The authors also evaluate their proposed method on a testbed, comparing it against ground-truth data sources at different geographic resolutions to demonstrate its effectiveness.
