---
layout: distill
title: "Lecture 16: Canonical Gradient and Efficient Influence Curve"
description: "Notes by Rachael Phillips for PB HLTH 290, Spring 2019"
date: 2026-02-20
categories: dso-603 statistics
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

# Introduction

An asymptotically linear estimator with influence curve equal to the efficient influence curve is optimal in the sense that there is no other asymptotically linear estimator with influence curve with a smaller variance. We call this estimator asymptotically efficient. 

# Setting

## Data and Model
   $$ O_1, \dots, O_n \overset{iid}{\sim} P_0 \in \mathcal{M}. $$
   Here, $$\mathcal{M}$$ denotes the statistical model, which is the collection of all possible probability distributions $$P$$ that could generate the data.

## Target Parameter
   - The target parameter is defined as a functional (or operator) $\Psi: \mathcal{M} \to \mathbb{R}$. 
   - This mapping takes a probability distribution $$P$$ as input and returns a scalar value representing a specific feature of that distribution (e.g., the mean, the risk difference).
   - Usually, target paramter is simple. Scalar or low dimensional vector. It is rarely a regression function.
   

## Estimand
   - The true value of the parameter, often denoted as $\psi_0 = \Psi(P_0)$, is the **estimand**. 
   - This is an unknown quantity because the true data-generating distribution $P_0$ is unknown.

# Goal
- We want to build a best possible estimator of $\psi_0$.
- To build a best estimator, we have to know the fundamental limi of estimation accuracy. The best estimator is what achieves this limit.
- The properties of the functional $\Psi$ itself dictate the difficulty of the estimation problem. 
 
# Local Perturbations
- To quantify this difficulty, we analyze the behavior of $\Psi$ under local perturbations.
- We ask: "If the true distribution $P_0$ changes slightly, how much does the parameter $\Psi(P_0)$ change?"
- This concept is analogous to a derivative in calculus. 
- The steepness of this functional derivative (formally captured by the *Efficient Influence Function*) determines the *Information Bound*. 
- A steeper functional implies that the parameter is more sensitive to fluctuations in the data, resulting in a harder estimation problem (higher minimum variance).

# Parametric submodels and scores
- Summary: given a path $h$ and submodel formula, we ontain a random variable $S_h(O)$.
- This random variable $S_h(O)$ measures the sensitivity: how the probability of observing your specific data point $O$ reacts when you start bending the underlying statistical distribution in direction $h$.
- 
## Motivation: Valid Directions
- When defining the derivative of $\Psi$, we cannot simply look at arbitrary perturbations $P + \epsilon h$ (as in standard calculus).
- The resulting object $P + \epsilon h$ might not be a valid probability distribution (e.g., it might not integrate to 1 or could be negative). 
- Therefore, we must restrict our attention to perturbations within the space of valid probabilities. 
- We achieve this by defining *parametric submodels*.

## Parametric submodel, given h

- For a specific **path** $h$ (a function in a Hilbert space), we define a one-dimensional parametric submodel passing through the true distribution $P$:

<p>
\begin{equation*}
\mathcal{M}_h(P) = \{ P^h_{\epsilon} : \epsilon \in (-\delta, \delta) \} \subset \mathcal{M}
\end{equation*}
</p>

- This submodel (collection of distributions) is a curve within the large model $\mathcal{M}$ such that:
  *   At $\epsilon = 0$, the distribution is the true data-generating distribution: $P^h_{\epsilon=0} = P$.
  *   For $\epsilon > 0$, we move away from $P$ by $\epsilon$ along the path $h$, while remaining inside the model $\mathcal{M}$.
  *   The specific value of $\delta$ is not critical. We are only interested in the behavior of the submodel in the immediate neighborhood of $\epsilon=0$.
  *   Defining $h$ itself is a bit flexible. Furthermore, after $P$ and $h$ are fixed, the form of $P^h_{\epsilon}$ is also flexible. Not necessarily $P+ \epsilon h$. We are allowed to invent any $P_\epsilon$ we want, as long as it passes through the true model $P$ at $\epsilon=0$ and stays on the path $h$. 

