---
layout: distill
title: "Augmented IPW and Double Robustness"
description: "AIPW estimator, double robustness, and cross-fitting"
date: 2025-10-15
categories: causal_inference statistics
tags: causal-inference aipw double-robustness
project: causal_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
bibliography: 2025-10-15-augmented-ipw-and-double-robustness.bib
toc:
  - name: Introduction
  - name: Statistical setting
  - name: Two characterizations of the ATE
  - name: Augmented IPW
  - name: Weak double robustness
  - name: Strong double robustness
  - name: Cross-fitting
  - name: Condensed notation
---

## Introduction
We saw that IPW is a simple ATE stimator under unconfoundedness, which is insensitive to the regression model misspecification. However, the large-sample properties of IPW are not particularly good enough.

## Two characterizations of the ATE
The ATE can be characterized in terms of the propensity score $$e(x) = \mathbb{P} [W_i = 1 \mid X_i = x]$$, as the expectation of oracle IPW estimator:

$$
\begin{equation*}
\tau = \mathbb{E} [\hat{\tau}^*_{IPW}] , \quad \hat{\tau}^*_{IPW} = \frac{1}{n} \sum_{i=1}^n \left( \frac{W_i Y_i}{e(X_i)} - \frac{(1 - W_i) Y_i}{1 - e(X_i)} \right).
\end{equation*}
$$

However, $\tau$ can also be characterized in terms of the conditional response surfaces $\mu_{(w)}(x) = \mathbb{E} [Y_i(w) \mid X_i = x]$. Under unconfoundedness,

$$
\begin{align*}
\tau(x) &:= \mathbb{E} [Y_i(1) - Y_i(0) \mid X_i = x] \\
&= \mathbb{E} [Y_i(1) \mid X_i = x] - \mathbb{E} [Y_i(0) \mid X_i = x] \\
&= \mathbb{E} [Y_i(1) \mid X_i = x, W_i = 1] - \mathbb{E} [Y_i(0) \mid X_i = x, W_i = 0] \quad &(\text{unconf}) \\
&= \mathbb{E} [Y_i \mid X_i = x, W_i = 1] - \mathbb{E} [Y_i \mid X_i = x, W_i = 0] \quad &(\text{SUTVA}) \\
&= \mu_{(1)}(x) - \mu_{(0)}(x),
\end{align*}
$$

and so $\tau = \mathbb{E} [\mu_{(1)}(x) - \mu_{(0)}(x)]$. Thus we could also derive a consistent (but not necessarily optimal) estimator for $\tau$ by first estimating $\mu_{(0)}(x)$ and $\mu_{(1)}(x)$ non-parametrically, and then using 
$$
\begin{equation*}
\hat{\tau}_{REG} = \frac{1}{n} \sum_{i=1}^n(\hat{\mu}_{(1)}(X_i) - \hat{\mu}_{(0)}(X_i)).
\end{equation*}
$$

## Augmented IPW
AIPW mixes the two characterization of ATE by first  making a best effort attempt at $$\tau$$ by estimating $$\mu_{(0)}(x)$$ and $$\mu_{(1)}(x)$$; then, it deals with any biases of the $$\hat{\mu}_{(w)}(x)$$ by applying IPW to the regression residuals<d-cite key="robinsEstimationRegressionCoefficients1994"></d-cite>:

<p>
$$
\begin{align*}
\hat{\tau}_{AIPW} &= \frac{1}{n} \sum_{i=1}^n \left( \hat{\mu}_{(1)}(X_i) - \hat{\mu}_{(0)}(X_i) + \frac{W_i (Y_i - \hat{\mu}_{(1)}(X_i))}{\hat{e}(X_i)} - \frac{(1 - W_i)(Y_i - \hat{\mu}_{(0)}(X_i))}{1 - \hat{e}(X_i)} \right).
\end{align*}
$$
</p>

