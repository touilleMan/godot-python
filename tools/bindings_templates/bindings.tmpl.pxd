{% from 'class.tmpl.pxd' import render_class_pxd %}
from godot_hazmat cimport gdapi
from godot_hazmat.gdnative_api_struct cimport *

{% for cls in classes %}
{{ render_class_pxd(cls) }}
{% endfor %}
