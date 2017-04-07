import cffi
import os


BASEDIR = os.path.dirname(os.path.abspath(__file__))

ffibuilder = cffi.FFI()

ffibuilder.embedding_api(r"""
    typedef struct { ...; } PyObject;
    typedef void godot_object;
    int do_stuff(int, int);
    PyObject *instanciate_binding_from_godot_obj(PyObject *py_cls, godot_object *godot_obj);
    void py_instance_set_godot_obj(PyObject *py_instance, godot_object *godot_obj);
    PyObject *variants_to_pyobjs(void **args, int argcount);
    PyObject *variant_to_pyobj2(void *arg);
""")

ffibuilder.set_source("pythonscriptcffi", """
#include "Include/Python.h"
#include "modules/dlscript/godot.h"
// TODO: MethodFlags not in ldscript headers
enum MethodFlags {
    METHOD_FLAG_NORMAL=1,
    METHOD_FLAG_EDITOR=2,
    METHOD_FLAG_NOSCRIPT=4,
    METHOD_FLAG_CONST=8,
    METHOD_FLAG_REVERSE=16, // used for events
    METHOD_FLAG_VIRTUAL=32,
    METHOD_FLAG_FROM_SCRIPT=64,
    METHOD_FLAG_VARARG=128,
    METHOD_FLAGS_DEFAULT=METHOD_FLAG_NORMAL,
};
CFFI_DLLEXPORT PyObject *instanciate_binding_from_godot_obj(PyObject *py_cls, godot_object *godot_obj);
CFFI_DLLEXPORT void py_instance_set_godot_obj(PyObject *py_instance, godot_object *godot_obj);
CFFI_DLLEXPORT PyObject *variants_to_pyobjs(void **args, int argcount);
CFFI_DLLEXPORT PyObject *variant_to_pyobj2(void *arg);
""")

with open(BASEDIR + '/mod_godot.inc.py', 'r') as fd:
    godot_module = fd.read()
with open(BASEDIR + '/tools.inc.py', 'r') as fd:
    tools = fd.read()
with open(BASEDIR + '/mod_godot_bindings.inc.py', 'r') as fd:
    godot_bindings_module = fd.read()

ffibuilder.embedding_init_code("""
print('============> INIT CFFI <===========')

from pythonscriptcffi import ffi, lib

@ffi.def_extern()
def do_stuff(x, y):
    return x + y

@ffi.def_extern()
def py_instance_set_godot_obj(instance_handle, godot_obj):
    self = ffi.from_handle(ffi.cast('void*', instance_handle))
    print('** %s switched from %s to %s' % (self, self._gd_obj, godot_obj))
    self._gd_obj = godot_obj


# TODO: find a cleaner way to prevent the newly initialized binding from beeing
# garbage collected as soon as we leave the function
newly_intanciated_anchor = []
@ffi.def_extern()
def instanciate_binding_from_godot_obj(py_cls_handle, godot_obj):
    global newly_intanciated_anchor
    py_cls = ffi.from_handle(ffi.cast('void*', py_cls_handle))
    instance = py_cls(godot_obj)
    instance_handle = ffi.new_handle(instance)
    newly_intanciated_anchor.append((instance, instance_handle))
    return instance_handle


@ffi.def_extern()
def variant_to_pyobj2(v):
    global newly_intanciated_anchor
    instance = variant_to_pyobj(v)
    instance_handle = ffi.new_handle(instance)
    newly_intanciated_anchor.append((instance, instance_handle))
    return instance_handle


@ffi.def_extern()
def variants_to_pyobjs(args, argcount):
    return [variant_to_pyobj(args[i]) for i in range(argcount)]


""" + tools + godot_module + godot_bindings_module + """

""")

