---
layout: page
title: Hybrid Partial Least Squars Regression with Multiple Functional and Scalar Predictors
description: We propose a computationally efficient NIPALS-type hybrid partial least squares regression algorithm that unifies functional and scalar predictors in a Hilbert space.
img:
importance: 4
category: fun
---

Regression of a scalar response on mixed functional- and scalar-valued predictors, such as medical imaging with auxiliary patient information, intro- duces the new challenge of handling cross-modality correlations. To address this, we propose a hybrid partial least squares (PLS) regression framework that integrates functional and scalar predictors within a unified Hilbert space. We then extend the classical nonlinear iterative PLS (NIPALS) algorithm to this hybrid Hilbert space by iteratively maximizing the empirical cross- covariance between the hybrid predictor and the response. As a result, our method identifies low-dimensional representations that capture both within- and between-modality variation, as well as the response-predictor correla- tion. The procedure is computationally efficient, requiring only the solution of linear systems at each step. We provide theoretical properties to justify our algorithm and demonstrate its effectiveness through simulations and an application to clinical outcome prediction using renal imaging and scalar co- variates from the Emory University renal study.
