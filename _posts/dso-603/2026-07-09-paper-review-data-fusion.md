---
layout: distill
title: "Paper review: Data Fusion for High-Resolution Estimation"
description: "A review of Guan et al. (2026) on fusing unbiased administrative data with biased survey data for high-resolution estimation."
date: 2026-07-09
categories: dso-603 causal-inference statistics
tags: data-fusion high-resolution-estimation sampling-bias
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: "The Problem: High-Resolution Estimation and Data Biases"
  - name: "The Solution: Data Fusion via KL Divergence"
bib_file: dso-603
paper_key: guan_data_2026
---


# Setting
## Unknown population quantity
- $P$: population distribution of $(X, Y, R)$. 
- $P_g, g \in \mathcal{G}$: population distribution of $(X, Y, R)$ for each state $g$.  Covairate shift assumption for subgroup: only the covariate distribution differs. Given covariate, distribution of Y is the same.
- We want to estimate: $E_{P_g}[Y]$ for any $g$.
## Known population quantity

- $P_X$: population covariate distribution. Known because we have access to Census data.
- $P_{g,X}, g \in \mathcal{G}$: covariate distribution for each state $g$. $P_X$ would be a mixture of $P_{g,X}$ for all states, where the mixing weights are the population shares of each state. 

## What we can easily estimate
- $S$: distribution of $(X, Y)$ conditioned on $R=1$. called survey distribution.
- $\mu_{S}(x) := E_{S} [Y | X = x] = E_P [Y|X = x, R= 1]$: condtional outcome for the survey population.

## Problem
We allow $R$ to be correlated to both X and Y. then niave conditional outcome approach of ijtegrating $\mu_{S}(x)$ with respect to $P_X$ fails. it is a biased esitmator of $E_{P_g}[Y]$.

Ideal case: MCAR (missing completely at random)
PP [Ri = 1 | Xi = x, Yi = y] = α0 ∀x ∈ X , y ∈ Y. (2)

Easy assumption: missing at random (MAR): similar to covariate shift assumption
PP [Ri = 1 | Xi = x, Yi = y] = α(x) ∀x ∈ X , y ∈ Y. (3)

Our assuption: (MNAR) if the probability of response can depend on the outcome, i.e. there exists a function $alpha$ : X × Y → [0, 1] such that  PP [Ri = 1 | Xi = x, Yi = y] = α(x, y) ∀x ∈ X , y ∈ Y.
equivalnetly, assuming that the probability of response depends on unobservable characteristics that are not independent from the outcome.

# From Optimization to Estimating Equations
- We cast the statistical learning problem as optimization problems.
- The learning problem is semiparametric, so the optimization involves both a finite-dimensional parameter of interest and infinite-dimensional nuisance functions. 

## A Semiparametric Optimization Problem

- The optimization problem is an example of a **semiparametric learning problem**. 
- Throughout this discussion, assume that the outcome is binary: $Y \in \{0,1\}.$
- Let $P$ denote the true population distribution over $(X,Y,R)$. This is unknown and thesamples from it are never directly observed.

### The Survey distribution $S$
- What we observe is a sample from $S$, which is generated from $P$ by conditioning on $R=1$.
- Thus $S$ is the conditional distribution of $(X,Y)$ given $R=1$.
- We index $S$ by an infinite-dimensional paramter, $\mu : \mathcal{X} \rightarrow [0,1]$, where $\mu \in L^2(P_X, \mathcal{X})$.

- The function $\mu(x)$ represents the conditional outcome of observed samples.

- Define $S(\mu)$ as the distribution over $(X,Y)$ satisfying

$$P_{S(\mu)}(Y=1 \mid X=x)=\mu(x).$$

- $\mu$ can be estimated from the observed data. Therefore it will be fixed after we estimate it. Our learning problem do not optimize over $\mu$.

### Candidate distribution $Q$
- In addtion to $\mu$, we add another parameter $\theta$ and define $Q$ based on $\mu$ and $\theta$.
- (Assumption 1, Lemma 1, and Section 3.1) Let $Q(\theta, \mu)$ denote the distribution over $(X, Y )$ where 
$$dQ_{Y|X}(\theta, \mu) \propto dS_{Y|X}(\mu) · \exp(\theta^T \eta(x, y))$$
- We can see that we are not conveniently assuming covariate shift: even conditioned on $X$, the distribution of $Y$ differs between $Q$ and $S$.
- However, we do assume that the difference in condistional distribution is in the form of exponential tilt, where
$\eta(x,y)$ is a *known* function that captures the relationship between the unobservable factors and the outcome.
- Since $\eta$ depends on $y$, it is a function of the observed covariates $X$ and the unobserved confounders $U$.
- The parameter $\theta$ controls the tilt of the distribution.

### The optimization problem
- We minimze KL divegence between candidate distribution and $S$, while sticking to the moment condition.
- To unify the expectation to be with respect to $S$, we use change of variable by introducing 
$$
r(x)
=
\frac{dP_X(x)}{dS_X(x)}.
$$
- $r$ can also be estimated from observed data and we will not optimize over $r$.
- With these definitions, the optimization problem is written as

