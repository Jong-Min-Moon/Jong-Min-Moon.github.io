---
layout: page
title: Coursework
permalink: /coursework/
description: Summary of coursework and related projects.
nav: true
nav_order: 3
display_categories: [core, elective]
horizontal: true
---

<!-- pages/coursework.md -->
<div class="projects">
{%- if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized coursework -->
  {%- for category in page.display_categories %}
  <h2 class="category">{{ category }}</h2>
  {%- assign categorized_coursework = site.coursework | where: "category", category -%}
  {%- assign sorted_coursework = categorized_coursework | sort: "importance" %}
  <!-- Generate cards for each coursework -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-1">
    {%- for project in sorted_coursework -%}
      {% include projects_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for project in sorted_coursework -%}
      {% include projects.html %}
    {%- endfor %}
    </div>
  {%- endif -%}
  {% endfor %}

{%- else -%}
<!-- Display coursework without categories -->
  {%- assign sorted_coursework = site.coursework | sort: "importance" -%}
  <!-- Generate cards for each coursework -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-1">
    {%- for project in sorted_coursework -%}
      {% include projects_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for project in sorted_coursework -%}
      {% include projects.html %}
    {%- endfor %}
    </div>
  {%- endif -%}
{%- endif -%}
</div>
