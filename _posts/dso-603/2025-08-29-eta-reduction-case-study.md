---
layout: distill
title: "Case Study: Causal Effect of ETA Reduction"
description: "A practical case study on measuring the causal effect of reducing Estimated Time of Arrival (ETA) in a ridesharing marketplace."
date: 2025-08-29
categories: dso-603 statistics
tags: causal-inference case-study marketplace experimentation
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jong-min.org"
bibliography: 2025-08-29-eta-reduction-case-study.bib
---

# Speculation before experiment  

Consider ETA in the ride-hailing industry, defined as the estimated time for a driver to reach the rider’s pickup location. ETA is a key driver of revenue for several reasons:

### Short-term competitive advantage  
- Ride-hailing is largely commoditized.  
- This is because trips are short and similar-getting from A to B-so differentiation between Uber and Lyft is minimal.  
- Riders are most sensitive to **price** and **wait time**.  
- Lower ETA wins marginal users who multi-home (check multiple apps).  
- For example, as a student in LA, I compare both apps: price first (often different), then ETA if prices are similar—especially during undersupply (e.g., after games or concerts).  

### Long-term competitive advantage  
- Over time, if users learn one platform is reliably faster (e.g., Uber arrives ~3 minutes sooner), they stop checking alternatives.  
- Lower ETA → faster pickups → less idle driving → more billable trips → higher driver earnings and greater platform throughput.



# Experiment for short-term competitive advantage
Let us design an experiment to measure the short-term causal effect of ETA reduction

## Treatment
- Introduce a new matching algorithm to reduce average ETAs by x minutes (or y%), or simply inflate the control group's displayed ETA by the equivalent amount.

- The engineering team will define x and y. These values must remain uniform to uphold the SUTVA assumption of a single treatment version

## Metric
We need to define metrics to quantitatively evaluate the impact of reducing ETA. One metric isn't enoguh. we need at least 3 metrics to ensure we aren't optimizing one area at the expense of another.

### Primary Metric: Session Conversion Rate

We use the conversion rate as the primary metric. Conversion rate can be defined in many ways <d-cite key="amazon-conversion"></d-cite>

Session Conversion Rate: The percentage of app opens that result in a completed booking.
<p>
\begin{equation*}
\text{Session Conversion Rate} = \frac{\text{Number of completed trips}}{\text{Number of app opens}}
\end{equation*}
<\p>

### Secondary  Metric: Rider Cancellation Rate
Seconday metrics help explain the *why* behind the primary metric's movement: **If the primary metric goes up, secondary metrics reveal the mechanism** (e.g., users are finding the button faster). We consider the Rider Cancellation Rate as secondary metric:

<p>
\begin{equation*}
\text{Rider Cancellation Rate} = \frac{\text{Number of canceled trips}}{\text{Number of requested trips}}
\end{equation*}
</p>



### Guardrail Metrics:
We do not necessarily want to improve this, but we want to ensure it does not degrade. 

- ETA reduction is meaningless if the ETA is not accurate. We consider the ETA Mean Absolute Error (MAE) as a guardrail metric:

<p>
\begin{equation*}
\text{ETA MAE} = \frac{1}{N} \sum_{i=1}^{N} \big| \text{Predicted ETA}_i - \text{Actual Arrival Time}_i \big|
\end{equation*}
</p>

- Match Rate / Unfulfilled Requests: Ensuring the system isn't breaking to achieve artificially low ETAs.
## Experiment Design

### Network interference
Here the unit is app user. App users in ridesharing marketplace are notoriously **networked** since they share the same pool of drivers. This violates the SUTVA assumption of no interference. Consider the following scenario where ETA reduction has positive effect on conversion rate.
- If Treatment users receive a lower ETA, they will book more rides.
- By booking more rides, they consume the limited, shared supply of vehicles in the neighborhood.
- The Control users, sharing the exact same physical neighborhood, are now starved of cars. This forces their *actual* ETAs to rise and their conversion to drop artificially.
- The estimated treatment effect will be wildly exaggerated, making the ETA reduction look far more powerful than it actually is globally.



###  Switchback Experiments

Instead of randomizing individual users, we randomize the entire state of the marketplace over time intervals or small regions. 
We can then compare the aggregated conversion rate during the Treatment windows versus the Control windows.

## Confounding Scenarios
When the experimental results contradict our underlying intuition (e.g., shorter ETAs failing to improve or even hurting conversion), it is usually driven by unobserved confounding or our insight is wrong. Below is a key scenario where this occurs.

### Geographic Selection Bias
Running a switchback experiment in a geographic zone that is too small or entirely homogeneous can yield results that do not generalize to the broader network.

- Suppose we run a switchback experiment exclusively in the University Park area in Los Angeles. The ride-hailing demand here is heavily dominated by a single demographic: USC students. The trip composition is highly skewed toward short-distance rides between campus, nearby apartments, and local retail (e.g., Ralphs, Target, local restaurants).
This creates two distinct behavioral distortions:
  - Diminishing Returns on Speed: Because the geographic footprint is so small, baseline ETAs are likely already very short. Shaving 1 minute off a 3-minute ETA provides negligible marginal utility to a student taking a 5-minute ride.
  - Denominator inflation: College students frequently use the app as a planning tool while getting ready in their dorms or apartments. If the quoted ETA is too short (e.g., 1 minute), they will not request the ride because they aren't physically ready to walk out the door. They will close the app, finish getting ready, and request later. This artificially inflates the denominator (sessions) without increasing the numerator (orders), tanking the session conversion rate for the treatment group.

- The Root Cause: Setting the geographic zone too small restricts our sample to a highly homogenous population. We are no longer measuring the Global Average Treatment Effect (ATE) for the platform; we are measuring a very specific Conditional Average Treatment Effect (CATE) for college students taking short trips.

- The Remedies:
  - Expand and Diversify the Experimental Units: Instead of running the switchback in a single hyper-local neighborhood, define the experimental units at the city or macro-regional level (e.g., all of Los Angeles County). If you must use smaller zones, ensure the experiment runs across a representative sample of zone types (e.g., mixing University Park with Downtown LA business districts, and suburban areas like Pasadena) so the aggregate result reflects the true market variance.
  - Redefine the Conversion Metric: Augment the primary "Session Conversion Rate" with a "User-Level Time-Bounded Conversion Rate" (e.g., Did the user book a ride within 15 minutes of their first app open?). This captures the student who closed the app because the ETA was too fast, but successfully booked 10 minutes later when they were actually ready.

### Matching algorithm backfired
- Greedy algorithms (matching the absolute closest car instantly) keep ETAs incredibly low but can create network imbalances, leading to "No Cars Available" screens for other users in the same neighborhood.
- On the other hand, consider the scenario where the control group algorithm uses a batching window.
  - For example, waiting 10–15 seconds to collect all neighborhood requests before dispatching to find the global optimum. In this case, the quoted ETA will naturally be slightly higher.
  - However, this global optimization dramatically reduces the number of failed matches. -- Because almost everyone who opens the app is guaranteed a ride (no error screens), the overall session conversion can go up.

###  Cannibalization Effect

- Imagine a user opens the app and sees UberX has an unusually high ETA of 12 minutes, but Uber Comfort or UberPool is only 5 minutes away.
Instead of closing the app (which would hurt conversion), the user upgrades to Comfort or shifts to Pool. The overall session conversion for the app goes up, even though the primary product's ETA degraded.
 
 
 
