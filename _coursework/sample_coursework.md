---
layout: project
title: Sample Coursework Project
description: This is a sample coursework project to demonstrate the new Coursework tab.
img: assets/img/pomdp.png
importance: 1
category: cs
project_handle: sample-coursework
course_number: BUAD 311
institution: USC Marshall
course_level: Undergraduate
---

This is a sample coursework project description.
You can include any markdown content here.

- Feature 1
- Feature 2

It also supports related posts if you set `project_handle` and use `project: sample-coursework` in your blog posts.

---

# Related Posts

<div class="projects">
{% assign category_posts = site.categories['sample-coursework'] | reverse %}

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
