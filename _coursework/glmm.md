---
layout: project
title: "Generalized Linear Mixed Models"
description: "Theory and data analysis methods for Generalized Linear Mixed Models (GLMM), extending regression to exponential families and random effects."
img: assets/img/publication_preview/glmm.png
importance: 2
category: core
project_handle: glmm
course_number: STA6640
institution: Yonsei University
course_level: Graduate
---

## Course Goals and Overview
This course covers the theory and data analysis methods of **Generalized Linear Mixed Models (GLMM)**. 
GLMM is fundamentally an extension of regression analysis:
1.  **Response Variable Extension**: Extends from normal distribution to distributions in the **exponential family**.
    *   Binomial distribution $\rightarrow$ Logistic regression
    *   Poisson distribution $\rightarrow$ Poisson regression
2.  **Predictor Variable Extension**: Extends to include not only **fixed effects** but also **random effects**.

Through these extensions, students will study **Covariance Pattern Models** and **Random Coefficient Models (Hierarchical Models)**, and learn how to analyze **Longitudinal Data**.

## Prerequisites
Enrollment is restricted to students who have completed the following prerequisite courses. Verification of grades in the first class is required.
1.  **Undergraduate Mathematical Statistics II** or **Graduate Mathematical Statistics**
2.  **Undergraduate Regression Analysis** or **Graduate Linear Models**

## Course Operation
*   **2 Hours**: Pre-recorded video lectures uploaded to RunUs. Students can watch at their convenience.
*   **1 Hour**: Real-time interaction with students via Zoom.
*   **Focus**: Lectures will be based on the instructor's notes. The course will focus on case studies analyzing various models using **SAS**.


## Instructor Information
*   **Instructor**: Prof. Seung-Ho Kang

## Topics
- One-way classifications
- Single-predictor regression
- Linear models
- Generalized linear models
- Linear mixed models
- Generalized linear mixed models
- Models for longitudinal data

---

# Related Posts

<div class="projects">
{% assign category_posts = site.categories['glmm'] | reverse %}

{% if category_posts.size > 0 %}
  <!-- Collect all unique tags -->
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

  <!-- Filter Script -->
  <script src="{{ '/assets/js/projects.js' | relative_url }}"></script>
{% else %}
  <p>No posts found for this course yet.</p>
{% endif %}
</div>