$$
\min_{\theta \in \mathbb{R}^J}
\;
\mathbb{E}_S
\left[
r(X)\,
\mathrm{KL}\!\left(
Q_{Y|X}(\theta,\mu)
\;\|\;
S_{Y|X}(\mu)
\right)
\right]
$$

subject to

$$
\mathbb{E}_S
\left[
r(X)\,
\mathbb{E}_{Q(\theta,\mu)}
\left[
\gamma(X,Y)
\mid X
\right]
\right]
=
\bar{\gamma}_P.
$$

- The function $\gamma$ is also a known function and usually a very simple function.
- The parameter of interest is $\theta$, a finite-dimensional vector. The nuisance functions are $\mu$ and $r$.

 

# Estimating Equations
- The problem is constrained optimzation over expectation.
- The most straightforward approach for constrained optimization is to use Lagrange multipliers.

# Lagrangian
- The optimization formulation uses a  change of measure trick. 
- Notice the term $r(X) = dP_X(x)/dS_X(x)$. 
- If we multiply an expectation over the survey distribution $S$ by $r(X)$, it mathematically transforms it into an expectation over the true population distribution $P$.
- Noticing this, our opitmizaiton problem is equivlanetly:

$$\min_{\theta} \mathbb{E}_P [\text{KL}(Q_{Y\vert{}X}(\theta) \vert{}\vert{} S_{Y\vert{}X})] \quad \text{subject to} \quad \mathbb{E}_P [\mathbb{E}_{Q(\theta)}[\gamma(X,Y) \vert{} X]] = \bar{\gamma}_P$$

- we combine the objective function and the constraint into a single equation by introducing a Lagrange multiplier, $\lambda$, which penalizes the equation if the constraint is violated:

$$
\mathcal{L}(\theta, \lambda) =
\mathbb{E}_P [\text{KL}(Q_{Y\vert{}X}(\theta) \vert{}\vert{} S_{Y\vert{}X})] + \lambda^T \left( \mathbb{E}_P [\mathbb{E}_{Q(\theta)}[\gamma(X, Y) \vert{} X]] - \bar{\gamma}_P \right)
$$

- We find the stationary point where the derivatives of $\mathcal{L}$ with respect to $\theta$ and $\lambda$ are exactly zero.

## Deriving DL (equation 16)
- We take the derivative with respect to $\theta$.
- Since we can use the dominated convergence theorem, let us look at the inside of $\mathbb{E}_P$. 
### The KL Divergence Term
- By definition, $\text{KL}(Q\vert{}\vert{}S) = \mathbb{E}_Q [\log(dQ/dS)]$.
- By definition,  the ratio $dQ/dS$ is proportional to $\exp(\theta^T \eta)$. Specifically:

$$\log\left(\frac{dQ}{dS}\right) = \theta^T \eta(X,Y) - A(X, \theta)$$

- Here, $A(X, \theta)$ is the log-partition function (a normalizing constant to ensure probabilities sum to 1). 
-
- If we take the expected value of this under $Q$, we get:

$$\text{KL} = \theta^T \mathbb{E}_Q[\eta(X,Y)\vert{}X] - A(X, \theta)$$

- $A(X, \theta)$ is not affected because it is a function of $X$ and $Q$ is conditioned on $X$.
- Now, let's take the derivative of this with respect to $\theta$. Using the product rule on the first part:


$$\nabla_\theta (\text{KL}) = \mathbb{E}_Q[\eta] + (\nabla_\theta \mathbb{E}_Q[\eta]) \theta - \nabla_\theta A(X, \theta)$$

- Now it becomes evident why the paper assumes exponential tilting and sufficient statistic. **The derivative of the log-partition function is always the expected value of the sufficient statistic**. Therefore, $\nabla_\theta A(X, \theta) = \mathbb{E}_Q[\eta]$.

- Because of this, $\mathbb{E}_Q[\eta]$ and $-\nabla_\theta A(X, \theta)$ cancel each other out perfectly! We are left with:


$$\nabla_\theta (\text{KL}) = (\nabla_\theta \mathbb{E}_Q[\eta]) \theta$$

- Another property of exponential families is that **the derivative of the expectation is the covariance matrix**. Therefore, $\nabla_\theta \mathbb{E}_Q[\eta] = \text{Cov}_Q[\eta(X,Y) \vert{} X]$.
This gives us the first half of Equation 16:


$$\nabla_\theta (\text{KL}) = \text{Cov}_Q[\eta(X,Y) \vert{} X] \theta$$

### The Constraint Term
- Next, we take the derivative of the second part of the Lagrangian, $\lambda^T \mathbb{E}_Q[\gamma \vert{} X]$,  with respect to $\theta$.

- We use the chain rule for the linear part. 

- Reusing the exponential family property, the derivative of the expectation of *any* function $\gamma$ under our exponential tilt is the covariance between that function and our sufficient statistic $\eta$:


$$\nabla_\theta \mathbb{E}_Q[\gamma \vert{} X] = \text{Cov}_Q[\eta(X,Y), \gamma(X,Y) \vert{} X]$$

