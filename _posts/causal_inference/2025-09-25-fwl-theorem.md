---
layout: distill
title: "FWL Theorem"
description: "Frisch-Waugh-Lovell theorem"
date: 2025-09-25
categories: causal_inference
tags: fwl-theorem
project: causal_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
---

# Estimating a Subset of Regression Coefficients

## 1. Model Setup

Consider the linear regression model:

\[
\begin{aligned}
Y &= X B + U \\
  &= [X_1 \quad X_2] 
     \begin{bmatrix} 
     \beta_1 \\ 
     \beta_2 
     \end{bmatrix} 
     + U \\
  &= X_1 \beta_1 + X_2 \beta_2 + U
\end{aligned}
\]

where:

- \( Y \) is an \( n \times 1 \) vector of observations.
- \( X = [X_1 \; X_2] \) is an \( n \times k \) matrix of regressors.
- \( \beta = (\beta_1', \beta_2')' \) is the parameter vector.
- \( U \) is the disturbance term.
- \( X_1 \) contains control variables.
- \( X_2 \) contains variables of interest.

Our objective is to estimate **only** \( \beta_2 \).

---

## 2. Idea: Partialling Out \( X_1 \)

To isolate the effect of \( X_2 \), we remove (project out) the variation explained by \( X_1 \).

Let:

\[
M_{X_1} = I - X_1 (X_1'X_1)^{-1} X_1'
\]

be the **orthogonal projection matrix onto the orthogonal complement of the column space of \( X_1 \)**.

Key property:

\[
M_{X_1} X_1 = 0
\]

---

## 3. Projecting the Model

Pre-multiply the model by \( M_{X_1} \):

\[
\begin{aligned}
M_{X_1} Y 
&= M_{X_1} X_1 \beta_1 
   + M_{X_1} X_2 \beta_2 
   + M_{X_1} U \\
&= \underbrace{M_{X_1} X_1 \beta_1}_{=0} 
   + M_{X_1} X_2 \beta_2 
   + M_{X_1} U
\end{aligned}
\]

Thus,

\[
M_{X_1} Y = M_{X_1} X_2 \beta_2 + M_{X_1} U
\]

After projection, the effect of \( X_1 \) disappears.

---

## 4. Estimation of \( \beta_2 \)

Now run OLS of \( M_{X_1} Y \) on \( M_{X_1} X_2 \):

\[
\hat{\beta}_2
= \left[ (M_{X_1} X_2)' (M_{X_1} X_2) \right]^{-1}
  (M_{X_1} X_2)' M_{X_1} Y
\]

Using properties of projection matrices:

- \( M_{X_1}' = M_{X_1} \) (symmetric)
- \( M_{X_1}^2 = M_{X_1} \) (idempotent)

So,

\[
\begin{aligned}
\hat{\beta}_2
&= \left[ X_2' M_{X_1}' M_{X_1} X_2 \right]^{-1}
   X_2' M_{X_1}' M_{X_1} Y \\
&= \left[ X_2' M_{X_1} X_2 \right]^{-1}
   X_2' M_{X_1} Y
\end{aligned}
\]

---

## 5. Interpretation

This result shows that:

- Estimating \( \beta_2 \) in the full regression of \( Y \) on \( X_1 \) and \( X_2 \)
- is equivalent to:
  1. Regressing \( Y \) on \( X_1 \) and keeping residuals,
  2. Regressing each column of \( X_2 \) on \( X_1 \) and keeping residuals,
  3. Running OLS of residualized \( Y \) on residualized \( X_2 \).

This is the **Frisch–Waugh–Lovell (FWL) Theorem**.

---

## 6. Key Takeaway

To estimate a subset of coefficients:

\[
\boxed{
\hat{\beta}_2
= (X_2' M_{X_1} X_2)^{-1} X_2' M_{X_1} Y
}
\]

You can obtain \( \hat{\beta}_2 \) by *partialling out* the effect of \( X_1 \) before running OLS.

## References

- Econometrics: FWL Theorem Algebraic Intuition (<https://www.youtube.com/watch?v=bvw-eJP3sBg>)
- On Cross-Fitting with Plug-in Estimators (<https://www.syadlowsky.com/blog/semiparametric/2022/10/24/on-cross-fitting-with-plug-in-estimators.html>)
- Double Machine Learning (<https://www.causalmlbook.com/double-machine-learning.html>)
- Double Machine Learning for Causal Inference: A Practical Guide (<https://medium.com/@med.hmamouch99/double-machine-learning-for-causal-inference-a-practical-guide-5d85b77aa586>)
- The FWL Theorem, or How to Make All Regressions Intuitive (<https://towardsdatascience.com/the-fwl-theorem-or-how-to-make-all-regressions-intuitive-59f801eb3299>)
