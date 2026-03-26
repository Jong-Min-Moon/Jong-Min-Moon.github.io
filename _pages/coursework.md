---
layout: page
title: Coursework
permalink: /coursework/
description: Summary of coursework and related projects.
nav: false

display_categories: [stat, opt, cs, math]
horizontal: true
---

<!-- pages/coursework.md -->
<div class="projects">
{%- if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized coursework -->
  <div class="project-filters">
      <button class="filter-btn active" data-filter="all">All</button>
      {%- for category in page.display_categories %}
      <button class="filter-btn" data-filter="{{ category }}">{{ category }}</button>
      {%- endfor %}
  </div>
{%- endif -%}

{%- assign sorted_coursework = site.coursework | sort: "importance" -%}
<!-- Generate cards for each coursework -->
{% if page.horizontal -%}
<div class="container">
  <div class="row row-cols-1">
  {%- for project in sorted_coursework -%}
    {% include coursework_horizontal.html %}
  {%- endfor %}
  </div>
</div>
{%- else -%}
<div class="grid">
  {%- for project in sorted_coursework -%}
    {% include coursework.html %}
  {%- endfor %}
</div>
{%- endif -%}

</div>

<!-- Filter Script -->
<script src="{{ '/assets/js/projects.js' | relative_url }}"></script>
