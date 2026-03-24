---
layout: distill
title: "Causal Assumption: SUTVA and Ignorability"
description: "Understanding SUTVA and ignorability, fundamental assumptions in causal inference, what they mean, and what happens when they are violated."
date: 2025-08-24
categories: dso-603 statistics
tags: causal-basics
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
toc:
  - name: Rubin Potential Outcomes Framework
  - name: SUTVA
    subsections:
      - name: 1. Consistency: One Version of the Treatment
      - name: 2. No Interference
      - name: What Happens When SUTVA is Violated?
      - name: How to Handle SUTVA Violations (Interference)
  - name: Ignorability: When Does Linear Regression Yield Causal Inference?
    subsections:
      - name: RCT is the gold standard
      - name: Observational studies
      - name: Ignorability
      - name: Overlap
      - name: Well specified linear model
  - name: References
---

# Rubin Potential Outcomes Framework
- Every experimental  unit (e.g. user) walks around with two pieces of paper, one in each back pocket.
- On one of these papers is written that subject’s inevitable outcome should she happen to be assigned to the control group.
On the other piece of paper is written her outcome given assignment to the treatment. Together, the two pieces of paper are a unit’s potential outcomes.
- In ideal universe, we will take one unit and observe both potential outcomes. The causal inference is done.
- But in reality, we can only observe one of the potential outcomes for each unit. Therefore we need at least to units: one for treatment and one for control.
- When there are many units, whether in a randomized A/B test or an observational study, we rely heavily on the **Stable Unit Treatment Value Assumption (SUTVA)**. 
For observational studies, in addition to SUTVA,another important assumption is ignorability (or unconfoundedness).


# SUTVA
- SUTVA consists of two distinct components:
  1.  **Consistency**: No hidden variations of treatment.
  2.  **No Interference** 
   
- Consistency is straightforward, but there's no remedy if it is violated. 
- No intererence is complicated, but there are many remedies.
## 1. Consistency: One Version of the Treatment

- **Definition:** For each unit, there are no different forms or versions of each treatment level, which lead to different potential outcomes (Imbens and Rubin 2015, 10; Keele 2015b, 5)

- **Interpretation:** If a unit receives "Treatment A", it must mean the exact same thing across all units. This also means that the experiment must be well-defined.
- This is very crucial and if this is violated, there is no remedy.

### Examples of SUTVA Violations for "One Version"
- **Dosage Variations:** If the treatment is defined as "taking Aspirin," but some people take 100mg and others take 500mg, we don't have one version of the treatment. Same for "exercise".  Is it 10 minutes running considered as exercise? is 1 hour of playing wii sports considered as exercise? 
- **Surgical Procedures:** If the treatment is "receiving knee surgery," but one surgeon is world-class and another is inexperienced, the treatment varies wildly depending on who performs it.
- **Software Rollouts:** If a UI feature performs very fast on iOS but is buggy and slow on Android, treating "Feature X" as a single uniform treatment will blur the causal effect.

## 2. No Interference

**Definition:** The potential outcomes for any unit do not vary with the treatments assigned to other units

<p align="center">
\begin{equation*}
    Y_1(W_1) = Y_1(W_1 | W_2=0) = Y_1(W_1 | W_2=1) =  ... = Y_1(W_1 | W_n=w_n)
\end{equation*}
</p>

Simply put, what happens to *you* under a treatment or control condition is not affected by whether *someone else* is in the treatment or control group. 

### Examples Validating "No Interference"
- **Medical Trials (Non-Infectious):** If a patient takes a pill for a headache, it does not alleviate or worsen another patient's headache. The outcome for Patient A only depends on Patient A's treatment.
- **Standard E-commerce A/B Tests:** If User A sees a blue "Buy" button and User B sees a red one, User A's likelihood to purchase is  independent of User B's experience.

### Examples of "Interference" (SUTVA Violation)
- **Vaccines:** In infectious diseases, if everyone around you is vaccinated (Treatment), your potential outcome of getting sick (Control) drops drastically due to herd immunity. Even if not seriously infectious, the control group patient might share his drug with his friends because the drug is a cure and expensive.
- **Social Networks:** If Facebook tests a feature that makes users post more, and your friends get the treatment, your feed will have more posts—even if you are in the control group. This is often called **network spillover**.
- **Two-Sided Marketplaces (Ride-sharing):** If a new feature makes treatment riders match with drivers much faster, it removes available drivers from the road, making control riders wait longer ("crowd-out effect"). 



## What Happens When SUTVA is Violated?

When SUTVA is violated, our estimates of the **Average Treatment Effect (ATE)** become biased. 

Without one version of the treatment, the ATE becomes a muddy average of several wildly different treatments rather than a clear estimate of one specific intervention.

