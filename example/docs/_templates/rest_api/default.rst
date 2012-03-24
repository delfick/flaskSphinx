{% extends "flaskSphinx_templates/rest_api/default.rst" %}

{% block api %}
{{ super() }}

{% if api.view.requires_things %}
This view requires things!
{% endif %}

{% if api.special %}
This view is Special!
{% endif %}
{% endblock %}