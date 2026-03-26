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



# The Business Question

In any on-demand marketplace (ridesharing, food delivery, logistics), a critical user-facing metric is the **Estimated Time of Arrival (ETA)**. A fundamental business question invariably arises: 

> *"What is the exact causal effect of reducing ETA by 1 minute on a user's probability of requesting a ride (conversion)?"*

Understanding the true price elasticity and time elasticity of demand is crucial. If the platform mathematically knows how much 1 minute of ETA is worth in revenue, it can perfectly optimize its dispatch distances, dynamic pricing, and driver incentives to maximize efficiency.

---

# Why is this so hard to measure?

## 1. The Trap of Observational Data (Endogeneity)

The most naive approach is to query historical data: plot a scatterplot of ETA on the x-axis and Conversion Rate on the y-axis, and draw a regression line. 

If you attempt this in a real ridesharing network, you will often find a surprisingly flat line, or sometimes even a **positive** correlation (higher ETA = higher conversion). Does this mean customers actually *prefer* waiting longer for their driver? 

Of course not. This is a classic violation of the unconfoundedness assumption, specifically **Omitted Variable Bias (Endogeneity)**. 
- During a rainstorm, a blizzard, or rush hour, demand naturally surges. 
- Because demand surges, available vehicle supply drops, causing average ETAs to spike across the city.
- However, because it's raining or cold, riders' outside options (like walking, biking, or taking the bus) vanish. Their *intent to book* is drastically higher.
- Therefore, they book the ride *despite* the high ETA. 

The external environmental context (weather, rush hour, events) acts as a massive confounder that entirely masks the true negative elasticity of ETA.

## 2. The Trap of Standard A/B Testing (Interference)

Since historical observational data is hopelessly confounded, the natural next step for a data scientist is a randomized A/B test. We could artificially inflate the ETA display by 2 minutes for the Control group, or physically improve the ETA for the Treatment group by allowing their requests to search a much wider radius for drivers.

As discussed in our previous posts on the SUTVA assumption, this fails catastrophically due to **Network Interference**. 
- If Treatment users receive a lower ETA, they will book more rides.
- By booking more rides, they consume the limited, shared supply of vehicles in the neighborhood.
- The Control users, sharing the exact same physical neighborhood, are now starved of cars. This forces their *actual* ETAs to rise and their conversion to drop artificially.
- Your estimated treatment effect will be wildly exaggerated, making the ETA reduction look far more powerful than it actually is globally.

---

# How do we actually measure the causal effect?

Data scientists employ several advanced causal inference techniques to cut through the noise of endogeneity and the bias of network interference.

## Approach 1: Instrumental Variables (IV)

An **Instrumental Variable (IV)** is something that is highly correlated with the ETA (the treatment) but has absolutely no direct relationship with the user's inherent intent to book (the outcome) or the confounding variables (like weather).

**The Instrument:** *Random Supply Shocks.*
Imagine User A opens the app. By pure luck, a driver just dropped off another passenger on the exact same block 5 seconds ago. User A gets a 1-minute ETA. 
User B opens the app a block away, but no driver randomly dropped off nearby, so they get a 5-minute ETA. 

This localized, micro-level variation in supply is functionally random. It is deeply correlated with the ETA but completely uncorrelated with whether it's raining or rush hour. By using this random supply shock as an instrument, we can isolate the unconfounded causal effect of ETA on conversion.

## Approach 2: Switchback Experiments

Instead of randomizing individual users, we randomize the entire state of the marketplace over time.

We can run a **Switchback Experiment** where we alternate the system's dispatch parameters (which dictate aggregate average ETAs) every 30 minutes in a single city. 
- **12:00 PM - 12:30 PM (Treatment):** highly aggressive dispatch $\rightarrow$ Faster ETAs overall.
- **12:30 PM - 1:00 PM (Control):** Standard dispatch $\rightarrow$ Standard ETAs.

By keeping the entire city in the same uniform state, we neutralize user-level competitive interference. We can then compare the aggregate conversion rate during the Treatment windows versus the Control windows.

## Approach 3: Geospatial Discontinuity

Sometimes, platform algorithms or driver incentive zones create hard geographic boundaries on the map. 
- **Zone A:** Drivers receive a massive $10 bonus per ride, so supply is abundant and ETAs are 2 minutes.
- **Zone B:** Drivers receive no bonus, so supply is sparse and ETAs are 7 minutes.

If we look at users standing perfectly on the border between Zone A and Zone B (perhaps one side of the street vs. the other), they are essentially identical in demographics, intent, and macro weather patterns. The only difference is an arbitrary boundary line slicing down the middle of the street altering their supply. Applying a **Regression Discontinuity Design (RDD)** spatially across this boundary allows us to cleanly estimate the impact of the ETA difference.

---

# Conclusion

Measuring the causal impact of ETA lies at the absolute heart of marketplace operations. Because simple queries are plagued by endogeneity and standard A/B tests are biased by network interference, estimating this single parameter requires the full toolkit of advanced experimental design and causal inference.
