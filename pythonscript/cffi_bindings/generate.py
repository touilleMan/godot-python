import cffi
import os


BASEDIR = os.path.dirname(os.path.abspath(__file__))

ffibuilder = cffi.FFI()

ffibuilder.embedding_api(r"""
    typedef struct { ...; } PyObject;
    typedef void godot_object;
    int do_stuff(int, int);
    void py_instance_set_godot_obj(PyObject *py_instance, godot_object *godot_obj);
""")

ffibuilder.set_source("pythonscriptcffi", """
#include "Include/Python.h"
#include "modules/dlscript/godot.h"
""")

with open(BASEDIR + '/mod_godot.py', 'r') as fd:
    godot_module = fd.read()
with open(BASEDIR + '/mod_godot_bindings.py', 'r') as fd:
    godot_bindings_module = fd.read()

ffibuilder.embedding_init_code("""
print('============> INIT CFFI <===========')
import os
import sys
import imp

from pythonscriptcffi import ffi, lib

""" + godot_module + godot_bindings_module + """

@ffi.def_extern()
def do_stuff(x, y):
    return x + y

@ffi.def_extern()
def py_instance_set_godot_obj(instance_handle, godot_obj):
    self = ffi.from_handle(ffi.cast('void*', instance_handle))
    print('** %s switched from %s to %s' % (self, self._gd_obj, godot_obj))
    self._gd_obj = godot_obj
""")

# with open(BASEDIR + "../../modules/dlscript/godot.h", 'r') as fd:
#     ffibuilder.cdef()
ffibuilder.cdef("""
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
char **godot_get_class_list();
typedef godot_object *(*godot_class_constructor)();
godot_class_constructor godot_get_class_constructor(const char *p_classname);
const char **godot_get_class_methods(const char *p_classname);
const char **godot_get_class_constants(const char *p_classname);
const char **godot_get_class_properties(const char *p_classname);
const char *godot_get_class_parent(const char *p_classname);


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


godot_string godot_variant_as_string(const godot_variant *p_v);
godot_dictionary godot_variant_as_dictionary(const godot_variant *p_v);
""")

# ffibuilder.compile(target="pythonscriptcffi.*", verbose=True)
ffibuilder.emit_c_code(BASEDIR + "/pythonscriptcffi.cpp")
