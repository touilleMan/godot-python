{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class Plane:
{% block cdef_attributes %}
    cdef godot_plane _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, godot_real a, godot_real b, godot_real c, godot_real d):
        {{ force_mark_rendered("godot_plane_new_with_reals") }}
        gdapi10.godot_plane_new_with_reals(&self._gd_data, a, b, c, d)

    @staticmethod
    def from_vectors(Vector3 v1 not None, Vector3 v2 not None, Vector3 v3 not None):
        cdef Plane ret = Plane.__new__(Plane)
        {{ force_mark_rendered("godot_plane_new_with_vectors") }}
        gdapi10.godot_plane_new_with_vectors(&ret._gd_data, &v1._gd_data, &v2._gd_data, &v3._gd_data)
        return ret

    @staticmethod
    def from_normal(Vector3 normal not None, godot_real d):
        cdef Plane ret = Plane.__new__(Plane)
        {{ force_mark_rendered("godot_plane_new_with_normal") }}
        gdapi10.godot_plane_new_with_normal(&ret._gd_data, &normal._gd_data, d)
        return ret

    def __repr__(Plane self):
        return f"<Plane({self.as_string()})>"

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method("operator_neg", py_name="__neg__") | indent }}

    def __pos__(Plane self):
        return self

    {{ render_property("normal", getter="get_normal", setter="set_normal") | indent }}
    {{ render_property("d", getter="get_d", setter="set_d") | indent }}

    {{ render_method("as_string") | indent }}
    {{ render_method("normalized") | indent }}
    {{ render_method("center") | indent }}
    {{ render_method("get_any_point") | indent }}
    {{ render_method("is_point_over") | indent }}
    {{ render_method("distance_to") | indent }}
    {{ render_method("has_point") | indent }}
    {{ render_method("project") | indent }}

    def intersects_segment(Plane self, Vector3 begin not None, Vector3 end not None):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        {{ force_mark_rendered("godot_plane_intersects_segment") }}
        if gdapi10.godot_plane_intersects_segment(&self._gd_data, &ret._gd_data, &begin._gd_data, &end._gd_data):
            return ret
        else:
            return None

    def intersects_ray(Plane self, Vector3 from_ not None, Vector3 dir not None):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        {{ force_mark_rendered("godot_plane_intersects_ray") }}
        if gdapi10.godot_plane_intersects_ray(&self._gd_data, &ret._gd_data, &from_._gd_data, &dir._gd_data):
            return ret
        else:
            return None

    def intersect_3(Plane self, Plane b not None, Plane c not None):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        {{ force_mark_rendered("godot_plane_intersect_3") }}
        if gdapi10.godot_plane_intersect_3(&self._gd_data, &ret._gd_data, &b._gd_data, &c._gd_data):
            return ret
        else:
            return None

    {{ render_method("set_normal") | indent }}
    {{ render_method("get_normal") | indent }}
    {{ render_method("get_d") | indent }}
    {{ render_method("set_d") | indent }}
{% endblock %}

{%- block python_consts %}
    PLANE_YZ = Plane(1, 0, 0, 0)
    PLANE_XZ = Plane(0, 1, 0, 0)
    PLANE_XY = Plane(0, 0, 1, 0)
{% endblock %}
