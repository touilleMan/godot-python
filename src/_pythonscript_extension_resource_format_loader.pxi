from godot.classes cimport ScriptLanguageExtensionProfilingInfo


cdef gd_string_name_t gdname_resourceformatloader
cdef gd_string_name_t gdname_pythonresourceformatloader


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

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _exists(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_exists")
        gd_string_del(&path)
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_classes_used(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_classes_used")
        gd_string_del(&path)
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_dependencies(self, gd_string_t path, gd_bool_t add_types):
        spy_log("CALLED PythonResourceFormatLoader::_get_dependencies")
        gd_string_del(&path)
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self):
        spy_log("CALLED PythonResourceFormatLoader::_get_recognized_extensions")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"py", b"pyc", b"pyo", b"pyd"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_resource_script_class(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_resource_script_class")
        gd_string_del(&path)
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _get_resource_uid(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_resource_uid")
        gd_string_del(&path)
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _handles_type(self, gd_string_name_t type):
        cdef gd_string_t candidate
        cdef gd_bool_t ret = False
        spy_log("CALLED PythonResourceFormatLoader::_handles_type")

        candidate = gd_string_from_pybytes("PythonScript")
        ret = gd_string_op_equal_string(&type, &candidate)
        gd_string_name_del(&candidate)
        if not ret:
            candidate = gd_string_from_pybytes("Script")
            ret = gd_string_op_equal_string(&type, &candidate)
            gd_string_name_del(&candidate)

        gd_string_name_del(&type)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_resource_type(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_resource_type")
        gd_string_del(&path)
        pass
    TODO!!!!!!!!!!!!!!!!!!!!!
    #	String el = p_path.get_extension().to_lower();
    #	if (el == "gd" || el == "gdc") {
    #		return "GDScript";
    #	}
    #	return "";

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _load(self, gd_string_t path, gd_string_t original_path, gd_bool_t use_sub_threads, gd_int_t cache_mode):
        spy_log("CALLED PythonResourceFormatLoader::_load")
        gd_string_del(&path)
        gd_string_del(&original_path)
        pass

    # Don't overload `_recognize_path()`, so Godot instead relies on `_get_recognized_extensions()` & `_get_resource_type()`

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _rename_dependencies(self, gd_string_t path, gd_dictionary_t renames):
        spy_log("CALLED PythonResourceFormatLoader::_rename_dependencies")
        gd_string_del(&path)
        gd_dictionary_del(&renames)
        return Error.ERR_UNAVAILABLE
