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

<p>$$p_\theta(x_0) := \int p_\theta(x_{0:T}) dx_{1:T}$$</p>

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
- Because we define a parameterized generative model $p_\theta(x_{0:T})$, it possesses its own true posterior $p_\theta(x_{1:T}\vert{}x_0)$. 
- However, integrating over high-dimensional continuous latent spaces to find this true posterior is mathematically intractable.
- We introduce $q(x_{1:T}\vert{}x_0)$ as a tractable, pre-defined distribution (the forward process) to approximate the intractable true posterior. So this part is ASSUMPTION, or modeling. This structure is not learned from data. It came from the author's mind.

<p>$$q(x_{1:T}|x_0) := \prod_{t=1}^T q(x_t|x_{t-1}), \quad q(x_t|x_{t-1}) := \mathcal{N}(x_t; \sqrt{1 - \beta_t}x_{t-1}, \beta_t\mathbf{I})$$</p>
where $\beta_t$ is a variance schedule and we assume it is given. We will not learn it.


# Training: KL divergence
- We have samples from posterior, $q(x_{1:T}|x_0)$. Actually we have all samples in the intermediate steps.

- Just as MLE maximizes sample mean of log likelihood, here we minimize sample mean of negative log likelihood.

- The negative log likelihood is hard to compute, so we minimize its upper bound.

- with some algbra, the loss function we minimze is
<p>$$L = \mathbb{E}_q \left[ DKL(q(x_T |x_0) ‖ p(x_T )) + \sum_{t>1} DKL(q(x_{t-1}|x_t, x_0) ‖ p_\theta(x_{t-1}|x_t)) - \log p_\theta(x_0|x_1) \right]$$</p>

 
- $\mathbb{E}_q$ means sample average from samples drawn from distributon $q$. the forward process.

- It is the negative Evidence Lower Bound (ELBO). Let's evaluate the three components:
  - $D_{KL}(q(x_T \vert{}x_0) \Vert{} p(x_T ))$: This term has no learnable parameters $\theta$. It is the distance between the final noisy data and a standard normal distribution. We assume $\beta_t$ is scheduled such that $q(x_T\vert{}x_0) \approx \mathcal{N}(0, I)$, making this term nearly zero. We ignore it during optimization.
  - $-\log p_\theta(x_0\vert{}x_1)$: This is the reconstruction term. It is modeled as a discrete decoder in practice, but conceptually, it is just the final step of the reverse process.
  - $\sum_{t>1} D_{KL}(q(x_{t-1}\vert{}x_t, x_0) \Vert{} p_\theta(x_{t-1}\vert{}x_t))$: This is the core of the diffusion model.

## Gaussian assumption: KL divergence to simple ERM
To minimize that summation of KL divergences. Notice that both distributions inside the KL divergence are Gaussian:$p_\theta(x_{t-1}\vert{}x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$q(x_{t-1}\vert{}x_t, x_0) = \mathcal{N}(x_{t-1}; \tilde{\mu}_t(x_t, x_0), \tilde{\beta}_t I)$

Because of the Markov property and properties of Gaussians, the forward process conditioned on $x_0$ has a beautifully tractable closed-form mean:<p>$$\tilde{\mu}_t(x_t, x_0) = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t}x_0 + \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t}x_t$$</p>(where $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$)

Since the KL divergence between two Gaussians with fixed variances is simply proportional to the $L_2$ distance between their means, minimizing the KL divergence is mathematically equivalent to solving the following least squares problem:
<p>$$\arg\min_\theta \Vert{} \tilde{\mu}_t(x_t, x_0) - \mu_\theta(x_t, t) \Vert{}^2$$</p>

Instead of predicting the mean directly, we can use the reparameterization trick. We know that $x_t$ is just a deterministic combination of $x_0$ and some pure noise $\epsilon \sim \mathcal{N}(0, I)$:<p>$$x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1 - \bar{\alpha}_t}\epsilon$$</p>If we substitute $x_0$ out of the $\tilde{\mu}_t$ equation using the formula above, and we parameterize our neural network to predict the noise $\epsilon_\theta(x_t, t)$ rather than predicting the mean $\mu_\theta$, the complex statistical KL divergence collapses into a remarkably simple empirical risk minimization problem:<p>$$L_{simple}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \left[ \Vert{} \epsilon - \epsilon_\theta(x_t, t) \Vert{}^2 \right]$$</p>


# My understanding
The names are forward and reverse. But the paper introduces reverse first, because reverse is the modeling of the density. forward is the modeling of training data generation.
# References
- https://velog.io/@js43o/Diffusion-Model-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-with-DDPM
