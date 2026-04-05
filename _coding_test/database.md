---
layout: project
title: "Database"
description: "Undergraduate course introducing Python programming for business analytics, covering data collection, processing, statistical analyses, and machine learning fundamentals."
importance: 1
category: cs
project_handle: database
---
 


 

# Related Posts

<div class="projects">
{% assign category_posts = site.categories['database'] | reverse %}

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

  <style>
    .post-list {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      width: 100%;
    }
    .post-list-item {
      width: 100%;
      display: block;
    }
    .post-list-item .post-link {
      text-decoration: none;
      color: inherit;
      display: block;
      width: 100%;
    }
    .post-list-item .card {
      width: 100%;
      margin-bottom: 0 !important;
      border-radius: 8px;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .post-list-item .card-body {
      padding: 1.5rem;
    }
    .post-list-item .card-title {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }
    .post-list-item .post-date {
      color: var(--global-text-color-light, #6c757d);
      font-size: 0.9rem;
      margin-bottom: 1rem;
    }
  </style>

  <div class="post-list">
    {% for post in category_posts %}
      <div class="card-item post-list-item" data-category="{{ post.tags | jsonify | escape }}">
        {% if post.redirect -%}
        <a href="{{ post.redirect }}" class="post-link">
        {%- else -%}
        <a href="{{ post.url | relative_url }}" class="post-link">
        {%- endif %}
          <div class="card hoverable">
            <div class="card-body">
              <h3 class="card-title text-lowercase">{{ post.title }}</h3>
              <div class="post-date">{{ post.date | date: "%B %-d, %Y" }}</div>
              <p class="card-text">{{ post.description }}</p>
              <div class="row ml-1 mr-1 p-0 mt-3">
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
