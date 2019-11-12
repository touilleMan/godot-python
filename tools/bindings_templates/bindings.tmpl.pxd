{% from 'class.tmpl.pxd' import render_class_pxd %}
from godot.hazmat cimport gdapi
from godot.hazmat.gdnative_api_struct cimport *

{% for cls in classes %}
{{ render_class_pxd(cls) }}
{% endfor %}
