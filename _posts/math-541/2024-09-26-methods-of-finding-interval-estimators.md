---
layout: distill
title: "Methods of Finding Interval Estimators: Inverting a Test Statistic"
description: "A discussion on finding interval estimators by inverting test statistics, exploring the strong correspondence between hypothesis testing and interval estimation."
date: 2024-09-26
categories: math-541
tags: statistics interval-estimation hypothesis-testing
project: math-541
---

## 9.2 Methods of Finding Interval Estimators

We present methods of finding interval estimators. Operationally, most standard methods are based on the same strategy: **inverting a test statistic**. (A notable exception is Bayesian intervals, which leverage a different construction method based on posterior distributions.)

### 9.2.1 Inverting a Test Statistic

There is a very strong correspondence between hypothesis testing and interval estimation. In fact, we can say in general that every confidence set corresponds to a test and vice versa. Consider the following example.

**Example 9.2.1 (Inverting a normal test)**

Let $X_1, \dots, X_n$ be iid $N(\mu, \sigma^2)$ and consider testing $H_0: \mu = \mu_0$ versus $H_1: \mu \neq \mu_0$. For a fixed $\alpha$ level, a reasonable test (in fact, the most powerful unbiased test) has the rejection region:
$$ \{x: |\bar{x} - \mu_0| > z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\} $$

Note that $H_0$ is accepted for sample points with $|\bar{x} - \mu_0| \le z_{\alpha/2}\frac{\sigma}{\sqrt{n}}$ or, equivalently,

$$ \bar{x} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}} \le \mu_0 \le \bar{x} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}} $$

Since the test has size $\alpha$, this means that $P(H_0 \text{ is rejected} \mid \mu = \mu_0) = \alpha$ or, stated in another way, $P(H_0 \text{ is accepted} \mid \mu = \mu_0) = 1 - \alpha$. Combining this with the above characterization of the acceptance region, we can write:

$$ P\left(\bar{X} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}} \le \mu_0 \le \bar{X} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}} \mathrel{\Big|} \mu = \mu_0\right) = 1 - \alpha $$

But this probability statement is true for every $\mu_0$. Hence, the statement

$$ P_\mu\left(\bar{X} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}} \le \mu \le \bar{X} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right) = 1 - \alpha $$

is true. The interval $\left[\bar{x} - z_{\alpha/2}\frac{\sigma}{\sqrt{n}}, \bar{x} + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right]$, obtained by inverting the acceptance region of the level $\alpha$ test, is a $1 - \alpha$ confidence interval. $\blacksquare$

---

We have illustrated the correspondence between confidence sets and tests. The acceptance region of the hypothesis test, which is the set in the sample space for which $H_0: \mu = \mu_0$ is accepted, is given by:

$$ A(\mu_0) = \left\{ (x_1, \dots, x_n) : \mu_0 - z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \le \bar{x} \le \mu_0 + z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \right\} $$

and the confidence interval, which is the set in the parameter space with plausible values of $\mu$, is given by:

$$ C(x_1, \dots, x_n) = \left\{ \mu : \bar{x} - z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \le \mu \le \bar{x} + z_{\alpha/2} \frac{\sigma}{\sqrt{n}} \right\} $$

These sets are connected to each other by the tautology:

$$ (x_1, \dots, x_n) \in A(\mu_0) \iff \mu_0 \in C(x_1, \dots, x_n) $$

Both tests and intervals ask the same question, but from a slightly different perspective. Both procedures look for consistency between sample statistics and population parameters.
- The **hypothesis test** fixes the parameter and asks what sample values (the acceptance region) are consistent with that fixed value.
- The **confidence set** fixes the sample value and asks what parameter values (the confidence interval) make this sample value most plausible.

The correspondence between acceptance regions of tests and confidence sets holds in general. The next theorem gives a formal version of this correspondence.

---

### Theorem 9.2.2

For each $\theta_0 \in \Theta$, let $A(\theta_0)$ be the acceptance region of a level $\alpha$ test of $H_0 : \theta = \theta_0$. For each $x \in \mathcal{X}$, define a set $C(x)$ in the parameter space by:

$$ C(x) = \{\theta_0 : x \in A(\theta_0)\} \quad \text{(9.2.1)} $$

Then the random set $C(X)$ is a $1 - \alpha$ confidence set.

Conversely, let $C(X)$ be a $1 - \alpha$ confidence set. For any $\theta_0 \in \Theta$, define:

$$ A(\theta_0) = \{x : \theta_0 \in C(x)\} $$

Then $A(\theta_0)$ is the acceptance region of a level $\alpha$ test of $H_0 : \theta = \theta_0$.

<br/>

**Proof:**

For the first part, since $A(\theta_0)$ is the acceptance region of a level $\alpha$ test, we know $P_{\theta_0}(X \notin A(\theta_0)) \le \alpha$, and hence:

$$ P_{\theta_0}(X \in A(\theta_0)) \ge 1 - \alpha $$

Since $\theta_0$ is arbitrary, we can write $\theta$ instead of $\theta_0$. The above inequality, together with equation (9.2.1), shows that the coverage probability of the set $C(X)$ is given by:

$$ P_\theta(\theta \in C(X)) = P_\theta(X \in A(\theta)) \ge 1 - \alpha $$

showing that $C(X)$ is a $1 - \alpha$ confidence set.

For the second part, the Type I Error probability for the test of $H_0 : \theta = \theta_0$ with acceptance region $A(\theta_0)$ is:

$$ P_{\theta_0}(X \notin A(\theta_0)) = P_{\theta_0}(\theta_0 \notin C(X)) \le \alpha $$

So this forms a valid level $\alpha$ test. $\blacksquare$

---

### Understanding the Tradeoffs and Shapes

Although it is common to talk about inverting a test to obtain a confidence set, Theorem 9.2.2 makes it clear that we actually have a **family of tests**, one for each value of $\theta_0 \in \Theta$, that we invert to obtain one confidence set.

The fact that tests can be inverted to obtain a confidence set and vice versa is theoretically interesting, but the really useful part of Theorem 9.2.2 is the first part:
It is usually a relatively easy task to construct a level $\alpha$ acceptance region. The difficult task is constructing a confidence set directly. Thus, the method of obtaining a confidence set by inverting an acceptance region is quite useful. All of the techniques we have for obtaining tests can immediately be applied to constructing confidence sets.

In Theorem 9.2.2, we stated only the null hypothesis $H_0 : \theta = \theta_0$. All that is required of the acceptance region is:

$$ P_{\theta_0}(X \in A(\theta_0)) \ge 1 - \alpha $$

In practice, when constructing a confidence set by test inversion, we will also have in mind an alternative hypothesis such as $H_1 : \theta \neq \theta_0$ or $H_1 : \theta > \theta_0$.
- The alternative will dictate the form of $A(\theta_0)$ that is reasonable.
- The form of $A(\theta_0)$ will determine the shape of $C(x)$.

Note, however, that we carefully used the word **set** rather than **interval**. This is because there is no guarantee that the confidence set obtained by test inversion will be an interval. In most cases, however:
- One-sided tests give one-sided intervals.
- Two-sided tests give two-sided intervals.
- Strange-shaped acceptance regions give strange-shaped confidence sets.
