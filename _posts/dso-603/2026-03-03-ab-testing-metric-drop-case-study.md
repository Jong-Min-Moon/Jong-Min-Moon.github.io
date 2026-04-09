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
bib_file: dso-603
bibliography: dso-603.bib
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

Monthly active users (MAU) <d-cite key="investopedia-mau"></d-cite> is a key performance indicator (KPI) that measures the number of unique users who engage with a site or app within a month. It serves as a main metric for assessing a company's overall health and user engagement, often influencing investor sentiment. While MAU is usually tracked using unique identifiers like emails or usernames, measurement methods vary across platforms, making direct comparisons between companies difficult. 

Consider a ride-hailing service. Let us define Monthly Active Users as the number of users completing $\ge 1$ ride. Suppose the company observes a 7% drop in MAU.


### 1. 
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
# Phase  1: Set the Context for the Experiment

* The primary business goal is to decrease churn among existing users to stabilize MAU. The stakeholders are thinking of giving coupons.
  
* Is it worth running the experiment? Then the MAU drop should not be due to natural factors.

## Is the drop natural?
 You would slice the data to isolate the anomaly:

*   **Time:** Was the drop sudden (e.g., a bug introduced in a recent app release, a server outage in dispatch) or gradual (seasonal trends, slowly increasing churn)?
*   **Funnel Analysis:** Where in the user journey are they dropping off? Are app opens down? Are users requesting rides but canceling due to long wait times or high surge pricing (a supply-side issue)? Are drivers canceling more often?
*   **Segmentation:** I would check if this drop is isolated to a specific geographic region, a specific platform (iOS vs. Android), or a specific user cohort (e.g., new riders vs. power users).


## Is the drop resulted from external competitors?

If the drop is external, you will usually see it localized by geography or user behavior rather than a technical failure:

*   **Geographic isolation:** Did the drop occur specifically in a market where a competitor recently launched, expanded, or is heavily subsidizing rides with promotions?
*   **App behavior:** Are we seeing an increase in "abandoned carts"? For instance, a user opens the app, checks the price of a trip, and then closes it without requesting. This often indicates they are comparing prices with a competitor app and finding us more expensive.
*   **Third-party data:** We can look at external market share reports, app store download rankings, or credit card panel data to see if a competitor's transaction volume spiked concurrently.


## Formulate the hypothesis

### Treatment
* A targeted, 7-day expiration coupon (e.g., 20% off your next ride) delivered via push notification. 
* Note that we will ranomly send coupons among the targeted users. So we still have RCT.

### Hypothesis
* Sending a time-boxed coupon to at-risk users will incentivize them to take a ride, retaining them as an MAU and generating a net-positive ROI compared to the control group.

### Metrics
* **Success metrics:** Day-14 or Day-30 Retention Rate (Did they complete a ride within the window?). Incremental trips per user. Incremental Gross Booking Value (GBV).
* **Guardrail metrics:** Average Profit Margin per User (we are subsidizing rides, so we must ensure we don't bleed too much cash). Driver-side earnings (ensure the promotion doesn't negatively impact the supply side's unit economics).
* **Tracking metrics:** Coupon open rate, Coupon redemption rate.  

# Phase 2: Experiment Design


### Population
Deciding who to give coupons to (Eligible Users).

We shouldn't give coupons to everyone. Giving them to guaranteed riders cannibalizes revenue, while giving them to completely lost users is wasted effort. I would frame our targeting as an optimization problem:

* The Target Profile: Users with a high probability of churning (e.g., no app opens in 14 days) but a historically high Lifetime Value (LTV).

* The Methodology: We should use uplift modeling (a causal inference approach) to identify users with the highest heterogeneous treatment effect. This ensures we only subsidize users whose behavior will actually change because of the intervention.


### Unit of Randomization
- Because this is a stateful, long-term intervention aimed at a 30-day MAU metric, switchback testing is inappropriate due to severe temporal spillover. Instead, I would recommend a Geo-experiment using a Synthetic Control. Alternatively, if we need to move faster and have a large enough user base, we could use User-Level randomization but restrict the treatment to less than 1% of traffic to ensure the incremental demand doesn't cause driver starvation for the control group.

1. Geo-Experimentation (Cluster Randomization) + Synthetic Control
This is the most robust way to test marketplace pricing and promotions.

- The Design: You randomize at the market (city) level. You select a few treatment cities to launch the churn-reduction coupon campaign, leaving the rest of your cities as the control.

- Why it works: It perfectly isolates the driver pools. The drivers in Chicago (Control) are completely unaffected if the riders in Seattle (Treatment) suddenly start taking more rides. You can easily track the 30-day MAU retention in Seattle without interference.

- The Analysis: Because cities naturally behave differently, a simple t-test won't work. You would use Difference-in-Differences (DiD) or a Synthetic Control Method (like Google's CausalImpact algorithm) to construct a "fake Seattle" using a weighted blend of control cities, and measure the long-term lift against that baseline.

2. The Pragmatic Alternative: "Micro-Traffic" User-Level Randomization
Geo-experiments are expensive and slow. In reality, tech companies often still use User-Level randomization for coupons, but with a strict mathematical constraint to prevent network interference.

- The Design: You randomize at the User level, but you restrict the Treatment group to a microscopic percentage of your eligible users (e.g., 1% or 0.5%).

- Why it works: If only 1% of your at-risk users receive a coupon, the incremental rides they take will be a drop in the bucket compared to the total daily ride volume. They will not consume enough supply to increase wait times or surge pricing for the 99% Control group.

- The Trade-off: You avoid interference and get to track individual 30-day retention, but you need a massive overall user base to achieve statistical significance with only a 1% treatment group.

---

### Part 2: Design the experiment

**1. Unit of randomization.**


**2. Statistical tests.**
* I would use a **z-test of proportions** for the binary success metric (30-day Retention Rate: retained vs. not retained).
* I would use a **two-sample t-test** to measure the continuous metric: average incremental revenue (Value minus Cost) per user. 
* **Standard Errors:** Because revenue variance can differ wildly between light users and power users (heteroskedasticity), using heteroskedastic robust standard errors (like Huber-White) would be appropriate to prevent artificially small p-values.

**3. Power analysis and sample size calculation.**
* I would calculate the required sample size using a standard Type I error ($\alpha$) of 0.05 and Power ($1 - \beta$) of 0.80.
* **Measuring Cost and Value (MDE):** The Minimum Detectable Effect is critical here. It is determined by the break-even point. 
  * *Cost:* The dollar amount of redeemed coupons + engineering/marketing overhead.
  * *Value:* The profit from the *incremental* rides generated. 
  * If the average coupon costs $5, and average profit per ride is $2, a user needs to take 2.5 incremental rides for us to break even. We calculate the percentage lift required to achieve that break-even revenue and set that as our MDE.

---

### Part 3: The "Gotcha" Decision

**Let’s say the result is statistically significant but not practically significant, would you ship it or not, and why?**

I would **not** ship it. 

* **Why:** Statistical significance just means we are highly confident the coupon caused *some* lift (we reject the null hypothesis). However, practical significance relates to our MDE. If our MDE was a 5% lift just to break even on the cost of the coupons, but our statistically significant result shows only a 1% lift, the experiment "worked," but the business is actively losing money on the campaign.
* In a marketplace where you are giving away actual margin via promo codes, a practically insignificant lift is a net-negative for the company's bottom line.



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
