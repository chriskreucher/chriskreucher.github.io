---
layout: archive
permalink: /teaching/
author_profile: true
---

{% include base_path %}

From September 1998 until August 2002, I was an adjunct lecturer in the Electrical 
and Computer Engineering Department at the University of Michigan - Dearborn, where 
I taught ECE 210, ECE 273, ECE 365, ECE 460, and ECE 500 at one time or another. 
Students are directed to these links which contain solutions to old quizzes, exams, 
homeworks, and lab assignments.

{% for post in site.teaching %}
  {% include archive-single.html %}
{% endfor %}
