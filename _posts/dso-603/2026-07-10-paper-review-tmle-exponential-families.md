---
layout: distill
title: "Paper review: Targeted Maximum Likelihood Estimation Using Exponential Families"
description: "A review of Díaz and Rosenblum (2015) on constructing fluctuation submodels via exponential families for targeted maximum likelihood estimation."
date: 2026-07-10
categories: dso-603 causal-inference statistics tmle
tags: targeted-learning exponential-families tmle semiparametric-inference double-robustness
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Introduction & Motivation
  - name: Semiparametric Framework & Efficient Influence Curves
  - name: Fluctuation Submodels via Exponential Families
  - name: The Targeted Estimation Algorithm
  - name: Applications & Key Takeaways
bib_file: dso-603
paper_key: diaz_targeted_2015
---

# Why TMLE?

### The Breakdown of Simple Estimators Under Missing Data
- Estimating a simple parameter, like the marginal mean of an outcome $Y$, is trivial under perfect observation.
- The sample mean is unbiased, and by the Central Limit Theorem (CLT), it is asymptotically normal, allowing for straightforward confidence intervals. 
- However, in causal inference and missing data problems, the data-generating process complicates this reality.
- When $Y$ is only partially observed and the missingness ($M$) depends on side information $X$, the simple sample mean is no longer an unbiased estimator.

### The MAR Assumption and High Dimensionality

- To proceed, we must account for the missingness mechanism by conditioning on the covariates $X$.
- The standard requirement is the Missing At Random (MAR) assumption, which states that conditional on $X$, the missingness indicator $M$ is independent of $Y$:
<p>
\begin{equation}
P(M = m \mid X, Y) = P(M = m \mid X)
\end{equation}
</p>

- Under MAR, the marginal mean of $Y$ can be identified via standard standardization (G-computation):
    1. Estimate the conditional outcome regression $\mu(X) = E(Y \mid M = 1, X)$.
    2. Integrate this conditional expectation over the marginal distribution of $X$.
- The practical hurdle is that for the MAR assumption to be scientifically plausible in observational data, $X$ must capture all relevant confounders, making it inherently high-dimensional.

### The Flaw in Plug-in ML Estimators
- High-dimensional regression requires sophisticated machine learning algorithms (e.g., Lasso, random forests, neural networks) to avoid overfitting. 
- However, these algorithms achieve predictive power through regularization, which deliberately trades variance for bias to minimize overall Mean Squared Error (MSE).
- Consequently, these machine learning estimators converge at a rate slower than $n^{-1/2}$. 
- If we simply plug these biased predictions into our integration step, the regularization bias propagates directly to our final estimate of the mean. 
- This destroys $\sqrt{n}$-consistency (asymptotic unbiasedness) and renders our standard confidence intervals completely invalid.

### The TMLE Correction
- Targeted Maximum Likelihood Estimation (TMLE) resolves this by explicitly correcting the bias of the initial ML regression.
- TMLE uses a targeted update step that fluctuates the initial, biased outcome estimates using a "clever covariate".
- This targeting step forces the final estimate to solve the efficient influence function (EIF) estimating equation.
- By doing so, TMLE provides two critical statistical guarantees for the target parameter:
    1. **Double Robustness:** The final estimate remains consistent if either the outcome regression model *or* the propensity score model is correctly specified.
    2. **Asymptotic Efficiency & Normality:** By shrinking the regularized bias fast enough, the estimator achieves $\sqrt{n}$-consistency. This ensures that the Central Limit Theorem holds, allowing for valid statistical inference even when utilizing complex, black-box machine learning algorithms under the hood.


---

# Semiparametric Framework & Efficient Influence Curves

## Data Generating Process & Target Parameter
Consider observing $n$ independent and identically distributed (i.i.d.) random vectors $O_1, \dots, O_n$ sampled from an unknown true distribution $P_0 \in \mathcal{M}$, where $\mathcal{M}$ represents a non-parametric or semiparametric statistical model. Typically, the observed data vector is decomposed into baseline covariates, exposure/treatment, and outcome:
<p>$$O = (W, A, Y) \sim P_0$$</p>

We are interested in estimating a finite-dimensional parameter $\theta_0 = \Psi(P_0) \in \mathbb{R}^k$, where $\Psi: \mathcal{M} \to \mathbb{R}^k$ is a pathwise differentiable target mapping (e.g., the average treatment effect $\mathbb{E}[Y(1) - Y(0)]$ or missing outcome mean $\mathbb{E}[Y]$).

