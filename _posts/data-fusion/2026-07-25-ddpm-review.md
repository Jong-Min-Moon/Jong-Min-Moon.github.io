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
- Nonparametric density estimation: we want to learn a density $q(x_0)$. A very traditional task.
- Rather than learning a closed form formulation of $q(x_0)$ for given $x_0$. We want a program that generates samples from $q(\cdot)$. Having this program is equivalent to having the analytic form of $q(\cdot)$.

# Neural network
- We will be nonparametric. We know that nonparametric methods are actually   parametric, they just use complex basis functions.
- So we use neural net to approximate $q(x_0)$. We denote that approximation as $p_{\theta}(x_0)$ where $\theta$ denotes the neural net weight.
- Again, we do not aim to write down $p_{\theta}(x_0)$ for given $x_0$. Instead we want a program that generates samples from $p_{\theta}(\cdot)$.

# Statistical Modeling: Reverse Process
- For a moment, let's just forget the name *reverse process*. This is just all about modeling of the structure of the density function so that the estimation is tractable.

- This structure is an assumption on the data generating process. Therefore this part is exactly the statistical modeling. After we learn the parameters of this model, we can generate the data.


- Diffusion models assumes that $p_{\theta}(x_0)$ can be written as a latent variable model of the form 

<p>$$p_{\theta}(x_0) := \int p_{\theta}(x_{0:T}) dx_{1:T}$$</p>

- So our new task is, statistically:
> We want to learn the joint distribution $p_{\theta}(x_{0:T})$ from just observing $x_0$.

- From ML perspective, the task is:
> We want to use neural net to write a program that draws samples from $p_{\theta}(x_{0:T})$.

- To simplify the problem, we assume a Gaussian Markov chain structure on $p_{\theta}(x_{0:T})$. That is:
  - $p(x_T) = \mathcal{N}(x_T; 0, I)$ (start from unconditional pure Gaussian noise)
  - $p_{\theta} (x_{t-1}\, | \, x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$ (the $t-1$ step latent variable is only determined by the previous latent variable $x_t$ and timestep $t$, and it follows a Gaussian distribution)
- Therefore, $p_{\theta}(x_{0:T}) := p(x_T) \prod_{t=1}^T p_{\theta}(x_{t-1}|x_t)$.
- Our goal is to use a neural network to learn the functions $\mu_\theta$ and $\Sigma_\theta$.
- After learning this, the sample generating program works as follows:
  - Generate a random vector from a standard multivariate normal distribution.
  - Sequentially draw Gaussian random vectors based on the previous latent variable sample and timestep.
- We call the joint distribution $p_{\theta}(x_{0:T})$ the *reverse process*.

# Modeling 2: Forward process assumption
- We add the second assumption on $p_{\theta}(x_{0:T})$.
- Because we define a parameterized generative model $p_{\theta}(x_{0:T})$, it possesses its own true posterior $p_{\theta}(x_{1:T}\vert{}x_0)$. 
- However, integrating over high-dimensional continuous latent spaces to find this true posterior is mathematically intractable.
- We introduce $q(x_{1:T}\vert{}x_0)$ as a tractable, pre-defined distribution (the forward process) to approximate the intractable true posterior. So this part is ASSUMPTION, or modeling. This structure is not learned from data. It came from the author's mind.

<p>$$q(x_{1:T}|x_0) := \prod_{t=1}^T q(x_t|x_{t-1}), \quad q(x_t|x_{t-1}) := \mathcal{N}(x_t; \sqrt{1 - \beta_t}x_{t-1}, \beta_t\mathbf{I})$$</p>
where $\beta_t$ is a variance schedule and we assume it is given. We will not learn it.

# Training: KL Divergence

- We have samples from the posterior, $q(x_{1:T}|x_0)$. Actually, we have all samples in the intermediate steps.
- Just as MLE maximizes the sample mean of the log-likelihood, here we minimize the sample mean of the negative log-likelihood.
- The negative log-likelihood is hard to compute, so we minimize its upper bound.
- With some algebra, the loss function we minimize is:

<p>\begin{equation}L = \mathbb{E}_q \left[ D_{KL}(q(x_T |x_0) \Vert p(x_T )) + \sum_{t>1} D_{KL}(q(x_{t-1}|x_t, x_0) \Vert p_{\theta}(x_{t-1}|x_t)) - \log p_{\theta}(x_0|x_1) \right]\end{equation}</p>
 
- $\mathbb{E}_q$ represents the sample average from samples drawn from distribution $q$, the forward process.
- It is the negative Evidence Lower Bound (ELBO). Let's evaluate the three components:
  - $D_{KL}(q(x_T \vert x_0) \Vert p(x_T ))$: This term has no learnable parameters $\theta$. It is the distance between the final noisy data and a standard normal distribution. We assume $\beta_t$ is scheduled such that $q(x_T \vert x_0) \approx \mathcal{N}(0, I)$, making this term nearly zero. We ignore it during optimization.
  - $-\log p_{\theta}(x_0 \vert x_1)$: This is the reconstruction term. It is modeled as a discrete decoder in practice, but conceptually, it is just the final step of the reverse process.
  - $\sum_{t>1} D_{KL}(q(x_{t-1} \vert x_t, x_0) \Vert p_{\theta}(x_{t-1} \vert x_t))$: This is the core of the diffusion model.

## Gaussian Assumption: KL Divergence to Simple ERM

To minimize that summation of KL divergences, notice that both distributions inside the KL divergence are Gaussian:

<p>\begin{equation}p_{\theta}(x_{t-1} \vert x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))\end{equation}</p>

