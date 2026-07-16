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


# Setting
## Unknown population quantity
- $P$: population distribution of $(X, Y, R)$. 
- $P_g, g \in \mathcal{G}$: population distribution of $(X, Y, R)$ for each state $g$.  Covairate shift assumption for subgroup: only the covariate distribution differs. Given covariate, distribution of Y is the same.
- We want to estimate: $E_{P_g}[Y]$ for any $g$.
## Known population quantity

- $P_X$: population covariate distribution. Known because we have access to Census data.
- $P_{g,X}, g \in \mathcal{G}$: covariate distribution for each state $g$. $P_X$ would be a mixture of $P_{g,X}$ for all states, where the mixing weights are the population shares of each state. 

## What we can easily estimate
- $S$: distribution of $(X, Y)$ conditioned on $R=1$. called survey distribution.
- $\mu_{S}(x) := E_{S} [Y | X = x] = E_P [Y|X = x, R= 1]$: condtional outcome for the survey population.

## Problem
We allow $R$ to be correlated to both X and Y. then niave conditional outcome approach of ijtegrating $\mu_{S}(x)$ with respect to $P_X$ fails. it is a biased esitmator of $E_{P_g}[Y]$.

Ideal case: MCAR (missing completely at random)
PP [Ri = 1 | Xi = x, Yi = y] = α0 ∀x ∈ X , y ∈ Y. (2)

Easy assumption: missing at random (MAR): similar to covariate shift assumption
PP [Ri = 1 | Xi = x, Yi = y] = α(x) ∀x ∈ X , y ∈ Y. (3)

Our assuption: (MNAR) if the probability of response can depend on the outcome, i.e. there exists a function $alpha$ : X × Y → [0, 1] such that  PP [Ri = 1 | Xi = x, Yi = y] = α(x, y) ∀x ∈ X , y ∈ Y.
equivalnetly, assuming that the probability of response depends on unobservable characteristics that are not independent from the outcome.



# Estimating equation
- A no-brainer solution for calculus level optimization is takeing the derivative and set it to zero.
-  maximum likelihood estimation in undergrad math stat is similar. a little difference is we plug in our data and take derivative with respect to the paramter. Casella book has both cases for constrained and uncosnraiint case.
An estimating equation is simply a generalized version of this: we define a function $\Psi$, plug in our data, and solve for the parameters that make $\Psi = 0$.


- the survey data is biased.
- To fix this, the authors want to "tilt" the survey distribution to match the true population distribution.
  - $\theta$ is the parameter that controls how much we tilt the distribution based on unobservables (Assumption 1)
  - known facts about the general population (moment conditions) act as constraint. 
  - They want to find a tilted distribution that is as close as possible to the survey data (minimizing the KL divergence) while still strictly matching those known population facts.

- Because this is a constrained optimization problem, we use a Lagrangian. This introduces a second parameter, $\lambda$, which is a penalty multiplier for breaking the moment constraints. Together, we are trying to solve for $\nu = (\theta, \lambda)$.

## The "Naive" Estimating Equations (Equations 16 & 17)
If we had perfect, infinite data,  finding $\nu$ would just require taking the derivative of the (expected) Lagrangian and setting it to zero, while ensuring our constraints are met. This gives us the first two pieces of our puzzle:$\text{DL}(\nu; \mu)$: This is the derivative of the Lagrangian with respect to $\theta$. Setting this to zero is the mathematical equivalent of finding the minimum KL divergence.$M(\nu; \mu)$: This is the moment constraint. at the same time it is the lagrangian derivative with respect to lambda. 

solving this system is classical lagraigian solution of constraint optimization.

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