## Pathwise Differentiability and the Canonical Gradient
Standard semiparametric efficiency theory dictates that any regular, pathwise differentiable parameter $\Psi$ possesses a unique **canonical gradient** (or **efficient influence curve**, EIC), denoted by $D^*(O; P) \in L_2^0(P)$. 

For any smooth parametric submodel $\{P_\epsilon : \epsilon \in \mathbb{R}^k\} \subset \mathcal{M}$ passing through $P$ at $\epsilon = 0$ with score $\mathbf{S}(O) = \left. \frac{\partial}{\partial \epsilon} \log dP_\epsilon(O) \right|_{\epsilon=0}$, pathwise differentiability implies:
<p>$$\left. \frac{d}{d\epsilon} \Psi(P_\epsilon) \right|_{\epsilon=0} = \mathbb{E}_P \left[ D^*(O; P) \mathbf{S}(O)^T \right]$$</p>

An estimator $\hat{\theta}_n$ is **asymptotically efficient** at $P_0$ if it is asymptotically linear with influence function equal to $D^*(O; P_0)$:
<p>$$\sqrt{n}(\hat{\theta}_n - \theta_0) = \frac{1}{\sqrt{n}} \sum_{i=1}^n D^*(O_i; P_0) + o_p(1) \quad \xrightarrow{d} \quad \mathcal{N}\left(0, \operatorname{Var}_{P_0}(D^*(O; P_0))\right)$$</p>

To achieve efficiency via substitution, a TMLE updated distribution $\hat{P}^*$ must solve the empirical score equation:
<p>$$\mathbb{E}_{P_n} \left[ D^*(O; \hat{P}^*) \right] = \frac{1}{n} \sum_{i=1}^n D^*(O_i; \hat{P}^*) = o_p(n^{-1/2})$$</p>

---

# Fluctuation Submodels via Exponential Families

## The General Exponential Family Submodel
Let $p^0(y \mid a, w)$ denote an initial conditional density estimate of $Y$ given $(A,W)$, typically obtained via flexible machine learning algorithms (e.g., Super Learner, Random Forests, or Neural Networks). 

Instead of adding a standard clever covariate $H(A,W)$ to a link function, {% cite diaz_targeted_2015 %} introduce a parametric fluctuation submodel $\{p(\epsilon) : \epsilon \in \mathbb{R}^k\}$ defined as a canonical exponential family tilted away from the initial density $p^0$:

<p>$$p(\epsilon)(y \mid a, w) = p^0(y \mid a, w) \exp\left( \epsilon^T T(y, a, w) - A(\epsilon; a, w) \right)$$</p>

where:
* $T(y, a, w) \in \mathbb{R}^k$ is a vector of **sufficient statistics** chosen based on the target parameter's efficient influence curve.
* $A(\epsilon; a, w)$ is the **log-partition function** (normalizing constant), defined by:
<p>$$A(\epsilon; a, w) = \log \int \exp\left( \epsilon^T T(y, a, w) \right) p^0(y \mid a, w) \, dy$$</p>

## Score Derivation & Matching the Canonical Gradient
Taking the derivative of the log-density of $p(\epsilon)$ with respect to the fluctuation parameter $\epsilon$:
<p>$$\nabla_\epsilon \log p(\epsilon)(y \mid a, w) = T(y, a, w) - \nabla_\epsilon A(\epsilon; a, w)$$</p>

Using classic exponential family identities, the gradient of the log-partition function equals the conditional expectation of the sufficient statistic under $p(\epsilon)$:
<p>$$\nabla_\epsilon A(\epsilon; a, w) = \mathbb{E}_{p(\epsilon)} \left[ T(Y, a, w) \mid A=a, W=w \right]$$</p>

Evaluating the score at $\epsilon = 0$ yields:
<p>$$\left. \nabla_\epsilon \log p(\epsilon)(y \mid a, w) \right|_{\epsilon=0} = T(y, a, w) - \mathbb{E}_{p^0} \left[ T(Y, a, w) \mid A=a, W=w \right]$$</p>

### Key Insight
To ensure that the fluctuation path spans the required component of the efficient influence curve $D^*(O; P)$, the sufficient statistic $T(y, a, w)$ is explicitly constructed so that its centered expectation matches the score component of $D^*$.

For example, when estimating a conditional mean parameter where the EIC takes the form $D^*(O; P) = H(A,W) \left( Y - \mathbb{E}_P[Y \mid A,W] \right)$, setting $T(y, a, w) = H(a, w) y$ gives:
<p>$$\left. \nabla_\epsilon \log p(\epsilon)(y \mid a, w) \right|_{\epsilon=0} = H(a, w) \left( y - \mathbb{E}_{p^0}[Y \mid A=a, W=w] \right) = D^*(O; P^0)$$</p>

---

