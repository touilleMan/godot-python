{% from 'class.tmpl.pyx' import render_class %}
{% for cls in classes %}
{{ render_class(cls) }}
{% endfor %}
