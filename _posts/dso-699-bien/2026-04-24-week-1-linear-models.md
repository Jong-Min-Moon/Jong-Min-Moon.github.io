---
layout: post
title: "DSO 699 Week 1: Linear Models and Matrix Decompositions"
date: 2026-04-24 18:45:00-0700
description: Review of linear algebra foundations for statistical modeling, including projections, QR decomposition, and SVD.
tags: lecture-notes linear-algebra
categories: dso-699-bien
project: dso-699-bien
---

### Overview
In the first week of DSO 699, we reviewed the linear algebra foundations that underpin modern statistical modeling. Understanding these concepts is crucial for interpreting model coefficients and developing efficient algorithms.

### Key Topics

#### 1. Projections and Normal Theory
We discussed the geometric interpretation of ordinary least squares (OLS) as a projection of the response vector $y$ onto the column space of the design matrix $X$.
- The projection matrix: $P = X(X^\top X)^{-1}X^\top$.
- Residuals: $e = (I - P)y$.

#### 2. QR Decomposition and Gram-Schmidt
The QR decomposition is a stable way to compute the projection and interpret coefficients.
- $X = QR$, where $Q$ has orthonormal columns and $R$ is upper triangular.
- Implications for interpreting coefficients in nested models.

#### 3. SVD and Moore-Penrose Pseudoinverse
The Singular Value Decomposition (SVD) provides a deeper look into the structure of $X$, especially in cases of multicollinearity or high-dimensional settings ($p > n$).
- $X = U \Sigma V^\top$.
- The pseudoinverse $X^\dagger = V \Sigma^\dagger U^\top$ allows us to find the minimum-norm solution to underdetermined systems.

### Looking Ahead
Next week, we will dive into dummy coding, interactions, and the connections between linear models and ANOVA.
