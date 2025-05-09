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
        # TODO
        # `resource` is an instance of `Resource`

        spy_log("CALLED PythonResourceFormatSaver::_get_recognized_extensions")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        # cdef gd_string_t extension

        # for py_extension in RESOURCE_EXTENSIONS:
        #     extension = gd_string_from_unchecked_pystr(py_extension)
        #     gd_packed_string_array_append(&extensions, &extension)
        #     gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _recognize(self, gd_object_t resource):
        # TODO

        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_recognize")

        return False

    # Don't overload `_recognize_path()` to mimic GDScript

    # godot_extension: method(virtual=True)
    cdef gd_int_t _save(self, gd_object_t resource, gd_string_t path, gd_int_t flags):
        # TODO

        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_save")
        gd_string_del(&path)

        return Error.ERR_UNAVAILABLE

    # Don't overload `_set_uid()` to mimic GDScript
