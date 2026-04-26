---
layout: distill
title: "Causal Assumption: SUTVA and Ignorability"
description: "Understanding SUTVA and ignorability, fundamental assumptions in causal inference, what they mean, and what happens when they are violated."
date: 2025-08-24
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
- **Definition:** The potential outcomes for any unit do not vary with the treatments assigned to other units (Imbens and Rubin 2015, 10). 
- **Interpretation:** One unit's treatment assignment should not affect another unit's outcome. If you are in the treatment group, it shouldn't matter if your neighbor is in the treatment or control group. 

### Examples of "Interference" (SUTVA Violation)
- **Vaccination Programs:** If your neighbor gets a flu shot, your probability of getting the flu decreases even if you don't get the shot yourself (herd immunity). This is a classic example of interference.
- **Ridesharing Marketplaces:** If one driver is given a bonus to work in a certain area, it might affect the earnings and availability of other drivers in that same area, regardless of whether they also received the bonus.
- **Social Networks:** If your friend starts using a new social feature, you might be more likely to use it too, even if the feature wasn't directly rolled out to you.

## What Happens When SUTVA is Violated?

When SUTVA is violated, our estimates of the **Average Treatment Effect (ATE)** become biased. 
Specifically, the standard difference-in-means estimator $\hat{\tau} = \bar{Y}_{treated} - \bar{Y}_{control}$ no longer purely measures the effect of the treatment itself. 
It now also includes the "spillover" effects from other units' assignments.

In many marketplaces (like Uber or Lyft), this bias is typically negative. 
If we treat some users and they consume all the available drivers, the control group users will have worse outcomes (longer wait times) than they would have in a pure control world. 
This makes the treatment look better than it actually is.

## How to Handle SUTVA Violations (Interference)

In modern tech, interference is the most common and difficult SUTVA violation. To deal with it, data scientists use alternative experimental designs:

1.  **Cluster Randomization:** Instead of randomizing at the user level, we randomize at a higher level where interference is less likely (e.g., randomizing by city or by geographic neighborhood).
2.  **Switchback (Time-Series) Experiments:** We randomize the entire system between treatment and control states over different time windows.
3.  **Graph-based Randomization:** If we know the social or network connections between units, we can use graph-partitioning algorithms to ensure that treated units are mostly surrounded by other treated units (and same for control).

---

# Ignorability: When Does Linear Regression Yield Causal Inference?

## RCT is the gold standard
- In a Randomized Controlled Trial (RCT), we randomly assign units to treatment or control. 
- This ensures that, on average, the treatment and control groups are identical in all aspects (both observed and unobserved) except for the treatment itself. 
- Therefore, any difference in outcomes can be attributed directly to the treatment.

## Observational studies
- In observational studies, units are not randomly assigned. 
- People choose to take a treatment, or doctors decide who gets a drug based on their health status. 
- This leads to **confounding**: the treated group might be different from the control group in ways that also affect the outcome (e.g., wealthier people being more likely to buy a health supplement and also having better general health).

## Ignorability
To make causal claims from observational data, we need the **Ignorability Assumption** (also known as "Unconfoundedness" or "Selection on Observables"):

- **Definition:** $(Y_i(0), Y_i(1)) \perp W_i \mid X_i$
- **Interpretation:** Given a set of observed covariates $X$, the treatment assignment $W$ is as if it were random. There are no *unobserved* variables that affect both the treatment assignment and the potential outcomes.

## Overlap
- **Definition:** $0 < P(W_i = 1 \mid X_i) < 1$ for all $X$.
- **Interpretation:** For every possible value of the covariates, there is a non-zero probability of being in either the treatment or the control group. We can't compare treated and control units if some types of people *only* ever receive treatment or *only* ever receive control.

## Well specified linear model
If ignorability and overlap hold, we can estimate the causal effect by adjusting for $X$. A common way is using linear regression:
<p>
$$
Y_i = \alpha + \tau W_i + \beta X_i + \epsilon_i
$$
</p>
In this model, $\tau$ can be interpreted as the causal effect if the model correctly captures the relationship between $X$ and $Y$.


# References
- Imbens, G. W., & Rubin, D. B. (2015). Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction. Cambridge University Press.
- Keele, L. (2015). The Statistics of Causal Inference: A View from Political Methodology. Political Analysis.
- SUTVA (Stable Unit Treatment Value Assumption) - Causal Inference, Data Talks, Youtube Video. [link](https://youtu.be/wFpUKGNgb0Y?si=kf7eE0bYyNOMXaYi)