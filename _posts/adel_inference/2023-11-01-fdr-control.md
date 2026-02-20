---
layout: distill
title: "FDR control: Storey's procedure"
description: "Review of Storey's procedure for FDR control."
date: 2023-11-01
categories: adel_inference statistics
tags: fdr statistics
project: adel_inference
authors:
  - name: Jong Min Moon
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Improving BH
  - name: An estimate of $\pi_0$
  - name: Storey’s procedure
---
## False Discovery Rate

The False Discovery Rate (FDR) is defined as the expected proportion of false positives (incorrectly rejected null hypotheses) among all rejected hypotheses.

$$
\text{FDR} = \mathbb{E}\left[ \frac{V}{R} \right] = \mathbb{E}\left[ \frac{V}{V+S} \right]
$$

where:
* $V$ is the number of false positives (Type I errors).
* $S$ is the number of true positives.
* $R = V + S$ is the total number of rejections.
* If $R=0$, the ratio $V/R$ is defined as 0.

Controlling the FDR at level $\alpha$ (e.g., 0.05) ensures that the expected proportion of false discoveries remains below $5\%$.

## Improving BH

A key limitation of the original Benjamini-Hochberg (BH) procedure is its conservatism. The BH procedure guarantees:

$$
\text{FDR} \le \pi_0 \alpha
$$

where $\pi_0$ is the true proportion of null hypotheses.
* If $\pi_0 \approx 1$ (most hypotheses are true nulls), the BH control is tight.
* If $\pi_0 < 1$ (a significant fraction of hypotheses are false), the actual FDR is controlled at a level strictly lower than $\alpha$.

This means the procedure is less powerful than it could be. Storey's procedure improves upon this by estimating $\pi_0$ from the data to potentially gain more power while maintaining FDR control.

Recall the empirical process view point of BH:

$$
\frac{\hat{\pi}_0(t) t}{\hat{F}(t)} \le \alpha
$$

We were to able to exactly characterize FDR of BH procedure as

$$
\text{FDR}_{\text{BH}} = \pi_0 \alpha
$$

What if we could estimate $\pi_0$?

## An estimate of $\pi_0$

Let $\pi_0 = n_0 / n$ be the fraction of nulls. Pick $\lambda \in (0, 1)$ and compute

$$
\hat{\pi}_0 = \frac{\sum_{i=1}^n \mathbb{I}(p_i > \lambda)}{n(1-\lambda)}
$$

Why is this estimate sensible?

## Storey’s procedure

1. Pick $\lambda \in [0, 1)$ (typically $1/2$)
2. Estimate null proportions:

$$
\hat{\pi}_0(\lambda) = \frac{1 + \sum_{i=1}^n \mathbb{I}(p_i > \lambda)}{n(1-\lambda)}
$$

3. Similar to BH construct the cutoff:

$$
\text{storey}_{\lambda} = \sup \{ t : \frac{\hat{\pi}_0(\lambda) t}{\hat{F}(t)} \le \alpha \}
$$

We only consider $\lambda < t$ because in the estimate $\hat{\pi}_0$ we implicitly assume p-values above $\lambda$ are null.

### Theorem (Storey 2004)

If the p-values are independent, then for $\alpha \in (0, 1)$ the Storey’s procedure controls FDR as

$$
\text{FDR} \le \alpha
$$
