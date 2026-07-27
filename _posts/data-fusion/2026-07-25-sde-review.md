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


# Score-Based Generative Models

**One-Liner:** Knowing the score function is equivalent to knowing the probability density *up to a normalization constant*. Consequently, if we can estimate the score, we can generate samples from the underlying true distribution (subject to discretization error).

## The Score Function

* **Definition:** The "score" is defined as the gradient of the log-likelihood with respect to the data.
* **Crucial Distinction:** Note that the gradient is taken with respect to the data vector $x$, not the model parameters $\theta$ (unlike the traditional Fisher score).
* **Geometric Intuition:** The score function acts as a vector field mapping any data point $x$ to a gradient vector that points in the direction of the steepest increase in data likelihood:

$$s(x) := \nabla_x \log p(x)$$



**2. Continuous Dynamics: Langevin Diffusion**
The theoretical foundation of sampling via scores relies on a continuous-time Stochastic Differential Equation (SDE) known as Langevin Diffusion:


$$dx_t = \nabla_x \log p(x_t) dt + \sqrt{2} dW_t$$

* **Components:** The drift term pulls the data toward high-density regions (using the score), while $W_t$ (standard Brownian motion) injects noise to ensure full exploration of the distribution.
* **Exact Sampling:** Under mild regularity conditions (e.g., $p(x)$ is strictly log-concave and smooth), the continuous-time process $x_t$ has $p(x)$ as its exact stationary (invariant) distribution. Simulating this SDE as $t \to \infty$ yields exact samples from $p(x)$.

**3. Practical Implementation: Langevin Monte Carlo (LMC)**
Because we cannot simulate continuous time in practice, we use Langevin Monte Carlo, which is the numerical discretization (Euler-Maruyama method) of the Langevin Diffusion SDE:


$$x_k := x_{k-1} + \alpha \nabla_x \log p(x_{k-1}) + \sqrt{2\alpha} u_k, \quad u_k \sim \mathcal{N}(0, I)$$

* **Mechanism:** By sequentially shifting the data in the direction of the score ($\alpha \nabla_x \log p(x_{k-1})$) while simultaneously injecting scaled Gaussian noise ($\sqrt{2\alpha} u_k$), we traverse the space to generate highly plausible samples.
* *Note: Because of the discrete step size $\alpha > 0$, this introduces a discretization bias, meaning we are sampling from an approximation of $p(x)$ unless Metropolis-Hastings corrections are applied.*

**Conclusion**
The paradigm of implementing a generative model by training a neural network to approximate this vector field $s(x)$, rather than directly modeling the scalar probability mass $p(x)$, is called a **Score-based Generative Model**.

---

Would you like to expand these notes to include how Score Matching (specifically Denoising Score Matching) is actually used to train the neural network to approximate $s(x)$?

---

**A quick statistical note on the translation:**
Your text perfectly captures the intuition of **Langevin Dynamics**. In statistical physics and MCMC literature, the term $\alpha \nabla_x \log p(x_{k-1})$ pulls the sample toward the mode of the distribution (Gradient Ascent), while the injected noise $\sqrt{2\alpha} u_k$ prevents the sample from collapsing into a single point (point mass), ensuring it properly explores the full variance of the target distribution $p(x)$.

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
