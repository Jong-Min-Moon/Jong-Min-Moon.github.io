---
layout: page
title: Offline Dynamic Pricing under Covariate Shift and Local Differential Privacy via Twofold Pessimism
description: We propose a DM (direct method)-type transfer learning algorithm for learning continuous treatment assignment policy from offline data under local differential privacy.
img: assets/img/pricing.png
venue: NeurIPS 2025 MLxOR Workshop
importance: 3
category: work
---

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

