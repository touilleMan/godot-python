#include <stdio.h>
#include <godot/gdextension_interface.h>

#ifdef _WIN32
# define DLL_EXPORT __declspec(dllexport)
# define DLL_IMPORT __declspec(dllimport)
#else
# define DLL_EXPORT
# define DLL_IMPORT
#endif

// Flush before and after print to avoid out-of-order output from previous prints
#define flush_print(msg) \
    fflush(NULL); \
    printf(msg); \
    fflush(NULL)

static void _initialize(void *userdata, GDExtensionInitializationLevel p_level) {
    if (p_level != GDEXTENSION_INITIALIZATION_SERVERS) {
        return;
    }
    flush_print("My GDExtension initialize\n");
}

static void _deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
    if (p_level != GDEXTENSION_INITIALIZATION_SERVERS) {
        return;
    }
    flush_print("My GDExtension deinitialize\n");
}

DLL_EXPORT GDExtensionBool my_init(
    const GDExtensionInterfaceGetProcAddress p_get_proc_address,
    const GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
    flush_print("My GDExtension entry point call\n");

    r_initialization->minimum_initialization_level  = GDEXTENSION_INITIALIZATION_SERVERS;
	r_initialization->userdata = NULL;
    r_initialization->initialize = _initialize;
    r_initialization->deinitialize = _deinitialize;

    return 1;
}