- We can think of the submodel $P_\epsilon^h$ as constructed by a **curve-drawing machine**. 
  *   **Input:** We feed it a "drawing parameter" $h$, which determines the style or direction of the curve.
  *   **Action:** As we vary $\epsilon$, the machine draws a series of dots (probability distributions) inside the model space. In other words, $\epsilon$ is a slider. It is a distance.
  *   **Output:** The collection of these dots forms the curve $\mathcal{M}_h(P)$. By construction, every dot on this curve is a valid probability distribution passing through $P$ at $\epsilon=0$.

## A special direction: score $S$, given $h$
- The only direction we care about each submodel, $\mathcal{M}_h(P)$, is its score. 
- Given a path $h$, its score $S_h$ is defined as a transformation of an observation: 
<p>
\begin{equation*}
S_h(O)=\left . \frac{d}{d\epsilon}\log dP_{\epsilon}^h/dP(O)\right |_{\epsilon=0}
\end{equation*}
</p>

- The term $\frac{dP_{\epsilon}^h}{dP}$ (which your text simplifies to $p_{\epsilon}^h$) is a likelihood ratio. 
  - For any given data point $O$, this ratio asks: "How much more (or less) likely is it to observe this exact data point under the new, nudged distribution compared to the original baseline distribution?"
  - Or we can view this as taking the log of the density that is defined with respect to $$P$$ itself.
- The derivative $\frac{d}{d\epsilon}$ evaluated exactly at the starting point ($\epsilon = 0$) measures the instantaneous rate of change.

- Ultimately, the score $S_h(O)$ measures sensitivity. 
- It tells you exactly how the probability of observing your specific data point $O$ reacts when you start bending the underlying statistical distribution in direction $h$.
  - If the score is large and positive, it means that nudging the distribution in direction $h$ rapidly makes the data point $O$ more likely to occur.
  - If the score is large and negative, moving in direction $h$ makes $O$ less likely.
  - If the score is zero, the likelihood of seeing $O$ is completely unaffected by tiny shifts in that specific direction.

 

# Tangent space and Hilbert space
- Summary: class of paths $h$ is not our choice. It is defined by true distribution $P$.
## Class of paths, Class of Scores (the Tangent Set)
- Let's fix the submodel formula. Then for each $h$, we have one score random variable $S_h(O)$.
- We consider a collection of $h$: a set of paths $\mathcal{H}$.
- This leads to a collection of scores random variables $\mathcal{S} = \{ S_h : h \in \mathcal{H} \}$, which is the collection of all score functions generated by these paths.
- **We should be careful about $\mathcal{H}$**. We choose $\mathcal{H}$ to be sufficiently "rich" to ensure that the set of scores $\mathcal{S}$ 
  - captures all possible local directions in which we can perturb $P$,
  - and remain within the constraints of the model $\mathcal{M}$.
- The set $\mathcal{S}$ (specifically, the closure of its linear span) is formally called the **Tangent Space** of the model at $P$.

## The Hilbert Space $L_0^2(P)$

### Scores as Random Variables
- Scores are measurable functions of the data $O \sim P$.
- Therefore, they are random variables with specific properties:
  - **Mean Zero:** $\mathbb{E}_P[S(O)] = 0$.
  - **Finite Variance:** $\mathrm{Var}_P[S(O)] < \infty$.

### Hilbert Space defined by $P$
- We define $L^2_0(P)$ as the Hilbert space containing all such mean-zero, square-integrable functions of $O$ (thus they are mostly correlated)

<p>
\begin{equation}
L^2_0(P) = \{ f(O) : \mathbb{E}_P[f(O)]=0, \, \mathbb{E}_P[f(O)^2] < \infty \}
\end{equation}
</p>

with inner product defined as the covariance (since they are centered):

<p>
\begin{equation}
\langle f, g \rangle_P = \mathbb{E}_P[ f(O)g(O) ] = \mathrm{Cov}_P(f,g)
\end{equation}
</p>

- $L^2_0(P)$ is related to $P$ because expectation is taken with respect to $P$. But its definition is not yet related to the derivative or score.
- The tangent space (the scores) is a sub-Hilbert space of $L^2_0(P)$.


