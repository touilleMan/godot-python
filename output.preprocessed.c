typedef int uint16_t;
typedef int size_t;
typedef int uint8_t;
typedef int uint64_t;
typedef int int16_t;
typedef int int8_t;
typedef int uint32_t;
typedef int int64_t;
typedef int int32_t;
typedef int bool;
typedef int wchar_t;








































typedef enum {
	GODOT_OK,
	GODOT_FAILED,
	GODOT_ERR_UNAVAILABLE,
	GODOT_ERR_UNCONFIGURED,
	GODOT_ERR_UNAUTHORIZED,
	GODOT_ERR_PARAMETER_RANGE_ERROR,
	GODOT_ERR_OUT_OF_MEMORY,
	GODOT_ERR_FILE_NOT_FOUND,
	GODOT_ERR_FILE_BAD_DRIVE,
	GODOT_ERR_FILE_BAD_PATH,
	GODOT_ERR_FILE_NO_PERMISSION,
	GODOT_ERR_FILE_ALREADY_IN_USE,
	GODOT_ERR_FILE_CANT_OPEN,
	GODOT_ERR_FILE_CANT_WRITE,
	GODOT_ERR_FILE_CANT_READ,
	GODOT_ERR_FILE_UNRECOGNIZED,
	GODOT_ERR_FILE_CORRUPT,
	GODOT_ERR_FILE_MISSING_DEPENDENCIES,
	GODOT_ERR_FILE_EOF,
	GODOT_ERR_CANT_OPEN,
	GODOT_ERR_CANT_CREATE,
	GODOT_ERR_QUERY_FAILED,
	GODOT_ERR_ALREADY_IN_USE,
	GODOT_ERR_LOCKED,
	GODOT_ERR_TIMEOUT,
	GODOT_ERR_CANT_CONNECT,
	GODOT_ERR_CANT_RESOLVE,
	GODOT_ERR_CONNECTION_ERROR,
	GODOT_ERR_CANT_ACQUIRE_RESOURCE,
	GODOT_ERR_CANT_FORK,
	GODOT_ERR_INVALID_DATA,
	GODOT_ERR_INVALID_PARAMETER,
	GODOT_ERR_ALREADY_EXISTS,
	GODOT_ERR_DOES_NOT_EXIST,
	GODOT_ERR_DATABASE_CANT_READ,
	GODOT_ERR_DATABASE_CANT_WRITE,
	GODOT_ERR_COMPILATION_FAILED,
	GODOT_ERR_METHOD_NOT_FOUND,
	GODOT_ERR_LINK_FAILED,
	GODOT_ERR_SCRIPT_FAILED,
	GODOT_ERR_CYCLIC_LINK,
	GODOT_ERR_INVALID_DECLARATION,
	GODOT_ERR_DUPLICATE_SYMBOL,
	GODOT_ERR_PARSE_ERROR,
	GODOT_ERR_BUSY,
	GODOT_ERR_SKIP,
	GODOT_ERR_HELP,
	GODOT_ERR_BUG,
	GODOT_ERR_PRINTER_ON_FIRE,
} godot_error;



typedef bool godot_bool;




typedef int godot_int;



typedef float godot_real;


typedef void godot_object;



































typedef wchar_t godot_char_type;


typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_string;


typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_char_string;




































typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_array;






































typedef struct {
	uint8_t _dont_touch_that[1];
} godot_pool_array_read_access;

typedef godot_pool_array_read_access godot_pool_byte_array_read_access;
typedef godot_pool_array_read_access godot_pool_int_array_read_access;
typedef godot_pool_array_read_access godot_pool_real_array_read_access;
typedef godot_pool_array_read_access godot_pool_string_array_read_access;
typedef godot_pool_array_read_access godot_pool_vector2_array_read_access;
typedef godot_pool_array_read_access godot_pool_vector3_array_read_access;
typedef godot_pool_array_read_access godot_pool_color_array_read_access;




typedef struct {
	uint8_t _dont_touch_that[1];
} godot_pool_array_write_access;

typedef godot_pool_array_write_access godot_pool_byte_array_write_access;
typedef godot_pool_array_write_access godot_pool_int_array_write_access;
typedef godot_pool_array_write_access godot_pool_real_array_write_access;
typedef godot_pool_array_write_access godot_pool_string_array_write_access;
typedef godot_pool_array_write_access godot_pool_vector2_array_write_access;
typedef godot_pool_array_write_access godot_pool_vector3_array_write_access;
typedef godot_pool_array_write_access godot_pool_color_array_write_access;




typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_pool_byte_array;




typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_pool_int_array;




typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_pool_real_array;




typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_pool_string_array;




typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_pool_vector2_array;




typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_pool_vector3_array;




typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_pool_color_array;

































































typedef struct {
	uint8_t _dont_touch_that[16];
} godot_color;































































void  godot_color_new_rgba(godot_color *r_dest, const godot_real p_r, const godot_real p_g, const godot_real p_b, const godot_real p_a);
void  godot_color_new_rgb(godot_color *r_dest, const godot_real p_r, const godot_real p_g, const godot_real p_b);

godot_real godot_color_get_r(const godot_color *p_self);
void godot_color_set_r(godot_color *p_self, const godot_real r);

godot_real godot_color_get_g(const godot_color *p_self);
void godot_color_set_g(godot_color *p_self, const godot_real g);

godot_real godot_color_get_b(const godot_color *p_self);
void godot_color_set_b(godot_color *p_self, const godot_real b);

godot_real godot_color_get_a(const godot_color *p_self);
void godot_color_set_a(godot_color *p_self, const godot_real a);

godot_real godot_color_get_h(const godot_color *p_self);
godot_real godot_color_get_s(const godot_color *p_self);
godot_real godot_color_get_v(const godot_color *p_self);

godot_string  godot_color_as_string(const godot_color *p_self);

godot_int  godot_color_to_rgba32(const godot_color *p_self);

godot_int  godot_color_to_abgr32(const godot_color *p_self);

godot_int  godot_color_to_abgr64(const godot_color *p_self);

godot_int  godot_color_to_argb64(const godot_color *p_self);

godot_int  godot_color_to_rgba64(const godot_color *p_self);

godot_int  godot_color_to_argb32(const godot_color *p_self);

godot_real  godot_color_gray(const godot_color *p_self);

godot_color  godot_color_inverted(const godot_color *p_self);

godot_color  godot_color_contrasted(const godot_color *p_self);

godot_color  godot_color_linear_interpolate(const godot_color *p_self, const godot_color *p_b, const godot_real p_t);

godot_color  godot_color_blend(const godot_color *p_self, const godot_color *p_over);

godot_color  godot_color_darkened(const godot_color *p_self, const godot_real p_amount);

godot_color  godot_color_from_hsv(const godot_color *p_self, const godot_real p_h, const godot_real p_s, const godot_real p_v, const godot_real p_a);

godot_color  godot_color_lightened(const godot_color *p_self, const godot_real p_amount);

godot_string  godot_color_to_html(const godot_color *p_self, const godot_bool p_with_alpha);

godot_bool  godot_color_operator_equal(const godot_color *p_self, const godot_color *p_b);

godot_bool  godot_color_operator_less(const godot_color *p_self, const godot_color *p_b);



































typedef struct {
	uint8_t _dont_touch_that[8];
} godot_vector2;


































void  godot_vector2_new(godot_vector2 *r_dest, const godot_real p_x, const godot_real p_y);

godot_string  godot_vector2_as_string(const godot_vector2 *p_self);

godot_vector2  godot_vector2_normalized(const godot_vector2 *p_self);

godot_real  godot_vector2_length(const godot_vector2 *p_self);

godot_real  godot_vector2_angle(const godot_vector2 *p_self);

godot_real  godot_vector2_length_squared(const godot_vector2 *p_self);

godot_bool  godot_vector2_is_normalized(const godot_vector2 *p_self);

godot_vector2  godot_vector2_direction_to(const godot_vector2 *p_self, const godot_vector2 *p_b);

godot_real  godot_vector2_distance_to(const godot_vector2 *p_self, const godot_vector2 *p_to);

godot_real  godot_vector2_distance_squared_to(const godot_vector2 *p_self, const godot_vector2 *p_to);

godot_real  godot_vector2_angle_to(const godot_vector2 *p_self, const godot_vector2 *p_to);

godot_real  godot_vector2_angle_to_point(const godot_vector2 *p_self, const godot_vector2 *p_to);

godot_vector2  godot_vector2_linear_interpolate(const godot_vector2 *p_self, const godot_vector2 *p_b, const godot_real p_t);

godot_vector2  godot_vector2_cubic_interpolate(const godot_vector2 *p_self, const godot_vector2 *p_b, const godot_vector2 *p_pre_a, const godot_vector2 *p_post_b, const godot_real p_t);

godot_vector2  godot_vector2_move_toward(const godot_vector2 *p_self, const godot_vector2 *p_to, const godot_real p_delta);

godot_vector2  godot_vector2_rotated(const godot_vector2 *p_self, const godot_real p_phi);

godot_vector2  godot_vector2_tangent(const godot_vector2 *p_self);

godot_vector2  godot_vector2_floor(const godot_vector2 *p_self);

godot_vector2  godot_vector2_snapped(const godot_vector2 *p_self, const godot_vector2 *p_by);

godot_real  godot_vector2_aspect(const godot_vector2 *p_self);

godot_real  godot_vector2_dot(const godot_vector2 *p_self, const godot_vector2 *p_with);

godot_vector2  godot_vector2_slide(const godot_vector2 *p_self, const godot_vector2 *p_n);

godot_vector2  godot_vector2_bounce(const godot_vector2 *p_self, const godot_vector2 *p_n);

godot_vector2  godot_vector2_reflect(const godot_vector2 *p_self, const godot_vector2 *p_n);

godot_vector2  godot_vector2_abs(const godot_vector2 *p_self);

godot_vector2  godot_vector2_clamped(const godot_vector2 *p_self, const godot_real p_length);

godot_vector2  godot_vector2_operator_add(const godot_vector2 *p_self, const godot_vector2 *p_b);

godot_vector2  godot_vector2_operator_subtract(const godot_vector2 *p_self, const godot_vector2 *p_b);

godot_vector2  godot_vector2_operator_multiply_vector(const godot_vector2 *p_self, const godot_vector2 *p_b);

godot_vector2  godot_vector2_operator_multiply_scalar(const godot_vector2 *p_self, const godot_real p_b);

godot_vector2  godot_vector2_operator_divide_vector(const godot_vector2 *p_self, const godot_vector2 *p_b);

godot_vector2  godot_vector2_operator_divide_scalar(const godot_vector2 *p_self, const godot_real p_b);

godot_bool  godot_vector2_operator_equal(const godot_vector2 *p_self, const godot_vector2 *p_b);

godot_bool  godot_vector2_operator_less(const godot_vector2 *p_self, const godot_vector2 *p_b);

godot_vector2  godot_vector2_operator_neg(const godot_vector2 *p_self);

void  godot_vector2_set_x(godot_vector2 *p_self, const godot_real p_x);

void  godot_vector2_set_y(godot_vector2 *p_self, const godot_real p_y);

godot_real  godot_vector2_get_x(const godot_vector2 *p_self);

godot_real  godot_vector2_get_y(const godot_vector2 *p_self);



































typedef struct {
	uint8_t _dont_touch_that[12];
} godot_vector3;




































typedef struct {
	uint8_t _dont_touch_that[36];
} godot_basis;

































































typedef struct {
	uint8_t _dont_touch_that[16];
} godot_quat;































































void  godot_quat_new(godot_quat *r_dest, const godot_real p_x, const godot_real p_y, const godot_real p_z, const godot_real p_w);
void  godot_quat_new_with_axis_angle(godot_quat *r_dest, const godot_vector3 *p_axis, const godot_real p_angle);
void  godot_quat_new_with_basis(godot_quat *r_dest, const godot_basis *p_basis);
void  godot_quat_new_with_euler(godot_quat *r_dest, const godot_vector3 *p_euler);

godot_real  godot_quat_get_x(const godot_quat *p_self);
void  godot_quat_set_x(godot_quat *p_self, const godot_real val);

godot_real  godot_quat_get_y(const godot_quat *p_self);
void  godot_quat_set_y(godot_quat *p_self, const godot_real val);

godot_real  godot_quat_get_z(const godot_quat *p_self);
void  godot_quat_set_z(godot_quat *p_self, const godot_real val);

godot_real  godot_quat_get_w(const godot_quat *p_self);
void  godot_quat_set_w(godot_quat *p_self, const godot_real val);

godot_string  godot_quat_as_string(const godot_quat *p_self);

godot_real  godot_quat_length(const godot_quat *p_self);

godot_real  godot_quat_length_squared(const godot_quat *p_self);

godot_quat  godot_quat_normalized(const godot_quat *p_self);

godot_bool  godot_quat_is_normalized(const godot_quat *p_self);

godot_quat  godot_quat_inverse(const godot_quat *p_self);

godot_real  godot_quat_dot(const godot_quat *p_self, const godot_quat *p_b);

godot_vector3  godot_quat_xform(const godot_quat *p_self, const godot_vector3 *p_v);

godot_quat  godot_quat_slerp(const godot_quat *p_self, const godot_quat *p_b, const godot_real p_t);

godot_quat  godot_quat_slerpni(const godot_quat *p_self, const godot_quat *p_b, const godot_real p_t);

godot_quat  godot_quat_cubic_slerp(const godot_quat *p_self, const godot_quat *p_b, const godot_quat *p_pre_a, const godot_quat *p_post_b, const godot_real p_t);

godot_quat  godot_quat_operator_multiply(const godot_quat *p_self, const godot_real p_b);

godot_quat  godot_quat_operator_add(const godot_quat *p_self, const godot_quat *p_b);

godot_quat  godot_quat_operator_subtract(const godot_quat *p_self, const godot_quat *p_b);

godot_quat  godot_quat_operator_divide(const godot_quat *p_self, const godot_real p_b);

godot_bool  godot_quat_operator_equal(const godot_quat *p_self, const godot_quat *p_b);

godot_quat  godot_quat_operator_neg(const godot_quat *p_self);

void  godot_quat_set_axis_angle(godot_quat *p_self, const godot_vector3 *p_axis, const godot_real p_angle);

































void  godot_basis_new_with_rows(godot_basis *r_dest, const godot_vector3 *p_x_axis, const godot_vector3 *p_y_axis, const godot_vector3 *p_z_axis);
void  godot_basis_new_with_axis_and_angle(godot_basis *r_dest, const godot_vector3 *p_axis, const godot_real p_phi);
void  godot_basis_new_with_euler(godot_basis *r_dest, const godot_vector3 *p_euler);
void  godot_basis_new_with_euler_quat(godot_basis *r_dest, const godot_quat *p_euler);

godot_string  godot_basis_as_string(const godot_basis *p_self);

godot_basis  godot_basis_inverse(const godot_basis *p_self);

godot_basis  godot_basis_transposed(const godot_basis *p_self);

godot_basis  godot_basis_orthonormalized(const godot_basis *p_self);

godot_real  godot_basis_determinant(const godot_basis *p_self);

godot_basis  godot_basis_rotated(const godot_basis *p_self, const godot_vector3 *p_axis, const godot_real p_phi);

godot_basis  godot_basis_scaled(const godot_basis *p_self, const godot_vector3 *p_scale);

godot_vector3  godot_basis_get_scale(const godot_basis *p_self);

godot_vector3  godot_basis_get_euler(const godot_basis *p_self);

godot_quat  godot_basis_get_quat(const godot_basis *p_self);

void  godot_basis_set_quat(godot_basis *p_self, const godot_quat *p_quat);

void  godot_basis_set_axis_angle_scale(godot_basis *p_self, const godot_vector3 *p_axis, godot_real p_phi, const godot_vector3 *p_scale);

void  godot_basis_set_euler_scale(godot_basis *p_self, const godot_vector3 *p_euler, const godot_vector3 *p_scale);

void  godot_basis_set_quat_scale(godot_basis *p_self, const godot_quat *p_quat, const godot_vector3 *p_scale);

godot_real  godot_basis_tdotx(const godot_basis *p_self, const godot_vector3 *p_with);

godot_real  godot_basis_tdoty(const godot_basis *p_self, const godot_vector3 *p_with);

godot_real  godot_basis_tdotz(const godot_basis *p_self, const godot_vector3 *p_with);

godot_vector3  godot_basis_xform(const godot_basis *p_self, const godot_vector3 *p_v);

godot_vector3  godot_basis_xform_inv(const godot_basis *p_self, const godot_vector3 *p_v);

godot_int  godot_basis_get_orthogonal_index(const godot_basis *p_self);

void  godot_basis_new(godot_basis *r_dest);


void  godot_basis_get_elements(const godot_basis *p_self, godot_vector3 *p_elements);

godot_vector3  godot_basis_get_axis(const godot_basis *p_self, const godot_int p_axis);

void  godot_basis_set_axis(godot_basis *p_self, const godot_int p_axis, const godot_vector3 *p_value);

godot_vector3  godot_basis_get_row(const godot_basis *p_self, const godot_int p_row);

void  godot_basis_set_row(godot_basis *p_self, const godot_int p_row, const godot_vector3 *p_value);

godot_bool  godot_basis_operator_equal(const godot_basis *p_self, const godot_basis *p_b);

godot_basis  godot_basis_operator_add(const godot_basis *p_self, const godot_basis *p_b);

godot_basis  godot_basis_operator_subtract(const godot_basis *p_self, const godot_basis *p_b);

godot_basis  godot_basis_operator_multiply_vector(const godot_basis *p_self, const godot_basis *p_b);

godot_basis  godot_basis_operator_multiply_scalar(const godot_basis *p_self, const godot_real p_b);

godot_basis  godot_basis_slerp(const godot_basis *p_self, const godot_basis *p_b, const godot_real p_t);

































typedef enum {
	GODOT_VECTOR3_AXIS_X,
	GODOT_VECTOR3_AXIS_Y,
	GODOT_VECTOR3_AXIS_Z,
} godot_vector3_axis;

void  godot_vector3_new(godot_vector3 *r_dest, const godot_real p_x, const godot_real p_y, const godot_real p_z);

godot_string  godot_vector3_as_string(const godot_vector3 *p_self);

godot_int  godot_vector3_min_axis(const godot_vector3 *p_self);

godot_int  godot_vector3_max_axis(const godot_vector3 *p_self);

godot_real  godot_vector3_length(const godot_vector3 *p_self);

godot_real  godot_vector3_length_squared(const godot_vector3 *p_self);

godot_bool  godot_vector3_is_normalized(const godot_vector3 *p_self);

godot_vector3  godot_vector3_normalized(const godot_vector3 *p_self);

godot_vector3  godot_vector3_inverse(const godot_vector3 *p_self);

godot_vector3  godot_vector3_snapped(const godot_vector3 *p_self, const godot_vector3 *p_by);

godot_vector3  godot_vector3_rotated(const godot_vector3 *p_self, const godot_vector3 *p_axis, const godot_real p_phi);

godot_vector3  godot_vector3_linear_interpolate(const godot_vector3 *p_self, const godot_vector3 *p_b, const godot_real p_t);

godot_vector3  godot_vector3_cubic_interpolate(const godot_vector3 *p_self, const godot_vector3 *p_b, const godot_vector3 *p_pre_a, const godot_vector3 *p_post_b, const godot_real p_t);

godot_vector3  godot_vector3_move_toward(const godot_vector3 *p_self, const godot_vector3 *p_to, const godot_real p_delta);