If there is interference, the difference between the Treatment and Control groups might look artificially large.
For example, in the ride-sharing case, the treatment riders got rides *at the expense* of control riders, making the control group perform worse than they would have if the treatment never existed. See [Lyft blog post](https://eng.lyft.com/challenges-in-experimentation-be9ab98a7ef4) for detailed discussion.



## How to Handle SUTVA Violations (Interference)

In modern tech, interference is the most common and difficult SUTVA violation. To deal with it, data scientists use alternative experimental designs:

1. **Cluster Randomization:** Instead of randomizing the treatment at the user level, you randomize at the cluster level (e.g., schools, cities, or highly connected friendship clusters). While individuals within a city interact, different cities rarely interfere with each other.
2. **Switchback (Time-Split) Experiments:** Used heavily in delivery and ride-sharing networks, this involves alternating entire regions between Treatment and Control over time (e.g., treating a city on Monday, turning it off Tuesday, treating again Wednesday). 
3. **Synthetic Controls:** Evaluating a treatment in a specific geographic region by comparing it against a mathematically constructed "synthetic" region that mirrors the treated region's pre-experiment trends.

# Ignorability: When Does Linear Regression Yield Causal Inference?

## RCT is the gold standard
The simplest solution to the fundamental problem of causal inference is to run a Randomized Controlled Trial (RCT). In an RCT, the treatment and control groups are **balanced** on average, meaning they are **drawn from the same underlying distribution**. In other words, the sample means $\bar{y}_0$ and $\bar{y}_1$ estimate the average outcomes under control and treatment for the **exact same population** <d-cite key="frangakis2004principal"></d-cite>. ATE estimation is simple: just take the difference in means: $$\text{ATE} = \bar{y}_1 - \bar{y}_0$$

## Observational studies
In reality, RCTs are often prohibitively expensive, meaning we frequently must rely on observational data. Unlike in an RCT, treatments in observational studies are not randomly assigned; they are simply observed. As a result, systematic differences usually exist between the treated and untreated groups—a problem known as confounding.

However, if certain assumptions are met, we can still estimate the Average Treatment Effect (ATE) from observational data. Doing so simply requires more sophisticated estimators, moving beyond a naive difference in means to methods like linear regression.


## Ignorability:
The key assumption is ignorability (also known as unconfoundedness). Intuitively, this means that instead of having a single randomized trial for the entire population, we essentially have a "mini-RCT" for every specific value of our observed covariates. Mathematically, this is expressed as conditional independence :
$$Y^{(0)},Y^{(1)} \perp T \mid X$$
This is a strong assumption! It requires that we haven't missed any pre-treatment covariates (unobserved confounders) that affect both the treatment assignment and the outcome. However, if this assumption holds—alongside the positivity assumption—we can estimate the Average Treatment Effect (ATE) from observational data using linear regression.

## Overlap
While ignorability concerns the dependence structure of the data, our second requirement restricts the assignment probabilities. This assumption—known as positivity or overlap—requires that for every possible value of our covariates, we observe subjects in both the treatment and control groups. Mathematically, the probability of receiving treatment given the covariates must be strictly between zero and one:
$$0 < P(T=1 \mid X=x) < 1$$
for all $x$ in the support of $X$.

## Well specified linear model
The final requirement for using linear regression in causal inference is that the model must be correctly specified. This means the underlying true data-generating process must follow this exact linear form:
$$Y = D\theta_0 + X^\top b_0 + \varepsilon$$
where the error term, $\varepsilon$, is independent of both the treatment $D$ and the covariates $X$. In other words, $D$ and $X$ must genuinely have a linear relationship with the outcome $Y$. Because this is an incredibly stringent and rarely realistic assumption, basic linear regression is often impractical for real-world causal inference. Instead, it serves primarily as a conceptual stepping stone for understanding more advanced methodologies.

# References
- Imbens, Guido W, and Donald B Rubin. 2015. Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction. Cambridge University Press.
- Keele, Luke. 2015b. “The Statistics of Causal Inference: A View from Political Methodology.” Polit. Anal. 23 (3): 313–35.
- Applied Causal Inference (with R) Paul C. Bauer, Version: 29 May, 2020. [link](https://bookdown.org/paul/applied-causal-analysis/sutva1.html)
- SUTVA (Stable Unit Treatment Value Assumption) - Causal Inference, Data Talks, Youtube Video. [link](https://youtu.be/wFpUKGNgb0Y?si=kf7eE0bYyNOMXaYi)
- Nicholas Chamandy, Experimentation in a Ridesharing Marketplace. Lyft Engineering blog post. [link](https://medium.com/@nicholas.chamandy/experimentation-in-a-ridesharing-marketplace-5b8701973677)
- Yingying Fan, Lecture note for DSO 603: Causal Inference with Modern Machine Learning Methods. Department of Data Sciences and Operations, University of Southern California.
- Stefan Wager, Lecture note for STA 361: Causal inference. Department of Statistics, Stanford University.