### Orthogonality
- In $L^2_0(P)$, two functions are **orthogonal** ($$f \perp g$$) when their corresponding random variables are **uncorrelated**. 
- Since our limiting distribution is Gaussian, later this will also mean independence.

### Projection
- Projection is the bread and butter for the Hilbert space, and is defined through orthogonality.
- Let $S$ be an element of $L^2_0(P)$, 
- Let $H$ be a sub-Hilbert space of $L^2_0(P)$. For example, tangent space at $P$.
- Then the projection $\Pi(S\mid H)$ of $S$ onto $H$ is a unique element defined by 
    1.  $\Pi(S\mid H) \in H$: being an element in $H$,
    2.  $S - \Pi(S\mid H) \perp H$: $S$ minus projection is uncorrelated with any element in $H$. 



## Tangent Space, T(P)
- We have that the score is an element of the Hilbert space $L^2_0(P)$, because score has  zero mean and finite variance.
- Let $T(P)\subset L^2_0(P)$ be the closure of the linear span of the set of scores $\mathcal{S}$ of our class of paths.
  - closure of the linear span means that any function you can approximate as an a limit of such linear combinations
- This is a sub-Hilbert space of $L^2_0(P)$.
- It is called the tangent space at $P$.
- The tangent space for a *nonparametric* model is the whole $L^2_0(P)$. We say that the model is locally saturated at $P$. 

 

# Pathwise derivative

## The Chain Rule Analogy
- While the formal calculus of functionals is more complex, the intuition parallels standard calculus ($\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$). 

<p>
\begin{equation*}
\underbrace{\frac{d}{d\epsilon} \Psi(P^h_\epsilon)}_{\text{Total Change}}\bigg|_{\epsilon=0} 
\approx 
\underbrace{
\frac{d\Psi}{dP}
}_{
\text{"Operator Change"}
} 
\cdot
\underbrace{
\frac{dP}{d\epsilon}
}_{
\text{"Curve Change"}
}
\end{equation*}
</p>

- The chain rule implies that we can separate the geometry of the model from the target parameter. 
- We can pre-compute the "curve part" (the Score $S_h$) purely based on the submodel.
- When we combine it with the Gradient via the inner product, we recover the pathwise derivative we need to study efficiency.

## Pathwise Derivative as a Linear Operator
- The pathwise derivative is defined as: 

<p>
\begin{equation*}
d\Psi(P)(S_h)=\left . \frac{d}{d\epsilon}\Psi(P_{\epsilon}^h)\right |_{\epsilon =0}
\end{equation*}
</p>

- This is linear operator in its score $S_h$. 
- Thus, $d\Psi(P):L^2_0(P)\rightarrow\mathbb{R}^d$ is a real valued linear operator on a Hilbert space $L^2_0(P)$.

### Pathwise differentiability and gradient

- $\Psi:\mathcal{M}\rightarrow\mathbb{R}^d$ is pathwise differentiable at $P$ if its pathwise derivative is a **bounded** linear operator. 
- By the Riesz-representation theorem, then $d\Psi(P):L^2_0(P)\rightarrow\mathbb{R}^d$ can be represented as an inner product of gradient with score:

<p>
\begin{equation*}
d\Psi(P)(S_h)=E_P D(P)(O)S_h(O)= \langle D(P),S_h\rangle_P 
\end{equation*}
</p>

- $D(P)$ is called a gradient of the pathwise derivative. It is also an element of the Hilbert space.

## Class of gradients

*   A gradient is not necessarily unique.
*   Let $T(P)^{\perp}=\{S\in L^2_0(P):P\perp T(P)\}$ be orthogonal complement of $T(P)$.
*   If $D(P)$ is a gradient, then $D(P)+S$ with $S\in T(P)^{\perp}$ is also a gradient.

## Canonical gradient is projection of gradient on tangent space

- There is one unique gradient $D^*(P)\in T(P)$ in the tangent space. 
- This is called the canonical gradient.
- The set of all gradients is $D^*(P)+S$ with $S\in T(P)^{\perp}$.
- If $D$ is gradient, then canonical gradient $D^*(P)$ is the projection of $D(P)$ onto tangent space.

### Example