godot_real  godot_vector3_dot(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_vector3  godot_vector3_cross(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_basis  godot_vector3_outer(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_basis  godot_vector3_to_diagonal_matrix(const godot_vector3 *p_self);

godot_vector3  godot_vector3_abs(const godot_vector3 *p_self);

godot_vector3  godot_vector3_floor(const godot_vector3 *p_self);

godot_vector3  godot_vector3_ceil(const godot_vector3 *p_self);

godot_vector3  godot_vector3_direction_to(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_real  godot_vector3_distance_to(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_real  godot_vector3_distance_squared_to(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_real  godot_vector3_angle_to(const godot_vector3 *p_self, const godot_vector3 *p_to);

godot_vector3  godot_vector3_slide(const godot_vector3 *p_self, const godot_vector3 *p_n);

godot_vector3  godot_vector3_bounce(const godot_vector3 *p_self, const godot_vector3 *p_n);

godot_vector3  godot_vector3_reflect(const godot_vector3 *p_self, const godot_vector3 *p_n);

godot_vector3  godot_vector3_operator_add(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_vector3  godot_vector3_operator_subtract(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_vector3  godot_vector3_operator_multiply_vector(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_vector3  godot_vector3_operator_multiply_scalar(const godot_vector3 *p_self, const godot_real p_b);

godot_vector3  godot_vector3_operator_divide_vector(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_vector3  godot_vector3_operator_divide_scalar(const godot_vector3 *p_self, const godot_real p_b);

godot_bool  godot_vector3_operator_equal(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_bool  godot_vector3_operator_less(const godot_vector3 *p_self, const godot_vector3 *p_b);

godot_vector3  godot_vector3_operator_neg(const godot_vector3 *p_self);

void  godot_vector3_set_axis(godot_vector3 *p_self, const godot_vector3_axis p_axis, const godot_real p_val);

godot_real  godot_vector3_get_axis(const godot_vector3 *p_self, const godot_vector3_axis p_axis);




































void  godot_pool_byte_array_new(godot_pool_byte_array *r_dest);
void  godot_pool_byte_array_new_copy(godot_pool_byte_array *r_dest, const godot_pool_byte_array *p_src);
void  godot_pool_byte_array_new_with_array(godot_pool_byte_array *r_dest, const godot_array *p_a);

void  godot_pool_byte_array_append(godot_pool_byte_array *p_self, const uint8_t p_data);

void  godot_pool_byte_array_append_array(godot_pool_byte_array *p_self, const godot_pool_byte_array *p_array);

godot_error  godot_pool_byte_array_insert(godot_pool_byte_array *p_self, const godot_int p_idx, const uint8_t p_data);

void  godot_pool_byte_array_invert(godot_pool_byte_array *p_self);

void  godot_pool_byte_array_push_back(godot_pool_byte_array *p_self, const uint8_t p_data);

void  godot_pool_byte_array_remove(godot_pool_byte_array *p_self, const godot_int p_idx);

void  godot_pool_byte_array_resize(godot_pool_byte_array *p_self, const godot_int p_size);

godot_pool_byte_array_read_access  *godot_pool_byte_array_read(const godot_pool_byte_array *p_self);

godot_pool_byte_array_write_access  *godot_pool_byte_array_write(godot_pool_byte_array *p_self);

void  godot_pool_byte_array_set(godot_pool_byte_array *p_self, const godot_int p_idx, const uint8_t p_data);
uint8_t  godot_pool_byte_array_get(const godot_pool_byte_array *p_self, const godot_int p_idx);

godot_int  godot_pool_byte_array_size(const godot_pool_byte_array *p_self);

godot_bool  godot_pool_byte_array_empty(const godot_pool_byte_array *p_self);

void  godot_pool_byte_array_destroy(godot_pool_byte_array *p_self);



void  godot_pool_int_array_new(godot_pool_int_array *r_dest);
void  godot_pool_int_array_new_copy(godot_pool_int_array *r_dest, const godot_pool_int_array *p_src);
void  godot_pool_int_array_new_with_array(godot_pool_int_array *r_dest, const godot_array *p_a);

void  godot_pool_int_array_append(godot_pool_int_array *p_self, const godot_int p_data);

void  godot_pool_int_array_append_array(godot_pool_int_array *p_self, const godot_pool_int_array *p_array);

godot_error  godot_pool_int_array_insert(godot_pool_int_array *p_self, const godot_int p_idx, const godot_int p_data);

void  godot_pool_int_array_invert(godot_pool_int_array *p_self);

void  godot_pool_int_array_push_back(godot_pool_int_array *p_self, const godot_int p_data);

void  godot_pool_int_array_remove(godot_pool_int_array *p_self, const godot_int p_idx);

void  godot_pool_int_array_resize(godot_pool_int_array *p_self, const godot_int p_size);

godot_pool_int_array_read_access  *godot_pool_int_array_read(const godot_pool_int_array *p_self);

godot_pool_int_array_write_access  *godot_pool_int_array_write(godot_pool_int_array *p_self);

void  godot_pool_int_array_set(godot_pool_int_array *p_self, const godot_int p_idx, const godot_int p_data);
godot_int  godot_pool_int_array_get(const godot_pool_int_array *p_self, const godot_int p_idx);

godot_int  godot_pool_int_array_size(const godot_pool_int_array *p_self);

godot_bool  godot_pool_int_array_empty(const godot_pool_int_array *p_self);

void  godot_pool_int_array_destroy(godot_pool_int_array *p_self);



void  godot_pool_real_array_new(godot_pool_real_array *r_dest);
void  godot_pool_real_array_new_copy(godot_pool_real_array *r_dest, const godot_pool_real_array *p_src);
void  godot_pool_real_array_new_with_array(godot_pool_real_array *r_dest, const godot_array *p_a);

void  godot_pool_real_array_append(godot_pool_real_array *p_self, const godot_real p_data);

void  godot_pool_real_array_append_array(godot_pool_real_array *p_self, const godot_pool_real_array *p_array);

godot_error  godot_pool_real_array_insert(godot_pool_real_array *p_self, const godot_int p_idx, const godot_real p_data);

void  godot_pool_real_array_invert(godot_pool_real_array *p_self);

void  godot_pool_real_array_push_back(godot_pool_real_array *p_self, const godot_real p_data);

void  godot_pool_real_array_remove(godot_pool_real_array *p_self, const godot_int p_idx);

void  godot_pool_real_array_resize(godot_pool_real_array *p_self, const godot_int p_size);

godot_pool_real_array_read_access  *godot_pool_real_array_read(const godot_pool_real_array *p_self);

godot_pool_real_array_write_access  *godot_pool_real_array_write(godot_pool_real_array *p_self);

void  godot_pool_real_array_set(godot_pool_real_array *p_self, const godot_int p_idx, const godot_real p_data);
godot_real  godot_pool_real_array_get(const godot_pool_real_array *p_self, const godot_int p_idx);

godot_int  godot_pool_real_array_size(const godot_pool_real_array *p_self);

godot_bool  godot_pool_real_array_empty(const godot_pool_real_array *p_self);

void  godot_pool_real_array_destroy(godot_pool_real_array *p_self);



void  godot_pool_string_array_new(godot_pool_string_array *r_dest);
void  godot_pool_string_array_new_copy(godot_pool_string_array *r_dest, const godot_pool_string_array *p_src);
void  godot_pool_string_array_new_with_array(godot_pool_string_array *r_dest, const godot_array *p_a);

void  godot_pool_string_array_append(godot_pool_string_array *p_self, const godot_string *p_data);

void  godot_pool_string_array_append_array(godot_pool_string_array *p_self, const godot_pool_string_array *p_array);

godot_error  godot_pool_string_array_insert(godot_pool_string_array *p_self, const godot_int p_idx, const godot_string *p_data);

void  godot_pool_string_array_invert(godot_pool_string_array *p_self);

void  godot_pool_string_array_push_back(godot_pool_string_array *p_self, const godot_string *p_data);

void  godot_pool_string_array_remove(godot_pool_string_array *p_self, const godot_int p_idx);

void  godot_pool_string_array_resize(godot_pool_string_array *p_self, const godot_int p_size);

godot_pool_string_array_read_access  *godot_pool_string_array_read(const godot_pool_string_array *p_self);

godot_pool_string_array_write_access  *godot_pool_string_array_write(godot_pool_string_array *p_self);

void  godot_pool_string_array_set(godot_pool_string_array *p_self, const godot_int p_idx, const godot_string *p_data);
godot_string  godot_pool_string_array_get(const godot_pool_string_array *p_self, const godot_int p_idx);

godot_int  godot_pool_string_array_size(const godot_pool_string_array *p_self);

godot_bool  godot_pool_string_array_empty(const godot_pool_string_array *p_self);

void  godot_pool_string_array_destroy(godot_pool_string_array *p_self);



void  godot_pool_vector2_array_new(godot_pool_vector2_array *r_dest);
void  godot_pool_vector2_array_new_copy(godot_pool_vector2_array *r_dest, const godot_pool_vector2_array *p_src);
void  godot_pool_vector2_array_new_with_array(godot_pool_vector2_array *r_dest, const godot_array *p_a);

void  godot_pool_vector2_array_append(godot_pool_vector2_array *p_self, const godot_vector2 *p_data);

void  godot_pool_vector2_array_append_array(godot_pool_vector2_array *p_self, const godot_pool_vector2_array *p_array);

godot_error  godot_pool_vector2_array_insert(godot_pool_vector2_array *p_self, const godot_int p_idx, const godot_vector2 *p_data);

void  godot_pool_vector2_array_invert(godot_pool_vector2_array *p_self);

void  godot_pool_vector2_array_push_back(godot_pool_vector2_array *p_self, const godot_vector2 *p_data);

void  godot_pool_vector2_array_remove(godot_pool_vector2_array *p_self, const godot_int p_idx);

void  godot_pool_vector2_array_resize(godot_pool_vector2_array *p_self, const godot_int p_size);

godot_pool_vector2_array_read_access  *godot_pool_vector2_array_read(const godot_pool_vector2_array *p_self);

godot_pool_vector2_array_write_access  *godot_pool_vector2_array_write(godot_pool_vector2_array *p_self);

void  godot_pool_vector2_array_set(godot_pool_vector2_array *p_self, const godot_int p_idx, const godot_vector2 *p_data);
godot_vector2  godot_pool_vector2_array_get(const godot_pool_vector2_array *p_self, const godot_int p_idx);

godot_int  godot_pool_vector2_array_size(const godot_pool_vector2_array *p_self);

godot_bool  godot_pool_vector2_array_empty(const godot_pool_vector2_array *p_self);

void  godot_pool_vector2_array_destroy(godot_pool_vector2_array *p_self);



void  godot_pool_vector3_array_new(godot_pool_vector3_array *r_dest);
void  godot_pool_vector3_array_new_copy(godot_pool_vector3_array *r_dest, const godot_pool_vector3_array *p_src);
void  godot_pool_vector3_array_new_with_array(godot_pool_vector3_array *r_dest, const godot_array *p_a);

void  godot_pool_vector3_array_append(godot_pool_vector3_array *p_self, const godot_vector3 *p_data);

void  godot_pool_vector3_array_append_array(godot_pool_vector3_array *p_self, const godot_pool_vector3_array *p_array);

godot_error  godot_pool_vector3_array_insert(godot_pool_vector3_array *p_self, const godot_int p_idx, const godot_vector3 *p_data);

void  godot_pool_vector3_array_invert(godot_pool_vector3_array *p_self);

void  godot_pool_vector3_array_push_back(godot_pool_vector3_array *p_self, const godot_vector3 *p_data);

void  godot_pool_vector3_array_remove(godot_pool_vector3_array *p_self, const godot_int p_idx);

void  godot_pool_vector3_array_resize(godot_pool_vector3_array *p_self, const godot_int p_size);

godot_pool_vector3_array_read_access  *godot_pool_vector3_array_read(const godot_pool_vector3_array *p_self);

godot_pool_vector3_array_write_access  *godot_pool_vector3_array_write(godot_pool_vector3_array *p_self);

void  godot_pool_vector3_array_set(godot_pool_vector3_array *p_self, const godot_int p_idx, const godot_vector3 *p_data);
godot_vector3  godot_pool_vector3_array_get(const godot_pool_vector3_array *p_self, const godot_int p_idx);

godot_int  godot_pool_vector3_array_size(const godot_pool_vector3_array *p_self);

godot_bool  godot_pool_vector3_array_empty(const godot_pool_vector3_array *p_self);

void  godot_pool_vector3_array_destroy(godot_pool_vector3_array *p_self);



void  godot_pool_color_array_new(godot_pool_color_array *r_dest);
void  godot_pool_color_array_new_copy(godot_pool_color_array *r_dest, const godot_pool_color_array *p_src);
void  godot_pool_color_array_new_with_array(godot_pool_color_array *r_dest, const godot_array *p_a);

void  godot_pool_color_array_append(godot_pool_color_array *p_self, const godot_color *p_data);

void  godot_pool_color_array_append_array(godot_pool_color_array *p_self, const godot_pool_color_array *p_array);

godot_error  godot_pool_color_array_insert(godot_pool_color_array *p_self, const godot_int p_idx, const godot_color *p_data);

void  godot_pool_color_array_invert(godot_pool_color_array *p_self);

void  godot_pool_color_array_push_back(godot_pool_color_array *p_self, const godot_color *p_data);

void  godot_pool_color_array_remove(godot_pool_color_array *p_self, const godot_int p_idx);

void  godot_pool_color_array_resize(godot_pool_color_array *p_self, const godot_int p_size);

godot_pool_color_array_read_access  *godot_pool_color_array_read(const godot_pool_color_array *p_self);

godot_pool_color_array_write_access  *godot_pool_color_array_write(godot_pool_color_array *p_self);

void  godot_pool_color_array_set(godot_pool_color_array *p_self, const godot_int p_idx, const godot_color *p_data);
godot_color  godot_pool_color_array_get(const godot_pool_color_array *p_self, const godot_int p_idx);

godot_int  godot_pool_color_array_size(const godot_pool_color_array *p_self);

godot_bool  godot_pool_color_array_empty(const godot_pool_color_array *p_self);

void  godot_pool_color_array_destroy(godot_pool_color_array *p_self);





godot_pool_byte_array_read_access  *godot_pool_byte_array_read_access_copy(const godot_pool_byte_array_read_access *p_other);
const uint8_t  *godot_pool_byte_array_read_access_ptr(const godot_pool_byte_array_read_access *p_read);
void  godot_pool_byte_array_read_access_operator_assign(godot_pool_byte_array_read_access *p_read, godot_pool_byte_array_read_access *p_other);
void  godot_pool_byte_array_read_access_destroy(godot_pool_byte_array_read_access *p_read);

godot_pool_int_array_read_access  *godot_pool_int_array_read_access_copy(const godot_pool_int_array_read_access *p_other);
const godot_int  *godot_pool_int_array_read_access_ptr(const godot_pool_int_array_read_access *p_read);
void  godot_pool_int_array_read_access_operator_assign(godot_pool_int_array_read_access *p_read, godot_pool_int_array_read_access *p_other);
void  godot_pool_int_array_read_access_destroy(godot_pool_int_array_read_access *p_read);

godot_pool_real_array_read_access  *godot_pool_real_array_read_access_copy(const godot_pool_real_array_read_access *p_other);
const godot_real  *godot_pool_real_array_read_access_ptr(const godot_pool_real_array_read_access *p_read);
void  godot_pool_real_array_read_access_operator_assign(godot_pool_real_array_read_access *p_read, godot_pool_real_array_read_access *p_other);
void  godot_pool_real_array_read_access_destroy(godot_pool_real_array_read_access *p_read);

godot_pool_string_array_read_access  *godot_pool_string_array_read_access_copy(const godot_pool_string_array_read_access *p_other);
const godot_string  *godot_pool_string_array_read_access_ptr(const godot_pool_string_array_read_access *p_read);
void  godot_pool_string_array_read_access_operator_assign(godot_pool_string_array_read_access *p_read, godot_pool_string_array_read_access *p_other);
void  godot_pool_string_array_read_access_destroy(godot_pool_string_array_read_access *p_read);

godot_pool_vector2_array_read_access  *godot_pool_vector2_array_read_access_copy(const godot_pool_vector2_array_read_access *p_other);
const godot_vector2  *godot_pool_vector2_array_read_access_ptr(const godot_pool_vector2_array_read_access *p_read);
void  godot_pool_vector2_array_read_access_operator_assign(godot_pool_vector2_array_read_access *p_read, godot_pool_vector2_array_read_access *p_other);
void  godot_pool_vector2_array_read_access_destroy(godot_pool_vector2_array_read_access *p_read);

godot_pool_vector3_array_read_access  *godot_pool_vector3_array_read_access_copy(const godot_pool_vector3_array_read_access *p_other);
const godot_vector3  *godot_pool_vector3_array_read_access_ptr(const godot_pool_vector3_array_read_access *p_read);
void  godot_pool_vector3_array_read_access_operator_assign(godot_pool_vector3_array_read_access *p_read, godot_pool_vector3_array_read_access *p_other);
void  godot_pool_vector3_array_read_access_destroy(godot_pool_vector3_array_read_access *p_read);

godot_pool_color_array_read_access  *godot_pool_color_array_read_access_copy(const godot_pool_color_array_read_access *p_other);
const godot_color  *godot_pool_color_array_read_access_ptr(const godot_pool_color_array_read_access *p_read);
void  godot_pool_color_array_read_access_operator_assign(godot_pool_color_array_read_access *p_read, godot_pool_color_array_read_access *p_other);
void  godot_pool_color_array_read_access_destroy(godot_pool_color_array_read_access *p_read);





godot_pool_byte_array_write_access  *godot_pool_byte_array_write_access_copy(const godot_pool_byte_array_write_access *p_other);
uint8_t  *godot_pool_byte_array_write_access_ptr(const godot_pool_byte_array_write_access *p_write);
void  godot_pool_byte_array_write_access_operator_assign(godot_pool_byte_array_write_access *p_write, godot_pool_byte_array_write_access *p_other);
void  godot_pool_byte_array_write_access_destroy(godot_pool_byte_array_write_access *p_write);

godot_pool_int_array_write_access  *godot_pool_int_array_write_access_copy(const godot_pool_int_array_write_access *p_other);
godot_int  *godot_pool_int_array_write_access_ptr(const godot_pool_int_array_write_access *p_write);
void  godot_pool_int_array_write_access_operator_assign(godot_pool_int_array_write_access *p_write, godot_pool_int_array_write_access *p_other);
void  godot_pool_int_array_write_access_destroy(godot_pool_int_array_write_access *p_write);

godot_pool_real_array_write_access  *godot_pool_real_array_write_access_copy(const godot_pool_real_array_write_access *p_other);
godot_real  *godot_pool_real_array_write_access_ptr(const godot_pool_real_array_write_access *p_write);
void  godot_pool_real_array_write_access_operator_assign(godot_pool_real_array_write_access *p_write, godot_pool_real_array_write_access *p_other);
void  godot_pool_real_array_write_access_destroy(godot_pool_real_array_write_access *p_write);

godot_pool_string_array_write_access  *godot_pool_string_array_write_access_copy(const godot_pool_string_array_write_access *p_other);
godot_string  *godot_pool_string_array_write_access_ptr(const godot_pool_string_array_write_access *p_write);
void  godot_pool_string_array_write_access_operator_assign(godot_pool_string_array_write_access *p_write, godot_pool_string_array_write_access *p_other);
void  godot_pool_string_array_write_access_destroy(godot_pool_string_array_write_access *p_write);

godot_pool_vector2_array_write_access  *godot_pool_vector2_array_write_access_copy(const godot_pool_vector2_array_write_access *p_other);
godot_vector2  *godot_pool_vector2_array_write_access_ptr(const godot_pool_vector2_array_write_access *p_write);
void  godot_pool_vector2_array_write_access_operator_assign(godot_pool_vector2_array_write_access *p_write, godot_pool_vector2_array_write_access *p_other);
void  godot_pool_vector2_array_write_access_destroy(godot_pool_vector2_array_write_access *p_write);

godot_pool_vector3_array_write_access  *godot_pool_vector3_array_write_access_copy(const godot_pool_vector3_array_write_access *p_other);
godot_vector3  *godot_pool_vector3_array_write_access_ptr(const godot_pool_vector3_array_write_access *p_write);
void  godot_pool_vector3_array_write_access_operator_assign(godot_pool_vector3_array_write_access *p_write, godot_pool_vector3_array_write_access *p_other);
void  godot_pool_vector3_array_write_access_destroy(godot_pool_vector3_array_write_access *p_write);

godot_pool_color_array_write_access  *godot_pool_color_array_write_access_copy(const godot_pool_color_array_write_access *p_other);
godot_color  *godot_pool_color_array_write_access_ptr(const godot_pool_color_array_write_access *p_write);
void  godot_pool_color_array_write_access_operator_assign(godot_pool_color_array_write_access *p_write, godot_pool_color_array_write_access *p_other);
void  godot_pool_color_array_write_access_destroy(godot_pool_color_array_write_access *p_write);



































typedef struct {
	uint8_t _dont_touch_that[(16 + sizeof(int64_t))];
} godot_variant;

typedef enum godot_variant_type {
	GODOT_VARIANT_TYPE_NIL,


	GODOT_VARIANT_TYPE_BOOL,
	GODOT_VARIANT_TYPE_INT,
	GODOT_VARIANT_TYPE_REAL,
	GODOT_VARIANT_TYPE_STRING,



	GODOT_VARIANT_TYPE_VECTOR2,
	GODOT_VARIANT_TYPE_RECT2,
	GODOT_VARIANT_TYPE_VECTOR3,
	GODOT_VARIANT_TYPE_TRANSFORM2D,
	GODOT_VARIANT_TYPE_PLANE,
	GODOT_VARIANT_TYPE_QUAT,
	GODOT_VARIANT_TYPE_AABB,
	GODOT_VARIANT_TYPE_BASIS,
	GODOT_VARIANT_TYPE_TRANSFORM,


	GODOT_VARIANT_TYPE_COLOR,
	GODOT_VARIANT_TYPE_NODE_PATH,
	GODOT_VARIANT_TYPE_RID,
	GODOT_VARIANT_TYPE_OBJECT,
	GODOT_VARIANT_TYPE_DICTIONARY,
	GODOT_VARIANT_TYPE_ARRAY,


	GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY,
	GODOT_VARIANT_TYPE_POOL_INT_ARRAY,
	GODOT_VARIANT_TYPE_POOL_REAL_ARRAY,
	GODOT_VARIANT_TYPE_POOL_STRING_ARRAY,
	GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY,
	GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY,
	GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY,
} godot_variant_type;

typedef enum godot_variant_call_error_error {
	GODOT_CALL_ERROR_CALL_OK,
	GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD,
	GODOT_CALL_ERROR_CALL_ERROR_INVALID_ARGUMENT,
	GODOT_CALL_ERROR_CALL_ERROR_TOO_MANY_ARGUMENTS,
	GODOT_CALL_ERROR_CALL_ERROR_TOO_FEW_ARGUMENTS,
	GODOT_CALL_ERROR_CALL_ERROR_INSTANCE_IS_NULL,
} godot_variant_call_error_error;

typedef struct godot_variant_call_error {
	godot_variant_call_error_error error;
	int argument;
	godot_variant_type expected;
} godot_variant_call_error;

typedef enum godot_variant_operator {

	GODOT_VARIANT_OP_EQUAL,
	GODOT_VARIANT_OP_NOT_EQUAL,
	GODOT_VARIANT_OP_LESS,
	GODOT_VARIANT_OP_LESS_EQUAL,
	GODOT_VARIANT_OP_GREATER,
	GODOT_VARIANT_OP_GREATER_EQUAL,


	GODOT_VARIANT_OP_ADD,
	GODOT_VARIANT_OP_SUBTRACT,
	GODOT_VARIANT_OP_MULTIPLY,
	GODOT_VARIANT_OP_DIVIDE,
	GODOT_VARIANT_OP_NEGATE,
	GODOT_VARIANT_OP_POSITIVE,
	GODOT_VARIANT_OP_MODULE,
	GODOT_VARIANT_OP_STRING_CONCAT,


	GODOT_VARIANT_OP_SHIFT_LEFT,
	GODOT_VARIANT_OP_SHIFT_RIGHT,
	GODOT_VARIANT_OP_BIT_AND,
	GODOT_VARIANT_OP_BIT_OR,
	GODOT_VARIANT_OP_BIT_XOR,
	GODOT_VARIANT_OP_BIT_NEGATE,


	GODOT_VARIANT_OP_AND,
	GODOT_VARIANT_OP_OR,
	GODOT_VARIANT_OP_XOR,
	GODOT_VARIANT_OP_NOT,


	GODOT_VARIANT_OP_IN,

	GODOT_VARIANT_OP_MAX,
} godot_variant_operator;




































typedef struct {
	uint8_t _dont_touch_that[24];
} godot_aabb;

































































typedef struct {
	uint8_t _dont_touch_that[16];
} godot_plane;































































void  godot_plane_new_with_reals(godot_plane *r_dest, const godot_real p_a, const godot_real p_b, const godot_real p_c, const godot_real p_d);
void  godot_plane_new_with_vectors(godot_plane *r_dest, const godot_vector3 *p_v1, const godot_vector3 *p_v2, const godot_vector3 *p_v3);
void  godot_plane_new_with_normal(godot_plane *r_dest, const godot_vector3 *p_normal, const godot_real p_d);

godot_string  godot_plane_as_string(const godot_plane *p_self);

godot_plane  godot_plane_normalized(const godot_plane *p_self);

godot_vector3  godot_plane_center(const godot_plane *p_self);

godot_vector3  godot_plane_get_any_point(const godot_plane *p_self);

godot_bool  godot_plane_is_point_over(const godot_plane *p_self, const godot_vector3 *p_point);

godot_real  godot_plane_distance_to(const godot_plane *p_self, const godot_vector3 *p_point);

godot_bool  godot_plane_has_point(const godot_plane *p_self, const godot_vector3 *p_point, const godot_real p_epsilon);

godot_vector3  godot_plane_project(const godot_plane *p_self, const godot_vector3 *p_point);

godot_bool  godot_plane_intersect_3(const godot_plane *p_self, godot_vector3 *r_dest, const godot_plane *p_b, const godot_plane *p_c);

godot_bool  godot_plane_intersects_ray(const godot_plane *p_self, godot_vector3 *r_dest, const godot_vector3 *p_from, const godot_vector3 *p_dir);

godot_bool  godot_plane_intersects_segment(const godot_plane *p_self, godot_vector3 *r_dest, const godot_vector3 *p_begin, const godot_vector3 *p_end);

godot_plane  godot_plane_operator_neg(const godot_plane *p_self);

godot_bool  godot_plane_operator_equal(const godot_plane *p_self, const godot_plane *p_b);

void  godot_plane_set_normal(godot_plane *p_self, const godot_vector3 *p_normal);

godot_vector3  godot_plane_get_normal(const godot_plane *p_self);

godot_real  godot_plane_get_d(const godot_plane *p_self);

void  godot_plane_set_d(godot_plane *p_self, const godot_real p_d);

































void  godot_aabb_new(godot_aabb *r_dest, const godot_vector3 *p_pos, const godot_vector3 *p_size);

godot_vector3  godot_aabb_get_position(const godot_aabb *p_self);
void  godot_aabb_set_position(const godot_aabb *p_self, const godot_vector3 *p_v);

godot_vector3  godot_aabb_get_size(const godot_aabb *p_self);
void  godot_aabb_set_size(const godot_aabb *p_self, const godot_vector3 *p_v);

godot_string  godot_aabb_as_string(const godot_aabb *p_self);

godot_real  godot_aabb_get_area(const godot_aabb *p_self);

godot_bool  godot_aabb_has_no_area(const godot_aabb *p_self);

godot_bool  godot_aabb_has_no_surface(const godot_aabb *p_self);

godot_bool  godot_aabb_intersects(const godot_aabb *p_self, const godot_aabb *p_with);

godot_bool  godot_aabb_encloses(const godot_aabb *p_self, const godot_aabb *p_with);

godot_aabb  godot_aabb_merge(const godot_aabb *p_self, const godot_aabb *p_with);

godot_aabb  godot_aabb_intersection(const godot_aabb *p_self, const godot_aabb *p_with);

godot_bool  godot_aabb_intersects_plane(const godot_aabb *p_self, const godot_plane *p_plane);

godot_bool  godot_aabb_intersects_segment(const godot_aabb *p_self, const godot_vector3 *p_from, const godot_vector3 *p_to);

godot_bool  godot_aabb_has_point(const godot_aabb *p_self, const godot_vector3 *p_point);

godot_vector3  godot_aabb_get_support(const godot_aabb *p_self, const godot_vector3 *p_dir);

godot_vector3  godot_aabb_get_longest_axis(const godot_aabb *p_self);

godot_int  godot_aabb_get_longest_axis_index(const godot_aabb *p_self);

godot_real  godot_aabb_get_longest_axis_size(const godot_aabb *p_self);

godot_vector3  godot_aabb_get_shortest_axis(const godot_aabb *p_self);

godot_int  godot_aabb_get_shortest_axis_index(const godot_aabb *p_self);

godot_real  godot_aabb_get_shortest_axis_size(const godot_aabb *p_self);

godot_aabb  godot_aabb_expand(const godot_aabb *p_self, const godot_vector3 *p_to_point);

godot_aabb  godot_aabb_grow(const godot_aabb *p_self, const godot_real p_by);

godot_vector3  godot_aabb_get_endpoint(const godot_aabb *p_self, const godot_int p_idx);

godot_bool  godot_aabb_operator_equal(const godot_aabb *p_self, const godot_aabb *p_b);


























































































































typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_dictionary;




























































































void  godot_dictionary_new(godot_dictionary *r_dest);
void  godot_dictionary_new_copy(godot_dictionary *r_dest, const godot_dictionary *p_src);
void  godot_dictionary_destroy(godot_dictionary *p_self);

godot_dictionary  godot_dictionary_duplicate(const godot_dictionary *p_self, const godot_bool p_deep);

godot_int  godot_dictionary_size(const godot_dictionary *p_self);

godot_bool  godot_dictionary_empty(const godot_dictionary *p_self);

void  godot_dictionary_clear(godot_dictionary *p_self);

godot_bool  godot_dictionary_has(const godot_dictionary *p_self, const godot_variant *p_key);

godot_bool  godot_dictionary_has_all(const godot_dictionary *p_self, const godot_array *p_keys);

void  godot_dictionary_erase(godot_dictionary *p_self, const godot_variant *p_key);

godot_int  godot_dictionary_hash(const godot_dictionary *p_self);

godot_array  godot_dictionary_keys(const godot_dictionary *p_self);

godot_array  godot_dictionary_values(const godot_dictionary *p_self);

godot_variant  godot_dictionary_get(const godot_dictionary *p_self, const godot_variant *p_key);
void  godot_dictionary_set(godot_dictionary *p_self, const godot_variant *p_key, const godot_variant *p_value);

godot_variant  *godot_dictionary_operator_index(godot_dictionary *p_self, const godot_variant *p_key);

const godot_variant  *godot_dictionary_operator_index_const(const godot_dictionary *p_self, const godot_variant *p_key);

godot_variant  *godot_dictionary_next(const godot_dictionary *p_self, const godot_variant *p_key);

godot_bool  godot_dictionary_operator_equal(const godot_dictionary *p_self, const godot_dictionary *p_b);

godot_string  godot_dictionary_to_json(const godot_dictionary *p_self);



godot_bool  godot_dictionary_erase_with_return(godot_dictionary *p_self, const godot_variant *p_key);

godot_variant  godot_dictionary_get_with_default(const godot_dictionary *p_self, const godot_variant *p_key, const godot_variant *p_default);



































typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_node_path;































































void  godot_node_path_new(godot_node_path *r_dest, const godot_string *p_from);
void  godot_node_path_new_copy(godot_node_path *r_dest, const godot_node_path *p_src);
void  godot_node_path_destroy(godot_node_path *p_self);

godot_string  godot_node_path_as_string(const godot_node_path *p_self);

godot_bool  godot_node_path_is_absolute(const godot_node_path *p_self);

godot_int  godot_node_path_get_name_count(const godot_node_path *p_self);

godot_string  godot_node_path_get_name(const godot_node_path *p_self, const godot_int p_idx);

godot_int  godot_node_path_get_subname_count(const godot_node_path *p_self);

godot_string  godot_node_path_get_subname(const godot_node_path *p_self, const godot_int p_idx);

godot_string  godot_node_path_get_concatenated_subnames(const godot_node_path *p_self);

godot_bool  godot_node_path_is_empty(const godot_node_path *p_self);

godot_bool  godot_node_path_operator_equal(const godot_node_path *p_self, const godot_node_path *p_b);

godot_node_path godot_node_path_get_as_property_path(const godot_node_path *p_self);

























































































































typedef struct godot_rect2 {
	uint8_t _dont_touch_that[16];
} godot_rect2;































































void  godot_rect2_new_with_position_and_size(godot_rect2 *r_dest, const godot_vector2 *p_pos, const godot_vector2 *p_size);
void  godot_rect2_new(godot_rect2 *r_dest, const godot_real p_x, const godot_real p_y, const godot_real p_width, const godot_real p_height);

godot_string  godot_rect2_as_string(const godot_rect2 *p_self);

godot_real  godot_rect2_get_area(const godot_rect2 *p_self);

godot_bool  godot_rect2_intersects(const godot_rect2 *p_self, const godot_rect2 *p_b);

godot_bool  godot_rect2_encloses(const godot_rect2 *p_self, const godot_rect2 *p_b);

godot_bool  godot_rect2_has_no_area(const godot_rect2 *p_self);

godot_rect2  godot_rect2_clip(const godot_rect2 *p_self, const godot_rect2 *p_b);

godot_rect2  godot_rect2_merge(const godot_rect2 *p_self, const godot_rect2 *p_b);

godot_bool  godot_rect2_has_point(const godot_rect2 *p_self, const godot_vector2 *p_point);

godot_rect2  godot_rect2_grow(const godot_rect2 *p_self, const godot_real p_by);

godot_rect2  godot_rect2_grow_individual(const godot_rect2 *p_self, const godot_real p_left, const godot_real p_top, const godot_real p_right, const godot_real p_bottom);

godot_rect2  godot_rect2_grow_margin(const godot_rect2 *p_self, const godot_int p_margin, const godot_real p_by);

godot_rect2  godot_rect2_abs(const godot_rect2 *p_self);

godot_rect2  godot_rect2_expand(const godot_rect2 *p_self, const godot_vector2 *p_to);

godot_bool  godot_rect2_operator_equal(const godot_rect2 *p_self, const godot_rect2 *p_b);

godot_vector2  godot_rect2_get_position(const godot_rect2 *p_self);

godot_vector2  godot_rect2_get_size(const godot_rect2 *p_self);

void  godot_rect2_set_position(godot_rect2 *p_self, const godot_vector2 *p_pos);

void  godot_rect2_set_size(godot_rect2 *p_self, const godot_vector2 *p_size);



































typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_rid;


































void  godot_rid_new(godot_rid *r_dest);

godot_int  godot_rid_get_id(const godot_rid *p_self);

void  godot_rid_new_with_resource(godot_rid *r_dest, const godot_object *p_from);

godot_bool  godot_rid_operator_equal(const godot_rid *p_self, const godot_rid *p_b);

godot_bool  godot_rid_operator_less(const godot_rid *p_self, const godot_rid *p_b);
































































typedef struct {
	uint8_t _dont_touch_that[48];
} godot_transform;

























































































































void  godot_transform_new_with_axis_origin(godot_transform *r_dest, const godot_vector3 *p_x_axis, const godot_vector3 *p_y_axis, const godot_vector3 *p_z_axis, const godot_vector3 *p_origin);
void  godot_transform_new(godot_transform *r_dest, const godot_basis *p_basis, const godot_vector3 *p_origin);
void  godot_transform_new_with_quat(godot_transform *r_dest, const godot_quat *p_quat);

godot_basis  godot_transform_get_basis(const godot_transform *p_self);
void  godot_transform_set_basis(godot_transform *p_self, const godot_basis *p_v);

godot_vector3  godot_transform_get_origin(const godot_transform *p_self);
void  godot_transform_set_origin(godot_transform *p_self, const godot_vector3 *p_v);

godot_string  godot_transform_as_string(const godot_transform *p_self);

godot_transform  godot_transform_inverse(const godot_transform *p_self);

godot_transform  godot_transform_affine_inverse(const godot_transform *p_self);

godot_transform  godot_transform_orthonormalized(const godot_transform *p_self);

godot_transform  godot_transform_rotated(const godot_transform *p_self, const godot_vector3 *p_axis, const godot_real p_phi);

godot_transform  godot_transform_scaled(const godot_transform *p_self, const godot_vector3 *p_scale);

godot_transform  godot_transform_translated(const godot_transform *p_self, const godot_vector3 *p_ofs);

godot_transform  godot_transform_looking_at(const godot_transform *p_self, const godot_vector3 *p_target, const godot_vector3 *p_up);

godot_plane  godot_transform_xform_plane(const godot_transform *p_self, const godot_plane *p_v);

godot_plane  godot_transform_xform_inv_plane(const godot_transform *p_self, const godot_plane *p_v);

void  godot_transform_new_identity(godot_transform *r_dest);

godot_bool  godot_transform_operator_equal(const godot_transform *p_self, const godot_transform *p_b);

godot_transform  godot_transform_operator_multiply(const godot_transform *p_self, const godot_transform *p_b);

godot_vector3  godot_transform_xform_vector3(const godot_transform *p_self, const godot_vector3 *p_v);

godot_vector3  godot_transform_xform_inv_vector3(const godot_transform *p_self, const godot_vector3 *p_v);

godot_aabb  godot_transform_xform_aabb(const godot_transform *p_self, const godot_aabb *p_v);

godot_aabb  godot_transform_xform_inv_aabb(const godot_transform *p_self, const godot_aabb *p_v);



































typedef struct {
	uint8_t _dont_touch_that[24];
} godot_transform2d;




























































































void  godot_transform2d_new(godot_transform2d *r_dest, const godot_real p_rot, const godot_vector2 *p_pos);
void  godot_transform2d_new_axis_origin(godot_transform2d *r_dest, const godot_vector2 *p_x_axis, const godot_vector2 *p_y_axis, const godot_vector2 *p_origin);

godot_string  godot_transform2d_as_string(const godot_transform2d *p_self);

godot_transform2d  godot_transform2d_inverse(const godot_transform2d *p_self);

godot_transform2d  godot_transform2d_affine_inverse(const godot_transform2d *p_self);

godot_real  godot_transform2d_get_rotation(const godot_transform2d *p_self);

godot_vector2  godot_transform2d_get_origin(const godot_transform2d *p_self);

godot_vector2  godot_transform2d_get_scale(const godot_transform2d *p_self);

godot_transform2d  godot_transform2d_orthonormalized(const godot_transform2d *p_self);

godot_transform2d  godot_transform2d_rotated(const godot_transform2d *p_self, const godot_real p_phi);

godot_transform2d  godot_transform2d_scaled(const godot_transform2d *p_self, const godot_vector2 *p_scale);

godot_transform2d  godot_transform2d_translated(const godot_transform2d *p_self, const godot_vector2 *p_offset);

godot_vector2  godot_transform2d_xform_vector2(const godot_transform2d *p_self, const godot_vector2 *p_v);

godot_vector2  godot_transform2d_xform_inv_vector2(const godot_transform2d *p_self, const godot_vector2 *p_v);

godot_vector2  godot_transform2d_basis_xform_vector2(const godot_transform2d *p_self, const godot_vector2 *p_v);

godot_vector2  godot_transform2d_basis_xform_inv_vector2(const godot_transform2d *p_self, const godot_vector2 *p_v);

godot_transform2d  godot_transform2d_interpolate_with(const godot_transform2d *p_self, const godot_transform2d *p_m, const godot_real p_c);

godot_bool  godot_transform2d_operator_equal(const godot_transform2d *p_self, const godot_transform2d *p_b);

godot_transform2d  godot_transform2d_operator_multiply(const godot_transform2d *p_self, const godot_transform2d *p_b);

void  godot_transform2d_new_identity(godot_transform2d *r_dest);

godot_rect2  godot_transform2d_xform_rect2(const godot_transform2d *p_self, const godot_rect2 *p_v);

godot_rect2  godot_transform2d_xform_inv_rect2(const godot_transform2d *p_self, const godot_rect2 *p_v);

























































































































godot_variant_type  godot_variant_get_type(const godot_variant *p_v);

void  godot_variant_new_copy(godot_variant *r_dest, const godot_variant *p_src);

void  godot_variant_new_nil(godot_variant *r_dest);

void  godot_variant_new_bool(godot_variant *r_dest, const godot_bool p_b);
void  godot_variant_new_uint(godot_variant *r_dest, const uint64_t p_i);
void  godot_variant_new_int(godot_variant *r_dest, const int64_t p_i);
void  godot_variant_new_real(godot_variant *r_dest, const double p_r);
void  godot_variant_new_string(godot_variant *r_dest, const godot_string *p_s);
void  godot_variant_new_vector2(godot_variant *r_dest, const godot_vector2 *p_v2);
void  godot_variant_new_rect2(godot_variant *r_dest, const godot_rect2 *p_rect2);
void  godot_variant_new_vector3(godot_variant *r_dest, const godot_vector3 *p_v3);
void  godot_variant_new_transform2d(godot_variant *r_dest, const godot_transform2d *p_t2d);
void  godot_variant_new_plane(godot_variant *r_dest, const godot_plane *p_plane);
void  godot_variant_new_quat(godot_variant *r_dest, const godot_quat *p_quat);
void  godot_variant_new_aabb(godot_variant *r_dest, const godot_aabb *p_aabb);
void  godot_variant_new_basis(godot_variant *r_dest, const godot_basis *p_basis);
void  godot_variant_new_transform(godot_variant *r_dest, const godot_transform *p_trans);
void  godot_variant_new_color(godot_variant *r_dest, const godot_color *p_color);
void  godot_variant_new_node_path(godot_variant *r_dest, const godot_node_path *p_np);
void  godot_variant_new_rid(godot_variant *r_dest, const godot_rid *p_rid);
void  godot_variant_new_object(godot_variant *r_dest, const godot_object *p_obj);
void  godot_variant_new_dictionary(godot_variant *r_dest, const godot_dictionary *p_dict);
void  godot_variant_new_array(godot_variant *r_dest, const godot_array *p_arr);
void  godot_variant_new_pool_byte_array(godot_variant *r_dest, const godot_pool_byte_array *p_pba);
void  godot_variant_new_pool_int_array(godot_variant *r_dest, const godot_pool_int_array *p_pia);
void  godot_variant_new_pool_real_array(godot_variant *r_dest, const godot_pool_real_array *p_pra);
void  godot_variant_new_pool_string_array(godot_variant *r_dest, const godot_pool_string_array *p_psa);
void  godot_variant_new_pool_vector2_array(godot_variant *r_dest, const godot_pool_vector2_array *p_pv2a);
void  godot_variant_new_pool_vector3_array(godot_variant *r_dest, const godot_pool_vector3_array *p_pv3a);
void  godot_variant_new_pool_color_array(godot_variant *r_dest, const godot_pool_color_array *p_pca);

godot_bool  godot_variant_as_bool(const godot_variant *p_self);
uint64_t  godot_variant_as_uint(const godot_variant *p_self);
int64_t  godot_variant_as_int(const godot_variant *p_self);
double  godot_variant_as_real(const godot_variant *p_self);
godot_string  godot_variant_as_string(const godot_variant *p_self);
godot_vector2  godot_variant_as_vector2(const godot_variant *p_self);
godot_rect2  godot_variant_as_rect2(const godot_variant *p_self);
godot_vector3  godot_variant_as_vector3(const godot_variant *p_self);
godot_transform2d  godot_variant_as_transform2d(const godot_variant *p_self);
godot_plane  godot_variant_as_plane(const godot_variant *p_self);
godot_quat  godot_variant_as_quat(const godot_variant *p_self);
godot_aabb  godot_variant_as_aabb(const godot_variant *p_self);
godot_basis  godot_variant_as_basis(const godot_variant *p_self);
godot_transform  godot_variant_as_transform(const godot_variant *p_self);
godot_color  godot_variant_as_color(const godot_variant *p_self);
godot_node_path  godot_variant_as_node_path(const godot_variant *p_self);
godot_rid  godot_variant_as_rid(const godot_variant *p_self);
godot_object  *godot_variant_as_object(const godot_variant *p_self);
godot_dictionary  godot_variant_as_dictionary(const godot_variant *p_self);
godot_array  godot_variant_as_array(const godot_variant *p_self);
godot_pool_byte_array  godot_variant_as_pool_byte_array(const godot_variant *p_self);
godot_pool_int_array  godot_variant_as_pool_int_array(const godot_variant *p_self);
godot_pool_real_array  godot_variant_as_pool_real_array(const godot_variant *p_self);
godot_pool_string_array  godot_variant_as_pool_string_array(const godot_variant *p_self);
godot_pool_vector2_array  godot_variant_as_pool_vector2_array(const godot_variant *p_self);
godot_pool_vector3_array  godot_variant_as_pool_vector3_array(const godot_variant *p_self);
godot_pool_color_array  godot_variant_as_pool_color_array(const godot_variant *p_self);

godot_variant  godot_variant_call(godot_variant *p_self, const godot_string *p_method, const godot_variant **p_args, const godot_int p_argcount, godot_variant_call_error *r_error);

godot_bool  godot_variant_has_method(const godot_variant *p_self, const godot_string *p_method);

godot_bool  godot_variant_operator_equal(const godot_variant *p_self, const godot_variant *p_other);
godot_bool  godot_variant_operator_less(const godot_variant *p_self, const godot_variant *p_other);

godot_bool  godot_variant_hash_compare(const godot_variant *p_self, const godot_variant *p_other);

godot_bool  godot_variant_booleanize(const godot_variant *p_self);

void  godot_variant_destroy(godot_variant *p_self);



godot_string  godot_variant_get_operator_name(godot_variant_operator p_op);
void  godot_variant_evaluate(godot_variant_operator p_op, const godot_variant *p_a, const godot_variant *p_b, godot_variant *r_ret, godot_bool *r_valid);


































void  godot_array_new(godot_array *r_dest);
void  godot_array_new_copy(godot_array *r_dest, const godot_array *p_src);
void  godot_array_new_pool_color_array(godot_array *r_dest, const godot_pool_color_array *p_pca);
void  godot_array_new_pool_vector3_array(godot_array *r_dest, const godot_pool_vector3_array *p_pv3a);
void  godot_array_new_pool_vector2_array(godot_array *r_dest, const godot_pool_vector2_array *p_pv2a);
void  godot_array_new_pool_string_array(godot_array *r_dest, const godot_pool_string_array *p_psa);
void  godot_array_new_pool_real_array(godot_array *r_dest, const godot_pool_real_array *p_pra);
void  godot_array_new_pool_int_array(godot_array *r_dest, const godot_pool_int_array *p_pia);
void  godot_array_new_pool_byte_array(godot_array *r_dest, const godot_pool_byte_array *p_pba);

void  godot_array_set(godot_array *p_self, const godot_int p_idx, const godot_variant *p_value);

godot_variant  godot_array_get(const godot_array *p_self, const godot_int p_idx);

godot_variant  *godot_array_operator_index(godot_array *p_self, const godot_int p_idx);

const godot_variant  *godot_array_operator_index_const(const godot_array *p_self, const godot_int p_idx);

void  godot_array_append(godot_array *p_self, const godot_variant *p_value);

void  godot_array_clear(godot_array *p_self);

godot_int  godot_array_count(const godot_array *p_self, const godot_variant *p_value);

godot_bool  godot_array_empty(const godot_array *p_self);

void  godot_array_erase(godot_array *p_self, const godot_variant *p_value);

godot_variant  godot_array_front(const godot_array *p_self);

godot_variant  godot_array_back(const godot_array *p_self);

godot_int  godot_array_find(const godot_array *p_self, const godot_variant *p_what, const godot_int p_from);

godot_int  godot_array_find_last(const godot_array *p_self, const godot_variant *p_what);

godot_bool  godot_array_has(const godot_array *p_self, const godot_variant *p_value);

godot_int  godot_array_hash(const godot_array *p_self);

void  godot_array_insert(godot_array *p_self, const godot_int p_pos, const godot_variant *p_value);

void  godot_array_invert(godot_array *p_self);

godot_variant  godot_array_pop_back(godot_array *p_self);

godot_variant  godot_array_pop_front(godot_array *p_self);

void  godot_array_push_back(godot_array *p_self, const godot_variant *p_value);

void  godot_array_push_front(godot_array *p_self, const godot_variant *p_value);

void  godot_array_remove(godot_array *p_self, const godot_int p_idx);

void  godot_array_resize(godot_array *p_self, const godot_int p_size);

godot_int  godot_array_rfind(const godot_array *p_self, const godot_variant *p_what, const godot_int p_from);

godot_int  godot_array_size(const godot_array *p_self);

void  godot_array_sort(godot_array *p_self);

void  godot_array_sort_custom(godot_array *p_self, godot_object *p_obj, const godot_string *p_func);

godot_int  godot_array_bsearch(godot_array *p_self, const godot_variant *p_value, const godot_bool p_before);

godot_int  godot_array_bsearch_custom(godot_array *p_self, const godot_variant *p_value, godot_object *p_obj, const godot_string *p_func, const godot_bool p_before);

void  godot_array_destroy(godot_array *p_self);

godot_array  godot_array_duplicate(const godot_array *p_self, const godot_bool p_deep);

godot_array  godot_array_slice(const godot_array *p_self, const godot_int p_begin, const godot_int p_end, const godot_int p_step, const godot_bool p_deep);

godot_variant  godot_array_max(const godot_array *p_self);

godot_variant  godot_array_min(const godot_array *p_self);

void  godot_array_shuffle(godot_array *p_self);






























































godot_int  godot_char_string_length(const godot_char_string *p_cs);
const char  *godot_char_string_get_data(const godot_char_string *p_cs);
void  godot_char_string_destroy(godot_char_string *p_cs);

void  godot_string_new(godot_string *r_dest);
void  godot_string_new_copy(godot_string *r_dest, const godot_string *p_src);
void  godot_string_new_with_wide_string(godot_string *r_dest, const wchar_t *p_contents, const int p_size);

const wchar_t  *godot_string_operator_index(godot_string *p_self, const godot_int p_idx);
wchar_t  godot_string_operator_index_const(const godot_string *p_self, const godot_int p_idx);
const wchar_t  *godot_string_wide_str(const godot_string *p_self);

godot_bool  godot_string_operator_equal(const godot_string *p_self, const godot_string *p_b);
godot_bool  godot_string_operator_less(const godot_string *p_self, const godot_string *p_b);
godot_string  godot_string_operator_plus(const godot_string *p_self, const godot_string *p_b);



godot_int  godot_string_length(const godot_string *p_self);



signed char  godot_string_casecmp_to(const godot_string *p_self, const godot_string *p_str);
signed char  godot_string_nocasecmp_to(const godot_string *p_self, const godot_string *p_str);
signed char  godot_string_naturalnocasecmp_to(const godot_string *p_self, const godot_string *p_str);

godot_bool  godot_string_begins_with(const godot_string *p_self, const godot_string *p_string);
godot_bool  godot_string_begins_with_char_array(const godot_string *p_self, const char *p_char_array);
godot_array  godot_string_bigrams(const godot_string *p_self);
godot_string  godot_string_chr(wchar_t p_character);
godot_bool  godot_string_ends_with(const godot_string *p_self, const godot_string *p_string);
godot_int  godot_string_count(const godot_string *p_self, godot_string p_what, godot_int p_from, godot_int p_to);
godot_int  godot_string_countn(const godot_string *p_self, godot_string p_what, godot_int p_from, godot_int p_to);
godot_int  godot_string_find(const godot_string *p_self, godot_string p_what);
godot_int  godot_string_find_from(const godot_string *p_self, godot_string p_what, godot_int p_from);
godot_int  godot_string_findmk(const godot_string *p_self, const godot_array *p_keys);
godot_int  godot_string_findmk_from(const godot_string *p_self, const godot_array *p_keys, godot_int p_from);
godot_int  godot_string_findmk_from_in_place(const godot_string *p_self, const godot_array *p_keys, godot_int p_from, godot_int *r_key);
godot_int  godot_string_findn(const godot_string *p_self, godot_string p_what);
godot_int  godot_string_findn_from(const godot_string *p_self, godot_string p_what, godot_int p_from);
godot_int  godot_string_find_last(const godot_string *p_self, godot_string p_what);
godot_string  godot_string_format(const godot_string *p_self, const godot_variant *p_values);
godot_string  godot_string_format_with_custom_placeholder(const godot_string *p_self, const godot_variant *p_values, const char *p_placeholder);
godot_string  godot_string_hex_encode_buffer(const uint8_t *p_buffer, godot_int p_len);
godot_int  godot_string_hex_to_int(const godot_string *p_self);
godot_int  godot_string_hex_to_int_without_prefix(const godot_string *p_self);
godot_string  godot_string_insert(const godot_string *p_self, godot_int p_at_pos, godot_string p_string);
godot_bool  godot_string_is_numeric(const godot_string *p_self);
godot_bool  godot_string_is_subsequence_of(const godot_string *p_self, const godot_string *p_string);
godot_bool  godot_string_is_subsequence_ofi(const godot_string *p_self, const godot_string *p_string);
godot_string  godot_string_lpad(const godot_string *p_self, godot_int p_min_length);
godot_string  godot_string_lpad_with_custom_character(const godot_string *p_self, godot_int p_min_length, const godot_string *p_character);
godot_bool  godot_string_match(const godot_string *p_self, const godot_string *p_wildcard);
godot_bool  godot_string_matchn(const godot_string *p_self, const godot_string *p_wildcard);
godot_string  godot_string_md5(const uint8_t *p_md5);
godot_string  godot_string_num(double p_num);
godot_string  godot_string_num_int64(int64_t p_num, godot_int p_base);
godot_string  godot_string_num_int64_capitalized(int64_t p_num, godot_int p_base, godot_bool p_capitalize_hex);
godot_string  godot_string_num_real(double p_num);
godot_string  godot_string_num_scientific(double p_num);
godot_string  godot_string_num_with_decimals(double p_num, godot_int p_decimals);
godot_string  godot_string_pad_decimals(const godot_string *p_self, godot_int p_digits);
godot_string  godot_string_pad_zeros(const godot_string *p_self, godot_int p_digits);
godot_string  godot_string_replace_first(const godot_string *p_self, godot_string p_key, godot_string p_with);
godot_string  godot_string_replace(const godot_string *p_self, godot_string p_key, godot_string p_with);
godot_string  godot_string_replacen(const godot_string *p_self, godot_string p_key, godot_string p_with);
godot_int  godot_string_rfind(const godot_string *p_self, godot_string p_what);
godot_int  godot_string_rfindn(const godot_string *p_self, godot_string p_what);
godot_int  godot_string_rfind_from(const godot_string *p_self, godot_string p_what, godot_int p_from);
godot_int  godot_string_rfindn_from(const godot_string *p_self, godot_string p_what, godot_int p_from);
godot_string  godot_string_rpad(const godot_string *p_self, godot_int p_min_length);
godot_string  godot_string_rpad_with_custom_character(const godot_string *p_self, godot_int p_min_length, const godot_string *p_character);
godot_real  godot_string_similarity(const godot_string *p_self, const godot_string *p_string);
godot_string  godot_string_sprintf(const godot_string *p_self, const godot_array *p_values, godot_bool *p_error);
godot_string  godot_string_substr(const godot_string *p_self, godot_int p_from, godot_int p_chars);
double  godot_string_to_double(const godot_string *p_self);
godot_real  godot_string_to_float(const godot_string *p_self);
godot_int  godot_string_to_int(const godot_string *p_self);

godot_string  godot_string_camelcase_to_underscore(const godot_string *p_self);
godot_string  godot_string_camelcase_to_underscore_lowercased(const godot_string *p_self);
godot_string  godot_string_capitalize(const godot_string *p_self);
double  godot_string_char_to_double(const char *p_what);
godot_int  godot_string_char_to_int(const char *p_what);
int64_t  godot_string_wchar_to_int(const wchar_t *p_str);
godot_int  godot_string_char_to_int_with_len(const char *p_what, godot_int p_len);
int64_t  godot_string_char_to_int64_with_len(const wchar_t *p_str, int p_len);
int64_t  godot_string_hex_to_int64(const godot_string *p_self);
int64_t  godot_string_hex_to_int64_with_prefix(const godot_string *p_self);
int64_t  godot_string_to_int64(const godot_string *p_self);
double  godot_string_unicode_char_to_double(const wchar_t *p_str, const wchar_t **r_end);

godot_int  godot_string_get_slice_count(const godot_string *p_self, godot_string p_splitter);
godot_string  godot_string_get_slice(const godot_string *p_self, godot_string p_splitter, godot_int p_slice);
godot_string  godot_string_get_slicec(const godot_string *p_self, wchar_t p_splitter, godot_int p_slice);

godot_array  godot_string_split(const godot_string *p_self, const godot_string *p_splitter);
godot_array  godot_string_split_allow_empty(const godot_string *p_self, const godot_string *p_splitter);
godot_array  godot_string_split_floats(const godot_string *p_self, const godot_string *p_splitter);
godot_array  godot_string_split_floats_allows_empty(const godot_string *p_self, const godot_string *p_splitter);
godot_array  godot_string_split_floats_mk(const godot_string *p_self, const godot_array *p_splitters);
godot_array  godot_string_split_floats_mk_allows_empty(const godot_string *p_self, const godot_array *p_splitters);
godot_array  godot_string_split_ints(const godot_string *p_self, const godot_string *p_splitter);
godot_array  godot_string_split_ints_allows_empty(const godot_string *p_self, const godot_string *p_splitter);
godot_array  godot_string_split_ints_mk(const godot_string *p_self, const godot_array *p_splitters);
godot_array  godot_string_split_ints_mk_allows_empty(const godot_string *p_self, const godot_array *p_splitters);
godot_array  godot_string_split_spaces(const godot_string *p_self);

wchar_t  godot_string_char_lowercase(wchar_t p_char);
wchar_t  godot_string_char_uppercase(wchar_t p_char);
godot_string  godot_string_to_lower(const godot_string *p_self);
godot_string  godot_string_to_upper(const godot_string *p_self);

godot_string  godot_string_get_basename(const godot_string *p_self);
godot_string  godot_string_get_extension(const godot_string *p_self);
godot_string  godot_string_left(const godot_string *p_self, godot_int p_pos);
wchar_t  godot_string_ord_at(const godot_string *p_self, godot_int p_idx);
godot_string  godot_string_plus_file(const godot_string *p_self, const godot_string *p_file);
godot_string  godot_string_right(const godot_string *p_self, godot_int p_pos);
godot_string  godot_string_strip_edges(const godot_string *p_self, godot_bool p_left, godot_bool p_right);
godot_string  godot_string_strip_escapes(const godot_string *p_self);

void  godot_string_erase(godot_string *p_self, godot_int p_pos, godot_int p_chars);

godot_char_string  godot_string_ascii(const godot_string *p_self);
godot_char_string  godot_string_ascii_extended(const godot_string *p_self);
godot_char_string  godot_string_utf8(const godot_string *p_self);
godot_bool  godot_string_parse_utf8(godot_string *p_self, const char *p_utf8);
godot_bool  godot_string_parse_utf8_with_len(godot_string *p_self, const char *p_utf8, godot_int p_len);
godot_string  godot_string_chars_to_utf8(const char *p_utf8);
godot_string  godot_string_chars_to_utf8_with_len(const char *p_utf8, godot_int p_len);

uint32_t  godot_string_hash(const godot_string *p_self);
uint64_t  godot_string_hash64(const godot_string *p_self);
uint32_t  godot_string_hash_chars(const char *p_cstr);
uint32_t  godot_string_hash_chars_with_len(const char *p_cstr, godot_int p_len);
uint32_t  godot_string_hash_utf8_chars(const wchar_t *p_str);
uint32_t  godot_string_hash_utf8_chars_with_len(const wchar_t *p_str, godot_int p_len);
godot_pool_byte_array  godot_string_md5_buffer(const godot_string *p_self);
godot_string  godot_string_md5_text(const godot_string *p_self);
godot_pool_byte_array  godot_string_sha256_buffer(const godot_string *p_self);
godot_string  godot_string_sha256_text(const godot_string *p_self);

godot_bool godot_string_empty(const godot_string *p_self);


godot_string  godot_string_get_base_dir(const godot_string *p_self);
godot_string  godot_string_get_file(const godot_string *p_self);
godot_string  godot_string_humanize_size(uint64_t p_size);
godot_bool  godot_string_is_abs_path(const godot_string *p_self);
godot_bool  godot_string_is_rel_path(const godot_string *p_self);
godot_bool  godot_string_is_resource_file(const godot_string *p_self);
godot_string  godot_string_path_to(const godot_string *p_self, const godot_string *p_path);
godot_string  godot_string_path_to_file(const godot_string *p_self, const godot_string *p_path);
godot_string  godot_string_simplify_path(const godot_string *p_self);

godot_string  godot_string_c_escape(const godot_string *p_self);
godot_string  godot_string_c_escape_multiline(const godot_string *p_self);
godot_string  godot_string_c_unescape(const godot_string *p_self);
godot_string  godot_string_http_escape(const godot_string *p_self);
godot_string  godot_string_http_unescape(const godot_string *p_self);
godot_string  godot_string_json_escape(const godot_string *p_self);
godot_string  godot_string_word_wrap(const godot_string *p_self, godot_int p_chars_per_line);
godot_string  godot_string_xml_escape(const godot_string *p_self);
godot_string  godot_string_xml_escape_with_quotes(const godot_string *p_self);
godot_string  godot_string_xml_unescape(const godot_string *p_self);

godot_string  godot_string_percent_decode(const godot_string *p_self);
godot_string  godot_string_percent_encode(const godot_string *p_self);

godot_bool  godot_string_is_valid_float(const godot_string *p_self);
godot_bool  godot_string_is_valid_hex_number(const godot_string *p_self, godot_bool p_with_prefix);
godot_bool  godot_string_is_valid_html_color(const godot_string *p_self);
godot_bool  godot_string_is_valid_identifier(const godot_string *p_self);
godot_bool  godot_string_is_valid_integer(const godot_string *p_self);
godot_bool  godot_string_is_valid_ip_address(const godot_string *p_self);

godot_string  godot_string_dedent(const godot_string *p_self);
godot_string  godot_string_trim_prefix(const godot_string *p_self, const godot_string *p_prefix);
godot_string  godot_string_trim_suffix(const godot_string *p_self, const godot_string *p_suffix);
godot_string  godot_string_rstrip(const godot_string *p_self, const godot_string *p_chars);
godot_pool_string_array  godot_string_rsplit(const godot_string *p_self, const godot_string *p_divisor, const godot_bool p_allow_empty, const godot_int p_maxsplit);

void  godot_string_destroy(godot_string *p_self);






































typedef struct {
	uint8_t _dont_touch_that[sizeof(void *)];
} godot_string_name;


































void  godot_string_name_new(godot_string_name *r_dest, const godot_string *p_name);
void  godot_string_name_new_data(godot_string_name *r_dest, const char *p_name);

godot_string  godot_string_name_get_name(const godot_string_name *p_self);

uint32_t  godot_string_name_get_hash(const godot_string_name *p_self);
const void  *godot_string_name_get_data_unique_pointer(const godot_string_name *p_self);

godot_bool  godot_string_name_operator_equal(const godot_string_name *p_self, const godot_string_name *p_other);
godot_bool  godot_string_name_operator_less(const godot_string_name *p_self, const godot_string_name *p_other);

void  godot_string_name_destroy(godot_string_name *p_self);


































































































































































































































































































































































































































































































void  godot_object_destroy(godot_object *p_o);



































godot_object  *godot_global_get_singleton(char *p_name);



typedef struct {
	uint8_t _dont_touch_that[1];
} godot_method_bind;

godot_method_bind  *godot_method_bind_get_method(const char *p_classname, const char *p_methodname);
void  godot_method_bind_ptrcall(godot_method_bind *p_method_bind, godot_object *p_instance, const void **p_args, void *p_ret);
godot_variant  godot_method_bind_call(godot_method_bind *p_method_bind, godot_object *p_instance, const godot_variant **p_args, const int p_arg_count, godot_variant_call_error *p_call_error);


typedef struct godot_gdnative_api_version {
	unsigned int major;
	unsigned int minor;
} godot_gdnative_api_version;

typedef struct godot_gdnative_api_struct godot_gdnative_api_struct;

struct godot_gdnative_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
};


typedef struct {
	godot_bool in_editor;
	uint64_t core_api_hash;
	uint64_t editor_api_hash;
	uint64_t no_api_hash;
	void (*report_version_mismatch)(const godot_object *p_library, const char *p_what, godot_gdnative_api_version p_want, godot_gdnative_api_version p_have);
	void (*report_loading_error)(const godot_object *p_library, const char *p_what);
	godot_object *gd_native_library;
	const struct godot_gdnative_core_api_struct *api_struct;
	const godot_string *active_library_path;
} godot_gdnative_init_options;

typedef struct {
	godot_bool in_editor;
} godot_gdnative_terminate_options;


typedef godot_object *(*godot_class_constructor)();

godot_class_constructor  godot_get_class_constructor(const char *p_classname);

godot_dictionary  godot_get_global_constants();


typedef void (*godot_gdnative_init_fn)(godot_gdnative_init_options *);
typedef void (*godot_gdnative_terminate_fn)(godot_gdnative_terminate_options *);
typedef godot_variant (*godot_gdnative_procedure_fn)(godot_array *);



typedef godot_variant (*native_call_cb)(void *, godot_array *);
void  godot_register_native_call_type(const char *p_call_type, native_call_cb p_callback);


void  *godot_alloc(int p_bytes);
void  *godot_realloc(void *p_ptr, int p_bytes);
void  godot_free(void *p_ptr);


void  godot_print_error(const char *p_description, const char *p_function, const char *p_file, int p_line);
void  godot_print_warning(const char *p_description, const char *p_function, const char *p_file, int p_line);
void  godot_print(const godot_string *p_message);



bool  godot_is_instance_valid(const godot_object *p_object);


void  *godot_get_class_tag(const godot_string_name *p_class);
godot_object  *godot_object_cast_to(const godot_object *p_object, void *p_class_tag);


godot_object  *godot_instance_from_id(godot_int p_instance_id);
































































void * godot_android_get_env();
void *  godot_android_get_activity();
void *  godot_android_get_surface();
bool  godot_android_is_activity_resumed();




































































typedef struct {
	godot_gdnative_api_version version;
	void *(*constructor)(godot_object *);
	void (*destructor)(void *);
	godot_string (*get_name)(const void *);
	godot_int (*get_capabilities)(const void *);
	godot_bool (*get_anchor_detection_is_enabled)(const void *);
	void (*set_anchor_detection_is_enabled)(void *, godot_bool);
	godot_bool (*is_stereo)(const void *);
	godot_bool (*is_initialized)(const void *);
	godot_bool (*initialize)(void *);
	void (*uninitialize)(void *);
	godot_vector2 (*get_render_targetsize)(const void *);
	godot_transform (*get_transform_for_eye)(void *, godot_int, godot_transform *);
	void (*fill_projection_for_eye)(void *, godot_real *, godot_int, godot_real, godot_real, godot_real);
	void (*commit_for_eye)(void *, godot_int, godot_rid *, godot_rect2 *);
	void (*process)(void *);

	godot_int (*get_external_texture_for_eye)(void *, godot_int);
	void (*notification)(void *, godot_int);
	godot_int (*get_camera_feed_id)(void *);

	godot_int (*get_external_depth_for_eye)(void *, godot_int);
} godot_arvr_interface_gdnative;

void  godot_arvr_register_interface(const godot_arvr_interface_gdnative *p_interface);


godot_real  godot_arvr_get_worldscale();
godot_transform  godot_arvr_get_reference_frame();


void  godot_arvr_blit(godot_int p_eye, godot_rid *p_render_target, godot_rect2 *p_rect);
godot_int  godot_arvr_get_texid(godot_rid *p_render_target);


godot_int  godot_arvr_add_controller(char *p_device_name, godot_int p_hand, godot_bool p_tracks_orientation, godot_bool p_tracks_position);
void  godot_arvr_remove_controller(godot_int p_controller_id);
void  godot_arvr_set_controller_transform(godot_int p_controller_id, godot_transform *p_transform, godot_bool p_tracks_orientation, godot_bool p_tracks_position);
void  godot_arvr_set_controller_button(godot_int p_controller_id, godot_int p_button, godot_bool p_is_pressed);
void  godot_arvr_set_controller_axis(godot_int p_controller_id, godot_int p_axis, godot_real p_value, godot_bool p_can_be_negative);
godot_real  godot_arvr_get_controller_rumble(godot_int p_controller_id);


void  godot_arvr_set_interface(godot_object *p_arvr_interface, const godot_arvr_interface_gdnative *p_gdn_interface);
godot_int  godot_arvr_get_depthid(godot_rid *p_render_target);































































typedef enum {
	GODOT_METHOD_RPC_MODE_DISABLED,
	GODOT_METHOD_RPC_MODE_REMOTE,
	GODOT_METHOD_RPC_MODE_MASTER,
	GODOT_METHOD_RPC_MODE_PUPPET,
	GODOT_METHOD_RPC_MODE_SLAVE = GODOT_METHOD_RPC_MODE_PUPPET,
	GODOT_METHOD_RPC_MODE_REMOTESYNC,
	GODOT_METHOD_RPC_MODE_SYNC = GODOT_METHOD_RPC_MODE_REMOTESYNC,
	GODOT_METHOD_RPC_MODE_MASTERSYNC,
	GODOT_METHOD_RPC_MODE_PUPPETSYNC,
} godot_method_rpc_mode;

typedef enum {
	GODOT_PROPERTY_HINT_NONE,
	GODOT_PROPERTY_HINT_RANGE,
	GODOT_PROPERTY_HINT_EXP_RANGE,
	GODOT_PROPERTY_HINT_ENUM,
	GODOT_PROPERTY_HINT_EXP_EASING,
	GODOT_PROPERTY_HINT_LENGTH,
	GODOT_PROPERTY_HINT_SPRITE_FRAME,
	GODOT_PROPERTY_HINT_KEY_ACCEL,
	GODOT_PROPERTY_HINT_FLAGS,
	GODOT_PROPERTY_HINT_LAYERS_2D_RENDER,
	GODOT_PROPERTY_HINT_LAYERS_2D_PHYSICS,
	GODOT_PROPERTY_HINT_LAYERS_3D_RENDER,
	GODOT_PROPERTY_HINT_LAYERS_3D_PHYSICS,
	GODOT_PROPERTY_HINT_FILE,
	GODOT_PROPERTY_HINT_DIR,
	GODOT_PROPERTY_HINT_GLOBAL_FILE,
	GODOT_PROPERTY_HINT_GLOBAL_DIR,
	GODOT_PROPERTY_HINT_RESOURCE_TYPE,
	GODOT_PROPERTY_HINT_MULTILINE_TEXT,
	GODOT_PROPERTY_HINT_PLACEHOLDER_TEXT,
	GODOT_PROPERTY_HINT_COLOR_NO_ALPHA,
	GODOT_PROPERTY_HINT_IMAGE_COMPRESS_LOSSY,
	GODOT_PROPERTY_HINT_IMAGE_COMPRESS_LOSSLESS,
	GODOT_PROPERTY_HINT_OBJECT_ID,
	GODOT_PROPERTY_HINT_TYPE_STRING,
	GODOT_PROPERTY_HINT_NODE_PATH_TO_EDITED_NODE,
	GODOT_PROPERTY_HINT_METHOD_OF_VARIANT_TYPE,
	GODOT_PROPERTY_HINT_METHOD_OF_BASE_TYPE,
	GODOT_PROPERTY_HINT_METHOD_OF_INSTANCE,
	GODOT_PROPERTY_HINT_METHOD_OF_SCRIPT,
	GODOT_PROPERTY_HINT_PROPERTY_OF_VARIANT_TYPE,
	GODOT_PROPERTY_HINT_PROPERTY_OF_BASE_TYPE,
	GODOT_PROPERTY_HINT_PROPERTY_OF_INSTANCE,
	GODOT_PROPERTY_HINT_PROPERTY_OF_SCRIPT,
	GODOT_PROPERTY_HINT_MAX,
} godot_property_hint;

typedef enum {

	GODOT_PROPERTY_USAGE_STORAGE = 1,
	GODOT_PROPERTY_USAGE_EDITOR = 2,
	GODOT_PROPERTY_USAGE_NETWORK = 4,
	GODOT_PROPERTY_USAGE_EDITOR_HELPER = 8,
	GODOT_PROPERTY_USAGE_CHECKABLE = 16,
	GODOT_PROPERTY_USAGE_CHECKED = 32,
	GODOT_PROPERTY_USAGE_INTERNATIONALIZED = 64,
	GODOT_PROPERTY_USAGE_GROUP = 128,
	GODOT_PROPERTY_USAGE_CATEGORY = 256,
	GODOT_PROPERTY_USAGE_STORE_IF_NONZERO = 512,
	GODOT_PROPERTY_USAGE_STORE_IF_NONONE = 1024,
	GODOT_PROPERTY_USAGE_NO_INSTANCE_STATE = 2048,
	GODOT_PROPERTY_USAGE_RESTART_IF_CHANGED = 4096,
	GODOT_PROPERTY_USAGE_SCRIPT_VARIABLE = 8192,
	GODOT_PROPERTY_USAGE_STORE_IF_NULL = 16384,
	GODOT_PROPERTY_USAGE_ANIMATE_AS_TRIGGER = 32768,
	GODOT_PROPERTY_USAGE_UPDATE_ALL_IF_MODIFIED = 65536,

	GODOT_PROPERTY_USAGE_DEFAULT = GODOT_PROPERTY_USAGE_STORAGE | GODOT_PROPERTY_USAGE_EDITOR | GODOT_PROPERTY_USAGE_NETWORK,
	GODOT_PROPERTY_USAGE_DEFAULT_INTL = GODOT_PROPERTY_USAGE_STORAGE | GODOT_PROPERTY_USAGE_EDITOR | GODOT_PROPERTY_USAGE_NETWORK | GODOT_PROPERTY_USAGE_INTERNATIONALIZED,
	GODOT_PROPERTY_USAGE_NOEDITOR = GODOT_PROPERTY_USAGE_STORAGE | GODOT_PROPERTY_USAGE_NETWORK,
} godot_property_usage_flags;

typedef struct {
	godot_method_rpc_mode rset_type;

	godot_int type;
	godot_property_hint hint;
	godot_string hint_string;
	godot_property_usage_flags usage;
	godot_variant default_value;
} godot_property_attributes;

typedef struct {

	 void *(*create_func)(godot_object *, void *);
	void *method_data;
	 void (*free_func)(void *);
} godot_instance_create_func;

typedef struct {

	 void (*destroy_func)(godot_object *, void *, void *);
	void *method_data;
	 void (*free_func)(void *);
} godot_instance_destroy_func;

void  godot_nativescript_register_class(void *p_gdnative_handle, const char *p_name, const char *p_base, godot_instance_create_func p_create_func, godot_instance_destroy_func p_destroy_func);

void  godot_nativescript_register_tool_class(void *p_gdnative_handle, const char *p_name, const char *p_base, godot_instance_create_func p_create_func, godot_instance_destroy_func p_destroy_func);

typedef struct {
	godot_method_rpc_mode rpc_type;
} godot_method_attributes;

typedef struct {

	 godot_variant (*method)(godot_object *, void *, void *, int, godot_variant **);
	void *method_data;
	 void (*free_func)(void *);
} godot_instance_method;

void  godot_nativescript_register_method(void *p_gdnative_handle, const char *p_name, const char *p_function_name, godot_method_attributes p_attr, godot_instance_method p_method);

typedef struct {

	 void (*set_func)(godot_object *, void *, void *, godot_variant *);
	void *method_data;
	 void (*free_func)(void *);
} godot_property_set_func;

typedef struct {

	 godot_variant (*get_func)(godot_object *, void *, void *);
	void *method_data;
	 void (*free_func)(void *);
} godot_property_get_func;

void  godot_nativescript_register_property(void *p_gdnative_handle, const char *p_name, const char *p_path, godot_property_attributes *p_attr, godot_property_set_func p_set_func, godot_property_get_func p_get_func);

typedef struct {
	godot_string name;
	godot_int type;
	godot_property_hint hint;
	godot_string hint_string;
	godot_property_usage_flags usage;
	godot_variant default_value;
} godot_signal_argument;

typedef struct {
	godot_string name;
	int num_args;
	godot_signal_argument *args;
	int num_default_args;
	godot_variant *default_args;
} godot_signal;

void  godot_nativescript_register_signal(void *p_gdnative_handle, const char *p_name, const godot_signal *p_signal);

void  *godot_nativescript_get_userdata(godot_object *p_instance);





typedef struct {
	godot_string name;

	godot_variant_type type;
	godot_property_hint hint;
	godot_string hint_string;
} godot_method_arg;

void  godot_nativescript_set_method_argument_information(void *p_gdnative_handle, const char *p_name, const char *p_function_name, int p_num_args, const godot_method_arg *p_args);



void  godot_nativescript_set_class_documentation(void *p_gdnative_handle, const char *p_name, godot_string p_documentation);
void  godot_nativescript_set_method_documentation(void *p_gdnative_handle, const char *p_name, const char *p_function_name, godot_string p_documentation);
void  godot_nativescript_set_property_documentation(void *p_gdnative_handle, const char *p_name, const char *p_path, godot_string p_documentation);
void  godot_nativescript_set_signal_documentation(void *p_gdnative_handle, const char *p_name, const char *p_signal_name, godot_string p_documentation);



void  godot_nativescript_set_global_type_tag(int p_idx, const char *p_name, const void *p_type_tag);
const void  *godot_nativescript_get_global_type_tag(int p_idx, const char *p_name);

void  godot_nativescript_set_type_tag(void *p_gdnative_handle, const char *p_name, const void *p_type_tag);
const void  *godot_nativescript_get_type_tag(const godot_object *p_object);



typedef struct {
	 void *(*alloc_instance_binding_data)(void *, const void *, godot_object *);
	 void (*free_instance_binding_data)(void *, void *);
	 void (*refcount_incremented_instance_binding)(void *, godot_object *);
	 bool (*refcount_decremented_instance_binding)(void *, godot_object *);
	void *data;
	 void (*free_func)(void *);
} godot_instance_binding_functions;

int  godot_nativescript_register_instance_binding_data_functions(godot_instance_binding_functions p_binding_functions);
void  godot_nativescript_unregister_instance_binding_data_functions(int p_idx);

void  *godot_nativescript_get_instance_binding_data(int p_idx, godot_object *p_object);

void  godot_nativescript_profiling_add_data(const char *p_signature, uint64_t p_time);




































































typedef struct {

	godot_gdnative_api_version version;
	godot_object *data;


	godot_error (*get_data)(void *user, uint8_t *p_buffer, int p_bytes);
	godot_error (*get_partial_data)(void *user, uint8_t *p_buffer, int p_bytes, int *r_received);
	godot_error (*put_data)(void *user, const uint8_t *p_data, int p_bytes);
	godot_error (*put_partial_data)(void *user, const uint8_t *p_data, int p_bytes, int *r_sent);

	int (*get_available_bytes)(const void *user);

	void *next;
} godot_net_stream_peer;


void godot_net_bind_stream_peer(godot_object *p_obj, const godot_net_stream_peer *p_interface);

typedef struct {
	godot_gdnative_api_version version;

	godot_object *data;


	godot_error (*get_packet)(void *, const uint8_t **, int *);
	godot_error (*put_packet)(void *, const uint8_t *, int);
	godot_int (*get_available_packet_count)(const void *);
	godot_int (*get_max_packet_size)(const void *);

	void *next;
} godot_net_packet_peer;


void  godot_net_bind_packet_peer(godot_object *p_obj, const godot_net_packet_peer *);

typedef struct {
	godot_gdnative_api_version version;

	godot_object *data;


	godot_error (*get_packet)(void *, const uint8_t **, int *);
	godot_error (*put_packet)(void *, const uint8_t *, int);
	godot_int (*get_available_packet_count)(const void *);
	godot_int (*get_max_packet_size)(const void *);


	void (*set_transfer_mode)(void *, godot_int);
	godot_int (*get_transfer_mode)(const void *);

	void (*set_target_peer)(void *, godot_int);
	godot_int (*get_packet_peer)(const void *);
	godot_bool (*is_server)(const void *);
	void (*poll)(void *);

	int32_t (*get_unique_id)(const void *);
	void (*set_refuse_new_connections)(void *, godot_bool);
	godot_bool (*is_refusing_new_connections)(const void *);
	godot_int (*get_connection_status)(const void *);

	void *next;
} godot_net_multiplayer_peer;


void  godot_net_bind_multiplayer_peer(godot_object *p_obj, const godot_net_multiplayer_peer *);


































































typedef struct {
	godot_gdnative_api_version version;


	void (*unregistered)();



	godot_error (*create_peer_connection)(godot_object *);

	void *next;
} godot_net_webrtc_library;


typedef struct {
	godot_gdnative_api_version version;

	godot_object *data;


	godot_int (*get_connection_state)(const void *);

	godot_error (*initialize)(void *, const godot_dictionary *);
	godot_object *(*create_data_channel)(void *, const char *p_channel_name, const godot_dictionary *);
	godot_error (*create_offer)(void *);
	godot_error (*create_answer)(void *);
	godot_error (*set_remote_description)(void *, const char *, const char *);
	godot_error (*set_local_description)(void *, const char *, const char *);
	godot_error (*add_ice_candidate)(void *, const char *, int, const char *);
	godot_error (*poll)(void *);
	void (*close)(void *);

	void *next;
} godot_net_webrtc_peer_connection;


typedef struct {
	godot_gdnative_api_version version;

	godot_object *data;


	godot_error (*get_packet)(void *, const uint8_t **, int *);
	godot_error (*put_packet)(void *, const uint8_t *, int);
	godot_int (*get_available_packet_count)(const void *);
	godot_int (*get_max_packet_size)(const void *);


	void (*set_write_mode)(void *, godot_int);
	godot_int (*get_write_mode)(const void *);
	bool (*was_string_packet)(const void *);

	godot_int (*get_ready_state)(const void *);
	const char *(*get_label)(const void *);
	bool (*is_ordered)(const void *);
	int (*get_id)(const void *);
	int (*get_max_packet_life_time)(const void *);
	int (*get_max_retransmits)(const void *);
	const char *(*get_protocol)(const void *);
	bool (*is_negotiated)(const void *);

	godot_error (*poll)(void *);
	void (*close)(void *);

	void *next;
} godot_net_webrtc_data_channel;


godot_error  godot_net_set_webrtc_library(const godot_net_webrtc_library *);

void  godot_net_bind_webrtc_peer_connection(godot_object *p_obj, const godot_net_webrtc_peer_connection *);

void  godot_net_bind_webrtc_data_channel(godot_object *p_obj, const godot_net_webrtc_data_channel *);





























































































typedef void godot_pluginscript_instance_data;
typedef void godot_pluginscript_script_data;
typedef void godot_pluginscript_language_data;




typedef struct {
	godot_pluginscript_instance_data *(*init)(godot_pluginscript_script_data *p_data, godot_object *p_owner);
	void (*finish)(godot_pluginscript_instance_data *p_data);

	godot_bool (*set_prop)(godot_pluginscript_instance_data *p_data, const godot_string *p_name, const godot_variant *p_value);
	godot_bool (*get_prop)(godot_pluginscript_instance_data *p_data, const godot_string *p_name, godot_variant *r_ret);

	godot_variant (*call_method)(godot_pluginscript_instance_data *p_data,
			const godot_string_name *p_method, const godot_variant **p_args,
			int p_argcount, godot_variant_call_error *r_error);

	void (*notification)(godot_pluginscript_instance_data *p_data, int p_notification);

	godot_method_rpc_mode (*get_rpc_mode)(godot_pluginscript_instance_data *p_data, const godot_string *p_method);
	godot_method_rpc_mode (*get_rset_mode)(godot_pluginscript_instance_data *p_data, const godot_string *p_variable);





	void (*refcount_incremented)(godot_pluginscript_instance_data *p_data);
	bool (*refcount_decremented)(godot_pluginscript_instance_data *p_data);
} godot_pluginscript_instance_desc;



typedef struct {
	godot_pluginscript_script_data *data;
	godot_string_name name;
	godot_bool is_tool;
	godot_string_name base;


	godot_dictionary member_lines;









	godot_array methods;

	godot_array signals;










	godot_array properties;
} godot_pluginscript_script_manifest;

typedef struct {
	godot_pluginscript_script_manifest (*init)(godot_pluginscript_language_data *p_data, const godot_string *p_path, const godot_string *p_source, godot_error *r_error);
	void (*finish)(godot_pluginscript_script_data *p_data);
	godot_pluginscript_instance_desc instance_desc;
} godot_pluginscript_script_desc;



typedef struct {
	godot_string_name signature;
	godot_int call_count;
	godot_int total_time;
	godot_int self_time;
} godot_pluginscript_profiling_data;

typedef struct {
	const char *name;
	const char *type;
	const char *extension;
	const char **recognized_extensions;
	godot_pluginscript_language_data *(*init)();
	void (*finish)(godot_pluginscript_language_data *p_data);
	const char **reserved_words;
	const char **comment_delimiters;
	const char **string_delimiters;
	godot_bool has_named_classes;
	godot_bool supports_builtin_mode;

	godot_string (*get_template_source_code)(godot_pluginscript_language_data *p_data, const godot_string *p_class_name, const godot_string *p_base_class_name);
	godot_bool (*validate)(godot_pluginscript_language_data *p_data, const godot_string *p_script, int *r_line_error, int *r_col_error, godot_string *r_test_error, const godot_string *p_path, godot_pool_string_array *r_functions);
	int (*find_function)(godot_pluginscript_language_data *p_data, const godot_string *p_function, const godot_string *p_code);
	godot_string (*make_function)(godot_pluginscript_language_data *p_data, const godot_string *p_class, const godot_string *p_name, const godot_pool_string_array *p_args);
	godot_error (*complete_code)(godot_pluginscript_language_data *p_data, const godot_string *p_code, const godot_string *p_path, godot_object *p_owner, godot_array *r_options, godot_bool *r_force, godot_string *r_call_hint);
	void (*auto_indent_code)(godot_pluginscript_language_data *p_data, godot_string *p_code, int p_from_line, int p_to_line);

	void (*add_global_constant)(godot_pluginscript_language_data *p_data, const godot_string *p_variable, const godot_variant *p_value);
	godot_string (*debug_get_error)(godot_pluginscript_language_data *p_data);
	int (*debug_get_stack_level_count)(godot_pluginscript_language_data *p_data);
	int (*debug_get_stack_level_line)(godot_pluginscript_language_data *p_data, int p_level);
	godot_string (*debug_get_stack_level_function)(godot_pluginscript_language_data *p_data, int p_level);
	godot_string (*debug_get_stack_level_source)(godot_pluginscript_language_data *p_data, int p_level);
	void (*debug_get_stack_level_locals)(godot_pluginscript_language_data *p_data, int p_level, godot_pool_string_array *p_locals, godot_array *p_values, int p_max_subitems, int p_max_depth);
	void (*debug_get_stack_level_members)(godot_pluginscript_language_data *p_data, int p_level, godot_pool_string_array *p_members, godot_array *p_values, int p_max_subitems, int p_max_depth);
	void (*debug_get_globals)(godot_pluginscript_language_data *p_data, godot_pool_string_array *p_locals, godot_array *p_values, int p_max_subitems, int p_max_depth);
	godot_string (*debug_parse_stack_level_expression)(godot_pluginscript_language_data *p_data, int p_level, const godot_string *p_expression, int p_max_subitems, int p_max_depth);


	void (*get_public_functions)(godot_pluginscript_language_data *p_data, godot_array *r_functions);
	void (*get_public_constants)(godot_pluginscript_language_data *p_data, godot_dictionary *r_constants);

	void (*profiling_start)(godot_pluginscript_language_data *p_data);
	void (*profiling_stop)(godot_pluginscript_language_data *p_data);
	int (*profiling_get_accumulated_data)(godot_pluginscript_language_data *p_data, godot_pluginscript_profiling_data *r_info, int p_info_max);
	int (*profiling_get_frame_data)(godot_pluginscript_language_data *p_data, godot_pluginscript_profiling_data *r_info, int p_info_max);
	void (*profiling_frame)(godot_pluginscript_language_data *p_data);

	godot_pluginscript_script_desc script_desc;
} godot_pluginscript_language_desc;

void  godot_pluginscript_register_language(const godot_pluginscript_language_desc *language_desc);
































































typedef struct
{
	godot_gdnative_api_version version;
	void *next;
	void *(*constructor)(godot_object *);
	void (*destructor)(void *);
	const char *(*get_plugin_name)(void);
	const char **(*get_supported_extensions)(int *count);
	godot_bool (*open_file)(void *, void *);
	godot_real (*get_length)(const void *);
	godot_real (*get_playback_position)(const void *);
	void (*seek)(void *, godot_real);
	void (*set_audio_track)(void *, godot_int);
	void (*update)(void *, godot_real);
	godot_pool_byte_array *(*get_videoframe)(void *);
	godot_int (*get_audioframe)(void *, float *, int);
	godot_int (*get_channels)(const void *);
	godot_int (*get_mix_rate)(const void *);
	godot_vector2 (*get_texture_size)(const void *);
} godot_videodecoder_interface_gdnative;

typedef int (*GDNativeAudioMixCallback)(void *, const float *, int);


godot_int  godot_videodecoder_file_read(void *file_ptr, uint8_t *buf, int buf_size);
int64_t  godot_videodecoder_file_seek(void *file_ptr, int64_t pos, int whence);
void  godot_videodecoder_register_decoder(const godot_videodecoder_interface_gdnative *p_interface);





enum GDNATIVE_API_TYPES {
	GDNATIVE_CORE,
	GDNATIVE_EXT_NATIVESCRIPT,
	GDNATIVE_EXT_PLUGINSCRIPT,
	GDNATIVE_EXT_ANDROID,
	GDNATIVE_EXT_ARVR,
	GDNATIVE_EXT_VIDEODECODER,
	GDNATIVE_EXT_NET,
};

typedef struct godot_gdnative_ext_nativescript_1_1_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	void (*godot_nativescript_set_method_argument_information)(void *p_gdnative_handle, const char *p_name, const char *p_function_name, int p_num_args, const godot_method_arg *p_args);
	void (*godot_nativescript_set_class_documentation)(void *p_gdnative_handle, const char *p_name, godot_string p_documentation);
	void (*godot_nativescript_set_method_documentation)(void *p_gdnative_handle, const char *p_name, const char *p_function_name, godot_string p_documentation);
	void (*godot_nativescript_set_property_documentation)(void *p_gdnative_handle, const char *p_name, const char *p_path, godot_string p_documentation);
	void (*godot_nativescript_set_signal_documentation)(void *p_gdnative_handle, const char *p_name, const char *p_signal_name, godot_string p_documentation);
	void (*godot_nativescript_set_global_type_tag)(int p_idx, const char *p_name, const void *p_type_tag);
	const void *(*godot_nativescript_get_global_type_tag)(int p_idx, const char *p_name);
	void (*godot_nativescript_set_type_tag)(void *p_gdnative_handle, const char *p_name, const void *p_type_tag);
	const void *(*godot_nativescript_get_type_tag)(const godot_object *p_object);
	int (*godot_nativescript_register_instance_binding_data_functions)(godot_instance_binding_functions p_binding_functions);
	void (*godot_nativescript_unregister_instance_binding_data_functions)(int p_idx);
	void *(*godot_nativescript_get_instance_binding_data)(int p_idx, godot_object *p_object);
	void (*godot_nativescript_profiling_add_data)(const char *p_signature, uint64_t p_line);
} godot_gdnative_ext_nativescript_1_1_api_struct;

typedef struct godot_gdnative_ext_nativescript_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	void (*godot_nativescript_register_class)(void *p_gdnative_handle, const char *p_name, const char *p_base, godot_instance_create_func p_create_func, godot_instance_destroy_func p_destroy_func);
	void (*godot_nativescript_register_tool_class)(void *p_gdnative_handle, const char *p_name, const char *p_base, godot_instance_create_func p_create_func, godot_instance_destroy_func p_destroy_func);
	void (*godot_nativescript_register_method)(void *p_gdnative_handle, const char *p_name, const char *p_function_name, godot_method_attributes p_attr, godot_instance_method p_method);
	void (*godot_nativescript_register_property)(void *p_gdnative_handle, const char *p_name, const char *p_path, godot_property_attributes *p_attr, godot_property_set_func p_set_func, godot_property_get_func p_get_func);
	void (*godot_nativescript_register_signal)(void *p_gdnative_handle, const char *p_name, const godot_signal *p_signal);
	void *(*godot_nativescript_get_userdata)(godot_object *p_instance);
} godot_gdnative_ext_nativescript_api_struct;

typedef struct godot_gdnative_ext_pluginscript_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	void (*godot_pluginscript_register_language)(const godot_pluginscript_language_desc *language_desc);
} godot_gdnative_ext_pluginscript_api_struct;

typedef struct godot_gdnative_ext_android_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	void*(*godot_android_get_env)();
	void * (*godot_android_get_activity)();
	void * (*godot_android_get_surface)();
	bool (*godot_android_is_activity_resumed)();
} godot_gdnative_ext_android_api_struct;

typedef struct godot_gdnative_ext_arvr_1_2_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	void (*godot_arvr_set_interface)(godot_object *p_arvr_interface, const godot_arvr_interface_gdnative *p_gdn_interface);
	godot_int (*godot_arvr_get_depthid)(godot_rid *p_render_target);
} godot_gdnative_ext_arvr_1_2_api_struct;

typedef struct godot_gdnative_ext_arvr_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	void (*godot_arvr_register_interface)(const godot_arvr_interface_gdnative *p_interface);
	godot_real (*godot_arvr_get_worldscale)();
	godot_transform (*godot_arvr_get_reference_frame)();
	void (*godot_arvr_blit)(int p_eye, godot_rid *p_render_target, godot_rect2 *p_screen_rect);
	godot_int (*godot_arvr_get_texid)(godot_rid *p_render_target);
	godot_int (*godot_arvr_add_controller)(char *p_device_name, godot_int p_hand, godot_bool p_tracks_orientation, godot_bool p_tracks_position);
	void (*godot_arvr_remove_controller)(godot_int p_controller_id);
	void (*godot_arvr_set_controller_transform)(godot_int p_controller_id, godot_transform *p_transform, godot_bool p_tracks_orientation, godot_bool p_tracks_position);
	void (*godot_arvr_set_controller_button)(godot_int p_controller_id, godot_int p_button, godot_bool p_is_pressed);
	void (*godot_arvr_set_controller_axis)(godot_int p_controller_id, godot_int p_exis, godot_real p_value, godot_bool p_can_be_negative);
	godot_real (*godot_arvr_get_controller_rumble)(godot_int p_controller_id);
} godot_gdnative_ext_arvr_api_struct;

typedef struct godot_gdnative_ext_videodecoder_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	godot_int (*godot_videodecoder_file_read)(void *file_ptr, uint8_t *buf, int buf_size);
	int64_t (*godot_videodecoder_file_seek)(void *file_ptr, int64_t pos, int whence);
	void (*godot_videodecoder_register_decoder)(const godot_videodecoder_interface_gdnative *p_interface);
} godot_gdnative_ext_videodecoder_api_struct;

typedef struct godot_gdnative_ext_net_3_2_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	godot_error (*godot_net_set_webrtc_library)(const godot_net_webrtc_library *p_library);
	void (*godot_net_bind_webrtc_peer_connection)(godot_object *p_obj, const godot_net_webrtc_peer_connection *p_interface);
	void (*godot_net_bind_webrtc_data_channel)(godot_object *p_obj, const godot_net_webrtc_data_channel *p_interface);
} godot_gdnative_ext_net_3_2_api_struct;

typedef struct godot_gdnative_ext_net_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	void (*godot_net_bind_stream_peer)(godot_object *p_obj, const godot_net_stream_peer *p_interface);
	void (*godot_net_bind_packet_peer)(godot_object *p_obj, const godot_net_packet_peer *p_interface);
	void (*godot_net_bind_multiplayer_peer)(godot_object *p_obj, const godot_net_multiplayer_peer *p_interface);
} godot_gdnative_ext_net_api_struct;

typedef struct godot_gdnative_core_1_2_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	godot_dictionary (*godot_dictionary_duplicate)(const godot_dictionary *p_self, const godot_bool p_deep);
	godot_vector3 (*godot_vector3_move_toward)(const godot_vector3 *p_self, const godot_vector3 *p_to, const godot_real p_delta);
	godot_vector2 (*godot_vector2_move_toward)(const godot_vector2 *p_self, const godot_vector2 *p_to, const godot_real p_delta);
	godot_int (*godot_string_count)(const godot_string *p_self, godot_string p_what, godot_int p_from, godot_int p_to);
	godot_int (*godot_string_countn)(const godot_string *p_self, godot_string p_what, godot_int p_from, godot_int p_to);
	godot_vector3 (*godot_vector3_direction_to)(const godot_vector3 *p_self, const godot_vector3 *p_to);
	godot_vector2 (*godot_vector2_direction_to)(const godot_vector2 *p_self, const godot_vector2 *p_to);
	godot_array (*godot_array_slice)(const godot_array *p_self, const godot_int p_begin, const godot_int p_end, const godot_int p_step, const godot_bool p_deep);
	godot_bool (*godot_pool_byte_array_empty)(const godot_pool_byte_array *p_self);
	godot_bool (*godot_pool_int_array_empty)(const godot_pool_int_array *p_self);
	godot_bool (*godot_pool_real_array_empty)(const godot_pool_real_array *p_self);
	godot_bool (*godot_pool_string_array_empty)(const godot_pool_string_array *p_self);
	godot_bool (*godot_pool_vector2_array_empty)(const godot_pool_vector2_array *p_self);
	godot_bool (*godot_pool_vector3_array_empty)(const godot_pool_vector3_array *p_self);
	godot_bool (*godot_pool_color_array_empty)(const godot_pool_color_array *p_self);
	void *(*godot_get_class_tag)(const godot_string_name *p_class);
	godot_object *(*godot_object_cast_to)(const godot_object *p_object, void *p_class_tag);
	godot_object *(*godot_instance_from_id)(godot_int p_instance_id);
} godot_gdnative_core_1_2_api_struct;

