from godot.bindings cimport Resource
{% set py_type = "RID" %}

{% block pxd_header %}
{% endblock %}
{% block pyx_header %}
{% endblock %}


@cython.final
cdef class RID:
{% block cdef_attributes %}
    cdef godot_rid _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, Resource from_=None):
        if from_ is not None:
            gdapi.godot_rid_new_with_resource(
                &self._gd_data,
                from_._gd_ptr
            )
        else:
            gdapi.godot_rid_new(&self._gd_data)

    def __repr__(self):
        return f"<RID(id={self.get_id()})>"

    @staticmethod
    def from_resource(Resource resource not None):
        # Call to __new__ bypasses __init__ constructor
        cdef RID ret = RID.__new__(RID)
        gdapi.godot_rid_new_with_resource(&ret._gd_data, resource._gd_ptr)
        return ret
{% endblock %}

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}
    {{ render_method("get_id", "godot_int") | indent }}
