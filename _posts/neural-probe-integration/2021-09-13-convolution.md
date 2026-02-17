---
layout: post
title: "Fundamentals of Convolution"
date: 2021-09-13
description: "Inner product and convolution in signal processing and statistics"
project: neural-probe-integration
categories: research, computational neuroscience
math: true
---

### I. Signal Processing Perspective
**Core Concept:** Convolution is an extension of the inner product, representing the time-varying similarity between a signal and a kernel (filter).

#### 1. Mathematical Foundation: The Inner Product
* **Definition:** The scalar result obtained by summing the products of corresponding elements in two vectors.
* **Interpretation:** The inner product represents the **similarity** between two vectors.
    * High inner product: High similarity.
    * Zero inner product: Orthogonality (no similarity).

#### 2. The Convolution Operation
* **Definition:** A repeated computation of the inner product over time.
* **Procedure:**
    1.  **Flip:** The kernel (the mover or filter) is reversed in time.
    2.  **Shift:** The flipped kernel slides along the time axis of the signal.
    3.  **Multiply & Sum:** At each time step, the inner product is computed between the signal and the overlapping kernel section.
* **Result:** A time series representing the similarity between the signal and the flipped kernel at every time point.

#### 3. Convolution vs. Cross-Covariance
* **The "Flip" Distinction:**
    * **Convolution:** Requires the kernel to be flipped (reversed) relative to the time axis.
    * **Cross-Covariance:** The kernel is *not* flipped; it is simply shifted and the inner product is computed.
* **Note:** If the kernel is symmetric (e.g., a Gaussian distribution or cosine wave), convolution and cross-covariance yield mathematically identical results, though they remain conceptually distinct operations.

#### 4. Interpretations of Convolution
Cohen (2014) offers standard interpretations:
* **Signal Processing:** One signal acting as a weight for another signal that slides along it.
* **Statistical:** A cross-covariance (assuming symmetry or accounting for the flip).
* **Geometric:** A time series of mappings between two vectors.
* **Functional:** A **frequency filter** (isolating specific frequencies in the time domain).

---

### II. Statistical Perspective
**Core Concept:** Convolution defines the probability distribution of the **sum** of independent random variables.

#### 1. Sum of Random Variables
* Given two independent random variables \\( X \\) and \\( Y \\) with probability density functions (PDFs) \\( f_X \\) and \\( f_Y \\).
* Let \\( Z = X + Y \\).
* The PDF of \\( Z \\) is the convolution of the PDFs of \\( X \\) and \\( Y \\):

$$
f_Z(z) = (f_X \ast f_Y)(z)
$$

#### 2. The Integral Formulation

$$
f_Z(z) = \int_{-\infty}^{\infty} f_X(x) \cdot f_Y(z-x) \, dx
$$

* **Connection to Signal Processing:**
    * The term \\( f_Y(z-x) \\) contains the same "Flip and Shift" mechanics found in signal theory.
    * **Flip:** \\( -x \\) (the variable is negated/reversed).
    * **Shift:** \\( z \\) (the variable is shifted by the total sum).

---

### III. Common Properties: Smoothing
In both domains, convolution acts as a smoothing operator.
* **In Signals:** Convolving a sharp signal with a broad kernel smoothes out high-frequency noise (Low-pass filtering).
* **In Statistics:** Adding random variables increases uncertainty (variance). The resulting distribution \\( Z \\) is wider and flatter than the constituent distributions \\( X \\) or \\( Y \\).

**Source:** Cohen, M. X. *Analyzing Neural Time Series Data: Theory and Practice*. The MIT Press, Cambridge, Massachusetts, 2014. (Chapter 10).