typedef struct godot_gdnative_core_1_1_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	godot_int (*godot_color_to_abgr32)(const godot_color *p_self);
	godot_int (*godot_color_to_abgr64)(const godot_color *p_self);
	godot_int (*godot_color_to_argb64)(const godot_color *p_self);
	godot_int (*godot_color_to_rgba64)(const godot_color *p_self);
	godot_color (*godot_color_darkened)(const godot_color *p_self, const godot_real p_amount);
	godot_color (*godot_color_from_hsv)(const godot_color *p_self, const godot_real p_h, const godot_real p_s, const godot_real p_v, const godot_real p_a);
	godot_color (*godot_color_lightened)(const godot_color *p_self, const godot_real p_amount);
	godot_array (*godot_array_duplicate)(const godot_array *p_self, const godot_bool p_deep);
	godot_variant (*godot_array_max)(const godot_array *p_self);
	godot_variant (*godot_array_min)(const godot_array *p_self);
	void (*godot_array_shuffle)(godot_array *p_self);
	godot_basis (*godot_basis_slerp)(const godot_basis *p_self, const godot_basis *p_b, const godot_real p_t);
	godot_variant (*godot_dictionary_get_with_default)(const godot_dictionary *p_self, const godot_variant *p_key, const godot_variant *p_default);
	bool (*godot_dictionary_erase_with_return)(godot_dictionary *p_self, const godot_variant *p_key);
	godot_node_path (*godot_node_path_get_as_property_path)(const godot_node_path *p_self);
	void (*godot_quat_set_axis_angle)(godot_quat *p_self, const godot_vector3 *p_axis, const godot_real p_angle);
	godot_rect2 (*godot_rect2_grow_individual)(const godot_rect2 *p_self, const godot_real p_left, const godot_real p_top, const godot_real p_right, const godot_real p_bottom);
	godot_rect2 (*godot_rect2_grow_margin)(const godot_rect2 *p_self, const godot_int p_margin, const godot_real p_by);
	godot_rect2 (*godot_rect2_abs)(const godot_rect2 *p_self);
	godot_string (*godot_string_dedent)(const godot_string *p_self);
	godot_string (*godot_string_trim_prefix)(const godot_string *p_self, const godot_string *p_prefix);
	godot_string (*godot_string_trim_suffix)(const godot_string *p_self, const godot_string *p_suffix);
	godot_string (*godot_string_rstrip)(const godot_string *p_self, const godot_string *p_chars);
	godot_pool_string_array (*godot_string_rsplit)(const godot_string *p_self, const godot_string *p_divisor, const godot_bool p_allow_empty, const godot_int p_maxsplit);
	godot_quat (*godot_basis_get_quat)(const godot_basis *p_self);
	void (*godot_basis_set_quat)(godot_basis *p_self, const godot_quat *p_quat);
	void (*godot_basis_set_axis_angle_scale)(godot_basis *p_self, const godot_vector3 *p_axis, godot_real p_phi, const godot_vector3 *p_scale);
	void (*godot_basis_set_euler_scale)(godot_basis *p_self, const godot_vector3 *p_euler, const godot_vector3 *p_scale);
	void (*godot_basis_set_quat_scale)(godot_basis *p_self, const godot_quat *p_quat, const godot_vector3 *p_scale);
	bool (*godot_is_instance_valid)(const godot_object *p_object);
	void (*godot_quat_new_with_basis)(godot_quat *r_dest, const godot_basis *p_basis);
	void (*godot_quat_new_with_euler)(godot_quat *r_dest, const godot_vector3 *p_euler);
	void (*godot_transform_new_with_quat)(godot_transform *r_dest, const godot_quat *p_quat);
	godot_string (*godot_variant_get_operator_name)(godot_variant_operator p_op);
	void (*godot_variant_evaluate)(godot_variant_operator p_op, const godot_variant *p_a, const godot_variant *p_b, godot_variant *r_ret, godot_bool *r_valid);
} godot_gdnative_core_1_1_api_struct;