## Weak double robustness: convergence in probability to ATE
This means that AIPW is consistent if either the $\hat{\mu}_{(w)}(x)$ are consistent or $\hat{e}(x)$ is consistent. To see this, first consider the case where $\hat{\mu}_{(w)}(x)$ is consistent, the regression term goes to $\tau$ and the propensity term also goes to zero because of the residualization:

<p>
$$
\begin{align*}
\hat{\tau}_{AIPW} &= \frac{1}{n} \sum_{i=1}^n (\hat{\mu}_{(1)}(X_i) - \hat{\mu}_{(0)}(X_i)) \quad &\text{ (a consistent treatment effect estimator)} \\
&+ \frac{1}{n} \sum_{i=1}^n \left( \frac{W_i}{\hat{e}(X_i)}(Y_i - \hat{\mu}_{(1)}(X_i)) - \frac{1 - W_i}{1 - \hat{e}(X_i)}(Y_i - \hat{\mu}_{(0)}(X_i)) \right) \quad &\text{ ($\approx$ mean-zero noise)},
\end{align*}
$$
</p>

Second, suppose that $\hat{e}(x)$ is consistent, i.e., $\hat{e}(x) \approx e(x)$. We can express the AIPW estiamtor alternatively as IPW estiamtor plus  regression estimators weighted by propensity residuals. Then, the IPW term goes to $\tau$ and the regression term also goes to zero because of the residualization:

<p>
$$
\begin{align*}
\hat{\tau}_{AIPW} &= \frac{1}{n} \sum_{i=1}^n \left( \frac{W_iY_i}{\hat{e}(X_i)} - \frac{(1 - W_i)Y_i}{1 - \hat{e}(X_i)} \right) \quad &\text{ (the IPW estimator)} \\
&+ \frac{1}{n} \sum_{i=1}^n \left( \hat{\mu}_{(1)}(X_i) \left( 1 - \frac{W_i}{\hat{e}(X_i)} \right) - \hat{\mu}_{(0)}(X_i) \left( 1 - \frac{1 - W_i}{1 - \hat{e}(X_i)} \right)\right) \quad &\text{ ($\approx$ mean-zero noise)},
\end{align*}
$$  
</p>

 

## Strong double robustness: convergence speed (CLT)
 Consider the following “oracle” AIPW estimator that depends on the true $\mu_{(w)}(x)$ and $e(x)$ rather than on estimates thereof:

<p>
$$
\begin{equation*}
\hat{\tau}^*_{AIPW} = \frac{1}{n} \sum_{i=1}^n \left( \mu_{(1)}(X_i) - \mu_{(0)}(X_i) + \frac{W_i(Y_i - \mu_{(1)}(X_i))}{e(X_i)} - \frac{(1 - W_i) (Y_i - \mu_{(0)}(X_i))}{1 - e(X_i)} \right).
\end{equation*}
$$
</p>

Then, under flexible conditions described below, we can verify that

<p>
$$
\begin{equation*}
|\hat{\tau}_{AIPW} - \hat{\tau}^*_{AIPW}| = O_P \left( \max_w \mathbb{E} [(\hat{\mu}_{(w)}(X_i) - \mu_{(w)}(X_i))^2]^{\frac{1}{2}} \mathbb{E} [(\hat{e}(X_i) - e(X_i))^2]^{\frac{1}{2}} \right).
$$
\end{equation*}
</p>

In other words, $\hat{\tau}_{AIPW}$ is a good approximation for the oracle $\hat{\tau}^*_{AIPW}$ as long as both the outcome regressions $\hat{\mu}_{(w)}(\cdot)$ and the propensity regression $\hat{e}(\cdot)$ are reasonably accurate; and if one of them is very accurate it can tolerate the other being less so. The upshot is that, if

<p>
$$
\begin{equation*}
\max_w \mathbb{E} [(\hat{\mu}_{(w)}(X_i) - \mu_{(w)}(X_i))^2]^{\frac{1}{2}} \mathbb{E} [(\hat{e}(X_i) - e(X_i))^2]^{\frac{1}{2}} = o(n^{-1/2}),
\end{equation*}
$$
</p>

