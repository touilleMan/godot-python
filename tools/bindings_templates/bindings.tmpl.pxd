{% from 'class.tmpl.pxd' import render_class_pxd %}
from _godot cimport gdapi
from godot.gdnative_api_struct cimport *

{% for cls in classes %}
{{ render_class_pxd(cls) }}
{% endfor %}
