---
layout: distill
title: "Summary: Interference Across a Network (Lyft)"
description: "A summary of the Lyft Engineering blog post 'Interference Across a Network' detailing how naive A/B testing can bias effect estimates in ridesharing."
date: 2025-08-26
categories: dso-603 statistics
tags: causal-inference ab-testing experimentation network-effects
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

# Network interference in A/B testing

- A/B testing is not a fully solved problem. Lots of fruits left for reseaerchers.
- In ridesharing marketplace systems where supply and demand are affected by evolving network dynamics, user level RCT violates SUTVA and bias treatment effect.

- This post summarizes Part 1 of the Lyft Engineering series by Nicholas Chamandy, ["Experimentation in a Ridesharing Marketplace: Interference Across a Network"](https://eng.lyft.com/experimentation-in-a-ridesharing-marketplace-b39db027a66e), written in 2016. 

## The Problem: Network Dynamics and Pricing

- Consider a simple **undersupply** scenario: User A, User B, and **one available driver**.
- This triggers **"Prime Time" (surge pricing)**, which displays **prime time** badge in the Lyft app and the price is 1.5x higher than normal.
- We want to estimate the causal effect of subsidy for surge pricing (W=0: surge pricing, W=1: subsidy for surge pricing).
- Simplifying assumption: driver do not react to surge pricing. Only passengers react to surge pricing.

### Network effect
- Since there is only one driver, if user A requests a ride, user B cannot request a ride. 
- Therefore, user A's request affects user B's outcome. This is a violation of SUTVA.

### Causal estimand
- Let $Y_A$ and $Y_B$ be the number of rides completed by user A and user B, respectively. 
- Let $W_A$ and $W_B$ be the treatment assignments for user A and user B, respectively. 
- We are interested in the causal effect of the subsidy on the total number of rides completed, which is given by 
<p align="center">
\begin{equation*}
    \tau := E[Y_A + Y_B | W_A=1, W_B=1] - E[Y_A + Y_B | W_A=0, W_B=0]
\end{equation*}
</p>
- This definition is diffferent from ATE where unit indicators are collapsed. Since SUTVA is violated, we cannot use the standard ATE definition.

### Rider behavior model
- Whether user A opens the app first or user B opens the app first is uniformly random. 
- If no prime time, the user requests a ride with probability 1.
- If surge pricing is on, the user requests a ride with probability 0.5. 

### If there are parallel universes
1. **Global Control (No Subsidy for both):** Both users see Prime Time. 
   - By 0.5 + (1-0.5)*0.5 = 0.75 and symmetry, we have 
   <p align="center">
   \begin{equation*}
       E[Y_A + Y_B | W_A=0, W_B=0] = 0.5*0.75 + 0.5*0.75 = 0.75
   \end{equation*}
   </p>
2. **Global Treatment (Subsidy for All):** Neither sees Prime Time. Wait times aside, the first one to request gets the single driver.
   - The expected number of completed rides is exactly 
   <p align="center">
   \begin{equation*}
       E[Y_A + Y_B | W_A=1, W_B=1] = 0.5 + 0.5 = 1
   \end{equation*}
   </p>

The true causal treatment effect of the subsidy is an increase in completed rides from 0.75 to 1.0, a **33% increase**.

## Naive A/B Testing: Randomizing Users
- In reality, there is no parallel universe. We randomly pick a user and give subsidy. Another user do not receive subsidy. 
- without loss of generality assume user A is in control group (surge pricing) and user B is in treatment group (subsidy). 

### User A (Control; no subsidy; surge priced)
- Has a 50% chance to request. However, User A can only get a ride if they open the app first (50% chance). Otherwise, User B (subsidized) will request immediately and take the driver. 
- User A's expected rides is 

<p align="center">
\begin{equation*}
    E[Y_A + Y_B | W_A=0, W_B=1] = 0.25
\end{equation*}
</p>

- User A represents all users in parlalel universe 1. So $E[Y_A + Y_B | W_A=0, W_B=0]$ is estimated as $E[Y_A + Y_B | W_A=0, W_B=1] = 0.25$ 
- This is smaller than the true value 0.75

### User B (Treatment; subsidy; not surge priced)
- Opens app first (0.5) and gets a ride (*1) + opens the app late (0.5) but user A did not request a ride (*0.5) then user B gets a ride (*1) 

<p align="center">
\begin{equation*}
    E[Y_A + Y_B | W_A=1, W_B=0] = 0.5*1 + 0.5*0.5*1 = 0.75
\end{equation*}
</p>

### Estimated Treatment Effect

<p align="center">
\begin{equation*}
    \hat{\tau} = \frac{0.75 - 0.25}{0.25} = 2
\end{equation*}
</p>

The naive A/B test estimates a 200% increase in rides, overestimating the true global effect (33%) by a factor of six! 

## Statistical Interference

Why did this breakdown occur? It is due to a statistical phenomenon known as **interference**, which is a violation of the Stable Unit Treatment Value Assumption (SUTVA). 

A key assumption of causal inference is that a unit's potential outcomes are unaffected by the group assignments of *other* units. **Interference occurs when assigning User B to treatment negatively impacts the potential outcome of User A.** 

When User B's Prime Time was subsidized, User B "stole" the single driver with much higher probability, tanking User A's expected rides to 0.25. This drove the Control group down and the Treatment group up, exaggerating the true effect of the subsidy.

## Alternative Experiment Designs

Interference cannot be completely eradicated in a two-sided marketplace, but alternative experimental units give varying levels of protection against bias. You can randomize beyond the User level at coarser units:
- **App Sessions:** Moderate Bias, Moderate Variance.
- **Space (Blocks to Cities):** Low Bias, High Variance.
- **Time (Intervals):** Low Bias, High Variance.

Randomizing by City or by Time Interval provides strong protection against interference bias, but pays a steep cost: **Increased Variance**. Coarser randomization units drastically decrease your effective sample size and introduce more between-unit heterogeneity.

In its earlier days, Lyft dealt with this by randomizing **time intervals** (alternating the network between a global treatment period and a global control period) to combat bias despite the higher variance. 

*To rigorously quantify these tradeoffs, simulation frameworks are heavily utilized, which is the subject of Part 2.*
