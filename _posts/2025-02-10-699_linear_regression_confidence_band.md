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
# Confidence band for simultaneous estimation in multiple regression

## 1. Model Setup
The general formula in words is:
\[
  \text{Sample estimate} \pm (\text{t-multiplier} \times \text{standard error}).
  \]
We derive this using the normal theory. We assume the conditional normal model with fixed full-rank design. The OLS estimator  $\hat{\bm{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{Y}$ is a linear transformation of the random vector $\mathbf{Y}$. Since $\mathbf{Y}$ is multivariate normal, $\hat{\bm{\beta}}$ is also multivariate normal, and $\hat{\mathbb{E}}[\mathbf{Y} | \mathbf{X} = \mathbf{x}_0] = \mathbf{x}_0^\top \hat{\boldsymbol{\beta}}$, the conditional expectation of a new feature $\mathbf{x}_0$, is also multivariate normal. Therefore the distribution of $\mathbf{x}_0^\top \hat{\boldsymbol{\beta}}$ is fully specified by its expectation and variance. These can be computed using the formulas for expectation and variance of linear transformation. As a result, we have:
\[\mathbf{x}_0^\top \hat{\boldsymbol{\beta}}
 \sim N(\mathbf{x}_0^\top \boldsymbol{\beta}, \sigma^2 \mathbf{x}_0^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_0).
  \]
 Now, standardization and inverting will give us a confidence interval of $\mathbf{x}_0^\top \boldsymbol{\beta}$ that defined using $\sigma^2$ and $Z_{\alpha/2}$. This is useless, since we do not know $\sigma^2$. Therefore we use the following facts:
-  $\mathbf{Y}^\top(\mathbf{I} - \mathbf{H}) \mathbf{Y} / \sigma^2 \sim \chi^2(n - p)$, where $\mathbf{H}:=\mathbf{X}(\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^\top,$
-  $\mathbf{Y}^\top(\mathbf{I} - \mathbf{H}) \mathbf{Y}$ and $\mathbf{x}_0^\top \hat{\boldsymbol{\beta}}$ are independent.

The first one comes from the rank of the projector $\mathbf{I}-\mathbf{H}$. The second one comes from that for normal distribution, uncorrelation means indendence, and $\mathbf{x}_0^\top \hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{Y}$, where $(\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^\top$ is in the column space of $\mathbf{X}$.

 it was shown that the mean square error 
\[
Y'(I - M) Y / (n - r)
\]
is an unbiased estimate of \( \sigma^2 \). We now show that

Clearly,
\[
Y / \sigma \sim N(X\beta / \sigma, I),
\]
so by Theorem 1.3.3,
\[
Y'(I - M) Y / \sigma^2 \sim \chi^2(r(I - M), \beta' X' (I - M) X \beta / 2\sigma^2).
\]

We have already shown that \( r(I - M) = n - r \) and 
\[
\beta' X' (I - M) X \beta / 2\sigma^2 = 0.
\]
Moreover, by Theorem 1.3.7, \( MY \) and \( Y' (I - M) Y \) are independent.
}}

\end{document}


Our goal is to construct a confidence interval for this quantity.

---

## 2. Distribution of \( \hat{y}_\text{new} = \mathbf{x}_\text{new}^T \hat{\bm{\beta}} \)

Since \( \hat{\bm{\beta}} \) is a linear transformation of \( \mathbf{y} \), it follows a **multivariate normal distribution**:

\[
\hat{\bm{\beta}} \sim \mathcal{N} \left( \bm{\beta}, \sigma^2 (\mathbf{X}^T \mathbf{X})^{-1} \right).
\]

Thus, the **distribution of \( \hat{y}_\text{new} \)** is:

\[
\hat{y}_\text{new} = \mathbf{x}_\text{new}^T \hat{\bm{\beta}} \sim \mathcal{N} \left( \mathbf{x}_\text{new}^T \bm{\beta}, \sigma^2 \mathbf{x}_\text{new}^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_\text{new} \right).
\]

### Standardization (Pivot Construction)
Define the standardized statistic:

\[
Z = \frac{\hat{y}_\text{new} - \mathbf{x}_\text{new}^T \bm{\beta}}{\sigma \sqrt{\mathbf{x}_\text{new}^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_\text{new}}}.
\]

Since \( \hat{y}_\text{new} \) is normally distributed, it follows that:

\[
Z \sim \mathcal{N}(0,1).
\]

However, \( \sigma^2 \) is unknown, so we estimate it using the **residual variance**:

\[
\hat{\sigma}^2 = \frac{1}{n - p} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2.
\]

It is well known that:

\[
\frac{(n - p) \hat{\sigma}^2}{\sigma^2} \sim \chi^2_{n - p}.
\]

Since \( \hat{\sigma} \) is estimated from the data, replacing \( \sigma \) in the standardization leads to a **Student's \( t \)-distribution**:

\[
T = \frac{\hat{y}_\text{new} - \mathbf{x}_\text{new}^T \bm{\beta

}}{\hat{\sigma} \sqrt{\mathbf{x}_\text{new}^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_\text{new}}} \sim t_{n - p}.
\]

---

## 3. Confidence Interval for the Conditional Expectation
Using the **pivot method**, for a confidence level \( 1 - \alpha \), we find the critical value \( t_{\alpha/2, n - p} \) such that:

\[
P \left( -t_{\alpha/2, n - p} \leq \frac{\hat{y}_\text{new} - \mathbf{x}_\text{new}^T \bm{\beta}}{\hat{\sigma} \sqrt{\mathbf{x}_\text{new}^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_\text{new}}} \leq t_{\alpha/2, n - p} \right) = 1 - \alpha.
\]

Rearranging gives the **confidence interval for \( \mathbf{x}_\text{new}^T \bm{\beta} \)**:

\[
\hat{y}_\text{new} \pm t_{\alpha/2, n - p} \cdot \hat{\sigma} \sqrt{\mathbf{x}_\text{new}^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_\text{new}}.
\]