<p>\begin{equation}q(x_{t-1} \vert x_t, x_0) = \mathcal{N}(x_{t-1}; \tilde{\mu}_t(x_t, x_0), \tilde{\beta}_t I)\end{equation}</p>

Because of the Markov property and properties of Gaussians, the forward process conditioned on $x_0$ has a beautifully tractable closed-form mean:

<p>\begin{equation}\tilde{\mu}_t(x_t, x_0) = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t}x_0 + \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t}x_t\end{equation}</p>

(where $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$)

Since the KL divergence between two Gaussians with fixed variances is simply proportional to the $L_2$ distance between their means, minimizing the KL divergence is mathematically equivalent to solving the following least squares problem:

<p>\begin{equation}\arg\min_\theta \Vert \tilde{\mu}_t(x_t, x_0) - \mu_\theta(x_t, t) \Vert^2\end{equation}</p>

Instead of predicting the mean directly, we can use the reparameterization trick. We know that $x_t$ is just a deterministic combination of $x_0$ and some pure noise $\epsilon \sim \mathcal{N}(0, I)$:

<p>\begin{equation}x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1 - \bar{\alpha}_t}\epsilon\end{equation}</p>

If we substitute $x_0$ out of the $\tilde{\mu}_t$ equation using the formula above, and we parameterize our neural network to predict the noise $\epsilon_\theta(x_t, t)$ rather than predicting the mean $\mu_\theta$, the complex statistical KL divergence collapses into a remarkably simple empirical risk minimization problem:

<p>\begin{equation}L_{simple}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \left[ \Vert \epsilon - \epsilon_\theta(x_t, t) \Vert^2 \right]\end{equation}</p>

# Training in Practice
 - The *training data* is not simply a massive folder of pristine images, audio files, or molecular structures.
 - Those clean, ground-truth samples ($x_0$) are the foundational source material. However, they aren't the actual data pairs fed into the neural net training.
- Actaully, we create the training data on the fly: pairs of $(x_t, \epsilon)$ created from that original clean data and pure random noise.

 
### What the Pytorch Looks At

Unlike a standard image classifier that looks at a clean image, a diffusion model's core network takes in two distinct pieces of information during a forward pass:

1. **The Noisy Data ($x_t$):** This is the corrupted version of the original data.
2. **The Timestep ($t$):** A scalar value telling the network *how corrupted* the data is (e.g., step 450 out of 1000). The network absolutely needs this context. Pulling noise out of a slightly blurry image requires a completely different mathematical transformation than pulling noise out of pure static.

### The Target: What the Network Tries to Predict
The math in this paper shows that the target label is:

* **The Actual Noise ($\epsilon$):** The exact, pure Gaussian noise matrix that was added to the clean data to create $x_t$.

### Building the Dataset on the Fly

One of the most elegant aspects of training a diffusion model is that you don't pre-compute and save terabytes of noisy intermediate images. Instead, the training loop generates the neural network's training pairs instantly in memory during every batch.

Here is the step-by-step anatomy of how this data is generated in a training iteration:

1. **Sample the Ground Truth:** Draw a clean, real data point ($x_0$) from your original dataset.
2. **Select a Timestep:** Randomly pick a timestep $t$ from a uniform distribution (e.g., $t \in [1, T]$).
3. **Generate the Target:** Sample pure random noise ($\epsilon$) from a standard normal distribution. This will be the ground truth for our loss function.
4. **Create the Input:** Mathematically mix $x_0$ and $\epsilon$ together using the closed-form forward process formula. Because of the properties of Gaussians, we don't have to simulate every step; we can jump directly to step $t$:
5. **Feed the Network:** Pass the newly minted noisy data ($x_t$) and the timestep ($t$) into the neural network.
6. **Calculate the Loss:** The network outputs its prediction of the noise ($\epsilon_\theta$). The loss is simply the Mean Squared Error between the network's prediction and the actual noise ($\epsilon$) drawn in step 3.

### The Infinite Stream

By shifting our perspective to the neural network's specific inputs and outputs, it becomes clear that the original dataset is merely a seed. The actual dataset being pushed through the optimizer is an infinite, constantly generated stream of `(noisy data, timestep) -> actual noise` mappings.

Because the noise and timesteps are sampled randomly, every time the model encounters the same underlying image $x_0$, it sees it corrupted by a completely different noise pattern at a different severity level. This dynamic generation is what prevents severe overfitting and allows the model to robustly learn the full reverse trajectory of generation.

# My understanding
The names are forward and reverse. But the paper introduces reverse first, because reverse is the modeling of the density. forward is the modeling of training data generation.
# References
- https://velog.io/@js43o/Diffusion-Model-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-with-DDPM
