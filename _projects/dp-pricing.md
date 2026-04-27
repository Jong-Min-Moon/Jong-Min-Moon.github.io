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

This work was presented at NeurIPS 2025 MLxOR workshop. You can also check out the full paper [here](https://openreview.net/pdf?id=ZL748l6oQG).


# Introduction
- Just as patients exhibit heterogeneous responses to medical treatments, consumers show highly heterogeneous responses to prices. 
-  Understanding and leveraging this individualized response is the fundamental goal of dynamic pricing.
-  We consider the problem of learning personalized pricing policies by analyzing historical observational data to map customer features to optimal price points.

## Practical impliation
- Explicit dynamic pricing faces public backlash.
- Still, dynamic pricing is widely used in practice by firm in implicit form
- A good example ad-supported subscription services such as Netflix and YouTube. Although these platforms typically offer only two plan types (free and paid), free users may receive a personalized level of advertising exposure, which can vary continuously. LLM tokens can be another example.
- Consumers seem to be accepting this type of implicit dynamic pricing.
- Therefore learning a good dynamic pricing policy from customer features is still an important problem.

# Dangers of Policy Learning from Historical Data

## Market Shift on customer profiles
- A pricing algorithm naturally achieves higher precision for customer profiles that are abundant in the historical dataset, as it has more observations to accurately estimate their conditional outcomes.
  
- However, when the market environment changes, such as when a firm enters a new geographic region or experiences demographic shifts, the feature distribution of the target market diverges from the historical data. A customer profile that was common in the historical data may become rare in the target market. 
  
- Consequently, a policy trained on the historical data will not perform as effectively in the new market.

- First, we quantify how shifts in the consumer base affect learning accuracy.   

## Under-exploration on price
- Even if the market does not shift, since we are not actively collecting data but relying on historical observational data, there is always risk of underexploration.
- To identify a profit-maximizing price for each customer ($\mathbf{x}$), the historical data must contain enough variability in price ($p$) to allow the algorithm to compare counterfactual outcomes.
- In practice, however, explicit pricing experimentation is prohibitively expensive and risky, and transactions are based on reasonable prices that followed some resonable policy, resulting in historical datasets with narrow price exploration.

## Remedy: More Data, with Privacy
- One way to handle the two problems above is to collect more data: more data with wider price exploration and diverse customer profiles.
- Since we are not actively collecting data but relying on historical observational data, one way to collect more data is collaborations with other firms, sharing each other's data.
- Data sharing raises privacy concerns. In adtech industry, firms created a secure environment called data clean room, where firms can share their privacy-protected data and run the analysis. 
- Privacy protection is basically adding noise to the data or the analysis result. The amount of noise and the level of privacy is formalized by the notion called differential privacy.
- However, adding noise will hurt the accuracy of the data. This is the trade-off of privacy protection. 

# Goal of this paper: quantifying the trade-offs
- So, privacy protection can allevaiate market shift and under-exploration. But its noise injection hurts the accuracy of the data. 
- So, we want to quantify the effect of these three factors to the performance of the pricing policy learning. 
- To this end we first need to formalize and quantify the three factors

## Market Shift: transfer exponent
- Let $P$ and $Q$ denote the distributions of customer features in the historical and target markets, respectively.
- We quantify this market shift using the transfer exponent, a standard concept in the transfer learning literature.
- Intuitively, for any customer segment of size $h \in (0,1)$, the transfer exponent $\alpha$ bounds the ratio between its proportion in historical and target markets by $h^\alpha$.
- A smaller $\alpha$ indicates stronger structural alignment between the markets.
- The bound naturally relaxes as segments become increasingly niche ($h \to 0$).

## Price exploration: exploretion coefficient
- To quantify the quality of the logged data, we introduce a parameter $\zeta \in [0, 1]$ that captures the propensity of the past pricing algorithm to   select near-optimal prices.
- Intuitively, this ensures that $P(T \approx t^\dagger \mid \mathbf{X}^P \approx \mathbf{x}) \ge \zeta$ for every context $\mathbf{x}$, where $t^\dagger$ denotes an optimal price (allowing for the possibility of multiple optima).


## Privacy Protection: noise variance
- Local differntial privacy formalizes the notion of datapoint level privacy. Most of the time, local differential privacy is satisfied by adding iid noise to each datapoint. 
- Intuitively, the privacy level corresponds to the inverse of the noise variance added to each datapoint.
 
# Analysis  without privacy
## Unavoidable limit of any policy
We first demonstrate that for any policy $\pi$, its optimality gap relative to the optimal policy $\pi^\ast$—measured by expected profit in the target market—is lower bounded as:
<p>
	\begin{equation}\label{regret_lower_bound}
		V({\pi^\ast}) - V(\pi) \gtrsim (\zeta n)^{-\frac{\beta }{2\beta+\alpha+d+1}},
	\end{equation}
</p>
where $\beta$ represents the smoothness of the conditional outcome.


## Reaching the limit by a policy learning algorithm
- We demonstrate that a policy learning algorithm based on the principle of pessimism achieves this theoretical lower bound.

- The algorithm utilizes a local average estimator to predict the conditional expected outcome.

- This estimator allows us to compute rigorous confidence intervals for the outcome associated with any specific customer profile and price.

- Rather than optimizing the point estimate of the outcome, the algorithm selects the price that maximizes the lower confidence bound (LCB).

- Through this pessimistic optimization, uncertainty stemming from  lack of datapoints with respect to customer profile and price is naturally incorporated into the learning process.

- The policy learned via this algorithm achieves a regret bound that matches the lower bound up to a constant factor, proving that the lower bound is tight and rigorously quantifies the fundamental limits of the problem.

# Analysis under privacy protection
- Working on this. The core is finding the confidence interval under noise injection. The pessimism is applied twice: once for the statistical uncertainty and once for the privacy-induced uncertainty.


 


