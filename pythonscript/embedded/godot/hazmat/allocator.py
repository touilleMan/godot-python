from functools import partial

from pythonscriptcffi import ffi, lib


def alloc_with_destructor_factory(type, constructor, destructor):

    def free(data):
        destructor(data)
        lib.free(data)

    allocator = ffi.new_allocator(
        alloc=lib.malloc, free=free, should_clear_after_alloc=False
    )

    def alloc(initialized=True):
        """
        /!\ With `initialized=False`, you must use `lib.godot_*_new` on the
        result otherwise strange things will happened when destructor kicks in /!\
        """
        data = allocator(type)
        if initialized:
            constructor(data)
        return data

    alloc.allocator = allocator
    return alloc


# Simplest types
godot_bool_alloc = partial(ffi.new, "godot_bool*")
godot_int_alloc = partial(ffi.new, "godot_int*")
godot_real_alloc = partial(ffi.new, "godot_real*")
godot_object_alloc = partial(ffi.new, "godot_object**")
# Allocation of struct with no destructor
godot_vector3_alloc = partial(ffi.new, "godot_vector3*")
godot_vector2_alloc = partial(ffi.new, "godot_vector2*")
godot_transform2d_alloc = partial(ffi.new, "godot_transform2d*")
godot_transform_alloc = partial(ffi.new, "godot_transform*")
godot_rid_alloc = partial(ffi.new, "godot_rid*")
godot_aabb_alloc = partial(ffi.new, "godot_aabb*")
godot_rect2_alloc = partial(ffi.new, "godot_rect2*")
godot_quat_alloc = partial(ffi.new, "godot_quat*")
godot_plane_alloc = partial(ffi.new, "godot_plane*")
godot_color_alloc = partial(ffi.new, "godot_color*")
godot_basis_alloc = partial(ffi.new, "godot_basis*")
# Use a custom memory allocator to handle destructors
godot_variant_alloc = alloc_with_destructor_factory(
    "godot_variant*", lib.godot_variant_new_nil, lib.godot_variant_destroy
)
godot_string_alloc = alloc_with_destructor_factory(
    "godot_string*", lib.godot_string_new, lib.godot_string_destroy
)
godot_node_path_alloc = alloc_with_destructor_factory(
    "godot_node_path*",
    lambda data, path=godot_string_alloc(): lib.godot_node_path_new(data, path),
    lib.godot_node_path_destroy,
)
godot_dictionary_alloc = alloc_with_destructor_factory(
    "godot_dictionary*", lib.godot_dictionary_new, lib.godot_dictionary_destroy
)
godot_array_alloc = alloc_with_destructor_factory(
    "godot_array*", lib.godot_array_new, lib.godot_array_destroy
)
godot_pool_byte_array_alloc = alloc_with_destructor_factory(
    "godot_pool_byte_array*",
    lib.godot_pool_byte_array_new,
    lib.godot_pool_byte_array_destroy,
)
godot_pool_int_array_alloc = alloc_with_destructor_factory(
    "godot_pool_int_array*",
    lib.godot_pool_int_array_new,
    lib.godot_pool_int_array_destroy,
)
godot_pool_real_array_alloc = alloc_with_destructor_factory(
    "godot_pool_real_array*",
    lib.godot_pool_real_array_new,
    lib.godot_pool_real_array_destroy,
)
godot_pool_string_array_alloc = alloc_with_destructor_factory(
    "godot_pool_string_array*",
    lib.godot_pool_string_array_new,
    lib.godot_pool_string_array_destroy,
)
godot_pool_color_array_alloc = alloc_with_destructor_factory(
    "godot_pool_color_array*",
    lib.godot_pool_color_array_new,
    lib.godot_pool_color_array_destroy,
)
godot_pool_vector2_array_alloc = alloc_with_destructor_factory(
    "godot_pool_vector2_array*",
    lib.godot_pool_vector2_array_new,
    lib.godot_pool_vector2_array_destroy,
)
godot_pool_vector3_array_alloc = alloc_with_destructor_factory(
    "godot_pool_vector3_array*",
    lib.godot_pool_vector3_array_new,
    lib.godot_pool_vector3_array_destroy,
)
