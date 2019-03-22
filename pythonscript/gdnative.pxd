# cython: language_level=3

from libc.stdint cimport uint8_t, uint64_t, int64_t, uint32_t


cdef extern from "godot_headers/gdnative/gdnative.h":

    ctypedef enum godot_error:
        GODOT_OK
        GODOT_FAILED
        GODOT_ERR_UNAVAILABLE
        GODOT_ERR_UNCONFIGURED
        GODOT_ERR_UNAUTHORIZED
        GODOT_ERR_PARAMETER_RANGE_ERROR
        GODOT_ERR_OUT_OF_MEMORY
        GODOT_ERR_FILE_NOT_FOUND
        GODOT_ERR_FILE_BAD_DRIVE
        GODOT_ERR_FILE_BAD_PATH
        GODOT_ERR_FILE_NO_PERMISSION
        GODOT_ERR_FILE_ALREADY_IN_USE
        GODOT_ERR_FILE_CANT_OPEN
        GODOT_ERR_FILE_CANT_WRITE
        GODOT_ERR_FILE_CANT_READ
        GODOT_ERR_FILE_UNRECOGNIZED
        GODOT_ERR_FILE_CORRUPT
        GODOT_ERR_FILE_MISSING_DEPENDENCIES
        GODOT_ERR_FILE_EOF
        GODOT_ERR_CANT_OPEN
        GODOT_ERR_CANT_CREATE
        GODOT_ERR_QUERY_FAILED
        GODOT_ERR_ALREADY_IN_USE
        GODOT_ERR_LOCKED
        GODOT_ERR_TIMEOUT
        GODOT_ERR_CANT_CONNECT
        GODOT_ERR_CANT_RESOLVE
        GODOT_ERR_CONNECTION_ERROR
        GODOT_ERR_CANT_ACQUIRE_RESOURCE
        GODOT_ERR_CANT_FORK
        GODOT_ERR_INVALID_DATA
        GODOT_ERR_INVALID_PARAMETER
        GODOT_ERR_ALREADY_EXISTS
        GODOT_ERR_DOES_NOT_EXIST
        GODOT_ERR_DATABASE_CANT_READ
        GODOT_ERR_DATABASE_CANT_WRITE
        GODOT_ERR_COMPILATION_FAILED
        GODOT_ERR_METHOD_NOT_FOUND
        GODOT_ERR_LINK_FAILED
        GODOT_ERR_SCRIPT_FAILED
        GODOT_ERR_CYCLIC_LINK
        GODOT_ERR_INVALID_DECLARATION
        GODOT_ERR_DUPLICATE_SYMBOL
        GODOT_ERR_PARSE_ERROR
        GODOT_ERR_BUSY
        GODOT_ERR_SKIP
        GODOT_ERR_HELP
        GODOT_ERR_BUG
        GODOT_ERR_PRINTER_ON_FIRE

    ctypedef bool godot_bool

    ctypedef int godot_int

    ctypedef float godot_real

    ctypedef void godot_object

    ctypedef wchar_t godot_char_type

    ctypedef struct godot_string:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_char_string:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_pool_array_read_access:
        uint8_t _dont_touch_that[1]

    ctypedef godot_pool_array_read_access godot_pool_byte_array_read_access

    ctypedef godot_pool_array_read_access godot_pool_int_array_read_access

    ctypedef godot_pool_array_read_access godot_pool_real_array_read_access

    ctypedef godot_pool_array_read_access godot_pool_string_array_read_access

    ctypedef godot_pool_array_read_access godot_pool_vector2_array_read_access

    ctypedef godot_pool_array_read_access godot_pool_vector3_array_read_access

    ctypedef godot_pool_array_read_access godot_pool_color_array_read_access

    ctypedef struct godot_pool_array_write_access:
        uint8_t _dont_touch_that[1]

    ctypedef godot_pool_array_write_access godot_pool_byte_array_write_access

    ctypedef godot_pool_array_write_access godot_pool_int_array_write_access

    ctypedef godot_pool_array_write_access godot_pool_real_array_write_access

    ctypedef godot_pool_array_write_access godot_pool_string_array_write_access

    ctypedef godot_pool_array_write_access godot_pool_vector2_array_write_access

    ctypedef godot_pool_array_write_access godot_pool_vector3_array_write_access

    ctypedef godot_pool_array_write_access godot_pool_color_array_write_access

    ctypedef struct godot_pool_byte_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_pool_int_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_pool_real_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_pool_string_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_pool_vector2_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_pool_vector3_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_pool_color_array:
        uint8_t _dont_touch_that[sizeof(void *)]

    ctypedef struct godot_color:
        uint8_t _dont_touch_that[16]

    void godot_color_new_rgba(godot_color* r_dest, godot_real p_r, godot_real p_g, godot_real p_b, godot_real p_a)

    void godot_color_new_rgb(godot_color* r_dest, godot_real p_r, godot_real p_g, godot_real p_b)

    godot_real godot_color_get_r(godot_color* p_self)

    void godot_color_set_r(godot_color* p_self, godot_real r)

    godot_real godot_color_get_g(godot_color* p_self)

    void godot_color_set_g(godot_color* p_self, godot_real g)

    godot_real godot_color_get_b(godot_color* p_self)

    void godot_color_set_b(godot_color* p_self, godot_real b)

    godot_real godot_color_get_a(godot_color* p_self)

    void godot_color_set_a(godot_color* p_self, godot_real a)

    godot_real godot_color_get_h(godot_color* p_self)

    godot_real godot_color_get_s(godot_color* p_self)

    godot_real godot_color_get_v(godot_color* p_self)

    godot_string godot_color_as_string(godot_color* p_self)

    godot_int godot_color_to_rgba32(godot_color* p_self)

    godot_int godot_color_to_abgr32(godot_color* p_self)

    godot_int godot_color_to_abgr64(godot_color* p_self)

    godot_int godot_color_to_argb64(godot_color* p_self)

    godot_int godot_color_to_rgba64(godot_color* p_self)

    godot_int godot_color_to_argb32(godot_color* p_self)

    godot_real godot_color_gray(godot_color* p_self)

    godot_color godot_color_inverted(godot_color* p_self)

    godot_color godot_color_contrasted(godot_color* p_self)

    godot_color godot_color_linear_interpolate(godot_color* p_self, godot_color* p_b, godot_real p_t)

    godot_color godot_color_blend(godot_color* p_self, godot_color* p_over)

    godot_color godot_color_darkened(godot_color* p_self, godot_real p_amount)

    godot_color godot_color_from_hsv(godot_color* p_self, godot_real p_h, godot_real p_s, godot_real p_v, godot_real p_a)

    godot_color godot_color_lightened(godot_color* p_self, godot_real p_amount)

    godot_string godot_color_to_html(godot_color* p_self, godot_bool p_with_alpha)

    godot_bool godot_color_operator_equal(godot_color* p_self, godot_color* p_b)

    godot_bool godot_color_operator_less(godot_color* p_self, godot_color* p_b)

    ctypedef struct godot_vector2:
        uint8_t _dont_touch_that[8]

    void godot_vector2_new(godot_vector2* r_dest, godot_real p_x, godot_real p_y)

    godot_string godot_vector2_as_string(godot_vector2* p_self)

    godot_vector2 godot_vector2_normalized(godot_vector2* p_self)

    godot_real godot_vector2_length(godot_vector2* p_self)

    godot_real godot_vector2_angle(godot_vector2* p_self)

    godot_real godot_vector2_length_squared(godot_vector2* p_self)

    godot_bool godot_vector2_is_normalized(godot_vector2* p_self)

    godot_real godot_vector2_distance_to(godot_vector2* p_self, godot_vector2* p_to)

    godot_real godot_vector2_distance_squared_to(godot_vector2* p_self, godot_vector2* p_to)

    godot_real godot_vector2_angle_to(godot_vector2* p_self, godot_vector2* p_to)

    godot_real godot_vector2_angle_to_point(godot_vector2* p_self, godot_vector2* p_to)

    godot_vector2 godot_vector2_linear_interpolate(godot_vector2* p_self, godot_vector2* p_b, godot_real p_t)

    godot_vector2 godot_vector2_cubic_interpolate(godot_vector2* p_self, godot_vector2* p_b, godot_vector2* p_pre_a, godot_vector2* p_post_b, godot_real p_t)

    godot_vector2 godot_vector2_rotated(godot_vector2* p_self, godot_real p_phi)

    godot_vector2 godot_vector2_tangent(godot_vector2* p_self)

    godot_vector2 godot_vector2_floor(godot_vector2* p_self)

    godot_vector2 godot_vector2_snapped(godot_vector2* p_self, godot_vector2* p_by)

    godot_real godot_vector2_aspect(godot_vector2* p_self)

    godot_real godot_vector2_dot(godot_vector2* p_self, godot_vector2* p_with)

    godot_vector2 godot_vector2_slide(godot_vector2* p_self, godot_vector2* p_n)

    godot_vector2 godot_vector2_bounce(godot_vector2* p_self, godot_vector2* p_n)

    godot_vector2 godot_vector2_reflect(godot_vector2* p_self, godot_vector2* p_n)

    godot_vector2 godot_vector2_abs(godot_vector2* p_self)

    godot_vector2 godot_vector2_clamped(godot_vector2* p_self, godot_real p_length)

    godot_vector2 godot_vector2_operator_add(godot_vector2* p_self, godot_vector2* p_b)

    godot_vector2 godot_vector2_operator_subtract(godot_vector2* p_self, godot_vector2* p_b)

    godot_vector2 godot_vector2_operator_multiply_vector(godot_vector2* p_self, godot_vector2* p_b)

    godot_vector2 godot_vector2_operator_multiply_scalar(godot_vector2* p_self, godot_real p_b)

    godot_vector2 godot_vector2_operator_divide_vector(godot_vector2* p_self, godot_vector2* p_b)

    godot_vector2 godot_vector2_operator_divide_scalar(godot_vector2* p_self, godot_real p_b)

    godot_bool godot_vector2_operator_equal(godot_vector2* p_self, godot_vector2* p_b)

    godot_bool godot_vector2_operator_less(godot_vector2* p_self, godot_vector2* p_b)

    godot_vector2 godot_vector2_operator_neg(godot_vector2* p_self)

    void godot_vector2_set_x(godot_vector2* p_self, godot_real p_x)

    void godot_vector2_set_y(godot_vector2* p_self, godot_real p_y)

    godot_real godot_vector2_get_x(godot_vector2* p_self)

    godot_real godot_vector2_get_y(godot_vector2* p_self)

    ctypedef struct godot_vector3:
        uint8_t _dont_touch_that[12]

    ctypedef struct godot_basis:
        uint8_t _dont_touch_that[36]

    ctypedef struct godot_quat:
        uint8_t _dont_touch_that[16]

    void godot_quat_new(godot_quat* r_dest, godot_real p_x, godot_real p_y, godot_real p_z, godot_real p_w)

    void godot_quat_new_with_axis_angle(godot_quat* r_dest, godot_vector3* p_axis, godot_real p_angle)

    void godot_quat_new_with_basis(godot_quat* r_dest, godot_basis* p_basis)

    void godot_quat_new_with_euler(godot_quat* r_dest, godot_vector3* p_euler)

    godot_real godot_quat_get_x(godot_quat* p_self)

    void godot_quat_set_x(godot_quat* p_self, godot_real val)

    godot_real godot_quat_get_y(godot_quat* p_self)

    void godot_quat_set_y(godot_quat* p_self, godot_real val)

    godot_real godot_quat_get_z(godot_quat* p_self)

    void godot_quat_set_z(godot_quat* p_self, godot_real val)

    godot_real godot_quat_get_w(godot_quat* p_self)

    void godot_quat_set_w(godot_quat* p_self, godot_real val)

    godot_string godot_quat_as_string(godot_quat* p_self)

    godot_real godot_quat_length(godot_quat* p_self)

    godot_real godot_quat_length_squared(godot_quat* p_self)

    godot_quat godot_quat_normalized(godot_quat* p_self)

    godot_bool godot_quat_is_normalized(godot_quat* p_self)

    godot_quat godot_quat_inverse(godot_quat* p_self)

    godot_real godot_quat_dot(godot_quat* p_self, godot_quat* p_b)

    godot_vector3 godot_quat_xform(godot_quat* p_self, godot_vector3* p_v)

    godot_quat godot_quat_slerp(godot_quat* p_self, godot_quat* p_b, godot_real p_t)

    godot_quat godot_quat_slerpni(godot_quat* p_self, godot_quat* p_b, godot_real p_t)

    godot_quat godot_quat_cubic_slerp(godot_quat* p_self, godot_quat* p_b, godot_quat* p_pre_a, godot_quat* p_post_b, godot_real p_t)

    godot_quat godot_quat_operator_multiply(godot_quat* p_self, godot_real p_b)

    godot_quat godot_quat_operator_add(godot_quat* p_self, godot_quat* p_b)

    godot_quat godot_quat_operator_subtract(godot_quat* p_self, godot_quat* p_b)

    godot_quat godot_quat_operator_divide(godot_quat* p_self, godot_real p_b)

    godot_bool godot_quat_operator_equal(godot_quat* p_self, godot_quat* p_b)

    godot_quat godot_quat_operator_neg(godot_quat* p_self)

    void godot_quat_set_axis_angle(godot_quat* p_self, godot_vector3* p_axis, godot_real p_angle)

    void godot_basis_new_with_rows(godot_basis* r_dest, godot_vector3* p_x_axis, godot_vector3* p_y_axis, godot_vector3* p_z_axis)

    void godot_basis_new_with_axis_and_angle(godot_basis* r_dest, godot_vector3* p_axis, godot_real p_phi)

    void godot_basis_new_with_euler(godot_basis* r_dest, godot_vector3* p_euler)

    void godot_basis_new_with_euler_quat(godot_basis* r_dest, godot_quat* p_euler)

    godot_string godot_basis_as_string(godot_basis* p_self)

    godot_basis godot_basis_inverse(godot_basis* p_self)

    godot_basis godot_basis_transposed(godot_basis* p_self)

    godot_basis godot_basis_orthonormalized(godot_basis* p_self)

    godot_real godot_basis_determinant(godot_basis* p_self)

    godot_basis godot_basis_rotated(godot_basis* p_self, godot_vector3* p_axis, godot_real p_phi)

    godot_basis godot_basis_scaled(godot_basis* p_self, godot_vector3* p_scale)

    godot_vector3 godot_basis_get_scale(godot_basis* p_self)

    godot_vector3 godot_basis_get_euler(godot_basis* p_self)

    godot_quat godot_basis_get_quat(godot_basis* p_self)

    void godot_basis_set_quat(godot_basis* p_self, godot_quat* p_quat)

    void godot_basis_set_axis_angle_scale(godot_basis* p_self, godot_vector3* p_axis, godot_real p_phi, godot_vector3* p_scale)

    void godot_basis_set_euler_scale(godot_basis* p_self, godot_vector3* p_euler, godot_vector3* p_scale)

    void godot_basis_set_quat_scale(godot_basis* p_self, godot_quat* p_quat, godot_vector3* p_scale)

    godot_real godot_basis_tdotx(godot_basis* p_self, godot_vector3* p_with)

    godot_real godot_basis_tdoty(godot_basis* p_self, godot_vector3* p_with)

    godot_real godot_basis_tdotz(godot_basis* p_self, godot_vector3* p_with)

    godot_vector3 godot_basis_xform(godot_basis* p_self, godot_vector3* p_v)

    godot_vector3 godot_basis_xform_inv(godot_basis* p_self, godot_vector3* p_v)

    godot_int godot_basis_get_orthogonal_index(godot_basis* p_self)

    void godot_basis_new(godot_basis* r_dest)

    void godot_basis_get_elements(godot_basis* p_self, godot_vector3* p_elements)

    godot_vector3 godot_basis_get_axis(godot_basis* p_self, godot_int p_axis)

    void godot_basis_set_axis(godot_basis* p_self, godot_int p_axis, godot_vector3* p_value)

    godot_vector3 godot_basis_get_row(godot_basis* p_self, godot_int p_row)

    void godot_basis_set_row(godot_basis* p_self, godot_int p_row, godot_vector3* p_value)

    godot_bool godot_basis_operator_equal(godot_basis* p_self, godot_basis* p_b)

    godot_basis godot_basis_operator_add(godot_basis* p_self, godot_basis* p_b)

    godot_basis godot_basis_operator_subtract(godot_basis* p_self, godot_basis* p_b)

    godot_basis godot_basis_operator_multiply_vector(godot_basis* p_self, godot_basis* p_b)

    godot_basis godot_basis_operator_multiply_scalar(godot_basis* p_self, godot_real p_b)

    godot_basis godot_basis_slerp(godot_basis* p_self, godot_basis* p_b, godot_real p_t)

    ctypedef enum godot_vector3_axis:
        GODOT_VECTOR3_AXIS_X
        GODOT_VECTOR3_AXIS_Y
        GODOT_VECTOR3_AXIS_Z

    void godot_vector3_new(godot_vector3* r_dest, godot_real p_x, godot_real p_y, godot_real p_z)

    godot_string godot_vector3_as_string(godot_vector3* p_self)

    godot_int godot_vector3_min_axis(godot_vector3* p_self)

    godot_int godot_vector3_max_axis(godot_vector3* p_self)

    godot_real godot_vector3_length(godot_vector3* p_self)

    godot_real godot_vector3_length_squared(godot_vector3* p_self)

    godot_bool godot_vector3_is_normalized(godot_vector3* p_self)

    godot_vector3 godot_vector3_normalized(godot_vector3* p_self)

    godot_vector3 godot_vector3_inverse(godot_vector3* p_self)

    godot_vector3 godot_vector3_snapped(godot_vector3* p_self, godot_vector3* p_by)

    godot_vector3 godot_vector3_rotated(godot_vector3* p_self, godot_vector3* p_axis, godot_real p_phi)

    godot_vector3 godot_vector3_linear_interpolate(godot_vector3* p_self, godot_vector3* p_b, godot_real p_t)

    godot_vector3 godot_vector3_cubic_interpolate(godot_vector3* p_self, godot_vector3* p_b, godot_vector3* p_pre_a, godot_vector3* p_post_b, godot_real p_t)

    godot_real godot_vector3_dot(godot_vector3* p_self, godot_vector3* p_b)

    godot_vector3 godot_vector3_cross(godot_vector3* p_self, godot_vector3* p_b)

    godot_basis godot_vector3_outer(godot_vector3* p_self, godot_vector3* p_b)

    godot_basis godot_vector3_to_diagonal_matrix(godot_vector3* p_self)

    godot_vector3 godot_vector3_abs(godot_vector3* p_self)

    godot_vector3 godot_vector3_floor(godot_vector3* p_self)

    godot_vector3 godot_vector3_ceil(godot_vector3* p_self)

    godot_real godot_vector3_distance_to(godot_vector3* p_self, godot_vector3* p_b)

    godot_real godot_vector3_distance_squared_to(godot_vector3* p_self, godot_vector3* p_b)

    godot_real godot_vector3_angle_to(godot_vector3* p_self, godot_vector3* p_to)

    godot_vector3 godot_vector3_slide(godot_vector3* p_self, godot_vector3* p_n)

    godot_vector3 godot_vector3_bounce(godot_vector3* p_self, godot_vector3* p_n)

    godot_vector3 godot_vector3_reflect(godot_vector3* p_self, godot_vector3* p_n)

    godot_vector3 godot_vector3_operator_add(godot_vector3* p_self, godot_vector3* p_b)

    godot_vector3 godot_vector3_operator_subtract(godot_vector3* p_self, godot_vector3* p_b)

    godot_vector3 godot_vector3_operator_multiply_vector(godot_vector3* p_self, godot_vector3* p_b)

    godot_vector3 godot_vector3_operator_multiply_scalar(godot_vector3* p_self, godot_real p_b)

    godot_vector3 godot_vector3_operator_divide_vector(godot_vector3* p_self, godot_vector3* p_b)

    godot_vector3 godot_vector3_operator_divide_scalar(godot_vector3* p_self, godot_real p_b)

    godot_bool godot_vector3_operator_equal(godot_vector3* p_self, godot_vector3* p_b)

    godot_bool godot_vector3_operator_less(godot_vector3* p_self, godot_vector3* p_b)

    godot_vector3 godot_vector3_operator_neg(godot_vector3* p_self)

    void godot_vector3_set_axis(godot_vector3* p_self, godot_vector3_axis p_axis, godot_real p_val)

    godot_real godot_vector3_get_axis(godot_vector3* p_self, godot_vector3_axis p_axis)

    void godot_pool_byte_array_new(godot_pool_byte_array* r_dest)

    void godot_pool_byte_array_new_copy(godot_pool_byte_array* r_dest, godot_pool_byte_array* p_src)

    void godot_pool_byte_array_new_with_array(godot_pool_byte_array* r_dest, godot_array* p_a)

    void godot_pool_byte_array_append(godot_pool_byte_array* p_self, uint8_t p_data)

    void godot_pool_byte_array_append_array(godot_pool_byte_array* p_self, godot_pool_byte_array* p_array)

    godot_error godot_pool_byte_array_insert(godot_pool_byte_array* p_self, godot_int p_idx, uint8_t p_data)

    void godot_pool_byte_array_invert(godot_pool_byte_array* p_self)

    void godot_pool_byte_array_push_back(godot_pool_byte_array* p_self, uint8_t p_data)

    void godot_pool_byte_array_remove(godot_pool_byte_array* p_self, godot_int p_idx)

    void godot_pool_byte_array_resize(godot_pool_byte_array* p_self, godot_int p_size)

    godot_pool_byte_array_read_access* godot_pool_byte_array_read(godot_pool_byte_array* p_self)

    godot_pool_byte_array_write_access* godot_pool_byte_array_write(godot_pool_byte_array* p_self)

    void godot_pool_byte_array_set(godot_pool_byte_array* p_self, godot_int p_idx, uint8_t p_data)

    uint8_t godot_pool_byte_array_get(godot_pool_byte_array* p_self, godot_int p_idx)

    godot_int godot_pool_byte_array_size(godot_pool_byte_array* p_self)

    void godot_pool_byte_array_destroy(godot_pool_byte_array* p_self)

    void godot_pool_int_array_new(godot_pool_int_array* r_dest)

    void godot_pool_int_array_new_copy(godot_pool_int_array* r_dest, godot_pool_int_array* p_src)

    void godot_pool_int_array_new_with_array(godot_pool_int_array* r_dest, godot_array* p_a)

    void godot_pool_int_array_append(godot_pool_int_array* p_self, godot_int p_data)

    void godot_pool_int_array_append_array(godot_pool_int_array* p_self, godot_pool_int_array* p_array)

    godot_error godot_pool_int_array_insert(godot_pool_int_array* p_self, godot_int p_idx, godot_int p_data)

    void godot_pool_int_array_invert(godot_pool_int_array* p_self)

    void godot_pool_int_array_push_back(godot_pool_int_array* p_self, godot_int p_data)

    void godot_pool_int_array_remove(godot_pool_int_array* p_self, godot_int p_idx)

    void godot_pool_int_array_resize(godot_pool_int_array* p_self, godot_int p_size)

    godot_pool_int_array_read_access* godot_pool_int_array_read(godot_pool_int_array* p_self)

    godot_pool_int_array_write_access* godot_pool_int_array_write(godot_pool_int_array* p_self)

    void godot_pool_int_array_set(godot_pool_int_array* p_self, godot_int p_idx, godot_int p_data)

    godot_int godot_pool_int_array_get(godot_pool_int_array* p_self, godot_int p_idx)

    godot_int godot_pool_int_array_size(godot_pool_int_array* p_self)

    void godot_pool_int_array_destroy(godot_pool_int_array* p_self)

    void godot_pool_real_array_new(godot_pool_real_array* r_dest)

    void godot_pool_real_array_new_copy(godot_pool_real_array* r_dest, godot_pool_real_array* p_src)

    void godot_pool_real_array_new_with_array(godot_pool_real_array* r_dest, godot_array* p_a)

    void godot_pool_real_array_append(godot_pool_real_array* p_self, godot_real p_data)

    void godot_pool_real_array_append_array(godot_pool_real_array* p_self, godot_pool_real_array* p_array)

    godot_error godot_pool_real_array_insert(godot_pool_real_array* p_self, godot_int p_idx, godot_real p_data)

    void godot_pool_real_array_invert(godot_pool_real_array* p_self)

    void godot_pool_real_array_push_back(godot_pool_real_array* p_self, godot_real p_data)

    void godot_pool_real_array_remove(godot_pool_real_array* p_self, godot_int p_idx)

    void godot_pool_real_array_resize(godot_pool_real_array* p_self, godot_int p_size)

    godot_pool_real_array_read_access* godot_pool_real_array_read(godot_pool_real_array* p_self)

    godot_pool_real_array_write_access* godot_pool_real_array_write(godot_pool_real_array* p_self)

    void godot_pool_real_array_set(godot_pool_real_array* p_self, godot_int p_idx, godot_real p_data)

    godot_real godot_pool_real_array_get(godot_pool_real_array* p_self, godot_int p_idx)

    godot_int godot_pool_real_array_size(godot_pool_real_array* p_self)

    void godot_pool_real_array_destroy(godot_pool_real_array* p_self)

    void godot_pool_string_array_new(godot_pool_string_array* r_dest)

    void godot_pool_string_array_new_copy(godot_pool_string_array* r_dest, godot_pool_string_array* p_src)

    void godot_pool_string_array_new_with_array(godot_pool_string_array* r_dest, godot_array* p_a)

    void godot_pool_string_array_append(godot_pool_string_array* p_self, godot_string* p_data)

    void godot_pool_string_array_append_array(godot_pool_string_array* p_self, godot_pool_string_array* p_array)

    godot_error godot_pool_string_array_insert(godot_pool_string_array* p_self, godot_int p_idx, godot_string* p_data)

    void godot_pool_string_array_invert(godot_pool_string_array* p_self)

    void godot_pool_string_array_push_back(godot_pool_string_array* p_self, godot_string* p_data)

    void godot_pool_string_array_remove(godot_pool_string_array* p_self, godot_int p_idx)

    void godot_pool_string_array_resize(godot_pool_string_array* p_self, godot_int p_size)

    godot_pool_string_array_read_access* godot_pool_string_array_read(godot_pool_string_array* p_self)

    godot_pool_string_array_write_access* godot_pool_string_array_write(godot_pool_string_array* p_self)

    void godot_pool_string_array_set(godot_pool_string_array* p_self, godot_int p_idx, godot_string* p_data)

    godot_string godot_pool_string_array_get(godot_pool_string_array* p_self, godot_int p_idx)

    godot_int godot_pool_string_array_size(godot_pool_string_array* p_self)

    void godot_pool_string_array_destroy(godot_pool_string_array* p_self)

    void godot_pool_vector2_array_new(godot_pool_vector2_array* r_dest)

    void godot_pool_vector2_array_new_copy(godot_pool_vector2_array* r_dest, godot_pool_vector2_array* p_src)

    void godot_pool_vector2_array_new_with_array(godot_pool_vector2_array* r_dest, godot_array* p_a)

    void godot_pool_vector2_array_append(godot_pool_vector2_array* p_self, godot_vector2* p_data)

    void godot_pool_vector2_array_append_array(godot_pool_vector2_array* p_self, godot_pool_vector2_array* p_array)

    godot_error godot_pool_vector2_array_insert(godot_pool_vector2_array* p_self, godot_int p_idx, godot_vector2* p_data)

    void godot_pool_vector2_array_invert(godot_pool_vector2_array* p_self)

    void godot_pool_vector2_array_push_back(godot_pool_vector2_array* p_self, godot_vector2* p_data)

    void godot_pool_vector2_array_remove(godot_pool_vector2_array* p_self, godot_int p_idx)

    void godot_pool_vector2_array_resize(godot_pool_vector2_array* p_self, godot_int p_size)

    godot_pool_vector2_array_read_access* godot_pool_vector2_array_read(godot_pool_vector2_array* p_self)

    godot_pool_vector2_array_write_access* godot_pool_vector2_array_write(godot_pool_vector2_array* p_self)

    void godot_pool_vector2_array_set(godot_pool_vector2_array* p_self, godot_int p_idx, godot_vector2* p_data)

    godot_vector2 godot_pool_vector2_array_get(godot_pool_vector2_array* p_self, godot_int p_idx)

    godot_int godot_pool_vector2_array_size(godot_pool_vector2_array* p_self)

    void godot_pool_vector2_array_destroy(godot_pool_vector2_array* p_self)

    void godot_pool_vector3_array_new(godot_pool_vector3_array* r_dest)

    void godot_pool_vector3_array_new_copy(godot_pool_vector3_array* r_dest, godot_pool_vector3_array* p_src)

    void godot_pool_vector3_array_new_with_array(godot_pool_vector3_array* r_dest, godot_array* p_a)

    void godot_pool_vector3_array_append(godot_pool_vector3_array* p_self, godot_vector3* p_data)

    void godot_pool_vector3_array_append_array(godot_pool_vector3_array* p_self, godot_pool_vector3_array* p_array)

    godot_error godot_pool_vector3_array_insert(godot_pool_vector3_array* p_self, godot_int p_idx, godot_vector3* p_data)

    void godot_pool_vector3_array_invert(godot_pool_vector3_array* p_self)

    void godot_pool_vector3_array_push_back(godot_pool_vector3_array* p_self, godot_vector3* p_data)

    void godot_pool_vector3_array_remove(godot_pool_vector3_array* p_self, godot_int p_idx)

    void godot_pool_vector3_array_resize(godot_pool_vector3_array* p_self, godot_int p_size)

    godot_pool_vector3_array_read_access* godot_pool_vector3_array_read(godot_pool_vector3_array* p_self)

    godot_pool_vector3_array_write_access* godot_pool_vector3_array_write(godot_pool_vector3_array* p_self)

    void godot_pool_vector3_array_set(godot_pool_vector3_array* p_self, godot_int p_idx, godot_vector3* p_data)

    godot_vector3 godot_pool_vector3_array_get(godot_pool_vector3_array* p_self, godot_int p_idx)

    godot_int godot_pool_vector3_array_size(godot_pool_vector3_array* p_self)

    void godot_pool_vector3_array_destroy(godot_pool_vector3_array* p_self)

    void godot_pool_color_array_new(godot_pool_color_array* r_dest)

    void godot_pool_color_array_new_copy(godot_pool_color_array* r_dest, godot_pool_color_array* p_src)

    void godot_pool_color_array_new_with_array(godot_pool_color_array* r_dest, godot_array* p_a)

    void godot_pool_color_array_append(godot_pool_color_array* p_self, godot_color* p_data)

    void godot_pool_color_array_append_array(godot_pool_color_array* p_self, godot_pool_color_array* p_array)

    godot_error godot_pool_color_array_insert(godot_pool_color_array* p_self, godot_int p_idx, godot_color* p_data)

    void godot_pool_color_array_invert(godot_pool_color_array* p_self)

    void godot_pool_color_array_push_back(godot_pool_color_array* p_self, godot_color* p_data)

    void godot_pool_color_array_remove(godot_pool_color_array* p_self, godot_int p_idx)

    void godot_pool_color_array_resize(godot_pool_color_array* p_self, godot_int p_size)

    godot_pool_color_array_read_access* godot_pool_color_array_read(godot_pool_color_array* p_self)

    godot_pool_color_array_write_access* godot_pool_color_array_write(godot_pool_color_array* p_self)

    void godot_pool_color_array_set(godot_pool_color_array* p_self, godot_int p_idx, godot_color* p_data)

    godot_color godot_pool_color_array_get(godot_pool_color_array* p_self, godot_int p_idx)

    godot_int godot_pool_color_array_size(godot_pool_color_array* p_self)

    void godot_pool_color_array_destroy(godot_pool_color_array* p_self)

    godot_pool_byte_array_read_access* godot_pool_byte_array_read_access_copy(godot_pool_byte_array_read_access* p_other)

    uint8_t* godot_pool_byte_array_read_access_ptr(godot_pool_byte_array_read_access* p_read)

    void godot_pool_byte_array_read_access_operator_assign(godot_pool_byte_array_read_access* p_read, godot_pool_byte_array_read_access* p_other)

    void godot_pool_byte_array_read_access_destroy(godot_pool_byte_array_read_access* p_read)

    godot_pool_int_array_read_access* godot_pool_int_array_read_access_copy(godot_pool_int_array_read_access* p_other)

    godot_int* godot_pool_int_array_read_access_ptr(godot_pool_int_array_read_access* p_read)

    void godot_pool_int_array_read_access_operator_assign(godot_pool_int_array_read_access* p_read, godot_pool_int_array_read_access* p_other)

    void godot_pool_int_array_read_access_destroy(godot_pool_int_array_read_access* p_read)

    godot_pool_real_array_read_access* godot_pool_real_array_read_access_copy(godot_pool_real_array_read_access* p_other)

    godot_real* godot_pool_real_array_read_access_ptr(godot_pool_real_array_read_access* p_read)

    void godot_pool_real_array_read_access_operator_assign(godot_pool_real_array_read_access* p_read, godot_pool_real_array_read_access* p_other)

    void godot_pool_real_array_read_access_destroy(godot_pool_real_array_read_access* p_read)

    godot_pool_string_array_read_access* godot_pool_string_array_read_access_copy(godot_pool_string_array_read_access* p_other)

    godot_string* godot_pool_string_array_read_access_ptr(godot_pool_string_array_read_access* p_read)

    void godot_pool_string_array_read_access_operator_assign(godot_pool_string_array_read_access* p_read, godot_pool_string_array_read_access* p_other)

    void godot_pool_string_array_read_access_destroy(godot_pool_string_array_read_access* p_read)

    godot_pool_vector2_array_read_access* godot_pool_vector2_array_read_access_copy(godot_pool_vector2_array_read_access* p_other)

    godot_vector2* godot_pool_vector2_array_read_access_ptr(godot_pool_vector2_array_read_access* p_read)

    void godot_pool_vector2_array_read_access_operator_assign(godot_pool_vector2_array_read_access* p_read, godot_pool_vector2_array_read_access* p_other)

    void godot_pool_vector2_array_read_access_destroy(godot_pool_vector2_array_read_access* p_read)

    godot_pool_vector3_array_read_access* godot_pool_vector3_array_read_access_copy(godot_pool_vector3_array_read_access* p_other)

    godot_vector3* godot_pool_vector3_array_read_access_ptr(godot_pool_vector3_array_read_access* p_read)

    void godot_pool_vector3_array_read_access_operator_assign(godot_pool_vector3_array_read_access* p_read, godot_pool_vector3_array_read_access* p_other)

    void godot_pool_vector3_array_read_access_destroy(godot_pool_vector3_array_read_access* p_read)

    godot_pool_color_array_read_access* godot_pool_color_array_read_access_copy(godot_pool_color_array_read_access* p_other)

    godot_color* godot_pool_color_array_read_access_ptr(godot_pool_color_array_read_access* p_read)

    void godot_pool_color_array_read_access_operator_assign(godot_pool_color_array_read_access* p_read, godot_pool_color_array_read_access* p_other)

    void godot_pool_color_array_read_access_destroy(godot_pool_color_array_read_access* p_read)

    godot_pool_byte_array_write_access* godot_pool_byte_array_write_access_copy(godot_pool_byte_array_write_access* p_other)

    uint8_t* godot_pool_byte_array_write_access_ptr(godot_pool_byte_array_write_access* p_write)

    void godot_pool_byte_array_write_access_operator_assign(godot_pool_byte_array_write_access* p_write, godot_pool_byte_array_write_access* p_other)

    void godot_pool_byte_array_write_access_destroy(godot_pool_byte_array_write_access* p_write)

    godot_pool_int_array_write_access* godot_pool_int_array_write_access_copy(godot_pool_int_array_write_access* p_other)

    godot_int* godot_pool_int_array_write_access_ptr(godot_pool_int_array_write_access* p_write)

    void godot_pool_int_array_write_access_operator_assign(godot_pool_int_array_write_access* p_write, godot_pool_int_array_write_access* p_other)

    void godot_pool_int_array_write_access_destroy(godot_pool_int_array_write_access* p_write)

    godot_pool_real_array_write_access* godot_pool_real_array_write_access_copy(godot_pool_real_array_write_access* p_other)

    godot_real* godot_pool_real_array_write_access_ptr(godot_pool_real_array_write_access* p_write)

    void godot_pool_real_array_write_access_operator_assign(godot_pool_real_array_write_access* p_write, godot_pool_real_array_write_access* p_other)

    void godot_pool_real_array_write_access_destroy(godot_pool_real_array_write_access* p_write)

    godot_pool_string_array_write_access* godot_pool_string_array_write_access_copy(godot_pool_string_array_write_access* p_other)

    godot_string* godot_pool_string_array_write_access_ptr(godot_pool_string_array_write_access* p_write)

    void godot_pool_string_array_write_access_operator_assign(godot_pool_string_array_write_access* p_write, godot_pool_string_array_write_access* p_other)

    void godot_pool_string_array_write_access_destroy(godot_pool_string_array_write_access* p_write)

    godot_pool_vector2_array_write_access* godot_pool_vector2_array_write_access_copy(godot_pool_vector2_array_write_access* p_other)

    godot_vector2* godot_pool_vector2_array_write_access_ptr(godot_pool_vector2_array_write_access* p_write)

    void godot_pool_vector2_array_write_access_operator_assign(godot_pool_vector2_array_write_access* p_write, godot_pool_vector2_array_write_access* p_other)

    void godot_pool_vector2_array_write_access_destroy(godot_pool_vector2_array_write_access* p_write)

    godot_pool_vector3_array_write_access* godot_pool_vector3_array_write_access_copy(godot_pool_vector3_array_write_access* p_other)

    godot_vector3* godot_pool_vector3_array_write_access_ptr(godot_pool_vector3_array_write_access* p_write)

    void godot_pool_vector3_array_write_access_operator_assign(godot_pool_vector3_array_write_access* p_write, godot_pool_vector3_array_write_access* p_other)

    void godot_pool_vector3_array_write_access_destroy(godot_pool_vector3_array_write_access* p_write)

    godot_pool_color_array_write_access* godot_pool_color_array_write_access_copy(godot_pool_color_array_write_access* p_other)

    godot_color* godot_pool_color_array_write_access_ptr(godot_pool_color_array_write_access* p_write)

    void godot_pool_color_array_write_access_operator_assign(godot_pool_color_array_write_access* p_write, godot_pool_color_array_write_access* p_other)

    void godot_pool_color_array_write_access_destroy(godot_pool_color_array_write_access* p_write)

    ctypedef struct godot_variant:
        uint8_t _dont_touch_that[16 + sizeof(void *)]

    cdef enum godot_variant_type:
        GODOT_VARIANT_TYPE_NIL
        GODOT_VARIANT_TYPE_BOOL
        GODOT_VARIANT_TYPE_INT
        GODOT_VARIANT_TYPE_REAL
        GODOT_VARIANT_TYPE_STRING
        GODOT_VARIANT_TYPE_VECTOR2
        GODOT_VARIANT_TYPE_RECT2
        GODOT_VARIANT_TYPE_VECTOR3
        GODOT_VARIANT_TYPE_TRANSFORM2D
        GODOT_VARIANT_TYPE_PLANE
        GODOT_VARIANT_TYPE_QUAT
        GODOT_VARIANT_TYPE_AABB
        GODOT_VARIANT_TYPE_BASIS
        GODOT_VARIANT_TYPE_TRANSFORM
        GODOT_VARIANT_TYPE_COLOR
        GODOT_VARIANT_TYPE_NODE_PATH
        GODOT_VARIANT_TYPE_RID
        GODOT_VARIANT_TYPE_OBJECT
        GODOT_VARIANT_TYPE_DICTIONARY
        GODOT_VARIANT_TYPE_ARRAY
        GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY
        GODOT_VARIANT_TYPE_POOL_INT_ARRAY
        GODOT_VARIANT_TYPE_POOL_REAL_ARRAY
        GODOT_VARIANT_TYPE_POOL_STRING_ARRAY
        GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY
        GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY
        GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY

    cdef enum godot_variant_call_error_error:
        GODOT_CALL_ERROR_CALL_OK
        GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD
        GODOT_CALL_ERROR_CALL_ERROR_INVALID_ARGUMENT
        GODOT_CALL_ERROR_CALL_ERROR_TOO_MANY_ARGUMENTS
        GODOT_CALL_ERROR_CALL_ERROR_TOO_FEW_ARGUMENTS
        GODOT_CALL_ERROR_CALL_ERROR_INSTANCE_IS_NULL

    cdef struct godot_variant_call_error:
        godot_variant_call_error_error error
        int argument
        godot_variant_type expected

    cdef enum godot_variant_operator:
        GODOT_VARIANT_OP_EQUAL
        GODOT_VARIANT_OP_NOT_EQUAL
        GODOT_VARIANT_OP_LESS
        GODOT_VARIANT_OP_LESS_EQUAL
        GODOT_VARIANT_OP_GREATER
        GODOT_VARIANT_OP_GREATER_EQUAL
        GODOT_VARIANT_OP_ADD
        GODOT_VARIANT_OP_SUBTRACT
        GODOT_VARIANT_OP_MULTIPLY
        GODOT_VARIANT_OP_DIVIDE
        GODOT_VARIANT_OP_NEGATE
        GODOT_VARIANT_OP_POSITIVE
        GODOT_VARIANT_OP_MODULE
        GODOT_VARIANT_OP_STRING_CONCAT
        GODOT_VARIANT_OP_SHIFT_LEFT
        GODOT_VARIANT_OP_SHIFT_RIGHT
        GODOT_VARIANT_OP_BIT_AND
        GODOT_VARIANT_OP_BIT_OR
        GODOT_VARIANT_OP_BIT_XOR
        GODOT_VARIANT_OP_BIT_NEGATE
        GODOT_VARIANT_OP_AND
        GODOT_VARIANT_OP_OR
        GODOT_VARIANT_OP_XOR
        GODOT_VARIANT_OP_NOT
        GODOT_VARIANT_OP_IN
        GODOT_VARIANT_OP_MAX

    ctypedef struct godot_aabb:
        uint8_t _dont_touch_that[24]

    ctypedef struct godot_plane:
        uint8_t _dont_touch_that[16]

    void godot_plane_new_with_reals(godot_plane* r_dest, godot_real p_a, godot_real p_b, godot_real p_c, godot_real p_d)

    void godot_plane_new_with_vectors(godot_plane* r_dest, godot_vector3* p_v1, godot_vector3* p_v2, godot_vector3* p_v3)

    void godot_plane_new_with_normal(godot_plane* r_dest, godot_vector3* p_normal, godot_real p_d)

    godot_string godot_plane_as_string(godot_plane* p_self)

    godot_plane godot_plane_normalized(godot_plane* p_self)

    godot_vector3 godot_plane_center(godot_plane* p_self)

    godot_vector3 godot_plane_get_any_point(godot_plane* p_self)

    godot_bool godot_plane_is_point_over(godot_plane* p_self, godot_vector3* p_point)

    godot_real godot_plane_distance_to(godot_plane* p_self, godot_vector3* p_point)

    godot_bool godot_plane_has_point(godot_plane* p_self, godot_vector3* p_point, godot_real p_epsilon)

    godot_vector3 godot_plane_project(godot_plane* p_self, godot_vector3* p_point)

    godot_bool godot_plane_intersect_3(godot_plane* p_self, godot_vector3* r_dest, godot_plane* p_b, godot_plane* p_c)

    godot_bool godot_plane_intersects_ray(godot_plane* p_self, godot_vector3* r_dest, godot_vector3* p_from, godot_vector3* p_dir)

    godot_bool godot_plane_intersects_segment(godot_plane* p_self, godot_vector3* r_dest, godot_vector3* p_begin, godot_vector3* p_end)

    godot_plane godot_plane_operator_neg(godot_plane* p_self)

    godot_bool godot_plane_operator_equal(godot_plane* p_self, godot_plane* p_b)

    void godot_plane_set_normal(godot_plane* p_self, godot_vector3* p_normal)

    godot_vector3 godot_plane_get_normal(godot_plane* p_self)

    godot_real godot_plane_get_d(godot_plane* p_self)

    void godot_plane_set_d(godot_plane* p_self, godot_real p_d)

    void godot_aabb_new(godot_aabb* r_dest, godot_vector3* p_pos, godot_vector3* p_size)

    godot_vector3 godot_aabb_get_position(godot_aabb* p_self)

    void godot_aabb_set_position(godot_aabb* p_self, godot_vector3* p_v)

    godot_vector3 godot_aabb_get_size(godot_aabb* p_self)

    void godot_aabb_set_size(godot_aabb* p_self, godot_vector3* p_v)

    godot_string godot_aabb_as_string(godot_aabb* p_self)

    godot_real godot_aabb_get_area(godot_aabb* p_self)

    godot_bool godot_aabb_has_no_area(godot_aabb* p_self)

    godot_bool godot_aabb_has_no_surface(godot_aabb* p_self)

    godot_bool godot_aabb_intersects(godot_aabb* p_self, godot_aabb* p_with)

    godot_bool godot_aabb_encloses(godot_aabb* p_self, godot_aabb* p_with)

    godot_aabb godot_aabb_merge(godot_aabb* p_self, godot_aabb* p_with)

    godot_aabb godot_aabb_intersection(godot_aabb* p_self, godot_aabb* p_with)

    godot_bool godot_aabb_intersects_plane(godot_aabb* p_self, godot_plane* p_plane)

    godot_bool godot_aabb_intersects_segment(godot_aabb* p_self, godot_vector3* p_from, godot_vector3* p_to)

    godot_bool godot_aabb_has_point(godot_aabb* p_self, godot_vector3* p_point)

    godot_vector3 godot_aabb_get_support(godot_aabb* p_self, godot_vector3* p_dir)

    godot_vector3 godot_aabb_get_longest_axis(godot_aabb* p_self)

    godot_int godot_aabb_get_longest_axis_index(godot_aabb* p_self)

    godot_real godot_aabb_get_longest_axis_size(godot_aabb* p_self)

    godot_vector3 godot_aabb_get_shortest_axis(godot_aabb* p_self)

    godot_int godot_aabb_get_shortest_axis_index(godot_aabb* p_self)

    godot_real godot_aabb_get_shortest_axis_size(godot_aabb* p_self)

    godot_aabb godot_aabb_expand(godot_aabb* p_self, godot_vector3* p_to_point)

    godot_aabb godot_aabb_grow(godot_aabb* p_self, godot_real p_by)

    godot_vector3 godot_aabb_get_endpoint(godot_aabb* p_self, godot_int p_idx)

    godot_bool godot_aabb_operator_equal(godot_aabb* p_self, godot_aabb* p_b)

    ctypedef struct godot_dictionary:
        uint8_t _dont_touch_that[sizeof(void *)]

    void godot_dictionary_new(godot_dictionary* r_dest)

    void godot_dictionary_new_copy(godot_dictionary* r_dest, godot_dictionary* p_src)

    void godot_dictionary_destroy(godot_dictionary* p_self)

    godot_int godot_dictionary_size(godot_dictionary* p_self)

    godot_bool godot_dictionary_empty(godot_dictionary* p_self)

    void godot_dictionary_clear(godot_dictionary* p_self)

    godot_bool godot_dictionary_has(godot_dictionary* p_self, godot_variant* p_key)

    godot_bool godot_dictionary_has_all(godot_dictionary* p_self, godot_array* p_keys)

    void godot_dictionary_erase(godot_dictionary* p_self, godot_variant* p_key)

    godot_int godot_dictionary_hash(godot_dictionary* p_self)

    godot_array godot_dictionary_keys(godot_dictionary* p_self)

    godot_array godot_dictionary_values(godot_dictionary* p_self)

    godot_variant godot_dictionary_get(godot_dictionary* p_self, godot_variant* p_key)

    void godot_dictionary_set(godot_dictionary* p_self, godot_variant* p_key, godot_variant* p_value)

    godot_variant* godot_dictionary_operator_index(godot_dictionary* p_self, godot_variant* p_key)

    godot_variant* godot_dictionary_operator_index_const(godot_dictionary* p_self, godot_variant* p_key)

    godot_variant* godot_dictionary_next(godot_dictionary* p_self, godot_variant* p_key)

    godot_bool godot_dictionary_operator_equal(godot_dictionary* p_self, godot_dictionary* p_b)

    godot_string godot_dictionary_to_json(godot_dictionary* p_self)

    godot_bool godot_dictionary_erase_with_return(godot_dictionary* p_self, godot_variant* p_key)

    ctypedef struct godot_node_path:
        uint8_t _dont_touch_that[sizeof(void *)]

    void godot_node_path_new(godot_node_path* r_dest, godot_string* p_from)

    void godot_node_path_new_copy(godot_node_path* r_dest, godot_node_path* p_src)

    void godot_node_path_destroy(godot_node_path* p_self)

    godot_string godot_node_path_as_string(godot_node_path* p_self)

    godot_bool godot_node_path_is_absolute(godot_node_path* p_self)

    godot_int godot_node_path_get_name_count(godot_node_path* p_self)

    godot_string godot_node_path_get_name(godot_node_path* p_self, godot_int p_idx)

    godot_int godot_node_path_get_subname_count(godot_node_path* p_self)

    godot_string godot_node_path_get_subname(godot_node_path* p_self, godot_int p_idx)

    godot_string godot_node_path_get_concatenated_subnames(godot_node_path* p_self)

    godot_bool godot_node_path_is_empty(godot_node_path* p_self)

    godot_bool godot_node_path_operator_equal(godot_node_path* p_self, godot_node_path* p_b)

    godot_node_path godot_node_path_get_as_property_path(godot_node_path* p_self)

    cdef struct godot_rect2:
        uint8_t _dont_touch_that[16]

    void godot_rect2_new_with_position_and_size(godot_rect2* r_dest, godot_vector2* p_pos, godot_vector2* p_size)

    void godot_rect2_new(godot_rect2* r_dest, godot_real p_x, godot_real p_y, godot_real p_width, godot_real p_height)

    godot_string godot_rect2_as_string(godot_rect2* p_self)

    godot_real godot_rect2_get_area(godot_rect2* p_self)

    godot_bool godot_rect2_intersects(godot_rect2* p_self, godot_rect2* p_b)

    godot_bool godot_rect2_encloses(godot_rect2* p_self, godot_rect2* p_b)

    godot_bool godot_rect2_has_no_area(godot_rect2* p_self)

    godot_rect2 godot_rect2_clip(godot_rect2* p_self, godot_rect2* p_b)

    godot_rect2 godot_rect2_merge(godot_rect2* p_self, godot_rect2* p_b)

    godot_bool godot_rect2_has_point(godot_rect2* p_self, godot_vector2* p_point)

    godot_rect2 godot_rect2_grow(godot_rect2* p_self, godot_real p_by)

    godot_rect2 godot_rect2_grow_individual(godot_rect2* p_self, godot_real p_left, godot_real p_top, godot_real p_right, godot_real p_bottom)

    godot_rect2 godot_rect2_grow_margin(godot_rect2* p_self, godot_int p_margin, godot_real p_by)

    godot_rect2 godot_rect2_abs(godot_rect2* p_self)

    godot_rect2 godot_rect2_expand(godot_rect2* p_self, godot_vector2* p_to)

    godot_bool godot_rect2_operator_equal(godot_rect2* p_self, godot_rect2* p_b)

    godot_vector2 godot_rect2_get_position(godot_rect2* p_self)

    godot_vector2 godot_rect2_get_size(godot_rect2* p_self)

    void godot_rect2_set_position(godot_rect2* p_self, godot_vector2* p_pos)

    void godot_rect2_set_size(godot_rect2* p_self, godot_vector2* p_size)

    ctypedef struct godot_rid:
        uint8_t _dont_touch_that[sizeof(void *)]

    void godot_rid_new(godot_rid* r_dest)

    godot_int godot_rid_get_id(godot_rid* p_self)

    void godot_rid_new_with_resource(godot_rid* r_dest, godot_object* p_from)

    godot_bool godot_rid_operator_equal(godot_rid* p_self, godot_rid* p_b)

    godot_bool godot_rid_operator_less(godot_rid* p_self, godot_rid* p_b)

    ctypedef struct godot_transform:
        uint8_t _dont_touch_that[48]

    void godot_transform_new_with_axis_origin(godot_transform* r_dest, godot_vector3* p_x_axis, godot_vector3* p_y_axis, godot_vector3* p_z_axis, godot_vector3* p_origin)

    void godot_transform_new(godot_transform* r_dest, godot_basis* p_basis, godot_vector3* p_origin)

    void godot_transform_new_with_quat(godot_transform* r_dest, godot_quat* p_quat)

    godot_basis godot_transform_get_basis(godot_transform* p_self)

    void godot_transform_set_basis(godot_transform* p_self, godot_basis* p_v)

    godot_vector3 godot_transform_get_origin(godot_transform* p_self)

    void godot_transform_set_origin(godot_transform* p_self, godot_vector3* p_v)

    godot_string godot_transform_as_string(godot_transform* p_self)

    godot_transform godot_transform_inverse(godot_transform* p_self)

    godot_transform godot_transform_affine_inverse(godot_transform* p_self)

    godot_transform godot_transform_orthonormalized(godot_transform* p_self)

    godot_transform godot_transform_rotated(godot_transform* p_self, godot_vector3* p_axis, godot_real p_phi)

    godot_transform godot_transform_scaled(godot_transform* p_self, godot_vector3* p_scale)

    godot_transform godot_transform_translated(godot_transform* p_self, godot_vector3* p_ofs)

    godot_transform godot_transform_looking_at(godot_transform* p_self, godot_vector3* p_target, godot_vector3* p_up)

    godot_plane godot_transform_xform_plane(godot_transform* p_self, godot_plane* p_v)

    godot_plane godot_transform_xform_inv_plane(godot_transform* p_self, godot_plane* p_v)

    void godot_transform_new_identity(godot_transform* r_dest)

    godot_bool godot_transform_operator_equal(godot_transform* p_self, godot_transform* p_b)

    godot_transform godot_transform_operator_multiply(godot_transform* p_self, godot_transform* p_b)

    godot_vector3 godot_transform_xform_vector3(godot_transform* p_self, godot_vector3* p_v)

    godot_vector3 godot_transform_xform_inv_vector3(godot_transform* p_self, godot_vector3* p_v)

    godot_aabb godot_transform_xform_aabb(godot_transform* p_self, godot_aabb* p_v)

    godot_aabb godot_transform_xform_inv_aabb(godot_transform* p_self, godot_aabb* p_v)

    ctypedef struct godot_transform2d:
        uint8_t _dont_touch_that[24]

    void godot_transform2d_new(godot_transform2d* r_dest, godot_real p_rot, godot_vector2* p_pos)

    void godot_transform2d_new_axis_origin(godot_transform2d* r_dest, godot_vector2* p_x_axis, godot_vector2* p_y_axis, godot_vector2* p_origin)

    godot_string godot_transform2d_as_string(godot_transform2d* p_self)

    godot_transform2d godot_transform2d_inverse(godot_transform2d* p_self)

    godot_transform2d godot_transform2d_affine_inverse(godot_transform2d* p_self)

    godot_real godot_transform2d_get_rotation(godot_transform2d* p_self)

    godot_vector2 godot_transform2d_get_origin(godot_transform2d* p_self)

    godot_vector2 godot_transform2d_get_scale(godot_transform2d* p_self)

    godot_transform2d godot_transform2d_orthonormalized(godot_transform2d* p_self)

    godot_transform2d godot_transform2d_rotated(godot_transform2d* p_self, godot_real p_phi)

    godot_transform2d godot_transform2d_scaled(godot_transform2d* p_self, godot_vector2* p_scale)

    godot_transform2d godot_transform2d_translated(godot_transform2d* p_self, godot_vector2* p_offset)

    godot_vector2 godot_transform2d_xform_vector2(godot_transform2d* p_self, godot_vector2* p_v)

    godot_vector2 godot_transform2d_xform_inv_vector2(godot_transform2d* p_self, godot_vector2* p_v)

    godot_vector2 godot_transform2d_basis_xform_vector2(godot_transform2d* p_self, godot_vector2* p_v)

    godot_vector2 godot_transform2d_basis_xform_inv_vector2(godot_transform2d* p_self, godot_vector2* p_v)

    godot_transform2d godot_transform2d_interpolate_with(godot_transform2d* p_self, godot_transform2d* p_m, godot_real p_c)

    godot_bool godot_transform2d_operator_equal(godot_transform2d* p_self, godot_transform2d* p_b)

    godot_transform2d godot_transform2d_operator_multiply(godot_transform2d* p_self, godot_transform2d* p_b)

    void godot_transform2d_new_identity(godot_transform2d* r_dest)

    godot_rect2 godot_transform2d_xform_rect2(godot_transform2d* p_self, godot_rect2* p_v)

    godot_rect2 godot_transform2d_xform_inv_rect2(godot_transform2d* p_self, godot_rect2* p_v)

    godot_variant_type godot_variant_get_type(godot_variant* p_v)

    void godot_variant_new_copy(godot_variant* r_dest, godot_variant* p_src)

    void godot_variant_new_nil(godot_variant* r_dest)

    void godot_variant_new_bool(godot_variant* r_dest, godot_bool p_b)

    void godot_variant_new_uint(godot_variant* r_dest, uint64_t p_i)

    void godot_variant_new_int(godot_variant* r_dest, int64_t p_i)

    void godot_variant_new_real(godot_variant* r_dest, double p_r)

    void godot_variant_new_string(godot_variant* r_dest, godot_string* p_s)

    void godot_variant_new_vector2(godot_variant* r_dest, godot_vector2* p_v2)

    void godot_variant_new_rect2(godot_variant* r_dest, godot_rect2* p_rect2)

    void godot_variant_new_vector3(godot_variant* r_dest, godot_vector3* p_v3)

    void godot_variant_new_transform2d(godot_variant* r_dest, godot_transform2d* p_t2d)

    void godot_variant_new_plane(godot_variant* r_dest, godot_plane* p_plane)

    void godot_variant_new_quat(godot_variant* r_dest, godot_quat* p_quat)

    void godot_variant_new_aabb(godot_variant* r_dest, godot_aabb* p_aabb)

    void godot_variant_new_basis(godot_variant* r_dest, godot_basis* p_basis)

    void godot_variant_new_transform(godot_variant* r_dest, godot_transform* p_trans)

    void godot_variant_new_color(godot_variant* r_dest, godot_color* p_color)

    void godot_variant_new_node_path(godot_variant* r_dest, godot_node_path* p_np)

    void godot_variant_new_rid(godot_variant* r_dest, godot_rid* p_rid)

    void godot_variant_new_object(godot_variant* r_dest, godot_object* p_obj)

    void godot_variant_new_dictionary(godot_variant* r_dest, godot_dictionary* p_dict)

    void godot_variant_new_array(godot_variant* r_dest, godot_array* p_arr)

    void godot_variant_new_pool_byte_array(godot_variant* r_dest, godot_pool_byte_array* p_pba)

    void godot_variant_new_pool_int_array(godot_variant* r_dest, godot_pool_int_array* p_pia)

    void godot_variant_new_pool_real_array(godot_variant* r_dest, godot_pool_real_array* p_pra)

    void godot_variant_new_pool_string_array(godot_variant* r_dest, godot_pool_string_array* p_psa)

    void godot_variant_new_pool_vector2_array(godot_variant* r_dest, godot_pool_vector2_array* p_pv2a)

    void godot_variant_new_pool_vector3_array(godot_variant* r_dest, godot_pool_vector3_array* p_pv3a)

    void godot_variant_new_pool_color_array(godot_variant* r_dest, godot_pool_color_array* p_pca)

    godot_bool godot_variant_as_bool(godot_variant* p_self)

    uint64_t godot_variant_as_uint(godot_variant* p_self)

    int64_t godot_variant_as_int(godot_variant* p_self)

    double godot_variant_as_real(godot_variant* p_self)

    godot_string godot_variant_as_string(godot_variant* p_self)

    godot_vector2 godot_variant_as_vector2(godot_variant* p_self)

    godot_rect2 godot_variant_as_rect2(godot_variant* p_self)

    godot_vector3 godot_variant_as_vector3(godot_variant* p_self)

    godot_transform2d godot_variant_as_transform2d(godot_variant* p_self)

    godot_plane godot_variant_as_plane(godot_variant* p_self)

    godot_quat godot_variant_as_quat(godot_variant* p_self)

    godot_aabb godot_variant_as_aabb(godot_variant* p_self)

    godot_basis godot_variant_as_basis(godot_variant* p_self)

    godot_transform godot_variant_as_transform(godot_variant* p_self)

    godot_color godot_variant_as_color(godot_variant* p_self)

    godot_node_path godot_variant_as_node_path(godot_variant* p_self)

    godot_rid godot_variant_as_rid(godot_variant* p_self)

    godot_object* godot_variant_as_object(godot_variant* p_self)

    godot_dictionary godot_variant_as_dictionary(godot_variant* p_self)

    godot_array godot_variant_as_array(godot_variant* p_self)

    godot_pool_byte_array godot_variant_as_pool_byte_array(godot_variant* p_self)

    godot_pool_int_array godot_variant_as_pool_int_array(godot_variant* p_self)

    godot_pool_real_array godot_variant_as_pool_real_array(godot_variant* p_self)

    godot_pool_string_array godot_variant_as_pool_string_array(godot_variant* p_self)

    godot_pool_vector2_array godot_variant_as_pool_vector2_array(godot_variant* p_self)

    godot_pool_vector3_array godot_variant_as_pool_vector3_array(godot_variant* p_self)

    godot_pool_color_array godot_variant_as_pool_color_array(godot_variant* p_self)

    godot_variant godot_variant_call(godot_variant* p_self, godot_string* p_method, godot_variant** p_args, godot_int p_argcount, godot_variant_call_error* r_error)

    godot_bool godot_variant_has_method(godot_variant* p_self, godot_string* p_method)

    godot_bool godot_variant_operator_equal(godot_variant* p_self, godot_variant* p_other)

    godot_bool godot_variant_operator_less(godot_variant* p_self, godot_variant* p_other)

    godot_bool godot_variant_hash_compare(godot_variant* p_self, godot_variant* p_other)

    godot_bool godot_variant_booleanize(godot_variant* p_self)

    void godot_variant_destroy(godot_variant* p_self)

    godot_string godot_variant_get_operator_name(godot_variant_operator p_op)

    void godot_variant_evaluate(godot_variant_operator p_op, godot_variant* p_a, godot_variant* p_b, godot_variant* r_ret, godot_bool* r_valid)

    void godot_array_new(godot_array* r_dest)

    void godot_array_new_copy(godot_array* r_dest, godot_array* p_src)

    void godot_array_new_pool_color_array(godot_array* r_dest, godot_pool_color_array* p_pca)

    void godot_array_new_pool_vector3_array(godot_array* r_dest, godot_pool_vector3_array* p_pv3a)

    void godot_array_new_pool_vector2_array(godot_array* r_dest, godot_pool_vector2_array* p_pv2a)

    void godot_array_new_pool_string_array(godot_array* r_dest, godot_pool_string_array* p_psa)

    void godot_array_new_pool_real_array(godot_array* r_dest, godot_pool_real_array* p_pra)

    void godot_array_new_pool_int_array(godot_array* r_dest, godot_pool_int_array* p_pia)

    void godot_array_new_pool_byte_array(godot_array* r_dest, godot_pool_byte_array* p_pba)

    void godot_array_set(godot_array* p_self, godot_int p_idx, godot_variant* p_value)

    godot_variant godot_array_get(godot_array* p_self, godot_int p_idx)

    godot_variant* godot_array_operator_index(godot_array* p_self, godot_int p_idx)

    godot_variant* godot_array_operator_index_const(godot_array* p_self, godot_int p_idx)

    void godot_array_append(godot_array* p_self, godot_variant* p_value)

    void godot_array_clear(godot_array* p_self)

    godot_int godot_array_count(godot_array* p_self, godot_variant* p_value)

    godot_bool godot_array_empty(godot_array* p_self)

    void godot_array_erase(godot_array* p_self, godot_variant* p_value)

    godot_variant godot_array_front(godot_array* p_self)

    godot_variant godot_array_back(godot_array* p_self)

    godot_int godot_array_find(godot_array* p_self, godot_variant* p_what, godot_int p_from)

    godot_int godot_array_find_last(godot_array* p_self, godot_variant* p_what)

    godot_bool godot_array_has(godot_array* p_self, godot_variant* p_value)

    godot_int godot_array_hash(godot_array* p_self)

    void godot_array_insert(godot_array* p_self, godot_int p_pos, godot_variant* p_value)

    void godot_array_invert(godot_array* p_self)

    godot_variant godot_array_pop_back(godot_array* p_self)

    godot_variant godot_array_pop_front(godot_array* p_self)

    void godot_array_push_back(godot_array* p_self, godot_variant* p_value)

    void godot_array_push_front(godot_array* p_self, godot_variant* p_value)

    void godot_array_remove(godot_array* p_self, godot_int p_idx)

    void godot_array_resize(godot_array* p_self, godot_int p_size)

    godot_int godot_array_rfind(godot_array* p_self, godot_variant* p_what, godot_int p_from)

    godot_int godot_array_size(godot_array* p_self)

    void godot_array_sort(godot_array* p_self)

    void godot_array_sort_custom(godot_array* p_self, godot_object* p_obj, godot_string* p_func)

    godot_int godot_array_bsearch(godot_array* p_self, godot_variant* p_value, godot_bool p_before)

    godot_int godot_array_bsearch_custom(godot_array* p_self, godot_variant* p_value, godot_object* p_obj, godot_string* p_func, godot_bool p_before)

    void godot_array_destroy(godot_array* p_self)

    godot_array godot_array_duplicate(godot_array* p_self, godot_bool p_deep)

    godot_variant godot_array_max(godot_array* p_self)

    godot_variant godot_array_min(godot_array* p_self)

    void godot_array_shuffle(godot_array* p_self)

    godot_int godot_char_string_length(godot_char_string* p_cs)

    char* godot_char_string_get_data(godot_char_string* p_cs)

    void godot_char_string_destroy(godot_char_string* p_cs)

    void godot_string_new(godot_string* r_dest)

    void godot_string_new_copy(godot_string* r_dest, godot_string* p_src)

    void godot_string_new_with_wide_string(godot_string* r_dest, wchar_t* p_contents, int p_size)

    wchar_t* godot_string_operator_index(godot_string* p_self, godot_int p_idx)

    wchar_t godot_string_operator_index_const(godot_string* p_self, godot_int p_idx)

    wchar_t* godot_string_wide_str(godot_string* p_self)

    godot_bool godot_string_operator_equal(godot_string* p_self, godot_string* p_b)

    godot_bool godot_string_operator_less(godot_string* p_self, godot_string* p_b)

    godot_string godot_string_operator_plus(godot_string* p_self, godot_string* p_b)

    godot_int godot_string_length(godot_string* p_self)

    signed char godot_string_casecmp_to(godot_string* p_self, godot_string* p_str)

    signed char godot_string_nocasecmp_to(godot_string* p_self, godot_string* p_str)

    signed char godot_string_naturalnocasecmp_to(godot_string* p_self, godot_string* p_str)

    godot_bool godot_string_begins_with(godot_string* p_self, godot_string* p_string)

    godot_bool godot_string_begins_with_char_array(godot_string* p_self, char* p_char_array)

    godot_array godot_string_bigrams(godot_string* p_self)

    godot_string godot_string_chr(wchar_t p_character)

    godot_bool godot_string_ends_with(godot_string* p_self, godot_string* p_string)

    godot_int godot_string_find(godot_string* p_self, godot_string p_what)

    godot_int godot_string_find_from(godot_string* p_self, godot_string p_what, godot_int p_from)

    godot_int godot_string_findmk(godot_string* p_self, godot_array* p_keys)

    godot_int godot_string_findmk_from(godot_string* p_self, godot_array* p_keys, godot_int p_from)

    godot_int godot_string_findmk_from_in_place(godot_string* p_self, godot_array* p_keys, godot_int p_from, godot_int* r_key)

    godot_int godot_string_findn(godot_string* p_self, godot_string p_what)

    godot_int godot_string_findn_from(godot_string* p_self, godot_string p_what, godot_int p_from)

    godot_int godot_string_find_last(godot_string* p_self, godot_string p_what)

    godot_string godot_string_format(godot_string* p_self, godot_variant* p_values)

    godot_string godot_string_format_with_custom_placeholder(godot_string* p_self, godot_variant* p_values, char* p_placeholder)

    godot_string godot_string_hex_encode_buffer(uint8_t* p_buffer, godot_int p_len)

    godot_int godot_string_hex_to_int(godot_string* p_self)

    godot_int godot_string_hex_to_int_without_prefix(godot_string* p_self)

    godot_string godot_string_insert(godot_string* p_self, godot_int p_at_pos, godot_string p_string)

    godot_bool godot_string_is_numeric(godot_string* p_self)

    godot_bool godot_string_is_subsequence_of(godot_string* p_self, godot_string* p_string)

    godot_bool godot_string_is_subsequence_ofi(godot_string* p_self, godot_string* p_string)

    godot_string godot_string_lpad(godot_string* p_self, godot_int p_min_length)

    godot_string godot_string_lpad_with_custom_character(godot_string* p_self, godot_int p_min_length, godot_string* p_character)

    godot_bool godot_string_match(godot_string* p_self, godot_string* p_wildcard)

    godot_bool godot_string_matchn(godot_string* p_self, godot_string* p_wildcard)

    godot_string godot_string_md5(uint8_t* p_md5)

    godot_string godot_string_num(double p_num)

    godot_string godot_string_num_int64(int64_t p_num, godot_int p_base)

    godot_string godot_string_num_int64_capitalized(int64_t p_num, godot_int p_base, godot_bool p_capitalize_hex)

    godot_string godot_string_num_real(double p_num)

    godot_string godot_string_num_scientific(double p_num)

    godot_string godot_string_num_with_decimals(double p_num, godot_int p_decimals)

    godot_string godot_string_pad_decimals(godot_string* p_self, godot_int p_digits)

    godot_string godot_string_pad_zeros(godot_string* p_self, godot_int p_digits)

    godot_string godot_string_replace_first(godot_string* p_self, godot_string p_key, godot_string p_with)

    godot_string godot_string_replace(godot_string* p_self, godot_string p_key, godot_string p_with)

    godot_string godot_string_replacen(godot_string* p_self, godot_string p_key, godot_string p_with)

    godot_int godot_string_rfind(godot_string* p_self, godot_string p_what)

    godot_int godot_string_rfindn(godot_string* p_self, godot_string p_what)

    godot_int godot_string_rfind_from(godot_string* p_self, godot_string p_what, godot_int p_from)

    godot_int godot_string_rfindn_from(godot_string* p_self, godot_string p_what, godot_int p_from)

    godot_string godot_string_rpad(godot_string* p_self, godot_int p_min_length)

    godot_string godot_string_rpad_with_custom_character(godot_string* p_self, godot_int p_min_length, godot_string* p_character)

    godot_real godot_string_similarity(godot_string* p_self, godot_string* p_string)

    godot_string godot_string_sprintf(godot_string* p_self, godot_array* p_values, godot_bool* p_error)

    godot_string godot_string_substr(godot_string* p_self, godot_int p_from, godot_int p_chars)

    double godot_string_to_double(godot_string* p_self)

    godot_real godot_string_to_float(godot_string* p_self)

    godot_int godot_string_to_int(godot_string* p_self)

    godot_string godot_string_camelcase_to_underscore(godot_string* p_self)

    godot_string godot_string_camelcase_to_underscore_lowercased(godot_string* p_self)

    godot_string godot_string_capitalize(godot_string* p_self)

    double godot_string_char_to_double(char* p_what)

    godot_int godot_string_char_to_int(char* p_what)

    int64_t godot_string_wchar_to_int(wchar_t* p_str)

    godot_int godot_string_char_to_int_with_len(char* p_what, godot_int p_len)

    int64_t godot_string_char_to_int64_with_len(wchar_t* p_str, int p_len)

    int64_t godot_string_hex_to_int64(godot_string* p_self)

    int64_t godot_string_hex_to_int64_with_prefix(godot_string* p_self)

    int64_t godot_string_to_int64(godot_string* p_self)

    double godot_string_unicode_char_to_double(wchar_t* p_str, wchar_t** r_end)

    godot_int godot_string_get_slice_count(godot_string* p_self, godot_string p_splitter)

    godot_string godot_string_get_slice(godot_string* p_self, godot_string p_splitter, godot_int p_slice)

    godot_string godot_string_get_slicec(godot_string* p_self, wchar_t p_splitter, godot_int p_slice)

    godot_array godot_string_split(godot_string* p_self, godot_string* p_splitter)

    godot_array godot_string_split_allow_empty(godot_string* p_self, godot_string* p_splitter)

    godot_array godot_string_split_floats(godot_string* p_self, godot_string* p_splitter)

    godot_array godot_string_split_floats_allows_empty(godot_string* p_self, godot_string* p_splitter)

    godot_array godot_string_split_floats_mk(godot_string* p_self, godot_array* p_splitters)

    godot_array godot_string_split_floats_mk_allows_empty(godot_string* p_self, godot_array* p_splitters)

    godot_array godot_string_split_ints(godot_string* p_self, godot_string* p_splitter)

    godot_array godot_string_split_ints_allows_empty(godot_string* p_self, godot_string* p_splitter)

    godot_array godot_string_split_ints_mk(godot_string* p_self, godot_array* p_splitters)

    godot_array godot_string_split_ints_mk_allows_empty(godot_string* p_self, godot_array* p_splitters)

    godot_array godot_string_split_spaces(godot_string* p_self)

    wchar_t godot_string_char_lowercase(wchar_t p_char)

    wchar_t godot_string_char_uppercase(wchar_t p_char)

    godot_string godot_string_to_lower(godot_string* p_self)

    godot_string godot_string_to_upper(godot_string* p_self)

    godot_string godot_string_get_basename(godot_string* p_self)

    godot_string godot_string_get_extension(godot_string* p_self)

    godot_string godot_string_left(godot_string* p_self, godot_int p_pos)

    wchar_t godot_string_ord_at(godot_string* p_self, godot_int p_idx)

    godot_string godot_string_plus_file(godot_string* p_self, godot_string* p_file)

    godot_string godot_string_right(godot_string* p_self, godot_int p_pos)

    godot_string godot_string_strip_edges(godot_string* p_self, godot_bool p_left, godot_bool p_right)

    godot_string godot_string_strip_escapes(godot_string* p_self)

    void godot_string_erase(godot_string* p_self, godot_int p_pos, godot_int p_chars)

    godot_char_string godot_string_ascii(godot_string* p_self)

    godot_char_string godot_string_ascii_extended(godot_string* p_self)

    godot_char_string godot_string_utf8(godot_string* p_self)

    godot_bool godot_string_parse_utf8(godot_string* p_self, char* p_utf8)

    godot_bool godot_string_parse_utf8_with_len(godot_string* p_self, char* p_utf8, godot_int p_len)

    godot_string godot_string_chars_to_utf8(char* p_utf8)

    godot_string godot_string_chars_to_utf8_with_len(char* p_utf8, godot_int p_len)

    uint32_t godot_string_hash(godot_string* p_self)

    uint64_t godot_string_hash64(godot_string* p_self)

    uint32_t godot_string_hash_chars(char* p_cstr)

    uint32_t godot_string_hash_chars_with_len(char* p_cstr, godot_int p_len)

    uint32_t godot_string_hash_utf8_chars(wchar_t* p_str)

    uint32_t godot_string_hash_utf8_chars_with_len(wchar_t* p_str, godot_int p_len)

    godot_pool_byte_array godot_string_md5_buffer(godot_string* p_self)

    godot_string godot_string_md5_text(godot_string* p_self)

    godot_pool_byte_array godot_string_sha256_buffer(godot_string* p_self)

    godot_string godot_string_sha256_text(godot_string* p_self)

    godot_bool godot_string_empty(godot_string* p_self)

    godot_string godot_string_get_base_dir(godot_string* p_self)

    godot_string godot_string_get_file(godot_string* p_self)

    godot_string godot_string_humanize_size(size_t p_size)

    godot_bool godot_string_is_abs_path(godot_string* p_self)

    godot_bool godot_string_is_rel_path(godot_string* p_self)

    godot_bool godot_string_is_resource_file(godot_string* p_self)

    godot_string godot_string_path_to(godot_string* p_self, godot_string* p_path)

    godot_string godot_string_path_to_file(godot_string* p_self, godot_string* p_path)

    godot_string godot_string_simplify_path(godot_string* p_self)

    godot_string godot_string_c_escape(godot_string* p_self)

    godot_string godot_string_c_escape_multiline(godot_string* p_self)

    godot_string godot_string_c_unescape(godot_string* p_self)

    godot_string godot_string_http_escape(godot_string* p_self)

    godot_string godot_string_http_unescape(godot_string* p_self)

    godot_string godot_string_json_escape(godot_string* p_self)

    godot_string godot_string_word_wrap(godot_string* p_self, godot_int p_chars_per_line)

    godot_string godot_string_xml_escape(godot_string* p_self)

    godot_string godot_string_xml_escape_with_quotes(godot_string* p_self)

    godot_string godot_string_xml_unescape(godot_string* p_self)

    godot_string godot_string_percent_decode(godot_string* p_self)

    godot_string godot_string_percent_encode(godot_string* p_self)

    godot_bool godot_string_is_valid_float(godot_string* p_self)

    godot_bool godot_string_is_valid_hex_number(godot_string* p_self, godot_bool p_with_prefix)

    godot_bool godot_string_is_valid_html_color(godot_string* p_self)

    godot_bool godot_string_is_valid_identifier(godot_string* p_self)

    godot_bool godot_string_is_valid_integer(godot_string* p_self)

    godot_bool godot_string_is_valid_ip_address(godot_string* p_self)

    godot_string godot_string_dedent(godot_string* p_self)

    godot_string godot_string_trim_prefix(godot_string* p_self, godot_string* p_prefix)

    godot_string godot_string_trim_suffix(godot_string* p_self, godot_string* p_suffix)

    godot_string godot_string_rstrip(godot_string* p_self, godot_string* p_chars)

    godot_pool_string_array godot_string_rsplit(godot_string* p_self, godot_string* p_divisor, godot_bool p_allow_empty, godot_int p_maxsplit)

    void godot_string_destroy(godot_string* p_self)

    ctypedef struct godot_string_name:
        uint8_t _dont_touch_that[sizeof(void *)]

    void godot_string_name_new(godot_string_name* r_dest, godot_string* p_name)

    void godot_string_name_new_data(godot_string_name* r_dest, char* p_name)

    godot_string godot_string_name_get_name(godot_string_name* p_self)

    uint32_t godot_string_name_get_hash(godot_string_name* p_self)

    void* godot_string_name_get_data_unique_pointer(godot_string_name* p_self)

    godot_bool godot_string_name_operator_equal(godot_string_name* p_self, godot_string_name* p_other)

    godot_bool godot_string_name_operator_less(godot_string_name* p_self, godot_string_name* p_other)

    void godot_string_name_destroy(godot_string_name* p_self)

    void godot_object_destroy(godot_object* p_o)

    godot_object* godot_global_get_singleton(char* p_name)

    ctypedef struct godot_method_bind:
        uint8_t _dont_touch_that[1]

    godot_method_bind* godot_method_bind_get_method(char* p_classname, char* p_methodname)

    void godot_method_bind_ptrcall(godot_method_bind* p_method_bind, godot_object* p_instance, void** p_args, void* p_ret)

    godot_variant godot_method_bind_call(godot_method_bind* p_method_bind, godot_object* p_instance, godot_variant** p_args, int p_arg_count, godot_variant_call_error* p_call_error)

    cdef struct godot_gdnative_api_version:
        unsigned int major
        unsigned int minor

    cdef struct godot_gdnative_api_struct:
        unsigned int type
        godot_gdnative_api_version version
        godot_gdnative_api_struct* next

    ctypedef void (*_godot_gdnative_init_options_godot_gdnative_init_options_report_version_mismatch_ft)(godot_object* p_library, char* p_what, godot_gdnative_api_version p_want, godot_gdnative_api_version p_have)

    ctypedef void (*_godot_gdnative_init_options_godot_gdnative_init_options_report_loading_error_ft)(godot_object* p_library, char* p_what)

    ctypedef struct godot_gdnative_init_options:
        godot_bool in_editor
        uint64_t core_api_hash
        uint64_t editor_api_hash
        uint64_t no_api_hash
        _godot_gdnative_init_options_godot_gdnative_init_options_report_version_mismatch_ft report_version_mismatch
        _godot_gdnative_init_options_godot_gdnative_init_options_report_loading_error_ft report_loading_error
        godot_object* gd_native_library
        godot_gdnative_core_api_struct* api_struct
        godot_string* active_library_path

    ctypedef struct godot_gdnative_terminate_options:
        godot_bool in_editor

    ctypedef godot_object* (*godot_class_constructor)()

    godot_class_constructor godot_get_class_constructor(char* p_classname)

    godot_dictionary godot_get_global_constants()

    ctypedef void (*godot_gdnative_init_fn)(godot_gdnative_init_options*)

    ctypedef void (*godot_gdnative_terminate_fn)(godot_gdnative_terminate_options*)

    ctypedef godot_variant (*godot_gdnative_procedure_fn)(godot_array*)

    ctypedef godot_variant (*native_call_cb)(void*, godot_array*)

    void godot_register_native_call_type(char* p_call_type, native_call_cb p_callback)

    void* godot_alloc(int p_bytes)

    void* godot_realloc(void* p_ptr, int p_bytes)

    void godot_free(void* p_ptr)

    void godot_print_error(char* p_description, char* p_function, char* p_file, int p_line)

    void godot_print_warning(char* p_description, char* p_function, char* p_file, int p_line)

    void godot_print(godot_string* p_message)

    bool godot_is_instance_valid(godot_object* p_object)
