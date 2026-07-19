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
  - name: Setting
  - name: From Optimization to Estimating Equations
  - name: One-step Estimator
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

 

## Naive Estimating Equations
- The problem is constrained optimzation over expectation.
- The most straightforward approach for constrained optimization is to use Lagrange multipliers.

### Lagrangian
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

#### Deriving DL (equation 16)
- We take the derivative with respect to $\theta$.
- Since we can use the dominated convergence theorem, let us look at the inside of $\mathbb{E}_P$. 
##### The KL Divergence Term
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

##### The Constraint Term
- Next, we take the derivative of the second part of the Lagrangian, $\lambda^T \mathbb{E}_Q[\gamma \vert{} X]$,  with respect to $\theta$.

- We use the chain rule for the linear part. 

- Reusing the exponential family property, the derivative of the expectation of *any* function $\gamma$ under our exponential tilt is the covariance between that function and our sufficient statistic $\eta$:


$$\nabla_\theta \mathbb{E}_Q[\gamma \vert{} X] = \text{Cov}_Q[\eta(X,Y), \gamma(X,Y) \vert{} X]$$

##### Conclusion
Adding these two derivatives together and taking the outer expectation over $P$, we get the exact formula for $DL$ (Equation 16):

$$\nabla_\theta \mathcal{L} = \mathbb{E}_P \left[ \text{Cov}_{Q(\theta, \mu)} [\eta(X,Y) \vert{} X] \theta + \text{Cov}_{Q(\theta, \mu)} [\eta(X,Y), \gamma(X,Y) \vert{} X] \lambda \right] = \text{DL}(\nu; \mu)$$

---

#### Deriving M

- Taking the derivative of the Lagrangian with respect to the Lagrange multiplier $\lambda$ simply strips away the $\lambda$ and returns the constraint itself.

$$\nabla_\lambda \mathcal{L} = \mathbb{E}_P [\mathbb{E}_{Q(\theta, \mu)}[\gamma(X, Y) \vert{} X]] - \bar{\gamma}_P = M(\nu; \mu)$$

This perfectly matches Equation 17.
 
## DML estimating equation

- We want to use flexible Machine Learning (ML) methods to estimate complex nuisance parameters,  such as the conditional probability of an outcome ($\mu$) or density ratios ($r$). 

- The problem is that ML methods are built for prediction, not estimation.

- To prevent overfitting and ensure generalizability, models like Random Forests or Neural Networks rely heavily on regularization. This regularization intentionally trades variance for bias. 

- While this is great for predicting a label, that inherited bias destroys our ability to perform valid statistical inference on our main target parameters.

### The form of the DML estimating equation

- To protect the target parameter $\nu$ from the mistakes made by the ML models when estimating the nuisance parameters, we must add an error-correction term.

- The final population estimating equations are given by $\Psi(\nu; \mu, r) = E_{\mathcal{S}} [\psi(X, Y ; \nu, \mu, r)]$, where $\psi$ is defined as

$$\psi(X, Y; \nu, \mu, r) = \begin{bmatrix} \text{DL}(\nu; \mu) + r(X) \cdot \delta_{\text{DL}}(X; \nu, \mu) \cdot (Y - \mu(X)) \\ M(\nu; \mu) + r(X) \cdot \delta_M(X; \nu, \mu) \cdot (Y - \mu(X)) \end{bmatrix}$$

- The error-correcting terms $r(X) \cdot \delta_{\text{DL}}(X; \nu, \mu) \cdot (Y - \mu(X))$ and $r(X) \cdot \delta_M(X; \nu, \mu) \cdot (Y - \mu(X))$ 
  are added to the "naive" base terms ($\text{DL}$ and $M$)

### How the Error Correcting term Works

* **Residual:** The core of the term, $(Y - \mu(X))$, is the residual, the difference between the actual outcome and the ML model's predicted outcome.
* **When Naive is perfect:** If our ML model for $\mu(X)$ is perfectly accurate, the expected value of this residual is zero. The entire correction term vanishes, leaving us with just the naive equations.
* **First-order error cancelation** If our ML model is slightly wrong, the functions $\delta_{\text{DL}}$ and $\delta_M$ kick in. These functions are  designed to ensure that the first-order errors from the ML models cancel out perfectly.

