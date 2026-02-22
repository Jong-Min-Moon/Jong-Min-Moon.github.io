---
layout: distill
title: "Lecture 16: Canonical Gradient and Efficient Influence Curve"
description: "Notes by Rachael Phillips for PB HLTH 290, Spring 2019"
date: 2026-02-20
categories: causal_inference statistics
tags: causal-inference asymptotic-efficiency efficiency-theory
project: causal_inference
authors:
  - name: Rachael Phillips
    affiliations:
      name: UC Berkeley
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Introduction
  - name: Setting
  - name: "Insight: The Geometry of Pathwise Derivatives"
  - name: Goal
  - name: Parametric submodels and scores
  - name: "Tangent Space, T(P)"
  - name: Problem with standard directional derivative of target parameter
  - name: Pathwise derivative
  - name: Class of gradients
  - name: Canonical gradient is projection of gradient on tangent space
---

## Introduction

An asymptotically linear estimator with influence curve equal to the efficient influence curve is optimal in the sense that there is no other asymptotically linear estimator with influence curve with a smaller variance. We call this estimator asymptotically efficient. 

## Setting

1. **Data and Model:**
   $$ O_1, \dots, O_n \overset{iid}{\sim} P_0 \in \mathcal{M}. $$
   Here, $$\mathcal{M}$$ denotes the statistical model, which is the collection of all possible probability distributions $$P$$ that could generate the data.

2. **Target Parameter:**
   The target parameter is defined as a functional (or operator) $$\Psi: \mathcal{M} \to \mathbb{R}$$. This mapping takes a probability distribution $$P$$ as input and returns a scalar value representing a specific feature of that distribution (e.g., the mean, the risk difference).

3. **Estimand:**
   The true value of the parameter, often denoted as $$\psi_0 = \Psi(P_0)$$, is the **estimand**. This is an unknown quantity because the true data-generating distribution $$P_0$$ is unknown.

## Insight: The Geometry of Pathwise Derivatives

**The Problem: The "Straight Line" Fallacy.**
We want to measure the sensitivity ("steepness") of the functional $$\Psi$$ at the distribution $$P$$. In standard calculus, we would simply take a derivative along a straight line ($$P + \epsilon Q$$). However, the space of probability distributions is curved, not flat (it is not a vector space). If we try to walk in a straight line off of $$P$$, we immediately land in "invalid territory" (e.g., generating negative probabilities or measures that do not sum to one).

**The Solution: The Curve-Drawing Machine.**
To stay within the valid distribution space, we approach $$P$$ along smooth curves. We utilize a **parametric submodel**, constructed by a **curve-drawing machine** $$P_\epsilon^h$$.
*   **Input:** We feed it a "drawing parameter" $$h$$ (a function), which determines the style or direction of the curve.
*   **Action:** As we vary $$\epsilon$$, the machine draws a series of dots (probability distributions) inside the model space.
*   **Output:** The collection of these dots forms the curve $$\mathcal{M}_h(P)$$. By construction, every dot on this curve is a valid probability distribution passing through $$P$$ at $$\epsilon=0$$.

**The Mechanism: The Chain Rule Analogy.**
We want to calculate how the parameter $$\Psi$$ changes as we move along this curve. We can understand this via a **Chain Rule Analogy**. While the formal calculus of functionals is more complex, the intuition parallels standard calculus ($$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$):

$$
\underbrace{\frac{d}{d\epsilon} \Psi(P^h_\epsilon)}_{\text{Total Change}}\bigg|_{\epsilon=0} \approx \underbrace{\text{"Operator Change"}}_{\frac{d\Psi}{dP}} \cdot \underbrace{\text{"Curve Change"}}_{\frac{dP}{d\epsilon}}
$$

However, mathematically, the components are defined more precisely in the Hilbert space $$L_2(P)$$.

**Conclusion.**
The beauty of this approach is that we can separate the geometry of the model from the target parameter. We can pre-compute the "curve part" (the Score $$S_h$$) purely based on the submodel. When we combine it with the Gradient via the inner product, we recover the pathwise derivative we need to study efficiency.

## Goal

Our primary objective is to estimate the unknown quantity $$\psi_0 = \Psi(P_0)$$ and to understand the fundamental limits of estimation accuracy. The properties of the functional $$\Psi$$ itself dictate the difficulty of the estimation problem.

