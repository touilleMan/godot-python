from cpython.mem cimport PyMem_Malloc, PyMem_Free
from threading import Lock
from contextlib import contextmanager

from godot.hazmat.gdextension_interface cimport *
from godot.classes cimport BaseGDObject


# LibGodot API
cdef extern from *:
    """
    typedef struct {
        const char* key;
        void* val;
    } LibGodotExtensionParameter;

    GDExtensionObjectPtr libgodot_create_godot_instance(int p_argc, char *p_argv[], GDExtensionInitializationFunction p_init_func, LibGodotExtensionParameter *p_params);
    void libgodot_destroy_godot_instance(GDExtensionObjectPtr p_godot_instance);
    """

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

    cdef BaseGDObject instance
    try:
        from godot.classes import GodotInstance
        instance = GodotInstance.__new__(GodotInstance)
        _libgodot_instance = instance

        _libgodot_init_lock.release()

        yield instance

    finally:
        with _libgodot_init_lock:
            libgodot_destroy_godot_instance(instance._gd_ptr)
            _libgodot_instance = None


cdef GDExtensionObjectPtr _create_godot_instance(argv: list[str]):
    # Convert argv Python `list[str]` into C `char*[]`
    pybytes_argv = [
        a.encode("utf8") for a in argv
    ]
    cdef int length = len(argv)
    cdef char **c_argv = <char **>PyMem_Malloc(length * sizeof(char*))
    assert c_argv != NULL
    try:
        for i in range(length):
            c_argv[i] = <char*>pybytes_argv

        # `c_argv` is ready, now we can initialize Godot instance !
        return libgodot_create_godot_instance(
            len(argv),
            c_argv,
            _gdpy_init,
            NULL
        )

    finally:
        PyMem_Free(c_argv)


#
# Callbacks used by Godot on instance creation
#


# Those symbols are defined in `gdpy_gdextension_ptrs.c` which is
# going to be compiled together with this file into a single shared library.
cdef extern from *:
    """
    void init_gdpy_gdextension();
    """

    const GDExtensionInterfaceGetProcAddress gdpy_gdptr_get_proc_address
    const GDExtensionClassLibraryPtr gdpy_gdptr_library
    void init_gdpy_gdextension()


cdef GDExtensionBool _gdpy_init(
    GDExtensionInterfaceGetProcAddress p_get_proc_address,
    GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) noexcept with gil:
    print('[libgodot] gdpy_init()', flush=True)

    # `gdpy_gdptr_*` must be set as early as possible given it is never
    # null-pointer checked, especially in the Cython modules.
    # Note we start by setting only `get_proc_address`&`library` since it is the
    # minimum we need to check Godot compatibility, and only after that we proceed
    # with the rest of the pointers.
    gdpy_gdptr_get_proc_address = p_get_proc_address
    gdpy_gdptr_library = p_library

    # Initialize the rest of the `gdpy_gdptr_*` pointers
    init_gdpy_gdextension()

    # Initialize as early as possible, this way we can have 3rd party plugins written
    # in Python/Cython that can do things at this level
    r_initialization.minimum_initialization_level  = GDEXTENSION_INITIALIZATION_CORE
    r_initialization.userdata = NULL
    r_initialization.initialize = _initialize
    r_initialization.deinitialize = _deinitialize


cdef void _initialize(void *userdata, GDExtensionInitializationLevel p_level) noexcept with gil:
    print(f'[libgodot] _initialize({p_level})', flush=True)

    import godot._lang
    gdpy_initialize = <void (*)(int)><size_t>godot._lang.gdpy_initialize_function_ptr
    gdpy_initialize(p_level);


cdef void _deinitialize(void *userdata, GDExtensionInitializationLevel p_level) noexcept with gil:
    print(f'[libgodot] _deinitialize({p_level})', flush=True)

    import godot._lang
    gdpy_deinitialize = <void (*)(int)><size_t>godot._lang.gdpy_deinitialize_function_ptr
    gdpy_deinitialize(p_level);