- This cancellation effect relies on a core functional property called **Neyman orthogonality**.

- If we define the true expected value of our score as $\Psi(\nu, \mu, r) = \mathbb{E}[\psi(X, Y; \nu, \mu, r)]$, we want the equation to have "reduced sensitivity" to the ML inputs.
- In calculus terms, this means that the mathematical derivative (specifically the Gateaux derivative) of $\Psi$ with respect to the nuisance parameters $\mu$ and $r$ evaluates exactly to **zero** when evaluated at the true parameter values.

* The "naive" base terms, $\text{DL}(\nu; \mu)$ and $M(\nu; \mu)$, are highly sensitive to estimation errors in $\mu$.
* The complex additive adjustments act as the orthogonalizing terms. They are specifically engineered so that their derivatives perfectly cancel out the derivatives of the naive terms.

Here is the cleaned-up markdown formatting with proper LaTeX applied to all equations and variables:

### Error Correcting Term Definitions

* Given a function $g$, define:
$$\Delta g(X, Y; \nu, \mu) := g(X, Y) - E_{Q(\theta,\mu)}[g(X, Y) \vert X]$$


* Applying this definition to $\eta$ and $\gamma$ (the sufficient statistic and moment condition transformation function), we define:
$$\rho(X, Y; \nu, \mu) := \Delta\eta(X, Y; \nu, \mu)^{\otimes 2}\theta + \Delta\eta(X, Y; \nu, \mu) \otimes \Delta\gamma(X, Y; \nu, \mu)\lambda$$


* We also define a tilting function $w(X, Y; \nu, \mu)$ that captures how the conditional probabilities change under the exponential tilting. Here we exploit our binary assumption on $Y$:
$$w(X, Y; \nu, \mu) = \frac{\exp(\theta^T \eta(X, Y))}{\mu(X) \cdot \exp(\theta^T (\eta(X, 1) - \eta(X, 0))) + \exp(\theta^T \eta(X, 0))}$$


* Finally, the delta functions are defined as:
$$\delta_{\text{DL}}(X; \nu, \mu) := (\rho(X, 1; \nu, \mu) - \rho(X, 0; \nu, \mu)) \cdot w(X, 1; \nu, \mu) \cdot w(X, 0; \nu, \mu)$$


$$\delta_M(X; \nu, \mu) := (\gamma(X, 1) - \gamma(X, 0)) \cdot w(X, 1; \nu, \mu) \cdot w(X, 0; \nu, \mu)$$

### Strong Orthogonality of Estimating Equations

The population estimating equations $\Psi$ satisfy a **stronger, global form of Neyman orthogonality**. Both standard and strong orthogonality require that we evaluate at the true nuisance parameter values ($\mu_0$ and $r_0$).

* We take the Gateaux derivative of $\Psi$ with respect to $\mu$. This derivative remains a function of the three parameters: $\nu$, $\mu$, and $r$.
* **Standard Neyman Orthogonality (Local):** The derivative is zero *only* when evaluated at the true target and true nuisance parameters: $(\nu_0, \mu_0, r_0)$.
* **Strong Orthogonality (Global):** The derivative is zero for **any** value of the target parameter $\nu$, provided the nuisance parameters are at their true values: $(\nu, \mu_0, r_0)$.

This stronger property significantly simplifies the mathematical analysis of the one-step estimator.


# One-step Estimator
## Why Can't We Use Z-Estimation?

A natural idea is to estimate the parameter by solving the empirical estimating equation,

$$
\Psi_n(\nu)
:=
\frac{1}{n}
\sum_{i=1}^{n}
\psi(X_i, Y_i; \nu)
=
0.
$$

This is the standard **Z-estimation** approach: replace the population estimating equation with its empirical counterpart and solve for the parameter.

Unfortunately, this approach does not work for our problem. The optimization problem in Equation (9) is **nonconvex**, meaning its objective function may have multiple local minima and stationary points. As a result, the first-order optimality conditions do **not** uniquely characterize the global minimizer.

Consequently, solving the empirical estimating equation alone may converge to a stationary point that is not the desired global solution. In other words, the solution to

$$
\Psi_n(\nu) = 0
$$

is not guaranteed to be a **consistent estimator** of the optimizer of Equation (9).

## The Idea Behind One-Step Estimation

