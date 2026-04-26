---
layout: page
title: Software
permalink: /software/
description: Software packages and implementations.
nav: true
nav_order: 4
horizontal: true
---

<div class="projects">
  {%- assign sorted_software = site.software | sort: "importance" -%}
  <!-- Generate cards for each software -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-1">
    {%- for project in sorted_software -%}
      {% include projects_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for project in sorted_software -%}
      {% include projects.html %}
    {%- endfor %}
  </div>
  {%- endif -%}
</div>
