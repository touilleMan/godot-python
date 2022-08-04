from godot._hazmat.gdnative_interface cimport GDNativeInterface


cdef extern from * nogil:
    # Global variables defined in `pythonscript.c`
    # Given `libpythonscript.so` is responsible for initializing the Python
    # interpreter, we are guanteed `pythonscript_gdapi` symbol is always
    # resolved and set to a non-null value \o/
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