*   **Local Perturbations:** To quantify this difficulty, we analyze the behavior of $$\Psi$$ under local perturbations. We ask: "If the true distribution $$P_0$$ changes slightly, how much does the parameter $$\Psi(P_0)$$ change?"
*   **Derivatives and Variance:** This concept is analogous to a derivative in calculus. The "steepness" of this functional derivative (formally captured by the *Efficient Influence Function*) determines the *Information Bound*. A "steeper" functional implies that the parameter is more sensitive to fluctuations in the data, resulting in a harder estimation problem (higher minimum variance).

## Parametric submodels and scores

**Motivation: Valid Directions.**
When defining the derivative of a target parameter, we cannot simply look at arbitrary perturbations $$P + \epsilon h$$ (as in standard calculus). The resulting object $$P + \epsilon h$$ might not be a valid probability distribution (e.g., it might not integrate to 1 or could be negative). Therefore, we must restrict our attention to perturbations within the space of valid probabilities. We achieve this by defining *parametric submodels*.

### Parametric submodel, given h

For a specific path $$h$$, we define a one-dimensional parametric submodel passing through the true distribution $$P$$:

$$
\mathcal{M}_h(P) = \{ P^h_{\epsilon} : \epsilon \in (-\delta, \delta) \} \subset \mathcal{M}
$$

This submodel (collection of distributions) is a curve within the large model $$\mathcal{M}$$ such that:
*   At $$\epsilon = 0$$, the distribution is the true data-generating distribution: $$P^h_{\epsilon=0} = P$$.
*   For $$\epsilon>0$$, we move away from $$P$$ by $$\epsilon$$ in the direction $$h$$, while remaining inside the model $$\mathcal{M}$$.
*   The specific value of $$\delta$$ is not critical. We are only interested in the behavior of the submodel in the immediate neighborhood of $$\epsilon=0$$.
*   Form of $$P^h_{\epsilon}$$ is quite flexible. Not necessarily $$P+ \epsilon h$$. We are allowed to invent any path $$P_\epsilon$$ we want, as long as it passes through the true model $$P$$ at $$\epsilon=0$$. There is no single "correct" way to draw a line through a probability distribution.

### Score, given h

The only direction we care about each submodel, $$\mathcal{M}_h(P)$$, is its score. For a path $$h$$, its score $$S_h$$ is defined as a transformation of an observation: 

$$
S_h(O)=\left . \frac{d}{d\epsilon}\log dP_{\epsilon}^h/dP(O)\right |_{\epsilon=0}
$$

Notice that the score is defined as usual. We take the log of the density that is defined with respect to $$P$$ itself. In other words, you choose the path where all the probability distributions are of the same nature as $$P$$ itself so that you can define $$\frac{dP_{\epsilon}}{dP}$$. Then we have a collection of densities because $$\frac{dP_{\epsilon}}{dP} = p_{\epsilon}^h$$ so we have that $$S_h(O)=\frac{d}{d\epsilon}\log p_{\epsilon}^h |_{\epsilon=0}$$.

### Tangent space and Hilbert space

#### The Tangent Set (Class of Scores): class of h

We consider the class of all parametric submodels $$\{\mathcal{M}_h(P) : h \in \mathcal{H}\}$$, indexed by a set of paths $$\mathcal{H}$$. Let $$\mathcal{S} = \{ S_h : h \in \mathcal{H} \}$$ be the collection of all score functions generated by these paths. **We should be careful about $$\mathcal{H}$$**.

*   **Richness of $$\mathcal{H}$$:** We choose the index set $$\mathcal{H}$$ to be sufficiently "rich" to ensure coverage. This ensures that the set of scores $$\mathcal{S}$$ captures all possible local directions in which we can perturb $$P$$ while remaining within the constraints of the model $$\mathcal{M}$$.
*   **Tangent Space:** The set $$\mathcal{S}$$ (specifically, the closure of its linear span) is formally called the **Tangent Space** of the model at $$P$$. includes any function that can be approximated by limit of elements of the linear span

#### The Hilbert Space $$L_0^2(P)$$

**Scores as Random Variables.**
Scores are measurable functions of the data $$O \sim P$$. Therefore, they are random variables with specific properties:
*   **Mean Zero:** $$\mathbb{E}_P[S(O)] = 0$$.
*   **Finite Variance:** $$\mathrm{Var}_P[S(O)] < \infty$$.

**Hilbert Space.**
We define $$L^2_0(P)$$ as the Hilbert space containing all such mean-zero, square-integrable functions of $$O$$ (thus they are mostly correlated)

