{{ api.route }}
{% for letter in api.route %}={% endfor %}

{% block original %}
{{ api.doc }}
{% endblock %}

{% block api %}
{% for section in api.sections %}
``{{section}}``

{% endfor %}
{% endblock %}