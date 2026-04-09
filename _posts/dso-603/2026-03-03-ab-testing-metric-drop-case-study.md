---
layout: distill
title: "Case Study: Diagnosing and Addressing a Metric Drop"
description: "An end-to-end framework for investigating MAU drops, targeting at-risk users, and making data-driven 'ship' decisions."
date: 2026-03-03
categories: dso-603 statistics
tags: a-b-testing case-study product-analytics metrics
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jong-min.org"
---

Remember the framework:

### 1. Set the Context for the Experiment
- **Define the objective**
  - Clarify the business goal  
  - Determine the purpose of the experiment  
  - Assess whether an A/B test is appropriate  

- **Formulate the hypothesis**
  - Define treatment and control  
  - State the hypothesis clearly  
  - Identify:
    - Success metrics  
    - Guardrail metrics  
    - Tracking metrics  

---

### 2. Design the Experiment
- **Choose the unit of randomization**
  - Ensure metrics can be accurately measured  
  - Minimize interference and network effects  
  - Consider user experience  

- **Select statistical methods**
  - Common tests:
    - t-test or z-test  
  - Alternative approaches:
    - Quasi-experimental methods (e.g., difference-in-differences)  
  - Determine if adjustments are needed:
    - Heteroskedasticity-robust standard errors  
    - Clustered standard errors  

- **Plan sample size and power**
  - Conduct power analysis using:
    - Minimum Detectable Effect (MDE)  
    - Statistical power  
    - Type I error rate (α)  

Monthly active users (MAU) is a key performance indicator (KPI) that measures the number of unique users who engage with a site or app within a month. It serves as a main metric for assessing a company's overall health and user engagement, often influencing investor sentiment.

While MAU is usually tracked using unique identifiers like emails or usernames, measurement methods vary across platforms, making direct comparisons between companies difficult.

# Phase  1: Diagnosing the Metric Drop

Before designing an experiment, you have to find the root cause of the problem.

### 1. The MAU dropped by 7%, how would you investigate?

A 7% drop in Monthly Active Users (defined as completing $\ge 1$ ride) is significant. I would slice the data to isolate the anomaly:

*   **Time:** Was the drop sudden (e.g., a bug introduced in a recent app release, a server outage in dispatch) or gradual (seasonal trends, slowly increasing churn)?
*   **Funnel Analysis:** Where in the user journey are they dropping off? Are app opens down? Are users requesting rides but canceling due to long wait times or high surge pricing (a supply-side issue)? Are drivers canceling more often?
*   **Segmentation:** I would check if this drop is isolated to a specific geographic region, a specific platform (iOS vs. Android), or a specific user cohort (e.g., new riders vs. power users).

### 2. How do you know if it resulted from external competitors?

If the drop is external, you will usually see it localized by geography or user behavior rather than a technical failure:

*   **Geographic isolation:** Did the drop occur specifically in a market where a competitor recently launched, expanded, or is heavily subsidizing rides with promotions?
*   **App behavior:** Are we seeing an increase in "abandoned carts"? For instance, a user opens the app, checks the price of a trip, and then closes it without requesting. This often indicates they are comparing prices with a competitor app and finding us more expensive.
*   **Third-party data:** We can look at external market share reports, app store download rankings, or credit card panel data to see if a competitor's transaction volume spiked concurrently.

---

# Part 2: Applying the A/B Test Framework

Once we determine the issue is internal (e.g., existing users are churning due to lack of engagement), we move to the experiment phase.

## Phase 1: Set the Context

*   **Experiment Purpose:** Decrease churn among existing users to stabilize MAU.
*   **Treatment:** A time-boxed coupon (expires in 7 days) to incentivize them to take a ride.

### Who to give coupons to (Eligible Users)

We shouldn't give coupons to everyone. If we give coupons to users who were going to ride anyway, we cannibalize our own revenue. Conversely, if we give them to users who have permanently uninstalled the app, it's wasted effort.

*   **Targeting:** I would frame this as an optimization problem. We want to target users with a high probability of churn but a high potential Lifetime Value (LTV). We could use a causal inference approach (like uplift modeling) to identify users who have the highest heterogeneous treatment effect—meaning their behavior is most likely to change because of the coupon.

### Metrics

*   **Success Metric:** Day-14 or Day-30 Retention Rate (Did they complete a ride within the window?). Incremental trips per user.
*   **Guardrail Metrics:** Average Profit Margin per User (we are subsidizing rides, so we must ensure we don't bleed too much cash). Driver-side earnings (ensure the promotion doesn't negatively impact the supply side's unit economics).
*   **Tracking Metrics:** Coupon redemption rate.

## Phase 2: Experiment Design

*   **Unit of Randomization:** Randomizing at the user level is the standard approach here. We want to avoid session-level randomization because a user might log in, not see a coupon, log out, log back in, and suddenly see one, resulting in a poor user experience and diluted data.

### Measuring Cost and Value (Trade-offs)

To measure the financial impact, the design needs to account for incremental lift.

*   **Cost:** The actual dollar amount of the redeemed coupons + the engineering cost of running the campaign.
*   **Value:** The gross booking value (GBV) of the incremental rides generated by the treatment group that the control group did not take.

### Analysis

We are looking for the **Incremental ROI**. We would likely use a standard two-sample t-test on the mean revenue per user, or a z-test of proportions for the retention metric.

### Implementation Note

Following the framework, I would launch this to a 1% traffic allocation initially. A bug in a pricing promotion can be incredibly costly, so we must verify the redemption logic and data pipelines for 48 hours before ramping up.

---

# Part 3: The "Gotcha" Decision

**Question: Let’s say the result is statistically significant but not practically significant, would you ship it or not, and why?**

I would **not** ship it. 

*   **The reasoning:** Statistical significance only tells us that we are confident the coupon caused some effect (we reject the null hypothesis). However, practical significance (the Minimum Detectable Effect, or MDE) tells us if that effect is actually worth the cost of doing business.
*   **The business reality:** If our MDE was 5% to justify the millions of dollars spent on the coupon subsidies and the engineering hours required to maintain the promo code infrastructure, but our stat-sig lift was only 0.5%, we are losing money.
*   **The exception:** The only reason I would discuss shipping it is if the cost of the treatment was absolute zero and it required zero maintenance—but in a marketplace where you are actively giving away margin via coupons, a practically insignificant lift is a net-negative for the company's bottom line.
