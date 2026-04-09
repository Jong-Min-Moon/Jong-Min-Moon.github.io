---
layout: distill
title: "8.3.1 Power Function"
description: "8 Hypothesis testing / 8.3 Method of evaluating tests
date: 2024-09-26
categories: math-541
tags: statistics hypothesis-testing
project: math-541
---
 
  - Power function unifies type I and type II errors.
 - Test is completely defined by the rejection region $R(x_1, ..., x_n) \in \mathcal{X}^n$.
 - That rejection may or may not be determined by conditioning on one distribution. Usually it does.
- But power function does not. It is also completely determined by the rejection region. The resulting function is a statistical functional: it maps a distribution to a real number.
- That is, how the hypotheses devide the distribution space has nothing to do with the defnition of the power function. 
- Usually the workflow is: 
  - the method of finding a test determins a class of tests (such as LRT with cutoff c)
  - It defines a power function with $c$ unspecified
  - The size constraint is used to determine the value of $c$, pinpointing one test in the class. Here is the first use of the power function.
  - Then the power function is evaluated to see if it is good enough.

 
### Definition 8.3.1: the power function

- The power function of a hypothesis test with rejection region $R$ is the function of $\theta$ defined by $\beta(\theta) = P_{\theta}(X \in R)$.
- Note that the input is $\theta$, a distribution.
- And the power function is completely determined by the rejection region $R$.
> The function of $\theta$, $P_{\theta}(X \in R)$, contains all the information about the test with rejection region $R$.


### Shape of the power function
- Ideally, power function should be a step function, being 0 at at the nulls and 1 at all alternatives. But practically no test can yield a step function as the power function.
- Almost always power function is smooth. Therefore at some alternatives the power is inevitably low.
- This yields the notion of uniform separtion (for theoreists) and Minimum Detectable Effect (MDE; for practitionors). If we are testing for the mean of the distribution being zero or not and the MDE is 0.5, then the test is not guranteed to yield a good power when the true mean is 0.4, for example.

### Examples 8.3.3 and 8.3.4
- For Z test with right tail alternative $H_1: \mu > \mu_0$, the power function is given by $\beta(\mu) = P_{\mu}(Z > z_{\alpha} - \frac{\mu - \mu_0}{\sigma / \sqrt{n}})$. This is a smooth increasing function of $\mu$ (example 8.3.3)
- Several things are unspecified and can be determined by the user (example 8.3.4)
  - type I error condition specifies the rejection region and materializes the curve a little bit. We know that size is usually 0.05.
  - then the MDE condition and power condition determines the sample size, thereby completely determining the power function curve. **This is a basic question for big tech A/B testing interview.** Power condition is usually 0.8. MDE is determined by the business size.
  