- One-step estimation begins with a **preliminary consistent estimator** of the true parameter, denoted by $\tilde{\nu}_n$.
- We improve this initial estimate by taking **one Newton step**.
- Let $\dot{\Psi}_\nu$ denote the Jacobian of the estimating function $\psi$ with respect to $\nu$, and define its empirical counterpart by

$$
\dot{\Psi}_n(\nu)
:=
\frac{1}{n}
\sum_{i=1}^n
\dot{\Psi}_\nu(X_i, Y_i; \nu).
$$

- The one-step estimator $\hat{\nu}_n$ is obtained by solving the linearized estimating equation

$$
\Psi_n(\tilde{\nu}_n)
+
\dot{\Psi}_n(\tilde{\nu}_n)
(\nu-\tilde{\nu}_n)
=
0.
$$

- The LHS is close to the original $\Psi_n(\nu)$ when $\nu$ is close to $\tilde{\nu}_n$.


- Geometrically, one-step estimation performs a **local search** around the preliminary estimator. 
## Cross-Fitting Estimator

### Intuition

The key idea behind **cross-fitting** is to separate the estimation of the nuisance functions from the evaluation of the estimating equations. This helps avoid overfitting and leads to better statistical properties.

The procedure is as follows:

1. **Split the data into two folds**, $I_1$ and $I_2$.

2. **Estimate the nuisance functions** $\mu$ and $r$ using only the data in $I_1$.

3. **Evaluate the estimating equation and its Jacobian** on the *other* fold, $I_2$, using the nuisance estimates obtained from $I_1$.

4. **Take one Newton step** from the preliminary estimator $\tilde{\nu}_n$ to obtain an updated estimate.

5. **Swap the roles of the two folds**: estimate the nuisance functions on $I_2$, evaluate the estimating equation on $I_1$, and compute a second one-step estimator.

6. **Average the two one-step estimators** (weighted by the fold sizes) to obtain the final cross-fitted estimator.

In short, **each observation is used either to estimate the nuisance functions or to evaluate the estimating equation, but never both at the same time.** This sample splitting reduces the bias introduced by estimating the nuisance parameters.

---

### Formal Definition

Suppose we observe i.i.d. data

<p>$$
(X_i, Y_i) \sim S, \qquad i=1,\ldots,n.
$$</p>

Randomly split the sample into two folds, $I_1$ and $I_2$. For any fold $I$, define the empirical estimating equation

<p>$$
\Psi_n^I(\nu,\mu,r)
=
\frac{1}{|I|}
\sum_{i\in I}
\psi(X_i,Y_i;\nu,\mu,r),
$$</p>

and its empirical Jacobian

<p>$$
\dot{\Psi}_n^I(\nu,\mu,r)
=
\frac{1}{|I|}
\sum_{i\in I}
\dot{\psi}_\nu(X_i,Y_i;\nu,\mu,r),
$$</p>

where $\dot{\psi}_\nu$ is the Jacobian of $\psi$ with respect to $\nu$.

Next, let $\hat{\mu}_n^I$ and $\hat{r}_n^I$ denote the nuisance estimators trained using only the observations in fold $I$.

To construct the first one-step estimator, estimate the nuisance functions on $I_2$ and evaluate the estimating equation on $I_1$. The estimator $\hat{\nu}_n^{I_1}$ is defined as the solution to

<p>$$
\dot{\Psi}_n^{I_1}
(\tilde{\nu}_n,\hat{\mu}_n^{I_2},\hat{r}_n^{I_2})
(\nu-\tilde{\nu}_n)
+
\Psi_n^{I_1}
(\tilde{\nu}_n,\hat{\mu}_n^{I_2},\hat{r}_n^{I_2})
=
0.
$$</p>

The estimator $\hat{\nu}_n^{I_2}$ is defined analogously by reversing the roles of the two folds.

Finally, the **cross-fitted one-step estimator** is the weighted average

<p>$$
\hat{\nu}_n
=
\frac{|I_1|}{n}\hat{\nu}_n^{I_1}
+
\frac{|I_2|}{n}\hat{\nu}_n^{I_2}.
$$</p>

When the folds have equal size, this is simply the average of the two one-step estimators.
 
- the initial estimate is obtaiend via sequential quadratic programming.