# The Targeted Estimation Algorithm

The algorithm proceeds iteratively using maximum likelihood estimation over the fluctuation parameter $\epsilon$, guaranteeing computational efficiency through strict log-likelihood concavity.

```
       +-------------------------------------------------------+
       | 1. Initial ML Estimation                              |
       |    - Estimate p^0(Y|A,W) via Super Learner            |
       |    - Estimate nuisance mechanism g^0(A|W)             |
       +-------------------------------------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       | 2. Exponential Family Submodel Construction           |
       |    - Define canonical gradient D*(O; p^k, g^0)        |
       |    - Set sufficient statistic T_k(y,a,w)              |
       |    - Form p^k(\epsilon) \propto p^k exp(\epsilon^T T) |
       +-------------------------------------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       | 3. Convex Maximum Likelihood Update                   |
       |    - Solve \hat{\epsilon}_k = argmax \sum log p^k(\epsilon)|
       |    - Update p^{k+1} = p^k(\hat{\epsilon}_k)           |
       +-------------------------------------------------------+
                                   |
                         Is ||\hat{\epsilon}_k|| < tol?
                         /                           \
                       No                             Yes
                       /                               \
                      v                                 v
       [ Repeat Step 2 & 3 ]                 +-------------------------+
                                             | 4. Plug-in Estimation   |
                                             |    \hat{\theta} = \Psi  |
                                             +-------------------------+
```

## Step-by-Step Procedure

1. **Initial Nuisance Estimation**:
   * Estimate the conditional distribution $p^0(y \mid a, w)$ and propensity/missingness mechanism $g^0(a \mid w)$ using machine learning.
2. **Construct Exponential Family Fluctuation**:
   * Compute the clever covariate / sufficient statistic $T_k(y,a,w)$ from the EIC at iteration $k$.
   * Define the submodel $p^k(\epsilon)(y \mid a, w) \propto p^k(y \mid a, w) \exp(\epsilon^T T_k(y,a,w))$.
3. **Convex Optimization Update**:
   * Fit $\hat{\epsilon}_k$ by maximizing the empirical log-likelihood:
   <p>$$\hat{\epsilon}_k = \arg\max_{\epsilon \in \mathbb{R}^k} \frac{1}{n} \sum_{i=1}^n \log p^k(\epsilon)(Y_i \mid A_i, W_i)$$</p>
   * Update the density: $p^{k+1}(y \mid a, w) = p^k(\hat{\epsilon}_k)(y \mid a, w)$.
4. **Convergence Check & Plug-in Evaluation**:
   * Iterate steps 2 and 3 until $\|\hat{\epsilon}_k\| < \tau$ (or $\frac{1}{n}\sum_{i=1}^n D^*(O_i; p^k, g^0) \approx 0$).
   * Evaluate the target parameter by plug-in substitution: $\hat{\theta}_{\text{TMLE}} = \Psi(P^*(\hat{\epsilon}))$.

## Theoretical Advantages of Exponential Family TMLE

1. **Guaranteed Convexity**: Log-likelihood optimization over canonical exponential family parameters $\epsilon$ is strictly concave. This eliminates sensitivity to starting values and guarantees rapid convergence via Newton-Raphson or GLM algorithms.
2. **Double Robustness**: Like standard TMLE, the resulting estimator is doubly robust—consistent if either the outcome conditional density $p^0(y \mid a,w)$ or the exposure mechanism $g^0(a \mid w)$ is correctly specified.
3. **Generalization Beyond Binary Outcomes**: Natural application to continuous, count, or survival outcomes without requiring heuristic transformations or bounded unit interval projections.

---

# Applications & Key Takeaways

{% cite diaz_targeted_2015 %} demonstrate the exponential family TMLE framework across three key problem domains:

| Problem Domain | Challenge in Standard TMLE | Exponential Family Solution |
| :--- | :--- | :--- |
| **Missing Outcome Mean** | Non-standard outcome bounds | Canonical exponential tilting directly adjusts the conditional density $p(y \mid w)$. |
| **Median Regression** | Non-differentiable indicator objective | Exponential family submodel creates a smooth fluctuation path spanning the non-smooth EIC. |
| **Continuous Exposure** | Infinite-dimensional nuisance functions | Multi-dimensional exponential family submodels handle kernel-smoothed density fluctuations seamlessly. |

## Summary

The exponential family approach introduced by {% cite diaz_targeted_2015 %} unifies targeted maximum likelihood estimation by replacing ad-hoc clever covariates with a principled, convex exponential tilting mechanism. This framework provides robust theoretical guarantees, numerical stability, and seamless scalability for complex causal parameters in modern data science and semiparametric inference.
