---
layout: project
title: "Privacy-Preserving Machine Learning"
description: "Foundations of privacy-preserving machine learning, focusing on maximizing utility while protecting individual privacy against modern attacks."
importance: 1
category: cs
project_handle: csci-699-privacy
course_number: CSCI 699
institution: USC
course_level: Graduate
---

**Instructor:** Sai Praneeth Karimireddy (karimire@usc.edu)  
**Location:** WPH 102  
**Time:** Fri 1:00 pm - 4:20 pm  

## Course Description
This course focuses on the foundations of privacy-preserving machine learning. Extremely personal data is being collected at an unprecedented scale by ML companies. While training ML models on such confidential data can be highly beneficial, it also comes with huge privacy risks. This course addresses the dual challenge of maximizing the utility of machine learning models while protecting individual privacy. We will cover the following topics: differential privacy; private training of ML models; privacy attacks and audits; federated and decentralized machine learning.

This course will prepare you to rigorously identify, reason about, and manage privacy risks in machine learning. You will learn to design algorithms that protect sensitive information, and to analyze the privacy leakage of any ML system. Additionally, the course will introduce you to cutting-edge research and practical applications. By the end of the course, you will be well-equipped to undertake research and address real-world privacy challenges in machine learning.

*(For providing anonymous feedback at any point in the course, please use the provided anonymous form in the course portal.)*

## Learning Objectives
Upon successful completion of this course, students will be able to:
1. Rigorously identify, reason about, and manage privacy risks in machine learning systems.
2. Design and implement algorithms that protect sensitive information while maximizing model utility.
3. Analyze and audit the privacy leakage of complex machine learning systems.
4. Evaluate cutting-edge research to undertake original research and address real-world privacy challenges.

## Prerequisites
While there are no official prerequisites, knowledge of advanced probability (at the level of MATH 505a), linear algebra and multi-variable calculus (at the level of MATH 225), analysis of algorithms (at the level of CSCI 570), introductory statistics and hypothesis testing (at the level of MATH 308), and machine learning (at the level of CSCI 567) is recommended.

## Syllabus

| Week | Topics/Daily Activities | Additional Readings | Deliverables |
| :--- | :--- | :--- | :--- |
| **Week 1** | **Theory:** Introduction to anonymity and data privacy; Data anonymization techniques; De-anonymization attacks; Linkage and Reconstruction attacks.<br>**Practical:** Implement some linkage attacks. | Zhang et al. 2020. *The Secret Revealer*<br>Haim et al. 2022. *Reconstructing Training Data from Trained Neural Networks*<br>Carlini et al. 2021. *Is Private Learning Possible with Instance Encoding?*<br>Orekondy et al. 2019. *Knockoff Nets* | Lab-1a, Lab-1b, Slides |
| **Week 2** | **Theory:** Differential Privacy; Randomized response; Laplace mechanism; Hypothesis testing interpretation.<br>**Practical:** Implement differential privacy defenses. | Dong et al. 2019. *Gaussian Differential Privacy* | Annotated Slides<br>Homework 1 (due Sep 20) |
| **Week 3** | **Theory:** ML training; gradient descent; SGD.<br>**Practical:** SGD vs. Adam vs. DP-SGD on PyTorch. | Reddi et al. 2019. *On the Convergence of Adam and Beyond*<br>Zhang et al. 2020. *Why are Adaptive Methods Good for Attention Models?*<br>Li et al. 2022. *Private Adaptive Optimization with Side Information* | |
| **Week 4** | **Theory:** Private ML training; DP-SGD; Gaussian DP; Sub-sampling; Composition.<br>**Practical:** Opacus Library for private deep learning. | Abadi et al. 2016. *Deep Learning with Differential Privacy*<br>Kairouz et al. 2021. *Practical and Private (Deep) Learning*<br>Denisov et al 2022. *Improved Differential Privacy for SGD*<br>Cohen et al. 2024. *Data Reconstruction: When You See It and When You Don't* | HW 2 out. |
| **Week 5** | **Theory:** Practical Privacy auditing; Designing powerful membership inference attacks; Measuring the influence of training data.<br>**Practical:** DP-auditing. | Tramer et al. 2022. *Debugging Differential Privacy*<br>Steinke et al. 2024. *Privacy Auditing with One (1) Training Run.*<br>Lesci et al. 2024. *Causal Estimation of Memorisation Profiles*<br>Aerni et al. 2024. *Evaluations of ML Privacy Defenses are Misleading* | HW 2 due before class. |
| **Week 6** | **Theory:** Privacy in LLMs; RLHF/prompt engineering for privacy; Data stealing attacks; private in-context learning.<br>**Practical:** Privacy defending and attacking prompts. | Shi et al. 2024. *Detecting Pretraining Data from LLMs*<br>Nasr et al. 2023. *Scalable Extraction of Training Data*<br>Yu et al. 2024. *Privacy-Preserving Instructions for Aligning LLMs*<br>Wu et al. 2023. *Privacy-Preserving In-Context Learning for LLMs*<br>Debenedetti et al. 2024. *SaTML LLM Capture-the-Flag* | HW 3 out. |
| **Week 7** | **Theory:** Unlearning algorithms; guarantees; Model editing and correcting.<br>**Practical:** Implement unlearning. | Izzo et al 2021. *Approximate Data Deletion from ML Models*<br>Sekhari et al. 2021. *Remember What You Want to Forget*<br>Zhang et al. 2024. *Negative Preference Optimization*<br>Meng et al. 2022. *Locating and Editing Factual Associations in GPT*<br>Pawelczyk et al. 2024. *In-Context Unlearning* | HW 3 due before class. |
| **Week 8** | **Theory:** Decentralized privacy, Local DP.<br>Confidential Computing: Guest lecture by Mengyuan Li<br>**Practical:** Comparing local vs. central DP. | Erlingsson et al. 2014. *RAPPOR*<br>Kasiviswanathan et al. 2011. *What Can We Learn Privately?*<br>Dwork et al. 2006. *Our Data, Ourselves*<br>Eichner et al. 2024. *Confidential Federated Computations* | |
| **Week 9** | **Theory:** Federated learning; challenges due to data heterogeneity, communication compression; Privacy attacks in FL.<br>**Practical:** Federated learning on hospital data. | Wang et al. 2021. *Field Guide to Federated Optimization.*<br>Geiping et al. 2020. *Inverting Gradients*<br>Fowl et al. 2022. *Robbing the Fed* | |
| **Week 10** | **Theory:** Privacy in FL; Secure aggregation; Quantized DP.<br>**Practical:** DPFL vs. Local DP. | Bonawitz et al. 2022. *Federated Learning and Privacy*<br>Bonawitz et al. 2016. *Practical Secure Aggregation for FL*<br>Chen et al. 2022. *The Poisson binomial mechanism*<br>*(Amplified) Banded Matrix Factorization* | |
| **Week 11** | **Theory:** Privacy in Practice; Incentives; Relation to Copyright law. | Brown et al. 2022. *What Does it Mean for a Language Model to Preserve Privacy?*<br>NY Times 2024. *Consent in Crisis*<br>Wei et al. 2024. *Proving membership in LLM pretraining data*<br>Duarte et al. 2024. *DE-COP: Detecting Copyrighted Content*<br>Elkin-Koren et al. 2024. *Can Copyright be Reduced to Privacy?* | |
| **Weeks 12-15** | Student presentations. In-class presentations. Option to schedule earlier in the semester. | | |
| **Final** | Final project report | | Report due on final exam date. |

