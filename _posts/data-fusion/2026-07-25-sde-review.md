---
layout: distill
title: "Paper review: Score-Based Generative Modeling through SDEs"
description: "A summary of Song et al. (2021) which generalizes DDPMs and Score Matching into a unified continuous-time SDE framework."
date: 2026-07-25
categories: data-fusion machine-learning
tags: diffusion-models generative-ai sde
project: data-fusion
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Introduction
  - name: Forward SDE
  - name: Reverse SDE
  - name: Probability Flow ODE
bib_file: data-fusion
paper_key: song_scorebased_2021
---

# Introduction
Score-Based Generative Modeling through Stochastic Differential Equations (Song et al., 2021) is a seminal paper that elegantly unifies two major classes of generative models: Denoising Diffusion Probabilistic Models (DDPMs) and Noise Conditioned Score Networks (NCSNs). By taking the limit as the number of discrete noise scales approaches infinity, the authors show that both methods are discretizations of a continuous-time Stochastic Differential Equation (SDE).

# Forward SDE
In the continuous-time framework, the discrete sequence of noisy variables $x_t$ is replaced by a continuous stochastic process $\{x(t)\}_{t \in [0, T]}$. This process is described by an Itô SDE:

<p>$$dx = f(x, t)dt + g(t)dw$$</p>

- $f(x, t)$ is the drift coefficient.
- $g(t)$ is the diffusion coefficient.
- $w$ is standard Brownian motion.

By carefully choosing $f$ and $g$, this SDE slowly perturbs the data distribution $p_0(x)$ at $t=0$ into a tractable prior distribution $p_T(x)$ at $t=T$ (e.g., standard Gaussian).

# Reverse SDE
The magic of this formulation lies in Anderson's theorem, which states that any SDE has a corresponding reverse-time SDE. Starting from samples in the prior distribution $x(T) \sim p_T(x)$, we can reverse the diffusion process to generate data $x(0) \sim p_0(x)$ by simulating:

<p>$$dx = [f(x, t) - g(t)^2 \nabla_x \log p_t(x)]dt + g(t)d\bar{w}$$</p>

Here, $\bar{w}$ is a reverse-time Brownian motion. The critical term is the score function $\nabla_x \log p_t(x)$. We parameterize a neural network $s_\theta(x, t)$ to approximate this score using a continuous-time score matching objective. 

# Probability Flow ODE
An astonishing theoretical result of this paper is that for any SDE describing a diffusion process, there exists a deterministic Ordinary Differential Equation (ODE) whose trajectories share the exact same marginal probability densities $p_t(x)$ at every time $t$:

<p>$$dx = \left[ f(x, t) - \frac{1}{2}g(t)^2 \nabla_x \log p_t(x) \right] dt$$</p>

This is known as the Probability Flow ODE. This ODE enables exact likelihood computation using the instantaneous change of variables formula, bridging the gap between diffusion models and continuous normalizing flows!
