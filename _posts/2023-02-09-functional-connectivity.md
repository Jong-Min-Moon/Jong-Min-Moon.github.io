---
layout: post
title: "Fundamentals of Functional Connectivity and Gradients"
date: 2023-02-09
description: "Principle and practice of mapping the brain's functional architecture into a low-dimensional space."
project: autism-sex-differences
categories: research
---

## I. Functional Connectivity
In neuroscience, it is well established that brain regions cooperate within large-scale functional networks to support specific cognitive processes. Consequently, connectivity data has emerged as a fundamental modality for studying brain function.

There are three main types of brain connectivity:

| Connectivity Type | Description |
| :--- | :--- |
| **Functional Connectivity** | Investigates the **undirected** statistical dependence between separate brain regions characterized by similar temporal dynamics. It does not imply direct structural connection. |
| **Effective Connectivity** | Refers to the **directed, or causal** influence of one region over another. |
| **Structural Connectivity** | Investigates the **physical connections** (e.g., axons, white matter) between brain regions. |

Functional connectivities are inferred when signals from two separate regions fluctuate in synchrony. Basically, computing correlation. Signals can be from any modalities. For example:
*   **fMRI:** Functional magnetic resonance imaging (fMRI) provides an indirect measure of neuronal activity by evaluating changes in blood oxygenation over different areas of the brain. Good spatial resolution, low temporal resolution.
*   **EEG / MEG:** Measures **electrical/magnetic activity** directly. Excellent temporal resolution, lower spatial resolution.

 
 

## II. Functional Gradients: Low-Dimensional Representation

### 1. The High-Dimensionality Challenge
*   **The Problem:** Functional connectivity analysis generates a $p \times p$ matrix, where $p$ is the number of brain regions. If $p=400$, each region is defined by a complex 400-dimensional connectivity vector. This high-dimensional space is noisy, difficult to visualize, and computationally expensive to model.
*   **The Solution:** Dimensionality reduction techniques (e.g., PCA, t-SNE, Diffusion Mapping) are applied to extract the "dominant axes" of variance. These axes represent the underlying organizational principles of the brain.

### 2. What is a "Gradient"?
A **Functional Gradient** is a PC score. It is a continuous coordinate system for the brain. Instead of forcing regions into discrete "clusters", a gradient places every region along a continuous spectrum based on the similarity of their connectivity profiles.

### 3. Why use Functional Gradients?
It is low-dimensional but encodes the brain activity sufficiently well. For example, gradients provide a parsimonious representation of the **Cortical Hierarchy**, revealing the transition from sensation to abstraction:

*   **Efficiency:** They condense complex connectivity patterns into a single, biologically interpretable axis.
*   **The Principal Gradient (Cortical Hierarchy) distinguishes:**
    *   **Anchor 1: Unimodal (Low-Level):** Primary sensory/motor regions (e.g., Visual Cortex) that process immediate external stimuli.
    *   **Anchor 2: Transmodal (High-Level):** Association regions (e.g., Default Mode Network) involved in abstract, internal cognition like memory and planning.
    *   **Insight:** This gradient captures the fundamental biological principle of how the brain abstracts raw sensory data into high-level thought. 
---

## III. Data Acquisition Workflow 

This workflow moves beyond simple "Region A connects to Region B" analysis to map the macro-scale hierarchy of the brain.

### 1. Workflow Steps

1.  **Construct Connectivity Matrix:**
    *   *Input:* Time-series data for $p$ regions.
    *   *Operation:* Pearson correlation between all pairs.
    *   *Result:* **Symmetric, Dense Matrix**.
2.  **Row-wise Thresholding:**
    *   *Operation:* For each row, keep only the top 10% strongest connections.
    *   *Result:* **Sparse, Asymmetric Matrix**. (Asymmetry arises because being in A's top 10% doesn't guarantee A is in B's top 10%).
    *   *Purpose:* Filter out noise and weak correlations.
3.  **Affinity Matrix Calculation:**
    *   *Operation:* Compute **Cosine Similarity** between the sparse rows (connectivity profiles).
    *   *Question:* "Do Region A and Region B have similar 'friends' (connectivity patterns)?"
    *   *Result:* **Symmetric Affinity Matrix**. represents *contextual similarity*, not direct correlation.
4.  **Dimensionality Reduction:**
    *   *Operation:* Apply **Diffusion Map Embedding**.
    *   *Result:* **Principal Gradients**. Each region gets a coordinate/score along these axes.