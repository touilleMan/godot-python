# from _pythonscript import pythonscript_gdapi

from godot._hazmat.gdnative_interface cimport GDNativeInterface

cdef extern from * nogil:
    # Global variables defined in _pythonscript.pyx
    # Given _pythonscript.pyx is always the very first module loaded, we are
    # guanteed `pythonscript_gdapi` symbol is always resolved
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
