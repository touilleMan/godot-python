from godot._hazmat.gdnative_interface cimport GDNativeInterface


cdef extern from * nogil:
    # Global variables defined in _pythonscript.pyx
    # Just easier to inline the definitions instead of use a header file
    # and having to tweak compile flags.
    """
    #include <godot/gdnative_interface.h>
    #ifdef _WIN32
    # define DLL_IMPORT __declspec(dllimport)
    #else
    # define DLL_IMPORT
    #endif
    DLL_IMPORT extern const GDNativeInterface *pythonscript_gdapi;
    """

    cdef const GDNativeInterface *pythonscript_gdapi
