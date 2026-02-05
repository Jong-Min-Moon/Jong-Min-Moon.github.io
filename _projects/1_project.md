---
layout: project
title: Off-Policy Learning in Partially Observed Markov Decision Processes under Sequential Ignorability
description: We stabilize off-policy learning from partially observed health data using a geometry-aware gradient method, improving convergence and policy performance in simulations.
img: assets/img/pomdp.png
importance: 1
category: coursework
project_handle: pomdp-learning
related_publications: einstein1956investigations, einstein1950meaning
---
 

Learning treatment policies from historical mobile health data is challenging due to partial observability and the absence of online experimentation. Off-policy evaluation with history-dependent importance weighting
provides unbiased estimates but induces a highly ill-conditioned, nonconvex objective, making naive gradient-based optimization unstable. We propose a weighted second-moment preconditioned gradient ascent method
that stabilizes learning by accounting for the variance and curvature of
importance-weighted gradients. In simulations motivated by glucose regulation, our method converges faster, reduces variability across runs, and
achieves higher estimated policy values than naive gradient ascent. These
results underscore the importance of geometry-aware optimization in offpolicy learning under partial observability.

You can also check out the full paper [here](https://jong-min.org/assets/pdf/preprint_pomdp.pdf).

This project began as the final assignment for DSO-603: Causal Inference with Modern Machine Learning Methods, offered at USC in Fall 2025. The core idea of transitioning from POMDP OPE to learning was suggested by Donggyu Derek Cho, a PhD student in Statistics at Duke University.
 
