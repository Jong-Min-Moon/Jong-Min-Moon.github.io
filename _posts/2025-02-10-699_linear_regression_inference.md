---
layout: distill
title: a distill-style blog post
description: an example of a distill-style blog post and main elements
tags: distill formatting
giscus_comments: true
date: 2021-05-22
featured: true

authors:
  - name: Albert Einstein
    url: "https://en.wikipedia.org/wiki/Albert_Einstein"
    affiliations:
      name: IAS, Princeton
  - name: Boris Podolsky
    url: "https://en.wikipedia.org/wiki/Boris_Podolsky"
    affiliations:
      name: IAS, Princeton
  - name: Nathan Rosen
    url: "https://en.wikipedia.org/wiki/Nathan_Rosen"
    affiliations:
      name: IAS, Princeton

bibliography: 2018-12-22-distill.bib

# Optionally, you can add a table of contents to your post.
# NOTES:
#   - make sure that TOC names match the actual section names
#     for hyperlinks within the post to work correctly.
#   - we may want to automate TOC generation in the future using
#     jekyll-toc plugin (https://github.com/toshimaru/jekyll-toc).
toc:
  - name: Equations
    # if a section has subsections, you can add them as follows:
    # subsections:
    #   - name: Example Child Subsection 1
    #   - name: Example Child Subsection 2
  - name: Citations
  - name: Footnotes
  - name: Code Blocks
  - name: Interactive Plots
  - name: Layouts
  - name: Other Typography?

# Below is an example of injecting additional post-specific styles.
# If you use this post as a template, delete this _styles block.
_styles: >
  .fake-img {
    background: #bbb;
    border: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: 0 0px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 12px;
  }
  .fake-img p {
    font-family: monospace;
    color: white;
    text-align: left;
    margin: 12px 0;
    text-align: center;
    font-size: 16px;
  }

---
# Confidence Interval for the Conditional Expectation in Multiple Linear Regression

## 1. Interval for single estimation
The general formula in words is:
\[
  \text{Sample estimate} \pm (\text{t-multiplier} \times \text{standard error}).
  \]
We derive this using the normal theory. We assume:
- $ n > p$. 
- The conditional normal model, independent noise.
- Fixed full-rank design matrix of size $n \times (p+1)$, with the first column being the all 1's.
- A new predictor $\mathbf{x}_0 \in \mathbb{R}^{(p+1)}$ contains 1 as the first element (for intercept)
The fixed design simplfies many analysis, making many things just as a linear transform of $\mathbf{Y}$.

The OLS estimator  $\hat{\bm{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{Y}$ is a linear transformation of the random vector $\mathbf{Y}$. Since $\mathbf{Y}$ is multivariate normal, $\hat{\bm{\beta}}$ is also multivariate normal, and $\hat{\mathbb{E}}[\mathbf{Y} | \mathbf{X} = \mathbf{x}_0] = \mathbf{x}_0^\top \hat{\boldsymbol{\beta}}$, the conditional expectation of a new feature $\mathbf{x}_0$, is also multivariate normal. Therefore the distribution of $\mathbf{x}_0^\top \hat{\boldsymbol{\beta}}$ is fully specified by its expectation and variance. These can be computed using the formulas for expectation and variance of linear transformation. As a result, we have the following one-dimensional normal distribution:
\[\mathbf{x}_0^\top \hat{\boldsymbol{\beta}}
 \sim N(\mathbf{x}_0^\top \boldsymbol{\beta}, \sigma^2 \mathbf{x}_0^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_0).\] Now, standardization and inverting will give us a confidence interval of $\mathbf{x}_0^\top \boldsymbol{\beta}$ that defined using $\sigma^2$ and $z_{\alpha/2}$. This is useless, since we do not know $\sigma^2$. 
 
 Therefore we derive a t distribution by replacing $\sigma^2$ by its estimate. For this purpose, define the projection matrix $\mathbf{H}:=\mathbf{X}(\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^\top$. We will use  $\mathbf{Y}^\top(\mathbf{I} - \mathbf{H}) \mathbf{Y}$, called the residual sum of squares (RSS) or error sum of squares (SSE). Note that $\mathrm{RSS}/(n-p-1)$ is an unbiased estimator of $\sigma^2$. Therefore, RSS can give us a standard error, which is an estimate of the standard deviation of the sampling ditribution. We will use the following facts:
-  RSS and  $\mathbf{x}_0^\top \hat{\boldsymbol{\beta}}$ are independent.
-  $\dfrac{1}{\sigma^2} \mathrm{RSS} \sim \chi^2(n - p-1)$.
The first one comes from the rank of the projector $\mathbf{I}-\mathbf{H}$. The second one comes from that for normal distribution, uncorrelation means indendence, and $\mathbf{x}_0^\top \hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{Y}$, where $(\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^\top$ is in the column space of $\mathbf{X}$.

Using the formula $U/\sqrt{V/df}$ for t distribution, and with some cancelations (importantly, $\sigma$ cancels out), we obtain:
\[
T = \frac{
  \mathbf{x}_0^\top \hat{\boldsymbol{\beta}} - \mathbf{x}_0^\top \boldsymbol{\beta}
}{
  \sqrt{
\mathbf{x}_0^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_0 
\dfrac{1}{n-p-1}\mathbf{Y}^\top(\mathbf{I} - \mathbf{H}) \mathbf{Y}
  }
  }
  \sim
  t(n-p-1).
\]
The denominator is a standard error. Not necessarily an unbiased estimator. It is a square root of the unbiased estimaotr of the variance of the sampling distribution.

## 2. Interval for simultaneous estimation
