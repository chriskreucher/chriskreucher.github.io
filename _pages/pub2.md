---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---


<div class="wordwrap"> Blah blah blah 1</div>div>

{% if site.author.googlescholar %}
  <div class="wordwrap">You can also find my articles on <a href="{{site.author.googlescholar}}">my Google Scholar profile</a>.</div>
{% endif %}

<div class="wordwrap"> Blah blah blah 2</div>div>


{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
