---
layout: distill
title: "Fundamentals of Diffusion Map Embedding"
description: Principles and practice of nonlinear dimensionality reduction popularly used in neuroscience. 
tags: distill formatting
categories: research computational-neuroscience
date: 2024-09-13
featured: true
mermaid:
  enabled: true
  zoomable: true
code_diff: true
map: true
chart:
  chartjs: true
  echarts: true
  vega_lite: true
tikzjax: true
typograms: true
project: site-harmonization
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
bibliography: 2023-02-09-fc.bib

# Optionally, you can add a table of contents to your post.
# NOTES:
#   - make sure that TOC names match the actual section names
#     for hyperlinks within the post to work correctly.
#   - we may want to automate TOC generation in the future using
#     jekyll-toc plugin (https://github.com/toshimaru/jekyll-toc).
toc:
  - name: "Creating a stochastic matrix"
  - name: "Eigendecomposition and Embedding"

# Below is an example of injecting additional post-specific styles.
# If you use this post as a template, delete this _styles block.
_styles: >
  .fake-img {
    margin-bottom: 12px;
  }
  .fake-img p {
    text-align: center;
    margin: 12px 0;
  }
---
## Creating a stochastic matrix 

## Eigendecomposition and Embedding
At this stage, diffusion map embedding also does eigendecomposition, but on a $n \times n$ matrix, not a $p \times p$ matrix.

### 1. Principal Component Analysis (PCA)
PCA operates on the **feature space**. We first compute the covariance matrix $\Sigma = \frac{1}{n-1}X^TX$, which is a $p \times p$ matrix. We then perform the eigendecomposition:
$$\Sigma = U \Lambda U^T$$
We retain the first $k$ components to form $U_k$. The low-dimensional embedding is then calculated via **projection** (inner product):
$$X_{low} = XU_k$$
By design, this imbedding preserves the covariance matrix.



### 2. Diffusion Map Embedding
In contrast, Diffusion Maps operate on the **sample space**. Here, we use a stochastic transition matrix $M$, which is $n \times n$ (where $n$ is the number of observations). Now each observation $X_i$ need not be $p$-dimensional Euclidean. It can be of any data type for which a kernel can be defined.

The eigenvector of $M$ is therefore an $n$-vector. For embedding, we do not project, but lookup and scale.

* For each observation $x_i$, we extract the $i$-th element from the first $k$ eigenvectors.
* After scaling by the eigenvalues $\lambda^t$ to account for the diffusion time, we arrive at the $k$-dimensional embedding:
$$\Psi_t(x_i) = \left( \lambda_1^t \psi_1(i), \lambda_2^t \psi_2(i), \dots, \lambda_k^t \psi_k(i) \right)$$


