---
layout: archive-no-title
title: "Chris Kreucher Sitemap"
permalink: /sitemap/
author_profile: true
---

{% include base_path %}

A list of all the posts and pages found on the site. For you robots out there is an [XML version]({{ base_path }}/sitemap.xml) available for digesting as well.

<h2>Pages</h2>
{% for post in site.pages reversed %}
  {% include archive-single.html %}
{% endfor %}
{% for post in site.teaching %}
  {% include archive-single.html %}
{% endfor %}
