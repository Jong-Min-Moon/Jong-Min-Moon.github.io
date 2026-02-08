---
layout: project
title: Causal inference of sex differences in autism spectrum disorder
description: Stabilizing heterogeneous treatment effect estimation for high-dimensional outcomes in high-imbalance regimes
img: assets/img/publication_preview/neuroimage_wide.png
venue: NeuroImage
importance: 2
category: work
project_handle: autism-sex-differences
---

This project addresses the statistical challenge of estimating heterogeneous treatment effects (HTEs) in Autism Spectrum Disorder (ASD), where female participants are significantly underrepresented using class imbalance adjusted functional connectivity. By employing a cluster-aware generative model for oversampling, we improve the stability of estimates for the female subgroup.

Our findings reveal significant sex-specific functional connectivity patterns associated with higher-order cognitive control functions, highlighting the importance of proper statistical handling of imbalanced biomedical data.



---

### 1. Motivation: The Causal Estimand
The primary objective of this study was to estimate the **Heterogeneous Treatment Effect (HTE)** of Autism Spectrum Disorder (ASD) conditional on biological sex.

Let $T$ denote the treatment (diagnosis: ASD=1, Control=0), $X$ denote the covariate (Sex: Male/Female), and $Y$ denote the outcome (Functional Gradient Score, a low-dimensional embedding of brain connectivity). Even after dimensionality reduction, we have several region of interst, so we can consider $Y$ as a high-dimensional outcome.

The target estimand is the **Interaction Effect**, defined as:

$$
\tau_{interaction} = \underbrace{(E[Y|T=1, X=F] - E[Y|T=0, X=F])}_{\text{Causal Effect in Females}} - \underbrace{(E[Y|T=1, X=M] - E[Y|T=0, X=M])}_{\text{Causal Effect in Males}}
$$

We hypothesized that the treatment effect of ASD on functional brain organization differs significantly between sexes.

---

### 2. The Identification Challenge: Practical Positivity Violation
While the theoretical assumption of **Positivity** ($0 < P(T=1|X) < 1$) holds, the study faces a severe **class imbalance** problem common in observational ASD research.
* **The Imbalance:** The prevalence of ASD is significantly higher in males, with ratios ranging from 4:1 to 9:1.
* **The Consequence:** The Female/ASD stratum is extremely sparse, representing approximately 12% of the total sample in this dataset.

In a finite sample regime, this sparsity compromises the estimation of the conditional expectation $E[Y|T=1, X=F]$. Standard non-parametric estimators like **Inverse Probability Weighting (IPW)** might  assign extreme weights to the few observed female cases, pontentially containing outliers. This would inflate the variance of the estimator, rendering confidence intervals too wide to detect significant interaction effects.

---

### 3. Methodological Contribution: Parametric Variance Reduction
To address the bias-variance trade-off inherent in the sparse stratum, the authors proposed a **Gaussian Mixture Model (GMM)-based Oversampling** technique[cite: 24, 64].

#### A. The Estimator
Instead of re-weighting existing data points (as in IPW), the authors constructed a synthetic pseudo-population to balance the strata ($N_{female} \rightarrow N_{male}$).

1.  **Distribution Estimation:** The probability density function of the sparse class, $f(Y|X=F)$, was estimated using a parametric GMM[cite: 110, 111]:
    $$
    f(x) = \sum_{j=1}^{J} \pi_j \psi(x | \mu_j, \sigma_j^2)
    $$
    where $\psi$ represents Gaussian density components and parameters are optimized via the Expectation-Maximization (EM) algorithm.
2.  **Generative Oversampling:** Synthetic observations $\hat{Y}$ were drawn from the estimated density $f(x)$ until the sample sizes were balanced.

#### B. Statistical Justification (vs. Undersampling/IPW)
From a causal inference perspective, this method acts as a variance stabilization technique:
* **Undersampling:** Standard approaches often undersample the majority class (males), which introduces additional randomness and discards information.
* **GMM Oversampling:** By injecting a smoothness assumption (that brain gradients follow a mixture of Gaussians), the method effectively "fills in the gaps" of the sparse female data space.
* **Asymptotic Validity:** The authors argue that because GMMs are universal approximators for smooth densities, the expanded dataset converges to the true distribution in the asymptotic regime, allowing for valid Type I error control despite the added randomness of synthesis.

---

### 4. Assessing Validity: Parametric Assumptions
To claim the estimand is identifiable and the parametric assumption valid, the study employed the following validation steps:

* **Consistency & Exchangeability:** The study implicitly assumes conditional exchangeability by controlling for **Age** and **Site** during the oversampling process.
* **Parametric Fit Validation (Wasserstein Distance):** To justify replacing the empirical distribution with the GMM approximation, the authors calculated the **Wasserstein Distance** between the histograms of the *actual* female gradients and the *synthetic* gradients.
    * **Result:** The distance was consistently low, providing empirical evidence that the functional gradients are well-approximated by the Gaussian mixture, thus minimizing the bias introduced by the parametric assumption.

---

### 5. Results: Uncovering Hidden Heterogeneity
By stabilizing the estimator variance, the study detected significant Heterogeneous Treatment Effects that were previously obscured by the noise of the imbalanced data.

* **Finding:** Significant interaction effects were identified in the **Somatomotor** ($P_{FDR}=0.029$), **Dorsal Attention** ($P_{FDR}=0.029$), and **Default Mode Networks (DMN)** ($P_{FDR}<0.001$).
* **Direction of Effect:** Female participants with ASD showed large shifts in gradient values (reduced values in DMN), whereas male participants showed smaller or opposite shifts.
* **Conclusion:** The oversampling approach increased statistical power, revealing that female susceptibility to ASD involves distinct alterations in higher-order cognitive control networks.