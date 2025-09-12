cdef object RESOURCE_TYPE_NAME = "PythonScript"
cdef object RESOURCE_EXTENSIONS = ("py", "pyc", "pyo", "pyd")


# godot_extension: class(parent="ResourceFormatLoader")
@cython.final
cdef class PythonResourceFormatLoader:
    cdef gd_object_t _gd_ptr

    # Don't overload `_exists()`, so Godot default to checking file existence

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_dependencies(self, gd_string_t path, gd_bool_t add_types):
        cdef gd_packed_string_array_t dependencies = gd_packed_string_array_new()
        cdef object py_path = gdapi.gd_string_to_pystr(&path)
        gd_string_del(&path)

        spy_log(f"CALLED PythonResourceFormatLoader::_get_dependencies(path={py_path}, add_types={add_types})")

        # For Python scripts, we could analyze imports to find dependencies
        # For now, return empty dependencies as most Python scripts don't have
        # Godot resource dependencies that need tracking
        try:
            with open(py_path, 'r', encoding='utf-8') as f:
                source = f.read()
            # TODO: Parse imports and find Godot resource dependencies
            # This would involve parsing "from godot import" statements and
            # potentially resource load calls like ResourceLoader.load()
        except:
            pass  # File doesn't exist or can't be read

        return dependencies

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self):
        spy_log("CALLED PythonResourceFormatLoader::_get_recognized_extensions()")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in RESOURCE_EXTENSIONS:
            extension = gd_string_from_unchecked_pystr(py_extension)
            gd_packed_string_array_meth_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # Don't overload `_get_classes_used()` to mimic GDScript
    # Don't overload `_get_resource_script_class()` to mimic GDScript
    # Don't overload `_get_resource_uid()` to mimic GDScript

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _handles_type(self, gd_string_name_t type):
        cdef gd_string_t candidate
        cdef gd_bool_t ret = False

        spy_log(f"CALLED PythonResourceFormatLoader::_handles_type(type={gdapi.gd_string_name_to_pystr(&type)!r})")

        candidate = gd_string_from_unchecked_pystr(RESOURCE_TYPE_NAME)
        ret = gd_string_name_op_equal_string(&type, &candidate)
        gd_string_del(&candidate)
        if not ret:
            candidate = gd_string_from_pybytes(b"Script")
            ret = gd_string_name_op_equal_string(&type, &candidate)
            gd_string_del(&candidate)

        gd_string_name_del(&type)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_resource_type(self, gd_string_t path):
        cdef object py_path
        cdef object py_extension

        py_path = gdapi.gd_string_to_pystr(&path)
        gd_string_del(&path)

        spy_log(f"CALLED PythonResourceFormatLoader::_get_resource_type(path={py_path!r})")

        py_extension = py_path.rsplit(".", 1)[-1].lower()
        if py_extension in RESOURCE_EXTENSIONS:
            return gd_string_from_unchecked_pystr(RESOURCE_TYPE_NAME)
        else:
            return gd_string_from_unchecked_pystr("")  # Empty string for unknown types

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _load(self, gd_string_t path, gd_string_t original_path, gd_bool_t use_sub_threads, gd_int_t cache_mode):
        cdef gd_variant_t ret = gd_variant_new()
        cdef object py_path = gdapi.gd_string_to_pystr(&path)
        cdef object py_original_path = gdapi.gd_string_to_pystr(&original_path)
        gd_string_del(&path)
        gd_string_del(&original_path)
        spy_log(f"CALLED PythonResourceFormatLoader::_load(path={py_path!r}, original_path={py_original_path!r}, use_sub_threads={use_sub_threads}, cache_mode={cache_mode})")

        cdef PythonScript script
        cdef gd_string_t gd_source
        cdef gd_string_t gd_script_path
        cdef GDString source_code

        # Load the source code from file

        from godot.classes import FileAccess
        # TODO: use `path` directly !
        cdef object file = FileAccess.open(GDString(py_path), FileAccess.ModeFlags.READ.value)
        if file is None:
            spy_log(f"Failed to load Python script {py_original_path}: cannot open file {path}")
            # If file loading fails, return the nil variant (already initialized)
            return ret
        # TODO: what happen if the text is not UTF8 ?
        source_code = file.get_as_text()

        # Create a new script instance from the source code

        script = PythonScript()
        script._set_source_code(source_code.into_gd_data())
        # `into_gd_data()` steal the underlying Godot string, so `source_code`
        # ends up containing nothing and we'd rather destroy it early to avoid
        # confusions.
        del source_code

        # Return the script as a variant

        # Note it's okay to steal `scripts`'s Godot object pointer like this,
        # since the Godot object itself controls the lifetime of `script` (i.e.
        # `script` is not going to be destroyed when this function finishes).
        ret = gd_object_into_variant(script._gd_ptr)
        return ret

    # Don't overload `_rename_dependencies()` to mimic GDScript

    # Don't overload `_recognize_path()`, so Godot instead relies on `_get_recognized_extensions()` & `_get_resource_type()`

    # godot_extension: generate_class_code()


# godot_extension: generate_module_code()
