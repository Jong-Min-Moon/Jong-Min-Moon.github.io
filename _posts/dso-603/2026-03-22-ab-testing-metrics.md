---
layout: distill
title: "A/B Testing Metrics"
description: "A comprehensive guide to selecting and evaluating metrics in A/B testing and online experimentation."
date: 2026-03-22
categories: dso-603 statistics
tags: experimentation
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

A/B testing (or online experimentation) is the gold standard for causal inference in tech and business. A key challenge in A/B testing is deciding **what** to measure. The choice of metrics determines whether we can accurately assess the causal impact of a new feature or change.

# Types of Metrics

When designing an experiment, metrics generally fall into different roles:

## 1. Primary Metric
- The primary metric encodes the main goal of the experiment.
- simple enough to be understood by stakeholders
- stable over time
- They are mostly conditional probabilities.
- **Example:** Click-through rate (CTR), conversion rate, or average revenue per user (ARPU).

### Example: Click-Through Rate (CTR)
- Ratio of users who click on a specific link or button to the total number of users who view the page.
- **Formula:** CTR = (Number of Clicks / Number of Impressions) * 100
- **Ad Example:** 5 clicks and 100 impressions = 5% CTR.
- **Email Example:** 4 clicks per 100 people who saw it (not *opened*; so spam filtered does not count, but deleting without opening counts) = 4% CTR.
- **Industry Benchmarks:**
    - **Display Ads:** 0.5%–2% (varies widely by industry)
    - **Search Ads:** 2%–5% (often higher for branded terms)
    - **Email Marketing:** 2%–5% (varies by industry and list quality)

## 2. Secondary  Metrics
- aka Diagnostic, driver, surrogate, indirect, predictive metrics
- These help explain the *why* behind the primary metric's movement: **If the primary metric goes up, secondary metrics reveal the mechanism** (e.g., users are finding the button faster).
- align with the primary metric and more sensitive to the product change
- **Example:** Time to first click, scroll depth, or number of searches per session.

## 3. Guardrail  Metrics
- aka safety metric
- Metrics that act as a safety net. You do not necessarily want to improve them, but you want to ensure they do not degrade.
- **Example:** Page load time, crash rate, unsubscribe rate, or customer support ticket volume.

### trustworthy-related metrics
-  monitors trustworthiness of the experiemnt
- checks violation of assumptions
- example: randomization units assinged to variant: if the numbers are significanlty different accross treatments (sample ratio mismatch) measured by t-test or chi-square test
# Characteristics of a Good Metric

A metric in an A/B test is only useful if it reliably distinguishes robust changes from noise. It should be:
 1. simple and claer. shoud be explained in one sentence.
 2. actionable: must lead to a decision. for example, if the metric is short-term revenue, it is easy to make it significant (increase the price). but in long term lose custemer and lost long term goal. so it is not actionable.
1. **Sensitive (Statistical Power):** The metric must be sensitive enough to detect meaningful changes caused by the treatment. If the metric is too noisy (high variance), it will be difficult to achieve statistical significance.
2. **Robust:** The metric should not be overly sensitive to outliers or unrelated systemic variations.
3. **Actionable & Understandable:** Stakeholders must easily understand what the metric measures so they can make informed decisions when the experiment concludes.
4. **Timely:** The metric must manifest quickly enough to be measured within the duration of the experiment. For example, "Customer lifetime value over 5 years" is a poor A/B test metric because it takes 5 years to measure; a good proxy metric would be "User retention after 7 days".

# Statistical Properties

When analyzing metrics, we typically rely on normal approximation via the Central Limit Theorem. Important statistical concepts include:

- **Variance:** Metrics with high variance (like revenue per user, where a single large spender can skew results) are much harder to move with statistical significance. Often, techniques like **CUPED** (Controlled-experiment Using Pre-Experiment Data) are used to reduce variance for these metrics.
- **Minimum Detectable Effect (MDE):** The smallest effect size we care about detecting. Metrics with lower baseline variance have a smaller MDE for a given sample size.
- **Unit of Randomization vs. Unit of Analysis:** The metric is often calculated at the unit of analysis (e.g., click or pageview). However, if the unit of randomization is higher (e.g., the user account), we must account for the correlation of events from the same user when calculating standard errors (e.g., using the delta method or cluster-robust standard errors).

# References
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing.* Cambridge University Press.
- A/B Testing Metrics: What You Need to Know About Success, Driver, and Guardrail Metrics! (https://www.youtube.com/watch?v=SuXc5ckvlJ8)