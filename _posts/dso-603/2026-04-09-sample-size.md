---
layout: distill
title: "Quick and Dirty Sample Size Calculation"
description: ""
date: 2026-04-09
categories: dso-603 statistics
tags: experimentation ab-testing metrics
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jong-min.org"
bibliography: 2025-08-25-sample-size.bib
---

* In big tech A/B testing, sample sizes are typically large enough to confidently rely on the Central Limit Theorem, permitting the use of the standard normal distribution under the null hypothesis. 
* This frees us from relying on complex statistical theory to determine cutoffs. 
* However, it is worth noting that while the sample size may be large enough to assume normality, it is not always sufficient to achieve the desired statistical power.

# Sample Size Calculation for a Two-Sample Z-Test
* Assume equal sample sizes for both groups. 
* Assume the standard deviation, $\sigma$, is known.
* To compute the required sample size, we need three parameters: the Minimum Detectable Effect (MDE), the Type I error rate ($\alpha$), and statistical power ($1 - \beta$).
* We will discuss the MDE in more detail later, but for now, let's denote it as $\delta$.
* Calculating the sample size requires analyzing two sampling distributions: one under the null hypothesis and one under the alternative hypothesis (the null + MDE).

### Under the Null Hypothesis
* The test statistic is the difference in means: $\bar{X}_2 - \bar{X}_1$.
* The variance is easily computed as $\frac{2\sigma^2}{n}$.
* The resulting sampling distribution is $\mathcal{N}(0, \frac{2\sigma^2}{n})$.
* Given a Type I error rate of $\alpha$, the critical value is $z_{\alpha/2} \cdot \sqrt{\frac{2\sigma^2}{n}}$.

### Under the Alternative Hypothesis
* The sampling distribution shifts to $\mathcal{N}(\delta, \frac{2\sigma^2}{n})$.
* We want to achieve a specific power: $\mathbb{P}_{H_1}\left(\bar{X}_2 - \bar{X}_1 > z_{\alpha/2} \cdot \sqrt{\frac{2\sigma^2}{n}}\right) = 1 - \beta$. 
* Let's denote the critical value as $r = z_{\alpha/2} \cdot \sqrt{\frac{2\sigma^2}{n}}$.
* *Note: We are assuming a one-sided test setup here by fixing the MDE as a positive value.*
* After standardizing the variable and utilizing the symmetry of the normal distribution, we arrive at the requirement:
<p>$$\frac{r-\delta}{\sigma \sqrt{\frac{2}{n}}} = -z_{1-\beta}$$</p>

### Final Step
* We now have an equation with one unknown ($n$). Solving for $n$, we get:
<p>$$n = \frac{2\sigma^2}{\delta^2} (z_{1-\alpha/2} + z_{1-\beta})^2$$</p>
* For a quick and dirty calculation (assuming standard values like $\alpha = 0.05$ and $80\%$ power), the multiplier $2(z_{1-\alpha/2} + z_{1-\beta})^2 \approx 16$.
* This gives us a handy rule of thumb for sample size:
<p>$$n \approx \frac{16\sigma^2}{\delta^2}$$</p>


# Examples
These examples are from <d-cite key="larsenStatisticalChallengesOnline2024"></d-cite>



These examples illustrate the crucial caveat: ***"while the sample size may be large enough to assume normality, it is not always sufficient to achieve the desired statistical power."***

To analyze both scenarios, we use our derived rule of thumb: 
<p>$$n \approx \frac{16\sigma^2}{\delta^2}$$</p>

### The Common Parameters
Before splitting into the two scenarios, let's identify the constants shared by both:
* **Standard Deviation ($\sigma$):** $\$6$
* **Average Spend per Visitor:** $\$1.25$
* **Statistical Parameters:** 80% power ($1-\beta$) and a 5% significance level ($\alpha$). These standard parameters give us the constant multiplier of roughly **$16$** in our numerator.
* **Numerator Constant:** $16\sigma^2 = 16 \times (6)^2 = 576$

---

### Scenario 1: The Small Startup
*The goal is to detect a $5\%$ relative change in average revenue.*

* **Defining the MDE ($\delta$):** The Minimum Detectable Effect is $5\%$ of the average spend.
    <p>$$\delta = \$1.25 \times 0.05 = 0.0625$$</p>
* **Applying the Framework:** We plug our $\delta$ and our numerator constant into the rule of thumb formula.
    <p>$$n \approx \frac{576}{(0.0625)^2} = \frac{576}{0.00390625} \approx 147,456$$</p>
* **Conclusion:** The experiment requires about $147,456$ users per variant. For a startup, generating a few hundred thousand visitors over a reasonable timeframe is a highly feasible requirement to achieve $80\%$ power.

---

### Scenario 2: The Massive Enterprise
*The goal is to detect a $0.02\%$ relative change in average revenue (which represents a material $\$10$ million shift for a $\$50$ billion company).*

* **Defining the MDE ($\delta$):** The Minimum Detectable Effect is now infinitesimally smaller: $0.02\%$ of the average spend.
    <p>$$\delta = \$1.25 \times 0.0002 = 0.00025$$</p>
* **Applying the Framework:** We plug the new $\delta$ into the exact same formula.
    <p>$$n \approx \frac{576}{(0.00025)^2} = \frac{576}{0.0000000625} = 9,216,000,000$$</p>
* **Conclusion:** The experiment requires **$9.2$ billion users per variant** ($18.4$ billion total). 

### The Core Takeaway: The Quadratic Penalty
These examples highlight the mathematical reality of the $\delta^2$ term in the denominator. 

Because the Minimum Detectable Effect ($\delta$) is squared, sample size requirements do not scale linearly; they scale quadratically. If you want to detect an effect that is $250$ times smaller (dropping from $5\%$ to $0.02\%$), you do not need $250$ times as many users—you need **$250^2$ ($62,500$) times as many users**. 

Note that change always result in negative impact. Therefore big companies cannot risk big changes. Therefore the new features that engineering team make are usually small changes. And the data scientists should detect small changes because that small change is big enough to move millions of dollors.

This demonstrates why massive tech companies cannot simply rely on standard A/B testing to detect highly impactful but relatively tiny changes in conversion or revenue, forcing them to look beyond standard two-sample z-tests toward variance reduction techniques (like CUPED) or alternative experimental designs.
# References
