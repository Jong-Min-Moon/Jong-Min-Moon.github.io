---
layout: page
title: Travel
permalink: /travel/
nav: true
nav_order: 5
description: A collection of my travel pictures.
---

Welcome to my travel page! Here I will share pictures and stories from my travels across the United States. Click on any state to view photos taken there!

<div class="favorite-photos-section mt-5 mb-5">
  <h3 class="mb-4">My Favorite Moments</h3>
  <div class="row">
  {% for state_page in site.pages %}
    {% if state_page.url contains '/travel/' and state_page.favorite_photos %}
      {% for photo in state_page.favorite_photos %}
        <div class="col-6 col-md-4 mb-4">
          <a href="{{ state_page.url | relative_url }}" class="favorite-photo-link" title="{{ state_page.title }}">
            <div class="favorite-photo-wrapper rounded z-depth-1">
              <img src="{{ 'assets/img/travel/' | append: photo | append: '-thumb.jpg' | relative_url }}" alt="Favorite from {{ state_page.title }}" class="img-fluid w-100 h-100">
              <div class="favorite-photo-overlay">
                <span>{{ state_page.title }}</span>
              </div>
            </div>
          </a>
        </div>
      {% endfor %}
    {% endif %}
  {% endfor %}
  </div>
</div>

<style>
/* Existing Map Styles */
.us-state-map {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 8px;
    max-width: 100%;
    margin: 2rem auto;
}
.state-tile {
    aspect-ratio: 1;
    color: var(--global-bg-color, #ffffff) !important;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    border-radius: 6px;
    transition: transform 0.2s ease, opacity 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.state-tile.visited {
    background-color: var(--global-theme-color, #2698ba);
    cursor: pointer;
}
.state-tile.unvisited {
    background-color: #bbbbbb;
    opacity: 0.6;
    cursor: default;
    pointer-events: none;
}
.state-tile.visited:hover {
    transform: translateY(-2px) scale(1.05);
    opacity: 0.9;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    text-decoration: none;
}

/* Favorite Photos Styles */
.favorite-photo-wrapper {
    aspect-ratio: 4 / 3;
    overflow: hidden;
    position: relative;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.favorite-photo-wrapper img {
    object-fit: cover;
    width: 100%;
    height: 100%;
}
.favorite-photo-link:hover .favorite-photo-wrapper {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.favorite-photo-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
    color: white;
    padding: 10px;
    font-weight: 600;
    opacity: 0;
    transition: opacity 0.2s ease;
}
.favorite-photo-link:hover .favorite-photo-overlay {
    opacity: 1;
}

/* Responsive adjustments for smaller screens */
@media (max-width: 600px) {
    .us-state-map {
        gap: 4px;
    }
    .state-tile {
        font-size: 0.7rem;
        border-radius: 4px;
    }
}
@media (max-width: 400px) {
    .state-tile {
        font-size: 0.6rem;
    }
}
</style>

{% assign visited_urls = "" %}
{% for p in site.pages %}
  {% assign visited_urls = visited_urls | append: p.url | append: "," %}
{% endfor %}
{% for p in site.posts %}
  {% assign visited_urls = visited_urls | append: p.url | append: "," %}
{% endfor %}

<div class="us-state-map">
    <!-- Row 1 -->
    <a href="/travel/alaska/" class="state-tile {% if visited_urls contains '/travel/alaska/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 1; grid-row: 1;" title="Alaska">AK</a>
    <a href="/travel/maine/" class="state-tile {% if visited_urls contains '/travel/maine/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 12; grid-row: 1;" title="Maine">ME</a>
    
    <!-- Row 2 -->
    <a href="/travel/washington/" class="state-tile {% if visited_urls contains '/travel/washington/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 2; grid-row: 2;" title="Washington">WA</a>
    <a href="/travel/idaho/" class="state-tile {% if visited_urls contains '/travel/idaho/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 3; grid-row: 2;" title="Idaho">ID</a>
    <a href="/travel/montana/" class="state-tile {% if visited_urls contains '/travel/montana/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 4; grid-row: 2;" title="Montana">MT</a>
    <a href="/travel/north-dakota/" class="state-tile {% if visited_urls contains '/travel/north-dakota/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 5; grid-row: 2;" title="North Dakota">ND</a>
    <a href="/travel/minnesota/" class="state-tile {% if visited_urls contains '/travel/minnesota/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 6; grid-row: 2;" title="Minnesota">MN</a>
    <a href="/travel/wisconsin/" class="state-tile {% if visited_urls contains '/travel/wisconsin/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 7; grid-row: 2;" title="Wisconsin">WI</a>
    <a href="/travel/michigan/" class="state-tile {% if visited_urls contains '/travel/michigan/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 8; grid-row: 2;" title="Michigan">MI</a>
    <a href="/travel/new-york/" class="state-tile {% if visited_urls contains '/travel/new-york/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 10; grid-row: 2;" title="New York">NY</a>
    <a href="/travel/vermont/" class="state-tile {% if visited_urls contains '/travel/vermont/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 11; grid-row: 2;" title="Vermont">VT</a>
    <a href="/travel/new-hampshire/" class="state-tile {% if visited_urls contains '/travel/new-hampshire/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 12; grid-row: 2;" title="New Hampshire">NH</a>
    
    <!-- Row 3 -->
    <a href="/travel/oregon/" class="state-tile {% if visited_urls contains '/travel/oregon/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 2; grid-row: 3;" title="Oregon">OR</a>
    <a href="/travel/nevada/" class="state-tile {% if visited_urls contains '/travel/nevada/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 3; grid-row: 3;" title="Nevada">NV</a>
    <a href="/travel/wyoming/" class="state-tile {% if visited_urls contains '/travel/wyoming/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 4; grid-row: 3;" title="Wyoming">WY</a>
    <a href="/travel/south-dakota/" class="state-tile {% if visited_urls contains '/travel/south-dakota/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 5; grid-row: 3;" title="South Dakota">SD</a>
    <a href="/travel/iowa/" class="state-tile {% if visited_urls contains '/travel/iowa/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 6; grid-row: 3;" title="Iowa">IA</a>
    <a href="/travel/illinois/" class="state-tile {% if visited_urls contains '/travel/illinois/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 7; grid-row: 3;" title="Illinois">IL</a>
    <a href="/travel/indiana/" class="state-tile {% if visited_urls contains '/travel/indiana/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 8; grid-row: 3;" title="Indiana">IN</a>
    <a href="/travel/ohio/" class="state-tile {% if visited_urls contains '/travel/ohio/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 9; grid-row: 3;" title="Ohio">OH</a>
    <a href="/travel/pennsylvania/" class="state-tile {% if visited_urls contains '/travel/pennsylvania/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 10; grid-row: 3;" title="Pennsylvania">PA</a>
    <a href="/travel/new-jersey/" class="state-tile {% if visited_urls contains '/travel/new-jersey/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 11; grid-row: 3;" title="New Jersey">NJ</a>
    <a href="/travel/massachusetts/" class="state-tile {% if visited_urls contains '/travel/massachusetts/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 12; grid-row: 3;" title="Massachusetts">MA</a>
    
    <!-- Row 4 -->
    <a href="/travel/california/" class="state-tile {% if visited_urls contains '/travel/california/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 2; grid-row: 4;" title="California">CA</a>
    <a href="/travel/utah/" class="state-tile {% if visited_urls contains '/travel/utah/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 3; grid-row: 4;" title="Utah">UT</a>
    <a href="/travel/colorado/" class="state-tile {% if visited_urls contains '/travel/colorado/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 4; grid-row: 4;" title="Colorado">CO</a>
    <a href="/travel/nebraska/" class="state-tile {% if visited_urls contains '/travel/nebraska/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 5; grid-row: 4;" title="Nebraska">NE</a>
    <a href="/travel/missouri/" class="state-tile {% if visited_urls contains '/travel/missouri/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 6; grid-row: 4;" title="Missouri">MO</a>
    <a href="/travel/kentucky/" class="state-tile {% if visited_urls contains '/travel/kentucky/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 7; grid-row: 4;" title="Kentucky">KY</a>
    <a href="/travel/west-virginia/" class="state-tile {% if visited_urls contains '/travel/west-virginia/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 8; grid-row: 4;" title="West Virginia">WV</a>
    <a href="/travel/virginia/" class="state-tile {% if visited_urls contains '/travel/virginia/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 9; grid-row: 4;" title="Virginia">VA</a>
    <a href="/travel/maryland/" class="state-tile {% if visited_urls contains '/travel/maryland/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 10; grid-row: 4;" title="Maryland">MD</a>
    <a href="/travel/connecticut/" class="state-tile {% if visited_urls contains '/travel/connecticut/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 11; grid-row: 4;" title="Connecticut">CT</a>
    <a href="/travel/rhode-island/" class="state-tile {% if visited_urls contains '/travel/rhode-island/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 12; grid-row: 4;" title="Rhode Island">RI</a>
    
    <!-- Row 5 -->
    <a href="/travel/arizona/" class="state-tile {% if visited_urls contains '/travel/arizona/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 3; grid-row: 5;" title="Arizona">AZ</a>
    <a href="/travel/new-mexico/" class="state-tile {% if visited_urls contains '/travel/new-mexico/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 4; grid-row: 5;" title="New Mexico">NM</a>
    <a href="/travel/kansas/" class="state-tile {% if visited_urls contains '/travel/kansas/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 5; grid-row: 5;" title="Kansas">KS</a>
    <a href="/travel/arkansas/" class="state-tile {% if visited_urls contains '/travel/arkansas/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 6; grid-row: 5;" title="Arkansas">AR</a>
    <a href="/travel/tennessee/" class="state-tile {% if visited_urls contains '/travel/tennessee/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 7; grid-row: 5;" title="Tennessee">TN</a>
    <a href="/travel/north-carolina/" class="state-tile {% if visited_urls contains '/travel/north-carolina/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 8; grid-row: 5;" title="North Carolina">NC</a>
    <a href="/travel/south-carolina/" class="state-tile {% if visited_urls contains '/travel/south-carolina/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 9; grid-row: 5;" title="South Carolina">SC</a>
    <a href="/travel/washington-dc/" class="state-tile {% if visited_urls contains '/travel/washington-dc/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 10; grid-row: 5;" title="Washington D.C.">DC</a>
    <a href="/travel/delaware/" class="state-tile {% if visited_urls contains '/travel/delaware/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 11; grid-row: 5;" title="Delaware">DE</a>
    
    <!-- Row 6 -->
    <a href="/travel/oklahoma/" class="state-tile {% if visited_urls contains '/travel/oklahoma/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 5; grid-row: 6;" title="Oklahoma">OK</a>
    <a href="/travel/louisiana/" class="state-tile {% if visited_urls contains '/travel/louisiana/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 6; grid-row: 6;" title="Louisiana">LA</a>
    <a href="/travel/mississippi/" class="state-tile {% if visited_urls contains '/travel/mississippi/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 7; grid-row: 6;" title="Mississippi">MS</a>
    <a href="/travel/alabama/" class="state-tile {% if visited_urls contains '/travel/alabama/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 8; grid-row: 6;" title="Alabama">AL</a>
    <a href="/travel/georgia/" class="state-tile {% if visited_urls contains '/travel/georgia/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 9; grid-row: 6;" title="Georgia">GA</a>
    
    <!-- Row 7 -->
    <a href="/travel/texas/" class="state-tile {% if visited_urls contains '/travel/texas/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 5; grid-row: 7;" title="Texas">TX</a>
    <a href="/travel/florida/" class="state-tile {% if visited_urls contains '/travel/florida/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 9; grid-row: 7;" title="Florida">FL</a>
    
    <!-- Row 8 -->
    <a href="/travel/hawaii/" class="state-tile {% if visited_urls contains '/travel/hawaii/' %}visited{% else %}unvisited{% endif %}" style="grid-column: 2; grid-row: 8;" title="Hawaii">HI</a>
</div>
