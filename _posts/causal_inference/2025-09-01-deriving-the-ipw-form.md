---
layout: distill
title: "Deriving the IPW Estimator: From One RCT to Infinite RCTs under Unconfoundedness"
description: "An intuitive derivation of the Inverse Probability Weighting (IPW) estimator from a single RCT to multiple RCTs and observational data."
date: 2025-09-01
categories: causal_inference statistics
tags: causal-inference ipw
project: causal_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
bibliography: 2025-09-01-ipw.bib
toc:
  - name: "1. One RCT (The Baseline)"
  - name: "2. Two RCTs"
  - name: "3. Many RCTs (Discrete Covariates)"
  - name: "4. Infinitely Many RCTs (Continuous Covariates)"
---
This post shows that somewhat intimitating form of IPW estimator 

<p>
$$
\begin{equation*}
\hat{\tau}_{IPW} = \frac{1}{n} \sum_{i=1}^n \left( \frac{W_i Y_i}{\hat{e}(X_i)} - \frac{(1 - W_i) Y_i}{1 - \hat{e}(X_i)} \right)
\end{equation*}
$$
</p>

is actually just a weighted average of many mean differences.

## 1. One RCT (The Baseline)

<p>
$$
\begin{align*}
\hat{\tau} &= \left( \text{Average of Treated} \right) - \left( \text{Average of Control} \right)\\&= \frac{1}{n_1} \sum_{W_i=1} Y_i - \frac{1}{n_0} \sum_{W_i=0} Y_i 
\end{align*}
$$
</p>

**Derivation to IPW form:**
First, rewrite the sums over subsets as sums over the entire sample $$n$$ by using $$W_i$$ and $$(1 - W_i)$$ to zero out the irrelevant terms:

<p>
$$
\begin{equation*}
\hat{\tau} = \sum_{i=1}^n \frac{W_i Y_i}{n_1} - \sum_{i=1}^n \frac{(1 - W_i) Y_i}{n_0}
\end{equation*}
$$
</p>

Next, define the constant propensity score $$e = \frac{n_1}{n}$$. This implies:

<p>
$$
\begin{align*}
n_1 &= n \cdot e\\
n_0 &= n \cdot (1 - e)
\end{align*}
$$
</p>

Substitute these into the denominators:

<p>
$$
\begin{equation*}
\hat{\tau} = \sum_{i=1}^n \frac{W_i Y_i}{n \cdot e} - \sum_{i=1}^n \frac{(1 - W_i) Y_i}{n \cdot (1 - e)}
\end{equation*}
$$
</p>

Finally, factor out $$\frac{1}{n}$$ to reveal the IPW form:

<p>
$$
\begin{equation*}
\hat{\tau} = \frac{1}{n} \sum_{i=1}^n \left( \frac{W_i Y_i}{e} - \frac{(1 - W_i) Y_i}{1 - e} \right)
\end{equation*}
$$
</p>

## 2. Two RCTs 
Let's say we have two separate RCTs, one in City A and one in City B. 
The intuitive approach is to calculate the ATE for each city separately, and then take a weighted average based on their population sizes.

<p>
$$
\begin{equation*}
\hat{\tau}_\{\mathrm{AGG}\} = \frac{n_A}{n} \hat{\tau}_A + \frac{n_B}{n} \hat{\tau}_B
\end{equation*}
$$
</p>

This is the sample version of:

<p>
$$
\begin{equation*}
\tau = \mathbb{E}[\tau(X)\,|\,X] = \sum P(X) \tau(X)
\end{equation*}
$$
</p>

**Derivation to IPW form:**
Using the logic from Step 1, we can write the ATE for City A ($$\hat{\tau}_A$$) in its local IPW form, where $$\hat{e}_A$$ is the specific treatment probability in City A:

<p>
$$
\begin{equation*}
\hat{\tau}_A = \frac{1}{n_A} \sum_{i \in A} \left( \frac{W_i Y_i}{\hat{e}_A} - \frac{(1 - W_i) Y_i}{1 - \hat{e}_A} \right)
\end{equation*}
$$
</p>

Now, plug this back into the intuitive aggregation formula. Notice how the city population size $n_A$ perfectly cancels out:

<p>
$$
\begin{align*}
\frac{n_A}{n} \hat{\tau}_A &= \frac{n_A}{n} \left[ \frac{1}{n_A} \sum_{i \in A} \left( \frac{W_i Y_i}{\hat{e}_A} - \frac{(1 - W_i) Y_i}{1 - \hat{e}_A} \right) \right]
\\&= \frac{1}{n} \sum_{i \in A} \left( \frac{W_i Y_i}{\hat{e}_A} - \frac{(1 - W_i) Y_i}{1 - \hat{e}_A} \right)
\end{align*}
$$
</p>

