{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_rid_new(godot_rid* r_dest)
godot_int godot_rid_get_id(godot_rid* p_self)
void godot_rid_new_with_resource(godot_rid* r_dest, godot_object* p_from)
godot_bool godot_rid_operator_equal(godot_rid* p_self, godot_rid* p_b)
godot_bool godot_rid_operator_less(godot_rid* p_self, godot_rid* p_b)
// GDAPI: 1.1
// GDAPI: 1.2
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
from godot.bindings cimport Resource
{% endblock -%}


@cython.final
cdef class RID:
{% block cdef_attributes %}
    cdef godot_rid _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, Resource from_=None):
        if from_ is not None:
            gdapi10.godot_rid_new_with_resource(
                &self._gd_data,
                from_._gd_ptr
            )
        else:
            gdapi10.godot_rid_new(&self._gd_data)

    def __repr__(RID self):
        return f"<RID(id={self.get_id()})>"

    @staticmethod
    def from_resource(Resource resource not None):
        # Call to __new__ bypasses __init__ constructor
        cdef RID ret = RID.__new__(RID)
        gdapi10.godot_rid_new_with_resource(&ret._gd_data, resource._gd_ptr)
        return ret

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}
    {{ render_method(**gd_functions["get_id"]) | indent }}

{% endblock %}

{%- block python_consts %}
{% endblock -%}