### Conclusion
Adding these two derivatives together and taking the outer expectation over $P$, we get the exact formula for $DL$ (Equation 16):

$$\nabla_\theta \mathcal{L} = \mathbb{E}_P \left[ \text{Cov}_{Q(\theta, \mu)} [\eta(X,Y) \vert{} X] \theta + \text{Cov}_{Q(\theta, \mu)} [\eta(X,Y), \gamma(X,Y) \vert{} X] \lambda \right] = \text{DL}(\nu; \mu)$$

---

## Deriving M

- Taking the derivative of the Lagrangian with respect to the Lagrange multiplier $\lambda$ simply strips away the $\lambda$ and returns the constraint itself.

$$\nabla_\lambda \mathcal{L} = \mathbb{E}_P [\mathbb{E}_{Q(\theta, \mu)}[\gamma(X, Y) \vert{} X]] - \bar{\gamma}_P = M(\nu; \mu)$$

This perfectly matches Equation 17.
 
# DML estimating equation

- We want to use flexible Machine Learning (ML) methods to estimate complex nuisance parameters,  such as the conditional probability of an outcome ($\mu$) or density ratios ($r$). 

- The problem is that ML methods are built for prediction, not estimation.

- To prevent overfitting and ensure generalizability, models like Random Forests or Neural Networks rely heavily on regularization. This regularization intentionally trades variance for bias. 

- While this is great for predicting a label, that inherited bias destroys our ability to perform valid statistical inference on our main target parameters.

## The form of the DML estimating equation

- To protect the target parameter $\nu$ from the mistakes made by the ML models when estimating the nuisance parameters, we must add an error-correction term.

- Let's look at a final estimating equation function $\psi$ in equation 21:

$$\psi(X, Y; \nu, \mu, r) = \begin{bmatrix} \text{DL}(\nu; \mu) + r(X) \cdot \delta_{\text{DL}}(X; \nu, \mu) \cdot (Y - \mu(X)) \\ M(\nu; \mu) + r(X) \cdot \delta_M(X; \nu, \mu) \cdot (Y - \mu(X)) \end{bmatrix}$$

- The error-correcting terms $r(X) \cdot \delta_{\text{DL}}(X; \nu, \mu) \cdot (Y - \mu(X))$ and $r(X) \cdot \delta_M(X; \nu, \mu) \cdot (Y - \mu(X))$ 
  are added to the "naive" base terms ($\text{DL}$ and $M$)

## How the Error Correcting term Works

* **Residual:** The core of the term, $(Y - \mu(X))$, is the residual, the difference between the actual outcome and the ML model's predicted outcome.
* **When Naive is perfect:** If our ML model for $\mu(X)$ is perfectly accurate, the expected value of this residual is zero. The entire correction term vanishes, leaving us with just the naive equations.
* **First-order error cancelation** If our ML model is slightly wrong, the functions $\delta_{\text{DL}}$ and $\delta_M$ kick in. These functions are  designed to ensure that the first-order errors from the ML models cancel out perfectly.

- This cancellation effect relies on a core functional property called **Neyman orthogonality**.

- If we define the true expected value of our score as $\Psi(\nu, \mu, r) = \mathbb{E}[\psi(X, Y; \nu, \mu, r)]$, we want the equation to have "reduced sensitivity" to the ML inputs.
- In calculus terms, this means that the mathematical derivative (specifically the Gateaux derivative) of $\Psi$ with respect to the nuisance parameters $\mu$ and $r$ evaluates exactly to **zero** when evaluated at the true parameter values.

* The "naive" base terms, $\text{DL}(\nu; \mu)$ and $M(\nu; \mu)$, are highly sensitive to estimation errors in $\mu$.
* The complex additive adjustments act as the orthogonalizing terms. They are specifically engineered so that their derivatives perfectly cancel out the derivatives of the naive terms.


 

# The Problem: High-Resolution Estimation and Data Biases

- Creating high-resolution estimates of population health indicators is essential for precision public health.
- However, researchers are often faced with a trade-off between two distinct types of data:
  - **Administrative data**: Unbiased but typically only available at a low resolution (e.g., state or national level).
  - **Online surveys**: Available at a high resolution (e.g., county or zip code level), but potentially subject to significant sampling bias.
- The high-resolution data often suffers from selection bias where the probability of response is influenced by unit observables. 

---

# The Solution: Data Fusion via KL Divergence

- To address this challenge, the authors propose a method to "fuse" these two data sources.
- The core idea is to learn a distribution that minimizes the Kullback-Leibler (KL) divergence to the survey distribution.
- This learned distribution must satisfy two constraints:
  1. It must remain consistent with the unbiased administrative data.
  2. It must align with the assumed sampling bias model of the survey data.
- By combining the strengths of both data sources, this approach significantly reduces bias in high-resolution estimates compared to using either data source independently.
- The authors also evaluate their proposed method on a testbed, comparing it against ground-truth data sources at different geographic resolutions to demonstrate its effectiveness.