then $\hat{\tau}_{AIPW}$ is first-order equivalent to the oracle, meaning that

<p>
$$
\begin{equation*}
\sqrt{n} (\hat{\tau}_{AIPW} - \hat{\tau}^*_{AIPW}) \xrightarrow{p} 0.
\end{equation*}
$$
</p>

Now, $\hat{\tau}^*_{AIPW}$ is just an IID average, so we immediately see that

<p>
$$
\begin{equation*}
\sqrt{n} (\hat{\tau}^*_{AIPW} - \tau) \Rightarrow \mathcal{N} \left(0, V^* \right),
\end{equation*}
$$
</p>

and so whenever $\sqrt{n} (\hat{\tau}_{AIPW} - \hat{\tau}^*_{AIPW}) \xrightarrow{p} 0$ holds $\hat{\tau}_{AIPW}$ also satisfies a CLT as above. In interpreting the constraint, note that if $\hat{\mu}_{(w)}$ and $\hat{e}$ both attained the parametric “$\sqrt{n}$-consistent” rate, then the error product would be bounded as $O(1/n)$. A simple way to satisfy it is to have all regression adjustments be $o(n^{-1/4})$ consistent in root-mean squared error (RMSE), which is an order of magnitude slower than the parametric rate. Moreover, this condition doesn’t depend on the internal structure of the machine learning method used; rather, it only depends on the mean-squared error of the risk adjustments, and so justifies tuning the $\hat{\mu}_{(w)}(\cdot)$ and $\hat{e}(\cdot)$ estimates via cross-validation.



## Cross-fitting
When choosing which treatment effect estimator to use in practice, we want to attain performance as in the CLT equation and so need to make sure that first-order equivalence holds. In order to formally establish this result, it is helpful to consider the following minor modification of AIPW using cross-fitting. At a high level, cross-fitting uses cross-fold estimation to avoid bias due to overfitting; the reason why this works is exactly the same as why we want to use cross-validation when estimating the predictive accuracy of an estimator.

Cross-fitting first splits the data (at random) into two halves $\mathcal{I}_1$ and $\mathcal{I}_2$, and then uses an estimator

<p>
$$
\begin{equation*}
\hat{\tau}_{AIPW} = \frac{|\mathcal{I}_1|}{n} \hat{\tau}_{\mathcal{I}_1} + \frac{|\mathcal{I}_2|}{n} \hat{\tau}_{\mathcal{I}_2},
\end{equation*}
$$
</p>

<p>
$$
\begin{equation*}
\hat{\tau}_{\mathcal{I}_1} = \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} \left( \hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \hat{\mu}_{\mathcal{I}_2}^{(0)}(X_i) + \frac{W_i (Y_i - \hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i))}{\hat{e}_{\mathcal{I}_2}(X_i)} - \frac{(1 - W_i) (Y_i - \hat{\mu}_{\mathcal{I}_2}^{(0)}(X_i))}{1 - \hat{e}_{\mathcal{I}_2}(X_i)} \right),
\end{equation*}
$$
</p>

where the $\hat{\mu}_{\mathcal{I}_2}^{(w)}(\cdot)$ and $\hat{e}_{\mathcal{I}_2}(\cdot)$ are estimates of $\mu_{(w)}(\cdot)$ and $e(\cdot)$ obtained using only the half-sample $\mathcal{I}_2$, and $\hat{\tau}_{\mathcal{I}_2}$ is defined analogously (with the roles of $\mathcal{I}_1$ and $\mathcal{I}_2$ swapped). In other words, $\hat{\tau}_{\mathcal{I}_1}$ is a treatment effect estimator on $\mathcal{I}_1$ that uses $\mathcal{I}_2$ to estimate its nuisance components, and vice-versa. This cross-estimation construction allows us to, asymptotically, ignore the idiosyncrasies of the specific machine learning adjustment we chose to use, and to simply rely on the following high-level conditions:

