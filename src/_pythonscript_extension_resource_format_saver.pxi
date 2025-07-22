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
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in ("py", "pyc", "pyo", "pyd"):
            extension = gd_string_from_unchecked_pystr(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _recognize(self, gd_object_t resource):
        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_recognize")

        # Get the class name of the resource
        cdef gd_string_name_t class_name
        cdef gd_string_t py_script_name
        cdef gd_string_t script_name
        cdef gd_bool_t is_python_script
        cdef gd_bool_t result = pythonscript_gdextension.object_get_class_name(
            resource,
            pythonscript_gdextension_library,
            &class_name
        )

        if not result:
            return False

        # Check if this is a PythonScript
        py_script_name = gd_string_from_unchecked_pystr("PythonScript")
        is_python_script = gd_string_name_op_equal_string(&class_name, &py_script_name)
        gd_string_del(&py_script_name)

        # Also check for generic "Script" class
        if not is_python_script:
            script_name = gd_string_from_pybytes(b"Script")
            is_python_script = gd_string_name_op_equal_string(&class_name, &script_name)
            gd_string_del(&script_name)

        gd_string_name_del(&class_name)
        return is_python_script

    # Don't overload `_recognize_path()` to mimic GDScript

    # godot_extension: method(virtual=True)
    cdef gd_int_t _save(self, gd_object_t resource, gd_string_t path, gd_int_t flags):
        # `resource` is an instance of `Resource`
        spy_log("CALLED PythonResourceFormatSaver::_save")

        # Convert the path to a Python string
        cdef object py_path = gd_string_to_pystr(&path)
        gd_string_del(&path)

        # For now, just write a simple placeholder file
        # TODO: Once PythonScript._get_source_code() is properly implemented,
        # we can call it directly here to get the actual source code

        try:
            with open(py_path, 'w', encoding='utf-8') as f:
                f.write("# Python script saved from Godot\n")
            return Error.OK
        except:
            return Error.ERR_FILE_CANT_OPEN

    # Don't overload `_set_uid()` to mimic GDScript
