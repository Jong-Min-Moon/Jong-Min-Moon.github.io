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



A/B testing is not a solved problem. In ridesharing marketplace systems where supply and demand are affected by network effects, naively randomizing users into control and treatment groups can violently bias the effect estimates.

This post summarizes Part 1 of the Lyft Engineering series by Nicholas Chamandy, ["Experimentation in a Ridesharing Marketplace: Interference Across a Network"](https://eng.lyft.com/experimentation-in-a-ridesharing-marketplace-b39db027a66e), written in 2016. 

## The Problem: Network Dynamics and Pricing

Consider a simple, microscopic example of **undersupply**: Two prospective passengers (User A and User B) open the app simultaneously, but there is only **one available driver**. To maintain driver availability, Lyft may trigger "Prime Time" (surge pricing).

Suppose Lyft wants to test the effect of **subsidizing Prime Time** (paying the surge cost on the passenger's behalf). The metric of interest is the **total number of rides completed on average**.
- If a user sees Prime Time, they have a 50% chance of requesting a ride.
- If a user receives the subsidy (does not see Prime Time), they have a 100% chance of requesting a ride.

### Comparing the Parallel Universes
To find the **Global Average Treatment Effect (ATE)**, we examine two counterfactuals:
1. **Global Control (No Subsidy):** Both users see Prime Time. 
   - A requests 50% of the time, B requests 50% of the time. 
   - If both request, only one can get a ride.
   - Using basic probability, the expected number of completed rides is **0.75**.
2. **Global Treatment (Subsidy for All):** Neither sees Prime Time. Wait times aside, the first one to request gets the single driver.
   - The expected number of completed rides is exactly **1.0**.

The true causal treatment effect of the subsidy is an increase in completed rides from 0.75 to 1.0, a **33% increase**.

## Naive A/B Testing: Randomizing Users

If we test this subsidy by randomly assigning passengers to groups, we create a third, mutually exclusive universe. Suppose User A is assigned to the **Control Group** (sees Prime Time) and User B is assigned to the **Treatment Group** (gets the subsidy). 

Let's calculate the expected rides for each user under this naive randomization:
- **Treatment User B:** Has a 100% chance to request. User B will *always* get the driver, unless User A happened to open the app slightly earlier (50% chance) *and* decided to accept Prime Time (50% chance of that half). User B's expected rides is **0.75**.
- **Control User A:** Has a 50% chance to request. However, User A can only get a ride if they open the app first (50% chance). Otherwise, User B will request immediately and take the driver. User A's expected rides is **0.25**.

Calculating the **Estimated Treatment Effect**:
- (Treatment - Control) / Control = (0.75 - 0.25) / 0.25 = **+200%**.

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
