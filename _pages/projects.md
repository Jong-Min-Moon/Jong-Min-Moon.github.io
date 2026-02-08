---
layout: page
title: Projects
permalink: /projects/
description: Working papers that have not yet been published in journals, conferences, or on arXiv, often originating from course projects or personal explorations.  Also includes data analysis projects that are featured in the published research.
nav: true
nav_order: 2
display_categories: [causal inference, reinforcement learning/bandits, computational neuroscience, differential privacy, nonparametric statistics, high-dimensional statistics, class imbalance]
horizontal: true
---

<!-- pages/projects.md -->
<div class="projects">
  {%- if site.enable_project_categories and page.display_categories %}
    <!-- Display categorized projects -->
    <div class="project-filters">
        <button class="filter-btn active" data-filter="all">All</button>
        {%- for category in page.display_categories %}
        <button class="filter-btn" data-filter="{{ category }}">{{ category }}</button>
        {%- endfor %}
    </div>
  {%- endif -%}

  {%- assign sorted_projects = site.projects | sort: "importance" -%}
  <!-- Generate cards for each project -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-1">
    {%- for project in sorted_projects -%}
      {% include projects_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for project in sorted_projects -%}
      {% include projects.html %}
    {%- endfor %}
  </div>
  {%- endif -%}

</div>

<!-- Filter Script -->
<script src="{{ '/assets/js/projects.js' | relative_url }}"></script>
