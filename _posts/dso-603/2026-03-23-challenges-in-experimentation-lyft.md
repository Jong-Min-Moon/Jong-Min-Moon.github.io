---
layout: distill
title: "Summary: Challenges in Experimentation (Lyft)"
description: "A summary of the Lyft Engineering blog post 'Challenges in Experimentation' by John Kirn."
date: 2026-03-23
categories: dso-603 statistics
tags: causal-inference ab-testing experimentation
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

This post is a summary of the Lyft Engineering blog article, ["Challenges in Experimentation" by John Kirn](https://eng.lyft.com/challenges-in-experimentation-8167f6071060), which details how Lyft scales and manages online experimentation and A/B testing across its complex network.

Lyft maintains a robust culture of experimentation, testing virtually every product change to build causal evidence for strategic decisions. However, operating a dynamic two-sided marketplace at scale presents four major challenges.

## 1. Measuring Network Effects

In traditional A/B testing, one user's treatment is independent of another's. In ride-sharing, **interference (or "crowd out")** occurs: if a treatment makes some users request rides faster, they may match with nearby drivers, leaving control users with fewer options. This violates the assumption of independence. 

**Lyft's Solutions:**
- **Time Split Testing:** Giving all users within a certain time and geographic boundary the same experience. This reduces interference but can lead to inconsistent user experiences if they use the app across different periods.
- **Region Split Testing:** Dividing treatments geographically and using **synthetic controls**. Lyft uses pre-test trends to generate counterfactual predictions of what would have happened if the treatment wasn't launched.
- **Variance Reduction Techniques:** Applying causal inference methodologies like **residualization** to time split tests to improve statistical power and speed, making tests more resilient to external shocks like storms or outages.

## 2. Managing Real-World Dynamism

Lyft operates in a real-world environment affected by rapidly changing variables such as weather, traffic, and macroeconomic labor trends. As a result, parameters optimized via A/B tests months ago may quickly lose their external validity.

**Lyft's Solutions:**
- **Adaptive Experimentation:** Investing in always-on platforms to continuously test and adjust.
- **Parameter Tuning:** Jointly optimizing multiple continuous parameters dynamically.
- **Reinforcement Learning:** Utilizing **contextual bandits** to test broad treatment sets and converge on the optimal variants faster than fixed A/B tests, ensuring better experiences sooner.

## 3. Supporting Diverse Lines of Business

As Lyft expands beyond classic ride-sharing into Transit, Bikes, and Scooters (TBS), the standard "rider vs. driver" random split is no longer sufficient.

**Lyft's Solutions:**
- Introducing new randomization units, including:
  - **Session splits:** Alternating treatments each time a user opens the app.
  - **Hardware splits:** Randomizing treatments at the physical hardware level (e.g., across individual eBikes).

## 4. Supporting a Culture of Experimentation

With thousands of experiments running annually across growing teams, maintaining science hygiene and preventing coordination issues is extremely difficult. Lyft identifies three main pitfalls and solutions:

- **Pitfall 1: Poor Hypothesis Creation & HARKing.** Experimenters may fail to define primary metrics, ignore guardrails, or hypothesize *after* results are known (HARKing). 
  - *Solution:* A **guided hypothesis workflow** that pre-registers and formally records the hypothesis, main metrics, and guardrails before launch.
- **Pitfall 2: The Multiple Comparisons Problem.** Examining too many metrics or dimensional cuts drastically increases Type I error (false positives).
  - *Solution:* Automatically applying the **Benjamini-Hochberg method** to adjust p-values and correct for Multiple Hypothesis Testing (MHT).
- **Pitfall 3: Unaligned Trade-offs.** Different teams might optimize conflicting metrics (e.g., Team A spends money to increase rides, while Team B sacrifices rides to increase revenue), leading to destructive "buy high, sell low" scenarios.
  - *Solution:* A specialized **Revenue Operations** team acts as a clearinghouse. Lyft also built advanced results and decision-tracking logs to quantify the thousands of decisions being made and build consensus on proper investment trade-offs across the company.
