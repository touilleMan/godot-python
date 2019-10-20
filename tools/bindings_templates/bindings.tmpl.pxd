{% from 'class.tmpl.pxd' import render_class_pxd %}
from godot.gdnative_api_struct cimport *
from godot.hazmat cimport gdapi

{% for cls in classes %}
{{ render_class_pxd(cls) }}
{% endfor %}
