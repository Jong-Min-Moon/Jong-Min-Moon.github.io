---
layout: distill
title: "Paper review: Denoising Diffusion Probabilistic Models"
description: "A summary of Ho et al. (2020) on high-quality image synthesis using diffusion models."
date: 2026-07-25
categories: data-fusion machine-learning
tags: diffusion-models generative-ai
project: data-fusion
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Introduction
  - name: The Forward Process
  - name: The Reverse Process
  - name: Loss Function and Score Matching
  - name: Results
bib_file: data-fusion
paper_key: ho2020denoising
---

# The task
- We want to do nonparametric density estimation. 
- We want to learn a density $q(x_0)$.
- Rather than learning a closed form formulation of $q(x_0)$ for given $x_0$. We want a program that generates samples from $q(x_0)$. Having this program is equivalent to having the analytic form of $q(x_0)$.

# Neural network
- We will be nonparametric. We know that nonparametric methods are actually non nonparametric, they just use complex basis functions.
- So we use neural net to approximate $q(x_0)$. We denote that approximation as $p_\theta(x_0)$ where $\theta$ denotes the neural net weight.
- Again, we do not aim to write down $p_\theta(x_0)$ for given $x_0$. Instead we want a program that generates samples from $p_\theta(x_0)$.

# Modeling 1: Reverse Process
- Let's just forget the name reverse process. This is just all about modeling of the structure of the density function so that the estimation is tractable.


- Diffusion models assumes that $p_\theta(x_0)$ can be written as a latent variable model of the form 

$$p_\theta(x_0) := \int p_\theta(x_{0:T}) dx_{1:T}$$

- So our new task is, statistically:
> We want to learn the joint distribution $p_\theta(x_{0:T})$ from just observing $x_0$.

- From ML perspective, the task is:
> We want to use neural net to write a program that draws samples from $p_\theta(x_{0:T})$.

- To simplify the problem we assume Gaussian markov chain structure on $p_\theta(x_{0:T})$. That is:
  - $p(x_T) = \mathcal{N}(x_T; 0, I)$ (start from unconditional pure Gaussian noise)
  - $p_\theta(x_{t-1}|x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$ ($t-1$ step latent variable is only determined by previous latent variable $x_t$ and timestep $t$. And it is Gaussian distribution)
- Therefore, $p_\theta(x_{0:T}) := p(x_T) \prod_{t=1}^T p_\theta(x_{t-1}|x_t)$.
- Our goal is to use neural network to learn functions $\mu_\theta$ and $\Sigma_\theta$.
- After we learned that, the sample generating program works as:
  - Generate a random vector from standard multivaraite normal
  - sequentially draw Guassian random vectors based on previous latent variable sample and timestep.
- We call the joint distribution $p_\theta(x_{0:T})$ as the *reverse process*.

# Modeling 2: Forward process assumption
- We add the second assumption on $p_\theta(x_{0:T})$.
- Let us denote the true joint distribution as $q(x_{0:T})$. So $p_\theta(x_{0:T})$ is an approximation of $q(x_{0:T})$.
- Since we can observe $x_0$, we can think of $q(x_{1:T}|x_0)$. This is a posterior distribution. This is just a transformation of the estimation target.
- We assume that this posterior distribution is Guassian markov chain:
$$q(x_{1:T}|x_0) := \prod_{t=1}^T q(x_t|x_{t-1}), \quad q(x_t|x_{t-1}) := \mathcal{N}(x_t; \sqrt{1 - \beta_t}x_{t-1}, \beta_t\mathbf{I})$$
where $\beta_t$ is a variance schedule and we assume it is given. We will not learn it.

# Main idea
If we can incrementally add gaussian noise to obtain completely pure gaussian distribution, then reversely, we can start from pure gaussian distribution sample to recover the original data.

This is possible because, if the added noise is gaussian, then for infinitesimally small time interval, reverse process is also gaussian distribution.
 
# Introduction
Denoising Diffusion Probabilistic Models (DDPM) introduced by Ho et al. present a class of latent variable models inspired by nonequilibrium thermodynamics. They demonstrated that diffusion models are capable of generating high-quality images that rival and sometimes surpass state-of-the-art Generative Adversarial Networks (GANs).

# The Forward Process
The forward process, or diffusion process, is a Markov chain that gradually adds Gaussian noise to the data over $T$ timesteps. Given an initial data point $x_0 \sim q(x_0)$, the process defines a sequence of noisy variables $x_1, x_2, \dots, x_T$ according to a fixed variance schedule $\beta_1, \dots, \beta_T$:

$$q(x_t \mid x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t \mathbf{I})$$

As $t \to T$, the data distribution is completely destroyed, and $x_T$ approximates an isotropic Gaussian distribution.

# The Reverse Process
The goal of the generative model is to learn the reverse process, which is also modeled as a Markov chain with learned Gaussian transitions. Starting from $x_T \sim \mathcal{N}(0, \mathbf{I})$, the model denoises the variable step-by-step to recover a sample from the original data distribution:

$$p_\theta(x_{t-1} \mid x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

The neural network is tasked with predicting the mean $\mu_\theta$, or equivalently, the noise $\epsilon_\theta$ that was added to the data at timestep $t$.

# Loss Function and Score Matching
Training the model involves optimizing the variational lower bound (VLB) on the negative log-likelihood. However, the authors proposed a simplified objective that improves sample quality. Instead of predicting the mean directly, the network $\epsilon_\theta$ predicts the noise component:

$$L_{\text{simple}}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \left[ \| \epsilon - \epsilon_\theta(\sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, t) \|^2 \right]$$

This objective reveals a deep connection between diffusion models and denoising score matching with Langevin dynamics. The network $\epsilon_\theta$ essentially learns the score function $\nabla_x \log p_t(x)$ of the smoothed data distribution.

# Results
The DDPM model achieved remarkable success in unconditional image synthesis. On the CIFAR-10 dataset, it obtained an Inception score of 9.46 and a state-of-the-art Fréchet Inception Distance (FID) of 3.17. The model also generated high-quality samples on the 256x256 LSUN dataset, proving that diffusion models can produce results comparable to, and structurally superior to, ProgressiveGANs.


# References
- https://velog.io/@js43o/Diffusion-Model-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-with-DDPM
