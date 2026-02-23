---
layout: page
permalink: /study/papers/
title: Papers
description: A collection of research papers I've read and found insightful.
nav: false
display_categories: [causal inference, optimization, machine learning]
---

<!-- _pages/reading_list.md -->
<div class="publications">

  {%- if page.display_categories %}
  <!-- Display categorized publications -->
  <div class="project-filters">
    <button class="filter-btn active" data-filter="all">All</button>
    {%- for category in page.display_categories %}
    <button class="filter-btn" data-filter="{{ category }}">{{ category }}</button>
    {%- endfor %}
  </div>
  {%- endif -%}

  <div class="publications-list">
    {% bibliography -f reading_list --group_by none %}
  </div>

</div>

<!-- Filter Script -->
<script src="{{ '/assets/js/projects.js' | relative_url }}"></script>