1. **Overlap**: The true propensity score is bounded away from 0 and 1, such that $\eta < e(x) < 1 - \eta$ for all $x \in \mathcal{X}$.
2. **Consistency**: All machine learning adjustments are sup-norm consistent,
   $$ \sup_{x \in \mathcal{X}} |\hat{\mu}_{\mathcal{I}_2}^{(w)}(x) - \mu_{(w)}(x)|, \sup_{x \in \mathcal{X}} |\hat{e}_{\mathcal{I}_2}(x) - e(x)| \xrightarrow{p} 0. $$
3. **Risk decay**: The product of the errors for the outcome and propensity models decays as
   $$ \mathbb{E} \left[ (\hat{\mu}_{\mathcal{I}_2}^{(w)}(X_i) - \mu_{(w)}(X_i))^2 \right] \mathbb{E} \left[ (\hat{e}_{\mathcal{I}_2}(X_i) - e(X_i))^2 \right] = o \left( \frac{1}{n} \right), $$
   where the randomness above is taken over both the training of $\hat{\mu}_{(w)}$ and $\hat{e}$ and the test example $X$.

Given these assumptions, we characterize the cross-fitting estimator by coupling it with the oracle efficient score estimator $\hat{\tau}^*$, i.e.,

<p>
$$
\sqrt{n} (\hat{\tau}_{AIPW} - \hat{\tau}^*) \xrightarrow{p} 0.
$$
</p>

To do so, we first note that we can write

<p>
$$
\hat{\tau}^* = \frac{|\mathcal{I}_1|}{n} \hat{\tau}_{\mathcal{I}_1, *} + \frac{|\mathcal{I}_2|}{n} \hat{\tau}_{\mathcal{I}_2, *}
$$
</p>

analogously. Moreover, we can decompose $\hat{\tau}_{\mathcal{I}_1}$ itself as

<p>
$$
\begin{equation*}
\hat{\tau}_{\mathcal{I}_1} = \hat{\mu}_{\mathcal{I}_1}^{(1)} - \hat{\mu}_{\mathcal{I}_1}^{(0)}, \quad \hat{\mu}_{\mathcal{I}_1}^{(1)} = \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} \left( \hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) + \frac{W_i (Y_i - \hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i))}{\hat{e}_{\mathcal{I}_2}(X_i)} \right), 
\end{equation*}
$$
</p>

etc., and define $\hat{\mu}_{\mathcal{I}_1, *}^{(0)}$ and $\hat{\mu}_{\mathcal{I}_1, *}^{(1)}$ analogously. Given this buildup, in order to verify $\sqrt{n} (\hat{\tau}_{AIPW} - \hat{\tau}^*) \xrightarrow{p} 0$, it suffices to show that

<p>
$$
\sqrt{n} \left( \hat{\mu}_{\mathcal{I}_1}^{(1)} - \hat{\mu}_{\mathcal{I}_1, *}^{(1)} \right) \xrightarrow{p} 0.
$$
</p>

We now study the term by decomposing it as follows:

<p>
$$
\begin{align*}
\hat{\mu}_{\mathcal{I}_1}^{(1)} - \hat{\mu}_{\mathcal{I}_1, *}^{(1)} &= \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} \left( \hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) + \frac{W_i(Y_i - \hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i))}{\hat{e}_{\mathcal{I}_2}(X_i)} - \mu_{(1)}(X_i) - \frac{W_i(Y_i - \mu_{(1)}(X_i))}{e(X_i)} \right) \\
&= \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} \left( (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i)) \left( 1 - \frac{W_i}{e(X_i)} \right) \right) \\
&+ \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} W_i \left( (Y_i - \mu_{(1)}(X_i)) \left( \frac{1}{\hat{e}_{\mathcal{I}_2}(X_i)} - \frac{1}{e(X_i)} \right) \right) \\
&- \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} W_i \left( (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i)) \left( \frac{1}{\hat{e}_{\mathcal{I}_2}(X_i)} - \frac{1}{e(X_i)} \right) \right).
\end{align*}
$$
</p>

