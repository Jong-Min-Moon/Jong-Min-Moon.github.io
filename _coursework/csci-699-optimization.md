---
layout: project
title: "Trustworthy Machine Learning from an Optimization Lens"
description: "Optimization techniques for modern considerations such as privacy, robustness and fairness in machine learning."
importance: 1
category: cs
project_handle: csci-699-optimization
course_number: CSCI 699
institution: USC
course_level: Graduate
---

  

## Course Description and Objectives
Optimization techniques lie at the heart of how models are trained and developed. In this course, we will explore modern considerations such as privacy, robustness and fairness, particularly from the standpoint of optimization techniques. We will both discuss recent research work on formalizing these societal requirements, and algorithmic solutions for obtaining them. Optimization-based approaches such as differentially private optimization, minimax and constrained optimization are particularly useful toolboxes for these problems, and will be explored in this context.

## Recommended Preparation
Machine learning knowledge (at the level of CSCI 567, CSCI 467, or ISE 529 is sufficient) using Python. Basic optimization knowledge, basic probability and linear algebra concepts. Mathematical maturity to read research papers.

## Syllabus and Materials
The following is a tentative schedule. We will post lecture notes and assignments here. Additional related reading for all lectures will be posted on ed discussion after the lecture.

| Lecture | Topics | Lecture notes | Homework |
| :--- | :--- | :--- | :--- |
| **1, 08/27** | Course introduction, ML basics, Adversarial examples, Finding adversarial examples, Adversarial training | Lecture slides | |
| **2, 09/03** | Certified robustness, randomized smoothing, data poisoning<br>Paper presentations:<br>(1) Recent Advances in Algorithmic High-Dimensional Robust Statistics (also see Robustness Meets Algorithms)<br>(2) Jailbreaking Black Box Large Language Models in Twenty Queries | Lecture slides | |
| **3, 09/10** | Undetectable backdoors, tradeoffs in adversarial robustness<br>Paper presentations:<br>(1) Deliberative Alignment: Reasoning Enables Safer Language Models (briefly cover Adversarial Reasoning at Jailbreaking Time)<br>(2) Do ImageNet Classifiers Generalize to ImageNet?<br>(3) Accuracy on the Line: On the Strong Correlation Between Out-of-Distribution and In-Distribution Generalization (briefly cover Accuracy on the wrong line: On the pitfalls of noisy data for out-of-distribution generalisation) | Lecture slides | |
| **4, 09/17** | Robust and non-robust features, distributional robustness, introduction to algorithmic fairness<br>Paper presentations:<br>(1) Discrimination in the Age of Algorithms<br>(2) First-Person Fairness in Chatbots | Lecture slides | HW1 |
| **5, 09/24** | Fairness notions in classification, individual fairness, group fairness, case study of fairness notions<br>Paper presentations:<br>(1) Performative Prediction<br>(2) The Value of Prediction in Identifying the Worst-Off | Lecture slides | |
| **6, 10/01** | Inherent tradeoffs between notions, individual fairness via uncertainty quantification, multicalibration<br>Paper presentations:<br>(1) Delayed Impact of Fair Machine Learning<br>(2) Avoiding Discrimination through Causal Reasoning<br>(3) Why Language Models Hallucinate (also see Calibrated Language Models Must Hallucinate) | Lecture slides | |
| **7, 10/08** | Review of iteration complexity analysis: smooth convex, strongly convex, and nonconvex | Lecture slides | Project proposal due |
| **8, 10/15** | Privacy and membership inference attacks<br>Paper presentations:<br>(1) Robust De-anonymization of Large Datasets (also see Resolving Individuals Contributing Trace Amounts of DNA)<br>(2) Model Inversion Attacks (also see Membership Inference Attacks Against Machine Learning Models) | Lecture slides | |
| **9, 10/22** | Differential privacy and its basic properties<br>Paper presentations:<br>(1) Learning with Privacy at Scale at Apple<br>(2) Scalable Extraction of Training Data from (Production) Language Models | Lecture slides | HW1 due |
| **10, 10/29** | DP mechanisms and properties of DP<br>Paper presentations:<br>(1) Semi-supervised Knowledge Transfer for Deep Learning from Private Training Data (PATE)<br>(2) Deep Learning with Differential Privacy (DP-SGD)<br>(3) Extracting Training Data from Diffusion Models | Lecture slides | |
| **11, 11/05** | DP optimization: output perturbation, objective perturbation, and exponential mechanism<br>Paper presentations:<br>(1) Scaling Laws for Differentially Private Language Models<br>(2) Renyi Differential Privacy<br>(3) Differentially Private Fine-tuning of Language Models | Lecture slides | |
| **12, 11/12** | DP optimization: DP-SGD and its variants<br>Paper presentations:<br>(1) Privacy Auditing with One Training Run<br>(2) Large Language Models Can Be Strong Differentially Private Learners (Ghost Clipping)<br>(3) Inverting Gradients - How easy is it to break privacy in federated learning? (also see Deep Leakage from Gradients) | Lecture slides | |
| **13, 11/19** | Project presentations | | |
| **14, 12/03** | Project presentations | | HW2 due |

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
