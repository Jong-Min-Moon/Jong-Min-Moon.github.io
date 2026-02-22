---
layout: distill
title: "Nonlinear Mixed-Effects Modeling"
description: "An overview of Nonlinear Mixed-Effects Models (NLME), their structure, and workflow using SimBiology."
date: 2021-11-10
categories: glmm statistics
tags: nlme mixed-effects statistics
project: glmm
img: assets/img/publication_preview/glmm.png
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: Yonsei University
toc:
  - name: Repeated Measurement in Pharmacokinetics
  - name: The Goal of Population PK Modeling
  - name: Need for Mixed-Effects Models
  - name: Mixed-Effect Modeling in Population PK
  - name: General NLME Model Structure
  - name: Modeling Workflow
---

## Repeated Measurement in Pharmacokinetics

Pharmacokinetics (PK) is the study of how the body handles a drug over time—specifically its absorption, distribution, metabolism, and excretion. It essentially characterizes "what the body does to the drug." Since these biological processes are dynamic, drug handling is not instantaneous; it evolves over time. Consequently, we must measure drug concentration at multiple time points to fully understand the PK profile.

Let's define our variables:
- Let $i=1, \ldots, N$ denote the subject index.
- Let $j=1, \ldots, n_i$ denote the time point index for the $i$-th subject.
- $y_{ij}$ represents the measured drug concentration for the $i$-th subject at time $t_{ij}$.

Our basic dataset consists of these repeated measurements: $(y_{ij}, t_{ij})$.

## Population PK Modeling b

The primary goals of population PK modeling are twofold:
1.  **Describe the Trajectory**: Determine how the drug concentration $y_{ij}$ changes as a function of time $t_{ij}$. This requires the main modeling.
2.  **Explain Variability**: Understand how individual characteristics influence this trajectory. This requires modifying the main modeling just a little bit.

To address the first goal, we need a structural model. A common choice for PK data is the exponential decay function, as many drugs are eliminated from the body in an exponential fashion after distribution. A basic one-compartment model can be described as:

$$
y_{ij} = \frac{D_i}{V} e^{-k_i t_{ij}} + \epsilon_{ij}
$$

Here:

$D_i$ is the dose administered to the $i$-th individual.

$V$ is the **Volume of Distribution**, which represents the apparent volume into which the drug distributes (think of it as the "tank size"). A small $V$ (e.g., 3–5 L) suggests the drug remains in the bloodstream, while a large $V$ implies extensive tissue binding, making the apparent volume much larger than the body itself.

$k_i$ is the **Elimination Rate**, which determines how fast the drug is removed.

$\epsilon_{ij} \sim N(0, \sigma^2)$ represents measurement error.

The elimination rate $k_i$ is often parameterized as the ratio of **Clearance** ($Cl_i$) to Volume ($V$):
$$ k_i = \frac{Cl_i}{V} $$
where $Cl_i$ represents the volume of blood cleared of the drug per unit time (think of it as "blood cleaning speed"). Note that $k_i$ and $Cl_i$ are patient-specific parameters, allowing for individual variability.

## Need for Mixed-Effects Models

In repeated measurement data, observations from the same individual ($y_{i1}, y_{i2}, \dots$) are correlated, violating the independence assumption of standard regression models.

To handle this, we have two extreme approaches:
1.  **Pool all data**: Fit a single regression model to all data points, ignoring individual correlations. This obscures important inter-individual differences.
2.  **Individual fits**: Fit a separate regression model for each individual. This requires a large number of data points per subject, which is often unavailable in clinical trials or sparse biological datasets.

**Mixed-effects models** offer a compromise. They recognize correlations within sample subgroups (individuals) and allow us to make broad inferences on population-wide parameters (fixed effects) while estimating individual-specific deviations (random effects). This approach allows for robust estimation even with sparse data per subject.

## Mixed-Effect Modeling in Population PK

To model the biological variation between individuals, we treat parameters like clearance ($Cl$) as random variables that vary around a population mean.

We split the parameter into a **fixed effect** (population mean) and a **random effect** (individual deviation). For the $i$-th individual, we can model clearance as:

$$
Cl_i = \theta_{Cl} + \eta_i
$$

*   $\theta_{Cl}$: Fixed effect (the typical clearance value for the population).
*   $\eta_i$: Random effect (the specific deviation for subject $i$).

We typically assume deviations are normally distributed: $\eta_i \sim N(0, \sigma^2_\eta)$. This formulation allows us to capture heterogeneity without estimating a completely free parameter for every individual.

### Incorporating Covariates
We can further refine the model by adding individual-specific covariates (e.g., weight, age, renal function) to explain some of the inter-individual variability. Ideally, this reduces the unexplained variance in the random effect.

For example, if clearance is related to weight ($w_i$), we can expand the model:

$$
Cl_i = \theta_{Cl} + \theta_{wt} \cdot w_i + \eta_i
$$

Here, $\theta_{wt}$ is the fixed effect quantifying the relationship between weight and clearance.

## General NLME Model Structure

A general Nonlinear Mixed-Effects (NLME) model can be mathematically formulated as follows:

$$
y_{ij} = f(x_{ij}, p_i) + \epsilon_{ij} \\
p_i = A_i \theta + B_i \eta_i \\
\epsilon_{ij} \sim N(0, \sigma^2) \\
\eta_i \sim N(0, \Psi)
$$

Where:
*   $y_{ij}$: Response vector (e.g., drug concentration).
*   $f(\cdot)$: Nonlinear function governing the process (e.g., the PK compartmental equations).
*   $p_i$: Vector of individual-specific parameters (e.g., $Cl_i, V_i$).
*   $\theta$: Vector of fixed effects (population parameters).
*   $\eta_i$: Vector of random effects, assumed $\eta_i \sim MVN(0, \Psi)$.
*   $A_i, B_i$: Design matrices linking covariates and random effects to individual parameters.
*   $\Psi$: Covariance matrix quantifying the between-subject variability.
*   $\sigma^2$: Residual error variance.

## Modeling Workflow

Estimating these models involves determining the fixed effects $\theta$, the random effect covariance $\Psi$, and residual variance $\sigma^2$. Software like MATLAB's **SimBiology** facilitates this process using Maximum Likelihood Estimation.

A typical workflow involves:

1.  **Import & Format**: Load data and convert to `groupedData` format.
2.  **Structural Model**: Define the compartmental model (e.g., distribution and elimination kinetics).
3.  **Covariate Model**: Specify relationships between parameters and covariates (e.g., Weight on Clearance).
4.  **Error Model**: Choose an error structure (Constant, Proportional, or Combined) for $\epsilon_{ij}$.
5.  **Estimation**: Use algorithms (like FOCE, stochastic EM) to maximize the likelihood function:
    $$ p(y | \theta, \sigma^2, \Psi) = \int p(y | \theta, \eta, \sigma^2) p(\eta | \Psi) \, d\eta $$

This approach allows for rigorous quantification of drug behavior across populations, supporting dose optimization and clinical decision-making.
