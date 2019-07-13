from _godot cimport gdapi
from godot.gdnative_api_struct cimport *

{% include "global_constants.tmpl.pyx" %}
{% include "classes.tmpl.pyx" %}
{% include "singletons.tmpl.pyx" %}
