# godot_extension: class(parent="ScriptExtension")
@cython.final
cdef class PythonScript:
    cdef gd_object_t _gd_ptr

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _can_instantiate(self):
        spy_log("CALLED PythonScript::_can_instantiate()")
        return self._is_valid()

    # godot_extension: method(virtual=True)
    cdef gd_bool_t _editor_can_reload_from_file(self):
        spy_log("CALLED PythonScript::_editor_can_reload_from_file()")
        # Python scripts can be reloaded from file
        return True

    # godot_extension: method(virtual=True, const=True)
    cdef gd_object_t _get_base_script(self):
        spy_log("CALLED PythonScript::_get_base_script()")
        # For now, Python scripts don't have base scripts
        # This could be enhanced to support script inheritance
        return NULL

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_constants(self):
        spy_log("CALLED PythonScript::_get_constants()")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_documentation(self):
        spy_log("CALLED PythonScript::_get_documentation()")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_name_t _get_instance_base_type(self):
        spy_log("CALLED PythonScript::_get_instance_base_type()")
        # For Python scripts, the base type is typically Object or Node
        # This could be enhanced to parse the class definition
        return gd_string_name_from_pybytes(b"Object")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_object_t _get_language(self):
        spy_log("CALLED PythonScript::_get_language()")
        # Return the PythonScriptLanguage instance
        assert _pythons_script_language._gd_ptr != NULL
        return _pythons_script_language._gd_ptr

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _get_member_line(self, gd_string_name_t member):
        spy_log(f"CALLED PythonScript::_get_member_line(member={gdapi.gd_string_name_to_pystr(&member)!r})")

        # Convert string name to string, then to Python string
        cdef gd_string_t member_str = gdapi.gd_string_new_from_string_name(&member)
        cdef object py_member = gdapi.gd_string_to_pystr(&member_str)
        gd_string_del(&member_str)
        gd_string_name_del(&member)

        # Find the line where the member is defined
        if not self._source_code:
            return 0
        try:
            lines = self._source_code.split('\n')
            for i, line in enumerate(lines):
                if (line.strip().startswith(f'def {py_member}(') or
                    line.strip().startswith(f'{py_member} =') or
                    line.strip().startswith(f'self.{py_member}')):
                    return i + 1  # Line numbers are 1-based
        except:
            pass
        return 0

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_name_t _get_members(self):
        spy_log("CALLED PythonScript::_get_members()")
        # TODO
        cdef gd_string_name_t ret = gd_string_name_from_pybytes(b"")
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_method_info(self, gd_string_name_t method):
        spy_log(f"CALLED PythonScript::_get_method_info(method={gdapi.gd_string_name_to_pystr(&method)!r})")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_name_del(&method)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _get_property_default_value(self, gd_string_name_t property):
        spy_log(f"CALLED PythonScript::_get_property_default_value(property={gdapi.gd_string_name_to_pystr(&property)!r})")
        # TODO
        cdef gd_variant_t ret = gd_variant_new()
        gd_string_name_del(&property)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _get_rpc_config(self):
        spy_log("CALLED PythonScript::_get_rpc_config()")
        # TODO
        cdef gd_variant_t ret = gd_variant_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_script_method_list(self):
        spy_log("CALLED PythonScript::_get_script_method_list()")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_script_property_list(self):
        spy_log("CALLED PythonScript::_get_script_property_list()")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_script_signal_list(self):
        spy_log("CALLED PythonScript::_get_script_signal_list()")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # PythonScript instance variable to store source code
    cdef object _source_code

    def __init__(self):
        self._source_code = ""

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_source_code(self):
        spy_log("CALLED PythonScript::_get_source_code()")
        return gd_string_from_unchecked_pystr(self._source_code)

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_method(self, gd_string_name_t method):
        spy_log(f"CALLED PythonScript::_has_method(method={gdapi.gd_string_name_to_pystr(&method)!r})")
        # Convert string name to string, then to Python string
        cdef gd_string_t method_str = gdapi.gd_string_new_from_string_name(&method)
        cdef object py_method = gdapi.gd_string_to_pystr(&method_str)
        gd_string_del(&method_str)
        gd_string_name_del(&method)

        # Check if method exists in the Python source code
        if not self._source_code:
            return False
        try:
            # Simple check for method definition
            lines = self._source_code.split('\n')
            for line in lines:
                if line.strip().startswith(f'def {py_method}('):
                    return True
        except:
            pass
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_property_default_value(self, gd_string_name_t property):
        spy_log(f"CALLED PythonScript::_has_property_default_value(property={gdapi.gd_string_name_to_pystr(&property)!r})")
        # TODO
        gd_string_name_del(&property)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_script_signal(self, gd_string_name_t signal):
        spy_log(f"CALLED PythonScript::_has_script_signal(signal={gdapi.gd_string_name_to_pystr(&signal)!r})")
        # TODO
        gd_string_name_del(&signal)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_source_code(self):
        spy_log("CALLED PythonScript::_has_source_code()")
        return len(self._source_code) > 0

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _inherits_script(self, gd_object_t script):
        spy_log(f"CALLED PythonScript::_inherits_script(script=<object 0x{<size_t>script:x}>)")
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef void* _instance_create(self, gd_object_t for_object):
        spy_log(f"CALLED PythonScript::_instance_create(for_object=<object 0x{<size_t>for_object:x}>)")
        # For now, return NULL as we don't have full instance support yet
        # This would need to create a Python script instance that can
        # execute the script code and handle Godot callbacks
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return NULL

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _instance_has(self, gd_object_t object):
        spy_log(f"CALLED PythonScript::_instance_has(object=<object 0x{<size_t>object:x}>)")
        # Check if the given object is an instance of this script
        # For now return False as we don't track instances yet
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _is_placeholder_fallback_enabled(self):
        spy_log("CALLED PythonScript::_is_placeholder_fallback_enabled()")
        # TODO
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _is_tool(self):
        spy_log("CALLED PythonScript::_is_tool()")
        # Check if the script contains @tool decorator or similar
        if not self._source_code:
            return False
        try:
            lines = self._source_code.split('\n')
            for line in lines:
                if line.strip().startswith('@tool') or '# tool' in line.lower():
                    return True
        except:
            pass
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _is_valid(self):
        spy_log("CALLED PythonScript::_is_valid()")
        # A script is valid if it has source code and can be compiled
        if not self._source_code:
            return False
        try:
            compile(self._source_code, '<string>', 'exec')
            return True
        except:
            return False

    # godot_extension: method(virtual=True)
    cdef void _placeholder_erased(self, void* placeholder):
        spy_log(f"CALLED PythonScript::_placeholder_erased(placeholder=<opaque ptr>)")
        # TODO
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef void* _placeholder_instance_create(self, gd_object_t for_object):
        spy_log(f"CALLED PythonScript::_placeholder_instance_create(for_object=<object 0x{<size_t>for_object:x}>)")
        # Create a placeholder instance for when the script is not ready
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return NULL

    # godot_extension: method(virtual=True)
    cdef gd_int_t _reload(self, gd_bool_t keep_state):
        spy_log(f"CALLED PythonScript::_reload(keep_state={keep_state})")
        # For basic reloading, we just validate the source code
        if self._is_valid():
            return Error.OK
        else:
            return Error.FAILED

    # godot_extension: method(virtual=True)
    cdef void _set_source_code(self, gd_string_t code):
        self._source_code = gdapi.gd_string_to_pystr(&code)
        spy_log(f"CALLED PythonScript::_set_source_code(code={self._source_code!r})")
        gd_string_del(&code)

    # godot_extension: method(virtual=True)
    cdef void _update_exports(self):
        spy_log("CALLED PythonScript::_update_exports()")
        # Update exported properties by analyzing the script
        # This could parse decorators like @export in the Python code
        # For now, just acknowledge the call
        pass

    # godot_extension: generate_class_code()

# godot_extension: generate_module_code()
