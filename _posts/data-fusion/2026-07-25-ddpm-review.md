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
