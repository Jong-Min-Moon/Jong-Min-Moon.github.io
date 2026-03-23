---
layout: distill
title: "Causal Assumption: SUTVA"
description: "Understanding SUTVA, a fundamental assumption in causal inference, what it means, and what happens when it is violated."
date: 2026-03-23
categories: dso-603 statistics
tags: causal-inference ab-testing experimentation
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

Causal inference under Rubin potential outcomes framework, whether from a randomized A/B test or an observational study, relies heavily on the **Stable Unit Treatment Value Assumption (SUTVA)**. 
SUTVA consists of two distinct components:
  1.  **No Interference** 
  2.  **One Version of the Treatment**.



## 1. No Interference

**Definition:** The potential outcomes for any unit do not depend on the treatment assigned to other units.

<p align="center">
\begin{equation*}
    Y_1(W_1) = Y_1(W_1 | W_2=0) = Y_1(W_1 | W_2=1) = ... = Y_1(W_1 | W_2=w_2) = ... = Y_1(W_1 | W_n=w_n)
\end{equation*}
</p>

Simply put, what happens to *you* under a treatment or control condition is not affected by whether *someone else* is in the treatment or control group. 

### Examples Validating "No Interference"
- **Medical Trials (Non-Infectious):** If a patient takes a pill for a headache, it does not alleviate or worsen another patient's headache. The outcome for Patient A only depends on Patient A's treatment.
- **Standard E-commerce A/B Tests:** If User A sees a blue "Buy" button and User B sees a red one, User A's likelihood to purchase is largely independent of User B's experience.

### Examples of "Interference" (SUTVA Violation)
- **Vaccines:** In infectious diseases, if everyone around you is vaccinated (Treatment), your potential outcome of getting sick (Control) drops drastically due to herd immunity.
- **Social Networks:** If Facebook tests a feature that makes users post more, and your friends get the treatment, your feed will have more posts—even if you are in the control group. This is often called **network spillover**.
- **Two-Sided Marketplaces (Ride-sharing):** If a new feature makes treatment riders match with drivers much faster, it removes available drivers from the road, making control riders wait longer ("crowd-out effect"). 

---

## 2. One Version of the Treatment

**Definition:** For each unit, there are no different forms or versions of each treatment level that lead to different potential outcomes. 

If a unit receives "Treatment A", it must mean the exact same thing across all units.

### Examples of SUTVA Violations for "One Version"
- **Dosage Variations:** If the treatment is defined as "taking Aspirin," but some people take 100mg and others take 500mg, we don't have one version of the treatment. 
- **Surgical Procedures:** If the treatment is "receiving knee surgery," but one surgeon is world-class and another is inexperienced, the treatment varies wildly depending on who performs it.
- **Software Rollouts:** If a UI feature performs very fast on iOS but is buggy and slow on Android, treating "Feature X" as a single uniform treatment will blur the causal effect.

---

## What Happens When SUTVA is Violated?

When SUTVA is violated, our estimates of the **Average Treatment Effect (ATE)** become biased. 

If there is interference, the difference between the Treatment and Control groups might look artificially large (e.g., the treatment riders got rides *at the expense* of control riders, making the control group perform worse than they would have if the treatment never existed). 

Without one version of the treatment, the ATE becomes a muddy average of several wildly different treatments rather than a clear estimate of one specific intervention.

## How to Handle SUTVA Violations (Interference)

In modern tech, interference is the most common and difficult SUTVA violation. To deal with it, data scientists use alternative experimental designs:

1. **Cluster Randomization:** Instead of randomizing the treatment at the user level, you randomize at the cluster level (e.g., schools, cities, or highly connected friendship clusters). While individuals within a city interact, different cities rarely interfere with each other.
2. **Switchback (Time-Split) Experiments:** Used heavily in delivery and ride-sharing networks, this involves alternating entire regions between Treatment and Control over time (e.g., treating a city on Monday, turning it off Tuesday, treating again Wednesday). 
3. **Synthetic Controls:** Evaluating a treatment in a specific geographic region by comparing it against a mathematically constructed "synthetic" region that mirrors the treated region's pre-experiment trends.
