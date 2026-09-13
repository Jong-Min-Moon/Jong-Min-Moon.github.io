---
layout: distill
title: "Impact of High Dimensionality in Covariance Matrix Estimation"
description: "Lecture notes on how high dimensionality distorts sample covariance spectra, including the Marchenko–Pastur law, the Tracy–Widom limit for the largest eigenvalue, and connections to modern random matrix theory."
date: 2026-09-13
categories: dso-607 statistics random-matrix-theory
tags: high-dimensional-statistics covariance-estimation random-matrix-theory
project: dso-607
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Setup
  - name: Failure of Classical Concentration
  - name: Almost-Sure Limit of the Largest Eigenvalue
  - name: Tracy–Widom Fluctuations
  - name: Implications for Principal Components
  - name: Monte Carlo Study
  - name: "Part (b): Marchenko–Pastur Benchmark"
  - name: "Part (c): Johnstone Standardization and Tracy–Widom"
---

# Setup
To avoid mean estimation, suppose we observe random vectors from a zero-mean distribution. For example, $x_1, \ldots, x_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, I_p)$.

Then a natural estimator is the sample covariance matrix (without mean estimation) defined as

<p>$$\widehat{\Sigma} = \frac{1}{n} \sum_{i=1}^{n} x_i x_i^{\top} = \frac{1}{n} X^{\top} X,$$</p>

where $X \in \mathbb{R}^{n \times p}$ has the $x_i$ as its rows.

**Central question.** Does the largest eigenvalue $\lambda_{\max}(\widehat{\Sigma})$ concentrate near the population value $1$ as $n \to \infty$? 

Since the true covariance matrix $I_p$ has all eigenvalues equal to 1, we expect $\lambda_{\max}(\widehat{\Sigma})$ to be close to 1 as $n \to \infty$. But this is not true in diverging dimensions scenario. We have two theories to explain this phenomenon.

## Upper Bound of the Largest Eigenvalue

**Geman (1980)** showed that, when \(n,p\to\infty\) with
<p>\[
\frac{n}{p}\to\gamma\geq 1,
\]</p>
the largest eigenvalue of \(\widehat{\Sigma}\) converges almost surely to
<p>\[
\left(1+\sqrt{\gamma^{-1}}\right)^2.
\]</p>

This quantity is precisely the **upper edge of the Marchenko–Pastur law**, which describes the limiting spectral distribution of \(\widehat{\Sigma}\) in the proportional-growth regime.

As \(\gamma\to\infty\) (equivalently, \(p/n\to 0\)), the upper edge approaches \(1\), recovering the classical low-dimensional behavior. In contrast, when \(\gamma=1\), so that \(p/n\to 1\), the limiting largest eigenvalue is
<p>\[
(1+1)^2=4,
\]</p>
which is substantially larger than the population eigenvalue \(1\).

Thus, in high dimensions, the largest sample eigenvalue can be systematically inflated even when the true covariance matrix is \(I_p\). This is not a small-sample artifact: the discrepancy persists asymptotically when \(p\) and \(n\) grow at comparable rates. In particular, when \(p/n\to 1\), the largest eigenvalue converges to \(4\), rather than \(1\).

The key point is that the eigenvalues of the sample covariance matrix do not collapse around the population eigenvalue in the proportional-growth regime. Instead, they spread over a nontrivial interval determined by the Marchenko–Pastur law, with the upper edge governing the asymptotic behavior of the largest eigenvalue.



## Tracy–Widom Fluctuations

**Johnstone (2001)** refined the almost-sure limit established by Geman by characterizing the fluctuations of $\lambda_{\max}(\widehat{\Sigma})$ around its limiting value. Specifically, define the centering and scaling sequences
<p>\[
\mu_{np}
=
\left(\sqrt{n-1}+\sqrt{p}\right)^2,
\qquad
\sigma_{np}
=
\left(\sqrt{n-1}+\sqrt{p}\right)
\left(
\frac{1}{\sqrt{n-1}}+\frac{1}{\sqrt{p}}
\right)^{1/3}.
\]</p>

The corresponding standardized statistic is
<p>\[
Z_{n,p}
=
\frac{n\lambda_{\max}(\widehat{\Sigma})-\mu_{np}}
{\sigma_{np}}.
\]</p>

A natural question is whether $Z_{n,p}$ is approximately Gaussian when $n$ and $p$ are large. Surprisingly, the answer is no. A common misconception is that a large sample size should automatically lead to an approximately normal standardized statistic. While this is true for many classical statistics governed by a central limit theorem, the largest eigenvalue is an **extreme spectral statistic** and belongs to a different universality class.

In the proportional-growth regime, where both $n$ and $p$ grow at comparable rates, $\lambda_{\max}(\widehat{\Sigma})$ fluctuates around the upper edge of the Marchenko–Pastur distribution. After the specific Johnstone centering and scaling,
<p>\[
Z_{n,p}
=
\frac{n\lambda_{\max}(\widehat{\Sigma})-\mu_{np}}
{\sigma_{np}},
\]</p>
these fluctuations converge in distribution to the **Tracy–Widom distribution of type 1**, rather than to a normal distribution.