## Grading
* **Assignments (30%):** 3 assignments. Collaboration is allowed but must be stated. Grades are based on correctness. The theory part should be written in Latex and the coding part in Jupyter Python notebooks.
* **Course Presentation and Project (55%):**
    * *Presentations (25%):* Students will be assigned a paper based on their interest and will present it in class for 30 minutes.
    * *Project (30%):* Students will write a 4-page report on 1-2 papers, which could either be on the paper they presented, supplemented by related readings, or on a different paper(s) of their choice. Pursuing a personal research topic is strongly encouraged.
* **Discussions and Participation (15%):** This will involve reviewing, commenting, and discussing each other's presentations and projects using the role-playing reading group format.

## Resources
There are no required textbooks. The following writeups are excellent supplemental readings and may be used as references:
* C. Dwork and A. Roth. *The Algorithmic Foundations of Differential Privacy*. Foundations and Trends in Theoretical Computer Science, 2014. Reference for DP.
* Nissim et al. *Differential Privacy: A Primer for a Non-technical Audience*. Journal of Entertainment & Technology Law, 2018. Great read with many examples tying legal definitions and privacy in practice.
* Kairouz et al. *Advances and Open Problems in Federated Learning*. Community survey on federated learning.

This course builds on several related courses which can serve as valuable additional references:
* *Privacy-Preserving Machine Learning* by Aurelien Bellet at Inria
* *Trustworthy Machine Learning* by Reza Shokri at NUS
* *Federated and Collaborative Learning* by Virginia Smith at CMU
* *Large Scale Optimization for Machine Learning (ISE 633)* by Meisam Razaviyayn at USC
* *Digital Privacy* by Vitaly Shmatikov at Cornell

---

# Related Posts

<div class="projects">
{% assign category_posts = site.categories['csci-699'] | reverse %}

{% if category_posts.size > 0 %}
  {% assign all_tags = "" | split: "" %}
  {% for post in category_posts %}
    {% for tag in post.tags %}
      {% assign all_tags = all_tags | push: tag %}
    {% endfor %}
  {% endfor %}
  {% assign unique_tags = all_tags | uniq | sort %}

  <div class="project-filters">
      <button class="filter-btn active" data-filter="all">All</button>
      {% for tag in unique_tags %}
      <button class="filter-btn" data-filter="{{ tag }}">{{ tag }}</button>
      {% endfor %}
  </div>

  <div class="grid">
    <div class="grid-sizer"></div>
    {% for post in category_posts %}
      <div class="grid-item" data-category="{{ post.tags | jsonify | escape }}">
        {% if post.redirect -%}
        <a href="{{ post.redirect }}">
        {%- else -%}
        <a href="{{ post.url | relative_url }}">
        {%- endif %}
          <div class="card hoverable">
            <div class="card-body">
              <h2 class="card-title text-lowercase">{{ post.title }}</h2>
              <p class="card-text">{{ post.description }}</p>
              <div class="row ml-1 mr-1 p-0">
                {% for tag in post.tags %}
                  <span class="badge badge-secondary mr-1 mb-1">{{ tag }}</span>
                {% endfor %}
              </div>
            </div>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>

  <script src="{{ '/assets/js/projects.js' | relative_url }}"></script>
{% else %}
  <p>No posts found for this course yet.</p>
{% endif %}
</div>