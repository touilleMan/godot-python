from godot.classes cimport ScriptLanguageExtensionProfilingInfo


cdef gd_string_name_t gdname_resourceformatloader
cdef gd_string_name_t gdname_pythonresourceformatloader
cdef object RESOURCE_TYPE_NAME = "PythonScript"
cdef object RESOURCE_EXTENSIONS = ("py", "pyc", "pyo", "pyd")

# godot_extension: class(parent="ResourceFormatLoader")
@cython.final
cdef class PythonResourceFormatLoader:
    cdef gd_object_t _gd_ptr

    def __cinit__(self):
        self._gd_ptr = pythonscript_gdextension.classdb_construct_object(&gdname_resourceformatloader)
        pythonscript_gdextension.object_set_instance(self._gd_ptr, &gdname_pythonresourceformatloader, <PyObject*>self)

    # godot_extension: register_class_hook()
    @staticmethod
    cdef inline void _register_class_hook():
        global gdname_resourceformatloader, gdname_pythonresourceformatloader
        gdname_resourceformatloader = gd_string_name_from_unchecked_pystr("ResourceFormatLoader")
        gdname_pythonresourceformatloader = gd_string_name_from_unchecked_pystr("PythonResourceFormatLoader")

    # godot_extension: unregister_class_hook()
    @staticmethod
    cdef inline void _unregister_class_hook():
        global gdname_resourceformatloader, gdname_pythonresourceformatloader
        gd_string_name_del(&gdname_resourceformatloader)
        gd_string_name_del(&gdname_pythonresourceformatloader)

    # godot_extension: generate_code()

    # Don't overload `_exists()`, so Godot default to checking file existence

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_dependencies(self, gd_string_t path, gd_bool_t add_types):
        # TODO
        cdef gd_packed_string_array_t dependencies = gd_packed_string_array_new()

        spy_log("CALLED PythonResourceFormatLoader::_get_dependencies")
        gd_string_del(&path)

        return dependencies

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self):
        spy_log("CALLED PythonResourceFormatLoader::_get_recognized_extensions")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in RESOURCE_EXTENSIONS:
            extension = gd_string_from_unchecked_pystr(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # Don't overload `_get_classes_used()` to mimic GDScript
    # Don't overload `_get_resource_script_class()` to mimic GDScript
    # Don't overload `_get_resource_uid()` to mimic GDScript

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _handles_type(self, gd_string_name_t type):
        cdef gd_string_t candidate
        cdef gd_bool_t ret = False

        spy_log("CALLED PythonResourceFormatLoader::_handles_type {type:r}")

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

        spy_log("CALLED PythonResourceFormatLoader::_get_resource_type")

        py_path = gd_string_to_pystr(&path)
        gd_string_del(&path)

        py_extension = py_path.rsplit(".", 1)[-1].lower()
        if py_extension in RESOURCE_EXTENSIONS:
            return gd_string_from_unchecked_pystr(RESOURCE_TYPE_NAME)
        else:
            return gd_string_from_unchecked_pystr("")  # Empty string for unknown types

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _load(self, gd_string_t path, gd_string_t original_path, gd_bool_t use_sub_threads, gd_int_t cache_mode):
        # TODO
        cdef gd_variant_t ret = gd_variant_new()

        spy_log("CALLED PythonResourceFormatLoader::_load")
        gd_string_del(&path)
        gd_string_del(&original_path)

        return ret

    # Don't overload `_rename_dependencies()` to mimic GDScript

    # Don't overload `_recognize_path()`, so Godot instead relies on `_get_recognized_extensions()` & `_get_resource_type()`
