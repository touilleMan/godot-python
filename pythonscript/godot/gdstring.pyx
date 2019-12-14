# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport godot_string
from godot._hazmat.conversion cimport godot_string_to_pyobj, pyobj_to_godot_string


@cython.final
cdef class GDString:

    def __init__(self, str pystr=None):
        if not pystr:
            gdapi.godot_string_new(&self._gd_data)
        else:
            pyobj_to_godot_string(pystr, &self._gd_data)

    def __dealloc__(self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi.godot_string_destroy(&self._gd_data)

    @staticmethod
    cdef inline GDString new():
        # Call to __new__ bypasses __init__ constructor
        cdef GDString ret = GDString.__new__(GDString)
        gdapi.godot_string_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline GDString new_with_pystr(str pystr):
        # Call to __new__ bypasses __init__ constructor
        cdef GDString ret = GDString.__new__(GDString)
        pyobj_to_godot_string(pystr, &ret._gd_data)
        return ret

    @staticmethod
    cdef inline GDString from_ptr(const godot_string *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef GDString ret = GDString.__new__(GDString)
        # `godot_string` is a cheap structure pointing on a refcounted vector
        # of variants. Unlike it name could let think, `godot_string_new_copy`
        # only increment the refcount of the underlying structure.
        gdapi.godot_string_new_copy(&ret._gd_data, _ptr)
        return ret

    def __repr__(self):
        return f"<GDString({str(self)!r})>"

    # Operators

    def __str__(self):
        return godot_string_to_pyobj(&self._gd_data)

    def __eq__(self, other):
        return str(self) == str(other)
