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
            {{ force_mark_rendered("godot_rid_new_with_resource") }}
            gdapi10.godot_rid_new_with_resource(
                &self._gd_data,
                from_._gd_ptr
            )
        else:
            {{ force_mark_rendered("godot_rid_new") }}
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
    {{ render_method("get_id") | indent }}

{% endblock %}

{%- block python_consts %}
{% endblock -%}
