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
---

# Setup

Let $x_1, \ldots, x_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, I_p)$ and define the sample covariance matrix (without mean estimation) as

<p>$$\widehat{\Sigma} = \frac{1}{n} \sum_{i=1}^{n} x_i x_i^{\top} = \frac{1}{n} X^{\top} X,$$</p>

where $X \in \mathbb{R}^{n \times p}$ has the $x_i$ as its rows.

**Central question.** Does the largest eigenvalue $\lambda_{\max}(\widehat{\Sigma})$ concentrate near the population value $1$ as $n \to \infty$?

---

# Failure of Classical Concentration

In the **fixed-$p$** regime, the law of large numbers guarantees $\widehat{\Sigma} \xrightarrow{a.s.} I_p$, so $\lambda_{\max}(\widehat{\Sigma}) \xrightarrow{a.s.} 1$.

In high dimensions the picture changes dramatically. Consider $n = 100$ and increasing $p$:

| Dimension | Approximate range of $\lambda_{\max}(\widehat{\Sigma})$ | Centering |
|-----------|----------------------------------------------------------|-----------|
| $p = 5$   | $[1.0,\; 1.8]$                                          | Near 1    |
| $p = 50$  | $[2.6,\; 3.2]$                                          | Far right |
| $p = 500$ | $[9.5,\; 11.0]$                                         | Far right |

As $p$ grows with $n$, the distribution of $\lambda_{\max}(\widehat{\Sigma})$ **shifts systematically to the right of 1**. This is a central phenomenon in **random matrix theory (RMT)**.

---

# Almost-Sure Limit of the Largest Eigenvalue

**Geman (1980)** established that when $n, p \to \infty$ with $p/n \to \gamma^{-1} \geq 1$ (equivalently, $n/p \to \gamma \geq 1$),

<p>$$\lambda_{\max}(\widehat{\Sigma}) \xrightarrow{a.s.} \left(1 + \gamma^{-1/2}\right)^2.$$</p>

This is the **upper edge of the Marchenko–Pastur law**, the limiting spectral distribution of $\widehat{\Sigma}$ in this proportional-growth regime. Key observations:

- When $\gamma = 1$ ($p/n \to 1$), the limit is $(1 + 1)^2 = 4$, far from the population value of $1$.
- As $\gamma \to \infty$ ($p \ll n$), the limit approaches $1$, recovering classical behavior.
- The shift is **deterministic** and grows monotonically as the dimension-to-sample ratio $p/n$ increases.

---

# Tracy–Widom Fluctuations

**Johnstone (2001)** refined the almost-sure limit by characterizing the fluctuations of $\lambda_{\max}(\widehat{\Sigma})$ around its Geman limit. Specifically, define the centering and scaling sequences

<p>$$\mu_{np} = \left(\sqrt{n-1} + \sqrt{p}\right)^2, \qquad \sigma_{np} = \left(\sqrt{n-1} + \sqrt{p}\right)\left(\frac{1}{\sqrt{n-1}} + \frac{1}{\sqrt{p}}\right)^{1/3}.$$</p>

Then

<p>$$\frac{n\,\lambda_{\max}(\widehat{\Sigma}) - \mu_{np}}{\sigma_{np}} \xrightarrow{D} \mathrm{TW}_1,$$</p>

where $\mathrm{TW}_1$ is the **Tracy–Widom distribution of order 1**, arising originally in the study of the largest eigenvalue of the Gaussian Orthogonal Ensemble (GOE).

### Remarks

- $\mathrm{TW}_1$ is a universal, non-Gaussian limit: it is skewed to the right and has heavier right tails than a normal.
- The centering $\mu_{np}$ and the scaling $\sigma_{np}$ both depend on **both** $n$ and $p$; there is no clean separation of sample-size and dimension effects.
- Tracy–Widom universality extends well beyond the Gaussian case: the same limit holds for a wide class of sub-Gaussian designs, making it a robust inferential benchmark.

---

# Implications for Principal Components

The concentration failure of $\lambda_{\max}(\widehat{\Sigma})$ is not merely a curiosity. It has direct consequences for **principal component analysis (PCA)** and **spectral embeddings** in high dimensions:

- **Inconsistency of leading eigenvectors.** Even when the population has a single spiked direction, the sample eigenvector can be inconsistent for the population direction when $p/n \not\to 0$ (Johnstone & Lu, 2009).
- **Overestimation of signal strength.** Naive use of $\lambda_{\max}(\widehat{\Sigma})$ as a test statistic for signal detection requires Tracy–Widom calibration, not $\chi^2$ or normal calibration.
- **Rank selection.** Distinguishing true spikes from noise eigenvalues requires methods that account for the bulk spectral edge (Johnstone & Onatski, 2020).

Current course topics extend this analysis to:

1. **Diverging spikes** — eigenvector asymptotics when the spike strength grows with $n$ and $p$ (Fan, Fan, Han & Lv, 2022).
2. **Generalized Laplacian latent embeddings** — spectral theory for graph-based representations (Fan et al., 2026).
3. **Universal rank inference** — data-driven rank selection via residual subsampling (Han, Yang & Fan, 2023).
4. **Deep representation geometry** — connecting RMT to neural collapse and uncertainty quantification in deep networks.
