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


# The task

* Nonparametric conditional density estimation: we want to learn a conditional density $P(X_0 = x \vert{} y)$. The variable $y$ is our condition (e.g., a class label, or text embedding). A very traditional task.
* Rather than learning a closed-form formulation of $P(x\vert{}y)$ for a given $x$ and $y$, we want a program that generates samples from $P(\cdot \vert{} y)$. Having this program is equivalent to having the analytic form of the conditional density.

# Statistical Modeling: Forward Process

* In standard diffusion models, we used discrete Markov chains. Here, we generalize the data generating process to continuous time using Stochastic Differential Equations (SDEs).
* This structure is an assumption on the forward data corruption process. We consider adding noise progressively to $X_0$, while leaving the condition $y$ untouched.
* This corruption is described by a forward Ornstein–Uhlenbeck (OU) process:

* Here, $W_t$ is a standard Wiener process.
* In the infinite-time limit ($t \to \infty$), $X_\infty$ converges to a standard Gaussian distribution $\mathcal{N}(0, I)$, completely wiping out the information from both $x$ and $y$.
* At any finite time $t$, the transition kernel from $x_0$ to $x_t$ is Gaussian, denoted as $\phi_t(x'\vert{}x_0)$. Its score (the gradient of the log density) has a known closed form: $\nabla_{x'} \log \phi_t(x'\vert{}x_0) = -(x' - \alpha_t x_0)/\sigma_t^2$, where $\alpha_t = e^{-t/2}$ and $\sigma_t^2 = 1 - e^{-t}$.

# Statistical Modeling: Reverse Process

* Just like the discrete case, to generate new samples we must reverse time. By stochastic calculus, the reverse of the forward OU process is another SDE:

* We use the arrow on $\overleftarrow{X}$ and $\overleftarrow{W}$ to emphasize that time is flowing backward from a large terminal time $T$ down to $0$.
* Look closely at the drift term in the brackets. The only unknown piece in this entire differential equation is the **conditional score function**: $\nabla \log p_{T-t}(X\vert{}y)$.
* So our new task is, statistically:

> We want to estimate the conditional score function $\nabla \log p_t(x\vert{}y)$ from our data. If we have this, we can solve the SDE backwards to generate samples.

# Neural network & Classifier-free guidance

* We will use a neural network to approximate this conditional score. We denote that estimator as $\hat{s}(x, y, t)$.
* However, the current state-of-the-art approach introduces **Classifier-Free Guidance (CFG)**.
* CFG suggests that instead of *just* learning the conditional score, we should simultaneously learn the *unconditional* score. We define two theoretical estimators:
* $s_1(x, y, t)$ to estimate the conditional score $\nabla \log p_t(x\vert{}y)$
* $s_2(x, t)$ to estimate the unconditional score $\nabla \log p_t(x)$


* To unify this into a single neural network architecture, we introduce a mask signal $\tau \in \{\emptyset, \text{id}\}$.
* $\emptyset$ means we drop the guidance $y$.
* $\text{id}$ means we keep the guidance $y$.


* Now, our neural network is a unified tri-variate function $s(x, \tau y, t)$, where it acts as $s_1$ when the mask is $\text{id}$, and acts as $s_2$ when the mask is $\emptyset$.

# Training in Practice

* The true score $\nabla \log p_t(x\vert{}y)$ is intractable, but thanks to score matching theory, minimizing the distance to the true score is mathematically equivalent to minimizing the distance to the score of the forward transition kernel $\nabla_{x'} \log \phi_t(x'\vert{}x_0)$, which we know exactly!
* During training, we randomly mask out the condition $y$. For simplicity, assume a uniform prior: $P(\tau = \emptyset) = P(\tau = \text{id}) = 0.5$.
* We integrate over time from an early-stopping time $t_0$ (to prevent the score from blowing up near $t=0$) to $T$. The unified population risk is:

* In practice, we don't have the population distribution; we have an i.i.d. dataset of size $n$, $\{(x_i, y_i)\}_{i=1}^n$.
* For a single data point, the loss function $\ell(x, y; s)$ evaluates the expected score matching error across timesteps and mask signals:

* Therefore, the Empirical Risk Minimization (ERM) problem we actually feed into our PyTorch optimizer is:

# My understanding

The discrete-time formulation frames diffusion as "predicting the noise," while the continuous-time SDE formulation frames it as "score matching." Mathematically, they are sides of the same coin, but the SDE viewpoint makes the transition to conditional generation highly elegant.

Classifier-free guidance essentially acts as a structured data augmentation trick at the architecture level. By randomly zeroing out $y$ during the creation of our on-the-fly training batches, a single neural network is forced to learn both the conditional density and the marginal density simultaneously. At inference time, this allows us to extrapolate between the unconditional and conditional score predictions, pushing the SDE generation stronger in the direction of $y$ without ever needing a separate classifier model.