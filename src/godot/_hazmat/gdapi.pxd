from godot._hazmat.gdnative_interface cimport GDNativeInterface


cdef extern from * nogil:
    # Global variables defined in pythonscript.c
    # Just easier to inline the definitions instead of use a header file
    # and having to tweak compile flags.
    """
    #include <godot/gdnative_interface.h>
    #ifdef _WIN32
    # define PYTHONSCRIPT_IMPORT __declspec(dllimport)
    #else
    # define PYTHONSCRIPT_IMPORT
    #endif
    PYTHONSCRIPT_IMPORT extern const GDNativeInterface *gdapi;
    """

    cdef const GDNativeInterface *gdapi
