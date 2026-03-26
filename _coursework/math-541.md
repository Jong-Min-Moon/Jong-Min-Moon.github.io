---
layout: project
title: "Math 541: Graduate Mathematical Statistics I & II"
description: "Foundational sequences in graduate mathematical statistics covering probability, estimation, hypothesis testing, and asymptotics."
importance: 1
category: stat
project_handle: math-541
course_number: Math 541A/B, STA6010
institution: USC, Yonsei University
course_level: Graduate
---

# Objectives and Overview
This coursework page combines materials and notes for the core graduate mathematical statistics sequence at USC:
- **Math 541A:** Graduate Mathematical Statistics I (Spring 2024)
- **Math 541B:** Graduate Mathematical Statistics II (Fall 2024)
and core graduate mathematical statistics courses at Yonsei University:

- **STA6010**: Graduate Mathematical Statistics I (Spring 2022)


# Topics

1. **Probability Foundations:** Probability spaces, random variables, expectations, inequalities, convergence modes.
2. **Distribution Theory:** Transformations, families of distributions (exponential families, location-scale families), sufficient statistics, ancillary statistics, complete statistics.
3. **Point Estimation:** Methods of estimation (Method of moments, Maximum likelihood), criteria for evaluating estimators (MSE, UMVUE).
4. **Information Inequality:** Cramér-Rao lower bound, Fisher Information.

5. **Hypothesis Testing:** Neyman-Pearson Lemma, Uniformly Most Powerful (UMP) tests, Likelihood ratio tests.
6. **Confidence Intervals:** Inverting test statistics, pivotal quantities.
7. **Asymptotic Theory:** Delta method, asymptotic relative efficiency, asymptotics of MLEs and likelihood ratio tests.
8. **Advanced Topics:** Bayesian analysis basics, minimax estimation, and nonparametric methods.

---

# Related Posts

<div class="projects">
{% assign category_posts = site.categories['math-541'] | reverse %}

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
