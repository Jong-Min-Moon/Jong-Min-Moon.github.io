---
layout: page
title: Private and Scalable Hash Kernel Bit-flip Two-Sample Testing
description: We propose using Hash Kernels to compress high-dimensional data before bit-flip privatization, making locally private A/B testing viable for massive, unknown alphabets.
img: assets/img/hash.png
importance: 2
category: coursework
---
 
**Mun et al. (2025)** proposed a minimax optimal two-sample (A/B) testing algorithm under local differential privacy (LDP). However, a key challenge arises when dealing with high-dimensional datasets, such as images or text, where the domain size $k$ is massive or unknown.

The resulting multinomial distribution implies that the entry-wise perturbation method of **Mun et al. (2025)**, which relies on a variant of **Erlingsson et al. (2014)**, introduces excessive noise relative to the signal, significantly reducing testing power. Furthermore, conventional dimension reduction methods like PCA are not directly applicable in the LDP setting, as individual data owners cannot access the global covariance structure.

Since the test statistic relies on the Euclidean inner product—a simple linear kernel—we propose utilizing the hash kernel approximation from **Shi et al. (2009)** to enhance scalability. We present a modified LDP algorithm that projects high-dimensional data into a lower-dimensional sketch before noise injection. This approach enables efficient computation and handles unknown alphabet sizes while preserving the core geometric structure required for the two-sample test.

This project began as the final assignment for CSCI-699: Privacy-Preserving Machine Learning, offered at USC in Fall 2024. The core idea of using hashing  was suggested by Sai Praneeth Karimireddy, the lecturer of the course and an assistant professor of computer science at USC.
You can also check out the full paper [here](https://jong-min.org/assets/pdf/preprint_hash.pdf).

### References

* **Mun, J., Kwak, M., & Kim, I.** (2025). Minimax optimal two-sample testing under local differential privacy. *Journal of Machine Learning Research*.
* **Erlingsson, Ú., Pihur, V., & Korolova, A.** (2014). RAPPOR: Randomized aggregatable privacy-preserving ordinal response. *ACM CCS*.
* **Shi, Q., Petterson, J., Drezde, G., Li, X., Smola, A., & Vishwanathan, S.** (2009). Hash kernels for structured data. *Journal of Machine Learning Research*.
