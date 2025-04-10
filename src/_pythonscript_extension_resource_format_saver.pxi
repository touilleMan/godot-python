from godot.classes cimport ScriptLanguageExtensionProfilingInfo


cdef gd_string_name_t gdname_resourceformatsaver
cdef gd_string_name_t gdname_pythonresourceformatsaver


# godot_extension: class(parent="ResourceFormatSaver")
@cython.final
cdef class PythonResourceFormatSaver:
    cdef gd_object_t _gd_ptr

    def __cinit__(self):
        self._gd_ptr = pythonscript_gdextension.classdb_construct_object(&gdname_resourceformatsaver)
        pythonscript_gdextension.object_set_instance(self._gd_ptr, &gdname_pythonresourceformatsaver, <PyObject*>self)

    # godot_extension: register_class_hook()
    @staticmethod
    cdef inline void _register_class_hook():
        global gdname_resourceformatsaver, gdname_pythonresourceformatsaver
        gdname_resourceformatsaver = gd_string_name_from_unchecked_pystr("ResourceFormatSaver")
        gdname_pythonresourceformatsaver = gd_string_name_from_unchecked_pystr("PythonResourceFormatSaver")

    # godot_extension: unregister_class_hook()
    @staticmethod
    cdef inline void _unregister_class_hook():
        global gdname_resourceformatsaver, gdname_pythonresourceformatsaver
        gd_string_name_del(&gdname_resourceformatsaver)
        gd_string_name_del(&gdname_pythonresourceformatsaver)

    # godot_extension: generate_code()

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self, gd_object_t resource):
        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_get_recognized_extensions")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _recognize(self, gd_object_t resource):
        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_recognize")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _recognize_path(self, gd_object_t resource, gd_string_t path):
        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_recognize_path")
        gd_string_del(&path)
        pass

    # godot_extension: method(virtual=True)
    cdef gd_int_t _save(self, gd_object_t resource, gd_string_t path, gd_int_t flags):
        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_save")
        gd_string_del(&path)
        return Error.ERR_UNAVAILABLE

    # godot_extension: method(virtual=True)
    cdef gd_int_t _set_uid(self, gd_string_t path, gd_int_t uid):
        spy_log("CALLED PythonResourceFormatSaver::_set_uid")
        gd_string_del(&path)
        return Error.ERR_UNAVAILABLE