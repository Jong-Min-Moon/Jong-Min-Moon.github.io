---
layout: page
title: Data Fusion for High-Resolution Estimation using score based diffusion
description: A new project on data fusion for high-resolution estimation using score based diffusion.
importance: 1
category: [data fusion, machine learning]
---

# Introduction

Description of the project goes here.

<br>
## Related Posts
<div class="posts">
  <div class="table-responsive">
    <table class="table table-sm table-borderless">
    {% assign related_posts = site.posts | where: "project", "data-fusion" %}
    {% for item in related_posts %}
      <tr>
        <th scope="row" style="width: 20%">{{ item.date | date: "%b %-d, %Y" }}</th>
        <td>
          <a class="news-title" href="{{ item.url | relative_url }}">{{ item.title }}</a>
        </td>
      </tr>
    {% endfor %}
    </table>
  </div>
</div>
