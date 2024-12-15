---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}



## Privacy-preserving A/B testing
<a href="https://arxiv.org/abs/2411.09064">Minimax optimal two-sample testing under local differential privacy</a>
<br />
<small><u>Jongmin Mun</u>, Seungwoo Kwak, Ilmun Kim (2024). submitted to **Journal of Machine Learning Research**.</small>

## Statistical learning under class imbalance <small>$^*$:Co-first author.</small>

<a href="https://doi.org/10.1016/j.csda.2024.108078">Weighted support vector machine for extremely imbalanced data</a>
<br />
<small><u>Jongmin Mun</u>, Sungwan Bang, Jaeoh Kim (2025). **Computational Statistics & Data Analysis**. [(distributable version)](http://Jong-Min-Moon.github.io/files/preprint_gswsvm.pdf)
</small>
<br />
Data augmentation and loss function adjustments are two common techniques for imbalanced classification. In cases of extreme class imbalance, it is often standard practice to combine these two approaches. However, determining the optimal oversampling ratio and the degree of asymmetry in the loss function typically relies on heuristics. We further consider the scenario where the minority class consists of subgroups and propose a straightforward method for combining data augmentation and loss function adjustments. This method serves as a sample-based approximation of the population-level asymptotically Bayes optimal oracle procedure.
<br />
<br />

<a href="https://doi.org/10.1007/s00357-024-09467-1">Prediction of forest fire risk for artillery military training using weighted support vector machine for imbalanced data</a>
<br />
<small>Ji Hyun Nam<sup>\*</sup>, 
<u>Jongmin Mun</u>
<sup>\*</sup> , Seongil Jo, Jaeoh Kim (2024). **Journal of Classification**.  [(distributable version)](http://Jong-Min-Moon.github.io/files/manuscript_joc.pdf)</small>
<br />
Artillery training inherently poses wildfire risks. Predictive modeling of these wildfires faces two key challenges: the scarcity of wildfire cases and the limited granularity of meteorological data during training. We address the first challenge by augmenting the data using a Gaussian mixture generative model and adjusting the loss function of a support vector machine. To tackle the second challenge, we integrate the Republic of Korea Army (ROKA) dataset with the Korea Meteorological Administration database. Our resulting model achieves a 99% improvement in balanced classification metrics compared to previous models.
<br />
<br />

<a href="https://doi.org/10.1016/j.neuroimage.2024.120956">Sex differences in autism spectrum disorder using class imbalance adjusted functional connectivity</a>
<br />
<small>
 Jong Young Namgung<sup>\*</sup>, 
<u>Jongmin Mun</u><sup>\*</sup>,Yeongjun Park,  Jaeoh Kim, Bo-yong Park (2024). **Neuroimage**.</small>
<br />
Detecting sex differences in brain connectome organization in autism spectrum disorder (ASD) through statistical hypothesis testing is challenging. This challenge arises from the reliance of statistical power on the smaller group size, coupled with the significant imbalance in diagnostic ratios of ASD between males and females. While <a href="https://doi.org/10.1080/01621459.2013.800763">Chen et al. (2013, Journal of the American Statistical Association)</a> addressed this issue using an ensemble of undersampling approaches, we take an alternative approach: oversampling. 

Our method combines dimension reduction via diffusion map embedding with Gaussian mixture model-based oversampling to balance the sex ratio in functional connectivity data. This approach reveals significant sex-related differences in the sensorimotor, attention, and default mode networks, with gradients linked to higher-order cognitive control. Transcriptomic analysis identifies gene enrichment in the cortex, thalamus, and striatum. Notably, gradient-symptom associations differ by sex, with stronger effects observed in females. These findings highlight the sex heterogeneity in ASD's large-scale brain networks.
<br />
<br />
## Scientific collaboration


<a href="https://doi.org/10.1038/s41467-024-45768-0">In-vivo integration of soft neural probes through high-resolution printing of liquid electronics on the cranium</a>
<br />
<small>
Young-Geun Park, Yong Won Kwon, Chin Su Koh, Enji Kim, Dong Ha Lee, Sumin Kim, <u>Jongmin Mun</u>, Yeon-Mi Hong, Sanghoon Lee, Ju-Young Kim, Jae-Hyun Lee, Hyun Ho Jung, Jinwoo Cheon, Jin Woo Chang, Jang-Ung Park (2024). **Nature Communications**.</small>


{% include module.html image_path="http://Jong-Min-Moon.github.io/files/image_nature_comm.png" title="Some title text" description="We present a soft, conformable neural interface system for long-term, stable monitoring of single-unit neural activity in freely moving subjects. The system integrates soft neural probes in the brain with liquid metal-based electronics printed on the cranial surface. In-vivo mouse studies, leveraging dimension reduction, clustering analysis and goodness-of-fit testing, statistically demonstrate stable 33-week neural recording and behavior-induced activation across multiple brain regions during T-maze tests." %}