This explains why the standardized empirical distribution can remain visibly non-Gaussian even for large $n$ and $p$. In particular, the Tracy–Widom distribution is asymmetric and right-skewed, so the empirical distribution of $Z_{n,p}$ should exhibit positive skewness. Likewise, a normal Q–Q plot will generally show systematic deviations from a straight line, especially in the tails.

Therefore, **observing a visibly non-Gaussian shape is not a contradiction of asymptotic theory; it is precisely what the Tracy–Widom limit predicts**. The important point is that standardization does not imply Gaussianity: the limiting distribution depends on the underlying asymptotic regime and on the statistic being studied.

 
 
# Monte Carlo Simulations

## 1. Simulation Setup

Fix the sample size at \(n=100\) and consider three dimensional settings:
<p>\[
p\in\{5,50,500\}.
\]</p>

For each value of \(p\), perform at least \(1{,}000\) independent Monte Carlo replications. In each replication:

1. Generate the data matrix \(X\in\mathbb{R}^{n\times p}\) according to the model specified above.

2. Compute the sample covariance matrix
   <p>\[
   \widehat{\Sigma}
   =\frac{1}{n}X^\top X.
   \]</p>

3. Record the largest eigenvalue
   <p>\[
   \lambda_{\max}(\widehat{\Sigma}).
   \]</p>

4. For \(p=50\) and \(p=500\), compute the Johnstone-standardized statistic
   <p>\[
   Z_{n,p}
   =
   \frac{n\lambda_{\max}(\widehat{\Sigma})-\mu_{n,p}}
   {\sigma_{n,p}},
   \]</p>
   where
   <p>\[
   \mu_{n,p}
   =
   \left(\sqrt{n-1}+\sqrt{p}\right)^2,
   \]</p>
   and
   <p>\[
   \sigma_{n,p}
   =
   \left(\sqrt{n-1}+\sqrt{p}\right)
   \left(
   \frac{1}{\sqrt{n-1}}+\frac{1}{\sqrt{p}}
   \right)^{1/3}.
   \]</p>

Use the simulated values to obtain the empirical distributions of
\(\lambda_{\max}(\widehat{\Sigma})\) for \(p=5,50,500\), and of \(Z_{n,p}\) for \(p=50,500\).

## 2. Empirical Distributions of the Largest Eigenvalue

Produce a single figure with three clearly labeled panels, one for each value of \(p\). In each panel:

- Plot the empirical distribution of \(\lambda_{\max}(\widehat{\Sigma})\).
- Clearly label the axes and indicate the corresponding value of \(p\).
- Add the theoretical Marchenko–Pastur/Geman upper-edge benchmark
  <p>\[
  \lambda_+\left(\frac{p}{n}\right)
  =
  \left(1+\sqrt{\frac{p}{n}}\right)^2.
  \]</p>
- Compare the theoretical upper edge with the empirical center and upper tail of the distribution.

For each \(p\), also report the following empirical summary statistics:

- Mean
- Standard deviation
- Median
- 5th percentile
- 95th percentile

Present these results in a numerical table.

## 3. Tracy–Widom Behavior

For \(p=50\) and \(p=500\):

- Plot the empirical distributions of the Johnstone-standardized statistic \(Z_{n,p}\).
- Report the empirical skewness of each standardized distribution.
- Include a normal Q–Q plot for each value of \(p\).

Use these plots and summary statistics to assess whether the standardized distributions appear approximately Gaussian or instead exhibit the asymmetric, right-skewed shape expected under the Tracy–Widom limit.



## Note on Implementation

A naive approach computes all eigenvalues of the $p \times p$ matrix $\widehat{\Sigma} = X^\top X / n$, which costs $O(p^3)$ time. For $p = 500$ this is already heavy, and for larger $p$ it becomes prohibitive. Two algebraic facts eliminate this bottleneck.

### Fact 1: The $XX^\top$ / $X^\top X$ eigenvalue identity

For any $X \in \mathbb{R}^{n \times p}$, the **nonzero eigenvalues** of $X^\top X$ and $X X^\top$ are identical.

*Proof sketch.* If $X^\top X \, v = \lambda v$ with $\lambda \neq 0$, set $u = Xv / \|Xv\|$. Then $X X^\top u = \lambda u$. The argument is symmetric.

Consequence: $\lambda_{\max}(\widehat{\Sigma}) = \lambda_{\max}(X^\top X) / n = \lambda_{\max}(X X^\top) / n$. 
When $p > n$, computing eigenvalues of $X X^\top$ (size $n \times n$) instead of $X^\top X$ (size $p \times p$) reduces cost from $O(p^3)$ to $O(n^2 p)$.

### Fact 2: Singular values connect both matrices

The singular values $s_1 \geq s_2 \geq \cdots$ of $X$ satisfy

<p>$$s_k^2 = \lambda_k(X^\top X) = \lambda_k(X X^\top) \quad \text{for } k = 1, \ldots, \min(n,p).$$</p>

Therefore

<p>$$\lambda_{\max}(\widehat{\Sigma}) = \frac{s_{\max}(X)^2}{n}.$$</p>

In NumPy, `np.linalg.svd(X, compute_uv=False)` returns only singular values (skipping the expensive $U, V$ computation) in $O(n^2 p)$ time for $n \leq p$, automatically selecting the efficient path. This is the cleanest one-liner for large-scale Monte Carlo.
 