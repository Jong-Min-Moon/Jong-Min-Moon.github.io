---
layout: distill
title: "Paper review: Building Representative Matched Samples With Multi-Valued Treatments in Large Observational Studies"
description: "A review of Magdelena Bennett et al. (2020) on using mixed-integer optimization to create representative matched samples for multi-valued treatments."
date: 2026-02-22
categories: ml_mio optimization statistics
tags: causal-inference mixed-integer-programming matching-methods benchmarking
project: ml_mio
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Problem Setting
  - name: Optimization Framework
  - name: Key Innovations
  - name: Computational Efficiency
---

## Problem Setting

Without loss of generality, we focus on a single treatment level, as the matching procedure remains identical across all levels.

### Datasets
The study involves units (e.g., students) defined by an outcome, a treatment status, and a set of covariates. We consider $P$ **categorical** covariates, $\mathcal{P} = \{p_1, \ldots, p_P\}$. Note that continuous variables, such as household income, are discretized into categories in this paper.

In the paper's running example, the covariates include categorical variables such as gender, ethnicity, parental education levels, and household income. While each covariate in practice has a distinct number of levels, for ease of exposition we assume that each has exactly $K$ categories. Accordingly, each unit $i$ is represented by a covariate vector, for example, $\mathbf{x}_i \in [K]^P$.


The data is organized into two distinct sets:
1.  **Treatment Dataset ($\mathcal{L}$):** Units that received the specific treatment level under study. We denote this set as $\mathcal{L} = \{\ell_1, \ldots, \ell_L\}$. For example, a unit $\ell_1$ consists of an outcome $y_{ell_1}$, treatment $A_{ell_1}$ and a covariate vector $\mathbf{x}_{\ell_1}$. For matching stage, we only care about the covariate vector $\mathbf{x}_{\ell_1}$.
2.  **Template Dataset ($\mathcal{T}$):** A sample drawn from the population that represents the target covariate distribution. We denote this set as $\mathcal{T} = \{t_1, \ldots, t_T\}$. Since this dataset is genereated for the matching purpose,  we only care about the covariate vector $\mathbf{x}_{t_1}$.

### Problem Coefficients
For each covariate $p \in \{1, \dots, P\}$ and category $k \in \{1, \dots, K\}$, we define:
*   **$N_{p,k}$:** The number of units in the **template dataset** $\mathcal{T}$ that belong to category $k$ of covariate $p$. These represent our target counts for a representative sample.

### Decision Variables
The optimization model uses two types of variables:
*   **$m_{t,\ell} \in \{0, 1\}$:** A binary indicator that is $1$ if template unit $t \in \mathcal{T}$ is matched to treated unit $\ell \in \mathcal{L}$, and $0$ otherwise.
*   **$v_{p,k} \geq 0$:** A continuous variable representing the "cell count margin"—the absolute difference between the number of matched treated units and the target count $N_{p,k}$. Our goal is to minimize the sum of these margins.

### Constraints
The core logic of the model is captured in the following constraints:

1.  **Count Balance:** This constraint connects the matching decisions ($m$) to the discrepancy margins ($v$):
    $$| \sum_{\ell \in \mathcal{L}_{p,k}} \left( \sum_{t \in \mathcal{T}} m_{t,\ell} \right) - N_{p,k} | \leq v_{p,k}$$
    where $\mathcal{L}_{p,k}$ is the subset of treated units possessing category $k$ of covariate $p$.

2.  **Matching Requirements:** These ensure a valid one-to-one mapping without replacement:
    *   Each treated unit is matched at most once: $\sum_{t \in \mathcal{T}} m_{t,\ell} \leq 1, \quad \forall \ell \in \mathcal{L}$
    *   Each template unit is matched exactly once: $\sum_{\ell \in \mathcal{L}} m_{t,\ell} = 1, \quad \forall t \in \mathcal{T}$

### Analogy: Filling the Grid
Imagine a grid of size $P \times K$ where each cell represents a specific covariate category. The template units are already distributed across these cells. The matching process is like "filling" these cells with treated units to mirror the template's distribution as closely as possible.

```mermaid
graph TD
    subgraph Grid ["Grid: P Covariates x K Categories"]
        Cell1 ["Cell (1,1): Target N_1,1"]
        Cell2 ["Cell (1,2): Target N_1,2"]
        Cell3 ["..."]
        Cell4 ["Cell (P,K): Target N_P,K"]
    end

    TreatedPool ["Treated Pool (L)"] -- "Matched via m_t,l" --> Grid
    
    style Grid fill:#f9f9f9,stroke:#333,stroke-width:2px
    style TreatedPool fill:#e1f5fe,stroke:#01579b
```

By minimizing $\sum v_{pk}$, we ensure that the final "population" of matched treated units is a representative reflection of the template.