$$
L^2_0(P) = \{ f(O) : \mathbb{E}_P[f(O)]=0, \, \mathbb{E}_P[f(O)^2] < \infty \}
$$

with inner product defined as the covariance (since they are centered):

$$
\langle f, g \rangle_P = \mathbb{E}_P[ f(O)g(O) ] = \mathrm{Cov}_P(f,g)
$$

Scores belong to $$L_0^2(P)$$.

**Orthogonality.**
In this space, two functions are **orthogonal** ($$f \perp g$$) when their corresponding random variables are **uncorrelated**. Since our limiting distribution is Gaussian, later this will also mean independence.

**Projection.**
Projection is the bread and butter for the Hilbert space.
*   Let $$S$$ be an element of $$L^2_0(P)$$, 
*   Let $$H$$ be a sub-Hilbert space of $$L^2_0(P)$$. For example, tangent space at $$P$$.
*   Then the projection $$\Pi(S\mid H)$$ of $$S$$ onto $$H$$ is a unique element defined by 
    1.  $$\Pi(S\mid H)\in H$$: being an element in $$H$$,
    2.  $$S-\Pi(S\mid H) \perp H$$: $$S$$ minus projection is uncorrelated with any element in $$H$$.

### Example

**Model.**
$$\mathcal{M}$$ is nonparametric. Here we define it as a collection of all probability distributions which have densities.

**Direction $$h(o)$$.**
*   $$h$$ is also a function of $$o$$
*   $$h(o)$$ represents the "shape" of the perturbation
*   If $$h(o)$$ is positive, we increase the probability of observing $$o$$
*   If $$h(o)$$ is negative, we decrease it.
*   We pick $$h(o)$$ such that $$h$$ uniformly bounded and $$\mathbb{E}_Ph(O)=0$$. This broad definition is equivalent to defining $$\mathcal{H}$$

**Submodel.**
We **define** $$P_\epsilon^h$$ so that $$dP_{\epsilon}(o)=(1+\epsilon h(o)) dP(o)$$. Defined via densities.
*   In semi-parametric theory, we are allowed to invent any path $$P_\epsilon$$ we want, as long as it passes through the true model $$P$$ at $$\epsilon=0$$. There is no single "correct" way to draw a line through a probability distribution.
*   Submodel check 1: density integration to 1

$$
\int dP_\epsilon(o) = \int (1 + \epsilon h(o)) dP(o)   = \underbrace{\int 1 \, dP(o)}_{=1} + \epsilon \underbrace{\int h(o) \, dP(o)}_{= E_P[h(O)] \text{ should be 0}}
$$

Intuition: To add probability mass to one area (where $$h > 0$$), we must steal it from another area (where $$h < 0$$) to keep the total mass constant.

*   Submodel check 2: nonnegativity. Let's think of a worst case scenario: at some observation $$o$$, $$h(o)$$ takes its most negative possible value; $$h(o) = -\|h\|_\infty$$. Then the scaling factor becomes $$1 + \epsilon (-\|h\|_\infty)$$. We need this factor to stay non-negative:
    
$$
1 - \epsilon \|h\|_\infty \ge 0 \iff 1 \ge \epsilon \|h\|_\infty \iff \epsilon \le \frac{1}{\|h\|_\infty}
$$

Therefore, if we restrict $$\epsilon$$ to be smaller than $$\delta = 1/\|h\|_\infty$$, i.e.  $$\epsilon\in (-\delta,\delta)$$ with $$\delta=1/\|h\|_{\infty}$$, this is a submodel $$\mathcal{M}_h(P)$$.

**Score.**
This construction perfectly yields the score $$h$$. By the construction $$dP_{\epsilon} = (1+\epsilon h) dP$$:

$$
S(O) = \frac{d}{d\epsilon} \log \big( \frac{(1+\epsilon h(O)) dP(O)}{dP(O)} \big) \bigg|_{\epsilon=0}
$$

The derivative of $$\log(u)$$ is $$u'/u$$:

$$
S(O) = \frac{h(O)}{1+\epsilon h(O)} \bigg|_{\epsilon=0}
$$

Set $$\epsilon=0$$:

$$
S(O) = \frac{h(O)}{1} = h(O)
$$

**Scores.**
$$\mathcal{S}$$ is all $$h\in L^2_0(P)$$ with $$\|h\|_{\infty}<\infty$$.

## Tangent Space, T(P)

