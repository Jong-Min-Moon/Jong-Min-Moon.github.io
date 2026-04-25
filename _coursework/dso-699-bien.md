---
layout: project
title: "Advanced Data Science: Modeling, Computing, & Optimization"
description: "Ph.D. level course on statistical machine learning, covering the core process from data to model, algorithm, and insight."
importance: 1
category: stat opt
project_handle: dso-699-bien
course_number: DSO 699
institution: USC Marshall
course_level: Graduate
lecturer: Jacob Bien
semester: TBD
---
 

| Week | Topics | Deliverables |
| :--- | :--- | :--- |
| Week 1 | Linear models (linear algebra + normal theory: projection, QR / Gram-Schmidt implications for interpretation of coefficients, SVD + Moore-Penrose) | |
| Week 2 | Dummy coding, interactions, connections to ANOVA | |
| Week 3 | Generalized linear models: Fundamentals... Exponential families + IRLS/Newton-Raphson | |
| Week 4 | Key examples of GLMs | HW 1 due |
| Week 5 | Logistic regression (prospective/retrospective sampling, Bradley-Terry, class imbalance, etc.) + multinomial regression | |
| Week 6 | Count data (Poisson regression, mover-stayer models, connection to multinomial regression via the Poisson trick, overdispersion and the negative binomial) | |
| Week 7 | Designing and solving custom convex regularizers for data modeling (e.g., trend filtering, hierarchical sparse modeling) | HW 2 due |
| Week 8 | Optimization methods for statistical modeling (proximal gradient, coordinate descent) | |
| Week 9 | Optimization methods for statistical modeling (continued; ADMM) | |
| Week 10 | Degrees of freedom and SURE for regularized regression | HW 3 due |
| Week 11 | Nonparametric regression, smoothing splines, generalized additive models | |
| Week 12 | Modeling dependence with covariance estimation | |
| Week 13 | Unsupervised learning: mixture of Gaussians + EM | HW 4 due |
| Week 14 | Unsupervised learning (continued): k-means, hierarchical, and other clustering | |
| Week 15 | Unsupervised learning (continued): PCA and UMAP | R package due |

---

# Related Posts

<div class="projects">
{% assign category_posts = site.categories['dso-699-bien'] | reverse %}

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
