---
layout: distill
title: "Paper review: Improving randomized controlled trial analysis via data-adaptive borrowing"
description: "A deep dive into how machine learning and adaptive lasso can enhance RCTs by selectively borrowing information from external controls."
date: 2026-02-20
categories: causal_inference statistics
tags: causal-inference medical-statistics adaptive-lasso machine-learning
project: causal_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Core Assumptions
  - name: The Detection Mechanism
  - name: Practical Implementation
---

## Core Assumptions

**Assumption 2 (External control compatibility).** Suppose that (i) $E\{Y(0) \mid X = x, R = 0\} = E\{Y (0) \mid X = x, R = 1\}$ and...

## The Detection Mechanism

The adaptive lasso penalty detects incomparable external controls by recasting the challenge of identifying compatible subjects as a model selection problem based on individual bias. Here is how the detection mechanism works:

*   **Defining the Bias Parameter:** For each external control subject, a specific bias parameter ($b_{i,0}$) is introduced. This parameter measures the difference in the expected outcome between the external control subject and a concurrent trial control subject, given their baseline covariates. An external subject is considered comparable if their bias is exactly zero ($b_{i,0} = 0$) and incomparable if it is non-zero.
*   **Initial Estimation:** The framework first uses machine learning models to calculate an initial, consistent estimate of this bias ($\hat{b}_{i}$) for every single external subject.
*   **Applying the Penalty:** A refined bias estimator ($\tilde{b}$) is then computed using penalized estimation. The adaptive lasso penalty term applied to each subject is proportional to $|b_{i}| / |\hat{b}_{i}|^{\nu}$.
*   **The Shrinkage Mechanism:** Because the initial bias estimate ($\hat{b}_{i}$) acts as the denominator in the penalty term, it dictates the severity of the penalty. If an external subject is truly comparable, their initial bias estimate will be close to zero, which forces the associated penalty to become exceedingly large. This massive penalty shrinks the subject's final, refined bias estimate ($\tilde{b}_{i}$) exactly to zero.
*   **Selective Borrowing:** Once the penalized estimation is complete, the framework looks at the refined bias estimates. Any external subject whose refined bias is exactly zero ($\tilde{b}_{i} = 0$) is grouped into a comparable subset ($\tilde{\mathcal{A}}$) and retained for the trial analysis, while anyone with a non-zero bias is permanently excluded.

By using this penalty, the framework achieves "selection consistency" (Lemma 1). This means that as long as the initial estimator is high quality and the tuning parameters are chosen properly, the adaptive lasso will consistently and reliably pinpoint the zero-bias subjects, naturally filtering out incomparable external controls that could otherwise skew the trial's results.

## Practical Implementation

To learn the exact value of the bias parameter for each external control subject, the framework uses a two-step process involving machine learning predictions followed by a penalized optimization:

1.  **Defining the True Bias:** The true subject-level bias, $b_{i,0}$, is defined mathematically as the difference between the expected conditional outcome for an external control subject ($\mu_{0,E}(X_{i})$) and a concurrent trial control subject ($\mu_{0}(X_{i})$), which is expressed as $b_{i,0} = \mu_{0,E}(X_{i}) - \mu_{0}(X_{i})$.
2.  **Calculating an Initial Estimate:** An initial, unpenalized estimator, $\hat{b}_{i}$, is constructed by calculating the difference between the estimated outcome means for both groups: $\hat{b}_{i} = \hat{\mu}_{0,E}(X_{i}) - \hat{\mu}_{0}(X_{i})$. In practice, these conditional outcome means ($\hat{\mu}_{0,E}$ and $\hat{\mu}_{0}$) are estimated using off-the-shelf machine learning algorithms that possess guaranteed convergence rates.
3.  **Applying the Adaptive Lasso Penalty:** Finally, a refined bias estimator, $\tilde{b}$, is computed by solving a penalized least-squares optimization problem. The framework finds the vector of biases $b$ that minimizes the following equation:

$$
\tilde{b} = \text{argmin}_{b} \{ (\hat{b}-b)^{T} \hat{\Sigma}_{b}^{-1} (\hat{b}-b) + \lambda_{N} \sum_{i \in E} p(|b_{i}|) \}
$$

### Breaking down the components:

*   $\hat{\Sigma}_{b}$ is the estimated variance of the initial bias estimator $\hat{b}$.
*   $p(|b_{i}|)$ is the adaptive lasso penalty term applied to each subject, which is defined as $|b_{i}| / |\hat{b}_{i}|^{\nu}$.
*   $\lambda_{N}$ and $\nu$ are two tuning parameters that dictate the strength of the penalty; they are selected by minimizing the mean square error using cross-validation.

Because the initial estimate $\hat{b}_{i}$ acts as the denominator in the penalty term $p(|b_{i}|)$, subjects who are truly comparable (and thus have an initial bias estimate close to zero) will receive an exceedingly large penalty. This dynamic successfully shrinks their final refined bias estimate ($\tilde{b}_{i}$) to exactly zero, allowing the framework to pinpoint and select them for the trial.

cenrla limit diffusion


fluid market sie lambda t

precious setting: lambda and n together goes to infinty
static price approach (dynamic pricing is not need in seminal dynamic rpciing paper) uses CLT
iterative reoptimization heuristic
the core logic is even though we use CLT, we dont need large number actually

this talk focuses on large market regime
core: same CLT small number argument

the core message: what matter is the ratio. not which one is fixed


plot: the optial policy in large market regime is not the static policy (high price w