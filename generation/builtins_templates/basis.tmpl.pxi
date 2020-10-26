{%- block pxd_header -%}
{%- endblock -%}
{%- block pyx_header -%}

cdef inline Basis Basis_multiply_vector(Basis self, Basis b):
    cdef Basis ret  = Basis.__new__(Basis)
    {{ force_mark_rendered("godot_basis_operator_multiply_vector") }}
    ret._gd_data = gdapi10.godot_basis_operator_multiply_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Basis Basis_multiply_scalar(Basis self, godot_real b):
    cdef Basis ret  = Basis.__new__(Basis)
    {{ force_mark_rendered("godot_basis_operator_multiply_scalar") }}
    ret._gd_data = gdapi10.godot_basis_operator_multiply_scalar(&self._gd_data, b)
    return ret

{%- endblock %}

@cython.final
cdef class Basis:
{% block cdef_attributes %}
    cdef godot_basis _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, Vector3 x not None=Vector3.RIGHT, Vector3 y not None=Vector3.UP, Vector3 z not None=Vector3.BACK):
        {{ force_mark_rendered("godot_basis_new") }} {# We always use the `with_rows` version #}
        {{ force_mark_rendered("godot_basis_new_with_rows") }}
        gdapi10.godot_basis_new_with_rows(&self._gd_data, &(<Vector3>x)._gd_data, &(<Vector3>y)._gd_data, &(<Vector3>z)._gd_data)

    @staticmethod
    def from_euler(from_):
        cdef Basis ret = Basis.__new__(Basis)
        try:
            {{ force_mark_rendered("godot_basis_new_with_euler") }}
            gdapi10.godot_basis_new_with_euler(&ret._gd_data, &(<Vector3?>from_)._gd_data)
            return ret
        except TypeError:
            pass
        try:
            {{ force_mark_rendered("godot_basis_new_with_euler_quat") }}
            gdapi10.godot_basis_new_with_euler_quat(&ret._gd_data, &(<Quat?>from_)._gd_data)
            return ret
        except TypeError:
            raise TypeError('`from_` must be Quat or Vector3')

    @staticmethod
    def from_axis_angle(Vector3 axis not None, phi):
        cdef Basis ret = Basis.__new__(Basis)
        {{ force_mark_rendered("godot_basis_new_with_axis_and_angle") }}
        gdapi10.godot_basis_new_with_axis_and_angle(&ret._gd_data, &axis._gd_data, phi)
        return ret

    def __repr__(self):
        return f"<Basis({self.as_string()})>"

    @property
    def x(Basis self) -> Vector3:
        cdef Vector3 ret = Vector3.__new__(Vector3)
        {{ force_mark_rendered("godot_basis_get_axis") }}
        ret._gd_data = gdapi10.godot_basis_get_axis(&self._gd_data, 0)
        return ret

    @x.setter
    def x(Basis self, Vector3 val not None) -> None:
        {{ force_mark_rendered("godot_basis_set_axis") }}
        gdapi10.godot_basis_set_axis(&self._gd_data, 0, &val._gd_data)

    @property
    def y(Basis self) -> Vector3:
        cdef Vector3 ret = Vector3.__new__(Vector3)
        {{ force_mark_rendered("godot_basis_get_axis") }}
        ret._gd_data = gdapi10.godot_basis_get_axis(&self._gd_data, 1)
        return ret

    @y.setter
    def y(Basis self, Vector3 val not None) -> None:
        {{ force_mark_rendered("godot_basis_set_axis") }}
        gdapi10.godot_basis_set_axis(&self._gd_data, 1, &val._gd_data)

    @property
    def z(Basis self) -> Vector3:
        cdef Vector3 ret = Vector3.__new__(Vector3)
        {{ force_mark_rendered("godot_basis_get_axis") }}
        ret._gd_data = gdapi10.godot_basis_get_axis(&self._gd_data, 2)
        return ret

    @z.setter
    def z(Basis self, Vector3 val not None) -> None:
        {{ force_mark_rendered("godot_basis_set_axis") }}
        gdapi10.godot_basis_set_axis(&self._gd_data, 2, &val._gd_data)

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method("operator_add", py_name="__add__") | indent }}
    {{ render_method("operator_subtract", py_name="__sub__") | indent }}

    def __mul__(Basis self, val):
        cdef Basis _val

        try:
            _val = <Basis?>val

        except TypeError:
            return Basis_multiply_scalar(self, val)

        else:
            return Basis_multiply_vector(self, _val)

    {{ render_method("as_string") | indent }}
    {{ render_method("inverse") | indent }}
    {{ render_method("transposed") | indent }}
    {{ render_method("orthonormalized") | indent }}
    {{ render_method("determinant") | indent }}
    {{ render_method("rotated") | indent }}
    {{ render_method("scaled") | indent }}
    {{ render_method("get_scale") | indent }}
    {{ render_method("get_euler") | indent }}
    {{ render_method("get_quat") | indent }}
    {{ render_method("set_quat") | indent }}
    {{ render_method("set_axis_angle_scale") | indent }}
    {{ render_method("set_euler_scale") | indent }}
    {{ render_method("set_quat_scale") | indent }}
    {{ render_method("tdotx") | indent }}
    {{ render_method("tdoty") | indent }}
    {{ render_method("tdotz") | indent }}
    {{ render_method("xform") | indent }}
    {{ render_method("xform_inv") | indent }}
    {{ render_method("get_orthogonal_index") | indent }}
    {{ render_method("get_elements") | indent }}
    {{ render_method("get_row") | indent }}
    {{ render_method("set_row") | indent }}
    {{ render_method("slerp") | indent }}
{% endblock %}
