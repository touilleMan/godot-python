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
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_classes_used(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_classes_used")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_dependencies(self, gd_string_t path, gd_bool_t add_types):
        spy_log("CALLED PythonResourceFormatLoader::_get_dependencies")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self):
        spy_log("CALLED PythonResourceFormatLoader::_get_recognized_extensions")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_resource_script_class(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_resource_script_class")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_resource_type(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_resource_type")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _get_resource_uid(self, gd_string_t path):
        spy_log("CALLED PythonResourceFormatLoader::_get_resource_uid")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _handles_type(self, gd_string_name_t type):
        spy_log("CALLED PythonResourceFormatLoader::_handles_type")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _load(self, gd_string_t path, gd_string_t original_path, gd_bool_t use_sub_threads, gd_int_t cache_mode):
        spy_log("CALLED PythonResourceFormatLoader::_load")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _recognize_path(self, gd_string_t path, gd_string_name_t type):
        spy_log("CALLED PythonResourceFormatLoader::_recognize_path")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _rename_dependencies(self, gd_string_t path, gd_dictionary_t renames):
        spy_log("CALLED PythonResourceFormatLoader::_rename_dependencies")
        return Error.ERR_UNAVAILABLE
