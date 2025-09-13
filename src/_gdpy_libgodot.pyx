from libc.stdlib cimport malloc, free
from threading import Lock
from contextlib import contextmanager

from godot.hazmat.gdextension_interface cimport *
from godot.classes cimport BaseGDObject


# LibGodot API
cdef extern from "*":
    ctypedef struct LibGodotExtensionParameter:
        const char* key
        void* val

    GDExtensionObjectPtr libgodot_create_godot_instance(int p_argc, char *p_argv[], GDExtensionInitializationFunction p_init_func, LibGodotExtensionParameter *p_params)
    void libgodot_destroy_godot_instance(GDExtensionObjectPtr p_godot_instance)


# Godot uses global variables, hence only a single instance can be created
cdef object _libgodot_instance = None
cdef object _libgodot_init_lock = Lock()


@contextmanager
def create_godot_instance(argv: list[str]):
    global _libgodot_instance

    _libgodot_init_lock.acquire()

    if _libgodot_instance is not None:
        raise RuntimeError(f"Only a single instance of Godot can exist at once ! ({_libgodot_instance!r} already exist)")

    cdef GDExtensionObjectPtr gd_instance = _create_godot_instance(argv)
    if gd_instance == NULL:
        raise RuntimeError("Failed to create Godot instance")

    try:
        from godot.classes import GodotInstance
        cdef BaseGDObject instance = GodotInstance.__new__(GodotInstance)
        _libgodot_instance = instance

        _libgodot_init_lock.release()

        yield instance

    finally:
        with _libgodot_init_lock:
            libgodot_destroy_godot_instance(instance._gd_instance)
            _libgodot_instance = None


cdef GDExtensionObjectPtr _create_godot_instance(argv: list[str]):
    # Convert argv Python `list[str]` into C `char*[]`
    pybytes_argv = [
        a.encode("utf8") for a in argv
    ]
    cdef int length = len(argv)
    cdef char **c_argv = <char **>malloc(length * sizeof(char*))
    assert c_argv != NULL
    try:
        for i in range(length):
            c_argv[i] = <const char*>pybytes_argv

        # `c_argv` is ready, now we can initialize Godot instance !
        return libgodot_create_godot_instance(
            len(argv),
            c_argv,
            pythonscript_init,
            NULL
        )

    finally:
        free(c_argv)


#
# Callbacks used by Godot on instance creation
#


# Those symbols are defined in `pythonscript_gdextension_ptrs.c` which is
# going to be compiled together with this file into a single shared library.
cdef extern from "*":
    const GDExtensionInterfaceGetProcAddress pythonscript_gdptr_get_proc_address
    const GDExtensionClassLibraryPtr pythonscript_gdptr_library
    void init_pythonscript_gdextension()


cdef public GDExtensionBool pythonscript_init(
    const GDExtensionInterfaceGetProcAddress p_get_proc_address,
    const GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
):
    print('[libgodot] pythonscript_init()', flush=True)

    # `pythonscript_gdptr_*` must be set as early as possible given it is never
    # null-pointer checked, especially in the Cython modules.
    # Note we start by setting only `get_proc_address`&`library` since it is the
    # minimum we need to check Godot compatibility, and only after that we proceed
    # with the rest of the pointers.
    pythonscript_gdptr_get_proc_address = p_get_proc_address
    pythonscript_gdptr_library = p_library

    # Initialize the rest of the `pythonscript_gdptr_*` pointers
    init_pythonscript_gdextension()

    # Initialize as early as possible, this way we can have 3rd party plugins written
    # in Python/Cython that can do things at this level
    r_initialization.minimum_initialization_level  = GDEXTENSION_INITIALIZATION_CORE
	r_initialization.userdata = NULL
    r_initialization.initialize = _initialize
    r_initialization.deinitialize = _deinitialize


cdef void _initialize(void *userdata, GDExtensionInitializationLevel p_level):
    print(f'[libgodot] _initialize({p_level})', flush=True)

    import godot._lang
    pythonscript_initialize = <void(*)(int)>godot._lang.pythonscript_initialize_function_ptr
    pythonscript_initialize(p_level);


cdef void _deinitialize(void *userdata, GDExtensionInitializationLevel p_level):
    print(f'[libgodot] _deinitialize({p_level})', flush=True)

    import godot._lang
    pythonscript_deinitialize = <void(*)(int)>godot._lang.pythonscript_deinitialize_function_ptr
    pythonscript_deinitialize(p_level);
