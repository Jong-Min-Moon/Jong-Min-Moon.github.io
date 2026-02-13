---
layout: page
permalink: /publications/
title: Publications
description:  
nav: true
nav_order: 1
display_categories: [causal inference, "reinforcement learning/bandits", computational neuroscience, differential privacy, nonparametric statistics, high-dimensional statistics, class imbalance]
---

<!-- _pages/publications.md -->
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
    {% bibliography -f {{ site.scholar.bibliography }} --group_by none %}
  </div>

</div>

<!-- Filter Script -->
<script src="{{ '/assets/js/projects.js' | relative_url }}"></script>
