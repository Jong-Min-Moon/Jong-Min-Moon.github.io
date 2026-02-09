---
layout: project
title: fMRI Site Harmonization Using Causal Inference
description: Site Harmonization Using Average Treatment Effect for the Overlap Population
img: assets/img/publication_preview/natcomm_mini.png
venue: Nature Communications
importance: 3
category: computational neuroscience
project_handle: site-harmonization
---

Pooling multi-site MRI data is crucial for enhancing statistical power in neuroimag- ing studies. However, site-related variability introduces significant challenges, particularly when biological covariates are unevenly distributed across sites. Traditional harmonization methods, such as ComBat and its extensions, rely on strong modeling assumptions about the conditional expectation of imaging features given site and covariates, which may not scale effectively to high-dimensional settings. In this study, we reframe site harmonization as a causal inference problem and propose the use of overlap weighting, an improved variant of inverse propensity score weighting (IPW), to estimate and remove site effects. Unlike conditional outcome modeling, overlap weighting does not require direct modeling of high-dimensional outcomes and naturally accommodates heterogeneous site effects. It also mitigates the issue of extreme weights that often hampers IPW. Applying our method to the ABIDE1 dataset, which includes MRI features from 748 brain regions across 19 sites, we show that ATO-based harmonization enhances detection power in group comparisons relative to ComBat, while preserving valid statistical inference.