*   Let $$T(P)\subset L^2_0(P)$$ be the closure of the linear span of the set of scores $$\mathcal{S}$$ of our class of paths.
*   This is a sub-Hilbert space of $$L^2_0(P)$$.
*   It is called the tangent space at $$P$$.
*   The tangent space for a *nonparametric* model is the whole $$L^2_0(P)$$. We say that the model is locally saturated at $$P$$. 

We have that the score is an element of the Hilbert space and we have a collection of scores that correspond with this class of paths, generating a sub-Hilbert space of $$L_0^2(P)$$. We might take any linear combination of all the scores and the closure (any function you can approximate as an a limit of such linear combinations of all these scores is also additive) and that creates a sub-Hilbert space, $$H$$ of $$L_0^2(P)$$. $$H$$ is the tangent space corresponding with this class of paths.

## Problem with standard directional derivative of target parameter

*   We want to define a type of differentiability of $$\Psi:\mathcal{M}\rightarrow\mathbb{R}^d$$.
*   We could use the definition of a directional derivative in direction $$h$$:

$$
d\Psi(P)(h)=\left . \frac{d}{d\epsilon}\Psi(P+\epsilon h)\right |_{\epsilon =0}
$$

*   However, $$P+\epsilon h$$ is not a path within $$\mathcal{M}$$, so this could be ill defined.
*   Therefore, we define a derivative along paths that are submodels of $$\mathcal{M}$$.

## Pathwise derivative

*   The pathwise derivative is defined as: 

$$
d\Psi(P)(S_h)=\left . \frac{d}{d\epsilon}\Psi(P_{\epsilon}^h)\right |_{\epsilon =0}
$$

*   This is linear operator in its score $$S_h$$. 
*   Thus, $$d\Psi(P):L^2_0(P)\rightarrow\mathbb{R}^d$$ is a real valued linear operator on a Hilbert space $$L^2_0(P)$$.

### Pathwise differentiability and gradient

*   $$\Psi:\mathcal{M}\rightarrow\mathbb{R}^d$$ is pathwise differentiable at $$P$$ if its pathwise derivative is a **bounded** linear operator. 
*   By the Riesz-representation theorem, then $$d\Psi(P):L^2_0(P)\rightarrow\mathbb{R}^d$$ can be represented as an inner product of gradient with score:

$$
d\Psi(P)(S_h)=E_P D(P)(O)S_h(O)= \langle D(P),S_h\rangle_P 
$$

*   $$D(P)$$ is called a gradient of the pathwise derivative. 

## Class of gradients

*   A gradient is not necessarily unique.
*   Let $$T(P)^{\perp}=\{S\in L^2_0(P):P\perp T(P)\}$$ be orthogonal complement of $$T(P)$$.
*   If $$D(P)$$ is a gradient, then $$D(P)+S$$ with $$S\in T(P)^{\perp}$$ is also a gradient.

## Canonical gradient is projection of gradient on tangent space

*   There is one unique gradient $$D^*(P)\in T(P)$$ in the tangent space. 
*   This is called the canonical gradient.
*   The set of all gradients is $$D^*(P)+S$$ with $$S\in T(P)^{\perp}$$.
*   If $$D$$ is gradient, then canonical gradient $$D^*(P)$$ is the projection of $$D(P)$$ onto tangent space.

### Example

*   $$O=T$$, $$\mathcal{M}$$ nonparametric model, $$\Psi(P)=P(T>5)$$.
*   $$dP_{\epsilon}(T) =(1+\epsilon S(T))dP(T)$$, $$S(T)$$ is score.
*   
$$
\left . \frac{d}{d\epsilon}\Psi(P_{\epsilon}^h)\right |_{\epsilon =0} =E_P D(P)(T)S_h(T)
$$

where gradient

$$
D(P)(T)=I(T>5)-\Psi(P)
$$

### Nonparametric model has only one gradient

*   This gradient $$D(P)$$ is also the canonical gradient. 

$$T(P)=L_0^2(P)$$ so the orthogonal complement of the tangent space is empty meaning you cannot add to the canonical gradient anything to create more gradients. 

### Finding canonical gradient in non-saturated models

*   First find a gradient $$D(P)$$ by computing the pathwise derivative for each path $$=E_P[D(P)(O)S(O)]$$.
*   The canonical gradient equals the projection of $$D(P)$$ onto the tangent space $$T(P)$$:

$$
D^*(P)=\Pi(D(P)\mid T(P))
$$