typedef struct godot_gdnative_core_api_struct {
	unsigned int type;
	godot_gdnative_api_version version;
	const godot_gdnative_api_struct *next;
	unsigned int num_extensions;
	const godot_gdnative_api_struct **extensions;
	void (*godot_color_new_rgba)(godot_color *r_dest, const godot_real p_r, const godot_real p_g, const godot_real p_b, const godot_real p_a);
	void (*godot_color_new_rgb)(godot_color *r_dest, const godot_real p_r, const godot_real p_g, const godot_real p_b);
	godot_real (*godot_color_get_r)(const godot_color *p_self);
	void (*godot_color_set_r)(godot_color *p_self, const godot_real r);
	godot_real (*godot_color_get_g)(const godot_color *p_self);
	void (*godot_color_set_g)(godot_color *p_self, const godot_real g);
	godot_real (*godot_color_get_b)(const godot_color *p_self);
	void (*godot_color_set_b)(godot_color *p_self, const godot_real b);
	godot_real (*godot_color_get_a)(const godot_color *p_self);
	void (*godot_color_set_a)(godot_color *p_self, const godot_real a);
	godot_real (*godot_color_get_h)(const godot_color *p_self);
	godot_real (*godot_color_get_s)(const godot_color *p_self);
	godot_real (*godot_color_get_v)(const godot_color *p_self);
	godot_string (*godot_color_as_string)(const godot_color *p_self);
	godot_int (*godot_color_to_rgba32)(const godot_color *p_self);
	godot_int (*godot_color_to_argb32)(const godot_color *p_self);
	godot_real (*godot_color_gray)(const godot_color *p_self);
	godot_color (*godot_color_inverted)(const godot_color *p_self);
	godot_color (*godot_color_contrasted)(const godot_color *p_self);
	godot_color (*godot_color_linear_interpolate)(const godot_color *p_self, const godot_color *p_b, const godot_real p_t);
	godot_color (*godot_color_blend)(const godot_color *p_self, const godot_color *p_over);
	godot_string (*godot_color_to_html)(const godot_color *p_self, const godot_bool p_with_alpha);
	godot_bool (*godot_color_operator_equal)(const godot_color *p_self, const godot_color *p_b);
	godot_bool (*godot_color_operator_less)(const godot_color *p_self, const godot_color *p_b);
	void (*godot_vector2_new)(godot_vector2 *r_dest, const godot_real p_x, const godot_real p_y);
	godot_string (*godot_vector2_as_string)(const godot_vector2 *p_self);
	godot_vector2 (*godot_vector2_normalized)(const godot_vector2 *p_self);
	godot_real (*godot_vector2_length)(const godot_vector2 *p_self);
	godot_real (*godot_vector2_angle)(const godot_vector2 *p_self);
	godot_real (*godot_vector2_length_squared)(const godot_vector2 *p_self);
	godot_bool (*godot_vector2_is_normalized)(const godot_vector2 *p_self);
	godot_real (*godot_vector2_distance_to)(const godot_vector2 *p_self, const godot_vector2 *p_to);
	godot_real (*godot_vector2_distance_squared_to)(const godot_vector2 *p_self, const godot_vector2 *p_to);
	godot_real (*godot_vector2_angle_to)(const godot_vector2 *p_self, const godot_vector2 *p_to);
	godot_real (*godot_vector2_angle_to_point)(const godot_vector2 *p_self, const godot_vector2 *p_to);
	godot_vector2 (*godot_vector2_linear_interpolate)(const godot_vector2 *p_self, const godot_vector2 *p_b, const godot_real p_t);
	godot_vector2 (*godot_vector2_cubic_interpolate)(const godot_vector2 *p_self, const godot_vector2 *p_b, const godot_vector2 *p_pre_a, const godot_vector2 *p_post_b, const godot_real p_t);
	godot_vector2 (*godot_vector2_rotated)(const godot_vector2 *p_self, const godot_real p_phi);
	godot_vector2 (*godot_vector2_tangent)(const godot_vector2 *p_self);
	godot_vector2 (*godot_vector2_floor)(const godot_vector2 *p_self);
	godot_vector2 (*godot_vector2_snapped)(const godot_vector2 *p_self, const godot_vector2 *p_by);
	godot_real (*godot_vector2_aspect)(const godot_vector2 *p_self);
	godot_real (*godot_vector2_dot)(const godot_vector2 *p_self, const godot_vector2 *p_with);
	godot_vector2 (*godot_vector2_slide)(const godot_vector2 *p_self, const godot_vector2 *p_n);
	godot_vector2 (*godot_vector2_bounce)(const godot_vector2 *p_self, const godot_vector2 *p_n);
	godot_vector2 (*godot_vector2_reflect)(const godot_vector2 *p_self, const godot_vector2 *p_n);
	godot_vector2 (*godot_vector2_abs)(const godot_vector2 *p_self);
	godot_vector2 (*godot_vector2_clamped)(const godot_vector2 *p_self, const godot_real p_length);
	godot_vector2 (*godot_vector2_operator_add)(const godot_vector2 *p_self, const godot_vector2 *p_b);
	godot_vector2 (*godot_vector2_operator_subtract)(const godot_vector2 *p_self, const godot_vector2 *p_b);
	godot_vector2 (*godot_vector2_operator_multiply_vector)(const godot_vector2 *p_self, const godot_vector2 *p_b);
	godot_vector2 (*godot_vector2_operator_multiply_scalar)(const godot_vector2 *p_self, const godot_real p_b);
	godot_vector2 (*godot_vector2_operator_divide_vector)(const godot_vector2 *p_self, const godot_vector2 *p_b);
	godot_vector2 (*godot_vector2_operator_divide_scalar)(const godot_vector2 *p_self, const godot_real p_b);
	godot_bool (*godot_vector2_operator_equal)(const godot_vector2 *p_self, const godot_vector2 *p_b);
	godot_bool (*godot_vector2_operator_less)(const godot_vector2 *p_self, const godot_vector2 *p_b);
	godot_vector2 (*godot_vector2_operator_neg)(const godot_vector2 *p_self);
	void (*godot_vector2_set_x)(godot_vector2 *p_self, const godot_real p_x);
	void (*godot_vector2_set_y)(godot_vector2 *p_self, const godot_real p_y);
	godot_real (*godot_vector2_get_x)(const godot_vector2 *p_self);
	godot_real (*godot_vector2_get_y)(const godot_vector2 *p_self);
	void (*godot_quat_new)(godot_quat *r_dest, const godot_real p_x, const godot_real p_y, const godot_real p_z, const godot_real p_w);
	void (*godot_quat_new_with_axis_angle)(godot_quat *r_dest, const godot_vector3 *p_axis, const godot_real p_angle);
	godot_real (*godot_quat_get_x)(const godot_quat *p_self);
	void (*godot_quat_set_x)(godot_quat *p_self, const godot_real val);
	godot_real (*godot_quat_get_y)(const godot_quat *p_self);
	void (*godot_quat_set_y)(godot_quat *p_self, const godot_real val);
	godot_real (*godot_quat_get_z)(const godot_quat *p_self);
	void (*godot_quat_set_z)(godot_quat *p_self, const godot_real val);
	godot_real (*godot_quat_get_w)(const godot_quat *p_self);
	void (*godot_quat_set_w)(godot_quat *p_self, const godot_real val);
	godot_string (*godot_quat_as_string)(const godot_quat *p_self);
	godot_real (*godot_quat_length)(const godot_quat *p_self);
	godot_real (*godot_quat_length_squared)(const godot_quat *p_self);
	godot_quat (*godot_quat_normalized)(const godot_quat *p_self);
	godot_bool (*godot_quat_is_normalized)(const godot_quat *p_self);
	godot_quat (*godot_quat_inverse)(const godot_quat *p_self);
	godot_real (*godot_quat_dot)(const godot_quat *p_self, const godot_quat *p_b);
	godot_vector3 (*godot_quat_xform)(const godot_quat *p_self, const godot_vector3 *p_v);
	godot_quat (*godot_quat_slerp)(const godot_quat *p_self, const godot_quat *p_b, const godot_real p_t);
	godot_quat (*godot_quat_slerpni)(const godot_quat *p_self, const godot_quat *p_b, const godot_real p_t);
	godot_quat (*godot_quat_cubic_slerp)(const godot_quat *p_self, const godot_quat *p_b, const godot_quat *p_pre_a, const godot_quat *p_post_b, const godot_real p_t);
	godot_quat (*godot_quat_operator_multiply)(const godot_quat *p_self, const godot_real p_b);
	godot_quat (*godot_quat_operator_add)(const godot_quat *p_self, const godot_quat *p_b);
	godot_quat (*godot_quat_operator_subtract)(const godot_quat *p_self, const godot_quat *p_b);
	godot_quat (*godot_quat_operator_divide)(const godot_quat *p_self, const godot_real p_b);
	godot_bool (*godot_quat_operator_equal)(const godot_quat *p_self, const godot_quat *p_b);
	godot_quat (*godot_quat_operator_neg)(const godot_quat *p_self);
	void (*godot_basis_new_with_rows)(godot_basis *r_dest, const godot_vector3 *p_x_axis, const godot_vector3 *p_y_axis, const godot_vector3 *p_z_axis);
	void (*godot_basis_new_with_axis_and_angle)(godot_basis *r_dest, const godot_vector3 *p_axis, const godot_real p_phi);
	void (*godot_basis_new_with_euler)(godot_basis *r_dest, const godot_vector3 *p_euler);
	godot_string (*godot_basis_as_string)(const godot_basis *p_self);
	godot_basis (*godot_basis_inverse)(const godot_basis *p_self);
	godot_basis (*godot_basis_transposed)(const godot_basis *p_self);
	godot_basis (*godot_basis_orthonormalized)(const godot_basis *p_self);
	godot_real (*godot_basis_determinant)(const godot_basis *p_self);
	godot_basis (*godot_basis_rotated)(const godot_basis *p_self, const godot_vector3 *p_axis, const godot_real p_phi);
	godot_basis (*godot_basis_scaled)(const godot_basis *p_self, const godot_vector3 *p_scale);
	godot_vector3 (*godot_basis_get_scale)(const godot_basis *p_self);
	godot_vector3 (*godot_basis_get_euler)(const godot_basis *p_self);
	godot_real (*godot_basis_tdotx)(const godot_basis *p_self, const godot_vector3 *p_with);
	godot_real (*godot_basis_tdoty)(const godot_basis *p_self, const godot_vector3 *p_with);
	godot_real (*godot_basis_tdotz)(const godot_basis *p_self, const godot_vector3 *p_with);
	godot_vector3 (*godot_basis_xform)(const godot_basis *p_self, const godot_vector3 *p_v);
	godot_vector3 (*godot_basis_xform_inv)(const godot_basis *p_self, const godot_vector3 *p_v);
	godot_int (*godot_basis_get_orthogonal_index)(const godot_basis *p_self);
	void (*godot_basis_new)(godot_basis *r_dest);
	void (*godot_basis_new_with_euler_quat)(godot_basis *r_dest, const godot_quat *p_euler);
	void (*godot_basis_get_elements)(const godot_basis *p_self, godot_vector3 *p_elements);
	godot_vector3 (*godot_basis_get_axis)(const godot_basis *p_self, const godot_int p_axis);
	void (*godot_basis_set_axis)(godot_basis *p_self, const godot_int p_axis, const godot_vector3 *p_value);
	godot_vector3 (*godot_basis_get_row)(const godot_basis *p_self, const godot_int p_row);
	void (*godot_basis_set_row)(godot_basis *p_self, const godot_int p_row, const godot_vector3 *p_value);
	godot_bool (*godot_basis_operator_equal)(const godot_basis *p_self, const godot_basis *p_b);
	godot_basis (*godot_basis_operator_add)(const godot_basis *p_self, const godot_basis *p_b);
	godot_basis (*godot_basis_operator_subtract)(const godot_basis *p_self, const godot_basis *p_b);
	godot_basis (*godot_basis_operator_multiply_vector)(const godot_basis *p_self, const godot_basis *p_b);
	godot_basis (*godot_basis_operator_multiply_scalar)(const godot_basis *p_self, const godot_real p_b);
	void (*godot_vector3_new)(godot_vector3 *r_dest, const godot_real p_x, const godot_real p_y, const godot_real p_z);
	godot_string (*godot_vector3_as_string)(const godot_vector3 *p_self);
	godot_int (*godot_vector3_min_axis)(const godot_vector3 *p_self);
	godot_int (*godot_vector3_max_axis)(const godot_vector3 *p_self);
	godot_real (*godot_vector3_length)(const godot_vector3 *p_self);
	godot_real (*godot_vector3_length_squared)(const godot_vector3 *p_self);
	godot_bool (*godot_vector3_is_normalized)(const godot_vector3 *p_self);
	godot_vector3 (*godot_vector3_normalized)(const godot_vector3 *p_self);
	godot_vector3 (*godot_vector3_inverse)(const godot_vector3 *p_self);
	godot_vector3 (*godot_vector3_snapped)(const godot_vector3 *p_self, const godot_vector3 *p_by);
	godot_vector3 (*godot_vector3_rotated)(const godot_vector3 *p_self, const godot_vector3 *p_axis, const godot_real p_phi);
	godot_vector3 (*godot_vector3_linear_interpolate)(const godot_vector3 *p_self, const godot_vector3 *p_b, const godot_real p_t);
	godot_vector3 (*godot_vector3_cubic_interpolate)(const godot_vector3 *p_self, const godot_vector3 *p_b, const godot_vector3 *p_pre_a, const godot_vector3 *p_post_b, const godot_real p_t);
	godot_real (*godot_vector3_dot)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_vector3 (*godot_vector3_cross)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_basis (*godot_vector3_outer)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_basis (*godot_vector3_to_diagonal_matrix)(const godot_vector3 *p_self);
	godot_vector3 (*godot_vector3_abs)(const godot_vector3 *p_self);
	godot_vector3 (*godot_vector3_floor)(const godot_vector3 *p_self);
	godot_vector3 (*godot_vector3_ceil)(const godot_vector3 *p_self);
	godot_real (*godot_vector3_distance_to)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_real (*godot_vector3_distance_squared_to)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_real (*godot_vector3_angle_to)(const godot_vector3 *p_self, const godot_vector3 *p_to);
	godot_vector3 (*godot_vector3_slide)(const godot_vector3 *p_self, const godot_vector3 *p_n);
	godot_vector3 (*godot_vector3_bounce)(const godot_vector3 *p_self, const godot_vector3 *p_n);
	godot_vector3 (*godot_vector3_reflect)(const godot_vector3 *p_self, const godot_vector3 *p_n);
	godot_vector3 (*godot_vector3_operator_add)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_vector3 (*godot_vector3_operator_subtract)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_vector3 (*godot_vector3_operator_multiply_vector)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_vector3 (*godot_vector3_operator_multiply_scalar)(const godot_vector3 *p_self, const godot_real p_b);
	godot_vector3 (*godot_vector3_operator_divide_vector)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_vector3 (*godot_vector3_operator_divide_scalar)(const godot_vector3 *p_self, const godot_real p_b);
	godot_bool (*godot_vector3_operator_equal)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_bool (*godot_vector3_operator_less)(const godot_vector3 *p_self, const godot_vector3 *p_b);
	godot_vector3 (*godot_vector3_operator_neg)(const godot_vector3 *p_self);
	void (*godot_vector3_set_axis)(godot_vector3 *p_self, const godot_vector3_axis p_axis, const godot_real p_val);
	godot_real (*godot_vector3_get_axis)(const godot_vector3 *p_self, const godot_vector3_axis p_axis);
	void (*godot_pool_byte_array_new)(godot_pool_byte_array *r_dest);
	void (*godot_pool_byte_array_new_copy)(godot_pool_byte_array *r_dest, const godot_pool_byte_array *p_src);
	void (*godot_pool_byte_array_new_with_array)(godot_pool_byte_array *r_dest, const godot_array *p_a);
	void (*godot_pool_byte_array_append)(godot_pool_byte_array *p_self, const uint8_t p_data);
	void (*godot_pool_byte_array_append_array)(godot_pool_byte_array *p_self, const godot_pool_byte_array *p_array);
	godot_error (*godot_pool_byte_array_insert)(godot_pool_byte_array *p_self, const godot_int p_idx, const uint8_t p_data);
	void (*godot_pool_byte_array_invert)(godot_pool_byte_array *p_self);
	void (*godot_pool_byte_array_push_back)(godot_pool_byte_array *p_self, const uint8_t p_data);
	void (*godot_pool_byte_array_remove)(godot_pool_byte_array *p_self, const godot_int p_idx);
	void (*godot_pool_byte_array_resize)(godot_pool_byte_array *p_self, const godot_int p_size);
	godot_pool_byte_array_read_access *(*godot_pool_byte_array_read)(const godot_pool_byte_array *p_self);
	godot_pool_byte_array_write_access *(*godot_pool_byte_array_write)(godot_pool_byte_array *p_self);
	void (*godot_pool_byte_array_set)(godot_pool_byte_array *p_self, const godot_int p_idx, const uint8_t p_data);
	uint8_t (*godot_pool_byte_array_get)(const godot_pool_byte_array *p_self, const godot_int p_idx);
	godot_int (*godot_pool_byte_array_size)(const godot_pool_byte_array *p_self);
	void (*godot_pool_byte_array_destroy)(godot_pool_byte_array *p_self);
	void (*godot_pool_int_array_new)(godot_pool_int_array *r_dest);
	void (*godot_pool_int_array_new_copy)(godot_pool_int_array *r_dest, const godot_pool_int_array *p_src);
	void (*godot_pool_int_array_new_with_array)(godot_pool_int_array *r_dest, const godot_array *p_a);
	void (*godot_pool_int_array_append)(godot_pool_int_array *p_self, const godot_int p_data);
	void (*godot_pool_int_array_append_array)(godot_pool_int_array *p_self, const godot_pool_int_array *p_array);
	godot_error (*godot_pool_int_array_insert)(godot_pool_int_array *p_self, const godot_int p_idx, const godot_int p_data);
	void (*godot_pool_int_array_invert)(godot_pool_int_array *p_self);
	void (*godot_pool_int_array_push_back)(godot_pool_int_array *p_self, const godot_int p_data);
	void (*godot_pool_int_array_remove)(godot_pool_int_array *p_self, const godot_int p_idx);
	void (*godot_pool_int_array_resize)(godot_pool_int_array *p_self, const godot_int p_size);
	godot_pool_int_array_read_access *(*godot_pool_int_array_read)(const godot_pool_int_array *p_self);
	godot_pool_int_array_write_access *(*godot_pool_int_array_write)(godot_pool_int_array *p_self);
	void (*godot_pool_int_array_set)(godot_pool_int_array *p_self, const godot_int p_idx, const godot_int p_data);
	godot_int (*godot_pool_int_array_get)(const godot_pool_int_array *p_self, const godot_int p_idx);
	godot_int (*godot_pool_int_array_size)(const godot_pool_int_array *p_self);
	void (*godot_pool_int_array_destroy)(godot_pool_int_array *p_self);
	void (*godot_pool_real_array_new)(godot_pool_real_array *r_dest);
	void (*godot_pool_real_array_new_copy)(godot_pool_real_array *r_dest, const godot_pool_real_array *p_src);
	void (*godot_pool_real_array_new_with_array)(godot_pool_real_array *r_dest, const godot_array *p_a);
	void (*godot_pool_real_array_append)(godot_pool_real_array *p_self, const godot_real p_data);
	void (*godot_pool_real_array_append_array)(godot_pool_real_array *p_self, const godot_pool_real_array *p_array);
	godot_error (*godot_pool_real_array_insert)(godot_pool_real_array *p_self, const godot_int p_idx, const godot_real p_data);
	void (*godot_pool_real_array_invert)(godot_pool_real_array *p_self);
	void (*godot_pool_real_array_push_back)(godot_pool_real_array *p_self, const godot_real p_data);
	void (*godot_pool_real_array_remove)(godot_pool_real_array *p_self, const godot_int p_idx);
	void (*godot_pool_real_array_resize)(godot_pool_real_array *p_self, const godot_int p_size);
	godot_pool_real_array_read_access *(*godot_pool_real_array_read)(const godot_pool_real_array *p_self);
	godot_pool_real_array_write_access *(*godot_pool_real_array_write)(godot_pool_real_array *p_self);
	void (*godot_pool_real_array_set)(godot_pool_real_array *p_self, const godot_int p_idx, const godot_real p_data);
	godot_real (*godot_pool_real_array_get)(const godot_pool_real_array *p_self, const godot_int p_idx);
	godot_int (*godot_pool_real_array_size)(const godot_pool_real_array *p_self);
	void (*godot_pool_real_array_destroy)(godot_pool_real_array *p_self);
	void (*godot_pool_string_array_new)(godot_pool_string_array *r_dest);
	void (*godot_pool_string_array_new_copy)(godot_pool_string_array *r_dest, const godot_pool_string_array *p_src);
	void (*godot_pool_string_array_new_with_array)(godot_pool_string_array *r_dest, const godot_array *p_a);
	void (*godot_pool_string_array_append)(godot_pool_string_array *p_self, const godot_string *p_data);
	void (*godot_pool_string_array_append_array)(godot_pool_string_array *p_self, const godot_pool_string_array *p_array);
	godot_error (*godot_pool_string_array_insert)(godot_pool_string_array *p_self, const godot_int p_idx, const godot_string *p_data);
	void (*godot_pool_string_array_invert)(godot_pool_string_array *p_self);
	void (*godot_pool_string_array_push_back)(godot_pool_string_array *p_self, const godot_string *p_data);
	void (*godot_pool_string_array_remove)(godot_pool_string_array *p_self, const godot_int p_idx);
	void (*godot_pool_string_array_resize)(godot_pool_string_array *p_self, const godot_int p_size);
	godot_pool_string_array_read_access *(*godot_pool_string_array_read)(const godot_pool_string_array *p_self);
	godot_pool_string_array_write_access *(*godot_pool_string_array_write)(godot_pool_string_array *p_self);
	void (*godot_pool_string_array_set)(godot_pool_string_array *p_self, const godot_int p_idx, const godot_string *p_data);
	godot_string (*godot_pool_string_array_get)(const godot_pool_string_array *p_self, const godot_int p_idx);
	godot_int (*godot_pool_string_array_size)(const godot_pool_string_array *p_self);
	void (*godot_pool_string_array_destroy)(godot_pool_string_array *p_self);
	void (*godot_pool_vector2_array_new)(godot_pool_vector2_array *r_dest);
	void (*godot_pool_vector2_array_new_copy)(godot_pool_vector2_array *r_dest, const godot_pool_vector2_array *p_src);
	void (*godot_pool_vector2_array_new_with_array)(godot_pool_vector2_array *r_dest, const godot_array *p_a);
	void (*godot_pool_vector2_array_append)(godot_pool_vector2_array *p_self, const godot_vector2 *p_data);
	void (*godot_pool_vector2_array_append_array)(godot_pool_vector2_array *p_self, const godot_pool_vector2_array *p_array);
	godot_error (*godot_pool_vector2_array_insert)(godot_pool_vector2_array *p_self, const godot_int p_idx, const godot_vector2 *p_data);
	void (*godot_pool_vector2_array_invert)(godot_pool_vector2_array *p_self);
	void (*godot_pool_vector2_array_push_back)(godot_pool_vector2_array *p_self, const godot_vector2 *p_data);
	void (*godot_pool_vector2_array_remove)(godot_pool_vector2_array *p_self, const godot_int p_idx);
	void (*godot_pool_vector2_array_resize)(godot_pool_vector2_array *p_self, const godot_int p_size);
	godot_pool_vector2_array_read_access *(*godot_pool_vector2_array_read)(const godot_pool_vector2_array *p_self);
	godot_pool_vector2_array_write_access *(*godot_pool_vector2_array_write)(godot_pool_vector2_array *p_self);
	void (*godot_pool_vector2_array_set)(godot_pool_vector2_array *p_self, const godot_int p_idx, const godot_vector2 *p_data);
	godot_vector2 (*godot_pool_vector2_array_get)(const godot_pool_vector2_array *p_self, const godot_int p_idx);
	godot_int (*godot_pool_vector2_array_size)(const godot_pool_vector2_array *p_self);
	void (*godot_pool_vector2_array_destroy)(godot_pool_vector2_array *p_self);
	void (*godot_pool_vector3_array_new)(godot_pool_vector3_array *r_dest);
	void (*godot_pool_vector3_array_new_copy)(godot_pool_vector3_array *r_dest, const godot_pool_vector3_array *p_src);
	void (*godot_pool_vector3_array_new_with_array)(godot_pool_vector3_array *r_dest, const godot_array *p_a);
	void (*godot_pool_vector3_array_append)(godot_pool_vector3_array *p_self, const godot_vector3 *p_data);
	void (*godot_pool_vector3_array_append_array)(godot_pool_vector3_array *p_self, const godot_pool_vector3_array *p_array);
	godot_error (*godot_pool_vector3_array_insert)(godot_pool_vector3_array *p_self, const godot_int p_idx, const godot_vector3 *p_data);
	void (*godot_pool_vector3_array_invert)(godot_pool_vector3_array *p_self);
	void (*godot_pool_vector3_array_push_back)(godot_pool_vector3_array *p_self, const godot_vector3 *p_data);
	void (*godot_pool_vector3_array_remove)(godot_pool_vector3_array *p_self, const godot_int p_idx);
	void (*godot_pool_vector3_array_resize)(godot_pool_vector3_array *p_self, const godot_int p_size);
	godot_pool_vector3_array_read_access *(*godot_pool_vector3_array_read)(const godot_pool_vector3_array *p_self);
	godot_pool_vector3_array_write_access *(*godot_pool_vector3_array_write)(godot_pool_vector3_array *p_self);
	void (*godot_pool_vector3_array_set)(godot_pool_vector3_array *p_self, const godot_int p_idx, const godot_vector3 *p_data);
	godot_vector3 (*godot_pool_vector3_array_get)(const godot_pool_vector3_array *p_self, const godot_int p_idx);
	godot_int (*godot_pool_vector3_array_size)(const godot_pool_vector3_array *p_self);
	void (*godot_pool_vector3_array_destroy)(godot_pool_vector3_array *p_self);
	void (*godot_pool_color_array_new)(godot_pool_color_array *r_dest);
	void (*godot_pool_color_array_new_copy)(godot_pool_color_array *r_dest, const godot_pool_color_array *p_src);
	void (*godot_pool_color_array_new_with_array)(godot_pool_color_array *r_dest, const godot_array *p_a);
	void (*godot_pool_color_array_append)(godot_pool_color_array *p_self, const godot_color *p_data);
	void (*godot_pool_color_array_append_array)(godot_pool_color_array *p_self, const godot_pool_color_array *p_array);
	godot_error (*godot_pool_color_array_insert)(godot_pool_color_array *p_self, const godot_int p_idx, const godot_color *p_data);
	void (*godot_pool_color_array_invert)(godot_pool_color_array *p_self);
	void (*godot_pool_color_array_push_back)(godot_pool_color_array *p_self, const godot_color *p_data);
	void (*godot_pool_color_array_remove)(godot_pool_color_array *p_self, const godot_int p_idx);
	void (*godot_pool_color_array_resize)(godot_pool_color_array *p_self, const godot_int p_size);
	godot_pool_color_array_read_access *(*godot_pool_color_array_read)(const godot_pool_color_array *p_self);
	godot_pool_color_array_write_access *(*godot_pool_color_array_write)(godot_pool_color_array *p_self);
	void (*godot_pool_color_array_set)(godot_pool_color_array *p_self, const godot_int p_idx, const godot_color *p_data);
	godot_color (*godot_pool_color_array_get)(const godot_pool_color_array *p_self, const godot_int p_idx);
	godot_int (*godot_pool_color_array_size)(const godot_pool_color_array *p_self);
	void (*godot_pool_color_array_destroy)(godot_pool_color_array *p_self);
	godot_pool_byte_array_read_access *(*godot_pool_byte_array_read_access_copy)(const godot_pool_byte_array_read_access *p_read);
	const uint8_t *(*godot_pool_byte_array_read_access_ptr)(const godot_pool_byte_array_read_access *p_read);
	void (*godot_pool_byte_array_read_access_operator_assign)(godot_pool_byte_array_read_access *p_read, godot_pool_byte_array_read_access *p_other);
	void (*godot_pool_byte_array_read_access_destroy)(godot_pool_byte_array_read_access *p_read);
	godot_pool_int_array_read_access *(*godot_pool_int_array_read_access_copy)(const godot_pool_int_array_read_access *p_read);
	const godot_int *(*godot_pool_int_array_read_access_ptr)(const godot_pool_int_array_read_access *p_read);
	void (*godot_pool_int_array_read_access_operator_assign)(godot_pool_int_array_read_access *p_read, godot_pool_int_array_read_access *p_other);
	void (*godot_pool_int_array_read_access_destroy)(godot_pool_int_array_read_access *p_read);
	godot_pool_real_array_read_access *(*godot_pool_real_array_read_access_copy)(const godot_pool_real_array_read_access *p_read);
	const godot_real *(*godot_pool_real_array_read_access_ptr)(const godot_pool_real_array_read_access *p_read);
	void (*godot_pool_real_array_read_access_operator_assign)(godot_pool_real_array_read_access *p_read, godot_pool_real_array_read_access *p_other);
	void (*godot_pool_real_array_read_access_destroy)(godot_pool_real_array_read_access *p_read);
	godot_pool_string_array_read_access *(*godot_pool_string_array_read_access_copy)(const godot_pool_string_array_read_access *p_read);
	const godot_string *(*godot_pool_string_array_read_access_ptr)(const godot_pool_string_array_read_access *p_read);
	void (*godot_pool_string_array_read_access_operator_assign)(godot_pool_string_array_read_access *p_read, godot_pool_string_array_read_access *p_other);
	void (*godot_pool_string_array_read_access_destroy)(godot_pool_string_array_read_access *p_read);
	godot_pool_vector2_array_read_access *(*godot_pool_vector2_array_read_access_copy)(const godot_pool_vector2_array_read_access *p_read);
	const godot_vector2 *(*godot_pool_vector2_array_read_access_ptr)(const godot_pool_vector2_array_read_access *p_read);
	void (*godot_pool_vector2_array_read_access_operator_assign)(godot_pool_vector2_array_read_access *p_read, godot_pool_vector2_array_read_access *p_other);
	void (*godot_pool_vector2_array_read_access_destroy)(godot_pool_vector2_array_read_access *p_read);
	godot_pool_vector3_array_read_access *(*godot_pool_vector3_array_read_access_copy)(const godot_pool_vector3_array_read_access *p_read);
	const godot_vector3 *(*godot_pool_vector3_array_read_access_ptr)(const godot_pool_vector3_array_read_access *p_read);
	void (*godot_pool_vector3_array_read_access_operator_assign)(godot_pool_vector3_array_read_access *p_read, godot_pool_vector3_array_read_access *p_other);
	void (*godot_pool_vector3_array_read_access_destroy)(godot_pool_vector3_array_read_access *p_read);
	godot_pool_color_array_read_access *(*godot_pool_color_array_read_access_copy)(const godot_pool_color_array_read_access *p_read);
	const godot_color *(*godot_pool_color_array_read_access_ptr)(const godot_pool_color_array_read_access *p_read);
	void (*godot_pool_color_array_read_access_operator_assign)(godot_pool_color_array_read_access *p_read, godot_pool_color_array_read_access *p_other);
	void (*godot_pool_color_array_read_access_destroy)(godot_pool_color_array_read_access *p_read);
	godot_pool_byte_array_write_access *(*godot_pool_byte_array_write_access_copy)(const godot_pool_byte_array_write_access *p_write);
	uint8_t *(*godot_pool_byte_array_write_access_ptr)(const godot_pool_byte_array_write_access *p_write);
	void (*godot_pool_byte_array_write_access_operator_assign)(godot_pool_byte_array_write_access *p_write, godot_pool_byte_array_write_access *p_other);
	void (*godot_pool_byte_array_write_access_destroy)(godot_pool_byte_array_write_access *p_write);
	godot_pool_int_array_write_access *(*godot_pool_int_array_write_access_copy)(const godot_pool_int_array_write_access *p_write);
	godot_int *(*godot_pool_int_array_write_access_ptr)(const godot_pool_int_array_write_access *p_write);
	void (*godot_pool_int_array_write_access_operator_assign)(godot_pool_int_array_write_access *p_write, godot_pool_int_array_write_access *p_other);
	void (*godot_pool_int_array_write_access_destroy)(godot_pool_int_array_write_access *p_write);
	godot_pool_real_array_write_access *(*godot_pool_real_array_write_access_copy)(const godot_pool_real_array_write_access *p_write);
	godot_real *(*godot_pool_real_array_write_access_ptr)(const godot_pool_real_array_write_access *p_write);
	void (*godot_pool_real_array_write_access_operator_assign)(godot_pool_real_array_write_access *p_write, godot_pool_real_array_write_access *p_other);
	void (*godot_pool_real_array_write_access_destroy)(godot_pool_real_array_write_access *p_write);
	godot_pool_string_array_write_access *(*godot_pool_string_array_write_access_copy)(const godot_pool_string_array_write_access *p_write);
	godot_string *(*godot_pool_string_array_write_access_ptr)(const godot_pool_string_array_write_access *p_write);
	void (*godot_pool_string_array_write_access_operator_assign)(godot_pool_string_array_write_access *p_write, godot_pool_string_array_write_access *p_other);
	void (*godot_pool_string_array_write_access_destroy)(godot_pool_string_array_write_access *p_write);
	godot_pool_vector2_array_write_access *(*godot_pool_vector2_array_write_access_copy)(const godot_pool_vector2_array_write_access *p_write);
	godot_vector2 *(*godot_pool_vector2_array_write_access_ptr)(const godot_pool_vector2_array_write_access *p_write);
	void (*godot_pool_vector2_array_write_access_operator_assign)(godot_pool_vector2_array_write_access *p_write, godot_pool_vector2_array_write_access *p_other);
	void (*godot_pool_vector2_array_write_access_destroy)(godot_pool_vector2_array_write_access *p_write);
	godot_pool_vector3_array_write_access *(*godot_pool_vector3_array_write_access_copy)(const godot_pool_vector3_array_write_access *p_write);
	godot_vector3 *(*godot_pool_vector3_array_write_access_ptr)(const godot_pool_vector3_array_write_access *p_write);
	void (*godot_pool_vector3_array_write_access_operator_assign)(godot_pool_vector3_array_write_access *p_write, godot_pool_vector3_array_write_access *p_other);
	void (*godot_pool_vector3_array_write_access_destroy)(godot_pool_vector3_array_write_access *p_write);
	godot_pool_color_array_write_access *(*godot_pool_color_array_write_access_copy)(const godot_pool_color_array_write_access *p_write);
	godot_color *(*godot_pool_color_array_write_access_ptr)(const godot_pool_color_array_write_access *p_write);
	void (*godot_pool_color_array_write_access_operator_assign)(godot_pool_color_array_write_access *p_write, godot_pool_color_array_write_access *p_other);
	void (*godot_pool_color_array_write_access_destroy)(godot_pool_color_array_write_access *p_write);
	void (*godot_array_new)(godot_array *r_dest);
	void (*godot_array_new_copy)(godot_array *r_dest, const godot_array *p_src);
	void (*godot_array_new_pool_color_array)(godot_array *r_dest, const godot_pool_color_array *p_pca);
	void (*godot_array_new_pool_vector3_array)(godot_array *r_dest, const godot_pool_vector3_array *p_pv3a);
	void (*godot_array_new_pool_vector2_array)(godot_array *r_dest, const godot_pool_vector2_array *p_pv2a);
	void (*godot_array_new_pool_string_array)(godot_array *r_dest, const godot_pool_string_array *p_psa);
	void (*godot_array_new_pool_real_array)(godot_array *r_dest, const godot_pool_real_array *p_pra);
	void (*godot_array_new_pool_int_array)(godot_array *r_dest, const godot_pool_int_array *p_pia);
	void (*godot_array_new_pool_byte_array)(godot_array *r_dest, const godot_pool_byte_array *p_pba);
	void (*godot_array_set)(godot_array *p_self, const godot_int p_idx, const godot_variant *p_value);
	godot_variant (*godot_array_get)(const godot_array *p_self, const godot_int p_idx);
	godot_variant *(*godot_array_operator_index)(godot_array *p_self, const godot_int p_idx);
	const godot_variant *(*godot_array_operator_index_const)(const godot_array *p_self, const godot_int p_idx);
	void (*godot_array_append)(godot_array *p_self, const godot_variant *p_value);
	void (*godot_array_clear)(godot_array *p_self);
	godot_int (*godot_array_count)(const godot_array *p_self, const godot_variant *p_value);
	godot_bool (*godot_array_empty)(const godot_array *p_self);
	void (*godot_array_erase)(godot_array *p_self, const godot_variant *p_value);
	godot_variant (*godot_array_front)(const godot_array *p_self);
	godot_variant (*godot_array_back)(const godot_array *p_self);
	godot_int (*godot_array_find)(const godot_array *p_self, const godot_variant *p_what, const godot_int p_from);
	godot_int (*godot_array_find_last)(const godot_array *p_self, const godot_variant *p_what);
	godot_bool (*godot_array_has)(const godot_array *p_self, const godot_variant *p_value);
	godot_int (*godot_array_hash)(const godot_array *p_self);
	void (*godot_array_insert)(godot_array *p_self, const godot_int p_pos, const godot_variant *p_value);
	void (*godot_array_invert)(godot_array *p_self);
	godot_variant (*godot_array_pop_back)(godot_array *p_self);
	godot_variant (*godot_array_pop_front)(godot_array *p_self);
	void (*godot_array_push_back)(godot_array *p_self, const godot_variant *p_value);
	void (*godot_array_push_front)(godot_array *p_self, const godot_variant *p_value);
	void (*godot_array_remove)(godot_array *p_self, const godot_int p_idx);
	void (*godot_array_resize)(godot_array *p_self, const godot_int p_size);
	godot_int (*godot_array_rfind)(const godot_array *p_self, const godot_variant *p_what, const godot_int p_from);
	godot_int (*godot_array_size)(const godot_array *p_self);
	void (*godot_array_sort)(godot_array *p_self);
	void (*godot_array_sort_custom)(godot_array *p_self, godot_object *p_obj, const godot_string *p_func);
	godot_int (*godot_array_bsearch)(godot_array *p_self, const godot_variant *p_value, const godot_bool p_before);
	godot_int (*godot_array_bsearch_custom)(godot_array *p_self, const godot_variant *p_value, godot_object *p_obj, const godot_string *p_func, const godot_bool p_before);
	void (*godot_array_destroy)(godot_array *p_self);
	void (*godot_dictionary_new)(godot_dictionary *r_dest);
	void (*godot_dictionary_new_copy)(godot_dictionary *r_dest, const godot_dictionary *p_src);
	void (*godot_dictionary_destroy)(godot_dictionary *p_self);
	godot_int (*godot_dictionary_size)(const godot_dictionary *p_self);
	godot_bool (*godot_dictionary_empty)(const godot_dictionary *p_self);
	void (*godot_dictionary_clear)(godot_dictionary *p_self);
	godot_bool (*godot_dictionary_has)(const godot_dictionary *p_self, const godot_variant *p_key);
	godot_bool (*godot_dictionary_has_all)(const godot_dictionary *p_self, const godot_array *p_keys);
	void (*godot_dictionary_erase)(godot_dictionary *p_self, const godot_variant *p_key);
	godot_int (*godot_dictionary_hash)(const godot_dictionary *p_self);
	godot_array (*godot_dictionary_keys)(const godot_dictionary *p_self);
	godot_array (*godot_dictionary_values)(const godot_dictionary *p_self);
	godot_variant (*godot_dictionary_get)(const godot_dictionary *p_self, const godot_variant *p_key);
	void (*godot_dictionary_set)(godot_dictionary *p_self, const godot_variant *p_key, const godot_variant *p_value);
	godot_variant *(*godot_dictionary_operator_index)(godot_dictionary *p_self, const godot_variant *p_key);
	const godot_variant *(*godot_dictionary_operator_index_const)(const godot_dictionary *p_self, const godot_variant *p_key);
	godot_variant *(*godot_dictionary_next)(const godot_dictionary *p_self, const godot_variant *p_key);
	godot_bool (*godot_dictionary_operator_equal)(const godot_dictionary *p_self, const godot_dictionary *p_b);
	godot_string (*godot_dictionary_to_json)(const godot_dictionary *p_self);
	void (*godot_node_path_new)(godot_node_path *r_dest, const godot_string *p_from);
	void (*godot_node_path_new_copy)(godot_node_path *r_dest, const godot_node_path *p_src);
	void (*godot_node_path_destroy)(godot_node_path *p_self);
	godot_string (*godot_node_path_as_string)(const godot_node_path *p_self);
	godot_bool (*godot_node_path_is_absolute)(const godot_node_path *p_self);
	godot_int (*godot_node_path_get_name_count)(const godot_node_path *p_self);
	godot_string (*godot_node_path_get_name)(const godot_node_path *p_self, const godot_int p_idx);
	godot_int (*godot_node_path_get_subname_count)(const godot_node_path *p_self);
	godot_string (*godot_node_path_get_subname)(const godot_node_path *p_self, const godot_int p_idx);
	godot_string (*godot_node_path_get_concatenated_subnames)(const godot_node_path *p_self);
	godot_bool (*godot_node_path_is_empty)(const godot_node_path *p_self);
	godot_bool (*godot_node_path_operator_equal)(const godot_node_path *p_self, const godot_node_path *p_b);
	void (*godot_plane_new_with_reals)(godot_plane *r_dest, const godot_real p_a, const godot_real p_b, const godot_real p_c, const godot_real p_d);
	void (*godot_plane_new_with_vectors)(godot_plane *r_dest, const godot_vector3 *p_v1, const godot_vector3 *p_v2, const godot_vector3 *p_v3);
	void (*godot_plane_new_with_normal)(godot_plane *r_dest, const godot_vector3 *p_normal, const godot_real p_d);
	godot_string (*godot_plane_as_string)(const godot_plane *p_self);
	godot_plane (*godot_plane_normalized)(const godot_plane *p_self);
	godot_vector3 (*godot_plane_center)(const godot_plane *p_self);
	godot_vector3 (*godot_plane_get_any_point)(const godot_plane *p_self);
	godot_bool (*godot_plane_is_point_over)(const godot_plane *p_self, const godot_vector3 *p_point);
	godot_real (*godot_plane_distance_to)(const godot_plane *p_self, const godot_vector3 *p_point);
	godot_bool (*godot_plane_has_point)(const godot_plane *p_self, const godot_vector3 *p_point, const godot_real p_epsilon);
	godot_vector3 (*godot_plane_project)(const godot_plane *p_self, const godot_vector3 *p_point);
	godot_bool (*godot_plane_intersect_3)(const godot_plane *p_self, godot_vector3 *r_dest, const godot_plane *p_b, const godot_plane *p_c);
	godot_bool (*godot_plane_intersects_ray)(const godot_plane *p_self, godot_vector3 *r_dest, const godot_vector3 *p_from, const godot_vector3 *p_dir);
	godot_bool (*godot_plane_intersects_segment)(const godot_plane *p_self, godot_vector3 *r_dest, const godot_vector3 *p_begin, const godot_vector3 *p_end);
	godot_plane (*godot_plane_operator_neg)(const godot_plane *p_self);
	godot_bool (*godot_plane_operator_equal)(const godot_plane *p_self, const godot_plane *p_b);
	void (*godot_plane_set_normal)(godot_plane *p_self, const godot_vector3 *p_normal);
	godot_vector3 (*godot_plane_get_normal)(const godot_plane *p_self);
	godot_real (*godot_plane_get_d)(const godot_plane *p_self);
	void (*godot_plane_set_d)(godot_plane *p_self, const godot_real p_d);
	void (*godot_rect2_new_with_position_and_size)(godot_rect2 *r_dest, const godot_vector2 *p_pos, const godot_vector2 *p_size);
	void (*godot_rect2_new)(godot_rect2 *r_dest, const godot_real p_x, const godot_real p_y, const godot_real p_width, const godot_real p_height);
	godot_string (*godot_rect2_as_string)(const godot_rect2 *p_self);
	godot_real (*godot_rect2_get_area)(const godot_rect2 *p_self);
	godot_bool (*godot_rect2_intersects)(const godot_rect2 *p_self, const godot_rect2 *p_b);
	godot_bool (*godot_rect2_encloses)(const godot_rect2 *p_self, const godot_rect2 *p_b);
	godot_bool (*godot_rect2_has_no_area)(const godot_rect2 *p_self);
	godot_rect2 (*godot_rect2_clip)(const godot_rect2 *p_self, const godot_rect2 *p_b);
	godot_rect2 (*godot_rect2_merge)(const godot_rect2 *p_self, const godot_rect2 *p_b);
	godot_bool (*godot_rect2_has_point)(const godot_rect2 *p_self, const godot_vector2 *p_point);
	godot_rect2 (*godot_rect2_grow)(const godot_rect2 *p_self, const godot_real p_by);
	godot_rect2 (*godot_rect2_expand)(const godot_rect2 *p_self, const godot_vector2 *p_to);
	godot_bool (*godot_rect2_operator_equal)(const godot_rect2 *p_self, const godot_rect2 *p_b);
	godot_vector2 (*godot_rect2_get_position)(const godot_rect2 *p_self);
	godot_vector2 (*godot_rect2_get_size)(const godot_rect2 *p_self);
	void (*godot_rect2_set_position)(godot_rect2 *p_self, const godot_vector2 *p_pos);
	void (*godot_rect2_set_size)(godot_rect2 *p_self, const godot_vector2 *p_size);
	void (*godot_aabb_new)(godot_aabb *r_dest, const godot_vector3 *p_pos, const godot_vector3 *p_size);
	godot_vector3 (*godot_aabb_get_position)(const godot_aabb *p_self);
	void (*godot_aabb_set_position)(const godot_aabb *p_self, const godot_vector3 *p_v);
	godot_vector3 (*godot_aabb_get_size)(const godot_aabb *p_self);
	void (*godot_aabb_set_size)(const godot_aabb *p_self, const godot_vector3 *p_v);
	godot_string (*godot_aabb_as_string)(const godot_aabb *p_self);
	godot_real (*godot_aabb_get_area)(const godot_aabb *p_self);
	godot_bool (*godot_aabb_has_no_area)(const godot_aabb *p_self);
	godot_bool (*godot_aabb_has_no_surface)(const godot_aabb *p_self);
	godot_bool (*godot_aabb_intersects)(const godot_aabb *p_self, const godot_aabb *p_with);
	godot_bool (*godot_aabb_encloses)(const godot_aabb *p_self, const godot_aabb *p_with);
	godot_aabb (*godot_aabb_merge)(const godot_aabb *p_self, const godot_aabb *p_with);
	godot_aabb (*godot_aabb_intersection)(const godot_aabb *p_self, const godot_aabb *p_with);
	godot_bool (*godot_aabb_intersects_plane)(const godot_aabb *p_self, const godot_plane *p_plane);
	godot_bool (*godot_aabb_intersects_segment)(const godot_aabb *p_self, const godot_vector3 *p_from, const godot_vector3 *p_to);
	godot_bool (*godot_aabb_has_point)(const godot_aabb *p_self, const godot_vector3 *p_point);
	godot_vector3 (*godot_aabb_get_support)(const godot_aabb *p_self, const godot_vector3 *p_dir);
	godot_vector3 (*godot_aabb_get_longest_axis)(const godot_aabb *p_self);
	godot_int (*godot_aabb_get_longest_axis_index)(const godot_aabb *p_self);
	godot_real (*godot_aabb_get_longest_axis_size)(const godot_aabb *p_self);
	godot_vector3 (*godot_aabb_get_shortest_axis)(const godot_aabb *p_self);
	godot_int (*godot_aabb_get_shortest_axis_index)(const godot_aabb *p_self);
	godot_real (*godot_aabb_get_shortest_axis_size)(const godot_aabb *p_self);
	godot_aabb (*godot_aabb_expand)(const godot_aabb *p_self, const godot_vector3 *p_to_point);
	godot_aabb (*godot_aabb_grow)(const godot_aabb *p_self, const godot_real p_by);
	godot_vector3 (*godot_aabb_get_endpoint)(const godot_aabb *p_self, const godot_int p_idx);
	godot_bool (*godot_aabb_operator_equal)(const godot_aabb *p_self, const godot_aabb *p_b);
	void (*godot_rid_new)(godot_rid *r_dest);
	godot_int (*godot_rid_get_id)(const godot_rid *p_self);
	void (*godot_rid_new_with_resource)(godot_rid *r_dest, const godot_object *p_from);
	godot_bool (*godot_rid_operator_equal)(const godot_rid *p_self, const godot_rid *p_b);
	godot_bool (*godot_rid_operator_less)(const godot_rid *p_self, const godot_rid *p_b);
	void (*godot_transform_new_with_axis_origin)(godot_transform *r_dest, const godot_vector3 *p_x_axis, const godot_vector3 *p_y_axis, const godot_vector3 *p_z_axis, const godot_vector3 *p_origin);
	void (*godot_transform_new)(godot_transform *r_dest, const godot_basis *p_basis, const godot_vector3 *p_origin);
	godot_basis (*godot_transform_get_basis)(const godot_transform *p_self);
	void (*godot_transform_set_basis)(godot_transform *p_self, const godot_basis *p_v);
	godot_vector3 (*godot_transform_get_origin)(const godot_transform *p_self);
	void (*godot_transform_set_origin)(godot_transform *p_self, const godot_vector3 *p_v);
	godot_string (*godot_transform_as_string)(const godot_transform *p_self);
	godot_transform (*godot_transform_inverse)(const godot_transform *p_self);
	godot_transform (*godot_transform_affine_inverse)(const godot_transform *p_self);
	godot_transform (*godot_transform_orthonormalized)(const godot_transform *p_self);
	godot_transform (*godot_transform_rotated)(const godot_transform *p_self, const godot_vector3 *p_axis, const godot_real p_phi);
	godot_transform (*godot_transform_scaled)(const godot_transform *p_self, const godot_vector3 *p_scale);
	godot_transform (*godot_transform_translated)(const godot_transform *p_self, const godot_vector3 *p_ofs);
	godot_transform (*godot_transform_looking_at)(const godot_transform *p_self, const godot_vector3 *p_target, const godot_vector3 *p_up);
	godot_plane (*godot_transform_xform_plane)(const godot_transform *p_self, const godot_plane *p_v);
	godot_plane (*godot_transform_xform_inv_plane)(const godot_transform *p_self, const godot_plane *p_v);
	void (*godot_transform_new_identity)(godot_transform *r_dest);
	godot_bool (*godot_transform_operator_equal)(const godot_transform *p_self, const godot_transform *p_b);
	godot_transform (*godot_transform_operator_multiply)(const godot_transform *p_self, const godot_transform *p_b);
	godot_vector3 (*godot_transform_xform_vector3)(const godot_transform *p_self, const godot_vector3 *p_v);
	godot_vector3 (*godot_transform_xform_inv_vector3)(const godot_transform *p_self, const godot_vector3 *p_v);
	godot_aabb (*godot_transform_xform_aabb)(const godot_transform *p_self, const godot_aabb *p_v);
	godot_aabb (*godot_transform_xform_inv_aabb)(const godot_transform *p_self, const godot_aabb *p_v);
	void (*godot_transform2d_new)(godot_transform2d *r_dest, const godot_real p_rot, const godot_vector2 *p_pos);
	void (*godot_transform2d_new_axis_origin)(godot_transform2d *r_dest, const godot_vector2 *p_x_axis, const godot_vector2 *p_y_axis, const godot_vector2 *p_origin);
	godot_string (*godot_transform2d_as_string)(const godot_transform2d *p_self);
	godot_transform2d (*godot_transform2d_inverse)(const godot_transform2d *p_self);
	godot_transform2d (*godot_transform2d_affine_inverse)(const godot_transform2d *p_self);
	godot_real (*godot_transform2d_get_rotation)(const godot_transform2d *p_self);
	godot_vector2 (*godot_transform2d_get_origin)(const godot_transform2d *p_self);
	godot_vector2 (*godot_transform2d_get_scale)(const godot_transform2d *p_self);
	godot_transform2d (*godot_transform2d_orthonormalized)(const godot_transform2d *p_self);
	godot_transform2d (*godot_transform2d_rotated)(const godot_transform2d *p_self, const godot_real p_phi);
	godot_transform2d (*godot_transform2d_scaled)(const godot_transform2d *p_self, const godot_vector2 *p_scale);
	godot_transform2d (*godot_transform2d_translated)(const godot_transform2d *p_self, const godot_vector2 *p_offset);
	godot_vector2 (*godot_transform2d_xform_vector2)(const godot_transform2d *p_self, const godot_vector2 *p_v);
	godot_vector2 (*godot_transform2d_xform_inv_vector2)(const godot_transform2d *p_self, const godot_vector2 *p_v);
	godot_vector2 (*godot_transform2d_basis_xform_vector2)(const godot_transform2d *p_self, const godot_vector2 *p_v);
	godot_vector2 (*godot_transform2d_basis_xform_inv_vector2)(const godot_transform2d *p_self, const godot_vector2 *p_v);
	godot_transform2d (*godot_transform2d_interpolate_with)(const godot_transform2d *p_self, const godot_transform2d *p_m, const godot_real p_c);
	godot_bool (*godot_transform2d_operator_equal)(const godot_transform2d *p_self, const godot_transform2d *p_b);
	godot_transform2d (*godot_transform2d_operator_multiply)(const godot_transform2d *p_self, const godot_transform2d *p_b);
	void (*godot_transform2d_new_identity)(godot_transform2d *r_dest);
	godot_rect2 (*godot_transform2d_xform_rect2)(const godot_transform2d *p_self, const godot_rect2 *p_v);
	godot_rect2 (*godot_transform2d_xform_inv_rect2)(const godot_transform2d *p_self, const godot_rect2 *p_v);
	godot_variant_type (*godot_variant_get_type)(const godot_variant *p_v);
	void (*godot_variant_new_copy)(godot_variant *r_dest, const godot_variant *p_src);
	void (*godot_variant_new_nil)(godot_variant *r_dest);
	void (*godot_variant_new_bool)(godot_variant *r_dest, const godot_bool p_b);
	void (*godot_variant_new_uint)(godot_variant *r_dest, const uint64_t p_i);
	void (*godot_variant_new_int)(godot_variant *r_dest, const int64_t p_i);
	void (*godot_variant_new_real)(godot_variant *r_dest, const double p_r);
	void (*godot_variant_new_string)(godot_variant *r_dest, const godot_string *p_s);
	void (*godot_variant_new_vector2)(godot_variant *r_dest, const godot_vector2 *p_v2);
	void (*godot_variant_new_rect2)(godot_variant *r_dest, const godot_rect2 *p_rect2);
	void (*godot_variant_new_vector3)(godot_variant *r_dest, const godot_vector3 *p_v3);
	void (*godot_variant_new_transform2d)(godot_variant *r_dest, const godot_transform2d *p_t2d);
	void (*godot_variant_new_plane)(godot_variant *r_dest, const godot_plane *p_plane);
	void (*godot_variant_new_quat)(godot_variant *r_dest, const godot_quat *p_quat);
	void (*godot_variant_new_aabb)(godot_variant *r_dest, const godot_aabb *p_aabb);
	void (*godot_variant_new_basis)(godot_variant *r_dest, const godot_basis *p_basis);
	void (*godot_variant_new_transform)(godot_variant *r_dest, const godot_transform *p_trans);
	void (*godot_variant_new_color)(godot_variant *r_dest, const godot_color *p_color);
	void (*godot_variant_new_node_path)(godot_variant *r_dest, const godot_node_path *p_np);
	void (*godot_variant_new_rid)(godot_variant *r_dest, const godot_rid *p_rid);
	void (*godot_variant_new_object)(godot_variant *r_dest, const godot_object *p_obj);
	void (*godot_variant_new_dictionary)(godot_variant *r_dest, const godot_dictionary *p_dict);
	void (*godot_variant_new_array)(godot_variant *r_dest, const godot_array *p_arr);
	void (*godot_variant_new_pool_byte_array)(godot_variant *r_dest, const godot_pool_byte_array *p_pba);
	void (*godot_variant_new_pool_int_array)(godot_variant *r_dest, const godot_pool_int_array *p_pia);
	void (*godot_variant_new_pool_real_array)(godot_variant *r_dest, const godot_pool_real_array *p_pra);
	void (*godot_variant_new_pool_string_array)(godot_variant *r_dest, const godot_pool_string_array *p_psa);
	void (*godot_variant_new_pool_vector2_array)(godot_variant *r_dest, const godot_pool_vector2_array *p_pv2a);
	void (*godot_variant_new_pool_vector3_array)(godot_variant *r_dest, const godot_pool_vector3_array *p_pv3a);
	void (*godot_variant_new_pool_color_array)(godot_variant *r_dest, const godot_pool_color_array *p_pca);
	godot_bool (*godot_variant_as_bool)(const godot_variant *p_self);
	uint64_t (*godot_variant_as_uint)(const godot_variant *p_self);
	int64_t (*godot_variant_as_int)(const godot_variant *p_self);
	double (*godot_variant_as_real)(const godot_variant *p_self);
	godot_string (*godot_variant_as_string)(const godot_variant *p_self);
	godot_vector2 (*godot_variant_as_vector2)(const godot_variant *p_self);
	godot_rect2 (*godot_variant_as_rect2)(const godot_variant *p_self);
	godot_vector3 (*godot_variant_as_vector3)(const godot_variant *p_self);
	godot_transform2d (*godot_variant_as_transform2d)(const godot_variant *p_self);
	godot_plane (*godot_variant_as_plane)(const godot_variant *p_self);
	godot_quat (*godot_variant_as_quat)(const godot_variant *p_self);
	godot_aabb (*godot_variant_as_aabb)(const godot_variant *p_self);
	godot_basis (*godot_variant_as_basis)(const godot_variant *p_self);
	godot_transform (*godot_variant_as_transform)(const godot_variant *p_self);
	godot_color (*godot_variant_as_color)(const godot_variant *p_self);
	godot_node_path (*godot_variant_as_node_path)(const godot_variant *p_self);
	godot_rid (*godot_variant_as_rid)(const godot_variant *p_self);
	godot_object *(*godot_variant_as_object)(const godot_variant *p_self);
	godot_dictionary (*godot_variant_as_dictionary)(const godot_variant *p_self);
	godot_array (*godot_variant_as_array)(const godot_variant *p_self);
	godot_pool_byte_array (*godot_variant_as_pool_byte_array)(const godot_variant *p_self);
	godot_pool_int_array (*godot_variant_as_pool_int_array)(const godot_variant *p_self);
	godot_pool_real_array (*godot_variant_as_pool_real_array)(const godot_variant *p_self);
	godot_pool_string_array (*godot_variant_as_pool_string_array)(const godot_variant *p_self);
	godot_pool_vector2_array (*godot_variant_as_pool_vector2_array)(const godot_variant *p_self);
	godot_pool_vector3_array (*godot_variant_as_pool_vector3_array)(const godot_variant *p_self);
	godot_pool_color_array (*godot_variant_as_pool_color_array)(const godot_variant *p_self);
	godot_variant (*godot_variant_call)(godot_variant *p_self, const godot_string *p_method, const godot_variant **p_args, const godot_int p_argcount, godot_variant_call_error *r_error);
	godot_bool (*godot_variant_has_method)(const godot_variant *p_self, const godot_string *p_method);
	godot_bool (*godot_variant_operator_equal)(const godot_variant *p_self, const godot_variant *p_other);
	godot_bool (*godot_variant_operator_less)(const godot_variant *p_self, const godot_variant *p_other);
	godot_bool (*godot_variant_hash_compare)(const godot_variant *p_self, const godot_variant *p_other);
	godot_bool (*godot_variant_booleanize)(const godot_variant *p_self);
	void (*godot_variant_destroy)(godot_variant *p_self);
	godot_int (*godot_char_string_length)(const godot_char_string *p_cs);
	const char *(*godot_char_string_get_data)(const godot_char_string *p_cs);
	void (*godot_char_string_destroy)(godot_char_string *p_cs);
	void (*godot_string_new)(godot_string *r_dest);
	void (*godot_string_new_copy)(godot_string *r_dest, const godot_string *p_src);
	void (*godot_string_new_with_wide_string)(godot_string *r_dest, const wchar_t *p_contents, const int p_size);
	const wchar_t *(*godot_string_operator_index)(godot_string *p_self, const godot_int p_idx);
	wchar_t (*godot_string_operator_index_const)(const godot_string *p_self, const godot_int p_idx);
	const wchar_t *(*godot_string_wide_str)(const godot_string *p_self);
	godot_bool (*godot_string_operator_equal)(const godot_string *p_self, const godot_string *p_b);
	godot_bool (*godot_string_operator_less)(const godot_string *p_self, const godot_string *p_b);
	godot_string (*godot_string_operator_plus)(const godot_string *p_self, const godot_string *p_b);
	godot_int (*godot_string_length)(const godot_string *p_self);
	signed char (*godot_string_casecmp_to)(const godot_string *p_self, const godot_string *p_str);
	signed char (*godot_string_nocasecmp_to)(const godot_string *p_self, const godot_string *p_str);
	signed char (*godot_string_naturalnocasecmp_to)(const godot_string *p_self, const godot_string *p_str);
	godot_bool (*godot_string_begins_with)(const godot_string *p_self, const godot_string *p_string);
	godot_bool (*godot_string_begins_with_char_array)(const godot_string *p_self, const char *p_char_array);
	godot_array (*godot_string_bigrams)(const godot_string *p_self);
	godot_string (*godot_string_chr)(wchar_t p_character);
	godot_bool (*godot_string_ends_with)(const godot_string *p_self, const godot_string *p_string);
	godot_int (*godot_string_find)(const godot_string *p_self, godot_string p_what);
	godot_int (*godot_string_find_from)(const godot_string *p_self, godot_string p_what, godot_int p_from);
	godot_int (*godot_string_findmk)(const godot_string *p_self, const godot_array *p_keys);
	godot_int (*godot_string_findmk_from)(const godot_string *p_self, const godot_array *p_keys, godot_int p_from);
	godot_int (*godot_string_findmk_from_in_place)(const godot_string *p_self, const godot_array *p_keys, godot_int p_from, godot_int *r_key);
	godot_int (*godot_string_findn)(const godot_string *p_self, godot_string p_what);
	godot_int (*godot_string_findn_from)(const godot_string *p_self, godot_string p_what, godot_int p_from);
	godot_int (*godot_string_find_last)(const godot_string *p_self, godot_string p_what);
	godot_string (*godot_string_format)(const godot_string *p_self, const godot_variant *p_values);
	godot_string (*godot_string_format_with_custom_placeholder)(const godot_string *p_self, const godot_variant *p_values, const char *p_placeholder);
	godot_string (*godot_string_hex_encode_buffer)(const uint8_t *p_buffer, godot_int p_len);
	godot_int (*godot_string_hex_to_int)(const godot_string *p_self);
	godot_int (*godot_string_hex_to_int_without_prefix)(const godot_string *p_self);
	godot_string (*godot_string_insert)(const godot_string *p_self, godot_int p_at_pos, godot_string p_string);
	godot_bool (*godot_string_is_numeric)(const godot_string *p_self);
	godot_bool (*godot_string_is_subsequence_of)(const godot_string *p_self, const godot_string *p_string);
	godot_bool (*godot_string_is_subsequence_ofi)(const godot_string *p_self, const godot_string *p_string);
	godot_string (*godot_string_lpad)(const godot_string *p_self, godot_int p_min_length);
	godot_string (*godot_string_lpad_with_custom_character)(const godot_string *p_self, godot_int p_min_length, const godot_string *p_character);
	godot_bool (*godot_string_match)(const godot_string *p_self, const godot_string *p_wildcard);
	godot_bool (*godot_string_matchn)(const godot_string *p_self, const godot_string *p_wildcard);
	godot_string (*godot_string_md5)(const uint8_t *p_md5);
	godot_string (*godot_string_num)(double p_num);
	godot_string (*godot_string_num_int64)(int64_t p_num, godot_int p_base);
	godot_string (*godot_string_num_int64_capitalized)(int64_t p_num, godot_int p_base, godot_bool p_capitalize_hex);
	godot_string (*godot_string_num_real)(double p_num);
	godot_string (*godot_string_num_scientific)(double p_num);
	godot_string (*godot_string_num_with_decimals)(double p_num, godot_int p_decimals);
	godot_string (*godot_string_pad_decimals)(const godot_string *p_self, godot_int p_digits);
	godot_string (*godot_string_pad_zeros)(const godot_string *p_self, godot_int p_digits);
	godot_string (*godot_string_replace_first)(const godot_string *p_self, godot_string p_key, godot_string p_with);
	godot_string (*godot_string_replace)(const godot_string *p_self, godot_string p_key, godot_string p_with);
	godot_string (*godot_string_replacen)(const godot_string *p_self, godot_string p_key, godot_string p_with);
	godot_int (*godot_string_rfind)(const godot_string *p_self, godot_string p_what);
	godot_int (*godot_string_rfindn)(const godot_string *p_self, godot_string p_what);
	godot_int (*godot_string_rfind_from)(const godot_string *p_self, godot_string p_what, godot_int p_from);
	godot_int (*godot_string_rfindn_from)(const godot_string *p_self, godot_string p_what, godot_int p_from);
	godot_string (*godot_string_rpad)(const godot_string *p_self, godot_int p_min_length);
	godot_string (*godot_string_rpad_with_custom_character)(const godot_string *p_self, godot_int p_min_length, const godot_string *p_character);
	godot_real (*godot_string_similarity)(const godot_string *p_self, const godot_string *p_string);
	godot_string (*godot_string_sprintf)(const godot_string *p_self, const godot_array *p_values, godot_bool *p_error);
	godot_string (*godot_string_substr)(const godot_string *p_self, godot_int p_from, godot_int p_chars);
	double (*godot_string_to_double)(const godot_string *p_self);
	godot_real (*godot_string_to_float)(const godot_string *p_self);
	godot_int (*godot_string_to_int)(const godot_string *p_self);
	godot_string (*godot_string_camelcase_to_underscore)(const godot_string *p_self);
	godot_string (*godot_string_camelcase_to_underscore_lowercased)(const godot_string *p_self);
	godot_string (*godot_string_capitalize)(const godot_string *p_self);
	double (*godot_string_char_to_double)(const char *p_what);
	godot_int (*godot_string_char_to_int)(const char *p_what);
	int64_t (*godot_string_wchar_to_int)(const wchar_t *p_str);
	godot_int (*godot_string_char_to_int_with_len)(const char *p_what, godot_int p_len);
	int64_t (*godot_string_char_to_int64_with_len)(const wchar_t *p_str, int p_len);
	int64_t (*godot_string_hex_to_int64)(const godot_string *p_self);
	int64_t (*godot_string_hex_to_int64_with_prefix)(const godot_string *p_self);
	int64_t (*godot_string_to_int64)(const godot_string *p_self);
	double (*godot_string_unicode_char_to_double)(const wchar_t *p_str, const wchar_t **r_end);
	godot_int (*godot_string_get_slice_count)(const godot_string *p_self, godot_string p_splitter);
	godot_string (*godot_string_get_slice)(const godot_string *p_self, godot_string p_splitter, godot_int p_slice);
	godot_string (*godot_string_get_slicec)(const godot_string *p_self, wchar_t p_splitter, godot_int p_slice);
	godot_array (*godot_string_split)(const godot_string *p_self, const godot_string *p_splitter);
	godot_array (*godot_string_split_allow_empty)(const godot_string *p_self, const godot_string *p_splitter);
	godot_array (*godot_string_split_floats)(const godot_string *p_self, const godot_string *p_splitter);
	godot_array (*godot_string_split_floats_allows_empty)(const godot_string *p_self, const godot_string *p_splitter);
	godot_array (*godot_string_split_floats_mk)(const godot_string *p_self, const godot_array *p_splitters);
	godot_array (*godot_string_split_floats_mk_allows_empty)(const godot_string *p_self, const godot_array *p_splitters);
	godot_array (*godot_string_split_ints)(const godot_string *p_self, const godot_string *p_splitter);
	godot_array (*godot_string_split_ints_allows_empty)(const godot_string *p_self, const godot_string *p_splitter);
	godot_array (*godot_string_split_ints_mk)(const godot_string *p_self, const godot_array *p_splitters);
	godot_array (*godot_string_split_ints_mk_allows_empty)(const godot_string *p_self, const godot_array *p_splitters);
	godot_array (*godot_string_split_spaces)(const godot_string *p_self);
	wchar_t (*godot_string_char_lowercase)(wchar_t p_char);
	wchar_t (*godot_string_char_uppercase)(wchar_t p_char);
	godot_string (*godot_string_to_lower)(const godot_string *p_self);
	godot_string (*godot_string_to_upper)(const godot_string *p_self);
	godot_string (*godot_string_get_basename)(const godot_string *p_self);
	godot_string (*godot_string_get_extension)(const godot_string *p_self);
	godot_string (*godot_string_left)(const godot_string *p_self, godot_int p_pos);
	wchar_t (*godot_string_ord_at)(const godot_string *p_self, godot_int p_idx);
	godot_string (*godot_string_plus_file)(const godot_string *p_self, const godot_string *p_file);
	godot_string (*godot_string_right)(const godot_string *p_self, godot_int p_pos);
	godot_string (*godot_string_strip_edges)(const godot_string *p_self, godot_bool p_left, godot_bool p_right);
	godot_string (*godot_string_strip_escapes)(const godot_string *p_self);
	void (*godot_string_erase)(godot_string *p_self, godot_int p_pos, godot_int p_chars);
	godot_char_string (*godot_string_ascii)(const godot_string *p_self);
	godot_char_string (*godot_string_ascii_extended)(const godot_string *p_self);
	godot_char_string (*godot_string_utf8)(const godot_string *p_self);
	godot_bool (*godot_string_parse_utf8)(godot_string *p_self, const char *p_utf8);
	godot_bool (*godot_string_parse_utf8_with_len)(godot_string *p_self, const char *p_utf8, godot_int p_len);
	godot_string (*godot_string_chars_to_utf8)(const char *p_utf8);
	godot_string (*godot_string_chars_to_utf8_with_len)(const char *p_utf8, godot_int p_len);
	uint32_t (*godot_string_hash)(const godot_string *p_self);
	uint64_t (*godot_string_hash64)(const godot_string *p_self);
	uint32_t (*godot_string_hash_chars)(const char *p_cstr);
	uint32_t (*godot_string_hash_chars_with_len)(const char *p_cstr, godot_int p_len);
	uint32_t (*godot_string_hash_utf8_chars)(const wchar_t *p_str);
	uint32_t (*godot_string_hash_utf8_chars_with_len)(const wchar_t *p_str, godot_int p_len);
	godot_pool_byte_array (*godot_string_md5_buffer)(const godot_string *p_self);
	godot_string (*godot_string_md5_text)(const godot_string *p_self);
	godot_pool_byte_array (*godot_string_sha256_buffer)(const godot_string *p_self);
	godot_string (*godot_string_sha256_text)(const godot_string *p_self);
	godot_bool (*godot_string_empty)(const godot_string *p_self);
	godot_string (*godot_string_get_base_dir)(const godot_string *p_self);
	godot_string (*godot_string_get_file)(const godot_string *p_self);
	godot_string (*godot_string_humanize_size)(uint64_t p_size);
	godot_bool (*godot_string_is_abs_path)(const godot_string *p_self);
	godot_bool (*godot_string_is_rel_path)(const godot_string *p_self);
	godot_bool (*godot_string_is_resource_file)(const godot_string *p_self);
	godot_string (*godot_string_path_to)(const godot_string *p_self, const godot_string *p_path);
	godot_string (*godot_string_path_to_file)(const godot_string *p_self, const godot_string *p_path);
	godot_string (*godot_string_simplify_path)(const godot_string *p_self);
	godot_string (*godot_string_c_escape)(const godot_string *p_self);
	godot_string (*godot_string_c_escape_multiline)(const godot_string *p_self);
	godot_string (*godot_string_c_unescape)(const godot_string *p_self);
	godot_string (*godot_string_http_escape)(const godot_string *p_self);
	godot_string (*godot_string_http_unescape)(const godot_string *p_self);
	godot_string (*godot_string_json_escape)(const godot_string *p_self);
	godot_string (*godot_string_word_wrap)(const godot_string *p_self, godot_int p_chars_per_line);
	godot_string (*godot_string_xml_escape)(const godot_string *p_self);
	godot_string (*godot_string_xml_escape_with_quotes)(const godot_string *p_self);
	godot_string (*godot_string_xml_unescape)(const godot_string *p_self);
	godot_string (*godot_string_percent_decode)(const godot_string *p_self);
	godot_string (*godot_string_percent_encode)(const godot_string *p_self);
	godot_bool (*godot_string_is_valid_float)(const godot_string *p_self);
	godot_bool (*godot_string_is_valid_hex_number)(const godot_string *p_self, godot_bool p_with_prefix);
	godot_bool (*godot_string_is_valid_html_color)(const godot_string *p_self);
	godot_bool (*godot_string_is_valid_identifier)(const godot_string *p_self);
	godot_bool (*godot_string_is_valid_integer)(const godot_string *p_self);
	godot_bool (*godot_string_is_valid_ip_address)(const godot_string *p_self);
	void (*godot_string_destroy)(godot_string *p_self);
	void (*godot_string_name_new)(godot_string_name *r_dest, const godot_string *p_name);
	void (*godot_string_name_new_data)(godot_string_name *r_dest, const char *p_name);
	godot_string (*godot_string_name_get_name)(const godot_string_name *p_self);
	uint32_t (*godot_string_name_get_hash)(const godot_string_name *p_self);
	const void *(*godot_string_name_get_data_unique_pointer)(const godot_string_name *p_self);
	godot_bool (*godot_string_name_operator_equal)(const godot_string_name *p_self, const godot_string_name *p_other);
	godot_bool (*godot_string_name_operator_less)(const godot_string_name *p_self, const godot_string_name *p_other);
	void (*godot_string_name_destroy)(godot_string_name *p_self);
	void (*godot_object_destroy)(godot_object *p_o);
	godot_object *(*godot_global_get_singleton)(char *p_name);
	godot_method_bind *(*godot_method_bind_get_method)(const char *p_classname, const char *p_methodname);
	void (*godot_method_bind_ptrcall)(godot_method_bind *p_method_bind, godot_object *p_instance, const void **p_args, void *p_ret);
	godot_variant (*godot_method_bind_call)(godot_method_bind *p_method_bind, godot_object *p_instance, const godot_variant **p_args, const int p_arg_count, godot_variant_call_error *p_call_error);
	godot_class_constructor (*godot_get_class_constructor)(const char *p_classname);
	godot_dictionary (*godot_get_global_constants)();
	void (*godot_register_native_call_type)(const char *call_type, native_call_cb p_callback);
	void *(*godot_alloc)(int p_bytes);
	void *(*godot_realloc)(void *p_ptr, int p_bytes);
	void (*godot_free)(void *p_ptr);
	void (*godot_print_error)(const char *p_description, const char *p_function, const char *p_file, int p_line);
	void (*godot_print_warning)(const char *p_description, const char *p_function, const char *p_file, int p_line);
	void (*godot_print)(const godot_string *p_message);
} godot_gdnative_core_api_struct;

