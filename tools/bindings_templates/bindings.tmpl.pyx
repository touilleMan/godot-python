from _godot cimport gdapi
from godot.gdnative_api_struct cimport *

### Classes ###

{% include "classes.tmpl.pyx" %}

### Singletons ###

{% include "singletons.tmpl.pyx" %}

### Global constants ###

{% include "global_constants.tmpl.pyx" %}
