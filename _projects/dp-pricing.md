---
layout: page
title: Offline Dynamic Pricing under Covariate Shift and Local Differential Privacy via Twofold Pessimism
description: We propose a DM (direct method)-type transfer learning algorithm for learning continuous treatment assignment policy from offline data under local differential privacy.
img: assets/img/pricing.png
venue: NeurIPS 2025 MLxOR Workshop
importance: 5
category: [differential privacy, nonparametric statistics, causal inference, reinforcement learning/bandits]
related_publications: munOfflineDynamicPricing2025
---

# Personalized (implicit) pricing
- Explicit dynamic pricing faces public backlash.
- Still, dynamic pricing is widely used in practice by firm in implicit form
- A good example ad-supported subscription services such as Netflix and YouTube. Although these platforms typically offer only two plan types (free and paid), free users may receive a personalized level of advertising exposure, which can vary continuously. LLM tokens can be another example.
- Consumers seem to be accepting this type of implicit dynamic pricing.
- Therefore learning a good dynamic pricing policy from customer features is still an important problem.

# Introduction
- Just as patients exhibit heterogeneous responses to medical treatments, consumers show highly heterogeneous responses to prices. 
-  Understanding and leveraging this individualized response is the fundamental goal of dynamic pricing.
-  We consider the problem of learning personalized pricing policies by analyzing historical observational data to map customer features to optimal price points. 

# Dangers of Policy Learning from Historical Data

## Market Shift
- A pricing algorithm naturally achieves higher precision for customer profiles that are abundant in the historical dataset, as it has more observations to accurately estimate their conditional outcomes.
  
- However, when the market environment changes, such as when a firm enters a new geographic region or experiences demographic shifts, the feature distribution of the target market diverges from the historical data. A customer profile that was common in the historical data may become rare in the target market. 
  
- Consequently, a policy trained on the historical data will not perform as effectively in the new market.

- First, we quantify how shifts in the consumer base affect learning accuracy.   We formalize this covariate shift and rigorously quantify how the degree of mismatch between the source and target distributions degrades policy accuracy, thereby establishing the true sample size required to maintain performance under market evolution.

- We ask a foundational question: What are the fundamental limits of learning from historical pricing data, and how many samples are required to guarantee a specific level of accuracy in a dynamic environment?To answer this, we must formally quantify the impact of the core operational constraints that define real-world dynamic pricing. We focus on characterizing the sample complexity required to learn an optimal policy when faced with two primary challenges: market shift and limited historical exploration.Quantifying the Necessity of Historical ExplorationSecond, we quantify the minimum degree of historical price variation needed to learn an effective policy. To identify a profit-maximizing price, the historical data must contain enough variability to allow the algorithm to compare counterfactual outcomes. In practice, however, explicit pricing experimentation is prohibitively expensive and risky, resulting in historical datasets with notoriously narrow price exploration.Previous literature has typically accounted for this by imposing a strict, global overlap assumption: for any given customer, the historical logging policy must have explored every possible price interval of length $r$ with at least some probability $\zeta$. We relax this restrictive assumption and demonstrate a tighter, more realistic dependency. We prove that the accuracy of the learned policy—and the resulting sample complexity—does not depend on exploring the entire price range. Instead, it depends exclusively on the coverage of the optimal price. Specifically, we show that successful policy learning is bounded only by the proportion of historical transactions that fall within a narrow interval centered at the true optimal price for a given customer.By analyzing these phenomena—while also accounting for the noise introduced by modern Local Differential Privacy (LDP) constraints—we establish a unified theoretical framework. This framework not only yields a minimax-optimal policy learning algorithm but provides a precise mathematical characterization of the data requirements necessary for successful personalized dynamic pricing.

# propnseity assumption
Assumption 4.


We study pricing policy learning from batched contextual bandit data under market
shift and privacy protection. Market shift is modeled as covariate shift, where
the relationship among treatments, features, and rewards remains invariant, while
privacy is enforced through local differential privacy (LDP), which perturbs each
data point before use. Viewing the off-policy setting, covariate shift, and LDP
collectively as forms of distributional shift, we develop a policy learning algorithm
based on a unified pessimism principle that addresses all three shifts. Without
privacy, we estimate the conditional reward via nonparametric regression and
quantify its variance to construct a pessimistic estimator, yielding a policy with
minimax-optimal decision error. Under LDP, we apply the Laplace mechanism and
adjust the pessimistic estimator to account for additional uncertainty from privacy
noise. The resulting doubly pessimistic objective is then optimized to determine
the final pricing policy.

This work was presented at NeurIPS 2025 MLxOR workshop. You can also check out the full paper [here](https://openreview.net/pdf?id=ZL748l6oQG).

