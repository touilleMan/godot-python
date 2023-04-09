# cython: language_level=3

from godot.hazmat.gdapi cimport *


def initialize(level):
    print("MY initialize", level)


def deinitialize(level):
    print("MY deinitialize", level)


cdef public void _my_initialize(void *userdata, GDExtensionInitializationLevel p_level) with gil:
    print("==> _initialize")


cdef extern void _my_deinitialize(void *userdata, GDExtensionInitializationLevel p_level) with gil:
    print("==> _deinitialize")


cdef extern GDExtensionBool _my_init(
    const GDExtensionInterface *p_interface,
    const GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) nogil:
    # print("==> _my_init")
    r_initialization.minimum_initialization_level  = GDEXTENSION_INITIALIZATION_SERVERS
    r_initialization.userdata = NULL
    #  r_initialization.initialize = _my_initialize
    #  r_initialization.deinitialize = _my_deinitialize
    return True


cdef extern from * nogil:
    """
    #include <godot/gdextension_interface.h>
    #ifdef _WIN32
    # define DLL_EXPORT __declspec(dllexport)
    #else
    # define DLL_EXPORT
    #endif

    GDExtensionBool _my_init(const GDExtensionInterface *, const GDExtensionClassLibraryPtr, GDExtensionInitialization *);
    DLL_EXPORT GDExtensionBool my_init(
        const GDExtensionInterface *p_interface,
        const GDExtensionClassLibraryPtr p_library,
        GDExtensionInitialization *r_initialization
    ) {
        return _my_init(p_interface, p_library, r_initialization);
    }
    """