Now, we can verify that these are small for different reasons. For the first term, we intricately use the fact that, thanks to our double machine learning construction, $\hat{\mu}_{\mathcal{I}_2}^{(w)}$ can effectively be treated as deterministic. Thus after conditioning on $\mathcal{I}_2$, the summands used to build this term become mean-zero and independent:

<p>
$$
\begin{align*}
\mathbb{E} &\left[ \left( \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} \left( (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i)) \left( 1 - \frac{W_i}{e(X_i)} \right) \right) \right)^2 \right] \\
&= \mathbb{E} \left[ \mathbb{E} \left[ \left( \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} \left( (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i)) \left( 1 - \frac{W_i}{e(X_i)} \right) \right) \right)^2 \;\middle|\; \mathcal{I}_2 \right] \right] \\
&= \mathbb{E} \left[ \text{Var} \left[ \frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1} \left( (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i)) \left( 1 - \frac{W_i}{e(X_i)} \right) \right) \;\middle|\; \mathcal{I}_2 \right] \right] \\
&= \frac{1}{|\mathcal{I}_1|} \mathbb{E} \left[ \text{Var} \left[ (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i)) \left( 1 - \frac{W_i}{e(X_i)} \right) \;\middle|\; \mathcal{I}_2 \right] \right] \\
&= \frac{1}{|\mathcal{I}_1|} \mathbb{E} \left[ \mathbb{E} \left[ (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i))^2 \left( \frac{1}{e(X_i)} - 1 \right) \;\middle|\; \mathcal{I}_2 \right] \right] \\
&\leq \frac{1}{\eta |\mathcal{I}_1|} \mathbb{E} \left[ (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i))^2 \right] \\
&= o_P \left( \frac{1}{n} \right)
\end{align*}
$$
</p>

by consistency (2), because $|\mathcal{I}_1| \approx n/2$. The key step in this argument was the 3rd equality: Because the summands become independent and mean-zero after conditioning, we “earn” a factor $1/|\mathcal{I}_1|$ due to concentration of iid sums.

The second summand in our decomposition here can also be bounded similarly (thanks to overlap). Finally, for the last summand, we simply use Cauchy-Schwarz:

<p>
$$
\begin{align*}
\frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1, W_i=1} \left( (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i)) \left( \frac{1}{\hat{e}_{\mathcal{I}_2}(X_i)} - \frac{1}{e(X_i)} \right) \right)
&\leq \sqrt{\frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1, W_i=1} (\hat{\mu}_{\mathcal{I}_2}^{(1)}(X_i) - \mu_{(1)}(X_i))^2} \times \sqrt{\frac{1}{|\mathcal{I}_1|} \sum_{i \in \mathcal{I}_1, W_i=1} \left( \frac{1}{\hat{e}_{\mathcal{I}_2}(X_i)} - \frac{1}{e(X_i)} \right)^2}
\\&= o_P \left( \frac{1}{\sqrt{n}} \right)
\end{align*}
$$
</p>
by risk decay (3). (To establish this fact, also note that by consistency (2), the estimated propensities will all eventually also be uniformly bounded away from 0, $\eta/2 \leq \hat{e}_{\mathcal{I}_2}(X_i) \leq 1 - \eta/2$, and so the MSE for the inverse weights decays at the same rate as the MSE for the propensities themselves.)

The upshot is that by using cross-fitting, we can transform any $o_P(n^{-1/4})$-consistent machine learning method into an efficient ATE estimator. Also, the proof was remarkably short (at least compared to a typical proof in the semiparametric efficiency literature).
Stefan Wager recommends:
> When I talk about AIPW, I’ll implicitly assume we’re using cross-fitting unless specified otherwise. I also recommend using cross-fitting when implementing AIPW in practice.