When you do this for both City A and City B and add them together, summing over City A plus summing over City B is exactly the same as summing over the entire dataset $$n$$:

<p>
$$ 
\begin{align*}
\hat{\tau}_\{\mathrm{AGG}\} &= \frac{1}{n} \sum_{i=1}^n \left( \frac{W_i Y_i}{\hat{e}(C_i)} - \frac{(1 - W_i) Y_i}{1 - \hat{e}(C_i)} \right)
\end{align*}
$$
</p>

## 3. Many RCTs (Discrete Covariates)

This is the exact same mathematical mechanism as the Two RCT case, generalized to $p$ finite groups defined by covariates $X_i = x$:

<p>
$$
\begin{equation*}
\hat{\tau}_\{\mathrm{AGG}\} = \sum_{x \in \mathcal{X}} \frac{n_x}{n} \hat{\tau}(x)
\end{equation*}
$$
</p>

Where the group-specific ATE is:

<p>
$$
\begin{equation*}
\hat{\tau}(x) = \frac{1}{n_{x,1}} \sum_{X_i=x, W_i=1} Y_i - \frac{1}{n_{x,0}} \sum_{X_i=x, W_i=0} Y_i
\end{equation*}
$$
</p>

**Derivation to IPW form:**
First, express the denominators $n_{x,1}$ and $n_{x,0}$ using the group-specific propensity score $\hat{e}(x) = \frac{n_{x,1}}{n_x}$:

<p>
$$
\begin{align*}
n_{x,1} &= n_x \hat{e}(x)
\\
n_{x,0} &= n_x (1 - \hat{e}(x))
\end{align*}
$$
</p>

Rewrite $\hat{\tau}(x)$ using the $W_i$ filter trick to sum over everyone in group $x$:

<p>
$$
\begin{align*}
\hat{\tau}(x) &= \sum_{i: X_i=x} \left( \frac{W_i Y_i}{n_x \hat{e}(x)} - \frac{(1 - W_i) Y_i}{n_x (1 - \hat{e}(x))} \right) \\
&= \frac{1}{n_x} \sum_{i: X_i=x} \left( \frac{W_i Y_i}{\hat{e}(x)} - \frac{(1 - W_i) Y_i}{1 - \hat{e}(x)} \right)
\end{align*}
$$
</p>

Now, plug this $$\hat{\tau}(x)$$ back into the outer aggregation sum $\hat{\tau}_\{\mathrm{AGG}\}$. Once again, the subgroup sizes $n_x$ cancel out:

<p>
$$ 
\begin{align*}
\hat{\tau}_\{\mathrm{AGG}\} &= \sum_{x \in \mathcal{X}} \frac{n_x}{n} \left[ \frac{1}{n_x} \sum_{i: X_i=x} \left( \frac{W_i Y_i}{\hat{e}(x)} - \frac{(1 - W_i) Y_i}{1 - \hat{e}(x)} \right) \right] 
\\
&= \sum_{x \in \mathcal{X}} \frac{1}{n} \sum_{i: X_i=x} \left( \frac{W_i Y_i}{\hat{e}(X_i)} - \frac{(1 - W_i) Y_i}{1 - \hat{e}(X_i)} \right) 
\end{align*}
$$
</p>

Summing across all discrete groups $x$ is equivalent to a single sum over all $n$ individuals in the dataset, leaving us with the final, generalized formula:

<p>
$$ 
\begin{equation*}
\hat{\tau}_\{\mathrm{AGG}\} = \frac{1}{n} \sum_{i=1}^n \left( \frac{W_i Y_i}{\hat{e}(X_i)} - \frac{(1 - W_i) Y_i}{1 - \hat{e}(X_i)} \right) 
\end{equation*}
$$
</p>

## 4. Infinitely Many RCTs (Continuous Covariates)
Here we just convince ourselves that the same logic applies to continuous covariates. The only difference is that we can no longer calculate the empirical fraction $\hat{e}(X_i)$ because the group size $n_x$ often drops to 1 or 0. 
We just replace the empirical fraction $\hat{e}(X_i)$ with a modeled probability from a continuous function (like logistic regression):

<p>
$$ 
\begin{equation*}
\hat{\tau}_{IPW} = \frac{1}{n} \sum_{i=1}^n \left( \frac{W_i Y_i}{\hat{e}(X_i)} - \frac{(1 - W_i) Y_i}{1 - \hat{e}(X_i)} \right) 
\end{equation*}
$$
</p>

## 5. Assumptions
We have to make sure that we have RCT for each covariate fixed. This means that we need to have ignorability and overlap assumptions, just as in \href{https://jong-min.org/blog/2025/when-does-linear-regression-yield-causal-inference/}{causal inference by linear regression}. The difference is that we no longer need the well specified linear model assumption <d-cite key="wager2024stats361"></d-cite>.