- $O=T$, $\mathcal{M}$ nonparametric model, $\Psi(P)=P(T>5)$.
- $dP_{\epsilon}(T) =(1+\epsilon S(T))dP(T)$, $S(T)$ is score.
- 
<p>
\begin{equation*}
\left . \frac{d}{d\epsilon}\Psi(P_{\epsilon}^h)\right |_{\epsilon =0} =E_P D(P)(T)S_h(T)
\end{equation*}
</p>

where gradient

<p>
\begin{equation*}
D(P)(T)=I(T>5)-\Psi(P)
\end{equation*}
</p>

### Nonparametric model has only one gradient

*   This gradient $$D(P)$$ is also the canonical gradient. 

$$T(P)=L_0^2(P)$$ so the orthogonal complement of the tangent space is empty meaning you cannot add to the canonical gradient anything to create more gradients. 

### Finding canonical gradient in non-saturated models

*   First find a gradient $$D(P)$$ by computing the pathwise derivative for each path $$=E_P[D(P)(O)S(O)]$$.
*   The canonical gradient equals the projection of $$D(P)$$ onto the tangent space $$T(P)$$:

<p>
\begin{equation*}
D^*(P)=\Pi(D(P)\mid T(P))
\end{equation*}
</p>



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

<p>
\begin{equation*}
\int dP_\epsilon(o) = \int (1 + \epsilon h(o)) dP(o)   = \underbrace{\int 1 \, dP(o)}_{=1} + \epsilon \underbrace{\int h(o) \, dP(o)}_{= E_P[h(O)] \text{ should be 0}}
\end{equation*}
</p>

Intuition: To add probability mass to one area (where $$h > 0$$), we must steal it from another area (where $$h < 0$$) to keep the total mass constant.

*   Submodel check 2: nonnegativity. Let's think of a worst case scenario: at some observation $$o$$, $$h(o)$$ takes its most negative possible value; $$h(o) = -\|h\|_\infty$$. Then the scaling factor becomes $$1 + \epsilon (-\|h\|_\infty)$$. We need this factor to stay non-negative:
    
<p>
\begin{equation*}
1 - \epsilon \|h\|_\infty \ge 0 \iff 1 \ge \epsilon \|h\|_\infty \iff \epsilon \le \frac{1}{\|h\|_\infty}
\end{equation*}
</p>

Therefore, if we restrict $$\epsilon$$ to be smaller than $$\delta = 1/\|h\|_\infty$$, i.e.  $$\epsilon\in (-\delta,\delta)$$ with $$\delta=1/\|h\|_{\infty}$$, this is a submodel $$\mathcal{M}_h(P)$$.

**Score.**
This construction perfectly yields the score $$h$$. By the construction $$dP_{\epsilon} = (1+\epsilon h) dP$$:

<p>
\begin{equation*}
S(O) = \frac{d}{d\epsilon} \log \big( \frac{(1+\epsilon h(O)) dP(O)}{dP(O)} \big) \bigg|_{\epsilon=0}
\end{equation*}
</p>

The derivative of $$\log(u)$$ is $$u'/u$$:

<p>
\begin{equation*}
S(O) = \frac{h(O)}{1+\epsilon h(O)} \bigg|_{\epsilon=0}
\end{equation*}
</p>

**Score.**
This construction perfectly yields the score $$h$$. By the construction $$dP_{\epsilon} = (1+\epsilon h) dP$$:

<p>
\begin{equation*}
S(O) = \frac{d}{d\epsilon} \log \big( \frac{(1+\epsilon h(O)) dP(O)}{dP(O)} \big) \bigg|_{\epsilon=0}
\end{equation*}
</p>

The derivative of $$\log(u)$$ is $$u'/u$$:

<p>
\begin{equation*}
S(O) = \frac{h(O)}{1+\epsilon h(O)} \bigg|_{\epsilon=0}
\end{equation*}
</p>

Set $$\epsilon=0$$:

<p>
\begin{equation*}
S(O) = \frac{h(O)}{1} = h(O)
\end{equation*}
</p>

**Scores.**
<p>
\begin{equation*}
\mathcal{S} = \{h\in L^2_0(P) : \|h\|_{\infty}<\infty\}.
\end{equation*}
</p>