# with open(BASEDIR + "../../modules/dlscript/godot.h", 'r') as fd:
#     ffibuilder.cdef()
ffibuilder.cdef("""
// TODO: not in ldscript headers ?
enum MethodFlags {
    METHOD_FLAG_NORMAL=1,
    METHOD_FLAG_EDITOR=2,
    METHOD_FLAG_NOSCRIPT=4,
    METHOD_FLAG_CONST=8,
    METHOD_FLAG_REVERSE=16, // used for events
    METHOD_FLAG_VIRTUAL=32,
    METHOD_FLAG_FROM_SCRIPT=64,
    METHOD_FLAG_VARARG=128,
    METHOD_FLAGS_DEFAULT=METHOD_FLAG_NORMAL,
};


// Atomic types
typedef bool godot_bool;
typedef int godot_int;
typedef float godot_real;
typedef double godot_real64; // for Variant in 3.0
typedef void godot_object;

// Method binds
typedef struct godot_method_bind {
    uint8_t _dont_touch_that[1]; // TODO
} godot_method_bind;

godot_method_bind *godot_method_bind_get_method(const char *p_classname, const char *p_methodname);
void godot_method_bind_ptrcall(godot_method_bind *p_method_bind, godot_object *p_instance, const void **p_args, void *p_ret);

godot_object *godot_global_get_singleton(char *p_name); // result shouldn't be freed

// TODO remove this custom stuff
// char **godot_get_class_list();
// typedef godot_object *(*godot_class_constructor)();
// godot_class_constructor godot_get_class_constructor(const char *p_classname);
// const char **godot_get_class_methods(const char *p_classname);
// const char **godot_get_class_constants(const char *p_classname);
// const char **godot_get_class_properties(const char *p_classname);
// const char *godot_get_class_parent(const char *p_classname);


typedef float godot_real;
typedef double godot_real64;

// vector2
typedef struct godot_vector2 {
    uint8_t _dont_touch_that[8];
} godot_vector2;
void godot_vector2_new(godot_vector2 *p_v, const godot_real p_x, const godot_real p_y);
void godot_vector2_set_x(godot_vector2 *p_v, const godot_real p_x);
void godot_vector2_set_y(godot_vector2 *p_v, const godot_real p_y);
godot_real godot_vector2_get_x(const godot_vector2 *p_v);
godot_real godot_vector2_get_y(const godot_vector2 *p_v);
void godot_vector2_normalize(godot_vector2 *p_v);
void godot_vector2_normalized(godot_vector2 *p_dest, const godot_vector2 *p_src);
godot_real godot_vector2_length(const godot_vector2 *p_v);
godot_real godot_vector2_length_squared(const godot_vector2 *p_v);
godot_real godot_vector2_distance_to(const godot_vector2 *p_a, const godot_vector2 *p_b);
godot_real godot_vector2_distance_squared_to(const godot_vector2 *p_a, const godot_vector2 *p_b);

// godot_string.h
typedef struct godot_string {
    uint8_t _dont_touch_that[8];
} godot_string;
void godot_string_new(godot_string *p_str);
void godot_string_new_data(godot_string *p_str, const char *p_contents, const int p_size);
void godot_string_get_data(const godot_string *p_str, wchar_t *p_dest, int *p_size);
void godot_string_copy_string(const godot_string *p_dest, const godot_string *p_src);
wchar_t *godot_string_operator_index(godot_string *p_str, const godot_int p_idx);
const wchar_t *godot_string_c_str(const godot_string *p_str);
godot_bool godot_string_operator_equal(const godot_string *p_a, const godot_string *p_b);
godot_bool godot_string_operator_less(const godot_string *p_a, const godot_string *p_b);
void godot_string_operator_plus(godot_string *p_dest, const godot_string *p_a, const godot_string *p_b);


// godot_variant.h
typedef struct godot_variant {
    uint8_t _dont_touch_that[24];
} godot_variant;
enum godot_variant_type {
    GODOT_VARIANT_TYPE_NIL,

    // atomic types
    GODOT_VARIANT_TYPE_BOOL,
    GODOT_VARIANT_TYPE_INT,
    GODOT_VARIANT_TYPE_REAL,
    GODOT_VARIANT_TYPE_STRING,

    // math types

    GODOT_VARIANT_TYPE_VECTOR2,     // 5
    GODOT_VARIANT_TYPE_RECT2,
    GODOT_VARIANT_TYPE_VECTOR3,
    GODOT_VARIANT_TYPE_TRANSFORM2D,
    GODOT_VARIANT_TYPE_PLANE,
    GODOT_VARIANT_TYPE_QUAT,            // 10
    GODOT_VARIANT_TYPE_RECT3, //sorry naming convention fail :( not like it's used often
    GODOT_VARIANT_TYPE_BASIS,
    GODOT_VARIANT_TYPE_TRANSFORM,

    // misc types
    GODOT_VARIANT_TYPE_COLOR,
    GODOT_VARIANT_TYPE_IMAGE,           // 15
    GODOT_VARIANT_TYPE_NODE_PATH,
    GODOT_VARIANT_TYPE_RID,
    GODOT_VARIANT_TYPE_OBJECT,
    GODOT_VARIANT_TYPE_INPUT_EVENT,
    GODOT_VARIANT_TYPE_DICTIONARY,      // 20
    GODOT_VARIANT_TYPE_ARRAY,

    // arrays
    GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY,
    GODOT_VARIANT_TYPE_POOL_INT_ARRAY,
    GODOT_VARIANT_TYPE_POOL_REAL_ARRAY,
    GODOT_VARIANT_TYPE_POOL_STRING_ARRAY,   // 25
    GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY,
    GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY,
    GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY,
};
typedef enum godot_variant_type godot_variant_type;


// godot_array.h
typedef struct godot_array {
    uint8_t _dont_touch_that[8];
} godot_array;
void godot_array_set(godot_array *p_arr, const godot_int p_idx, const godot_variant *p_value);
godot_variant *godot_array_get(godot_array *p_arr, const godot_int p_idx);
void godot_array_append(godot_array *p_arr, const godot_variant *p_value);
void godot_array_clear(godot_array *p_arr);
godot_int godot_array_count(godot_array *p_arr, const godot_variant *p_value);
godot_bool godot_array_empty(const godot_array *p_arr);
void godot_array_erase(godot_array *p_arr, const godot_variant *p_value);
godot_variant godot_array_front(const godot_array *p_arr);
godot_variant godot_array_back(const godot_array *p_arr);
godot_int godot_array_find(const godot_array *p_arr, const godot_variant *p_what, const godot_int p_from);
godot_int godot_array_find_last(const godot_array *p_arr, const godot_variant *p_what);
godot_bool godot_array_has(const godot_array *p_arr,const  godot_variant *p_value);
uint32_t godot_array_hash(const godot_array *p_arr);
void godot_array_insert(godot_array *p_arr, const godot_int p_pos, const godot_variant *p_value);
void godot_array_invert(godot_array *p_arr);
godot_bool godot_array_is_shared(const godot_array *p_arr);
godot_variant godot_array_pop_back(godot_array *p_arr);
godot_variant godot_array_pop_front(godot_array *p_arr);
void godot_array_push_back(godot_array *p_arr, const godot_variant *p_value);
void godot_array_push_front(godot_array *p_arr, const godot_variant *p_value);
void godot_array_remove(godot_array *p_arr, const godot_int p_idx);
void godot_array_resize(godot_array *p_arr, const godot_int p_size);
godot_int godot_array_rfind(const godot_array *p_arr, const godot_variant *p_what, const godot_int p_from);
godot_int godot_array_size(const godot_array *p_arr);
void godot_array_sort(godot_array *p_arr);
void godot_array_sort_custom(godot_array *p_arr, godot_object *p_obj, const godot_string *p_func);
void godot_array_destroy(godot_array *p_arr);


// godot_pool_arrays.h -- string array
typedef struct godot_pool_string_array {
    uint8_t _dont_touch_that[8];
} godot_pool_string_array;
void godot_pool_string_array_new(godot_pool_string_array *p_psa);
void godot_pool_string_array_new_with_array(godot_pool_string_array *p_psa, const godot_array *p_a);
void godot_pool_string_array_append(godot_pool_string_array *p_psa, const godot_string *p_data);
void godot_pool_string_array_append_array(godot_pool_string_array *p_psa, const godot_pool_string_array *p_array);
int godot_pool_string_array_insert(godot_pool_string_array *p_psa, const godot_int p_idx, const godot_string *p_data);
void godot_pool_string_array_invert(godot_pool_string_array *p_psa);
void godot_pool_string_array_push_back(godot_pool_string_array *p_psa, const godot_string *p_data);
void godot_pool_string_array_remove(godot_pool_string_array *p_psa, const godot_int p_idx);
void godot_pool_string_array_resize(godot_pool_string_array *p_psa, const godot_int p_size);
void godot_pool_string_array_set(godot_pool_string_array *p_psa, const godot_int p_idx, const godot_string *p_data);
godot_string godot_pool_string_array_get(godot_pool_string_array *p_psa, const godot_int p_idx);
godot_int godot_pool_string_array_size(godot_pool_string_array *p_psa);
void godot_pool_string_array_destroy(godot_pool_string_array *p_psa);

// godot_dictionary.h
typedef struct godot_dictionary {
    uint8_t _dont_touch_that[8];
} godot_dictionary;
void godot_dictionary_new(godot_dictionary *p_dict);
void godot_dictionary_clear(godot_dictionary *p_dict);
godot_bool godot_dictionary_empty(const godot_dictionary *p_dict);
void godot_dictionary_erase(godot_dictionary *p_dict, const godot_variant *p_key);
godot_bool godot_dictionary_has(const godot_dictionary *p_dict, const godot_variant *p_key);
godot_bool godot_dictionary_has_all(const godot_dictionary *p_dict, const godot_array *p_keys);
uint32_t godot_dictionary_hash(const godot_dictionary *p_dict);
godot_array godot_dictionary_keys(const godot_dictionary *p_dict);
godot_int godot_dictionary_parse_json(godot_dictionary *p_dict, const godot_string *p_json);
godot_variant *godot_dictionary_operator_index(godot_dictionary *p_dict, const godot_variant *p_key);
godot_int godot_dictionary_size(const godot_dictionary *p_dict);
godot_string godot_dictionary_to_json(const godot_dictionary *p_dict);
godot_array godot_dictionary_values(const godot_dictionary *p_dict);
void godot_dictionary_destroy(godot_dictionary *p_dict);


godot_variant_type godot_variant_get_type(const godot_variant *p_v);
void godot_variant_copy(godot_variant *p_dest, const godot_variant *p_src);
void godot_variant_new_nil(godot_variant *p_v);
void godot_variant_new_bool(godot_variant *p_v, const godot_bool p_b);
void godot_variant_new_int(godot_variant *p_v, const uint64_t p_i);
void godot_variant_new_real(godot_variant *p_v, const double p_r);
void godot_variant_new_string(godot_variant *p_v, const godot_string *p_s);
// void godot_variant_new_vector2(godot_variant *p_v, const godot_vector2 *p_v2);
// void godot_variant_new_rect2(godot_variant *p_v, const godot_rect2 *p_rect2);
// void godot_variant_new_vector3(godot_variant *p_v, const godot_vector3 *p_v3);
// void godot_variant_new_transform2d(godot_variant *p_v, const godot_transform2d *p_t2d);
// void godot_variant_new_plane(godot_variant *p_v, const godot_plane *p_plane);
// void godot_variant_new_quat(godot_variant *p_v, const godot_quat *p_quat);
// void godot_variant_new_rect3(godot_variant *p_v, const godot_rect3 *p_rect3);
// void godot_variant_new_basis(godot_variant *p_v, const godot_basis *p_basis);
// void godot_variant_new_transform(godot_variant *p_v, const godot_transform *p_trans);
// void godot_variant_new_color(godot_variant *p_v, const godot_color *p_color);
// void godot_variant_new_image(godot_variant *p_v, const godot_image *p_img);
// void godot_variant_new_node_path(godot_variant *p_v, const godot_node_path *p_np);
// void godot_variant_new_rid(godot_variant *p_v, const godot_rid *p_rid);
// void godot_variant_new_object(godot_variant *p_v, const godot_object *p_obj);
// void godot_variant_new_input_event(godot_variant *p_v, const godot_input_event *p_event);
// void godot_variant_new_dictionary(godot_variant *p_v, const godot_dictionary *p_dict);
// void godot_variant_new_array(godot_variant *p_v, const godot_array *p_arr);
// void godot_variant_new_pool_byte_array(godot_variant *p_v, const godot_pool_byte_array *p_pba);
// void godot_variant_new_pool_int_array(godot_variant *p_v, const godot_pool_int_array *p_pia);
// void godot_variant_new_pool_real_array(godot_variant *p_v, const godot_pool_real_array *p_pra);
// void godot_variant_new_pool_string_array(godot_variant *p_v, const godot_pool_string_array *p_psa);
// void godot_variant_new_pool_vector2_array(godot_variant *p_v, const godot_pool_vector2_array *p_pv2a);
// void godot_variant_new_pool_vector3_array(godot_variant *p_v, const godot_pool_vector3_array *p_pv3a);
// void godot_variant_new_pool_color_array(godot_variant *p_v, const godot_pool_color_array *p_pca);
godot_bool godot_variant_as_bool(const godot_variant *p_v);
uint64_t godot_variant_as_int(const godot_variant *p_v);
godot_real godot_variant_as_real(const godot_variant *p_v);
godot_string godot_variant_as_string(const godot_variant *p_v);
// godot_vector2 godot_variant_as_vector2(const godot_variant *p_v);
// godot_rect2 godot_variant_as_rect2(const godot_variant *p_v);
// godot_vector3 godot_variant_as_vector3(const godot_variant *p_v);
// godot_transform2d godot_variant_as_transform2d(const godot_variant *p_v);
// godot_plane godot_variant_as_plane(const godot_variant *p_v);
// godot_quat godot_variant_as_quat(const godot_variant *p_v);
// godot_rect3 godot_variant_as_rect3(const godot_variant *p_v);
// godot_basis godot_variant_as_basis(const godot_variant *p_v);
// godot_transform godot_variant_as_transform(const godot_variant *p_v);
// godot_color godot_variant_as_color(const godot_variant *p_v);
// godot_image godot_variant_as_image(const godot_variant *p_v);
// godot_node_path godot_variant_as_node_path(const godot_variant *p_v);
// godot_rid godot_variant_as_rid(const godot_variant *p_v);
// godot_object *godot_variant_as_object(const godot_variant *p_v);
// godot_input_event godot_variant_as_input_event(const godot_variant *p_v);
godot_dictionary godot_variant_as_dictionary(const godot_variant *p_v);
godot_array godot_variant_as_array(const godot_variant *p_v);
// godot_pool_byte_array godot_variant_as_pool_byte_array(const godot_variant *p_v);
// godot_pool_int_array godot_variant_as_pool_int_array(const godot_variant *p_v);
// godot_pool_real_array godot_variant_as_pool_real_array(const godot_variant *p_v);
// godot_pool_string_array godot_variant_as_pool_string_array(const godot_variant *p_v);
// godot_pool_vector2_array godot_variant_as_pool_vector2_array(const godot_variant *p_v);
// godot_pool_vector3_array godot_variant_as_pool_vector3_array(const godot_variant *p_v);
// godot_pool_color_array godot_variant_as_pool_color_array(const godot_variant *p_v);
godot_variant godot_variant_call(godot_variant *p_v, const godot_string *p_method, const godot_variant **p_args, const godot_int p_argcount /*, godot_variant_call_error *r_error */);
godot_bool godot_variant_has_method(godot_variant *p_v, const godot_string *p_method);
godot_bool godot_variant_operator_equal(const godot_variant *p_a, const godot_variant *p_b);
godot_bool godot_variant_operator_less(const godot_variant *p_a, const godot_variant *p_b);
godot_bool godot_variant_hash_compare(const godot_variant *p_a, const godot_variant *p_b);
godot_bool godot_variant_booleanize(const godot_variant *p_v, godot_bool *p_valid);
void godot_variant_destroy(godot_variant *p_v);

""")

# ffibuilder.compile(target="pythonscriptcffi.*", verbose=True)
ffibuilder.emit_c_code(BASEDIR + "/pythonscriptcffi.cpp")
